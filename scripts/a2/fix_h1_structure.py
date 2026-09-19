#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Один H1 на страницу вместо двух-трёх.

Наследие Tilda: в одном файле лежат мобильная и десктопная вёрстки, у каждой
свой H1, а кое-где сверху добавлен ещё и sr-only заголовок для поиска. Итог:
18 страниц с двумя H1, главная с тремя (замер 19.09.2026, SEO-PLAN.md).

Оставляем тот H1, у которого текст содержательнее (обычно расширенный вариант
«Услуги рекламного агентства в Москве и по России» против короткого «Услуги»),
остальные понижаем до H2. Вид не меняется: у тильдовских заголовков стили
висят на классах, а общее правило .mhome h1 продублировано для h2.

    python3 scripts/a2/fix_h1_structure.py           # применить
    python3 scripts/a2/fix_h1_structure.py --check   # показать, что нашлось

Идемпотентен: после прогона H1 остаётся один, понижать больше нечего.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

H1 = re.compile(r'<h1(\s[^>]*)?>(.*?)</h1>', re.S)


def plain(t):
    return ' '.join(re.sub(r'<[^>]+>', '', t).split())


def pick(matches):
    """Главный H1 это самый содержательный: короткое «Digital» проигрывает
    «Digital-направление: сайты и посадочные страницы проектов»."""
    best, best_len = 0, -1
    for i, m in enumerate(matches):
        n = len(plain(m.group(2)))
        if n > best_len:
            best, best_len = i, n
    return best


def process(path, apply=True):
    s = open(path, encoding='utf-8').read()
    ms = list(H1.finditer(s))
    if len(ms) < 2:
        return 0, []
    keep = pick(ms)
    texts = [plain(m.group(2))[:60] for m in ms]
    if not apply:
        return len(ms) - 1, texts
    out, last = [], 0
    for i, m in enumerate(ms):
        out.append(s[last:m.start()])
        if i == keep:
            out.append(m.group(0))
        else:
            attrs = m.group(1) or ''
            out.append(f'<h2{attrs}>{m.group(2)}</h2>')
        last = m.end()
    out.append(s[last:])
    open(path, 'w', encoding='utf-8').write(''.join(out))
    return len(ms) - 1, texts


def main(apply=True):
    files = glob.glob(os.path.join(ROOT, 'mirror', '**', 'index*.html'), recursive=True)
    total, pages = 0, 0
    for f in sorted(files):
        n, texts = process(f, apply)
        if n:
            total += n
            pages += 1
            short = f.replace(ROOT + '/mirror', '')
            print(f'{short:44s} понижено {n}: {texts}')
    verb = 'понижено' if apply else 'найдено лишних'
    print(f'\nстраниц {pages}, {verb} заголовков {total}')


if __name__ == '__main__':
    main(apply='--check' not in sys.argv)
