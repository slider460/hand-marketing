#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Разбор длинных тире в текстах страницы: что можно заменить механически,
а что требует перестройки фразы.

    python3 scripts/audit/tire.py exhibition            # разбор
    python3 scripts/audit/tire.py exhibition --apply    # применить безопасные

Работает по видимому тексту из дампа (scripts/audit/pages/<slug>.json), а правки
вносит в источник страницы (генератор или mirror), сверяя вхождение по контексту.

Классы:
  A  «X — это Y»                     → тире убирается вместе с «это»
  B  пояснение до конца предложения  → двоеточие
  C  однородное перечисление / вставка → запятая
  D  подлежащее и сказуемое, название, прямая речь → руками, не трогаем
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PAGES = os.path.join(HERE, 'pages')

# внутри этих сочетаний тире часть названия и не трогается
KEEP = ['Россия — спортивная держава', 'Weekend — ', '— спортивная держава']


def classify(text, pos):
    """pos — индекс тире в text. Возвращает (класс, замена всего фрагмента) или (D, None)."""
    for k in KEEP:
        if k in text[max(0, pos - 60):pos + 60]:
            return 'D', None
    left = text[:pos].rstrip()
    right = text[pos + 1:].lstrip()
    if not left or not right:
        return 'D', None

    # A: «X — это Y»
    if right.startswith('это ') or right.startswith('Это '):
        return 'A', (left + ' ' + right[4:], 'убрано «— это»')

    tail = right.split('. ')[0]
    # B: пояснение занимает остаток предложения и в нём нет своего двоеточия
    if ':' not in left[-80:] and ':' not in tail and len(tail.split()) >= 3:
        # сказуемое в правой части — признак самостоятельного предложения,
        # для него двоеточие звучит тяжело, лучше точка
        return 'B', (left + ': ' + right[0].lower() + right[1:], 'тире → двоеточие')
    # C: короткая вставка
    if len(tail.split()) <= 3:
        return 'C', (left + ', ' + right, 'тире → запятая')
    return 'D', None


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1].strip('/')
    apply_ = '--apply' in sys.argv
    slug = path.replace('/', '-') or 'home'
    d = json.load(open(os.path.join(PAGES, slug + '.json'), encoding='utf-8'))
    src = os.path.join(ROOT, d['source']['file'])
    if not os.path.isfile(src):
        sys.exit(f'нет источника {src}')
    code = open(src, encoding='utf-8').read()

    stats = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'применено': 0, 'нет в источнике': 0}
    report = []
    seen = set()
    for it in d['flow']:
        t = it.get('text')
        if not t or ' — ' not in t or it.get('chrome') or t in seen:
            continue
        seen.add(t)
        new = t
        while ' — ' in new:
            pos = new.index(' — ') + 1
            cls, res = classify(new, pos)
            if cls == 'D' or res is None:
                stats['D'] += 1
                report.append(('D', new[max(0, pos - 55):pos + 55], ''))
                break
            new, why = res
            stats[cls] += 1
            report.append((cls, t[:110], why))
        if new != t:
            if t in code:
                if apply_:
                    code = code.replace(t, new)
                    stats['применено'] += 1
            else:
                stats['нет в источнике'] += 1
                report.append(('!', t[:90], 'фрагмент собран из кусков, править вручную'))

    if apply_:
        open(src, 'w', encoding='utf-8').write(code)

    print(f"\n{path}  источник: {d['source']['file']}")
    print(f"  A (убрано «это»): {stats['A']}   B (двоеточие): {stats['B']}   "
          f"C (запятая): {stats['C']}   D (руками): {stats['D']}")
    if stats['нет в источнике']:
        print(f"  фрагментов, собранных из кусков кода: {stats['нет в источнике']}")
    if apply_:
        print(f"  ПРИМЕНЕНО замен: {stats['применено']}")
    else:
        for cls, frag, why in report[:40]:
            mark = {'A': 'A', 'B': 'B', 'C': 'C', 'D': '·', '!': '!'}[cls]
            print(f"  {mark} {frag}" + (f"   [{why}]" if why else ''))


if __name__ == '__main__':
    main()
