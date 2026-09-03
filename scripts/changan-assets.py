#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Презентация Changan CS35» (/event/changan/).

Материал по кейсу (папка «Материалы для обновления сайта/Changan»):
  • FR_Changan_ENG_Triplan_180220.pdf — финальный отчёт на 42 полосы:
    бриф, механика BTL, посуточные данные стенда, воронка, вопросы
    посетителей, тайминг вечера, макеты (анкета A5, призы, ролл-ап);
  • Changan_small/ — 210 файлов: 31 кадр 1920×1080 со съёмки в ТЦ
    и 179 фотографий вечера в дилерском центре;
  • media/changan.mp4 — ролик 80 с (на проде /media/changan-hm-180220.mp4).

Что делает:
  1. Шрифты Philosopher + Golos Text + Neucha локально
     (mirror/fonts/philosopher-golos.css + files/*.woff2). Внешних CDN
     на сайте нет принципиально.
  2. Кладёт отобранные кадры в mirror/images/changan/ в двух размерах
     и с webp рядом.
  3. Выпрямляет лист-раскраску: четыре угла бумаги снимаются с кадра,
     гомография разворачивает лист в A4 — тот самый лист с метками
     по углам, который раздавали гостям.
  4. Оцифровывает график «Mall data by days» из отчёта: столбцы
     находятся по цветам легенды, высоты переводятся в значения по
     линиям сетки. Суммы сверяются с итоговой воронкой.
  5. Достаёт из отчёта макет анкеты A5 и призы, берёт из ролика
     кадры трассы и сканера.
  6. Пишет scripts/a2/changan_map.json.

Запуск: python3 scripts/changan-assets.py [--fonts] [--photos] [--mapping]
                                          [--sheet] [--grabs] [--pdf] [--map]
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
IMG = os.path.join(MIRROR, 'images', 'changan')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
MAP = os.path.join(ROOT, 'scripts', 'a2', 'changan_map.json')

SRC = os.path.expanduser('~/Documents/Материалы для обновления сайта/Changan')
PHOTOS_DIR = os.path.join(SRC, 'Changan_small')
REPORT = os.path.join(SRC, 'FR_Changan_ENG_Triplan_180220.pdf')
VIDEO = os.path.join(ROOT, 'media', 'changan.mp4')
# бекстейдж с телефона: заезд машин в атриум ночью и работа смены
BACKSTAGE_MOV = [
    ('back-door', 'IMG_4722.MOV', 1.0, 'Машина въезжает в торговый центр через входную группу'),
    ('back-mall', 'IMG_4722.MOV', 8.0, 'Машина едет по галерее мимо витрин'),
    ('back-ramp', 'IMG_4721.MOV', 9.0, 'Заезд на подиум по двум аппарелям'),
    ('back-podium', 'IMG_4722.MOV', 15.6, 'Машина доехала до места в атриуме'),
]
BACKSTAGE_PIC = [
    ('back-hall', 'IMG_4790.HEIC', 0, 'Стенд в атриуме, смена на месте'),
    ('back-top', 'IMG_4794.HEIC', 0, 'Стенд сверху, посетители у машин'),
]

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700'
      '&family=Golos+Text:wght@400..900&family=Neucha&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── кадры: (слаг, файл, что в кадре) ──────────────────────────────────────
# 1920×1080 — съёмка в ТЦ «Июнь», 1024×683 — фотоотчёт вечера в «РИА Авто».
STAND = [
    ('mall', '03.jpg', 'ТРЦ «Июнь»: фасад с оранжевой аркой входа'),
    ('stand-top', '09.jpg', 'Стенд сверху: два подиума, экран на стойке, '
                            'инфостойка, ролл-апы, зона с диваном'),
    ('stand-wide', '16.jpg', 'Общий план стенда в атриуме с посетителями'),
    ('form', '21.jpg', 'Промо-модель заполняет анкету с гостем'),
    ('form2', '24.jpg', 'Двое заполняют анкеты у открытого капота'),
    ('hood', '18.jpg', 'Консультация у моторного отсека'),
    ('gift', '11.jpg', 'Подарок посетителю: спиннер с маркой'),
    ('sofa', '26.jpg', 'Семья в зоне отдыха, запись на тест-драйв'),
    ('leaflet', '31.jpg', 'Раздача в галерее торгового центра'),
    ('wheel', '14.jpg', 'Ребёнок за рулём CS35'),
    ('podium', '32.jpg', 'Чёрный CS35 на подиуме с подсветкой'),
]
EVENING = [
    ('dealer', 'DSC_5917.jpg', 'Дилерский центр «РИА Авто»: фасад автосалона'),
    ('testdrive', 'DSC_5922.jpg', 'Машины тест-драйва с оклейкой у салона'),
    ('reception', 'DSC_6003.jpg', 'Встреча гостей в шоуруме'),
    ('guest-form', 'DSC_6116.jpg', 'Гости заполняют анкеты на входе'),
    ('drums', 'DSC_6320.jpg', 'Шоу китайских барабанов у автомобиля'),
    ('lanterns', 'DSC_6295.jpg', 'Танец с фонарями на фоне обратной проекции'),
    ('fans', 'DSC_6509.jpg', 'Танец с веерами'),
    ('color-hands', 'DSC_6440.jpg', 'Гостья раскрашивает лист фломастерами'),
    ('color-table', 'DSC_6431.jpg', 'Стол раскраски: листы, фломастеры, гости'),
    ('color-done', 'DSC_6473.jpg', 'Готовая раскраска в руках у гостьи'),
    ('award', 'DSC_6761.jpg', 'Ведущий с раскрасками участников'),
    ('dessert', 'DSC_6483.jpg', 'Десерты с маркой на глазури'),
    ('crowd', 'DSC_6272.jpg', 'Зрители снимают шоу на телефоны'),
]
# Шесть кадров контента трёхминутного шоу (кадры не сводятся, см. mapping).
MAPPING = [
    ('hero-show', 'DSC_6282.jpg', 'Кадр для обложки: контур по кузову, город на экране'),
    ('map-fire', 'DSC_6259.jpg', 'Пиксельный эквалайзер по борту, на экране горы'),
    ('map-lines', 'DSC_6784.jpg', 'Контурная сетка по кузову'),
    ('map-spark', 'DSC_6786.jpg', 'Разряды по борту'),
    ('map-flame', 'DSC_6787.jpg', 'Пламя по капоту и крылу'),
    ('map-blue', 'DSC_5968.jpg', 'Синие росчерки по всему борту'),
    ('map-acid', 'DSC_6260.jpg', 'Кислотные полосы по кузову'),
    ('map-flow', 'DSC_6262.jpg', 'Потоки света вдоль капота'),
    ('map-brand', 'DSC_6796.jpg', 'Знак и марка на двери'),
    ('map-wave', 'DSC_6287.jpg', 'Экран за машиной сменил пейзаж на лес'),
]

# Фотоотчёт: кадры, которых нет в секциях, по одному на сюжет.
GALLERY = [
    ('5916', 'Дилерский центр «РИА Авто» в день мероприятия'),
    ('5925', 'Машина тест-драйва с оклейкой у входа в салон'),
    ('5931', 'Стойка встречи гостей в шоуруме'),
    ('5958', 'Гость заполняет анкету на тест-драйв'),
    ('5993', 'Анкеты заполняли и стоя, у стола регистрации'),
    ('6007', 'Промо-модели у автомобиля в шоуруме'),
    ('6057', 'Встреча гостей у стойки регистрации'),
    ('6087', 'Гости в зоне ожидания перед началом программы'),
    ('6096', 'Регистрация гостей мероприятия'),
    ('6151', 'Гости в зале перед началом шоу'),
    ('6163', 'Зал наполняется, зона фуршета перед программой'),
    ('6176', 'Съёмочная группа снимает мероприятие'),
    ('6193', 'Ведущий открывает программу у автомобиля'),
    ('6216', 'Официальная часть мероприятия у Changan CS35'),
    ('6225', 'Представители дилера и марки на сцене'),
    ('6236', 'Вручение подарка на официальной части'),
    ('6245', 'Подарок представителю марки Changan'),
    ('6270', 'Гости снимают шоу на телефоны'),
    ('6278', 'Зрители у пресс-волла Changan и РИА Авто'),
    ('6289', 'Барабанщицы готовятся к выходу у автомобиля'),
    ('6300', 'Танец с фонарями на фоне экрана'),
    ('6307', 'Фонари в танцевальном номере крупным планом'),
    ('6322', 'Шоу китайских барабанов на презентации автомобиля'),
    ('6333', 'Барабанщица во время выступления'),
    ('6345', 'Гости смотрят программу вечера'),
    ('6356', 'Танцевальный номер с веерами'),
    ('6374', 'Веера в танцевальном номере'),
    ('6386', 'Финал танцевального блока'),
    ('6404', 'Гости у столов с раскрасками'),
    ('6412', 'Промо-модель раздаёт листы для раскраски'),
    ('6450', 'Гости раскрашивают машины фломастерами'),
    ('6748', 'Награждение участников конкурса раскрасок'),
    ('6798', 'Ведущие на фоне автомобиля под проекцией'),
]
# Лист-раскраска: кадр, где лист виден целиком (углы бумаги в кадре).
SHEET_QUAD = [(210, 264), (676, 202), (819, 549), (353, 611)]   # L, T, R, B

# ─── данные отчёта ─────────────────────────────────────────────────────────
FUNNEL = [
    ('Выслушали информацию', 1603),
    ('Прошли демонстрацию', 599),
    ('Записались на тест-драйв', 126),
    ('Записались на мероприятие', 117),
    ('Дошли до мероприятия', 27),
]
DAYS = ['27 января', '28 января', '29 января', '30 января', '31 января',
        '1 февраля', '2 февраля']
PROGRAM = [
    ('12:00', '13:00', 'Сбор гостей'),
    ('13:00', '13:10', 'Официальное открытие'),
    ('13:10', '13:30', 'Первый блок программы'),
    ('13:30', '14:00', 'Фуршет'),
    ('14:00', '14:30', 'Активности'),
    ('14:30', '15:00', 'Второй блок программы'),
    ('15:00', '15:30', 'Фуршет'),
    ('15:30', '17:00', 'Активности'),
    ('17:00', '18:00', 'Завершение'),
]
QUESTIONS = [
    'Кто делает двигатели',
    'Кто разрабатывал коробку',
    'Есть ли полный привод',
    'Какая минимальная цена',
    'Где собирают машину',
    'У дилера цена не такая, как в прайс-листе',
    'Базовых комплектаций нет в наличии',
    'Что с запчастями',
    'Сервисных центров мало, до них далеко',
]
LIKED = [
    'Цвета кузова, чаще всего хвалили коричневый',
    'Темно-красный из буклета спрашивали отдельно, его на стенде не было',
    'Цена',
    'Салон внутри',
    'Как выглядит снаружи',
    'Двери закрываются мягко',
    'Обычный четырехступенчатый автомат, без вариатора',
    'Срок гарантии',
    'Дорожный просвет',
    'Тихо едет',
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


def need(path):
    if not os.path.exists(path):
        sys.exit(f'✗ нет исходника: {path}')
    return path


def save(im, slug, sizes=((1280, 86), (640, 82)), q=90):
    """Кадр в двух размерах + webp рядом: телефон не должен тянуть большой."""
    os.makedirs(IMG, exist_ok=True)
    big = os.path.join(IMG, f'{slug}.jpg')
    cv2.imwrite(big, im, [cv2.IMWRITE_JPEG_QUALITY, q])
    webp(big)
    for side, qq in sizes:
        if max(im.shape[:2]) <= side:
            continue
        k = side / max(im.shape[1], im.shape[0])
        dst = os.path.join(IMG, f'{slug}-{side}.jpg')
        cv2.imwrite(dst, cv2.resize(im, None, fx=k, fy=k,
                                    interpolation=cv2.INTER_AREA),
                    [cv2.IMWRITE_JPEG_QUALITY, qq])
        webp(dst)


def fonts():
    """Philosopher (заголовки: каллиграфические срезы, кириллица),
    Golos Text (текст) и Neucha на подписи в блоке раскраски —
    рукописный там не украшение, а голос фломастера с листа."""
    os.makedirs(FILES, exist_ok=True)
    css = fetch(GF).decode('utf-8')
    blocks = re.findall(r'/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    out, n = [], 0
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        wght = re.search(r'font-weight:\s*([\d ]+)', block).group(1).replace(' ', '-')
        name = f'{fam.lower().replace(" ", "-")}-{wght}-{subset}.woff2'
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    head = ('/* Philosopher + Golos Text + Neucha, self-host для /event/changan/.\n'
            '   Сгенерировано scripts/changan-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'philosopher-golos.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def photos():
    for slug, fname, _what in STAND + EVENING:
        save(cv2.imread(need(os.path.join(PHOTOS_DIR, fname))), slug)
    print(f'✓ кадры: {len(STAND) + len(EVENING)} шт. × 2 размера')


def mapping():
    """Шесть состояний контента шоу.

    Кадры сняты с одной точки, но между дублями камера гуляла на десятки
    пикселей. Сводить их гомографией нельзя: контент на кузове каждый раз
    другой, опорные точки цепляются за проекцию, а не за машину, и кузов
    от такой подгонки ведёт. Поэтому кадры идут как есть — это шесть
    фотографий трёхминутного шоу, а не шесть состояний одного кадра.
    """
    for slug, fname, _what in MAPPING:
        save(cv2.imread(need(os.path.join(PHOTOS_DIR, fname))), slug)
    print(f'✓ маппинг: {len(MAPPING)} кадра контента')


def sheet():
    """Лист-раскраска, выпрямленный с кадра.

    Гости раскрашивали лист с контуром машины и чёрными метками по углам —
    по ним сканер ловил рисунок. На кадре лист лежит на коленях под углом;
    четыре угла найдены по маске бумаги (approxPolyDP даёт три надёжных,
    четвёртый достроен как параллелограмм — перспектива на таком
    расстоянии почти аффинная), дальше обычная гомография в A4.
    Правую треть листа держит рука: это фотография артефакта, а не
    восстановленный макет, и страница показывает его именно так.
    """
    im = cv2.imread(need(os.path.join(PHOTOS_DIR, 'DSC_6440.jpg')))
    quad = np.float32(SHEET_QUAD)
    w, h = 1414, 1000
    m = cv2.getPerspectiveTransform(quad, np.float32([[0, 0], [w, 0], [w, h], [0, h]]))
    save(cv2.warpPerspective(im, m, (w, h)), 'sheet', sizes=((640, 84),))
    print('✓ лист-раскраска выпрямлен в A4')


def grabs():
    """Кадры ролика: трасса виртуального тест-драйва и сканер."""
    for slug, t in (('track', 65.4), ('track2', 66.2), ('scanner', 64.8)):
        dst = os.path.join(IMG, f'{slug}.jpg')
        os.makedirs(IMG, exist_ok=True)
        sh(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', need(VIDEO),
            '-frames:v', '1', '-q:v', '3', '-y', dst])
        save(cv2.imread(dst), slug, sizes=((640, 84),))
    print('✓ кадры ролика: трасса и сканер')


def backstage():
    """Бекстейдж, снятый на телефон: как машины заводили в атриум.

    Два ролика по 17 секунд и два снимка. Ролики сняты квадратом 720×720
    в темноте, поэтому берём из них не превью, а конкретные секунды:
    въезд через входную группу, проезд по галерее, заезд на аппарели
    и машина уже на подиуме. HEIC разворачиваем по флагу ориентации,
    иначе снимок сверху ложится боком.
    """
    for slug, name, t, _what in BACKSTAGE_MOV:
        dst = os.path.join(IMG, f'{slug}.jpg')
        os.makedirs(IMG, exist_ok=True)
        sh(['ffmpeg', '-v', 'error', '-ss', str(t), '-i',
            need(os.path.join(SRC, name)), '-frames:v', '1', '-q:v', '2',
            '-y', dst])
        save(cv2.imread(dst), slug, sizes=((640, 84),))
    for slug, name, rot, _what in BACKSTAGE_PIC:
        tmp = os.path.join(IMG, f'_{slug}.jpg')
        sh(['sips', '-s', 'format', 'jpeg', need(os.path.join(SRC, name)),
            '--out', tmp])
        im = cv2.imread(tmp)
        os.remove(tmp)
        if rot:
            im = cv2.rotate(im, cv2.ROTATE_90_COUNTERCLOCKWISE)
        save(im, slug, sizes=((1280, 86), (640, 82)))
    print(f'✓ бекстейдж: {len(BACKSTAGE_MOV) + len(BACKSTAGE_PIC)} кадра')


def gallery():
    """Фотоотчёт: кадры, которых нет в секциях.

    Для плитки хватает средних размеров, но в лайтбоксе кадр открывается
    крупно, поэтому кладём оба размера.
    """
    for num, _alt in GALLERY:
        save(cv2.imread(need(os.path.join(PHOTOS_DIR, f'DSC_{num}.jpg'))),
             f'g{num}', sizes=((640, 82),))
    print(f'✓ фотоотчёт: {len(GALLERY)} кадров')


def pdf():
    """Макеты из отчёта: анкета A5 и призы. Ролл-ап и прайс-лист
    в кейс не идут — на них цены, а год и цены клиент показывать
    не просил."""
    import fitz
    doc = fitz.open(need(REPORT))
    # Полосы отчёта, а не вложенные в PDF картинки: макеты вставлены туда
    # скриншотами рабочего стола, вместе с чужим окном видеозвонка.
    # Боксы — в координатах рендера при 100 dpi (2667×1500).
    for slug, page, box in (('form-a5', 29, (300, 450, 2400, 1150)),
                            ('prizes', 28, (500, 430, 2150, 1220))):
        pm = doc[page].get_pixmap(dpi=200)
        arr = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, pm.n)
        arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR if pm.n == 3 else cv2.COLOR_RGBA2BGR)
        x0, y0, x1, y1 = [v * 2 for v in box]
        save(arr[y0:y1, x0:x1], slug, sizes=((640, 84),))
    print('✓ макеты из отчёта: анкета и призы')


def chart():
    """Посуточные данные стенда, снятые с графика отчёта.

    В отчёте есть две полосы с цифрами: столбчатый график по семи дням
    (без подписей значений) и итоговая воронка с числами. График
    оцифровывается по цветам легенды: для каждого ряда находятся
    прямоугольники, верх переводится в значение по линиям сетки
    (шаг 20 единиц, ноль на оси). Суммы сверяются с воронкой —
    расхождение по нижним двум рядам страница называет вслух.
    """
    import fitz
    doc = fitz.open(need(REPORT))
    pm = doc[7].get_pixmap(dpi=110)
    a = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, pm.n)[:, :, :3]
    a = a.astype(int)
    cols = {'listen': (225, 6, 19), 'demo': (41, 171, 225),
            'test': (139, 197, 62), 'event': (197, 156, 108)}
    top, bot = 380, 1425
    base, unit = 1419.5, (1419.5 - 435.0) / 300.0     # ось и цена деления
    sub = a[top:bot]
    rows = {}
    for key, c in cols.items():
        m = (np.abs(sub - np.array(c)).sum(2) < 30)
        on = m.sum(0) > 4
        bars, s = [], None
        for x, v in enumerate(on):
            if v and s is None:
                s = x
            elif (not v) and s is not None:
                if x - s > 8:
                    bars.append((s, x - 1))
                s = None
        vals = []
        for x0, x1 in bars:
            ys, _ = np.nonzero(m[:, x0:x1 + 1])
            vals.append(int(round((base - (ys.min() + top)) / unit)))
        if len(vals) != len(DAYS):
            sys.exit(f'✗ ряд {key}: найдено {len(vals)} столбцов вместо {len(DAYS)}')
        rows[key] = vals
    for key in rows:
        print(f'  {key:<7} {rows[key]}  сумма {sum(rows[key])}')
    print('✓ график по дням оцифрован')
    return rows


# Окна, в которых на кадрах трассы видны раскрашенные машины гостей.
RIVAL_BOXES = [('track2', (720, 250, 835, 310)),
               ('track2', (1130, 368, 1248, 436)),
               ('track', (752, 322, 892, 392)),
               ('track', (880, 402, 1070, 478))]


def rivals():
    """Цвета машин-соседей по трассе, снятые с кадров ролика.

    Кадры сильно засинены светом проектора, поэтому просто «самый
    насыщенный кластер» даёт фон трассы. Считаем медианный тон всего
    кадра (это и есть фон) и берём из k-means те кластеры, чей тон
    отстоит от фона дальше всего: так проступает раскраска, а не асфальт.
    """
    out = []
    for slug, (x0, y0, x1, y1) in RIVAL_BOXES:
        im = cv2.imread(need(os.path.join(IMG, slug + '.jpg')))
        base = int(np.median(cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[:, :, 0]))
        win = im[y0:y1, x0:x1].reshape(-1, 3).astype(np.float32)
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 24, 1.0)
        _, _lab, cen = cv2.kmeans(win, 5, None, crit, 8, cv2.KMEANS_PP_CENTERS)
        cand = []
        for c in cen:
            b, g, r = [max(0, min(255, int(round(v)))) for v in c]
            h, sat, val = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]
            d = abs(int(h) - base)
            d = min(d, 180 - d)                     # тон замкнут по кругу
            if val < 45:
                continue
            cand.append((d * (int(sat) + 40), '#%02X%02X%02X' % (r, g, b)))
        cand.sort(reverse=True)
        out.append([cand[0][1], cand[1][1] if len(cand) > 1 else cand[0][1]])
    return out


def write_map():
    rows = chart()
    riv = rivals()
    data = {
        'brief': {
            'mall': 'ТРЦ «Июнь»',
            'mall_days': 'с 27 января по 2 февраля',
            'mall_hours': 'с 12:00 до 20:00',
            'staff': 'координатор и две промо-модели',
            'dealer': 'Дилерский центр «РИА Авто»',
            'dealer_day': '4 февраля',
            'dealer_hours': 'с 12:00 до 18:00',
        },
        'funnel': [{'label': l, 'value': v} for l, v in FUNNEL],
        'days': DAYS,
        'rows': rows,
        'rows_sum': {k: sum(v) for k, v in rows.items()},
        'program': [{'from': a, 'to': b, 'what': c} for a, b, c in PROGRAM],
        'questions': QUESTIONS,
        'liked': LIKED,
        'rivals': riv,
        'photos': {slug: what for slug, _f, what in STAND + EVENING + MAPPING},
        'backstage': {s: w for s, _n, _t, w in BACKSTAGE_MOV}
                     | {s: w for s, _n, _r, w in BACKSTAGE_PIC},
        'gallery': [{'id': f'g{n}', 'alt': a} for n, a in GALLERY],
    }
    os.makedirs(os.path.dirname(MAP), exist_ok=True)
    json.dump(data, open(MAP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'✓ карта кейса: {os.path.relpath(MAP, ROOT)}')


def main():
    args = sys.argv[1:]
    all_ = not args
    if all_ or '--fonts' in args:
        fonts()
    if all_ or '--photos' in args:
        photos()
    if all_ or '--mapping' in args:
        mapping()
    if all_ or '--sheet' in args:
        sheet()
    if all_ or '--grabs' in args:
        grabs()
    if all_ or '--backstage' in args:
        backstage()
    if all_ or '--gallery' in args:
        gallery()
    if all_ or '--pdf' in args:
        pdf()
    if all_ or '--map' in args:
        write_map()


if __name__ == '__main__':
    main()
