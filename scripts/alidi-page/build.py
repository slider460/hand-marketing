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
         video='/media/transrzhd.mp4', poster='/images/rgd-history/poster.jpg', link='/video/rgd/history/'),
    dict(id='isotec', color='#9b2a8a', tag='Имиджевый фильм · Saint-Gobain · ISOTEC · 2024',
         title='«Изотек»: двенадцать лет бренда в одной истории',
         accent='От образования направления до криогенной изоляции.',
         text='Ролик показывает «Изотек» как живой бренд с историей, а не как поставщика материалов. Работает в двух контурах: для клиентов, партнёров и отраслевых событий и для внутренних коммуникаций и адаптации сотрудников. Структура: пролог, хронология, география, производство, цифровые сервисы, итоги. Съёмки на действующих производственных площадках по регламентам СИЗ.',
         stats=[('4:33', 'хронометраж фильма'), ('9 вех', '2012-2024, каждая вынесена в экранную графику'), ('6', 'площадок с реальными кадрами производства')],
         video='/media/izotek-brand-video.mp4', poster='/images/isotec/poster.jpg', link='/isotec/'),
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
     '/media/technopark-zubovo.mp4', '/images/zubovo/poster.jpg', '/zubovo/'),
    ('Технопарк «Бекабад»', 'Узбекистан · 2:34', 'Площадка в Ташкентской области, которую Башкортостан строит вместе с Узбекистаном. Мастер-план поднимается поверх аэросъёмки реального участка.',
     '/media/bekabad-hd.mp4', '/images/bekabad/poster.jpg', '/bekobod1/'),
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
    ('Две концепции и сценарий', 'Предлагаем два хода на выбор и доводим выбранный до покадрового сценария.', 'Газель-трансформер', '/video/gaz/'),
    ('Съёмка на складе и в цеху', 'Работаем на действующих площадках по регламентам СИЗ, не останавливая смену.', '«Изотек»', '/isotec/'),
    ('Несколько групп одновременно', 'Параллельные выезды в разные города с одним режиссёрским планом.', 'ЦМ РЖД', '/video/rgd/history/'),
    ('Аэросъёмка', 'Территория, терминалы и подъездные пути сверху, с квадрокоптера.', 'Технопарк «Зубово»', '/zubovo/'),
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


VERSION = '9 октября 2026'
PDF_FILE = '2026-10-09'  # дата в имени скачиваемого PDF

# Новые блоки страницы: функции, которые возвращают HTML секции. Добавляем по одному.
def blk_heard():
    """Письмо после встречи 7 октября + протокол договорённостей. Тон: от человека, их словами."""
    rows = [
        ('Драфт-бюджет: три версии, русский язык, все площадки', 'Hand Marketing', '20 октября', True),
        ('Таблица фактов и цифр для заполнения', 'Hand Marketing', 'вместе с бюджетом', False),
        ('Примеры: как снимаем руководителей и сотрудников, и кино для сравнения', 'Hand Marketing', 'готово', 'done'),
        ('Петербург в брифе', 'АЛИДИ', 'готово', 'done'),
        ('Список логотипов, которые можно показывать', 'АЛИДИ', 'до съёмок', False),
        ('Брендбук и гайды', 'АЛИДИ', 'до сценария', False),
        ('Даты съёмок по загрузке складов', 'вместе', 'после выбора идеи', False),
    ]
    def cls(h):
        return 'done' if h == 'done' else ('hot' if h else '')
    def note(w, h):
        if h != 'done':
            return e(w)
        link = ' <a href="#how">на этой странице ↓</a>' if w.startswith('Примеры') else ' <a href="#geo2">на этой странице ↓</a>'
        return e(w) + link
    tr = ''.join(f'<tr class="{cls(hot)}"><td>{note(w, hot)}</td><td>{e(who)}</td><td class="dt">{"✓ " if hot == "done" else ""}{e(when)}</td></tr>' for w, who, when, hot in rows)
    return (
        '<section class="memo" id="top"><div class="wrap memo-in">'
        '<aside class="memo-side"><p class="mono">9.10.2026</p><p class="mono dim">после встречи 7 октября</p>'
        f'<a class="pdf-dl pdf-btn" href="?pdf=1">Скачать PDF<span class="mono">версия от {VERSION}</span></a>'
        f'<div class="memo-to">{alidi_svg}<span>ГК АЛИДИ<br>имиджевый фильм к 35-летию</span></div></aside>'
        '<div class="memo-body">'
        '<h1>Спасибо за разговор.</h1>'
        '<p>Записали главное, чтобы не держать в голове.</p>'
        '<p>Сейчас вам нужен не сценарий, а понятная сумма: заложить её в бюджет на 2027 год и сравнить подрядчиков на одинаковом объёме. '
        'Поэтому до 20 октября пришлём драфт-бюджет на три версии фильма: к 35-летию, партнёрскую и для HH.ru. Русский язык, съёмки на всех площадках, озвучка, графика, музыка. '
        'Если по дороге понадобится что-то сверх этого, например переводы, посчитаем отдельно и скажем заранее.</p>'
        '<blockquote>«Питер… это в целом красивая картинка, которую можно показать»<cite>из разговора 7 октября</cite></blockquote>'
        '<p>Петербург добавляем, для партнёрской версии он сильный. Казань посчитаем отдельной строкой, решите, когда увидите цифры.</p>'
        '<p>Форма, порядок в кадре и логотипы на вашей стороне, мы подстроимся под дни с меньшей нагрузкой. '
        'Без киношного грима, договорились. Как мы снимаем руководителей и сотрудников в обычной рабочей обстановке, покажем на примерах.</p>'
        '<p class="sign">Александр Народецкий<br><span>Hand Marketing</span></p>'
        '</div></div>'
        '<div class="wrap"><div class="proto"><div class="proto-h"><h2>Договорились</h2><p class="mono dim">обновляем здесь по мере движения</p></div>'
        f'<table><thead><tr><th>Что</th><th>Кто</th><th>Когда</th></tr></thead><tbody>{tr}</tbody></table></div></div></section>')


GEO2 = [  # с запада на восток: город, тип, подпись
    ('Калининград', 'stock', 'стоки и архив'),
    ('Минск', 'shoot', 'склад и офис'),
    ('Санкт-Петербург', 'new', 'добавили 7 октября'),
    ('Москва', 'shoot', 'офис и Валищево'),
    ('Нижний Новгород', 'flag', 'отсюда с 1992 года'),
    ('Казань', 'option', 'отдельной строкой'),
    ('Алматы', 'shoot', 'склад и офис'),
]


def geo2_svg(vertical=False):
    """Схема-линия с запада на восток. Перед Алматы разрыв: ~3 000 км."""
    n = len(GEO2)
    if not vertical:
        W, H, y = 820, 190, 95
        xs = [40 + i * 112 for i in range(n - 1)] + [780]
        o = [f'<svg class="geo2 hz" viewBox="0 0 {W} {H}" role="img" aria-label="Съёмки с запада на восток">']
        o.append(f'<line class="ln" x1="{xs[0]}" y1="{y}" x2="{xs[-2] + 40}" y2="{y}"/>')
        o.append(f'<path class="ln br" d="M{xs[-2] + 40},{y} l10,-10 l12,20 l12,-20 l12,20 l10,-10"/>')
        o.append(f'<line class="ln" x1="{xs[-2] + 96}" y1="{y}" x2="{xs[-1]}" y2="{y}"/>')
        o.append(f'<text class="km" x="{xs[-2] + 74}" y="{y - 24}" text-anchor="middle">≈3 000 км</text>')
        for i, ((name, t, sub), x) in enumerate(zip(GEO2, xs)):
            up = i % 2 == 0
            ty = y - 38 if up else y + 40
            r = 11 if t == 'flag' else 9
            o.append(f'<g class="g2 g2-{t}"><circle cx="{x}" cy="{y}" r="{r + 8}" class="hl"/><path d="M{x - r},{y + r * .7} L{x},{y - r} L{x + r},{y + r * .7}z"/>'
                     f'<text x="{x}" y="{ty}" text-anchor="middle"><tspan class="nm">{e(name)}</tspan><tspan class="sb" x="{x}" dy="16">{e(sub)}</tspan></text></g>')
    else:
        W, H, x = 320, 470, 40
        ys = [30 + i * 62 for i in range(n - 1)] + [450]
        o = [f'<svg class="geo2 vt" viewBox="0 0 {W} {H}" role="img" aria-label="Съёмки с запада на восток">']
        o.append(f'<line class="ln" x1="{x}" y1="{ys[0]}" x2="{x}" y2="{ys[-2] + 24}"/>')
        o.append(f'<path class="ln br" d="M{x},{ys[-2] + 24} l-9,8 l18,10 l-18,10 l9,8"/>')
        o.append(f'<line class="ln" x1="{x}" y1="{ys[-2] + 60}" x2="{x}" y2="{ys[-1]}"/>')
        o.append(f'<text class="km" x="{x + 24}" y="{ys[-2] + 46}">≈3 000 км</text>')
        for (name, t, sub), yy in zip(GEO2, ys):
            r = 11 if t == 'flag' else 9
            o.append(f'<g class="g2 g2-{t}"><circle cx="{x}" cy="{yy}" r="{r + 8}" class="hl"/><path d="M{x - r},{yy + r * .7} L{x},{yy - r} L{x + r},{yy + r * .7}z"/>'
                     f'<text x="{x + 26}" y="{yy - 2}"><tspan class="nm">{e(name)}</tspan><tspan class="sb" x="{x + 26}" dy="16">{e(sub)}</tspan></text></g>')
    o.append('</svg>')
    return ''.join(o)


def blk_geo():
    """География: схема-линия с подписями, заголовок их словами."""
    return ('<section class="route" id="geo2"><div class="wrap">'
            '<div class="route-h"><h2>От Калининграда<br>до Алматы.</h2>'
            '<p>Снимаем шесть городов, остальные филиалы показываем на карте стоками и архивом. '
            'Москва без командировок, в смете отдельно Петербург, Нижний, Минск, Алматы и, по желанию, Казань.</p></div>'
            '<div class="route-map">' + geo2_svg() + geo2_svg(True) + '</div></div></section>')


def blk_ideas():
    """Идеи фильма коротко: одна фраза и финал. Плюс три версии под площадки."""
    ideas = [
        ('Сутки без остановки', 'Один рабочий день компании: начинается в 05:52 в Алматы, заканчивается ночной сменой. Солнце идёт с востока на запад вместе с фильмом, у каждого города свой час, между городами переходим через ворота склада. Время в титре всегда настоящее.', '«Обычный день АЛИДИ. 12 783-й подряд.»'),
        ('Год приёма', 'Историю рассказывают сотрудники, каждый называет год, когда пришёл. Люди выстроены по годам от самых первых до пришедших в 2027-м, и через их места работы видно, как росла компания. Без хроники и диктора.', 'Финал: самый опытный и самый новый встают рядом, за ними все герои.'),
        ('Невидимый партнёр', 'От полки в магазине назад по цепочке: склад, заказ, приёмка. Фильм начинается с обычного утра покупателя и показывает, сколько людей и решений стоит за одним товаром. Сроки «за 2 часа», «за 9 часов» берём настоящие.', '«Ни на одной полке нет нашего логотипа. На каждой есть наша работа.»'),
        ('Одна минута', 'Одно и то же движение в пяти городах: стандарт один везде. Коробку берут в Алматы, сканируют в Минске, ставят на паллет в Нижнем, а склейка получается только потому, что процессы действительно одинаковые.', '«Пять городов. Одна компания.»'),
        ('Та же точка, 35 лет спустя', 'Архивное фото в руке на фоне того же места сегодня. Так проходим вехи от первого здания в Нижнем Новгороде до сегодняшних площадок в трёх странах, рассказывает голос человека, который всё это видел.', '«Тогда хватало одного кадра. Сегодня нужны три страны.»'),
    ]
    vers = [('К 35-летию', '4–5 минут', 'большой экран, со звуком'),
            ('Партнёрская', '2:30–3:00', 'переговоры и тендеры по контрактам'),
            ('Для HH.ru', '60–90 секунд', 'телефон, вертикаль, без звука')]
    o = ('<section class="ideas" id="ideas"><div class="wrap"><div class="ideas-h"><h2>Пять идей.</h2>'
         '<p>Выбираем две, обе доводим до сценария. Из одних съёмок собираем три версии.</p></div><ol class="ideas-l">')
    for i, (n, x, fin) in enumerate(ideas):
        o += f'<li><span class="mono dim">0{i + 1}</span><div><h3>{e(n)}</h3><p>{e(x)}</p></div><p class="ifin">{e(fin).replace("12 783", "12&nbsp;783")}</p></li>'
    o += '</ol><div class="vers">' + ''.join(
        f'<div><b>{e(a)}</b><span class="mono">{e(b)}</span><p>{e(c)}</p></div>' for a, b, c in vers) + '</div></div></section>'
    return o


def blk_how():
    """Примеры уровня съёмки: руководители, сотрудники и путь клиента, кино для сравнения."""
    tops = [  # таймкод во второй части фильма SG, портрет, имя, должность (только снятые нами в Москве)
        (7.2, 2, 'Маргарита Молодых', 'директор бизнес-подразделения'), (19.2, 3, 'Рафаэль Зохрабян', 'генеральный директор'),
        (28.8, 4, 'Артём Гаврилюк', 'директор по продажам'), (36.0, 5, 'Елена Сильвестрова', 'директор по персоналу'),
        (45.6, 6, 'Андрей Зарипов', 'индустриальный директор'), (55.2, 7, 'Ирина Кочкина', 'директор по закупкам'),
        (64.8, 8, 'Марина Ченцова', 'директор по логистике'), (74.4, 9, 'Елена Радченко', 'финансовый директор'),
        (108.0, 12, 'Тимур Сагиров', 'директор по IT'), (122.4, 13, 'Юлия Ночёвина', 'директор по маркетингу'),
    ]
    path = [(37.2, 'sc-road', 'реклама и выбор'), (142.4, 'sc-gyproc-yard', 'завод'), (196.2, 'sc-isover-belt', 'линия'),
            (221.4, 'sc-pallets', 'склад и отгрузка'), (232.0, 'sc-mounting', 'монтаж'), (409.5, 'sc-clients-final', 'финал')]
    cine = [('https://hand-marketing.ru/media/vivax-samburskaya.mp4', '/images/vivax/rest-smile.jpg', 'VIVAX SPORT', 'реклама с Настасьей Самбурской, 49 с', '/video/vivax/'),
            ('https://hand-marketing.ru/media/gazelle-transformer.mp4', '/images/gaz/poster.jpg', 'Газель-трансформер', 'вирусный ролик для Eaton, 1:42', '/video/gaz/'),
            ('https://hand-marketing.ru/media/eaton-yaz.mp4', '/images/patriot/poster.jpg', 'УАЗ Патриот', 'рекламный ролик для Eaton, 60 с', '/video/patriot/')]
    o = ('<section class="how" id="how"><div class="wrap"><div class="ideas-h"><h2>Как снимаем.</h2>'
         '<p>Шесть примеров: на что смотреть и к какой версии вашего фильма это относится.</p></div>')
    # 1. руководители
    chips = ''.join(f'<button type="button" class="tp" data-p="v-tops" data-t="{t}"><img src="/images/sgcx/sp-{i:02d}@280.jpg" alt="" loading="lazy">'
                    f'<b>{e(n)}</b><span>{e(r)}</span></button>' for t, i, n, r in tops)
    o += ('<div class="ex"><div class="ex-t"><p class="mono dim">01 · руководители</p><h3>Интервью топ-менеджеров</h3>'
          '<p>Saint-Gobain, фильм «Клиентский опыт». Руководителей снимали на трёх площадках: две локации в Москве и завод. Снимали между их встречами, свет и звук наши, профессионального грима нет.</p>'
          '<p class="ex-for">В вашем фильме: Иван Сычёв и руководители направлений, во всех трёх версиях.</p>'
          '<p class="ex-note">Руководителей из Казахстана и Беларуси в этом фильме мы не снимали: компания прислала их записи отдельно, поэтому в пример их не берём.</p><a class="ex-link" href="https://hand-marketing.ru/video/saintgobain/cx/" target="_blank" rel="noopener">страница кейса ↗</a></div>'
          '<div class="ex-v"><video id="v-tops" controls preload="none" playsinline poster="img/sg-tops.jpg" src="https://hand-marketing.ru/media/sg-cx-part2.mp4#t=7"></video>'
          f'<p class="mono dim tp-h">выберите, с кого начать</p><div class="tps">{chips}</div></div></div>')
    # 2. путь клиента и сотрудники
    pch = ''.join(f'<button type="button" class="pc" data-p="v-path" data-t="{t}"><img src="/images/sgcx/{f}@560.jpg" alt="" loading="lazy"><span>{e(c)}</span></button>'
                  for t, f, c in path)
    o += ('<div class="ex"><div class="ex-t"><p class="mono dim">02 · сотрудники</p><h3>Путь клиента через всю компанию</h3>'
          '<p>Тот же фильм, первая часть: один заказ проходит от рекламы до готового дома. В кадре 48 сотрудников на своих местах, каждый подписан по имени. Офис в Москве и два завода в Егорьевске.</p>'
          '<p class="ex-for">В вашем фильме: склады, офисы и люди в «Сутках», «Годе приёма», HR-версии.</p><a class="ex-link" href="https://hand-marketing.ru/video/saintgobain/cx/" target="_blank" rel="noopener">страница кейса ↗</a></div>'
          '<div class="ex-v"><video id="v-path" controls preload="none" playsinline poster="/images/sgcx/hero-poster.jpg" src="https://hand-marketing.ru/media/sg-cx-part1.mp4"></video>'
          f'<div class="pcs">{pch}</div></div></div>')
    # 3. масштаб: много площадок в одном фильме
    pt = [(37.0, 'poster-short', 'Лужники'), (66.0, 'obj-match', 'матч'), (78.0, 'nums-a', 'цифры'),
          (112.0, 'shoot-fence', 'обход площадки'), (165.0, 'shoot-cables', 'кабельные трассы'), (225.0, 'shoot-gen', 'генератор и кран')]
    pch2 = ''.join(f'<button type="button" class="pc" data-p="v-pt" data-t="{t}"><img src="/images/powertech/{f}.jpg" alt="" loading="lazy"><span>{e(c)}</span></button>'
                   for t, f, c in pt)
    o += ('<div class="ex"><div class="ex-t"><p class="mono dim">03 · масштаб</p><h3>Вся компания и много площадок в одном фильме</h3>'
          '<p>Power Technologies на чемпионате мира 2018: 11 городов, 12 стадионов, месяц съёмок мобильными группами. Объекты, работа смен, руководители и инфографика собраны в один рассказ о масштабе.</p>'
          '<p class="ex-for">В вашем фильме: шесть городов в трёх странах, партнёрская версия.</p><a class="ex-link" href="https://hand-marketing.ru/video/powertechnologies/" target="_blank" rel="noopener">страница кейса ↗</a></div>'
          '<div class="ex-v"><video id="v-pt" controls preload="none" playsinline poster="/images/powertech/poster-short.jpg" src="https://hand-marketing.ru/media/pt-film-short.mp4"></video>'
          f'<div class="pcs">{pch2}</div></div></div>')
    # 4. история по годам
    iso = [(20, 'tl-1', '2012'), (49, 'tl-3', '2014'), (71, 'tl-5', '2018'), (94, 'tl-7', '2022'), (101, 'tl-8', '2023'), (115, 'tl-9', '2024')]
    pch3 = ''.join(f'<button type="button" class="pc yr" data-p="v-iso" data-t="{t}"><img src="/images/isotec/{f}.jpg" alt="" loading="lazy"><span class="mono">{e(c)}</span></button>'
                   for t, f, c in iso)
    o += ('<div class="ex"><div class="ex-t"><p class="mono dim">04 · история</p><h3>Годы компании в одном ролике</h3>'
          '<p>Бренд-фильм «Изотек»: двенадцать лет направления, девять вех от 2012 до 2024, каждая вынесена в графику поверх живых кадров производства. Дальше география и итоги в цифрах.</p>'
          '<p class="ex-for">В вашем фильме: 35 лет от 1992 года, идеи «Та же точка» и «Год приёма».</p><a class="ex-link" href="https://hand-marketing.ru/isotec/" target="_blank" rel="noopener">страница кейса ↗</a></div>'
          '<div class="ex-v"><video id="v-iso" controls preload="none" playsinline poster="/images/isotec/poster.jpg" src="https://hand-marketing.ru/media/izotek-brand-video.mp4"></video>'
          f'<div class="pcs">{pch3}</div></div></div>')
    # 5. смесь: история, объект, интервью
    mm = [(14.5, 'ren-2', 'объект'), (27.0, 'hist-1', 'история'), (38.0, 'was', 'было и будет'),
          (84.0, 'ex-1', 'эксперт'), (118.5, 'num-2', 'цифры'), (262.0, 'ex-2', 'арендаторы')]
    pch4 = ''.join(f'<button type="button" class="pc" data-p="v-mmg" data-t="{t}"><img src="/images/mmg/{f}.jpg" alt="" loading="lazy"><span>{e(c)}</span></button>'
                   for t, f, c in mm)
    o += ('<div class="ex"><div class="ex-t"><p class="mono dim">05 · всё вместе</p><h3>История, объект и интервью в одном фильме</h3>'
          '<p>ТРЦ «Павелецкая Плаза» для MMG, 5:37. Архив Павелецкой площади и та же площадь в проекте, рендеры комплекса, карта зоны охвата и цифры, '
          'интервью экспертов и арендаторов: «Эконика», «Теремок».</p>'
          '<p class="ex-for">В вашем фильме: история с 1992 года, площадки сегодня и голоса руководителей вместе, партнёрская версия и версия к 35-летию.</p><a class="ex-link" href="https://hand-marketing.ru/mmg/" target="_blank" rel="noopener">страница кейса ↗</a></div>'
          '<div class="ex-v"><video id="v-mmg" controls preload="none" playsinline poster="/images/mmg/poster.jpg" src="https://hand-marketing.ru/media/mmg-paveleckayaplaza.mp4"></video>'
          f'<div class="pcs">{pch4}</div></div></div>')
    # 6. кино для сравнения
    o += ('<div class="ex ex-cine"><div class="ex-t"><p class="mono dim">06 · для сравнения</p><h3>Кинематографичный уровень</h3>'
          '<p>Грим, постановочный свет, актёры, раскадровка каждого плана. Для корпоративного фильма в таком объёме это не нужно, показываем, чтобы было с чем сравнить уровни в бюджете.</p></div>'
          '<div class="cines">' + ''.join(
              f'<div class="cn"><div class="vid0"><video controls preload="none" playsinline poster="{pp}" src="{v}"></video></div><b>{e(t)}</b><span>{e(c)}</span>'
              f'<a class="ex-link" href="https://hand-marketing.ru{lk}" target="_blank" rel="noopener">страница кейса ↗</a></div>'
              for v, pp, t, c, lk in cine) + '</div></div>')
    return o + '</div></section>'


def blk_maps():
    """Как мы показываем карту присутствия: четыре немые петли из наших роликов."""
    maps = [('map-rzd', 'ЦМ РЖД', 'Сеть терминалов прорастает с запада на восток, от Калининграда до Находки.', '/video/rgd/history/'),
            ('map-iso', '«Изотек»', 'Города присутствия по одному загораются на карте России.', '/isotec/'),
            ('map-zub', 'Технопарк «Зубово»', 'Регион на карте страны, затем подъезды к площадке: аэропорт, станция, трасса.', '/zubovo/'),
            ('map-bek', 'Технопарк «Бекабад»', 'Страна на карте мира и торговые коридоры во все стороны.', '/bekobod1/'),
            ('map-silk', 'Silk Way Rally · 3D', 'Глобус приближается к городу старта, этап поднимается рельефом по координатам маршрута.', '/video/silkway/')]
    o = ('<section class="maps" id="maps"><div class="wrap"><div class="ideas-h"><h2>Карта в фильме.</h2>'
         '<p>Так мы уже показывали масштаб в роликах: плоско, на глобусе и в 3D.</p></div><div class="mp-grid">')
    for f, t, x, link in maps:
        o += (f'<figure class="mp"><video class="mp-v" muted loop playsinline preload="none" poster="img/{f}.jpg" data-src="img/{f}.mp4" aria-hidden="true"></video>'
              f'<figcaption><b>{e(t)}</b><span>{e(x)}</span><a href="{full(link)}" target="_blank" rel="noopener">страница кейса ↗</a></figcaption></figure>')
    o += ('<div class="mp-for"><p class="mono dim">для АЛИДИ</p><h3>Россия, Беларусь и Казахстан на одной карте</h3>'
          '<p>Точки всплывают от Калининграда до Алматы, на каждую короткий кадр с площадки. Шесть городов снимаем, остальные филиалы даём стоками и архивом. '
          'Стиль карты подбираем под ваш брендбук.</p></div>')
    return o + '</div></div></section>'


def blk_sb():
    """Проверка службой безопасности: статус регистрации на tender.alidi.ru."""
    st = [('Регистрация на tender.alidi.ru', 'готово', True), ('Учредительные документы', 'загружены', True),
          ('Бухгалтерские документы', 'в работе', False)]
    return ('<section class="sb" id="sb"><div class="wrap"><div class="sb-in"><div><p class="mono dim">проверка службой безопасности</p>'
            '<h3>Документы на tender.alidi.ru</h3></div><ul>'
            + ''.join(f'<li class="{"ok" if ok else "wip"}"><span>{e(a)}</span><b class="mono">{"✓ " if ok else ""}{e(b)}</b></li>' for a, b, ok in st)
            + '</ul></div></div></section>')


def blk_more():
    """Чем ещё можем помочь к 35-летию: компактно, без навязывания."""
    L = '/images/lib/'
    cols = [
        ('Выставочные стенды', 'Строим под ключ, но главное в другом: нестандартную мультимедиа и контент закладываем ещё на этапе проекта, а не добавляем на монтаже.',
         [('Самара на ВДНХ', '/portfolio/samara-stand-vdnh/', L + 'custom-samara-vdnh/cover-main.png', False),
          ('Ставрополье на ВДНХ', '/portfolio/stavropol-stand-vdnh/', L + 'custom-stavropol-vdnh/cover-main.png', False),
          ('Как разрабатываем: проект стенда Самары, 204 м², 79 листов', '/exhibition/dizayn-stenda/', '/images/exhibition/samara/render-v1-a.jpg', True)]),
        ('События', 'Наше основное направление с открытия агентства. Одна идея проходит через всё мероприятие: приглашение, площадку, сцену, экраны и подарки.',
         [('«Внутри стихии», ТРЦ Ривьера', '/event/riviera/', L + 'as3062-3363-4134-b333-623232303134/__-22.png', False),
          ('Новый год Samsung', '/event/samsung/', L + 'as3466-3261-4738-b938-303637303133/__-18.png', False)]),
        ('Контент и медианосители', 'Контент для мероприятий и выставок под конкретную площадку: проекции на здание и автомобиль, изогнутые и кинетические экраны, интерактив, песочные столы.',
         [('3D mapping на здании, Ставрополь', '/3d/stavropol/', L + 'as6466-3635-4534-b432-353364376364/__-01.png', False),
          ('Mapping на кузове Changan CS35', '/event/changan/', L + 'as3635-3436-4663-b265-633363383261/__-98.png', False),
          ('Интерактив с Kinect, музей Алабина', '/portfolio/samara-exhibition/', L + 'custom-samara-exhibition/cover-main.png', False),
          ('3D-маршрут и песочный стол, Silk Way', '/video/silkway/', L + 'as6164-6432-4132-a361-613136626438/__-51.png', False)]),
        ('Дизайн', 'Своя креативная студия: айдентика, полиграфия, упаковка и сувенирная продукция.',
         [('Брендбук Metra', '/creative/metra/', L + 'custom-metra/cover-main.png', False),
          ('Чемодан Saint-Gobain', '/creative/saintgobain/suitcase/', L + 'as3734-3562-4636-a636-633764353537/__-41.png', False),
          ('Стиль отдела продаж Becar', '/creative/becar/sdep/', L + 'as6366-6163-4338-b039-373730386163/__-74.png', False),
          ('Брошюра Vertical, 24 полосы', '/creative/becar/vertical/', L + 'as6633-6662-4561-b364-303861353166/__-64.png', False),
          ('Календарь Saint-Gobain: креативная концепция', '/creative/saintgobain/calendar/', L + 'custom-sgcalendar/cover-main.png', False),
          ('Новогодний набор ЦМ РЖД', '/creative/rgd/suvenir/', L + 'as3634-3861-4239-b237-356636663535/__-60.png', False)]),
    ]
    o = ('<section class="more" id="more"><div class="wrap"><div class="more-h"><h2>Готовы участвовать и в других проектах.</h2>'
         '<p>Не только фильм. То, что мы делаем давно и хорошо.</p></div><div class="more-g">')
    for t, x, cases in cols:
        o += f'<div class="mc"><h3>{e(t)}</h3><p>{e(x)}</p><ul>'
        for n, u, img, photo in cases:
            o += (f'<li><a href="https://hand-marketing.ru{u}" target="_blank" rel="noopener">'
                  f'<img class="{"ph" if photo else ""}" src="{img}" alt="" loading="lazy"><span>{e(n)}</span><i>↗</i></a></li>')
        o += '</ul></div>'
    return o + '</div></div></section>'


NEW_BLOCKS = [blk_heard, blk_sb, blk_geo, blk_maps, blk_ideas, blk_how, blk_more]



# ---------- HTML ----------
def page():
    o = []
    a = o.append
    a('<header class="top"><div class="wrap top-in">'
      f'<a class="brand" href="#top" aria-label="В начало">{alidi_svg}<i></i><img src="hm-logo.svg" alt="Hand Marketing" width="34" height="34"></a>'
      '<nav class="nav"><a href="#top">Материалы</a><a href="#archive-open">Наши работы</a><a href="#contacts">Контакты</a></nav>'
      '<a class="pdf-btn" href="?pdf=1">PDF</a></div></header>')

    # 0. новая страница: блоки собираем по одному (NEW_BLOCKS)
    for blk in NEW_BLOCKS:
        a(blk())

    # архив: всё, что было на странице до встречи, открывается кнопкой
    a('<section class="arch-bar" id="archive-open"><div class="wrap arch-in">'
      '<div><p class="eyebrow">' + TRI + 'Материалы от 1 октября</p><h3>Наши работы и как мы их снимали</h3>'
      '<p>Кейсы, фильмы, отзывы и всё, что мы показывали до встречи. <a class="pdf-btn" href="?pdf=portfolio">Портфолио в PDF</a></p></div>'
      '<button class="btn ghost-d" type="button" id="arch-btn" aria-expanded="false" aria-controls="archive">Посмотреть</button>'
      '</div></section><div id="archive" hidden>')

    # 1. первый экран
    a('<section class="hero" id="hero">'
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
      '<a class="m-link" href="https://hand-marketing.ru/video/saintgobain/cx/" target="_blank" rel="noopener">стена лиц на странице кейса <span>↗</span></a></div>'
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

    a('</div>')  # конец архива

    # 10. контакты
    a('<section class="final" id="contacts"><div class="wrap fin">'
      f'<div><p class="eyebrow light">{TRI}Контакты</p><h2>На связи.</h2>'
      '<p class="lead">Пишите на почту с любыми вопросами по идеям, смете и площадкам.</p>'
      '<div class="hero-cta"><a class="btn" href="mailto:anarodetsky@hand-marketing.ru?subject=%D0%90%D0%9B%D0%98%D0%94%D0%98%3A%20%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%20%D0%BA%2035-%D0%BB%D0%B5%D1%82%D0%B8%D1%8E">Написать письмо</a>'
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
<link rel="stylesheet" href="/fonts/golos-ptserif.css">
<link rel="stylesheet" href="/fonts/plex.css">
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
// PDF только после входа: файлы лежат рядом, прямой доступ закрыт в .htaccess.
// ?pdf=1 текущая версия материалов (собирается scripts/alidi-page/pdf.mjs), ?pdf=portfolio портфолио от 30 сентября
if (isset($_GET['pdf'])) {
    $old = $_GET['pdf'] === 'portfolio';
    $f = __DIR__ . ($old ? '/alidi-portfolio.pdf' : '/alidi-materials.pdf');
    if (!is_file($f)) { http_response_code(404); exit; }
    hm_event('pdf_download', array('file' => $old ? 'portfolio' : 'materials'));
    hm_tg("📄 <b>АЛИДИ скачали PDF</b>" . ($old ? " (портфолио)" : " (материалы __PDFDATE__)") . "\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where(hm_geo(hm_ip())) . "\n" . date('d.m H:i'));
    header('Content-Type: application/pdf');
    header('Content-Disposition: attachment; filename="' . ($old ? 'Hand_Marketing_ALIDI_portfolio.pdf' : 'Hand_Marketing_ALIDI___PDFFILE__.pdf') . '"');
    header('Content-Length: ' . filesize($f));
    readfile($f);
    exit;
}
hm_event('page_view');
?>
'''

assert '$' not in GATE_HTML.replace('{$errHtml}', ''), 'в экране пароля не должно быть $ кроме {$errHtml}'
php = PHP_HEAD.replace('__PDFDATE__', VERSION).replace('__PDFFILE__', PDF_FILE).replace('__HASH__', ACCESS_HASH).replace('__GATE__', GATE_HTML.rstrip('\n')) + PAGE_PHP
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.php').write_text(php, encoding='utf8')
(OUT / '_preview-page.html').write_text(PAGE_PREVIEW, encoding='utf8')
(OUT / '_preview-gate.html').write_text(GATE_HTML.replace('{$errHtml}', ''), encoding='utf8')
print('ok', len(php), 'байт;', sum(len(c) for _, c in CATS), 'карточек в «Все остальные»')
