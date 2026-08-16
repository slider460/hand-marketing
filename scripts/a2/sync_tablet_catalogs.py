#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Планшетные каталоги кейсов = десктопные.

На каталожных страницах два store-блока: десктопный (data-screen-min="980px") и
планшетный (data-screen-max="980px"). Исторически они смотрят в РАЗНЫЕ фиды
(`storepart`), и планшетные копии отстали: /creativedesign 14 кейсов против 19,
/event 8 против 9, главная 50 против 52. Новый кейс заводится в общие каталоги и
в категорийный фид десктопа — планшетный дубль про него не узнаёт.

Скрипт переводит планшетный блок на storepart десктопного: один фид на страницу,
дрейфу неоткуда взяться. Правит и index.html (источник для build_v1), и
index-a2.html (то, что уезжает на прод). Идемпотентен, есть --check.

    python3 scripts/a2/sync_tablet_catalogs.py [--check]
"""
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror'))


def blocks(html):
    """[(rec, storepart, 'min980'|'max980'|'все', позиция storepart в тексте)]"""
    out = []
    for m in re.finditer(r"t_store_init\('(\d+)'", html):
        rec = m.group(1)
        start = html.rfind('var options', 0, m.start())
        sp = re.search(r"storepart:'(\d+)'", html[start:m.start()])
        if not sp:
            continue
        pos = start + sp.start(1)
        anchor = html.find('id="rec%s"' % rec)
        scr = re.search(r'data-screen-(min|max)="(\d+)px"', html[anchor:anchor + 400]) if anchor >= 0 else None
        out.append((rec, sp.group(1), (scr.group(1) + scr.group(2)) if scr else 'все', pos))
    return out


def sync(path, check=False):
    html = open(path, encoding='utf-8').read()
    bs = blocks(html)
    desk = [b for b in bs if b[2] == 'min980']
    tab = [b for b in bs if b[2] == 'max980']
    if not desk or not tab:
        return None
    target = desk[0][1]
    changed = []
    # правим с конца, чтобы не сбить позиции
    for rec, part, _, pos in sorted(tab, key=lambda b: -b[3]):
        if part == target:
            continue
        changed.append((rec, part, target))
        if not check:
            html = html[:pos] + target + html[pos + len(part):]
    if changed and not check:
        open(path, 'w', encoding='utf-8').write(html)
    return changed


def main():
    check = '--check' in sys.argv
    total = 0
    for dirpath, _, files in os.walk(ROOT):
        for name in ('index.html', 'index-a2.html'):
            if name not in files:
                continue
            path = os.path.join(dirpath, name)
            res = sync(path, check)
            if res:
                total += len(res)
                rel = os.path.relpath(path, ROOT)
                for rec, old, new in res:
                    print(f'{rel}: rec{rec} storepart {old} -> {new}')
    if not total:
        print('Планшетные каталоги уже смотрят в десктопный фид.')
    elif check:
        print(f'\n[--check] расхождений: {total}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
