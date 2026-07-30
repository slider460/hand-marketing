#!/usr/bin/env python3
"""Ассеты кейса «Брошюра „Дом с рыцарем“» (Becar Asset Management).

Источник: печатный PDF ~/Downloads/бекар дом с рыцарем финалим-2.pdf
18 полос, альбом 307×190 мм с вылетами (чистый обрез 297×180 мм).

Что делает:
  1. режет вылеты и рендерит полосы в чистый обрез;
  2. кладёт обложку, задник и миниатюры для листалки;
  3. вынимает кадры, которые нужны секциям страницы: фасад, парадное в шевроне,
     интерьер, карта района, планы 2 и 3 этажа.

Итог: mirror/images/knight/. После прогона — scripts/gen-webp.sh mirror/images/knight
Идемпотентно, просто перезаписывает.
"""
import os
import io
import fitz
from PIL import Image

SRC = os.path.expanduser('~/Downloads/бекар дом с рыцарем финалим-2.pdf')
DST = 'mirror/images/knight'

BLEED_MM = 5.0
PAGE_PX = 1700          # ширина полосы в чистом обрезе

os.makedirs(DST, exist_ok=True)


def render_pages():
    """Полосы PDF в чистый обрез, без вылетов."""
    doc = fitz.open(SRC)
    bleed = BLEED_MM / 25.4 * 72
    out = []
    for page in doc:
        r = page.rect
        clip = fitz.Rect(r.x0 + bleed, r.y0 + bleed, r.x1 - bleed, r.y1 - bleed)
        zoom = PAGE_PX / clip.width
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
        out.append(Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB'))
    return out


def save(im, name, maxw, q=86):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    print('  ', name, im.size, f'{os.path.getsize(p)//1024} КБ')


# Кадры для секций страницы: (полоса, имя, доли обрезки left/top/right/bottom)
CROPS = [
    (3,  'facade.jpg', (0.54, 0.07, 0.98, 0.93)),   # фасад дома, северный модерн
    (4,  'gate.jpg', (0.70, 0.00, 1.00, 1.00)),     # парадное и лев, кадр в шевроне
    (9,  'interior.jpg', (0.00, 0.00, 0.52, 1.00)),  # спальня, высокие потолки
    (5,  'map.jpg', (0.50, 0.00, 1.00, 1.00)),      # карта Тверского района
    (11, 'plan-2.jpg', (0.09, 0.02, 0.64, 0.47)),   # план 2 этажа, апартаменты А
    (11, 'plan-3.jpg', (0.40, 0.50, 0.99, 0.94)),   # план 3 этажа, апартаменты В
]


def crops(pages):
    for pg, name, (l, t, r, b) in CROPS:
        im = pages[pg - 1]
        w, h = im.size
        save(im.crop((round(w * l), round(h * t), round(w * r), round(h * b))), name, 1400)


if __name__ == '__main__':
    print('полосы:')
    pages = render_pages()
    for i, im in enumerate(pages, 1):
        save(im, f'page-{i:02d}.jpg', PAGE_PX)
        save(im, f'thumb-{i:02d}.jpg', 220, q=80)
    print('кадры:')
    crops(pages)
    print('готово →', DST)
