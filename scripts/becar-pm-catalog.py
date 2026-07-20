#!/usr/bin/env python3
"""Добавляет кейс Becar × Private Money в Tilda-каталоги проектов (идемпотентно):
mirror/api/getproductslist.json, _950070406371 (главная), _689558768071 (/project).
Позиция — 7-я карточка каталога (по просьбе пользователя не первая).
Карточка: обложки /images/lib/custom-becar-pm/ (hover-«оборот»), ссылка на кейс."""
import json

URL = '/portfolio/becar-private-money'
UID = 999900445610
POS = 6           # 0-based → седьмая карточка
SORT = 1001700    # между 3d/stavropol (1001500) и video/patriot (1002000)
FILES = ['mirror/api/getproductslist.json',
         'mirror/api/getproductslist_950070406371.json',
         'mirror/api/getproductslist_689558768071.json']

PRODUCT = {
    "uid": UID, "title": "⠀", "sku": "", "text": "", "mark": "", "quantity": "",
    "portion": 0, "unit": "", "single": "", "price": None, "priceold": "", "descr": "",
    "gallery": json.dumps([{"img": "/images/lib/custom-becar-pm/cover-main.png"},
                           {"img": "/images/lib/custom-becar-pm/cover-hover.png"}]),
    "buttonlink": URL, "buttontarget": "", "json_options": "", "sort": SORT,
    "url": URL, "pack_label": "lwh", "pack_x": 0, "pack_y": 0, "pack_z": 0, "pack_m": 0,
    "partuids": "[950070406371,689558768071]", "externalid": None,
    "editions": [{"uid": UID, "price": None, "priceold": "", "sku": "", "quantity": "",
                  "img": "/images/lib/custom-becar-pm/cover-main.png"}],
    "characteristics": [],
}

for f in FILES:
    d = json.load(open(f))
    prods = [p for p in d['products'] if p.get('url') != URL]
    added = len(prods) != len(d['products'])  # True если уже был и мы его вынули
    prods.insert(min(POS, len(prods)), dict(PRODUCT))
    if isinstance(d.get('total'), int) and not added:
        d['total'] += 1
    d['products'] = prods
    json.dump(d, open(f, 'w'), ensure_ascii=False)
    pos = [p.get('url') for p in prods].index(URL) + 1
    print(f'{f}: позиция {pos}, товаров {len(prods)}')
