#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Клиентский опыт Saint-Gobain» (/video/saintgobain/cx/).

Материал (папка «Материалы для обновления сайта/Saint-Gobain/CX_video»):
  • «SG клиентский опыт часть 1.mp4» — путь клиента, 416,6 с, 1280×720, 25 к/с;
  • «SG клиентский опыт часть 2 ТЕЗИСЫ.mp4» — 18 тезисов директоров, 190,9 с;
  • «Видео расписание съёмок.xlsx» — три листа = три съёмочных дня, сетка 15 минут;
  • «Видео1.xlsx» — бриф, посценный сценарий части 1, тезисы части 2 со спикерами,
    12 ссылок на архивные ролики Изовер / Ветонит / Изорок.

Веб-версии роликов лежат в mirror/media/sg-cx-part1.mp4 и -part2.mp4 (x264 crf 27,
720p, faststart) и грузятся на хостинг вручную, как остальные крупные видео.

Что делает скрипт:
  1. Режет 48 портретов парада: тайм-коды планов взяты из детекта склеек
     (scripts/a2/agent-out/sg-cx/facts.json), в каждом плане берётся самый
     резкий кадр из окна, лицо ищется каскадом, кроп 3:4 строится вокруг лица
     с запасом сверху под воздух; если лица нет — кроп по центру верхней трети.
  2. Снимает кадры сцен части 1 и портреты 17 спикеров части 2.
  3. Кладёт 2 размера каждого кадра + webp рядом.
  4. Пишет scripts/a2/sgcx_map.json — что откуда снято, с тайм-кодами.

Запуск: python3 scripts/sgcx-assets.py [--parade] [--scenes] [--speakers] [--map]
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
IMG = os.path.join(MIRROR, 'images', 'sgcx')
VIDEOS = os.path.join(MIRROR, 'videos')
OUT = os.path.join(ROOT, 'scripts', 'a2', 'agent-out', 'sg-cx')
P1 = os.path.join(MIRROR, 'media', 'sg-cx-part1.mp4')
P2 = os.path.join(MIRROR, 'media', 'sg-cx-part2.mp4')

FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
# Wix Madefor Display + Text: фильм набран не парой шрифтов, а одним нейтральным
# гротеском в двух оптиках — имя в плашке капсом крупной оптикой, отдел под ним
# мелкой. Страница пересобирает эту плашку своими средствами.
GF = ('https://fonts.googleapis.com/css2?family=Wix+Madefor+Display:wght@400..800'
      '&family=Wix+Madefor+Text:ital,wght@0,400..800;1,400..800&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

FACTS = json.load(open(os.path.join(OUT, 'facts.json'), encoding='utf-8'))
CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
PROFILE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

# сцены части 1: тайм-код → что в кадре. Границы сняты с контактных листов
# (шаг 5,2 с) и уточнены по детекту склеек cuts-part1.txt
SCENES = [
    (11.0,  'office-door',   'Табличка Saint-Gobain на двери офиса'),
    (16.0,  'reception',     'Ресепшн офиса, менеджер программы идёт с папкой'),
    (23.2,  'folder',        'Папка программы: обложка с портретом клиента'),
    (33.0,  'measure',       'Клиенты выбирают материалы на своём ремонте'),
    (34.9,  'client-tablet', 'План квартиры, с которого всё начинается'),
    (37.2,  'road',          'Клиент за рулём по дороге мимо рекламы'),
    (57.0,  'sales-talk',    'Разговор клиента с сотрудником отдела продаж'),
    (78.0,  'mosaic',        'Мозаика из портретов сотрудников со знаком компании'),
    (132.0, 'meeting',       'Офис: работа с документами по заказу'),
    (142.4, 'gyproc-yard',   'Сотрудник Gyproc на площадке завода'),
    (148.4, 'isover-stock',  'Линия ISOVER в цеху'),
    (168.0, 'vetonit-line',  'Маркировка ведра weber.vetonit на линии'),
    (183.0, 'mnemo',         'Оператор Vetonit за пультом линии'),
    (191.6, 'control-room',  'Операторская завода'),
    (196.2, 'isover-belt',   'Плита минеральной ваты на конвейере'),
    (211.0, 'shipping-doc',  'Отметка в накладной на пункте отгрузки'),
    (221.4, 'pallets',       'Паллеты weber.vetonit едут в фуру'),
    (226.4, 'truck',         'Фура с продукцией уходит по трассе'),
    (232.0, 'mounting',      'Монтаж: каркас и плиты на объекте'),
    (409.5, 'clients-final', 'Клиенты в готовой квартире, финал ролика'),
]



def sharpest(cap, fps, t0, t1):
    """Самый резкий кадр в окне: на панорамах и проходах середина плана мылит."""
    best, bestv = None, -1.0
    for f in range(int(t0 * fps), int(t1 * fps), max(1, int(fps * 0.12))):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        ok, fr = cap.read()
        if not ok:
            continue
        v = cv2.Laplacian(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        if v > bestv:
            best, bestv = fr, v
    return best


def face_crop(fr, ratio=3 / 4, cut_plate=True, side=None):
    """Кроп под портрет: лицо ставится в верхнюю треть, ширина по соотношению.

    Нижние 22 % кадра отрезаются до поиска лица: там лежит плашка с именем,
    и она не должна попасть в портрет — подписи на странице свои."""
    if cut_plate:
        fr = fr[:int(fr.shape[0] * 0.78), :]
    h, w = fr.shape[:2]
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    faces = CASCADE.detectMultiScale(g, 1.12, 5, minSize=(54, 54))
    if not len(faces):
        faces = PROFILE.detectMultiScale(g, 1.12, 5, minSize=(54, 54))
    if not len(faces):
        faces = PROFILE.detectMultiScale(cv2.flip(g, 1), 1.12, 5, minSize=(54, 54))
        faces = [(w - x - fw, y, fw, fh) for x, y, fw, fh in faces]
    if side and len(faces) > 1:
        faces = [min(faces, key=lambda f: f[0])] if side == 'left' else [max(faces, key=lambda f: f[0])]
    if len(faces):
        x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
        cx, cy = x + fw / 2, y + fh / 2
        ch = min(h, fh * 4.6)
        cw = ch * ratio
        x0 = int(np.clip(cx - cw / 2, 0, w - cw))
        y0 = int(np.clip(cy - ch * 0.34, 0, h - ch))
        return fr[y0:int(y0 + ch), x0:int(x0 + cw)], True
    ch = h * 0.92
    cw = ch * ratio
    x0 = int((w - cw) / 2)
    return fr[0:int(ch), x0:int(x0 + cw)], False


def fetch(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA})).read()


def fonts():
    os.makedirs(FILES, exist_ok=True)
    css = fetch(GF).decode('utf-8')
    blocks = re.findall(r'/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    out, n = [], 0
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        wght = re.search(r'font-weight:\s*([\d .]+)', block).group(1).strip().replace(' ', '-')
        ital = 'i' if 'font-style: italic' in block else ''
        name = f'{fam.lower().replace(" ", "-")}-{wght}{ital}-{subset}.woff2'
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    head = ('/* Wix Madefor Display + Wix Madefor Text, self-host '
            'для /video/saintgobain/cx/.\n'
            '   Сгенерировано scripts/sgcx-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'madefor.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def best_portrait(cap, fps, t0, t1, side=None):
    """Портрет из окна плана: кадр выбирается не по резкости, а по лицу.

    Планы парада начинаются с общего кадра или движения, и самый резкий кадр
    часто оказывается пустым столом. Считаем на каждом шаге площадь найденного
    лица и резкость, берём максимум произведения; если лица нет нигде — падаем
    на самый резкий кадр с кропом по центру."""
    best, bestscore, sharp, sharpv = None, 0.0, None, -1.0
    for f in range(int(t0 * fps), int(t1 * fps), max(1, int(fps * 0.16))):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        ok, fr = cap.read()
        if not ok:
            continue
        v = cv2.Laplacian(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        if v > sharpv:
            sharp, sharpv = fr, v
        crop, hit = face_crop(fr, side=side)
        if hit:
            score = crop.shape[0] * crop.shape[1] * (v ** 0.5)
            if score > bestscore:
                best, bestscore = crop, score
    if best is not None:
        return best, True
    if sharp is None:
        return None, False
    return face_crop(sharp)


def save(img, name, widths=(560, 280)):
    os.makedirs(IMG, exist_ok=True)
    paths = []
    for i, wid in enumerate(widths):
        hh = int(img.shape[0] * wid / img.shape[1])
        r = cv2.resize(img, (wid, hh), interpolation=cv2.INTER_AREA)
        p = os.path.join(IMG, f'{name}.jpg' if i == 0 else f'{name}@{wid}.jpg')
        cv2.imwrite(p, r, [cv2.IMWRITE_JPEG_QUALITY, 86])
        paths.append(p)
    return paths


def parade():
    """48 портретов парада: план каждого сотрудника → кадр → портрет 3:4."""
    cap = cv2.VideoCapture(P1)
    fps = cap.get(cv2.CAP_PROP_FPS)
    rows = []
    people = FACTS['parade']
    for i, p in enumerate(people):
        t = p['t']
        # t — момент, на котором плашка читается; окно берётся вокруг него,
        # иначе на коротких планах кадр уезжает к следующему сотруднику
        t0 = max(0.0, t - 1.1)
        t1 = t + 1.1
        if i + 1 < len(people):
            t1 = min(t1, people[i + 1]['t'] - 0.6)
        # Пятаева и Фаллетта сняты одним планом с двумя плашками сразу:
        # в кадре два человека, и каждому нужно своё лицо, левое или правое
        # Пятаева и Фаллетта сняты одним планом с двумя плашками сразу: берём
        # общий кадр и режем его пополам, иначе детектор отдаёт обоим одно лицо
        # или цепляется за монитор
        half = {'Марат Фаллетта': (0.02, 0.52), 'Янина Пятаева': (0.46, 0.98)}.get(p['name'])
        if half:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(323.4 * fps))
            ok, fr = cap.read()
            w = fr.shape[1]
            # в этом плане плашек две и стоят они выше обычного, поэтому
            # режем кадр по 0,70 высоты, а не по стандартным 0,78
            fr = fr[:int(fr.shape[0] * 0.70), :]
            crop, hit = face_crop(fr[:, int(w * half[0]):int(w * half[1])], cut_plate=False)
        else:
            crop, hit = best_portrait(cap, fps, t0, max(t1, t0 + 0.4))
        if crop is None:
            print('  ! нет кадра', p['name'])
            continue
        name = f'p{i + 1:02d}'
        save(crop, name)
        rows.append({'id': name, 'name': p['name'], 'unit': p['unit'], 't': t, 'face': hit})
        print(f"  · {name} {p['name']:<24} {'лицо' if hit else 'центр'}")
    cap.release()
    json.dump(rows, open(os.path.join(OUT, 'parade-crops.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'✓ портретов: {len(rows)}, лиц найдено: {sum(r["face"] for r in rows)}')


def scenes():
    """Кадры сцен части 1 — широкие, 16:9, без кропа."""
    cap = cv2.VideoCapture(P1)
    fps = cap.get(cv2.CAP_PROP_FPS)
    for t, name, descr in SCENES:
        fr = sharpest(cap, fps, t, t + 0.7)
        if fr is None:
            print('  ! нет кадра', name)
            continue
        save(fr, f'sc-{name}', widths=(1120, 560))
        print(f'  · sc-{name:<14} {t:6.1f}s  {descr}')
    cap.release()


def speakers():
    """17 портретов спикеров второй части.

    Кадр надо выбрать так, чтобы в нём не было ни вшитого титра с именем
    (на странице имя набирается своим шрифтом рядом, два титра поверх друг
    друга выглядят как брак), ни чёрно-белого дубля из наплыва между
    спикерами. Поэтому в окне реплики отбираются кадры, у которых:
      • найдено лицо;
      • кадр цветной (в наплыве соседний спикер идёт обесцвеченным);
      • нижняя полоса чистая от текста (плотность границ ниже порога).
    Из подходящих берём самый крупный и резкий."""
    cap = cv2.VideoCapture(P2)
    fps = cap.get(cv2.CAP_PROP_FPS)
    seen = {}
    ths = FACTS['theses']
    order = []
    for th in ths:
        if th['speaker'] not in order:
            order.append(th['speaker'])
    for i, th in enumerate(ths):
        key = th['speaker']
        if key in seen:
            continue
        # окно кончается до следующей реплики, иначе на коротких тезисах
        # лучший кадр достаётся уже следующему спикеру
        t_end = min(th['t'] + 9.0,
                    ths[i + 1]['t'] - 1.0 if i + 1 < len(ths) else th['t'] + 9.0)
        # Порядок отбора: сперва строгие пороги, потом послабления. Кадр должен
        # быть цветным (в наплыве соседний спикер обесцвечен и кадр рассыпан на
        # прямоугольники), без вшитой плашки с именем в средней полосе и с лицом
        # в верхних 62 % — ниже идёт титр тезиса, который в портрет не берём.
        best, bestscore, t_best = None, 0.0, None
        for color_min, gray_max, edge_max in ((0.58, 0.20, 3.4), (0.50, 0.30, 4.0), (0.42, 0.38, 5.5),
                                              (0.30, 0.50, 7.5), (0.18, 0.70, 99.0)):
          if best is not None:
            break
          # наплывы стоят по краям реплики: первые секунды после плашки и
          # последние перед следующим спикером, поэтому окно берём из середины
          for f in range(int((th['t'] + 3.2) * fps), int(max(t_end - 1.5, th['t'] + 4.4) * fps),
                         max(1, int(fps * 0.2))):
            cap.set(cv2.CAP_PROP_POS_FRAMES, f)
            ok, fr = cap.read()
            if not ok:
                break
            h = fr.shape[0]
            sat = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)[:, :, 1]
            if float((sat > 60).mean()) < color_min or float((sat < 25).mean()) > gray_max:
                continue
            plate = cv2.cvtColor(fr[int(h * 0.42):int(h * 0.70), :], cv2.COLOR_BGR2GRAY)
            if float(cv2.Canny(plate, 90, 220).mean()) > edge_max:
                continue
            top = fr[:int(h * 0.62), :]
            crop, hit = face_crop(top, cut_plate=False)
            if not hit:
                continue
            v = cv2.Laplacian(cv2.cvtColor(top, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
            score = crop.shape[0] * crop.shape[1] * (v ** 0.5)
            if score > bestscore:
                best, bestscore, t_best = crop, score, f / fps
        if best is None:
            print('  ! чистого кадра нет:', key)
            continue
        name = 'sp-' + str(order.index(key) + 1).zfill(2)
        save(best, name)
        seen[key] = {'id': name, 'speaker': key, 'title': th['title'],
                     't': th['t'], 'frame_t': round(t_best, 2), 'face': True}
        print(f"  · {name} {key:<22} кадр {t_best:6.2f} с")
    cap.release()
    json.dump(list(seen.values()), open(os.path.join(OUT, 'speaker-crops.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'✓ спикеров: {len(seen)}')


# нарезка для первого экрана: планы, которые показывают охват съёмки —
# офис, спецодежда на площадке, линия, лаборатория, отгрузка, трасса,
# монтаж и клиенты в готовой квартире. (тайм-код, длительность)
HERO_CUTS = [
    (37.4, 1.5), (16.2, 1.2), (142.6, 1.3), (151.3, 1.3), (183.2, 1.3),
    (197.4, 1.3), (221.6, 1.4), (226.6, 1.7), (232.2, 1.4), (244.0, 1.2),
    (409.6, 1.8),
]


def hero_loop():
    """Собирает mirror/videos/sgcx-hero-loop.mp4: короткий немой луп для героя.

    Лежит внутри mirror/**, поэтому уезжает на хостинг обычным деплоем и
    ручной заливки не требует (в отличие от полных роликов в /media/).
    Постер снимается с первого кадра лупа: пока видео грузится, на его месте
    стоит тот же кадр, и подмена не видна."""
    tmp = os.path.join(OUT, 'hero-parts')
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(VIDEOS, exist_ok=True)
    parts = []
    for i, (t, dur) in enumerate(HERO_CUTS):
        p = os.path.join(tmp, f'{i:02d}.mp4')
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-t', str(dur),
                        '-i', P1, '-an', '-vf', 'scale=1280:720:force_original_aspect_ratio=increase,'
                        'crop=1280:720,setsar=1', '-c:v', 'libx264', '-crf', '26',
                        '-preset', 'slow', '-g', '50', p], check=True)
        parts.append(p)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    out = os.path.join(VIDEOS, 'sgcx-hero-loop.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                    '-c:v', 'libx264', '-crf', '26', '-preset', 'slow', '-an',
                    '-movflags', '+faststart', out], check=True)
    # постер: первый кадр лупа, тот же размер
    poster = os.path.join(IMG, 'hero-poster.jpg')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', out, '-frames:v', '1',
                    '-q:v', '3', poster], check=True)
    for p in parts + [lst]:
        os.remove(p)
    os.rmdir(tmp)
    total = sum(d for _, d in HERO_CUTS)
    print(f'✓ луп героя: {len(HERO_CUTS)} планов, {total:.1f} с, '
          f'{os.path.getsize(out) / 1024 / 1024:.1f} МБ + постер')


def webp():
    subprocess.run(['bash', os.path.join(ROOT, 'scripts', 'gen-webp.sh'), IMG], check=False)


def write_map():
    m = {'part1': '/media/sg-cx-part1.mp4', 'part2': '/media/sg-cx-part2.mp4',
         'img_base': '/images/sgcx', 'scenes': [{'t': t, 'id': n, 'descr': d} for t, n, d in SCENES]}
    p = os.path.join(ROOT, 'scripts', 'a2', 'sgcx_map.json')
    json.dump(m, open(p, 'w'), ensure_ascii=False, indent=1)
    print('✓', os.path.relpath(p, ROOT))


if __name__ == '__main__':
    args = sys.argv[1:]
    todo = set(a.lstrip('-') for a in args) or {'fonts', 'parade', 'scenes', 'speakers',
                                                'hero', 'map'}
    if 'fonts' in todo:
        print('· шрифты'); fonts()
    if 'parade' in todo:
        print('· парад'); parade()
    if 'scenes' in todo:
        print('· сцены'); scenes()
    if 'speakers' in todo:
        print('· спикеры'); speakers()
    if 'hero' in todo:
        print('· луп героя'); hero_loop()
    if 'map' in todo:
        write_map()
    webp()
