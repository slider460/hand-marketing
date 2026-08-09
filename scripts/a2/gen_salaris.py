#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/event/salaris/index.html: кейс «Презентация МФК „Саларис“
будущим арендаторам», 5 апреля 2018, арт-пространство «ФотоФактура».

Идея страницы. В апреле 2018 торгового центра ещё не было: стройка. А в зале
сидели двести ритейлеров, которым предстояло решать про аренду. Значит вечер
был не банкетом, а инструментом продажи площадей, и страница собрана вокруг
этого: сначала то, что показывали на экране, потом то, как был устроен зал.

Две механики, которых на сайте не было:
  • «Экран» — пять слайдов презентации, пересобранных вектором в фирменной
    палитре Саларис по видеозаписи вечера, а не заскриншоченных с проектора.
    Цифра на слайде набегает счётчиком, графика оживает при переключении.
  • «Зонт» — сувенир, который получал каждый на выходе. Вид сверху у зонта тот
    же, что у знака клиента: диск из клиньев. Поэтому зонт на финале
    раскрывается по скроллу и превращается в солнце Саларис.

Фактура: фотоотчёт вечера (15 кадров) и аftermovie media/salaris-event-fin180416.mp4.
Цифры сняты со слайдов на видеозаписи: 250 автобусов в час, мост в Neopolis на
5 500 человек в день, заселение соседних корпусов с сентября 2018.

Ассеты: mirror/images/salaris/ (scripts/salaris-assets.py).

НЕ публикуем: имена гостей и сотрудников клиента с бейджей и слайда «Команда
проекта», лица крупным планом в качестве иллюстраций к цифрам.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/salaris'
VIDEO = '/media/salaris-event-fin180416.mp4'   # источник: scripts/a2/video_map.json
URL = 'https://hand-marketing.ru/event/salaris/'

# ─── что было в брифе ───────────────────────────────────────────────────────
TASK = [
    ('Дать увидеть проект глазами собственника',
     'Не рендер в презентации, а вечер, после которого ритейлер понимает объект '
     'так же, как понимает его владелец.'),
    ('Найти площадку в центре Москвы у метро',
     'Ехать в Новую Москву на стройку арендаторов не позовёшь. Нужен был зал в '
     'городе, в шаговой доступности от метро.'),
    ('Собрать концепцию и наполнение вечера',
     'Сценарий, оформление, кейтеринг, развлекательная часть, сувениры и '
     'реализация всего этого на площадке.'),
    ('Оформить основную презентацию',
     'Ту самую, по которой выступали со сцены: инфраструктура, архитектура, '
     'статус стройки, планы открытия.'),
    ('Снять ролик об объекте',
     'Разработать техническое задание, снять и смонтировать видео о комплексе '
     'и его инфраструктуре. Его показывали в зале.'),
]

# ─── слайды: цифра, единица, тип графики, метка таба, заголовок, текст, зачем ─
# содержание снято со слайдов на видеозаписи вечера, графика пересобрана вектором
DECK = [
    ('310 000', 'м²', 'blocks', 'Состав', 'Что именно строится',
     'Гипермаркет, многозальный кинотеатр национальной сети, электроника и '
     'бытовая техника, мебельный гипермаркет, развлечения для всей семьи, '
     'одежда и обувь, видовые рестораны и кафе. Один из крупнейших проектов '
     'Новой Москвы.',
     'Состав комплекса и есть список категорий, которые арендатор примеряет на '
     'себя: с кем он окажется в одной галерее.'),
    ('250', 'автобусов в час', 'buses', 'Автобусы', 'Автобусная станция',
     'Пропускная способность станции: до 250 автобусов в час, включая '
     'маршруты до аэропорта Внуково. Станция встроена в комплекс, а не '
     'вынесена на соседнюю улицу.',
     'Для ритейлера автобусная станция это поток людей, который проходит '
     'через здание, даже если человек ехал совсем в другое место.'),
    ('5 500', 'человек в день', 'bridge', 'Мост', 'Пешеходный мост',
     'Соединение с деловым кварталом Neopolis по пешеходному мосту. '
     'Дополнительный трафик 5 500 человек в день.',
     'Офисный квартал рядом даёт то, чего не даёт спальный район: будни, обед '
     'и вечер после работы.'),
    ('3', 'вида транспорта в одной точке', 'metro', 'Метро', 'Транспортно-пересадочный узел',
     'Метро, автобусная станция и перехватывающий паркинг сходятся в одной '
     'точке. Это один из крупнейших транспортных узлов Москвы.',
     'Точка, мимо которой не проехать: сюда приезжают из области и '
     'пересаживаются в город.'),
    ('2018', 'заселение с сентября', 'homes', 'Жильё', 'Жильё вплотную к комплексу',
     'Перспективная жилая застройка вокруг МФК: ЖК «Саларьева Парк», город '
     'Московский, корпуса вдоль Киевского шоссе.',
     'Соседи въезжают раньше, чем открывается центр. К открытию у комплекса '
     'уже есть свой район.'),
]

# ─── вечер по шагам ─────────────────────────────────────────────────────────
# (время, слаг фото, заголовок, текст, alt, «широкая» ли строка)
EVENING = [
    ('Сбор', 'badges', 'Именной бейдж вместо списка',
     'Двести бейджей в фирменных цветах разложены на стойке заранее. Человек '
     'находит своё имя, и с этой секунды он не «гость мероприятия», а участник '
     'встречи, где его ждали.',
     'Ряды именных бейджей Саларис на стойке регистрации'),
    ('Велком-дринк', 'welcome', 'Первые двадцать минут',
     'Пока собирается зал, работает велком-дринк. Стойку собрали в фирменном '
     'жёлтом на фоне белого кирпича площадки, поэтому цвет знака клиента '
     'попадает в кадр раньше, чем начинается презентация.',
     'Жёлтая стойка велком-дринка с лимонадами на фоне белой кирпичной стены'),
    ('Официальная часть', 'hall-light', 'Зал, который заполнился',
     'За час до начала это ряды пустых стульев перед экраном. К выступлению '
     'свободных мест не осталось: пришли двести человек. Со сцены выступали '
     'команда проекта и консультанты по сдаче в аренду, CBRE и Knight Frank.',
     'Полный зал на официальной части, световая ферма над сценой'),
    ('Ролик', 'title', 'Кино про то, чего ещё нет',
     'Техническое задание, съёмка и монтаж наши. Комплекс на тот момент был на '
     'стадии строительства, поэтому будущее здание собирали графикой по '
     'существующей модели, а натуру снимали дроном и операторами.',
     'Титр ролика: презентация МФК «Саларис» для арендаторов, 5 апреля 2018'),
    ('Фуршет', 'nitro', 'Три станции',
     'После официальной части и до конца вечера работал фуршет. Помимо общей '
     'линии, гостей ждали три отдельные станции: крем-брюле, сорбет и оленина. '
     'Сорбет готовили при гостях на жидком азоте.',
     'Станция с жидким азотом: облако пара над оранжевыми графинами'),
    ('Фото 180°', 'photo180', 'Объёмный кадр за минуту',
     'Зона кругового фото: участник вставал в центр, установка снимала его со '
     'всех сторон, результат показывали тут же на экране и присылали на почту. '
     'Единственная точка вечера, где очередь была всё время.',
     'Зона фото 180 градусов: результат съёмки на экране рядом с площадкой'),
]

STATIONS = [
    ('Крем-брюле', 'Карамельная корочка, которую жгут при гостях'),
    ('Сорбет', 'Готовят на жидком азоте прямо на станции'),
    ('Оленина', 'Гастрономическая позиция для разговора у стойки'),
]

# ─── что осталось после вечера ──────────────────────────────────────────────
RESULT = [
    ('200', 'человек посетило мероприятие'),
    ('310 000', 'м² объекта, который они разбирали по слайдам'),
    ('3:15', 'минуты аftermovie, снятого и смонтированного нами'),
]


# ─── графика: веер лучей знака Саларис ──────────────────────────────────────
def fan(n=44, r0=30.0, r1=96.0, cx=100.0, cy=100.0, start=-96.0, span=352.0,
        wide=0.62, thin=0.05, opacity=None, cls=''):
    """Веер знака клиента: лепестки по кругу вырождаются в тонкие лучи.

    Форма снята с логотипа: сверху широкие лепестки, дальше по часовой они
    сужаются и к низу превращаются в иглы. Рисуем сами, потому что этот же
    веер нужен и в фоне, и на слайдах, и в зонте — каждый раз со своими
    пропорциями."""
    out = []
    for i in range(n):
        t = i / (n - 1)
        a = math.radians(start + span * t)
        half = math.radians((wide + (thin - wide) * t) * 360 / n * 1.6)
        length = r1 - (r1 - r0) * 0.10 * t
        p0 = (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        tip = (cx + length * math.cos(a), cy + length * math.sin(a))
        mid = r0 + (length - r0) * 0.45
        c1 = (cx + mid * math.cos(a - half), cy + mid * math.sin(a - half))
        c2 = (cx + mid * math.cos(a + half), cy + mid * math.sin(a + half))
        col = f'var(--sl-fan{i % 3})'
        op = f' opacity="{opacity}"' if opacity else ''
        out.append(
            f'<path d="M{p0[0]:.1f} {p0[1]:.1f}Q{c1[0]:.1f} {c1[1]:.1f} {tip[0]:.1f} '
            f'{tip[1]:.1f}Q{c2[0]:.1f} {c2[1]:.1f} {p0[0]:.1f} {p0[1]:.1f}Z" '
            f'fill="{col}"{op}/>')
    return (f'<svg class="sl-fan {cls}" viewBox="0 0 200 200" aria-hidden="true" '
            f'focusable="false">{"".join(out)}</svg>')


UMB_N = 16
UMB_R = 92.0


def umb_wedge(i, e, n=UMB_N, r=UMB_R):
    """Геометрия одного клина зонта при степени раскрытия e (0 сложен, 1 раскрыт).

    Считаем координаты, а не крутим готовый путь трансформом: у SVG-элементов
    точка вращения зависит от transform-box/transform-origin, и клинья начинают
    расходиться каждый вокруг своего угла. Здесь двусмысленности нет."""
    step = 2 * math.pi / n
    half = step / 2 * (0.34 + 0.66 * e)   # сложенный зонт ещё и уже
    ang = -math.pi / 2 + step * i * e
    rr = r * (0.62 + 0.38 * e)
    p1 = (rr * math.cos(ang - half), rr * math.sin(ang - half))
    p2 = (rr * math.cos(ang + half), rr * math.sin(ang + half))
    bulge = rr * 1.07
    b = (bulge * math.cos(ang), bulge * math.sin(ang))
    d = (f'M0 0L{p1[0]:.2f} {p1[1]:.2f}Q{b[0]:.2f} {b[1]:.2f} '
         f'{p2[0]:.2f} {p2[1]:.2f}Z')
    rib = (rr * math.cos(ang), rr * math.sin(ang))
    return d, rib


def umbrella():
    """Зонт сверху это диск из клиньев. Сложенный: все клинья в одном секторе.
    Раскрытый: расходятся по кругу и складываются в знак клиента."""
    cols = ['var(--sl-sun1)', 'var(--sl-sun2)', 'var(--sl-sun3)', 'var(--sl-indigo)']
    seg, ribs = [], []
    for i in range(UMB_N):
        # в разметку кладём наполовину раскрытое состояние: так зонт выглядит
        # осмысленно и без JS, и до того, как отработает первый расчёт
        d, rib = umb_wedge(i, 0.0)
        seg.append(f'<path class="sl-umb__w" data-i="{i}" d="{d}" fill="{cols[i % 4]}"/>')
        ribs.append(f'<line class="sl-umb__rib" data-i="{i}" x1="0" y1="0" '
                    f'x2="{rib[0]:.2f}" y2="{rib[1]:.2f}"/>')
    return (
      '<svg class="sl-umb" viewBox="-110 -110 220 220" role="img" '
      'aria-label="Зонт с логотипом МФК «Саларис», вид сверху: раскрываясь, '
      'клинья складываются в знак клиента">'
      f'{"".join(seg)}{"".join(ribs)}'
      '<circle class="sl-umb__cap" r="17"/>'
      '<circle class="sl-umb__pin" r="5"/></svg>')


# ─── слайды: векторная графика внутри экрана ────────────────────────────────
def slide_art(kind):
    """Графика слайда. viewBox широкий (320×110): экран презентации сам широкий,
    в квадратном холсте рисунок ужимался бы в узкую полосу посередине."""
    if kind == 'blocks':
        # силуэт комплекса: семь объёмов разной высоты
        h = [44, 72, 56, 94, 64, 82, 50]
        bars = ''.join(
            f'<rect class="sl-bar" style="--i:{i}" x="{18 + i * 42}" '
            f'y="{98 - v}" width="30" height="{v}" rx="4"/>' for i, v in enumerate(h))
        return ('<svg viewBox="0 0 320 110" aria-hidden="true">'
                f'{bars}<line class="sl-ground" x1="8" y1="100" x2="312" y2="100"/></svg>')
    if kind == 'buses':
        # десять автобусов: наглядная единица «столько проходит за час»
        b = ''.join(
            f'<g class="sl-bus" style="--i:{i}">'
            f'<rect x="{16 + (i % 5) * 60}" y="{16 + (i // 5) * 50}" width="46" '
            f'height="24" rx="6"/>'
            f'<rect class="sl-bus__win" x="{22 + (i % 5) * 60}" y="{21 + (i // 5) * 50}" '
            f'width="20" height="9" rx="3"/>'
            f'<circle cx="{26 + (i % 5) * 60}" cy="{42 + (i // 5) * 50}" r="4"/>'
            f'<circle cx="{52 + (i % 5) * 60}" cy="{42 + (i // 5) * 50}" r="4"/>'
            f'</g>' for i in range(10))
        return f'<svg viewBox="0 0 320 110" aria-hidden="true">{b}</svg>'
    if kind == 'bridge':
        # два берега и мост, по дуге идут люди
        x0, x1, ytop, ybase = 92.0, 228.0, 34.0, 60.0
        dots = []
        for i in range(9):
            t = (i + 0.5) / 9
            # точка на квадратичной кривой моста
            x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * 160 + t ** 2 * x1
            y = (1 - t) ** 2 * ybase + 2 * (1 - t) * t * ytop + t ** 2 * ybase
            dots.append(f'<circle class="sl-walk" style="--i:{i}" cx="{x:.1f}" '
                        f'cy="{y - 6:.1f}" r="4"/>')
        return ('<svg viewBox="0 0 320 110" aria-hidden="true">'
                '<rect class="sl-slab" x="8" y="60" width="84" height="42" rx="6"/>'
                '<rect class="sl-slab" x="228" y="60" width="84" height="42" rx="6"/>'
                f'<path class="sl-span" d="M{x0} {ybase}Q160 {ytop} {x1} {ybase}"/>'
                + ''.join(dots) + '</svg>')
    if kind == 'metro':
        # три вида транспорта, нанизанные на одну линию: метро, автобус, паркинг
        cy = 62.0
        xs = (76.0, 160.0, 244.0)
        glyphs = [
            f'<text class="sl-gl" x="{xs[0]}" y="{cy + 10}">М</text>',
            # автобус собираем фигурами: текстовой глиф тут читался бы хуже
            f'<g class="sl-gl-bus"><rect x="{xs[1] - 17}" y="{cy - 14}" width="34" '
            f'height="20" rx="5"/><rect class="sl-gl-bus__win" x="{xs[1] - 12}" '
            f'y="{cy - 10}" width="14" height="7" rx="2"/>'
            f'<circle cx="{xs[1] - 9}" cy="{cy + 9}" r="4"/>'
            f'<circle cx="{xs[1] + 9}" cy="{cy + 9}" r="4"/></g>',
            f'<text class="sl-gl" x="{xs[2]}" y="{cy + 10}">P</text>',
        ]
        stops = ''.join(
            f'<circle class="sl-stop" style="--i:{i}" cx="{x}" cy="{cy}" r="29"/>'
            for i, x in enumerate(xs))
        return ('<svg viewBox="0 0 320 110" aria-hidden="true">'
                f'<line class="sl-leg" x1="{xs[0]}" y1="{cy}" x2="{xs[2]}" y2="{cy}"/>'
                f'{stops}{"".join(glyphs)}</svg>')
    # homes: сетка корпусов, часть уже заселяется
    on = (1, 2, 5, 6, 7, 10, 11, 13)
    cells = ''.join(
        f'<rect class="sl-home" style="--i:{i}" data-on="{1 if i in on else 0}" '
        f'x="{16 + (i % 6) * 50}" y="{12 + (i // 6) * 34}" width="36" height="26" rx="4"/>'
        for i in range(18))
    return f'<svg viewBox="0 0 320 110" aria-hidden="true">{cells}</svg>'


PAGE_CSS = """<style id="sl-css">
:root{
 --sl-ink:#141232;--sl-ink2:#5b5878;
 --sl-indigo:#414495;--sl-indigo2:#5b5ec4;--sl-deep:#1b1a4a;
 --sl-sun1:#fdc431;--sl-sun2:#f59021;--sl-sun3:#e95127;
 --sl-screen:#a32bb0;--sl-lime:#d9e04a;
 --sl-paper:#faf6ee;--sl-paper2:#f2ebdd;--sl-line:rgba(20,18,50,.14);
 --sl-fan0:var(--sl-sun1);--sl-fan1:var(--sl-sun2);--sl-fan2:var(--sl-sun3);
 --sl-df:'Nunito',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --sl-bf:'Wix Madefor Text',system-ui,-apple-system,Segoe UI,Arial,sans-serif}
/* без scroll-behavior:smooth: на длинной странице плавная прокрутка перебивает
   быстрые скроллы и до низа страница доезжает не с первого раза */
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
.sl{font-family:var(--sl-bf);color:var(--sl-ink);background:var(--sl-paper);
 line-height:1.62;font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.sl *{box-sizing:border-box}
.sl img{max-width:100%;height:auto;display:block}
.sl a{color:inherit}
.sl h1,.sl h2,.sl h3{font-family:var(--sl-df);font-weight:900;line-height:1.03;
 letter-spacing:-.022em;margin:0;text-wrap:balance}
.sl p{text-wrap:pretty}
.sl-w{max-width:1220px;margin:0 auto;padding:0 clamp(18px,4vw,48px)}
.sl-sec{padding:clamp(54px,7.4vw,116px) 0;position:relative}
.sl-sec--alt{background:var(--sl-paper2)}
.sl-kick{font-weight:700;font-size:11.5px;letter-spacing:.17em;text-transform:uppercase;
 display:inline-flex;align-items:center;gap:10px;color:var(--sl-ink2)}
.sl-kick::before{content:"";width:24px;height:3px;border-radius:3px;
 background:linear-gradient(90deg,var(--sl-sun1),var(--sl-sun3))}
.sl-h2{font-size:clamp(27px,4.1vw,50px);margin:clamp(12px,1.7vw,18px) 0 0;max-width:19ch}
.sl-h3{font-size:clamp(19px,2.2vw,27px);font-weight:800;letter-spacing:-.015em}
.sl-lead{margin:clamp(12px,1.7vw,18px) 0 0;font-size:clamp(16px,1.3vw,19px);
 color:var(--sl-ink2);max-width:60ch}
.sl-r{opacity:0;transform:translateY(18px);transition:opacity .75s,transform .75s}
.sl-r.is-in{opacity:1;transform:none}
.no-js .sl-r{opacity:1;transform:none}

/* веер знака клиента: общая деталь для героя, слайдов и зонта */
.sl-fan{display:block;width:100%;height:auto}

/* ── герой ───────────────────────────────────────────────────────────────── */
.sl-hero{position:relative;background:var(--sl-deep);color:#fff;overflow:hidden;
 padding:clamp(96px,11vw,150px) 0 clamp(48px,6vw,86px)}
.sl-hero::after{content:"";position:absolute;inset:auto 0 0;height:36%;
 background:linear-gradient(180deg,transparent,rgba(0,0,0,.32))}
.sl-hero__fan{position:absolute;top:50%;left:100%;width:min(78vw,760px);
 transform:translate(-42%,-50%);opacity:.5;pointer-events:none}
.sl-hero .sl-w{position:relative;z-index:2}
.sl-hero__logo{width:clamp(78px,9vw,116px);height:auto;
 filter:drop-shadow(0 8px 26px rgba(0,0,0,.35))}
.sl-hero h1{font-size:clamp(34px,6.1vw,84px);margin:clamp(18px,2.4vw,30px) 0 0;
 max-width:15ch}
.sl-hero h1 em{font-style:normal;
 background:linear-gradient(96deg,var(--sl-sun1),var(--sl-sun3));
 -webkit-background-clip:text;background-clip:text;color:transparent}
.sl-hero__lead{margin:clamp(16px,2vw,24px) 0 0;font-size:clamp(16px,1.42vw,20px);
 color:#c9c7e8;max-width:56ch}
.sl-hero__meta{list-style:none;margin:clamp(22px,3vw,34px) 0 0;padding:0;
 display:flex;flex-wrap:wrap;gap:8px 10px}
.sl-hero__meta li{font-size:13.5px;font-weight:600;padding:.5em 1em;border-radius:999px;
 border:1px solid rgba(255,255,255,.24);color:#efeefb}
.sl-hero__shot{margin:clamp(30px,4vw,52px) 0 0;position:relative;border-radius:20px;
 overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.42)}
.sl-hero__shot img{width:100%;aspect-ratio:16/7;object-fit:cover}
.sl-hero__cap{position:absolute;left:0;right:0;bottom:0;padding:26px clamp(16px,2.4vw,28px) 16px;
 font-size:13px;color:#e7e5fa;
 background:linear-gradient(180deg,transparent,rgba(12,11,40,.82))}
.sl-nums{list-style:none;margin:clamp(26px,3.4vw,44px) 0 0;padding:0;display:grid;gap:clamp(14px,2vw,26px);
 grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.sl-nums b{display:block;font-family:var(--sl-df);font-weight:900;
 font-size:clamp(26px,3.4vw,42px);line-height:1;letter-spacing:-.03em;
 background:linear-gradient(96deg,var(--sl-sun1),var(--sl-sun3));
 -webkit-background-clip:text;background-clip:text;color:transparent}
.sl-nums span{display:block;margin-top:7px;font-size:13.5px;color:#b3b1d8;max-width:24ch}

/* ── задача ──────────────────────────────────────────────────────────────── */
.sl-task{display:grid;gap:clamp(26px,4vw,64px);grid-template-columns:minmax(0,1fr)}
@media(min-width:900px){.sl-task{grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr)}}
.sl-task__list{list-style:none;margin:0;padding:0;counter-reset:t}
.sl-task__list li{counter-increment:t;padding:clamp(16px,2vw,22px) 0;
 border-top:1px solid var(--sl-line);display:grid;gap:4px 18px;
 grid-template-columns:auto minmax(0,1fr)}
.sl-task__list li:last-child{border-bottom:1px solid var(--sl-line)}
.sl-task__list li::before{content:counter(t,decimal-leading-zero);grid-row:span 2;
 font-family:var(--sl-df);font-weight:900;font-size:15px;color:var(--sl-sun3);
 padding-top:3px}
.sl-task__list b{font-family:var(--sl-df);font-weight:800;font-size:clamp(17px,1.7vw,20px);
 letter-spacing:-.01em}
.sl-task__list p{margin:0;color:var(--sl-ink2);font-size:15.5px}
.sl-quote{margin:clamp(22px,3vw,32px) 0 0;padding:clamp(20px,2.6vw,30px);
 border-radius:18px;background:#fff;border:1px solid var(--sl-line);
 font-size:clamp(16px,1.4vw,19px);line-height:1.5}
.sl-quote b{font-family:var(--sl-df);font-weight:900}

/* ── экран: пересобранные слайды ─────────────────────────────────────────── */
.sl-deck{display:grid;gap:clamp(22px,3vw,44px);grid-template-columns:minmax(0,1fr);
 margin-top:clamp(28px,3.6vw,48px)}
@media(min-width:960px){.sl-deck{grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);
 align-items:start}}
.sl-screen{position:relative;border-radius:16px;overflow:hidden;color:#fff;
 background:radial-gradient(120% 130% at 12% 8%,#c445c8 0%,var(--sl-screen) 42%,#5b2ea8 100%);
 box-shadow:0 26px 60px rgba(60,20,90,.28)}
.sl-screen__fan{position:absolute;top:-24%;left:-16%;width:56%;opacity:.55;
 pointer-events:none}
/* высоту задаёт содержимое, а не фиксированная пропорция: при aspect-ratio
   графика упиралась в max-height и ужималась к центру вместо полной ширины */
.sl-screen__in{position:relative;z-index:1;display:flex;flex-direction:column;
 gap:clamp(10px,1.6vw,18px);padding:clamp(16px,2.5vw,30px);
 min-height:clamp(290px,32vw,430px)}
.sl-screen__num{font-family:var(--sl-df);font-weight:900;line-height:.92;
 font-size:clamp(38px,7.4vw,86px);letter-spacing:-.035em;
 text-shadow:0 6px 26px rgba(40,6,60,.35)}
.sl-screen__unit{display:block;font-family:var(--sl-bf);font-weight:600;
 font-size:clamp(12px,1.3vw,16px);letter-spacing:.02em;margin-top:8px;color:#ffe6b3}
.sl-screen__art{position:relative;margin-top:auto}
.sl-screen__art>svg{display:none;width:100%;height:auto}
.sl-screen__art>svg.is-on{display:block}
/* графика слайда: без этих правил svg рисуется чёрным по умолчанию */
.sl-bar{fill:#ffd76a;transform-box:fill-box;transform-origin:50% 100%}
.sl-ground{stroke:rgba(255,255,255,.42);stroke-width:1.6}
.sl-bus rect{fill:#ffd76a}
.sl-bus circle{fill:rgba(255,255,255,.7)}
.sl-bus .sl-bus__win{fill:var(--sl-screen)}
.sl-slab{fill:rgba(255,255,255,.2)}
.sl-span{fill:none;stroke:#ffd76a;stroke-width:5;stroke-linecap:round}
.sl-walk{fill:#fff}
.sl-leg{stroke:rgba(255,255,255,.45);stroke-width:3;stroke-linecap:round}
.sl-stn{fill:#ffd76a}
.sl-hub{fill:#fff}
.sl-stop{fill:#ffd76a}
.sl-gl{fill:var(--sl-screen);font-family:var(--sl-df);font-weight:900;font-size:30px;
 text-anchor:middle}
.sl-gl-bus rect{fill:var(--sl-screen)}
.sl-gl-bus circle{fill:var(--sl-screen)}
.sl-gl-bus .sl-gl-bus__win{fill:#ffd76a}
.sl-home{fill:rgba(255,255,255,.2)}
.sl-home[data-on="1"]{fill:#ffd76a}
@keyframes sl-grow{from{transform:scaleY(.04)}to{transform:none}}
@keyframes sl-pop{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
@keyframes sl-dash{from{stroke-dasharray:0 200}to{stroke-dasharray:200 0}}
.sl-art.is-on .sl-bar{animation:sl-grow .62s cubic-bezier(.2,.8,.3,1) both;
 animation-delay:calc(var(--i)*62ms)}
.sl-art.is-on .sl-bus,.sl-art.is-on .sl-home,.sl-art.is-on .sl-stn,
.sl-art.is-on .sl-walk,.sl-art.is-on .sl-stop{animation:sl-pop .5s ease-out both;
 animation-delay:calc(var(--i)*55ms)}
.sl-art.is-on .sl-span,.sl-art.is-on .sl-leg{animation:sl-dash .8s ease-out both}
.sl-screen__foot{display:flex;align-items:center;justify-content:space-between;gap:12px;
 font-size:11.5px;letter-spacing:.13em;text-transform:uppercase;color:#f6dcff;
 font-weight:700}
.sl-screen__foot img{width:34px;height:auto;opacity:.95}
.sl-tabs{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.sl-tabs button{font:700 13px/1 var(--sl-df);cursor:pointer;border-radius:999px;
 padding:.72em 1.05em;border:1.5px solid var(--sl-line);background:#fff;color:var(--sl-ink2);
 transition:background .25s,color .25s,border-color .25s,transform .25s}
.sl-tabs button:hover{transform:translateY(-2px);border-color:var(--sl-indigo2)}
.sl-tabs button[aria-selected=true]{background:var(--sl-indigo);border-color:var(--sl-indigo);
 color:#fff}
.sl-slide h3{margin:0}
.sl-slide p{margin:12px 0 0;color:var(--sl-ink2);font-size:15.8px}
.sl-slide__why{margin-top:16px;padding-top:16px;border-top:1px solid var(--sl-line);
 font-size:15px;color:var(--sl-ink)}
.sl-slide__why::before{content:"Зачем это ритейлеру";display:block;font:700 11px/1 var(--sl-df);
 letter-spacing:.15em;text-transform:uppercase;color:var(--sl-sun3);margin-bottom:8px}
.sl-note{margin:clamp(18px,2.4vw,26px) 0 0;font-size:13.5px;color:var(--sl-ink2)}

/* ── вечер по шагам ──────────────────────────────────────────────────────── */
.sl-step{display:grid;gap:clamp(18px,3vw,46px);align-items:center;
 grid-template-columns:minmax(0,1fr);padding:clamp(26px,3.4vw,44px) 0;
 border-top:1px solid var(--sl-line)}
@media(min-width:860px){
 .sl-step{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
 .sl-step--flip .sl-step__media{order:2}}
.sl-step__media{min-width:0}
.sl-step__media>img{width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:16px;
 background:#e8e2d6}
.sl-step__time{font:700 11.5px/1 var(--sl-df);letter-spacing:.16em;text-transform:uppercase;
 color:var(--sl-sun3)}
.sl-step h3{margin:10px 0 0}
.sl-step p{margin:12px 0 0;color:var(--sl-ink2);font-size:15.8px;max-width:52ch}
.sl-pair{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sl-pair figure{margin:0;border-radius:12px;overflow:hidden;position:relative;background:#e8e2d6}
.sl-pair img{width:100%;aspect-ratio:4/3;object-fit:cover}
.sl-pair figcaption{position:absolute;left:8px;bottom:8px;font:700 10.5px/1 var(--sl-df);
 letter-spacing:.1em;text-transform:uppercase;color:#fff;background:rgba(20,18,50,.7);
 padding:.5em .7em;border-radius:6px}
.sl-stations{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:8px}
.sl-stations li{display:grid;grid-template-columns:auto minmax(0,1fr);gap:12px;
 align-items:baseline;padding:11px 14px;border-radius:12px;background:#fff;
 border:1px solid var(--sl-line);font-size:15px}
.sl-stations b{font-family:var(--sl-df);font-weight:800}
.sl-stations span{color:var(--sl-ink2);font-size:14px}
/* фото 180°: карточка чуть поворачивается за курсором, намёк на объёмный кадр */
.sl-tilt{perspective:1100px}
.sl-tilt__in{transition:transform .35s cubic-bezier(.2,.7,.3,1);transform-style:preserve-3d;
 border-radius:16px;overflow:hidden;will-change:transform}

/* ── ролик ───────────────────────────────────────────────────────────────── */
.sl-film{background:var(--sl-deep);color:#fff}
.sl-film .sl-h2{color:#fff}
.sl-film .sl-lead{color:#bcb9e0}
.sl-film__box{margin-top:clamp(22px,3vw,38px);border-radius:18px;overflow:hidden;
 background:#000;box-shadow:0 26px 60px rgba(0,0,0,.45)}
.sl-film__box video{width:100%;height:auto;display:block;aspect-ratio:16/9;
 background:#000;object-fit:cover}

/* ── зонт и результат ────────────────────────────────────────────────────── */
.sl-out{background:linear-gradient(180deg,var(--sl-paper2),var(--sl-paper))}
.sl-out__grid{display:grid;gap:clamp(26px,4vw,60px);grid-template-columns:minmax(0,1fr);
 align-items:center}
@media(min-width:900px){.sl-out__grid{grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr)}}
.sl-umb{width:min(100%,420px);height:auto;margin:0 auto;display:block;
 filter:drop-shadow(0 22px 40px rgba(30,20,70,.22))}
.sl-umb__rib{stroke:rgba(255,255,255,.5);stroke-width:1.2}
.sl-umb__cap{fill:var(--sl-indigo)}
.sl-umb__pin{fill:#fff;opacity:.9}
.sl-umb__hint{text-align:center;font-size:13px;color:var(--sl-ink2);margin:14px 0 0}
.sl-res{list-style:none;margin:clamp(20px,2.6vw,30px) 0 0;padding:0;display:grid;
 gap:clamp(12px,1.8vw,18px);grid-template-columns:repeat(auto-fit,minmax(140px,1fr))}
.sl-res b{display:block;font-family:var(--sl-df);font-weight:900;
 font-size:clamp(24px,3.1vw,38px);line-height:1;letter-spacing:-.03em;color:var(--sl-indigo)}
.sl-res span{display:block;margin-top:6px;font-size:13.5px;color:var(--sl-ink2)}
.sl-kpi{margin:clamp(20px,2.6vw,30px) 0 0;padding:clamp(18px,2.4vw,26px);border-radius:16px;
 background:#fff;border:1px solid var(--sl-line)}
.sl-kpi b{font-family:var(--sl-df);font-weight:900}
.sl-more{margin:clamp(18px,2.2vw,24px) 0 0;font-size:15px;color:var(--sl-ink2)}
.sl-more a{color:var(--sl-indigo);font-weight:600;text-underline-offset:3px}

@media(prefers-reduced-motion:reduce){
 .sl *{animation:none!important;transition:none!important}
 .sl-r{opacity:1;transform:none}}
</style>"""


# ─── секции ─────────────────────────────────────────────────────────────────
def hero():
    meta = ''.join(f'<li>{t}</li>' for t in (
        '5 апреля 2018', 'Арт-пространство «ФотоФактура»', 'Москва',
        'Event под ключ', 'Съёмка и монтаж ролика'))
    nums = ''.join(f'<li><b>{k}</b><span>{v}</span></li>' for k, v in (
        ('200', 'гостей: ритейлеры, консультанты, пресса'),
        ('310&nbsp;000', 'м² комплекса, о котором шла речь'),
        ('5', 'слайдов, на которых держалась вся аргументация'),
        ('1', 'зонт каждому на выходе'),
    ))
    return (
      '<header class="sl-hero">'
      f'<div class="sl-hero__fan">{fan(n=40, opacity=".9")}</div>'
      '<div class="sl-w">'
      '<div class="sl-r">'
      f'<img class="sl-hero__logo" src="{IMG}/logo-salaris.png" width="760" height="632" '
      'alt="Знак МФК «Саларис»" fetchpriority="high">'
      '<p class="sl-kick" style="margin-top:18px">Event · Презентация объекта</p>'
      '<h1>Продать площади в центре, <em>которого ещё нет</em></h1>'
      '<p class="sl-hero__lead">В апреле 2018 года МФК «Саларис» был стройкой на '
      'Киевском шоссе. Двести ритейлеров нужно было собрать в одном зале и дать '
      'им увидеть проект так, как его видит собственник.</p>'
      f'<ul class="sl-hero__meta">{meta}</ul>'
      '</div>'
      '<div class="sl-hero__shot sl-r">'
      f'<img src="{IMG}/hall-full.jpg" width="1600" height="1067" loading="lazy" '
      'alt="Полный зал во время официальной части, на экране знак «Саларис»">'
      '<p class="sl-hero__cap">Официальная часть. Зал арт-пространства '
      '«ФотоФактура», 5 апреля 2018 года</p></div>'
      f'<ul class="sl-nums sl-r">{nums}</ul>'
      '</div></header>')


def task():
    lis = ''.join(f'<li><b>{k}</b><p>{v}</p></li>' for k, v in TASK)
    return (
      '<section class="sl-sec"><div class="sl-w">'
      '<div class="sl-task">'
      '<div class="sl-r">'
      '<p class="sl-kick">Задача</p>'
      '<h2 class="sl-h2">Вечер как инструмент, а не как банкет</h2>'
      '<p class="sl-lead">МФК «Саларис» это один из крупнейших проектов Новой '
      'Москвы: гипермаркет, многозальный кинотеатр, электроника, мебель, '
      'развлечения для всей семьи, одежда и обувь, видовые рестораны. '
      'Общая площадь 310 000 м².</p>'
      '<div class="sl-quote">Ритейлер решает не про красивое здание, а про свой '
      'будущий оборот в конкретной точке. Значит, вечер должен отвечать на '
      '<b>его</b> вопросы: откуда придут люди, сколько их и когда.</div>'
      '</div>'
      f'<div class="sl-r"><ul class="sl-task__list">{lis}</ul></div>'
      '</div></div></section>')


def deck():
    tabs = ''.join(
        f'<button type="button" role="tab" id="sl-tab-{i}" aria-controls="sl-pan-{i}" '
        f'aria-selected="{"true" if i == 0 else "false"}" data-i="{i}">'
        f'{i + 1:02d} · {tab}</button>'
        for i, (_, _, _, tab, _, _, _) in enumerate(DECK))
    # графику рисуем сразу в разметку: без JS виден первый слайд, дальше её меняет JS
    arts = ''.join(
        slide_art(kind).replace('<svg ', f'<svg class="sl-art{" is-on" if i == 0 else ""}" '
                                f'data-i="{i}" ', 1)
        for i, (_, _, kind, _, _, _, _) in enumerate(DECK))
    panels = ''.join(
        f'<div class="sl-slide" role="tabpanel" id="sl-pan-{i}" aria-labelledby="sl-tab-{i}" '
        f'data-i="{i}"{"" if i == 0 else " hidden"}>'
        f'<h3 class="sl-h3">{title}</h3><p>{text}</p>'
        f'<p class="sl-slide__why">{why}</p></div>'
        for i, (_, _, _, _, title, text, why) in enumerate(DECK))
    num0, unit0 = DECK[0][0], DECK[0][1]
    return (
      '<section class="sl-sec sl-sec--alt"><div class="sl-w">'
      '<div class="sl-r">'
      '<p class="sl-kick">Экран</p>'
      '<h2 class="sl-h2">Что видел зал</h2>'
      '<p class="sl-lead">Основная презентация держалась на пяти утверждениях про '
      'трафик. Мы пересобрали их заново, вектором в фирменной палитре клиента, '
      'по видеозаписи вечера.</p></div>'
      '<div class="sl-deck sl-r">'
      '<div>'
      '<div class="sl-screen" id="sl-screen">'
      f'<div class="sl-screen__fan">{fan(n=30, opacity=".75")}</div>'
      '<div class="sl-screen__in">'
      '<div class="sl-screen__foot"><span>МФК «Саларис»</span>'
      f'<img src="{IMG}/logo-salaris.png" width="760" height="632" loading="lazy" alt=""></div>'
      '<div>'
      f'<p class="sl-screen__num" id="sl-num" data-v="{num0}">{num0}'
      f'<span class="sl-screen__unit" id="sl-unit">{unit0}</span></p></div>'
      f'<div class="sl-screen__art" id="sl-art">{arts}</div>'
      '</div></div>'
      f'<div class="sl-tabs" role="tablist" aria-label="Слайды презентации">{tabs}</div>'
      '</div>'
      f'<div>{panels}'
      '<p class="sl-note">Слайды восстановлены по кадрам аftermovie: цифры и '
      'формулировки с экрана в зале, графика нарисована заново.</p>'
      '</div></div></div></section>')


def evening():
    rows = []
    for i, (time_, slug, title, text, alt) in enumerate(EVENING):
        if slug == 'hall-light':
            media = ('<div class="sl-pair">'
                     f'<figure><img src="{IMG}/hall-empty.jpg" width="1600" height="1067" '
                     'loading="lazy" alt="Пустые ряды стульев перед экраном за час до начала">'
                     '<figcaption>за час до</figcaption></figure>'
                     f'<figure><img src="{IMG}/hall-light.jpg" width="1400" height="934" '
                     f'loading="lazy" alt="{alt}"><figcaption>во время</figcaption></figure>'
                     '</div>')
        elif slug == 'photo180':
            media = ('<div class="sl-tilt" data-tilt><div class="sl-tilt__in">'
                     f'<img src="{IMG}/{slug}.jpg" width="1400" height="932" loading="lazy" '
                     f'alt="{alt}"></div></div>')
        else:
            media = (f'<img src="{IMG}/{slug}.jpg" width="1400" height="934" loading="lazy" '
                     f'alt="{alt}">')
        extra = ''
        if slug == 'nitro':
            extra = ('<ul class="sl-stations">' + ''.join(
                f'<li><b>{k}</b><span>{v}</span></li>' for k, v in STATIONS) + '</ul>')
        flip = ' sl-step--flip' if i % 2 else ''
        rows.append(
          f'<article class="sl-step sl-r{flip}">'
          f'<div class="sl-step__media">{media}</div>'
          f'<div><p class="sl-step__time">{time_}</p><h3 class="sl-h3">{title}</h3>'
          f'<p>{text}</p>{extra}</div></article>')
    return (
      '<section class="sl-sec"><div class="sl-w">'
      '<div class="sl-r">'
      '<p class="sl-kick">Зал</p>'
      '<h2 class="sl-h2">Как был устроен вечер</h2>'
      '<p class="sl-lead">Площадку искали в городе и у метро: везти арендаторов '
      'на стройку в Новую Москву было нельзя. Подошло арт-пространство '
      '«ФотоФактура»: белый кирпич, высокие окна, зал под двести человек.</p>'
      '</div>' + ''.join(rows) + '</div></section>')


def film():
    return (
      '<section class="sl-sec sl-film"><div class="sl-w">'
      '<div class="sl-r">'
      '<p class="sl-kick">Ролик</p>'
      '<h2 class="sl-h2">Три минуты, снятые на вечере</h2>'
      '<p class="sl-lead">Аftermovie презентации: регистрация, зал, официальная '
      'часть, фуршет и фото 180°. Съёмка и монтаж наши.</p></div>'
      '<div class="sl-film__box sl-r">'
      f'<video controls preload="none" playsinline poster="{IMG}/poster.jpg">'
      f'<source src="{VIDEO}" type="video/mp4">'
      'Ваш браузер не поддерживает видео.</video></div>'
      '</div></section>')


def out():
    res = ''.join(f'<li><b>{k}</b><span>{v}</span></li>' for k, v in RESULT)
    return (
      '<section class="sl-sec sl-out"><div class="sl-w">'
      '<div class="sl-out__grid">'
      '<div class="sl-r" id="sl-umb-box">'
      + umbrella() +
      '<p class="sl-umb__hint">Зонт сверху это тот же диск из клиньев, что и знак '
      '«Саларис». Прокрутите страницу, чтобы он раскрылся.</p>'
      '</div>'
      '<div class="sl-r">'
      '<p class="sl-kick">Результат</p>'
      '<h2 class="sl-h2">На выходе каждому вручали зонт</h2>'
      '<p class="sl-lead">Сувенир, который в Москве в апреле достают из машины на '
      'следующий же день. Логотип комплекса уезжал с гостем и работал дальше сам.</p>'
      f'<ul class="sl-res">{res}</ul>'
      '<div class="sl-kpi"><b>KPI проекта выполнены.</b> Мероприятие посетило 200 '
      'человек. Площадку, концепцию, оформление, кейтеринг, сувениры, презентацию '
      'и ролик об объекте агентство вело под ключ.</div>'
      '<p class="sl-more">Мероприятия под ключ это наша '
      '<a href="/event">услуга Event</a>. Рядом: '
      '<a href="/btl/salaris-xmas">акция «Ком подарков» в том же ТРЦ «Саларис»</a>, '
      '<a href="/event/riviera">презентация ТРЦ Ривьера арендаторам</a> и '
      '<a href="/video/salaris">видеоролики о комплексе</a>.</p>'
      '</div></div></div></section>')


HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Презентация МФК «Саларис» арендаторам, 2018 | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: презентация МФК «Саларис» будущим арендаторам, 5 апреля 2018 года, арт-пространство «ФотоФактура». 200 гостей, презентация о транспортном узле и трафике, фуршет с тремя станциями, зона фото 180°, ролик об объекте и зонт с логотипом на выходе.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Презентация МФК «Саларис» арендаторам, 2018 | Hand Marketing">
<meta property="og:description" content="Торгового центра ещё не было: стройка на Киевском шоссе. Двести ритейлеров собрали в зале в центре Москвы и показали объект так, как его видит собственник.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/hall-full.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/nunito-madefor.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


PAGE_JS = """<script>(function(){
 var DECK=%DECK%;
 // ── экран: переключение слайдов, цифра набегает счётчиком
 var tabs=document.querySelector('.sl-tabs'),
     numEl=document.getElementById('sl-num'),
     unitEl=document.getElementById('sl-unit'),
     art=document.getElementById('sl-art'),
     cur=0,timer=null;
 function digits(s){return s.replace(/[^0-9]/g,'');}
 function setNum(txt){
  var d=digits(txt);
  if(!d||d.length!==txt.replace(/\\s|\\u00a0/g,'').length){numEl.firstChild.nodeValue=txt;return;}
  // разряды разбиваем только там, где они были в исходной строке: иначе год
  // 2018 превращается в «2 018»
  var grp=/\\s|\\u00a0/.test(txt),to=parseInt(d,10),t0=performance.now(),dur=700;
  if(timer)cancelAnimationFrame(timer);
  (function step(now){
   var k=Math.min(1,(now-t0)/dur),p=1-Math.pow(1-k,3),v=Math.round(to*p),s=String(v);
   numEl.firstChild.nodeValue=grp?s.replace(/\\B(?=(\\d{3})+(?!\\d))/g,'\\u00a0'):s;
   if(k<1)timer=requestAnimationFrame(step);
  })(t0);
 }
 function show(i){
  if(i===cur||!DECK[i])return;cur=i;
  [].forEach.call(tabs.querySelectorAll('button'),function(b){
   b.setAttribute('aria-selected',String(+b.getAttribute('data-i')===i));});
  [].forEach.call(document.querySelectorAll('.sl-slide'),function(p){
   p.hidden=+p.getAttribute('data-i')!==i;});
  [].forEach.call(art.children,function(s){
   s.classList.toggle('is-on',+s.getAttribute('data-i')===i);});
  unitEl.textContent=DECK[i].unit;
  setNum(DECK[i].num);
 }
 if(tabs){
  tabs.addEventListener('click',function(e){
   var b=e.target.closest('button');if(b)show(+b.getAttribute('data-i'));});
  var btns=[].slice.call(tabs.querySelectorAll('button'));
  tabs.addEventListener('keydown',function(e){
   var i=btns.indexOf(document.activeElement);if(i<0)return;
   var d=(e.key==='ArrowRight'||e.key==='ArrowDown')?1:
         (e.key==='ArrowLeft'||e.key==='ArrowUp')?-1:0;
   if(!d)return;e.preventDefault();
   var n=(i+d+btns.length)%btns.length;btns[n].focus();btns[n].click();});
 }

 // ── зонт: раскрывается по мере прохода секции через экран
 var box=document.getElementById('sl-umb-box');
 if(box){
  var N=%UMB_N%,R=%UMB_R%,
      wedges=[].slice.call(box.querySelectorAll('.sl-umb__w')),
      ribs=[].slice.call(box.querySelectorAll('.sl-umb__rib')),
      last=-1,
      slow=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  // тот же расчёт, что в генераторе: координаты, а не трансформы
  function wedge(i,e){
   var step=2*Math.PI/N,half=step/2*(0.34+0.66*e),
       ang=-Math.PI/2+step*i*e,rr=R*(0.62+0.38*e),
       x1=rr*Math.cos(ang-half),y1=rr*Math.sin(ang-half),
       x2=rr*Math.cos(ang+half),y2=rr*Math.sin(ang+half),
       bx=rr*1.07*Math.cos(ang),by=rr*1.07*Math.sin(ang);
   return{d:'M0 0L'+x1.toFixed(2)+' '+y1.toFixed(2)+'Q'+bx.toFixed(2)+' '+by.toFixed(2)
          +' '+x2.toFixed(2)+' '+y2.toFixed(2)+'Z',
         rx:rr*Math.cos(ang),ry:rr*Math.sin(ang)};
  }
  function draw(k){
   var e=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
   if(Math.abs(e-last)<0.004)return;
   last=e;
   for(var i=0;i<wedges.length;i++){
    var w=wedge(i,e);
    wedges[i].setAttribute('d',w.d);
    if(ribs[i]){ribs[i].setAttribute('x2',w.rx.toFixed(2));
                ribs[i].setAttribute('y2',w.ry.toFixed(2));}
   }
  }
  function onScroll(){
   var r=box.getBoundingClientRect(),h=window.innerHeight||800;
   // 0 когда блок только вошёл снизу, 1 когда его середина у середины экрана
   var k=(h-r.top-r.height*0.18)/(h*0.72);
   draw(Math.max(0,Math.min(1,k)));
  }
  if(slow){draw(1);}
  else{addEventListener('scroll',onScroll,{passive:true});
       addEventListener('resize',onScroll);onScroll();}
 }

 // ── фото 180°: карточка чуть отклоняется за курсором
 [].forEach.call(document.querySelectorAll('[data-tilt]'),function(root){
  var inner=root.firstElementChild;
  if(!inner||!matchMedia('(hover:hover)').matches)return;
  root.addEventListener('pointermove',function(e){
   var r=root.getBoundingClientRect();
   var x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
   inner.style.transform='rotateY('+(x*9).toFixed(2)+'deg) rotateX('+(-y*7).toFixed(2)+'deg)';
  });
  root.addEventListener('pointerleave',function(){inner.style.transform='';});
 });

 // ── появление блоков: свип по скроллу, а не IntersectionObserver.
 // Наблюдатель отдаёт колбэк на следующем кадре, и при быстрой прокрутке до
 // низа и мгновенном возврате наверх нижние блоки остаются с opacity:0.
 // Свип считает геометрию синхронно, поэтому невидимого контента не остаётся.
 // Считаем синхронно, без rAF: под нагрузкой кадр приезжает с задержкой, флаг
 // троттлинга остаётся взведённым, и половина скроллов проходит мимо.
 var els=[].slice.call(document.querySelectorAll('.sl-r'));
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

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Event","item":"https://hand-marketing.ru/event/"},'
  '{"@type":"ListItem","position":3,"name":"Презентация МФК «Саларис» арендаторам",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    deck_js = [{'num': n, 'unit': u} for n, u, *_rest in DECK]
    js = (PAGE_JS.replace('%DECK%', json.dumps(deck_js, ensure_ascii=False))
          .replace('%UMB_N%', str(UMB_N)).replace('%UMB_R%', str(UMB_R)))
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="sl">{hero()}{task()}{deck()}{evening()}'
            f'{film()}{out()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'event', 'salaris')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
