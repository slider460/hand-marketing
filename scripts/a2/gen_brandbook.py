#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/creativedesign/brandbook/index.html: «Разработка брендбука».

Почему эта посадочная, а не другие из дизайна (Вордстат, Москва, точные,
сентябрь 2026): «разработка брендбука» 97, «разработка логотипа» 51,
«разработка фирменного стиля» 36, «брендбук» 778 широкий. Выдача по
«разработка брендбука» целиком коммерческая: все десять мест у агентств,
цены «от 350 000» и «от 850 000». «Фирменный стиль» (201) и «дизайн
презентации» (188) информационные, там статьи и шаблоны, отдельная страница
под них не окупится.

Позиционирование владельца 20.09.2026: B2B, заказчик проверяет квалификацию.
Цена по дизайну владельцем не названа, поэтому «по объёму», без выдуманной вилки.
Язык оформления тот же, что у секций главной: цвет направления Creative
#C12164, тег с квадратом-маркером, радиус 24 с мягкой тенью, диск-стрелка.

Правки: ТОЛЬКО через этот скрипт.
Прогон: python3 scripts/a2/finalize_page.py gen_brandbook.py
"""
import html as H
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
sys.path.insert(0, HERE)
import commerce_block as cb  # noqa: E402

spec = importlib.util.spec_from_file_location('rc', os.path.join(HERE, 'react-chrome.py'))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

URL = 'https://hand-marketing.ru/creativedesign/brandbook/'
ACCENT = '#C12164'


def covers():
    """Круглые обложки кейсов из карусели каталога: те же, что на главной и /project."""
    car = open(os.path.join(HERE, 'carousels', 'all.html'), encoding='utf-8').read()
    return {m.group(1).rstrip('/'): m.group(2) for m in
            re.finditer(r'<a class="mcase" href="([^"]+)"[^>]*>.*?<img[^>]+src="([^"]+)"', car, re.S)}


COVERS = covers()

# что входит в брендбук: (что, зачем, цвет метки)
PARTS = [
    ('Логотип и знак', 'Основная и упрощённая версии, охранное поле, минимальный размер, '
     'запреты. Знак вынимается кривыми, чтобы работать от визитки до фасада.', '#C12164'),
    ('Цвет', 'Основная и дополнительная палитры с кодами для экрана, печати и производства. '
     'Проверяем, как цвет ведёт себя на плёнке, ткани и металле.', '#673A7E'),
    ('Шрифты', 'Пара для заголовков и текста, правила набора, кириллица. Если шрифт '
     'платный, подбираем лицензию или свободную замену.', '#8E5FB0'),
    ('Паттерны и графика', 'Фирменная графика, которая узнаётся без логотипа: паттерны, '
     'иконки, иллюстрации. Для Metra паттерны собирает генератор.', '#CF6F19'),
    ('Носители', 'Визитки, бланки, презентации, сувениры, форма персонала, транспорт. '
     'Каждый носитель с размерами и готовым файлом.', '#E08A2B'),
    ('Навигация и среда', 'Таблички, указатели, оформление стенда и помещения. '
     'Для выставки «Самара» сделали конструктор таблички по модулю.', '#3B729D'),
    ('Архитектура бренда', 'Как связаны материнский бренд и дочерние: общее и различия. '
     'Для Metra это пять брендов одной экосистемы.', '#5E9A2E'),
    ('Гайдлайн и шаблоны', 'Правила применения и исходники в рабочих форматах, чтобы '
     'дизайнер заказчика собирал новые материалы без нас.', '#D6357E'),
]

# форматы: (название, что внутри, срок)
FORMATS = [
    ('Логотип и мини-гайд', 'Знак, цвета, шрифты и базовые правила на нескольких полосах. '
     'Для нового проекта или продукта.', '2–3 недели'),
    ('Фирменный стиль', 'Логотип плюс фирменная графика и основные носители: '
     'бланки, презентация, визитки, соцсети.', 'от 3 недель'),
    ('Полный брендбук', 'Весь фирменный стиль, носители, навигация, среда и подробный '
     'гайдлайн с шаблонами.', 'от месяца'),
    ('Архитектура бренда', 'Система из нескольких брендов: материнский, дочерние, '
     'правила их сосуществования.', 'по объёму'),
]

# кейсы: (ссылка, заголовок, цифра, подпись)
CASES = [
    ('/creative/metra', 'Брендбук Metra Technology Group', '5 брендов',
     '69 полос, архитектура индустриальной экосистемы и генератор паттернов '
     'для каждого бренда.'),
    ('/creative/samara', 'Фирменный стиль выставки «Самара»', '28 полос',
     'Руководство для музея: маскот в 16 образах, конструктор навигационной таблички '
     'по модулю, стена зоны из 46 слов.'),
    ('/creative/becar/sdep', 'Стиль отдела продаж Becar', 'SALESDEP',
     'Знак и паттерн, вынутые кривыми из исходника, гайдлайн для всех '
     'материалов отдела.'),
    ('/creative/piloti', 'Пилоты будущего', 'логотип',
     'Креативная концепция и фирменный стиль детского клуба технологий: '
     'знак-корабль и паттерн.'),
    ('/creative/patriki', 'Журнал Patriki Times', 'сетка',
     'Дизайн издания и модульная сетка, по которой номер собирается '
     'каждый месяц.'),
    ('/creative/skolkovo', 'Доклад для СКОЛКОВО', '86 полос',
     'Вёрстка доклада «Цифровое производство» с инфографикой в едином '
     'визуальном языке.'),
]

STEPS = [
    ('Бриф и аудит', 'Задачи бренда, аудитория, конкуренты. Смотрим, что уже есть '
     'и что стоит сохранить.', '#673A7E'),
    ('Концепция', 'Два-три направления идеи с обоснованием. Выбираем одно '
     'и развиваем его.', '#8E5FB0'),
    ('Знак и система', 'Логотип, цвет, шрифты и графика. Проверяем на реальных '
     'носителях, а не на белом листе.', '#C12164'),
    ('Носители', 'Раскладываем стиль на все нужные материалы с размерами '
     'и готовыми файлами.', '#CF6F19'),
    ('Гайдлайн и сдача', 'Правила применения, шаблоны и исходники. Всё передаём '
     'заказчику, без привязки к нам.', '#5E9A2E'),
]

FAQ = [
    ('Сколько стоит разработка брендбука?',
     'Считаем по объёму. Логотип с мини-гайдом, фирменный стиль и полный брендбук '
     'с архитектурой бренда это разные сметы. После брифа готовим смету бесплатно, '
     'в ней видно каждую позицию.'),
    ('Сколько времени занимает работа?',
     'Логотип и базовая айдентика обычно 2–3 недели, полный брендбук от месяца. '
     'Срок зависит от числа носителей и итераций согласования.'),
    ('Чем брендбук отличается от фирменного стиля?',
     'Фирменный стиль это сам визуальный язык: знак, цвет, шрифты, графика. '
     'Брендбук добавляет к нему правила применения, носители и шаблоны, '
     'чтобы стиль держался без автора.'),
    ('Вы работаете с существующим брендом?',
     'Да. Можем развить готовую айдентику: добавить носители, собрать шаблоны, '
     'привести материалы к единому виду. Для Saint-Gobain мы годами делаем '
     'материалы внутри их гайдлайна.'),
    ('Что мы получим в конце?',
     'Брендбук в PDF, исходники в рабочих форматах, шрифты и лицензии, шаблоны '
     'носителей. Всё передаётся заказчику, без привязки к агентству.'),
    ('Вы потом печатаете и производите носители?',
     'Да, это наше отличие: печать, сувениры, навигация и оформление стендов '
     'делаются внутри агентства, поэтому стиль доходит до носителя без потерь '
     'в цвете и пропорциях.'),
]

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px" alt=""></div></noscript>')

CSS = """<style id="bb-css">
.bb{--ink:#14171C;--mut:#5A616A;--a:#C12164;--line:#ECEEF2;
 font-family:'Montserrat',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff}
.bb *{box-sizing:border-box}
.bb__in{max-width:1180px;margin:0 auto;padding:0 40px}
.bb-tag{display:inline-flex;align-items:center;gap:9px;font-size:11px;font-weight:800;
 letter-spacing:.2em;text-transform:uppercase;color:var(--c,var(--a));margin-bottom:12px}
.bb-tag::before{content:"";width:11px;height:11px;border-radius:3px;background:currentColor}
.bb-hero{position:relative;overflow:hidden;isolation:isolate;padding:72px 0 64px}
.bb-hero__ghost{position:absolute;z-index:-1;right:-20px;top:10px;font:900 420px/1 'Montserrat',Arial,sans-serif;
 color:var(--a);opacity:.06;letter-spacing:-.06em;pointer-events:none;user-select:none}
.bb-hero h1{margin:0 0 18px;font-size:clamp(32px,4.6vw,58px);font-weight:900;letter-spacing:-.03em;line-height:1.02;max-width:16ch}
.bb-hero p{margin:0;max-width:64ch;font-size:clamp(16px,1.5vw,18px);line-height:1.65;color:#3d434b}
.bb-chips{display:flex;flex-wrap:wrap;gap:10px;margin:26px 0 0;padding:0;list-style:none}
.bb-chips li{border:1.5px solid var(--line);border-radius:30px;padding:9px 18px;font-size:14px;font-weight:700}
.bb-cta{display:inline-block;margin-top:28px;background:#FCB724;color:#14171C!important;font-weight:800;font-size:15.5px;
 padding:15px 34px;border-radius:30px;text-decoration:none}
.bb-crumbs{font-size:13px;color:#8A9099;padding:20px 0 0}
.bb-crumbs a{color:#8A9099!important;text-decoration:none}
.bb-sec{padding:clamp(52px,6vw,84px) 0;border-top:1.5px solid var(--line)}
.bb-sec h2{margin:0 0 14px;font-size:clamp(26px,3.1vw,40px);font-weight:800;letter-spacing:-.02em;line-height:1.08}
.bb-sec p.lead{margin:0 0 30px;max-width:74ch;font-size:16.5px;line-height:1.7;color:#3d434b}
.bb-parts{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.bb-part{position:relative;background:#fff;border:1.5px solid var(--line);border-radius:24px;padding:22px 22px 20px;
 box-shadow:0 14px 30px -22px rgba(20,23,28,.5)}
.bb-part i{display:block;width:40px;height:6px;border-radius:3px;background:var(--c);margin-bottom:14px}
.bb-part h3{margin:0 0 8px;font-size:17px;font-weight:800;line-height:1.25}
.bb-part p{margin:0;font-size:14px;line-height:1.55;color:var(--mut)}
.bb-formats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.bb-f{position:relative;isolation:isolate;overflow:hidden;background:#fff;border:1.5px solid var(--line);border-radius:24px;
 padding:24px;box-shadow:0 14px 30px -22px rgba(20,23,28,.5);display:flex;flex-direction:column;gap:10px}
.bb-f__ghost{position:absolute;z-index:-1;right:2px;bottom:-40px;font:900 150px/1 'Montserrat',Arial,sans-serif;
 color:var(--a);opacity:.08;letter-spacing:-.06em}
.bb-f h3{margin:0;font-size:19px;font-weight:800;letter-spacing:-.01em;line-height:1.15}
.bb-f p{margin:0;font-size:14px;line-height:1.55;color:var(--mut)}
.bb-f b{margin-top:auto;font-size:14px;font-weight:800;color:var(--a)}
.bb-cases{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.bb-case{display:flex;flex-direction:column;background:#fff;border:1.5px solid var(--line);border-radius:24px;overflow:hidden;
 text-decoration:none;color:inherit!important;box-shadow:0 14px 30px -22px rgba(20,23,28,.5);transition:transform .2s,border-color .25s}
.bb-case:hover{transform:translateY(-3px);border-color:var(--a)}
.bb-case img{width:100%;height:210px;object-fit:contain;background:#F7F4F1;display:block;padding:12px 0}
.bb-case__b{padding:18px 22px 22px;display:flex;flex-direction:column;gap:8px;flex:1}
.bb-case__n{font-size:24px;font-weight:900;letter-spacing:-.02em;color:var(--a)}
.bb-case__t{font-size:17px;font-weight:800;line-height:1.25}
.bb-case__d{font-size:14px;line-height:1.55;color:var(--mut)}
.bb-case__go{margin-top:auto;font-size:14px;font-weight:800;color:var(--a)}
.bb-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:20px}
.bb-step__n{width:46px;height:46px;border-radius:50%;background:var(--c);color:#fff;font-size:17px;font-weight:900;
 display:inline-flex;align-items:center;justify-content:center;margin-bottom:12px}
.bb-step h3{margin:0 0 6px;font-size:16px;font-weight:800;line-height:1.25}
.bb-step p{margin:0;font-size:13.5px;line-height:1.55;color:var(--mut)}
.bb-faq{display:grid;gap:12px;max-width:900px}
.bb-faq details{border:1.5px solid var(--line);border-radius:20px;padding:0 22px;background:#fff}
.bb-faq summary{cursor:pointer;list-style:none;padding:18px 0;font-size:16px;font-weight:800;display:flex;align-items:center;gap:14px}
.bb-faq summary::-webkit-details-marker{display:none}
.bb-faq summary::before{content:"+";width:30px;height:30px;border-radius:50%;flex:none;background:#ECEEF2;color:#14171C;
 font-size:20px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;line-height:1}
.bb-faq details[open] summary::before{content:"\\2212";background:var(--a);color:#fff}
.bb-faq p{margin:0 0 20px 44px;font-size:15px;line-height:1.65;color:var(--mut)}
.bb-more{margin:30px 0 0;font-size:15.5px;line-height:1.7;color:#3d434b}
.bb-more a{color:var(--a)!important;font-weight:700}
@media(max-width:1100px){.bb-parts,.bb-formats{grid-template-columns:repeat(2,1fr)}.bb-steps{grid-template-columns:repeat(2,1fr)}}
@media(max-width:900px){.bb-cases{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.bb__in{padding:0 18px}.bb-parts,.bb-formats,.bb-cases,.bb-steps{grid-template-columns:1fr}
 .bb-hero__ghost{font-size:260px}}
</style>"""


def esc(t):
    return H.escape(t, quote=False)


def page():
    parts = ''.join(f'<div class="bb-part" style="--c:{c}"><i aria-hidden="true"></i>'
                    f'<h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d, c in PARTS)
    formats = ''.join(f'<div class="bb-f"><span class="bb-f__ghost" aria-hidden="true">{i + 1}</span>'
                      f'<h3>{esc(t)}</h3><p>{esc(d)}</p><b>{esc(term)}</b></div>'
                      for i, (t, d, term) in enumerate(FORMATS))
    cases = ''
    for href, title, num, txt in CASES:
        img = COVERS.get(href.rstrip('/'), '')
        pic = (f'<img src="{img}" alt="{H.escape(title)}" loading="lazy" width="600" height="600">'
               if img else '')
        cases += (f'<a class="bb-case" href="{href}/">{pic}<span class="bb-case__b">'
                  f'<span class="bb-case__n">{esc(num)}</span>'
                  f'<span class="bb-case__t">{esc(title)}</span>'
                  f'<span class="bb-case__d">{esc(txt)}</span>'
                  f'<span class="bb-case__go">Смотреть проект →</span></span></a>')
    steps = ''.join(f'<div class="bb-step" style="--c:{c}"><span class="bb-step__n">{i + 1:02d}</span>'
                    f'<h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
                    for i, (t, d, c) in enumerate(STEPS))
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
    ld_faq = {'@context': 'https://schema.org', '@type': 'FAQPage',
              'mainEntity': [{'@type': 'Question', 'name': q,
                              'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}

    title = 'Разработка брендбука и фирменного стиля в Москве | Hand Marketing'
    descr = ('Разработка брендбука, фирменного стиля и логотипа под ключ: знак, цвет, шрифты, '
             'паттерны, носители и гайдлайн. Брендбуки для Metra, выставки «Самара», Becar. '
             'Печать носителей своими силами.')
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
        f'{rc.header()}<main class="bb">'
        '<section class="bb-hero"><span class="bb-hero__ghost" aria-hidden="true">B</span>'
        '<div class="bb__in">'
        '<span class="bb-tag">Creative &amp; Design</span>'
        '<h1>Разработка брендбука и фирменного стиля</h1>'
        '<p>Делаем фирменный стиль, который работает на реальных носителях: от визитки '
        'до выставочного стенда. Брендбук Metra Technology Group на 69 полос с пятью брендами '
        'экосистемы, фирменный стиль выставки «Самара» на 28 полос, стиль отдела продаж Becar. '
        'Печать и производство носителей делаем сами, поэтому стиль доходит до площадки '
        'без потерь.</p>'
        '<ul class="bb-chips"><li>логотип за 2–3 недели</li><li>брендбук от месяца</li>'
        '<li>печать носителей своими силами</li></ul>'
        '<a class="bb-cta" href="#lead">Обсудить проект</a>'
        '</div></section>'
        '<div class="bb__in"><nav class="bb-crumbs" aria-label="Навигация по разделам">'
        '<a href="/">Главная</a> · <a href="/creativedesign/">Креатив и дизайн</a> · '
        'Разработка брендбука</nav></div>'

        '<section class="bb-sec"><div class="bb__in">'
        '<span class="bb-tag">Состав</span>'
        '<h2>Что входит в брендбук</h2>'
        '<p class="lead">Брендбук это не альбом с логотипом, а правила, по которым стиль '
        'держится без автора. Ниже то, что обычно входит в работу. Состав подбираем под задачу: '
        'новому продукту хватает мини-гайда, экосистеме нужна архитектура бренда.</p>'
        f'<div class="bb-parts">{parts}</div></div></section>'

        '<section class="bb-sec"><div class="bb__in">'
        '<span class="bb-tag">Форматы</span>'
        '<h2>От логотипа до архитектуры бренда</h2>'
        f'<div class="bb-formats">{formats}</div></div></section>'

        '<section class="bb-sec"><div class="bb__in">'
        '<span class="bb-tag">Проекты</span>'
        '<h2>Брендбуки и фирменные стили, которые мы сделали</h2>'
        '<p class="lead">У каждого проекта на сайте есть разбор: знак, система, носители '
        'и то, как стиль работает в реальной среде.</p>'
        f'<div class="bb-cases">{cases}</div></div></section>'

        '<section class="bb-sec"><div class="bb__in">'
        '<span class="bb-tag">Порядок работы</span>'
        '<h2>Как идёт разработка</h2>'
        '<p class="lead">Согласование идёт по промежуточным листам: заказчик видит концепцию, '
        'знак и носители до того, как стиль уйдёт в производство.</p>'
        f'<div class="bb-steps">{steps}</div></div></section>'

        '<section class="bb-sec"><div class="bb__in">'
        '<span class="bb-tag">Стоимость</span>'
        f'<h2>Стоимость и отзывы</h2>{cb.render("brandbook")}'
        '<p class="bb-more">Состав смет по всем направлениям разобран на странице '
        '<a href="/price/">стоимости</a>, другие работы по дизайну в разделе '
        '<a href="/creativedesign/">креатива и дизайна</a>.</p>'
        '</div></section>'

        '<section class="bb-sec"><div class="bb__in">'
        '<span class="bb-tag">Вопросы</span>'
        f'<h2>Что спрашивают о брендбуке</h2><div class="bb-faq">{faq}</div>'
        f'<script type="application/ld+json">'
        f'{json.dumps(ld_faq, ensure_ascii=False, separators=(",", ":"))}</script>'
        '</div></section>'
        '</main>'
        f'<a id="lead"></a>{rc.footer()}{rc.JS}</body></html>')
    return head + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creativedesign', 'brandbook')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('создано:', p, os.path.getsize(p) // 1024, 'КБ')
