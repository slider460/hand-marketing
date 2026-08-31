#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Вирусный ролик VIVAX SPORT с Настасьей Самбурской»
(/video/vivax/).

Материал:
  • сам ролик media/vivax-samburskaya.mp4, 49,28 с, 1080×606, 25 к/с;
  • четыре фотографии и один клип со смены 29.05.2017 (iPhone 7 Plus,
    гео 55.7372/37.5044) из «Материалы для обновления сайта/Vivax».
    Из шести исходных фото одно (2697ef71…, снято 28.05 в шатре Reebok/UFC)
    с другого дня и места, ещё одно повторяет соседний кадр площадки —
    оба не берутся. Из двух клипов взят тот, что длиннее и полнее;
    второй показывал ту же сцену почти с той же точки.

Что делает:
  1. Шрифты Jost + Inter Tight локально (mirror/fonts/jost-intertight.css
     + files/*.woff2). Jost — геометрическая антиква футуровского строя,
     тем же строем набраны титры ролика и логотип VIVAX. Внешних CDN
     на сайте нет принципиально.
  2. Режет склейки: гистограммы по 3×3 блокам, адаптивный порог по
     локальной медиане (съёмка с рук + быстрые панорамы дают ложные пики).
  3. Снимает кадры под страницу: в каждом окне берётся самый резкий кадр.
  4. Считает громкость по 0,25 с: на 30,25–32,25 с музыка уходит почти
     в ноль, и ровно там стоит самый длинный снятый план — пустой зал,
     из которого героиня уже выпала.
  5. Снимает палитру пипеткой с титровых шевронов и с плашки заставки.
  6. Готовит фото смены (3 размера + webp) и клип для веба. Клип снят
     на телефон вертикально, ориентация берётся из rotation-метаданных.
  7. Пишет scripts/a2/vivax_map.json.

Запуск: python3 scripts/vivax-assets.py [--fonts] [--stills] [--bts]
                                        [--clips] [--map]
Без флагов делает всё.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
import wave

import cv2
import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
IMG = os.path.join(MIRROR, 'images', 'vivax')
VIDEOS = os.path.join(MIRROR, 'videos')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
MAP = os.path.join(ROOT, 'scripts', 'a2', 'vivax_map.json')

VIDEO = os.path.join(ROOT, 'media', 'vivax-samburskaya.mp4')
SRC = ('/Users/aleksandrnarodetskii/Documents/Материалы для обновления сайта/Vivax')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Jost:wght@200;300;400;500;600;700'
      '&family=Inter+Tight:wght@400;500;600;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

FPS = 25.0
VW, VH = 1080, 606
DURATION = 49.28
END_CARD = 42.04   # с этой секунды идёт заставка VIVAX SPORT, съёмки в ней нет

# ─── кадры: (слаг, секунда, окно поиска резкого кадра, что в кадре) ────────
# секунды выверены по нарезке на планы, окно не выходит за границы плана
STILLS = [
    # приход в зал
    ('walk-far', 0.50, 0.30, 'Общий план зала: она идёт к камере между тренажёрами'),
    ('walk-mid', 1.80, 0.40, 'Средний план прохода по залу'),
    ('walk-legs', 3.30, 0.35, 'Ноги и шаг со спины, проход мимо стоек'),
    ('walk-face', 4.50, 0.35, 'Портрет: идёт прямо на камеру'),

    # разогрев, красный крем
    ('tube-warm', 5.85, 0.35, 'Красный тюбик VIVAX SPORT крупно, титр «Разогрев»'),
    ('title-warm', 6.25, 0.10, 'Титр ролика: красный шеврон и слово «Разогрев»'),
    ('warm-squeeze', 6.75, 0.12, 'Крем выдавливается на ладонь'),
    ('warm-shoulder', 7.10, 0.18, 'Наносит крем на плечо и ключицу'),
    ('warm-delta', 7.50, 0.14, 'Растирает дельту и трапецию'),
    ('warm-back', 7.90, 0.18, 'Растирает поясницу и косые'),
    ('warm-arm', 9.00, 0.40, 'Растирает предплечье, средний план'),

    # тренировка
    ('ex-kick', 10.20, 0.20, 'Отведение ноги назад в упоре'),
    ('ex-medball', 10.75, 0.22, 'Набивной мяч у груди'),
    ('ex-ballstep', 11.70, 0.25, 'Прыжки через набивной мяч'),
    ('ex-throw', 13.60, 0.25, 'Бросок набивного мяча над головой'),
    ('ex-bodybar', 14.20, 0.25, 'Бодибар на плечах, выпады'),
    ('ex-abs', 12.60, 0.35, 'Пресс и косые: серия ударов руками'),
    ('ex-squat', 15.10, 0.18, 'Приседания, перчатки у лица'),
    ('ex-glutes', 17.20, 0.22, 'Выпад, вид со спины'),
    ('ex-elbow', 17.72, 0.22, 'Удар локтем'),
    ('ex-plank', 18.90, 0.12, 'Упор лёжа, отведение ноги'),
    ('face-pad', 16.72, 0.20, 'Лапа болтается над головой, взгляд исподлобья'),
    ('ex-pads', 19.70, 0.45, 'Удары по боксёрским лапам'),
    ('ex-pads2', 20.65, 0.22, 'Тренер держит лапу, удар крупно'),
    ('rest-face', 21.24, 0.25, 'Портрет между подходами'),
    ('ex-stretch', 22.20, 0.20, 'Растяжка трицепса, рука за головой'),
    ('rest-smile', 22.76, 0.22, 'Улыбается, поднимает руку'),

    # восстановление, синий гель
    ('tube-cool', 23.95, 0.40, 'Синий тюбик VIVAX SPORT, титр «Восстановление»'),
    ('title-cool', 24.30, 0.15, 'Титр ролика: синий шеврон и слово «Восстановление»'),
    ('cool-squeeze', 24.80, 0.12, 'Гель выдавливается на ладонь'),
    ('cool-shin', 25.20, 0.20, 'Растирает гель по голени, нога поднята на опору'),
    ('cool-quad', 26.05, 0.35, 'Растирает гель по бедру, квадрицепс крупно'),
    ('fall-step', 28.40, 0.16, 'Стопа встаёт на край блина от штанги, лежащего на полу'),
    ('fall-flail', 29.52, 0.22, 'Взмах руками: равновесие потеряно'),
    ('fall-out', 30.08, 0.06, 'Уходит вниз, из кадра'),
    ('empty-gym', 31.50, 0.60, 'Пустой зал: само падение осталось за кадром'),
    ('fall-back', 33.36, 0.20, 'Выныривает обратно в кадр и вытирает лоб'),
    ('face-shock', 34.30, 0.20, 'Охает и оглядывает себя'),

    # травма, зелёный крем
    ('bruise', 35.90, 0.45, 'Ушиб на локте крупным планом'),
    ('grimace', 37.20, 0.55, 'Морщится от боли'),
    ('tube-heal', 39.40, 0.45, 'Зелёный тюбик VIVAX SPORT, титр «Реабилитация»'),
    ('title-heal', 39.10, 0.15, 'Титр ролика: зелёный шеврон и слово «Реабилитация»'),
    ('heal-elbow', 40.10, 0.12, 'Наносит крем на ушибленный локоть'),
    ('heal-rub', 40.55, 0.10, 'Растирает локоть'),
    ('heal-smile', 41.30, 0.50, 'Улыбается, растирает руку'),

    # заставка
    ('endcard', 45.00, 0.80, 'Заставка: VIVAX SPORT, «Ты сможешь больше!», www.vivax.ru'),
]

# кадры, парные к клипам со смены (тот же сетап, что снимает оператор)
PAIRS = {'ex-pads': 19.70, 'ex-pads2': 20.65}

# ─── фото со смены 29.05.2017 ─────────────────────────────────────────────
PHOTOS = [
    ('set-wide', 'IMG_2097.JPG',
     'Площадка: она с тюбиком в руках, камера на плечевом риге, '
     'два софтбокса и панель на стойке'),
    ('set-monitor', 'IMG_2098.JPG',
     'Съёмка крупного плана. На столике у плейбека стоит сам тюбик'),
    ('set-red', 'IMG_2106.JPG', 'Камера смены: RED на штативе'),
    ('set-selfie', 'IMG_2103.JPG', 'Перерыв между дублями'),
]

# сняты на телефон вертикально, поэтому на странице стоят в 9:16
CLIPS = [
    ('bts-pads', 'IMG_2108.MOV', 0.0, 9.03,
     'Работа по лапам: тренер отходит спиной вперёд, камера едет рядом '
     'с рук, вся группа движется вместе с ними'),
]


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(cmd) + '\n' + r.stderr.decode('utf-8', 'ignore')[:800])
    return r


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
    head = ('/* Jost + Inter Tight, self-host для /video/vivax/.\n'
            '   Сгенерировано scripts/vivax-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'jost-intertight.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    cyr = sum(1 for s, _ in blocks if s.startswith('cyrillic'))
    print(f'✓ шрифты: {len(out)} @font-face (кириллических блоков {cyr}), '
          f'скачано файлов {n}')


# ══ 2. склейки ═════════════════════════════════════════════════════════════
def shot_list():
    """Гистограммы по 3×3 блокам, порог адаптивный: пик должен быть втрое
    выше локальной медианы. Простая разница кадров тут не работает — ролик
    снят с рук и внутри планов движение сильнее, чем на части склеек."""
    cap = cv2.VideoCapture(VIDEO)
    feats = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        s = cv2.resize(f, (126, 72), interpolation=cv2.INTER_AREA)
        h = []
        for by in range(3):
            for bx in range(3):
                blk = s[by * 24:(by + 1) * 24, bx * 42:(bx + 1) * 42]
                for c in range(3):
                    hh = cv2.calcHist([blk], [c], None, [16], [0, 256]).ravel()
                    h.append(hh / blk[:, :, 0].size)
        feats.append(np.concatenate(h))
    cap.release()
    F = np.stack(feats)
    n = len(F)
    d = np.abs(np.diff(F, axis=0)).sum(axis=1) / 2 / 9
    cuts = []
    for i in range(n - 1):
        lo, hi = max(0, i - 12), min(n - 1, i + 13)
        loc = np.median(np.delete(d[lo:hi], i - lo))
        if d[i] > 0.16 and d[i] > 3.0 * loc and d[i] == d[max(0, i - 2):i + 3].max():
            cuts.append(i + 1)
    bounds = [0] + cuts + [n]
    shots = [[round(bounds[i] / FPS, 2), round(bounds[i + 1] / FPS, 2)]
             for i in range(len(bounds) - 1)]
    print(f'✓ монтаж: {len(shots)} планов, средний '
          f'{sum(b - a for a, b in shots) / len(shots):.2f} с')
    return shots


# ══ 3. кадры ═══════════════════════════════════════════════════════════════
def sharpest(cap, sec, win):
    """Самый резкий кадр в окне ±win: съёмка с рук, соседние кадры смазаны."""
    a = max(0, int((sec - win) * FPS))
    b = int((sec + win) * FPS)
    best = (-1.0, None, a)
    for fr in range(a, b + 1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, fr)
        ok, f = cap.read()
        if not ok:
            continue
        s = cv2.Laplacian(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        if s > best[0]:
            best = (s, f, fr)
    if best[1] is None:
        sys.exit(f'✗ не прочитался кадр на {sec} с')
    return best


def stills():
    os.makedirs(IMG, exist_ok=True)
    cap = cv2.VideoCapture(VIDEO)
    picked = {}
    for slug, sec, win, what in STILLS:
        _score, frame, fr = sharpest(cap, sec, win)
        picked[slug] = {'sec': round(fr / FPS, 2), 'what': what}
        for suffix, width, q in (('', 1080, 85), ('-m', 720, 84), ('-s', 420, 82)):
            k = width / VW
            dst = os.path.join(IMG, f'{slug}{suffix}.jpg')
            im = frame if k >= 1.0 else cv2.resize(frame, None, fx=k, fy=k,
                                                   interpolation=cv2.INTER_AREA)
            cv2.imwrite(dst, im, [cv2.IMWRITE_JPEG_QUALITY, q])
            webp(dst)
    cap.release()
    print(f'✓ кадры: {len(STILLS)} шт. × 3 размера в mirror/images/vivax/')
    return picked


# ══ 4. звук: где ролик замолкает ═══════════════════════════════════════════
def loudness():
    wav = os.path.join(ROOT, 'scripts', '.vivax.wav')
    sh(['ffmpeg', '-v', 'error', '-y', '-i', VIDEO, '-ac', '1', '-ar', '8000',
        '-f', 'wav', wav])
    w = wave.open(wav)
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    sr = w.getframerate()
    w.close()
    os.remove(wav)
    h = int(sr * 0.25)
    r = np.array([np.sqrt((a[i * h:(i + 1) * h] ** 2).mean())
                  for i in range(len(a) // h)])
    db = np.maximum(20 * np.log10(np.maximum(r, 1e-6)), -60)
    # провал: подряд идущие окна тише -20 дБ при медиане около -12
    quiet = db < -20.0
    runs, s = [], None
    for i, q in enumerate(quiet):
        if q and s is None:
            s = i
        elif not q and s is not None:
            if i - s >= 4:
                runs.append([round(s * 0.25, 2), round(i * 0.25, 2)])
            s = None
    print(f'✓ звук: медиана {np.median(db):.1f} дБ, провалов {len(runs)}: {runs}')
    return [round(float(x), 1) for x in db], runs


# ══ 5. палитра пипеткой ════════════════════════════════════════════════════
def swatch(cap, sec, box, pick):
    """Медиана по пикселям, прошедшим фильтр pick, в окне box кадра на sec."""
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * FPS))
    ok, f = cap.read()
    if not ok:
        sys.exit(f'✗ кадр {sec}')
    x0, y0, x1, y1 = box
    a = f[y0:y1, x0:x1][:, :, ::-1].astype(int)   # BGR → RGB
    m = pick(a)
    px = a[m]
    if len(px) < 50:
        sys.exit(f'✗ палитра: на {sec} с в окне {box} только {len(px)} пикселей')
    lo = np.percentile(px, 25, axis=0).astype(int)
    hi = np.percentile(px, 85, axis=0).astype(int)
    return '#%02X%02X%02X' % tuple(lo), '#%02X%02X%02X' % tuple(hi), int(len(px))


def palette():
    cap = cv2.VideoCapture(VIDEO)
    red = lambda a: (a[..., 0] - a[..., 2] > 50) & (a[..., 0] > 170)
    blue = lambda a: (a[..., 2] - a[..., 0] > 50)
    green = lambda a: (a[..., 1] - a[..., 0] > 30) & (a[..., 1] > 170)
    bar = lambda a: (a[..., 0] - a[..., 1] > 90) & (a[..., 0] > 180)
    out = {}
    out['warm'] = swatch(cap, 6.24, (580, 140, 700, 230), red)
    out['cool'] = swatch(cap, 23.92, (400, 400, 560, 510), blue)
    out['heal'] = swatch(cap, 39.20, (110, 360, 220, 460), green)
    out['brand'] = swatch(cap, 45.00, (300, 290, 760, 330), bar)
    cap.release()
    for k, v in out.items():
        print(f'✓ палитра {k}: {v[0]} → {v[1]} ({v[2]} px)')
    return {k: {'dark': v[0], 'light': v[1]} for k, v in out.items()}


# ══ 5b. шеврон-знак кривыми ════════════════════════════════════════════════
def chevron():
    """Знак VIVAX вынимается контуром, а не рисуется на глаз.

    Кадр 39,72 с: титр «Реабилитация» к этому моменту дорисован целиком
    (раньше, на 39,2 с, у знака ещё не залито остриё, и контур выходит
    с зазубриной). Маска по «зелёности» G - max(R,B): титр лежит на
    расфокусированном сером фоне и отделяется чисто. Берётся самая
    крупная связная область, approxPolyDP 2.2 убирает ступеньки
    антиалиасинга и оставляет 10 точек фигуры."""
    cap = cv2.VideoCapture(VIDEO)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 993)
    ok, f = cap.read()
    cap.release()
    if not ok:
        sys.exit('✗ шеврон: кадр 39,72 с не прочитался')
    sub = f[360:480, 100:230]
    g = sub[..., 1].astype(int) - np.maximum(sub[..., 0], sub[..., 2]).astype(int)
    m = cv2.morphologyEx((g > 16).astype(np.uint8) * 255, cv2.MORPH_CLOSE,
                         np.ones((3, 3), np.uint8))
    num, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    if num > 1:
        k = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        m = ((lab == k) * 255).astype(np.uint8)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    pts = (cv2.approxPolyDP(c, 2.2, True).reshape(-1, 2).astype(float)
           - [x, y]) / max(w, h) * 100
    path = 'M' + ' L'.join(f'{a:.1f} {b:.1f}' for a, b in pts) + ' Z'
    print(f'✓ шеврон: {len(pts)} точек, кроп {w}×{h} px')
    return path


# ══ 6. фото и клипы со смены ═══════════════════════════════════════════════
def bts():
    os.makedirs(IMG, exist_ok=True)
    out = {}
    for slug, fname, what in PHOTOS:
        src = os.path.join(SRC, fname)
        if not os.path.exists(src):
            sys.exit(f'✗ нет исходника {src}')
        im = cv2.imread(src)
        if im is None:
            sys.exit(f'✗ не читается {src}')
        h, w = im.shape[:2]
        for suffix, width, q in (('', 1400, 84), ('-m', 900, 83), ('-s', 480, 82)):
            k = min(1.0, width / w)
            dst = os.path.join(IMG, f'{slug}{suffix}.jpg')
            o = im if k >= 1.0 else cv2.resize(im, None, fx=k, fy=k,
                                               interpolation=cv2.INTER_AREA)
            cv2.imwrite(dst, o, [cv2.IMWRITE_JPEG_QUALITY, q])
            webp(dst)
        out[slug] = {'what': what, 'w': w, 'h': h, 'src': fname}
    print(f'✓ фото смены: {len(PHOTOS)} шт. × 3 размера')
    return out


def clips():
    os.makedirs(VIDEOS, exist_ok=True)
    out = {}
    for slug, fname, ss, dur, what in CLIPS:
        src = os.path.join(SRC, fname)
        if not os.path.exists(src):
            sys.exit(f'✗ нет исходника {src}')
        dst = os.path.join(VIDEOS, f'vivax-{slug}.mp4')
        sh(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur), '-i', src,
            '-vf', 'scale=800:-2', '-c:v', 'libx264', '-crf', '29', '-preset', 'veryslow',
            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', dst])
        # постер клипа в тех же трёх размерах, что и остальные картинки
        raw = os.path.join(IMG, f'{slug}.jpg')
        sh(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss + dur / 2), '-i', src,
            '-frames:v', '1', '-vf', 'scale=1080:-2', '-q:v', '3', raw])
        webp(raw)
        im = cv2.imread(raw)
        for suffix, width, q in (('-m', 720, 84), ('-s', 420, 82)):
            k = width / im.shape[1]
            pdst = os.path.join(IMG, f'{slug}{suffix}.jpg')
            cv2.imwrite(pdst, cv2.resize(im, None, fx=k, fy=k,
                                         interpolation=cv2.INTER_AREA),
                        [cv2.IMWRITE_JPEG_QUALITY, q])
            webp(pdst)
        mb = os.path.getsize(dst) / 1e6
        out[slug] = {'what': what, 'src': fname, 'dur': dur,
                     'url': f'/videos/vivax-{slug}.mp4', 'mb': round(mb, 2)}
        print(f'  {slug}: {dur:.2f} с, {mb:.2f} МБ')
    print(f'✓ клипы смены: {len(CLIPS)} шт. в mirror/videos/')
    return out


# ══ main ═══════════════════════════════════════════════════════════════════
def main():
    args = set(sys.argv[1:])
    everything = not args
    old = json.load(open(MAP, encoding='utf-8')) if os.path.exists(MAP) else {}
    data = dict(old)

    if everything or '--fonts' in args:
        fonts()
    if everything or '--stills' in args:
        data['stills'] = stills()
        data['shots'] = shot_list()
        db, quiet = loudness()
        data['loudness'] = db
        data['quiet'] = quiet
        data['palette'] = palette()
        data['chevron'] = chevron()
    if everything or '--bts' in args:
        data['photos'] = bts()
    if everything or '--clips' in args:
        data['clips'] = clips()

    data['video'] = '/media/vivax-samburskaya.mp4'
    data['duration'] = DURATION
    data['fps'] = FPS
    data['size'] = [VW, VH]
    if data.get('shots'):
        lens = [round(b - a, 2) for a, b in data['shots']]
        # заставка это графика, а не съёмка: её планы (самые длинные в ролике)
        # портят статистику монтажа, поэтому считаем ещё и отдельно по съёмке
        film = [(a, b) for a, b in data['shots'] if b <= END_CARD + .01]
        flens = [round(b - a, 2) for a, b in film]
        data['stats'] = {
            'shots': len(lens),
            'mean': round(sum(lens) / len(lens), 2),
            'min': min(lens),
            'max': max(lens),
            'longest_at': data['shots'][lens.index(max(lens))],
            'film_shots': len(flens),
            'film_mean': round(sum(flens) / len(flens), 2),
            'film_min': min(flens),
            'film_max': max(flens),
            'film_longest_at': list(film[flens.index(max(flens))]),
            'endcard_at': END_CARD,
        }
    json.dump(data, open(MAP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'✓ карта: {os.path.relpath(MAP, ROOT)}')


if __name__ == '__main__':
    main()
