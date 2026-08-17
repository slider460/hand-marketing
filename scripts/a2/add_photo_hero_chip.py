#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Photo production в список услуг под заголовком на главной.

Список живёт в трёх вариантах вёрстки, и правятся все три:
  1. десктопный Zero-блок rec226204768 — отдельные text-элементы с абсолютным
     позиционированием;
  2. планшетный блок .hm-hero-t__chips — обычный flex-список;
  3. мобильный .mh-chips внутри .mhome — тоже flex-список.

Про Zero-блок. Позиции считает движок lib-zero по data-field-атрибутам:
  x = центр страницы + left% × ширина_сетки / 100 − ширина_элемента / 2,
где ширина сетки 1200 на базовом брейкпоинте и 960 на следующем (ниже 960
Zero-блок скрыт, там работают варианты 2 и 3). Запечённый CSS для текстовых
элементов этой сетки уже разъехался с движком до нас, но значения в нём
держим синхронными с data-field, чтобы не было скачка до инициализации JS.

Второй ряд (Print, BTL, Digital, 3D Mapping) сдвигается влево, справа встаёт
Photo production: внутренние промежутки ряда сохранены, ряд остаётся по
центру, а его правый край совпадает с правым краем первого ряда.

Идемпотентен. Правит index.html (исходник) и index-a2.html (уезжает в деплой).
Проверка: python3 scripts/a2/add_photo_hero_chip.py --check
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR = os.path.abspath(os.path.join(HERE, '..', '..'), )
MIRROR = os.path.join(MIRROR, 'mirror')
PAGES = [os.path.join(MIRROR, n) for n in ('index.html', 'index-a2.html')]

REC = '226204768'
SRC = '1599144319846'        # Video production: та же ширина 191, тот же ряд-донор
NEW = '1755500000060'
TITLE = 'Photo production'
HREF = '/photo'
COLOR = '#3B729D'

# новые left% второго ряда: [base, 960]. Ниже 960 Zero-блок скрыт, значения
# res-640/480/320 у сдвигаемых плиток не трогаем.
ROW2 = {
    '1599144393830': ('-30', '-34'),   # Print & Production
    '1599144494280': ('-14', '-16'),   # BTL
    '1599144524102': ('-2', '-4'),     # Digital
    '1599144552758': ('11', '11'),     # 3D Mapping
}
# сама новая плитка: (top, left) по брейкпоинтам base и 960
NEW_POS = {'top': ('31', '38'), 'left': ('30', '34')}


def elem_span(html, elem_id):
    m = re.search(r"<div class='t396__elem tn-elem tn-elem__" + REC + elem_id + r"[ ']", html)
    if not m:
        return None
    i, depth, j = m.start(), 0, m.start()
    while j < len(html):
        if html.startswith('<div', j):
            depth += 1
            j += 4
        elif html.startswith('</div>', j):
            depth -= 1
            j += 6
            if depth == 0:
                return i, j
        else:
            j += 1
    return None


def set_field(el, key, val):
    return re.sub(key + r'="[^"]*"', f'{key}="{val}"', el)


def move_row2(html):
    """Сдвигает четыре плитки второго ряда: и data-field, и запечённый CSS."""
    for eid, (base, r960) in ROW2.items():
        span = elem_span(html, eid)
        if not span:
            raise SystemExit(f'✗ не найден элемент {eid}')
        el = html[span[0]:span[1]]
        new = set_field(el, 'data-field-left-value', base)
        new = set_field(new, 'data-field-left-res-960-value', r960)
        html = html[:span[0]] + new + html[span[1]:]
        # CSS: первое позиционное правило — базовое, второе — брейкпоинт 960
        rules = list(re.finditer(
            r'#rec' + REC + r' \.tn-elem\[data-elem-id="' + eid + r'"\]\{[^}]*left:calc\([^}]*\}', html))
        for rule, val in zip(rules[:2], (base, r960)):
            fixed = re.sub(r'(left:calc\(50% - [\d.]+px \+ )-?[\d.]+px\)',
                           lambda m: m.group(1) + val + 'px)', rule.group(0))
            html = html[:rule.start()] + fixed + html[rule.end():]
    return html


def add_chip(html):
    span = elem_span(html, SRC)
    if not span:
        raise SystemExit(f'✗ не найден донор {SRC}')
    el = html[span[0]:span[1]]
    new = el.replace(REC + SRC, REC + NEW).replace(f"'{SRC}'", f"'{NEW}'")
    new = set_field(new, 'data-field-top-value', NEW_POS['top'][0])
    new = set_field(new, 'data-field-top-res-960-value', NEW_POS['top'][1])
    new = set_field(new, 'data-field-left-value', NEW_POS['left'][0])
    new = set_field(new, 'data-field-left-res-960-value', NEW_POS['left'][1])
    new = re.sub(r'<a href="[^"]*"([^>]*)>[^<]*</a>',
                 lambda m: f'<a href="{HREF}"{m.group(1)}>{TITLE}</a>', new)
    html = html[:span[1]] + new + html[span[1]:]

    # CSS-правила донора клонируем следом, правим top/left базового и 960-го
    rules = list(re.finditer(
        r'#rec' + REC + r' \.tn-elem(?:\.[\w-]+)?\[data-elem-id="' + SRC + r'"\][^{]*\{[^}]*\}', html))
    add, n_pos = [], 0
    for rule in rules:
        clone = rule.group(0).replace(SRC, NEW)
        if 'left:calc(' in clone and n_pos < 2:
            clone = re.sub(r'(top:calc\([\d.]+px - [\d.]+px \+ )-?[\d.]+px\)',
                           lambda m: m.group(1) + NEW_POS['top'][n_pos] + 'px)', clone)
            clone = re.sub(r'(left:calc\(50% - [\d.]+px \+ )-?[\d.]+px\)',
                           lambda m: m.group(1) + NEW_POS['left'][n_pos] + 'px)', clone)
            n_pos += 1
        add.append((rule.end(), clone))
    for end, clone in reversed(add):
        html = html[:end] + clone + html[end:]
    return html


def add_flat_chips(html):
    """Планшетный и мобильный списки: обычные ссылки, вставляем после видео."""
    for cls in ('hm-hero-t__chip', 'mh-chip'):
        pat = re.compile(r'<a class="' + cls + r'" href="/videoproduction"[^>]*>[^<]*</a>')
        chip = (f'<a class="{cls}" href="{HREF}" style="--c:{COLOR}">{TITLE}</a>')
        html = pat.sub(lambda m: m.group(0) + chip, html)
    return html


def patch(path):
    html = open(path, encoding='utf-8').read()
    if NEW in html:
        return 'уже было'
    if f'rec{REC}' not in html:
        return 'нет Zero-блока героя, пропуск'
    html = move_row2(html)
    html = add_chip(html)
    html = add_flat_chips(html)
    open(path, 'w', encoding='utf-8').write(html)
    return 'добавлено'


def check(path):
    html = open(path, encoding='utf-8').read()
    if f'rec{REC}' not in html:
        return 'нет Zero-блока'
    if NEW not in html:
        return '✗ плитки нет'
    span = elem_span(html, NEW)
    el = html[span[0]:span[1]]
    left = re.search(r'data-field-left-value="([^"]*)"', el).group(1)
    n_flat = html.count(f'href="{HREF}" style="--c:{COLOR}"')
    return (f'✓ на месте (left={left}, плоских списков: {n_flat})'
            if left == NEW_POS['left'][0] else f'✗ left={left}')


if __name__ == '__main__':
    mode = check if '--check' in sys.argv else patch
    for p in PAGES:
        if os.path.exists(p):
            print(f'{os.path.basename(p)}: {mode(p)}')
