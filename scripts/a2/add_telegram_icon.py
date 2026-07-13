#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавить значок Telegram в hm-foot__soc на кастомных страницах (exhibition, content,
videoproduction, portfolio/*) — там было только WhatsApp + YouTube. Telegram ставим
ПЕРВЫМ. Идемпотентно (пропуск, если Telegram уже есть). Правит все *.html зеркала.
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror')
TG = 'https://t.me/narodetskii'
TG_SVG = ('<svg viewBox="0 0 24 24"><path d="M9.8 16.6l-.4 4c.5 0 .8-.2 1-.5l2.5-2.3 5 3.7'
          'c.9.5 1.6.2 1.8-.8l3.3-15.3c.3-1.2-.5-1.7-1.3-1.4L1.6 10c-1.2.5-1.2 1.1-.2 1.4l5 1.6'
          'L18 5.7c.5-.3 1-.2.6.2"/></svg>')
TG_A = f'<a href="{TG}" target="_blank" rel="noopener" aria-label="Telegram">{TG_SVG}</a>'


def main():
    n = 0
    for f in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        html = open(f, encoding='utf-8').read()
        if 'hm-foot__soc' not in html:
            continue
        # уже есть Telegram в блоке соцсетей?
        m = re.search(r'<div class="hm-foot__soc">', html)
        if not m:
            continue
        soc_end = html.find('</div>', m.end())
        if 'aria-label="Telegram"' in html[m.start():soc_end]:
            continue
        html = html[:m.end()] + TG_A + html[m.end():]
        open(f, 'w', encoding='utf-8').write(html)
        n += 1
        print('  + ' + os.path.relpath(f, ROOT))
    print(f'Готово: Telegram добавлен на {n} страниц.')


if __name__ == '__main__':
    main()
