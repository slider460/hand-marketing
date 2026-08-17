#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/photo/saint-gobain/index.html: кейс «Предметная съёмка
продукции Gyproc» для Saint-Gobain.

Первоисточник один: сдаточная папка Saint_Gobain_foto_231124 (62 файла PNG
5760×3240 с вырезанным фоном) плюс два кадра бекстейджа и бриф заказчика.
Съёмка 23.11.2023, один съёмочный день, 63 позиции продукции. Все цифры на
странице посчитаны scripts/sg-photo-assets.py по самим файлам и лежат в
sgphoto_map.json: число сквозных отверстий, габарит силуэта, вписываемость
в квадрат. Ничего не придумано.

Идея страницы. Заказчик покупал не «красивые фото», а сдачу под три канала
сразу: печатные каталоги, сайт и POS-материалы. Из этого вырос бриф с двумя
техническими требованиями, которые обычно не видно в портфолио: любой кадр
должен кадрироваться в квадрат без потери главного, а фон у отдельных позиций
должен быть вырезан. Страница показывает не «как красиво», а как именно это
сдано, и даёт проверить руками.

Механики:

1. «Лист сдачи» (сигнатурная). Все 62 кадра лежат одним листом в родной
   пропорции 16:9. Тумблер переводит лист в 1:1, и каждый кадр на глазах
   кадрируется в тот самый квадрат: окно кадрирования встаёт в посчитанное
   положение (поле sq в карте — левый край квадрата в долях ширины кадра).
   Плашка на кадре говорит, вошёл предмет целиком или квадрат взят по узлу,
   счётчик пересчитывает выборку. Фильтр по разделам брифа сужает лист.
2. Подложка. Кадры сданы с альфа-каналом, поэтому фон под ними меняется
   кнопкой: белый лист, фирменный синий с ленты, графит, шахматка. На
   шахматке видно, что вырезан контур, а не прямоугольник, и что вместе с
   контуром вырезаны 615 сквозных отверстий перфорации.
3. Деталь и система: четыре пары «позиция отдельно» ↔ «она же в собранном
   каркасе», связка проверена по самим кадрам.
4. Смена одним листом: 299 позиций счётчика камеры от IMG_2103 до IMG_2401,
   62 из них ушли в сдачу. Видно, сколько дублей стоит за одним каталожным
   кадром.

Шрифты — Exo 2 (заголовки и интерфейс) и Spectral (текст), self-host:
/fonts/exo2-spectral.css. Exo 2 — техно-гротеск с родной кириллицей под
инженерную фактуру металла, Spectral — шрифт печатного каталога, а каталоги
и были главным адресатом съёмки. Палитра снята пипеткой с самой продукции:
синий поризованной ленты, синий этикетки Марко ПРО, лиловый акустического
подвеса, серый оцинковки.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import html as H
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

MAP = json.load(open(os.path.join(HERE, 'sgphoto_map.json'), encoding='utf-8'))
IMG = '/images/sgphoto'
URL = 'https://hand-marketing.ru/photo/saint-gobain'
TITLE = 'Предметная съёмка продукции Gyproc для Saint-Gobain | Hand Marketing'
DESCR = ('Предметная съёмка комплектующих Gyproc для Saint-Gobain: 63 позиции '
         'за один съёмочный день, 62 кадра в сдаче, вырезанный по контуру фон '
         'и кадрирование под квадрат для каталогов, сайта и POS.')

ST = MAP['stats']


def plural(n, one, few, many):
    """Русское склонение при числительном: 1 кадр, 2 кадра, 5 кадров."""
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        return one
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14:
        return few
    return many



SHOTS = [dict(s, group=g['slug'], gtitle=g['title'], section=g['section'])
         for g in MAP['groups'] for s in g['shots']]
BY_ID = {s['id']: s for s in SHOTS}
SECTIONS = []
for s in SHOTS:
    if s['section'] not in SECTIONS:
        SECTIONS.append(s['section'])

# «компактные» — всё, кроме длинномера и собранных систем: именно они идут
# в квадратные карточки, и именно по ним считается вписываемость
COMPACT = [s for s in SHOTS if s['section'] not in ('профили', 'системы')]
COMPACT_FIT = sum(1 for s in COMPACT if s['fits'])
SOLO = sum(1 for s in SHOTS if s['section'] != 'системы')
SYS = sum(1 for s in SHOTS if s['section'] == 'системы')

# ─── тексты ─────────────────────────────────────────────────────────────────
# Четыре пункта брифа — дословно из задания заказчика.
BRIEF = [
    ('Отдельно каждый продукт',
     'Фото отдельного продукта на столе',
     f'{SOLO} кадров отдельных позиций: подвесы, соединители, удлинители, '
     'ленты, крепёж, профили. На позицию от одного до шести ракурсов.'),
    ('Продукт внутри системы',
     'Фото продуктов внутри системы',
     f'{SYS} кадр собранных систем: подвесной потолок и перегородка. Каркас '
     'собирал специалист заказчика прямо на съёмочном столе, между кадрами '
     'система пересобиралась.'),
    ('Кадрируется в квадрат',
     'Любое фото можно кадрировать под квадрат, и не обрезается ничего важного',
     f'Компактные позиции, которые идут в карточки, входят в квадрат целиком: '
     f'{COMPACT_FIT} из {len(COMPACT)}. Длинномер и собранные системы в квадрат '
     'не помещаются физически, поэтому у них квадрат берётся по узлу. Ниже это '
     'переключается и видно сразу на всех кадрах.'),
    ('Фон вырезан, ретушь',
     'Общая обработка, у отдельных позиций вырезать фон, местами дополнительная ретушь',
     f'Фон вырезан по контуру у всех {ST["shots"]} кадров, не прямоугольником. '
     f'Вместе с контуром вырезано {ST["holes"]} сквозных отверстий: перфорация '
     'подвесов, прорези профиля, просветы в собранном каркасе.'),
]

# Пары «позиция отдельно» ↔ «она же в системе». Каждая связка выверена по
# самим кадрам: на системном кадре видно ровно эту деталь.
PAIRS = [
    (2105, 2401, 'Соединитель «краб»',
     'На кресте двух профилей краб держит их в одной плоскости'),
    (2121, 2400, 'Удлинитель профиля',
     'Муфта надета на стык и стягивает два профиля в одну линию'),
    (2192, 2342, 'Подвес акустический',
     'Пара подвесов с лиловой виброразвязкой стоит на несущем профиле'),
    (2134, 2332, 'Подвес анкерный с тягой',
     'Тяга уходит вверх, зажим держит несущий профиль каркаса'),
]

BACKSTAGE = [
    ('setup', 'Систему собирают в кадре',
     'Специалист Saint-Gobain собирает каркас прямо на съёмочном столе: между '
     'кадрами меняются подвесы, соединители и шаг профиля. На мониторе рядом '
     'идёт превью снятого.'),
    ('crew', 'Площадка вместо студии',
     'Снимали в учебном центре заказчика, где лежит вся продукция: камера на '
     'штативе, два прибора на стойках, верхний свет на журавле, белый лист '
     'фоном. Студия развёрнута на месте за час.'),
]

FACTS = [
    ('1', 'съёмочный день', '23 ноября 2023 года'),
    ('63', 'позиции продукции', 'подвесы, соединители, ленты, крепёж, профили'),
    (str(ST['shots']), 'кадра в сдаче', 'из 299 срабатываний затвора'),
    (str(ST['holes']), 'отверстий вырезано', 'вместе с контуром, а не прямоугольником'),
]

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px;" alt="" /></div></noscript>'
           '<!-- /Yandex.Metrika counter -->')

BREADCRUMB_LD = ('<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Главная",
         "item": "https://hand-marketing.ru/"},
        {"@type": "ListItem", "position": 2, "name": "Фотопродакшн",
         "item": "https://hand-marketing.ru/photo"},
        {"@type": "ListItem", "position": 3,
         "name": "Предметная съёмка продукции Gyproc", "item": URL},
    ]}, ensure_ascii=False) + '</script>')

CSS = """<style id="sg-css">
.sg{--ink:#16191C;--paper:#fff;--mist:#F2F4F6;--line:rgba(22,25,28,.12);
 --blue:#4CA4E8;--deep:#3B729D;--violet:#A25A92;--metal:#717572;
 --stage:#fff;--stage-ink:#16191C;
 font-family:'Spectral',Georgia,serif;color:var(--ink);background:var(--paper);
 -webkit-font-smoothing:antialiased}
.sg *{box-sizing:border-box}
.sg h1,.sg h2,.sg h3,.sg .ui{font-family:'Exo 2','Montserrat',-apple-system,Arial,sans-serif}
.sg :focus-visible{outline:3px solid var(--deep);outline-offset:3px;border-radius:3px}
.sg__wrap{max-width:1240px;margin:0 auto;padding:0 40px}
.sg__sec{padding:88px 0;border-top:1px solid var(--line)}
.sg__sec:first-child{border-top:0}
.sg__kicker{font-family:'Exo 2',sans-serif;font-size:12px;font-weight:700;letter-spacing:.16em;
 text-transform:uppercase;color:var(--deep);margin:0 0 14px}
.sg__h{font-size:clamp(26px,3.4vw,42px);font-weight:700;letter-spacing:-.02em;line-height:1.1;margin:0 0 18px}
.sg__lead{font-size:clamp(16px,1.5vw,19px);line-height:1.65;max-width:64ch;margin:0 0 8px;color:#2E3439}
.sg__note{font-size:14px;line-height:1.6;color:#6B7178}

/* ─── герой ─────────────────────────────────────────────────────────────── */
.sg-hero{padding:56px 0 72px}
.sg-hero__top{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center}
.sg-hero h1{font-size:clamp(30px,4.6vw,58px);font-weight:800;line-height:1.03;letter-spacing:-.03em;margin:0 0 20px}
.sg-hero h1 em{font-style:normal;color:var(--deep)}
.sg-hero__stage{position:relative;border-radius:18px;overflow:hidden;background:var(--stage);
 border:1px solid var(--line);transition:background .35s}
.sg-hero__stage img{display:block;width:100%;height:auto}
.sg-hero__stage_pad{display:flex;align-items:center;justify-content:center;padding:34px;min-height:340px}
.sg-hero__stage_pad img{width:auto;max-width:100%;max-height:420px}
.sg-crumbs{font-family:'Exo 2',sans-serif;font-size:13px;color:#6B7178;margin:0 0 22px}
.sg-crumbs a{color:#6B7178;text-decoration:none;border-bottom:1px solid rgba(107,113,120,.35)}
.sg-crumbs a:hover{color:var(--deep);border-color:var(--deep)}
.sg-facts{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:52px}
.sg-facts div{border-top:2px solid var(--ink);padding-top:12px}
.sg-facts b{font-family:'Exo 2',sans-serif;display:block;font-size:clamp(28px,3.6vw,44px);
 font-weight:800;line-height:1;letter-spacing:-.02em}
.sg-facts span{display:block;font-family:'Exo 2',sans-serif;font-size:13px;font-weight:600;
 margin:8px 0 4px}
.sg-facts em{font-style:normal;font-size:13px;line-height:1.45;color:#6B7178}

/* ─── переключатель подложки ────────────────────────────────────────────── */
.sg-bg{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.sg-bg__t{font-family:'Exo 2',sans-serif;font-size:12px;font-weight:700;letter-spacing:.12em;
 text-transform:uppercase;color:#6B7178;margin-right:4px}
.sg-bg button{font-family:'Exo 2',sans-serif;font-size:13px;font-weight:600;cursor:pointer;
 padding:7px 14px 7px 30px;border-radius:999px;border:1px solid var(--line);background:#fff;
 color:var(--ink);position:relative;transition:border-color .2s,color .2s}
.sg-bg button::before{content:"";position:absolute;left:9px;top:50%;transform:translateY(-50%);
 width:14px;height:14px;border-radius:4px;border:1px solid rgba(22,25,28,.2);background:var(--sw,#fff)}
.sg-bg button[aria-pressed=true]{border-color:var(--ink);color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.sg-bg button:hover{border-color:var(--deep)}
.sg-check::before{background-image:
 linear-gradient(45deg,#D6DADE 25%,transparent 25%,transparent 75%,#D6DADE 75%),
 linear-gradient(45deg,#D6DADE 25%,transparent 25%,transparent 75%,#D6DADE 75%);
 background-size:8px 8px;background-position:0 0,4px 4px;background-color:#fff}

/* ─── бриф ──────────────────────────────────────────────────────────────── */
.sg-brief{display:grid;grid-template-columns:repeat(2,1fr);gap:28px;margin-top:34px}
.sg-brief__i{border:1px solid var(--line);border-radius:16px;padding:26px 26px 24px;background:#fff}
.sg-brief__n{font-family:'Exo 2',sans-serif;font-size:12px;font-weight:700;color:var(--deep);
 letter-spacing:.12em;text-transform:uppercase}
.sg-brief__h{font-family:'Exo 2',sans-serif;font-size:20px;font-weight:700;margin:8px 0 12px}
.sg-brief__q{font-size:15px;line-height:1.6;color:#4A5157;border-left:3px solid var(--blue);
 padding-left:14px;margin:0 0 14px;font-style:italic}
.sg-brief__a{font-size:15.5px;line-height:1.65;margin:0}

/* ─── лист сдачи ────────────────────────────────────────────────────────── */
.sg-ctrl{display:flex;flex-wrap:wrap;gap:20px 28px;align-items:center;justify-content:space-between;
 margin:26px 0 22px;padding:18px 22px;border:1px solid var(--line);border-radius:14px;background:var(--mist)}
.sg-ctrl__g{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.sg-ratio{display:inline-flex;border:1px solid var(--ink);border-radius:999px;overflow:hidden}
.sg-ratio button{font-family:'Exo 2',sans-serif;font-size:13px;font-weight:700;cursor:pointer;
 padding:8px 18px;border:0;background:#fff;color:var(--ink)}
.sg-ratio button[aria-pressed=true]{background:var(--ink);color:#fff}
.sg-chip{font-family:'Exo 2',sans-serif;font-size:13px;font-weight:600;cursor:pointer;padding:7px 14px;
 border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--ink);transition:.2s}
.sg-chip[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
.sg-chip:hover{border-color:var(--deep)}
.sg-count{font-family:'Exo 2',sans-serif;font-size:14px;font-weight:600;color:#4A5157}
.sg-count b{color:var(--ink)}
.sg-sheet{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.sg-shot{position:relative;margin:0;border:1px solid var(--line);border-radius:12px;overflow:hidden;
 background:var(--stage);transition:background .35s,border-color .2s;cursor:zoom-in;padding:0}
.sg-shot:hover{border-color:var(--deep)}
.sg-shot__box{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;transition:aspect-ratio .45s}
.sg-shot__box img{position:absolute;top:0;left:0;width:100%;height:auto;display:block;
 transition:width .45s cubic-bezier(.3,.7,.3,1),left .45s cubic-bezier(.3,.7,.3,1)}
.sg-sheet[data-ratio="1"] .sg-shot__box{aspect-ratio:1/1}
.sg-sheet[data-ratio="1"] .sg-shot__box img{width:177.78%;left:calc(var(--sq) * -177.78%)}
.sg-shot__cap{display:flex;justify-content:space-between;align-items:center;gap:8px;
 padding:9px 12px 10px;border-top:1px solid var(--line);background:#fff}
.sg-shot__n{font-family:'Exo 2',sans-serif;font-size:12px;font-weight:600;color:#6B7178}
.sg-shot__f{font-family:'Exo 2',sans-serif;font-size:11px;font-weight:700;letter-spacing:.04em;
 padding:3px 8px;border-radius:999px;white-space:nowrap}
.sg-shot__f b{font-weight:700}
.sg-shot__f .sm{display:none}
.sg-shot__f_y{background:rgba(76,164,232,.16);color:#215C87}
.sg-shot__f_n{background:rgba(22,25,28,.07);color:#5A6167}
.sg-shot[hidden]{display:none}

/* ─── просмотр кадра ────────────────────────────────────────────────────── */
.sg-lb{position:fixed;inset:0;z-index:9999;background:rgba(12,14,16,.86);display:none;
 align-items:center;justify-content:center;padding:32px}
.sg-lb[open],.sg-lb.is-on{display:flex}
.sg-lb__in{max-width:1100px;width:100%}
.sg-lb__st{background:var(--stage);border-radius:14px;overflow:hidden}
.sg-lb__st img{display:block;width:100%;height:auto}
.sg-lb__m{display:flex;flex-wrap:wrap;gap:8px 22px;justify-content:space-between;align-items:center;
 margin-top:14px;color:#E7EAED;font-family:'Exo 2',sans-serif;font-size:14px}
.sg-lb__m b{color:#fff}
.sg-lb__x{position:absolute;top:18px;right:22px;width:44px;height:44px;border-radius:50%;
 border:1px solid rgba(255,255,255,.35);background:transparent;color:#fff;font-size:22px;cursor:pointer}
.sg-lb__x:hover{background:rgba(255,255,255,.12)}

/* ─── вырез ─────────────────────────────────────────────────────────────── */
.sg-cut{display:grid;grid-template-columns:1.25fr .75fr;gap:40px;align-items:start;margin-top:30px}
.sg-cut__st{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:var(--stage);
 transition:background .35s}
.sg-cut__st img{display:block;width:100%;height:auto}
.sg-card{border:1px solid var(--line);border-radius:16px;padding:18px;background:#fff}
.sg-card__sq{aspect-ratio:1/1;border-radius:10px;background:#fff;display:flex;align-items:center;
 justify-content:center;overflow:hidden;border:1px solid var(--line)}
.sg-card__sq img{max-width:86%;max-height:86%;width:auto;height:auto}
.sg-card__t{font-family:'Exo 2',sans-serif;font-weight:700;font-size:16px;margin:14px 0 4px}
.sg-card__p{font-family:'Exo 2',sans-serif;font-size:14px;color:#6B7178;margin:0 0 12px}
.sg-card__b{display:block;text-align:center;font-family:'Exo 2',sans-serif;font-size:14px;font-weight:700;
 padding:11px;border-radius:8px;background:var(--deep);color:#fff}
.sg-card__note{font-size:13px;line-height:1.55;color:#6B7178;margin:12px 0 0}

/* ─── деталь и система ──────────────────────────────────────────────────── */
.sg-pairs{display:grid;grid-template-columns:repeat(2,1fr);gap:26px;margin-top:32px}
.sg-pair{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff}
.sg-pair__g{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line)}
.sg-pair__c{position:relative;background:var(--stage);transition:background .35s}
.sg-pair__c img{display:block;width:100%;height:auto}
.sg-pair__l{position:absolute;left:10px;top:10px;font-family:'Exo 2',sans-serif;font-size:11px;
 font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:rgba(255,255,255,.9);
 color:var(--ink);padding:4px 9px;border-radius:999px}
.sg-pair__t{padding:16px 18px 18px}
.sg-pair__t h3{font-size:18px;font-weight:700;margin:0 0 6px}
.sg-pair__t p{font-size:14.5px;line-height:1.6;color:#4A5157;margin:0}

/* ─── смена ─────────────────────────────────────────────────────────────── */
.sg-day{margin-top:30px}
.sg-strip{display:flex;gap:1px;align-items:flex-end;height:76px;padding:14px 16px;border:1px solid var(--line);
 border-radius:12px;background:var(--mist);overflow:hidden}
.sg-strip i{flex:1 1 auto;min-width:1px;height:22%;background:rgba(22,25,28,.14);border-radius:1px}
.sg-strip i.on{height:100%;background:var(--deep)}
.sg-strip i.on:hover{background:var(--blue)}
.sg-legend{display:flex;flex-wrap:wrap;gap:8px 24px;margin:12px 0 0;font-family:'Exo 2',sans-serif;
 font-size:13px;color:#6B7178}
.sg-legend b{color:var(--ink);font-weight:700}
.sg-back{display:grid;grid-template-columns:repeat(2,1fr);gap:26px;margin-top:34px}
.sg-back figure{margin:0;border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff}
.sg-back img{display:block;width:100%;height:auto}
.sg-back figcaption{padding:16px 18px 18px}
.sg-back h3{font-size:18px;font-weight:700;margin:0 0 6px}
.sg-back p{font-size:14.5px;line-height:1.6;color:#4A5157;margin:0}
.sg-final{margin-top:46px;padding:30px 32px;border-radius:16px;background:var(--ink);color:#F2F4F6}
.sg-final h3{font-family:'Exo 2',sans-serif;font-size:20px;font-weight:700;margin:0 0 10px;color:#fff}
.sg-final p{font-size:15.5px;line-height:1.65;margin:0 0 8px;max-width:78ch}
.sg-final a{color:var(--blue)}

/* ─── адаптив ───────────────────────────────────────────────────────────── */
@media(max-width:1080px){
 .sg__wrap{padding:0 28px}
 .sg-hero__top{grid-template-columns:1fr;gap:30px}
 .sg-cut{grid-template-columns:1fr;gap:26px}
 .sg-sheet{grid-template-columns:repeat(3,1fr)}
 .sg-facts{grid-template-columns:repeat(2,1fr);gap:22px}
}
@media(max-width:880px){
 .sg__sec{padding:58px 0}
 .sg-brief,.sg-pairs,.sg-back{grid-template-columns:1fr}
 .sg-ctrl{padding:16px}
}
@media(max-width:640px){
 .sg__wrap{padding:0 18px}
 .sg-sheet{grid-template-columns:repeat(2,1fr);gap:10px}
 .sg-shot__cap{padding:7px 9px 8px}
 .sg-shot__n{font-size:11px}
 .sg-shot__f{font-size:10px;padding:2px 6px}
 .sg-shot__f .lg{display:none}
 .sg-shot__f .sm{display:inline}
 .sg-strip{height:56px}
 .sg-final{padding:22px 20px}
 .sg-lb{padding:16px}
}
@media(max-width:420px){
 .sg-facts{grid-template-columns:1fr 1fr;gap:16px}
}
/* ландшафт телефона: лист не должен разъезжаться в одну колонку-простыню */
@media(max-height:520px) and (orientation:landscape){
 .sg__sec{padding:42px 0}
 .sg-sheet{grid-template-columns:repeat(4,1fr)}
 .sg-lb{padding:12px}
 .sg-lb__in{max-width:min(1100px,84vw)}
}
@media(prefers-reduced-motion:reduce){
 .sg-shot__box,.sg-shot__box img{transition:none}
}
</style>"""


def bgbar(idpref):
    """Переключатель подложки. Тот же орган управления в трёх местах страницы,
    состояние общее: атрибут data-bg на .sg."""
    opts = [('paper', 'Белый лист', '#fff'), ('blue', 'Синий Gyproc', '#4CA4E8'),
            ('ink', 'Графит', '#16191C'), ('check', 'Шахматка', '')]
    b = ''
    for key, name, sw in opts:
        cls = ' class="sg-check"' if key == 'check' else ''
        style = f' style="--sw:{sw}"' if sw else ''
        b += (f'<button type="button" data-bg="{key}"{cls}{style} '
              f'aria-pressed="{"true" if key == "paper" else "false"}">{name}</button>')
    return (f'<div class="sg-bg" id="{idpref}"><span class="sg-bg__t">Подложка</span>{b}</div>')


def hero():
    facts = ''.join(f'<div><b>{n}</b><span>{t}</span><em>{d}</em></div>'
                    for n, t, d in FACTS)
    return f'''<header class="sg__sec sg-hero"><div class="sg__wrap">
<p class="sg-crumbs"><a href="/">Главная</a> · <a href="/photo">Фотопродакшн</a> · Saint-Gobain</p>
<div class="sg-hero__top">
 <div>
  <p class="sg__kicker">Saint-Gobain · предметная съёмка · 2023</p>
  <h1>Съёмка продукции <em>Gyproc</em> для каталогов, сайта и POS</h1>
  <p class="sg__lead">Комплектующие для гипсокартонных систем: подвесы, соединители,
   ленты, крепёж, профили. Один съёмочный день на площадке заказчика, 63 позиции.
   Сдача под три канала сразу, поэтому в брифе было два технических требования,
   которые обычно не показывают в портфолио: любой кадр должен кадрироваться
   в квадрат, а фон у отдельных позиций должен быть вырезан.</p>
  <p class="sg__note">Ниже это можно проверить руками: подложка под кадрами
   переключается, лист сдачи кадрируется в квадрат целиком.</p>
 </div>
 <figure class="sg-hero__stage sg-hero__stage_pad" style="margin:0">
  <img src="{IMG}/item-2105.webp" width="900" height="600" alt="Соединитель «краб» Gyproc, предметная съёмка с вырезанным фоном" fetchpriority="high">
 </figure>
</div>
<div style="margin-top:26px">{bgbar('sg-bg-hero')}</div>
<div class="sg-facts">{facts}</div>
</div></header>'''


def brief():
    items = ''
    for i, (h, q, a) in enumerate(BRIEF, 1):
        items += (f'<div class="sg-brief__i"><span class="sg-brief__n">Пункт {i}</span>'
                  f'<h3 class="sg-brief__h">{H.escape(h)}</h3>'
                  f'<p class="sg-brief__q">«{H.escape(q)}»</p>'
                  f'<p class="sg-brief__a">{H.escape(a)}</p></div>')
    return f'''<section class="sg__sec"><div class="sg__wrap">
<p class="sg__kicker">Бриф заказчика</p>
<h2 class="sg__h">Четыре пункта задания и что по ним сдано</h2>
<p class="sg__lead">Задание пришло списком позиций и четырьмя комментариями к фото.
 Комментарии процитированы дословно.</p>
<div class="sg-brief">{items}</div>
</div></section>'''


def sheet():
    chips = ('<button type="button" class="sg-chip" data-sect="all" aria-pressed="true">'
             f'Все {ST["shots"]}</button>')
    for sec in SECTIONS:
        n = sum(1 for s in SHOTS if s['section'] == sec)
        chips += (f'<button type="button" class="sg-chip" data-sect="{H.escape(sec)}" '
                  f'aria-pressed="false">{H.escape(sec.capitalize())} {n}</button>')
    tiles = ''
    for s in SHOTS:
        f_cls = 'sg-shot__f_y' if s['fits'] else 'sg-shot__f_n'
        # на узком экране плашка сокращается: полный текст рядом с номером кадра
        # уже не помещается и жмётся к краю плитки
        f_txt = ('<b class="lg">в квадрат целиком</b><b class="sm">целиком</b>'
                 if s['fits'] else
                 '<b class="lg">квадрат по узлу</b><b class="sm">по узлу</b>')
        alt = f'{s["gtitle"]} Gyproc, кадр {s["id"]}'
        tiles += (
            f'<figure class="sg-shot" data-id="{s["id"]}" data-sect="{H.escape(s["section"])}" '
            f'data-fits="{1 if s["fits"] else 0}" style="--sq:{s["sq"]}" tabindex="0" role="button" '
            f'aria-label="Открыть кадр {s["id"]}: {H.escape(s["gtitle"])}">'
            f'<div class="sg-shot__box"><img src="{IMG}/frame-{s["id"]}.webp" width="1440" height="810" '
            f'loading="lazy" decoding="async" alt="{H.escape(alt)}"></div>'
            f'<figcaption class="sg-shot__cap"><span class="sg-shot__n">IMG_{s["id"]}</span>'
            f'<span class="sg-shot__f {f_cls}">{f_txt}</span></figcaption></figure>')
    return f'''<section class="sg__sec"><div class="sg__wrap">
<p class="sg__kicker">Лист сдачи</p>
<h2 class="sg__h">Все {ST["shots"]} {plural(ST["shots"], "кадр", "кадра", "кадров")} и тот самый квадрат</h2>
<p class="sg__lead">Кадры сданы в 16:9. Тумблер переводит лист в 1:1 и показывает,
 что останется в квадратном кадрировании у каждого файла. У компактных позиций
 предмет входит целиком, у длинномера и собранных систем квадрат берётся по узлу:
 это видно сразу на всём листе, а не на одном удачном примере.</p>
<div class="sg-ctrl">
 <div class="sg-ctrl__g">
  <span class="sg-bg__t">Кадр</span>
  <span class="sg-ratio" role="group" aria-label="Пропорция кадра">
   <button type="button" data-ratio="16" aria-pressed="true">16:9</button>
   <button type="button" data-ratio="1" aria-pressed="false">1:1</button>
  </span>
  <span class="sg-count" id="sg-count"></span>
 </div>
 <div class="sg-ctrl__g" id="sg-filter">{chips}</div>
</div>
<div style="margin-bottom:18px">{bgbar('sg-bg-sheet')}</div>
<div class="sg-sheet" id="sg-sheet" data-ratio="16">{tiles}</div>
</div></section>'''


def cut():
    hero_id = 2192
    card_id = 2196
    return f'''<section class="sg__sec"><div class="sg__wrap">
<p class="sg__kicker">Обработка</p>
<h2 class="sg__h">Фон вырезан по контуру, а не прямоугольником</h2>
<p class="sg__lead">Отдельные позиции сданы с прозрачностью, поэтому их можно класть
 на любую подложку без переделки: белый лист каталога, фирменный синий, тёмный
 фон POS-материала. Переключите подложку на шахматку, и станет видно, где
 проходит граница выреза: вместе с контуром вырезано {ST["holes"]} сквозных
 отверстий, включая перфорацию подвесов.</p>
<div style="margin-top:22px">{bgbar('sg-bg-cut')}</div>
<div class="sg-cut">
 <figure class="sg-cut__st" style="margin:0">
  <img src="{IMG}/frame-{hero_id}.webp" width="1440" height="810" loading="lazy"
   alt="Подвес акустический Gyproc с вырезанным по контуру фоном">
 </figure>
 <div class="sg-card">
  <div class="sg-card__sq"><img src="{IMG}/item-{card_id}.webp" loading="lazy"
   alt="Подвес акустический Gyproc в квадратной карточке товара"></div>
  <p class="sg-card__t">Подвес акустический</p>
  <p class="sg-card__p">Артикул · наличие · цена</p>
  <span class="sg-card__b">В корзину</span>
  <p class="sg-card__note">Макет карточки: тот же сданный файл без доработки
   ложится в квадрат каталога. Ради этого в брифе и стоял пункт про квадратное
   кадрирование.</p>
 </div>
</div>
</div></section>'''


def pairs():
    items = ''
    for solo, sys_, name, txt in PAIRS:
        items += f'''<article class="sg-pair"><div class="sg-pair__g">
<div class="sg-pair__c"><span class="sg-pair__l">позиция</span>
 <img src="{IMG}/frame-{solo}.webp" width="1440" height="810" loading="lazy"
  alt="{H.escape(name)} Gyproc, отдельная позиция"></div>
<div class="sg-pair__c"><span class="sg-pair__l">в системе</span>
 <img src="{IMG}/frame-{sys_}.webp" width="1440" height="810" loading="lazy"
  alt="{H.escape(name)} Gyproc в собранном каркасе"></div>
</div><div class="sg-pair__t"><h3>{H.escape(name)}</h3><p>{H.escape(txt)}</p></div></article>'''
    return f'''<section class="sg__sec"><div class="sg__wrap">
<p class="sg__kicker">Деталь и система</p>
<h2 class="sg__h">Одна и та же позиция: отдельно и в работе</h2>
<p class="sg__lead">Второй пункт брифа закрывался не отдельной съёмкой, а сборкой
 в кадре: специалист заказчика собирал каркас на съёмочном столе, и та же деталь,
 что лежала на белом, тут же вставала в систему. Для каталога это пара картинок
 на один артикул.</p>
<div class="sg-pairs">{items}</div>
</div></section>'''


def day():
    lo, hi = ST['frame_range']
    have = {s['id'] for s in SHOTS}
    ticks = ''.join(
        (f'<i class="on" title="IMG_{n}" data-id="{n}"></i>' if n in have else '<i></i>')
        for n in range(lo, hi + 1))
    total = hi - lo + 1
    figs = ''
    for slug, h, t in BACKSTAGE:
        figs += (f'<figure><img src="{IMG}/backstage-{slug}.jpg" loading="lazy" '
                 f'alt="{H.escape(h)}: бекстейдж съёмки продукции Gyproc">'
                 f'<figcaption><h3>{H.escape(h)}</h3><p>{H.escape(t)}</p></figcaption></figure>')
    return f'''<section class="sg__sec"><div class="sg__wrap">
<p class="sg__kicker">Смена</p>
<h2 class="sg__h">Один день, {total} срабатываний затвора, {ST["shots"]} кадра в сдаче</h2>
<p class="sg__lead">Счётчик камеры прошёл от IMG_{lo} до IMG_{hi}. Каждая засечка ниже это
 один кадр смены, тёмные засечки дошли до сдачи. Плотные участки это позиции,
 которые переставляли и пересвечивали дольше остальных.</p>
<div class="sg-day">
 <div class="sg-strip" id="sg-strip" role="img"
  aria-label="Шкала съёмочного дня: {total} кадров, {ST['shots']} в сдаче">{ticks}</div>
 <p class="sg-legend"><span><b>{ST['shots']}</b> кадров в сдаче</span>
  <span><b>{total}</b> срабатываний затвора</span>
  <span><b>23.11.2023</b> одна смена</span></p>
</div>
<div class="sg-back">{figs}</div>
<div class="sg-final">
 <h3>Что получил заказчик</h3>
 <p>Пакет из {ST["shots"]} файлов 5760×3240 с альфа-каналом: отдельные позиции
  и собранные системы, готовые под печатный каталог, карточку на сайте и POS.
  Отдельная съёмка под каждый канал не потребовалась, потому что требования
  всех трёх были собраны в один бриф до выезда на площадку.</p>
 <p>Такие же съёмки делаем под каталоги и маркетплейсы: <a href="/photo">фотопродакшн
  Hand Marketing</a>.</p>
</div>
</div></section>'''


LB = '''<div class="sg-lb" id="sg-lb" role="dialog" aria-modal="true" aria-label="Просмотр кадра">
<button type="button" class="sg-lb__x" id="sg-lb-x" aria-label="Закрыть">×</button>
<div class="sg-lb__in"><div class="sg-lb__st"><img id="sg-lb-img" src="" alt=""></div>
<div class="sg-lb__m"><span id="sg-lb-t"></span><span id="sg-lb-d"></span></div></div></div>'''

PAGE_JS = """<script>(function(){
var sg=document.querySelector('.sg');if(!sg)return;
var MAP=%MAP%;

// ── подложка: три переключателя, одно состояние ─────────────────────────────
function setBg(v){
 sg.setAttribute('data-bg',v);
 var st={paper:'#fff',blue:'#4CA4E8',ink:'#16191C'}[v]||'#fff';
 sg.style.setProperty('--stage',st);
 // шахматку рисуем градиентом на самих сценах
 [].forEach.call(sg.querySelectorAll('.sg-hero__stage,.sg-shot,.sg-cut__st,.sg-pair__c,.sg-lb__st'),function(e){
  if(v==='check'){e.style.backgroundImage='linear-gradient(45deg,#D6DADE 25%,transparent 25%,transparent 75%,#D6DADE 75%),linear-gradient(45deg,#D6DADE 25%,transparent 25%,transparent 75%,#D6DADE 75%)';
   e.style.backgroundSize='18px 18px';e.style.backgroundPosition='0 0,9px 9px';e.style.backgroundColor='#fff';}
  else{e.style.backgroundImage='';e.style.backgroundColor='';}
 });
 [].forEach.call(sg.querySelectorAll('.sg-bg button'),function(b){
  b.setAttribute('aria-pressed',b.getAttribute('data-bg')===v?'true':'false');});
}
[].forEach.call(sg.querySelectorAll('.sg-bg button'),function(b){
 b.addEventListener('click',function(){setBg(b.getAttribute('data-bg'));});});

// ── лист: пропорция, фильтр, счётчик ────────────────────────────────────────
var sheet=document.getElementById('sg-sheet'),
    countEl=document.getElementById('sg-count'),
    shots=[].slice.call(sheet.querySelectorAll('.sg-shot'));
function recount(){
 var vis=shots.filter(function(s){return !s.hasAttribute('hidden');});
 var fit=vis.filter(function(s){return s.getAttribute('data-fits')==='1';}).length;
 countEl.innerHTML='в квадрат целиком <b>'+fit+'</b> из <b>'+vis.length+'</b>';
}
[].forEach.call(document.querySelectorAll('.sg-ratio button'),function(b){
 b.addEventListener('click',function(){
  sheet.setAttribute('data-ratio',b.getAttribute('data-ratio'));
  [].forEach.call(document.querySelectorAll('.sg-ratio button'),function(o){
   o.setAttribute('aria-pressed',o===b?'true':'false');});
 });});
[].forEach.call(document.querySelectorAll('#sg-filter .sg-chip'),function(c){
 c.addEventListener('click',function(){
  var v=c.getAttribute('data-sect');
  [].forEach.call(document.querySelectorAll('#sg-filter .sg-chip'),function(o){
   o.setAttribute('aria-pressed',o===c?'true':'false');});
  shots.forEach(function(s){
   if(v==='all'||s.getAttribute('data-sect')===v)s.removeAttribute('hidden');
   else s.setAttribute('hidden','');});
  recount();
 });});
recount();

// ── просмотр кадра ──────────────────────────────────────────────────────────
var lb=document.getElementById('sg-lb'),lbImg=document.getElementById('sg-lb-img'),
    lbT=document.getElementById('sg-lb-t'),lbD=document.getElementById('sg-lb-d'),last=null;
function open(id){
 var m=MAP[id];if(!m)return;
 lbImg.src='/images/sgphoto/frame-'+id+'.webp';lbImg.alt=m.t+', кадр '+id;
 lbT.innerHTML='<b>'+m.t+'</b> · IMG_'+id;
 lbD.innerHTML=(m.f?'в квадрат целиком':'квадрат по узлу')+
  (m.h?' · вырезано отверстий: <b>'+m.h+'</b>':'');
 lb.classList.add('is-on');document.body.style.overflow='hidden';
 document.getElementById('sg-lb-x').focus();
}
function close(){lb.classList.remove('is-on');document.body.style.overflow='';
 if(last&&last.focus)last.focus();}
shots.forEach(function(s){
 function go(){last=s;open(s.getAttribute('data-id'));}
 s.addEventListener('click',go);
 s.addEventListener('keydown',function(e){
  if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});
});
lb.addEventListener('click',function(e){if(e.target===lb)close();});
document.getElementById('sg-lb-x').addEventListener('click',close);
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.classList.contains('is-on'))close();});

// ── шкала смены: засечка открывает кадр ─────────────────────────────────────
var strip=document.getElementById('sg-strip');
if(strip)strip.addEventListener('click',function(e){
 var id=e.target&&e.target.getAttribute&&e.target.getAttribute('data-id');
 if(id){last=null;open(id);}});
})();</script>"""

HEAD = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<!--custom-page-->'
        f'<title>{TITLE}</title>'
        f'<meta name="description" content="{DESCR}">'
        f'<link rel="canonical" href="{URL}">'
        '<meta property="og:type" content="article">'
        f'<meta property="og:title" content="{TITLE}">'
        f'<meta property="og:description" content="{DESCR}">'
        f'<meta property="og:url" content="{URL}">'
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/backstage-setup.jpg">'
        '<link rel="stylesheet" href="/fonts/exo2-spectral.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    thin = {str(s['id']): {'t': s['gtitle'], 'f': 1 if s['fits'] else 0, 'h': s['holes']}
            for s in SHOTS}
    js = PAGE_JS.replace('%MAP%', json.dumps(thin, ensure_ascii=False,
                                             separators=(',', ':')))
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer()
    body = (f'{rc.header()}<main class="sg" data-bg="paper">{hero()}{brief()}{sheet()}'
            f'{cut()}{pairs()}{day()}</main>{LB}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'photo', 'saint-gobain')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
