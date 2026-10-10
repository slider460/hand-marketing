#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/team/index.html: страница «Команда».

Зачем: у половины агентств из топ-10 Яндекса команда показана лицами, у нас
она была только каруселью на главной, где имена и должности вшиты в картинки,
то есть невидимы ни поиску, ни скринридеру.

Портреты вырезаны из тех же плашек главной (круг слева) скриптом, который
живёт в шапке этого файла, имена и должности перенесены текстом.

Про каждого пишем только то, что следует из должности и из проектов агентства.
Ничего личного и никаких выдуманных биографий: сведений о людях у нас нет.

Как пересобрать портреты, если плашки на главной обновятся:
    python3 -c "import re,os;from PIL import Image; ..."  см. историю коммита,
    кроп круга на макете 834x417 это (54, 68, 336, 350).

Правки: ТОЛЬКО через этот скрипт.
Прогон: python3 scripts/a2/finalize_page.py gen_team.py
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

URL = 'https://hand-marketing.ru/team/'

# (файл портрета, имя, должность, за что отвечает в проекте)
TEAM = [
    ('narodetskiy', 'Народецкий Александр', 'Client Service Director / CEO',
     'Отвечает за работу с заказчиком: от первого разговора и сметы до сдачи проекта. '
     'К нему приходят задачи, которые ещё не разложены на услуги.'),
    ('semenov', 'Семенов Эдвард', 'Commercial Director',
     'Коммерческие условия, договоры и экономика проектов. Считает, во что обойдётся '
     'работа и как уложиться в бюджет заказчика.'),
    ('klichanovskiy', 'Сергей Кличановский', 'Business Development Director',
     'Развитие направлений и новые клиенты. Занимается тендерами и большими '
     'многоэтапными проектами вроде выставочных стендов.'),
    ('dementyev', 'Дементьев Святослав', 'Chief Creative Officer',
     'Идеи и визуальный язык проектов: концепции мероприятий, фирменные стили, '
     'сценарии роликов и контент для мультимедийных зон.'),
    ('osotov', 'Осотов Алексей', 'Chief Information Officer',
     'Отвечает за цифровую часть: сайты и посадочные страницы, аналитику, '
     'внутренние системы агентства.'),
    ('agafonova', 'Агафонова Илона', 'Senior Account Manager',
     'Ведёт проекты по шагам: график, подрядчики, согласования и сроки. '
     'Тот человек, который отвечает на вопрос «на каком мы этапе».'),
    ('muratov', 'Муратов Денис', 'Technical Director',
     'Техническая часть площадок и съёмок: свет, звук, экраны и проекции, '
     'расчёт схем размещения, монтаж и работа на объекте.'),
]

# как роли складываются в проект
FLOW = [
    ('Задача', 'Разговор с клиент-сервисом: что нужно получить, к какому сроку '
     'и в каких деньгах.'),
    ('Идея и смета', 'Креативный директор предлагает решение, коммерческий считает '
     'смету. Обе части приходят к заказчику вместе.'),
    ('Производство', 'Съёмку, дизайн и контент делает наша команда, за печать и застройку отвечаем сами. '
     'Аккаунт держит график и согласования.'),
    ('Площадка', 'Технический директор ведёт монтаж и работу на объекте: свет, '
     'звук, экраны, проекции.'),
    ('Сдача', 'Материалы, исходники и отчётность передаём заказчику. '
     'Дальше обычно начинается следующий проект.'),
]

FACTS = [
    ('с 2012', 'года агентство работает под этим именем'),
    ('7', 'человек в постоянной команде, остальных собираем под проект'),
    ('10', 'направлений, от съёмки до застройки стендов'),
]

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px" alt=""></div></noscript>')



def esc(t):
    return H.escape(t, quote=False)


# круглые портреты с кольцом, как в блоке команды на главной; цвет кольца у каждого свой
RING = (ds.VIOLET, '#FCB724', ds.CON, ds.CRE, ds.DIG, ds.PHO, ds.EV)

CSS = """<style id="tm-css">
.tm-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:56px 36px}
.tm-card{text-align:center}
.tm-card img{display:block;width:170px;height:170px;margin:0 auto;border-radius:50%;object-fit:cover;box-shadow:0 0 0 6px #fff,0 0 0 8px var(--c)}
.tm-card h3{margin:24px 0 0;font-size:19px;font-weight:700;line-height:1.3;color:#111}
.tm-card .role{display:block;margin-top:6px;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--c)}
.tm-card p{margin:12px auto 0;max-width:30ch;font-size:14.5px;line-height:1.6;color:#4C4C4C}
.tm-more{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;background:#F6F4F9;padding:32px 26px}
.tm-more img{width:64px;height:64px}
.tm-more b{margin-top:18px;font-size:17px;line-height:1.4;color:#111}
.tm-more p{margin:10px 0 0;font-size:14.5px;line-height:1.6;color:#4C4C4C}
@media(max-width:980px){.tm-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.tm-grid{grid-template-columns:minmax(0,1fr);gap:44px}}
</style>"""


def page():
    cards = ''.join(
        f'<article class="tm-card" style="--c:{RING[i]}">'
        f'<img src="/images/team/{slug}.jpg" alt="{H.escape(name)}, {H.escape(role)}" '
        f'loading="lazy" width="264" height="264">'
        f'<h3>{esc(name)}</h3><span class="role">{esc(role)}</span><p>{esc(about)}</p>'
        f'</article>' for i, (slug, name, role, about) in enumerate(TEAM))
    cards += (f'<div class="tm-more"><img src="{ds.FIG[7]}" alt="" aria-hidden="true" width="64" height="64">'
              '<b>Под проект собираем группы</b><p>Съёмочные группы, монтажники и промо-персонал. '
              'За результат отвечает кто-то из семерых.</p></div>')

    title = 'Команда агентства Hand Marketing'
    descr = ('Кто делает проекты Hand Marketing: клиент-сервис, коммерческий и креативный '
             'директора, аккаунт, технический директор. Семь человек в постоянной команде '
             'и десять направлений работы.')
    ld = {'@context': 'https://schema.org', '@type': 'Organization',
          'name': 'Hand Marketing', 'url': 'https://hand-marketing.ru/',
          'telephone': '+7 495 580 75 37', 'email': 'info@hand-marketing.ru',
          'employee': [{'@type': 'Person', 'name': name, 'jobTitle': role}
                       for _s, name, role, _a in TEAM]}
    crumbs_ld = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Главная', 'item': 'https://hand-marketing.ru/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Команда', 'item': URL}]}
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))

    lede = ('Проект ведут те же люди, которые его придумали: это семь человек, между которыми поделены '
            'клиент-сервис, коммерция, креатив, продакшн и техническая часть. Под конкретную работу '
            'собираем съёмочные группы, монтажников и промо-персонал, но отвечает за результат всегда '
            'кто-то из этого списка.')
    hero = ds.hero('Team', 'Об агентстве · Команда', 'Команда', esc(lede), figs=1)
    hero = hero.replace('</div></section>', ds.nums(FACTS, cols=3, center=True) + '</div></section>', 1)
    crumbs = ds.crumbs([('Главная', '/'), ('Команда', None)])
    grid = ds.sec(f'<div class="tm-grid">{cards}</div>', 'Кто ведёт ваш проект', icons=3)
    flow = ds.band(ds.steps([(t, esc(d)) for t, d in FLOW], cols=5), 'Как проект проходит через команду',
                   esc('Заказчик общается с одним человеком, но внутри задача проходит через всех, '
                       'кого касается.'), fig='blocks')
    cta = ds.sec('<p class="hd-lead" style="margin:0;font-size:18px;color:#111">Хотите понять, как мы '
                 'работаем на деле, посмотрите <a href="/project">проекты</a> и <a href="/reviews/">письма '
                 'клиентов</a>, а порядок работы и цены описаны на странице <a href="/price/">стоимости</a>.</p>')

    head = (
        '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{title} | Hand Marketing</title>'
        f'<meta name="description" content="{H.escape(descr)}">'
        f'<link rel="canonical" href="{URL}">'
        '<meta name="robots" content="index, follow">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{H.escape(title)}">'
        f'<meta property="og:description" content="{H.escape(descr)}">'
        f'<meta property="og:url" content="{URL}">'
        '<meta property="og:image" content="https://hand-marketing.ru/static/thb/as3230-6663-4363-b038-333866373133/-/resize/504x/__76876-145.png">'
        + rc.FONT + rc.CSS + ds.CSS + CSS + METRIKA + '</head><body>')
    body = (f'{rc.header()}<main class="hd" style="--a:{ds.VIOLET}">{crumbs}{hero}{grid}{flow}{cta}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}'
            f'<script type="application/ld+json">{dump(ld)}</script>'
            f'<script type="application/ld+json">{dump(crumbs_ld)}</script>'
            '</body></html>')
    return head + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'team')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('создано:', p, os.path.getsize(p) // 1024, 'КБ')
