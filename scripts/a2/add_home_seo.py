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

# направление -> (ссылка, что это, нижняя граница бюджета)
# Цена на главной нужна поиску: по коммерческим запросам Яндекс сверяет, похожа ли
# страница на место, где услугу заказывают. Подаём её как порядок бюджета, а не как
# прайс со скидками: заказчик у нас проверяет квалификацию, а не ищет дешевле.
LINES = [
    ('Выставочные стенды под ключ', '/exhibition/', 'от 500 000 ₽',
     'Концепция, проект, конструктив, застройка, мультимедиа и монтаж. Отвечаем '
     'за стенд целиком, включая согласования с площадкой и работу на монтаже.'),
    ('Мультимедиа для стенда', '/exhibition/multimedia/', 'от 150 000 ₽',
     'Экраны, кинетика, интерактив и контент под них. Считаем под конкретную '
     'поверхность, а не подгоняем готовый ролик.'),
    ('Организация мероприятий', '/event/', 'от 500 000 ₽',
     'Конференции, презентации, корпоративные события и вечера для арендаторов: '
     'концепция, площадка, продакшн, техника и проведение.'),
    ('Видеопродакшн', '/videoproduction/', 'от 150 000 ₽',
     'Рекламные ролики, корпоративные фильмы, съёмка объектов и мероприятий. '
     'Своя съёмочная группа, операторы и техника.'),
    ('Мультимедийный контент', '/content/', 'от 150 000 ₽',
     'Контент для экранов, куполов, фасадов, кинетических конструкций и VR. '
     'Собственная команда графики и 3D.'),
    ('3D Mapping и проекционные шоу', '/3dmapping/', 'по объёму',
     'Проекции на здания и объекты: замеры, сценарий, графика под геометрию, '
     'оборудование, монтаж и показ.'),
    ('Креатив и дизайн', '/creativedesign/', 'по объёму',
     'Концепции кампаний, фирменный стиль и брендбуки, дизайн полиграфии '
     'и презентаций, 3D-визуализация.'),
    ('Печать и рекламное производство', '/printandproduction/', 'по объёму',
     'Широкоформатная печать, полиграфия, POS-материалы, навигация '
     'и нестандартные конструкции.'),
    ('Фотопродакшн', '/photo', 'по объёму',
     'Предметная и каталожная съёмка, съёмка оборудования на объекте, '
     'репортаж с мероприятий.'),
    ('BTL и промо', '/btl/', 'по объёму',
     'Промо-акции, семплинг, полевые команды и отчётность по точкам.'),
    ('Сайты и посадочные страницы', '/digital/', 'по объёму',
     'Страницы объектов и проектов: структура, дизайн, тексты, сборка '
     'и аналитика.'),
]

# проекты, по которым нас проверяют: (цифра, подпись, ссылка, пояснение)
PROOF = [
    ('248 дней', 'работы стенда Самарской области', '/portfolio/samara-stand-vdnh/',
     'Выставка-форум «Россия» на ВДНХ: экран-парус с naked eye 3D, кинетическая '
     'стена, тач-панели и расписание на 817 слотов. Стенд работал без нас '
     'на площадке каждый день восемь месяцев.'),
    ('27 проекторов', 'на фасаде Правительства Ставропольского края', '/3d/stavropol/',
     'Проекционное шоу на площади Ленина: девять зон по зданию, один пульт, '
     'больше 25 000 зрителей за вечер.'),
    ('11 городов', 'чемпионата мира по футболу', '/video/powertechnologies/',
     'Фильм для Power Technologies об энергоснабжении ЧМ-2018: 12 стадионов, '
     'восемь интервью, съёмка по всей стране.'),
    ('117 планов', 'в фильме к десятилетию ЦМ РЖД', '/video/rgd/history/',
     'Грузовые дворы, техника в работе и семь услуг дирекции в одном рассказе '
     'на 3:54. Съёмка шла в нескольких городах сети.'),
    ('10 минут', 'фильма о клиентском опыте Saint-Gobain', '/video/saintgobain/cx/',
     'Две части: путь заказа от завода до объекта и прямая речь сотрудников. '
     '48 человек названы в кадре по имени.'),
    ('3 дня', 'партнёрской конференции Eaton в Алматы', '/event/eaton/',
     'Программа в двух часовых поясах, печатный гид участника, работа '
     'с площадкой и подрядчиками в другой стране.'),
]

STEPS = [
    ('Бриф и задача',
     'Разбираемся, что должно получиться и по каким критериям это примут. '
     'На этом шаге честно говорим, если задача не помещается в срок или бюджет.'),
    ('Решение и смета',
     'Показываем, как сделаем, и считаем смету построчно. Заказчик видит, '
     'из чего складывается цифра и что можно убрать.'),
    ('Промежуточные листы',
     'Работа видна на каждом шаге: 79 листов проекта стенда, 31 лист раскадровки '
     'ролика для ГАЗ, 79 склеек в монтажном листе. Согласование идёт по ним, '
     'а не по словам «уже почти готово».'),
    ('Производство',
     'Съёмка, графика, дизайн, печать и конструкции внутри агентства. Между '
     'этапами нет чужих подрядчиков, на которых можно сослаться при срыве.'),
    ('Площадка и сдача',
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
     'Съёмка, монтаж, графика и 3D, дизайн, печать и конструкции делаются внутри '
     'агентства. Это и есть причина, по которой у проекта один ответственный: '
     'нам не на кого сослаться, если что-то пошло не так.'),
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
.hs{--ink:#14171C;--mut:#5A616A;--a:#673A7E;--line:rgba(20,23,28,.12);
 font-family:'Montserrat',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff;
 padding:72px 0 64px;border-top:1px solid var(--line)}
.hs *{box-sizing:border-box}
.hs__in{max-width:1180px;margin:0 auto;padding:0 40px}
.hs h2{margin:0 0 14px;font-size:clamp(25px,3vw,36px);font-weight:800;letter-spacing:-.02em;line-height:1.12}
.hs h3{margin:46px 0 16px;font-size:clamp(20px,2.3vw,26px);font-weight:800;letter-spacing:-.015em}
.hs p.lead{margin:0 0 16px;max-width:74ch;font-size:16.5px;line-height:1.7;color:#3d434b}
.hs-dirs{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.hs-dir{border:1px solid var(--line);border-radius:16px;padding:18px 20px}
.hs-dir b{display:block;margin-bottom:8px;font-size:16px}
.hs-dir b a{color:inherit;text-decoration:none;border-bottom:2px solid rgba(103,58,126,.35)}
.hs-dir b a:hover{color:var(--a)}
.hs-dir span{font-size:13.5px;line-height:1.6;color:var(--mut)}
.hs-dir em{display:block;margin-top:10px;font-style:normal;font-size:13px;font-weight:700;letter-spacing:.04em;color:var(--a)}
.hs-proof{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.hs-p{border-top:2px solid var(--a);padding-top:14px}
.hs-p b{display:block;font-size:26px;font-weight:800;letter-spacing:-.02em;color:var(--a)}
.hs-p i{display:block;font-style:normal;font-size:14.5px;font-weight:700;margin:2px 0 8px}
.hs-p span{display:block;font-size:13.5px;line-height:1.6;color:var(--mut)}
.hs-p a{display:inline-block;margin-top:8px;font-size:13.5px;font-weight:700;color:var(--a);
 text-decoration:none;border-bottom:1px solid rgba(103,58,126,.4)}
.hs-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;counter-reset:hs}
.hs-step{counter-increment:hs;border-top:2px solid var(--a);padding-top:12px}
.hs-step::before{content:"0" counter(hs);font-weight:800;font-size:13px;color:var(--a);letter-spacing:.08em}
.hs-step h4{margin:6px 0 6px;font-size:15px;font-weight:700;line-height:1.35}
.hs-step p{margin:0;font-size:13.5px;line-height:1.55;color:var(--mut)}
.hs-quotes{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.hs-q{border:1px solid var(--line);border-radius:16px;padding:20px}
.hs-q blockquote{margin:0 0 12px;font-size:15px;line-height:1.6}
.hs-q figcaption{font-size:13.5px;color:var(--mut)}
.hs-q figcaption b{display:block;color:var(--ink);font-size:14.5px}
.hs-budget{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:8px}
.hs-budget div{border:1px solid var(--line);border-radius:16px;padding:18px 20px}
.hs-budget b{display:block;font-size:22px;font-weight:800;letter-spacing:-.02em;color:var(--a);white-space:nowrap}
.hs-budget span{display:block;margin-top:6px;font-size:13.5px;line-height:1.55;color:var(--mut)}
.hs-faq{display:grid;gap:10px;max-width:860px}
.hs-faq details{border:1px solid var(--line);border-radius:14px;padding:0 20px}
.hs-faq summary{cursor:pointer;list-style:none;position:relative;padding:16px 36px 16px 0;font-size:15.5px;font-weight:700}
.hs-faq summary::-webkit-details-marker{display:none}
.hs-faq summary::after{content:"";position:absolute;right:2px;top:50%;width:11px;height:11px;
 transform:translateY(-70%) rotate(45deg);border-right:2.5px solid var(--a);border-bottom:2.5px solid var(--a);transition:transform .2s}
.hs-faq details[open] summary::after{transform:translateY(-30%) rotate(225deg)}
.hs-faq p{margin:0 0 16px;font-size:14.5px;line-height:1.65;color:var(--mut)}
.hs-more{margin:34px 0 0;font-size:15.5px;line-height:1.7;color:#3d434b}
.hs-more a{color:var(--a);font-weight:700}
@media(max-width:1000px){.hs-dirs,.hs-proof,.hs-quotes,.hs-budget{grid-template-columns:1fr 1fr}
 .hs-steps{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.hs__in{padding:0 18px}.hs{padding:52px 0 44px}
 .hs-dirs,.hs-proof,.hs-quotes,.hs-steps,.hs-budget{grid-template-columns:1fr}}
</style>"""


def esc(t):
    return H.escape(t, quote=False)


def quotes():
    rv = json.load(open(os.path.join(HERE, 'reviews.json'), encoding='utf-8'))
    out = ''
    for k in ('sg_video', 'messe', 'becar_2019'):
        r = rv[k]
        q = r['quote']
        if len(q) > 190:
            q = q[:188].rsplit(' ', 1)[0] + '…'
        out += (f'<figure class="hs-q"><blockquote>«{esc(q)}»</blockquote>'
                f'<figcaption><b>{esc(r["company"])}</b>{esc(r["person"])}, '
                f'{esc(r["role"])}</figcaption></figure>')
    return out


def build(with_css=True, with_ld=True):
    dirs = ''.join(f'<div class="hs-dir"><b><a href="{h}">{esc(t)}</a></b>'
                   f'<span>{esc(d)}</span><em>{esc(price)}</em></div>'
                   for t, h, price, d in LINES)
    proof = ''.join(f'<div class="hs-p"><b>{esc(n)}</b><i>{esc(cap)}</i><span>{esc(txt)}</span>'
                    f'<a href="{href}">Разбор проекта →</a></div>'
                    for n, cap, href, txt in PROOF)
    steps = ''.join(f'<div class="hs-step"><h4>{esc(t)}</h4><p>{esc(d)}</p></div>'
                    for t, d in STEPS)
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
<h2>Рекламное агентство полного цикла в Москве</h2>
<p class="lead">Hand Marketing работает с 2012 года. Мы строим выставочные стенды, проводим
 мероприятия, снимаем рекламу и корпоративные фильмы, делаем мультимедийный контент, фирменный
 стиль и печать. Заказчики приходят не за отдельной услугой, а за результатом на площадке:
 стенд, который отработает восемь месяцев на ВДНХ, фильм, который покажут партнёрам, шоу,
 которое увидит городская площадь.</p>
<p class="lead">С нами работают компании, у которых цена ошибки выше стоимости проекта:
 Samsung, Saint-Gobain, Eaton, РЖД, Messe Düsseldorf, Becar, администрации регионов.
 Для них важно не то, что подрядчик дешевле, а то, что он доведёт работу до конца
 в согласованный срок и в согласованном виде. Поэтому производство мы держим внутри:
 съёмка, графика, дизайн, печать и конструкции делаются нашей командой.</p>

<h3>Направления</h3>
<div class="hs-dirs">{dirs}</div>

<h3>Проекты, по которым нас проверяют</h3>
<p class="lead">Ниже шесть проектов, где масштаб виден по цифрам. У каждого на сайте
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
 <div><b>от 150 000 ₽</b><span>рекламный ролик или корпоративный фильм</span></div>
 <div><b>от 150 000 ₽</b><span>мультимедийная зона на стенде или мероприятии</span></div>
 <div><b>от 500 000 ₽</b><span>мероприятие под ключ</span></div>
 <div><b>от 500 000 ₽</b><span>выставочный стенд под ключ</span></div>
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
            s = s.replace(anchor, build(with_css=(n == 0), with_ld=(n == 0)) + anchor, 1)
            n += 1
        if not n:
            print(f'{os.path.basename(path)}: якорей формы нет — пропуск')
            continue
        open(path, 'w', encoding='utf-8').write(s)
        print(f'{os.path.basename(path)}: секция вставлена в {n} мест(а)')


if __name__ == '__main__':
    main()
