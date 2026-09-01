#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дозаполняет подписи карточек кейсов в мобильных каталогах.

На мобильной вёрстке карточка это круг-постер плюс подпись под ним:
чип категории, клиент и одна строка про проект. У шести карточек подпись
оказалась пустой, и в ленте они читались как дырки: картинка есть,
белый блок под ней пустой. Данные брались с самих страниц кейсов
(title и h1), а не выдумывались.

Скрипт идемпотентный: заполняет только пустые t/d/cat, заполненные
не трогает. Правит и запечённые каталоги mirror/**/index-a2.html,
и шаблоны scripts/a2/**, из которых они собираются.

Запуск: python3 scripts/a2/fix_mcase_captions.py [--check]
С --check ничего не пишет, только показывает оставшиеся пустые подписи.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

# цвета чипов взяты из уже заполненных карточек тех же каталогов
CAT_COLOR = {
    'Video production': '#CF6F19',
    'Creative &amp; Design': '#C12164',
    'Creative': '#C12164',
    'Event': '#C12164',
    'Digital': '#5E9A2E',
    'Exhibition Build': '#673A7E',
    '3D mapping': '#7E3FA0',
    'MICE': '#14171C',
    'Photo Production': '#14171C',
}

# url → (категория, клиент, строка про проект)
CARDS = {
    '/video/eaton': ('Video production', 'Eaton',
                     'Ролик для международной выставки'),
    '/creative/becar/vertical': ('Creative &amp; Design', 'Becar',
                                 'Брошюра Vertical BW Signature Collection'),
    '/mmg': ('Video production', 'MMG Павелецкая Плаза',
             'Рекламный фильм торгового центра'),
    '/bekobod1': ('Video production', 'Технопарк «Бекабад»',
                  'Презентационный ролик технопарка'),
    '/zubovo': ('Video production', 'Технопарк «Зубово»',
                'Презентационный фильм технопарка под Уфой'),
    '/isotec': ('Video production', 'Изотек',
                'Бренд-ролик ISOTEC для Saint-Gobain'),
}


def files():
    out = []
    for pat in ('mirror/**/*.html', 'scripts/a2/**/*.html'):
        out += glob.glob(os.path.join(ROOT, pat), recursive=True)
    return [f for f in out if 'deploytree' not in f]


def patch(text):
    """Заполняет пустые подписи. Возвращает (новый текст, сколько карточек)."""
    n = 0
    for url, (cat, title, descr) in CARDS.items():
        # карточка целиком: от <a class="mcase" href="url"> до </a>
        pat = re.compile(r'(<a class="mcase"[^>]*href="' + re.escape(url) +
                         r'"[^>]*>.*?</a>)', re.S)

        def one(m):
            nonlocal n
            card = m.group(1)
            before = card
            card = re.sub(r'(class="mcase__cat"[^>]*>)(</span>)',
                          r'\1' + cat + r'\2', card)
            card = re.sub(r'(class="mcase__cat" style="--c:)#14171C(">)' +
                          re.escape(cat), r'\g<1>' + CAT_COLOR[cat] + r'\g<2>' + cat,
                          card)
            card = card.replace('<div class="mcase__t"></div>',
                                f'<div class="mcase__t">{title}</div>')
            card = card.replace('<div class="mcase__d"></div>',
                                f'<div class="mcase__d">{descr}</div>')
            if card != before:
                n += 1
            return card

        text = pat.sub(one, text)
    return text, n


def check():
    bad = 0
    for f in files():
        s = open(f, encoding='utf-8', errors='ignore').read()
        for m in re.finditer(r'<a class="mcase"[^>]*href="([^"]+)"[^>]*>.*?</a>',
                             s, re.S):
            card, url = m.group(0), m.group(1)
            miss = [k for k, pat in (
                ('категория', r'class="mcase__cat"[^>]*></span>'),
                ('клиент', r'<div class="mcase__t"></div>'),
                ('описание', r'<div class="mcase__d"></div>'))
                if re.search(pat, card)]
            if miss:
                bad += 1
                print(f'  ✗ {os.path.relpath(f, ROOT)} {url}: нет {", ".join(miss)}')
    print(f'карточек с неполной подписью: {bad}' if bad
          else '✓ у всех карточек подпись на месте')
    return bad


def main():
    if '--check' in sys.argv:
        sys.exit(1 if check() else 0)
    total, touched = 0, 0
    for f in files():
        s = open(f, encoding='utf-8', errors='ignore').read()
        new, n = patch(s)
        if new != s:
            open(f, 'w', encoding='utf-8').write(new)
            touched += 1
            total += n
            print(f'  ✓ {os.path.relpath(f, ROOT)}: {n} карточек')
    print(f'дозаполнено {total} карточек в {touched} файлах' if total
          else 'все подписи уже на месте')
    check()


if __name__ == '__main__':
    main()
