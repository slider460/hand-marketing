#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Цифровое производство» (Московская школа управления СКОЛКОВО).

Источник: ~/Downloads/Цифровое__производство30октябрь2017.pdf — рабочий доклад
Департамента корпоративного обучения, 86 полос A4, редакция от 30.10.2017.
Файл сверстан одиночными полосами, поэтому развороты склеиваем сами:
полоса N лежит на странице файла N+2 (страница 1 файла — обложка).

Что делает:
  1. рендерит обложку и склеивает 12 разворотов + миниатюры для ленты;
  2. вырезает инфографику по подписи «Рисунок N.»: подпись стоит НАД схемой,
     значит режем от неё до низа полосы за вычетом колонцифры. Так кадр всегда
     приходит вместе с родной подписью издания, ничего не подбирая руками;
  3. вынимает четыре фотографии с обложки (они там единственные растры крупнее
     600 px, остальные 137 картинок на полосе — это плашки логотипа СКОЛКОВО);
  4. рендерит логотип СКОЛКОВО с шапки полосы в прозрачный PNG;
  5. копирует четыре мокапа из ассетов старой страницы кейса, обрезая пустые поля.

Итог: mirror/images/skolkovo/. После прогона — scripts/gen-webp.sh mirror/images/skolkovo
Идемпотентно, просто перезаписывает.
"""
import io
import os

import fitz
from PIL import Image

SRC = os.path.expanduser('~/Downloads/Цифровое__производство30октябрь2017.pdf')
DST = 'mirror/images/skolkovo'
MOCKUPS_SRC = 'site/src/assets/projects/creative__skolkovo'

PAGE_PX = 1500          # одна полоса A4 в листалке
FIG_PX = 1600           # кадр инфографики
COVER_PX = 1200

os.makedirs(DST, exist_ok=True)


def save(im, name, maxw, q=88, fmt='JPEG'):
    if fmt == 'JPEG' and im.mode != 'RGB':
        im = im.convert('RGB')
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    if fmt == 'JPEG':
        im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    else:
        im.save(p, fmt, optimize=True)
    print('  ', name, im.size, f'{os.path.getsize(p)//1024} КБ')


def render(page, width):
    zoom = width / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')


def spread(doc, left_folio):
    """Склейка разворота по номеру ЛЕВОЙ полосы: полоса N — страница N+2."""
    a = render(doc[left_folio + 1], PAGE_PX)
    b = render(doc[left_folio + 2], PAGE_PX)
    out = Image.new('RGB', (a.width + b.width, max(a.height, b.height)), 'white')
    out.paste(a, (0, 0))
    out.paste(b, (a.width, 0))
    return out


# ─── развороты листалки: (левая полоса, глава, заголовок) ────────────────────
SPREADS = [
    (8,  'Структура доклада'),
    (10, 'Ускорение диффузии технологий'),
    (12, 'Падение стоимости технологий'),
    (18, '15 ключевых компонентов'),
    (26, 'Традиционное и передовое производство'),
    (30, 'Экосистема технологий'),
    (32, 'Фабрики Будущего'),
    (40, 'Уровни развития и метасистема EIM'),
    (48, 'Трансфер технологий'),
    (50, 'Бенчмаркинг двух компаний'),
    (72, 'Автономные производства'),
    (80, 'Опросный лист диагностики'),
]

# ─── инфографика: (страница файла, номер рисунка, имя файла) ─────────────────
# Номер нужен только для проверки: на полосе может быть подпись со ссылкой
# на чужой рисунок в тексте, поэтому ищем строку «Рисунок N.» целиком.
FIGURES = [
    (11, 1,  'fig-cycle.jpg'),      # система развития цифровых предприятий, 5 шагов
    (13, 2,  'fig-diffusion.jpg'),  # диффузия потребительских технологий за 110 лет
    (14, 3,  'fig-cost.jpg'),       # резкое падение стоимости ключевых технологий
    (20, 7,  'fig-15.jpg'),         # 15 ключевых компонентов производства
    (29, 9,  'fig-compare.jpg'),    # традиционный и передовой подходы
    (33, 12, 'fig-gartner.jpg'),    # цикл зрелости Гартнера 2016
    (35, 14, 'fig-factories.jpg'),  # трёхуровневая схема Фабрик Будущего
    (42, 15, 'fig-flowers.jpg'),    # две ромашки: уровни развития и результат диагностики
    (43, 16, 'fig-eim.jpg'),        # модули и системы метасистемы EIM
    (51, 18, 'fig-transfer.jpg'),   # система трансфера технологий по этапам
    (52, 19, 'fig-bench.jpg'),      # бенчмаркинг двух компаний
]

MOCKUPS = [
    ('g2.png', 'mock-cover.png'),    # книга на белом
    ('g4.png', 'mock-spread.png'),   # разворот 40-41 с ромашками
    ('g5.png', 'mock-charts.png'),   # разворот с диаграммами
    ('g6.png', 'mock-stack.png'),    # стопка: раскрытая книга и обложка
]


def figure(doc, pno, num, name):
    """Кадр рисунка вместе с родной подписью «Рисунок N.».

    Подпись в издании стоит по-разному: у полосных схем сверху над картинкой,
    у врезок внизу полосы над своей картинкой, но иногда картинка занимает верх
    полосы, а подпись висит под ней. Ориентируемся на текст: если ниже подписи
    ещё идёт наборная колонка, значит рисунок выше подписи.
    """
    page = doc[pno - 1]
    hits = page.search_for(f'Рисунок {num}.')
    if not hits:
        print('   !! подпись не найдена:', name, pno, num)
        return
    w, h = page.rect.width, page.rect.height
    cap_top = min(t.y0 for t in hits)
    cap_bot = max(t.y1 for t in hits)
    # у схем ниже подписи тоже полно текста, но это короткие метки внутри
    # картинки; наборную колонку узнаём по длине блока
    below = max([len(b[4]) for b in page.get_text('blocks')
                 if b[1] > cap_bot + 6 and b[3] < h - 40] or [0])
    if below > 300:                       # под подписью продолжается текст
        clip = fitz.Rect(28, 64, w - 28, cap_bot + 10)
    else:
        clip = fitz.Rect(28, cap_top - 8, w - 28, h - 34)
    zoom = FIG_PX / clip.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
    save(Image.open(io.BytesIO(pix.tobytes('png'))), name, FIG_PX)


def cover_photos(doc):
    """Фотографии производства с обложки — единственные крупные растры."""
    seen, n = set(), 0
    for xref, *_ in doc[0].get_images(full=True):
        if xref in seen:
            continue
        seen.add(xref)
        info = doc.extract_image(xref)
        im = Image.open(io.BytesIO(info['image']))
        if im.width < 600:
            continue
        n += 1
        save(im, f'photo-{n}.jpg', 1100, q=84)
    if n != 4:
        print(f'   !! ожидали 4 фотографии, получили {n}')


def logo(doc):
    """Логотип СКОЛКОВО с шапки полосы, прозрачный PNG."""
    page = doc[3]                       # полоса 2, логотип в левом верхнем углу
    clip = fitz.Rect(62, 26, 240, 100)
    zoom = 900 / clip.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=True)
    im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGBA')
    # белый фон полосы делаем прозрачным, знак и подпись остаются
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if r > 246 and g > 246 and b > 246:
                px[x, y] = (r, g, b, 0)
    im = im.crop(im.getbbox())          # поля клипа режем по самому знаку
    save(im, 'logo-skolkovo.png', 900, fmt='PNG')


def main():
    doc = fitz.open(SRC)
    print('обложка:')
    save(render(doc[0], COVER_PX), 'cover.jpg', COVER_PX)

    print('развороты:')
    for folio, _ in SPREADS:
        sp = spread(doc, folio)
        save(sp, f'spread-{folio:02d}.jpg', 2000, q=84)
        save(sp, f'thumb-{folio:02d}.jpg', 260, q=80)

    print('инфографика:')
    for pno, num, name in FIGURES:
        figure(doc, pno, num, name)

    print('фотографии с обложки:')
    cover_photos(doc)

    print('логотип:')
    logo(doc)

    print('мокапы:')
    for src, dst in MOCKUPS:
        s = os.path.join(MOCKUPS_SRC, src)
        if not os.path.exists(s):
            print('   !! нет мокапа', s)
            continue
        # в исходниках вокруг мокапа гуляют пустые поля до трети кадра,
        # из-за них книга на странице выглядит крошечной
        im = Image.open(s).convert('RGBA')
        bb = im.getbbox()
        if bb:
            im = im.crop(bb)
        save(im, dst, 1300, fmt='PNG')


if __name__ == '__main__':
    main()
