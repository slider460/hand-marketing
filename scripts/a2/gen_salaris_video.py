#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/salaris/index.html: кейс «Ролики МФК „Саларис“».

Идея страницы. Роликов два, и это не две версии одного, а два разных
доказательства об одном объекте, снятые с разницей в полгода:

  • salaris-1.mp4 (2:58, зима 2018) — про ОБЪЕКТ. Центра ещё нет: аэросъёмка
    стройплощадки, будущее здание собрано графикой по существующей модели и
    вписано в натурный кадр. Дальше метры, транспортный узел, пул арендаторов.
  • salaris-2.mp4 (2:33, лето-осень 2018) — про АУДИТОРИЮ. Ни одного крана:
    готовое здание, зона охвата изохронами, демография, интервью у метро,
    подводка к открытию 1 марта 2019.

Общего у роликов шесть кусков (заставка, метры, метро с автобусами, пул
брендов, слоган, титр команды) — одни и те же цифры звучат сначала как
обещание стройки, потом как факт. Отсюда главный экран страницы.

Три механики, которых на сайте не было:
  • «Две дорожки» — хронометражи обоих роликов рядом, сегмент к сегменту;
    общие куски связаны дугами между дорожками, клик по сегменту переключает
    источник в плеере и перематывает на эту секунду.
  • «Зона охвата» — карта из второго ролика, снятая контурами с кадров
    (scripts/salaris-video-assets.py, данные в salaris_video_map.json):
    зона 20 минут, станции метро 2019, трасса Солнцево-Бутово-Видное и
    зона 30 минут, население набегает счётчиком 2 млн → 3,5 млн.
  • «105 000 м² в масштабе» — арендопригодная площадь квадратом, якорные
    арендаторы занимают в нём свою настоящую долю по метражу из ролика.

Цифры и названия сняты с экранных плашек обоих роликов, ничего не додумано.
Палитра снята пипеткой с заставки: индиго #440099, оранжевый луч, жёлтые
плашки титров. Жёлтая плашка — сквозной приём страницы: так набраны все
экранные подписи в обоих роликах.

Ассеты: mirror/images/salaris-video/ + шрифты (scripts/salaris-video-assets.py).

НЕ публикуем: лица респондентов крупным планом как иллюстрацию к цифрам
демографии (кадры интервью идут отдельным блоком, как съёмка, а не как
«портрет покупателя»), имена сотрудников клиента.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/salaris-video'
V1 = '/media/salaris-1.mp4'    # источник: scripts/a2/video_map.json
V2 = '/media/salaris-2.mp4'
URL = 'https://hand-marketing.ru/video/salaris/'
MAP = json.load(open(os.path.join(HERE, 'salaris_video_map.json'), encoding='utf-8'))

DUR1, DUR2 = 178.4, 152.9      # хронометражи из ffprobe

# ─── сегменты роликов: (старт, конец, метка, тег темы, что внутри) ──────────
# tag общий у кусков, которые есть в обоих роликах: по нему рисуются дуги
FILMS = [
    {
        'n': 1, 'src': V1, 'dur': DUR1, 'poster': f'{IMG}/poster-1.jpg',
        'title': 'Объект', 'sub': 'зима 2018, стройка',
        'note': 'Съёмка дроном и операторами, здание собрано графикой.',
        'segs': [
            (0, 4, 'Знак', 'logo', 'Заставка: солнце и слово «саларис».'),
            (4, 12, 'Здание графикой', 'cg',
             'Будущий комплекс собран по существующей 3D-модели и вписан в '
             'зимний натурный кадр.'),
            (12, 32, 'Транспортный узел', 'node',
             'Схема подъездов и парковок нарисована прямо поверх плана площадки.'),
            (32, 56, 'Метро и автобусы', 'flow',
             'До 250 автобусов в час, 64 000 человек в день на выходе из метро.'),
            (56, 70, 'Neopolis', 'office',
             'Деловой квартал по соседству: 5 500 офисных сотрудников.'),
            (70, 94, 'Жильё вокруг', 'homes',
             '«Саларьево Парк» и соседние корпуса, 1 500 000 м² жилья к 2020 году.'),
            (94, 106, 'Карта района', 'homes',
             'Десять жилых комплексов вокруг, прирост 195 000 человек к 2019 году.'),
            (106, 120, 'Метры', 'metrics',
             '310 000 м² общая площадь, 105 000 м² аренды, 5 000 машиномест.'),
            (120, 130, 'Стройка', 'build',
             'Состояние площадки на момент съёмки: плита, каркас, краны.'),
            (130, 162, 'Арендаторы', 'tenants',
             'Якоря с площадями: Globus, Синема Парк, Спортмастер, Reserved и другие.'),
            (162, 172, 'Слоган', 'slogan', '«Солнце в каждом из нас».'),
            (172, DUR1, 'Команда', 'team',
             'Титр: девелопер, управление, генподряд, проектировщик, архитектор.'),
        ],
    },
    {
        'n': 2, 'src': V2, 'dur': DUR2, 'poster': f'{IMG}/poster-2.jpg',
        'title': 'Аудитория', 'sub': 'лето-осень 2018, здание готово',
        'note': 'Съёмка в готовом центре плюс интервью у метро.',
        'segs': [
            (0, 4, 'Знак', 'logo', 'Та же заставка, что и в первом ролике.'),
            (4, 8, 'Где это', 'geo',
             'Точка на карте Москвы: Киевское шоссе между МКАД и Внуково.'),
            (8, 14, 'Метры', 'metrics',
             'Те же 310 000 м² и 5 000 мест, но уже как факт: 290 магазинов.'),
            (14, 24, 'Метро и автобусы', 'flow',
             'Трафик выхода из метро 70 000, 280 автобусных маршрутов в час.'),
            (24, 44, 'Зона охвата', 'reach',
             'Изохроны 0–5, 5–10, 10–15, 15–20, 20–30 минут: 2 млн человек.'),
            (44, 58, 'Новая трасса', 'reach',
             'Солнцево-Бутово-Видное, подъезд к МФК и станции метро 2019 года.'),
            (58, 66, 'Настроение', 'mood',
             'Индекс потребительской уверенности +8 против −11 в 2017 году.'),
            (66, 86, 'Что уже работает', 'tenants',
             'Галерея открытого центра: одежда, спорт, кино, детские форматы.'),
            (86, 100, 'Кто эти люди', 'people',
             'Возраст, семьи, доход: срез жителей зоны охвата.'),
            (100, 128, 'Интервью у метро', 'people',
             'Репортёры спрашивают у выхода из метро, чего людям не хватает.'),
            (128, 140, 'Открытие', 'open',
             '60 000 гостей в день открытия, 10 000 подписчиков в соцсетях.'),
            (140, 148, 'Слоган', 'slogan', 'Тот же финал и дата: 1 марта 2019 года.'),
            (148, DUR2, 'Команда', 'team', 'Тот же титр команды проекта.'),
        ],
    },
]

# темы, встречающиеся в обоих роликах: заголовок дуги
SHARED = {
    'logo': 'Заставка',
    'metrics': 'Метры объекта',
    'flow': 'Метро и автобусы',
    'tenants': 'Бренды',
    'slogan': 'Слоган',
    'team': 'Команда проекта',
}

# ─── что снимали и зачем ────────────────────────────────────────────────────
BRIEF = [
    ('Показать объект, которого нет',
     'К началу работы центр был на стадии котлована и каркаса. Здание для '
     'кадра собрали графикой по существующей модели и вписали в натурную '
     'съёмку площадки.'),
    ('Снять натуру с воздуха и с земли',
     'Дрон над площадкой и вокруг неё, операторы на подъездах, у метро и на '
     'автобусной станции.'),
    ('Доказать поток, а не пообещать его',
     'Второй ролик строится на исследовании зоны охвата: изохроны, население, '
     'демография, потребности жителей.'),
    ('Спросить у самой аудитории',
     'Репортёры с камерой у выхода из метро «Саларьево»: чего людям не хватает '
     'в районе. Ответы вошли в ролик без переозвучки.'),
]

# ─── главный эпизод первого ролика: проезд вдоль трассы ─────────────────────
# Центр восстановлен в 3D целиком и вписан в съёмку с воздуха вдоль Киевского
# шоссе. Границы сняты покадрово: до 3.9 идёт заставка, после 10.8 монтажный
# стык на аэросъёмку стройплощадки.
DRIVE = (3.9, 10.8)

# ─── что ещё дорисовано поверх съёмки ───────────────────────────────────────
LAYERS = [
    ('v1-site', 'Натура', 'Та же площадка без графики: плита, каркас, краны, снег.'),
    ('v1-node', 'Разметка', 'Пятно застройки и парковки залиты цветом прямо '
     'поверх аэрокадра.'),
    ('v1-scheme', 'Схема', 'Подъезды, автостанция и вход в метро — отдельным '
     'планом-графикой.'),
    ('v1-map', 'Карта', 'Окружение: десять жилых комплексов и прирост населения.'),
]

# ─── зона охвата: шаги механики ─────────────────────────────────────────────
# (ключ, подпись кнопки, население, заголовок, пояснение)
REACH_STEPS = [
    ('z20', '20 минут', 2_000_000, 'Зона 20 минут',
     'Внутри 5–20 минут доступности живут 2 млн человек. Это ядро, ради '
     'которого центр строился именно здесь.'),
    ('metro', 'Метро 2019', 2_000_000, 'Четыре новые станции',
     'Сокольническая линия уходит дальше в Новую Москву: «Филатов луг», '
     '«Прокшино», «Ольховская» и «Столбово» открываются в 2019 году. '
     'Ещё до открытия центра карта вокруг него меняется.'),
    ('z30', '30 минут', 3_500_000, 'Зона 30 минут',
     'Трасса Солнцево-Бутово-Видное и отдельный подъезд к комплексу добавляют '
     '1,5 млн человек. Общая зона охвата — 3,5 млн.'),
]

# ─── арендаторы: (название, м², категория) ──────────────────────────────────
# площади с плашек первого ролика, 130–160 с
TENANTS = [
    ('Globus', 26525, 'гипермаркет'),
    ('Панда парк', 4300, 'развлечения'),
    ('Reserved · Mohito<br>Sinsay · Cropp', 4071, 'одежда'),
    ('Синема Парк', 4000, 'кино'),
    ('Спортмастер', 2200, 'спорт'),
    ('Raketa', 2200, 'развлечения'),
    ('М.видео', 1900, 'электроника'),
    ('Dino Zoo', 1500, 'детское'),
]
LEASE_TOTAL = 105000
RESTAURANTS = ['Чайхона № 1', 'Планета Суши', 'Il Патио', 'Osteria Mario', 'Швили']

# ─── аудитория из второго ролика ────────────────────────────────────────────
AGES = [('21 %', '21–34 года'), ('35 %', '35–44 года'), ('20 %', '45–54 года')]
FAMILY = [('65 %', 'состоят в браке'),
          ('2,9', 'человека в семье, выше среднего по Москве'),
          ('+8', 'индекс потребительской уверенности против −11 в 2017')]
NEEDS = [('29 %', 'одежда и обувь'), ('17 %', 'кинотеатр, кафе и рестораны'),
         ('11 %', 'продуктовый гипермаркет')]
INTERVIEWS = [
    ('v2-int-1', 'Мужчина у выхода из метро «Саларьево»'),
    ('v2-int-2', 'Женщина с ребёнком на автобусной станции'),
    ('v2-int-3', 'Женщина в сквере у метро'),
]

# ─── финал ──────────────────────────────────────────────────────────────────
FINALE = [('1 марта 2019', 'дата открытия комплекса'),
          ('60 000', 'гостей в день торжественного открытия'),
          ('10 000', 'подписчиков в соцсетях к открытию')]
TEAM = [('Девелопер и собственник', 'Хорус'), ('Управление проектом', 'Mall Management Group'),
        ('Генподрядчик', 'BOES'), ('Генпроектировщик', 'Apex project bureau'),
        ('Архитектор', 'S-Design')]


# ─── страница ───────────────────────────────────────────────────────────────
TITLE = 'Два ролика для МФК «Саларис» — кейс Hand Marketing'
DESCR = ('Два видеоролика об МФК «Саларис»: объект на стройке и аудитория зоны '
         'охвата. Съёмка дроном, 3D-графика, интервью у метро. Кейс Hand Marketing.')

CSS = """<style>
:root{
 --ind:#440099;      /* индиго заставки, снят пипеткой */
 --ind-d:#26005C;
 --ind-l:#6A2BC9;
 --sun:#F5821F;      /* оранжевый луч знака */
 --gold:#FFC800;     /* жёлтые плашки экранных титров */
 --ink:#150A28;
 --paper:#F5F3F8;
 --line:rgba(20,8,45,.14);
 --mut:#6B6480;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);
 font:400 17px/1.62 Ruda,system-ui,sans-serif;overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
.sv{max-width:100%;overflow:hidden}
.sv h1,.sv h2,.sv h3,.sv .num,.sv .plate{font-family:'Sofia Sans Condensed',
 'Arial Narrow',system-ui,sans-serif;font-weight:800;letter-spacing:.01em}
.sv section{padding:clamp(56px,8vw,104px) 0}
.sv .in{width:min(1180px,92vw);margin:0 auto}
.sv .nar{width:min(760px,92vw);margin:0 auto}
.sv h2{font-size:clamp(30px,5.4vw,58px);line-height:.98;margin:0 0 14px;
 text-transform:uppercase}
.sv h3{font-size:clamp(21px,2.6vw,28px);line-height:1.08;margin:0 0 8px}
.sv p{margin:0 0 14px}
.sv .lead{font-size:clamp(17px,2vw,21px);color:#3A3050;max-width:64ch}
.sv .mut{color:var(--mut)}
.sv .kick{font:700 13px/1 'Sofia Sans Condensed',sans-serif;letter-spacing:.22em;
 text-transform:uppercase;color:var(--ind-l);margin:0 0 16px}

/* жёлтая плашка: тем же приёмом набраны экранные титры в обоих роликах */
.plate{display:inline-block;background:var(--gold);color:#140A02;
 padding:.16em .5em .2em;transform:rotate(-1.1deg);
 box-shadow:0 6px 16px rgba(20,8,45,.16);text-transform:uppercase;line-height:1}
.plate.sm{font-size:clamp(15px,1.8vw,19px)}
.plate.lg{font-size:clamp(26px,4.4vw,44px)}

/* ── шапка кейса ─────────────────────────────────────────────────────────── */
.sv-hero{background:
  radial-gradient(120% 90% at 78% 8%,#5B18C4 0%,var(--ind) 38%,var(--ind-d) 100%);
 color:#fff;padding:clamp(96px,13vw,150px) 0 clamp(50px,7vw,84px);position:relative;
 overflow:hidden}
.sv-hero .in{position:relative;z-index:2}
.sv-hero__fan{position:absolute;right:-14%;top:-16%;width:min(760px,74vw);
 opacity:.5;pointer-events:none;z-index:1}
.sv-hero__back{position:absolute;left:-6%;bottom:-30%;width:min(620px,62vw);
 opacity:.18;pointer-events:none;z-index:1}
.sv-hero h1{font-size:clamp(38px,8.2vw,96px);line-height:.9;margin:0 0 20px;
 text-transform:uppercase;max-width:15ch}
.sv-hero h1 em{font-style:normal;color:var(--gold)}
.sv-hero .lead{color:rgba(255,255,255,.86);max-width:56ch;font-size:clamp(17px,2vw,21px)}
.sv-hero__crumb{font:600 13px/1 'Sofia Sans Condensed',sans-serif;letter-spacing:.2em;
 text-transform:uppercase;color:rgba(255,255,255,.6);margin:0 0 22px}
.sv-hero__crumb a{color:inherit;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.3)}
.sv-hero__two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;
 margin-top:clamp(30px,4vw,46px);max-width:660px}
.sv-hero__card{display:block;text-decoration:none;background:rgba(255,255,255,.1);
 border:1px solid rgba(255,255,255,.2);border-radius:14px;padding:16px 18px;
 transition:background .2s,border-color .2s}
.sv-hero__card:hover{background:rgba(255,255,255,.17);border-color:rgba(255,200,0,.6)}
.sv-hero__card b{display:block;font:800 clamp(24px,3.4vw,34px)/1 'Sofia Sans Condensed',sans-serif;
 color:var(--gold);text-transform:uppercase}
.sv-hero__card span{display:block;font-size:14px;color:rgba(255,255,255,.78);margin-top:5px}

/* ── бриф ────────────────────────────────────────────────────────────────── */
.sv-brief{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
 gap:clamp(20px,3vw,34px);margin-top:34px}
.sv-brief__it h3{font-size:clamp(19px,2.2vw,23px)}
.sv-brief__it p{color:#463C5E;margin:0}
.sv-brief__it b{display:block;width:34px;height:3px;background:var(--sun);margin:0 0 14px}

/* ── две дорожки ─────────────────────────────────────────────────────────── */
.sv-twin{background:var(--ink);color:#fff}
.sv-twin h2{color:#fff}
.sv-twin .lead{color:rgba(255,255,255,.74)}
.sv-stage{position:relative;margin:clamp(26px,4vw,40px) 0 0;border-radius:16px;
 overflow:hidden;background:#000;aspect-ratio:16/9}
.sv-stage video{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;
 opacity:0;transition:opacity .25s}
.sv-stage video.is-on{opacity:1}
.sv-stage__tag{position:absolute;left:12px;top:12px;z-index:3;
 font:700 12px/1 'Sofia Sans Condensed',sans-serif;letter-spacing:.16em;
 text-transform:uppercase;background:rgba(0,0,0,.6);color:#fff;padding:7px 10px;
 border-radius:6px}
.sv-stage__cap{position:absolute;left:0;right:0;bottom:0;z-index:3;padding:14px 16px;
 background:linear-gradient(transparent,rgba(0,0,0,.82));font-size:15px;
 color:rgba(255,255,255,.92)}
.sv-tracks{margin-top:22px}
.sv-track{display:flex;gap:3px;align-items:stretch}
.sv-track__lbl{flex:0 0 auto;width:104px;padding-right:10px;
 font:700 13px/1.2 'Sofia Sans Condensed',sans-serif;text-transform:uppercase;
 letter-spacing:.08em;display:flex;flex-direction:column;justify-content:center}
.sv-track__lbl span{font:400 11px/1.3 Ruda,sans-serif;letter-spacing:0;
 color:rgba(255,255,255,.5);text-transform:none;margin-top:3px}
.sv-track__row{flex:1 1 auto;display:flex;gap:3px;min-width:0}
.sv-seg{flex:0 0 auto;min-width:0;border:0;padding:11px 8px;border-radius:7px;
 background:rgba(255,255,255,.12);color:rgba(255,255,255,.9);cursor:pointer;
 text-align:left;font:600 12.5px/1.15 'Sofia Sans Condensed',sans-serif;
 text-transform:uppercase;letter-spacing:.03em;overflow:hidden;
 min-height:76px;
 transition:background .18s,color .18s,transform .18s}
.sv-seg span{display:block;font:400 10px/1.2 Ruda,sans-serif;letter-spacing:0;
 text-transform:none;color:rgba(255,255,255,.5);margin-top:3px;white-space:nowrap;
 overflow:hidden;text-overflow:ellipsis}
.sv-seg.narrow{writing-mode:vertical-rl;transform:rotate(180deg);
 padding:8px 6px;text-align:right;font-size:11.5px}
.sv-seg.narrow.is-on{transform:rotate(180deg) translateY(2px)}
.sv-seg[data-shared="1"]{background:rgba(255,200,0,.13);color:#fff;
 box-shadow:inset 0 0 0 1px rgba(255,200,0,.5)}
.sv-seg:hover,.sv-seg:focus-visible{background:rgba(255,255,255,.26);outline:0}
.sv-seg.is-pair{background:rgba(255,200,0,.3);color:#fff;
 box-shadow:inset 0 0 0 2px var(--gold)}
.sv-seg.is-on{background:var(--gold);color:#160A00;transform:translateY(-2px)}
.sv-seg.is-on span{color:rgba(20,10,0,.66)}
.sv-links{display:block;width:100%;height:62px;margin:0;overflow:visible}
.sv-links path{fill:none;stroke:rgba(255,200,0,.4);stroke-width:1.6;
 vector-effect:non-scaling-stroke;transition:stroke .18s,stroke-width .18s}
.sv-links path.is-lit{stroke:var(--gold);stroke-width:3}
.sv-links__in{margin-left:104px}
.sv-legend{display:flex;flex-wrap:wrap;gap:16px;margin-top:20px;
 font-size:13px;color:rgba(255,255,255,.6)}
.sv-legend i{display:inline-block;width:12px;height:12px;border-radius:3px;
 background:rgba(255,200,0,.42);margin-right:7px;vertical-align:-1px}
.sv-legend i.solo{background:rgba(255,255,255,.14)}
/* строка-подсказка: у коротких плиток текста нет, читаем здесь */
.sv-now{margin-top:14px;font-size:14.5px;color:rgba(255,255,255,.82);min-height:1.5em}
.sv-now b{font:700 14.5px/1 'Sofia Sans Condensed',sans-serif;text-transform:uppercase;
 letter-spacing:.05em;color:var(--gold);margin-right:8px}


/* ── эпизод с 3D-центром ─────────────────────────────────────────────────── */
.sv-drive{background:linear-gradient(180deg,#1B0B3A 0%,#2A0F5E 100%);color:#fff}
.sv-drive h2{color:#fff}
.sv-drive__box{position:relative;margin:clamp(26px,4vw,40px) 0 0;border-radius:16px;
 overflow:hidden;background:#000;box-shadow:0 24px 60px rgba(8,2,24,.5)}
.sv-drive__box video{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}
.sv-drive__box figcaption{padding:16px 20px 18px;background:rgba(255,255,255,.06);
 font-size:15px;color:rgba(255,255,255,.74);line-height:1.55}
.sv-drive__box figcaption a{color:#fff;text-decoration:underline;
 text-underline-offset:3px;text-decoration-color:rgba(255,200,0,.6)}
.sv-drive__box figcaption a:hover{text-decoration-color:var(--gold)}
.sv-drive__box figcaption b{display:block;font:800 17px/1 'Sofia Sans Condensed',sans-serif;
 text-transform:uppercase;letter-spacing:.04em;color:var(--gold);margin-bottom:6px}
.sv-drive__btn{position:absolute;left:50%;top:calc(50% - 42px);transform:translate(-50%,-50%);
 width:74px;height:74px;border-radius:50%;border:0;cursor:pointer;z-index:2;
 background:var(--gold);color:#160A00;font-size:26px;line-height:1;
 box-shadow:0 10px 30px rgba(0,0,0,.45);transition:transform .2s,opacity .2s}
.sv-drive__btn:hover{transform:translate(-50%,-50%) scale(1.06)}
.sv-drive__box.is-playing .sv-drive__btn{opacity:0;pointer-events:none}
@media(max-width:700px){.sv-drive__btn{width:58px;height:58px;font-size:20px}}


/* ── выбор ролика над сценой ─────────────────────────────────────────────── */
.sv-films{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;
 margin:clamp(24px,3.4vw,36px) 0 0}
.sv-film{position:relative;text-align:left;cursor:pointer;padding:16px 18px 15px;
 border-radius:13px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);
 color:#fff;transition:border-color .2s,background .2s,transform .2s}
.sv-film:hover{background:rgba(255,255,255,.12);border-color:rgba(255,200,0,.6)}
.sv-film[data-on="1"]{background:rgba(255,200,0,.14);border-color:var(--gold)}
.sv-film__n{display:block;font:700 12px/1 'Sofia Sans Condensed',sans-serif;
 letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.58)}
.sv-film b{display:block;font:800 clamp(20px,2.6vw,27px)/1 'Sofia Sans Condensed',sans-serif;
 text-transform:uppercase;margin:7px 0 5px}
.sv-film[data-on="1"] b{color:var(--gold)}
.sv-film__d{display:block;font-size:13.5px;color:rgba(255,255,255,.64);line-height:1.4}
.sv-film__t{position:absolute;right:16px;top:14px;font:700 15px/1 'Sofia Sans Condensed',sans-serif;
 letter-spacing:.04em;color:rgba(255,255,255,.72)}
.sv-film[data-on="1"] .sv-film__t{color:var(--gold)}
.sv-film::after{content:'▶ смотреть целиком';display:block;margin-top:10px;
 font:700 12px/1 'Sofia Sans Condensed',sans-serif;letter-spacing:.14em;
 text-transform:uppercase;color:rgba(255,255,255,.5)}
.sv-film[data-on="1"]::after{content:'▶ идёт в плеере';color:rgba(255,200,0,.8)}
@media(max-width:640px){.sv-films{grid-template-columns:minmax(0,1fr)}}

/* ── слои кадра ──────────────────────────────────────────────────────────── */
.sv-layers{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
 gap:clamp(14px,2vw,22px);margin-top:34px}
.sv-layer{position:relative;border-radius:12px;overflow:hidden;background:#0D0620;
 box-shadow:0 12px 30px rgba(20,8,45,.16);display:flex;flex-direction:column}
.sv-layer__t{flex:1 1 auto}
.sv-layer img{width:100%;aspect-ratio:16/9;object-fit:cover;
 transform:scale(1.04);transition:transform .5s ease}
.sv-layer:hover img{transform:scale(1)}
.sv-layer__n{position:absolute;left:10px;top:10px;z-index:2;background:var(--gold);
 color:#140A02;font:800 13px/1 'Sofia Sans Condensed',sans-serif;padding:6px 8px;
 border-radius:5px;text-transform:uppercase}
.sv-layer__t{padding:14px 16px 16px;color:#fff}
.sv-layer__t b{display:block;font:800 18px/1.1 'Sofia Sans Condensed',sans-serif;
 text-transform:uppercase;margin-bottom:5px}
.sv-layer__t span{font-size:13.5px;color:rgba(255,255,255,.66);line-height:1.5}

/* ── зона охвата ─────────────────────────────────────────────────────────── */
.sv-reach{background:linear-gradient(180deg,#2A0F5E 0%,#1A0840 100%);color:#fff}
.sv-reach h2{color:#fff}
.sv-reach .lead{color:rgba(255,255,255,.74)}
.sv-reach__grid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);
 gap:clamp(20px,3vw,40px);align-items:center;margin-top:clamp(26px,4vw,40px)}
.sv-map{position:relative;border-radius:16px;overflow:hidden;
 background:radial-gradient(70% 60% at 42% 44%,#4B2C93 0%,#2A1160 55%,#1B0940 100%)}
.sv-map svg{display:block;width:100%;height:auto}
.sv-map .z30{fill:#3E1173;opacity:0;transition:opacity .7s ease}
.sv-map .z20{fill:#8C3BC4;opacity:.94}
.sv-map .roads{fill:rgba(255,255,255,.62)}
.sv-map .hwy{fill:none;stroke:var(--gold);stroke-width:5;stroke-linecap:round;
 stroke-linejoin:round;opacity:0;transition:opacity .5s}
.sv-map .hwy.dash{stroke-dasharray:14 12;stroke-width:4}
.sv-map .spur{stroke-width:4}
.sv-map .mstop{opacity:0;transition:opacity .45s}
.sv-map .mstop circle{fill:#D6083B;stroke:#fff;stroke-width:2}
.sv-map .mstop text{fill:#fff;font:600 13px Ruda,sans-serif;paint-order:stroke;
 stroke:rgba(12,4,32,.75);stroke-width:3.4}
.sv-map .pin circle{fill:var(--sun);stroke:#fff;stroke-width:2.5}
.sv-map .pin text{fill:#fff;font:700 14px 'Sofia Sans Condensed',sans-serif;
 text-transform:uppercase;letter-spacing:.04em;paint-order:stroke;
 stroke:rgba(12,4,32,.8);stroke-width:3.6}
.sv-map[data-step="metro"] .mstop,.sv-map[data-step="z30"] .mstop{opacity:1}
.sv-map[data-step="metro"] .hwy,.sv-map[data-step="z30"] .hwy{opacity:1}
.sv-map[data-step="z30"] .z30{opacity:1}
.sv-steps{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px}
.sv-steps button{border:1px solid rgba(255,255,255,.28);background:transparent;
 color:#fff;padding:9px 15px;border-radius:999px;cursor:pointer;
 font:700 14px/1 'Sofia Sans Condensed',sans-serif;text-transform:uppercase;
 letter-spacing:.06em;transition:background .2s,border-color .2s,color .2s}
.sv-steps button:hover{border-color:var(--gold)}
.sv-steps button.is-on{background:var(--gold);border-color:var(--gold);color:#160A00}
.sv-reach__num{font:800 clamp(42px,7vw,76px)/1 'Sofia Sans Condensed',sans-serif;
 color:var(--gold);letter-spacing:.01em}
.sv-reach__num small{display:block;font:400 14px/1.4 Ruda,sans-serif;
 color:rgba(255,255,255,.66);margin-top:6px;letter-spacing:0}
.sv-reach__txt{margin-top:18px;min-height:118px}
.sv-reach__txt h3{color:#fff}
.sv-reach__txt p{color:rgba(255,255,255,.76);margin:0}
.sv-iso{margin-top:clamp(28px,4vw,44px);display:grid;
 grid-template-columns:minmax(0,1fr) minmax(0,320px);gap:clamp(18px,3vw,32px);
 align-items:center}
.sv-iso img{border-radius:12px}

/* ── 105 000 м² в масштабе ───────────────────────────────────────────────── */
.sv-lease__wrap{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);
 gap:clamp(20px,3vw,40px);align-items:start;margin-top:34px}
.sv-tree{position:relative;width:100%;aspect-ratio:1/.72;border-radius:12px;
 overflow:hidden;background:#EDE8F4;border:1px solid var(--line)}
.sv-tree__c{position:absolute;padding:9px 10px;overflow:hidden;
 border-radius:7px;transition:transform .2s,filter .2s}
.sv-tree__c b{display:block;font:800 clamp(12px,1.5vw,17px)/1.05 'Sofia Sans Condensed',sans-serif;
 text-transform:uppercase}
.sv-tree__c i{display:block;font:400 11.5px/1.25 Ruda,sans-serif;font-style:normal;
 opacity:.72;margin-top:3px}
.sv-tree__c.anchor{background:var(--ind);color:#fff}
.sv-tree__c.anchor:nth-child(2n){background:#5A18B8}
.sv-tree__c.big{background:var(--sun);color:#2A1000}
.sv-tree__c.rest{background:#DCD3EA;color:#3B3053}
.sv-tree__c:hover{filter:brightness(1.08)}
.sv-lease__side p{color:#463C5E}
.sv-rest{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.sv-rest span{border:1px solid var(--line);border-radius:999px;padding:6px 13px;
 font-size:13.5px;background:#fff}

/* ── аудитория ───────────────────────────────────────────────────────────── */
.sv-people{background:#fff}
.sv-figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
 gap:clamp(14px,2vw,22px);margin-top:30px}
.sv-fig{border:1px solid var(--line);border-radius:12px;padding:18px}
.sv-fig b{display:block;font:800 clamp(30px,4.4vw,44px)/1 'Sofia Sans Condensed',sans-serif;
 color:var(--ind);text-transform:uppercase}
.sv-fig span{display:block;font-size:14px;color:#524868;margin-top:6px;line-height:1.45}
.sv-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
 gap:clamp(20px,3vw,34px);margin-top:clamp(30px,4vw,46px)}
.sv-int{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
 gap:14px;margin-top:26px}
.sv-int figure{margin:0}
.sv-int img{border-radius:12px;aspect-ratio:16/9;object-fit:cover}
.sv-int figcaption{font-size:13.5px;color:var(--mut);margin-top:8px}

/* ── финал ───────────────────────────────────────────────────────────────── */
.sv-fin{background:
  radial-gradient(110% 80% at 22% 12%,#5B18C4 0%,var(--ind) 42%,var(--ind-d) 100%);
 color:#fff;position:relative;overflow:hidden}
.sv-fin h2{color:#fff}
.sv-fin__grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
 gap:clamp(16px,2.4vw,26px);margin-top:30px}
.sv-fin__c b{display:block;font:800 clamp(28px,4.2vw,42px)/1 'Sofia Sans Condensed',sans-serif;
 color:var(--gold);text-transform:uppercase}
.sv-fin__c span{display:block;font-size:14.5px;color:rgba(255,255,255,.76);margin-top:6px}
.sv-team{margin-top:clamp(32px,4.6vw,52px);border-top:1px solid rgba(255,255,255,.2);
 padding-top:22px;display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
 gap:16px}
.sv-team div{font-size:14px;color:rgba(255,255,255,.62)}
.sv-team b{display:block;color:#fff;font:700 16px/1.2 'Sofia Sans Condensed',sans-serif;
 text-transform:uppercase;margin-top:4px;letter-spacing:.02em}
.sv-fin__slogan{margin-top:clamp(34px,5vw,56px);border-top:1px solid rgba(255,255,255,.2);
 padding-top:26px;font:800 clamp(24px,4vw,42px)/1
 'Sofia Sans Condensed',sans-serif;text-transform:uppercase;color:var(--gold)}

/* ── появление блоков ────────────────────────────────────────────────────── */
.sv-r{opacity:0;transform:translateY(22px);transition:opacity .6s ease,transform .6s ease}
.sv-r.is-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
 .sv-r{opacity:1;transform:none;transition:none}
 .sv-layer img{transition:none}
}

@media(max-width:900px){
 .sv-reach__grid,.sv-lease__wrap,.sv-iso{grid-template-columns:minmax(0,1fr)}
 .sv-iso{gap:18px}
}
@media(max-width:700px){
 .sv-hero__two{grid-template-columns:minmax(0,1fr)}
 .sv-track__lbl{width:64px;font-size:11.5px}
 .sv-track__lbl span{display:none}
 .sv-links__in{margin-left:64px}
 .sv-seg,.sv-seg.narrow{padding:11px 4px;font-size:0;letter-spacing:0;min-height:54px;
  writing-mode:horizontal-tb;transform:none;text-align:center}
 .sv-seg.narrow.is-on{transform:translateY(-2px)}
 /* подпись кадра на телефоне села бы на элементы управления плеера,
    тот же текст показывает строка под дорожками */
 .sv-stage__cap{display:none}
 .sv-seg span{display:none}
 .sv-seg::before{content:attr(data-i);font:700 12px/1 'Sofia Sans Condensed',sans-serif}
 .sv-links{height:40px}
}
@media(max-width:520px){
 .sv-tree{aspect-ratio:1/1.05}
 .sv-tree__c b{font-size:11px}
 .sv-tree__c i{display:none}
}
</style>"""

def fan(n=42, r0=26.0, r1=96.0, cx=100.0, cy=100.0, start=-100.0, span=350.0,
        wide=0.62, thin=0.06, cls=''):
    """Веер знака «Саларис»: лепестки по кругу вырождаются в тонкие иглы.

    Форма снята с заставки обоих роликов: сверху широкие лепестки, дальше по
    часовой они сужаются. Рисуем сами — знак нужен и в шапке, и в финале, и
    точкой комплекса на карте охвата, каждый раз со своими пропорциями."""
    import math
    out = []
    for i in range(n):
        t = i / (n - 1)
        a = math.radians(start + span * t)
        half = math.radians((wide + (thin - wide) * t) * 360 / n * 1.6)
        length = r1 - (r1 - r0) * 0.12 * t
        p0 = (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        tip = (cx + length * math.cos(a), cy + length * math.sin(a))
        mid = r0 + (length - r0) * 0.45
        c1 = (cx + mid * math.cos(a - half), cy + mid * math.sin(a - half))
        c2 = (cx + mid * math.cos(a + half), cy + mid * math.sin(a + half))
        col = ('#F5821F', '#FFC800', '#FF9E2C')[i % 3]
        out.append(
            f'<path d="M{p0[0]:.1f} {p0[1]:.1f}Q{c1[0]:.1f} {c1[1]:.1f} {tip[0]:.1f} '
            f'{tip[1]:.1f}Q{c2[0]:.1f} {c2[1]:.1f} {p0[0]:.1f} {p0[1]:.1f}Z" '
            f'fill="{col}"/>')
    return (f'<svg class="{cls}" viewBox="0 0 200 200" aria-hidden="true" '
            f'focusable="false">{"".join(out)}</svg>')


def hero():
    return (
      '<header class="sv-hero">'
      f'{fan(cls="sv-hero__fan")}{fan(n=30, cls="sv-hero__back")}'
      '<div class="in">'
      '<p class="sv-hero__crumb"><a href="/project/">Проекты</a> · '
      '<a href="/videoproduction/">Видеопродакшн</a> · МФК «Саларис»</p>'
      '<h1>Один объект.<br><em>Два ролика.</em><br>Разные доказательства</h1>'
      '<p class="lead">Первый ролик снимали зимой 2018-го, когда торгового центра '
      'ещё не было: аэросъёмка площадки и здание, собранное графикой. Второй — '
      'через полгода, когда доказывать нужно было уже не метры, а то, что в эти '
      'метры кто-то придёт.</p>'
      '<div class="sv-hero__two">'
      '<a class="sv-hero__card" href="#films"><b>2:58 · объект</b>'
      '<span>Стройплощадка с дрона, 3D-модель в натурном кадре, метры и пул '
      'арендаторов</span></a>'
      '<a class="sv-hero__card" href="#films"><b>2:33 · аудитория</b>'
      '<span>Зона охвата изохронами, демография, интервью у метро '
      '«Саларьево»</span></a>'
      '</div></div></header>')


def brief():
    items = ''.join(
        f'<div class="sv-brief__it sv-r"><b></b><h3>{t}</h3><p>{d}</p></div>'
        for t, d in BRIEF)
    return ('<section><div class="in">'
            '<p class="kick">Задача</p>'
            '<h2>Серия роликов об объекте,<br>его инфраструктуре и аудитории</h2>'
            '<p class="lead">МФК «Саларис» на Киевском шоссе — 310 000 м² в Новой '
            'Москве у метро «Саларьево». Мы начали работу на стадии строительства '
            'и закончили роликом, который вышел к открытию.</p>'
            f'<div class="sv-brief">{items}</div>'
            '</div></section>')


def twin():
    """Две дорожки: сегменты обоих роликов и дуги между общими темами."""
    tracks, centers = [], {}
    for film in FILMS:
        segs = []
        for i, (a, b, label, tag, note) in enumerate(film['segs'], 1):
            w = (b - a) / film['dur'] * 100
            shared = '1' if tag in SHARED else '0'
            centers.setdefault(tag, {})[film['n']] = (a + (b - a) / 2) / film['dur'] * 100
            # что влезет в плитку, решаем по её доле хронометража, а не CSS-ом:
            # в широкую идёт подпись с пояснением, в среднюю только подпись,
            # в узкую та же подпись, но повёрнутая на бок — голый номер не читается
            narrow = w < 5.5 and len(label) > 5
            inner = (f'{label}<span>{note}</span>' if w >= 11 else label)
            cls = 'sv-seg narrow' if narrow else 'sv-seg'
            segs.append(
              f'<button class="{cls}" style="flex:{w:.3f} 1 0" data-film="{film["n"]}" '
              f'data-start="{a}" data-end="{b}" data-tag="{tag}" data-shared="{shared}" '
              f'data-i="{i}" data-label="{label}" data-note="{note}" '
              f'title="{label}: {note}">{inner}</button>')
        tracks.append(
          f'<div class="sv-track" data-film="{film["n"]}">'
          f'<div class="sv-track__lbl">Ролик {film["n"]}<span>{film["sub"]}</span></div>'
          f'<div class="sv-track__row">{"".join(segs)}</div></div>')

    # дуги: от центра сегмента верхней дорожки к центру парного снизу.
    # viewBox тянется по ширине, поэтому штрих задан non-scaling, иначе
    # горизонтальные участки кривой были бы толще вертикальных.
    arcs = []
    for tag in SHARED:
        c = centers.get(tag, {})
        if 1 not in c or 2 not in c:
            continue
        x1, x2 = c[1] * 10, c[2] * 10
        arcs.append(f'<path data-tag="{tag}" d="M{x1:.1f} 0C{x1:.1f} 46 {x2:.1f} 44 {x2:.1f} 90"/>')
    links = ('<div class="sv-links__in"><svg class="sv-links" viewBox="0 0 1000 90" '
             f'preserveAspectRatio="none" aria-hidden="true">{"".join(arcs)}</svg></div>')

    # явный выбор ролика: механика дорожек хороша для разбора, но человек,
    # который зашёл посмотреть работу, должен включить ролик целиком в один клик
    tabs = ''.join(
      f'<button class="sv-film" data-film="{f["n"]}"'
      f'{" data-on=1" if f["n"] == 1 else ""}>'
      f'<span class="sv-film__n">Ролик {f["n"]}</span>'
      f'<b>{f["title"]}</b>'
      f'<span class="sv-film__d">{f["sub"]}</span>'
      f'<span class="sv-film__t">{round(f["dur"]) // 60}:{round(f["dur"]) % 60:02d}</span>'
      '</button>'
      for f in FILMS)

    videos = ''.join(
        f'<video id="sv-v{f["n"]}" src="{f["src"]}" poster="{f["poster"]}" '
        f'playsinline preload="metadata" controls{" class=is-on" if f["n"] == 1 else ""}></video>'
        for f in FILMS)

    return ('<section class="sv-twin"><div class="in">'
      '<p class="kick">Два ролика рядом</p>'
      '<h2>Где ролики совпадают,<br>а где расходятся</h2>'
      '<p class="lead">Оба ролика целиком, со звуком: выберите ролик кнопкой ''выше плеера. Ниже хронометражи разложены по смыслу и поставлены друг под '
      'друга. Жёлтым отмечены куски, которые есть в обоих роликах: заставка, '
      'метры, транспорт, бренды, слоган и титр команды. Дуга связывает пару. '
      'Нажмите на любой кусок — плеер переключится на нужный ролик и '
      'перемотает на это место.</p>'
      f'<div class="sv-films" id="films">{tabs}</div>'
      f'<div class="sv-stage sv-r"><span class="sv-stage__tag" id="sv-tag">Ролик 1 · объект</span>'
      f'{videos}<div class="sv-stage__cap" id="sv-cap">Ролик про объект: '
      'стройплощадка с дрона и здание, собранное графикой.</div></div>'
      f'<div class="sv-tracks sv-r">{tracks[0]}{links}{tracks[1]}</div>'
      '<p class="sv-now" id="sv-now">Выберите кусок на дорожке</p>'
      '<div class="sv-legend"><span><i></i>есть в обоих роликах</span>'
      '<span><i class="solo"></i>только в этом</span>'
      '<span>2:58 и 2:33 — реальные хронометражи</span></div>'
      '</div></section>')


def drive():
    """Главный эпизод первого ролика: 3D-центр в кадре с воздуха вдоль трассы.

    Играет отрезком по петле, а не отдельным файлом: media/ на бой заливается
    руками, лишний файл там был бы обузой. Границы держит JS, звук снят —
    эпизод в ролике идёт под музыку, и включать её сама страница не должна."""
    a, b = DRIVE
    return ('<section class="sv-drive"><div class="in">'
      '<p class="kick" style="color:#C9A6FF">Первый ролик · 0:04–0:11</p>'
      '<h2>Центр, которого<br>ещё не существовало</h2>'
      '<p class="lead" style="color:rgba(255,255,255,.78)">Съёмки шли зимой '
      '2018-го, когда на площадке стояли краны и плита. Комплекс для этого '
      'кадра восстановили в 3D целиком — фасад, вывеска, знак, витрины — и '
      'вписали в съёмку с воздуха вдоль Киевского шоссе. Шоссе, машины на нём, '
      'парковка, лес и снег настоящие; здания в этом кадре нет ни одного '
      'настоящего пикселя.</p>'
      f'<figure class="sv-drive__box sv-r" data-a="{a}" data-b="{b}">'
      f'<video id="sv-drive" src="{V1}" poster="{IMG}/v1-cg.jpg" muted loop '
      'playsinline preload="metadata" aria-label="Эпизод ролика: комплекс, '
      'собранный в 3D, в кадре с воздуха вдоль Киевского шоссе"></video>'
      '<button class="sv-drive__btn" id="sv-drive-btn" type="button" '
      'aria-label="Запустить эпизод">▶</button>'
      '<figcaption><b>Со стороны трассы</b>'
      'Камера идёт вдоль шоссе и выходит на фасад: так объект увидит человек, '
      'который проезжает мимо. Этот ролик показывали арендаторам на '
      '<a href="/event/salaris/">презентации комплекса</a> весной 2018-го, '
      'когда на площадке ещё работали краны.</figcaption>'
      '</figure>'
      '</div></section>')


def layers():
    cards = ''.join(
        f'<figure class="sv-layer sv-r"><span class="sv-layer__n">{i}</span>'
        f'<img src="{IMG}/{slug}.jpg" alt="{alt}" loading="lazy" width="1100" height="618">'
        f'<figcaption class="sv-layer__t"><b>{name}</b><span>{alt}</span></figcaption>'
        '</figure>'
        for i, (slug, name, alt) in enumerate(LAYERS, 1))
    return ('<section class="sv-twin" style="background:#1D1030"><div class="in">'
      '<p class="kick">Тот же приём дальше по ролику</p>'
      '<h2>Что ещё дорисовано<br>поверх съёмки</h2>'
      '<p class="lead">Графика в ролике не заканчивается зданием. Пятно '
      'застройки, подъезды, автостанция и окружение ложатся прямо на кадры с '
      'дрона: зритель всё время смотрит на настоящую площадку, но видит на ней '
      'то, чего пока нет.</p>'
      f'<div class="sv-layers">{cards}</div>'
      '</div></section>')


def reach():
    m = MAP
    z30 = ''.join(f'<path class="z30" d="{d}"/>' for d in m['zone30'])
    z20 = ''.join(f'<path class="z20" d="{d}"/>' for d in m['zone20'])
    stops = ''.join(
      f'<g class="mstop"><circle cx="{s["x"]}" cy="{s["y"]}" r="7"/>'
      f'<text x="{s["x"] + 13}" y="{s["y"] + 5}">{s["name"]}</text></g>'
      for s in m['metro'])
    # viewBox по фактическим габаритам зон, а не по всему кадру: иначе четверть
    # блока занимает пустое поле, оставшееся от полей исходного кадра
    box = '14 6 654 692'
    svg = (f'<svg viewBox="{box}" role="img" '
           'aria-label="Карта зоны охвата МФК «Саларис»: зоны 20 и 30 минут, '
           'новая трасса и станции метро 2019 года">'
           f'{z30}{z20}'
           f'<path class="roads" fill-rule="evenodd" d="{m["roads"]}"/>'
           f'<path class="hwy dash" d="{m["highwayDash"]}"/>'
           f'<path class="hwy" d="{m["highway"]}"/>'
           f'<path class="hwy spur" d="{m["spur"]}"/>'
           f'{stops}'
           '<g class="pin"><circle cx="310" cy="487" r="9"/>'
           '<text x="310" y="516" text-anchor="middle">МФК «Саларис»</text></g>'
           '</svg>')
    btns = ''.join(
      f'<button data-step="{k}"{" class=is-on" if i == 0 else ""}>{lbl}</button>'
      for i, (k, lbl, _p, _h, _d) in enumerate(REACH_STEPS))
    return ('<section class="sv-reach"><div class="in">'
      '<p class="kick">Второй ролик · зона охвата</p>'
      '<h2>Сколько людей<br>живёт в получасе отсюда</h2>'
      '<p class="lead">Второй ролик отвечает на вопрос арендатора: откуда '
      'возьмётся трафик. Карта ниже собрана по кадрам ролика — контуры зон, '
      'дорожная сеть и трасса сняты с исходной графики, а не нарисованы на глаз.</p>'
      '<div class="sv-reach__grid sv-r">'
      f'<div class="sv-map" data-step="z20" id="sv-map">{svg}</div>'
      '<div>'
      f'<div class="sv-steps" id="sv-steps">{btns}</div>'
      '<div class="sv-reach__num"><span id="sv-pop">2 000 000</span>'
      '<small>человек в зоне доступности</small></div>'
      '<div class="sv-reach__txt"><h3 id="sv-rh">Зона 20 минут</h3>'
      '<p id="sv-rd">Внутри 5–20 минут доступности живут 2 млн человек. Это ядро, '
      'ради которого центр строился именно здесь.</p></div>'
      '</div></div>'
      '<div class="sv-iso sv-r">'
      f'<img src="{IMG}/v2-iso.jpg" alt="Кадр ролика: зона охвата 2019 года изохронами" '
      'loading="lazy" width="1280" height="720">'
      '<div><h3 style="color:#fff">Так это выглядело в ролике</h3>'
      '<p style="color:rgba(255,255,255,.72)">Кольца доступности от 5 до 30 минут, '
      'посчитанные по дорожной сети, а не циркулем от точки. Внутри 5–20 минут '
      'живут два миллиона человек — это и есть ответ на вопрос про трафик.</p>'
      '<p style="color:rgba(255,255,255,.72)">Через полгода после съёмки центр '
      'открылся, и в первый день в него вошли 60 000 человек.</p></div>'
      '</div></div></section>')


def squarify(items, x, y, w, h):
    """Squarified treemap (Bruls, Huizing, van Wijk): плитки укладываются
    рядами так, чтобы соотношение сторон было ближе к квадрату.

    Нужно, чтобы плитка арендатора занимала в квадрате аренды свою настоящую
    долю: Globus с его 26 525 м² должен визуально давить всё остальное, как
    он и давит в реальном пуле. Площади масштабируем к площади прямоугольника
    один раз, дальше работаем уже в «пикселях» — так остаток всегда сходится."""
    total = sum(it[1] for it in items)
    scale = (w * h) / total
    rest = [(it, it[1] * scale) for it in sorted(items, key=lambda i: -i[1])]
    out = []

    def worst(row, side):
        s = sum(a for _i, a in row)
        if s <= 0 or side <= 0:
            return float('inf')
        mx = max(a for _i, a in row)
        mn = min(a for _i, a in row)
        return max(side * side * mx / (s * s), s * s / (side * side * mn))

    while rest:
        side = min(w, h)
        row = [rest.pop(0)]
        while rest and worst(row + [rest[0]], side) <= worst(row, side):
            row.append(rest.pop(0))
        s = sum(a for _i, a in row)
        if w <= h:                      # ряд ложится горизонтальной полосой
            rh = s / w if w else 0
            ox = x
            for it, a in row:
                rw = a / rh if rh else 0
                out.append((it, ox, y, rw, rh))
                ox += rw
            y, h = y + rh, h - rh
        else:                           # ряд ложится вертикальной колонкой
            rw = s / h if h else 0
            oy = y
            for it, a in row:
                rh = a / rw if rw else 0
                out.append((it, x, oy, rw, rh))
                oy += rh
            x, w = x + rw, w - rw
    return out


def lease():
    rest_area = LEASE_TOTAL - sum(a for _n, a, _c in TENANTS)
    items = [(n, a, c) for n, a, c in TENANTS]
    items.append(('Галерея и рестораны', rest_area, '290 магазинов'))
    cells = []
    for (name, area, cat), x, y, w, h in squarify(items, 0, 0, 100, 100):
        kind = ('rest' if name.startswith('Галерея')
                else 'big' if area > 20000 else 'anchor')
        cells.append(
          f'<div class="sv-tree__c {kind}" style="left:{x:.2f}%;top:{y:.2f}%;'
          f'width:{w:.2f}%;height:{h:.2f}%" title="{cat}, {area:,} м²">'
          f'<b>{name}</b><i>{area:,} м²</i></div>'.replace(',', ' '))
    rests = ''.join(f'<span>{r}</span>' for r in RESTAURANTS)
    return ('<section><div class="in">'
      '<p class="kick">Первый ролик · пул арендаторов</p>'
      '<h2>105 000 м² аренды<br>в настоящем масштабе</h2>'
      '<p class="lead">В ролике якорные арендаторы идут списком с площадями. '
      'Здесь те же цифры разложены по одному квадрату: каждая плитка занимает '
      'ровно свою долю арендопригодной площади.</p>'
      '<div class="sv-lease__wrap sv-r">'
      f'<div class="sv-tree">{"".join(cells)}</div>'
      '<div class="sv-lease__side">'
      '<p><span class="plate sm">310 000 м² общая площадь</span></p>'
      '<p>Из них 105 000 м² сдаются в аренду, остальное — парковка на 5 000 '
      'машиномест, технические и общие зоны. Восемь якорей забирают меньше '
      'половины: остальное — галерея на 290 магазинов.</p>'
      '<p>Рестораны и кафе в ролике идут отдельным кадром:</p>'
      f'<div class="sv-rest">{rests}</div>'
      '</div></div></div></section>')


def people():
    ages = ''.join(f'<div class="sv-fig sv-r"><b>{n}</b><span>{t}</span></div>'
                   for n, t in AGES)
    fam = ''.join(f'<div class="sv-fig sv-r"><b>{n}</b><span>{t}</span></div>'
                  for n, t in FAMILY)
    needs = ''.join(f'<div class="sv-fig sv-r"><b>{n}</b><span>{t}</span></div>'
                    for n, t in NEEDS)
    ints = ''.join(
      f'<figure><img src="{IMG}/{slug}.jpg" alt="{cap}" loading="lazy" '
      f'width="1280" height="720"><figcaption>{cap}</figcaption></figure>'
      for slug, cap in INTERVIEWS)
    return ('<section class="sv-people"><div class="in">'
      '<p class="kick">Второй ролик · кто придёт</p>'
      '<h2>Аудитория цифрами<br>и своими словами</h2>'
      '<p class="lead">Возраст, состав семьи и настроение — из исследования зоны '
      'охвата. Чего людям не хватает в районе — из интервью, которые репортёры '
      'записали у выхода из метро.</p>'
      f'<div class="sv-figs">{ages}</div>'
      f'<div class="sv-figs">{fam}</div>'
      '<h3 style="margin-top:clamp(30px,4vw,46px)">Что жители называют сами</h3>'
      '<p class="mut">Потребности в зоне охвата по мнению самих жителей — три '
      'первых ответа. Ровно эти категории и стали якорями центра.</p>'
      f'<div class="sv-figs">{needs}</div>'
      '<h3 style="margin-top:clamp(30px,4vw,46px)">Интервью у метро «Саларьево»</h3>'
      '<p class="mut" style="max-width:70ch">Съёмочная группа работала на выходе '
      'из метро и на автобусной станции. В ролике эти же три цифры идут плашкой '
      'поверх интервью: сначала человек говорит, чего ему не хватает, а рядом '
      'стоит доля тех, кто ответил так же. Ответы вошли без переозвучки.</p>'
      f'<div class="sv-int">{ints}</div>'
      '</div></section>')


def finale():
    cards = ''.join(f'<div class="sv-fin__c sv-r"><b>{n}</b><span>{t}</span></div>'
                    for n, t in FINALE)
    team = ''.join(f'<div>{role}<b>{who}</b></div>' for role, who in TEAM)
    return ('<section class="sv-fin">'
      f'{fan(cls="sv-hero__fan")}'
      '<div class="in" style="position:relative;z-index:2">'
      '<p class="kick" style="color:rgba(255,255,255,.66)">Чем закончилось</p>'
      '<h2>Второй ролик вышел<br>к открытию центра</h2>'
      '<p class="lead" style="color:rgba(255,255,255,.78)">Первый ролик показывали '
      'арендаторам, пока на площадке работали краны. Второй — уже в готовом '
      'здании, за несколько месяцев до того, как в него вошли первые 60 000 '
      'человек.</p>'
      f'<div class="sv-fin__grid">{cards}</div>'
      f'<div class="sv-team">{team}</div>'
      '<p class="sv-fin__slogan">«Солнце в каждом из нас»</p>'
      '</div></section>')


HEAD = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<!--custom-page-->'
        f'<title>{TITLE}</title>'
        f'<meta name="description" content="{DESCR}">'
        f'<link rel="canonical" href="{URL}">'
        '<meta property="og:type" content="article">'
        f'<meta property="og:title" content="{TITLE}">'
        f'<meta property="og:description" content="{DESCR}">'
        f'<meta property="og:url" content="{URL}">'
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/v1-cg-name.jpg">'
        '<link rel="preconnect" href="/">'
        '<link rel="stylesheet" href="/fonts/sofia-ruda.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


PAGE_JS = """<script>(function(){
 var slow=matchMedia('(prefers-reduced-motion:reduce)').matches;

 // ── две дорожки: сегменты управляют парой плееров ────────────────────────
 var vids={1:document.getElementById('sv-v1'),2:document.getElementById('sv-v2')};
 var tag=document.getElementById('sv-tag'),cap=document.getElementById('sv-cap'),
     now=document.getElementById('sv-now');
 var segs=[].slice.call(document.querySelectorAll('.sv-seg'));
 var arcs=[].slice.call(document.querySelectorAll('.sv-links path'));
 var FILM={1:'Ролик 1 · объект',2:'Ролик 2 · аудитория'};
 var cur=1;

 function setNow(s){
  if(!now)return;
  var sh=s.dataset.shared==='1'?' Есть в обоих роликах.':'';
  now.innerHTML='<b>Ролик '+s.dataset.film+' · '+s.dataset.label+'</b>'+s.dataset.note+sh;
 }
 function lightPair(t,on){
  segs.forEach(function(s){s.classList.toggle('is-pair',!!on&&s.dataset.tag===t&&!s.classList.contains('is-on'));});
  arcs.forEach(function(a){a.classList.toggle('is-lit',!!on&&a.dataset.tag===t);});
 }
 function markPlaying(film,time){
  var hit=null;
  segs.forEach(function(s){
   var on=(+s.dataset.film===film&&time>=+s.dataset.start&&time<+s.dataset.end);
   s.classList.toggle('is-on',on);
   if(on){hit=s;s.classList.remove('is-pair');}
  });
  if(hit){
   cap.textContent=hit.dataset.note;
   if(now)setNow(hit);
   // подсветить дугу текущей темы, если тема общая
   arcs.forEach(function(a){a.classList.toggle('is-lit',a.dataset.tag===hit.dataset.tag);});
  }
 }
 function show(film){
  cur=film;
  if(typeof markFilm==='function')markFilm(film);
  for(var k in vids){
   var v=vids[k];if(!v)continue;
   var on=(+k===film);
   v.classList.toggle('is-on',on);
   if(!on){try{v.pause();}catch(e){}}
  }
  tag.textContent=FILM[film];
 }
 segs.forEach(function(s){
  s.addEventListener('click',function(){
   var film=+s.dataset.film,v=vids[film];if(!v)return;
   show(film);
   // назначаем время после метаданных: до них currentTime молча обнуляется
   var seek=function(){try{v.currentTime=+s.dataset.start;}catch(e){}};
   if(v.readyState>0)seek();else v.addEventListener('loadedmetadata',seek,{once:true});
   v.play().catch(function(){});
   markPlaying(film,+s.dataset.start+0.1);
  });
  s.addEventListener('mouseenter',function(){lightPair(s.dataset.tag,1);setNow(s);});
  s.addEventListener('mouseleave',function(){lightPair(s.dataset.tag,0);});
  s.addEventListener('focus',function(){lightPair(s.dataset.tag,1);setNow(s);});
  s.addEventListener('blur',function(){lightPair(s.dataset.tag,0);});
 });
 [1,2].forEach(function(n){
  var v=vids[n];if(!v)return;
  v.addEventListener('timeupdate',function(){if(cur===n)markPlaying(n,v.currentTime);});
  v.addEventListener('play',function(){show(n);});
 });


 // ── эпизод с 3D-центром: петля по отрезку внутри первого ролика ──────────
 var dBox=document.querySelector('.sv-drive__box'),
     dVid=document.getElementById('sv-drive'),
     dBtn=document.getElementById('sv-drive-btn');
 if(dBox&&dVid){
  var A=parseFloat(dBox.dataset.a),B=parseFloat(dBox.dataset.b);
  var seeked=false;
  function toStart(){try{dVid.currentTime=A;seeked=true;}catch(e){}}
  dVid.addEventListener('loadedmetadata',toStart);
  if(dVid.readyState>0)toStart();
  // loop у <video> отматывает на 0, а нам нужен конец отрезка
  dVid.addEventListener('timeupdate',function(){
   if(dVid.currentTime>B||dVid.currentTime<A-0.5)toStart();
  });
  function playDrive(){
   if(!seeked)toStart();
   dVid.play().then(function(){dBox.classList.add('is-playing');})
              .catch(function(){dBox.classList.remove('is-playing');});
  }
  dBtn.addEventListener('click',playDrive);
  dVid.addEventListener('click',function(){
   if(dVid.paused)playDrive();else{dVid.pause();dBox.classList.remove('is-playing');}
  });
  // автостарт, когда блок попал в кадр: беззвучное видео браузеры пускают,
  // при отказе остаётся кнопка. При reduced-motion не трогаем вовсе.
  if(!slow){
   var started=false;
   var watch=function(){
    if(started)return;
    var r=dBox.getBoundingClientRect();
    if(r.top<innerHeight*0.75&&r.bottom>innerHeight*0.25){started=true;playDrive();
     removeEventListener('scroll',watch);}
   };
   addEventListener('scroll',watch,{passive:true});watch();
  }
 }


 // ── кнопки выбора ролика: включить целиком с начала ──────────────────────
 var films=[].slice.call(document.querySelectorAll('.sv-film'));
 function markFilm(n){films.forEach(function(f){
  if(+f.dataset.film===n)f.dataset.on='1';else f.removeAttribute('data-on');});}
 films.forEach(function(f){
  f.addEventListener('click',function(){
   var n=+f.dataset.film,v=vids[n];if(!v)return;
   show(n);markFilm(n);
   var rewind=function(){try{v.currentTime=0;}catch(e){}};
   if(v.readyState>0)rewind();else v.addEventListener('loadedmetadata',rewind,{once:true});
   v.play().catch(function(){});
  });
 });

 // ── зона охвата: шаги, счётчик населения ─────────────────────────────────
 var STEPS=%STEPS%;
 var map=document.getElementById('sv-map'),pop=document.getElementById('sv-pop'),
     rh=document.getElementById('sv-rh'),rd=document.getElementById('sv-rd'),
     steps=document.getElementById('sv-steps');
 var popCur=STEPS.length?STEPS[0].pop:0,anim=null;
 function fmt(n){return String(Math.round(n)).replace(/\\B(?=(\\d{3})+(?!\\d))/g,' ');}
 function runTo(to){
  if(anim)cancelAnimationFrame(anim);
  var from=popCur,t0=null,dur=slow?0:700;
  if(!dur){popCur=to;pop.textContent=fmt(to);return;}
  function tick(ts){
   if(t0===null)t0=ts;
   var k=Math.min(1,(ts-t0)/dur),e=1-Math.pow(1-k,3);
   popCur=from+(to-from)*e;pop.textContent=fmt(popCur);
   if(k<1)anim=requestAnimationFrame(tick);
  }
  anim=requestAnimationFrame(tick);
 }
 if(steps)steps.addEventListener('click',function(e){
  var b=e.target.closest('button');if(!b)return;
  var st=null;for(var i=0;i<STEPS.length;i++)if(STEPS[i].key===b.dataset.step)st=STEPS[i];
  if(!st)return;
  [].forEach.call(steps.querySelectorAll('button'),function(x){x.classList.toggle('is-on',x===b);});
  map.dataset.step=st.key;rh.textContent=st.h;rd.textContent=st.d;runTo(st.pop);
 });

 // ── появление блоков: свип по скроллу, а не IntersectionObserver.
 // Наблюдатель отдаёт колбэк на следующем кадре, и при быстрой прокрутке до
 // низа страницы нижние блоки остаются с opacity:0. Свип считает геометрию
 // синхронно, поэтому невидимого контента не остаётся.
 var els=[].slice.call(document.querySelectorAll('.sv-r'));
 function sweep(){
  for(var i=els.length-1;i>=0;i--){
   var r=els[i].getBoundingClientRect();
   if(r.top<innerHeight*1.1&&r.bottom>-120){els[i].classList.add('is-in');els.splice(i,1);}
  }
  if(!els.length){removeEventListener('scroll',sweep);removeEventListener('resize',sweep);}
 }
 addEventListener('scroll',sweep,{passive:true});
 addEventListener('resize',sweep);
 sweep();
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Видеопродакшн","item":"https://hand-marketing.ru/videoproduction/"},'
  '{"@type":"ListItem","position":3,"name":"Ролики МФК «Саларис»",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    steps = [{'key': k, 'pop': p, 'h': h, 'd': d} for k, _l, p, h, d in REACH_STEPS]
    js = PAGE_JS.replace('%STEPS%', json.dumps(steps, ensure_ascii=False))
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="sv">{hero()}{brief()}{drive()}{twin()}{layers()}'
            f'{reach()}{lease()}{people()}{finale()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'salaris')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
