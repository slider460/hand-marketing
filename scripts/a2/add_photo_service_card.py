#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавляет карточку «Photo Production» в мобильный список услуг на /service
(наш собственный блок .mh-scards, не тильдовская вёрстка). Карточка встаёт
сразу после Video Production: съёмку заказывают рядом с видео.

Десктопную Zero-сетку услуг (t396, запечённые координаты по пяти брейкпоинтам)
скрипт НЕ трогает: там 9 плиток в раскладке 4+4+1, десятая требует пересчёта
геометрии и отдельного согласования (см. add_exhibition_tile.py, где такой
пересчёт делался для восьмой).

Идемпотентен. Правит index.html (исходник) и index-a2.html (уезжает в деплой)."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

CARD = ('<a class="mh-scard" href="/photo" style="--c:#3B729D">'
        '<span class="mh-scard__ghost" aria-hidden="true">P</span>'
        '<span class="mh-scard__tag">Услуга</span>'
        '<h3 class="mh-scard__t">Photo Production</h3>'
        '<p class="mh-scard__d">Предметная съёмка товаров и оборудования '
        'для каталогов</p>'
        '<span class="mh-scard__go" aria-hidden="true"></span></a>')

ANCHOR = re.compile(r'(<a class="mh-scard" href="/videoproduction"[\s\S]{0,700}?</a>)')


def patch(path):
    h = open(path, encoding='utf-8').read()
    if 'href="/photo"' in h:
        return 'уже было'
    if not ANCHOR.search(h):
        # в старом index.html мобильного блока .mh-scards нет: на деплое его
        # всё равно перезаписывает index-a2.html, так что это не ошибка
        return 'блока .mh-scards нет, пропуск'
    h = ANCHOR.sub(lambda m: m.group(1) + CARD, h, count=1)
    open(path, 'w', encoding='utf-8').write(h)
    return 'добавлено'


if __name__ == '__main__':
    ok = True
    for name in ('index.html', 'index-a2.html'):
        p = os.path.join(MIRROR, 'service', name)
        if not os.path.exists(p):
            continue
        r = patch(p)
        print(f'service/{name}: {r}')
        ok &= r != 'НЕ НАЙДЕН'
    sys.exit(0 if ok else 1)
