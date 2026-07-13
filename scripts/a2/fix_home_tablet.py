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
    круглых обложек (первые 12 + кнопка «Все проекты» → /project).
  - Клиенты: прячем битый rec249777353, показываем десктопный rec226824033
    (он корректно перетекает в 3 колонки на планшете).

«О нас» (rec250571348) в этой полосе рендерится нормально — не трогаем.
Идемпотентен. Откат: git checkout mirror/index-a2.html
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror')
PAGE = os.path.join(ROOT, 'index-a2.html')

# первые 12 кейсов (обложка, ссылка) — как на десктопе; текст запечён в картинку
CASES = [
    ('/images/lib/custom-stavropol-vdnh/cover-main.png', '/portfolio/stavropol-stand-vdnh'),
    ('/images/lib/custom-samara-vdnh/cover-main.png', '/portfolio/samara-stand-vdnh'),
    ('/images/lib/custom-samara-exhibition/cover-main.png', '/portfolio/samara-exhibition'),
    ('/images/lib/as6135-3563-4735-a365-643234376439/icons-112.png', '/eaton_online'),
    ('/images/lib/as3466-3261-4738-b938-303637303133/__-18.png', '/event/samsung'),
    ('/images/lib/as6466-3635-4534-b432-353364376364/__-01.png', '/3d/stavropol'),
    ('/images/lib/as3532-3737-4330-b333-386531636666/__-03.png', '/video/patriot'),
    ('/images/lib/as3731-3666-4163-a661-383336646133/__-13.png', '/event/marieclaire'),
    ('/images/lib/as3234-6262-4231-b031-663033663939/__-16.png', '/event/salaris'),
    ('/images/lib/as3233-3363-4138-b265-353738653739/__-20.png', '/video/gaz'),
    ('/images/lib/as3933-3462-4563-b861-383364333966/__-15.png', '/video/salaris'),
    ('/images/lib/as3062-3363-4134-b333-623232303134/__-22.png', '/event/riviera'),
]

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


def build_block():
    cards = ''.join(
        f'<a class="hm-cases-t__c" href="{href}"><img src="{cov}" alt="Проект Hand Marketing" loading="lazy"></a>'
        for cov, href in CASES
    )
    return (f'\n{CSS}\n<section class="hm-cases-t"><div class="hm-cases-t__grid">{cards}</div>'
            f'<a class="hm-cases-t__more" href="/project">Все проекты</a></section>\n')


def main():
    html = open(PAGE, encoding='utf-8').read()
    if 'hm-home-tablet' in html:
        print('Уже применено (hm-home-tablet), пропуск.')
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
    html = html[:ins] + build_block() + html[ins:]
    open(PAGE, 'w', encoding='utf-8').write(html)
    print('Готово: адаптивная сетка кейсов + своп клиентов (641–980px).')


if __name__ == '__main__':
    sys.exit(main())
