#!/usr/bin/env python3
"""Закрытая страница для ГК «Киевская площадь» (УК «Центральная Площадь»): ответ на запрос вендор-листа.

Источники (папка ~/Documents/Тендеры/УК «Центральная Площадь»/):
  ТЗ Подрядные работы МАРКЕТИНГ.xlsx  -> tz.json (предмет, что просят, запрос на расчёт, критерии)
  src/kievskaya_data.py               -> data.py (ставки и расчёты, копия; цены меняются там и тут)
  src/kievskaya_build_md.py           -> content.py (ответы на документы, кейсы к позициям)
  КП_Хэнд-маркетинг_вендор-лист_Киевская-площадь.xlsx -> mirror/for/kievskaya-ploshchad/kp.xlsx
Текст без «ё» и без длинного тире, как в спецификации страницы.

Выход:
  mirror/for/kievskaya-ploshchad/index.php           калитка с паролем + страница (руками не править)
  mirror/for/kievskaya-ploshchad/_preview-page.html  страница без PHP, для локального превью (не коммитить)
  mirror/for/kievskaya-ploshchad/_preview-gate.html  экран пароля без PHP (не коммитить)

Запуск: python3 scripts/kievskaya-page/build.py
"""
import hashlib
import json
import re
from html import escape as e
from pathlib import Path

from content import (RATES, POS, AGENCY_FEE, DISC, clean, provide_items, status, CASES, POS_CASES, TAG,
                     PAY, FIX, PAYKEY, line_calc, task_total, discounted)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / 'mirror' / 'for' / 'kievskaya-ploshchad'

PASSWORD = 'KIEVSKAYA'  # калитка делает upper + trim, клиенту отдаём «kievskaya»
ACCESS_HASH = hashlib.sha256(PASSWORD.encode()).hexdigest()

TZ = {int(k): v for k, v in json.loads((HERE / 'tz.json').read_text(encoding='utf8')).items()}

# метка направления -> (семья HM, цвет, фигура)
FAM = {'PROD': ('orange', '#F6A500', 'fig_05'), '3D': ('pink', '#EE2BEE', 'fig_14'), 'CREATIVE': ('yellow', '#FDC400', 'fig_08'),
       'EVENTS': ('purple', '#941B80', 'fig_15'), 'BTL': ('red', '#E30521', 'fig_09')}
TAGNAME = {'PROD': 'Производство', '3D': 'CGI и 3D', 'CREATIVE': 'Креатив', 'EVENTS': 'Мероприятия', 'BTL': 'BTL и персонал'}

TAKEN = [p for p in POS if p[3]]
NT = len(TAKEN)

VAT = 0.22  # НДС начисляется сверху цен

DISC_TXT = {'svc': 'Скидка 10% на работу агентства уже в ценах расчета. Подрядчики, аренда и персонал без скидки 10%, скидка от объема.',
            'adv': 'Скидка 10% на работу агентства уже в ценах. Модели, аренда, персонал и подрядчики без скидки: скидка от объема.',
            'prod': 'Производство и закупки: скидка от объема конкретного заказа. Наши работы в составе позиции со скидкой 10%.'}

OBJECTS = ['Ривьера', 'Центральный рынок', 'Венеция', 'Времена года', 'ЦДМ на Лубянке']


def rub(x):
    return f'{x:,.0f}'.replace(',', '\u00a0') + '\u00a0₽'


def num(q):
    return (f'{q:.2f}'.rstrip('0').rstrip('.')).replace('.', ',')


def plural(n, one, few, many):
    n = abs(n) % 100
    if 10 < n < 20:
        return many
    n %= 10
    return one if n == 1 else few if 2 <= n <= 4 else many


def t(s):
    """Типографика: без «ё», без длинного тире, неразрывный пробел после коротких слов."""
    s = clean(s).replace(' - ', ': ')  # тире из ТЗ клиента тоже маркер, ставим двоеточие
    return re.sub(r'(?<![\w])([а-яА-Яa-zA-Z]{1,2}|№|\d+) (?=\S)', '\\1\u00a0', s)


# ---------- кейсы ----------
# Все торговые центры с сайта: ни один не пропускаем (просьба владельца 22.10.2026)
MALL = [
    ('riviera', 'ТРЦ «Ривьера»', 'Вечер «Внутри стихии» для почти двухсот руководителей прямо на стройке ТРЦ', '/event/riviera', '/images/riviera/stage.jpg', 'Event'),
    ('mozaika', 'ТРЦ «Мозаика»: «Пора выходить на свет»', 'Вечер для арендаторов: 134 гостя собрали новый знак ТЦ из своих лампочек', '/event/mozaika', '/images/mozaika/wall-lit.jpg', 'Event'),
    ('mozvideo', 'Ролик ТРЦ «Мозаика»', '4:31, аэросъемка, галереи и 13 синхронов арендаторов', '/video/mozaika', '/images/mozaika-video/atrium.jpg', 'Video'),
    ('salaris', 'МФК «Саларис»: презентация для арендаторов', '200 ритейлеров, площадка, концепция, презентация о трафике и ролик об объекте', '/event/salaris', '/images/salaris/hall-full.jpg', 'Event'),
    ('salaris_v', 'Ролики МФК «Саларис»', 'Объект на стадии стройки в 3D-графике и аэросъемке, аудитория зоны охвата', '/video/salaris', '/images/salaris-video/v1-cg-name.jpg', 'Video'),
    ('salaris_x', 'Новогодняя акция «Ком подарков» в «Саларисе»', 'Командная механика баллов, сайт акции, промо-корнеры, шоу с розыгрышем автомобиля', '/btl/salaris-xmas', '/images/salaris-xmas/step-site.jpg', 'BTL'),
    ('mmg', 'ТРЦ «Павелецкая Плаза»: фильм для арендаторов', 'Локация, трафик, аудитория, готовность объекта, 5:37', '/mmg', '/images/mmg/hero.jpg', 'Video'),
    ('changan', 'Changan CS35 в атриуме ТЦ', 'Три недели презентации, запись на тест-драйв, финал с 3D mapping на кузове', '/event/changan', '/images/changan/hero-show.jpg', 'Event'),
    ('marieclaire', 'Marie Claire в ТЦ Москвы', 'ГУМ, «Европейский», «Атриум», «Метрополис»: стенды, семплинг, POS, финальный вечер', '/event/marieclaire', '/images/marieclaire/corner-mall.jpg', 'Event'),
    ('becar_smile', 'Брошюра ТЦ «Смайл»', '22 полосы для инвесторов в торговые метры, инфографика доходности', '/creative/becar/smile', '/images/smile-broch/cover.jpg', 'Creative'),
    ('smile_web', 'Сайт ТРЦ «Смайл»', 'Посадочная страница инвестпродукта: восемь экранов, формы заявки, адаптив', '/digital/becar/smile', '/images/smile/hero.jpg', 'Digital'),
]
BIG = [
    ('Стенд Самарской области на ВДНХ', '204 м², экран-парус с naked eye 3D, более 18 млн посетителей выставки «Россия»', '/portfolio/samara-stand-vdnh', '/images/lib/custom-samara-vdnh/live-rocket.jpg'),
    ('Стенд Ставропольского края на ВДНХ', '248 дней работы: LED-куб с naked eye 3D, виртуальный терренкур, тач-панели', '/portfolio/stavropol-stand-vdnh', '/images/stavropol/cube-field.jpg'),
    ('3D mapping шоу в Ставрополе', '27 проекторов, 410 000 люмен, более 25 000 зрителей на площади', '/3d/stavropol', '/images/lib/as3130-6433-4331-b864-383333663738/-3-1.jpg'),
    ('Новый год Samsung', 'Зимний лес из проекций и интерактивный почтовый ящик Деда Мороза', '/event/samsung', '/images/samsung/hero.jpg'),
    ('3D-маршрут Silk Way Rally', '5 947,93 км рельефом по координатам легенды для презентации гонки', '/video/silkway', '/images/silkway/led-relief-m.jpg'),
]
# картинки для мини-карточек «Похожие проекты» внутри позиций
IMG = {m[0]: m[4] for m in MALL}
IMG.update({
    'samara': '/images/lib/custom-samara-vdnh/live-rocket.jpg', 'stavropol': '/images/lib/as3130-6433-4331-b864-383333663738/-3-1.jpg',
    'samsung': '/images/samsung/hero.jpg', 'silkway': '/images/silkway/led-relief-m.jpg',
    'sgphoto': '/images/lib/custom-sgphoto/cover-main.png', 'metra': '/images/lib/custom-metra/cover-main.png',
    'rgd': '/images/lib/as3634-3861-4239-b237-356636663535/__-60.png', 'teoxane': '/images/lib/as3538-6538-4236-b937-343132366134/__-76.png',
    'samara_brand': '/images/lib/custom-samara-brand/cover-main.png', 'becar_sdep': '/images/lib/as6366-6163-4338-b039-373730386163/__-74.png',
    'becar_wei': '/images/lib/as3532-6637-4235-a237-396563653836/__-78.png', 'sg_calendar': '/images/lib/custom-sgcalendar/cover-main.png',
    'skolkovo': '/images/lib/as3266-3963-4363-a239-646364383365/__-72.png', 'sgcx': '/images/lib/custom-sgcx/cover-main.png',
    'lingerie': '/images/lib/as3439-3739-4562-a533-616631333163/__-37.png', 'interpl': '/images/lib/as3331-3035-4965-a439-613266363431/__-54.png',
    'eaton_kz': '/images/lib/as6165-3534-4833-b866-366532623865/__-26.png', 'eaton_on': '/images/lib/as6135-3563-4735-a365-643234376439/icons-112.png',
    'messe': '/images/lib/as6536-6131-4737-a636-313561623430/__-47.png', 'becar_pm': '/images/lib/custom-becar-pm/cover-main.png',
})
MALL_KEYS = {m[0] for m in MALL}


# ---------- блоки ----------

def kick(n, title, sub=''):
    return f'<div class="kick"><i>{n}</i>{e(title)}{f"<em>{e(sub)}</em>" if sub else ""}</div>'


def hero():
    cells = []
    for no, name, objs, pay, tasks, _ in POS:
        if pay:
            fam, col, fig = FAM[TAG[no]]
            cells.append(f'<a class="c on" href="#p{no:02d}" style="--c:{col}" title="{no:02d}. {e(name)}"><img src="img/fig/{fig}.svg" alt=""><b>{no:02d}</b></a>')
        else:
            cells.append(f'<a class="c" href="#p{no:02d}" title="{no:02d}. {e(name)}: не оказываем"><b>{no:02d}</b></a>')
    legend = ''.join(f'<span style="--c:{c}"><i></i>{TAGNAME[k]}</span>' for k, (_, c, _) in FAM.items()) + '<span class="no"><i></i>Не наш профиль</span>'
    stats = [(f'{NT} из 31', 'направлений с расчетом. Остальные не наш профиль, перепродавать их не будем'),
             ('10%', 'скидка на работу агентства, уже в ценах'),
             ('6 мес.', 'фиксируем цены на работу агентства с даты КП, на производство 3 мес.'),
             ('1 менеджер', 'на 7 юрлиц холдинга, договоры на одинаковых условиях')]
    return (
        '<section class="hero"><div class="wrap">'
        '<div class="kick light"><i>КП</i>ГК «Киевская площадь» · вендор-лист маркетинговых подрядчиков</div>'
        '<div class="hg"><div>'
        f'<h1>Берем {NT} направлений из 31 и считаем каждое по вашему ТЗ</h1>'
        '<p class="lead">Один менеджер на все пять объектов и все семь юрлиц холдинга.</p>'
        '<ul class="objs">' + ''.join(f'<li>{e(o)}</li>' for o in OBJECTS) + '</ul>'
        '<div class="btns"><a class="b" href="#positions">Смотреть 31 позицию</a><a class="b o xlsx-btn" href="?xlsx=1">Скачать КП, xlsx</a></div>'
        '</div>'
        '<div class="grid31"><p class="gt">Ваша таблица из 31 строки. Нажмите на клетку, чтобы перейти к ответу</p>'
        f'<div class="cells">{"".join(cells)}</div><div class="lg">{legend}</div></div>'
        '</div>'
        '<dl class="stats">' + ''.join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in stats) + '</dl>'
        '<p class="sig">Цены без НДС, НДС 22% сверху · ООО «Хэнд-маркетинг» · с 2012 года · <a href="https://hand-marketing.ru" target="_blank" rel="noopener">hand-marketing.ru</a></p>'
        '</div></section>')


POS_STYLE = ' style="object-position:50% 85%"'  # mapping: здание внизу кадра


def card(title, sub, url, img, tag='', cls='cc'):
    return (f'<a class="{cls}" href="https://hand-marketing.ru{url}" target="_blank" rel="noopener">'
            f'<span class="ph"><img src="{img}" alt="" loading="lazy" decoding="async"{POS_STYLE if "as3130" in img else ""}>{f"<i>{e(tag)}</i>" if tag else ""}</span>'
            f'<b>{e(title)}</b><span class="s">{e(sub)}</span></a>')


def malls():
    k, title, sub, url, img, tag = MALL[0]
    big = (f'<a class="riv" href="https://hand-marketing.ru{url}" target="_blank" rel="noopener"><span class="ph"><img src="{img}" alt="Сцена вечера «Внутри стихии» в ТРЦ «Ривьера»" loading="lazy"></span>'
           '<span class="tx"><i>Ваш объект · Event</i><b>ТРЦ «Ривьера»: вечер «Внутри стихии»</b>'
           '<span class="p">Ривьера готовилась к открытию и передавала помещение «Ашан Сити» под отделку. Задача была подтвердить сроки и статус комплекса перед будущими арендаторами. '
           'Мы придумали концепцию «Внутри стихии» и провели вечер для почти двухсот руководителей прямо на стройке. Креатив прошел через все: оформление, сценарий, мультимедийный контент, кейтеринг и сувенирную продукцию. '
           'Презентационной поверхностью стали три экрана в одной композиции, ролик собрали из четырех стихий.</span><u>Открыть кейс</u></span></a>')
    rest = ''.join(card(t_, s_, u_, i_, g_) for _, t_, s_, u_, i_, g_ in MALL[1:])
    return (f'<section id="malls" class="malls"><div class="wrap">{kick("01", "Торговые центры", "все проекты подряд")}'
            '<h2>С Ривьерой мы уже работали. И еще с десятью торговыми проектами</h2>'
            '<p class="sub">Арендаторы, атриумы, ночной монтаж и служба безопасности ТЦ нам знакомы. Ниже все наши работы для торговых центров: мероприятия, ролики, акции, печать и сайты.</p>'
            f'{big}<div class="cg">{rest}</div></div></section>')


def flagships():
    cards = ''.join(card(a, b, c, d, cls='fc') for a, b, c, d in BIG)
    return (f'<section class="big"><div class="wrap">{kick("02", "Крупные проекты", "масштаб команды", )}'
            '<h2>Та же команда делает проекты федерального масштаба</h2>'
            '<p class="sub">Стенды регионов на ВДНХ, шоу на фасаде краевого парламента, новогодние события брендов. Эти проекты показывают, какой объем мы держим одновременно.</p>'
            f'<div class="fg">{cards}</div></div></section>')


def legend():
    return (f'<section class="legend"><div class="wrap">{kick("03", "Как читать предложение")}'
            '<dl class="lgd">'
            f'<div><dt><s>12\u00a0000</s> 10\u00a0800\u00a0₽</dt><dd>цена по прайсу и цена для вендор-листа со скидкой 10% на работу агентства</dd></div>'
            '<div><dt>58\u00a0000\u00a0₽</dt><dd>производство и закупки: скидка от объема конкретного заказа</dd></div>'
            '<div><dt><em>по запросу</em></dt><dd>цена зависит от макета, конструкции или объекта. Срок расчета указан в строке</dd></div>'
            '<div><dt>р.д.</dt><dd>рабочие дни, отсчет от утверждения брифа, макета или образца</dd></div>'
            '</dl><p class="vat">Все цены без НДС. НДС 22% начисляется сверху, в каждом расчете показан итог с НДС.</p></div></section>')


def price_cell(key, h, d, j):
    if d:
        return f'<s>{rub(h)}</s> <b>{rub(j)}</b>'
    return f'<b>{rub(j)}</b>'


def task_html(no, tname, term, lines, subtotal):
    tot = task_total(lines, no)
    rows = []
    vat = 0  # НДС по строкам с округлением, как в xlsx
    for key, q, lnote in lines:
        lab, unit, price, _ = RATES[key]
        c = line_calc(key, q)
        extra = f'<small>{e(t(lnote))}</small>' if lnote else ''
        if c is None:
            rows.append(f'<tr><td>{e(t(lab))}{extra}</td><td class="m">{num(q)}\u00a0{e(unit)}</td><td class="m r"><em>по запросу</em></td><td class="m r"><em>по запросу</em></td></tr>')
        else:
            h, d, j = c
            vat += round(j * VAT)
            rows.append(f'<tr><td>{e(t(lab))}{extra}</td><td class="m">{num(q)}\u00a0{e(unit)}</td><td class="m r">{rub(price)}</td><td class="m r">{price_cell(key, h, d, j)}</td></tr>')
    if no == 22:
        th = sum(line_calc(k, q)[0] for k, q, _ in lines)
        fh = round(AGENCY_FEE * th)
        vat += round(round(fh * (1 - DISC)) * VAT)
        rows.append(f'<tr><td>Агентская комиссия 12% от сметы</td><td class="m">12%</td><td class="m r"></td><td class="m r"><s>{rub(fh)}</s> <b>{rub(round(fh * (1 - DISC)))}</b></td></tr>')
    if tot is not None and not subtotal and len(lines) > 1:
        total = '<em>цена по строкам</em>'  # варианты тиража, а не одна смета
    else:
        total = (f'{rub(tot)}<small>без НДС · с НДС {rub(tot + vat)}</small>' if tot is not None else '<em>по запросу</em>')
    return (f'<div class="task"><div class="th"><h4>{e(t(tname))}</h4><span class="term">{e(t(term or "по согласованию"))}</span><span class="tot m">{total}</span></div>'
            f'<div class="tw"><table><thead><tr><th>Строка</th><th>Объем</th><th class="r">Цена за ед., без НДС</th><th class="r">Для вендор-листа, без НДС</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></div>')


def positions():
    out = []
    for no, name, objs, pay, tasks, note in POS:
        tz = TZ[no]
        if not pay:
            out.append(f'<div class="pos off" id="p{no:02d}" data-s="off"><div class="row"><span class="no m">{no:02d}</span><span class="nm">{e(name)}</span>'
                       f'<span class="ob">{e(objs)}</span><span class="tg">Не оказываем</span></div></div>')
            continue
        tg = TAG[no]
        _, col, fig = FAM[tg]
        if len(tasks) == 1:
            first = task_total(tasks[0][2], no)
            head = rub(first) if first is not None else '<em>по запросу</em>'
        else:
            head = f'{len(tasks)} {plural(len(tasks), "расчет", "расчета", "расчетов")}'
        docs = provide_items(tz['provide'])
        docs_html = ''
        if docs:
            docs_html = ('<div class="docs"><h5>Что просили предоставить</h5><ol>' +
                         ''.join(f'<li><span>{e(t(it))}</span><b>{e(t(status(it, no)))}</b></li>' for it in docs) + '</ol></div>')
        refs = POS_CASES.get(no, [])
        refs_html = ''
        if refs:
            refs_html = '<div class="refs"><h5>Похожие проекты</h5><div>' + ''.join(
                f'<a href="{CASES[k][2]}" target="_blank" rel="noopener"><img src="{IMG.get(k, "")}" alt="" loading="lazy"><b>{e(t(CASES[k][0]))}</b><span>{e(t(CASES[k][1]))}</span></a>'
                for k in refs) + '</div></div>'
        out.append(
            f'<details class="pos" id="p{no:02d}" data-s="on" style="--c:{col}"><summary class="row"><span class="no m">{no:02d}</span><span class="nm">{e(name)}</span>'
            f'<span class="ob">{e(objs)}</span><span class="tg"><img src="img/fig/{fig}.svg" alt="">{TAGNAME[tg]}</span><span class="hd m">{head}</span><span class="ar" aria-hidden="true"></span></summary>'
            '<div class="body">'
            f'<div class="ask"><h5>Ваш запрос</h5><p>{e(t(tz["subject"]))}</p>' + (f'<p class="rq">{e(t(tz["request"]))}</p>' if tz.get('request') else '') + '</div>'
            + ''.join(task_html(no, tn, term, lines, sub) for tn, term, lines, sub in tasks) +
            '<dl class="facts">'
            f'<div><dt>Что входит</dt><dd>{e(t(note))}</dd></div>'
            f'<div><dt>Оплата и фиксация</dt><dd>{e(PAY[PAYKEY.get(no, pay)])}. {e(FIX[PAYKEY.get(no, pay)])}.</dd></div>'
            f'<div><dt>НДС и скидка</dt><dd>Цены без НДС, НДС 22% сверху. {e(DISC_TXT[PAYKEY.get(no, pay)])}</dd></div>'
            f'<div><dt>Ваши критерии</dt><dd>{e(t(tz["criteria"]))}</dd></div></dl>'
            f'{docs_html}{refs_html}</div></details>')
    flt = (f'<div class="flt" role="tablist"><button class="on" data-f="all">Все 31</button><button data-f="on">Берем {NT}</button>'
           f'<button data-f="off">Не оказываем {31 - NT}</button><button class="ex" data-x="1">Раскрыть все</button></div>')
    return (f'<section id="positions" class="positions"><div class="wrap">{kick("04", "Все 31 направление", "построчно, как в ТЗ")}'
            '<h2>Ваша таблица, наши ответы построчно</h2>'
            '<p class="sub">Номера и порядок строк как в вашем ТЗ. Нажмите на строку: внутри расчет по вашему запросу, условия, ответы на документы и похожие проекты.</p>'
            f'{flt}<div class="plist">{"".join(out)}</div></div></section>')


def prices():
    blocks = []
    for no, name, objs, pay, tasks, note in POS:
        if not pay:
            continue
        _, col, fig = FAM[TAG[no]]
        rows = []
        for k in [k for k in RATES if k.startswith(f'p{no}_')]:
            lab, unit, price, rnote = RATES[k]
            if price is None:
                a = b = '<em>по запросу</em>'
            elif price == 0:
                a = b = 'бесплатно'
            else:
                a = rub(price)
                b = f'<b>{rub(round(price * (1 - DISC)))}</b>' if discounted(k) else f'<b>{rub(price)}</b><small>скидка от объема</small>'
            rows.append(f'<tr><td>{e(t(lab))}{f"<small>{e(t(rnote))}</small>" if rnote else ""}</td><td class="m">{e(unit)}</td><td class="m r">{a}</td><td class="m r">{b}</td></tr>')
        blocks.append(f'<details class="pr" style="--c:{col}"><summary><img src="img/fig/{fig}.svg" alt=""><span class="m">{no:02d}</span>{e(name)}<i>{len(rows)}</i></summary>'
                      f'<div class="tw"><table><thead><tr><th>Услуга или изделие</th><th>Ед.</th><th class="r">По прайсу, без НДС</th><th class="r">Для вендор-листа, без НДС</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></details>')
    return (f'<section id="price" class="price"><div class="wrap">{kick("05", "Прайс")}'
            '<h2>Ставки на разовые задачи</h2><p class="sub">Те же цены, что в расчетах выше, плюс почасовые и поштучные ставки.</p>'
            f'<div class="prl">{"".join(blocks)}</div>'
            '<p class="extra">Доплаты: ночной монтаж с 23:00 до 07:00 плюс 30% к стоимости монтажа, кроме ночной смены монтажника: она уже ночная. Срочный выезд монтажной бригады в течение 24 часов плюс 25% к стоимости смен. '
            'Срочный текст день в день плюс 50%. Агентская комиссия на мероприятия 12% от сметы.</p></div></section>')


TERMS = [
    ('НДС', 'ООО «Хэнд-маркетинг» на ОСНО. Цены указаны без НДС, НДС 22% начисляется сверху'),
    ('Скидка на работу агентства', '10% уже в ценах: креатив, дизайн, тексты, CGI, фото- и видеосъемка, продюсирование, концепции, эскизы, агентская комиссия'),
    ('Подрядчики, аренда, персонал', 'Модели, аренда техники, звукорежиссер, диджей, промоутеры, монтажники и логистика без скидки 10%: считаем по объему заказа'),
    ('Скидка на производство', 'Производство, тиражи и закупки считаем от объема конкретного заказа. Чем больше тираж или пакет работ, тем ниже цена'),
    ('Оплата услуг', '100% по факту, в течение 10 рабочих дней после акта. Где есть расходы на подрядчиков (съемка с моделями, звук и свет, диджей, звукорежиссер, персонал), аванс 50%'),
    ('Оплата производства, тиражей, мероприятий', 'Аванс 70%, остаток 30% после акта'),
    ('Фиксация цен', 'Работа агентства: 6 месяцев с даты КП. Производство, тиражи и закупки: 3 месяца с даты КП, дальше пересчет по ценам поставщиков на дату заказа'),
    ('Сроки', 'В рабочих днях. Отсчет от утверждения брифа, макета или образца'),
    ('Правки', 'Количество кругов указано в каждой позиции'),
    ('Права', 'Исключительные права на креатив, ролики, фото и исходники передаем по договору. Музыка, шрифты, стоки и AI-материалы передаются в объеме их лицензий'),
    ('Работа в ТЦ', 'Пропуска, ночной режим, вывоз мусора, согласование со службой безопасности объекта'),
]
EXTRA = [
    ('11 · 12', 'Тестовые задания по дизайну и текстам выполним бесплатно, до договора.'),
    ('22', 'Концепция мероприятия бесплатно. Агентская комиссия 12% отдельной строкой, как просили.'),
    ('01', 'Замер под рекламные конструкции бесплатно, выезд в течение 1 рабочего дня.'),
    ('15', 'Над центром Москвы полеты ограничены, поэтому в атриумах снимаем FPV-дроном внутри объекта.'),
    ('31', 'Зеркальный пол фотозоны закрываем антискользящей защитной пленкой: по нему ходят каждый день.'),
    ('···', 'Позиции «по запросу» считаем за 2-3 рабочих дня после макета, эскиза или выезда.'),
]
ENTITIES = [('ООО «ЦДМ на Лубянке»', '9702064516'), ('ООО «Октан плюс Альфа»', '7704256001'), ('ООО «Квинта»', '9721099017'),
            ('ООО «Монолит»', '7724894524'), ('ООО «Центральная Площадь»', '7730338370'), ('ИП Ягубов Н.Ш.', '502743704780'),
            ('ИП Хананияев Ш.А.', '771899849300')]
NEXT = [
    ('01', 'Тестовые задания', 'Пришлите ключевой визуал и бриф: адаптируем в сторис и баннер 3 × 6 м и напишем пост-анонс. Бесплатно.'),
    ('02', 'Встреча с маркетологами объектов', 'Разбираем годовой план по направлениям, чтобы посчитать скидку от объема.'),
    ('03', 'Договоры', 'Одинаковые условия для семи юрлиц, один менеджер.'),
    ('04', 'Первая задача', 'Новогодняя кампания: ролик, оформление атриума, мерч. По позициям «по запросу» расчет за 2-3 дня после брифа.'),
]


def rest():
    o = []
    o.append(f'<section id="terms" class="terms"><div class="wrap">{kick("06", "Условия")}<h2>Условия для вендор-листа</h2><dl class="tl">' +
             ''.join(f'<div><dt>{e(a)}</dt><dd>{e(t(b))}</dd></div>' for a, b in TERMS) + '</dl></div></section>')
    o.append(f'<section class="extra-s"><div class="wrap">{kick("07", "Сверх запроса")}<h2>То, о чем вы не спрашивали</h2><ul class="xl">' +
             ''.join(f'<li><i class="m">{e(a)}</i><span>{e(t(b))}</span></li>' for a, b in EXTRA) + '</ul></div></section>')
    o.append(f'<section class="ent"><div class="wrap">{kick("08", "Юрлица холдинга")}<h2>Семь договоров на одинаковых условиях</h2>'
             '<p class="sub">По письму № 38/2026 от 16.03.2026 закрепляем одного менеджера и заключаем договоры на одинаковых условиях со всеми юрлицами.</p><ul class="el">' +
             ''.join(f'<li><b>{e(a)}</b><span class="m">ИНН {b}</span></li>' for a, b in ENTITIES) +
             '</ul><p class="note">Условия СК «Олимпийский» нам не известны. Пришлите параметры, и мы сверим их с нашими по сопоставимым позициям за 2 рабочих дня.</p></div></section>')
    o.append(f'<section class="next"><div class="wrap">{kick("09", "Что дальше")}<h2>Четыре шага до первой задачи</h2><ol class="nl">' +
             ''.join(f'<li><i class="m">{a}</i><b>{e(b)}</b><span>{e(t(c))}</span></li>' for a, b, c in NEXT) + '</ol></div></section>')
    o.append('<section id="contacts" class="contacts"><div class="wrap">' + kick('10', 'Контакты') +
             '<div class="ct"><div><h2>Один менеджер на все пять объектов</h2>'
             '<div class="btns"><a class="b" href="https://t.me/narodetskii" target="_blank" rel="noopener">Написать в Telegram</a>'
             '<a class="b o" href="tel:+79859998783">+7 985 999-87-83</a><a class="b o xlsx-btn" href="?xlsx=1">Скачать КП, xlsx</a></div></div>'
             '<dl><dt>Контактное лицо</dt><dd><b>Народецкий Александр</b><br>Client Service Director</dd>'
             '<dt>Телефон</dt><dd><a href="tel:+79859998783">+7 985 999-87-83</a> · <a href="tel:+74955807537">+7 495 580-75-37</a></dd>'
             '<dt>Почта</dt><dd><a href="mailto:anarodetsky@hand-marketing.ru?subject=Вендор-лист%20Киевская%20площадь">anarodetsky@hand-marketing.ru</a></dd>'
             '<dt>Офис</dt><dd>123022, Москва, ул. Рочдельская, 14А</dd>'
             '<dt>Реквизиты</dt><dd>ООО «Хэнд-маркетинг» · ИНН 7709931482 · КПП 770901001 · ОГРН 1137746525608</dd></dl></div>'
             '<p class="foot">Страница подготовлена для ГК «Киевская площадь» · доступ по личному приглашению</p></div></section>')
    return ''.join(o)


def page():
    nav = ('<header class="top"><div class="wrap ti"><img src="hm-logo.svg" alt="Hand Marketing"><span class="x">× ГК «Киевская площадь»</span>'
           '<nav><a href="#malls">ТЦ</a><a href="#positions">31 позиция</a><a href="#price">Прайс</a><a href="#terms">Условия</a><a href="#contacts">Контакты</a></nav></div></header>')
    return nav + hero() + malls() + flagships() + legend() + positions() + prices() + rest()


CSS = (HERE / 'page.css').read_text(encoding='utf8')
JS = (HERE / 'page.js').read_text(encoding='utf8')
TRACK = (HERE / 'track.js').read_text(encoding='utf8')

HEAD = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#080000">
<title>Hand Marketing для ГК «Киевская площадь»</title>
<meta name="description" content="__NT__ направлений для маркетинговых отделов пяти объектов: расчеты по ТЗ, прайс, условия, проекты в торговых центрах.">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/react-main.css">
<link rel="stylesheet" href="/fonts/plex.css">
<style>
'''.replace('__NT__', str(NT)) + CSS + '''
</style>
</head>
<body>
'''

METRIKA = '''<script>
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
ym(71125393, "init", { clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true, params:{ private_page:'kievskaya-ploshchad' } });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute; left:-9999px;" alt=""></div></noscript>
'''

BODY = HEAD + page() + '\n<script>\n' + JS + '\n</script>\n'
PAGE_PHP = BODY + '<script id="hm-kp-analytics">\n' + TRACK + '\n</script>\n' + METRIKA + '</body>\n</html>\n'
PAGE_PREVIEW = BODY + '</body>\n</html>\n'

GATE_HTML = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Доступ к странице · ГК «Киевская площадь» × Hand Marketing</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/react-main.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Inter',system-ui,sans-serif; color:#080000; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:20px; background:#FAFAF8; }
  .gate { width:100%; max-width:440px; padding:40px 34px 30px; border-radius:6px; background:#fff; border:1px solid #E7E7E4; box-shadow:0 30px 60px -30px rgba(8,0,0,.18); position:relative; overflow:hidden; }
  .gate:before { content:""; position:absolute; left:0; right:0; top:0; height:6px; background:linear-gradient(90deg,#93C01F 0 14.3%,#F6A500 0 28.6%,#60C0D8 0 42.9%,#941B80 0 57.1%,#FDC400 0 71.4%,#EE2BEE 0 85.7%,#E30521 0); }
  .logos { display:flex; align-items:center; gap:12px; margin-bottom:30px; font-family:'Montserrat',sans-serif; font-weight:700; font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:#8C8C88; }
  .logos img { height:30px; }
  h1 { font-family:'Montserrat',sans-serif; font-weight:800; font-size:30px; line-height:1.1; letter-spacing:-.02em; margin-bottom:12px; }
  .sub { font-size:15px; color:#4A4A47; margin-bottom:24px; }
  form { display:flex; flex-direction:column; gap:10px; }
  input { font-family:'IBM Plex Mono',monospace; font-weight:500; font-size:19px; letter-spacing:.14em; text-align:center; text-transform:uppercase; color:#080000;
    padding:14px; border:1.5px solid #C8C8C4; border-radius:6px; outline:none; background:#fff; }
  input:focus { border-color:#080000; }
  button { font-family:'Montserrat',sans-serif; font-weight:700; font-size:15px; color:#fff; background:#080000; border:0; border-radius:6px; padding:16px; cursor:pointer; }
  button:hover { background:#941B80; }
  .gate-error { color:#E30521; font-size:13px; margin-top:4px; text-align:center; }
  .note { margin-top:22px; font-size:12px; color:#8C8C88; text-align:center; }
</style>
</head>
<body>
  <div class="gate">
    <div class="logos"><img src="hm-logo.svg" alt="Hand Marketing"><span>× Киевская площадь</span></div>
    <h1>Вендор-лист: наш ответ на 31 позицию</h1>
    <p class="sub">Расчеты по ТЗ, прайс, условия и проекты в торговых центрах. Введите код доступа из письма</p>
    <form method="post" action="./" autocomplete="off">
      <input type="text" name="code" placeholder="код доступа" maxlength="30" autocapitalize="characters" spellcheck="false" autofocus required>
      <button type="submit">Открыть предложение</button>
      {$errHtml}
    </form>
    <p class="note">Hand Marketing · доступ по личному приглашению</p>
  </div>
</body>
</html>
'''

PHP_HEAD = r'''<?php
// Закрытая страница для ГК «Киевская площадь»: ответ на запрос вендор-листа. Доступ по коду.
// Собирается scripts/kievskaya-page/build.py, руками не править.
// В файле только SHA-256 хеш кода. Аналитика визитов: _analytics.php, отчёт по ?stats=<ключ>.
define('HM_KP', 1);
date_default_timezone_set('Europe/Moscow');
require __DIR__ . '/_analytics.php';

$ACCESS_HASH = '__HASH__';
$COOKIE_NAME = 'hm_kp_access';

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
        setcookie($COOKIE_NAME, $ACCESS_HASH, time() + 60 * 60 * 24 * 30, '/for/kievskaya-ploshchad/', '', hm_https(), true);
        $g = hm_geo(hm_ip());
        hm_event('login_ok', array('geo' => $g));
        hm_tg("🔓 <b>Киевская площадь открыла страницу</b>\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where($g) . "\n" . date('d.m H:i'));
        header('Location: ./');
        exit;
    }
    // введённый текст не сохраняем: это может оказаться чужой пароль
    hm_event('login_fail', array('len' => function_exists('mb_strlen') ? mb_strlen($input) : strlen($input)));
    $error = true;
}

if (!$authed) {
    if ($_SERVER['REQUEST_METHOD'] === 'GET') hm_event('gate_view');
    $errHtml = $error ? '<p class="gate-error">Код не подошел. Попробуйте еще раз.</p>' : '';
    echo <<<GATE
__GATE__
GATE;
    exit;
}
// КП в Excel: только после входа, прямой доступ к файлу закрыт в .htaccess
if (isset($_GET['xlsx'])) {
    $f = __DIR__ . '/kp.xlsx';
    if (!is_file($f)) { http_response_code(404); exit; }
    hm_event('xlsx_download');
    hm_tg("📄 <b>Киевская площадь скачала КП (xlsx)</b>\n" . hm_device(isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '') . "\n" . hm_where(hm_geo(hm_ip())) . "\n" . date('d.m H:i'));
    header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    header("Content-Disposition: attachment; filename=\"Hand_Marketing_KP_Kievskaya_ploshchad.xlsx\"; filename*=UTF-8''" . rawurlencode('КП_Хэнд-маркетинг_вендор-лист_Киевская-площадь.xlsx'));
    header('Content-Length: ' . filesize($f));
    readfile($f);
    exit;
}
hm_event('page_view');
?>
'''

if __name__ == '__main__':
    assert '$' not in GATE_HTML.replace('{$errHtml}', ''), 'в экране пароля не должно быть $ кроме {$errHtml}'
    assert '<?' not in PAGE_PHP, 'в странице не должно быть <?'
    for bad in ('ё', 'Ё', '—'):
        assert bad not in page(), f'в тексте страницы есть «{bad}»'
    php = PHP_HEAD.replace('__HASH__', ACCESS_HASH).replace('__GATE__', GATE_HTML.rstrip('\n')) + PAGE_PHP
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'index.php').write_text(php, encoding='utf8')
    (OUT / '_preview-page.html').write_text(PAGE_PREVIEW, encoding='utf8')
    (OUT / '_preview-gate.html').write_text(GATE_HTML.replace('{$errHtml}', ''), encoding='utf8')
    # все картинки страницы должны лежать в mirror
    miss = sorted({p for p in re.findall(r'src="(/images/[^"]+)"', PAGE_PREVIEW) if not (ROOT / 'mirror' / p.lstrip('/')).exists()})
    assert not miss, f'нет картинок: {miss}'
    print('ok', len(php), 'байт')
