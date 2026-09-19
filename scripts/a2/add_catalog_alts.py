#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Подписи к картинкам каталогов на тильдовских страницах.

Замер 19.09.2026 (SEO-PLAN.md): 660 картинок на боевых страницах без alt. Основная
масса это карточки каталога t-store: Tilda рисует их JS-ом из JSON и alt не ставит.
Скрипт кладёт на страницу инлайн-скрипт, который после отрисовки проставляет alt
первой картинке карточки (название проекта), пустой alt hover-дублю и aria-label
ссылке. Подписи берём из add_home_alts.case_alts(), они уже сверены по кейсам.

Заодно статическим декоративным картинкам (фоновые паттерны, кляксы) ставим
alt="" и aria-hidden: это не «забытый alt», а осознанный пустой.

    python3 scripts/a2/add_catalog_alts.py

Идемпотентен: старый скрипт вырезается и вставляется заново. Патчит index-a2.html
(боевая версия, см. память index-a2-deploy-trap) и index.html, если он есть.
"""
import html as H
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from add_home_alts import case_alts  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
MARK = 'hm-catalog-alts'

PAGES = ['project', 'creativedesign', 'digital', 'event', '3dmapping', 'btl',
         'printandproduction', 'creative/piloti', 'creative/teoxane', 'about', 'clients']

# декор: фоновые пятна и паттерны шапки, содержания не несут
DECOR = ('pizdapattrtn', 'pngegg', 'noise', 'blur-', 'gradient-')


def js_block(alts):
    return ('<script id="' + MARK + '">(function(){var M=' +
            json.dumps(alts, ensure_ascii=False) + ';'
            'function f(){var n=0;document.querySelectorAll('
            '".t-store a[href],.js-store a[href],.t-feed a[href],.t858 a[href],.t786 a[href]'
            ',.t-store__card a[href]").forEach(function(a){'
            'var h=(a.getAttribute("href")||"").replace(/^https?:\\/\\/[^\\/]+/,"").replace(/\\/$/,"");'
            'var k=M[h];if(!k)return;'
            'if(!a.getAttribute("aria-label"))a.setAttribute("aria-label",k);'
            # Tilda ставит карточкам alt="", поэтому проверяем «пустой или отсутствует»,
            # а не только отсутствие: иначе подпись никогда не появится
            'a.querySelectorAll("img").forEach(function(i,j){'
            'if(!i.getAttribute("alt"))i.setAttribute("alt",j?"":k)});n++});return n}'
            'var t=0,iv=setInterval(function(){t++;if(f()>0&&t>3||t>40)clearInterval(iv)},500);'
            'if(document.readyState!=="loading")f();else document.addEventListener("DOMContentLoaded",f);'
            '})();</script>\n')


def static_pass(s, alts):
    """Карточки мобильных сеток (.mcase) лежат в HTML статически, и это единственное,
    что видит робот, не исполнивший JS. Подпись им ставим прямо в разметке,
    не полагаясь на скрипт: на /project без JS названо было 2 картинки из 66."""
    n = 0

    def fix(m):
        nonlocal n
        href, img = m.group(1), m.group(0)
        k = alts.get(href.rstrip('/'))
        if not k or 'alt=""' not in img:
            return img
        n += 1
        return img.replace('alt=""', f'alt="{H.escape(k)}"', 1)

    s = re.sub(r'<a class="mcase" href="([^"]+)".{0,400}?<img[^>]*>', fix, s, flags=re.S)
    return s, n


def decor_pass(s):
    """Пустой alt декоративным картинкам: у них нет содержания, и это надо сказать явно."""
    n = 0

    def fix(m):
        nonlocal n
        tag = m.group(0)
        if 'alt=' in tag:
            return tag
        src = re.search(r'(?:src|data-original)=["\']([^"\']+)["\']', tag)
        if not src or not any(d in src.group(1) for d in DECOR):
            return tag
        n += 1
        return tag[:-1].rstrip() + ' alt="" aria-hidden="true">'

    return re.sub(r'<img\b[^>]*>', fix, s), n


def main():
    alts = {k.rstrip('/'): v for k, v in case_alts().items()}
    total_js = total_decor = 0
    for slug in PAGES:
        for name in ('index-a2.html', 'index.html'):
            path = os.path.join(ROOT, slug, name)
            if not os.path.isfile(path):
                continue
            s = open(path, encoding='utf-8').read()
            s = re.sub(r'<script id="' + MARK + r'">.*?</script>\n?', '', s, flags=re.S)
            s, ns = static_pass(s, alts)
            s, nd = decor_pass(s)
            i = s.rfind('</body>')
            if i < 0:
                print(f'/{slug}/{name}: нет </body> — пропуск')
                continue
            s = s[:i] + js_block(alts) + s[i:]
            open(path, 'w', encoding='utf-8').write(s)
            total_js += 1
            total_decor += nd
            print(f'/{slug}/{name}: карточек подписано {ns}, декор {nd}, скрипт на месте')
    print(f'Готово: файлов {total_js}, декоративных картинок закрыто {total_decor}')


if __name__ == '__main__':
    main()
