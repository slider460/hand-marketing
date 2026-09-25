# -*- coding: utf-8 -*-
"""
Блок «Стоимость и отзывы» для страниц услуг + разметка Service и BreadcrumbList.

Зачем: по коммерческим запросам Яндекс оценивает, похожа ли страница на место, где услугу
можно заказать: цена «от», условия, сроки, отзывы. Цены утверждены владельцем 14.09.2026,
цитаты дословно из благодарственных писем (scripts/a2/reviews.json, согласие клиентов есть).

    import commerce_block as cb
    cb.render('video')     -> html секции без внешнего контейнера (оборачивает страница)

Отзывы намеренно НЕ размечены schema.org Review: отзывы о себе на своём сайте поисковики
не показывают звёздами, а разметку считают попыткой накрутки.
Стили в своём пространстве имён .hm-cost, цвет акцента страницы передаётся через --hmcost-a.
Длинного тире в текстах нет (правило сайта).
"""
import html as H
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REVIEWS = json.load(open(os.path.join(HERE, 'reviews.json'), encoding='utf-8'))
SITE = 'https://hand-marketing.ru'

PAGES = {
    'video': dict(
        path='/videoproduction/', crumb='Видеопродакшн', accent='#CF6F19',
        service='Видеопродакшн: рекламные и корпоративные ролики',
        prices=[('Рекламный или корпоративный ролик', 150000)],
        facts=['Цена зависит от хронометража, числа съёмочных дней, графики и прав на музыку.',
               'Смету в двух вариантах готовим бесплатно после брифа.',
               'Экспресс-формат снимаем и отдаём за неделю, полноценный ролик или фильм занимает 2–3 недели.'],
        reviews=['sg_video', 'eaton_2019']),
    'event': dict(
        path='/event/', crumb='Организация мероприятий', accent='#C12164',
        service='Организация корпоративных мероприятий под ключ',
        prices=[('Мероприятие под ключ', 500000), ('Мультимедийная зона на мероприятии', 150000)],
        facts=['Цена зависит от формата, площадки, числа гостей и техники.',
               'Концепцию с предварительной сметой готовим бесплатно после брифа.',
               'Лучше всего обращаться за 4–8 недель до даты.'],
        reviews=['messe', 'laut']),
    'exhibition': dict(
        path='/exhibition/', crumb='Застройка выставочных стендов', accent='#673A7E',
        service='Застройка выставочных стендов под ключ с мультимедиа',
        prices=[('Выставочный стенд под ключ', 500000), ('Мультимедийная зона на стенде', 150000)],
        facts=['Цена зависит от площади, конструктива и объёма мультимедиа.',
               'Первые эскизы и зонирование готовим за одну-две недели.',
               'Точный расчёт присылаем после брифа.'],
        reviews=['becar_2018']),
    'content': dict(
        path='/content/', crumb='Мультимедийный контент', accent='#C12164',
        service='Мультимедийные зоны и контент для мероприятий и выставок',
        prices=[('Мультимедийная зона', 150000)],
        facts=['Цена зависит от хронометража, разрешения поверхностей и сложности графики.',
               'Смету считаем бесплатно после брифа.',
               'Контент считаем под конкретную поверхность: экран, фасад, купол, пол, кинетика.'],
        reviews=['eaton_2016', 'becar_2018']),
    'ny': dict(
        path='/event/novogodniy-korporativ/', crumb='Новогодний корпоратив', accent='#C12164',
        parent=('Организация мероприятий', '/event/'),
        service='Организация новогоднего корпоратива под ключ',
        prices=[('Новогодний корпоратив под ключ', 500000), ('Мультимедийная зона на вечере', 150000)],
        facts=['Цена зависит от числа гостей, площадки, программы и техники.',
               'Концепцию с предварительной сметой готовим бесплатно после брифа.',
               'Лучше начинать в октябре: залы на вторую половину декабря разбирают первыми.'],
        reviews=['messe']),
    'mm': dict(
        path='/exhibition/multimedia/', crumb='Мультимедиа для стенда', accent='#673A7E',
        parent=('Застройка выставочных стендов', '/exhibition/'),
        service='Мультимедиа для выставочного стенда: экраны, интерактив и контент',
        prices=[('Мультимедийная зона', 150000), ('Выставочный стенд под ключ', 500000)],
        facts=['Цена зависит от числа экранов, площади поверхностей и сложности контента.',
               'Схему мультимедиа и эскизы готовим за одну-две недели, полный проект от двух недель.',
               'Контент, интерфейсы и монтажное сопровождение делаем сами.'],
        reviews=['becar_2018']),
    'conf': dict(
        path='/event/konferencii/', crumb='Организация конференций', accent='#C12164',
        parent=('Организация мероприятий', '/event/'),
        service='Организация конференций под ключ',
        prices=[('Конференция под ключ', 500000), ('Мультимедийная зона на мероприятии', 150000)],
        facts=['Цена зависит от числа участников, города, площадки, программы и логистики.',
               'Концепцию и предварительную смету готовим бесплатно после брифа.',
               'Лучше начинать за 4–8 недель до даты, с перелётами и отелем для группы раньше.'],
        reviews=['eaton_2016', 'laut']),
    'stand_design': dict(
        path='/exhibition/dizayn-stenda/', crumb='Дизайн выставочного стенда', accent='#673A7E',
        parent=('Застройка выставочных стендов', '/exhibition/'),
        service='Дизайн и проектирование выставочных стендов',
        prices=[('Дизайн-проект стенда', 100000), ('Выставочный стенд под ключ', 500000)],
        facts=['Цена проекта зависит от площади, числа концепций и вариантов, объёма мультимедиа '
               'и детализации чертежей.',
               'Эскизы и зонирование готовим за одну-две недели, полный проект от двух недель.',
               'Смету готовим бесплатно после брифа.'],
        reviews=['becar_2018']),
    'design': dict(
        path='/creativedesign', crumb='Креатив и дизайн', accent='#C12164',
        service='Креативные концепции, фирменный стиль и дизайн полиграфии',
        prices=[],
        facts=['Считаем по объёму: логотип и мини-гайд, полный брендбук или серия макетов это разные сметы.',
               'Смету готовим бесплатно после брифа, в ней видно каждую позицию.',
               'Печать ведём сами, поэтому макет не приходится переделывать под типографию.'],
        reviews=['sg_design', 'becar_2018']),
    'map': dict(
        path='/3dmapping', crumb='3D Mapping и видеомаппинг', accent='#7E3FA0',
        service='3D Mapping и проекционные шоу под ключ',
        prices=[],
        facts=['Цена зависит от площади поверхности, хронометража, сложности графики и числа проекторов.',
               'Шоу на фасаде здания и объектная проекция на сцене это разные бюджеты.',
               'Смету считаем после замеров и брифа, бесплатно.'],
        reviews=['laut']),
    'print': dict(
        path='/printandproduction', crumb='Печать и рекламное производство', accent='#E08A2B',
        service='Широкоформатная печать, полиграфия и рекламное производство',
        prices=[],
        facts=['Считаем по площади, материалу и тиражу. Расчёт по вашему макету присылаем в тот же день.',
               'Дизайн, препресс, печать и монтаж ведёт одна команда, цвет не теряется на стыках.',
               'Возим и монтируем в других городах.'],
        reviews=['becar_2018', 'rzd']),
    'btl': dict(
        path='/btl', crumb='BTL и промо-акции', accent='#D6357E',
        service='BTL-акции, промо-персонал и полевой маркетинг',
        prices=[],
        facts=['Считаем по числу точек, длительности акции, количеству промоутеров и раздаточных материалов.',
               'Смету даём с расчётом на точку, чтобы было видно стоимость масштабирования.',
               'POS-материалы готовим вместе с механикой, отдельный подрядчик на печать не нужен.'],
        reviews=['laut']),
    'digital': dict(
        path='/digital', crumb='Digital и разработка', accent='#2F6FC4',
        service='Сайты, посадочные страницы и digital-продвижение',
        prices=[],
        facts=['Считаем по объёму: посадочная страница, сайт проекта и сопровождение это разные сметы.',
               'Дизайн, тексты, вёрстка и запуск идут одной командой, подрядчиков не подключаем.',
               'Смету готовим бесплатно после брифа.'],
        reviews=['becar_2019']),
    'service': dict(
        path='/service', crumb='Услуги', accent='#673A7E',
        service='Рекламное агентство полного цикла: реклама, мероприятия, выставки, контент',
        prices=[('Рекламный или корпоративный ролик', 150000),
                ('Мультимедийная зона', 150000),
                ('Мероприятие под ключ', 500000),
                ('Выставочный стенд под ключ', 500000)],
        facts=['Это нижние границы по направлениям. Итог зависит от объёма работ, сроков и площадки.',
               'Смету по вашей задаче готовим бесплатно после брифа.',
               'По остальным направлениям, от дизайна до печати, считаем по объёму: цена зависит '
               'от числа макетов, тиража или числа точек.'],
        reviews=['becar_2019', 'eaton_2019']),
    'brandbook': dict(
        path='/creativedesign/brandbook/', crumb='Разработка брендбука', accent='#C12164',
        parent=('Креатив и дизайн', '/creativedesign/'),
        service='Разработка брендбука и фирменного стиля',
        prices=[],
        facts=['Считаем по объёму: логотип с мини-гайдом, фирменный стиль или полный брендбук '
               'с архитектурой бренда это разные сметы.',
               'Логотип и базовая айдентика обычно 2–3 недели, полный брендбук от месяца.',
               'Смету готовим бесплатно после брифа, в ней видно каждую позицию.'],
        reviews=['sg_design', 'becar_2018']),
    'photo': dict(
        path='/photo', crumb='Фотопродакшн', accent='#4CA4E8',
        service='Предметная и каталожная съёмка товаров и оборудования',
        prices=[],
        facts=['Считаем по числу позиций и ракурсов, а не по часам: съёмочный день, обработка '
               'и вырезание фона стоят в смете отдельно.',
               'Смету готовим бесплатно после списка позиций.',
               'Снимаем в студии и на площадке заказчика, по Москве и в регионах.'],
        reviews=['sg_design']),
    'ad': dict(
        path='/videoproduction/reklamnyy-rolik/', crumb='Рекламный ролик', accent='#CF6F19',
        parent=('Видеопродакшн', '/videoproduction/'),
        service='Съёмка рекламного ролика под ключ',
        prices=[('Рекламный ролик', 150000)],
        facts=['Цена зависит от хронометража, числа съёмочных дней, графики и прав на музыку.',
               'Экспресс-формат снимаем за неделю, полноценный ролик или фильм занимает 2–3 недели.',
               'Снимаем по всей России и за рубежом: съёмочная группа, техника и операторы свои.'],
        reviews=['eaton_2019']),
    'film': dict(
        path='/videoproduction/korporativnyy-film/', crumb='Корпоративный фильм', accent='#CF6F19',
        parent=('Видеопродакшн', '/videoproduction/'),
        service='Корпоративный фильм о компании под ключ',
        prices=[('Корпоративный фильм', 150000)],
        facts=['Цена зависит от хронометража, числа съёмочных дней, графики и прав на музыку.',
               'Экспресс-формат снимаем за неделю, полноценный ролик или фильм занимает 2–3 недели.',
               'Снимаем по всей России и за рубежом: съёмочная группа, техника и операторы свои.'],
        reviews=['sg_video']),
    'obj': dict(
        path='/videoproduction/prezentacionnyy-rolik/', crumb='Презентационный ролик', accent='#CF6F19',
        parent=('Видеопродакшн', '/videoproduction/'),
        service='Презентационный ролик объекта под ключ',
        prices=[('Презентационный ролик', 150000)],
        facts=['Цена зависит от хронометража, числа съёмочных дней, графики и прав на музыку.',
               'Экспресс-формат снимаем за неделю, полноценный ролик или фильм занимает 2–3 недели.',
               'Снимаем по всей России и за рубежом: съёмочная группа, техника и операторы свои.'],
        reviews=['morton']),
}

CSS = """<style id="hm-cost-css">
/* приёмы те же, что в секциях главной и услуг: тег с квадратом-маркером,
   радиус 24 с мягкой тенью, кавычка и кружок с инициалами в отзыве.
   Цвета ссылок помечены important: у тильдовских страниц #allrecords a
   красит их фирменным коралловым и перебивает классы */
.hm-cost{--hmcost-a:#673A7E;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:clamp(18px,3vw,40px);align-items:start;margin:0 0 8px}
.hm-cost--solo{grid-template-columns:minmax(0,1fr)}
.hm-cost--solo .hm-cost__price{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:clamp(24px,4vw,56px);align-items:start}
.hm-cost--solo .hm-cost__k{grid-column:1/-1}
.hm-cost--solo .hm-cost__f{margin:0}
.hm-cost__price{border:1.5px solid #ECEEF2;border-radius:24px;padding:clamp(22px,2.6vw,30px);
 background:#fff;box-shadow:0 14px 30px -22px rgba(20,23,28,.5)}
.hm-cost__k{margin:0 0 16px;font-size:11px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;
 color:var(--hmcost-a);display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.hm-cost__k::before{content:"";width:11px;height:11px;border-radius:3px;background:var(--hmcost-a);flex:none}
.hm-cost__k a{color:var(--hmcost-a)!important;text-decoration:none;border-bottom:1px solid currentColor}
.hm-cost__row{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:4px 16px;padding:14px 0;border-top:1px solid #ECEEF2}
.hm-cost__row:first-of-type{border-top:0;padding-top:0}
.hm-cost__what{font-size:15px;font-weight:600;color:#14171C;line-height:1.35}
.hm-cost__v{font-size:clamp(24px,2.8vw,32px);font-weight:900;letter-spacing:-.02em;color:var(--hmcost-a);white-space:nowrap}
.hm-cost__v small{font-size:.5em;font-weight:800;margin-right:4px;color:#5A616A}
.hm-cost__f{margin:18px 0 0;padding:0;list-style:none;display:grid;gap:9px}
.hm-cost__f li{position:relative;padding-left:20px;font-size:14.5px;line-height:1.55;color:#5A616A}
.hm-cost__f li::before{content:"";position:absolute;left:0;top:.5em;width:9px;height:9px;border-radius:3px;background:var(--hmcost-a)}
.hm-cost__rev{display:grid;gap:16px;align-content:start}
.hm-cost__rk{margin:0;font-size:11px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:#5A616A;
 display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.hm-cost__rk::before{content:"";width:11px;height:11px;border-radius:3px;background:#5A616A;flex:none}
.hm-cost__rk a{color:var(--hmcost-a)!important;text-decoration:none;border-bottom:1px solid currentColor;font-weight:800}
.hm-cost__q{margin:0;position:relative;background:#fff;border:1.5px solid #ECEEF2;border-radius:24px;
 padding:22px 24px;box-shadow:0 14px 30px -22px rgba(20,23,28,.5)}
.hm-cost__q::before{content:"“";display:block;font:900 52px/.55 'Montserrat',Arial,sans-serif;
 color:var(--hmcost-a);opacity:.18;margin-bottom:10px}
.hm-cost__q blockquote{margin:0 0 14px;font-size:clamp(15px,1.4vw,16.5px);line-height:1.6;color:#14171C}
.hm-cost__q figcaption{font-size:13.5px;line-height:1.45;color:#5A616A}
.hm-cost__q figcaption b{display:block;color:#14171C;font-size:14.5px}
.hm-cost .hm-cost__q a{color:var(--hmcost-a)!important;font-weight:800;text-decoration:none;white-space:nowrap;
 border-bottom:1px solid currentColor}
@media(max-width:860px){.hm-cost{grid-template-columns:minmax(0,1fr)}.hm-cost--solo .hm-cost__price{grid-template-columns:minmax(0,1fr)}.hm-cost--solo .hm-cost__f{margin:16px 0 0}}
</style>"""


def rub(n):
    return f'{n:,}'.replace(',', ' ') + ' ₽'


def jsonld(key):
    p = PAGES[key]
    service = {
        '@context': 'https://schema.org', '@type': 'Service',
        'name': p['service'], 'serviceType': p['crumb'],
        'url': SITE + p['path'],
        'areaServed': {'@type': 'Country', 'name': 'Россия'},
        'provider': {'@type': 'Organization', 'name': 'Hand Marketing', 'url': SITE + '/',
                     'telephone': '+7 495 580 75 37', 'email': 'info@hand-marketing.ru'},
    }
    if p['prices']:
        service['offers'] = [
            {'@type': 'Offer', 'name': name, 'priceCurrency': 'RUB',
             'priceSpecification': {'@type': 'PriceSpecification', 'minPrice': price,
                                    'priceCurrency': 'RUB'}}
            for name, price in p['prices']]
    crumbs = {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Главная', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': p.get('parent', ('Услуги', '/service/'))[0],
             'item': SITE + p.get('parent', ('Услуги', '/service/'))[1]},
            {'@type': 'ListItem', 'position': 3, 'name': p['crumb'], 'item': SITE + p['path']},
        ]}
    if key == 'service':  # сама страница услуг вторым и третьим шагом была бы дублем
        crumbs['itemListElement'] = crumbs['itemListElement'][:2]
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
    return (f'<script type="application/ld+json" data-hmc="service">{dump(service)}</script>'
            f'<script type="application/ld+json" data-hmc="crumbs">{dump(crumbs)}</script>')


def render(key, with_css=True, with_ld=True):
    """with_css/with_ld=False для второй копии той же страницы (тильдовский /event держит
    мобильную и десктопную версии в одном файле; стили и разметку дублировать нельзя)."""
    p = PAGES[key]
    rows = ''.join(f'<div class="hm-cost__row"><span class="hm-cost__what">{H.escape(name)}</span>'
                   f'<span class="hm-cost__v"><small>от</small>{rub(price)}</span></div>'
                   for name, price in p['prices'])
    facts = ''.join(f'<li>{H.escape(f)}</li>' for f in p['facts'])
    kicker = ('Стоимость' if p['prices'] else 'Как считаем смету') + \
        ' <a href="/price/">все цены&nbsp;→</a>'
    price = (f'<div class="hm-cost__price"><p class="hm-cost__k">{kicker}</p>{rows}'
             f'<ul class="hm-cost__f">{facts}</ul></div>')
    rev = ''
    if p['reviews']:
        qs = ''
        for k in p['reviews']:
            r = REVIEWS[k]
            who = H.escape(r['person'] + ', ' + r['role'])
            link = f' <a href="{r["case"]}">Кейс&nbsp;→</a>' if r.get('case') else ''
            qs += (f'<figure class="hm-cost__q"><blockquote>«{H.escape(r["quote"])}»</blockquote>'
                   f'<figcaption><b>{H.escape(r["company"])}</b>{who}{link}</figcaption></figure>')
        rev = (f'<div class="hm-cost__rev"><p class="hm-cost__rk">Из благодарственных писем'
               f' <a href="/reviews/">все письма&nbsp;→</a></p>{qs}</div>')
    solo = '' if rev else ' hm-cost--solo'
    return ((CSS if with_css else '') +
            f'<div class="hm-cost{solo}" style="--hmcost-a:{p["accent"]}" data-hmc="{key}">{price}{rev}</div>'
            + (jsonld(key) if with_ld else ''))
