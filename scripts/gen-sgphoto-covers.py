#!/usr/bin/env python3
"""Обложки карточки кейса «Предметная съёмка продукции Gyproc» (477×396),
механика дизайн-системы v2.2:
- cover-main: КРУГ-постер — соединитель «краб» со съёмки лежит на фирменном
  синем; фон у исходника вырезан по контуру, поэтому деталь садится на круг
  без подложки и выходит за его край, как и положено 3D-блокам системы.
  Белый вордмарк SAINT-GOBAIN и пилюля-метрика «62 КАДРА».
- cover-hover: синий КВАДРАТ того же цвета — фоновое эхо «1:1», вордмарк,
  заголовок «Съёмка продукции» и «СМОТРЕТЬ КЕЙС →».
Кладёт в mirror/images/lib/custom-sgphoto/ (+ webp через scripts/gen-webp.sh).

Синий взят не из палитры вообще, а с самой продукции: этикетка ленты Гипрок
Марко ПРО (#3B729D), поднятая по насыщенности до каталожной читаемости."""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-sgphoto')
ITEM = os.path.join(ROOT, 'mirror', 'images', 'sgphoto', 'item-2105.webp')
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

BLUE = (31, 111, 184)
BLUE_D = (18, 71, 122)
ACCENT = (238, 15, 63)
WHITE = (255, 255, 255)
SS = 4


def font(sz, v='Bold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def wordmark(d, x, y, h_px, color):
    """SAINT-GOBAIN разрядкой: цветной логотип клиента на синем не читается."""
    f = font(h_px, 'ExtraBold')
    for ch in 'SAINT-GOBAIN':
        d.text((x, y), ch, font=f, fill=color)
        x += d.textbbox((0, 0), ch, font=f)[2] + h_px * 0.13


def cover_main():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    cx, cy, r = CX * S, CY * S, R * S
    d = ImageDraw.Draw(img)
    # круг: ровная фирменная заливка с лёгким градиентом к низу
    disc = Image.new('RGBA', (2 * r, 2 * r), BLUE + (255,))
    dp = disc.load()
    for y in range(2 * r):
        k = y / (2 * r)
        col = tuple(round(BLUE[i] + (BLUE_D[i] - BLUE[i]) * k * k) for i in range(3))
        for x in range(2 * r):
            dp[x, y] = col + (255,)
    mask = Image.new('L', (W * S, H * S), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    tmp = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    tmp.paste(disc, (cx - r, cy - r))
    img.paste(tmp, (0, 0), mask)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE + (46,), width=2 * S)

    # деталь поверх круга: вырезанный по контуру краб, выходит за границу круга
    item = Image.open(ITEM).convert('RGBA')
    tw = int(r * 2.02)
    item = item.resize((tw, round(item.height * tw / item.width)), Image.LANCZOS)
    # выше центра: под деталью должно остаться чистое синее поле под вордмарк
    img.alpha_composite(item, (cx - item.width // 2, cy - item.height // 2 - int(46 * S)))

    # вордмарк и метрика — в нижней половине: сверху карточку режет чип категории
    wordmark(d, cx - int(104 * S), cy + int(58 * S), int(22 * S), WHITE + (255,))
    ptxt = '62 КАДРА'
    pf = font(int(19 * S), 'ExtraBold')
    tb = d.textbbox((0, 0), ptxt, font=pf)
    tw_, th_ = tb[2] - tb[0], tb[3] - tb[1]
    px, py = int(24 * S), int(14 * S)
    pw, ph = tw_ + px * 2, th_ + py * 2
    plx, ply = cx - pw // 2, cy + r - int(74 * S)
    d.rounded_rectangle([plx, ply, plx + pw, ply + ph], radius=ph // 2, fill=ACCENT + (255,))
    d.text((plx + px - tb[0], ply + py - tb[1]), ptxt, font=pf, fill=WHITE)
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), BLUE + (255,))
    d = ImageDraw.Draw(img)
    ef = font(int(200 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), '1:1', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(16 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(6 * S) - eb[1]), '1:1', font=ef, fill=BLUE_D + (255,))
    wordmark(d, int(34 * S), int(30 * S), int(19 * S), WHITE + (255,))
    hf = font(int(44 * S), 'ExtraBold')
    for i, ln in enumerate(['Съёмка', 'продукции']):
        d.text((int(34 * S), int((160 + i * 52) * S)), ln, font=hf, fill=WHITE + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(276 * S)), 'предметная, 2023', font=sf, fill=WHITE + (200,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(338 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=WHITE + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
