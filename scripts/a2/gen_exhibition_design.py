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
import hm_ds as ds  # noqa: E402

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


# альбом проекта на фиолетовой полосе (radio + :checked, без JS) и два режима работы
CSS = """<style id="dsg-css">
.ds-alb>input{position:absolute;opacity:0;pointer-events:none}
.ds-alb__tabs{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 28px}
.ds-alb__lbl{cursor:pointer;display:inline-flex;align-items:center;gap:8px;border:1.5px solid rgba(255,255,255,.45);border-radius:30px;padding:9px 18px;font-size:14px;font-weight:700;color:#fff;transition:background .15s,color .15s}
.ds-alb__lbl span{font-size:12px;opacity:.7}
.ds-alb__lbl:hover{border-color:#fff}
.ds-alb__sheet{display:none}
.ds-alb__frame{position:relative;background:#fff;padding:12px}
.ds-alb__frame img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}
.ds-alb__stamp{position:absolute;right:24px;bottom:24px;display:grid;grid-template-columns:auto auto;background:#fff;border:1.5px solid #111;font-size:11px;line-height:1.3;color:#111}
.ds-alb__stamp span{padding:5px 10px;border-bottom:1px solid #111}
.ds-alb__stamp span:nth-child(odd){border-right:1px solid #111;font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:10px}
.ds-alb__stamp span:nth-last-child(-n+2){border-bottom:0}
.ds-alb__cap{margin:18px 0 0;max-width:80ch;font-size:16px;line-height:1.7;color:rgba(255,255,255,.86)}
.ds-alb__cap b{color:#fff}
.ds-modes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:1.5px solid #111}
.ds-mode{padding:28px 32px 30px 0;border-bottom:1px solid #E6E6E6}
.ds-mode+.ds-mode{padding-left:32px;border-left:1px solid #E6E6E6}
.ds-mode small{display:block;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--a)}
.ds-mode b{display:block;margin-top:10px;font-size:clamp(28px,3vw,36px);font-weight:800;color:#111}
.ds-mode p{margin:10px 0 0;font-size:15px;line-height:1.65;color:#4C4C4C}
.ds-mode a{display:inline-block;margin-top:14px;font-size:14px;font-weight:700;color:#111;text-decoration:none;border-bottom:2px solid #FFF700}
@media(max-width:860px){.ds-alb__stamp{position:static;margin-top:10px;grid-template-columns:auto minmax(0,1fr)}
 .ds-alb__lbl{font-size:13px;padding:8px 14px}
 .ds-modes{grid-template-columns:minmax(0,1fr)}.ds-mode+.ds-mode{padding-left:0;border-left:0}}
</style>"""


def hero():
    lede = ('Придумываем, о чём стенд, разводим потоки гостей, рисуем стенд в 3D и выпускаем чертежи, '
            'по которым его строят. Экраны и интерактив закладываем в проект с первого листа.')
    return ds.hero('Exhibition', 'Exhibition · Дизайн стенда',
                   'Дизайн и проектирование выставочных стендов', esc(lede),
                   chips=('дизайн-проект от 100 000 ₽', 'эскизы за 1–2 недели', 'только проект или под ключ'),
                   ctas=(('Обсудить стенд', '#lead', 'y'), ('Застройка под ключ', '/exhibition/', 'o')),
                   figs=0)


def banner():
    return ds.banner('/exhibition/#ex-case', '/videos/design-hero-poster.jpg',
                     '3D-визуализация проекта стенда Самарской области', 'Проект стенда Самарской области',
                     'Две концепции, два варианта, 79 листов',
                     'Проект к форуму «Россия — спортивная держава» на 204 м²: варианты дизайна в 3D '
                     'до начала производства.', chips=('204 м²', '79 листов'),
                     video='/videos/design-hero-loop.mp4')


def crumbs():
    return ds.crumbs([('Главная', '/'), ('Застройка выставочных стендов', '/exhibition/'),
                      ('Дизайн стенда', None)])


def route():
    tiles = ds.tiles([(img, alt, f'{i + 1:02d} · {t}', cap) for i, (t, img, cap, alt) in enumerate(ROUTE)],
                     cols=3)
    more = ('<p class="hd-note">Подробно о стенде в <a href="/portfolio/samara-stand-vdnh/">кейсе '
            'стенда Самарской области</a>. Для выставки «Самара» в Музее Алабина мы сделали '
            '<a href="/creative/samara/">фирменный стиль и оформление зон</a>. Ещё один стенд '
            'по нашему проекту: <a href="/portfolio/becar-private-money/">You&amp;Co для Becar</a> '
            'на форуме Private Money 2021, семь брендов на узкой полосе галереи. Клиенту показали '
            'два эскиза и финальный вариант, потом построили.</p>')
    return ds.sec(tiles + more, 'От рендера до стенда на ВДНХ',
                  esc('Один объект в трёх состояниях: стенд Самарской области мы спроектировали и '
                      'построили, он отработал на ВДНХ 248 дней. Проект здесь не картинка для '
                      'согласования, а документ, по которому стенд собирают в павильоне.'), icons=3, top=True)


def kinds():
    lead = ('Состав подбираем под выставку и задачу. Небольшому стенду хватит эскиза и плана, стенду '
            'региона нужен полный альбом с чертежами и контентом. Как экраны встраиваются в конструктив, '
            'разобрано на странице <a href="/exhibition/multimedia/">мультимедиа для стенда</a>.')
    return ds.sec(ds.feats([(t, esc(d)) for t, d in KINDS], cols=3), 'Что входит в дизайн-проект стенда',
                  lead, alt=True, icons=3, icon_start=3)


def album():
    """Порядок узлов важен: сначала все input, потом вкладки, потом листы."""
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
        css += (f'#ds-{key}:checked~.ds-alb__tabs label[for="ds-{key}"]'
                '{background:#FFF700;border-color:#FFF700;color:#000}'
                f'#ds-{key}:focus-visible~.ds-alb__tabs label[for="ds-{key}"]{{outline:2px solid #FFF700;outline-offset:3px}}'
                f'#ds-{key}:checked~.ds-alb__sheets [data-sheet="{key}"]{{display:block}}')
    inner = (f'<style>{css}</style><div class="ds-alb">{inputs}'
             f'<div class="ds-alb__tabs">{labels}</div><div class="ds-alb__sheets">{sheets}</div></div>'
             f'<p class="hd-note">Все пятнадцать зон, обе концепции и видеопрезентации в '
             f'<a href="/exhibition/#ex-case">полном разборе проекта</a> на странице застройки стендов.</p>')
    lead = ('Шесть листов из проекта стенда Самарской области к форуму «Россия — спортивная держава»: '
            '204 м², две концепции, два варианта дизайна, 79 листов в альбоме. Стенд по этому проекту '
            'не строили, но на нём видно, как идёт работа до производства. Выберите лист.')
    return ds.band(inner, 'Проект стенда по листам', esc(lead), kicker='Альбом проекта', fig='blocks')


def modes():
    cards = ''
    for title, price, text, link in MODES:
        a = f'<a href="{link[0]}">{esc(link[1])}</a>' if link else ''
        cards += f'<div class="ds-mode"><small>{esc(title)}</small><b>{esc(price)}</b><p>{esc(text)}</p>{a}</div>'
    return ds.sec(f'<div class="ds-modes">{cards}</div>', 'Только проект или стенд под ключ',
                  esc('Если у вас есть свой застройщик, заказывайте только дизайн. Если нет, ведём стенд '
                      'от эскиза до демонтажа.'), icons=2, icon_start=6)


def steps():
    return ds.band(ds.steps([(t, esc(d)) for t, d in STEPS], cols=5), 'Этапы и сроки', dark=True, fig='h')


def price():
    return ds.sec(ds.cost('stand_design'), 'Стоимость и отзыв')


def faq():
    return ds.sec(ds.faq(FAQ), 'Вопросы о дизайне стенда', alt=True)


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
    + rc.FONT + rc.CSS + ds.CSS + CSS + METRIKA + '</head><body>')


def page():
    body = (f'{rc.header()}<main class="hd" style="--a:{ds.EXH}">{crumbs()}{hero()}{banner()}{route()}{kinds()}'
            f'{album()}{modes()}{steps()}{price()}{faq()}</main>'
            f'{ds.BANNER_JS}<a id="lead"></a>{rc.footer()}{rc.JS}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'exhibition', 'dizayn-stenda')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
