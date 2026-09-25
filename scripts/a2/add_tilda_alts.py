#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Подписи к содержательным картинкам тильдовских Zero-блоков.

В Zero-блоках у всех картинок alt='' и src на размытую заглушку 20 px
(/-/resize/20x/), настоящий адрес лежит в data-original и подставляется
тильдовским JS. Большая часть этих картинок декор: цветные круги, узоры,
иконки мессенджеров, и пустой alt для них правильный. Содержательных мало:
фото команды на главной и в /about, скан писем, логотип оператора ЭДО.
Им ставим alt и настоящий src, чтобы робот картинок видел кадр, а не заглушку.

Сопоставление фото с людьми сделано по лицам 25.09.2026 (подписи в самом
Zero-блоке стоят отдельными элементами, порядок в разметке не совпадает
с расположением на экране).

    python3 scripts/a2/add_tilda_alts.py

Идемпотентен. Правит mirror/ напрямую: тильдовские страницы генератора не имеют.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
MIRROR = os.path.join(ROOT, 'mirror')

PAGES = ['index.html', 'index-a2.html',
         'about/index.html', 'about/index-a2.html',
         'contacts/index.html', 'contacts/index-a2.html',
         'clients/index.html', 'clients/index-a2.html']

# имя файла картинки -> alt (имена и должности как на /team/)
ALTS = {
    'mriyaresort_-01-01.png': 'Осотов Алексей, Chief Information Officer',
    'mriyaresort_-01-02.png': 'Муратов Денис, Technical Director',
    'mriyaresort_-01-03.png': 'Агафонова Илона, Senior Account Manager',
    'mriyaresort_-01-04.png': 'Народецкий Александр, Client Service Director / CEO',
    'mriyaresort_-01-05.png': 'Кличановский Сергей, Business Development Director',
    'mriyaresort_-01-06.png': 'Семенов Эдвард, Commercial Director',
    'mriyaresort_-01-07.png': 'Дементьев Святослав, Chief Creative Officer',
    'Free_Flyer_01.png': 'Благодарственные письма клиентов Hand Marketing',
    'sberkorus.png': 'СберКорус, оператор электронного документооборота',
    'noroot.png': 'СберКорус, оператор электронного документооборота',
}

# опечатки, запечённые в тильдовских текстовых элементах
TYPOS = [('Chief information Officet', 'Chief Information Officer')]

IMG = re.compile(r'<img\b[^>]*>', re.S)


def patch_img(tag):
    m = re.search(r"data-original=(['\"])([^'\"]+)\1", tag)
    if not m:
        return tag
    name = m.group(2).rsplit('/', 1)[-1]
    alt = ALTS.get(name)
    if not alt:
        return tag
    real = m.group(2)
    tag = re.sub(r"\salt=(['\"])[^'\"]*\1", f" alt='{alt}'", tag, count=1) \
        if re.search(r"\salt=", tag) else tag.replace('<img', f"<img alt='{alt}'", 1)
    # заглушку 20 px меняем на сам кадр; data-original остаётся, ленивая
    # загрузка Тильды просто подставит тот же адрес
    tag = re.sub(r"\ssrc=(['\"])[^'\"]*/-/resize/20x/[^'\"]*\1", f" src='{real}'", tag, count=1)
    return tag


def main():
    total = 0
    for rel in PAGES:
        p = os.path.join(MIRROR, rel)
        if not os.path.isfile(p):
            continue
        s = open(p, encoding='utf-8').read()
        new = IMG.sub(lambda m: patch_img(m.group(0)), s)
        for a, b in TYPOS:
            new = new.replace(a, b)
        if new != s:
            open(p, 'w', encoding='utf-8').write(new)
            total += 1
            print(f'{rel}: исправлен')
    print(f'add_tilda_alts: файлов {total}')


if __name__ == '__main__':
    main()
