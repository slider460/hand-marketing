#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рамка-плашка при наведении на услугу в хиро главной.

Как было. На каждую услугу в Zero-блоке rec226204768 заведён отдельный
shape-элемент с абсолютными координатами и sbs-анимацией по hover. Координаты
плашек живут своей жизнью, и после add_photo_hero_chip.py они разъехались:
  - у Photo production плашки нет вообще (её никто не рисовал);
  - плашки второго ряда стоят на 132 px правее своих названий (ряд сдвинули
    влево, плашки остались);
  - ниже 1200 px все плашки сидят на 12-16 px выше названий.

Как стало. Девять старых плашек гасим, рамку рисует псевдоэлемент у самой
ссылки с названием. Она облегает текст на любом брейкпоинте и не разъедется,
когда список услуг снова поедет. Вид сохранён: рамка 1 px #b0b0b0, радиус
14 px, плавное появление.

Правило включено от 960 px: ниже Zero-блок скрыт, там работают .hm-hero-t__chips
(планшет) и .mh-chips (мобильный), у них своя подсветка.

Идемпотентен. Правит index.html (исходник) и index-a2.html (уезжает в деплой).
Проверка: python3 scripts/a2/fix_hero_hover_badges.py --check
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
MIRROR = os.path.join(ROOT, 'mirror')
PAGES = [os.path.join(MIRROR, n) for n in ('index.html', 'index-a2.html')]

MARKER = 'hm-hero-hover-badges'
REC = '226204768'

# названия услуг в хиро: id текстового элемента -> подпись (для сообщений)
LABELS = {
    '1751500000020': 'Exhibition Build',
    '1751500000040': 'Content',
    '1599143810215': 'Event',
    '1599144251550': 'Creative & Design',
    '1599144319846': 'Video production',
    '1755500000060': 'Photo production',
    '1599144393830': 'Print & Production',
    '1599144494280': 'BTL',
    '1599144524102': 'Digital',
    '1599144552758': '3D Mapping',
}

# старые shape-плашки: их гасим
OLD_BADGES = [
    '1751500000021',  # Exhibition Build
    '1751500000041',  # Content
    '1602343067387',  # Event
    '1602343207645',  # Creative & Design
    '1602343322196',  # Video production
    '1602343349908',  # Print & Production
    '1602343381397',  # BTL
    '1602343401676',  # Digital
    '1602343417196',  # 3D Mapping
]

PAD_X = 16   # воздух по бокам, из старых плашек (запас был 4-18 px)
PAD_Y = 13   # воздух сверху и снизу: высота плашки 46 при строке 19


def sel(elem_id, tail=''):
    return '#rec%s .tn-elem[data-elem-id="%s"]%s' % (REC, elem_id, tail)


def build_style():
    hide = ',\n'.join(sel(i) for i in OLD_BADGES)
    links = ',\n'.join(sel(i, ' .tn-atom a') for i in LABELS)
    frames = ',\n'.join(sel(i, ' .tn-atom a::after') for i in LABELS)
    hover = ',\n'.join(sel(i, ':hover .tn-atom a::after') for i in LABELS)
    return (
        "<style id='%s'>\n" % MARKER +
        "/* %s: рамка при наведении рисуется у самой ссылки с названием услуги,\n"
        "   старые shape-плашки с абсолютными координатами погашены */\n" % MARKER +
        "%s{display:none!important}\n" % hide +
        "%s{position:relative}\n" % links +
        "%s{content:'';position:absolute;\n"
        "  top:-%dpx;right:-%dpx;bottom:-%dpx;left:-%dpx;\n"
        "  border:1px solid #b0b0b0;border-radius:14px;\n"
        "  opacity:0;transition:opacity .25s ease-in-out;pointer-events:none}\n"
        % (frames, PAD_Y, PAD_X, PAD_Y, PAD_X) +
        "%s{opacity:1}\n" % hover +
        "@media (max-width:959px){\n%s{display:none}\n}\n" % frames +
        "</style>"
    )


def patch(path, check=False):
    name = os.path.relpath(path, ROOT)
    with open(path, encoding='utf-8') as f:
        html = f.read()

    missing = [i for i in LABELS if 'data-elem-id="%s"' % i not in html
               and "data-elem-id='%s'" % i not in html]
    if missing:
        print('✗ %s: не найдены услуги %s' % (name, ', '.join(missing)))
        return False

    has = MARKER in html
    if check:
        print('%s %s: %s' % ('✓' if has else '✗', name,
                             'плашки привязаны к названиям' if has else 'МАРКЕРА НЕТ'))
        return has

    style = build_style()
    if has:
        html = re.sub(r"<style id='%s'>.*?</style>" % MARKER, style, html, flags=re.S)
        action = 'обновлён'
    else:
        if '</head>' not in html:
            print('✗ %s: нет </head>' % name)
            return False
        html = html.replace('</head>', style + '\n</head>', 1)
        action = 'вставлен'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('✓ %s: блок %s (%d услуг, %d старых плашек погашено)'
          % (name, action, len(LABELS), len(OLD_BADGES)))
    return True


def main():
    check = '--check' in sys.argv
    ok = all([patch(p, check) for p in PAGES])
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
