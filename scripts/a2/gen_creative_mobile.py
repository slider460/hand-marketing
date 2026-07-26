#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Мобильные версии кейсов «Креатив» (mirror/creative/**) — реконструкция уникальной
десктопной вёрстки вместо шаблона-галереи (маркер hm-creative-mob).

Каждый кейс на десктопе свёрстан уникально (Zero-артборд + Tilda-галереи).
Скрипт разбирает рекорды и строит мобильный поток, повторяющий ЛОГИКУ вёрстки:
- Zero-артборд: элементы сортируются по top, кластеризуются в ряды; ряд из
  нескольких картинок -> сетка, одиночная -> во всю ширину; тексты в потоке
  (fs>=28 -> заголовок), включая повёрнутые ярлыки «Задача/Решение»; шейпы с
  background-image выводятся как картинки, декор-шейпы пропускаются; тёмный фон
  артборда сохраняется (секция с фоном + белый текст).
- T670 (карусель) -> горизонтальный свайп со всеми слайдами.
- T410 (до/после) -> слайдер сравнения (разметка mh-ba, стили/JS уже на странице).
Все data-original поднимаются до оригиналов, отсутствующие файлы логируются.
Попутно sr-only <h1> (сырой Tilda-титул) заменяется русским из cases.json.

Заменяется середина .mhome: от конца секции mh-hero до <section class="mh-form".
Идемпотентен. Откат: git checkout mirror/creative/ + перезапуск нужных скриптов.
"""
import io, json, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MARK = "hm-creative-mob"

cases = json.load(open(os.path.join(ROOT, "src", "data", "cases.json"), encoding="utf-8"))
TITLE = {c["route"].strip("/"): c["title"] for c in cases}

PAGES = [r["route"].strip("/") for r in cases if r["category"] == "creative"]

CSS = """<style data-%(m)s="css">@media (max-width:640px){
.cmb{overflow:hidden}
.cmb__sec{padding:26px 0 6px}
.cmb__sec--dark{color:#fff}
.cmb__sec--dark h2,.cmb__sec--dark p{color:#fff}
.cmb h2{font-size:26px;font-weight:800;padding:0 20px;margin:18px 0 10px}
.cmb h3{font-size:19px;font-weight:700;padding:0 20px;margin:16px 0 8px}
.cmb p{margin:10px 0;padding:0 20px;font-size:15.5px;line-height:1.6;color:#454C54}
.cmb__sec--dark p{color:rgba(255,255,255,.88)}
.cmb__img{padding:6px 14px}
.cmb__img img{width:100%;height:auto;border-radius:14px;box-shadow:0 14px 30px -16px rgba(20,23,28,.35)}
/* плоская графика (лого, вордмарк) — без карточки: тень/скругление вокруг
   прозрачного PNG выглядят как посторонний серый прямоугольник */
.cmb__img--flat{padding:10px 20px}
.cmb__img--flat img{border-radius:0;box-shadow:none}
/* логотип клиента — компактный знак в потоке, а не баннер во всю ширину */
.cmb__logo{padding:12px 20px 16px;line-height:0}
.cmb__logo img{display:block;width:auto;height:auto;max-width:min(60%,200px);max-height:64px;object-fit:contain;object-position:left center;border-radius:0;box-shadow:none}
.cmb__grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:6px 14px}
.cmb__grid img{width:100%;height:auto;border-radius:12px}
.cmb__slider{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding:8px 14px 14px}
.cmb__slider::-webkit-scrollbar{display:none}
.cmb__slider>img{flex:0 0 86vw;max-width:420px;scroll-snap-align:center;border-radius:14px;height:auto;object-fit:contain;align-self:center}
.cmb__hint{padding:0 20px;font-size:12.5px;color:#8A909A;margin:0 0 8px}
.cmb__textimg img{max-width:60%;height:auto;margin:6px 0}
}</style>"""


def norm_url(u):
    u = re.sub(r"^(\.\./)+", "/", u.strip())
    if not u.startswith("/"):
        u = "/" + u
    return u


def img_exists(u):
    return os.path.exists(os.path.join(ROOT, "mirror", u.lstrip("/")))


_FLAT_CACHE = {}


def is_flat(u):
    """Плоская графика (лого/вордмарк на прозрачном или белом фоне)?

    Такую картинку нельзя раздувать во всю ширину карточкой с тенью: получается
    гигантский баннер, а тень ложится прямоугольником вокруг прозрачного PNG.
    Растр читаем через PIL; SVG и всё, что не открылось, считаем фото."""
    if u in _FLAT_CACHE:
        return _FLAT_CACHE[u]
    flat = False
    try:
        from PIL import Image
        from collections import Counter
        im = Image.open(os.path.join(ROOT, "mirror", u.lstrip("/"))).convert("RGBA")
        im.thumbnail((200, 200))
        px = list(im.getdata())
        n = len(px)
        transp = sum(1 for r, g, b, a in px if a < 16)
        opaque = [(r, g, b) for r, g, b, a in px if a >= 200]
        white = sum(1 for r, g, b in opaque if r > 243 and g > 243 and b > 243)
        ink = [c for c in opaque if not (c[0] > 243 and c[1] > 243 and c[2] > 243)]
        ncol = len(Counter((r >> 4, g >> 4, b >> 4) for r, g, b in ink))
        flat = (transp + white) / n > 0.6 and ncol <= 90 and len(ink) / n < 0.35
    except Exception:
        flat = False
    _FLAT_CACHE[u] = flat
    return flat


def is_dark(bg):
    m = re.match(r"#([0-9a-fA-F]{6})", bg or "")
    if not m:
        return False
    r, g, b = (int(m.group(1)[k:k+2], 16) for k in (0, 2, 4))
    return (0.299*r + 0.587*g + 0.114*b) < 110


def parse_zero(seg, rid, log):
    """Элементы артборда -> список dict(top,left,w,h,kind,payload)."""
    els = []
    marks = [m for m in re.finditer(r"<div class='t396__elem tn-elem[^']*' data-elem-id='(\d+)' data-elem-type='(\w+)'([^>]*)>", seg)]
    for k, m in enumerate(marks):
        eid, et, attrs = m.groups()
        end = marks[k+1].start() if k+1 < len(marks) else len(seg)
        body = seg[m.end():end]

        def fv(name, d=None):
            mm = re.search(r'data-field-%s-value="([^"]*)"' % name, attrs)
            return mm.group(1) if mm else d
        try:
            top = float(fv("top", 0) or 0); left = float(fv("left", 0) or 0); w = float(fv("width", 0) or 0)
        except ValueError:
            continue
        fw, fh = fv("filewidth"), fv("fileheight")
        fs = float(fv("fontsize", 0) or 0)

        if et == "image":
            src = re.search(r"data-original=['\"]([^'\"]+)['\"]", body)
            if not src:
                continue
            u = norm_url(src.group(1))
            if not img_exists(u):
                log.append("НЕТ ФАЙЛА (image): " + u); continue
            hh = w * float(fh) / float(fw) if fw and fh and float(fw) else w * 0.7
            if w < 90:   # мелкий декор
                continue
            els.append(dict(top=top, left=left, w=w, h=hh, kind="img", src=u))
        elif et == "text":
            am = re.search(r"<div class='tn-atom'[^>]*>(.*?)</div>\s*</div>\s*$", body, re.S) or \
                 re.search(r"<div class='tn-atom'[^>]*>(.*)", body, re.S)
            if not am:
                continue
            html = am.group(1)
            html = re.sub(r"<script.*?</script>", "", html, flags=re.S)
            html = re.sub(r"<style.*?</style>", "", html, flags=re.S)
            html = re.sub(r"<script.*$", "", html, flags=re.S)
            # поднять ленивые картинки внутри текста
            html = re.sub(r"<img[^>]*data-original='([^']+)'[^>]*>",
                          lambda mm: '<img src="%s" alt="">' % norm_url(mm.group(1)), html)
            html = re.sub(r"\s(?:field|imgfield|data-redactor-[a-z]+)='[^']*'", "", html)
            # только inline-разметка: блочные теги ломают дерево (<div> внутри <p>
            # закрывает p, а лишние </div> выбивают mh-form из #mhome)
            html = re.sub(r"</?(?:div|p|section|ul|ol|li|h\d|table|tr|td)[^>]*>", " ", html)
            html = re.sub(r"(?:\s*<br\s*/?>\s*){3,}", "<br><br>", html)
            plain = re.sub(r"<[^>]+>", " ", html)
            plain = re.sub(r"(?:&nbsp;| |\s)+", " ", plain).strip()
            if not plain and "<img" not in html:
                continue
            nl = max(1, len(plain) / max(10, w / (fs * 0.55 or 9)))
            els.append(dict(top=top, left=left, w=w, h=max(fs * 1.3, fs * 1.3 * nl), kind="txt",
                            html=html.strip(), fs=fs, plain=plain))
        elif et == "shape":
            bgm = re.search(r"background-image:\s*url\('([^']+)'\)", body) or \
                  re.search(r"data-original=['\"]([^'\"]+)['\"]", body)
            if bgm and w >= 120:
                u = norm_url(bgm.group(1))
                if img_exists(u):
                    els.append(dict(top=top, left=left, w=w, h=w * 0.7, kind="img", src=u))
                else:
                    log.append("НЕТ ФАЙЛА (shape): " + u)
    return els


def rows_of(els):
    """Кластеризация в ряды по вертикальному перекрытию."""
    rows = []
    for e in sorted(els, key=lambda x: (x["top"], x["left"])):
        if rows:
            last = rows[-1]
            bottom = max(x["top"] + x["h"] for x in last)
            tops = min(x["top"] for x in last)
            if e["top"] < bottom - 8 and e["top"] - tops < 900:
                last.append(e); continue
        rows.append([e])
    return rows


def el_html(e):
    if e["kind"] == "img":
        if is_flat(e["src"]):
            # мелкая плоская графика в макете = логотип клиента -> компактный знак
            if e["w"] <= 460:
                return ('<div class="cmb__logo"><img src="%s" alt="Логотип клиента" '
                        'loading="lazy"></div>' % e["src"])
            return ('<div class="cmb__img cmb__img--flat"><img src="%s" alt="" '
                    'loading="lazy"></div>' % e["src"])
        return '<div class="cmb__img"><img src="%s" alt="" loading="lazy"></div>' % e["src"]
    if "<img" in e["html"]:
        return '<div class="cmb__textimg"><p>%s</p></div>' % e["html"]
    if e["fs"] >= 34:
        return "<h2>%s</h2>" % e["html"]
    if e["fs"] >= 24:
        return "<h3>%s</h3>" % e["html"]
    return "<p>%s</p>" % e["html"]


def flow_sort(items):
    """Порядок чтения: по top; при почти равных top заголовок раньше текста, затем left."""
    def key(e):
        head = e["kind"] == "txt" and e.get("fs", 0) >= 24
        return (e["top"] - (18 if head else 0), e["left"])
    return sorted(items, key=key)


def lcluster(row):
    """Кластеры по горизонтальному пересечению интервалов [left, left+w]."""
    clusters = []
    for e in sorted(row, key=lambda x: x["left"]):
        a1, a2 = e["left"], e["left"] + e["w"]
        placed = False
        for c in clusters:
            b1, b2 = c["a"], c["b"]
            ov = min(a2, b2) - max(a1, b1)
            if ov > 0.2 * min(e["w"], b2 - b1):
                c["a"], c["b"] = min(a1, b1), max(a2, b2)
                c["els"].append(e); placed = True; break
        if not placed:
            clusters.append(dict(a=a1, b=a2, els=[e]))
    return clusters


def render_zero(els):
    out = []
    for row in rows_of(els):
        # парные ярлыки («Задача» | «Решение») на одном уровне -> две колонки
        heads = [e for e in row if e["kind"] == "txt" and e.get("fs", 0) >= 24]
        if len(heads) == 2 and abs(heads[0]["top"] - heads[1]["top"]) < 60 \
                and abs(heads[0]["left"] - heads[1]["left"]) > 300:
            mid = (heads[0]["left"] + heads[1]["left"]) / 2 + 80
            cols = ([e for e in row if e["left"] < mid], [e for e in row if e["left"] >= mid])
            for c in cols:
                # ярлык колонки («Задача»/«Решение») всегда первым
                for e in sorted(c, key=lambda x: (not (x["kind"] == "txt" and x.get("fs", 0) >= 24), x["top"], x["left"])):
                    out.append(el_html(e))
            continue
        cl = lcluster(row)
        if len(cl) >= 2 and all(len(c["els"]) > 1 for c in cl):
            # независимые колонки (напр. «Задача» | «Решение») — каждую целиком
            for c in cl:
                for e in flow_sort(c["els"]):
                    out.append(el_html(e))
        else:
            # единый поток; ряды из нескольких картинок подряд — сеткой
            seq = flow_sort(row)
            i = 0
            while i < len(seq):
                if seq[i]["kind"] == "img":
                    grp = [seq[i]]
                    while i + 1 < len(seq) and seq[i+1]["kind"] == "img" and \
                            abs(seq[i+1]["top"] - grp[0]["top"]) < 60:
                        i += 1; grp.append(seq[i])
                    if len(grp) == 1:
                        out.append(el_html(grp[0]))
                    else:
                        cols = "1fr 1fr 1fr" if len(grp) == 3 else "1fr 1fr"
                        cells = "".join('<img src="%s" alt="" loading="lazy">' % e["src"] for e in grp)
                        out.append('<div class="cmb__grid" style="grid-template-columns:%s">%s</div>' % (cols, cells))
                else:
                    out.append(el_html(seq[i]))
                i += 1
    return "".join(out)


def render_670(seg):
    imgs = []
    for m in re.finditer(r'class="t-slds__bgimg[^"]*"\s+data-original="([^"]+)"', seg):
        u = norm_url(m.group(1))
        if img_exists(u):
            imgs.append(u)
    # без дублей (клоны слайдов у зацикленных каруселей)
    seen, uniq = set(), []
    for u in imgs:
        if u not in seen:
            seen.add(u); uniq.append(u)
    if not uniq:
        return ""
    cells = "".join('<img src="%s" alt="" loading="lazy">' % u for u in uniq)
    return ('<div class="cmb__slider">%s</div>'
            '<p class="cmb__hint">листайте →</p>' % cells)


def render_410(seg):
    m = re.search(r'data-beforeafter-imgurl-first="([^"]+)"\s+data-beforeafter-imgurl-second="([^"]+)"', seg)
    if not m:
        return ""
    first, second = norm_url(m.group(1)), norm_url(m.group(2))
    if not (img_exists(first) and img_exists(second)):
        return ""
    return ('<section class="mh-sec mh-ba"><h2 style="padding:0 20px">ТЗ и дизайн</h2>'
            '<div class="mh-ba__box" data-ba>'
            '<img class="mh-ba__after" src="%s" alt="Дизайн">'
            '<div class="mh-ba__before"><img src="%s" alt="ТЗ"></div>'
            '<span class="mh-ba__lbl mh-ba__lbl_l">ТЗ</span><span class="mh-ba__lbl mh-ba__lbl_r">Дизайн</span>'
            '<span class="mh-ba__handle"></span>'
            '<input class="mh-ba__range" type="range" min="0" max="100" value="50" aria-label="Сравнить ТЗ и дизайн">'
            '</div><p class="mh-ba__hint">← потяните, чтобы сравнить →</p></section>' % (second, first))


def build_mobile(html, route, log):
    j = html.find('id="allrecords"')
    desk = html[j:]
    recs = [(m.group(1), m.group(2), m.start())
            for m in re.finditer(r'<div id="rec(\d+)"[^>]*data-record-type="(\d+)"', desk)]
    parts = []
    zero_seen = 0
    for k, (rid, rt, pos) in enumerate(recs):
        end = recs[k+1][2] if k+1 < len(recs) else len(desk)
        seg = desk[pos:end]
        if rt == "396":
            zero_seen += 1
            if zero_seen == 1 or k == len(recs) - 1:   # шапка / футер
                continue
            if "t282" in seg:
                continue
            els = parse_zero(seg, rid, log)
            if not els:
                continue
            bg = re.search(r"#rec%s \.t396__artboard \{[^}]*background-color:\s*([^;}]+)" % rid, seg)
            dark = is_dark(bg.group(1) if bg else "")
            style = ' style="background:%s"' % bg.group(1).strip() if (bg and dark) else ""
            parts.append('<div class="cmb__sec%s"%s>%s</div>'
                         % (" cmb__sec--dark" if dark else "", style, render_zero(els)))
        elif rt == "670":
            parts.append(render_670(seg))
        elif rt == "410":
            parts.append(render_410(seg))
        # 121 (форма) и 327 (бургер) — пропуск: у мобилы своя форма mh-form
    return '<div class="cmb" data-%s="1">%s</div>' % (MARK, "".join(parts))


def patch(path, route):
    html = io.open(path, encoding="utf-8").read()
    orig = html
    log = []

    mob = build_mobile(html, route, log)

    # зона замены: конец секции mh-hero ... начало mh-form
    hero = re.search(r'<section class="mh-hero.*?</section>', html, re.S)
    formm = re.search(r'<section class="mh-form', html)
    if not hero or not formm or formm.start() < hero.end():
        print("SKIP (нет hero/form):", path); return False
    html = html[:hero.end()] + CSS.replace("%(m)s", MARK) + mob + html[formm.start():]

    # sr-only h1: сырой Tilda-титул -> русский из cases.json
    t = TITLE.get(route)
    if t:
        html = re.sub(
            r'(<h1 style="position:absolute;width:1px[^"]*">)[^<]*(</h1>)',
            lambda m: m.group(1) + t + m.group(2), html, count=1)

    if html != orig:
        io.open(path, "w", encoding="utf-8").write(html)
        n_img = mob.count("<img")
        print("OK: %-32s img=%d %s" % (route, n_img, ("| " + "; ".join(log)) if log else ""))
        return True
    print("Без изменений:", path)
    return False


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    n = 0
    for route in PAGES:
        if only and only not in route:
            continue
        p = os.path.join(ROOT, "mirror", route, "index-a2.html")
        if os.path.exists(p):
            n += bool(patch(p, route))
        else:
            print("НЕТ ФАЙЛА:", p)
    print("готово, изменено:", n)
