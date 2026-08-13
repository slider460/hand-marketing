#!/usr/bin/env python3
"""Обложки карточки кейса «Фирменный стиль выставки „Самара“» (477×396),
механика дизайн-системы v2.2:
- cover-main: КРУГ-постер в фирменном синем 368AB5, внутри — кривая паруса
  светлым тоном (тот самый фоновый паттерн из гайда), маскот «Ладушка» строго
  по центру и плашка «БРЕНДБУК / ВЫСТАВКА „САМАРА“»: в каталоге карточка идёт
  без подписи, поэтому кейс объясняет сам постер, а не знак региона;
- cover-hover: КВАДРАТ того же синего — фоновое эхо «46» (слов семантического
  ядра), знак-парус, заголовок и «СМОТРЕТЬ КЕЙС →».
Знак и парус не рисуем руками: берём кривые из scripts/a2/samara_vectors.json,
то есть тот же вектор, что и на самой странице кейса.
Кладёт в mirror/images/lib/custom-samara-brand/ (webp — scripts/gen-webp.sh)."""
import json
import math
import os

import fitz
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
SS = 4  # суперсэмплинг

VEC = json.load(open(os.path.join(HERE, 'a2', 'samara_vectors.json'), encoding='utf-8'))
MASCOT = os.path.join(ROOT, 'mirror', 'images', 'samara-brand', 'hero.png')
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-samara-brand')
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

BLUE = (54, 138, 181)      # 368AB5 — основной синий палитры
DEEP = (4, 96, 129)        # 046081 — им уходим в глубину
INK = (45, 48, 81)         # 2D3051
SAND = (244, 227, 219)     # F4E3DB
WHITE = (255, 255, 255)


def font(sz, v='Bold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def vector(key, width_px, color='#FFFFFF', stroke_w=None):
    """Фигура из брендбука в прозрачный PNG нужной ширины."""
    fig = VEC[key]
    body = []
    for p in fig['paths']:
        if p['fill']:
            rule = ' fill-rule="evenodd"' if p['even_odd'] else ''
            body.append(f'<path d="{p["d"]}" fill="{color}"{rule}/>')
        else:
            body.append(f'<path d="{p["d"]}" fill="none" stroke="{color}" '
                        f'stroke-width="{stroke_w or p["w"] or 2}" '
                        f'stroke-linecap="round" stroke-linejoin="round"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fig["viewBox"]}">'
           f'{"".join(body)}</svg>')
    tmp = os.path.join(OUT, '_vec.svg')
    open(tmp, 'w', encoding='utf-8').write(svg)
    doc = fitz.open(tmp)
    page = doc[0]
    zoom = width_px / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=True)
    img = Image.frombytes('RGBA', (pix.width, pix.height), pix.samples)
    doc.close()
    os.remove(tmp)
    return img


def disc():
    """Круг: синяя заливка с уходом в глубину и кривая паруса поверх."""
    S = SS
    d2 = 2 * R * S
    im = Image.new('RGBA', (d2, d2), BLUE + (255,))
    px = im.load()
    for y in range(d2):
        k = y / d2
        row = tuple(round(BLUE[i] + (DEEP[i] - BLUE[i]) * k * 0.85) for i in range(3))
        for x in range(d2):
            px[x, y] = row + (255,)
    sail = vector('sail', int(d2 * 1.15), color='#8FC4DC', stroke_w=7)
    im.alpha_composite(sail, (int(-d2 * 0.06), int(-d2 * 0.10)))
    return im


MAIN_PLATE = ('БРЕНДБУК', 'ВЫСТАВКА «САМАРА»')
PLATE_TOP = 300      # верх плашки в координатах карточки
FIG_H, FIG_BOTTOM = 252, 298   # рост фигуры и уровень, на котором она стоит


def cover_main():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    cx, cy, r = CX * S, CY * S, R * S
    layer = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    layer.paste(disc(), (cx - r, cy - r))
    mask = Image.new('L', (W * S, H * S), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(layer, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE + (52,), width=2 * S)

    # маскот строго по центру круга: карточка в каталоге идёт без подписи,
    # поэтому объяснять кейс должен сам постер
    m = Image.open(MASCOT).convert('RGBA')
    mh = int(FIG_H * S)
    m = m.resize((max(1, round(m.width * mh / m.height)), mh), Image.LANCZOS)
    img.alpha_composite(m, (cx - m.width // 2, int(FIG_BOTTOM * S) - mh))

    # плашка вместо знака: знак региона узнаётся не всеми, а «что это за кейс»
    # с карточки должно читаться сразу. Знак остаётся на hover-квадрате.
    rows = []
    for text, size, color in ((MAIN_PLATE[0], 16, SAND), (MAIN_PLATE[1], 12, (168, 196, 214))):
        f = font(int(size * S), 'ExtraBold')
        tb = d.textbbox((0, 0), text, font=f)
        rows.append((text, f, tb, tb[2] - tb[0], tb[3] - tb[1], color))
    padx, pady, gap = int(20 * S), int(12 * S), int(7 * S)
    pw = max(x[3] for x in rows) + padx * 2
    ph = sum(x[4] for x in rows) + gap + pady * 2
    plx, ply = cx - pw // 2, int(PLATE_TOP * S)
    # плашка обязана вписаться в хорду круга на своей высоте, иначе углы вылезут
    half = math.sqrt(max(0.0, (R * S) ** 2 - ((ply + ph / 2) - cy) ** 2))
    if pw / 2 > half - 12 * S:
        raise SystemExit('✗ плашка шире круга на этой высоте: %.0f px против %.0f px'
                         % (pw / S, 2 * (half - 12 * S) / S))
    d.rounded_rectangle([plx, ply, plx + pw, ply + ph], radius=int(16 * S), fill=INK + (255,))
    y = ply + pady
    for _t, f, tb, tw, th, color in rows:
        d.text((cx - tw // 2 - tb[0], y - tb[1]), _t, font=f, fill=color + (255,))
        y += th + gap
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), BLUE + (255,))
    d = ImageDraw.Draw(img)
    # фоновое эхо: 46 слов семантического ядра
    ef = font(int(340 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), '46', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(18 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(2 * S) - eb[1]), '46', font=ef, fill=DEEP + (255,))
    lg = vector('mark', int(58 * S))
    img.paste(lg, (int(34 * S), int(30 * S)), lg)
    hf = font(int(36 * S), 'ExtraBold')
    for i, ln in enumerate(['Фирменный стиль', 'выставки «Самара»']):
        d.text((int(34 * S), int((156 + i * 44) * S)), ln, font=hf, fill=WHITE + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(268 * S)), 'брендбук региона, 28 полос',
           font=sf, fill=WHITE + (190,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(336 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=WHITE + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
