#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Газель-трансформер» (/video/gaz/).

Готовит четыре вещи:

1. Шрифты Tektur + Rubik, self-host (mirror/fonts/tektur-rubik.css +
   mirror/fonts/files/). Внешних CDN в проекте нет принципиально.
2. Кадры из самого ролика media/gazelle-transformer.mp4 (1280x720, 1:42):
   пара «пробка / робот» для героя, кадры под каждый лист сториборда,
   постер плеера и два кадра для сопоставления со съёмочными фото.
3. Сториборд и фотографии локации из презентации проекта
   «eaton gaz.pptx»: 31 карандашный лист (30 кадров сюжета + пэкшот) и
   два снимка размытой параллельной дороги со скаутинга. Презентация
   лежит вне репозитория, путь задаётся GAZ_PPTX (по умолчанию
   ~/Downloads/eaton gaz.pptx); если её нет, шаг пропускается —
   готовые картинки уже лежат в mirror/images/gaz/.
4. Две фотографии со съёмки из общего каталога ассетов: оператор с краном
   у опоры ЛЭП и актёр в кабине ГАЗели. Опора на фото — та самая, мимо
   которой в ролике шагает робот, поэтому кадры идут парами.

Запуск: python3 scripts/gaz-assets.py [--fonts] [--frames] [--deck]
        (без ключей — всё сразу)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
MIRROR = os.path.join(ROOT, 'mirror')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
OUT = os.path.join(MIRROR, 'images', 'gaz')
FILM = os.path.join(ROOT, 'media', 'gazelle-transformer.mp4')
ASSETS = os.path.join(ROOT, 'public', 'assets')
SB_OUT = os.path.join(OUT, 'sb')
PPTX = os.environ.get('GAZ_PPTX',
                      os.path.expanduser('~/Downloads/eaton gaz.pptx'))

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Tektur:wght@400..900'
      '&family=Rubik:wght@300..700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ролик снят широким кадром и лежит в файле 1280x720 с чёрными полосами
# (cropdetect даёт 1280:528:0:96). Все кадры режем по живой картинке, иначе
# полосы вылезают в вёрстке как чёрные поля.
CROP = 'crop=1280:528:0:96'

# Пары «лист сториборда → секунда в ролике». Номер = номер листа (1..31).
# Без пары остаётся единственный лист 20 (крупный план механики робота):
# в готовый ролик он не вошёл. На странице такой лист остаётся рисунком.
PAIRS = {
    1: 1.5, 2: 6.0, 3: 9.5, 4: 11.0, 5: 12.0, 6: 16.0, 7: 20.5,
    8: 23.5, 9: 13.5, 10: 24.0,
    11: 27.0, 12: 26.0, 13: 29.0, 14: 30.0, 15: 30.5, 16: 33.0, 17: 36.0,
    18: 40.0, 19: 44.0, 21: 57.0, 22: 50.0, 23: 48.0, 24: 58.0, 25: 67.5,
    26: 72.0, 27: 79.0, 28: 74.0, 29: 89.0, 30: 93.5, 31: 97.0,
}

# кадры из ролика: (секунда, имя файла, ширина)
SHOTS = [
    # герой: одна и та же грязная колея вдоль пробки — до и после кнопки
    (1.5,  'hero-jam.jpg',   1600),
    (57.0, 'hero-robot.jpg', 1600),
    # кадры под съёмочные фотографии
    (56.0, 'shot-pylon.jpg',   1000),  # робот у опоры ЛЭП
    (16.0, 'shot-driver.jpg',  1000),  # водитель в кабине
] + [(sec, 'f-%02d.jpg' % n, 760) for n, sec in sorted(PAIRS.items())]

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


def deck():
    """Сториборд и фото локации из презентации проекта.

    Внутри pptx листы сториборда лежат как image10…image40 (230x141,
    карандаш с оранжевыми стрелками), фотографии локации — image42 и
    image43. Порядок файлов внутри архива совпадает с порядком кадров
    на слайдах 7-8, поэтому сортировки по номеру достаточно.
    """
    if not os.path.exists(PPTX):
        print(f'· презентации нет ({PPTX}) — сториборд пропущен, '
              'готовые картинки уже в mirror/images/gaz/sb/')
        return
    os.makedirs(SB_OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='gaz-deck-')
    try:
        with zipfile.ZipFile(PPTX) as z:
            names = [n for n in z.namelist() if n.startswith('ppt/media/')]
            for n in names:
                z.extract(n, tmp)
        media = os.path.join(tmp, 'ppt', 'media')

        def num(name):
            return int(re.search(r'(\d+)', name).group(1))

        sheets = sorted((f for f in os.listdir(media)
                         if f.endswith('.png') and num(f) >= 10), key=num)
        if len(sheets) != 31:
            sys.exit(f'✗ ожидал 31 лист сториборда, нашёл {len(sheets)}')
        n = 0
        for i, f in enumerate(sheets, 1):
            dst = os.path.join(SB_OUT, '%02d.jpg' % i)
            # исходники маленькие (230 px), тянем до 440: карандашный штрих
            # апскейл переносит спокойно, а на retina иначе каша
            sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(media, f),
                '-vf', 'scale=440:-2:flags=lanczos,format=yuv420p', '-q:v', '3', dst])
            webp(dst)
            n += 1
        for src, name in (('image42.jpeg', 'loc-1.jpg'), ('image43.jpeg', 'loc-2.jpg')):
            s = os.path.join(media, src)
            if not os.path.exists(s):
                sys.exit(f'✗ нет фотографии локации {src} в презентации')
            dst = os.path.join(OUT, name)
            sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', s,
                '-vf', 'scale=800:-2:flags=lanczos', '-q:v', '3', dst])
            webp(dst)
            n += 1
        print(f'✓ презентация: {n} картинок (31 лист сториборда + 2 фото локации)')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--frames' in args:
        frames()
    if do_all or '--deck' in args:
        deck()
