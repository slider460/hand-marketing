#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Презентация МФК „Саларис“ арендаторам» (/event/salaris/).

Что делает:
  1. Шрифты Nunito + Wix Madefor Text из Google Fonts кладёт локально
     (mirror/fonts/files/ + mirror/fonts/nunito-madefor.css). Внешних CDN на
     сайте нет принципиально, поэтому качаем сами. Nunito выбран за скруглённые
     окончания: они повторяют начертание слова «саларис» в знаке клиента.
  2. Переносит фотоотчёт вечера из общего каталога mirror/images/lib/**
     в mirror/images/salaris/ с осмысленными именами. Оригиналы 1680 px,
     на странице столько не нужно, поэтому режем по назначению кадра.
     Пути взяты из scripts/a2/gallery_map.json (там они указывают на
     /static/cdn/, а лежат файлы на деле в /images/lib/ — учтено).
  3. Режет кадры из аftermovie media/salaris-event-fin180416.mp4: титр с датой
     и слайды презентации, которых в фотоотчёте нет.
  4. Делает .webp рядом с каждым jpg (хостинг отдаёт webp, если файл есть).

Запуск: python3 scripts/salaris-assets.py [--fonts] [--photos] [--frames]
Без флагов делает всё.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
IMG = os.path.join(MIRROR, 'images', 'salaris')
LIB = os.path.join(MIRROR, 'images', 'lib')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VIDEO = os.path.join(ROOT, 'media', 'salaris-event-fin180416.mp4')
GALLERY_MAP = os.path.join(ROOT, 'scripts', 'a2', 'gallery_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900'
      '&family=Wix+Madefor+Text:wght@400;500;600&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── фотоотчёт: исходное имя файла → (слаг, ширина) ──────────────────────────
# имена исходников это номера кадров фотографа, поэтому подписываем, что на них
PHOTOS = [
    ('_001.jpg', 'badges', 1400),      # ряды именных бейджей на стойке регистрации
    ('_004.jpg', 'welcome', 1400),     # жёлтая стойка велком-дринка у белого кирпича
    ('_006.jpg', 'hall-empty', 1600),  # зал до начала: пустые ряды, знак на экране
    ('_034.jpg', 'hostess', 1400),     # хостес с красными папками у пресс-волла
    ('_052.jpg', 'guests-1', 1200),    # гости на фуршете
    ('_060.jpg', 'guests-2', 1200),    # гости на фуршете
    ('_070.jpg', 'foyer', 1400),       # фуршетная линия и толпа
    ('_093.jpg', 'crowd', 1400),       # плотный сбор перед официальной частью
    ('_100.jpg', 'hall-full', 1600),   # тот же зал во время выступления, битком
    ('_118.jpg', 'hall-light', 1400),  # зал со световой фермой, гости сидят
    ('_144.jpg', 'slide-team', 1400),  # слайд «Команда проекта»: CBRE, Knight Frank
    ('_180.jpg', 'photo180', 1400),    # зона фото 180°, результат сразу на экране
    ('_184.jpg', 'nitro', 1400),       # станция с жидким азотом, оранжевые графины
    ('_212.jpg', 'art', 1200),         # подсвеченные рамки выставки на стене
    ('_234.jpg', 'bar', 1400),         # бармен в облаке азота
]
# кадр не из галереи, он лежит отдельно и был единственным фото старой страницы
EXTRA = ('as3263-6238-4839-b835-616638666666/photo_2020-10-11_01-.jpg', 'hall-wide', 1600)
LOGO = ('as3266-6136-4465-a430-643336316434/__-43.png', 'logo-salaris.png')

# ─── кадры аftermovie: (секунда, слаг, ширина) ──────────────────────────────
FRAMES = [
    (3.0, 'title', 1280),            # титр «Презентация МФК „Саларис“, 5|04|2018»
    (122.0, 'slide-transport', 1280),  # слайд: автобусная станция и пешеходный мост
    (124.5, 'slide-map', 1280),      # слайд: перспективная жилая застройка у МФК
    (12.0, 'poster', 1280),          # постер плеера: разговор гостей на входе
]


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(str(c) for c in cmd) + '\n' + r.stderr[-800:])


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req).read()


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
    head = ('/* Nunito + Wix Madefor Text, self-host для /event/salaris/.\n'
            '   Сгенерировано scripts/salaris-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'nunito-madefor.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def webp(path):
    """Тот же cwebp с теми же ключами, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def find_src(basename):
    """Файлы фотоотчёта разложены по каталогам-хешам, ищем по имени."""
    for d in os.listdir(LIB):
        p = os.path.join(LIB, d, basename)
        if os.path.exists(p):
            return p
    sys.exit(f'✗ не нашёл исходник {basename} в mirror/images/lib/')


def photos():
    os.makedirs(IMG, exist_ok=True)
    # сверка с реестром галерей: если фотоотчёт пополнят, несоответствие видно сразу
    gal = {os.path.basename(p) for p in
           json.load(open(GALLERY_MAP, encoding='utf-8'))['event/salaris']}
    known = {name for name, _, _ in PHOTOS}
    if gal - known:
        print('  ⚠ в gallery_map есть кадры, которых нет в PHOTOS:', ', '.join(sorted(gal - known)))

    for basename, slug, width in PHOTOS:
        dst = os.path.join(IMG, f'{slug}.jpg')
        sh(['ffmpeg', '-v', 'error', '-i', find_src(basename),
            '-vf', f'scale={width}:-2:flags=lanczos', '-q:v', '3', dst, '-y'])
        webp(dst)

    src, slug, width = EXTRA
    dst = os.path.join(IMG, f'{slug}.jpg')
    sh(['ffmpeg', '-v', 'error', '-i', os.path.join(LIB, src),
        '-vf', f'scale={width}:-2:flags=lanczos', '-q:v', '3', dst, '-y'])
    webp(dst)

    src, name = LOGO
    dst = os.path.join(IMG, name)
    sh(['ffmpeg', '-v', 'error', '-i', os.path.join(LIB, src),
        '-vf', 'scale=760:-2:flags=lanczos', dst, '-y'])
    webp(dst)
    print(f'✓ фото: {len(PHOTOS) + 2} шт. в mirror/images/salaris/')


def frames():
    os.makedirs(IMG, exist_ok=True)
    # -ss ПОСЛЕ -i: точный поиск по кадру. С быстрым поиском до -i ffmpeg
    # прыгает на ближайший ключевой кадр и промахивается мимо слайда.
    for sec, slug, width in FRAMES:
        dst = os.path.join(IMG, f'{slug}.jpg')
        sh(['ffmpeg', '-v', 'error', '-i', VIDEO, '-ss', str(sec),
            '-vf', f'scale={width}:-2:flags=lanczos', '-frames:v', '1',
            '-q:v', '3', dst, '-y'])
        webp(dst)
    print(f'✓ кадры ролика: {len(FRAMES)} шт. в mirror/images/salaris/')


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--photos' in args:
        photos()
    if do_all or '--frames' in args:
        frames()
