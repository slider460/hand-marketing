#!/usr/bin/env python3
"""Обложки карточки кейса «Новогодний сувенир ЦМ РЖД» (477×396),
механика дизайн-системы v2.2:
- cover-main: КРУГ-постер в фирменной бирюзе дирекции, по кругу пущен разгон
  (тот же движок полос, что и на самой странице кейса), поверх лежит
  печатный лист «03 март» с лёгким наклоном, ниже вордмарк ЦМ РЖД
  и пилюля-метрика «12 УСЛУГ»;
- cover-hover: КВАДРАТ той же бирюзы, фоновое эхо «2019», вордмарк,
  заголовок «Календарь и набор» и «СМОТРЕТЬ КЕЙС →».
Старая карточка была стоковым валенком с ёлкой, к кейсу отношения не имела.

Бирюза снята с макета календаря (#008A96), см. scripts/rgd-suvenir-assets.py.
Кладёт в mirror/images/lib/custom-rgd-suvenir/ (+ webp через gen-webp.sh).
"""
import json
import math
import os
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
SS = 4  # суперсэмплинг
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-rgd-suvenir')
SHEET = os.path.join(ROOT, 'mirror', 'images', 'rgd-suvenir', 'sheet-march.jpg')
MAP = os.path.join(ROOT, 'scripts', 'a2', 'rgd_suvenir_map.json')
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

PAL = json.load(open(MAP, encoding='utf-8'))['palette']


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


TEAL = rgb(PAL['teal'])
TEAL_D = (0, 92, 101)
TEAL_L = rgb(PAL['tealLight'])
BLUE = rgb(PAL['blue'])
GREEN = rgb(PAL['green'])
ACCENT = (238, 15, 63)
WHITE = (255, 255, 255)

# лист «03 март» вырезан из мокапа тиража по краю бумаги, без стены
SHEET_BOX = (.316, .147, .686, .876)


def font(sz, v='Bold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def wordmark(d, x, y, h_px, color):
    """ЦМ РЖД разрядкой: фирменный знак дирекции на бирюзе набираем текстом."""
    f = font(h_px, 'ExtraBold')
    for ch in 'ЦМ РЖД':
        d.text((x, y), ch, font=f, fill=color)
        x += d.textbbox((0, 0), ch, font=f)[2] + h_px * 0.14


def run(size, seed=20181123, dens=.85, lane=None, cols=None):
    """Разгон полос: тот же приём, что и на странице кейса, только на PIL.
    Полосы под 45°, длина и толщина случайные, плотность нарастает к углу."""
    w = h = size
    big = int(size * 1.6)
    img = Image.new('RGBA', (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lane = lane or size / 15
    cols = cols or [TEAL_L, TEAL_L, BLUE, TEAL_D, GREEN, WHITE]
    rnd = _rnd(seed)
    lanes = int(big / lane) + 2
    for i in range(lanes):
        y = i * lane
        across = i / lanes
        x = -big * .2
        while x < big * 1.2:
            along = (x + big * .2) / (big * 1.4)
            p = dens * (.35 + 1.3 * along) * (.5 + 1.1 * (1 - across))
            ln = lane * (1.2 + rnd() * (2 + 8 * min(1, p)))
            if rnd() < min(.9, p):
                c = cols[int(rnd() * len(cols))]
                th = lane * (.3 + rnd() * .55)
                a = 190 if c is not WHITE else 130
                d.rectangle([x, y, x + ln, y + th], fill=tuple(c) + (a,))
            x += ln + lane * (.2 + rnd() * 1.4)
    img = img.rotate(-45, resample=Image.BICUBIC, center=(big / 2, big / 2))
    off = (big - size) // 2
    return img.crop((off, off, off + size, off + size))


def _rnd(seed):
    """mulberry32, тот же генератор, что и в JS на странице."""
    state = {'a': seed & 0xFFFFFFFF}

    def nxt():
        state['a'] = (state['a'] + 0x6D2B79F5) & 0xFFFFFFFF
        t = state['a']
        t = (t ^ (t >> 15)) * (1 | t) & 0xFFFFFFFF
        t = (t + ((t ^ (t >> 7)) * (61 | t) & 0xFFFFFFFF)) & 0xFFFFFFFF ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


def sheet_img(target_h):
    im = Image.open(SHEET).convert('RGBA')
    w, h = im.size
    x0, y0, x1, y1 = SHEET_BOX
    im = im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
    k = target_h / im.height
    return im.resize((round(im.width * k), target_h), Image.LANCZOS)


def cover_main():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    cx, cy, r = CX * S, CY * S, R * S
    d = ImageDraw.Draw(img)

    # круг: фирменная бирюза с уходом в глубину книзу
    disc = Image.new('RGBA', (2 * r, 2 * r), TEAL + (255,))
    dp = disc.load()
    for y in range(2 * r):
        k = y / (2 * r)
        col = tuple(round(TEAL[i] + (TEAL_D[i] - TEAL[i]) * k * k) for i in range(3))
        for x in range(2 * r):
            dp[x, y] = col + (255,)
    disc.alpha_composite(run(2 * r, dens=.8, lane=2 * r / 13))
    mask = Image.new('L', (W * S, H * S), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    tmp = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    tmp.paste(disc, (cx - r, cy - r))
    img.paste(tmp, (0, 0), mask)

    # печатный лист поверх круга: выходит за верхний край, как и положено
    # 3D-блокам системы, снизу остаётся чистое поле под вордмарк и метрику
    sh = sheet_img(int(r * 1.42))
    sh = sh.rotate(-4, resample=Image.BICUBIC, expand=True)
    shadow = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    sm = sh.split()[3].point(lambda a: min(120, a))
    shadow.paste((0, 40, 44, 120), (cx - sh.width // 2 + 6 * S,
                                    cy - sh.height // 2 - int(40 * S) + 8 * S), sm)
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(9 * S)))
    img.alpha_composite(sh, (cx - sh.width // 2, cy - sh.height // 2 - int(40 * S)))

    wordmark(d, cx - int(56 * S), cy + int(92 * S), int(20 * S), WHITE + (255,))
    ptxt = '12 УСЛУГ'
    pf = font(int(19 * S), 'ExtraBold')
    tb = d.textbbox((0, 0), ptxt, font=pf)
    px, py = int(24 * S), int(14 * S)
    pw, ph = tb[2] - tb[0] + px * 2, tb[3] - tb[1] + py * 2
    plx, ply = cx - pw // 2, cy + r - int(58 * S)
    d.rounded_rectangle([plx, ply, plx + pw, ply + ph], radius=ph // 2,
                        fill=ACCENT + (255,))
    d.text((plx + px - tb[0], ply + py - tb[1]), ptxt, font=pf, fill=WHITE)
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), TEAL + (255,))
    d = ImageDraw.Draw(img)
    ef = font(int(190 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), '2019', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(14 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(4 * S) - eb[1]), '2019',
           font=ef, fill=TEAL_D + (255,))
    wordmark(d, int(34 * S), int(30 * S), int(19 * S), WHITE + (255,))
    hf = font(int(44 * S), 'ExtraBold')
    for i, ln in enumerate(['Календарь', 'и набор']):
        d.text((int(34 * S), int((160 + i * 52) * S)), ln, font=hf,
               fill=WHITE + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(276 * S)), '13 листов, месяц равен услуге',
           font=sf, fill=WHITE + (205,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(338 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf,
           fill=WHITE + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, im in (('cover-main.png', cover_main()),
                     ('cover-hover.png', cover_hover())):
        p = os.path.join(OUT, name)
        im.save(p)
        subprocess.run(['cwebp', '-quiet', '-q', '88', '-m', '6', '-sharp_yuv',
                        '-metadata', 'none', p, '-o', p + '.webp'], check=True)
    print('written', OUT)
