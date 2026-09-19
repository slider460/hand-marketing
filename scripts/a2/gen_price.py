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
    ('Выставочный стенд под ключ', '/exhibition/', 500000,
     'Проект и дизайн стенда, конструктив, застройка и монтаж, мультимедиа '
     'и контент, демонтаж.',
     'Площадь, этажность, конструктив, объём мультимедиа, выставка и город.'),
    ('3D Mapping и проекционные шоу', '/3dmapping/', None,
     'Замеры объекта, сценарий, 3D-графика под геометрию, оборудование, монтаж '
     'и показ.',
     'Площадь поверхности, хронометраж, число проекторов, сложность графики.'),
    ('Креатив, фирменный стиль, дизайн', '/creativedesign/', None,
     'Концепция, макеты, айдентика или брендбук, файлы и гайдлайны.',
     'Объём: логотип с мини-гайдом, полный брендбук или серия макетов это '
     'разные сметы.'),
    ('Печать и рекламное производство', '/printandproduction/', None,
     'Препресс, печать, постпечатная обработка, сборка конструкций, доставка '
     'и монтаж.',
     'Площадь и материал, тираж, постобработка, монтаж в другом городе.'),
    ('Предметная и каталожная съёмка', '/photo', None,
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
    ('Договор', 'Работаем с юридическими лицами: договор, счёт, закрывающие документы.'),
    ('Работа', 'Производство внутри агентства, без цепочки посредников с наценками.'),
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

CSS = """<style id="pr-css">
.pr{--ink:#14171C;--mut:#5A616A;--a:#673A7E;--line:rgba(20,23,28,.12);
 font-family:'Montserrat',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff}
.pr *{box-sizing:border-box}
.pr__wrap{max-width:1180px;margin:0 auto;padding:0 40px}
.pr-hero{padding:64px 0 36px}
.pr-hero h1{margin:0 0 16px;font-size:clamp(28px,4vw,48px);font-weight:800;letter-spacing:-.025em;line-height:1.08}
.pr-hero p{margin:0 0 10px;max-width:72ch;font-size:16.5px;line-height:1.65;color:var(--mut)}
.pr-rows{display:grid;gap:14px;padding:10px 0 8px}
.pr-row{display:grid;grid-template-columns:minmax(0,1.15fr) 190px;gap:24px;align-items:start;
 border:1px solid var(--line);border-radius:18px;padding:22px 24px;background:#fff}
.pr-row h2{margin:0 0 10px;font-size:19px;font-weight:800;letter-spacing:-.01em}
.pr-row h2 a{color:inherit;text-decoration:none;border-bottom:2px solid rgba(103,58,126,.35)}
.pr-row h2 a:hover{color:var(--a)}
.pr-row dl{margin:0;display:grid;gap:8px}
.pr-row dt{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--a)}
.pr-row dd{margin:0 0 4px;font-size:14.5px;line-height:1.6;color:var(--mut)}
.pr-price{text-align:right}
.pr-price b{display:block;font-size:26px;font-weight:800;letter-spacing:-.02em;white-space:nowrap}
.pr-price small{display:block;font-size:12px;font-weight:700;letter-spacing:.08em;
 text-transform:uppercase;color:var(--mut);margin-bottom:2px}
.pr-price span{display:block;margin-top:6px;font-size:13px;line-height:1.5;color:var(--mut)}
.pr-sec{padding:48px 0 0}
.pr-sec h2{margin:0 0 8px;font-size:clamp(22px,2.6vw,30px);font-weight:800;letter-spacing:-.02em}
.pr-sec p.lead{margin:0 0 24px;max-width:72ch;font-size:16px;line-height:1.65;color:var(--mut)}
.pr-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;counter-reset:pr}
.pr-step{counter-increment:pr;border-top:2px solid var(--a);padding-top:12px}
.pr-step::before{content:"0" counter(pr);font-weight:800;font-size:13px;color:var(--a);letter-spacing:.08em}
.pr-step h3{margin:6px 0 6px;font-size:15px;font-weight:700;line-height:1.35}
.pr-step p{margin:0;font-size:13.5px;line-height:1.55;color:var(--mut)}
.pr-faq{display:grid;gap:10px;max-width:860px}
.pr-faq details{border:1px solid var(--line);border-radius:14px;padding:0 20px}
.pr-faq summary{cursor:pointer;list-style:none;position:relative;padding:16px 36px 16px 0;font-size:15.5px;font-weight:700}
.pr-faq summary::-webkit-details-marker{display:none}
.pr-faq summary::after{content:"";position:absolute;right:2px;top:50%;width:11px;height:11px;
 transform:translateY(-70%) rotate(45deg);border-right:2.5px solid var(--a);border-bottom:2.5px solid var(--a);transition:transform .2s}
.pr-faq details[open] summary::after{transform:translateY(-30%) rotate(225deg)}
.pr-faq p{margin:0 0 16px;font-size:14.5px;line-height:1.65;color:var(--mut)}
.pr-cta{margin:44px 0 64px;padding:26px 28px;border-radius:20px;background:#F8F6FA;
 font-size:16px;line-height:1.6}
.pr-cta a{color:var(--a);font-weight:700}
@media(max-width:1000px){.pr-steps{grid-template-columns:repeat(2,1fr)}}
@media(max-width:760px){.pr__wrap{padding:0 18px}.pr-row{grid-template-columns:1fr}
 .pr-price{text-align:left}.pr-steps{grid-template-columns:1fr}}
</style>"""


def rub(n):
    return f'{n:,}'.replace(',', ' ') + ' ₽'


def esc(t):
    return H.escape(t, quote=False)


def rows_html():
    out = ''
    for name, href, price, inc, dep in ROWS:
        if price:
            money = f'<small>от</small><b>{rub(price)}</b>'
        else:
            money = ('<small>по объёму</small><span>Считаем по вашему списку работ, '
                     'смета бесплатна</span>')
        out += (f'<article class="pr-row">'
                f'<div><h2><a href="{href}">{esc(name)}</a></h2>'
                f'<dl><dt>Что входит</dt><dd>{esc(inc)}</dd>'
                f'<dt>От чего зависит цена</dt><dd>{esc(dep)}</dd></dl></div>'
                f'<div class="pr-price">{money}</div></article>')
    return out


def page():
    steps = ''.join(f'<div class="pr-step"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
                    for t, d in STEPS)
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
                  for q, a in FAQ)
    title = 'Цены на услуги агентства: ролики, мероприятия, стенды | Hand Marketing'
    descr = ('Сколько стоит работа Hand Marketing: рекламный ролик и мультимедийная зона '
             'от 150 000 ₽, мероприятие под ключ и выставочный стенд от 500 000 ₽. '
             'Что входит в смету и от чего зависит цена.')
    ld_faq = {'@context': 'https://schema.org', '@type': 'FAQPage',
              'mainEntity': [{'@type': 'Question', 'name': q,
                              'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    ld_crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Главная', 'item': 'https://hand-marketing.ru/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Цены', 'item': URL}]}
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))

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
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')

    body = (
        f'{rc.header()}<main class="pr">'
        '<section class="pr-hero"><div class="pr__wrap">'
        '<h1>Цены на услуги</h1>'
        '<p>Ниже нижние границы по направлениям и то, из чего складывается смета. '
        'Точную цифру называем после брифа: мы считаем работу, а не продаём позиции '
        'из прайса.</p>'
        '<p>Смету готовим бесплатно и обычно в двух вариантах, чтобы было видно, '
        'на чём можно сэкономить без потери результата.</p>'
        '</div></section>'
        f'<div class="pr__wrap"><div class="pr-rows">{rows_html()}</div>'
        '<section class="pr-sec"><h2>Как мы считаем</h2>'
        '<p class="lead">Смета собирается из позиций, а не из общей суммы: видно, '
        'сколько стоит съёмочный день, сколько графика и сколько работа на площадке.</p>'
        f'<div class="pr-steps">{steps}</div></section>'
        '<section class="pr-sec"><h2>Вопросы о деньгах</h2>'
        f'<div class="pr-faq">{faq}</div></section>'
        '<p class="pr-cta">Расскажите задачу, и мы посчитаем. Если сомневаетесь, '
        'посмотрите <a href="/project">проекты</a> и <a href="/reviews/">письма клиентов</a>: '
        'там видно, что мы уже делали и за какой срок.</p>'
        '</div></main>'
        f'<a id="lead"></a>{rc.footer()}{rc.JS}'
        f'<script type="application/ld+json">{dump(ld_faq)}</script>'
        f'<script type="application/ld+json">{dump(ld_crumbs)}</script>'
        '</body></html>')
    return head + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'price')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('создано:', p, os.path.getsize(p) // 1024, 'КБ')
