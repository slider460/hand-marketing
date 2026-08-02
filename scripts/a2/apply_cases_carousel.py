#!/usr/bin/env python3
"""Врезает свежие фрагменты каруселей кейсов в A2-страницы (идемпотентно).

Фрагменты собирает scripts/a2/gen_cases_carousel.py; здесь они только
подставляются на место готовых блоков, чтобы не гонять build_v1 целиком
(он перетирает кастомные страницы).

Что куда:
  index-a2.html                → all       (карусель на главной)
  <услуга>/index-a2.html       → карусель своей категории
  project/index-a2.html        → сетка mh-grid со всеми карточками

Запуск: python3 scripts/a2/apply_cases_carousel.py [--check]"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))
FRAG = os.path.join(HERE, 'carousels')

# страница → фрагмент
PAGES = {
    'index-a2.html': 'all',
    'creativedesign/index-a2.html': 'creative',
    'event/index-a2.html': 'event',
    'digital/index-a2.html': 'digital',
    '3dmapping/index-a2.html': '3d',
}
GRID_PAGE = 'project/index-a2.html'


def frag(name):
    return open(os.path.join(FRAG, name + '.html'), encoding='utf-8').read().strip()


def swap_carousel(html, new):
    """Меняет блок <div class="mcases" data-mcases> ... </div> перед </section>."""
    i = html.find('<div class="mcases" data-mcases>')
    if i < 0:
        return html, 0
    end = html.find('</section>', i)
    if end < 0:
        return html, 0
    return html[:i] + new + html[end:], 1


def swap_grid(html, new):
    """На /project карточки лежат сеткой mh-grid, без обёртки track."""
    inner = re.sub(r'^<div class="mcases" data-mcases><div class="mcases__track">', '', new)
    inner = re.sub(r'</div></div>$', '</div>', inner) if inner.endswith('</div></div>') else inner
    m = re.search(r'<div class="mh-grid">', html)
    if not m:
        return html, 0
    end = html.find('</section>', m.end())
    if end < 0:
        return html, 0
    return html[:m.end()] + inner + '</div>' + html[end:], 1


def main():
    check = '--check' in sys.argv
    for page, name in PAGES.items():
        p = os.path.join(ROOT, page)
        if not os.path.exists(p):
            print('нет', page)
            continue
        html = open(p, encoding='utf-8').read()
        out, n = swap_carousel(html, frag(name))
        cards = out.count('class="mcase"')
        if not check and out != html:
            open(p, 'w', encoding='utf-8').write(out)
        print(f'{page}: {name}, блоков {n}, карточек {cards}')

    p = os.path.join(ROOT, GRID_PAGE)
    if os.path.exists(p):
        html = open(p, encoding='utf-8').read()
        out, n = swap_grid(html, frag('all'))
        if not check and out != html:
            open(p, 'w', encoding='utf-8').write(out)
        print(f'{GRID_PAGE}: all, блоков {n}, карточек {out.count(chr(34) + "mcase" + chr(34))}')


if __name__ == '__main__':
    main()
