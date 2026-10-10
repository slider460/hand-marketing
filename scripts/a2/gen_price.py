#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/price/index.html: страница «Цены».

Зачем: «сколько стоит» это первый вопрос посетителя и один из самых частых
уточняющих запросов. У всех конкурентов из топ-10 цены на странице есть,
у нас они были только на четырёх страницах услуг.

Цены объявлены владельцем 14.09.2026: ролик и мультимедийная зона от 150 000 ₽,
мероприятие и выставочный стенд от 500 000 ₽. По остальным направлениям цифру
не объявляли, поэтому там описано, из чего складывается смета. Выдумывать
диапазоны нельзя: клиент придёт с этой цифрой на переговоры.

Правки: ТОЛЬКО через этот скрипт.
Прогон: python3 scripts/a2/finalize_page.py gen_price.py
"""
import html as H
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
sys.path.insert(0, HERE)
import hm_ds as ds  # noqa: E402

spec = importlib.util.spec_from_file_location('rc', os.path.join(HERE, 'react-chrome.py'))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

URL = 'https://hand-marketing.ru/price/'

# (направление, ссылка, цена или None, что входит в базовую работу, от чего зависит цена)
ROWS = [
    ('Рекламный ролик', '/videoproduction/reklamnyy-rolik/', 150000,
     'Сценарий и раскадровка, съёмочная смена своей группой, монтаж, цвет, звук, '
     'версии под площадки.',
     'Хронометраж, число съёмочных дней, объём графики и 3D, права на музыку, '
     'съёмка с медийным лицом.'),
    ('Корпоративный фильм', '/videoproduction/korporativnyy-film/', 150000,
     'Сценарий, съёмка на объекте, интервью, монтаж и графика, короткая версия '
     'для соцсетей.',
     'Хронометраж, число локаций и городов, количество интервью, сложность графики.'),
    ('Презентационный ролик объекта', '/videoproduction/prezentacionnyy-rolik/', 150000,
     'Съёмка объекта и окружения, аэросъёмка, инфографика с цифрами, монтаж.',
     'Площадь объекта, аэросъёмка, число версий под разные аудитории.'),
    ('Мультимедийная зона', '/content/', 150000,
     'Идея и раскадровка, контент под конкретную поверхность, сборка и тесты '
     'на площадке.',
     'Хронометраж, разрешение поверхностей, интерактив, число экранов и сцен.'),
    ('Мероприятие под ключ', '/event/', 500000,
     'Концепция и сценарий, площадка, застройка и декор, техника, ведущий, '
     'работа команды на площадке, съёмка.',
     'Формат, число гостей, площадка, объём техники и артистов, город.'),
    ('Новогодний корпоратив', '/event/novogodniy-korporativ/', 500000,
     'Концепция вечера, площадка, оформление, программа и ведущий, техника, '
     'подарки гостям, фото- и видеосъёмка.',
     'Число гостей, площадка, программа и артисты, объём проекций и декора.'),
    ('Конференция под ключ', '/event/konferencii/', 500000,
     'Площадка и отель, перелёты и трансферы участников, зал, сцена и техника, программа '
     'и тайминг, материалы участника, трансляция и съёмка.',
     'Число участников, город, площадка, программа, логистика и трансляция.'),
    ('Выставочный стенд под ключ', '/exhibition/', 500000,
     'Проект и дизайн стенда, конструктив, застройка и монтаж, мультимедиа '
     'и контент, демонтаж.',
     'Площадь, этажность, конструктив, объём мультимедиа, выставка и город.'),
    ('Дизайн-проект выставочного стенда', '/exhibition/dizayn-stenda/', 100000,
     'Концепция, зонирование, 3D-визуализация, чертежи и спецификации. Можно заказать '
     'только проект для своего застройщика.',
     'Площадь, число концепций и вариантов, объём мультимедиа, детализация чертежей.'),
    ('Мультимедиа для выставочного стенда', '/exhibition/multimedia/', 150000,
     'Экраны, проекции и интерактив под конструктив стенда, контент под каждую '
     'поверхность, интерфейсы, монтаж и запуск на выставке.',
     'Число экранов, площадь поверхностей, интерактив, сложность контента.'),
    ('3D Mapping и проекционные шоу', '/3dmapping/', None,
     'Замеры объекта, сценарий, 3D-графика под геометрию, оборудование, монтаж '
     'и показ.',
     'Площадь поверхности, хронометраж, число проекторов, сложность графики.'),
    ('Креатив, фирменный стиль, дизайн', '/creativedesign/', None,
     'Концепция, макеты, айдентика или брендбук, файлы и гайдлайны.',
     'Объём: логотип с мини-гайдом, полный брендбук или серия макетов это '
     'разные сметы.'),
    ('Брендбук и фирменный стиль', '/creativedesign/brandbook/', None,
     'Логотип и знак, цвет и шрифты, фирменная графика, носители, правила '
     'применения и шаблоны в рабочих форматах.',
     'Объём: логотип с мини-гайдом делаем за 2–3 недели, полный брендбук '
     'от месяца.'),
    ('Печать и рекламное производство', '/printandproduction/', None,
     'Препресс, печать, постпечатная обработка, сборка конструкций, доставка '
     'и монтаж.',
     'Площадь и материал, тираж, постобработка, монтаж в другом городе.'),
    ('Предметная и каталожная съёмка', '/photo/', None,
     'Съёмка позиций в студии или на объекте, обработка, вырезание фона, '
     'кадрирование под площадки.',
     'Число позиций и ракурсов, сложность ретуши, выезд на площадку заказчика.'),
    ('BTL и промо-акции', '/btl/', None,
     'Механика, персонал с обучением, POS-материалы, супервайзинг, отчётность.',
     'Число точек и городов, длительность, количество промоутеров, раздаточные '
     'материалы.'),
    ('Сайты и посадочные страницы', '/digital/', None,
     'Структура, дизайн, тексты, сборка, формы, аналитика и запуск.',
     'Объём: одна страница, сайт проекта или сопровождение.'),
]

STEPS = [
    ('Бриф', 'Задача, аудитория, сроки и рамки бюджета. Разговор занимает полчаса.'),
    ('Решение', 'Предлагаем, как сделать. Если задача в бюджет не помещается, скажем '
     'сразу и предложим другой формат, а не будем подгонять смету.'),
    ('Смета', 'Позиции отдельными строками: видно, за что платите и что можно убрать. '
     'Смета бесплатна и ни к чему не обязывает.'),
    ('Договор', 'Работаем с юридическими лицами: договор, счёт, закрывающие документы, НДС.'),
    ('Работа', 'Съёмку, дизайн и контент делает наша команда, за печать и застройку отвечаем сами.'),
]

FAQ = [
    ('Почему нет прайса по позициям?',
     'Потому что он вводил бы в заблуждение. Ролик на один съёмочный день и ролик '
     'с графикой, кастингом и выездом в другой город стоят по-разному, хотя в прайсе '
     'назывались бы одинаково. Мы даём вилку «от» и считаем смету по конкретной задаче.'),
    ('Сколько стоит смета?',
     'Ничего. После брифа мы бесплатно готовим решение и расчёт, обычно в двух '
     'вариантах: базовом и расширенном.'),
    ('Можно ли уложиться в фиксированный бюджет?',
     'Да, если сказать его в начале. Мы соберём работу под сумму: меньше съёмочных дней, '
     'проще графика, другой формат мероприятия. Это честнее, чем показать красивую '
     'концепцию, которая не помещается в деньги.'),
    ('От чего цена растёт сильнее всего?',
     'От числа съёмочных дней и выездов в другие города, от объёма 3D-графики, '
     'от площади стенда и объёма мультимедиа на нём, от числа гостей на мероприятии.'),
    ('Вы работаете в регионах, это дороже?',
     'Снимаем и строим по всей России и за рубежом. В смете это отдельные строки: '
     'переезд команды, логистика оборудования, проживание. Мы показываем их отдельно, '
     'чтобы было видно, во что обходится география.'),
    ('Можно заказать одну услугу, а не весь цикл?',
     'Да. Большинство проектов начинается с одной задачи. Связка появляется потом, '
     'когда видно, что ролик, стенд и печать удобнее делать в одном месте.'),
]

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px" alt=""></div></noscript>')



def rub(n):
    return f'{n:,}'.replace(',', ' ') + ' ₽'


def esc(t):
    return H.escape(t, quote=False)


# метка направления по разделу сайта, цвета как в метках услуг на главной
TAGS = [('/videoproduction/', 'Video', ds.VID), ('/content/', 'Content', ds.CON), ('/event/', 'Event', ds.EV),
        ('/exhibition/', 'Exhibition', ds.EXH), ('/3dmapping/', '3D', ds.MAP),
        ('/creativedesign/', 'Creative', ds.CRE), ('/printandproduction/', 'Print', ds.PRN),
        ('/photo/', 'Photo', ds.PHO), ('/btl/', 'BTL', ds.BTL), ('/digital/', 'Digital', ds.DIG)]

CSS = """<style id="pr-css">
.pr-head,.pr-row{display:grid;grid-template-columns:118px minmax(0,1.1fr) minmax(0,2.8fr) 190px;gap:28px;align-items:start}
.pr-head{padding:0 0 14px;border-bottom:2px solid #111;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#4C4C4C}
.pr-head__dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.pr-head span:last-child{text-align:right}
.pr-row{padding:26px 0;border-bottom:1px solid #E6E6E6}
.pr-tag{justify-self:start;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--c);border:1.5px solid var(--c);border-radius:999px;padding:5px 12px;white-space:nowrap}
.pr-row h3{margin:0;font-size:18px;font-weight:700;line-height:1.35}
.pr-row h3 a{color:#111;text-decoration:none;border-bottom:2px solid transparent;transition:border-color .15s}
.pr-row h3 a:hover{border-bottom-color:#FFF700}
.pr-row dl{margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.pr-row dt{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.pr-row dd{margin:0;font-size:14.5px;line-height:1.6;color:#4C4C4C}
.pr-price{text-align:right}
.pr-price b{display:block;font-size:26px;font-weight:800;color:#111;white-space:nowrap}
.pr-price small{display:block;font-size:18px;font-weight:800;color:#4C4C4C}
.pr-price span{display:block;margin-top:6px;font-size:12.5px;line-height:1.45;color:#8A8A8A}
@media(max-width:980px){
 .pr-head{display:none}
 .pr-row{grid-template-columns:minmax(0,1fr) auto;gap:12px 20px}
 .pr-tag{grid-column:1/-1}
 .pr-row dl{grid-column:1/-1;grid-row:3;grid-template-columns:minmax(0,1fr);gap:12px}
 .pr-row dt{position:static;width:auto;height:auto;overflow:visible;clip:auto;white-space:normal;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#8A8A8A;margin-bottom:4px}
 .pr-price b{font-size:22px}
 .pr-price span{max-width:16ch;margin-left:auto}
}
</style>"""


def rows_html():
    out = ''
    for name, href, price, inc, dep in ROWS:
        tag, color = next((t, c) for pre, t, c in TAGS if href.startswith(pre))
        if price:
            money = f'<b>от {ds.rub(price)}</b>'
        else:
            money = '<small>по объёму</small><span>Считаем по вашему списку работ, смета бесплатна</span>'
        out += (f'<article class="pr-row" style="--c:{color}"><span class="pr-tag">{tag}</span>'
                f'<h3><a href="{href}">{esc(name)}</a></h3>'
                f'<dl><div><dt>Что входит</dt><dd>{esc(inc)}</dd></div>'
                f'<div><dt>От чего зависит цена</dt><dd>{esc(dep)}</dd></div></dl>'
                f'<div class="pr-price">{money}</div></article>')
    head = ('<div class="pr-head" aria-hidden="true"><span>Направление</span><span>Услуга</span>'
            '<span class="pr-head__dl"><span>Что входит</span><span>От чего зависит цена</span></span>'
            '<span>Стоимость</span></div>')
    return head + out


def page():
    title = 'Цены на услуги агентства: ролики, мероприятия, стенды | Hand Marketing'
    descr = ('Сколько стоит работа Hand Marketing: рекламный ролик и мультимедийная зона '
             'от 150 000 ₽, мероприятие под ключ и выставочный стенд от 500 000 ₽. '
             'Что входит в смету и от чего зависит цена.')
    ld_crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Главная', 'item': 'https://hand-marketing.ru/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Цены', 'item': URL}]}
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))

    lede = ('Ниже нижние границы по направлениям и то, из чего складывается смета. Точную цифру называем '
            'после брифа: мы считаем работу, а не продаём позиции из прайса. Смету готовим бесплатно '
            'и обычно в двух вариантах, чтобы было видно, на чём можно сэкономить без потери результата.')
    hero = ds.hero('Price', 'Об агентстве · Стоимость', 'Цены на услуги', esc(lede),
                   chips=('смета бесплатно', 'обычно в двух вариантах', 'договор, счёт, НДС'),
                   ctas=(('Посчитать проект', '#lead', 'y'), ('Проекты', '/project/', 'o')), figs=0)
    crumbs = ds.crumbs([('Главная', '/'), ('Цены', None)])
    banner = ds.banner(None, '/videos/price-hero-poster.jpg', 'Кадры из проектов агентства',
                       'Из наших проектов', 'Ролики, мероприятия, стенды',
                       'Нарезка из шоурила агентства: съёмки, мероприятия и застройка разных лет.',
                       video='/videos/price-hero-loop.mp4')
    table = ds.sec(rows_html(), 'Стоимость по направлениям', icons=4, top=True)
    steps = ds.band(ds.steps([(t, esc(d)) for t, d in STEPS], cols=5), 'Как мы считаем',
                    esc('Смета собирается из позиций, а не из общей суммы: видно, сколько стоит съёмочный '
                        'день, сколько графика и сколько работа на площадке.'), fig='h')
    faq = ds.sec(ds.faq(FAQ), 'Вопросы о деньгах')
    cta = ds.sec('<p class="hd-lead" style="margin:0;font-size:18px;color:#111">Расскажите задачу, и мы '
                 'посчитаем. Если сомневаетесь, посмотрите <a href="/project">проекты</a>, '
                 '<a href="/team/">команду</a> и <a href="/reviews/">письма клиентов</a>: там видно, что '
                 'мы уже делали и за какой срок.</p>', alt=True)

    head = (
        '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{title}</title>'
        f'<meta name="description" content="{H.escape(descr)}">'
        f'<link rel="canonical" href="{URL}">'
        '<meta name="robots" content="index, follow">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{H.escape(title)}">'
        f'<meta property="og:description" content="{H.escape(descr)}">'
        f'<meta property="og:url" content="{URL}">'
        '<meta property="og:image" content="https://hand-marketing.ru/static/thb/as3230-6663-4363-b038-333866373133/-/resize/504x/__76876-145.png">'
        + rc.FONT + rc.CSS + ds.CSS + CSS + METRIKA + '</head><body>')
    body = (f'{rc.header()}<main class="hd" style="--a:{ds.VIOLET}">{crumbs}{hero}{banner}{table}{steps}{faq}{cta}</main>'
            f'{ds.BANNER_JS}<a id="lead"></a>{rc.footer()}{rc.JS}'
            f'<script type="application/ld+json">{dump(ld_crumbs)}</script>'
            '</body></html>')
    return head + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'price')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('создано:', p, os.path.getsize(p) // 1024, 'КБ')
