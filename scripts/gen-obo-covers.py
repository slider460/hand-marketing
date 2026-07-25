#!/usr/bin/env python3
"""Обложки карточки кейса «OBO Bettermann Academy — серия продуктовых роликов»
для каталога проектов (477x396), механика дизайн-системы v2.2:
- cover-main: КРУГ на прозрачном фоне — фирменный оранжевый OBO, диагональная
  штриховка (мотив брендбука), крупный белый логотип OBO Bettermann + метрика
  «10 роликов».
- cover-hover: оранжевый ПРЯМОУГОЛЬНИК того же цвета — фоновое эхо «OBO»,
  заголовок «Серия продуктовых роликов», «СМОТРЕТЬ КЕЙС →».
Кладёт в mirror/images/lib/custom-obo-academy/ (webp — через scripts/gen-webp.sh)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
# ОФИЦИАЛЬНЫЙ логотип (белый, растеризован из исходника движком браузера — build-вход)
LOGO_WHITE = os.path.join(HERE, 'assets', 'logo-white.png')


def logo(target_w):
    lg = Image.open(LOGO_WHITE).convert('RGBA')
    h = max(1, round(target_w * lg.height / lg.width))
    return lg.resize((target_w, h), Image.LANCZOS)


W, H = 477, 396
CX, CY, R = 238, 190, 176
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-obo-academy')
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

ORANGE = (243, 155, 0)
ORANGE_D = (214, 132, 0)
INK = (40, 42, 49)
WHITE = (255, 255, 255)
SS = 4  # рисуем крупно, потом уменьшаем


def font(sz, v='Black'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def hatch(size, color, step, width, alpha):
    """Слой диагональной штриховки (мотив обложки брендбука)."""
    w, h = size
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = color + (alpha,)
    x = -h
    while x < w:
        d.line([(x, h), (x + h, 0)], fill=c, width=width)
        x += step
    return lay


def cover_main():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy, r = CX * S, CY * S, R * S
    # круг
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE + (255,))
    # штриховка внутри круга (по маске)
    hl = hatch((W * S, H * S), WHITE, 26 * S, 3 * S, 42)
    mask = Image.new('L', (W * S, H * S), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(hl, (0, 0), Image.composite(hl.split()[3], Image.new('L', img.size, 0), mask))
    # тонкое внутреннее кольцо
    d.ellipse([cx - r + 7 * S, cy - r + 7 * S, cx + r - 7 * S, cy + r - 7 * S],
              outline=WHITE + (60,), width=2 * S)
    # официальный логотип OBO по центру (белый)
    lg = logo(int(236 * S))
    img.alpha_composite(lg, (cx - lg.width // 2, cy - lg.height // 2 - int(10 * S)))
    # метрика «10 роликов» — тёмная пилюля у низа круга
    d2 = d
    ptxt = '10 РОЛИКОВ'
    pf = font(int(20 * S), 'ExtraBold')
    tb = d2.textbbox((0, 0), ptxt, font=pf)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = int(28 * S), int(16 * S)
    pill_w, pill_h = tw + px * 2, th + py * 2
    plx, ply = cx - pill_w // 2, cy + r - pill_h - int(30 * S)
    d2.rounded_rectangle([plx, ply, plx + pill_w, ply + pill_h], radius=pill_h // 2, fill=INK + (255,))
    d2.text((plx + px - tb[0], ply + py - tb[1]), ptxt, font=pf, fill=WHITE)
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), ORANGE + (255,))
    d = ImageDraw.Draw(img)
    # штриховка по всему полю
    img.alpha_composite(hatch((W * S, H * S), WHITE, 30 * S, 3 * S, 30))
    # фоновое эхо «OBO» — крупно, чуть темнее
    ef = font(int(300 * S), 'Black')
    eb = d.textbbox((0, 0), 'OBO', font=ef)
    d.text((W * S - (eb[2] - eb[0]) - int(30 * S) - eb[0], H * S - (eb[3] - eb[1]) - int(6 * S) - eb[1]),
           'OBO', font=ef, fill=ORANGE_D + (255,))
    # официальный логотип сверху (белый — на оранжевом читается корректно)
    lg = logo(int(132 * S))
    img.alpha_composite(lg, (int(34 * S), int(26 * S)))
    # заголовок
    hf = font(int(44 * S), 'ExtraBold')
    lines = ['Серия', 'продуктовых', 'роликов']
    y = int(168 * S)
    for ln in lines:
        d.text((int(34 * S), y), ln, font=hf, fill=INK + (255,))
        y += int(50 * S)
    # СМОТРЕТЬ КЕЙС →
    cf = font(int(21 * S), 'Bold')
    d.text((int(35 * S), int(336 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=INK + (255,))
    return img.convert('RGBA').resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
