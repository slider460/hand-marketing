#!/usr/bin/env python3
"""Генерит mirror/creative/saintgobain/calendar/index.html — кейс «Концепция
новогоднего календаря Saint-Gobain» (разработана в 2020-м, календарь на 2021).

Дизайн-концепция: страница ведёт себя как сам календарь, то есть как белый лист,
который наполняется цветом. Отсюда три вещи, которых нет в исходной презентации:
  • линия-город. Знак Saint-Gobain это город, нарисованный одной ломаной, а
    коробка карандашей с первой полосы даёт ровно такой же силуэт. Линия обведена
    по фактическим срезам карандашей (scripts/sgcalendar-assets.py) и рисуется
    при появлении блока;
  • конструктор: один и тот же имидж в трёх конструкциях (1/2/4 пружины),
    переключается на месте, вместе с картинкой меняется таблица характеристик;
  • раскраска: под линейной графикой открытки лежит canvas, посетитель закрашивает
    рисунок цветами из знака Saint-Gobain. Это прямая цитата тезиса презентации
    «раскраска это тоже творчество».

Ассеты: mirror/images/sgcalendar/ (scripts/sgcalendar-assets.py).
Обложки карточки каталога: scripts/gen-sgcalendar-covers.py.
Карточка в каталогах: scripts/sgcalendar-catalog.py.

Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import html as H
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/sgcalendar'
URL = 'https://hand-marketing.ru/creative/saintgobain/calendar/'

SKYLINE = open(os.path.join(ROOT, 'images', 'sgcalendar', 'skyline.svg'), encoding='utf-8').read()

# ─── иллюстрации: (файл, из чего, что получилось, текст, alt, ширина, высота) ─
IDEAS = [
    ('idea-footballer', 'Молоток + карандаш', 'Футболист',
     'Боёк молотка работает мячом, деревянная рукоятка телом, всё остальное дорисовано '
     'тушью в три движения. Удар в кадре появился раньше, чем сам рисунок.',
     'Иллюстрация из молотка и карандаша: футболист бьёт по мячу, рукоятка молотка образует корпус',
     900, 900),
    ('idea-flamingo', 'Рулетка + отвёртка + метр', 'Фламинго',
     'Измерительная лента даёт изгиб шеи, отвёртка становится головой с клювом, сложенный '
     'метр раскрывается в оперение и ногу. Ни одной дорисованной детали.',
     'Иллюстрация из рулетки, отвёртки и складного метра: фламинго стоит на одной ноге',
     750, 752),
    ('idea-narwhal', 'Сверло по бетону', 'Нарвал',
     'Спиральная канавка бура читается как витой рог, тело написано акварелью в один серый '
     'тон. Инструмент остаётся инструментом и одновременно становится животным.',
     'Иллюстрация из сверла по бетону: нарвал, у которого бур работает витым рогом',
     900, 900),
]

# ─── полосы календаря: (файл, цифра, подпись, бренд, заголовок, текст, alt, ш, в) ──
SHEETS = [
    ('mock-gyproc', '12', 'Декабрь', 'Gyproc',
     'Потолочный профиль превращается в башню',
     'Зимний город нарисован синей линией от руки, а единственная фотография в кадре это сам '
     'профиль ПП. Перфорация металла читается как окна небоскрёба, брызги краски работают '
     'снегом. Под изображением идёт короткая справка ровно для того, кто будет этот профиль '
     'ставить: разметка не нужна, шаг корректируется по месту, саморез входит в любую точку.',
     'Полоса календаря Saint-Gobain: потолочный профиль Gyproc в виде небоскрёба среди нарисованного зимнего города',
     1200, 1632),
    ('mock-isover', '07', 'Июль', 'ISOVER',
     'Плита утеплителя становится пляжем',
     'Жёлтый торец плиты ISOVER Профи стал песчаной косой с зонтиками, а сразу за ней '
     'начинается холодное море с айсбергом. Это и есть работа утеплителя, показанная одной '
     'картинкой: с одной стороны от него холод, с другой тепло. Штриховка сделана вручную '
     'и держит всю полосу на двух цветах.',
     'Полоса календаря Saint-Gobain: плита утеплителя ISOVER в виде пляжа с зонтиками рядом с айсбергом',
     900, 1982),
    ('mock-cover', '', 'Обложка', 'Saint-Gobain',
     'Обложку отдают незакрашенной',
     'Верхний лист собран из плотного орнамента: шары, спирали, чешуя, ёлочные шишки. '
     'Клиент получает его чёрно-белым, в коробке рядом лежат маркеры. Это приглашение взяться '
     'за календарь до того, как начнётся год.',
     'Обложка календаря Saint-Gobain: чёрно-белый орнамент-раскраска в подарочной коробке',
     900, 1264),
]

# ─── конструкции: (ключ, файл, кнопка, заголовок, текст, [(характеристика, значение)], в) ──
BUILDS = [
    ('b1', 'build-1', '1 пружина', 'Одна пружина, один блок',
     'Имидж во всю высоту, под ним единый блок с тремя месяцами. Самый простой в сборке '
     'и самый дешёвый вариант. Текущий месяц приходится искать глазами внутри общей сетки.',
     [('Имидж', 'во всю высоту'), ('Блоков дат', 'один'), ('Дата с трёх метров', 'читается хуже'),
      ('Сборка', 'самая простая')], 1737),
    ('b2', 'build-2', '2 пружины', 'Две пружины, два блока',
     'Имидж и даты разделены второй пружиной, название месяца выносится прямо на иллюстрацию. '
     'Картинка почти ничего не теряет, а сетка получает собственное поле и перестаёт спорить '
     'с рисунком.',
     [('Имидж', 'почти во всю высоту'), ('Блоков дат', 'два'), ('Дата с трёх метров', 'читается'),
      ('Сборка', 'средняя')], 1735),
    ('b4', 'build-4', '4 пружины', 'Четыре пружины, четыре блока',
     'Привычный квартальный формат: три отдельных блока по месяцам плюс имидж сверху. '
     'Даты видно с другого конца комнаты, но иллюстрация ужимается примерно вдвое.',
     [('Имидж', 'верхняя треть'), ('Блоков дат', 'три'), ('Дата с трёх метров', 'читается лучше всего'),
      ('Сборка', 'самая дорогая')], 1727),
]

# ─── палитра раскраски: цвета взяты из знака Saint-Gobain ────────────────────
INKS = [
    ('#3FC8A9', 'Мятный'), ('#34BDEC', 'Голубой'), ('#1350E0', 'Синий'),
    ('#7A28B0', 'Фиолетовый'), ('#EE0F3F', 'Красный'), ('#F5591D', 'Оранжевый'),
    ('#F4C300', 'Жёлтый'),
]

PAPERS = [
    ('sheet-card', 'Открытка', 468, 382,
     'Линейный рисунок с открытки: стопка новогодних подарочных коробок с узорами'),
    ('sheet-cover', 'Обложка', 613, 875,
     'Орнамент с обложки календаря: круги, спирали и чешуя'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 5l-7 7 7 7"/></svg>')

PAGE_CSS = """<style id="sg-css">
:root{
 --sg-mint:#3FC8A9;--sg-cyan:#34BDEC;--sg-blue:#1350E0;--sg-navy:#16309B;
 --sg-violet:#7A28B0;--sg-red:#EE0F3F;--sg-orange:#F5591D;
 --sg-ink:#14161c;--sg-ink2:#5b6270;--sg-line:rgba(20,22,28,.13);
 --sg-df:'Montserrat',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --sg-bf:'Onest',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --sg-mf:'JetBrains Mono',ui-monospace,SFMono-Regular,Consolas,monospace;
 --sg-grad:linear-gradient(90deg,#3FC8A9,#34BDEC 28%,#1350E0 46%,#7A28B0 56%,#EE0F3F 72%,#F5591D)}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.sg{font-family:var(--sg-bf);color:var(--sg-ink);background:#fff;line-height:1.62;
 font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.sg *{box-sizing:border-box}
.sg img{max-width:100%;height:auto;display:block}
.sg a{color:inherit}
.sg h1,.sg h2,.sg h3{font-family:var(--sg-df);font-weight:800;line-height:1.05;
 letter-spacing:-.03em;margin:0;text-wrap:balance}
.sg p{text-wrap:pretty}
.sg-w{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,52px)}
.sg-kick{font-family:var(--sg-mf);font-weight:700;font-size:12px;letter-spacing:.14em;
 text-transform:uppercase;display:inline-flex;align-items:center;gap:10px;color:var(--sg-ink2)}
.sg-kick::before{content:"";width:26px;height:3px;background:var(--sg-grad)}
.sg-btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--sg-df);
 font-weight:800;font-size:15px;padding:.95em 1.5em;border:0;cursor:pointer;border-radius:999px;
 text-decoration:none;transition:transform .25s,background .25s,color .25s,border-color .25s}
.sg-btn svg{width:1.1em;height:1.1em}
/* .sg a{color:inherit} специфичнее одного класса, поэтому у ссылок-кнопок
   цвет задаём с тегом: иначе белая надпись на чёрной кнопке становится чёрной */
.sg a.sg-btn--p,.sg-btn--p{background:var(--sg-ink);color:#fff}
.sg-btn--p:hover{transform:translateY(-2px);background:var(--sg-blue)}
.sg a.sg-btn--gh,.sg-btn--gh{background:transparent;color:var(--sg-ink);
 border:2px solid var(--sg-line)}
.sg-btn--gh:hover{border-color:var(--sg-ink);transform:translateY(-2px)}

/* ── ГЕРОЙ ── */
.sg-hero{padding:clamp(30px,4.5vw,60px) 0 0}
.sg-hero__grid{display:grid;grid-template-columns:1.02fr .98fr;gap:clamp(26px,4.5vw,64px);
 align-items:center}
.sg-hero__client{display:flex;align-items:center;gap:14px;margin-bottom:clamp(18px,2.4vw,26px)}
.sg-hero__client img{width:clamp(124px,13vw,166px)}
.sg-hero__client span{font-family:var(--sg-mf);font-size:11.5px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--sg-ink2);border-left:1px solid var(--sg-line);padding-left:14px}
.sg-hero h1{font-size:clamp(32px,5vw,64px);max-width:15ch}
.sg-hero__sub{margin:clamp(16px,2vw,24px) 0 0;font-size:clamp(16px,1.4vw,19px);
 color:#33374a;max-width:52ch}
.sg-chips{display:flex;flex-wrap:wrap;gap:8px;margin:clamp(20px,2.4vw,28px) 0 0;padding:0;list-style:none}
.sg-chips li{padding:6px 14px;border:1px solid var(--sg-line);border-radius:999px;
 font-size:12.5px;font-weight:600;color:var(--sg-ink2)}
.sg-hero__cta{margin-top:clamp(22px,3vw,32px);display:flex;gap:12px;flex-wrap:wrap}
/* фото карандашей + обведённая по ним линия-город */
.sg-fig{position:relative}
.sg-fig img{width:100%}
.sg-sky{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.sg-sky path{transition:stroke-dashoffset 2.6s cubic-bezier(.35,.8,.3,1)}
.sg-cap{margin:16px 0 0;font-size:13.5px;line-height:1.55;color:var(--sg-ink2);max-width:46ch}
.sg-cap b{color:var(--sg-ink);font-weight:700}
.sg-redraw{margin-top:8px;background:none;border:0;padding:0;cursor:pointer;font:600 13px var(--sg-bf);
 color:var(--sg-blue);border-bottom:1px solid currentColor}
.sg-spec{margin-top:clamp(32px,5vw,66px);border-top:1px solid var(--sg-line);
 border-bottom:1px solid var(--sg-line)}
.sg-spec__in{max-width:1240px;margin:0 auto;padding:22px clamp(20px,4vw,52px);
 display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.sg-spec dt{font-family:var(--sg-df);font-weight:800;font-size:clamp(24px,2.6vw,34px);
 letter-spacing:-.03em;line-height:1}
.sg-spec div:nth-child(1) dt{color:var(--sg-mint)}
.sg-spec div:nth-child(2) dt{color:var(--sg-blue)}
.sg-spec div:nth-child(3) dt{color:var(--sg-red)}
.sg-spec div:nth-child(4) dt{color:var(--sg-orange)}
.sg-spec dd{margin:6px 0 0;font-family:var(--sg-mf);font-size:11.5px;letter-spacing:.08em;
 text-transform:uppercase;color:var(--sg-ink2);line-height:1.4}

/* ── ЗАДАЧА ── */
.sg-task{padding:clamp(58px,7.5vw,104px) 0}
.sg-task__grid{display:grid;grid-template-columns:1.06fr .94fr;gap:clamp(28px,5vw,66px);align-items:start}
.sg-task h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px}
.sg-task p{margin:20px 0 0;font-size:clamp(15.5px,1.3vw,17.5px);color:#33374a;max-width:58ch}
.sg-task b{font-weight:700;color:var(--sg-ink)}
.sg-task__side{border-left:3px solid transparent;border-image:var(--sg-grad) 1;
 padding-left:clamp(18px,2.4vw,28px)}
.sg-task__side h3{font-size:clamp(18px,1.8vw,22px)}
.sg-task__side ul{margin:14px 0 0;padding:0;list-style:none;display:grid;gap:12px}
.sg-task__side li{font-size:15.5px;color:#33374a;padding-left:22px;position:relative}
.sg-task__side li::before{content:"";position:absolute;left:0;top:.62em;width:10px;height:2px;
 background:var(--sg-red)}
.sg-quote{margin:clamp(34px,4.5vw,54px) 0 0;padding:clamp(24px,3.4vw,40px) 0;
 border-top:1px solid var(--sg-line);border-bottom:1px solid var(--sg-line);
 font-family:var(--sg-df);font-weight:800;font-size:clamp(19px,2.6vw,32px);line-height:1.2;
 letter-spacing:-.025em;max-width:24ch}
.sg-quote span{background:var(--sg-grad);-webkit-background-clip:text;background-clip:text;color:transparent}

/* ── ИДЕЯ ── */
.sg-idea{background:#f6f7f8;padding:clamp(58px,7.5vw,104px) 0}
.sg-idea h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:18ch}
.sg-idea__lede{margin:18px 0 0;max-width:60ch;color:#33374a;font-size:clamp(15.5px,1.3vw,17.5px)}
.sg-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2.4vw,30px);
 margin-top:clamp(28px,3.6vw,46px);padding:0;list-style:none}
.sg-card{background:#fff;display:flex;flex-direction:column}
.sg-card>img{aspect-ratio:1/1;object-fit:cover;width:100%}
.sg-card__b{padding:clamp(18px,2vw,24px)}
.sg-card__pair{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;
 font-family:var(--sg-mf);font-size:11.5px;letter-spacing:.05em;text-transform:uppercase}
.sg-card__pair i{font-style:normal;color:var(--sg-ink2)}
.sg-card__pair s{text-decoration:none;color:var(--sg-red);font-weight:700}
.sg-card h3{font-size:clamp(20px,2vw,26px);margin-top:10px}
.sg-card p{margin:12px 0 0;font-size:15px;color:#33374a}

/* ── ПОЛОСЫ КАЛЕНДАРЯ ── */
.sg-cal{padding:clamp(58px,7.5vw,104px) 0 clamp(20px,3vw,34px)}
.sg-cal h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:20ch}
.sg-cal__lede{margin:18px 0 0;max-width:60ch;color:#33374a;font-size:clamp(15.5px,1.3vw,17.5px)}
.sg-sheet{display:grid;grid-template-columns:.92fr 1.08fr;gap:clamp(24px,4vw,58px);
 align-items:center;padding:clamp(34px,5vw,68px) 0;border-bottom:1px solid var(--sg-line)}
/* nth-of-type, а не nth-child: в этой же обёртке лежат шапка секции и подсказка,
   и обычный nth-child сдвинул бы чередование на одну полосу */
.sg-sheet:nth-of-type(even){grid-template-columns:1.08fr .92fr}
.sg-sheet:nth-of-type(even) .sg-sheet__t{order:2}
.sg-sheet__n{display:flex;align-items:baseline;gap:12px}
.sg-sheet__n b{font-family:var(--sg-df);font-weight:800;font-size:clamp(44px,6vw,84px);
 line-height:.85;letter-spacing:-.05em;font-variant-numeric:tabular-nums;
 background:var(--sg-grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.sg-sheet__n span{font-family:var(--sg-mf);font-size:11.5px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--sg-ink2)}
.sg-sheet h3{font-size:clamp(21px,2.4vw,31px);margin-top:16px;max-width:17ch}
.sg-sheet p{margin:14px 0 0;font-size:16px;color:#33374a;max-width:48ch}
.sg-shot{border:0;padding:0;background:none;cursor:zoom-in;display:block;width:100%;
 transition:transform .3s}
.sg-shot:hover{transform:translateY(-4px)}
/* мокапы полос очень высокие (900×2000), без потолка по высоте один разворот
   растягивал бы экран на два с половиной */
.sg-shot img{margin:0 auto;max-height:min(76vh,740px);width:auto;
 filter:drop-shadow(0 34px 54px rgba(20,22,28,.22))}
.sg-cal__hint{margin:22px 0 0;font-size:13.5px;color:var(--sg-ink2)}

/* ── КОНСТРУКЦИИ ── */
.sg-build{background:var(--sg-ink);color:#fff;padding:clamp(58px,7.5vw,104px) 0}
.sg-build .sg-kick{color:rgba(255,255,255,.6)}
.sg-build h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:16ch}
.sg-build__lede{margin:18px 0 0;max-width:58ch;color:rgba(255,255,255,.74);font-size:clamp(15.5px,1.3vw,17.5px)}
.sg-tabs{display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(26px,3.4vw,40px)}
.sg-tabs button{cursor:pointer;background:transparent;border:2px solid rgba(255,255,255,.2);
 color:#fff;padding:10px 20px;border-radius:999px;font:800 13.5px var(--sg-df);
 transition:background .2s,border-color .2s,color .2s}
.sg-tabs button:hover{border-color:rgba(255,255,255,.6)}
.sg-tabs button[aria-selected=true]{background:#fff;border-color:#fff;color:var(--sg-ink)}
.sg-build__box{display:grid;grid-template-columns:.85fr 1.15fr;gap:clamp(24px,4vw,60px);
 align-items:center;margin-top:clamp(24px,3vw,38px)}
.sg-build__pane[hidden]{display:none}
.sg-build__pane{display:contents}
.sg-build__t h3{font-size:clamp(20px,2.2vw,28px)}
.sg-build__t p{margin:14px 0 0;font-size:15.5px;color:rgba(255,255,255,.76);max-width:44ch}
.sg-build__t dl{margin:clamp(20px,2.6vw,30px) 0 0;display:grid;gap:0}
.sg-build__t dl>div{display:flex;justify-content:space-between;gap:16px;
 border-top:1px solid rgba(255,255,255,.16);padding:11px 0}
.sg-build__t dt{font-family:var(--sg-mf);font-size:11.5px;letter-spacing:.08em;
 text-transform:uppercase;color:rgba(255,255,255,.55)}
.sg-build__t dd{margin:0;font-size:14.5px;font-weight:600;text-align:right}
.sg-build__pic{display:flex;justify-content:center}
.sg-build__pic img{max-height:min(74vh,700px);width:auto;
 filter:drop-shadow(0 34px 60px rgba(0,0,0,.5))}

/* ── РАСКРАСКА ── */
.sg-color{padding:clamp(58px,7.5vw,104px) 0}
.sg-color h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:16ch}
.sg-color__lede{margin:18px 0 0;max-width:56ch;color:#33374a;font-size:clamp(15.5px,1.3vw,17.5px)}
.sg-color__grid{display:grid;grid-template-columns:.78fr 1.22fr;gap:clamp(26px,4vw,60px);
 align-items:start;margin-top:clamp(28px,3.6vw,44px)}
.sg-tools{display:grid;gap:18px}
.sg-tools h3{font-family:var(--sg-mf);font-weight:700;font-size:11.5px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--sg-ink2)}
.sg-inks{display:flex;flex-wrap:wrap;gap:9px;margin-top:10px}
.sg-inks button{width:38px;height:38px;border-radius:50%;border:2px solid transparent;
 cursor:pointer;padding:0;box-shadow:inset 0 0 0 1px rgba(20,22,28,.1);transition:transform .18s}
.sg-inks button:hover{transform:scale(1.1)}
.sg-inks button[aria-pressed=true]{border-color:var(--sg-ink);transform:scale(1.1)}
.sg-inks .sg-eraser{background:#fff;display:flex;align-items:center;justify-content:center;
 font:700 10px var(--sg-mf);color:var(--sg-ink2);box-shadow:inset 0 0 0 2px rgba(20,22,28,.16)}
.sg-papers{display:flex;gap:9px;flex-wrap:wrap;margin-top:10px}
.sg-papers button{cursor:pointer;background:transparent;border:1px solid var(--sg-line);
 border-radius:999px;padding:8px 16px;font:600 13px var(--sg-bf);color:var(--sg-ink2);
 transition:border-color .2s,color .2s}
.sg-papers button[aria-pressed=true]{border-color:var(--sg-ink);color:var(--sg-ink)}
.sg-clear{justify-self:start;background:transparent;border:1px solid var(--sg-line);
 border-radius:999px;padding:10px 20px;cursor:pointer;font:700 13px var(--sg-df);
 color:var(--sg-ink);transition:border-color .2s,background .2s}
.sg-clear:hover{border-color:var(--sg-ink)}
.sg-tools p{margin:0;font-size:13.5px;color:var(--sg-ink2);max-width:38ch}
.sg-paint{position:relative;background:#fff;border:1px solid var(--sg-line);
 padding:clamp(14px,2.4vw,32px);touch-action:none}
.sg-paint__in{position:relative}
.sg-paint canvas{position:absolute;inset:0;width:100%;height:100%;cursor:crosshair;
 touch-action:none;border-radius:2px}
.sg-paint img{position:relative;width:100%;pointer-events:none}
.sg-paint__note{position:absolute;left:50%;bottom:12px;transform:translateX(-50%);
 font:600 12px var(--sg-bf);color:var(--sg-ink2);background:rgba(255,255,255,.86);
 padding:5px 12px;border-radius:999px;pointer-events:none;transition:opacity .3s}
.sg-paint.is-used .sg-paint__note{opacity:0}

/* ── ПОДАРКИ ── */
.sg-gift{background:#f6f7f8;padding:clamp(58px,7.5vw,104px) 0}
.sg-gift h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:18ch}
.sg-gift__grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(20px,3vw,40px);
 align-items:end;margin-top:clamp(28px,3.6vw,44px)}
.sg-gift p{margin:18px 0 0;font-size:clamp(15.5px,1.3vw,17.5px);color:#33374a;max-width:58ch}
.sg-gift figure{margin:0}
/* оба мокапа вертикальные и разной пропорции: равняем их по высоте, а не по
   ширине колонки, иначе открытка встанет заметно крупнее коробки с маркерами.
   Каждый кадр центрируем в своей колонке — при разной ширине прижатые к краям
   мокапы оставляли бы посередине дыру шире самой картинки */
.sg-gift__grid img{max-height:min(58vh,500px);width:auto;margin:0 auto}
.sg-gift__grid figcaption{text-align:center}
.sg-gift figcaption{margin-top:12px;font-family:var(--sg-mf);font-size:11.5px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--sg-ink2)}

/* ── РЕЗУЛЬТАТ ── */
.sg-res{padding:clamp(58px,7.5vw,104px) 0}
.sg-res__grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(28px,5vw,66px);align-items:start}
.sg-res h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px}
.sg-res__more{margin:20px 0 0;font-size:16px;color:#33374a;max-width:44ch}
.sg-res__more a{font-weight:700;color:var(--sg-blue);text-decoration:underline;
 text-underline-offset:3px}
.sg-res__list{list-style:none;margin:0;padding:0;display:grid;gap:clamp(14px,2vw,22px)}
.sg-res__list li{display:grid;grid-template-columns:auto 1fr;gap:clamp(14px,2vw,22px);
 align-items:start;border-top:1px solid var(--sg-line);padding-top:clamp(14px,2vw,20px)}
.sg-num{font-family:var(--sg-df);font-weight:800;font-variant-numeric:tabular-nums;
 font-size:clamp(28px,3.6vw,44px);line-height:1;letter-spacing:-.04em;min-width:2.2ch;color:var(--sg-mint)}
.sg-res__list li:nth-child(2) .sg-num{color:var(--sg-blue)}
.sg-res__list li:nth-child(3) .sg-num{color:var(--sg-red)}
.sg-res__list li:nth-child(4) .sg-num{color:var(--sg-orange)}
.sg-res__list span:last-child{font-size:15.5px;color:#33374a}
.sg-res__list b{color:var(--sg-ink)}

/* лайтбокс */
.sg-lb{position:fixed;inset:0;z-index:1200;background:rgba(246,247,248,.97);display:none;
 align-items:center;justify-content:center;padding:clamp(16px,4vw,52px)}
.sg-lb.is-open{display:flex}
.sg-lb__box{position:relative;width:min(1200px,100%);display:flex;flex-direction:column;
 align-items:center}
.sg-lb img{width:auto;max-width:100%;max-height:78vh}
.sg-lb__cap{margin-top:14px;color:var(--sg-ink2);font-size:14px;text-align:center}
.sg-lb__cap b{font-family:var(--sg-df);font-weight:800;color:var(--sg-ink);font-size:16px;
 display:block}
.sg-lb__x,.sg-lb__nav{position:absolute;border:0;cursor:pointer;background:#fff;
 box-shadow:0 6px 20px -8px rgba(20,22,28,.4);color:var(--sg-ink);width:46px;height:46px;
 border-radius:50%;display:flex;align-items:center;justify-content:center;transition:transform .2s}
.sg-lb__x:hover,.sg-lb__nav:hover{transform:scale(1.08)}
.sg-lb__x{top:-56px;right:0;font-size:24px;line-height:1}
.sg-lb__nav{top:calc(39vh - 23px)}
.sg-lb__nav svg{width:20px;height:20px}
.sg-lb__nav--p{left:-56px}
.sg-lb__nav--n{right:-56px;transform:scaleX(-1)}
.sg-lb__nav--n:hover{transform:scaleX(-1) scale(1.08)}

/* появление */
html.no-js .sg-r{opacity:1!important;transform:none!important}
.sg-r{opacity:0;transform:translateY(22px);
 transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.sg-r.is-in{opacity:1;transform:none}

/* ── АДАПТИВ ── */
@media(max-width:1020px){
 .sg-hero__grid,.sg-task__grid,.sg-res__grid,.sg-sheet,.sg-sheet:nth-of-type(even),
 .sg-build__box,.sg-color__grid,.sg-gift__grid{grid-template-columns:1fr;gap:28px}
 .sg-sheet:nth-of-type(even) .sg-sheet__t{order:0}
 .sg-spec__in{grid-template-columns:repeat(2,1fr)}
 .sg-cards{grid-template-columns:1fr}
 .sg-card{display:grid;grid-template-columns:.8fr 1.2fr;align-items:center}
 .sg-card>img{height:100%}
 .sg-build__pic img{max-height:62vh}
 .sg-lb__nav--p{left:0}.sg-lb__nav--n{right:0}
 .sg-lb__nav{top:auto;bottom:-56px}
}
@media(max-width:680px){
 .sg{font-size:16px}
 .sg-card{grid-template-columns:1fr}
 .sg-card>img{aspect-ratio:4/3}
 .sg-inks button{width:34px;height:34px}
}
@media(max-width:420px){
 .sg-spec__in{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){
 .sg-r{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .sg *{transition-duration:.01ms!important;scroll-behavior:auto}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Концепция новогоднего календаря Saint-Gobain: иллюстрации из инструментов | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: концепция новогоднего календаря Saint-Gobain на 2021 год. Иллюстрации собраны из настоящих инструментов и материалов: потолочный профиль Gyproc становится небоскрёбом, плита ISOVER пляжем, сверло рогом нарвала. Три варианта конструкции, обложка-раскраска и подарочный набор маркеров.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Концепция новогоднего календаря Saint-Gobain | кейс Hand Marketing">
<meta property="og:description" content="Продукт становится сюжетом: профиль Gyproc это небоскрёб, плита ISOVER это пляж у айсберга. Три конструкции, обложка-раскраска и маркеры в подарок.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/mock-isover.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def hero():
    chips = ''.join(f'<li>{c}</li>' for c in (
        'Идея', 'Иллюстрации', 'Календарная сетка', 'Три конструкции',
        'Обложка-раскраска', 'Подарки'))
    spec = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in (
        ('2021', 'год календаря'),
        ('12', 'месяцев, 12 продуктов'),
        ('3', 'варианта конструкции'),
        ('2', 'подарка в комплекте'),
    ))
    return (
      '<header class="sg-hero"><div class="sg-w">'
      '<div class="sg-hero__grid">'
      '<div class="sg-r">'
      f'<div class="sg-hero__client"><img src="{IMG}/logo-sg.png" alt="Saint-Gobain" '
      'width="361" height="151"><span>Концепция<br>новогоднего календаря</span></div>'
      '<h1>Календарь, который хочется раскрасить</h1>'
      '<p class="sg-hero__sub">Saint-Gobain делает материалы, с которыми люди работают руками. '
      'Мы предложили показать эти материалы так, как их видит мастер: потолочный профиль '
      'становится небоскрёбом, плита утеплителя пляжем, сверло рогом нарвала.</p>'
      f'<ul class="sg-chips">{chips}</ul>'
      '<div class="sg-hero__cta">'
      f'<a class="sg-btn sg-btn--p" href="#sg-idea">Посмотреть идею {ARROW}</a>'
      '<a class="sg-btn sg-btn--gh" href="#sg-color">Раскрасить</a>'
      '</div></div>'
      '<div class="sg-r">'
      f'<div class="sg-fig" id="sg-fig">'
      f'<img src="{IMG}/pencils.jpg" alt="Коробка простых карандашей, среди которых один '
      'красный: силуэт повторяет городскую линию из знака Saint-Gobain" '
      f'width="1300" height="1582" fetchpriority="high">{SKYLINE}</div>'
      '<p class="sg-cap"><b>Знак Saint-Gobain нарисован одной линией, и это город.</b> '
      'Коробка карандашей складывается в такой же силуэт, а самый высокий в ней красный. '
      'С этого совпадения началась вся концепция.</p>'
      '<button class="sg-redraw" id="sg-redraw" type="button">Обвести ещё раз</button>'
      '</div>'
      '</div></div>'
      f'<div class="sg-spec"><div class="sg-spec__in">{spec}</div></div>'
      '</header>')


def task():
    side = ''.join(f'<li>{t}</li>' for t in (
      'Показывать не продукт, а то, что в нём можно увидеть.',
      'Собирать иллюстрации из настоящих инструментов и материалов, а не рисовать их с нуля.',
      'Дать календарю три конструкции, чтобы выбор был не только про картинку, но и про бюджет.',
      'Положить в комплект маркеры и оставить часть рисунка незакрашенной.',
    ))
    return (
      '<section class="sg-task"><div class="sg-w">'
      '<div class="sg-task__grid">'
      '<div class="sg-r"><span class="sg-kick">Задача</span>'
      '<h2>Подарок, который не выкидывают в январе</h2>'
      '<p>Привычные, часто повторяемые действия ведут к рутине: теряется интерес и к работе, '
      'и к результату. Для клиентов Saint-Gobain это ежедневная реальность, потому что '
      'монтажник годами повторяет одни и те же операции.</p>'
      '<p>Настенный календарь висит на объекте или в офисе весь год, и всё это время он '
      'либо работает на бренд, либо просто занимает стену. Сетка дат с логотипом сверху '
      'занимает стену. Нам нужен был <b>сюжет, который заставляет остановиться</b> и '
      'разглядывать картинку дольше пяти секунд.</p>'
      '</div>'
      '<div class="sg-task__side sg-r"><h3>Что предложили</h3>'
      f'<ul>{side}</ul></div></div>'
      '<p class="sg-quote sg-r">И лишь с помощью творчества раскрываются новые уровни '
      'возможностей. Работа становится удовольствием, <span>исполнитель становится '
      'мастером</span>.</p>'
      '</div></section>')


def idea():
    cards = ''
    for f, src, got, text, alt, w, h in IDEAS:
        cards += (
          '<li class="sg-card sg-r">'
          f'<img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" loading="lazy" width="{w}" height="{h}">'
          '<div class="sg-card__b">'
          f'<p class="sg-card__pair"><i>{H.escape(src)}</i><s>&rarr;</s></p>'
          f'<h3>{H.escape(got)}</h3><p>{text}</p></div></li>')
    return (
      '<section class="sg-idea" id="sg-idea"><div class="sg-w">'
      '<div class="sg-r"><span class="sg-kick">Идея</span>'
      '<h2>Инструмент, в котором уже есть картинка</h2>'
      '<p class="sg-idea__lede">За основу взята идея привычных в обращении предметов, которые '
      'могут вдохновлять. При творческом подходе и мастерском использовании они становятся '
      'частью искусства. Каждый прототип наполовину состоит из фотографии реального предмета '
      'и наполовину из рисунка от руки: карандаш, тушь, акварель. Ничего не дорисовано в '
      'графическом редакторе.</p></div>'
      f'<ul class="sg-cards">{cards}</ul></div></section>')


def calendar():
    rows = ''
    for i, (f, num, month, brand, title, text, alt, w, h) in enumerate(SHEETS):
        rows += (
          '<article class="sg-sheet sg-r">'
          '<div class="sg-sheet__t">'
          # у обложки номера месяца нет, поэтому крупная цифра просто не выводится
          f'<p class="sg-sheet__n">{f"<b>{num}</b>" if num else ""}'
          f'<span>{H.escape(month)} · {H.escape(brand)}</span></p>'
          f'<h3>{H.escape(title)}</h3><p>{text}</p></div>'
          f'<div><button class="sg-shot" type="button" data-i="{i}" data-src="{IMG}/{f}.jpg" '
          f'data-title="{H.escape(title)}" data-cap="{H.escape(month)} · {H.escape(brand)}">'
          f'<img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" loading="lazy" width="{w}" height="{h}">'
          '</button></div></article>')
    return (
      '<section class="sg-cal"><div class="sg-w">'
      '<div class="sg-r"><span class="sg-kick">Полосы</span>'
      '<h2>Продукт становится сюжетом, а не подписью под ним</h2>'
      '<p class="sg-cal__lede">Каждый месяц отдан одному продукту Saint-Gobain. Продукт '
      'не лежит на полке и не висит в воздухе: он встроен в пейзаж и работает его частью. '
      'Сетку дат при этом оставили строгой и скучной, потому что календарь остаётся '
      'рабочим инструментом.</p></div>'
      f'{rows}'
      '<p class="sg-cal__hint">Нажмите на полосу, чтобы рассмотреть её крупно.</p>'
      '</div></section>')


def build():
    tabs = ''.join(
      f'<button type="button" role="tab" id="tab-{k}" aria-controls="pane-{k}" '
      f'aria-selected="{"true" if i == 0 else "false"}">{H.escape(cap)}</button>'
      for i, (k, f, cap, t, d, specs, h) in enumerate(BUILDS))
    panes = ''
    for i, (k, f, cap, title, text, specs, h) in enumerate(BUILDS):
        dl = ''.join(f'<div><dt>{H.escape(a)}</dt><dd>{H.escape(b)}</dd></div>' for a, b in specs)
        panes += (
          f'<div class="sg-build__pane" id="pane-{k}" role="tabpanel" aria-labelledby="tab-{k}"'
          f'{"" if i == 0 else " hidden"}>'
          f'<div class="sg-build__t"><h3>{H.escape(title)}</h3><p>{text}</p><dl>{dl}</dl></div>'
          f'<div class="sg-build__pic"><img src="{IMG}/{f}.jpg" '
          f'alt="Календарь Saint-Gobain в конструкции «{H.escape(cap)}»: имидж с пляжем ISOVER '
          f'и блоки дат" loading="lazy" width="780" height="{h}"></div>'
          '</div>')
    return (
      '<section class="sg-build" id="sg-build"><div class="sg-w">'
      '<div class="sg-r"><span class="sg-kick">Конструкция</span>'
      '<h2>Одна идея, три бюджета</h2>'
      '<p class="sg-build__lede">Одна и та же иллюстрация собирается в три разных календаря. '
      'Отличается количество пружин и блоков, а вместе с ними площадь имиджа, читаемость дат '
      'с расстояния и цена сборки. Клиенту это даёт выбор внутри уже утверждённой идеи, '
      'а не выбор между разными идеями.</p></div>'
      f'<div class="sg-tabs sg-r" id="sg-tabs" role="tablist" '
      f'aria-label="Варианты конструкции календаря">{tabs}</div>'
      f'<div class="sg-build__box sg-r" id="sg-panes">{panes}</div>'
      '</div></section>')


def color():
    inks = ''.join(
      f'<button type="button" data-ink="{hexv}" style="background:{hexv}" '
      f'aria-pressed="{"true" if i == 4 else "false"}" aria-label="{H.escape(name)}"></button>'
      for i, (hexv, name) in enumerate(INKS))
    papers = ''.join(
      f'<button type="button" data-paper="{f}" data-w="{w}" data-h="{h}" '
      f'data-alt="{H.escape(alt)}" aria-pressed="{"true" if i == 0 else "false"}">'
      f'{H.escape(cap)}</button>' for i, (f, cap, w, h, alt) in enumerate(PAPERS))
    f0, cap0, w0, h0, alt0 = PAPERS[0]
    return (
      '<section class="sg-color" id="sg-color"><div class="sg-w">'
      '<div class="sg-r"><span class="sg-kick">Раскраска</span>'
      '<h2>Раскраска это тоже творчество</h2>'
      '<p class="sg-color__lede">Обложка календаря и открытка приходят клиенту чёрно-белыми, '
      'а в коробке рядом лежат маркеры. Ниже настоящий рисунок из концепции: возьмите цвет '
      'и проведите по нему курсором или пальцем.</p></div>'
      '<div class="sg-color__grid">'
      '<div class="sg-tools sg-r">'
      f'<div><h3>Цвет</h3><div class="sg-inks" id="sg-inks">{inks}'
      '<button type="button" class="sg-eraser" data-ink="erase" aria-pressed="false" '
      'aria-label="Ластик">ласт</button></div></div>'
      f'<div><h3>Лист</h3><div class="sg-papers" id="sg-papers">{papers}</div></div>'
      '<button class="sg-clear" id="sg-clear" type="button">Стереть всё</button>'
      '<p>Цвета взяты из знака Saint-Gobain: от мятного левого края до оранжевого правого. '
      'Седьмой, жёлтый, добавлен ради утеплителя ISOVER.</p>'
      '</div>'
      '<div class="sg-paint sg-r" id="sg-paint">'
      '<div class="sg-paint__in">'
      '<canvas id="sg-cv" aria-label="Поле для раскрашивания"></canvas>'
      f'<img id="sg-paper" src="{IMG}/{f0}.png" alt="{H.escape(alt0)}" loading="lazy" '
      f'width="{w0}" height="{h0}">'
      '</div>'
      '<span class="sg-paint__note">Проведите по рисунку</span>'
      '</div></div></div></section>')


def gifts():
    return (
      '<section class="sg-gift"><div class="sg-w">'
      '<div class="sg-r"><span class="sg-kick">Подарки</span>'
      '<h2>Маркеры в коробке с логотипом</h2>'
      '<p>Комплект к календарю: набор маркеров Copic Sketch в прозрачном боксе с фирменной '
      'наклейкой Saint-Gobain и открытка с ручным леттерингом. На открытке та же графика, '
      'что и на обложке календаря, и она тоже приходит незакрашенной. Получатель сам решает, '
      'каким будет цвет его декабря.</p></div>'
      '<div class="sg-gift__grid">'
      f'<figure class="sg-r"><img src="{IMG}/markers.jpg" alt="Набор маркеров Copic Sketch '
      'в прозрачном боксе с наклейкой Saint-Gobain" '
      'loading="lazy" width="897" height="1053">'
      '<figcaption>Набор маркеров Copic Sketch</figcaption></figure>'
      f'<figure class="sg-r"><img src="{IMG}/card.jpg" alt="Новогодняя открытка Saint-Gobain '
      'с рукописным леттерингом и рисунком-раскраской из подарочных коробок" '
      'loading="lazy" width="745" height="1059">'
      '<figcaption>Открытка с леттерингом</figcaption></figure>'
      '</div></div></section>')


def result():
    items = [
      ('3', '<b>Три иллюстрации-прототипа</b>, собранные из настоящих инструментов: молоток '
       'с карандашом, отвёртка с рулеткой и складным метром, сверло по бетону.'),
      ('12', '<b>Двенадцать месяцев</b>, у каждого свой продукт Saint-Gobain и короткая '
       'справка для того, кто с этим продуктом работает.'),
      ('3', '<b>Три варианта конструкции</b> под разный бюджет: одна, две и четыре пружины, '
       'от максимального имиджа до максимально читаемых дат.'),
      ('2', '<b>Два подарка в комплекте</b>: набор маркеров Copic и открытка-раскраска, '
       'плюс обложка календаря, которую тоже отдают чёрно-белой.'),
    ]
    lis = ''.join(f'<li><span class="sg-num">{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="sg-res"><div class="sg-w sg-res__grid">'
      '<div class="sg-r"><span class="sg-kick">Результат</span>'
      '<h2>Что вошло в концепцию</h2>'
      '<p class="sg-res__more">Концепция разработана в 2020 году для календаря на 2021. '
      'Больше о направлении: <a href="/creativedesign">услуга «Creative&nbsp;&amp;&nbsp;Design»</a>. '
      'Ещё один проект для этого клиента: '
      '<a href="/creative/saintgobain/suitcase">презентационный чемодан Saint-Gobain</a>.</p></div>'
      f'<ul class="sg-res__list sg-r">{lis}</ul>'
      '</div></section>')


LIGHTBOX = ('<div class="sg-lb" id="sg-lb" aria-hidden="true">'
            '<div class="sg-lb__box">'
            '<button class="sg-lb__x" id="sg-lb-x" type="button" aria-label="Закрыть">&times;</button>'
            f'<button class="sg-lb__nav sg-lb__nav--p" id="sg-lb-p" type="button" aria-label="Предыдущая полоса">{CHEV}</button>'
            f'<button class="sg-lb__nav sg-lb__nav--n" id="sg-lb-n" type="button" aria-label="Следующая полоса">{CHEV}</button>'
            # без src="": пустой атрибут браузер трактует как ссылку на саму
            # страницу и шлёт лишний запрос. Картинку подставляет JS при открытии
            '<img id="sg-lb-img" alt="">'
            '<div class="sg-lb__cap"><b id="sg-lb-t"></b><span id="sg-lb-c"></span></div>'
            '</div></div>')

PAGE_JS = """<script>(function(){
 // ── линия-город: рисуется при появлении фото и по кнопке
 var sky=document.querySelector('.sg-sky path'),fig=document.getElementById('sg-fig'),
     redraw=document.getElementById('sg-redraw'),LEN=0;
 if(sky&&sky.getTotalLength){
  LEN=sky.getTotalLength();
  sky.style.strokeDasharray=LEN;sky.style.strokeDashoffset=LEN;
  var draw=function(){sky.style.strokeDashoffset=0;};
  var reset=function(){sky.style.transition='none';sky.style.strokeDashoffset=LEN;
   sky.getBoundingClientRect();sky.style.transition='';setTimeout(draw,40);};
  if('IntersectionObserver' in window){
   var io1=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){draw();io1.disconnect();}});},{rootMargin:'0px 0px -12% 0px'});
   io1.observe(fig);
  }else{draw();}
  if(redraw)redraw.addEventListener('click',reset);
 }else if(redraw){redraw.style.display='none';}
 // ── конструкции: вкладки
 var tabs=document.getElementById('sg-tabs');
 if(tabs){
  var tb=[].slice.call(tabs.querySelectorAll('button'));
  tb.forEach(function(b){b.addEventListener('click',function(){
   tb.forEach(function(o){
    var on=o===b;o.setAttribute('aria-selected',String(on));
    var p=document.getElementById(o.getAttribute('aria-controls'));
    if(p)p.hidden=!on;});});});
  tabs.addEventListener('keydown',function(e){
   var i=tb.indexOf(document.activeElement);if(i<0)return;
   var n=e.key==='ArrowRight'?i+1:e.key==='ArrowLeft'?i-1:-1;
   if(n<0)return;e.preventDefault();n=(n+tb.length)%tb.length;tb[n].focus();tb[n].click();});
 }
 // ── раскраска: canvas под линейной графикой
 var box=document.getElementById('sg-paint'),cv=document.getElementById('sg-cv'),
     paper=document.getElementById('sg-paper');
 if(box&&cv&&cv.getContext){
  var ctx=cv.getContext('2d'),ink='#EE0F3F',erase=false,down=false,px=0,py=0;
  function fit(){
   var r=paper.getBoundingClientRect();if(!r.width)return;
   var dpr=Math.min(2,window.devicePixelRatio||1),
       w=Math.round(r.width*dpr),h=Math.round(r.height*dpr);
   if(cv.width===w&&cv.height===h)return;
   var old=null;
   if(cv.width&&cv.height){old=document.createElement('canvas');
    old.width=cv.width;old.height=cv.height;old.getContext('2d').drawImage(cv,0,0);}
   cv.width=w;cv.height=h;ctx=cv.getContext('2d');
   if(old)ctx.drawImage(old,0,0,w,h);
   ctx.lineCap='round';ctx.lineJoin='round';
  }
  function pos(e){var r=cv.getBoundingClientRect();
   return [(e.clientX-r.left)/r.width*cv.width,(e.clientY-r.top)/r.height*cv.height];}
  function stroke(x,y){
   ctx.globalCompositeOperation=erase?'destination-out':'source-over';
   ctx.strokeStyle=ink;ctx.lineWidth=cv.width*0.055;
   ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(x,y);ctx.stroke();px=x;py=y;
  }
  cv.addEventListener('pointerdown',function(e){
   fit();down=true;box.classList.add('is-used');
   if(cv.setPointerCapture)try{cv.setPointerCapture(e.pointerId);}catch(err){}
   var p=pos(e);px=p[0];py=p[1];stroke(p[0]+0.01,p[1]+0.01);e.preventDefault();});
  cv.addEventListener('pointermove',function(e){
   if(!down)return;var p=pos(e);stroke(p[0],p[1]);e.preventDefault();});
  ['pointerup','pointercancel','pointerleave'].forEach(function(t){
   cv.addEventListener(t,function(){down=false;});});
  var inks=document.getElementById('sg-inks');
  if(inks){var ib=[].slice.call(inks.querySelectorAll('button'));
   ib.forEach(function(b){b.addEventListener('click',function(){
    var v=b.getAttribute('data-ink');erase=(v==='erase');if(!erase)ink=v;
    ib.forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});});});}
  var clear=document.getElementById('sg-clear');
  if(clear)clear.addEventListener('click',function(){
   ctx.clearRect(0,0,cv.width,cv.height);box.classList.remove('is-used');});
  var pb=document.getElementById('sg-papers');
  if(pb){var pbs=[].slice.call(pb.querySelectorAll('button'));
   pbs.forEach(function(b){b.addEventListener('click',function(){
    paper.width=b.getAttribute('data-w');paper.height=b.getAttribute('data-h');
    paper.alt=b.getAttribute('data-alt');
    paper.src='/images/sgcalendar/'+b.getAttribute('data-paper')+'.png';
    ctx.clearRect(0,0,cv.width,cv.height);box.classList.remove('is-used');
    pbs.forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});});});}
  if(paper.complete)fit();
  paper.addEventListener('load',fit);
  addEventListener('resize',fit);
 }
 // ── лайтбокс полос календаря
 var shots=[].slice.call(document.querySelectorAll('.sg-shot')),
     lb=document.getElementById('sg-lb'),img=document.getElementById('sg-lb-img'),
     ttl=document.getElementById('sg-lb-t'),cap=document.getElementById('sg-lb-c'),
     x=document.getElementById('sg-lb-x'),p=document.getElementById('sg-lb-p'),
     n=document.getElementById('sg-lb-n'),cur=0;
 function show(i){
  if(i<0)i=shots.length-1;if(i>=shots.length)i=0;cur=i;
  var c=shots[i];
  img.src=c.getAttribute('data-src');
  img.alt=c.querySelector('img').alt;
  ttl.textContent=c.getAttribute('data-title');
  cap.textContent=c.getAttribute('data-cap');
 }
 function open(i){show(i);lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';x.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  img.removeAttribute('src');document.body.style.overflow='';}
 shots.forEach(function(c,i){c.addEventListener('click',function(){open(i);});});
 x.addEventListener('click',close);
 p.addEventListener('click',function(){show(cur-1);});
 n.addEventListener('click',function(){show(cur+1);});
 lb.addEventListener('click',function(e){if(e.target===lb)close();});
 document.addEventListener('keydown',function(e){
  if(!lb.classList.contains('is-open'))return;
  if(e.key==='Escape')close();
  if(e.key==='ArrowRight'){e.preventDefault();show(cur+1);}
  if(e.key==='ArrowLeft'){e.preventDefault();show(cur-1);}});
 // ── появление блоков
 var els=[].slice.call(document.querySelectorAll('.sg-r'));
 function inn(nd){nd.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(nd){var r=nd.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(nd);else io.observe(nd);});
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Концепция новогоднего календаря Saint-Gobain",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    # своего блока «обсудить проект» нет: фиолетовая форма из rc.footer() закрывает
    # страницу, второй CTA был бы дублем (как на CeramicaNova, OBO и We&I)
    body = (f'{rc.header()}<main class="sg">{hero()}{task()}{idea()}{calendar()}'
            f'{build()}{color()}{gifts()}{result()}</main>{LIGHTBOX}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'saintgobain', 'calendar')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page())
    print('written', os.path.join(out, 'index.html'))
