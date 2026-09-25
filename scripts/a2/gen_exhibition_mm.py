#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/exhibition/multimedia/index.html — страницу «Мультимедиа для
выставочного стенда».

Зачем отдельно от /exhibition: у мультимедиа свой спрос и свои конкуренты (artkartel,
filin, interpro, pro-lgroup), а застройщики в топе продают конструкции. Вордстат, Москва:
интерактивная зона 258, интерактивный стенд 155, интерактивные инсталляции 114,
контент для экранов 87, кинетический экран 62, видеостена аренда 65.

⚠️ Интент: по «интерактивный стенд» в топе школьные и учебные стенды, туда не целимся.
Ключевые формулировки страницы: мультимедийный выставочный стенд, интерактивные зоны
и инсталляции, контент для экранов стенда.

Факты только из наших кейсов: стенд Самарской области на ВДНХ (экран-парус, кинетический
экран, восемь тач-панелей, LED-шары, прозрачный OLED, VR и MR), стенд Ставропольского края
(12 экранов, наша часть — мультимедийное оснащение), выставка «Самара» в Музее Алабина
(техника переехала со стенда, пять комплектов VR наши: поставка, разработка и виртуальный
запуск ракеты). Цены и формулировки согласованы с владельцем 19.09.2026; про партнёров
по технике на сайте не пишем.

Сигнатурная механика: переключатель поверхностей стенда (radio + :checked, без JS):
выбираешь поверхность, видишь кадр и что на ней шло.

Правки: ТОЛЬКО через этот скрипт.
Прогон: python3 scripts/a2/finalize_page.py gen_exhibition_mm.py
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

URL = 'https://hand-marketing.ru/exhibition/multimedia/'
TITLE = 'Мультимедийный выставочный стенд: экраны и интерактив | Hand Marketing'
DESCR = ('Мультимедиа для выставочного стенда: LED-экраны, проекция и naked eye 3D, сенсорные '
         'панели, интерактивные инсталляции и контент под ваши поверхности. От 150 000 ₽.')
SV = '/images/lib/custom-samara-vdnh'
ST = '/images/stavropol'

SURFACES = [
    ('parus', 'Экран-парус', f'{SV}/parus-poster.jpg',
     'Изогнутый LED с шагом 2 мм и 16,5 млн светодиодов на двух сторонах. Снаружи идёт контент '
     'naked eye 3D, внутри работает поверхность программы стенда.',
     'Изогнутый экран-парус стенда Самарской области'),
    ('kinetic', 'Кинетический экран', f'{SV}/kin-live.jpg',
     'Пиксели выдвигаются из плоскости на 20 см. На нём шли портреты земляков и сравнение '
     '«было и стало»: рельеф переключает состояние прямо на экране.',
     'Кинетический экран с выдвинутыми пикселями'),
    ('touch', 'Тач-панели', f'{SV}/stand-touch.jpg',
     'Восемь панелей на 86 и 32 дюйма: каталог региона, расписание событий, голосования '
     'и розыгрыши. Интерфейсы и структуру меню делали мы.',
     'Гость у сенсорной панели на стенде'),
    ('balls', 'LED-шары и прозрачный экран', f'{SV}/stand-balls.jpg',
     'Три LED-шара под потолком и две прозрачные панели OLED 55 дюймов: текст ложится поверх '
     'витрины с айдентикой региона.',
     'LED-шары над стендом'),
    ('kinect', 'Интерактив с камерой', f'{SV}/live-kinect.jpg',
     'Футбол с «Крыльями Советов», баскетбол и хоккей: гость играет телом, без контроллеров. '
     'Очередь к такой зоне держится весь день.',
     'Гость играет в футбол перед экраном с камерой'),
    ('vr', 'VR и смешанная реальность', f'{SV}/live-vr.jpg',
     'Сборка и запуск виртуальной ракеты «Союз» руками и VR-кинотеатр о регионе. '
     'Поставка оборудования и разработка контента наши.',
     'Посетители стенда в VR-очках'),
]

KINDS = [
    ('LED-экраны и видеостены', 'Главный экран зоны, лента над стойкой, медиапотолок.'),
    ('Проекция и naked eye 3D', 'Картинка, рассчитанная под точку зрителя в зале.'),
    ('Сенсорные панели и столы', 'Каталог, навигатор по продукту, заявка прямо на стенде.'),
    ('Кинетика', 'Экран с выдвижением пикселей: движение притягивает взгляд с прохода.'),
    ('Интерактивные инсталляции', 'Аттракцион, где гость участвует телом, а не кликом.'),
    ('Контент и интерфейсы', 'Ролики, графика, меню панелей и система управления показом.'),
]

CASES = [
    ('/portfolio/samara-stand-vdnh/', f'{SV}/stand-crowd.jpg',
     'Стенд Самарской области, ВДНХ',
     '248 дней работы и 16 млн посетителей стенда. Экран-парус, кинетический экран, восемь '
     'тач-панелей, LED-шары, прозрачные панели, VR и MR: всё управлялось с одного пульта.',
     'Посетители у стенда Самарской области на ВДНХ'),
    ('/portfolio/stavropol-stand-vdnh/', f'{ST}/stand-wide.jpg',
     'Стенд Ставропольского края, ВДНХ',
     'Наша часть на этом стенде это мультимедийное оснащение: 12 экранов, анаморфный куб, панель с жилым '
     'кварталом, тач-экран с красками края, терренкур и VR-станции.',
     'Стенд Ставропольского края с анаморфным кубом'),
    ('/portfolio/samara-exhibition/', f'{SV}/stand-front.jpg',
     'Выставка «Самара» в Музее Алабина',
     'Техника переехала со стенда ВДНХ и продолжила работать: экран-парус с 3D, кинетический '
     'экран, панели с Kinect и пять комплектов VR.',
     'Экран-парус на выставке в Музее Алабина'),
]

WHY = [
    ('Место и нагрузка', 'Экран, пилон и сенсорная стойка требуют места, подводки и точки '
     'крепления. Если их рисуют после конструктива, они лезут в проход или не держатся.'),
    ('Размер картинки', 'Контент считается под реальные размеры поверхности. Иначе графику '
     'обрезает по краям, а текст на изогнутом экране ломается.'),
    ('Очередь и сценарий', 'Сценарий зоны решает, сколько человек стоит у экрана '
     'одновременно и куда идёт очередь, чтобы она не перекрывала вход на стенд.'),
]

FAQ = [
    ('Сколько стоит мультимедиа для выставочного стенда?',
     'Мультимедийная зона от 150 000 ₽, стенд под ключ вместе с мультимедиа от 500 000 ₽. '
     'Итог зависит от числа экранов, площади поверхностей и сложности контента. Смету готовим '
     'бесплатно после брифа.'),
    ('Можно ли заказать мультимедиа, если стенд строит другой подрядчик?',
     'Да, это отдельная услуга. Мы подключаемся на этапе проекта, согласуем места и нагрузки '
     'с вашим застройщиком и берём на себя экраны, интерактив и контент.'),
    ('Какие интерактивные инсталляции можно поставить на стенд?',
     'На стенде Самарской области работали игры с камерой: футбол с «Крыльями Советов», баскетбол '
     'и хоккей, где гость играет телом. Рядом сенсорные панели с викторинами и голосованиями '
     'и VR со сборкой и запуском ракеты «Союз». Набор подбираем под поток гостей и задачу стенда.'),
    ('Кто делает контент для экранов?',
     'Мы. Графика, анимация и ролики, интерфейсы сенсорных панелей и система управления показом. '
     'Съёмку ведут наши операторы.'),
    ('Сколько времени занимает подготовка?',
     'Схему мультимедиа и эскизы готовим за одну-две недели, полный проект от двух недель. '
     'Дальше идёт производство контента и монтаж по графику выставки.'),
    ('Что остаётся после выставки?',
     'Техника и контент могут работать дальше. Оснащение стенда Самарской области после ВДНХ '
     'переехало в Музей имени Алабина и продолжило работать на выставке «Самара».'),
]

CSS = """<style>
.mm{--a:#673A7E;font-family:'Montserrat',Arial,sans-serif;color:#14171C;background:#fff}
.mm__in{max-width:1180px;margin:0 auto;padding:0 40px}
.mm-sec{padding:clamp(46px,5.6vw,80px) 0}
.mm-sec__h{margin:0 0 10px;font-size:clamp(26px,3.1vw,40px);font-weight:800;letter-spacing:-.02em;line-height:1.1}
.mm-sec__lead{margin:0 0 30px;max-width:72ch;font-size:16.5px;line-height:1.65;color:#5A616A}
.mm-hero{position:relative;min-height:clamp(380px,56vh,560px);display:flex;align-items:flex-end;color:#fff;overflow:hidden}
.mm-hero__img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.mm-hero__sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,10,20,.3),rgba(12,10,20,.86))}
.mm-hero__in{position:relative;width:100%;max-width:1180px;margin:0 auto;padding:0 40px clamp(34px,4.6vw,60px)}
.mm-hero__k{margin:0 0 14px;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#D9C4E8}
.mm-hero h1{margin:0;font-size:clamp(28px,4.2vw,54px);font-weight:800;letter-spacing:-.025em;line-height:1.06;max-width:19ch}
.mm-hero__lead{margin:18px 0 0;max-width:60ch;font-size:clamp(15.5px,1.5vw,18px);line-height:1.6;color:rgba(255,255,255,.88)}
.mm-hero__f{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 0;padding:0;list-style:none}
.mm-hero__f li{border:1px solid rgba(255,255,255,.35);border-radius:30px;padding:9px 18px;font-size:14px;font-weight:600}
.mm-hero__cta{display:inline-block;margin-top:24px;background:#FCB724;color:#14171C;font-weight:800;font-size:15.5px;padding:15px 34px;border-radius:30px;text-decoration:none}
.mm-crumbs{font-size:13px;color:#8A9099;padding:18px 0 0}
.mm-crumbs a{color:#8A9099;text-decoration:none}
.mm-crumbs a:hover{text-decoration:underline}
.mm-kinds{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.mm-kind{border-top:2px solid var(--a);padding:14px 0 0}
.mm-kind b{display:block;font-size:16px;margin-bottom:6px}
.mm-kind span{font-size:14.5px;line-height:1.55;color:#5A616A}
.mm-surf{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:clamp(20px,3vw,44px);align-items:start}
.mm-surf__tabs{display:grid;gap:8px}
.mm-surf input{position:absolute;opacity:0;pointer-events:none}
.mm-surf__lbl{display:block;border:1px solid rgba(20,23,28,.12);border-radius:14px;padding:14px 18px;font-size:15px;font-weight:700;cursor:pointer;transition:border-color .15s,background .15s}
.mm-surf__lbl:hover{border-color:var(--a)}
.mm-surf__panel{display:none}
.mm-surf__panel figure{margin:0}
.mm-surf__panel img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:18px;display:block}
.mm-surf__panel figcaption{margin-top:16px;font-size:15.5px;line-height:1.65;color:#5A616A;max-width:62ch}
.mm-surf__panel b{display:block;margin-bottom:6px;font-size:19px;color:#14171C;letter-spacing:-.01em}
.mm-cases{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.mm-case{display:flex;flex-direction:column;border:1px solid rgba(20,23,28,.1);border-radius:20px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .2s ease}
.mm-case:hover{transform:translateY(-4px)}
.mm-case img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.mm-case__b{padding:18px 20px 22px;display:flex;flex-direction:column;gap:8px;flex:1}
.mm-case__t{font-size:18px;font-weight:800;letter-spacing:-.01em}
.mm-case__d{font-size:14.5px;line-height:1.6;color:#5A616A}
.mm-case__go{margin-top:auto;font-size:14px;font-weight:700;color:var(--a)}
.mm-why{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.mm-why__c{background:#F6F4F9;border-radius:18px;padding:22px 24px}
.mm-why__c b{display:block;margin-bottom:8px;font-size:17px}
.mm-why__c span{font-size:14.5px;line-height:1.6;color:#5A616A}
.mm-faq{display:grid;gap:10px;max-width:860px}
.mm-faq__i{border:1px solid rgba(20,23,28,.1);border-radius:14px;padding:0 20px}
.mm-faq__i summary{cursor:pointer;list-style:none;position:relative;padding:16px 36px 16px 0;font-size:15.5px;font-weight:700}
.mm-faq__i summary::-webkit-details-marker{display:none}
.mm-faq__i summary::after{content:"";position:absolute;right:2px;top:50%;width:11px;height:11px;transform:translateY(-70%) rotate(45deg);border-right:2.5px solid var(--a);border-bottom:2.5px solid var(--a);transition:transform .2s}
.mm-faq__i[open] summary::after{transform:translateY(-30%) rotate(225deg)}
.mm-faq__i p{margin:0 0 16px;font-size:14.5px;line-height:1.65;color:#5A616A}
@media(max-width:980px){.mm-kinds,.mm-cases,.mm-why{grid-template-columns:repeat(2,minmax(0,1fr))}.mm-surf{grid-template-columns:minmax(0,1fr)}}
@media(max-width:640px){.mm__in,.mm-hero__in{padding-left:18px;padding-right:18px}.mm-kinds,.mm-cases,.mm-why{grid-template-columns:minmax(0,1fr)}}
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
        '<section class="mm-hero">'
        f'<img class="mm-hero__img" src="{SV}/stand-front.jpg" '
        'alt="Мультимедийный выставочный стенд Самарской области: изогнутый экран-парус" '
        'fetchpriority="high" decoding="async">'
        '<span class="mm-hero__sh" aria-hidden="true"></span>'
        '<div class="mm-hero__in">'
        '<p class="mm-hero__k">Exhibition · Мультимедиа</p>'
        '<h1>Мультимедиа для выставочного стенда</h1>'
        '<p class="mm-hero__lead">Экраны, проекции и интерактивные инсталляции, которые проектируются вместе '
        'с конструктивом стенда, а не вешаются на готовые стены. Контент под каждую поверхность '
        'рисуем сами.</p>'
        '<ul class="mm-hero__f"><li>от 150 000 ₽</li><li>три стенда на ВДНХ и в музее</li>'
        '<li>контент и интерфейсы наши</li></ul>'
        '<a class="mm-hero__cta" href="#lead">Обсудить проект</a>'
        '</div></section>')


def crumbs():
    return ('<div class="mm__in"><nav class="mm-crumbs" aria-label="Навигация по разделам">'
            '<a href="/">Главная</a> · <a href="/exhibition/">Застройка выставочных стендов</a> · '
            'Мультимедиа для стенда</nav></div>')


def kinds():
    items = ''.join(f'<div class="mm-kind"><b>{esc(t)}</b><span>{esc(d)}</span></div>'
                    for t, d in KINDS)
    return (f'<section class="mm-sec"><div class="mm__in">'
            f'<h2 class="mm-sec__h">Что ставим на стенд</h2>'
            f'<p class="mm-sec__lead">Набор подбирается под задачу стенда и поток посетителей, '
            f'а не по прайсу оборудования.</p>'
            f'<div class="mm-kinds">{items}</div></div></section>')


def surfaces():
    """Переключатель поверхностей: radio + :checked, без JS.
    Порядок узлов важен: сначала все input, потом .mm-surf__tabs с label, потом панели."""
    inputs, labels, panels, css = '', '', '', ''
    for i, (key, name, img, text, alt) in enumerate(SURFACES):
        checked = ' checked' if i == 0 else ''
        inputs += f'<input type="radio" name="mmsurf" id="mm-{key}"{checked}>'
        labels += f'<label class="mm-surf__lbl" for="mm-{key}">{esc(name)}</label>'
        panels += (f'<div class="mm-surf__panel" data-surf="{key}"><figure>'
                   f'<img src="{img}" alt="{esc(alt)}" loading="lazy" width="1200" height="675">'
                   f'<figcaption><b>{esc(name)}</b>{esc(text)}</figcaption></figure></div>')
        css += (f'#mm-{key}:checked ~ .mm-surf__tabs label[for="mm-{key}"]'
                '{border-color:var(--a);background:rgba(103,58,126,.07)}'
                f'#mm-{key}:checked ~ .mm-surf__panels [data-surf="{key}"]{{display:block}}')
    return (f'<section class="mm-sec" style="background:#FAF9FC"><div class="mm__in">'
            f'<h2 class="mm-sec__h">Поверхности стенда и что на них шло</h2>'
            f'<p class="mm-sec__lead">Состав мультимедиа стенда Самарской области на ВДНХ. '
            f'Выберите поверхность, чтобы увидеть кадр и содержание.</p>'
            f'<style>{css}</style>'
            f'<div class="mm-surf">{inputs}'
            f'<div class="mm-surf__tabs">{labels}</div>'
            f'<div class="mm-surf__panels">{panels}</div></div>'
            f'</div></section>')


def cases():
    cards = ''.join(
        f'<a class="mm-case" href="{href}">'
        f'<img src="{img}" alt="{esc(alt)}" loading="lazy" width="800" height="500">'
        f'<span class="mm-case__b"><span class="mm-case__t">{esc(title)}</span>'
        f'<span class="mm-case__d">{esc(text)}</span>'
        f'<span class="mm-case__go">Смотреть кейс →</span></span></a>'
        for href, img, title, text, alt in CASES)
    return (f'<section class="mm-sec"><div class="mm__in">'
            f'<h2 class="mm-sec__h">Где это уже работает</h2>'
            f'<div class="mm-cases">{cards}</div></div></section>')


def why():
    cards = ''.join(f'<div class="mm-why__c"><b>{esc(t)}</b><span>{esc(d)}</span></div>'
                    for t, d in WHY)
    return (f'<section class="mm-sec"><div class="mm__in">'
            f'<h2 class="mm-sec__h">Почему мультимедиа закладывают в проект, а не вешают потом</h2>'
            f'<p class="mm-sec__lead">Три причины, по которым экраны и интерактив мы рисуем '
            f'вместе с конструктивом. Как это выглядит на реальном проекте, видно в '
            f'<a href="/exhibition/#ex-case">разборе стенда Самарской области</a>. Экраны на плане '
            f'появляются на стадии <a href="/exhibition/dizayn-stenda/">дизайна и проектирования стенда</a>.</p>'
            f'<div class="mm-why">{cards}</div></div></section>')


def price():
    return (f'<section class="mm-sec" style="background:#FAF9FC"><div class="mm__in">'
            f'<h2 class="mm-sec__h">Стоимость и отзыв</h2>{cb.render("mm")}</div></section>')


def faq():
    items = ''.join(f'<details class="mm-faq__i"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
                    for q, a in FAQ)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage',
          'mainEntity': [{'@type': 'Question', 'name': q,
                          'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    return (f'<section class="mm-sec"><div class="mm__in">'
            f'<h2 class="mm-sec__h">Вопросы о мультимедиа на стенде</h2>'
            f'<div class="mm-faq">{items}</div>'
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
    f'<meta property="og:image" content="https://hand-marketing.ru{SV}/stand-front.jpg">'
    + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    body = (f'{rc.header()}<main class="mm">{hero()}{crumbs()}{kinds()}{surfaces()}'
            f'{cases()}{why()}{price()}{faq()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'exhibition', 'multimedia')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
