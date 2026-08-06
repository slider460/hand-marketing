#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Стенд Ставропольского края на ВДНХ» (/portfolio/stavropol-stand-vdnh/).

Что делает:
  1. Шрифты Prata + Commissioner из Google Fonts кладёт локально
     (mirror/fonts/files/ + mirror/fonts/prata-commissioner.css). Внешних CDN
     на сайте нет принципиально, поэтому качаем сами.
  2. Режет кадры naked-eye куба из съёмки media/stavropol-vdnh-nakedeye.mp4:
     это реальные сюжеты, которые крутились на кубе (танец, заставка, поле,
     слон, водопад, комбайн, Тифлисские ворота, ветропарк, флаг).
  3. Достаёт стоп-кадры зон стенда из media/stavropol-vdnh-main.mp4 там, где
     готовых фотографий нет или они мелкие (480px).
  4. Делает .webp рядом с каждым jpg (хостинг отдаёт webp, если файл есть).
  5. Режет короткую версию главного ролика: mirror/videos/stavropol-stand.mp4.
     В исходной съёмке экскурсию ведёт человек, которого не должно быть на сайте,
     поэтому монтаж собирается из кусков без него (список CLIP_SEGMENTS) и без
     звука: голос ведущего идёт на петличку и отдельно не отделяется.

Запуск: python3 scripts/stavropol-assets.py [--fonts] [--frames] [--clip]
Без флагов делает всё.
"""
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
IMG = os.path.join(MIRROR, 'images', 'stavropol')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VIDEO_CUBE = os.path.join(ROOT, 'media', 'stavropol-vdnh-nakedeye.mp4')
VIDEO_MAIN = os.path.join(ROOT, 'media', 'stavropol-vdnh-main.mp4')
CLIP = os.path.join(MIRROR, 'videos', 'stavropol-stand.mp4')

# куски исходной съёмки без ведущего, границы выверены по раскадровке 0.25 с
CLIP_SEGMENTS = [
    (0, 14.4),      # ВДНХ, вход на выставку, зелёный зал
    (22.4, 32.2),   # бинокуляр, зелёный зал, пейзажи КМВ
    (37.4, 44.8),   # велотренажёр и отснятые тропы
    (55.6, 57.7),   # открытка «С любовью из Ставрополья»
    (60.6, 68.5),   # экраны края, макет города, гоночный симулятор
    (78.4, 80.7),   # съёмочная группа и общий план стенда
    (86.6, 88.9),   # работа уехала в телефон, куб
    (93.0, 104.2),  # куб, зал, арка ВДНХ
]

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Prata'
      '&family=Commissioner:wght@400;500;600;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── сюжеты naked-eye куба: (секунда, имя файла, подпись) ────────────────────
# секунды сняты по раскадровке съёмки 3:41, один полный цикл контента
CUBE = [
    (8,   'dance',    'Танец над пшеничным полем'),
    (20,  'title',    'Заставка «Ставрополье — край для жизни»'),
    (40,  'field',    'Колосья выходят за плоскость экрана'),
    (64,  'elephant', 'Слон, символ края'),
    (88,  'wings',    'Колосья складываются в крылья'),
    (104, 'water',    'Вода падает внутрь куба'),
    (164, 'harvest',  'Уборочная'),
    (193, 'gate',     'Тифлисские ворота'),
    (201, 'wind',     'Ветропарк'),
    (217, 'flag',     'Флаг Ставропольского края'),
]
CUBE_CROP = 'crop=446:272:434:98'

# ─── зоны стенда: (секунда, имя файла) из главного ролика ────────────────────
ZONES = [
    (26, 'spirit-hall'),      # зелёная зона с холмами и светящимся источником
    (34, 'terrenkur-bike'),   # велотренажёр, посетитель крутит педали
    (44, 'terrenkur-road'),   # пейзаж на видеостенах терренкура
    (58, 'postcard'),         # «С любовью из Ставрополья»
    (62, 'city-panels'),      # подсвеченные панели с кварталами и кластерами
    (87, 'draw-phone'),       # картина уехала на телефон
    (80, 'stand-wide'),       # общий план стенда
]

# кадры, из которых нужен только кусок: (секунда, имя, crop w:h:x:y).
# Съёмка идёт экскурсией, ведущий стоит почти в каждом кадре с интерфейсами,
# поэтому берём моменты и рамки, где в кадре только сама техника.
ZONE_CROPS = [
    (72, 'glass-panel', 'crop=900:606:130:0'),   # панель с домом, без людей
    (82, 'draw-frame', 'crop=310:300:172:306'),  # готовая работа в золотой раме
]


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
    blocks = re.findall(r'/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    out, n = [], 0
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        wght = re.search(r'font-weight:\s*(\d+)', block).group(1)
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        name = f'{fam.lower()}-{wght}-{subset}.woff2'
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    head = ('/* Prata + Commissioner, self-host для /portfolio/stavropol-stand-vdnh/.\n'
            '   Сгенерировано scripts/stavropol-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'prata-commissioner.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def webp(path):
    """Тот же cwebp с теми же ключами, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def frames():
    os.makedirs(IMG, exist_ok=True)
    # -ss ПОСЛЕ -i: точный поиск по кадру. С быстрым поиском до -i ffmpeg
    # прыгает на ближайший ключевой кадр и промахивается мимо сюжета на 2-8 с.
    for sec, slug, _ in CUBE:
        dst = os.path.join(IMG, f'cube-{slug}.jpg')
        sh(['ffmpeg', '-v', 'error', '-i', VIDEO_CUBE, '-ss', str(sec),
            '-vf', CUBE_CROP + ',scale=892:-2:flags=lanczos', '-frames:v', '1',
            '-q:v', '3', dst, '-y'])
        webp(dst)
    for sec, slug in ZONES:
        dst = os.path.join(IMG, f'{slug}.jpg')
        sh(['ffmpeg', '-v', 'error', '-i', VIDEO_MAIN, '-ss', str(sec),
            '-vf', 'scale=1080:-2:flags=lanczos', '-frames:v', '1',
            '-q:v', '3', dst, '-y'])
        webp(dst)
    for sec, slug, crop in ZONE_CROPS:
        dst = os.path.join(IMG, f'{slug}.jpg')
        sh(['ffmpeg', '-v', 'error', '-i', VIDEO_MAIN, '-ss', str(sec),
            '-vf', crop, '-frames:v', '1', '-q:v', '3', dst, '-y'])
        webp(dst)
    # постер короткой версии берём из неё же, чтобы кадр совпадал с первым кадром
    if os.path.exists(CLIP):
        sh(['ffmpeg', '-v', 'error', '-i', CLIP, '-ss', '48',
            '-vf', 'scale=1080:-2', '-frames:v', '1', '-q:v', '3',
            os.path.join(IMG, 'poster-main.jpg'), '-y'])
        webp(os.path.join(IMG, 'poster-main.jpg'))
    sh(['ffmpeg', '-v', 'error', '-i', VIDEO_CUBE, '-ss', '88',
        '-frames:v', '1', '-q:v', '3',
        os.path.join(IMG, 'poster-cube.jpg'), '-y'])
    webp(os.path.join(IMG, 'poster-cube.jpg'))
    print(f'✓ кадры: {len(CUBE)} сюжетов куба + {len(ZONES) + len(ZONE_CROPS)} зон + постеры')


def clip():
    """Короткая версия ролика без ведущего и без звука."""
    os.makedirs(os.path.dirname(CLIP), exist_ok=True)
    sel = '+'.join(f'between(t,{a},{b})' for a, b in CLIP_SEGMENTS)
    sh(['ffmpeg', '-v', 'error', '-i', VIDEO_MAIN,
        '-vf', f"select='{sel}',setpts=N/FRAME_RATE/TB,scale=960:-2", '-an',
        '-c:v', 'libx264', '-crf', '27', '-preset', 'slower', '-profile:v', 'high',
        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', CLIP, '-y'])
    total = sum(b - a for a, b in CLIP_SEGMENTS)
    mb = os.path.getsize(CLIP) / 1024 / 1024
    print(f'✓ ролик: {len(CLIP_SEGMENTS)} кусков, {total:.0f} с, {mb:.1f} МБ')


def photos_webp():
    """У части исходных фото webp-соседа нет — дособрать."""
    src = os.path.join(MIRROR, 'portfolio', 'stavropol-vdnh')
    made = []
    for f in sorted(os.listdir(src)):
        if f.endswith('.jpg') and not os.path.exists(os.path.join(src, f + '.webp')):
            webp(os.path.join(src, f))
            # webp() сносит результат, который не меньше оригинала
            if os.path.exists(os.path.join(src, f + '.webp')):
                made.append(f)
    print(f'✓ webp дособрано для {len(made)} фото' +
          (': ' + ', '.join(made) if made else ' (остальные исходники уже мельче webp)'))


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--clip' in args:
        clip()
    if do_all or '--frames' in args:
        frames()
        photos_webp()
