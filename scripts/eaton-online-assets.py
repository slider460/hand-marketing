#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «ONLINE трансляция EATON» (/eaton_online).

Готовит две вещи:

1. Шрифты IBM Plex Sans + IBM Plex Mono, self-host
   (mirror/fonts/plex.css + mirror/fonts/files/). Внешних CDN в проекте нет.
2. Кадры в mirror/images/eaton-online/: исходников всего четыре штуки
   (две фотографии смены в офисе Eaton, 3D-визуал зала форума IT-ОСЬ 2020
   и скрин виртуального стенда Eaton), из них нарезаются окна мультивью
   в 16:9 под режиссёрский монитор на странице.

Запуск: python3 scripts/eaton-online-assets.py [--fonts] [--frames]
        (без ключей — всё сразу)
"""
import os
import re
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
MIRROR = os.path.join(ROOT, 'mirror')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
OUT = os.path.join(MIRROR, 'images', 'eaton-online')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600'
      '&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

CA = os.path.join(MIRROR, 'case-assets')
LIB = os.path.join(MIRROR, 'images', 'lib')

# исходники: (имя источника, путь)
SRC = {
    'desk':  os.path.join(CA, '10a4474e_photo_2021-03-06_22-.jpg'),   # 1280x720, аппаратная у брендволла
    'rack':  os.path.join(CA, 'c1284dcc_image.jpeg'),                 # 1280x960, пульт, микшер, камеры
    'hall':  os.path.join(CA, 'a1acfaea_image_2021-03-06_22-.png'),   # 794x571, 3D-зал форума
    'stand': os.path.join(LIB, 'as6532-3166-4836-a266-643265393861', 'noroot.png'),  # 1280x539, стенд Eaton
}

# кадры целиком: (имя источника, имя файла, ширина по длинной стороне)
FULL = [
    ('desk',  'shift-desk.jpg',  1280),
    ('rack',  'shift-rack.jpg',  1280),
    ('hall',  'forum-hall.jpg',   794),
    ('stand', 'forum-stand.jpg', 1280),
]

# окна мультивью, все 16:9: (источник, имя файла, crop w:h:x:y)
CROPS = [
    ('desk',  'cam1.jpg',  'crop=672:378:196:206'),   # спикеры у брендволла Eaton
    ('rack',  'cam2.jpg',  'crop=816:459:150:430'),   # микшер и ноутбук с vMix
    ('rack',  'cam3.jpg',  'crop=608:342:352:60'),    # две камеры на штативах и свет
    ('stand', 'slide.jpg', 'crop=364:205:428:166'),   # экран презентации на стенде
]
CROP_W = 960   # окна мультивью показываются мелко, 960 по ширине хватает с запасом


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(cmd) + '\n' + r.stderr[-800:])


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req).read()


def fonts():
    os.makedirs(FILES, exist_ok=True)
    css = fetch(GF).decode('utf-8')
    blocks = re.findall(r'/\*\s*([a-z\-\[\]0-9]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    out, n = [], 0
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        wght = re.search(r'font-weight:\s*(\d+)', block).group(1)
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        name = f"{fam.lower().replace(' ', '-')}-{wght}-{subset}.woff2"
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    head = ('/* IBM Plex Sans + IBM Plex Mono, self-host для /eaton_online/.\n'
            '   Сгенерировано scripts/eaton-online-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'plex.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def webp(path):
    """Те же ключи, что и в scripts/gen-webp.sh."""
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv', path, '-o', path + '.webp'])


def frames():
    os.makedirs(OUT, exist_ok=True)
    for key, path in SRC.items():
        if not os.path.exists(path):
            sys.exit(f'✗ нет исходника {key}: {path}')
    n = 0
    for key, name, width in FULL:
        dst = os.path.join(OUT, name)
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', SRC[key],
            '-vf', f'scale={width}:-2:flags=lanczos', '-q:v', '3', dst])
        webp(dst)
        n += 1
    for key, name, crop in CROPS:
        dst = os.path.join(OUT, name)
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', SRC[key],
            '-vf', f'{crop},scale={CROP_W}:-2:flags=lanczos', '-q:v', '3', dst])
        webp(dst)
        n += 1
    print(f'✓ кадры: {n} шт. в mirror/images/eaton-online/')


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--frames' in args:
        frames()
