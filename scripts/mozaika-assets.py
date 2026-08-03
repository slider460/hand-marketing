#!/usr/bin/env python3
"""Ассеты кейса «Мозаика» (/event/mozaika).

Источники:
  • ~/Downloads/FR_Mozaika_HM_FIN.pdf — наш финальный отчёт о проведении
    мероприятия от 08.11.2018, 25 полос со съёмкой вечера. Это главный
    источник: страница строится на реальных кадрах, а не на референсах;
  • ~/Downloads/Mosaika8_10_2018.pdf — презентация идеи, которую показывали
    клиенту до вечера. Из неё берём ровно две вещи: логотип «Мозаики»
    кривыми (в углу каждой полосы он лежит одним путём из 75 сегментов)
    и рендер стены-логотипа, чтобы поставить замысел рядом с результатом.

Что делает:
  1. вынимает потоки кадров: на полосах отчёта поверх фотографий лежат
     заголовки и затемняющие плашки макета, а сам поток чистый;
  2. считает сетку ламповых гнёзд по контуру логотипа. Решётка ровная, без
     смещения строк, и гнездо ставится только там, где буква заполнена почти
     целиком: иначе крупные лампы съедают штрихи и «Мозаика» перестаёт
     читаться. Шаг 36 даёт около 340 гнёзд, как на самой панели;
  3. вынимает план зала (полоса «Площадка»): 349 путей белой схемы плюс
     подписи зон с координатами, чтобы перерисовать план живым SVG.

Итог: mirror/images/mozaika/ + logo.json (контур, патроны) + plan.json (схема).
После прогона — scripts/gen-webp.sh mirror/images/mozaika
Идемпотентно, просто перезаписывает.
"""
import io
import json
import os

import fitz
import numpy as np
from PIL import Image

REPORT = os.path.expanduser('~/Downloads/FR_Mozaika_HM_FIN.pdf')
CONCEPT = os.path.expanduser('~/Downloads/Mosaika8_10_2018.pdf')
DST = 'mirror/images/mozaika'
MAXW = 1600
GUESTS = 134          # столько человек было на вечере (из финального отчёта)
STAFF = 6             # гнёзда организаторов, последнее из них достаётся спикеру
STEP = 36             # шаг решётки гнёзд: мельче — знак читается, крупнее — расползается

os.makedirs(DST, exist_ok=True)
rep = fitz.open(REPORT)
con = fitz.open(CONCEPT)

# ─── кадры отчёта: (файл, xref, кроп в долях, качество) ─────────────────────
SHOTS = [
    ('wall-lit',   172, None, 88),          # собранная стена горит целиком
    ('wall-empty', 236, None, 88),          # панель с пустыми гнёздами и первыми лампами
    ('lighting',    28, None, 86),          # лампочку вкручивают в стену
    ('handover',    62, None, 86),          # проводник света отдаёт лампочку гостю
    ('hall-blue',    4, None, 84),          # зал в синем монохроме, идёт презентация
    ('task',         8, None, 84),          # выступление, зал слушает
    ('host',        56, None, 84),          # ведущий открывает вечер, справа стена
    ('official',    69, None, 84),          # официальная часть
    ('reception',   46, None, 84),          # встреча гостей на ресепшене
    ('welcome',     51, None, 84),          # сбор гостей, велком-дринк
    ('catering',    74, None, 84),          # фуршет
    ('lottery',     82, None, 84),          # лотерея на сцене
    ('gift',        86, None, 86),          # фонарики-пауэрбанки в подарок
    ('badges',      92, None, 86),          # именные бейджи
    ('tags',       115, None, 86),          # гардеробные бирки
    ('presswall',  124, None, 86),          # пресс-волл
    ('video',      129, None, 84),          # ролик об объекте на экране
    ('screen',     133, None, 84),          # заставка с новым знаком и слоганом
    ('hall-color', 168, None, 84),          # зал после Момента Х, свет цветной
    ('team',       166, None, 84),          # общий кадр команды в финале вечера
]

# ─── кадры презентации идеи ─────────────────────────────────────────────────
# рендер режем по знаку: рядом с кадром с вечера он должен идти в том же
# масштабе, иначе шторка сравнивает не концепцию с результатом, а поля с полями
CONCEPT_SHOTS = [
    ('concept-wall', 20, (.16, .13, .87, .93), 86),   # рендер стены из презентации
]

LOGO_RECT = (102, 117, 224.003, 226.542)


def save(im, name, q=86):
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    if name.endswith('.png'):
        im.save(p, optimize=True)
    else:
        im.convert('RGB').save(p, quality=q, subsampling=0, optimize=True)
    print(f'  {name:<20} {im.size[0]}×{im.size[1]}  {os.path.getsize(p)//1024} KB')


def stream(doc, xref, crop=None):
    im = Image.open(io.BytesIO(doc.extract_image(xref)['image']))
    if crop:
        w, h = im.size
        im = im.crop((round(crop[0] * w), round(crop[1] * h),
                      round(crop[2] * w), round(crop[3] * h)))
    return im


def shots():
    print('кадры вечера:')
    for name, xref, crop, q in SHOTS:
        save(stream(rep, xref, crop), name + '.jpg', q)
    print('кадры презентации идеи:')
    for name, xref, crop, q in CONCEPT_SHOTS:
        save(stream(con, xref, crop), name + '.jpg', q)


def render(doc, page_no, rect, zoom=2.0):
    page = doc[page_no]
    clip = fitz.Rect(*rect) & page.rect
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
    return Image.open(io.BytesIO(pix.tobytes('png')))


# ─── логотип кривыми ────────────────────────────────────────────────────────
def logo_path():
    """Контур логотипа одним path d, в системе 0..1000 по ширине."""
    page = con[1]
    dr = [d for d in page.get_drawings() if len(d['items']) == 75][0]
    x0, y0, x1, y1 = LOGO_RECT
    k = 1000 / (x1 - x0)

    def pt(p):
        return f'{(p.x - x0) * k:.2f} {(p.y - y0) * k:.2f}'

    out, cur = [], None
    for it in dr['items']:
        a = it[1]
        if cur is None or abs(a.x - cur.x) > .01 or abs(a.y - cur.y) > .01:
            out.append(f'M{pt(a)}')
        if it[0] == 'l':
            out.append(f'L{pt(it[2])}')
            cur = it[2]
        elif it[0] == 'c':
            out.append(f'C{pt(it[2])} {pt(it[3])} {pt(it[4])}')
            cur = it[4]
    return ' '.join(out) + 'Z', round((y1 - y0) * k, 2)


def logo_mask(zoom=8.0):
    """Растр логотипа со второй полосы презентации: лайм на малиновом."""
    im = render(con, 1, LOGO_RECT, zoom).convert('RGB')
    a = np.asarray(im).astype(int)
    return (a[:, :, 1] > 150) & (a[:, :, 2] < 120), im.size


def sockets(step, mask, size, margin=0.12):
    """Гнёзда: ровная решётка по маске логотипа, без сдвига строк.

    margin — сколько площади вокруг узла может выходить за букву. Держим
    жёстко: гнездо, наполовину висящее за контуром, размывает силуэт знака.
    """
    W, H = size
    k = W / 1000.0
    r = step * k * .5
    pts, y = [], step * .62
    while y * k < H:
        x = step * .62
        while x * k < W:
            px, py = int(x * k), int(y * k)
            sl = mask[max(0, int(py - r)):int(py + r), max(0, int(px - r)):int(px + r)]
            if sl.size and sl.mean() >= 1 - margin:
                pts.append((round(x, 1), round(y, 1)))
            x += step
        y += step
    return pts


def logo():
    d, h = logo_path()
    mask, size = logo_mask()
    pts = sockets(STEP, mask, size)
    data = {'d': d, 'w': 1000, 'h': h, 'step': STEP, 'guests': GUESTS,
            'staff': STAFF, 'sockets': [list(p) for p in pts]}
    json.dump(data, open(os.path.join(DST, 'logo.json'), 'w'),
              ensure_ascii=False, separators=(',', ':'))
    print(f'  logo.json            контур {len(d)} симв., гнёзд {len(pts)}, '
          f'шаг {STEP}, вьюбокс 1000×{h}')


# ─── план зала ──────────────────────────────────────────────────────────────
def plan():
    """Схема зала из полосы «Площадка»: пути + подписи зон."""
    page = rep[6]
    draws = [d for d in page.get_drawings()
             if d['rect'].width < 1500 and d['rect'].x0 > 700]
    x0 = min(d['rect'].x0 for d in draws); y0 = min(d['rect'].y0 for d in draws)
    x1 = max(d['rect'].x1 for d in draws); y1 = max(d['rect'].y1 for d in draws)
    k = 1000 / (x1 - x0)

    def pt(p):
        return f'{(p.x - x0) * k:.1f} {(p.y - y0) * k:.1f}'

    segs = []
    for d in draws:
        cur = None
        for it in d['items']:
            if it[0] == 're':
                r = it[1]
                segs.append(f'M{pt(r.top_left)} L{pt(r.top_right)} '
                            f'L{pt(r.bottom_right)} L{pt(r.bottom_left)}Z')
                cur = None
                continue
            if it[0] == 'qu':
                q = it[1]
                segs.append(f'M{pt(q.ul)} L{pt(q.ur)} L{pt(q.lr)} L{pt(q.ll)}Z')
                cur = None
                continue
            a = it[1]
            if cur is None or abs(a.x - cur.x) > .01 or abs(a.y - cur.y) > .01:
                segs.append(f'M{pt(a)}')
            if it[0] == 'l':
                segs.append(f'L{pt(it[2])}'); cur = it[2]
            elif it[0] == 'c':
                segs.append(f'C{pt(it[2])} {pt(it[3])} {pt(it[4])}'); cur = it[4]
    # пути сливаем в один: правило nonzero само делает вырезы, и схема читается
    # так же, как в макете (поле зала залито, стены и подписи выбраны дырками)
    data = {'d': ' '.join(segs) + 'Z', 'w': 1000, 'h': round((y1 - y0) * k, 1)}
    json.dump(data, open(os.path.join(DST, 'plan.json'), 'w'),
              ensure_ascii=False, separators=(',', ':'))
    print(f'  plan.json            путей {len(draws)}, '
          f'вьюбокс 1000×{data["h"]}')


def cleanup():
    """Стоковые референсы первой версии страницы: на реальной съёмке не нужны."""
    old = ['dark', 'light', 'gather', 'invite', 'guard', 'wall', 'flash',
           'ledgrid', 'wallcolor', 'party', 'guests', 'tunnel']
    for n in old:
        for ext in ('.jpg', '.jpg.webp'):
            p = os.path.join(DST, n + ext)
            if os.path.exists(p):
                os.remove(p)
                print('  удалён', n + ext)


if __name__ == '__main__':
    shots()
    print('векторы:')
    logo()
    plan()
    cleanup()
