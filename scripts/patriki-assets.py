#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Журнал Patriki Times» (Ай Кей / Ирсон Кудикова).

Источники — два печатных номера:
  ~/Downloads/final 9_5_compressed.pdf              №9,  январь-февраль 2018, 52 полосы
  ~/Downloads/final восстановленно_compressed.pdf   №10, февраль-март 2018,  68 полос

Оба файла — одиночные полосы 220×307 мм: A4 210×297 плюс 5 мм вылетов по кругу
(TrimBox не размечен, поэтому обрез считаем сами и режем ровно 5 мм).

Что делает:
  1. режет вылеты и рендерит избранные полосы обоих номеров для листалки
     (24 полосы №9 и 28 полос №10) плюс миниатюры для ленты под ней;
  2. отдельно кладёт обложки крупно — для героя и для разбора анатомии;
  3. рендерит две типовые текстовые полосы под оверлей модульной сетки:
     трёхколонник (№9, стр. 14) и двухколонник (№9, стр. 33);
  4. вынимает шесть рекламных модулей: Rolls-Royce, «Сенатор», Mangusta,
     Ferretti, JetSmarter и Grand Marina;
  5. склеивает три разворота для раздела «В печати».

Итог: mirror/images/patriki/. После прогона — scripts/gen-webp.sh mirror/images/patriki
Идемпотентно, просто перезаписывает.
"""
import io
import os

import fitz
from PIL import Image

SRC9 = os.path.expanduser('~/Downloads/final 9_5_compressed.pdf')
SRC10 = os.path.expanduser('~/Downloads/final восстановленно_compressed.pdf')
DST = 'mirror/images/patriki'

# вылеты: 5 мм от 220 мм по ширине и от 307 мм по высоте
BLEED_X = 5 / 220
BLEED_Y = 5 / 307

PAGE_PX = 1000      # полоса в листалке
THUMB_PX = 180      # миниатюра в ленте
COVER_PX = 1300     # обложка в герое и в разборе
GRID_PX = 1200      # полоса под оверлей сетки
AD_PX = 820         # рекламный модуль
SPREAD_PX = 2000    # разворот в мокапе

# избранные полосы: без рекламных модулей, они живут своим разделом
PAGES9 = [1, 3, 4, 5, 7, 8, 10, 11, 12, 15, 16, 18, 19, 20,
          22, 25, 30, 34, 36, 40, 42, 46, 48, 52]
PAGES10 = [1, 3, 4, 7, 8, 11, 13, 15, 16, 19, 22, 23, 25, 26,
           28, 30, 35, 38, 40, 42, 46, 50, 54, 56, 60, 62, 64, 68]

# рекламные модули: (документ, полоса, имя)
ADS = [
    (9, 2, 'ad-rollsroyce'),
    (9, 9, 'ad-senator'),
    (9, 21, 'ad-mangusta'),
    (9, 35, 'ad-ferretti'),
    (9, 51, 'ad-jetsmarter'),
    (10, 53, 'ad-grandmarina'),
]

# развороты для «В печати»: (документ, левая полоса, имя)
SPREADS = [
    (9, 18, 'spread-elka'),        # «В лесу родилась ёлочка»
    (10, 8, 'spread-sport'),       # «Патрики спорт», модуль героя
    (10, 22, 'spread-berezka'),    # Bistrot Берёзка
]

os.makedirs(DST, exist_ok=True)
DOCS = {}


def doc(n):
    if n not in DOCS:
        DOCS[n] = fitz.open(SRC9 if n == 9 else SRC10)
    return DOCS[n]


def render(n, page, width):
    """Полоса без вылетов, шириной width пикселей."""
    p = doc(n)[page - 1]
    # рендерим с запасом, чтобы после обрезки вылетов получить нужную ширину
    zoom = (width / (1 - 2 * BLEED_X)) / p.rect.width
    pix = p.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    w, h = im.size
    return im.crop((round(w * BLEED_X), round(h * BLEED_Y),
                    round(w * (1 - BLEED_X)), round(h * (1 - BLEED_Y))))


def save(im, name, q=78):
    p = os.path.join(DST, name)
    im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    return os.path.getsize(p)


total = 0
for n, pages in ((9, PAGES9), (10, PAGES10)):
    print(f'— номер №{n}: {len(pages)} полос')
    for i in pages:
        im = render(n, i, PAGE_PX)
        total += save(im, f'p{n}-{i}.jpg')
        th = im.resize((THUMB_PX, round(im.height * THUMB_PX / im.width)), Image.LANCZOS)
        total += save(th, f't{n}-{i}.jpg', q=74)
    print(f'  полосы и миниатюры готовы')

print('— обложки')
for n in (9, 10):
    total += save(render(n, 1, COVER_PX), f'cover{n}.jpg', q=86)

print('— полосы под оверлей сетки')
total += save(render(9, 14, GRID_PX), 'grid-3col.jpg', q=86)   # трёхколонник, «История»
total += save(render(9, 33, GRID_PX), 'grid-2col.jpg', q=86)   # двухколонник, «Здоровье»

print('— рекламные модули')
for n, i, name in ADS:
    total += save(render(n, i, AD_PX), f'{name}.jpg', q=82)

print('— развороты')
for n, left, name in SPREADS:
    a = render(n, left, SPREAD_PX // 2)
    b = render(n, left + 1, SPREAD_PX // 2)
    sp = Image.new('RGB', (a.width + b.width, max(a.height, b.height)), 'white')
    sp.paste(a, (0, 0))
    sp.paste(b, (a.width, 0))
    total += save(sp, f'{name}.jpg', q=80)

print(f'\nИтого {total // 1024} КБ в {DST}')
