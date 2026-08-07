#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/eaton_online/index.html: кейс «ONLINE трансляция EATON»
с III Глобального технологического форума OCS Distribution «IT-ОСЬ 2020»
(19 ноября 2020, онлайн).

Что было раньше: запечённая Tilda-страница — сплошной текст «задача → решение →
результат», из графики только иконки соцсетей внизу. Все цифры кейса (два канала,
70/50 Мбит, ping 7 мс, jitter 2 мс, эфир 10:30–17:30) лежали в тексте абзацем.

Идея страницы: кейс про трансляцию показать так, как его видит режиссёр — с
монитора аппаратной. Отсюда три механики:

1. Мультивью: окно ЭФИР + четыре источника, клик выводит источник в эфир,
   в шапке бежит таймкод и мигает REC (кадры считаются по-настоящему, 25 к/с).
2. Часы смены: ползунок 10:30 → 17:30 гоняет эфирное время в 60 раз быстрее
   реального и синхронно двигает таймкод, счётчик uptime и график каналов.
3. Телеметрия связи на canvas: две линии исходящего потока (основной и резерв)
   рисуются от эфирного времени. Кнопка обрывает основной канал — резерв
   подхватывает поток, счётчик обрывов эфира остаётся нулевым. Это главный
   аргумент кейса, показанный вместо описания.

Честность цифр: 70/50 Мбит, ping 7 мс, jitter 2 мс, 10:30–17:30, состав смены и
оборудование — из текста кейса. Масштаб форума (около 1500 участников, 40+
вендоров, пятичасовая программа, виртуальные стенды и демо-зоны) — из
пресс-релиза OCS и публикаций о форуме, в блоке контекста это прямо подписано.
График каналов — модель по паспортным показателям, а не запись мониторинга,
и подписан так же.

Шрифты IBM Plex Sans + IBM Plex Mono, локальные (/fonts/plex.css),
кадры готовит scripts/eaton-online-assets.py.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/eaton-online'
URL = 'https://hand-marketing.ru/eaton_online/'

# ─── паспорт проекта ────────────────────────────────────────────────────────
FACTS = [
    ('Клиент', 'Eaton'),
    ('Событие', 'Форум OCS «IT-ОСЬ 2020», 19 ноября'),
    ('Формат', 'Трансляция из офиса заказчика'),
    ('Эфир', '10:30 — 17:30 МСК'),
    ('Обрывов', '0'),
]

# ─── источники мультивью: (файл, метка, подпись под окном) ──────────────────
SOURCES = [
    ('cam1.jpg', 'КАМ 1 · СПИКЕР',
     'Первая камера держит крупный план презентующего: это основная картинка семи часов эфира.',
     'Спикеры за столом у брендволла Eaton, справа стойка с оборудованием'),
    ('cam2.jpg', 'КАМ 2 · ПУЛЬТ',
     'Микшер, внешняя звуковая карта и ноутбук с vMix: отсюда картинка уходит в сеть.',
     'Микшерный пульт Yamaha и ноутбук с программной средой vMix на столе аппаратной'),
    ('cam3.jpg', 'КАМ 3 · ПЛОЩАДКА',
     'Вторая камера на штативе: её выводили, когда акцент нужен был на оборудовании Eaton.',
     'Две камеры на штативах и световой прибор в офисе Eaton'),
    ('slide.jpg', 'ЭФИР · ПЛАТФОРМА',
     'Так поток выглядел у зрителя: спикер и презентация в окне виртуального стенда.',
     'Окно трансляции на виртуальном стенде Eaton: спикер и слайд презентации'),
]

# ─── тракт сигнала: (индекс, заголовок, состав, описание) ───────────────────
CHAIN = [
    ('Съёмка', ['Камера 1 — крупный план', 'Камера 2 — акцент на оборудовании',
                'Световые приборы', 'Петличные гарнитуры'],
     'Оператор вёл две камеры сразу: одна всё время держала презентующего, вторая '
     'подхватывала, когда нужно было показать оборудование. Свет ставили под офисный '
     'потолок, звук снимали петличками, чтобы спикер не был привязан к столу.'),
    ('Аппаратная', ['Мини-ПТС', 'Ноутбук с vMix', 'Внешняя звуковая карта',
                    'Инженер трансляции'],
     'Мини-ПТС — передвижная телевизионная станция: многокамерная съёмка и вещание в сеть '
     'с одного рабочего места. Инженер сводил картинку и звук в vMix и отвечал за весь '
     'контент, который уходил в эфир: подложки, презентации, титры.'),
    ('Связь', ['Основной канал', 'Резервный канал', 'Роутер с автопереключением'],
     'Своего интернета для вещания в офисе не было. Завели два независимых внешних канала '
     'мобильного интернета и подняли их на одном роутере: основной и резервный. '
     'При проблеме с основным система переключается на резерв сама.'),
    ('Платформа', ['Виртуальный стенд Eaton', 'Демо-зона', 'Чат и вопросы из зала'],
     'Поток уходил на площадку форума, в окно виртуального стенда Eaton. Там же зритель '
     'скачивал материалы, заходил в демо-зону и задавал вопросы: связь работала в обе '
     'стороны, поэтому канал нужен был широкий не только на отдачу.'),
]

# ─── контекст форума (по данным OCS) ────────────────────────────────────────
FORUM = [
    ('≈1500', 'участников из городов России и других стран'),
    ('40+', 'вендоров со своими стендами на площадке'),
    ('5 часов', 'шла программа форума'),
    ('19.11.2020', 'третий форум OCS «IT-ОСЬ», полностью онлайн'),
]

# ─── показатели канала из кейса ─────────────────────────────────────────────
LINK = [
    ('in', '70', 'Mbit/sec'),
    ('out', '50', 'Mbit/sec'),
    ('ping', '7', 'ms'),
    ('jitter', '2', 'ms'),
]

PAGE_CSS = """<style id="eo-css">
:root{
 --eo-bg:#0A0D12; --eo-bg2:#0F141C; --eo-panel:#151C26; --eo-line:rgba(255,255,255,.12);
 --eo-txt:#E8EDF5; --eo-dim:#93A1B5; --eo-red:#FF3B2F; --eo-amber:#FF7A18;
 --eo-blue:#0071CE; --eo-ok:#25D07A;
}
.eo{font-family:'IBM Plex Sans',-apple-system,Arial,sans-serif;color:var(--eo-txt);
 background:var(--eo-bg);-webkit-font-smoothing:antialiased;overflow-x:clip;
 background-image:radial-gradient(120% 80% at 50% 0,rgba(255,122,24,.10),transparent 60%)}
.eo *{box-sizing:border-box}
.eo img{max-width:100%;height:auto;display:block}
.eo h1,.eo h2,.eo h3{font-weight:600;letter-spacing:-.02em;margin:0;line-height:1.08}
.eo p{margin:0}
.eo__wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.eo__mono{font-family:'IBM Plex Mono',ui-monospace,Menlo,monospace}
.eo__eyebrow{font-family:'IBM Plex Mono',ui-monospace,Menlo,monospace;font-size:12px;
 letter-spacing:.18em;text-transform:uppercase;color:var(--eo-amber)}
.eo__lead{font-size:clamp(16px,1.5vw,19px);line-height:1.6;color:var(--eo-dim)}
.eo-sec{padding:clamp(56px,7vw,110px) 0;position:relative}
.eo-sec__h{font-size:clamp(26px,3.4vw,46px);max-width:20ch}
.eo-sec__sub{margin-top:22px;max-width:64ch;font-size:clamp(15px,1.3vw,17px);
 line-height:1.7;color:var(--eo-dim)}
.eo-r{opacity:0;transform:translateY(18px);transition:opacity .7s ease,transform .7s ease}
.eo-r.in{opacity:1;transform:none}
.eo-note{margin-top:14px;font-size:12.5px;line-height:1.5;color:#6F7D91}

/* ── ГЕРОЙ ── */
.eo-hero{padding:clamp(20px,3vw,40px) 0 clamp(40px,5vw,72px)}
.eo-back{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:500;
 color:var(--eo-dim);text-decoration:none;margin-bottom:clamp(22px,3.4vw,44px)}
.eo-back:hover{color:var(--eo-amber)}
.eo-hero__grid{display:grid;grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr);
 gap:clamp(24px,3.4vw,54px);align-items:center}
.eo-hero h1{font-size:clamp(30px,4.6vw,60px);margin:14px 0 0}
.eo-hero h1 em{font-style:normal;color:var(--eo-amber)}
.eo-hero__lead{margin-top:20px;max-width:44ch}
.eo-facts{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--eo-line);
 border:1px solid var(--eo-line);margin-top:clamp(28px,4vw,52px)}
.eo-facts div{background:var(--eo-bg2);padding:16px 15px}
.eo-facts dt{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
 letter-spacing:.14em;text-transform:uppercase;color:#6F7D91}
.eo-facts dd{margin:8px 0 0;font-size:clamp(14px,1.25vw,17px);line-height:1.3;font-weight:500}

/* ── МУЛЬТИВЬЮ ── */
.eo-mv{background:var(--eo-panel);border:1px solid var(--eo-line);border-radius:6px;
 padding:12px;box-shadow:0 40px 80px -50px #000}
.eo-mv__bar{display:flex;align-items:center;gap:12px;padding:2px 4px 11px;
 font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;color:var(--eo-dim);
 letter-spacing:.06em}
.eo-mv__rec{display:inline-flex;align-items:center;gap:6px;color:var(--eo-red);font-weight:600}
.eo-mv__rec i{width:8px;height:8px;border-radius:50%;background:var(--eo-red);
 animation:eo-blink 1.6s steps(1,end) infinite}
@keyframes eo-blink{0%,55%{opacity:1}56%,100%{opacity:.16}}
.eo-mv__src{color:var(--eo-txt)}
.eo-mv__tc{margin-left:auto;color:var(--eo-txt);font-variant-numeric:tabular-nums}
.eo-mv__pgm{position:relative;aspect-ratio:16/9;background:#05070A;overflow:hidden;
 border:1px solid rgba(255,255,255,.08)}
.eo-mv__pgm img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 opacity:0;transition:opacity .32s ease}
.eo-mv__pgm img.is-on{opacity:1}
.eo-mv__air{position:absolute;left:10px;top:10px;padding:4px 9px;background:var(--eo-red);
 color:#fff;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
 letter-spacing:.16em;font-weight:600}
.eo-mv__vu{position:absolute;right:10px;top:10px;bottom:10px;width:16px;display:flex;
 gap:4px;align-items:flex-end}
.eo-mv__vu i{flex:1;background:linear-gradient(180deg,var(--eo-red),var(--eo-amber) 34%,var(--eo-ok) 70%);
 height:30%;transform-origin:bottom;border-radius:1px;opacity:.85}
.eo-mv__row{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}
.eo-mv__btn{position:relative;padding:0;border:1px solid rgba(255,255,255,.12);background:#05070A;
 cursor:pointer;overflow:hidden;aspect-ratio:16/9;display:block;transition:border-color .2s}
.eo-mv__btn img{width:100%;height:100%;object-fit:cover;opacity:.5;transition:opacity .2s}
.eo-mv__btn:hover img{opacity:.8}
.eo-mv__btn.is-on{border-color:var(--eo-red)}
.eo-mv__btn.is-on img{opacity:1}
.eo-mv__btn span{position:absolute;left:0;right:0;bottom:0;padding:8px 6px 4px;
 font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.5px;letter-spacing:.08em;
 color:#fff;background:linear-gradient(180deg,transparent,rgba(5,7,10,.9));text-align:left}
.eo-mv__cap{margin-top:10px;font-size:13px;line-height:1.5;color:var(--eo-dim);min-height:2.9em}
.eo-mv__cap b{color:var(--eo-txt);font-weight:500}

/* ── ЗАДАЧА ── */
.eo-task{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
 gap:clamp(24px,3.6vw,60px)}
.eo-task p+p{margin-top:16px}
.eo-task p{font-size:clamp(15px,1.35vw,17px);line-height:1.7;color:var(--eo-dim)}
.eo-task b{color:var(--eo-txt);font-weight:600}
.eo-quote{border-left:2px solid var(--eo-amber);padding:4px 0 4px 20px;
 font-size:clamp(17px,1.7vw,22px);line-height:1.45;letter-spacing:-.01em}

/* ── ФОРУМ ── */
.eo-forum{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--eo-line);
 border:1px solid var(--eo-line);margin-top:clamp(26px,3.6vw,44px)}
.eo-forum div{background:var(--eo-bg2);padding:20px 18px}
.eo-forum b{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:clamp(20px,2.3vw,29px);font-weight:600;color:var(--eo-amber);letter-spacing:-.02em}
.eo-forum span{display:block;margin-top:8px;font-size:13px;line-height:1.45;color:var(--eo-dim)}
.eo-shots{display:grid;grid-template-columns:minmax(0,.62fr) minmax(0,1fr);gap:14px;
 margin-top:clamp(22px,3vw,38px)}
.eo-fig{margin:0;border:1px solid var(--eo-line);background:var(--eo-bg2)}
.eo-fig img{width:100%}
.eo-fig figcaption{padding:11px 13px;font-size:12.5px;line-height:1.45;color:var(--eo-dim)}

/* ── ТРАКТ ── */
.eo-chain{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;
 margin-top:clamp(26px,3.6vw,46px)}
.eo-node{position:relative;text-align:left;background:var(--eo-bg2);border:1px solid var(--eo-line);
 padding:18px 16px 16px;cursor:pointer;color:inherit;font:inherit;transition:border-color .2s,background .2s}
.eo-node:hover{border-color:rgba(255,122,24,.55)}
.eo-node.is-on{border-color:var(--eo-amber);background:#151C26}
.eo-node__n{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;color:var(--eo-amber);
 letter-spacing:.14em}
.eo-node h3{margin-top:9px;font-size:clamp(16px,1.5vw,20px)}
.eo-node ul{margin:12px 0 0;padding:0;list-style:none}
.eo-node li{position:relative;padding-left:14px;font-size:13px;line-height:1.65;color:var(--eo-dim)}
.eo-node li::before{content:'';position:absolute;left:0;top:.62em;width:5px;height:5px;
 background:var(--eo-amber);opacity:.7}
.eo-node::after{content:'';position:absolute;right:-12px;top:50%;width:12px;height:1px;
 background:linear-gradient(90deg,var(--eo-amber),rgba(255,122,24,.15));z-index:1}
.eo-chain>.eo-node:last-child::after{display:none}
.eo-chain__flow{position:absolute;right:-12px;top:50%;width:12px;height:3px;margin-top:-1px;
 pointer-events:none}
.eo-desc{margin-top:14px;border:1px solid var(--eo-line);border-left:2px solid var(--eo-amber);
 background:var(--eo-bg2);padding:18px 20px;font-size:clamp(14px,1.3vw,16px);line-height:1.7;
 color:var(--eo-dim);min-height:6.2em}
.eo-desc b{color:var(--eo-txt);font-weight:600}

/* ── СВЯЗЬ / ТЕЛЕМЕТРИЯ ── */
.eo-net{margin-top:clamp(26px,3.6vw,44px);border:1px solid var(--eo-line);background:var(--eo-bg2)}
.eo-net__top{display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;padding:14px 18px;
 border-bottom:1px solid var(--eo-line);font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:11.5px;letter-spacing:.06em;color:var(--eo-dim)}
.eo-net__st{display:inline-flex;align-items:center;gap:8px;color:var(--eo-ok);font-weight:600}
.eo-net__st i{width:8px;height:8px;border-radius:50%;background:currentColor}
.eo-net.is-fail .eo-net__st{color:var(--eo-amber)}
.eo-net__up{margin-left:auto;color:var(--eo-txt);font-variant-numeric:tabular-nums}
.eo-canvas{display:block;width:100%;height:240px;background:#0A0D12}
.eo-net__legend{display:flex;flex-wrap:wrap;gap:8px 22px;padding:12px 18px;
 border-top:1px solid var(--eo-line);font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:11px;color:var(--eo-dim);letter-spacing:.04em}
.eo-net__legend span{display:inline-flex;align-items:center;gap:7px}
.eo-net__legend i{width:16px;height:2px;background:currentColor}
.eo-net__legend .a{color:var(--eo-amber)}
.eo-net__legend .b{color:var(--eo-blue)}
.eo-net__act{display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:14px 18px;
 border-top:1px solid var(--eo-line)}
.eo-btn{font:600 13px 'IBM Plex Sans',Arial,sans-serif;padding:11px 18px;cursor:pointer;
 background:var(--eo-red);color:#fff;border:0;letter-spacing:.01em;transition:transform .15s,filter .2s}
.eo-btn:hover{transform:translateY(-1px);filter:brightness(1.08)}
.eo-btn--ghost{background:transparent;border:1px solid var(--eo-line);color:var(--eo-txt)}
.eo-net__hint{font-size:12.5px;line-height:1.5;color:#6F7D91;max-width:52ch}
.eo-link{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--eo-line);
 border:1px solid var(--eo-line);border-top:0}
.eo-link div{background:var(--eo-bg2);padding:15px 16px}
.eo-link dt{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
 letter-spacing:.14em;text-transform:uppercase;color:#6F7D91}
.eo-link dd{margin:6px 0 0;font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:clamp(18px,2vw,25px);font-weight:600;letter-spacing:-.02em}
.eo-link dd small{font-size:11.5px;font-weight:400;color:var(--eo-dim);margin-left:6px;letter-spacing:0}

/* ── ЧАСЫ СМЕНЫ ── */
.eo-clock{margin-top:clamp(26px,3.6vw,44px);border:1px solid var(--eo-line);background:var(--eo-bg2);
 padding:clamp(18px,2.4vw,26px)}
.eo-clock__head{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 20px}
.eo-clock__tc{font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:clamp(30px,5vw,58px);font-weight:600;letter-spacing:-.03em;
 font-variant-numeric:tabular-nums;line-height:1}
.eo-clock__st{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12px;
 letter-spacing:.1em;color:var(--eo-amber);text-transform:uppercase}
.eo-clock__up{margin-left:auto;font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:12px;color:var(--eo-dim);letter-spacing:.06em}
.eo-scrub{margin-top:20px;position:relative}
.eo-scrub input{-webkit-appearance:none;appearance:none;width:100%;height:34px;background:transparent;
 cursor:pointer;display:block;margin:0}
.eo-scrub input::-webkit-slider-runnable-track{height:34px;background:
 linear-gradient(90deg,rgba(255,122,24,.5),rgba(255,122,24,.5)) 0/var(--p,0%) 100% no-repeat,#0A0D12;
 border:1px solid var(--eo-line)}
.eo-scrub input::-moz-range-track{height:34px;background:#0A0D12;border:1px solid var(--eo-line)}
.eo-scrub input::-moz-range-progress{height:34px;background:rgba(255,122,24,.5)}
.eo-scrub input::-webkit-slider-thumb{-webkit-appearance:none;width:4px;height:44px;
 background:var(--eo-red);border:0;margin-top:-6px;box-shadow:0 0 0 1px #0A0D12}
.eo-scrub input::-moz-range-thumb{width:4px;height:44px;background:var(--eo-red);border:0;border-radius:0}
.eo-scrub__marks{display:flex;justify-content:space-between;margin-top:8px;
 font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;color:#6F7D91;letter-spacing:.04em}
.eo-clock__hint{margin-top:14px;font-size:12.5px;line-height:1.55;color:#6F7D91;max-width:60ch}

/* ── СМЕНА ── */
.eo-crew{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:clamp(24px,3.4vw,42px)}
.eo-kit{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--eo-line);
 border:1px solid var(--eo-line);margin-top:14px}
.eo-kit div{background:var(--eo-bg2);padding:14px 16px}
.eo-kit dt{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
 letter-spacing:.13em;text-transform:uppercase;color:var(--eo-amber)}
.eo-kit dd{margin:6px 0 0;font-size:13.5px;line-height:1.55;color:var(--eo-dim)}

/* ── ИТОГ ── */
.eo-end{border-top:1px solid var(--eo-line);padding-top:clamp(28px,4vw,54px);
 display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,3.4vw,56px)}
.eo-big{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:clamp(46px,8vw,104px);
 font-weight:600;line-height:.94;letter-spacing:-.04em;color:var(--eo-amber)}
.eo-big small{display:block;margin-top:16px;font-family:'IBM Plex Sans',Arial,sans-serif;
 font-size:clamp(14px,1.35vw,16px);font-weight:400;line-height:1.65;color:var(--eo-dim);
 letter-spacing:0;max-width:38ch}
.eo-end p+p{margin-top:14px}
.eo-end p{font-size:clamp(15px,1.35vw,17px);line-height:1.7;color:var(--eo-dim)}

/* ── ПЛАНШЕТ ── */
@media (max-width:980px){
 .eo-hero__grid{grid-template-columns:1fr;gap:26px}
 .eo-hero__lead{max-width:none}
 .eo-facts{grid-template-columns:repeat(3,1fr)}
 .eo-facts div:last-child{grid-column:1/-1}
 .eo-task{grid-template-columns:1fr;gap:22px}
 .eo-forum{grid-template-columns:repeat(2,1fr)}
 .eo-chain{grid-template-columns:repeat(2,1fr)}
 .eo-node::after{display:none}
 .eo-end{grid-template-columns:1fr;gap:24px}
}
/* ── ТЕЛЕФОН ── */
@media (max-width:640px){
 .eo__wrap{padding:0 18px}
 .eo-facts{grid-template-columns:repeat(2,1fr)}
 .eo-forum{grid-template-columns:1fr}
 .eo-shots{grid-template-columns:1fr}
 .eo-chain{grid-template-columns:1fr;gap:8px}
 .eo-crew{grid-template-columns:1fr}
 .eo-kit{grid-template-columns:1fr}
 .eo-link{grid-template-columns:repeat(2,1fr)}
 .eo-mv{padding:8px}
 .eo-mv__row{gap:5px}
 .eo-mv__btn span{font-size:8px;padding:6px 4px 3px}
 .eo-mv__bar{gap:8px;font-size:10.5px}
 .eo-canvas{height:190px}
 .eo-net__up{margin-left:0;width:100%}
 .eo-net__act{gap:9px}
 .eo-btn{width:100%;text-align:center}
 .eo-net__hint{max-width:none}
}
/* ── ЛАНДШАФТ ТЕЛЕФОНА ── */
@media (max-height:460px) and (orientation:landscape){
 .eo-sec{padding:44px 0}
 .eo-canvas{height:170px}
 .eo-clock__tc{font-size:clamp(26px,4.4vw,40px)}
}
@media (prefers-reduced-motion:reduce){
 .eo-r{opacity:1;transform:none;transition:none}
 .eo-mv__rec i{animation:none}
}
</style>"""


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ─── секции ─────────────────────────────────────────────────────────────────
def multiview():
    pgm = ''.join(
        f'<img src="{IMG}/{f}" width="960" height="540" alt="{esc(alt)}"'
        f'{" class=is-on" if i == 0 else ""}'
        f'{" fetchpriority=high" if i == 0 else " loading=lazy"} decoding="async">'
        for i, (f, label, _cap, alt) in enumerate(SOURCES))
    btns = ''.join(
        f'<button class="eo-mv__btn{" is-on" if i == 0 else ""}" type="button" data-i="{i}"'
        f' aria-label="Вывести в эфир: {esc(label)}">'
        f'<img src="{IMG}/{f}" width="480" height="270" loading="lazy" decoding="async" alt="">'
        f'<span>{esc(label)}</span></button>'
        for i, (f, label, _cap, _alt) in enumerate(SOURCES))
    vu = ''.join('<i></i>' for _ in range(2))
    return f'''<div class="eo-mv" id="eoMv">
<div class="eo-mv__bar"><span class="eo-mv__rec"><i></i>REC</span>
<span class="eo-mv__src" id="eoMvSrc">{esc(SOURCES[0][1])}</span>
<span class="eo-mv__tc" id="eoMvTc">10:30:00:00</span></div>
<div class="eo-mv__pgm">{pgm}<div class="eo-mv__air">В ЭФИРЕ</div>
<div class="eo-mv__vu" id="eoVu" aria-hidden="true">{vu}</div></div>
<div class="eo-mv__row">{btns}</div>
<p class="eo-mv__cap" id="eoMvCap"><b>{esc(SOURCES[0][1])}.</b> {esc(SOURCES[0][2])}</p>
</div>'''


def hero():
    facts = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in FACTS)
    return f'''<section class="eo-hero"><div class="eo__wrap">
<a class="eo-back" href="/project">← Проекты</a>
<div class="eo-hero__grid">
<div><div class="eo__eyebrow">Event · онлайн-трансляция</div>
<h1>Семь часов эфира из офиса, куда <em>не завели интернет</em></h1>
<p class="eo__lead eo-hero__lead">Eaton выступал на третьем форуме OCS Distribution
«IT-ОСЬ 2020». Форум прошёл полностью онлайн, а спикер остался у себя в офисе:
мы собрали там аппаратную и вели трансляцию на площадку форума с 10:30 до 17:30.</p></div>
{multiview()}
</div>
<dl class="eo-facts">{facts}</dl>
</div></section>'''


def task():
    forum = ''.join(f'<div><b>{esc(n)}</b><span>{esc(t)}</span></div>' for n, t in FORUM)
    return f'''<section class="eo-sec"><div class="eo__wrap">
<div class="eo-task eo-r">
<div><div class="eo__eyebrow">Задача</div>
<h2 class="eo-sec__h" style="margin-top:14px">Вывести спикера на форум,
не вывозя его из офиса</h2></div>
<div>
<p>Осенью 2020 года форум, который два года подряд собирал зал в Центре международной
торговли, перенесли в онлайн. Стенды вендоров стали виртуальными, выступления шли
потоком, и каждому участнику нужно было откуда-то вещать.</p>
<p><b>Eaton решил выступать из собственного офиса.</b> Значит, офис на день превращается
в студию: свет, звук, две камеры, аппаратная и, главное, канал связи, которого хватит
на семь часов непрерывной отдачи.</p>
<p class="eo-quote">«Организовать online-трансляцию из офиса заказчика для участия
в форуме. Организовать отдельный интернет-канал вещания».</p>
<p class="eo-note">Формулировка задачи из брифа.</p>
</div></div>
<div class="eo-r"><div class="eo-forum">{forum}</div>
<p class="eo-note">Масштаб площадки — по данным OCS Distribution об итогах форума
«IT-ОСЬ 2020».</p></div>
<div class="eo-shots eo-r">
<figure class="eo-fig"><img src="{IMG}/forum-hall.jpg" width="794" height="571"
 loading="lazy" decoding="async"
 alt="3D-визуализация зала форума IT-ОСЬ 2020: виртуальные стенды вендоров, среди них Eaton">
<figcaption>Виртуальный зал форума: стенды вендоров стоят так же, как стояли бы
в павильоне.</figcaption></figure>
<figure class="eo-fig"><img src="{IMG}/forum-stand.jpg" width="1280" height="539"
 loading="lazy" decoding="async"
 alt="Виртуальный стенд Eaton на форуме: окно трансляции, кнопки демо-зоны, чат с менеджером">
<figcaption>Стенд Eaton. В центре — окно, в которое уходил наш поток; рядом кнопки
демо-зоны, розыгрыша и видеозвонка с вендором.</figcaption></figure>
</div>
</div></section>'''


def chain():
    nodes = ''.join(
        f'<button class="eo-node{" is-on" if i == 0 else ""}" type="button" data-i="{i}">'
        f'<span class="eo-node__n">0{i + 1}</span><h3>{esc(title)}</h3>'
        + '<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in items) + '</ul></button>'
        for i, (title, items, _d) in enumerate(CHAIN))
    return f'''<section class="eo-sec"><div class="eo__wrap">
<div class="eo-r"><div class="eo__eyebrow">Решение · тракт</div>
<h2 class="eo-sec__h" style="margin-top:14px">Путь картинки: от объектива
до вопроса в чате</h2>
<p class="eo-sec__sub">Подобрали оборудование и людей под задачу и собрали из них
цепочку. Нажмите на ступень, чтобы посмотреть, что на ней происходило.</p></div>
<div class="eo-chain eo-r">{nodes}</div>
<p class="eo-desc eo-r" id="eoChainDesc">{esc(CHAIN[0][2])}</p>
</div></section>'''


def net():
    link = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}<small>{esc(u)}</small></dd></div>'
                   for k, v, u in LINK)
    return f'''<section class="eo-sec"><div class="eo__wrap">
<div class="eo-r"><div class="eo__eyebrow">Решение · связь</div>
<h2 class="eo-sec__h" style="margin-top:14px">Канал, которого в офисе не было</h2>
<p class="eo-sec__sub">Доступ к корпоративной сети нам не дали, а трансляции нужен
был свой канал: семь часов зрителям отдавали большой объём информации, и они же
задавали вопросы обратно. Поэтому в офис завели два независимых канала мобильного
интернета и подняли их на одном роутере — основной и резервный. Если основной падает,
система переключается на резерв сама, эфир этого не замечает.</p></div>
<div class="eo-net eo-r" id="eoNet">
 <div class="eo-net__top">
  <span class="eo-net__st" id="eoNetSt"><i></i>ОСНОВНОЙ КАНАЛ · В ЭФИРЕ</span>
  <span>ИСХОДЯЩИЙ ПОТОК, Mbit/sec</span>
  <span class="eo-net__up" id="eoNetUp">ОБРЫВОВ ЭФИРА: 0</span>
 </div>
 <canvas class="eo-canvas" id="eoCanvas" width="1160" height="240"
  role="img" aria-label="График исходящего потока по основному и резервному каналам"></canvas>
 <div class="eo-net__legend">
  <span class="a"><i></i>основной канал</span>
  <span class="b"><i></i>резервный канал</span>
  <span>порог вещания 12 Mbit/sec</span>
 </div>
 <div class="eo-net__act">
  <button class="eo-btn" type="button" id="eoFail">Оборвать основной канал</button>
  <button class="eo-btn eo-btn--ghost" type="button" id="eoBack" hidden>Вернуть основной</button>
  <span class="eo-net__hint" id="eoNetHint">Так выглядела бы авария на площадке.
  Нажмите — и посмотрите, что увидит зритель.</span>
 </div>
 <dl class="eo-link">{link}</dl>
</div>
<p class="eo-note eo-r">Показатели каналов — из замеров на площадке. Сам график —
модель по этим показателям, а не запись мониторинга: логи трансляции 2020 года
не сохранились.</p>
</div></section>'''


def clock():
    marks = ''.join(f'<span>{h}:30</span>' for h in range(10, 18))
    return f'''<section class="eo-sec"><div class="eo__wrap">
<div class="eo-r"><div class="eo__eyebrow">Смена</div>
<h2 class="eo-sec__h" style="margin-top:14px">10:30 → 17:30, без перерывов</h2>
<p class="eo-sec__sub">Трансляция началась в 10:30 по московскому времени и
закончилась в 17:30 — семь часов в эфире без прерываний и сбоев. Программа самого
форума занимала около пяти часов; остальное — подключения, паузы между блоками
и вопросы, на которые отвечали в прямом эфире.</p></div>
<div class="eo-clock eo-r" id="eoClock">
 <div class="eo-clock__head">
  <span class="eo-clock__tc" id="eoClockTc">10:30</span>
  <span class="eo-clock__st" id="eoClockSt">в эфире</span>
  <span class="eo-clock__up" id="eoClockUp">UPTIME 00:00:00</span>
 </div>
 <div class="eo-scrub">
  <input type="range" id="eoScrub" min="0" max="25200" step="1" value="0"
   aria-label="Время эфира, от 10:30 до 17:30">
 </div>
 <div class="eo-scrub__marks">{marks}</div>
 <p class="eo-clock__hint">Ползунок гонит эфирное время: вместе с ним идёт таймкод
 в аппаратной наверху и график каналов выше. Сам по себе эфир проигрывается в 60 раз
 быстрее реального.</p>
</div>
</div></section>'''


def crew():
    kit = [
        ('Оператор', 'Держал две камеры: крупный план презентующего и акцент '
                     'на презентационном оборудовании.'),
        ('Инженер трансляции', 'Отвечал за весь контент, который уходил в эфир, '
                               'и за сведение картинки со звуком.'),
        ('Мини-ПТС', 'Передвижная станция для многокамерной съёмки с параллельной '
                     'трансляцией в сеть.'),
        ('vMix', 'Программная среда вещания на ноутбуке: переключение источников, '
                 'титры, презентации.'),
        ('Звук', 'Внешняя звуковая карта, микшер и петличные гарнитуры на спикерах.'),
        ('Свет', 'Приборы под офисный потолок, чтобы кадр не выглядел переговоркой.'),
    ]
    items = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in kit)
    return f'''<section class="eo-sec"><div class="eo__wrap">
<div class="eo-r"><div class="eo__eyebrow">Площадка</div>
<h2 class="eo-sec__h" style="margin-top:14px">Офис, который на день стал студией</h2></div>
<div class="eo-crew eo-r">
<figure class="eo-fig"><img src="{IMG}/shift-desk.jpg" width="1280" height="720"
 loading="lazy" decoding="async"
 alt="Аппаратная в офисе Eaton: спикеры за столом у брендволла, стойка с оборудованием, камера">
<figcaption>Брендволл, стол спикеров, стойка с оборудованием и камера — всё
в одном офисном помещении.</figcaption></figure>
<figure class="eo-fig"><img src="{IMG}/shift-rack.jpg" width="1280" height="960"
 loading="lazy" decoding="async"
 alt="Рабочее место инженера трансляции: микшер Yamaha, ноутбук с vMix, кейсы, камеры на штативах">
<figcaption>Рабочее место инженера: микшер, ноутбук с vMix, контрольный монитор.
Слева — кейсы, в которых всё это приехало.</figcaption></figure>
</div>
<dl class="eo-kit eo-r">{items}</dl>
</div></section>'''


def finale():
    return f'''<section class="eo-sec"><div class="eo__wrap">
<div class="eo-end eo-r">
<div><div class="eo-big">0<small>Обрывов эфира за семь часов. Трансляция началась
в 10:30 и закончилась в 17:30 по московскому времени без прерываний и сбоев.</small></div></div>
<div>
<p>Зрители форума видели спикера Eaton в окне виртуального стенда и могли тут же
задать вопрос, скачать материалы или уйти в демо-зону. Ни один из них не знал,
что картинка идёт из обычного офиса на двух каналах мобильного интернета.</p>
<p>Такую же схему мы собираем под любое выступление, которое нельзя перенести
в студию: конференция, годовое собрание, запуск продукта, обучение дилеров.</p>
</div></div>
</div></section>'''


PAGE_JS = """<script>(function(){
var d=document,RM=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;

// появление секций
var io=window.IntersectionObserver?new IntersectionObserver(function(es){
 es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});
},{rootMargin:'0px 0px -8% 0px'}):null;
[].forEach.call(d.querySelectorAll('.eo-r'),function(n){io?io.observe(n):n.classList.add('in');});

// ── общее эфирное время: 0..25200 с (10:30 → 17:30), идёт в 60 раз быстрее ──
var T=0,MAX=25200,SPEED=60,last=0,held=false;
var CAPS=[__CAPS__];
var tcEl=d.getElementById('eoMvTc'),srcEl=d.getElementById('eoMvSrc'),capEl=d.getElementById('eoMvCap'),
    clockTc=d.getElementById('eoClockTc'),clockUp=d.getElementById('eoClockUp'),
    clockSt=d.getElementById('eoClockSt'),
    scrub=d.getElementById('eoScrub'),
    pgm=[].slice.call(d.querySelectorAll('.eo-mv__pgm img')),
    btns=[].slice.call(d.querySelectorAll('.eo-mv__btn')),
    vu=[].slice.call(d.querySelectorAll('.eo-mv__vu i'));

function p2(n){return (n<10?'0':'')+n;}
function airTime(t){var s=Math.floor(t)+37800;/* 10:30:00 в секундах */
 return p2(Math.floor(s/3600)%24)+':'+p2(Math.floor(s/60)%60)+':'+p2(Math.floor(s)%60);}

// ── мультивью: клик выводит источник в эфир ──
var cur=0,autoAt=0;
function put(i,manual){
 if(i===cur&&manual)return;
 cur=i;
 pgm.forEach(function(n,k){n.classList.toggle('is-on',k===i);});
 btns.forEach(function(n,k){n.classList.toggle('is-on',k===i);});
 if(srcEl)srcEl.textContent=CAPS[i][0];
 if(capEl)capEl.innerHTML='<b>'+CAPS[i][0]+'.</b> '+CAPS[i][1];
 if(manual)held=true;
}
btns.forEach(function(b){b.addEventListener('click',function(){put(+b.getAttribute('data-i'),true);});});

// ── телеметрия каналов ──
var cv=d.getElementById('eoCanvas'),net=d.getElementById('eoNet'),
    stEl=d.getElementById('eoNetSt'),hintEl=d.getElementById('eoNetHint'),
    failBtn=d.getElementById('eoFail'),backBtn=d.getElementById('eoBack'),
    ctx=cv?cv.getContext('2d'):null,failT=-1,WIN=900,DPRK=1; // окно графика: 15 минут эфира
function noise(x){var s=Math.sin(x*12.9898)*43758.5453;return s-Math.floor(s);}
function sn(x){                        // сглаженный шум: линия дышит, а не пилит
 var i=Math.floor(x),f=x-i,a=noise(i),b=noise(i+1);
 return a+(b-a)*f*f*(3-2*f);
}
// исходящий поток канала в момент эфирного времени t (Mbit/sec).
// t<0 это «до начала эфира»: модель зеркалим, чтобы график не начинался с пустоты.
function flow(t,main){
 var x=t<0?-t:t,k=main?0:7.3,n=(sn(x/6+k)-.5)*10+(sn(x/29+k)-.5)*7;
 if(failT>=0&&t>=failT){
  if(main)return 0;
  return (43+n*.6)*Math.min(1,(t-failT)/5);   // резерв поднимается за пять секунд
 }
 if(!main)return 1.3+Math.abs(n)*.22;         // резерв ждёт вхолостую
 return 44+n;
}
function draw(){
 if(!ctx)return;
 var W=cv.width,H=cv.height,t1=T,t0=T-WIN,MAXY=64;
 ctx.clearRect(0,0,W,H);
 // сетка
 ctx.strokeStyle='rgba(255,255,255,.07)';ctx.lineWidth=1;
 for(var g=0;g<=4;g++){var y=Math.round(H-H*g/4)+.5;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
 // порог вещания 12 Mbit/sec
 var yt=H-12/MAXY*H;
 ctx.strokeStyle='rgba(255,255,255,.22)';ctx.setLineDash([4,5]);
 ctx.beginPath();ctx.moveTo(0,yt);ctx.lineTo(W,yt);ctx.stroke();ctx.setLineDash([]);
 function line(main,color,fill){
  ctx.beginPath();
  for(var i=0;i<=W;i+=2){
   var t=t0+(t1-t0)*i/W,v=Math.max(0,flow(t,main)),y=H-v/MAXY*H;
   i?ctx.lineTo(i,y):ctx.moveTo(i,y);
  }
  ctx.strokeStyle=color;ctx.lineWidth=2*DPRK;ctx.stroke();
  if(fill){ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.closePath();ctx.fillStyle=fill;ctx.fill();}
 }
 line(false,'#3E93E0','rgba(0,113,206,.16)');
 line(true,'#FF7A18','rgba(255,122,24,.14)');
 // момент переключения на резерв
 if(failT>=0&&failT>t0&&failT<t1){
  var xf=Math.round((failT-t0)/(t1-t0)*W)+.5;
  ctx.strokeStyle='rgba(255,255,255,.5)';ctx.setLineDash([3*DPRK,4*DPRK]);
  ctx.beginPath();ctx.moveTo(xf,0);ctx.lineTo(xf,H);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='rgba(232,237,245,.8)';ctx.font=(10.5*DPRK)+'px "IBM Plex Mono",monospace';
  ctx.fillText('переключение', Math.min(xf+6*DPRK, W-96*DPRK), 30*DPRK);
 }
 // подпись шкалы
 ctx.fillStyle='rgba(147,161,181,.75)';ctx.font=(11*DPRK)+'px "IBM Plex Mono",monospace';
 ctx.fillText('64',6*DPRK,14*DPRK);ctx.fillText('0',6*DPRK,H-6*DPRK);
}

if(failBtn)failBtn.addEventListener('click',function(){
 failT=T;net.classList.add('is-fail');
 stEl.innerHTML='<i></i>РЕЗЕРВНЫЙ КАНАЛ · В ЭФИРЕ';
 hintEl.textContent='Основной канал упал. Роутер отдал поток резервному, зритель '+
  'на площадке форума ничего не заметил: счётчик обрывов эфира остался нулевым.';
 failBtn.hidden=true;backBtn.hidden=false;
});
if(backBtn)backBtn.addEventListener('click',function(){
 failT=-1;net.classList.remove('is-fail');
 stEl.innerHTML='<i></i>ОСНОВНОЙ КАНАЛ · В ЭФИРЕ';
 hintEl.textContent='Основной канал вернулся. Резерв снова ждёт вхолостую.';
 backBtn.hidden=true;failBtn.hidden=false;
});

// ── ползунок смены ──
function scrubPaint(){
 if(!scrub)return;
 scrub.style.setProperty('--p',(T/MAX*100).toFixed(2)+'%');
}
if(scrub)scrub.addEventListener('input',function(){T=+scrub.value;held=true;paint();});

var frames=0;
function paint(){
 if(tcEl)tcEl.textContent=airTime(T)+':'+p2(frames);
 if(clockTc)clockTc.textContent=airTime(T).slice(0,5);
 if(clockUp)clockUp.textContent='UPTIME '+p2(Math.floor(T/3600))+':'+
  p2(Math.floor(T/60)%60)+':'+p2(Math.floor(T)%60);
 if(clockSt)clockSt.textContent=T>=MAX-30?'эфир окончен':(T<45?'выходим в эфир':'в эфире');
 scrubPaint();
 if(netVis)draw();
}

// ── общий цикл ──
var netVis=true;
if(window.IntersectionObserver&&cv){
 new IntersectionObserver(function(es){netVis=es[0].isIntersecting;},
  {rootMargin:'120px'}).observe(cv);
}
function fit(){                       // canvas под ширину блока и плотность экрана
 if(!cv)return;
 var r=cv.getBoundingClientRect(),k=Math.min(2,window.devicePixelRatio||1);
 var w=Math.round(r.width*k),h=Math.round(r.height*k);
 DPRK=k;
 if(w&&h&&(cv.width!==w||cv.height!==h)){cv.width=w;cv.height=h;}
}
fit();window.addEventListener('resize',fit);
window.addEventListener('orientationchange',function(){setTimeout(fit,300);});
function frame(ts){
 var dt=last?Math.min(.2,(ts-last)/1000):0;last=ts;
 T+=dt*SPEED;
 frames=Math.floor((ts/1000%1)*25);
 if(T>MAX){T=0;failT=failT>=0?0:-1;}
 if(scrub&&d.activeElement!==scrub)scrub.value=Math.round(T);
 // авто-переключение камер, пока зритель сам не выбрал источник
 if(!held&&T-autoAt>240){autoAt=T;put((cur+1)%pgm.length,false);}
 // VU-метр: пляшет от того же шума
 vu.forEach(function(n,k){
  var v=.22+Math.abs(Math.sin(T*3.1+k*1.7))*.55+noise(T*7+k)*.2;
  n.style.height=Math.min(1,v)*100+'%';
 });
 paint();
 requestAnimationFrame(frame);
}
if(RM){paint();}
else{requestAnimationFrame(frame);}

// ── тракт сигнала ──
var nodes=[].slice.call(d.querySelectorAll('.eo-node')),desc=d.getElementById('eoChainDesc'),
    TXT=[__CHAIN__];
nodes.forEach(function(b){b.addEventListener('click',function(){
 var i=+b.getAttribute('data-i');
 nodes.forEach(function(n,k){n.classList.toggle('is-on',k===i);});
 if(desc)desc.textContent=TXT[i];
});});
})();</script>"""

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
                 '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"ONLINE трансляция Eaton с форума IT-ОСЬ 2020",'
                 '"item":"' + URL + '"}]}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>ONLINE трансляция Eaton с форума OCS «IT-ОСЬ 2020» | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: онлайн-трансляция выступления Eaton на форуме OCS Distribution «IT-ОСЬ 2020». Аппаратная в офисе заказчика, две камеры, мини-ПТС и vMix, два независимых канала мобильного интернета с автопереключением. Семь часов эфира с 10:30 до 17:30 без сбоев.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="ONLINE трансляция Eaton с форума «IT-ОСЬ 2020» | кейс Hand Marketing">
<meta property="og:description" content="Офис заказчика на день стал студией: две камеры, мини-ПТС, vMix и два канала мобильного интернета. Семь часов эфира на виртуальный стенд форума без единого обрыва.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/shift-desk.jpg">
<meta property="og:site_name" content="Hand Marketing"><meta property="og:locale" content="ru_RU">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/plex.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def js():
    caps = ','.join("['%s','%s']" % (label.replace("'", "\\'"), cap.replace("'", "\\'"))
                    for _f, label, cap, _alt in SOURCES)
    chain = ','.join("'%s'" % d.replace("'", "\\'") for _t, _i, d in CHAIN)
    return PAGE_JS.replace('__CAPS__', caps).replace('__CHAIN__', chain)


def build():
    return (HEAD + rc.header() + '<main class="eo">' + hero() + task() + chain() +
            net() + clock() + crew() + finale() + '</main><a id="lead"></a>' +
            rc.footer() + rc.JS + js() + BREADCRUMB_LD + '</body></html>')


if __name__ == '__main__':
    out = os.path.join(ROOT, 'eaton_online')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    # index-a2.html это деплой-источник (workflow переименовывает его в index.html)
    # и затёр бы кастомную страницу на проде.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('удалён устаревший index-a2.html')
    print('written', os.path.join(out, 'index.html'))
