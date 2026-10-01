#!/usr/bin/env python3
"""Собирает приватную страницу /for/alidi/ (ГК АЛИДИ, имиджевый фильм к 35-летию).

Выход:
  mirror/for/alidi/index.php           калитка с паролем + страница (идёт на прод)
  mirror/for/alidi/_preview-page.html  страница без PHP, для локального превью (не коммитить)
  mirror/for/alidi/_preview-gate.html  экран пароля без PHP (не коммитить)

Тексты и факты: scripts/alidi-page/brief.md (раздел 7 «Все остальные проекты» парсится из него).
Пересборка: python3 scripts/alidi-page/build.py
"""
import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'mirror' / 'for' / 'alidi'

ACCESS_HASH = '156abb09c845b428d02f8822a212502a76306d57c6d0eba3ba689d08c8bd778c'
SITE = 'https://hand-marketing.ru'
e = html.escape


def rel(url):
    """Ссылки на кейсы оставляем абсолютными, картинки берём с того же домена."""
    return url.replace(SITE, '') if url.startswith(SITE + '/images/') else url


# ---------- логотип АЛИДИ: чёрные части через currentColor, синий треугольник свой ----------
alidi_svg = (HERE / 'alidi-logo.svg').read_text(encoding='utf8')
alidi_svg = re.sub(r'<\?xml[^>]*>', '', alidi_svg)
alidi_svg = alidi_svg.replace('fill="#141417"', 'fill="currentColor"')
alidi_svg = re.sub(r'<svg width="260" height="46"', '<svg class="alidi-logo" role="img" aria-label="АЛИДИ"', alidi_svg, count=1)
alidi_svg = alidi_svg.replace('clip0_14_377', 'alc')
alidi_svg = re.sub(r'\s*\n\s*', ' ', alidi_svg).strip()

TRI = '<svg class="tri" viewBox="0 0 22 12" aria-hidden="true"><path d="M0 12 11 0 22 12z"/></svg>'

# ---------- раздел 7 из брифа ----------
brief = (HERE / 'brief.md').read_text(encoding='utf8')
part7 = brief.split('## 7. Все остальные проекты')[1].split('\n---')[0]
CATS = []
DROP = {'https://hand-marketing.ru/event/messeduessleldorf'}  # решение владельца 01.10: не показывать
DROP_CATS = {'Сайты и посадочные страницы'}
for block in re.split(r'\n### ', part7)[1:]:
    head, *items = re.split(r'\n#### ', block)
    cat = head.strip().split('\n')[0]
    if cat in DROP_CATS:
        continue
    cards = []
    for it in items:
        lines = [l for l in it.strip().split('\n') if l.strip()]
        title = lines[0].strip()
        link = re.search(r'Ссылка: (\S+)', it).group(1)
        cover = re.search(r'Обложка: (\S+)', it).group(1)
        desc = [l for l in lines[1:] if not l.startswith('- ')][-1].strip()
        client, _, name = title.partition(': ')
        cards.append(dict(client=client, name=name or client, link=link, cover=rel(cover), desc=desc))
    cards = [c for c in cards if c['link'] not in DROP]
    if cards:
        CATS.append((cat, cards))

CAT_SHORT = {
    'Рекламные, выставочные и репортажные ролики': ('video', 'Ролики'),
    'Дизайн и графика': ('design', 'Дизайн и 3D'),
    'Полиграфия и айдентика для Becar': ('print', 'Полиграфия'),
    'Мероприятия, стенды, шоу и трансляции': ('event', 'События и стенды'),
    'Сайты и посадочные страницы': ('web', 'Сайты'),
}

# ---------- карта съёмочных площадок ----------
SITES = [  # имя, долгота, широта, страна, что там, сдвиг подписи
    ('Минск', 27.56, 53.90, 'РБ', 'офис и склад', (0, 30)),
    ('Москва', 37.62, 55.75, 'РФ', 'головной офис', (-14, -34)),
    ('Валищево', 37.48, 55.33, 'РФ', 'складской комплекс', (14, 30)),
    ('Нижний Новгород', 44.00, 56.33, 'РФ', 'офис и склад', (14, -34)),
    ('Алматы', 76.95, 43.24, 'РК', 'офис и склад', (0, -26)),
]


def proj(lon, lat):
    k = 17.5
    return round(60 + (lon - 26) * math.cos(math.radians(50)) * k, 1), round(40 + (58 - lat) * k, 1)


def map_svg():
    mx, my = proj(37.62, 55.75)
    parts = ['<svg class="geo-svg" viewBox="0 0 680 330" role="img" aria-label="Пять съёмочных площадок: Москва, Валищево, Нижний Новгород, Минск, Алматы">']
    # сетка-меридианы, чтобы карта читалась как карта, а не как схема
    for lon in range(30, 80, 10):
        x, _ = proj(lon, 50)
        parts.append(f'<line class="mer" x1="{x}" y1="18" x2="{x}" y2="312"/><text class="deg" x="{x+4}" y="314">{lon}°</text>')
    for lat in (45, 50, 55):
        _, y = proj(30, lat)
        parts.append(f'<line class="mer" x1="20" y1="{y}" x2="660" y2="{y}"/><text class="deg" x="22" y="{y-4}">{lat}°</text>')
    for i, (n, lon, lat, c, what, off) in enumerate(SITES):
        x, y = proj(lon, lat)
        if n != 'Москва':
            cx, cy = (mx + x) / 2, min(my, y) - 26 - abs(x - mx) * 0.12
            if n == 'Валищево':
                cx, cy = mx + 30, (my + y) / 2
            parts.append(f'<path class="route" style="--d:{i*0.35}s" d="M{mx},{my} Q{cx:.1f},{cy:.1f} {x},{y}"/>')
    for i, (n, lon, lat, c, what, off) in enumerate(SITES):
        x, y = proj(lon, lat)
        tx, ty = x + off[0], y + off[1]
        anchor = {'Москва': 'end', 'Валищево': 'start', 'Нижний Новгород': 'start'}.get(n, 'middle')
        parts.append(
            f'<g class="pt pt-{c}" style="--d:{i*0.35+0.4}s"><circle class="halo" cx="{x}" cy="{y}" r="11"/>'
            f'<path class="tri-pt" d="M{x-7},{y+5} L{x},{y-7} L{x+7},{y+5}z"/>'
            f'<text x="{tx}" y="{ty}" text-anchor="{anchor}"><tspan class="nm">{e(n)}</tspan>'
            f'<tspan class="cc" x="{tx}" dy="15">{c} · {e(what)}</tspan></text></g>')
    parts.append('</svg>')
    return ''.join(parts)


# ---------- данные разделов ----------
TZ = [
    ('2', 'версии фильма', 'Презентационная 2:30-3:00 и мини-фильм 4:00-5:00. Горизонталь для зала, ТВ и ПК.'),
    ('5', 'съёмочных площадок', 'Москва, Валищево, Нижний Новгород, Минск, Алматы. Офисы и склады.'),
    ('3', 'страны в смете', 'Организация съёмок в РФ, РБ и РК отдельными разделами, как просит ТЗ.'),
    ('2', 'концепции на старте', 'Два сценария на выбор, дальше детальная доработка выбранного.'),
    ('3', 'круга правок', 'Включены в стоимость. Под ключ: идея, сценарий, съёмки, дизайн, озвучка, монтаж.'),
    ('26.07', '2027, сдача', 'Обе версии согласованы. Старт съёмок 1 февраля 2027 года.'),
]

MATCH = [
    ('Склад, погрузчик, отгрузка, фура в кадре',
     'Saint-Gobain «Клиентский опыт»: путь одного заказа через закупку, линию, склад, отгрузку и доставку.',
     '/video/saintgobain/cx', ['/images/sgcx/sc-pallets.jpg', '/images/sgcx/sc-truck@560.jpg', '/images/sgcx/sc-shipping-doc@560.jpg']),
    ('Логистическая сеть в разных городах',
     'ЦМ РЖД: три группы параллельно в Москве, Петербурге и Калининграде, грузовые дворы с земли и сверху.',
     '/video/rgd/history', ['/images/rgd-history/aero-station.jpg', '/images/rgd-history/baltkran.jpg', '/images/rgd-history/aero-kal.jpg']),
    ('Офис и прямая речь руководителей',
     'Saint-Gobain: 17 интервью руководителей всех направлений, в московском офисе и на заводе. Свет, кадр и вопросы готовили на месте под каждого спикера.',
     '/video/saintgobain/cx', ['/images/sgcx/sp-01.jpg', '/images/sgcx/sp-06.jpg', '/images/sgcx/sp-07.jpg', '/images/sgcx/sp-12.jpg']),
    ('История компании по годам',
     'Бренд-ролик «Изотек»: 2012-2024, девять вех, шесть площадок, цифры итога в финале.',
     '/isotec', ['/images/isotec/map.jpg', '/images/isotec/prod-5.jpg', '/images/isotec/prod-4.jpg']),
    ('Две версии одного фильма',
     'Power Technologies: полная 11:39 для переговоров и короткая 4:27 для соцсетей и стенда.',
     '/video/powertechnologies', ['/images/powertech/poster-full.jpg', '/images/powertech/poster-short.jpg']),
]

FILMS = [
    dict(id='sgcx', color='#5a9a2c', tag='Корпоративный фильм · программа «Клиентский опыт»',
         title='Saint-Gobain: один заказ через всю компанию',
         accent='Реклама, закупка, линия, склад, отгрузка, фура, монтаж. Без пропусков.',
         text='Saint-Gobain запускал внутри компании программу «Клиентский опыт» и хотел объяснить каждому сотруднику простую вещь: путь клиента складывается из работы всех подразделений, даже тех, кто клиента ни разу не видит. Первая часть фильма проходит весь путь заказа: реклама, выбор, закупка сырья, планирование, смена на линии, склад, отгрузка, доставка, монтаж и готовый дом. Вторая собирает прямую речь руководителей всех направлений. Две смены в московском офисе, одна смена на двух заводах в Егорьевске. Руководителей из Казахстана и Беларуси сняли отдельно и собрали в общий монтаж.',
         stats=[('10 мин', 'две части фильма: путь клиента и голоса руководителей'), ('17', 'интервью, от операционного директора до глав компании в Казахстане и Беларуси'),
                ('48', 'сотрудников названы в кадре по имени, на своих рабочих местах'), ('3 смены', 'офис в Москве и два завода в Егорьевске')],
         video='/media/sg-cx-part1.mp4', poster='/images/sgcx/hero-poster.jpg', link='/video/saintgobain/cx',
         parts=('Часть 1 · путь клиента', 'Часть 2 · голоса руководителей'), video2='/media/sg-cx-part2.mp4', poster2='img/sg-leaders.jpg'),
    dict(id='rgd', color='#e2661c', tag='Корпоративный фильм к десятилетию дирекции',
         title='ЦМ РЖД: терминально-складское хозяйство за 3:54',
         accent='Грузовой двор, где вагон встречается с автомобилем и складом.',
         text='Центральная дирекция по управлению терминально-складским комплексом держит грузовые дворы по всей стране, от Калининграда до Находки. За 3:54 фильм показывает, что это за хозяйство, чем оно занято каждый день и что изменилось за десять лет. Три съёмочные группы вышли параллельно, снимали действующие терминалы с земли и с квадрокоптера, слайды дирекции пересобрали в экранную графику. Итог десяти лет проговаривает начальник дирекции.',
         stats=[('3 группы', 'параллельно: Москва, Санкт-Петербург, Калининград'), ('117', 'планов в фильме, средняя длина 2 секунды'),
                ('15', 'городов на карте сети терминалов, с запада на восток')],
         video='/media/transrzhd.mp4', poster='/images/rgd-history/poster.jpg', link='/video/rgd/history'),
    dict(id='isotec', color='#9b2a8a', tag='Имиджевый фильм · Saint-Gobain · ISOTEC · 2024',
         title='«Изотек»: двенадцать лет бренда в одной истории',
         accent='От образования направления до криогенной изоляции.',
         text='Ролик показывает «Изотек» как живой бренд с историей, а не как поставщика материалов. Работает в двух контурах: для клиентов, партнёров и отраслевых событий и для внутренних коммуникаций и адаптации сотрудников. Структура: пролог, хронология, география, производство, цифровые сервисы, итоги. Съёмки на действующих производственных площадках по регламентам СИЗ.',
         stats=[('4:33', 'хронометраж фильма'), ('9 вех', '2012-2024, каждая вынесена в экранную графику'), ('6', 'площадок с реальными кадрами производства')],
         video='/media/izotek-brand-video.mp4', poster='/images/isotec/poster.jpg', link='/isotec'),
    dict(id='pt', color='#1f8a85', tag='История успеха · Чемпионат мира по футболу 2018',
         title='Power Technologies: фильм снят, пока шёл проект',
         accent='Одиннадцать городов, двенадцать стадионов, месяц съёмок.',
         text='Power Technologies обеспечивала временное энергоснабжение всех объектов чемпионата. Мобильные группы (оператор, репортёр, полевой директор, техспециалист) месяц собирали материал в городах: объекты, работу смен, синхроны руководителей проекта и вещателей. По просьбе заказчика фильм собран в двух версиях.',
         stats=[('11', 'городов от Калининграда до Екатеринбурга и Сочи'), ('2 версии', 'полная 11:39 для переговоров и короткая 4:27 для соцсетей и стенда'),
                ('12', 'стадионов в кадре, плюс вещательный центр и фан-зоны')],
         video='/media/pt-film-short.mp4', poster='/images/powertech/poster-short.jpg', link='/video/powertechnologies'),
]

PLACES = [
    ('Технопарк «Зубово»', 'Башкортостан · 3:04', 'Живая промышленная площадка под Уфой: корпуса, инженерия, облёт территории, синхроны руководства. Более 70 гектаров.',
     '/media/technopark-zubovo.mp4', '/images/zubovo/poster.jpg', '/zubovo'),
    ('Технопарк «Бекабад»', 'Узбекистан · 2:34', 'Площадка в Ташкентской области, которую Башкортостан строит вместе с Узбекистаном. Мастер-план поднимается поверх аэросъёмки реального участка.',
     '/media/bekabad-hd.mp4', '/images/bekabad/poster.jpg', '/bekobod1'),
    ('ТРЦ «Павелецкая Плаза»', 'MMG · 5:37', 'Фильм для арендаторов объекта на стройке: локация, трафик, аудитория, готовность. В первом кадре знак победителя MIPIM 2020.',
     '/media/mmg-paveleckayaplaza.mp4', '/images/mmg/poster.jpg', '/mmg'),
]

SERIES = [
    ('17', 'роликов', 'CeramicaNova', 'По фильму на коллекцию санфарфора. Предметная макросъёмка, смыв на подкрашенной воде, 16:9 и 1:1.', '/portfolio/ceramicanova', '/images/lib/custom-ceramicanova/cover-main.png'),
    ('10', 'роликов', 'OBO Bettermann', 'Съёмка в шоу-руме Академии OBO. Эксперт компании разбирает продукт: назначение, устройство, монтаж.', '/portfolio/obo-academy', '/images/lib/custom-obo-academy/cover-main.png'),
    ('19:30', 'минут курса', 'Saint-Gobain, обучение', 'Курс для руководителей: 28 экранов графики, 9 игровых сцен, 4 актёра, разбор поверх кадра.', '/video/saintgobain/training', '/images/lib/custom-sgtraining/cover-main.png'),
    ('63', 'позиции за смену', 'Saint-Gobain, Gyproc', 'Предметная съёмка на площадке заказчика: 62 кадра в сдаче под каталог, сайт и POS.', '/photo/saint-gobain', '/images/lib/custom-sgphoto/cover-main.png'),
]

SKILLS = [  # что умеем → где это видно
    ('Две концепции и сценарий', 'Предлагаем два хода на выбор и доводим выбранный до покадрового сценария.', 'Газель-трансформер', '/video/gaz'),
    ('Съёмка на складе и в цеху', 'Работаем на действующих площадках по регламентам СИЗ, не останавливая смену.', '«Изотек»', '/isotec'),
    ('Несколько групп одновременно', 'Параллельные выезды в разные города с одним режиссёрским планом.', 'ЦМ РЖД', '/video/rgd/history'),
    ('Аэросъёмка', 'Территория, терминалы и подъездные пути сверху, с квадрокоптера.', 'Технопарк «Зубово»', '/zubovo'),
    ('Синхроны и интервью', 'Ставим свет и кадр в кабинете и на рабочем месте, готовим вопросы со спикером.', 'Saint-Gobain', '/video/saintgobain/cx'),
    ('Экранная графика и 3D', 'От полностью смоделированного запуска ракеты в космос до контента на все экраны стенда, плюс ежедневные репортажи и трансляции.', 'стенд Самары на ВДНХ', '/portfolio/samara-stand-vdnh'),
    ('Озвучка и языки', 'Дикторский текст, английская версия, вшитые субтитры.', 'Eaton для выставки', '/video/eaton'),
    ('Версии под площадки', 'Длинная для зала и переговоров, короткая для экранов и соцсетей, из одного материала.', 'Power Technologies', '/video/powertechnologies'),
]

# Отзывы: дословно из scripts/a2/reviews.json (благодарственные письма, согласие клиентов есть). Первый крупно.
import json
_REV = json.loads((ROOT / 'scripts' / 'a2' / 'reviews.json').read_text(encoding='utf8'))
_REV = [v for k, v in _REV.items() if isinstance(v, dict)]
REVIEWS = []
for comp, person in [('Saint-Gobain', 'Татьяна Дулуба'), ('ЦМ РЖД', 'А. Ю. Бельский'), ('Eaton', 'А. К. Бурочкин'),
                     ('Becar Asset Management', 'Д. С. Сороколетов|2018'), ('МФК «Саларис» (АО «ЛАУТ»)', 'Т. В. Левченко')]:
    name, _, year = person.partition('|')
    r = next(v for v in _REV if v['company'] == comp and v['person'] == name and (not year or v.get('year') == year))
    REVIEWS.append(r)

STEPS = [
    ('01', 'Онлайн-встреча', 'Приоритет площадок показа, обязательные объекты, утверждённые цифры, бренды партнёров в кадре.'),
    ('02', 'Коммерческое предложение', 'Две концепции, календарь до 26 июля 2027, смета построчно: концепция, РФ, РБ, РК, дизайн, пост, правки.'),
    ('03', 'Видео-скаут площадок', 'Удалённый осмотр пяти объектов до фиксации сметы: окна активности, свет, маршруты, допуски.'),
]


def full(u):
    return u if u.startswith('http') else SITE + u


def vid(src, poster, label, cls=''):
    return (f'<button class="vid {cls}" type="button" data-video="{src}" aria-label="Смотреть: {e(label)}">'
            f'<img src="{poster}" alt="" loading="lazy" width="1280" height="720"><span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></button>')


def part_html(f):
    if not f.get('video2'):
        return vid(f['video'], f['poster'], f['title'])
    a, b = f['parts']
    return (f'<p class="part">{a}</p>{vid(f["video"], f["poster"], f["title"] + ", " + a)}'
            f'<p class="part">{b}</p>{vid(f["video2"], f["poster2"], f["title"] + ", " + b)}')


# ---------- HTML ----------
def page():
    o = []
    a = o.append
    a('<header class="top"><div class="wrap top-in">'
      f'<a class="brand" href="#top" aria-label="В начало">{alidi_svg}<i></i><img src="hm-logo.svg" alt="Hand Marketing" width="34" height="34"></a>'
      '<nav class="nav"><a href="#tz">ТЗ</a><a href="#match">Опыт</a><a href="#films">Фильмы</a><a href="#skills">Умеем</a><a href="#all">Все работы</a><a href="#next">Дальше</a></nav>'
      '<a class="pdf-btn" href="?pdf=1">PDF</a></div></header>')

    # 1. первый экран
    a('<section class="hero" id="top">'
      '<video class="hero-bg" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="auto" poster="img/hero-loop.jpg" aria-hidden="true" tabindex="-1">'
      '<source src="img/hero-loop.mp4" type="video/mp4"></video><div class="wrap">'
      f'<p class="eyebrow light">{TRI}ГК АЛИДИ · имиджевый фильм к 35-летию</p>'
      '<h1>Наши работы<br>и как мы их снимали.</h1>'
      '<p class="lead">Корпоративные и имиджевые фильмы, съёмки на заводах, складах и терминалах, серии роликов, графика. Каждый проект со ссылкой на страницу кейса с видео.</p>'
      '<div class="hero-cta"><a class="btn" href="#match">Что из задачи мы уже снимали</a>'
      '</div>'
      '<div class="clock" id="clock">'
      '<div class="clock-n"><b id="days">330</b><span>дней до 35-летия АЛИДИ<br>26 августа 2027</span></div>'
      '<div class="line" aria-hidden="true"><i class="now" id="now"></i>'
      '<span class="mk" style="--p:0%"><b>сегодня</b></span>'
      '<span class="mk" data-d="2027-02-01"><b>1 февраля</b>старт съёмок</span>'
      '<span class="mk blue" data-d="2027-07-26"><b>26 июля</b>сдача фильма</span>'
      '<span class="mk end" data-d="2027-08-26"><b>26 августа</b>юбилей</span></div></div>'
      '<p class="sign">ООО «Хэнд-маркетинг» · с 2012 года · hand-marketing.ru</p>'
      '</div></section>')

    # 2. как прочитали ТЗ
    a('<section class="sec" id="tz"><div class="wrap">'
      f'<p class="eyebrow">{TRI}<b>01</b> Задача</p><h2>Как мы прочитали ТЗ.</h2><div class="tz">')
    for n, cap, txt in TZ:
        a(f'<div class="tz-c"><b class="n">{n}</b><span class="cap">{cap}</span><p>{txt}</p></div>')
    a('</div><div class="note"><b>Сверили даты с alidi.ru.</b> Компания основана в 1992 году, 34 года исполнилось 26 августа 2026. Значит, 35 лет будет 26 августа 2027, и сдача 26 июля ложится ровно за месяц до юбилея. В ТЗ указан август 2026, это стоит поправить до сценария.</div>'
      '<div class="geo"><div class="geo-t"><h3>Пять площадок, три страны, одна съёмочная группа</h3>'
      '<p>Фильм в трёх странах собираем с одним режиссёром и оператором-постановщиком на всех площадках, чтобы Минск, Алматы и Валищево выглядели как одна компания.</p>'
      '<ul class="geo-l"><li><i class="c-rf"></i>РФ · 3 площадки</li><li><i class="c-rb"></i>РБ · Минск</li><li><i class="c-rk"></i>РК · Алматы</li></ul></div>'
      f'<div class="geo-m">{map_svg()}</div></div>'
      '</div></section>')

    # 3. что уже снимали
    a('<section class="sec dark" id="match"><div class="wrap">'
      f'<p class="eyebrow light">{TRI}<b>02</b> Опыт под задачу</p><h2>Что из этой задачи мы уже снимали.</h2>'
      '<div class="match"><div class="m-list" role="tablist">')
    for i, (need, where, link, imgs) in enumerate(MATCH):
        a(f'<button class="m-row{" on" if i == 0 else ""}" type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-i="{i}"><span class="m-n">0{i+1}</span><span class="m-need">{e(need)}</span></button>')
    a('</div><div class="m-panes">')
    for i, (need, where, link, imgs) in enumerate(MATCH):
        shots = ''.join((f'<figure><img src="{x.split("|")[0]}" alt="" loading="lazy"><figcaption>{x.split("|")[1]}</figcaption></figure>' if '|' in x
                         else f'<figure><img src="{x}" alt="" loading="lazy"></figure>') for x in imgs)
        a(f'<div class="m-pane{" on" if i == 0 else ""}" role="tabpanel" data-i="{i}"><div class="m-shots n{len(imgs)}">{shots}</div>'
          f'<p class="m-need-m">{e(need)}</p><p>{e(where)}</p><a class="m-link" href="{full(link)}" target="_blank" rel="noopener">{full(link).replace("https://", "")} <span>↗</span></a></div>')
    a('</div></div></div></section>')

    # 4. корпоративные фильмы
    a('<section class="sec" id="films"><div class="wrap">'
      f'<p class="eyebrow">{TRI}<b>03</b> Корпоративные и имиджевые фильмы</p><h2>Четыре фильма, ближе всего к вашему.</h2>')
    for i, f in enumerate(FILMS):
        stats = ''.join(f'<div><b>{n}</b><span>{t}</span></div>' for n, t in f['stats'])
        quote = f'<blockquote>«{f["quote"][0]}»<cite>{f["quote"][1]}</cite></blockquote>' if f.get('quote') else ''
        a(f'<article class="film{" rev" if i % 2 else ""}" id="f-{f["id"]}" style="--c:{f["color"]}">'
          f'<div class="film-v">{part_html(f)}<p class="accent">{f["accent"]}</p></div>'
          f'<div class="film-t"><p class="tag">{f["tag"]}</p><h3>{f["title"]}</h3><p>{f["text"]}</p>'
          f'<div class="stats n{len(f["stats"])}">{stats}</div>{quote}'
          f'<a class="case-link" href="{full(f["link"])}" target="_blank" rel="noopener">Страница кейса <span>↗</span></a></div></article>')
    a('</div></section>')

    # 4б. люди в кадре
    faces = ''.join(f'<img src="/images/sgcx/p{i:02d}@280.jpg" alt="" loading="lazy" width="280" height="374">' for i in range(1, 49))
    a('<section class="sec faces" id="people"><div class="wrap faces-in">'
      f'<div class="faces-t"><p class="eyebrow light">{TRI}<b>04</b> Люди в кадре</p>'
      '<h2>48 сотрудников по имени, на своих местах.</h2>'
      '<p>Так мы снимали Saint-Gobain: не массовка в коридоре, а кладовщик, водитель, технолог и менеджер, каждый подписан в кадре. Юбилейный фильм АЛИДИ тоже про людей: тысячи сотрудников в трёх странах, и зритель должен узнать в фильме своих коллег.</p>'
      '<a class="m-link" href="https://hand-marketing.ru/video/saintgobain/cx" target="_blank" rel="noopener">стена лиц на странице кейса <span>↗</span></a></div>'
      f'<div class="wall" aria-hidden="true">{faces}</div></div></section>')

    # 5. площадки
    a('<section class="sec" id="places"><div class="wrap">'
      f'<p class="eyebrow">{TRI}<b>05</b> Презентационные фильмы</p><h2>Фильмы о площадках для инвесторов.</h2><div class="places">')
    for t, meta, txt, src, poster, link in PLACES:
        a(f'<article class="place">{vid(src, poster, t)}<p class="meta">{meta}</p><h3>{t}</h3><p>{txt}</p>'
          f'<a class="case-link" href="{full(link)}" target="_blank" rel="noopener">Страница кейса <span>↗</span></a></article>')
    a('</div></div></section>')

    # 6. серии
    a('<section class="sec tint" id="series"><div class="wrap">'
      f'<p class="eyebrow">{TRI}<b>06</b> Серии</p><h2>Серии в едином языке: от десятка роликов до курса.</h2><div class="series">')
    for n, u, t, txt, link, cover in SERIES:
        a(f'<a class="ser" href="{full(link)}" target="_blank" rel="noopener"><img src="{cover}" alt="" loading="lazy" width="476" height="396">'
          f'<p class="ser-n"><b>{n}</b> {u}</p><h3>{t}</h3><p>{txt}</p><span class="arr">↗</span></a>')
    a('</div></div></section>')

    # 7. что умеем
    a('<section class="sec" id="skills"><div class="wrap">'
      f'<p class="eyebrow">{TRI}<b>07</b> Что мы умеем</p><h2>Всё, что нужно юбилейному фильму, в одних руках.</h2>'
      '<p class="sub">Своя съёмочная группа и техника. Идею, сценарий, съёмки, графику, озвучку и монтаж делает одна команда. У каждого пункта есть кейс, где это видно.</p><div class="skills">')
    for i, (t, txt, proof, link) in enumerate(SKILLS):
        a(f'<div class="sk"><span class="sk-n">{i+1:02d}</span><h3>{t}</h3><p>{txt}</p>'
          f'<a href="{full(link)}" target="_blank" rel="noopener">где видно: {e(proof)} <span>↗</span></a></div>')
    a('</div></div></section>')

    # 7б. отзывы
    a('<section class="sec dark" id="reviews"><div class="wrap">'
      f'<p class="eyebrow light">{TRI}<b>08</b> Отзывы</p><h2>Что пишут клиенты в благодарственных письмах.</h2><div class="revs">')
    for i, r in enumerate(REVIEWS):
        meta = ', '.join(x for x in (r['role'], r.get('year')) if x)
        link = f'<a href="{full(r["case"])}" target="_blank" rel="noopener">кейс <span>↗</span></a>' if r.get('case') else ''
        a(f'<figure class="rev{" big" if i == 0 else ""}"><blockquote>«{e(r["quote"])}»</blockquote>'
          f'<figcaption><b>{e(r["company"])}</b>{e(r["person"])}, {e(meta)}{link}</figcaption></figure>')
    a('</div><p class="revs-note">Цитаты из писем без правок. Сканы писем показываем на встрече.</p></div></section>')

    # 8. все остальные
    total = sum(len(c) for _, c in CATS)
    a('<section class="sec tint" id="all"><div class="wrap">'
      f'<p class="eyebrow">{TRI}<b>09</b> Все остальные проекты</p><h2>Ролики, дизайн, полиграфия и события.</h2>'
      f'<div class="tabs" role="tablist"><button class="on" type="button" data-f="*">Все <i>{total}</i></button>')
    for cat, cards in CATS:
        k, short = CAT_SHORT[cat]
        a(f'<button type="button" data-f="{k}">{short} <i>{len(cards)}</i></button>')
    a('</div><div class="grid">')
    for cat, cards in CATS:
        k, _ = CAT_SHORT[cat]
        for c in cards:
            a(f'<a class="card" data-k="{k}" href="{c["link"]}" target="_blank" rel="noopener"><img src="{c["cover"]}" alt="" loading="lazy" width="476" height="396">'
              f'<span class="cl">{e(c["client"])}</span><h4>{e(c["name"])}</h4><p>{e(c["desc"])}</p></a>')
    a('</div></div></section>')

    # 9. дальше
    a('<section class="sec" id="next"><div class="wrap">'
      f'<p class="eyebrow">{TRI}<b>10</b> Следующие шаги</p><h2>Как двигаемся дальше.</h2><div class="steps">')
    for n, t, txt in STEPS:
        a(f'<div class="st"><b>{n}</b><h3>{t}</h3><p>{txt}</p></div>')
    a('</div><div class="par"><span class="par-l">параллельно</span><div><h3>Проверка СБ</h3>'
      '<p>С первого дня регистрируемся на tender.alidi.ru и загружаем документы для службы безопасности. Работа над фильмом при этом не ждёт.</p></div></div>')
    a('</div></section>')

    # 10. контакты
    a('<section class="final" id="contacts"><div class="wrap fin">'
      f'<div><p class="eyebrow light">{TRI}Контакты</p><h2>Готовы к встрече.</h2>'
      '<p class="lead">Назовите удобное время, покажем, как видим фильм, и ответим на вопросы по смете и площадкам.</p>'
      '<div class="hero-cta"><a class="btn" href="mailto:anarodetsky@hand-marketing.ru?subject=%D0%90%D0%9B%D0%98%D0%94%D0%98%3A%20%D0%BE%D0%BD%D0%BB%D0%B0%D0%B9%D0%BD-%D0%B2%D1%81%D1%82%D1%80%D0%B5%D1%87%D0%B0">Назначить встречу</a>'
      '<a class="btn ghost" href="https://t.me/narodetskii" target="_blank" rel="noopener">Telegram</a><a class="btn ghost pdf-btn" href="?pdf=1">Скачать PDF</a></div></div>'
      '<dl class="cont">'
      '<dt>Контактное лицо</dt><dd>Народецкий Александр · Client Service Director</dd>'
      '<dt>Телефон</dt><dd><a href="tel:+79859998783">+7 985 999 87 83</a> · <a href="tel:+74955807537">+7 495 580 75 37</a></dd>'
      '<dt>Почта</dt><dd><a href="mailto:info@hand-marketing.ru">info@hand-marketing.ru</a></dd>'
      '<dt>Офис</dt><dd>123022, Москва, ул. Рочдельская, 14А</dd>'
      '<dt>Все проекты</dt><dd><a href="https://hand-marketing.ru/project" target="_blank" rel="noopener">hand-marketing.ru/project</a></dd>'
      '<dt>Реквизиты</dt><dd>ООО «Хэнд-маркетинг» · ИНН 7709931482 · КПП 770901001 · ОГРН 1137746525608</dd>'
      '</dl></div><p class="wrap foot">Страница подготовлена для ГК АЛИДИ · доступ по личному приглашению</p></section>')

    a('<div class="modal" id="modal" hidden><button class="x" type="button" aria-label="Закрыть">×</button><div class="mv"></div></div>')
    return '\n'.join(o)


CSS = (HERE / 'page.css').read_text(encoding='utf8')
JS = (HERE / 'page.js').read_text(encoding='utf8')
TRACK = (HERE / 'track.js').read_text(encoding='utf8')

HEAD = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Hand Marketing для ГК АЛИДИ: имиджевый фильм к 35-летию</title>
<meta name="description" content="Корпоративные и имиджевые фильмы, съёмки на складах и производстве, работа в Казахстане и Беларуси. Кейсы со ссылками.">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/react-main.css">
<style>
''' + CSS + '''
</style>
</head>
<body>
'''

METRIKA = '''<script>
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
ym(71125393, "init", { clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true, params:{ private_page:'alidi' } });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute; left:-9999px;" alt=""></div></noscript>
'''

BODY = HEAD + page() + '\n<script>\n' + JS + '\n</script>\n'
PAGE_PHP = BODY + '<script id="hm-al-analytics">\n' + TRACK + '\n</script>\n' + METRIKA + '</body>\n</html>\n'
PAGE_PREVIEW = BODY + '</body>\n</html>\n'

GATE_HTML = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Доступ к странице · АЛИДИ × Hand Marketing</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/react-main.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Inter',system-ui,sans-serif; color:#141417; background:#141417;
    min-height:100vh; display:flex; align-items:center; justify-content:center; padding:20px; }
  .gate { background:#fff; border-radius:6px; padding:44px 36px 34px; max-width:430px; width:100%; position:relative; overflow:hidden; }
  .gate:before { content:''; position:absolute; left:0; top:0; right:0; height:6px; background:#0041EA; }
  .logos { display:flex; align-items:center; gap:16px; margin-bottom:34px; }
  .logos svg { height:20px; width:auto; color:#141417; }
  .logos img { height:34px; }
  .logos i { width:1px; height:26px; background:#d6d6dc; }
  h1 { font-family:'Montserrat',sans-serif; font-weight:800; font-size:24px; line-height:1.2; letter-spacing:-.02em; margin-bottom:10px; }
  .sub { font-size:15px; color:#6e6e78; margin-bottom:24px; }
  form { display:flex; flex-direction:column; gap:10px; }
  input { font-family:'Montserrat',sans-serif; font-weight:600; font-size:17px; letter-spacing:.08em; text-align:center; text-transform:uppercase;
    padding:15px; border:1.5px solid #e1e1e6; border-radius:4px; outline:none; background:#f5f5f2; }
  input:focus { border-color:#0041EA; background:#fff; }
  button { font-family:'Montserrat',sans-serif; font-weight:700; font-size:15px; color:#fff; background:#0041EA; border:0;
    border-radius:4px; padding:16px; cursor:pointer; }
  button:hover { background:#0034bb; }
  .gate-error { color:#d92d2d; font-size:13px; margin-top:4px; text-align:center; }
  .note { margin-top:24px; font-size:12px; color:#8a8a93; text-align:center; }
</style>
</head>
<body>
  <div class="gate">
    <div class="logos">''' + alidi_svg + '''<i></i><img src="hm-logo.svg" alt="Hand Marketing"></div>
    <h1>Имиджевый фильм<br>к 35-летию АЛИДИ</h1>
    <p class="sub">Введите код доступа из письма</p>
    <form method="post" action="./" autocomplete="off">
      <input type="text" name="code" placeholder="код доступа" maxlength="30" autocapitalize="characters" spellcheck="false" autofocus required>
      <button type="submit">Открыть страницу</button>
      {$errHtml}
    </form>
    <p class="note">Hand Marketing · доступ по личному приглашению</p>
  </div>
</body>
</html>
'''

PHP_HEAD = r'''<?php
// Персональная страница для ГК АЛИДИ: имиджевый фильм к 35-летию. Доступ по коду.
// Собирается scripts/alidi-page/build.py, руками не править.
// В файле только SHA-256 хеш кода. Аналитика визитов: _analytics.php, отчёт по ?stats=<ключ>.
define('HM_ALIDI', 1);
date_default_timezone_set('Europe/Moscow');
require __DIR__ . '/_analytics.php';

$ACCESS_HASH = '__HASH__';
$COOKIE_NAME = 'hm_al_access';

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: private, no-store');

hm_vid();
if (isset($_GET['stats'])) { hm_stats_page($_GET['stats']); }

$authed = isset($_COOKIE[$COOKIE_NAME]) && hash_equals($ACCESS_HASH, $_COOKIE[$COOKIE_NAME]);

// Приём событий со страницы: только от вошедших
if (isset($_GET['track'])) {
    if (!$authed) { http_response_code(403); exit; }
    hm_track();
    exit;
}

$error = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = isset($_POST['code']) ? $_POST['code'] : '';
    $code = strtoupper(preg_replace('/\s+/', '', $input));
    if ($code !== '' && hash_equals($ACCESS_HASH, hash('sha256', $code))) {
        setcookie($COOKIE_NAME, $ACCESS_HASH, time() + 60 * 60 * 24 * 30, '/for/alidi/', '', hm_https(), true);
        $g = hm_geo(hm_ip());
        hm_event('login_ok', array('geo' => $g));
        hm_tg("🔓 <b>АЛИДИ открыли страницу</b>\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where($g) . "\n" . date('d.m H:i'));
        header('Location: ./');
        exit;
    }
    // введённый текст не сохраняем: это может оказаться чужой пароль
    hm_event('login_fail', array('len' => function_exists('mb_strlen') ? mb_strlen($input) : strlen($input)));
    $error = true;
}

if (!$authed) {
    if ($_SERVER['REQUEST_METHOD'] === 'GET') hm_event('gate_view');
    $errHtml = $error ? '<p class="gate-error">Код не подошёл. Попробуйте ещё раз.</p>' : '';
    echo <<<GATE
__GATE__
GATE;
    exit;
}
// PDF-портфолио только после входа: файл лежит рядом, прямой доступ закрыт в .htaccess
if (isset($_GET['pdf'])) {
    $f = __DIR__ . '/alidi-portfolio.pdf';
    if (!is_file($f)) { http_response_code(404); exit; }
    hm_event('pdf_download');
    hm_tg("📄 <b>АЛИДИ скачали PDF</b>\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where(hm_geo(hm_ip())) . "\n" . date('d.m H:i'));
    header('Content-Type: application/pdf');
    header('Content-Disposition: attachment; filename="Hand_Marketing_ALIDI_portfolio.pdf"');
    header('Content-Length: ' . filesize($f));
    readfile($f);
    exit;
}
hm_event('page_view');
?>
'''

assert '$' not in GATE_HTML.replace('{$errHtml}', ''), 'в экране пароля не должно быть $ кроме {$errHtml}'
php = PHP_HEAD.replace('__HASH__', ACCESS_HASH).replace('__GATE__', GATE_HTML.rstrip('\n')) + PAGE_PHP
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.php').write_text(php, encoding='utf8')
(OUT / '_preview-page.html').write_text(PAGE_PREVIEW, encoding='utf8')
(OUT / '_preview-gate.html').write_text(GATE_HTML.replace('{$errHtml}', ''), encoding='utf8')
print('ok', len(php), 'байт;', sum(len(c) for _, c in CATS), 'карточек в «Все остальные»')
