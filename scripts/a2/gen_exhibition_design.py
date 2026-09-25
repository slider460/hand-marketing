#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/exhibition/dizayn-stenda/index.html — страницу «Дизайн и проектирование
выставочных стендов».

Зачем отдельно от /exhibition: у дизайна свой спрос. Вордстат, Москва, 25.09.2026, точная
частотность (фраза в кавычках): «дизайн выставочного стенда» 71, «проектирование выставочных
стендов» 51. Вместе почти как главный запрос /exhibition «застройка выставочных стендов» 143.

Решения владельца 25.09.2026: дизайн-проект стенда делаем и отдельно от застройки, для чужого
застройщика, цена от 100 000 ₽. Разбор проекта стенда Самарской области к форуму «Россия —
спортивная держава» остаётся на /exhibition (#ex-case), здесь только выжимка со ссылкой.
По этому проекту стенд НЕ строили, это пишем прямо.

Факты только из наших проектов: стенд Самарской области на ВДНХ построен (248 дней работы,
16 млн посетителей); концепт-рендер этого же стенда вырезан из cn-mood1.jpg в
/images/exhibition/design/vdnh-render.jpg. Стенд Ставрополья сюда не берём: там наша часть
только мультимедиа. Фирменный стиль выставки «Самара» в Музее Алабина: /creative/samara.

Сигнатурная механика: альбом проекта. Шесть листов проекта Самары в рамке чертежа со штампом
«объект / стадия / лист», переключаются radio + :checked без JS.

Правки: ТОЛЬКО через этот скрипт.
Прогон: python3 scripts/a2/finalize_page.py gen_exhibition_design.py
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

URL = 'https://hand-marketing.ru/exhibition/dizayn-stenda/'
TITLE = 'Дизайн и проектирование выставочных стендов в Москве | Hand Marketing'
DESCR = ('Дизайн выставочного стенда: концепция, зонирование, 3D-визуализация и рабочие чертежи. '
         'Проект для вашего застройщика или стенд под ключ. Дизайн-проект от 100 000 ₽.')
EX = '/images/exhibition/samara'
VP = '/images/vp'
SV = '/images/lib/custom-samara-vdnh'

# проект → монтаж → работающий стенд: один объект, стенд Самарской области на ВДНХ
ROUTE = [
    ('Проект', '/images/exhibition/design/vdnh-render.jpg',
     'Концепт-рендер: изогнутый экран-парус, амфитеатр для программы, LED-шары под потолком.',
     'Концепт-рендер стенда Самарской области на ВДНХ'),
    ('Монтаж', f'{SV}/build-hall.jpg',
     'Каркас паруса и амфитеатр в павильоне. Размеры экранов и точки крепления заданы проектом.',
     'Монтаж стенда Самарской области в павильоне ВДНХ'),
    ('Стенд', f'{SV}/stand-hero.jpg',
     'Стенд работает: 248 дней, 16 млн посетителей, экраны и интерактив по одному пульту.',
     'Стенд Самарской области на ВДНХ с экраном-парусом'),
]

KINDS = [
    ('Легенда и концепция', 'О чём стенд и чем его запомнят. Для крупного стенда показываем '
     'несколько концепций, у каждой своя видеопрезентация.'),
    ('Зонирование и потоки', 'Где стойка, где переговорная, где очередь к интерактиву. '
     'У делегаций, деловых гостей и семей с детьми свои маршруты.'),
    ('3D-визуализация', 'Рендеры с нескольких точек и видеооблёт: стенд можно показать '
     'руководству до начала производства.'),
    ('Конструктив и чертежи', 'План застройки, развёртки, узлы и спецификации. По ним стенд '
     'строим мы или ваш застройщик.'),
    ('Экраны в конструктиве', 'LED-пилоны, медиапотолок и сенсорные стойки получают место, '
     'подводку и крепление в проекте, а не на монтаже.'),
    ('Требования выставки', 'Высота застройки, нагрузки, электричество и пожарные нормы '
     'павильона. Проект согласуем с организатором.'),
]

# (ключ, ярлык вкладки, стадия, картинка, подпись, alt)
SHEETS = [
    ('legend', 'Легенда', 'Концепция', f'{VP}/4-stihii_samara.jpg',
     'Концепция «Четыре стихии»: земля, вода, огонь и воздух. У каждой свой цвет, звук и своя '
     'зона на стенде. Параллельно шла вторая концепция, «Пять духов».',
     'Концепция «Четыре стихии» для стенда Самарской области'),
    ('plan', 'Зоны', 'Зонирование', f'{EX}/plan-v2.jpg',
     'План застройки второго варианта на 204 м². Пятнадцать зон: деловая сцена, '
     'VIP-переговорная, аттракционы спортивных клубов, фотозона.',
     'План застройки стенда Самарской области с подписями зон'),
    ('arena', 'Вариант 1', 'Визуализация', f'{EX}/render-v1-a.jpg',
     'Вариант «Неоновая арена»: светящийся контур по периметру и фасад, открытый на проход.',
     'Вариант «Неоновая арена»: 3D-визуализация стенда'),
    ('keepers', 'Вариант 2', 'Визуализация', f'{EX}/render-v2-a.jpg',
     'Вариант «Хранители»: медиаколонны с образами хранителей и LED-столбы. Подписи на рендере '
     'показывают, какие поверхности работают как экраны.',
     'Вариант «Хранители»: 3D-визуализация стенда с медиаколоннами'),
    ('ceiling', 'Медиапотолок', 'Мультимедиа', f'{EX}/render-v1-c.jpg',
     'Интерьер первого варианта. Экран над головой гостей заложен в конструктив с первого '
     'чертежа, а не подвешен после.',
     'Интерьер стенда с медиапотолком'),
    ('content', 'Контент', 'Контент', f'{VP}/content_samara.jpg',
     'Контент для экранов входит в проект: серия роликов «Самарский спорт в лицах» '
     'с AI-образами спортсменов.',
     'Концепция контента для экранов стенда'),
]

MODES = [
    ('Только дизайн-проект', 'от 100 000 ₽',
     'Концепция, зонирование, 3D-визуализация, чертежи и спецификация экранов. Отдаём файлы '
     'вашему застройщику и отвечаем на его вопросы по проекту.', None),
    ('Стенд под ключ', 'от 500 000 ₽',
     'Тот же проект, а дальше застройка, мультимедиа, контент, монтаж и демонтаж на выставке. '
     'За стенд отвечает одна команда.', ('/exhibition/', 'Застройка стендов под ключ')),
]

STEPS = [
    ('Бриф', 'Выставка, площадь и место в павильоне, задачи стенда, требования организатора.'),
    ('Эскизы и зоны', 'Одна-две недели: концепция, план с потоками гостей, первые эскизы.'),
    ('3D и выбор', 'Визуализация и видеооблёт вариантов, правки до утверждения.'),
    ('Рабочий проект', 'Полный проект от двух недель: чертежи, спецификации, экраны и контент.'),
    ('Застройка', 'Строим под ключ или передаём проект вашему застройщику.'),
]

FAQ = [
    ('Сколько стоит дизайн выставочного стенда?',
     'Дизайн-проект от 100 000 ₽, стенд под ключ вместе с проектом от 500 000 ₽. Итог зависит '
     'от площади, числа вариантов, объёма мультимедиа и от того, нужны ли рабочие чертежи. '
     'Смету готовим бесплатно после брифа.'),
    ('Можно заказать только проект, если стенд строит другой подрядчик?',
     'Да. Передаём вашему застройщику концепцию, визуализацию, план застройки, чертежи '
     'и спецификации и отвечаем на его вопросы по проекту.'),
    ('Сколько времени занимает проектирование стенда?',
     'Эскизы и зонирование готовим за одну-две недели, полный проект от двух недель. '
     'График считаем от даты монтажа на выставке.'),
    ('Что нужно от нас для начала работы?',
     'Название выставки, площадь и место стенда на плане павильона, требования организатора '
     'к застройке, задачи стенда и фирменный стиль компании.'),
    ('Сколько вариантов дизайна вы показываете?',
     'Столько, сколько нужно для решения. Для стенда Самарской области мы сделали две концепции '
     'и два варианта дизайна.'),
    ('Закладываете ли вы в проект экраны и интерактив?',
     'Да, с первого чертежа: место, подводка и крепление экрана решаются в проекте. Контент '
     'для экранов тоже делаем мы.'),
]

CSS = """<style>
.ds{--a:#673A7E;--ink:#14171C;--mut:#5A616A;--line:rgba(20,23,28,.12);--paper:#F7F5F0;
 font-family:'Montserrat',Arial,sans-serif;color:var(--ink);background:#fff}
.ds__in{max-width:1180px;margin:0 auto;padding:0 40px}
.ds-sec{padding:clamp(46px,5.6vw,80px) 0}
.ds-sec__h{margin:0 0 10px;font-size:clamp(26px,3.1vw,40px);font-weight:800;letter-spacing:-.02em;line-height:1.1}
.ds-sec__lead{margin:0 0 30px;max-width:72ch;font-size:16.5px;line-height:1.65;color:var(--mut)}
.ds-sec__lead a,.ds-more a{color:var(--a);font-weight:700}
.ds-hero{position:relative;min-height:clamp(400px,58vh,580px);display:flex;align-items:flex-end;color:#fff;overflow:hidden;background:#0E1016}
.ds-hero__img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ds-hero__sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,18,.25),rgba(10,10,18,.88))}
.ds-hero__in{position:relative;width:100%;max-width:1180px;margin:0 auto;padding:0 40px clamp(34px,4.6vw,60px)}
.ds-hero__k{margin:0 0 14px;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#D9C4E8}
.ds-hero h1{margin:0;font-size:clamp(28px,4.2vw,54px);font-weight:800;letter-spacing:-.025em;line-height:1.06;max-width:17ch}
.ds-hero__lead{margin:18px 0 0;max-width:60ch;font-size:clamp(15.5px,1.5vw,18px);line-height:1.6;color:rgba(255,255,255,.88)}
.ds-hero__f{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 0;padding:0;list-style:none}
.ds-hero__f li{border:1px solid rgba(255,255,255,.35);border-radius:30px;padding:9px 18px;font-size:14px;font-weight:600}
.ds-hero__cta{display:inline-block;margin-top:24px;background:#FCB724;color:#14171C;font-weight:800;font-size:15.5px;padding:15px 34px;border-radius:30px;text-decoration:none}
.ds-hero__cap{position:absolute;right:40px;top:22px;font-size:12px;color:rgba(255,255,255,.7);max-width:34ch;text-align:right}
.ds-crumbs{font-size:13px;color:#8A9099;padding:18px 0 0}
.ds-crumbs a{color:#8A9099;text-decoration:none}
.ds-crumbs a:hover{text-decoration:underline}
/* проект → монтаж → стенд */
.ds-route{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;counter-reset:rt}
.ds-route figure{margin:0;counter-increment:rt}
.ds-route__f{position:relative;border-radius:16px;overflow:hidden;background:var(--paper)}
.ds-route img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block}
.ds-route__t{position:absolute;left:12px;top:12px;background:#fff;border-radius:20px;padding:6px 14px 6px 10px;font-size:13px;font-weight:800;display:flex;gap:8px;align-items:center}
.ds-route__t::before{content:"0" counter(rt);color:var(--a)}
.ds-route figcaption{margin-top:12px;font-size:14.5px;line-height:1.6;color:var(--mut)}
.ds-more{margin:22px 0 0;font-size:15px;line-height:1.65;color:var(--mut);max-width:74ch}
.ds-kinds{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.ds-kind{border-top:2px solid var(--a);padding:14px 0 0}
.ds-kind b{display:block;font-size:16px;margin-bottom:6px}
.ds-kind span{font-size:14.5px;line-height:1.55;color:var(--mut)}
.ds-kind a{color:inherit}
/* альбом проекта: лист в рамке чертежа со штампом */
.ds-alb input{position:absolute;opacity:0;pointer-events:none}
.ds-alb__tabs{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}
.ds-alb__lbl{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:10px;padding:10px 14px;font-size:14px;font-weight:700;cursor:pointer;background:#fff;transition:border-color .15s,background .15s}
.ds-alb__lbl span{font-size:12px;color:#8A9099;font-weight:700}
.ds-alb__lbl:hover{border-color:var(--a)}
.ds-alb__sheet{display:none}
.ds-alb__frame{position:relative;background:#fff;border:1.5px solid var(--ink);padding:12px;box-shadow:10px 10px 0 -1px var(--paper),10px 10px 0 0 var(--line)}
.ds-alb__frame img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block;background:var(--paper)}
.ds-alb__stamp{position:absolute;right:12px;bottom:12px;display:grid;grid-template-columns:auto auto;background:#fff;border:1.5px solid var(--ink);font-size:11.5px;line-height:1.3}
.ds-alb__stamp span{padding:5px 9px;border-right:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.ds-alb__stamp span:nth-child(2n){border-right:0;font-weight:700}
.ds-alb__stamp span:nth-last-child(-n+2){border-bottom:0}
.ds-alb__stamp span:nth-child(2n+1){color:#8A9099;text-transform:uppercase;letter-spacing:.06em;font-size:10.5px}
.ds-alb__cap{margin:18px 0 0;font-size:15.5px;line-height:1.65;color:var(--mut);max-width:70ch}
.ds-alb__cap b{color:var(--ink)}
.ds-modes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.ds-mode{border:1px solid var(--line);border-radius:20px;padding:24px 26px;display:flex;flex-direction:column;gap:10px}
.ds-mode__h{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:6px 16px}
.ds-mode__h b{font-size:19px;letter-spacing:-.01em}
.ds-mode__h em{font-style:normal;font-size:22px;font-weight:900;color:var(--a);white-space:nowrap}
.ds-mode p{margin:0;font-size:15px;line-height:1.6;color:var(--mut)}
.ds-mode a{margin-top:auto;font-size:14px;font-weight:700;color:var(--a)}
.ds-steps{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:20px;counter-reset:st}
.ds-step{counter-increment:st;border-top:2px solid var(--a);padding-top:12px}
.ds-step::before{content:"0" counter(st);font-weight:800;font-size:13px;color:var(--a);letter-spacing:.08em}
.ds-step b{display:block;margin:6px 0;font-size:15px}
.ds-step span{font-size:14px;line-height:1.55;color:var(--mut)}
.ds-faq{display:grid;gap:10px;max-width:860px}
.ds-faq__i{border:1px solid rgba(20,23,28,.1);border-radius:14px;padding:0 20px}
.ds-faq__i summary{cursor:pointer;list-style:none;position:relative;padding:16px 36px 16px 0;font-size:15.5px;font-weight:700}
.ds-faq__i summary::-webkit-details-marker{display:none}
.ds-faq__i summary::after{content:"";position:absolute;right:2px;top:50%;width:11px;height:11px;transform:translateY(-70%) rotate(45deg);border-right:2.5px solid var(--a);border-bottom:2.5px solid var(--a);transition:transform .2s}
.ds-faq__i[open] summary::after{transform:translateY(-30%) rotate(225deg)}
.ds-faq__i p{margin:0 0 16px;font-size:14.5px;line-height:1.65;color:var(--mut)}
@media(max-width:980px){.ds-kinds{grid-template-columns:repeat(2,minmax(0,1fr))}.ds-steps{grid-template-columns:repeat(2,minmax(0,1fr))}.ds-route{grid-template-columns:minmax(0,1fr)}.ds-route img{aspect-ratio:16/9}}
@media(max-width:640px){.ds__in,.ds-hero__in{padding-left:18px;padding-right:18px}.ds-kinds,.ds-modes,.ds-steps{grid-template-columns:minmax(0,1fr)}
 .ds-hero__cap{display:none}.ds-alb__frame{padding:8px;box-shadow:none}.ds-alb__stamp{position:static;margin-top:8px}}
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
        '<section class="ds-hero">'
        f'<img class="ds-hero__img" src="{EX}/render-v1-a.jpg" '
        'alt="Дизайн-проект выставочного стенда Самарской области: 3D-визуализация варианта «Неоновая арена»" '
        'fetchpriority="high" decoding="async">'
        '<span class="ds-hero__sh" aria-hidden="true"></span>'
        '<p class="ds-hero__cap">Дизайн-проект стенда Самарской области, вариант «Неоновая арена»</p>'
        '<div class="ds-hero__in">'
        '<p class="ds-hero__k">Exhibition · Дизайн стенда</p>'
        '<h1>Дизайн и проектирование выставочных стендов</h1>'
        '<p class="ds-hero__lead">Придумываем, о чём стенд, разводим потоки гостей, рисуем стенд '
        'в 3D и выпускаем чертежи, по которым его строят. Экраны и интерактив закладываем '
        'в проект с первого листа.</p>'
        '<ul class="ds-hero__f"><li>дизайн-проект от 100 000 ₽</li><li>эскизы за 1–2 недели</li>'
        '<li>только проект или под ключ</li></ul>'
        '<a class="ds-hero__cta" href="#lead">Обсудить стенд</a>'
        '</div></section>')


def crumbs():
    return ('<div class="ds__in"><nav class="ds-crumbs" aria-label="Навигация по разделам">'
            '<a href="/">Главная</a> · <a href="/exhibition/">Застройка выставочных стендов</a> · '
            'Дизайн стенда</nav></div>')


def route():
    figs = ''.join(
        f'<figure><div class="ds-route__f"><img src="{img}" alt="{esc(alt)}" loading="lazy" '
        f'width="800" height="600"><span class="ds-route__t">{esc(t)}</span></div>'
        f'<figcaption>{esc(cap)}</figcaption></figure>'
        for t, img, cap, alt in ROUTE)
    return (f'<section class="ds-sec"><div class="ds__in">'
            f'<h2 class="ds-sec__h">От рендера до стенда на ВДНХ</h2>'
            f'<p class="ds-sec__lead">Один объект в трёх состояниях: стенд Самарской области '
            f'мы спроектировали и построили, он отработал на ВДНХ 248 дней. Проект здесь '
            f'не картинка для согласования, а документ, по которому стенд собирают в павильоне.</p>'
            f'<div class="ds-route">{figs}</div>'
            f'<p class="ds-more">Подробно о стенде в <a href="/portfolio/samara-stand-vdnh/">кейсе '
            f'стенда Самарской области</a>. Для выставки «Самара» в Музее Алабина мы сделали '
            f'<a href="/creative/samara/">фирменный стиль и оформление зон</a>.</p>'
            f'</div></section>')


def kinds():
    items = ''.join(f'<div class="ds-kind"><b>{esc(t)}</b><span>{esc(d)}</span></div>'
                    for t, d in KINDS)
    return (f'<section class="ds-sec" style="background:#FAF9FC"><div class="ds__in">'
            f'<h2 class="ds-sec__h">Что входит в дизайн-проект стенда</h2>'
            f'<p class="ds-sec__lead">Состав подбираем под выставку и задачу. Небольшому стенду '
            f'хватит эскиза и плана, стенду региона нужен полный альбом с чертежами и контентом. '
            f'Как экраны встраиваются в конструктив, разобрано на странице '
            f'<a href="/exhibition/multimedia/">мультимедиа для стенда</a>.</p>'
            f'<div class="ds-kinds">{items}</div></div></section>')


def album():
    """Альбом проекта: radio + :checked, без JS. Порядок узлов важен:
    сначала все input, потом вкладки, потом листы."""
    inputs, labels, sheets, css = '', '', '', ''
    n = len(SHEETS)
    for i, (key, tab, stage, img, cap, alt) in enumerate(SHEETS):
        checked = ' checked' if i == 0 else ''
        inputs += f'<input type="radio" name="dsalb" id="ds-{key}"{checked}>'
        labels += (f'<label class="ds-alb__lbl" for="ds-{key}"><span>{i + 1:02d}</span>'
                   f'{esc(tab)}</label>')
        sheets += (f'<div class="ds-alb__sheet" data-sheet="{key}"><figure style="margin:0">'
                   f'<div class="ds-alb__frame"><img src="{img}" alt="{esc(alt)}" loading="lazy" '
                   f'width="1600" height="900">'
                   f'<div class="ds-alb__stamp"><span>Объект</span><span>Стенд Самарской области, 204 м²</span>'
                   f'<span>Стадия</span><span>{esc(stage)}</span>'
                   f'<span>Лист</span><span>{i + 1:02d} из {n:02d} на странице</span></div></div>'
                   f'<figcaption class="ds-alb__cap"><b>{esc(tab)}.</b> {esc(cap)}</figcaption>'
                   f'</figure></div>')
        css += (f'#ds-{key}:checked ~ .ds-alb__tabs label[for="ds-{key}"]'
                '{border-color:var(--a);background:rgba(103,58,126,.07)}'
                f'#ds-{key}:checked ~ .ds-alb__sheets [data-sheet="{key}"]{{display:block}}')
    return (f'<section class="ds-sec"><div class="ds__in">'
            f'<h2 class="ds-sec__h">Проект стенда по листам</h2>'
            f'<p class="ds-sec__lead">Шесть листов из проекта стенда Самарской области к форуму '
            f'«Россия — спортивная держава»: 204 м², две концепции, два варианта дизайна, '
            f'79 листов в альбоме. Стенд по этому проекту не строили, но на нём видно, как идёт '
            f'работа до производства. Выберите лист.</p>'
            f'<style>{css}</style>'
            f'<div class="ds-alb">{inputs}'
            f'<div class="ds-alb__tabs">{labels}</div>'
            f'<div class="ds-alb__sheets">{sheets}</div></div>'
            f'<p class="ds-more">Все пятнадцать зон, обе концепции и видеопрезентации в '
            f'<a href="/exhibition/#ex-case">полном разборе проекта</a> на странице застройки стендов.</p>'
            f'</div></section>')


def modes():
    cards = ''
    for title, price, text, link in MODES:
        a = f'<a href="{link[0]}">{esc(link[1])} →</a>' if link else ''
        cards += (f'<div class="ds-mode"><div class="ds-mode__h"><b>{esc(title)}</b>'
                  f'<em>{esc(price)}</em></div><p>{esc(text)}</p>{a}</div>')
    return (f'<section class="ds-sec" style="background:#FAF9FC"><div class="ds__in">'
            f'<h2 class="ds-sec__h">Только проект или стенд под ключ</h2>'
            f'<p class="ds-sec__lead">Если у вас есть свой застройщик, заказывайте только дизайн. '
            f'Если нет, ведём стенд от эскиза до демонтажа.</p>'
            f'<div class="ds-modes">{cards}</div></div></section>')


def steps():
    items = ''.join(f'<div class="ds-step"><b>{esc(t)}</b><span>{esc(d)}</span></div>'
                    for t, d in STEPS)
    return (f'<section class="ds-sec"><div class="ds__in">'
            f'<h2 class="ds-sec__h">Этапы и сроки</h2>'
            f'<div class="ds-steps">{items}</div></div></section>')


def price():
    return (f'<section class="ds-sec" style="background:#FAF9FC"><div class="ds__in">'
            f'<h2 class="ds-sec__h">Стоимость и отзыв</h2>{cb.render("stand_design")}</div></section>')


def faq():
    items = ''.join(f'<details class="ds-faq__i"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
                    for q, a in FAQ)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage',
          'mainEntity': [{'@type': 'Question', 'name': q,
                          'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    return (f'<section class="ds-sec"><div class="ds__in">'
            f'<h2 class="ds-sec__h">Вопросы о дизайне стенда</h2>'
            f'<div class="ds-faq">{items}</div>'
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
    f'<meta property="og:image" content="https://hand-marketing.ru{EX}/render-v1-a.jpg">'
    + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    body = (f'{rc.header()}<main class="ds">{hero()}{crumbs()}{route()}{kinds()}{album()}'
            f'{modes()}{steps()}{price()}{faq()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'exhibition', 'dizayn-stenda')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
