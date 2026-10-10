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
import hm_ds as ds  # noqa: E402

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
    ('Кинетика', 'Экран с выдвижением пикселей и шары на лебёдках: движение притягивает взгляд с прохода.'),
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


# переключатель поверхностей на тёмной полосе: radio + :checked, без JS
CSS = """<style id="mm-css">
.mm-surf>input{position:absolute;opacity:0;pointer-events:none}
.mm-surf__tabs{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 30px}
.mm-surf__lbl{cursor:pointer;border:1.5px solid rgba(255,255,255,.45);border-radius:30px;padding:10px 18px;font-size:14px;font-weight:700;color:#fff;transition:background .15s,color .15s}
.mm-surf__lbl:hover{border-color:#fff}
.mm-surf__panel{display:none}
.mm-surf__panel figure{margin:0;display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:40px;align-items:center}
.mm-surf__panel img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}
.mm-surf__panel b{display:block;font-size:26px;font-weight:700;color:#fff;margin-bottom:14px}
.mm-surf__panel figcaption{font-size:16px;line-height:1.7;color:rgba(255,255,255,.82)}
@media(max-width:860px){.mm-surf__panel figure{grid-template-columns:minmax(0,1fr);gap:20px}.mm-surf__lbl{font-size:13px;padding:8px 14px}}
</style>"""


def hero():
    lede = ('Экраны, проекции и интерактивные инсталляции, которые проектируются вместе с конструктивом '
            'стенда, а не вешаются на готовые стены. Контент под каждую поверхность рисуем сами.')
    return ds.hero('Exhibition', 'Exhibition · Мультимедиа', 'Мультимедийный выставочный стенд', esc(lede),
                   chips=('от 150 000 ₽', 'три стенда на ВДНХ и в музее', 'контент и интерфейсы наши'),
                   ctas=(('Обсудить проект', '#lead', 'y'),
                         ('Стенд Самарской области', '/portfolio/samara-stand-vdnh/', 'o')), figs=1)


def banner():
    href, img, title, text, alt = CASES[0]
    return ds.banner(href, f'{SV}/stand-front.jpg',
                     'Мультимедийный выставочный стенд Самарской области: изогнутый экран-парус',
                     'ВДНХ · 248 дней', title, text, chips=('16 млн посетителей', 'один пульт'))


def crumbs():
    return ds.crumbs([('Главная', '/'), ('Застройка выставочных стендов', '/exhibition/'),
                      ('Мультимедиа для стенда', None)])


def kinds():
    return ds.sec(ds.feats([(t, esc(d)) for t, d in KINDS], cols=3), 'Что ставим на стенд',
                  esc('Набор подбирается под задачу стенда и поток посетителей, а не по прайсу оборудования.'),
                  icons=3, top=True)


def surfaces():
    """Порядок узлов важен: сначала все input, потом .mm-surf__tabs с label, потом панели."""
    inputs, labels, panels, css = '', '', '', ''
    for i, (key, name, img, text, alt) in enumerate(SURFACES):
        checked = ' checked' if i == 0 else ''
        inputs += f'<input type="radio" name="mmsurf" id="mm-{key}"{checked}>'
        labels += f'<label class="mm-surf__lbl" for="mm-{key}">{esc(name)}</label>'
        panels += (f'<div class="mm-surf__panel" data-surf="{key}"><figure>'
                   f'<img src="{img}" alt="{esc(alt)}" loading="lazy" width="1200" height="675">'
                   f'<figcaption><b>{esc(name)}</b>{esc(text)}</figcaption></figure></div>')
        css += (f'#mm-{key}:checked~.mm-surf__tabs label[for="mm-{key}"]'
                '{background:#FFF700;border-color:#FFF700;color:#000}'
                f'#mm-{key}:focus-visible~.mm-surf__tabs label[for="mm-{key}"]{{outline:2px solid #FFF700;outline-offset:3px}}'
                f'#mm-{key}:checked~.mm-surf__panels [data-surf="{key}"]{{display:block}}')
    inner = (f'<style>{css}</style><div class="mm-surf">{inputs}'
             f'<div class="mm-surf__tabs">{labels}</div><div class="mm-surf__panels">{panels}</div></div>')
    return ds.band(inner, 'Поверхности стенда и что на них шло',
                   esc('Состав мультимедиа стенда Самарской области на ВДНХ. Выберите поверхность, '
                       'чтобы увидеть кадр и содержание.'), kicker='Стенд Самарской области', dark=True,
                   fig='h')


def why():
    lead = ('Три причины, по которым экраны и интерактив мы рисуем вместе с конструктивом. Как это '
            'выглядит на реальном проекте, видно в <a href="/exhibition/#ex-case">разборе стенда '
            'Самарской области</a>. Экраны на плане появляются на стадии '
            '<a href="/exhibition/dizayn-stenda/">дизайна и проектирования стенда</a>.')
    return ds.band(ds.steps([(t, esc(d)) for t, d in WHY], cols=3),
                   'Почему мультимедиа закладывают в проект, а не вешают потом', lead, fig='disc')


def cases():
    items = [(href, title, text, img) for href, img, title, text, alt in CASES]
    return ds.sec(ds.cases(items, cols=3), 'Где это уже работает', icons=3, icon_start=5)


def price():
    return ds.sec(ds.cost('mm'), 'Стоимость и отзыв', alt=True)


def faq():
    return ds.sec(ds.faq(FAQ), 'Вопросы о мультимедиа на стенде')


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
    + rc.FONT + rc.CSS + ds.CSS + CSS + METRIKA + '</head><body>')


def page():
    body = (f'{rc.header()}<main class="hd" style="--a:{ds.EXH}">{crumbs()}{hero()}{banner()}{kinds()}'
            f'{surfaces()}{cases()}{why()}{price()}{faq()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'exhibition', 'multimedia')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
