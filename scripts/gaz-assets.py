#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Газель-трансформер» (/video/gaz/).

Готовит три вещи:

1. Шрифты Tektur + Rubik, self-host (mirror/fonts/tektur-rubik.css +
   mirror/fonts/files/). Внешних CDN в проекте нет принципиально.
2. Кадры из самого ролика media/gazelle-transformer.mp4 (1280x720, 1:42):
   пара «пробка / робот» для героя, одиннадцать кадров раскадровки,
   постер плеера и два кадра для сопоставления со съёмочными фото.
3. Две фотографии со съёмки из общего каталога ассетов: оператор с краном
   у опоры ЛЭП и актёр в кабине ГАЗели. Опора на фото — та самая, мимо
   которой в ролике шагает робот, поэтому кадры идут парами.

Запуск: python3 scripts/gaz-assets.py [--fonts] [--frames]
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
OUT = os.path.join(MIRROR, 'images', 'gaz')
FILM = os.path.join(ROOT, 'media', 'gazelle-transformer.mp4')
ASSETS = os.path.join(ROOT, 'public', 'assets')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Tektur:wght@400..900'
      '&family=Rubik:wght@300..700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ролик снят широким кадром и лежит в файле 1280x720 с чёрными полосами
# (cropdetect даёт 1280:528:0:96). Все кадры режем по живой картинке, иначе
# полосы вылезают в вёрстке как чёрные поля.
CROP = 'crop=1280:528:0:96'

# кадры из ролика: (секунда, имя файла, ширина)
SHOTS = [
    # герой: одна и та же грязная колея вдоль пробки — до и после кнопки
    (1.5,  'hero-jam.jpg',   1600),
    (57.0, 'hero-robot.jpg', 1600),
    # раскадровка, 11 бит
    (1.5,  'sb-01.jpg',  760),
    (6.0,  'sb-02.jpg',  760),
    (9.5,  'sb-03.jpg',  760),
    (16.0, 'sb-04.jpg',  760),
    (20.5, 'sb-05.jpg',  760),
    (27.0, 'sb-06.jpg',  760),
    (33.0, 'sb-07.jpg',  760),
    (40.0, 'sb-08.jpg',  760),
    (44.0, 'sb-09.jpg',  760),
    (79.0, 'sb-10.jpg',  760),
    (93.5, 'sb-11.jpg',  760),
    # кадры под съёмочные фотографии
    (56.0, 'shot-pylon.jpg',   1000),  # робот у опоры ЛЭП
    (16.0, 'shot-driver.jpg',  1000),  # водитель в кабине
]

# постер плеера — единственный кадр БЕЗ обрезки полос: он лежит в окне 16:9
# вместе с самим файлом и должен совпасть с первым кадром воспроизведения
POSTER = (40.0, 'poster.jpg', 1280)

# фотографии со съёмки: (файл в public/assets, имя, ширина)
PHOTOS = [
    ('d5629cae_IMG_0201.jpg', 'shoot-crew.jpg', 1000),  # оператор с краном у опоры
    ('e4473617_IMG_0286.jpg', 'shoot-cab.jpg',  1000),  # актёр в кабине ГАЗели
]

# карточка для соцсетей: робот в кадре, 1200x630
OG = (57.0, 'og.jpg')


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(map(str, cmd)) + '\n' + r.stderr[-800:])


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
        wght = re.search(r'font-weight:\s*([\d ]+);', block).group(1).replace(' ', '-')
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        name = f"{fam.lower().replace(' ', '-')}-{wght}-{subset}.woff2"
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    if not out:
        sys.exit('✗ Google Fonts не отдал ни одного @font-face — проверь GF')
    head = ('/* Tektur + Rubik, self-host для /video/gaz/.\n'
            '   Сгенерировано scripts/gaz-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'tektur-rubik.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def webp(path):
    """Те же ключи, что и в scripts/gen-webp.sh."""
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv', path, '-o', path + '.webp'])


def frames():
    if not os.path.exists(FILM):
        sys.exit(f'✗ нет ролика: {FILM}')
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for sec, name, width in SHOTS:
        dst = os.path.join(OUT, name)
        # -ss до -i: быстрый поиск по ключевым кадрам, точности до кадра тут не нужно
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(sec), '-i', FILM,
            '-frames:v', '1', '-vf', f'{CROP},scale={width}:-2:flags=lanczos', '-q:v', '3', dst])
        webp(dst)
        n += 1
    for src, name, width in PHOTOS:
        s = os.path.join(ASSETS, src)
        if not os.path.exists(s):
            sys.exit(f'✗ нет фото со съёмки: {s}')
        dst = os.path.join(OUT, name)
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', s,
            '-vf', f'scale={width}:-2:flags=lanczos', '-q:v', '3', dst])
        webp(dst)
        n += 1
    sec, name, width = POSTER
    dst = os.path.join(OUT, name)
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(sec), '-i', FILM, '-frames:v', '1',
        '-vf', f'scale={width}:-2:flags=lanczos', '-q:v', '3', dst])
    webp(dst)
    n += 1
    sec, name = OG
    dst = os.path.join(OUT, name)
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(sec), '-i', FILM, '-frames:v', '1',
        '-vf', f'{CROP},scale=1200:630:force_original_aspect_ratio=increase:flags=lanczos,'
               'crop=1200:630', '-q:v', '3', dst])
    webp(dst)
    n += 1
    print(f'✓ кадры: {n} шт. в mirror/images/gaz/')


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--frames' in args:
        frames()
