#!/usr/bin/env python3
"""PDF-презентация для АЛИДИ: те же материалы, что на странице /for/alidi/, но слайдами 16:9.
Каждый пример со ссылкой и QR. Собирает mirror/for/alidi/_preview-slides.html (не коммитится),
PDF печатает scripts/alidi-page/pdf.mjs.
Запуск: python3 scripts/alidi-page/slides.py && node scripts/alidi-page/pdf.mjs"""
import html
import io
import sys
from pathlib import Path

import segno

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import build  # noqa: E402  (пересобирает страницу и даёт общие куски: логотип, схему городов, VERSION)

e = html.escape
SITE = 'https://hand-marketing.ru'
PAGE = SITE + '/for/alidi/'
VERSION = build.VERSION


def qr(url, px=96, light=False):
    buf = io.BytesIO()
    segno.make(url, error='m').save(buf, kind='svg', scale=4, border=1, dark='#ffffff' if light else '#141417', light=None, xmldecl=False, svgns=True)
    svg = buf.getvalue().decode().replace('<svg ', f'<svg width="{px}" height="{px}" ', 1)
    return f'<a class="qr" href="{e(url)}">{svg}</a>'


def link(url, text=None):
    t = text or url.replace('https://', '')
    return f'<a class="lk" href="{e(url)}">{e(t)} ↗</a>'


slides = []
n = [0]


def slide(body, dark=False, cls=''):
    n[0] += 1
    slides.append(f'<section class="s {"dk" if dark else ""} {cls}"><div class="hd"><span>ГК АЛИДИ · имиджевый фильм к 35-летию</span>'
                  f'<span>{n[0]:02d}</span></div>{body}</section>')


# 1. Титул
slides.append(
    '<section class="s title"><img class="bgv" src="img/hero-loop.jpg" alt=""><div class="shade"></div>'
    f'<div class="t-logos">{build.alidi_svg}<i></i><img src="hm-logo.svg" alt="Hand Marketing"></div>'
    '<p class="t-k">ГК АЛИДИ · имиджевый фильм к 35-летию</p>'
    '<h1>Материалы<br>после встречи.</h1>'
    f'<p class="t-d">Онлайн-встреча 7 октября 2026 · версия от {e(VERSION)}</p>'
    f'<div class="t-qr">{qr(PAGE, 112, light=True)}<div><b>Живая версия страницы</b>{link(PAGE)}<span>пароль: alidi</span></div></div>'
    '<p class="t-f">ООО «Хэнд-маркетинг» · hand-marketing.ru</p></section>')

# 2. Письмо
slide('<div class="memo"><div class="m-l"><p class="mono">9.10.2026</p><p class="mono dim">после встречи 7 октября</p></div><div class="m-r">'
      '<h2>Спасибо за разговор.</h2>'
      '<p>Сейчас вам нужен не сценарий, а понятная сумма: заложить её в бюджет на 2027 год и сравнить подрядчиков на одинаковом объёме. '
      'Поэтому до 20 октября пришлём драфт-бюджет на три версии фильма: к 35-летию, партнёрскую и для HH.ru. Русский язык, съёмки на всех площадках, озвучка, графика, музыка.</p>'
      '<blockquote>«Питер… это в целом красивая картинка, которую можно показать»</blockquote>'
      '<p>Петербург добавляем, Казань считаем отдельной строкой. Форма, порядок в кадре и логотипы на вашей стороне, мы подстроимся под дни с меньшей нагрузкой. Без киношного грима.</p>'
      '<p class="sign">Александр Народецкий · Hand Marketing</p></div></div>')

# 3. Договорились + СБ
rows = [('Драфт-бюджет: три версии, русский язык, все площадки', 'Hand Marketing', '20 октября', 'hot'),
        ('Таблица фактов и цифр для заполнения', 'Hand Marketing', 'вместе с бюджетом', ''),
        ('Примеры съёмки: руководители, сотрудники, кино', 'Hand Marketing', '✓ готово', 'done'),
        ('Петербург в брифе', 'АЛИДИ', '✓ готово', 'done'),
        ('Список логотипов, которые можно показывать', 'АЛИДИ', 'до съёмок', ''),
        ('Брендбук и гайды', 'АЛИДИ', 'до сценария', ''),
        ('Даты съёмок по загрузке складов', 'вместе', 'после выбора идеи', '')]
tr = ''.join(f'<tr class="{c}"><td>{e(a)}</td><td>{e(b)}</td><td class="dt">{e(d)}</td></tr>' for a, b, d, c in rows)
sb = [('Регистрация на tender.alidi.ru', '✓ готово', 'ok'), ('Учредительные документы', '✓ загружены', 'ok'), ('Бухгалтерские документы', 'в работе', 'wip')]
slide(f'<h2 class="ttl">Договорились.</h2><div class="two"><table class="proto"><tr><th>Что</th><th>Кто</th><th>Когда</th></tr>{tr}</table>'
      '<div class="sbx"><p class="mono dim">проверка службой безопасности</p><h3>Документы на tender.alidi.ru</h3><ul>'
      + ''.join(f'<li class="{c}"><span>{e(a)}</span><b>{e(b)}</b></li>' for a, b, c in sb) + '</ul></div></div>')

# 4. География
slide('<h2 class="ttl">От Калининграда<br>до Алматы.</h2><p class="lead">Снимаем шесть городов, остальные филиалы показываем на карте стоками и архивом. '
      'Москва без командировок, в смете отдельно Петербург, Нижний, Минск, Алматы и, по желанию, Казань.</p>'
      f'<div class="route">{build.geo2_svg()}</div>', dark=True)

# 5. Карты
maps = [('map-rzd', 'ЦМ РЖД', 'Сеть терминалов от Калининграда до Находки', '/video/rgd/history/'),
        ('map-iso', '«Изотек»', 'Города присутствия загораются на карте', '/isotec/'),
        ('map-zub', 'Технопарк «Зубово»', 'Регион и подъезды к площадке', '/zubovo/'),
        ('map-bek', 'Технопарк «Бекабад»', 'Страна на карте мира и коридоры', '/bekobod1/'),
        ('map-silk', 'Silk Way Rally · 3D', 'Глобус и этап рельефом по координатам', '/video/silkway/')]
cells = ''.join(f'<div class="mc"><img src="img/{f}.jpg" alt=""><div class="mc-t"><div><b>{e(t)}</b><span>{e(x)}</span>{link(SITE + u, "страница кейса")}</div>{qr(SITE + u, 64)}</div></div>'
                for f, t, x, u in maps)
slide('<h2 class="ttl">Карта в фильме.</h2><p class="lead">Так мы уже показывали масштаб: плоско, на глобусе и в 3D. Для АЛИДИ Россия, Беларусь и Казахстан на одной карте, '
      f'точки всплывают от Калининграда до Алматы, на каждую короткий кадр с площадки.</p><div class="maps">{cells}</div>')

# 6. Пять идей
ideas = [('Сутки без остановки', 'Один рабочий день компании от 05:52 в Алматы до ночной смены. Солнце идёт с востока на запад, между городами переходим через ворота склада.', '«Обычный день АЛИДИ. 12 783-й подряд.»'),
         ('Год приёма', 'Историю рассказывают сотрудники, каждый называет год, когда пришёл. Через их места работы видно, как росла компания.', 'Самый опытный и самый новый встают рядом, за ними все герои.'),
         ('Невидимый партнёр', 'От полки в магазине назад по цепочке: склад, заказ, приёмка. Сроки «за 2 часа», «за 9 часов» настоящие.', '«Ни на одной полке нет нашего логотипа. На каждой есть наша работа.»'),
         ('Одна минута', 'Одно движение в пяти городах: коробку берут в Алматы, сканируют в Минске, ставят на паллет в Нижнем. Стандарт один везде.', '«Пять городов. Одна компания.»'),
         ('Та же точка, 35 лет спустя', 'Архивное фото в руке на фоне того же места сегодня: от первого здания в Нижнем Новгороде до площадок в трёх странах.', '«Тогда хватало одного кадра. Сегодня нужны три страны.»')]
li = ''.join(f'<li><span class="mono dim">0{i + 1}</span><div><h3>{e(a)}</h3><p>{e(b)}</p></div><p class="fin">{e(c).replace("12 783", "12&nbsp;783")}</p></li>'
             for i, (a, b, c) in enumerate(ideas))
vers = ''.join(f'<div><b>{a}</b><span class="mono">{b}</span><p>{c}</p></div>' for a, b, c in
               [('К 35-летию', '4–5 минут', 'большой экран, со звуком'), ('Партнёрская', '2:30–3:00', 'переговоры и тендеры по контрактам'), ('Для HH.ru', '60–90 секунд', 'телефон, вертикаль, без звука')])
slide(f'<h2 class="ttl">Пять идей.</h2><ol class="ideas">{li}</ol><div class="vers">{vers}</div>')

# 7–12. Как снимаем
EX = [
    ('01 · руководители', 'Интервью топ-менеджеров', 'Saint-Gobain, фильм «Клиентский опыт». Три площадки: две локации в Москве и завод. Между встречами руководителей, свет и звук наши, без профессионального грима.',
     'Иван Сычёв и руководители направлений, во всех трёх версиях.', 'img/sg-tops.jpg', '/video/saintgobain/cx/',
     [f'/images/sgcx/sp-{i:02d}@280.jpg' for i in (2, 3, 4, 5, 6, 7, 8, 9, 12, 13)], 'faces',
     'Руководителей из Казахстана и Беларуси в этом фильме мы не снимали: их записи компания прислала отдельно.'),
    ('02 · сотрудники', 'Путь клиента через всю компанию', 'Первая часть того же фильма: один заказ от рекламы до готового дома. 48 сотрудников на своих местах, каждый подписан по имени.',
     'Склады, офисы и люди в «Сутках», «Годе приёма», HR-версии.', '/images/sgcx/hero-poster.jpg', '/video/saintgobain/cx/',
     [f'/images/sgcx/{f}@560.jpg' for f in ('sc-road', 'sc-gyproc-yard', 'sc-isover-belt', 'sc-pallets', 'sc-mounting', 'sc-clients-final')], 'frames', ''),
    ('03 · масштаб', 'Вся компания и много площадок в одном фильме', 'Power Technologies на чемпионате мира 2018: 11 городов, 12 стадионов, месяц съёмок мобильными группами. Объекты, смены, руководители и инфографика в одном рассказе.',
     'Шесть городов в трёх странах, партнёрская версия.', '/images/powertech/poster-short.jpg', '/video/powertechnologies/',
     [f'/images/powertech/{f}.jpg' for f in ('obj-match', 'nums-a', 'shoot-fence', 'shoot-cables', 'shoot-gen', 'shoot-camera')], 'frames', ''),
    ('04 · история', 'Годы компании в одном ролике', 'Бренд-фильм «Изотек»: девять вех от 2012 до 2024 в графике поверх живых кадров производства, дальше география и итоги в цифрах.',
     '35 лет от 1992 года, идеи «Та же точка» и «Год приёма».', '/images/isotec/poster.jpg', '/isotec/',
     [f'/images/isotec/tl-{i}.jpg' for i in (1, 3, 5, 7, 8, 9)], 'frames', ''),
    ('05 · всё вместе', 'История, объект и интервью в одном фильме', 'ТРЦ «Павелецкая Плаза» для MMG, 5:37: архив площади и она же в проекте, рендеры, карта зоны охвата, цифры, интервью экспертов и арендаторов.',
     'История с 1992 года, площадки сегодня и голоса руководителей вместе.', '/images/mmg/poster.jpg', '/mmg/',
     [f'/images/mmg/{f}.jpg' for f in ('ren-2', 'hist-1', 'was', 'ex-1', 'num-2', 'ex-2')], 'frames', ''),
]
for k, h, txt, fit, poster, url, strip, kind, note in EX:
    st = ''.join(f'<img src="{i}" alt="">' for i in strip)
    slide(f'<div class="exs"><div class="ex-l"><p class="mono dim">как снимаем · {e(k)}</p><h2>{e(h)}</h2><p>{e(txt)}</p>'
          f'<p class="fit"><b>В вашем фильме:</b> {e(fit)}</p>' + (f'<p class="note">{e(note)}</p>' if note else '')
          + f'<div class="ql">{qr(SITE + url, 92)}<div><b>Смотреть фильм</b>{link(SITE + url, "страница кейса")}</div></div></div>'
          f'<div class="ex-r"><div class="pv"><img src="{poster}" alt=""><i></i></div><div class="strip {kind}">{st}</div></div></div>')

cine = [('VIVAX SPORT', 'реклама с Настасьей Самбурской', '/images/vivax/rest-smile.jpg', '/video/vivax/'),
        ('Газель-трансформер', 'вирусный ролик для Eaton', '/images/gaz/poster.jpg', '/video/gaz/'),
        ('УАЗ Патриот', 'рекламный ролик для Eaton', '/images/patriot/poster.jpg', '/video/patriot/')]
cc = ''.join(f'<div class="cn"><div class="pv"><img src="{p}" alt=""><i></i></div><div class="cn-t"><div><b>{e(t)}</b><span>{e(x)}</span>{link(SITE + u, "страница кейса")}</div>{qr(SITE + u, 64)}</div></div>'
             for t, x, p, u in cine)
slide('<p class="mono dim">как снимаем · 06 · для сравнения</p><h2 class="ttl">Кинематографичный уровень.</h2>'
      '<p class="lead">Грим, постановочный свет, актёры, раскадровка каждого плана. Для корпоративного фильма в таком объёме это не нужно, показываем, чтобы было с чем сравнить уровни в бюджете.</p>'
      f'<div class="cines">{cc}</div>')

# 13. Готовы участвовать
L = '/images/lib/'
cols = [('Выставочные стенды', 'Под ключ, но главное: мультимедиа и контент закладываем на этапе проекта.',
         [('Самара на ВДНХ', '/portfolio/samara-stand-vdnh/'), ('Ставрополье на ВДНХ', '/portfolio/stavropol-stand-vdnh/'), ('Как разрабатываем: проект Самары, 79 листов', '/exhibition/dizayn-stenda/')]),
        ('События', 'Основное направление с открытия агентства. Одна идея через всё мероприятие.',
         [('«Внутри стихии», ТРЦ Ривьера', '/event/riviera/'), ('Новый год Samsung', '/event/samsung/')]),
        ('Контент и медианосители', 'Проекции на здание и автомобиль, изогнутые экраны, интерактив, песочные столы.',
         [('3D mapping, Ставрополь', '/3d/stavropol/'), ('Mapping на кузове Changan', '/event/changan/'), ('Kinect, музей Алабина', '/portfolio/samara-exhibition/'), ('Песочный стол, Silk Way', '/video/silkway/')]),
        ('Дизайн', 'Своя креативная студия: айдентика, полиграфия, упаковка, сувенирная продукция.',
         [('Брендбук Metra', '/creative/metra/'), ('Чемодан Saint-Gobain', '/creative/saintgobain/suitcase/'), ('Стиль отдела продаж Becar', '/creative/becar/sdep/'),
          ('Брошюра Vertical', '/creative/becar/vertical/'), ('Календарь Saint-Gobain', '/creative/saintgobain/calendar/'), ('Набор ЦМ РЖД', '/creative/rgd/suvenir/')])]
cl = ''.join(f'<div class="mo"><h3>{e(t)}</h3><p>{e(x)}</p><ul>' + ''.join(f'<li><a href="{SITE + u}">{e(a)} ↗</a></li>' for a, u in cs) + '</ul></div>' for t, x, cs in cols)
slide(f'<h2 class="ttl">Готовы участвовать и в других проектах.</h2><div class="more">{cl}</div>'
      f'<div class="ql bottom">{qr(SITE + "/project/", 72)}<div><b>Все проекты</b>{link(SITE + "/project/")}</div></div>')

# 14. Контакты
slides.append(
    '<section class="s dk end"><div class="hd"><span>ГК АЛИДИ · имиджевый фильм к 35-летию</span><span></span></div>'
    '<h1>На связи.</h1><dl><dt>Контактное лицо</dt><dd>Александр Народецкий · Client Service Director</dd>'
    '<dt>Телефон</dt><dd>+7 985 999 87 83 · +7 495 580 75 37</dd><dt>Почта</dt><dd><a href="mailto:anarodetsky@hand-marketing.ru">anarodetsky@hand-marketing.ru</a></dd>'
    '<dt>Сайт</dt><dd><a href="https://hand-marketing.ru">hand-marketing.ru</a></dd></dl>'
    f'<div class="t-qr end-qr">{qr(PAGE, 140, light=True)}<div><b>Живая версия: материалы обновляем там</b>{link(PAGE)}<span>пароль: alidi</span></div></div>'
    '<img class="hm" src="hm-logo.svg" alt="Hand Marketing"></section>')

CSS = (HERE / 'slides.css').read_text(encoding='utf8')
doc = ('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Hand Marketing для ГК АЛИДИ · материалы</title>'
       '<link rel="stylesheet" href="/fonts/react-main.css"><link rel="stylesheet" href="/fonts/golos-ptserif.css"><link rel="stylesheet" href="/fonts/plex.css">'
       f'<style>{CSS}</style></head><body>' + '\n'.join(slides) + '</body></html>')
(ROOT / 'mirror' / 'for' / 'alidi' / '_preview-slides.html').write_text(doc, encoding='utf8')
print(len(slides), 'слайдов')
