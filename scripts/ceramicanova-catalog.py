#!/usr/bin/env python3
"""Добавляет кейс «Имиджевые ролики для CeramicaNova» в Tilda-каталоги проектов
(идемпотентно): getproductslist.json, _950070406371 (главная), _689558768071 (/project).
Позиция — 7-я карточка (место, где стоял OBO): CeramicaNova встаёт перед OBO,
OBO и becar сдвигаются на одну. Обложки /images/lib/custom-ceramicanova/
(круг-посток → малиновый квадрат на hover)."""
import json

URL = '/portfolio/ceramicanova'
UID = 999900557017
POS = 6            # 7-я карточка (перед OBO)
SORT = 1001800
FILES = ['mirror/api/getproductslist.json',
         'mirror/api/getproductslist_950070406371.json',
         'mirror/api/getproductslist_689558768071.json']

PRODUCT = {
    "uid": UID, "title": "⠀", "sku": "", "text": "Video production", "mark": "",
    "quantity": "", "portion": 0, "unit": "", "single": "", "price": None,
    "priceold": "", "descr": "",
    "gallery": json.dumps([{"img": "/images/lib/custom-ceramicanova/cover-main.png"},
                           {"img": "/images/lib/custom-ceramicanova/cover-hover.png"}]),
    "buttonlink": URL, "buttontarget": "", "json_options": "", "sort": SORT,
    "url": URL, "pack_label": "lwh", "pack_x": 0, "pack_y": 0, "pack_z": 0, "pack_m": 0,
    "partuids": "[950070406371,689558768071]", "externalid": None,
    "editions": [{"uid": UID, "price": None, "priceold": "", "sku": "", "quantity": "",
                  "img": "/images/lib/custom-ceramicanova/cover-main.png"}],
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
