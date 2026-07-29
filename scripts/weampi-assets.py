#!/usr/bin/env python3
"""Ассеты кейса «Брошюра We&I by Vertical Hotel» (Becar Asset Management).

Источник: печатный PDF/X-1a ~/Downloads/Becar_we&i_4+4_+3мм_200916.pdf
24 полосы, квадрат 216×216 мм = 210×210 мм после обрезки + вылеты 3 мм.

Что делает:
  1. режет вылеты (3 мм с каждой стороны) и рендерит полосы в чистый обрез;
  2. склеивает полосы попарно в 11 разворотов (2-3, 4-5 … 22-23) — так буклет
     и читался в руках; обложка (полоса 1) и задник (полоса 24) идут отдельно;
  3. перекладывает 3D-мокапы печатного буклета из /images/lib в папку кейса
     (в lib они лежат PNG по 1,6-2,1 МБ, здесь становятся JPEG).

Итог: mirror/images/weampi/. После прогона — scripts/gen-webp.sh mirror/images/weampi
Идемпотентно, просто перезаписывает.
"""
import os
import io
import fitz
from PIL import Image

SRC = os.path.expanduser('~/Downloads/Becar_we&i_4+4_+3мм_200916.pdf')
LIB = 'mirror/images/lib'
DST = 'mirror/images/weampi'

BLEED_MM = 3
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
        # отдельные миниатюры для ленты под листалкой: иначе на 74 px грузился бы
        # разворот целиком, все 11 сразу
        save(canvas, f'thumb-{i:02d}.jpg', 220, q=80)


# Левая половина слайдера «ТЗ и дизайн»: как разворот про 100% дохода выглядел
# в исходном файле клиента. Правая половина — наш spread-05.jpg.
BRIEF = 'as3535-3864-4461-b337-353235373831/10-26.jpg'

# 3D-мокапы печатного буклета из старой версии кейса: хорошие, оставляем
MOCKUPS = {
    'as3266-6331-4137-b832-653331316332/Perfect_Binding_Broc.png': 'mock-cover.jpg',
    'as6664-3335-4863-a336-643065616431/369.png':                  'mock-float.jpg',
    'as6130-3035-4333-a137-343639663932/Perfect_Binding_Broc.png': 'mock-rooms.jpg',
    'as3332-3936-4235-b137-353766646233/Perfect_Binding_Broc.png': 'mock-navy.jpg',
    'as3361-3630-4635-a239-333238616533/Perfect_Binding_Broc.png': 'mock-hundred.jpg',
}


def mockups():
    for src, name in MOCKUPS.items():
        im = Image.open(os.path.join(LIB, src))
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA')
            bg = Image.new('RGB', im.size, 'white')
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert('RGB')
        save(im, name, 1800)


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
    print('готово →', DST)
