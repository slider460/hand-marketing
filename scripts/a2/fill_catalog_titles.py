#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Возвращает названия проектам в каталогах t-store.

Дизайн v2.2 оставил карточки каталога чистыми кругами: title и descr в JSON
заполнены символом-пустышкой. Для поиска это значит, что 56 проектов на главной
и на /project не содержат ни слова текста, а для посетителя — что он не знает,
на что смотрит, пока не наведёт курсор.

Владелец 20.09.2026: делаем как лучше для поиска. Поэтому подставляем
в каталоги название клиента и короткое описание из карусели проектов
(scripts/a2/carousels/all.html) — те же подписи, что уже показывает
мобильная версия под кругами.

    python3 scripts/a2/fill_catalog_titles.py          # заполнить
    python3 scripts/a2/fill_catalog_titles.py --check  # показать, что будет
    python3 scripts/a2/fill_catalog_titles.py --undo   # вернуть пустые подписи

Идемпотентен: повторный прогон ничего не меняет.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
API = os.path.join(ROOT, 'mirror', 'api')
BLANK = '⠀'  # U+2800, им были забиты названия


def pairs():
    car = open(os.path.join(HERE, 'carousels', 'all.html'), encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'<a class="mcase" href="([^"]+)".*?<div class="mcase__t">([^<]*)</div>'
                         r'<div class="mcase__d">([^<]*)</div>', car, re.S):
        out[m.group(1).rstrip('/')] = (m.group(2).strip(), m.group(3).strip())
    return out


def main(mode='apply'):
    P = pairs()
    files = sorted(glob.glob(os.path.join(API, 'getproductslist*.json')))
    total = 0
    for f in files:
        d = json.load(open(f, encoding='utf-8'))
        ps = d.get('products') or []
        changed = 0
        for p in ps:
            url = (p.get('url') or p.get('buttonlink') or '').rstrip('/')
            cur = (p.get('title') or '').strip()
            if mode == 'undo':
                if cur and cur != BLANK and url in P and cur == P[url][0]:
                    p['title'], p['descr'] = BLANK, ''
                    changed += 1
                continue
            if cur and cur != BLANK:
                continue                      # у каталога уже свои подписи, не трогаем
            if url not in P:
                continue
            title, descr = P[url]
            p['title'], p['descr'] = title, descr
            changed += 1
        if changed and mode != 'check':
            json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        if changed:
            total += changed
            print(f'{os.path.basename(f)}: {changed} карточек')
    verb = {'apply': 'подписано', 'check': 'будет подписано', 'undo': 'очищено'}[mode]
    print(f'{verb} карточек: {total}')


if __name__ == '__main__':
    main('check' if '--check' in sys.argv else 'undo' if '--undo' in sys.argv else 'apply')
