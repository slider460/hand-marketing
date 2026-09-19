#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Укорачивает слишком длинные <title> кейс-страниц.

Замер 19.09.2026 (SEO-PLAN.md): у 31 страницы title длиннее 70 знаков, в выдаче
он обрезается на середине фразы. Целимся в 55–68 знаков вместе с « | Hand Marketing»:
клиент и суть проекта остаются, хвост с подробностями уходит в description.

Правим и сам генератор, и уже собранный файл в mirror, чтобы не гонять 25 генераторов
и чтобы следующая пересборка страницы не вернула длинный вариант.

    python3 scripts/a2/shorten_titles.py          # применить
    python3 scripts/a2/shorten_titles.py --check  # только показать, что найдено
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
BRAND = ' | Hand Marketing'

# старый title (без бренда) -> новый (без бренда)
TITLES = {
    'Новый год Samsung 2020: панорамные проекции, сетка с автосбросом и digital-ящик Деда Мороза':
        'Новый год Samsung 2020: панорамное шоу в зале',
    'Брошюра ТЦ «Смайл» для Becar: 22 полосы про инвестиции в торговую недвижимость':
        'Брошюра ТЦ «Смайл» для Becar: 22 полосы',
    'Брошюра Vertical BW Signature Collection для Becar: 24 полосы про кондо-отель':
        'Брошюра Vertical BW для Becar: 24 полосы',
    '3D-визуализация маршрута Silk Way Rally: рельеф трассы для презентации гонки':
        '3D-визуализация маршрута Silk Way Rally',
    'Брошюра «Дом с рыцарем» для Becar: 18 полос про апартаменты в доходном доме':
        'Брошюра «Дом с рыцарем» для Becar: 18 полос',
    'Концепция новогоднего календаря Saint-Gobain: иллюстрации из инструментов':
        'Новогодний календарь Saint-Gobain: концепция',
    'Фирменный стиль отдела продаж Becar: логотип SALESDEP, паттерн и гайдлайн':
        'Фирменный стиль SALESDEP для Becar',
    'Презентационный фильм технопарка «Зубово» под Уфой: кейс видеопродакшна':
        'Презентационный фильм технопарка «Зубово»',
    'Брошюра We&I by Vertical Hotel для Becar: 24 полосы про кондо-отель':
        'Брошюра We&I by Vertical для Becar: 24 полосы',
    # в собранном HTML амперсанд экранирован, ищем оба написания
    'Брошюра We&amp;I by Vertical Hotel для Becar: 24 полосы про кондо-отель':
        'Брошюра We&amp;I by Vertical для Becar: 24 полосы',
    'Доклад «Цифровое производство» для СКОЛКОВО: дизайн и вёрстка 86 полос':
        'Доклад «Цифровое производство» для СКОЛКОВО',
    'Брошюра Ramada Encore для Becar: 20 полос про инвестиции в кондо-отель':
        'Брошюра Ramada Encore для Becar: 20 полос',
    'Брендбук Metra Technology Group: архитектура бренда, знак и паттерны':
        'Брендбук Metra Technology Group: пять брендов',
    'Посадочная страница ТРЦ «Смайл» для Becar: кейс разработки лендинга':
        'Лендинг ТРЦ «Смайл» для Becar',
    '3D Mapping шоу в Ставрополе: 27 проекторов на здание Правительства':
        '3D Mapping шоу в Ставрополе: 27 проекторов',
    'Рекламный фильм ТРЦ «Павелецкая Плаза» (MMG): кейс видеопродакшна':
        'Рекламный фильм ТРЦ «Павелецкая Плаза»',
    'BTL-кампания для ТРЦ «Саларис»: акция «Ком подарков» на Christmas':
        'BTL-акция «Ком подарков» в ТРЦ «Саларис»',
    'Бренд-ролик «Изотек» (ISOTEC, Saint-Gobain): кейс видеопродакшна':
        'Бренд-ролик «Изотек» для Saint-Gobain',
    'Серия продуктовых роликов для OBO Bettermann: съёмка в Академии':
        'Продуктовые ролики OBO Bettermann: 10 фильмов',
    'Презентационный ролик технопарка «Бекабад»: кейс видеопродакшна':
        'Презентационный ролик технопарка «Бекабад»',
    'Ролик «История успеха ЦМ РЖД»: фильм к десятилетию дирекции':
        'Фильм к десятилетию ЦМ РЖД: 117 планов',
    'Имиджевый ролик Power Technologies: энергоснабжение ЧМ-2018':
        'Имиджевый ролик Power Technologies: ЧМ-2018',
    'Имиджевые ролики для CeramicaNova: 17 фильмов по коллекциям':
        'Имиджевые ролики CeramicaNova: 17 фильмов',
    '3D-визуализация оборудования Eaton: ЦОД, гипермаркет, завод':
        '3D-визуализация оборудования Eaton',
    'Стенд Becar на Private Money Expo Forum: выставка под ключ':
        'Стенд Becar на Private Money Expo Forum',
    'Журнал Patriki Times: дизайн издания и ежемесячная вёрстка':
        'Журнал Patriki Times: дизайн и вёрстка',
}


def check():
    rows = []
    for f in glob.glob(os.path.join(ROOT, 'mirror', '**', 'index*.html'), recursive=True):
        m = re.search(r'<title>(.*?)</title>', open(f, encoding='utf-8').read(6000), re.S)
        if m and len(m.group(1).strip()) > 68:
            rows.append((len(m.group(1).strip()), f.replace(ROOT + '/mirror', ''), m.group(1).strip()))
    rows.sort(reverse=True)
    for n, p, t in rows:
        known = ' (в словаре)' if t.replace(BRAND, '') in TITLES else ''
        print(f'{n:>4} {p}{known}')
    print('всего длинных:', len(rows))


def apply():
    targets = glob.glob(os.path.join(HERE, 'gen_*.py')) + \
        glob.glob(os.path.join(ROOT, 'mirror', '**', 'index*.html'), recursive=True)
    hits = 0
    for f in targets:
        s = open(f, encoding='utf-8').read()
        orig = s
        for old, new in TITLES.items():
            if old in s:
                s = s.replace(old, new)
        if s != orig:
            open(f, 'w', encoding='utf-8').write(s)
            hits += 1
            print('поправлен', f.replace(ROOT + '/', ''))
    print('файлов изменено:', hits)


if __name__ == '__main__':
    check() if '--check' in sys.argv else apply()
