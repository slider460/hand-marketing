#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/powertechnologies/index.html — кейс «История успеха
Power Technologies» (фильм о временном энергоснабжении объектов ЧМ-2018).

Что было: запечённая Tilda-страница плюс отдельная мобильная копия .mhome, оба
ролика за одинаковыми плашками «Смотреть», один и тот же постер на мобильной.

Дизайн-концепция: главное в кейсе — масштаб проекта. Чемпионат шёл месяц в
одиннадцати городах на двенадцати стадионах, и временное энергоснабжение всех
объектов держала одна компания. Страница ведёт от этого масштаба к фильму:

  • герой и цифры проекта (150 ДГУ, 960 км кабелей, 75 МВт, 300 человек) сняты
    с инфографики самого фильма, география — одиннадцать городов чемпионата;
  • объекты и съёмка: что именно запитывали и как снимали на действующих
    площадках мобильными группами;
  • голоса в кадре взяты с титров фильма, клик по карточке перематывает плеер;
  • фильм в финале страницы: большой плеер с главами. То, что версий две
    (11:39 и 4:27), живёт скромным переключателем над плеером, а не отдельным
    сюжетом страницы;
  • картинки — кадры роликов (scripts/powertech-assets.py), из полной версии
    режем только то, чего в короткой нет: она 640x360, короткая 1280x720;
  • тайминги глав короткой версии сверены с полной покадрово
    (scripts/powertech-edl.py -> powertech_edl.json).

Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->. После генерации гонять add_cookie_consent.py и
add_metrika_goals.py (они затираются регенерацией)."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

URL = 'https://hand-marketing.ru/video/powertechnologies/'
IMG = '/images/powertech'
EDL = json.load(open(os.path.join(HERE, 'powertech_edl.json'), encoding='utf-8'))

DUR_F = int(EDL['long']['dur'])     # 699, полная версия
DUR_S = int(EDL['short']['dur'])    # 267, короткая версия


def mmss(sec):
    return f'{int(sec) // 60}:{int(sec) % 60:02d}'


TIME_F, TIME_S = mmss(DUR_F), mmss(DUR_S)

# ─── главы обеих версий ─────────────────────────────────────────────────────
# секунда, название, подпись
CHAPTERS = {
    'full': [
        (0,   'Пролог',        'Чемпионат глазами зрителя'),
        (88,  'Титр проекта',  'Временное энергоснабжение ЧМ-2018'),
        (150, 'Подготовка',    'Стадионы, площадки, монтаж'),
        (330, 'Цифры проекта', 'Инфографика с итогами'),
        (358, 'Временная энергетика', 'Глава фильма'),
        (469, 'Резервирование мощностей', 'Глава фильма'),
        (610, 'Командная работа', 'Глава фильма'),
        (694, 'Финал',         'Кубок чемпионата'),
    ],
    'short': [
        (0,   'Открытие',      'Трансляция и стадион'),
        (27,  'Титр проекта',  'Временное энергоснабжение ЧМ-2018'),
        (37,  'Площадки',      'Монтаж на стадионах'),
        (74,  'Цифры проекта', 'Инфографика с итогами'),
        (98,  'Временная энергетика', 'Глава фильма'),
        (135, 'Стадион «Фишт»', 'Сочи, распределение питания'),
        (181, 'Вещатели',      'NBC и Telemundo в кадре'),
        (255, 'Финал',         'Кубок чемпионата'),
    ],
}

VERSIONS = [
    ('full',  'Полная версия',   TIME_F, '/media/pt-film-long.mp4',  'poster-full',
     'Вся хронология проекта: подготовка, монтаж, интервью команды, работа смен во время матчей.',
     'Переговоры, презентации, показы для партнёров'),
    ('short', 'Короткая версия', TIME_S, '/media/pt-film-short.mp4', 'poster-short',
     'Тот же сюжет плотнее: ключевые объекты, цифры проекта и финал, без длинных подводок.',
     'Соцсети, выставочный стенд, рассылка'),
]

# ─── цифры с инфографики фильма (дословно с кадра, 5:30) ────────────────────
NUMBERS = [
    ('', '150', 'дизель-генераторных установок'),
    ('', '80', 'топливных ёмкостей'),
    ('', '2500', 'единиц щитового оборудования'),
    ('свыше', '960', 'километров кабелей'),
    ('более', '75', 'мегаватт суммарной мощности'),
    ('свыше', '300', 'человек в проекте'),
]

# ─── голоса в кадре: имя, должность, кадр, секунда в полной, секунда в короткой
VOICES = [
    ('Эдуард Антонян', 'Генеральный менеджер специальных проектов Power Technologies',
     'sp-antonyan', 151, None),
    ('Александр Крылов', 'Операционный директор Power Technologies, Нижний Новгород',
     'sp-krylov', 194, None),
    ('Леонид Сапожников', 'Операционный директор Power Technologies на стадионе «Калининград»',
     'sp-sapozhnikov', 266, None),
    ('Малкольм Бест', 'Технический директор Power Technologies',
     'sp-best', 401, 105),
    ('Олег Щербаков', 'Операционный директор Power Technologies на стадионе «Фишт», Сочи',
     'sp-sherbakov', 496, 140),
    ('Чарльз Яблонски', 'Менеджер по энергетическим проектам NBC',
     'sp-yablonski', 552, 180),
    ('Питер Гринтер', 'Представитель логистической службы NBC и Telemundo',
     'sp-grinter', 589, 217),
    ('Уаррам Питер Леонард', 'Инженер по энергетике HBS на стадионе в Нижнем Новгороде',
     'sp-warram', 567, 196),
]

# ─── география чемпионата: город и его арены ────────────────────────────────
# сколько площадок попало в кадр фильма, на странице НЕ показываем: съёмка шла
# не на всех стадионах, и такая отметка читалась бы как минус проекту
CITIES = [
    ('Москва', 'Лужники, Спартак'),
    ('Санкт-Петербург', 'Санкт-Петербург'),
    ('Калининград', 'Калининград'),
    ('Нижний Новгород', 'Нижний Новгород'),
    ('Казань', 'Казань Арена'),
    ('Самара', 'Самара Арена'),
    ('Волгоград', 'Волгоград Арена'),
    ('Ростов-на-Дону', 'Ростов Арена'),
    ('Саранск', 'Мордовия Арена'),
    ('Екатеринбург', 'Екатеринбург Арена'),
    ('Сочи', 'Фишт'),
]

# ─── объекты проекта: кадр, секунда в полной версии, заголовок, подпись ─────
OBJECTS = [
    ('obj-match', 309, 'Стадионы во время матчей',
     'Смены дежурили на аренах всё время подготовки и проведения игр, '
     'а отключение на объекте чемпионата увидел бы весь мир'),
    ('cut-ibc', 222, 'Международный вещательный центр',
     'Через IBC шло вещание на весь мир, и питание там нельзя было прерывать ни на минуту'),
    ('poster-full', 640, 'Аппаратные и позиции вещателей',
     'Режиссёрские, ПТС, спутниковые тарелки и студии вещателей на самих стадионах'),
    ('cut-fans', 616, 'Города вокруг чемпионата',
     'Фан-зоны и городские площадки: чемпионат шёл не только на аренах'),
]

# ─── съёмка ─────────────────────────────────────────────────────────────────
CRAFT = [
    ('shoot-camera', 'Съёмка на поле стадиона между матчами'),
    ('shoot-cables', 'Кабельные трассы: сотни километров линий'),
    ('shoot-gen', 'Доставка и установка дизель-генераторной установки'),
    ('shoot-fence', 'Обход площадки вместе с инженерами'),
]


# ─── CSS ────────────────────────────────────────────────────────────────────
PAGE_CSS = """<style id="pt-css">
.pt{--bg:#080B12;--bg2:#0E1420;--card:#131B2A;--line:rgba(255,255,255,.10);
 --tx:#E9EDF5;--mu:#8D97A9;--full:#3F8CFF;--short:#F5A524;--acc:var(--full);
 background:var(--bg);color:var(--tx);font-family:'Onest',-apple-system,Arial,sans-serif;
 overflow-x:hidden}
.pt *,.pt *::before,.pt *::after{box-sizing:border-box}
.pt h1,.pt h2,.pt h3{font-family:'Manrope','Onest',Arial,sans-serif;letter-spacing:-.03em;margin:0}
.pt__w{max-width:1180px;margin:0 auto;padding:0 40px}
.pt__s{padding:92px 0}
.pt__lab{display:flex;align-items:center;gap:12px;margin:0 0 18px;font-size:12px;font-weight:700;
 letter-spacing:.16em;text-transform:uppercase;color:var(--mu)}
.pt__lab b{color:var(--acc);font-weight:800}
.pt__lab::after{content:"";flex:1;height:1px;background:var(--line)}
.pt__h2{font-size:clamp(30px,3.6vw,46px);line-height:1.04;font-weight:800}
.pt__intro{margin:16px 0 0;max-width:760px;font-size:17px;line-height:1.65;color:var(--mu)}
.pt a:focus-visible,.pt button:focus-visible{outline:2px solid var(--acc);outline-offset:3px;border-radius:6px}
.pt .r{opacity:0;transform:translateY(18px);transition:opacity .7s ease,transform .7s ease}
.pt .r.is-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.pt .r{transition:none}}

/* ── герой ───────────────────────────────────────────────────────────────── */
.pt__hero{position:relative;padding:74px 0 78px;overflow:hidden}
.pt__hero::before{content:"";position:absolute;inset:-20% -10% auto -10%;height:120%;
 background:radial-gradient(60% 60% at 22% 8%,rgba(63,140,255,.20),transparent 70%),
            radial-gradient(46% 46% at 88% 22%,rgba(245,165,36,.16),transparent 70%);
 pointer-events:none}
.pt__hero>*{position:relative}
.pt__kick{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:26px}
.pt__kick span{padding:7px 14px;border:1px solid var(--line);border-radius:999px;
 font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mu)}
.pt__kick span.on{border-color:transparent;background:var(--full);color:#06080D}
.pt__t{font-size:clamp(40px,6.6vw,84px);line-height:.98;font-weight:800}
.pt__t em{font-style:normal;color:var(--full)}
.pt__sub{margin:24px 0 0;max-width:660px;font-size:clamp(17px,1.5vw,19px);line-height:1.6;color:var(--mu)}
.pt__act{margin-top:38px;display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.pt__btn{display:inline-flex;align-items:center;gap:10px;padding:16px 30px;border:0;border-radius:999px;
 background:var(--full);color:#06080D;font-family:'Manrope',Arial,sans-serif;font-size:16px;font-weight:800;
 cursor:pointer;text-decoration:none;transition:transform .15s,box-shadow .15s}
.pt__btn:hover{transform:translateY(-2px);box-shadow:0 18px 34px -18px rgba(63,140,255,.9)}
.pt__ghost{display:inline-flex;align-items:center;gap:10px;padding:16px 26px;border:1px solid var(--line);
 border-radius:999px;color:var(--tx);text-decoration:none;font-family:'Manrope',Arial,sans-serif;
 font-size:15px;font-weight:800;transition:border-color .2s}
.pt__ghost:hover{border-color:var(--full)}
.pt__facts{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin:52px 0 0;
 padding-top:26px;border-top:1px solid var(--line)}
.pt__facts dt{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mu)}
.pt__facts dd{margin:8px 0 0;font-family:'Manrope',Arial,sans-serif;font-size:17px;font-weight:700;line-height:1.3}

/* ── плеер ───────────────────────────────────────────────────────────────── */
.pt__film{background:var(--bg2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.pt__switch{display:inline-flex;padding:5px;gap:5px;border-radius:999px;background:#0A0F1A;
 border:1px solid var(--line);margin-bottom:24px}
.pt__switch button{display:flex;align-items:baseline;gap:9px;padding:11px 22px;border:0;border-radius:999px;
 background:transparent;color:var(--mu);font-family:'Manrope',Arial,sans-serif;font-size:15px;
 font-weight:800;cursor:pointer;transition:background .2s,color .2s}
.pt__switch button span{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;opacity:.75}
.pt__switch button[aria-selected="true"]{color:#06080D}
.pt__switch button[data-v="full"][aria-selected="true"]{background:var(--full)}
.pt__switch button[data-v="short"][aria-selected="true"]{background:var(--short)}
.pt__screen{position:relative;border-radius:20px;overflow:hidden;background:#000;
 box-shadow:0 40px 90px -50px rgba(0,0,0,.9);border:1px solid var(--line)}
.pt__screen video{display:block;width:100%;aspect-ratio:16/9;background:#000}
.pt__chaps{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:18px}
.pt__chap{padding:13px 15px;border-radius:13px;border:1px solid var(--line);background:var(--bg);
 color:var(--tx);text-align:left;cursor:pointer;font-family:inherit;transition:border-color .2s,background .2s}
.pt__chap:hover{background:var(--card);border-color:var(--acc)}
.pt__chap[aria-current="true"]{border-color:var(--acc);background:var(--card)}
.pt__chap b{display:block;font-family:'Manrope',Arial,sans-serif;font-size:14px;font-weight:800}
.pt__chap i{display:block;margin-top:4px;font-style:normal;font-size:12px;line-height:1.35;color:var(--mu)}
.pt__chap u{display:inline-block;margin-top:6px;text-decoration:none;font-family:'JetBrains Mono',monospace;
 font-size:11px;color:var(--acc)}

.pt__note{margin:16px 0 0;font-size:13.5px;line-height:1.6;color:var(--mu);max-width:720px}
.pt__note b{color:var(--tx);font-weight:700}

/* ── география чемпионата ────────────────────────────────────────────────── */
.pt__geo{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:34px}
.pt__city{position:relative;padding:20px 22px;border-radius:16px;border:1px solid var(--line);
 background:var(--bg2)}
.pt__city b{display:block;font-family:'Manrope',Arial,sans-serif;font-size:18px;font-weight:800}
.pt__city span{display:block;margin-top:6px;font-size:13.5px;line-height:1.4;color:var(--mu)}

/* ── объекты ─────────────────────────────────────────────────────────────── */
.pt__objs{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:34px}
.pt__obj{padding:0;border:1px solid var(--line);border-radius:20px;overflow:hidden;background:var(--bg2);
 color:var(--tx);text-align:left;cursor:pointer;font-family:inherit;transition:border-color .2s,transform .2s}
.pt__obj:hover{transform:translateY(-4px);border-color:var(--full)}
.pt__obj img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.pt__obj div{padding:20px 24px 24px}
.pt__obj b{display:block;font-family:'Manrope',Arial,sans-serif;font-size:19px;font-weight:800}
.pt__obj i{display:block;margin-top:8px;font-style:normal;font-size:14.5px;line-height:1.55;color:var(--mu)}
.pt__obj u{display:inline-block;margin-top:12px;text-decoration:none;font-family:'JetBrains Mono',monospace;
 font-size:11px;color:var(--full)}

/* ── цифры фильма ────────────────────────────────────────────────────────── */
.pt__nums{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:34px}
.pt__num{padding:26px 26px 24px;border-radius:18px;border:1px solid var(--line);background:var(--bg2)}
.pt__num em{display:block;margin-bottom:4px;font-style:normal;font-size:12px;font-weight:700;
 letter-spacing:.12em;text-transform:uppercase;color:var(--mu)}
.pt__num b{display:block;font-family:'Manrope',Arial,sans-serif;font-size:44px;font-weight:800;line-height:1;
 color:var(--acc)}
.pt__num span{display:block;margin-top:10px;font-size:15px;line-height:1.45;color:var(--mu)}
.pt__numshot{margin-top:26px;display:grid;grid-template-columns:1fr 1fr;gap:18px}
.pt__numshot button{padding:0;border:1px solid var(--line);border-radius:16px;overflow:hidden;
 background:none;cursor:pointer;display:block}
.pt__numshot img{display:block;width:100%;height:auto}

/* ── голоса ──────────────────────────────────────────────────────────────── */
.pt__voices{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:34px}
.pt__voice{padding:0;border:1px solid var(--line);border-radius:18px;overflow:hidden;background:var(--bg2);
 color:var(--tx);text-align:left;cursor:pointer;font-family:inherit;transition:border-color .2s,transform .2s}
.pt__voice:hover{transform:translateY(-4px);border-color:var(--acc)}
.pt__voice img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.pt__voice div{padding:16px 18px 18px}
.pt__voice b{display:block;font-family:'Manrope',Arial,sans-serif;font-size:16px;font-weight:800}
.pt__voice i{display:block;margin-top:6px;font-style:normal;font-size:12.5px;line-height:1.45;color:var(--mu)}
.pt__voice u{display:inline-block;margin-top:10px;text-decoration:none;font-family:'JetBrains Mono',monospace;
 font-size:11px;color:var(--acc)}

/* ── съёмка ──────────────────────────────────────────────────────────────── */
.pt__craft{display:grid;grid-template-columns:1.25fr 1fr;gap:34px;margin-top:34px;align-items:start}
.pt__crafttxt p{margin:0 0 16px;font-size:16px;line-height:1.7;color:var(--mu)}
.pt__crafttxt p b{color:var(--tx)}
.pt__grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.pt__grid figure{margin:0;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:var(--bg2)}
.pt__grid img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.pt__grid figcaption{padding:12px 14px;font-size:12.5px;line-height:1.45;color:var(--mu)}

/* ── задача/решение/результат ────────────────────────────────────────────── */
.pt__story{display:grid;gap:18px;margin-top:34px}
.pt__step{display:grid;grid-template-columns:200px 1fr;gap:30px;padding:30px 32px;border-radius:20px;
 border:1px solid var(--line);background:var(--bg2)}
.pt__step .n{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--acc);letter-spacing:.06em}
.pt__step h3{font-size:23px;font-weight:800;margin-bottom:12px}
.pt__step p{margin:0 0 12px;font-size:16px;line-height:1.7;color:var(--mu)}
.pt__step p:last-child{margin-bottom:0}
.pt__step ul{margin:14px 0 0;padding:0;list-style:none;display:grid;gap:9px}
.pt__step li{position:relative;padding-left:22px;font-size:15px;line-height:1.55;color:var(--mu)}
.pt__step li::before{content:"";position:absolute;left:0;top:8px;width:8px;height:8px;border-radius:50%;
 background:var(--acc)}

@media(max-width:1020px){
 .pt__w{padding:0 24px}.pt__s{padding:66px 0}
 .pt__facts{grid-template-columns:1fr 1fr;gap:18px}
 .pt__chaps{grid-template-columns:1fr 1fr}
 .pt__voices{grid-template-columns:1fr 1fr}
 .pt__nums{grid-template-columns:1fr 1fr}
 .pt__geo{grid-template-columns:1fr 1fr}
 .pt__craft{grid-template-columns:1fr;gap:26px}
 .pt__step{grid-template-columns:1fr;gap:12px;padding:24px}
}
@media(max-width:640px){
 .pt__w{padding:0 18px}.pt__s{padding:52px 0}
 .pt__hero{padding:44px 0 52px}
 .pt__facts{grid-template-columns:1fr}
 .pt__chaps{grid-template-columns:1fr}
 .pt__nums{grid-template-columns:1fr}
 .pt__numshot{grid-template-columns:1fr}
 .pt__voices{grid-template-columns:1fr}
 .pt__objs{grid-template-columns:1fr}
 /* города оставляем в две колонки: карточки короткие, иначе список на пол-экрана */
 .pt__geo{grid-template-columns:1fr 1fr;gap:10px}
 .pt__city{padding:15px 14px 16px}
 .pt__city b{font-size:15px}
 .pt__city span{font-size:12px;margin-top:4px}
 .pt__grid{grid-template-columns:1fr}
 .pt__act{gap:10px}
 .pt__btn,.pt__ghost{width:100%;justify-content:center}
 .pt__switch{width:100%}
 .pt__switch button{flex:1;justify-content:center;padding:11px 12px}
}
</style>"""

PLAY = '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M8 5v14l11-7z"/></svg>'


# ─── секции ─────────────────────────────────────────────────────────────────
def hero():
    facts = ''.join(f'<div><dt>{t}</dt><dd>{v}</dd></div>' for t, v in [
        ('Клиент', 'Power Technologies'),
        ('Событие', 'Чемпионат мира по футболу, 2018'),
        ('География', '11 городов, 12 стадионов'),
        ('Работы', 'Сценарий, съёмка, постпродакшн'),
    ])
    return f'''<section class="pt__hero"><div class="pt__w">
<div class="pt__kick"><span>Power Technologies</span><span>Video Production</span><span class="on">2018</span></div>
<h1 class="pt__t">История успеха<br><em>Power Technologies</em></h1>
<p class="pt__sub">Месяц чемпионата мира по футболу, одиннадцать городов и двенадцать стадионов.
Временное энергоснабжение всех объектов держала одна компания, и мы сняли об этом фильм,
пока проект шёл: на площадках, в аппаратных и на трибунах.</p>
<div class="pt__act">
<a class="pt__btn" href="#film">{PLAY} Смотреть фильм</a>
<a class="pt__ghost" href="#scale">Масштаб проекта</a></div>
<dl class="pt__facts">{facts}</dl>
</div></section>'''


def scale():
    nums = ''.join(f'<div class="pt__num">{f"<em>{p}</em>" if p else ""}'
                   f'<b>{b}</b><span>{s}</span></div>' for p, b, s in NUMBERS)
    cities = ''.join(f'<div class="pt__city"><b>{c}</b><span>{st}</span></div>'
                     for c, st in CITIES)
    return f'''<section class="pt__s" id="scale"><div class="pt__w">
<p class="pt__lab"><b>Масштаб</b> · чемпионат целиком</p>
<h2 class="pt__h2">Одиннадцать городов, двенадцать стадионов</h2>
<p class="pt__intro">Чемпионат шёл месяц от Калининграда до Екатеринбурга и от Санкт-Петербурга
до Сочи. Стадионы, тренировочные площадки, вещательные центры и фан-зоны работали
одновременно, и каждый объект нужно было запитать, зарезервировать и держать под
наблюдением до последнего матча.</p>
<div class="pt__geo r">{cities}</div>
<div class="pt__nums r">{nums}</div>
<div class="pt__numshot r">
<button type="button" data-go="full" data-sec="330" aria-label="Смотреть эпизод с цифрами проекта">
<img src="{IMG}/nums-a.jpg" width="1200" height="675" loading="lazy"
 alt="Кадр фильма: 150 дизель-генераторных установок, 80 топливных ёмкостей, 2500 единиц щитового оборудования"></button>
<button type="button" data-go="full" data-sec="345" aria-label="Смотреть эпизод с цифрами проекта">
<img src="{IMG}/nums-b.jpg" width="1200" height="675" loading="lazy"
 alt="Кадр фильма: свыше 960 километров кабелей, более 75 мегаватт, свыше 300 человек"></button>
</div>
<p class="pt__note">Цифры взяты с инфографики самого фильма: <b>для временного энергоснабжения
всех объектов чемпионата было задействовано</b> именно столько техники и людей.
Клик по кадру открывает этот эпизод.</p>
</div></section>'''


def objects():
    cards = ''.join(
        f'<button class="pt__obj" type="button" data-go="full" data-sec="{sec}">'
        f'<img src="{IMG}/{shot}.jpg" width="1100" height="619" loading="lazy" alt="Кадр фильма: {ttl}">'
        f'<div><b>{ttl}</b><i>{descr}</i><u>{PLAY} эпизод фильма {mmss(sec)}</u></div></button>'
        for shot, sec, ttl, descr in OBJECTS)
    return f'''<section class="pt__s"><div class="pt__w">
<p class="pt__lab"><b>Объекты</b> · что было под напряжением</p>
<h2 class="pt__h2">Не только стадионы</h2>
<p class="pt__intro">Матч видят на трибунах, но зависит от питания гораздо больше: вещательный
центр, аппаратные, ПТС и спутниковые тарелки, городские площадки. Фильм показывает эту изнанку
целиком, а не парадную часть. Клик по карточке открывает нужный эпизод.</p>
<div class="pt__objs r">{cards}</div>
</div></section>'''


def film():
    tabs = ''.join(
        f'<button role="tab" type="button" data-v="{k}" id="pt-tab-{k}" aria-controls="pt-video"'
        f' aria-selected="{"true" if i == 0 else "false"}">{name}<span>{time}</span></button>'
        for i, (k, name, time, _s, _p, _d, _u) in enumerate(VERSIONS))
    return f'''<section class="pt__s pt__film" id="film"><div class="pt__w">
<p class="pt__lab"><b>Фильм</b> · история успеха Power Technologies</p>
<h2 class="pt__h2">Смотреть</h2>
<p class="pt__intro">Собран из материала, снятого во время чемпионата: объекты, работа смен,
синхроны руководителей проекта и вещателей. Ниже главы, по ним можно перематывать.</p>
<div class="pt__switch" role="tablist" aria-label="Версия фильма">{tabs}</div>
<div class="pt__screen"><video id="pt-video" controls preload="none" playsinline
 poster="{IMG}/poster-full.jpg" width="1280" height="720">
<source id="pt-src" src="/media/pt-film-long.mp4" type="video/mp4">Ваш браузер не воспроизводит видео.</video></div>
<div class="pt__chaps r" id="pt-chaps" role="group" aria-label="Главы фильма"></div>
<p class="pt__note">По просьбе заказчика фильм собран в двух версиях: полная {TIME_F}
для переговоров и показов, короткая {TIME_S} для соцсетей и стенда. Переключатель над плеером.</p>
</div></section>'''


def voices():
    cards = ''
    for name, role, shot, sf, ss in VOICES:
        v, sec = ('short', ss) if ss is not None else ('full', sf)
        where = f'в короткой {mmss(ss)}' if ss is not None else f'в полной {mmss(sf)}'
        cards += (f'<button class="pt__voice" type="button" data-go="{v}" data-sec="{sec}">'
                  f'<img src="{IMG}/{shot}.jpg" width="900" height="506" loading="lazy"'
                  f' alt="Кадр фильма: {name}">'
                  f'<div><b>{name}</b><i>{role}</i><u>{PLAY} {where}</u></div></button>')
    return f'''<section class="pt__s" id="voices"><div class="pt__w">
<p class="pt__lab"><b>Герои</b> · восемь синхронов</p>
<h2 class="pt__h2">Кто говорит в кадре</h2>
<p class="pt__intro">Историю рассказывают не закадровым текстом, а люди проекта: операционные
директора на стадионах «Калининград» и «Фишт», технический директор, генеральный менеджер
специальных проектов. Отдельно говорят те, кто вещал чемпионат: NBC, Telemundo и HBS,
хозяин трансляции. Для них Power Technologies держала питание на объектах вещания.</p>
<div class="pt__voices r">{cards}</div>
</div></section>'''


def craft():
    figs = ''.join(
        f'<figure><img src="{IMG}/{shot}.jpg" width="1100" height="619" loading="lazy" alt="{cap}">'
        f'<figcaption>{cap}</figcaption></figure>' for shot, cap in CRAFT)
    return f'''<section class="pt__s"><div class="pt__w">
<p class="pt__lab"><b>Съёмка</b> · месяц в городах-участниках</p>
<h2 class="pt__h2">Как снимали</h2>
<div class="pt__craft r">
<div class="pt__crafttxt">
<p>Монтажные и пусконаладочные работы шли на стадионах параллельно во всех городах,
и ждать, пока объекты освободятся, было нельзя. <b>Мы собрали мобильные съёмочные группы</b>:
видеооператор, репортёр для интервью, полевой директор и технический специалист, который
отвечал за допуск и безопасность на действующем объекте.</p>
<p>Группы работали месяц: снимали монтаж, оборудование, интервью и команду за работой,
подстраиваясь под график подготовки и матчей. Материал сводился в Москве параллельно со съёмкой,
поэтому первый монтаж собрался сразу после последнего съёмочного дня.</p>
<p>Фильм смонтирован из этого материала: <b>ни одного стокового кадра</b>, все объекты, люди
и техника в кадре относятся к проекту.</p>
</div>
<div class="pt__grid">{figs}</div>
</div></div></section>'''


def story():
    return f'''<section class="pt__s"><div class="pt__w">
<p class="pt__lab"><b>Кейс</b> · задача, решение, результат</p>
<div class="pt__story r">
<div class="pt__step"><div class="n">01 / Задача</div>
<div><h3>Зафиксировать опыт, который больше не повторится</h3>
<p>Power Technologies организовала временное энергоснабжение на всех стадионах и во всех
городах-участниках чемпионата мира по футболу 2018 года. Такой проект не повторяется:
объекты сдаются, площадки разбираются, команда расходится по другим контрактам.
Компании нужен был фильм, который зафиксирует этот опыт и будет работать как аргумент
в переговорах с заказчиками уровня чемпионата.</p></div></div>
<div class="pt__step"><div class="n">02 / Решение</div>
<div><h3>Мобильные группы и съёмка на действующих объектах</h3>
<p>Разработали сценарий и сняли материал прямо во время подготовки и проведения матчей.
Съёмка шла месяц, параллельно в нескольких городах, на объектах с ограниченным доступом.</p>
<ul><li>Сценарий и структура фильма: от эмоции чемпионата к инженерной изнанке</li>
<li>Восемь синхронов: руководители проекта и вещатели NBC, Telemundo и HBS</li>
<li>Инфографика с итоговыми цифрами проекта</li>
<li>Постпродакшн: монтаж, графика, звук, цветокоррекция</li></ul></div></div>
<div class="pt__step"><div class="n">03 / Результат</div>
<div><h3>Фильм, который защищает опыт компании</h3>
<p>Получилась история успеха, снятая на месте событий: одиннадцать городов, двенадцать
стадионов, вещательный центр, смены на объектах и люди, которые за это отвечали.
Компания получила материал, который показывает её работу на проекте мирового уровня
и продолжает работать в переговорах спустя годы.</p>
<p>Фильм собран в двух версиях: полная {TIME_F} для переговоров и показов, короткая
{TIME_S} для соцсетей и выставочного стенда.</p></div></div>
</div></div></section>'''


# ─── JS ─────────────────────────────────────────────────────────────────────
CH_JSON = json.dumps(CHAPTERS, ensure_ascii=False)
V_JSON = json.dumps({k: {'src': src, 'poster': f'{IMG}/{p}.jpg', 'dur': (DUR_F if k == 'full' else DUR_S)}
                     for k, _n, _t, src, p, _d, _u in VERSIONS}, ensure_ascii=False)

PAGE_JS = """<script>(function(){
 var CH=""" + CH_JSON + """,V=""" + V_JSON + """;
 var root=document.querySelector('.pt'),v=document.getElementById('pt-video'),
     src=document.getElementById('pt-src'),chaps=document.getElementById('pt-chaps'),
     tabs=[].slice.call(document.querySelectorAll('.pt__switch button')),cur='full';
 function mmss(s){s=Math.max(0,Math.round(s));return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2);}
 // ── главы текущей версии ────────────────────────────────────────────────
 function drawChaps(){
  chaps.innerHTML=CH[cur].map(function(c){
   return '<button class="pt__chap" type="button" data-sec="'+c[0]+'" data-chap="'+c[0]+'">'+
    '<b>'+c[1]+'</b><i>'+c[2]+'</i><u>'+mmss(c[0])+'</u></button>';}).join('');
 }
 // ── переключение версии ─────────────────────────────────────────────────
 function setVersion(k,keep){
  if(k===cur&&keep)return;
  cur=k;root.setAttribute('data-v',k);
  tabs.forEach(function(b){b.setAttribute('aria-selected',b.getAttribute('data-v')===k?'true':'false');});
  v.pause();src.src=V[k].src;v.setAttribute('poster',V[k].poster);v.load();
  drawChaps();
 }
 tabs.forEach(function(b){b.addEventListener('click',function(){setVersion(b.getAttribute('data-v'),true);});});
 // ── перемотка: [data-go] задаёт версию, [data-sec] секунду ──────────────
 function seek(sec,scroll){
  var go=function(){try{v.currentTime=sec;}catch(e){}v.play().catch(function(){});};
  if(v.readyState<1){v.addEventListener('loadedmetadata',go,{once:true});v.load();}else{go();}
  if(scroll!==false){var r=v.getBoundingClientRect();
   if(r.top<70||r.bottom>innerHeight)v.scrollIntoView({behavior:'smooth',block:'center'});}
 }
 document.addEventListener('click',function(e){
  var b=e.target.closest?e.target.closest('[data-sec]'):null;
  if(!b||!root.contains(b))return;
  e.preventDefault();
  var go=b.getAttribute('data-go');
  if(go)setVersion(go,true);
  seek(parseFloat(b.getAttribute('data-sec')));
 });
 // ── активная глава ──────────────────────────────────────────────────────
 var last=-1;
 v.addEventListener('timeupdate',function(){
  var list=[].slice.call(chaps.querySelectorAll('[data-chap]')),t=v.currentTime,c=0;
  list.forEach(function(n,i){if(t>=parseFloat(n.getAttribute('data-chap')))c=i;});
  if(c===last)return;last=c;
  list.forEach(function(n,i){n.setAttribute('aria-current',i===c?'true':'false');});});
 drawChaps();
 // ── появление блоков ────────────────────────────────────────────────────
 var els=[].slice.call(document.querySelectorAll('.pt .r'));
 function inn(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(n);else io.observe(n);});
})();</script>"""


def video_ld(name, descr, url, poster, dur_iso):
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            f'"@type":"VideoObject","name":"{name}","description":"{descr}",'
            f'"thumbnailUrl":"https://hand-marketing.ru{poster}",'
            f'"contentUrl":"https://hand-marketing.ru{url}","duration":"{dur_iso}",'
            '"uploadDate":"2018-09-01","publisher":{"@type":"Organization","name":"Hand Marketing",'
            '"logo":{"@type":"ImageObject","url":"https://hand-marketing.ru/images/lib/'
            'as3365-6332-4339-a263-313566616365/152.png"}}}</script>')


LD = (video_ld('История успеха Power Technologies, полная версия',
                'Фильм об организации временного энергоснабжения объектов чемпионата мира '
                'по футболу 2018 года. Полная версия 11 минут 39 секунд.',
                '/media/pt-film-long.mp4', f'{IMG}/poster-full.jpg', 'PT11M39S') +
      video_ld('История успеха Power Technologies, короткая версия',
                'Короткая версия фильма об энергоснабжении объектов чемпионата мира '
                'по футболу 2018 года, 4 минуты 27 секунд.',
                '/media/pt-film-short.mp4', f'{IMG}/poster-short.jpg', 'PT4M27S'))

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
                 '"@type":"BreadcrumbList","itemListElement":['
                 '{"@type":"ListItem","position":1,"name":"Проекты",'
                 '"item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"Video Production",'
                 '"item":"https://hand-marketing.ru/videoproduction/"},'
                 '{"@type":"ListItem","position":3,"name":"История успеха Power Technologies",'
                 f'"item":"{URL}"}}]}}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Имиджевый ролик Power Technologies: энергоснабжение ЧМ-2018 | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: фильм «История успеха» Power Technologies о временном энергоснабжении объектов чемпионата мира по футболу 2018. Одиннадцать городов и двенадцать стадионов, 150 дизель-генераторов, 960 км кабелей, съёмка мобильными группами прямо во время чемпионата.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="История успеха Power Technologies | кейс Hand Marketing">
<meta property="og:description" content="Фильм о временном энергоснабжении объектов чемпионата мира по футболу 2018: одиннадцать городов, двенадцать стадионов, вещательный центр.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/poster-short.jpg">
<meta name="theme-color" content="#080B12">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def build():
    # порядок: масштаб проекта ведёт к фильму, фильм закрывает страницу
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма из rc.footer()
    body = (f'{rc.header()}<main class="pt" data-v="full">{hero()}{scale()}{objects()}'
            f'{craft()}{voices()}{story()}{film()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{LD}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'video', 'powertechnologies')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(build())
    # A2-файла быть не должно: деплой переименовывает его поверх нашей страницы
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
