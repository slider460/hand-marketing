#!/usr/bin/env python3
"""Ассеты кейса «Фирменный стиль отдела продаж Becar» (SALESDEP).

Источник: гайдлайн ~/Downloads/CS_SalesDep_FIN.pdf, 29 полос 1920×1080.

Что делает:
  1. вынимает знак кривыми (он набран Grifter Bold, шрифта у нас нет) и собирает
     из тех же кривых тайл фирменного паттерна — на странице они живые SVG;
  2. рендерит полосы-носители в JPEG (галерея с лайтбоксом на странице кейса);
  3. режет из полос-визуализаций крупные планы без белых полей и подписей —
     они идут в блоки «носители» как самостоятельные картинки.

Итог: mirror/images/sdep/. После прогона — scripts/gen-webp.sh mirror/images/sdep
Идемпотентно, просто перезаписывает.
"""
import io
import os

import fitz
from PIL import Image

SRC = os.path.expanduser('~/Downloads/CS_SalesDep_FIN.pdf')
DST = 'mirror/images/sdep'

os.makedirs(DST, exist_ok=True)

# ─── полосы гайдлайна в галерею: (номер полосы, имя файла) ───────────────────
SLIDES = [
    (2,  'logo'),        (3,  'colors'),      (4,  'type'),        (5,  'pattern'),
    (7,  'infographic'), (8,  'deck-cover'),  (9,  'deck-body'),
    (11, 'social-rules'),(12, 'social-avatar'),(13, 'instagram'),  (14, 'facebook'),
    (15, 'stickers'),    (16, 'stickers-tg'),
    (18, 'office-1'),    (19, 'office-2'),
    (20, 'docs'),        (21, 'business'),    (22, 'business-3d'),
    (23, 'expo'),        (24, 'expo-3d'),
    (25, 'fc'),          (26, 'fc-3d'),
    (27, 'gifts'),       (28, 'gifts-3d'),
]

# ─── крупные планы: (полоса, (x0,y0,x1,y1) в координатах 1920×1080, имя) ─────
CROPS = [
    (22, (600,   0, 1920, 1080), 'shot-business'),   # папка, бейджи, визитка на синем
    (24, (628,   0, 1920, 1080), 'shot-expo'),       # пресс-волл, ролл-ап, стенд
    (26, (600,   0, 1920, 1080), 'shot-fc'),         # флаг, футболка, мяч
    (28, (540,  40, 1920, 1040), 'shot-gifts'),      # стакан, блокнот, зонт, кружка
    (16, (640,   0, 1920, 1080), 'shot-stickers'),   # телеграм-пак на бирюзовом
    (12, (700,  90, 1920, 1010), 'shot-social'),     # монитор и телефон с оформлением
    (19, (590,   0, 1920, 1080), 'shot-office'),     # кухня и переговорная
]


# ─── логотип ────────────────────────────────────────────────────────────────
# Знак набран Grifter Bold и в PDF лежит кривыми: 8 глифов на полосе 2,
# пять бирюзовых (SALES) и три розовых (DEP). Собираем из них SVG, где цвет
# каждого блока задаётся через CSS (по гайдлайну знак можно красить в любой
# фирменный цвет, лишь бы SALES и DEP были каждый одного цвета).
CYAN = (0.0, 0.7879911661148071, 0.850995659828186)
SDEP_SHIFT = 373.8   # на столько сдвигаем DEP влево для сокращённой версии


def glyphs():
    """Восемь глифов основной версии знака с полосы 2 (белую подпись отсекаем)."""
    out = [dr for dr in fitz.open(SRC)[1].get_drawings()
           if dr['rect'].x1 < 1000 and 250 < dr['rect'].y0 and dr['rect'].y1 < 520
           and dr.get('fill') != (1.0, 1.0, 1.0)]
    return sorted(out, key=lambda d: d['rect'].x0)


def path_d(dr, dx=0.0):
    """Кривые PyMuPDF → атрибут d для SVG."""
    def pt(p):
        return f'{p.x - dx:.2f} {p.y:.2f}'
    d, cur = [], None
    for it in dr['items']:
        if it[0] == 'l':
            if cur != it[1]:
                d.append('M' + pt(it[1]))
            d.append('L' + pt(it[2]))
            cur = it[2]
        elif it[0] == 'c':
            if cur != it[1]:
                d.append('M' + pt(it[1]))
            d.append('C' + pt(it[2]) + ' ' + pt(it[3]) + ' ' + pt(it[4]))
            cur = it[4]
        elif it[0] == 're':
            r = it[1]
            d.append(f'M{r.x0 - dx:.2f} {r.y0:.2f}H{r.x1 - dx:.2f}V{r.y1:.2f}H{r.x0 - dx:.2f}Z')
            cur = None
    return ' '.join(d) + 'Z'


def logo_svg(name, parts, shift_dep=0.0):
    """parts: список (глиф, класс). Класс a — блок SALES/S, b — блок DEP."""
    xs, ys = [], []
    body = []
    for dr, cls in parts:
        dx = shift_dep if cls == 'b' else 0.0
        r = dr['rect']
        xs += [r.x0 - dx, r.x1 - dx]
        ys += [r.y0, r.y1]
        body.append(f'<path class="{cls}" d="{path_d(dr, dx)}"/>')
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} '
           f'{x1 - x0:.2f} {y1 - y0:.2f}" role="img" aria-label="Логотип SALESDEP">'
           '<style>.a{fill:var(--sd-a,#00CADA)}.b{fill:var(--sd-b,#FF1071)}</style>'
           + ''.join(body) + '</svg>')
    p = os.path.join(DST, name + '.svg')
    open(p, 'w', encoding='utf-8').write(svg)
    print('  ', name, f'{os.path.getsize(p) // 1024} КБ')


def logos():
    g = glyphs()
    full = [(dr, 'a' if dr.get('fill') == CYAN else 'b') for dr in g]
    logo_svg('logo', full)
    # сокращённая версия: S из SALES и блок DEP, придвинутый вплотную
    short = [full[0]] + [p for p in full if p[1] == 'b']
    logo_svg('logo-sdep', short, shift_dep=SDEP_SHIFT)


def patterns():
    """Фирменный паттерн — то же слово, положенное встык.

    Тайл отдаётся белым по прозрачному: на странице он работает маской, а цвет
    (градиент, плашку) даёт слой под ней. Так один файл закрывает и розовую
    стену, и контурную сетку на белом.
    """
    g = glyphs()
    x0, y0 = g[0]['rect'].x0, min(d['rect'].y0 for d in g)
    y1 = max(d['rect'].y1 for d in g)
    w = max(d['rect'].x1 for d in g) - x0 + 6.9   # межбуквенный просвет = как внутри слова
    h = (y1 - y0) * 1.16                          # интерлиньяж как в гайдлайне
    for name, attrs in (('pattern-solid', 'fill="#fff"'),
                        ('pattern-line', 'fill="none" stroke="#fff" stroke-width="3"')):
        body = ''.join(f'<path d="{path_d(d, x0)}"/>' for d in g)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {y0:.2f} {w:.2f} {h:.2f}" '
               f'width="{w:.0f}" height="{h:.0f}"><g {attrs}>{body}</g></svg>')
        p = os.path.join(DST, name + '.svg')
        open(p, 'w', encoding='utf-8').write(svg)
        print('  ', name, f'{w:.0f}×{h:.0f}', f'{os.path.getsize(p) // 1024} КБ')


def render(page_no, scale=1.0):
    """Полоса PDF в PIL.Image (1920×1080 × scale)."""
    page = fitz.open(SRC)[page_no - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')


def save(im, name, maxw, q=84):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name + '.jpg')
    im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    print('  ', name, im.size, f'{os.path.getsize(p) // 1024} КБ')


if __name__ == '__main__':
    print('логотип и паттерн:')
    logos()
    patterns()
    print('полосы:')
    for no, name in SLIDES:
        page = render(no, 1.4)
        save(page, 'slide-' + name, 1500)
        save(page, 'thumb-' + name, 300, q=78)
    print('крупные планы:')
    for no, box, name in CROPS:
        page = render(no, 2.0)
        k = page.width / 1920
        save(page.crop(tuple(round(v * k) for v in box)), name, 1700, q=86)
    print('готово →', DST)
