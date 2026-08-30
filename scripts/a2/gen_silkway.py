#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/silkway/index.html: кейс «3D-визуализация маршрута
Silk Way Rally».

Материал: сам ролик (8:41, но всего 640×224), восемь фотографий с площадки
и два видео 1080p оттуда же. Год клиент просил не ставить, поэтому даты
этапов на странице идут без года: 16.07, 17.07 и так далее.

Идея страницы. Ролик тут не «красивая графика», а инструмент презентации:
организатор объявляет гонку, и объявить надо не настроение, а дистанцию.
Поэтому страница не пересказывает ролик, а показывает то, что в нём
зашито и на экране пролетает за секунды: десять этапов, у каждого лиазоны,
спецучасток, сервисный маршрут и состав покрытия. Все эти числа сняты
с ролика (scripts/silkway-assets.py, временная медиана) и сходятся:
у каждого этапа сумма частей равна его же TOTAL, а сумма лиазонов
совпадает с финальной сводкой, снятой на фотографии LED-экрана.

  • «Лента марафона» это первая механика: 5 947,93 км одной полосой,
    ширина блока равна длине этапа, внутри блока в тех же долях лежат
    лиазон, спецучасток и второй лиазон. Между Урумчи и Астраханью
    в ленте разрыв: там перелёт. Клик по этапу перематывает плеер
    в его сцену (тайм-коды найдены сканом ролика).
  • «Что под колёсами» это вторая механика и техника, которой на сайте
    ещё не было: 3 164,23 км спецучастков разложены по семи типам
    покрытия, и полоса не заливается плашками, а рисуется на canvas
    настоящей фактурой: гравий это отдельные камни, дюны это гребни,
    песчаные дороги это две колеи. Переключатель «Китай / Россия»
    показывает главное, что видно только в сумме: в Китае под колёсами
    песок и гравий, в России грунт, а последний этап до Москвы
    целиком грунтовый.
  • «Песочный стол» это третья механика: на площадке стоял лайтбокс,
    художник сыпал по нему песок, камера на журавле снимала сверху,
    и сигнал ложился в презентацию верхним слоем через альфа-канал.
    На странице лайтбокс живой: курсором можно разгребать песок
    (высота хранится полем, песок отваливает к краям штриха, как
    настоящий), а рядом «эфир» собирает то же самое поверх кадра
    маршрута, беря альфу из той же высоты. Это и есть показ того,
    как работал ключ, только вживую.

Шрифты: Advent Pro (узкий приборный гротеск под легенду трассы,
прописными) + Arsenal. Ни того, ни другого на сайте не было.
Палитра снята алгоритмом: цвет каждого этапа взят с его же плиты
рельефа в ролике, красный с печатного знака ралли.

Ассеты: mirror/images/silkway/ и mirror/videos/silkway-*.mp4
(scripts/silkway-assets.py). Ролик остаётся прежним: /media/silkway-3d.mp4.

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

IMG = '/images/silkway'
VID = '/videos'
FILM = '/media/silkway-3d.mp4'
URL = 'https://hand-marketing.ru/video/silkway/'
TITLE = ('3D-визуализация маршрута Silk Way Rally: рельеф трассы '
         'для презентации гонки | Hand Marketing')
DESCR = ('Кейс Hand Marketing: 3D-визуализация маршрута ралли-марафона '
         'Silk Way Rally от Сианя до Москвы. Десять этапов и 5 947,93 км '
         'собраны рельефом по координатам легенды трассы, ролик 8:41 '
         'работал на презентации гонки вместе с песочным столом.')

MAP = json.load(open(os.path.join(HERE, 'silkway_map.json'), encoding='utf-8'))
WHAT = MAP['photos']
WHAT.update(MAP['stills'])
SEEK = MAP['stages']                       # тайм-коды и цвет каждого этапа
RED = MAP['palette']['red']

# ─── десять этапов ────────────────────────────────────────────────────────
# Всё снято с карточек ролика временной медианой (см. ассет-скрипт) и
# перепроверено по фотографии контрольного монитора и финальной сводке
# на LED-экране. Проверка на сходимость: л1 + СУ + л2 = «итого» у всех
# десяти, сумма лиазонов совпадает со слайдом сводки до копейки.
# (№, дата, латиницей как в ролике, по-русски, лиазон 1, СУ, лиазон 2,
#  итого, сервисный маршрут, покрытие спецучастка)
STAGES = [
    (1, '16.07', 'XIAN / ZHONGWEI', 'Сиань → Чжунвэй',
     571.28, 101.61, 29.37, 702.26, 647,
     [('грунт', 15), ('гравий', 80), ('камни', 5)]),
    (2, '17.07', 'ZHONGWEI / ALASHAN YOUQI', 'Чжунвэй → Алашань-Юци',
     136.69, 238.09, 162.02, 536.80, 554,
     [('грунт', 45), ('песок', 35), ('песчаные дороги', 20)]),
    (3, '18.07', 'ALASHAN YOUQI / JIAYUGUAN', 'Алашань-Юци → Цзяюйгуань',
     77.89, 337.95, 181.89, 597.73, 370,
     [('грунт', 30), ('песок', 60), ('песчаные дороги', 10)]),
    (4, '19.07', 'JIAYUGUAN / HAMI', 'Цзяюйгуань → Хами',
     218.66, 451.52, 83.74, 753.92, 614,
     [('грунт', 30), ('гравий с песком', 70)]),
    (5, '20.07', 'HAMI / URUMQI', 'Хами → Урумчи',
     54.77, 405.40, 297.37, 757.54, 595,
     [('дюны', 10), ('гравий', 70), ('песчаные дороги', 20)]),
    (6, '23.07', 'ASTRAKHAN / ASTRAKHAN', 'Астрахань → Астрахань',
     25.67, 311.00, 26.11, 362.78, 0,
     [('грунт', 70), ('песчаные дороги', 30)]),
    (7, '24.07', 'ASTRAKHAN / ASTRAKHAN', 'Астрахань → Астрахань',
     25.83, 366.03, 28.33, 420.19, 0,
     [('грунт', 60), ('песчаные дороги', 40)]),
    (8, '25.07', 'ASTRAKHAN / VOLGOGRAD', 'Астрахань → Волгоград',
     28.82, 443.78, 80.11, 552.71, 460,
     [('грунт', 80), ('песчаные дороги', 20)]),
    (9, '26.07', 'VOLGOGRAD / LIPETSK', 'Волгоград → Липецк',
     76.13, 317.15, 373.50, 766.78, 650,
     [('грунт', 90), ('песчаные дороги', 10)]),
    (10, '27.07', 'LIPETSK / MOSCOW', 'Липецк → Москва',
     18.79, 191.70, 286.73, 497.22, 477,
     [('грунт', 100)]),
]
CHINA = 5                                  # первые пять этапов это Китай

# ─── как рисовать фактуру покрытия на canvas ──────────────────────────────
# (тип, подпись в легенде, базовый цвет, узор, как это называется в ролике)
SURFACES = [
    ('грунт', 'Грунт', '#8A7A4E', 'terra', 'TERRA'),
    ('гравий', 'Гравий', '#8E8577', 'gravel', 'GRAVEL'),
    ('гравий с песком', 'Гравий с песком', '#B09A6E', 'mix', 'GRAVEL AND SAND'),
    ('песок', 'Песок', '#D9BE84', 'sand', 'SAND'),
    ('песчаные дороги', 'Песчаные дороги', '#C4AD84', 'track', 'SANDY ROADS'),
    ('дюны', 'Дюны', '#E2CB96', 'dunes', 'DUNES'),
    ('камни', 'Камни', '#6F6A63', 'stones', 'STONES'),
]
ORDER = [s[0] for s in SURFACES]

# ─── что было на площадке ─────────────────────────────────────────────────
# Кадр показывается на странице РОВНО ОДИН раз: sand-table живёт в разделе
# про песочный стол, led-total-2 в итогах, остальные здесь. Дубль-снимок
# сводки (led-total) не берём совсем: это тот же экран секундой раньше.
RIG = [
    ('LED-экран во всю сцену',
     'Экран собран во всю ширину сцены, подиум ведущего сбоку. Плита рельефа '
     'шла на него целиком, чтобы маршрут читался и с задних столов.', 'hall'),
    ('Рельеф на экране',
     'Так этап выглядел в зале: плита с ниткой трассы, точками старта '
     'и финиша и карточкой километража в углу.', 'led-relief'),
    ('Зал к приёму',
     'Презентация шла на фуршете, у коктейльных столов. Отсюда требование '
     'к графике: крупно, контрастно, читаемо издалека.', 'hall-tables'),
    ('Контрольный монитор и микшер',
     'Режиссёрская точка сбоку от сцены: превью источников, перегон '
     'на большой экран, синхрон с ведущим.', 'monitor'),
    ('Техзона у песочного стола',
     'Рабочие места операторов вплотную к лайтбоксу: сигнал с камеры над '
     'столом шёл в микшер здесь же.', 'sand-crew'),
]

# кадры для лайтбокса это те же карточки раздела, отдельной сетки нет:
# вторая сетка означала бы те же снимки по второму разу
GALLERY = [slug for _t, _d, slug in RIG]


# ══ счёт ══════════════════════════════════════════════════════════════════
def num(v, dec=2):
    """Русский формат: 5 947,93 и 4 367."""
    s = f'{v:,.{dec}f}'.replace(',', ' ').replace('.', ',')
    return s.rstrip('0').rstrip(',') if dec and s.endswith(',00') else s


def totals(rows):
    lia = sum(r[4] + r[6] for r in rows)
    ss = sum(r[5] for r in rows)
    return {'lia': lia, 'ss': ss, 'all': lia + ss,
            'srv': sum(r[8] for r in rows), 'days': len(rows)}


ALL = totals(STAGES)
CN = totals(STAGES[:CHINA])
RU = totals(STAGES[CHINA:])


def by_surface(rows):
    """Километры спецучастков по типам покрытия: процент с карточки этапа
    умножается на длину его спецучастка."""
    acc = {k: 0.0 for k in ORDER}
    for r in rows:
        for name, pct in r[9]:
            acc[name] += r[5] * pct / 100.0
    return acc


GROUND = {'all': by_surface(STAGES), 'cn': by_surface(STAGES[:CHINA]),
          'ru': by_surface(STAGES[CHINA:])}


# ══ CSS ═══════════════════════════════════════════════════════════════════
CSS = """<style id="sw-css">
.sw{--ink:#15130F;--dim:#6B6459;--line:#D8D2C6;--paper:#F4F1EA;--sheet:#FFFDF8;
 --red:%RED%;--dark:#1A1713;--sand:#C9AC79;
 font-family:'Arsenal',Georgia,serif;color:var(--ink);background:var(--paper);
 font-size:17px;line-height:1.6;-webkit-text-size-adjust:100%}
.sw *,.sw *::before,.sw *::after{box-sizing:border-box}
.sw h1,.sw h2,.sw h3,.sw .sw-num,.sw .sw-lat{font-family:'Advent Pro','Arsenal',sans-serif;
 font-weight:700;letter-spacing:.02em}
.sw p{margin:0 0 1em}
.sw-in{max-width:1180px;margin:0 auto;padding:0 24px}
.sw-sec{padding:76px 0}
.sw-sec--dark{background:var(--dark);color:#EDE7DC}
.sw-sec--dark h2,.sw-sec--dark h3{color:#fff}
.sw-sec--sheet{background:var(--sheet)}
.sw h2{font-size:clamp(28px,4.4vw,46px);line-height:1.05;margin:0 0 14px;
 text-transform:uppercase}
.sw h3{font-size:clamp(19px,2.4vw,23px);line-height:1.15;margin:0 0 10px;
 text-transform:uppercase}
.sw-lead{font-size:clamp(17px,2vw,20px);color:var(--dim);max-width:56ch;margin:0 0 34px}
.sw-sec--dark .sw-lead{color:#B3AB9C}
.sw-kicker{font-family:'Advent Pro',sans-serif;font-weight:600;font-size:13px;
 letter-spacing:.22em;text-transform:uppercase;color:var(--red);margin:0 0 10px}
.sw-note{font-size:14px;line-height:1.55;color:var(--dim)}
.sw-sec--dark .sw-note{color:#9C9485}

/* ── шапка ─────────────────────────────────────────────────────────────── */
.sw-hero{position:relative;background:#120F0C;color:#fff;overflow:hidden}
.sw-hero__bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 opacity:.55}
.sw-hero__sh{position:absolute;inset:0;background:
 linear-gradient(180deg,rgba(18,15,12,.72),rgba(18,15,12,.35) 40%,rgba(18,15,12,.92))}
.sw-hero__in{position:relative;max-width:1180px;margin:0 auto;padding:110px 24px 54px}
.sw-hero h1{font-size:clamp(32px,6.2vw,72px);line-height:.98;margin:0 0 18px;
 text-transform:uppercase;max-width:16ch}
.sw-hero__sub{font-size:clamp(16px,2vw,20px);color:#D7CFC1;max-width:56ch;margin:0 0 40px}
.sw-hero__k{display:flex;flex-wrap:wrap;gap:10px 40px;border-top:1px solid rgba(255,255,255,.2);
 padding-top:22px}
.sw-hero__k div{min-width:118px}
.sw-hero__k b{display:block;font-family:'Advent Pro',sans-serif;font-weight:700;
 font-size:clamp(22px,3.4vw,34px);line-height:1.05}
.sw-hero__k span{font-size:13px;color:#ADA495;letter-spacing:.04em}

/* ── бриф ──────────────────────────────────────────────────────────────── */
.sw-brief{display:grid;grid-template-columns:repeat(3,1fr);gap:34px}
.sw-brief h3{color:var(--red)}

/* ── лента марафона ────────────────────────────────────────────────────── */
.sw-band{overflow-x:auto;overflow-y:hidden;padding-bottom:10px;
 -webkit-overflow-scrolling:touch}
.sw-band__in{display:flex;align-items:stretch;gap:0;min-width:860px}
.sw-st{position:relative;border:0;padding:0;background:none;cursor:pointer;
 text-align:left;font:inherit;color:inherit;display:block}
.sw-st__bar>span{flex:none;display:block}
.sw-st__bar{height:64px;display:flex;border-radius:2px;overflow:hidden;
 outline:2px solid transparent;transition:outline-color .15s,transform .15s}
.sw-st:hover .sw-st__bar,.sw-st.on .sw-st__bar{outline-color:var(--red)}
.sw-st.on .sw-st__bar{transform:translateY(-4px)}
.sw-st__l{background-image:repeating-linear-gradient(135deg,#CFC8BA 0 4px,#E2DCD0 4px 8px)}
.sw-st__s{position:relative}
.sw-st__n{font-family:'Advent Pro',sans-serif;font-weight:700;font-size:13px;
 color:var(--dim);padding:8px 0 0;letter-spacing:.08em}
.sw-st.on .sw-st__n{color:var(--red)}
.sw-st__d{font-size:12px;color:var(--dim);letter-spacing:.04em}
.sw-gap{flex:0 0 46px;position:relative;margin:0 2px}
.sw-gap::before{content:"";position:absolute;left:0;right:0;top:31px;
 border-top:2px dashed #BEB6A6}
.sw-gap__t{position:absolute;top:-16px;left:50%;transform:translateX(-50%);
 white-space:nowrap;font-family:'Advent Pro',sans-serif;font-size:11px;
 letter-spacing:.14em;color:var(--dim);text-transform:uppercase}
.sw-legend{display:flex;flex-wrap:wrap;gap:8px 26px;margin:22px 0 0;font-size:13px;
 color:var(--dim)}
.sw-legend i{display:inline-block;width:22px;height:10px;margin-right:8px;
 vertical-align:middle;border-radius:2px}

/* выбранный этап + плеер */
.sw-play{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);
 gap:30px;margin-top:40px;align-items:start}
.sw-screen{background:#0E0C0A;border-radius:4px;padding:12px;
 box-shadow:0 18px 46px rgba(0,0,0,.22)}
.sw-screen video{width:100%;display:block;border-radius:2px;background:#000}
.sw-screen__b{display:flex;justify-content:space-between;align-items:center;
 gap:12px;padding:10px 2px 2px;font-size:12px;color:#8C8578;
 font-family:'Advent Pro',sans-serif;letter-spacing:.08em;text-transform:uppercase}
.sw-card{border:1px solid var(--line);border-top:3px solid var(--line);
 background:var(--sheet);padding:24px 26px 20px;border-radius:3px}
.sw-card__t{font-family:'Advent Pro',sans-serif;font-weight:700;font-size:12px;
 letter-spacing:.2em;text-transform:uppercase;color:var(--dim)}
.sw-card h3{margin:6px 0 2px;font-size:26px}
.sw-card__lat{font-family:'Advent Pro',sans-serif;font-size:13px;letter-spacing:.16em;
 color:var(--dim);text-transform:uppercase;margin-bottom:16px}
.sw-rows{border-top:1px solid var(--line)}
.sw-rows div{display:flex;justify-content:space-between;gap:16px;
 border-bottom:1px solid var(--line);padding:7px 0;font-size:15px}
.sw-rows b{font-family:'Advent Pro',sans-serif;font-weight:700;white-space:nowrap}
.sw-rows .big{font-size:17px}
.sw-mix{display:flex;height:12px;border-radius:2px;overflow:hidden;margin:16px 0 8px}
.sw-mix i{display:block;flex:none}
.sw-mixl{font-size:13px;color:var(--dim)}
.sw-seek{margin-top:16px;font:inherit;font-family:'Advent Pro',sans-serif;
 font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:13px;
 background:var(--red);color:#fff;border:0;border-radius:2px;padding:11px 18px;
 cursor:pointer}
.sw-seek:hover{filter:brightness(1.1)}

/* ── таблица этапов ────────────────────────────────────────────────────── */
.sw-tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.sw-tbl{border-collapse:collapse;width:100%;min-width:760px;font-size:14px}
.sw-tbl th,.sw-tbl td{text-align:right;padding:9px 10px;border-bottom:1px solid var(--line);
 white-space:nowrap}
.sw-tbl th{font-family:'Advent Pro',sans-serif;font-weight:700;font-size:12px;
 letter-spacing:.1em;text-transform:uppercase;color:var(--dim);
 border-bottom:1px solid #B9B1A2}
.sw-tbl td:first-child,.sw-tbl th:first-child,
.sw-tbl td:nth-child(2),.sw-tbl th:nth-child(2){text-align:left}
.sw-tbl td:nth-child(2){white-space:normal;min-width:190px}
.sw-tbl tfoot td{font-family:'Advent Pro',sans-serif;font-weight:700;
 border-top:1px solid #B9B1A2;border-bottom:0;padding-top:12px}
.sw-tbl .num{font-family:'Advent Pro',sans-serif;font-weight:600}

/* ── что под колёсами ──────────────────────────────────────────────────── */
.sw-seg{display:inline-flex;border:1px solid rgba(255,255,255,.28);border-radius:2px;
 overflow:hidden;margin-bottom:26px}
.sw-seg button{font:inherit;font-family:'Advent Pro',sans-serif;font-weight:700;
 letter-spacing:.1em;text-transform:uppercase;font-size:13px;background:none;
 color:#CFC7B8;border:0;padding:10px 20px;cursor:pointer}
.sw-seg button+button{border-left:1px solid rgba(255,255,255,.28)}
.sw-seg button.on{background:var(--red);color:#fff}
.sw-gc{width:100%;height:170px;display:block;border-radius:3px;background:#241F19}
.sw-gl{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
 gap:14px 26px;margin-top:26px}
.sw-gl__i{display:flex;align-items:baseline;gap:10px;font-size:15px}
.sw-gl__sw{flex:0 0 14px;height:14px;border-radius:2px;transform:translateY(2px)}
.sw-gl__km{margin-left:auto;font-family:'Advent Pro',sans-serif;font-weight:700;
 white-space:nowrap}
.sw-gl__i.off{opacity:.32}

/* ── итоги ─────────────────────────────────────────────────────────────── */
.sw-tot{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:34px;
 align-items:center}
.sw-tot figure{margin:0}
.sw-tot img{width:100%;display:block;border-radius:3px}
.sw-tg{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--line);
 border:1px solid var(--line);border-radius:3px;overflow:hidden}
.sw-tg div{background:var(--sheet);padding:18px 18px 16px}
.sw-tg b{display:block;font-family:'Advent Pro',sans-serif;font-weight:700;
 font-size:clamp(20px,2.8vw,30px);line-height:1.05}
.sw-tg span{font-size:13px;color:var(--dim)}
.sw-tg .wide{grid-column:1/-1}

/* ── песочный стол ─────────────────────────────────────────────────────── */
.sw-sand{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:30px;
 align-items:start}
.sw-box{border-radius:4px;overflow:hidden;background:#0E0C0A;padding:10px;
 box-shadow:0 18px 46px rgba(0,0,0,.3)}
.sw-box canvas{width:100%;display:block;border-radius:2px;touch-action:none;
 cursor:crosshair}
.sw-box__b{display:flex;flex-wrap:wrap;gap:10px;align-items:center;
 padding:10px 2px 2px}
.sw-box__b span{font-family:'Advent Pro',sans-serif;font-size:12px;letter-spacing:.1em;
 text-transform:uppercase;color:#8C8578}
.sw-btn{font:inherit;font-family:'Advent Pro',sans-serif;font-weight:700;font-size:12px;
 letter-spacing:.1em;text-transform:uppercase;background:none;color:#CFC7B8;
 border:1px solid rgba(255,255,255,.3);border-radius:2px;padding:7px 14px;cursor:pointer}
.sw-btn:hover{background:rgba(255,255,255,.1)}
.sw-btn.on{background:var(--red);color:#fff;border-color:var(--red)}
.sw-air{margin-top:18px}
.sw-air canvas{cursor:default}
.sw-vid{width:100%;display:block;border-radius:3px;margin-top:18px}

/* ── как собирали ──────────────────────────────────────────────────────── */
.sw-rig{display:grid;grid-template-columns:repeat(3,1fr);gap:26px}
.sw-rig figure{margin:0}
.sw-rig img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;
 border-radius:3px;margin-bottom:14px}
.sw-rig figure>button{margin-bottom:14px}
.sw-shot{border:0;padding:0;background:none;cursor:zoom-in;display:block;width:100%}
.sw-shot img{transition:opacity .15s}
.sw-shot:hover img{opacity:.86}
.sw-lb{position:fixed;inset:0;z-index:9000;background:rgba(12,10,8,.94);
 display:none;align-items:center;justify-content:center;padding:26px}
.sw-lb.on{display:flex}
.sw-lb img{max-width:100%;max-height:78vh;display:block;border-radius:3px}
.sw-lb__c{max-width:1000px}
.sw-lb__cap{color:#CFC7B8;font-size:14px;margin-top:12px;max-width:70ch}
.sw-lb__x,.sw-lb__p,.sw-lb__n{position:absolute;top:18px;right:20px;background:none;
 border:0;color:#fff;font-size:30px;line-height:1;cursor:pointer;padding:6px 12px}
.sw-lb__p{top:50%;left:10px;right:auto;transform:translateY(-50%)}
.sw-lb__n{top:50%;right:10px;transform:translateY(-50%)}

/* ── планшет ───────────────────────────────────────────────────────────── */
@media (max-width:1000px){
 .sw-play,.sw-sand,.sw-tot{grid-template-columns:1fr}
 .sw-brief{grid-template-columns:1fr 1fr}
 .sw-rig{grid-template-columns:repeat(2,1fr)}
 .sw-sec{padding:60px 0}
}
/* ── телефон ───────────────────────────────────────────────────────────── */
@media (max-width:640px){
 .sw{font-size:16px}
 .sw-in{padding:0 18px}
 .sw-sec{padding:48px 0}
 .sw-hero__in{padding:76px 18px 40px}
 .sw-brief,.sw-rig{grid-template-columns:1fr}
 .sw-tg{grid-template-columns:1fr}
 .sw-hero__k{gap:14px 26px}
 .sw-hero__k div{min-width:94px}
 .sw-card{padding:20px}
 .sw-gc{height:132px}
}
/* ── телефон лёжа: шапка не должна съедать весь экран ──────────────────── */
@media (max-height:520px) and (orientation:landscape){
 .sw-hero__in{padding:62px 24px 30px}
 .sw-hero h1{font-size:30px}
 .sw-hero__sub{margin-bottom:20px}
}
</style>"""


# ══ разметка ══════════════════════════════════════════════════════════════
def hero():
    k = [(num(ALL['all']), 'километров марафона'),
         ('10', 'этапов в двух странах'),
         (num(ALL['ss']), 'км спецучастков'),
         ('8:41', 'хронометраж ролика')]
    kk = ''.join(f'<div><b>{v}</b><span>{t}</span></div>' for v, t in k)
    return (
      '<header class="sw-hero">'
      f'<video class="sw-hero__bg" src="{VID}/silkway-hall.mp4" '
      f'poster="{IMG}/silkway-hall-poster.jpg" autoplay muted loop playsinline '
      'preload="metadata" aria-hidden="true"></video>'
      '<div class="sw-hero__sh"></div>'
      '<div class="sw-hero__in">'
      '<p class="sw-kicker">Silk Way Rally · Video Production &amp; Creative</p>'
      '<h1>3D-визуализация маршрута ралли</h1>'
      '<p class="sw-hero__sub">Организатору нужно было объявить будущую гонку '
      'так, чтобы дистанция читалась с первого взгляда. Мы собрали весь '
      'маршрут рельефом по координатам легенды трассы и отдали его '
      'в презентацию вместе с песочным столом и технической поддержкой '
      'площадки.</p>'
      f'<div class="sw-hero__k">{kk}</div>'
      '</div></header>')


def brief():
    return (
      '<section class="sw-sec"><div class="sw-in">'
      '<div class="sw-brief">'
      '<div><h3>Задача</h3><p>Показать маршрут предстоящего ралли-марафона '
      'с настоящим ландшафтом, а не условной линией на карте. И отработать '
      'презентацию технически: экран, источники, живая графика.</p></div>'
      '<div><h3>Решение</h3><p>Рельеф каждого этапа построен по координатам '
      'легенды трассы, которые мы вносили в Google Earth. Поверх рельефа '
      'легли нитка трассы, точки старта и финиша и карточка этапа '
      'с километражом и составом покрытия.</p></div>'
      '<div><h3>Результат</h3><p>Ролик на 8:41 отработал в презентации гонки: '
      'по нему шёл рассказ о дистанции. Параллельно на площадке работал '
      'песочный стол, картинка с него подавалась в общую презентацию '
      'верхним слоем через альфа-канал.</p></div>'
      '</div></div></section>')


def band():
    """Лента: ширина блока равна длине этапа, внутри доли лиазонов и СУ."""
    out = []
    for i, r in enumerate(STAGES):
        n, date, lat, ru, l1, ss, l2, tot, srv, mix = r
        col = SEEK[i]['color']
        parts = (f'<span class="sw-st__l" style="width:{l1/tot*100:.3f}%"></span>'
                 f'<span class="sw-st__s" style="width:{ss/tot*100:.3f}%;'
                 f'background:{col}"></span>'
                 f'<span class="sw-st__l" style="width:{l2/tot*100:.3f}%"></span>')
        out.append(
          f'<button class="sw-st" data-i="{i}" style="flex:{tot:.2f} 1 0" '
          f'aria-label="Этап {n}, {ru}, {num(tot)} км">'
          f'<span class="sw-st__bar">{parts}</span>'
          f'<span class="sw-st__n">{n:02d}</span> '
          f'<span class="sw-st__d">{date}</span></button>')
        if n == CHINA:
            out.append('<div class="sw-gap" aria-hidden="true">'
                       '<span class="sw-gap__t">перелёт</span></div>')
    legend = (
      '<div class="sw-legend">'
      '<span><i style="background:repeating-linear-gradient(135deg,#CFC8BA 0 4px,'
      '#E2DCD0 4px 8px)"></i>лиазон, дорога общего пользования</span>'
      '<span><i style="background:linear-gradient(90deg,#6A3F18,#77643F)"></i>'
      'спецучасток, цвет снят с плиты рельефа этого этапа в ролике</span>'
      '<span>ширина блока равна длине этапа</span></div>')
    return (f'<div class="sw-band"><div class="sw-band__in">{"".join(out)}</div></div>'
            f'{legend}')


def player():
    return (
      '<div class="sw-play">'
      '<div><div class="sw-screen">'
      f'<video id="swfilm" src="{FILM}" poster="{IMG}/stage-01.jpg" controls '
      'preload="metadata" playsinline></video>'
      '<div class="sw-screen__b"><span>3D Silk Way · 8:41</span>'
      '<span id="swnow">этап 01</span></div></div>'
      '<p class="sw-note" style="margin-top:14px">Ролик отдан так, как он '
      'существует: это единственная сохранившаяся копия, 640×224. '
      'Числа на карточках этапов мы сняли с него покадровой медианой '
      'и сверили с фотографией контрольного монитора на площадке.</p></div>'
      '<div class="sw-card" id="swcard"></div>'
      '</div>')


def route():
    return (
      '<section class="sw-sec sw-sec--sheet"><div class="sw-in">'
      '<p class="sw-kicker">Дистанция</p>'
      '<h2>Марафон одной лентой</h2>'
      f'<p class="sw-lead">{num(ALL["all"])} км за десять дней гонки. '
      'Ширина каждого блока равна длине этапа, штриховка это лиазоны, '
      'сплошная заливка это спецучасток. Нажмите на этап, чтобы плеер '
      'перемотал ролик в его сцену.</p>'
      f'{band()}{player()}'
      '</div></section>')


def table():
    head = ('<tr><th>Этап</th><th>Маршрут</th><th>Лиазон 1</th><th>СУ</th>'
            '<th>Лиазон 2</th><th>Итого</th><th>Сервис</th><th>Покрытие СУ</th></tr>')
    rows = []
    for r in STAGES:
        n, date, lat, ru, l1, ss, l2, tot, srv, mix = r
        m = ', '.join(f'{k} {p}%' for k, p in mix)
        rows.append(
          f'<tr><td><b class="num">{n:02d}</b> {date}</td><td>{ru}</td>'
          f'<td class="num">{num(l1)}</td><td class="num">{num(ss)}</td>'
          f'<td class="num">{num(l2)}</td><td class="num">{num(tot)}</td>'
          f'<td class="num">{num(srv, 0)}</td><td>{m}</td></tr>')
    foot = (f'<tr><td colspan="2">Всего за десять этапов</td>'
            f'<td colspan="2" class="num">{num(ALL["lia"])} лиазонов</td>'
            f'<td class="num">{num(ALL["ss"])} СУ</td>'
            f'<td class="num">{num(ALL["all"])}</td>'
            f'<td class="num">{num(ALL["srv"], 0)}</td><td></td></tr>')
    return (
      '<section class="sw-sec"><div class="sw-in">'
      '<p class="sw-kicker">Все десять карточек</p>'
      '<h2>Что было зашито в ролик</h2>'
      '<p class="sw-lead">На экране карточка этапа живёт несколько секунд. '
      'Здесь она целиком, все десять. Километры в таблице сходятся: '
      'у каждого этапа сумма лиазонов и спецучастка равна его же итогу.</p>'
      f'<div class="sw-tw"><table class="sw-tbl"><thead>{head}</thead>'
      f'<tbody>{"".join(rows)}</tbody><tfoot>{foot}</tfoot></table></div>'
      '<p class="sw-note" style="margin-top:18px">В легенде трассы это '
      'называется LIAISON (перегон по дорогам общего пользования), '
      'SS, special stage (спецучасток на время) и SERVICE ROUTE '
      '(маршрут технички). Покрытие подписано словами TERRA, GRAVEL, SAND, '
      'SANDY ROADS, DUNES и STONES.</p>'
      '</div></section>')


def ground():
    seg = ('<div class="sw-seg" role="group" aria-label="Часть марафона">'
           '<button data-g="all" class="on">Весь марафон</button>'
           '<button data-g="cn">Китай</button>'
           '<button data-g="ru">Россия</button></div>')
    return (
      '<section class="sw-sec sw-sec--dark"><div class="sw-in">'
      '<p class="sw-kicker">Покрытие</p>'
      '<h2>Что под колёсами</h2>'
      f'<p class="sw-lead">У каждого этапа в карточке записан состав покрытия '
      f'спецучастка. Если свести все десять, получится {num(ALL["ss"])} км '
      'на время, разложенные по семи типам грунта. Полоса ниже нарисована '
      'в реальных долях, фактура у каждого типа своя.</p>'
      f'{seg}<canvas class="sw-gc" id="swground" '
      'aria-label="Полоса покрытия спецучастков"></canvas>'
      '<div class="sw-gl" id="swglegend"></div>'
      f'<p class="sw-note" style="margin-top:24px">В Китае под колёсами '
      f'песок, гравий и дюны, грунта всего '
      f'{GROUND["cn"]["грунт"] / CN["ss"] * 100:.0f}%. В России наоборот: '
      f'{GROUND["ru"]["грунт"] / RU["ss"] * 100:.0f}% грунта и ни одного '
      'километра песка, а последний этап до Москвы грунтовый целиком.</p>'
      '</div></section>')


def tot():
    g = [(num(CN['all']), 'км в Китае, пять этапов'),
         (num(RU['all']), 'км в России, пять этапов'),
         (num(ALL['lia']), 'км лиазонов'),
         (num(ALL['ss']), 'км спецучастков'),
         (num(ALL['srv'], 0), 'км маршрутов технички'),
         (str(len(SURFACES)), 'типов покрытия на спецучастках')]
    cells = ''.join(f'<div><b>{v}</b><span>{t}</span></div>' for v, t in g)
    cells += (f'<div class="wide"><b>{num(ALL["all"])}</b>'
              '<span>км всего, от Сианя до Москвы</span></div>')
    return (
      '<section class="sw-sec sw-sec--sheet"><div class="sw-in">'
      '<p class="sw-kicker">Финал ролика</p>'
      '<h2>Две плиты и общий метраж</h2>'
      '<p class="sw-lead">Ролик заканчивается сводкой: китайская и российская '
      'части встают рядом двумя плитами, между ними самолёт перегона. '
      'Так дистанция читается целиком, одним кадром.</p>'
      '<div class="sw-tot">'
      f'<figure><img src="{IMG}/led-total-2-m.jpg" loading="lazy" '
      f'alt="{WHAT["led-total-2"]}" width="1100" height="825">'
      '<figcaption class="sw-note" style="margin-top:10px">Сводка на '
      'LED-экране зала.</figcaption></figure>'
      f'<div class="sw-tg">{cells}</div>'
      '</div></div></section>')


def sand():
    return (
      '<section class="sw-sec sw-sec--dark"><div class="sw-in">'
      '<p class="sw-kicker">Техническая поддержка</p>'
      '<h2>Песочный стол и верхний слой</h2>'
      '<p class="sw-lead">Кроме ролика на площадке работал стол для рисования '
      'песком: лайтбокс снизу, песок сверху, камера на журавле над столом. '
      'Сигнал с камеры уходил в презентацию верхним слоем через альфа-канал: '
      'светящийся лайтбокс становился прозрачным, песок оставался.</p>'
      '<div class="sw-sand"><div>'
      '<div class="sw-box"><canvas id="swsand" aria-label="Стол с песком, '
      'можно рисовать курсором"></canvas>'
      '<div class="sw-box__b"><span>стол: рисуйте песком по лайтбоксу</span>'
      '<button class="sw-btn on" id="swpour" type="button" aria-pressed="true">'
      'Сыпать</button>'
      '<button class="sw-btn" id="swdig" type="button" aria-pressed="false">'
      'Разгребать</button>'
      '<button class="sw-btn" id="swclear" type="button">Смести</button>'
      '</div></div>'
      '<div class="sw-box sw-air"><canvas id="swair" aria-label="Тот же песок '
      'поверх кадра маршрута"></canvas>'
      '<div class="sw-box__b"><span>эфир: тот же песок поверх маршрута</span>'
      '<button class="sw-btn on" id="swkey" type="button" aria-pressed="true">'
      'Альфа включена</button></div></div>'
      '</div>'
      f'<div><figure style="margin:0 0 22px">'
      f'<img src="{IMG}/sand-table-s.jpg" loading="lazy" '
      f'alt="{WHAT["sand-table"]}" width="700" height="525" '
      'style="width:100%;display:block;border-radius:3px">'
      '<figcaption class="sw-note" style="margin-top:10px">Лайтбокс, песок '
      'и камера на журавле над столом.</figcaption></figure>'
      '<h3>Как это работало</h3>'
      '<p>Яркость кадра с камеры и есть маска прозрачности: там, где лайтбокс '
      'светит в объектив, слой прозрачен, там, где лежит песок, он плотный. '
      'Микшеру остаётся положить эту картинку поверх слайда, и рисунок '
      'появляется прямо на маршруте, без рамки и подложки.</p>'
      '<p>Слева тот же принцип вживую. Холст хранит высоту песка в каждой '
      'точке: курсор сыплет его или разгребает к краям штриха, как ведёт '
      'себя настоящий песок под пальцем. Нижний холст берёт из этой же '
      'высоты альфу и кладёт песок поверх кадра рельефа, ничего больше '
      'не делая. Кнопка «Альфа» показывает, что ушло бы в эфир без ключа: '
      'вместе с рисунком лёг бы весь стол.</p>'
      f'<video class="sw-vid" src="{VID}/silkway-sand.mp4" '
      f'poster="{IMG}/silkway-sand-poster.jpg" muted loop playsinline '
      'controls preload="none"></video>'
      '<p class="sw-note" style="margin-top:10px">Художник за столом '
      'во время презентации.</p>'
      '</div></div></div></section>')


def rig():
    cards = ''.join(
      f'<figure><button class="sw-shot" data-i="{i}" aria-label="Открыть кадр">'
      f'<img src="{IMG}/{slug}-s.jpg" loading="lazy" alt="{WHAT[slug]}" '
      f'width="700" height="525"></button><h3>{t}</h3><p>{d}</p></figure>'
      for i, (t, d, slug) in enumerate(RIG))
    return (
      '<section class="sw-sec"><div class="sw-in">'
      '<p class="sw-kicker">Площадка</p>'
      '<h2>Что стояло в зале</h2>'
      '<p class="sw-lead">Мы не только отдали файл: на презентации работала '
      'наша техническая группа, от подачи графики на экран до живого '
      'песочного стола. Нажмите на кадр, чтобы открыть его крупно.</p>'
      f'<div class="sw-rig">{cards}</div>'
      '</div></section>'
      '<div class="sw-lb" id="swlb" role="dialog" aria-modal="true">'
      '<button class="sw-lb__x" aria-label="Закрыть">&times;</button>'
      '<button class="sw-lb__p" aria-label="Предыдущий">&#8249;</button>'
      '<button class="sw-lb__n" aria-label="Следующий">&#8250;</button>'
      '<div class="sw-lb__c"><img src="" alt=""><div class="sw-lb__cap"></div></div>'
      '</div>')


# ══ JS ════════════════════════════════════════════════════════════════════
PAGE_JS = """<script>(function(){
var ST=%STAGES%, SEEK=%SEEK%, SURF=%SURF%, GROUND=%GROUND%, IMG='%IMG%';

/* ── лента и карточка этапа ─────────────────────────────────────────────── */
var film=document.getElementById('swfilm'), card=document.getElementById('swcard'),
    now=document.getElementById('swnow'),
    btns=[].slice.call(document.querySelectorAll('.sw-st')), cur=-1;
function fmt(v,d){var s=v.toFixed(d===undefined?2:d);
  s=s.replace('.',',').replace(/\\B(?=(\\d{3})+(?!\\d))/,' ');
  if(/,00$/.test(s))s=s.slice(0,-3);return s;}
function draw(i){
  var s=ST[i], c=SEEK[i].color;
  var rows=[['Лиазон 1',fmt(s.l1)+' км',0],['Спецучасток',fmt(s.ss)+' км',1],
            ['Лиазон 2',fmt(s.l2)+' км',0],['Итого за день',fmt(s.tot)+' км',1],
            ['Маршрут технички',fmt(s.srv,0)+' км',0]];
  var html='<div class="sw-card__t">Этап '+(i<9?'0':'')+(i+1)+' · '+s.date+'</div>'+
    '<h3>'+s.ru+'</h3><div class="sw-card__lat">'+s.lat+'</div><div class="sw-rows">';
  rows.forEach(function(r){html+='<div'+(r[2]?' class="big"':'')+'><span>'+r[0]+
    '</span><b>'+r[1]+'</b></div>';});
  html+='</div><div class="sw-mix">';
  s.mix.forEach(function(m){var f=SURF[m[0]];
    html+='<i style="width:'+m[1]+'%;background:'+f.color+'"></i>';});
  html+='</div><div class="sw-mixl">Покрытие спецучастка: '+
    s.mix.map(function(m){return m[0]+' '+m[1]+'%';}).join(', ')+'</div>'+
    '<button class="sw-seek" type="button">Смотреть этот этап</button>';
  card.innerHTML=html;
  card.querySelector('.sw-seek').addEventListener('click',function(){
    if(!film)return;
    try{film.currentTime=SEEK[i].seek;}catch(e){}
    film.play().catch(function(){});
    film.scrollIntoView({block:'center',behavior:'smooth'});
  });
  card.style.borderTopColor=c;
}
function pick(i){
  if(i===cur)return; cur=i;
  btns.forEach(function(b,j){b.classList.toggle('on',j===i);});
  draw(i);
  if(now)now.textContent='этап '+(i<9?'0':'')+(i+1);
  /* постер плеера идёт за выбором, пока ролик не запущен */
  if(film&&film.paused&&!film.currentTime)
    film.poster=IMG+'/stage-'+(i<9?'0':'')+(i+1)+'.jpg';
}
btns.forEach(function(b){b.addEventListener('click',function(){
  var i=+b.getAttribute('data-i'); pick(i);
  try{film.currentTime=SEEK[i].seek;}catch(e){}
});});
pick(0);
/* плеер сам подсвечивает этап, в котором сейчас находится */
if(film)film.addEventListener('timeupdate',function(){
  var t=film.currentTime,k=-1;
  for(var i=0;i<SEEK.length;i++){if(t>=SEEK[i].seek-6)k=i;}
  if(k>=0&&k!==cur)pick(k);
});

/* ── что под колёсами: фактура покрытия на canvas ───────────────────────── */
var gc=document.getElementById('swground'), gl=document.getElementById('swglegend'),
    gset='all';
/* свой генератор псевдослучайных: узор должен быть одинаковым при каждой
   перерисовке, иначе полоса «кипит» при ресайзе */
function rnd(seed){var s=seed>>>0;return function(){
  s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function texture(ctx,x,w,h,kind,color){
  ctx.save();ctx.beginPath();ctx.rect(x,0,w,h);ctx.clip();
  ctx.fillStyle=color;ctx.fillRect(x,0,w,h);
  var R=rnd(Math.round(x*7.3)+kind.length*991), i,n,px,py,r;
  ctx.globalAlpha=.5;
  if(kind==='sand'||kind==='track'||kind==='mix'){
    n=Math.round(w*h/9);
    for(i=0;i<n;i++){px=x+R()*w;py=R()*h;
      ctx.fillStyle=R()>.5?'rgba(255,252,242,.75)':'rgba(88,64,30,.55)';
      ctx.fillRect(px,py,R()>.75?2:1,1);}
  }
  if(kind==='sand'){          /* мелкая рябь, чтобы песок не читался плашкой */
    ctx.globalAlpha=.22;ctx.lineWidth=1.2;ctx.strokeStyle='rgba(120,92,48,.9)';
    for(i=0;i<Math.round(h/9);i++){var ry=i*9+R()*4;ctx.beginPath();
      ctx.moveTo(x,ry);
      for(var rx=0;rx<=w;rx+=8)ctx.lineTo(x+rx,ry+Math.sin((rx+i*37)/23)*1.8);
      ctx.stroke();}
  }
  if(kind==='terra'){
    /* утоптанный грунт: комья двух тонов вплотную, поверх сетка трещин.
       Мелкая точка на ретине усредняется в плашку, поэтому комья не пиксели,
       а эллипсы, и их много. */
    n=Math.round(w*h/22);
    for(i=0;i<n;i++){px=x+R()*w;py=R()*h;r=.8+R()*1.9;
      ctx.globalAlpha=.5;
      ctx.fillStyle=R()>.45?'rgba(58,46,22,.85)':'rgba(232,220,186,.8)';
      ctx.beginPath();ctx.ellipse(px,py,r,r*.75,R()*3.14,0,6.284);ctx.fill();}
    /* короткие трещины утоптанного грунта: концы штриха считаем от его же
       начала, иначе линия растягивается на всю ширину сегмента */
    ctx.globalAlpha=.42;ctx.strokeStyle='rgba(44,36,18,.95)';ctx.lineWidth=1.1;
    for(i=0;i<Math.round(w*h/260);i++){
      var sx=x+R()*w, sy=R()*h, a0=R()*6.284, ln=6+R()*11;
      ctx.beginPath();ctx.moveTo(sx,sy);
      ctx.lineTo(sx+Math.cos(a0)*ln,sy+Math.sin(a0)*ln*.45);ctx.stroke();}
  }
  if(kind==='gravel'||kind==='mix'||kind==='stones'){
    var big=kind==='stones'?4.2:(kind==='mix'?1.9:2.4);
    n=Math.round(w*h/(kind==='stones'?150:64));
    for(i=0;i<n;i++){px=x+R()*w;py=R()*h;r=1+R()*big;
      ctx.globalAlpha=.75;
      ctx.fillStyle=R()>.5?'rgba(246,240,228,.85)':'rgba(52,46,38,.75)';
      ctx.beginPath();
      ctx.ellipse(px,py,r,r*(.6+R()*.5),R()*3.14,0,6.284);ctx.fill();}
  }
  if(kind==='dunes'){
    ctx.globalAlpha=.6;ctx.lineWidth=1.4;
    for(i=0;i<Math.round(h/7);i++){
      var y0=i*7+R()*3;ctx.beginPath();ctx.moveTo(x,y0);
      for(var xx=0;xx<=w;xx+=6)ctx.lineTo(x+xx,y0+Math.sin((xx+i*23)/17)*3.2);
      ctx.strokeStyle=i%2?'rgba(255,250,235,.75)':'rgba(120,92,48,.6)';ctx.stroke();}
  }
  if(kind==='track'){
    ctx.globalAlpha=.5;ctx.fillStyle='rgba(120,96,56,.55)';
    ctx.fillRect(x,h*0.34,w,h*0.07);ctx.fillRect(x,h*0.60,w,h*0.07);
  }
  ctx.restore();ctx.globalAlpha=1;
}
function drawGround(){
  if(!gc)return;
  var css=gc.getBoundingClientRect(), dpr=Math.min(2,window.devicePixelRatio||1);
  var w=Math.max(1,Math.round(css.width)), h=Math.max(1,Math.round(css.height));
  gc.width=w*dpr; gc.height=h*dpr;
  var ctx=gc.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,w,h);
  var data=GROUND[gset], tot=0, k;
  for(k in data)tot+=data[k];
  var x=0;
  SURF.order.forEach(function(name){
    var km=data[name]||0; if(km<=0)return;
    var seg=km/tot*w;
    texture(ctx,x,seg,h,SURF[name].kind,SURF[name].color);
    if(seg>2){ctx.fillStyle='rgba(26,23,19,.55)';ctx.fillRect(x,0,1,h);}
    x+=seg;
  });
}
function drawLegend(){
  if(!gl)return;
  var data=GROUND[gset], html='';
  SURF.order.forEach(function(name){
    var km=data[name]||0;
    html+='<div class="sw-gl__i'+(km<=0?' off':'')+'">'+
      '<i class="sw-gl__sw" style="background:'+SURF[name].color+'"></i>'+
      '<span>'+SURF[name].label+'</span>'+
      '<b class="sw-gl__km">'+(km>0?fmt(km)+' км':'нет')+'</b></div>';
  });
  gl.innerHTML=html;
}
[].slice.call(document.querySelectorAll('.sw-seg button')).forEach(function(b){
  b.addEventListener('click',function(){
    gset=b.getAttribute('data-g');
    [].slice.call(document.querySelectorAll('.sw-seg button')).forEach(function(o){
      o.classList.toggle('on',o===b);});
    drawGround();drawLegend();
  });
});
drawLegend();

/* ── песочный стол ──────────────────────────────────────────────────────── */
var sc=document.getElementById('swsand'), ac=document.getElementById('swair'),
    GW=220, GH=77, H=new Float32Array(GW*GH), base=null, air=new Image(), airOk=false,
    keyOn=true, mode='pour';
air.onload=function(){airOk=true;paintAir();};
air.src=IMG+'/stage-05.jpg';
/* Стол начинается почти чистым: на площадке лайтбокс светил сквозь пустое
   стекло, а рисунком был сам песок. Поэтому курсор по умолчанию сыплет,
   а не разгребает, и в «эфире» кадр маршрута виден, пока на него не насыпали. */
function fill(){var R=rnd(20240607);
  for(var i=0;i<H.length;i++)H[i]=0.03*R();}
function pour(gx,gy,rad){
  var i,j,d,idx;
  for(j=Math.max(0,gy-rad);j<Math.min(GH,gy+rad+1);j++)
    for(i=Math.max(0,gx-rad);i<Math.min(GW,gx+rad+1);i++){
      d=Math.sqrt((i-gx)*(i-gx)+(j-gy)*(j-gy)); if(d>rad)continue;
      idx=j*GW+i;
      H[idx]=Math.min(1.35,H[idx]+0.34*(1-d/rad));
    }
}
function dig(gx,gy,rad){
  var moved=0,i,j,d,idx;
  for(j=Math.max(0,gy-rad);j<Math.min(GH,gy+rad+1);j++)
    for(i=Math.max(0,gx-rad);i<Math.min(GW,gx+rad+1);i++){
      d=Math.sqrt((i-gx)*(i-gx)+(j-gy)*(j-gy)); if(d>rad)continue;
      idx=j*GW+i; var take=H[idx]*(1-d/rad)*0.75;
      H[idx]-=take; moved+=take;
    }
  /* снятый песок отваливает валиком по краю штриха: так ведёт себя настоящий */
  var ring=[],r2=rad+2;
  for(j=Math.max(0,gy-r2);j<Math.min(GH,gy+r2+1);j++)
    for(i=Math.max(0,gx-r2);i<Math.min(GW,gx+r2+1);i++){
      d=Math.sqrt((i-gx)*(i-gx)+(j-gy)*(j-gy));
      if(d>rad*0.82&&d<=r2)ring.push(j*GW+i);
    }
  if(ring.length){var add=moved/ring.length;
    for(i=0;i<ring.length;i++)H[ring[i]]=Math.min(1.6,H[ring[i]]+add);}
}
function paintSand(){
  if(!sc)return;
  var ctx=sc.getContext('2d'), im=ctx.createImageData(GW,GH), d=im.data;
  var G=rnd(7717);
  for(var i=0;i<H.length;i++){
    var a=Math.max(0,Math.min(1,H[i]));
    /* зерно: песчинка либо есть, либо нет, поэтому шум идёт в альфу */
    a=Math.max(0,Math.min(1,a*(0.86+0.28*G())));
    var sh=0.78+0.22*Math.min(1,H[i]);   /* толще слой, темнее просвет */
    d[i*4]=Math.round(96*sh); d[i*4+1]=Math.round(64*sh);
    d[i*4+2]=Math.round(44*sh); d[i*4+3]=Math.round(Math.pow(a,1.3)*255);
  }
  if(!base){base=document.createElement('canvas');base.width=GW;base.height=GH;}
  base.getContext('2d').putImageData(im,0,0);
  ctx.setTransform(1,0,0,1,0,0);
  ctx.clearRect(0,0,sc.width,sc.height);
  /* лайтбокс снизу */
  var g=ctx.createLinearGradient(0,0,0,sc.height);
  g.addColorStop(0,'#FFFDF6');g.addColorStop(1,'#F0E6D2');
  ctx.fillStyle=g;ctx.fillRect(0,0,sc.width,sc.height);
  ctx.imageSmoothingEnabled=true;
  ctx.drawImage(base,0,0,sc.width,sc.height);
  paintAir();
}
function paintAir(){
  if(!ac)return;
  var ctx=ac.getContext('2d');
  ctx.setTransform(1,0,0,1,0,0);
  ctx.clearRect(0,0,ac.width,ac.height);
  if(airOk)ctx.drawImage(air,0,0,ac.width,ac.height);
  else{ctx.fillStyle='#2A241C';ctx.fillRect(0,0,ac.width,ac.height);}
  if(!base)return;
  if(keyOn){ctx.drawImage(base,0,0,ac.width,ac.height);}
  else{
    /* без ключа поверх кадра легла бы вся плоскость стола, вместе с фоном */
    ctx.save();
    ctx.fillStyle='#FBF4E6';ctx.fillRect(0,0,ac.width,ac.height);
    ctx.drawImage(base,0,0,ac.width,ac.height);
    ctx.restore();
  }
}
function sizeSand(){
  if(!sc)return;
  var dpr=Math.min(2,window.devicePixelRatio||1);
  [sc,ac].forEach(function(c){
    if(!c)return;
    var w=Math.max(1,Math.round(c.getBoundingClientRect().width));
    c.width=Math.round(w*dpr); c.height=Math.round(w*dpr*GH/GW);
    c.style.height=Math.round(w*GH/GW)+'px';
  });
  paintSand();
}
function at(e,c){
  var r=c.getBoundingClientRect();
  var p=e.touches?e.touches[0]:e;
  return [Math.round((p.clientX-r.left)/r.width*GW),
          Math.round((p.clientY-r.top)/r.height*GH)];
}
if(sc){
  var down=false,last=null;
  function stroke(e){
    var p=at(e,sc);
    var brush=mode==='pour'?pour:dig, rad=mode==='pour'?4:5;
    if(last){/* дотянуть штрих между кадрами, иначе на быстром движении дырки */
      var dx=p[0]-last[0],dy=p[1]-last[1],n=Math.max(1,Math.round(Math.hypot(dx,dy)/2));
      for(var s=1;s<=n;s++)brush(Math.round(last[0]+dx*s/n),Math.round(last[1]+dy*s/n),rad);
    }else brush(p[0],p[1],rad);
    last=p; paintSand();
  }
  sc.addEventListener('pointerdown',function(e){down=true;last=null;sc.setPointerCapture(e.pointerId);stroke(e);});
  sc.addEventListener('pointermove',function(e){if(down){e.preventDefault();stroke(e);}});
  ['pointerup','pointercancel'].forEach(function(ev){
    sc.addEventListener(ev,function(){down=false;last=null;});});
  var cl=document.getElementById('swclear');
  if(cl)cl.addEventListener('click',function(){fill();paintSand();});
  var pb=document.getElementById('swpour'), db=document.getElementById('swdig');
  function setMode(m){mode=m;
    [[pb,'pour'],[db,'dig']].forEach(function(o){
      if(!o[0])return;
      o[0].classList.toggle('on',o[1]===m);
      o[0].setAttribute('aria-pressed',o[1]===m?'true':'false');});}
  if(pb)pb.addEventListener('click',function(){setMode('pour');});
  if(db)db.addEventListener('click',function(){setMode('dig');});
  var kb=document.getElementById('swkey');
  if(kb)kb.addEventListener('click',function(){
    keyOn=!keyOn; kb.classList.toggle('on',keyOn);
    kb.setAttribute('aria-pressed',keyOn?'true':'false');
    kb.textContent=keyOn?'Альфа включена':'Альфа выключена';
    paintAir();});
  fill();
}

/* ── галерея ────────────────────────────────────────────────────────────── */
var GAL=%GAL%, lb=document.getElementById('swlb');
if(lb){
  var lim=lb.querySelector('img'),lcap=lb.querySelector('.sw-lb__cap'),gi=0;
  function show(i){gi=(i+GAL.length)%GAL.length;
    lim.src=IMG+'/'+GAL[gi][0]+'-m.jpg';lim.alt=GAL[gi][1];lcap.textContent=GAL[gi][1];}
  function open(i){show(i);lb.classList.add('on');document.body.style.overflow='hidden';}
  function close(){lb.classList.remove('on');document.body.style.overflow='';}
  [].slice.call(document.querySelectorAll('.sw-shot')).forEach(function(b){
    b.addEventListener('click',function(){open(+b.getAttribute('data-i'));});});
  lb.querySelector('.sw-lb__x').addEventListener('click',close);
  lb.querySelector('.sw-lb__n').addEventListener('click',function(e){e.stopPropagation();show(gi+1);});
  lb.querySelector('.sw-lb__p').addEventListener('click',function(e){e.stopPropagation();show(gi-1);});
  lb.addEventListener('click',function(e){if(e.target===lb||e.target===lim)close();});
  document.addEventListener('keydown',function(e){
    if(!lb.classList.contains('on'))return;
    if(e.key==='Escape')close();
    if(e.key==='ArrowRight')show(gi+1);
    if(e.key==='ArrowLeft')show(gi-1);});
}

/* ── ресайз ─────────────────────────────────────────────────────────────── */
var rt=null;
function relayout(){drawGround();sizeSand();}
window.addEventListener('resize',function(){
  clearTimeout(rt);rt=setTimeout(relayout,120);});
window.addEventListener('orientationchange',function(){setTimeout(relayout,260);});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(relayout);
relayout();
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Видеопродакшн","item":"https://hand-marketing.ru/videoproduction/"},'
  '{"@type":"ListItem","position":3,"name":"3D-визуализация маршрута Silk Way Rally",'
  f'"item":"{URL}"}}]}}</script>')

VIDEO_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"VideoObject","name":"3D-визуализация маршрута Silk Way Rally",'
  '"description":"Маршрут ралли-марафона Silk Way Rally от Сианя до Москвы: '
  'десять этапов собраны рельефом по координатам легенды трассы, у каждого '
  'этапа лиазоны, спецучасток, маршрут технички и состав покрытия.",'
  f'"thumbnailUrl":"https://hand-marketing.ru{IMG}/stage-01.jpg",'
  '"duration":"PT8M41S",'
  f'"contentUrl":"https://hand-marketing.ru{FILM}",'
  '"publisher":{"@type":"Organization","name":"Hand Marketing"}}</script>')

HEAD = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
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
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/led-relief-m.jpg">'
        '<link rel="stylesheet" href="/fonts/adventpro-arsenal.css">'
        + rc.FONT + rc.CSS + CSS.replace('%RED%', RED) + METRIKA + '</head><body>')


def page():
    st = [{'n': r[0], 'date': r[1], 'lat': r[2], 'ru': r[3], 'l1': r[4],
           'ss': r[5], 'l2': r[6], 'tot': r[7], 'srv': r[8], 'mix': r[9]}
          for r in STAGES]
    surf = {k: {'label': lab, 'color': col, 'kind': kind}
            for k, lab, col, kind, _orig in SURFACES}
    surf['order'] = ORDER
    gal = [[s, WHAT.get(s, '')] for s in GALLERY]
    js = (PAGE_JS.replace('%STAGES%', json.dumps(st, ensure_ascii=False))
                 .replace('%SEEK%', json.dumps(SEEK, ensure_ascii=False))
                 .replace('%SURF%', json.dumps(surf, ensure_ascii=False))
                 .replace('%GROUND%', json.dumps(
                     {k: {n: round(v, 2) for n, v in d.items()}
                      for k, d in GROUND.items()}, ensure_ascii=False))
                 .replace('%GAL%', json.dumps(gal, ensure_ascii=False))
                 .replace('%IMG%', IMG))
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="sw">{hero()}{brief()}{route()}{table()}'
            f'{ground()}{tot()}{sand()}{rig()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}'
            f'{BREADCRUMB_LD}{VIDEO_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'silkway')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
