#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Закрывает «висячие» домены в тильдовских библиотеках (mirror/static/**/*.js).

При переезде с Тильды адреса её серверов в библиотеках заменили заглушками:
  blackhole.invalid.<зона>  → получается blackhole.invalid.com, а invalid.com —
                              обычный домен, с 1997 года он у постороннего владельца;
  forms.tn-api-offline.<зона>, *.tn-cdn-offline.com → домены свободны (whois 10.10.2026:
                              No match), их может купить кто угодно.
Сейчас ни один из них не резолвится, поэтому запросы падают и вреда нет. Но
библиотеки форм, Zero-блоков, маски телефона и каталога грузят оттуда <script>,
а форма на запасном пути шлёт туда имя и телефон. Стоит кому-то завести DNS,
и его JavaScript выполнится на наших страницах.

Что делаем, не меняя поведения:
  1. CSS с blackhole.invalid.<зона>/css/ — сразу на локальную копию /static/cdn/css/
     (до сих пор это на лету делал fx() из fix_forms.py, результат тот же);
  2. всё остальное — в зону .invalid (RFC 6761: она не резолвится и не продаётся),
     запросы падают так же, как падали.
Проверки вида indexOf(...) и регулярки остаются как есть: адреса из них на наших
страницах не встречаются.

Идемпотентен, правит файлы на месте:
    python3 scripts/a2/fix_dangling_domains.py            # mirror/
    python3 scripts/a2/fix_dangling_domains.py <корень>   # копия дерева для проверки
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))

# "https://blackhole.invalid."+X+"/css/…  → "/static/cdn/css/…
CSS_RE = re.compile(r'"https://blackhole\.invalid\."\+[A-Za-z_$][\w$]*(?:\(\))?\+"/css/')
# lib-zero-forms: один адрес d на скрипты (d+"/js/") и стили (d+"/css/"); стили
# раньше переносил на локальные fx(), теперь сразу, скрипты остаются в .invalid
ZF_OLD = 'c.href=d+"/css/"+o'
ZF_NEW = 'c.href="/static/cdn/css/"+o'
SUBS = [
    # «blackhole.invalid.» + зона  → хост blackhole.invalid, зона уходит в путь
    (re.compile(r'blackhole\.invalid\.(?=["\']\+)'), 'blackhole.invalid/'),
    # forms./store.tn-api-offline. + зона → хост в .invalid
    (re.compile(r'tn-api-offline\.(?=["\']\+)'), 'tn-api-offline.invalid/'),
    (re.compile(r'tn-cdn-offline\.(?=["\']\+)'), 'tn-cdn-offline.invalid/'),
    # готовые хосты *.tn-cdn-offline.com (и в проверках, и в адресах: в проверках
    # такие строки на наших страницах не встречаются, сравнение не меняется)
    (re.compile(r'tn-cdn-offline\.com'), 'tn-cdn-offline.invalid'),
    # домен превью, к нему потом дописывают "."+зона: заканчиваем путём, а не точкой
    (re.compile(r'"optim\.tn-cdn-offline"'), '"optim.tn-cdn-offline.invalid/t"'),
]
# что после правки ещё может дать регистрируемый хост
LEFT_RE = re.compile(r'blackhole\.invalid\.["\']?\+|tn-(?:api|cdn)-offline\.["\']\+|tn-cdn-offline\.com|invalid\.com')


def main():
    files = sorted(glob.glob(os.path.join(ROOT, 'static', '**', '*.js'), recursive=True))
    changed = 0
    for f in files:
        s = open(f, encoding='utf-8').read()
        if not re.search(r'blackhole\.invalid|tn-api-offline|tn-cdn-offline', s):
            continue
        o = s
        s, n_css = CSS_RE.subn('"/static/cdn/css/', s)
        if ZF_OLD in s:
            s = s.replace(ZF_OLD, ZF_NEW)
            n_css += 1
        n = n_css
        for rx, rep in SUBS:
            s, k = rx.subn(rep, s)
            n += k
        if s != o:
            open(f, 'w', encoding='utf-8').write(s)
            changed += 1
            print(f'  {os.path.relpath(f, ROOT)}: замен {n} (CSS на локальные {n_css})')
        left = LEFT_RE.findall(s)
        if left:
            sys.exit(f'✗ {f}: осталось {left}')
    print(f'файлов изменено: {changed}' + ('' if changed else ' (уже закрыто)'))


if __name__ == '__main__':
    main()
