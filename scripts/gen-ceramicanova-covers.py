#!/usr/bin/env python3
"""Обложки карточки кейса «Имиджевые ролики для CeramicaNova» для каталога
проектов (477x396), механика дизайн-системы v2.2:
- cover-main: КРУГ-постер — реальный кадр (подкрашенная вода в чаше) в круглой
  маске + мягкий графитовый градиент снизу, белый вордмарк «ceramicanova ♥»
  и пилюля-метрика «17 роликов».
- cover-hover: малиновый КВАДРАТ фирменного цвета — фоновое эхо «17», белый
  вордмарк, заголовок «Имиджевые ролики» и «СМОТРЕТЬ КЕЙС →».
Кладёт в mirror/images/lib/custom-ceramicanova/ (webp — через scripts/gen-webp.sh)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
CX, CY, R = 238, 190, 178
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-ceramicanova')
PHOTO = os.path.join(ROOT, 'mirror', 'images', 'ceramicanova', 'poster-cn02.jpg')
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

RED = (225, 16, 63)
RED_D = (182, 13, 51)
INK = (13, 14, 17)
WHITE = (255, 255, 255)
SS = 4


def font(sz, v='Bold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def heart(size, color):
    """Маленькое фирменное сердце (PNG RGBA)."""
    s = size * 4
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = s * 0.27
    d.ellipse([s*0.5-2*r, s*0.16, s*0.5, s*0.16+2*r], fill=color)
    d.ellipse([s*0.5, s*0.16, s*0.5+2*r, s*0.16+2*r], fill=color)
    d.polygon([(s*0.5-2*r+2, s*0.16+r*1.15), (s*0.5+2*r-2, s*0.16+r*1.15), (s*0.5, s*0.9)], fill=color)
    return im.resize((size, size), Image.LANCZOS)


def wordmark(draw, img, x, y, h_px, color, S):
    """Рисует «ceramica nova ♥»: ceramica (Medium) + nova (ExtraBold) + сердце."""
    fa = font(h_px, 'Medium'); fb = font(h_px, 'ExtraBold')
    d = draw
    d.text((x, y), 'ceramica', font=fa, fill=color)
    wa = d.textbbox((0, 0), 'ceramica', font=fa)[2]
    d.text((x + wa, y), 'nova', font=fb, fill=color)
    wb = d.textbbox((0, 0), 'nova', font=fb)[2]
    hs = int(h_px * 0.5)
    ht = heart(hs, RED + (255,))
    img.alpha_composite(ht, (int(x + wa + wb + h_px * 0.16), int(y - h_px * 0.06)))


def cover_main():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    cx, cy, r = CX * S, CY * S, R * S
    # фото в круглой маске
    photo = Image.open(PHOTO).convert('RGB')
    side = min(photo.size)
    photo = photo.crop(((photo.width-side)//2, (photo.height-side)//2,
                        (photo.width+side)//2, (photo.height+side)//2)).resize((2*r, 2*r), Image.LANCZOS)
    disc = Image.new('RGBA', (W*S, H*S), (0, 0, 0, 0))
    disc.paste(photo, (cx-r, cy-r))
    mask = Image.new('L', (W*S, H*S), 0)
    ImageDraw.Draw(mask).ellipse([cx-r, cy-r, cx+r, cy+r], fill=255)
    img.paste(disc, (0, 0), mask)
    # градиент снизу для читаемости (графит → прозрачный), в маске круга
    grad = Image.new('L', (1, 2*r), 0)
    for i in range(2*r):
        t = i / (2*r)
        grad.putpixel((0, i), int(max(0, (t-0.42)/0.58) * 205))
    grad = grad.resize((2*r, 2*r))
    gfull = Image.new('L', (W*S, H*S), 0); gfull.paste(grad, (cx-r, cy-r))
    gm = Image.new('L', (W*S, H*S), 0)
    gm.paste(gfull.crop((cx-r, cy-r, cx+r, cy+r)), (cx-r, cy-r))
    gm = Image.composite(gm, Image.new('L', (W*S, H*S), 0), mask)
    ink_layer = Image.new('RGBA', (W*S, H*S), INK + (255,))
    img = Image.alpha_composite(img, Image.composite(ink_layer, Image.new('RGBA', (W*S, H*S), (0, 0, 0, 0)), gm))
    d = ImageDraw.Draw(img)
    # тонкое кольцо-обводка
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=WHITE + (38,), width=2*S)
    # вордмарк снизу
    wordmark(d, img, cx - int(96*S), cy + int(96*S), int(26*S), WHITE + (255,), S)
    # метрика «17 РОЛИКОВ» — малиновая пилюля у верха круга
    ptxt = '17 РОЛИКОВ'
    pf = font(int(19*S), 'ExtraBold')
    tb = d.textbbox((0, 0), ptxt, font=pf)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    px, py = int(24*S), int(14*S)
    pw, ph = tw+px*2, th+py*2
    plx, ply = cx - pw//2, cy - r + int(26*S)
    d.rounded_rectangle([plx, ply, plx+pw, ply+ph], radius=ph//2, fill=RED + (255,))
    d.text((plx+px-tb[0], ply+py-tb[1]), ptxt, font=pf, fill=WHITE)
    return img.resize((W, H), Image.LANCZOS)


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W*S, H*S), RED + (255,))
    d = ImageDraw.Draw(img)
    # фоновое эхо «17»
    ef = font(int(340*S), 'ExtraBold')
    eb = d.textbbox((0, 0), '17', font=ef)
    d.text((W*S - (eb[2]-eb[0]) - int(20*S) - eb[0], H*S - (eb[3]-eb[1]) - int(2*S) - eb[1]),
           '17', font=ef, fill=RED_D + (255,))
    # вордмарк сверху
    wordmark(d, img, int(34*S), int(30*S), int(23*S), WHITE + (255,), S)
    # заголовок
    hf = font(int(46*S), 'ExtraBold')
    for i, ln in enumerate(['Имиджевые', 'ролики']):
        d.text((int(34*S), int((170+i*54)*S)), ln, font=hf, fill=WHITE + (255,))
    # СМОТРЕТЬ КЕЙС →
    cf = font(int(20*S), 'Bold')
    d.text((int(35*S), int(338*S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=WHITE + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_main().save(os.path.join(OUT, 'cover-main.png'))
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', OUT)
