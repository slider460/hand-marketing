#!/usr/bin/env python3
"""Обложки карточки кейса «Брендбук Metra Technology Group» для каталога (477x396),
механика дизайн-системы v2.2:
- cover-main: КРУГ-постер — кадр роботизированной ячейки под бирюзовым тинтом
  (то самое правило фотостиля из брендбука), белый логотип и метрика «5 брендов»;
- cover-hover: бирюзовый КВАДРАТ того же цвета — фоновое эхо «69», логотип,
  заголовок «Брендбук Metra» и «СМОТРЕТЬ КЕЙС →».
Логотип не рисуем руками: растеризуем настоящий вектор из mirror/images/metra.
Кладёт в mirror/images/lib/custom-metra/ (webp — через scripts/gen-webp.sh)."""
import os

import fitz
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
SRC = os.path.join(ROOT, 'mirror', 'images', 'metra')
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-metra')
PHOTO = os.path.join(SRC, 'photo-cell.jpg')
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

COL = (0, 95, 124)
COL_D = (0, 50, 63)
COL_L = (135, 199, 215)
INK = (20, 24, 26)
WHITE = (255, 255, 255)
SS = 4


def font(sz, v='Bold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def logo(width_px, white=True):
    """Логотип из SVG в прозрачный PNG нужной ширины."""
    path = os.path.join(SRC, 'logo-mtg.svg')
    src = open(path, encoding='utf-8').read()
    if white:
        src = src.replace('#005F7C', '#FFFFFF').replace('#2188A0', '#FFFFFF') \
                 .replace('#87C7D7', '#FFFFFF')
    tmp = os.path.join(OUT, '_logo.svg')
    open(tmp, 'w', encoding='utf-8').write(src)
    doc = fitz.open(tmp)
    page = doc[0]
    zoom = width_px / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=True)
    img = Image.frombytes('RGBA', (pix.width, pix.height), pix.samples)
    os.remove(tmp)
    return img


def tinted():
    """Кадр под фирменным тинтом: в брендбуке фотография всегда уходит в глубину
    под тёмным слоем, здесь тот же приём, только цветом бренда."""
    im = Image.open(PHOTO).convert('RGB')
    side = min(im.width, im.height)
    left = (im.width - side) // 2
    im = im.crop((left, 0, left + side, side)).resize((2 * R * SS, 2 * R * SS), Image.LANCZOS)
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            k = (r * 0.30 + g * 0.59 + b * 0.11) / 255
            px[x, y] = tuple(round(COL_D[i] + (COL[i] - COL_D[i]) * k
                                   + (255 - COL[i]) * k * k * 0.34) for i in range(3))
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
    # логотип и метрика в нижней половине круга: сверху карточку перекрывает чип
    # категории, и всё, что там стоит, режется
    lg = logo(int(210 * S))
    img.paste(lg, (cx - lg.width // 2, cy + int(34 * S)), lg)
    ptxt = '5 БРЕНДОВ'
    pf = font(int(18 * S), 'ExtraBold')
    tb = d.textbbox((0, 0), ptxt, font=pf)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = int(24 * S), int(14 * S)
    pw, ph = tw + px * 2, th + py * 2
    plx, ply = cx - pw // 2, cy + r - int(74 * S)
    d.rounded_rectangle([plx, ply, plx + pw, ply + ph], radius=ph // 2, fill=INK + (255,))
    d.text((plx + px - tb[0], ply + py - tb[1]), ptxt, font=pf, fill=COL_L + (255,))
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), COL + (255,))
    d = ImageDraw.Draw(img)
    ef = font(int(340 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), '69', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(18 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(2 * S) - eb[1]), '69', font=ef, fill=COL_D + (255,))
    lg = logo(int(168 * S))
    img.paste(lg, (int(34 * S), int(30 * S)), lg)
    hf = font(int(44 * S), 'ExtraBold')
    for i, ln in enumerate(['Брендбук', 'Metra']):
        d.text((int(34 * S), int((150 + i * 52) * S)), ln, font=hf, fill=WHITE + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(274 * S)), 'архитектура бренда, 69 полос',
           font=sf, fill=WHITE + (185,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(336 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=WHITE + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
