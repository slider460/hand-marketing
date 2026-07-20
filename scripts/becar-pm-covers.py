#!/usr/bin/env python3
"""Обложки карточки кейса Becar × Private Money для Tilda-каталога (477x396).
Как у остальных карточек каталога — КРУГ на прозрачном фоне, но в стиле You&Co
(«бумажный коллаж» вместо кубиков ВДНХ):
- cover-main: круг с фото построенного стенда, жёлтое кольцо, вырезные формы
  по углам, стикеры «BECAR × PRIVATE MONEY» / «выставка под ключ».
- cover-hover: круг с финальным 3D-рендером, фиолетовое кольцо, инверсия форм,
  стикеры «СМОТРЕТЬ КЕЙС →» / «от 3D-проекта до стенда».
Кладёт в mirror/images/lib/custom-becar-pm/ (+webp через scripts/gen-webp.sh)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 477, 396
CX, CY, R = 238, 190, 176          # круг как у остальных обложек каталога
OUT = 'mirror/images/lib/custom-becar-pm'
_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'Montserrat.ttf')

PURPLE = (59, 37, 100)
PURPLE_L = (122, 79, 168)
RED = (232, 64, 74)
YELLOW = (245, 167, 49)
GOLD = (255, 211, 122)
INK = (20, 23, 28)


def font(sz, w='ExtraBold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(w)
    except Exception:
        pass
    return f


def poly(base, pts, color):
    ImageDraw.Draw(base).polygon(pts, fill=color)


def star(base, cx, cy, r, color, rot=0.0):
    import math
    pts = []
    for i in range(10):
        a = math.pi * i / 5 - math.pi / 2 + rot
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    ImageDraw.Draw(base).polygon(pts, fill=color)


def circle_photo(base, photo, focus=0.5, ring=None):
    im = Image.open(photo).convert('RGB')
    w, h = im.size
    side = min(w, h)
    left = int((w - side) * focus)
    top = (h - side) // 2
    ph = im.crop((left, top, left + side, top + side)).resize((2 * R, 2 * R), Image.LANCZOS)
    m = Image.new('L', (2 * R, 2 * R), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 2 * R, 2 * R], fill=255)
    base.paste(ph, (CX - R, CY - R), m)
    if ring:
        ImageDraw.Draw(base).ellipse([CX - R, CY - R, CX + R, CY + R], outline=ring, width=6)


def sticker(base, lines, bg, fg, cx, cy, angle, sz=26, pad=(18, 10)):
    f = font(sz)
    tmp = Image.new('RGBA', (W * 2, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    tw = max(d.textlength(t, font=f) for t in lines)
    lh = int(sz * 1.22)
    bw, bh = int(tw + 2 * pad[0]), lh * len(lines) + 2 * pad[1]
    st = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
    ds = ImageDraw.Draw(st)
    ds.rounded_rectangle([0, 0, bw - 1, bh - 1], 10, fill=bg)
    y = pad[1]
    for t in lines:
        ds.text(((bw - ds.textlength(t, font=f)) / 2, y), t, font=f, fill=fg)
        y += lh
    st = st.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(st, (int(cx - st.width / 2), int(cy - st.height / 2)))


def main_cover():
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # без боковых декоров: You&Co-формы не наша айдентика (правка пользователя 20.07)
    # круг: построенный стенд (реальное фото)
    circle_photo(base, 'mirror/images/becar-pm/photo-stand-full.jpg', focus=0.52, ring=YELLOW)
    # стикеры поверх нижней части круга
    sticker(base, ['BECAR × PRIVATE MONEY'], YELLOW, INK, CX, 330, -3, sz=25)
    sticker(base, ['выставка под ключ'], RED, (255, 255, 255), CX + 10, 368, 2, sz=17, pad=(14, 7))
    os.makedirs(OUT, exist_ok=True)
    base.save(os.path.join(OUT, 'cover-main.png'))
    print('saved cover-main.png')


def hover_cover():
    # при наведении — ПРЯМОУГОЛЬНАЯ карточка (как в механике сайта: круг → квадрат),
    # жёлтое поле с вырезными формами и кругом 3D-рендера
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([0, 0, W - 1, H - 1], 26, fill=YELLOW)
    poly(base, [(0, 30), (72, 0), (96, 84), (12, 116)], PURPLE)
    poly(base, [(W - 100, H - 4), (W - 6, H - 96), (W - 4, H - 4)], RED)
    poly(base, [(W - 74, 0), (W - 4, 22), (W - 34, 66), (W - 92, 40)], (255, 224, 160))
    star(base, 50, H - 64, 26, PURPLE, rot=0.5)
    # круг с рендером — чуть меньше, внутри карточки
    im = Image.open('mirror/images/becar-pm/render-front.jpg').convert('RGB')
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    r = 138
    ph = im.crop((left, top, left + side, top + side)).resize((2 * r, 2 * r), Image.LANCZOS)
    m = Image.new('L', (2 * r, 2 * r), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 2 * r, 2 * r], fill=255)
    base.paste(ph, (250 - r, 176 - r), m)
    ImageDraw.Draw(base).ellipse([250 - r, 176 - r, 250 + r, 176 + r], outline=PURPLE, width=5)
    sticker(base, ['СМОТРЕТЬ КЕЙС →'], PURPLE, (255, 255, 255), 238, 330, 3, sz=25)
    sticker(base, ['от 3D-проекта до стенда'], INK, GOLD, 250, 366, -2, sz=16, pad=(14, 7))
    # маска скругления карточки
    mm = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mm).rounded_rectangle([0, 0, W - 1, H - 1], 26, fill=255)
    base.putalpha(mm)
    base.save(os.path.join(OUT, 'cover-hover.png'))
    print('saved cover-hover.png')


if __name__ == '__main__':
    main_cover()
    hover_cover()
