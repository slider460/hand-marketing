#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Внутренние ссылки сразу на канонический адрес со слэшем.

Шапка и подвал (тильдовские t-menu, Zero-блоки, наш hm-chrome) ведут на
/about, /service, /photo… без слэша. Сервер отвечает на такой адрес 301
на /about/, то есть каждая ссылка на каждой из 84 страниц проходит через
редирект. Поисковик доходит, но вес по ссылке теряется, а обход тратится
на лишние запросы.

Правим готовый HTML, а не исходники: ссылки запечены в тильдовских блоках,
в mpages/, mcases/, carousels/ и в десятке генераторов, и любой из них
при следующем прогоне вернул бы старый вид. Поэтому скрипт стоит
пост-скриптом в finalize_page.py и идемпотентен.

Меняется только href="/путь" без расширения, если в mirror/ есть такая
страница (mirror/путь/index.html). Хвост ?query и #hash сохраняется.

    python3 scripts/a2/fix_internal_slashes.py          # правка
    python3 scripts/a2/fix_internal_slashes.py --check  # только подсчёт
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
MIRROR = os.path.join(ROOT, 'mirror')
PAGES = ('index.html', 'index-a2.html')

HREF = re.compile(r'''(href=)(["'])(/[^"'?#\s]*)([?#][^"']*)?\2''')


def existing_pages():
    out = set()
    for dirpath, _dirs, files in os.walk(MIRROR):
        if any(f in files for f in PAGES):
            rel = os.path.relpath(dirpath, MIRROR).replace(os.sep, '/')
            if rel != '.':
                out.add('/' + rel)
    return out


def fix(html, pages):
    n = 0

    def repl(m):
        nonlocal n
        path = m.group(3)
        if path == '/' or path.endswith('/') or '.' in path.rsplit('/', 1)[-1]:
            return m.group(0)
        if path not in pages:
            return m.group(0)
        n += 1
        return f'{m.group(1)}{m.group(2)}{path}/{m.group(4) or ""}{m.group(2)}'

    return HREF.sub(repl, html), n


def main():
    check = '--check' in sys.argv
    pages = existing_pages()
    total = files = 0
    for dirpath, _dirs, names in os.walk(MIRROR):
        for name in names:
            if name not in PAGES:
                continue
            p = os.path.join(dirpath, name)
            s = open(p, encoding='utf-8').read()
            new, n = fix(s, pages)
            if n:
                files += 1
                total += n
                if not check:
                    open(p, 'w', encoding='utf-8').write(new)
    verb = 'найдено' if check else 'исправлено'
    print(f'fix_internal_slashes: {verb} {total} ссылок в {files} файлах')


if __name__ == '__main__':
    main()
