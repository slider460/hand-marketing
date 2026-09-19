#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Убирает блок «404 Страница не найдена» с /portfolio/samara-exhibition.

Страница тянула бандл React-приложения и монтировала его в #root. Маршрута
/portfolio/samara-exhibition в приложении нет, поэтому оно рисовало собственную
404-страницу прямо внутри готовой статической страницы: посетитель видел её
под контентом, а в разметке появлялся второй H1 «404» (замер 19.09.2026).

Ничего другого React на этой странице не рисует (в #root только блок 404),
поэтому убираем и подключение бандла, и сам контейнер. Скрипты подсветки
(rough-notation, hm-annotate) не трогаем: они оформляют текст.

    python3 scripts/a2/fix_react_404.py

Идемпотентен: повторный прогон ничего не находит.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
PAGES = ['portfolio/samara-exhibition']


def main():
    for slug in PAGES:
        for name in ('index-a2.html', 'index.html'):
            path = os.path.join(ROOT, slug, name)
            if not os.path.isfile(path):
                continue
            s = open(path, encoding='utf-8').read()
            before = len(s)
            s, n_js = re.subn(r'<script[^>]+src="/assets/index-[^"]+\.js"[^>]*>\s*</script>', '', s)
            s, n_css = re.subn(r'<link[^>]+href="/assets/index-[^"]+\.css"[^>]*>', '', s)
            s, n_root = re.subn(r'<div id="root"[^>]*>\s*</div>', '', s)
            if not (n_js or n_css or n_root):
                print(f'/{slug}/{name}: уже чисто')
                continue
            open(path, 'w', encoding='utf-8').write(s)
            print(f'/{slug}/{name}: убрано бандлов {n_js}, стилей {n_css}, контейнеров {n_root}, '
                  f'{(before - len(s)) // 1024} КБ')


if __name__ == '__main__':
    main()
