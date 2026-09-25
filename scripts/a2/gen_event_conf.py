#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/event/konferencii/index.html — страницу «Организация конференций под ключ».

Спрос (Вордстат, Москва, 25.09.2026, точная частотность): «организация бизнес конференций» 16,
«организация конференций» 9, «организация конференции под ключ» 8, «проведение конференций» 8.
Широкие 1534 почти целиком научные конференции, туда не целимся.

Ответы владельца 25.09.2026: цена от 500 000 ₽; на партнёрской конференции Eaton в Алматы было
100 участников; других конференций, которые можно показать, НЕТ. Поэтому опора страницы:
Eaton в Алматы (всё, кроме содержания докладов, было на нас), онлайн-эфир Eaton на форуме
OCS «IT-ОСЬ 2020» и два деловых вечера для арендаторов («Саларис», «Мозаика»).
Про технику пишем формулой владельца: подбираем под площадку, привозим, отвечаем за монтаж.

Сигнатурная механика: разделение ответственности на конференции Eaton. Девять задач
разложены по двум колонкам, у заказчика осталась одна.

Правки: ТОЛЬКО через этот скрипт.
Прогон: python3 scripts/a2/finalize_page.py gen_event_conf.py
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

URL = 'https://hand-marketing.ru/event/konferencii/'
TITLE = 'Организация конференций под ключ в Москве | Hand Marketing'
DESCR = ('Организация конференций под ключ: площадка, логистика участников, зал и техника, '
         'программа и трансляция. Конференция Eaton на 100 человек. От 500 000 ₽.')
EA = '/images/eaton-almaty'
EO = '/images/eaton-online'

TASKS = [
    ('Площадка и отель', 'Подбираем площадку и отель под технический райдер, число '
     'участников и дорогу от аэропорта.'),
    ('Логистика участников', 'Перелёты, трансферы, размещение по спискам, сопровождение '
     'VIP-групп.'),
    ('Программа и тайминг', 'Режиссура дня и контроль тайминга: доклады, перерывы, обед '
     'и выезд под обратные рейсы.'),
    ('Зал и техника', 'Сцена, звук, свет, LED и проекция, застройка и брендирование зала. '
     'Технику подбираем под площадку, привозим и отвечаем за монтаж.'),
    ('Материалы участника', 'Бейджи, ленты, навигация, раздатка и гид участника: программа, '
     'отель, рестораны, погода и курс валют.'),
    ('Трансляция и съёмка', 'Онлайн-эфир для тех, кто не приехал, фото и видео с конференции '
     'нашей съёмочной группой.'),
]

# кто за что отвечал на конференции Eaton в Алматы (список «Что было на нас» из кейса)
SPLIT = [
    ('Содержание докладов', 'client'),
    ('Подбор и бронь отеля под технический райдер', 'us'),
    ('Перелёты, трансферы, размещение, VIP-группы', 'us'),
    ('Программа, режиссура и контроль тайминга', 'us'),
    ('Сцена, звук, свет, LED и проекция', 'us'),
    ('Застройка зала и брендирование', 'us'),
    ('Бейджи, ленты, раздатка, навигация', 'us'),
    ('Гид участника: разработка и печать', 'us'),
    ('Сопровождение все три дня, круглосуточно', 'us'),
]

CASES = [
    ('/event/eaton/', f'{EA}/hall-full.jpg', 'Партнёрская конференция Eaton, Алматы',
     '100 участников, трое суток. Перелёт 4 ч 30 мин, отель в 14 км от аэропорта, семь '
     'выступлений за день и гид участника на восемь полос.',
     'Зал партнёрской конференции Eaton в Алматы во время доклада'),
    ('/event/salaris/', '/images/salaris/hall-full.jpg', 'Презентация МФК «Саларис» арендаторам',
     '200 гостей в арт-пространстве «ФотоФактура», 5 апреля 2018. Презентация о транспортном '
     'узле и трафике, фуршет и ролик об объекте.',
     'Гости на презентации МФК «Саларис» для арендаторов'),
    ('/event/mozaika/', '/images/mozaika/hall-blue.jpg', 'Вечер для арендаторов ТЦ «Мозаика»',
     '134 гостя, 31 октября 2018. Зал в синем монохроме и световая панель с логотипом, '
     'которую гости собрали своими лампочками.',
     'Зал вечера для арендаторов ТЦ «Мозаика»'),
]

STEPS = [
    ('Бриф', 'Даты, город, число участников, формат программы и рамки бюджета.'),
    ('Площадка и смета', 'Варианты площадок и отелей, предварительная смета. Бесплатно.'),
    ('Логистика и программа', 'Списки участников, перелёты и трансферы, тайминг дня, материалы.'),
    ('Подготовка зала', 'Застройка, техника и брендирование, проверка площадки до приезда гостей.'),
    ('Конференция и отчёт', 'Работаем на площадке все дни, после сдаём фото и видео.'),
]

FAQ = [
    ('Сколько стоит организация конференции под ключ?',
     'От 500 000 ₽. Итог зависит от числа участников, города, площадки, программы и логистики. '
     'Концепцию и предварительную смету готовим бесплатно после брифа.'),
    ('Организуете конференции в других городах и странах?',
     'Да. Партнёрскую конференцию Eaton провели в Алматы: 100 участников, перелёты, трансферы, '
     'отель, зал и гид участника на восемь полос.'),
    ('Можно ли провести конференцию онлайн или с трансляцией?',
     'Да. Для Eaton вели семичасовой эфир выступления на форуме OCS «IT-ОСЬ 2020» из офиса '
     'заказчика: две камеры, резервный канал связи, эфир без сбоев.'),
    ('За сколько времени начинать подготовку?',
     'Лучше за 4–8 недель до даты. Если нужны перелёты и отель для группы, раньше: номера '
     'и билеты на группу бронируются первыми.'),
    ('Что остаётся на стороне заказчика?',
     'Содержание докладов и список участников. Всё остальное, от брони отеля до выезда '
     'в аэропорт, можем взять на себя.'),
    ('Вы снимаете конференцию?',
     'Да, нашей съёмочной группой: фотоотчёт, ролик о событии и запись выступлений.'),
]

CSS = """<style>
.cf{--a:#C12164;--ink:#14171C;--mut:#5A616A;--line:rgba(20,23,28,.12);--soft:#FBF6F8;
 font-family:'Montserrat',Arial,sans-serif;color:var(--ink);background:#fff}
.cf__in{max-width:1180px;margin:0 auto;padding:0 40px}
.cf-sec{padding:clamp(46px,5.6vw,80px) 0}
.cf-sec__h{margin:0 0 10px;font-size:clamp(26px,3.1vw,40px);font-weight:800;letter-spacing:-.02em;line-height:1.1}
.cf-sec__lead{margin:0 0 30px;max-width:72ch;font-size:16.5px;line-height:1.65;color:var(--mut)}
.cf-sec__lead a{color:var(--a);font-weight:700}
.cf-hero{position:relative;min-height:clamp(400px,58vh,580px);display:flex;align-items:flex-end;color:#fff;overflow:hidden;background:#15121A}
.cf-hero__img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cf-hero__sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,10,16,.25),rgba(14,10,16,.88))}
.cf-hero__in{position:relative;width:100%;max-width:1180px;margin:0 auto;padding:0 40px clamp(34px,4.6vw,60px)}
.cf-hero__k{margin:0 0 14px;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#F2C4D6}
.cf-hero h1{margin:0;font-size:clamp(28px,4.2vw,54px);font-weight:800;letter-spacing:-.025em;line-height:1.06;max-width:16ch}
.cf-hero__lead{margin:18px 0 0;max-width:60ch;font-size:clamp(15.5px,1.5vw,18px);line-height:1.6;color:rgba(255,255,255,.88)}
.cf-hero__f{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 0;padding:0;list-style:none}
.cf-hero__f li{border:1px solid rgba(255,255,255,.35);border-radius:30px;padding:9px 18px;font-size:14px;font-weight:600}
.cf-hero__cta{display:inline-block;margin-top:24px;background:#FCB724;color:#14171C;font-weight:800;font-size:15.5px;padding:15px 34px;border-radius:30px;text-decoration:none}
.cf-crumbs{font-size:13px;color:#8A9099;padding:18px 0 0}
.cf-crumbs a{color:#8A9099;text-decoration:none}
.cf-crumbs a:hover{text-decoration:underline}
.cf-tasks{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.cf-task{border-top:2px solid var(--a);padding:14px 0 0}
.cf-task b{display:block;font-size:16px;margin-bottom:6px}
.cf-task span{font-size:14.5px;line-height:1.55;color:var(--mut)}
/* разделение ответственности: у заказчика одна строка, остальное на нас */
.cf-split{border:1px solid var(--line);border-radius:22px;overflow:hidden;background:#fff}
.cf-split__head,.cf-split__row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.cf-split__head span{padding:16px 22px;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#8A9099;border-bottom:1px solid var(--line)}
.cf-split__head span+span{border-left:1px solid var(--line);color:var(--a)}
.cf-split__row>span{padding:9px 22px;min-height:44px;display:flex;align-items:center}
.cf-split__row>span+span{border-left:1px solid var(--line);background:var(--soft)}
.cf-split__row i{font-style:normal;display:inline-block;border-radius:10px;padding:8px 14px;font-size:14.5px;font-weight:700;line-height:1.35}
.cf-split__row [data-side=client] i{border:1.5px solid var(--ink)}
.cf-split__row [data-side=us] i{background:var(--a);color:#fff}
.cf-split__sum{display:flex;flex-wrap:wrap;gap:8px 24px;align-items:baseline;margin:18px 0 0;font-size:15.5px;color:var(--mut)}
.cf-split__sum b{font-size:clamp(28px,3vw,38px);font-weight:900;color:var(--a);letter-spacing:-.02em}
.cf-online{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(20px,3vw,44px);align-items:center}
.cf-online img{width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;border-radius:18px;display:block}
.cf-online ul{margin:14px 0 0;padding:0;list-style:none;display:grid;gap:10px}
.cf-online li{position:relative;padding-left:20px;font-size:15px;line-height:1.55;color:var(--mut)}
.cf-online li::before{content:"";position:absolute;left:0;top:.5em;width:9px;height:9px;border-radius:3px;background:var(--a)}
.cf-online a{display:inline-block;margin-top:16px;font-size:14.5px;font-weight:700;color:var(--a)}
.cf-cases{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.cf-case{display:flex;flex-direction:column;border:1px solid rgba(20,23,28,.1);border-radius:20px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .2s ease}
.cf-case:hover{transform:translateY(-4px)}
.cf-case img{width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;display:block}
.cf-case__b{padding:18px 20px 22px;display:flex;flex-direction:column;gap:8px;flex:1}
.cf-case__t{font-size:18px;font-weight:800;letter-spacing:-.01em}
.cf-case__d{font-size:14.5px;line-height:1.6;color:var(--mut)}
.cf-case__go{margin-top:auto;font-size:14px;font-weight:700;color:var(--a)}
.cf-steps{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:20px;counter-reset:st}
.cf-step{counter-increment:st;border-top:2px solid var(--a);padding-top:12px}
.cf-step::before{content:"0" counter(st);font-weight:800;font-size:13px;color:var(--a);letter-spacing:.08em}
.cf-step b{display:block;margin:6px 0;font-size:15px}
.cf-step span{font-size:14px;line-height:1.55;color:var(--mut)}
.cf-faq{display:grid;gap:10px;max-width:860px}
.cf-faq__i{border:1px solid rgba(20,23,28,.1);border-radius:14px;padding:0 20px}
.cf-faq__i summary{cursor:pointer;list-style:none;position:relative;padding:16px 36px 16px 0;font-size:15.5px;font-weight:700}
.cf-faq__i summary::-webkit-details-marker{display:none}
.cf-faq__i summary::after{content:"";position:absolute;right:2px;top:50%;width:11px;height:11px;transform:translateY(-70%) rotate(45deg);border-right:2.5px solid var(--a);border-bottom:2.5px solid var(--a);transition:transform .2s}
.cf-faq__i[open] summary::after{transform:translateY(-30%) rotate(225deg)}
.cf-faq__i p{margin:0 0 16px;font-size:14.5px;line-height:1.65;color:var(--mut)}
@media(max-width:980px){.cf-tasks,.cf-cases{grid-template-columns:repeat(2,minmax(0,1fr))}.cf-steps{grid-template-columns:repeat(2,minmax(0,1fr))}.cf-online{grid-template-columns:minmax(0,1fr)}}
@media(max-width:640px){.cf__in,.cf-hero__in{padding-left:18px;padding-right:18px}.cf-tasks,.cf-cases,.cf-steps{grid-template-columns:minmax(0,1fr)}
 .cf-split__head span{padding:12px 12px;font-size:10.5px;letter-spacing:.08em}.cf-split__row>span{padding:7px 10px}.cf-split__row i{font-size:13px;padding:7px 10px}}
</style>"""

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px" alt=""></div></noscript>')


def esc(s):
    return H.escape(s, quote=False)


def hero():
    return (
        '<section class="cf-hero">'
        f'<img class="cf-hero__img" src="{EA}/hall-full.jpg" '
        'alt="Партнёрская конференция Eaton в Алматы: зал во время доклада" '
        'fetchpriority="high" decoding="async">'
        '<span class="cf-hero__sh" aria-hidden="true"></span>'
        '<div class="cf-hero__in">'
        '<p class="cf-hero__k">Event · Конференции</p>'
        '<h1>Организация конференций под ключ</h1>'
        '<p class="cf-hero__lead">Площадка, логистика участников, зал, программа и трансляция. '
        'Вы готовите доклады, остальное берём на себя: так мы провели партнёрскую конференцию '
        'Eaton в Алматы на 100 человек.</p>'
        '<ul class="cf-hero__f"><li>от 500 000 ₽</li><li>100 участников в Алматы</li>'
        '<li>эфир 7 часов без сбоев</li></ul>'
        '<a class="cf-hero__cta" href="#lead">Обсудить конференцию</a>'
        '</div></section>')


def crumbs():
    return ('<div class="cf__in"><nav class="cf-crumbs" aria-label="Навигация по разделам">'
            '<a href="/">Главная</a> · <a href="/event/">Организация мероприятий</a> · '
            'Конференции</nav></div>')


def tasks():
    items = ''.join(f'<div class="cf-task"><b>{esc(t)}</b><span>{esc(d)}</span></div>'
                    for t, d in TASKS)
    return (f'<section class="cf-sec"><div class="cf__in">'
            f'<h2 class="cf-sec__h">Что берём на себя</h2>'
            f'<p class="cf-sec__lead">Конференция в другом городе это не только зал и сцена. '
            f'Участника нужно довезти, поселить, накормить и ни разу не оставить без ответа '
            f'на вопрос.</p>'
            f'<div class="cf-tasks">{items}</div></div></section>')


def split():
    rows = ''
    for text, side in SPLIT:
        cell = f'<i>{esc(text)}</i>'
        left = f'<span data-side="client">{cell}</span>' if side == 'client' else '<span></span>'
        right = f'<span data-side="us">{cell}</span>' if side == 'us' else '<span></span>'
        rows += f'<div class="cf-split__row">{left}{right}</div>'
    ours = sum(1 for _t, s in SPLIT if s == 'us')
    return (f'<section class="cf-sec" style="background:#FAF8F9"><div class="cf__in">'
            f'<h2 class="cf-sec__h">Кто за что отвечал на конференции Eaton</h2>'
            f'<p class="cf-sec__lead">Список задач из нашего кейса, без округлений. Eaton готовил '
            f'выступления, мы всё, что вокруг них: от брони отеля до выезда в аэропорт.</p>'
            f'<div class="cf-split" role="table" aria-label="Распределение задач на конференции Eaton">'
            f'<div class="cf-split__head" role="row"><span role="columnheader">Eaton</span>'
            f'<span role="columnheader">Hand Marketing</span></div>{rows}</div>'
            f'<p class="cf-split__sum"><b>{ours} из {len(SPLIT)}</b>задач конференции были на нас. '
            f'<a href="/event/eaton/" style="color:var(--a);font-weight:700">Разбор конференции →</a></p>'
            f'</div></section>')


def online():
    return (f'<section class="cf-sec"><div class="cf__in"><div class="cf-online">'
            f'<img src="{EO}/shift-desk.jpg" alt="Аппаратная онлайн-трансляции Eaton в офисе заказчика" '
            f'loading="lazy" width="1200" height="750">'
            f'<div><h2 class="cf-sec__h">Если участники не могут приехать</h2>'
            f'<p class="cf-sec__lead" style="margin-bottom:0">Выступление Eaton на онлайн-форуме '
            f'OCS Distribution «IT-ОСЬ 2020» мы вели из офиса заказчика.</p>'
            f'<ul><li>Эфир с 10:30 до 17:30, семь часов без сбоев</li>'
            f'<li>Две камеры, мини-ПТС и vMix</li>'
            f'<li>Два независимых канала мобильного интернета с автопереключением</li></ul>'
            f'<a href="/eaton_online/">Как была устроена трансляция →</a></div>'
            f'</div></div></section>')


def cases():
    cards = ''.join(
        f'<a class="cf-case" href="{href}">'
        f'<img src="{img}" alt="{esc(alt)}" loading="lazy" width="800" height="500">'
        f'<span class="cf-case__b"><span class="cf-case__t">{esc(title)}</span>'
        f'<span class="cf-case__d">{esc(text)}</span>'
        f'<span class="cf-case__go">Смотреть кейс →</span></span></a>'
        for href, img, title, text, alt in CASES)
    return (f'<section class="cf-sec" style="background:#FAF8F9"><div class="cf__in">'
            f'<h2 class="cf-sec__h">Конференции и деловые события</h2>'
            f'<p class="cf-sec__lead">Конференция для партнёров и вечера для арендаторов торговых центров. '
            f'Везде одна задача: собрать деловую аудиторию и провести её по программе без сбоев. '
            f'Другие форматы собраны на странице <a href="/event/">организации мероприятий</a>.</p>'
            f'<div class="cf-cases">{cards}</div></div></section>')


def steps():
    items = ''.join(f'<div class="cf-step"><b>{esc(t)}</b><span>{esc(d)}</span></div>'
                    for t, d in STEPS)
    return (f'<section class="cf-sec"><div class="cf__in">'
            f'<h2 class="cf-sec__h">Как готовим конференцию</h2>'
            f'<div class="cf-steps">{items}</div></div></section>')


def price():
    return (f'<section class="cf-sec" style="background:#FAF8F9"><div class="cf__in">'
            f'<h2 class="cf-sec__h">Стоимость и отзывы</h2>{cb.render("conf")}</div></section>')


def faq():
    items = ''.join(f'<details class="cf-faq__i"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
                    for q, a in FAQ)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage',
          'mainEntity': [{'@type': 'Question', 'name': q,
                          'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    return (f'<section class="cf-sec"><div class="cf__in">'
            f'<h2 class="cf-sec__h">Вопросы об организации конференций</h2>'
            f'<div class="cf-faq">{items}</div>'
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
    f'<meta property="og:image" content="https://hand-marketing.ru{EA}/hall-full.jpg">'
    + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    body = (f'{rc.header()}<main class="cf">{hero()}{crumbs()}{tasks()}{split()}{online()}'
            f'{cases()}{steps()}{price()}{faq()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'event', 'konferencii')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
