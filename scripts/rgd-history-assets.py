#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Ролик „История успеха ЦМ РЖД“» (/video/rgd/history/).

Источник один: media/transrzhd.mp4 (3:54, 1280×720, путь из scripts/a2/video_map.json).
Фильм снят к десятилетию Центральной дирекции по управлению
терминально-складским комплексом, филиала ОАО «РЖД»: три съёмочные группы
работали параллельно, аэросъёмка и земля, графика собрана из презентации
клиента, финальный синхрон записан с начальником дирекции.

Что делает:
  1. Кладёт локально шрифты Podkova + Istok Web (mirror/fonts/files/ +
     mirror/fonts/podkova-istok.css). Внешних CDN на сайте нет принципиально.
     Podkova — слэб с широкими засечками, интонация вокзальной таблички;
     Istok Web — русский гротеск ParaType, как в железнодорожных бланках.
  2. Режет кадры ролика: экранные плашки с цифрами, слайды презентации,
     карта сети, анимация ширины колеи, терминалы, люди, синхрон.
  3. Вынимает из кадра слайда «Услуги ЦМ» (25,0 с) семь шестиугольников
     с фотографиями услуг: на странице ими закрыты те услуги, которых
     в натурной съёмке фильма нет.
  4. Портрет спикера — кроп по лицу каскадом OpenCV выше экранного титра.
  5. Делает .webp рядом с каждым jpg (хостинг отдаёт webp, если файл есть).

Запуск: python3 scripts/rgd-history-assets.py [--fonts] [--frames] [--crops]
Без флагов делает всё.
"""
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
IMG = os.path.join(MIRROR, 'images', 'rgd-history')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VID = os.path.join(ROOT, 'media', 'transrzhd.mp4')    # источник: scripts/a2/video_map.json

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Podkova:wght@400..800'
      '&family=Istok+Web:wght@400;700&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── кадры: (секунда, слаг, ширина, что в кадре) ────────────────────────────
# секунды выверены по покадровому разбору: плашка должна быть дорисована,
# а склейка — не начаться
FRAMES = [
    (22.0, 'poster', 1280, 'терминал с воздуха: штабели, козловые краны, автопоезда'),
    (4.2, 'logo', 1280, 'заставка: знак «10 лет» с краном и логотип ОАО «РЖД»'),
    (14.6, 'found', 1280, 'плашка «образована в 2009 году» над совещанием дирекции'),
    (16.4, 'board', 1280, 'совещание руководства дирекции'),
    # слайды презентации клиента
    (25.0, 'slide-services', 1280, 'слайд «Услуги ЦМ»: семь шестиугольников'),
    (46.4, 'slide-cargo1', 1280, 'слайд «Перерабатываемые грузы», верхний ряд'),
    (48.6, 'slide-cargo2', 1280, 'слайд «Перерабатываемые грузы», нижний ряд'),
    (123.5, 'etp', 1280, 'электронная торговая площадка «Грузовые перевозки»'),
    (118.5, 'site', 1280, 'страница дирекции на сайте ОАО «РЖД»'),
    (131.0, 'teskad', 1280, 'АС ТЕСКАД: ведомость погрузочно-разгрузочных работ'),
    # экранные плашки с цифрами
    (30.8, 'n750', 1280, 'плашка «более 750 грузовых дворов» над тележкой вагона'),
    (34.2, 'n5300', 1280, 'плашка «5300 объектов недвижимого имущества»'),
    (36.6, 'n7000', 1280, 'плашка «7000 профессиональных сотрудников»'),
    (40.0, 'n2000', 1280, 'плашка «2000 единиц погрузочной техники»'),
    (52.4, 'n100', 1280, 'плашки «более 100 млн тонн грузов» и «1 000 000 вагонов»'),
    (55.4, 'n1mln', 1280, 'плашка «1 000 000 вагонов» над составом'),
    # сеть и стройки
    (70.5, 'map-west', 1280, 'карта сети: западная часть страны'),
    (72.5, 'map', 1280, 'карта сети целиком: от Калининграда до Находки'),
    (78.5, 'builds', 1280, 'коллаж крупных строек: Тамань, «Сила Сибири», Сочи'),
    (82.0, 'builds2', 1280, 'коллаж строек: морские порты и федеральные трассы'),
    (90.0, 'booklet', 1280, 'буклеты «Ваш груз — наша забота»'),
    # двор и операции
    (117.0, 'gantry', 1280, 'козловой кран снимает контейнер с платформы'),
    (115.5, 'baltkran', 1280, 'козловой кран «Балткран» грузоподъёмностью 41 т'),
    (126.0, 'reach', 1280, 'ричстакер несёт сорокафутовый контейнер'),
    (27.5, 'truck', 1280, 'контейнер MAERSK опускают на автопоезд'),
    (141.0, 'storage', 1280, 'крытый склад: паллеты и электропогрузчик'),
    (60.5, 'shed', 1280, 'крытый склад дирекции с фирменной аркой'),
    (35.2, 'wagons', 1280, 'состав сверху: платформы, полувагоны, цистерны'),
    # Калининград и колея
    (96.5, 'aero-kal', 1280, 'контейнерный поезд на подходе к терминалу'),
    (101.5, 'kal-coal', 1280, 'ТЛЦ «Калининград»: экскаватор грузит уголь в полувагоны'),
    (104.5, 'kal-load', 1280, 'погрузчик на угольном штабеле терминала'),
    (108.6, 'gauge20', 1280, 'экранная линейка ширины колеи: 1520 мм'),
    (111.5, 'gauge35', 1280, 'та же линейка после пересчёта: 1435 мм'),
    # люди
    (162.0, 'craneop', 1280, 'крановщик в кабине козлового крана'),
    (186.8, 'brigade', 1280, 'приёмосдатчики с документами и рацией на площадке'),
    (136.0, 'client', 1280, 'переговоры с клиентом в кабинете дирекции'),
    (148.0, 'conf', 1280, 'зал конференции дирекции'),
    (172.5, 'team', 1280, 'командная игра на слёте молодежи ЦМ'),
    (179.0, 'polo', 1280, 'поло «I Слёт молодежи ЦМ»'),
    (168.0, 'flip', 1280, 'флипчарт слёта: конкуренты и социальная ответственность'),
    (155.0, 'aero-station', 1280, 'станция с воздуха: парк путей и грузовой двор'),
    # финал
    (190.5, 'change', 1280, 'титр «Мы меняемся для вас» над контейнерной площадкой'),
    (199.0, 'sync', 1280, 'синхрон начальника дирекции'),
    (231.0, 'final', 1280, 'финальная плашка с адресом cm.rzd.ru'),
]

# ─── шестиугольники со слайда «Услуги ЦМ» ───────────────────────────────────
# кадр 25,0 с: слайд целиком в кадре, все семь фотографий читаются.
# (слаг, x, y, сторона) в координатах кадра 1280×720
HEX = [
    ('h-load', 40, 330, 165),      # погрузка и выгрузка: кран с контейнером
    ('h-truck', 215, 365, 165),    # завоз и вывоз автотранспортом
    ('h-store', 385, 330, 165),    # хранение и складская обработка
    ('h-svh', 565, 365, 165),      # склады временного хранения
    ('h-wash', 760, 330, 165),     # очистка и промывка вагонов
    ('h-reefer', 945, 365, 165),   # рефконтейнеры с подключением к сети
    ('h-mobile', 1115, 330, 165),  # мобильные бригады
]

SYNC_SEC = 212.5     # секунда портрета: спикер смотрит в камеру, титр уже ушёл


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
        # у переменного шрифта вес записан диапазоном «400 800» — в имя файла
        # берём первое число, сам блок оставляем как есть
        wght = re.search(r'font-weight:\s*(\d+)', block).group(1)
        name = f'{fam.lower().replace(" ", "-")}-{wght}-{subset}.woff2'
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    head = ('/* Podkova + Istok Web, self-host для /video/rgd/history/.\n'
            '   Сгенерировано scripts/rgd-history-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'podkova-istok.css'), 'w', encoding='utf-8').write(
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
    # -ss ПОСЛЕ -i: точный поиск по кадру. С быстрым поиском ffmpeg прыгает
    # на ближайший ключевой кадр и промахивается мимо плашки с цифрой.
    dst = os.path.join(IMG, f'{slug}.jpg')
    sh(['ffmpeg', '-v', 'error', '-i', VID, '-ss', str(sec),
        '-vf', f'scale={width}:-2:flags=lanczos', '-frames:v', '1',
        '-q:v', quality, dst, '-y'])
    webp(dst)
    return dst


def frames():
    os.makedirs(IMG, exist_ok=True)
    for sec, slug, width, _what in FRAMES:
        cut(sec, slug, width)
    portrait()
    print(f'✓ кадры: {len(FRAMES) + 1} шт. в mirror/images/rgd-history/')


def portrait():
    """Портрет спикера: квадрат по лицу, экранный титр в кадр не попадает."""
    import cv2
    cc = cv2.CascadeClassifier(cv2.data.haarcascades
                               + 'haarcascade_frontalface_default.xml')
    tmp = os.path.join(IMG, '_tmp.png')
    sh(['ffmpeg', '-v', 'error', '-i', VID, '-ss', str(SYNC_SEC),
        '-frames:v', '1', tmp, '-y'])
    im = cv2.imread(tmp)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = [f for f in cc.detectMultiScale(gray, 1.1, 5, minSize=(70, 70))
             if 20 < f[1] < 380]
    if not faces:
        sys.exit(f'✗ лицо не найдено на {SYNC_SEC} с')
    x, y, w, h = max(faces, key=lambda f: f[2])
    side = int(min(max(w * 3.0, 420), 620))
    cx, cy = x + w // 2, y + h // 2
    x0 = int(min(max(cx - side // 2, 0), 1280 - side))
    y0 = int(min(max(cy - side * 0.40, 0), 720 - side))
    crop = cv2.resize(im[y0:y0 + side, x0:x0 + side], (560, 560),
                      interpolation=cv2.INTER_AREA)
    dst = os.path.join(IMG, 'p-belsky.jpg')
    cv2.imwrite(dst, crop, [cv2.IMWRITE_JPEG_QUALITY, 88])
    webp(dst)
    os.remove(tmp)
    print('✓ портрет спикера: p-belsky.jpg')


def crops():
    """Семь фотографий услуг, вынутых из кадра слайда «Услуги ЦМ»."""
    import cv2
    os.makedirs(IMG, exist_ok=True)
    tmp = os.path.join(IMG, '_slide.png')
    sh(['ffmpeg', '-v', 'error', '-i', VID, '-ss', '25.0',
        '-frames:v', '1', tmp, '-y'])
    im = cv2.imread(tmp)
    for slug, x, y, side in HEX:
        x1, y1 = min(x + side, 1280), min(y + side, 720)
        piece = cv2.resize(im[y:y1, x:x1], (330, 330), interpolation=cv2.INTER_AREA)
        dst = os.path.join(IMG, f'{slug}.jpg')
        cv2.imwrite(dst, piece, [cv2.IMWRITE_JPEG_QUALITY, 88])
        webp(dst)
    os.remove(tmp)
    print(f'✓ услуги со слайда: {len(HEX)} шт.')


if __name__ == '__main__':
    args = set(sys.argv[1:])
    todo = args & {'--fonts', '--frames', '--crops'} or {'--fonts', '--frames', '--crops'}
    os.makedirs(IMG, exist_ok=True)
    if '--fonts' in todo:
        fonts()
    if '--frames' in todo:
        frames()
    if '--crops' in todo:
        crops()
