#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Фирменный стиль выставки „Самара“» (/creative/samara/).

Всё берётся из одного первоисточника — brandbook_v2_2.pdf, 28 полос,
руководство по использованию фирменного стиля Самарской области. PDF лежит
вне репозитория (~/Downloads), готовые файлы коммитятся.

Что делает:
  1. --fonts   Manrope 200-800 из Google Fonts кладёт локально
               (mirror/fonts/files/ + mirror/fonts/manrope-samara.css).
               В manrope-onest.css есть только 500-800, а брендбук показывает
               всю линейку ExtraLight → ExtraBold, она нужна на странице.
  2. --mascots 16 рендеров маскота «Ладушка» — в PDF они лежат отдельными
               картинками с масками прозрачности, вынимаем с альфой,
               обрезаем по непрозрачным пикселям, ужимаем по высоте.
  3. --mockups Носители из гайда: ситиформат в метро, планшет, стены зон,
               экраны приложения, баннеры, фото Музея Алабина.
  4. --vectors Знак-парус, кривая фонового паттерна и обе группы иконок
               (тематические и навигационные) — не растром, а кривыми:
               в PDF это векторные объекты, конвертируем items → SVG path
               и складываем в scripts/a2/samara_vectors.json, откуда их
               берёт генератор. PDF при вёрстке страницы больше не нужен.

Запуск: python3 scripts/samara-brand-assets.py [--fonts] [--mascots]
        [--mockups] [--vectors]. Без флагов делает всё.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
IMG = os.path.join(MIRROR, 'images', 'samara-brand')
FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
VECTORS = os.path.join(ROOT, 'scripts', 'a2', 'samara_vectors.json')
ANCHORS = os.path.join(ROOT, 'scripts', 'a2', 'samara_mascots.json')

PDF = os.path.join(os.path.expanduser('~'), 'Downloads', 'brandbook_v2_2.pdf')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
GF = ('https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800'
      '&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── маскот: (страница PDF, xref картинки, имя, подпись зоны) ───────────────
# «Ладушка» — маскот бренда. Один персонаж, 16 образов: меняются одежда,
# атрибут и поза, лицо и коса остаются. Подписи — из самого гайда (полосы 9-12).
MASCOTS = [
    (1,  333, 'hero',       'Базовый образ'),
    (9,   42, 'business',   'Бизнес'),
    (9,   44, 'city',       'Благоустройство'),
    (10,  60, 'patriotism', 'Патриотизм'),
    (10,  56, 'health',     'Здравоохранение'),
    (10,  54, 'games',      'Игры'),
    (10,  58, 'future',     'Будущее'),
    (11,  78, 'education',  'Обучение'),
    (11,  76, 'youth',      'Молодость'),
    (11,  74, 'art',        'Искусство'),
    (11,  72, 'tourism',    'Туризм'),
    (12,  85, 'hockey',     'Спорт'),
    (12,  95, 'football',   'Спорт'),
    (12,  93, 'basketball', 'Спорт'),
    (12,  97, 'gifts',      'Подарки'),
    (20, 140, 'lecture',    'Лекторий'),
]
MASCOT_H = 1100  # высота готового PNG: на странице рендер не бывает выше 550 CSS-px

# ─── носители: (страница, xref, имя, ширина готового jpg) ───────────────────
MOCKUPS = [
    (15, 110, 'citylight',      1333),  # ситиформаты в переходе метро
    (16, 118, 'tablet',         1332),  # планшет с расписанием событий
    (21, 145, 'wall-volga',     1515),  # стена зоны: волна, экран 1586/1737
    (22, 150, 'screen-level',    504),  # экран «Выбери уровень»
    (22, 153, 'banner-win',     1186),  # баннер «Выиграй билет»
    (22, 156, 'screen-players', 1232),  # экран с игроками «Крыльев Советов»
    (25, 242, 'museum',         1546),  # Музей им. П. В. Алабина
    (25, 243, 'app-schedule',    860),  # экран расписания активностей
    (26, 248, 'app-welcome',     884),  # мобильный экран «Узнай больше»
    (26, 249, 'banner-welcome', 1311),  # баннер «Познакомься с Самарской областью»
]

# ─── векторы: что именно вырезаем со страниц ───────────────────────────────
# Ключ → (страница PDF, прямоугольник-окно в координатах страницы 1920×1080).
# Всё, что рисуется внутри окна, склеивается в один SVG path.
VEC_WINDOWS = {
    # знак логотипа, вертикальная версия (полоса «Логотип»)
    'mark':        (3,  (1325, 465, 1495, 680)),
    # кривая — «основа фоновых паттернов», левая половина полосы
    'sail':        (16, (190, 340, 610, 935)),
    # тематические иконки, полоса «Иконки»: сердце, волны, геймпад,
    # кораблик, самолёт, конфедератка
    'ic-heart':    (17, (1300, 200, 1410, 292)),
    'ic-waves':    (17, (1468, 216, 1562, 288)),
    'ic-gamepad':  (17, (1608, 220, 1716, 290)),
    'ic-boat':     (17, (1306, 342, 1410, 390)),
    'ic-plane':    (17, (1470, 331, 1562, 400)),
    'ic-cap':      (17, (1616, 335, 1710, 396)),
    # навигационные иконки, полоса «Навигационные иконки»
    'nav-wc':      (28, (68, 410, 148, 478)),
    'nav-info':    (28, (70, 526, 148, 602)),
    'nav-down-l':  (28, (212, 420, 270, 466)),
    'nav-up':      (28, (355, 415, 412, 470)),
    'nav-down-r':  (28, (496, 420, 546, 466)),
    'nav-right':   (28, (630, 418, 692, 468)),
    'nav-coffee':  (28, (210, 528, 282, 598)),
    'nav-enter':   (28, (355, 530, 415, 595)),
    'nav-exit':    (28, (492, 530, 552, 595)),
    'nav-hanger':  (28, (626, 532, 694, 592)),
}


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('✗ ' + ' '.join(str(c) for c in cmd) + '\n' + r.stderr[-800:])


def fetch(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA})).read()


def webp(path, q='82'):
    dst = path + '.webp'
    sh(['cwebp', '-quiet', '-q', q, '-m', '6', '-sharp_yuv',
        '-metadata', 'none', path, '-o', dst])
    if os.path.getsize(dst) >= os.path.getsize(path):
        os.remove(dst)


def need_pdf():
    if not os.path.exists(PDF):
        sys.exit('✗ нет исходника: %s\n  Брендбук лежит вне репозитория, положи '
                 'его в ~/Downloads (готовые ассеты уже в git)' % PDF)


def fonts():
    os.makedirs(FILES, exist_ok=True)
    css = fetch(GF).decode('utf-8')
    blocks = re.findall(r'/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    out, n = [], 0
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        wght = re.search(r'font-weight:\s*([\d ]+);', block).group(1).strip().replace(' ', '-')
        name = 'manrope-%s-%s.woff2' % (wght, subset)
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, 'files/%s' % name))
    head = ('/* Manrope 200-800, self-host для /creative/samara/.\n'
            '   Брендбук Самарской области предписывает Manrope во всех ролях,\n'
            '   поэтому нужна вся линейка весов; в manrope-onest.css только 500-800.\n'
            '   Сгенерировано scripts/samara-brand-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'manrope-samara.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print('✓ шрифты: %d @font-face, скачано файлов %d' % (len(out), n))


def _extract(doc, pno, xref):
    """Картинка со страницы вместе с маской прозрачности."""
    import fitz
    smask = 0
    for im in doc[pno - 1].get_images(full=True):
        if im[0] == xref:
            smask = im[1]
            break
    pix = fitz.Pixmap(doc, xref)
    if pix.n > 3 and not pix.alpha:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    if smask:
        pix = fitz.Pixmap(pix, fitz.Pixmap(doc, smask))
    return pix


def _figure_box(im):
    """Рамка самой фигуры, без отдельно стоящего реквизита.

    В рендерах гайда рядом с маскотом попадаются цветок в горшке, скейт или
    брошенная клюшка. Простой getbbox() считает их частью кадра, поэтому у
    разных образов фигура оказывается разного размера и наложение силуэтов
    не совпадает. Берём самую крупную связную область непрозрачных пикселей —
    это и есть персонаж; всё, что его не касается, в рамку не попадает.
    """
    import numpy as np
    from scipy import ndimage
    a = np.array(im)[:, :, 3] > 24
    if not a.any():
        return im.getbbox()
    lab, n = ndimage.label(a)
    if n > 1:
        sizes = ndimage.sum(a, lab, range(1, n + 1))
        a = lab == (int(np.argmax(sizes)) + 1)
    ys, xs = np.where(a)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def _foot_anchor(im):
    """Доля ширины, на которой стоят ступни.

    Позы разные: где-то поднята рука, где-то в кадре клюшка или маски, поэтому
    центр рамки у образов не совпадает и наложение силуэтов расходится. Точка
    опоры берётся по нижней полоске фигуры — по ней силуэты и совмещаются.
    """
    import numpy as np
    a = np.array(im)[:, :, 3] > 24
    band = a[max(0, a.shape[0] - max(4, a.shape[0] // 14)):]
    xs = np.where(band.any(axis=0))[0]
    if not len(xs):
        return 0.5
    return round(float((xs.min() + xs.max()) / 2 / a.shape[1]), 4)


def mascots():
    need_pdf()
    import fitz
    from PIL import Image
    os.makedirs(IMG, exist_ok=True)
    doc = fitz.open(PDF)
    sizes, anchors = {}, {}
    for pno, xref, name, _zone in MASCOTS:
        pix = _extract(doc, pno, xref)
        im = Image.frombytes('RGBA' if pix.alpha else 'RGB',
                             (pix.width, pix.height), pix.samples)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        im = im.crop(_figure_box(im))
        if im.height > MASCOT_H:
            im = im.resize((max(1, round(im.width * MASCOT_H / im.height)), MASCOT_H),
                           Image.LANCZOS)
        dst = os.path.join(IMG, name + '.png')
        im.save(dst, optimize=True)
        webp(dst, q='88')
        sizes[name] = im.size
        anchors[name] = _foot_anchor(im)
    json.dump(anchors, open(ANCHORS, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('✓ маскот: %d образов (точки опоры → %s)'
          % (len(MASCOTS), os.path.relpath(ANCHORS, ROOT)))
    return sizes


def mockups():
    need_pdf()
    import fitz
    from PIL import Image
    os.makedirs(IMG, exist_ok=True)
    doc = fitz.open(PDF)
    sizes = {}
    for pno, xref, name, width in MOCKUPS:
        pix = _extract(doc, pno, xref)
        im = Image.frombytes('RGBA' if pix.alpha else 'RGB',
                             (pix.width, pix.height), pix.samples)
        if im.mode == 'RGBA':
            bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
            bg.alpha_composite(im)
            im = bg
        im = im.convert('RGB')
        if im.width > width:
            im = im.resize((width, max(1, round(im.height * width / im.width))), Image.LANCZOS)
        dst = os.path.join(IMG, name + '.jpg')
        im.save(dst, quality=88, optimize=True)
        webp(dst)
        sizes[name] = im.size
    print('✓ носители: %d' % len(MOCKUPS))
    return sizes


# ─── векторы ────────────────────────────────────────────────────────────────
def _num(v):
    """Короткая запись координаты: 12.0 → 12, 12.3456 → 12.35."""
    return ('%.2f' % v).rstrip('0').rstrip('.')


def _items_to_d(items):
    """items из fitz.Page.get_drawings() → строка d для SVG path."""
    d, cur = [], None
    for it in items:
        op = it[0]
        if op == 'l':
            p1, p2 = it[1], it[2]
            if cur != (p1.x, p1.y):
                d.append('M%s %s' % (_num(p1.x), _num(p1.y)))
            d.append('L%s %s' % (_num(p2.x), _num(p2.y)))
            cur = (p2.x, p2.y)
        elif op == 'c':
            p1, p2, p3, p4 = it[1], it[2], it[3], it[4]
            if cur != (p1.x, p1.y):
                d.append('M%s %s' % (_num(p1.x), _num(p1.y)))
            d.append('C%s %s %s %s %s %s' % (_num(p2.x), _num(p2.y), _num(p3.x),
                                             _num(p3.y), _num(p4.x), _num(p4.y)))
            cur = (p4.x, p4.y)
        elif op == 're':
            r = it[1]
            d.append('M%s %sH%sV%sH%sZ' % (_num(r.x0), _num(r.y0), _num(r.x1),
                                           _num(r.y1), _num(r.x0)))
            cur = None
        elif op == 'qu':
            q = it[1]
            pts = [q.ul, q.ur, q.lr, q.ll]
            d.append('M%s %s' % (_num(pts[0].x), _num(pts[0].y)))
            d += ['L%s %s' % (_num(p.x), _num(p.y)) for p in pts[1:]]
            d.append('Z')
            cur = None
    return ''.join(d)


def vectors():
    need_pdf()
    import fitz
    doc = fitz.open(PDF)
    out = {}
    for key, (pno, win) in VEC_WINDOWS.items():
        rect = fitz.Rect(*win)
        parts = []
        for dr in doc[pno - 1].get_drawings():
            if not rect.contains(dr['rect']):
                continue
            if dr['rect'].width < 1 and dr['rect'].height < 1:
                continue
            d = _items_to_d(dr['items'])
            if not d:
                continue
            parts.append({
                'd': d,
                'fill': bool(dr.get('fill')),
                # штрих иконок в гайде задан в пунктах страницы, сохраняем как есть
                'w': round(dr.get('width') or 0, 2),
                'even_odd': bool(dr.get('even_odd')),
            })
        if not parts:
            sys.exit('✗ пусто в окне %s (стр. %d): проверь координаты' % (key, pno))
        # общий bbox посчитаем по самим путям: окно шире фигуры
        bb = None
        for dr in doc[pno - 1].get_drawings():
            if rect.contains(dr['rect']):
                bb = dr['rect'] if bb is None else (bb | dr['rect'])
        pad = max(p['w'] for p in parts) / 2 + 0.5
        vb = (round(bb.x0 - pad, 2), round(bb.y0 - pad, 2),
              round(bb.width + 2 * pad, 2), round(bb.height + 2 * pad, 2))
        out[key] = {'viewBox': '%s %s %s %s' % tuple(_num(v) for v in vb), 'paths': parts}
    json.dump(out, open(VECTORS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('✓ векторы: %d фигур → %s' % (len(out), os.path.relpath(VECTORS, ROOT)))


if __name__ == '__main__':
    args = set(sys.argv[1:])
    allof = not args
    sizes = {}
    if allof or '--fonts' in args:
        fonts()
    if allof or '--mascots' in args:
        sizes.update(mascots())
    if allof or '--mockups' in args:
        sizes.update(mockups())
    if allof or '--vectors' in args:
        vectors()
    if sizes:
        # размеры нужны генератору для width/height, чтобы вёрстка не прыгала
        print('\nSIZE = ' + json.dumps({k: list(v) for k, v in sorted(sizes.items())},
                                       ensure_ascii=False))
