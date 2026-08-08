#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «3D Mapping шоу в Ставрополе» (/3d/stavropol/).

Что делает:
  1. Шрифты Unbounded + Fira Sans из Google Fonts кладёт локально
     (mirror/fonts/files/ + mirror/fonts/unbounded-fira.css). Внешних CDN
     на сайте нет принципиально, поэтому качаем сами.
  2. Режет кадры из съёмки media/stavropol-3dmapping.mp4:
     — сцены шоу с «воздушной» камеры (она стоит неподвижно всю программу,
       поэтому фасад в каждом кадре в одной и той же геометрии — на этом
       держится «пульт мэппинга» на странице: зоны проекторов ложатся
       на кадр по одному и тому же четырёхугольнику);
     — техника и площадь: башня проекторов, прибор, пульт, лазерный софт,
       монтаж, толпа, лазер в ёлку.
  3. Делает .webp рядом с каждым jpg (хостинг отдаёт webp, если файл есть).
  4. Постер для плеера.

Запуск: python3 scripts/stavropol-3d-assets.py [--fonts] [--frames]
Без флагов делает всё.
"""
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
IMG = os.path.join(MIRROR, 'images', 'stavropol-3d')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VIDEO = os.path.join(ROOT, 'media', 'stavropol-3dmapping.mp4')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;500;700'
      '&family=Fira+Sans:wght@400;500;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── сцены шоу с неподвижной верхней камеры ──────────────────────────────────
# Кадр 1280×720 режется одинаково: crop 960×300 от (120, 270). В этой рамке
# фасад Дома Правительства лежит четырёхугольником (30,26) (938,42) (938,251)
# (31,187) — по нему страница строит зоны проекторов.
SCENE_CROP = 'crop=960:300:120:270'
# Съёмка сведена в 2,2:1, сверху и снизу в кадре 1280×720 чёрные поля по 69 px.
SHOT_CROP = 'crop=1280:582:0:69'
SCENES = [
    (58.5, 'scene-arcade'),      # здание разбирается в античную аркаду
    (65.0, 'scene-carpet'),      # ковровый орнамент
    (72.0, 'scene-deer'),        # олени
    (80.0, 'scene-elephants'),   # слоны, символ края
    (90.0, 'scene-tree'),        # ёлка и золотой орнамент во всю длину
    (94.0, 'scene-laser'),       # лазерная графика поверх проекции
]

# ─── площадь и техника: (секунда, имя) ───────────────────────────────────────
SHOTS = [
    (33.0, 'flags'),        # флаги России и края над площадью, день
    (44.0, 'rig'),          # монтаж прибора на ферме
    (70.2, 'projector'),    # проекционный блок на площади
    (71.0, 'desk'),         # пульт
    (78.5, 'laser-soft'),   # лазерная графика в софте на планшете
    (82.8, 'tower'),        # башня проекторов
    (97.0, 'facade-laser'), # фасад и лазеры, вид с площади
    (101.0, 'tree-laser'),  # луч в ёлку
    (120.0, 'crowd'),       # дискотека на площади
    (66.0, 'fog'),          # туман над площадью в свете проекции
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
        wght = re.search(r'font-weight:\s*([\d ]+);', block).group(1).strip().replace(' ', '-')
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        name = '%s-%s-%s.woff2' % (fam.lower().replace(' ', '-'), wght, subset)
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, 'files/%s' % name))
    head = ('/* Unbounded + Fira Sans, self-host для /3d/stavropol/.\n'
            '   Сгенерировано scripts/stavropol-3d-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'unbounded-fira.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print('✓ шрифты: %d @font-face, скачано файлов %d' % (len(out), n))


def webp(path):
    """Тот же cwebp с теми же ключами, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def grab(sec, dst, vf, q='2'):
    # -ss ПОСЛЕ -i: точный поиск по кадру, иначе ffmpeg прыгает на ключевой
    # кадр и промахивается мимо сцены на несколько секунд.
    sh(['ffmpeg', '-v', 'error', '-i', VIDEO, '-ss', str(sec),
        '-vf', vf, '-frames:v', '1', '-q:v', q, dst, '-y'])
    webp(dst)


def frames():
    os.makedirs(IMG, exist_ok=True)
    for sec, slug in SCENES:
        grab(sec, os.path.join(IMG, slug + '.jpg'), SCENE_CROP)
    for sec, slug in SHOTS:
        grab(sec, os.path.join(IMG, slug + '.jpg'),
             SHOT_CROP + ',scale=1120:-2:flags=lanczos')
    # постер плеера: общий план фасада с площади
    grab(88.0, os.path.join(IMG, 'poster.jpg'), SHOT_CROP + ',scale=1280:-2:flags=lanczos',
         q='3')
    print('✓ кадры: %d сцен шоу + %d планов площади + постер' % (len(SCENES), len(SHOTS)))


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--frames' in args:
        frames()
