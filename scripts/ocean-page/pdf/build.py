#!/usr/bin/env python3
"""Версия для печати страницы океанариума: A4 альбом, данные берутся из scripts/ocean-page/build.py.

Порядок сборки:
  1. python3 scripts/ocean-page/build.py            (страница и _preview-page.html)
  2. node scripts/ocean-page/pdf/capture.mjs         (скриншоты интерактивов, нужен PHP-сервер mirror на :8093)
  3. python3 scripts/ocean-page/pdf/build.py         (HTML в scripts/ocean-page/pdf/out/print.html)
  4. node scripts/ocean-page/pdf/render.mjs          (PDF в mirror/for/oceanarium/oceanarium.pdf)
"""
import os
import sys
from html import escape as e

import segno

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build as ob  # noqa: E402  данные страницы

ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
M = 'file://' + os.path.join(ROOT, 'mirror')
IMG = M + '/for/oceanarium/img/'
CAP = 'file://' + os.path.join(HERE, 'captures') + '/'
LIVE = 'https://hand-marketing.ru/for/oceanarium/'


def qr(url):
    return segno.make(url, error='m').svg_inline(scale=1, border=2, dark='#0b1f2e', light='#ffffff', omitsize=True)


def im(name, cls=''):
    return f'<img class="{cls}" src="{IMG}{name}.jpg" alt="">'


def cap(name, cls=''):
    return f'<img class="{cls}" src="{CAP}{name}.jpg" alt="">'


pages = []


def page(body, cls=''):
    n = len(pages) + 1
    foot = (f'<div class="foot"><img src="{M}/for/oceanarium/hm-logo.svg" alt=""><span>Hand Marketing для океанариума · версия для печати</span>'
            f'<em>интерактивная версия: hand-marketing.ru/for/oceanarium</em><b>{n:02d}</b></div>')
    pages.append(f'<section class="pg {cls}">{body}{foot}</section>')


def head(kick, title):
    return f'<div class="kick">{kick}</div><h2>{title}</h2>'


# 01 обложка
page(f'''{im("p-hug", "bleed")}<div class="shade"></div>
<div class="cover">
  <div class="kick light">Океанариум · мультимедиа</div>
  <h1>Глубина.<span>Три проекта для океанариума</span></h1>
  <div class="trio">
    <div><i>01</i><b>WOW-зона «Глубина»</b><span>Закрытый зал или мультимедийная стена, интерактивный пол, модули</span></div>
    <div><i>02</i><b>Пингвин Гумбольдта</b><span>Ростовой маскот, лицо рисует свет изнутри головы</span></div>
    <div><i>03</i><b>Экраны входной группы</b><span>Боковые экраны, экран в арке и световая арка</span></div>
  </div>
  <div class="qrb"><div class="qr">{qr(LIVE)}</div><div><b>Это версия для печати</b><span>Схемы в движении, демо пола, касания маскота и выбор идей для расчёта работают на странице: hand-marketing.ru/for/oceanarium</span></div></div>
</div>''', 'dark')

# 02 запрос
rows = ''.join(f'<tr><td class="n">{i + 1:02d}</td><td><b>{e(t)}</b></td><td>{e(d)}</td></tr>' for i, (t, d) in enumerate(ob.REQ))
rows += '<tr class="plus"><td class="n">+</td><td><b>Точка съёмки</b></td><td>Место под вертикальное видео, где в финале сеанса глаз кашалота встаёт ровно за спиной гостя</td></tr>'
page(head('01 · WOW-зона · ваш запрос построчно', 'Каждое требование и как мы его закрываем') +
     f'<table class="tbl">{rows}</table>'
     '<p class="note box">Так закрываем запрос, если есть возможность построить закрытую зону. Дополнительно рассматриваем мультимедийную стену прямо на маршруте: какой вариант подходит, станет понятно после технического визита.</p>')

# 03 концепция
ch = ''.join(f'<div class="ch">{cap(f"dive-{i}")}<div><b style="color:{c}">{f"{d:,}".replace(",", " ")} м</b><i>{e(n)}</i><p>{e(t)}</p></div></div>'
             for i, (d, n, t, c) in enumerate(ob.CHAPTERS))
page(head('Концепция · шоу 5 минут, пять глав', '11 километров вниз за пять минут') +
     '<p class="lead">Посетитель входит в тёмный зал и начинает погружение. На стене глубиномер, цифры растут. С каждой главой меняются свет, звук и обитатели: тот же океан, что за стеклом аквариумов, только на глубине, куда человек не спускается. Героями глав становятся ваши обитатели: пингвины Гумбольдта, рифовые акулы, скаты.</p>'
     f'<div class="chs">{ch}</div>')

# 04 режимы и пол
fl = ''.join(f'<div class="fl">{cap("floor-" + k)}<b>{i + 1:02d} · {e(n)}</b><p>{e(t)}</p></div>' for i, (k, n, t) in enumerate(ob.FLOOR))
page(head('Опыт посетителя и интерактив', 'Два режима, и пол отвечает на каждый шаг') +
     '<div class="cols2"><div class="card"><i>Режим 1 · между сеансами</i><b>Свободное плавание</b><p>Спокойный океан на стенах, петля 10 минут. Пол интерактивный, сцены меняются по кругу.</p></div>'
     '<div class="card"><i>Режим 2 · сеанс</i><b>Погружение</b><p>Запуск автоматически, когда датчик видит группу. 5 минут, пять глав, звук вокруг зрителя, в финале кадр для соцсетей.</p></div></div>'
     f'<div class="fls">{fl}</div>'
     '<p class="note">Интерактивный пол делаем, если есть техническая возможность: высота потолка, точки подвеса и покрытие пола проверяем на техническом визите. Две камеры глубины под потолком видят людей в темноте, новая сцена к празднику ставится файлом.</p>')

# 05 два варианта
lay = lambda L: ''.join(f'<li><b style="color:{c}">{e(n)}</b> {e(t)}</li>' for _, n, t, c in L)
page(head('Техническое решение · два варианта', 'Отдельный зал или стена на маршруте') +
     f'<div class="cols2 plans"><div><h3>А · Закрытый зал 8,5 × 6 м</h3><div class="svgbox">{ob.plan_svg()}</div><ul class="lay">{lay(ob.LAYERS)}</ul></div>'
     f'<div><h3>Б · Мультимедийная стена</h3><div class="svgbox">{ob.wall_svg()}</div><ul class="lay">{lay(ob.LAYERS_B)}</ul></div></div>')

# 06 сравнение
cmp_rows = ''.join(f'<tr><td><b>{e(k)}</b></td><td>{e(x)}</td><td>{e(y)}</td></tr>' for k, x, y in ob.COMPARE)
page(head('Техническое решение · сравнение', 'Что выбрать: зал или стену') +
     f'<table class="tbl cmp"><tr class="th"><td></td><td>А · Закрытый зал</td><td>Б · Мультимедийная стена</td></tr>{cmp_rows}</table>'
     '<p class="note">Почему для стены LED, а не проекция: в открытой части свет экспозиции и витрины засвечивают проекцию, светодиодная стена держит картинку при любом свете. Размеры стены и шаг пикселя ориентировочные, уточняем по плану и фото места.</p>')

# 07 оборудование
eq = ''.join(f'<tr><td class="big">{n}</td><td><b>{e(t)}</b></td><td>{e(d)}</td></tr>' for n, t, d in ob.EQ)
six = ''.join(f'<div class="card sm"><i>{n}</i><b>{e(t)}</b><p>{e(d)}</p></div>' for n, t, d, _ in ob.SIX)
page(head('Оборудование · вариант А', 'Ориентировочный состав оборудования') +
     '<p class="note box">Состав приблизительный, пока без расчёта проектировщика и инженера. Модели и количество уточняем в проекте.</p>'
     f'<table class="tbl">{eq}</table><div class="grid3">{six}</div>')

# 08 модули
mods = ''.join(f'<div class="card"><i>{e(k)}</i><b>{e(t)}</b><p>{e(d)}</p><em>{e(term)}</em></div>' for t, k, d, fl_, term, _ in ob.MODS)
page(head('Модули · берутся сразу или во вторую очередь', 'Что ещё делает зону живой') +
     f'<div class="cols2"><div class="card hl"><i>стол на 6 мест и сканер</i><b>Нарисуй рыбу и отпусти её в океан</b><p>Ребёнок раскрашивает бланк, кладёт под сканер, и через пять секунд его рыба плывёт по стене в общем косяке. Рисунок можно забрать домой в фирменной рамке. Место 4 кв. м рядом с залом, розетка и точка сети. На странице это можно попробовать: раскрашенная рыба уплывает в косяк.</p></div>{mods}</div>'
     '<p class="note">Модули считаются отдельно от зала.</p>')

# 09 маскот 1
faces = ''.join(f'<div class="face">{im(f)}<b>{e(n)}</b><span>{e(t)}</span></div>' for _, (f, n, t) in ob.FACES.items())
page(head('02 · Маскот · модуль для зала', 'Пингвин, которого хочется обнять') +
     f'<div class="masc"><div>{im("p-hug", "ph")}</div><div>'
     '<p class="lead">Ростовая фигура с 3D-печати. Лицо не нарисовано, а проецируется изнутри головы: маскот моргает, говорит, следит взглядом и меняет настроение.</p>'
     '<div class="nums"><div><b>1,9 м</b><span>рост</span></div><div><b>0,1 с</b><span>от касания до реакции</span></div><div><b>9</b><span>состояний</span></div><div><b>0</b><span>движущихся частей</span></div></div>'
     '<p class="note box warn"><b>Драфт.</b> Предложение по маскоту будет скорректировано после разработки проекта: размеры, оснащение и сценарии уточним вместе с вами.</p>'
     f'</div></div><div class="faces">{faces}</div>')

# 10 маскот 2
parts = ''.join(f'<li><i>{i + 1}</i><b>{e(n)}</b> {e(d)}</li>' for i, (n, d, *_) in enumerate(ob.PARTS))
day = ''.join(f'<div class="dayc">{im(f)}<b>{t} · {e(n)}</b><span>{e(d)}</span></div>' for t, n, d, f, _ in ob.DAY)
page(head('Маскот · как устроен и как живёт', 'Что внутри и один день пингвина') +
     f'<div class="anat">{im("p-inside", "ph")}<ol class="parts">{parts}</ol></div><div class="days">{day}</div>')

# 11 маскот 3
st = ''.join(f'<div class="st"><b>{e(n)}</b><em>{e(t)}</em><p>{e(d)}</p></div>' for n, t, d, _ in ob.STATES)
mk = ''.join(f'<div class="mk">{im(f)}<b>{k} · {e(n)}</b><span>{e(d)}</span></div>' for k, n, d, f in ob.MAKE)
page(head('Маскот · сценарии, варианты лица, производство', 'Девять состояний и путь от эскиза до зала') +
     f'<div class="states">{st}</div>'
     f'<div class="cols2 opts"><div class="card">{im("opt-mask", "opt")}<b>Проектор на всю маску</b><p>Мимика на всё лицо, маска меняется за 10 минут, внутри нужна тихая вентиляция. Лучше для затемнённого зала.</p></div>'
     f'<div class="card">{im("opt-eyes", "opt")}<b>Экраны в глазах</b><p>Лицо скульптурное, светятся только глаза, почти не греется. Мимика скромнее. Лучше для светлого входа.</p></div></div>'
     f'<div class="make">{mk}</div>')

# 12 LED фасад
page(head('03 · Экраны входной группы · проект ТЗ, параметры ориентировочные', 'Три экрана и световая арка в одной композиции') +
     f'<div class="ledimg">{cap("led")}</div>'
     f'<div class="grid3"><div class="card sm"><i>10</i><b>Световая арка</b><p>Адресная лента в рассеивающем профиле по наружной и внутренней кромке, около 36 м. Свет ведёт тот же медиасервер, волна бежит по арке вместе с контентом.</p></div>'
     f'<div class="card sm"><i>11</i><b>Экран в арке</b><p>Над входом, ступенями по контуру: ориентир {ob.ARCH_MOD} модулей 250 × 250, около {str(ob.ARCH_MOD * 0.0625).replace(".", ",")} кв. м. Та же технология и общая калибровка с боковыми.</p></div>'
     '<div class="card sm"><i>12</i><b>Боковые экраны</b><p>Два экрана по 13,4 кв. м, шаг 2 мм, по 215 модулей. Рыба уплывает с левого экрана и появляется на правом после паузы, равной ширине арки.</p></div></div>'
     '<p class="note">Размеры в мм, контур арки принят условно до получения чертежа.</p>')

# 13 LED параметры
spec = ''.join(f'<tr><td><b>{e(k)}</b></td><td>{e(v)}</td></tr>' for k, v in ob.LED_SPEC)
page(head('Экраны · требования', 'Параметры экранов') +
     f'<div class="cols2 wide"><table class="tbl small">{spec}</table><div>'
     '<div class="card sm"><b>Конструкция</b><p>Своя стальная рама на анкерах в пол, перегородка из ГКЛ нагрузку не несёт. Металл заземлён, острых элементов в зоне посетителей нет, кабели нг(А)-LS.</p></div>'
     '<div class="card sm"><b>Питание</b><p>380/220 В, 3 фазы. Ориентир до расчёта: пик до 16 кВт, в среднем около 5,4 кВт плюс экран в арке и свет. После отключения сети экран включается сам.</p></div>'
     '<div class="card sm"><b>Синхронность</b><p>Один видеопроцессор ведёт все экраны кадр в кадр.</p></div>'
     '<div class="card sm"><b>Документы и сервис</b><p>До производства: спецификация, раскладка по контуру арки, карта пикселей, расчёт рамы, однолинейная схема. Условия гарантии и сервиса фиксируем в договоре.</p></div>'
     '</div></div>')

# 14 вопросы с местом для ответа
q = ''.join(f'<tr><td class="n">{i + 1:02d}</td><td><b>{e(qq)}</b><span>Наше предложение: {e(a)}</span></td><td class="ck">☐ верно<br>☐ иначе: ____________</td></tr>'
            for i, (qq, a) in enumerate(ob.LED_Q))
page(head('Экраны · параметры для просчёта, Оренбург', 'Подтвердите или впишите свой вариант') +
     f'<table class="tbl qs">{q}</table>')

# 15 сроки и где заказывать
W = ob.WEEKS
g = '<tr class="th"><td>Неделя</td>' + ''.join(f'<td class="w">{i}</td>' for i in range(1, W + 1)) + '</tr>'
for t, s_, f_, c in ob.GANTT:
    g += f'<tr><td>{e(t)}</td>' + ''.join(f'<td class="w"><i style="background:{c}"></i></td>' if s_ <= w <= f_ else '<td class="w"></td>' for w in range(1, W + 1)) + '</tr>'
page(head('Сроки WOW-зоны · ориентир, уточняется в расчёте', 'Около 80 рабочих дней от договора до запуска') +
     f'<table class="gantt">{g}</table>'
     '<div class="note box"><b>Где заказывать оборудование и экраны?</b> Производство в Китае обычно дешевле, но поставка дольше. В России быстрее, но дороже. Какой вариант считать: ☐ в России ☐ в Китае ☐ оба</div>'
     '<p class="note">Монтаж планируем в ночные окна по регламенту ТЦ. Маскот и модули можно делать параллельно с залом.</p>')

# 16 опыт
cs = ''.join(f'<div class="case">{im(f)}<b>{e(t)}</b><span>{e(d)}</span><em>hand-marketing.ru{u}</em></div>' for f, t, d, u, _ in ob.CASES)
page(head('Опыт · проекция, маппинг, датчики, ежедневный поток', 'Мы уже делали это для Самары') + f'<div class="cases">{cs}</div>')

# 17 выбор и контакты
ideas = ''.join(f'<div class="ig"><b>{e(g_)}</b>' + ''.join(f'<span>☐ {e(t)}</span>' for _, t, _ in items) + '</div>' for g_, items in ob.IDEAS)
page(head('Следующий шаг', 'Выберите, что считаем') +
     '<p class="lead">Отметьте идеи для сметы и подтвердите параметры экранов. Удобнее всего на странице: там выбор отправляется одной кнопкой.</p>'
     f'<div class="ideas">{ideas}</div>'
     f'<div class="contacts"><div class="qrb light"><div class="qr">{qr(LIVE + "#next")}</div><div><b>Отметить и отправить онлайн</b><span>hand-marketing.ru/for/oceanarium</span></div></div>'
     '<div class="who"><b>Александр Народецкий</b><span>Client Service Director</span><span>+7 985 999-87-83 · WhatsApp, Telegram</span><span>info@hand-marketing.ru · +7 495 580-75-37</span>'
     '<span>ООО «Хэнд-маркетинг» · 123022, Москва, ул. Рочдельская, 14А</span></div></div>'
     '<p class="note">Изображения маскота и зала концептуальные.</p>')

css = open(os.path.join(HERE, 'print.css'), encoding='utf8').read()
html = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Hand Marketing · Океанариум</title>
<link rel="stylesheet" href="{M}/fonts/oswald-onest.css"><link rel="stylesheet" href="{M}/fonts/jost-intertight.css"><link rel="stylesheet" href="{M}/fonts/plex.css">
<style>{css}</style></head><body>{"".join(pages)}</body></html>'''
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
open(os.path.join(HERE, 'out', 'print.html'), 'w', encoding='utf8').write(html)
print('ok', len(pages), 'листов')
