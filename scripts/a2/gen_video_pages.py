#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит три посадочные страницы видеопродакшна:

    mirror/videoproduction/reklamnyy-rolik/index.html      — рекламный ролик
    mirror/videoproduction/korporativnyy-film/index.html   — корпоративный фильм
    mirror/videoproduction/prezentacionnyy-rolik/index.html — презентационный ролик объекта

Почему именно эти три и почему не другие (Вордстат, Москва, сентябрь 2026):
  съёмка рекламного ролика 76, заказать рекламный ролик 53, производство роликов 23;
  корпоративное видео 255, корпоративный фильм 197, фильм о компании 123;
  презентационный ролик 123, имиджевый ролик 177.
Проверено и отброшено по интенту: «обучающее видео» 6395 (школьные уроки и взрослый
контент), «вирусный ролик» 447 (статьи «как снять вирусное»), «видео для маркетплейса» 235
(в топе съёмка от 2000 ₽, другой покупатель). Виральный формат и селебрити живут блоками
внутри страницы рекламного ролика.

Факты владельца 19.09.2026: цена от 150 000 ₽, экспресс за неделю, полноценный ролик
2–3 недели, снимаем по России и за рубежом, техника и операторы свои. Имена руководителей
клиентов в текстах не называем.

Сигнатурная механика: полоса хронометража (длина шкалы пропорциональна длительности
ролика, подписи с фактами). На сайте такого блока ещё не было.

Правки: ТОЛЬКО через этот скрипт.
Прогон: python3 scripts/a2/finalize_page.py gen_video_pages.py
"""
import html as H
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import commerce_block as cb  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
spec = importlib.util.spec_from_file_location('rc', os.path.join(HERE, 'react-chrome.py'))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

SITE = 'https://hand-marketing.ru'
IMG = '/images'

PAGES = {
    'ad': dict(
        out=('videoproduction', 'reklamnyy-rolik'),
        key='ad', kicker='Video Production · Реклама',
        title='Съёмка рекламного ролика под ключ в Москве | Hand Marketing',
        descr=('Съёмка рекламного ролика под ключ: идея и сценарий, съёмка своей группой, '
               'графика и 3D, монтаж. Ролики для УАЗ, ГАЗ, Eaton и VIVAX. От 150 000 ₽.'),
        h1='Съёмка рекламного ролика',
        lead=('Снимаем рекламу, которую досматривают до конца: 60 секунд про блокировку '
              'дифференциала для УАЗ Патриот, 49 секунд с Настасьей Самбурской для VIVAX SPORT '
              'и 1:42 «Газели-трансформера», которую пересылали друг другу сами.'),
        hero=f'{IMG}/vpg/ad-hero.jpg',
        hero_alt='Кадр рекламного ролика УАЗ Патриот на бездорожье',
        loop='/media/ad-hero-loop.mp4',
        shots_h2='Кадры из наших рекламных роликов',
        shots_lead='Три ролика, три разных задачи: показать работу узла, показать '
                   'средство в деле и заставить переслать ролик дальше.',
        shots=[('ad/patriot-mud.jpg', 'УАЗ Патриот: три съёмочные смены на бездорожье'),
               ('ad/patriot-ford.jpg', 'Брод сняли с воды и с берега, чтобы показать глубину'),
               ('ad/patriot-diff.jpg', 'Разрез дифференциала собран графикой поверх съёмки'),
               ('ad/gaz-robot.jpg', 'Трансформер нарисован по сториборду на 31 лист'),
               ('ad/gaz-street.jpg', 'Реакцию прохожих и пассажиров снимали отдельной сменой'),
               ('ad/vivax-gym.jpg', 'VIVAX SPORT: тренировка в зале, один съёмочный день'),
               ('ad/vivax-apply.jpg', 'Продукт входит в кадр по ходу тренировки, без пауз'),
               ],
        chips=['от 150 000 ₽', 'экспресс за неделю', 'съёмка по России и за рубежом'],
        bar_h2='Три ролика и их хронометраж',
        bar_lead='Длина полосы пропорциональна длительности ролика.',
        bars=[
            ('УАЗ Патриот и Eaton', 60, '/video/patriot/',
             'Реклама одной опции в прайсе: блокировки дифференциала. Три смены на бездорожье, '
             'живой разрез узла в графике.'),
            ('VIVAX SPORT', 49, '/video/vivax/',
             'Три средства линейки внутри одной тренировки, в кадре Настасья Самбурская. '
             'Съёмка в зале, разрез мышцы графикой.'),
            ('«Газель-трансформер», ГАЗ и Eaton', 102, '/video/gaz/',
             'Вирусный формат: сториборд на 31 лист, четыре смены. Ролик рекламирует '
             'не машину, а одну опцию.'),
        ],
        cards_h2='Кейсы рекламных роликов',
        cards=[
            ('/video/patriot/', f'{IMG}/patriot/poster.jpg', 'УАЗ Патриот и Eaton, 60 секунд',
             'Рекламный ролик про блокировку дифференциала: три съёмочные смены на бездорожье '
             'и разрез узла в графике.', 'Кадр рекламного ролика УАЗ Патриот'),
            ('/video/vivax/', f'{IMG}/vivax/set-wide.jpg', 'VIVAX SPORT, 0:49',
             'Ролик со звездой: три средства линейки показаны внутри одной тренировки, '
             'без пауз на демонстрацию упаковки.', 'Съёмочная площадка ролика VIVAX SPORT в зале'),
            ('/video/gaz/', f'{IMG}/gaz/poster.jpg', '«Газель-трансформер», 1:42',
             'Вирусный ролик для ГАЗ и Eaton, который перезаливали в сети с 2013 по 2025 год.',
             'Кадр вирусного ролика «Газель-трансформер»'),
        ],
        lists=[
            ('Что входит в работу',
             [('Идея и сценарий', 'Раскадровка и смета до съёмок, две итерации правок включены.'),
              ('Съёмка', 'Своя группа, операторы и техника. Локации, кастинг, реквизит.'),
              ('Графика и 3D', 'Разрезы, схемы работы узла, титры и анимация.'),
              ('Музыка и озвучка', 'Подбор музыки с правами, дикторы, звуковое оформление.'),
              ('Версии под площадки', 'ТВ-эфир, сайт, экран мероприятия, вертикаль для соцсетей.'),
              ('Права и сдача', 'Мастер-файл и версии, исходники по договорённости.')]),
            ('Форматы, которые мы снимали',
             [('Реклама продукта', 'Показываем, как работает вещь, а не рассказываем о ней.'),
              ('Ролик со звездой или блогером', 'Съёмка с медийным лицом, как с Самбурской для VIVAX.'),
              ('Вирусный формат', 'Ход, ради которого ролик пересылают, как «Газель-трансформер».'),
              ('Ролик для выставки и стенда', 'Короткая петля под экран, читается без звука.')]),
        ],
        faq=[
            ('Сколько стоит съёмка рекламного ролика?',
             'От 150 000 ₽. Итог зависит от хронометража, числа съёмочных дней, графики и прав '
             'на музыку. После брифа бесплатно готовим смету в двух вариантах.'),
            ('Сколько времени занимает производство?',
             'Экспресс-формат снимаем и отдаём за неделю. Полноценный рекламный ролик занимает '
             '2–3 недели от брифа до мастера, в зависимости от графики и согласований.'),
            ('Где вы снимаете?',
             'По всей России и за рубежом: где снимать, для нас роли не играет. Снимали в Москве, '
             'Самаре, Ставрополе и Алматы.'),
            ('Можно ли снять ролик с известным человеком?',
             'Да. Для VIVAX SPORT снимали с Настасьей Самбурской: подбор, согласование съёмочного '
             'дня и права на использование берём на себя.'),
            ('Что получим на выходе?',
             'Мастер-файл и версии под площадки: ТВ-эфир, сайт, экран мероприятия и вертикаль '
             'для соцсетей.'),
        ]),

    'film': dict(
        out=('videoproduction', 'korporativnyy-film'),
        key='film', kicker='Video Production · Фильм о компании',
        title='Корпоративный фильм о компании: съёмка под ключ | Hand Marketing',
        descr=('Корпоративный фильм о компании под ключ: сценарий, съёмка своими операторами, '
               'графика и монтаж. Фильмы для РЖД, Saint-Gobain, Power Technologies. От 150 000 ₽.'),
        h1='Корпоративный фильм о компании',
        lead=('Фильм к десятилетию дирекции РЖД, фильм о клиентском опыте Saint-Gobain, фильм '
              'об энергоснабжении чемпионата мира по футболу. Снимаем то, что компания хочет '
              'показывать партнёрам, сотрудникам и на тендере.'),
        hero=f'{IMG}/vpg/film-hero.jpg',
        hero_alt='Кадр корпоративного фильма: грузовой двор Центральной дирекции РЖД',
        loop='/media/film-hero-loop.mp4',
        shots_h2='Кадры из корпоративных фильмов',
        shots_lead='Производство, объекты и люди компании: снимаем в рабочую смену, '
                   'без перекрытия площадки и без постановочных сцен.',
        shots=[('film/rzd-yard.jpg', 'Грузовой двор ЦМ РЖД снят с воздуха'),
               ('film/rzd-crane.jpg', 'Портальный кран в работе, смену не останавливали'),
               ('film/rzd-air.jpg', 'Съёмка шла в нескольких городах сети дирекции'),
               ('film/sg-wall.jpg', 'Saint-Gobain: 48 сотрудников сняты в одном свете'),
               ('film/sg-line.jpg', 'Линия упаковки: производство в рабочую смену'),
               ('film/pt-gallery.jpg', 'Международный вещательный центр чемпионата мира'),
               ('film/pt-numbers.jpg', 'Цифры проекта: 960 км кабеля, 75 МВт, 300 человек'),
               ('film/isotec-plant.jpg', 'Изотек: цех и склад в бренд-фильме компании'),
               ],
        chips=['от 150 000 ₽', '2–3 недели', 'съёмка по России и за рубежом'],
        bar_h2='Сколько длится корпоративный фильм',
        bar_lead='Хронометраж наших фильмов: полоса пропорциональна длительности.',
        bars=[
            ('Power Technologies, ЧМ-2018', 699, '/video/powertechnologies/',
             '11 городов и 12 стадионов, восемь интервью. Есть короткая версия на 4:27 '
             'для показа на стенде и встречах.'),
            ('Saint-Gobain, клиентский опыт', 607, '/video/saintgobain/cx/',
             'Две части по 6:57 и 3:11: путь заказа от завода до объекта и прямая речь команды.'),
            ('ЦМ РЖД, фильм к десятилетию', 234, '/video/rgd/history/',
             '117 планов, семь услуг дирекции и съёмка в нескольких городах.'),
        ],
        cards_h2='Кейсы корпоративных фильмов',
        cards=[
            ('/video/rgd/history/', f'{IMG}/rgd-history/poster.jpg', 'ЦМ РЖД, 3:54',
             'Фильм к десятилетию Центральной дирекции: 117 планов, грузовые дворы и семь услуг '
             'в одном рассказе.', 'Кадр фильма для Центральной дирекции РЖД'),
            ('/video/saintgobain/cx/', f'{IMG}/sgcx/hero-poster.jpg', 'Saint-Gobain, 10 минут',
             'Фильм о клиентском опыте в двух частях: путь заказа, производство и прямая речь '
             'сотрудников компании.', 'Кадр фильма о клиентском опыте Saint-Gobain'),
            ('/video/powertechnologies/', f'{IMG}/powertech/poster-full.jpg',
             'Power Technologies, ЧМ-2018',
             'Фильм о работе на чемпионате мира: 11 городов, 12 стадионов и восемь интервью. '
             'Полная версия 11:39 и короткая на 4:27.',
             'Кадр фильма Power Technologies о чемпионате мира'),
            ('/isotec/', f'{IMG}/isotec/poster.jpg', 'Изотек, бренд-фильм',
             'История компании от 2012 года до сегодняшнего дня, две версии под разные площадки.',
             'Кадр бренд-фильма компании Изотек'),
        ],
        lists=[
            ('Какие фильмы снимаем',
             [('К юбилею и итогам года', 'История компании и результаты в одном рассказе.'),
              ('О производстве', 'Как устроен процесс: цеха, техника, люди на площадке.'),
              ('О клиентском опыте', 'Путь заказа глазами клиента и сотрудников.'),
              ('HR-фильм', 'Для найма и адаптации: кто работает в компании и как.'),
              ('Для выставки и стенда', 'Версия под экран: читается без звука, идёт петлёй.'),
              ('Для тендера и инвесторов', 'Сжатая версия с цифрами и объектами.')]),
            ('Как проходит работа',
             [('Бриф и сценарий', 'Цели, аудитория, герои. Сценарий и смета до съёмок.'),
              ('Подготовка', 'Локации, согласования на объектах, график смен.'),
              ('Съёмка', 'Своя группа и техника, интервью и съёмка процессов.'),
              ('Постпродакшн', 'Монтаж, цвет, графика, звук. Две итерации правок включены.'),
              ('Версии', 'Полный фильм, короткая версия, нарезка для соцсетей.'),
              ('Где живёт фильм', 'Экран на стенде, зал мероприятия, сайт, внутренние экраны.')]),
        ],
        faq=[
            ('Сколько стоит корпоративный фильм?',
             'От 150 000 ₽. Итог зависит от хронометража, числа съёмочных дней и графики. '
             'Смету в двух вариантах готовим бесплатно после брифа.'),
            ('Сколько времени занимает производство фильма?',
             'Экспресс-формат снимаем за неделю, полноценный фильм занимает 2–3 недели от брифа '
             'до мастера.'),
            ('Кто пишет сценарий?',
             'Мы. После брифа предлагаем сюжет и структуру, согласуем до съёмок, чтобы на площадке '
             'не переделывать.'),
            ('Снимаете ли вы в других городах?',
             'Да. Снимаем по всей России и за рубежом, география значения не имеет.'),
            ('Что получим на выходе?',
             'Мастер-файл фильма, короткую версию и нарезки под площадки: стенд, зал, сайт '
             'и соцсети.'),
        ]),

    'obj': dict(
        out=('videoproduction', 'prezentacionnyy-rolik'),
        key='obj', kicker='Video Production · Объекты',
        title='Презентационный ролик объекта под ключ | Hand Marketing',
        descr=('Презентационный ролик объекта: торговый центр, технопарк, площадка. Съёмка, '
               'графика, аэросъёмка и монтаж. Ролики для ТРЦ «Мозаика», МФК «Саларис», MMG. '
               'От 150 000 ₽.'),
        h1='Презентационный ролик объекта',
        lead=('Ролик, который показывают арендаторам, инвесторам и городу. Снимали торговые '
              'центры, многофункциональные комплексы и технопарки: объект, трафик, зоны '
              'и цифры в одном рассказе.'),
        hero=f'{IMG}/vpg/obj-hero.jpg',
        hero_alt='Кадр презентационного ролика торгового центра «Мозаика» с воздуха',
        loop='/media/obj-hero-loop.mp4',
        shots_h2='Кадры из роликов об объектах',
        shots_lead='Объект с воздуха и изнутри, зона охвата и цифры: то, что арендатор '
                   'и инвестор хотят увидеть до встречи.',
        shots=[('obj/mozaika-air.jpg', 'ТРЦ «Мозаика»: 68 000 м² торговой площади'),
               ('obj/mozaika-gallery.jpg', 'Галереи снимали в рабочие часы, центр не закрывали'),
               ('obj/mozaika-link.jpg', 'Переход в жилую часть квартала'),
               ('obj/salaris-scheme.jpg', 'Зона охвата «Салариса» вдоль Киевского шоссе'),
               ('obj/salaris-site.jpg', 'Стройка 310 000 м²: съёмка с земли и с воздуха'),
               ('obj/mmg-air.jpg', 'Павелецкая площадь: объект в центре Москвы'),
               ('obj/mmg-reach.jpg', 'Зона охвата: более 3 млн человек в 15–20 минутах'),
               ('obj/zubovo-map.jpg', 'Технопарк «Зубово» в 40 км от Уфы'),
               ('obj/zubovo-plan.jpg', 'Схема площадки: подстанция, котельная, водозабор'),
               ],
        chips=['от 150 000 ₽', '2–3 недели', 'съёмка по России и за рубежом'],
        bar_h2='Хронометраж роликов об объектах',
        bar_lead='Чем сложнее объект, тем длиннее рассказ. Полоса пропорциональна длительности.',
        bars=[
            ('ТРЦ «Мозаика»', 271, '/video/mozaika/',
             '13 синхронов с арендаторами и руководителями, рост арендопригодной площади в графике.'),
            ('МФК «Саларис», ролик об объекте', 178, '/video/salaris/',
             'Объект и зона охвата: трасса, транспорт, 105 000 м² в схеме.'),
            ('МФК «Саларис», ролик об аудитории', 153, '/video/salaris/',
             'Второй ролик под другую аудиторию: посетители и сценарии визита.'),
        ],
        cards_h2='Кейсы роликов об объектах',
        cards=[
            ('/video/mozaika/', f'{IMG}/mozaika-video/poster.jpg', 'ТРЦ «Мозаика», 4:31',
             'Фильм о комплексе для арендаторов: 13 синхронов, цифры по трафику и аренде.',
             'Кадр ролика о торговом центре «Мозаика»'),
            ('/video/salaris/', f'{IMG}/salaris-video/poster-1.jpg', 'МФК «Саларис», два ролика',
             'Объект и аудитория разведены в два ролика: 2:58 и 2:33, зона охвата и трафик.',
             'Кадр ролика о многофункциональном комплексе «Саларис»'),
            ('/mmg/', f'{IMG}/mmg/poster.jpg', '«Павелецкая Плаза», MMG',
             'Ролик под задачи лизинга: трафик площади, зоны охвата, интервью архитектора '
             'и арендаторов.', 'Кадр ролика о торговом центре «Павелецкая Плаза»'),
            ('/zubovo/', f'{IMG}/zubovo/poster.jpg', 'Технопарк «Зубово»',
             'Презентация площадки для резидентов и инвесторов: инфраструктура и земельный баланс.',
             'Кадр презентационного ролика технопарка «Зубово»'),
        ],
        lists=[
            ('Кому показывают такой ролик',
             [('Арендаторам', 'Трафик, зоны, соседи по галерее и условия входа.'),
              ('Инвесторам', 'Масштаб объекта, стадия готовности, экономика в цифрах.'),
              ('Городу и администрации', 'Что объект даёт территории и людям.'),
              ('Посетителям', 'Отдельная версия под аудиторию, как второй ролик «Саларис».')]),
            ('Что входит',
             [('Съёмка объекта', 'Интерьеры, фасады, потоки людей, работа в смену.'),
              ('Аэросъёмка', 'Объект в окружении: транспорт, подъезды, зона охвата.'),
              ('Графика и цифры', 'Схемы зон, площади, трафик и динамика в инфографике.'),
              ('Интервью', 'Руководители, арендаторы, архитектор.'),
              ('Версии', 'Полная версия для встречи и короткая для рассылки.')]),
        ],
        faq=[
            ('Сколько стоит презентационный ролик объекта?',
             'От 150 000 ₽. Итог зависит от хронометража, числа смен, аэросъёмки и графики. '
             'Смету готовим бесплатно после брифа.'),
            ('Сколько времени занимает съёмка?',
             'Экспресс-формат за неделю, полноценный ролик 2–3 недели. Съёмку объекта планируем '
             'так, чтобы не мешать работе площадки.'),
            ('Нужно ли закрывать объект на время съёмки?',
             'Нет. Торговые центры мы снимали в рабочие часы, а технические кадры делали до '
             'открытия и после закрытия.'),
            ('Можно ли сделать несколько версий под разные аудитории?',
             'Да. Для МФК «Саларис» сняли два ролика: один про объект для арендаторов, второй '
             'про сценарии визита для посетителей.'),
            ('Снимаете ли вы объекты в других городах?',
             'Да, по всей России и за рубежом. Снимали в Москве, Самаре, Ставрополе, Уфе '
             'и Ташкентской области.'),
        ]),
}

CSS = """<style>
.vpg{--a:#CF6F19;font-family:'Montserrat',Arial,sans-serif;color:#14171C;background:#fff}
.vpg__in{max-width:1180px;margin:0 auto;padding:0 40px}
.vpg-sec{padding:clamp(46px,5.6vw,80px) 0}
.vpg-sec_alt{background:#FBF7F3}
.vpg-sec__h{margin:0 0 10px;font-size:clamp(26px,3.1vw,40px);font-weight:800;letter-spacing:-.02em;line-height:1.1}
.vpg-sec__lead{margin:0 0 30px;max-width:72ch;font-size:16.5px;line-height:1.65;color:#5A616A}
.vpg-hero{position:relative;min-height:clamp(380px,56vh,560px);display:flex;align-items:flex-end;color:#fff;overflow:hidden}
.vpg-hero__img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.vpg-hero__sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,10,6,.52) 0%,rgba(14,10,6,.42) 38%,rgba(14,10,6,.9) 100%)}
.vpg-hero__v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .8s ease;pointer-events:none}
.vpg-hero__v.is-on{opacity:1}
.vpg-shots{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}
.vpg-shot{position:relative;margin:0;border-radius:14px;overflow:hidden;background:#EFE9E3;grid-column:span 2}
.vpg-shot:first-child,.vpg-shot:nth-child(2){grid-column:span 3}
.vpg-shot img{width:100%;height:100%;aspect-ratio:16/9;object-fit:cover;display:block}
.vpg-shot figcaption{position:absolute;left:0;right:0;bottom:0;padding:26px 16px 12px;font-size:13.5px;line-height:1.45;color:#fff;background:linear-gradient(180deg,rgba(14,10,6,0),rgba(14,10,6,.82))}
@media(max-width:980px){.vpg-shots{grid-template-columns:repeat(2,1fr)}.vpg-shot,.vpg-shot:first-child,.vpg-shot:nth-child(2){grid-column:span 1}}
@media(max-width:640px){.vpg-shots{grid-template-columns:1fr}}
.vpg-hero__in{position:relative;width:100%;max-width:1180px;margin:0 auto;padding:0 40px clamp(34px,4.6vw,60px)}
.vpg-hero__k{margin:0 0 14px;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#F6C99A}
.vpg-hero h1{margin:0;font-size:clamp(28px,4.2vw,54px);font-weight:800;letter-spacing:-.025em;line-height:1.06;max-width:19ch}
.vpg-hero__lead{margin:18px 0 0;max-width:62ch;font-size:clamp(15.5px,1.5vw,18px);line-height:1.6;color:rgba(255,255,255,.88)}
.vpg-hero__f{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 0;padding:0;list-style:none}
.vpg-hero__f li{border:1px solid rgba(255,255,255,.35);border-radius:30px;padding:9px 18px;font-size:14px;font-weight:600}
.vpg-hero__cta{display:inline-block;margin-top:24px;background:#FCB724;color:#14171C;font-weight:800;font-size:15.5px;padding:15px 34px;border-radius:30px;text-decoration:none}
.vpg-crumbs{font-size:13px;color:#8A9099;padding:18px 0 0}
.vpg-crumbs a{color:#8A9099;text-decoration:none}
.vpg-crumbs a:hover{text-decoration:underline}
.vpg-bars{display:grid;gap:22px}
.vpg-bar__top{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;margin-bottom:8px}
.vpg-bar__n{font-size:17px;font-weight:700;letter-spacing:-.01em}
.vpg-bar__n a{color:inherit;text-decoration:none;border-bottom:1px solid rgba(207,111,25,.45)}
.vpg-bar__t{font-size:15px;font-weight:800;color:var(--a);font-variant-numeric:tabular-nums}
.vpg-bar__line{height:14px;border-radius:7px;background:rgba(207,111,25,.14);overflow:hidden}
.vpg-bar__fill{height:100%;border-radius:7px;background:var(--a)}
.vpg-bar__d{margin:10px 0 0;font-size:14.5px;line-height:1.6;color:#5A616A;max-width:74ch}
.vpg-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(252px,1fr));gap:20px}
.vpg-card{display:flex;flex-direction:column;border:1px solid rgba(20,23,28,.1);border-radius:20px;overflow:hidden;text-decoration:none;color:inherit;background:#fff;transition:transform .2s ease}
.vpg-card:hover{transform:translateY(-4px)}
.vpg-card img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.vpg-card__b{padding:18px 20px 22px;display:flex;flex-direction:column;gap:8px;flex:1}
.vpg-card__t{font-size:18px;font-weight:800;letter-spacing:-.01em}
.vpg-card__d{font-size:14.5px;line-height:1.6;color:#5A616A}
.vpg-card__go{margin-top:auto;font-size:14px;font-weight:700;color:var(--a)}
.vpg-list{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.vpg-list__i{border-top:2px solid var(--a);padding:14px 0 0}
.vpg-list__i b{display:block;font-size:16px;margin-bottom:6px}
.vpg-list__i span{font-size:14.5px;line-height:1.55;color:#5A616A}
.vpg-faq{display:grid;gap:10px;max-width:860px}
.vpg-faq__i{border:1px solid rgba(20,23,28,.1);border-radius:14px;padding:0 20px}
.vpg-faq__i summary{cursor:pointer;list-style:none;position:relative;padding:16px 36px 16px 0;font-size:15.5px;font-weight:700}
.vpg-faq__i summary::-webkit-details-marker{display:none}
.vpg-faq__i summary::after{content:"";position:absolute;right:2px;top:50%;width:11px;height:11px;transform:translateY(-70%) rotate(45deg);border-right:2.5px solid var(--a);border-bottom:2.5px solid var(--a);transition:transform .2s}
.vpg-faq__i[open] summary::after{transform:translateY(-30%) rotate(225deg)}
.vpg-faq__i p{margin:0 0 16px;font-size:14.5px;line-height:1.65;color:#5A616A}
@media(max-width:980px){.vpg-cards,.vpg-list{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){.vpg__in,.vpg-hero__in{padding-left:18px;padding-right:18px}.vpg-cards,.vpg-list{grid-template-columns:minmax(0,1fr)}}
</style>"""

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px" alt=""></div></noscript>')


def esc(s):
    return H.escape(s, quote=False)


def mmss(sec):
    return f'{sec // 60}:{sec % 60:02d}' if sec >= 60 else f'0:{sec:02d}'


def hero(p):
    chips = ''.join(f'<li>{esc(c)}</li>' for c in p['chips'])
    return (
        '<section class="vpg-hero">'
        f'<img class="vpg-hero__img" src="{p["hero"]}" alt="{esc(p["hero_alt"])}" '
        'fetchpriority="high" decoding="async">'
        f'<video class="vpg-hero__v" autoplay muted loop playsinline preload="metadata" '
        f'aria-hidden="true"><source src="{p["loop"]}" type="video/mp4"></video>'
        '<span class="vpg-hero__sh" aria-hidden="true"></span>'
        '<div class="vpg-hero__in">'
        f'<p class="vpg-hero__k">{esc(p["kicker"])}</p>'
        f'<h1>{esc(p["h1"])}</h1>'
        f'<p class="vpg-hero__lead">{esc(p["lead"])}</p>'
        f'<ul class="vpg-hero__f">{chips}</ul>'
        '<a class="vpg-hero__cta" href="#lead">Обсудить проект</a>'
        '</div></section>')


def crumbs(p):
    return ('<div class="vpg__in"><nav class="vpg-crumbs" aria-label="Навигация по разделам">'
            '<a href="/">Главная</a> · <a href="/videoproduction/">Видеопродакшн</a> · '
            f'{esc(cb.PAGES[p["key"]]["crumb"])}</nav></div>')


def bars(p):
    top = max(sec for _n, sec, _h, _d in p['bars'])
    rows = ''
    for name, sec, href, text in p['bars']:
        w = round(sec / top * 100)
        rows += (f'<div class="vpg-bar"><div class="vpg-bar__top">'
                 f'<span class="vpg-bar__n"><a href="{href}">{esc(name)}</a></span>'
                 f'<span class="vpg-bar__t">{mmss(sec)}</span></div>'
                 f'<div class="vpg-bar__line"><div class="vpg-bar__fill" style="width:{w}%"></div></div>'
                 f'<p class="vpg-bar__d">{esc(text)}</p></div>')
    return (f'<section class="vpg-sec vpg-sec_alt"><div class="vpg__in">'
            f'<h2 class="vpg-sec__h">{esc(p["bar_h2"])}</h2>'
            f'<p class="vpg-sec__lead">{esc(p["bar_lead"])}</p>'
            f'<div class="vpg-bars">{rows}</div></div></section>')


def shots(p):
    """Кадры со съёмок. Подпись несёт факт о работе, а не пересказ того, что видно."""
    items = ''.join(
        f'<figure class="vpg-shot"><img src="{IMG}/vpg/{f}" alt="{esc(cap)}" '
        f'loading="lazy" width="1600" height="900">'
        f'<figcaption>{esc(cap)}</figcaption></figure>' for f, cap in p['shots'])
    return (f'<section class="vpg-sec"><div class="vpg__in">'
            f'<h2 class="vpg-sec__h">{esc(p["shots_h2"])}</h2>'
            f'<p class="vpg-sec__lead">{esc(p["shots_lead"])}</p>'
            f'<div class="vpg-shots">{items}</div></div></section>')


def cards(p):
    items = ''.join(
        f'<a class="vpg-card" href="{href}">'
        f'<img src="{img}" alt="{esc(alt)}" loading="lazy" width="800" height="500">'
        f'<span class="vpg-card__b"><span class="vpg-card__t">{esc(title)}</span>'
        f'<span class="vpg-card__d">{esc(text)}</span>'
        f'<span class="vpg-card__go">Смотреть кейс →</span></span></a>'
        for href, img, title, text, alt in p['cards'])
    return (f'<section class="vpg-sec"><div class="vpg__in">'
            f'<h2 class="vpg-sec__h">{esc(p["cards_h2"])}</h2>'
            f'<div class="vpg-cards">{items}</div></div></section>')


def lists(p):
    out = ''
    for i, (head, items) in enumerate(p['lists']):
        cls = ' vpg-sec_alt' if i % 2 else ''
        body = ''.join(f'<div class="vpg-list__i"><b>{esc(t)}</b><span>{esc(d)}</span></div>'
                       for t, d in items)
        out += (f'<section class="vpg-sec{cls}"><div class="vpg__in">'
                f'<h2 class="vpg-sec__h">{esc(head)}</h2>'
                f'<div class="vpg-list">{body}</div></div></section>')
    return out


def price(p):
    return (f'<section class="vpg-sec"><div class="vpg__in">'
            f'<h2 class="vpg-sec__h">Стоимость и отзыв</h2>{cb.render(p["key"])}</div></section>')


def faq(p):
    items = ''.join(f'<details class="vpg-faq__i"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
                    for q, a in p['faq'])
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage',
          'mainEntity': [{'@type': 'Question', 'name': q,
                          'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in p['faq']]}
    return (f'<section class="vpg-sec vpg-sec_alt"><div class="vpg__in">'
            f'<h2 class="vpg-sec__h">Вопросы</h2>'
            f'<div class="vpg-faq">{items}</div>'
            f'<script type="application/ld+json">'
            f'{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>'
            f'</div></section>')


HERO_JS = """<script>(function(){
var v=document.querySelector('.vpg-hero__v');if(!v)return;
function on(){v.classList.add('is-on')}
if(v.readyState>2){on()}else{v.addEventListener('loadeddata',on)}
if('IntersectionObserver' in window){
 new IntersectionObserver(function(e){e[0].isIntersecting?v.play().catch(function(){}):v.pause()},
  {threshold:.05}).observe(v)}
if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){v.pause();v.removeAttribute('autoplay')}
})();</script>"""


def page(p):
    url = SITE + cb.PAGES[p['key']]['path']
    head = (
        '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{p["title"]}</title>'
        f'<meta name="description" content="{H.escape(p["descr"])}">'
        f'<link rel="canonical" href="{url}">'
        '<meta name="robots" content="index, follow">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{H.escape(p["title"])}">'
        f'<meta property="og:description" content="{H.escape(p["descr"])}">'
        f'<meta property="og:url" content="{url}">'
        f'<meta property="og:image" content="{SITE}{p["hero"]}">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')
    body = (f'{rc.header()}<main class="vpg">{hero(p)}{crumbs(p)}{bars(p)}{cards(p)}'
            f'{shots(p)}{lists(p)}{price(p)}{faq(p)}</main>{HERO_JS}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}</body></html>')
    return head + body


if __name__ == '__main__':
    for key, p in PAGES.items():
        outdir = os.path.join(ROOT, *p['out'])
        os.makedirs(outdir, exist_ok=True)
        f = os.path.join(outdir, 'index.html')
        open(f, 'w', encoding='utf-8').write(page(p))
        print('written', f, os.path.getsize(f) // 1024, 'KB')
