#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/rgd/history/index.html: кейс «История успеха ЦМ РЖД».

Материал один: media/transrzhd.mp4 — фильм на 3:54, снятый к десятилетию
Центральной дирекции по управлению терминально-складским комплексом, филиала
ОАО «РЖД». Три съёмочные группы работали параллельно в Москве, Санкт-Петербурге
и Калининграде, съёмка с земли и с квадрокоптера, графика собрана из
презентации дирекции, финал закрывает синхрон начальника дирекции.

Идея страницы. В фильме услуги дирекции показаны так, как они лежат в её
презентации: ряд шестиугольников с подписями. Мы развернули этот ряд обратно
в место, где услуги происходят.

  • «Грузовой двор» — главная механика. План терминала сверху нарисован
    кодом (пути, козловой кран, штабели, крытый склад, рефплощадка, зона СВХ,
    весовая с воротами, пункт промывки), на нём семь остановок по числу услуг
    со слайда. Выбор остановки ведёт контейнер по двору, подсвечивает зону,
    ставит рядом кадр и перематывает плеер. У трёх услуг кадр натурный,
    у четырёх — фотография из слайда: в фильме их живьём не снимали, и на
    схеме это помечено. Такой механики (план площадки с проводкой объекта
    по нему) на сайте не было.
  • Линейка колеи: в фильме поверх площадки лежит размер, который меняется
    с 1520 на 1435. Ползунок повторяет этот кадр и объясняет, почему
    единственный названный в фильме терминал — калининградский.
  • Паспорт дирекции: семь экранных плашек с цифрами, каждая перематывает
    плеер на свою секунду.
  • Миллион вагонов: та же цифра с плашки, пересчитанная в длину сцепки
    (1 000 000 × 14 м ≈ 14 000 км, полторы длины Транссиба).

Цифры, названия, должности и списки сняты с экранных плашек и слайдов
фильма, ничего не додумано. Палитра снята с заставки: красный ОАО «РЖД»,
синий кран, серый бетон площадки.

Шрифты: Podkova (слэб, интонация вокзальной таблички) + Istok Web.

Ассеты: mirror/images/rgd-history/ (scripts/rgd-history-assets.py).

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

IMG = '/images/rgd-history'
VIDEO = '/media/transrzhd.mp4'          # источник: scripts/a2/video_map.json
URL = 'https://hand-marketing.ru/video/rgd/history/'

DUR = 233.9            # ffprobe
SHOTS = 117            # планов в фильме (детектор склеек ffmpeg scene>0.3)

# ─── семь услуг со слайда «Услуги ЦМ» (0:25) ────────────────────────────────
# name — дословно со слайда; x,y — место на плане двора; sec — секунда фильма,
# на которую перематывает плеер; a,b — отрезок, по которому остановка
# подсвечивается во время воспроизведения; shot=True — кадр натурной съёмки,
# False — фотография из самого слайда (живьём услугу в фильме не снимали)
STOPS = [
    ('load', 'Погрузка и выгрузка грузов',
     'из вагонов, платформ, контейнеров, в том числе танк-контейнеров '
     'на терминале ЦМ',
     445, 150, 'gantry', 117.0, 115.6, 118.6, True,
     'Козловой кран снимает контейнер с платформы. Снято на терминале '
     'в парке путей: кран идёт по подкрановым путям вдоль штабеля.'),
    ('wash', 'Очистка и промывка вагонов',
     'вагонов, контейнеров, включая танк-контейнеры',
     985, 105, 'h-wash', 25.0, 22.4, 26.2, False,
     'Единственное изображение этой услуги в фильме это фотография на слайде '
     'дирекции: крытый вагон под струёй на пункте промывки.'),
    ('store', 'Хранение и складская обработка грузов',
     'крытый склад дирекции: приём, подсортировка, выдача',
     195, 360, 'storage', 141.0, 139.5, 143.5, True,
     'Кадр с крытого склада: паллеты в штабелях, электропогрузчик, '
     'рабочий с рохлей разбирает партию тарно-штучного груза.'),
    ('reefer', 'Хранение рефконтейнеров',
     'с подключением к сети на площадке терминала',
     780, 320, 'h-reefer', 25.0, 22.4, 26.2, False,
     'Ряд рефконтейнеров с включёнными агрегатами. В натурной съёмке фильма '
     'этой услуги нет, кадр взят из слайда дирекции.'),
    ('svh', 'Услуги складов временного хранения',
     'груз под таможенным контролем на территории двора',
     215, 545, 'h-svh', 25.0, 22.4, 26.2, False,
     'Внутренний вид склада временного хранения со слайда дирекции. '
     'Отдельного кадра СВХ в фильме нет.'),
    ('truck', 'Завоз, вывоз грузов автотранспортом',
     'от двери клиента до двора и обратно',
     1080, 540, 'truck', 27.5, 26.6, 29.4, True,
     'Контейнер MAERSK опускают на автопоезд. Снято с земли на площадке '
     'у выезда с терминала.'),
    ('mobile', 'Предоставление услуг мобильными бригадами',
     'бригада с техникой выезжает на пути клиента',
     1165, 345, 'h-mobile', 25.0, 22.4, 26.2, False,
     'Автокран мобильной бригады на слайде дирекции. Выезд бригады '
     'в фильме не снимали.'),
]

# ─── экранные плашки с цифрами: (слаг, число, подпись, кадр, секунда) ────────
NUMBERS = [
    ('found', '2009', 'год, в котором образована дирекция', 'found', 14.6),
    ('yards', '750+', 'грузовых дворов', 'n750', 30.8),
    ('objects', '5300', 'объектов недвижимого имущества', 'n5300', 34.2),
    ('people', '7000', 'профессиональных сотрудников', 'n7000', 36.6),
    ('tech', '2000', 'единиц погрузочной техники', 'n2000', 40.0),
    ('tons', '100 млн+', 'тонн грузов', 'n100', 52.4),
    ('wagons', '1 000 000', 'вагонов', 'n1mln', 55.4),
]

# ─── слайд «Перерабатываемые грузы» (0:46-0:49), порядок как на слайде ───────
CARGO = ['щебень', 'уголь', 'контейнеры', 'тяжеловесные грузы', 'металлы',
         'трубы', 'негабаритные грузы', 'автомобили', 'лесоматериалы круглые',
         'пиломатериалы', 'тарно-штучные грузы', 'биг бэги', 'контрейлеры']

# ─── карта сети (1:09-1:13): подписи городов в порядке с запада на восток ────
CITIES = ['Калининград', 'Санкт-Петербург', 'Москва', 'Ярославль',
          'Нижний Новгород', 'Воронеж', 'Самара', 'Екатеринбург', 'Челябинск',
          'Новосибирск', 'Красноярск', 'Иркутск', 'Чита', 'Хабаровск',
          'Находка']

# ─── коллаж крупных строек (1:14-1:24), дословно с экрана ───────────────────
BUILDS = [
    'Железнодорожный подход к порту Тамань',
    'Строительство и участие в модернизации федеральных автомобильных дорог',
    'Газопровод «Сила Сибири»',
    'Олимпийские игры-2014 в г. Сочи',
    'Увеличение мощностей морских портов Российской Федерации',
]

# ─── плитки ЭТП «Грузовые перевозки» (2:03), дословно с экрана ──────────────
ETP = ['Перевозка от станции до станции', 'Перевозка от двери до двери',
       'Терминальные услуги', 'Поиск схем и чертежей погрузки',
       'Торги лотами подвижного состава', 'Торги лотами грузов']

# ─── что мы сделали ─────────────────────────────────────────────────────────
CRAFT = [
    ('Три группы в трёх городах',
     'Москва, Санкт-Петербург и Калининград снимались параллельно, тремя '
     'группами. Сеть, растянутую на страну, иначе не снять в один период, '
     'а фильму нужны были разные типы дворов: контейнерный, складской '
     'и угольный.'),
    ('Земля и воздух',
     'Обычная съёмка и квадрокоптер. Масштаб терминала читается только сверху: '
     'парк путей, штабели, кран и автопоезда в одном кадре.'),
    ('Графика из презентации дирекции',
     'Услуги, перерабатываемые грузы, карта сети и коллаж строек взяты '
     'из материалов клиента и собраны в экранные слайды, а цифры разложены '
     'плашками поверх натурных кадров.'),
    ('Руководитель вместо диктора',
     'Об итогах десяти лет говорит начальник дирекции, а не закадровый голос: '
     'финальный синхрон записан на рабочем месте, в кадре видна аппаратная.'),
    (f'{SHOTS} планов на 3:54',
     'Средняя длина плана 2,0 секунды: фильм собран короткими планами, чтобы '
     'за четыре минуты уместились двор, техника, люди, цифры и география.'),
]


def mmss(sec):
    sec = int(round(sec))
    return f'{sec // 60}:{sec % 60:02d}'


# ─── план грузового двора: рисуется кодом, а не картинкой ───────────────────
BOX_DY = 34          # контейнер ставим ниже метки остановки, чтобы её не закрывать
PALETTE = ['#C3402F', '#2E6E9E', '#D8A32C', '#3F7A4E', '#8C8F94', '#B75A2A',
           '#4A5C6A', '#A8B0B6']


def stack(x, y, cols, rows, w=48, h=24, gap=5, seed=7):
    """Штабель контейнеров: детерминированная раскладка цветов."""
    out, n = [], seed
    for r in range(rows):
        for c in range(cols):
            n = (n * 1103515245 + 12345) % 2147483648
            col = PALETTE[n % len(PALETTE)]
            out.append(f'<rect x="{x + c * (w + gap)}" y="{y + r * (h + gap)}" '
                       f'width="{w}" height="{h}" rx="2" fill="{col}" '
                       f'fill-opacity=".92"/>')
    return ''.join(out)


def track(y, x1, x2):
    """Путь: две нитки рельсов и шпалы."""
    ties = ''.join(f'<line x1="{x}" y1="{y - 9}" x2="{x}" y2="{y + 9}"/>'
                   for x in range(x1 + 6, x2, 20))
    return (f'<g class="rz-track"><g class="rz-tie">{ties}</g>'
            f'<line x1="{x1}" y1="{y - 5}" x2="{x2}" y2="{y - 5}"/>'
            f'<line x1="{x1}" y1="{y + 5}" x2="{x2}" y2="{y + 5}"/></g>')


def wagon(x, y, w, kind='flat', box='#C3402F'):
    """Вагон на пути: платформа с контейнером или полувагон."""
    if kind == 'flat':
        return (f'<g><rect x="{x}" y="{y - 11}" width="{w}" height="22" rx="2" '
                f'fill="#5A6068"/><rect x="{x + 6}" y="{y - 9}" width="{w - 12}" '
                f'height="18" rx="1.5" fill="{box}" fill-opacity=".92"/></g>')
    return (f'<g><rect x="{x}" y="{y - 11}" width="{w}" height="22" rx="2" '
            f'fill="#454B52"/><rect x="{x + 4}" y="{y - 7}" width="{w - 8}" '
            f'height="14" rx="1" fill="#23272C"/></g>')


def plan_svg():
    p = []
    # площадка
    p.append('<rect x="0" y="0" width="1200" height="660" fill="#E7E3DA"/>')
    p.append('<rect x="24" y="238" width="700" height="216" rx="4" fill="#D8D3C7"/>')
    p.append('<rect x="960" y="430" width="216" height="200" rx="4" fill="#D8D3C7"/>')

    # ── пути и приёмо-отправочный парк ────────────────────────────────────
    p.append(track(105, 30, 780))
    p.append(track(150, 30, 780))
    p.append(track(195, 30, 640))
    p.append(track(105, 800, 1150))          # тупик пункта промывки
    p.append(wagon(250, 150, 120, box='#2E6E9E') + wagon(380, 150, 120, box='#C3402F')
             + wagon(510, 150, 120, box='#D8A32C'))
    p.append(wagon(60, 195, 110, 'open') + wagon(180, 195, 110, 'open')
             + wagon(300, 195, 110, 'open'))
    p.append(wagon(860, 105, 120, 'open'))

    # ── козловой кран над путями ──────────────────────────────────────────
    p.append('<g class="rz-crane">'
             '<rect x="326" y="58" width="13" height="176" rx="3"/>'
             '<rect x="556" y="58" width="13" height="176" rx="3"/>'
             '<rect x="320" y="118" width="255" height="15" rx="3"/>'
             '<rect x="430" y="112" width="34" height="27" rx="3" fill="#C3402F"/>'
             '</g>')

    # ── контейнерная площадка ─────────────────────────────────────────────
    p.append(stack(300, 272, 6, 4))
    p.append('<text class="rz-lbl" x="300" y="262">контейнерная площадка</text>')

    # ── крытый склад ──────────────────────────────────────────────────────
    p.append('<g id="z-store" class="rz-zone">'
             '<rect x="108" y="280" width="176" height="160" rx="6" fill="#C6C0B2"/>'
             '<path d="M120 300h152M120 322h152M120 344h152M120 366h152" '
             'stroke="#8E877A" stroke-width="2"/>'
             '<rect x="266" y="312" width="26" height="34" rx="2" fill="#23272C"/>'
             '<rect x="266" y="366" width="26" height="34" rx="2" fill="#23272C"/>'
             '</g>'
             '<text class="rz-lbl" x="108" y="270">крытый склад</text>')

    # ── рефплощадка ───────────────────────────────────────────────────────
    ref = ''.join(f'<rect x="{700 + i * 30}" y="272" width="24" height="76" rx="2" '
                  f'fill="#F1F0EC" stroke="#9AA1A8"/>'
                  f'<circle cx="{712 + i * 30}" cy="286" r="5" fill="#2E6E9E"/>'
                  for i in range(6))
    p.append(f'<g id="z-reefer" class="rz-zone">{ref}'
             '<rect x="694" y="358" width="168" height="14" rx="3" fill="#8C8F94"/>'
             '<rect x="866" y="290" width="34" height="82" rx="4" fill="#4A5C6A"/>'
             '</g>'
             '<text class="rz-lbl" x="694" y="262">рефконтейнеры и подстанция</text>')

    # ── склад временного хранения ─────────────────────────────────────────
    p.append('<g id="z-svh" class="rz-zone">'
             '<rect x="108" y="486" width="212" height="126" rx="6" fill="none" '
             'stroke="#7B8288" stroke-width="3" stroke-dasharray="9 7"/>'
             '<rect x="130" y="508" width="128" height="82" rx="4" fill="#CFCABD"/>'
             '<path d="M320 548h44" stroke="#C3402F" stroke-width="6"/>'
             '</g>'
             '<text class="rz-lbl" x="108" y="476">склад временного хранения</text>')

    # ── пункт промывки ────────────────────────────────────────────────────
    p.append('<g id="z-wash" class="rz-zone">'
             '<rect x="880" y="60" width="212" height="92" rx="6" fill="none" '
             'stroke="#2E6E9E" stroke-width="3"/>'
             '<path d="M900 70v72M940 70v72M980 70v72M1020 70v72M1060 70v72" '
             'stroke="#2E6E9E" stroke-opacity=".45" stroke-width="2"/>'
             '</g>'
             '<text class="rz-lbl" x="880" y="52">пункт промывки</text>')

    # ── дорога, весовая и ворота ──────────────────────────────────────────
    road = 'M196 452V468H1084V498'
    p.append(f'<path class="rz-road" d="{road}"/>')
    p.append('<path class="rz-road" d="M366 468V548H336"/>')
    p.append(f'<path class="rz-road-line" d="{road}"/>')
    p.append('<g id="z-truck" class="rz-zone">'
             '<rect x="1000" y="470" width="152" height="120" rx="6" fill="#CFCABD"/>'
             '<rect x="1016" y="492" width="60" height="34" rx="3" fill="#4A5C6A"/>'
             '<rect x="1016" y="540" width="120" height="30" rx="3" fill="#8C8F94"/>'
             '<path d="M1140 470v120" stroke="#C3402F" stroke-width="5"/>'
             '</g>'
             '<text class="rz-lbl" x="1000" y="462">весовая и ворота</text>')

    # ── выезд мобильной бригады за территорию ─────────────────────────────
    p.append('<g id="z-mobile" class="rz-zone">'
             '<path d="M1120 452C1160 430 1170 400 1168 366" fill="none" '
             'stroke="#C3402F" stroke-width="3" stroke-dasharray="8 6"/>'
             '<path d="M1160 372l8-22 9 21z" fill="#C3402F"/>'
             '<rect x="1132" y="300" width="62" height="34" rx="4" fill="#C3402F"/>'
             '<rect x="1140" y="288" width="28" height="16" rx="3" fill="#8C8F94"/>'
             '</g>')

    # ── зона погрузки-выгрузки: подсвечивается участок под краном ─────────
    p.append('<g id="z-load" class="rz-zone">'
             '<rect x="318" y="76" width="262" height="150" rx="6" fill="none" '
             'stroke="#C3402F" stroke-width="3" stroke-dasharray="10 6"/>'
             '</g>')

    # ── остановки ─────────────────────────────────────────────────────────
    for i, (sid, *_rest) in enumerate(STOPS):
        x, y = STOPS[i][3], STOPS[i][4]
        p.append(f'<g class="rz-pin" id="pin-{sid}" data-i="{i}" tabindex="0" '
                 f'role="button" aria-label="Остановка {i + 1}">'
                 f'<circle cx="{x}" cy="{y}" r="19"/>'
                 f'<text x="{x}" y="{y + 6}">{i + 1}</text></g>')

    # контейнер, который ходит по двору
    p.append(f'<g id="rz-box" transform="translate({STOPS[0][3]},{STOPS[0][4] + BOX_DY})">'
             '<rect x="-26" y="-14" width="52" height="28" rx="3" fill="#C3402F" '
             'stroke="#fff" stroke-width="3"/>'
             '<path d="M-16-14v28M-6-14v28M4-14v28M14-14v28" stroke="#fff" '
             'stroke-opacity=".55" stroke-width="2"/></g>')

    return ('<svg class="rz-plan" viewBox="0 0 1200 660" role="img" '
            'aria-label="Схема грузового двора: пути, козловой кран, '
            'контейнерная площадка, крытый склад, рефконтейнеры, склад '
            'временного хранения, пункт промывки, весовая и ворота">'
            + ''.join(p) + '</svg>')


CSS = """<style>
:root{
 --red:#C3402F;      /* красный ОАО «РЖД» с заставки фильма */
 --deep:#171B21;     /* графит */
 --steel:#4A5C6A;
 --blue:#2E6E9E;     /* синий кранов и заставки */
 --sand:#EFEBE2;     /* бетон площадки */
 --paper:#FFFFFF;
 --ink:#191C21;
 --mut:#6B7178;
 --line:rgba(25,28,33,.14);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);
 font:400 17px/1.62 'Istok Web',system-ui,sans-serif;overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
.rz{max-width:100%;overflow:hidden}
.rz h1,.rz h2,.rz h3,.rz .num,.rz .kick,.rz .tc{font-family:'Podkova',Georgia,serif}
.rz h1,.rz h2,.rz h3{font-weight:700}
.rz section{padding:clamp(50px,7vw,96px) 0}
.rz .in{width:min(1200px,92vw);margin:0 auto}
.rz .nar{width:min(760px,92vw);margin:0 auto}
.rz h2{font-size:clamp(26px,4.3vw,46px);line-height:1.06;margin:0 0 16px;
 letter-spacing:-.01em}
.rz h3{font-size:clamp(18px,2.2vw,23px);line-height:1.18;margin:0 0 8px}
.rz p{margin:0 0 14px}
.rz .lead{font-size:clamp(17px,1.85vw,20px);color:#3A4048;max-width:64ch}
.rz .mut{color:var(--mut)}
.rz .kick{font-size:13px;letter-spacing:.22em;text-transform:uppercase;
 color:var(--red);margin:0 0 12px;font-weight:700}
.rz .cap{font-size:14px;color:var(--mut);margin:8px 0 0}
.rz .sand{background:var(--sand)}
.rz a{color:inherit}
.rz-r{opacity:0;transform:translateY(16px);transition:opacity .5s,transform .5s}
.rz-r.is-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rz-r{opacity:1;transform:none;transition:none}
 #rz-box{transition:none!important}}

/* ── шапка ─────────────────────────────────────────────────────────────── */
.rz-hero{position:relative;background:var(--deep);color:#fff;
 padding:clamp(40px,5.4vw,68px) 0 clamp(40px,5.4vw,64px);overflow:hidden}
.rz-hero__bg{position:absolute;inset:0;background:url(%IMG%/poster.jpg) center/cover;
 opacity:.3}
.rz-hero__bg::after{content:'';position:absolute;inset:0;
 background:linear-gradient(102deg,rgba(23,27,33,.94) 34%,rgba(23,27,33,.5) 100%)}
.rz-hero .in{position:relative}
.rz-hero__crumb{font-size:13px;letter-spacing:.16em;text-transform:uppercase;
 color:rgba(255,255,255,.72);margin:0 0 18px;font-family:'Podkova',Georgia,serif}
.rz-hero__crumb a{color:inherit;text-decoration:none;
 border-bottom:1px solid rgba(255,255,255,.36)}
.rz-hero h1{font-size:clamp(32px,6vw,68px);line-height:1;margin:0 0 8px;
 letter-spacing:-.015em;max-width:16ch}
.rz-hero__sub{font-size:clamp(16px,2vw,21px);color:rgba(255,255,255,.78);
 max-width:52ch;margin:0 0 22px}
.rz-hero__grid{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);
 gap:clamp(24px,4vw,52px);align-items:end}
.rz-hero__shot{border-radius:14px;overflow:hidden;box-shadow:0 24px 54px rgba(0,0,0,.5)}
.rz-hero__meta{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;
 margin-top:clamp(22px,3vw,32px)}
.rz-hero__meta div{background:rgba(255,255,255,.07);
 border:1px solid rgba(255,255,255,.18);border-radius:11px;padding:12px 13px}
.rz-hero__meta b{display:block;font-family:'Podkova',Georgia,serif;font-weight:700;
 font-size:clamp(19px,2.4vw,27px);line-height:1}
.rz-hero__meta span{display:block;font-size:13px;color:rgba(255,255,255,.74);
 margin-top:5px;line-height:1.3}

/* ── бриф ──────────────────────────────────────────────────────────────── */
.rz-brief{display:grid;grid-template-columns:repeat(auto-fit,minmax(268px,1fr));
 gap:clamp(20px,3vw,34px);margin-top:28px}
.rz-brief__it b{display:block;width:36px;height:4px;background:var(--red);
 margin:0 0 14px}
.rz-brief__it p{color:#3E444B;margin:0}

/* ── двор: главная механика ────────────────────────────────────────────── */
.rz-yard{background:var(--deep);color:#fff}
.rz-yard h2{color:#fff}
.rz-yard .lead{color:rgba(255,255,255,.8)}
.rz-yard .kick{color:#F0A08E}
.rz-stage{margin:clamp(22px,3vw,32px) 0 20px}
@media(min-width:981px) and (min-height:640px){
 .rz-stage{position:sticky;top:12px;z-index:6}}
.rz-stage video{width:100%;display:block;border-radius:12px;background:#000;
 box-shadow:0 18px 40px rgba(0,0,0,.5)}
.rz-yard__grid{display:grid;grid-template-columns:minmax(0,1fr) 306px;gap:18px;
 align-items:start}
.rz-planwrap{background:#0F1216;border:1px solid rgba(255,255,255,.14);
 border-radius:14px;padding:10px;overflow-x:auto}
.rz-hint{display:none;font-size:13.5px;color:rgba(255,255,255,.6);margin:8px 2px 0}
@media(max-width:820px){.rz-hint{display:block}}
.rz-plan{display:block;width:100%;min-width:700px;height:auto;border-radius:8px}
.rz-track line{stroke:#8A9299;stroke-width:3}
.rz-tie line{stroke:#7B7468;stroke-width:5}
.rz-crane rect{fill:#2E6E9E}
.rz-lbl{font:600 15px 'Istok Web',sans-serif;fill:#5D636A}
.rz-road{stroke:#B9B3A6;stroke-width:26;fill:none;stroke-linejoin:round}
.rz-road-line{stroke:#EFEBE2;stroke-width:2;fill:none;stroke-dasharray:14 12}
.rz-zone{opacity:.98}
.rz-zone.is-on{filter:drop-shadow(0 0 12px rgba(195,64,47,.95))}
.rz-pin circle{fill:#171B21;stroke:#fff;stroke-width:3;cursor:pointer;
 transition:fill .18s,r .18s}
.rz-pin text{font:700 19px 'Podkova',serif;fill:#fff;text-anchor:middle;
 pointer-events:none}
.rz-pin:hover circle,.rz-pin:focus circle{fill:var(--red)}
.rz-pin.is-on circle{fill:var(--red);stroke:#fff}
.rz-pin.is-live circle{stroke:#F0A08E}
.rz-pin:focus{outline:none}
#rz-box{transition:transform .62s cubic-bezier(.55,.06,.3,1)}
.rz-side{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.16);
 border-radius:14px;padding:14px}
.rz-side img{width:100%;border-radius:9px;aspect-ratio:16/9;object-fit:cover;
 background:#000}
.rz-side .tc{font-size:19px;color:#F0A08E;margin:12px 0 2px}
.rz-side h3{font-size:18px;margin:0 0 6px;color:#fff}
.rz-side p{font-size:14.5px;line-height:1.5;color:rgba(255,255,255,.8);margin:0}
.rz-badge{display:inline-block;font-size:12px;letter-spacing:.08em;
 text-transform:uppercase;border-radius:99px;padding:4px 10px;margin:0 0 10px;
 font-weight:700}
.rz-badge.shot{background:rgba(195,64,47,.24);color:#F2A493;
 border:1px solid rgba(242,164,147,.5)}
.rz-badge.slide{background:rgba(46,110,158,.24);color:#9CC6E4;
 border:1px solid rgba(156,198,228,.5)}
.rz-stops{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
 gap:10px;margin-top:18px;padding:0;list-style:none}
.rz-stops button{width:100%;height:100%;text-align:left;cursor:pointer;
 background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.16);
 color:#fff;border-radius:12px;padding:12px 14px;font:400 15px/1.4 'Istok Web',sans-serif;
 transition:background .18s,border-color .18s}
.rz-stops button:hover,.rz-stops button:focus-visible{background:rgba(255,255,255,.14)}
.rz-stops button.is-on{background:rgba(195,64,47,.26);border-color:rgba(242,164,147,.6)}
.rz-stops button.is-live{box-shadow:inset 0 0 0 1px rgba(240,160,142,.7)}
.rz-stops b{display:block;font-family:'Podkova',serif;font-size:17px;margin:0 0 4px}
.rz-stops i{font-style:normal;color:rgba(255,255,255,.6);font-size:13.5px;
 display:block;margin-top:5px}
.rz-stops em{font-style:normal;display:inline-block;font-size:11.5px;
 letter-spacing:.08em;text-transform:uppercase;margin-right:8px;color:#F0A08E}
.rz-stops .sl em{color:#9CC6E4}
.rz-walk{margin:16px 0 0;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.rz-walk button{cursor:pointer;background:var(--red);border:0;color:#fff;
 border-radius:99px;padding:11px 20px;font:700 15px 'Podkova',serif}
.rz-walk span{font-size:14px;color:rgba(255,255,255,.62)}

/* ── колея ─────────────────────────────────────────────────────────────── */
.rz-gauge__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
 gap:clamp(22px,3.4vw,42px);align-items:center;margin-top:26px}
.rz-gauge__box{background:var(--sand);border-radius:14px;padding:clamp(16px,2.4vw,26px)}
.rz-gauge svg{width:100%;height:auto;display:block}
.rz-gauge input[type=range]{width:100%;margin:18px 0 6px;accent-color:var(--red)}
.rz-gauge__val{font-family:'Podkova',serif;font-weight:700;
 font-size:clamp(30px,4.6vw,46px);line-height:1}
.rz-gauge__val span{font-size:16px;font-family:'Istok Web',sans-serif;
 font-weight:400;color:var(--mut);margin-left:8px}
.rz-gauge__ends{display:flex;justify-content:space-between;font-size:13px;
 color:var(--mut)}
.rz-gauge__shot img{border-radius:12px}

/* ── цифры ─────────────────────────────────────────────────────────────── */
.rz-nums{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));
 gap:12px;margin-top:26px;padding:0;list-style:none}
.rz-nums button{width:100%;height:100%;cursor:pointer;text-align:left;
 background:var(--paper);border:1px solid var(--line);border-radius:13px;
 padding:16px 16px 14px;transition:border-color .18s,transform .18s,box-shadow .18s;
 font:inherit;color:inherit}
.rz-nums button:hover,.rz-nums button:focus-visible{border-color:var(--red);
 transform:translateY(-2px);box-shadow:0 12px 26px rgba(25,28,33,.1)}
.rz-nums button.is-on{border-color:var(--red);background:#FCF3F1}
.rz-nums .num{display:block;font-family:'Podkova',serif;font-weight:700;
 font-size:clamp(25px,3.2vw,36px);line-height:1;color:var(--red)}
.rz-nums small{display:block;font-size:14.5px;color:#41474E;margin-top:7px;
 line-height:1.35}
.rz-nums .tc{display:block;font-size:13px;color:var(--mut);margin-top:9px}
.rz-numshot{margin-top:18px;display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);
 gap:18px;align-items:center}
.rz-numshot img{border-radius:13px;width:100%}

/* ── миллион вагонов ───────────────────────────────────────────────────── */
.rz-train{background:var(--deep);color:#fff;border-radius:16px;
 padding:clamp(20px,3vw,34px);margin-top:26px}
.rz-train h3{color:#fff}
.rz-train__bars{margin-top:20px;display:grid;gap:14px}
.rz-train__bar b{display:block;font-family:'Podkova',serif;font-size:17px;
 margin:0 0 6px;font-weight:700}
.rz-train__bar i{display:block;height:20px;border-radius:4px;background:var(--red);
 font-style:normal}
.rz-train__bar.alt i{background:#4A5C6A}
.rz-train__bar span{display:block;font-size:13.5px;color:rgba(255,255,255,.66);
 margin-top:6px}
.rz-train__math{font-size:14.5px;color:rgba(255,255,255,.72);margin:18px 0 0}

/* ── общая сетка карточек ──────────────────────────────────────────────── */
.rz-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
 gap:clamp(18px,2.6vw,30px);margin-top:26px}
.rz-card{border:1px solid var(--line);border-radius:14px;overflow:hidden;
 background:var(--paper)}
.rz-card img{width:100%}
.rz-card__t{padding:14px 16px 16px}
.rz-card__t h3{margin:0 0 6px}
.rz-card__t p{margin:0;font-size:15px;color:#454B52}
.rz-tags{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0;padding:0;list-style:none}
.rz-tags li{border:1px solid var(--line);border-radius:99px;padding:8px 15px;
 font-size:15px;background:var(--paper)}
.rz-tags li b{font-family:'Podkova',serif;color:var(--red);margin-right:7px}
.rz-list{margin:22px 0 0;padding:0;list-style:none;display:grid;gap:10px}
.rz-list li{display:flex;gap:13px;align-items:baseline;border-bottom:1px solid var(--line);
 padding-bottom:10px}
.rz-list b{font-family:'Podkova',serif;color:var(--red);flex:none;font-size:17px}
.rz-two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
 gap:clamp(18px,2.6vw,30px);margin-top:26px}
.rz-two img{border-radius:13px;width:100%}

/* ── синхрон ───────────────────────────────────────────────────────────── */
.rz-sync{background:var(--sand)}
.rz-sync__grid{display:grid;grid-template-columns:232px minmax(0,1fr);
 gap:clamp(20px,3vw,38px);align-items:center}
.rz-sync__grid img{border-radius:50%;width:232px;height:232px;object-fit:cover}
.rz-sync blockquote{margin:0 0 16px;font-family:'Podkova',serif;font-weight:700;
 font-size:clamp(20px,2.7vw,30px);line-height:1.2}
.rz-sync .who{font-size:15px;color:#454B52;margin:0 0 16px}
.rz-go{display:inline-block;background:var(--red);color:#fff;text-decoration:none;
 border-radius:99px;padding:12px 22px;font:700 15px 'Podkova',serif;border:0;
 cursor:pointer}

/* ── финал ─────────────────────────────────────────────────────────────── */
.rz-end{background:var(--red);color:#fff;text-align:center}
.rz-end h2{color:#fff;letter-spacing:.02em}
.rz-end p{color:rgba(255,255,255,.88);margin-left:auto;margin-right:auto}
.rz-end .rz-end__shot{max-width:760px;margin:26px auto 0;border-radius:14px;
 overflow:hidden}

/* ── адаптив ───────────────────────────────────────────────────────────── */
@media(max-width:1080px){
 .rz-yard__grid{grid-template-columns:minmax(0,1fr)}
 .rz-side{display:grid;grid-template-columns:220px minmax(0,1fr);gap:14px;
  align-items:start}
 .rz-side img{grid-row:span 5}
}
@media(max-width:860px){
 .rz-hero__grid,.rz-gauge__grid,.rz-two,.rz-numshot{grid-template-columns:minmax(0,1fr)}
 .rz-hero__meta{grid-template-columns:repeat(2,minmax(0,1fr))}
 .rz-sync__grid{grid-template-columns:minmax(0,1fr);justify-items:start}
 .rz-sync__grid img{width:168px;height:168px}
}
@media(max-width:560px){
 .rz-side{grid-template-columns:minmax(0,1fr)}
 .rz-side img{grid-row:auto}
 .rz-hero__meta{grid-template-columns:minmax(0,1fr)}
}
</style>"""


# ─── секции ─────────────────────────────────────────────────────────────────
def hero():
    meta = [('3:54', 'хронометраж фильма'),
            (str(SHOTS), 'планов, средняя длина 2,0 с'),
            ('3', 'города и три съёмочные группы'),
            ('2009', 'год образования дирекции')]
    tiles = ''.join(f'<div><b>{n}</b><span>{t}</span></div>' for n, t in meta)
    return (
      '<section class="rz-hero"><div class="rz-hero__bg"></div><div class="in">'
      '<p class="rz-hero__crumb"><a href="/project/">Проекты</a> / '
      '<a href="/videoproduction/">Видеопродакшн</a> / РЖД</p>'
      '<div class="rz-hero__grid"><div>'
      '<h1>История успеха ЦМ РЖД</h1>'
      '<p class="rz-hero__sub">Фильм к десятилетию Центральной дирекции '
      'по управлению терминально-складским комплексом, филиала ОАО «РЖД»</p>'
      '<p class="lead" style="color:rgba(255,255,255,.9)">Дирекция держит '
      'грузовые дворы по всей стране: от Калининграда до Находки. За 3:54 фильм '
      'должен был показать, что это за хозяйство, чем оно занято каждый день '
      'и что изменилось за десять лет.</p>'
      f'<div class="rz-hero__meta">{tiles}</div>'
      '</div>'
      f'<div class="rz-hero__shot"><img src="{IMG}/logo.jpg" width="1280" height="720" '
      'alt="Заставка фильма: знак «10 лет» с краном и логотип ОАО «РЖД»" '
      'fetchpriority="high"></div>'
      '</div></div></section>')


def brief():
    items = [
      ('Задача',
       'Показать дирекцию, которую снаружи почти никто не видит. Грузовой двор '
       'это место, где вагон встречается с автомобилем и складом, и объяснить '
       'это нужно было и клиентам, и самим железнодорожникам.'),
      ('Что было на входе',
       'Презентация дирекции: услуги, перерабатываемые грузы, карта сети '
       'и крупные стройки страны. Плюс доступ на действующие терминалы: '
       'в кадре дворы работают, погрузка идёт своим чередом.'),
      ('Решение',
       'Три съёмочные группы вышли параллельно в Москве, Санкт-Петербурге '
       'и Калининграде. Съёмка с земли и с квадрокоптера, слайды дирекции '
       'пересобраны в экранную графику, итог десяти лет проговаривает '
       'сам начальник дирекции.'),
    ]
    cards = ''.join(f'<div class="rz-brief__it rz-r"><b></b><h3>{t}</h3><p>{d}</p></div>'
                    for t, d in items)
    return ('<section><div class="in">'
            '<p class="kick">Кейс</p>'
            '<h2>Четыре минуты про хозяйство<br>размером в страну</h2>'
            f'<div class="rz-brief">{cards}</div>'
            '</div></section>')


def yard():
    stops = ''
    for i, (sid, name, sub, x, y, shot, sec, a, b, natural, note) in enumerate(STOPS):
        kind = '' if natural else ' sl'
        mark = 'кадр съёмки' if natural else 'фото со слайда'
        stops += (f'<li><button type="button" class="rz-stop{kind}" data-i="{i}">'
                  f'<b>{i + 1}. {name}</b>'
                  f'<em>{mark}</em><span class="mut">{mmss(sec)}</span>'
                  f'<i>{sub}</i></button></li>')
    first = STOPS[0]
    return (
      '<section class="rz-yard"><div class="in">'
      '<p class="kick">Главная механика</p>'
      '<h2>Семь услуг дирекции,<br>разложенных по грузовому двору</h2>'
      '<p class="lead">В фильме услуги показаны так, как они лежат в презентации '
      'дирекции: ряд шестиугольников с подписями. Мы собрали двор, на котором '
      'эти услуги происходят, и поставили к каждой кадр из фильма. Три услуги '
      'сняты живьём, четыре остались фотографией со слайда, и на схеме это видно '
      'по цвету пометки.</p>'
      '<div class="rz-stage"><video id="rz-v" controls preload="none" playsinline '
      f'poster="{IMG}/poster.jpg" width="1280" height="720">'
      f'<source src="{VIDEO}" type="video/mp4">'
      'Ваш браузер не воспроизводит видео.</video></div>'
      '<div class="rz-yard__grid">'
      f'<div><div class="rz-planwrap" id="rz-wrap">{plan_svg()}</div>'
      '<p class="rz-hint">Схема шире экрана: её можно прокрутить вбок, '
      'а выбор остановки подводит нужное место сам.</p></div>'
      '<aside class="rz-side">'
      f'<img id="rz-shot" src="{IMG}/{first[5]}.jpg" width="1280" height="720" '
      f'alt="Кадр фильма: {first[1].lower()}" loading="lazy">'
      '<div><span class="rz-badge shot" id="rz-badge">кадр съёмки</span>'
      f'<h3 id="rz-name">{first[1]}</h3>'
      f'<p class="tc" id="rz-tc">{mmss(first[6])}</p>'
      f'<p id="rz-note">{first[10]}</p></div>'
      '</aside></div>'
      f'<ul class="rz-stops">{stops}</ul>'
      '<div class="rz-walk"><button type="button" id="rz-walk">Пройти двор целиком</button>'
      '<span>Контейнер обойдёт семь остановок по порядку слайда</span></div>'
      '</div></section>')


def gauge():
    return (
      '<section class="sand"><div class="in">'
      '<p class="kick">Калининград</p>'
      '<h2>Восемьдесят пять миллиметров,<br>из-за которых нужен терминал</h2>'
      '<p class="lead">На 1:49 в фильме поверх площадки ложится размер, и число '
      'на нём уходит с 1520 на 1435. Это ширина колеи: российская сеть построена '
      'на 1520 мм, европейская на 1435 мм. Калининградский узел стоит ровно '
      'на стыке, поэтому груз здесь переставляют, перегружают и хранят. '
      'ТЛЦ «Калининград» это единственный терминал, который в фильме назван '
      'по имени: его подпись держится в кадре с 1:38 по 1:45.</p>'
      '<div class="rz-gauge__grid">'
      '<div class="rz-gauge rz-gauge__box">'
      '<svg viewBox="0 0 460 200" role="img" aria-label="Сечение пути: '
      'две рельсовые нитки и размер между ними">'
      '<rect x="30" y="128" width="400" height="26" rx="4" fill="#8C7C63"/>'
      '<rect x="30" y="154" width="400" height="12" rx="3" fill="#B9B3A6"/>'
      '<g id="rz-rails">'
      '<path id="rz-rail-l" d="M92 128v-52h16v52z" fill="#4A5C6A"/>'
      '<path id="rz-rail-r" d="M344 128v-52h16v52z" fill="#4A5C6A"/>'
      '<line id="rz-dim" x1="108" y1="60" x2="352" y2="60" stroke="#C3402F" '
      'stroke-width="3"/>'
      '<line id="rz-dim-l" x1="108" y1="48" x2="108" y2="72" stroke="#C3402F" '
      'stroke-width="3"/>'
      '<line id="rz-dim-r" x1="352" y1="48" x2="352" y2="72" stroke="#C3402F" '
      'stroke-width="3"/>'
      '</g></svg>'
      '<p class="rz-gauge__val"><span id="rz-gv">1520</span> <span>мм между '
      'внутренними гранями рельсов</span></p>'
      '<input id="rz-range" type="range" min="1435" max="1520" step="1" value="1520" '
      'aria-label="Ширина колеи в миллиметрах">'
      '<div class="rz-gauge__ends"><span>1435, Европа</span><span>1520, Россия</span></div>'
      '<p class="cap" id="rz-gnote">Российская колея. По ней груз доезжает '
      'до калининградских терминалов.</p>'
      '</div>'
      '<div class="rz-gauge__shot">'
      f'<img id="rz-gshot" src="{IMG}/gauge20.jpg" width="1280" height="720" '
      'alt="Кадр фильма: экранная линейка ширины колеи над площадкой" loading="lazy">'
      '<p class="cap" id="rz-gcap">1:49. Размер 1520 в кадре: тот же приём '
      'мы повторили ползунком слева.</p>'
      '</div></div>'
      '<div class="rz-two" style="margin-top:26px">'
      f'<div><img src="{IMG}/kal-coal.jpg" width="1280" height="720" '
      'alt="ТЛЦ «Калининград»: экскаватор грузит уголь в полувагоны" loading="lazy">'
      '<p class="cap">1:42. Перегрузка угля в полувагоны, подпись '
      '«ТЛЦ „Калининград“» в правом нижнем углу кадра.</p></div>'
      f'<div><img src="{IMG}/baltkran.jpg" width="1280" height="720" '
      'alt="Козловой кран «Балткран» грузоподъёмностью 41 тонна" loading="lazy">'
      '<p class="cap">1:56. Козловой кран «Балткран» на 41 тонну: маркировка '
      'читается прямо на ригеле.</p></div>'
      '</div></div></section>')


def numbers():
    items = ''
    for i, (nid, num, cap, shot, sec) in enumerate(NUMBERS):
        items += (f'<li><button type="button" class="rz-num" data-i="{i}">'
                  f'<span class="num">{num}</span><small>{cap}</small>'
                  f'<span class="tc">{mmss(sec)} в фильме</span></button></li>')
    first = NUMBERS[0]
    return (
      '<section><div class="in">'
      '<p class="kick">Паспорт дирекции</p>'
      '<h2>Семь плашек, на которых<br>держится вся первая минута</h2>'
      '<p class="lead">Первую минуту фильм отдаёт цифрам: они выходят поверх '
      'натурных кадров, без отдельных заставок. Здесь они собраны в один ряд, '
      'нажатие ставит плеер на ту секунду, где плашка появляется.</p>'
      f'<ul class="rz-nums">{items}</ul>'
      '<div class="rz-numshot">'
      f'<img id="rz-nshot" src="{IMG}/{first[3]}.jpg" width="1280" height="720" '
      f'alt="Кадр фильма с плашкой: {first[2]}" loading="lazy">'
      f'<p class="cap" id="rz-ncap">{mmss(first[4])}. Плашка «{first[1]}»: '
      f'{first[2]}.</p>'
      '</div>'
      + train() +
      '</div></section>')


def train():
    # 1 000 000 вагонов × 14 м ≈ 14 000 км сцепки; для сравнения длина Транссиба
    # Москва - Владивосток 9288,2 км
    return (
      '<div class="rz-train rz-r"><h3>Что такое миллион вагонов</h3>'
      '<p style="color:rgba(255,255,255,.8);max-width:60ch">Цифра с плашки '
      'на 0:55 сама по себе абстрактна. Если сцепить миллион вагонов подряд, '
      'состав получится длиннее страны.</p>'
      '<div class="rz-train__bars">'
      '<div class="rz-train__bar"><b>≈ 14 000 км</b>'
      '<i style="width:100%"></i>'
      '<span>Миллион вагонов в сцепке: длина полувагона по осям автосцепок '
      'взята за 14 м.</span></div>'
      '<div class="rz-train__bar alt"><b>9288 км</b>'
      '<i style="width:66.3%"></i>'
      '<span>Транссиб от Москвы до Владивостока, для сравнения.</span></div>'
      '</div>'
      '<p class="rz-train__math">1 000 000 × 14 м = 14 000 000 м = 14 000 км. '
      'Это полторы длины Транссиба. Период плашка не называет, и мы его '
      'не додумываем.</p></div>')


def cargo():
    tags = ''.join(f'<li><b>{i + 1}</b>{name}</li>' for i, name in enumerate(CARGO))
    return (
      '<section class="sand"><div class="in">'
      '<p class="kick">Перерабатываемые грузы</p>'
      '<h2>Тринадцать позиций,<br>которые дирекция берёт на двор</h2>'
      '<p class="lead">Слайд «Перерабатываемые грузы» проезжает в фильме '
      'за три секунды, и целиком его не увидеть: камера идёт по кругам '
      'с фотографиями. Список снят с этого слайда, порядок сохранён.</p>'
      f'<ul class="rz-tags">{tags}</ul>'
      '<div class="rz-two">'
      f'<div><img src="{IMG}/slide-cargo1.jpg" width="1280" height="720" '
      'alt="Слайд «Перерабатываемые грузы», верхний ряд кругов" loading="lazy">'
      '<p class="cap">0:46. Верхний ряд: от щебня до негабаритных грузов.</p></div>'
      f'<div><img src="{IMG}/slide-cargo2.jpg" width="1280" height="720" '
      'alt="Слайд «Перерабатываемые грузы», нижний ряд кругов" loading="lazy">'
      '<p class="cap">0:49. Нижний ряд: от автомобилей до контрейлеров.</p></div>'
      '</div></div></section>')


def geography():
    cities = ''.join(f'<li>{c}</li>' for c in CITIES)
    builds = ''.join(f'<li><b>{i + 1}</b><span>{b}</span></li>'
                     for i, b in enumerate(BUILDS))
    return (
      '<section><div class="in">'
      '<p class="kick">География</p>'
      '<h2>От Калининграда до Находки</h2>'
      '<p class="lead">На 1:05 в фильме разворачивается карта сети: точки '
      'терминалов по всей стране и линия Транссиба. Подписанных городов '
      'пятнадцать, они идут с запада на восток.</p>'
      f'<ul class="rz-tags">{cities}</ul>'
      '<div class="rz-two">'
      f'<div><img src="{IMG}/map.jpg" width="1280" height="720" '
      'alt="Кадр фильма: карта сети терминалов от Калининграда до Находки" '
      'loading="lazy">'
      '<p class="cap">1:12. Карта сети целиком.</p></div>'
      f'<div><img src="{IMG}/builds.jpg" width="1280" height="720" '
      'alt="Кадр фильма: коллаж крупных строек страны" loading="lazy">'
      '<p class="cap">1:19. Коллаж строек: снимки разлетаются по экрану, '
      'подписи держатся в центре.</p></div>'
      '</div>'
      '<h3 style="margin-top:34px">Стройки, которые фильм называет отдельно</h3>'
      f'<ul class="rz-list">{builds}</ul>'
      '</div></section>')


def digital():
    tiles = ''.join(f'<li><b>{i + 1}</b><span>{t}</span></li>'
                    for i, t in enumerate(ETP))
    return (
      '<section class="sand"><div class="in">'
      '<p class="kick">Экраны в фильме</p>'
      '<h2>Заказ, ведомость и счётчик вагонов</h2>'
      '<p class="lead">Кроме двора в фильме есть третий слой: рабочие экраны '
      'дирекции. Их снимали с монитора, поэтому в кадре видны и реальные данные, '
      'и живой счётчик вагонов за день.</p>'
      '<div class="rz-cols">'
      f'<div class="rz-card rz-r"><img src="{IMG}/etp.jpg" width="1280" height="720" '
      'alt="Электронная торговая площадка «Грузовые перевозки»" loading="lazy">'
      '<div class="rz-card__t"><h3>ЭТП «Грузовые перевозки»</h3>'
      '<p>2:04. Шесть плиток заказа поверх карты страны, справа счётчик '
      '«вагонов за день».</p></div></div>'
      f'<div class="rz-card rz-r"><img src="{IMG}/teskad.jpg" width="1280" height="720" '
      'alt="АС ТЕСКАД: ведомость погрузочно-разгрузочных работ" loading="lazy">'
      '<div class="rz-card__t"><h3>АС ТЕСКАД</h3>'
      '<p>2:11. Ведомость погрузочно-разгрузочных работ: Санкт-Петербург '
      'Витебская МЧ-4, участок Шушары, смена 22.09.19.</p></div></div>'
      f'<div class="rz-card rz-r"><img src="{IMG}/site.jpg" width="1280" height="720" '
      'alt="Страница дирекции на сайте ОАО «РЖД»" loading="lazy">'
      '<div class="rz-card__t"><h3>Раздел на сайте ОАО «РЖД»</h3>'
      '<p>1:59. Страница дирекции с перечнем погрузочно-разгрузочных работ, '
      'вкладки «Услуги» и «Грузовые дворы».</p></div></div>'
      '</div>'
      f'<ul class="rz-tags">{tiles}</ul>'
      '<p class="cap">Плитки ЭТП перечислены в том порядке, в каком они стоят '
      'на экране в кадре.</p>'
      '</div></section>')


def people():
    cards = [
      ('craneop', 'Крановщик', '2:42. Кабина козлового крана изнутри: '
       'оператор ведёт спредер к штабелю.'),
      ('brigade', 'Приёмосдатчики', '3:07. Двое в жилетах ЦМ с ведомостью '
       'и рацией: приёмка груза идёт с бумагой в руках.'),
      ('polo', 'I Слёт молодежи ЦМ', '2:59. Красное поло с надписью: слёт '
       'дирекции занимает в фильме почти полминуты.'),
      ('team', 'Командная игра', '2:53. Разбор кейсов на слёте, флипчарты '
       'с конкурентами и социальной ответственностью.'),
    ]
    out = ''.join(
      f'<div class="rz-card rz-r"><img src="{IMG}/{s}.jpg" width="1280" height="720" '
      f'alt="Кадр фильма: {t.lower()}" loading="lazy">'
      f'<div class="rz-card__t"><h3>{t}</h3><p>{d}</p></div></div>'
      for s, t, d in cards)
    return (
      '<section><div class="in">'
      '<p class="kick">Люди</p>'
      '<h2>Семь тысяч человек,<br>из которых в кадр попали десятки</h2>'
      '<p class="lead">Вторая половина фильма уходит от техники к людям: '
      'крановщики, приёмосдатчики, водители, переговоры с клиентом, конференция '
      'и слёт молодежи дирекции. Это та часть, ради которой фильм показывают '
      'внутри компании, а не только клиентам.</p>'
      f'<div class="rz-cols">{out}</div>'
      '</div></section>')


def sync():
    return (
      '<section class="rz-sync"><div class="in"><div class="rz-sync__grid">'
      f'<img src="{IMG}/p-belsky.jpg" width="560" height="560" '
      'alt="Алексей Юрьевич Бельский, начальник Центральной дирекции '
      'по управлению терминально-складским комплексом" loading="lazy">'
      '<div>'
      '<p class="kick">Финальный синхрон</p>'
      '<blockquote>Итог десяти лет проговаривает начальник дирекции, '
      'а не закадровый диктор</blockquote>'
      '<p class="who">Алексей Юрьевич Бельский, начальник Центральной дирекции '
      'по управлению терминально-складским комплексом, филиала ОАО «РЖД». '
      'Титр держится в кадре с 3:18 по 3:28, сам синхрон идёт с 3:15 по 3:37 '
      'и закрывает фильм.</p>'
      '<button type="button" class="rz-go" id="rz-sync-go">Включить синхрон '
      'с 3:15</button>'
      '</div></div></div></section>')


def craft():
    items = ''.join(f'<div class="rz-brief__it rz-r"><b></b><h3>{t}</h3><p>{d}</p></div>'
                    for t, d in CRAFT)
    return ('<section><div class="in">'
            '<p class="kick">Работа</p>'
            '<h2>Что мы сделали</h2>'
            f'<div class="rz-brief">{items}</div>'
            '</div></section>')


def ending():
    return (
      '<section class="rz-end"><div class="nar">'
      '<h2>Мы меняемся для вас</h2>'
      '<p>Титр, которым фильм выходит на финал: он держится с 3:08 по 3:15 '
      'над контейнерной площадкой, снятой с воздуха. Дальше синхрон '
      'и адрес дирекции на экране.</p>'
      f'<div class="rz-end__shot"><img src="{IMG}/change.jpg" width="1280" '
      'height="720" alt="Кадр фильма: титр «Мы меняемся для вас» над '
      'контейнерной площадкой" loading="lazy"></div>'
      '</div></section>')


PAGE_JS = """<script>(function(){
 var STOPS=%STOPS%,NUMS=%NUMS%,IMG='%IMG%',BOXDY=%BOXDY%;
 var v=document.getElementById('rz-v');
 if(!v)return;

 function mmss(s){s=Math.max(0,Math.round(s));return (s/60|0)+':'+('0'+(s%60)).slice(-2);}
 function inView(el){var r=el.getBoundingClientRect();
  return r.top>-40&&r.bottom<innerHeight+40;}
 function seek(s,play){
  // до загрузки метаданных currentTime молча игнорируется — ждём событие
  function go(){v.currentTime=Math.min(s,(v.duration||1e5)-.2);
   if(play!==false){var q=v.play();if(q&&q.catch)q.catch(function(){});}}
  if(v.readyState>0)go();
  else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}
  if(!inView(v))v.scrollIntoView({block:'center',behavior:'smooth'});
 }

 // ── двор: остановка ведёт контейнер, подсвечивает зону и кадр ───────────
 var box=document.getElementById('rz-box'),
     shot=document.getElementById('rz-shot'),badge=document.getElementById('rz-badge'),
     name=document.getElementById('rz-name'),tc=document.getElementById('rz-tc'),
     note=document.getElementById('rz-note'),
     btns=[].slice.call(document.querySelectorAll('.rz-stop')),
     pins=[].slice.call(document.querySelectorAll('.rz-pin')),
     cur=-1,walk=0;

 function show(i,doSeek){
  var s=STOPS[i];if(!s)return;
  if(box)box.setAttribute('transform','translate('+s.x+','+(s.y+BOXDY)+')');
  btns.forEach(function(b,j){b.classList.toggle('is-on',j===i);});
  pins.forEach(function(p,j){p.classList.toggle('is-on',j===i);});
  STOPS.forEach(function(o,j){
   var z=document.getElementById('z-'+o.id);
   if(z)z.classList.toggle('is-on',j===i);
  });
  shot.src=IMG+'/'+s.shot+'.jpg';
  shot.alt='Кадр фильма: '+s.name.toLowerCase();
  badge.className='rz-badge '+(s.natural?'shot':'slide');
  badge.textContent=s.natural?'кадр съёмки':'фото со слайда';
  name.textContent=s.name;tc.textContent=mmss(s.sec);note.textContent=s.note;
  cur=i;
  // узкий экран: схема шире контейнера, подводим выбранное место сами
  var wrap=document.getElementById('rz-wrap');
  if(wrap&&wrap.scrollWidth>wrap.clientWidth+4){
   var svg=wrap.querySelector('.rz-plan'),k=svg.getBoundingClientRect().width/1200;
   wrap.scrollTo({left:s.x*k-wrap.clientWidth/2,behavior:'smooth'});
  }
  if(doSeek)seek(s.sec,true);
 }
 btns.forEach(function(b){b.addEventListener('click',function(){
  stopWalk();show(+b.dataset.i,true);});});
 pins.forEach(function(p){
  p.addEventListener('click',function(){stopWalk();show(+p.dataset.i,true);});
  p.addEventListener('keydown',function(e){
   if(e.key==='Enter'||e.key===' '){e.preventDefault();stopWalk();show(+p.dataset.i,true);}
  });
 });

 // ── прогон по двору: контейнер обходит остановки, плеер не трогаем ──────
 var walkBtn=document.getElementById('rz-walk');
 function stopWalk(){if(walk){clearInterval(walk);walk=0;
  if(walkBtn)walkBtn.textContent='Пройти двор целиком';}}
 if(walkBtn)walkBtn.addEventListener('click',function(){
  if(walk){stopWalk();return;}
  walkBtn.textContent='Остановить обход';
  var i=0;show(i,false);
  walk=setInterval(function(){
   i++;if(i>=STOPS.length){stopWalk();return;}
   show(i,false);
  },2000);
 });

 // ── плеер ведёт схему: подсвечены остановки, попавшие в текущий отрезок ──
 var last=-1;
 v.addEventListener('timeupdate',function(){
  var t=v.currentTime|0;if(t===last)return;last=t;
  STOPS.forEach(function(s,j){
   var live=v.currentTime>=s.a&&v.currentTime<s.b;
   if(btns[j])btns[j].classList.toggle('is-live',live);
   if(pins[j])pins[j].classList.toggle('is-live',live);
  });
 });

 // ── цифры: карточка перематывает плеер и меняет кадр ────────────────────
 var nshot=document.getElementById('rz-nshot'),ncap=document.getElementById('rz-ncap'),
     nbtns=[].slice.call(document.querySelectorAll('.rz-num'));
 nbtns.forEach(function(b){b.addEventListener('click',function(){
  var n=NUMS[+b.dataset.i];
  nbtns.forEach(function(o,j){o.classList.toggle('is-on',j===+b.dataset.i);});
  nshot.src=IMG+'/'+n.shot+'.jpg';
  nshot.alt='Кадр фильма с плашкой: '+n.cap;
  ncap.textContent=mmss(n.sec)+'. Плашка «'+n.num+'»: '+n.cap+'.';
  seek(n.sec,true);
 });});

 // ── колея: ползунок повторяет экранный размер из фильма ─────────────────
 var range=document.getElementById('rz-range'),gv=document.getElementById('rz-gv'),
     rl=document.getElementById('rz-rail-l'),rr=document.getElementById('rz-rail-r'),
     dim=document.getElementById('rz-dim'),dl=document.getElementById('rz-dim-l'),
     dr=document.getElementById('rz-dim-r'),gshot=document.getElementById('rz-gshot'),
     gcap=document.getElementById('rz-gcap'),gnote=document.getElementById('rz-gnote');
 function gauge(mm){
  // 1520 мм = 244 px между внутренними гранями: масштаб взят от рисунка
  var w=244*mm/1520,cx=230,xl=cx-w/2,xr=cx+w/2;
  rl.setAttribute('d','M'+(xl-16)+' 128v-52h16v52z');
  rr.setAttribute('d','M'+xr+' 128v-52h16v52z');
  dim.setAttribute('x1',xl);dim.setAttribute('x2',xr);
  dl.setAttribute('x1',xl);dl.setAttribute('x2',xl);
  dr.setAttribute('x1',xr);dr.setAttribute('x2',xr);
  gv.textContent=mm;
  var euro=mm<1478;
  gshot.src=IMG+'/'+(euro?'gauge35':'gauge20')+'.jpg';
  gcap.textContent=euro?'1:52. Тот же кадр после пересчёта: 1435.'
                       :'1:49. Размер 1520 в кадре: тот же приём мы повторили ползунком слева.';
  gnote.textContent=euro?'Европейская колея. Дальше груз идёт уже в другом вагоне, '
                       +'и без перегрузки на терминале не обойтись.'
                       :'Российская колея. По ней груз доезжает до калининградских терминалов.';
 }
 if(range){range.addEventListener('input',function(){gauge(+range.value);});gauge(1520);}

 // ── синхрон ─────────────────────────────────────────────────────────────
 var sg=document.getElementById('rz-sync-go');
 if(sg)sg.addEventListener('click',function(){seek(195.5,true);});

 // ── появление блоков: свип по скроллу, а не IntersectionObserver.
 // Наблюдатель отдаёт колбэк на следующем кадре, и при быстрой прокрутке
 // нижние блоки остаются с opacity:0. Свип считает геометрию синхронно.
 var els=[].slice.call(document.querySelectorAll('.rz-r'));
 function sweep(){
  for(var i=els.length-1;i>=0;i--){
   var r=els[i].getBoundingClientRect();
   if(r.top<innerHeight*1.1&&r.bottom>-120){els[i].classList.add('is-in');els.splice(i,1);}
  }
  if(!els.length){removeEventListener('scroll',sweep);removeEventListener('resize',sweep);}
 }
 addEventListener('scroll',sweep,{passive:true});
 addEventListener('resize',sweep);
 sweep();
})();</script>"""

TITLE = ('Ролик «История успеха ЦМ РЖД»: фильм к десятилетию дирекции '
         '| Hand Marketing')
DESCR = ('Кейс Hand Marketing: фильм на 3:54 к десятилетию Центральной дирекции '
         'по управлению терминально-складским комплексом ОАО «РЖД». Три '
         'съёмочные группы в Москве, Санкт-Петербурге и Калининграде, съёмка '
         'с земли и с воздуха. Семь услуг дирекции разложены по схеме грузового '
         'двора прямо на странице.')

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Видеопродакшн","item":"https://hand-marketing.ru/videoproduction/"},'
  '{"@type":"ListItem","position":3,"name":"Ролик «История успеха ЦМ РЖД»",'
  f'"item":"{URL}"}}]}}</script>')

VIDEO_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"VideoObject","name":"История успеха ЦМ РЖД",'
  '"description":"Фильм Hand Marketing к десятилетию Центральной дирекции '
  'по управлению терминально-складским комплексом ОАО «РЖД»: терминалы '
  'с воздуха и с земли, услуги и цифры дирекции экранной графикой, '
  'синхрон начальника дирекции.",'
  f'"thumbnailUrl":"https://hand-marketing.ru{IMG}/poster.jpg",'
  '"uploadDate":"2019-10-01","duration":"PT3M54S",'
  f'"contentUrl":"https://hand-marketing.ru{VIDEO}",'
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
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/poster.jpg">'
        '<link rel="stylesheet" href="/fonts/podkova-istok.css">'
        + rc.FONT + rc.CSS + CSS.replace('%IMG%', IMG) + METRIKA + '</head><body>')


def page():
    stops = [{'id': s[0], 'name': s[1], 'x': s[3], 'y': s[4], 'shot': s[5],
              'sec': s[6], 'a': s[7], 'b': s[8], 'natural': s[9], 'note': s[10]}
             for s in STOPS]
    nums = [{'num': n[1], 'shot': n[3], 'sec': n[4], 'cap': n[2]} for n in NUMBERS]
    js = (PAGE_JS.replace('%STOPS%', json.dumps(stops, ensure_ascii=False))
                 .replace('%NUMS%', json.dumps(nums, ensure_ascii=False))
                 .replace('%IMG%', IMG).replace('%BOXDY%', str(BOX_DY)))
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="rz">{hero()}{brief()}{yard()}{gauge()}'
            f'{numbers()}{cargo()}{geography()}{digital()}{people()}{sync()}'
            f'{craft()}{ending()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}{VIDEO_LD}'
            '</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'rgd', 'history')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
