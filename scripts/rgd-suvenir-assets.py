#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Новогодний сувенир ЦМ РЖД» (/creative/rgd/suvenir/).

Материалы:
  1. Печатный календарь «RGD_CD_191205.pdf», 13 полос A4: титул с цифрами
     дирекции и двенадцать месяцев. Отсюда и текст (номер и название месяца,
     услуга дирекции, её описание), и сами листы картинками. Рядом в папке
     лежит рабочий макет «календарь ржд_v10_181123.pdf» от 23.11.2018,
     но он старее: в нём другой август и другой май, а кадры черновые.
  1a. Открытка «календарь ржд_45шт.pdf», разворот 200×200 мм: лицо
     с новогодним составом и оборот с поздравлением дирекции.
  2. Мокапы набора, они лежали в галерее старой тильдовской страницы
     (public/assets/**): титульный лист, лист «03 март», пакет, powerbank,
     термокружки, коробка, ежедневник, ёлочный шар.
  3. Съёмка тиража из ~/Documents/Материалы для обновления сайта/РЖД:
     напечатанный ежедневник и папка на столе дирекции (04.12.2018),
     ёлочный шар в коробке на полке (13.12.2018) и рендер красного шара —
     того, который в итоге ушёл в тираж вместо белого из мокапа.

Что делает:
  1. Шрифты Commissioner (300-800) + PT Sans Narrow локально
     (mirror/fonts/commissioner-ptnarrow.css + files/*.woff2). Внешних CDN
     на сайте нет принципиально.
  2. Переносит мокапы и съёмку в mirror/images/rgd-suvenir/ под говорящими
     именами, в трёх размерах (полный, 1000, 640) и с .webp рядом.
  3. Вынимает из PDF текст двенадцати листов: месяц, услуга, описание.
     Ничего не переписывается руками, в кейсе стоит то же, что в макете.
  4. Снимает палитру айдентики прямо с полосы макета: рендерит страницу
     без фотографий и берёт насыщенные пиксели — это фирменные бирюза,
     светлая бирюза, зелёный и синий, плюс красный календарной сетки.
  5. Считает производственный календарь 2019 года: для каждого месяца
     раскладка по неделям, выходные и праздники РФ (постановление
     Правительства РФ № 1163 от 01.10.2018 о переносе выходных).
     Мартовская сетка из мокапа тиража сверяется с расчётом.

Всё уходит в scripts/a2/rgd_suvenir_map.json, страницу собирает
scripts/a2/gen_rgd_suvenir.py.

Запуск: python3 scripts/rgd-suvenir-assets.py [--fonts] [--images] [--map]
Без флагов делает всё.
"""
import calendar
import datetime
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
PUB = os.path.join(ROOT, 'public', 'assets')
IMG = os.path.join(MIRROR, 'images', 'rgd-suvenir')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
MAP = os.path.join(ROOT, 'scripts', 'a2', 'rgd_suvenir_map.json')

SRC = os.path.expanduser('~/Documents/Материалы для обновления сайта/РЖД')
PDF = os.path.join(SRC, 'RGD_CD_191205.pdf')            # печатный календарь, 13 полос
CARD = os.path.join(SRC, 'календарь ржд_45шт.pdf')      # открытка, разворот 200×200

# низ коллажа на полосе месяца: макет модульный, граница у всех одна.
# Ниже неё на печатном листе идёт календарная сетка, её страница считает сама
COLLAGE_BOTTOM = .712
SHEET_DPI = 140      # ~1160 px по ширине A4, дальше идут -m 1000 и -s 640

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?'
      'family=Commissioner:wght@300;400;500;600;700;800'
      '&family=PT+Sans+Narrow:wght@400;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── картинки: (слаг, файл-источник, что в кадре) ───────────────────────────
# PUB: мокапы из галереи старой страницы; SRC: съёмка тиража от клиента
PICS = [
    ('sheet-title', PUB, '0d04d9b0_12345678901234567890.png',
     'Титульный лист календаря: год, заголовок «ЦМ сегодня это» '
     'и цифры дирекции на фоне контейнерной площадки'),
    ('sheet-march', PUB, '8912fdbf_12345678901234567890.png',
     'Лист «03 март» на стене: услуга «Завоз/вывоз грузов автомобильным '
     'транспортом», коллаж с автопоездом и календарная сетка'),
    ('bag', PUB, '8264a04c_photo.jpg',
     'Бумажный пакет набора: знак ЦМ и разгон полос по нижнему углу'),
    ('power', PUB, '122ded3d_noroot.png',
     'Внешний аккумулятор с кабелем: разгон уходит из нижнего угла в диагональ'),
    ('mugs', PUB, 'f481b528_photo_2020-10-30_19-.jpg',
     'Три цветовых варианта термокружки: зелёная, бирюзовая и белая'),
    ('box', PUB, 'fea6a296_photo_2020-10-30_19-.jpg',
     'Подарочная коробка набора: крышка со знаком ЦМ и разгоном по торцу'),
    ('diary', PUB, 'ac711a71_photo_2020-10-30_19-.jpg',
     'Ежедневник в синей обложке: знак ЦМ по центру, разгон снизу'),
    ('ball', PUB, '2d190b7b_Shar.jpg',
     'Ёлочный шар из мокапа: белый, со знаком ЦМ и бирюзовым разгоном'),
    ('ball-red', SRC, 'PHOTO-2018-11-26-19-12-54.jpg',
     'Шар, ушедший в тираж: красный, со знаком ЦМ и морозным напылением'),
    ('diary-print', SRC, 'PHOTO-2018-12-04-18-07-29.jpg',
     'Напечатанный ежедневник на рабочем столе дирекции, декабрь 2018 года'),
    ('folder-print', SRC, 'PHOTO-2018-12-04-18-08-24.jpg',
     'Напечатанная папка набора: разгон занимает нижнюю половину обложки'),
    ('ball-box', SRC, 'PHOTO-2018-12-13-17-22-42.jpg',
     'Шар в подарочной коробке на полке в кабинете дирекции'),
]

# ─── титульный лист: цифры дирекции, дословно с мокапа ──────────────────────
# Порядок как на листе: сверху вниз по колонкам инфографики.
FIGURES = [
    ('16', 'региональных дирекций'),
    ('174', 'единицы погрузочно-разгрузочной техники'),
    ('289', 'автомобилей'),
    ('24', 'пункта промывки, универсальной обработки подвижного состава '
           'и контейнеров'),
    ('13', 'складов временного хранения'),
    ('5 300', 'объектов общей площадью 7,9 млн м²'),
]

# ─── праздники 2019 года ────────────────────────────────────────────────────
# Нерабочие дни по ТК РФ плюс переносы по постановлению Правительства РФ
# № 1163 от 01.10.2018. Печатный лист марта из мокапа с этим расчётом сходится.
HOLIDAYS_2019 = [
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
    (2, 23),
    (3, 8),
    (5, 1), (5, 2), (5, 3), (5, 9), (5, 10),
    (6, 12),
    (11, 4),
]
# рабочие субботы 2019 года не выпали: переносы ушли в будни
WORKING_WEEKENDS_2019 = []

WEEKDAYS = {'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'}
MONTHS_RU = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль',
             'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=60).read()


def sh(cmd):
    subprocess.run(cmd, check=True)


def webp(path):
    """Те же ключи, что и в scripts/gen-webp.sh."""
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', '82', '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def fonts():
    """Commissioner ведёт всю страницу, PT Sans Narrow живёт внутри листов
    календаря: печатный лист набран узким гротеском, и реконструкция листа
    должна говорить тем же голосом, что и оригинал."""
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
    head = ('/* Commissioner + PT Sans Narrow, self-host для '
            '/creative/rgd/suvenir/.\n'
            '   Сгенерировано scripts/rgd-suvenir-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'commissioner-ptnarrow.css'), 'w',
         encoding='utf-8').write(head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def images():
    """Мокапы и съёмка в трёх размерах: полный (лайтбокс), 1000 (карточка),
    640 (превью и телефон). Рядом .webp, как на всём сайте."""
    os.makedirs(IMG, exist_ok=True)
    for slug, base, fname, _what in PICS:
        src = os.path.join(base, fname)
        if not os.path.exists(src):
            sys.exit(f'✗ нет исходника: {src}')
        im = cv2.imread(src, cv2.IMREAD_UNCHANGED)
        if im is None:
            sys.exit(f'✗ не читается: {src}')
        if im.ndim == 3 and im.shape[2] == 4:      # PNG с альфой кладём на белое
            a = im[:, :, 3:4].astype(np.float32) / 255.0
            im = (im[:, :, :3] * a + 255 * (1 - a)).astype(np.uint8)
        big = os.path.join(IMG, f'{slug}.jpg')
        cv2.imwrite(big, im, [cv2.IMWRITE_JPEG_QUALITY, 88])
        webp(big)
        for suffix, side, q in (('-m', 1000, 86), ('-s', 640, 84)):
            k = min(1.0, side / max(im.shape[1], im.shape[0]))
            dst = os.path.join(IMG, f'{slug}{suffix}.jpg')
            cv2.imwrite(dst, cv2.resize(im, None, fx=k, fy=k,
                                        interpolation=cv2.INTER_AREA),
                        [cv2.IMWRITE_JPEG_QUALITY, q])
            webp(dst)
    print(f'✓ картинки: {len(PICS)} шт. × 3 размера в mirror/images/rgd-suvenir/')


def sheets():
    """Текст листов дословно из печатного календаря.

    На полосе месяца три текстовых куска: «03 МАРТ», название услуги
    прописными и описание в узкую колонку. Порядок кусков в потоке плавает,
    поэтому разбираем по смыслу: строка с номером и месяцем ищется
    регуляркой, всё прописное кроме неё это услуга, остальное описание.
    Переносы внутри слов в макете расставлены руками, их склеиваем.
    Нижний подвал с реквизитами дирекции в описание не пускаем."""
    import fitz
    doc = fitz.open(PDF)
    if doc.page_count != 13:
        sys.exit(f'✗ в календаре {doc.page_count} полос, ожидалось 13')
    names = '|'.join(x.upper() for x in MONTHS_RU)
    out = []
    for i in range(1, 13):                       # полоса 1 это титул
        page = doc[i]
        raw = [ln.strip() for ln in page.get_text().splitlines() if ln.strip()]
        m = re.search(r'\b(\d{2})\s+(' + names + r')\b', ' '.join(raw).upper())
        if not m:
            sys.exit(f'✗ полоса {i + 1}: не нашёл номер и месяц')
        month = m.group(2).lower()
        if month != MONTHS_RU[i - 1]:
            sys.exit(f'✗ полоса {i + 1}: месяц «{month}», ожидался '
                     f'«{MONTHS_RU[i - 1]}»')
        title, descr = [], []
        for ln in raw:
            up = ln.upper()
            if 'ЮР. АДРЕС' in up or 'ТЕЛЕФОН' in up or 'WWW.CM' in up:
                continue                          # подвал листа с реквизитами
            clean = re.sub(r'\b\d{2}\s+(' + names + r')\b', '', up)
            clean = re.sub(r'^\s*(\d{2}|' + names + r')\s*$', '', clean).strip()
            if re.fullmatch(r'[\d\s]*', clean):
                continue                          # числа календарной сетки
            if clean and all(w in WEEKDAYS for w in clean.split()):
                continue                          # шапка дней недели в сетке
            if up == ln:
                title.append(clean)
            else:
                descr.append(ln)
        title = re.sub(r'\s+', ' ', ' '.join(title)).strip()
        text = re.sub(r'\s+', ' ', ' '.join(descr))
        text = re.sub(r'(\S)-\s+(\w)', r'\1\2', text)
        text = re.sub(r'(\w)/\s+(\w)', r'\1/\2', text).strip()
        if not title or not text:
            sys.exit(f'✗ полоса {i + 1}: пустая услуга или описание')
        out.append({'n': m.group(1), 'month': MONTHS_RU[i - 1],
                    'title': title, 'text': text})
    print(f'✓ листы: {len(out)} полос разобрано из печатного календаря')
    return out


def sheet_pics():
    """Листы календаря картинками.

    Полоса месяца режется по низу коллажа: печатная календарная сетка
    в кейс не едет, её страница считает сама и кладёт под кадр живой.
    Титул идёт целиком, сетки на нём нет."""
    import fitz
    doc = fitz.open(PDF)
    os.makedirs(IMG, exist_ok=True)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=SHEET_DPI)
        im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, 3)
        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
        if i == 0:
            slug, cut = 'sheet-00', im.shape[0]
        else:
            slug, cut = f'sheet-{i:02d}', int(im.shape[0] * COLLAGE_BOTTOM)
        big = os.path.join(IMG, f'{slug}.jpg')
        cv2.imwrite(big, im[:cut], [cv2.IMWRITE_JPEG_QUALITY, 86])
        webp(big)
        for suffix, side, q in (('-m', 1000, 86), ('-s', 640, 84)):
            k = min(1.0, side / im.shape[1])
            cv2.imwrite(os.path.join(IMG, f'{slug}{suffix}.jpg'),
                        cv2.resize(im[:cut], None, fx=k, fy=k,
                                   interpolation=cv2.INTER_AREA),
                        [cv2.IMWRITE_JPEG_QUALITY, q])
            webp(os.path.join(IMG, f'{slug}{suffix}.jpg'))
    print(f'✓ листы календаря: {doc.page_count} полос в mirror/images/rgd-suvenir/')


def card_pics():
    """Открытка: лицо и оборот разворота 200×200 мм."""
    import fitz
    doc = fitz.open(CARD)
    if doc.page_count != 2:
        sys.exit(f'✗ в открытке {doc.page_count} полос, ожидалось 2')
    for i, slug in enumerate(('card-front', 'card-back')):
        pix = doc[i].get_pixmap(dpi=SHEET_DPI)
        im = cv2.cvtColor(
            np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, 3), cv2.COLOR_RGB2BGR)
        big = os.path.join(IMG, f'{slug}.jpg')
        cv2.imwrite(big, im, [cv2.IMWRITE_JPEG_QUALITY, 86])
        webp(big)
        for suffix, side, q in (('-m', 1000, 86), ('-s', 640, 84)):
            k = min(1.0, side / im.shape[1])
            cv2.imwrite(os.path.join(IMG, f'{slug}{suffix}.jpg'),
                        cv2.resize(im, None, fx=k, fy=k,
                                   interpolation=cv2.INTER_AREA),
                        [cv2.IMWRITE_JPEG_QUALITY, q])
            webp(os.path.join(IMG, f'{slug}{suffix}.jpg'))
    text = ' '.join(doc[1].get_text().split())
    print('✓ открытка: лицо и оборот')
    return text


def grid_2019():
    """Сетка каждого месяца 2019 года: число, день недели, выходной или нет.

    На печатном листе марта из мокапа тиража красным отмечены 2, 3, 8, 9, 10,
    16, 17, 23, 24, 30 и 31 — суббота с воскресеньем плюс 8 марта. Расчёт
    обязан дать то же самое, иначе сетка на странице врёт."""
    wd = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    hol = set(HOLIDAYS_2019)
    work = set(WORKING_WEEKENDS_2019)
    months = []
    for m in range(1, 13):
        days = []
        for d in range(1, calendar.monthrange(2019, m)[1] + 1):
            w = datetime.date(2019, m, d).weekday()
            off = ((w >= 5) or (m, d) in hol) and (m, d) not in work
            days.append({'d': d, 'w': wd[w], 'off': bool(off)})
        months.append(days)
    march = {d['d'] for d in months[2] if d['off']}
    printed = {2, 3, 8, 9, 10, 16, 17, 23, 24, 30, 31}
    if march != printed:
        sys.exit(f'✗ март 2019 не сошёлся с печатным листом: {sorted(march)}')
    print('✓ сетка 2019: 12 месяцев, март сверен с печатным листом')
    return months


def palette():
    """Фирменные краски прямо из макета.

    Полосы разгона, плашка знака и цифра месяца лежат на полосе вектором:
    заливки ровные, без градиента, поэтому в рендере они дают острые пики
    по частоте. k-means здесь только размазал бы их по фотографиям, а мода
    квантованного цвета вытаскивает ровно печатные краски. Берём двенадцать
    самых частых насыщенных тонов и разбираем их по ролям."""
    import collections
    import fitz
    page = fitz.open(PDF)[3]     # полоса «03 март»
    pix = page.get_pixmap(dpi=150)
    im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).reshape(-1, 3)
    px = im.reshape(-1, 3)[(hsv[:, 1] > 90) & (hsv[:, 2] > 90)]
    cnt = collections.Counter(map(tuple, (px // 6 * 6)))
    got = ['#%02X%02X%02X' % (t[2], t[1], t[0]) for t, _k in cnt.most_common(12)]
    print('✓ палитра из макета:', ' '.join(got[:6]))

    def near(r, g, b):
        t = np.array([r, g, b], dtype=float)
        d = [np.linalg.norm(np.array([int(c[1:3], 16), int(c[3:5], 16),
                                      int(c[5:7], 16)]) - t) for c in got]
        return got[int(np.argmin(d))]

    return {
        'teal': near(0, 138, 150),        # плашка знака ЦМ, основная краска
        'tealLight': near(78, 174, 186),  # светлая бирюза разгона
        'green': near(66, 168, 60),       # номер месяца
        'blue': near(66, 132, 180),       # синие полосы разгона
        'red': near(192, 18, 18),         # выходные в календарной сетке
        'ink': '#1B2A32',
        'deep': '#26608F',                # обложка ежедневника, снята с тиража
    }


def build_map():
    card = card_pics()
    data = {
        'card': card,
        'sheets': sheets(),
        'grid': grid_2019(),
        'figures': [{'n': n, 'what': w} for n, w in FIGURES],
        'palette': palette(),
        'what': {slug: what for slug, _b, _f, what in PICS},
    }
    # подписи к листам календаря для alt и лайтбокса
    data['what']['sheet-00'] = ('Титульный лист календаря 2019 года: цифры '
                                'дирекции на кадре контейнерной площадки')
    for sh in data['sheets']:
        data['what']['sheet-' + sh['n']] = (
            'Лист «{n} {m}»: {t}'.format(n=sh['n'], m=sh['month'],
                                         t=sh['title'].capitalize()))
    data['what']['card-front'] = ('Лицо открытки: новогодний состав '
                                  'с Дедом Морозом идёт через бумажный лес, '
                                  'знак ЦМ на подвешенной табличке')
    data['what']['card-back'] = ('Оборот открытки: лес в три плана, '
                                 'поздравление дирекции и разгон в углу')
    json.dump(data, open(MAP, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'✓ карта: {os.path.relpath(MAP, ROOT)}')


if __name__ == '__main__':
    args = sys.argv[1:]
    every = not args
    if every or '--fonts' in args:
        fonts()
    if every or '--images' in args:
        images()
        sheet_pics()
    if every or '--map' in args:
        build_map()
