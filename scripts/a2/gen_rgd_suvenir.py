#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/creative/rgd/suvenir/index.html: кейс «Новогодний сувенир
ЦМ РЖД» (календарь на 13 листов и сувенирный набор).

Материалы: печатный календарь на 13 полос (RGD_CD_191205.pdf), открытка
разворотом 200×200 мм, мокапы набора и съёмка тиража из кабинета дирекции.
Всё разбирает scripts/rgd-suvenir-assets.py, результат в
scripts/a2/rgd_suvenir_map.json.

Идея страницы. Проект был не про календарь, а про новогодний набор
целиком: шесть позиций, от бумажного пакета до ёлочного шара.
Поэтому страница идёт от концепции набора к его составу и только потом
разбирает календарь как главный предмет.

Концепция держится на трёх опорах: разгон полос связывает предметы,
календарь несёт содержание (месяц равен услуге дирекции), а Новый год
живёт в открытке и шаре, чтобы деловая часть набора не превращалась
в мишуру.

  • Перекидной календарь на тринадцать листов, главная механика и такой
    на сайте не было. Полосы показаны один в один, как их напечатали,
    вместе с их собственной календарной сеткой: титул с цифрами дирекции
    и двенадцать месяцев. Лист перекидывается через нарисованную пружину:
    уходит вверх вокруг верхней грани, как на стене.
    ⚠️ В файле RGD_CD_191205.pdf выходные во всех месяцах отмечены на одних
    позициях, а на мокапе тиража марта сетка правильная — значит в печать
    ушла более поздняя версия файла. Если она найдётся, листы надо заменить.
  • Разгон как один лист на весь набор, вторая новая механика. Полосы
    рисует движок на canvas (45°, четыре краски макета, нарастающая
    плотность), получается длинный рулон запечатанной бумаги. Предметы
    набора это вырубки в нём: шесть силуэтов вырезают из одного и того же
    рисунка свой кусок. Ползунок двигает рулон под вырубками, и видно,
    что айдентика на пакете, коробке и шаре это не шесть похожих узоров,
    а один рисунок, нарезанный по носителям. Тот же движок рисует фон
    обложки.
  • Открытка отдельным блоком: разворот 200×200 мм, где дирекция говорит
    не про терминалы, а про железную дорогу, плюс поздравление дословно
    с оборота.
  • Мокап против тиража: шар в макете был белый с бирюзовым разгоном,
    а в тираж ушёл красный с серебром, и он же снят в коробке на полке
    кабинета. Рядом ежедневник, снятый на рабочем столе дирекции.

Палитра снята с макета: заливки в нём ровные, поэтому мода квантованного
цвета даёт ровно печатные краски (бирюза #008A96, светлая #4EAEBA,
зелёный #42A83C, синий #4284B4, красный сетки #C01212).

Шрифты: Commissioner ведёт страницу, PT Sans Narrow держит календарную
сетку под печатной полосой (сам календарь набран узким гротеском Akrobat,
воспроизвести его на сайте нечем: в Google Fonts его нет, а вшитые в PDF
подмножества неполные).

Ассеты: mirror/images/rgd-suvenir/ (scripts/rgd-suvenir-assets.py).

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

IMG = '/images/rgd-suvenir'
URL = 'https://hand-marketing.ru/creative/rgd/suvenir/'
TITLE = 'Новогодний сувенир ЦМ РЖД: календарь и набор | Hand Marketing'
DESCR = ('Новогодний подарок Центральной дирекции по управлению '
         'терминально-складским комплексом РЖД: календарь на 13 листов, где '
         'каждый месяц это одна услуга дирекции, и сувенирный набор '
         'в единой айдентике.')

MAP = json.load(open(os.path.join(HERE, 'rgd_suvenir_map.json'), encoding='utf-8'))
SHEETS = MAP['sheets']
FIGURES = MAP['figures']
PAL = MAP['palette']
WHAT = MAP['what']

# ─── состав набора ─────────────────────────────────────────────────────────
# (слаг кадра; имя; строка про то, что с этим предметом делала айдентика;
#  техника из спецификации коротко). По договору позиций было семь, но
#  плащ-дождевик из кейса убран по просьбе клиента: съёмки у него нет,
#  и на прозрачной плёнке от айдентики остаётся один знак
KIT = [
    ('bag', 'Бумажный пакет',
     'Разгон занимает нижний угол и уходит на боковую стенку, знак ЦМ '
     'стоит по центру над ручками',
     'До 250×360×100 мм, мелованная бумага от 270 г/м², офсет с двух сторон, '
     'ламинация, витой шнур и кольца пикколо'),
    ('sheet-march', 'Перекидной календарь',
     'Тринадцать листов: титул с цифрами дирекции и двенадцать месяцев, '
     'на каждом одна услуга ЦМ',
     'Формат А3, мелованный картон от 300 г/м², глянцевая ламинация, '
     'навивка на белую пружину с ригелем'),
    ('diary', 'Ежедневник',
     'Единственный предмет набора с заливкой на всю обложку: разгон '
     'читается снизу вверх по тёмно-синему',
     'Формат А4, недатированный, эко-кожа с тиснением, блок от 170 страниц, '
     'бумага от 120 г/м²'),
    ('mugs', 'Термокружка',
     'Печать идёт по кольцу, поэтому от разгона осталась плашка со знаком. '
     'Собрано три цветовых варианта',
     'Силикон, нержавеющая сталь и пластик, объём от 0,5 л'),
    ('power', 'Портативное зарядное',
     'Узкая вырубка: в кадр попадают четыре полосы и один зелёный просвет',
     'Алюминий, 10 000 mAh, два выхода USB, картонная упаковка'),
    ('ball', 'Сувенирный шар',
     'Круглая вырубка режет полосы по дуге, поэтому знак пришлось поднять '
     'выше центра',
     'Стекло с матовым покрытием, диаметр от 10 см, пластиковая '
     'или картонная упаковка'),
]

# ─── что вырубает айдентику: шесть печатных носителей набора ───────────────
# (слаг кадра, имя, ключ силуэта) — календарь показан отдельным блоком
CUTS = [
    ('bag', 'Пакет', 'bag'),
    ('box', 'Коробка', 'box'),
    ('diary', 'Ежедневник', 'diary'),
    ('power', 'Аккумулятор', 'power'),
    ('mugs', 'Термокружка', 'mug'),
    ('ball', 'Шар', 'ball'),
]

# ─── силуэты вырубок: путь в поле 160×220 ──────────────────────────────────
SHAPES = {
    'bag': 'M20 60h120v150H20z',
    'box': 'M14 96h132v96H14z',
    'diary': 'M26 40h108a6 6 0 0 1 6 6v168a6 6 0 0 1-6 6H26z',
    'power': 'M48 46h64a10 10 0 0 1 10 10v148a10 10 0 0 1-10 10H48a10 10 0 0 1-10-10V56a10 10 0 0 1 10-10z',
    'mug': 'M46 66h68l-10 148a8 8 0 0 1-8 8H64a8 8 0 0 1-8-8z',
    'ball': 'M80 52a74 74 0 1 1 0 148 74 74 0 0 1 0-148z',
}
# ручки пакета и подвес шара рисуются поверх вырубки, в узор они не входят
EXTRA = {
    'bag': '<path d="M54 60V50a26 26 0 0 1 52 0v10" class="o"/>',
    'ball': '<path d="M80 52V38M70 30h20v10H70z" class="o"/>',
    'mug': '<path d="M42 52h76v14H42z" class="o"/>',
    'box': '<path d="M14 118h132" class="o"/>',
    'diary': '<path d="M40 40v180" class="o"/>',
    'power': '<path d="M70 190h20" class="o"/>',
}

# ─── состав работ ───────────────────────────────────────────────────────────
CRAFT = [
    ('Айдентика набора',
     'Разгон полос, плашка знака ЦМ и палитра. Один рисунок разложен '
     'по шести носителям: от листа календаря до ёлочного шара.'),
    ('Тринадцать листов',
     'Титул с цифрами дирекции и двенадцать месяцев. На каждом листе своя '
     'услуга ЦМ, её описание и параметры предоставления.'),
    ('Вёрстка и календарная сетка',
     'Полосы A4 под пружину, сетка на 2019 год с выходными и переносами, '
     'реквизиты дирекции на каждом листе.'),
    ('Открытка',
     'Разворот 200 на 200 мм: иллюстрация с новогодним составом на лице '
     'и поздравление дирекции на обороте.'),
    ('Предпечатная подготовка',
     'Подготовка макетов под печать и вырубку: календарь, открытка, пакет, '
     'коробка, ежедневник, аккумулятор, термокружка, шар.'),
]

CSS = """<style id="rs-css">
/* Кейс «Новогодний сувенир ЦМ РЖД». Правки только в gen_rgd_suvenir.py. */
.rs{--teal:%TEAL%;--tealL:%TEALL%;--green:%GREEN%;--blue:%BLUE%;--red:%RED%;
 --deep:%DEEP%;--ink:#16232B;--mute:#5E6C75;--paper:#fff;--day:#F2F5F6;
 --night:#0E1A21;--night2:#152530;--line:rgba(22,35,43,.13);
 --lineN:rgba(255,255,255,.16);
 font-family:'Commissioner',Arial,sans-serif;color:var(--ink);background:var(--paper);
 font-size:17px;line-height:1.6;overflow-x:hidden;-webkit-text-size-adjust:100%}
.rs *,.rs *::before,.rs *::after{box-sizing:border-box}
.rs p{margin:0 0 16px}
.rs section{padding:86px 40px}
.rs .in{max-width:1180px;margin:0 auto}
.rs .lbl{font-weight:700;font-size:12px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--teal);margin:0 0 18px}
.rs h2{font-size:clamp(28px,4.2vw,46px);font-weight:800;line-height:1.06;margin:0 0 20px;
 letter-spacing:-.015em}
.rs h3{font-size:20px;font-weight:700;margin:0 0 12px}
.rs .lead{font-size:clamp(17px,1.7vw,20px);line-height:1.55;max-width:780px;color:var(--mute)}
.rs .night{background:var(--night);color:#E6EDF0}
.rs .night h2,.rs .night h3{color:#fff}
.rs .night .lead{color:rgba(230,237,240,.66)}
.rs .night .lbl{color:var(--tealL)}
.rs .day{background:var(--day)}
.rs .note{font-size:13.5px;line-height:1.5;color:var(--mute)}
.rs figure{margin:0}
.rs figcaption{margin-top:9px;font-size:13.5px;line-height:1.5;color:var(--mute)}
.rs .night figcaption{color:rgba(230,237,240,.6)}

/* ── обложка ────────────────────────────────────────────────────────────── */
.rs-hero{position:relative;padding:0;background:var(--night);color:#E6EDF0;overflow:hidden}
.rs-hero__run{position:absolute;inset:0;width:100%;height:100%;display:block;
 background:linear-gradient(118deg,#0E1A21 30%,#0d3f4a 70%,#0E1A21 100%)}
/* завеса: слева текст читается по тёмному, справа разгон остаётся открытым */
.rs-hero__veil{position:absolute;inset:0;background:linear-gradient(102deg,
 rgba(14,26,33,.95) 0%,rgba(14,26,33,.88) 32%,rgba(14,26,33,.44) 64%,
 rgba(14,26,33,.06) 100%)}
.rs-hero__in{position:relative;max-width:1180px;margin:0 auto;padding:70px 40px 46px}
.rs-back{display:inline-block;font-size:14px;color:rgba(230,237,240,.62);
 text-decoration:none;margin-bottom:28px}
.rs-back:hover{color:var(--tealL)}
.rs-hero h1{font-size:clamp(32px,5.6vw,68px);line-height:1.03;font-weight:800;
 margin:0 0 20px;letter-spacing:-.025em;color:#fff;max-width:15em}
.rs-hero .lead{font-size:clamp(17px,1.9vw,22px);color:rgba(230,237,240,.74);max-width:640px}
.rs-facts{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--lineN);
 border-top:1px solid var(--lineN);border-bottom:1px solid var(--lineN);margin-top:46px}
.rs-facts div{background:var(--night);padding:22px 20px}
.rs-facts b{display:block;font-weight:700;font-size:15px;line-height:1.3;margin-bottom:5px;
 color:#fff}
.rs-facts span{font-size:14px;color:rgba(230,237,240,.62);line-height:1.45}

/* ── компания и задача ──────────────────────────────────────────────────── */
.rs-brief{display:grid;grid-template-columns:1fr 1fr;gap:56px}
.rs-brief .col p:last-child{margin-bottom:0}
.rs-brief a{color:var(--teal)}

/* ── концепция ──────────────────────────────────────────────────────────── */
.rs-concept{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;
 background:var(--line);border:1px solid var(--line);margin-top:34px}
.rs-concept div{background:var(--paper);padding:30px 26px}
.rs-concept b{display:block;font-weight:800;font-size:19px;margin-bottom:10px;
 color:var(--teal)}
.rs-concept span{font-size:15px;line-height:1.62;color:var(--mute)}

/* ── титульный лист: цифры дирекции ─────────────────────────────────────── */
.rs-fig__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;
 background:var(--line);border:1px solid var(--line);margin-top:34px}
.rs-fig__grid div{background:var(--paper);padding:24px 22px}
.rs-fig__grid b{display:block;font-size:clamp(26px,3.4vw,38px);font-weight:800;
 line-height:1;letter-spacing:-.02em;color:var(--teal);margin-bottom:8px}
.rs-fig__grid span{font-size:14.5px;line-height:1.45;color:var(--mute)}

/* ── перекидной календарь ───────────────────────────────────────────────── */
.rs-cal{display:grid;grid-template-columns:300px 1fr;gap:44px;margin-top:36px;
 align-items:start}
.rs-cal__list{display:flex;flex-direction:column;gap:1px;background:var(--lineN);
 border-top:1px solid var(--lineN);border-bottom:1px solid var(--lineN)}
.rs-cal__list button{display:grid;grid-template-columns:34px 1fr;gap:10px;align-items:baseline;
 text-align:left;border:0;background:var(--night);color:rgba(230,237,240,.66);
 padding:12px 14px;cursor:pointer;font:500 14px/1.35 'Commissioner',Arial,sans-serif;
 transition:background .18s,color .18s}
.rs-cal__list button i{font-style:normal;font-weight:700;font-size:13px;letter-spacing:.04em;
 color:var(--tealL)}
.rs-cal__list button:hover{background:var(--night2);color:#fff}
.rs-cal__list button[aria-current="true"]{background:var(--teal);color:#fff}
.rs-cal__list button[aria-current="true"] i{color:#fff}
.rs-cal__stage{position:relative}
.rs-cal__spring{display:grid;grid-template-columns:repeat(16,1fr);gap:0;height:26px;
 padding:0 8%;position:relative;z-index:9}
.rs-cal__spring i{display:block;height:26px;border:2px solid rgba(230,237,240,.5);
 border-top:0;border-radius:0 0 9px 9px;margin:0 3px}
.rs-cal__book{position:relative;perspective:2200px}
.rs-cal__book>div{position:relative;width:100%;aspect-ratio:210/297}
.rs-sh{position:absolute;inset:0;background:#fff;color:#1B2A32;overflow:hidden;
 transform-origin:top center;backface-visibility:hidden;
 box-shadow:0 24px 60px rgba(0,0,0,.42);
 transition:transform .62s cubic-bezier(.36,.06,.22,1),opacity .4s linear .12s;
}
.rs-sh.past{transform:rotateX(-116deg);opacity:0;pointer-events:none}
.rs-sh__pic{width:100%;height:100%;object-fit:contain;display:block;background:#fff}
.rs-cal__bar{display:flex;align-items:center;gap:14px;margin-top:22px}
.rs-cal__bar button{width:46px;height:46px;border:1px solid var(--lineN);background:none;
 color:#fff;cursor:pointer;font-size:19px;line-height:1;border-radius:50%;
 transition:background .18s,border-color .18s}
.rs-cal__bar button:hover{background:var(--teal);border-color:var(--teal)}
.rs-cal__bar button[disabled]{opacity:.32;cursor:default}
.rs-cal__bar button[disabled]:hover{background:none;border-color:var(--lineN)}
.rs-cal__count{font-weight:700;font-size:15px;letter-spacing:.04em}
.rs-cal__count span{color:rgba(230,237,240,.5)}
.rs-cal__hint{margin-left:auto;font-size:13.5px;color:rgba(230,237,240,.5)}
.rs-cal__real{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:52px;
 padding-top:34px;border-top:1px solid var(--lineN)}
.rs-cal__real img{width:100%;display:block;border-radius:2px}

/* ── открытка ───────────────────────────────────────────────────────────── */
.rs-card{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:34px}
.rs-card img{width:100%;display:block;border-radius:2px}
.rs-card__note{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:30px;
 padding-top:28px;border-top:1px solid var(--line)}
.rs-card__quote{font-size:16px;line-height:1.62;color:var(--mute);
 border-left:3px solid var(--teal);padding-left:20px;margin:0}
.rs-card__quote b{display:block;font-size:13px;letter-spacing:.06em;
 text-transform:uppercase;color:var(--teal);margin-top:12px;font-weight:700}

/* ── разгон: рулон и вырубки ────────────────────────────────────────────── */
.rs-roll{margin-top:36px}
.rs-roll__box{position:relative;background:#fff;border:1px solid var(--line);
 padding:26px 22px 14px;overflow:hidden}
.rs-roll__svg{display:block;width:100%;height:auto}
.rs-roll__svg .o{fill:none;stroke:var(--ink);stroke-width:3;stroke-linejoin:round;
 vector-effect:non-scaling-stroke}
.rs-roll__svg .fb{fill:var(--tealL)}
.rs-roll__svg .pd{fill:#F5F9FA}
.rs-roll__names{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin-top:12px}
.rs-roll__names span{font-weight:700;font-size:12.5px;letter-spacing:.04em;
 text-transform:uppercase;color:var(--mute);text-align:center}
.rs-roll__ctl{display:flex;align-items:center;gap:16px;margin-top:22px}
.rs-roll__ctl label{font-weight:700;font-size:12px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--mute);white-space:nowrap}
.rs-roll__ctl input{flex:1;accent-color:var(--teal);height:26px}
.rs-kit{display:grid;grid-template-columns:repeat(3,1fr);gap:30px 26px;margin-top:44px}
.rs-kit img{width:100%;aspect-ratio:4/3;object-fit:contain;display:block;
 border-radius:2px;background:var(--paper)}
.rs-kit h3{margin:14px 0 6px;font-size:18px}
.rs-kit p{margin:0;font-size:14.5px;line-height:1.55;color:var(--mute)}
.rs-kit__spec{margin-top:10px!important;font-size:13px!important;
 color:var(--mute);opacity:.78;border-top:1px solid var(--line);padding-top:10px}

/* ── мокап против тиража ────────────────────────────────────────────────── */
.rs-print{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:34px}
.rs-print--two{grid-template-columns:repeat(2,1fr)}
/* оба кадра шара вертикальные: широкая рамка оставляла бы полполя пустым */
.rs-print--two figure img{aspect-ratio:3/4}
.rs-print figure img{width:100%;aspect-ratio:4/3;object-fit:contain;display:block;
 border-radius:2px;background:var(--night2)}
.rs-print__row img{width:100%;display:block;border-radius:2px}
.rs-print__step{font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--tealL);margin-bottom:10px}
.rs-print__row{display:grid;grid-template-columns:1.33fr .75fr;gap:22px;
 margin-top:30px;align-items:start}

/* ── состав работ ───────────────────────────────────────────────────────── */
.rs-craft{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);
 border:1px solid var(--line);margin-top:34px}
.rs-craft div{background:var(--paper);padding:28px 26px}
.rs-craft b{display:block;font-weight:700;font-size:17px;margin-bottom:8px}
.rs-craft span{font-size:15px;line-height:1.6;color:var(--mute)}

/* ── лайтбокс ───────────────────────────────────────────────────────────── */
.rs-zoom{padding:0;border:0;background:none;cursor:zoom-in;display:block;
 line-height:0;width:100%}
.rs-lb{position:fixed;inset:0;z-index:9999;background:rgba(9,17,22,.95);display:none;
 align-items:center;justify-content:center;padding:32px}
.rs-lb.on{display:flex}
.rs-lb img{max-width:94vw;max-height:82vh;object-fit:contain;border-radius:2px}
.rs-lb__cap{position:absolute;left:0;right:0;bottom:20px;text-align:center;font-size:14px;
 color:rgba(255,255,255,.7);padding:0 24px}
.rs-lb__x{position:absolute;top:20px;right:20px;border:0;background:rgba(255,255,255,.14);
 color:#fff;cursor:pointer;width:46px;height:46px;border-radius:50%;font-size:20px}
.rs-lb__x:hover{background:var(--teal)}

/* ── адаптив ────────────────────────────────────────────────────────────── */
@media(max-width:1100px){
 .rs section{padding:70px 28px}
 .rs-hero__in{padding:52px 28px 38px}
 .rs-cal{grid-template-columns:1fr;gap:26px}
 .rs-cal__list{flex-direction:row;flex-wrap:wrap;background:none;border:0;gap:8px}
 .rs-cal__list button{flex:1 1 30%;border:1px solid var(--lineN)}
 .rs-cal__book{max-width:520px}
 .rs-cal__spring{max-width:520px}
 .rs-fig{grid-template-columns:1fr;gap:30px}
 .rs-brief{gap:34px}
 .rs-kit{grid-template-columns:repeat(2,1fr)}
 .rs-concept{grid-template-columns:1fr}
}
@media(max-width:760px){
 .rs{font-size:16px}
 .rs section{padding:52px 18px}
 .rs-hero__in{padding:40px 18px 30px}
 .rs-hero__veil{background:linear-gradient(180deg,rgba(14,26,33,.9) 0%,
  rgba(14,26,33,.86) 70%,rgba(14,26,33,.6) 100%)}
 .rs-facts{grid-template-columns:1fr 1fr}
 .rs-brief,.rs-craft,.rs-cal__real,.rs-print__row,.rs-card,
 .rs-card__note{grid-template-columns:1fr}
 .rs-fig__grid,.rs-concept{grid-template-columns:1fr}
 .rs-kit{grid-template-columns:1fr;gap:24px}
 .rs-print{grid-template-columns:1fr}
 .rs-cal__list button{flex:1 1 46%}
 .rs-cal__hint{display:none}
 .rs-roll__box{padding:16px 12px 10px;overflow-x:auto;
  -webkit-overflow-scrolling:touch}
 .rs-roll__inner{min-width:700px}
 .rs-lb{padding:14px}
}
@media(max-height:470px) and (orientation:landscape){
 .rs section{padding:40px 22px}
 .rs-hero__in{padding:32px 22px 24px}
 .rs-cal__book{max-width:300px}
 .rs-cal__spring{max-width:300px}
 .rs-lb img{max-height:70vh}
}
@media(prefers-reduced-motion:reduce){
 .rs-sh{transition-duration:.01ms}
}
</style>"""
for k, v in PAL.items():
    CSS = CSS.replace('%{}%'.format(k.upper()), v)


def pic(slug, sizes, cls='', extra=''):
    """Кадр в трёх размерах: браузер берёт нужный по ширине места."""
    a = WHAT.get(slug, '')
    c = ' class="{}"'.format(cls) if cls else ''
    return ('<img{c} src="{i}/{s}-s.jpg" srcset="{i}/{s}-s.jpg 640w, '
            '{i}/{s}-m.jpg 1000w, {i}/{s}.jpg 1400w" sizes="{z}" alt="{a}" '
            'loading="lazy" decoding="async"{e}>').format(
                c=c, i=IMG, s=slug, z=sizes, a=a, e=extra)


def zoom(slug, sizes):
    """Кадр, который открывается в лайтбоксе."""
    return ('<button class="rs-zoom" type="button" data-zoom="{s}">{p}</button>'
            .format(s=slug, p=pic(slug, sizes)))


def hero():
    facts = [
        ('6 позиций', 'Пакет, календарь, ежедневник, термокружка, '
                      'зарядное, шар'),
        ('13 листов', 'Календарь А3 на пружине: титул и двенадцать месяцев'),
        ('12 услуг', 'Каждый месяц закреплён за услугой дирекции'),
        ('Один разгон', 'Айдентика набрана одним рисунком на весь набор'),
    ]
    f = ''.join('<div><b>{}</b><span>{}</span></div>'.format(t, d)
                for t, d in facts)
    return (
      '<section class="rs-hero">'
      '<canvas class="rs-hero__run" id="rsHero" aria-hidden="true"></canvas>'
      '<div class="rs-hero__veil" aria-hidden="true"></div>'
      '<div class="rs-hero__in">'
      '<a class="rs-back" href="/project">← Все проекты</a>'
      '<div class="lbl" style="color:var(--tealL)">Creative &amp; Design · '
      'ЦМ РЖД</div>'
      '<h1>Новогодний набор, который рассказывает про дирекцию</h1>'
      '<p class="lead">Подарок Центральной дирекции по управлению '
      'терминально-складским комплексом: шесть позиций от бумажного пакета '
      'до ёлочного шара. Мы придумали для набора одну концепцию и раскатали '
      'её на все предметы, а календарь внутри неё взял на себя содержание: '
      'каждый его месяц закреплён за услугой ЦМ.</p>'
      '<div class="rs-facts">{}</div>'
      '</div></section>').format(f)


def brief():
    return (
      '<section><div class="in rs-brief">'
      '<div class="col"><div class="lbl">Заказчик</div>'
      '<h3>Дирекция ЦМ</h3>'
      '<p>Центральная дирекция по управлению терминально-складским '
      'комплексом это филиал ОАО «РЖД». Она отвечает за грузовые дворы '
      'сети: погрузку и выгрузку, хранение, промывку вагонов, склады '
      'временного хранения, аренду площадок и завоз груза автотранспортом.</p>'
      '<p>Про масштаб дирекции мы рассказывали в соседнем проекте: '
      '<a href="/video/rgd/history/">фильм «История успеха ЦМ»</a>, где те же '
      'услуги разложены по схеме грузового двора.</p></div>'
      '<div class="col"><div class="lbl">Задача</div>'
      '<h3>Концепция, а не логотип на шести предметах</h3>'
      '<p>Собрать новогодний подарок дирекции: шесть позиций набора, каждая '
      'со своим материалом и способом печати. Требование договора звучало '
      'коротко: дизайн по брендбуку ОАО «РЖД», единый на всех элементах, '
      'а календарь должен покрывать услуги дирекции.</p>'
      '<p>Задача поэтому была не оформительская. Нужна была концепция, '
      'которая одинаково хорошо ложится и на бумажный пакет, и на стекло '
      'ёлочного шара, и при этом оставляет календарю место под смысл.</p>'
      '</div></div></section>')


def concept():
    """Концепция набора: три опоры, на которых собраны все семь предметов."""
    parts = [
        ('Разгон', 'Фирменный рисунок дирекции: полосы под 45 градусов, '
         'четыре краски и белые просветы, плотность нарастает к углу. '
         'Он держит набор вместе: один и тот же рисунок нарезан по семи '
         'предметам, а не нарисован для каждого заново.'),
        ('Год как каталог услуг', 'Календарь не иллюстрирует зиму, а работает: '
         'титул отдан цифрам дирекции, каждый месяц закреплён за услугой ЦМ '
         'и её параметрами. Подарок висит у клиента весь год и весь год '
         'объясняет, что дирекция умеет.'),
        ('Праздник отдельной нотой', 'Новый год живёт не в календаре, '
         'а в открытке и шаре: состав с Дедом Морозом, бумажный лес, '
         'морозное напыление на стекле. Так деловая часть набора '
         'не превращается в ёлочную мишуру.'),
    ]
    cells = ''.join(
        '<div><b>{}</b><span>{}</span></div>'.format(t, d) for t, d in parts)
    return (
      '<section><div class="in">'
      '<div class="lbl">Концепция</div>'
      '<h2>Три опоры, на которых собран набор</h2>'
      '<p class="lead">Подарок от дирекции получают клиенты и партнёры, '
      'то есть люди, которые возят через её терминалы грузы. Значит, '
      'подарок мог не только поздравлять, но и работать. Отсюда разделение '
      'ролей: айдентика связывает предметы, календарь несёт содержание, '
      'открытка и шар отвечают за праздник.</p>'
      '<div class="rs-concept">{}</div>'
      '</div></section>').format(cells)


def figures():
    cells = ''.join('<div><b>{}</b><span>{}</span></div>'.format(f['n'], f['what'])
                    for f in FIGURES)
    return (
      '<section class="day"><div class="in">'
      '<div class="lbl">Титульный лист</div>'
      '<h2>ЦМ сегодня это</h2>'
      '<p class="lead">Первый лист календаря не отдан ни одному месяцу: '
      'на нём дирекция в цифрах. Они задают тон остальным двенадцати, '
      'дальше идут не картинки про логистику, а конкретные услуги '
      'с параметрами.</p>'
      '<div class="rs-fig__grid">{c}</div>'
      '</div></section>').format(c=cells)


def sheet(i):
    """Лист календаря: печатная полоса целиком, как её напечатали."""
    sh = SHEETS[i - 1] if i else None
    slug = 'sheet-{:02d}'.format(i)
    return (
      '<article class="rs-sh" data-i="{i}" aria-hidden="{h}">'
      '<img class="rs-sh__pic" src="{img}/{s}-m.jpg" '
      'srcset="{img}/{s}-s.jpg 640w, {img}/{s}-m.jpg 1000w, '
      '{img}/{s}.jpg 1240w" sizes="(max-width:1100px) 92vw, 620px" '
      'alt="{a}" loading="{l}" decoding="async"></article>').format(
          i=i, h='false' if i == 0 else 'true', img=IMG, s=slug,
          a=WHAT.get(slug, ''), l='eager' if i == 0 else 'lazy')


def calendar():
    items = ('<button type="button" data-go="0" aria-current="true">'
             '<i>00</i><span>Титул: ЦМ сегодня это</span></button>')
    items += ''.join(
        '<button type="button" data-go="{i}" aria-current="false">'
        '<i>{n}</i><span>{t}</span></button>'.format(
            i=i + 1, n=x['n'], t=x['title'].capitalize())
        for i, x in enumerate(SHEETS))
    sheets = ''.join(sheet(i) for i in range(len(SHEETS) + 1))
    return (
      '<section class="night"><div class="in">'
      '<div class="lbl">Тринадцать листов</div>'
      '<h2>Месяц равен услуге</h2>'
      '<p class="lead">Главный предмет набора. Тринадцать полос А3 '
      'на пружине: титул отдан цифрам дирекции, дальше двенадцать месяцев, '
      'и на каждом ровно одна услуга ЦМ с описанием и параметрами. Полосы '
      'показаны один в один, как их напечатали.</p>'
      '<div class="rs-cal">'
      '<div class="rs-cal__list" id="rsList">{i}</div>'
      '<div class="rs-cal__stage">'
      '<div class="rs-cal__spring" aria-hidden="true">'
      + '<i></i>' * 16 +
      '</div>'
      '<div class="rs-cal__book" id="rsBook"><div>{s}</div></div>'
      '<div class="rs-cal__bar">'
      '<button type="button" id="rsPrev" aria-label="Предыдущий лист" '
      'disabled>‹</button>'
      '<button type="button" id="rsNext" aria-label="Следующий лист">›</button>'
      '<div class="rs-cal__count"><b id="rsNum">01</b><span> / 13</span></div>'
      '<div class="rs-cal__hint">Перекидывается стрелками, кликом по месяцу '
      'и свайпом</div>'
      '</div></div></div>'
      '<div class="rs-cal__real">'
      '<div><h3>Как устроен лист</h3>'
      '<p class="lead">Модуль у всех двенадцати полос один: слева плашка '
      'знака ЦМ и описание услуги узкой колонкой, справа номер и название '
      'месяца, под ними коллаж, где фотография услуги разрезана диагоналями '
      'фирменного разгона. От месяца к месяцу меняются только текст, кадр '
      'и раскладка чисел.</p>'
      '<p class="note">Год закрывает весь профиль дирекции: от комплексной '
      'терминально-логистической услуги в январе до разработки схем '
      'погрузки в декабре. Календарь висит у клиента весь год и весь год '
      'работает каталогом.</p></div>'
      '</div></div></section>').format(i=items, s=sheets)


def roll():
    """Рулон айдентики и шесть вырубок по нему."""
    w, h, step = 1200, 240, 200
    clips, imgs, outs, names = '', '', '', ''
    for i, (_slug, name, shape) in enumerate(CUTS):
        d = SHAPES[shape]
        # силуэт нарисован в поле 160×220, ставим его в свою ячейку и ужимаем
        tr = 'translate({} 8) scale(.98)'.format(i * step + 18)
        clips += ('<clipPath id="rsC{i}" transform="{t}"><path d="{d}"/>'
                  '</clipPath>').format(i=i, t=tr, d=d)
        imgs += ('<path class="pd" d="{d}" transform="{t}"/>'
                 '<g clip-path="url(#rsC{i})">'
                 '<image href="" class="rs-roll__img" x="-600" y="-40" '
                 'width="2400" height="320" preserveAspectRatio="none"/></g>'
                 '<path class="fb" d="{d}" transform="{t}" data-fb="1"/>'
                 ).format(i=i, d=d, t=tr)
        outs += '<g transform="{t}"><path class="o" d="{d}"/>{e}</g>'.format(
            t=tr, d=d, e=EXTRA[shape])
        names += '<span>{}</span>'.format(name)
    return (
      '<section><div class="in">'
      '<div class="lbl">Айдентика</div>'
      '<h2>Один разгон, нарезанный по носителям</h2>'
      '<p class="lead">Фирменный рисунок дирекции это разгон: полосы под '
      '45 градусов, четыре краски и белые просветы, плотность нарастает '
      'к углу. На странице его рисует движок по параметрам, снятым '
      'с макета, и получается длинный лист запечатанной бумаги. Предметы '
      'набора это вырубки в нём: каждый силуэт забирает из общего рисунка '
      'свой кусок.</p>'
      '<div class="rs-roll"><div class="rs-roll__box">'
      '<div class="rs-roll__inner">'
      '<svg class="rs-roll__svg" viewBox="0 0 {w} {h}" '
      'role="img" aria-label="Шесть предметов набора как вырубки в одном '
      'листе фирменного разгона">'
      '<defs>{c}</defs><g id="rsRollG">'
      '<image id="rsRollBack" href="" x="-600" y="-40" width="2400" '
      'height="320" preserveAspectRatio="none" opacity=".16"/>{i}</g>'
      '<g>{o}</g></svg>'
      '<div class="rs-roll__names">{n}</div></div></div>'
      '<div class="rs-roll__ctl"><label for="rsSlide">Двигать рулон</label>'
      '<input id="rsSlide" type="range" min="0" max="100" value="34" '
      'aria-label="Положение вырубок на рулоне"></div>'
      '<p class="note" style="margin-top:14px">Вырубки стоят на месте, '
      'двигается лист под ними. Полосы переходят с предмета на предмет '
      'без разрыва: это и значит, что набор собран одной айдентикой, '
      'а не шестью похожими узорами.</p></div>'
      '</div></section>').format(w=w, h=h, c=clips, i=imgs, o=outs, n=names)


def card():
    """Открытка: разворот 200×200 мм, лицо и оборот."""
    # текст поздравления берём дословно с оборота (разбор в assets-скрипте),
    # подпись отделяем: она идёт от лица дирекции
    txt = MAP['card']
    cut = txt.find('От лица коллектива')
    hello = txt[:cut].strip() if cut > 0 else txt
    sign = txt[cut:].strip() if cut > 0 else ''
    return (
      '<section><div class="in">'
      '<div class="lbl">Открытка</div>'
      '<h2>Состав, который везёт поздравление</h2>'
      '<p class="lead">Квадратный разворот 200 на 200 мм в наборе отвечает '
      'за собственно праздник. Календарь говорит про терминалы и погрузку, '
      'открытка про то, что дирекция это железная дорога: по бумажному лесу '
      'идёт состав с Дедом Морозом в кабине, знак ЦМ подвешен над путями '
      'на табличке.</p>'
      '<div class="rs-card">'
      '<figure>{f}<figcaption>Лицо открытки</figcaption></figure>'
      '<figure>{b}<figcaption>Оборот с поздравлением '
      'дирекции</figcaption></figure>'
      '</div>'
      '<div class="rs-card__note">'
      '<p class="rs-card__quote">{h}<b>{s}</b></p>'
      '<div><h3>Одна айдентика, два регистра</h3>'
      '<p>Набор должен был работать в двух режимах сразу. Календарь '
      'висит в кабинете весь год и объясняет услуги, поэтому он строгий: '
      'фотография, цифры, сетка. Открытку вручают один раз, и здесь можно '
      'иллюстрацию.</p>'
      '<p class="note">Связывает их разгон: на календарных полосах он '
      'режет фотографии по диагонали, на обороте открытки уходит из угла, '
      'на предметах набора становится печатью.</p></div>'
      '</div></div></section>').format(
          f=zoom('card-front', '(max-width:760px) 100vw, 560px'),
          b=zoom('card-back', '(max-width:760px) 100vw, 560px'),
          h=hello, s=sign)


def kit():
    """Состав набора: предметы со спецификацией из договора."""
    cards = ''
    for slug, name, what, spec in KIT:
        cards += ('<div>{p}<h3>{n}</h3><p>{w}</p>'
                  '<p class="rs-kit__spec">{s}</p></div>').format(
                      p=zoom(slug, '(max-width:760px) 100vw, '
                                   '(max-width:1100px) 46vw, 360px'),
                      n=name, w=what, s=spec)
    return (
      '<section class="day"><div class="in">'
      '<div class="lbl">Состав</div>'
      '<h2>Шесть позиций набора</h2>'
      '<p class="lead">Договор описывал набор списком: пакет, календарь, '
      'ежедневник, термокружка, зарядное устройство и ёлочный шар. '
      'Предметы разные по форме, материалу и способу печати, поэтому одна '
      'и та же айдентика на каждом обрезана по-своему. Общими остаются знак '
      'ЦМ, палитра и направление разгона.</p>'
      '<div class="rs-kit">{}</div>'
      '</div></section>').format(cards)


def print_run():
    return (
      '<section class="night"><div class="in">'
      '<div class="lbl">Тираж</div>'
      '<h2>От мокапа до полки в кабинете</h2>'
      '<p class="lead">Часть набора клиент снял уже напечатанной и прислал '
      'кадры со своих столов. На шаре между макетом и тиражом произошла '
      'замена: белый со стеклянным разгоном не пошёл, вместо него сделали '
      'красный с серебряным знаком и морозным напылением.</p>'
      '<div class="rs-print rs-print--two">'
      '<figure><div class="rs-print__step">Утверждено в печать</div>{b}'
      '<figcaption>Шар, ушедший в тираж</figcaption></figure>'
      '<figure><div class="rs-print__step">13 декабря 2018</div>{c}'
      '<figcaption>Шар в упаковке, кабинет дирекции</figcaption></figure>'
      '</div>'
      '<div class="rs-print__row">'
      '<figure>{d}<figcaption>Ежедневник на столе дирекции, '
      '4 декабря 2018</figcaption></figure>'
      '<figure>{e}<figcaption>Папка из того же набора</figcaption></figure>'
      '</div></div></section>').format(
          b=zoom('ball-red', '(max-width:760px) 100vw, 480px'),
          c=zoom('ball-box', '(max-width:760px) 100vw, 480px'),
          d=zoom('diary-print', '(max-width:760px) 100vw, 560px'),
          e=zoom('folder-print', '(max-width:760px) 100vw, 560px'))


def craft():
    cells = ''.join('<div><b>{}</b><span>{}</span></div>'.format(t, d)
                    for t, d in CRAFT)
    return (
      '<section><div class="in">'
      '<div class="lbl">Состав работ</div>'
      '<h2>Что сделали</h2>'
      '<div class="rs-craft">{}</div>'
      '</div></section>').format(cells)


def lightbox():
    return ('<div class="rs-lb" id="rsLb" role="dialog" aria-modal="true" '
            'aria-label="Просмотр кадра"><img alt="" decoding="async">'
            '<div class="rs-lb__cap"></div>'
            '<button class="rs-lb__x" type="button" aria-label="Закрыть">×'
            '</button></div>')


PAGE_JS = """<script>(function(){
var PAL=%PAL%, WHAT=%WHAT%, IMG='%IMG%';
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ── движок разгона ────────────────────────────────────────────────────────
   Полоса это прямоугольник в системе координат, повёрнутой на 45 градусов.
   Дорожки идут поперёк направления полос, плотность растёт вдоль разгона,
   часть полос с изломом — как на макете. Генератор детерминированный:
   один и тот же seed всегда даёт один и тот же рисунок. */
function rnd32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);
 t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}

function paintRun(ctx,W,H,o){
  var r=rnd32(o.seed||7);
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle=o.bg;ctx.fillRect(0,0,W,H);
  var diag=Math.sqrt(W*W+H*H), lane=o.lane||Math.max(9,H/16);
  ctx.save();
  ctx.translate(0,H);
  ctx.rotate(-Math.PI/4);
  var lanes=Math.ceil(diag*1.7/lane);
  for(var i=0;i<lanes;i++){
    var y=i*lane-diag*0.62;
    var across=i/lanes;                       // положение поперёк разгона
    var x=-diag*0.35;
    while(x<diag*1.25){
      var along=(x+diag*0.35)/(diag*1.6);
      var f=o.flat||0;
      var dens=o.dens*((1-f)*(0.32+1.5*along)+f*1.05)
                     *((1-f)*(0.45+1.25*(1-across))+f*1.0);
      var len=lane*(1.4+r()*(3+10*Math.min(1,dens)));
      if(r()<Math.min(0.92,dens)){
        var c=o.cols[Math.floor(r()*o.cols.length)];
        var th=lane*(0.3+r()*0.62);
        ctx.fillStyle=c;
        ctx.globalAlpha=o.alpha||1;
        ctx.fillRect(x,y,len,th);
        /* излом: продолжение полосы уходит на соседнюю дорожку */
        if(r()<0.16){ctx.fillRect(x+len,y+(r()<0.5?-lane:lane)*0.62,
                                  len*(0.3+r()*0.7),th);}
      }
      x+=len+lane*(0.14+r()*1.15);
    }
  }
  ctx.restore();
  ctx.globalAlpha=1;
}

/* Один рулон на всю страницу: обложка рисуется своим тёмным набором красок,
   светлый рулон уходит и в окна листов, и в вырубки предметов. */
function makeRoll(){
  var c=document.createElement('canvas');
  c.width=2400;c.height=320;
  paintRun(c.getContext('2d'),2400,320,{
    seed:4, bg:'#FFFFFF', lane:22, dens:1.25, flat:.55,
    cols:[PAL.teal,PAL.teal,PAL.teal,PAL.tealLight,PAL.tealLight,PAL.tealLight,
          PAL.blue,PAL.blue,'#0B6E79','#8FD3DA','#8FD3DA',PAL.green,
          '#FFFFFF','#E3EDF0']});
  return c.toDataURL('image/png');
}

var roll=null;
try{roll=makeRoll();}catch(e){roll=null;}
if(roll){
  /* вырубки предметов */
  var back=document.getElementById('rsRollBack');
  if(back){back.setAttributeNS('http://www.w3.org/1999/xlink','href',roll);
           back.setAttribute('href',roll);}
  var imgs=document.querySelectorAll('.rs-roll__img');
  for(var j=0;j<imgs.length;j++){
    imgs[j].setAttributeNS('http://www.w3.org/1999/xlink','href',roll);
    imgs[j].setAttribute('href',roll);
  }
  var fb=document.querySelectorAll('[data-fb]');
  for(var f=0;f<fb.length;f++){fb[f].style.display='none';}
}

/* обложка: тот же движок, но на ночном фоне и крупнее */
var hero=document.getElementById('rsHero');
if(hero&&hero.getContext){
  var draw=function(){
    var w=hero.clientWidth||1200,h=hero.clientHeight||520;
    var dpr=Math.min(2,window.devicePixelRatio||1);
    hero.width=Math.round(w*dpr);hero.height=Math.round(h*dpr);
    var g=hero.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);
    paintRun(g,w,h,{seed:2019, bg:'#0E1A21', lane:Math.max(16,h/13), dens:0.5,
      alpha:.9,
      cols:[PAL.teal,PAL.tealLight,PAL.blue,'#0E3B47','#12505E','#0E3B47',
            PAL.green,'#17323D','#0E1A21','#17323D']});
  };
  draw();
  var t=null;
  window.addEventListener('resize',function(){
    clearTimeout(t);t=setTimeout(draw,180);});
}

/* ── перекидной календарь ───────────────────────────────────────────────── */
var book=document.getElementById('rsBook');
if(book){
  var shs=[].slice.call(book.querySelectorAll('.rs-sh'));
  var list=[].slice.call(document.querySelectorAll('#rsList button'));
  var prev=document.getElementById('rsPrev'),next=document.getElementById('rsNext');
  var num=document.getElementById('rsNum'),cur=0,N=shs.length;
  shs.forEach(function(s,i){s.style.zIndex=String(N-i);});
  function go(k){
    cur=Math.max(0,Math.min(N-1,k));
    shs.forEach(function(s,i){
      var past=i<cur;
      s.classList.toggle('past',past);
      s.setAttribute('aria-hidden',i===cur?'false':'true');
    });
    list.forEach(function(b,i){b.setAttribute('aria-current',i===cur?'true':'false');});
    num.textContent=(cur+1<10?'0':'')+(cur+1);
    prev.disabled=cur===0;next.disabled=cur===N-1;
  }
  prev.addEventListener('click',function(){go(cur-1);});
  next.addEventListener('click',function(){go(cur+1);});
  list.forEach(function(b){b.addEventListener('click',function(){
    go(+b.getAttribute('data-go'));});});
  book.setAttribute('tabindex','0');
  book.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key==='ArrowDown'){go(cur+1);e.preventDefault();}
    if(e.key==='ArrowLeft'||e.key==='ArrowUp'){go(cur-1);e.preventDefault();}
  });
  var sx=null,sy=null;
  book.addEventListener('touchstart',function(e){
    sx=e.touches[0].clientX;sy=e.touches[0].clientY;},{passive:true});
  book.addEventListener('touchend',function(e){
    if(sx===null)return;
    var dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;
    if(Math.abs(dx)>44&&Math.abs(dx)>Math.abs(dy)){go(cur+(dx<0?1:-1));}
    else if(Math.abs(dy)>44&&Math.abs(dy)>Math.abs(dx)){go(cur+(dy<0?1:-1));}
    sx=sy=null;},{passive:true});
  go(0);
}

/* ── ползунок рулона ────────────────────────────────────────────────────── */
var slide=document.getElementById('rsSlide'),rollG=document.getElementById('rsRollG');
if(slide&&rollG){
  var band=[].slice.call(rollG.querySelectorAll('image'));
  var move=function(){
    var x=-600-slide.value*7;
    band.forEach(function(n){n.setAttribute('x',String(x));});};
  slide.addEventListener('input',move);
  move();
}

/* ── лайтбокс ───────────────────────────────────────────────────────────── */
var lb=document.getElementById('rsLb');
if(lb){
  var im=lb.querySelector('img'),cp=lb.querySelector('.rs-lb__cap');
  function close(){lb.classList.remove('on');document.body.style.overflow='';}
  document.addEventListener('click',function(e){
    var b=e.target.closest?e.target.closest('[data-zoom]'):null;
    if(b){var s=b.getAttribute('data-zoom');
      im.src=IMG+'/'+s+'.jpg';im.alt=WHAT[s]||'';cp.textContent=WHAT[s]||'';
      lb.classList.add('on');document.body.style.overflow='hidden';return;}
    if(e.target===lb||e.target===im||e.target.closest('.rs-lb__x'))close();
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&lb.classList.contains('on'))close();});
}
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Новогодний сувенир ЦМ РЖД",'
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
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/sheet-title.jpg">'
        '<link rel="stylesheet" href="/fonts/commissioner-ptnarrow.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    js = (PAGE_JS.replace('%PAL%', json.dumps(PAL))
                 .replace('%WHAT%', json.dumps(WHAT, ensure_ascii=False))
                 .replace('%IMG%', IMG))
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="rs">{hero()}{brief()}{concept()}{kit()}'
            f'{figures()}{calendar()}{card()}{roll()}{print_run()}{craft()}'
            '</main>'
            f'{lightbox()}<a id="lead"></a>{rc.footer()}{rc.JS}{js}'
            f'{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'creative', 'rgd', 'suvenir')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
