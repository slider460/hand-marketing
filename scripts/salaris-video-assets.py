#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Ролики МФК „Саларис“» (/video/salaris/).

Кейс про два ролика, а не про один: media/salaris-1.mp4 (2:58, зима 2018,
объект на стройке) и media/salaris-2.mp4 (2:33, лето-осень 2018, аудитория
и зона охвата). Пути к файлам — из scripts/a2/video_map.json.

Что делает:
  1. Шрифты Sofia Sans Condensed + Ruda из Google Fonts кладёт локально
     (mirror/fonts/files/ + mirror/fonts/sofia-ruda.css). Внешних CDN на сайте
     нет принципиально. Sofia Sans Condensed взят за сжатые прописные: тем же
     приёмом набраны экранные плашки в обоих роликах. Ruda — округлый гротеск,
     родня начертанию слова «саларис» в знаке.
  2. Режет кадры обоих роликов в mirror/images/salaris-video/. Первый ролик
     640×360, поэтому кадры из него апскейлим бережно (lanczos) и на странице
     не даём крупнее половины ширины.
  3. Снимает геометрию карт зоны охвата прямо с кадров второго ролика и
     кладёт её в scripts/a2/salaris_video_map.json — контурами, а не
     картинками, чтобы на странице зоны были живыми (см. reach_map()).
  4. Делает .webp рядом с каждым jpg (хостинг отдаёт webp, если файл есть).

Запуск: python3 scripts/salaris-video-assets.py [--fonts] [--frames] [--map]
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
IMG = os.path.join(MIRROR, 'images', 'salaris-video')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
V1 = os.path.join(ROOT, 'media', 'salaris-1.mp4')   # источник: scripts/a2/video_map.json
V2 = os.path.join(ROOT, 'media', 'salaris-2.mp4')
MAP_JSON = os.path.join(ROOT, 'scripts', 'a2', 'salaris_video_map.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Sofia+Sans+Condensed:wght@400;600;700;800'
      '&family=Ruda:wght@400;500;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── кадры первого ролика: (секунда, слаг, ширина, что на кадре) ─────────────
# исходник 640×360, поэтому ширины скромные: выше 1100 картинка начинает сыпаться
FRAMES_1 = [
    (6.0, 'v1-cg', 1100, 'здание собрано графикой и вписано в зимний натурный кадр'),
    (9.0, 'v1-cg-name', 1100, 'вывеска «саларис» на графической модели фасада'),
    (11.0, 'v1-site', 1100, 'та же площадка с дрона: каркас, краны, снег'),
    (17.0, 'v1-node', 1100, 'плашка «транспортный узел» поверх плана комплекса'),
    (28.0, 'v1-scheme', 1100, 'схема подъездов: заезд с области, парковка, автостанция'),
    (38.5, 'v1-buses', 1100, 'плашка «до 250 автобусов в час» над автостанцией'),
    (47.0, 'v1-metro', 1100, 'выход из метро «Саларьево», 64 000 человек в день'),
    (67.0, 'v1-neopolis', 1100, 'деловой квартал Neopolis, 5 500 офисных сотрудников'),
    (75.0, 'v1-zhk', 1100, 'корпуса ЖК «Саларьево Парк» вплотную к площадке'),
    (81.0, 'v1-mln', 1100, 'плашка «1 500 000 м² к 2020 году»'),
    (103.0, 'v1-map', 1100, 'карта окружения: десять ЖК, прирост 195 000 человек'),
    (109.0, 'v1-area', 1100, 'плашка «общая площадь 310 000 м²» над каркасом'),
    (117.0, 'v1-parking', 1100, 'плашки арендопригодной площади и парковочной зоны'),
    (123.0, 'v1-build', 1100, 'кран над плитой: состояние стройки зимой 2018'),
    (167.0, 'v1-slogan', 1100, 'финальный знак и строка «Солнце в каждом из нас»'),
]

# ─── кадры второго ролика (1280×720) ────────────────────────────────────────
FRAMES_2 = [
    (5.0, 'v2-city', 1280, 'положение комплекса на карте Москвы у Киевского шоссе'),
    (9.0, 'v2-area', 1280, 'пятно участка сверху: 310 000 м², 5 000 парковочных мест'),
    (12.5, 'v2-lease', 1280, 'готовое здание: 290 магазинов, 105 000 м² аренды'),
    (17.5, 'v2-metro', 1280, 'вестибюль метро «Саларьево» и поток на выходе'),
    (20.5, 'v2-buses', 1280, 'автобусная станция: 280 маршрутов в час'),
    (23.0, 'v2-parking', 1280, 'перехватывающая парковка на 1 500 машиномест'),
    (43.0, 'v2-iso', 1280, 'зона охвата 2019 изохронами, 2 млн человек в 5–20 минутах'),
    (53.0, 'v2-road', 1280, 'трасса Солнцево-Бутово-Видное и станции метро 2019'),
    (58.5, 'v2-reach', 1280, 'общая зона охвата 3,5 млн человек'),
    (65.0, 'v2-mood', 1280, 'индекс потребительской уверенности +8 против −11 в 2017'),
    (69.0, 'v2-mall', 1280, 'галерея готового центра: Reserved, Cropp, Oysho, House'),
    (73.0, 'v2-fun', 1280, 'парк аттракционов Jolly Joya и верёвочный TeikaBoom'),
    (77.0, 'v2-kids', 1280, 'детская зона: поролоновый бассейн'),
    (83.0, 'v2-sport', 1280, 'спорт: re:Store, Under Armour, Nike, Спортмастер'),
    (89.5, 'v2-age', 1280, 'возрастной срез аудитории: 21 %, 35 %, 20 %'),
    (97.0, 'v2-family', 1280, '65 % состоят в браке, 2,9 человека в семье'),
    (105.0, 'v2-int-1', 1280, 'интервью у метро: мужчина'),
    (109.0, 'v2-needs', 1280, 'потребности: одежда, кино и рестораны, гипермаркет'),
    (117.0, 'v2-int-2', 1280, 'интервью у метро: женщина с ребёнком'),
    (124.0, 'v2-int-3', 1280, 'интервью у метро: женщина'),
    (131.0, 'v2-social', 1280, 'соцсети центра в телефоне, 60 000 гостей на открытии'),
    (139.0, 'v2-open', 1280, 'сцена и зал на открытии, 10 000 подписчиков'),
    (145.0, 'v2-final', 1280, 'финал: знак, слоган и дата открытия 1 марта 2019'),
]

# постеры плееров
POSTERS = [(V1, 11.0, 'poster-1', 1100), (V2, 69.0, 'poster-2', 1280)]


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
    head = ('/* Sofia Sans Condensed + Ruda, self-host для /video/salaris/.\n'
            '   Сгенерировано scripts/salaris-video-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'sofia-ruda.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def webp(path):
    """Тот же cwebp с теми же ключами, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def cut(video, sec, slug, width):
    # -ss ПОСЛЕ -i: точный поиск по кадру. С быстрым поиском ffmpeg прыгает на
    # ближайший ключевой кадр и промахивается мимо плашки с цифрой.
    dst = os.path.join(IMG, f'{slug}.jpg')
    sh(['ffmpeg', '-v', 'error', '-i', video, '-ss', str(sec),
        '-vf', f'scale={width}:-2:flags=lanczos', '-frames:v', '1',
        '-q:v', '3', dst, '-y'])
    webp(dst)


def frames():
    os.makedirs(IMG, exist_ok=True)
    for sec, slug, width, _what in FRAMES_1:
        cut(V1, sec, slug, width)
    for sec, slug, width, _what in FRAMES_2:
        cut(V2, sec, slug, width)
    for video, sec, slug, width in POSTERS:
        cut(video, sec, slug, width)
    n = len(FRAMES_1) + len(FRAMES_2) + len(POSTERS)
    print(f'✓ кадры: {n} шт. в mirror/images/salaris-video/')


# ─── геометрия карт зоны охвата ─────────────────────────────────────────────
# Во втором ролике зона охвата показана двумя картами. Обе рисованы в 3D под
# наклоном, поэтому геометрию снимаем прямо с кадров, а не подбираем на глаз:
# так на странице зоны совпадают с тем, что видел клиент в ролике.
#
# Карта «перспективы 2019» (44–58 с): зона 20 минут появляется первой, зона
# 30 минут дорисовывается позже. Обе залиты близкими фиолетовыми, и внешняя
# по цвету совпадает с затемнением фона по краям кадра — по цвету их не
# разделить. Зато разделяет время: маска зоны 30 = что изменилось на кадре
# между 46.5 с (её ещё нет) и 53 с (она уже есть).
REACH_SRC = {
    'before': 46.5,   # только зона 20 минут
    'after': 53.0,    # обе зоны, трасса, станции метро 2019
}
CROP = (520, 0, 1280, 720)   # область карты на кадре 1280×720, левее — плашки

# станции метро, открытые в 2019 (снято с кадра 53 с), в координатах CROP
METRO = [
    (392, 383, 'Саларьево', False),
    (373, 419, 'Филатов луг', True),
    (399, 478, 'Прокшино', True),
    (420, 533, 'Ольховская', True),
    (446, 570, 'Столбово', True),
]

# Трасса Солнцево-Бутово-Видное и отдельный подъезд к комплексу: точки сняты
# с кадра 53 с по осевой линии. Ломаной, а не маской по цвету: тем же жёлтым
# на карте набраны подписи улиц, и фильтр по цвету тащит буквы вместе с дорогой.
HIGHWAY = [(258, 313), (262, 372), (300, 404), (355, 406), (372, 425),
           (392, 470), (404, 500), (424, 533), (452, 553)]
SPUR = [(310, 404), (310, 487)]          # подъезд к МФК, упирается в площадку
HIGHWAY_DASH = [(620, 540), (620, 600), (520, 600), (470, 578)]   # пунктир продолжения


def _contours(mask, min_area, eps, cv2, np, holes=False):
    """Контуры маски → список полигонов в координатах CROP.

    holes=False: только внешние контуры (заливка зоны сплошная, дороги поверх
    неё кладём отдельным слоем). holes=True: внешние вместе с дырами, чтобы
    дорожную сеть можно было нарисовать одним path с fill-rule:evenodd —
    иначе внешний контур связной сети заливается сплошным пятном."""
    mode = cv2.RETR_CCOMP if holes else cv2.RETR_EXTERNAL
    cnts, _ = cv2.findContours(mask, mode, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for c in cnts:
        if abs(cv2.contourArea(c)) < min_area:
            continue
        c = cv2.approxPolyDP(c, eps, True)
        if len(c) < 3:
            continue
        out.append([[int(x), int(y)] for x, y in c[:, 0, :]])
    return sorted(out, key=lambda p: -len(p))


def _path(poly):
    d = f'M{poly[0][0]} {poly[0][1]}'
    d += ''.join(f'L{x} {y}' for x, y in poly[1:])
    return d + 'Z'


def _line(pts):
    return f'M{pts[0][0]} {pts[0][1]}' + ''.join(f'L{x} {y}' for x, y in pts[1:])


def reach_map():
    import cv2
    import numpy as np

    def frame(sec):
        dst = os.path.join(ROOT, 'scripts', 'a2', f'.reach-{sec}.png')
        sh(['ffmpeg', '-v', 'error', '-i', V2, '-ss', str(sec),
            '-frames:v', '1', dst, '-y'])
        im = cv2.imread(dst)[CROP[1]:CROP[3], CROP[0]:CROP[2]]
        os.remove(dst)
        return im

    before, after = frame(REACH_SRC['before']), frame(REACH_SRC['after'])
    hsv = cv2.cvtColor(after, cv2.COLOR_BGR2HSV).astype(int)
    S, V = hsv[..., 1], hsv[..., 2]

    # зона 30 минут: всё, что дорисовалось между кадрами. Дыры внутри (зона
    # 20 минут, дороги, подписи) закрываем — зона рисуется сплошной заливкой.
    d = cv2.absdiff(before, after).max(axis=2)
    z30 = ((d > 28).astype(np.uint8)) * 255
    z30 = cv2.morphologyEx(z30, cv2.MORPH_CLOSE, np.ones((29, 29), np.uint8))
    z30 = cv2.morphologyEx(z30, cv2.MORPH_OPEN, np.ones((45, 45), np.uint8))
    # затемнение фона к краям кадра по цвету неотличимо от заливки зоны и
    # лезет в маску дугой у правого края. Открытие её не берёт (дуга широкая),
    # поэтому режем по x: восточнее МКАД (x≈600) заливки на карте уже нет.
    z30[:, 672:] = 0

    hsv_b = cv2.cvtColor(before, cv2.COLOR_BGR2HSV).astype(int)
    Hb, Sb, Vb = hsv_b[..., 0], hsv_b[..., 1], hsv_b[..., 2]
    z20 = (((Hb > 128) & (Hb < 155) & (Sb > 150) & (Vb > 80) & (Vb < 190))
           .astype(np.uint8)) * 255
    z20 = cv2.morphologyEx(z20, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    z20 = cv2.morphologyEx(z20, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    z20[:, 672:] = 0   # та же дуга затемнения у правого края кадра

    # дороги: тонкая светлая сеть. Подписи улиц набраны тем же светлым, но
    # буквы мелкие — уходят на открытии ядром 5×5.
    roads = (((V > 195) & (S < 70)).astype(np.uint8)) * 255
    roads = cv2.morphologyEx(roads, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    data = {
        'note': ('Геометрия зон охвата снята с кадров media/salaris-2.mp4 '
                 f'({REACH_SRC["before"]} с и {REACH_SRC["after"]} с) '
                 'скриптом scripts/salaris-video-assets.py. Не править руками.'),
        'viewBox': f'0 0 {CROP[2] - CROP[0]} {CROP[3] - CROP[1]}',
        'zone30': [_path(p) for p in _contours(z30, 6000, 2.0, cv2, np)[:4]],
        'zone20': [_path(p) for p in _contours(z20, 2500, 1.6, cv2, np)[:6]],
        # одним path с fill-rule:evenodd, иначе связная сеть зальётся пятном
        'roads': ''.join(_path(p) for p in
                         _contours(roads, 300, 1.1, cv2, np, holes=True)[:120]),
        'highway': _line(HIGHWAY),
        'spur': _line(SPUR),
        'highwayDash': _line(HIGHWAY_DASH),
        'metro': [{'x': x, 'y': y, 'name': n, 'new': new} for x, y, n, new in METRO],
    }
    json.dump(data, open(MAP_JSON, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f"✓ карта охвата: зона30 {len(data['zone30'])} контуров, "
          f'зона20 {len(data["zone20"])}, дороги {len(data["roads"])}, '
          f'трасса {len(data["highway"])} → {os.path.relpath(MAP_JSON, ROOT)}')


if __name__ == '__main__':
    args = sys.argv[1:]
    do_all = not args
    if do_all or '--fonts' in args:
        fonts()
    if do_all or '--frames' in args:
        frames()
    if do_all or '--map' in args:
        reach_map()
