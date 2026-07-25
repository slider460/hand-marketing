#!/usr/bin/env python3
"""Добавляет кейс «Серия продуктовых роликов для OBO Bettermann» в Tilda-каталоги
проектов (идемпотентно): mirror/api/getproductslist.json, _950070406371 (главная),
_689558768071 (/project). Позиция — первая карточка (новый флагманский видео-кейс).
Обложки /images/lib/custom-obo-academy/ (круг → прямоугольник на hover)."""
import json

URL = '/portfolio/obo-academy'
UID = 999900556710
POS = 6            # седьмая карточка (по просьбе пользователя, как becar)
SORT = 1001600     # между 3d/stavropol (1001500) и becar (1001700)
FILES = ['mirror/api/getproductslist.json',
         'mirror/api/getproductslist_950070406371.json',
         'mirror/api/getproductslist_689558768071.json']

PRODUCT = {
    "uid": UID, "title": "⠀", "sku": "", "text": "Video production", "mark": "",
    "quantity": "", "portion": 0, "unit": "", "single": "", "price": None,
    "priceold": "", "descr": "",
    "gallery": json.dumps([{"img": "/images/lib/custom-obo-academy/cover-main.png"},
                           {"img": "/images/lib/custom-obo-academy/cover-hover.png"}]),
    "buttonlink": URL, "buttontarget": "", "json_options": "", "sort": SORT,
    "url": URL, "pack_label": "lwh", "pack_x": 0, "pack_y": 0, "pack_z": 0, "pack_m": 0,
    "partuids": "[950070406371,689558768071]", "externalid": None,
    "editions": [{"uid": UID, "price": None, "priceold": "", "sku": "", "quantity": "",
                  "img": "/images/lib/custom-obo-academy/cover-main.png"}],
    "characteristics": [],
}

for f in FILES:
    d = json.load(open(f))
    prods = [p for p in d['products'] if p.get('url') != URL]
    removed = len(prods) != len(d['products'])
    prods.insert(min(POS, len(prods)), dict(PRODUCT))
    if isinstance(d.get('total'), int) and not removed:
        d['total'] += 1
    d['products'] = prods
    json.dump(d, open(f, 'w'), ensure_ascii=False)
    pos = [p.get('url') for p in prods].index(URL) + 1
    print(f'{f}: позиция {pos}, товаров {len(prods)}')
