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
    ('Производство', 'Съёмка, дизайн, контент и печать внутри агентства. '
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

CSS = """<style id="tm-css">
.tm{--ink:#14171C;--mut:#5A616A;--a:#673A7E;--line:rgba(20,23,28,.12);
 font-family:'Montserrat',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff}
.tm *{box-sizing:border-box}
.tm__wrap{max-width:1180px;margin:0 auto;padding:0 40px}
.tm-hero{padding:64px 0 34px}
.tm-hero h1{margin:0 0 16px;font-size:clamp(28px,4vw,48px);font-weight:800;letter-spacing:-.025em;line-height:1.08}
.tm-hero p{margin:0;max-width:72ch;font-size:16.5px;line-height:1.65;color:var(--mut)}
.tm-facts{display:flex;flex-wrap:wrap;gap:34px;margin-top:26px}
.tm-facts div b{display:block;font-size:30px;font-weight:800;letter-spacing:-.02em;color:var(--a)}
.tm-facts div span{font-size:13.5px;color:var(--mut);max-width:26ch;display:block}
.tm-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px 24px;padding:36px 0 8px}
.tm-card{border:1px solid var(--line);border-radius:20px;padding:24px 24px 26px;background:#fff}
.tm-card img{width:132px;height:132px;border-radius:50%;object-fit:cover;display:block;margin-bottom:16px}
.tm-card h2{margin:0 0 4px;font-size:19px;font-weight:800;letter-spacing:-.01em}
.tm-card .role{display:block;margin-bottom:12px;font-size:13px;font-weight:700;letter-spacing:.06em;
 text-transform:uppercase;color:var(--a)}
.tm-card p{margin:0;font-size:14.5px;line-height:1.6;color:var(--mut)}
.tm-sec{padding:44px 0 0}
.tm-sec h2{margin:0 0 8px;font-size:clamp(22px,2.6vw,30px);font-weight:800;letter-spacing:-.02em}
.tm-sec p.lead{margin:0 0 24px;max-width:74ch;font-size:16px;line-height:1.65;color:var(--mut)}
.tm-flow{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;counter-reset:tm}
.tm-step{counter-increment:tm;border-top:2px solid var(--a);padding-top:12px}
.tm-step::before{content:"0" counter(tm);font-weight:800;font-size:13px;color:var(--a);letter-spacing:.08em}
.tm-step h3{margin:6px 0 6px;font-size:15px;font-weight:700;line-height:1.35}
.tm-step p{margin:0;font-size:13.5px;line-height:1.55;color:var(--mut)}
.tm-cta{margin:42px 0 64px;padding:26px 28px;border-radius:20px;background:#F8F6FA;font-size:16px;line-height:1.6}
.tm-cta a{color:var(--a);font-weight:700}
@media(max-width:1000px){.tm-grid{grid-template-columns:1fr 1fr}.tm-flow{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.tm__wrap{padding:0 18px}.tm-grid,.tm-flow{grid-template-columns:1fr}}
</style>"""


def esc(t):
    return H.escape(t, quote=False)


def page():
    cards = ''.join(
        f'<article class="tm-card">'
        f'<img src="/images/team/{slug}.jpg" alt="{H.escape(name)}, {H.escape(role)}" '
        f'loading="lazy" width="264" height="264">'
        f'<h2>{esc(name)}</h2><span class="role">{esc(role)}</span><p>{esc(about)}</p>'
        f'</article>' for slug, name, role, about in TEAM)
    flow = ''.join(f'<div class="tm-step"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
                   for t, d in FLOW)
    facts = ''.join(f'<div><b>{esc(n)}</b><span>{esc(t)}</span></div>' for n, t in FACTS)

    title = 'Команда агентства Hand Marketing'
    descr = ('Кто делает проекты Hand Marketing: клиент-сервис, коммерческий и креативный '
             'директора, аккаунт, технический директор. Семь человек в постоянной команде '
             'и десять направлений работы.')
    ld = {'@context': 'https://schema.org', '@type': 'Organization',
          'name': 'Hand Marketing', 'url': 'https://hand-marketing.ru/',
          'telephone': '+7 495 580 75 37', 'email': 'info@hand-marketing.ru',
          'employee': [{'@type': 'Person', 'name': name, 'jobTitle': role}
                       for _s, name, role, _a in TEAM]}
    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Главная', 'item': 'https://hand-marketing.ru/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Команда', 'item': URL}]}
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))

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
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')

    body = (
        f'{rc.header()}<main class="tm">'
        '<section class="tm-hero"><div class="tm__wrap">'
        '<h1>Команда</h1>'
        '<p>Проект ведут те же люди, которые его придумали: это семь человек, между '
        'которыми поделены клиент-сервис, коммерция, креатив, продакшн и техническая '
        'часть. Под конкретную работу собираем съёмочные группы, монтажников и '
        'промо-персонал, но отвечает за результат всегда кто-то из этого списка.</p>'
        f'<div class="tm-facts">{facts}</div>'
        '</div></section>'
        f'<div class="tm__wrap"><div class="tm-grid">{cards}</div>'
        '<section class="tm-sec"><h2>Как проект проходит через команду</h2>'
        '<p class="lead">Заказчик общается с одним человеком, но внутри задача проходит '
        'через всех, кого касается.</p>'
        f'<div class="tm-flow">{flow}</div></section>'
        '<p class="tm-cta">Хотите понять, как мы работаем на деле, посмотрите '
        '<a href="/project">проекты</a> и <a href="/reviews/">письма клиентов</a>, '
        'а порядок работы и цены описаны на странице <a href="/price/">стоимости</a>.</p>'
        '</div></main>'
        f'<a id="lead"></a>{rc.footer()}{rc.JS}'
        f'<script type="application/ld+json">{dump(ld)}</script>'
        f'<script type="application/ld+json">{dump(crumbs)}</script>'
        '</body></html>')
    return head + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'team')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('создано:', p, os.path.getsize(p) // 1024, 'КБ')
