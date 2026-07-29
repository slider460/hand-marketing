#!/usr/bin/env python3
"""Ассеты кейса «Брошюра Vertical BW Signature Collection» (Becar Asset Management).

Источник: печатный PDF ~/Downloads/Vertical_for_print.pdf
24 полосы, квадрат 215×215 мм (210×210 в чистом обрезе + вылеты 2,5 мм).

Что делает:
  1. режет вылеты и рендерит полосы в чистый обрез;
  2. склеивает полосы попарно в 11 разворотов (2-3, 4-5 … 22-23); обложка (полоса 1)
     и задник (полоса 24) идут отдельно;
  3. перекладывает мокапы печатного буклета из /images/lib в папку кейса; у мокапа
     разворота про Becar фон был фиолетовый, вне палитры Vertical, — перекрашиваем
     его в фирменный малиновый;
  4. готовит левую половину шторки «ТЗ и дизайн»: текст клиента без вёрстки.

Итог: mirror/images/vertical/. После прогона — scripts/gen-webp.sh mirror/images/vertical
Идемпотентно, просто перезаписывает.
"""
import os
import io
import fitz
from PIL import Image

SRC = os.path.expanduser('~/Downloads/Vertical_for_print.pdf')
LIB = 'mirror/images/lib'
DST = 'mirror/images/vertical'

BLEED_MM = 2.5
PAGE_PX = 1250          # ширина одной полосы в чистом обрезе → разворот 2500 px
COVER_PX = 1400

os.makedirs(DST, exist_ok=True)


def render_pages():
    """Полосы PDF в чистый обрез, без вылетов."""
    doc = fitz.open(SRC)
    bleed = BLEED_MM / 25.4 * 72
    out = []
    for page in doc:
        r = page.rect
        clip = fitz.Rect(r.x0 + bleed, r.y0 + bleed, r.x1 - bleed, r.y1 - bleed)
        zoom = COVER_PX / clip.width
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
        out.append(Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB'))
    return out


def save(im, name, maxw, q=86):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    print('  ', name, im.size, f'{os.path.getsize(p)//1024} КБ')


def spreads(pages):
    """Полосы 2-3, 4-5 … 22-23 — так буклет раскрывается на столе."""
    for i, left in enumerate(range(2, 23, 2), start=1):
        a, b = pages[left - 1], pages[left]
        w = PAGE_PX
        h = round(a.height * w / a.width)
        a = a.resize((w, h), Image.LANCZOS)
        b = b.resize((w, h), Image.LANCZOS)
        canvas = Image.new('RGB', (w * 2, h), 'white')
        canvas.paste(a, (0, 0))
        canvas.paste(b, (w, 0))
        save(canvas, f'spread-{i:02d}.jpg', w * 2)
        # миниатюры для ленты под листалкой: иначе на 74 px грузились бы все 11
        # разворотов целиком
        save(canvas, f'thumb-{i:02d}.jpg', 220, q=80)


# Левая половина слайдера «ТЗ и дизайн»: текст, который пришёл от клиента, без вёрстки.
# Тот же файл стоял в этом блоке на прежней версии кейса. Правая половина — spread-11.jpg.
BRIEF = 'as3535-3864-4461-b337-353235373831/10-26.jpg'

# 3D-мокапы печатного буклета из старой версии кейса
MOCKUPS = {
    'as6239-6132-4132-b165-363935373165/Perfect_Binding_Broc.png': 'mock-cover.jpg',
    'as3835-3039-4365-b261-623664653866/Perfect_Binding_Broc.jpg': 'mock-what.jpg',
}
# на этом мокапе четыре ракурса двух разворотов: режем на два отдельных кадра,
# иначе в сетке «В печати» один и тот же разворот стоит по два-три раза
MOCK_CROPS = [
    ('as6461-3831-4133-a563-623562653239/3694567890.jpg', 'mock-life.jpg',
     (0.19, 0.615, 0.79, 1.0)),      # разворот 10-11, нижний экземпляр
    ('as6461-3831-4133-a563-623562653239/3694567890.jpg', 'mock-numbers.jpg',
     (0.235, 0.0, 0.775, 0.305)),    # разворот 2-3, верхний экземпляр
]
# у этого фон фиолетовый, перекрашиваем
MOCK_RECOLOR = ('as3439-3865-4561-a134-373531313961/Perfect_Binding_Broc.png',
                'mock-becar.jpg')
BERRY = (162, 25, 91)


def flatten(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, 'white')
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert('RGB')


def mockups():
    for src, name in MOCKUPS.items():
        save(flatten(Image.open(os.path.join(LIB, src))), name, 1800)


def recolor_mockup():
    """Фиолетовый фон мокапа в фирменный малиновый. Фон однородный, но с мягкой
    тенью под буклетом, поэтому не заливаем плашкой: держим относительную яркость
    пикселя, меняем только сам цвет."""
    src, name = MOCK_RECOLOR
    im = flatten(Image.open(os.path.join(LIB, src)))
    px = im.load()
    w, h = im.size
    base = px[8, 8]                      # угол — заведомо фон
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            # фиолетовый: синева заметно выше зелени, красный между ними
            if b > g + 40 and b > 90 and r < b:
                k = (r + g + b) / (base[0] + base[1] + base[2])   # тень темнее фона
                px[x, y] = tuple(min(255, round(c * k)) for c in BERRY)
    save(im, name, 1800)


CARD_RATIO = 4 / 3      # сетка «В печати» режет карточки под 4:3


def crop_mockups():
    """По одному буклету на кадр вместо повторяющихся ракурсов. Кадр добиваем полями
    цвета фона до пропорции карточки: иначе широкий кроп обрежется по бокам и съест
    заголовок разворота."""
    for src, name, (l, t, r, b) in MOCK_CROPS:
        im = flatten(Image.open(os.path.join(LIB, src)))
        w, h = im.size
        cut = im.crop((round(w * l), round(h * t), round(w * r), round(h * b)))
        cw, ch = cut.size
        box = (cw, max(ch, round(cw / CARD_RATIO)))
        canvas = Image.new('RGB', box, im.getpixel((4, 4)))
        canvas.paste(cut, (0, (box[1] - ch) // 2))
        save(canvas, name, 1400)


def brief():
    """ТЗ приводим ровно к 2:1, чтобы шторка совпадала с разворотом пиксель в пиксель."""
    im = Image.open(os.path.join(LIB, BRIEF)).convert('RGB')
    h = round(im.width / 2)
    top = max(0, (im.height - h) // 2)
    save(im.crop((0, top, im.width, top + h)), 'brief.jpg', 1680)


if __name__ == '__main__':
    print('полосы:')
    pages = render_pages()
    save(pages[0], 'cover.jpg', COVER_PX)
    save(pages[23], 'back.jpg', COVER_PX)
    print('развороты:')
    spreads(pages)
    print('ТЗ для шторки:')
    brief()
    print('мокапы:')
    mockups()
    recolor_mockup()
    crop_mockups()
    print('готово →', DST)
