#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Фикс блока «Наша команда» на главной для планшетного диапазона (маркер hm-team-tablet).

Проблема: десктопный Tilda-артборд #rec226573802 (сетка 4+3 лиц с подписями) свёрстан
под ≥1280px. В промежутке 641–1279px он разваливается:
  - 641–960 (вкл. iPad-портрет 768): движок отдаёт артборду высоту 0 → блок СХЛОПЫВАЕТСЯ,
    команда пропадает целиком;
  - 961–1279 (вкл. iPad-ландшафт 1024): элементы (координаты под ~1200) уходят за экран
    (maxRight до 1344, minLeft до −90) → правые лица ОБРЕЗАЮТСЯ, подписи с именами НАЕЗЖАЮТ
    друг на друга и на фото.
На ≤640 работает своя мобильная лента (.mh-team в #mhome), на ≥1280 — десктопная сетка.

Решение (как с подвалом): в диапазоне 641–1279px прячем #rec226573802 и показываем
самодостаточную адаптивную CSS-grid-версию тех же 7 карточек (то же фото/имя/должность,
круглый портрет, сетка 4→3→2 колонки). Не редизайн — верная responsive-копия десктопа.

Идемпотентен (маркер). Откат: git checkout mirror/index-a2.html
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror')

# страницы с блоком команды: file -> (anchor — вставить грид ПЕРЕД этой записью;
# hide — родные записи команды, прячем их в планшетном диапазоне)
PAGES = {
    'index-a2.html': {
        'anchor': 'rec249757129',
        'hide': ['rec226573802', 'rec249757129', 'rec249908352', 'rec249912163'],
    },
    os.path.join('about', 'index-a2.html'): {
        'anchor': 'rec237659936',
        'hide': ['rec249828659', 'rec249919980', 'rec249919996'],
    },
}

# person: (photo, name, role) — порядок как на десктопе (ряд 1: 4, ряд 2: 3).
# Пути АБСОЛЮТНЫЕ (/images/...) — чтобы фото грузились на любой глубине (/about/ и т.п.)
TEAM = [
    ('/images/lib/as3731-3535-4665-a633-663639313564/mriyaresort_-01-04.png', 'Народецкий Александр', 'Client Service Director / CEO'),
    ('/images/lib/as3366-6336-4430-b166-646662633061/mriyaresort_-01-06.png', 'Семёнов Эдвард', 'Commercial Director'),
    ('/images/lib/as6133-3736-4165-a366-353530633430/mriyaresort_-01-05.png', 'Сергей Кличановский', 'Business Development Director'),
    ('/images/lib/as6463-3334-4266-b835-313433396166/mriyaresort_-01-07.png', 'Дементьев Святослав', 'Chief Creative Officer'),
    ('/images/lib/as3735-6531-4234-b830-363630623332/mriyaresort_-01-01.png', 'Осотов Алексей', 'Chief Information Officer'),
    ('/images/lib/as3636-6463-4437-b436-383331356332/mriyaresort_-01-03.png', 'Агафонова Илона', 'Senior Account Manager'),
    ('/images/lib/as6238-6262-4661-a665-306166343031/mriyaresort_-01-02.png', 'Муратов Денис', 'Technical Director'),
]

CSS = """<style>/*hm-team-tablet*/
.hm-team-t{display:none}
@media (min-width:641px) and (max-width:1279.98px){
  /* прячем ВСЕ родные версии команды (десктоп-сетка screenmin-980, клипается на
     981–1279; + планшетные screenmax-980 слайдеры с пустым полем) в планшетном
     диапазоне; список записей — под конкретную страницу */
  __HIDE__{display:none!important}
  .hm-team-t{display:block;box-sizing:border-box;padding:60px 24px 20px;background:#fff;text-align:center;font-family:'Montserrat','Circe',-apple-system,Arial,sans-serif}
  .hm-team-t *{box-sizing:border-box}
  .hm-team-t h2{font-family:'Montserrat';font-weight:800;font-size:clamp(26px,4vw,40px);color:#14171C;margin:0 0 40px;letter-spacing:.01em}
  .hm-team-t__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:36px 16px;max-width:1040px;margin:0 auto}
  .hm-team-t__c{display:flex;flex-direction:column;align-items:center;text-align:center}
  .hm-team-t__c img{width:140px;height:140px;border-radius:50%;object-fit:cover;background:#eee;border:1px solid rgba(20,23,28,.1);margin-bottom:16px}
  .hm-team-t__n{font-family:'Montserrat';font-weight:700;font-size:16px;color:#14171C;line-height:1.25}
  .hm-team-t__r{font-size:13px;color:#6A7078;margin-top:5px;line-height:1.3;padding:0 4px}
}
@media (min-width:641px) and (max-width:1023.98px){.hm-team-t__grid{grid-template-columns:repeat(3,1fr)}}
@media (min-width:641px) and (max-width:679.98px){.hm-team-t__grid{grid-template-columns:repeat(2,1fr)}}
</style>"""


def build_block(hide_ids):
    css = CSS.replace('__HIDE__', ','.join('#' + r for r in hide_ids))
    cards = ''.join(
        f'<div class="hm-team-t__c"><img src="{ph}" alt="{nm}" loading="lazy">'
        f'<div class="hm-team-t__n">{nm}</div><div class="hm-team-t__r">{rl}</div></div>'
        for ph, nm, rl in TEAM
    )
    return f'\n{css}\n<section class="hm-team-t"><h2>Наша команда</h2><div class="hm-team-t__grid">{cards}</div></section>\n'


def patch(rel, anchor, hide_ids):
    page = os.path.join(ROOT, rel)
    html = open(page, encoding='utf-8').read()
    if 'hm-team-tablet' in html:
        print(f'  = {rel}: уже применено, пропуск')
        return
    a = html.find('id="' + anchor + '"')
    if a < 0:
        print(f'  !! {rel}: якорь {anchor} не найден')
        return
    ins = html.rfind('<div ', 0, a)   # начало тега <div id="anchor" ...>
    if ins < 0:
        print(f'  !! {rel}: не найдено начало <div> якоря')
        return
    html = html[:ins] + build_block(hide_ids) + html[ins:]
    open(page, 'w', encoding='utf-8').write(html)
    print(f'  + {rel}: грид вставлен, скрыты {hide_ids}')


def main():
    for rel, cfg in PAGES.items():
        patch(rel, cfg['anchor'], cfg['hide'])


if __name__ == '__main__':
    sys.exit(main())
