#!/usr/bin/env python3
"""Обложки карточки кейса «Обучающие видео для руководителей» Saint-Gobain
(477×396), механика дизайн-системы v2.2:
- cover-main: КРУГ-постер — общий план переговорной из курса под бирюзовым
  тинтом (бирюза это рабочий цвет экранов курса), белый вордмарк SAINT-GOBAIN
  и чёрная пилюля-метрика «9 СЦЕН, 28 ЭКРАНОВ»;
- cover-hover: бирюзовый КВАДРАТ того же цвета — фоновое эхо «STAR», вордмарк,
  заголовок «Обучающие видео» и «СМОТРЕТЬ КЕЙС →».
Кладёт в mirror/images/lib/custom-sgtraining/ (webp — через scripts/gen-webp.sh)."""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-sgtraining')
FRAMES = os.path.join(ROOT, 'mirror', 'images', 'sgtraining')
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

TEAL = (31, 110, 106)       # тинт круга и заливка квадрата
TEAL_D = (12, 54, 52)
CORAL = (244, 108, 84)      # #F46C54, третья полоса фирменного перехода
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
    """Имя клиента разрядкой: фирменный знак на карточку не ставим."""
    f = font(h_px, 'ExtraBold')
    for ch in text:
        d.text((x, y), ch, font=f, fill=color)
        x += d.textbbox((0, 0), ch, font=f)[2] + h_px * 0.16


def tinted(side):
    """Кадр переговорной под бирюзовым тинтом: тот самый интерьер, в котором
    сняты все девять сцен курса."""
    # крупный план из сцены: на общем плане в кадре стоит знак Saint-Gobain
    # на стене, и он спорит с вордмарком самой карточки
    src = Image.open(os.path.join(FRAMES, 'd1-b.jpg')).convert('RGB')
    s = src.height
    left = int((src.width - s) * 0.56)
    src = src.crop((left, 0, left + s, s))
    im = src.resize((side, side), Image.LANCZOS)
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            k = (r * 0.30 + g * 0.59 + b * 0.11) / 255
            px[x, y] = tuple(round(TEAL_D[i] + (TEAL[i] - TEAL_D[i]) * k
                                   + (255 - TEAL[i]) * k * k * 0.66) for i in range(3))
    return im


def cover_main():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    cx, cy, r = CX * S, CY * S, R * S
    disc = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    disc.paste(tinted(2 * r), (cx - r, cy - r))
    mask = Image.new('L', (W * S, H * S), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(disc, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE + (52,), width=2 * S)
    # вордмарк и метрика в нижней половине круга: сверху карточку перекрывает чип
    wordmark(d, cx - int(104 * S), cy + int(56 * S), int(19 * S), WHITE + (255,))
    ptxt = '9 СЦЕН, 28 ЭКРАНОВ'
    pf = font(int(17 * S), 'ExtraBold')
    tb = d.textbbox((0, 0), ptxt, font=pf)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = int(22 * S), int(14 * S)
    pw, ph = tw + px * 2, th + py * 2
    plx, ply = cx - pw // 2, cy + r - int(74 * S)
    d.rounded_rectangle([plx, ply, plx + pw, ply + ph], radius=ph // 2, fill=INK + (255,))
    d.text((plx + px - tb[0], ply + py - tb[1]), ptxt, font=pf, fill=CORAL + (255,))
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), TEAL + (255,))
    d = ImageDraw.Draw(img)
    ef = font(int(150 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), 'STAR', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(16 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(6 * S) - eb[1]), 'STAR', font=ef,
           fill=TEAL_D + (255,))
    wordmark(d, int(34 * S), int(30 * S), int(16 * S), WHITE + (235,))
    hf = font(int(42 * S), 'ExtraBold')
    for i, ln in enumerate(['Обучающие', 'видео']):
        d.text((int(34 * S), int((146 + i * 50) * S)), ln, font=hf, fill=WHITE + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(268 * S)), 'курс для руководителей, 19 минут',
           font=sf, fill=WHITE + (190,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(334 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=CORAL + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
