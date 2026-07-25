#!/usr/bin/env python3
"""Логотип OBO Bettermann (Pillow, плоский одноцветный) — верная геометрия:
две буквы «O» — точные кольца, «B» — геометрическая (заливка минус контрформы),
сверху/снизу бруски со скруглёнными концами, снизу вордмарк BETTERMANN,
подогнанный по ширине под бруски. Рисуем ×SS и уменьшаем (чистое сглаживание).
Возвращает RGBA на прозрачном фоне."""
import os
from PIL import Image, ImageDraw, ImageFont

_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'Montserrat.ttf')
SS = 4


def _font(sz, variation='Black'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(variation)
    except Exception:
        pass
    return f


def make_logo(target_w=600, color=(255, 255, 255, 255)):
    H = 240                     # высота литер OBO
    t = 60                      # толщина штриха
    gap = 30                    # зазор между литерами
    Ow = H                      # «O» — круг, ширина = высота
    Bw = 168                    # ширина «B»
    obo_w = Ow + gap + Bw + gap + Ow

    # ── маска литер OBO ──
    m = Image.new('L', (obo_w, H), 0)
    d = ImageDraw.Draw(m)
    # первая O — кольцо
    d.ellipse([0, 0, Ow, H], outline=255, width=t)
    # B
    bx = Ow + gap
    _draw_B(d, bx, 0, Bw, H, t)
    # вторая O
    ox2 = Ow + gap + Bw + gap
    d.ellipse([ox2, 0, ox2 + Ow, H], outline=255, width=t)

    # ── бруски ──
    bar_t = int(t * 0.82)
    bar_gap = int(t * 0.62)
    r = bar_t // 2
    top_h = bar_t + bar_gap + H + bar_gap + bar_t
    canvas = Image.new('L', (obo_w, top_h), 0)
    cd = ImageDraw.Draw(canvas)
    cd.rounded_rectangle([0, 0, obo_w - 1, bar_t], radius=r, fill=255)
    canvas.paste(m, (0, bar_t + bar_gap))
    y2 = bar_t + bar_gap + H + bar_gap
    cd.rounded_rectangle([0, y2, obo_w - 1, y2 + bar_t], radius=r, fill=255)

    # ── BETTERMANN — по ширине брусков, плотно ──
    word = 'BETTERMANN'
    fs = 10
    while True:
        f = _font(fs, 'Black')
        w = ImageDraw.Draw(Image.new('L', (2, 2))).textlength(word, font=f)
        if w >= obo_w or fs > 400:
            break
        fs += 2
    f = _font(fs - 2, 'Black')
    tmp = Image.new('L', (2, 2)); td = ImageDraw.Draw(tmp)
    bb = td.textbbox((0, 0), word, font=f)
    ww, wh = bb[2] - bb[0], bb[3] - bb[1]
    word_gap = int(t * 0.7)
    full_h = top_h + word_gap + wh
    full = Image.new('L', (obo_w, full_h), 0)
    full.paste(canvas, (0, 0))
    fd = ImageDraw.Draw(full)
    fd.text(((obo_w - ww) // 2 - bb[0], top_h + word_gap - bb[1]), word, font=f, fill=255)

    out = Image.new('RGBA', full.size, (color[0], color[1], color[2], 0))
    solid = Image.new('RGBA', full.size, color)
    out = Image.composite(solid, out, full)

    scale = target_w / obo_w
    return out.resize((target_w, max(1, int(full_h * scale))), Image.LANCZOS)


def _draw_B(d, x, y, Bw, H, t):
    """Геометрическая «B»: заливка чашек минус контрформы + спинка."""
    half = H / 2
    # спинка
    d.rectangle([x, y, x + t, y + H], fill=255)
    # верхняя и нижняя чашки (полные эллипсы), левым краем перекрывают спинку
    d.ellipse([x + t - int(t * 0.9), y, x + Bw, y + half + t * 0.15], fill=255)
    d.ellipse([x + t - int(t * 0.9), y + half - t * 0.15, x + Bw, y + H], fill=255)
    # контрформы (дырки)
    inset = t
    d.ellipse([x + t + inset * 0.15, y + t, x + Bw - inset, y + half - t * 0.35], fill=0)
    d.ellipse([x + t + inset * 0.15, y + half + t * 0.35, x + Bw - inset, y + H - t], fill=0)
    # спинку перерисовать поверх, чтобы левый край был ровный
    d.rectangle([x, y, x + t, y + H], fill=255)


if __name__ == '__main__':
    for name, col, bg in [('white', (255, 255, 255, 255), (243, 155, 0, 255)),
                          ('orange', (243, 155, 0, 255), (40, 42, 49, 255)),
                          ('ink', (40, 42, 49, 255), (255, 255, 255, 255))]:
        lg = make_logo(600, col)
        canvas = Image.new('RGBA', (lg.width + 120, lg.height + 120), bg)
        canvas.alpha_composite(lg, (60, 60))
        p = f'/private/tmp/claude-501/-Users-aleksandrnarodetskii-Downloads-hand-marketing-react/c55e4ad3-ed66-4704-acd0-ffc05221bf97/scratchpad/logo2-{name}.png'
        canvas.convert('RGB').save(p)
        print('preview', p, lg.size)
