#!/usr/bin/env python3
"""Ассеты кейса «Концепция новогоднего календаря Saint-Gobain».

Источники:
  • презентация ~/Downloads/SGabainCalendar_pres 2.pdf, 7 полос. Картинки внутри
    лежат в CMYK, поэтому берём их не рендером страницы, а напрямую из потока
    (extract_image) и конвертируем в RGB: рендер страницы пережал бы мокапы
    до 1920 px, а в потоке они по 5-6 тысяч пикселей;
  • отдельные мокапы подарков ~/Downloads/sg-calendar-{box,card,markers}.png.
    На полосе «Подарки» коробка и открытка стоят частично за краем кадра, и любой
    кроп из презентации резал орнамент. Эти три файла — те же мокапы целиком,
    поэтому раскраска и подарки собираются из них, а не из PDF.

Что делает:
  1. вынимает 7 растров из PDF и раскладывает по смыслу;
  2. режет композиции: полоса с тремя мокапами календаря и полоса с тремя
     вариантами конструкции (1/2/4 пружины) — каждый мокап отдельным кадром;
  3. готовит два листа-раскраски с прозрачным фоном: линия остаётся, бумага
     уходит в альфу. Под такой PNG на странице кладётся canvas, и посетитель
     закрашивает рисунок фирменными цветами, не пачкая линию;
  4. вырезает знак Saint-Gobain с белой подложки в PNG с альфой.

Итог: mirror/images/sgcalendar/. После прогона — scripts/gen-webp.sh mirror/images/sgcalendar
Идемпотентно, просто перезаписывает.
"""
import io
import os

import fitz
import numpy as np
from PIL import Image

SRC = os.path.expanduser('~/Downloads/SGabainCalendar_pres 2.pdf')
MOCKS = {k: os.path.expanduser(f'~/Downloads/sg-calendar-{k}.png')
         for k in ('box', 'card', 'markers')}
DST = 'mirror/images/sgcalendar'

os.makedirs(DST, exist_ok=True)


def sources():
    """{ключ: RGB-картинка} — по одному растру на полосу, кроме полосы «Идея»."""
    doc = fitz.open(SRC)
    out = {}
    order = {1: ['pencils'], 2: ['narwhal', 'flamingo', 'footballer'],
             3: ['calendar'], 4: ['builds'], 5: ['gifts']}
    for i, page in enumerate(doc, start=1):
        for j, im in enumerate(page.get_images(full=True)):
            info = doc.extract_image(im[0])
            pic = Image.open(io.BytesIO(info['image'])).convert('RGB')
            out[order[i][j]] = pic
    return out


def save(im, name, maxw, q=88):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    if name.endswith('.png'):
        im.save(p, 'PNG', optimize=True)
    else:
        im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    print('  ', name, im.size, f'{os.path.getsize(p) // 1024} КБ')


def cut(im, box):
    w, h = im.size
    l, t, r, b = box
    return im.crop((round(w * l), round(h * t), round(w * r), round(h * b)))


# ─── кадры внутри композиций: (ключ источника, файл, кроп, ширина) ───────────
# кропы сняты по фактическим границам объектов (профиль «пиксель отличается от
# фона») плюс поле в полпроцента, иначе у мокапов срезает край листа
CROPS = [
    # полоса 3: три мокапа календаря рядом
    ('calendar', 'mock-gyproc.jpg', (0.030, 0.068, 0.415, 1.000), 1200),
    ('calendar', 'mock-isover.jpg', (0.518, 0.122, 0.713, 0.886), 900),
    # мокап обложки на этой полосе обрезан правым краем кадра — он собирается
    # ниже из отдельного файла, см. CLEAN
    # полоса 4: 1 / 2 / 4 пружины
    ('builds', 'build-1.jpg', (0.127, 0.112, 0.339, 0.950), 780),
    ('builds', 'build-2.jpg', (0.388, 0.112, 0.600, 0.950), 780),
    ('builds', 'build-4.jpg', (0.652, 0.112, 0.865, 0.950), 780),
]

# ─── отдельные мокапы подарков: (файл-источник, файл, кроп, ширина) ──────────
# кроп только по белым полям вокруг предмета, сам предмет не режем
CLEAN = [
    ('box',     'mock-cover.jpg', (0.100, 0.015, 0.960, 1.000), 900),
    ('card',    'card.jpg',       (0.285, 0.015, 0.800, 0.990), 900),
    ('markers', 'markers.jpg',    (0.200, 0.020, 0.820, 0.990), 900),
]

# ─── листы-раскраски: (файл-источник, файл, кроп) ────────────────────────────
# берём орнамент целиком, с полем в пару процентов: посетитель закрашивает ровно
# то, что напечатано на обложке и на открытке, без обреза по краю
SHEETS = [
    ('card', 'sheet-card.png',  (0.291, 0.472, 0.614, 0.824)),
    ('box',  'sheet-cover.png', (0.203, 0.238, 0.745, 0.868)),
]

# знак Saint-Gobain: на обложке календаря он самый крупный и лежит на чистом белом
LOGO_BOX = (0.895, 0.800, 0.972, 0.868)


def lineart(im, black=95, white=225):
    """Бумага в альфу, линия остаётся.

    Рисунок отсканирован серым по чуть сероватой бумаге, поэтому не режем по
    порогу (сгрызло бы тонкие штрихи), а переводим яркость в прозрачность:
    чем темнее пиксель, тем плотнее альфа. Полутона на краях штриха сохраняются,
    и линия не рвётся на мелком масштабе.
    """
    lum = np.asarray(im.convert('L')).astype(np.float32)
    alpha = np.clip((white - lum) / (white - black), 0, 1)
    # LA вместо RGBA: цвет линии постоянный (графит), хранить три одинаковых
    # канала незачем — плотный дудл в RGBA весит вчетверо больше
    la = np.dstack([np.full_like(alpha, 26), alpha * 255]).round().astype(np.uint8)
    return Image.fromarray(la)


def keyed(im, white=238):
    """Знак с белой подложки: то же по смыслу, но цвет пикселя сохраняем —
    у знака градиент от мяты к оранжевому, перекрашивать его нельзя."""
    a = np.asarray(im).astype(np.float32)
    lum = np.asarray(im.convert('L')).astype(np.float32)
    alpha = np.clip((white - lum) / (white - 120), 0, 1)
    # цвет насыщаем обратно: полупрозрачный пиксель на белом выглядел бы блёклым
    with np.errstate(invalid='ignore', divide='ignore'):
        rgb = np.where(alpha[..., None] > 0.02,
                       (a - 255 * (1 - alpha[..., None])) / np.maximum(alpha[..., None], 1e-3),
                       a)
    rgba = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).round().astype(np.uint8)
    out = Image.fromarray(rgba)
    return out.crop(out.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox())


# ─── линия-город по карандашам ──────────────────────────────────────────────
# Знак Saint-Gobain — город, нарисованный одной ломаной. Коробка карандашей на
# первой полосе презентации даёт ровно такой же силуэт, с красным карандашом
# вместо самой высокой башни. Обводим верхние срезы карандашей и кладём линию
# на фото в герое: это утверждение кейса, а не украшение, поэтому линия должна
# совпадать с фотографией пиксель в пиксель, а не рисоваться на глаз.
SKY_TAIL = 130          # хвост вправо по нижней ступени, как «земля» в знаке
SKY_STEP = 16           # порог: на сколько пикселей срез должен уйти, чтобы это была новая башня
SKY_MIN = 16            # ступени короче — шум от теней между карандашами


def skyline(im):
    a = np.asarray(im.convert('RGB')).astype(int)
    h, w, _ = a.shape
    ink = (a.mean(2) < 238) | ((a.max(2) - a.min(2)) > 22)   # не бумага
    tops = np.full(w, h, dtype=float)
    for x in range(w):
        ys = np.nonzero(ink[:, x])[0]
        if len(ys):
            tops[x] = ys[0]
    last = int(np.nonzero(tops < h)[0][-1])
    t = tops[:last + 1]
    k = 9                                                     # медиана: сбить зубцы на фасках
    pad = np.pad(t, k // 2, mode='edge')
    t = np.array([np.median(pad[i:i + k]) for i in range(len(t))])

    runs, s = [], 0
    for i in range(1, len(t) + 1):
        if i == len(t) or abs(t[i] - np.median(t[s:i])) > SKY_STEP:
            runs.append((s, i, float(np.median(t[s:i]))))
            s = i
    runs = [r for r in runs if r[1] - r[0] >= SKY_MIN]

    d = []
    for x0, x1, y in runs:
        d.append(('M' if not d else 'L') + f'{x0} {round(y)}')
        d.append(f'L{x1} {round(y)}')
    d.append(f'L{min(w, runs[-1][1] + SKY_TAIL)} {round(runs[-1][2])}')
    return (f'<svg class="sg-sky" viewBox="0 0 {w} {h}" fill="none" aria-hidden="true" '
            'preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="sgSkyG" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#3FC8A9"/><stop offset=".28" stop-color="#34BDEC"/>'
            '<stop offset=".46" stop-color="#1350E0"/><stop offset=".56" stop-color="#7A28B0"/>'
            '<stop offset=".72" stop-color="#EE0F3F"/><stop offset="1" stop-color="#F5591D"/>'
            '</linearGradient></defs>'
            f'<path d="{"".join(d)}" stroke="url(#sgSkyG)" stroke-width="9" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')


if __name__ == '__main__':
    src = sources()
    print('исходники:', ', '.join(f'{k} {v.size[0]}×{v.size[1]}' for k, v in src.items()))

    print('целые кадры:')
    save(src['pencils'], 'pencils.jpg', 1300)
    save(src['narwhal'], 'idea-narwhal.jpg', 900)
    save(src['flamingo'], 'idea-flamingo.jpg', 900)
    save(src['footballer'], 'idea-footballer.jpg', 900)

    print('кадры из композиций:')
    for key, name, box, w in CROPS:
        save(cut(src[key], box), name, w)

    mock = {k: Image.open(p).convert('RGB') for k, p in MOCKS.items()}
    print('отдельные мокапы:', ', '.join(f'{k} {v.size[0]}×{v.size[1]}' for k, v in mock.items()))
    for key, name, box, w in CLEAN:
        save(cut(mock[key], box), name, w)

    # 760 px хватает: на странице лист занимает около 600 CSS-пикселей, а дудл
    # на обложке настолько плотный, что каждая лишняя сотня пикселей это +100 КБ
    print('листы-раскраски:')
    for key, name, box in SHEETS:
        save(lineart(cut(mock[key], box)), name, 760)

    print('знак:')
    save(keyed(cut(src['calendar'], LOGO_BOX)), 'logo-sg.png', 560)

    print('линия-город:')
    svg = skyline(Image.open(os.path.join(DST, 'pencils.jpg')))
    p = os.path.join(DST, 'skyline.svg')
    open(p, 'w', encoding='utf-8').write(svg)
    print('   skyline.svg', f'{len(svg)} байт, {svg.count("L")} ступеней')

    print('готово →', DST)
