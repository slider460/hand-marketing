#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/mozaika/index.html: кейс «Ролик ТРЦ „Мозаика“».

Материал один: media/mozaika.mp4 — презентационный фильм о комплексе на
134 000 м² у метро «Дубровка», 4:31. Мы сняли и смонтировали его осенью 2018
и показали арендаторам в зале на вечере «Пора выходить на свет» (наш же кейс
/event/mozaika/: на фотографии экрана видно кадр 2:26 из этого ролика).

Идея страницы. Знак «Мозаики» в заставке собран как мозаика: буквы — цветные
плашки, в части плашек вместо цвета стоит фотография. Ровно так же собрана
главная механика кейса.

  • «Весь ролик одним листом» — 271 плитка, по одной на секунду ролика.
    Плитки нарезаны одним спрайтом (scripts/mozaika-video-assets.py →
    strip.jpg, 16×17 по 160×90) и покрашены в четыре цвета знака по частям
    фильма: лист читается как мозаика цветных зон, наведение снимает краску
    и показывает кадр, нажатие ставит плеер на эту секунду. Пока ролик идёт,
    плитка текущей секунды подсвечена — лист работает шкалой воспроизведения.
    Такой механики на сайте не было.
  • Кривая «Открытие магазинов 2016-2018. GLA %» снята с кадра попиксельно
    (scripts/a2/mozaika_video_map.json) и перерисована живым SVG: 54,0 % →
    75,0 %. Рядом посещаемость по годам с той же экранной плашки.
  • Стена из 13 синхронов: портреты вырезаны по лицу из кадров, титры набраны
    заново, клик по карточке открывает отрезок этого спикера в плеере.

Цифры, названия и должности сняты с экранных плашек ролика, ничего не
додумано. Палитра снята пипеткой с заставки: оранжевый фон #E99614, маджента
#DF114A, бирюза #2CD8B0, тёмно-синий #0C1557.

Шрифты: Russo One (квадратная геометрия, родня буквам знака) + Alegreya Sans.

Ассеты: mirror/images/mozaika-video/ (scripts/mozaika-video-assets.py).

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

IMG = '/images/mozaika-video'
VIDEO = '/media/mozaika.mp4'          # источник: scripts/a2/video_map.json
EVENT_IMG = '/images/mozaika'         # кадры вечера, кейс /event/mozaika/
URL = 'https://hand-marketing.ru/video/mozaika/'
MAP = json.load(open(os.path.join(HERE, 'mozaika_video_map.json'), encoding='utf-8'))

DUR = 270.6            # ffprobe
TILES = 271            # кадров в контактном листе, по одному на секунду
SHEET_COLS, SHEET_ROWS = 16, 17       # геометрия спрайта strip.jpg

# ─── части фильма: (ключ, название, старт, конец, цвет, что внутри) ─────────
# границы сняты детектором склеек (ffmpeg scene>0.25), цвета — четыре цвета
# знака «Мозаики» из заставки, они идут по кругу: цвет отмечает смену части,
# а не уникален сам по себе. Финал возвращается к оранжевому заставки честно —
# в конце ролика стоит тот же знак, что и в начале.
PARTS = [
    ('logo', 'Знак', 0, 7.0, '#E99614',
     'Заставка: знак «Мозаики» собирается из цветных плашек, в части плашек '
     'вместо цвета стоит фотография, ниже рукописное «Делай интересно».'),
    ('object', 'Комплекс', 7.0, 24.4, '#0C1557',
     'Комплекс с воздуха на фоне района, фасады, входная группа, первые метры '
     'галереи и поток людей внутри.'),
    ('numbers', 'Цифры и новые магазины', 24.4, 61.3, '#DF114A',
     'График заполняемости и посещаемость по годам, торговая и общая площадь, '
     'парковка, магазины, открывшиеся к съёмке.'),
    ('tenants', 'Арендаторы и события', 61.3, 86.1, '#2CD8B0',
     'Вывески якорей одна за другой, семьи в галерее, заезд колясок, '
     'фитнес-шоу на сцене комплекса.'),
    ('district', 'Район и МЦК', 86.1, 123.0, '#E99614',
     'Аэросъёмка района, ж/д и развязок, платформа МЦК «Дубровка», крытый '
     'переход, остановка и фирменные маршрутки.'),
    ('map', 'Карта подъездов и досуг', 123.0, 146.8, '#0C1557',
     '3D-карта с Третьим транспортным кольцом и съездами, детский мастер-класс '
     'и игровая зона комплекса.'),
    ('talks', 'Тринадцать синхронов', 146.8, 265.6, '#DF114A',
     'Арендаторы и руководители комплекса говорят на камеру, каждый снят '
     'на своём месте, а не в переговорной.'),
    ('final', 'Финал', 265.6, DUR, '#E99614',
     'Тот же знак, что и в начале ролика.'),
]

# ─── синхроны: (слаг, имя, должность, бренд, старт, конец) ──────────────────
# имена и должности сняты с экранных титров ролика
SPEAKERS = [
    ('torkunov', 'Михаил Торкунов', 'генеральный директор',
     'парк виртуальной реальности «Engage VR»', 146.8, 154.4),
    ('avdokhina', 'Елена Авдохина', 'территориальный управляющий',
     '«ANTIGA»', 154.4, 161.9),
    ('tikhonenkova', 'Татьяна Тихоненкова', 'менеджер по рекламе',
     '«Kari»', 161.9, 167.2),
    ('skuba', 'Виктория Скуба', 'директор кинотеатра',
     '«Киномакс»', 167.2, 174.9),
    ('skoritskaya', 'Юлия Скорицкая', 'PR-директор',
     '«Ruxara»', 174.9, 181.8),
    ('bokovanova', 'Ольга Бокованова', 'управляющая гипермаркета',
     '«Лента»', 181.8, 186.3),
    ('shirkevich', 'Ольга Ширкевич', 'заместитель директора гипермаркета',
     '«Домовой»', 186.3, 197.1),
    ('ilyashenko', 'Роман Ильяшенко', 'директор ресторана',
     '«Il Patio»', 197.1, 204.7),
    ('kaya', 'Дарья Кайа', 'директор магазина',
     '«КупиКоляску.ru»', 204.7, 215.5),
    ('lomakin', 'Григорий Ломакин', 'владелец фитнес-клуба',
     '«Лето»', 215.5, 222.2),
    ('eremeev', 'Николай Еремеев',
     'директор по развитию сети магазинов цифровой и бытовой техники',
     '«DNS»', 222.2, 229.8),
    ('kuzmin', 'Алексей Кузьмин', 'управляющий директор',
     'ТРЦ «Мозаика»', 229.8, 247.9),
    ('starichenko', 'Ольга Стариченко', 'коммерческий директор',
     'ТРЦ «Мозаика»', 255.9, 265.6),
]

# ─── посещаемость с экранной плашки ролика ──────────────────────────────────
TRAFFIC = [
    ('2016 год', '4 552 017', 4552017),
    ('2017 год', '7 724 744', 7724744),
    ('январь-март 2018', '2 182 904', 2182904),
]

# ─── метры объекта: (кадр, число, единица, подпись) ─────────────────────────
FACTS = [
    ('d-134k', '134 000', 'м²', 'Общая площадь комплекса'),
    ('d-68k', '68 000', 'м²', 'Торговая площадь: половина общей'),
    ('d-2500', '2500', 'мест', 'Парковка у комплекса'),
]

# ─── вывески, показанные в ролике: (слаг, подпись) ──────────────────────────
SIGNS = [
    ('s-front', 'Фасад: «Рив Гош», O`STIN, DNS'),
    ('s-lenta', '«Лента»'),
    ('s-kinomax', '«Киномакс» и IMAX'),
    ('s-dns', 'DNS «Гипер»'),
    ('s-domovoy', '«Домовой»'),
    ('s-gloria', 'Gloria Jeans'),
    ('s-ostin', 'O`STIN'),
    ('s-monki', 'Monki'),
    ('s-familia', 'Familia'),
    ('s-funday', 'FUNDAY и «Котофей»'),
    ('s-kolyaski', '«Купи-коляску.ру»'),
    ('s-leto', 'Фитнес-клуб «Лето»'),
    ('s-kari', 'kari'),
]

# магазины, открывшиеся к съёмке: в ролике они идут отдельным блоком
NEWCOMERS = [
    ('n-ichef', 'I-CHEF', 'био-бистро в фуд-зоне'),
    ('n-zolla', 'Zolla', 'магазин одежды в галерее'),
    ('n-ruxara', 'Ruxara', 'магазин одежды у входной группы'),
]

# ─── как доехать: три маршрута из ролика ────────────────────────────────────
# (ключ, заголовок, число, единица, текст, кадр, цвет)
ROUTES = [
    ('mck', 'МЦК «Дубровка»', '10 000', 'человек в день',
     'Плашка в ролике называет пассажиропоток выхода из МЦК «Дубровка». '
     'От платформы к комплексу ведёт крытый переход: эскалатор, галерея, '
     'вход прямо в торговый центр, на улицу выходить не нужно.',
     'd-mck', '#DF114A'),
    ('shuttle', 'Фирменные маршрутки', '5', 'станций метро',
     'Фирменные маршрутки «Мозаики» связывают комплекс с пятью станциями: «Автозаводская», '
     '«Кожуховская», «Дубровка», «Коломенская», «Пролетарская». Список снят '
     'с вывески остановки в кадре.',
     't-shuttle', '#2CD8B0'),
    ('ttk', 'Третье транспортное', '2', 'стороны съезда',
     'Комплекс стоит вплотную к ТТК, съезды сделаны и с внешней, и с '
     'внутренней стороны кольца. В ролике это показано отдельной 3D-картой '
     'с подписями улиц и развязок.',
     'd-map3d', '#E99614'),
]

# ─── что мы сделали ─────────────────────────────────────────────────────────
CRAFT = [
    ('Съёмка с воздуха',
     'Комплекс и район сверху: кровля с парковкой, ТТК, железная дорога, '
     'эстакады и жилые кварталы вокруг.'),
    ('Съёмка внутри',
     'Атриум, галереи, эскалаторы и входные группы в обычный рабочий день, '
     'без перекрытий и постановки.'),
    ('Тринадцать синхронов',
     'Каждого снимали на его месте: у касс гипермаркета, в фойе кинотеатра, '
     'среди колясок, в зале фитнес-клуба, у стойки бистро.'),
    ('Экранная графика',
     'Плашки с метражом и парковкой, график заполняемости, 3D-карта подъездов '
     'с подписями улиц и съездов.'),
    ('Монтаж 4:31',
     'Сборка от знака до знака: объект, цифры, арендаторы, доступность, люди. '
     'Хронометраж под показ в зале, а не под ленту в соцсетях.'),
]


def mmss(sec):
    sec = int(sec)
    return f'{sec // 60}:{sec % 60:02d}'


def part_of(sec):
    """Часть фильма, которой принадлежит секунда."""
    for i, (_k, _l, a, b, _c, _d) in enumerate(PARTS):
        if a <= sec < b:
            return i
    return len(PARTS) - 1


CSS = """<style>
:root{
 --or:#E99614;      /* оранжевый фон заставки, снят пипеткой */
 --mag:#DF114A;     /* маджента букв знака */
 --tur:#2CD8B0;     /* бирюза букв знака */
 --nav:#0C1557;     /* тёмно-синий за буквами */
 --ink:#14171C;
 --paper:#FFFFFF;
 --sand:#FBF4E9;    /* оранжевый, разведённый до бумаги */
 --line:rgba(20,23,28,.12);
 --mut:#6E6A66;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);
 font:400 17px/1.6 'Alegreya Sans',system-ui,sans-serif;overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
.mz{max-width:100%;overflow:hidden}
.mz h1,.mz h2,.mz h3,.mz .num,.mz .kick,.mz .tc{font-family:'Russo One',
 Impact,system-ui,sans-serif;font-weight:400}
.mz section{padding:clamp(52px,7.5vw,100px) 0}
.mz .in{width:min(1180px,92vw);margin:0 auto}
.mz .nar{width:min(760px,92vw);margin:0 auto}
.mz h2{font-size:clamp(27px,4.6vw,50px);line-height:1.02;margin:0 0 16px;
 letter-spacing:-.01em}
.mz h3{font-size:clamp(19px,2.3vw,25px);line-height:1.14;margin:0 0 8px}
.mz p{margin:0 0 14px}
.mz .lead{font-size:clamp(17px,1.9vw,21px);color:#3D3A36;max-width:66ch}
.mz .mut{color:var(--mut)}
.mz .kick{font-size:13px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--mag);margin:0 0 14px}
.mz .cap{font-size:14px;color:var(--mut);margin:8px 0 0}
.mz .sand{background:var(--sand)}
.mz a{color:inherit}
.mz-r{opacity:0;transform:translateY(18px);transition:opacity .5s,transform .5s}
.mz-r.is-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.mz-r{opacity:1;transform:none;transition:none}}

/* ── шапка кейса: оранжевый лист заставки ──────────────────────────────── */
.mz-hero{background:radial-gradient(120% 120% at 26% 12%,#F2A62B 0%,var(--or) 46%,#D07F0B 100%);
 color:#fff;padding:clamp(44px,6vw,72px) 0 clamp(44px,6vw,74px)}
.mz-hero__grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);
 gap:clamp(26px,4vw,52px);align-items:center}
.mz-hero__crumb{font-size:13px;letter-spacing:.16em;text-transform:uppercase;
 color:rgba(255,255,255,.78);margin:0 0 18px;font-family:'Russo One',system-ui,sans-serif}
.mz-hero__crumb a{color:inherit;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.4)}
.mz-hero h1{font-size:clamp(34px,6.6vw,74px);line-height:.98;margin:0 0 18px;
 letter-spacing:-.015em;text-shadow:0 4px 22px rgba(120,60,0,.22)}
.mz-hero h1 em{font-style:normal;color:var(--nav)}
.mz-hero .lead{color:rgba(255,255,255,.94);max-width:52ch}
.mz-hero__shot{border-radius:16px;overflow:hidden;box-shadow:0 26px 60px rgba(90,45,0,.34)}
.mz-hero__meta{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;
 margin-top:clamp(24px,3.4vw,36px)}
.mz-hero__meta div{background:rgba(12,21,87,.22);border:1px solid rgba(255,255,255,.26);
 border-radius:12px;padding:12px 14px}
.mz-hero__meta b{display:block;font-family:'Russo One',system-ui,sans-serif;
 font-size:clamp(18px,2.4vw,26px);line-height:1}
.mz-hero__meta span{display:block;font-size:13px;color:rgba(255,255,255,.82);margin-top:5px}

/* ── бриф ──────────────────────────────────────────────────────────────── */
.mz-brief{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
 gap:clamp(20px,3vw,36px);margin-top:30px}
.mz-brief__it b{display:block;width:38px;height:4px;background:var(--mag);margin:0 0 14px}
.mz-brief__it p{color:#413D39;margin:0}

/* ── контактный лист: главная механика ─────────────────────────────────── */
.mz-film{background:var(--nav);color:#fff}
.mz-film h2,.mz-film .lead{color:#fff}
.mz-film .lead{color:rgba(255,255,255,.84)}
.mz-film .kick{color:var(--tur)}
.mz-stage{margin:clamp(24px,3vw,34px) 0 18px}
@media(min-width:861px) and (min-height:620px){
 .mz-stage{position:sticky;top:12px;z-index:6}}
.mz-stage__in{display:grid;grid-template-columns:minmax(0,1fr) 260px;gap:18px;
 align-items:start}
.mz-stage video{width:100%;display:block;border-radius:14px;background:#000;
 box-shadow:0 20px 44px rgba(0,0,0,.42)}
.mz-side{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);
 border-radius:14px;padding:14px;min-height:184px}
.mz-peek{width:100%;aspect-ratio:16/9;border-radius:9px;background-color:rgba(0,0,0,.4);
 background-image:url(%IMG%/strip.jpg);background-size:1600% 1700%;
 background-position:0 0;background-repeat:no-repeat}
.mz-side .tc{font-size:20px;margin:12px 0 4px;color:var(--tur)}
.mz-side .who{font-size:14px;color:rgba(255,255,255,.8);line-height:1.4}
.mz-legend{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 14px;padding:0;list-style:none}
.mz-legend button{display:inline-flex;align-items:center;gap:8px;cursor:pointer;
 background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);color:#fff;
 border-radius:99px;padding:7px 13px 7px 9px;font:500 14px/1 'Alegreya Sans',sans-serif;
 transition:background .18s,border-color .18s}
.mz-legend button:hover,.mz-legend button:focus-visible{background:rgba(255,255,255,.18)}
.mz-legend i{width:12px;height:12px;border-radius:3px;display:block;flex:none}
.mz-legend em{font-style:normal;color:rgba(255,255,255,.6);font-size:13px}
.mz-sheet{--cols:20;display:grid;grid-template-columns:repeat(var(--cols),1fr);
 gap:2px;overflow:hidden;border-radius:10px;background:rgba(0,0,0,.3);padding:2px}
.mz-t{position:relative;aspect-ratio:16/9;border:0;padding:0;cursor:pointer;
 background-image:url(%IMG%/strip.jpg);background-size:1600% 1700%;
 background-repeat:no-repeat;transition:transform .16s;transform-origin:center}
.mz-t::after{content:'';position:absolute;inset:0;background:var(--c);opacity:.72;
 transition:opacity .16s}
.mz-t:hover,.mz-t:focus-visible{transform:scale(2.2);z-index:5;outline:none;
 box-shadow:0 10px 26px rgba(0,0,0,.5)}
.mz-t:hover::after,.mz-t:focus-visible::after{opacity:0}
.mz-t.is-now{z-index:4}
.mz-t.is-now::after{opacity:.1}
.mz-t.is-now::before{content:'';position:absolute;inset:0;z-index:2;
 box-shadow:inset 0 0 0 2px #fff}
.mz-sheet.is-dim .mz-t.is-off::after{opacity:.9;background:#0C1557}
.mz-note{margin:14px 0 0;font-size:15px;color:rgba(255,255,255,.72);min-height:3em}
.mz-note b{color:#fff}
@media(max-width:1023px){.mz-sheet{--cols:16}}
@media(max-width:860px){
 .mz-stage__in{grid-template-columns:1fr}
 .mz-side{display:flex;gap:14px;min-height:0;align-items:center}
 .mz-peek{width:132px;flex:none}
 .mz-side .tc{margin:0 0 4px}
}
@media(max-width:640px){.mz-sheet{--cols:12}.mz-t:hover{transform:scale(2.6)}}
@media(max-width:400px){.mz-sheet{--cols:10}}

/* ── график заполняемости ──────────────────────────────────────────────── */
.mz-gla{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);
 gap:clamp(24px,3.6vw,46px);align-items:center;margin-top:28px}
.mz-chart{background:#fff;border:1px solid var(--line);border-radius:16px;
 padding:clamp(16px,2.4vw,26px);box-shadow:0 14px 40px rgba(20,23,28,.07)}
.mz-chart svg{width:100%;height:auto;display:block}
/* кегли в SVG заданы в единицах viewBox (1000 в ширину): на десктопе карточка
   ужимается примерно вдвое, поэтому цифры вдвое крупнее «экранных» */
.mz-chart .gl{stroke:rgba(20,23,28,.16);stroke-width:1.5;stroke-dasharray:5 6}
.mz-chart .ax{stroke:var(--ink);stroke-width:3}
.mz-chart .lb{font:500 26px 'Alegreya Sans',sans-serif;fill:var(--mut)}
.mz-chart .curve{fill:none;stroke:var(--mag);stroke-width:7;stroke-linecap:round;
 stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset 1.9s ease-out}
.mz-chart.is-in .curve{stroke-dashoffset:0}
.mz-chart .dot{fill:var(--mag)}
.mz-chart .val{font-family:'Russo One',system-ui,sans-serif;fill:var(--ink);font-size:40px}
.mz-chart .cap{font:500 24px 'Alegreya Sans',sans-serif;fill:var(--mut)}
.mz-traffic{list-style:none;margin:26px 0 0;padding:0;border-top:1px solid var(--line)}
.mz-traffic li{display:flex;align-items:baseline;justify-content:space-between;gap:16px;
 padding:14px 0;border-bottom:1px solid var(--line)}
.mz-traffic .num{font-size:clamp(22px,3vw,32px);line-height:1;color:var(--nav)}
.mz-traffic span{font-size:15px;color:var(--mut)}

/* ── метры ─────────────────────────────────────────────────────────────── */
.mz-facts{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);
 gap:clamp(24px,4vw,54px);align-items:center;margin-top:30px}
.mz-sq{width:100%;max-width:320px}
.mz-sq svg{width:100%;height:auto;display:block}
.mz-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}
.mz-card{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}
.mz-card img{width:100%}
.mz-card__b{padding:14px 16px 16px}
.mz-card .num{font-size:clamp(24px,3.2vw,34px);line-height:1;color:var(--nav)}
.mz-card .num i{font-style:normal;font-size:.5em;color:var(--mut);margin-left:5px}
.mz-card p{margin:6px 0 0;font-size:15px;color:var(--mut)}

/* ── стена синхронов ───────────────────────────────────────────────────── */
.mz-people{background:var(--sand)}
.mz-wall{display:grid;grid-template-columns:repeat(auto-fill,minmax(184px,1fr));
 gap:clamp(12px,1.6vw,18px);margin-top:30px}
.mz-p{position:relative;display:block;width:100%;padding:0;border:0;cursor:pointer;
 background:#fff;border-radius:14px;overflow:hidden;text-align:left;
 box-shadow:0 6px 20px rgba(20,23,28,.08);transition:transform .18s,box-shadow .18s}
.mz-p:hover,.mz-p:focus-visible{transform:translateY(-4px);outline:none;
 box-shadow:0 16px 34px rgba(20,23,28,.16)}
.mz-p img{width:100%;aspect-ratio:1;object-fit:cover}
/* внутри <button> живут только span-ы: <p> там невалиден, поэтому блочность
   расставлена руками, иначе имя и должность слипаются в одну строку */
.mz-p__b{display:block;padding:12px 13px 14px}
.mz-p__n{display:block;font-family:'Russo One',system-ui,sans-serif;font-size:16px;
 line-height:1.15;margin:0 0 5px}
.mz-p__r{display:block;font-size:13.5px;line-height:1.35;color:var(--mut);margin:0}
.mz-p__r b{color:var(--ink);font-weight:700}
.mz-p__t{position:absolute;left:9px;top:9px;background:rgba(12,21,87,.86);color:#fff;
 font-family:'Russo One',system-ui,sans-serif;font-size:12px;border-radius:99px;
 padding:5px 9px}
.mz-p.is-now{box-shadow:0 0 0 3px var(--mag),0 16px 34px rgba(20,23,28,.16)}

/* ── вывески ───────────────────────────────────────────────────────────── */
.mz-signs{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));
 gap:12px;margin-top:28px}
.mz-signs figure{margin:0;border-radius:12px;overflow:hidden;border:1px solid var(--line)}
.mz-signs figcaption{padding:9px 12px 11px;font-size:14px;color:var(--mut);background:#fff}
.mz-new{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
 gap:16px;margin-top:26px}
.mz-new figure{margin:0}
.mz-new img{border-radius:12px}
.mz-new figcaption{margin-top:9px;font-size:15px}
.mz-new b{font-family:'Russo One',system-ui,sans-serif;font-weight:400}

/* ── маршруты ──────────────────────────────────────────────────────────── */
.mz-routes{display:grid;gap:clamp(16px,2.4vw,26px);margin-top:30px}
.mz-route{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);
 gap:clamp(18px,3vw,34px);align-items:center;border-top:3px solid var(--c);
 padding-top:clamp(16px,2.2vw,24px)}
.mz-route:nth-child(even){grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)}
.mz-route:nth-child(even) .mz-route__t{order:2}
.mz-route img{border-radius:14px}
.mz-route .num{font-size:clamp(34px,5.4vw,58px);line-height:1;color:var(--c)}
.mz-route .num i{font-style:normal;font-size:.34em;color:var(--mut);margin-left:8px;
 font-family:'Alegreya Sans',sans-serif;font-weight:700}
.mz-route h3{margin:10px 0 8px}
.mz-route p{margin:0;color:#413D39}

/* ── показ в зале ──────────────────────────────────────────────────────── */
.mz-screen{background:var(--nav);color:#fff}
.mz-screen h2{color:#fff}
.mz-screen__grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);
 gap:clamp(24px,4vw,48px);align-items:center}
.mz-screen img{border-radius:14px}
.mz-screen p{color:rgba(255,255,255,.84)}
.mz-screen .go{display:inline-block;margin-top:8px;background:var(--or);color:#14171C;
 font-family:'Russo One',system-ui,sans-serif;text-decoration:none;border-radius:99px;
 padding:14px 26px;transition:transform .16s}
.mz-screen .go:hover{transform:translateY(-2px)}

/* ── что сделали ───────────────────────────────────────────────────────── */
.mz-craft{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
 gap:clamp(18px,2.6vw,30px);margin-top:30px;counter-reset:c}
.mz-craft__it{counter-increment:c}
.mz-craft__it:before{content:counter(c,decimal-leading-zero);display:block;
 font-family:'Russo One',system-ui,sans-serif;font-size:26px;color:var(--tur);
 margin-bottom:8px}
.mz-craft__it p{margin:0;color:#413D39}

@media(max-width:860px){
 .mz-hero__grid,.mz-gla,.mz-facts,.mz-route,.mz-route:nth-child(even),
 .mz-screen__grid{grid-template-columns:1fr}
 .mz-route:nth-child(even) .mz-route__t{order:0}
 .mz-hero__meta{grid-template-columns:repeat(2,minmax(0,1fr))}
 .mz-sq{max-width:260px;margin:0 auto}
}
@media(max-height:520px){.mz-stage{position:static}}
</style>"""


def hero():
    return (
      '<header class="mz-hero"><div class="in"><div class="mz-hero__grid">'
      '<div>'
      '<p class="mz-hero__crumb"><a href="/project/">Проекты</a> · '
      '<a href="/videoproduction/">Видеопродакшн</a> · ТРЦ «Мозаика»</p>'
      '<h1>Ролик ТРЦ<br><em>«Мозаика»</em></h1>'
      '<p class="lead">Презентационный фильм о комплексе на 134 000 м² '
      'у метро «Дубровка»: съёмка с воздуха и в галереях, цифры объекта '
      'экранной графикой и тринадцать человек в кадре: арендаторы и руководители '
      'комплекса. Четыре с половиной минуты, снятые осенью 2018 года.</p>'
      '<div class="mz-hero__meta">'
      '<div><b>4:31</b><span>хронометраж</span></div>'
      '<div><b>13</b><span>синхронов</span></div>'
      '<div><b>134 000</b><span>м² комплекса</span></div>'
      '<div><b>271</b><span>кадр на листе</span></div>'
      '</div></div>'
      f'<div class="mz-hero__shot"><img src="{IMG}/logo.jpg" width="1280" height="720" '
      'alt="Заставка ролика: знак «Мозаики» из цветных плашек и рукописное '
      '«Делай интересно»" fetchpriority="high"></div>'
      '</div></div></header>')


def brief():
    return (
      '<section><div class="in">'
      '<p class="kick">Задача</p>'
      '<h2>Показать перемены в комплексе<br>и дать слово арендаторам</h2>'
      '<p class="lead">ТРЦ «Мозаика» — крупный торгово-развлекательный центр '
      'в Москве недалеко от метро «Дубровка», «Автозаводская» и «Кожуховская». '
      'К 2018 году центр заметно изменился, и это нужно было показать одним '
      'фильмом: что уже открылось, что открывается, и как на это смотрят те, '
      'кто уже работает внутри.</p>'
      '<div class="mz-brief">'
      '<div class="mz-brief__it mz-r"><b></b><h3>Снять изменения</h3>'
      '<p>Ролик должен был показать перемены, которые в комплексе уже '
      'произошли, и те, что были впереди: новые магазины, метры, парковку, '
      'транспортную доступность.</p></div>'
      '<div class="mz-brief__it mz-r"><b></b><h3>Записать арендаторов</h3>'
      '<p>Вторая часть задачи — интервью с действующими арендаторами. '
      'Не отзывы «на бумаге», а живые синхроны на камеру, снятые прямо '
      'в их магазинах и залах.</p></div>'
      '<div class="mz-brief__it mz-r"><b></b><h3>Собрать для зала</h3>'
      '<p>Фильм делался под показ на большом экране перед арендаторами, '
      'поэтому он длинный по меркам рекламы и построен как доклад: объект, '
      'цифры, люди.</p></div>'
      '</div></div></section>')


def sheet():
    """271 плитка контактного листа: цвет по частям фильма, клик — перемотка."""
    legend = ''.join(
      f'<li><button type="button" data-part="{i}" data-start="{a}">'
      f'<i style="background:{c}"></i>{label}<em>{mmss(a)}</em></button></li>'
      for i, (_k, label, a, _b, c, _d) in enumerate(PARTS))

    tiles = []
    for i in range(TILES):
        p = part_of(i + 0.5)
        col, row = i % SHEET_COLS, i // SHEET_COLS
        bx = col / (SHEET_COLS - 1) * 100
        by = row / (SHEET_ROWS - 1) * 100
        tiles.append(
          f'<button type="button" class="mz-t" data-s="{i}" data-p="{p}" '
          f'style="--c:{PARTS[p][4]};background-position:{bx:.4f}% {by:.4f}%" '
          f'aria-label="Секунда {mmss(i)}, часть «{PARTS[p][1]}»"></button>')

    return (
      '<section class="mz-film" id="film"><div class="in">'
      '<p class="kick">Как устроен ролик</p>'
      '<h2>Весь ролик одним листом</h2>'
      '<p class="lead">В ролике 271 секунда — и здесь 271 кадр, по одному '
      'на каждую. Плитки покрашены в четыре цвета знака «Мозаики» по частям '
      'фильма: так лист сразу показывает, из чего фильм собран. Наведите — '
      'краска сойдёт и останется кадр. Нажмите — плеер встанет на эту секунду. '
      'Пока ролик идёт, своя плитка подсвечивается сама.</p>'
      '<div class="mz-stage"><div class="mz-stage__in">'
      f'<video id="mz-v" controls playsinline preload="metadata" '
      f'poster="{IMG}/poster.jpg" width="1280" height="720">'
      f'<source src="{VIDEO}" type="video/mp4">'
      'Ваш браузер не умеет показывать видео.</video>'
      '<div class="mz-side">'
      '<div class="mz-peek" id="mz-peek" aria-hidden="true"></div>'
      '<div><p class="tc" id="mz-tc">0:00</p>'
      '<p class="who" id="mz-who">Заставка ролика</p></div>'
      '</div></div></div>'
      f'<ul class="mz-legend">{legend}</ul>'
      f'<div class="mz-sheet" id="mz-sheet">{"".join(tiles)}</div>'
      '<p class="mz-note" id="mz-note"><b>Знак.</b> ' + PARTS[0][5] + '</p>'
      '</div></section>')


def gla():
    """Кривая заполняемости, снятая с кадра ролика, живым SVG."""
    pts = MAP['gla']['points']
    lo, hi = 50.0, 78.0                      # рамка по оси Y с запасом под концы
    W, H = 1000.0, 470.0
    L, R, TOP, AX = 92.0, W - 24, 30.0, 376.0   # поля, верх поля и линия оси X

    def sx(x):
        return L + x * (R - L)

    def sy(v):
        return AX - (v - lo) / (hi - lo) * (AX - TOP)

    d = 'M' + ' L'.join(f'{sx(x):.1f} {sy(y):.1f}' for x, y in pts)
    grid = ''.join(
      f'<line class="gl" x1="{L:.0f}" y1="{sy(v):.1f}" x2="{R:.0f}" y2="{sy(v):.1f}"></line>'
      f'<text class="lb" x="{L - 14:.0f}" y="{sy(v) + 8:.1f}" text-anchor="end">{v} %</text>'
      for v in (55, 60, 65, 70, 75))
    first, last = pts[0], pts[-1]
    # подписи концов вынесены под ось: рядом с точками они наезжали на кривую
    svg = (
      f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
      'aria-label="График заполняемости: с 54 процентов в начале 2016 года '
      'до 75 процентов к весне 2018 года">'
      f'{grid}'
      f'<line class="ax" x1="{L:.0f}" y1="{AX:.0f}" x2="{R:.0f}" y2="{AX:.0f}"></line>'
      f'<path class="curve" pathLength="1" d="{d}"></path>'
      f'<circle class="dot" cx="{sx(first[0]):.1f}" cy="{sy(first[1]):.1f}" r="10"></circle>'
      f'<circle class="dot" cx="{sx(last[0]):.1f}" cy="{sy(last[1]):.1f}" r="10"></circle>'
      f'<text class="val" x="{L:.0f}" y="{AX + 48:.0f}">54 %</text>'
      f'<text class="cap" x="{L:.0f}" y="{AX + 78:.0f}">начало 2016</text>'
      f'<text class="val" x="{R:.0f}" y="{AX + 48:.0f}" text-anchor="end">75 %</text>'
      f'<text class="cap" x="{R:.0f}" y="{AX + 78:.0f}" text-anchor="end">весна 2018</text>'
      '</svg>')

    rows = ''.join(
      f'<li><span>{label}</span><b class="num">{val}</b></li>'
      for label, val, _n in TRAFFIC)

    return (
      '<section class="sand"><div class="in">'
      '<p class="kick">Цифры из ролика</p>'
      '<h2>Заполняемость выросла<br>на глазах у арендаторов</h2>'
      '<p class="lead">В ролике поверх съёмки висит график «Открытие магазинов '
      '2016-2018. GLA&nbsp;%». Мы сняли эту кривую прямо с кадра, по красным '
      'пикселям, и перерисовали её здесь живой: 54 % арендопригодной площади '
      'в начале 2016 года и 75 % к весне 2018-го. Ниже — посещаемость с той же '
      'экранной плашки.</p>'
      '<div class="mz-gla">'
      f'<div class="mz-chart mz-r">{svg}</div>'
      f'<div><ul class="mz-traffic">{rows}</ul>'
      f'<figure style="margin:26px 0 0"><img src="{IMG}/d-chart.jpg" '
      'width="1280" height="720" loading="lazy" alt="Кадр ролика: график '
      'открытия магазинов и посещаемость по годам поверх съёмки галереи">'
      '<figcaption class="cap">Так этот же график выглядит в ролике: '
      'кривая и три года посещаемости поверх съёмки фуд-зоны</figcaption>'
      '</figure></div>'
      '</div></div></section>')


def facts():
    """Метры объекта: 68 000 м² внутри 134 000 м² честной долей площади."""
    # сторона внутреннего квадрата = корень из доли, чтобы площади читались верно
    ratio = (68000 / 134000) ** 0.5
    side = 300 * ratio
    sq = (
      '<svg viewBox="0 0 300 300" role="img" aria-label="Квадрат общей площади '
      '134 000 м² и вписанный в него квадрат торговой площади 68 000 м², '
      'занимающий половину">'
      '<rect x="0" y="0" width="300" height="300" fill="#0C1557"></rect>'
      f'<rect x="0" y="{300 - side:.1f}" width="{side:.1f}" height="{side:.1f}" '
      'fill="#DF114A"></rect>'
      '<text x="290" y="26" text-anchor="end" fill="#fff" '
      'font-family="Russo One, system-ui, sans-serif" font-size="20">134 000 м²</text>'
      '<text x="290" y="48" text-anchor="end" fill="rgba(255,255,255,.7)" '
      'font-family="Alegreya Sans, sans-serif" font-size="15">общая</text>'
      f'<text x="12" y="{300 - side + 26:.1f}" fill="#fff" '
      'font-family="Russo One, system-ui, sans-serif" font-size="20">68 000 м²</text>'
      f'<text x="12" y="{300 - side + 48:.1f}" fill="rgba(255,255,255,.8)" '
      'font-family="Alegreya Sans, sans-serif" font-size="15">торговая</text>'
      '</svg>')

    cards = ''.join(
      f'<div class="mz-card mz-r"><img src="{IMG}/{slug}.jpg" width="1280" height="720" '
      f'loading="lazy" alt="Кадр ролика с плашкой «{num} {unit}»">'
      f'<div class="mz-card__b"><p class="num">{num}<i>{unit}</i></p>'
      f'<p>{cap}</p></div></div>'
      for slug, num, unit, cap in FACTS)

    return (
      '<section><div class="in">'
      '<p class="kick">Метры</p>'
      '<h2>Паспорт объекта плашками<br>поверх съёмки</h2>'
      '<p class="lead">Цифры в ролике не проговариваются диктором в пустоту: '
      'каждая плашка стоит поверх того, о чём говорит. Торговая площадь — '
      'над корпусом с воздуха, парковка — над самой парковкой.</p>'
      '<div class="mz-facts">'
      f'<div class="mz-sq mz-r">{sq}</div>'
      f'<div class="mz-cards">{cards}</div>'
      '</div></div></section>')


def people():
    """Стена синхронов: клик по карточке открывает отрезок спикера в плеере."""
    cards = ''.join(
      f'<button type="button" class="mz-p" data-start="{a}" data-end="{b}" '
      f'data-slug="{slug}" aria-label="Открыть синхрон: {name}, {role} {brand}">'
      f'<img src="{IMG}/p-{slug}.jpg" width="560" height="560" loading="lazy" '
      f'alt="{name}, {role} {brand}, кадр синхрона из ролика">'
      f'<span class="mz-p__t">{mmss(a)}</span>'
      f'<span class="mz-p__b"><span class="mz-p__n">{name}</span>'
      f'<span class="mz-p__r">{role}<br><b>{brand}</b></span></span></button>'
      for slug, name, role, brand, a, b in SPEAKERS)

    return (
      '<section class="mz-people" id="people"><div class="in">'
      '<p class="kick">Синхроны</p>'
      '<h2>Тринадцать человек,<br>снятых на своих местах</h2>'
      '<p class="lead">Каждого арендатора снимали там, где он работает: '
      'у касс гипермаркета, в фойе кинотеатра, среди колясок, в зале '
      'фитнес-клуба, у витрины бистро. Замыкают ролик управляющий и '
      'коммерческий директор комплекса. Нажмите на карточку — плеер откроет '
      'именно этот синхрон.</p>'
      f'<div class="mz-wall">{cards}</div>'
      '</div></section>')


def signs():
    figs = ''.join(
      f'<figure><img src="{IMG}/{slug}.jpg" width="1280" height="720" loading="lazy" '
      f'alt="Кадр ролика: {cap}"><figcaption>{cap}</figcaption></figure>'
      for slug, cap in SIGNS)
    new = ''.join(
      f'<figure><img src="{IMG}/{slug}.jpg" width="1280" height="720" loading="lazy" '
      f'alt="Кадр ролика: {name}, {cap}">'
      f'<figcaption><b>{name}</b> — {cap}</figcaption></figure>'
      for slug, name, cap in NEWCOMERS)
    return (
      '<section><div class="in">'
      '<p class="kick">Кто внутри</p>'
      '<h2>Вывески идут подряд,<br>как список без слов</h2>'
      '<p class="lead">Середина ролика построена на одном приёме: камера '
      'проходит по вывескам якорей одну за другой. Ни закадрового текста, '
      'ни подписей — только фасады и входы.</p>'
      f'<div class="mz-signs">{figs}</div>'
      '<h3 style="margin-top:clamp(34px,4vw,52px)">И отдельно — те, '
      'кто открылся к съёмке</h3>'
      f'<div class="mz-new">{new}</div>'
      '</div></section>')


def routes():
    items = ''.join(
      f'<div class="mz-route mz-r" style="--c:{color}">'
      f'<div class="mz-route__t"><p class="num">{num}<i>{unit}</i></p>'
      f'<h3>{title}</h3><p>{text}</p></div>'
      f'<div><img src="{IMG}/{shot}.jpg" width="1280" height="720" loading="lazy" '
      f'alt="Кадр ролика: {title}"></div></div>'
      for _k, title, num, unit, text, shot, color in ROUTES)
    return (
      '<section class="sand"><div class="in">'
      '<p class="kick">Доступность</p>'
      '<h2>Минута из четырёх с половиной —<br>про то, как сюда доехать</h2>'
      '<p class="lead">Для торгового центра это главный аргумент, поэтому '
      'в фильме он занимает целую часть: платформа МЦК и крытый переход, '
      'остановка фирменных маршруток, съезды с Третьего транспортного '
      'и 3D-карта подъездов с подписями улиц.</p>'
      f'<div class="mz-routes">{items}</div>'
      '<p class="cap" style="margin-top:22px">К этому в ролике добавлена '
      'плашка «парковка 2500 мест»: заезд с кровли и наземные площадки '
      'у входных групп.</p>'
      '</div></section>')


def screening():
    return (
      '<section class="mz-screen"><div class="in"><div class="mz-screen__grid">'
      '<div>'
      '<p class="kick" style="color:var(--tur)">Где его показали</p>'
      '<h2>Премьеру смотрели<br>в тёмном зале</h2>'
      '<p>Ролик сделали к вечеру для арендаторов «Мозаики», который мы же '
      'и придумали: 31 октября 2018 года, 134 гостя, зал в синем монохроме '
      'и знак комплекса, который собирали из лампочек сами гости.</p>'
      '<p>На фотографии с вечера на экране — 2:26 этого ролика, игровая зона '
      'комплекса. Тот самый кадр есть и на листе выше.</p>'
      '<a class="go" href="/event/mozaika/">Кейс вечера «Пора выходить на свет»</a>'
      '</div>'
      f'<div><img src="{EVENT_IMG}/video.jpg" width="1600" height="960" loading="lazy" '
      'alt="Зал на вечере арендаторов: на большом экране кадр из ролика '
      'с игровой зоной комплекса"></div>'
      '</div></div></section>')


def craft():
    items = ''.join(
      f'<div class="mz-craft__it mz-r"><h3>{t}</h3><p>{d}</p></div>'
      for t, d in CRAFT)
    return (
      '<section><div class="in">'
      '<p class="kick">Работа</p>'
      '<h2>Что мы сделали</h2>'
      f'<div class="mz-craft">{items}</div>'
      '</div></section>')


PAGE_JS = """<script>(function(){
 var PARTS=%PARTS%;
 var v=document.getElementById('mz-v'),sheet=document.getElementById('mz-sheet'),
     peek=document.getElementById('mz-peek'),tc=document.getElementById('mz-tc'),
     who=document.getElementById('mz-who'),note=document.getElementById('mz-note');
 if(!v||!sheet)return;
 var tiles=[].slice.call(sheet.querySelectorAll('.mz-t')),
     cards=[].slice.call(document.querySelectorAll('.mz-p')),
     COLS=16,ROWS=17,now=-1;

 function mmss(s){s=Math.max(0,Math.floor(s));return (s/60|0)+':'+('0'+(s%60)).slice(-2);}
 function partAt(s){for(var i=0;i<PARTS.length;i++)if(s>=PARTS[i].a&&s<PARTS[i].b)return i;
  return PARTS.length-1;}
 // спрайт: та же арифметика, что и в разметке плиток
 function peekAt(s){
  var c=s%COLS,r=(s/COLS|0);
  peek.style.backgroundPosition=(c/(COLS-1)*100).toFixed(4)+'% '+(r/(ROWS-1)*100).toFixed(4)+'%';
 }
 function say(s){
  var p=PARTS[partAt(s)];
  tc.textContent=mmss(s);who.textContent=p.l;peekAt(s);
 }
 function tell(i){
  var p=PARTS[i];
  note.innerHTML='<b>'+p.l+'.</b> '+p.d;
 }
 function seek(s,play){
  // до загрузки метаданных currentTime молча игнорируется — ждём событие
  function go(){v.currentTime=Math.min(s,(v.duration||1e5)-.2);
   if(play!==false){var q=v.play();if(q&&q.catch)q.catch(function(){});}}
  if(v.readyState>0)go();
  else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}
  say(s);
 }
 function inView(el){
  var r=el.getBoundingClientRect();
  return r.top>-40&&r.bottom<innerHeight+40;
 }

 // ── лист: наведение показывает кадр, клик перематывает ──────────────────
 sheet.addEventListener('mouseover',function(e){
  var t=e.target.closest('.mz-t');if(!t)return;
  say(+t.dataset.s);tell(+t.dataset.p);
 });
 sheet.addEventListener('focusin',function(e){
  var t=e.target.closest('.mz-t');if(!t)return;
  say(+t.dataset.s);tell(+t.dataset.p);
 });
 sheet.addEventListener('click',function(e){
  var t=e.target.closest('.mz-t');if(!t)return;
  var s=+t.dataset.s;tell(+t.dataset.p);seek(s,true);
  if(!inView(v))v.scrollIntoView({block:'center',behavior:'smooth'});
 });

 // ── легенда: клик открывает часть, наведение гасит остальные ────────────
 var legend=document.querySelector('.mz-legend');
 if(legend){
  legend.addEventListener('click',function(e){
   var b=e.target.closest('button');if(!b)return;
   var i=+b.dataset.part;tell(i);seek(+b.dataset.start,true);
   if(!inView(v))v.scrollIntoView({block:'center',behavior:'smooth'});
  });
  legend.addEventListener('mouseover',function(e){
   var b=e.target.closest('button');if(!b)return;
   var i=b.dataset.part;sheet.classList.add('is-dim');
   tiles.forEach(function(t){t.classList.toggle('is-off',t.dataset.p!==i);});
   tell(+i);
  });
  legend.addEventListener('mouseleave',function(){
   sheet.classList.remove('is-dim');
   tiles.forEach(function(t){t.classList.remove('is-off');});
  });
 }

 // ── карточки синхронов ──────────────────────────────────────────────────
 cards.forEach(function(c){
  c.addEventListener('click',function(){
   seek(+c.dataset.start,true);
   v.scrollIntoView({block:'center',behavior:'smooth'});
  });
 });

 // ── плеер ведёт лист: подсвечена плитка текущей секунды ─────────────────
 v.addEventListener('timeupdate',function(){
  var s=Math.floor(v.currentTime);
  if(s===now)return;
  if(tiles[now])tiles[now].classList.remove('is-now');
  now=s;
  if(tiles[now])tiles[now].classList.add('is-now');
  say(s);
  var p=partAt(s);
  cards.forEach(function(c){
   c.classList.toggle('is-now',s>=+c.dataset.start&&s<+c.dataset.end);
  });
  if(v.dataset.part!==''+p){v.dataset.part=p;tell(p);}
 });

 // ── появление блоков: свип по скроллу, а не IntersectionObserver.
 // Наблюдатель отдаёт колбэк на следующем кадре, и при быстрой прокрутке
 // нижние блоки остаются с opacity:0. Свип считает геометрию синхронно.
 var els=[].slice.call(document.querySelectorAll('.mz-r,.mz-chart'));
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

TITLE = 'Ролик ТРЦ «Мозаика»: презентационный фильм о комплексе | Hand Marketing'
DESCR = ('Кейс Hand Marketing: презентационный ролик ТРЦ «Мозаика» на 4:31. '
         'Съёмка с воздуха и в галереях, экранная инфографика по цифрам '
         'объекта, 3D-карта подъездов и 13 синхронов с арендаторами. '
         'Весь ролик разложен на 271 кадр прямо на странице.')

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Видеопродакшн","item":"https://hand-marketing.ru/videoproduction/"},'
  '{"@type":"ListItem","position":3,"name":"Ролик ТРЦ «Мозаика»",'
  f'"item":"{URL}"}}]}}</script>')

VIDEO_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"VideoObject",'
  '"name":"Презентационный ролик ТРЦ «Мозаика»",'
  '"description":"Презентационный фильм Hand Marketing о ТРЦ «Мозаика»: комплекс '
  'с воздуха и изнутри, цифры объекта экранной графикой, транспортная доступность '
  'и 13 синхронов с арендаторами.",'
  f'"thumbnailUrl":"https://hand-marketing.ru{IMG}/poster.jpg",'
  '"uploadDate":"2018-10-31","duration":"PT4M31S",'
  f'"contentUrl":"https://hand-marketing.ru{VIDEO}",'
  '"publisher":{"@type":"Organization","name":"Hand Marketing"}}</script>')

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
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/logo.jpg">'
        '<link rel="stylesheet" href="/fonts/russo-alegreya.css">'
        + rc.FONT + rc.CSS + CSS.replace('%IMG%', IMG) + METRIKA + '</head><body>')


def page():
    parts = [{'l': label, 'a': a, 'b': b, 'd': d}
             for _k, label, a, b, _c, d in PARTS]
    js = PAGE_JS.replace('%PARTS%', json.dumps(parts, ensure_ascii=False))
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="mz">{hero()}{brief()}{sheet()}{gla()}'
            f'{facts()}{people()}{signs()}{routes()}{screening()}{craft()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}{VIDEO_LD}'
            '</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'mozaika')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
