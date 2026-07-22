#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Правильная вёрстка страницы /clients + новые клиенты (маркер hm-clients-grid).

Проблема: список клиентов на /clients — Tilda-артборд rec228499506 с запечёнными
координатами; тексты разной длины налезают друг на друга, добавление клиента
требует ручной допечки координат на 5 брейкпоинтах.

Решение: артборд прячется, перед ним вставляется самодостаточная адаптивная
CSS-сетка «лого + описание» (2 колонки ≥960, 1 колонка ниже). Список клиентов —
в CLIENTS ниже: 25 исходных + 4 новых (Самарская область, Транспорт Будущего,
Bella-Systech, Ceramica Nova). sr-only <h1> страницы не трогаем — видимый
заголовок в сетке сделан div'ом.

Заодно (маркеры-проверки по наличию файла custom-clients/bella-systech.png):
  - главная (index.html + index-a2.html): 2 новые карточки в t594 «С нами
    работают» (rec226824033) — Bella-Systech и Ceramica Nova;
  - мобильная главная (.mh-logos в index-a2.html): те же 2 логотипа.
  (Самарская область и Транспорт Будущего на главной уже были.)

Идемпотентен: повторный запуск заменяет вставленный блок. Правки /clients —
только через этот скрипт. Откат: git checkout mirror/clients mirror/index.html
mirror/index-a2.html.
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror')
MARK = 'hm-clients-grid'

CC = '/images/lib/custom-clients'
LIB = '/images/lib'
CDN = '/static/cdn'

# (лого, имя для alt, описание)
CLIENTS = [
    (f'{CC}/samara-region.png', 'Правительство Самарской области',
     'Правительство Самарской области — высший исполнительный орган государственной власти региона.'),
    (f'{CC}/transport-budushchego.png', 'Транспорт будущего',
     'Российский разработчик и производитель беспилотных авиационных систем.'),
    (f'{LIB}/as6563-3839-4331-a464-333237363138/-2_-18.png', 'Samsung',
     'Южнокорейская компания, крупнейший в мире производитель бытовой техники и электроники.'),
    (f'{CDN}/as6633-3565-4237-b830-323132626430/mriyaresort_-01.svg', 'Mriya Resort & Spa',
     'Отель премиум класса, расположенный на Южном берегу Крыма.'),
    (f'{CDN}/as3738-3233-4764-b634-616662333832/logotype.svg', 'Becar Asset Management',
     'Becar Asset Management — международная группа компаний с более чем 27-летним опытом работы в России, США, Европе, странах СНГ и Ближнего Востока.'),
    (f'{CDN}/as6666-6365-4239-b562-663862326666/eaton_2-01.svg', 'Eaton',
     'Американская машиностроительная корпорация, производитель электротехнического и гидравлического оборудования, автокомплектующих, компонентов для авиационной промышленности.'),
    (f'{LIB}/as3834-3363-4037-b736-626139383339/-2_-21.png', 'Changan',
     'Китайская автомобилестроительная компания. Входит в тройку крупнейших производителей пассажирского транспорта в Китае.'),
    (f'{LIB}/as6263-6664-4461-b331-633965323131/-2_-05.png', 'ТРЦ «Мозаика»',
     'Торгово-развлекательный центр в Москве.'),
    (f'{LIB}/as3234-6363-4863-a134-343861633133/-2_-06.png', 'Messe Düsseldorf',
     'Организатор около 80 различных выставок по всему миру, охватывающих практически все отрасли экономики. Работает с 1963 года.'),
    (f'{LIB}/as6531-6161-4330-b638-376239336235/site-logo.png', 'Альфа-Центр Здоровья',
     'Крупная федеральная сеть клиник по всей России.'),
    (f'{CDN}/as3532-3263-4038-a436-383137663638/logo_1.svg', 'Lingerie',
     'Одно из самых читаемых в России изданий о нижнем белье и бельевом бизнесе.'),
    (f'{LIB}/as3962-6535-4633-b234-313362346432/marie-claire.png', 'Marie Claire',
     'Ежемесячный женский журнал, впервые опубликованный во Франции, но издаваемый и в других странах.'),
    (f'{LIB}/as3935-6539-4939-a166-666436383763/e027f8dd-f4b2-4daa-b.jpg', 'Hearst Shkulev Media',
     'Российская компания, входящая в медиахолдинг Hearst Shkulev Group, издающий журналы Elle, Elle girl, Elle decoration, Maxim, Marie Claire, Psychologies, Departures, «Антенна-Телесемь».'),
    (f'{LIB}/as6133-3838-4366-a335-643465326232/photo.jpg', 'Saint-Gobain',
     'Мировой лидер в создании комфортного пространства для проживания, работы и отдыха человека. Входит в ТОП-100 крупнейших индустриальных корпораций мира.'),
    (f'{LIB}/as6666-3065-4636-b362-323839366138/-2_-19.png', 'МедикСити',
     'Многопрофильная медицинская клиника.'),
    (f'{LIB}/as3466-3165-4263-b431-326163656630/unnamed_1.png', 'ТРЦ «Ривьера»',
     'Торгово-развлекательный центр в Москве.'),
    (f'{LIB}/as3131-6165-4730-b133-623636646536/gb_2f0921c524f0f7485.jpg', 'ТРЦ «Саларис»',
     'Торгово-развлекательный центр в Москве.'),
    (f'{LIB}/as6338-3930-4238-a461-356638373131/logo.png', 'ВСК',
     'Одна из системообразующих российских страховых компаний.'),
    (f'{LIB}/as3539-3962-4366-b030-633538343864/photo.png', 'IXcellerate',
     'IXcellerate — ведущий оператор коммерческих центров обработки данных, входящий в топ-3 крупнейших игроков России.'),
    (f'{LIB}/as3464-6632-4035-a335-316336663466/default_1.jpg', 'ЛОР клиника №1',
     'Медицинский центр в Москве.'),
    (f'{LIB}/as6462-3337-4432-a563-653630323466/Logo_PT_2017.jpg', 'Power Technologies',
     'Поставщик услуг по организации и эксплуатации систем временного энергоснабжения.'),
    (f'{LIB}/as3334-6333-4662-a133-663762666634/logo_short.png', 'Академия Научной Красоты',
     'Поставщик профессиональной косметики и косметологического оборудования.'),
    (f'{LIB}/as3335-6162-4865-a161-303266373539/VVC-logo-18_50x150.png', 'VIVAX',
     'Российская компания, разрабатывающая инновационные пептидные технологии для долгой и здоровой жизни.'),
    (f'{LIB}/as3834-3935-4464-b932-633864386437/__7.png', 'Teoxane',
     'Профессиональная швейцарская лаборатория космецевтики.'),
    (f'{LIB}/as3539-3938-4561-b764-616137636331/SKOLKOVO_Logo_en.jpg', 'СКОЛКОВО',
     'Московская школа управления СКОЛКОВО.'),
    (f'{LIB}/as3438-3231-4534-a438-333965613166/__8.png', 'Silk Way Rally',
     'Международный ралли-марафон, проводящийся с 2009 года на территории России, а также — в отдельные годы — государств Центральной Азии и Китая.'),
    (f'{LIB}/as3937-6164-4338-a236-363664623862/1603629-01.png', 'РЖД',
     'Российская государственная вертикально интегрированная компания, владелец инфраструктуры общего пользования и крупнейший перевозчик российской сети железных дорог.'),
    (f'{CDN}/as3335-3366-4863-a461-623130393638/g-01.svg', 'Mall Management Group',
     'Mall Management Group (MMG) занимается девелопментом и созданием качественных объектов коммерческой недвижимости, а также сопровождением полного цикла жизни проектов.'),
    (f'{CC}/bella-systech.png', 'Bella-Systech',
     'Поставщик лазерного и косметологического оборудования для клиник эстетической медицины.'),
    (f'{CC}/ceramicanova.png', 'Ceramica Nova',
     'Бренд керамической сантехники: итальянский дизайн в сочетании с немецкими технологиями производства.'),
]

CSS = f'''<style>/*{MARK}*/
#rec228499506{{display:none!important}}
.hm-clients{{background:#fff;box-sizing:border-box;padding:80px 20px 90px;font-family:'Montserrat',Arial,sans-serif}}
.hm-clients *{{box-sizing:border-box}}
.hm-clients__in{{max-width:1200px;margin:0 auto}}
.hm-clients__t{{font-weight:700;font-size:52px;line-height:1.1;color:#000;margin:0 0 64px}}
.hm-clients__grid{{display:grid;grid-template-columns:1fr 1fr;gap:52px 72px}}
.hm-clients__i{{display:grid;grid-template-columns:170px 1fr;gap:30px;align-items:center}}
.hm-clients__logo{{display:flex;align-items:center;justify-content:center;min-height:70px}}
.hm-clients__logo img{{max-width:160px;max-height:95px;width:auto;height:auto;display:block}}
.hm-clients__d{{font-weight:300;font-size:15px;line-height:1.55;color:#000;margin:0}}
@media screen and (max-width:1199px){{.hm-clients__grid{{gap:44px 40px}}}}
@media screen and (max-width:959px){{.hm-clients__grid{{grid-template-columns:1fr;gap:36px}}.hm-clients__t{{font-size:42px;margin-bottom:44px}}}}
@media screen and (max-width:639px){{.hm-clients{{padding:70px 16px 60px}}.hm-clients__t{{font-size:32px;margin-bottom:32px}}.hm-clients__i{{grid-template-columns:112px 1fr;gap:18px}}.hm-clients__logo{{min-height:52px}}.hm-clients__logo img{{max-width:104px;max-height:64px}}.hm-clients__d{{font-size:14px}}}}
</style>'''


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')


def section():
    items = ''.join(
        f'<article class="hm-clients__i">'
        f'<div class="hm-clients__logo"><img src="{logo}" alt="{esc(name)}" loading="lazy"></div>'
        f'<p class="hm-clients__d">{esc(descr)}</p>'
        f'</article>'
        for logo, name, descr in CLIENTS)
    return (f'<!--{MARK}-->{CSS}'
            f'<section class="hm-clients"><div class="hm-clients__in">'
            f'<div class="hm-clients__t">Клиенты</div>'
            f'<div class="hm-clients__grid">{items}</div>'
            f'</div></section><!--/{MARK}-->')


def patch_clients_page(path):
    h = open(path, encoding='utf-8').read()
    h = re.sub(f'<!--{MARK}-->.*?<!--/{MARK}-->', '', h, flags=re.S)
    anchor = '<div id="rec228499506"'
    if anchor not in h:
        print(f'  !! {path}: артборд rec228499506 не найден, пропуск')
        return
    h = h.replace(anchor, section() + anchor, 1)
    open(path, 'w', encoding='utf-8').write(h)
    print(f'  ok {path}: сетка на {len(CLIENTS)} клиентов')


# --- главная: t594 «С нами работают» + мобильная лента .mh-logos ---

T594_ITEM = ('<div class="t-col t-card__col t-card__col_withoutbtn t594__item t594__item_6-in-row"> '
             '<img class="t594__img t-img t594__greyonhovercolor t594__alphaonhover"\n'
             'src="{src}" data-original="{src}"\n'
             'imgfield="li_img_{iid}"\n'
             'style="max-width:150px;" alt="{alt}"> </div>')

HOME_NEW = [
    (f'{CC}/bella-systech.png'.lstrip('/'), 'Bella-Systech', 'hm1'),
    (f'{CC}/ceramicanova.png'.lstrip('/'), 'Ceramica Nova', 'hm2'),
]


def patch_home(path):
    h = open(path, encoding='utf-8').read()
    if 'custom-clients/bella-systech.png' in h:
        print(f'  == {path}: логотипы уже добавлены')
        return
    # конец сетки t594 (rec226824033) — последний item с __-71.png (Becar)
    m = re.search(
        r'(<div class="t-col t-card__col t-card__col_withoutbtn t594__item t594__item_6-in-row"> '
        r'<img class="t594__img[^>]*?\n'
        r'src="[^"]*__-71\.png"[^>]*?> </div>)', h, re.S)
    if not m:
        print(f'  !! {path}: t594-сетка не найдена, пропуск')
        return
    add = ' '.join(T594_ITEM.format(src=src, alt=alt, iid=iid) for src, alt, iid in HOME_NEW)
    h = h[:m.end(1)] + ' ' + add + h[m.end(1):]
    # мобильная лента (только index-a2, у index.html mhome нет)
    tail = '" alt="" loading="lazy"></div></div>'
    last_mob = '/images/lib/as3961-6133-4661-b461-666462373731/__-71.png' + tail
    if last_mob in h:
        mob = ''.join(f'<div class="mh-logo"><img src="/{src}" alt="{esc(alt)}" loading="lazy"></div>'
                      for src, alt, _ in HOME_NEW)
        h = h.replace(last_mob,
                      '/images/lib/as3961-6133-4661-b461-666462373731/__-71.png" alt="" loading="lazy"></div>'
                      + mob + '</div>', 1)
        print(f'  ok {path}: +2 в t594 и в .mh-logos')
    else:
        print(f'  ok {path}: +2 в t594')
    open(path, 'w', encoding='utf-8').write(h)


def main():
    print('/clients:')
    for f in ('clients/index.html', 'clients/index-a2.html'):
        patch_clients_page(os.path.join(ROOT, f))
    print('главная:')
    for f in ('index.html', 'index-a2.html'):
        patch_home(os.path.join(ROOT, f))


if __name__ == '__main__':
    sys.exit(main())
