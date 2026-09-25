#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Блок «Смежные проекты» на кейс-страницах.

Зачем: замер 19.09.2026 (SEO-PLAN.md) показал, что на 54 страницах меньше 20
внутренних ссылок, то есть только шапка и подвал. У сайтов из топа Яндекса
70–280. Кейс сейчас тупик: посетитель дочитал и ушёл, вес страницы никуда
не передаётся.

Блок ставится перед формой заявки (<a id="lead">): ссылка на страницу услуги
и три соседних кейса того же направления. Соседей берём по кругу от текущего,
чтобы ссылки расходились по каталогу, а не сходились на первых трёх кейсах.

    python3 scripts/a2/add_related_links.py

Идемпотентен (маркер hm-related). Пост-скрипт: его гоняет finalize_page.py
после генератора, иначе регенерация страницы блок потеряет.
"""
import html as H
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
MIRROR = os.path.join(ROOT, 'mirror')
CASES = json.load(open(os.path.join(ROOT, 'src', 'data', 'cases.json'), encoding='utf-8'))


def covers():
    """Обложки берём из карусели каталога, а не из cases.json: там у половины кейсов
    путь на /assets/** (React-сборка, зеркалу недоступна), и у двенадцати он вдобавок
    один и тот же файл-заглушка. В карусели у каждого кейса своя круглая обложка."""
    car = open(os.path.join(HERE, 'carousels', 'all.html'), encoding='utf-8').read()
    return {m.group(1).rstrip('/'): m.group(2) for m in
            re.finditer(r'<a class="mcase" href="([^"]+)"[^>]*>.*?<img[^>]+src="([^"]+)"',
                        car, re.S)}


COVERS = covers()
MARK = 'hm-related'
# якорь формы: у кастомных страниц <a id="lead">, у тильдовских своя запись формы,
# у части кейсов только фиолетовая секция CTA из общего шелла
ANCHORS = ('<a id="lead">', '<div id="rec237885363"', '<section class="mh-form',
           '<section class="hm-cta"')

SERVICE = {  # направление -> (страница услуги, как её назвать в блоке, цвет)
    'video': ('/videoproduction/', 'Видеопродакшн', '#CF6F19'),
    'event': ('/event/', 'Организация мероприятий', '#C12164'),
    'creative': ('/creativedesign/', 'Креатив и дизайн', '#C12164'),
    'digital': ('/digital/', 'Digital и сайты', '#2F6FC4'),
    'photo': ('/photo/', 'Фотопродакшн', '#4CA4E8'),
    '3dmapping': ('/3dmapping/', '3D Mapping', '#7E3FA0'),
}

CSS = """<style id="hm-related-css">
.hm-rel{font-family:'Montserrat',-apple-system,Arial,sans-serif;background:#fff;color:#14171C;padding:64px 0 56px;border-top:1px solid rgba(20,23,28,.1)}
.hm-rel__in{max-width:1180px;margin:0 auto;padding:0 40px}
.hm-rel__h{margin:0 0 6px;font-size:clamp(21px,2.4vw,28px);font-weight:800;letter-spacing:-.02em}
.hm-rel__lead{margin:0 0 26px;font-size:15.5px;line-height:1.6;color:#5A616A}
.hm-rel__lead a{color:var(--rel-a);font-weight:700}
.hm-rel__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.hm-rel__c{display:flex;flex-direction:column;border:1px solid rgba(20,23,28,.1);border-radius:16px;overflow:hidden;text-decoration:none;color:inherit;background:#fff;transition:transform .2s,border-color .2s}
.hm-rel__c:hover{transform:translateY(-3px);border-color:var(--rel-a)}
.hm-rel__c img{width:100%;height:190px;object-fit:contain;background:#F7F4F1;display:block;padding:10px 0}
@media(max-width:600px){.hm-rel__c img{height:220px}}
.hm-rel__b{padding:14px 16px 18px}
.hm-rel__cl{display:block;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--rel-a);margin-bottom:6px}
.hm-rel__t{display:block;font-size:15px;font-weight:700;line-height:1.4}
.hm-rel__dirs{margin:26px 0 0;padding:20px 0 0;border-top:1px solid rgba(20,23,28,.1);font-size:14.5px;line-height:1.9;color:#5A616A}
.hm-rel__dirs b{display:block;margin-bottom:6px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#14171C}
.hm-rel__dirs a{color:#14171C;text-decoration:none;border-bottom:1px solid rgba(20,23,28,.25);margin-right:6px}
.hm-rel__dirs a:hover{color:var(--rel-a);border-color:var(--rel-a)}
@media(max-width:900px){.hm-rel__grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.hm-rel__in{padding:0 18px}.hm-rel__grid{grid-template-columns:1fr}}
</style>"""


# сквозной список направлений: кейс перестаёт быть тупиком и раздаёт вес услугам
DIRECTIONS = [
    ('/videoproduction/', 'Видеопродакшн'), ('/event/', 'Мероприятия'),
    ('/exhibition/', 'Выставочные стенды'), ('/content/', 'Мультимедийный контент'),
    ('/3dmapping/', '3D Mapping'), ('/creativedesign/', 'Креатив и дизайн'),
    ('/printandproduction/', 'Печать и производство'), ('/photo/', 'Фотопродакшн'),
    ('/btl/', 'BTL и промо'), ('/digital/', 'Digital и сайты'),
    ('/price/', 'Цены'), ('/reviews/', 'Отзывы'), ('/team/', 'Команда'),
]

# посадочные под конкретный запрос: без ссылок с кейсов у них было по 1–3
# входящих против 9–14 у кейсов, и Яндекс видел их почти сиротами (замер 25.09.2026)
FORMATS = {
    'video': [('/videoproduction/reklamnyy-rolik/', 'Съёмка рекламного ролика'),
              ('/videoproduction/korporativnyy-film/', 'Корпоративный фильм о компании'),
              ('/videoproduction/prezentacionnyy-rolik/', 'Презентационный ролик объекта')],
    'event': [('/event/novogodniy-korporativ/', 'Новогодний корпоратив под ключ'),
              ('/exhibition/multimedia/', 'Мультимедиа для выставочного стенда')],
    'creative': [('/creativedesign/brandbook/', 'Разработка брендбука и фирменного стиля')],
    '3dmapping': [('/exhibition/multimedia/', 'Мультимедиа для выставочного стенда')],
}


def ru(t):
    """Прямые кавычки в названиях кейсов из каталога заменяем на ёлочки:
    на странице рядом стоит наш текст, и разнобой заметен."""
    out, opened = [], False
    for ch in t:
        if ch == '"':
            out.append('«' if not opened else '»')
            opened = not opened
        else:
            out.append(ch)
    return ''.join(out)


def block(case, siblings):
    href, label, accent = SERVICE[case['category']]
    dirs = ''.join(f'<a href="{h}">{t}</a>' for h, t in DIRECTIONS
                   if h.rstrip('/') != href.rstrip('/'))
    formats = ''
    if FORMATS.get(case['category']):
        formats = ('<p class="hm-rel__dirs"><b>Отдельно по задачам</b>'
                   + ''.join(f'<a href="{h}">{t}</a>' for h, t in FORMATS[case['category']])
                   + '</p>')
    cards = ''
    for s in siblings:
        cover = COVERS.get(s['route'].rstrip('/'), s['cover'])
        cards += (f'<a class="hm-rel__c" href="{s["route"]}/">'
                  f'<img src="{cover}" alt="{H.escape(s["client"])}. {H.escape(ru(s["title"]))}" '
                  f'loading="lazy" width="600" height="600">'
                  f'<span class="hm-rel__b"><span class="hm-rel__cl">{H.escape(s["client"])}</span>'
                  f'<span class="hm-rel__t">{H.escape(ru(s["title"]))}</span></span></a>')
    return (f'<!-- {MARK} -->{CSS}'
            f'<section class="hm-rel" style="--rel-a:{accent}" aria-label="Смежные проекты">'
            f'<div class="hm-rel__in">'
            f'<h2 class="hm-rel__h">Похожие проекты</h2>'
            f'<p class="hm-rel__lead">Этот кейс из направления '
            f'<a href="{href}">{label}</a>. Рядом лежат проекты, где мы решали похожие задачи.</p>'
            f'<div class="hm-rel__grid">{cards}</div>'
            f'{formats}'
            f'<p class="hm-rel__dirs"><b>Все направления</b>{dirs}</p>'
            f'</div></section><!-- /{MARK} -->')


def strip_old(s):
    return re.sub(r'<!-- ' + MARK + r' -->.*?<!-- /' + MARK + r' -->', '', s, flags=re.S)


def main():
    # /samara_vdnh это неканоническая копия /portfolio/samara-stand-vdnh: обложки
    # в каталоге у неё нет, а cover из cases.json ведёт на /assets/** и отдаёт 404.
    # В соседи такие страницы не берём, сами блок получают
    shown = [c for c in CASES if c['route'].rstrip('/') in COVERS]
    by_cat = {}
    for c in shown:
        by_cat.setdefault(c['category'], []).append(c)

    done = skipped = 0
    for c in CASES:
        group = by_cat.get(c['category'], [])
        if len(group) < 2:
            continue  # направление из одного кейса: соседей нет, блок был бы пустым
        i = group.index(c) if c in group else -1
        siblings = [group[(i + k) % len(group)] for k in range(1, min(7, len(group)))]
        path = os.path.join(MIRROR, c['route'].strip('/'), 'index.html')
        a2 = os.path.join(MIRROR, c['route'].strip('/'), 'index-a2.html')
        for p in (a2, path):
            if not os.path.isfile(p):
                continue
            s = open(p, encoding='utf-8').read()
            s = strip_old(s)
            anchor = next((a for a in ANCHORS if a in s), None)
            if not anchor:
                skipped += 1
                print(f'{c["route"]} ({os.path.basename(p)}): нет якоря формы — пропуск')
                continue
            s = s.replace(anchor, block(c, siblings) + anchor, 1)
            open(p, 'w', encoding='utf-8').write(s)
            done += 1
    print(f'Готово: файлов {done}, пропущено {skipped}')


if __name__ == '__main__':
    main()
