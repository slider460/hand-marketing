#!/usr/bin/env python3
# Титульные карточки 2560x1440 (запас под zoompan) в стиле белых карточек HM
import os
from PIL import Image, ImageDraw, ImageFont

SC = os.path.dirname(os.path.abspath(__file__))
W, H = 2560, 1440
FONT_XB = os.path.join(SC, "fonts/montserrat-latin-800.ttf")   # латиница
FONT_SB = os.path.join(SC, "fonts/montserrat-600.ttf")         # кириллица

logo = Image.open(os.path.join(SC, "logo/logo_header.svg.png")).convert("RGBA")
# обрезать прозрачные/белые поля по содержимому
bbox = logo.convert("RGB").point(lambda p: 0 if p > 245 else 255).convert("L").getbbox()
logo = logo.crop(bbox)

def spaced_text(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking

def text_width(draw, text, font, tracking):
    return sum(draw.textlength(c, font=font) for c in text) + tracking * (len(text) - 1)

def make_card(path, url_line=False):
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    # куб
    lh = 560
    lw = int(logo.width * lh / logo.height)
    lg = logo.resize((lw, lh), Image.LANCZOS)
    img.paste(lg, ((W - lw) // 2, int(H * 0.16)), lg)
    # HAND MARKETING
    f1 = ImageFont.truetype(FONT_XB, 120)
    t1 = "HAND MARKETING"
    tr1 = 42
    w1 = text_width(d, t1, f1, tr1)
    spaced_text(d, ((W - w1) / 2, int(H * 0.60)), t1, f1, (26, 26, 26), tr1)
    # подпись
    f2 = ImageFont.truetype(FONT_SB, 52)
    t2 = "рекламное агентство полного цикла"
    tr2 = 10
    w2 = text_width(d, t2, f2, tr2)
    spaced_text(d, ((W - w2) / 2, int(H * 0.72)), t2, f2, (140, 140, 140), tr2)
    if url_line:
        f3 = ImageFont.truetype(FONT_XB, 56)
        t3 = "hand-marketing.ru"
        tr3 = 16
        w3 = text_width(d, t3, f3, tr3)
        spaced_text(d, ((W - w3) / 2, int(H * 0.82)), t3, f3, (150, 194, 35), tr3)
    img.save(path)
    print("saved", path)

make_card(os.path.join(SC, "card_intro.png"), url_line=False)
make_card(os.path.join(SC, "card_outro.png"), url_line=True)
