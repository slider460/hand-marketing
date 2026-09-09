#!/usr/bin/env python3
"""Заводит кейс «Клиентский опыт» Saint-Gobain (/video/saintgobain/cx)
в Tilda-каталоги проектов. Идемпотентно: повторный запуск не плодит дубли.

Каталоги: getproductslist.json (общий), _689558768071 (главная и /project),
_951929931011 (категория Video production, из неё собирается витрина
/videoproduction). Планшетные дубли (_950070406371, _452111646711 и прочие)
выведены из обращения скриптом scripts/a2/sync_tablet_catalogs.py, в них
не пишем.

Позиция: седьмая карточка в общих каталогах (POS) и первая в категории,
кейс свежий. Обложки рисует scripts/gen-sgcx-covers.py."""
import json

URL = '/video/saintgobain/cx'
UID = 999900558100
SORT = 1005000
POS = 6          # седьмая карточка в общих фидах
CAT_POS = 0      # первая в витрине /videoproduction
CIRCLE = '/images/lib/custom-sgcx/cover-main.png'
SQUARE = '/images/lib/custom-sgcx/cover-hover.png'
CAT_FILE = 'mirror/api/getproductslist_951929931011.json'
FILES = ['mirror/api/getproductslist.json',
         'mirror/api/getproductslist_689558768071.json',
         CAT_FILE]

PRODUCT = {
    "uid": UID, "title": "", "sku": "", "text": "", "mark": "",
    "quantity": "", "portion": 0, "unit": "", "single": "", "price": None,
    "priceold": "", "descr": "",
    "gallery": json.dumps([{"img": CIRCLE}, {"img": SQUARE}]),
    "buttonlink": URL, "buttontarget": "", "json_options": "", "sort": SORT,
    "url": URL, "pack_label": "lwh", "pack_x": 0, "pack_y": 0, "pack_z": 0, "pack_m": 0,
    "partuids": "[951929931011,689558768071]", "externalid": None,
    "editions": [{"uid": UID, "price": None, "priceold": "", "sku": "", "quantity": "",
                  "img": CIRCLE}],
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
    print(f'{f}: позиция {pos + 1}, товаров {len(prods)}')
