#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/event/novogodniy-korporativ/index.html — посадочную страницу
«Организация новогоднего корпоратива».

Зачем отдельная страница, а не абзац на /event: спрос сезонный и отдельный
(Вордстат, Москва: «новогодний корпоратив» 3257, «…в Москве» 399, «…2027» 193,
«организация новогоднего корпоратива» 83, «…под ключ» 45), а в топ-10 Яндекса стоят
именно посадочные страницы агентств, не разделы услуг.

Чем отличается от конкурентов: у них каталог форматов и площадок, у нас три реальных
новогодних проекта со своей механикой. Обещаем только то, что показываем: квестов,
казино и выездных форматов в портфолио нет, их тут нет и в тексте.

Факты подтверждены владельцем 19.09.2026: Samsung более 200 гостей, Messe более 50,
других новогодних корпоративов в портфолио нет, цена от 500 000 ₽, съёмка своя.
Своя техника — только для видеопродакшна; проекция, свет и звук идут через постоянных
технических партнёров ([[agency-facts-owner]]).

Сигнатурная механика страницы, которой на сайте ещё не было: обратный отсчёт до вечера
(шкала от «за 8 недель» к «утру после», кадры меняются от пустого зала к празднику).

Правки: ТОЛЬКО через этот скрипт. Прогон: python3 scripts/a2/finalize_page.py gen_ny_korporativ.py
"""
import html as H
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import commerce_block as cb  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
spec = importlib.util.spec_from_file_location('rc', os.path.join(HERE, 'react-chrome.py'))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

URL = 'https://hand-marketing.ru/event/novogodniy-korporativ/'
TITLE = 'Организация новогоднего корпоратива в Москве под ключ | Hand Marketing'
DESCR = ('Новогодний корпоратив под ключ: концепция, площадка или ваш офис, мультимедиа '
         'вместо декораций, программа и подарки сотрудникам. От 500 000 ₽. Кейсы Samsung и Messe.')
ACCENT = '#C12164'
IMG = '/images'

PROJECTS = [
    ('/event/samsung/', f'{IMG}/samsung/forest.jpg', 'Samsung, Новый год 2020',
     'Мультимедиа вместо декораций',
     'Более 200 гостей ужинали внутри картинки: зимний лес шёл по дуге балкона. Сетка над сценой '
     'уходила вниз за 0,2 секунды, а почтовый ящик Деда Мороза отвечал гостю прямо на стене.',
     'Зал Samsung под панорамной проекцией зимнего леса'),
    ('/event/messeduessleldorf/', f'{IMG}/messe/disco.jpg', 'Messe Düsseldorf Moscow',
     'Новый год в собственном офисе',
     'Более 50 человек встретили Новый год там, где работают каждый день. Мы поделили офис на '
     'четыре зоны, поставили бар в кирпичную арку и фуршет вдоль стены. К утру офис снова работал.',
     'Танцпол в офисе Messe Düsseldorf: гости на новогоднем вечере'),
    ('/creative/rgd/suvenir/', f'{IMG}/rgd-suvenir/box.jpg', 'ЦМ РЖД',
     'Подарок, который работает весь год',
     'Набор из шести позиций в одной айдентике и перекидной календарь на 13 листов: каждый месяц '
     'закреплён за услугой дирекции. Такой подарок висит у клиента все двенадцать месяцев.',
     'Новогодний сувенирный набор ЦМ РЖД в коробке'),
]

WORKS = [
    ('Концепция и сценарий', 'Идея вечера, сюжет по частям программы, тайминг.'),
    ('Площадка', 'Подбираем зал или работаем на вашей территории, включая офис.'),
    ('Оформление и мультимедиа', 'Проекции, экраны, фотозоны, интерактивные зоны.'),
    ('Программа', 'Ведущий, артисты, конкурсы, шаржист.'),
    ('Техника', 'Звук, свет и проекция: подбираем под площадку, привозим и ведём весь вечер.'),
    ('Фуршет и бар', 'Кейтеринг, барная станция, посуда, карточки меню.'),
    ('Подарки', 'Наборы для сотрудников и клиентов в фирменном стиле.'),
    ('Фото и видео', 'Съёмка вечера своими операторами и ролик по итогам.'),
]

IDEAS = [
    (f'{IMG}/samsung/pano-1.jpg', 'Зимний лес на панорамных полотнах',
     'Гости ужинают внутри картинки, а контент меняется медленно и не спорит с разговором за столом.',
     'Панорамная проекция зимнего леса по дуге зала'),
    (f'{IMG}/samsung/mail-drop.jpg', 'Почтовый ящик Деда Мороза',
     'Гость опускает открытку, срабатывает датчик внутри ящика, и на стене появляется ответ.',
     'Гость опускает открытку в стеклянный ящик с подсветкой'),
    (f'{IMG}/samsung/mesh.jpg', 'Логотип на сетке перед сценой',
     'Номер начинается с графики в воздухе, полотно уходит вниз, и сцена открывается целиком.',
     'Проекционная сетка с логотипом перед сценой'),
    (f'{IMG}/messe/bar.jpg', 'Бар в кирпичной арке',
     'Проём, который весь год был просто стеной, на вечер становится барной стойкой с гирляндой.',
     'Барная стойка в кирпичной арке офиса'),
    (f'{IMG}/messe/gifts.jpg', 'Стойка ресепшена как выдача подарков',
     'Крафт-пакеты по числу сотрудников стоят в ряд ещё до прихода гостей.',
     'Подарочные крафт-пакеты в ряд на стойке ресепшена'),
    (f'{IMG}/rgd-suvenir/sheet-march.jpg', 'Подарок-календарь',
     'Каждый лист отдан одной услуге компании, поэтому подарок объясняет бизнес весь год.',
     'Лист перекидного календаря ЦМ РЖД'),
]

COUNTDOWN = [
    ('8', 'недель', 'Бриф и концепция', 'Идея вечера, смета по вариантам, выбор площадки. '
     'В декабре хорошие залы разбирают первыми, поэтому начинать лучше в октябре.', None, None),
    ('6', 'недель', 'Сценарий и программа', 'Тайминг вечера, ведущий и артисты, подрядчики по '
     'кейтерингу, состав подарков.', None, None),
    ('4', 'недели', 'Контент и оформление', 'Рисуем графику под конкретные поверхности зала, '
     'заказываем оформление и подарки, бронируем технику.',
     f'{IMG}/samsung/content-1.jpg', 'Кадр новогоднего контента для проекции'),
    ('1', 'неделя', 'Монтажный план', 'Согласование с площадкой, схема подвеса, прогон сценария '
     'и репетиция номеров.', f'{IMG}/samsung/build-1.jpg', 'Монтаж в пустом зале: леса и фермы'),
    ('0', 'день вечера', 'Монтаж и сопровождение', 'Сборка, юстировка проекций, звук и свет, '
     'весь вечер за пультом сидит наш оператор.', f'{IMG}/samsung/foh.jpg',
     'Пульт оператора в зале: лист сцен на экране медиасервера'),
    ('+1', 'утро', 'Демонтаж', 'Вывозим оборудование и декорации. Если праздник был в офисе, '
     'к началу рабочего дня это снова офис.', f'{IMG}/messe/talk.jpg',
     'Тихая зона офиса с рабочими столами'),
]

FAQ = [
    ('Сколько стоит организация новогоднего корпоратива?',
     'От 500 000 ₽. Итог зависит от числа гостей, площадки, программы и техники. После брифа '
     'бесплатно готовим концепцию с предварительной сметой.'),
    ('Когда нужно бронировать новогодний корпоратив?',
     'Лучше в октябре. Залы на вторую половину декабря разбирают раньше всего, а на контент и '
     'оформление нужно 4–8 недель. Если времени меньше, тоже берёмся: часть проектов мы '
     'запускали за две недели.'),
    ('Можно ли провести корпоратив у нас в офисе?',
     'Да. Новый год Messe Düsseldorf мы провели прямо в офисе компании: без сверления стен, '
     'с оформлением на стойках и в проёмах, а наутро офис снова работал.'),
    ('Делаете ли вы подарки сотрудникам и клиентам?',
     'Да. Разрабатываем и производим наборы в фирменном стиле, как новогодний набор с календарём '
     'для Центральной дирекции РЖД.'),
    ('Можно ли заказать только мультимедиа для вечера?',
     'Да. Проекции, экраны и интерактивные зоны делаем и отдельно от организации праздника, '
     'от 150 000 ₽.'),
]

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px;" alt="" /></div></noscript>'
           '<!-- /Yandex.Metrika counter -->')


CSS = """<style>
.ny{--a:#C12164;font-family:'Montserrat',Arial,sans-serif;color:#14171C;background:#fff}
.ny__in{max-width:1180px;margin:0 auto;padding:0 40px}
.ny-sec{padding:clamp(48px,6vw,84px) 0}
.ny-sec__h{margin:0 0 10px;font-size:clamp(26px,3.1vw,40px);font-weight:800;letter-spacing:-.02em;line-height:1.1}
.ny-sec__lead{margin:0 0 30px;max-width:72ch;font-size:16.5px;line-height:1.65;color:#5A616A}
.ny-hero{position:relative;min-height:clamp(420px,62vh,620px);display:flex;align-items:flex-end;color:#fff;overflow:hidden}
.ny-hero__img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ny-hero__sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,12,18,.25),rgba(10,12,18,.88))}
.ny-hero__in{position:relative;width:100%;max-width:1180px;margin:0 auto;padding:0 40px clamp(38px,5vw,64px)}
.ny-hero__k{margin:0 0 14px;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#FFD9E7}
.ny-hero h1{margin:0;font-size:clamp(30px,4.4vw,58px);font-weight:800;letter-spacing:-.025em;line-height:1.05;max-width:20ch}
.ny-hero__lead{margin:18px 0 0;max-width:62ch;font-size:clamp(15.5px,1.5vw,18px);line-height:1.6;color:rgba(255,255,255,.88)}
.ny-hero__f{display:flex;flex-wrap:wrap;gap:10px;margin:26px 0 0;padding:0;list-style:none}
.ny-hero__f li{border:1px solid rgba(255,255,255,.35);border-radius:30px;padding:9px 18px;font-size:14px;font-weight:600}
.ny-hero__cta{display:inline-block;margin-top:26px;background:#FCB724;color:#14171C;font-weight:800;font-size:15.5px;padding:15px 34px;border-radius:30px;text-decoration:none}
.ny-prj{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.ny-prj__c{display:flex;flex-direction:column;border:1px solid rgba(20,23,28,.1);border-radius:20px;overflow:hidden;text-decoration:none;color:inherit;background:#fff;transition:transform .2s ease}
.ny-prj__c:hover{transform:translateY(-4px)}
.ny-prj__c img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.ny-prj__b{padding:20px 22px 24px;display:flex;flex-direction:column;gap:8px;flex:1}
.ny-prj__k{font-size:12px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--a)}
.ny-prj__t{font-size:19px;font-weight:800;letter-spacing:-.01em}
.ny-prj__d{font-size:14.5px;line-height:1.6;color:#5A616A}
.ny-prj__go{margin-top:auto;font-size:14px;font-weight:700;color:var(--a)}
.ny-works{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.ny-work{border-top:2px solid var(--a);padding:14px 0 0}
.ny-work b{display:block;font-size:15.5px;margin-bottom:6px}
.ny-work span{font-size:14px;line-height:1.55;color:#5A616A}
.ny-ideas{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.ny-idea img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px;display:block}
.ny-idea b{display:block;margin:14px 0 6px;font-size:16.5px;letter-spacing:-.01em}
.ny-idea span{font-size:14.5px;line-height:1.6;color:#5A616A}
.ny-cd{background:#14171C;color:#fff}
.ny-cd .ny-sec__lead{color:rgba(255,255,255,.72)}
.ny-cd__track{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(240px,1fr);gap:18px;overflow-x:auto;padding-bottom:10px;scroll-snap-type:x mandatory}
.ny-cd__c{scroll-snap-align:start;border:1px solid rgba(255,255,255,.16);border-radius:18px;padding:20px 20px 22px;background:rgba(255,255,255,.04);display:flex;flex-direction:column;gap:10px}
.ny-cd__n{display:flex;align-items:baseline;gap:8px;color:var(--a)}
.ny-cd__n b{font-size:clamp(34px,4vw,46px);font-weight:800;letter-spacing:-.03em;line-height:1}
.ny-cd__n span{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:rgba(255,255,255,.6)}
.ny-cd__t{font-size:17px;font-weight:700}
.ny-cd__d{font-size:14.5px;line-height:1.6;color:rgba(255,255,255,.72)}
.ny-cd__c img{width:100%;height:150px;flex:none;align-self:stretch;object-fit:cover;border-radius:12px;margin-top:auto}
.ny-cd__note{margin:22px 0 0;font-size:14px;color:rgba(255,255,255,.6)}
.ny-faq{display:grid;gap:10px;max-width:860px}
.ny-faq__i{border:1px solid rgba(20,23,28,.1);border-radius:14px;padding:0 20px}
.ny-faq__i summary{cursor:pointer;list-style:none;position:relative;padding:16px 36px 16px 0;font-size:15.5px;font-weight:700}
.ny-faq__i summary::-webkit-details-marker{display:none}
.ny-faq__i summary::after{content:"";position:absolute;right:2px;top:50%;width:11px;height:11px;transform:translateY(-70%) rotate(45deg);border-right:2.5px solid var(--a);border-bottom:2.5px solid var(--a);transition:transform .2s}
.ny-faq__i[open] summary::after{transform:translateY(-30%) rotate(225deg)}
.ny-faq__i p{margin:0 0 16px;font-size:14.5px;line-height:1.65;color:#5A616A}
.ny-crumbs{font-size:13px;color:#8A9099;padding:18px 0 0}
.ny-crumbs a{color:#8A9099;text-decoration:none}
.ny-crumbs a:hover{text-decoration:underline}
@media(max-width:980px){.ny-prj,.ny-ideas{grid-template-columns:repeat(2,minmax(0,1fr))}.ny-works{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){.ny__in,.ny-hero__in{padding-left:18px;padding-right:18px}.ny-prj,.ny-ideas,.ny-works{grid-template-columns:minmax(0,1fr)}}
</style>"""


def esc(s):
    return H.escape(s, quote=False)


def hero():
    return (
        '<section class="ny-hero">'
        f'<img class="ny-hero__img" src="{IMG}/samsung/hall-wide.jpg" '
        'alt="Новогодний корпоратив Samsung: зал под панорамной проекцией зимнего леса" '
        'fetchpriority="high" decoding="async">'
        '<span class="ny-hero__sh" aria-hidden="true"></span>'
        '<div class="ny-hero__in">'
        '<p class="ny-hero__k">Event · Новый год 2027</p>'
        '<h1>Организация новогоднего корпоратива в Москве под ключ</h1>'
        '<p class="ny-hero__lead">Для Samsung мы превратили банкетный зал в зимний лес из проекций, '
        'для Messe Düsseldorf на один вечер пересобрали собственный офис компании. Берём на себя '
        'концепцию, площадку, оформление, программу, технику и подарки.</p>'
        '<ul class="ny-hero__f"><li>от 500 000 ₽</li><li>за 4–8 недель до даты</li>'
        '<li>Москва и выезд</li></ul>'
        '<a class="ny-hero__cta" href="#lead">Обсудить вечер</a>'
        '</div></section>')


def crumbs():
    return ('<div class="ny__in"><nav class="ny-crumbs" aria-label="Навигация по разделам">'
            '<a href="/">Главная</a> · <a href="/event/">Организация мероприятий</a> · '
            'Новогодний корпоратив</nav></div>')


def projects():
    cards = ''.join(
        f'<a class="ny-prj__c" href="{href}">'
        f'<img src="{img}" alt="{esc(alt)}" loading="lazy" width="800" height="500">'
        f'<span class="ny-prj__b"><span class="ny-prj__k">{esc(kick)}</span>'
        f'<span class="ny-prj__t">{esc(title)}</span>'
        f'<span class="ny-prj__d">{esc(text)}</span>'
        f'<span class="ny-prj__go">Смотреть кейс →</span></span></a>'
        for href, img, kick, title, text, alt in PROJECTS)
    return (f'<section class="ny-sec"><div class="ny__in">'
            f'<h2 class="ny-sec__h">Три новогодних проекта</h2>'
            f'<p class="ny-sec__lead">Мы показываем только то, что делали сами. '
            f'Два новогодних вечера и подарочный набор, который компания вручила сотрудникам '
            f'и клиентам.</p>'
            f'<div class="ny-prj">{cards}</div></div></section>')


def works():
    items = ''.join(f'<div class="ny-work"><b>{esc(t)}</b><span>{esc(d)}</span></div>'
                    for t, d in WORKS)
    return (f'<section class="ny-sec"><div class="ny__in">'
            f'<h2 class="ny-sec__h">Что берём на себя</h2>'
            f'<p class="ny-sec__lead">Вечер ведёт одна команда: от идеи до вывоза оборудования '
            f'наутро. Съёмку делаем своими операторами, технику подбираем под площадку '
            f'и отвечаем за монтаж.</p>'
            f'<div class="ny-works">{items}</div></div></section>')


def ideas():
    cards = ''.join(
        f'<figure class="ny-idea"><img src="{img}" alt="{esc(alt)}" loading="lazy" '
        f'width="800" height="600"><figcaption><b>{esc(t)}</b><span>{esc(d)}</span></figcaption></figure>'
        for img, t, d, alt in IDEAS)
    return (f'<section class="ny-sec"><div class="ny__in">'
            f'<h2 class="ny-sec__h">Идеи с наших вечеров</h2>'
            f'<p class="ny-sec__lead">Эти приёмы уже работали на реальных площадках, поэтому их '
            f'можно взять в свой сценарий и посчитать в смете.</p>'
            f'<div class="ny-ideas">{cards}</div></div></section>')


def countdown():
    cards = ''
    for n, unit, t, d, img, alt in COUNTDOWN:
        pic = (f'<img src="{img}" alt="{esc(alt)}" loading="lazy" width="800" height="500">'
               if img else '')
        cards += (f'<article class="ny-cd__c"><p class="ny-cd__n"><b>{n}</b><span>{esc(unit)}</span></p>'
                  f'<p class="ny-cd__t">{esc(t)}</p><p class="ny-cd__d">{esc(d)}</p>{pic}</article>')
    return (f'<section class="ny-sec ny-cd"><div class="ny__in">'
            f'<h2 class="ny-sec__h">Обратный отсчёт до вечера</h2>'
            f'<p class="ny-sec__lead">Сколько времени занимает подготовка и что происходит '
            f'на каждом шаге. Лента листается вбок.</p>'
            f'<div class="ny-cd__track">{cards}</div>'
            f'<p class="ny-cd__note">Обычно начинаем за 4–8 недель. Если времени меньше, '
            f'тоже берёмся: часть проектов мы запускали за две недели.</p></div></section>')


def price():
    return (f'<section class="ny-sec"><div class="ny__in">'
            f'<h2 class="ny-sec__h">Стоимость и отзыв</h2>{cb.render("ny")}</div></section>')


def faq():
    items = ''.join(f'<details class="ny-faq__i"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
                    for q, a in FAQ)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage',
          'mainEntity': [{'@type': 'Question', 'name': q,
                          'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    return (f'<section class="ny-sec"><div class="ny__in">'
            f'<h2 class="ny-sec__h">Вопросы о новогоднем корпоративе</h2>'
            f'<div class="ny-faq">{items}</div>'
            f'<script type="application/ld+json">'
            f'{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>'
            f'</div></section>')


HEAD = (
    '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    f'<title>{TITLE}</title>'
    f'<meta name="description" content="{H.escape(DESCR)}">'
    f'<link rel="canonical" href="{URL}">'
    '<meta name="robots" content="index, follow">'
    '<meta property="og:type" content="website">'
    f'<meta property="og:title" content="{H.escape(TITLE)}">'
    f'<meta property="og:description" content="{H.escape(DESCR)}">'
    f'<meta property="og:url" content="{URL}">'
    f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/samsung/hall-wide.jpg">'
    + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    body = (f'{rc.header()}<main class="ny">{hero()}{crumbs()}{projects()}{works()}'
            f'{ideas()}{countdown()}{price()}{faq()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'event', 'novogodniy-korporativ')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
