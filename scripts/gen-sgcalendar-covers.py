#!/usr/bin/env python3
"""Обложки карточки кейса «Концепция новогоднего календаря Saint-Gobain» для
каталога проектов (477x396), механика дизайн-системы v2.2:
- cover-main: КРУГ-постер — декабрьская полоса календаря (потолочный профиль
  Gyproc как башня в нарисованном зимнем городе) в круглой маске под фирменным
  синим тинтом, белый вордмарк SAINT-GOBAIN и красная пилюля-метрика.
- cover-hover: синий КВАДРАТ того же цвета — фоновое эхо «12», белый вордмарк,
  заголовок «Новогодний календарь» и «СМОТРЕТЬ КЕЙС →».
Кладёт в mirror/images/lib/custom-sgcalendar/ (webp — через scripts/gen-webp.sh)."""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-sgcalendar')
PHOTO = os.path.join(ROOT, 'mirror', 'images', 'sgcalendar', 'mock-gyproc.jpg')
# квадрат с башней и городом, без календарной сетки и подписи под изображением
PHOTO_BOX = (150, 120, 1050, 1020)
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

BLUE = (19, 80, 224)
BLUE_D = (13, 58, 168)
RED = (238, 15, 63)
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
    """SAINT-GOBAIN разрядкой: логотип клиента цветной и на синем читается плохо,
    поэтому в обложке он набран текстом."""
    f = font(h_px, 'ExtraBold')
    for ch in 'SAINT-GOBAIN':
        d.text((x, y), ch, font=f, fill=color)
        x += d.textbbox((0, 0), ch, font=f)[2] + h_px * 0.13


def tinted():
    """Полоса календаря под фирменным синим: исходник почти весь белый, и без
    тинта круг на светлом каталоге просто не читался бы как круг."""
    im = Image.open(PHOTO).convert('RGB').crop(PHOTO_BOX).resize((2 * R * SS, 2 * R * SS), Image.LANCZOS)
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            k = (r * 0.30 + g * 0.59 + b * 0.11) / 255      # яркость исходника
            # белая бумага уходит в фирменный синий, рисунок остаётся темнее фона
            px[x, y] = tuple(round(BLUE_D[i] + (BLUE[i] - BLUE_D[i]) * k + (255 - BLUE[i]) * k * k * 0.55)
                             for i in range(3))
    return im


def cover_main():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    cx, cy, r = CX * S, CY * S, R * S
    disc = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    disc.paste(tinted(), (cx - r, cy - r))
    mask = Image.new('L', (W * S, H * S), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(disc, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE + (46,), width=2 * S)
    # вордмарк и метрика оба в нижней половине круга: сверху карточку каталога
    # перекрывает чип категории («Creative & Design»), и всё, что там стоит, режется
    wordmark(d, cx - int(104 * S), cy + int(58 * S), int(22 * S), WHITE + (255,))
    ptxt = '12 МЕСЯЦЕВ'
    pf = font(int(19 * S), 'ExtraBold')
    tb = d.textbbox((0, 0), ptxt, font=pf)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = int(24 * S), int(14 * S)
    pw, ph = tw + px * 2, th + py * 2
    plx, ply = cx - pw // 2, cy + r - int(74 * S)
    d.rounded_rectangle([plx, ply, plx + pw, ply + ph], radius=ph // 2, fill=RED + (255,))
    d.text((plx + px - tb[0], ply + py - tb[1]), ptxt, font=pf, fill=WHITE)
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), BLUE + (255,))
    d = ImageDraw.Draw(img)
    ef = font(int(340 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), '12', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(20 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(2 * S) - eb[1]), '12', font=ef, fill=BLUE_D + (255,))
    wordmark(d, int(34 * S), int(30 * S), int(19 * S), WHITE + (255,))
    hf = font(int(44 * S), 'ExtraBold')
    for i, ln in enumerate(['Новогодний', 'календарь']):
        d.text((int(34 * S), int((160 + i * 52) * S)), ln, font=hf, fill=WHITE + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(276 * S)), 'концепция, 2021', font=sf, fill=WHITE + (200,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(338 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=WHITE + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
