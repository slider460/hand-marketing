#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Текстовая секция на /about и /clients.

Замер 19.09.2026: /about 291 слово старого тильдовского текста про «бизнес-философию,
которую можно охарактеризовать словом прозрачность», /clients 425 слов описаний
компаний без единого слова о том, что мы для них делали. Обе страницы читает
заказчик, который проверяет подрядчика перед тендером или первой встречей.

Позиционирование владельца 20.09.2026: B2B, крупные компании, на сайте они
подтверждают квалификацию. Поэтому доказываем объектами, годами работы
и повторными заказами, а не прилагательными.

    python3 scripts/a2/add_about_seo.py

Секция встаёт перед формой заявки в обе версии вёрстки. Идемпотентен.
"""
import html as H
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
sys.path.insert(0, HERE)

MARK = 'hm-about-seo'
END = '<!-- /hm-about-seo -->'
ANCHORS = ['<section class="mh-form"', '<div id="rec237885363"']

# /about: чем закрываем вопрос «кто вы такие»
ABOUT_FACTS = [
    ('2012', 'год основания агентства', '#673A7E'),
    ('56', 'проектов разобраны на сайте по шагам', '#CF6F19'),
    ('11', 'благодарственных писем со сканами', '#C12164'),
    ('7', 'городов, где мы работали на площадке', '#5E9A2E'),
]

BLOCK_COLORS = ['#673A7E', '#CF6F19', '#C12164', '#8E5FB0', '#5E9A2E']
GROUP_COLORS = ['#CF6F19', '#3B729D', '#8E5FB0', '#5E9A2E', '#C12164']

ABOUT_BLOCKS = [
    ('Что мы делаем',
     'Hand Marketing это рекламное агентство полного цикла. Мы строим выставочные '
     'стенды и делаем для них мультимедиа, проводим мероприятия, снимаем рекламу '
     'и корпоративные фильмы, разрабатываем фирменный стиль, печатаем и производим '
     'конструкции. Заказчик получает не набор услуг, а результат на площадке: '
     'стенд, который отработает сезон, фильм, который покажут партнёрам, шоу, '
     'которое увидит город.'),
    ('Почему производство внутри',
     'Съёмка, монтаж, графика и 3D, дизайн, печать и конструкции делаются нашей '
     'командой. Это не экономия, а управляемость: между этапами нет чужих '
     'подрядчиков, на которых можно сослаться при срыве срока. Когда контент '
     'для экрана считает та же команда, что проектировала экран, на площадке '
     'не приходится подгонять картинку в последнюю ночь.'),
    ('Как заказчик видит работу',
     'Согласование идёт по промежуточным листам, а не по словам «уже почти готово». '
     '79 листов проекта стенда, 31 лист раскадровки ролика для ГАЗ, 79 склеек '
     'в монтажном листе фильма для Eaton: на каждом шаге есть документ, который '
     'можно посмотреть и поправить до того, как работа уйдёт в производство.'),
    ('С кем работаем',
     'Среди заказчиков Samsung, Saint-Gobain, Eaton, РЖД, Messe Düsseldorf, Becar, '
     'Power Technologies, администрации Самарской области и Ставропольского края. '
     'Большинство приходит с одной задачей и остаётся: с Saint-Gobain мы сделали '
     'фильмы, предметную съёмку, календарь и печатные материалы, с Eaton ролики, '
     'конференцию в Алматы и онлайн-трансляцию, с Becar десяток проектов '
     'от брошюр до выставочного стенда.'),
    ('Где работаем',
     'Офис в Москве, на Рочдельской. Проекты вели в Москве и области, Самаре, '
     'Ставрополе, Уфе, Калининграде, Санкт-Петербурге и Алматы. Логистику, монтаж '
     'и работу с местными службами берём на себя, отдельного подрядчика в чужом '
     'городе искать не нужно.'),
]

# /clients: клиенты по отраслям и что для них сделано
CLIENT_GROUPS = [
    ('Промышленность и производство',
     'Saint-Gobain, Eaton, OBO Bettermann, CeramicaNova, Изотек, AnVIT',
     'Корпоративные фильмы и обучающее видео, предметная съёмка каталогов, '
     '3D-визуализация оборудования, печатные материалы и выставочные стенды. '
     'Для Saint-Gobain сняли фильм о клиентском опыте и 63 позиции продукции '
     'за одну смену, для Eaton сделали ролики, конференцию и онлайн-трансляцию.'),
    ('Транспорт и инфраструктура',
     'РЖД, ГАЗ, УАЗ, Power Technologies, Silk Way Rally',
     'Фильм к десятилетию Центральной дирекции РЖД на 117 планов, рекламные ролики '
     'для ГАЗ и УАЗ, фильм об энергоснабжении чемпионата мира в 11 городах, '
     '3D-визуализация маршрута ралли на 5 947 км.'),
    ('Недвижимость и торговые центры',
     'Becar Asset Management, МФК «Саларис», ТРЦ «Мозаика», ТРЦ «Ривьера», MMG',
     'Презентационные ролики объектов, вечера для арендаторов, брошюры и сайты '
     'продуктов, выставочный стенд на Private Money Expo Forum. Для Becar '
     'за несколько лет сделали больше десяти проектов.'),
    ('Регионы и государственные структуры',
     'Правительство Самарской области, Ставропольский край, Музей им. Алабина',
     'Стенды на выставке-форуме «Россия» на ВДНХ, фирменный стиль выставки, '
     '3D-шоу на фасаде Правительства края, мультимедийная экспозиция в музее.'),
    ('Бренды и медиа',
     'Samsung, Changan, VIVAX, Teoxane, Marie Claire, Hearst Shkulev Media, '
     'Messe Düsseldorf',
     'Новогодние мероприятия и презентации, рекламные ролики со съёмкой '
     'медийных лиц, ключевые визуалы кампаний, кросс-мероприятия с изданиями '
     'и обзорные ролики выставок.'),
]

PAGES = {
    'about': dict(
        tag='Агентство с 2012 года',
        h2='Агентство Hand Marketing: чем занимаемся и как работаем',
        lead='Мы работаем с 2012 года и делаем проекты, которые видно на площадке: '
             'выставочные стенды, мероприятия, ролики, мультимедийный контент, '
             'фирменный стиль и печать. Ниже без прилагательных: что именно делаем, '
             'как устроена работа и кто уже проверил это на своих задачах.',
        blocks=ABOUT_BLOCKS, facts=ABOUT_FACTS, groups=None,
        tail='Проекты разобраны в <a href="/project">портфолио</a>, письма заказчиков '
             'со сканами лежат на странице <a href="/reviews/">отзывов</a>, состав '
             'команды на странице <a href="/team/">команды</a>, порядок расчёта '
             'на странице <a href="/price/">стоимости</a>.'),
    'clients': dict(
        tag='Кто с нами работает',
        h2='Клиенты агентства: кто и с какими задачами приходит',
        lead='С нами работают промышленные компании, транспортные холдинги, '
             'девелоперы, торговые центры, региональные администрации и бренды. '
             'Ниже отрасли, конкретные компании и то, что мы для них делали.',
        blocks=None, facts=None, groups=CLIENT_GROUPS,
        tail='Разборы проектов с цифрами лежат в <a href="/project">портфолио</a>, '
             'благодарственные письма на странице <a href="/reviews/">отзывов</a>. '
             'Если задача похожа на одну из перечисленных, напишите: посчитаем '
             'и покажем, как делали у других.'),
}

CSS = """<style id="hm-about-seo-css">
/* те же приёмы, что в секции главной: цветной тег с квадратом, радиус 24,
   мягкая тень, цветные акценты по палитре направлений */
.ab{--ink:#14171C;--mut:#5A616A;--a:#673A7E;--line:#ECEEF2;
 font-family:'Montserrat',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff;
 padding:76px 0 68px;border-top:1.5px solid var(--line)}
.ab *{box-sizing:border-box}
.ab__in{max-width:1180px;margin:0 auto;padding:0 40px}
.ab__tag{display:inline-flex;align-items:center;gap:9px;font-size:11px;font-weight:800;
 letter-spacing:.2em;text-transform:uppercase;color:var(--a);margin-bottom:12px}
.ab__tag::before{content:"";width:11px;height:11px;border-radius:3px;background:currentColor}
.ab h2{margin:0 0 14px;font-size:clamp(26px,3.1vw,38px);font-weight:800;letter-spacing:-.02em;line-height:1.1}
.ab p.lead{margin:0 0 30px;max-width:74ch;font-size:16.5px;line-height:1.7;color:#3d434b}
.ab-facts{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:0 0 36px}
.ab-facts div{background:#fff;border:1.5px solid var(--line);border-radius:24px;padding:22px 24px;
 box-shadow:0 14px 30px -22px rgba(20,23,28,.5)}
.ab-facts div i{display:block;width:40px;height:6px;border-radius:3px;background:var(--c);margin-bottom:14px}
.ab-facts div b{display:block;font-size:30px;font-weight:900;letter-spacing:-.02em;color:var(--c)}
.ab-facts div span{display:block;margin-top:6px;font-size:13.5px;line-height:1.5;color:var(--mut)}
.ab-blocks{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.ab-b{position:relative;background:#fff;border:1.5px solid var(--line);border-radius:24px;
 padding:24px 26px;box-shadow:0 14px 30px -22px rgba(20,23,28,.5)}
.ab-b h3{margin:0 0 10px;font-size:19px;font-weight:800;letter-spacing:-.01em;
 display:flex;align-items:center;gap:12px}
.ab-b h3::before{content:"";width:11px;height:11px;border-radius:3px;background:var(--c);flex:none}
.ab-b p{margin:0;font-size:15px;line-height:1.68;color:var(--mut)}
.ab-groups{display:grid;gap:18px}
.ab-g{position:relative;background:#fff;border:1.5px solid var(--line);border-radius:24px;
 padding:24px 28px;box-shadow:0 14px 30px -22px rgba(20,23,28,.5);
 border-left:6px solid var(--c)}
.ab-g h3{margin:0 0 6px;font-size:20px;font-weight:800;letter-spacing:-.01em}
.ab-g em{display:block;margin-bottom:10px;font-style:normal;font-size:13.5px;font-weight:800;
 letter-spacing:.04em;color:var(--c)}
.ab-g p{margin:0;font-size:15px;line-height:1.68;color:var(--mut);max-width:92ch}
.ab-tail{margin:34px 0 0;font-size:15.5px;line-height:1.7;color:#3d434b;max-width:82ch}
.ab-tail a{color:var(--a)!important;font-weight:700}
@media(max-width:1000px){.ab-facts{grid-template-columns:1fr 1fr}.ab-blocks{grid-template-columns:1fr}}
@media(max-width:640px){.ab__in{padding:0 18px}.ab{padding:52px 0 44px}.ab-facts{grid-template-columns:1fr}}
</style>"""


def esc(t):
    return H.escape(t, quote=False)


def build(slug, with_css=True):
    p = PAGES[slug]
    facts = ''
    if p['facts']:
        facts = ('<div class="ab-facts">' + ''.join(
            f'<div style="--c:{c}"><i aria-hidden="true"></i><b>{esc(n)}</b>'
            f'<span>{esc(t)}</span></div>' for n, t, c in p['facts']) + '</div>')
    body = ''
    if p['blocks']:
        body = ('<div class="ab-blocks">' + ''.join(
            f'<div class="ab-b" style="--c:{BLOCK_COLORS[i % len(BLOCK_COLORS)]}">'
            f'<h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
            for i, (t, d) in enumerate(p['blocks'])) + '</div>')
    if p['groups']:
        body = ('<div class="ab-groups">' + ''.join(
            f'<div class="ab-g" style="--c:{GROUP_COLORS[i % len(GROUP_COLORS)]}">'
            f'<h3>{esc(t)}</h3><em>{esc(who)}</em><p>{esc(d)}</p></div>'
            for i, (t, who, d) in enumerate(p['groups'])) + '</div>')
    return (f'<!-- {MARK} -->{CSS if with_css else ""}'
            f'<section class="ab" aria-label="Об агентстве">'
            f'<div class="ab__in">'
            f'<span class="ab__tag">{esc(p["tag"])}</span><h2>{esc(p["h2"])}</h2>'
            f'<p class="lead">{esc(p["lead"])}</p>{facts}{body}'
            f'<p class="ab-tail">{p["tail"]}</p>'
            f'</div></section>{END}')


def strip_old(s):
    while True:
        i = s.find(f'<!-- {MARK}')
        if i < 0:
            return s
        j = s.find(END, i)
        j = j + len(END) if j >= 0 else s.find('</section>', i) + len('</section>')
        s = s[:i] + s[j:]


def main():
    for slug in PAGES:
        for name in ('index-a2.html', 'index.html'):
            path = os.path.join(ROOT, slug, name)
            if not os.path.isfile(path):
                continue
            s = strip_old(open(path, encoding='utf-8').read())
            n = 0
            # стиль отдаём ОБЕИМ копиям вёрстки: в тильдовской десктопной версии
            # свои правила для ссылок, и без нашего <style> заголовки красятся
            # фирменным коралловым. Дубль <style> с тем же id безвреден,
            # дубль JSON-LD нет, поэтому разметка идёт только в первую вставку
            for anchor in ANCHORS:
                if anchor not in s:
                    continue
                s = s.replace(anchor, build(slug, with_css=True) + anchor, 1)
                n += 1
            if not n:
                print(f'/{slug}/{name}: якорей формы нет — пропуск')
                continue
            open(path, 'w', encoding='utf-8').write(s)
            print(f'/{slug}/{name}: секция вставлена в {n} мест(а)')


if __name__ == '__main__':
    main()
