#!/usr/bin/env python3
"""Обложки карточки кейса «Брошюра „Дом с рыцарем“» для каталога проектов (477x396),
механика дизайн-системы v2.2:
- cover-main: КРУГ-постер — фасад доходного дома на Садовой-Самотечной в круглой
  маске под медным тинтом, белый вордмарк ДОМ С РЫЦАРЕМ и чёрная пилюля-метрика;
- cover-hover: медный КВАДРАТ того же цвета — фоновое эхо «18», вордмарк, заголовок
  «Дом с рыцарем» и «СМОТРЕТЬ КЕЙС →».
Кладёт в mirror/images/lib/custom-knight/ (webp — через scripts/gen-webp.sh)."""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-knight')
PHOTO = os.path.join(ROOT, 'mirror', 'images', 'knight', 'facade.jpg')
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

COP = (179, 118, 60)
COP_D = (109, 68, 30)
INK = (20, 19, 16)
WHITE = (255, 255, 255)
SS = 4


def font(sz, v='Bold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def wordmark(d, x, y, h_px, color, text='ДОМ С РЫЦАРЕМ'):
    """Имя дома разрядкой: у объекта нет логотипа, в брошюре это набор капсом."""
    f = font(h_px, 'ExtraBold')
    for ch in text:
        d.text((x, y), ch, font=f, fill=color)
        x += d.textbbox((0, 0), ch, font=f)[2] + h_px * 0.15


def tinted():
    """Фасад под медным тинтом: исходник светлый, без тинта круг не читался бы
    как круг на светлом каталоге. Держим относительную яркость пикселя."""
    im = Image.open(PHOTO).convert('RGB')
    # квадрат по центру фасада: верх кадра с небом обрезаем
    side = min(im.width, im.height)
    top = max(0, (im.height - side) // 3)
    im = im.crop((0, top, side, top + side)).resize((2 * R * SS, 2 * R * SS), Image.LANCZOS)
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            k = (r * 0.30 + g * 0.59 + b * 0.11) / 255
            px[x, y] = tuple(round(COP_D[i] + (COP[i] - COP_D[i]) * k
                                   + (255 - COP[i]) * k * k * 0.5) for i in range(3))
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
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE + (52,), width=2 * S)
    # вордмарк и метрика в нижней половине круга: сверху карточку перекрывает чип
    # категории, и всё, что там стоит, режется
    wordmark(d, cx - int(112 * S), cy + int(58 * S), int(20 * S), WHITE + (255,))
    ptxt = '6 АПАРТАМЕНТОВ'
    pf = font(int(18 * S), 'ExtraBold')
    tb = d.textbbox((0, 0), ptxt, font=pf)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = int(24 * S), int(14 * S)
    pw, ph = tw + px * 2, th + py * 2
    plx, ply = cx - pw // 2, cy + r - int(74 * S)
    d.rounded_rectangle([plx, ply, plx + pw, ply + ph], radius=ph // 2, fill=INK + (255,))
    d.text((plx + px - tb[0], ply + py - tb[1]), ptxt, font=pf, fill=COP + (255,))
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), COP + (255,))
    d = ImageDraw.Draw(img)
    ef = font(int(340 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), '18', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(20 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(2 * S) - eb[1]), '18', font=ef, fill=COP_D + (255,))
    wordmark(d, int(34 * S), int(30 * S), int(17 * S), INK + (255,))
    hf = font(int(46 * S), 'ExtraBold')
    for i, ln in enumerate(['Дом', 'с рыцарем']):
        d.text((int(34 * S), int((156 + i * 54) * S)), ln, font=hf, fill=INK + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(278 * S)), 'брошюра, 18 полос', font=sf, fill=INK + (190,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(338 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=INK + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
