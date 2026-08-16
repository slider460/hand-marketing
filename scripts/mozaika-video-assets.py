#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Ролик ТРЦ „Мозаика“» (/video/mozaika/).

Источник один: media/mozaika.mp4 (4:31, 1280×720, путь из scripts/a2/video_map.json).
Ролик снят и смонтирован нами для вечера арендаторов «Мозаики» осенью 2018,
в нём 13 синхронов с арендаторами и экранная инфографика по объекту.

Что делает:
  1. Шрифты Russo One + Alegreya Sans кладёт локально (mirror/fonts/files/ +
     mirror/fonts/russo-alegreya.css). Внешних CDN на сайте нет принципиально.
     Russo One взят за квадратную геометрию: так нарисованы буквы знака
     «Мозаики» в заставке ролика.
  2. Собирает контактный лист всего ролика: 271 кадр, по одному на секунду,
     одним спрайтом strip.jpg (16×17 плиток по 160×90). На странице из него
     выложена мозаика — главная механика кейса.
  3. Режет кадры: портреты 13 спикеров (кроп по лицу, каскад OpenCV; нижняя
     треть с титром в кадр не попадает — имена набраны заново), вывески
     арендаторов, экранные плашки с цифрами, транспорт, события.
  4. Снимает кривую «ОТКРЫТИЕ МАГАЗИНОВ 2016-2018. GLA %» прямо с кадра:
     красные пиксели графика → полилиния в процентах (54,0 → 75,0).
     Данные в scripts/a2/mozaika_video_map.json, на странице график живой.
  5. Делает .webp рядом с каждым jpg (хостинг отдаёт webp, если файл есть).

Запуск: python3 scripts/mozaika-video-assets.py [--fonts] [--strip] [--frames] [--curve]
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
IMG = os.path.join(MIRROR, 'images', 'mozaika-video')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VID = os.path.join(ROOT, 'media', 'mozaika.mp4')      # источник: scripts/a2/video_map.json
MAP_JSON = os.path.join(ROOT, 'scripts', 'a2', 'mozaika_video_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Russo+One'
      '&family=Alegreya+Sans:wght@400;500;700;800&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

DUR = 270.6          # ffprobe
SHEET_COLS = 16      # плиток в ряду спрайта
TILE_W, TILE_H = 160, 90

# ─── синхроны: (слаг, старт, конец, секунда для портрета) ───────────────────
# границы сняты детектором склеек (ffmpeg scene>0.25), секунда портрета выбрана
# так, чтобы в кадре не было экранного титра и человек смотрел в камеру
SPEAKERS = [
    ('torkunov', 146.8, 154.4, 153.2),
    ('avdokhina', 154.4, 161.9, 160.7),
    ('tikhonenkova', 161.9, 167.2, 166.0),
    ('skuba', 167.2, 174.9, 173.7),
    ('skoritskaya', 174.9, 181.8, 180.6),
    ('bokovanova', 181.8, 186.3, 183.6),
    ('shirkevich', 186.3, 197.1, 195.9),
    ('ilyashenko', 197.1, 204.7, 203.5),
    ('kaya', 204.7, 215.5, 214.3),
    ('lomakin', 215.5, 222.2, 221.0),
    ('eremeev', 222.2, 229.8, 226.5),
    ('kuzmin', 229.8, 247.9, 246.7),
    ('starichenko', 255.9, 265.6, 264.4),
]

# ─── кадры: (секунда, слаг, ширина, что на кадре) ───────────────────────────
FRAMES = [
    (3.9, 'logo', 1280, 'заставка: знак «Мозаики» и рукописное «Делай интересно»'),
    (8.5, 'aero', 1280, 'комплекс с воздуха на фоне района'),
    (12.5, 'facade', 1280, 'входная группа со стороны Волгоградского проспекта'),
    (19.0, 'entrance', 1280, 'поток на входе в комплекс'),
    (16.5, 'atrium', 1280, 'атриум с деревьями сверху'),
    (30.5, 'gallery', 1280, 'торговая галерея в будний день'),
    # экранная инфографика
    (37.0, 'd-chart', 1280, 'график «Открытие магазинов 2016-2018. GLA %» и посещаемость'),
    (50.0, 'd-68k', 1280, 'плашка «торговая площадь 68 000 м²» над комплексом'),
    (54.8, 'd-134k', 1280, 'плашка «общая площадь 134 000 м²»'),
    (60.1, 'd-2500', 1280, 'плашка «парковка 2500 мест» над парковкой'),
    (103.5, 'd-mck', 1280, 'плашка «10 000 человек в день» на платформе МЦК «Дубровка»'),
    (129.0, 'd-map3d', 1280, '3D-карта подъездов: ТТК, съезды, вход в комплекс'),
    (134.5, 'd-map-ttk', 1280, 'та же карта крупно: внешняя и внутренняя стороны ТТК'),
    # вывески
    (61.8, 's-front', 1280, 'фасадные вывески: «Рив Гош», O`STIN, DNS, «Лента»'),
    (63.6, 's-ostin', 1280, 'вывеска O`STIN на фасаде'),
    (65.7, 's-lenta', 1280, 'вывеска гипермаркета «Лента»'),
    (67.0, 's-kinomax', 1280, 'вход в «Киномакс» с залом IMAX'),
    (69.0, 's-dns', 1280, 'вход в DNS «Гипер» с ростовой фигурой'),
    (70.8, 's-funday', 1280, 'вывески FUNDAY и «Котофей»'),
    (72.9, 's-kolyaski', 1280, 'вход в «Купи-коляску.ру»'),
    (74.0, 's-domovoy', 1280, 'вывеска «Домовой. Товары для дома»'),
    (75.2, 's-leto', 1280, 'вход в фитнес-клуб «Лето»'),
    (76.4, 's-gloria', 1280, 'вывеска Gloria Jeans'),
    (77.4, 's-familia', 1280, 'вход в Familia'),
    (78.8, 's-monki', 1280, 'вывеска Monki на фасаде'),
    (251.0, 's-kari', 1280, 'магазин kari в галерее'),
    # магазины, открывшиеся к съёмке
    (39.6, 'n-ichef', 1280, 'био-бистро I-CHEF'),
    (42.5, 'n-zolla', 1280, 'магазин Zolla'),
    (45.6, 'n-ruxara', 1280, 'магазин Ruxara'),
    # события и досуг
    (81.5, 'e-family', 1280, 'семьи в галерее комплекса'),
    (82.9, 'e-incl', 1280, 'проезд на колясках по галерее'),
    (85.2, 'e-fitness', 1280, 'фитнес-шоу на сцене комплекса'),
    (144.2, 'e-kids', 1280, 'детский мастер-класс в атриуме'),
    (145.8, 'e-play', 1280, 'игровая зона с сетками и батутом'),
    # транспорт
    (106.5, 't-esc', 1280, 'эскалатор от платформы МЦК к переходу'),
    (108.5, 't-bridge', 1280, 'крытый переход от МЦК «Дубровка» к комплексу'),
    (111.2, 't-stop', 1280, 'вывеска «Остановка маршрутного транспорта» с пятью станциями'),
    (114.5, 't-shuttle', 1280, 'фирменная маршрутка «Мозаики» у входа'),
    (121.0, 't-road', 1280, 'ТТК у комплекса'),
]

POSTER = (16.5, 'poster', 1280)


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
    head = ('/* Russo One + Alegreya Sans, self-host для /video/mozaika/.\n'
            '   Сгенерировано scripts/mozaika-video-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'russo-alegreya.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def webp(path):
    """Тот же cwebp с теми же ключами, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def cut(sec, slug, width, quality='3'):
    # -ss ПОСЛЕ -i: точный поиск по кадру. С быстрым поиском ffmpeg прыгает на
    # ближайший ключевой кадр и промахивается мимо плашки с цифрой.
    dst = os.path.join(IMG, f'{slug}.jpg')
    sh(['ffmpeg', '-v', 'error', '-i', VID, '-ss', str(sec),
        '-vf', f'scale={width}:-2:flags=lanczos', '-frames:v', '1',
        '-q:v', quality, dst, '-y'])
    webp(dst)
    return dst


def strip():
    """Контактный лист всего ролика одним спрайтом: 271 кадр, кадр в секунду."""
    os.makedirs(IMG, exist_ok=True)
    dst = os.path.join(IMG, 'strip.jpg')
    sh(['ffmpeg', '-v', 'error', '-i', VID,
        '-vf', (f'fps=1,scale={TILE_W}:{TILE_H}:flags=lanczos,'
                f'tile={SHEET_COLS}x17:padding=0:margin=0'),
        '-frames:v', '1', '-q:v', '6', dst, '-y'])
    webp(dst)
    kb = os.path.getsize(dst) // 1024
    wkb = os.path.getsize(dst + '.webp') // 1024 if os.path.exists(dst + '.webp') else 0
    print(f'✓ контактный лист: strip.jpg {kb} КБ (webp {wkb} КБ)')


def portraits():
    """Портреты спикеров: квадрат по лицу, титр ролика в кадр не попадает."""
    import cv2
    cc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    tmp = os.path.join(IMG, '_tmp.png')
    for slug, _a, _b, sec in SPEAKERS:
        sh(['ffmpeg', '-v', 'error', '-i', VID, '-ss', str(sec),
            '-frames:v', '1', tmp, '-y'])
        im = cv2.imread(tmp)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = [f for f in cc.detectMultiScale(gray, 1.1, 5, minSize=(70, 70))
                 if 20 < f[1] < 380]
        if not faces:
            sys.exit(f'✗ лицо не найдено: {slug} на {sec} с')
        x, y, w, h = max(faces, key=lambda f: f[2])
        side = int(min(max(w * 3.2, 420), 640))
        cx, cy = x + w // 2, y + h // 2
        x0 = int(min(max(cx - side // 2, 0), 1280 - side))
        y0 = int(min(max(cy - side * 0.42, 0), 720 - side))
        crop = cv2.resize(im[y0:y0 + side, x0:x0 + side], (560, 560),
                          interpolation=cv2.INTER_AREA)
        dst = os.path.join(IMG, f'p-{slug}.jpg')
        cv2.imwrite(dst, crop, [cv2.IMWRITE_JPEG_QUALITY, 86])
        webp(dst)
    os.remove(tmp)
    print(f'✓ портреты: {len(SPEAKERS)} шт.')


def frames():
    os.makedirs(IMG, exist_ok=True)
    for sec, slug, width, _what in FRAMES:
        cut(sec, slug, width)
    cut(POSTER[0], POSTER[1], POSTER[2])
    portraits()
    print(f'✓ кадры: {len(FRAMES) + 1} шт. в mirror/images/mozaika-video/')


# ─── кривая заполняемости с кадра ───────────────────────────────────────────
# График «ОТКРЫТИЕ МАГАЗИНОВ 2016-2018. GLA %» держится на экране с 24-й по 38-ю
# секунду и к 37-й дорисован до конца. Ось Y подписана 55-75 %, шаг сетки снят
# по пунктирным линиям: 55 % на y=360, 75 % на y=104, то есть 12,8 px на процент.
CURVE_SEC = 37.0
CURVE_X0, CURVE_X1 = 926, 1240      # левая ось и правый край поля графика
CURVE_Y75, CURVE_PX = 104.0, 12.8   # y семидесяти пяти процентов и px на 1 %


def curve():
    import numpy as np
    from PIL import Image
    tmp = os.path.join(IMG, '_chart.png')
    sh(['ffmpeg', '-v', 'error', '-i', VID, '-ss', str(CURVE_SEC),
        '-frames:v', '1', tmp, '-y'])
    a = np.asarray(Image.open(tmp).convert('RGB')).astype(int)
    os.remove(tmp)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = (r > 140) & (r - g > 60) & (r - b > 60)
    # по колонке берём самый длинный сплошной ряд красных пикселей: график
    # полупрозрачный, и в отдельных колонках сквозь него просвечивает красное
    # из съёмки (вывеска, куртка) — медиана по всем красным уводит точку вниз
    raw = []
    for x in range(CURVE_X0, CURVE_X1):
        ys = np.nonzero(red[60:430, x])[0]
        if len(ys) == 0:
            continue
        best, run = (ys[0], ys[0]), (ys[0], ys[0])
        for y in ys[1:]:
            run = (run[0], y) if y - run[1] <= 2 else (y, y)
            if run[1] - run[0] >= best[1] - best[0]:
                best = run
        raw.append((x, 60 + (best[0] + best[1]) / 2))
    # одиночные выбросы срезаем медианой по окну в 5 колонок
    pts = []
    for i, (x, _y) in enumerate(raw):
        w = [v for _u, v in raw[max(0, i - 2):i + 3]]
        y = float(np.median(w))
        pts.append((round((x - CURVE_X0) / (CURVE_X1 - 1 - CURVE_X0), 4),
                    round(75 - (y - CURVE_Y75) / CURVE_PX, 2)))
    if len(pts) < 200:
        sys.exit(f'✗ кривая не считалась: точек {len(pts)}')
    # прореживаем до ~40 точек: странице хватает, файл остаётся читаемым
    step = max(1, len(pts) // 40)
    thin = pts[::step]
    if thin[-1] != pts[-1]:
        thin.append(pts[-1])
    data = {
        '_': 'Снято с кадра ролика скриптом scripts/mozaika-video-assets.py',
        'source': {'sec': CURVE_SEC, 'title': 'ОТКРЫТИЕ МАГАЗИНОВ 2016-2018. GLA %'},
        'from': thin[0][1], 'to': thin[-1][1],
        'points': [[x, y] for x, y in thin],
    }
    old = {}
    if os.path.exists(MAP_JSON):
        old = json.load(open(MAP_JSON, encoding='utf-8'))
    old['gla'] = data
    json.dump(old, open(MAP_JSON, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'✓ кривая GLA: {len(thin)} точек, {data["from"]} % → {data["to"]} %')


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    os.makedirs(IMG, exist_ok=True)
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--strip' in args:
        strip()
    if do_all or '--frames' in args:
        frames()
    if do_all or '--curve' in args:
        curve()
