#!/usr/bin/env python3
"""Обложка-квадрат карточки кейса «Презентация Changan CS35» (477x396).

Круг-постер для этого кейса дизайнер сделал ещё во времена Тильды, он лежит в
библиотеке и НЕ перерисовывается:
    /images/lib/as3635-3436-4663-b265-633363383261/__-98.png
    (зелёный круг, автомобиль под маппингом, 3D-блоки за границей круга)
Не хватало только пары под hover, поэтому скрипт рисует один квадрат в цвет
круга (#00751F, взят пипеткой из готовой обложки) по механике v2.2: фоновое
эхо «35» (модель CS35), вордмарк, заголовок и «СМОТРЕТЬ КЕЙС →».

Кладёт в mirror/images/lib/custom-changan/ (webp — через scripts/gen-webp.sh)."""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

W, H = 477, 396
OUT = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-changan')
CIRCLE = '/images/lib/as3635-3436-4663-b265-633363383261/__-98.png'  # готовый круг, для справки
os.makedirs(OUT, exist_ok=True)
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

GREEN = (0, 117, 31)     # цвет круга-постера
GREEN_D = (0, 74, 20)    # эхо на квадрате
WHITE = (255, 255, 255)
SS = 4


def font(sz, v='Bold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def wordmark(d, x, y, h_px, color, text='CHANGAN'):
    """Имя марки разрядкой: в вектор логотип клиента не вынуть, на площадке он
    набран капсом на баннерах."""
    f = font(h_px, 'ExtraBold')
    for ch in text:
        d.text((x, y), ch, font=f, fill=color)
        x += d.textbbox((0, 0), ch, font=f)[2] + h_px * 0.22


def cover_hover():
    S = SS
    img = Image.new('RGBA', (W * S, H * S), GREEN + (255,))
    d = ImageDraw.Draw(img)
    ef = font(int(340 * S), 'ExtraBold')
    eb = d.textbbox((0, 0), '35', font=ef)  # эхо модели: CS35
    d.text((W * S - (eb[2] - eb[0]) - int(20 * S) - eb[0],
            H * S - (eb[3] - eb[1]) - int(2 * S) - eb[1]), '35', font=ef, fill=GREEN_D + (255,))
    wordmark(d, int(34 * S), int(30 * S), int(17 * S), WHITE + (255,))
    hf = font(int(44 * S), 'ExtraBold')
    for i, ln in enumerate(['Презентация', 'CS35']):
        d.text((int(34 * S), int((150 + i * 54) * S)), ln, font=hf, fill=WHITE + (255,))
    sf = font(int(19 * S), 'Medium')
    d.text((int(34 * S), int(278 * S)), 'атриум ТЦ и 3D mapping шоу', font=sf, fill=WHITE + (205,))
    cf = font(int(20 * S), 'Bold')
    d.text((int(35 * S), int(338 * S)), 'СМОТРЕТЬ КЕЙС  →', font=cf, fill=WHITE + (255,))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    cover_hover().save(os.path.join(OUT, 'cover-hover.png'))
    print('written', os.path.join(OUT, 'cover-hover.png'))
    print('круг-постер берём готовый:', CIRCLE)
