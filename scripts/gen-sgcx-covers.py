#!/usr/bin/env python3
"""Обложки карточки кейса «Клиентский опыт» Saint-Gobain для каталога (477×396),
механика дизайн-системы v2.2:
- cover-main: КРУГ-постер — мозаика из портретов переклички (те самые 48 лиц,
  вынутые из фильма) под фирменным синим тинтом, белый вордмарк SAINT-GOBAIN
  и чёрная пилюля-метрика «48 ИМЁН В КАДРЕ»;
- cover-hover: синий КВАДРАТ того же цвета — фоновое эхо «48», вордмарк,
  заголовок «Клиентский опыт» и «СМОТРЕТЬ КЕЙС →».
Кладёт в mirror/images/lib/custom-sgcx/ (webp — через scripts/gen-webp.sh)."""
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-sgcx')
FACES = os.path.join(ROOT, 'mirror', 'images', 'sgcx')
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

BLUE = (24, 31, 113)        # #181F71, тёмно-синий знака Saint-Gobain
BLUE_D = (10, 14, 58)
CX_BLUE = (41, 150, 197)    # #2996C5, голубой знака Customer eXperience
INK = (16, 24, 40)
WHITE = (255, 255, 255)
SS = 4


def font(sz, v='Bold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def wordmark(d, x, y, h_px, color, text='SAINT-GOBAIN'):
    """Имя клиента разрядкой: фирменный знак на карточку не ставим,
    ставим набор капсом, как во всех обложках каталога."""
    f = font(h_px, 'ExtraBold')
    for ch in text:
        d.text((x, y), ch, font=f, fill=color)
        x += d.textbbox((0, 0), ch, font=f)[2] + h_px * 0.16


def mosaic(side):
    """Сетка 7×7 из портретов переклички под синим тинтом.

    Мозаика не выдумана: ровно так собран знак компании на 78-й секунде
    фильма, кадр из портретов сотрудников."""
    files = sorted(f for f in os.listdir(FACES)
                   if f.startswith('p') and f.endswith('@280.jpg'))
    random.Random(48).shuffle(files)
    n = 7
    cell = side // n
    im = Image.new('RGB', (cell * n, cell * n), BLUE_D)
    for i in range(n * n):
        src = Image.open(os.path.join(FACES, files[i % len(files)])).convert('RGB')
        s = min(src.size)
        src = src.crop(((src.width - s) // 2, 0, (src.width + s) // 2, s))
        im.paste(src.resize((cell, cell), Image.LANCZOS), (cell * (i % n), cell * (i // n)))
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            k = (r * 0.30 + g * 0.59 + b * 0.11) / 255
            px[x, y] = tuple(round(BLUE_D[i] + (BLUE[i] - BLUE_D[i]) * k
                                   + (255 - BLUE[i]) * k * k * 0.62) for i in range(3))
    return im.resize((side, side), Image.LANCZOS)


def cover_main():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    cx, cy, r = CX * S, CY * S, R * S
    disc = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    disc.paste(mosaic(2 * r), (cx - r, cy - r))
    mask = Image.new('L', (W * S, H * S), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(disc, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE + (52,), width=2 * S)
    # вордмарк и метрика в нижней половине круга: сверху карточку перекрывает
    # чип категории, и всё, что там стоит, режется
    wordmark(d, cx - int(104 * S), cy + int(56 * S), int(19 * S), WHITE + (255,))
    ptxt = '48 ИМЁН В КАДРЕ'
    pf = font(int(18 * S), 'ExtraBold')
    tb = d.textbbox((0, 0), ptxt, font=pf)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = int(24 * S), int(14 * S)
    pw, ph = tw + px * 2, th + py * 2
    plx, ply = cx - pw // 2, cy + r - int(74 * S)
    d.rounded_rectangle([plx, ply, plx + pw, ply + ph], radius=ph // 2, fill=INK + (255,))
    d.text((plx + px - tb[0], ply + py - tb[1]), ptxt, font=pf, fill=CX_BLUE + (255,))
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), BLUE + (255,))
    d = ImageDraw.Draw(img)
    ef = font(int(340 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), '48', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(20 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(2 * S) - eb[1]), '48', font=ef, fill=BLUE_D + (255,))
    wordmark(d, int(34 * S), int(30 * S), int(16 * S), WHITE + (235,))
    hf = font(int(44 * S), 'ExtraBold')
    for i, ln in enumerate(['Клиентский', 'опыт']):
        d.text((int(34 * S), int((150 + i * 52) * S)), ln, font=hf, fill=WHITE + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(274 * S)), 'корпоративный фильм, 10 минут',
           font=sf, fill=WHITE + (185,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(336 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=CX_BLUE + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
