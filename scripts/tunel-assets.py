#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Дезинфекционный тоннель и лицевые экраны AnVIT»
(/creative/tunel/).

Материал по кейсу — четыре картинки со старой тильдовской страницы
(scripts/a2/gallery_map.json → mirror/images/lib/**):
  • фото тоннеля AnVIT S12T на площадке;
  • фото лицевого экрана с печатью TELE2;
  • фото экрана на человеке;
  • векторный знак «стоп-вирус» с панели тоннеля (на страницу не идёт,
    с него снимается палитра).
Ни чертежей, ни съёмки сборки, ни видео работы нет — всё, что страница
показывает сверх этих кадров, она считает и рисует сама.

Что делает:
  1. Шрифты Bitter + Ysabeau Office + PT Mono локально
     (mirror/fonts/bitter-ysabeau.css + files/*.woff2). Внешних CDN
     на сайте нет принципиально.
  2. Кладёт четыре кадра в mirror/images/tunel/ в двух размерах и с webp.
  3. Оголовье экрана: вырезает накладку и СНИМАЕТ С НЕЁ ПЕЧАТЬ —
     белые литеры TELE2 находятся по яркости и закрашиваются inpaint'ом
     по окружающему пластику. Чистая накладка нужна конструктору
     персонализации на странице: туда встаёт произвольный текст.
  4. Меряет по фото каркас: светлые алюминиевые стойки берутся как пики
     яркости по столбцам, ригель — как самый резкий перепад по строкам.
     Отсюда честное «три пролёта × два ряда = шесть панелей на сторону».
  5. Снимает палитру: красный и синий с векторного знака, серый профиля
     и асфальт — с фото площадки.
  6. Пишет scripts/a2/tunel_map.json.

Запуск: python3 scripts/tunel-assets.py [--fonts] [--photos] [--band] [--map]
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
IMG = os.path.join(MIRROR, 'images', 'tunel')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
MAP = os.path.join(ROOT, 'scripts', 'a2', 'tunel_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Bitter:wght@400;600;700;800'
      '&family=Ysabeau+Office:wght@300;400;500;600;700'
      '&family=PT+Mono&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── исходники: (слаг, каталог в images/lib, файл, что в кадре) ─────────────
PHOTOS = [
    ('tunnel', 'as3961-6639-4231-b835-643763666530', '_-03.png',
     'Тоннель AnVIT S12T на площадке: печатные панели, алюминиевый каркас, '
     'ПВХ-шторка на входе, надстройка с маркой над проёмом'),
    ('shield', 'as6432-3932-4137-b331-346465616161', '_-02.png',
     'Лицевой экран: ПЭТ 4 мм, чёрная накладка оголовья с печатью TELE2'),
    ('worn', 'as6439-3162-4263-a430-313934343139', '_-01.png',
     'Экран на человеке: поле обзора не перекрыто, стекло не запотевает'),
]
BADGE = ('as3934-3332-4163-a262-336137313161', '__-49.png')

BAND = (80, 230, 80, 600)          # накладка оголовья в кадре экрана 809×607
LOGO = (140, 200, 440, 545)        # печать TELE2 внутри того же кадра


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


def src(folder, fname):
    p = os.path.join(LIB, folder, fname)
    if not os.path.exists(p):
        sys.exit(f'✗ нет исходника: {p}')
    return p


def fonts():
    """Bitter (слэб — голос приборной таблички и санитарной инструкции),
    Ysabeau Office (канцелярский гротеск бланка) и PT Mono под телеметрию."""
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
    head = ('/* Bitter + Ysabeau Office + PT Mono, self-host для /creative/tunel/.\n'
            '   Сгенерировано scripts/tunel-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'bitter-ysabeau.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def save(im, slug, sizes=((1200, 88), (640, 84))):
    """Кадр в двух размерах + webp рядом: телефон не должен тянуть большой."""
    big = os.path.join(IMG, f'{slug}.jpg')
    cv2.imwrite(big, im, [cv2.IMWRITE_JPEG_QUALITY, 90])
    webp(big)
    for side, q in sizes:
        if max(im.shape[:2]) <= side:
            continue
        k = side / max(im.shape[1], im.shape[0])
        dst = os.path.join(IMG, f'{slug}-{side}.jpg')
        cv2.imwrite(dst, cv2.resize(im, None, fx=k, fy=k,
                                    interpolation=cv2.INTER_AREA),
                    [cv2.IMWRITE_JPEG_QUALITY, q])
        webp(dst)


def photos():
    os.makedirs(IMG, exist_ok=True)
    for slug, folder, fname, _what in PHOTOS:
        save(cv2.imread(src(folder, fname)), slug)
    print(f'✓ кадры: {len(PHOTOS)} шт. × 2 размера в mirror/images/tunel/')


def band():
    """Накладка оголовья без печати.

    Персонализация по кейсу делалась именно на верхней накладке, и страница
    даёт её потрогать: в конструктор встаёт произвольный текст. Чтобы под
    ним не просвечивал чужой логотип, печать снимается: в окне логотипа
    белые литеры отделяются от чёрного пластика порогом Оцу, маска
    расширяется на кайму и закрашивается inpaint'ом по соседнему пластику.
    Блики от ламп при этом остаются — они часть предмета, а не печати.
    """
    os.makedirs(IMG, exist_ok=True)
    im = cv2.imread(src(*PHOTOS[1][1:3]))
    y0, y1, x0, x1 = BAND
    ly0, ly1, lx0, lx1 = LOGO

    mask = np.zeros(im.shape[:2], np.uint8)
    win = cv2.cvtColor(im[ly0:ly1, lx0:lx1], cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(win, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask[ly0:ly1, lx0:lx1] = th
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
    clean = cv2.inpaint(im, mask, 7, cv2.INPAINT_TELEA)

    save(im[y0:y1, x0:x1], 'band', sizes=((640, 86),))
    save(clean[y0:y1, x0:x1], 'band-clean', sizes=((640, 86),))
    px = int(mask[ly0:ly1, lx0:lx1].sum() // 255)
    print(f'✓ накладка: печать снята, закрашено {px} px')
    return {'w': x1 - x0, 'h': y1 - y0,
            'logo': [round((lx0 - x0) / (x1 - x0), 4),
                     round((ly0 - y0) / (y1 - y0), 4),
                     round((lx1 - lx0) / (x1 - x0), 4),
                     round((ly1 - ly0) / (y1 - y0), 4)]}


def frame():
    """Каркас по фото.

    Стойки ищем на нижнем ряду панелей: там печать тёмно-синяя, а профиль
    анодированный, и он вдвое-втрое светлее фона — хватает пика яркости
    по столбцу с порогом по абсолютной величине (иначе в кандидаты лезут
    блики на печати). Ригель — самая светлая строка в окне, где по кадру
    проходит горизонтальный профиль; он уходит вверх слева направо, потому
    что дальний торец тоннеля дальше от камеры.

    Отсюда честное «три пролёта × два ряда = шесть панелей на сторону»,
    которое страница называет вслух.
    """
    g = cv2.cvtColor(cv2.imread(src(*PHOTOS[0][1:3])), cv2.COLOR_BGR2GRAY).astype(float)
    col = g[440:660, 170:770].mean(axis=0)
    posts, last = [], -99
    for i in range(3, len(col) - 3):
        if (col[i] > col[i - 3] + 8 and col[i] > col[i + 3] + 8
                and col[i] > 110 and i - last > 20):
            posts.append(i + 170)
            last = i
    rails = []
    for x0, x1 in ((210, 390), (440, 570), (630, 730)):
        rails.append(int(np.argmax(g[370:430, x0:x1].mean(axis=1))) + 370)
    return {'posts': posts, 'bays': len(posts) - 1,
            'rails': rails, 'rows': 2,
            'panels_per_side': (len(posts) - 1) * 2}


def palette():
    """Красный и синий — с векторного знака (там краска чистая, без съёмочного
    света), серый профиля и асфальт — с фото площадки."""
    def med(im, x, y, w, h):
        p = im[y:y + h, x:x + w].reshape(-1, im.shape[2])[:, :3]
        b, g_, r = np.median(p, axis=0)
        return '#%02X%02X%02X' % (int(round(r)), int(round(g_)), int(round(b)))
    badge = cv2.imread(src(*BADGE), cv2.IMREAD_UNCHANGED)
    tun = cv2.imread(src(*PHOTOS[0][1:3]))
    return {'red': med(badge, 1100, 400, 60, 60),
            'navy': med(badge, 950, 1480, 60, 20),
            'panel': med(tun, 300, 430, 60, 60),
            'alu': med(tun, 405, 300, 6, 120),
            'paper': med(tun, 300, 180, 60, 60),
            'asphalt': med(tun, 760, 700, 40, 40)}


def main():
    args = sys.argv[1:]
    todo = set(a.lstrip('-') for a in args) or {'fonts', 'photos', 'band', 'map'}
    if 'fonts' in todo:
        fonts()
    if 'photos' in todo:
        photos()
    b = band() if ('band' in todo or 'map' in todo) else None
    if 'map' in todo:
        data = {'palette': palette(), 'frame': frame(), 'band': b,
                'what': {s: w for s, _f, _n, w in PHOTOS}}
        json.dump(data, open(MAP, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('✓ карта:', MAP)
        print('  палитра:', data['palette'])
        print('  каркас :', data['frame'])


if __name__ == '__main__':
    main()
