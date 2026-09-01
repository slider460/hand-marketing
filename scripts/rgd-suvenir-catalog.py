#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Меняет обложку карточки кейса «Новогодний сувенир ЦМ РЖД» в каталогах.

Карточка кейса стояла со стоковым валенком и ёлкой: к календарю дирекции
и сувенирному набору эта картинка отношения не имеет. Ставим пару обложек
дизайн-системы v2.2 из scripts/gen-rgd-suvenir-covers.py (круг + квадрат).

Правит идемпотентно (повторный запуск ничего не меняет):
  - четыре tilda-каталога mirror/api/getproductslist*.json;
  - запечённые каталоги mirror/**/index-a2.html (главная, /project,
    /creativedesign);
  - шаблоны каруселей и мобильных страниц в scripts/a2/**, из которых
    эти каталоги собираются;
  - заголовок кейса в src/data/cases.json.

Запуск: python3 scripts/rgd-suvenir-catalog.py
"""
import json
import os
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

OLD_MAIN = '/images/lib/as3634-3861-4239-b237-356636663535/__-60.png'
OLD_HOVER = '/images/lib/as3863-6464-4034-a339-656434613230/__-61.png'
NEW_MAIN = '/images/lib/custom-rgd-suvenir/cover-main.png'
NEW_HOVER = '/images/lib/custom-rgd-suvenir/cover-hover.png'

URL = '/creative/rgd/suvenir'
CASES = os.path.join(ROOT, 'src', 'data', 'cases.json')
TITLE = 'Новогодний сувенир ЦМ РЖД: календарь и набор'


def targets():
    """Файлы, где встречается старая пара обложек."""
    out = subprocess.run(
        ['grep', '-rlE', '--binary-files=without-match',
         'as3634-3861-4239-b237-356636663535|as3863-6464-4034-a339-656434613230',
         'mirror', 'scripts/a2'],
        cwd=ROOT, capture_output=True, text=True).stdout.split()
    return [p for p in out if 'deploytree' not in p]


def main():
    for name in (NEW_MAIN, NEW_HOVER):
        if not os.path.exists(os.path.join(ROOT, 'mirror', name.lstrip('/'))):
            sys.exit(f'✗ нет обложки {name}: сперва gen-rgd-suvenir-covers.py')
    # tilda-каталоги правим структурно: gallery в них это JSON-строка внутри
    # JSON, слеши в ней экранированы дважды, и текстовая замена их не ловит
    for rel in ['mirror/api/getproductslist.json',
                'mirror/api/getproductslist_950070406371.json',
                'mirror/api/getproductslist_573067849371.json',
                'mirror/api/getproductslist_689558768071.json']:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding='utf-8'))
        hit = False
        for prod in d.get('products', []):
            if prod.get('url') != URL:
                continue
            prod['gallery'] = json.dumps([{'img': NEW_MAIN}, {'img': NEW_HOVER}])
            for ed in prod.get('editions', []):
                ed['img'] = NEW_MAIN
            hit = True
        if hit:
            json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
            print(f'  ✓ {rel}')

    n = 0
    for rel in targets():
        p = os.path.join(ROOT, rel)
        s = open(p, encoding='utf-8').read()
        # в json пути экранированы слешами: /images → \/images
        new = (s.replace(OLD_MAIN, NEW_MAIN).replace(OLD_HOVER, NEW_HOVER)
                .replace(OLD_MAIN.replace('/', '\\/'), NEW_MAIN.replace('/', '\\/'))
                .replace(OLD_HOVER.replace('/', '\\/'), NEW_HOVER.replace('/', '\\/')))
        if new != s:
            open(p, 'w', encoding='utf-8').write(new)
            n += 1
            print(f'  ✓ {rel}')
    # шаблоны в scripts/a2 ссылаются на картинки через /static/cdn/<каталог>/,
    # сборка переписывает этот префикс в /images/lib/. Правим и там, иначе
    # следующая пересборка каталогов вернёт стоковый валенок
    for rel in ('scripts/a2/mhome.html', 'scripts/a2/cases_carousel.html'):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        new_s = (s.replace('/static/cdn/' + OLD_MAIN.split('/')[3] + '/__-60.png',
                           '/static/cdn/custom-rgd-suvenir/cover-main.png')
                  .replace('/static/cdn/' + OLD_HOVER.split('/')[3] + '/__-61.png',
                           '/static/cdn/custom-rgd-suvenir/cover-hover.png'))
        if new_s != s:
            open(p, 'w', encoding='utf-8').write(new_s)
            n += 1
            print(f'  ✓ {rel}')
    print(f'обложка заменена в {n} файлах' if n else 'обложка уже новая')

    d = json.load(open(CASES, encoding='utf-8'))
    items = d if isinstance(d, list) else d.get('cases', [])
    for c in items:
        if c.get('route') == URL:
            c['title'] = 'Новогодний сувенир ЦМ РЖД'
            c['metaTitle'] = TITLE
            json.dump(d, open(CASES, 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=2)
            print('  ✓ src/data/cases.json: заголовок кейса')
            break


if __name__ == '__main__':
    main()
