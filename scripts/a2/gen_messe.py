#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/event/messeduessleldorf/index.html: кейс «Новый год Messe Düsseldorf».

Материал один: съёмка вечера, 15 кадров (лежали в галерее тильдовской
страницы). Ни видео, ни макетов, ни сметы по кейсу нет, год клиент просил
не ставить: было давно.

Идея страницы. Корпоратив прошёл не в ресторане, а в собственном офисе
компании, и на кадрах это видно в каждой детали: подвесной потолок,
люминесцентные светильники, ковролин, рабочие столы, роллап компании,
розетки в кабель-канале. Отсюда сюжет: не «сделали праздник», а
«переоборудовали рабочее помещение в площадку на четыре зоны».

  • «Растр знака» это главная механика, такой на сайте не было. Знак
    Messe Düsseldorf набран квадратами четырёх оттенков одной гаммы, и в том
    же модуле сделана карточка меню на столах. Мы взяли модуль как единицу
    страницы: каждый кадр разложен по сетке модулей, яркость куска кадра
    квантована в четыре тона знака (scripts/messe-assets.py), и кадр сперва
    показан фирменным узором клиента. Плитки переворачиваются и собирают
    из узора фотографию. Цвета плиток посчитаны из самого кадра, ничего
    не нарисовано руками.
  • Опись комнаты: две колонки «что стояло в офисе» против «чем это стало
    на вечер», обе сняты с кадров.
  • Страница идёт из дня в вечер: верх на светлом офисном фоне, ниже зоны
    и программа на тёмном.

Палитра снята с фотозоны алгоритмом: четыре краски знака стоят четырьмя
пиками по тону, медиана в каждой полосе и есть фирменный цвет.

Шрифты: Ubuntu (квадратноватый гротеск под модульную логику знака) + Scada.

Ассеты: mirror/images/messe/ (scripts/messe-assets.py).

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->. index-a2.html в каталоге кейса быть не должно: деплой
переименовал бы его в index.html и затёр кастомную страницу."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/messe'
URL = 'https://hand-marketing.ru/event/messeduessleldorf/'
TITLE = 'Новый год Messe Düsseldorf в офисе компании | Hand Marketing'
DESCR = ('Корпоративный Новый год Messe Düsseldorf Moscow в собственном офисе: '
         'рабочее помещение поделено на четыре зоны, фуршет, сцена, бар и зона '
         'шаржиста, программа с ведущим, фокусником и восточными танцами.')

MAP = json.load(open(os.path.join(HERE, 'messe_map.json'), encoding='utf-8'))
PALETTE = MAP['palette']
WHAT = MAP['photos']          # слаг → что в кадре (подписи из ассет-скрипта)

# ─── опись комнаты: (что стояло в офисе, чем стало на вечер, кадр) ──────────
# всё снято с кадров съёмки, ничего не додумано
ROOM = [
    ('Проектор и экран для совещаний', 'Экран официальной части: итоги года '
     'и слайды конкурсов', 'host'),
    ('Кирпичная арка в стене', 'Бар: стойка, кофемашина, линейка мохито, '
     'гирлянда-занавес в проёме', 'bar'),
    ('Стойка ресепшена', 'Выдача подарков: крафт-пакеты в ряд по всей стойке',
     'gifts'),
    ('Стеклянная перегородка со знаком компании', 'Фотозона: знак обведён '
     'гирляндой по периметру', 'photozone'),
    ('Рабочие столы и офисные кресла', 'Тихая зона: шаржист рисует гостей, '
     'рядом разговоры и бокалы', 'sketch'),
    ('Ковролин во всю комнату', 'Танцпол: без каблуков по нему танцевали '
     'и восточный номер', 'disco'),
    ('Стена с кабель-каналом и розетками', 'Питание звука и приборов заливки '
     'по всей длине стены', 'award'),
    ('Подвесной потолок с люминесцентными панелями', 'Держать оформление '
     'на нём нельзя: свет, шары и звук встали на стойки и в проёмы', 'fire'),
]

# ─── что приехало в офис: (группа, перечень) ───────────────────────────────
BROUGHT = [
    ('Звук и свет', 'две активные колонки на стойках, приборы заливки, '
     'два зеркальных шара, пульт у сцены'),
    ('Фуршет', 'линия вдоль стены: мармиты на подогреве, ассорти закусок '
     'и салатов, горячее с гарнирами, десерт'),
    ('Бар', 'барная станция в арке, посуда, коктейльная карта, '
     'мохито партиями по десять стаканов'),
    ('Оформление', 'красный текстиль со стойкой до пола, гирлянды-занавесы, '
     'ватные шары, ёлочные шары в бокалах, свечи, карточки меню'),
    ('Подарки', 'крафт-пакеты по числу сотрудников, выставлены на стойке '
     'ресепшена до прихода гостей'),
    ('Люди', 'ведущий, фокусник, танцовщица, шаржист, бармены, официанты, '
     'фотограф'),
]

# ─── четыре зоны: (слаг растра, номер, имя, описание) ──────────────────────
ZONES = [
    ('bufet', '01', 'Фуршетная линия',
     'Вдоль кирпичной стены: мармиты на подогреве, ассорти рыбы и мяса, '
     'салаты, горячее. Линия поставлена так, чтобы очередь шла вдоль стены '
     'и не резала комнату пополам.'),
    ('host', '02', 'Сцена и экран',
     'Официальная часть и развлекательная работали на одном пятне: экран '
     'проектора, колонки по краям, свободный пол перед ним. Ведущий вечера '
     'актёр Никита Тарасов.'),
    ('bar', '03', 'Бар в арке',
     'Кирпичный проём оказался готовой барной стойкой: бармены за ней, '
     'гирлянда-занавес позади, мохито собирают партиями заранее.'),
    ('sketch', '04', 'Тихая зона',
     'Дальний угол с рабочими столами и креслами: шаржист рисует гостей, '
     'рядом можно сесть и поговорить, не перекрикивая музыку.'),
]

# ─── программа вечера: (кадр, заголовок, текст) ────────────────────────────
PROGRAM = [
    ('award', 'Официальная часть', 'Итоги года, слова руководства, вручение '
     'подарков. Ведущий работает без сцены и подиума, прямо в комнате.'),
    ('cards', 'Фокусник: карты', 'Микромагия в кругу гостей, без реквизитной '
     'сцены и без ассистента.'),
    ('fire', 'Фокусник: огонь', 'Второй выход на столике посреди зала. '
     'Открытый огонь в офисе делает только артист и только на своём столе.'),
    ('dance-red', 'Восточный танец', 'Первый выход с веерами-вейлами '
     'в красно-чёрном костюме.'),
    ('dance-blue', 'Второй выход', 'Смена костюма на бирюзовый, продолжение '
     'номера уже под зеркальным шаром.'),
    ('sketch', 'Шаржист', 'Работает весь вечер: гость садится напротив '
     'и уходит с портретом.'),
    ('disco', 'Дискотека', 'Финал вечера: пиджаки сняты, галстуки ослаблены, '
     'танцуют на офисном ковролине.'),
]

# ─── галерея: порядок показа ───────────────────────────────────────────────
GALLERY = ['bufet', 'gifts', 'photozone', 'menu', 'host', 'talk', 'sketch',
           'portrait', 'award', 'cards', 'fire', 'bar', 'dance-red',
           'dance-blue', 'disco']


CSS = """<style id="mz-css">
/* Кейс «Новый год Messe Düsseldorf». Модуль знака клиента как единица
   страницы: сетка, плитки растра, отбивки. Правки только в gen_messe.py. */
.mz{--t0:%T0%;--t1:%T1%;--t2:%T2%;--t3:%T3%;
 --day:#F1EFEC;--paper:#FFFFFF;--ink:#191713;--mute:#6E6862;
 --night:#141210;--night2:#1E1A16;--line:rgba(25,23,19,.12);--lineN:rgba(255,255,255,.14);
 font-family:'Scada',Arial,sans-serif;color:var(--ink);background:var(--day);
 font-size:17px;line-height:1.62;overflow-x:hidden}
.mz *,.mz *::before,.mz *::after{box-sizing:border-box}
.mz h1,.mz h2,.mz h3,.mz .u{font-family:'Ubuntu',Arial,sans-serif}
.mz p{margin:0 0 16px}
.mz section{padding:84px 40px}
.mz .in{max-width:1180px;margin:0 auto}
.mz .lbl{font-family:'Ubuntu',Arial,sans-serif;font-weight:700;font-size:12px;
 letter-spacing:.18em;text-transform:uppercase;color:var(--t1);margin:0 0 18px}
.mz h2{font-size:clamp(28px,4.2vw,48px);font-weight:700;line-height:1.08;margin:0 0 22px;
 letter-spacing:-.01em}
.mz .lead{font-size:clamp(17px,1.7vw,21px);line-height:1.55;max-width:760px;color:var(--mute)}
.mz .night{background:var(--night);color:#EDE7E1}
.mz .night .lead,.mz .night .mute{color:rgba(237,231,225,.62)}
.mz .night h2,.mz .night h3{color:#fff}

/* ── растр знака: плитка модуля переворачивается и открывает кадр ────────
   Фотография лежит под сеткой целиком, плитки закрывают её лицевой гранью
   и уходят по rotateY. Так у собранного кадра нет швов между плитками:
   картинка одна, а не 600 кусков фона. */
.mz-rst{position:relative;display:grid;grid-template-columns:repeat(var(--c),1fr);
 width:100%;aspect-ratio:var(--c)/var(--r);overflow:hidden;background:var(--t0)}
.mz-rst>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.mz-rst i{position:relative;display:block;aspect-ratio:1;transform-style:preserve-3d;
 transition:transform .5s cubic-bezier(.35,0,.2,1);transition-delay:calc(var(--d)*1ms)}
.mz-rst.on i{transform:rotateY(180deg)}
.mz-rst i::before{content:"";position:absolute;inset:-.5px;background:var(--t);
 -webkit-backface-visibility:hidden;backface-visibility:hidden}
/* без 3d (старый webkit): плитка не переворачивается, а растворяется */
.mz-rst.flat i{transform:none!important}
.mz-rst.flat i::before{transition:opacity .5s;transition-delay:calc(var(--d)*1ms)}
.mz-rst.flat.on i::before{opacity:0}
/* пока JS не разложил плитки, виден просто кадр */
.mz-shot{position:relative}
.mz-shot__cap{margin-top:10px;font-size:13px;line-height:1.45;color:var(--mute)}
.mz-tog{position:absolute;right:12px;bottom:12px;z-index:3;border:0;cursor:pointer;
 font:700 12px/1 'Ubuntu',Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;
 padding:11px 16px;border-radius:2px;background:rgba(20,18,16,.72);color:#fff;
 backdrop-filter:blur(6px);transition:background .2s}
.mz-tog:hover{background:var(--t2)}

/* ── обложка ────────────────────────────────────────────────────────────── */
.mz-hero{padding:0 0 0;background:var(--paper)}
.mz-hero__top{max-width:1180px;margin:0 auto;padding:46px 40px 34px}
.mz-back{display:inline-block;font-size:14px;color:var(--mute);text-decoration:none;margin-bottom:26px}
.mz-back:hover{color:var(--t1)}
.mz-hero h1{font-size:clamp(34px,6vw,74px);line-height:1.02;font-weight:700;margin:0 0 20px;
 letter-spacing:-.02em}
.mz-hero .lead{font-size:clamp(17px,1.9vw,23px);color:var(--mute)}
.mz-hero__grid{max-width:1180px;margin:0 auto;padding:0 40px 0;display:grid;
 grid-template-columns:1fr;gap:0}
.mz-hero__facts{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);
 border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:34px}
.mz-hero__facts div{background:var(--paper);padding:22px 20px}
.mz-hero__facts b{display:block;font:700 15px/1.3 'Ubuntu',Arial,sans-serif;margin-bottom:5px}
.mz-hero__facts span{font-size:14px;color:var(--mute);line-height:1.45}

/* ── клиент и задача ────────────────────────────────────────────────────── */
.mz-brief{display:grid;grid-template-columns:1fr 1fr;gap:56px}
.mz-brief h3{font-size:20px;font-weight:700;margin:0 0 12px}
.mz-brief .col p:last-child{margin-bottom:0}

/* ── опись комнаты ──────────────────────────────────────────────────────── */
.mz-room__head{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:0 0 12px;
 border-bottom:2px solid var(--ink)}
.mz-room__head span{font:700 12px/1 'Ubuntu',Arial,sans-serif;letter-spacing:.16em;
 text-transform:uppercase;color:var(--mute)}
.mz-room__row{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:20px 0;
 border-bottom:1px solid var(--line);cursor:default;transition:background .18s}
.mz-room__row:hover{background:rgba(230,93,2,.055)}
.mz-room__was{font-weight:700}
.mz-room__is{color:var(--mute);position:relative;padding-left:26px}
.mz-room__is::before{content:"";position:absolute;left:0;top:11px;width:14px;height:2px;
 background:var(--t2)}
.mz-room__row:hover .mz-room__is{color:var(--ink)}
.mz-room__pic{margin-top:34px;display:grid;grid-template-columns:2fr 1fr;gap:24px;align-items:start}
.mz-room__pic img{width:100%;height:100%;object-fit:cover;display:block;border-radius:2px}
.mz-room__note{font-size:14px;color:var(--mute);line-height:1.55}

/* ── что привезли ───────────────────────────────────────────────────────── */
.mz-br{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--lineN);
 border:1px solid var(--lineN);margin-top:34px}
.mz-br div{background:var(--night);padding:26px 24px}
.mz-br b{display:block;font:700 13px/1 'Ubuntu',Arial,sans-serif;letter-spacing:.12em;
 text-transform:uppercase;color:var(--t3);margin-bottom:12px}
.mz-br span{font-size:15px;line-height:1.6;color:rgba(237,231,225,.78)}

/* ── зоны ───────────────────────────────────────────────────────────────── */
.mz-zones{display:grid;grid-template-columns:1fr 1fr;gap:38px;margin-top:38px}
.mz-zone__num{font:700 12px/1 'Ubuntu',Arial,sans-serif;letter-spacing:.16em;color:var(--t3)}
.mz-zone h3{font-size:24px;font-weight:700;margin:10px 0 10px}
.mz-zone p{font-size:15.5px;line-height:1.6;color:rgba(237,231,225,.72);margin:0}
.mz-zone .mz-shot{margin-bottom:18px}
.mz-zone .mz-tog{opacity:0;transition:opacity .2s,background .2s}
.mz-zone .mz-shot:hover .mz-tog,.mz-zone .mz-tog:focus-visible{opacity:1}
@media(hover:none){.mz-zone .mz-tog{opacity:1}}

/* ── программа ──────────────────────────────────────────────────────────── */
.mz-prog{display:grid;grid-template-columns:repeat(3,1fr);gap:30px 26px;margin-top:38px}
.mz-prog__it img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;border-radius:2px;
 margin-bottom:14px}
.mz-prog__it h3{font-size:20px;font-weight:700;margin:0 0 8px}
.mz-prog__it p{font-size:15px;line-height:1.58;color:rgba(237,231,225,.72);margin:0}
.mz-prog__it.wide{grid-column:1/-1;border-top:1px solid var(--lineN);padding-top:30px}
.mz-prog__it.wide img{aspect-ratio:21/9;margin-bottom:18px}
.mz-prog__it.wide>div{display:grid;grid-template-columns:1fr 1.6fr;gap:28px;align-items:baseline}
.mz-prog__it.wide h3{font-size:28px;margin:0}
.mz-prog__it.wide p{font-size:16.5px}

/* ── фирменный модуль ───────────────────────────────────────────────────── */
.mz-mod{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;margin-top:34px}
.mz-mod img{width:100%;display:block;border-radius:2px}
.mz-pal{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin:26px 0 22px;
 background:var(--lineN)}
.mz-pal div{padding:52px 10px 12px;font:700 12px/1 'Ubuntu',Arial,sans-serif;color:#fff;
 letter-spacing:.06em}
.mz-mod__pics{display:grid;gap:18px}
.mz-mod figure{margin:0}
.mz-mod figcaption{margin-top:9px;font-size:13.5px;line-height:1.5;color:rgba(237,231,225,.62)}

/* ── галерея ────────────────────────────────────────────────────────────── */
.mz-gal{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:34px}
.mz-gal button{padding:0;border:0;background:none;cursor:zoom-in;display:block;line-height:0}
.mz-gal img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;border-radius:2px;
 transition:transform .3s,filter .3s;filter:saturate(.92)}
.mz-gal button:hover img{transform:scale(1.02);filter:saturate(1.06)}
.mz-lb{position:fixed;inset:0;z-index:9999;background:rgba(12,10,9,.94);display:none;
 align-items:center;justify-content:center;padding:32px}
.mz-lb.on{display:flex}
.mz-lb img{max-width:94vw;max-height:82vh;object-fit:contain;border-radius:2px}
.mz-lb__cap{position:absolute;left:0;right:0;bottom:22px;text-align:center;font-size:14px;
 color:rgba(255,255,255,.72);padding:0 24px}
.mz-lb__x,.mz-lb__n,.mz-lb__p{position:absolute;border:0;background:rgba(255,255,255,.12);
 color:#fff;cursor:pointer;width:46px;height:46px;border-radius:50%;font:700 20px/1 'Ubuntu',Arial,sans-serif}
.mz-lb__x{top:20px;right:20px}
.mz-lb__p{left:20px;top:calc(50% - 23px)}
.mz-lb__n{right:20px;top:calc(50% - 23px)}
.mz-lb__x:hover,.mz-lb__n:hover,.mz-lb__p:hover{background:var(--t2)}

/* ── адаптив ────────────────────────────────────────────────────────────── */
@media(max-width:1024px){
 .mz section{padding:72px 28px}
 .mz-hero__top{padding:38px 28px 28px}
 .mz-hero__grid{padding:0 28px}
 .mz-brief{gap:34px}
 .mz-prog{grid-template-columns:repeat(2,1fr)}
 .mz-br{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:760px){
 .mz{font-size:16px}
 .mz section{padding:54px 18px}
 .mz-hero__top{padding:26px 18px 22px}
 .mz-hero__grid{padding:0 18px}
 .mz-hero__facts{grid-template-columns:1fr 1fr}
 .mz-brief,.mz-zones,.mz-mod{grid-template-columns:1fr;gap:28px}
 .mz-room__head,.mz-room__row{grid-template-columns:1fr;gap:6px}
 .mz-room__row{padding:15px 0}
 .mz-room__pic{grid-template-columns:1fr}
 .mz-br{grid-template-columns:1fr}
 .mz-prog{grid-template-columns:1fr;gap:26px}
 .mz-prog__it.wide>div{grid-template-columns:1fr;gap:8px}
 .mz-prog__it.wide img{aspect-ratio:3/2}
 .mz-gal{grid-template-columns:1fr 1fr;gap:10px}
 .mz-pal div{padding:40px 8px 10px;font-size:11px}
 .mz-lb{padding:16px}
 .mz-lb img{max-width:92vw;max-height:74vh}
 .mz-lb__p{left:10px}.mz-lb__n{right:10px}
}
@media(max-height:460px) and (orientation:landscape){
 .mz section{padding:42px 22px}
 .mz-hero h1{font-size:34px}
 .mz-lb img{max-height:68vh}
}
@media(prefers-reduced-motion:reduce){
 .mz-rst i{transition-duration:.01ms;transition-delay:0ms!important}
 .mz-gal img{transition:none}
}
</style>"""
for i, c in enumerate(PALETTE):
    CSS = CSS.replace('%T{}%'.format(i), c)


def pic(slug, sizes, cls='', extra=''):
    """<img> кадра в трёх размерах: браузер берёт нужный по ширине места."""
    a = WHAT.get(slug, '')
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="{IMG}/{slug}-s.jpg" '
            f'srcset="{IMG}/{slug}-s.jpg 640w, {IMG}/{slug}-m.jpg 1000w, '
            f'{IMG}/{slug}.jpg 1200w" sizes="{sizes}" alt="{a}" '
            f'loading="lazy" decoding="async"{extra}>')


def rst(slug, cap=None, tog='собрать кадр', sizes='(max-width:1240px) 100vw, 1100px'):
    """Полотно растра: сетка модулей знака, которая переворачивается в кадр.
    Внутри лежит сама фотография: пока JS не построил плитки (или если он
    выключен), виден просто кадр."""
    g = MAP['grids'][slug]
    b = (f'<button class="mz-tog" type="button" data-tog="{slug}">{tog}</button>'
         if tog else '')
    c = f'<div class="mz-shot__cap">{cap}</div>' if cap else ''
    return (f'<div class="mz-shot"><div class="mz-rst nojs" data-slug="{slug}" '
            f'style="--c:{g["cols"]};--r:{g["rows"]};--img:url({IMG}/{slug}.jpg)">'
            + pic(slug, sizes) + f'</div>{b}{c}</div>')


def hero():
    facts = [
        ('Площадка', 'Собственный офис компании, без переезда в ресторан'),
        ('Зоны', 'Фуршет, сцена с экраном, бар в арке, тихая зона'),
        ('Программа', 'Ведущий, фокусник, восточный танец, шаржист, дискотека'),
        ('Оформление', 'В фирменном модуле клиента, вплоть до карточек меню'),
    ]
    f = ''.join(f'<div><b>{t}</b><span>{d}</span></div>' for t, d in facts)
    return (
      '<section class="mz-hero"><div class="mz-hero__top">'
      '<a class="mz-back" href="/project">← Все проекты</a>'
      '<div class="lbl">Event · Messe Düsseldorf Moscow</div>'
      '<h1>Новый год в собственном офисе</h1>'
      '<p class="lead">Компания решила встретить Новый год не в ресторане, '
      'а у себя: в тех же комнатах, где сотрудники работают каждый день. '
      'Мы поделили офис на четыре зоны, собрали в нём фуршет, сцену и бар '
      'и вернули помещение в рабочий вид.</p>'
      '</div><div class="mz-hero__grid">'
      + rst('disco', 'Финал вечера на офисном ковролине. Нажмите «рассыпать», '
            'чтобы увидеть модуль знака, из которого собран кадр.',
            'рассыпать в модуль')
      + f'<div class="mz-hero__facts">{f}</div>'
      '</div></section>')


def brief():
    return (
      '<section><div class="in mz-brief">'
      '<div class="col"><div class="lbl">Компания</div>'
      '<h3>Messe Düsseldorf</h3>'
      '<p>Организатор примерно 80 выставок по всему миру, они закрывают '
      'практически все отрасли экономики. В России компания работает '
      'с 1963 года: тогда она привезла официальную делегацию Германии '
      'на международную выставку «Химия», приехав по приглашению '
      'Торгово-промышленной палаты СССР.</p>'
      '<p>Московский офис небольшой, и корпоратив здесь это встреча людей, '
      'которые весь год сидят в соседних кабинетах.</p></div>'
      '<div class="col"><div class="lbl">Задача</div>'
      '<h3>Праздник там, где рабочие места</h3>'
      '<p>Провести корпоративный Новый год в стенах офиса. Это значит '
      'не «украсить кабинет», а на один вечер сменить назначение помещения: '
      'развести потоки людей, накрыть фуршет, поставить звук и свет, '
      'найти место бару и артистам.</p>'
      '<p>Ограничения задавала сама комната. Подвесной потолок ничего '
      'не держит, свет в нём люминесцентный и его не перекрасить, '
      'сверлить стены нельзя, а к утру офис должен снова работать.</p>'
      '</div></div></section>')


def room():
    rows = ''.join(
        f'<div class="mz-room__row"><div class="mz-room__was">{was}</div>'
        f'<div class="mz-room__is">{now}</div></div>' for was, now, _s in ROOM)
    return (
      '<section><div class="in">'
      '<div class="lbl">Инвентаризация</div>'
      '<h2>Что в комнате уже было</h2>'
      '<p class="lead">Перед тем как что-то везти, мы разобрали офис '
      'по предметам. Половина площадки собралась из того, что и так стояло '
      'на своих местах: проёмы, стойки, техника и мебель просто получили '
      'на вечер другое назначение.</p>'
      f'<div class="mz-room__head"><span>Было в офисе</span>'
      f'<span>Стало на вечер</span></div>{rows}'
      '<div class="mz-room__pic">'
      + pic('sketch', '(max-width:760px) 100vw, (max-width:1180px) 62vw, 720px') +
      '<div class="mz-room__note"><p>Кадр из тихой зоны: рабочие столы, '
      'офисные кресла и роллап компании остались на местах, к ним просто '
      'подсели гости и шаржист.</p>'
      '<p>Это и есть главная особенность площадки. Офис не притворяется '
      'банкетным залом: кирпич, ковролин и подвесной потолок видно на каждом '
      'кадре, и оформление работает вместе с ними, а не поверх них.</p>'
      '</div></div></div></section>')


def brought():
    items = ''.join(f'<div><b>{g}</b><span>{d}</span></div>' for g, d in BROUGHT)
    return (
      '<section class="night"><div class="in">'
      '<div class="lbl">Завоз</div>'
      '<h2>Что приехало в офис</h2>'
      '<p class="lead">Всё остальное привезли и поставили за несколько часов '
      'после рабочего дня. Ничего не крепится к потолку и не сверлится '
      'в стены: звук и свет стоят на стойках, гирлянды заходят в проёмы '
      'и по периметру перегородок, питание идёт от розеток в кабель-канале.</p>'
      f'<div class="mz-br">{items}</div>'
      '</div></section>')


def zones():
    cards = ''
    for slug, num, name, text in ZONES:
        sizes = '(max-width:760px) 100vw, (max-width:1180px) 46vw, 560px'
        cards += ('<div class="mz-zone">' + rst(slug, None, 'собрать кадр', sizes)
                  + f'<div class="mz-zone__num">{num}</div>'
                  f'<h3>{name}</h3><p>{text}</p></div>')
    return (
      '<section class="night"><div class="in">'
      '<div class="lbl">Планировка</div>'
      '<h2>Четыре зоны в одной комнате</h2>'
      '<p class="lead">Зоны расставлены по кругу так, чтобы они не мешали '
      'друг другу: пока у экрана идёт официальная часть, у бара можно '
      'разговаривать, а очередь на фуршете не пересекает пятно перед сценой.</p>'
      f'<div class="mz-zones">{cards}</div>'
      '</div></section>')


def program():
    it = ''
    for n, (slug, title, text) in enumerate(PROGRAM):
        wide = ' wide' if n == len(PROGRAM) - 1 else ''
        shot = pic(slug, '(max-width:760px) 100vw, (max-width:1180px) 48vw, 380px')
        body = f'<div><h3>{title}</h3><p>{text}</p></div>'
        it += f'<div class="mz-prog__it{wide}">{shot}{body}</div>'
    return (
      '<section class="night"><div class="in">'
      '<div class="lbl">Программа</div>'
      '<h2>Вечер по номерам</h2>'
      '<p class="lead">Программа собрана так, чтобы каждый номер работал '
      'в комнате без сцены: артист выходит на свободный пол, гости стоят '
      'вокруг, а не сидят рядами.</p>'
      f'<div class="mz-prog">{it}</div>'
      '</div></section>')


def module():
    pal = ''.join(f'<div style="background:{c}">{c}</div>' for c in PALETTE)
    return (
      '<section class="night"><div class="in">'
      '<div class="lbl">Фирменный модуль</div>'
      '<h2>Знак клиента как единица оформления</h2>'
      '<p class="lead">Знак Messe Düsseldorf набран квадратами: одна форма, '
      'четыре оттенка одной оранжево-красной гаммы. В том же модуле сделана '
      'карточка меню на столах, то есть графику вечера задал сам клиент, '
      'а мы её продолжили.</p>'
      '<div class="mz-mod"><div>'
      f'<div class="mz-pal">{pal}</div>'
      '<p class="mute">Четыре тона сняты с кадра фотозоны, а не подобраны '
      'на глаз: краски знака стоят четырьмя пиками по тону, и медиана '
      'в каждой полосе даёт фирменный цвет. Блики гирлянды и тени в расчёт '
      'не идут.</p>'
      '<p class="mute">Кадры на этой странице разложены по тому же модулю. '
      'Цвет плитки это яркость своего куска кадра, приведённая к четырём '
      'тонам знака: сначала фотография выглядит фирменным узором клиента, '
      'потом плитки переворачиваются и собирают снимок.</p>'
      + rst('photozone', 'Фотозона: знак на стеклянной перегородке, обведённый '
            'гирляндой.', 'собрать кадр',
            '(max-width:760px) 100vw, (max-width:1180px) 46vw, 560px') +
      '</div><div class="mz-mod__pics">'
      f'<figure><img src="{IMG}/sign.jpg" alt="Знак Messe Düsseldorf Moscow, '
      'набранный квадратами четырёх оттенков" loading="lazy" decoding="async">'
      '<figcaption>Знак на перегородке: модуль виден без увеличения, '
      'каждый квадрат это один шаг сетки.</figcaption></figure>'
      f'<figure><img src="{IMG}/menu-card.jpg" alt="Карточка меню в фирменной '
      'пиксельной рамке" loading="lazy" decoding="async">'
      '<figcaption>Карточка меню на столе: рамка набрана тем же модулем, '
      'знак стоит в нижнем углу.</figcaption></figure>'
      '</div></div></div></section>')


def gallery():
    g = ''.join(
        f'<button type="button" data-i="{i}">'
        + pic(s, '(max-width:760px) 50vw, (max-width:1180px) 32vw, 380px')
        + '</button>' for i, s in enumerate(GALLERY))
    return (
      '<section class="night"><div class="in">'
      '<div class="lbl">Съёмка</div>'
      '<h2>Как это выглядело</h2>'
      f'<div class="mz-gal">{g}</div></div>'
      '<div class="mz-lb" id="mzlb" role="dialog" aria-modal="true" aria-label="Фотография">'
      '<button class="mz-lb__x" type="button" aria-label="Закрыть">×</button>'
      '<button class="mz-lb__p" type="button" aria-label="Предыдущая">‹</button>'
      '<button class="mz-lb__n" type="button" aria-label="Следующая">›</button>'
      '<img src="" alt=""><div class="mz-lb__cap"></div></div>'
      '</section>')


PAGE_JS = """<script>(function(){
var GRIDS=%GRIDS%,PAL=%PAL%,GAL=%GAL%,IMG='%IMG%';
var FLAT=!(window.CSS&&CSS.supports&&CSS.supports('transform-style','preserve-3d'));
// разложить полотно на плитки модуля: цвет плитки уже посчитан ассет-скриптом,
// здесь только раскладка и позиция куска кадра на обороте
function build(el){
  var g=GRIDS[el.getAttribute('data-slug')];if(!g||el.getAttribute('data-built'))return;
  var c=g.cols,r=g.rows,f=document.createDocumentFragment(),x,y,row,i;
  for(y=0;y<r;y++){row=g.rowsData[y];
    for(x=0;x<c;x++){i=document.createElement('i');
      i.style.setProperty('--t',PAL[+row.charAt(x)]);
      i.style.setProperty('--d',(x+y)*14);
      f.appendChild(i);}}
  el.appendChild(f);el.setAttribute('data-built','1');
  if(FLAT)el.classList.add('flat');
}
function label(b,on){if(b)b.textContent=on?'рассыпать в модуль':'собрать кадр';}
function setOn(el,on){
  el.classList.toggle('on',on);
  var b=el.parentNode.querySelector('.mz-tog');label(b,on);
}
var nodes=[].slice.call(document.querySelectorAll('.mz-rst'));
nodes.forEach(build);
// кадр собирается сам, когда полотно попадает в экран
if(window.IntersectionObserver){
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting&&!e.target.getAttribute('data-touched')){
        e.target.setAttribute('data-touched','1');
        setTimeout(function(){setOn(e.target,true);},700);
        io.unobserve(e.target);}});},{threshold:.25});
  nodes.forEach(function(n){io.observe(n);});
}else{nodes.forEach(function(n){setOn(n,true);});}
document.addEventListener('click',function(e){
  var b=e.target.closest?e.target.closest('.mz-tog'):null;if(!b)return;
  var el=b.parentNode.querySelector('.mz-rst');if(!el)return;
  el.setAttribute('data-touched','1');setOn(el,!el.classList.contains('on'));
});
// галерея
var lb=document.getElementById('mzlb');
if(lb){
  var im=lb.querySelector('img'),cp=lb.querySelector('.mz-lb__cap'),cur=0;
  function show(i){cur=(i+GAL.length)%GAL.length;
    im.src=IMG+'/'+GAL[cur][0]+'.jpg';im.alt=GAL[cur][1];cp.textContent=GAL[cur][1];}
  function open(i){show(i);lb.classList.add('on');document.body.style.overflow='hidden';}
  function close(){lb.classList.remove('on');document.body.style.overflow='';}
  [].slice.call(document.querySelectorAll('.mz-gal button')).forEach(function(b){
    b.addEventListener('click',function(){open(+b.getAttribute('data-i'));});});
  lb.querySelector('.mz-lb__x').addEventListener('click',close);
  lb.querySelector('.mz-lb__n').addEventListener('click',function(e){e.stopPropagation();show(cur+1);});
  lb.querySelector('.mz-lb__p').addEventListener('click',function(e){e.stopPropagation();show(cur-1);});
  lb.addEventListener('click',function(e){if(e.target===lb||e.target===im)close();});
  document.addEventListener('keydown',function(e){
    if(!lb.classList.contains('on'))return;
    if(e.key==='Escape')close();
    if(e.key==='ArrowRight')show(cur+1);
    if(e.key==='ArrowLeft')show(cur-1);});
}
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Event","item":"https://hand-marketing.ru/event/"},'
  '{"@type":"ListItem","position":3,"name":"Новый год Messe Düsseldorf",'
  f'"item":"{URL}"}}]}}</script>')

HEAD = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<!--custom-page-->'
        f'<title>{TITLE}</title>'
        f'<meta name="description" content="{DESCR}">'
        '<meta name="robots" content="index, follow">'
        f'<link rel="canonical" href="{URL}">'
        '<meta property="og:type" content="article">'
        f'<meta property="og:title" content="{TITLE}">'
        f'<meta property="og:description" content="{DESCR}">'
        f'<meta property="og:url" content="{URL}">'
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/photozone.jpg">'
        '<link rel="stylesheet" href="/fonts/ubuntu-scada.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    gal = [[s, WHAT.get(s, '')] for s in GALLERY]
    js = (PAGE_JS.replace('%GRIDS%', json.dumps(MAP['grids'], ensure_ascii=False))
                 .replace('%PAL%', json.dumps(PALETTE))
                 .replace('%GAL%', json.dumps(gal, ensure_ascii=False))
                 .replace('%IMG%', IMG))
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="mz">{hero()}{brief()}{room()}{brought()}'
            f'{zones()}{program()}{module()}{gallery()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}'
            '</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'event', 'messeduessleldorf')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
