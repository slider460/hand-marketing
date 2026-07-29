#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/digital/becar/smile/index.html — кейс «Посадочная страница ТРЦ
Смайл» для Becar Asset Management: одностраничник, которым продавали метры в
действующем торговом центре в Петербурге частным инвесторам.

Дизайн-концепция: «улыбка». Вся айдентика посадочной держится на круге (логотип
центра — улыбка, кнопка, аватар смайла) и на паре бирюза + жёлтый. Кейс собран в
той же палитре, круги вынесены в фон, жёлтый работает только на главном.

Главный блок — прокрутка настоящей страницы внутри мокапа ноутбука: снимок снят
с исходной вёрстки 2020 года (scripts/smile-assets.py), поэтому кейс показывает
не три архивных картинки, а всю страницу целиком, плюс переключатель на телефон.
Второй интерактив — живой смайл в шапке: моргает сам и подмигивает на наведение,
ровно как на исходной странице («если долго смотреть на смайлик, он подмигнёт»).

Тексты переписаны. В тильдовской версии задача была скопирована с соседнего
кейса и гласила «для инвестиционного продукта ТРЦ Станция», хотя кейс про Смайл.

Ассеты: mirror/images/smile/ (scripts/smile-assets.py).
URL кейса прежний (он в sitemap и каталогах). Правки — ТОЛЬКО через этот скрипт;
build_v1 страницу пропускает по маркеру <!--custom-page-->."""
import os
import importlib.util
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/smile'
URL = 'https://hand-marketing.ru/digital/becar/smile/'

# ─── разбор экранов посадочной: (файл, номер, надзаголовок, заголовок, текст, alt)
SCREENS = [
 ('hero', '01', 'Первый экран',
  'Доходность и форма в одном кадре',
  'Логотип центра, обещание «до 13% годовых» и два поля формы стоят в одном экране. '
  'Тому, кто уже готов, не нужно ничего листать: имя, телефон, кнопка. Вся остальная '
  'страница работает на тех, кому сначала нужны доказательства.',
  'Первый экран посадочной страницы ТРЦ Смайл: логотип, доходность до 13% годовых и форма заявки'),
 ('tenants', '02', 'Кто платит аренду',
  '80% площадей заняты сетевыми арендаторами',
  'Слева одна крупная цифра, справа шесть коротких аргументов, под ними карусель '
  'логотипов. Абстрактный «арендный поток» превращается в знакомые вывески: '
  'Перекрёсток, Сбербанк, МТС, Билайн, Буквоед. Это первый ответ на вопрос, откуда '
  'берётся доход.',
  'Экран посадочной ТРЦ Смайл: 80% площадей у сетевых арендаторов и карусель логотипов'),
 ('mac', '03', 'Второй продукт',
  'Готовый арендный бизнес: Макдональдс, 343 кв. м',
  'Кроме долей в центре продавалось отдельное помещение с действующим договором '
  'аренды до 2030 года. Ему отдали отдельный экран и единственный на всю страницу '
  'фиолетовый фон: старая ставка 8% зачёркнута, рядом стоит 10%. По цвету видно, что '
  'это другое предложение, а не продолжение предыдущего.',
  'Экран продажи готового арендного бизнеса: Макдональдс, 343 кв. м, доходность 10% годовых'),
 ('guarantee', '04', 'Возражения',
  'Что будет, если арендаторы уйдут',
  'Три колонки закрывают главный страх: единая концепция управления, лояльность '
  'арендаторов, лояльность аудитории центра. Тут же объясняется, что организационными '
  'вопросами занимается управляющая компания, а инвестор получает отчётность.',
  'Экран «Гарантии дохода» на посадочной ТРЦ Смайл: концепция управления и лояльность арендаторов'),
 ('numbers', '05', 'Доказательства',
  'Восемь цифр вместо восьми обещаний',
  'Рост среднесуточной посещаемости, доход с квадратного метра выше рынка, доля '
  'сетевых арендаторов, частота визитов жителя района. Внизу экрана внешняя оценка: '
  'финалист RCSC Awards 2017 в категории «Малый торговый центр».',
  'Экран «Секрет успеха ТЦ Смайл»: восемь метрик объекта и премия RCSC Awards 2017'),
 ('map', '06', 'Локация',
  'Smile Family: центр притяжения района',
  'Карта района, поверх неё вторая форма. Экран отвечает сразу двоим: жителю показывает '
  'знакомые улицы, инвестору объясняет, что трафик у центра районный и берётся из '
  'соседних домов, а не из рекламы.',
  'Экран с картой района и формой заявки на посадочной странице ТРЦ Смайл'),
 ('becar', '07', 'Кто за этим стоит',
  'От объекта к компании',
  'Финальный экран переключает разговор с торгового центра на группу: 8 млн кв. м в '
  'управлении, 25 000 объектов недвижимости, 5000 сотрудников, офисы в Лондоне, Москве '
  'и Петербурге. Мировая карта собрана из дерева, чтобы блок не выглядел как сухая '
  'справка.',
  'Финальный экран посадочной: цифры группы Becar Asset Management и карта офисов'),
]

# ─── цифры объекта, которыми страница убеждает (взяты с самой посадочной) ─────
FIGURES = [
 ('7 160', 'рост среднесуточной посещаемости центра'),
 ('+115%', 'увеличилась посещаемость'),
 ('+54,4%', 'выросла доходность объекта'),
 ('+34%', 'увеличена арендопригодная площадь'),
 ('+18%', 'посещаемость выше средней по городу'),
 ('+12%', 'доход с квадратного метра выше рынка'),
 ('&gt;80%', 'площадей арендовано сетевыми арендаторами'),
 ('4-6', 'раз в месяц житель района заходит в центр'),
]

TENANTS = [
 ('perekrestok', 'Перекрёсток'), ('familiya', 'Familia'), ('modis', 'Modis'),
 ('sberbank', 'Сбербанк'), ('mts', 'МТС'), ('beeline', 'Билайн'),
 ('bukvoed', 'Буквоед'), ('kari', 'Kari'), ('obuv-com', 'Obuv.com'),
 ('trial_sport', 'Триал-Спорт'), ('redmond', 'Redmond'), ('detki', 'Детки'),
 ('equipment', 'ВсеИнструменты'), ('kotofei', 'Котофей'),
]

PALETTE = [
 ('#2AC8BB', 'Бирюза', 'фон трёх экранов из восьми'),
 ('#0A5F6A', 'Глубокая', 'шапка, поля формы, тени'),
 ('#FFC324', 'Жёлтый', 'смайл, цифры, одна кнопка'),
 ('#40307E', 'Фиолетовый', 'экран арендного бизнеса'),
 ('#5B56A6', 'Сиреневый', 'круги в фоне и вторая форма'),
 ('#FFFFFF', 'Белый', 'экраны с текстом и логотипами'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h13M13 6l6 6-6 6"/></svg>')

PAGE_CSS = """<style id="sm-css">
.sm{--teal:#2AC8BB;--teal-2:#1EA79E;--deep:#0A5F6A;--ink:#08262B;--yellow:#FFC324;
 --violet:#40307E;--violet-2:#5B56A6;--paper:#F2FAF9;--line:rgba(8,38,43,.12);
 --disp:'Montserrat',-apple-system,Arial,sans-serif;--text:'Onest','Montserrat',Arial,sans-serif;
 --mono:'JetBrains Mono',ui-monospace,Menlo,monospace;
 font-family:var(--text);color:var(--ink);background:#fff;overflow-x:clip}
.sm *,.sm *::before,.sm *::after{box-sizing:border-box}
.sm img{max-width:100%;height:auto;display:block}
.sm h1,.sm h2,.sm h3{font-family:var(--disp);font-weight:800;letter-spacing:-.02em;margin:0}
.sm h2{font-size:clamp(28px,3.5vw,46px);line-height:1.06}
.sm h3{font-size:clamp(19px,1.7vw,24px);line-height:1.2;letter-spacing:-.015em}
.sm p{margin:0;line-height:1.62}
.sm-w{max-width:1180px;margin:0 auto;padding:0 32px}
.sm-kick{display:inline-block;font-family:var(--mono);font-size:12px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--teal-2);margin-bottom:18px}
.sm-kick--on{color:rgba(255,255,255,.72)}
section{position:relative}

/* появление */
.sm-r{opacity:0;transform:translateY(22px);transition:opacity .6s ease,transform .6s cubic-bezier(.22,.9,.3,1)}
.sm-r.is-in{opacity:1;transform:none}
.js .sm-r+.sm-r{transition-delay:.06s}
@media(prefers-reduced-motion:reduce){.sm-r{opacity:1;transform:none;transition:none}}

/* ── ГЕРОЙ ───────────────────────────────────────────────────────── */
.sm-hero{background:linear-gradient(168deg,#33D2C4 0%,var(--teal) 46%,#22B0A6 100%);
 color:#fff;padding:76px 0 0;overflow:hidden;position:relative}
.sm-hero__bub{position:absolute;border-radius:50%;background:rgba(10,95,106,.28);pointer-events:none}
.sm-b1{width:520px;height:520px;left:-190px;top:130px}
.sm-b2{width:300px;height:300px;right:-60px;top:-120px;background:rgba(91,86,166,.3)}
.sm-b3{width:150px;height:150px;right:24%;bottom:120px;background:rgba(255,255,255,.14)}
.sm-hero__in{position:relative;z-index:2;display:grid;grid-template-columns:1.1fr .9fr;
 gap:48px;align-items:center;padding-bottom:56px}
.sm-hero h1{font-size:clamp(36px,5vw,68px);line-height:1.02;margin:0 0 22px}
.sm-hero h1 em{font-style:normal;color:var(--yellow)}
.sm-hero__sub{font-size:clamp(16px,1.35vw,19px);max-width:56ch;color:rgba(255,255,255,.92)}
.sm-chips{display:flex;flex-wrap:wrap;gap:9px;list-style:none;padding:0;margin:26px 0 0}
.sm-chips li{font-size:13px;font-weight:600;padding:7px 15px;border-radius:999px;
 background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.26)}
.sm-hero__cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.sm-btn{display:inline-flex;align-items:center;gap:10px;height:52px;padding:0 26px;border-radius:999px;
 font-family:var(--disp);font-weight:700;font-size:15px;text-decoration:none;transition:transform .18s,box-shadow .18s}
.sm-btn svg{width:19px;height:19px}
.sm-btn--y{background:var(--yellow);color:var(--ink);box-shadow:0 10px 26px rgba(8,38,43,.22)}
.sm-btn--gh{border:2px solid rgba(255,255,255,.55);color:#fff}
.sm-btn:hover{transform:translateY(-2px)}
.sm-btn--gh:hover{background:rgba(255,255,255,.12)}

/* живой смайл */
.sm-face{justify-self:center;text-align:center}
.sm-face svg{width:min(340px,64vw);height:auto;filter:drop-shadow(0 22px 40px rgba(8,38,43,.28))}
.sm-face__hint{margin-top:16px;font-family:var(--mono);font-size:11px;letter-spacing:.14em;
 text-transform:uppercase;color:rgba(255,255,255,.75)}
.sm-eye{transform-box:fill-box;transform-origin:center}

.sm-spec{position:relative;z-index:2;background:rgba(8,38,43,.22);
 border-top:1px solid rgba(255,255,255,.18)}
.sm-spec dl{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin:0;
 max-width:1180px;padding:22px 32px}
.sm-spec dt{font-family:var(--disp);font-weight:800;font-size:clamp(18px,1.7vw,24px)}
.sm-spec dd{margin:4px 0 0;font-size:13px;color:rgba(255,255,255,.8);line-height:1.4}

/* ── КЛИЕНТ ──────────────────────────────────────────────────────── */
.sm-about{padding:86px 0}
.sm-about__grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.sm-about p+p{margin-top:14px}
.sm-facts{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--line);
 border:1px solid var(--line);border-radius:20px;overflow:hidden}
.sm-facts div{background:#fff;padding:24px 22px}
.sm-facts b{display:block;font-family:var(--disp);font-weight:800;font-size:clamp(22px,2.4vw,32px);
 color:var(--deep);letter-spacing:-.02em}
.sm-facts span{display:block;margin-top:6px;font-size:13.5px;color:#4A6367;line-height:1.4}

/* ── ЗАДАЧА ──────────────────────────────────────────────────────── */
.sm-task{background:var(--deep);color:#fff;padding:86px 0}
.sm-task__lede{font-size:clamp(19px,2.1vw,27px);line-height:1.4;max-width:26ch;
 font-family:var(--disp);font-weight:700;letter-spacing:-.015em}
.sm-task__grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:56px;align-items:start}
.sm-task ol{list-style:none;counter-reset:t;margin:0;padding:0;display:grid;gap:24px}
.sm-task li{counter-increment:t;padding-left:56px;position:relative}
.sm-task li::before{content:counter(t,decimal-leading-zero);position:absolute;left:0;top:2px;
 font-family:var(--mono);font-size:13px;color:var(--yellow);letter-spacing:.06em}
.sm-task li b{display:block;font-family:var(--disp);font-weight:700;font-size:18px;margin-bottom:7px}
.sm-task li p{color:rgba(255,255,255,.8);font-size:15.5px}

/* ── ЖИВАЯ СТРАНИЦА ──────────────────────────────────────────────── */
.sm-live{padding:86px 0 96px;background:var(--paper)}
.sm-live__head{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-end;justify-content:space-between}
.sm-live__lede{max-width:60ch;margin-top:14px;color:#3C575B}
.sm-tabs{display:inline-flex;padding:5px;border-radius:999px;background:#fff;border:1px solid var(--line)}
.sm-tabs button{border:0;background:none;cursor:pointer;font:700 14px var(--disp);color:#4A6367;
 padding:9px 20px;border-radius:999px;transition:background .2s,color .2s}
.sm-tabs button.is-on{background:var(--deep);color:#fff}
.sm-stage{margin-top:38px;display:flex;justify-content:center}

/* ноутбук */
.sm-lap{width:min(940px,100%)}
.sm-lap__shell{background:#DFE4E7;border:1px solid #C8D0D4;border-radius:22px 22px 6px 6px;
 padding:16px 16px 20px;box-shadow:0 34px 70px rgba(8,38,43,.16)}
.sm-lap__bar{display:flex;align-items:center;gap:6px;padding:0 4px 11px}
.sm-lap__bar i{width:9px;height:9px;border-radius:50%;background:#C2CBD0}
.sm-lap__url{margin-left:12px;flex:1;height:20px;border-radius:999px;background:#EDF1F3;
 font:500 11px/20px var(--mono);color:#8A9AA0;padding:0 12px;overflow:hidden;white-space:nowrap}
.sm-screen{position:relative;border-radius:6px;overflow:hidden;background:#2AC8BB}
.sm-scroll{height:min(62vh,580px);overflow-y:auto;overflow-x:hidden;scroll-behavior:smooth;
 -webkit-overflow-scrolling:touch;overscroll-behavior:contain}
.sm-scroll img{width:100%}
.sm-scroll::-webkit-scrollbar{width:8px}
.sm-scroll::-webkit-scrollbar-thumb{background:rgba(8,38,43,.28);border-radius:8px}
.sm-lap__base{height:14px;margin:0 auto;width:106%;max-width:none;transform:translateX(-3%);
 background:linear-gradient(180deg,#D3DADE,#B9C3C8);border-radius:0 0 14px 14px}
.sm-lap__base::after{content:"";display:block;width:112px;height:5px;margin:0 auto;
 background:#A9B5BB;border-radius:0 0 6px 6px}
/* телефон */
.sm-phone{width:min(330px,84vw)}
.sm-phone__shell{background:#11282D;border-radius:42px;padding:12px;box-shadow:0 30px 60px rgba(8,38,43,.24)}
.sm-phone .sm-screen{border-radius:32px}
.sm-phone .sm-scroll{height:min(64vh,620px)}
.sm-phone__notch{position:absolute;z-index:3;top:0;left:50%;transform:translateX(-50%);
 width:110px;height:20px;background:#11282D;border-radius:0 0 14px 14px}
.sm-live__note{margin-top:26px;text-align:center;font-family:var(--mono);font-size:11.5px;
 letter-spacing:.1em;text-transform:uppercase;color:#7B9096}
.sm-prog{height:3px;border-radius:3px;background:rgba(8,38,43,.12);margin:20px auto 0;max-width:940px;overflow:hidden}
.sm-prog i{display:block;height:100%;width:0;background:var(--teal-2);border-radius:3px;transition:width .12s linear}

/* ── РАЗБОР ЭКРАНОВ ──────────────────────────────────────────────── */
.sm-scr{padding:90px 0}
.sm-scr__list{display:grid;gap:26px;margin-top:44px}
.sm-scr__item{display:grid;grid-template-columns:1.15fr .85fr;gap:38px;align-items:center;
 padding:26px;border:1px solid var(--line);border-radius:24px;background:#fff}
.sm-scr__item:nth-child(even) .sm-scr__ph{order:2}
.sm-scr__ph{border-radius:16px;overflow:hidden;background:var(--paper);
 box-shadow:0 14px 34px rgba(8,38,43,.10)}
.sm-scr__no{font-family:var(--mono);font-size:12px;letter-spacing:.14em;color:var(--teal-2)}
.sm-scr__over{display:block;margin:14px 0 8px;font-size:12.5px;font-weight:700;letter-spacing:.06em;
 text-transform:uppercase;color:#8A9AA0}
.sm-scr__txt p{margin-top:12px;color:#3C575B;font-size:15.5px}

/* ── ПОДМИГИВАНИЕ ────────────────────────────────────────────────── */
.sm-wink{background:var(--yellow);padding:70px 0}
.sm-wink__in{display:grid;grid-template-columns:230px 1fr;gap:44px;align-items:center}
.sm-wink img{width:230px;height:230px;border-radius:50%;background:#fff}
.sm-wink h2{max-width:18ch}
.sm-wink p{margin-top:16px;max-width:62ch;font-size:16.5px}
.sm-wink__file{margin-top:16px;font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;
 text-transform:uppercase;color:rgba(8,38,43,.55)}

/* ── КАЛЬКУЛЯТОР ─────────────────────────────────────────────────── */
.sm-calc{padding:88px 0;background:var(--paper)}
.sm-calc__box{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;
 background:#fff;border:1px solid var(--line);border-radius:26px;padding:40px}
.sm-calc__lede{margin-top:14px;color:#3C575B}
.sm-calc label{display:block;font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;
 text-transform:uppercase;color:#7B9096;margin-bottom:12px}
.sm-calc output{display:block;font-family:var(--disp);font-weight:800;letter-spacing:-.02em;
 font-size:clamp(26px,3vw,38px);color:var(--deep)}
.sm-calc input[type=range]{width:100%;margin:20px 0 0;accent-color:#1EA79E;height:26px}
.sm-calc__out{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:26px}
.sm-calc__out div{background:var(--paper);border-radius:16px;padding:20px}
.sm-calc__out b{display:block;font-family:var(--disp);font-weight:800;font-size:clamp(20px,2.2vw,28px);
 color:var(--teal-2);letter-spacing:-.02em}
.sm-calc__out span{display:block;margin-top:5px;font-size:13px;color:#5D767A}
.sm-calc__fine{margin-top:20px;font-size:12.5px;color:#7B9096;line-height:1.5}

/* ── ЦИФРЫ ───────────────────────────────────────────────────────── */
.sm-fig{background:linear-gradient(160deg,#2FCCBE,#159A92);color:#fff;padding:88px 0}
.sm-fig__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;margin-top:42px;
 background:rgba(255,255,255,.22);border-radius:22px;overflow:hidden}
.sm-fig__grid div{background:linear-gradient(160deg,#2FCCBE,#1AA79E);padding:28px 22px}
.sm-fig__grid b{display:block;font-family:var(--disp);font-weight:800;letter-spacing:-.02em;
 font-size:clamp(26px,3vw,38px);color:var(--yellow)}
.sm-fig__grid span{display:block;margin-top:8px;font-size:13.5px;line-height:1.45;color:rgba(255,255,255,.9)}
.sm-award{margin-top:30px;display:inline-flex;align-items:center;gap:16px;padding:18px 26px;
 border-radius:18px;background:rgba(8,38,43,.24)}
.sm-award b{font-family:var(--disp);font-weight:800;font-size:20px;color:var(--yellow);white-space:nowrap}
.sm-award span{font-size:14px;color:rgba(255,255,255,.9);line-height:1.4}

/* ── АРЕНДАТОРЫ ──────────────────────────────────────────────────── */
.sm-ten{padding:64px 0 72px;overflow:hidden}
.sm-ten__head{text-align:center;max-width:720px;margin:0 auto}
.sm-ten__head p{max-width:56ch;margin-left:auto;margin-right:auto}
.sm-ten__head p{margin-top:12px;color:#3C575B}
.sm-marq{margin-top:36px;position:relative;
 -webkit-mask-image:linear-gradient(90deg,transparent,#000 9%,#000 91%,transparent);
 mask-image:linear-gradient(90deg,transparent,#000 9%,#000 91%,transparent)}
.sm-marq__t{display:flex;width:max-content;animation:sm-marq 42s linear infinite}
.sm-marq:hover .sm-marq__t{animation-play-state:paused}
.sm-marq figure{margin:0 10px;width:186px;height:96px;border:1px solid var(--line);border-radius:16px;
 background:#fff;display:flex;align-items:center;justify-content:center;padding:16px;flex:0 0 auto}
.sm-marq img{max-height:52px;width:auto;object-fit:contain}
@keyframes sm-marq{to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.sm-marq__t{animation:none;flex-wrap:wrap;width:auto;justify-content:center}}

/* ── ПАЛИТРА ─────────────────────────────────────────────────────── */
.sm-brand{padding:88px 0;background:var(--ink);color:#fff}
.sm-brand__grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;margin-top:42px;align-items:start}
.sm-sw{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.sm-sw div{border-radius:16px;padding:16px;border:1px solid rgba(255,255,255,.14)}
.sm-sw i{display:block;height:64px;border-radius:10px;margin-bottom:12px}
.sm-sw b{display:block;font-family:var(--mono);font-size:11.5px;letter-spacing:.06em}
.sm-sw span{display:block;margin-top:5px;font-size:12.5px;color:rgba(255,255,255,.62);line-height:1.4}
.sm-type{border:1px solid rgba(255,255,255,.14);border-radius:20px;padding:28px}
.sm-type__name{font-family:var(--disp);font-weight:800;font-size:30px;letter-spacing:-.02em}
.sm-type__row{display:flex;align-items:baseline;gap:16px;padding:16px 0;border-top:1px solid rgba(255,255,255,.12)}
.sm-type__row:first-of-type{border-top:0}
.sm-type__row b{font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:rgba(255,255,255,.5);
 min-width:74px;text-transform:uppercase}
.sm-type__spec{margin-top:18px;font-size:14px;color:rgba(255,255,255,.68);line-height:1.6}
.sm-brand__rules{list-style:none;margin:34px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.sm-brand__rules li{border-top:2px solid var(--yellow);padding-top:14px;font-size:14.5px;
 color:rgba(255,255,255,.78);line-height:1.55}
.sm-brand__rules b{display:block;font-family:var(--disp);font-weight:700;color:#fff;margin-bottom:6px}

/* ── АДАПТИВ ─────────────────────────────────────────────────────── */
.sm-adapt{padding:88px 0}
.sm-adapt__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:44px}
.sm-adapt figure{margin:0}
/* три одинаковые рамки: кадры разной высоты подрезаются сверху, а не тянут строку */
.sm-adapt__ph{border-radius:26px;overflow:hidden;border:9px solid #11282D;background:#11282D;
 box-shadow:0 20px 44px rgba(8,38,43,.16);height:min(58vh,540px)}
.sm-adapt__ph img{width:100%;height:100%;object-fit:cover;object-position:top center}
.sm-adapt figcaption{margin-top:14px;font-size:14px;color:#3C575B;line-height:1.5}
.sm-adapt__note{margin-top:38px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.sm-adapt__note div{border-top:2px solid var(--teal);padding-top:14px;font-size:14.5px;color:#3C575B;line-height:1.55}
.sm-adapt__note b{display:block;font-family:var(--disp);font-weight:700;color:var(--ink);margin-bottom:6px}

/* ── РЕЗУЛЬТАТ ───────────────────────────────────────────────────── */
.sm-res{padding:88px 0 96px;background:var(--paper)}
.sm-res__grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:56px;align-items:start}
.sm-res__more{margin-top:16px;font-size:15px;color:#3C575B}
.sm-res__more a{color:var(--teal-2);font-weight:600}
.sm-res ul{list-style:none;margin:0;padding:0;display:grid;gap:18px}
.sm-res li{display:grid;grid-template-columns:34px 1fr;gap:18px;align-items:start;
 padding-bottom:18px;border-bottom:1px solid var(--line)}
.sm-res li:last-child{border-bottom:0;padding-bottom:0}
.sm-res li span:first-child{font-family:var(--mono);font-size:12px;color:var(--teal-2);padding-top:4px}
.sm-res li b{font-family:var(--disp);font-weight:700}

/* ── ПЛАНШЕТ И ТЕЛЕФОН ───────────────────────────────────────────── */
@media(max-width:1000px){
 .sm-hero__in,.sm-about__grid,.sm-task__grid,.sm-calc__box,.sm-brand__grid,
 .sm-res__grid,.sm-wink__in{grid-template-columns:1fr;gap:34px}
 .sm-face{order:-1}
 .sm-spec dl{grid-template-columns:1fr 1fr;gap:18px}
 .sm-scr__item{grid-template-columns:1fr;gap:22px}
 .sm-scr__item:nth-child(even) .sm-scr__ph{order:0}
 .sm-fig__grid{grid-template-columns:1fr 1fr}
 .sm-brand__rules,.sm-adapt__note{grid-template-columns:1fr}
 .sm-adapt__grid{grid-template-columns:1fr 1fr}
 .sm-wink img{width:180px;height:180px}
}
@media(max-width:640px){
 .sm-w{padding:0 18px}
 .sm-hero{padding-top:44px}
 .sm-hero__in{padding-bottom:38px}
 .sm-spec dl{padding:18px}
 .sm-about,.sm-task,.sm-live,.sm-scr,.sm-calc,.sm-fig,.sm-brand,.sm-adapt,.sm-res{padding:56px 0}
 .sm-facts,.sm-sw{grid-template-columns:1fr 1fr}
 .sm-fig__grid,.sm-adapt__grid,.sm-calc__out{grid-template-columns:1fr}
 .sm-calc__box{padding:24px}
 .sm-scr__item{padding:16px}
 .sm-live__head{flex-direction:column;align-items:flex-start}
 .sm-btn{height:48px;padding:0 20px;font-size:14px}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Посадочная страница ТРЦ «Смайл» для Becar: кейс разработки лендинга | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: посадочная страница инвестиционного продукта ТРЦ «Смайл» для Becar Asset Management. Восемь экранов, доходность до 13% годовых на первом экране, формы заявки, адаптив и анимации. В кейсе страница прокручивается целиком.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Посадочная страница ТРЦ «Смайл» | кейс Hand Marketing">
<meta property="og:description" content="Одностраничник, которым Becar продавал метры в действующем торговом центре в Петербурге. Дизайн, вёрстка, адаптив, формы. Страницу можно пролистать прямо в кейсе.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/hero.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


# ─── живой смайл: моргает сам, подмигивает на наведение ──────────────────────
FACE = '''<div class="sm-face sm-r">
<svg id="sm-face" viewBox="0 0 260 260" role="img"
 aria-label="Жёлтый смайл с посадочной страницы ТРЦ Смайл, который подмигивает">
 <circle cx="130" cy="130" r="122" fill="none" stroke="#fff" stroke-width="6" opacity=".85"/>
 <circle cx="130" cy="130" r="104" fill="#FFC324"/>
 <g id="sm-eyes" stroke="#fff" stroke-width="9" stroke-linecap="round">
  <line class="sm-eye" id="sm-eye-l" x1="102" y1="98" x2="102" y2="128"/>
  <line class="sm-eye" id="sm-eye-r" x1="158" y1="98" x2="158" y2="128"/>
 </g>
 <path d="M88 156c10 22 30 33 42 33s32-11 42-33" fill="none" stroke="#fff"
  stroke-width="9" stroke-linecap="round"/>
</svg>
<div class="sm-face__hint">наведите на смайл</div></div>'''


def hero():
    return (
      '<header class="sm-hero">'
      '<span class="sm-hero__bub sm-b1" aria-hidden="true"></span>'
      '<span class="sm-hero__bub sm-b2" aria-hidden="true"></span>'
      '<span class="sm-hero__bub sm-b3" aria-hidden="true"></span>'
      '<div class="sm-w sm-hero__in">'
      '<div class="sm-r">'
      '<span class="sm-kick sm-kick--on">Digital / посадочная страница / 2020</span>'
      '<h1>Одностраничник, который продаёт <em>метры в торговом центре</em></h1>'
      '<p class="sm-hero__sub">Becar Asset Management выводил на рынок непривычный продукт: '
      'долю в действующем торговом центре «Смайл» в Петербурге. Мы собрали посадочную '
      'страницу, где доходность стоит на первом экране, форма находится прямо под ней, '
      'а дальше идут доказательства, что центр работает.</p>'
      '<ul class="sm-chips"><li>Дизайн восьми экранов</li><li>Вёрстка</li>'
      '<li>Адаптив</li><li>Формы и заявки</li><li>Анимации</li></ul>'
      '<div class="sm-hero__cta">'
      f'<a class="sm-btn sm-btn--y" href="#sm-live">Пролистать страницу {ARROW}</a>'
      '<a class="sm-btn sm-btn--gh" href="#sm-screens">Разбор экранов</a>'
      '</div></div>'
      f'{FACE}'
      '</div>'
      '<div class="sm-spec"><dl class="sm-w">'
      '<div><dt>8 экранов</dt><dd>от обещания доходности до контактов отдела продаж</dd></div>'
      '<div><dt>до 13%</dt><dd>годовых, главное число всей страницы</dd></div>'
      '<div><dt>15 000 кв. м</dt><dd>площадь торгового центра в Петербурге</dd></div>'
      '<div><dt>2 формы</dt><dd>на первом экране и на карте района, плюс модальная</dd></div>'
      '</dl></div></header>')


def about():
    facts = [('8 млн кв. м', 'в управлении группы'),
             ('25 000', 'объектов недвижимости'),
             ('15 000', 'объектов сдано в аренду'),
             ('5 000', 'сотрудников в группе')]
    f = ''.join(f'<div><b>{k}</b><span>{v}</span></div>' for k, v in facts)
    return (
      '<section class="sm-about"><div class="sm-w sm-about__grid">'
      '<div class="sm-r"><span class="sm-kick">Клиент</span>'
      '<h2>Becar Asset Management</h2>'
      '<p style="margin-top:18px">Международная группа, которая проектирует, строит и '
      'управляет недвижимостью в России, США, Европе, СНГ и на Ближнем Востоке. Основана '
      'в 1992 году Александром Шараповым. Среди её проектов бизнес-центр «Станция», '
      'МФК The Loft Club, сеть апарт-отелей Vertical.</p>'
      '<p>Торговый центр «Смайл» в Петербурге входит в портфель группы. Это районный '
      'центр на 15 000 кв. м, больше 80% площадей в нём занимают сетевые арендаторы. '
      'В 2020 году Becar продавал в нём метры частным инвесторам и заказал под эту '
      'продажу отдельную посадочную страницу.</p></div>'
      f'<div class="sm-facts sm-r">{f}</div>'
      '</div></section>')


def task():
    items = [
      ('Продукт, которого нет в привычной сетке',
       'Инвестор понимает квартиру и банковский вклад. «Доля в торговом центре» требует '
       'объяснения на пальцах: кто платит аренду, кто занимается арендаторами, из чего '
       'складываются те самые 13% годовых.'),
      ('Обещанию доходности никто не верит',
       'Цифру «до 13%» можно написать на любом лендинге. Поэтому страница построена не '
       'на обещании, а на доказательствах: показатели самого объекта, список сетевых '
       'арендаторов, внешняя премия, цифры управляющей группы.'),
      ('Два разных предложения на одной странице',
       'Кроме долей в центре продавался готовый арендный бизнес: помещение «Макдональдса» '
       'на 343 кв. м с договором до 2030 года. Его нужно было показать так, чтобы он не '
       'смешался с основным предложением и не сбил человека с пути к форме.'),
    ]
    lis = ''.join(f'<li><b>{H.escape(t)}</b><p>{H.escape(p)}</p></li>' for t, p in items)
    return (
      '<section class="sm-task"><div class="sm-w sm-task__grid">'
      '<div class="sm-r"><span class="sm-kick sm-kick--on">Задача</span>'
      '<p class="sm-task__lede">Разработать посадочную страницу инвестиционного продукта '
      'ТРЦ «Смайл» и довести её до заявки в отделе продаж.</p></div>'
      f'<ol class="sm-r">{lis}</ol>'
      '</div></section>')


def live():
    return (
      '<section class="sm-live" id="sm-live"><div class="sm-w">'
      '<div class="sm-live__head sm-r">'
      '<div><span class="sm-kick">Страница целиком</span>'
      '<h2>Пролистайте её прямо здесь</h2>'
      '<p class="sm-live__lede">Внутри экрана та самая посадочная 2020 года, снятая с '
      'исходной вёрстки: все восемь блоков в том порядке, в котором их видел инвестор. '
      'Крутите колесом внутри окна или переключитесь на телефон.</p></div>'
      '<div class="sm-tabs" role="tablist" aria-label="Устройство">'
      '<button type="button" class="is-on" data-dev="desk" role="tab" aria-selected="true">Десктоп</button>'
      '<button type="button" data-dev="mob" role="tab" aria-selected="false">Телефон</button>'
      '</div></div>'
      '<div class="sm-stage sm-r">'
      # ноутбук
      '<div class="sm-lap" id="sm-lap"><div class="sm-lap__shell">'
      '<div class="sm-lap__bar"><i></i><i></i><i></i>'
      '<span class="sm-lap__url">smile.becar.ru / инвестиции в торговую недвижимость</span></div>'
      '<div class="sm-screen"><div class="sm-scroll" id="sm-scroll-d" tabindex="0">'
      f'<img src="{IMG}/page-desktop.jpg" width="1120" height="5402" loading="lazy" '
      'alt="Посадочная страница ТРЦ Смайл целиком: восемь экранов от доходности до контактов">'
      '</div></div></div><div class="sm-lap__base"></div></div>'
      # телефон
      '<div class="sm-phone" id="sm-phone" hidden><div class="sm-phone__shell">'
      '<div class="sm-screen"><span class="sm-phone__notch" aria-hidden="true"></span>'
      '<div class="sm-scroll" id="sm-scroll-m" tabindex="0">'
      f'<img src="{IMG}/page-mobile.jpg" width="500" height="7923" loading="lazy" '
      'alt="Мобильная версия посадочной страницы ТРЦ Смайл целиком">'
      '</div></div></div></div>'
      '</div>'
      '<div class="sm-prog"><i id="sm-prog"></i></div>'
      '<p class="sm-live__note">снято с исходной вёрстки проекта</p>'
      '</div></section>')


def screens():
    items = ''
    for f, no, over, title, text, alt in SCREENS:
        items += (
          '<article class="sm-scr__item sm-r">'
          f'<div class="sm-scr__ph"><img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" loading="lazy"></div>'
          f'<div class="sm-scr__txt"><span class="sm-scr__no">{no}</span>'
          f'<span class="sm-scr__over">{H.escape(over)}</span>'
          f'<h3>{H.escape(title)}</h3><p>{H.escape(text)}</p></div></article>')
    return (
      '<section class="sm-scr" id="sm-screens"><div class="sm-w">'
      '<div class="sm-r" style="max-width:64ch"><span class="sm-kick">Разбор</span>'
      '<h2>Что делает каждый экран</h2>'
      '<p style="margin-top:14px;color:#3C575B">Страница читается сверху вниз как разговор '
      'с инвестором: сначала предложение, потом доказательства, в конце компания, которая '
      'за всё это отвечает.</p></div>'
      f'<div class="sm-scr__list">{items}</div>'
      '</div></section>')


def wink():
    return (
      '<section class="sm-wink"><div class="sm-w sm-wink__in">'
      f'<img class="sm-r" src="{IMG}/smile-wink.gif" width="230" height="230" loading="lazy" '
      'alt="Анимированный смайл с посадочной страницы: жёлтый круг, который подмигивает">'
      '<div class="sm-r"><span class="sm-kick">Деталь</span>'
      '<h2>Смайл, который подмигивает</h2>'
      '<p>В задании этого не было. Логотип центра и есть улыбка, поэтому мы сделали её '
      'живой: жёлтый круг на первом экране моргает, если задержать на нём взгляд. '
      'В сдаточном письме этот пункт звучал так: «И да, если долго смотреть на смайлик, '
      'он подмигнёт». Мелочь на двадцать килобайт, из-за которой страницу показывали '
      'коллегам.</p>'
      '<p class="sm-wink__file">ball_smile.gif / 500 × 500 / 20 КБ</p>'
      '</div></div></section>')


def calc():
    return (
      '<section class="sm-calc"><div class="sm-w"><div class="sm-calc__box sm-r">'
      '<div><span class="sm-kick">Арифметика</span>'
      '<h2>Ради чего человек оставлял телефон</h2>'
      '<p class="sm-calc__lede">Весь длинный разговор на странице сводился к одному '
      'простому действию: посчитать свои деньги по ставке с первого экрана. Мы вынесли '
      'этот счёт в кейс, чтобы было видно логику продукта.</p>'
      '<p class="sm-calc__fine">Ставка «до 13% годовых» взята с посадочной страницы '
      '2020 года. Это иллюстрация к кейсу, а не инвестиционное предложение.</p></div>'
      '<div><label for="sm-sum">Сумма вложения</label>'
      '<output id="sm-sum-out" for="sm-sum">5 000 000 ₽</output>'
      '<input type="range" id="sm-sum" min="1" max="30" step="1" value="5" '
      'aria-label="Сумма вложения в миллионах рублей">'
      '<div class="sm-calc__out">'
      '<div><b id="sm-year">650 000 ₽</b><span>в год при ставке 13%</span></div>'
      '<div><b id="sm-month">54 167 ₽</b><span>в месяц</span></div>'
      '</div></div>'
      '</div></div></section>')


def figures():
    g = ''.join(f'<div><b>{k}</b><span>{v}</span></div>' for k, v in FIGURES)
    return (
      '<section class="sm-fig"><div class="sm-w">'
      '<div class="sm-r" style="max-width:62ch"><span class="sm-kick sm-kick--on">Доказательства</span>'
      '<h2>Цифры, на которых держится страница</h2>'
      '<p style="margin-top:14px;color:rgba(255,255,255,.88)">Все показатели пришли от '
      'управляющей компании и относятся к самому объекту, а не к рынку в целом. На '
      'странице они собраны в один экран, потому что по отдельности каждая цифра '
      'звучит как реклама, а вместе они читаются как отчёт.</p></div>'
      f'<div class="sm-fig__grid sm-r">{g}</div>'
      '<div class="sm-award sm-r"><b>RCSC Awards 2017</b>'
      '<span>ТЦ «Смайл» финалист номинации «Действующий торговый центр»<br>'
      'в категории «Малый торговый центр»</span></div>'
      '</div></section>')


def tenants():
    row = ''.join(
      f'<figure><img src="{IMG}/tenants/{s}.png" alt="Логотип арендатора ТЦ Смайл: {H.escape(n)}" '
      'loading="lazy" height="96"></figure>' for s, n in TENANTS)
    return (
      '<section class="sm-ten"><div class="sm-w sm-ten__head sm-r">'
      '<span class="sm-kick">Арендаторы</span>'
      '<h2>Аргумент, который узнают без объяснений</h2>'
      '<p>Четырнадцать вывесок из соседнего торгового центра работают лучше любого '
      'абзаца про стабильность арендного потока. На странице они идут каруселью сразу '
      'под цифрой 80%.</p></div>'
      f'<div class="sm-marq"><div class="sm-marq__t">{row}{row}</div></div>'
      '</section>')


def brand():
    sw = ''.join(
      f'<div><i style="background:{c}"></i><b>{c}</b><span>{H.escape(u)}</span></div>'
      for c, _n, u in PALETTE)
    rules = [
      ('Круг вместо прямоугольника',
       'Логотип центра это улыбка, поэтому круг стал основной формой: смайл, кнопки, '
       'фоновые пятна, поля формы со скруглением на всю высоту.'),
      ('Волна между экранами',
       'Экраны разделены не линиями, а волной. За счёт неё длинная страница читается '
       'как одно полотно, а не как склейка блоков.'),
      ('Жёлтый только на главном',
       'Жёлтый достаётся смайлу, цифрам и одной кнопке на экран. Всё остальное живёт '
       'на бирюзе и белом, поэтому взгляд всегда знает, куда идти.'),
    ]
    r = ''.join(f'<li><b>{H.escape(t)}</b>{H.escape(p)}</li>' for t, p in rules)
    return (
      '<section class="sm-brand"><div class="sm-w">'
      '<div class="sm-r" style="max-width:60ch"><span class="sm-kick">Как это сделано</span>'
      '<h2>Палитра и шрифт</h2></div>'
      '<div class="sm-brand__grid">'
      f'<div class="sm-sw sm-r">{sw}</div>'
      '<div class="sm-type sm-r"><div class="sm-type__name">Gotham Pro</div>'
      '<div class="sm-type__row"><b>Black</b><span style="font-weight:800;font-size:26px">СМАЙЛ 13%</span></div>'
      '<div class="sm-type__row"><b>Regular</b><span style="font-size:18px">Доходность до 13% годовых</span></div>'
      '<div class="sm-type__row"><b>Light</b><span style="font-weight:300;font-size:16px">'
      'доступные инвестиции в торговую недвижимость</span></div>'
      '<p class="sm-type__spec">Одна гарнитура на всю страницу, три начертания. Black '
      'работает на числах и заголовках, Light держит длинные абзацы, между ними ничего '
      'не нужно. Шрифт подключён файлами с сервера проекта, без внешних подгрузок.</p>'
      '</div></div>'
      f'<ul class="sm-brand__rules sm-r">{r}</ul>'
      '</div></section>')


def adapt():
    shots = [
      ('mob-hero', 500, 885,
       'Первый экран на телефоне: логотип, смайл и форма помещаются в один вертикальный кадр',
       'Первый экран собирается в столбец, но обещание и форма по-прежнему видны без прокрутки.'),
      ('mob-numbers', 500, 1435,
       'Экран с цифрами объекта в мобильной версии посадочной ТРЦ Смайл',
       'Сетка цифр из трёх колонок разворачивается в один столбец, чтобы числа не мельчали.'),
      ('mob-becar', 500, 1234,
       'Блок группы Becar в мобильной версии: своя иллюстрация вместо карты с городами',
       'У блока группы на телефоне своя иллюстрация: карта с городами на узком экране не читается.'),
    ]
    figs = ''.join(
      f'<figure class="sm-r"><div class="sm-adapt__ph"><img src="{IMG}/{f}.jpg" width="{w}" '
      f'height="{h}" loading="lazy" alt="{H.escape(alt)}"></div>'
      f'<figcaption>{H.escape(cap)}</figcaption></figure>' for f, w, h, alt, cap in shots)
    notes = [
      ('Четыре брейкпоинта', 'Раскладка пересобирается на 1024, 600 и 480 пикселях, '
       'плюс отдельные правила для телефона в портрете.'),
      ('Своя мобильная графика', 'Часть иллюстраций на телефоне заменена: там, где на '
       'десктопе дерево с городами, на узком экране стоит компактный знак.'),
      ('Формы работают везде', 'Маска телефона, проверка полей и модальное окно '
       '«Спасибо» одинаково ведут себя на всех разрешениях.'),
    ]
    n = ''.join(f'<div><b>{H.escape(t)}</b>{H.escape(p)}</div>' for t, p in notes)
    return (
      '<section class="sm-adapt"><div class="sm-w">'
      '<div class="sm-r" style="max-width:62ch"><span class="sm-kick">Адаптив</span>'
      '<h2>Телефон не уменьшенный десктоп</h2>'
      '<p style="margin-top:14px;color:#3C575B">Больше половины переходов на такие '
      'страницы приходит с телефона, поэтому мобильная версия собиралась отдельно, '
      'а не сжатием десктопной сетки.</p></div>'
      f'<div class="sm-adapt__grid">{figs}</div>'
      f'<div class="sm-adapt__note sm-r">{n}</div>'
      '</div></section>')


def result():
    items = [
      ('01', '<b>Дизайн восьми экранов</b> и вся страница целиком: от первого экрана '
       'с доходностью до контактов отдела продаж.'),
      ('02', '<b>Вёрстка без конструктора</b>, свои стили и скрипты. Страница осталась '
       'лёгкой: шрифты и картинки лежат на сервере проекта, внешних подгрузок нет.'),
      ('03', '<b>Три формы заявки</b>: на первом экране, на карте района и в модальном '
       'окне, с маской телефона, проверкой полей и экраном благодарности.'),
      ('04', '<b>Анимации по прокрутке</b> и карусель арендаторов. Ничего не двигается '
       'просто так: движение появляется там, где нужно задержать взгляд.'),
      ('05', '<b>Адаптив на все разрешения</b> с отдельной мобильной графикой, '
       'проверенный на телефонах, планшетах и широких мониторах.'),
    ]
    lis = ''.join(f'<li><span>{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="sm-res"><div class="sm-w sm-res__grid">'
      '<div class="sm-r"><span class="sm-kick">Результат</span>'
      '<h2>Что получил клиент</h2>'
      '<p class="sm-res__more">Дизайн, вёрстка, формы и поддержка страницы. Больше о '
      'направлении: <a href="/digital">услуга «Digital»</a></p></div>'
      f'<ul class="sm-r">{lis}</ul>'
      '</div></section>')


PAGE_JS = """<script>(function(){
 // ── живой смайл: моргает сам, подмигивает на наведение, следит за курсором
 var face=document.getElementById('sm-face');
 if(face&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
  var l=document.getElementById('sm-eye-l'),r=document.getElementById('sm-eye-r'),busy=false;
  function shut(el,ms){ // «закрыть глаз»: линия схлопывается по вертикали
   el.style.transition='transform .12s ease';el.style.transform='scaleY(.06)';
   setTimeout(function(){el.style.transform='scaleY(1)';},ms);}
  function blink(){if(busy)return;busy=true;shut(l,130);shut(r,130);
   setTimeout(function(){busy=false;},420);}
  function wink(){if(busy)return;busy=true;shut(r,260);
   setTimeout(function(){busy=false;},560);}
  setInterval(function(){if(Math.random()<.55)blink();},4200);
  face.addEventListener('mouseenter',wink);
  face.addEventListener('click',wink);
  face.addEventListener('mousemove',function(e){
   var b=face.getBoundingClientRect(),
       dx=Math.max(-1,Math.min(1,(e.clientX-(b.left+b.width/2))/(b.width/2))),
       dy=Math.max(-1,Math.min(1,(e.clientY-(b.top+b.height/2))/(b.height/2))),
       g=document.getElementById('sm-eyes');
   g.style.transform='translate('+(dx*7).toFixed(1)+'px,'+(dy*5).toFixed(1)+'px)';});
  face.addEventListener('mouseleave',function(){
   document.getElementById('sm-eyes').style.transform='';});
 }

 // ── мокап: переключение десктоп/телефон + полоса прокрутки
 var lap=document.getElementById('sm-lap'),ph=document.getElementById('sm-phone'),
     prog=document.getElementById('sm-prog'),
     tabs=[].slice.call(document.querySelectorAll('.sm-tabs button'));
 function track(box){
  if(!box)return;
  box.addEventListener('scroll',function(){
   var m=box.scrollHeight-box.clientHeight;
   prog.style.width=(m>0?(box.scrollTop/m*100):0).toFixed(1)+'%';});
 }
 track(document.getElementById('sm-scroll-d'));
 track(document.getElementById('sm-scroll-m'));
 tabs.forEach(function(b){b.addEventListener('click',function(){
  var mob=b.getAttribute('data-dev')==='mob';
  tabs.forEach(function(x){var on=x===b;x.classList.toggle('is-on',on);
   x.setAttribute('aria-selected',on?'true':'false');});
  lap.hidden=mob;ph.hidden=!mob;prog.style.width='0%';
  var box=document.getElementById(mob?'sm-scroll-m':'sm-scroll-d');
  if(box)box.scrollTop=0;});});

 // ── счёт по ставке с первого экрана
 var sum=document.getElementById('sm-sum');
 if(sum){
  var out=document.getElementById('sm-sum-out'),y=document.getElementById('sm-year'),
      m=document.getElementById('sm-month');
  function fmt(n){return Math.round(n).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,' ')+' \\u20BD';}
  function calc(){var v=+sum.value*1e6;out.textContent=fmt(v);
   y.textContent=fmt(v*.13);m.textContent=fmt(v*.13/12);}
  sum.addEventListener('input',calc);calc();
 }

 // ── появление блоков
 var els=[].slice.call(document.querySelectorAll('.sm-r'));
 function show(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(show);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){show(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var b=n.getBoundingClientRect();
  if(b.top<innerHeight&&b.bottom>0)show(n);else io.observe(n);});
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Digital","item":"https://hand-marketing.ru/digital/"},'
  '{"@type":"ListItem","position":3,"name":"Посадочная страница ТРЦ «Смайл»",'
  f'"item":"{URL}"}}]}}</script>')


def build():
    # Отдельного CTA-блока нет: фиолетовая форма из rc.footer() уже закрывает страницу
    body = (f'{rc.header()}<main class="sm">{hero()}{about()}{task()}{live()}{screens()}'
            f'{wink()}{calc()}{figures()}{tenants()}{brand()}{adapt()}{result()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'digital', 'becar', 'smile')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
    # CI переименовывает index-a2.html в index.html, поэтому старый A2-файл надо убрать,
    # иначе он затрёт кастомную страницу прямо на деплое. Тильда-версия остаётся в git.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
