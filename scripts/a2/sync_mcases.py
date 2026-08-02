#!/usr/bin/env python3
"""Врезает свежую карусель кейсов (scripts/a2/carousels/<cat>.html) в мобильную
часть готовой A2-страницы, не пересобирая её целиком.

Мобильный список `.mcase` в index-a2.html — статическая вёрстка, он не читает
каталожные JSON, поэтому после правок в каталоге расходится с десктопной сеткой.
Скрипт идемпотентный: меняет только содержимое блока `.mcases__track`.

Использование: python3 scripts/a2/sync_mcases.py digital [event ...]"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
# страница A2 -> карусель категории
CAT = {'event': 'event', 'creativedesign': 'creative', 'videoproduction': 'video',
       'digital': 'digital', '3dmapping': '3d', 'project': 'all'}
# якорь конца — только `</a></div></div>`: внутри самой карточки тоже есть
# `</div></div>`, на нём нежадный поиск обрывается на первой карточке
BLOCK = re.compile(r'(<div class="mcases" data-mcases><div class="mcases__track">)'
                   r'(?:<a class="mcase".*?</a>)+(</div></div>)', re.S)

for page in sys.argv[1:] or ['digital']:
    car = os.path.join(HERE, 'carousels', CAT[page] + '.html')
    fp = os.path.join(ROOT, 'mirror', page, 'index-a2.html')
    track = re.search(r'<div class="mcases__track">(.*)</div></div>',
                      open(car).read(), re.S).group(1)
    html = open(fp).read()
    was = len(re.findall(r'<a class="mcase"', BLOCK.search(html).group(0)))
    html, n = BLOCK.subn(lambda m: m.group(1) + track + m.group(2), html, count=1)
    assert n == 1, f'{page}: блок карусели не найден'
    open(fp, 'w').write(html)
    now = len(re.findall(r'<a class="mcase"', track))
    print(f'{page}: карточек было {was}, стало {now}')
