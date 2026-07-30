#!/usr/bin/env python3
"""Приводит каталог кейсов на /digital (storepart 750728959451) к стандартной
механике карточек v2.2: круг-постер по умолчанию → цветной квадрат с
дескриптором при наведении, без подписей под карточкой.

Было: старые широкие баннеры 401x232 с плашкой «Creative» в одном кадре плюс
текстовые подписи «Becar / Посадочная страница ...» под карточкой. Пары
круг+ховер для этих же кейсов уже лежат в общих каталогах (главная, /project),
здесь мы просто переносим их в digital-каталог и гасим подписи.

Идемпотентно: гоняется сколько угодно раз."""
import json

CAT = 'mirror/api/getproductslist_750728959451.json'
LIB = '/images/lib/'

# url -> (круг-постер, квадрат-ховер с дескриптором)
COVERS = {
    '/digital/becar/invest': (
        'as6165-6430-4232-b230-663664343939/__-39.png',
        'as6138-6363-4734-a561-306333643530/__-38.png'),
    # у «Смайла» круг свой, свёрстанный под кейс (smile-assets.py),
    # ховер берём бирюзовый из старой пары — цвет совпадает
    '/digital/becar/smile': (
        'custom-smile/cover.png',
        'as3666-3735-4630-b963-366432643535/__-63.png'),
    '/digital/becar/vertical': (
        'as3462-6263-4765-b137-646564356534/__-66.png',
        'as3063-3531-4566-a238-643138376439/__-67.png'),
    '/becar_stancia': (
        'as3939-3635-4466-b432-623031656566/icons-113.png',
        'as6532-3137-4338-a237-616131646565/icons-116.png'),
    '/bacar_vertical_all': (
        'as3338-3562-4161-a436-306532643230/icons-114.png',
        'as3839-6539-4733-a435-613464326132/icons-117.png'),
    '/eaton_online': (
        'as6135-3563-4735-a365-643234376439/icons-112.png',
        'as6130-3361-4766-b563-336137333839/icons-115.png'),
}

d = json.load(open(CAT))
for p in d['products']:
    pair = COVERS.get(p.get('url'))
    if not pair:
        print('  пропуск (нет пары обложек):', p.get('url'))
        continue
    main, hover = (LIB + x for x in pair)
    p['gallery'] = json.dumps([{'img': main}, {'img': hover}])
    for e in p.get('editions') or []:
        e['img'] = main
    # подписи под карточкой гасим: весь текст живёт на ховер-квадрате
    p['title'] = p['descr'] = p['text'] = ''
    print('  ok', p['url'])

json.dump(d, open(CAT, 'w'), ensure_ascii=False)
print(f'{CAT}: карточек {len(d["products"])}')
