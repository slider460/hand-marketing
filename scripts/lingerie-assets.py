#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Подиумная съёмка для журнала Lingerie» (/video/lingerie/).

Единственный исходник — сам отчётный ролик media/lingerie.mp4: 7:08, 1280×720,
25 fps, «Гранд-дефиле Lingerie», Осень-Зима 2014/2015 на выставке CPM.
Ничего не дорисовано: вся фактура страницы снята с файла этим скриптом.

Что делает.

  1. Шрифты Oranienbaum + Mulish кладёт локально (mirror/fonts/files/ +
     mirror/fonts/oranienbaum-mulish.css). Внешних CDN на сайте нет
     принципиально. Oranienbaum — дидон с родной кириллицей, рифмуется
     с логотипом журнала; Mulish держит текст.

  2. Главный приём: вынимает из ролика каждый выход модели. Камера стоит
     неподвижно в торце подиума, поэтому силуэт растёт по мере приближения.
     Считаем фон локальной медианой (±5 с), берём крупнейшую связную
     компоненту переднего плана в границах подиума и ищем локальные максимумы
     её площади — это момент, когда модель дошла до отметки и встала в позу.
     Внутри окна пика уточняем кадр по минимуму движения (чтобы не поймать
     смазанный шаг) и режем портрет 3:4 вокруг силуэта.

  3. Пульс показа: та же площадь силуэта за все 428 секунд, прорежённая
     до ~2 значений в секунду, уезжает в lingerie_map.json — по ней страница
     рисует canvas-кривую с зубцом на каждый выход.

  4. Кадры-подложки: зал целиком, титульная плашка, финальная стенка логотипов.

  5. Палитра снимается с реальных кадров (чёрный зал, белый подиум,
     голубой экран задника).

  6. Рядом с каждым jpg делает .webp.

Разметка блоков (тайм-коды нижних плашек и склеек) снята детектом и лежит
в BLOCKS — она же уезжает в json.

Запуск: python3 scripts/lingerie-assets.py [--fonts] [--looks] [--frames] [--pulse]
Без флагов делает всё.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

import cv2
import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
IMG = os.path.join(MIRROR, 'images', 'lingerie')
LOOKS = os.path.join(IMG, 'looks')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VIDEO = os.path.join(ROOT, 'media', 'lingerie.mp4')
MAP_JSON = os.path.join(ROOT, 'scripts', 'a2', 'lingerie_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Oranienbaum'
      '&family=Mulish:wght@300;400;500;600;700;800&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── структура показа ───────────────────────────────────────────────────────
# (slug, имя как на плашке, подпись на финальной стенке, начало блока,
#  секунда нижней плашки, конец блока). Тайм-коды сняты детектом: плашка ищется
# по синему прямоугольнику в левом нижнем углу, границы блоков — по склейкам.
BLOCKS = [
    ('gattina',   'Gattina',                      'Gattina',                       10.0,  10.5,  55.1),
    ('vonfollies','Von Follies by Dita Von Teese','Von Follies by Dita Von Teese',  55.5,  56.0,  85.5),
    ('parah',     'Parah',                        'parah',                          85.9,  87.0, 115.8),
    ('vandacatucci','Vanda Catucci',              'VandaCatucci Milano',           116.2, 117.0, 146.1),
    ('dorofeeva', 'Марина Дорофеева',             'МАРИНА ДОРОФЕЕВА',              146.5, 147.0, 176.4),
    ('dana',      'Dana Pisarra',                 'DANA Pisarra',                  176.9, 178.0, 206.8),
    ('massana',   'Massana',                      'MASSANA Barcelona',             207.2, 208.0, 242.1),
    ('jc',        'Jaycris',                      'Artesania J&C Madrid',          242.5, 243.5, 272.4),
    ('nightdreams','Nightdreams',                 'NIGHTDREAMS by Boris Bütefür',  272.8, 274.0, 302.8),
    ('zimmerli',  'Zimmerli',                     'zimmerli of Switzerland',       303.2, 304.0, 333.1),
    ('ritratti',  'Ritratti',                     'RITRATTI Milano',               333.5, 334.5, 363.2),
    ('finale',    'Финал',                        '',                              363.2, 0.0,   413.1),
]

# кадры-подложки: (секунда, slug, ширина, что это)
FRAMES = [
    (2.0,   'title',   1400, 'титульная заставка ролика'),
    (16.0,  'hall',    1800, 'общий план: зал, подиум, зрители'),
    (24.0,  'close',   1800, 'крупный план: модель на отметке'),
    (367.0, 'finale',  1800, 'финал: экран вернулся к титульному слайду'),
    (414.5, 'wall',    1600, 'стенка из логотипов одиннадцати брендов'),
]

STEP = 5            # каждый 5-й кадр = 5 замеров в секунду
SMALL = (320, 180)  # рабочее разрешение разбора
WIN = 25            # ±5 с для локальной медианы фона
FLASH = 210         # средняя яркость выше — это склейка-вспышка, кадр не берём
DISSOLVE = 20       # межкадровая разница выше — это наплыв между планами


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(str(c) for c in cmd) + '\n' + r.stderr[-800:])


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req).read()


def webp(path):
    """Тот же cwebp с теми же ключами, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


# ─── 1. шрифты ──────────────────────────────────────────────────────────────
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
    head = ('/* Oranienbaum + Mulish, self-host для /video/lingerie/.\n'
            '   Сгенерировано scripts/lingerie-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'oranienbaum-mulish.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


# ─── разбор ролика ──────────────────────────────────────────────────────────
def read_small():
    """Все кадры ролика в сером 320×180 с шагом STEP. Возвращает (A, T, fps)."""
    cap = cv2.VideoCapture(VIDEO)
    if not cap.isOpened():
        sys.exit(f'✗ не открывается {VIDEO}')
    fps = cap.get(cv2.CAP_PROP_FPS)
    A, T, i = [], [], 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        if i % STEP == 0:
            A.append(cv2.resize(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), SMALL))
            T.append(i / fps)
        i += 1
    cap.release()
    return np.array(A, dtype=np.uint8), np.array(T), fps


def silhouette(A):
    """Площадь, низ и центр крупнейшего силуэта на подиуме в каждом кадре.

    Фон — медиана соседних кадров (±WIN шагов). Камера неподвижна, поэтому
    всё, что отличается от медианы в границах подиума, — идущая модель.
    Границы (верх 45 px, левее 70 и правее 250) отсекают ферму под потолком
    и ряды зрителей: там движения тоже хватает, но это не выход.
    """
    n = len(A)
    area = np.zeros(n)
    foot = np.zeros(n)
    cx = np.zeros(n)
    bright = A.reshape(n, -1).mean(axis=1)
    for i in range(n):
        a, b = max(0, i - WIN), min(n, i + WIN + 1)
        bg = np.median(A[a:b:3], axis=0).astype(np.uint8)
        m = (cv2.absdiff(A[i], bg) > 28).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        m[:45, :] = 0
        m[:, :70] = 0
        m[:, 250:] = 0
        cnt, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
        if cnt < 2:
            continue
        k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        if st[k, cv2.CC_STAT_AREA] < 80:
            continue
        area[i] = st[k, cv2.CC_STAT_AREA]
        foot[i] = st[k, cv2.CC_STAT_TOP] + st[k, cv2.CC_STAT_HEIGHT]
        cx[i] = cen[k][0]
    return area, foot, cx, bright


def motion(A):
    d = np.zeros(len(A))
    for i in range(1, len(A)):
        d[i] = float(np.abs(A[i].astype(np.int16) - A[i - 1].astype(np.int16)).mean())
    d[0] = d[1] if len(d) > 1 else 0
    return d


def title_bar(fps):
    """Флаг «на кадре висит нижняя плашка с именем бренда».

    Плашка — синий прямоугольник в левом нижнем углу; ищем по цвету
    (синий канал заметно выше красного) в прямоугольнике 2..47 % по ширине
    и 85..94 % по высоте. Кадры с плашкой в портрет не берём: она попала бы
    в угол обрезанным словом.
    """
    cap = cv2.VideoCapture(VIDEO)
    flags, i = [], 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        if i % STEP == 0:
            H, W = fr.shape[:2]
            r = fr[int(H * .85):int(H * .94), int(W * .02):int(W * .47)]
            r = cv2.resize(r, (40, 10)).astype(np.int16)
            b, g, rr = r[:, :, 0], r[:, :, 1], r[:, :, 2]
            flags.append(int(((b > rr + 35) & (b > 90) & (g > rr)).sum()) > 60)
        i += 1
    cap.release()
    return np.array(flags, dtype=bool)


def find_passes(T, area, cx, bright, mot, bar):
    """Локальные максимумы площади силуэта = выходы моделей.

    Пик берём как максимум сглаженной площади в окне ±12 шагов (±2,4 с),
    минимальный зазор между выходами — 2,5 с. Кадры со средней яркостью
    выше FLASH — это белые вспышки на склейках между блоками, они дают
    ложный «силуэт» во весь экран и отбрасываются.
    """
    s = np.convolve(area, np.ones(5) / 5, mode='same')
    raw = []
    for i in range(3, len(T) - 3):
        if bright[i] > FLASH:
            continue
        if s[i] != max(s[max(0, i - 12):i + 13]) or s[i] < 250:
            continue
        if raw and T[i] - T[raw[-1]] < 2.5:
            if s[i] > s[raw[-1]]:
                raw[-1] = i
            continue
        raw.append(i)
    # Уточняем кадр: наименьшее движение в узком окне ±1,2 с вокруг пика.
    # Окно шире одного наплыва (склейки внутри блоков идут через микс ~1 с),
    # иначе портрет попадает на двойную экспозицию или на смазанный шаг.
    # Шире не берём: через пару секунд модель уже развернулась и уходит,
    # такой кадр формально спокойный, но показывает спину.
    # Исключение — первый выход блока, на котором ещё висит нижняя плашка
    # с именем бренда: там тянемся вперёд до +2,4 с, пока плашка не уйдёт.
    def pick(i, lo, hi, skip_bar):
        a, b = max(0, i - lo), min(len(T), i + hi + 1)
        cost = [mot[k] if (bright[k] < FLASH and not (skip_bar and bar[k])) else 1e9
                for k in range(a, b)]
        return (a + int(np.argmin(cost))) if min(cost) < 1e9 else None

    out = []
    for i in raw:
        j = pick(i, 6, 6, True)
        if j is None:
            j = pick(i, 6, 12, True)          # плашка держится: ищем дальше вперёд
        if j is None:
            j = pick(i, 6, 6, False)          # не нашлось — берём как есть
        out.append({'t': round(float(T[j]), 2), 'area': float(s[i]), 'cx': float(cx[j])})
    # После сдвига два соседних пика могут сойтись в один кадр — схлопываем
    ded = []
    for p in out:
        if ded and p['t'] - ded[-1]['t'] < 2.0:
            if p['area'] > ded[-1]['area']:
                ded[-1] = p
            continue
        ded.append(p)
    return ded


def assign(passes):
    """Раскладываем выходы по блокам. Первые и последние 1,5 с блока
    не берём: там идёт переход на следующий бренд."""
    for slug, name, wall, a, tit, b in BLOCKS:
        got = [p for p in passes if a + 1.5 < p['t'] < b - 1.5]
        for k, p in enumerate(got, 1):
            p['brand'] = slug
            p['n'] = k
    return [p for p in passes if p.get('brand')]


# ─── 2. портреты выходов ────────────────────────────────────────────────────
def cut_look(cap, fps, p, dst, w=560, h=746):
    """Портрет 3:4 вокруг силуэта. Кроп по горизонтали ведём за центром
    силуэта, по вертикали берём нижние 88 % кадра: модель стоит на подиуме,
    сверху остаётся только задник."""
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(p['t'] * fps)))
    ok, fr = cap.read()
    if not ok:
        return False
    H, W = fr.shape[:2]
    ch = int(H * 0.88)
    cw = int(ch * 3 / 4)
    cxf = p['cx'] / SMALL[0] * W
    x = int(np.clip(cxf - cw / 2, 0, W - cw))
    y = H - ch
    crop = fr[y:y + ch, x:x + cw]
    crop = cv2.resize(crop, (w, h), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(dst, crop, [cv2.IMWRITE_JPEG_QUALITY, 88])
    return True


def looks(passes):
    os.makedirs(LOOKS, exist_ok=True)
    cap = cv2.VideoCapture(VIDEO)
    fps = cap.get(cv2.CAP_PROP_FPS)
    n = 0
    for p in passes:
        dst = os.path.join(LOOKS, f"{p['brand']}-{p['n']:02d}.jpg")
        if cut_look(cap, fps, p, dst):
            webp(dst)
            n += 1
    cap.release()
    print(f'✓ выходы: {n} портретов в {LOOKS}')


# ─── 3. кадры-подложки ──────────────────────────────────────────────────────
def frames():
    os.makedirs(IMG, exist_ok=True)
    for sec, slug, width, _what in FRAMES:
        dst = os.path.join(IMG, f'{slug}.jpg')
        # -ss ПОСЛЕ -i: точный поиск по кадру, иначе ffmpeg прыгает
        # на ближайший ключевой и промахивается мимо плашки
        sh(['ffmpeg', '-v', 'error', '-i', VIDEO, '-ss', str(sec),
            '-vf', f'scale={width}:-2:flags=lanczos', '-frames:v', '1',
            '-q:v', '3', dst, '-y'])
        webp(dst)
    print(f'✓ подложки: {len(FRAMES)} кадров')


# ─── 4. палитра ─────────────────────────────────────────────────────────────
def palette():
    """Три цвета зала прямо с кадра 16 с: тёмный борт, белый подиум,
    голубой экран задника."""
    cap = cv2.VideoCapture(VIDEO)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(16 * fps))
    ok, fr = cap.read()
    cap.release()
    if not ok:
        return {}
    H, W = fr.shape[:2]
    def med(x0, y0, x1, y1):
        r = fr[int(H * y0):int(H * y1), int(W * x0):int(W * x1)]
        b, g, rr = np.median(r.reshape(-1, 3), axis=0)
        return '#%02x%02x%02x' % (int(rr), int(g), int(b))
    return {'hall': med(0.02, 0.55, 0.12, 0.75),
            'runway': med(0.42, 0.88, 0.58, 0.97),
            'screen': med(0.46, 0.30, 0.54, 0.40)}


# ─── 5. карта для страницы ──────────────────────────────────────────────────
def build_map(T, area, passes, pal, fps, bright, mot):
    """Пульс прорежаем до ~2 значений в секунду и нормируем в 0..1000:
    страница рисует по нему canvas-кривую, точность выше не нужна.

    Три чистки, без которых кривая читается как шум, а не как ритм показа:
      • на белых вспышках между блоками «силуэтом» становится весь кадр —
        обнуляем по яркости;
      • вспышка идёт с разгоном и затуханием, и на её склонах медианный фон
        ещё загрязнён: гасим окно ±2 с вокруг каждой границы блока. Переход
        не принадлежит ничьему проходу, так что это не подгонка, а вырезание
        заведомо чужого куска;
      • внутри блоков планы склеены наплывом: полсекунды в кадре живут два
        изображения сразу, и «силуэтом» опять становится пол-экрана. Наплыв
        видно по всплеску межкадровой разницы (на проходе она 2..9, на
        наплыве за 20), такие кадры тоже гасим: это склейка, а не чьё-то
        положение на подиуме;
      • нормируем не по максимуму, а по 98-му процентилю, иначе один выброс
        прижимает все реальные зубцы к нулю.

    Рисуем корень из площади, а не площадь. Площадь силуэта растёт как квадрат
    приближения, поэтому на площади проход у самой отметки в разы выше прохода
    в середине подиума, и кривая читается как частокол случайных пиков. Корень
    возвращает линейную величину — видимый рост модели в кадре, то есть ровно
    то, что глаз и считывает как «далеко/близко».
    """
    a = area.copy()
    a[bright > FLASH] = 0.0
    a[mot > DISSOLVE] = 0.0
    for _s, _n, _w, st, _t, en in BLOCKS:
        for edge in (st, en):
            a[(T > edge - 2.0) & (T < edge + 2.0)] = 0.0
    a = np.sqrt(a)
    a = np.convolve(a, np.ones(5) / 5, mode='same')
    idx = np.arange(0, len(T), 2)
    mx = float(np.percentile(a[a > 0], 98)) if (a > 0).any() else 1.0
    pulse = [int(round(min(1.0, a[i] / mx) * 1000)) for i in idx]
    blocks = []
    for slug, name, wall, s, tit, e in BLOCKS:
        got = [p for p in passes if p['brand'] == slug]
        blocks.append({'slug': slug, 'name': name, 'wall': wall,
                       'start': s, 'title': tit, 'end': e,
                       'looks': [{'t': p['t'], 'n': p['n']} for p in got]})
    # длительность берём по числу кадров в файле, а не по прореженной выборке:
    # выборка округляет вверх и даёт 428,0 с вместо реальных 427,88,
    # из-за чего страница писала 7:08 там, где плеер показывает 7:07
    cap = cv2.VideoCapture(VIDEO)
    nframes = float(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    data = {'duration': round(nframes / fps, 2),
            'fps': fps, 'pulse_step': round(float(2 * STEP / fps), 3),
            'pulse': pulse, 'blocks': blocks, 'palette': pal,
            'total_looks': len(passes)}
    json.dump(data, open(MAP_JSON, 'w', encoding='utf-8'),
              ensure_ascii=False, separators=(',', ':'))
    print(f'✓ карта: {MAP_JSON}, выходов {len(passes)}, пульс {len(pulse)} точек')
    return data


if __name__ == '__main__':
    args = sys.argv[1:]
    todo = set(a.lstrip('-') for a in args) or {'fonts', 'looks', 'frames', 'pulse'}
    if 'fonts' in todo:
        fonts()
    if todo & {'looks', 'pulse'}:
        A, T, fps = read_small()
        area, foot, cx, bright = silhouette(A)
        mot = motion(A)
        bar = title_bar(fps)
        passes = assign(find_passes(T, area, cx, bright, mot, bar))
        if 'looks' in todo:
            looks(passes)
        if 'pulse' in todo:
            build_map(T, area, passes, palette(), fps, bright, mot)
    if 'frames' in todo:
        frames()
