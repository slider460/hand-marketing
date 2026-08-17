#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Photo production — десятая плитка в родной Tilda Zero-сетке услуг
(/service, rec228726270).

Сетка 4 колонки: ряд 1 Exhibition/Content/Event/Creative, ряд 2
Video/Print/BTL/Digital, ряд 3 только 3D Mapping. То есть слот справа от
3D Mapping свободен на всех пяти брейкпоинтах, и двигать существующие
плитки не нужно (в отличие от add_exhibition_tile.py, где сетка 4+3
переезжала в 4+4).

Приём: новая плитка = клон 3D Mapping (он даёт вертикаль третьего ряда)
с горизонталью колонки Content (вторая колонка). Клонируются и элементы
разметки с их data-field-атрибутами для движка lib-zero, и весь запечённый
CSS по всем брейкпоинтам — правится только горизонталь, картинка и подпись.
Так плитка гарантированно встаёт в ту же сетку, что и соседи.

Иконка — mirror/images/services/photo-production.svg, изометрическая камера
в стиле остальных иконок (три грани с градиентами, тот же viewBox, что у
content.svg), в синем из палитры страницы /photo.

Идемпотентен. Правит index.html (исходник) и index-a2.html (уезжает в деплой).
Проверка: python3 scripts/a2/add_photo_tile.py --check
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))
PAGES = [os.path.join(MIRROR, 'service', n) for n in ('index.html', 'index-a2.html')]

REC = '228726270'
SRC_ICON = '1599785755041'      # 3D Mapping, иконка: ряд 3, колонка 1
SRC_LABEL = '1599786054597'     # 3D Mapping, подпись
NEW_ICON = '1755500000050'
NEW_LABEL = '1755500000051'

TITLE = 'Photo production'
HREF = '/photo'
SVG = '../images/services/photo-production.svg'

# горизонталь второй колонки, снята с плитки Content по порядку брейкпоинтов
# [base, 960, 640, 480, 320]
ICON_LEFT = ['371', '280', '161', '102', '80']
LABEL_LEFT = ['-13', '-13', '-13', '-12', '-11']
# половина сетки в left:calc(50% - Xpx + ...) — для контроля, что порядок правил не съехал
ICON_HALF = ['600', '480', '320', '240', '160']

Z_ICON, Z_LABEL = '20', '21'


def outer(html, elem_id):
    """Возвращает (start, end) внешнего div элемента Zero-блока."""
    m = re.search(r"<div class='t396__elem tn-elem tn-elem__" + REC + elem_id + r"[ ']", html)
    if not m:
        return None
    i = m.start()
    depth, j = 0, i
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


def clone_element(html, src_id, new_id, lefts, is_label):
    """Клон элемента: новый id, своя горизонталь, своя ссылка и картинка."""
    span = outer(html, src_id)
    if not span:
        raise SystemExit(f'✗ не найден элемент {src_id}')
    el = html[span[0]:span[1]]
    new = el.replace(REC + src_id, REC + new_id).replace(f"'{src_id}'", f"'{new_id}'")

    # горизонталь по брейкпоинтам
    order = ['data-field-left-value', 'data-field-left-res-960-value',
             'data-field-left-res-640-value', 'data-field-left-res-480-value',
             'data-field-left-res-320-value']
    for key, val in zip(order, lefts):
        new = re.sub(key + r'="[^"]*"', f'{key}="{val}"', new)

    # анимация появления: новая плитка выходит последней
    dts = re.findall(r"'dt':'?(\d+)'?", new)
    if dts:
        last = max(int(d) for d in dts)
        new = new.replace(f"'dt':{last}", f"'dt':{last + 500}")

    if is_label:
        new = re.sub(r'<a href="[^"]*"style="color: inherit">[^<]*</a>',
                     f'<a href="{HREF}"style="color: inherit">{TITLE}</a>', new)
    else:
        new = re.sub(r'href="[^"]*"', f'href="{HREF}"', new, count=1)
        new = re.sub(r'data-original="[^"]*"', f'data-original="{SVG}"', new)
        new = re.sub(r"aria-label='[^']*'", f"aria-label='{TITLE}'", new)
    return html[:span[1]] + new + html[span[1]:], span[1]


def clone_css(html, src_id, new_id, lefts, z, atom_fix=None):
    """Клон всех CSS-правил элемента: правило вставляется сразу за исходным,
    поэтому остаётся в своём media-блоке. Горизонталь берётся по порядку
    позиционных правил (base, 1199, 959, 639, 479)."""
    pat = re.compile(r'#rec' + REC + r' \.tn-elem[^{]*"' + src_id + r'"\][^{]*\{[^}]*\}')
    out, pos, n_left, added = [], 0, 0, 0
    for m in pat.finditer(html):
        out.append(html[pos:m.end()])
        rule = m.group(0).replace(src_id, new_id)
        if 'left:calc(' in rule:
            if n_left >= len(lefts):
                raise SystemExit(f'✗ у {src_id} больше позиционных правил, чем брейкпоинтов')
            # в left:calc(50% - Xpx + Ypx) меняем только Y
            rule = re.sub(r'(left:calc\(50% - [\d.]+px \+ )-?[\d.]+px\)',
                          lambda mm: mm.group(1) + lefts[n_left] + 'px)', rule)
            n_left += 1
        rule = re.sub(r'z-index:\d+', f'z-index:{z}', rule)
        if atom_fix and '.tn-atom{' in rule:
            rule = rule.replace(*atom_fix)
        out.append(rule)
        added += 1
        pos = m.end()
    out.append(html[pos:])
    return ''.join(out), added, n_left


def patch(path):
    html = open(path, encoding='utf-8').read()
    if NEW_ICON in html:
        return 'уже было'
    if f'rec{REC}' not in html:
        return 'нет Zero-блока услуг, пропуск'

    html, _ = clone_element(html, SRC_ICON, NEW_ICON, ICON_LEFT, is_label=False)
    html, _ = clone_element(html, SRC_LABEL, NEW_LABEL, LABEL_LEFT, is_label=True)
    # у 3D иконка тильдовская и тянется cover; наш SVG с полями, как content.svg
    html, n1, l1 = clone_css(html, SRC_ICON, NEW_ICON, ICON_LEFT, Z_ICON,
                             atom_fix=('background-size:cover', 'background-size:auto 69%'))
    html, n2, l2 = clone_css(html, SRC_LABEL, NEW_LABEL, LABEL_LEFT, Z_LABEL)
    if l1 != len(ICON_LEFT) or l2 != len(LABEL_LEFT):
        raise SystemExit(f'✗ {path}: позиционных правил {l1}/{l2}, ожидалось по 5')
    open(path, 'w', encoding='utf-8').write(html)
    return f'добавлено (правил CSS: иконка {n1}, подпись {n2})'


def check(path):
    html = open(path, encoding='utf-8').read()
    if f'rec{REC}' not in html:
        return 'нет Zero-блока'
    if NEW_ICON not in html:
        return '✗ плитки нет'
    half = re.findall(r'"' + NEW_ICON + r'"\][^{]*\{[^}]*left:calc\(50% - ([\d.]+)px \+ (-?[\d.]+)px\)',
                      html)
    got = [h for h, _ in half]
    want = ICON_HALF
    return '✓ на месте' if got == want else f'✗ сетка съехала: {got} вместо {want}'


if __name__ == '__main__':
    mode = check if '--check' in sys.argv else patch
    for p in PAGES:
        if os.path.exists(p):
            print(f'service/{os.path.basename(p)}: {mode(p)}')
