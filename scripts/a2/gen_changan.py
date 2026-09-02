#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/event/changan/index.html: кейс «Презентация Changan CS35».

Материал — финальный отчёт по проекту на 42 полосы, 210 фотографий
(31 кадр со съёмки в ТРЦ «Июнь» и 179 снимков вечера в дилерском центре
«РИА Авто») и ролик 80 с. Отчёт даёт то, чего почти никогда нет в кейсах:
полную воронку BTL с цифрами, посуточные данные стенда, список вопросов
и возражений посетителей, тайминг вечера и рекомендации агентства.

Год клиент просил не ставить, цены не показывать: поэтому на странице нет
ни года, ни ролл-апа с ценой, ни прайс-листа, хотя в отчёте они есть.

Идея страницы. Кейс не про «сделали красиво», а про воронку: 1603 разговора
в атриуме превращаются в 27 гостей вечера, и обе площадки существуют ради
этого перехода. Отсюда механики:

  • «Семь дней» — главная по данным. Воронка из пяти ступеней и посуточная
    разбивка, снятая пиксельно с графика отчёта (scripts/changan-assets.py).
    Две верхние суммы сходятся с итогом (1594 против 1603, 597 против 599),
    две нижние расходятся вдвое: часть записей пришла не через стенд.
    Страница называет это вслух, а не прячет.
  • «Раскрась и выпусти на трассу» — главная интерактивная, такой на сайте
    не было. На площадке гость раскрашивал лист с контуром машины, лист
    сканировали, и раскрашенная машина выезжала на виртуальную трассу.
    Здесь то же самое: кузов сверху набран зонами, фломастеры взяты
    с кадров, кнопка «Сканировать» отправляет вашу машину на трассу
    к соседям, чьи цвета сняты с кадров ролика.
  • «Три проектора» — почему проекция на машину сложнее, чем на стену:
    один луч оставляет весь дальний борт в тени, стекло без плёнки
    не отражает, а пропускает. Схема считает освещённую долю кузова.

Палитра снята с материала: синий и серебро с фирменного знака, кислотный
лайм и маджента с кадров маппинга, красный с костюмов барабанного шоу,
бумага и чернила с листа-раскраски.

Шрифты: Philosopher (заголовки, каллиграфические срезы), Golos Text
(текст), Neucha на подписи в блоке раскраски: рукописный там не украшение,
а голос фломастера с листа.

Ассеты: mirror/images/changan/ (scripts/changan-assets.py).

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

IMG = '/images/changan'
VIDEO = '/media/changan-hm-180220.mp4'
URL = 'https://hand-marketing.ru/event/changan/'
TITLE = 'Презентация Changan CS35: стенд в ТРЦ и шоу в дилерском центре | Hand Marketing'
DESCR = ('Презентация обновлённого Changan CS35: семь дней стенда в атриуме '
         'ТРЦ «Июнь», 1603 разговора и 126 записей на тест-драйв, вечер '
         'в дилерском центре «РИА Авто» с 3D-маппингом на автомобиле, '
         'китайским шоу и виртуальным тест-драйвом с раскраской.')

MAP = json.load(open(os.path.join(HERE, 'changan_map.json'), encoding='utf-8'))
BRIEF = MAP['brief']
FUNNEL = MAP['funnel']
DAYS = MAP['days']
ROWS = MAP['rows']
SUMS = MAP['rows_sum']
PROGRAM = MAP['program']

# ─── палитра ───────────────────────────────────────────────────────────────
PAL = {
    'ink': '#0C1017',        # ночь зала
    'ink2': '#141A25',
    'blue': '#1E5AA8',       # синий фирменного знака
    'blue2': '#4C8FE0',
    'lime': '#C9F23C',       # кислотный контур маппинга
    'mag': '#FF3E9A',        # маджента проекции
    'cyan': '#4ADEF0',
    'red': '#D5222B',        # костюмы барабанного шоу
    'paper': '#F5F1E8',      # лист раскраски
    'sand': '#C7B9A0',
}

# ─── фломастеры: цвета сняты с кадров, где гости раскрашивают листы ────────
PENS = [
    ('#E02A24', 'красный'), ('#F07C1E', 'оранжевый'), ('#F5C518', 'жёлтый'),
    ('#3EB44A', 'зелёный'), ('#1B6FD0', 'синий'), ('#8B3FC4', 'фиолетовый'),
    ('#EE3D8F', 'розовый'), ('#111418', 'чёрный'), ('#FFFFFF', 'белый'),
]

# ─── зоны кузова сверху: (id, тип, геометрия, подпись, цвет по умолчанию) ──
# Геометрия задана в системе 0 0 820 420, машина носом вправо, ось y=210.
# Все зоны обрезаны клипом по контуру кузова, поэтому стыки точные,
# а формы остаются простыми прямоугольниками и трапециями.
# Контур кузова строится из продольного профиля полуширины: так форму
# можно править числами, а не подгонять кривые на глаз. Пропорции сняты
# с габаритов CS35 (длина к ширине примерно 2,4 к 1).
BODY_PROFILE = [(96, 104), (140, 128), (215, 142), (330, 147), (450, 148),
                (585, 144), (672, 134), (742, 112)]


def _smooth(points, closed=True):
    """Catmull-Rom через точки, переведённый в кубические Безье."""
    n = len(points)
    d = f'M {points[0][0]:.1f},{points[0][1]:.1f}'
    for i in range(n - (0 if closed else 1)):
        p0 = points[(i - 1) % n]; p1 = points[i]
        p2 = points[(i + 1) % n]; p3 = points[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += (f' C {c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} '
              f'{p2[0]:.1f},{p2[1]:.1f}')
    return d + (' Z' if closed else '')


def _body_points():
    up = [(x, 210 - w) for x, w in BODY_PROFILE]
    down = [(x, 210 + w) for x, w in reversed(BODY_PROFILE)]
    return up + [(790, 210 - 44), (798, 210), (790, 210 + 44)] + down + \
        [(50, 210 + 40), (42, 210), (50, 210 - 40)]


BODY_D = _smooth(_body_points())
ZONES = [
    ('bumper-rear', 'rect', (20, 30, 108, 360), 'Задний бампер', '#FFFFFF'),
    ('tailgate', 'rect', (128, 30, 50, 360), 'Дверь багажника', '#FFFFFF'),
    ('glass-rear', 'poly', ((178, 96), (250, 116), (250, 304), (178, 324)),
     'Заднее стекло', '#7E8892'),
    ('roof', 'rect', (250, 118, 220, 184), 'Крыша', '#FFFFFF'),
    ('glass-side-l', 'rect', (262, 92, 196, 28), 'Стекло слева', '#7E8892'),
    ('glass-side-r', 'rect', (262, 300, 196, 28), 'Стекло справа', '#7E8892'),
    ('door-rear-l', 'rect', (178, 30, 112, 62), 'Задняя дверь слева', '#FFFFFF'),
    ('door-front-l', 'rect', (290, 30, 180, 62), 'Передняя дверь слева', '#FFFFFF'),
    ('door-rear-r', 'rect', (178, 328, 112, 62), 'Задняя дверь справа', '#FFFFFF'),
    ('door-front-r', 'rect', (290, 328, 180, 62), 'Передняя дверь справа', '#FFFFFF'),
    ('glass-front', 'poly', ((470, 118), (556, 88), (556, 332), (470, 302)),
     'Лобовое стекло', '#7E8892'),
    ('hood', 'rect', (556, 30, 146, 360), 'Капот', '#FFFFFF'),
    ('bumper-front', 'rect', (702, 30, 104, 360), 'Передний бампер', '#FFFFFF'),
]
MIRRORS = [(524, 46, 42, 22), (524, 352, 42, 22)]      # x, y, w, h
WHEELS = [(206, 68), (206, 352), (616, 68), (616, 352)]  # центры колёс

# ─── что стояло на стенде: снято с кадра сверху ────────────────────────────
STAND_ITEMS = [
    ('Два подиума', 'Белый и чёрный CS35 в разных комплектациях: у одного '
                    'открыт капот и багажник, во второй сажали за руль'),
    ('Экран на стойке', 'Ролик крутился между подиумами, лицом к потоку'),
    ('Инфостойка', 'Прайс-листы, буклеты и анкеты под рукой у промо-модели'),
    ('Два ролл-апа', 'Марка, модель и предложение дилера'),
    ('Зона с диваном', 'Место, где садились заполнять анкету и разговаривать'),
    ('Три человека смены', 'Координатор и две промо-модели в фирменной одежде'),
]
GIFTS = [
    ('Спиннер с маркой', 'Приз первой категории'),
    ('Шоколад с маркой', 'Получал каждый, кто заинтересовался машиной'),
    ('Прайс-лист и буклет', 'Уносили с собой'),
    ('Снеки и напитки', 'Работали на стенде все восемь часов смены'),
]

# ─── маппинг: что видно на кадрах ──────────────────────────────────────────
SHOW = [
    ('map-fire', 'Кислотный контур по рёбрам кузова'),
    ('map-lines', 'Сетка линий по борту'),
    ('map-spark', 'Разряды по двери'),
    ('map-flame', 'Пламя по капоту и крылу'),
    ('map-wave', 'Волны вдоль борта'),
    ('map-brand', 'Знак и марка на двери'),
]

# ─── главы ролика: тайм-коды сняты сканом кадров ───────────────────────────
CHAPTERS = [
    (0, 'Титры'),
    (6, 'Обновлённый CS35 крупно'),
    (16, 'Стенд в ТРЦ «Июнь»'),
    (46, 'Вечер в дилерском центре'),
    (52, 'Шоу маппинга'),
    (62, 'Раскраска, сканер, трасса'),
    (72, 'Финал'),
]


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def pic(slug, alt, cls='', sizes='(max-width:760px) 92vw, 640px', lazy=True):
    """Кадр с webp и вторым размером: телефон не должен тянуть большой."""
    ld = ' loading="lazy" decoding="async"' if lazy else ''
    return (f'<picture class="{cls}">'
            f'<source type="image/webp" sizes="{sizes}" '
            f'srcset="{IMG}/{slug}-640.jpg.webp 640w, {IMG}/{slug}.jpg.webp 1280w">'
            f'<source sizes="{sizes}" '
            f'srcset="{IMG}/{slug}-640.jpg 640w, {IMG}/{slug}.jpg 1280w">'
            f'<img src="{IMG}/{slug}.jpg" alt="{esc(alt)}"{ld}></picture>')


CSS1 = """<style id="cg-css">
.cg{--ink:%INK%;--ink2:%INK2%;--blue:%BLUE%;--blue2:%BLUE2%;--lime:%LIME%;
 --mag:%MAG%;--cyan:%CYAN%;--red:%RED%;--paper:%PAPER%;--sand:%SAND%;
 --line:rgba(255,255,255,.14);--dim:rgba(255,255,255,.62);
 background:var(--ink);color:#fff;
 font-family:'Golos Text',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 font-size:17px;line-height:1.62;overflow-x:hidden}
.cg *,.cg *::before,.cg *::after{box-sizing:border-box}
.cg h1,.cg h2,.cg h3,.cg .ttl{font-family:'Philosopher',Georgia,serif;font-weight:700;
 line-height:1.08;letter-spacing:-.01em;margin:0}
.cg p{margin:0 0 1em}
.cg section{padding:88px 24px;position:relative}
.cg .in{max-width:1180px;margin:0 auto}
.cg .narrow{max-width:820px}
.cg .lead{font-size:20px;line-height:1.6;color:rgba(255,255,255,.86)}
.cg .dim{color:var(--dim)}
.cg .kicker{font:600 12px/1 'Golos Text',sans-serif;letter-spacing:.18em;
 text-transform:uppercase;color:var(--blue2);margin:0 0 18px}
.cg h2{font-size:clamp(28px,4.2vw,46px);margin:0 0 18px}
.cg h3{font-size:clamp(20px,2.4vw,26px);margin:0 0 10px}
.cg .note{font-size:14px;line-height:1.55;color:rgba(255,255,255,.5)}
.cg picture{display:block}
.cg picture img{display:block;width:100%;height:auto}
.cg .rv{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.cg .rv.on{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.cg .rv{opacity:1;transform:none;transition:none}}

/* ── герой ───────────────────────────────────────────────────────────── */
.cg-hero{padding:0;min-height:min(92vh,860px);display:flex;align-items:flex-end;
 background:#05070B;overflow:hidden}
.cg-hero__bg{position:absolute;inset:0;overflow:hidden}
.cg-hero__bg picture,.cg-hero__bg img{width:100%;height:100%;object-fit:cover}
.cg-hero__bg::after{content:'';position:absolute;inset:0;
 background:linear-gradient(180deg,rgba(5,7,11,.55) 0%,rgba(5,7,11,.2) 38%,rgba(5,7,11,.94) 88%)}
.cg-hero__in{position:relative;width:100%;max-width:1180px;margin:0 auto;padding:120px 24px 60px}
.cg-hero h1{font-size:clamp(38px,7.2vw,84px);max-width:16ch}
.cg-hero__sub{margin:22px 0 0;max-width:56ch;font-size:clamp(17px,2vw,21px);
 color:rgba(255,255,255,.86)}
.cg-hero__where{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 22px}
.cg-hero__where span{font:600 13px/1 'Golos Text',sans-serif;letter-spacing:.04em;
 padding:9px 14px;border:1px solid var(--line);border-radius:999px;
 background:rgba(10,14,20,.5);backdrop-filter:blur(6px)}
.cg-hero__nums{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;margin-top:44px;
 border-top:1px solid var(--line)}
.cg-hero__nums div{padding:20px 18px 0}
.cg-hero__nums b{display:block;font-family:'Philosopher',Georgia,serif;font-weight:700;
 font-size:clamp(30px,4vw,44px);line-height:1;color:var(--lime)}
.cg-hero__nums span{display:block;margin-top:8px;font-size:14px;color:var(--dim);line-height:1.4}

/* ── две площадки ────────────────────────────────────────────────────── */
.cg-two{background:var(--ink2)}
.cg-two__grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:34px}
.cg-place{border:1px solid var(--line);border-radius:18px;overflow:hidden;
 background:rgba(255,255,255,.02);display:flex;flex-direction:column}
.cg-place picture img{aspect-ratio:16/9;object-fit:cover}
.cg-place__b{padding:22px 24px 26px}
.cg-place__t{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:12px}
.cg-place__t b{font-family:'Philosopher',Georgia,serif;font-size:23px}
.cg-place__t i{font-style:normal;font-size:13px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--blue2)}
.cg-place dl{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;margin:0;font-size:15px}
.cg-place dt{color:rgba(255,255,255,.45)}
.cg-place dd{margin:0}
.cg-task{margin-top:34px;display:grid;grid-template-columns:1fr 1fr;gap:26px}
.cg-task__box{border-left:2px solid var(--blue);padding-left:20px}
.cg-task__box h3{font-size:19px;margin-bottom:8px}
.cg-task__box ul{margin:0;padding-left:18px}
.cg-task__box li{margin-bottom:6px;color:rgba(255,255,255,.8)}

/* ── воронка ─────────────────────────────────────────────────────────── */
.cg-fun{background:var(--ink)}
.cg-fun__wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
 gap:40px;margin-top:36px;align-items:start}
.cg-fun__steps{display:flex;flex-direction:column}
.cg-step{position:relative;border:0;padding:0;background:none;color:inherit;
 text-align:left;cursor:pointer;font:inherit;display:block;width:100%}
.cg-step{padding:14px 0;border-bottom:1px solid rgba(255,255,255,.07)}
.cg-step__top{display:flex;align-items:baseline;gap:14px;margin-bottom:10px}
.cg-step__top b{font-family:'Philosopher',Georgia,serif;font-size:32px;line-height:1;
 min-width:2.6em}
.cg-step__top span{font-size:15px;color:rgba(255,255,255,.86);flex:1}
.cg-step__top i{font-style:normal;font-size:13px;color:var(--lime);white-space:nowrap}
.cg-step__bar{position:relative;display:block;height:12px;border-radius:6px;overflow:hidden;
 background:rgba(255,255,255,.06)}
.cg-step__fill{position:absolute;left:0;top:0;bottom:0;border-radius:9px;
 background:linear-gradient(90deg,var(--blue) 0%,var(--blue2) 100%);
 transition:width .55s cubic-bezier(.4,0,.2,1)}
.cg-step:nth-child(5) .cg-step__fill{background:linear-gradient(90deg,#8A2740,var(--mag))}
.cg-step.is-on .cg-step__top b{color:var(--lime)}
.cg-step.is-on .cg-step__bar{box-shadow:0 0 0 1px var(--lime)}
.cg-step:hover .cg-step__top span{color:#fff}
.cg-fun__panel{border:1px solid var(--line);border-radius:18px;padding:24px;
 background:rgba(255,255,255,.02)}
.cg-fun__head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;
 margin-bottom:18px}
.cg-fun__head h3{font-size:20px}
.cg-fun__head p{margin:6px 0 0;font-size:14px;color:var(--dim)}
.cg-days{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;align-items:end;
 height:190px;margin-top:10px}
.cg-day{display:flex;flex-direction:column;justify-content:flex-end;height:100%;gap:6px}
.cg-day__bar{border-radius:6px 6px 2px 2px;background:linear-gradient(180deg,var(--blue2),var(--blue));
 transition:height .5s cubic-bezier(.4,0,.2,1);min-height:2px}
.cg-day__v{font:700 13px/1 'Golos Text',sans-serif;text-align:center}
.cg-day__d{font-size:11px;color:rgba(255,255,255,.45);text-align:center;line-height:1.25}
.cg-fun__sum{margin-top:18px;padding-top:16px;border-top:1px solid var(--line);
 font-size:14px;color:var(--dim)}
.cg-fun__sum b{color:#fff;font-weight:600}
.cg-toggle{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:3px;
 gap:2px;background:rgba(255,255,255,.03)}
.cg-toggle button{border:0;background:none;color:var(--dim);cursor:pointer;
 font:600 13px/1 'Golos Text',sans-serif;padding:9px 16px;border-radius:999px;
 transition:background .2s,color .2s}
.cg-toggle button.is-on{background:#fff;color:#0C1017}
.cg-fun__foot{margin-top:34px;display:grid;grid-template-columns:1.2fr 1fr;gap:30px;
 align-items:start}
.cg-drop{border-top:2px solid var(--mag);padding-top:16px}
.cg-drop b{font-family:'Philosopher',Georgia,serif;font-size:30px;color:var(--mag)}
</style>"""


CSS2 = """<style id="cg-css2">
/* ── стенд ───────────────────────────────────────────────────────────── */
.cg-stand{background:var(--ink2)}
.cg-stand__top{display:grid;grid-template-columns:1.35fr 1fr;gap:34px;margin-top:34px;
 align-items:start}
.cg-stand__ph{border-radius:16px;overflow:hidden;border:1px solid var(--line)}
.cg-stand__list{display:flex;flex-direction:column;gap:2px}
.cg-stand__list div{padding:14px 0;border-bottom:1px solid var(--line)}
.cg-stand__list b{display:block;font-size:16px;margin-bottom:3px}
.cg-stand__list span{font-size:14px;color:var(--dim);line-height:1.5}
.cg-form{display:grid;grid-template-columns:1fr 1fr;gap:34px;margin-top:44px;align-items:center}
.cg-form__ph{border-radius:14px;overflow:hidden;background:#fff;padding:14px}
.cg-form ul{margin:0;padding-left:20px;font-size:15px;color:rgba(255,255,255,.82)}
.cg-form li{margin-bottom:5px}
.cg-gifts{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:40px}
.cg-gift{border:1px solid var(--line);border-radius:14px;padding:18px}
.cg-gift b{display:block;font-size:15px;margin-bottom:4px}
.cg-gift span{font-size:13px;color:var(--dim)}
.cg-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:34px}
.cg-strip picture{border-radius:12px;overflow:hidden;border:1px solid var(--line)}
.cg-strip img{aspect-ratio:16/10;object-fit:cover}

/* ── голоса поля ─────────────────────────────────────────────────────── */
.cg-voice{background:var(--ink)}
.cg-voice__cols{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:34px}
.cg-voice__col h3{display:flex;align-items:center;gap:10px;font-size:19px;margin-bottom:18px}
.cg-voice__col h3 i{font-style:normal;width:26px;height:26px;border-radius:50%;
 display:grid;place-items:center;font:700 14px/1 'Golos Text',sans-serif}
.cg-voice__col.q h3 i{background:rgba(213,34,43,.18);color:#FF7A7A}
.cg-voice__col.l h3 i{background:rgba(201,242,60,.16);color:var(--lime)}
.cg-voice__col ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
.cg-voice__col li{padding:13px 16px;border-radius:12px;font-size:15px;line-height:1.45;
 background:rgba(255,255,255,.04);border-left:2px solid transparent}
.cg-voice__col.q li{border-left-color:rgba(213,34,43,.7)}
.cg-voice__col.l li{border-left-color:rgba(201,242,60,.6)}

/* ── раскраска ───────────────────────────────────────────────────────── */
.cg-color{background:var(--paper);color:#14171C}
.cg-color .kicker{color:var(--blue)}
.cg-color .lead,.cg-color p{color:#3A4048}
.cg-color .note{color:#6B7280}
.cg-paint{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:34px;align-items:start}
.cg-sheet{background:#fff;border:2px solid #14171C;border-radius:8px;padding:18px;
 box-shadow:0 18px 40px -26px rgba(0,0,0,.5);position:relative}
.cg-sheet__marks span{position:absolute;width:22px;height:22px;background:#14171C}
.cg-sheet__marks span:nth-child(1){left:14px;top:14px}
.cg-sheet__marks span:nth-child(2){left:14px;bottom:14px}
.cg-sheet__marks span:nth-child(3){right:14px;bottom:14px}
.cg-sheet svg{display:block;width:100%;height:auto;touch-action:pan-y}
.cg-sheet .z{cursor:pointer;transition:opacity .15s}
.cg-sheet .z:hover{opacity:.82}
.cg-sheet .ln{fill:none;stroke:#14171C;stroke-width:3.5;pointer-events:none}
.cg-sheet .body{fill:none;stroke:#14171C;stroke-width:7}
.cg-sheet .wheels rect{fill:#14171C}
.cg-sheet .mirrors rect{fill:#14171C}
.cg-sheet .det rect{fill:#14171C;opacity:.92}
.cg-sheet .det .seam{fill:none;stroke:#14171C;stroke-width:3.5;opacity:.75}
.cg-sheet #cgStrokes{pointer-events:none}
.cg-sheet__hint{font-family:'Neucha',cursive;font-size:19px;color:#6B7280;
 text-align:center;margin:6px 0 0}
.cg-tools{margin-top:18px;display:flex;flex-direction:column;gap:14px}
.cg-pens{display:flex;flex-wrap:wrap;gap:9px}
.cg-pen{width:38px;height:38px;border-radius:50%;border:2px solid rgba(0,0,0,.15);
 cursor:pointer;padding:0;transition:transform .15s,box-shadow .15s}
.cg-pen:hover{transform:translateY(-2px)}
.cg-pen.is-on{box-shadow:0 0 0 3px #14171C;transform:translateY(-2px)}
.cg-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.cg-btn{border:1.5px solid #14171C;background:#fff;color:#14171C;border-radius:999px;
 padding:11px 20px;font:600 14px/1 'Golos Text',sans-serif;cursor:pointer;
 transition:background .18s,color .18s,transform .18s}
.cg-btn:hover{background:#14171C;color:#fff}
.cg-btn.is-on{background:#14171C;color:#fff}
.cg-btn--go{background:var(--blue);border-color:var(--blue);color:#fff;padding:13px 26px;
 font-size:15px}
.cg-btn--go:hover{background:#14171C;border-color:#14171C;transform:translateY(-2px)}
.cg-track{background:#0F1722;border-radius:16px;padding:14px;position:relative;
 border:1px solid rgba(0,0,0,.2)}
.cg-track canvas{display:block;width:100%;height:auto;border-radius:10px}
.cg-track__cap{display:flex;justify-content:space-between;gap:14px;align-items:center;
 margin-top:12px;color:rgba(255,255,255,.68);font-size:13px}
.cg-track__cap b{color:#fff;font-weight:600}
.cg-scan{position:absolute;left:0;right:0;height:44%;pointer-events:none;opacity:0;
 background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.85),rgba(255,255,255,0))}
.cg-color__ph{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:36px}
.cg-color__ph figure{margin:0}
.cg-color__ph picture{border-radius:12px;overflow:hidden}
.cg-color__ph img{aspect-ratio:3/2;object-fit:cover}
.cg-color__ph figcaption{font-family:'Neucha',cursive;font-size:17px;color:#5A626C;
 margin-top:8px;line-height:1.35}

/* ── маппинг ─────────────────────────────────────────────────────────── */
.cg-map{background:#07090E}
.cg-map__wrap{display:grid;grid-template-columns:1.15fr 1fr;gap:34px;margin-top:34px;
 align-items:start}
.cg-scene{border:1px solid var(--line);border-radius:16px;padding:18px;
 background:radial-gradient(120% 90% at 50% 0%,rgba(76,143,224,.12),transparent 70%)}
.cg-scene svg{display:block;width:100%;height:auto}
.cg-map__ctl{display:flex;flex-direction:column;gap:22px}
.cg-ctl h3{font-size:18px;margin-bottom:8px}
.cg-ctl p{font-size:15px;color:var(--dim);margin:0 0 12px}
.cg-read{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:6px}
.cg-read div{border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.cg-read b{display:block;font-family:'Philosopher',Georgia,serif;font-size:28px;
 line-height:1;color:var(--lime)}
.cg-read span{display:block;margin-top:6px;font-size:13px;color:var(--dim);line-height:1.35}
.cg-show{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:36px}
.cg-show figure{margin:0}
.cg-show picture{border-radius:12px;overflow:hidden;border:1px solid var(--line)}
.cg-show img{aspect-ratio:3/2;object-fit:cover}
.cg-show figcaption{margin-top:8px;font-size:13px;color:var(--dim);line-height:1.4}

/* ── вечер ───────────────────────────────────────────────────────────── */
.cg-eve{background:var(--ink2)}
.cg-eve__wrap{display:grid;grid-template-columns:340px 1fr;gap:34px;margin-top:34px;
 align-items:start}
.cg-time{display:flex;flex-direction:column;border-left:2px solid var(--line);padding-left:0}
.cg-time__row{display:grid;grid-template-columns:96px 1fr;gap:14px;padding:11px 0 11px 18px;
 position:relative;border-bottom:1px solid rgba(255,255,255,.06)}
.cg-time__row::before{content:'';position:absolute;left:-5px;top:20px;width:8px;height:8px;
 border-radius:50%;background:var(--blue2)}
.cg-time__row.hot::before{background:var(--lime)}
.cg-time__row time{font:600 14px/1.4 'Golos Text',sans-serif;color:var(--dim)}
.cg-time__row span{font-size:15px}
.cg-eve__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.cg-eve__grid figure{margin:0}
.cg-eve__grid picture{border-radius:12px;overflow:hidden;border:1px solid var(--line)}
.cg-eve__grid img{aspect-ratio:3/2;object-fit:cover}
.cg-eve__grid figcaption{margin-top:7px;font-size:13px;color:var(--dim);line-height:1.4}

/* ── плеер ───────────────────────────────────────────────────────────── */
.cg-film{background:var(--ink)}
.cg-film__box{margin-top:30px;border-radius:16px;overflow:hidden;border:1px solid var(--line);
 background:#000}
.cg-film video{display:block;width:100%;height:auto}
.cg-chaps{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.cg-chaps button{border:1px solid var(--line);background:rgba(255,255,255,.03);color:var(--dim);
 border-radius:999px;padding:9px 15px;font:600 13px/1 'Golos Text',sans-serif;cursor:pointer;
 transition:border-color .2s,color .2s}
.cg-chaps button:hover,.cg-chaps button.is-on{border-color:var(--lime);color:#fff}
.cg-chaps button i{font-style:normal;color:var(--lime);margin-right:7px}

/* ── итоги ───────────────────────────────────────────────────────────── */
.cg-out{background:var(--ink2)}
.cg-out__grid{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:30px}
.cg-out__box{border:1px solid var(--line);border-radius:16px;padding:24px 26px}
.cg-out__box h3{font-size:19px;margin-bottom:12px}
.cg-out__box ul{margin:0;padding-left:18px;font-size:15px;color:rgba(255,255,255,.82)}
.cg-out__box li{margin-bottom:8px}
.cg-out__last{margin-top:34px;font-size:19px;line-height:1.6;max-width:62ch}
</style>"""

CSS3 = """<style id="cg-css3">
@media (max-width:1080px){
 .cg-fun__wrap,.cg-map__wrap,.cg-eve__wrap{grid-template-columns:1fr}
 .cg-stand__top,.cg-paint,.cg-form,.cg-fun__foot{grid-template-columns:1fr}
 .cg-eve__wrap{gap:26px}
}
@media (max-width:860px){
 .cg section{padding:64px 18px}
 .cg-two__grid,.cg-task,.cg-voice__cols,.cg-out__grid{grid-template-columns:1fr}
 .cg-gifts,.cg-strip{grid-template-columns:1fr 1fr}
 .cg-show,.cg-eve__grid,.cg-color__ph{grid-template-columns:1fr 1fr}
 .cg-hero__nums{grid-template-columns:1fr 1fr;gap:0}
 .cg-hero__nums div{padding:16px 0}
 .cg-hero__in{padding:100px 18px 48px}
 .cg-days{height:150px;gap:5px}
 .cg-day__v{font-size:11px}
 .cg-day__d{font-size:9px}
}
@media (max-width:560px){
 .cg{font-size:16px}
 .cg-strip,.cg-gifts,.cg-show,.cg-eve__grid,.cg-color__ph{grid-template-columns:1fr}
 .cg-step__top{flex-wrap:wrap;gap:6px 12px}
 .cg-step__top b{font-size:26px;min-width:2.2em}
 .cg-step__top span{font-size:14px}
 .cg-step__top i{flex-basis:100%}
 .cg-sheet{padding:12px}
 .cg-sheet__marks span{width:14px;height:14px;left:9px;top:9px}
 .cg-sheet__marks span:nth-child(2){left:9px;bottom:9px}
 .cg-sheet__marks span:nth-child(3){right:9px;bottom:9px}
 .cg-pen{width:34px;height:34px}
}
/* телефон в ландшафте: высокий герой не должен съедать весь экран */
@media (max-height:520px) and (orientation:landscape){
 .cg-hero{min-height:auto}
 .cg-hero__in{padding:88px 18px 36px}
 .cg-hero__nums{margin-top:26px}
}
</style>"""


def hero():
    nums = [
        ('1603', 'разговора на стенде за семь дней'),
        ('126', 'записей на тест-драйв'),
        ('3 мин', 'световое шоу на кузове CS35'),
        ('8 часов', 'смена стенда, с полудня до восьми'),
    ]
    cells = ''.join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in nums)
    return (
        '<section class="cg-hero">'
        f'<div class="cg-hero__bg">{pic("map-fire", "Changan CS35 под проекцией светового шоу", sizes="100vw", lazy=False)}</div>'
        '<div class="cg-hero__in">'
        '<div class="cg-hero__where">'
        f'<span>Event и BTL</span><span>{BRIEF["mall"]}</span>'
        f'<span>{BRIEF["dealer"]}</span></div>'
        '<h1>Презентация Changan CS35</h1>'
        '<p class="cg-hero__sub">Семь дней стенда в атриуме торгового центра, '
        'чтобы собрать тех, кому интересна машина. И один вечер в дилерском '
        'центре, чтобы они приехали на тест-драйв.</p>'
        f'<div class="cg-hero__nums">{cells}</div>'
        '</div></section>')


def two():
    tasks = ('<div class="cg-task__box"><h3>Что просил клиент</h3><ul>'
             '<li>Поднять знание марки Changan</li>'
             '<li>Показать обновлённый CS35</li>'
             '<li>Сделать рекламную активность на лояльность к марке</li>'
             '<li>Привести целевую аудиторию на тест-драйв</li>'
             '</ul></div>'
             '<div class="cg-task__box"><h3>Что взяло на себя агентство</h3><ul>'
             '<li>Выбрать торговый центр под задачу и арендовать место</li>'
             '<li>Построить выставочное пространство под презентацию</li>'
             '<li>Вести презентацию и записывать целевых посетителей</li>'
             '<li>Сделать рекламное событие на площадке дилерского центра</li>'
             '</ul></div>')
    return (
        '<section class="cg-two"><div class="in">'
        '<p class="kicker rv">Две площадки</p>'
        '<h2 class="rv">Атриум собирает, дилерский центр закрывает</h2>'
        '<p class="lead narrow rv">Машину в торговом центре видят все, кто идёт мимо, '
        'но купить её там нельзя. Поэтому стенд работал как сито: разговор, '
        'демонстрация, анкета, запись. А приглашение на вечер получали те, '
        'кто дошёл до анкеты.</p>'
        '<div class="cg-two__grid">'
        '<div class="cg-place rv">'
        f'{pic("stand-top", "Стенд Changan в атриуме ТРЦ «Июнь» сверху")}'
        '<div class="cg-place__b"><div class="cg-place__t">'
        f'<b>{BRIEF["mall"]}</b><i>стенд</i></div><dl>'
        f'<dt>Даты</dt><dd>{BRIEF["mall_days"]}, семь дней</dd>'
        f'<dt>Смена</dt><dd>{BRIEF["mall_hours"]}</dd>'
        f'<dt>Люди</dt><dd>{BRIEF["staff"]}</dd>'
        '<dt>Машины</dt><dd>две, в разных цветах и комплектациях</dd>'
        '</dl></div></div>'
        '<div class="cg-place rv">'
        f'{pic("dealer", "Фасад дилерского центра «РИА Авто»")}'
        '<div class="cg-place__b"><div class="cg-place__t">'
        f'<b>{BRIEF["dealer"]}</b><i>вечер</i></div><dl>'
        f'<dt>Дата</dt><dd>{BRIEF["dealer_day"]}, один день</dd>'
        f'<dt>Время</dt><dd>{BRIEF["dealer_hours"]}</dd>'
        '<dt>Программа</dt><dd>маппинг, барабаны, танцы, конкурсы</dd>'
        '<dt>Зачем</dt><dd>тест-драйв и предложение на покупку</dd>'
        '</dl></div></div>'
        '</div>'
        f'<div class="cg-task rv">{tasks}</div>'
        '</div></section>')


def funnel():
    steps = ''
    keys = ['listen', 'demo', 'test', 'event', None]
    for i, st in enumerate(FUNNEL):
        prev = FUNNEL[i - 1]['value'] if i else None
        conv = ('' if prev is None else
                ('<i>' + f'{st["value"] / prev * 100:.1f}'.replace('.', ',')
                 + ' % от прошлого шага</i>'))
        w = st['value'] / FUNNEL[0]['value'] * 100
        steps += (
            f'<button class="cg-step{" is-on" if i == 0 else ""}" type="button" '
            f'data-i="{i}" data-key="{keys[i] or ""}" data-value="{st["value"]}">'
            f'<span class="cg-step__top"><b>{st["value"]}</b>'
            f'<span>{st["label"]}</span>{conv}</span>'
            f'<span class="cg-step__bar"><span class="cg-step__fill" '
            f'style="width:{max(w, 1.6):.2f}%"></span></span></button>')
    days = ''.join(
        f'<div class="cg-day"><div class="cg-day__v" data-v="{i}"></div>'
        f'<div class="cg-day__bar" data-b="{i}" style="height:0"></div>'
        f'<div class="cg-day__d">{d.replace(" ", "<br>")}</div></div>'
        for i, d in enumerate(DAYS))
    return (
        '<section class="cg-fun" id="funnel"><div class="in">'
        '<p class="kicker rv">Семь дней стенда</p>'
        '<h2 class="rv">1603 разговора, 27 гостей</h2>'
        '<p class="lead narrow rv">Каждый шаг воронки в отчёте посчитан руками '
        'смены: сколько человек выслушали рассказ, сколько дошли до показа машины, '
        'сколько заполнили анкету. Нажмите на ступень, чтобы увидеть её по дням.</p>'
        '<div class="cg-fun__wrap">'
        f'<div class="cg-fun__steps rv">{steps}</div>'
        '<div class="cg-fun__panel rv"><div class="cg-fun__head">'
        '<div><h3 data-panel-title>Выслушали информацию</h3>'
        '<p data-panel-sub>По дням, с 27 января по 2 февраля</p></div>'
        '<div class="cg-toggle"><button type="button" class="is-on" data-mode="abs">штуки</button>'
        '<button type="button" data-mode="rel">доля дня</button></div></div>'
        f'<div class="cg-days">{days}</div>'
        '<div class="cg-fun__sum" data-panel-sum></div>'
        '</div></div>'
        '<div class="cg-fun__foot">'
        '<div class="rv"><div class="cg-drop"><b>27 из 117</b></div>'
        '<p style="margin-top:12px">До вечера в дилерском центре дошёл каждый '
        'четвёртый из записавшихся. В отчёте причина названа прямо: в день '
        'мероприятия была плохая погода. Это не отговорка, а цифра, которую '
        'учитывают в следующем плане: если явка держится на четверти, '
        'приглашать нужно вчетверо больше.</p></div>'
        '<div class="rv"><h3>Почему суммы не сходятся</h3>'
        f'<p class="note">Итоговых цифр в отчёте пять, а посуточный график '
        f'подписей значений не имеет, поэтому столбцы сняты с него пиксельно. '
        f'По верхним двум ступеням суммы почти совпадают с итогом: '
        f'{SUMS["listen"]} против {FUNNEL[0]["value"]} и {SUMS["demo"]} против '
        f'{FUNNEL[1]["value"]}, разница в пределах точности снятия. По записям '
        f'на тест-драйв и на событие график даёт {SUMS["test"]} и {SUMS["event"]}, '
        f'а итог {FUNNEL[2]["value"]} и {FUNNEL[3]["value"]}: значит часть '
        f'записей пришла мимо стенда, по телефону дилера и на самой площадке '
        f'вечера. Мы показываем обе цифры, а не подгоняем одну под другую.</p>'
        '</div></div>'
        '</div></section>')


def stand():
    items = ''.join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in STAND_ITEMS)
    gifts = ''.join(f'<div class="cg-gift"><b>{b}</b><span>{s}</span></div>'
                    for b, s in GIFTS)
    strip = ''.join(pic(s, a) for s, a in (
        ('hood', 'Консультация у открытого капота CS35'),
        ('sofa', 'Семья заполняет анкету в зоне отдыха стенда'),
        ('gift', 'Подарок посетителю: спиннер с маркой'),
        ('leaflet', 'Раздача материалов в галерее торгового центра')))
    return (
        '<section class="cg-stand"><div class="in">'
        '<p class="kicker rv">Как работал стенд</p>'
        '<h2 class="rv">Сито на 1603 разговора</h2>'
        '<div class="cg-stand__top">'
        f'<div class="cg-stand__ph rv">{pic("stand-wide", "Стенд Changan в атриуме с посетителями")}'
        '<p class="note" style="padding:12px 4px 0">Атриум, два подиума, '
        'между ними экран с роликом. Всё, что стояло на площадке, '
        'видно на одном кадре сверху.</p></div>'
        f'<div class="cg-stand__list rv">{items}</div>'
        '</div>'
        '<div class="cg-form">'
        f'<div class="cg-form__ph rv">{pic("form-a5", "Макет анкеты A5 для записи на тест-драйв")}</div>'
        '<div class="rv"><h3>Анкета решала всё</h3>'
        '<p>Разговор считался результативным, когда посетитель заполнял анкету. '
        'В ней десять пунктов, и только семь из них про контакты. Остальные '
        'работают на дилера: есть ли машина сейчас, когда планируется покупка, '
        'в какой ценовой категории, нужен ли кредит и трейд-ин.</p>'
        '<ul><li>Владеете ли вы автомобилем сейчас, марка, модель, год</li>'
        '<li>Собираетесь ли купить автомобиль в ближайшие три месяца</li>'
        '<li>В какой ценовой категории</li>'
        '<li>Воспользуетесь ли кредитом и трейд-ином</li>'
        '<li>Когда удобно приехать на тест-драйв</li></ul>'
        '<p class="note">Последний пункт и превращал анкету в запись: человек '
        'сам называл день и время, а дилер знал, кому звонить.</p></div>'
        '</div>'
        '<h3 class="rv" style="margin-top:48px">Что уносили со стенда</h3>'
        f'<div class="cg-gifts rv">{gifts}</div>'
        f'<div class="cg-strip rv">{strip}</div>'
        '</div></section>')


def voices():
    qs = ''.join(f'<li>{q}</li>' for q in MAP['questions'])
    ls = ''.join(f'<li>{l}</li>' for l in MAP['liked'])
    return (
        '<section class="cg-voice"><div class="in">'
        '<p class="kicker rv">Поле</p>'
        '<h2 class="rv">О чём спрашивали и что хвалили</h2>'
        '<p class="lead narrow rv">Смена записывала не только цифры. За семь дней '
        'у стенда собрался живой список вопросов и возражений: то, что мешает '
        'человеку решиться, и то, ради чего он всё-таки возвращается к машине. '
        'Для марки, которая заходит на рынок, это ценнее охвата.</p>'
        '<div class="cg-voice__cols">'
        f'<div class="cg-voice__col q rv"><h3><i>?</i>Вопросы и сомнения</h3><ul>{qs}</ul></div>'
        f'<div class="cg-voice__col l rv"><h3><i>+</i>Что нравилось</h3><ul>{ls}</ul></div>'
        '</div>'
        '<p class="note rv" style="margin-top:26px;max-width:70ch">Половина '
        'вопросов не про машину, а про то, что будет после покупки: '
        'запчасти, сервис, расхождение цены у дилера с прайс-листом. '
        'Отдельная строка отчёта: тёмно-красный цвет из буклета спрашивали '
        'так часто, что его отметили как отдельный факт.</p>'
        '</div></section>')


# ─── геометрия кузова: доли поверхности считаются, а не берутся на глаз ────
def _bezier_poly(step=0.02):
    """Контур кузова из BODY_D в виде полигона: кубические Безье
    сэмплируются, чтобы можно было честно посчитать площади зон."""
    pts, cur, i = [], None, 0
    toks = BODY_D.replace(',', ' ').split()
    while i < len(toks):
        t = toks[i]
        if t == 'M':
            cur = (float(toks[i + 1]), float(toks[i + 2])); pts.append(cur); i += 3
        elif t == 'C':
            p1 = (float(toks[i + 1]), float(toks[i + 2]))
            p2 = (float(toks[i + 3]), float(toks[i + 4]))
            p3 = (float(toks[i + 5]), float(toks[i + 6]))
            k = step
            while k <= 1.0001:
                u = 1 - k
                x = (u ** 3 * cur[0] + 3 * u * u * k * p1[0]
                     + 3 * u * k * k * p2[0] + k ** 3 * p3[0])
                y = (u ** 3 * cur[1] + 3 * u * u * k * p1[1]
                     + 3 * u * k * k * p2[1] + k ** 3 * p3[1])
                pts.append((x, y)); k += step
            cur = p3; i += 7
        elif t in ('Z', 'z'):
            i += 1
        else:
            i += 1
    return pts


def areas():
    """Доли поверхности кузова сверху: сколько занимает остекление.

    Нужно для схемы маппинга: без белой плёнки стекло не отражает свет,
    а пропускает его в салон, и вся эта доля выпадает из картинки.
    Считается растеризацией зон внутри контура, а не прикидкой.
    """
    import numpy as np
    poly = np.array(_bezier_poly(), dtype=float)
    W, H = 820, 420
    yy, xx = np.mgrid[0:H, 0:W]
    px, py = xx + .5, yy + .5
    inside = np.zeros((H, W), bool)
    x1, y1 = poly[:, 0], poly[:, 1]
    x2, y2 = np.roll(x1, -1), np.roll(y1, -1)
    for a, b, c, d in zip(x1, y1, x2, y2):
        if b == d:
            continue
        cond = ((b > py) != (d > py))
        xin = (c - a) * (py - b) / (d - b) + a
        inside ^= cond & (px < xin)
    total = int(inside.sum())
    glass = np.zeros((H, W), bool)
    for zid, kind, geo, _lab, _col in ZONES:
        if not zid.startswith('glass'):
            continue
        m = np.zeros((H, W), bool)
        if kind == 'rect':
            x, y, w, h = geo
            m[max(int(y), 0):int(y + h), max(int(x), 0):int(x + w)] = True
        else:
            gx = np.array([p[0] for p in geo], float)
            gy = np.array([p[1] for p in geo], float)
            gx2, gy2 = np.roll(gx, -1), np.roll(gy, -1)
            for a, b, c, d in zip(gx, gy, gx2, gy2):
                if b == d:
                    continue
                cond = ((b > py) != (d > py))
                xin = (c - a) * (py - b) / (d - b) + a
                m ^= cond & (px < xin)
        glass |= m
    glass &= inside
    return {'total': total, 'glass': int(glass.sum()),
            'share': round(int(glass.sum()) / total * 100, 1)}


AREAS = areas()


def car_svg():
    """Кузов сверху: зоны заливки и разметка.

    Все зоны обрезаны одним клипом по контуру, поэтому стыки сходятся
    сами и не требуют подгонки форм. Ровно так же устроен настоящий
    лист: жирная линия контура, серые стёкла, всё остальное белое.
    """
    def tag(kind, geo, attrs):
        if kind == 'rect':
            x, y, w, h = geo
            return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {attrs}'
        pts = ' '.join(f'{x},{y}' for x, y in geo)
        return f'<polygon points="{pts}" {attrs}'

    fills, lines = '', ''
    for zid, kind, geo, lab, col in ZONES:
        name = 'rect' if kind == 'rect' else 'polygon'
        fills += (tag(kind, geo, f'class="z" data-z="{zid}" fill="{col}">')
                  + f'<title>{lab}</title></{name}>')
        lines += tag(kind, geo, 'class="ln"/>')
    wheels = ''.join(
        f'<rect x="{x - 38}" y="{y - 15}" width="76" height="30" rx="11" class="wh"/>'
        for x, y in WHEELS)
    mirrors = ''.join(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" class="mir"/>'
        for x, y, w, h in MIRRORS)
    return (
        '<svg id="cgCar" viewBox="0 0 820 420" role="img" '
        'aria-label="Контур Changan CS35 сверху: раскрасьте кузов">'
        f'<defs><clipPath id="cgBodyClip"><path d="{BODY_D}"/></clipPath></defs>'
        f'<g class="wheels">{wheels}</g>'
        f'<g clip-path="url(#cgBodyClip)"><rect x="0" y="0" width="820" height="420" '
        f'fill="#FFFFFF"/>{fills}<g id="cgStrokes"></g></g>'
        f'<g class="lines" clip-path="url(#cgBodyClip)">{lines}</g>'
        f'<path class="body" d="{BODY_D}"/>'
        f'<g class="mirrors">{mirrors}</g>'
        '<g class="det">'
        '<path class="seam" d="M 290,64 V 122 M 290,298 V 356"/>'
        '<path class="seam" d="M 470,64 V 120 M 470,300 V 356"/>'
        '<path class="seam" d="M 596,72 C 640,84 680,102 712,124 M 596,348 '
        'C 640,336 680,318 712,296"/>'
        '<rect x="706" y="118" width="34" height="52" rx="12"/>'
        '<rect x="706" y="250" width="34" height="52" rx="12"/>'
        '<rect x="756" y="150" width="16" height="120" rx="7"/>'
        '<rect x="74" y="128" width="26" height="46" rx="9"/>'
        '<rect x="74" y="246" width="26" height="46" rx="9"/>'
                '</g></svg>')


def color():
    pens = ''.join(
        f'<button class="cg-pen{" is-on" if i == 0 else ""}" type="button" '
        f'data-pen="{c}" style="background:{c}" aria-label="Фломастер {n}"></button>'
        for i, (c, n) in enumerate(PENS))
    shots = ''.join(
        f'<figure>{pic(s, a)}<figcaption>{cap}</figcaption></figure>'
        for s, a, cap in (
            ('color-table', 'Гости раскрашивают листы за столом',
             'Столы с фломастерами стояли рядом с площадкой шоу'),
            ('scanner', 'Лист с раскраской под сканером',
             'Готовый лист клали под сканер, метки по углам ловили рисунок'),
            ('track', 'Раскрашенные машины на виртуальной трассе',
             'Через несколько секунд машина выезжала на общую трассу')))
    return (
        '<section class="cg-color" id="paint"><div class="in">'
        '<p class="kicker rv">Виртуальный тест-драйв</p>'
        '<h2 class="rv">Раскрасьте машину и выпустите её на трассу</h2>'
        '<p class="lead narrow rv">На площадке это работало так: гость получал лист '
        'с контуром машины и фломастеры, раскрашивал как хотел, лист клали под '
        'сканер, и раскрашенная машина выезжала на трассу с символикой марки, '
        'к таким же машинам других гостей. Ниже то же самое, только лист '
        'нарисован кодом. Кликните по детали кузова, чтобы залить её цветом, '
        'или возьмите фломастер и рисуйте поверх.</p>'
        '<div class="cg-paint">'
        '<div class="rv">'
        '<div class="cg-sheet"><div class="cg-sheet__marks"><span></span><span></span>'
        f'<span></span></div>{car_svg()}</div>'
        '<p class="cg-sheet__hint">Чёрные квадраты по углам настоящие: по ним '
        'сканер ловил лист</p>'
        '<div class="cg-tools">'
        f'<div class="cg-pens">{pens}</div>'
        '<div class="cg-row">'
        '<button class="cg-btn is-on" type="button" data-tool="fill">Заливка</button>'
        '<button class="cg-btn" type="button" data-tool="pen">Фломастер</button>'
        '<button class="cg-btn" type="button" data-act="random">Случайно</button>'
        '<button class="cg-btn" type="button" data-act="clear">Начать заново</button>'
        '</div>'
        '<div class="cg-row">'
        '<button class="cg-btn cg-btn--go" type="button" data-act="scan">'
        'Сканировать и выпустить на трассу</button></div>'
        '</div></div>'
        '<div class="rv"><div class="cg-track">'
        '<canvas id="cgTrack" width="960" height="560" '
        'aria-label="Трасса с раскрашенными машинами"></canvas>'
        '<div class="cg-scan" id="cgScan"></div>'
        '<div class="cg-track__cap"><span data-track-msg>Трасса идёт по кругу. '
        'Ваша машина встанет в общий поток после сканирования.</span>'
        '<b data-track-lap>круг 1</b></div></div>'
        '<p class="note" style="margin-top:14px">Соседи по трассе не выдуманы: '
        'их цвета сняты с кадров ролика, где по трассе едут машины, '
        'раскрашенные гостями вечера.</p></div>'
        '</div>'
        f'<div class="cg-color__ph rv">{shots}</div>'
        '</div></section>')


def mapping():
    shots = ''.join(
        f'<figure>{pic(s, cap)}<figcaption>{cap}</figcaption></figure>'
        for s, cap in SHOW)
    return (
        '<section class="cg-map" id="mapping"><div class="in">'
        '<p class="kicker rv">Шоу на кузове</p>'
        '<h2 class="rv">Три проектора на одну машину</h2>'
        '<p class="lead narrow rv">Вечер открывался трёхминутным световым шоу. '
        'Под него сняли форму автомобиля и собрали 3D-маску, чтобы контент '
        'ложился по кузову, а не по воздуху вокруг. Один проектор работал '
        'обратной проекцией на экран за машиной и вёл пейзаж, будто она едет. '
        'Два других светили на сам кузов.</p>'
        '<div class="cg-map__wrap">'
        '<div class="cg-scene rv" id="cgScene">'
        '<svg viewBox="0 0 700 600" role="img" aria-label="Схема расстановки '
        'проекторов вокруг автомобиля, вид сверху">'
        '<defs>'
        '<linearGradient id="cgBeamL" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#4ADEF0" stop-opacity=".42"/>'
        '<stop offset="1" stop-color="#4ADEF0" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="cgBeamR" x1="1" y1="0" x2="0" y2="0">'
        '<stop offset="0" stop-color="#FF3E9A" stop-opacity=".42"/>'
        '<stop offset="1" stop-color="#FF3E9A" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="cgBeamB" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#C9F23C" stop-opacity=".30"/>'
        '<stop offset="1" stop-color="#C9F23C" stop-opacity="0"/></linearGradient>'
        '</defs>'
        '<g id="cgBeams"></g>'
        '<g id="cgScreen"><rect x="120" y="74" width="460" height="16" rx="4"/>'
        '<text x="350" y="116" text-anchor="middle">экран, обратная проекция</text></g>'
        '<g id="cgCarTop"></g>'
        '<g id="cgProj"></g>'
        '</svg></div>'
        '<div class="cg-map__ctl">'
        '<div class="cg-ctl rv"><h3>Сколько проекторов светит на кузов</h3>'
        '<p>Машина не стена: свет от одного проектора закрывает только '
        'обращённый к нему борт, всё остальное остаётся тёмным. Второй проектор '
        'ставят не для яркости, а чтобы закрыть вторую половину кузова.</p>'
        '<div class="cg-toggle" data-group="proj">'
        '<button type="button" data-proj="1">один</button>'
        '<button type="button" class="is-on" data-proj="2">два</button></div></div>'
        '<div class="cg-ctl rv"><h3>Стёкла: плёнка или как есть</h3>'
        f'<p>Остекление занимает {str(AREAS["share"]).replace(".", ",")} % '
        'поверхности, которую видит проектор сверху и сбоку. Стекло свет '
        'не отражает, а пропускает в салон, поэтому окна заклеили белой '
        'плёнкой: иначе на месте стёкол в картинке остаются дыры.</p>'
        '<div class="cg-toggle" data-group="film">'
        '<button type="button" class="is-on" data-film="1">плёнка есть</button>'
        '<button type="button" data-film="0">без плёнки</button></div></div>'
        '<div class="cg-read">'
        '<div><b data-read="lit">0 %</b><span>кузова под картинкой</span></div>'
        '<div><b data-read="dark">0 %</b><span>остаётся тёмным или проваливается '
        'в стекло</span></div></div>'
        '<p class="note">Доли считаются по контуру кузова сверху: периметр '
        'разбит на участки, участок засчитан освещённым, если он развёрнут '
        'к включённому проектору. Остекление вычитается по площади зон.</p>'
        '</div></div>'
        '<h3 class="rv" style="margin-top:48px">Шесть кадров из трёх минут</h3>'
        '<p class="note rv" style="max-width:70ch;margin-bottom:22px">Кадры сняты '
        'с одной точки, но между дублями камера гуляла, и сводить их в один '
        'ракурс мы не стали: это шесть фотографий шоу, а не шесть состояний '
        'одного кадра.</p>'
        f'<div class="cg-show rv">{shots}</div>'
        '</div></section>')


def evening():
    hot = {'Первый блок программы', 'Второй блок программы', 'Активности'}
    rows = ''.join(
        f'<div class="cg-time__row{" hot" if p["what"] in hot else ""}">'
        f'<time>{p["from"]} – {p["to"]}</time><span>{p["what"]}</span></div>'
        for p in PROGRAM)
    shots = ''.join(
        f'<figure>{pic(s, cap)}<figcaption>{cap}</figcaption></figure>'
        for s, cap in (
            ('drums', 'Шоу китайских барабанов у автомобиля'),
            ('lanterns', 'Танец с фонарями на фоне обратной проекции'),
            ('fans', 'Танец с веерами'),
            ('crowd', 'Гости снимают шоу на телефоны'),
            ('award', 'Ведущий показывает залу раскраски участников'),
            ('dessert', 'Десерты с маркой на глазури')))
    return (
        '<section class="cg-eve"><div class="in">'
        '<p class="kicker rv">Вечер</p>'
        '<h2 class="rv">Шесть часов в дилерском центре</h2>'
        '<p class="lead narrow rv">Гостей встречали на входе и помогали заполнить '
        'анкету на тест-драйв, дальше был welcome-фуршет и виртуальный тест-драйв. '
        'Между блоками программы люди уезжали на настоящий тест-драйв '
        'и возвращались в зал.</p>'
        '<div class="cg-eve__wrap">'
        f'<div class="cg-time rv">{rows}</div>'
        f'<div class="cg-eve__grid rv">{shots}</div>'
        '</div></div></section>')


def film():
    chaps = ''.join(
        f'<button type="button" data-t="{t}"><i>{t // 60}:{t % 60:02d}</i>{name}</button>'
        for t, name in CHAPTERS)
    return (
        '<section class="cg-film"><div class="in">'
        '<p class="kicker rv">Ролик</p>'
        '<h2 class="rv">Как это выглядело</h2>'
        '<div class="cg-film__box rv">'
        f'<video id="cgVideo" controls preload="metadata" playsinline '
        f'poster="{IMG}/map-fire-640.jpg">'
        f'<source src="{VIDEO}" type="video/mp4"></video></div>'
        f'<div class="cg-chaps rv">{chaps}</div>'
        '</div></section>')


def outro():
    return (
        '<section class="cg-out"><div class="in">'
        '<p class="kicker rv">Итоги</p>'
        '<h2 class="rv">Что записали в отчёт</h2>'
        '<div class="cg-out__grid">'
        '<div class="cg-out__box rv"><h3>Сработало</h3><ul>'
        '<li>Обновлённый CS35 приняли тепло: список того, что нравилось, '
        'длиннее списка возражений</li>'
        '<li>Стенд дал дилеру 126 записей на тест-драйв с датой и временем</li>'
        '<li>Задачи проекта закрыты, уровень организации оценён высоко</li>'
        '</ul></div>'
        '<div class="cg-out__box rv"><h3>Что рекомендовали изменить</h3><ul>'
        '<li>Не ставить такие события на январь и первую половину февраля: '
        'после праздников люди ещё не восстановили бюджет</li>'
        '<li>Делать не одно событие, а серию: за один вечер до покупки '
        'доходит слишком узкая часть тех, кого удалось собрать</li>'
        '</ul></div></div>'
        '<p class="cg-out__last rv">Кейс хорош не тем, что цифры большие, '
        'а тем, что они есть на каждом шаге. Когда видно, где воронка теряет '
        'людей, следующая презентация начинается не с площадки и не с шоу, '
        'а с вопроса, сколько человек нужно собрать наверху, чтобы внизу '
        'осталось столько, сколько нужно дилеру.</p>'
        '</div></section>')


PAGE_JS = """<script>
(function(){
 'use strict';
 var ROWS=%ROWS%, DAYS=%DAYS%, FUNNEL=%FUNNEL%, ZONES=%ZONES%,
     BODY=%BODY%, POLY=%POLY%, GLASS=%GLASS%, RIVALS=%RIVALS%;
 var rmotion=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

 /* ── проявление блоков ──────────────────────────────────────────────── */
 var rv=[].slice.call(document.querySelectorAll('.cg .rv'));
 if(!('IntersectionObserver' in window)){rv.forEach(function(e){e.classList.add('on');});}
 else{
  var io=new IntersectionObserver(function(es){
   es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);}});
  },{rootMargin:'0px 0px -8% 0px',threshold:.08});
  rv.forEach(function(e){io.observe(e);});
 }

 /* ── воронка: ступень задаёт, какой ряд показан по дням ─────────────── */
 var steps=[].slice.call(document.querySelectorAll('.cg-step')),
     mode='abs', cur=0,
     pTitle=document.querySelector('[data-panel-title]'),
     pSub=document.querySelector('[data-panel-sub]'),
     pSum=document.querySelector('[data-panel-sum]');
 function drawDays(){
  var st=steps[cur], key=st.getAttribute('data-key'), row=ROWS[key];
  pTitle.textContent=FUNNEL[cur].label;
  var i,bar,val;
  if(!row){
   pSub.textContent='Событие было одно, по дням эта ступень не делится';
   for(i=0;i<7;i++){
    bar=document.querySelector('[data-b="'+i+'"]'); val=document.querySelector('[data-v="'+i+'"]');
    bar.style.height='0%'; val.textContent='';
   }
   pSum.innerHTML='В отчёте по этой ступени одна цифра: <b>'+FUNNEL[cur].value+
     '</b> из '+FUNNEL[cur-1].value+' записавшихся.';
   return;
  }
  var max=Math.max.apply(null,row), sum=row.reduce(function(a,b){return a+b;},0);
  pSub.textContent='По дням, с 27 января по 2 февраля';
  for(i=0;i<7;i++){
   bar=document.querySelector('[data-b="'+i+'"]'); val=document.querySelector('[data-v="'+i+'"]');
   var h=row[i]/max*100;
   bar.style.height=Math.max(h,1.5)+'%';
   if(mode==='abs'){val.textContent=row[i];}
   else{
    var base=key==='listen'?null:ROWS[key==='demo'?'listen':(key==='test'?'demo':'test')];
    val.textContent=base?Math.round(row[i]/base[i]*100)+'%':Math.round(row[i]/sum*100)+'%';
   }
  }
  var itog=FUNNEL[cur].value;
  pSum.innerHTML='Сумма по дням <b>'+sum+'</b>, в итоговой таблице отчёта <b>'+itog+'</b>'+
   (Math.abs(sum-itog)/itog<0.03?'. Сходится в пределах точности снятия.'
    :'. Разница '+(itog-sum)+': столько записей пришло мимо стенда.');
 }
 steps.forEach(function(st,i){
  st.addEventListener('click',function(){
   steps.forEach(function(s){s.classList.remove('is-on');});
   st.classList.add('is-on'); cur=i; drawDays();
  });
 });
 [].slice.call(document.querySelectorAll('.cg-fun [data-mode]')).forEach(function(b){
  b.addEventListener('click',function(){
   [].slice.call(document.querySelectorAll('.cg-fun [data-mode]')).forEach(function(x){
    x.classList.remove('is-on');});
   b.classList.add('is-on'); mode=b.getAttribute('data-mode'); drawDays();
  });
 });
 drawDays();
})();
</script>"""

PAINT_JS = """<script>
(function(){
 'use strict';
 var ZONES=%ZONES%, BODY=%BODY%, PENS=%PENS%, RIVALS=%RIVALS%, WHEELS=%WHEELS%;
 var svg=document.getElementById('cgCar');
 if(!svg) return;
 var strokesG=document.getElementById('cgStrokes'),
     canvas=document.getElementById('cgTrack'), ctx=canvas.getContext('2d'),
     scanEl=document.getElementById('cgScan'),
     msg=document.querySelector('[data-track-msg]'),
     lapEl=document.querySelector('[data-track-lap]');
 var pen=PENS[0][0], tool='fill', strokes=[], drawing=null;
 var paint={};                       /* id зоны -> цвет */
 ZONES.forEach(function(z){paint[z.id]=z.color;});

 /* ── инструменты ────────────────────────────────────────────────────── */
 function sel(list,el){list.forEach(function(x){x.classList.remove('is-on');});el.classList.add('is-on');}
 var pens=[].slice.call(document.querySelectorAll('.cg-pen'));
 pens.forEach(function(b){b.addEventListener('click',function(){
  pen=b.getAttribute('data-pen'); sel(pens,b);});});
 var tools=[].slice.call(document.querySelectorAll('[data-tool]'));
 tools.forEach(function(b){b.addEventListener('click',function(){
  tool=b.getAttribute('data-tool'); sel(tools,b);});});

 /* ── заливка и фломастер по кузову ──────────────────────────────────── */
 function pt(ev){
  var m=svg.getScreenCTM().inverse(),
      p=svg.createSVGPoint(); p.x=ev.clientX; p.y=ev.clientY;
  var q=p.matrixTransform(m); return [q.x,q.y];
 }
 function strokePath(s){
  var d='M '+s.pts.map(function(p){return p[0].toFixed(1)+','+p[1].toFixed(1);}).join(' L ');
  return '<path d="'+d+'" fill="none" stroke="'+s.color+'" stroke-width="'+s.w+
         '" stroke-linecap="round" stroke-linejoin="round"/>';
 }
 function renderStrokes(){
  strokesG.innerHTML=strokes.map(strokePath).join('');
 }
 svg.addEventListener('pointerdown',function(ev){
  var t=ev.target, z=t.getAttribute&&t.getAttribute('data-z');
  if(tool==='fill'){
   if(z){paint[z]=pen; t.setAttribute('fill',pen);}
   return;
  }
  ev.preventDefault();
  drawing={color:pen,w:16,pts:[pt(ev)]};
  strokes.push(drawing); renderStrokes();
  svg.setPointerCapture&&svg.setPointerCapture(ev.pointerId);
 });
 svg.addEventListener('pointermove',function(ev){
  if(!drawing) return;
  var p=pt(ev), last=drawing.pts[drawing.pts.length-1];
  if(Math.abs(p[0]-last[0])+Math.abs(p[1]-last[1])<4) return;
  drawing.pts.push(p); renderStrokes();
 });
 ['pointerup','pointercancel','pointerleave'].forEach(function(e){
  svg.addEventListener(e,function(){drawing=null;});
 });
 document.querySelector('[data-act="clear"]').addEventListener('click',function(){
  strokes=[]; renderStrokes();
  ZONES.forEach(function(z){paint[z.id]=z.color;
   var el=svg.querySelector('[data-z="'+z.id+'"]'); if(el) el.setAttribute('fill',z.color);});
  msg.textContent='Лист чистый. Раскрасьте заново и отправьте на сканер.';
 });
 document.querySelector('[data-act="random"]').addEventListener('click',function(){
  ZONES.forEach(function(z){
   var c=z.id.indexOf('glass')===0?PENS[(Math.random()*PENS.length)|0][0]
                                  :PENS[(Math.random()*PENS.length)|0][0];
   paint[z.id]=c;
   var el=svg.querySelector('[data-z="'+z.id+'"]'); if(el) el.setAttribute('fill',c);
  });
 });

 /* ── трасса ─────────────────────────────────────────────────────────── */
 var W=canvas.width, H=canvas.height, cx=W/2, cy=H/2, RA=W*0.36, RB=H*0.30, ROAD=86;
 var bg=document.createElement('canvas'); bg.width=W; bg.height=H;
 (function paintBg(){
  var g=bg.getContext('2d');
  g.fillStyle='#12281A'; g.fillRect(0,0,W,H);
  for(var i=0;i<900;i++){
   g.fillStyle='rgba(255,255,255,'+(0.012+Math.random()*0.03)+')';
   g.fillRect(Math.random()*W,Math.random()*H,2,2);
  }
  function ell(r1,r2){g.beginPath();g.ellipse(cx,cy,r1,r2,0,0,Math.PI*2);g.closePath();}
  g.lineWidth=ROAD; g.strokeStyle='#33383F'; ell(RA,RB); g.stroke();
  g.lineWidth=8; g.strokeStyle='#E8EAEE'; ell(RA+ROAD/2-6,RB+ROAD/2-6); g.stroke();
  g.strokeStyle='#E8EAEE'; ell(RA-ROAD/2+6,RB-ROAD/2+6); g.stroke();
  g.lineWidth=4; g.strokeStyle='rgba(255,255,255,.5)'; g.setLineDash([26,22]);
  ell(RA,RB); g.stroke(); g.setLineDash([]);
  g.lineWidth=16; g.strokeStyle='#1E5AA8'; ell(RA+ROAD/2+16,RB+ROAD/2+16); g.stroke();
  g.strokeStyle='#4ADEF0'; g.lineWidth=6; ell(RA-ROAD/2-14,RB-ROAD/2-14); g.stroke();
  /* стартовая клетка */
  var x0=cx+RA-ROAD/2, y0=cy, cell=11;
  for(var r=0;r<Math.floor(ROAD/cell);r++)
   for(var c=0;c<3;c++){
    g.fillStyle=((r+c)%2)?'#FFFFFF':'#14171C';
    g.fillRect(x0+r*cell, y0-cell*1.5+c*cell, cell, cell);
   }
  g.font='700 30px Golos Text, Arial, sans-serif'; g.fillStyle='rgba(255,255,255,.16)';
  g.textAlign='center'; g.fillText('CHANGAN', cx, cy-6);
  g.font='600 15px Golos Text, Arial, sans-serif'; g.fillStyle='rgba(255,255,255,.13)';
  g.fillText('виртуальный тест-драйв', cx, cy+20);
 })();

 var zonePaths={};
 ZONES.forEach(function(z){zonePaths[z.id]=new Path2D(z.d);});
 var bodyPath=new Path2D(BODY);
 function drawCar(g,x,y,ang,scale,colors,strokeList){
  g.save(); g.translate(x,y); g.rotate(ang); g.scale(scale,scale); g.translate(-417,-210);
  g.save(); g.clip(bodyPath);
  g.fillStyle='#FFFFFF'; g.fillRect(0,0,820,420);
  ZONES.forEach(function(z){g.fillStyle=colors[z.id]||z.color; g.fill(zonePaths[z.id]);});
  if(strokeList) strokeList.forEach(function(s){
   g.strokeStyle=s.color; g.lineWidth=s.w; g.lineCap='round'; g.lineJoin='round';
   g.beginPath(); s.pts.forEach(function(p,i){i?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1]);});
   g.stroke();
  });
  g.restore();
  g.fillStyle='#14171C';
  WHEELS.forEach(function(w){
   g.beginPath(); g.rect(w[0]-38,w[1]-15,76,30); g.fill();
  });
  g.lineWidth=7; g.strokeStyle='#14171C'; g.stroke(bodyPath);
  g.restore();
 }
 var cars=RIVALS.map(function(r,i){
  var col={};
  ZONES.forEach(function(z){
   col[z.id]=z.id.indexOf('glass')===0?'#7E8892':(z.id.indexOf('bumper')===0?r[1]:r[0]);
  });
  return {t:i*1.7+0.4, sp:0.19+i*0.021, lane:(i%3-1)*20, colors:col, mine:false};
 });
 var mine=null, laps=0, prevT=0;
 function pos(t,lane){
  var a=t, x=cx+(RA+lane)*Math.cos(a), y=cy+(RB+lane)*Math.sin(a);
  var dx=-(RA+lane)*Math.sin(a), dy=(RB+lane)*Math.cos(a);
  return [x,y,Math.atan2(dy,dx)];
 }
 var running=true, last=0;
 function frame(ts){
  if(!last) last=ts;
  var dt=Math.min((ts-last)/1000,0.05); last=ts;
  ctx.clearRect(0,0,W,H); ctx.drawImage(bg,0,0);
  var all=cars.concat(mine?[mine]:[]);
  all.forEach(function(c){
   if(running&&!rmotionPause) c.t+=c.sp*dt;
   var p=pos(c.t,c.lane);
   drawCar(ctx,p[0],p[1],p[2],0.155,c.colors,c.mine?c.strokes:null);
   if(c.mine){
    ctx.save(); ctx.strokeStyle='rgba(201,242,60,.9)'; ctx.lineWidth=2;
    ctx.beginPath(); ctx.arc(p[0],p[1],52,0,Math.PI*2); ctx.stroke(); ctx.restore();
   }
  });
  if(mine){
   var l=Math.floor(mine.t/(Math.PI*2));
   if(l!==laps){laps=l; lapEl.textContent='круг '+(laps+1);}
  }
  requestAnimationFrame(frame);
 }
 var rmotionPause=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 if('IntersectionObserver' in window){
  new IntersectionObserver(function(es){running=es[0].isIntersecting;},{threshold:.05})
   .observe(canvas);
 }
 requestAnimationFrame(frame);

 /* ── сканирование ───────────────────────────────────────────────────── */
 document.querySelector('[data-act="scan"]').addEventListener('click',function(){
  var sheet=document.querySelector('.cg-sheet');
  sheet.animate?sheet.animate([{transform:'none'},{transform:'translateY(14px) scale(.985)'},
   {transform:'none'}],{duration:520,easing:'ease-in-out'}):0;
  scanEl.style.transition='none'; scanEl.style.top='-40%'; scanEl.style.opacity='1';
  requestAnimationFrame(function(){
   scanEl.style.transition='top 1.05s linear, opacity .3s ease .9s';
   scanEl.style.top='100%'; scanEl.style.opacity='0';
  });
  msg.textContent='Сканируем лист...';
  setTimeout(function(){
   var col={}; ZONES.forEach(function(z){col[z.id]=paint[z.id];});
   var copy=strokes.map(function(s){return {color:s.color,w:s.w,pts:s.pts.slice()};});
   if(!mine){mine={t:0,sp:0.235,lane:0,colors:col,strokes:copy,mine:true};laps=0;}
   else{mine.colors=col; mine.strokes=copy; mine.t=0; laps=0;}
   lapEl.textContent='круг 1';
   msg.innerHTML='Ваша машина на трассе. <b>Обведена лаймовым</b>.';
  },1100);
 });
})();
</script>"""


SCENE_JS = """<script>
(function(){
 'use strict';
 var BODY=%BODY%, POLY=%POLY%, GLASS=%GLASS%;
 var scene=document.getElementById('cgScene');
 if(!scene) return;
 var beams=document.getElementById('cgBeams'),
     carG=document.getElementById('cgCarTop'),
     projG=document.getElementById('cgProj'),
     readLit=document.querySelector('[data-read="lit"]'),
     readDark=document.querySelector('[data-read="dark"]');
 var nProj=2, film=1;
 var SC=0.36, CX=350, CY=330;
 /* машина стоит носом к экрану: контур поворачивается на -90 градусов */
 function tp(p){
  var x=(p[0]-420)*SC, y=(p[1]-210)*SC;
  return [CX+y, CY-x];
 }
 var pts=POLY.map(tp);
 var PROJ=[{x:92,y:520,c:'#4ADEF0',g:'url(#cgBeamL)',name:'проектор слева'},
           {x:608,y:520,c:'#FF3E9A',g:'url(#cgBeamR)',name:'проектор справа'}];
 var BACK={x:350,y:14,c:'#C9F23C',g:'url(#cgBeamB)',name:'третий проектор: пейзаж на экран'};

 function segments(){
  var out=[], total=0, lit=0;
  for(var i=0;i<pts.length;i++){
   var a=pts[i], b=pts[(i+1)%pts.length];
   var dx=b[0]-a[0], dy=b[1]-a[1], len=Math.hypot(dx,dy);
   if(!len) continue;
   total+=len;
   var nx=dy/len, ny=-dx/len, mx=(a[0]+b[0])/2, my=(a[1]+b[1])/2, col=null;
   for(var k=0;k<nProj;k++){
    var p=PROJ[k], vx=p.x-mx, vy=p.y-my, vl=Math.hypot(vx,vy);
    if((nx*vx+ny*vy)/vl>0.26){col=p.c;break;}
   }
   if(col) lit+=len;
   out.push({a:a,b:b,c:col});
  }
  return {segs:out, share:lit/total};
 }

 function draw(){
  /* лучи */
  var html='';
  for(var k=0;k<nProj;k++){
   var p=PROJ[k];
   var l=-1e9,r=1e9,minP=null,maxP=null,best=-1e9,worst=1e9;
   pts.forEach(function(q){
    var ang=Math.atan2(q[1]-p.y,q[0]-p.x);
    if(ang>best){best=ang;maxP=q;}
    if(ang<worst){worst=ang;minP=q;}
   });
   var ext=2.1;
   function far(q){return [p.x+(q[0]-p.x)*ext,p.y+(q[1]-p.y)*ext];}
   var f1=far(minP), f2=far(maxP);
   html+='<polygon points="'+p.x+','+p.y+' '+f1[0]+','+f1[1]+' '+f2[0]+','+f2[1]+
         '" fill="'+p.g+'"/>';
  }
  var bf=BACK;
  html+='<polygon points="'+bf.x+','+bf.y+' 150,520 550,520" fill="'+bf.g+'"/>';
  beams.innerHTML=html;

  /* машина: серый силуэт, поверх контур цветом того проектора,
     который этот участок видит; тёмный участок значит «сюда не светит» */
  var r=segments(), share=r.share, eff=film?share:share*(1-GLASS/100);
  var glassOp=film?'1':'.2';
  var body='<path d="'+BODY+'" class="cgcar"/>';
  var inner='<rect x="250" y="118" width="220" height="184" class="cgglass" opacity="'+
   glassOp+'"/><polygon points="470,118 556,88 556,332 470,302" class="cgglass" opacity="'+
   glassOp+'"/><polygon points="178,96 250,116 250,304 178,324" class="cgglass" opacity="'+
   glassOp+'"/>';
  var edge=r.segs.map(function(s){
   return '<line x1="'+s.a[0].toFixed(1)+'" y1="'+s.a[1].toFixed(1)+'" x2="'+
    s.b[0].toFixed(1)+'" y2="'+s.b[1].toFixed(1)+'" stroke="'+(s.c||'#2A3038')+
    '" stroke-width="9" stroke-linecap="round"/>';
  }).join('');
  carG.innerHTML='<g transform="translate('+CX+','+CY+') rotate(-90) scale('+SC+') '+
   'translate(-420,-210)">'+body+inner+'</g>'+edge+
   '<text x="'+CX+'" y="'+(CY+178)+'" text-anchor="middle" class="cglab">'+
   'CS35 на подиуме, вид сверху</text>';

  /* проекторы */
  var ph='';
  for(var j=0;j<PROJ.length;j++){
   var q=PROJ[j], off=j<nProj;
   ph+='<g opacity="'+(off?1:.3)+'"><rect x="'+(q.x-26)+'" y="'+(q.y-14)+
       '" width="52" height="28" rx="6" fill="'+(off?q.c:'#3A414C')+'"/>'+
       '<text x="'+q.x+'" y="'+(q.y+34)+'" text-anchor="middle" class="cglab">'+
       q.name+'</text></g>';
  }
  ph+='<g><rect x="'+(BACK.x-26)+'" y="'+(BACK.y-4)+'" width="52" height="24" rx="6" fill="'+
      BACK.c+'"/><text x="'+BACK.x+'" y="'+(BACK.y+46)+'" text-anchor="middle" '+
      'class="cglab">третий проектор: пейзаж на экран</text></g>';
  projG.innerHTML=ph;

  readLit.textContent=Math.round(eff*100)+' %';
  readDark.textContent=Math.round((1-eff)*100)+' %';
 }
 [].slice.call(scene.parentNode.parentNode.querySelectorAll('[data-proj]')).forEach(function(b){
  b.addEventListener('click',function(){
   [].slice.call(document.querySelectorAll('[data-proj]')).forEach(function(x){
    x.classList.remove('is-on');});
   b.classList.add('is-on'); nProj=+b.getAttribute('data-proj'); draw();
  });
 });
 [].slice.call(document.querySelectorAll('[data-film]')).forEach(function(b){
  b.addEventListener('click',function(){
   [].slice.call(document.querySelectorAll('[data-film]')).forEach(function(x){
    x.classList.remove('is-on');});
   b.classList.add('is-on'); film=+b.getAttribute('data-film'); draw();
  });
 });
 draw();
})();
</script>"""

FILM_JS = """<script>
(function(){
 'use strict';
 var v=document.getElementById('cgVideo');
 if(!v) return;
 var bs=[].slice.call(document.querySelectorAll('.cg-chaps button'));
 bs.forEach(function(b){
  b.addEventListener('click',function(){
   var t=+b.getAttribute('data-t');
   try{v.currentTime=t;}catch(e){}
   v.play&&v.play().catch(function(){});
  });
 });
 v.addEventListener('timeupdate',function(){
  var t=v.currentTime, on=0;
  bs.forEach(function(b,i){if(+b.getAttribute('data-t')<=t) on=i;});
  bs.forEach(function(b,i){b.classList.toggle('is-on',i===on);});
 });
})();
</script>"""

SCENE_CSS = """<style id="cg-scene-css">
.cg-scene .cgcar{fill:#E7EBF0;stroke:#0C1017;stroke-width:8}
.cg-scene .cgglass{fill:#94A0AE}
.cg-scene text{font:600 12px 'Golos Text',Arial,sans-serif;fill:rgba(255,255,255,.6)}
.cg-scene #cgScreen rect{fill:#E7EBF0;opacity:.9}
.cg-scene .cglab{font-size:12px}
</style>"""


BREADCRUMB_LD = (
    '<script type="application/ld+json">{"@context":"https://schema.org",'
    '"@type":"BreadcrumbList","itemListElement":['
    '{"@type":"ListItem","position":1,"name":"Главная","item":"https://hand-marketing.ru/"},'
    '{"@type":"ListItem","position":2,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
    '{"@type":"ListItem","position":3,"name":"Event","item":"https://hand-marketing.ru/event/"},'
    '{"@type":"ListItem","position":4,"name":"Презентация Changan CS35",'
    f'"item":"{URL}"}}]}}</script>')


def zones_json():
    """Зоны кузова для JS: и SVG, и canvas на трассе рисуют одни и те же
    пути, поэтому машина на трассе совпадает с листом до пикселя."""
    out = []
    for zid, kind, geo, lab, col in ZONES:
        if kind == 'rect':
            x, y, w, h = geo
            d = f'M {x},{y} H {x + w} V {y + h} H {x} Z'
        else:
            d = 'M ' + ' L '.join(f'{x},{y}' for x, y in geo) + ' Z'
        out.append({'id': zid, 'd': d, 'color': col, 'label': lab})
    return out


def css():
    out = CSS1 + CSS2 + CSS3 + SCENE_CSS
    for k, v in (('%INK%', PAL['ink']), ('%INK2%', PAL['ink2']),
                 ('%BLUE%', PAL['blue']), ('%BLUE2%', PAL['blue2']),
                 ('%LIME%', PAL['lime']), ('%MAG%', PAL['mag']),
                 ('%CYAN%', PAL['cyan']), ('%RED%', PAL['red']),
                 ('%PAPER%', PAL['paper']), ('%SAND%', PAL['sand'])):
        out = out.replace(k, v)
    return out


def scripts():
    j = json.dumps
    poly = [[round(x, 1), round(y, 1)] for x, y in _bezier_poly(step=0.08)]
    subs = {
        '%ROWS%': j(ROWS), '%DAYS%': j(DAYS, ensure_ascii=False),
        '%FUNNEL%': j(FUNNEL, ensure_ascii=False),
        '%ZONES%': j(zones_json(), ensure_ascii=False),
        '%BODY%': j(BODY_D), '%POLY%': j(poly),
        '%GLASS%': j(AREAS['share']), '%PENS%': j(PENS, ensure_ascii=False),
        '%WHEELS%': j(WHEELS),
        '%RIVALS%': j(MAP['rivals']),
    }
    out = PAGE_JS + PAINT_JS + SCENE_JS + FILM_JS
    for k, v in subs.items():
        out = out.replace(k, v)
    return out


def page():
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
            f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/map-fire.jpg">'
            '<link rel="stylesheet" href="/fonts/philosopher-golos.css">'
            + rc.FONT + rc.CSS + css() + METRIKA + '</head><body>')
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="cg">{hero()}{two()}{funnel()}{stand()}'
            f'{voices()}{color()}{mapping()}{evening()}{film()}{outro()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{scripts()}{BREADCRUMB_LD}'
            '</body></html>')
    return head + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'event', 'changan')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
