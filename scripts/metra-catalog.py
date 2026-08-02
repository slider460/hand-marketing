#!/usr/bin/env python3
"""Добавляет кейс «Брендбук Metra Technology Group» в Tilda-каталоги проектов
(идемпотентно): getproductslist.json, _950070406371 (главная), _689558768071
(/project) и _573067849371 (категория Creative & Design, из неё собирается
витрина на /creativedesign).

Позиция в общих каталогах — 7-я карточка: свежая работа идёт первой из кастомных,
остальные сдвигаются на одну. В категории кейс встаёт первым.
Обложки mirror/images/lib/custom-metra/ (круг-постер → бирюзовый квадрат)."""
import json

URL = '/creative/metra'
UID = 999900557022
POS = 6            # 7-я карточка в общих каталогах
CAT_POS = 0        # первый в категории Creative & Design
SORT = 1001903
CAT_FILE = 'mirror/api/getproductslist_573067849371.json'
FILES = ['mirror/api/getproductslist.json',
         'mirror/api/getproductslist_950070406371.json',
         'mirror/api/getproductslist_689558768071.json',
         CAT_FILE]

PRODUCT = {
    "uid": UID, "title": "⠀", "sku": "", "text": "Creative & Design", "mark": "",
    "quantity": "", "portion": 0, "unit": "", "single": "", "price": None,
    "priceold": "", "descr": "",
    "gallery": json.dumps([{"img": "/images/lib/custom-metra/cover-main.png"},
                           {"img": "/images/lib/custom-metra/cover-hover.png"}]),
    "buttonlink": URL, "buttontarget": "", "json_options": "", "sort": SORT,
    "url": URL, "pack_label": "lwh", "pack_x": 0, "pack_y": 0, "pack_z": 0, "pack_m": 0,
    "partuids": "[573067849371,689558768071,950070406371]", "externalid": None,
    "editions": [{"uid": UID, "price": None, "priceold": "", "sku": "", "quantity": "",
                  "img": "/images/lib/custom-metra/cover-main.png"}],
    "characteristics": [],
}

for f in FILES:
    d = json.load(open(f))
    prods = [p for p in d['products'] if p.get('url') != URL]
    removed = len(prods) != len(d['products'])
    pos = CAT_POS if f == CAT_FILE else POS
    prods.insert(min(pos, len(prods)), dict(PRODUCT))
    if isinstance(d.get('total'), int) and not removed:
        d['total'] += 1
    d['products'] = prods
    json.dump(d, open(f, 'w'), ensure_ascii=False)
    print(f'{f}: позиция {[p.get("url") for p in prods].index(URL) + 1}, товаров {len(prods)}')
