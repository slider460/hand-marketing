#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Рекламный ролик УАЗ Патриот & Eaton» (/video/patriot/).

Что делает:
  1. Шрифты Alumni Sans + Fira Sans из Google Fonts кладёт локально
     (mirror/fonts/files/ + mirror/fonts/alumni-fira.css). Внешних CDN на
     сайте нет принципиально, поэтому качаем сами.
  2. Режет кадры из самого ролика media/eaton-yaz.mp4 — других материалов по
     кейсу нет, а ролик и есть работа. Секунды выверены по раскадровке 0.5 с:
     кабинет (схема на флипчарте, анимация ELocker на ноутбуке), поле (пыль,
     грязь, брод), кульминация на 40-й секунде — палец на кнопке блокировки.
  3. Делает .webp рядом с каждым jpg (хостинг отдаёт webp, если файл есть).

Запуск: python3 scripts/patriot-assets.py [--fonts] [--frames]
Без флагов делает всё.
"""
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
IMG = os.path.join(MIRROR, 'images', 'patriot')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VIDEO = os.path.join(ROOT, 'media', 'eaton-yaz.mp4')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Alumni+Sans:wght@400;600;700;800'
      '&family=Fira+Sans:wght@400;500;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── кадры: (секунда, имя файла, ширина) ────────────────────────────────────
FRAMES = [
    (30.5, 'hero', 1280),        # Патриот в брод, туман над водой
    (21.0, 'poster', 1280),      # постер плеера: машина в стене грязи
    (1.5, 'city', 1080),         # Москва-Сити на рассвете
    (11.0, 'bridge', 1080),      # Патриот в городе
    (13.0, 'office', 1080),      # разбор схемы у ноутбука, логотип Eaton
    (14.5, 'laptop-open', 1080),  # «Работа в открытом состоянии»
    (19.0, 'marker', 1080),      # маркер у флипчарта
    (27.5, 'night', 1080),       # ночь, один в переговорке
    (34.0, 'board', 1080),       # снова к флипчарту
    (36.0, 'elocker', 1080),     # ELocker: момент распределяется на оба колеса
    (17.5, 'dust', 1080),        # грунтовка, пыль из-под колёс
    (22.5, 'mud', 1080),         # грязь заливает капот
    (24.5, 'splash', 1080),      # брызги из-под колеса
    (33.5, 'ford', 1080),        # колесо в воде
    (40.5, 'button', 1080),      # палец жмёт кнопку блокировки
    (42.5, 'tacho', 1080),       # тахометр
    (45.5, 'wheel', 1080),       # колесо выходит из воды
    (47.5, 'out', 1080),         # машина вышла на берег
    (50.5, 'hero-man', 1080),    # герой у машины в поле
    (56.5, 'packshot', 1280),    # пэкшот УАЗ + EATON
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
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        name = f'{fam.lower().replace(" ", "-")}-{wght}-{subset}.woff2'
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    head = ('/* Alumni Sans + Fira Sans, self-host для /video/patriot/.\n'
            '   Сгенерировано scripts/patriot-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'alumni-fira.css'), 'w', encoding='utf-8').write(
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
    # прыгает на ближайший ключевой кадр и промахивается мимо сюжета.
    for sec, slug, width in FRAMES:
        dst = os.path.join(IMG, f'{slug}.jpg')
        sh(['ffmpeg', '-v', 'error', '-i', VIDEO, '-ss', str(sec),
            '-vf', f'scale={width}:-2:flags=lanczos', '-frames:v', '1',
            '-q:v', '3', dst, '-y'])
        webp(dst)
    print(f'✓ кадры: {len(FRAMES)} шт. в mirror/images/patriot/')


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--frames' in args:
        frames()
