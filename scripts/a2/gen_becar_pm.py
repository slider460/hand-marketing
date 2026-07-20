#!/usr/bin/env python3
"""Генерит mirror/portfolio/becar-private-money/index.html — кейс «Стенд You&Co
для Becar на Private Money Expo Forum 2021» (выставка под ключ: концепция, дизайн,
застройка, презентация для сцены, POSM/полиграфия, сопровождение, демонтаж,
фотоотчёт). Индивидуальный дизайн в айдентике You&Co: фиолетовый/красный/жёлтый,
«вырезные» бумажные формы как в презентации, дубайский лайн-арт, кубки-буллеты.
Интерактив: переключатель «эскизы В1/В2 → финальный 3D» с ракурсами и tilt-эффектом,
лента слайдов презентации. Ассеты: mirror/images/becar-pm/ (scripts/becar-pm-assets.py).
Шапка/форма/подвал — стандартные из react-chrome.py. Правки страницы — только через
этот скрипт. build_v1 страницу пропускает по маркеру <!--custom-page-->."""
import os, importlib.util, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/becar-pm'

# ─── CSS (обычная строка, НЕ f-string — фигурные скобки не экранируем) ───────
PAGE_CSS = """<style id="bp-css">
:root{--bp-purple:#5B3A8F;--bp-deep:#3B2564;--bp-red:#E8404A;--bp-yellow:#F5A731;
 --bp-blue:#2456A6;--bp-ink:#14171C;--bp-paper:#FAF7F2;--bp-gold:#FFD37A}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bp-paper)}
.bp,.bp *{box-sizing:border-box}
.bp{font-family:'Montserrat',-apple-system,Arial,sans-serif;color:var(--bp-ink);overflow:hidden}
.bp img{max-width:100%;height:auto;display:block}
.bp-wrap{max-width:1160px;margin:0 auto;padding:0 40px;position:relative;z-index:2}
.bp-sec{position:relative;padding:84px 0}
.bp-kicker{display:inline-flex;align-items:center;gap:10px;font-size:12.5px;font-weight:800;
 letter-spacing:.16em;text-transform:uppercase}
.bp-kicker::before{content:"";width:26px;height:3px;background:currentColor;border-radius:2px}
.bp-h2{margin:14px 0 18px;font-size:clamp(28px,3.6vw,44px);font-weight:800;line-height:1.04;letter-spacing:-.02em}
.bp-lead{max-width:64ch;font-size:17px;line-height:1.7;color:#4A4453;margin:0 0 14px}
/* reveal */
.bp-r{opacity:0;transform:translateY(22px);transition:opacity .6s ease,transform .6s ease}
.bp-r.is-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.bp-r{opacity:1;transform:none;transition:none}}
/* «вырезные» декоративные формы */
.bp-cut{position:absolute;z-index:1;pointer-events:none}
/* ── HERO ── */
.bp-hero{background:var(--bp-deep);color:#fff;padding:70px 0 0;position:relative}
.bp-hero .bp-kicker{color:var(--bp-gold)}
.bp-hero__grid{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center}
.bp-hero__client{display:flex;align-items:center;gap:12px;margin:0 0 22px;font-size:14px;font-weight:600;color:#CBBFE3}
.bp-hero__client b{color:#fff;font-weight:800}
.bp-h1{margin:12px 0 18px;font-size:clamp(34px,4.6vw,58px);font-weight:800;line-height:1.02;letter-spacing:-.025em}
.bp-h1 .amp{color:var(--bp-yellow)}
.bp-hero__lead{max-width:56ch;font-size:16.5px;line-height:1.7;color:#D9D0EC;margin:0 0 26px}
.bp-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 34px;padding:0;list-style:none}
.bp-chips li{padding:8px 15px;border:1.5px solid rgba(255,255,255,.28);border-radius:999px;
 font-size:12.5px;font-weight:700;letter-spacing:.02em;color:#EFE9FA}
.bp-chips li.hot{background:var(--bp-yellow);border-color:var(--bp-yellow);color:var(--bp-ink)}
.bp-hero__ph{position:relative;z-index:2}
.bp-hero__ph img{border-radius:18px;box-shadow:0 30px 70px rgba(10,4,30,.5);
 clip-path:polygon(0 3.5%,3% 0,100% 1%,98.5% 96%,96% 100%,1% 98.5%)}
.bp-hero__tag{position:absolute;right:-14px;top:-18px;z-index:3;background:var(--bp-red);color:#fff;
 font-size:12.5px;font-weight:800;letter-spacing:.06em;padding:10px 16px;border-radius:6px;
 transform:rotate(3deg);box-shadow:0 10px 24px rgba(0,0,0,.35)}
/* факты-лента под hero */
.bp-facts{margin-top:64px;background:var(--bp-purple);position:relative;z-index:2}
.bp-facts__in{max-width:1160px;margin:0 auto;padding:26px 40px;display:grid;
 grid-template-columns:repeat(4,1fr);gap:18px}
.bp-fact{display:flex;flex-direction:column;gap:2px;padding-left:16px;border-left:3px solid var(--bp-yellow)}
.bp-fact b{font-size:26px;font-weight:800;color:#fff;line-height:1.1}
.bp-fact span{font-size:12.5px;font-weight:600;color:#D5C8EF;line-height:1.35}
/* дубайский лайн-арт в hero */
.bp-skyline{position:absolute;left:0;right:0;bottom:-2px;z-index:1;opacity:.5}
.bp-skyline svg{display:block;width:100%;height:150px}
/* ── ЗАДАЧА ── */
.bp-task__grid{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:start}
.bp-list{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:12px}
.bp-list li{position:relative;padding-left:34px;font-size:15.5px;line-height:1.6;color:#3E3849}
.bp-list li::before{content:"";position:absolute;left:0;top:2px;width:20px;height:20px;
 background:var(--cup,var(--bp-red));-webkit-mask:var(--bp-cup-mask) no-repeat center/contain;mask:var(--bp-cup-mask) no-repeat center/contain}
.bp-card{position:relative;background:#fff;border-radius:18px;padding:34px 32px;
 box-shadow:0 18px 50px rgba(59,37,100,.12)}
.bp-card_alert{background:var(--bp-red);color:#fff;transform:rotate(1.2deg)}
.bp-card_alert h3{margin:0 0 10px;font-size:21px;font-weight:800;line-height:1.2}
.bp-card_alert p{margin:0;font-size:15px;line-height:1.65;color:#FFE3E5}
.bp-card__stamp{position:absolute;top:-16px;right:22px;background:var(--bp-ink);color:var(--bp-gold);
 font-size:11.5px;font-weight:800;letter-spacing:.1em;padding:8px 14px;border-radius:6px;transform:rotate(-2deg)}
.bp-arrowline{margin:22px 0 0;display:flex;align-items:center;gap:10px;font-size:13.5px;font-weight:800;
 color:var(--bp-purple);text-transform:uppercase;letter-spacing:.08em}
/* ── КОНЦЕПЦИЯ ── */
.bp-idea{background:var(--bp-blue);color:#fff}
.bp-idea .bp-kicker{color:var(--bp-gold)}
.bp-idea .bp-lead{color:#D7E3F8}
.bp-idea__grid{display:grid;grid-template-columns:1fr 1fr;gap:52px;align-items:center}
.bp-idea__art{position:relative}
.bp-idea__art img{border-radius:16px;box-shadow:0 26px 60px rgba(2,12,40,.45);
 clip-path:polygon(2% 0,100% 2.5%,98% 100%,0 97%)}
.bp-brands{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 0;padding:0;list-style:none}
.bp-brands li{background:rgba(255,255,255,.12);border-radius:8px;padding:7px 13px;
 font-size:12.5px;font-weight:700;color:#EAF1FC}
.bp-idea__note{margin-top:26px;display:flex;gap:14px;align-items:flex-start;background:rgba(255,255,255,.08);
 border-left:4px solid var(--bp-yellow);border-radius:0 12px 12px 0;padding:16px 18px;font-size:14px;line-height:1.6;color:#DCE7FA}
/* ── 3D-БЛОК ── */
.bp-3d{background:var(--bp-deep);color:#fff}
.bp-3d .bp-kicker{color:var(--bp-gold)}
.bp-3d .bp-lead{color:#D9D0EC}
.bp-tabs{display:flex;flex-wrap:wrap;gap:10px;margin:30px 0 26px}
.bp-tab{appearance:none;border:2px solid rgba(255,255,255,.25);background:transparent;color:#E4DCF4;
 border-radius:999px;padding:11px 22px;font:800 13.5px Montserrat,Arial,sans-serif;letter-spacing:.03em;
 cursor:pointer;transition:all .2s}
.bp-tab:hover{border-color:#fff;color:#fff}
.bp-tab.is-on{background:var(--bp-yellow);border-color:var(--bp-yellow);color:var(--bp-ink)}
.bp-viewer{perspective:1200px}
.bp-viewer__stage{position:relative;border-radius:20px;overflow:hidden;background:#241542;
 box-shadow:0 34px 80px rgba(8,2,26,.55);transform-style:preserve-3d;transition:transform .18s ease-out;will-change:transform}
.bp-viewer__stage img{width:100%;aspect-ratio:16/10;object-fit:cover;transition:opacity .28s ease}
.bp-viewer__stage img.is-fading{opacity:0}
.bp-viewer__hint{position:absolute;left:18px;bottom:14px;background:rgba(20,10,44,.72);color:#E9E1F8;
 font-size:12px;font-weight:700;letter-spacing:.05em;padding:7px 13px;border-radius:999px;backdrop-filter:blur(4px)}
.bp-viewer__cap{margin:18px 2px 0;font-size:14.5px;line-height:1.65;color:#CFC3E8;max-width:78ch}
.bp-thumbs{display:flex;gap:12px;margin-top:18px}
.bp-thumb{appearance:none;border:2.5px solid transparent;border-radius:12px;overflow:hidden;padding:0;
 background:none;cursor:pointer;width:132px;flex:none;transition:border-color .2s,transform .2s}
.bp-thumb img{aspect-ratio:16/10;object-fit:cover}
.bp-thumb:hover{transform:translateY(-3px)}
.bp-thumb.is-on{border-color:var(--bp-yellow)}
/* ── ГАЛЕРЕЯ ЗАСТРОЙКИ ── */
.bp-build__grid{display:grid;grid-template-columns:repeat(6,1fr);gap:18px;margin-top:36px}
.bp-shot{position:relative;border-radius:14px;overflow:hidden;box-shadow:0 16px 40px rgba(59,37,100,.16)}
.bp-shot img{width:100%;height:100%;object-fit:cover}
.bp-shot figcaption{position:absolute;left:12px;bottom:12px;background:rgba(20,23,28,.78);color:#fff;
 font-size:11.5px;font-weight:700;letter-spacing:.04em;padding:6px 12px;border-radius:999px;backdrop-filter:blur(3px)}
.bp-shot_a{grid-column:span 4;aspect-ratio:16/9}
.bp-shot_b{grid-column:span 2;aspect-ratio:4/5}
.bp-shot_c{grid-column:span 2;aspect-ratio:4/3.2}
.bp-shot_t1{transform:rotate(-.6deg)}.bp-shot_t2{transform:rotate(.7deg)}
/* ── СЦЕНА ── */
.bp-stage{background:var(--bp-ink);color:#fff}
.bp-stage .bp-kicker{color:var(--bp-red)}
.bp-stage .bp-lead{color:#C9CDD4}
.bp-stage__grid{display:grid;grid-template-columns:1.25fr .75fr;gap:18px;margin:36px 0 14px}
.bp-stage__grid img{border-radius:14px;width:100%;height:100%;object-fit:cover;aspect-ratio:16/10}
.bp-slides{margin-top:34px}
.bp-slides__head{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:16px}
.bp-slides__head h3{margin:0;font-size:19px;font-weight:800}
.bp-slides__nav{display:flex;gap:8px}
.bp-slides__nav button{appearance:none;width:42px;height:42px;border-radius:50%;border:2px solid rgba(255,255,255,.3);
 background:transparent;color:#fff;font-size:18px;font-weight:800;cursor:pointer;transition:all .2s}
.bp-slides__nav button:hover{background:var(--bp-yellow);border-color:var(--bp-yellow);color:var(--bp-ink)}
.bp-slides__track{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;
 padding:4px 4px 14px;scrollbar-width:thin;scrollbar-color:var(--bp-purple) transparent}
.bp-slides__track img{flex:none;width:min(430px,78vw);scroll-snap-align:start;border-radius:12px;
 box-shadow:0 14px 34px rgba(0,0,0,.45);transform:rotate(-.4deg)}
.bp-slides__track img:nth-child(even){transform:rotate(.5deg)}
/* ── POSM + НАГРАДА ── */
.bp-posm__grid{display:grid;grid-template-columns:.95fr 1.05fr;gap:56px;align-items:center}
.bp-posm__ph{position:relative}
.bp-posm__ph img{border-radius:16px;box-shadow:0 24px 60px rgba(59,37,100,.2);
 clip-path:polygon(0 2%,98% 0,100% 98%,2% 100%)}
.bp-posm__star{position:absolute;right:-16px;top:-20px;width:104px;height:104px;z-index:3;
 background:var(--bp-yellow);border-radius:50%;display:flex;align-items:center;justify-content:center;
 text-align:center;font-size:10.5px;font-weight:800;letter-spacing:.06em;line-height:1.3;color:var(--bp-ink);
 transform:rotate(6deg);box-shadow:0 12px 30px rgba(59,37,100,.25);padding:12px}
/* ── ИТОГ ── */
.bp-total{background:var(--bp-purple);color:#fff}
.bp-total .bp-kicker{color:var(--bp-gold)}
.bp-total .bp-lead{color:#E2D8F4}
.bp-total__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:38px}
.bp-step{background:rgba(255,255,255,.08);border-radius:14px;padding:20px 18px;min-height:118px;
 display:flex;flex-direction:column;gap:8px;transition:transform .2s,background .2s}
.bp-step:hover{transform:translateY(-4px);background:rgba(255,255,255,.14)}
.bp-step i{width:24px;height:24px;background:var(--bp-yellow);
 -webkit-mask:var(--bp-cup-mask) no-repeat center/contain;mask:var(--bp-cup-mask) no-repeat center/contain}
.bp-step b{font-size:14.5px;font-weight:800;line-height:1.25}
.bp-step span{font-size:12.5px;line-height:1.5;color:#D9CDF0}
.bp-total__cta{margin-top:42px;display:flex;align-items:center;gap:22px;flex-wrap:wrap}
.bp-btn{display:inline-flex;align-items:center;gap:10px;background:var(--bp-yellow);color:var(--bp-ink);
 font:800 15px Montserrat,Arial,sans-serif;padding:16px 34px;border-radius:999px;text-decoration:none;
 transition:transform .18s,box-shadow .18s}
.bp-btn:hover{transform:translateY(-3px);box-shadow:0 14px 34px rgba(0,0,0,.3)}
.bp-total__more{font-size:14px;color:#E2D8F4}
.bp-total__more a{color:#fff;font-weight:700}
/* ── АДАПТИВ ── */
@media(max-width:1023px){
 .bp-hero__grid,.bp-task__grid,.bp-idea__grid,.bp-posm__grid{grid-template-columns:1fr;gap:36px}
 .bp-facts__in{grid-template-columns:repeat(2,1fr);padding:24px 24px}
 .bp-total__grid{grid-template-columns:repeat(2,1fr)}
 .bp-stage__grid{grid-template-columns:1fr}
 .bp-hero__tag{right:6px}
}
@media(max-width:679px){
 .bp-wrap{padding:0 18px}
 .bp-sec{padding:58px 0}
 .bp-hero{padding-top:48px}
 .bp-facts__in{grid-template-columns:1fr 1fr;gap:14px;padding:20px 18px}
 .bp-fact b{font-size:21px}
 .bp-build__grid{grid-template-columns:1fr 1fr;gap:12px}
 .bp-shot_a{grid-column:span 2;aspect-ratio:16/10}
 .bp-shot_b,.bp-shot_c{grid-column:span 1;aspect-ratio:1/1}
 .bp-thumb{width:96px}
 .bp-total__grid{grid-template-columns:1fr}
 .bp-slides__nav{display:none}
 .bp-viewer__hint{display:none}
}
</style>"""

# кубок You&Co как mask-иконка (общая переменная)
CUP_MASK = ("<style>:root{--bp-cup-mask:url('data:image/svg+xml;utf8,"
            "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\">"
            "<path d=\"M6 2h12v2h4v3c0 3-2.4 5.4-5.3 5.9A6 6 0 0 1 13 16v3h4v3H7v-3h4v-3a6 6 0 0 1-3.7-3.1C4.4 12.4 2 10 2 7V4h4V2zm-2 4v1c0 1.8 1.2 3.3 2.8 3.8A9 9 0 0 1 6 7V6H4zm16 0h-2v1c0 1.7-.3 3.1-.8 4.8C18.8 10.3 20 8.8 20 7V6z\"/>"
            "</svg>')}</style>")

def cut(shape, css):
    """Вырезная декоративная форма: инлайн-SVG полигона с абсолютным позиционированием."""
    fills = {'red': '#E8404A', 'yellow': '#F5A731', 'purple': '#7A4FA8', 'blue': '#2456A6', 'gold': '#FFD37A'}
    pts = {
        'shard':  '12,0 100,22 74,100 0,64',
        'burst':  '50,0 61,35 100,38 68,59 80,100 50,74 20,100 32,59 0,38 39,35',
        'wave':   '0,40 28,10 66,28 100,6 100,100 0,100',
        'corner': '0,0 100,0 100,26 30,100 0,100',
    }
    name, color = shape.split('-')
    return (f'<svg class="bp-cut" style="{css}" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
            f'<polygon points="{pts[name]}" fill="{fills[color]}"/></svg>')

# лайн-арт Дубая (Burj Khalifa, колесо Ain Dubai, пальма, застройка) — белые штрихи
SKYLINE = ('<div class="bp-skyline" aria-hidden="true"><svg viewBox="0 0 1200 150" preserveAspectRatio="xMidYMax slice" '
           'fill="none" stroke="rgba(255,255,255,.55)" stroke-width="2">'
           '<circle cx="150" cy="88" r="46"/><circle cx="150" cy="88" r="7"/>'
           '<path d="M150 42v92M110 60l80 56M110 116l80-56M104 88h92"/>'
           '<path d="M150 134l-18 16M150 134l18 16"/>'
           '<path d="M320 150V96h34v54M337 96V74M330 84h14"/>'
           '<path d="M430 150V70h44v80M440 70V56h24v14M446 86h12M446 102h12M446 118h12"/>'
           '<path d="M600 150 618 12M636 150 618 12M604 118h28M608 92h20M612 66h12M618 12V0"/>'
           '<path d="M760 150v-44c0-10 18-10 18 0v44M769 106V88"/>'
           '<path d="M769 88c-14-12-30-14-42-8 14 2 26 6 42 8zM769 88c14-12 30-14 42-8-14 2-26 6-42 8zM769 88c-10-16-8-30 0-40-2 14-2 26 0 40zM769 88c10-16 8-30 0-40 2 14 2 26 0 40z"/>'
           '<path d="M920 150V86h56v64M934 86V70h28v16M942 102h14M942 120h14"/>'
           '<path d="M1080 150V108h40v42M1090 108V96h20v12"/>'
           '</svg></div>')

HEAD = f'''<!doctype html><html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Стенд Becar на Private Money Expo Forum — выставка под ключ | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: подготовка Becar Asset Management к форуму Private Money 2021 под ключ — концепция и дизайн стенда You&Co, застройка на компактной площадке, презентация для главной сцены, POSM и полиграфия, сопровождение, демонтаж и фотоотчёт.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hand-marketing.ru/portfolio/becar-private-money/">
<meta property="og:type" content="article"><meta property="og:title" content="Стенд You&Co для Becar на Private Money Expo Forum 2021 — кейс Hand Marketing">
<meta property="og:description" content="Выставка под ключ: концепция, дизайн и застройка стенда, презентация для выступления топ-менеджеров, POSM и полиграфия, сопровождение и фотоотчёт.">
<meta property="og:url" content="https://hand-marketing.ru/portfolio/becar-private-money/">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/render-front.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
{rc.FONT}<link href="/fonts/raleway-700.css" rel="stylesheet">{rc.CSS}{CUP_MASK}{PAGE_CSS}{METRIKA}
</head>
<body>'''

# ─── интерактив: данные вариантов стенда для 3D-блока ────────────────────────
VARIANTS_JS = """<script>
var BP3D={
 v1:{views:['%(i)s/sketch-v1-a.jpg','%(i)s/sketch-v1-b.jpg','%(i)s/sketch-v1-c.jpg'],
  cap:'Эскиз №1 — «пляж Марины»: жёлтая ресепшен-стойка и подиумные столики, песочная зона отдыха у кромки «моря» на полу, карта Дубая во всю стену. Смелый ход, но открытая пляжная зона съедала дефицитные метры.'},
 v2:{views:['%(i)s/sketch-v2-a.jpg','%(i)s/sketch-v2-b.jpg','%(i)s/sketch-v2-c.jpg'],
  cap:'Эскиз №2 — «вечерний город»: белая стойка с лайн-артом фасадов, бордовый текстиль, колесо обозрения и звёзды. Эффектно, но тёмная гамма спорила со светлой галереей площадки.'},
 fin:{views:['%(i)s/render-front.jpg','%(i)s/render-top.jpg','%(i)s/render-detail.jpg'],
  cap:'Финальный 3D-проект: вся коммуникация ушла на стену-панно с картой Дубая, лаунж на светлом дереве вдоль фронта, ТВ-зона отдела продаж с QR, торцевые пилоны-витрины со всеми брендами экосистемы Becar. Каждый метр работает.'}
};
(function(){
 var stage=document.getElementById('bp3d-stage'),img=stage&&stage.querySelector('img');
 var cap=document.getElementById('bp3d-cap'),thumbs=document.getElementById('bp3d-thumbs');
 if(!stage||!img)return;
 var cur='fin',view=0;
 function swap(src,alt){img.classList.add('is-fading');setTimeout(function(){img.src=src;if(alt)img.alt=alt;img.classList.remove('is-fading');},180);}
 function draw(){
  var d=BP3D[cur];cap.textContent=d.cap;
  thumbs.innerHTML='';
  d.views.forEach(function(v,i){
   var b=document.createElement('button');b.type='button';b.className='bp-thumb'+(i===view?' is-on':'');
   b.setAttribute('aria-label','Ракурс '+(i+1));
   var t=document.createElement('img');t.src=v;t.alt='';t.loading='lazy';b.appendChild(t);
   b.addEventListener('click',function(){view=i;swap(v);[].forEach.call(thumbs.children,function(c,j){c.classList.toggle('is-on',j===i);});});
   thumbs.appendChild(b);
  });
 }
 [].forEach.call(document.querySelectorAll('.bp-tab'),function(t){
  t.addEventListener('click',function(){
   cur=t.getAttribute('data-v');view=0;
   [].forEach.call(document.querySelectorAll('.bp-tab'),function(x){x.classList.toggle('is-on',x===t);});
   swap(BP3D[cur].views[0],t.textContent+' — стенд You&Co для Becar');draw();
  });
 });
 // лёгкий tilt за курсором (только точные указатели, без reduced-motion)
 if(window.matchMedia&&matchMedia('(pointer:fine)').matches&&!matchMedia('(prefers-reduced-motion:reduce)').matches){
  stage.addEventListener('mousemove',function(e){
   var r=stage.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
   stage.style.transform='rotateY('+(x*7).toFixed(2)+'deg) rotateX('+(-y*5).toFixed(2)+'deg)';
  });
  stage.addEventListener('mouseleave',function(){stage.style.transform='';});
 }
 draw();
})();
// лента слайдов: стрелки
(function(){
 var tr=document.getElementById('bp-slides-track');if(!tr)return;
 function step(dir){tr.scrollBy({left:dir*(tr.firstElementChild.getBoundingClientRect().width+16),behavior:'smooth'});}
 var p=document.getElementById('bp-sl-prev'),n=document.getElementById('bp-sl-next');
 if(p)p.addEventListener('click',function(){step(-1);});
 if(n)n.addEventListener('click',function(){step(1);});
})();
</script>""" % {'i': IMG}

REVEAL_JS = """<script>(function(){
var els=[].slice.call(document.querySelectorAll('.bp-r'));
if(!('IntersectionObserver' in window)){els.forEach(function(n){n.classList.add('is-in');});return;}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
els.forEach(function(n,i){n.style.transitionDelay=Math.min(i%4*90,270)+'ms';
 // видимое при загрузке проявляем сразу (без ожидания IO — надёжно и без «мигания» первого экрана)
 var r=n.getBoundingClientRect();
 if(r.top<window.innerHeight&&r.bottom>0){n.classList.add('is-in');}else{io.observe(n);}});
})();</script>"""

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
 '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
 '{"@type":"ListItem","position":2,"name":"Стенд Becar на Private Money Expo Forum",'
 '"item":"https://hand-marketing.ru/portfolio/becar-private-money/"}]}</script>')


def hero():
    return (f'<section class="bp-hero">'
        + cut('shard-red', 'width:150px;height:130px;left:-46px;top:52px;transform:rotate(-14deg)')
        + cut('corner-yellow', 'width:130px;height:120px;right:-34px;top:-26px;transform:rotate(8deg)')
        + cut('burst-gold', 'width:56px;height:56px;left:46%;top:34px;opacity:.85')
        + f'<div class="bp-wrap"><div class="bp-hero__grid">'
        f'<div class="bp-r"><span class="bp-kicker">Кейс · выставка под ключ</span>'
        f'<h1 class="bp-h1">You<span class="amp">&amp;</span>Co на форуме Private&nbsp;Money</h1>'
        f'<div class="bp-hero__client"><b>Becar Asset Management</b> · Private Money Expo Forum · Москва, 2021</div>'
        f'<p class="bp-hero__lead">Подготовили генерального партнёра форума в области недвижимости '
        f'к выставке полностью под ключ: от идеи стенда и презентации для главной сцены — '
        f'до последней брошюры, демонтажа и фотоотчёта.</p>'
        f'<ul class="bp-chips"><li class="hot">Концепция</li><li>Дизайн стенда</li><li>Застройка</li>'
        f'<li>Презентация для сцены</li><li>POSM и полиграфия</li><li>Сопровождение</li>'
        f'<li>Демонтаж</li><li>Фотоотчёт</li></ul></div>'
        f'<div class="bp-hero__ph bp-r"><span class="bp-hero__tag">Этот стенд сделали мы!</span>'
        f'<img src="{IMG}/photo-stand-full.jpg" alt="Построенный стенд You&Co для Becar на форуме Private Money 2021" width="2000" height="1334"></div>'
        f'</div></div>{SKYLINE}'
        f'<div class="bp-facts"><div class="bp-facts__in">'
        f'<div class="bp-fact bp-r"><b>7 брендов</b><span>экосистемы Becar собраны на одном стенде</span></div>'
        f'<div class="bp-fact bp-r"><b>2 топ-спикера</b><span>Becar выступили на главной сцене #PME2021</span></div>'
        f'<div class="bp-fact bp-r"><b>2 эскиза + финал</b><span>вариантов дизайна до утверждения проекта</span></div>'
        f'<div class="bp-fact bp-r"><b>100% под ключ</b><span>от концепции до демонтажа и фотоотчёта</span></div>'
        f'</div></div></section>')


def task():
    return (f'<section class="bp-sec bp bp-task">'
        + cut('burst-purple', 'width:74px;height:74px;right:6%;top:44px;opacity:.16')
        + f'<div class="bp-wrap"><div class="bp-task__grid">'
        f'<div class="bp-r"><span class="bp-kicker" style="color:#E8404A">Задача</span>'
        f'<h2 class="bp-h2">Форум инвесторов — и один шанс собрать всё вместе</h2>'
        f'<p class="bp-lead">Private Money Expo Forum — главная встреча частных инвесторов в недвижимость. '
        f'Becar Asset Management шёл на форум генеральным партнёром со всей продуктовой линейкой: '
        f'отели We&I и Vertical, БЦ «Станция», ТРЦ «Смайл», Ramada Encore, GrowUp и зонтичный бренд '
        f'доходных инвестиций You&Co.</p>'
        f'<ul class="bp-list">'
        f'<li style="--cup:#E8404A">Разработать концепцию и дизайн стенда, который продаёт сразу семь продуктов</li>'
        f'<li style="--cup:#F5A731">Застроить его на площадке форума и обеспечить работу все дни</li>'
        f'<li style="--cup:#5B3A8F">Подготовить дизайн презентации для выступления топ-менеджеров на главной сцене</li>'
        f'<li style="--cup:#2456A6">Произвести POSM и полиграфию: брошюры, папки, раздаточные материалы</li>'
        f'<li style="--cup:#E8404A">Демонтировать стенд и отдать клиенту готовый фотоотчёт</li></ul></div>'
        f'<div class="bp-r"><div class="bp-card bp-card_alert">'
        f'<span class="bp-card__stamp">Главный вызов</span>'
        f'<h3>Очень мало пространства</h3>'
        f'<p>Вместо просторного павильона — узкая линейная полоса в галерее у панорамного остекления: '
        f'глубокой застройки не сделать, каждый метр на счету. Значит, работать должна каждая '
        f'поверхность — стены, торцы и даже пол.</p></div>'
        f'<div class="bp-arrowline">Решение — ниже ↓</div></div>'
        f'</div></div></section>')


def idea():
    return (f'<section class="bp-sec bp-idea">'
        + cut('shard-yellow', 'width:120px;height:104px;right:-30px;bottom:40px;transform:rotate(16deg);opacity:.9')
        + cut('burst-red', 'width:60px;height:60px;left:4%;top:40px;opacity:.8')
        + f'<div class="bp-wrap"><div class="bp-idea__grid">'
        f'<div class="bp-r"><span class="bp-kicker">Концепция</span>'
        f'<h2 class="bp-h2">Стенд-открытка из Дубая</h2>'
        f'<p class="bp-lead">You&Co выводил инвесторов на самый горячий рынок 2021 года — Дубай. '
        f'Мы превратили длинную стену — единственный крупный носитель на площадке — в иллюстрированную '
        f'карту города в фирменном лайн-арте: Burj Khalifa, Palm Jumeirah, колесо Ain Dubai, Marina '
        f'и маршрут к будущему объекту.</p>'
        f'<p class="bp-lead">Торцевые пилоны стали витринами экосистемы: на каждом — вся продуктовая '
        f'линейка Becar. Куда бы гость ни посмотрел, он видел и город мечты, и конкретные продукты, '
        f'в которые можно инвестировать уже сегодня.</p>'
        f'<ul class="bp-brands"><li>Becar AM</li><li>You&Co</li><li>We&I by Vertical</li><li>Vertical</li>'
        f'<li>БЦ «Станция»</li><li>Ramada Encore</li><li>ТРЦ «Смайл»</li><li>GrowUp</li></ul>'
        f'<div class="bp-idea__note bp-r">Светящийся логотип You&Co, ТВ-зона отдела продаж с QR-кодом '
        f'и лаунж на светлом дереве с коврами — тёплый «отельный» приём вместо витринного официоза.</div></div>'
        f'<div class="bp-idea__art bp-r"><img src="{IMG}/photo-speaker.jpg" loading="lazy" '
        f'alt="Стена-панно с картой Дубая и светящимся логотипом You&Co" width="2000" height="1334"></div>'
        f'</div></div></section>')


def viewer3d():
    return (f'<section class="bp-sec bp-3d" id="bp-3d">'
        + cut('corner-red', 'width:110px;height:100px;left:-30px;bottom:-20px;transform:rotate(180deg);opacity:.85')
        + cut('burst-gold', 'width:52px;height:52px;right:8%;top:52px;opacity:.75')
        + f'<div class="bp-wrap">'
        f'<div class="bp-r"><span class="bp-kicker">Стенд в 3D</span>'
        f'<h2 class="bp-h2">От эскиза до финального проекта</h2>'
        f'<p class="bp-lead">Клиент выбирал не «кота в мешке»: мы отрисовали стенд в 3D в двух концепциях, '
        f'а после утверждения довели финальный проект до рабочего дизайна. Покрутите ракурсы — '
        f'так стенд выглядел ещё до начала застройки.</p></div>'
        f'<div class="bp-tabs bp-r" role="tablist">'
        f'<button type="button" class="bp-tab" data-v="v1">Эскиз · вариант 1</button>'
        f'<button type="button" class="bp-tab" data-v="v2">Эскиз · вариант 2</button>'
        f'<button type="button" class="bp-tab is-on" data-v="fin">Финальный 3D-проект</button></div>'
        f'<div class="bp-viewer bp-r"><div class="bp-viewer__stage" id="bp3d-stage">'
        f'<img src="{IMG}/render-front.jpg" alt="Финальный 3D-проект стенда You&Co для Becar" width="1920" height="1200">'
        f'<span class="bp-viewer__hint">Наведите курсор — стенд наклонится · выбирайте ракурсы ниже</span></div>'
        f'<p class="bp-viewer__cap" id="bp3d-cap"></p>'
        f'<div class="bp-thumbs" id="bp3d-thumbs"></div></div>'
        f'</div></section>')


def build_gallery():
    shots = [
        ('photo-stand-full.jpg', 'Смонтированный стенд до открытия форума', 'a', 't1'),
        ('photo-lounge.jpg', 'Лаунж-зона у карты Дубая', 'b', 't2'),
        ('photo-talks.jpg', 'Переговоры на стенде', 'c', 't2'),
        ('photo-crowd.jpg', 'Поток гостей в часы форума', 'a', 't1'),
    ]
    figs = ''.join(
        f'<figure class="bp-shot bp-shot_{sz} bp-shot_{tl} bp-r"><img src="{IMG}/{f}" loading="lazy" '
        f'alt="{H.escape(capt)} — стенд Becar на Private Money 2021" width="2000" height="1334">'
        f'<figcaption>{H.escape(capt)}</figcaption></figure>'
        for f, capt, sz, tl in shots)
    return (f'<section class="bp-sec bp bp-build">'
        + cut('shard-purple', 'width:96px;height:88px;left:-26px;top:120px;transform:rotate(-10deg);opacity:.14')
        + f'<div class="bp-wrap"><div class="bp-r">'
        f'<span class="bp-kicker" style="color:#5B3A8F">Реализация</span>'
        f'<h2 class="bp-h2">Как это выглядело вживую</h2>'
        f'<p class="bp-lead">Застройка прошла в ночь до открытия: каркас, печать панно, светящийся логотип, '
        f'мебель, ТВ-зона и лифлетницы. Все дни форума наша команда дежурила на площадке — '
        f'стенд отработал программу без единого сбоя, а после закрытия мы демонтировали '
        f'конструкции и передали клиенту фотоотчёт.</p></div>'
        f'<div class="bp-build__grid">{figs}</div>'
        f'</div></section>')


def stage():
    slides = ''.join(
        f'<img src="{IMG}/slide-{n}.jpg" loading="lazy" alt="Слайд презентации Becar для сцены Private Money — {H.escape(t)}" width="1400" height="788">'
        for n, t in [(1, 'Откуда — куда'), (2, 'хроника сцены 2017–2019'), (3, '2020 год'),
                     (4, 'что у вас сейчас'), (5, 'лапти против кед'), (6, 'коливинги в мире')])
    return (f'<section class="bp-sec bp-stage">'
        + cut('shard-red', 'width:120px;height:110px;right:-34px;top:60px;transform:rotate(24deg);opacity:.9')
        + cut('burst-yellow', 'width:54px;height:54px;left:5%;bottom:70px;opacity:.8')
        + f'<div class="bp-wrap">'
        f'<div class="bp-r"><span class="bp-kicker">Главная сцена</span>'
        f'<h2 class="bp-h2">Презентация, с которой не спят в зале</h2>'
        f'<p class="bp-lead">Вице-президент Becar Дмитрий Сороколетов и CVO Александр Пестряков выходили '
        f'на главную сцену форума — мы собрали для выступления презентацию в айдентике You&Co. '
        f'Вместо корпоративных таблиц — вырезные формы, кубки, мемы и честные графики: лапти против кед, '
        f'перекати-поле 2020-го и карта мировых коливингов. Зал слушал — и досидел до конца.</p></div>'
        f'<div class="bp-stage__grid">'
        f'<img class="bp-r" src="{IMG}/photo-stage-hall.jpg" loading="lazy" alt="Выступление Becar на главной сцене Private Money Expo Forum 2021" width="2000" height="1334">'
        f'<img class="bp-r" src="{IMG}/photo-stage-tops.jpg" loading="lazy" alt="Топ-менеджеры Becar на сцене #PME2021" width="2000" height="1334"></div>'
        f'<div class="bp-slides bp-r"><div class="bp-slides__head"><h3>Листайте слайды ↔</h3>'
        f'<div class="bp-slides__nav"><button type="button" id="bp-sl-prev" aria-label="Предыдущий слайд">‹</button>'
        f'<button type="button" id="bp-sl-next" aria-label="Следующий слайд">›</button></div></div>'
        f'<div class="bp-slides__track" id="bp-slides-track">{slides}</div></div>'
        f'</div></section>')


def posm():
    return (f'<section class="bp-sec bp bp-posm">'
        + cut('burst-red', 'width:64px;height:64px;right:7%;top:46px;opacity:.15')
        + f'<div class="bp-wrap"><div class="bp-posm__grid">'
        f'<div class="bp-posm__ph bp-r">'
        f'<span class="bp-posm__star">Награда форума — на нашем стенде</span>'
        f'<img src="{IMG}/photo-award.jpg" loading="lazy" '
        f'alt="Статуэтка Private Money 2021 и папка «Доходные инвестиции» на стенде Becar" width="2000" height="1334"></div>'
        f'<div class="bp-r"><span class="bp-kicker" style="color:#F5A731">POSM и полиграфия</span>'
        f'<h2 class="bp-h2">Раздатка, которую уносят с собой</h2>'
        f'<p class="bp-lead">Инвестор уходит со стенда — а продукты остаются у него в руках. '
        f'Мы произвели весь печатный комплект в единой айдентике:</p>'
        f'<ul class="bp-list">'
        f'<li style="--cup:#5B3A8F">Папки «Доходные инвестиции» со всей линейкой продуктов</li>'
        f'<li style="--cup:#E8404A">Брошюры We&I, Vertical, «Смайл», «Станция» и Ramada Encore</li>'
        f'<li style="--cup:#F5A731">«Конверт выгодных сделок» отдела продаж — офферы прямо на стенде</li>'
        f'<li style="--cup:#2456A6">Календари You&Co, лифлетницы и навигационная графика</li></ul>'
        f'<p class="bp-lead" style="margin-top:16px">Финальный штрих: вице-президент Becar получил '
        f'награду от организаторов форума — статуэтку «за личный вклад в создание новых стандартов '
        f'доходной недвижимости в России». Достойное завершение работы, в которую команда вложила '
        f'столько сил.</p></div>'
        f'</div></div></section>')


def total():
    steps = [
        ('Концепция и дизайн', 'Два эскизных 3D-варианта, финальный проект, рабочая документация'),
        ('Производство и застройка', 'Печать панно, светологотип, мебель, монтаж в ночь до открытия'),
        ('Контент и сцена', 'Дизайн презентации для выступления топ-менеджеров на главной сцене'),
        ('POSM и полиграфия', 'Папки, брошюры, конверты сделок, календари, лифлетницы'),
        ('Сопровождение', 'Команда на площадке все дни работы форума'),
        ('ТВ-зона продаж', 'Экран с роликами продуктов и QR-код отдела продаж SalesDep'),
        ('Демонтаж', 'Разбор конструкций и вывоз после закрытия — без забот клиента'),
        ('Фотоотчёт', 'Профессиональная съёмка стенда, гостей и выступлений'),
    ]
    cards = ''.join(f'<div class="bp-step bp-r"><i aria-hidden="true"></i><b>{H.escape(t)}</b>'
                    f'<span>{H.escape(d)}</span></div>' for t, d in steps)
    return (f'<section class="bp-sec bp-total">'
        + cut('corner-yellow', 'width:120px;height:110px;right:-30px;top:-26px;transform:rotate(6deg)')
        + cut('shard-red', 'width:100px;height:90px;left:-30px;bottom:30px;transform:rotate(-18deg);opacity:.85')
        + f'<div class="bp-wrap">'
        f'<div class="bp-r"><span class="bp-kicker">Что вошло в «под ключ»</span>'
        f'<h2 class="bp-h2">Один подрядчик — вся выставка</h2>'
        f'<p class="bp-lead">Клиент занимался переговорами с инвесторами. Всё остальное — от первой '
        f'идеи до фотоотчёта — сделал Hand Marketing.</p></div>'
        f'<div class="bp-total__grid">{cards}</div>'
        f'<div class="bp-total__cta bp-r"><a class="bp-btn" href="#lead">Обсудить свой стенд</a>'
        f'<span class="bp-total__more">Ещё стенды под ключ: <a href="/portfolio/samara-stand-vdnh">Самарская область</a>, '
        f'<a href="/portfolio/stavropol-stand-vdnh">Ставропольский край</a> · <a href="/exhibition/">услуга Exhibition Build</a></span></div>'
        f'</div></section>')


def build():
    body = (f'{rc.header()}<main class="bp">{hero()}{task()}{idea()}{viewer3d()}'
            f'{build_gallery()}{stage()}{posm()}{total()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{VARIANTS_JS}{REVEAL_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'portfolio', 'becar-private-money')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
