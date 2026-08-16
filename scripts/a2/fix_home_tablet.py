#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Фикс главной для планшетного диапазона 641–980px (маркер hm-home-tablet).

На ≤640 работает mhome, на ≥981 — десктопные Tilda-блоки (на 1024 ОК). В полосе
641–980 показываются screenmax-980 «планшетные» версии, и две из них битые:
  1) КЕЙСЫ (rec249926772, screenmax-980) — схлопывается в 0 → кейсы пропадают
     (десктоп rec249749070 скрыт как screenmin-980);
  2) КЛИЕНТЫ (rec249777353, screenmax-980) — логотипы налезают кучей
     (десктоп rec226824033 — нормальная grid-сетка, перетекает чисто).

Фиксы:
  - Кейсы: прячем rec249926772, показываем самодостаточную адаптивную сетку
    круглых обложек (ВСЕ кейсы + кнопка «Все проекты» → /project). Список берётся
    из мобильной карусели `.mcases` на этой же странице — она источник правды,
    её пересобирает gen_cases_carousel.py + apply_cases_carousel.py.
  - Клиенты: прячем битый rec249777353, показываем десктопный rec226824033
    (он корректно перетекает в 3 колонки на планшете).

«О нас» (rec250571348) в этой полосе рендерится нормально — не трогаем.
Идемпотентен. Откат: git checkout mirror/index-a2.html
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror')
PAGE = os.path.join(ROOT, 'index-a2.html')


def read_cases(html):
    """Пары (обложка, ссылка) из мобильной карусели .mcases на этой же странице."""
    i = html.find('data-mcases')
    if i < 0:
        return []
    seg = html[i:html.find('</section>', i)]
    return [(cov, href) for href, cov in
            re.findall(r'<a class="mcase" href="([^"]+)"><div class="mcase__img">'
                       r'<img src="([^"]+)"', seg)]

CSS = """<style>/*hm-home-tablet*/
.hm-cases-t{display:none}
@media (min-width:641px) and (max-width:980px){
  #rec249926772{display:none!important}                 /* битая планшетная лента кейсов */
  #rec249777353{display:none!important}                 /* битая планшетная лента клиентов */
  #rec226824033{display:block!important}                /* десктоп-сетка клиентов (перетекает чисто) */
  .hm-cases-t{display:block;box-sizing:border-box;padding:16px 24px 40px;background:#fff;text-align:center}
  .hm-cases-t *{box-sizing:border-box}
  .hm-cases-t__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px 16px;max-width:1040px;margin:0 auto}
  .hm-cases-t__c{display:block;line-height:0;transition:transform .2s ease}
  .hm-cases-t__c:hover{transform:translateY(-4px)}
  .hm-cases-t__c img{width:100%;height:auto;display:block;border-radius:50%}
  .hm-cases-t__more{display:inline-block;margin-top:36px;padding:14px 34px;border-radius:30px;background:#14171C;color:#fff!important;font-family:'Montserrat',sans-serif;font-weight:700;font-size:15px;text-decoration:none;line-height:1.2}
}
@media (min-width:641px) and (max-width:980px) and (max-width:860px){.hm-cases-t__grid{grid-template-columns:repeat(3,1fr)}}
@media (min-width:641px) and (max-width:679.98px){.hm-cases-t__grid{grid-template-columns:repeat(2,1fr)}}
</style>"""


def build_block(cases):
    cards = ''.join(
        f'<a class="hm-cases-t__c" href="{href}"><img src="{cov}" alt="Проект Hand Marketing" loading="lazy"></a>'
        for cov, href in cases
    )
    return (f'\n{CSS}\n<section class="hm-cases-t"><div class="hm-cases-t__grid">{cards}</div>'
            f'<a class="hm-cases-t__more" href="/project">Все проекты</a></section>\n')


def main():
    html = open(PAGE, encoding='utf-8').read()
    cases = read_cases(html)
    if not cases:
        print('!! карусель .mcases не найдена — нечем наполнить планшетную сетку')
        return 1
    if 'hm-home-tablet' in html:
        # уже вставлено: пересобираем секцию под актуальный список кейсов
        a = html.find('<style>/*hm-home-tablet*/')
        b = html.find('</section>', html.find('<section class="hm-cases-t"', a))
        if a < 0 or b < 0:
            print('!! маркер есть, но секцию разобрать не удалось')
            return 1
        new = build_block(cases)
        old = html[a:b + len('</section>')]
        if old == new.strip():
            print(f'Актуально ({len(cases)} кейсов), правок нет.')
            return
        open(PAGE, 'w', encoding='utf-8').write(html[:a] + new.strip() + html[b + len('</section>'):])
        print(f'Планшетная сетка кейсов обновлена: {len(cases)} карточек.')
        return
    # вставляем перед десктопным блоком кейсов rec249749070 (в его позиции)
    a = html.find('id="rec249749070"')
    if a < 0:
        print('!! якорь rec249749070 не найден')
        return 1
    ins = html.rfind('<div ', 0, a)
    if ins < 0:
        print('!! не найдено начало <div> якоря')
        return 1
    html = html[:ins] + build_block(cases) + html[ins:]
    open(PAGE, 'w', encoding='utf-8').write(html)
    print('Готово: адаптивная сетка кейсов + своп клиентов (641–980px).')


if __name__ == '__main__':
    sys.exit(main())
