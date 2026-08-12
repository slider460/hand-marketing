#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Партнёрская конференция Eaton» (/event/eaton/).

Что делает:
  1. Шрифты Cuprum + PT Sans из Google Fonts кладёт локально
     (mirror/fonts/files/ + mirror/fonts/cuprum-ptsans.css). Внешних CDN
     на сайте нет принципиально, поэтому качаем сами.
  2. Перекладывает съёмку конференции из общего каталога mirror/images/lib/<hash>/
     в mirror/images/eaton-almaty/ под осмысленными именами: в lib лежат
     файлы вида «DSC_2635.jpg», по ним не понять, что где.
  3. Режет кадры из media/eaton-almaty.mp4 (1:47) — застройка, зал, кофе-брейк.
  4. Растрирует гид участника (8 полос, Eaton_Kazahstan_2016_print.pdf) и макет
     бейджа (eaton_badge_2.pdf) — это наши печатные макеты 2016 года, страница
     построена вокруг них. На 4-й полосе замазываются три личных мобильных
     номера организаторов: на публичной странице им не место.
  5. Делает .webp рядом с каждым jpg (хостинг отдаёт webp, если файл есть).

Исходные PDF лежат вне репозитория (~/Downloads), поэтому шаг --guide
переносится только при наличии файлов; готовые jpg коммитятся.

Запуск: python3 scripts/eaton-almaty-assets.py [--fonts] [--photos] [--frames] [--guide]
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
IMG = os.path.join(MIRROR, 'images', 'eaton-almaty')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VIDEO = os.path.join(ROOT, 'media', 'eaton-almaty.mp4')

HOME = os.path.expanduser('~')
PDF_GUIDE = os.path.join(HOME, 'Downloads', 'Eaton_Kazahstan_2016_print.pdf')
PDF_BADGE = os.path.join(HOME, 'Downloads', 'eaton_badge_2.pdf')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Cuprum:wght@400;500;600;700'
      '&family=PT+Sans:wght@400;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── съёмка конференции: (каталог в images/lib, файл, новое имя) ─────────────
PHOTOS = [
    ('as6539-3937-4134-a262-613030353036', 'DSC_2707.jpg', 'hotel-sign'),    # вывеска Tien Shan Hotels
    ('as6664-6636-4232-b037-326662316634', 'DSC_1830.jpg', 'badges'),        # бейджи на синих лентах
    ('as3233-3662-4562-b966-316263316265', 'DSC_1843.jpg', 'registration'),  # стойка регистрации
    ('as3131-3136-4638-b366-363130366434', 'DSC_2635.jpg', 'hall-empty'),    # зал до участников
    ('as6136-3733-4663-a363-643964353234', 'DSC_2049.jpg', 'hall-full'),     # зал с участниками
    ('as3639-6666-4031-b363-383362346239', 'DSC_1891.jpg', 'panel'),         # четверо у экрана
    ('as3062-6531-4631-b338-616638336333', 'DSC_2107.jpg', 'speaker-m'),     # спикер у ролл-апа
    ('as3738-6664-4930-b839-306365333134', 'DSC_2075.jpg', 'rollup'),        # ролл-ап крупно
    ('as3733-3438-4339-b837-633835363933', 'DSC_2407.jpg', 'kit'),           # каталог, блокнот, брелок
    ('as3463-3138-4231-b263-656561643639', 'DSC_2645.jpg', 'photozone'),     # бренд-волл
]

# ─── кадры ролика: (секунда, имя) ───────────────────────────────────────────
FRAMES = [
    (12, 'v-rollup-night'),   # ролл-ап «Больше возможностей для Вашего бизнеса»
    (20, 'v-desk'),           # стойка регистрации со скатертью Eaton
    (24, 'v-handover'),       # выдача бейджей
    (52, 'v-slide'),          # доклад, слайд на экране
    (92, 'v-networking'),     # общение в фойе
]
POSTER = (44, 'poster')       # панель у экрана — обложка ролика

# ─── гид участника: какая полоса как называется ─────────────────────────────
GUIDE_PAGES = 8
# личные мобильные на 4-й полосе: доли от ширины/высоты страницы (x0,y0,x1,y1)
PHONE_BOXES = [
    (0.340, 0.752, 0.530, 0.776),
    (0.368, 0.826, 0.564, 0.850),
    (0.302, 0.843, 0.492, 0.867),
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
        name = '%s-%s-%s.woff2' % (fam.lower().replace(' ', '-'), wght, subset)
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, 'files/%s' % name))
    head = ('/* Cuprum + PT Sans, self-host для /event/eaton/.\n'
            '   Сгенерировано scripts/eaton-almaty-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'cuprum-ptsans.css'), 'w', encoding='utf-8').write(
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
        # съёмка 2016 года — 1680 px по длинной стороне, увеличивать нечего
        sh(['ffmpeg', '-v', 'error', '-i', src,
            '-vf', "scale='min(1600,iw)':-2", '-q:v', '3', dst, '-y'])
        if os.path.getsize(dst) > os.path.getsize(src):
            shutil.copyfile(src, dst)
        webp(dst)
    print('✓ фото: %d' % len(PHOTOS))


def grab(sec, name, q='3', crop=True):
    dst = os.path.join(IMG, name + '.jpg')
    # -ss ПОСЛЕ -i: точный поиск по кадру, иначе ffmpeg прыгает на ключевой
    # кадр и промахивается мимо сцены на секунду-другую
    cmd = ['ffmpeg', '-v', 'error', '-i', VIDEO, '-ss', str(sec), '-frames:v', '1']
    if crop:
        # в ролик впечатан кинематографический леттербокс: полосы 76 px сверху
        # и 92 px снизу от кадра 1280×720. На странице кадры стоят рядом с
        # фотографиями, полосы там выглядят браком, поэтому режем.
        # Постер оставляем нетронутым: он должен совпасть с первым кадром плеера.
        cmd += ['-vf', 'crop=1280:552:0:76']
    sh(cmd + ['-q:v', q, dst, '-y'])
    webp(dst)


def frames():
    if not os.path.exists(VIDEO):
        sys.exit('✗ нет ролика: %s (лежит вне git, см. VIDEO-UPLOAD.md)' % VIDEO)
    os.makedirs(IMG, exist_ok=True)
    for sec, name in FRAMES:
        grab(sec, name)
    grab(POSTER[0], POSTER[1], q='2', crop=False)
    print('✓ кадры ролика: %d + постер' % len(FRAMES))


def guide():
    """Полосы гида и бейдж из исходных PDF 2016 года."""
    from PIL import Image, ImageFilter
    for p in (PDF_GUIDE, PDF_BADGE):
        if not os.path.exists(p):
            sys.exit('✗ нет исходника: %s\n  PDF лежат вне репозитория, положи '
                     'их в ~/Downloads или прогоняй скрипт без --guide '
                     '(готовые jpg уже в git)' % p)
    os.makedirs(IMG, exist_ok=True)
    tmp = os.path.join(IMG, '_tmp')
    os.makedirs(tmp, exist_ok=True)

    sh(['pdftoppm', '-r', '170', '-png', PDF_GUIDE, os.path.join(tmp, 'g')])
    for i in range(1, GUIDE_PAGES + 1):
        src = os.path.join(tmp, 'g-%d.png' % i)
        im = Image.open(src).convert('RGB')
        if i == 4:
            # три личных мобильных на полосе с контактами организаторов:
            # размываем до нечитаемости, плашка и имена остаются на месте
            w, h = im.size
            for x0, y0, x1, y1 in PHONE_BOXES:
                box = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
                im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(9)), box)
        dst = os.path.join(IMG, 'guide-%d.jpg' % i)
        im.save(dst, quality=88, optimize=True)
        webp(dst)

    sh(['pdftoppm', '-r', '260', '-png', PDF_BADGE, os.path.join(tmp, 'b')])
    dst = os.path.join(IMG, 'badge.jpg')
    Image.open(os.path.join(tmp, 'b-1.png')).convert('RGB').save(dst, quality=90, optimize=True)
    webp(dst)

    shutil.rmtree(tmp)
    print('✓ гид: %d полос + бейдж' % GUIDE_PAGES)


if __name__ == '__main__':
    args = set(sys.argv[1:])
    allof = not args
    if allof or '--fonts' in args:
        fonts()
    if allof or '--photos' in args:
        photos()
    if allof or '--frames' in args:
        frames()
    if allof or '--guide' in args:
        guide()
