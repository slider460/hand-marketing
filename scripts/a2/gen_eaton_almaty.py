#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/event/eaton/index.html: кейс «Партнёрская конференция Eaton»
(Алматы, Grand Hotel Tien Shan, 28 сентября 2016).

Что было раньше: остаток Tilda на три абзаца «Задачи → Решение → Результат».
Ни одной из двенадцати фотографий съёмки, ролик в мёртвом t868-попапе.

Откуда факты. Ничего не придумано, всё читается с первоисточников:
  • Eaton_Kazahstan_2016_print.pdf — гид участника, 8 полос 158×220 мм, наш
    макет от 25.09.2016. Оттуда: расписание трёх дней, программа дня
    конференции с семью выступлениями, данные по Алма-Ате (население
    1 716 779 на 01.04.2016, погода 27-30 сентября, +3 часа, курс 1 ₽ = 5,3 ₸,
    перелёт 4 ч 30 мин, 30 минут от аэропорта), отель (Богенбай батыра 115,
    14 км до аэропорта, 0,5 км до метро «Алмалы»), пять ресторанов.
  • eaton_badge_2.pdf — макет бейджа A6 от 23.09.2016.
  • media/eaton-almaty.mp4 (1:47) — заставка ролика дала дату и название
    «Партнерская конференция Eaton, 28 сентября 2016».
  • 12 кадров съёмки из общего каталога images/lib.
Дни 1 и 3 намеренно без дат: гид даёт погоду на 27-30 сентября, то есть часть
участников уезжала 30-го, и точный день вылета по документу не определяется.

Идея страницы. Кейс не про зал на один день, а про трое суток в чужой стране,
где у участника не должно остаться ни одного нерешённого вопроса. Отсюда
две механики на первоисточниках:

1. «Гид участника» (сигнатурная). Восемь полос лежат веером. Слева семь
   вопросов, которые возникают у человека в командировке. Клик по вопросу
   вытягивает нужную полосу вперёд и подсвечивает на ней точное место
   с ответом (прожектор box-shadow по прямоугольнику в долях страницы).
   Разметка снята с самих полос, ничего не дорисовано.
2. «Трое суток» — расписание из гида построчно, с двумя часовыми поясами
   в каждой строке (Алматы и Москва, разница +3), и «наша часть» у каждого
   шага. Медиа шага: где есть съёмка — кадр, где нет — плитка с фактом
   или сама полоса гида.

Фон и связка страницы — фирменная точечная решётка Eaton 2016: диагональная
сетка, радиус точки растёт по той же оси, что и градиент. Восстановлена
кодом по обложке гида и заставке ролика, canvas рисует её один раз
на ресайз (плюс разбег радиусов при появлении).

Палитра снята пипеткой с полос гида: синий заголовков #1478C7, оранжевый
лейблов #F68B11, малиновый имён и плашки контактов #B20D35, тёмно-синий
градиента #212C5E.

Шрифты Cuprum + PT Sans, локальные (/fonts/cuprum-ptsans.css). На сайте их
не было; IBM Plex сознательно не берём, он занят кейсом /eaton_online того же
клиента. Кадры, полосы гида и шрифты готовит scripts/eaton-almaty-assets.py.

Личные мобильные организаторов на 4-й полосе гида замазаны в ассет-скрипте.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/eaton-almaty'
VIDEO = '/media/eaton-almaty.mp4'
URL = 'https://hand-marketing.ru/event/eaton/'

# размеры готовых файлов — проставляем в width/height, чтобы вёрстка
# не прыгала, пока грузится картинка
SIZE = {
    'badge': (758, 1075), 'badges': (1600, 1060), 'guide-1': (1058, 1473),
    'guide-2': (1058, 1473), 'guide-3': (1058, 1473), 'guide-4': (1058, 1473),
    'guide-5': (1058, 1473), 'guide-6': (1058, 1473), 'guide-7': (1058, 1473),
    'guide-8': (1058, 1473), 'hall-empty': (1600, 1060), 'hall-full': (1600, 1060),
    'hotel-sign': (1600, 1060), 'kit': (1600, 1060), 'panel': (1600, 1060),
    'photozone': (1600, 2326), 'poster': (1280, 720), 'registration': (1600, 1060),
    'rollup': (1600, 1066), 'speaker-m': (1600, 1060),
    'v-desk': (1280, 552), 'v-handover': (1280, 552), 'v-networking': (1280, 552),
    'v-rollup-night': (1280, 552), 'v-slide': (1280, 552),
}


def img(name, alt, cls='', lazy=True, sizes=''):
    w, h = SIZE[name]
    l = ' loading="lazy" decoding="async"' if lazy else ''
    c = f' class="{cls}"' if cls else ''
    s = f' sizes="{sizes}"' if sizes else ''
    return (f'<img src="{IMG}/{name}.jpg" alt="{alt}" width="{w}" height="{h}"'
            f'{c}{l}{s}>')


# ─── герой: цифры из гида ───────────────────────────────────────────────────
FACTS = [
    ('4 ч 30 мин', 'перелёт из Москвы'),
    ('+3 часа', 'разница с Москвой'),
    ('14 км', 'от аэропорта до отеля'),
    ('7', 'выступлений за день'),
]

SCOPE = [
    'Подбор и бронь отеля под технический райдер',
    'Перелёты, трансферы, размещение, сопровождение VIP-групп',
    'Программа, режиссура и контроль тайминга',
    'Сцена, звук, свет, LED и проекция',
    'Застройка зала и брендирование пространства',
    'POSm: бейджи, ленты, раздатка, навигация',
    'Гид участника: разработка и печать',
    'Сопровождение все три дня, круглосуточно',
]

# ─── трое суток: (день, время Алматы, время Москвы, шаг, наша часть,
#                  вид медиа, файл/значение, подпись) ────────────────────────
TRIP = [
    ('День 1', '15:30-16:30', '12:30-13:30', 'Прилёт, получение багажа',
     'Бронь билетов для участников из разных стран, встреча в аэропорту.',
     'fact', ('4 ч 30 мин', 'столько занимает перелёт. Часы в Алматы переводятся вперёд на три'), ''),
    ('День 1', '16:30-17:00', '13:30-14:00', 'Трансфер',
     'Трансфер от аэропорта, персональное сопровождение VIP-групп.',
     'fact', ('14 км', 'от международного аэропорта Алматы до отеля, 30 минут в пути'), ''),
    ('День 1', '17:00-17:15', '14:00-14:15', 'Заселение',
     'Бронь номерного фонда и расселение по спискам.',
     'img', 'hotel-sign',
     'Гранд-отель «Тянь-Шань». Выбрали его, проанализировав отели Алматы по удалённости от аэропорта и инфраструктуре рядом.'),
    ('День 1', '18:30', '15:30', 'Обзорная экскурсия по зонам отеля',
     'Сопровождение групп по площадке.',
     'fact', ('0,5 км', 'до метро «Алмалы». Wi-Fi по всей территории отеля, СПА-центр «Bali» бесплатно'), ''),
    ('День 1', '19:00', '16:00', 'Team dinner',
     'Ресторан, меню и рассадка.',
     'guide', 'guide-7',
     'Полоса гида с ресторанами: кухня, адрес, график, средний чек, расстояние до отеля и время на такси.'),
    ('День 2', '9:00', '6:00', 'Сбор участников на регистрацию',
     'Стойка регистрации, бейджи на лентах, гид участника, приветственный кофе-брейк.',
     'img', 'registration', 'Стойка регистрации: бейджи на лентах и раздатка.'),
    ('День 2', '10:00', '7:00', 'Конференция',
     'Сцена, звук, свет, проекция, застройка зала и контроль тайминга.',
     'img', 'hall-full', 'Зал во время доклада. Семь выступлений, два перерыва.'),
    ('День 2', '14:30', '11:30', 'Обед и завершение мероприятия',
     'Кейтеринг и тайминг, чтобы никто не опоздал на обратный рейс.',
     'img', 'v-networking', 'Общение в перерыве, кадр из ролика.'),
    ('День 3', '13:00', '10:00', 'Трансфер в аэропорт Алматы',
     'Выезд группами под рейсы.',
     'guide', 'guide-8', 'Задняя обложка гида: «Желаем приятной и продуктивной поездки!»'),
]

# ─── гид: полосы веером ─────────────────────────────────────────────────────
GUIDE = [
    ('guide-1', 'Обложка'), ('guide-2', 'Разворот'), ('guide-3', 'Алма-Ата'),
    ('guide-4', 'Расписание'), ('guide-5', 'День конференции'), ('guide-6', 'Отель'),
    ('guide-7', 'Рестораны'), ('guide-8', 'Финал'),
]

# вопрос → (индекс полосы, прямоугольник ответа в долях полосы, ответ)
QUESTIONS = [
    ('Сколько лететь?', 2, (0.113, 0.475, 0.575, 0.030),
     '4 часа 30 минут из Москвы. И часы вперёд на три.'),
    ('Что надеть?', 2, (0.113, 0.348, 0.575, 0.070),
     'От +5 до +21. Прогноз в гиде на все четыре дня, с 27 по 30 сентября.'),
    ('Сколько это в тенге?', 2, (0.113, 0.446, 0.575, 0.030),
     '1 рубль равен 5,3 тенге. Ужин на 1500 ₽ это примерно 7 950 ₸.'),
    ('Во сколько мой доклад?', 4, (0.100, 0.285, 0.790, 0.560),
     'Семь выступлений с 9:00 до 15:30, с именами, должностями и темами.'),
    ('Где я живу?', 5, (0.500, 0.395, 0.410, 0.110),
     'Grand Hotel Tien Shan, улица Богенбай батыра, 115. До аэропорта 14 км, до метро «Алмалы» 0,5 км.'),
    ('Куда пойти вечером?', 6, (0.065, 0.642, 0.860, 0.280),
     'Пять ресторанов: кухня, средний чек и время на такси, от 5 до 9 минут от отеля.'),
    ('Кому звонить, если что-то не так?', 3, (0.110, 0.655, 0.790, 0.255),
     'Два номера Hand Marketing на любой вопрос во время пребывания в Алматы. Здесь они замазаны: это личные мобильные.'),
]

# ─── программа дня: (минуты, время, имя, должность, тема) ───────────────────
# «имя» пустое у служебных блоков — они рисуются приглушённо
PROGRAM = [
    (60, '9:00 - 10:00', '', '', 'Сбор и регистрация участников, приветственный кофе-брейк'),
    (20, '10:00 - 10:20', 'Татьяна Фантаева',
     'Генеральный директор Eaton в России и Казахстане', 'Приветственная речь'),
    (40, '10:20 - 11:00', 'Виктор Новиков',
     'Директор по продажам канала «Компоненты»', '«О канале сбыта Компоненты»'),
    (20, '11:00 - 11:20', 'Василий Мун',
     'Sales-инженер, развитие бизнеса Eaton в линейках PD и PQ', '«Eaton в Казахстане»'),
    (40, '11:20 - 12:00', 'Олег Сероштан',
     'Директор по продажам канала «Проекты»', '«Проектный бизнес»'),
    (30, '12:00 - 12:30', 'Азамат Мазабеков',
     'Sales-инженер, проектные продажи в каналах PD и PQ', '«Проектный бизнес в Казахстане»'),
    (30, '12:30 - 13:00', '', '', 'Кофе-брейк'),
    (20, '13:00 - 13:20', 'Сергей Игнатенко',
     'Технический специалист по продуктам каналов PD и PQ',
     '«Оборудование Eaton направления качественное электропитание»'),
    (70, '13:20 - 14:30', 'Максим Рубаненко',
     'Руководитель направления по продажам IT Channel',
     '«Партнёрская программа: как заработать с Eaton»'),
    (60, '14:30 - 15:30', '', '', 'Обед и завершение мероприятия'),
]

# ─── застройка: (файл, подпись) ─────────────────────────────────────────────
BUILD = [
    ('hall-empty', 'Зал до участников: экран, ролл-ап, стойка регистрации.'),
    ('rollup', 'Ролл-ап про инженерную инфраструктуру ЦОД, крупный план печати.'),
    ('v-rollup-night', 'Второй ролл-ап: «Больше возможностей для Вашего бизнеса».'),
    ('v-desk', 'Гости у бренд-волла и стойки регистрации.'),
    ('photozone|top', 'Бренд-волл: фотозона с логотипами Eaton.'),
    ('panel', 'Выступление у экрана и ролл-апа.'),
    ('speaker-m', 'Доклад на фоне ролл-апа.'),
    ('v-slide', 'Проекция: слайды докладов на экране в зале.'),
]

RESULT = [
    ('Ни одного сбоя', 'в расписании трёх дней и в логистике'),
    ('7 выступлений', 'уложились в тайминг с 9:00 до 15:30, с двумя перерывами'),
    ('3 дня', 'под ключ: от брони отеля до посадки на обратный рейс'),
]


def hero():
    facts = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in FACTS)
    return (
      '<section class="ea-hero">'
      '<canvas class="ea-hero__cv" id="ea-cv" aria-hidden="true"></canvas>'
      '<div class="ea-hero__in ea-w">'
      '<p class="ea-hero__kick">Event <i>·</i> MICE <i>·</i> Казахстан</p>'
      '<h1 class="ea-hero__h1">Партнёрская<br>конференция Eaton</h1>'
      '<p class="ea-hero__sub">Алматы <i>·</i> Grand Hotel Tien Shan <i>·</i> 28 сентября 2016</p>'
      f'<ul class="ea-hero__facts">{facts}</ul>'
      '</div></section>')


def task():
    scope = ''.join(f'<li>{s}</li>' for s in SCOPE)
    return (
      '<section class="ea-sec ea-task"><div class="ea-w ea-task__grid">'
      '<div class="ea-r">'
      '<p class="ea-kick">Задача</p>'
      '<h2 class="ea-h2">Конференция, до которой ещё надо долететь</h2>'
      '<p class="ea-lead">Eaton собирал партнёров в Алматы. Мероприятие в другой '
      'стране это не только зал и сцена: участника нужно довезти, поселить, '
      'накормить и ни разу не оставить без ответа на вопрос. Мы взяли на себя '
      'всё, кроме содержания докладов.</p>'
      '<p class="ea-note">Eaton, американская корпорация, основана в 1911 году: '
      'электротехническое и гидравлическое оборудование, компоненты для '
      'авиационной промышленности. Представлена более чем в 160 странах.</p>'
      '</div>'
      f'<div class="ea-r ea-scope"><h3>Что было на нас</h3><ul>{scope}</ul></div>'
      '</div></section>')


def trip():
    rows, day = [], None
    for d, ta, tm, title, our, kind, media, cap in TRIP:
        if d != day:
            day = d
            rows.append(f'<li class="ea-day"><span>{d}</span></li>')
        if kind == 'fact':
            num, txt = media
            art = (f'<div class="ea-tile"><b>{num}</b><span>{txt}</span></div>')
        elif kind == 'guide':
            art = (f'<figure class="ea-shot ea-shot--pg">{img(media, cap)}'
                   f'<figcaption>{cap}</figcaption></figure>')
        else:
            art = (f'<figure class="ea-shot">{img(media, cap)}'
                   f'<figcaption>{cap}</figcaption></figure>')
        rows.append(
          '<li class="ea-step ea-r">'
          f'<div class="ea-step__t"><b>{ta}</b><span>{tm} в Москве</span></div>'
          f'<div class="ea-step__b"><h3>{title}</h3>'
          f'<p class="ea-step__our"><i>Наша часть.</i> {our}</p>{art}</div>'
          '</li>')
    return (
      '<section class="ea-sec ea-trip" id="trip"><div class="ea-w">'
      '<p class="ea-kick">Маршрут</p>'
      '<h2 class="ea-h2">Трое суток одного участника</h2>'
      '<p class="ea-lead ea-lead--w">Расписание не сочинено для кейса: это то, что '
      'было напечатано в гиде и роздано на входе. Крупно время Алматы, под ним '
      'московское, потому что летели в основном из Москвы.</p>'
      f'<ol class="ea-steps">{"".join(rows)}</ol>'
      '</div></section>')


def guide():
    qs = ''.join(
      f'<button class="ea-q" type="button" role="tab" data-i="{i}"'
      f' aria-selected="{"true" if i == 0 else "false"}">{q}</button>'
      for i, (q, _p, _b, _a) in enumerate(QUESTIONS))
    ans = ''.join(
      f'<p class="ea-ans" data-i="{i}"{"" if i == 0 else " hidden"}>{a}</p>'
      for i, (_q, _p, _b, a) in enumerate(QUESTIONS))
    # веер: угол и подъём считаем здесь, чтобы в CSS не понадобился abs()
    n = len(GUIDE)
    pages = []
    for i, (name, label) in enumerate(GUIDE):
        off = i - (n - 1) / 2
        ang = round(off * 5.0, 2)
        up = round(abs(off) * abs(off) * 1.5, 1)
        pages.append(
          f'<div class="ea-page" data-p="{i}" style="--a:{ang}deg;--u:{up}px;--z:{i}">'
          f'{img(name, "Гид участника, полоса: " + label)}'
          '<span class="ea-hl" hidden></span>'
          f'<span class="ea-page__lb">{label}</span></div>')
    return (
      '<section class="ea-sec ea-guide" id="guide"><div class="ea-w">'
      '<p class="ea-kick">Печать</p>'
      '<h2 class="ea-h2">Гид участника: ответ раньше вопроса</h2>'
      '<p class="ea-lead ea-lead--w">Восемь полос формата 158×220 мм, отпечатанных '
      'к вылету. В них собрано всё, что человек спрашивает в чужом городе. '
      'Выберите вопрос, гид покажет, где ответ.</p>'
      '<div class="ea-guide__grid">'
      f'<div class="ea-qs" role="tablist" aria-label="Вопросы участника">{qs}'
      f'<div class="ea-ans__box">{ans}</div></div>'
      f'<div class="ea-fan" id="ea-fan">{"".join(pages)}</div>'
      '</div>'
      '<p class="ea-fine">Личные мобильные организаторов на полосе с контактами '
      'закрыты: в печати они были, на сайте им не место.</p>'
      '</div></section>')


def program():
    total = sum(m for m, *_ in PROGRAM)
    bars, rows = [], []
    for i, (mins, time, name, role, topic) in enumerate(PROGRAM):
        kind = 'talk' if name else 'break'
        bars.append(
          f'<button class="ea-bar ea-bar--{kind}" type="button" data-i="{i}"'
          f' style="flex-grow:{mins}" aria-label="{time}, {topic}">'
          f'<span class="ea-bar__m">{mins}</span></button>')
        who = (f'<b>{name}</b><i>{role}</i>' if name else '')
        rows.append(
          f'<li class="ea-slot ea-slot--{kind}" data-i="{i}">'
          f'<span class="ea-slot__t">{time}</span>'
          f'<span class="ea-slot__w">{who}<span class="ea-slot__topic">{topic}</span></span>'
          f'<span class="ea-slot__m">{mins} мин</span></li>')
    return (
      '<section class="ea-sec ea-prog" id="program"><div class="ea-w">'
      '<p class="ea-kick">День 2</p>'
      '<h2 class="ea-h2">28 сентября, с 9:00 до 15:30</h2>'
      '<p class="ea-lead ea-lead--w">Шесть с половиной часов, семь выступлений '
      'и два перерыва. Полоса ниже нарисована по реальной длительности блоков: '
      'видно, что доклад о партнёрской программе занял больше часа, '
      'а приветственная речь двадцать минут.</p>'
      f'<div class="ea-track" role="group" aria-label="Хронометраж дня">{"".join(bars)}</div>'
      '<div class="ea-track__ends"><span>9:00</span>'
      f'<span>{total} минут</span><span>15:30</span></div>'
      f'<ol class="ea-slots">{"".join(rows)}</ol>'
      '</div></section>')


def build():
    cells = []
    for n, c in BUILD:
        # «имя|top» — вертикальный кадр, в сетке 16/11 его надо ровнять по верху,
        # иначе object-fit:cover срезает головы
        top = n.endswith('|top')
        n = n.split('|')[0]
        cls = 'ea-cell ea-cell--top ea-r' if top else 'ea-cell ea-r'
        cells.append(f'<figure class="{cls}">{img(n, c)}'
                     f'<figcaption>{c}</figcaption></figure>')
    cells = ''.join(cells)
    return (
      '<section class="ea-sec ea-build" id="build"><div class="ea-w">'
      '<p class="ea-kick">Площадка</p>'
      '<h2 class="ea-h2">Что мы привезли в зал</h2>'
      '<p class="ea-lead ea-lead--w">Конференц-зал отеля превращается в площадку '
      'Eaton: ролл-апы, экран и проекция, стойка регистрации, бренд-волл '
      'и навигация. Всё по глобальным гайдлайнам клиента.</p>'
      f'<div class="ea-grid">{cells}</div>'
      '</div></section>')


def kit():
    return (
      '<section class="ea-sec ea-kit" id="kit"><div class="ea-w">'
      '<p class="ea-kick">Комплект участника</p>'
      '<h2 class="ea-h2">Бейдж, лента и раздатка</h2>'
      '<div class="ea-kit__grid">'
      '<div class="ea-r ea-kit__badge">'
      f'{img("badge", "Макет бейджа участника, A6")}'
      '<p class="ea-cap">Макет бейджа, 74×105 мм. Печатался под каждого '
      'участника, имя и компания подставлялись в поле.</p></div>'
      '<div class="ea-r ea-kit__side">'
      '<p class="ea-lead">Бейдж и обложка гида собраны на одной решётке: это '
      'фирменный паттерн Eaton 2016 года. Диагональная сетка, точка тем крупнее, '
      'чем светлее фон под ней. Мы разобрали его и пересобрали кодом, справа '
      'он живой и перерисовывается под размер окна.</p>'
      '<canvas class="ea-kit__cv" id="ea-cv2" aria-hidden="true"></canvas>'
      '</div>'
      f'<figure class="ea-cell ea-r">{img("badges", "Бейджи на лентах на стойке регистрации")}'
      '<figcaption>Бейджи на синих лентах, разложенные к сбору участников.</figcaption></figure>'
      f'<figure class="ea-cell ea-r">{img("kit", "Каталог, блокнот, ручка и брелок Eaton")}'
      '<figcaption>Раздатка: каталог электротехнической продукции, блокнот, '
      'ручка и брелок.</figcaption></figure>'
      f'<figure class="ea-cell ea-r">{img("v-handover", "Выдача бейджа участнику")}'
      '<figcaption>Выдача комплекта на входе.</figcaption></figure>'
      '</div></div></section>')


def film():
    return (
      '<section class="ea-sec ea-film"><div class="ea-w ea-film__grid">'
      '<div class="ea-r">'
      '<p class="ea-kick">Ролик</p>'
      '<h2 class="ea-h2">Как это выглядело</h2>'
      '<p class="ea-lead">Отчётный ролик конференции: регистрация, застройка, '
      'доклады, кофе-брейк и общение в фойе. Съёмка и монтаж наши.</p></div>'
      '<div class="ea-film__box ea-r">'
      f'<video controls preload="none" playsinline poster="{IMG}/poster.jpg">'
      f'<source src="{VIDEO}" type="video/mp4">'
      'Ваш браузер не поддерживает видео.</video></div>'
      '</div></section>')


def out():
    res = ''.join(f'<li><b>{k}</b><span>{v}</span></li>' for k, v in RESULT)
    return (
      '<section class="ea-sec ea-out"><div class="ea-w">'
      '<p class="ea-kick">Результат</p>'
      '<h2 class="ea-h2">Конференция прошла без накладок</h2>'
      '<p class="ea-lead ea-lead--w">Расписание трёх дней выдержано, логистика '
      'сработала без сбоев. Уровень мероприятия отметили и сотрудники Eaton, '
      'и приглашённые участники.</p>'
      f'<ul class="ea-res">{res}</ul>'
      '<p class="ea-sign">Желаем приятной и продуктивной поездки!</p>'
      '<p class="ea-more">Другие проекты с этим клиентом: '
      '<a href="/eaton_online">онлайн-трансляция Eaton</a>, '
      '<a href="/video/patriot">ролик УАЗ Патриот и Eaton</a>.</p>'
      '</div></section>')


PAGE_CSS = """<style id="ea-css">
.ea{--navy:#0B1B44;--deep:#212C5E;--blue:#1478C7;--cyan:#6ACEEE;--amber:#F68B11;
 --crimson:#B20D35;--paper:#F2F5F9;--ink:#111826;--mute:#66717F;--line:#DDE4EC;
 font-family:'PT Sans',-apple-system,Arial,sans-serif;color:var(--ink);
 background:#fff;overflow-x:clip}
.ea *,.ea *::before,.ea *::after{box-sizing:border-box}
.ea img,.ea video,.ea canvas{max-width:100%;display:block}
.ea h1,.ea h2,.ea h3,.ea .ea-kick,.ea .ea-tile b,.ea .ea-hero__facts b,.ea .ea-res b,
.ea .ea-slot__t,.ea .ea-step__t b,.ea .ea-q,.ea .ea-sign,.ea .ea-track__ends
 {font-family:'Cuprum','PT Sans',Arial,sans-serif}
.ea-w{width:min(1180px,100% - 48px);margin-inline:auto}
.ea-sec{padding:clamp(56px,7vw,104px) 0}
.ea-kick{margin:0 0 14px;font-size:13px;letter-spacing:.22em;text-transform:uppercase;
 font-weight:700;color:var(--blue)}
.ea-h2{margin:0 0 18px;font-weight:700;line-height:1.06;letter-spacing:-.01em;
 font-size:clamp(28px,4.4vw,52px)}
.ea-lead{margin:0 0 8px;font-size:clamp(16px,1.35vw,19px);line-height:1.62;color:#39414F}
.ea-lead--w{max-width:64ch}
.ea-note{margin:22px 0 0;padding-top:18px;border-top:1px solid var(--line);
 font-size:15px;line-height:1.6;color:var(--mute)}
.ea-fine{margin:26px 0 0;font-size:13.5px;line-height:1.6;color:var(--mute)}
.ea-r{opacity:0;transform:translateY(20px);transition:opacity .6s ease,transform .6s ease}
.ea-r.is-in,.no-js .ea-r{opacity:1;transform:none}

/* ── ГЕРОЙ ─────────────────────────────────────────────────────────────── */
.ea-hero{position:relative;isolation:isolate;background:var(--navy);color:#fff;
 min-height:clamp(430px,88svh,820px);display:flex;align-items:flex-end;
 padding:clamp(88px,12vh,140px) 0 clamp(34px,5vh,64px);overflow:hidden}
.ea-hero__cv{position:absolute;inset:0;width:100%;height:100%;z-index:-1}
.ea-hero__in{position:relative}
.ea-hero__kick{margin:0 0 16px;font-size:12.5px;letter-spacing:.26em;text-transform:uppercase;
 font-weight:700;color:#B7DDF6}
.ea-hero__kick i,.ea-hero__sub i{font-style:normal;opacity:.55;padding:0 4px}
.ea-hero__h1{margin:0;font-weight:700;line-height:.96;letter-spacing:-.015em;
 font-size:clamp(38px,7.4vw,104px);text-shadow:0 2px 30px rgba(4,18,52,.35)}
.ea-hero__sub{margin:18px 0 0;font-size:clamp(15px,1.6vw,20px);color:#DCEEFB}
.ea-hero__facts{list-style:none;margin:clamp(26px,4vh,48px) 0 0;padding:0;display:grid;
 gap:14px 26px;grid-template-columns:repeat(4,minmax(0,1fr));max-width:900px}
.ea-hero__facts li{border-top:2px solid rgba(255,255,255,.32);padding-top:10px}
.ea-hero__facts b{display:block;font-size:clamp(20px,2.5vw,30px);font-weight:700;line-height:1.1}
.ea-hero__facts span{display:block;margin-top:3px;font-size:13px;line-height:1.35;color:#C7E3F7}

/* ── ЗАДАЧА ────────────────────────────────────────────────────────────── */
.ea-task{background:var(--paper)}
.ea-task__grid{display:grid;gap:clamp(28px,4vw,64px);grid-template-columns:1.35fr 1fr;
 align-items:start}
.ea-scope{background:#fff;border:1px solid var(--line);border-radius:4px;
 padding:clamp(22px,2.4vw,32px)}
.ea-scope h3{margin:0 0 16px;font-size:19px;font-weight:700}
.ea-scope ul{list-style:none;margin:0;padding:0}
.ea-scope li{position:relative;padding:9px 0 9px 26px;font-size:15px;line-height:1.5;
 border-top:1px solid var(--line)}
.ea-scope li:first-child{border-top:0}
.ea-scope li::before{content:"";position:absolute;left:4px;top:17px;width:8px;height:8px;
 border-radius:50%;background:var(--blue)}

/* ── ТРОЕ СУТОК ────────────────────────────────────────────────────────── */
.ea-steps{list-style:none;margin:clamp(30px,4vw,52px) 0 0;padding:0;position:relative}
.ea-steps::before{content:"";position:absolute;left:7px;top:6px;bottom:6px;width:2px;
 background:linear-gradient(180deg,var(--blue),#CBD7E4)}
.ea-day{position:relative;padding:26px 0 12px 40px;font-family:'Cuprum','PT Sans',Arial,sans-serif;
 font-size:13px;letter-spacing:.2em;text-transform:uppercase;font-weight:700;color:var(--crimson)}
.ea-day::before{content:"";position:absolute;left:0;top:29px;width:16px;height:16px;
 border-radius:50%;background:var(--crimson);box-shadow:0 0 0 5px #fff}
.ea-step{position:relative;display:grid;grid-template-columns:150px minmax(0,1fr);
 gap:clamp(16px,2.4vw,40px);padding:0 0 30px 40px}
.ea-step::before{content:"";position:absolute;left:3px;top:7px;width:10px;height:10px;
 border-radius:50%;background:var(--blue);box-shadow:0 0 0 5px #fff}
.ea-step__t b{display:block;font-size:clamp(20px,2.1vw,27px);font-weight:700;line-height:1.1;
 color:var(--navy)}
.ea-step__t span{display:block;margin-top:3px;font-size:12.5px;color:var(--mute)}
.ea-step__b h3{margin:0 0 8px;font-size:clamp(18px,1.9vw,23px);font-weight:700;line-height:1.2}
.ea-step__our{margin:0;font-size:15px;line-height:1.6;color:#39414F}
.ea-step__our i{font-style:normal;font-weight:700;color:var(--amber)}
.ea-shot{margin:16px 0 0}
.ea-shot img{width:100%;max-width:640px;height:auto;border-radius:3px;aspect-ratio:16/10;
 object-fit:cover}
.ea-shot--pg img{aspect-ratio:auto;max-width:290px;border:1px solid var(--line);
 box-shadow:0 14px 34px rgba(11,27,68,.14)}
.ea-shot figcaption,.ea-cap{margin-top:9px;font-size:13.5px;line-height:1.5;color:var(--mute);
 max-width:56ch}
.ea-tile{margin:16px 0 0;background:var(--navy);color:#fff;border-radius:3px;
 padding:clamp(18px,2vw,26px);max-width:430px}
.ea-tile b{display:block;font-size:clamp(28px,3.6vw,42px);font-weight:700;line-height:1;
 color:var(--cyan)}
.ea-tile span{display:block;margin-top:8px;font-size:14px;line-height:1.5;color:#CFE3F6}

/* ── ГИД ───────────────────────────────────────────────────────────────── */
.ea-guide{background:var(--navy);color:#fff}
.ea-guide .ea-kick{color:var(--cyan)}
.ea-guide .ea-lead{color:#CBDCEE}
.ea-guide .ea-fine{color:#8FA6C0}
.ea-guide__grid{display:grid;gap:clamp(26px,3vw,52px);grid-template-columns:minmax(0,.82fr) minmax(0,1.18fr);
 align-items:center;margin-top:clamp(28px,3.4vw,48px)}
.ea-qs{display:flex;flex-direction:column;gap:8px;min-width:0}
.ea-q{appearance:none;text-align:left;cursor:pointer;font-size:clamp(15px,1.5vw,18px);
 font-weight:700;line-height:1.3;color:#DCEBF9;background:rgba(255,255,255,.06);
 border:1px solid rgba(255,255,255,.14);border-left:3px solid transparent;
 border-radius:3px;padding:12px 14px;transition:background .2s,color .2s,border-color .2s}
.ea-q:hover{background:rgba(255,255,255,.12)}
.ea-q[aria-selected=true]{background:#fff;color:var(--navy);border-left-color:var(--amber)}
.ea-ans__box{margin-top:16px;border-top:1px solid rgba(255,255,255,.18);padding-top:16px;
 min-height:96px}
.ea-ans{margin:0;font-size:clamp(16px,1.5vw,19px);line-height:1.55;color:#fff}
.ea-fan{position:relative;aspect-ratio:4/3;min-height:300px}
.ea-page{position:absolute;left:50%;bottom:0;height:84%;width:auto;aspect-ratio:1058/1473;
 transform-origin:50% 118%;z-index:var(--z);cursor:pointer;overflow:hidden;border-radius:2px;
 background:#fff;box-shadow:0 12px 30px rgba(3,10,30,.45);
 transform:translateX(-50%) rotate(var(--a)) translateY(var(--u));
 transition:transform .45s cubic-bezier(.2,.7,.3,1),box-shadow .35s,filter .35s}
.ea-page img{width:100%;height:100%;object-fit:cover}
.ea-page:not(.is-on){filter:brightness(.78) saturate(.85)}
.ea-page:not(.is-on):hover{filter:none}
.ea-page.is-on{z-index:40;transform:translateX(-50%) rotate(0deg) translateY(-4%) scale(1.14);
 filter:none;box-shadow:0 26px 54px rgba(3,10,30,.55);cursor:default}
.ea-page__lb{position:absolute;left:0;right:0;bottom:0;padding:16px 8px 6px;text-align:center;
 font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#fff;opacity:0;
 background:linear-gradient(180deg,rgba(6,16,42,0),rgba(6,16,42,.8));transition:opacity .3s}
.ea-page:hover .ea-page__lb{opacity:1}
.ea-hl{position:absolute;border:2px solid var(--amber);border-radius:2px;
 box-shadow:0 0 0 2000px rgba(6,16,44,.6);animation:ea-pulse 1.6s ease-in-out infinite}
@keyframes ea-pulse{0%,100%{border-color:var(--amber)}50%{border-color:#FFD08A}}

/* ── ПРОГРАММА ─────────────────────────────────────────────────────────── */
.ea-track{display:flex;gap:3px;margin-top:clamp(26px,3vw,42px);height:66px}
.ea-bar{appearance:none;border:0;cursor:pointer;padding:0;min-width:0;border-radius:2px;
 position:relative;transition:filter .2s,transform .2s;flex-basis:0}
.ea-bar--talk{background:linear-gradient(180deg,var(--blue),#0F5FA3)}
.ea-bar--break{background:#D7DFE9}
.ea-bar:hover,.ea-bar.is-on{filter:brightness(1.12);transform:translateY(-3px)}
.ea-bar.is-on{outline:2px solid var(--amber);outline-offset:2px}
.ea-bar__m{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 font-family:'Cuprum','PT Sans',Arial,sans-serif;font-size:13px;font-weight:700;color:#fff}
.ea-bar--break .ea-bar__m{color:#5A6673}
.ea-track__ends{display:flex;justify-content:space-between;margin-top:8px;font-size:12.5px;
 letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.ea-slots{list-style:none;margin:clamp(24px,3vw,40px) 0 0;padding:0;border-top:1px solid var(--line)}
.ea-slot{display:grid;grid-template-columns:118px minmax(0,1fr) 72px;gap:18px;align-items:baseline;
 padding:14px 12px;border-bottom:1px solid var(--line);transition:background .2s}
.ea-slot.is-on{background:#EAF3FC}
.ea-slot__t{font-size:16px;font-weight:700;color:var(--navy);white-space:nowrap}
.ea-slot--break .ea-slot__t{color:var(--mute)}
.ea-slot__w b{display:block;font-size:17px;color:var(--crimson)}
.ea-slot__w i{display:block;font-style:normal;font-size:14px;color:var(--mute);margin:2px 0 4px}
.ea-slot__topic{display:block;font-size:15.5px;line-height:1.45}
.ea-slot--break .ea-slot__topic{color:var(--mute)}
.ea-slot__m{text-align:right;font-size:13px;color:var(--mute);white-space:nowrap}

/* ── ЗАСТРОЙКА И КОМПЛЕКТ ──────────────────────────────────────────────── */
.ea-build{background:var(--paper)}
.ea-grid{display:grid;gap:clamp(18px,2.2vw,30px);margin-top:clamp(26px,3vw,44px);
 grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
.ea-cell img{width:100%;height:auto;aspect-ratio:16/11;object-fit:cover;border-radius:3px}
.ea-cell--top img{object-position:50% 16%}
.ea-cell figcaption{margin-top:9px;font-size:13.5px;line-height:1.5;color:var(--mute)}
.ea-kit__grid{display:grid;gap:clamp(18px,2.4vw,34px);margin-top:clamp(26px,3vw,44px);
 grid-template-columns:repeat(3,minmax(0,1fr));align-items:start}
.ea-kit__badge img{width:100%;max-width:330px;height:auto;border-radius:2px;
 box-shadow:0 18px 42px rgba(11,27,68,.18)}
.ea-kit__side{grid-column:span 2;display:grid;gap:18px;grid-template-columns:1fr 1fr;
 align-items:center}
.ea-kit__cv{width:100%;aspect-ratio:1/1;border-radius:3px}

/* ── РОЛИК И РЕЗУЛЬТАТ ─────────────────────────────────────────────────── */
.ea-film{background:var(--deep);color:#fff}
.ea-film .ea-kick{color:var(--cyan)}
.ea-film .ea-lead{color:#CBDCEE}
.ea-film__grid{display:grid;gap:clamp(24px,3vw,48px);grid-template-columns:.8fr 1.2fr;
 align-items:center}
.ea-film__box video{width:100%;height:auto;aspect-ratio:16/9;background:#000;border-radius:3px}
.ea-res{list-style:none;margin:clamp(26px,3vw,42px) 0 0;padding:0;display:grid;
 gap:clamp(16px,2vw,30px);grid-template-columns:repeat(3,minmax(0,1fr))}
.ea-res li{border-top:3px solid var(--blue);padding-top:14px}
.ea-res b{display:block;font-size:clamp(21px,2.4vw,29px);font-weight:700;line-height:1.1}
.ea-res span{display:block;margin-top:6px;font-size:14.5px;line-height:1.5;color:var(--mute)}
.ea-sign{margin:clamp(30px,4vw,48px) 0 0;font-size:clamp(22px,3vw,34px);font-weight:700;
 color:var(--blue)}
.ea-more{margin:16px 0 0;font-size:15px;color:var(--mute)}
.ea-more a{color:var(--blue)}

/* ── АДАПТИВ ───────────────────────────────────────────────────────────── */
@media (max-width:1000px){
 .ea-task__grid,.ea-film__grid,.ea-guide__grid{grid-template-columns:1fr}
 .ea-kit__grid{grid-template-columns:1fr 1fr}
 .ea-kit__side{grid-column:span 2}
 .ea-res{grid-template-columns:1fr}
 .ea-res li{border-top-width:2px}
}
/* с 1000px сетка гида схлопывается в одну колонку, и веер в ней уже не живёт:
   показываем одну полосу, вопросы идут списком выше. position:relative на
   полосе обязателен — иначе прожектор .ea-hl считает координаты от .ea-fan
   и уезжает за пределы страницы */
@media (max-width:1000px){
 .ea-fan{aspect-ratio:auto;min-height:0;display:flex;justify-content:center}
 .ea-page{display:none}
 .ea-page.is-on{display:block;position:relative;left:auto;bottom:auto;height:auto;
  width:min(380px,100%);transform:none;box-shadow:0 18px 40px rgba(3,10,30,.5)}
 .ea-page__lb{opacity:1}
}
@media (max-width:720px){
 .ea-w{width:min(1180px,100% - 32px)}
 .ea-hero__facts{grid-template-columns:1fr 1fr;gap:12px 18px}
 .ea-step{grid-template-columns:1fr;gap:8px;padding-left:32px}
 .ea-step__t{display:flex;align-items:baseline;gap:10px}
 .ea-step__t b{font-size:19px}
 .ea-steps::before{left:5px}
 .ea-step::before{left:1px}
 .ea-day{padding-left:32px}
 .ea-day::before{width:12px;height:12px;top:31px}
 .ea-slot{grid-template-columns:1fr;gap:4px;padding:14px 8px}
 .ea-slot__m{text-align:left}
 .ea-track{height:52px}
 .ea-bar__m{font-size:11px}
 .ea-kit__grid,.ea-kit__side{grid-template-columns:1fr}
 .ea-kit__side{grid-column:auto}
 .ea-kit__cv{max-width:340px}
 .ea-shot--pg img{max-width:230px}
}
@media (max-width:520px){
 .ea-track{gap:2px}
 .ea-bar__m{display:none}
}
/* ландшафт телефона: герой не должен занимать три экрана */
@media (max-height:520px) and (orientation:landscape){
 .ea-hero{min-height:0;padding-top:96px}
 .ea-hero__facts{margin-top:20px}
}
@media (prefers-reduced-motion:reduce){
 .ea-r{opacity:1;transform:none;transition:none}
 .ea-page{transition:none}
 .ea-hl{animation:none}
}
</style>"""


PAGE_JS = """<script>(function(){
 var RM=matchMedia('(prefers-reduced-motion:reduce)').matches;

 // ── фирменная решётка Eaton: диагональная сетка, радиус растёт по той же
 //    оси, что и градиент (левый низ тёмный и пустой, правый верх светлый
 //    и крупный). Рисуем один раз на ресайз, при появлении разбегаемся от 0.
 function lattice(cv,o){
  var ctx=cv.getContext('2d');if(!ctx)return;
  var w=cv.clientWidth,h=cv.clientHeight;if(!w||!h)return;
  var dpr=Math.min(2,window.devicePixelRatio||1);
  cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr);
  var t0=0,raf=0;
  function draw(k){
   ctx.setTransform(dpr,0,0,dpr,0,0);
   var g=ctx.createLinearGradient(0,h,w,0),i;
   for(i=0;i<o.stops.length;i++)g.addColorStop(o.stops[i][0],o.stops[i][1]);
   ctx.fillStyle=g;ctx.fillRect(0,0,w,h);
   var s=Math.max(14,Math.min(38,Math.min(w,h)/o.div)),
       th=o.angle*Math.PI/180,cs=Math.cos(th),sn=Math.sin(th),
       R=Math.sqrt(w*w+h*h),u,v,x,y,t,r;
   for(u=-R;u<R;u+=s){
    for(v=-R;v<R;v+=s){
     x=u*cs-v*sn+w*0.5;y=u*sn+v*cs+h*0.5;
     if(x<-s||x>w+s||y<-s||y>h+s)continue;
     // t — «светлость» точки: правее и выше значит крупнее
     t=(x/w)*0.66+(1-y/h)*0.34;
     if(t<=o.floor)continue;
     t=(t-o.floor)/(1-o.floor);
     r=s*(0.05+0.30*Math.pow(t,1.5))*k;
     if(r<0.3)continue;
     ctx.beginPath();ctx.arc(x,y,r,0,6.2832);
     ctx.fillStyle='rgba(255,255,255,'+(0.14+0.74*t).toFixed(3)+')';ctx.fill();
     // вторая решётка вполсмещения, приглушённая: в печати точки двухтоновые
     x+=(cs-sn)*s/2;y+=(sn+cs)*s/2;
     if(x<0||x>w||y<0||y>h)continue;
     ctx.beginPath();ctx.arc(x,y,r*0.62,0,6.2832);
     ctx.fillStyle='rgba(190,228,250,'+(0.10+0.34*t).toFixed(3)+')';ctx.fill();
    }
   }
  }
  if(RM){draw(1);return;}
  cancelAnimationFrame(raf);
  (function step(now){
   if(!t0)t0=now;
   var k=Math.min(1,(now-t0)/700);
   draw(1-Math.pow(1-k,3));
   if(k<1)raf=requestAnimationFrame(step);
  })(performance.now());
 }
 var CVS=[['ea-cv',{angle:-26,div:26,floor:0.06,
   stops:[[0,'#071233'],[.42,'#17408F'],[.78,'#2E7FCB'],[1,'#68C2E9']]}],
  ['ea-cv2',{angle:-26,div:14,floor:0.04,
   stops:[[0,'#0B1B44'],[.5,'#1F5FB0'],[1,'#6ACEEE']]}]];
 function paint(){
  for(var i=0;i<CVS.length;i++){
   var el=document.getElementById(CVS[i][0]);
   if(el)lattice(el,CVS[i][1]);
  }
 }
 var rt;
 addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(paint,180);});
 paint();

 // ── гид: вопрос вытягивает полосу и подсвечивает место с ответом
 var Q=%Q%,fan=document.getElementById('ea-fan');
 if(fan){
  var qs=[].slice.call(document.querySelectorAll('.ea-q')),
      pages=[].slice.call(fan.querySelectorAll('.ea-page')),
      answers=[].slice.call(document.querySelectorAll('.ea-ans')),cur=-1;
  function show(i){
   if(i===cur||!Q[i])return;cur=i;
   var q=Q[i];
   qs.forEach(function(b,j){b.setAttribute('aria-selected',String(j===i));});
   answers.forEach(function(a,j){a.hidden=j!==i;});
   pages.forEach(function(p,j){
    var on=j===q.p,hl=p.querySelector('.ea-hl');
    p.classList.toggle('is-on',on);
    if(on){
     hl.hidden=false;
     hl.style.left=(q.b[0]*100)+'%';hl.style.top=(q.b[1]*100)+'%';
     hl.style.width=(q.b[2]*100)+'%';hl.style.height=(q.b[3]*100)+'%';
    }else{hl.hidden=true;}
   });
  }
  qs.forEach(function(b){b.addEventListener('click',function(){show(+b.getAttribute('data-i'));});});
  // клик по полосе выбирает первый вопрос, который на неё ссылается
  pages.forEach(function(p){
   p.addEventListener('click',function(){
    var pi=+p.getAttribute('data-p');
    for(var i=0;i<Q.length;i++)if(Q[i].p===pi){show(i);return;}
   });
  });
  document.querySelector('.ea-qs').addEventListener('keydown',function(e){
   var d=e.key==='ArrowDown'?1:e.key==='ArrowUp'?-1:0;if(!d)return;
   e.preventDefault();var n=(cur+d+qs.length)%qs.length;show(n);qs[n].focus();
  });
  show(0);
 }

 // ── программа: полоса и список подсвечивают друг друга
 var track=document.querySelector('.ea-track'),slots=document.querySelector('.ea-slots');
 if(track&&slots){
  var bars=[].slice.call(track.children),rows=[].slice.call(slots.children);
  function mark(i,on){
   if(bars[i])bars[i].classList.toggle('is-on',on);
   if(rows[i])rows[i].classList.toggle('is-on',on);
  }
  function bind(list){
   list.forEach(function(el,i){
    el.addEventListener('mouseenter',function(){mark(i,true);});
    el.addEventListener('mouseleave',function(){mark(i,false);});
    el.addEventListener('focus',function(){mark(i,true);});
    el.addEventListener('blur',function(){mark(i,false);});
   });
  }
  bind(bars);bind(rows);
 }

 // ── появление блоков
 var els=[].slice.call(document.querySelectorAll('.ea-r'));
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
<title>Партнёрская конференция Eaton в Алматы, 2016 | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: партнёрская конференция Eaton, Алматы, Grand Hotel Tien Shan, 28 сентября 2016. Перелёты, трансферы, размещение, застройка зала, сцена и проекция, POSm и печатный гид участника на 8 полос. Семь выступлений с 9:00 до 15:30.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Партнёрская конференция Eaton в Алматы, 2016 | Hand Marketing">
<meta property="og:description" content="Трое суток в другой стране под ключ: перелёты и трансферы, отель, застройка зала, комплект участника и гид, в котором есть ответ на любой вопрос.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/hall-full.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/cuprum-ptsans.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Event","item":"https://hand-marketing.ru/event/"},'
  '{"@type":"ListItem","position":3,"name":"Партнёрская конференция Eaton",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    q = [{'p': p, 'b': list(b)} for _t, p, b, _a in QUESTIONS]
    js = PAGE_JS.replace('%Q%', json.dumps(q, ensure_ascii=False))
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="ea">{hero()}{task()}{trip()}{guide()}'
            f'{program()}{build()}{kit()}{film()}{out()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'event', 'eaton')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
