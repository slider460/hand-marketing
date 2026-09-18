#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO-секция на /event: текст об услуге (ивент-агентство, организация корпоративных
мероприятий под ключ), направления с привязкой к реальным кейсам, процесс, FAQ
со schema.org. Вставляется СВОЕЙ секцией перед записью формы (rec237885363) —
Tilda Zero-блоки и их запечённая геометрия не трогаются.
Идемпотентен (маркер ev-seo). Патчит mirror/event/index-a2.html и index.html.
Семантика: «ивент агентство» (837 точных), «организация корпоративных
мероприятий» (97), «под ключ» (53), «агентство по организации мероприятий» (71).
"""
import os, json

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'mirror')
MARK = 'ev-seo'
ANCHOR = '<div id="rec237885363"'

FAQ = [
    ('Какие мероприятия организует ивент-агентство Hand Marketing?',
     'Корпоративные мероприятия и праздники, презентации брендов и продуктов, деловые форумы и MICE-события, вечера для арендаторов торговых центров, кросс-мероприятия с медиа, мультимедийные шоу и 3D-маппинг. По масштабу от Нового года в офисе Messe Düsseldorf до 3D-шоу на площади Ленина в Ставрополе, куда пришли больше 25 000 человек.'),
    ('Сколько стоит организация мероприятия под ключ?',
     'Мероприятие под ключ стоит от 500 000 ₽, мультимедийная зона от 150 000 ₽. Итог зависит от формата, площадки, числа гостей и техники. После брифа бесплатно готовим концепцию с предварительной сметой. Оставьте заявку, и мы перезвоним в течение рабочего дня.'),
    ('Вы работаете только в Москве?',
     'Нет. Офис в Москве, а мероприятия проводим и в других городах и странах: 3D-шоу для администрации Ставрополя, партнёрская конференция Eaton в Алматы.'),
    ('Можно ли заказать только техническое обеспечение: свет, звук, экраны?',
     'Да. Свет, звук, экраны и проекторы ставим вместе с постоянными техническими партнёрами, с которыми работаем годами. Берём и полное техническое сопровождение чужих мероприятий.'),
    ('За сколько времени лучше обращаться?',
     'Лучше всего за 4–8 недель до даты, тогда концепцию, площадку и продакшн успеем проработать без спешки. Но умеем и быстро: часть наших проектов запускалась за две недели.'),
]

def faq_block():
    items, ld = '', []
    for q, a in FAQ:
        items += f'<details class="ev-faq__i"><summary>{q}</summary><p>{a}</p></details>'
        ld.append({'@type': 'Question', 'name': q,
                   'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    schema = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': ld}, ensure_ascii=False)
    return items, schema

def build_section():
    faq_items, schema = faq_block()
    return f'''<!-- {MARK}: SEO-секция услуги (вставка, Zero-блоки не тронуты) -->
<style id="ev-seo-css">
.ev-seo{{font-family:'Montserrat',-apple-system,Arial,sans-serif;color:#14171C;background:#fff;padding:72px 0 64px}}
.ev-in{{max-width:1180px;margin:0 auto;padding:0 40px}}
.ev-h2{{margin:0 0 14px;font-size:clamp(26px,3vw,38px);font-weight:800;letter-spacing:-.02em;line-height:1.1}}
.ev-lead{{margin:0 0 36px;max-width:70ch;font-size:16.5px;line-height:1.65;color:#5A616A}}
.ev-h3{{margin:44px 0 18px;font-size:clamp(20px,2.3vw,26px);font-weight:800;letter-spacing:-.015em}}
.ev-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.ev-card{{border:1px solid rgba(20,23,28,.1);border-radius:16px;padding:18px 20px}}
.ev-card h4{{margin:0 0 8px;font-size:15.5px;font-weight:800;line-height:1.35}}
.ev-card p{{margin:0;font-size:13.5px;line-height:1.55;color:#5A616A}}
.ev-card i{{display:block;width:34px;height:4px;border-radius:2px;margin-bottom:12px}}
.ev-steps{{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;counter-reset:ev}}
.ev-step{{counter-increment:ev;border-top:2px solid #96C223;padding-top:12px}}
.ev-step::before{{content:"0" counter(ev);font-weight:800;font-size:13px;color:#96C223;letter-spacing:.08em}}
.ev-step h4{{margin:6px 0 6px;font-size:14.5px;font-weight:700;line-height:1.35}}
.ev-step p{{margin:0;font-size:13px;line-height:1.5;color:#5A616A}}
.ev-why{{max-width:74ch;font-size:15.5px;line-height:1.7;color:#3d434b}}
.ev-why a{{color:#673A7E;font-weight:600}}
.ev-faq{{display:grid;gap:10px;max-width:820px}}
.ev-faq__i{{border:1px solid rgba(20,23,28,.1);border-radius:14px;background:#fff;padding:0 20px}}
.ev-faq__i summary{{cursor:pointer;list-style:none;position:relative;padding:15px 36px 15px 0;font-size:15.5px;font-weight:700}}
.ev-faq__i summary::-webkit-details-marker{{display:none}}
.ev-faq__i summary::after{{content:"";position:absolute;right:2px;top:50%;width:11px;height:11px;transform:translateY(-70%) rotate(45deg);border-right:2.5px solid #96C223;border-bottom:2.5px solid #96C223;transition:transform .2s}}
.ev-faq__i[open] summary::after{{transform:translateY(-30%) rotate(225deg)}}
.ev-faq__i p{{margin:0 0 16px;font-size:14.5px;line-height:1.65;color:#5A616A}}
@media(max-width:960px){{.ev-grid{{grid-template-columns:1fr 1fr}}.ev-steps{{grid-template-columns:1fr 1fr}}}}
@media(max-width:640px){{.ev-in{{padding:0 20px}}.ev-grid,.ev-steps{{grid-template-columns:1fr}}.ev-seo{{padding:48px 0 40px}}}}
</style>
<section class="ev-seo" aria-label="Об услуге организации мероприятий">
<div class="ev-in">
<h2 class="ev-h2">Одна команда вместо пяти подрядчиков</h2>
<p class="ev-lead">Hand Marketing работает как ивент-агентство полного цикла: свой видеопродакшн и 3D-контент, застройка площадок и техника постоянных партнёров, с которыми мы работаем годами. Поэтому организацию корпоративных мероприятий не приходится делить между подрядчиками. Концепцию, сценарий, продакшн, технику и проведение ведёт одна команда. Работаем в Москве и по всей России с 2012 года.</p>

<h3 class="ev-h3">Что мы организуем</h3>
<div class="ev-grid">
<div class="ev-card"><i style="background:#96C223"></i><h4>Презентации брендов и продуктов</h4><p>Запуски и премьеры. Changan CS35 мы неделю показывали в атриуме ТРЦ «Июнь», а в дилерском центре сделали для него трёхминутное световое шоу на кузове.</p></div>
<div class="ev-card"><i style="background:#673A7E"></i><h4>Корпоративные мероприятия</h4><p>Праздники, юбилеи и <a href="/event/novogodniy-korporativ/">новогодние корпоративы</a>. Новый год Samsung 2020 собрали из проекций с зимним лесом по дуге зала, Новый год Messe Düsseldorf провели прямо в офисе компании.</p></div>
<div class="ev-card"><i style="background:#CF6F19"></i><h4>MICE и деловые события</h4><p>Форумы, конференции и партнёрские программы. Для Eaton провели партнёрскую конференцию в Алматы, а в 2020 году семь часов транслировали выступление компании на онлайн-форуме OCS «IT-ОСЬ 2020».</p></div>
<div class="ev-card"><i style="background:#C12164"></i><h4>События для торговых центров</h4><p>Вечера для арендаторов: «Внутри стихии» на стройке ТРЦ «Ривьера», презентация МФК «Саларис» на 200 гостей, «Пора выходить на свет» в ТЦ «Мозаика».</p></div>
<div class="ev-card"><i style="background:#5E9A2E"></i><h4>Кросс-мероприятия с медиа</h4><p>Совместные проекты с изданиями и партнёрами. Серию кросс-мероприятий Marie Claire в 2011–2013 годах проводили в ГУМе, «Европейском», «Атриуме» и «Метрополисе».</p></div>
<div class="ev-card"><i style="background:#7E3FA0"></i><h4>Мультимедийные шоу</h4><p>3D-маппинг, кинетические инсталляции и проекционные шоу как самостоятельное событие или часть программы.</p></div>
</div>

<h3 class="ev-h3">Как мы работаем</h3>
<div class="ev-steps">
<div class="ev-step"><h4>Бриф и концепция</h4><p>Цели, аудитория, площадка. Креативную идею и предварительную смету готовим бесплатно.</p></div>
<div class="ev-step"><h4>Сценарий и режиссура</h4><p>Тайминг, механики вовлечения, ведущие и артисты.</p></div>
<div class="ev-step"><h4>Продакшн</h4><p>Декорации, застройку, брендинг и печать делаем на своём производстве.</p></div>
<div class="ev-step"><h4>Мультимедиа</h4><p>Экраны, проекции, контент и интерактив из собственного парка техники.</p></div>
<div class="ev-step"><h4>Проведение</h4><p>Монтаж, шоу-контроль, фото- и видеоотчёт после события.</p></div>
</div>

<h3 class="ev-h3">Почему выбирают нас</h3>
<p class="ev-why">Контент мы не заказываем на стороне. У нас свой <a href="/videoproduction">видеопродакшн</a>, мы сами делаем <a href="/content">мультимедийный контент и интерактивные инсталляции</a> и <a href="/exhibition">застраиваем площадки и выставочные стенды</a>. Технику ставят постоянные партнёры, с которыми мы работаем годами, поэтому на площадке нет случайных подрядчиков. Для заказчика это один договор.</p>

<h3 class="ev-h3">Вопросы об организации мероприятий</h3>
<div class="ev-faq">{faq_items}</div>
</div>
<script type="application/ld+json">{schema}</script>
</section>
'''

patched = 0
for name in ('index-a2.html', 'index.html'):
    path = os.path.join(ROOT, 'event', name)
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8') as f:
        h = f.read()
    if MARK in h:
        print(f'{name}: уже пропатчен')
        continue
    if ANCHOR not in h:
        print(f'{name}: якорь формы не найден — пропуск')
        continue
    h = h.replace(ANCHOR, build_section() + ANCHOR, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(h)
    patched += 1
    print(f'{name}: секция вставлена перед формой')
print('Готово:', patched)
