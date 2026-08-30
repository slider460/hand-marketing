#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Новый год Messe Düsseldorf» (/event/messeduessleldorf/).

Материал один: съёмка вечера, 15 кадров. Они лежали в галерее старой
тильдовской страницы (scripts/a2/gallery_map.json), исходники в
mirror/images/lib/**. Ни видео, ни макетов, ни брифа по кейсу нет.

Что делает:
  1. Шрифты Ubuntu + Scada локально (mirror/fonts/ubuntu-scada.css +
     files/*.woff2). Внешних CDN на сайте нет принципиально.
  2. Переносит 15 кадров в mirror/images/messe/ под говорящими именами,
     в двух размерах (полный + превью 640) и с .webp рядом.
  3. Снимает палитру знака Messe Düsseldorf прямо с фотозоны: маска по
     оранжево-красному, k-means на 4 центра — это те четыре тона, которыми
     набран знак и фирменная рамка меню.
  4. Считает «растр» кадров: кадр разбивается на модули знака, яркость
     каждого модуля квантуется по квантилям в 4 тона палитры. Матрицы
     уходят в scripts/a2/messe_map.json, страница выкладывает из них
     пиксельный узор и переворачивает плитки в фотографию.
  5. Кропы: фирменная рамка меню, знак на фотозоне.

Запуск: python3 scripts/messe-assets.py [--fonts] [--photos] [--raster]
Без флагов делает всё.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

import cv2
import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
LIB = os.path.join(MIRROR, 'images', 'lib')
IMG = os.path.join(MIRROR, 'images', 'messe')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
MAP = os.path.join(ROOT, 'scripts', 'a2', 'messe_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Ubuntu:wght@400;500;700'
      '&family=Scada:wght@400;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── 15 кадров съёмки: (слаг, каталог в images/lib, файл, что в кадре) ──────
# порядок — как шёл вечер: подготовка, сбор, официальная часть, номера, танцы
PHOTOS = [
    ('bufet', 'as6438-6562-4238-b832-653736643738', 'IMG_2915.jpg',
     'Фуршетная линия вдоль кирпичной стены: мармиты на подогреве, '
     'ассорти закусок, красный текстиль со стойкой до пола'),
    ('gifts', 'as3038-6139-4636-a130-313463393238', 'IMG_2925.jpg',
     'Подарки в крафт-пакетах выстроены на стойке ресепшена, '
     'по стойке пущена гирлянда из ватных шаров'),
    ('photozone', 'as6165-3064-4861-b563-353338666233', 'IMG_2955.jpg',
     'Фотозона: знак Messe Düsseldorf Moscow на стеклянной перегородке, '
     'по периметру пущена гирлянда'),
    ('menu', 'as3265-6334-4531-a366-336235626233', 'IMG_2995.jpg',
     'Сервировка: карточка меню в фирменной пиксельной рамке, '
     'салфетки конусом, бусы и ёлочный декор'),
    ('host', 'as3161-3231-4938-b935-343030353261', 'IMG_3045.jpg',
     'Официальная часть: ведущий у экрана, на проекции слайд конкурса, '
     'над головами зеркальный шар'),
    ('talk', 'as6236-3235-4230-b832-353835353564', 'IMG_3103.jpg',
     'Гости общаются в зоне у экрана'),
    ('sketch', 'as3461-6164-4163-b633-383362316561', 'IMG_3157.jpg',
     'Тихая зона: шаржист работает с гостями, за спиной рабочие столы '
     'и роллап компании'),
    ('portrait', 'as6635-3137-4362-a666-666262653833', 'IMG_3159.jpg',
     'Готовый шарж на память'),
    ('award', 'as3030-3365-4362-a238-343831336433', '2013-12-25_23-47-35_.JPG',
     'Вручение подарка: ведущий передаёт микрофон гостям'),
    ('cards', 'as6465-6532-4238-b730-323566383664', 'IMG_3240.jpg',
     'Фокусник работает с картами в кругу гостей'),
    ('fire', 'as6264-6439-4764-b132-663036353331', '2013-12-25_23-48-08_.JPG',
     'Фокус с огнём на столике посреди зала'),
    ('bar', 'as3732-6537-4962-a564-663931313233', '2013-12-25_23-48-41_.JPG',
     'Бар в кирпичной арке: линейка мохито, гирлянда-занавес на стене'),
    ('dance-red', 'as3431-6532-4731-a430-303536306364', '2013-12-25_23-47-17_.JPG',
     'Восточный танец с веерами-вейлами, красно-чёрный костюм'),
    ('dance-blue', 'as3765-3036-4134-b931-613937663033', 'IMG_3615.jpg',
     'Второй выход танцовщицы, бирюзовый костюм'),
    ('disco', 'as6665-6335-4634-b433-323562353633', 'IMG_3661.jpg',
     'Дискотека: галстук ослаблен, пиджаки сняты'),
]

# ─── что раскладываем в растр знака: (слаг, колонок по длинной стороне) ─────
RASTER = [('disco', 30),                                    # обложка
          ('bufet', 16), ('host', 16), ('bar', 16), ('sketch', 16),   # зоны
          ('photozone', 14),                                # разбор модуля
          ('menu', 16), ('gifts', 16), ('cards', 16), ('fire', 16),
          ('dance-blue', 14), ('dance-red', 14)]

SIGN_SRC = ('as6165-3064-4861-b563-353338666233', 'IMG_2955.jpg')  # фотозона


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(str(c) for c in cmd) + '\n' + r.stderr[-800:])


def fetch(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA})).read()


def webp(path):
    """Те же ключи, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def fonts():
    os.makedirs(FILES, exist_ok=True)
    css = fetch(GF).decode('utf-8')
    blocks = re.findall(r'/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    out, n = [], 0
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        wght = re.search(r'font-weight:\s*(\d+)', block).group(1)
        name = f'{fam.lower().replace(" ", "-")}-{wght}-{subset}.woff2'
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    head = ('/* Ubuntu + Scada, self-host для /event/messeduessleldorf/.\n'
            '   Сгенерировано scripts/messe-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'ubuntu-scada.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def photos():
    """Кадры под говорящими именами в трёх размерах: полный (лайтбокс),
    средний 1000 (обложка и разбор модуля) и превью 640 (карточки, галерея).
    На странице они отдаются через srcset, чтобы телефон не тянул большой."""
    os.makedirs(IMG, exist_ok=True)
    for slug, folder, fname, _what in PHOTOS:
        src = os.path.join(LIB, folder, fname)
        if not os.path.exists(src):
            sys.exit(f'✗ нет исходника: {src}')
        im = cv2.imread(src)
        big = os.path.join(IMG, f'{slug}.jpg')
        cv2.imwrite(big, im, [cv2.IMWRITE_JPEG_QUALITY, 88])
        webp(big)
        for suffix, side, q in (('-m', 1000, 86), ('-s', 640, 84)):
            k = side / max(im.shape[1], im.shape[0])
            dst = os.path.join(IMG, f'{slug}{suffix}.jpg')
            cv2.imwrite(dst, cv2.resize(im, None, fx=k, fy=k,
                                        interpolation=cv2.INTER_AREA),
                        [cv2.IMWRITE_JPEG_QUALITY, q])
            webp(dst)
    print(f'✓ кадры: {len(PHOTOS)} шт. × 3 размера в mirror/images/messe/')


def sign_palette():
    """Четыре тона знака, снятые с фотозоны.

    Знак набран квадратами четырёх оттенков одной оранжево-красной гаммы.
    Кластеризовать их в BGR бесполезно: гирлянда по периметру фотозоны даёт
    блики и тени, и k-means выделяет их, а не краску. Зато по тону (hue)
    четыре краски стоят четырьмя пиками — 2, 7, 12 и 18 — и достаточно взять
    медианный цвет в каждой полосе, отбросив ненасыщенное (блик и тень).
    """
    im = cv2.imread(os.path.join(LIB, *SIGN_SRC))
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    mask = (((h <= 22) | (h >= 172)) & (s > 195) & (v > 110)).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    # знак — крупная компонента в верхней половине кадра (внизу такой же
    # оранжевый паркет, по площади он больше, и его надо отсечь)
    cand = [i for i in range(1, n) if stats[i, cv2.CC_STAT_TOP] < im.shape[0] // 2]
    idx = max(cand, key=lambda i: stats[i, cv2.CC_STAT_AREA])
    sel = lab == idx
    hue = h[sel].astype(int)
    px = im[sel].astype(float)
    hexes = []
    for a, b in ((0, 4), (5, 9), (10, 14), (15, 22)):
        m = (hue >= a) & (hue <= b)
        if m.sum() < 200:
            sys.exit(f'✗ полоса hue {a}-{b} пустая — проверь маску знака')
        med = np.median(px[m], axis=0)
        hexes.append('#%02X%02X%02X' % (int(med[2]), int(med[1]), int(med[0])))
    print('✓ палитра знака:', ' '.join(hexes))
    return hexes, stats[idx, :4].tolist()


def raster_matrix(slug, cols):
    """Кадр → матрица индексов палитры. Яркость режется по квантилям, чтобы
    все четыре тона знака были заняты и в тёмных ночных кадрах тоже."""
    im = cv2.imread(os.path.join(IMG, f'{slug}.jpg'))
    hgt, wid = im.shape[:2]
    rows = int(round(cols * hgt / wid))
    small = cv2.resize(im, (cols, rows), interpolation=cv2.INTER_AREA)
    lum = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY).astype(np.float32)
    q = np.quantile(lum, [0.25, 0.5, 0.75])
    idx = np.digitize(lum, q)           # 0..3, тёмное → тёмный тон знака
    return rows, [''.join(str(int(v)) for v in row) for row in idx]


def raster():
    pal, box = sign_palette()
    data = {'palette': pal, 'signBox': box, 'grids': {},
            'photos': {s: w for s, _f, _n, w in PHOTOS}}
    for slug, cols in RASTER:
        rows, mat = raster_matrix(slug, cols)
        data['grids'][slug] = {'cols': cols, 'rows': rows, 'rowsData': mat}
    json.dump(data, open(MAP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'✓ растр: {len(RASTER)} кадров → scripts/a2/messe_map.json')


def crops():
    """Кропы: фирменная рамка меню и знак на фотозоне."""
    os.makedirs(IMG, exist_ok=True)
    im = cv2.imread(os.path.join(LIB, 'as3265-6334-4531-a366-336235626233', 'IMG_2995.jpg'))
    c = im[360:630, 180:470]
    c = cv2.resize(c, None, fx=2.2, fy=2.2, interpolation=cv2.INTER_LANCZOS4)
    dst = os.path.join(IMG, 'menu-card.jpg')
    cv2.imwrite(dst, c, [cv2.IMWRITE_JPEG_QUALITY, 90]); webp(dst)

    im = cv2.imread(os.path.join(LIB, *SIGN_SRC))
    # только пиктограмма: по маске она занимает строки 288..535, словесная
    # часть знака ниже, и в кроп её не берём (обрезалась бы по строке)
    c = im[274:546, 190:730]
    c = cv2.resize(c, None, fx=1.8, fy=1.8, interpolation=cv2.INTER_LANCZOS4)
    dst = os.path.join(IMG, 'sign.jpg')
    cv2.imwrite(dst, c, [cv2.IMWRITE_JPEG_QUALITY, 90]); webp(dst)
    print('✓ кропы: menu-card.jpg, sign.jpg')


if __name__ == '__main__':
    args = set(sys.argv[1:])
    todo = args & {'--fonts', '--photos', '--raster', '--crops'} or \
        {'--fonts', '--photos', '--raster', '--crops'}
    os.makedirs(IMG, exist_ok=True)
    if '--fonts' in todo:
        fonts()
    if '--photos' in todo:
        photos()
    if '--crops' in todo:
        crops()
    if '--raster' in todo:
        raster()
