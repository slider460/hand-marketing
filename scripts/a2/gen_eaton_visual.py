#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/creative/eaton/visual/index.html: кейс «3D-визуализация
решений Eaton» — три печатных плаката 2017 года, на которых оборудование
Eaton расставлено по трём типам объектов: ЦОД, коммерческий, промышленный.

Первоисточник — сами плакаты (300 dpi, 9449×7087 и 7087×9449). Ничего не
придумано: 20 выносок, 10 позиций оборудования, все спецификации и геометрия
кружков и линий сняты с печатных файлов скриптом scripts/eaton-visual-assets.py.

Идея страницы. Плакат — это два слоя: рендер объекта и печатная подача поверх
него (кружки с оборудованием, подписи, линии-выноски). Второй слой на бумаге
намертво прибит к формату А1. Значит, на странице его надо снять и собрать
заново живым — тогда видно, как устроена работа: одна библиотека 3D-моделей
оборудования раскладывается по трём разным сценам.

Отсюда механики:

1. «Живая выноска» (сигнатурная). Печатный слой снят с плаката алгоритмом
   (подложки plate-*.jpg — чистый рендер на градиенте), а кружки, линии и
   подписи нарисованы кодом в тех же координатах, что были в печати: линия
   приходит ровно в ту точку объекта, куда указывала печатная. Раскладка при
   этом адаптивная — на узком экране выноски превращаются в нумерованные точки
   и список, чего печатный лист не умеет.
2. Матрица «библиотека против сцены»: 10 позиций × 3 объекта. Видно, что
   четыре позиции повторяются везде, а шесть выбраны под тип объекта.
3. Печатный масштаб: фрагменты 1:1 с линейкой в сантиметрах — 300 dpi против
   экранного просмотра.

Шрифты — Play (заголовки и цифры) и Roboto с Roboto Condensed (текст
и спец-списки), self-host: /fonts/play-roboto.css. Play нарисован по чертёжной
технике и держит инженерный регистр кейса; Roboto — ближайший к Helvetica
плакатов гротеск, у которого есть кириллица, узкий Roboto Condensed повторяет
плотные списки характеристик. Archivo и Barlow, которые просились по рисунку,
кириллицы не содержат вовсе — на русском тексте они молча падают в системный. Палитра — из самих плакатов: синий градиент Eaton,
белый и сигнальный зелёный с таблички «выход».

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

MAP = json.load(open(os.path.join(HERE, 'eaton_visual_map.json'), encoding='utf-8'))

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/eaton-visual'
URL = 'https://hand-marketing.ru/creative/eaton/visual/'

# размеры готовых файлов из scripts/eaton-visual-assets.py
SIZE = {'plate-commercial': [2200, 1450], 'plate-dc': [2200, 1450],
        'plate-industry': [1800, 2119], 'poster-commercial': [2000, 1500],
        'poster-dc': [2000, 1500], 'poster-industry': [1700, 2266],
        'zoom-1': [1400, 1000], 'zoom-2': [1400, 1000], 'zoom-3': [1400, 1000],
        'zoom-4': [1400, 1000], 'chip-busway': [440, 440], 'chip-exit': [440, 440],
        'chip-monitoring': [440, 440], 'chip-powerxl': [440, 440],
        'chip-racks': [440, 440], 'chip-towers': [440, 440], 'chip-ups': [440, 440],
        'chip-xenergy': [440, 440], 'chip-xiria': [440, 440], 'chip-xstart': [440, 440]}

# ─── объекты ────────────────────────────────────────────────────────────────
# (slug, короткое имя, что за объект, что видно в разрезе)
OBJECTS = [
    ('dc', 'Центр обработки данных', 'ЦОД',
     'Машинный зал с тремя рядами стоек в закрытых холодных коридорах, '
     'газовое пожаротушение, зал ИБП, электрощитовая, операторская и ресепшн.'),
    ('commercial', 'Коммерческий объект', 'Гипермаркет',
     'Торговый зал с холодильными витринами и стеллажами, кассовая линия, '
     'кафе, склад с паллетами и погрузчиком, зона приёмки и техпомещения.'),
    ('industry', 'Промышленный объект', 'Завод',
     'Цех с прессами и конвейерной линией, сборочные столы, склады сырья '
     'и готовой продукции, погрузчики, электрощитовая и трансформаторная.'),
]

# ─── позиции оборудования: всё с плакатов, дословно ─────────────────────────
# key: (название, лид, [характеристики])
PRODUCTS = {
    'ups': ('ИБП PowerXpert 9395P',
            'Источник бесперебойного питания Eaton мощностью 250–1200 кВА',
            ['Высокий КПД до 96,3 % в режиме двойного преобразования.',
             'Максимальная эффективность даже при минимальной нагрузке благодаря '
             'адаптивной системе управления модулями VMMS.',
             'Технология HotSync для параллельного подключения до 8 ИБП, '
             'исключающая единую точку отказа.']),
    'xenergy': ('Система распределительных щитов xEnergy', '',
                ['Типовые протестированные устройства до 5000 А.',
                 'Возможность встроенной дуговой защиты — активная и пассивная.',
                 'Степень секционирования до 4B.',
                 'Выкатные секции, в том числе с интеллектуальным мониторингом.']),
    'xiria': ('КРУ Xiria', '',
              ['Воздушная и литая межфазная изоляция.',
               'Силовые и вакуумные выключатели.',
               'Электронные самозапитывающиеся элементы защиты.',
               'Класс устойчивости к внутренней дуге AFL.',
               'Компактное решение.']),
    'exit': ('Аварийное освещение', '',
             ['Модуль с инновационной светодиодной технологией.',
              'Модели с дистанцией видимости более 30 метров.',
              'Кнопка для проверки работоспособности.']),
    'busway': ('Шинопровод Power Xpert XP2', '',
               ['Полная линейка моделей с алюминиевыми и медными проводниками.',
                'Возможность вертикальной и горизонтальной прокладки шинопроводов.',
                'При изменении конфигурации или направления прокладки шинопроводов '
                'их характеристики не ухудшаются.']),
    'xstart': ('Компоненты управления и защиты XSTART', '',
               ['DIL Контакторы: 10 млн коммутационных циклов, увеличенная '
                'включающая способность, малое энергопотребление.',
                'PKZ Автоматические выключатели защиты двигателя: номинальная '
                'отключающая способность до 150 кА, чувствительность к выпадению фазы.',
                'RMQ-Titan Компоненты управления и сигнализации: 5 млн механических '
                'циклов, степень защиты IP67/IP69K, технология LED.',
                'PL6/PL7 Модульные автоматические выключатели: визуальная индикация '
                'состояния главных контактов, двойная защита от прогорания, '
                'возможность пломбировки.']),
    'racks': ('Стойки и аксессуары Eaton', '',
              ['Широкий модельный ряд стоек 27U / 42U / 47U.',
               'Модули распределения питания в стойках Eaton ePDU 10–32 А.',
               'Опции и аксессуары для кабельной организации в стойках.',
               'Резервирование вводов 16 и 30 А.']),
    'monitoring': ('Мониторинг',
                   'Рабочее место с системой мониторинга инженерной инфраструктуры',
                   []),
    'powerxl': ('Преобразователи частоты PowerXL', '',
                ['DG1: функция каскадного управления насосами, 2 встроенных '
                 'PID-регулятора, встроенный 5 % дроссель звена постоянного тока.',
                 'DE1: ввод в эксплуатацию без параметрирования, максимально прост '
                 'в использовании, самый компактный в классе.']),
    'towers': ('Световые колонны', '',
               ['Визуальная и акустическая индикация состояния машин и установок.',
                'Различные комбинации.',
                'Простой монтаж.']),
}

# отличия подачи на конкретных плакатах — тоже с оригиналов
NAME_ON = {('industry', 'xiria'): 'КРУ Xiria E'}
EXTRA = {
    ('dc', 'xenergy'): ['Система температурного мониторинга компонентов.'],
    ('industry', 'xstart'): ['Большой выбор изолированных корпусов для повышенной '
                             'степени защиты до IP65.'],
}
# где на объекте стоит эта позиция — короткая подпись к точке
WHERE = {
    ('dc', 'racks'): 'машинный зал', ('dc', 'ups'): 'зал ИБП',
    ('dc', 'xenergy'): 'электрощитовая', ('dc', 'xiria'): 'ввод 10 кВ',
    ('dc', 'monitoring'): 'операторская', ('dc', 'exit'): 'эвакуационный выход',
    ('dc', 'busway'): 'над машинным залом',
    ('commercial', 'xstart'): 'техпомещение', ('commercial', 'powerxl'): 'вентиляция и холод',
    ('commercial', 'exit'): 'торговый зал', ('commercial', 'xiria'): 'ввод 10 кВ',
    ('commercial', 'busway'): 'кассовая линия', ('commercial', 'xenergy'): 'электрощитовая',
    ('commercial', 'towers'): 'кассовая линия', ('commercial', 'ups'): 'серверная',
    ('industry', 'xenergy'): 'электрощитовая', ('industry', 'xstart'): 'цех',
    ('industry', 'ups'): 'серверная', ('industry', 'xiria'): 'трансформаторная',
    ('industry', 'exit'): 'склад сырья',
}

# порядок позиций в матрице: сначала то, что стоит на всех трёх объектах
ORDER = ['ups', 'xenergy', 'xiria', 'exit', 'busway', 'xstart',
         'racks', 'monitoring', 'powerxl', 'towers']

ZOOMS = [
    ('zoom-1', 'ЦОД: ряды стоек в закрытом холодном коридоре'),
    ('zoom-3', 'Гипермаркет: витрины, стеллажи и кассовая линия'),
    ('zoom-4', 'Завод: прессы, конвейер и сборочные столы'),
    ('zoom-2', 'Кружок ИБП PowerXpert 9395P в размере печати'),
]


def img(name, alt, cls='', lazy=True, ext='jpg'):
    w, h = SIZE[name]
    l = ' loading="lazy" decoding="async"' if lazy else ''
    c = f' class="{cls}"' if cls else ''
    return f'<img src="{IMG}/{name}.{ext}" alt="{alt}" width="{w}" height="{h}"{c}{l}>'


def items(slug):
    """Выноски объекта в порядке печати: сверху вниз, слева направо."""
    it = MAP[slug]['items']
    return sorted(it, key=lambda i: (round(i['circle'][1], 2), i['circle'][0]))


def objects_of(key):
    return [s for s, _, _, _ in OBJECTS if any(i['key'] == key for i in MAP[s]['items'])]


# ─── секции ─────────────────────────────────────────────────────────────────

def hero():
    thumbs = ''.join(
        f'<figure class="ev-hero__t"><img src="{IMG}/poster-{s}.jpg" alt="Плакат «{n}»" '
        f'width="{SIZE["poster-" + s][0]}" height="{SIZE["poster-" + s][1]}" '
        f'decoding="async"><figcaption>{short}</figcaption></figure>'
        for s, n, short, _ in OBJECTS)
    return f'''<section class="ev-hero">
<div class="ev-wrap">
 <p class="ev-kicker">Creative &amp; Design · Eaton · 2017</p>
 <h1>Оборудование, расставленное<br>по трём типам объектов</h1>
 <p class="ev-lead">Eaton выпускает всё, чем питается здание: от ИБП и щитов до контакторов
  и аварийных светильников. Показать это списком нельзя — нужно место, где инженер увидит
  своё здание. Мы собрали три объекта в 3D и отрендерили их в разрезе: ЦОД, гипермаркет
  и завод. На каждом стоит типовой набор оборудования Eaton для этого типа объекта.</p>
 <div class="ev-hero__thumbs">{thumbs}</div>
 <dl class="ev-nums">
  <div><dt>3</dt><dd>объекта в 3D</dd></div>
  <div><dt>20</dt><dd>выносок на плакатах</dd></div>
  <div><dt>10</dt><dd>позиций оборудования</dd></div>
  <div><dt>300</dt><dd>dpi под печать А1</dd></div>
 </dl>
</div></section>'''


def task():
    return '''<section class="ev-task ev-rev"><div class="ev-wrap ev-task__grid">
<div><h2>Задача</h2>
 <p>Создать визуальные образы, которые показывают типовое размещение оборудования Eaton
  на объектах разного типа: что и в каком помещении стоит, как это связано между собой.</p>
 <p class="ev-note">Eaton — американская машиностроительная корпорация, основана в 1911 году:
  электротехническое и гидравлическое оборудование, компоненты для авиационной
  промышленности.</p></div>
<div><h2>Что сделали</h2>
 <p>Построили 3D-модели трёх объектов и самого оборудования. Инженеры Eaton расставили
  по каждому объекту типовой набор — так, как это делается на реальном проекте.
  Мы сняли рендеры в единой изометрии и адаптировали подачу под печать: к каждому виду
  оборудования добавили кружок с моделью, линию-выноску в точку установки и описание.</p>
 <p class="ev-note">Ниже печатный слой снят с плакатов и собран заново — уже живым.</p></div>
</div></section>'''


def scene():
    """Сигнатурный блок: чистая подложка плюс выноски, нарисованные кодом."""
    tabs = ''.join(
        f'<button type="button" class="ev-tab{" is-on" if i == 0 else ""}" '
        f'data-obj="{s}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'<span class="ev-tab__n">{short}</span>'
        f'<span class="ev-tab__c">{len(MAP[s]["items"])} позиций</span></button>'
        for i, (s, n, short, _) in enumerate(OBJECTS))

    panes = []
    for i, (slug, name, short, about) in enumerate(OBJECTS):
        ratio = MAP[slug]['ratio']
        vh = round(1000 / ratio, 1)
        lines, chips, pins, cards = [], [], [], []
        for n, it in enumerate(items(slug), 1):
            key = it['key']
            cx, cy = it['circle']
            ax, ay = it['anchor']
            title = NAME_ON.get((slug, key), PRODUCTS[key][0])
            lead, specs = PRODUCTS[key][1], PRODUCTS[key][2] + EXTRA.get((slug, key), [])
            lines.append(
                f'<line class="ev-line" data-key="{key}" x1="{cx * 1000:.1f}" '
                f'y1="{cy * vh:.1f}" x2="{ax * 1000:.1f}" y2="{ay * vh:.1f}"/>')
            lines.append(
                f'<circle class="ev-dot" data-key="{key}" cx="{ax * 1000:.1f}" '
                f'cy="{ay * vh:.1f}" r="5"/>')
            pins.append(
                f'<button type="button" class="ev-pin" data-key="{key}" '
                f'style="left:{ax * 100:.2f}%;top:{ay * 100:.2f}%">{n}</button>')
            side = 'l' if cx < 0.5 else 'r'
            chips.append(
                f'<button type="button" class="ev-chip ev-chip--{side}" data-key="{key}" '
                f'style="left:{cx * 100:.2f}%;top:{cy * 100:.2f}%;width:{it["r"] * 200:.2f}%">'
                f'<img src="{IMG}/chip-{key}.png" alt="{title}" width="440" height="440" '
                f'loading="lazy" decoding="async">'
                f'<span class="ev-chip__tag"><b>{n}</b> {title}</span></button>')
            bullets = ''.join(f'<li>{s}</li>' for s in specs)
            cards.append(
                f'<article class="ev-card" data-key="{key}"><h3><span>{n}</span> {title}</h3>'
                + (f'<p class="ev-card__lead">{lead}</p>' if lead else '')
                + (f'<ul>{bullets}</ul>' if bullets else '')
                + f'<p class="ev-card__where">{WHERE[(slug, key)]}</p></article>')

        w, h = SIZE[f'plate-{slug}']
        panes.append(f'''<div class="ev-pane{" is-on" if i == 0 else ""}" data-obj="{slug}">
 <div class="ev-stage">
  <img class="ev-plate" src="{IMG}/plate-{slug}.jpg" alt="Разрез объекта «{name}» без печатного слоя"
   width="{w}" height="{h}" loading="lazy" decoding="async">
  <svg class="ev-net" viewBox="0 0 1000 {vh}" aria-hidden="true">{''.join(lines)}</svg>
  <div class="ev-pins">{''.join(pins)}</div>
  <div class="ev-chips">{''.join(chips)}</div>
 </div>
 <p class="ev-about"><b>{name}.</b> {about}</p>
 <div class="ev-cards">{''.join(cards)}</div>
</div>''')

    return f'''<section class="ev-scene ev-rev" id="objects"><div class="ev-wrap">
<h2>Три объекта, снятые с плакатов</h2>
<p class="ev-sub">Подложка — чистый рендер: кружки, подписи и линии сняты с печатного файла
 алгоритмом. Всё, что вы видите поверх, нарисовано кодом в тех же координатах, что были
 в печати: линия приходит ровно в ту точку, куда указывала печатная выноска.</p>
<div class="ev-tabs" role="group" aria-label="Тип объекта">{tabs}</div>
</div><div class="ev-wrap ev-wrap--wide">{''.join(panes)}</div></section>'''


def matrix():
    """Библиотека против сцены: 10 позиций × 3 объекта."""
    rows = []
    for key in ORDER:
        title = PRODUCTS[key][0]
        on = objects_of(key)
        cells = ''.join(
            f'<td class="{"is-on" if s in on else ""}"><span class="ev-mx__mark" '
            f'aria-label="{"стоит" if s in on else "нет"}">'
            f'{WHERE.get((s, key), "") if s in on else "—"}</span></td>'
            for s, _, _, _ in OBJECTS)
        rows.append(
            f'<tr data-key="{key}"><th scope="row"><img src="{IMG}/chip-{key}.png" alt="" '
            f'width="440" height="440" loading="lazy" decoding="async">'
            f'<span>{title}</span><b>{len(on)}/3</b></th>{cells}</tr>')
    heads = ''.join(f'<th scope="col">{short}<i>{len(MAP[s]["items"])}</i></th>'
                    for s, _, short, _ in OBJECTS)
    return f'''<section class="ev-mx ev-rev"><div class="ev-wrap">
<h2>Одна библиотека — три расстановки</h2>
<p class="ev-sub">Модели оборудования сделаны один раз и переезжают из сцены в сцену.
 Меняется не библиотека, а набор: четыре позиции нужны любому зданию, шесть выбираются
 под тип объекта. Кружки в таблице — те самые, что стояли на плакатах.</p>
<div class="ev-mx__scroll"><table>
<thead><tr><th scope="col">Позиция Eaton</th>{heads}</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p class="ev-note">ИБП, щиты xEnergy, КРУ Xiria и аварийное освещение стоят на всех трёх
 объектах. Стойки и мониторинг — только в ЦОД, преобразователи частоты и световые
 колонны — только в гипермаркете.</p>
</div></section>'''


def printing():
    posters = ''.join(
        f'<figure class="ev-pr__p"><a href="{IMG}/poster-{s}.jpg" target="_blank" '
        f'rel="noopener">{img("poster-" + s, "Плакат «" + n + "» как он ушёл в печать")}</a>'
        f'<figcaption>{n}<i>{len(MAP[s]["items"])} выносок</i></figcaption></figure>'
        for s, n, short, _ in OBJECTS)
    zooms = ''.join(
        f'<figure class="ev-pr__z{" is-on" if i == 0 else ""}" data-z="{i}">{img(k, c)}</figure>'
        for i, (k, c) in enumerate(ZOOMS))
    picks = ''.join(
        f'<button type="button" class="ev-pr__pick{" is-on" if i == 0 else ""}" '
        f'data-z="{i}">{c}</button>' for i, (k, c) in enumerate(ZOOMS))
    return f'''<section class="ev-pr ev-rev"><div class="ev-wrap">
<h2>Печатный масштаб</h2>
<p class="ev-sub">Плакаты собирались не для экрана: 9449 × 7087 пикселей при 300 dpi —
 это лист 800 × 600 мм, к которому подходят вплотную. Поэтому в сцене прорисованы
 мелочи, которых на экране не видно: маркировка на щитах, ручки шкафов, ценники
 на витринах.</p>
<div class="ev-pr__row">{posters}</div>
<div class="ev-pr__zoom" data-mode="paper">
 <div class="ev-pr__bar">
  <div class="ev-pr__picks">{picks}</div>
  <div class="ev-pr__modes">
   <button type="button" class="ev-pr__mode is-on" data-mode="paper">как на листе</button>
   <button type="button" class="ev-pr__mode" data-mode="pixel">пиксель в пиксель</button>
  </div>
 </div>
 <div class="ev-pr__win">{zooms}
  <div class="ev-pr__ruler" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i>
   <span>5 см на листе</span></div>
 </div>
 <p class="ev-note">Фрагменты вырезаны из печатных файлов. «Как на листе» — тот же
  размер, в котором кусок напечатан на плакате; «пиксель в пиксель» — как он лежит
  в файле, в три с лишним раза крупнее. Сантиметры линейки экранные, у вашего
  монитора масштаб может немного отличаться.</p>
</div></div></section>'''


def how():
    steps = [
        ('Библиотека', 'Модели оборудования Eaton: ИБП, щиты, КРУ, шинопровод, '
                       'пускатели, светильники. Сделаны один раз и переиспользуются.'),
        ('Сцена', 'Три здания в разрезе — планировка, помещения, начинка: стойки, '
                  'витрины, конвейер, погрузчики, столы, стеллажи.'),
        ('Расстановка', 'Инженеры Eaton расставили по каждому объекту типовой набор '
                        'для этого типа здания — как на реальном проекте.'),
        ('Подача', 'Рендер в единой изометрии, кружок с оборудованием, линия в точку '
                   'установки и описание. Свёрстано под лист А1, 300 dpi.'),
    ]
    li = ''.join(f'<li><b>{i}</b><h3>{t}</h3><p>{d}</p></li>'
                 for i, (t, d) in enumerate(steps, 1))
    return f'''<section class="ev-how ev-rev"><div class="ev-wrap">
<h2>Как это собиралось</h2><ol class="ev-how__list">{li}</ol></div></section>'''


def out():
    return '''<section class="ev-out ev-rev"><div class="ev-wrap">
<h2>Результат</h2>
<p>Три плаката, на которых заказчик показывает не каталог, а объект целиком: приходит
 к инженеру или закупщику с листом, где его тип здания уже собран и подписан. Одна
 библиотека 3D-моделей закрыла ЦОД, торговый комплекс и производство — и осталась
 у клиента как основа для следующих материалов.</p>
</div></section>'''


PAGE_CSS = """<style>
:root{--nav:#08243F;--deep:#0C4F8C;--sky:#4E8BC2;--pale:#EDF3FA;--ink:#0E1A26;
 --grey:#5A6B7C;--signal:#00A651;--rule:rgba(255,255,255,.28)}
.ev,.ev *{box-sizing:border-box}
.ev{font-family:'Roboto',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff;
 font-size:17px;line-height:1.55;overflow-x:hidden}
.ev h1,.ev h2,.ev h3{font-family:'Play',Arial,sans-serif;font-weight:700;
 letter-spacing:-.015em;line-height:1.06;margin:0}
.ev h2{font-size:clamp(26px,3.4vw,44px);margin-bottom:14px}
.ev p{margin:0 0 14px}
.ev-wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.ev-wrap--wide{max-width:1360px}
.ev-kicker{font:700 13px/1 'Roboto Condensed',Arial,sans-serif;letter-spacing:.16em;
 text-transform:uppercase;color:#8FBEEA;margin:0 0 20px}
.ev-sub{max-width:760px;color:var(--grey);margin-bottom:26px}
.ev-note{font-size:15px;color:var(--grey)}
.ev-rev{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}
.ev-rev.is-in{opacity:1;transform:none}
.no-js .ev-rev{opacity:1;transform:none}

/* ── герой ── */
.ev-hero{background:linear-gradient(160deg,#0B3766 0%,#08243F 55%,#061B31 100%);
 color:#fff;padding:clamp(48px,7vw,96px) 0 clamp(40px,5vw,72px)}
.ev-hero h1{font-size:clamp(32px,5.4vw,68px);margin-bottom:22px}
.ev-lead{max-width:720px;font-size:clamp(16px,1.5vw,19px);color:rgba(255,255,255,.8)}
.ev-hero__thumbs{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;margin:36px 0 30px}
.ev-hero__t{margin:0}
.ev-hero__t img{width:100%;height:auto;display:block;border-radius:3px;aspect-ratio:4/3;
 object-fit:contain;background:rgba(255,255,255,.05);padding:8px;
 box-shadow:0 18px 46px rgba(0,0,0,.42)}
.ev-hero__t figcaption{font:700 12px/1 'Roboto Condensed',Arial,sans-serif;
 letter-spacing:.14em;text-transform:uppercase;color:#8FBEEA;margin-top:10px}
.ev-nums{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:0;
 border-top:1px solid var(--rule);padding-top:22px}
.ev-nums dt{font:700 clamp(30px,3.6vw,46px)/1 'Play',Arial,sans-serif}
.ev-nums dd{margin:6px 0 0;font-size:14px;color:rgba(255,255,255,.66);max-width:150px}

/* ── задача ── */
.ev-task{padding:clamp(46px,6vw,84px) 0}
.ev-task__grid{display:grid;grid-template-columns:1fr 1fr;gap:44px}
.ev-task h2{font-size:clamp(22px,2.2vw,28px)}

/* ── сцена ── */
.ev-scene{background:var(--nav);color:#fff;padding:clamp(46px,6vw,84px) 0 clamp(40px,5vw,70px)}
.ev-scene .ev-sub{color:rgba(255,255,255,.62)}
.ev-tabs{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:8px}
.ev-tab{display:flex;flex-direction:column;gap:3px;align-items:flex-start;cursor:pointer;
 background:transparent;color:#fff;border:1px solid var(--rule);border-radius:2px;
 padding:11px 18px;font:inherit;transition:background .2s,border-color .2s}
.ev-tab__n{font:700 16px/1 'Play',Arial,sans-serif}
.ev-tab__c{font:500 12px/1 'Roboto Condensed',Arial,sans-serif;letter-spacing:.1em;
 text-transform:uppercase;color:rgba(255,255,255,.55)}
.ev-tab:hover{border-color:rgba(255,255,255,.6)}
.ev-tab.is-on{background:#fff;color:var(--nav);border-color:#fff}
.ev-tab.is-on .ev-tab__c{color:rgba(8,36,63,.6)}
.ev-pane{display:none}
.ev-pane.is-on{display:block}
.ev-stage{position:relative;container-type:inline-size;margin-top:22px}
.ev-plate{width:100%;height:auto;display:block;border-radius:3px}
.ev-net{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.ev-net .ev-line{stroke:rgba(255,255,255,.75);stroke-width:1.6;transition:stroke .2s}
.ev-net .ev-dot{fill:#fff;opacity:.9;transition:fill .2s,r .2s}
.ev-pins{position:absolute;inset:0;pointer-events:none}
.ev-pin{position:absolute;transform:translate(-50%,-50%);width:26px;height:26px;
 border-radius:50%;border:2px solid #fff;background:rgba(8,36,63,.85);color:#fff;
 font:700 13px/1 'Play',Arial,sans-serif;cursor:pointer;pointer-events:auto;
 display:none;align-items:center;justify-content:center;padding:0}
.ev-chips{position:absolute;inset:0;pointer-events:none}
.ev-chip{position:absolute;transform:translate(-50%,-50%);aspect-ratio:1;padding:0;border:0;
 background:transparent;cursor:pointer;pointer-events:auto}
.ev-chip img{width:100%;height:100%;display:block;border-radius:50%;
 box-shadow:0 6px 22px rgba(0,0,0,.28);transition:transform .25s}
.ev-chip__tag{position:absolute;top:50%;transform:translateY(-50%);width:190%;
 font:500 clamp(9px,1.2cqw,13px)/1.25 'Roboto Condensed',Arial,sans-serif;
 color:#fff;text-align:left;pointer-events:none}
.ev-chip__tag b{display:block;font:700 clamp(10px,1.25cqw,14px)/1 'Play',Arial,sans-serif;
 color:#8FBEEA;margin-bottom:3px}
.ev-chip--l .ev-chip__tag{left:118%}
.ev-chip--r .ev-chip__tag{left:112%;width:150%}
.ev-chip:hover img,.ev-chip.is-on img{transform:scale(1.06)}
.ev-stage[data-active] .ev-chip:not(.is-on) img{opacity:.45}
.ev-stage[data-active] .ev-chip:not(.is-on) .ev-chip__tag{opacity:.45}
.ev-about{margin:18px 0 0;max-width:820px;color:rgba(255,255,255,.72);font-size:16px}
.ev-about b{color:#fff}
.ev-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:2px;
 margin-top:26px}
.ev-card{background:#0B2E4E;padding:20px 20px 18px;transition:background .2s}
.ev-card.is-on{background:#0D3557}
.ev-card h3{font-size:17px;display:flex;gap:9px;align-items:baseline;margin-bottom:10px}
.ev-card h3 span{font:700 12px/1.6 'Play',Arial,sans-serif;color:var(--nav);
 background:#8FBEEA;border-radius:2px;min-width:20px;height:20px;display:inline-flex;
 align-items:center;justify-content:center;flex:none}
.ev-card__lead{font-size:14px;color:rgba(255,255,255,.75);margin-bottom:10px}
.ev-card ul{margin:0;padding:0;list-style:none}
.ev-card li{position:relative;padding-left:13px;font:400 13.5px/1.45 'Roboto',Arial,sans-serif;
 color:rgba(255,255,255,.72);margin-bottom:7px}
.ev-card li:before{content:'';position:absolute;left:0;top:8px;width:5px;height:1px;
 background:#8FBEEA}
.ev-card__where{margin:12px 0 0;font:700 11px/1 'Roboto Condensed',Arial,sans-serif;
 letter-spacing:.14em;text-transform:uppercase;color:var(--signal)}
.ev-stage[data-active] .ev-line{stroke:rgba(255,255,255,.22)}
.ev-stage[data-active] .ev-dot{fill:rgba(255,255,255,.35)}
.ev-stage[data-active] .ev-line.is-on{stroke:var(--signal);stroke-width:2.4}
.ev-stage[data-active] .ev-dot.is-on{fill:var(--signal);r:8}

/* ── матрица ── */
.ev-mx{padding:clamp(46px,6vw,84px) 0}
.ev-mx__scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.ev-mx table{width:100%;border-collapse:collapse;min-width:640px}
.ev-mx th,.ev-mx td{text-align:left;padding:12px 14px;border-bottom:1px solid #E2E9F2}
.ev-mx thead th{font:700 12px/1 'Roboto Condensed',Arial,sans-serif;letter-spacing:.14em;
 text-transform:uppercase;color:var(--grey);border-bottom:2px solid var(--ink);
 vertical-align:bottom}
.ev-mx thead th i{display:block;font:700 20px/1.2 'Play',Arial,sans-serif;color:var(--ink);
 font-style:normal;margin-top:6px}
.ev-mx tbody th{display:flex;align-items:center;gap:12px;font-weight:500;font-size:15.5px}
.ev-mx tbody th img{width:44px;height:44px;flex:none;border-radius:50%;background:#fff;
 box-shadow:0 2px 10px rgba(14,26,38,.14)}
.ev-mx tbody th b{margin-left:auto;font:700 13px/1 'Play',Arial,sans-serif;color:var(--grey)}
.ev-mx td{color:#A9B6C4;font:500 13px/1 'Roboto Condensed',Arial,sans-serif;
 letter-spacing:.06em;text-transform:uppercase}
.ev-mx td.is-on{color:var(--ink)}
.ev-mx td.is-on .ev-mx__mark:before{content:'';display:inline-block;width:8px;height:8px;
 border-radius:50%;background:var(--signal);margin-right:8px;vertical-align:middle}
.ev-mx tbody tr:hover{background:var(--pale)}

/* ── печать ── */
.ev-pr{background:var(--pale);padding:clamp(46px,6vw,84px) 0}
.ev-pr__row{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:40px}
.ev-pr__p{margin:0}
.ev-pr__p img{width:100%;height:auto;display:block;border-radius:2px;aspect-ratio:4/3;
 object-fit:contain;background:#fff;padding:10px;
 box-shadow:0 12px 34px rgba(12,42,74,.18)}
.ev-pr__p figcaption{display:flex;justify-content:space-between;gap:10px;margin-top:10px;
 font:700 12px/1.3 'Roboto Condensed',Arial,sans-serif;letter-spacing:.1em;
 text-transform:uppercase;color:var(--grey)}
.ev-pr__p i{font-style:normal;color:var(--deep)}
.ev-pr__bar{display:flex;flex-wrap:wrap;gap:14px;justify-content:space-between;
 align-items:flex-end;margin-bottom:14px}
.ev-pr__picks,.ev-pr__modes{display:flex;flex-wrap:wrap;gap:8px}
.ev-pr__pick,.ev-pr__mode{cursor:pointer;background:transparent;border:1px solid #C3D3E5;
 border-radius:2px;padding:7px 12px;color:var(--grey);
 font:700 12px/1.2 'Roboto Condensed',Arial,sans-serif;letter-spacing:.08em;
 text-transform:uppercase;transition:background .2s,color .2s,border-color .2s}
.ev-pr__pick:hover,.ev-pr__mode:hover{border-color:var(--deep);color:var(--deep)}
.ev-pr__pick.is-on,.ev-pr__mode.is-on{background:var(--deep);border-color:var(--deep);color:#fff}
.ev-pr__win{position:relative;height:min(72vw,470px);overflow:hidden;border-radius:2px;
 background:#DCE7F3;box-shadow:inset 0 0 0 1px rgba(12,79,140,.16)}
.ev-pr__z{margin:0;position:absolute;inset:0;display:none;align-items:center;
 justify-content:center}
.ev-pr__z.is-on{display:flex}
.ev-pr__z img{display:block;flex:none;width:1400px;max-width:none;height:auto;
 transform:scale(var(--k,.32));transform-origin:center;transition:transform .45s ease}
.ev-pr__zoom[data-mode="pixel"] .ev-pr__z img{--k:1}
.ev-pr__ruler{position:absolute;left:20px;bottom:18px;display:flex;align-items:flex-end;
 gap:0;pointer-events:none;transition:opacity .3s}
.ev-pr__ruler i{width:calc(100mm / 10);height:9px;border:1px solid rgba(12,42,74,.75);
 border-right:0;background:rgba(255,255,255,.55)}
.ev-pr__ruler i:nth-child(odd){background:rgba(12,42,74,.75)}
.ev-pr__ruler i:last-of-type{border-right:1px solid rgba(12,42,74,.75)}
.ev-pr__ruler span{margin-left:8px;font:700 11px/1 'Roboto Condensed',Arial,sans-serif;
 letter-spacing:.1em;text-transform:uppercase;color:#0C2A4A}
.ev-pr__zoom[data-mode="pixel"] .ev-pr__ruler{opacity:0}

/* ── как собиралось ── */
.ev-how{padding:clamp(46px,6vw,84px) 0}
.ev-how__list{list-style:none;margin:0;padding:0;display:grid;
 grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:26px}
.ev-how__list li{border-top:2px solid var(--ink);padding-top:14px}
.ev-how__list b{font:700 13px/1 'Play',Arial,sans-serif;color:var(--deep)}
.ev-how__list h3{font-size:20px;margin:10px 0 8px}
.ev-how__list p{font-size:15px;color:var(--grey);margin:0}

/* ── результат ── */
.ev-out{background:var(--nav);color:#fff;padding:clamp(46px,6vw,80px) 0}
.ev-out p{max-width:760px;font-size:clamp(16px,1.5vw,19px);color:rgba(255,255,255,.82)}

@media(max-width:1000px){
 .ev-chips{display:none}
 .ev-net{display:none}
 .ev-pin{display:inline-flex}
 .ev-card h3 span{background:#8FBEEA}
 .ev-task__grid{grid-template-columns:1fr;gap:26px}
 .ev-pr__row{grid-template-columns:1fr;gap:26px}
 .ev-hero__thumbs{grid-template-columns:1fr 1fr 1fr;gap:10px}
 .ev-nums{grid-template-columns:1fr 1fr;gap:14px}
}
@media(max-width:640px){
 .ev{font-size:16px}
 .ev-wrap{padding:0 16px}
 .ev-hero__thumbs{grid-template-columns:1fr;gap:14px}
 .ev-tab{flex:1 1 100%}
 .ev-cards{grid-template-columns:1fr}
 .ev-pr__z img{width:min(1400px,86vw)}
}
</style>"""

PAGE_JS = """<script>(function(){
 var scene=document.querySelector('.ev-scene');
 if(!scene)return;
 /* переключатель объектов */
 var tabs=[].slice.call(scene.querySelectorAll('.ev-tab'));
 var panes=[].slice.call(scene.querySelectorAll('.ev-pane'));
 tabs.forEach(function(t){
  t.addEventListener('click',function(){
   tabs.forEach(function(o){o.classList.toggle('is-on',o===t);
    o.setAttribute('aria-pressed',o===t?'true':'false');});
   panes.forEach(function(p){p.classList.toggle('is-on',p.dataset.obj===t.dataset.obj);});
  });
 });
 /* подсветка выноски: кружок, точка, линия и карточка — один data-key */
 panes.forEach(function(pane){
  var stage=pane.querySelector('.ev-stage');
  var parts=[].slice.call(pane.querySelectorAll('[data-key]'));
  function set(key){
   if(key){stage.setAttribute('data-active',key);}else{stage.removeAttribute('data-active');}
   parts.forEach(function(el){el.classList.toggle('is-on',!!key&&el.dataset.key===key);});
  }
  parts.forEach(function(el){
   el.addEventListener('mouseenter',function(){set(el.dataset.key);});
   el.addEventListener('focus',function(){set(el.dataset.key);});
   if(el.tagName==='BUTTON')el.addEventListener('click',function(){
    set(stage.getAttribute('data-active')===el.dataset.key?null:el.dataset.key);});
  });
  pane.addEventListener('mouseleave',function(){set(null);});
 });
})();
(function(){
 /* печатный масштаб: выбор фрагмента и переключатель «лист / пиксели» */
 var zoom=document.querySelector('.ev-pr__zoom');
 if(!zoom)return;
 var figs=[].slice.call(zoom.querySelectorAll('.ev-pr__z'));
 var picks=[].slice.call(zoom.querySelectorAll('.ev-pr__pick'));
 var modes=[].slice.call(zoom.querySelectorAll('.ev-pr__mode'));
 picks.forEach(function(b){b.addEventListener('click',function(){
  picks.forEach(function(o){o.classList.toggle('is-on',o===b);});
  figs.forEach(function(f){f.classList.toggle('is-on',f.dataset.z===b.dataset.z);});
 });});
 modes.forEach(function(b){b.addEventListener('click',function(){
  modes.forEach(function(o){o.classList.toggle('is-on',o===b);});
  zoom.setAttribute('data-mode',b.dataset.mode);
 });});
})();
(function(){
 var els=[].slice.call(document.querySelectorAll('.ev-rev'));
 if(!els.length)return;
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

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>3D-визуализация оборудования Eaton: ЦОД, гипермаркет, завод | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing для Eaton: три объекта в 3D — центр обработки данных, коммерческий и промышленный объект. Типовое размещение оборудования Eaton, 20 выносок, 10 позиций, печатные плакаты 300 dpi.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="3D-визуализация решений Eaton для ЦОД, коммерческих и промышленных объектов">
<meta property="og:description" content="Печатный слой снят с плакатов и собран заново: кружки оборудования и линии-выноски живут поверх чистого рендера в тех же координатах, что были в печати.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/poster-dc.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/play-roboto.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"3D-визуализация решений Eaton",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    body = (f'{rc.header()}<main class="ev">{hero()}{task()}{scene()}{matrix()}'
            f'{printing()}{how()}{out()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'creative', 'eaton', 'visual')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
