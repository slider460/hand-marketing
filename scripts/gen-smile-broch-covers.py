#!/usr/bin/env python3
"""Обложки карточки кейса «Брошюра ТЦ „Смайл“» для каталога проектов (477x396),
механика дизайн-системы v2.2:
- cover-main: КРУГ-постер — фасад торгового центра в круглой маске под фиолетовым
  тинтом, жёлтый вордмарк СМАЙЛ со смайлом и чёрная пилюля-метрика;
- cover-hover: фиолетовый КВАДРАТ того же цвета — фоновое эхо «22», вордмарк,
  заголовок «Брошюра ТЦ „Смайл“» и «СМОТРЕТЬ КЕЙС →».
Кладёт в mirror/images/lib/custom-smile-broch/ (webp — через scripts/gen-webp.sh)."""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-smile-broch')
PHOTO = os.path.join(ROOT, 'mirror', 'images', 'smile-broch', 'ph-facade.jpg')
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

VIO = (74, 59, 158)
VIO_D = (40, 31, 96)
YEL = (255, 195, 36)
INK = (24, 26, 44)
WHITE = (255, 255, 255)
SS = 4


def font(sz, v='Bold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def smile(d, cx, cy, r, fill, ink):
    """Знак издания: жёлтый круг, два глаза-штриха и улыбка."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    w = max(2, round(r * 0.13))
    for dx in (-r * 0.34, r * 0.34):
        d.line([(cx + dx, cy - r * 0.28), (cx + dx, cy + r * 0.02)], fill=ink, width=w)
    d.arc([cx - r * 0.56, cy - r * 0.34, cx + r * 0.56, cy + r * 0.68],
          start=25, end=155, fill=ink, width=w)


def wordmark(d, x, y, h_px, color, text='СМАЙЛ'):
    """Логотип объекта: разряженный капс, как на обложке брошюры."""
    f = font(h_px, 'ExtraBold')
    for ch in text:
        d.text((x, y), ch, font=f, fill=color)
        x += d.textbbox((0, 0), ch, font=f)[2] + h_px * 0.14
    return x


def tinted():
    """Фасад под фиолетовым тинтом: снимок пёстрый (жёлтое здание, вывески),
    без тинта круг не собрался бы с палитрой каталога. Держим относительную
    яркость пикселя."""
    im = Image.open(PHOTO).convert('RGB')
    side = min(im.width, im.height)
    left = max(0, (im.width - side) // 2)
    im = im.crop((left, 0, left + side, side)).resize((2 * R * SS, 2 * R * SS),
                                                     Image.LANCZOS)
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            k = (r * 0.30 + g * 0.59 + b * 0.11) / 255
            px[x, y] = tuple(round(VIO_D[i] + (VIO[i] - VIO_D[i]) * k
                                   + (255 - VIO[i]) * k * k * 0.55) for i in range(3))
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
    x0 = cx - int(96 * S)
    smile(d, x0 - int(20 * S), cy + int(68 * S), int(13 * S), YEL + (255,), VIO_D + (255,))
    wordmark(d, x0 + int(4 * S), cy + int(56 * S), int(24 * S), YEL + (255,))
    ptxt = '22 ПОЛОСЫ'
    pf = font(int(18 * S), 'ExtraBold')
    tb = d.textbbox((0, 0), ptxt, font=pf)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px_, py = int(24 * S), int(14 * S)
    pw, ph = tw + px_ * 2, th + py * 2
    plx, ply = cx - pw // 2, cy + r - int(74 * S)
    d.rounded_rectangle([plx, ply, plx + pw, ply + ph], radius=ph // 2, fill=INK + (255,))
    d.text((plx + px_ - tb[0], ply + py - tb[1]), ptxt, font=pf, fill=YEL + (255,))
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), VIO + (255,))
    d = ImageDraw.Draw(img)
    ef = font(int(340 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), '22', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(18 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(2 * S) - eb[1]), '22', font=ef,
           fill=VIO_D + (255,))
    smile(d, int(44 * S), int(38 * S), int(12 * S), YEL + (255,), VIO + (255,))
    wordmark(d, int(64 * S), int(28 * S), int(18 * S), WHITE + (255,))
    hf = font(int(44 * S), 'ExtraBold')
    for i, ln in enumerate(['Брошюра', 'ТЦ «Смайл»']):
        d.text((int(34 * S), int((152 + i * 52) * S)), ln, font=hf, fill=WHITE + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(276 * S)), 'издание, 22 полосы', font=sf,
           fill=WHITE + (190,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(336 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=YEL + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
