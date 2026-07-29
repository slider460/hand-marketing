#!/usr/bin/env python3
"""Ассеты кейса «Ком подарков» — BTL-кампания для ТРЦ «Саларис» (Christmas 2020).

Источник: ~/Downloads/SalarisXmas2020_FIN 2.pdf, 22 рабочие полосы 2000×1200
(с 23-й идёт общая информация об агентстве, она в кейс не входит).

Особенность исходника: на каждой полосе ровно одна растровая картинка 3–4 тыс. px
и текст поверх неё вектором. Поэтому визуалы вынимаются оригиналами, без надписей
и без пересъёмки слайда — extract_image, а не рендер страницы.

Что делает:
  1. вынимает знак «Саларис» (спираль — градиент под клипом, слово — кривые):
     рендерим угол первой полосы и снимаем плоский фиолетовый фон в альфу;
  2. режет ком подарков с ровного лаймового фона полосы 20 — на странице он
     лежит PNG с прозрачностью поверх фиолетового первого экрана;
  3. сохраняет визуалы полос в JPEG (+ маленькие превью для сетки коммуникаций).

Итог: mirror/images/salaris-xmas/. После прогона — scripts/gen-webp.sh mirror/images/salaris-xmas
Идемпотентно, просто перезаписывает.
"""
import io
import os

import fitz
import numpy as np
from PIL import Image, ImageFilter

SRC = os.path.expanduser('~/Downloads/SalarisXmas2020_FIN 2.pdf')
DST = 'mirror/images/salaris-xmas'

BRAND = (76, 54, 148)     # фирменный фиолетовый первой полосы
LIME = (177, 222, 89)     # фон полосы 20, с которого режем ком подарков

os.makedirs(DST, exist_ok=True)
doc = fitz.open(SRC)

# ─── визуалы полос: (полоса, имя, ширина в пикселях) ─────────────────────────
# Ширину держим по месту на странице: герои секций крупнее, сетка носителей мельче.
SHOTS = [
    (2,  'balls-pink',   1800),   # бриф: шары на розовом
    (3,  'clock',        1800),   # сроки: часы из шаров
    (4,  'trees',        1800),   # инсайт: ёлки на красном
    (5,  'kom-green',    1800),   # идея: зелёный ком подарков
    (6,  'step-card',    1400),   # 1. Купи — карта участника
    (7,  'step-site',    1400),   # 2. Активируй — сайт акции
    (8,  'step-coins',   1400),   # 3. Копи баллы — монеты salar
    (9,  'step-team',    1400),   # 4. Прибавляй — коробка шаров
    (10, 'step-gifts',   1400),   # 5. Подарки — коробочки
    (11, 'step-draw',    1400),   # 6. Розыгрыш — машинка
    (12, 'gifts-belt',   1600),   # три группы подарков на конвейере
    (13, 'photo-studio', 1200),   # фотосессия в студии
    (14, 'dinner',       1200),   # ужин в ресторане
    (15, 'volvo',        1400),   # розыгрыш: брендированный кроссовер (PNG с альфой)
    (16, 'disco',        1600),   # ивент: дискошар
    (17, 'pos',          1400),   # POS: лайтбокс и ролл-ап
    (18, 'corner',       1400),   # промо-корнер
    (19, 'billboard',    1400),   # билборд
    (20, 'decor',        1400),   # подвесное оформление
    (21, 'wifi',         1400),   # экран WiFi-авторизации
    (22, 'sponsor',      1400),   # инфоспонсор Marie Claire
]

# ─── ком подарков с полосы 20 (бокс в координатах картинки 4003×2400) ────────
# На полосе три кома внахлёст и нити подвеса; берём передний красный, а соседей
# и нити снимаем по каналам — у них синего больше, чем красного.
KOM_BOX = (760, 560, 2980, 2400)


def page_image(no):
    """Единственная растровая картинка полосы — оригиналом, без текста поверх."""
    xref = doc[no - 1].get_images(full=True)[0][0]
    d = doc.extract_image(xref)
    im = Image.open(io.BytesIO(d['image']))
    if d.get('smask'):
        m = Image.open(io.BytesIO(doc.extract_image(d['smask'])['image'])).convert('L')
        im = im.convert('RGB')
        im.putalpha(m.resize(im.size, Image.LANCZOS))
        return im
    return im.convert('RGB')


def save(im, name, maxw, q=84):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    png = im.mode == 'RGBA'
    p = os.path.join(DST, name + ('.png' if png else '.jpg'))
    if png:
        im.save(p, 'PNG', optimize=True)
    else:
        im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    print('  ', name, im.size, f'{os.path.getsize(p) // 1024} КБ')


def unmix(im, bg, soft=26.0, hard=64.0):
    """Плоский фон в альфу: чем ближе пиксель к фону, тем он прозрачнее.

    Объекты (комы подарков, знак) далеко от фона по цвету, поэтому простого
    расстояния хватает; мягкая полка soft…hard оставляет ровный край без каймы.
    """
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    dist = np.sqrt(((a - np.array(bg, dtype=np.float32)) ** 2).sum(axis=2))
    alpha = np.clip((dist - soft) / (hard - soft), 0.0, 1.0)
    out = np.dstack([a, alpha * 255.0]).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')


def crop_alpha(im):
    """Обрезает прозрачные поля по краям."""
    box = im.getbbox()
    return im.crop(box) if box else im


def logo():
    """Знак «Саларис»: спираль-градиент и слово кривыми лежат на плоском фоне.

    Разложить их по слоям нельзя (спираль — растровый градиент под клипом),
    поэтому рендерим угол полосы в 6× и снимаем фиолетовый фон в альфу.
    """
    clip = fitz.Rect(95, 175, 520, 470)
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(6, 6), clip=clip, alpha=False)
    im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    save(crop_alpha(unmix(im, BRAND, soft=30, hard=90)), 'logo-salaris', 900)


def kom():
    im = unmix(page_image(20).crop(KOM_BOX), LIME, soft=34, hard=96)
    a = np.asarray(im).astype(np.int16)
    a[..., 3] = np.where(a[..., 2] > a[..., 0] * 0.95, 0, a[..., 3])   # соседние комы
    # нити подвеса — линии в несколько пикселей; морфологическое размыкание
    # (эрозия + дилатация) стирает их целиком и не трогает сплошной ком
    alpha = Image.fromarray(a[..., 3].astype(np.uint8), 'L')
    opened = alpha.filter(ImageFilter.MinFilter(9)).filter(ImageFilter.MaxFilter(9))
    a[..., 3] = np.where(np.asarray(opened) > 0, a[..., 3], 0)
    # 1000 px хватает: на первом экране ком занимает ~500 CSS-пикселей даже на 2x,
    # а PNG с прозрачностью и градиентами весит заметно дороже JPEG
    save(crop_alpha(Image.fromarray(a.astype(np.uint8))), 'kom-red', 1000)


if __name__ == '__main__':
    print('знак:')
    logo()
    print('ком подарков:')
    kom()
    print('визуалы полос:')
    for no, name, w in SHOTS:
        im = page_image(no)
        save(im, name, w)
        if name in ('pos', 'corner', 'billboard', 'decor', 'wifi', 'sponsor'):
            save(im, 'thumb-' + name, 420, q=78)
    print('готово →', DST)
