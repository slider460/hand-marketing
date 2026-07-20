#!/usr/bin/env python3
"""Подготовка ассетов кейса Becar × Private Money Expo Forum 2021.
Источник: ~/Downloads/Bacar_pravedMoney → mirror/images/becar-pm/
Фото 7952px → 2000w q85; рендеры 2560 → 1920w; PDF-страницы → jpg.
Идемпотентно (перезаписывает). После — прогнать scripts/gen-webp.sh mirror/images/becar-pm
"""
import os
import fitz
from PIL import Image

SRC = os.path.expanduser('~/Downloads/Bacar_pravedMoney')
DST = 'mirror/images/becar-pm'
os.makedirs(DST, exist_ok=True)

def save_resized(src, out, maxw, q=85):
    im = Image.open(src).convert('RGB')
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(DST, out), 'JPEG', quality=q, optimize=True, progressive=True)
    print('photo', out, im.size)

# Фото застройки и работы стенда
PHOTOS = {
    'Becar_081.jpg': 'photo-team.jpg',         # команда Becar на стенде (hero, замена 20.07)
    'Becar_141.jpg': 'photo-talks.jpg',        # переговоры на стенде (Смайл/GrowUp)
    'Becar_145.jpg': 'photo-lounge.jpg',       # лаунж-зона, синяя стена Дубая
    'Becar_179.jpg': 'photo-stage-hall.jpg',   # зал: на экране НАШ слайд (замена Becar_180, 20.07)
    'Becar_211.jpg': 'photo-stand-full.jpg',   # общий вид построенного стенда
    'Becar_223.jpg': 'photo-speaker.jpg',      # спикер у стены You&Co
    'Becar_235.jpg': 'photo-award.jpg',        # награда PME2021 + папка «Доходные инвестиции»
    'Becar_255.jpg': 'photo-crowd.jpg',        # поток гостей у стенда
    'Becar_258.jpg': 'photo-stage-tops.jpg',   # топ-менеджеры на сцене
}
for src, out in PHOTOS.items():
    save_resized(os.path.join(SRC, src), out, 2000)

# Финальные 3D-рендеры
RENDERS = {
    'stand54.jpg': 'render-front.jpg',
    'stand544.jpg': 'render-top.jpg',
    'stand5444.jpg': 'render-detail.jpg',
}
for src, out in RENDERS.items():
    save_resized(os.path.join(SRC, src), out, 1920, q=88)

def pdf_page(doc, idx, out, zoom=2.0, crop_top=0.0, crop_bottom=0.0, maxw=1600, q=85):
    page = doc[idx]
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    t = round(im.height * crop_top); b = im.height - round(im.height * crop_bottom)
    im = im.crop((0, t, im.width, b))
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(DST, out), 'JPEG', quality=q, optimize=True, progressive=True)
    print('pdf', out, im.size)

# Эскизные варианты стенда (плашку «Вариант N» сверху срезаем)
d = fitz.open(os.path.join(SRC, 'stand_draft.pdf'))
SKETCH = [(0, 'sketch-v1-a.jpg'), (1, 'sketch-v1-b.jpg'), (2, 'sketch-v1-c.jpg'),
          (3, 'sketch-v2-a.jpg'), (4, 'sketch-v2-b.jpg'), (5, 'sketch-v2-c.jpg')]
for idx, out in SKETCH:
    pdf_page(d, idx, out, crop_top=0.135)
d.close()

# Слайды презентации для сцены
d = fitz.open(os.path.join(SRC, 'на сцену дубай 2021.pdf'))
SLIDES = [(0, 'slide-1.jpg'), (3, 'slide-2.jpg'), (4, 'slide-3.jpg'),
          (7, 'slide-4.jpg'), (15, 'slide-5.jpg'), (18, 'slide-6.jpg')]
for idx, out in SLIDES:
    pdf_page(d, idx, out, zoom=1.5, maxw=1400)
d.close()
print('done')
