#!/usr/bin/env python3
"""Ассеты кейса «Брошюра Ramada Encore» (Becar Asset Management).

Источник: печатный PDF ~/Downloads/Брошюра 1000_ramada encore_print_220x220_6 (2).pdf
20 полос, квадрат 220×220 мм. Вылеты в файле не размечены (TrimBox = MediaBox),
поэтому полосы берём целиком, без обрезки.

Что делает:
  1. рендерит полосы;
  2. склеивает попарно в 9 разворотов (2-3, 4-5 … 18-19); обложка (полоса 1)
     и задник (полоса 20) идут отдельно;
  3. перекладывает мокапы печатной брошюры из /images/lib в папку кейса. На одном
     мокапе четыре ракурса двух разворотов — режем на два кадра, чтобы в сетке
     «В печати» не стояло по два экземпляра одного разворота;
  4. вынимает круглую эмблему (гардиент + логотипы Becar и Ramada Encore + листья)
     для героя;
  5. готовит левую половину шторки «ТЗ и дизайн»: текст клиента без вёрстки.

Итог: mirror/images/ramada/. После прогона — scripts/gen-webp.sh mirror/images/ramada
Идемпотентно, просто перезаписывает.
"""
import os
import io
import fitz
from PIL import Image, ImageDraw

SRC = os.path.expanduser('~/Downloads/Брошюра 1000_ramada encore_print_220x220_6 (2).pdf')
LIB = 'mirror/images/lib'
DST = 'mirror/images/ramada'

PAGE_PX = 1250          # ширина одной полосы → разворот 2500 px
COVER_PX = 1400

os.makedirs(DST, exist_ok=True)


def render_pages():
    doc = fitz.open(SRC)
    out = []
    for page in doc:
        zoom = COVER_PX / page.rect.width
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        out.append(Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB'))
    return out


def save(im, name, maxw, q=86):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    print('  ', name, im.size, f'{os.path.getsize(p)//1024} КБ')


def save_png(im, name, maxw):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    im.save(p, 'PNG', optimize=True)
    print('  ', name, im.size, f'{os.path.getsize(p)//1024} КБ')


def spreads(pages):
    """Полосы 2-3, 4-5 … 18-19 — так брошюра раскрывается на столе."""
    for i, left in enumerate(range(2, 19, 2), start=1):
        a, b = pages[left - 1], pages[left]
        w = PAGE_PX
        h = round(a.height * w / a.width)
        a = a.resize((w, h), Image.LANCZOS)
        b = b.resize((w, h), Image.LANCZOS)
        canvas = Image.new('RGB', (w * 2, h), 'white')
        canvas.paste(a, (0, 0))
        canvas.paste(b, (w, 0))
        save(canvas, f'spread-{i:02d}.jpg', w * 2)
        # миниатюры для ленты под листалкой: иначе на 74 px грузились бы все девять
        # разворотов целиком
        save(canvas, f'thumb-{i:02d}.jpg', 220, q=80)


# Левая половина шторки «ТЗ и дизайн»: тот же текст, что стоит на полосах 8-9,
# только без вёрстки.
#
# В старой версии кейса тут лежал файл /images/lib/…/10-26.jpg. Он не про Ramada:
# это общий текст Becar, тот же файл стоит в шторке кейса Vertical, а про кондо-формат
# на Орджоникидзе там нет ни слова. Собираем левую половину сами и берём ровно те
# строки, которые напечатаны на развороте: сверено по рендеру полос в 200 dpi,
# включая двоеточие после «инвестора», дефис в «Management-» и «берет» без ё.
# Смысл блока в том, что текст не менялся ни на символ, менялась только вёрстка,
# поэтому придумывать формулировки для этой половины нельзя.
#
# (текст, кегль, насыщенность, серый ли)
BRIEF_LEFT = [
    ('ЗАРАБАТЫВАЙТЕ ВМЕСТЕ С ЛИДЕРАМИ', 18, 'Regular', True),
    ('ЗАРАБАТЫВАЙ, НЕ ТЕРЯЯ', 46, 'Light', False),
    ('Номер приносит доход без личного участия инвестора: все заботы берет '
     'на себя управляющая компания', 25, 'Regular', False),
    ('100% СОБСТВЕННОСТЬ', 31, 'Regular', False),
    ('ПРОЗРАЧНАЯ ОТЧЕТНОСТЬ', 23, 'SemiBold', False),
    ('по всему циклу работы управляющей компании', 22, 'Regular', True),
    ('ВЫБОР ПРОГРАММЫ', 23, 'SemiBold', False),
    ('доходности', 22, 'Regular', True),
    ('ЛИКВИДНОСТЬ АКТИВА', 23, 'SemiBold', False),
    ('это не просто квадратные метры, а готовый бизнес', 22, 'Regular', True),
]
BRIEF_RIGHT = [
    ('СЕТЬ VERTICAL', 40, 'Light', False),
    ('Becar Asset Management- это подтвержденный опыт работы с кондо-форматами, '
     'компетенция управления объектами со множественностью собственников '
     'и подтвержденные доходности в существующих проектах.', 25, 'Regular', False),
    ('УЖЕ МНОГО ЛЕТ ТЫСЯЧИ ИНВЕСТОРОВ ЗАРАБАТЫВАЮТ С BECAR ASSET MANAGEMENT',
     26, 'SemiBold', False),
]

# 3D-мокапы печатной брошюры со старой версии кейса. Каждый кадр — свой разворот
MOCKUPS = {
    # обложка рядом с развёрнутым разворотом 18-19 (общественные пространства)
    'as3264-6263-4135-a235-383139346634/Perfect_Binding_Broc.png': 'mock-cover.jpg',
    # разворот 8-9: «Зарабатывай, не теряя» и сеть Vertical
    'as3065-6235-4539-a666-613330386237/Perfect_Binding_Broc.jpg': 'mock-earn.jpg',
    # разворот 6-7: лидеры рынка и кондо-отель для инвестора
    'as6165-3137-4938-a265-376532626461/Perfect_Binding_Broc.jpg': 'mock-kondo.jpg',
}
# на этом кадре четыре ракурса двух разворотов: режем на два отдельных кадра
MOCK_CROPS = [
    ('as3237-3830-4034-a362-613263646161/369123.png', 'mock-terms.jpg',
     (0.19, 0.02, 0.70, 0.335)),    # разворот 12-13, «Условия покупки», верхний ракурс
    ('as3237-3830-4034-a362-613263646161/369123.png', 'mock-compare.jpg',
     (0.505, 0.20, 0.97, 0.61)),    # разворот 10-11, «Сравнение доходности», правый
]
# круглая эмблема с логотипами и листьями: фон прозрачный, отдаём PNG как есть
EMBLEM = ('as6530-3435-4836-b938-636136373463/__-47.png', 'emblem.png')

CARD_RATIO = 4 / 3      # сетка «В печати» режет карточки под 4:3


def flatten(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, 'white')
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert('RGB')


def mockups():
    for src, name in MOCKUPS.items():
        save(flatten(Image.open(os.path.join(LIB, src))), name, 1800)


def crop_mockups():
    """По одной брошюре на кадр вместо повторяющихся ракурсов. Кадр добиваем полями
    цвета фона до пропорции карточки, иначе широкий кроп обрежется по бокам."""
    for src, name, (l, t, r, b) in MOCK_CROPS:
        im = flatten(Image.open(os.path.join(LIB, src)))
        w, h = im.size
        cut = im.crop((round(w * l), round(h * t), round(w * r), round(h * b)))
        cw, ch = cut.size
        box = (cw, max(ch, round(cw / CARD_RATIO)))
        canvas = Image.new('RGB', box, im.getpixel((4, 4)))
        canvas.paste(cut, (0, (box[1] - ch) // 2))
        save(canvas, name, 1400)


def emblem():
    src, name = EMBLEM
    im = Image.open(os.path.join(LIB, src)).convert('RGBA')
    save_png(im, name, 900)


# Круг — главный приём брошюры: фотографии на полосах обрезаны дугами. Для сайта
# вынимаем квадратные куски фотографий, круг накладывает CSS. Полоса и квадрат в
# долях ширины полосы (страница квадратная, поэтому доли по x и y совпадают).
CIRCLES = [
    (15, 'circle-relax.jpg', (0.35, 0.00, 0.79, 0.44)),    # номер Comfort, кровать у окна
    (7,  'circle-refresh.jpg', (0.58, 0.45, 1.00, 0.87)),  # рендер комплекса с фасадом
    (17, 'circle-connect.jpg', (0.51, 0.04, 0.93, 0.46)),  # гости в общественной зоне
    (19, 'circle-guests.jpg', (0.45, 0.33, 0.89, 0.77)),   # компания за столом
    (14, 'circle-standard.jpg', (0.15, 0.04, 0.52, 0.41)),  # номер Standard, рабочий стол
    (15, 'circle-comfort.jpg', (0.06, 0.61, 0.35, 0.90)),  # номер Comfort, второй кадр
]


def circles(pages):
    for pg, name, (l, t, r, b) in CIRCLES:
        im = pages[pg - 1]
        w, h = im.size
        save(im.crop((round(w * l), round(h * t), round(w * r), round(h * b))), name, 900)


def brief():
    """Левая половина шторки: текст полос 8-9 как есть, без вёрстки.

    Ровно 2:1 (1680×840), чтобы шторка совпадала с разворотом пиксель в пиксель.
    Набор нарочно скучный: одна гарнитура, чёрный и серый на белом, строки идут
    подряд. Ни одного слова сверх того, что напечатано на развороте: смысл блока
    в том, что справа тот же текст, но собранный в полосу."""
    from PIL import ImageFont

    W, H = 1680, 840
    INK, GRAY, RULE = (34, 34, 34), (128, 128, 128), (219, 219, 219)
    COL_W = 690
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)

    def f(size, weight='Regular'):
        ft = ImageFont.truetype(os.path.join('scripts', 'fonts', 'Montserrat.ttf'), size)
        try:
            ft.set_variation_by_name(weight)
        except Exception:
            pass
        return ft

    def wrap(text, font, width):
        words, lines, cur = text.split(), [], ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=font) <= width:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def column(items, x, y):
        for text, size, weight, gray in items:
            ft = f(size, weight)
            for ln in wrap(text, ft, COL_W):
                d.text((x, y), ln, font=ft, fill=GRAY if gray else INK)
                y += round(size * 1.45)
            y += round(size * 1.1)
        return y

    d.line([(112, 32), (W - 112, 32)], fill=RULE, width=1)
    d.line([(112, H - 32), (W - 112, H - 32)], fill=RULE, width=1)
    column(BRIEF_LEFT, 112, 82)
    column(BRIEF_RIGHT, 880, 82)
    save(im, 'brief.jpg', W, q=92)


if __name__ == '__main__':
    print('полосы:')
    pages = render_pages()
    save(pages[0], 'cover.jpg', COVER_PX)
    save(pages[19], 'back.jpg', COVER_PX)
    print('развороты:')
    spreads(pages)
    print('ТЗ для шторки:')
    brief()
    print('мокапы:')
    mockups()
    crop_mockups()
    print('круглые кадры:')
    circles(pages)
    print('эмблема:')
    emblem()
    print('готово →', DST)
