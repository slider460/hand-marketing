#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Брошюра ТЦ Смайл» (Becar Asset Management).

Источник: печатный PDF ~/Downloads/Тц Смайл _ презентация 2020 (2).pdf
Файл сверстан развороты: полоса 1 (обложка), десять разворотов 420×210 мм
и полоса 22 (задник). Итого 22 полосы, квадрат 210×210 мм. Вылеты не размечены
(TrimBox = MediaBox), поэтому полосы берём целиком, без обрезки.

Что делает:
  1. рендерит страницы файла: обложку и задник отдельно, десять разворотов как есть
     (склеивать попарно не нужно, в файле они уже развороты) + миниатюры для ленты
     под листалкой;
  2. вынимает карту зоны охвата (левая половина разворота 14-15): она нарисована
     в цветах издания и работает подложкой живого блока про зоны охвата;
  3. режет фотополосу по низу разворота 10-11 на три кадра: Familia, Kidster
     и фасад ТЦ;
  4. вынимает три кадра графической системы для раздела «Приёмы»: жёлтая дуга
     с мятной половины разворота 6-7, текст-эхо «СИНЕРГИЯ» с разворота 2-3
     и жёлтые цифры в неоне с разворота 12-13;
  5. копирует контурный вордмарк СМАЙЛ из ассетов кейса посадочной страницы
     (/images/smile), чтобы кейс не зависел от соседней папки.

Итог: mirror/images/smile-broch/. После прогона — scripts/gen-webp.sh mirror/images/smile-broch
Идемпотентно, просто перезаписывает.
"""
import io
import os
import shutil

import fitz
from PIL import Image

SRC = os.path.expanduser('~/Downloads/Тц Смайл _ презентация 2020 (2).pdf')
DST = 'mirror/images/smile-broch'
SMILE = 'mirror/images/smile'          # ассеты кейса посадочной страницы

SPREAD_PX = 2400        # разворот 420×210 мм
COVER_PX = 1200         # обложка и задник квадратные
HIRES = 4000            # для мелких фотографий на полосе рендерим страницу крупнее

os.makedirs(DST, exist_ok=True)


def save(im, name, maxw, q=86):
    if im.mode != 'RGB':
        im = im.convert('RGB')
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    print('  ', name, im.size, f'{os.path.getsize(p)//1024} КБ')


def render(page, width):
    zoom = width / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')


def cut(im, box, name, maxw, q=86):
    """box — доли ширины и высоты страницы."""
    w, h = im.size
    l, t, r, b = box
    save(im.crop((round(w * l), round(h * t), round(w * r), round(h * b))), name, maxw, q)


# ─── кадры с полос: (страница файла, доли, имя, ширина) ──────────────────────
# карта района: левая половина разворота «Расположение»
MAP = (8, (0.0, 0.0, 0.5, 1.0), 'map.jpg', 1100)

# фотополоса по низу разворота «Секрет успеха»: три кадра вместо одной ленты
PHOTOS = [
    ((0.4906, 0.795, 0.675, 1.0), 'ph-familia.jpg'),   # вход в Familia
    ((0.675, 0.795, 0.822, 1.0), 'ph-kidster.jpg'),    # Kidster, товары для мам
    ((0.822, 0.795, 1.0, 1.0), 'ph-facade.jpg'),       # фасад ТЦ с вывесками
]
PHOTO_PAGE = 6

# приёмы графической системы
# кадры режем под 4:3, в сетке «Приёмы» карточки кадрируются по этой пропорции
CRAFT = [
    (4, (0.02, 0.06, 0.46, 0.72), 'craft-arc.jpg', 1100),   # дуга и контурный СМАЙЛ
    (2, (0.50, 0.24, 0.92, 0.87), 'craft-echo.jpg', 1100),  # текст-эхо «СИНЕРГИЯ»
    (7, (0.52, 0.06, 0.96, 0.72), 'craft-neon.jpg', 1100),  # жёлтые цифры в неоне
]


def main():
    doc = fitz.open(SRC)
    print('обложка и задник:')
    save(render(doc[0], COVER_PX), 'cover.jpg', COVER_PX)
    save(render(doc[len(doc) - 1], COVER_PX), 'back.jpg', COVER_PX)

    print('развороты:')
    for i in range(1, len(doc) - 1):
        sp = render(doc[i], SPREAD_PX)
        save(sp, f'spread-{i:02d}.jpg', SPREAD_PX)
        # миниатюры для ленты под листалкой: иначе на 74 px грузились бы все
        # десять разворотов целиком
        save(sp, f'thumb-{i:02d}.jpg', 240, q=80)

    print('карта района:')
    pg, box, name, mw = MAP
    cut(render(doc[pg - 1], SPREAD_PX), box, name, mw)

    print('фотографии объекта:')
    hi = render(doc[PHOTO_PAGE - 1], HIRES)
    for box, name in PHOTOS:
        cut(hi, box, name, 900, q=84)

    print('приёмы:')
    for pg, box, name, mw in CRAFT:
        cut(render(doc[pg - 1], SPREAD_PX), box, name, mw)

    print('вордмарк:')
    shutil.copy(os.path.join(SMILE, 'logo-smile.png'),
                os.path.join(DST, 'logo-smile.png'))
    print('   logo-smile.png')

    print('готово →', DST)


if __name__ == '__main__':
    main()
