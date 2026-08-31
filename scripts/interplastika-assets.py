#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Обзорный ролик выставки интерпластика» (/video/interplastika/).

Материал ровно один: сам ролик media/interplastika.mp4 (2:12, 1280×720, 25 fps),
на хостинге он же лежит как /media/interplastica-messe-duesseldorf.mp4.
Никаких фотографий, брифов и макетов по кейсу не сохранилось, поэтому вся
фактура страницы снята с ролика алгоритмом:

  1. Шрифты Jura + Nunito Sans локально (mirror/fonts/jura-nunito.css).
  2. Кадры: титры, стенды экспонентов, витрины сырья, изделия, план площадки.
     Из каждого окна берётся самый резкий кадр — съёмка с рук, соседние
     кадры смазаны, и на смазанном логотип стенда не читается.
  3. Разбор монтажа: склейки по кадровой разнице, длины планов, проверка
     ритмической сетки (ролик смонтирован на бит) и темп по автокорреляции
     спектрального потока звуковой дорожки.
  4. Палитра снята с финального кадра — плана Экспоцентра: синим на нём
     размечена интерпластика, красным upakovka.

Всё считанное уходит в scripts/a2/interplastika_map.json,
страницу собирает scripts/a2/gen_interplastika.py.

Запуск: python3 scripts/interplastika-assets.py [--fonts] [--stills] [--probe]
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
VIDEO = os.path.join(ROOT, 'media', 'interplastika.mp4')
IMG = os.path.join(MIRROR, 'images', 'interplastika')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
MAP = os.path.join(ROOT, 'scripts', 'a2', 'interplastika_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Jura:wght@400;500;600;700'
      '&family=Nunito+Sans:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

FPS = 25.0
VW, VH = 1280, 720

# ─── кадры: (слаг, секунда, окно поиска резкого кадра, что в кадре) ────────
# секунды выверены по нарезке ролика на планы, окно ±0.5 с не выходит
# за границы своего плана
STILLS = [
    # шапка и общие планы
    ('hall-engel', 102.4, 0.5, 'Проход между стендами: зелёные термопласт-автоматы ENGEL, зал полон'),
    ('roof', 86.2, 0.4, 'Ферма перекрытия Экспоцентра изнутри'),
    ('fountain', 88.0, 0.4, 'Фонтан во внутреннем дворе Экспоцентра'),
    ('crowd', 94.5, 0.4, 'Поток посетителей по галерее между павильонами'),
    ('escalator', 98.0, 0.4, 'Эскалатор на входе в павильон'),

    # регистрация
    ('reg-desk', 20.6, 0.4, 'Стойка регистрации: бейджи выдают на входе'),
    ('reg-form', 18.4, 0.4, 'Заполнение анкеты участника на стойке'),
    ('reg-badge', 24.2, 0.4, 'Печать бейджа посетителя'),

    # стенды: сырьё
    ('sibur', 70.4, 0.4, 'Стенд СИБУРа: «Формула будущего» на чёрной стене'),
    ('sibur-wide', 68.0, 0.4, 'Стенд СИБУРа общим планом, световые линии по потолку'),
    ('nknh', 116.6, 0.4, 'Стенд «Нижнекамскнефтехима» с макетом производства'),
    ('kos', 119.6, 0.25, 'Стенд «Казаньоргсинтеза»: знак завода и продуктовая линейка на стене'),
    ('kos-line', 120.4, 0.3, 'Витрины с гранулятом и чёрные ПЭ-трубы на стенде'),
    ('bayer', 75.6, 0.4, 'Стенд Bayer MaterialScience: Sharing Dreams, Sharing Values'),
    ('basf', 79.7, 0.4, 'Стенд BASF: Color Solutions и мастербатчи'),
    ('dow', 113.9, 0.4, 'Стенд Dow'),

    # стенды: компаунды и добавки
    ('mcpp', 63.3, 0.4, 'Стенд Mitsubishi Chemical Performance Polymers со списком марок'),
    ('marvyflo', 65.1, 0.4, 'Переговоры на стенде Marvyflo, порошок для slush molding'),
    ('polyplastic', 46.9, 0.4, 'Арка стенда «Полипластика»: «Партнёр, которому можно доверять»'),
    ('polumikronize', 81.0, 0.4, 'Стенд Polumikronize, разговор с посетителем'),

    # стенды: машины
    ('engel', 41.8, 0.4, 'Стенд ENGEL'),
    ('sumitomo', 32.5, 0.15, 'Проход у стенда Sumitomo Demag'),
    ('haitian', 104.2, 0.4, 'Каталоги Haitian на стойке'),
    ('kautex', 47.8, 0.4, 'Стенд Kautex: Get electrified by Kautex'),
    ('geiss', 125.9, 0.4, 'Термоформовочная машина GEISS AG'),
    ('cama', 126.6, 0.4, 'Упаковочный автомат CAMA'),
    ('press', 33.6, 0.4, 'Пульт термопласт-автомата с циклограммой смыкания'),
    ('press-screen', 34.4, 0.3, 'Экран машины: параметры закрытия и открытия формы'),

    # переработка и изделия
    ('crates-robot', 38.7, 0.4, 'Робот снимает отлитые ящики с термопласт-автомата'),
    ('crates', 39.9, 0.2, 'Готовые ящики уходят по конвейеру'),
    ('headlight', 84.2, 0.4, 'Автомобильная фара в витрине применений'),
    ('applications', 85.1, 0.4, 'Витрина «Применения»: изделия из инженерных пластиков'),
    ('phone-shells', 123.3, 0.4, 'Корпуса из поликарбоната на конвейере стенда'),
    ('bottles', 127.1, 0.3, 'Линия розлива: бутылки идут по транспортёру'),
    ('bosch', 50.7, 0.3, 'Стенд Bosch: «Разработано для жизни»'),
    ('bosch-wall', 51.3, 0.25, 'Знак Bosch на стене стенда крупно'),
    ('extruder', 55.2, 0.4, 'Экструзионная линия в работе'),
    ('lab', 57.5, 0.4, 'Лабораторная линия на стенде'),
    ('medical', 90.9, 0.4, 'Стенд медицинских полимерных изделий'),

    # витрины сырья крупно
    ('granule-hdpe', 121.2, 0.15, 'Витрина с полиэтиленом HDPE, табличка марки ПЭ2НТ22-12'),
    ('granule-pc', 122.4, 0.3, 'Витрина с поликарбонатом, табличка PC-007 UL'),
    ('granule-row', 118.4, 0.4, 'Ряд витрин с гранулятом на стенде'),

    # деловая программа и навигация
    ('forum', 43.2, 0.4, 'Зал деловой программы: доклад при полном зале'),
    ('forum-stage', 44.1, 0.4, 'Сцена деловой программы'),
    ('raw-materials', 107.8, 0.4, 'Секция raw materials: доклад под фирменной плашкой раздела'),
    ('germany', 124.2, 0.4, 'Национальный павильон Германии'),
    ('plan', 130.1, 0.6, 'План Экспоцентра: синим интерпластика, красным upakovka'),
    ('plan-early', 28.6, 0.4, 'Тот же план в начале ролика'),
    ('meeting', 112.1, 0.4, 'Рукопожатие на стенде'),
    ('tablet', 45.5, 0.4, 'Посетитель снимает данные со стенда на планшет'),
]

# ─── экспоненты, попавшие в кадр: ступень передела → карточки ─────────────
# ступень определена по тому, что компания показывала на своём стенде,
# тайм-код — секунда, на которую перематывается плеер
CHAIN = [
    ('raw', 'Сырьё', 'Полимеры в гранулах: полиэтилен, полипропилен, '
     'поликарбонат, стирольные пластики', [
        ('sibur', 'СИБУР', 'Формула будущего', 66.9, 'sibur'),
        ('nknh', 'Нижнекамскнефтехим', 'Каучуки и полиолефины', 116.7, 'nknh'),
        ('kos', 'Казаньоргсинтез', 'ПНД, ПВД, поликарбонаты, бисфенол-А', 118.5, 'kos'),
        ('bayer', 'Bayer MaterialScience', 'Поликарбонаты и полиуретаны', 72.2, 'bayer'),
        ('basf', 'BASF', 'Color Solutions, мастербатчи', 78.4, 'basf'),
        ('dow', 'Dow', 'Полиолефины и упаковочные решения', 114.0, 'dow'),
    ]),
    ('compound', 'Компаунды и добавки', 'Готовые рецептуры под конкретное '
     'изделие: эластомеры, красители, наполнители', [
        ('mcpp', 'Mitsubishi Chemical PP', 'Линейка марок от TEFABLOC до FORZEAS', 63.4, 'mcpp'),
        ('marvyflo', 'Marvyflo', 'Порошок для slush molding', 65.1, 'marvyflo'),
        ('polyplastic', 'Полипластик', 'Композиции и трубные марки', 46.5, 'polyplastic'),
        ('polumikronize', 'Polumikronize', 'Микронизированные наполнители', 80.7, 'polumikronize'),
    ]),
    ('machine', 'Машины', 'Термопласт-автоматы, экструзия, термоформование, '
     'упаковочные линии', [
        ('engel', 'ENGEL', 'Термопласт-автоматы, работают прямо на стенде', 100.6, 'engel'),
        ('sumitomo', 'Sumitomo Demag', 'Литьевые машины', 32.3, 'sumitomo'),
        ('haitian', 'Haitian', 'Литьевые машины', 104.0, 'haitian'),
        ('kautex', 'Kautex', 'Экструзионно-выдувное оборудование', 47.5, 'kautex'),
        ('geiss', 'GEISS AG', 'Термоформование крупных деталей', 125.7, 'geiss'),
        ('cama', 'CAMA', 'Упаковочные автоматы', 126.4, 'cama'),
    ]),
    ('product', 'Изделия', 'То, ради чего вся цепочка: детали, тара, корпуса, '
     'упаковка', [
        ('crates', 'Ящики', 'Робот снимает отливку с машины и ставит на конвейер', 38.4, 'crates-robot'),
        ('headlight', 'Автокомпоненты', 'Фара и корпусные детали в витрине применений', 84.0, 'headlight'),
        ('phone-shells', 'Корпуса', 'Поликарбонатные корпуса идут по конвейеру', 123.0, 'phone-shells'),
        ('bosch', 'Bosch', 'Бытовая техника из тех же материалов', 50.0, 'bosch'),
        ('bottles', 'Тара', 'Бутылки на линии розлива', 126.9, 'bottles'),
    ]),
]

# ─── что показывает витрина сырья (таблички прочитаны с кадров) ───────────
GRANULES = [
    ('Полиэтилен', 'ПЭ2НТ22-12 · HDPE', 'granule-hdpe',
     'Полиэтилен высокой плотности: трубы, тара, плёнка, ящики'),
    ('Поликарбонат', 'PC-007 UL', 'granule-pc',
     'Прозрачный конструкционный пластик: корпуса, оптика, остекление'),
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
    head = ('/* Jura + Nunito Sans, self-host для /video/interplastika/.\n'
            '   Сгенерировано scripts/interplastika-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'jura-nunito.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    cyr = sum(1 for s, _ in blocks if s.startswith('cyrillic'))
    print(f'✓ шрифты: {len(out)} @font-face (кириллических блоков {cyr}), '
          f'скачано файлов {n}')


# ══ 2. кадры ═══════════════════════════════════════════════════════════════
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
    for slug, sec, win, _what in STILLS:
        score, frame, fr = sharpest(cap, sec, win)
        picked[slug] = round(fr / FPS, 2)
        for suffix, width, q in (('', 1100, 84), ('-m', 800, 83), ('-s', 480, 82)):
            k = width / VW
            dst = os.path.join(IMG, f'{slug}{suffix}.jpg')
            im = frame if k >= 1.0 else cv2.resize(frame, None, fx=k, fy=k,
                                                   interpolation=cv2.INTER_AREA)
            cv2.imwrite(dst, im, [cv2.IMWRITE_JPEG_QUALITY, q])
            webp(dst)
    cap.release()
    print(f'✓ кадры: {len(STILLS)} шт. × 3 размера в mirror/images/interplastika/')
    return picked


# ══ 3. разбор монтажа ══════════════════════════════════════════════════════
def shot_list():
    """Склейки по разнице соседних кадров. Съёмка с рук и быстрые панорамы
    дают ложные пики, поэтому порог высокий, а слишком короткие куски
    приклеиваются к предыдущему плану."""
    cap = cv2.VideoCapture(VIDEO)
    prev, diff = None, []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        s = cv2.resize(f, (160, 90)).astype(np.float32)
        if prev is not None:
            diff.append(float(np.abs(s - prev).mean()))
        prev = s
    cap.release()
    n = len(diff) + 1
    cuts = []
    for j, v in enumerate(diff):
        if v > 30 and (not cuts or j + 1 - cuts[-1] >= 10):
            cuts.append(j + 1)
    bounds = [0] + cuts + [n]
    shots = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    shots = [(a, b) for a, b in shots if b - a >= 10]
    return shots, n


def tempo():
    """Темп музыки: спектральный поток → автокорреляция с гармониками.
    Ролик смонтирован на бит, и это слышно в звуке; отдельно тот же шаг
    ищется по длинам планов, см. grid_step()."""
    raw = subprocess.run(
        ['ffmpeg', '-v', 'error', '-i', VIDEO, '-ac', '1', '-ar', '22050',
         '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    hop, win = 128, 1024
    m = (len(x) - win) // hop
    frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop][:m]
    S = np.abs(np.fft.rfft(frames * np.hanning(win), axis=1))
    flux = np.maximum(0, np.diff(S, axis=0)).sum(1)
    flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    ac = np.correlate(flux, flux, 'full')[len(flux) - 1:]
    sr = 22050 / hop

    def score(bpm):
        lag = 60.0 / bpm * sr
        s = 0.0
        for k in (1, 2, 4):                      # доля, половина такта, такт
            i = k * lag
            i0 = int(i)
            if i0 + 1 >= len(ac):
                return -1e18
            s += (ac[i0] * (1 - (i - i0)) + ac[i0 + 1] * (i - i0)) / k
        return s

    grid = np.arange(110.0, 170.0, 0.02)
    return round(float(grid[int(np.argmax([score(b) for b in grid]))]), 1)


def grid_step(lengths):
    """Шаг монтажной сетки — независимо от звука, только по длинам планов:
    ищем период, на который ложится максимум планов."""
    best = (0, 1.0, 0.0)
    for T in np.arange(0.30, 0.80, 0.002):
        r = np.abs(lengths / T - np.round(lengths / T))
        ok = int((r < 0.15).sum())
        err = float(r[r < 0.15].mean()) if ok else 1.0
        if (ok, -err) > (best[0], -best[1]):
            best = (ok, err, float(T))
    return round(best[2], 3), best[0]


def palette():
    """Цвета плана площадки: синим на нём размечена интерпластика,
    красным — upakovka. Кадр снят при слабом свете, поэтому берём не
    среднее, а самый насыщенный тон каждой зоны и поднимаем яркость
    до печатного уровня."""
    cap = cv2.VideoCapture(VIDEO)
    _, frame, _ = sharpest(cap, 128.6, 0.8)
    cap.release()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def zone(y0, y1, x0, x1):
        h = hsv[y0:y1, x0:x1].reshape(-1, 3).astype(np.float32)
        h = h[h[:, 1] > 60]
        if not len(h):
            return None
        med = np.median(h, axis=0)
        med[2] = min(255, med[2] * 1.35)          # компенсация недосвета зала
        med[1] = min(255, med[1] * 1.2)
        bgr = cv2.cvtColor(np.uint8([[med]]), cv2.COLOR_HSV2BGR)[0][0]
        return '#%02X%02X%02X' % (int(bgr[2]), int(bgr[1]), int(bgr[0]))

    return {
        'interplastica': zone(300, 340, 900, 990),   # ПАВ.1, синий
        'upakovka': zone(200, 250, 640, 780),        # ПАВ.2, красный
    }


def probe(picked):
    shots, frames = shot_list()
    lengths = np.array([b - a for a, b in shots], dtype=float) / FPS
    bpm = tempo()
    beat, on_grid = grid_step(lengths)
    data = {
        'video': '/media/interplastica-messe-duesseldorf.mp4',
        'duration': round(frames / FPS, 2),
        'fps': FPS,
        'shots': [[round(a / FPS, 2), round(b / FPS, 2)] for a, b in shots],
        'shot_count': len(shots),
        'shot_mean': round(float(lengths.mean()), 2),
        'shot_median': round(float(np.median(lengths)), 2),
        'shot_min': round(float(lengths.min()), 2),
        'shot_max': round(float(lengths.max()), 2),
        'bpm': bpm,
        'beat': beat,
        'beat_bpm': round(60.0 / beat, 1),
        'on_grid': on_grid,
        'titles_until': round(shots[1][0] / FPS, 2) if len(shots) > 1 else None,
        'palette': palette(),
        'stills': {s: {'sec': picked.get(s, sec), 'what': what}
                   for s, sec, _w, what in STILLS},
        'chain': [{'id': cid, 'title': t, 'lead': lead,
                   'items': [{'id': i, 'name': nm, 'note': note,
                              'sec': sec, 'still': still}
                             for i, nm, note, sec, still in items]}
                  for cid, t, lead, items in CHAIN],
        'granules': [{'name': n, 'grade': g, 'still': s, 'note': note}
                     for n, g, s, note in GRANULES],
    }
    json.dump(data, open(MAP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'✓ разбор: {len(shots)} планов, средний {data["shot_mean"]} с, '
          f'темп по звуку {bpm} BPM, шаг сетки {beat} с '
          f'({data["beat_bpm"]} BPM), на сетке {on_grid} из {len(shots)}')
    print(f'  палитра плана: {data["palette"]}')
    return data


def main():
    flags = set(sys.argv[1:])
    allf = not flags
    picked = {}
    if allf or '--fonts' in flags:
        fonts()
    if allf or '--stills' in flags:
        picked = stills()
    if allf or '--probe' in flags:
        if not picked and os.path.exists(MAP):
            old = json.load(open(MAP, encoding='utf-8'))
            picked = {k: v['sec'] for k, v in old.get('stills', {}).items()}
        probe(picked)


if __name__ == '__main__':
    main()
