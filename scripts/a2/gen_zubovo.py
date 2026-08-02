#!/usr/bin/env python3
"""Генерит mirror/zubovo/index.html — кейс «Презентационный фильм технопарка „Зубово"».

Что было: индустриальный шаблон build-technopark.py (общий с BEKOBOD) — светлая
страница с чертёжной сеткой, пересказ ролика текстом и три абстрактных «ключевых
блока». Ни одной цифры из самого фильма на странице не было.

Дизайн-концепция: фильм — это презентация площадки инвестору, поэтому страница
собрана как её паспорт и работает пультом к фильму.

  • фирменная графика технопарка — соты; паспорт площадки набран сотовым
    «цветком» в SVG: центр — общая площадь, шесть ячеек вокруг — мощности
    инженерии и площади АБК, все цифры сняты с инфографики ролика;
  • земельный баланс 25,8 / 44 / 30,2 нарисован живым доном, сегменты
    подсвечиваются с легендой и перематывают плеер на этот эпизод;
  • под плеером — шкала фильма: 14 глав пропорциональными сегментами,
    заливка идёт за воспроизведением, клик по сегменту перематывает;
  • любая карточка (инженерия, логистика, синхроны, АБК) — кнопка перемотки:
    страница не пересказывает фильм, а водит по нему;
  • картинки — кадры самого ролика (scripts/zubovo-assets.py), своей съёмки по
    проекту нет.

Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import math
import os
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

URL = 'https://hand-marketing.ru/zubovo/'
IMG = '/images/zubovo'
VIDEO = '/portfolio/zubovo/brand-video.mp4'  # тот же файл, что /media/technopark-zubovo.mp4,
# но лежит внутри mirror: работает и в локальном превью, и на бою
DUR = 184  # 3:04


# ─── главы фильма (секунда, имя, подпись) ───────────────────────────────────
CHAPTERS = [
    (0,   'Открытие',      'Знак и слоган'),
    (10,  'Регион',        'Башкортостан'),
    (31,  'Логистика',     'Аэропорт, ЖД, порт'),
    (36,  'Облёт',         'Территория с высоты'),
    (47,  'Инженерия',     'Вода, ток, тепло'),
    (58,  'Масштаб',       'Более 70 гектаров'),
    (66,  'Производства',  'Цеха резидентов'),
    (73,  'Земля',         'Баланс участков'),
    (80,  'Условия',       'Что получает резидент'),
    (95,  'Корпуса',       'Здания в работе'),
    (106, 'Участки',       'Оборудование и стенды'),
    (118, 'Синхрон',       'Роман Зубов'),
    (132, 'Развитие',      'Стройка и АБК'),
    (147, 'Синхрон',       'Ильдус Самигуллин'),
]

# ─── паспорт площадки: сотовый «цветок», цифры с инфографики ролика ─────────
# позиция, число, подпись (до трёх строк), секунда эпизода
HEX = [
    ('c',  '70+',   ['гектаров', 'общая площадь'],                      58),
    ('t',  '580',   ['м³ в сутки', 'водозабор'],                        51),
    ('ur', '10',    ['МВт', 'подстанция'],                              51),
    ('lr', '40,5',  ['МВт', 'котельная'],                               53),
    ('b',  '30,2%', ['свободных', 'участков'],                          75),
    ('ll', '178',   ['м²', 'конференц-залы'],                          144),
    ('ul', '1735',  ['м²', 'офисных помещений'],                       144),
]

# ─── земельный баланс ───────────────────────────────────────────────────────
LAND = [
    (25.8, '#2E9E9A', 'Заняты резидентами', 'участки действующих производств'),
    (44.0, '#43A83A', 'Зарезервированы',    'подписаны и ждут резидента'),
    (30.2, '#F07C1E', 'Свободны',           'можно заходить с новым проектом'),
]

# ─── что получает резидент (из инфографики ролика) ──────────────────────────
TERMS = [
    ('key',  'Готовые помещения «под ключ»',
     'Корпуса уже построены: заходите в готовое здание, а не в чистое поле.'),
    ('net',  'Подключение к инженерным сетям',
     'Вода, тепло и электричество на площадке заведены, мощности свободны.'),
    ('adm',  'Персонал в административно-бытовом корпусе',
     'Офисы и конференц-залы АБК снимают вопрос «где посадить людей».'),
]

# ─── кадры площадки в работе ────────────────────────────────────────────────
WORK = [
    ('res-1',  96, 'Готовые корпуса резидентов вдоль внутреннего проезда'),
    ('res-2', 100, 'Административная часть корпуса: офис прямо на производстве'),
    ('prod-2', 108, 'Склад трубной продукции резидента'),
    ('prod-3', 112, 'Оператор за испытательным стендом'),
    ('prod-4', 116, 'Опрессовка модулей внутренним давлением'),
    ('prod-1', 69, 'Сварочный пост на производстве резидента'),
    ('res-4', 165, 'Освоенная часть площадки с высоты'),
]

# ─── синхроны ───────────────────────────────────────────────────────────────
VOICES = [
    ('sp-1', 118, 'Роман Николаевич Зубов',
     'начальник Управления строительством объектов недвижимости',
     'О стройке новых корпусов и о том, что площадка растёт дальше.'),
    ('sp-2', 147, 'Ильдус Зуфарович Самигуллин',
     'начальник производственного участка технопарка Зубово',
     'О работе производственного участка изнутри площадки.'),
]

# ─── развитие ───────────────────────────────────────────────────────────────
DEV = [
    ('dev-1', 133, 'Пятна застройки под новые корпуса'),
    ('dev-2', 137, 'Бетонные работы в новом производственном корпусе'),
    ('dev-3', 142, 'Каркас административно-бытового корпуса'),
]

LOGI = [
    ('Аэропорт', 32),
    ('ЖД-станция', 33),
    ('Речной порт', 34),
    ('Уфа', 31),
]


def mmss(sec):
    return f'{sec // 60}:{sec % 60:02d}'


# ─── CSS ────────────────────────────────────────────────────────────────────
PAGE_CSS = """<style id="zb-css">
.zb{
 --ink:#0A0C0F;--ink2:#101419;--ink3:#171C23;--ink4:#1F262F;
 --line:rgba(255,255,255,.09);--line2:rgba(255,255,255,.17);
 --tx:#9BA6B2;--hi:#F3F6F9;--dim:#6B7683;
 --or:#F07C1E;--or2:#FFB25E;--red:#E11B22;--teal:#2E9E9A;--grn:#43A83A;
 --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
 --e:cubic-bezier(.16,1,.3,1);
 background:var(--ink);color:var(--tx);
 font-family:'Onest',-apple-system,BlinkMacSystemFont,Arial,sans-serif;
 font-size:17px;line-height:1.62;-webkit-font-smoothing:antialiased;overflow-x:clip}
.zb *{box-sizing:border-box}
.zb ::selection{background:var(--or);color:#0A0A0A}
/* height:auto обязателен: атрибут height у <img> иначе перебивает aspect-ratio */
.zb img{max-width:100%;display:block;height:auto}
.zb h1,.zb h2,.zb h3,.zb h4{font-family:'Geologica',Arial,sans-serif;color:var(--hi);
 letter-spacing:-.02em;margin:0;font-weight:700;line-height:1.05}
.zb p{margin:0 0 16px}
.zb__w{max-width:1180px;margin:0 auto;padding:0 28px}
@media(max-width:640px){.zb__w{padding:0 18px}}

/* соты — фирменная графика технопарка, работают фоном секций */
.zb__comb{position:absolute;inset:0;pointer-events:none;opacity:.5;
 background-image:
  radial-gradient(circle at 50% 50%,transparent 0,transparent 0),
  url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='97' viewBox='0 0 56 97'%3E%3Cpath d='M14 0 42 0 56 24.25 42 48.5 14 48.5 0 24.25Z M14 48.5 42 48.5 56 72.75 42 97 14 97 0 72.75Z' fill='none' stroke='%23ffffff' stroke-opacity='.07' stroke-width='1.2'/%3E%3C/svg%3E");
 background-size:56px 97px}

.zb__lab{display:flex;align-items:center;gap:13px;font-family:var(--mono);
 font-size:12px;letter-spacing:.13em;text-transform:uppercase;color:var(--dim);margin:0 0 22px}
.zb__lab::before{content:"";width:24px;height:3px;background:var(--or)}
.zb__lab b{color:var(--hi);font-weight:500}

/* ── ГЕРОЙ ── */
.zb__hero{position:relative;padding:92px 0 70px;isolation:isolate;overflow:hidden}
.zb__hero::before{content:"";position:absolute;inset:0;z-index:-2;
 background:#06080B url('""" + IMG + """/hero.jpg') center/cover no-repeat;
 opacity:.36;filter:grayscale(.3) contrast(1.05)}
.zb__hero::after{content:"";position:absolute;inset:0;z-index:-1;
 background:radial-gradient(105% 75% at 78% 0%,rgba(240,124,30,.22),transparent 60%),
 linear-gradient(180deg,rgba(10,12,15,.60) 0%,rgba(10,12,15,.88) 55%,var(--ink) 100%)}
.zb__kick{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:center;font-family:var(--mono);
 font-size:12px;letter-spacing:.11em;text-transform:uppercase;color:#C7D0DA;margin:0 0 26px}
.zb__kick span{border:1px solid var(--line2);border-radius:999px;padding:5px 12px}
.zb__kick span.hot{border-color:transparent;background:var(--or);color:#120A02;font-weight:600}
.zb h1{font-size:clamp(40px,8.6vw,90px);margin:0 0 6px}
.zb h1 em{font-style:normal;color:var(--or)}
.zb__slog{font-family:var(--mono);font-size:clamp(12px,3.2vw,14px);letter-spacing:.22em;
 text-transform:uppercase;color:var(--or2);margin:16px 0 0}
.zb__sub{font-size:clamp(17px,4.2vw,21px);color:#C7D0DA;max-width:620px;margin:20px 0 32px}
.zb__act{display:flex;flex-wrap:wrap;gap:13px;align-items:center}
.zb__btn{display:inline-flex;align-items:center;gap:11px;border:0;cursor:pointer;border-radius:999px;
 padding:15px 26px;background:var(--or);color:#120A02;white-space:nowrap;
 font:700 15px 'Geologica',Arial,sans-serif;transition:transform .2s var(--e),box-shadow .2s var(--e);
 box-shadow:0 14px 34px -14px rgba(240,124,30,.8)}
.zb__btn:hover{transform:translateY(-2px);box-shadow:0 20px 42px -14px rgba(240,124,30,.9)}
.zb__btn svg{width:15px;height:15px;fill:#120A02}
.zb__ghost{display:inline-flex;align-items:center;gap:9px;border:1px solid var(--line2);
 background:transparent;color:var(--hi);border-radius:999px;padding:14px 24px;cursor:pointer;
 white-space:nowrap;font:600 15px 'Geologica',Arial,sans-serif;text-decoration:none;transition:.2s var(--e)}
.zb__ghost:hover{border-color:var(--or);color:#fff}
.zb__facts{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);
 border:1px solid var(--line);margin:46px 0 0;max-width:780px}
@media(min-width:760px){.zb__facts{grid-template-columns:repeat(4,1fr)}}
.zb__facts div{background:rgba(10,13,18,.74);padding:15px 17px;backdrop-filter:blur(6px)}
.zb__facts dt{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--dim);margin:0 0 6px}
.zb__facts dd{margin:0;color:var(--hi);font-weight:600;font-size:15px;font-family:'Geologica',Arial,sans-serif}

/* ── секции ── */
.zb__s{padding:76px 0;border-top:1px solid var(--line);position:relative}
@media(max-width:640px){.zb__s{padding:52px 0}}
.zb__h2{font-size:clamp(27px,6vw,44px);margin:0 0 18px;max-width:17ch}
.zb__intro{max-width:660px;margin:0 0 34px}

/* ── ПЛЕЕР И ШКАЛА ФИЛЬМА ── */
.zb__film{position:relative;overflow:hidden;border:1px solid var(--line2);background:#000;
 box-shadow:0 44px 90px -48px rgba(0,0,0,.95)}
.zb__film video{width:100%;height:auto;aspect-ratio:16/9;display:block;background:#000}
.zb__rail{position:relative;display:flex;gap:2px;margin:16px 0 0;height:26px;
 background:var(--ink2);border:1px solid var(--line);padding:2px}
.zb__seg{position:relative;border:0;padding:0;cursor:pointer;background:var(--ink3);
 overflow:hidden;transition:background .2s var(--e)}
.zb__seg:hover{background:var(--ink4)}
.zb__seg i{position:absolute;inset:0;transform-origin:left center;transform:scaleX(0);
 background:linear-gradient(90deg,rgba(240,124,30,.55),var(--or));transition:transform .25s linear}
.zb__seg[aria-current="true"]{background:var(--ink4)}
.zb__rail-t{display:flex;justify-content:space-between;font-family:var(--mono);font-size:11px;
 color:var(--dim);margin-top:7px;letter-spacing:.05em}
.zb__rail-t b{color:var(--or2);font-weight:500}
.zb__chaps{display:flex;gap:8px;overflow-x:auto;padding:16px 0 4px;scrollbar-width:thin}
@media(min-width:1000px){.zb__chaps{flex-wrap:wrap;overflow:visible}}
.zb__chaps::-webkit-scrollbar{height:3px}
.zb__chaps::-webkit-scrollbar-thumb{background:var(--line2)}
.zb__chap{flex:0 0 auto;display:flex;flex-direction:column;align-items:flex-start;gap:1px;
 border:1px solid var(--line);background:var(--ink2);padding:9px 14px;cursor:pointer;text-align:left;
 color:var(--tx);font-family:inherit;transition:.2s var(--e)}
.zb__chap b{color:var(--hi);font:600 14px 'Geologica',Arial,sans-serif}
.zb__chap i{font-style:normal;font-family:var(--mono);font-size:11px;color:var(--dim)}
.zb__chap:hover{border-color:var(--line2);background:var(--ink3)}
.zb__chap[aria-current="true"]{border-color:var(--or);background:var(--ink3)}
.zb__chap[aria-current="true"] i{color:var(--or2)}

/* ── РЕГИОН И ЛОГИСТИКА ── */
.zb__geo{display:grid;gap:26px}
@media(min-width:940px){.zb__geo{grid-template-columns:1.25fr .9fr;gap:40px;align-items:start}}
.zb__frame{border:1px solid var(--line);background:#05080C;overflow:hidden}
.zb__frame img{width:100%}
.zb__frame figcaption{padding:11px 14px;font-family:var(--mono);font-size:11.5px;color:var(--dim);
 border-top:1px solid var(--line)}
.zb__frame{margin:0}
.zb__chips{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0}
.zb__chip{border:1px solid var(--line2);background:transparent;color:var(--hi);cursor:pointer;
 font:500 13px var(--mono);letter-spacing:.04em;padding:8px 14px;transition:.2s var(--e)}
.zb__chip:hover{border-color:var(--or);color:#fff;background:rgba(240,124,30,.1)}
.zb__quote{border-left:3px solid var(--or);padding:4px 0 4px 18px;margin:26px 0 0;
 font-family:'Geologica',Arial,sans-serif;color:var(--hi);font-size:clamp(17px,3.8vw,21px);line-height:1.35}
.zb__quote span{display:block;font-family:var(--mono);font-size:11.5px;color:var(--dim);
 letter-spacing:.08em;text-transform:uppercase;margin-top:10px;font-weight:400}

/* ── ПАСПОРТ: СОТЫ ── */
.zb__pass{display:grid;gap:30px;align-items:center}
@media(min-width:960px){.zb__pass{grid-template-columns:1.05fr .95fr;gap:48px}}
.zb__hexwrap{position:relative}
.zb__hex svg{width:100%;height:auto;overflow:visible}
.zb__cell{cursor:pointer}
.zb__cell polygon{fill:var(--ink2);stroke:var(--line2);stroke-width:1.5;
 transition:fill .28s var(--e),stroke .28s var(--e)}
.zb__cell .num{fill:var(--hi);font-family:'Geologica',Arial,sans-serif;font-weight:700;
 font-size:40px;text-anchor:middle;letter-spacing:-.02em}
.zb__cell .cap{fill:#8A95A2;font-family:var(--mono);font-size:13px;text-anchor:middle}
.zb__cell:hover polygon,.zb__cell:focus-visible polygon{fill:#1C232C;stroke:var(--or)}
.zb__cell:hover .num{fill:var(--or2)}
.zb__cell.is-c polygon{fill:#17202A;stroke:var(--or)}
.zb__cell.is-c .num{fill:var(--or);font-size:52px}
.zb__pass-t li{list-style:none;position:relative;padding:13px 0 13px 22px;border-bottom:1px solid var(--line);
 font-size:15.5px}
.zb__pass-t{margin:0;padding:0;border-top:1px solid var(--line)}
.zb__pass-t li::before{content:"";position:absolute;left:0;top:22px;width:10px;height:3px;background:var(--or)}
.zb__pass-t b{color:var(--hi);font-family:'Geologica',Arial,sans-serif;font-weight:600}

/* ── ЗЕМЕЛЬНЫЙ БАЛАНС ── */
.zb__land{display:grid;gap:30px;align-items:center}
@media(min-width:900px){.zb__land{grid-template-columns:300px 1fr;gap:44px}}
.zb__donut{position:relative;width:100%;max-width:300px;margin:0 auto}
.zb__donut svg{width:100%;height:auto;transform:rotate(-90deg)}
.zb__donut circle{fill:none;stroke-width:30;transition:stroke-dashoffset 1.1s var(--e),opacity .25s var(--e)}
.zb__donut .is-dim{opacity:.22}
.zb__donut-c{position:absolute;inset:0;display:grid;place-content:center;text-align:center}
.zb__donut-c b{display:block;font-family:'Geologica',Arial,sans-serif;font-weight:700;color:var(--hi);
 font-size:26px;line-height:1}
.zb__donut-c i{font-style:normal;font-family:var(--mono);font-size:11px;color:var(--dim);
 letter-spacing:.08em;text-transform:uppercase}
.zb__leg{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
.zb__leg button{display:grid;grid-template-columns:auto 92px 1fr;gap:16px;align-items:center;
 background:var(--ink2);border:0;cursor:pointer;padding:17px 20px;text-align:left;color:var(--tx);
 font-family:inherit;transition:background .2s var(--e)}
.zb__leg button:hover{background:var(--ink3)}
.zb__leg .sw{width:13px;height:13px;border-radius:50%}
.zb__leg .pc{font-family:'Geologica',Arial,sans-serif;font-weight:700;font-size:24px;color:var(--hi);
 letter-spacing:-.02em}
.zb__leg b{display:block;color:var(--hi);font:600 15px 'Geologica',Arial,sans-serif}
.zb__leg i{font-style:normal;font-size:13.5px;color:var(--dim)}
@media(max-width:520px){.zb__leg button{grid-template-columns:auto 74px 1fr;gap:12px;padding:14px 15px}
 .zb__leg .pc{font-size:20px}}

/* ── УСЛОВИЯ ── */
.zb__terms{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);margin-top:30px}
@media(min-width:820px){.zb__terms{grid-template-columns:repeat(3,1fr)}}
.zb__term{background:var(--ink2);padding:28px 24px}
.zb__term .ic{width:52px;height:58px;margin-bottom:18px;display:block}
.zb__term h3{font-size:19px;margin:0 0 9px}
.zb__term p{margin:0;font-size:14.5px;color:var(--dim)}
.zb__advimg{position:relative;border:1px solid var(--line);overflow:hidden}
.zb__advimg img{width:100%;aspect-ratio:21/9;object-fit:cover;filter:grayscale(.15)}

/* ── ПЛОЩАДКА В РАБОТЕ ── */
.zb__grid{display:grid;gap:13px}
@media(min-width:720px){.zb__grid{grid-template-columns:repeat(6,1fr)}
 .zb__grid button:nth-child(1){grid-column:span 4}
 .zb__grid button:nth-child(2){grid-column:span 2}
 .zb__grid button:nth-child(3){grid-column:span 2}
 .zb__grid button:nth-child(4){grid-column:span 2}
 .zb__grid button:nth-child(5){grid-column:span 2}
 .zb__grid button:nth-child(6){grid-column:span 3}
 .zb__grid button:nth-child(7){grid-column:span 3}}
.zb__tile{border:1px solid var(--line);background:var(--ink2);padding:0;cursor:pointer;
 text-align:left;color:inherit;font-family:inherit;overflow:hidden;display:flex;flex-direction:column;
 transition:.24s var(--e)}
.zb__tile img{width:100%;aspect-ratio:16/9;object-fit:cover;flex:1 1 auto;min-height:0;
 transition:transform .5s var(--e)}
.zb__tile span{display:flex;justify-content:space-between;gap:12px;padding:11px 14px;
 font-family:var(--mono);font-size:11.5px;color:var(--dim);line-height:1.4}
.zb__tile span em{font-style:normal;color:var(--or2);flex:0 0 auto}
.zb__tile:hover{border-color:var(--line2)}
.zb__tile:hover img{transform:scale(1.05)}

/* ── СИНХРОНЫ ── */
.zb__voices{display:grid;gap:14px}
@media(min-width:800px){.zb__voices{grid-template-columns:1fr 1fr}}
.zb__voice{border:1px solid var(--line);background:var(--ink2);padding:0;cursor:pointer;text-align:left;
 color:inherit;font-family:inherit;overflow:hidden;transition:.24s var(--e)}
.zb__voice img{width:100%;aspect-ratio:16/9;object-fit:cover;transition:transform .5s var(--e)}
.zb__voice div{padding:20px 22px 24px}
.zb__voice b{display:block;color:var(--hi);font:700 18px 'Geologica',Arial,sans-serif;margin-bottom:4px}
.zb__voice i{font-style:normal;display:block;font-family:var(--mono);font-size:11.5px;color:var(--or2);
 margin-bottom:12px;line-height:1.45}
.zb__voice p{margin:0;font-size:14.5px;color:var(--dim)}
.zb__voice:hover{border-color:var(--or)}
.zb__voice:hover img{transform:scale(1.04)}

/* ── РАЗВИТИЕ ── */
.zb__dev{display:grid;gap:13px}
@media(min-width:760px){.zb__dev{grid-template-columns:repeat(3,1fr)}}
.zb__abk{display:grid;gap:26px;margin-top:36px;align-items:center;border:1px solid var(--line);
 background:var(--ink2);padding:26px}
@media(min-width:880px){.zb__abk{grid-template-columns:1.2fr .8fr;gap:40px;padding:34px}}
.zb__abk img{width:100%;border:1px solid var(--line)}
.zb__abk h3{font-size:clamp(21px,4.4vw,28px);margin:0 0 14px}
.zb__nums{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);
 border:1px solid var(--line);margin-top:20px}
.zb__nums div{background:var(--ink3);padding:18px 20px}
.zb__nums b{display:block;font-family:'Geologica',Arial,sans-serif;font-weight:700;color:var(--or);
 font-size:clamp(24px,5vw,32px);line-height:1;letter-spacing:-.02em}
.zb__nums i{font-style:normal;display:block;margin-top:7px;font-family:var(--mono);font-size:11px;
 letter-spacing:.06em;text-transform:uppercase;color:var(--dim)}

/* ── ЗАДАЧА / РЕШЕНИЕ / РЕЗУЛЬТАТ ── */
.zb__story{display:grid;gap:0}
.zb__step{display:grid;gap:14px;padding:30px 0;border-top:1px solid var(--line)}
@media(min-width:840px){.zb__step{grid-template-columns:190px 1fr;gap:44px}}
.zb__step:first-child{border-top:0;padding-top:0}
.zb__num{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--or)}
.zb__step h3{font-size:clamp(20px,4.4vw,28px);margin:0 0 14px}
.zb__step ul{margin:16px 0 0;padding:0;list-style:none;border-top:1px solid var(--line)}
.zb__step li{position:relative;padding:11px 0 11px 22px;border-bottom:1px solid var(--line);font-size:15px}
.zb__step li::before{content:"";position:absolute;left:0;top:20px;width:10px;height:3px;background:var(--or)}

/* появление */
.zb .r{opacity:0;transform:translateY(22px);transition:opacity .8s var(--e),transform .8s var(--e)}
.zb .r.is-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
 .zb .r{opacity:1;transform:none;transition:none}
 .zb *{transition:none!important;animation:none!important}}
.zb :focus-visible{outline:2px solid var(--or);outline-offset:3px}
</style>"""


PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'


# ─── секции ─────────────────────────────────────────────────────────────────
def hero():
    facts = ''.join(f'<div><dt>{t}</dt><dd>{v}</dd></div>' for t, v in [
        ('Клиент', 'Технопарк «Зубово»'),
        ('Регион', 'Башкортостан, Уфа'),
        ('Формат', 'Презентационный фильм'),
        ('Хронометраж', '3:04'),
    ])
    return f'''<section class="zb__hero"><div class="zb__w">
<div class="zb__kick"><span>Уфа, Башкортостан</span><span>Видеопродакшн</span><span class="hot">Индустриальная площадка</span></div>
<h1>Технопарк<br><em>«Зубово»</em></h1>
<p class="zb__slog">Инновации. Технологии. Развитие.</p>
<p class="zb__sub">Презентационный фильм о живой промышленной площадке под Уфой:
готовые корпуса, заведённые мощности и свободные участки, на которые можно зайти
с новым производством.</p>
<div class="zb__act">
<button class="zb__btn" type="button" data-seek="0">{PLAY}Смотреть фильм</button>
<a class="zb__ghost" href="#passport">Паспорт площадки</a></div>
<dl class="zb__facts">{facts}</dl>
</div></section>'''


def film():
    total = float(DUR)
    segs, chips = '', ''
    for i, (s, n, c) in enumerate(CHAPTERS):
        end = CHAPTERS[i + 1][0] if i + 1 < len(CHAPTERS) else DUR
        w = (end - s) / total * 100
        segs += (f'<button class="zb__seg" type="button" style="flex:0 0 {w:.3f}%" '
                 f'data-seek="{s}" data-chap="{s}" aria-label="{n}, {mmss(s)}"><i></i></button>')
        chips += (f'<button class="zb__chap" type="button" data-seek="{s}" data-chap="{s}">'
                  f'<b>{n}</b><i>{mmss(s)} · {c}</i></button>')
    return f'''<section class="zb__s" id="film"><div class="zb__w">
<p class="zb__lab"><b>Фильм</b> · 3 минуты 4 секунды</p>
<div class="zb__film r"><video id="zb-video" controls preload="none" playsinline
 poster="{IMG}/poster.jpg" width="1280" height="720">
<source src="{VIDEO}" type="video/mp4">Ваш браузер не воспроизводит видео.</video></div>
<div class="zb__rail" role="group" aria-label="Главы фильма">{segs}</div>
<div class="zb__rail-t"><span id="zb-now"><b>Открытие</b> · Знак и слоган</span><span>3:04</span></div>
<div class="zb__chaps">{chips}</div>
</div></section>'''


def geo():
    chips = ''.join(f'<button class="zb__chip" type="button" data-seek="{s}">{n}</button>'
                    for n, s in LOGI)
    return f'''<section class="zb__s" id="geo"><div class="zb__w">
<p class="zb__lab"><b>01</b> · Где стоит площадка</p>
<h2 class="zb__h2">Рядом с Уфой, а не «где-то в области»</h2>
<p class="zb__intro">Фильм начинается с географии: сначала республика на карте страны,
затем спутниковый план окрестностей Уфы. На нём видно всё, что важно логисту:
аэропорт, железнодорожная станция, речной порт и сам город рядом с площадкой,
через которую проходит федеральная трасса.</p>
<div class="zb__geo">
<figure class="zb__frame r"><img src="{IMG}/logimap.jpg" width="1280" height="720" loading="lazy"
 alt="Кадр фильма: спутниковая карта с технопарком «Зубово», аэропортом, ЖД-станцией, речным портом и Уфой">
<figcaption>Кадр фильма, 0:33 · транспортная схема вокруг площадки</figcaption></figure>
<div class="r">
<figure class="zb__frame"><img src="{IMG}/reg.jpg" width="1000" height="562" loading="lazy"
 alt="Кадр фильма: Республика Башкортостан на карте европейской части России">
<figcaption>Кадр фильма, 0:13 · Башкортостан на карте страны</figcaption></figure>
<div class="zb__chips">{chips}</div>
<blockquote class="zb__quote">Башкортостан входит в топ-5 регионов страны по количеству
индустриальных и технопарков.<span>Тезис из фильма, 0:29</span></blockquote>
</div></div></div></section>'''


def _hexcell(pos, num, caps, sec, R=100.0):
    """Одна сота «цветка»: центр по позиции, внутри число и подпись."""
    dx, dy = {
        'c':  (0, 0),
        't':  (0, -math.sqrt(3) * R),
        'b':  (0,  math.sqrt(3) * R),
        'ul': (-1.5 * R, -math.sqrt(3) * R / 2),
        'll': (-1.5 * R,  math.sqrt(3) * R / 2),
        'ur': (1.5 * R, -math.sqrt(3) * R / 2),
        'lr': (1.5 * R,  math.sqrt(3) * R / 2),
    }[pos]
    pts = ' '.join(f'{dx + R * math.cos(math.radians(a)):.1f},{dy + R * math.sin(math.radians(a)):.1f}'
                   for a in (0, 60, 120, 180, 240, 300))
    cls = 'zb__cell is-c' if pos == 'c' else 'zb__cell'
    ny = dy - 6 - (len(caps) - 2) * 4
    lines = ''.join(f'<text class="cap" x="{dx:.1f}" y="{ny + 22 + i * 17:.1f}">{c}</text>'
                    for i, c in enumerate(caps))
    label = num + ' ' + ' '.join(caps)
    return (f'<g class="{cls}" data-seek="{sec}" tabindex="0" role="button" aria-label="{label}">'
            f'<polygon points="{pts}"></polygon>'
            f'<text class="num" x="{dx:.1f}" y="{ny:.1f}">{num}</text>{lines}</g>')


def passport():
    cells = ''.join(_hexcell(*h) for h in HEX)
    return f'''<section class="zb__s" id="passport"><div class="zb__comb"></div><div class="zb__w">
<p class="zb__lab"><b>02</b> · Паспорт площадки</p>
<h2 class="zb__h2">Все цифры фильма собраны в одной соте</h2>
<p class="zb__intro">Знак технопарка это сота, поэтому инфографику фильма страница
пересобрала в сотовый паспорт. В центре стоит размер площадки, вокруг заведённые
мощности и площади административно-бытового корпуса. Клик по ячейке
перематывает фильм к эпизоду, из которого взята цифра.</p>
<div class="zb__pass">
<div class="zb__hex r"><svg viewBox="-262 -272 524 544" role="group"
 aria-label="Паспорт площадки: площадь, инженерные мощности и площади АБК">{cells}</svg></div>
<div class="r">
<ul class="zb__pass-t">
<li><b>Вода.</b> Собственный водозабор производительностью 580 м³ в сутки.</li>
<li><b>Электричество.</b> Распределительная подстанция мощностью 10 МВт.</li>
<li><b>Тепло.</b> Котельная мощностью 40,5 МВт на территории площадки.</li>
<li><b>Люди.</b> 1735 м² офисов и 178 м² конференц-залов в АБК.</li>
<li><b>Земля.</b> Более 70 гектаров, из них 30,2% свободны под новый проект.</li>
</ul>
<button class="zb__tile" type="button" data-seek="47" style="margin-top:24px;width:100%">
<img src="{IMG}/eng-2.jpg" width="1000" height="562" loading="lazy"
 alt="Кадр фильма: котельная и инженерные сети технопарка «Зубово»">
<span>Энергоцентр площадки: котельная, сети, подстанция<em>0:47</em></span></button>
</div></div></div></section>'''


def land():
    r = 80.0
    c = 2 * math.pi * r
    arcs, legend, acc = '', '', 0.0
    for i, (pc, col, name, note) in enumerate(LAND):
        ln = c * pc / 100
        arcs += (f'<circle data-seg="{i}" cx="110" cy="110" r="{r}" stroke="{col}" '
                 f'stroke-dasharray="{ln:.2f} {c:.2f}" stroke-dashoffset="{ln:.2f}" '
                 f'transform="rotate({acc * 3.6:.2f} 110 110)"></circle>')
        legend += (f'<button type="button" data-leg="{i}" data-seek="75">'
                   f'<span class="sw" style="background:{col}"></span>'
                   f'<span class="pc">{str(pc).replace(".", ",").replace(",0", "")}%</span>'
                   f'<span><b>{name}</b><i>{note}</i></span></button>')
        acc += pc
    return f'''<section class="zb__s" id="land"><div class="zb__w">
<p class="zb__lab"><b>03</b> · Земельный баланс</p>
<h2 class="zb__h2">Треть площадки ещё свободна</h2>
<p class="zb__intro">В фильме баланс участков показан кольцом поверх аэросъёмки.
Здесь это кольцо живое: наведите на строку, и сегмент выделится, а клик перемотает
фильм к этому эпизоду.</p>
<div class="zb__land">
<div class="zb__donut r" id="zb-donut">
<svg viewBox="0 0 220 220" aria-hidden="true">
<circle cx="110" cy="110" r="80" stroke="rgba(255,255,255,.07)" stroke-dasharray="none"
 stroke-dashoffset="0"></circle>{arcs}</svg>
<div class="zb__donut-c"><b>70+ га</b><i>общая площадь</i></div></div>
<div class="zb__leg r">{legend}</div></div>
<figure class="zb__frame r" style="margin-top:30px"><img src="{IMG}/land.jpg" width="1100" height="619"
 loading="lazy" alt="Кадр фильма: участки технопарка «Зубово», раскрашенные по статусу">
<figcaption>Кадр фильма, 1:17 · участки, раскрашенные по статусу: занятые, зарезервированные, свободные</figcaption></figure>
</div></section>'''


ICONS = {
    'key': '<svg class="ic" viewBox="0 0 52 58" fill="none" aria-hidden="true">'
           '<path d="M26 1.7 49.6 15v26L26 54.3 2.4 41V15L26 1.7Z" stroke="#F07C1E" stroke-width="2"/>'
           '<circle cx="20.5" cy="29" r="5.5" stroke="#F07C1E" stroke-width="2"/>'
           '<path d="M26 29h13m-4 0v5m-4-5v4" stroke="#F07C1E" stroke-width="2" stroke-linecap="square"/></svg>',
    'net': '<svg class="ic" viewBox="0 0 52 58" fill="none" aria-hidden="true">'
           '<path d="M26 1.7 49.6 15v26L26 54.3 2.4 41V15L26 1.7Z" stroke="#F07C1E" stroke-width="2"/>'
           '<rect x="21" y="17" width="10" height="7" stroke="#F07C1E" stroke-width="2"/>'
           '<rect x="12" y="34" width="10" height="7" stroke="#F07C1E" stroke-width="2"/>'
           '<rect x="30" y="34" width="10" height="7" stroke="#F07C1E" stroke-width="2"/>'
           '<path d="M26 24v6M17 30h18v4M35 30v4" stroke="#F07C1E" stroke-width="2"/></svg>',
    'adm': '<svg class="ic" viewBox="0 0 52 58" fill="none" aria-hidden="true">'
           '<path d="M26 1.7 49.6 15v26L26 54.3 2.4 41V15L26 1.7Z" stroke="#F07C1E" stroke-width="2"/>'
           '<rect x="16" y="17" width="20" height="24" stroke="#F07C1E" stroke-width="2"/>'
           '<path d="M21 23h4m2 0h4m-10 6h4m2 0h4m-10 6h10" stroke="#F07C1E" stroke-width="2" stroke-linecap="square"/></svg>',
}


def terms():
    cards = ''.join(f'<div class="zb__term">{ICONS[i]}<h3>{t}</h3><p>{d}</p></div>'
                    for i, t, d in TERMS)
    return f'''<section class="zb__s" id="terms"><div class="zb__comb"></div><div class="zb__w">
<p class="zb__lab"><b>04</b> · Что получает резидент</p>
<h2 class="zb__h2">Три довода, которые фильм проговаривает прямым текстом</h2>
<div class="zb__advimg r"><img src="{IMG}/adv.jpg" width="1280" height="549" loading="lazy"
 alt="Кадр фильма: готовые корпуса технопарка «Зубово» с высоты"></div>
<div class="zb__terms r">{cards}</div>
</div></section>'''


def work():
    tiles = ''.join(
        f'<button class="zb__tile" type="button" data-seek="{s}">'
        f'<img src="{IMG}/{n}.jpg" width="1000" height="562" loading="lazy" alt="Кадр фильма: {c.lower()}">'
        f'<span>{c}<em>{mmss(s)}</em></span></button>' for n, s, c in WORK)
    return f'''<section class="zb__s" id="work"><div class="zb__w">
<p class="zb__lab"><b>05</b> · Площадка в работе</p>
<h2 class="zb__h2">Резиденты, а не рендеры</h2>
<p class="zb__intro">Главный аргумент площадки в том, что она уже работает. Съёмка шла и
с воздуха, и внутри цехов: корпуса, склады, испытательные стенды и люди на смене.
Любой кадр ниже работает кнопкой перемотки на свой эпизод фильма.</p>
<div class="zb__grid r">{tiles}</div>
</div></section>'''


def voices():
    cards = ''.join(
        f'<button class="zb__voice" type="button" data-seek="{s}">'
        f'<img src="{IMG}/{n}.jpg" width="900" height="506" loading="lazy" alt="Кадр фильма: синхрон, {fio}">'
        f'<div><b>{fio}</b><i>{post}</i><p>{note}</p></div></button>'
        for n, s, fio, post, note in VOICES)
    return f'''<section class="zb__s" id="voices"><div class="zb__w">
<p class="zb__lab"><b>06</b> · Голоса площадки</p>
<h2 class="zb__h2">Два синхрона вместо закадрового обещания</h2>
<p class="zb__intro">Про стройку и про производство в кадре говорят те, кто ими
занимается. Это снимает главный вопрос к презентационному фильму: показанное
подтверждают люди с площадки.</p>
<div class="zb__voices r">{cards}</div>
</div></section>'''


def future():
    tiles = ''.join(
        f'<button class="zb__tile" type="button" data-seek="{s}">'
        f'<img src="{IMG}/{n}.jpg" width="1000" height="562" loading="lazy" alt="Кадр фильма: {c.lower()}">'
        f'<span>{c}<em>{mmss(s)}</em></span></button>' for n, s, c in DEV)
    return f'''<section class="zb__s" id="future"><div class="zb__w">
<p class="zb__lab"><b>07</b> · Развитие</p>
<h2 class="zb__h2">Площадка достраивается прямо в кадре</h2>
<p class="zb__intro">Финальная треть фильма про рост: подготовленные пятна
застройки, бетонные работы в новом корпусе и каркас административно-бытового
здания. Резидент видит не законченную картинку, а площадку в движении.</p>
<div class="zb__dev r">{tiles}</div>
<div class="zb__abk r">
<img src="{IMG}/abk.jpg" width="1100" height="619" loading="lazy"
 alt="Кадр фильма: рендер административно-бытового корпуса технопарка «Зубово»">
<div><h3>Административно-бытовой корпус</h3>
<p>Офисы, переговорные и конференц-залы для резидентов, чтобы инженеры и
управленцы сидели на той же площадке, где идёт производство.</p>
<div class="zb__nums"><div><b>1735</b><i>м² офисных помещений</i></div>
<div><b>178</b><i>м² конференц-залов</i></div></div></div></div>
</div></section>'''


def story():
    return '''<section class="zb__s" id="story"><div class="zb__w">
<p class="zb__lab"><b>08</b> · Как мы это сделали</p>
<div class="zb__story">
<div class="zb__step r"><div class="zb__num">01 / Задача</div>
<div><h3>Показать живую площадку, а не проект «на бумаге»</h3>
<p>Технопарк конкурирует за резидента с площадками соседних регионов, и решение
о заходе принимают по презентации. Значит, фильм должен за три минуты отвечать
на вопросы инвестора, а не рассказывать о преимуществах в общем.</p>
<ul><li>Объяснить, почему «Зубово» это удобная точка входа в Башкортостан.</li>
<li>Доказать, что мощности заведены, а корпуса построены.</li>
<li>Показать вклад площадки в промышленную политику региона.</li></ul></div></div>

<div class="zb__step r"><div class="zb__num">02 / Решение</div>
<div><h3>Технопарк глазами будущего резидента</h3>
<p>Сценарий выстроен как маршрут: регион и логистика, облёт территории,
инженерные мощности, земельный баланс, условия размещения, действующие
производства и стройка новых корпусов. Каждый тезис закрыт либо аэросъёмкой,
либо инфографикой с конкретной цифрой, либо синхроном сотрудника площадки.</p>
<ul><li>Съёмка с воздуха: масштаб территории и транспортная доступность.</li>
<li>Инфографика поверх кадров: мощности, площади, баланс участков.</li>
<li>Съёмка в цехах резидентов и два синхрона с руководителями.</li></ul></div></div>

<div class="zb__step r"><div class="zb__num">03 / Результат</div>
<div><h3>Готовая площадка, которой доверяют</h3>
<p>Фильм работает на встречах с инвесторами, делегациями и профильными
ведомствами, а также в цифровых каналах технопарка. Наглядная территория
и работающие производства снимают главное возражение: «Зубово» воспринимается
как живая площадка, куда можно заходить с производством.</p></div></div>
</div>
<button class="zb__tile r" type="button" data-seek="170" style="margin-top:38px;width:100%">
<img src="''' + IMG + '''/plan.jpg" width="1280" height="720" loading="lazy"
 alt="Финальный кадр фильма: контур технопарка «Зубово» с высоты">
<span>Финальный кадр фильма: контур площадки с высоты<em>2:50</em></span></button>
</div></section>'''


PAGE_JS = """<script>(function(){
 var v=document.getElementById('zb-video');
 var CH=""" + str([[s, n, c] for s, n, c in CHAPTERS]).replace("'", '"') + """;
 var DUR=""" + str(DUR) + """;
 // ── перемотка: любая кнопка с data-seek управляет одним плеером ──────────
 function seek(sec){
  if(!v)return;
  var go=function(){try{v.currentTime=sec;}catch(e){}v.play().catch(function(){});};
  if(v.readyState<1){v.addEventListener('loadedmetadata',go,{once:true});v.load();}else{go();}
  var r=v.getBoundingClientRect();
  if(r.top<0||r.bottom>innerHeight)v.scrollIntoView({behavior:'smooth',block:'center'});
 }
 document.addEventListener('click',function(e){
  var b=e.target.closest?e.target.closest('[data-seek]'):null;
  if(!b)return;e.preventDefault();seek(parseFloat(b.getAttribute('data-seek')));});
 // соты — <g>, до них клавиатура доходит только через Enter/Space
 document.addEventListener('keydown',function(e){
  if(e.key!=='Enter'&&e.key!==' ')return;
  var b=e.target.closest?e.target.closest('g[data-seek]'):null;
  if(!b)return;e.preventDefault();seek(parseFloat(b.getAttribute('data-seek')));});
 // ── шкала фильма: заливка сегмента и подсветка активной главы ────────────
 var segs=[].slice.call(document.querySelectorAll('.zb__seg')),
     chaps=[].slice.call(document.querySelectorAll('.zb__chap')),
     now=document.getElementById('zb-now'),last=-1;
 function paint(){
  var t=v.currentTime,cur=0,i;
  for(i=0;i<CH.length;i++){if(t>=CH[i][0])cur=i;}
  for(i=0;i<segs.length;i++){
   var a=CH[i][0],b=(i+1<CH.length?CH[i+1][0]:DUR),k=(t-a)/(b-a);
   k=k<0?0:(k>1?1:k);
   segs[i].firstChild.style.transform='scaleX('+k+')';}
  if(cur===last)return;last=cur;
  segs.forEach(function(s,i){s.setAttribute('aria-current',i===cur?'true':'false');});
  chaps.forEach(function(c,i){c.setAttribute('aria-current',i===cur?'true':'false');});
  if(now)now.innerHTML='<b>'+CH[cur][1]+'</b> · '+CH[cur][2];
 }
 if(v&&segs.length){v.addEventListener('timeupdate',paint);v.addEventListener('seeked',paint);
  segs[0].setAttribute('aria-current','true');chaps[0].setAttribute('aria-current','true');}
 // ── донат: легенда подсвечивает сегмент ─────────────────────────────────
 var dn=document.getElementById('zb-donut');
 if(dn){
  var arcs=[].slice.call(dn.querySelectorAll('[data-seg]'));
  [].slice.call(document.querySelectorAll('[data-leg]')).forEach(function(b){
   var i=+b.getAttribute('data-leg');
   function on(){arcs.forEach(function(a,k){a.classList.toggle('is-dim',k!==i);});}
   function off(){arcs.forEach(function(a){a.classList.remove('is-dim');});}
   b.addEventListener('mouseenter',on);b.addEventListener('focus',on);
   b.addEventListener('mouseleave',off);b.addEventListener('blur',off);});
  // кольцо дорисовывается, когда секция въезжает в экран
  var draw=function(){arcs.forEach(function(a){a.style.strokeDashoffset='0';});};
  if('IntersectionObserver' in window){
   var io2=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){draw();io2.disconnect();}});},{rootMargin:'0px 0px -12% 0px'});
   io2.observe(dn);}
  else draw();
 }
 // ── появление блоков ────────────────────────────────────────────────────
 var els=[].slice.call(document.querySelectorAll('.zb .r'));
 function inn(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(n);else io.observe(n);});
})();</script>"""


VIDEO_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"VideoObject","name":"Презентационный фильм технопарка «Зубово» (Уфа)",'
            '"description":"Презентационный фильм индустриальной площадки «Зубово» под Уфой: '
            'территория с воздуха, инженерные мощности, баланс участков, действующие резиденты '
            'и строительство новых корпусов.",'
            '"thumbnailUrl":"https://hand-marketing.ru' + IMG + '/poster.jpg",'
            '"contentUrl":"https://hand-marketing.ru' + VIDEO + '","duration":"PT3M4S",'
            '"uploadDate":"2021-11-01","publisher":{"@type":"Organization",'
            '"name":"Hand Marketing","logo":{"@type":"ImageObject",'
            '"url":"https://hand-marketing.ru/images/lib/as3365-6332-4339-a263-313566616365/152.png"}}}'
            '</script>')

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
                 '"@type":"BreadcrumbList","itemListElement":['
                 '{"@type":"ListItem","position":1,"name":"Проекты",'
                 '"item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"Video Production",'
                 '"item":"https://hand-marketing.ru/videoproduction/"},'
                 '{"@type":"ListItem","position":3,"name":"Технопарк «Зубово»",'
                 f'"item":"{URL}"}}]}}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Презентационный фильм технопарка «Зубово» под Уфой: кейс видеопродакшна | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: презентационный фильм индустриальной площадки «Зубово» (Уфа, Башкортостан). Аэросъёмка территории, инфографика мощностей, баланс участков и синхроны с руководителями площадки. Весь фильм разложен по главам прямо на странице.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Технопарк «Зубово» | кейс Hand Marketing">
<meta property="og:description" content="Презентационный фильм индустриальной площадки под Уфой: более 70 гектаров, заведённые мощности, действующие резиденты.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/poster.jpg">
<meta name="theme-color" content="#0A0C0F">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/geologica-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def build():
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма из rc.footer()
    body = (f'{rc.header()}<main class="zb">{hero()}{film()}{geo()}{passport()}{land()}'
            f'{terms()}{work()}{voices()}{future()}{story()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{VIDEO_LD}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'zubovo')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(build())
    # старая связка «десктоп Tilda + мобильная копия» больше не нужна: A2-файла быть
    # не должно, иначе деплой переименует его поверх нашей страницы
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
