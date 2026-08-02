#!/usr/bin/env python3
"""Готовит ассеты кейса «Брендбук Metra Technology Group» из ~/Downloads/метра.pdf.

Логотипы всех пяти брендов лежат в исходнике кривыми (наборный Gotham Pro
уже переведён в контуры), поэтому знак и логотипы вынимаются через
fitz.get_drawings() как настоящий вектор — коммерческий шрифт не нужен,
а цвета внутри SVG становятся классами c0/c1/c2 и красятся из CSS.

Пишет в mirror/images/metra/:
  logo-<brand>.svg     логотип целиком (знак + начертание)
  mark-<brand>.svg      только знак
  m-<name>.jpg          кропы носителей (правый квадрат разворота)
  sheet/<NN>.jpg        развороты гайдлайна для лайтбокса (1400px)
  sheet/th-<NN>.jpg     миниатюры сетки (420px)
  manifest.json         палитры, цвета логотипов, список кропов и разворотов

Запуск: python3 scripts/metra-assets.py [путь-к-pdf]
"""
import json
import os
import subprocess
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUT = os.path.join(ROOT, 'mirror', 'images', 'metra')
SHEET = os.path.join(OUT, 'sheet')
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Downloads/метра.pdf')

# ─── карта брендов ──────────────────────────────────────────────────────────
# logo  — (страница, прямоугольник логотипа «основная версия» на белом)
# pal   — (страница, y-полоса палитры) : плашки берём фактическими заливками
BRANDS = {
    'mtg':      dict(logo=(7,  (663, 139, 873, 184)), pal=(7,  396, 426), pattern=9),
    'metra':    dict(logo=(24, (663, 139, 817, 184)), pal=(24, 396, 426), pattern=26),
    'pro':      dict(logo=(37, (660, 139, 795, 184)), pal=(37, 396, 426), pattern=39),
    'robotics': dict(logo=(50, (663, 136, 910, 197)), pal=(50, 449, 479), pattern=52),
    'polis':    dict(logo=(61, (662, 139, 815, 189)), pal=(61, 447, 480), pattern=63),
}

# ─── кропы носителей: (имя, страница, прямоугольник) ────────────────────────
# По умолчанию берём правую часть разворота (в макете брендбука слева титул,
# справа носитель) и ужимаем её по фактическому пятну макета — см. trim().
R = (505, 0, 1190, 595)
CROPS = [
    ('mtg-docs',      10, R), ('mtg-cards',     11, R), ('mtg-city',      12, R),
    ('mtg-web',       13, (390, 0, 1190, 595)), ('mtg-photo', 14, (60, 300, 1160, 595)),
    ('mtg-transport', 15, (480, 60, 1190, 560)), ('mtg-gifts', 16, R),
    ('mtg-present',   17, R), ('mtg-cobrand',   18, R), ('mtg-social',    19, R),
    ('mtg-cloth',     20, (505, 20, 1190, 595)),
    ('metra-docs',    27, R), ('metra-cards',   28, R), ('metra-city',    29, R),
    ('metra-web',     30, (430, 0, 1190, 595)), ('metra-gifts', 31, R),
    ('metra-present', 33, R),
    ('pro-docs',      40, R), ('pro-cards',     41, R), ('pro-city',      42, R),
    ('pro-web',       43, (390, 0, 1190, 595)), ('pro-gifts', 44, R),
    ('pro-present',   46, R),
    ('robo-cards',    53, R), ('robo-city',     54, R),
    ('robo-web',      55, (430, 0, 1190, 595)),
    ('robo-gifts',    56, R), ('robo-present',  57, R), ('robo-docs',     58, R),
    ('polis-docs',    64, R), ('polis-city',    65, R),
    ('polis-web',     66, (450, 0, 1190, 595)),
    ('polis-cards',   67, R), ('polis-gifts',   68, R), ('polis-present', 69, R),
]


# ─── исходные фотографии для блока «фотостиль»: (имя, xref) ─────────────────
# Берём растр прямо из PDF, без затемнения и маски: правило гайдлайна
# (чёрный слой 70% и маска-сота) на странице накладывается вживую.
PHOTOS = [('cell', 125), ('earth', 126), ('line', 118)]


def hexc(c):
    return '#%02X%02X%02X' % tuple(int(round(v * 255)) for v in c)


# ─── сборка SVG из кривых PDF ───────────────────────────────────────────────
def path_d(items, dx, dy, closed=False):
    """Элементы пути fitz → атрибут d.

    Отрезки и кривые внутри одного контура идут встык, поэтому новый M пишем
    только когда очередной элемент начинается не там, где кончился прошлый:
    иначе каждая линия стала бы отдельным разомкнутым подконтуром и заливка
    буквы рассыпалась бы.
    """
    out, last = [], None

    def pt(p):
        return '%.2f %.2f' % (p.x - dx, p.y - dy)

    def near(a, b):
        return b is not None and abs(a.x - b.x) < .01 and abs(a.y - b.y) < .01

    for it in items:
        k = it[0]
        if k == 'l':
            a, b = it[1], it[2]
            if not near(a, last):
                if last is not None and closed:
                    out.append('Z')
                out.append('M' + pt(a))
            out.append('L' + pt(b))
            last = b
        elif k == 'c':
            a, b, c, e = it[1], it[2], it[3], it[4]
            if not near(a, last):
                if last is not None and closed:
                    out.append('Z')
                out.append('M' + pt(a))
            out.append('C%s %s %s' % (pt(b), pt(c), pt(e)))
            last = e
        elif k == 're':
            r = it[1]
            out.append('M%.2f %.2fH%.2fV%.2fH%.2fZ' % (
                r.x0 - dx, r.y0 - dy, r.x1 - dx, r.y1 - dy, r.x0 - dx))
            last = None
        elif k == 'qu':
            q = it[1]
            out.append('M' + 'L'.join(pt(p) for p in (q.ul, q.ur, q.lr, q.ll)) + 'Z')
            last = None
    if closed and last is not None:
        out.append('Z')
    return ''.join(out)


def svg_from(page, rect, pad=0.0):
    """Все кривые внутри rect → (svg-текст, список цветов в порядке появления)."""
    rc = fitz.Rect(*rect)
    picked = [d for d in page.get_drawings() if d['rect'].x0 >= rc.x0 - .5
              and d['rect'].y0 >= rc.y0 - .5 and d['rect'].x1 <= rc.x1 + .5
              and d['rect'].y1 <= rc.y1 + .5 and d['items']]
    if not picked:
        raise SystemExit('пусто в %s' % (rect,))
    x0 = min(d['rect'].x0 for d in picked) - pad
    y0 = min(d['rect'].y0 for d in picked) - pad
    x1 = max(d['rect'].x1 for d in picked) + pad
    y1 = max(d['rect'].y1 for d in picked) + pad

    colors, body = [], []
    for d in picked:
        col = d['fill'] or d['color']
        h = hexc(col) if col else '#000000'
        if h not in colors:
            colors.append(h)
        cls = 'c%d' % colors.index(h)
        dd = path_d(d['items'], x0, y0, closed=bool(d['fill']) or d.get('closePath'))
        if not dd:
            continue
        # Цвет пишем и атрибутом (чтобы файл был самодостаточным), и классом:
        # на странице CSS-правило .c0{fill:…} перебивает презентационный атрибут.
        if d['fill']:
            rule = 'evenodd' if d.get('even_odd') else 'nonzero'
            body.append('<path class="%s" fill="%s" fill-rule="%s" d="%s"/>' % (cls, h, rule, dd))
        else:
            w = d.get('width') or 1
            body.append('<path class="%s" fill="none" stroke="%s" stroke-width="%.2f" d="%s"/>'
                        % (cls, h, w, dd))

    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f">%s</svg>'
           % (x1 - x0, y1 - y0, ''.join(body)))
    return svg, colors, (x1 - x0, y1 - y0)


def mark_rect(page, rect):
    """Знак — самый левый кластер логотипа: обрезаем по первому широкому разрыву x."""
    rc = fitz.Rect(*rect)
    picked = [d['rect'] for d in page.get_drawings()
              if d['rect'].x0 >= rc.x0 - .5 and d['rect'].y0 >= rc.y0 - .5
              and d['rect'].x1 <= rc.x1 + .5 and d['rect'].y1 <= rc.y1 + .5]
    xs = sorted(picked, key=lambda r: r.x0)
    edge = xs[0].x1
    for r in xs[1:]:
        if r.x0 - edge > 4:          # разрыв между знаком и начертанием
            break
        edge = max(edge, r.x1)
    inside = [r for r in picked if r.x1 <= edge + .5]
    return (min(r.x0 for r in inside) - .5, min(r.y0 for r in inside) - .5,
            edge + .5, max(r.y1 for r in inside) + .5)


def palette(page, y0, y1):
    """Плашки палитры: фактическая заливка + подписи CMYK под ней."""
    sw = [d for d in page.get_drawings()
          if d['fill'] and d['rect'].width > 28 and d['rect'].height > 18
          and y0 <= d['rect'].y0 <= y1]
    sw.sort(key=lambda d: d['rect'].x0)
    words = page.get_text('words')            # (x0,y0,x1,y1,word,...)
    out = []
    for d in sw:
        r = d['rect']
        col = [w[4] for w in words if r.x0 - 8 < w[0] < r.x1 + 14 and r.y1 < w[1] < r.y1 + 80
               and w[4].isdigit()]
        out.append(dict(hex=hexc(d['fill']), cmyk=col[:4], x=round(r.x0)))
    return out


def trim(page, rect, tol=236, pad=6):
    """Ужимает область поиска до реального пятна макета: белые поля брендбука
    в кроп попадать не должны (см. правило про мокапы без пустых полос)."""
    rc = fitz.Rect(*rect)
    pix = page.get_pixmap(dpi=36, clip=rc)
    w, h, n = pix.width, pix.height, pix.n
    s = pix.samples
    cols, rows = [], []
    for y in range(h):
        row = False
        for x in range(w):
            i = (y * w + x) * n
            if s[i] < tol or s[i + 1] < tol or s[i + 2] < tol:
                row = True
                if x not in cols:
                    cols.append(x)
        if row:
            rows.append(y)
    if not rows:
        return rc
    k = 2                                        # 36 dpi → пункты
    return fitz.Rect(max(rc.x0 + min(cols) * k - pad, rc.x0),
                     max(rc.y0 + min(rows) * k - pad, rc.y0),
                     min(rc.x0 + (max(cols) + 1) * k + pad, rc.x1),
                     min(rc.y0 + (max(rows) + 1) * k + pad, rc.y1))


def render(page, rect, path, dpi=170, quality=82):
    pix = page.get_pixmap(dpi=dpi, clip=trim(page, rect))
    pix.pil_save(path, format='JPEG', quality=quality, optimize=True)


def main():
    os.makedirs(SHEET, exist_ok=True)
    doc = fitz.open(SRC)
    man = dict(brands={}, crops=[], sheet=[])

    for key, cfg in BRANDS.items():
        pg, rect = cfg['logo']
        page = doc[pg - 1]
        svg, colors, size = svg_from(page, rect)
        open(os.path.join(OUT, 'logo-%s.svg' % key), 'w', encoding='utf-8').write(svg)
        mr = mark_rect(page, rect)
        msvg, mcolors, msize = svg_from(page, mr)
        open(os.path.join(OUT, 'mark-%s.svg' % key), 'w', encoding='utf-8').write(msvg)
        # начертание отдельно: нужно на плитках «недопустимо», где знак и название
        # разъезжаются друг от друга
        wsvg, _, _ = svg_from(page, (mr[2], rect[1], rect[2], rect[3]))
        open(os.path.join(OUT, 'word-%s.svg' % key), 'w', encoding='utf-8').write(wsvg)
        ppg, py0, py1 = cfg['pal']
        man['brands'][key] = dict(
            logo=dict(colors=colors, w=round(size[0], 2), h=round(size[1], 2)),
            mark=dict(colors=mcolors, w=round(msize[0], 2), h=round(msize[1], 2)),
            palette=palette(doc[ppg - 1], py0, py1))
        print('logo %-9s %2d кривых-цветов %s  знак %s' % (key, len(colors), colors, mcolors))

    for name, xref in PHOTOS:
        img = doc.extract_image(xref)
        open(os.path.join(OUT, 'photo-%s.jpg' % name), 'wb').write(img['image'])
        man.setdefault('photos', []).append(dict(name=name, w=img['width'], h=img['height']))
    print('фотографий: %d' % len(PHOTOS))

    for name, pg, rect in CROPS:
        f = 'm-%s.jpg' % name
        render(doc[pg - 1], rect, os.path.join(OUT, f))
        man['crops'].append(dict(name=name, file=f, page=pg))
    print('кропов носителей: %d' % len(CROPS))

    for i, page in enumerate(doc, 1):
        big = os.path.join(SHEET, '%02d.jpg' % i)
        page.get_pixmap(dpi=86).pil_save(big, format='JPEG', quality=74, optimize=True)
        page.get_pixmap(dpi=26).pil_save(os.path.join(SHEET, 'th-%02d.jpg' % i),
                                         format='JPEG', quality=76, optimize=True)
        man['sheet'].append('%02d.jpg' % i)
    print('разворотов: %d' % len(doc))

    json.dump(man, open(os.path.join(OUT, 'manifest.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    webp = os.path.join(HERE, 'gen-webp.sh')
    if os.path.exists(webp):
        subprocess.run(['bash', webp, OUT], check=False)


if __name__ == '__main__':
    main()
