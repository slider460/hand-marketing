#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «3D-визуализация решений Eaton» (/creative/eaton/visual/).

Исходники — три печатных плаката 2017 года, 300 dpi (папка ~/Downloads/jpg):
ЦОД и коммерческий объект 9449×7087 px (800×600 мм), промышленный объект
7087×9449 px (600×800 мм). На каждом — изометрический разрез объекта на синем
градиенте и печатный слой поверх него: круглые фото оборудования, подписи
и белые линии-выноски.

Главный приём кейса: печатный слой снимается с плаката алгоритмом, остаётся
чистая подложка (здание на градиенте), а выноски пересобираются на странице
живыми. Поэтому скрипт не просто режет картинки, а разбирает плакат:

  1. Шрифты Play + Roboto (и Roboto Condensed) из Google Fonts кладёт локально
     (mirror/fonts/files/ + mirror/fonts/play-roboto.css). Внешних CDN на сайте
     нет принципиально. Play нарисован по чертёжной технической антикве — держит
     заголовки и цифры; Roboto — ближайший к Helvetica плакатов гротеск с полной
     кириллицей, узкий Roboto Condensed повторяет плотные списки характеристик.
     Archivo и Barlow, взятые сначала, кириллицы не содержат вовсе.
  2. Отделяет силуэт здания от печатного слоя (синева фона против нейтральных
     пикселей рендера), собирает маску кружков, подписей и линий и заливает её
     push-pull интерполяцией по градиенту — получается plate-*.jpg.
  3. Режет каждый кружок оборудования в отдельный png с альфой — это
     «библиотека моделей» на странице.
  4. Снимает геометрию: центры кружков и точки, куда упирались линии-выноски
     на здании → scripts/a2/eaton_visual_map.json (нормированные координаты).
  5. Кропы 1:1 из оригинала для блока про печатный масштаб.
  6. Делает .webp рядом с каждым jpg/png.

Запуск: python3 scripts/eaton-visual-assets.py [--fonts] [--plates] [--crops]
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
IMG = os.path.join(MIRROR, 'images', 'eaton-visual')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
SRC = os.path.expanduser('~/Downloads/jpg')
MAP_JSON = os.path.join(ROOT, 'scripts', 'a2', 'eaton_visual_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Play:wght@400;700'
      '&family=Roboto:wght@400;500;700'
      '&family=Roboto+Condensed:wght@500;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── три плаката ────────────────────────────────────────────────────────────
# (slug, файл, ширина plate на выходе, ширина poster на выходе)
POSTERS = [
    ('dc',         'Eaton_Poster додоеланный-01.jpg', 2200, 2000),
    ('commercial', 'Eaton_Poster додоеланный-02.jpg', 2200, 2000),
    ('industry',   'Eaton_Poster додоеланный-03.jpg', 1800, 1700),
]

# Кружки оборудования: какой продукт где стоит. Координаты — доля от размера
# плаката, снятые HoughCircles; скрипт передетектит круги и привяжет их к этим
# точкам по близости, поэтому здесь достаточно ориентира.
CIRCLES = {
    'dc': [
        ('racks',      0.072, 0.240),
        ('ups',        0.804, 0.244),
        ('xenergy',    0.804, 0.435),
        ('xiria',      0.804, 0.612),
        ('monitoring', 0.072, 0.812),
        ('exit',       0.577, 0.812),
        ('busway',     0.804, 0.813),
    ],
    'commercial': [
        ('xstart',     0.081, 0.227),
        ('powerxl',    0.550, 0.225),
        ('exit',       0.817, 0.229),
        ('xiria',      0.081, 0.424),
        ('busway',     0.816, 0.595),
        ('xenergy',    0.081, 0.713),
        ('towers',     0.817, 0.807),
        ('ups',        0.262, 0.864),
    ],
    'industry': [
        ('xenergy',    0.266, 0.233),
        ('xstart',     0.630, 0.199),
        ('ups',        0.106, 0.376),
        ('xiria',      0.634, 0.418),
        ('exit',       0.106, 0.534),
    ],
}

# С какого плаката резать кружок в библиотеку (где фото крупнее и чище)
CHIP_FROM = {
    'racks': 'dc', 'ups': 'industry', 'xenergy': 'industry', 'xiria': 'industry',
    'monitoring': 'dc', 'exit': 'industry', 'busway': 'dc', 'xstart': 'industry',
    'powerxl': 'commercial', 'towers': 'commercial',
}

WORK_W = 3000          # рабочее разрешение разбора
SAT_TH = 70            # порог насыщенности: фон плаката синий, рендер — нет


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(str(c) for c in cmd) + '\n' + r.stderr[-800:])


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req).read()


def imread(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)


def webp(path):
    """Тот же cwebp с теми же ключами, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def save(path, img, quality=88):
    if path.endswith('.png'):
        cv2.imwrite(path, img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    else:
        cv2.imwrite(path, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    webp(path)


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
    head = ('/* Play + Roboto, self-host для /creative/eaton/visual/.\n'
            '   Сгенерировано scripts/eaton-visual-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'play-roboto.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


# ─── разбор плаката ─────────────────────────────────────────────────────────

def push_pull(img, hole):
    """Заливка дыр по гладкому градиенту: пирамида вниз с весами, потом вверх.

    Телеа на кружке диаметром в 250 px мажет, а фон плаката — гладкий градиент,
    поэтому честнее восстановить его интерполяцией по пирамиде.
    """
    known = (hole == 0).astype(np.float32)
    cur_i = img.astype(np.float32) * known[..., None]
    cur_m = known
    pyr_i, pyr_m = [cur_i], [cur_m]
    while min(pyr_m[-1].shape[:2]) > 4:
        pyr_i.append(cv2.pyrDown(pyr_i[-1]))
        pyr_m.append(cv2.pyrDown(pyr_m[-1]))
    fill = pyr_i[-1] / np.maximum(pyr_m[-1], 1e-5)[..., None]
    for k in range(len(pyr_i) - 2, -1, -1):
        h, w = pyr_m[k].shape[:2]
        up = cv2.resize(fill, (w, h), interpolation=cv2.INTER_LINEAR)
        m = pyr_m[k]
        known_px = (m > 0.55)[..., None]
        avg = pyr_i[k] / np.maximum(m, 1e-5)[..., None]
        fill = np.where(known_px, avg, up)
    soft = cv2.GaussianBlur(hole.astype(np.float32) / 255.0, (0, 0), 3)[..., None]
    return np.clip(img.astype(np.float32) * (1 - soft) + fill * soft, 0, 255).astype(np.uint8)


def building_mask(work, circles):
    """Силуэт здания: крупнейшее не-синее пятно, залитое по внешнему контуру.

    Кружки печатного слоя выбиваем заранее: иначе круг прирастает к зданию
    через свою линию-выноску и попадает внутрь силуэта.
    """
    # Фон — насыщенный синий (S≈150), рендер — почти серый (S≈0…25).
    # Порог по «синеве» здесь врал: светлые стены здания тоже голубоватые.
    sat = cv2.cvtColor(work, cv2.COLOR_BGR2HSV)[..., 1]
    bg = (sat > SAT_TH).astype(np.uint8) * 255
    bg = cv2.morphologyEx(bg, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    nonbg = 255 - bg
    for _, cx, cy, rr in circles:
        cv2.circle(nonbg, (cx, cy), int(rr * 1.25), 0, cv2.FILLED)
    h, w = work.shape[:2]
    er = cv2.erode(nonbg, np.ones((13, 13), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(er, 8)
    # здание — все крупные куски рендера ниже белой шапки: у гипермаркета
    # левое крыло отделено тонкой стеной и в одну компоненту не сходится
    seed = np.zeros_like(er)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] > h * w * 0.004 and stats[i, cv2.CC_STAT_TOP] > h * 0.12:
            seed[lab == i] = 255
    # геодезическое восстановление внутри nonbg + заливка контуров
    k = np.ones((5, 5), np.uint8)
    prev, cur = None, seed
    for _ in range(60):
        cur = cv2.bitwise_and(cv2.dilate(cur, k, iterations=3), nonbg)
        if prev is not None and cv2.countNonZero(cv2.absdiff(cur, prev)) == 0:
            break
        prev = cur
    cur = cv2.morphologyEx(cur, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    cnts, _ = cv2.findContours(cur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(cur)
    keep = [c for c in cnts if cv2.contourArea(c) > h * w * 0.004]
    cv2.drawContours(filled, keep, -1, 255, cv2.FILLED)
    return nonbg, filled


def header_bottom(work):
    """Нижняя граница белой шапки плаката."""
    blue_rows = ((cv2.cvtColor(work, cv2.COLOR_BGR2HSV)[..., 1] > SAT_TH).mean(axis=1))
    for y in range(work.shape[0]):
        if blue_rows[y] > 0.5:
            return y
    return 0


def detect_circles(work, expect):
    """Круги печатного слоя + привязка к списку продуктов."""
    g = cv2.medianBlur(cv2.cvtColor(work, cv2.COLOR_BGR2GRAY), 5)
    rmin = int(work.shape[1] * 0.030)
    rmax = int(work.shape[1] * 0.075)
    c = cv2.HoughCircles(g, cv2.HOUGH_GRADIENT, dp=1, minDist=int(work.shape[1] * 0.04),
                         param1=120, param2=60, minRadius=rmin, maxRadius=rmax)
    found = np.round(c[0]).astype(int) if c is not None else []
    out = []
    h, w = work.shape[:2]
    for key, nx, ny in expect:
        px, py = nx * w, ny * h
        best = min(found, key=lambda t: (t[0] - px) ** 2 + (t[1] - py) ** 2)
        d = ((best[0] - px) ** 2 + (best[1] - py) ** 2) ** 0.5
        if d > w * 0.03:
            sys.exit(f'✗ круг {key}: ближайший найденный в {d:.0f}px от ожидаемого')
        out.append((key, int(best[0]), int(best[1]), int(best[2])))
    return out


def print_layer(work, build, top):
    """Печатный слой = всё, что отклоняется от гладкого фонового градиента.

    Подписи на плакатах набраны тёмно-синим по синему, порог «синевы» их не
    ловит. Зато медиана большим окном восстанавливает чистый градиент, и текст,
    плашки и линии видны как отклонение от него.
    """
    outside = 255 - cv2.dilate(build, np.ones((9, 9), np.uint8))
    outside[:top + 2, :] = 0
    med = cv2.medianBlur(work, 41)
    diff = np.max(cv2.absdiff(work, med), axis=2)
    layer = ((diff > 6) & (outside > 0)).astype(np.uint8) * 255
    return cv2.morphologyEx(layer, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))


def leader_lines(work):
    """Линии-выноски целиком: и на фоне, и там, где они лежат поверх рендера.

    Ключ — печать чисто белым: линия ровно 255, а самая светлая стена рендера
    не дотягивает до 250. Открытие ядром 9×9 съедает линию и оставляет
    плоскости, разница даёт тонкие структуры; дальше фильтр по вытянутости.
    """
    w = work.shape[1]
    pure = (work.min(axis=2) >= 250).astype(np.uint8) * 255
    flat = cv2.dilate(cv2.morphologyEx(pure, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)),
                      np.ones((3, 3), np.uint8))
    thin = cv2.bitwise_and(pure, 255 - flat)
    thin = cv2.morphologyEx(thin, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(thin, 8)
    lines = np.zeros_like(thin)
    for i in range(1, n):
        bw, bh, area = stats[i, 2], stats[i, 3], stats[i, 4]
        if max(bw, bh) > w * 0.02 and area < max(bw, bh) * 12:
            lines[lab == i] = 255
    return lines


def anchor_points(lines, build, circles, shape):
    """Куда указывала печатная выноска: дальний от кружка конец её линии.

    Берём точку внутри силуэта здания — иначе якорь садится на внешнюю стену
    или уезжает в текст, если линия слиплась с подписью.
    """
    h, w = shape
    n, lab, _, _ = cv2.connectedComponentsWithStats(lines, 8)
    comps = []
    for i in range(1, n):
        ys, xs = np.nonzero(lab == i)
        comps.append(np.stack([xs, ys], axis=1))
    inside = cv2.erode(build, np.ones((7, 7), np.uint8))
    # годятся только компоненты, которые доходят до здания: рядом с кружком
    # часто оказывается блок подписи, и он выигрывал по расстоянию
    reach = [(pts, pts[inside[pts[:, 1], pts[:, 0]] > 0]) for pts in comps]
    reach = [(p, d) for p, d in reach if len(d)]
    anchors = {}
    for key, cx, cy, r in circles:
        best, best_d = None, 1e18
        for pts, deep in reach:
            d = np.min((pts[:, 0] - cx) ** 2 + (pts[:, 1] - cy) ** 2)
            if d < best_d:
                best_d, best = d, deep
        if best is None or best_d > (r * 2.4) ** 2:
            anchors[key] = None
            continue
        far = (best[:, 0] - cx) ** 2 + (best[:, 1] - cy) ** 2
        px, py = best[int(np.argmax(far))]
        anchors[key] = (float(px / w), float(py / h))
    return anchors


def inpaint_patches(img, mask, radius):
    """Телеа по кускам: на полном кадре 3000 px он считается минутами."""
    out = img.copy()
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    pad = radius * 4
    for i in range(1, n):
        x, y, bw, bh, _ = stats[i]
        x0, y0 = max(0, x - pad), max(0, y - pad)
        x1, y1 = min(img.shape[1], x + bw + pad), min(img.shape[0], y + bh + pad)
        sub = out[y0:y1, x0:x1]
        m = ((lab[y0:y1, x0:x1] == i).astype(np.uint8)) * 255
        out[y0:y1, x0:x1] = cv2.inpaint(sub, m, radius, cv2.INPAINT_TELEA)
    return out


def lines_over_render(lines, build):
    """Куски выносок, лежащие поверх самого здания: их заливаем Телеа —
    стены и пол плоские, шва не видно."""
    over = cv2.bitwise_and(lines, cv2.erode(build, np.ones((5, 5), np.uint8)))
    return cv2.dilate(over, np.ones((5, 5), np.uint8))


# Якоря, снятые с плаката глазами: у правой колонки ЦОД линия-выноска идёт
# впритык к блоку подписи, и трассировщик уводит её в текст. Доли всего кадра.
ANCHOR_FIX = {
    'dc': {
        'ups':     (0.578, 0.245),   # чёрные шкафы ИБП в дальней комнате
        'xenergy': (0.669, 0.320),   # ряд щитов в электрощитовой
        'xiria':   (0.669, 0.374),   # ячейка КРУ рядом с щитовой
        'busway':  (0.639, 0.460),   # шинопровод над машинным залом
    },
}

# Печатные плашки, налезающие на само здание: убрать их фоном нельзя,
# они лежат поверх рендера. Прямоугольники в долях готовой подложки.
OVERLAP = {
    'commercial': [(0.135, 0.610, 0.265, 0.665)],   # шильд «щиты xEnergy»
}


def plates():
    os.makedirs(IMG, exist_ok=True)
    geo = {}
    for slug, fname, plate_w, poster_w in POSTERS:
        src = imread(os.path.join(SRC, fname))
        H, W = src.shape[:2]
        work = cv2.resize(src, (WORK_W, int(H * WORK_W / W)), interpolation=cv2.INTER_AREA)
        h, w = work.shape[:2]

        circles = detect_circles(work, CIRCLES[slug])
        nonbg, build = building_mask(work, circles)
        top = header_bottom(work)
        layer = print_layer(work, build, top)
        lines = leader_lines(work)
        over = lines_over_render(lines, build)
        anchors = anchor_points(lines, build, circles, (h, w))
        anchors.update(ANCHOR_FIX.get(slug, {}))

        # Печатный слой не вычищаем по букве, а пересобираем весь фон вне
        # здания: он и в оригинале гладкий (градиент плюс мягкие пятна света),
        # поэтому реконструкция ничего не теряет, зато не оставляет призраков.
        rough = layer.copy()
        for _, cx, cy, r in circles:
            cv2.circle(rough, (cx, cy), int(r * 1.07), 255, cv2.FILLED)
        rough[:top + 4, :] = 0
        # внутри плотного блока текста медиана берёт цвет самих букв, и такие
        # пиксели остаются «известными»: закрываем блок целиком, иначе после
        # блюра на их месте висит светлое облако
        rough = cv2.morphologyEx(rough, cv2.MORPH_CLOSE, np.ones((45, 45), np.uint8))
        rough = cv2.dilate(rough, np.ones((21, 21), np.uint8))
        rough = cv2.bitwise_and(rough, 255 - cv2.erode(build, np.ones((3, 3), np.uint8)))

        # фон восстанавливаем и под зданием тоже, иначе блюр размажет белые
        # стены наружу и вокруг объекта повиснет ореол
        hole = cv2.bitwise_or(rough, cv2.dilate(build, np.ones((9, 9), np.uint8)))
        field = cv2.GaussianBlur(push_pull(work, hole), (0, 0), 18)
        keep = cv2.GaussianBlur(build.astype(np.float32) / 255.0, (0, 0), 1.6)[..., None]
        clean = np.clip(work * keep + field * (1 - keep), 0, 255).astype(np.uint8)

        # печатное поверх рендера: линии-выноски и налезающие плашки
        ph_full = h - top
        for x0, y0, x1, y1 in OVERLAP.get(slug, []):
            cv2.rectangle(over, (int(x0 * w), top + int(y0 * ph_full)),
                          (int(x1 * w), top + int(y1 * ph_full)), 255, cv2.FILLED)
        clean = inpaint_patches(clean, over, 6)
        clean = clean[top:, :]

        # геометрия в координатах чистой подложки
        ph = h - top
        items = []
        for key, cx, cy, r in circles:
            a = anchors.get(key)
            items.append({
                'key': key,
                'circle': [round(cx / w, 4), round((cy - top) / ph, 4)],
                'r': round(r / w, 4),
                'anchor': [round(a[0], 4), round((a[1] * h - top) / ph, 4)] if a else None,
            })
        geo[slug] = {'plate': [w, ph], 'ratio': round(w / ph, 4), 'items': items}

        out = cv2.resize(clean, (plate_w, int(ph * plate_w / w)), interpolation=cv2.INTER_AREA)
        save(os.path.join(IMG, f'plate-{slug}.jpg'), out, 90)

        poster = cv2.resize(src, (poster_w, int(H * poster_w / W)), interpolation=cv2.INTER_AREA)
        save(os.path.join(IMG, f'poster-{slug}.jpg'), poster, 88)
        print(f'✓ {slug}: подложка {out.shape[1]}×{out.shape[0]}, '
              f'выносок {len(items)}, якорей {sum(1 for i in items if i["anchor"])}')

        # кружки-фишки в библиотеку
        for key, cx, cy, r in circles:
            if CHIP_FROM.get(key) != slug:
                continue
            k = W / w
            X, Y, R = int(cx * k), int(cy * k), int(r * k)
            pad = int(R * 1.02)
            crop = src[max(0, Y - pad):Y + pad, max(0, X - pad):X + pad]
            size = 440
            crop = cv2.resize(crop, (size, size), interpolation=cv2.INTER_AREA)
            alpha = np.zeros((size, size), np.uint8)
            cv2.circle(alpha, (size // 2, size // 2), int(size / 2 * 0.985), 255, cv2.FILLED)
            alpha = cv2.GaussianBlur(alpha, (0, 0), 1.2)
            rgba = np.dstack([crop, alpha])
            cv2.imwrite(os.path.join(IMG, f'chip-{key}.png'), rgba,
                        [cv2.IMWRITE_PNG_COMPRESSION, 9])
            webp(os.path.join(IMG, f'chip-{key}.png'))

    json.dump(geo, open(MAP_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'✓ геометрия → {os.path.relpath(MAP_JSON, ROOT)}')


# ─── кропы 1:1 для блока про печатный масштаб ───────────────────────────────
# (slug, cx, cy, подпись) — доля от размера оригинала, окно 1400×1000 px 1:1
CROPS = [
    ('dc',         0.470, 0.400, 'ряды стоек в холодном коридоре: 300 dpi держат мелочь'),
    ('dc',         0.804, 0.244, 'кружок ИБП PowerXpert 9395P в печатном размере'),
    ('commercial', 0.560, 0.640, 'торговый зал: витрины, стеллажи, кассовая линия'),
    ('industry',   0.700, 0.560, 'цех: прессы, конвейер, сборочные столы'),
]


def crops():
    os.makedirs(IMG, exist_ok=True)
    by_slug = {s: f for s, f, _, _ in POSTERS}
    for i, (slug, cx, cy, note) in enumerate(CROPS, 1):
        src = imread(os.path.join(SRC, by_slug[slug]))
        H, W = src.shape[:2]
        cw, ch = 1400, 1000
        x = int(np.clip(cx * W - cw / 2, 0, W - cw))
        y = int(np.clip(cy * H - ch / 2, 0, H - ch))
        save(os.path.join(IMG, f'zoom-{i}.jpg'), src[y:y + ch, x:x + cw], 92)
        print(f'✓ кроп 1:1 zoom-{i} ({slug}): {note}')


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--plates' in args:
        plates()
    if do_all or '--crops' in args:
        crops()
