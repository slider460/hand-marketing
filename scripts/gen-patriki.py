#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка кейса «Журнал Patriki Times» — mirror/creative/patriki/index.html.

Шапка, фиолетовая форма, футер и служебные скрипты берутся один в один из кейса
Ramada, чтобы обвязка у всех кастомных кейсов оставалась одинаковой. Всё, что
между ними, — своё: типографика повторяет само издание (узкий гротеск капсом,
красная плашка героя, линейки), поэтому шрифты Oswald + Onest.

Ассеты кладёт scripts/patriki-assets.py. Прогон: python3 scripts/gen-patriki.py
"""
import os
import re

SRC = 'mirror/creative/becar/ramada/index.html'
DST = 'mirror/creative/patriki/index.html'

ref = open(SRC, encoding='utf-8').read()


def slice_between(start, end, inclusive_end=True):
    a = ref.index(start)
    b = ref.index(end, a) + (len(end) if inclusive_end else 0)
    return ref[a:b]


CHROME_CSS = slice_between('<style id="hm-chrome-css">', '</style>')
METRIKA = slice_between('<!-- Yandex.Metrika counter -->', '<!-- /Yandex.Metrika counter -->')
HDR = slice_between('<div class="hm-chrome hm-hdr"', '<main class="rm">', inclusive_end=False)
FOOT = slice_between('<section class="hm-cta">', '<script>(function(){\n// убрать CTA', inclusive_end=False)
FORM_JS = ref[ref.index('<script>(function(){\n// убрать CTA'):]
FORM_JS = FORM_JS[:FORM_JS.index('</script>') + 9]

# ── содержание листалки ─────────────────────────────────────────────────────
PAGES = {
    9: [
        (1, 'Обложка. Генрих Карпин, 800°C Contemporary Steak'),
        (3, 'Колонка главного редактора и содержание номера'),
        (4, 'Блиц-интервью: Il Forno Group и мясной ресторан на Патриарших'),
        (5, 'Зал, бургер и стейк — фотоблок интервью'),
        (7, 'Рестораны: Ess-Thetik, австрийские сосиски под ёлкой'),
        (8, 'Рестораны: Tuna Sushi Bar и бренд-шеф Роман Яковенко'),
        (10, 'Патрики дети: Марк Беррес о чемпионате мира по футболу'),
        (11, 'Топ-5 игроков и топ-5 претендентов на мундиаль'),
        (12, 'История: Наполеон и Жозефина, открытие темы'),
        (15, 'Красная выноска на линейках закрывает историю Жозефины'),
        (16, 'История: Карл Фаберже и императорские пасхальные яйца'),
        (18, '«В лесу родилась ёлочка» — песня родом с Патриков'),
        (19, 'Ноты Бекмана, журнал «Малютка» и текст песни'),
        (20, 'Кино: Голливуд, к России с любовью. Нелли Холмс'),
        (22, 'Роман Резницкий: от поп до арт'),
        (25, 'Психология: Штирлиц Роза Карлосоновна о зависимости от любви'),
        (30, 'Олег Рой: анатомия разочарования'),
        (34, 'Красота: Color-time, пространство на Патриарших'),
        (36, 'Топ-10: самые дорогие дома в мире'),
        (40, 'Бизнес: Penny Lane Realty, итоги года на рынке аренды'),
        (42, 'Бизнес: Татьяна Гулина, тренды будущего'),
        (46, 'Патрики глазами животных: Адольф, пти-брабансон'),
        (48, 'Гид по Патриаршим: двадцать адресов района'),
        (52, 'Задняя обложка: Agent Provocateur'),
    ],
    10: [
        (1, 'Обложка. Андрей Шаронов, президент МШУ СКОЛКОВО'),
        (3, 'Колонка редактора и содержание февральско-мартовского номера'),
        (4, 'Блиц-интервью: Андрей Шаронов о спорте и СКОЛКОВО'),
        (7, 'Анна Резниченко и турнир к 90-летию Александра Гомельского'),
        (8, 'Патрики спорт: Маирбек Хостикоев, модуль героя'),
        (11, 'Аркадий Дворкович, капитан команды «Брига ДА»'),
        (13, 'Павел Колобков, министр спорта'),
        (15, 'Алексей Саврасенко, «Локомотив-Кубань»'),
        (16, 'Николай Падиус, тренер клуба СКОЛКОВО'),
        (19, 'Фоторепортаж с благотворительного турнира'),
        (22, 'Рестораны: Режис Тригель, шеф Bistrot Берёзка'),
        (23, 'Диагональная выноска на ночном Париже'),
        (25, 'Tuna Sushi Bar: вертикальные буквы на красном'),
        (26, 'Ess-Thetik: рукописная строка поверх фото'),
        (28, 'Патрики дети: топ-10 мультфильмов Марка Берреса'),
        (30, 'История: братья Третьяковы и их галерея'),
        (35, 'Третьяковская галерея: десять картин о Москве'),
        (38, 'Проект «Жизнь»: #докопаемсядоистины'),
        (40, 'Психология: Штирлиц Роза Карлосоновна, стоп отношения'),
        (42, 'Олег Рой: короля играет свита'),
        (46, 'Топ-10: десять семей, которые управляют миром'),
        (50, 'Татьяна Гулина: океан внутри, или будущая жизнь на воде'),
        (54, 'Мода: Кристина Кирия, весна наступает'),
        (56, 'Подиум: Chanel, Dior, Valentino, Elie Saab'),
        (60, 'Светская жизнь: премия Patriki Times Lifestyle Awards 2018'),
        (62, 'Патрики глазами животных: Лаффа'),
        (64, 'Гид по Патриаршим: обновлённый список адресов'),
        (68, 'Задняя обложка: Agent Provocateur'),
    ],
}

RUBRICS = ['История', 'Рестораны', 'Бизнес', 'Кино', 'Здоровье', 'Красота', 'Искусство',
           'Подарки', 'Психология', 'Мода', 'Патрики спорт', 'Патрики дети',
           'Светская жизнь', 'Домашний любимец', 'Патрики глазами животных',
           'Блиц-интервью', 'Топ-10', 'Гид по Патриаршим']

ADS = [
    ('ad-rollsroyce', 'Rolls-Royce Motor Cars Moscow', 'Полоса под обрез, дилерский блок в подвале на отдельной линейке'),
    ('ad-ferretti', 'Ferretti Yachts / Burevestnik Group', 'Светлая полоса: заголовок разрядкой, лента интерьеров, модельный ряд'),
    ('ad-jetsmarter', 'JetSmarter', 'Иллюстрация вместо фотографии, три коротких оффера столбиком'),
    ('ad-senator', '«Сенатор», бутик мужской одежды', 'Классическая антиква и рамка — единственный серифный модуль номера'),
    ('ad-mangusta', 'Mangusta / fast & glam', 'Тёмная полоса-контрапункт после светлого разворота'),
    ('ad-grandmarina', 'Sochi Grand Marina', 'Карта и порт: инфографика в рекламном модуле'),
]

SPREADS = [
    ('spread-elka', '«В лесу родилась ёлочка»', '№9, полосы 18–19'),
    ('spread-sport', 'Патрики спорт: модуль героя', '№10, полосы 8–9'),
    ('spread-berezka', 'Bistrot Берёзка', '№10, полосы 22–23'),
]

# ── страница ────────────────────────────────────────────────────────────────
CSS = """
.pt,.pt *{box-sizing:border-box}
.pt{--ink:#14171C;--red:#D40D2E;--red-d:#9E0A22;--yellow:#FFC61E;--orange:#F08A24;
 --green:#43B02A;--paper:#F5F2EC;--rule:rgba(20,23,28,.14);--mute:#6A7078;
 font-family:'Onest',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff;
 font-size:17px;line-height:1.62;-webkit-font-smoothing:antialiased}
.pt img{max-width:100%;height:auto;display:block}
.pt-w{max-width:1180px;margin:0 auto;padding:0 40px}
.pt section{padding:86px 0}
.pt h2,.pt h3,.pt .pt-rub,.pt .pt-num{font-family:'Oswald','Oswald Fallback',Impact,sans-serif;
 text-transform:uppercase;font-weight:600;margin:0}
.pt h2{font-size:clamp(30px,4.6vw,54px);line-height:1.02;letter-spacing:-.005em}
.pt h3{font-size:22px;line-height:1.1;letter-spacing:.01em}
.pt p{margin:0 0 18px}
.pt-lead{font-size:19px;color:#3A4048;max-width:62ch}
.pt-rub{display:inline-block;font-size:15px;letter-spacing:.1em;color:var(--red);
 border-bottom:2px solid var(--red);padding-bottom:3px;margin-bottom:18px}
.pt-hd{margin-bottom:44px}
.pt-hd h2{margin-bottom:16px}
.pt-hd h2 em{font-style:normal;color:var(--red)}

/* ── ГЕРОЙ ── */
.pt-hero{background:var(--paper);padding:0 0 70px;border-bottom:3px solid var(--ink)}
.pt-mast{border-bottom:2px solid var(--ink);padding:26px 0 16px;margin-bottom:52px}
.pt-mast__in{display:flex;align-items:baseline;justify-content:space-between;gap:20px;flex-wrap:wrap}
.pt-mast b{font-family:'Oswald',Impact,sans-serif;font-weight:300;font-size:clamp(22px,3.4vw,40px);
 letter-spacing:.34em;text-transform:uppercase;line-height:1}
.pt-mast span{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}
.pt-hero__in{display:grid;grid-template-columns:1.02fr .98fr;gap:56px;align-items:center}
.pt-kick{font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;font-weight:500;
 font-size:14px;letter-spacing:.12em;color:var(--red);margin:0 0 14px}
.pt-hero h1{font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;font-weight:600;
 font-size:clamp(40px,6.6vw,84px);line-height:.94;margin:0 0 22px;letter-spacing:-.01em}
.pt-hero h1 em{font-style:normal;color:var(--red)}
.pt-hero__lead{font-size:20px;line-height:1.55;color:#2B3038;max-width:36ch}
.pt-metrics{display:grid;grid-template-columns:repeat(4,auto);gap:0;margin-top:34px;
 border-top:1px solid var(--rule)}
.pt-metrics div{padding:16px 18px 4px 0}
.pt-metrics b{display:block;font-family:'Oswald',Impact,sans-serif;font-weight:600;
 font-size:34px;line-height:1;color:var(--ink)}
.pt-metrics span{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.pt-covers{position:relative;display:flex;align-items:center;justify-content:center;gap:0}
.pt-covers img{width:52%;flex:0 0 auto;box-shadow:0 24px 60px rgba(20,23,28,.28)}
.pt-covers img:first-child{transform:rotate(-4.5deg) translateX(6%);z-index:2}
.pt-covers img:last-child{transform:rotate(4deg) translateX(-6%)}

/* ── БРИФ ── */
.pt-brief{background:#fff}
.pt-brief__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:34px}
.pt-brief__c{border-top:3px solid var(--ink);padding-top:16px}
.pt-brief__c h3{margin-bottom:10px}
.pt-brief__c p{font-size:16px;color:#3A4048;margin:0}

/* ── ВЫПУСКИ ── */
.pt-run{background:var(--paper)}
.pt-run__pic{margin:0 0 46px}
.pt-run__pic:last-child{margin-bottom:0}
.pt-run__pic img{margin:0 auto}
.pt-run__pic figcaption{margin-top:16px;padding-top:12px;border-top:1px solid var(--rule);
 font-size:15px;color:var(--mute)}
.pt-names{border-top:3px solid var(--ink);padding-top:16px;margin:0 0 46px}
.pt-names b{font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;font-weight:600;
 font-size:15px;letter-spacing:.06em;display:block;margin-bottom:8px}
.pt .pt-names p{margin:0;font-size:17px;line-height:1.7;color:#3A4048}

/* ── АНАТОМИЯ ОБЛОЖКИ ── */
.pt-cover__in{display:grid;grid-template-columns:.86fr 1.14fr;gap:52px;align-items:start}
.pt-cover__pic{position:relative;box-shadow:0 18px 50px rgba(20,23,28,.22)}
.pt-cover__zone{position:absolute;border:2px solid var(--red);background:rgba(212,13,46,.1);
 opacity:0;transition:opacity .18s;pointer-events:none}
.pt-cover__zone.on{opacity:1}
.pt-zlist{list-style:none;margin:0;padding:0;counter-reset:z}
.pt-zlist li{counter-increment:z;border-top:1px solid var(--rule);padding:18px 0 18px 54px;
 position:relative;cursor:pointer;transition:background .15s}
.pt-zlist li:last-child{border-bottom:1px solid var(--rule)}
.pt-zlist li::before{content:counter(z,decimal-leading-zero);position:absolute;left:0;top:18px;
 font-family:'Oswald',Impact,sans-serif;font-size:15px;color:var(--red);letter-spacing:.06em}
.pt-zlist li.on{background:#fff}
.pt-zlist b{display:block;font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;
 font-weight:600;font-size:17px;letter-spacing:.02em;margin-bottom:3px}
.pt-zlist span{font-size:15px;color:#3A4048}

/* ── СЕТКА ── */
.pt-grid{background:var(--paper)}
.pt-grid__in{display:grid;grid-template-columns:1.1fr .9fr;gap:52px;align-items:start}
.pt-grid__page{position:relative;background:#fff;box-shadow:0 14px 40px rgba(20,23,28,.16)}
.pt-ov{position:absolute;inset:0;pointer-events:none}
.pt-ov i{position:absolute;display:block;background:rgba(212,13,46,.16);
 outline:1px solid rgba(212,13,46,.5);transition:left .3s,width .3s,opacity .2s}
.pt-ov u{position:absolute;left:8.71%;right:8.30%;top:11.05%;height:80.33%;
 border:1px dashed rgba(20,23,28,.5)}
.pt-ov s{position:absolute;text-decoration:none;background:rgba(20,23,28,.1);
 outline:1px solid rgba(20,23,28,.35)}
.pt-ov s.r{left:8.71%;right:8.30%;top:5.59%;height:3.11%}
.pt-ov s.f{left:8.71%;right:8.30%;top:93.65%;height:1.4%}
.pt-sw{display:inline-flex;border:2px solid var(--ink);margin-bottom:26px}
.pt-sw button{appearance:none;border:0;background:#fff;cursor:pointer;padding:10px 20px;
 font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;font-size:15px;letter-spacing:.06em}
.pt-sw button.on{background:var(--ink);color:#fff}
.pt-specs{list-style:none;margin:0;padding:0}
.pt-specs li{display:flex;justify-content:space-between;gap:18px;border-bottom:1px solid var(--rule);
 padding:13px 0;font-size:16px}
.pt-specs li b{font-family:'Oswald',Impact,sans-serif;font-weight:500;letter-spacing:.02em;white-space:nowrap}
.pt-specs li span{color:var(--mute);text-align:right}

/* ── РУБРИКАТОР ── */
.pt-rubs{background:var(--ink);color:#fff}
.pt-rubs h2,.pt-rubs .pt-lead{color:#fff}
.pt-rubs .pt-lead{color:rgba(255,255,255,.72)}
.pt-rubs .pt-rub{color:var(--yellow);border-color:var(--yellow)}
.pt-tags{display:flex;flex-wrap:wrap;gap:10px}
.pt-tags b{font-family:'Oswald',Impact,sans-serif;font-weight:500;text-transform:uppercase;
 font-size:17px;letter-spacing:.05em;border:1px solid rgba(255,255,255,.3);padding:9px 15px}
.pt-tags b:nth-child(3n){color:var(--yellow);border-color:rgba(255,198,30,.55)}

/* ── ЗАГОЛОВКИ ── */
.pt-heads__grid{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.pt-demo{border:1px solid var(--rule);padding:34px;display:flex;flex-direction:column}
.pt .pt-demo__cap{font-size:14px;color:var(--mute);margin:auto 0 0;padding-top:22px}
.pt-h2c{font-family:'Oswald',Impact,sans-serif;font-weight:600;text-transform:uppercase;
 font-size:clamp(28px,3.6vw,44px);line-height:.98}
.pt-h2c em{font-style:normal;color:var(--red)}
.pt-h2c i{font-style:normal;color:var(--orange)}
.pt-plate{position:relative;background:var(--red);color:#fff;padding:26px 26px 22px;overflow:hidden}
.pt-plate::before{content:"";position:absolute;left:0;top:0;bottom:0;width:64px;
 background:repeating-linear-gradient(90deg,rgba(255,255,255,.16) 0 6px,transparent 6px 16px)}
.pt-plate b{position:relative;display:block;font-family:'Oswald',Impact,sans-serif;font-weight:600;
 text-transform:uppercase;font-size:clamp(26px,3.4vw,40px);line-height:.98}
.pt-plate span{position:relative;display:block;margin-top:12px;font-size:14px;line-height:1.35;
 color:rgba(255,255,255,.85)}

/* ── ВРЕЗКИ ── */
.pt-calls{background:var(--paper)}
.pt-calls__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:30px}
.pt-call{background:#fff;padding:26px;margin:0;display:flex;flex-direction:column}
.pt-call__cap{font-size:14px;color:var(--mute);margin:auto 0 0;padding-top:20px}
.pt-star{border:2px solid var(--red);padding:20px}
.pt-star__row{display:flex;justify-content:center;gap:8px;margin:-32px 0 12px}
.pt-star__row svg{width:22px;height:22px;fill:#fff;stroke:var(--red);stroke-width:1.6}
.pt-star__row svg:nth-child(3){width:30px;height:30px;margin-top:-4px}
.pt-star p{font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;font-weight:500;
 font-size:19px;line-height:1.22;text-align:center;margin:0}
.pt-star p em{font-style:normal;color:var(--red)}
.pt-rulez{border-top:2px solid var(--red);border-bottom:2px solid var(--red);padding:18px 0}
.pt-rulez p{font-family:'PT Serif',Georgia,serif;font-style:italic;color:var(--red);
 font-size:19px;line-height:1.35;text-align:center;margin:0}
.pt-diag{position:relative;background:#1B1E24;color:#fff;padding:34px 26px;overflow:hidden}
.pt-diag::before,.pt-diag::after{content:"";position:absolute;left:-20%;right:-20%;height:38%;
 background:rgba(255,255,255,.07);transform:rotate(-9deg)}
.pt-diag::before{top:8%}
.pt-diag::after{bottom:2%}
.pt-diag p{position:relative;margin:0;font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;
 font-weight:500;font-size:20px;line-height:1.24}
.pt-diag p em{font-style:normal;color:var(--yellow);font-weight:600;font-size:26px}

/* ── ЛИСТАЛКА ── */
.pt-flip__top{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;flex-wrap:wrap}
.pt-issues{display:inline-flex;border:2px solid var(--ink)}
.pt-issues button{appearance:none;border:0;background:#fff;cursor:pointer;padding:12px 22px;text-align:left;
 font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;font-size:15px;letter-spacing:.05em}
.pt-issues button small{display:block;font-size:11px;letter-spacing:.05em;color:var(--mute);margin-top:3px}
.pt-issues button.on{background:var(--ink);color:#fff}
.pt-issues button.on small{color:rgba(255,255,255,.6)}
.pt-stage{display:grid;grid-template-columns:64px 1fr 64px;align-items:center;gap:18px;margin-top:34px}
.pt-stage__pic{position:relative;background:var(--paper);padding:26px}
.pt-stage__pic img{margin:0 auto;max-height:78vh;width:auto;box-shadow:0 16px 44px rgba(20,23,28,.22)}
.pt-arrow{appearance:none;width:64px;height:64px;border:2px solid var(--ink);background:#fff;
 cursor:pointer;font-size:24px;line-height:1;transition:background .15s,color .15s}
.pt-arrow:hover{background:var(--ink);color:#fff}
.pt-cap{display:flex;justify-content:space-between;gap:20px;align-items:baseline;
 margin:18px 0 0;padding-top:12px;border-top:1px solid var(--rule);font-size:16px}
.pt-cap b{font-family:'Oswald',Impact,sans-serif;font-weight:500;letter-spacing:.04em;
 text-transform:uppercase;color:var(--red);white-space:nowrap}
.pt-strip{display:flex;gap:8px;overflow-x:auto;padding:22px 2px 8px;scroll-behavior:smooth}
.pt-strip button{appearance:none;border:0;background:none;padding:0;cursor:pointer;flex:0 0 auto;
 line-height:0;opacity:.55;outline:2px solid transparent;transition:opacity .15s,outline-color .15s}
.pt-strip button.on,.pt-strip button:hover{opacity:1;outline-color:var(--red)}
.pt-strip img{width:64px;height:auto}

/* ── РЕКЛАМА ── */
.pt-ads{background:var(--paper)}
.pt-ads__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:30px}
.pt-ad img{box-shadow:0 12px 32px rgba(20,23,28,.18)}
.pt-ad{margin:0}
.pt-ad b{display:block;font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;font-weight:600;
 font-size:16px;letter-spacing:.03em;margin:16px 0 5px}
.pt-ad span{font-size:15px;color:#3A4048}

/* ── В ПЕЧАТИ ── */
.pt-print__list{display:grid;gap:52px}
.pt-print__i{margin:0}
.pt-print__i figcaption{display:flex;justify-content:space-between;gap:18px;align-items:baseline;
 margin-top:14px;padding-top:12px;border-top:1px solid var(--rule)}
.pt-print__i b{font-family:'Oswald',Impact,sans-serif;text-transform:uppercase;font-weight:600;font-size:17px}
.pt-print__i span{font-size:15px;color:var(--mute);white-space:nowrap}
.pt-paper{background:var(--paper);padding:34px;box-shadow:inset 0 0 0 1px var(--rule)}
.pt-paper img{box-shadow:0 18px 44px rgba(20,23,28,.24)}

/* ── РЕЗУЛЬТАТ ── */
.pt-res{background:var(--ink);color:#fff}
.pt-res h2{color:#fff}
.pt-res .pt-rub{color:var(--yellow);border-color:var(--yellow)}
.pt-res__grid{display:grid;grid-template-columns:repeat(2,1fr);gap:0 44px}
.pt-res__grid div{border-top:1px solid rgba(255,255,255,.18);padding:20px 0;display:flex;gap:16px}
.pt-res__grid b{font-family:'Oswald',Impact,sans-serif;font-weight:500;color:var(--yellow);
 font-size:15px;letter-spacing:.06em;padding-top:3px}
.pt-res__grid p{margin:0;color:rgba(255,255,255,.86);font-size:16px}

@media(max-width:1000px){
 .pt-hero__in,.pt-cover__in,.pt-grid__in,.pt-heads__grid{grid-template-columns:1fr;gap:36px}
 .pt-brief__grid,.pt-calls__grid,.pt-ads__grid{grid-template-columns:1fr}
 .pt-res__grid{grid-template-columns:1fr}
 .pt-covers img{width:46%}
}
@media(max-width:860px){
 .pt-w{padding:0 18px}
 .pt section{padding:56px 0}
 .pt-metrics{grid-template-columns:1fr 1fr}
 .pt-stage{grid-template-columns:1fr 1fr;gap:12px}
 .pt-stage__pic{padding:0;background:none;order:-1;grid-column:1/-1}
 .pt-arrow{width:100%;height:52px}
 .pt-cap{flex-direction:column;gap:6px}
 .pt-flip__top{align-items:flex-start}
}
@media(prefers-reduced-motion:reduce){.pt *{transition:none!important}.pt-strip{scroll-behavior:auto}}
"""


def zones():
    z = [
        ('Логотип издания', 'Сова в академической шапочке на радуге и монограмма «iK» — знак издателя, агентства «Ай Кей».', 6.5, 3.2, 23.5, 22.5),
        ('Шапка и номер', 'PATRIKI TIMES набран разрядкой в два яруса, номер выпуска повёрнут на 90° у правого края.', 35.5, 3.2, 59.5, 16.5),
        ('Строка издания', '«Ежемесячное издание, г. Москва» и слоган «где, как, когда и с кем» — две строки разной разрядки.', 32.5, 19.0, 62.0, 7.5),
        ('Фотография героя', 'Портрет уходит под обрез с трёх сторон и держит всю нижнюю часть обложки.', 0.0, 26.8, 100.0, 73.2),
        ('Анонсы номера', 'Три-четыре темы: жёлтым и оранжевым — рубрики, белым — герой обложки.', 3.5, 73.0, 59.5, 22.5),
    ]
    li, ov = [], []
    for i, (t, d, x, y, w, h) in enumerate(z):
        li.append(f'<li data-z="{i}"><b>{t}</b><span>{d}</span></li>')
        ov.append(f'<div class="pt-cover__zone" data-z="{i}" style="left:{x}%;top:{y}%;width:{w}%;height:{h}%"></div>')
    return '\n'.join(li), '\n'.join(ov)


ZLIST, ZONES = zones()
STAR = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.6l2.9 6 6.6.9-4.8 4.6 1.2 6.5-5.9-3.1-5.9 3.1 1.2-6.5L2.5 9.5l6.6-.9z"/></svg>')

RUBS = ''.join(f'<b>{r}</b>' for r in RUBRICS)
ADS_HTML = '\n'.join(
    f'<figure class="pt-ad"><img src="/images/patriki/{f}.jpg" alt="Рекламный модуль {t} в журнале Patriki Times"'
    f' width="820" height="1160" loading="lazy"><figcaption><b>{t}</b><span>{d}</span></figcaption></figure>'
    for f, t, d in ADS)
SPREADS_HTML = '\n'.join(
    f'<figure class="pt-print__i"><div class="pt-paper"><img src="/images/patriki/{f}.jpg"'
    f' alt="Разворот журнала Patriki Times: {t}" width="2000" height="1414" loading="lazy"></div>'
    f'<figcaption><b>{t}</b><span>{n}</span></figcaption></figure>'
    for f, t, n in SPREADS)

RESULT = [
    ('01', 'Издание вышло девятнадцать раз: сетка и правила полосы выдержали весь ежемесячный цикл без переделок.'),
    ('02', 'Рубрикатор из 18 разделов: читатель определяет тему по одному слову в углу полосы.'),
    ('03', 'Заголовочная система из двух начертаний и трёх цветов одинаково держит и блиц-интервью, и фоторепортаж со светского вечера.'),
    ('04', 'Рекламные модули соседей — от Rolls-Royce и Ferretti до Tiffany & Co. и Brioni — встали в номер, не споря с редакционными полосами.'),
    ('05', 'Каждый номер уходил в типографию в 4+4 на A4 — с готовым препрессом, без правок на приладке.'),
    ('06', 'Те же полосы переиспользовались для интернет-версии журнала без переверстки.'),
    ('07', 'Готовая система сократила срок сборки: следующий номер собирался быстрее предыдущего при том же объёме материалов.'),
    ('08', 'Обложка пережила смену шапки: к №17 добавились герб и новая строка, состав блоков остался прежним.'),
]
RESULT_HTML = '\n'.join(f'<div><b>{n}</b><p>{t}</p></div>' for n, t in RESULT)

JS_PAGES = '{' + ','.join(
    '"%d":[%s]' % (k, ','.join('[%d,"%s"]' % (n, c.replace('"', '\\"')) for n, c in v))
    for k, v in PAGES.items()) + '}'

HTML = f"""<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Журнал Patriki Times: дизайн издания и ежемесячная вёрстка | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: ежемесячный журнал Patriki Times о Патриарших прудах. Дизайн издания и сетка полос, рубрикатор, заголовочная система, оформление статей, интервью и рекламных модулей, макеты в типографию и под интернет-версию. Ежемесячная вёрстка номер за номером.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hand-marketing.ru/creative/patriki/">
<meta property="og:type" content="article">
<meta property="og:title" content="Журнал Patriki Times — кейс Hand Marketing">
<meta property="og:description" content="Дизайн издания, сетка полос, рубрикатор и заголовочная система — и ежемесячная вёрстка номеров журнала о Патриарших прудах.">
<meta property="og:url" content="https://hand-marketing.ru/creative/patriki/">
<meta property="og:image" content="https://hand-marketing.ru/images/patriki/cover9.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
<link href="/fonts/montserrat.css" rel="stylesheet"><link href="/fonts/oswald-onest.css" rel="stylesheet">
{CHROME_CSS}
<style id="pt-css">{CSS}</style>{METRIKA}
</head>
<body>{HDR}<main class="pt">

<header class="pt-hero">
 <div class="pt-mast"><div class="pt-w pt-mast__in"><b>Patriki Times</b><span>Ежемесячное издание, г. Москва · где, как, когда и с кем</span></div></div>
 <div class="pt-w pt-hero__in">
  <div>
   <p class="pt-kick">Ежемесячная вёрстка, 2018–2021</p>
   <h1>Журнал<br><em>Patriki Times</em></h1>
   <p class="pt-hero__lead">Глянцевое издание о Патриарших прудах: рестораторы, врачи, спортсмены, коллекционеры и сами жители района. Мы разработали дизайн журнала и сетку полос, а дальше вели ежемесячный выпуск: статьи, интервью, рекламные модули, макеты в типографию и под интернет-версию.</p>
   <div class="pt-metrics">
    <div><b>19</b><span>номеров вышло</span></div>
    <div><b>52–68</b><span>полос в номере</span></div>
    <div><b>18</b><span>рубрик</span></div>
    <div><b>A4</b><span>210×297, 4+4</span></div>
   </div>
  </div>
  <div class="pt-covers">
   <img src="/images/patriki/cover9.jpg" alt="Обложка журнала Patriki Times №9, январь-февраль 2018" width="1300" height="1838">
   <img src="/images/patriki/cover10.jpg" alt="Обложка журнала Patriki Times №10, февраль-март 2018" width="1300" height="1838" loading="lazy">
  </div>
 </div>
</header>

<section class="pt-brief"><div class="pt-w">
 <div class="pt-brief__grid">
  <div class="pt-brief__c"><h3>Компания</h3><p>Patriki Times — ежемесячный глянцевый журнал о лучших местах центра Москвы. Издатель — агентство «Ай Кей», главный редактор Ирсон Кудикова.</p></div>
  <div class="pt-brief__c"><h3>Задача</h3><p>Разработать дизайн журнала, включая сетку полос для ежемесячного выпуска. Оформить статьи, рекламные модули и интервью. Подготовить макеты для типографии и вёрстку интернет-версии.</p></div>
  <div class="pt-brief__c"><h3>Что сделали</h3><p>Модульную сетку и правила полосы, рубрикатор из 18 разделов, заголовочную систему и типы врезок, оформление рекламных модулей, препресс двух номеров.</p></div>
 </div>
</div></section>

<section class="pt-run"><div class="pt-w">
 <div class="pt-hd"><span class="pt-rub">Выпуски</span><h2>Номер <em>за номером</em></h2>
  <p class="pt-lead">Журнал выходил ежемесячно, поэтому вёрстка была не разовым макетом, а постоянной работой. От номера к номеру менялись герой обложки, темы и рекламодатели — правила полосы оставались прежними, и каждый следующий выпуск собирался быстрее предыдущего.</p></div>
 <figure class="pt-run__pic">
  <img src="/images/lib/as3332-3131-4438-a262-363937623539/2.png" alt="Обложки разных номеров журнала Patriki Times" width="1660" height="1200" loading="lazy">
  <figcaption>Обложки разных лет. У №9 и №11 шапка со слоганом «где, как, когда и с кем»; к №17 и №19 она обновилась: добавились герб, строка «лучшие люди и места центра» и номер решёткой. Набор блоков при этом не изменился.</figcaption>
 </figure>
 <div class="pt-names"><b>Герои номеров</b>
  <p>Александр Розенбаум · Аркадий Новиков · Сергей Мазаев · Гоша Куценко · Игорь Цвирко · Этери Аскерова · Алексей Фурсин · Алексей Филатов · Алимжан Тохтахунов · Владимир Малёшин · Дмитрий Ефимов · Вероника Smirnoff · Андрей Шаронов · Генрих Карпин · Аркадий Дворкович · Павел Колобков</p>
 </div>
 <figure class="pt-run__pic">
  <img src="/images/lib/as3135-3335-4734-a337-396563373033/photo.png" alt="Развороты из разных номеров журнала Patriki Times" width="1660" height="1200" loading="lazy">
  <figcaption>Развороты из разных номеров: рестораны, мода, красота, бизнес — и рекламные полосы соседей, от Ess-Thetik и Scampi до Tiffany&nbsp;&amp;&nbsp;Co. и Brioni.</figcaption>
 </figure>
</div></section>

<section class="pt-cover"><div class="pt-w">
 <div class="pt-hd"><span class="pt-rub">Обложка</span><h2>Пять постоянных <em>элементов</em></h2>
  <p class="pt-lead">Обложка собирается из одних и тех же блоков — меняются только герой и анонсы. Разбираем на №9; в поздних номерах шапка обновилась, но состав блоков остался тем же. Наведите на пункт списка, чтобы увидеть его место на полосе.</p></div>
 <div class="pt-cover__in">
  <div class="pt-cover__pic" id="pt-cpic">
   <img src="/images/patriki/cover9.jpg" alt="Разбор обложки журнала Patriki Times №9" width="1300" height="1838" loading="lazy">
   {ZONES}
  </div>
  <ul class="pt-zlist" id="pt-zlist">{ZLIST}</ul>
 </div>
</div></section>

<section class="pt-grid"><div class="pt-w">
 <div class="pt-hd"><span class="pt-rub">Сетка</span><h2>Модульная <em>полоса</em></h2>
  <p class="pt-lead">Живое поле одно на весь журнал, меняется только число колонок: текстовые материалы идут в три, интервью и врезки — в две. Средник и поля не двигаются никогда.</p></div>
 <div class="pt-grid__in">
  <div>
   <div class="pt-grid__page" id="pt-gpage">
    <img src="/images/patriki/grid-3col.jpg" id="pt-gimg" alt="Типовая текстовая полоса журнала Patriki Times с наложенной модульной сеткой" width="1200" height="1697" loading="lazy">
    <div class="pt-ov" id="pt-ov" aria-hidden="true"><u></u><s class="r"></s><s class="f"></s></div>
   </div>
  </div>
  <div>
   <div class="pt-sw" role="group" aria-label="Число колонок">
    <button type="button" class="on" data-cols="3">3 колонки</button>
    <button type="button" data-cols="2">2 колонки</button>
   </div>
   <ul class="pt-specs">
    <li><b>Формат</b><span>A4 210×297 мм, вылеты 5 мм</span></li>
    <li><b>Поля</b><span>18 мм слева и справа</span></li>
    <li><b>Живое поле</b><span>174,3 × 238,6 мм</span></li>
    <li><b>Колонка</b><span id="pt-colw">55,8 мм · три колонки</span></li>
    <li><b>Средник</b><span>3,45 мм</span></li>
    <li><b>Рубрика</b><span>верхнее поле, 17 мм от обреза</span></li>
    <li><b>Колонтитул</b><span>нижнее поле, 16 мм от обреза</span></li>
    <li><b>Красочность</b><span>4+4, полноцвет</span></li>
   </ul>
  </div>
 </div>
</div></section>

<section class="pt-rubs"><div class="pt-w">
 <div class="pt-hd"><span class="pt-rub">Навигация</span><h2>Восемнадцать <em>рубрик</em></h2>
  <p class="pt-lead">Одно слово узким гротеском в верхнем поле — единственный навигационный элемент внутри номера. Ни колонцифр по разделам, ни цветного обреза: читатель ориентируется по рубрике и колонтитулу.</p></div>
 <div class="pt-tags">{RUBS}</div>
</div></section>

<section class="pt-heads"><div class="pt-w">
 <div class="pt-hd"><span class="pt-rub">Заголовки</span><h2>Два начертания, <em>три цвета</em></h2>
  <p class="pt-lead">Заголовок всегда узкий гротеск капсом. Смысловое слово выделяется цветом, а не кеглем — так материал читается с разворота, но полоса не рассыпается.</p></div>
 <div class="pt-heads__grid">
  <div class="pt-demo">
   <div class="pt-h2c">Чемпионат <em>мира</em><br>по футболу</div>
   <p class="pt-demo__cap">Редакционный заголовок: цветом выделено одно слово, вторая строка меньшим кеглем.</p>
  </div>
  <div class="pt-demo">
   <div class="pt-h2c"><i>Карл</i><br><i>Фаберже</i></div>
   <p class="pt-demo__cap">Историческая рубрика: заголовок ложится на фотографию, цвет берётся из кадра.</p>
  </div>
  <div class="pt-demo">
   <div class="pt-plate"><b>Маирбек<br>Хостикоев</b><span>Основатель и руководитель баскетбольного клуба СКОЛКОВО</span></div>
   <p class="pt-demo__cap">Модуль героя: красная плашка с полосками, имя и регалии. Повторяется шесть раз подряд в рубрике «Патрики спорт» и держит весь блок интервью.</p>
  </div>
  <div class="pt-demo">
   <div class="pt-h2c" style="letter-spacing:.02em">Тренды<br><em>будущего</em></div>
   <p class="pt-demo__cap">Бизнес-рубрика: заголовок целиком в цвете, набран в две строки под колонку.</p>
  </div>
 </div>
</div></section>

<section class="pt-calls"><div class="pt-w">
 <div class="pt-hd"><span class="pt-rub">Врезки</span><h2>Три типа <em>выносок</em></h2>
  <p class="pt-lead">Длинные интервью разбиваются цитатой. Тип врезки закреплён за характером материала, поэтому номер не превращается в набор случайных плашек.</p></div>
 <div class="pt-calls__grid">
  <figure class="pt-call">
   <div class="pt-star"><div class="pt-star__row">{STAR*5}</div>
    <p><em>Спорт помогает</em>, это наверно, расхожая фраза, <em>и в работе, и в отдыхе</em>. И позволяет чувствовать себя в форме.</p></div>
   <figcaption class="pt-call__cap">Спортивные материалы: рамка со звёздами, узкий гротеск, два цвета.</figcaption>
  </figure>
  <figure class="pt-call">
   <div class="pt-rulez"><p>Легенда это или нет, но вдова де Богарне не только привлекала молодого человека красотой и опытом, но и оказалась родной для него душой.</p></div>
   <figcaption class="pt-call__cap">Историческая рубрика: серифный курсив красным между двумя линейками.</figcaption>
  </figure>
  <figure class="pt-call">
   <div class="pt-diag"><p>Патриаршие для меня, как для француза, <em>эта часть столицы</em> всегда напоминала <em>узкие улочки Парижа</em>.</p></div>
   <figcaption class="pt-call__cap">Рестораны: цитата поверх фотографии, диагональные полосы и жёлтый акцент.</figcaption>
  </figure>
 </div>
</div></section>

<section class="pt-flip" id="pt-flip"><div class="pt-w">
 <div class="pt-flip__top">
  <div class="pt-hd" style="margin-bottom:0">
   <span class="pt-rub">Разбор</span><h2>Два номера <em>под лупой</em></h2>
   <p class="pt-lead" style="margin:0">Систему проще показать на выпусках целиком: №9 и №10 за 2018 год. Остальные номера собраны по тем же правилам.</p>
  </div>
  <div class="pt-issues" role="group" aria-label="Выбор номера">
   <button type="button" class="on" data-issue="9">№9<small>январь-февраль 2018 · 52 полосы</small></button>
   <button type="button" data-issue="10">№10<small>февраль-март 2018 · 68 полос</small></button>
  </div>
 </div>
 <div class="pt-stage">
  <button type="button" class="pt-arrow pt-stage__prev" id="pt-prev" aria-label="Предыдущая полоса">‹</button>
  <div class="pt-stage__pic"><img id="pt-page" src="/images/patriki/p9-1.jpg" alt="Полоса 1 журнала Patriki Times №9" width="1000" height="1414" loading="lazy"></div>
  <button type="button" class="pt-arrow pt-stage__next" id="pt-next" aria-label="Следующая полоса">›</button>
 </div>
 <p class="pt-cap"><span id="pt-cap">Обложка. Генрих Карпин, 800°C Contemporary Steak</span><b id="pt-pos">Полоса 1 · №9</b></p>
 <div class="pt-strip" id="pt-strip"></div>
</div></section>

<section class="pt-ads"><div class="pt-w">
 <div class="pt-hd"><span class="pt-rub">Реклама</span><h2>Модули <em>соседей</em></h2>
  <p class="pt-lead">Рекламу в журнале дают те, кто живёт рядом: автомобильные и яхтенные дилеры, бутики, частная авиация. Каждый модуль занимает полосу целиком, поэтому редакционный материал никогда не спорит с рекламным.</p></div>
 <div class="pt-ads__grid">{ADS_HTML}</div>
</div></section>

<section class="pt-print"><div class="pt-w">
 <div class="pt-hd"><span class="pt-rub">В печати</span><h2>Развороты <em>в номере</em></h2>
  <p class="pt-lead">Полосы верстались парами: фотополоса под обрез слева, текст справа — или наоборот. Проверка всегда шла на развороте, а не на отдельной полосе.</p></div>
 <div class="pt-print__list">{SPREADS_HTML}
  <figure class="pt-print__i"><img src="/images/lib/as3162-3135-4335-b439-336639373739/39565.png" alt="Разворот журнала Patriki Times с интервью Игоря Цвирко" width="1660" height="1200" loading="lazy">
   <figcaption><b>Игорь Цвирко, Большой театр</b><span>поздний номер</span></figcaption></figure>
 </div>
</div></section>

<section class="pt-res"><div class="pt-w">
 <div class="pt-hd"><span class="pt-rub">Результат</span><h2>Что получилось</h2></div>
 <div class="pt-res__grid">{RESULT_HTML}</div>
</div></section>

</main>{FOOT}{FORM_JS}
<script>(function(){{
 // ── анатомия обложки ──
 var zl=document.getElementById('pt-zlist'),cp=document.getElementById('pt-cpic');
 if(zl&&cp){{
  var zones=cp.querySelectorAll('.pt-cover__zone'),items=zl.querySelectorAll('li');
  function pick(i){{
   for(var k=0;k<zones.length;k++)zones[k].classList.toggle('on',k===i);
   for(var m=0;m<items.length;m++)items[m].classList.toggle('on',m===i);
  }}
  items.forEach(function(li,i){{
   li.addEventListener('mouseenter',function(){{pick(i);}});
   li.addEventListener('click',function(){{pick(i);}});
  }});
  zl.addEventListener('mouseleave',function(){{pick(-1);}});
  pick(0);
 }}

 // ── оверлей модульной сетки ──
 var ov=document.getElementById('pt-ov'),gimg=document.getElementById('pt-gimg'),
     colw=document.getElementById('pt-colw');
 var GRID={{3:{{w:26.57,g:1.646,img:'grid-3col',cap:'55,8 мм · три колонки'}},
            2:{{w:40.71,g:1.63,img:'grid-2col',cap:'85,4 мм · две колонки'}}}};
 function cols(n){{
  if(!ov)return;
  var g=GRID[n],L=8.71,html='<u></u><s class="r"></s><s class="f"></s>';
  for(var i=0;i<n;i++){{
   html+='<i style="left:'+(L+i*(g.w+g.g)).toFixed(3)+'%;width:'+g.w+'%;top:11.05%;height:80.33%"></i>';
  }}
  ov.innerHTML=html;
  if(gimg)gimg.src='/images/patriki/'+g.img+'.jpg';
  if(colw)colw.textContent=g.cap;
 }}
 var sw=document.querySelector('.pt-sw');
 if(sw){{sw.addEventListener('click',function(e){{
  var b=e.target.closest('button[data-cols]');if(!b)return;
  sw.querySelectorAll('button').forEach(function(x){{x.classList.toggle('on',x===b);}});
  cols(+b.dataset.cols);
 }});}}
 cols(3);

 // ── листалка ──
 var P={JS_PAGES};
 var issue=9,idx=0,
     img=document.getElementById('pt-page'),cap=document.getElementById('pt-cap'),
     pos=document.getElementById('pt-pos'),strip=document.getElementById('pt-strip');
 function build(){{
  strip.innerHTML=P[issue].map(function(p,i){{
   return '<button type="button" data-i="'+i+'" aria-label="Полоса '+p[0]+'">'+
    '<img src="/images/patriki/t'+issue+'-'+p[0]+'.jpg" alt="" loading="lazy" width="64"></button>';
  }}).join('');
 }}
 function show(i){{
  var list=P[issue];idx=(i+list.length)%list.length;
  var p=list[idx];
  img.src='/images/patriki/p'+issue+'-'+p[0]+'.jpg';
  img.alt='Полоса '+p[0]+' журнала Patriki Times №'+issue+': '+p[1];
  cap.textContent=p[1];
  pos.textContent='Полоса '+p[0]+' · №'+issue;
  var bs=strip.querySelectorAll('button');
  for(var k=0;k<bs.length;k++)bs[k].classList.toggle('on',k===idx);
  var cur=bs[idx];
  if(cur)strip.scrollTo({{left:cur.offsetLeft-strip.clientWidth/2+cur.clientWidth/2,behavior:'smooth'}});
 }}
 document.getElementById('pt-prev').addEventListener('click',function(){{show(idx-1);}});
 document.getElementById('pt-next').addEventListener('click',function(){{show(idx+1);}});
 strip.addEventListener('click',function(e){{
  var b=e.target.closest('button[data-i]');if(b)show(+b.dataset.i);
 }});
 document.querySelector('.pt-issues').addEventListener('click',function(e){{
  var b=e.target.closest('button[data-issue]');if(!b)return;
  this.querySelectorAll('button').forEach(function(x){{x.classList.toggle('on',x===b);}});
  issue=+b.dataset.issue;build();show(0);
 }});
 document.addEventListener('keydown',function(e){{
  if(e.key!=='ArrowLeft'&&e.key!=='ArrowRight')return;
  var f=document.getElementById('pt-flip').getBoundingClientRect();
  if(f.top>window.innerHeight*.5||f.bottom<window.innerHeight*.5)return;
  show(e.key==='ArrowLeft'?idx-1:idx+1);
 }});
 build();show(0);
}})();</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"}},{{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"}},{{"@type":"ListItem","position":3,"name":"Журнал Patriki Times","item":"https://hand-marketing.ru/creative/patriki/"}}]}}</script></body></html>"""

os.makedirs(os.path.dirname(DST), exist_ok=True)
open(DST, 'w', encoding='utf-8').write(HTML)
print(f'{DST}: {len(HTML) // 1024} КБ')
