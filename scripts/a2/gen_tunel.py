#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/creative/tunel/index.html: кейс «Дезинфекционный тоннель
AnVIT S12T и защитные лицевые экраны».

Материал — четыре картинки со старой тильдовской страницы: тоннель на
площадке, лицевой экран с печатью TELE2, экран на человеке и векторный знак
с панели. Ни чертежей, ни съёмки сборки, ни спецификации изделия нет.
Год клиент просил не ставить.

Идея страницы. Это единственный кейс на сайте, где мы проектировали
физический прибор с гидравликой, и все три требования ТЗ — разборность,
цикл не более 20 секунд, экономный расход — проверяются не словами,
а геометрией. Отсюда механики:

  • «Развёртка оболочки» — главная, такой на сайте не было. Тоннель
    показан фронтальным сечением, человек идёт сквозь него, а рядом
    заливается развёртка его одежды: 360 градусов по горизонтали,
    рост по вертикали. Форсунки на П-образных рамках бьют факелами,
    страница честно считает, куда факел достаёт: дальность по давлению,
    угол раскрытия, самозатенение цилиндра фигуры. Видно, зачем рамка
    П-образная (без перемычки не обработаны плечи и голова) и зачем
    коллекторов несколько (одна рамка не берёт спину). Табло считает
    покрытие, расход и время в зоне и сверяет его с нормой ТЗ.
  • «Разлёт конструкции» — тоннель раскладывается на детали. Состав
    каркаса не выдуман: стойки и ригель сняты с фотографии яркостью
    (scripts/tunel-assets.py), отсюда три пролёта и шесть панелей
    на сторону. У каждой детали помечено, видно её на кадре или она
    известна только из описания.
  • «Прогиб экрана» — ответ на вопрос, почему ПЭТ именно 4 мм. Жёсткость
    на изгиб растёт как куб толщины, но и вес листа растёт линейно, так что
    провисание под собственным весом падает как квадрат: против типовой
    плёнки 0,5 мм лист 4 мм провисает в 64 раза меньше. Считается формулой,
    а не на глаз, и вертикаль на графике честно помечена как сжатая.
  • «Накладка» — персонализация делалась на верхней накладке оголовья.
    Печать TELE2 снята с кадра inpaint'ом, и в конструктор встаёт
    произвольный текст поверх настоящего пластика.

Палитра снята с материала: красный и синий — с векторного знака, серый
профиля, бумага панели и асфальт — с фото площадки.

Шрифты: Bitter (слэб, голос приборной таблички и санитарной инструкции)
+ Ysabeau Office (канцелярский гротеск бланка) + PT Mono на телеметрию.

Ассеты: mirror/images/tunel/ (scripts/tunel-assets.py).

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

IMG = '/images/tunel'
URL = 'https://hand-marketing.ru/creative/tunel/'
TITLE = 'Дезинфекционный тоннель AnVIT S12T и лицевые экраны | Hand Marketing'
DESCR = ('Разработка дезинфекционного тоннеля AnVIT S12T для входа на '
         'мероприятие и защитных лицевых экранов: П-образные коллекторы, '
         'датчик движения, обработка за 3-5 секунд, экран из ПЭТ 4 мм '
         'с персонализацией на накладке.')

RU = {1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть',
      7: 'семь', 8: 'восемь'}   # числа в прозе набираются словами

MAP = json.load(open(os.path.join(HERE, 'tunel_map.json'), encoding='utf-8'))
PAL = MAP['palette']
FRAME = MAP['frame']
WHAT = MAP['what']

# ─── требования ТЗ: (номер, коротко, подводка в герое, что за этим стояло,
#     чем закрыто) ─────────────────────────────────────────────────────────
SPEC = [
    ('01', 'Собирается и разбирается',
     'уезжает с площадки вместе с застройкой',
     'Тоннель ехал на площадку и уезжал с неё вместе с остальной застройкой. '
     'Значит никакой сварки и монолита: только каркас на профиле и панели, '
     'которые снимаются.',
     'Каркас из алюминиевого профиля, шесть печатных панелей на сторону'),
    ('02', 'Цикл не более 20 секунд',
     'иначе на входе встаёт очередь',
     'На входе мероприятия очередь, и прибор, который держит человека дольше '
     'двадцати секунд, превращается в пробку у рамки.',
     'Датчик движения вместо кнопки, обработка от 3 до 5 секунд'),
    ('03', 'Экономно расходует жидкость',
     'средство тратится на каждом проходе',
     'Дезинфицирующее средство расходуется на каждом проходе, и накопительный '
     'контейнер надо было заправлять между потоками, а не между гостями.',
     'Мелкодисперсный аэрозоль вместо струи, накопительный контейнер'),
]

# ─── состав тоннеля: (id, деталь, откуда мы это знаем, пояснение) ───────────
# «кадр» — деталь видно на фотографии, «описание» — известна только из текста
PARTS = [
    ('frame', 'Каркас из алюминиевого профиля', 'кадр',
     'Четыре стойки на длинной стороне и один ригель посередине: три пролёта '
     'по горизонтали, два ряда по высоте.'),
    ('panels', 'Шесть печатных панелей на сторону', 'кадр',
     'Верхний ряд белый с печатью, нижний тёмно-синий. Печать и есть '
     'оформление: знак, маркировка изделия, QR-код.'),
    ('curtain', 'ПВХ-шторка на входе', 'кадр',
     'Ламели держат аэрозоль внутри и пропускают человека без двери.'),
    ('cap', 'Надстройка над проёмом', 'кадр',
     'Тёмный короб с маркой изделия и зелёная панель с пиктограммой '
     'над самым входом.'),
    ('sensor', 'Датчик движения', 'кадр',
     'Небольшой корпус сверху над проёмом. Он включает распыление, '
     'кнопки на тоннеле нет.'),
    ('mani', 'П-образные коллекторы с форсунками', 'описание',
     'Две стойки и перемычка. Подают средство на всю внешнюю поверхность '
     'одежды, включая плечи и голову.'),
    ('tank', 'Накопительный контейнер', 'описание',
     'Держит запас средства, чтобы тоннель работал потоком, '
     'а не по одному человеку.'),
]

CSS1 = """<style id="av-css">
/* Кейс «Дезинфекционный тоннель AnVIT S12T». Голос страницы — приборная
   табличка и санитарный бланк: слэб на заголовках, канцелярский гротеск
   в тексте, моноширинный на всех цифрах. Правки только в gen_tunel.py. */
.av{--red:%RED%;--navy:%NAVY%;--panel:%PANEL%;--alu:%ALU%;--asph:%ASPH%;
 --deep:#0F1A31;--deep2:#16233F;--paper:#EFEEE9;--card:#FFFFFF;
 --ink:#16181C;--mute:#5C616B;--line:rgba(22,24,28,.13);
 --lineD:rgba(255,255,255,.14);--mist:#6FD3E4;--mist2:#B6ECF4;
 font-family:'Ysabeau Office',Arial,sans-serif;color:var(--ink);
 background:var(--paper);font-size:18px;line-height:1.6;overflow-x:hidden}
.av *,.av *::before,.av *::after{box-sizing:border-box}
.av h1,.av h2,.av h3,.av .sl{font-family:'Bitter',Georgia,serif;font-weight:700}
.av .mn,.av .num{font-family:'PT Mono','SFMono-Regular',Consolas,monospace}
.av p{margin:0 0 15px}
.av img{max-width:100%;display:block}
.av section{padding:78px 40px;position:relative}
.av .in{max-width:1180px;margin:0 auto}
.av .nar{max-width:800px}
.av .tag{font-family:'PT Mono',monospace;font-size:12px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--red);margin:0 0 16px;display:flex;
 align-items:center;gap:10px}
.av .tag::after{content:'';flex:1;height:1px;background:currentColor;opacity:.35}
.av h2{font-size:clamp(27px,3.6vw,42px);line-height:1.12;margin:0 0 20px;
 letter-spacing:-.01em;font-weight:800}
.av h3{font-size:clamp(19px,2vw,23px);line-height:1.25;margin:0 0 10px}
.av .lead{font-size:clamp(17px,1.6vw,20px);line-height:1.55;color:var(--mute);
 max-width:760px}
.av .dark{background:var(--deep);color:#E7EBF2}
.av .dark h2,.av .dark h3{color:#fff}
.av .dark .lead,.av .dark .mute{color:rgba(231,235,242,.66)}
.av .dark .tag{color:var(--mist)}
.av .alt{background:#E6E4DD}
.av .mute{color:var(--mute)}
.av .note{font-size:14px;line-height:1.5;color:var(--mute)}
.av .dark .note{color:rgba(231,235,242,.55)}

/* ── ГЕРОЙ ───────────────────────────────────────────────────────────── */
.av-hero{background:var(--deep);color:#E7EBF2;padding:0;overflow:hidden}
.av-hero__in{max-width:1180px;margin:0 auto;padding:56px 40px 0;
 display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.86fr);
 gap:44px;align-items:end}
.av-plate{display:inline-flex;flex-wrap:wrap;align-items:center;gap:0;
 font-family:'PT Mono',monospace;font-size:12px;letter-spacing:.06em;
 border:1px solid var(--lineD);border-radius:3px;overflow:hidden;
 margin:0 0 26px;background:rgba(255,255,255,.03)}
.av-plate span{padding:7px 13px;border-right:1px solid var(--lineD);
 color:rgba(231,235,242,.72);white-space:nowrap}
.av-plate span:last-child{border-right:0}
.av-plate b{color:var(--mist);font-weight:400}
.av-hero h1{font-size:clamp(33px,5.4vw,64px);line-height:1.03;margin:0 0 22px;
 letter-spacing:-.022em;font-weight:800;color:#fff}
.av-hero h1 i{font-style:normal;color:var(--mist)}
.av-hero__lead{font-size:clamp(17px,1.7vw,21px);line-height:1.5;
 color:rgba(231,235,242,.74);max-width:560px;margin:0 0 34px}
.av-hero__ph{position:relative;align-self:end;margin:0}
.av-hero__ph img{width:100%;border-radius:5px 5px 0 0;display:block}
.av-hero__cap{position:absolute;left:0;right:0;bottom:0;padding:44px 16px 12px;
 font-family:'PT Mono',monospace;font-size:11.5px;line-height:1.45;
 color:rgba(255,255,255,.82);
 background:linear-gradient(transparent,rgba(9,15,28,.86))}
.av-hero__strip{border-top:1px solid var(--lineD);margin-top:44px}
.av-hero__strip .in{display:grid;grid-template-columns:repeat(3,1fr);
 padding:0 40px}
.av-hero__strip div{padding:22px 26px 26px;border-right:1px solid var(--lineD)}
.av-hero__strip div:first-child{padding-left:0}
.av-hero__strip div:last-child{border-right:0}
.av-hero__strip b{display:block;font-family:'Bitter',serif;font-weight:700;
 font-size:16px;color:#fff;margin-bottom:5px}
.av-hero__strip span{font-size:14.5px;color:rgba(231,235,242,.6);line-height:1.45}
.av-hero__strip em{font-style:normal;font-family:'PT Mono',monospace;
 font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mist);
 display:block;margin-bottom:9px}

/* ── ТРЕБОВАНИЯ ТЗ ───────────────────────────────────────────────────── */
.av-spec{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:38px}
.av-spec article{background:var(--card);border:1px solid var(--line);
 border-radius:5px;padding:26px 24px 24px;display:flex;flex-direction:column}
.av-spec .n{font-family:'PT Mono',monospace;font-size:12px;color:var(--red);
 letter-spacing:.12em;margin-bottom:14px}
.av-spec h3{font-size:20px;margin-bottom:12px}
.av-spec p{font-size:16px;line-height:1.55;color:var(--mute);flex:1}
.av-spec .did{margin-top:16px;padding-top:14px;border-top:1px solid var(--line);
 font-size:14.5px;line-height:1.45;color:var(--ink)}
.av-spec .did em{font-style:normal;font-family:'PT Mono',monospace;font-size:11px;
 letter-spacing:.13em;text-transform:uppercase;color:var(--mute);display:block;
 margin-bottom:6px}
"""


CSS2 = """
/* ── СИМУЛЯТОР: сечение тоннеля и развёртка оболочки ─────────────────── */
.av-sim{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.06fr);
 gap:26px;margin-top:34px;align-items:start}
.av-box{background:var(--deep2);border:1px solid var(--lineD);border-radius:6px;
 padding:16px 16px 14px;position:relative}
.av-box__h{display:flex;justify-content:space-between;align-items:baseline;
 gap:12px;margin-bottom:12px}
.av-box__h b{font-family:'PT Mono',monospace;font-weight:400;font-size:11.5px;
 letter-spacing:.14em;text-transform:uppercase;color:var(--mist)}
.av-box__h i{font-style:normal;font-family:'PT Mono',monospace;font-size:11.5px;
 color:rgba(231,235,242,.5)}
.av-box canvas{width:100%;height:auto;display:block;border-radius:3px}
.av-read{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-top:22px;
 background:var(--lineD);border:1px solid var(--lineD);border-radius:5px;
 overflow:hidden}
.av-read div{background:var(--deep2);padding:15px 16px 14px}
.av-read em{font-style:normal;display:block;font-family:'PT Mono',monospace;
 font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
 color:rgba(231,235,242,.5);margin-bottom:8px}
.av-read b{font-family:'PT Mono',monospace;font-weight:400;
 font-size:clamp(21px,2.6vw,30px);color:#fff;line-height:1;display:block}
.av-read b.warn{color:var(--red)}
.av-read b.ok{color:var(--mist)}
.av-read span{display:block;font-size:13px;color:rgba(231,235,242,.5);
 margin-top:7px;line-height:1.35}
.av-norm{margin-top:16px;border:1px solid var(--lineD);border-radius:5px;
 padding:14px 16px 15px}
.av-norm__t{display:flex;justify-content:space-between;gap:12px;
 font-family:'PT Mono',monospace;font-size:11.5px;
 color:rgba(231,235,242,.55);margin-bottom:9px}
.av-norm__bar{height:9px;border-radius:5px;background:rgba(255,255,255,.09);
 position:relative;overflow:hidden}
.av-norm__bar i{position:absolute;left:0;top:0;bottom:0;width:0;
 background:var(--mist);border-radius:5px;transition:width .12s linear}
.av-norm__bar u{position:absolute;top:-4px;bottom:-4px;width:2px;
 background:var(--red);text-decoration:none}
.av-ctl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px 24px;
 margin-top:24px;align-items:start}
.av-ctl label{display:block;font-family:'PT Mono',monospace;font-size:11px;
 letter-spacing:.13em;text-transform:uppercase;color:rgba(231,235,242,.55);
 margin-bottom:9px}
.av-ctl label b{color:#fff;font-weight:400;float:right;letter-spacing:0;
 text-transform:none;font-size:12.5px}
.av-ctl input[type=range]{width:100%;-webkit-appearance:none;appearance:none;
 height:4px;border-radius:3px;background:rgba(255,255,255,.16);outline:none;
 margin:0;cursor:pointer}
.av-ctl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;
 width:18px;height:18px;border-radius:50%;background:var(--mist);
 border:3px solid var(--deep2);box-shadow:0 0 0 1px var(--mist);cursor:pointer}
.av-ctl input[type=range]::-moz-range-thumb{width:14px;height:14px;
 border-radius:50%;background:var(--mist);border:2px solid var(--deep2);
 cursor:pointer}
.av-seg{display:flex;gap:0;border:1px solid var(--lineD);border-radius:4px;
 overflow:hidden}
.av-seg button{flex:1;background:transparent;border:0;color:rgba(231,235,242,.6);
 font:400 13px 'PT Mono',monospace;padding:9px 6px;cursor:pointer;
 border-right:1px solid var(--lineD);transition:background .15s,color .15s}
.av-seg button:last-child{border-right:0}
.av-seg button[aria-pressed=true]{background:var(--mist);color:#0C1526}
.av-run{margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.av-run button{background:var(--red);border:0;border-radius:4px;color:#fff;
 font:700 15px 'Bitter',serif;padding:14px 30px;cursor:pointer;
 transition:transform .15s,filter .15s}
.av-run button:hover{transform:translateY(-1px);filter:brightness(1.08)}
.av-run p{margin:0;font-size:13.5px;color:rgba(231,235,242,.5);max-width:560px;
 line-height:1.45}
.av-gap{margin-top:16px;border-left:2px solid var(--red);padding:2px 0 2px 16px;
 font-size:15px;line-height:1.5;color:rgba(231,235,242,.8);min-height:44px}
.av-gap b{color:#fff;font-weight:400;font-family:'Bitter',serif}

/* ── РАЗЛЁТ КОНСТРУКЦИИ ──────────────────────────────────────────────── */
.av-exp{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);
 gap:34px;margin-top:34px;align-items:start}
.av-exp__stage{background:var(--card);border:1px solid var(--line);
 border-radius:6px;padding:10px}
.av-exp__stage svg{width:100%;height:auto;display:block}
.av-exp g[data-part]{transition:transform .18s ease-out}
.av-exp g[data-part=mani],.av-exp g[data-part=tank]{opacity:var(--xray,.32)}
.av-exp g[data-part] *{transition:opacity .2s,stroke .2s}
.av-exp.hl g[data-part]:not(.on){opacity:.22}
.av-exp__slide{margin-top:14px;padding:0 6px 4px}
.av-exp__slide label{display:flex;justify-content:space-between;
 font-family:'PT Mono',monospace;font-size:11px;letter-spacing:.13em;
 text-transform:uppercase;color:var(--mute);margin-bottom:9px}
.av-exp__slide input{width:100%;-webkit-appearance:none;appearance:none;height:4px;
 border-radius:3px;background:rgba(22,24,28,.14);outline:none;cursor:pointer}
.av-exp__slide input::-webkit-slider-thumb{-webkit-appearance:none;width:18px;
 height:18px;border-radius:50%;background:var(--red);border:3px solid #fff;
 box-shadow:0 0 0 1px var(--red);cursor:pointer}
.av-exp__slide input::-moz-range-thumb{width:14px;height:14px;border-radius:50%;
 background:var(--red);border:2px solid #fff;cursor:pointer}
.av-exp__list{list-style:none;margin:0;padding:0}
.av-exp__list li{border-top:1px solid var(--line);padding:15px 0;cursor:pointer}
.av-exp__list li:last-child{border-bottom:1px solid var(--line)}
.av-exp__list b{display:block;font-family:'Bitter',serif;font-size:17px;
 line-height:1.25;margin-bottom:5px}
.av-exp__list p{margin:0;font-size:15px;line-height:1.45;color:var(--mute)}
.av-exp__list .src{display:inline-block;font-family:'PT Mono',monospace;
 font-size:10px;letter-spacing:.12em;text-transform:uppercase;
 padding:3px 8px;border-radius:3px;margin-bottom:8px}
.av-exp__list .src.kadr{background:rgba(35,53,99,.1);color:var(--navy)}
.av-exp__list .src.opis{background:rgba(230,33,49,.09);color:var(--red)}
.av-exp__list li.on b{color:var(--red)}
"""


CSS3 = """
/* ── ЭКРАН: прогиб и накладка ────────────────────────────────────────── */
.av-flex{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
 gap:34px;margin-top:34px;align-items:start}
.av-flex__stage{background:var(--card);border:1px solid var(--line);
 border-radius:6px;padding:18px}
.av-flex__stage svg{width:100%;height:auto;display:block}
.av-thk{display:flex;gap:0;border:1px solid var(--line);border-radius:4px;
 overflow:hidden;margin-top:16px}
.av-thk button{flex:1;background:#fff;border:0;border-right:1px solid var(--line);
 font:400 13.5px 'PT Mono',monospace;padding:11px 6px;cursor:pointer;
 color:var(--mute);transition:background .15s,color .15s}
.av-thk button:last-child{border-right:0}
.av-thk button[aria-pressed=true]{background:var(--navy);color:#fff}
.av-fig{margin-top:18px;font-size:15.5px;line-height:1.5;color:var(--mute)}
.av-fig b{color:var(--ink);font-family:'PT Mono',monospace;font-weight:400}
.av-plateb{background:var(--card);border:1px solid var(--line);border-radius:6px;
 padding:18px;overflow:hidden}
.av-plateb__wrap{position:relative;border-radius:4px;overflow:hidden}
.av-plateb__wrap img{width:100%;display:block}
.av-plateb__txt{position:absolute;display:flex;align-items:center;
 justify-content:center;color:#fff;font-family:'Bitter',serif;font-weight:800;
 letter-spacing:.02em;white-space:nowrap;transform:rotate(-1.2deg);
 text-shadow:0 1px 2px rgba(0,0,0,.35);overflow:hidden;line-height:1}
.av-plateb__in{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap}
.av-plateb__in input{flex:1;min-width:180px;height:46px;border-radius:4px;
 border:1px solid var(--line);padding:0 14px;
 font:400 16px 'Ysabeau Office',Arial,sans-serif;color:var(--ink);background:#FBFBFA}
.av-plateb__in input:focus{outline:2px solid var(--navy);outline-offset:-1px}
.av-plateb__in button{height:46px;border:1px solid var(--line);background:#fff;
 border-radius:4px;padding:0 16px;cursor:pointer;font:400 13px 'PT Mono',monospace;
 color:var(--mute)}
.av-plateb__in button:hover{border-color:var(--navy);color:var(--navy)}
.av-pair{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px}
.av-pair figure{margin:0}
.av-pair picture{display:block}
.av-pair img{border-radius:5px;width:100%;aspect-ratio:4/3;object-fit:cover}
.av-pair figcaption{margin-top:10px;font-size:14px;line-height:1.45;
 color:var(--mute)}

/* ── ФИНАЛ ───────────────────────────────────────────────────────────── */
.av-out{border-top:1px solid var(--lineD);padding-top:34px;margin-top:38px;
 display:grid;grid-template-columns:repeat(3,1fr);gap:26px}
.av-out div em{font-style:normal;display:block;font-family:'PT Mono',monospace;
 font-size:11px;letter-spacing:.14em;text-transform:uppercase;
 color:var(--mist);margin-bottom:9px}
.av-out div b{display:block;font-family:'Bitter',serif;font-size:19px;
 color:#fff;margin-bottom:7px;line-height:1.25}
.av-out div span{font-size:15px;color:rgba(231,235,242,.62);line-height:1.5}

.av .rv{opacity:0;transform:translateY(18px);
 transition:opacity .5s ease,transform .5s ease}
.av .rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
 .av .rv{opacity:1;transform:none;transition:none}
 .av-exp g[data-part]{transition:none}}

/* ── АДАПТИВ ─────────────────────────────────────────────────────────── */
@media (max-width:1080px){
 .av-hero__in{grid-template-columns:1fr;gap:30px;padding:48px 32px 0}
 .av-hero__ph{max-width:560px}
 .av-sim,.av-exp,.av-flex{grid-template-columns:1fr}
 /* в одну колонку холсты растягиваются во всю ширину и становятся
    неоправданно высокими: держим их в разумном кадре по центру */
 .av-box,.av-exp__stage{max-width:600px;margin-left:auto;margin-right:auto}
 .av-exp__slide{max-width:600px;margin-left:auto;margin-right:auto}
 .av-read{grid-template-columns:1fr 1fr}
 .av-out{grid-template-columns:1fr 1fr}
 .av section{padding:64px 32px}
 .av-hero__strip .in{grid-template-columns:1fr;padding:0 32px}
 .av-hero__strip div{border-right:0;border-bottom:1px solid var(--lineD);
  padding:20px 0}
 .av-hero__strip div:last-child{border-bottom:0}
}
@media (max-width:760px){
 .av{font-size:17px}
 .av section{padding:52px 20px}
 .av-hero__in{padding:38px 20px 0}
 .av-hero__strip .in{padding:0 20px}
 .av-spec{grid-template-columns:1fr;gap:16px}
 .av-ctl{grid-template-columns:1fr}
 .av-ctl>div[style]{grid-column:span 1!important}
 .av-out{grid-template-columns:1fr;gap:20px}
 .av-pair{grid-template-columns:1fr}
 .av-read{grid-template-columns:1fr 1fr}
 .av-plate{font-size:11px}
 .av-plate span{padding:6px 10px}
}
@media (max-width:520px){
 .av-read{grid-template-columns:1fr}
}
/* телефон в ландшафте: не выдавливать страницу высокими холстами */
@media (max-height:520px) and (orientation:landscape){
 .av section{padding:40px 22px}
 .av-hero__in{padding:30px 22px 0}
}
</style>"""


def pic(slug, alt, sizes='(max-width:760px) 92vw, 620px', cls='', small=True):
    """Кадр через <picture>: webp с jpg-запасом, узкий экран берёт версию 640."""
    s = f' srcset="{IMG}/{slug}-640.jpg 640w, {IMG}/{slug}.jpg 1200w" sizes="{sizes}"' if small else ''
    w = f' srcset="{IMG}/{slug}-640.jpg.webp 640w, {IMG}/{slug}.jpg.webp 1200w" sizes="{sizes}"' if small else f' srcset="{IMG}/{slug}.jpg.webp"'
    c = f' class="{cls}"' if cls else ''
    return (f'<picture><source type="image/webp"{w}>'
            f'<img{c} src="{IMG}/{slug}.jpg"{s} alt="{alt}" loading="lazy" decoding="async"></picture>')


def hero():
    strip = ''.join(
        f'<div><em>Требование {n}</em><b>{t}</b><span>{tease}</span></div>'
        for n, t, tease, _why, _did in SPEC)
    return (
      '<section class="av-hero"><div class="av-hero__in">'
      '<div>'
      '<div class="av-plate"><span>AnVIT</span><span>Тоннель дезинфекции '
      '<b>S12T</b></span><span>#antivirustube</span></div>'
      '<h1>Тоннель, через который<br>проходят <i>на входе</i></h1>'
      '<p class="av-hero__lead">Компания AnVIT занимается антивирусными '
      'решениями и пришла с задачей на два изделия сразу: тоннель, который '
      'обеззараживает верхнюю одежду участников мероприятия на входе, '
      'и защитный лицевой экран для персонала. Мы разрабатывали и то, и другое.</p>'
      '</div>'
      f'<figure class="av-hero__ph">{pic("tunnel", WHAT["tunnel"], "(max-width:1080px) 92vw, 520px")}'
      f'<figcaption class="av-hero__cap">{WHAT["tunnel"]}</figcaption></figure>'
      '</div>'
      f'<div class="av-hero__strip"><div class="in">{strip}</div></div>'
      '</section>')


def spec():
    cards = ''.join(
      f'<article class="rv"><div class="n">{n}</div><h3>{t}</h3><p>{why}</p>'
      f'<div class="did"><em>Чем закрыто</em>{did}</div></article>'
      for n, t, _tease, why, did in SPEC)
    return (
      '<section><div class="in">'
      '<div class="tag">Задача</div>'
      '<h2>Три требования, которые решали всё остальное</h2>'
      '<p class="lead">Задача звучала просто: обеззараживать одежду входящих. '
      'Но тоннель едет на площадку вместе с застройкой, работает в очереди '
      'и заправляется дезинфицирующим средством, и каждое из этих трёх '
      'обстоятельств задало конструкцию жёстче, чем сама дезинфекция.</p>'
      f'<div class="av-spec">{cards}</div>'
      '</div></section>')


def sim():
    return (
      '<section class="dark" id="av-sim"><div class="in">'
      '<div class="tag">Как он работает</div>'
      '<h2>Развёртка одежды: куда факел достаёт, а куда нет</h2>'
      '<p class="lead">Тоннель показан в сечении: человек идёт на нас сквозь '
      'П-образные рамки с форсунками. Справа лежит оболочка его одежды, развёрнутая '
      'в прямоугольник: по горизонтали полный оборот от груди к спине и обратно, '
      'по вертикали рост. Она заливается по мере прохода, и на ней сразу видно, '
      'зачем у рамки перемычка и почему коллекторов больше одного.</p>'
      '<div class="av-sim">'
      '<div class="av-box"><div class="av-box__h"><b>Сечение тоннеля</b>'
      '<i>вид со стороны выхода</i></div>'
      '<canvas id="avC1" width="640" height="740" role="img" '
      'aria-label="Сечение тоннеля: П-образные рамки с форсунками, человек '
      'проходит сквозь факелы аэрозоля"></canvas></div>'
      '<div class="av-box"><div class="av-box__h"><b>Оболочка одежды</b>'
      '<i>360° × 180 см</i></div>'
      '<canvas id="avC2" width="640" height="420" role="img" '
      'aria-label="Развёртка оболочки одежды: закрашены обработанные участки"></canvas>'
      '<div class="av-gap" id="avGap">Нажмите «Пустить человека»: страница '
      'посчитает проход по геометрии факелов.</div></div>'
      '</div>'
      '<div class="av-read">'
      '<div><em>Покрытие оболочки</em><b id="avCov">0 %</b>'
      '<span>доля внешней поверхности одежды, до которой дошёл аэрозоль</span></div>'
      '<div><em>Расход за проход</em><b id="avVol">0 мл</b>'
      '<span>работают только те рамки, под которыми человек</span></div>'
      '<div><em>Время в зоне</em><b id="avSec">0,0 с</b>'
      '<span>от первого срабатывания датчика до выхода из последней рамки</span></div>'
      '<div><em>Норма по заданию</em><b class="ok">20 с</b>'
      '<span>предельная длительность цикла, заданная клиентом</span></div>'
      '</div>'
      '<div class="av-norm"><div class="av-norm__t"><span>цикл</span>'
      '<span id="avNormT">0,0 с из 20 с</span></div>'
      '<div class="av-norm__bar"><i id="avNormB"></i><u style="left:25%"></u></div>'
      '<div class="av-norm__t" style="margin:9px 0 0"><span>красная засечка: '
      'заявленные в кейсе 3-5 секунд обработки</span><span></span></div></div>'
      '<div class="av-ctl">'
      '<div><label>Коллекторов в тоннеле <b id="avLn">2</b></label>'
      '<input type="range" id="avN" min="1" max="4" step="1" value="2"></div>'
      '<div><label>Скорость прохода <b id="avLv">1,0 м/с</b></label>'
      '<input type="range" id="avV" min="60" max="180" step="5" value="100"></div>'
      '<div><label>Давление на форсунке <b id="avLp">4 бар</b></label>'
      '<input type="range" id="avP" min="2" max="6" step="1" value="4"></div>'
      '<div><label>Форма рамки</label><div class="av-seg" id="avShape">'
      '<button type="button" data-v="1" aria-pressed="true">П-образная</button>'
      '<button type="button" data-v="0" aria-pressed="false">две стойки</button>'
      '</div></div>'
      '<div style="grid-column:span 2"><label>Что показано на сечении</label>'
      '<div class="av-seg" id="avView">'
      '<button type="button" data-v="jet" aria-pressed="true">факелы</button>'
      '<button type="button" data-v="reach" aria-pressed="false">зона досягаемости</button>'
      '</div></div>'
      '</div>'
      '<div class="av-run"><button type="button" id="avGo">Пустить человека</button>'
      '<p>Это модель, а не протокол испытаний. Считается геометрия: дальность '
      'факела по давлению, угол раскрытия 38°, самозатенение фигуры. '
      'Производительность форсунки взята типовой, 0,6 мл/с при 4 барах: '
      'паспорта изделия у нас нет.</p></div>'
      '</div></section>')


# ─── разлёт: аксонометрия тоннеля, собранная по замерам с фотографии ───────
# мир: X поперёк (0…1,0 м), Y вверх (0…2,1 м), Z вдоль (0…2,4 м)
# проекция: масштаб 150 px/м, глубина уходит вправо-вверх
SC, DPX, DPY = 120.0, -55.0, -34.0   # масштаб px/м; ширина уходит влево-вверх
OX, OY = 200.0, 470.0
W, H, L = 1.0, 2.1, 2.4
BAYS = [(0.0, 0.8), (0.8, 1.6), (1.6, 2.4)]   # три пролёта: четыре стойки по кадру
ROWS = [(0.05, 1.03), (1.03, 2.05)]           # два ряда: ригель по кадру на 1,03 м


def pr(x, y, z):
    """Мир → экран, косоугольная проекция. Длина тоннеля идёт по горизонтали,
    ширина уходит влево-вверх. Поэтому видны печатная сторона X=0, крыша
    и входной торец Z=0 — ровно то, что видно на фотографии."""
    return (OX + SC * z + DPX * x, OY - SC * y + DPY * x)


def _p(*pts):
    return ' '.join('%.1f,%.1f' % pr(*p) for p in pts)


def _ln(a, b, col, w=4, extra=''):
    x1, y1 = pr(*a)
    x2, y2 = pr(*b)
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{col}" stroke-width="{w}" stroke-linecap="round"{extra}/>')


def _pg(pts, fill, stroke='none', w=1, extra=''):
    return (f'<polygon points="{_p(*pts)}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{w}"{extra}/>')


def exploded_svg():
    alu, alu2 = PAL['alu'], '#9AA1AC'
    g = []

    # каркас: восемь стоек, продольные и поперечные ригели, полупрозрачная крыша
    fr = [_pg([(0, H, 0), (W, H, 0), (W, H, L), (0, H, L)], 'rgba(35,53,99,.07)')]
    for z in (0.0, 0.8, 1.6, 2.4):
        for x in (0.0, W):
            fr.append(_ln((x, 0, z), (x, H, z), alu))
    for x in (0.0, W):
        for y in (0.0, 1.03, H):
            fr.append(_ln((x, y, 0), (x, y, L), alu2 if y == 1.03 else alu))
    for z in (0.0, L):
        for y in (0.0, H):
            fr.append(_ln((0, y, z), (W, y, z), alu))
    g.append('<g data-part="frame" data-dir="0,0">' + ''.join(fr) + '</g>')

    # шесть печатных панелей видимой длинной стороны: нижний ряд синий,
    # верхний белый с печатью. Видна сторона X=W: глубина уходит вправо,
    # значит наружу смотрит именно она.
    pn = []
    for z0, z1 in BAYS:
        for j, (y0, y1) in enumerate(ROWS):
            fill = '#FFFFFF' if j else PAL['navy']
            pn.append(_pg([(0, y0, z0), (0, y1, z0), (0, y1, z1), (0, y0, z1)],
                          fill, '#B9C0CB', 1.2))
    # печать на верхнем ряду: синяя полоса маркировки и красный знак
    pn.append(_pg([(0, 1.03, 0.1), (0, 1.34, 0.1), (0, 1.34, 2.3), (0, 1.03, 2.3)],
                  PAL['navy'], 'none'))
    cx, cy = pr(0, 1.66, 1.8)
    pn.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="24" fill="{PAL["red"]}"/>')
    g.append('<g data-part="panels" data-dir="-92,-58">' + ''.join(pn) + '</g>')

    # ПВХ-шторка во входном проёме: ламели
    cu = [_pg([(0.06, 0.02, 0), (0.06, 1.95, 0), (0.94, 1.95, 0), (0.94, 0.02, 0)],
              'rgba(201,198,210,.55)', '#A9A6B4', 1.2)]
    k = 0.06
    while k < 0.94:
        cu.append(_ln((k, 0.02, 0), (k, 1.95, 0), '#B7B4C2', 1.6))
        k += 0.075
    g.append('<g data-part="curtain" data-dir="-124,8">' + ''.join(cu) + '</g>')

    # надстройка над проёмом: короб с маркой и зелёная панель с пиктограммой
    cp = [_pg([(0, H, 0), (W, H, 0), (W, H + .34, 0), (0, H + .34, 0)],
              '#2E3238', '#1D2024', 1.2),
          _pg([(0, H, 0), (0, H + .34, 0), (0, H + .34, .3), (0, H, .3)],
              '#3A3F46', '#1D2024', 1.2),
          _pg([(0.62, H + .04, 0), (0.94, H + .04, 0), (0.94, H + .30, 0),
               (0.62, H + .30, 0)], '#7FA845', 'none')]
    x1, y1 = pr(0.08, H + .12, 0)
    cp.append(f'<rect x="{x1:.1f}" y="{y1:.1f}" width="46" height="7" '
              f'fill="rgba(255,255,255,.86)"/>')
    g.append('<g data-part="cap" data-dir="-40,-118">' + ''.join(cp) + '</g>')

    # датчик движения: небольшой корпус сверху над проёмом
    sx, sy = pr(0.30, H + .40, 0.05)
    g.append(f'<g data-part="sensor" data-dir="22,-126">'
             f'<rect x="{sx:.1f}" y="{sy:.1f}" width="26" height="15" rx="2" '
             f'fill="#F2F2F0" stroke="#B9BDC2" stroke-width="1.2"/>'
             f'<circle cx="{sx + 13:.1f}" cy="{sy + 19:.1f}" r="3.4" '
             f'fill="{PAL["red"]}"/></g>')

    # П-образные коллекторы: две стойки и перемычка, точки — форсунки
    mn = []
    for z in (0.8, 1.6):
        mn.append(_ln((0.09, 0.2, z), (0.09, 1.95, z), PAL['red'], 3))
        mn.append(_ln((0.91, 0.2, z), (0.91, 1.95, z), PAL['red'], 3))
        mn.append(_ln((0.09, 1.95, z), (0.91, 1.95, z), PAL['red'], 3))
        for y in (0.32, 0.72, 1.12, 1.52, 1.9):
            for x in (0.09, 0.91):
                nx, ny = pr(x, y, z)
                mn.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="3" fill="#fff" '
                          f'stroke="{PAL["red"]}" stroke-width="1.6"/>')
        for x in (0.26, 0.5, 0.74):
            nx, ny = pr(x, 1.95, z)
            mn.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="3" fill="#fff" '
                      f'stroke="{PAL["red"]}" stroke-width="1.6"/>')
    g.append('<g data-part="mani" data-dir="-10,150">' + ''.join(mn) + '</g>')

    # накопительный контейнер у дальнего торца
    tk = [_pg([(.18, 0, 1.95), (.18, .46, 1.95), (.52, .46, 1.95), (.52, 0, 1.95)],
              '#8A9099', '#6E747D', 1.2),
          _pg([(.52, 0, 1.95), (.52, .46, 1.95), (.52, .46, 2.3), (.52, 0, 2.3)],
              '#9AA0A8', '#6E747D', 1.2),
          _pg([(.18, .46, 1.95), (.52, .46, 1.95), (.52, .46, 2.3), (.18, .46, 2.3)],
              '#AEB4BB', '#6E747D', 1.2)]
    g.append('<g data-part="tank" data-dir="130,100">' + ''.join(tk) + '</g>')

    # порядок отрисовки от дальнего к ближнему: коллекторы идут последними,
    # красные линии поверх панелей читаются как «внутри тоннеля»
    order = ['frame', 'panels', 'tank', 'curtain', 'cap', 'sensor', 'mani']
    g.sort(key=lambda t: order.index(t.split('data-part="')[1].split('"')[0]))
    vb = _viewbox(g)
    return (f'<svg viewBox="{vb}" role="img" aria-label="Аксонометрия '
            'тоннеля: каркас, печатные панели, шторка, надстройка, датчик, '
            'коллекторы и накопительный контейнер">' + ''.join(g) + '</svg>')


def _viewbox(groups, pad=18):
    """viewBox по объединению двух состояний — собранного и разобранного,
    чтобы на сцене не оставалось пустых полей и ничего не срезалось."""
    import re as _re
    xs, ys = [], []
    for gr in groups:
        dx, dy = (float(v) for v in
                  _re.search(r'data-dir="([-\d.]+),([-\d.]+)"', gr).groups())
        pts = []
        for m in _re.finditer(r'points="([^"]+)"', gr):
            pts += [tuple(float(v) for v in q.split(',')) for q in m.group(1).split()]
        for m in _re.finditer(r'x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', gr):
            a, b, c, d = (float(v) for v in m.groups())
            pts += [(a, b), (c, d)]
        for m in _re.finditer(r'cx="([-\d.]+)" cy="([-\d.]+)" r="([-\d.]+)"', gr):
            cx, cy, r = (float(v) for v in m.groups())
            pts += [(cx - r, cy - r), (cx + r, cy + r)]
        for m in _re.finditer(r'x="([-\d.]+)" y="([-\d.]+)" width="([-\d.]+)" height="([-\d.]+)"', gr):
            x, y, w_, h_ = (float(v) for v in m.groups())
            pts += [(x, y), (x + w_, y + h_)]
        for x, y in pts:
            xs += [x, x + dx]
            ys += [y, y + dy]
    x0, x1 = min(xs) - pad, max(xs) + pad
    y0, y1 = min(ys) - pad, max(ys) + pad
    return f'{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}'


def exploded():
    items = ''.join(
      f'<li data-part="{pid}" tabindex="0"><span class="src '
      f'{"kadr" if src == "кадр" else "opis"}">'
      f'{"видно на кадре" if src == "кадр" else "из описания"}</span>'
      f'<b>{name}</b><p>{txt}</p></li>'
      for pid, name, src, txt in PARTS)
    return (
      '<section><div class="in">'
      '<div class="tag">Состав</div>'
      '<h2>Из чего он собран и откуда мы это знаем</h2>'
      '<p class="lead">Чертежей по кейсу не сохранилось, поэтому каркас снят '
      'с фотографии: светлые алюминиевые стойки читаются по яркости, '
      f'их четыре на длинной стороне, между ними один ригель. Значит '
      f'{FRAME["bays"]} пролёта и {FRAME["panels_per_side"]} печатных панелей '
      'на сторону. Всё, что видно на кадре, помечено одним ярлыком, всё, что '
      'известно только из описания изделия, другим.</p>'
      f'<div class="av-exp" id="avExp"><div><div class="av-exp__stage">{exploded_svg()}</div>'
      '<div class="av-exp__slide"><label><span>Собран</span>'
      '<span>Разобран</span></label>'
      '<input type="range" id="avE" min="0" max="100" value="0" '
      'aria-label="Разобрать тоннель"></div></div>'
      f'<ul class="av-exp__list">{items}</ul>'
      '</div></div></section>')


def shield():
    return (
      '<section class="alt"><div class="in">'
      '<div class="tag">Второе изделие</div>'
      '<h2>Лицевой экран: почему ПЭТ именно 4 миллиметра</h2>'
      '<p class="lead">Экран должен был оставаться лёгким, не царапаться '
      'и держать форму на голове целую смену. Толщину выбирали не на глаз. '
      'Жёсткость листа на изгиб растёт как куб толщины, но и вес растёт '
      'вместе с ней, поэтому провисание под собственным весом падает '
      'как квадрат: лист 4 мм держится в 64 раза лучше плёнки 0,5 мм.</p>'
      '<div class="av-flex">'
      '<div><div class="av-flex__stage">'
      '<svg viewBox="0 0 520 330" role="img" aria-label="Прогиб листа '
      'в зависимости от толщины: четыре кривые от 0,5 до 4 мм">'
      '<line x1="46" y1="52" x2="486" y2="52" stroke="rgba(22,24,28,.16)" '
      'stroke-width="1" stroke-dasharray="4 5"/>'
      '<text x="46" y="40" font-family="PT Mono, monospace" font-size="11" '
      'fill="#5C616B">заделка: лист выходит из оголовья</text>'
      '<g id="avBends"></g>'
      '<text id="avDrop" x="46" y="322" font-family="PT Mono, monospace" '
      'font-size="11" fill="#5C616B"></text>'
      '</svg></div>'
      '<div class="av-thk" id="avThk">'
      '<button type="button" data-t="0.5" aria-pressed="false">плёнка 0,5 мм</button>'
      '<button type="button" data-t="1" aria-pressed="false">1 мм</button>'
      '<button type="button" data-t="2" aria-pressed="false">2 мм</button>'
      '<button type="button" data-t="4" aria-pressed="true">ПЭТ 4 мм</button>'
      '</div>'
      '<p class="av-fig" id="avFig"></p>'
      '<p class="note">Считается консольная пластина под собственным весом: '
      'жёсткость на изгиб идёт как t³, погонная нагрузка как t, значит прогиб '
      'как 1/t². Абсолютные миллиметры зависят от вылета и способа крепления, '
      'поэтому важно здесь отношение, а не число.</p></div>'
      '<div>'
      '<h3>Персонализация на верхней накладке</h3>'
      '<p class="mute">Экран печатали под заказчика: полноцветная печать '
      'ложилась на накладку оголовья, а само поле обзора оставалось чистым. '
      'Ниже настоящая накладка с кадра, с которой алгоритмом снята печать. '
      'Наберите слово и посмотрите, как встаёт чужое имя.</p>'
      '<div class="av-plateb"><div class="av-plateb__wrap" id="avPlateW">'
      f'<img src="{IMG}/band-clean.jpg" alt="Накладка оголовья без печати" '
      'loading="lazy" decoding="async">'
      '<div class="av-plateb__txt" id="avPlateT">TELE2</div></div>'
      '<div class="av-plateb__in">'
      '<input type="text" id="avPlateI" maxlength="14" value="TELE2" '
      'aria-label="Надпись на накладке" placeholder="ваше слово">'
      '<button type="button" id="avPlateR">вернуть TELE2</button></div></div>'
      '<div class="av-pair">'
      f'<figure>{pic("shield", WHAT["shield"], "(max-width:1080px) 44vw, 280px")}'
      '<figcaption>Как экран пришёл с производства: печать TELE2 '
      'на накладке, поле обзора без плёнки и рисунка.</figcaption></figure>'
      f'<figure>{pic("worn", WHAT["worn"], "(max-width:1080px) 44vw, 280px")}'
      '<figcaption>На человеке: экран закрывает лицо целиком '
      'и не запотевает от дыхания.</figcaption></figure>'
      '</div></div></div></div></section>')


def outro():
    return (
      '<section class="dark"><div class="in nar">'
      '<div class="tag">Итог</div>'
      '<h2>Два изделия из одной задачи</h2>'
      '<p class="lead">Тоннель встал на входе площадки и работал потоком: '
      'человек входит, датчик включает распыление, мелкодисперсный аэрозоль '
      'обрабатывает верхнюю одежду и открытые кожные покровы, '
      'через три-пять секунд человек выходит с другой стороны. '
      'Экраны сделали для персонала, который весь день стоит на входе '
      'и в зале.</p>'
      '<div class="av-out">'
      '<div><em>Тоннель</em><b>AnVIT S12T</b><span>Разборный каркас, шесть '
      'печатных панелей на сторону, П-образные коллекторы, накопительный '
      'контейнер, датчик движения вместо кнопки.</span></div>'
      '<div><em>Цикл</em><b>3-5 секунд</b><span>Вчетверо меньше предельных '
      'двадцати секунд, заданных клиентом: очередь на входе не встаёт.</span></div>'
      '<div><em>Экран</em><b>ПЭТ 4 мм</b><span>Лёгкий, стойкий к царапинам, '
      'не запотевает. Полноцветная персонализация на верхней '
      'накладке.</span></div>'
      '</div></div></section>')


PAGE_JS = r"""<script>(function(){
'use strict';
var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;

/* ── появление блоков ────────────────────────────────────────────────── */
var rv=[].slice.call(document.querySelectorAll('.av .rv'));
if(window.IntersectionObserver&&!RM){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},
    {threshold:.15});
  rv.forEach(function(n){io.observe(n);});
}else{rv.forEach(function(n){n.classList.add('in');});}

/* ── СИМУЛЯТОР: развёртка оболочки одежды ────────────────────────────── */
/* Мир в метрах: X поперёк 0…1,0; Y вверх 0…2,1; Z вдоль 0…2,4.
   Человек — цилиндр радиуса 0,24 м, который выше 1,50 м заваливается
   в купол плеч и головы: именно из-за купола горизонтальный факел
   со стойки не берёт верх, и нужна перемычка. */
var TW=1.0,TH=2.1,TL=2.4,R=0.24,BH=1.80,NA=72,NH=36,NC=NA*NH;
var YS=[0.18,0.53,0.88,1.23,1.58,1.90];   // ряды форсунок на нечётной рамке
var YS2=[0.35,0.70,1.05,1.40,1.75];       // на чётной — разведены по высоте
var XS=[0.26,0.42,0.58,0.74];             // форсунки перемычки
var COST=Math.cos(38*Math.PI/180), CN=0.30, KD=34, DOSE=1;
var PX=new Float32Array(NC),PY=new Float32Array(NC),PZ=new Float32Array(NC),
    NX=new Float32Array(NC),NY=new Float32Array(NC),NZ=new Float32Array(NC),
    dose=new Float32Array(NC);
(function(){for(var ia=0;ia<NA;ia++){var a=(ia+.5)*2*Math.PI/NA,sa=Math.sin(a),ca=Math.cos(a);
 for(var ih=0;ih<NH;ih++){var h=(ih+.5)*BH/NH,t=Math.min(1,Math.max(0,(h-1.50)/(BH-1.50))),
  phi=t*78*Math.PI/180,cp=Math.cos(phi),rr=R*(1-.55*t*t),i=ia*NH+ih;
  PX[i]=.5+rr*sa;PY[i]=h;PZ[i]=rr*ca;
  NX[i]=sa*cp;NY[i]=Math.sin(phi);NZ[i]=ca*cp;}}})();

var st={n:2,v:1.0,p:4,shape:1,view:'jet',zp:-0.8,run:false,vol:0,tin:0,done:false};
function zks(){var a=[],k;for(k=0;k<st.n;k++)a.push(TL*(k+1)/(st.n+1));return a;}
function noz(k){ // форсунки k-й рамки: две стойки плюс перемычка
  var out=[],ys=(k%2?YS2:YS),i;
  for(i=0;i<ys.length;i++){out.push([0.09,ys[i],1,0,0]);out.push([0.91,ys[i],-1,0,0]);}
  if(st.shape)for(i=0;i<XS.length;i++)out.push([XS[i],1.98,0,-1,0]);
  return out;}
function reach(){return 0.30+0.10*st.p;}
function flow(){return 0.6*Math.sqrt(st.p/4);}

function step(dt){
  var Z=zks(),D=reach(),q=flow(),any=false,k,z,nz,j,f,fx,fy,fz,ax,ay,az,i,vx,vy,vz,d,cb,cn,g;
  for(k=0;k<Z.length;k++){z=Z[k];
    if(Math.abs(st.zp-z)>=0.55)continue;
    any=true;nz=noz(k);
    for(j=0;j<nz.length;j++){f=nz[j];fx=f[0];fy=f[1];ax=f[2];ay=f[3];az=f[4];fz=z;
      st.vol+=q*dt;
      for(i=0;i<NC;i++){
        vy=PY[i]-fy; if(vy>D||vy<-D)continue;
        vx=PX[i]-fx; vz=(st.zp+PZ[i])-fz;
        d=Math.sqrt(vx*vx+vy*vy+vz*vz); if(d>D||d<1e-6)continue;
        cb=(vx*ax+vy*ay+vz*az)/d; if(cb<COST)continue;
        cn=-(vx*NX[i]+vy*NY[i]+vz*NZ[i])/d; if(cn<CN)continue;
        g=d/0.35;
        dose[i]+=KD*dt*q*cn*Math.sqrt(cn)*cb*cb/(1+g*g);}}}
  if(any)st.tin+=dt;
  st.zp+=st.v*dt;
}

function covered(){var c=0,i;for(i=0;i<NC;i++)if(dose[i]>=DOSE)c++;return c/NC;}
/* какие зоны остались сухими: по высоте и по обороту */
function gaps(){
  var zn=[['плечи и голова',0,0],['корпус',0,0],['ниже колена',0,0]],
      az=[['грудь',0,0],['бока',0,0],['спина',0,0]],i,ia,ih,h,a,zi,ai;
  for(i=0;i<NC;i++){ia=(i/NH)|0;ih=i%NH;h=(ih+.5)*BH/NH;a=(ia+.5)*360/NA;
    zi=h>=1.50?0:(h>0.50?1:2);
    ai=(a<45||a>315)?0:((a>135&&a<225)?2:1);
    zn[zi][1]++;az[ai][1]++;
    if(dose[i]<DOSE){zn[zi][2]++;az[ai][2]++;}}
  function worst(t){var b=t[0],i;for(i=1;i<t.length;i++)if(t[i][2]/t[i][1]>b[2]/b[1])b=t[i];
    return [b[0],b[2]/b[1]];}
  return {h:worst(zn),a:worst(az)};
}
var fmt1=function(x){return x.toFixed(1).replace('.',',');};
function report(){
  var c=covered(),g=gaps(),el=document.getElementById('avGap'),s;
  document.getElementById('avCov').textContent=Math.round(c*100)+' %';
  document.getElementById('avCov').className=c<0.85?'warn':'ok';
  document.getElementById('avVol').textContent=fmt1(st.vol)+' мл';
  document.getElementById('avSec').textContent=fmt1(st.tin)+' с';
  var pc=Math.min(1,st.tin/20);
  document.getElementById('avNormB').style.width=(pc*100)+'%';
  document.getElementById('avNormT').textContent=fmt1(st.tin)+' с из 20 с';
  if(!el)return;
  if(c>=0.94){s='<b>Обработано '+Math.round(c*100)+' % оболочки.</b> Сухими '
    +'остаются обувь и самый низ брюк: ниже нижнего ряда форсунок факел '
    +'не достаёт, и это цена того, что форсунки не льют в пол.';}
  else{s='<b>Сухими остались '+g.h[0]+'</b>: не обработано '
    +Math.round(g.h[1]*100)+' % этой зоны';
    if(g.a[1]>0.12)s+=', по обороту хуже всего '+g.a[0];
    s+='. ';
    if(!st.shape&&g.h[0]==='плечи и голова')
      s+='Стойки бьют горизонтально, а плечи и голова это купол: '
        +'без перемычки факел скользит по касательной.';
    else if(st.n<2)s+='Одна рамка успевает пройти по человеку только один раз. '
      +'Прямо напротив форсунки факел ещё не раскрылся, и между рядами '
      +'остаются сухие полосы, их закрывает вторая рамка, у которой '
      +'ряды разведены по высоте.';
    else if(st.v>1.3)s+='При таком шаге человек проскакивает зону быстрее, '
      +'чем набирается доза.';
    else if(st.p<3)s+='На двух барах факел не добивает до дальней стороны: '
      +'от стойки до противоположного бока 0,65 м.';
    else s+='Добавьте рамку, сбавьте шаг или поднимите давление.';}
  el.innerHTML=s;
}

/* ── отрисовка ───────────────────────────────────────────────────────── */
var c1=document.getElementById('avC1'),c2=document.getElementById('avC2');
var g1=c1&&c1.getContext('2d'),g2=c2&&c2.getContext('2d');
var W1=640,H1=740,S=250,X0=195,Y0=700;                    // сечение
var PL=50,PR=590,PY0=34,PY1=86;                           // полоса плана
function wx(x){return X0+x*S;}
function wy(y){return Y0-y*S;}
function px_(z){return PL+(z/TL)*(PR-PL);}

function human(g){
  // силуэт в сечении отдельными телами: так читаются руки вдоль корпуса,
  // а не сливаются с торсом в одно пятно
  var cx=wx(.5),fill='rgba(231,235,242,.10)',line='rgba(231,235,242,.52)';
  function shape(fn){g.beginPath();fn();g.fillStyle=fill;g.fill();
    g.strokeStyle=line;g.lineWidth=2;g.stroke();}
  function rr(x0,y0,x1,y1,r){ // скруглённый прямоугольник по мировым метрам
    var a=wx(x0),b=wy(y1),c=wx(x1),d=wy(y0);
    g.moveTo(a+r,b);g.lineTo(c-r,b);g.quadraticCurveTo(c,b,c,b+r);
    g.lineTo(c,d-r);g.quadraticCurveTo(c,d,c-r,d);g.lineTo(a+r,d);
    g.quadraticCurveTo(a,d,a,d-r);g.lineTo(a,b+r);g.quadraticCurveTo(a,b,a+r,b);}
  shape(function(){g.arc(cx,wy(1.68),.105*S,0,6.284);});          // голова
  shape(function(){rr(.47,1.50,.53,1.60,3);});                    // шея
  shape(function(){                                               // торс
    g.moveTo(wx(.28),wy(1.50));g.lineTo(wx(.72),wy(1.50));
    g.lineTo(wx(.695),wy(1.14));g.lineTo(wx(.685),wy(0.92));
    g.lineTo(wx(.315),wy(0.92));g.lineTo(wx(.305),wy(1.14));g.closePath();});
  shape(function(){rr(.245,0.72,.30,1.46,7);});                   // левая рука
  shape(function(){rr(.70,0.72,.755,1.46,7);});                   // правая рука
  shape(function(){rr(.335,0.02,.435,0.94,7);});                  // левая нога
  shape(function(){rr(.565,0.02,.665,0.94,7);});                  // правая нога
}

function kk(c){return c.clientWidth?c.width/c.clientWidth:1;}
function mono(g,c,px){g.font=(px*kk(c)).toFixed(1)+'px "PT Mono",monospace';}

function drawSection(){
  var g=g1,K1=kk(c1),tight=K1>1.6;g.clearRect(0,0,W1,H1);
  g.fillStyle='#0C1526';g.fillRect(0,0,W1,H1);
  // ── полоса плана: тоннель сверху, рамки поперёк, человек точкой
  g.strokeStyle='rgba(255,255,255,.22)';g.lineWidth=1.5;
  g.strokeRect(PL,PY0,PR-PL,PY1-PY0);
  g.fillStyle='rgba(255,255,255,.34)';
  mono(g,c1,11);
  g.fillText('вход',PL,PY0-8);
  g.textAlign='right';g.fillText('выход',PR,PY0-8);g.textAlign='left';
  g.fillText('план сверху, 2,4 м',PL,PY1+8+11*K1);
  var Z=zks(),k,x;
  for(k=0;k<Z.length;k++){x=px_(Z[k]);
    g.strokeStyle=Math.abs(st.zp-Z[k])<0.55?'#E62131':'rgba(230,33,49,.42)';
    g.lineWidth=3;g.beginPath();g.moveTo(x,PY0+2);g.lineTo(x,PY1-2);g.stroke();}
  // шторка на входе
  g.strokeStyle='rgba(255,255,255,.28)';g.lineWidth=1;
  for(k=0;k<6;k++){g.beginPath();g.moveTo(PL+1+k*1.6,PY0+2);g.lineTo(PL+1+k*1.6,PY1-2);g.stroke();}
  x=px_(Math.max(-0.8,Math.min(TL+0.8,st.zp)));
  g.fillStyle='#B6ECF4';g.beginPath();
  g.arc(Math.max(PL-28,Math.min(PR+28,x)),(PY0+PY1)/2,9,0,6.284);g.fill();

  // ── сечение тоннеля
  g.strokeStyle='rgba(255,255,255,.26)';g.lineWidth=2;
  g.strokeRect(wx(0),wy(TH),TW*S,TH*S);
  g.fillStyle='rgba(255,255,255,.30)';
  g.fillText('сечение: 1,0 × 2,1 м',wx(0),wy(TH)-12);
  // зона досягаемости или факелы
  var D=reach(),Zn=zks(),k0=0,j,f,i;
  for(i=1;i<Zn.length;i++)
    if(Math.abs(st.zp-Zn[i])<Math.abs(st.zp-Zn[k0]))k0=i;
  var nzz=noz(k0),live=Math.max(0,1-Math.abs(st.zp-Zn[k0])/0.55);
  if(st.view==='reach'){
    var img=g.createImageData(1,1);
    for(var sx=wx(0);sx<wx(TW);sx+=3)for(var sy=wy(TH);sy<Y0;sy+=3){
      var mx=(sx-X0)/S,my=(Y0-sy)/S,hit=0;
      for(j=0;j<nzz.length;j++){f=nzz[j];
        var ux=mx-f[0],uy=my-f[1],dd=Math.sqrt(ux*ux+uy*uy);
        if(dd>D||dd<1e-4)continue;
        if((ux*f[2]+uy*f[3])/dd<COST)continue;
        hit=Math.max(hit,1-dd/D);}
      if(hit>0){g.fillStyle='rgba(111,211,228,'+(0.10+hit*0.38).toFixed(3)+')';
        g.fillRect(sx,sy,3.4,3.4);}}
  }else{
    // факелы: слабый конус плюс капли внутри него — сплошная заливка
    // на пересечении конусов давала ромбы, похожие на узор, а не на аэрозоль
    g.save();g.beginPath();g.rect(wx(0)+1,wy(TH)+1,TW*S-2,TH*S-2);g.clip();
    for(j=0;j<nzz.length;j++){f=nzz[j];
      var ang=Math.atan2(-f[3],f[2]),half=38*Math.PI/180,
          nx0=wx(f[0]),ny0=wy(f[1]),Lj=D*S,
          gr=g.createRadialGradient(nx0,ny0,2,nx0,ny0,Lj);
      gr.addColorStop(0,'rgba(182,236,244,'+(0.04+0.20*live).toFixed(3)+')');
      gr.addColorStop(1,'rgba(111,211,228,0)');
      g.fillStyle=gr;g.beginPath();g.moveTo(nx0,ny0);
      g.arc(nx0,ny0,Lj,ang-half,ang+half);g.closePath();g.fill();
      if(live<=0.02)continue;
      g.fillStyle='rgba(210,244,250,'+(0.10+0.55*live).toFixed(3)+')';
      for(i=0;i<18;i++){
        var u=Math.random(),rd=Lj*Math.sqrt(u),
            aa=ang+(Math.random()*2-1)*half*(0.35+0.65*Math.sqrt(u));
        g.beginPath();
        g.arc(nx0+Math.cos(aa)*rd,ny0+Math.sin(aa)*rd,
              0.7+1.5*(1-rd/Lj),0,6.284);
        g.fill();}}
    g.restore();
  }
  // П-рамка
  g.strokeStyle='#E62131';g.lineWidth=4;g.lineCap='round';
  g.beginPath();g.moveTo(wx(.09),wy(.20));g.lineTo(wx(.09),wy(1.95));
  if(st.shape)g.lineTo(wx(.91),wy(1.95));else{g.moveTo(wx(.91),wy(1.95));}
  g.lineTo(wx(.91),wy(.20));g.stroke();
  for(j=0;j<nzz.length;j++){f=nzz[j];
    g.fillStyle='#fff';g.beginPath();g.arc(wx(f[0]),wy(f[1]),3.4,0,6.284);g.fill();}
  // человек
  human(g);g.fillStyle='rgba(231,235,242,.10)';g.fill();
  g.strokeStyle='rgba(231,235,242,.55)';g.lineWidth=2;g.stroke();
  // подписи размеров
  g.fillStyle='rgba(255,255,255,.34)';
  g.fillText('форсунок: '+nzz.length,wx(TW)+14,wy(1.95));
  g.fillText('факел '+fmt1(D*100).replace(',0','')+' см',wx(TW)+14,wy(1.75));
  g.fillText('раскрытие 38°',wx(TW)+14,wy(1.55));
  if(!tight){
    g.fillText('соседние рамки',wx(TW)+14,wy(1.35));
    g.fillText('разведены по высоте',wx(TW)+14,wy(1.23));
    g.fillText('оболочка R 24 см',14,wy(0.95));}
  g.fillText('рост 1,80 м',14,wy(1.80));
}

function drawWrap(){
  var g=g2,K2=kk(c2),W=640,H=420,L=44*K2,T=14*K2,B=30*K2,Rt=10*K2,
      gw=W-L-Rt,gh=H-T-B,cw=gw/NA,ch=gh/NH,ia,ih,d,i;
  g.clearRect(0,0,W,H);
  g.fillStyle='#0C1526';g.fillRect(0,0,W,H);
  for(ia=0;ia<NA;ia++)for(ih=0;ih<NH;ih++){
    i=ia*NH+ih;d=dose[i];
    // четыре ступени: сухо, тронуто, обработано, обработано с запасом —
    // видно не только «дошло / не дошло», но и насколько равномерно
    if(d>=6)g.fillStyle='#D8F5FA';
    else if(d>=DOSE)g.fillStyle='#6FD3E4';
    else if(d>0)g.fillStyle='rgba(111,211,228,'+(0.08+0.30*d/DOSE).toFixed(3)+')';
    else g.fillStyle='#16233F';
    g.fillRect(L+ia*cw,T+gh-(ih+1)*ch,cw+.6,ch+.6);}
  g.strokeStyle='rgba(255,255,255,.16)';g.lineWidth=1;
  g.strokeRect(L,T,gw,gh);
  mono(g,c2,10.5);g.fillStyle='rgba(255,255,255,.5)';
  var lab=[['грудь',0],['бок',.25],['спина',.5],['бок',.75],['грудь',1]],j;
  for(j=0;j<lab.length;j++){
    var x=L+gw*lab[j][1];
    g.strokeStyle='rgba(255,255,255,.22)';
    g.beginPath();g.moveTo(x,T+gh);g.lineTo(x,T+gh+5);g.stroke();
    g.textAlign=j===0?'left':(j===lab.length-1?'right':'center');
    g.fillText(lab[j][0],x,T+gh+17*K2);}
  g.textAlign='right';
  var hs=[0,50,100,150,180],hi;
  for(hi=0;hi<hs.length;hi++){
    var y=T+gh-(hs[hi]/180)*gh;
    g.fillText(hs[hi]+(hi===hs.length-1?' см':''),L-7*K2,y+4*K2);}
  g.textAlign='left';
  // легенда ступеней дозы
  var lg=[['#16233F','сухо'],['rgba(111,211,228,.30)','тронуто'],
          ['#6FD3E4','обработано'],['#D8F5FA','с запасом']],lx=L;
  mono(g,c2,9.5);
  for(j=0;j<lg.length;j++){
    g.fillStyle=lg[j][0];g.fillRect(lx,3*K2,8*K2,8*K2);
    g.fillStyle='rgba(255,255,255,.5)';g.fillText(lg[j][1],lx+11*K2,10.5*K2);
    lx+=20*K2+g.measureText(lg[j][1]).width;}
}

function draw(){if(g1)drawSection();if(g2)drawWrap();}

var raf=null,last=0;
function tick(ts){
  if(!st.run)return;
  if(!last)last=ts;
  var dt=Math.min(0.05,(ts-last)/1000);last=ts;
  var sub=Math.max(1,Math.round(dt/(1/60))),k;
  for(k=0;k<sub;k++)step(1/60);
  draw();report();
  if(st.zp>TL+0.8){st.run=false;st.done=true;raf=null;
    document.getElementById('avGo').textContent='Пустить ещё раз';return;}
  raf=requestAnimationFrame(tick);
}
function reset(){
  if(raf)cancelAnimationFrame(raf);raf=null;last=0;
  dose=new Float32Array(NC);st.zp=-0.8;st.vol=0;st.tin=0;st.run=false;st.done=false;
  var b=document.getElementById('avGo');if(b)b.textContent='Пустить человека';
  draw();report();
  var el=document.getElementById('avGap');
  if(el)el.innerHTML='Нажмите «Пустить человека»: страница посчитает проход '
    +'по геометрии факелов.';
}
function go(){
  reset();
  if(RM){ // без анимации считаем проход целиком и сразу показываем итог
    while(st.zp<=TL+0.8)step(1/60);
    st.done=true;draw();report();
    document.getElementById('avGo').textContent='Пустить ещё раз';return;}
  st.run=true;last=0;raf=requestAnimationFrame(tick);
}

function seg(id,fn){
  var box=document.getElementById(id);if(!box)return;
  box.addEventListener('click',function(e){
    var b=e.target.closest('button');if(!b)return;
    [].slice.call(box.querySelectorAll('button')).forEach(function(x){
      x.setAttribute('aria-pressed',String(x===b));});
    fn(b.getAttribute('data-v'));});
}
if(c1&&c2){
  var iN=document.getElementById('avN'),iV=document.getElementById('avV'),
      iP=document.getElementById('avP');
  function labels(){
    document.getElementById('avLn').textContent=st.n;
    document.getElementById('avLv').textContent=fmt1(st.v)+' м/с';
    document.getElementById('avLp').textContent=st.p+' бар';}
  iN.addEventListener('input',function(){st.n=+iN.value;labels();reset();});
  iV.addEventListener('input',function(){st.v=+iV.value/100;labels();reset();});
  iP.addEventListener('input',function(){st.p=+iP.value;labels();reset();});
  seg('avShape',function(v){st.shape=+v;reset();});
  seg('avView',function(v){st.view=v;draw();});
  document.getElementById('avGo').addEventListener('click',go);
  var rt=null;
  window.addEventListener('resize',function(){
    clearTimeout(rt);rt=setTimeout(draw,180);});
  labels();reset();
}
"""

PAGE_JS += r"""
/* ── РАЗЛЁТ КОНСТРУКЦИИ ──────────────────────────────────────────────── */
var exp=document.getElementById('avExp');
if(exp){
  var eIn=document.getElementById('avE'),
      parts=[].slice.call(exp.querySelectorAll('g[data-part]')),
      lis=[].slice.call(exp.querySelectorAll('li[data-part]'));
  function place(){
    var e=+eIn.value/100;
    exp.style.setProperty('--xray',(0.32+0.68*e).toFixed(2));
    parts.forEach(function(g){
      var d=g.getAttribute('data-dir').split(',');
      g.setAttribute('transform','translate('+(d[0]*e).toFixed(1)+','
        +(d[1]*e).toFixed(1)+')');});}
  eIn.addEventListener('input',place);place();
  function hl(id){
    exp.classList.toggle('hl',!!id);
    parts.forEach(function(g){g.classList.toggle('on',g.getAttribute('data-part')===id);});
    lis.forEach(function(l){l.classList.toggle('on',l.getAttribute('data-part')===id);});}
  lis.forEach(function(l){
    var id=l.getAttribute('data-part');
    l.addEventListener('mouseenter',function(){hl(id);});
    l.addEventListener('focus',function(){hl(id);});
    l.addEventListener('mouseleave',function(){hl(null);});
    l.addEventListener('blur',function(){hl(null);});
    l.addEventListener('click',function(){
      if(+eIn.value<45){eIn.value=70;place();}});});
}

/* ── ПРОГИБ ЭКРАНА: жёсткость растёт как куб толщины ─────────────────── */
var thk=document.getElementById('avThk');
if(thk){
  var bends=document.getElementById('avBends'),figE=document.getElementById('avFig'),
      dropE=document.getElementById('avDrop'),
      X1=46,X2=486,YT=52,SPAN=234,TT=[4,2,1,0.5],LOG=Math.log(64);
  function curve(t){ // прогиб под собственным весом ~ 1/t²: жёсткость растёт
    var k=Math.pow(4/t,2),           // как t³, но и вес листа растёт как t.
                                     // По вертикали шкала сжата логарифмом
        d=SPAN*Math.log(k)/LOG,p='M'+X1+' '+YT,i;
    for(i=1;i<=26;i++){var u=i/26;
      p+=' L'+(X1+(X2-X1)*u).toFixed(1)+' '+(YT+d*u*u).toFixed(1);}
    return [p,k,d];}
  function setT(t){
    var s='',i,cur;
    for(i=0;i<TT.length;i++){var c=curve(TT[i]),on=TT[i]===t;
      if(on)cur=c;
      s+='<path d="'+c[0]+'" fill="none" stroke="'+(on?(t<=0.5?'#E62131':'#233563')
        :'rgba(22,24,28,.16)')+'" stroke-width="'+(on?Math.max(3,TT[i]*1.7):1.5).toFixed(1)
        +'" stroke-linecap="round"/>'
        +'<text x="516" y="'+(YT+c[2]+(c[2]<14?-9:5)).toFixed(1)+'" '
        +'font-family="PT Mono, monospace" '
        +'font-size="10" text-anchor="end" fill="'+(on?'#16181C':'rgba(22,24,28,.34)')
        +'">'+String(TT[i]).replace('.',',')+' мм</text>';}
    bends.innerHTML=s;
    var k=cur[1],kk=(k<10?fmt1(k):Math.round(k));
    dropE.textContent='вертикаль сжата логарифмом: иначе плёнка ушла бы '
      +'за кадр в 64 раза';
    figE.innerHTML=(t>=4
      ? 'Рабочая толщина. Всё остальное сравнивается с ней: <b>4 мм</b> '
        +'это единица, и экран держит форму на голове целую смену, '
        +'не ловит царапины от сумок и рукавов.'
      : 'Лист <b>'+String(t).replace('.',',')+' мм</b> провисает в <b>'+kk
        +'</b> раз'+(kk==2?'а':'')+' сильнее выбранных четырёх'
        +(t<=0.5?': такая плёнка живёт волной перед лицом и искажает обзор.'
                :': форма плывёт, и экран приходится поправлять рукой.'));}
  thk.addEventListener('click',function(e){
    var b=e.target.closest('button');if(!b)return;
    [].slice.call(thk.querySelectorAll('button')).forEach(function(x){
      x.setAttribute('aria-pressed',String(x===b));});
    setT(parseFloat(b.getAttribute('data-t')));});
  setT(4);
}

/* ── НАКЛАДКА ОГОЛОВЬЯ: печать снята, встаёт своё слово ──────────────── */
var pin=document.getElementById('avPlateI');
if(pin){
  var pt=document.getElementById('avPlateT'),pw=document.getElementById('avPlateW'),
      BX=%BAND%;
  function put(){
    var v=(pin.value||'').trim()||'TELE2';
    pt.textContent=v;
    pt.style.left=(BX[0]*100)+'%';pt.style.top=(BX[1]*100)+'%';
    pt.style.width=(BX[2]*100)+'%';pt.style.height=(BX[3]*100)+'%';
    var w=pw.clientWidth||520;
    pt.style.fontSize=Math.max(9,Math.min(w*BX[2]/(v.length*0.62),w*BX[3]*0.62))+'px';}
  pin.addEventListener('input',put);
  document.getElementById('avPlateR').addEventListener('click',function(){
    pin.value='TELE2';put();});
  window.addEventListener('resize',put);put();
}
})();</script>"""


BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creative/"},'
  '{"@type":"ListItem","position":3,"name":"Дезинфекционный тоннель AnVIT",'
  f'"item":"{URL}"}}]}}</script>')

def css():
    out = CSS1 + CSS2 + CSS3
    for k, v in (('%RED%', PAL['red']), ('%NAVY%', PAL['navy']),
                 ('%PANEL%', PAL['panel']), ('%ALU%', PAL['alu']),
                 ('%ASPH%', PAL['asphalt'])):
        out = out.replace(k, v)
    return out


def page():
    js = (PAGE_JS
          .replace('%BAND%', json.dumps(MAP['band']['logo']))
          .replace('%IMG%', IMG))
    head = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
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
            f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/tunnel.jpg">'
            '<link rel="stylesheet" href="/fonts/bitter-ysabeau.css">'
            + rc.FONT + rc.CSS + css() + METRIKA + '</head><body>')
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="av">{hero()}{spec()}{sim()}{exploded()}'
            f'{shield()}{outro()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}'
            '</body></html>')
    return head + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'creative', 'tunel')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
