#!/usr/bin/env python3
"""Генерит mirror/isotec/index.html — кейс «Бренд-ролик „Изотек"» (Saint-Gobain).

Что было: запечённая Tilda-страница (десктоп) плюс отдельная мобильная копия
.mhome, в которую попали ДВА видео, причём одно чужое (silkway-3d.mp4). Две
разные вёрстки расходились по содержанию. Здесь одна адаптивная страница на
оба размера и ровно один файл ролика.

Дизайн-концепция: сам фильм — это хронология бренда. Слайды в кадре идут от
2012 к 2024, каждый год — запуск нового направления изоляции. Поэтому страница
не пересказывает ролик текстом, а даёт его навигацией:

  • шкала 2012→2024 покрашена как термошкала (холодный синий → тёплый),
    девять вех — это девять слайдов фильма, тексты и списки продуктов сняты
    с кадров дословно;
  • клик по вехе, главе или площадке перематывает плеер на нужную секунду и
    запускает воспроизведение — страница управляет фильмом, а не дублирует;
  • картинки — кадры самого ролика (scripts/isotec-assets.py), своей съёмки по
    проекту нет, и выдумывать «мокапы» незачем;
  • деления линейки, по которой едут слайды в фильме, повторены декоративной
    лентой в шапке секций.

Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import os
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

URL = 'https://hand-marketing.ru/isotec/'
IMG = '/images/isotec'
VIDEO = '/portfolio/isotec/brand-video.mp4'
DUR = 273  # 4:33


# ─── главы фильма ───────────────────────────────────────────────────────────
# секунда, короткое имя, подпись
CHAPTERS = [
    (0,   'Пролог',     'Завод и продукт'),
    (18,  'Хронология', '2012 → 2024'),
    (117, 'География',  'Площадки и города'),
    (155, 'Производство', 'Съёмка в цехах'),
    (196, 'Сервисы',    'Цифровые инструменты'),
    (256, 'Итоги',      'Цифры с 2013 года'),
]

# ─── девять вех хронологии (тексты дословно с кадров ролика) ────────────────
# год, секунда, заголовок, продукты
TIMELINE = [
    ('2012', 20,
     'Образование в «Сен-Гобен» отдельного направления технической изоляции '
     'ISOTEC в кластере «Россия и страны СНГ»', []),
    ('2012-2013', 34,
     'Старт продаж технической изоляции на основе базальта',
     ['ISOTEC Wired mat', 'ISOTEC Tank Slab', 'ISOTEC Industrial Slab',
      'ISOTEC Fire Protect', 'ISOTEC Section', 'ISOTEC Shell']),
    ('2014', 49,
     'Старт продаж технической изоляции на основе кварца',
     ['ISOTEC M-15, M-25', 'ISOTEC Mat-T, Mat Light, Mat Flex',
      'ISOTEC TRAIN Slab', 'ISOTEC ПТ-15, ПТ-20']),
    ('2014-2015', 60,
     'Улучшенные технические условия и запуск сервиса проведения энергоаудитов', []),
    ('2018-2019', 71,
     'Разработка и запуск линейки негорючих фольгированных цилиндров', []),
    ('2019-2021', 85,
     'Запуск направления технической изоляции на основе вспененного каучука '
     'ISOTEC FLEX', []),
    ('2022', 94,
     'Запуск направления конструктивной огнезащиты', []),
    ('2023', 101,
     'Запуск направления судовой изоляции ISOTEC SR PROTECT',
     ['ISOTEC SR Protect Wired mat', 'ISOTEC SR Protect Section-M',
      'ISOTEC SR Protect Section-C', 'ISOTEC SR Protect Slab',
      'ISOTEC SR Protect Mat Lamella', 'ISOTEC SR Protect Mat 25']),
    ('2024', 115,
     'Старт продаж технической изоляции для криогеники ISOTEC Cryo', []),
]

# ─── шесть площадок, которые фильм показывает на карте ──────────────────────
GEO = [
    ('Егорьевск', 123, 'Производственная площадка'),
    ('Тамбов', 127, 'Производственная площадка'),
    ('Челябинск', 131, 'Производственная площадка'),
    ('Владимир', 135, 'Сырьевая площадка'),
    ('Арзамас', 139, 'Производственная площадка'),
    ('Гомзово', 143, 'Производственная площадка'),
]

CITIES = ['Санкт-Петербург', 'Москва', 'Владимир', 'Егорьевск', 'Воронеж',
          'Арзамас', 'Липецк', 'Гомзово', 'Нижний Новгород', 'Тамбов',
          'Краснодар', 'Самара', 'Пермь', 'Волгоград', 'Уфа', 'Казань',
          'Екатеринбург', 'Челябинск', 'Новосибирск', 'Красноярск',
          'Иркутск', 'Чита', 'Хабаровск', 'Владивосток']

# ─── производственные планы ─────────────────────────────────────────────────
PROD = [
    ('prod-1', 'Изолированные воздуховоды на действующем объекте'),
    ('prod-2', 'Цех: съёмка с соблюдением регламентов площадки'),
    ('prod-3', 'Резервуарный парк: масштаб применения'),
    ('prod-4', 'Монтаж изоляции на трубопроводе'),
    ('prod-5', 'Производственная линия в работе'),
]

# ─── цифровые сервисы в кадре ───────────────────────────────────────────────
SERVICES = [
    ('svc-1', 'Энергоаудит', 'Аудит технологического оборудования и трубопроводов'),
    ('svc-2', 'Калькулятор расчёта', 'Подбор технической изоляции ISOTEC'),
    ('svc-3', 'BIM и альбомы', 'Информационное моделирование и технические решения'),
    ('svc-4', 'Калькулятор сметы', 'Смета по объекту в несколько шагов'),
]

RESULTS = [
    ('7 000', 'проектов'),
    ('100 000', 'тонн'),
    ('2 000 000', 'м³'),
]


def mmss(sec):
    return f'{sec // 60}:{sec % 60:02d}'


# ─── CSS ────────────────────────────────────────────────────────────────────
PAGE_CSS = """<style id="iso-css">
.iso{
 --ink:#070A11;--ink2:#0D131F;--ink3:#141C2B;
 --line:rgba(255,255,255,.10);--line2:rgba(255,255,255,.18);
 --tx:#A7B0C0;--hi:#F2F5FA;--dim:#6B7688;
 --blue:#3E7BFA;--cold:#4FB8FF;--warm:#FF7A1A;--gold:#F5C542;
 --therm:linear-gradient(90deg,#2E5BFF 0%,#4FB8FF 26%,#F5C542 66%,#FF7A1A 100%);
 --mono:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;
 --e:cubic-bezier(.16,1,.3,1);
 background:var(--ink);color:var(--tx);
 font-family:'Onest',-apple-system,BlinkMacSystemFont,Arial,sans-serif;
 font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;
 overflow-x:clip}
.iso *{box-sizing:border-box}
.iso ::selection{background:var(--warm);color:#0A0A0A}
/* height:auto обязателен: иначе атрибут height у <img> перебивает CSS aspect-ratio
   и кадр показывается в натуральную величину, обрезанный по ширине карточки */
.iso img{max-width:100%;display:block;height:auto}
.iso h1,.iso h2,.iso h3,.iso h4{font-family:'Manrope',Arial,sans-serif;color:var(--hi);
 letter-spacing:-.025em;margin:0;font-weight:800;line-height:1.06}
.iso p{margin:0 0 16px}
.iso__w{max-width:1180px;margin:0 auto;padding:0 28px}
@media(max-width:640px){.iso__w{padding:0 18px}}

/* лента делений — цитата линейки, по которой едут слайды в фильме */
.iso__ruler{height:14px;background:
 repeating-linear-gradient(90deg,var(--line2) 0 1px,transparent 1px 14px);
 -webkit-mask-image:linear-gradient(90deg,#000 0 62%,transparent 100%);
 mask-image:linear-gradient(90deg,#000 0 62%,transparent 100%)}

/* ── метка секции ── */
.iso__lab{display:flex;align-items:center;gap:14px;font-family:var(--mono);
 font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin:0 0 22px}
.iso__lab::before{content:"";width:26px;height:3px;border-radius:2px;background:var(--therm)}
.iso__lab b{color:var(--hi);font-weight:500}

/* ── ГЕРОЙ ── */
.iso__hero{position:relative;padding:96px 0 74px;isolation:isolate;overflow:hidden}
.iso__hero::before{content:"";position:absolute;inset:0;z-index:-2;
 background:#05070C url('""" + IMG + """/hero.jpg') center/cover no-repeat;
 opacity:.30;filter:grayscale(.35) contrast(1.05)}
.iso__hero::after{content:"";position:absolute;inset:0;z-index:-1;
 background:radial-gradient(115% 78% at 12% 0%,rgba(62,123,250,.26),transparent 62%),
 linear-gradient(180deg,rgba(7,10,17,.62) 0%,rgba(7,10,17,.88) 58%,var(--ink) 100%)}
.iso__kick{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;
 font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;
 color:#C6D0E2;margin:0 0 26px}
.iso__kick span{border:1px solid var(--line2);border-radius:999px;padding:5px 12px}
.iso__kick span.hot{border-color:transparent;background:var(--therm);color:#0A0A0A;font-weight:600}
.iso h1{font-size:clamp(40px,8.4vw,88px);margin:0 0 8px}
.iso h1 em{font-style:normal;background:var(--therm);-webkit-background-clip:text;
 background-clip:text;color:transparent}
.iso__sub{font-size:clamp(17px,4.2vw,21px);color:#C6D0E2;max-width:620px;margin:20px 0 34px}
.iso__hero-act{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.iso__btn{display:inline-flex;align-items:center;gap:11px;border:0;cursor:pointer;
 border-radius:999px;padding:15px 26px;background:var(--therm);color:#0A0A0A;white-space:nowrap;
 font:700 15px 'Manrope',Arial,sans-serif;transition:transform .2s var(--e),box-shadow .2s var(--e);
 box-shadow:0 12px 34px -14px rgba(255,122,26,.7)}
.iso__btn:hover{transform:translateY(-2px);box-shadow:0 18px 40px -14px rgba(255,122,26,.85)}
.iso__btn svg{width:15px;height:15px;fill:#0A0A0A}
.iso__ghost{display:inline-flex;align-items:center;gap:9px;border:1px solid var(--line2);
 background:transparent;color:var(--hi);border-radius:999px;padding:14px 24px;cursor:pointer;
 white-space:nowrap;font:600 15px 'Manrope',Arial,sans-serif;text-decoration:none;
 transition:.2s var(--e)}
.iso__ghost svg{width:14px;height:14px;fill:currentColor}
.iso__ghost:hover{border-color:var(--warm);color:#fff}
.iso__facts{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);
 border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:48px 0 0;max-width:760px}
@media(min-width:760px){.iso__facts{grid-template-columns:repeat(4,1fr)}}
.iso__facts div{background:rgba(10,14,22,.72);padding:16px 18px;backdrop-filter:blur(6px)}
.iso__facts dt{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--dim);margin:0 0 7px}
.iso__facts dd{margin:0;color:var(--hi);font-weight:600;font-size:15px;font-family:'Manrope',Arial,sans-serif}

/* ── секции ── */
.iso__s{padding:78px 0;border-top:1px solid var(--line)}
@media(max-width:640px){.iso__s{padding:52px 0}}
.iso__h2{font-size:clamp(27px,6.2vw,46px);margin:0 0 18px;max-width:15ch}
.iso__intro{max-width:640px;color:var(--tx);margin:0 0 34px}

/* ── ПЛЕЕР ── */
.iso__film{position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--line2);
 background:#000;box-shadow:0 44px 90px -46px rgba(0,0,0,.95)}
.iso__film video{width:100%;height:auto;aspect-ratio:16/9;display:block;background:#000}
.iso__chaps{display:flex;gap:9px;overflow-x:auto;padding:18px 0 4px;scrollbar-width:thin;
 -webkit-overflow-scrolling:touch}
@media(min-width:900px){.iso__chaps{flex-wrap:wrap;overflow:visible}}
.iso__chaps::-webkit-scrollbar{height:3px}
.iso__chaps::-webkit-scrollbar-thumb{background:var(--line2);border-radius:3px}
.iso__chap{flex:0 0 auto;display:flex;flex-direction:column;align-items:flex-start;gap:2px;
 border:1px solid var(--line);background:var(--ink2);border-radius:11px;padding:10px 15px;
 cursor:pointer;text-align:left;transition:.22s var(--e);color:var(--tx);font-family:inherit}
.iso__chap b{color:var(--hi);font:600 14px 'Manrope',Arial,sans-serif}
.iso__chap i{font-style:normal;font-family:var(--mono);font-size:11px;color:var(--dim)}
.iso__chap:hover{border-color:var(--line2);background:var(--ink3)}
.iso__chap[aria-current="true"]{border-color:transparent;
 background:linear-gradient(var(--ink3),var(--ink3)) padding-box,var(--therm) border-box;
 border:1px solid transparent}
.iso__chap[aria-current="true"] i{color:var(--gold)}

/* ── ХРОНОЛОГИЯ ── */
.iso__rail{position:relative;margin:6px 0 0;padding:0 0 8px}
.iso__rail-line{position:absolute;left:0;right:0;top:13px;height:3px;border-radius:2px;
 background:var(--therm);opacity:.55}
.iso__years{position:relative;display:flex;gap:0;overflow-x:auto;scroll-snap-type:x proximity;
 padding:0 0 6px;scrollbar-width:none}
.iso__years::-webkit-scrollbar{display:none}
.iso__y{flex:1 0 auto;min-width:104px;scroll-snap-align:center;background:none;border:0;
 cursor:pointer;padding:0 6px;display:flex;flex-direction:column;align-items:center;gap:11px;
 font-family:var(--mono);font-size:13px;color:var(--dim);transition:color .22s var(--e)}
.iso__y::before{content:"";width:15px;height:15px;border-radius:50%;background:var(--ink);
 border:2px solid var(--line2);transition:.28s var(--e)}
.iso__y:hover{color:var(--hi)}
.iso__y:hover::before{border-color:var(--cold);transform:scale(1.15)}
.iso__y[aria-selected="true"]{color:var(--hi);font-weight:700}
.iso__y[aria-selected="true"]::before{background:var(--warm);border-color:var(--warm);
 box-shadow:0 0 0 6px rgba(255,122,26,.16);transform:scale(1.15)}
.iso__panel{display:grid;gap:26px;margin-top:34px;border:1px solid var(--line);
 border-radius:16px;background:var(--ink2);padding:26px;align-items:start}
/* колонка кадра задана явно: с auto процентная ширина картинки схлопывается в ноль */
@media(min-width:840px){.iso__panel{grid-template-columns:minmax(0,420px) 1fr;gap:38px;padding:32px}}
.iso__shot{border-radius:12px;overflow:hidden;border:1px solid var(--line);background:#000;
 width:100%;max-width:420px}
.iso__shot img{width:100%;aspect-ratio:45/32;object-fit:cover}
.iso__panel h3{font-size:clamp(21px,4.6vw,30px);margin:0 0 14px;max-width:22ch}
.iso__yearbig{font-family:'Manrope',Arial,sans-serif;font-weight:800;font-size:15px;
 letter-spacing:.02em;background:var(--therm);-webkit-background-clip:text;background-clip:text;
 color:transparent;margin:0 0 10px;display:block}
.iso__prod{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:0;
 border-top:1px solid var(--line)}
@media(min-width:620px){.iso__prod{grid-template-columns:1fr 1fr}}
.iso__prod[hidden]{display:none}
.iso__prod li{position:relative;padding:10px 0 10px 20px;border-bottom:1px solid var(--line);
 font-size:14.5px;color:var(--hi);font-family:var(--mono)}
.iso__prod li::before{content:"";position:absolute;left:0;top:18px;width:9px;height:3px;
 border-radius:2px;background:var(--therm)}
.iso__seek{margin-top:22px}

/* ── ГЕОГРАФИЯ ── */
.iso__geo{display:grid;gap:30px}
@media(min-width:960px){.iso__geo{grid-template-columns:1.35fr 1fr;gap:44px;align-items:start}}
.iso__map{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#050912}
.iso__map img{width:100%}
.iso__sites{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:420px){.iso__sites{grid-template-columns:1fr}}
.iso__site{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--ink2);
 cursor:pointer;padding:0;text-align:left;color:inherit;font-family:inherit;transition:.24s var(--e)}
.iso__site img{width:100%;aspect-ratio:16/9;object-fit:cover;transition:.4s var(--e)}
.iso__site span{display:block;padding:11px 13px 13px}
.iso__site b{display:block;color:var(--hi);font:700 15px 'Manrope',Arial,sans-serif}
.iso__site i{font-style:normal;font-family:var(--mono);font-size:11px;color:var(--dim)}
.iso__site:hover{border-color:var(--line2);transform:translateY(-2px)}
.iso__site:hover img{transform:scale(1.05)}
.iso__cities{display:flex;flex-wrap:wrap;gap:7px;margin-top:22px}
.iso__cities span{font-family:var(--mono);font-size:12px;color:var(--tx);
 border:1px solid var(--line);border-radius:999px;padding:5px 11px}

/* ── ЗАДАЧА / РЕШЕНИЕ / РЕЗУЛЬТАТ ── */
.iso__story{display:grid;gap:0}
.iso__step{display:grid;gap:14px;padding:30px 0;border-top:1px solid var(--line)}
@media(min-width:840px){.iso__step{grid-template-columns:180px 1fr;gap:44px}}
.iso__step:first-child{border-top:0;padding-top:0}
.iso__num{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--gold)}
.iso__step h3{font-size:clamp(20px,4.6vw,28px);margin:0 0 14px}
.iso__two{display:grid;gap:14px;margin-top:18px}
@media(min-width:640px){.iso__two{grid-template-columns:1fr 1fr;gap:18px}}
.iso__loop{border:1px solid var(--line);border-radius:12px;padding:18px;background:var(--ink2)}
.iso__loop b{display:block;color:var(--hi);font-family:'Manrope',Arial,sans-serif;margin-bottom:6px}
.iso__loop p{margin:0;font-size:15px}

/* ── КАДРЫ ПРОИЗВОДСТВА ── */
.iso__strip{display:grid;gap:14px}
@media(min-width:720px){.iso__strip{grid-template-columns:repeat(6,1fr)}
 .iso__strip figure:nth-child(1){grid-column:span 4}
 .iso__strip figure:nth-child(2){grid-column:span 2}
 .iso__strip figure:nth-child(3){grid-column:span 2}
 .iso__strip figure:nth-child(4){grid-column:span 4}
 .iso__strip figure:nth-child(5){grid-column:span 6}}
/* узкая плитка тянется до высоты соседней широкой: картинка растёт flex-ом и кропается,
   иначе под ней остаётся пустой прямоугольник карточки */
.iso__strip figure{margin:0;border:1px solid var(--line);border-radius:13px;overflow:hidden;
 background:var(--ink2);display:flex;flex-direction:column}
.iso__strip img{width:100%;aspect-ratio:16/9;object-fit:cover;flex:1 1 auto;min-height:0}
.iso__strip figcaption{padding:11px 14px;font-family:var(--mono);font-size:11.5px;
 letter-spacing:.03em;color:var(--dim)}
.iso__rules{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);
 border-radius:14px;overflow:hidden;margin-top:26px}
@media(min-width:760px){.iso__rules{grid-template-columns:repeat(3,1fr)}}
.iso__rule{background:var(--ink2);padding:24px 22px}
.iso__rule .bar{height:3px;width:42px;border-radius:2px;background:var(--therm);margin-bottom:14px}
.iso__rule h4{font-size:18px;margin:0 0 8px}
.iso__rule p{margin:0;font-size:14.5px;color:var(--dim)}

/* ── СЕРВИСЫ ── */
.iso__svc{display:grid;gap:14px}
@media(min-width:700px){.iso__svc{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1040px){.iso__svc{grid-template-columns:repeat(4,1fr)}}
.iso__card{border:1px solid var(--line);border-radius:13px;overflow:hidden;background:var(--ink2)}
.iso__card img{width:100%;aspect-ratio:16/9;object-fit:cover}
.iso__card div{padding:15px 16px 18px}
.iso__card b{display:block;color:var(--hi);font:700 16px 'Manrope',Arial,sans-serif;margin-bottom:5px}
.iso__card p{margin:0;font-size:14px;color:var(--dim)}

/* ── ИТОГ ── */
.iso__fin{position:relative;border-radius:18px;border:1px solid var(--line2);overflow:hidden;
 background:linear-gradient(140deg,#0F1626,#0A0E17 60%)}
.iso__fin::before{content:"";position:absolute;inset:0;
 background:radial-gradient(80% 120% at 100% 0%,rgba(255,122,26,.20),transparent 60%)}
.iso__fin-in{position:relative;padding:38px 30px}
.iso__fin .iso__h2{max-width:none}
@media(min-width:840px){.iso__fin-in{padding:52px 46px}}
.iso__nums{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);
 border-radius:14px;overflow:hidden;margin:0 0 34px}
@media(min-width:620px){.iso__nums{grid-template-columns:repeat(3,1fr)}}
.iso__num-c{background:rgba(8,12,20,.82);padding:24px 22px}
.iso__num-c b{display:block;font-family:'Manrope',Arial,sans-serif;font-weight:800;
 font-size:clamp(30px,6.4vw,44px);line-height:1;letter-spacing:-.03em;
 background:var(--therm);-webkit-background-clip:text;background-clip:text;color:transparent}
.iso__num-c i{font-style:normal;display:block;margin-top:8px;font-family:var(--mono);
 font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim)}
.iso__since{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--gold);margin:0 0 16px}

/* появление */
.iso .r{opacity:0;transform:translateY(22px);
 transition:opacity .8s var(--e),transform .8s var(--e)}
.iso .r.is-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
 .iso .r{opacity:1;transform:none;transition:none}
 .iso *{transition:none!important;animation:none!important}}
.iso :focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:6px}
</style>"""


# ─── секции ─────────────────────────────────────────────────────────────────
PLAY = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>')


def hero():
    facts = ''.join(
        f'<div><dt>{t}</dt><dd>{v}</dd></div>' for t, v in [
            ('Клиент', 'ISOTEC / «Изотек»'),
            ('Группа', 'Saint-Gobain'),
            ('Формат', 'Имиджевый фильм'),
            ('Хронометраж', '4:33'),
        ])
    return f'''<section class="iso__hero"><div class="iso__w">
<div class="iso__kick"><span>Saint-Gobain</span><span>Видеопродакшн</span><span class="hot">2024</span></div>
<h1>Бренд-ролик<br><em>«Изотек»</em></h1>
<p class="iso__sub">Имиджевый фильм о производителе технической изоляции ISOTEC.
Двенадцать лет бренда, от образования направления в «Сен-Гобен» до криогенной
изоляции, собраны в одну визуальную историю.</p>
<div class="iso__hero-act">
<button class="iso__btn" type="button" data-seek="0">{PLAY}Смотреть фильм</button>
<a class="iso__ghost" href="#chrono">Хронология 2012 → 2024</a></div>
<dl class="iso__facts">{facts}</dl>
</div></section>'''


def film():
    chaps = ''.join(
        f'<button class="iso__chap" type="button" data-seek="{s}" data-chap="{s}">'
        f'<b>{n}</b><i>{mmss(s)} · {c}</i></button>'
        for s, n, c in CHAPTERS)
    return f'''<section class="iso__s" id="film"><div class="iso__w">
<p class="iso__lab"><b>Фильм</b> · 4 минуты 33 секунды</p>
<div class="iso__film r"><video id="iso-video" controls preload="none" playsinline
 poster="{IMG}/poster.jpg" width="1280" height="720">
<source src="{VIDEO}" type="video/mp4">Ваш браузер не воспроизводит видео.</video></div>
<div class="iso__chaps r" role="group" aria-label="Главы фильма">{chaps}</div>
</div></section>'''


def chrono():
    years = ''.join(
        f'<button class="iso__y" type="button" role="tab" id="iso-y{i}"'
        f' aria-controls="iso-panel" aria-selected="{"true" if i == 0 else "false"}"'
        f' data-i="{i}">{y}</button>'
        for i, (y, _s, _t, _p) in enumerate(TIMELINE))
    first = TIMELINE[0]
    prods = ''
    return f'''<section class="iso__s" id="chrono"><div class="iso__w">
<p class="iso__lab"><b>Хронология</b> · девять вех из кадра</p>
<h2 class="iso__h2">Ролик рассказывает историю бренда по годам</h2>
<p class="iso__intro">Каждая веха это слайд из фильма: год, направление, продуктовая линейка.
Выберите год, и плеер перемотается ровно на этот эпизод.</p>
<div class="iso__rail r"><div class="iso__rail-line"></div>
<div class="iso__years" role="tablist" aria-label="Хронология ISOTEC">{years}</div></div>
<div class="iso__panel r" id="iso-panel" role="tabpanel" aria-labelledby="iso-y0">
<div class="iso__shot"><img id="iso-shot" src="{IMG}/tl-1.jpg" width="450" height="320"
 alt="Кадр бренд-ролика «Изотек»: {first[0]}" loading="lazy"></div>
<div><span class="iso__yearbig" id="iso-year">{first[0]}</span>
<h3 id="iso-title">{first[2]}</h3>
<ul class="iso__prod" id="iso-prod" hidden>{prods}</ul>
<button class="iso__ghost iso__seek" type="button" id="iso-ep">{PLAY}Смотреть эпизод</button>
</div></div></div></section>'''


def geo():
    sites = ''.join(
        f'<button class="iso__site" type="button" data-seek="{s}">'
        f'<img src="{IMG}/geo-{i + 1}.jpg" width="470" height="264" loading="lazy"'
        f' alt="Кадр ролика: площадка {n}">'
        f'<span><b>{n}</b><i>{d}</i></span></button>'
        for i, (n, s, d) in enumerate(GEO))
    cities = ''.join(f'<span>{c}</span>' for c in CITIES)
    return f'''<section class="iso__s"><div class="iso__w">
<p class="iso__lab"><b>География</b> · эпизод 1:57</p>
<h2 class="iso__h2">Площадки и карта присутствия</h2>
<p class="iso__intro">В этой части фильма камера идёт по стране: шесть площадок с реальными
кадрами производства и карта городов, где работает бренд. Клик по площадке открывает её эпизод
в плеере.</p>
<div class="iso__geo r">
<div><div class="iso__map"><img src="{IMG}/map.jpg" width="1240" height="600" loading="lazy"
 alt="Карта присутствия ISOTEC из бренд-ролика"></div>
<div class="iso__cities">{cities}</div></div>
<div class="iso__sites">{sites}</div>
</div></div></section>'''


def story():
    return '''<section class="iso__s"><div class="iso__w">
<p class="iso__lab"><b>Кейс</b> · задача, решение, результат</p>
<div class="iso__story r">
<div class="iso__step"><div class="iso__num">01 / Задача</div>
<div><h3>Показать живой бренд, а не поставщика материалов</h3>
<p>Клиенту нужен был фильм, который фиксирует путь становления: рост компетенций,
расширение линейки, укрепление позиций на рынке, формирование команды экспертов.
Ролик должен был работать в двух контурах одновременно.</p>
<div class="iso__two">
<div class="iso__loop"><b>Имиджевый контур</b><p>Клиенты, партнёры, отраслевые мероприятия,
сайт и презентации.</p></div>
<div class="iso__loop"><b>Корпоративный контур</b><p>Внутренние коммуникации, адаптация
новых сотрудников, идентичность бренда внутри команды.</p></div>
</div></div></div>
<div class="iso__step"><div class="iso__num">02 / Решение</div>
<div><h3>Короткая визуальная история развития</h3>
<p>Соединили архивные и актуальные материалы, производственные съёмки, командные моменты и
ключевые достижения так, чтобы за несколько минут зритель увидел, как менялись масштаб
бизнеса, технологии и подход к клиенту.</p>
<p>Сценарная конструкция построена как путь: от образования направления и первых линеек
к зрелому бренду с узнаваемым именем и собственными цифровыми сервисами. Хронология в кадре
держит ритм, производственные планы дают фактуру, карта показывает масштаб.</p></div></div>
<div class="iso__step"><div class="iso__num">03 / Результат</div>
<div><h3>Универсальный имиджевый инструмент</h3>
<p>Ролик используют на сайте компании, в отраслевых презентациях, на партнёрских встречах
и во внутренних коммуникациях. Для «Изотек» видео зафиксировало рубеж развития и стало
эмоциональной точкой опоры для команды, то есть дополнительным активом бренда в коммуникации
с рынком.</p></div></div>
</div></div></section>'''


def craft():
    figs = ''.join(
        f'<figure><img src="{IMG}/{n}.jpg" width="1100" height="619" loading="lazy" alt="{c}">'
        f'<figcaption>{c}</figcaption></figure>' for n, c in PROD)
    rules = ''.join(
        f'<div class="iso__rule"><div class="bar"></div><h4>{h}</h4><p>{p}</p></div>'
        for h, p in [
            ('Надёжность', 'Промышленная фактура, действующие площадки, инженерная точность кадра.'),
            ('Технологичность', 'Динамика производства, масштаб и современность процессов.'),
            ('Человеческое лицо', 'Команда и экспертиза: за материалом стоят люди.'),
        ])
    return f'''<section class="iso__s"><div class="iso__w">
<p class="iso__lab"><b>Съёмка</b> · эпизод 2:35</p>
<h2 class="iso__h2">Снимали на действующих производствах</h2>
<p class="iso__intro">Работа шла на действующих площадках, по регламентам СИЗ и техники
безопасности, принятым на всех заводах Saint-Gobain в России. Отдельная часть материала это
архив компании, он смонтирован встык с новой съёмкой.</p>
<div class="iso__strip r">{figs}</div>
<div class="iso__rules r">{rules}</div>
</div></section>'''


def digital():
    cards = ''.join(
        f'<div class="iso__card"><img src="{IMG}/{n}.jpg" width="900" height="506" loading="lazy"'
        f' alt="Кадр ролика: {t}"><div><b>{t}</b><p>{d}</p></div></div>'
        for n, t, d in SERVICES)
    return f'''<section class="iso__s"><div class="iso__w">
<p class="iso__lab"><b>Сервисы в кадре</b> · эпизод 3:16</p>
<h2 class="iso__h2">Бренд показан через инструменты, а не через слова</h2>
<p class="iso__intro">В финальной трети фильма показано то, чем «Изотек» отличается от поставщика
материалов: энергоаудит, расчётные калькуляторы, BIM-модели и альбомы технических решений.</p>
<div class="iso__svc r">{cards}</div>
</div></section>'''


def result():
    nums = ''.join(f'<div class="iso__num-c"><b>{v}</b><i>{c}</i></div>' for v, c in RESULTS)
    return f'''<section class="iso__s"><div class="iso__w"><div class="iso__fin r">
<div class="iso__fin-in">
<p class="iso__since">Финал ролика · с 2013 года более</p>
<div class="iso__nums">{nums}</div>
<h2 class="iso__h2">Цифры, которыми фильм заканчивается</h2>
<p class="iso__intro" style="margin-bottom:22px">Хронология, география и производство сходятся
в трёх числах. Это и есть итог двенадцати лет, ради которого снимался ролик.</p>
<button class="iso__ghost" type="button" data-seek="256">{PLAY}Посмотреть финал</button>
</div></div></div></section>'''


# ─── JS ─────────────────────────────────────────────────────────────────────
TL_JSON = '[' + ','.join(
    '{"y":"%s","s":%d,"t":"%s","p":[%s]}' % (
        y, s, t.replace('"', '\\"'),
        ','.join('"%s"' % x for x in p))
    for y, s, t, p in TIMELINE) + ']'

PAGE_JS = """<script>(function(){
 var TL=""" + TL_JSON + """;
 var v=document.getElementById('iso-video');
 // ── перемотка: любая кнопка с data-seek управляет одним плеером ──────────
 function seek(sec,scroll){
  if(!v)return;
  try{v.currentTime=sec;}catch(e){}
  var go=function(){try{v.currentTime=sec;}catch(e){}v.play().catch(function(){});};
  if(v.readyState<1){v.addEventListener('loadedmetadata',go,{once:true});v.load();}else{go();}
  if(scroll!==false){
   var r=v.getBoundingClientRect();
   if(r.top<0||r.bottom>innerHeight)v.scrollIntoView({behavior:'smooth',block:'center'});}
 }
 document.addEventListener('click',function(e){
  var b=e.target.closest?e.target.closest('[data-seek]'):null;
  if(!b)return;e.preventDefault();seek(parseFloat(b.getAttribute('data-seek')));});
 // ── подсветка активной главы ────────────────────────────────────────────
 var chaps=[].slice.call(document.querySelectorAll('[data-chap]'));
 if(v&&chaps.length){
  var last=-1;
  v.addEventListener('timeupdate',function(){
   var t=v.currentTime,cur=0;
   chaps.forEach(function(c,i){if(t>=parseFloat(c.getAttribute('data-chap')))cur=i;});
   if(cur===last)return;last=cur;
   chaps.forEach(function(c,i){c.setAttribute('aria-current',i===cur?'true':'false');});});
 }
 // ── хронология ──────────────────────────────────────────────────────────
 var ys=[].slice.call(document.querySelectorAll('.iso__y')),
     shot=document.getElementById('iso-shot'),year=document.getElementById('iso-year'),
     ttl=document.getElementById('iso-title'),prod=document.getElementById('iso-prod'),
     ep=document.getElementById('iso-ep'),cur=0;
 function show(i,focus){
  if(i<0)i=0;if(i>=TL.length)i=TL.length-1;cur=i;
  var d=TL[i];
  ys.forEach(function(b,k){b.setAttribute('aria-selected',k===i?'true':'false');
   b.tabIndex=k===i?0:-1;});
  shot.src='""" + IMG + """/tl-'+(i+1)+'.jpg';
  shot.alt='Кадр бренд-ролика «Изотек»: '+d.y;
  year.textContent=d.y;ttl.textContent=d.t;
  if(d.p.length){prod.hidden=false;
   prod.innerHTML=d.p.map(function(x){return '<li>'+x+'</li>';}).join('');}
  else{prod.hidden=true;prod.innerHTML='';}
  ep.setAttribute('data-seek',d.s);
  var b=ys[i];
  if(b&&b.parentNode.scrollWidth>b.parentNode.clientWidth)
   b.parentNode.scrollTo({left:b.offsetLeft-b.parentNode.clientWidth/2+b.offsetWidth/2,
    behavior:'smooth'});
  if(focus&&b)b.focus();
 }
 ys.forEach(function(b,i){
  b.tabIndex=i===0?0:-1;
  b.addEventListener('click',function(){show(i);});
  b.addEventListener('keydown',function(e){
   if(e.key==='ArrowRight'){e.preventDefault();show(i+1,true);}
   if(e.key==='ArrowLeft'){e.preventDefault();show(i-1,true);}
   if(e.key==='Home'){e.preventDefault();show(0,true);}
   if(e.key==='End'){e.preventDefault();show(TL.length-1,true);}
   if(e.key==='Enter'||e.key===' '){e.preventDefault();show(i);seek(TL[i].s);}});});
 if(ys.length)show(0);
 // ── появление блоков ────────────────────────────────────────────────────
 var els=[].slice.call(document.querySelectorAll('.iso .r'));
 function inn(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(n);else io.observe(n);});
})();</script>"""


VIDEO_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"VideoObject","name":"Бренд-ролик «Изотек» (ISOTEC, Saint-Gobain)",'
            '"description":"Имиджевый фильм для бренда технической изоляции ISOTEC: '
            'хронология развития 2012-2024, производственные площадки, география и цифровые '
            'сервисы компании.","thumbnailUrl":"https://hand-marketing.ru' + IMG + '/poster.jpg",'
            '"contentUrl":"https://hand-marketing.ru' + VIDEO + '","duration":"PT4M33S",'
            '"uploadDate":"2024-06-01","publisher":{"@type":"Organization",'
            '"name":"Hand Marketing","logo":{"@type":"ImageObject",'
            '"url":"https://hand-marketing.ru/images/lib/as3365-6332-4339-a263-313566616365/152.png"}}}'
            '</script>')

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
                 '"@type":"BreadcrumbList","itemListElement":['
                 '{"@type":"ListItem","position":1,"name":"Проекты",'
                 '"item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"Video Production",'
                 '"item":"https://hand-marketing.ru/videoproduction/"},'
                 '{"@type":"ListItem","position":3,"name":"Бренд-ролик «Изотек»",'
                 f'"item":"{URL}"}}]}}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Бренд-ролик «Изотек» (ISOTEC, Saint-Gobain): кейс видеопродакшна | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: имиджевый бренд-ролик компании «Изотек» (ISOTEC, группа Saint-Gobain). Хронология бренда 2012-2024 прямо в плеере, шесть производственных площадок, съёмка в действующих цехах, цифровые сервисы и итоговые цифры компании.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Бренд-ролик «Изотек» | кейс Hand Marketing">
<meta property="og:description" content="Имиджевый фильм для бренда технической изоляции ISOTEC: двенадцать лет развития компании в одной визуальной истории.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/poster.jpg">
<meta name="theme-color" content="#070A11">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def build():
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма из rc.footer()
    body = (f'{rc.header()}<main class="iso">{hero()}{film()}{chrono()}{geo()}'
            f'{story()}{craft()}{digital()}{result()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{VIDEO_LD}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'isotec')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(build())
    # старая связка «десктоп Tilda + .mhome» больше не нужна: A2-файла быть не должно,
    # иначе деплой переименует его поверх нашей страницы
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
