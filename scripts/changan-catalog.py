#!/usr/bin/env python3
"""Заводит кейс «Презентация Changan CS35» в Tilda-каталоги проектов (идемпотентно).

Страница /event/changan существует с миграции с Тильды, но в каталоги её так и не
добавили: её не было ни на главной, ни на /project, ни в витрине /event — только
прямая ссылка и sitemap.

Каталоги: getproductslist.json (общий), _689558768071 (главная и /project),
_252167513721 (категория Event, из неё собирается витрина /event). Устаревшие
дубли (_950070406371 и прочие «планшетные») выведены из обращения скриптом
scripts/a2/sync_tablet_catalogs.py — в них ничего не пишем.

Позиция — в конец: кейс старый, свежие работы стоят выше. Обложки: круг-постер
дизайнер сделал ещё на Тильде (лежит в библиотеке), квадрат под hover рисует
scripts/gen-changan-covers.py."""
import json

URL = '/event/changan'
UID = 999900557024
SORT = 1006510
CIRCLE = '/images/lib/as3635-3436-4663-b265-633363383261/__-98.png'
SQUARE = '/images/lib/custom-changan/cover-hover.png'
CAT_FILE = 'mirror/api/getproductslist_252167513721.json'
FILES = ['mirror/api/getproductslist.json',
         'mirror/api/getproductslist_689558768071.json',
         CAT_FILE]

PRODUCT = {
    "uid": UID, "title": "⠀", "sku": "", "text": "Event", "mark": "",
    "quantity": "", "portion": 0, "unit": "", "single": "", "price": None,
    "priceold": "", "descr": "",
    "gallery": json.dumps([{"img": CIRCLE}, {"img": SQUARE}]),
    "buttonlink": URL, "buttontarget": "", "json_options": "", "sort": SORT,
    "url": URL, "pack_label": "lwh", "pack_x": 0, "pack_y": 0, "pack_z": 0, "pack_m": 0,
    "partuids": "[252167513721,689558768071]", "externalid": None,
    "editions": [{"uid": UID, "price": None, "priceold": "", "sku": "", "quantity": "",
                  "img": CIRCLE}],
    "characteristics": [],
}

for f in FILES:
    d = json.load(open(f))
    prods = [p for p in d['products'] if p.get('url') != URL]
    removed = len(prods) != len(d['products'])
    prods.append(dict(PRODUCT))
    if isinstance(d.get('total'), int) and not removed:
        d['total'] += 1
    d['products'] = prods
    json.dump(d, open(f, 'w'), ensure_ascii=False)
    print(f'{f}: позиция {len(prods)}, товаров {len(prods)}')
