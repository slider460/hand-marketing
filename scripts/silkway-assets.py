#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «3D-визуализация маршрута Silk Way Rally» (/video/silkway/).

Материал (~/Downloads/silk_way):
  • «3D Silk Way.mp4» — сама сдача, 8:41, но всего 640×224. Это единственная
    существующая копия ролика, лучше нет: тот же файл лежит на хостинге как
    /media/silkway-3d.mp4.
  • 8 фотографий 4032×3024 с площадки и 2 видео 1080p (техзона и финал на
    LED-экране). Только они и дают нормальное разрешение, поэтому шапку
    страницы держат они, а не ролик.

Что делает скрипт:
  1. Шрифты Advent Pro + Arsenal локально (mirror/fonts/adventpro-arsenal.css).
     Внешних CDN на сайте нет принципиально.
  2. Фотографии HEIC → JPEG в трёх размерах + webp, mirror/images/silkway/.
  3. Два коротких лупа из MOV → mirror/videos/ (лежат внутри mirror/**,
     уезжают обычным деплоем, вручную грузить не надо).
  4. СНИМАЕТ ДАННЫЕ С РОЛИКА. Разрешения 640×224 не хватает, чтобы прочитать
     карточку этапа с одного кадра, поэтому берём временную медиану: фон
     под карточкой движется, сама карточка стоит, медиана по ~200 кадрам
     вычищает текст до читаемого. Так сняты все 10 карточек (проверено
     сверкой с фотографией монитора IMG_5856 и с финальной сводкой
     на LED-экране IMG_5865) и так же режутся постеры этапов.
  5. Ищет тайм-коды этапов: эталон карточки на каждый этап, дальше скан
     всего ролика посекундно с нормированной корреляцией. Нужен, чтобы
     клик по этапу перематывал плеер в его сцену.
  6. Палитра снята с самих плит рельефа в ролике (k-means по кадрам плит),
     плюс фирменный красный Silk Way с баннера на фотографии.

Всё считанное уходит в scripts/a2/silkway_map.json, страницу собирает
scripts/a2/gen_silkway.py.

Запуск: python3 scripts/silkway-assets.py [--fonts] [--photos] [--clips]
                                          [--stages] [--palette]
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
SRC = os.path.expanduser('~/Downloads/silk_way')
VIDEO = os.path.join(SRC, '3D Silk Way.mp4')
IMG = os.path.join(MIRROR, 'images', 'silkway')
VID = os.path.join(MIRROR, 'videos')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
MAP = os.path.join(ROOT, 'scripts', 'a2', 'silkway_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Advent+Pro:wght@400;600;700'
      '&family=Arsenal:ital,wght@0,400;0,700;1,400&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

VW, VH = 640, 224                      # родной размер ролика
CARD = (450, 8, 190, 112)              # x, y, w, h — угол с карточкой этапа

# ─── фотографии площадки: (слаг, файл, что в кадре) ────────────────────────
PHOTOS = [
    ('sand-table', 'IMG_5854.HEIC',
     'Стол для рисования песком: лайтбокс, камера на журавле над столом '
     'и монитор с картинкой, которая уходит в общую презентацию'),
    ('sand-crew', 'IMG_5855.HEIC',
     'Тот же стол со стороны техзоны: рядом рабочие места операторов'),
    ('monitor', 'IMG_5856.HEIC',
     'Контрольный монитор с карточкой первого этапа Xian—Zhongwei, '
     'за ним зал на монтаже и лайтбокс песочного стола'),
    ('hall', 'IMG_5857.HEIC',
     'Зал перед началом: LED-экран во всю сцену, по краям — тумбы со знаком '
     'ралли, подиум и красный ковёр'),
    ('led-relief', 'IMG_5858.HEIC',
     'Плита рельефа с линией маршрута на LED-экране зала'),
    ('hall-tables', 'IMG_5862.HEIC',
     'Зал накрыт к приёму: коктейльные столы, на экране китайская часть маршрута'),
    # IMG_5864 не берём: это тот же экран секундой раньше, чем IMG_5865,
    # и на странице он был бы вторым экземпляром одного кадра
    ('led-total-2', 'IMG_5865.HEIC',
     'Та же сводка крупнее: лиазоны, спецучастки и сервисные маршруты '
     'по обеим странам'),
]

# ─── лупы из съёмки: (слаг, файл, старт, длительность, ширина, что это) ────
CLIPS = [
    ('silkway-hall', 'IMG_5863.MOV', 3.6, 10.0, 1280,
     'Финал ролика на LED-экране в зале'),
    ('silkway-sand', 'IMG_5861.MOV', 22.5, 8.0, 1280,
     'Художник работает с песком на столе, камера сверху'),
]

# ─── якоря этапов: секунда, на которой карточка этапа заведомо на экране ───
# найдены просмотром ролика, дальше по ним строятся эталоны для скана
ANCHORS = [40, 62, 95, 130, 205, 285, 320, 365, 400, 475]

# ─── откуда резать постер этапа ────────────────────────────────────────────
# не совпадает с якорями: якорь нужен детектору (там карточка чистая),
# а постеру нужен кадр, где этап показан плитой рельефа целиком
POSTERS = [26, 62, 95, 130, 176, 258, 330, 356, 400, 475]

# ─── отдельные кадры ролика: (слаг, секунда, что в кадре) ──────────────────
STILLS = [
    ('finale', 508, 'Финальная сводка ролика: две плиты, Россия и Китай, '
     'и общий метраж марафона'),
    ('fuel', 250, 'Заправка спонсора на маршруте: сцена, собранная в 3D'),
]


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(str(c) for c in cmd) + '\n' + r.stderr[-800:])


def fetch(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA})).read()


def webp(path):
    """Те же ключи, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


# ══ 1. шрифты ══════════════════════════════════════════════════════════════
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
        ital = 'i' if 'font-style: italic' in block else ''
        name = f'{fam.lower().replace(" ", "-")}-{wght}{ital}-{subset}.woff2'
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    head = ('/* Advent Pro + Arsenal, self-host для /video/silkway/.\n'
            '   Сгенерировано scripts/silkway-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'adventpro-arsenal.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    cyr = sum(1 for s, _ in blocks if s.startswith('cyrillic'))
    print(f'✓ шрифты: {len(out)} @font-face (кириллических блоков {cyr}), '
          f'скачано файлов {n}')


# ══ 2. фотографии ══════════════════════════════════════════════════════════
def photos():
    os.makedirs(IMG, exist_ok=True)
    for slug, fname, _what in PHOTOS:
        src = os.path.join(SRC, fname)
        if not os.path.exists(src):
            sys.exit(f'✗ нет исходника: {src}')
        tmp = os.path.join(IMG, '_tmp.jpg')
        sh(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '92',
            src, '--out', tmp])
        im = cv2.imread(tmp)
        os.remove(tmp)
        for suffix, side, q in (('', 1800, 88), ('-m', 1100, 86), ('-s', 700, 84)):
            k = min(1.0, side / max(im.shape[1], im.shape[0]))
            dst = os.path.join(IMG, f'{slug}{suffix}.jpg')
            cv2.imwrite(dst, cv2.resize(im, None, fx=k, fy=k,
                                        interpolation=cv2.INTER_AREA),
                        [cv2.IMWRITE_JPEG_QUALITY, q])
            webp(dst)
    print(f'✓ фотографии: {len(PHOTOS)} шт. × 3 размера в mirror/images/silkway/')


# ══ 3. лупы со съёмки ══════════════════════════════════════════════════════
def clips():
    os.makedirs(VID, exist_ok=True)
    for slug, fname, ss, dur, w, _what in CLIPS:
        src = os.path.join(SRC, fname)
        if not os.path.exists(src):
            sys.exit(f'✗ нет исходника: {src}')
        dst = os.path.join(VID, f'{slug}.mp4')
        sh(['ffmpeg', '-v', 'error', '-ss', str(ss), '-t', str(dur), '-i', src,
            '-an', '-vf', f'scale={w}:-2', '-c:v', 'libx264', '-preset', 'slow',
            '-crf', '27', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
            dst, '-y'])
        # постер первого кадра — чтобы на телефоне без автоплея не было дыры
        pos = os.path.join(IMG, f'{slug}-poster.jpg')
        sh(['ffmpeg', '-v', 'error', '-ss', '1.2', '-i', dst, '-frames:v', '1',
            '-q:v', '3', pos, '-y'])
        webp(pos)
        print(f'  {slug}.mp4  {os.path.getsize(dst)//1024} КБ')
    print(f'✓ лупы: {len(CLIPS)} шт. в mirror/videos/')


# ══ 4-5. чтение ролика ═════════════════════════════════════════════════════
def gray_card_track():
    """Весь ролик одной лентой: серый кроп угла с карточкой на каждый кадр.
    13030 кадров × 112 × 190 = 277 МБ, в память влезает."""
    x, y, w, h = CARD
    cmd = ['ffmpeg', '-v', 'error', '-i', VIDEO, '-f', 'rawvideo',
           '-pix_fmt', 'gray', '-vf', f'crop={w}:{h}:{x}:{y}', '-']
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (w * h)
    return np.frombuffer(raw[:n * w * h], dtype=np.uint8).reshape(n, h, w)


def median_frame(t, dur=8.0):
    """Чистая карточка: медиана по окну. Фон движется, карточка стоит."""
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-t', str(dur),
                        '-i', VIDEO, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True)
    n = len(p.stdout) // (VW * VH * 3)
    if not n:
        sys.exit(f'✗ пустое окно медианы на {t} с')
    a = np.frombuffer(p.stdout[:n * VW * VH * 3], dtype=np.uint8).reshape(n, VH, VW, 3)
    return np.median(a, axis=0).astype(np.uint8)


def dominant(patch, k=4):
    """Самый частый тон куска кадра, но не чёрный и не выбеленный:
    именно цвет грунта, а не тень плиты и не пересвет неба."""
    px = patch.reshape(-1, 3).astype(np.float32)[::3]
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.4)
    _, lab, cen = cv2.kmeans(px, k, None, crit, 5, cv2.KMEANS_PP_CENTERS)
    cnt = np.bincount(lab.ravel(), minlength=k)
    ok = [i for i in range(k) if 45 < cen[i].mean() < 225]
    i = max(ok or range(k), key=lambda j: cnt[j])
    return '#%02X%02X%02X' % tuple(int(v) for v in cen[i])


def stages():
    """Постеры этапов + тайм-коды: с какой секунды крутить каждый этап."""
    os.makedirs(IMG, exist_ok=True)
    x, y, w, h = CARD

    def save(med, name):
        """Кадр ролика вдвое крупнее родных 640×224: в вёрстке он всё равно
        мелкий, а на ретине не рассыпается."""
        dst = os.path.join(IMG, f'{name}.jpg')
        cv2.imwrite(dst, cv2.resize(cv2.cvtColor(med, cv2.COLOR_RGB2BGR),
                                    (VW * 2, VH * 2), interpolation=cv2.INTER_LANCZOS4),
                    [cv2.IMWRITE_JPEG_QUALITY, 86])
        webp(dst)

    # эталон каждого этапа — чистая карточка вокруг якоря
    refs = []
    for t in ANCHORS:
        med = median_frame(t)
        refs.append(cv2.cvtColor(med[y:y + h, x:x + w], cv2.COLOR_RGB2GRAY)
                    .astype(np.float32))
    # постеры режутся со своих секунд: там этап показан плитой целиком.
    # оттуда же берём цвет этапа — доминирующий тон грунта на его же плите,
    # чтобы лента маршрута на странице была покрашена не на глаз
    colors = []
    for i, t in enumerate(POSTERS, 1):
        med = median_frame(t)
        save(med, f'stage-{i:02d}')
        colors.append(dominant(med[104:196, 30:610]))
    for name, t, _what in STILLS:
        save(median_frame(t), name)

    track = gray_card_track()
    fps = len(track) / 521.218
    secs = int(521)
    print(f'  ролик: {len(track)} кадров, {fps:.2f} fps')

    def sig(a):
        """Подпись карточки: только нижняя половина (там сама таблица),
        с вычтенным фоном — иначе корреляция считает не текст, а градиент
        ландшафта под полупрозрачной плашкой."""
        a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 1.0)
        a = a - cv2.GaussianBlur(a, (0, 0), 9.0)
        a = a[h // 2:]
        a = a - a.mean()
        s = a.std()
        return a / s if s > 1e-6 else a

    nrefs = [sig(r) for r in refs]
    step = int(round(fps))
    half = step * 2
    # score[s][k] — насколько секунда s похожа на карточку этапа k
    score = np.zeros((secs, len(nrefs)), dtype=np.float32)
    for s in range(secs):
        c = s * step
        win = track[max(0, c - half):c + half]
        if len(win) < 5:
            continue
        cur = sig(np.median(win, axis=0))
        for k, r in enumerate(nrefs):
            score[s, k] = float((cur * r).mean())

    # Этапы в ролике идут строго по порядку, поэтому не берём argmax
    # посекундно (он путает похожие карточки), а режем таймлайн на 10
    # последовательных отрезков так, чтобы суммарная похожесть была
    # максимальной. Классическая сегментация динамикой.
    K = len(nrefs)
    cum = np.vstack([np.zeros(K, np.float64), np.cumsum(score, axis=0)])
    NEG = -1e18
    dp = np.full((K + 1, secs + 1), NEG)
    back = np.zeros((K + 1, secs + 1), dtype=int)
    dp[0, 0] = 0.0
    for k in range(1, K + 1):
        for e in range(k, secs + 1):
            col = dp[k - 1, k - 1:e]
            gain = cum[e, k - 1] - cum[k - 1:e, k - 1]
            tot = col + gain
            j = int(np.argmax(tot))
            dp[k, e] = tot[j]
            back[k, e] = k - 1 + j
    bounds, e = [secs], secs
    for k in range(K, 0, -1):
        e = back[k, e]
        bounds.append(e)
    bounds.reverse()

    out = []
    for i in range(K):
        a, b = bounds[i], bounds[i + 1]
        col = score[a:b, i]
        thr = max(0.12, float(col.max()) * 0.45)
        on = [a + j for j, v in enumerate(col) if v >= thr]
        if not on:
            on = [a, b - 1]
        # самый длинный непрерывный кусок внутри отрезка (дырки до 3 с)
        runs, cur = [], [on[0]]
        for p, q in zip(on, on[1:]):
            if q - p <= 3:
                cur.append(q)
            else:
                runs.append(cur); cur = [q]
        runs.append(cur)
        run = max(runs, key=len)
        out.append({'from': int(run[0]), 'to': int(run[-1]),
                    'seek': int(max(0, run[0])), 'color': colors[i]})
        print(f'  этап {i+1:2d}: отрезок {a:3d}–{b:3d} с, '
              f'карточка {run[0]:3d}–{run[-1]:3d} с')
    return out


# ══ 6. палитра ═════════════════════════════════════════════════════════════
def palette():
    """Цвета берём с самих плит рельефа: k-means по кадрам, где плита
    занимает почти весь экран. Плюс красный Silk Way с баннера в зале."""
    px = []
    for t in (26, 62, 205, 285, 352, 400, 475):
        med = median_frame(t, 6.0)
        band = med[110:200, 40:600].reshape(-1, 3)          # тело плиты
        px.append(band[::7])
    px = np.vstack(px).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.4)
    _, lab, cen = cv2.kmeans(px, 6, None, crit, 6, cv2.KMEANS_PP_CENTERS)
    order = np.argsort(-np.bincount(lab.ravel(), minlength=6))
    ground = ['#%02X%02X%02X' % tuple(int(v) for v in cen[i]) for i in order]

    # фирменный красный: знак ралли напечатан на белой плашке обложки,
    # там он не залит светом зала, в отличие от баннеров на фотографиях
    cover = os.path.join(MIRROR, 'images', 'lib',
                         'as3165-6163-4638-a538-636436646239', '__-123.png')
    im = cv2.imread(cover)
    if im is None:
        sys.exit(f'✗ нет обложки со знаком: {cover}')
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    m = (((hsv[..., 0] < 8) | (hsv[..., 0] > 172)) & (hsv[..., 1] > 150)
         & (hsv[..., 2] > 110))
    bgr = np.median(im[m], axis=0) if m.sum() > 500 else np.array([26, 35, 226])
    red = '#%02X%02X%02X' % (int(bgr[2]), int(bgr[1]), int(bgr[0]))
    print(f'✓ палитра: грунт {ground}, красный {red}')
    return {'ground': ground, 'red': red}


def main():
    args = set(sys.argv[1:])
    steps = {'--fonts', '--photos', '--clips', '--stages', '--palette'}
    todo = args & steps or steps
    if not os.path.exists(VIDEO):
        sys.exit(f'✗ нет ролика: {VIDEO}')
    data = {}
    if os.path.exists(MAP):
        data = json.load(open(MAP, encoding='utf-8'))
    if '--fonts' in todo:
        fonts()
    if '--photos' in todo:
        photos()
        data['photos'] = {s: w for s, _f, w in PHOTOS}
    if '--clips' in todo:
        clips()
        data['clips'] = {s: w for s, _f, _a, _b, _c, w in CLIPS}
    if '--stages' in todo:
        data['stages'] = stages()
        data['stills'] = {n: w for n, _t, w in STILLS}
    if '--palette' in todo:
        data['palette'] = palette()
    json.dump(data, open(MAP, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('✓ карта:', os.path.relpath(MAP, ROOT))


if __name__ == '__main__':
    main()
