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
import hm_ds as ds  # noqa: E402

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
    lede = ('Площадка, логистика участников, зал, программа и трансляция. Вы готовите доклады, '
            'остальное берём на себя: так мы провели партнёрскую конференцию Eaton в Алматы на 100 человек.')
    return ds.hero('Event', 'Event · Конференции', 'Организация конференций под ключ', esc(lede),
                   chips=('от 500 000 ₽', '100 участников в Алматы', 'эфир 7 часов без сбоев'),
                   ctas=(('Обсудить конференцию', '#lead', 'y'),
                         ('Разбор конференции Eaton', '/event/eaton/', 'o')), figs=0)


def banner():
    href, img, title, text, alt = CASES[0]
    return ds.banner(href, img, 'Партнёрская конференция Eaton в Алматы: зал во время доклада',
                     'Алматы · Eaton', 'Партнёрская конференция Eaton', text,
                     chips=('100 участников', 'трое суток'))


def crumbs():
    return ds.crumbs([('Главная', '/'), ('Организация мероприятий', '/event/'), ('Конференции', None)])


def tasks():
    return ds.sec(ds.feats([(t, esc(d)) for t, d in TASKS], cols=3), 'Что берём на себя',
                  esc('Конференция в другом городе это не только зал и сцена. Участника нужно довезти, '
                      'поселить, накормить и ни разу не оставить без ответа на вопрос.'),
                  icons=3, top=True)


def split():
    rows = ''.join(
        f'<div role="row"><span role="cell">{esc(text)}</span>'
        f'<i role="cell">{"●" if side == "client" else ""}</i><i role="cell">{"●" if side == "us" else ""}</i></div>'
        for text, side in SPLIT)
    ours = sum(1 for _t, s in SPLIT if s == 'us')
    table = (f'<div class="hd-duty" role="table" aria-label="Распределение задач на конференции Eaton">'
             f'<div class="hd-duty__h" role="row"><span role="columnheader">Задача</span>'
             f'<i role="columnheader">Eaton</i><i role="columnheader">Hand Marketing</i></div>{rows}</div>'
             f'<p class="hd-note" style="font-size:16px"><b style="font-size:40px;font-weight:800;color:var(--a);'
             f'margin-right:10px">{ours} из {len(SPLIT)}</b>задач конференции были на нас. '
             f'<a href="/event/eaton/">Разбор конференции</a></p>')
    return ds.sec(table, 'Кто за что отвечал на конференции Eaton',
                  esc('Список задач из нашего кейса, без округлений. Eaton готовил выступления, мы всё, '
                      'что вокруг них: от брони отеля до выезда в аэропорт.'), alt=True)


def online():
    pic = (f'<img src="{EO}/shift-desk.jpg" alt="Аппаратная онлайн-трансляции Eaton в офисе заказчика" '
           f'loading="lazy" width="1200" height="750" style="display:block;width:100%;aspect-ratio:16/10;object-fit:cover">')
    facts = ds.nums([('7 часов', 'эфир с 10:30 до 17:30 без сбоев'),
                     ('2 камеры', 'мини-ПТС и vMix'),
                     ('2 канала', 'независимого мобильного интернета с автопереключением')], cols=3)
    right = (facts + '<p class="hd-note"><a href="/eaton_online/">Как была устроена трансляция</a></p>')
    return ds.band(ds.split(pic, right, ' hd-split--c'), 'Если участники не могут приехать',
                   esc('Выступление Eaton на онлайн-форуме OCS Distribution «IT-ОСЬ 2020» мы вели '
                       'из офиса заказчика.'), kicker='Онлайн и трансляция', dark=True, fig='h')


def cases():
    items = [(href, title, text, img) for href, img, title, text, alt in CASES]
    return ds.sec(ds.cases(items, cols=3), 'Конференции и деловые события',
                  'Конференция для партнёров и вечера для арендаторов торговых центров. Везде одна '
                  'задача: собрать деловую аудиторию и провести её по программе без сбоев. Другие '
                  'форматы собраны на странице <a href="/event/">организации мероприятий</a>.', icons=3,
                  icon_start=4)


def steps():
    return ds.band(ds.steps([(t, esc(d)) for t, d in STEPS], cols=5), 'Как готовим конференцию',
                   fig='blocks')


def price():
    return ds.sec(ds.cost('conf'), 'Стоимость и отзывы')


def faq():
    return ds.sec(ds.faq(FAQ), 'Вопросы об организации конференций', alt=True)


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
    + rc.FONT + rc.CSS + ds.CSS + METRIKA + '</head><body>')


def page():
    body = (f'{rc.header()}<main class="hd" style="--a:{ds.EV}">{crumbs()}{hero()}{banner()}{tasks()}'
            f'{split()}{online()}{cases()}{steps()}{price()}{faq()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'event', 'konferencii')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
