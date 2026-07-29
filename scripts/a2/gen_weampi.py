#!/usr/bin/env python3
"""Генерит mirror/creative/becar/weampi/index.html — кейс «Брошюра We&I by Vertical
Hotel» для Becar Asset Management: печатный буклет на 24 полосы, которым отдел продаж
объяснял инвесторам формат кондо-отеля.

Дизайн-концепция: «разворот как единица смысла». Айдентика We&I построена на рубленых
фигурах, будто вырезанных ножом, в четырёх цветах: жёлтый #FDC704, оранжевый #E9511D,
тёмно-синий #033D5C, тёплый серый #BFBAB1. Те же фигуры держат вёрстку страницы:
clip-path вместо рамок, диагонали вместо линеек. Типографика self-host: Manrope
(дисплей) + Onest (текст) из /fonts/manrope-onest.css.

Главный блок — листалка из 11 разворотов, собранных из печатного PDF (вылеты 3 мм
обрезаны, полосы склеены попарно). Скролл-снап, стрелки, миниатюры, лайтбокс на полный
размер. Ассеты: mirror/images/weampi/ (scripts/weampi-assets.py).

URL кейса прежний (он в sitemap и трёх каталогах). Правки — ТОЛЬКО через этот скрипт;
build_v1 страницу пропускает по маркеру <!--custom-page-->."""
import os
import importlib.util
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/weampi'
URL = 'https://hand-marketing.ru/creative/becar/weampi/'

# ─── 11 разворотов: (полосы, заголовок, описание, alt) ───────────────────────
SPREADS = [
 ('2-3', 'Первый разворот отвечает на главный вопрос',
  'Слева обещание: продукт от Becar Asset Management, доход инвесторам идёт с сентября '
  '2020 года. Справа четыре цифры, ради которых открывают такие буклеты: до 15% годовых, '
  '100% в собственности, 87% загрузки по сети Vertical, от 3,2 млн за номер с отделкой. '
  'Дальше можно не листать, чтобы понять, о чём разговор.',
  'Разворот брошюры We&I: жёлтая полоса с логотипом и синяя полоса с четырьмя цифрами доходности'),
 ('4-5', 'Что такое кондо-отель',
  'Разворот, ради которого всё затевалось. Слева формат объясняется через сравнение с '
  'апартаментами: их покупают, чтобы жить или сдавать самому, номер в кондо-отеле берут '
  'ради дохода без личного участия. Справа аргумент «инвестируйте в то, что уже работает» '
  'и фотография готового номера.',
  'Разворот брошюры We&I с объяснением формата кондо-отеля и фотографией номера'),
 ('6-7', 'Сделка за тридцать минут',
  'Слева снимается страх бумажной волокиты: электронная регистрация договора, полчаса в '
  'офисе. Справа четыре варианта оплаты, от единовременной до ипотеки. Возражение и ответ '
  'на него стоят на одном развороте, менеджеру не нужно ничего искать.',
  'Разворот брошюры We&I: условия покупки номера и варианты оплаты'),
 ('8-9', 'А где же доход?',
  'Слева ответ одной строкой: доход уже на вашей банковской карте. Справа что можно делать '
  'с номером и три ставки в столбик: 4,8% по депозиту, 6% от квартиры, до 15% от кондо-отеля. '
  'Сравнение сделано за читателя, считать в уме не приходится.',
  'Разворот брошюры We&I со сравнением доходности депозита, квартиры и кондо-отеля'),
 ('10-11', 'Сто процентов без вашего участия',
  'Оранжевая полоса про то, что управление номером занимает одну минуту в месяц: согласовать '
  'отчёт в личном кабинете. Ниже вес компании, которая это делает: 2000 гостиничных номеров, '
  '5000 сотрудников, 8 млн кв. м в управлении, почти 30 лет на рынке.',
  'Разворот брошюры We&I: 100% арендный доход без участия собственника и цифры Becar'),
 ('12-13', 'Люди вместо рендеров',
  'Середина буклета, где разговор переключается с денег на сам отель. В кадре команда '
  'управления, напротив полароиды с номерами и коридорами. Дальше читают уже про жизнь '
  'в отеле, а не про доходность.',
  'Разворот брошюры We&I: команда управления отелем и полароиды с интерьерами'),
 ('14-15', 'Номера для своих',
  '658 номеров, 6 категорий, 15 этажей, больше 1000 кв. м общественных пространств. '
  'Справа инфраструктура иконками: кухни, коворкинг, бар, фитнес, постирочная. Список '
  'превратился в схему, которую видно целиком.',
  'Разворот брошюры We&I: цифры отеля и иконки инфраструктуры'),
 ('16-17', 'Шесть категорий в одной таблице',
  'Метраж и вместимость каждой категории, от Studio Single на одного до Team на шестерых, '
  'под каждой рендер интерьера. Чёрная плашка держит строку через оба разворота, жёлтый '
  'круг отделяет номера для компаний от одиночных.',
  'Разворот брошюры We&I: шесть категорий номеров с метражом и рендерами интерьеров'),
 ('18-19', 'Общественные пространства',
  'Слева фотография лобби на всю полосу, справа текст про комьюнити, живую музыку и '
  'настолки. Финальная строка жёлтым: не просто стены и кровать, а целая жизнь, полная '
  'впечатлений. Это же обещание работает на загрузку отеля.',
  'Разворот брошюры We&I: лобби отеля и текст про комьюнити'),
 ('20-21', 'Пауза без единого слова',
  'Коллаж из фотографий отеля, вырезанный теми же угловатыми фигурами. Разворот работает '
  'как вдох перед практической частью и держит темп: после плотных цифр читателю нужно '
  'просто посмотреть.',
  'Разворот брошюры We&I: фотоколлаж лобби и общественных пространств без текста'),
 ('22-23', 'Как добраться',
  'Адрес на Большом Сампсониевском, аргументы за Петербург и карта района с таймингами: '
  'метро 10 минут, набережная Большой Невки 7, Пулково 35. Брошюра заканчивается тем, '
  'что можно проверить самому.',
  'Разворот брошюры We&I: карта района на Большом Сампсониевском с таймингами до метро и Пулково'),
]

MOCKUPS = [
 ('mock-float.jpg', 'Развороты про сделку и про команду отеля'),
 ('mock-rooms.jpg', 'Категории номеров: таблица работает через сгиб'),
 ('mock-navy.jpg', 'Тёмный разворот про инфраструктуру'),
 ('mock-hundred.jpg', 'Разворот про доход без личного участия'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 5l-7 7 7 7"/></svg>')
GRIP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M9 6l-5 6 5 6M15 6l5 6-5 6"/></svg>')

PAGE_CSS = """<style id="wi-css">
:root{
 --wi-navy:#033d5c;--wi-navy-d:#02293e;--wi-orange:#e9511d;--wi-yellow:#fdc704;
 --wi-sand:#bfbab1;--wi-paper:#f2efe9;--wi-ink:#14161a;--wi-ink2:#5a6169;
 --wi-df:'Manrope',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --wi-bf:'Onest',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --wi-z:1000}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.wi{font-family:var(--wi-bf);color:var(--wi-ink);background:#fff;line-height:1.62;
 font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.wi *{box-sizing:border-box}
.wi img{max-width:100%;height:auto;display:block}
.wi a{color:inherit;text-decoration:none}
.wi h1,.wi h2,.wi h3,.wi h4{font-family:var(--wi-df);font-weight:800;line-height:1.05;
 letter-spacing:-.03em;margin:0;text-wrap:balance}
.wi p{text-wrap:pretty}
.wi-w{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,52px)}
.wi-kick{font-family:var(--wi-df);font-weight:700;font-size:12.5px;letter-spacing:.15em;
 text-transform:uppercase;display:inline-flex;align-items:center;gap:10px}
.wi-kick::before{content:"";width:22px;height:3px;background:currentColor}
.wi-num{font-family:var(--wi-df);font-weight:800;font-variant-numeric:tabular-nums}
.wi-btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--wi-df);
 font-weight:700;font-size:15px;padding:.92em 1.45em;border:0;cursor:pointer;
 transition:transform .25s,background .25s,color .25s,border-color .25s}
.wi-btn svg{width:1.1em;height:1.1em}
.wi-btn--y{background:var(--wi-yellow);color:var(--wi-ink);
 clip-path:polygon(0 0,100% 4%,99% 100%,1% 96%)}
.wi-btn--y:hover{transform:translateY(-2px)}
.wi-btn--gh{background:transparent;color:#fff;border:1.6px solid rgba(255,255,255,.34)}
.wi-btn--gh:hover{border-color:#fff;transform:translateY(-2px)}

/* ── HERO ── */
.wi-hero{position:relative;background:var(--wi-navy);color:#fff;overflow:hidden}
.wi-cut{position:absolute;pointer-events:none;z-index:1}
.wi-cut--y{top:-6%;right:-4%;width:38vw;max-width:520px;aspect-ratio:1/.86;
 background:var(--wi-yellow);clip-path:polygon(16% 0,100% 9%,86% 100%,0 78%)}
/* повтор логотипа внутри жёлтой фигуры: тот же приём, что на обложке и заднике буклета.
   Блок заведомо больше фигуры и обрезается ею, строки со сбивкой, чтобы не читалось
   как ровная сетка */
.wi-cut__type{position:absolute;left:-30%;top:-16%;width:180%;transform:rotate(-7deg);
 font-family:var(--wi-df);font-weight:800;font-size:clamp(24px,3.1vw,46px);line-height:.98;
 letter-spacing:.03em;color:var(--wi-ink);white-space:nowrap}
.wi-cut__type span{display:block}
.wi-cut--o{bottom:-30%;left:-13%;width:32vw;max-width:400px;aspect-ratio:1/1;
 background:var(--wi-orange);clip-path:polygon(0 12%,88% 0,100% 82%,22% 100%)}
/* только вертикальные отступы: padding-шорткат затёр бы боковые из .wi-w */
.wi-hero__in{position:relative;z-index:2;padding-top:clamp(26px,3.4vw,40px);
 padding-bottom:clamp(52px,6vw,78px)}
.wi-hero__top{display:flex;align-items:baseline;gap:8px 18px;flex-wrap:wrap;
 padding-bottom:clamp(38px,6vw,74px)}
.wi-logo{font-family:var(--wi-df);font-weight:800;font-size:clamp(21px,2.4vw,27px);
 letter-spacing:.02em}
.wi-logo b{color:var(--wi-yellow)}
.wi-hero__by{font-size:13.5px;color:rgba(255,255,255,.6);letter-spacing:.02em}
.wi-hero__grid{display:grid;grid-template-columns:1.02fr .98fr;gap:clamp(28px,4vw,60px);
 align-items:center}
.wi-hero .wi-kick{color:var(--wi-yellow)}
.wi-hero h1{font-size:clamp(36px,5.6vw,68px);margin:16px 0 0;max-width:15ch}
.wi-hero h1 em{font-style:normal;color:var(--wi-yellow)}
.wi-hero__sub{margin:clamp(18px,2.4vw,26px) 0 0;font-size:clamp(16px,1.45vw,18.5px);
 color:rgba(255,255,255,.78);max-width:50ch}
.wi-chips{display:flex;flex-wrap:wrap;gap:8px;margin:clamp(22px,2.6vw,30px) 0 0;padding:0;list-style:none}
.wi-chips li{padding:7px 14px;border:1.5px solid rgba(255,255,255,.26);font-size:12.5px;
 font-weight:600;color:rgba(255,255,255,.9)}
.wi-hero__cta{margin-top:clamp(24px,3vw,34px);display:flex;gap:12px;flex-wrap:wrap}
.wi-hero__ph{position:relative}
.wi-hero__ph img{box-shadow:0 40px 80px -40px rgba(0,0,0,.75)}
.wi-hero__stamp{position:absolute;right:-6px;top:-22px;background:var(--wi-orange);color:#fff;
 font-family:var(--wi-df);font-weight:800;font-size:12.5px;letter-spacing:.05em;
 padding:11px 15px;line-height:1.25;text-align:center;transform:rotate(3deg);
 box-shadow:0 12px 26px rgba(0,0,0,.32)}
.wi-hero__stamp b{display:block;font-size:19px;letter-spacing:0}
/* спец-строка */
.wi-spec{position:relative;z-index:2;background:var(--wi-navy-d)}
.wi-spec__in{max-width:1240px;margin:0 auto;padding:22px clamp(20px,4vw,52px);
 display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.wi-spec div{padding-left:15px;border-left:3px solid var(--wi-yellow)}
.wi-spec dt{font-family:var(--wi-df);font-weight:800;font-size:clamp(19px,2vw,25px);
 color:#fff;letter-spacing:-.02em}
.wi-spec dd{margin:3px 0 0;font-size:12.5px;color:rgba(255,255,255,.62);line-height:1.4}

/* ── О КЛИЕНТЕ ── */
.wi-about{background:var(--wi-paper);padding:clamp(58px,7.5vw,100px) 0}
.wi-about .wi-kick{color:var(--wi-orange)}
.wi-about__grid{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(28px,5vw,64px);
 align-items:start}
.wi-about h2{font-size:clamp(26px,3.2vw,40px);margin-top:14px}
.wi-about p{margin:20px 0 0;font-size:clamp(15.5px,1.3vw,17.5px);color:#2f343a;max-width:60ch}
.wi-about b{font-weight:700;color:var(--wi-ink)}
.wi-geo{display:flex;flex-wrap:wrap;gap:7px;margin:24px 0 0;padding:0;list-style:none}
.wi-geo li{background:#fff;border:1px solid #e2ded6;padding:6px 12px;font-size:13px;
 color:#3f454b}
.wi-about__facts{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:#e2ded6;
 border:1px solid #e2ded6}
.wi-about__fact{background:#fff;padding:22px 20px 24px}
.wi-about__fact b{display:block;font-family:var(--wi-df);font-weight:800;
 font-size:clamp(24px,2.6vw,32px);letter-spacing:-.03em;line-height:1;color:var(--wi-navy)}
.wi-about__fact span{display:block;margin-top:8px;font-size:13px;color:var(--wi-ink2);line-height:1.4}
.wi-about__note{margin-top:2px;background:var(--wi-navy);color:#fff;padding:20px}
.wi-about__note b{display:block;font-family:var(--wi-df);font-weight:800;font-size:15px;
 color:var(--wi-yellow);margin-bottom:6px}
.wi-about__note span{font-size:14px;color:rgba(255,255,255,.82);line-height:1.55}

/* ── ЗАДАЧА ── */
.wi-task{padding:clamp(60px,8vw,110px) 0;background:#fff}
.wi-task__grid{display:grid;grid-template-columns:1.12fr .88fr;gap:clamp(28px,5vw,66px);
 align-items:start}
.wi-task .wi-kick{color:var(--wi-orange)}
.wi-task h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px}
.wi-task__lede p{margin:0 0 1.1em;font-size:clamp(16px,1.35vw,18.5px);color:#2f343a;max-width:62ch}
.wi-task__lede p:last-child{margin-bottom:0}
.wi-task__lede b{font-weight:700;color:var(--wi-ink)}
.wi-note{background:var(--wi-orange);color:#fff;padding:30px 28px;
 clip-path:polygon(0 2%,100% 0,98% 100%,2% 97%)}
.wi-note h3{font-size:21px;margin:0 0 12px}
.wi-note p{margin:0;font-size:15.5px;line-height:1.6;color:rgba(255,255,255,.92)}
.wi-note__tag{display:inline-block;background:var(--wi-ink);color:var(--wi-yellow);
 font-family:var(--wi-df);font-weight:800;font-size:11.5px;letter-spacing:.1em;
 padding:6px 12px;margin-bottom:16px}

/* ── ШТОРКА «ТЗ И ДИЗАЙН» ── */
.wi-cmp{background:var(--wi-paper);padding:clamp(60px,8vw,110px) 0}
.wi-cmp .wi-kick{color:var(--wi-orange)}
.wi-cmp__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:22px;
 flex-wrap:wrap;padding-bottom:clamp(24px,3vw,36px)}
.wi-cmp__hd h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:18ch}
.wi-cmp__hint{font-size:15px;color:var(--wi-ink2);max-width:40ch}
.wi-cmp__box{position:relative;aspect-ratio:2/1;overflow:hidden;background:#fff;
 --p:50%;box-shadow:0 26px 60px -38px rgba(3,61,92,.6)}
.wi-cmp__box img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.wi-cmp__box img.b{clip-path:inset(0 0 0 var(--p))}
.wi-cmp__lbl{position:absolute;top:14px;z-index:3;background:rgba(2,25,38,.78);color:#fff;
 font-family:var(--wi-df);font-weight:800;font-size:11.5px;letter-spacing:.1em;
 text-transform:uppercase;padding:7px 12px;backdrop-filter:blur(6px);pointer-events:none}
.wi-cmp__lbl.l{left:14px}
.wi-cmp__lbl.r{right:14px;background:var(--wi-yellow);color:var(--wi-ink)}
.wi-cmp__bar{position:absolute;top:0;bottom:0;left:var(--p);width:3px;z-index:2;
 background:var(--wi-yellow);pointer-events:none;transform:translateX(-1.5px)}
.wi-cmp__grip{position:absolute;top:50%;left:var(--p);z-index:3;width:46px;height:46px;
 margin:-23px 0 0 -23px;border-radius:50%;background:var(--wi-yellow);color:var(--wi-ink);
 display:grid;place-items:center;pointer-events:none;box-shadow:0 8px 22px rgba(0,0,0,.3)}
.wi-cmp__grip svg{width:22px;height:22px}
.wi-cmp__range{position:absolute;inset:0;z-index:4;width:100%;height:100%;margin:0;
 opacity:0;cursor:ew-resize;-webkit-appearance:none;appearance:none;background:none}
.wi-cmp__range::-webkit-slider-thumb{-webkit-appearance:none;width:46px;height:100%}
.wi-cmp__range::-moz-range-thumb{width:46px;height:400px;border:0;background:none}
.wi-cmp__range:focus-visible{outline:3px solid var(--wi-yellow);outline-offset:3px}
.wi-cmp__cap{margin:18px 0 0;font-size:15px;color:var(--wi-ink2);max-width:76ch}

/* ── ДВЕ ЛИНИИ ── */
.wi-lines{background:#fff;padding:clamp(60px,8vw,110px) 0}
.wi-lines .wi-kick{color:var(--wi-orange)}
.wi-lines h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:20ch}
.wi-lines__lede{margin:18px 0 0;font-size:clamp(16px,1.35vw,18.5px);color:#2f343a;max-width:66ch}
.wi-lines__row{margin-top:clamp(34px,4.4vw,54px);display:grid;grid-template-columns:1fr 1fr;gap:2px}
.wi-line{padding:32px 30px 34px;color:#fff}
.wi-line--a{background:var(--wi-navy)}
.wi-line--b{background:var(--wi-orange)}
.wi-line__n{font-family:var(--wi-df);font-weight:800;font-size:12.5px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--wi-yellow)}
.wi-line h3{font-size:clamp(21px,2.2vw,27px);margin:12px 0 12px}
.wi-line p{margin:0 0 18px;font-size:15.5px;color:rgba(255,255,255,.86)}
.wi-line ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.wi-line li{position:relative;padding-left:20px;font-size:14.5px;color:rgba(255,255,255,.92)}
.wi-line li::before{content:"";position:absolute;left:0;top:.55em;width:9px;height:9px;
 background:var(--wi-yellow);clip-path:polygon(0 0,100% 18%,82% 100%,10% 84%)}
.wi-line--b li::before{background:#fff}  /* жёлтый на оранжевом не читается */
.wi-line--b .wi-line__n{color:#fff}

/* ── ЛИСТАЛКА РАЗВОРОТОВ ── */
.wi-book{background:var(--wi-navy);color:#fff;padding:clamp(58px,7.5vw,104px) 0;overflow:hidden}
.wi-book .wi-kick{color:var(--wi-yellow)}
.wi-book__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:22px;
 flex-wrap:wrap;padding-bottom:clamp(26px,3.4vw,42px)}
.wi-book__hd h2{font-size:clamp(28px,3.8vw,48px);margin-top:12px}
.wi-book__hint{font-size:14px;color:rgba(255,255,255,.58);max-width:32ch}
.wi-track{display:flex;gap:clamp(14px,2vw,26px);overflow-x:auto;scroll-snap-type:x mandatory;
 scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.wi-track::-webkit-scrollbar{display:none}
.wi-slide{flex:0 0 100%;scroll-snap-align:center;margin:0}
.wi-slide__ph{position:relative;background:#02293e;cursor:zoom-in;overflow:hidden}
.wi-slide__ph img{width:100%;aspect-ratio:2/1;object-fit:cover}
.wi-slide__ph::after{content:"";position:absolute;top:0;bottom:0;left:50%;width:2px;
 background:linear-gradient(180deg,rgba(0,0,0,.16),rgba(0,0,0,.05));pointer-events:none}
.wi-slide__pg{position:absolute;left:0;top:0;z-index:2;background:var(--wi-yellow);
 color:var(--wi-ink);font-family:var(--wi-df);font-weight:800;font-size:12px;
 letter-spacing:.08em;padding:7px 13px}
.wi-slide__zoom{position:absolute;right:12px;bottom:12px;z-index:2;background:rgba(2,25,38,.72);
 color:#fff;font-size:12px;font-weight:600;padding:7px 12px;backdrop-filter:blur(6px);
 opacity:0;transition:opacity .25s}
.wi-slide__ph:hover .wi-slide__zoom{opacity:1}
.wi-slide figcaption{padding:24px 2px 0;display:grid;grid-template-columns:.62fr 1.38fr;
 gap:clamp(14px,3vw,40px);align-items:start;min-height:132px}
.wi-slide figcaption h3{font-size:clamp(19px,2vw,25px);color:#fff}
.wi-slide figcaption p{margin:0;font-size:15.5px;color:rgba(255,255,255,.72);max-width:64ch}
.wi-nav{margin-top:clamp(18px,2.4vw,28px);display:flex;align-items:center;
 justify-content:space-between;gap:18px;flex-wrap:wrap}
.wi-nav__btns{display:flex;align-items:center;gap:10px}
.wi-arrow{width:46px;height:46px;display:grid;place-items:center;background:transparent;
 border:1.6px solid rgba(255,255,255,.3);color:#fff;cursor:pointer;
 transition:background .2s,border-color .2s,opacity .2s}
.wi-arrow svg{width:20px;height:20px}
.wi-arrow--next svg{transform:rotate(180deg)}
.wi-arrow:hover{background:var(--wi-yellow);border-color:var(--wi-yellow);color:var(--wi-ink)}
.wi-arrow[disabled]{opacity:.28;cursor:default}
.wi-arrow[disabled]:hover{background:transparent;border-color:rgba(255,255,255,.3);color:#fff}
.wi-count{font-family:var(--wi-df);font-weight:800;font-size:15px;letter-spacing:.04em;
 color:rgba(255,255,255,.55);min-width:5.5em}
.wi-count b{color:var(--wi-yellow)}
.wi-thumbs{display:flex;gap:7px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.wi-thumbs::-webkit-scrollbar{display:none}
.wi-thumb{flex:0 0 auto;width:74px;padding:0;border:0;background:none;cursor:pointer;
 opacity:.42;transition:opacity .22s,outline-color .22s;outline:2px solid transparent;
 outline-offset:2px}
.wi-thumb img{width:100%;aspect-ratio:2/1;object-fit:cover}
.wi-thumb:hover{opacity:.8}
.wi-thumb.is-on{opacity:1;outline-color:var(--wi-yellow)}

/* ── ГРАФИКА ── */
.wi-craft{padding:clamp(60px,8vw,110px) 0;background:#fff}
.wi-craft__grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,64px);align-items:center}
.wi-craft .wi-kick{color:var(--wi-orange)}
.wi-craft h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px}
.wi-craft p{font-size:clamp(16px,1.35vw,18.5px);color:#2f343a;max-width:58ch}
.wi-craft p+p{margin-top:1.05em}
.wi-pal{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;margin-top:clamp(26px,3vw,36px)}
.wi-sw{padding:66px 12px 14px;color:#fff}
.wi-sw span{display:block;font-family:var(--wi-df);font-weight:800;font-size:12px;letter-spacing:.06em}
.wi-sw small{display:block;font-size:11.5px;opacity:.75;margin-top:2px}
.wi-sw--y{background:var(--wi-yellow);color:var(--wi-ink)}
.wi-sw--o{background:var(--wi-orange)}
.wi-sw--n{background:var(--wi-navy)}
.wi-sw--s{background:var(--wi-sand);color:var(--wi-ink)}
.wi-craft__ph figure{margin:0}
.wi-craft__ph img{box-shadow:0 30px 60px -34px rgba(3,61,92,.55)}
.wi-craft__ph figcaption{margin-top:14px;font-size:14px;color:var(--wi-ink2)}

/* ── В ПЕЧАТИ ── */
.wi-print{background:var(--wi-sand);padding:clamp(58px,7.5vw,104px) 0}
.wi-print .wi-kick{color:var(--wi-navy)}
.wi-print h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;color:var(--wi-ink)}
.wi-print__lede{margin:16px 0 0;font-size:clamp(16px,1.35vw,18.5px);color:#3a3f45;max-width:60ch}
.wi-print__grid{margin-top:clamp(32px,4vw,48px);display:grid;grid-template-columns:repeat(2,1fr);
 gap:clamp(16px,2vw,26px)}
.wi-print figure{margin:0;background:#fff}
.wi-print figure img{width:100%;aspect-ratio:4/3;object-fit:cover}
.wi-print figcaption{padding:14px 16px 16px;font-size:14px;color:var(--wi-ink2)}
.wi-print__specs{margin-top:clamp(28px,3.4vw,40px);display:flex;flex-wrap:wrap;gap:10px}
.wi-print__specs span{background:var(--wi-navy);color:#fff;font-family:var(--wi-df);
 font-weight:700;font-size:13px;padding:9px 15px}

/* ── РЕЗУЛЬТАТ ── */
.wi-res{padding:clamp(60px,8vw,110px) 0;background:#fff}
.wi-res__grid{display:grid;grid-template-columns:.78fr 1.22fr;gap:clamp(24px,5vw,64px);align-items:start}
.wi-res .wi-kick{color:var(--wi-orange)}
.wi-res h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px}
.wi-res__list{list-style:none;margin:0;padding:0;display:grid;gap:18px}
.wi-res__list li{display:flex;gap:18px;font-size:clamp(16px,1.3vw,18px);color:#2f343a;
 padding-bottom:18px;border-bottom:1px solid #e7e4de}
.wi-res__list li:last-child{border-bottom:0;padding-bottom:0}
.wi-res__list b{font-weight:700;color:var(--wi-ink)}
.wi-res__list .wi-num{color:var(--wi-orange);flex:none;font-size:17px;min-width:2.4em;padding-top:.04em}
.wi-res__more{margin:20px 0 0;font-size:15px;color:var(--wi-ink2);max-width:34ch}
.wi-res__more a{color:var(--wi-navy);font-weight:600;text-decoration:underline;text-underline-offset:3px}


/* ── ЛАЙТБОКС ── */
.wi-lb{position:fixed;inset:0;z-index:var(--wi-z);display:none;align-items:center;
 justify-content:center;padding:clamp(12px,3vw,44px);background:rgba(2,20,31,.94)}
.wi-lb.is-open{display:flex}
.wi-lb__box{position:relative;width:min(1500px,100%)}
.wi-lb__box img{width:100%;height:auto;max-height:82vh;object-fit:contain}
.wi-lb__cap{margin-top:14px;color:rgba(255,255,255,.8);font-size:14px}
.wi-lb__x{position:absolute;top:-46px;right:0;width:38px;height:38px;
 border:1.4px solid rgba(255,255,255,.4);background:transparent;color:#fff;font-size:22px;
 line-height:1;cursor:pointer;transition:background .2s,border-color .2s}
.wi-lb__x:hover{background:rgba(255,255,255,.14);border-color:#fff}

/* ── REVEAL ── */
html.no-js .wi-r{opacity:1!important;transform:none!important}
.wi-r{opacity:0;transform:translateY(22px);
 transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.wi-r.is-in{opacity:1;transform:none}

/* ── АДАПТИВ ── */
@media(max-width:1020px){
 /* фигура становится узкой: повтор логотипа в ней распадается на обрывки, убираем,
    саму фигуру поднимаем, чтобы не наезжала на строку с клиентом */
 .wi-cut__type{display:none}
 .wi-cut--y{top:-12%;width:30vw;max-width:300px}
 .wi-hero__grid{grid-template-columns:1fr;gap:30px}
 .wi-hero__ph{order:-1}
 .wi-spec__in{grid-template-columns:repeat(2,1fr)}
 .wi-task__grid,.wi-craft__grid,.wi-res__grid,.wi-about__grid{grid-template-columns:1fr;gap:26px}
 .wi-lines__row{grid-template-columns:1fr}
 .wi-slide figcaption{grid-template-columns:1fr;gap:10px;min-height:0}
}
@media(max-width:680px){
 .wi{font-size:16px}
 .wi-hero__stamp{right:auto;left:-4px;top:-16px;font-size:11.5px;padding:9px 12px}
 .wi-print__grid{grid-template-columns:1fr}
 .wi-about__facts{grid-template-columns:1fr}
 .wi-pal{grid-template-columns:repeat(2,1fr)}
 .wi-sw{padding:46px 12px 12px}
 .wi-slide__ph img{aspect-ratio:2/1}
 .wi-nav{gap:12px}
 .wi-thumbs{order:3;width:100%}
 .wi-lb__x{top:-38px}
}
@media(max-width:420px){
 .wi-spec__in{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){
 .wi-r{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .wi *{transition-duration:.01ms!important;scroll-behavior:auto}
 .wi-track{scroll-behavior:auto}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Брошюра We&amp;I by Vertical Hotel для Becar: 24 полосы про кондо-отель | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: печатная брошюра кондо-отеля We&amp;I by Vertical Hotel для Becar Asset Management. 24 полосы, 11 разворотов, квадрат 210×210 мм, полноцвет 4+4. Копирайтинг, вёрстка и препресс: буклет объясняет инвестору формат кондо-отеля и показывает отель изнутри.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Брошюра We&amp;I by Vertical Hotel | кейс Hand Marketing">
<meta property="og:description" content="24 полосы и 11 разворотов, которыми отдел продаж Becar объяснял инвесторам формат кондо-отеля. Копирайтинг, вёрстка, препресс, печать 4+4.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/mock-cover.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def cut_type():
    """Заливка жёлтой фигуры повтором «we&i»: 11 строк со сбивкой по горизонтали,
    лишнее срезает clip-path самой фигуры."""
    offsets = ['0', '1.1em', '-.5em', '.7em', '-.9em', '.4em',
               '1.4em', '-.3em', '.9em', '-1.1em', '.2em']
    rows = ''.join(f'<span style="margin-left:{o}">we&amp;i we&amp;i we&amp;i</span>'
                   for o in offsets)
    return f'<div class="wi-cut__type">{rows}</div>'


def hero():
    return (
      '<header class="wi-hero">'
      f'<div class="wi-cut wi-cut--y" aria-hidden="true">{cut_type()}</div>'
      '<div class="wi-cut wi-cut--o"></div>'
      '<div class="wi-w wi-hero__in">'
      '<div class="wi-hero__top">'
      '<span class="wi-logo">we<b>&amp;</b>i <span style="font-weight:500;opacity:.7">by Vertical Hotel</span></span>'
      # клиент держим слева рядом с лого: справа в шапку заходит жёлтая фигура
      '<span class="wi-hero__by">Becar Asset Management, Санкт-Петербург</span>'
      '</div>'
      '<div class="wi-hero__grid">'
      '<div>'
      '<span class="wi-kick">Полиграфия и копирайтинг</span>'
      '<h1>Брошюра, которая объясняет <em>кондо-отель</em> за один просмотр</h1>'
      '<p class="wi-hero__sub">Becar выводил на рынок We&amp;I by Vertical Hotel: отель, '
      'где номер покупают как бизнес, а не как квартиру. Формат был новым, объяснять его '
      'приходилось с нуля. Мы собрали буклет на 24 полосы, который делает это за менеджера.</p>'
      '<ul class="wi-chips"><li>Концепция издания</li><li>Копирайтинг</li>'
      '<li>Вёрстка разворотов</li><li>Препресс и печать</li></ul>'
      '<div class="wi-hero__cta">'
      f'<a class="wi-btn wi-btn--y" href="#wi-book">Листать развороты {ARROW}</a>'
      '<a class="wi-btn wi-btn--gh" href="#wi-print">Как выглядит в печати</a>'
      '</div></div>'
      '<div class="wi-hero__ph">'
      '<div class="wi-hero__stamp">Рекорды рынка<br>недвижимости 2020<b>#1</b></div>'
      f'<img src="{IMG}/mock-cover.jpg" width="1680" height="1260" '
      'alt="Печатная брошюра We&amp;I by Vertical Hotel: обложка и раскрытый первый разворот" '
      'loading="eager" fetchpriority="high">'
      '</div></div></div>'
      '<div class="wi-spec"><dl class="wi-spec__in">'
      '<div><dt>24 полосы</dt><dd>11 разворотов плюс обложка и задник</dd></div>'
      '<div><dt>210×210 мм</dt><dd>квадрат, чтобы не выглядеть каталогом недвижимости</dd></div>'
      '<div><dt>4+4</dt><dd>полноцвет с двух сторон, вылеты 3 мм</dd></div>'
      '<div><dt>Сентябрь 2020</dt><dd>файл ушёл в типографию в PDF/X-1a</dd></div>'
      '</dl></div></header>')


def about():
    """Справка о клиенте. Цифры взяты с разворота 10-11 самой брошюры."""
    facts = [('2000', 'гостиничных номеров под управлением'),
             ('5000', 'сотрудников в группе'),
             ('8 млн кв. м', 'недвижимости в управлении'),
             ('≈30 лет', 'на рынке недвижимости')]
    cells = ''.join(f'<div class="wi-about__fact"><b>{k}</b><span>{H.escape(v)}</span></div>'
                    for k, v in facts)
    geo = ''.join(f'<li>{g}</li>' for g in
                  ('Россия', 'США', 'Европа', 'СНГ', 'Ближний Восток'))
    return (
      '<section class="wi-about"><div class="wi-w wi-about__grid">'
      '<div class="wi-r"><span class="wi-kick">О клиенте</span>'
      '<h2>Becar Asset Management</h2>'
      '<p>Международная группа компаний, которая работает с недвижимостью почти тридцать '
      'лет: управление и техническая эксплуатация, девелопмент, собственные сети апарт- '
      'и кондо-отелей. Группа ровесница российского рынка недвижимости: росла вместе с ним '
      'и переносила сюда западные практики, за что в отрасли её негласно называли '
      '«русским разведчиком» на Западе.</p>'
      '<p><b>We&amp;I by Vertical Hotel</b> входит в сеть Vertical. Для инвестора это '
      'ключевая часть предложения: он покупает не отдельные стены с кроватью, а номер '
      'в работающей сети с общими каналами продаж, корпоративными договорами и программой '
      'лояльности. Поэтому в буклете цифры группы стоят сразу за обещанием дохода.</p>'
      f'<ul class="wi-geo">{geo}</ul></div>'
      '<div class="wi-r">'
      f'<div class="wi-about__facts">{cells}</div>'
      '<div class="wi-about__note"><b>Что это меняло для брошюры</b>'
      '<span>Инвестор доверяет не отелю, а тому, кто им управляет. Эти четыре цифры '
      'работают как гарантия и вынесены на отдельный разворот.</span></div>'
      '</div></div></section>')


def task():
    return (
      '<section class="wi-task"><div class="wi-w wi-task__grid">'
      '<div class="wi-r"><span class="wi-kick">Задача</span>'
      '<h2>Продать не метры, а схему</h2>'
      '<div class="wi-task__lede" style="margin-top:22px">'
      '<p>Кондо-отель в 2020 году путали с апартаментами. Инвестор видел знакомое слово '
      '«номер» и достраивал остальное сам: сдача, поиск жильцов, ремонт после каждого гостя. '
      'Продавать нужно было другое: <b>схему, где всей операционкой занимается управляющая '
      'компания</b>, а собственник раз в месяц подтверждает отчёт в личном кабинете.</p>'
      '<p>Отель к тому моменту уже работал и приносил доход, но у отдела продаж не было '
      'материала, который держит этот разговор от первой страницы до последней. Была '
      'айдентика We&amp;I, была фактура и были цифры, разложенные по разным файлам.</p>'
      '</div></div>'
      '<div class="wi-note wi-r"><span class="wi-note__tag">Сложность</span>'
      '<h3>У брошюры два читателя</h3>'
      '<p>Инвестор считает доходность и сроки. Будущий гость смотрит, захочет ли он тут '
      'жить, потому что от этого зависит загрузка, а значит и доход инвестора. Оба должны '
      'найти своё, не пролистывая чужое.</p></div>'
      '</div></section>')


def compare():
    """Шторка «ТЗ и дизайн»: слева файл клиента, справа наш разворот 10-11."""
    return (
      '<section class="wi-cmp"><div class="wi-w">'
      '<div class="wi-cmp__hd wi-r"><div><span class="wi-kick">С чего начинали</span>'
      '<h2>ТЗ и дизайн</h2></div>'
      '<p class="wi-cmp__hint">Потяните ползунок: слева разворот про доход, каким он '
      'пришёл от клиента, справа тот же разворот в буклете.</p></div>'
      '<div class="wi-cmp__box wi-r" id="wi-cmp">'
      f'<img class="a" src="{IMG}/brief.jpg" width="1680" height="840" '
      'alt="Исходный файл клиента: текст разворота про арендный доход без вёрстки" loading="lazy">'
      f'<img class="b" src="{IMG}/spread-05.jpg" width="2500" height="1250" '
      'alt="Тот же разворот в готовой брошюре We&amp;I: оранжевая плашка со 100% и цифры Becar" '
      'loading="lazy">'
      '<span class="wi-cmp__lbl l">ТЗ</span><span class="wi-cmp__lbl r">Дизайн</span>'
      '<span class="wi-cmp__bar"></span>'
      f'<span class="wi-cmp__grip">{GRIP}</span>'
      '<input class="wi-cmp__range" id="wi-cmp-range" type="range" min="0" max="100" '
      'value="50" step="0.5" aria-label="Сравнить ТЗ и готовый разворот">'
      '</div>'
      '<p class="wi-cmp__cap wi-r">Тот же смысл и те же цифры. Разница в том, что слева '
      'их надо читать подряд, а справа видно сразу: крупное «100%», четыре показателя '
      'компании и вопрос, на который отвечает менеджер.</p>'
      '</div></section>')


def lines():
    a = ('<div class="wi-line wi-line--a">'
         '<span class="wi-line__n">Развороты 1-5</span><h3>Линия инвестора</h3>'
         '<p>Сначала деньги: сколько приносит, кто управляет, как проходит сделка.</p>'
         '<ul><li>Доходность и стоимость номера в первых же цифрах</li>'
         '<li>Формат кондо-отеля в сравнении с апартаментами</li>'
         '<li>Условия покупки: оплата, рассрочка, ипотека</li>'
         '<li>Вес управляющей компании: 2000 номеров, 8 млн кв. м</li></ul></div>')
    b = ('<div class="wi-line wi-line--b">'
         '<span class="wi-line__n">Развороты 6-11</span><h3>Линия гостя</h3>'
         '<p>Потом отель: кто здесь работает, как выглядят номера, зачем сюда возвращаются.</p>'
         '<ul><li>Команда управления вместо безликих рендеров</li>'
         '<li>Шесть категорий номеров с метражом и вместимостью</li>'
         '<li>Общественные пространства, лобби и комьюнити</li>'
         '<li>Район, транспорт и тайминги до ключевых точек</li></ul></div>')
    return (
      '<section class="wi-lines"><div class="wi-w">'
      '<div class="wi-r" style="max-width:70ch"><span class="wi-kick">Решение</span>'
      '<h2>Две линии, один буклет</h2>'
      '<p class="wi-lines__lede">Мы развели разговоры по половинам издания и связали их '
      'одной графикой. Первая половина говорит с инвестором, вторая переводит разговор на '
      'сам отель. Стыка не чувствуется, потому что логика простая: сначала во что вы '
      'вкладываете, потом почему сюда будут возвращаться.</p></div>'
      f'<div class="wi-lines__row wi-r">{a}{b}</div>'
      '</div></section>')


def book():
    slides, thumbs = '', ''
    total = len(SPREADS)
    for i, (pg, title, text, alt) in enumerate(SPREADS, 1):
        src = f'{IMG}/spread-{i:02d}.jpg'
        eager = 'eager' if i == 1 else 'lazy'
        slides += (
          f'<figure class="wi-slide" data-i="{i}">'
          f'<div class="wi-slide__ph wi-zoom" role="button" tabindex="0" data-src="{src}" '
          f'data-cap="Разворот {i} из {total}: {H.escape(title)}. Полосы {pg}" '
          f'aria-label="Открыть разворот {i} на весь экран">'
          f'<span class="wi-slide__pg">Полосы {pg}</span>'
          f'<img src="{src}" width="2500" height="1250" alt="{alt}" loading="{eager}">'
          f'<span class="wi-slide__zoom">Открыть крупно</span></div>'
          f'<figcaption><h3>{H.escape(title)}</h3><p>{text}</p></figcaption></figure>')
        thumbs += (f'<button class="wi-thumb{" is-on" if i == 1 else ""}" data-go="{i}" '
                   f'type="button" aria-label="Разворот {i}, полосы {pg}">'
                   f'<img src="{IMG}/thumb-{i:02d}.jpg" width="220" height="110" alt="" '
                   f'loading="lazy"></button>')
    return (
      '<section class="wi-book" id="wi-book"><div class="wi-w">'
      '<div class="wi-book__hd wi-r"><div><span class="wi-kick">Развороты</span>'
      f'<h2>{total} разворотов, {total * 2 + 2} полосы</h2></div>'
      '<p class="wi-book__hint">Буклет читали в руках, поэтому здесь он тоже собран '
      'разворотами. Нажмите на разворот, чтобы рассмотреть его целиком.</p></div>'
      f'<div class="wi-track" id="wi-track">{slides}</div>'
      '<div class="wi-nav"><div class="wi-nav__btns">'
      f'<button class="wi-arrow wi-arrow--prev" id="wi-prev" type="button" aria-label="Предыдущий разворот">{CHEV}</button>'
      f'<button class="wi-arrow wi-arrow--next" id="wi-next" type="button" aria-label="Следующий разворот">{CHEV}</button>'
      f'<span class="wi-count" id="wi-count"><b>01</b> / {total:02d}</span></div>'
      f'<div class="wi-thumbs" id="wi-thumbs">{thumbs}</div>'
      '</div></div></section>')


def craft():
    return (
      '<section class="wi-craft"><div class="wi-w wi-craft__grid">'
      '<div class="wi-r"><span class="wi-kick">Графика</span>'
      '<h2>Фигуры, вырезанные ножом</h2>'
      '<p style="margin-top:22px">Айдентика We&amp;I держится на рубленых формах: '
      'плашки заходят друг на друга под углом, углы срезаны, ничего не выровнено по линейке. '
      'Мы сделали эти фигуры каркасом вёрстки. Они держат воздух, разделяют колонки без '
      'разделительных линий и переходят через сгиб, поэтому <b>разворот читается как одна '
      'картинка</b>, а не как две страницы рядом.</p>'
      '<p>Четыре цвета работают как навигация. Синий отвечает за цифры и деньги, '
      'оранжевый за акценты и всё, что нужно запомнить, жёлтый за жизнь в отеле, тёплый '
      'серый даёт паузу между плотными разворотами.</p>'
      '<div class="wi-pal">'
      '<div class="wi-sw wi-sw--n"><span>Синий</span><small>#033D5C</small></div>'
      '<div class="wi-sw wi-sw--o"><span>Оранжевый</span><small>#E9511D</small></div>'
      '<div class="wi-sw wi-sw--y"><span>Жёлтый</span><small>#FDC704</small></div>'
      '<div class="wi-sw wi-sw--s"><span>Тёплый серый</span><small>#BFBAB1</small></div>'
      '</div></div>'
      '<div class="wi-craft__ph wi-r"><figure>'
      f'<img src="{IMG}/spread-08.jpg" width="2500" height="1250" '
      'alt="Разворот брошюры We&amp;I: чёрная плашка с категориями номеров проходит через сгиб" '
      'loading="lazy">'
      '<figcaption>Чёрная плашка с категориями номеров идёт через сгиб, а жёлтый круг '
      'отделяет номера для компаний. Сгиб перестаёт быть границей.</figcaption>'
      '</figure></div>'
      '</div></section>')


def printing():
    figs = ''.join(
      f'<figure><img src="{IMG}/{f}" alt="Мокап печатной брошюры We&amp;I: {H.escape(c.lower())}" '
      f'loading="lazy"><figcaption>{H.escape(c)}</figcaption></figure>' for f, c in MOCKUPS)
    return (
      '<section class="wi-print" id="wi-print"><div class="wi-w">'
      '<div class="wi-r" style="max-width:64ch"><span class="wi-kick">В печати</span>'
      '<h2>Квадрат на столе переговорной</h2>'
      '<p class="wi-print__lede">Квадратный формат выбрали намеренно: он необычно лежит '
      'на столе и не похож на очередной каталог недвижимости. Файл ушёл в типографию '
      'в PDF/X-1a, с вылетами и полноцветом с двух сторон.</p></div>'
      f'<div class="wi-print__grid wi-r">{figs}</div>'
      '<div class="wi-print__specs wi-r"><span>24 полосы</span><span>210×210 мм</span>'
      '<span>Вылеты 3 мм</span><span>Полноцвет 4+4</span><span>PDF/X-1a</span></div>'
      '</div></section>')


def result():
    items = [
      ('24', 'Готовый макет на <b>24 полосы</b> с препрессом: вылеты, полноцвет, '
       'PDF/X-1a. В типографию ушёл файл, а не набор пожеланий.'),
      ('11', '<b>Одиннадцать разворотов</b>, каждый закрывает один вопрос и заканчивается '
       'цифрой. Менеджеру не нужно пересказывать буклет, он открывает нужный разворот.'),
      ('1', '<b>Один визуальный язык</b> на всё издание: рубленые фигуры, четыре цвета '
       'и крупная цифра как точка в конце разворота.'),
      ('#1', 'Знак победителя премии «Рекорды рынка недвижимости 2020» в номинации '
       '«Недвижимость для инвестиций» стоит прямо на обложке.'),
    ]
    lis = ''.join(f'<li><span class="wi-num">{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="wi-res"><div class="wi-w wi-res__grid">'
      '<div class="wi-r"><span class="wi-kick">Результат</span>'
      '<h2>Что получил клиент</h2>'
      '<p class="wi-res__more">Концепция, тексты, вёрстка и препресс. Больше о направлении: '
      '<a href="/creativedesign">услуга «Creative&nbsp;&amp;&nbsp;Design»</a></p></div>'
      f'<ul class="wi-res__list wi-r">{lis}</ul>'
      '</div></section>')


LIGHTBOX = ('<div class="wi-lb" id="wi-lb" aria-hidden="true">'
            '<div class="wi-lb__box">'
            '<button class="wi-lb__x" id="wi-lb-x" type="button" aria-label="Закрыть">&times;</button>'
            '<img id="wi-lb-img" src="" alt="">'
            '<div class="wi-lb__cap" id="wi-lb-cap"></div></div></div>')

PAGE_JS = """<script>(function(){
 var track=document.getElementById('wi-track');
 if(track){
  var slides=[].slice.call(track.querySelectorAll('.wi-slide')),
      thumbs=[].slice.call(document.querySelectorAll('.wi-thumb')),
      prev=document.getElementById('wi-prev'),next=document.getElementById('wi-next'),
      count=document.getElementById('wi-count'),cur=1,total=slides.length;
  function pad(n){return n<10?'0'+n:''+n;}
  function mark(i){cur=i;
   count.innerHTML='<b>'+pad(i)+'</b> / '+pad(total);
   thumbs.forEach(function(t,k){t.classList.toggle('is-on',k===i-1);});
   prev.disabled=(i===1);next.disabled=(i===total);
   var t=thumbs[i-1];
   if(t&&t.parentNode.scrollWidth>t.parentNode.clientWidth){
    var box=t.parentNode,l=t.offsetLeft-(box.clientWidth-t.offsetWidth)/2;
    box.scrollTo({left:l,behavior:'smooth'});}
  }
  function go(i){i=Math.min(total,Math.max(1,i));
   track.scrollTo({left:slides[i-1].offsetLeft-track.offsetLeft,behavior:'smooth'});mark(i);}
  prev.addEventListener('click',function(){go(cur-1);});
  next.addEventListener('click',function(){go(cur+1);});
  thumbs.forEach(function(t){t.addEventListener('click',function(){go(+t.getAttribute('data-go'));});});
  // активный слайд по скроллу (свайп на телефоне)
  var tmr;
  track.addEventListener('scroll',function(){clearTimeout(tmr);tmr=setTimeout(function(){
   var mid=track.scrollLeft+track.clientWidth/2,best=1,d=1e9;
   slides.forEach(function(s,k){var c=s.offsetLeft-track.offsetLeft+s.offsetWidth/2,
    dd=Math.abs(c-mid);if(dd<d){d=dd;best=k+1;}});
   if(best!==cur)mark(best);},90);});
  track.addEventListener('keydown',function(e){
   if(e.key==='ArrowRight'){e.preventDefault();go(cur+1);}
   if(e.key==='ArrowLeft'){e.preventDefault();go(cur-1);}});
  mark(1);
 }
 // шторка «ТЗ и дизайн»
 var cmp=document.getElementById('wi-cmp'),cr=document.getElementById('wi-cmp-range');
 if(cmp&&cr){var set=function(){cmp.style.setProperty('--p',cr.value+'%');};
  cr.addEventListener('input',set);set();}
 // лайтбокс разворотов
 var lb=document.getElementById('wi-lb'),lbi=document.getElementById('wi-lb-img'),
     lbc=document.getElementById('wi-lb-cap'),lbx=document.getElementById('wi-lb-x');
 function open(src,cap,alt){lbi.src=src;lbi.alt=alt||'';lbc.textContent=cap||'';
  lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';lbx.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  lbi.removeAttribute('src');document.body.style.overflow='';}
 [].forEach.call(document.querySelectorAll('.wi-zoom'),function(z){
  function fire(){var im=z.querySelector('img');
   open(z.getAttribute('data-src'),z.getAttribute('data-cap'),im?im.alt:'');}
  z.addEventListener('click',fire);
  z.addEventListener('keydown',function(e){
   if(e.key==='Enter'||e.key===' '){e.preventDefault();fire();}});});
 lbx.addEventListener('click',close);
 lb.addEventListener('click',function(e){if(e.target===lb||e.target===lb.firstChild)close();});
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape'&&lb.classList.contains('is-open'))close();});
 // reveal
 var els=[].slice.call(document.querySelectorAll('.wi-r'));
 function show(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(show);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){show(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)show(n);else io.observe(n);});
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Брошюра We&I by Vertical Hotel",'
  f'"item":"{URL}"}}]}}</script>')


def build():
    # Отдельного CTA-блока нет: фиолетовая форма из rc.footer() уже закрывает страницу,
    # второй «Обсудить проект» был бы дублем (как на CeramicaNova и OBO)
    body = (f'{rc.header()}<main class="wi">{hero()}{about()}{task()}{compare()}{lines()}{book()}'
            f'{craft()}{printing()}{result()}</main>{LIGHTBOX}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'becar', 'weampi')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
    # CI переименовывает index-a2.html в index.html, поэтому старый A2-файл надо убрать,
    # иначе он затрёт кастомную страницу прямо на деплое. Прежняя Tilda-версия остаётся
    # в истории git.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
