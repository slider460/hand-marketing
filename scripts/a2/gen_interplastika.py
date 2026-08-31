#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/interplastika/index.html: кейс «Обзорный ролик
выставки интерпластика» для Messe Düsseldorf.

Материал ровно один: сам ролик, 2:12. Ни фотографий со съёмки, ни брифа,
ни макетов не сохранилось, год клиент просил не ставить. Поэтому вся
фактура страницы снята с ролика алгоритмом (scripts/interplastika-assets.py):
кадры, тайм-коды стендов, склейки, ритм монтажа, палитра.

Идея страницы. Обзорный ролик про выставку продаёт не съёмку, а саму
выставку: за две минуты в кадре проходит вся отрасль — от гранулы сырья
до готового изделия. Значит и страница должна быть устроена как отрасль,
а не как хронометраж.

  • «Цепочка передела» — главный разбор: четыре ступени (сырьё, компаунды,
    машины, изделия), на каждой стоят компании, чьи стенды читаются в кадре.
    По схеме идёт живой поток гранул на canvas: труба перестраивается под
    ширину экрана, отводы приходят ровно в те карточки, что стоят в DOM.
    Клик по карточке перематывает плеер на её секунду.
  • «Литник» — механика, которой на сайте ещё не было: симулятор заполнения
    пресс-формы. Ставишь литник, и поле честно считает геодезическое время
    течения расплава по контуру детали (Дейкстра по сетке), рисует изохроны,
    показывает линии спая в местах, где фронты сходятся после обхода
    отверстий, и последнюю точку заполнения. Это ровно то, чем занимаются
    все машины и все марки сырья из ролика.
  • Витрина сырья: марки прочитаны с табличек в кадре (ПЭ2НТ22-12, PC-007 UL).
  • План площадки перерисован вектором с указателя, который стоит финальным
    кадром ролика: синим интерпластика, красным upakovka.
  • Ритм монтажа отдельным небольшим блоком в самом низу: он про нашу
    работу, а не про масштаб клиента, поэтому не претендует на главное место.

Шрифты: Jura (чертёжный техно-гротеск, заголовки прописными) + Nunito Sans.
Палитра снята с плана площадки.

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

IMG = '/images/interplastika'
URL = 'https://hand-marketing.ru/video/interplastika/'
TITLE = 'Обзорный ролик выставки интерпластика, Messe Düsseldorf | Hand Marketing'
DESCR = ('Обзорный ролик выставки полимеров интерпластика в ЦВК «Экспоцентр» '
         'для Messe Düsseldorf: регистрация, стенды сырьевых компаний '
         'и производителей машин, деловая программа. Разбор кейса: цепочка '
         'передела отрасли, симулятор заполнения пресс-формы, план площадки.')

MAP = json.load(open(os.path.join(HERE, 'interplastika_map.json'), encoding='utf-8'))
PAL = MAP['palette']
WHAT = {k: v['what'] for k, v in MAP['stills'].items()}
SEC = {k: v['sec'] for k, v in MAP['stills'].items()}
VIDEO = MAP['video']

# титры отделены от съёмки: первый «план» в разборе это заставка целиком
SHOTS = MAP['shots'][1:]
N_SHOTS = len(SHOTS)
LENS = [round(b - a, 2) for a, b in SHOTS]
MEAN = round(sum(LENS) / len(LENS), 2)
BEAT = MAP['beat']
BPM = MAP['bpm']
ON_GRID = MAP['on_grid']
DURATION = MAP['duration']
TITLES_UNTIL = MAP['titles_until']

# сколько компаний читается на стендах в кадре (без обезличенных карточек)
BRANDS = [i for s in MAP['chain'] for i in s['items']
          if i['id'] not in ('crates', 'headlight', 'phone-shells', 'bottles')]

# ─── титры ролика, слово в слово ───────────────────────────────────────────
TITLES = ['28–31 января', 'Москва', 'ЦВК «Экспоцентр»', 'интерпластика']

# ─── маршрут обзора: (секунда, заголовок, что происходит, кадр) ────────────
ROUTE = [
    (14.6, 'Вход и регистрация', 'Ролик начинается там же, где начинается '
     'выставка для посетителя: анкета на стойке, сканер, печать бейджа.',
     'reg-desk'),
    (28.6, 'Навигация', 'Указатель с планом площадки: куда идти и что где '
     'стоит.', 'plan-early'),
    (31.4, 'Машины в работе', 'Термопласт-автоматы и экструзия не стоят '
     'экспонатами, а льют и режут прямо на стендах.', 'press'),
    (43.2, 'Деловая программа', 'Доклады при полном зале: выставка это ещё '
     'и площадка отраслевых конференций.', 'forum'),
    (63.4, 'Сырьё и компаунды', 'Стенды химических компаний: марки, '
     'рецептуры, образцы в витринах.', 'mcpp'),
    (84.2, 'Применения', 'Витрины с готовыми деталями: фары, корпуса, '
     'арматура, медицинские изделия.', 'applications'),
    (100.6, 'Залы целиком', 'Общие планы: масштаб застройки и поток людей '
     'между стендами.', 'hall-engel'),
    (118.5, 'Гранулы крупно', 'Витрины с сырьём и табличками марок: то, '
     'с чего начинается любое изделие в зале.', 'granule-row'),
    (130.1, 'План площадки', 'Финальный кадр возвращает к указателю: '
     'интерпластика синим, upakovka красным.', 'plan'),
]

# ─── план ЦВК «Экспоцентр»: перерисован с указателя из финального кадра ───
# координаты плановые (u вдоль Красногвардейского проезда, v поперёк,
# к набережной), в SVG уходят через изометрию iso()
HALLS = [
    ('p6', 'Пав. 6', 'other', 22, 2, 74, 16),
    ('p2', 'Пав. 2', 'upakovka', 44, 28, 148, 40),
    ('p3', 'Пав. 3', 'inter', 8, 82, 66, 34),
    ('p8', 'Пав. 8', 'inter', 92, 78, 110, 28),
    ('p1', 'Пав. 1', 'inter', 212, 42, 80, 78),
    ('p5', 'Пав. 5', 'other', 250, 132, 70, 34),
    ('p7', 'Пав. 7', 'other', 18, 132, 88, 44),
    ('forum', 'Форум', 'inter', 106, 122, 60, 38),
    ('p4', 'Пав. 4', 'other', 150, 168, 46, 28),
]
# изометрия: экран = (ox + (u-v)*KX, oy + (u+v)*KY), здания с боковой гранью
ISO = dict(ox=300, oy=70, kx=1.62, ky=0.58, lift=13)

# ─── детали для симулятора формы ──────────────────────────────────────────
# контуры рисуются кодом в JS, здесь только подписи и связь с роликом
PARTS = [
    ('crate', 'Ящик', 'Решётчатый ящик: борта, дно в перфорации. '
     'Такие снимает робот с машины на 38-й секунде ролика.', 38.4),
    ('shell', 'Корпус', 'Тонкостенный корпус с вырезами. Поликарбонатные '
     'корпуса идут по конвейеру на 123-й секунде.', 123.0),
    ('rotor', 'Крыльчатка', 'Диск со спицами и зубчатым венцом: спицы '
     'разрезают поток и дают самые заметные линии спая.', 84.0),
]


CSS = """<style id="ip-css">
/* Кейс «Обзорный ролик выставки интерпластика». Чертёжная сетка, синий
   интерпластики и красный upakovka сняты с плана площадки в финальном
   кадре ролика. Правки только в gen_interplastika.py. */
.ip{--blue:%BLUE%;--red:%RED%;--ink:#12141B;--mute:#5C616E;--line:rgba(18,20,27,.13);
 --paper:#fff;--sheet:#F3F4F7;--night:#0F1117;--night2:#171A22;--lineN:rgba(255,255,255,.14);
 --green:#7CB518;--amber:#F2A104;
 font-family:'Nunito Sans',Arial,sans-serif;color:var(--ink);background:var(--paper);
 font-size:17px;line-height:1.62;overflow-x:hidden}
.ip *,.ip *::before,.ip *::after{box-sizing:border-box}
.ip h1,.ip h2,.ip h3,.ip h4,.ip .j{font-family:'Jura',Arial,sans-serif;font-weight:600}
.ip p{margin:0 0 16px}
.ip section{padding:82px 40px}
.ip .in{max-width:1200px;margin:0 auto}
.ip .lbl{font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:12px;
 letter-spacing:.24em;text-transform:uppercase;color:var(--blue);margin:0 0 16px}
.ip h2{font-size:clamp(27px,4vw,46px);line-height:1.06;margin:0 0 20px;letter-spacing:.005em}
.ip h3{font-size:clamp(19px,2.2vw,25px);line-height:1.2;margin:0 0 12px}
.ip .lead{font-size:clamp(17px,1.65vw,20px);line-height:1.55;max-width:790px;color:var(--mute)}
.ip .night{background:var(--night);color:#E8EAF0}
.ip .night .lead,.ip .night .mute{color:rgba(232,234,240,.62)}
.ip .night h2,.ip .night h3,.ip .night h4{color:#fff}
.ip .night .lbl{color:#8E9BFF}
.ip img{max-width:100%;display:block}
.ip .cap{margin-top:10px;font-size:13px;line-height:1.45;color:var(--mute)}
.ip .night .cap{color:rgba(232,234,240,.55)}
.ip .rv{opacity:0;transform:translateY(18px);transition:opacity .6s,transform .6s}
.ip .rv.on{opacity:1;transform:none}

/* ── обложка: титры ролика набираются на экране ───────────────────────── */
.ip-hero{position:relative;padding:0;background:var(--night);color:#fff;overflow:hidden}
.ip-hero__bg{position:absolute;inset:0}
.ip-hero__bg img{width:100%;height:100%;object-fit:cover;opacity:.34;
 filter:grayscale(.35) contrast(1.05)}
.ip-hero__bg::after{content:"";position:absolute;inset:0;
 background:linear-gradient(180deg,rgba(15,17,23,.55) 0%,rgba(15,17,23,.86) 62%,var(--night) 100%)}
.ip-hero__in{position:relative;max-width:1200px;margin:0 auto;padding:44px 40px 54px}
.ip-back{display:inline-block;font-size:14px;color:rgba(255,255,255,.6);text-decoration:none;margin-bottom:30px}
.ip-back:hover{color:#fff}
.ip-titles{margin:14px 0 26px;min-height:184px}
.ip-titles div{font-family:'Jura',Arial,sans-serif;font-weight:500;
 font-size:clamp(15px,1.8vw,20px);letter-spacing:.32em;text-transform:uppercase;
 color:rgba(255,255,255,.72);line-height:2.1;opacity:0;transform:translateY(6px);
 transition:opacity .5s,transform .5s}
.ip-titles div.on{opacity:1;transform:none}
.ip-titles div:last-child{font-weight:700;font-size:clamp(30px,6.4vw,72px);
 letter-spacing:.06em;color:#fff;line-height:1.1;margin-top:12px}
.ip-hero h1{font-size:clamp(21px,2.5vw,30px);font-weight:500;line-height:1.25;
 margin:0 0 18px;color:#fff;max-width:820px}
.ip-hero .lead{color:rgba(232,234,240,.72);max-width:720px}
.ip-facts{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--lineN);
 border:1px solid var(--lineN);margin-top:38px}
.ip-facts div{background:var(--night);padding:20px 18px}
.ip-facts b{display:block;font-family:'Jura',Arial,sans-serif;font-weight:700;
 font-size:clamp(22px,2.6vw,32px);color:#fff;line-height:1.1;margin-bottom:6px}
.ip-facts span{font-size:13.5px;line-height:1.4;color:rgba(232,234,240,.6)}

/* ── бриф ─────────────────────────────────────────────────────────────── */
.ip-brief{display:grid;grid-template-columns:repeat(3,1fr);gap:38px}
.ip-brief .col p:last-child{margin-bottom:0}
.ip-brief .col{border-top:2px solid var(--ink);padding-top:18px}
.ip-brief .col:nth-child(2){border-top-color:var(--blue)}
.ip-brief .col:nth-child(3){border-top-color:var(--red)}

/* ── плеер ────────────────────────────────────────────────────────────── */
.ip-player{background:var(--night2)}
.ip-player .in{max-width:1200px}
.ip-video{width:100%;display:block;background:#000;border:1px solid var(--lineN)}
.ip-route{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--lineN);
 border:1px solid var(--lineN);border-top:0;margin-bottom:0}
.ip-route button{background:var(--night2);border:0;text-align:left;cursor:pointer;
 padding:16px 18px;color:#E8EAF0;font-family:'Nunito Sans',Arial,sans-serif;
 transition:background .18s}
.ip-route button:hover,.ip-route button:focus-visible{background:#232733}
.ip-route b{display:block;font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:15px;
 letter-spacing:.02em;margin-bottom:4px}
.ip-route i{font-style:normal;font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:12px;
 letter-spacing:.1em;color:#8E9BFF;display:block;margin-bottom:6px}
.ip-route span{font-size:13.5px;line-height:1.45;color:rgba(232,234,240,.6)}

/* ── цепочка передела ─────────────────────────────────────────────────── */
.ip-chain{position:relative;margin-top:44px}
.ip-chain__flow{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0}
.ip-stages{position:relative;z-index:1;display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
.ip-stage{position:relative;padding-top:74px}
.ip-stage__port{position:absolute;top:0;left:0;width:1px;height:1px}
.ip-stage h3{font-size:19px;margin:0 0 6px;letter-spacing:.02em}
.ip-stage__n{font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:12px;
 letter-spacing:.2em;color:var(--blue);display:block;margin-bottom:8px}
.ip-stage__lead{font-size:14px;line-height:1.5;color:var(--mute);margin:0 0 18px}
.ip-card{display:block;width:100%;text-align:left;border:1px solid var(--line);
 background:var(--paper);cursor:pointer;padding:0;margin-bottom:10px;
 font-family:'Nunito Sans',Arial,sans-serif;transition:border-color .18s,transform .18s,box-shadow .18s}
.ip-card:hover,.ip-card:focus-visible{border-color:var(--blue);transform:translateY(-2px);
 box-shadow:0 10px 26px rgba(18,20,27,.1)}
.ip-card__img{position:relative;aspect-ratio:16/9;overflow:hidden;background:var(--sheet)}
.ip-card__img img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.ip-card:hover .ip-card__img img{transform:scale(1.04)}
.ip-card__t{position:absolute;left:0;bottom:0;background:var(--blue);color:#fff;
 font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:11.5px;letter-spacing:.08em;
 padding:4px 8px}
.ip-card__b{padding:12px 14px 14px}
.ip-card__b b{display:block;font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:15.5px;
 line-height:1.2;margin-bottom:4px}
.ip-card__b span{font-size:13px;line-height:1.45;color:var(--mute)}
.ip-chain__note{margin-top:26px;font-size:14px;color:var(--mute);max-width:820px}

/* ── витрина сырья ────────────────────────────────────────────────────── */
.ip-gran{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:36px}
.ip-gran figure{margin:0;border:1px solid var(--lineN);background:var(--night2)}
.ip-gran img{width:100%;aspect-ratio:16/9;object-fit:cover}
.ip-gran figcaption{padding:16px 18px 18px}
.ip-gran b{display:block;font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:18px;
 color:#fff;margin-bottom:2px}
.ip-gran em{font-style:normal;font-family:'Jura',Arial,sans-serif;font-size:13px;
 letter-spacing:.12em;color:var(--amber);display:block;margin-bottom:8px}
.ip-gran span{font-size:14px;line-height:1.5;color:rgba(232,234,240,.65)}
.ip-kos{display:flex;flex-wrap:wrap;gap:8px;margin-top:30px}
.ip-kos i{font-style:normal;font-family:'Jura',Arial,sans-serif;font-weight:500;font-size:13px;
 letter-spacing:.06em;border:1px solid var(--lineN);padding:7px 12px;color:rgba(232,234,240,.8)}

/* ── симулятор формы ──────────────────────────────────────────────────── */
.ip-mold{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(260px,1fr);gap:30px;
 margin-top:38px;align-items:start}
.ip-mold__stage{position:relative;border:1px solid var(--lineN);background:#0A0C11}
.ip-mold__cv{display:block;width:100%;height:auto;cursor:crosshair;touch-action:manipulation}
.ip-mold__hint{position:absolute;left:14px;bottom:12px;font-family:'Jura',Arial,sans-serif;
 font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.5);
 pointer-events:none}
.ip-mold__side h4{font-size:17px;margin:0 0 10px}
.ip-parts{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
.ip-parts button,.ip-mold__btn{font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:12.5px;
 letter-spacing:.1em;text-transform:uppercase;padding:9px 14px;cursor:pointer;
 border:1px solid var(--lineN);background:transparent;color:rgba(232,234,240,.75);
 transition:background .18s,color .18s,border-color .18s}
.ip-parts button:hover,.ip-mold__btn:hover{border-color:#8E9BFF;color:#fff}
.ip-parts button[aria-pressed=true]{background:#fff;color:var(--night);border-color:#fff}
.ip-mold__desc{font-size:14px;line-height:1.55;color:rgba(232,234,240,.65);margin-bottom:18px}
.ip-mold__read{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--lineN);
 border:1px solid var(--lineN);margin-bottom:16px}
.ip-mold__read div{background:var(--night);padding:14px 14px}
.ip-mold__read b{display:block;font-family:'Jura',Arial,sans-serif;font-weight:700;
 font-size:23px;color:#fff;line-height:1.1}
.ip-mold__read span{font-size:12.5px;color:rgba(232,234,240,.55)}
.ip-mold__legend{display:flex;flex-direction:column;gap:7px;margin:16px 0 18px;
 font-size:13px;color:rgba(232,234,240,.7)}
.ip-mold__legend i{display:inline-block;width:22px;height:8px;margin-right:9px;
 vertical-align:middle;border-radius:1px}
.ip-mold__row{display:flex;gap:8px;flex-wrap:wrap}
.ip-mold__note{margin-top:16px;font-size:13px;line-height:1.5;color:rgba(232,234,240,.5)}

/* ── план площадки ────────────────────────────────────────────────────── */
.ip-plan{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(240px,1fr);gap:34px;
 margin-top:34px;align-items:center}
.ip-plan svg{width:100%;height:auto;display:block}
.ip-plan .hall{transition:opacity .2s}
.ip-plan .hall text{font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:13px;
 fill:#fff;letter-spacing:.04em}
.ip-plan .hall.other text{fill:#6C7180}
.ip-legend div{display:flex;gap:12px;align-items:flex-start;margin-bottom:16px;font-size:14.5px;
 line-height:1.45;color:var(--mute)}
.ip-legend i{flex:0 0 auto;width:16px;height:16px;margin-top:3px;border-radius:2px}
.ip-legend b{display:block;font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:15px;
 color:var(--ink);letter-spacing:.02em}

/* ── ритм монтажа ─────────────────────────────────────────────────────── */
.ip-rhythm{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(240px,1fr);gap:34px;
 margin-top:30px;align-items:center}
.ip-comb{display:flex;align-items:flex-end;gap:2px;height:120px;width:100%}
.ip-comb i{flex:1 1 auto;background:var(--blue);opacity:.85;min-width:1px}
.ip-comb i.off{background:#B9BDC8}
.ip-nums{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);
 border:1px solid var(--line)}
.ip-nums div{background:var(--paper);padding:16px 16px}
.ip-nums b{display:block;font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:26px;
 line-height:1.1;margin-bottom:3px}
.ip-nums span{font-size:13px;color:var(--mute);line-height:1.4}

/* ── итог ─────────────────────────────────────────────────────────────── */
.ip-res{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);
 border:1px solid var(--line);margin-top:34px}
.ip-res div{background:var(--paper);padding:22px 20px}
.ip-res b{display:block;font-family:'Jura',Arial,sans-serif;font-weight:700;font-size:16px;
 margin-bottom:6px}
.ip-res span{font-size:14px;line-height:1.5;color:var(--mute)}

/* ── адаптив ──────────────────────────────────────────────────────────── */
@media(max-width:1080px){
 /* труба рисуется только на широком экране, где ступени стоят в ряд;
    в перестроенной сетке её место занимает засечка слева */
 .ip-chain__flow{display:none}
 .ip-stages{grid-template-columns:1fr 1fr}
 .ip-stage{padding-top:8px;padding-left:20px;border-left:2px solid var(--line)}
 .ip-stage__n{position:relative}
 .ip-stage__n::before{content:"";position:absolute;left:-27px;top:4px;width:10px;height:10px;
  border-radius:50%;background:var(--blue)}
 .ip-mold,.ip-plan,.ip-rhythm{grid-template-columns:1fr}
 .ip-brief{grid-template-columns:1fr;gap:26px}
 .ip-route{grid-template-columns:1fr 1fr}
}
@media(max-width:760px){
 .ip section{padding:56px 18px}
 .ip-hero__in{padding:28px 18px 40px}
 .ip-facts{grid-template-columns:1fr 1fr}
 .ip-stages{grid-template-columns:1fr;gap:26px}
 .ip-stage{padding-top:8px;padding-left:20px}
 .ip-gran{grid-template-columns:1fr}
 .ip-route{grid-template-columns:1fr}
 .ip-res{grid-template-columns:1fr}
 .ip-titles{min-height:150px}
 .ip-comb{height:84px}
}
@media(max-width:520px){
 .ip-nums,.ip-mold__read{grid-template-columns:1fr}
}
/* телефон в ландшафте: секции ниже, чтобы экран не забивался одним блоком */
@media(max-height:520px) and (orientation:landscape){
 .ip section{padding:44px 22px}
 .ip-titles{min-height:120px}
}
@media(prefers-reduced-motion:reduce){
 .ip .rv{opacity:1;transform:none;transition:none}
 .ip-titles div{opacity:1;transform:none;transition:none}
 .ip-card,.ip-card__img img{transition:none}
}
</style>"""
CSS = CSS.replace('%BLUE%', PAL['interplastica']).replace('%RED%', PAL['upakovka'])


def pic(slug, sizes, cls='', extra=''):
    """<img> кадра в трёх размерах: браузер берёт нужный по ширине места."""
    a = WHAT.get(slug, '')
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="{IMG}/{slug}-s.jpg" '
            f'srcset="{IMG}/{slug}-s.jpg 480w, {IMG}/{slug}-m.jpg 800w, '
            f'{IMG}/{slug}.jpg 1100w" sizes="{sizes}" alt="{a}" '
            f'loading="lazy" decoding="async"{extra}>')


def mmss(sec):
    return '%d:%02d' % (int(sec) // 60, int(sec) % 60)


def hero():
    t = ''.join(f'<div data-i="{i}">{x}</div>' for i, x in enumerate(TITLES))
    facts = [
        (mmss(DURATION), 'Хронометраж обзорного ролика'),
        (str(N_SHOTS), f'Планов в монтаже, средний {str(MEAN).replace(chr(46), chr(44))} с'),
        (str(len(BRANDS)), 'Компаний читается на стендах в кадре'),
        ('3 + Форум', 'Павильоны Экспоцентра под интерпластику'),
    ]
    f = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in facts)
    bg = (f'<img src="{IMG}/hall-engel-m.jpg" '
          f'srcset="{IMG}/hall-engel-m.jpg 800w, {IMG}/hall-engel.jpg 1100w" '
          f'sizes="100vw" alt="{WHAT["hall-engel"]}" fetchpriority="high" decoding="async">')
    return (
      '<section class="ip-hero">'
      f'<div class="ip-hero__bg">{bg}</div>'
      '<div class="ip-hero__in">'
      '<a class="ip-back" href="/project">← Все проекты</a>'
      '<div class="lbl" style="color:#8E9BFF">Video · Messe Düsseldorf</div>'
      f'<div class="ip-titles" id="ip-titles">{t}</div>'
      '<h1>Обзорный ролик выставки полимеров: две минуты, которые должны '
      'заменить прогулку по четырём павильонам</h1>'
      '<p class="lead">Messe Düsseldorf заказал фильм не про стенд и не про '
      'продукт, а про саму выставку. Такой ролик работает весь год: его '
      'показывают будущим экспонентам и посетителям вместо описания.</p>'
      f'<div class="ip-facts">{f}</div>'
      '</div></section>')


def brief():
    return (
      '<section><div class="in ip-brief">'
      '<div class="col"><div class="lbl">Компания</div>'
      '<h3>Messe Düsseldorf</h3>'
      '<p>Организатор примерно 80 выставок по всему миру, они закрывают '
      'практически все отрасли экономики. В России компания работает '
      'с 1963 года: тогда она привезла официальную делегацию Германии '
      'на международную выставку «Химия» по приглашению Торгово-промышленной '
      'палаты СССР.</p>'
      '<p>интерпластика, её московский смотр полимеров и оборудования '
      'для их переработки, идёт в ЦВК «Экспоцентр» в одни дни '
      'с выставкой упаковки upakovka.</p></div>'
      '<div class="col"><div class="lbl">Задача</div>'
      '<h3>Показать выставку целиком</h3>'
      '<p>Снять обзорный ролик про интерпластику: не репортаж с одного '
      'стенда, а картину всей площадки, от стойки регистрации до докладов '
      'деловой программы.</p>'
      '<p>Сложность обзорного жанра в том, что событие живёт четыре дня '
      'и разложено по четырём павильонам, а ролик должен уложиться '
      'в две минуты и не превратиться в перечисление логотипов.</p></div>'
      '<div class="col"><div class="lbl">Решение</div>'
      '<h3>Пройти отрасль по цепочке</h3>'
      '<p>Съёмка шла по логике производства: сырьё в гранулах, компаунды '
      'и добавки, машины, готовые изделия. Так зритель видит не набор '
      'стендов, а полную технологическую цепочку, которая помещается '
      'в одном комплексе.</p>'
      f'<p>Смонтировано в темп музыки: {N_SHOTS} планов, средний {str(MEAN).replace(".", ",")} секунды, '
      'к финалу шаг склеек уполовинивается дважды.</p></div>'
      '</div></section>')


def player():
    route = ''.join(
        f'<button type="button" data-seek="{s}"><i>{mmss(s)}</i><b>{t}</b>'
        f'<span>{d}</span></button>' for s, t, d, _im in ROUTE)
    return (
      '<section class="ip-player night" id="film"><div class="in">'
      '<div class="lbl">Ролик</div>'
      '<h2>Обзор выставки</h2>'
      '<p class="lead">Ниже по странице любая карточка перематывает плеер '
      'на свою секунду: и стенды, и маршрут обзора.</p>'
      f'<video class="ip-video" id="ip-video" controls preload="metadata" '
      f'playsinline poster="{IMG}/hall-engel-m.jpg">'
      f'<source src="{VIDEO}" type="video/mp4">'
      'Ваш браузер не умеет играть видео. '
      f'<a href="{VIDEO}">Скачать ролик</a>.</video>'
      f'<div class="ip-route">{route}</div>'
      '</div></section>')


def chain():
    stages = ''
    for n, st in enumerate(MAP['chain'], 1):
        cards = ''
        for it in st['items']:
            img = pic(it['still'], '(max-width:760px) 92vw, (max-width:1080px) 44vw, 22vw')
            cards += (
                f'<button class="ip-card" type="button" data-seek="{it["sec"]}">'
                f'<span class="ip-card__img">{img}'
                f'<span class="ip-card__t">{mmss(it["sec"])}</span></span>'
                f'<span class="ip-card__b"><b>{it["name"]}</b>'
                f'<span>{it["note"]}</span></span></button>')
        stages += (
            f'<div class="ip-stage" data-stage="{st["id"]}">'
            f'<span class="ip-stage__port" data-port="{st["id"]}"></span>'
            f'<span class="ip-stage__n">Ступень {n}</span>'
            f'<h3>{st["title"]}</h3>'
            f'<p class="ip-stage__lead">{st["lead"]}</p>{cards}</div>')
    return (
      '<section><div class="in">'
      '<div class="lbl">Что попало в кадр</div>'
      '<h2>Вся цепочка передела в одном комплексе</h2>'
      '<p class="lead">Мы разобрали ролик по стоп-кадрам и разложили компании, '
      f'чьи стенды в нём читаются, по ступеням производства. Их {len(BRANDS)}: '
      'сырьевые заводы, поставщики компаундов, машиностроители и те, кто '
      'показывает готовые изделия. Клик по карточке перематывает ролик '
      'на её секунду.</p>'
      f'<div class="ip-chain"><canvas class="ip-chain__flow" id="ip-flow" aria-hidden="true">'
      f'</canvas><div class="ip-stages">{stages}</div></div>'
      '<p class="ip-chain__note">В эти же дни Экспоцентр работает и на '
      'выставку упаковки upakovka / UPAK ITALIA, поэтому в обзор попадают '
      'и упаковочные линии: на плане площадки её павильон отмечен красным.</p>'
      '</div></section>')


def granules():
    g = ''
    for it in MAP['granules']:
        img = pic(it['still'], '(max-width:760px) 92vw, 46vw')
        g += (f'<figure>{img}<figcaption><b>{it["name"]}</b>'
              f'<em>{it["grade"]}</em><span>{it["note"]}</span></figcaption></figure>')
    line = ['ПНД', 'ПВД', 'Поликарбонаты', 'Бисфенол-А', 'Сэвилен', 'ПЭ трубы',
            'Фенол', 'Ацетон', 'Этаноламины']
    chips = ''.join(f'<i>{x}</i>' for x in line)
    return (
      '<section class="night"><div class="in">'
      '<div class="lbl">Витрина сырья</div>'
      '<h2>С чего начинается любое изделие в зале</h2>'
      '<p class="lead">На стенде «Казаньоргсинтеза» гранулы стоят в прозрачных '
      'кубах, у каждого своя табличка с маркой. Камера подходит к ним '
      'вплотную, и марки читаются прямо с кадра.</p>'
      f'<div class="ip-gran">{g}</div>'
      '<p class="cap" style="margin-top:26px">Продуктовая линейка с той же '
      'стены стенда:</p>'
      f'<div class="ip-kos">{chips}</div>'
      '</div></section>')


def mold():
    btns = ''.join(
        f'<button type="button" data-part="{pid}" '
        f'aria-pressed="{"true" if i == 0 else "false"}">{name}</button>'
        for i, (pid, name, _d, _s) in enumerate(PARTS))
    return (
      '<section class="night"><div class="in">'
      '<div class="lbl">Механика · литник</div>'
      '<h2>Что делают все машины из ролика</h2>'
      '<p class="lead">Термопласт-автомат впрыскивает расплав в форму через '
      'литник, и дальше материал сам растекается по полости. Куда поставить '
      'литник, это главный вопрос конструктора: от него зависит, за сколько '
      'форма заполнится и где встретятся встречные фронты. Поставьте литник '
      'кликом по детали.</p>'
      '<div class="ip-mold">'
      '<div class="ip-mold__stage">'
      '<canvas class="ip-mold__cv" id="ip-mold" width="680" height="420" '
      'role="img" aria-label="Поле заполнения пресс-формы расплавом"></canvas>'
      '<span class="ip-mold__hint">клик по детали ставит литник</span>'
      '</div>'
      '<div class="ip-mold__side">'
      f'<h4>Деталь</h4><div class="ip-parts">{btns}</div>'
      '<p class="ip-mold__desc" id="ip-mold-desc"></p>'
      '<div class="ip-mold__read">'
      '<div><b id="ip-mold-time">·</b><span>условных единиц пути '
      'до дальней точки</span></div>'
      '<div><b id="ip-mold-weld">·</b><span>линий спая на детали</span></div>'
      '</div>'
      '<div class="ip-mold__legend">'
      '<span><i style="background:linear-gradient(90deg,#8E9BFF,#F2A104)"></i>'
      'изохроны: чем светлее, тем позже пришёл расплав</span>'
      '<span><i style="background:%RED%"></i>линии спая: фронты сошлись '
      'после обхода отверстия</span>'
      '<span><i style="background:#fff"></i>литник и последняя точка '
      'заполнения</span></div>'
      '<div class="ip-mold__row">'
      '<button class="ip-mold__btn" type="button" id="ip-mold-reset">Сбросить</button>'
      '<button class="ip-mold__btn" type="button" id="ip-mold-two">Два литника</button>'
      '<button class="ip-mold__btn" type="button" id="ip-mold-play">Повторить залив</button>'
      '</div>'
      '<p class="ip-mold__note">Поле считается честно: время течения это '
      'геодезическое расстояние от литника по полости детали (алгоритм '
      'Дейкстры по сетке), линии спая ищутся как гребни этого поля. '
      'Реология расплава, толщина стенки и подстуживание здесь не '
      'моделируются: это наглядная схема, а не расчёт для производства.</p>'
      '</div></div></div></section>').replace('%RED%', PAL['upakovka'])


def iso(u, v, dz=0):
    return (ISO['ox'] + (u - v) * ISO['kx'],
            ISO['oy'] + (u + v) * ISO['ky'] - dz)


def plan():
    """Схема площадки: павильоны заданы в плановых координатах и подняты
    в изометрию, поэтому взаимное расположение совпадает с указателем."""
    fills = {'inter': (PAL['interplastica'], '#252587', '#4A4AC0'),
             'upakovka': (PAL['upakovka'], '#9C0015', '#E4213C'),
             'other': ('#D7DAE2', '#B4B8C4', '#E7E9EF')}
    halls = ''
    # рисуем от дальних к ближним: у изометрии порядок наложения важен
    for hid, label, role, u, v, du, dv in sorted(HALLS, key=lambda h: h[3] + h[4]):
        top, side, front = fills[role]
        c = [iso(u, v, ISO['lift']), iso(u + du, v, ISO['lift']),
             iso(u + du, v + dv, ISO['lift']), iso(u, v + dv, ISO['lift'])]
        g = [iso(u, v), iso(u + du, v), iso(u + du, v + dv), iso(u, v + dv)]
        roof = ' '.join(f'{x:.0f},{y:.0f}' for x, y in c)
        # боковые грани: правая (вдоль v) и передняя (вдоль u)
        s1 = (f'{c[1][0]:.0f},{c[1][1]:.0f} {c[2][0]:.0f},{c[2][1]:.0f} '
              f'{g[2][0]:.0f},{g[2][1]:.0f} {g[1][0]:.0f},{g[1][1]:.0f}')
        s2 = (f'{c[2][0]:.0f},{c[2][1]:.0f} {c[3][0]:.0f},{c[3][1]:.0f} '
              f'{g[3][0]:.0f},{g[3][1]:.0f} {g[2][0]:.0f},{g[2][1]:.0f}')
        cx = sum(x for x, _ in c) / 4
        cy = sum(y for _, y in c) / 4 + 4
        halls += (f'<g class="hall {role}" data-hall="{hid}">'
                  f'<polygon points="{s1}" fill="{side}"></polygon>'
                  f'<polygon points="{s2}" fill="{front}"></polygon>'
                  f'<polygon points="{roof}" fill="{top}" '
                  f'stroke="rgba(255,255,255,.4)" stroke-width="1"></polygon>'
                  f'<text x="{cx:.0f}" y="{cy:.0f}" text-anchor="middle">{label}</text></g>')

    def pt(u, v):
        x, y = iso(u, v)
        return f'{x:.0f},{y:.0f}'

    road = f'M {pt(0, 14)} L {pt(210, 14)} L {pt(330, 60)}'
    quay = f'M {pt(300, 100)} L {pt(330, 190)} L {pt(120, 210)}'
    legend = [
        (PAL['interplastica'], 'интерпластика',
         'Павильоны 1, 3, 8 и Форум. Там же секция raw&nbsp;materials '
         'и meeting point первого павильона.'),
        (PAL['upakovka'], 'upakovka / UPAK ITALIA',
         'Павильон 2, в зале 2.3 идёт Future Forum. Обе выставки работают '
         'в одни дни, по площадке ходит один и тот же поток.'),
        ('#D7DAE2', 'Остальные павильоны',
         'В эти дни заняты другими смотрами Экспоцентра.'),
    ]
    lg = ''.join(f'<div><i style="background:{c}"></i><span><b>{t}</b>{d}</span></div>'
                 for c, t, d in legend)
    return (
      '<section><div class="in">'
      '<div class="lbl">Площадка</div>'
      '<h2>Три павильона и Форум</h2>'
      '<p class="lead">Финальный кадр ролика это указатель у входа. Мы '
      'перерисовали его схему вектором: синим то, что занимает интерпластика, '
      'красным соседняя upakovka.</p>'
      '<div class="ip-plan">'
      '<div><svg viewBox="0 0 780 430" role="img" '
      'aria-label="Схема ЦВК Экспоцентр: павильоны интерпластики и upakovka">'
      '<defs><pattern id="ipgrid" width="26" height="26" patternUnits="userSpaceOnUse">'
      '<path d="M26 0H0V26" fill="none" stroke="rgba(18,20,27,.06)" stroke-width="1"/>'
      '</pattern></defs>'
      '<rect width="780" height="430" fill="url(#ipgrid)"></rect>'
      f'<path d="{road}" fill="none" stroke="rgba(18,20,27,.10)" stroke-width="16" '
      'stroke-linecap="round"></path>'
      f'<path d="{quay}" fill="none" stroke="rgba(53,53,157,.10)" stroke-width="20" '
      'stroke-linecap="round"></path>'
      f'{halls}'
      '<g font-family="Jura" font-size="12.5" font-weight="700" fill="#5C616E" '
      'letter-spacing="1">'
      f'<text x="{iso(30, -18)[0]:.0f}" y="{iso(30, -18)[1]:.0f}" text-anchor="middle">Северный вход</text>'
      f'<text x="{iso(86, 224)[0]:.0f}" y="{iso(86, 224)[1]:.0f}" text-anchor="middle">Западный вход</text>'
      f'<text x="{iso(86, 224)[0]:.0f}" y="{iso(86, 224)[1] + 17:.0f}" text-anchor="middle" '
      'font-weight="400">м. «Выставочная»</text>'
      f'<text x="{iso(300, 176)[0]:.0f}" y="{iso(300, 176)[1]:.0f}" text-anchor="middle">Южный вход</text>'
      '</g></svg>'
      '<p class="cap">Схема перерисована с указателя в кадре ролика: '
      'взаимное расположение павильонов сохранено, точная геометрия '
      'застройки не воспроизводится.</p></div>'
      f'<div class="ip-legend">{lg}</div>'
      '</div></div></section>')


def rhythm():
    bars = ''
    mx = max(LENS)
    for i, l in enumerate(LENS):
        h = max(4, round(l / mx * 100))
        on = abs(l / BEAT - round(l / BEAT)) < 0.15
        bars += (f'<i class="{"" if on else "off"}" style="height:{h}%" '
                 f'title="план {i + 1}: {str(l).replace(".", ",")} с"></i>')
    nums = [
        (str(N_SHOTS), 'планов после титров'),
        (str(MEAN).replace('.', ','), 'секунды средний план'),
        (str(BPM).replace('.', ','), 'удара в минуту в музыке'),
        (f'{ON_GRID} из {N_SHOTS}', 'планов лежат на доле такта'),
    ]
    n = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in nums)
    return (
      '<section style="background:var(--sheet)"><div class="in">'
      '<div class="lbl">Монтаж</div>'
      '<h2>Обзор держится на ритме</h2>'
      '<p class="lead">Обзорный ролик легко превращается в перечисление: '
      'кадр, кадр, кадр. Чтобы этого не было, монтаж посажен на музыку. '
      'Мы измерили результат по готовому файлу: длины планов ложатся '
      f'на сетку доли в {str(BEAT).replace(".", ",")} секунды, а к финалу шаг '
      'уполовинивается дважды и обзор ускоряется.</p>'
      '<div class="ip-rhythm">'
      f'<div><div class="ip-comb">{bars}</div>'
      '<p class="cap">Каждый штрих это план ролика, высота равна его длине. '
      'Серым отмечены планы, выпавшие из сетки доли.</p></div>'
      f'<div class="ip-nums">{n}</div>'
      '</div></div></section>')


def result():
    items = [
        ('Ролик на два адресата', 'Экспонентам он показывает поток '
         'посетителей и уровень соседей по залу, посетителям то, что выставку '
         'стоит закладывать в календарь.'),
        ('Живёт между выставками', 'Обзор снят так, что не привязан '
         'к конкретной новости: его можно показывать весь год до следующей '
         'сессии.'),
        ('Работает без звука', 'Смонтирован под музыку, но читается '
         'и в беззвучном автоплее на стойке или в ленте: сюжет держится '
         'на порядке кадров.'),
    ]
    r = ''.join(f'<div><b>{t}</b><span>{d}</span></div>' for t, d in items)
    return (
      '<section><div class="in">'
      '<div class="lbl">Результат</div>'
      '<h2>Что получил заказчик</h2>'
      f'<div class="ip-res">{r}</div>'
      '</div></section>')


PAGE_JS = """<script>(function(){
var root=document.querySelector('.ip');if(!root)return;
var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;

/* ── титры: набираются по очереди, как в ролике ─────────────────────── */
(function(){
  var box=document.getElementById('ip-titles');if(!box)return;
  var el=[].slice.call(box.children);
  if(RM){el.forEach(function(d){d.classList.add('on')});return;}
  el.forEach(function(d,i){setTimeout(function(){d.classList.add('on')},260+i*430)});
})();

/* ── reveal ─────────────────────────────────────────────────────────── */
(function(){
  var els=[].slice.call(root.querySelectorAll('.rv'));
  if(!('IntersectionObserver' in window)||RM){els.forEach(function(e){e.classList.add('on')});return;}
  var io=new IntersectionObserver(function(en){en.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);}})},{threshold:.12});
  els.forEach(function(e){io.observe(e)});
})();

/* ── перемотка плеера из любой карточки ─────────────────────────────── */
(function(){
  var v=document.getElementById('ip-video');if(!v)return;
  root.addEventListener('click',function(e){
    var b=e.target.closest('[data-seek]');if(!b)return;
    var t=parseFloat(b.getAttribute('data-seek'));if(isNaN(t))return;
    var top=v.getBoundingClientRect().top+window.pageYOffset-70;
    window.scrollTo({top:top,behavior:RM?'auto':'smooth'});
    var go=function(){try{v.currentTime=t;}catch(err){}
      var p=v.play();if(p&&p.catch)p.catch(function(){});};
    if(v.readyState>=1)go();else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}
  });
})();

/* ── поток гранул по цепочке передела ───────────────────────────────── */
(function(){
  var cv=document.getElementById('ip-flow');if(!cv)return;
  var wrap=cv.parentNode,ctx=cv.getContext('2d');
  var ports=[].slice.call(wrap.querySelectorAll('[data-port]'));
  var W=0,H=0,dpr=1,path=null,parts=[],raf=0,hot=-1,live=false;

  function layout(){
    var r=wrap.getBoundingClientRect();
    W=Math.max(1,Math.round(r.width));H=Math.max(1,Math.round(r.height));
    live=getComputedStyle(cv).display!=='none';
    dpr=Math.min(2,window.devicePixelRatio||1);
    cv.width=W*dpr;cv.height=H*dpr;cv.style.height=H+'px';
    ctx.setTransform(dpr,0,0,dpr,0,0);
    var pts=ports.map(function(p){
      var b=p.getBoundingClientRect();
      return {x:b.left-r.left,y:b.top-r.top};});
    var y=Math.max(16,pts.reduce(function(m,p){return Math.min(m,p.y);},1e9)-44);
    path={main:{y:y,x0:4,x1:W-4},taps:pts.map(function(p){
      return {x:p.x+16,y:y,len:34};})};
  }

  function spawn(u){
    parts.push({u:(u===undefined?-6:u),v:1.7+Math.random()*1.9,tap:-1,
      g:Math.random()*4|0,off:(Math.random()-.5)*7,drop:0});
  }
  function prefill(){
    parts.length=0;
    for(var i=0;i<130;i++)spawn(Math.random()*W);
  }

  function step(){
    var i,p;
    if(parts.length<150)for(var q=0;q<2;q++)spawn();
    for(i=parts.length-1;i>=0;i--){
      p=parts[i];
      if(p.tap<0){
        var prev=p.u;p.u+=p.v;
        // на подходе к отводу часть гранул сваливается в ступень
        for(var k=0;k<path.taps.length;k++){
          var t=path.taps[k];
          if(prev>=t.x||p.u<t.x)continue;
          var pr=(hot===k)?.55:.26;
          if(Math.random()<pr){p.tap=k;p.drop=0;p.u=t.x;}
        }
        if(p.u>W+10)parts.splice(i,1);
      }else{
        p.drop+=p.v*.8;
        if(p.drop>path.taps[p.tap].len+8)parts.splice(i,1);
      }
    }
  }

  var COL=['#35359D','#5A5AC8','#8E9BFF','#F2A104'];
  function draw(){
    ctx.clearRect(0,0,W,H);
    if(!path||!live)return;
    var m=path.main;
    ctx.strokeStyle='rgba(18,20,27,.12)';ctx.lineWidth=8;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(m.x0,m.y);ctx.lineTo(m.x1,m.y);ctx.stroke();
    path.taps.forEach(function(t,k){
      ctx.strokeStyle=(hot===k)?'rgba(53,53,157,.45)':'rgba(18,20,27,.12)';
      ctx.lineWidth=7;ctx.beginPath();
      ctx.moveTo(t.x,t.y);ctx.lineTo(t.x,t.y+t.len);ctx.stroke();
      ctx.fillStyle=(hot===k)?'#35359D':'rgba(18,20,27,.2)';
      ctx.beginPath();ctx.arc(t.x,t.y,5.5,0,6.284);ctx.fill();
    });
    parts.forEach(function(p){
      var x,y,t;
      if(p.tap<0){x=p.u;y=m.y+p.off*.45;}
      else{t=path.taps[p.tap];x=t.x+p.off*.5;y=t.y+p.drop;}
      ctx.fillStyle=COL[p.g];ctx.globalAlpha=.88;
      ctx.beginPath();ctx.arc(x,y,2.2,0,6.284);ctx.fill();
    });
    ctx.globalAlpha=1;
  }

  function loop(){step();draw();raf=requestAnimationFrame(loop);}
  function start(){if(!raf&&!RM&&live)raf=requestAnimationFrame(loop);}
  function stop(){if(raf){cancelAnimationFrame(raf);raf=0;}}

  var stages=[].slice.call(wrap.querySelectorAll('.ip-stage'));
  stages.forEach(function(s,i){
    s.addEventListener('mouseenter',function(){hot=i;});
    s.addEventListener('mouseleave',function(){hot=-1;});
    s.addEventListener('focusin',function(){hot=i;});
  });

  layout();prefill();draw();
  var ro=window.ResizeObserver?new ResizeObserver(function(){layout();draw();}):null;
  if(ro)ro.observe(wrap);else window.addEventListener('resize',function(){layout();draw();});
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(en){
      en.forEach(function(e){e.isIntersecting?start():stop();});
    },{threshold:.05}).observe(wrap);
  }else start();
  document.addEventListener('visibilitychange',function(){
    document.hidden?stop():start();});
})();

/* ── симулятор заполнения формы ─────────────────────────────────────── */
(function(){
  var cv=document.getElementById('ip-mold');if(!cv)return;
  var ctx=cv.getContext('2d');
  var PARTS=%PARTS%;
  var GW=340,GH=210,CELL=2;          // сетка расчёта; canvas 680×420
  var mask=null,dist=null,weld=null,weldLines=0,seeds=[],maxD=0,part=PARTS[0].id;
  var buf=document.createElement('canvas');buf.width=GW;buf.height=GH;
  var bctx=buf.getContext('2d');
  var anim=0,t0=0,dur=1500;

  /* контуры деталей рисуются кодом: маска снимается с альфы */
  function buildMask(id){
    var c=document.createElement('canvas');c.width=GW;c.height=GH;
    var g=c.getContext('2d');
    g.fillStyle='#fff';
    if(id==='crate'){
      rr(g,24,30,292,150,16);g.fill();
      g.globalCompositeOperation='destination-out';
      for(var r=0;r<3;r++)for(var k=0;k<6;k++){
        rr(g,54+k*42,56+r*42,26,26,4);g.fill();}
      g.globalCompositeOperation='source-over';
    }else if(id==='shell'){
      rr(g,112,10,116,190,22);g.fill();
      g.globalCompositeOperation='destination-out';
      g.beginPath();g.arc(170,42,12,0,6.284);g.fill();     /* камера */
      rr(g,148,72,44,7,3);g.fill();                        /* щель динамика */
      rr(g,138,96,54,36,6);g.fill();                       /* окно платы */
      g.beginPath();g.arc(132,166,8,0,6.284);g.fill();     /* бобышки */
      g.beginPath();g.arc(208,166,8,0,6.284);g.fill();
      g.globalCompositeOperation='source-over';
    }else{
      var cx=170,cy=105,R=88,teeth=18;
      g.beginPath();
      for(var i=0;i<teeth*2;i++){
        var a=i/(teeth*2)*6.28318,rad=(i%2?R:R-12);
        var x=cx+Math.cos(a)*rad,y=cy+Math.sin(a)*rad*.86;
        i?g.lineTo(x,y):g.moveTo(x,y);}
      g.closePath();g.fill();
      g.globalCompositeOperation='destination-out';
      for(var s2=0;s2<5;s2++){
        var a0=s2/5*6.28318+.30;
        g.beginPath();
        for(var q=0;q<=16;q++){
          var aa=a0+q/16*(6.28318/5-.60),ro=R-24;
          g.lineTo(cx+Math.cos(aa)*ro,cy+Math.sin(aa)*ro*.86);}
        for(var q2=16;q2>=0;q2--){
          var ab=a0+q2/16*(6.28318/5-.60),ri=32;
          g.lineTo(cx+Math.cos(ab)*ri,cy+Math.sin(ab)*ri*.86);}
        g.closePath();g.fill();}
      g.beginPath();g.arc(cx,cy,17,0,6.284);g.fill();      /* посадочное */
      g.globalCompositeOperation='source-over';
    }
    var d=g.getImageData(0,0,GW,GH).data,m=new Uint8Array(GW*GH);
    for(var p=0;p<GW*GH;p++)m[p]=d[p*4+3]>128?1:0;
    return m;
  }
  /* центр самой толстой части детали: туда и ставим литник по умолчанию */
  function thickest(m){
    var n=GW*GH,df=new Float32Array(n);
    for(var i=0;i<n;i++)df[i]=m[i]?1e6:0;
    var x,y,idx;
    for(y=0;y<GH;y++)for(x=0;x<GW;x++){
      idx=y*GW+x;if(!m[idx]){df[idx]=0;continue;}
      var v=df[idx];
      if(x>0)v=Math.min(v,df[idx-1]+1);
      if(y>0)v=Math.min(v,df[idx-GW]+1);
      if(x>0&&y>0)v=Math.min(v,df[idx-GW-1]+1.4142);
      if(x<GW-1&&y>0)v=Math.min(v,df[idx-GW+1]+1.4142);
      df[idx]=v;}
    for(y=GH-1;y>=0;y--)for(x=GW-1;x>=0;x--){
      idx=y*GW+x;if(!m[idx])continue;
      var w=df[idx];
      if(x<GW-1)w=Math.min(w,df[idx+1]+1);
      if(y<GH-1)w=Math.min(w,df[idx+GW]+1);
      if(x<GW-1&&y<GH-1)w=Math.min(w,df[idx+GW+1]+1.4142);
      if(x>0&&y<GH-1)w=Math.min(w,df[idx+GW-1]+1.4142);
      df[idx]=w;}
    /* литник ставим в середину детали, но не впритык к стенке: берём
       ближайшую к центру клетку, где до края остаётся хотя бы три шага */
    var bi=0,bd=1e18,cx0=GW/2,cy0=GH/2,any=false;
    for(var j=0;j<n;j++){
      if(!m[j]||df[j]<3.5)continue;
      var jx=j%GW,jy=(j-j%GW)/GW,dc=(jx-cx0)*(jx-cx0)+(jy-cy0)*(jy-cy0);
      if(dc<bd){bd=dc;bi=j;any=true;}
    }
    if(!any)for(var j2=0;j2<n;j2++)if(m[j2]){bi=j2;break;}
    return {x:bi%GW,y:(bi-bi%GW)/GW};
  }
  function rr(g,x,y,w,h,r){
    g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);
    g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();
  }

  /* время течения = геодезическое расстояние от литника (Дейкстра) */
  function solve(){
    var n=GW*GH,INF=1e9;
    /* Float64, а не Float32: у 32-битной точности шаг округления на этих
       значениях крупнее эпсилона сравнения, и релаксация зацикливалась */
    dist=new Float64Array(n);for(var i=0;i<n;i++)dist[i]=INF;
    if(!seeds.length){maxD=0;weld=new Uint8Array(n);weldLines=0;return;}
    var heap=[],hd=[];
    function push(idx,d){heap.push(idx);hd.push(d);var c=heap.length-1;
      while(c>0){var p=(c-1)>>1;if(hd[p]<=hd[c])break;
        var a=heap[p];heap[p]=heap[c];heap[c]=a;var b=hd[p];hd[p]=hd[c];hd[c]=b;c=p;}}
    function pop(){var top=heap[0],td=hd[0],last=heap.pop(),ld=hd.pop();
      if(heap.length){heap[0]=last;hd[0]=ld;var c=0;
        for(;;){var l=c*2+1,r=l+1,s=c;
          if(l<hd.length&&hd[l]<hd[s])s=l;
          if(r<hd.length&&hd[r]<hd[s])s=r;
          if(s===c)break;
          var a=heap[s];heap[s]=heap[c];heap[c]=a;var b=hd[s];hd[s]=hd[c];hd[c]=b;c=s;}}
      return [top,td];}
    seeds.forEach(function(s){var idx=s.y*GW+s.x;if(mask[idx]){dist[idx]=0;push(idx,0);}});
    var DX=[1,-1,0,0,1,1,-1,-1],DY=[0,0,1,-1,1,-1,1,-1];
    var WT=[1,1,1,1,1.4142,1.4142,1.4142,1.4142];
    while(heap.length){
      var q=pop(),idx=q[0],d=q[1];
      if(d>dist[idx]+1e-9)continue;
      var x=idx%GW,y=(idx-x)/GW;
      for(var k=0;k<8;k++){
        var nx=x+DX[k],ny=y+DY[k];
        if(nx<0||ny<0||nx>=GW||ny>=GH)continue;
        var ni=ny*GW+nx;if(!mask[ni])continue;
        var nd=d+WT[k];
        if(nd<dist[ni]-1e-9){dist[ni]=nd;push(ni,nd);}
      }
    }
    maxD=0;for(var j=0;j<n;j++)if(mask[j]&&dist[j]<INF&&dist[j]>maxD)maxD=dist[j];
    /* линии спая: гребень поля времени, точка позже обоих соседей по оси.
       Порог 0.55 отсекает шум сетки: у ровного течения перепад по оси
       равен двойному шагу, у гребня он падает почти до нуля с обеих сторон. */
    weld=new Uint8Array(n);
    var PX=[1,0,1,1],PY=[0,1,1,-1];
    for(var yy=1;yy<GH-1;yy++)for(var xx=1;xx<GW-1;xx++){
      var id2=yy*GW+xx;if(!mask[id2]||dist[id2]>=INF)continue;
      var inner=true;
      for(var a=-1;a<=1&&inner;a++)for(var b=-1;b<=1;b++)
        if(!mask[(yy+b)*GW+xx+a]){inner=false;break;}
      if(!inner)continue;
      for(var p2=0;p2<4;p2++){
        var i1=(yy+PY[p2])*GW+xx+PX[p2],i2=(yy-PY[p2])*GW+xx-PX[p2];
        if(dist[i1]>=INF||dist[i2]>=INF)continue;
        var s1=dist[id2]-dist[i1],s2=dist[id2]-dist[i2];
        if(s1>0.55&&s2>0.55){weld[id2]=1;break;}
      }
    }
    /* мелочь чистим, а заодно считаем сами линии: связные куски гребня */
    weldLines=0;
    var seen=new Uint8Array(n),stack=[];
    for(var w0=0;w0<n;w0++){
      if(!weld[w0]||seen[w0])continue;
      stack.length=0;stack.push(w0);seen[w0]=1;
      var cells=[w0];
      while(stack.length){
        var c0=stack.pop(),cx0=c0%GW,cy0=(c0-cx0)/GW;
        for(var dy0=-1;dy0<=1;dy0++)for(var dx0=-1;dx0<=1;dx0++){
          var nx0=cx0+dx0,ny0=cy0+dy0;
          if(nx0<0||ny0<0||nx0>=GW||ny0>=GH)continue;
          var ni0=ny0*GW+nx0;
          if(weld[ni0]&&!seen[ni0]){seen[ni0]=1;stack.push(ni0);cells.push(ni0);}
        }
      }
      if(cells.length<4){for(var q0=0;q0<cells.length;q0++)weld[cells[q0]]=0;}
      else weldLines++;
    }
  }

  function lastPoint(){
    var best=-1,bi=-1;
    for(var i=0;i<GW*GH;i++)if(mask[i]&&dist[i]<1e9&&dist[i]>best){best=dist[i];bi=i;}
    return bi;
  }

  /* заливка цветом по времени прихода */
  function paint(front){
    var im=bctx.createImageData(GW,GH),d=im.data;
    for(var i=0;i<GW*GH;i++){
      var o=i*4;
      if(!mask[i]){d[o]=13;d[o+1]=15;d[o+2]=21;d[o+3]=255;continue;}
      if(!seeds.length||dist[i]>front){d[o]=30;d[o+1]=34;d[o+2]=46;d[o+3]=255;continue;}
      var u=maxD?dist[i]/maxD:0;
      /* индиго → сиреневый → янтарь, полосами изохрон */
      var r,g,b;
      if(u<.5){var v=u/.5;r=53+(142-53)*v;g=53+(155-53)*v;b=157+(255-157)*v;}
      else{var v2=(u-.5)/.5;r=142+(242-142)*v2;g=155+(161-155)*v2;b=255+(4-255)*v2;}
      var step=maxD/9,band=(dist[i]%step)<0.85?.62:1;
      d[o]=r*band;d[o+1]=g*band;d[o+2]=b*band;d[o+3]=255;
      if(front-dist[i]<1.4){d[o]=255;d[o+1]=255;d[o+2]=255;}
    }
    if(showWeld&&weld)for(var w=0;w<GW*GH;w++)
      if(weld[w]&&dist[w]<=front){var o2=w*4;d[o2]=209;d[o2+1]=0;d[o2+2]=28;d[o2+3]=255;}
    bctx.putImageData(im,0,0);
    ctx.imageSmoothingEnabled=true;
    ctx.clearRect(0,0,cv.width,cv.height);
    ctx.drawImage(buf,0,0,GW,GH,0,0,cv.width,cv.height);
    /* литники и последняя точка */
    ctx.imageSmoothingEnabled=true;
    seeds.forEach(function(s){
      ctx.beginPath();ctx.arc((s.x+.5)*CELL,(s.y+.5)*CELL,7,0,6.284);
      ctx.fillStyle='#fff';ctx.fill();
      ctx.beginPath();ctx.arc((s.x+.5)*CELL,(s.y+.5)*CELL,3,0,6.284);
      ctx.fillStyle='#0F1117';ctx.fill();});
    if(seeds.length&&front>=maxD){
      var bi=lastPoint();
      if(bi>=0){var lx=bi%GW,ly=(bi-lx)/GW;
        ctx.strokeStyle='#fff';ctx.lineWidth=1.5;
        ctx.beginPath();ctx.arc((lx+.5)*CELL,(ly+.5)*CELL,9,0,6.284);ctx.stroke();}
    }
  }

  var showWeld=true;
  function readout(){
    document.getElementById('ip-mold-time').textContent=
      seeds.length?Math.round(maxD):'·';
    document.getElementById('ip-mold-weld').textContent=seeds.length?weldLines:'·';
  }
  function play(){
    if(anim)cancelAnimationFrame(anim);
    if(!seeds.length){paint(-1);readout();return;}
    t0=performance.now();
    if(RM){paint(maxD);readout();return;}
    (function frame(now){
      var k=Math.min(1,(now-t0)/dur);
      paint(maxD*k);
      if(k<1)anim=requestAnimationFrame(frame);else{anim=0;readout();}
    })(t0);
  }
  function setPart(id){
    part=id;mask=buildMask(id);seeds=[];
    [].slice.call(document.querySelectorAll('[data-part]')).forEach(function(b){
      b.setAttribute('aria-pressed',b.getAttribute('data-part')===id?'true':'false');});
    var p=PARTS.filter(function(x){return x.id===id;})[0];
    var d=document.getElementById('ip-mold-desc');
    d.innerHTML=p.note+' <button class="ip-mold__btn" type="button" '+
      'style="padding:4px 9px;font-size:11px;margin-left:2px" data-seek="'+p.sec+
      '">кадр в ролике</button>';
    var c0=thickest(mask);
    seeds=[{x:c0.x,y:c0.y}];solve();play();
  }
  function addSeed(ev){
    var r=cv.getBoundingClientRect();
    var px=(ev.clientX-r.left)/r.width*GW,py=(ev.clientY-r.top)/r.height*GH;
    var x=Math.max(0,Math.min(GW-1,Math.round(px))),
        y=Math.max(0,Math.min(GH-1,Math.round(py)));
    if(!mask[y*GW+x])return;                       /* мимо детали */
    if(seeds.length>=3)seeds=[];
    seeds.push({x:x,y:y});solve();play();
  }
  cv.addEventListener('click',addSeed);
  document.querySelectorAll('[data-part]').forEach(function(b){
    b.addEventListener('click',function(){setPart(b.getAttribute('data-part'));});});
  document.getElementById('ip-mold-reset').addEventListener('click',function(){
    setPart(part);});
  document.getElementById('ip-mold-two').addEventListener('click',function(){
    /* по одному литнику на половину детали: классическая схема двух впусков */
    var s2=[];
    [[0,GW>>1],[GW>>1,GW]].forEach(function(rg){
      var half=new Uint8Array(GW*GH);
      for(var y=0;y<GH;y++)for(var x=rg[0];x<rg[1];x++)half[y*GW+x]=mask[y*GW+x];
      var any=false;for(var i=0;i<half.length;i++)if(half[i]){any=true;break;}
      if(any)s2.push(thickest(half));});
    if(s2.length){seeds=s2;solve();play();}});
  document.getElementById('ip-mold-play').addEventListener('click',play);
  setPart(PARTS[0].id);
})();
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Video","item":"https://hand-marketing.ru/videoproduction/"},'
  '{"@type":"ListItem","position":3,"name":"Обзорный ролик выставки интерпластика",'
  f'"item":"{URL}"}}]}}</script>')

VIDEO_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"VideoObject","name":"Обзорный ролик выставки интерпластика",'
  '"description":"Обзор выставки полимеров интерпластика в ЦВК «Экспоцентр» '
  'для Messe Düsseldorf.",'
  f'"thumbnailUrl":"https://hand-marketing.ru{IMG}/hall-engel.jpg",'
  f'"contentUrl":"https://hand-marketing.ru{VIDEO}",'
  '"uploadDate":"2026-08-31","duration":"PT2M12S"}</script>')

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
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/hall-engel.jpg">'
        '<link rel="stylesheet" href="/fonts/jura-nunito.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    parts = [{'id': p, 'name': n, 'note': d, 'sec': s} for p, n, d, s in PARTS]
    js = PAGE_JS.replace('%PARTS%', json.dumps(parts, ensure_ascii=False))
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="ip">{hero()}{brief()}{player()}{chain()}'
            f'{granules()}{mold()}{plan()}{rhythm()}{result()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}'
            f'{BREADCRUMB_LD}{VIDEO_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'interplastika')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
