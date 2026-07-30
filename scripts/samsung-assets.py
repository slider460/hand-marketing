#!/usr/bin/env python3
"""Ассеты кейса «Новый год Samsung 2020» (event).

Источники:
  1. 38 фотографий вечера, лежащих в mirror/images/lib/as*/ после миграции с Тильды
     (два фотографа: файлы 061219Samsung_* и JAN_*);
  2. media/samsung-2020.mp4 — ролик вечера, из него берём кадры монтажа
     (фермы, пустой зал, юстировка проекции) и кадры самого контента.

Что делает:
  • раскладывает галерею в порядке хода вечера: g-01..g-38 (1600 px) + миниатюры
    t-01..t-38 (480 px);
  • кладёт именованные кадры для секций страницы (панорама зала, сетка над сценой,
    почтовый ящик с видимым проектором, олени, торт, финал);
  • вынимает из ролика кадры монтажа build-1..4, кадры контента content-1..2
    и постер для видеоблока.

Итог: mirror/images/samsung/. После прогона — scripts/gen-webp.sh mirror/images/samsung
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

os.makedirs(DST, exist_ok=True)

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
    for i, base in enumerate(GALLERY, 1):
        im = Image.open(find(base)).convert('RGB')
        w, h = save(im.copy(), f'g-{i:02d}.jpg', 1600, 82)
        save(im.copy(), f't-{i:02d}.jpg', 480, 76)
        sizes.append((f'g-{i:02d}.jpg', w, h))
    return sizes


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
    print('готово:', len(g), 'фото галереи,', len(n), 'кадров секций,', len(f), 'из ролика')
    print('дальше: scripts/gen-webp.sh mirror/images/samsung')
