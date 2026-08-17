#!/usr/bin/env python3
"""Добавляет кейс «Предметная съёмка продукции Gyproc» (/photo/saint-gobain)
в Tilda-каталоги проектов, идемпотентно: getproductslist.json и
_689558768071 (главная, /project и планшетный блок главной).

Категорийного фида у фотопродакшна нет и не заводится: витрина на /photo
своя, нативная (как на /videoproduction), поэтому storepart не нужен, и в
partuids стоит только общий каталог.

Позиция в общих каталогах — 7-я карточка: свежая работа идёт первой из
кастомных, остальные сдвигаются на одну.
Обложки: mirror/images/lib/custom-sgphoto/ (синий круг с деталью → синий квадрат)."""
import json

URL = '/photo/saint-gobain'
UID = 999900557031
POS = 6            # 7-я карточка в общих каталогах
SORT = 1001912
FILES = ['mirror/api/getproductslist.json',
         'mirror/api/getproductslist_689558768071.json']

PRODUCT = {
    "uid": UID, "title": "⠀", "sku": "", "text": "Photo Production", "mark": "",
    "quantity": "", "portion": 0, "unit": "", "single": "", "price": None,
    "priceold": "", "descr": "",
    "gallery": json.dumps([{"img": "/images/lib/custom-sgphoto/cover-main.png"},
                           {"img": "/images/lib/custom-sgphoto/cover-hover.png"}]),
    "buttonlink": URL, "buttontarget": "", "json_options": "", "sort": SORT,
    "url": URL, "pack_label": "lwh", "pack_x": 0, "pack_y": 0, "pack_z": 0, "pack_m": 0,
    "partuids": "[689558768071]", "externalid": None,
    "editions": [{"uid": UID, "price": None, "priceold": "", "sku": "", "quantity": "",
                  "img": "/images/lib/custom-sgphoto/cover-main.png"}],
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
    print(f'{f}: позиция {[p.get("url") for p in prods].index(URL) + 1}, '
          f'товаров {len(prods)}')
