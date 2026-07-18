#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO-батч по аудиту 18.07.2026 (идемпотентен, безопасен для повторных прогонов):
1) og:image на все страницы без него: кейсы — обложка из src/data/cases.json
   (/assets/* лежат в public/assets, деплоятся на /assets/), услуги/служебные —
   словарь OG_MAP, остальным — DEFAULT (превью главной). Относительный og:image
   главной абсолютизируется.
2) Дописаны короткие description шести страниц (DESC).
3) sr-only <h1> в статический пре-рендер 3 React-страниц /portfolio/* (маркер
   data-hm-seo-h1) — до гидрации краулер видит заголовок; вне #root, визуала нет.
Правит index.html и index-a2.html. Откат: git checkout mirror/.
"""
import io, json, os, re, glob

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SITE = "https://hand-marketing.ru"
DEFAULT_OG = SITE + "/static/thb/as3230-6663-4363-b038-333866373133/-/resize/504x/__76876-145.png"

cases = json.load(open(os.path.join(ROOT, "src", "data", "cases.json"), encoding="utf-8"))
# public/assets деплоится на прод в /case-assets/ (см. deploy.yml), НЕ в /assets/
COVER = {c["route"].strip("/"): SITE + "/case-assets/" + c["cover"].split("/")[-1] for c in cases}

# услуги/служебные с осмысленной картинкой
OG_MAP = {
    "event": SITE + "/images/event/hero-poster.jpg",
}

DESC = {
    "about": "Рекламное агентство полного цикла Hand Marketing: команда, подход и опыт с 2012 года — ивенты, выставочные стенды, видеопродакшн, мультимедийный контент, дизайн.",
    "becar_stancia": "Кейс для Becar Asset Management: посадочная страница продукта «Бизнес-центр Станция» — концепция, дизайн и вёрстка от агентства Hand Marketing.",
    "event/mozaika": "Организация мероприятия для ТРЦ «Мозаика» в Москве: концепция, шоу-программа, техническое обеспечение и продакшн под ключ — кейс ивент-агентства Hand Marketing.",
    "event/salaris": "Презентация ТРЦ «Саларис»: концепция мероприятия, площадка, шоу-программа и техническое обеспечение — кейс ивент-агентства полного цикла Hand Marketing.",
    "project": "Портфолио Hand Marketing: 40+ кейсов — ивенты, выставочные стенды, видеопродакшн, 3D-маппинг, мультимедийный контент, креатив, дизайн и полиграфия.",
    "service": "Услуги рекламного агентства полного цикла: организация мероприятий, застройка выставочных стендов, видеопродакшн, мультимедийный контент, дизайн, полиграфия, BTL и 3D-маппинг.",
}

# h1 для пре-рендеров React-страниц — тексты сняты с ЖИВОГО рантайм-h1 приложения
H1_PAGES = {
    "portfolio/samara-exhibition": "Выставка «Самара» в Музее им. П.В. Алабина",
    "portfolio/samara-stand-vdnh": "Стенд Самарской области на выставке-форуме «Россия»",
    "portfolio/stavropol-stand-vdnh": "Стенд Ставропольского края на выставке «Россия»",
}
# статика samara-exhibition несла title/description ДРУГОЙ страницы (стенд ВДНХ) —
# приводим к рантайму React (страница про выставку в музее)
TITLE_FIX = {
    "portfolio/samara-exhibition": (
        "Выставка «Самара» в Музее Алабина — Hand Marketing",
        "Выставка «Самара» в Музее им. П.В. Алабина: мультимедийная экспозиция, контент и техническое оснащение — кейс Hand Marketing.",
    ),
}
SR_ONLY = "position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0"


def patch_page(path, route):
    html = io.open(path, encoding="utf-8").read()
    orig = html

    # --- description ---
    if route in DESC:
        html = re.sub(r'(name="description" content=")[^"]*(")',
                      lambda m: m.group(1) + DESC[route] + m.group(2), html, count=1)
        # og:description при наличии — тоже
        html = re.sub(r'(property="og:description" content=")[^"]*(")',
                      lambda m: m.group(1) + DESC[route] + m.group(2), html, count=1)

    # --- og:image ---
    # фикс ранней версии скрипта: обложки вставлялись с путём /assets/ вместо /case-assets/
    html = html.replace('property="og:image" content="%s/assets/' % SITE,
                        'property="og:image" content="%s/case-assets/' % SITE)
    m = re.search(r'property="og:image" content="([^"]*)"', html)
    if m:
        url = m.group(1)
        if url and not url.startswith(("http://", "https://")):   # абсолютизировать
            html = html.replace(m.group(0), 'property="og:image" content="%s"' % (SITE + "/" + url.lstrip("/")))
    else:
        og = COVER.get(route) or OG_MAP.get(route) or DEFAULT_OG
        tag = '<meta property="og:image" content="%s">' % og
        i = html.find("</head>")
        if i > 0:
            html = html[:i] + tag + html[i:]

    # --- sr-only h1 для пре-рендеров (повторный прогон обновляет текст) ---
    if route in H1_PAGES:
        h1txt = H1_PAGES[route]
        tag = '<h1 data-hm-seo-h1 style="%s">%s</h1>' % (SR_ONLY, h1txt)
        if "data-hm-seo-h1" in html:
            html = re.sub(r'<h1 data-hm-seo-h1[^>]*>.*?</h1>', tag, html, count=1, flags=re.S)
        else:
            mb = re.search(r"<body[^>]*>", html)
            if mb:
                html = html[:mb.end()] + tag + html[mb.end():]

    # --- фикс чужого title/description статики ---
    if route in TITLE_FIX:
        t, d = TITLE_FIX[route]
        html = re.sub(r"<title>.*?</title>", "<title>%s</title>" % t, html, count=1, flags=re.S)
        html = re.sub(r'(name="description" content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), html, count=1)
        html = re.sub(r'(property="og:title" content=")[^"]*(")', lambda m: m.group(1) + t + m.group(2), html, count=1)
        html = re.sub(r'(property="og:description" content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), html, count=1)

    if html != orig:
        io.open(path, "w", encoding="utf-8").write(html)
        return True
    return False


def main():
    changed = 0
    for idx in glob.glob(os.path.join(ROOT, "mirror", "**", "index*.html"), recursive=True):
        base = os.path.basename(idx)
        if base not in ("index.html", "index-a2.html"):
            continue
        route = os.path.relpath(os.path.dirname(idx), os.path.join(ROOT, "mirror")).replace("\\", "/")
        if route == ".":
            route = ""
        # пропустить приватные клиентские страницы — им og не нужен
        if route.startswith("for/"):
            continue
        if patch_page(idx, route):
            changed += 1
    print("изменено файлов:", changed)

    # --- site.webmanifest ---
    wm = os.path.join(ROOT, "mirror", "site.webmanifest")
    data = {
        "name": "Hand Marketing — рекламное агентство полного цикла",
        "short_name": "Hand Marketing",
        "icons": [{"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}],
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "browser",
        "start_url": "/",
    }
    io.open(wm, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=1))
    print("site.webmanifest записан")


if __name__ == "__main__":
    main()
