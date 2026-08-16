#!/usr/bin/env python3
"""Заводит кейс «Презентация Changan CS35» ещё и в подкатегорию 3D mapping.

Финал кейса — шоу на трёх проекторах в дилерском центре (обратная проекция
пейзажа + маппинг на кузов и заклеенные плёнкой стёкла), поэтому кейс должен
стоять и в витрине /3dmapping, а не только в /event.

Механика та же, что у /3d/stavropol: карточка лежит сразу в нескольких
сторпартах, в partuids перечислены все. Скрипт идемпотентный.

Витрина /3dmapping — сторпарт 305877663751.
"""
import json

URL = '/event/changan'
PART_3D = 305877663751
FEED_3D = f'mirror/api/getproductslist_{PART_3D}.json'
FEEDS = ['mirror/api/getproductslist.json',
         'mirror/api/getproductslist_689558768071.json',
         'mirror/api/getproductslist_252167513721.json',
         FEED_3D]


def parts(p):
    try:
        return json.loads(p.get('partuids') or '[]')
    except ValueError:
        return []


# карточку берём из общего каталога, чтобы обложки и подписи не разъезжались
src = next(p for p in json.load(open(FEEDS[1]))['products'] if p.get('url') == URL)

for f in FEEDS:
    d = json.load(open(f))
    prods = d['products']
    cur = next((p for p in prods if p.get('url') == URL), None)
    if cur is None:
        cur = dict(src)
        prods.append(cur)
        d['total'] = len(prods)
    ids = sorted(set(parts(cur)) | {PART_3D})
    cur['partuids'] = '[' + ','.join(str(i) for i in ids) + ']'
    d['products'] = prods
    json.dump(d, open(f, 'w'), ensure_ascii=False)
    print(f'{f}: товаров {len(prods)}, partuids {cur["partuids"]}')
