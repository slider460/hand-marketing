#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Убрать дублирование заголовка на мобильных креатив-кейсах: hero-подзаголовок
(<p class="mh-lead">) повторялся первым <h2> контент-блока .cmb. Удаляем этот
<h2> ТОЛЬКО когда его текст (без <br>/пробелов) совпадает с mh-lead — страницы,
где h2 несёт другой заголовок (ramada, rgd/suvenir, tunel), не трогаем.

Идемпотентно. Откат: git checkout mirror/creative/**/index-a2.html
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')


def norm(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)
    for a, b in (('&amp;', '&'), ('&quot;', '"'), ('&laquo;', '«'), ('&raquo;', '»')):
        s = s.replace(a, b)
    return re.sub(r'\s+', '', s).lower()


def main():
    files = sorted(glob.glob(os.path.join(ROOT, 'mirror', 'creative', '**', 'index-a2.html'),
                             recursive=True))
    pat = re.compile(r'(<div class="cmb"[^>]*><div class="cmb__sec">)<h2>(.*?)</h2>', re.S)
    n = 0
    for f in files:
        html = open(f, encoding='utf-8').read()
        m = pat.search(html)
        lead = re.search(r'<p class="mh-lead">(.*?)</p>', html, re.S)
        if not (m and lead):
            continue
        if norm(m.group(2)) != norm(lead.group(1)):
            continue  # h2 несёт другой заголовок — не дубль
        html = html[:m.start()] + m.group(1) + html[m.end():]
        open(f, 'w', encoding='utf-8').write(html)
        n += 1
        print('  - ' + os.path.relpath(f, ROOT))
    print(f'Готово: убран дублирующий <h2> на {n} страницах.')


if __name__ == '__main__':
    main()
