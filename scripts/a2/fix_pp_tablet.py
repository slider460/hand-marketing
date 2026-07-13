#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Фикс инфографики «Полиграфия» на /printandproduction для планшета (маркер hm-pp-tablet).

Блок rec248650959 — одиночный десктопный артборд (без screen-версии), свёрстан под
≥1280px. На 641–1279 числа и подписи справа (год, «Рекламные конструкции»,
«Выставочный стенд», крупные суммы) обрезаются краем артборда.

Фикс: в 641–1279 прячем rec248650959 и показываем чистую адаптивную версию тех же
цифр — крупные итоги полиграфии + сетка счётчиков конструкций. Числа/подписи —
дословно из оригинала.  Откат: git checkout mirror/printandproduction/index-a2.html
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror')
PAGE = os.path.join(ROOT, 'printandproduction', 'index-a2.html')

TOTALS = [  # крупные итоги полиграфии
    ('Каталоги', '256 900'),
    ('Брошюры', '985 900'),
    ('Листовки', '5 900 700'),
    ('Нестандартная полиграфия', '3 050 900'),
]
COUNTERS = [  # рекламные конструкции
    ('L Banner', '230'), ('Pop UP', '48'), ('Press Wall', '92'), ('Roll UP', '560'),
    ('Демо-стенд', '390'), ('Лайтбокс', '95'), ('Навигация', '345'), ('Промостойка', '690'),
    ('Выставочный стенд', '89'), ('Сувенирная продукция', '98 000'),
    ('Нестандартные рекламные конструкции', '940'),
    ('Нестандартные конструкции для мероприятий', '1560'),
]

CSS = """<style>/*hm-pp-tablet*/
.hm-pp-t{display:none}
@media (min-width:641px) and (max-width:1279.98px){
  #rec248650959{display:none!important}
  .hm-pp-t{display:block;box-sizing:border-box;padding:20px 24px 40px;background:#fff}
  .hm-pp-t *{box-sizing:border-box}
  .hm-pp-t__h{font-family:'Montserrat',sans-serif;font-weight:800;font-size:clamp(26px,4vw,40px);color:#14171C;margin:0 0 8px}
  .hm-pp-t__sub{font-size:15px;color:#6A7078;margin:0 0 32px;max-width:640px}
  .hm-pp-t__totals{display:grid;grid-template-columns:repeat(4,1fr);gap:20px 16px;margin-bottom:44px}
  .hm-pp-t__big .v{font-family:'Montserrat',sans-serif;font-weight:800;font-size:clamp(22px,3.2vw,32px);color:#e6007e;line-height:1.1}
  .hm-pp-t__big .l{font-size:14px;color:#14171C;margin-top:6px}
  .hm-pp-t__cap{font-family:'Montserrat',sans-serif;font-weight:700;font-size:18px;color:#14171C;margin:0 0 20px}
  .hm-pp-t__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px 16px}
  .hm-pp-t__i .v{font-family:'Montserrat',sans-serif;font-weight:800;font-size:22px;color:#00b0d8;line-height:1.1}
  .hm-pp-t__i .l{font-size:13px;color:#6A7078;margin-top:4px;line-height:1.3}
}
@media (min-width:641px) and (max-width:900px){.hm-pp-t__totals,.hm-pp-t__grid{grid-template-columns:repeat(3,1fr)}}
@media (min-width:641px) and (max-width:679.98px){.hm-pp-t__totals,.hm-pp-t__grid{grid-template-columns:repeat(2,1fr)}}
</style>"""


def build_block():
    totals = ''.join(f'<div class="hm-pp-t__big"><div class="v">{v}</div><div class="l">{l}</div></div>' for l, v in TOTALS)
    counters = ''.join(f'<div class="hm-pp-t__i"><div class="v">{v}</div><div class="l">{l}</div></div>' for l, v in COUNTERS)
    return (f'\n{CSS}\n<section class="hm-pp-t">'
            f'<h2 class="hm-pp-t__h">Полиграфия</h2>'
            f'<p class="hm-pp-t__sub">Мы постарались подсчитать, сколько всего мы произвели полиграфии, и вот что вышло:</p>'
            f'<div class="hm-pp-t__totals">{totals}</div>'
            f'<p class="hm-pp-t__cap">Рекламные конструкции</p>'
            f'<div class="hm-pp-t__grid">{counters}</div></section>\n')


def main():
    html = open(PAGE, encoding='utf-8').read()
    if 'hm-pp-tablet' in html:
        print('Уже применено, пропуск.')
        return
    a = html.find('id="rec248650959"')
    if a < 0:
        print('!! rec248650959 не найден')
        return 1
    ins = html.rfind('<div ', 0, a)
    html = html[:ins] + build_block() + html[ins:]
    open(PAGE, 'w', encoding='utf-8').write(html)
    print('Готово: адаптивная «Полиграфия» (641–1279px).')


if __name__ == '__main__':
    sys.exit(main())
