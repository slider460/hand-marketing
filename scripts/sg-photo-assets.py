#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Предметная съёмка продукции Gyproc для Saint-Gobain»
(/photo/saint-gobain).

Первоисточник один: сдаточная папка Saint_Gobain_foto_231124 — 62 файла PNG
5760×3240 с альфа-каналом (фон вырезан) плюс два кадра бекстейджа с площадки.
Съёмка 23–24.11.2023, один съёмочный день. Ничего не дорисовано и не взято
из интернета: всё, что страница утверждает про съёмку, посчитано здесь.

Что делает скрипт:

  --fonts   Exo 2 + Spectral локально (mirror/fonts/files + exo2-spectral.css).
            Внешних CDN на сайте нет принципиально.
  --items   для каждого кадра: полный кадр 16:9 с прозрачностью (для механики
            квадрата и подложек) и тесный кроп по силуэту (для каталога).
  --back    два кадра бекстейджа.
  --map     метрики в scripts/a2/sgphoto_map.json:
              bbox   — габарит силуэта в долях кадра;
              holes  — число сквозных отверстий, вырезанных вместе с контуром
                       (связные прозрачные области внутри силуэта, полное
                       разрешение, порог 40 px — мельче уже шум кромки);
              square — влезает ли предмет в квадрат 3240×3240 и куда этот
                       квадрат надо поставить (доля ширины кадра).

Запуск: python3 scripts/sg-photo-assets.py [--fonts] [--items] [--back] [--map]
Без аргументов — всё сразу.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
SRC = '/Users/aleksandrnarodetskii/Downloads/Saint_Gobain_foto_231124'
IMG = os.path.join(MIRROR, 'images', 'sgphoto')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
MAP = os.path.join(ROOT, 'scripts', 'a2', 'sgphoto_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Exo+2:wght@300..800'
      '&family=Spectral:wght@300;400;600&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

FRAME_W = 1440      # полный кадр 16:9 для механик
ITEM_W = 900        # тесный кроп по силуэту для каталога
BACK_W = 1600

# ─── товарные группы ────────────────────────────────────────────────────────
# Порядок групп = порядок списка в брифе клиента: сначала подвесы, потом
# соединители, удлинители, ленты, крепёж, профили, в конце собранные системы.
# Названия — из брифа, ничего не додумано.
GROUPS = [
    ('podves-pryamoy', 'Подвес прямой', 'подвесы',
     [2136, 2138, 2140]),
    ('podves-ankernyy', 'Подвес анкерный с тягой', 'подвесы',
     [2127, 2129, 2132, 2134, 2150]),
    ('podves-akust', 'Подвес акустический и Акустик Про', 'подвесы',
     [2183, 2186, 2192, 2194, 2196]),
    ('krab', 'Соединитель «краб»', 'соединители',
     [2103, 2105]),
    ('soed-2ur', 'Соединитель двухуровневый', 'соединители',
     [2114, 2118, 2119]),
    ('udlinitel', 'Удлинитель профиля', 'соединители',
     [2121, 2125]),
    ('lenta-marko', 'Лента Гипрок Марко ПРО', 'ленты',
     [2198, 2211]),
    ('lenta-poriz', 'Лента поризованная 30 / 50 / 70 / 95 мм', 'ленты',
     [2217, 2220, 2224, 2227]),
    ('krepezh', 'Крепёж: саморезы и дюбели', 'крепёж',
     [2245]),
    # профили сведены по видимой геометрии, а не по артикулам: в брифе на
    # линейки Стандарт и Ультра просили по 4–8 кадров, сдано 14
    ('profil', 'Профиль: полка и стенка', 'профили',
     [2268, 2271, 2277, 2281, 2284, 2303, 2308, 2311, 2315, 2317, 2322]),
    ('profil-prorezi', 'Профиль с прорезями', 'профили',
     [2295, 2298, 2300]),
    ('sistema-peregorodka', 'Система: перегородка', 'системы',
     [2290, 2293, 2325, 2326]),
    ('sistema-potolok', 'Система: подвесной потолок', 'системы',
     [2328, 2330, 2332, 2335, 2336, 2340, 2342, 2345, 2353, 2370, 2373,
      2378, 2390, 2396, 2399, 2400, 2401]),
]

BACKSTAGE = [
    ('setup', '10FB676E-B9E7-41AD-A280-508C4FD82EA6.JPG',
     'Сборка системы в кадре: специалист Saint-Gobain собирает каркас прямо '
     'на съёмочном столе'),
    ('crew', 'e08fca44-364a-443c-841c-e26bc2b1efb7.JPG',
     'Площадка: камера на штативе, два прибора на стойках, журавль с '
     'верхним светом, белый фон-подложка'),
]


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(str(c) for c in cmd) + '\n' + r.stderr[-800:])


def fetch(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA})).read()


def src_path(num):
    return os.path.join(SRC, f'IMG_{num}.png')


# ─── шрифты ─────────────────────────────────────────────────────────────────
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
    head = ('/* Exo 2 + Spectral, self-host для /photo и /photo/saint-gobain.\n'
            '   Сгенерировано scripts/sg-photo-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'exo2-spectral.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


# ─── картинки ───────────────────────────────────────────────────────────────
def save_webp(im, path, quality=82):
    """WebP с альфой. PNG-двойника не кладём: файлы с прозрачностью в PNG
    весят вчетверо больше, а WebP с альфой держат все живые браузеры."""
    im.save(path, 'WEBP', quality=quality, method=6, exact=False)


def items():
    os.makedirs(IMG, exist_ok=True)
    total = 0
    for slug, _title, _sect, nums in GROUPS:
        for num in nums:
            im = Image.open(src_path(num)).convert('RGBA')
            # полный кадр: как сдан, с родной компоновкой — на нём работают
            # механика квадрата и переключатель подложки
            fr = im.resize((FRAME_W, FRAME_W * im.height // im.width), Image.LANCZOS)
            save_webp(fr, os.path.join(IMG, f'frame-{num}.webp'))
            # тесный кроп по силуэту с полем 3 % — для плиток каталога
            bb = im.getchannel('A').getbbox()
            pad = int(0.03 * max(bb[2] - bb[0], bb[3] - bb[1]))
            box = (max(0, bb[0] - pad), max(0, bb[1] - pad),
                   min(im.width, bb[2] + pad), min(im.height, bb[3] + pad))
            cr = im.crop(box)
            k = ITEM_W / max(cr.width, cr.height)
            cr = cr.resize((max(1, round(cr.width * k)), max(1, round(cr.height * k))),
                           Image.LANCZOS)
            save_webp(cr, os.path.join(IMG, f'item-{num}.webp'))
            total += 1
    print(f'✓ кадры: {total} × 2 файла в {os.path.relpath(IMG, ROOT)}')


def back():
    os.makedirs(IMG, exist_ok=True)
    for slug, fn, _cap in BACKSTAGE:
        im = Image.open(os.path.join(SRC, fn)).convert('RGB')
        im = im.resize((BACK_W, round(BACK_W * im.height / im.width)), Image.LANCZOS)
        p = os.path.join(IMG, f'backstage-{slug}.jpg')
        im.save(p, 'JPEG', quality=86, optimize=True, progressive=True)
        sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
            '-metadata', 'none', p, '-o', p + '.webp'])
    print(f'✓ бекстейдж: {len(BACKSTAGE)} кадра')


# ─── метрики ────────────────────────────────────────────────────────────────
def holes(alpha):
    """Сквозные отверстия: прозрачные связные области, НЕ касающиеся края
    кадра, площадью от 40 px. Считаются на полном разрешении."""
    bg = alpha < 8
    lab, n = ndimage.label(bg)
    if n == 0:
        return 0
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    sizes = ndimage.sum(bg, lab, range(1, n + 1))
    return int(sum(1 for i in range(n) if (i + 1) not in edge and sizes[i] >= 40))


def build_map():
    out = {'source': os.path.basename(SRC), 'shot': '2023-11-23', 'groups': []}
    total_holes = 0
    fit_any = 0
    for slug, title, sect, nums in GROUPS:
        g = {'slug': slug, 'title': title, 'section': sect, 'shots': []}
        for num in nums:
            im = Image.open(src_path(num))
            a = np.array(im.getchannel('A'))
            H, W = a.shape
            ys, xs = np.nonzero(a > 8)
            x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
            sw, sh_ = x1 - x0 + 1, y1 - y0 + 1
            h = holes(a)
            total_holes += h
            # квадрат стороной в высоту кадра: влезает ли предмет целиком и
            # куда квадрат ставить, чтобы предмет оказался по центру
            S = H
            fits = sw <= S and sh_ <= S
            fit_any += fits
            cx = (x0 + x1) / 2
            left = min(max(cx - S / 2, 0), W - S)
            g['shots'].append({
                'id': num,
                'bbox': [round(x0 / W, 4), round(y0 / H, 4),
                         round((x1 + 1) / W, 4), round((y1 + 1) / H, 4)],
                'ar': round(sw / sh_, 3),
                'holes': h,
                'fits': bool(fits),
                'sq': round(left / W, 4),       # левый край квадрата, доля ширины
                'sqw': round(S / W, 4),         # ширина квадрата, доля ширины
            })
        out['groups'].append(g)
    shots = sum(len(g['shots']) for g in out['groups'])
    out['stats'] = {
        'shots': shots,
        'holes': total_holes,
        'fits': fit_any,
        'frame_range': [min(n for *_, nums in GROUPS for n in nums),
                        max(n for *_, nums in GROUPS for n in nums)],
    }
    json.dump(out, open(MAP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'✓ карта: {shots} кадров, отверстий {total_holes}, '
          f'в квадрат целиком {fit_any}')


if __name__ == '__main__':
    args = set(sys.argv[1:])
    todo = args & {'--fonts', '--items', '--back', '--map'} or \
        {'--fonts', '--items', '--back', '--map'}
    if '--fonts' in todo:
        fonts()
    if '--items' in todo:
        items()
    if '--back' in todo:
        back()
    if '--map' in todo:
        build_map()
