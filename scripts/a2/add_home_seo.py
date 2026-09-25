#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Текстовая секция на главной: что за агентство, что делает, чем это доказано.

Замер 19.09.2026: на десктопной главной 272 слова видимого текста, из них
связного текста одна фраза. Направления названы латиницей («Exhibition Build»,
«Content»), карточки каталога идут с пустыми подписями. У главных страниц
конкурентов из топ-10 от 1013 до 2685 слов.

Позиционирование задано владельцем 20.09.2026: заказчики это крупные компании,
на сайте они подтверждают квалификацию подрядчика, а не ищут дешевле. При этом
цена на странице нужна поиску, и владелец расставил приоритет: сначала попасть
в выдачу. Поэтому цифры есть, но поданы как порядок бюджета, а доказываем
масштабом объектов и порядком работы, а не выгодой.

Вставляется перед формой заявки: в мобильную версию (section.mh-form) и
в десктопную (запись rec237885363). Zero-блоки не трогаем.

    python3 scripts/a2/add_home_seo.py

Идемпотентен: секция вырезается по маркеру и собирается заново.
"""
import html as H
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
sys.path.insert(0, HERE)

MARK = 'hm-home-seo'
END = '<!-- /hm-home-seo -->'
PAGE = os.path.join(ROOT, 'index-a2.html')
ANCHORS = ['<section class="mh-form"', '<div id="rec237885363"']

# направление -> (ссылка, бюджет, описание, цвет направления, буква-знак)
# Цвета и приёмы те же, что у карточек услуг в мобильной вёрстке (.mh-scard):
# буква-водяной знак под карточкой, тег с квадратом-маркером, диск-стрелка.
# Цена на главной нужна поиску: по коммерческим запросам Яндекс сверяет, похожа ли
# страница на место, где услугу заказывают. Подаём её как порядок бюджета, а не как
# прайс со скидками: заказчик у нас проверяет квалификацию, а не ищет дешевле.
LINES = [
    ('Выставочные стенды под ключ', '/exhibition/', 'от 500 000 ₽',
     'Концепция, проект, конструктив, застройка, мультимедиа и монтаж. Отвечаем '
     'за стенд целиком, включая согласования с площадкой и работу на монтаже.', '#8E5FB0', 'E'),
    ('Мультимедиа для стенда', '/exhibition/multimedia/', 'от 150 000 ₽',
     'Экраны, кинетика, интерактив и контент под них. Считаем под конкретную '
     'поверхность, а не подгоняем готовый ролик.', '#7E3FA0', 'M'),
    ('Организация мероприятий', '/event/', 'от 500 000 ₽',
     'Конференции, презентации, корпоративные события и вечера для арендаторов: '
     'концепция, площадка, продакшн, техника и проведение.', '#673A7E', 'E'),
    ('Видеопродакшн', '/videoproduction/', 'от 150 000 ₽',
     'Рекламные ролики, корпоративные фильмы, съёмка объектов и мероприятий. '
     'Своя съёмочная группа, операторы и техника.', '#CF6F19', 'V'),
    ('Мультимедийный контент', '/content/', 'от 150 000 ₽',
     'Контент для экранов, куполов, фасадов, кинетических конструкций и VR. '
     'Собственная команда графики и 3D.', '#E0427E', 'C'),
    ('3D Mapping и проекционные шоу', '/3dmapping/', 'по объёму',
     'Проекции на здания и объекты: замеры, сценарий, графика под геометрию, '
     'оборудование, монтаж и показ.', '#7E3FA0', '3'),
    ('Креатив и дизайн', '/creativedesign/', 'по объёму',
     'Концепции кампаний, фирменный стиль и брендбуки, дизайн полиграфии '
     'и презентаций, 3D-визуализация.', '#C12164', 'C'),
    ('Печать и рекламное производство', '/printandproduction/', 'по объёму',
     'Широкоформатная печать, полиграфия, POS-материалы, навигация '
     'и нестандартные конструкции.', '#E08A2B', 'P'),
    ('Фотопродакшн', '/photo/', 'по объёму',
     'Предметная и каталожная съёмка, съёмка оборудования на объекте, '
     'репортаж с мероприятий.', '#3B729D', 'P'),
    ('BTL и промо', '/btl/', 'по объёму',
     'Промо-акции, семплинг, полевые команды и отчётность по точкам.', '#D6357E', 'B'),
    ('Сайты и посадочные страницы', '/digital/', 'по объёму',
     'Страницы объектов и проектов: структура, дизайн, тексты, сборка '
     'и аналитика.', '#5E9A2E', 'D'),
]

# короткая метка направления в теге карточки: так они подписаны на сайте
TAGS = {
    'Выставочные стенды под ключ': 'Exhibition', 'Мультимедиа для стенда': 'Exhibition',
    'Организация мероприятий': 'Event', 'Видеопродакшн': 'Video production',
    'Мультимедийный контент': 'Content', '3D Mapping и проекционные шоу': '3D Mapping',
    'Креатив и дизайн': 'Creative & Design', 'Печать и рекламное производство': 'Print & Production',
    'Фотопродакшн': 'Photo production', 'BTL и промо': 'BTL',
    'Сайты и посадочные страницы': 'Digital',
}

# проекты: (цифра, подпись, ссылка, цвет, метка на круге, пояснение)
PROOF = [
    ('248 дней', 'работы стенда Самарской области', '/portfolio/samara-stand-vdnh/',
     '#8E5FB0', 'ВДНХ',
     'Выставка-форум «Россия» на ВДНХ: экран-парус с naked eye 3D, кинетическая '
     'стена, тач-панели и расписание на 817 слотов. Стенд работал без нас '
     'на площадке каждый день восемь месяцев.'),
    ('27 проекторов', 'на фасаде Правительства Ставропольского края', '/3d/stavropol/',
     '#7E3FA0', '3D',
     'Проекционное шоу на площади Ленина: девять зон по зданию, один пульт, '
     'больше 25 000 зрителей за вечер.'),
    ('11 городов', 'чемпионата мира по футболу', '/video/powertechnologies/',
     '#CF6F19', 'ЧМ',
     'Фильм для Power Technologies об энергоснабжении ЧМ-2018: 12 стадионов, '
     'восемь интервью, съёмка по всей стране.'),
    ('117 планов', 'в фильме к десятилетию ЦМ РЖД', '/video/rgd/history/',
     '#3B729D', 'РЖД',
     'Грузовые дворы, техника в работе и семь услуг дирекции в одном рассказе '
     'на 3:54. Съёмка шла в нескольких городах сети.'),
    ('10 минут', 'фильма о клиентском опыте Saint-Gobain', '/video/saintgobain/cx/',
     '#C12164', 'SG',
     'Две части: путь заказа от завода до объекта и прямая речь сотрудников. '
     '48 человек названы в кадре по имени.'),
    ('3 дня', 'партнёрской конференции Eaton в Алматы', '/event/eaton/',
     '#5E9A2E', 'EATON',
     'Программа в двух часовых поясах, печатный гид участника, работа '
     'с площадкой и подрядчиками в другой стране.'),
]

# шаги: (заголовок, цвет диска, текст)
STEPS = [
    ('Бриф и задача', '#673A7E',
     'Разбираемся, что должно получиться и по каким критериям это примут. '
     'На этом шаге честно говорим, если задача не помещается в срок или бюджет.'),
    ('Решение и смета', '#8E5FB0',
     'Показываем, как сделаем, и считаем смету построчно. Заказчик видит, '
     'из чего складывается цифра и что можно убрать.'),
    ('Промежуточные листы', '#C12164',
     'Работа видна на каждом шаге: 79 листов проекта стенда, 31 лист раскадровки '
     'ролика для ГАЗ, 79 склеек в монтажном листе. Согласование идёт по ним, '
     'а не по словам «уже почти готово».'),
    ('Производство', '#CF6F19',
     'Съёмка, графика, 3D и дизайн делает наша команда, за печать и конструкции '
     'отвечаем сами. У проекта один ответственный от брифа до площадки.'),
    ('Площадка и сдача', '#5E9A2E',
     'Монтаж, тесты, работа на объекте, демонтаж. Материалы, исходники '
     'и отчётность передаём заказчику.'),
]

FAQ = [
    ('Как вы работаете с крупными компаниями по документам?',
     'Договор, счёт, акты, НДС. Работаем с юридическими лицами, в том числе '
     'с международными компаниями и структурами с внутренними регламентами '
     'закупки. Среди заказчиков Samsung, Saint-Gobain, Eaton, РЖД, '
     'Messe Düsseldorf, Becar.'),
    ('Кто отвечает за проект и с кем общается заказчик?',
     'У проекта один менеджер и профильная команда: креативный директор, '
     'продюсер, технический директор. Заказчик обсуждает задачу с одним '
     'человеком, а не с пятью подрядчиками.'),
    ('Вы работаете в регионах и за рубежом?',
     'Да. Снимали и строили в Москве, Самаре, Ставрополе, Уфе, Калининграде, '
     'Санкт-Петербурге и Алматы. Логистику, монтаж и работу с местными службами '
     'берём на себя.'),
    ('Что вы делаете сами, а что отдаёте на сторону?',
     'Съёмка, монтаж, графика, 3D и дизайн делает наша команда. Печать, конструкции '
     'и технику мы ведём сами и отвечаем за них перед заказчиком: у проекта один '
     'ответственный, и нам не на кого сослаться, если что-то пошло не так.'),
    ('Можно заказать одно направление, а не весь цикл?',
     'Да, большинство проектов так и начинается: ролик, стенд или брошюра. '
     'Saint-Gobain, Eaton и Becar пришли с одной задачей и остались '
     'на несколько лет и десятки проектов.'),
    ('Сколько стоит проект?',
     'Рекламный ролик и мультимедийная зона от 150 000 ₽, мероприятие под ключ '
     'и выставочный стенд от 500 000 ₽. По дизайну, печати, промо и съёмке считаем '
     'по объёму работ. Точную цифру называем после брифа, смета бесплатна '
     'и построчна: видно, за что платите и что можно убрать.'),
]

CSS = """<style id="hm-home-seo-css">
/* приёмы взяты у карточек услуг мобильной вёрстки (.mh-scard): цвет направления,
   буква-водяной знак, радиус 24 с мягкой тенью, диск-стрелка вместо ссылки */
.hs{--ink:#14171C;--mut:#5A616A;--a:#673A7E;--line:#ECEEF2;
 font-family:'Montserrat',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff;
 padding:76px 0 68px;border-top:1.5px solid var(--line)}
.hs *{box-sizing:border-box}
.hs__in{max-width:1180px;margin:0 auto;padding:0 40px}
.hs__tag{display:inline-flex;align-items:center;gap:9px;font-size:11px;font-weight:800;
 letter-spacing:.2em;text-transform:uppercase;color:var(--a);margin-bottom:12px}
.hs__tag::before{content:"";width:11px;height:11px;border-radius:3px;background:currentColor}
.hs h2{margin:0 0 14px;font-size:clamp(26px,3.1vw,40px);font-weight:800;letter-spacing:-.02em;line-height:1.08}
.hs h3{margin:54px 0 18px;font-size:clamp(21px,2.4vw,28px);font-weight:800;letter-spacing:-.015em}
.hs p.lead{margin:0 0 16px;max-width:74ch;font-size:16.5px;line-height:1.7;color:#3d434b}
.hs p.lead a,.hs-budget span a{color:inherit!important;text-decoration:none;border-bottom:2px solid rgba(20,23,28,.28)}
.hs p.lead a:hover,.hs-budget span a:hover{border-color:currentColor}

/* направления */
.hs-dirs{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.hs-dir{position:relative;isolation:isolate;overflow:hidden;background:#fff;
 border:1.5px solid var(--line);border-radius:24px;padding:24px 24px 22px;
 box-shadow:0 14px 30px -22px rgba(20,23,28,.5);transition:border-color .25s,box-shadow .25s,transform .15s}
.hs-dir:hover{border-color:var(--c);box-shadow:0 18px 36px -20px var(--c);transform:translateY(-2px)}
.hs-dir__ghost{position:absolute;z-index:-1;right:4px;bottom:-44px;font:900 168px/1 'Montserrat',Arial,sans-serif;
 color:var(--c);opacity:.09;letter-spacing:-.06em;pointer-events:none;user-select:none}
.hs-dir__tag{display:inline-flex;align-items:center;gap:9px;font-size:11px;font-weight:800;
 letter-spacing:.2em;text-transform:uppercase;color:var(--c)}
.hs-dir__tag::before{content:"";width:11px;height:11px;border-radius:3px;background:var(--c)}
.hs-dir h4{margin:13px 0 9px;font-size:22px;font-weight:800;letter-spacing:-.01em;line-height:1.1}
.hs-dir h4 a{color:#14171C!important;text-decoration:none;border:0}
.hs-dir h4 a:hover{color:var(--c)!important}
.hs-p a,.hs-more a,.hs-faq a{border-bottom:2px solid currentColor;text-decoration:none}
.hs-dir p{margin:0 0 18px;font-size:15px;line-height:1.5;color:var(--mut)}
.hs-dir__foot{display:flex;align-items:center;justify-content:space-between;gap:12px}
.hs-dir__price{font-size:15px;font-weight:800;color:var(--c)}
.hs-dir__go{width:44px;height:44px;border-radius:50%;background:var(--c);color:#fff!important;display:inline-flex;
 align-items:center;justify-content:center;flex:none;text-decoration:none}
.hs-dir__go svg{width:18px;height:18px;stroke:#fff;fill:none;stroke-width:2.4;
 stroke-linecap:round;stroke-linejoin:round}

/* проекты с цифрами: круг обложки и кубики за его границей */
.hs-proof{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.hs-p{position:relative;background:#fff;border:1.5px solid var(--line);border-radius:24px;
 padding:28px 26px 24px;box-shadow:0 14px 30px -22px rgba(20,23,28,.5);
 display:flex;flex-direction:column;gap:14px;transition:border-color .25s,box-shadow .25s}
.hs-p:hover{border-color:var(--c);box-shadow:0 18px 36px -20px var(--c)}
.hs-p__disc{position:relative;width:118px;height:118px;flex:none}
.hs-p__disc span{width:118px;height:118px;border-radius:50%;background:var(--c);color:#fff;
 display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;letter-spacing:-.02em}
.hs-p__disc i,.hs-p__disc em{position:absolute;display:block;border-radius:6px;font-style:normal}
.hs-p__disc i{right:-9px;top:8px;width:24px;height:24px;background:#96C223}
.hs-p__disc em{left:-10px;bottom:10px;width:17px;height:17px;background:#FCB724}
.hs-p b{display:block;font-size:34px;font-weight:900;letter-spacing:-.03em;color:var(--c);line-height:1}
.hs-p i.cap{display:block;margin-top:6px;font-style:normal;font-size:15px;font-weight:700}
.hs-p span.txt{display:block;font-size:14.5px;line-height:1.6;color:var(--mut)}
.hs-p a{margin-top:auto;align-self:flex-start;font-size:14.5px;font-weight:800;color:var(--c)!important;
 text-decoration:none;border-bottom:2px solid currentColor}

/* шаги */
.hs-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:20px}
.hs-step__n{width:46px;height:46px;border-radius:50%;background:var(--c);color:#fff;
 font-size:17px;font-weight:900;display:inline-flex;align-items:center;justify-content:center;margin-bottom:12px}
.hs-step h4{margin:0 0 6px;font-size:16px;font-weight:800;line-height:1.25}
.hs-step p{margin:0;font-size:13.5px;line-height:1.55;color:var(--mut)}

/* отзывы */
.hs-quotes{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.hs-q{margin:0;position:relative;background:#fff;border:1.5px solid var(--line);border-radius:24px;
 padding:26px 24px 22px;box-shadow:0 14px 30px -22px rgba(20,23,28,.5);
 display:flex;flex-direction:column;gap:16px}
.hs-q__mark{font:900 64px/.6 'Montserrat',Arial,sans-serif;color:var(--c);opacity:.18}
.hs-q blockquote{margin:0;font-size:15.5px;line-height:1.6;font-weight:500}
.hs-q figcaption{margin-top:auto;display:flex;align-items:center;gap:12px;font-size:13.5px;
 line-height:1.4;color:var(--mut)}
.hs-q__ava{width:44px;height:44px;border-radius:50%;background:var(--c);color:#fff;flex:none;
 font-size:14px;font-weight:900;display:inline-flex;align-items:center;justify-content:center}
.hs-q figcaption b{display:block;color:var(--ink);font-size:15px}

/* бюджет */
.hs-budget{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:8px}
.hs-budget div{background:#fff;border:1.5px solid var(--line);border-radius:24px;padding:24px;
 box-shadow:0 14px 30px -22px rgba(20,23,28,.5)}
.hs-budget i{display:block;width:44px;height:6px;border-radius:3px;background:var(--c);margin-bottom:16px}
.hs-budget b{display:block;font-size:26px;font-weight:900;letter-spacing:-.02em;white-space:nowrap}
.hs-budget span{display:block;margin-top:8px;font-size:14.5px;line-height:1.55;color:var(--mut)}

/* вопросы */
.hs-faq{display:grid;gap:12px;max-width:900px}
.hs-faq details{border:1.5px solid var(--line);border-radius:20px;padding:0 22px;background:#fff}
.hs-faq summary{cursor:pointer;list-style:none;padding:18px 0;font-size:16px;font-weight:800;
 display:flex;align-items:center;gap:14px}
.hs-faq summary::-webkit-details-marker{display:none}
.hs-faq summary::before{content:"";width:30px;height:30px;border-radius:50%;flex:none;background:#ECEEF2;
 background-image:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2314171C' stroke-width='3' stroke-linecap='round'%3E%3Cpath d='M12 5v14M5 12h14'/%3E%3C/svg%3E");
 background-size:14px;background-repeat:no-repeat;background-position:center}
.hs-faq details[open] summary::before{background-color:#673A7E;
 background-image:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='3' stroke-linecap='round'%3E%3Cpath d='M5 12h14'/%3E%3C/svg%3E")}
.hs-faq p{margin:0 0 20px 44px;font-size:15px;line-height:1.65;color:var(--mut)}
.hs-more{margin:34px 0 0;font-size:15.5px;line-height:1.7;color:#3d434b}
.hs-more a{color:var(--a)!important;font-weight:700}
@media(max-width:1000px){.hs-dirs,.hs-proof,.hs-quotes,.hs-budget{grid-template-columns:1fr 1fr}
 .hs-steps{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.hs__in{padding:0 18px}.hs{padding:52px 0 44px}
 .hs-dirs,.hs-proof,.hs-quotes,.hs-steps,.hs-budget{grid-template-columns:1fr}}
</style>"""


def esc(t):
    return H.escape(t, quote=False)


def quotes():
    rv = json.load(open(os.path.join(HERE, 'reviews.json'), encoding='utf-8'))
    meta = {'sg_video': ('#C12164', 'SG'), 'messe': ('#673A7E', 'MD'),
            'becar_2019': ('#5E9A2E', 'BC')}
    out = ''
    for k, (color, ava) in meta.items():
        r = rv[k]
        q = r['quote']
        if len(q) > 190:
            q = q[:188].rsplit(' ', 1)[0] + '…'
        out += (f'<figure class="hs-q" style="--c:{color}">'
                f'<span class="hs-q__mark" aria-hidden="true">\u201c</span>'
                f'<blockquote>«{esc(q)}»</blockquote>'
                f'<figcaption><span class="hs-q__ava" aria-hidden="true">{ava}</span>'
                f'<span><b>{esc(r["company"])}</b>{esc(r["person"])}, '
                f'{esc(r["role"])}</span></figcaption></figure>')
    return out


def build(with_css=True, with_ld=True):
    arrow = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
             '<path d="M5 12h13M12 5l7 7-7 7"/></svg>')
    dirs = ''.join(
        f'<div class="hs-dir" style="--c:{color}">'
        f'<span class="hs-dir__ghost" aria-hidden="true">{esc(letter)}</span>'
        f'<span class="hs-dir__tag">{esc(TAGS.get(t, t))}</span>'
        f'<h4><a href="{h}">{esc(t)}</a></h4><p>{esc(d)}</p>'
        f'<span class="hs-dir__foot"><span class="hs-dir__price">{esc(price)}</span>'
        f'<a class="hs-dir__go" href="{h}" aria-label="Открыть направление: {H.escape(t)}">'
        f'{arrow}</a></span></div>'
        for t, h, price, d, color, letter in LINES)
    proof = ''.join(
        f'<div class="hs-p" style="--c:{color}">'
        f'<span class="hs-p__disc"><span>{esc(mark)}</span>'
        f'<i aria-hidden="true"></i><em aria-hidden="true"></em></span>'
        f'<span><b>{esc(n)}</b><i class="cap">{esc(cap)}</i></span>'
        f'<span class="txt">{esc(txt)}</span>'
        f'<a href="{href}">Разбор проекта →</a></div>'
        for n, cap, href, color, mark, txt in PROOF)
    steps = ''.join(
        f'<div class="hs-step" style="--c:{color}">'
        f'<span class="hs-step__n">{i + 1:02d}</span>'
        f'<h4>{esc(t)}</h4><p>{esc(d)}</p></div>'
        for i, (t, color, d) in enumerate(STEPS))
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
                  for q, a in FAQ)
    ld = ''
    if with_ld:
        schema = {'@context': 'https://schema.org', '@type': 'FAQPage',
                  'mainEntity': [{'@type': 'Question', 'name': q,
                                  'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                                 for q, a in FAQ]}
        ld = ('<script type="application/ld+json" data-hm="home-faq">'
              + json.dumps(schema, ensure_ascii=False, separators=(',', ':')) + '</script>')
    return f'''<!-- {MARK} -->{CSS if with_css else ''}
<section class="hs" aria-label="Об агентстве">
<div class="hs__in">
<span class="hs__tag">Рекламное агентство с 2012 года</span>
<h2>Рекламное агентство полного цикла в Москве</h2>
<p class="lead">Hand Marketing работает с 2012 года. Мы строим выставочные стенды, проводим
 мероприятия, снимаем <a href="/videoproduction/reklamnyy-rolik/">рекламу</a>
 и <a href="/videoproduction/korporativnyy-film/">корпоративные фильмы</a>, делаем мультимедийный
 контент, <a href="/creativedesign/brandbook/">фирменный стиль</a> и печать. Заказчики приходят не за отдельной услугой, а за результатом на площадке:
 стенд, который отработает восемь месяцев на ВДНХ, фильм, который покажут партнёрам, шоу,
 которое увидит городская площадь.</p>
<p class="lead">С нами работают компании, у которых цена ошибки выше стоимости проекта:
 Samsung, Saint-Gobain, Eaton, РЖД, Messe Düsseldorf, Becar, администрации регионов.
 Для них важно не то, что подрядчик дешевле, а то, что он доведёт работу до конца
 в согласованный срок и в согласованном виде. Поэтому производство мы держим внутри:
 съёмку, графику, 3D и дизайн делает наша команда, а за печать и конструкции мы
 отвечаем сами.</p>

<h3>Направления</h3>
<div class="hs-dirs">{dirs}</div>

<h3>Проекты, по которым нас проверяют</h3>
<p class="lead">Шесть проектов, где масштаб виден по цифрам. У каждого на сайте
 есть разбор: что было в задаче, как считали, что получилось.</p>
<div class="hs-proof">{proof}</div>

<h3>Как устроена работа</h3>
<div class="hs-steps">{steps}</div>

<h3>Что говорят заказчики</h3>
<div class="hs-quotes">{quotes()}</div>
<p class="hs-more">Все одиннадцать благодарственных писем со сканами лежат на странице
 <a href="/reviews/">отзывов</a>. Состав команды, которая ведёт проекты, на странице
 <a href="/team/">команды</a>, а порядок расчёта и нижние границы бюджетов
 на странице <a href="/price/">стоимости</a>.</p>

<h3>Порядок бюджета</h3>
<p class="lead">Ниже нижние границы по направлениям: это не прайс, а рамка, чтобы
 сразу понимать масштаб. Точную цифру считаем по задаче, смета бесплатна и построчна.</p>
<div class="hs-budget">
 <div style="--c:#CF6F19"><i aria-hidden="true"></i><b>от 150 000 ₽</b><span><a href="/videoproduction/reklamnyy-rolik/">рекламный ролик</a> или <a href="/videoproduction/korporativnyy-film/">корпоративный фильм</a></span></div>
 <div style="--c:#E0427E"><i aria-hidden="true"></i><b>от 150 000 ₽</b><span>мультимедийная зона на <a href="/exhibition/multimedia/">стенде</a> или мероприятии</span></div>
 <div style="--c:#673A7E"><i aria-hidden="true"></i><b>от 500 000 ₽</b><span>мероприятие под ключ, в том числе <a href="/event/novogodniy-korporativ/">новогодний корпоратив</a></span></div>
 <div style="--c:#8E5FB0"><i aria-hidden="true"></i><b>от 500 000 ₽</b><span>выставочный стенд под ключ</span></div>
</div>
<p class="hs-more">По дизайну, печати, промо и съёмке считаем по объёму работ: состав смет
 и что на них влияет, разобрано на странице <a href="/price/">стоимости</a>.</p>

<h3>Вопросы</h3>
<div class="hs-faq">{faq}</div>
</div>{ld}
</section>
{END}
'''


def strip_old(s):
    while True:
        i = s.find(f'<!-- {MARK}')
        if i < 0:
            return s
        j = s.find(END, i)
        j = j + len(END) if j >= 0 else s.find('</section>', i) + len('</section>')
        s = s[:i] + s[j:]


def main():
    for path in (PAGE, os.path.join(ROOT, 'index.html')):
        if not os.path.isfile(path):
            continue
        s = strip_old(open(path, encoding='utf-8').read())
        n = 0
        for anchor in ANCHORS:
            if anchor not in s:
                continue
            s = s.replace(anchor, build(with_css=True, with_ld=(n == 0)) + anchor, 1)
            n += 1
        if not n:
            print(f'{os.path.basename(path)}: якорей формы нет — пропуск')
            continue
        open(path, 'w', encoding='utf-8').write(s)
        print(f'{os.path.basename(path)}: секция вставлена в {n} мест(а)')


if __name__ == '__main__':
    main()
