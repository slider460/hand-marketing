#!/usr/bin/env python3
"""Ассеты кейса «Новый год Samsung 2020» (event).

Источники:
  1. 38 фотографий вечера, лежащих в mirror/images/lib/as*/ после миграции с Тильды
     (два фотографа: файлы 061219Samsung_* и JAN_*);
  2. media/samsung-2020.mp4 — ролик вечера, из него берём кадры монтажа
     (фермы, пустой зал, юстировка проекции) и кадры самого контента;
  3. ~/Downloads/Самсунг/ — съёмка с площадки самим агентством (30.07.2026):
     видео сброса сетки с пульта, видео зоны почтового ящика и 7 фотографий,
     включая рабочее место оператора с медиасервером.

Что делает:
  • раскладывает галерею в порядке хода вечера: g-01..g-45 (1600 px) + миниатюры
    t-01..t-45 (480 px), последние 7 кадров это съёмка с площадки;
  • кладёт именованные кадры для секций страницы (панорама зала, сетка над сценой,
    почтовый ящик с видимым проектором, олени, торт, финал, пульт);
  • вынимает из ролика кадры монтажа build-1..5, кадры контента content-1..2
    и постер для видеоблока;
  • режет и жмёт два клипа в mirror/videos/ (эта папка уезжает на хостинг вместе
    с mirror/**, ручная загрузка в /media не нужна):
      samsung-mesh-drop.mp4  — 5 с сброса сетки, снято с пульта
      samsung-mailbox.mp4    — 12 с зоны ящика, вертикальный кадр
    плюс покадровую раскадровку сброса drop-1..4 и кадры до/после.

Итог: mirror/images/samsung/ + mirror/videos/samsung-*.mp4.
После прогона — scripts/gen-webp.sh mirror/images/samsung
Идемпотентно, просто перезаписывает.
"""
import os
import glob
import subprocess
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LIB = os.path.join(ROOT, 'mirror', 'images', 'lib')
CASE = os.path.join(ROOT, 'mirror', 'case-assets')
VIDEO = os.path.join(ROOT, 'media', 'samsung-2020.mp4')
DST = os.path.join(ROOT, 'mirror', 'images', 'samsung')
VDST = os.path.join(ROOT, 'mirror', 'videos')
SHOT = os.path.expanduser('~/Downloads/Самсунг')   # съёмка с площадки

os.makedirs(DST, exist_ok=True)
os.makedirs(VDST, exist_ok=True)

# ─── Галерея: порядок = ход вечера, от встречи до конфетти ────────────────────
GALLERY = [
 'JAN_018-min', '061219Samsung_029-mi', 'JAN_055-min', '061219Samsung_030-mi',
 'JAN_041-min', 'JAN_007-min', '061219Samsung_022-mi', 'JAN_045-min',
 '061219Samsung_076-mi', '061219Samsung_083-mi', '061219Samsung_084-mi',
 '061219Samsung_244-mi', 'JAN_002-min', '061219Samsung_214-mi', 'JAN_001-min',
 'JAN_005-min', '061219Samsung_012-mi', 'JAN_064-min', '061219Samsung_096-mi',
 '061219Samsung_101-mi', 'JAN_113-min', '061219Samsung_180-mi', 'JAN_121-min',
 'JAN_209-min', 'JAN_148-min', 'JAN_108-min', 'JAN_247-min', 'JAN_254-min',
 '061219Samsung_366-mi', '061219Samsung_413-mi', '061219Samsung_399-mi',
 '061219Samsung_380-mi', '061219Samsung_430-mi', 'JAN_294-min',
 'd7703108_JAN_291', '061219Samsung_208-mi', 'JAN_034-min', '061219Samsung_014-mi',
]

# ─── Съёмка с площадки: (файл в ~/Downloads/Самсунг, имя кадра секции) ─────────
# эти же 7 кадров уходят в конец галереи (g-39..g-45)
PHONE = [
 ('IMG_1016.JPG', 'foh.jpg'),          # пульт: медиасервер и лист сцен
 ('IMG_1023.JPG', 'pano-1.jpg'),       # панорама леса по дуге, фигура над сценой
 ('IMG_1021.JPG', 'pano-2.jpg'),       # сцена сбоку, лес на полотнах
 ('IMG_1024.JPG', 'table.jpg'),        # вид со стола на панораму
 ('IMG_1028.JPG', 'screen-song.jpg'),  # экран с представлением спикера
 ('IMG_1037.JPG', 'hall-wide.jpg'),    # общий план зала и главного экрана
 ('IMG_1040.JPG', 'stage-color.jpg'),  # цветная графика на сцене и танцпол
]

# ─── Клипы с площадки: (файл, имя в mirror/videos, начало, длина, ширина, crf) ─
CLIPS = [
 ('сброс_сетки.mov', 'samsung-mesh-drop.mp4', 3.4, 5.0, 1280, 24),
 ('Ящик.MOV', 'samsung-mailbox.mp4', 2.5, 12.0, 620, 28),
]

# ─── Раскадровка сброса: (имя, секунда, обрезка l/t/r/b, подпись) ─────────────
# кадры для полосы обрезаны по порталу сцены, иначе на миниатюре ничего не видно
PORTAL = (0.22, 0.15, 0.82, 0.68)
DROP = [
 ('drop-before.jpg', 4.35, None, 'картинка идёт по полотну (постер видео)'),
 ('drop-1.jpg', 5.03, PORTAL, 'контент гаснет в белое'),
 ('drop-2.jpg', 5.13, PORTAL, 'полотно тёмное'),
 ('drop-3.jpg', 5.23, PORTAL, 'сброс: полотна в кадре нет'),
 ('drop-4.jpg', 5.60, PORTAL, 'сцена открыта, идёт дым'),
 ('drop-after.jpg', 7.90, None, 'логотип уже на экране за сценой'),
]

# ─── Постеры для клипов: (исходник, имя, секунда, ширина) ─────────────────────
POSTERS = [
 ('Ящик.MOV', 'mailbox-poster.jpg', 3.0, 720),
]

# ─── Именованные кадры секций: (имя, источник, ширина, обрезка l/t/r/b) ───────
NAMED = [
 ('hero.jpg',       '061219Samsung_083-mi', 1800, None),                 # панорама зала
 ('annot-hall.jpg', '061219Samsung_083-mi', 1400, None),                 # разбор: зал
 ('annot-stage.jpg', '061219Samsung_096-mi', 1400, None),                # разбор: сетка
 ('annot-mail.jpg', 'JAN_007-min',           980, (0.0, 0.02, 1.0, 1.0)),  # разбор: ящик
 ('mail-drop.jpg',  '061219Samsung_022-mi',  980, None),                 # открытка в ящик
 ('mail-cards.jpg', 'JAN_045-min',          1200, None),                 # стойка с открытками
 ('forest.jpg',     '061219Samsung_084-mi', 1400, None),                 # зал сверху
 ('hall2.jpg',      'JAN_002-min',          1400, None),                 # зал и полотно
 ('animals.jpg',    '061219Samsung_244-mi', 1200, None),                 # белые звери на стенах
 ('deer.jpg',       '061219Samsung_214-mi',  980, None),                 # золотые олени
 ('tree.jpg',       'JAN_001-min',          1200, None),                 # ёлка из частиц
 ('quiz.jpg',       '061219Samsung_366-mi', 1400, None),                 # табло конкурса
 ('cake.jpg',       '061219Samsung_399-mi', 1200, None),                 # торт
 ('finale.jpg',     'd7703108_JAN_291',     1400, None),                 # конфетти
 ('welcome.jpg',    'JAN_018-min',          1000, None),                 # встреча у дверей
 ('band.jpg',       'JAN_005-min',          1200, None),                 # оркестр-снежки
 ('mesh.jpg',       '061219Samsung_096-mi', 1600, None),                 # сетка крупно
]

# ─── Кадры из ролика: (имя, секунда, подпись для лога) ────────────────────────
FRAMES = [
 ('build-1.jpg',   11, 'зал до гостей: строительные леса и подвес приборов'),
 ('build-2.jpg',   20, 'техник на ферме заводит прибор'),
 ('build-3.jpg',   23, 'полотно над сценой на подвесе'),
 ('build-4.jpg',   27, 'сборка короба, в который спрятали УКФ-проектор'),
 ('build-5.jpg',   25, 'юстировка проекции на панорамное полотно'),
 ('content-1.jpg', 131, 'кадр контента: 50 years of experience'),
 ('content-2.jpg', 136, 'кадр контента: лента и снежинки'),
 ('poster.jpg',    40, 'постер видеоблока: логотип на сетке'),
]


def find(base):
    """Найти фото по имени файла в mirror/images/lib/as*/ или в case-assets."""
    hits = glob.glob(os.path.join(LIB, 'as*', base + '.jpg'))
    if hits:
        return hits[0]
    p = os.path.join(CASE, base + '.jpg')
    if os.path.exists(p):
        return p
    raise SystemExit('не найден источник: ' + base)


def save(im, name, maxw, q=82):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    print('  ', name, im.size, f'{os.path.getsize(p) // 1024} КБ')
    return im.size


def crop(im, box):
    if not box:
        return im
    l, t, r, b = box
    return im.crop((round(l * im.width), round(t * im.height),
                    round(r * im.width), round(b * im.height)))


def gallery():
    print('галерея:')
    sizes = []
    srcs = [find(b) for b in GALLERY]
    srcs += [os.path.join(SHOT, f) for f, _n in PHONE]   # съёмка с площадки в конец
    for i, p in enumerate(srcs, 1):
        if not os.path.exists(p):
            print('   пропуск, нет файла:', p)
            continue
        im = Image.open(p).convert('RGB')
        w, h = save(im.copy(), f'g-{i:02d}.jpg', 1600, 82)
        save(im.copy(), f't-{i:02d}.jpg', 480, 76)
        sizes.append((f'g-{i:02d}.jpg', w, h))
    return sizes


def phone():
    """Именованные кадры из съёмки с площадки."""
    if not os.path.isdir(SHOT):
        print('папки со съёмкой нет, кадры пропущены:', SHOT)
        return {}
    print('съёмка с площадки:')
    out = {}
    for src, name in PHONE:
        p = os.path.join(SHOT, src)
        if not os.path.exists(p):
            print('   пропуск:', src)
            continue
        out[name] = save(Image.open(p).convert('RGB'), name, 1600, 84)
    return out


def posters():
    """Постеры к клипам: первый осмысленный кадр."""
    if not os.path.isdir(SHOT):
        return {}
    print('постеры клипов:')
    out = {}
    tmp = os.path.join(DST, '_tmp.png')
    for src, name, sec, w in POSTERS:
        p = os.path.join(SHOT, src)
        if not os.path.exists(p):
            print('   пропуск:', src)
            continue
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(sec), '-i', p,
                        '-frames:v', '1', tmp], check=True)
        out[name] = save(Image.open(tmp).convert('RGB'), name, w, 82)
    if os.path.exists(tmp):
        os.remove(tmp)
    return out


def clips():
    """Клипы в mirror/videos: сброс сетки и зона ящика."""
    if not os.path.isdir(SHOT):
        return {}
    print('клипы:')
    out = {}
    for src, name, ss, dur, w, crf in CLIPS:
        p = os.path.join(SHOT, src)
        if not os.path.exists(p):
            print('   пропуск:', src)
            continue
        dst = os.path.join(VDST, name)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur),
                        '-i', p, '-an', '-vf', f'scale={w}:-2', '-c:v', 'libx264',
                        '-crf', str(crf), '-preset', 'slow', '-pix_fmt', 'yuv420p',
                        '-movflags', '+faststart', dst], check=True)
        kb = os.path.getsize(dst) // 1024
        print('  ', name, f'{dur:g} с, {kb} КБ')
        out[name] = kb
    return out


def drop():
    """Раскадровка сброса сетки: кадры до, во время и после."""
    p = os.path.join(SHOT, 'сброс_сетки.mov')
    if not os.path.exists(p):
        print('видео сброса не найдено, раскадровка пропущена')
        return {}
    print('раскадровка сброса:')
    out = {}
    tmp = os.path.join(DST, '_tmp.png')
    for name, sec, box, note in DROP:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(sec), '-i', p,
                        '-frames:v', '1', tmp], check=True)
        im = crop(Image.open(tmp).convert('RGB'), box)
        out[name] = save(im, name, 1280, 84)
        print('       ', note)
    os.remove(tmp)
    return out


def named():
    print('кадры секций:')
    out = {}
    for name, base, maxw, box in NAMED:
        im = crop(Image.open(find(base)).convert('RGB'), box)
        out[name] = save(im, name, maxw, 84)
    return out


def frames():
    """Кадры из ролика вечера: монтаж, контент, постер."""
    if not os.path.exists(VIDEO):
        print('ролик не найден, кадры монтажа пропущены:', VIDEO)
        return {}
    print('кадры из ролика:')
    out = {}
    tmp = os.path.join(DST, '_tmp.png')
    for name, sec, note in FRAMES:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(sec), '-i', VIDEO,
                        '-frames:v', '1', tmp], check=True)
        im = Image.open(tmp).convert('RGB')
        out[name] = save(im, name, 1280, 82)
        print('       ', note)
    os.remove(tmp)
    return out


if __name__ == '__main__':
    g = gallery()
    n = named()
    f = frames()
    p = phone()
    d = drop()
    d.update(posters())
    c = clips()
    print('готово:', len(g), 'фото галереи,', len(n) + len(p), 'кадров секций,',
          len(f), 'из ролика,', len(d), 'кадров сброса,', len(c), 'клипа')
    print('дальше: scripts/gen-webp.sh mirror/images/samsung')
