#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Кросс-мероприятия Marie Claire» (/event/marieclaire/).

Что делает:
  1. Шрифты Playfair Display + Jost из Google Fonts кладёт локально
     (mirror/fonts/files/ + mirror/fonts/playfair-jost.css). Внешних CDN
     на сайте нет принципиально, поэтому качаем сами.
  2. Перекладывает съёмку проекта из общего каталога mirror/images/lib/<hash>/
     в mirror/images/marieclaire/ под осмысленными именами: в lib лежат
     файлы вида «DSC01588-min.JPG», по ним не понять, что где.
  3. Режет кадры финального вечера в ТЦ «Метрополис» из media/marie-claire-event.mp4
     (2:37) — по ним на странице собрана лента вечера.
  4. Делает .webp рядом с каждым jpg (хостинг отдаёт webp, если файл есть).

Запуск: python3 scripts/marieclaire-assets.py [--fonts] [--photos] [--frames]
Без флагов делает всё.
"""
import os
import re
import shutil
import subprocess
import sys
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
LIB = os.path.join(MIRROR, 'images', 'lib')
IMG = os.path.join(MIRROR, 'images', 'marieclaire')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VIDEO = os.path.join(ROOT, 'media', 'marie-claire-event.mp4')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900'
      '&family=Jost:wght@300;400;500;600;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── съёмка проекта: (каталог в images/lib, файл, новое имя) ─────────────────
PHOTOS = [
    # застройка галерей ТЦ: белый корпус с аркой и пятёркой глаголов на стенах
    ('as3631-3230-4937-b730-623035626361', '12-min.JPG', 'stand-arch'),
    ('as6539-3538-4036-b532-383665383662', '32-min.JPG', 'stand-shoot'),
    ('as3531-6463-4162-a533-326664356139', '51-min.JPG', 'stand-makeup'),
    ('as3430-3037-4362-b735-643565666339', '47-min.JPG', 'promo-team'),
    ('as6333-3533-4064-a433-366634343733', '07092012637-min.jpg', 'corner-mall'),
    ('as3063-3334-4136-b732-343831383763', '07092012638-min.jpg', 'prix-2012'),
    ('as6132-6365-4832-b835-326262633330', '08092012649-min.jpg', 'gift-bags'),
    # «Приз великолепия» / Prix d'Excellence de la Beauté
    ('as6535-6533-4037-a630-386134363731', '_MG_2115-min.jpg', 'prix-2011'),
    ('as3763-3033-4663-b737-636561336634', 'IMG_1074-min.JPG', 'prix-2013'),
    # Fan di FENDI
    ('as3863-3634-4530-a236-306461303935', 'DSC01588-min.JPG', 'fendi-stand'),
    ('as3933-6166-4962-b731-373237356534', 'DSC01595-min.JPG', 'fendi-wall'),
    ('as3732-3832-4064-a233-616139643239', 'DSC01611-min.JPG', 'fendi-bar'),
    ('as6135-3430-4864-b337-663564323631', 'DSC01635-min.JPG', 'fendi-desk'),
    # бренд-корнеры и POSm
    ('as6137-3964-4332-b837-396538323937', '1500x1500_itog-min.jpg', 'viz-esteelauder'),
    ('as3961-6135-4761-a631-393465396532', 'clarins-150x150_var2.jpg', 'viz-clarins'),
    ('as3836-3462-4631-a162-313366356533', 'parus_var2-min.jpg', 'clarins-sail'),
    ('as3865-6535-4037-a330-373037316666', 'IMG_1073-min.JPG', 'dior-corner'),
    # выставки и турниры
    ('as3835-6137-4065-a334-616633393263', 'DSC01086-min.JPG', 'expo-stand'),
    ('as6237-3865-4237-b662-613062643635', 'DSC01094-min.JPG', 'expo-tennis'),
    ('as3934-6434-4362-a236-656332393034', 'DSC01381-min.JPG', 'expo-promo'),
    ('as3764-3630-4234-b139-303364616639', 'DSC01704-min.JPG', 'expo-intercharm'),
    ('as3437-3964-4430-a566-393136393134', 'DSC01715-min.JPG', 'expo-table'),
    ('as6161-3163-4834-a531-313739626634', 'DSC01720-min.JPG', 'expo-girls'),
    ('as6561-6463-4866-a534-646537646630', 'DSC01795-min.JPG', 'expo-model'),
    ('as3663-6263-4836-a230-303230623339', 'P1030953-min.JPG', 'expo-sport'),
]

# ─── лента финального вечера в «Метрополисе»: (секунда, имя) ─────────────────
# Ролик снят одной сменой: от дневной стойки регистрации до ночного шоу,
# поэтому кадры идут в хронологии вечера и на странице лежат в том же порядке.
FRAMES = [
    (13.0, 'night-desk'),      # стойка регистрации в галерее, ещё день
    (70.4, 'night-tag'),       # бирка «marie claire рекомендует» на витрине
    (19.0, 'night-looks'),     # образы на манекенах за красной лентой
    (26.5, 'night-hair'),      # зона стайлинга Cloud Nine
    (35.0, 'night-nails'),     # nail-бар
    (58.5, 'night-makeup'),    # make-up бар
    (50.5, 'night-photo'),     # фотозона у пресс-волла
    (85.0, 'night-show'),      # показ мод, разбор образов
    (118.0, 'night-podium'),   # подиум сверху: дискошар и шоу-программа
    (130.0, 'night-band'),     # выступление группы
    (92.0, 'night-crowd'),     # зрители на всех ярусах галереи
    (108.5, 'night-award'),    # награждение и вопросы из зала
    (138.0, 'night-gift'),     # подарок от журнала у пресс-волла
]
POSTER = (118.0, 'night-poster')


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
    head = ('/* Playfair Display + Jost, self-host для /event/marieclaire/.\n'
            '   Сгенерировано scripts/marieclaire-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'playfair-jost.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print('✓ шрифты: %d @font-face, скачано файлов %d' % (len(out), n))


def webp(path):
    """Тот же cwebp с теми же ключами, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def photos():
    os.makedirs(IMG, exist_ok=True)
    for d, f, name in PHOTOS:
        src = os.path.join(LIB, d, f)
        if not os.path.exists(src):
            sys.exit('✗ нет исходника: %s' % src)
        dst = os.path.join(IMG, name + '.jpg')
        # съёмка 2011-2013: часть кадров всего 800×600, увеличивать нечего —
        # ужимаем только то, что шире 1600, остальное копируем как есть.
        sh(['ffmpeg', '-v', 'error', '-i', src,
            '-vf', "scale='min(1600,iw)':-2", '-q:v', '3', dst, '-y'])
        if os.path.getsize(dst) > os.path.getsize(src):
            shutil.copyfile(src, dst)
        webp(dst)
    print('✓ фото: %d' % len(PHOTOS))


def grab(sec, name, q='3'):
    dst = os.path.join(IMG, name + '.jpg')
    # -ss ПОСЛЕ -i: точный поиск по кадру, иначе ffmpeg прыгает на ключевой
    # кадр и промахивается мимо сцены на секунду-другую.
    sh(['ffmpeg', '-v', 'error', '-i', VIDEO, '-ss', str(sec),
        '-frames:v', '1', '-q:v', q, dst, '-y'])
    webp(dst)


def frames():
    if not os.path.exists(VIDEO):
        sys.exit('✗ нет ролика: %s (лежит вне git, см. VIDEO-UPLOAD.md)' % VIDEO)
    os.makedirs(IMG, exist_ok=True)
    for sec, name in FRAMES:
        grab(sec, name)
    grab(*POSTER, q='2')
    print('✓ кадры вечера: %d + постер' % len(FRAMES))


if __name__ == '__main__':
    args = set(sys.argv[1:])
    allof = not args
    if allof or '--fonts' in args:
        fonts()
    if allof or '--photos' in args:
        photos()
    if allof or '--frames' in args:
        frames()
