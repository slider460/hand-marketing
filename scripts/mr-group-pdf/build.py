#!/usr/bin/env python3
"""Печатная версия предложения для MR («Наша школа» 2026): отдельная вёрстка A4 альбомом с QR-кодами.

Порядок сборки:
  1. node scripts/mr-group-pdf/capture.mjs   (скриншоты игры, куба и схем с превью-страницы, нужен сервер mirror на :8080)
  2. python3 scripts/mr-group-pdf/build.py   (HTML в scripts/mr-group-pdf/out/print.html)
  3. node scripts/mr-group-pdf/render.mjs    (PDF в mirror/for/mr-group/mr-proposal.pdf)
"""
import os
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
M = 'file://' + os.path.join(ROOT, 'mirror')
IMG = M + '/for/mr-group/img'
CAP = 'file://' + os.path.join(HERE, 'captures')
SITE = 'https://hand-marketing.ru'
LIVE = SITE + '/for/mr-group/'

MR_PATH = ('M6.40114 2.62744L13.8561 19.0357L21.1274 2.62744H33.2125C35.6477 2.62761 37.6628 3.30835 39.2863 4.67292'
           'C40.9437 6.00574 41.7558 7.69525 41.7559 9.70888C41.7559 11.7227 40.9438 13.4123 39.2863 14.7772'
           'C38.0071 15.8265 36.4856 16.4704 34.7067 16.6974H37.7436L42.6322 25.368H37.1439L32.318 16.6974H26.5329V25.368'
           'H21.5615V6.92235L13.3897 25.368H11.0514L2.59893 6.76485V25.368H0.486816V2.62744H6.40114ZM26.5329 4.83244V14.5873'
           'H31.5527C34.2322 14.5873 36.0071 12.6641 36.0071 9.70888C36.007 6.7539 34.2321 4.83245 31.5527 4.83244H26.5329Z')


def mr_logo(color='#090714', h='6mm'):
    return f'<svg viewBox="0 0 43 28" style="height:{h};width:auto;color:{color}"><path fill="currentColor" d="{MR_PATH}"/></svg>'


def qr(url, dark='#090714', light='#ffffff'):
    """Векторный QR: печатается чётко на любом принтере."""
    q = segno.make(url, error='m')
    return q.svg_inline(scale=1, border=2, dark=dark, light=light, omitsize=True)


def qr_block(url, title, sub='', size='30mm', dark_bg=False):
    cls = 'qrb dark' if dark_bg else 'qrb'
    return (f'<div class="{cls}"><div class="qr" style="width:{size};height:{size}">{qr(url)}</div>'
            f'<div class="qt"><b>{title}</b>{f"<span>{sub}</span>" if sub else ""}</div></div>')


def page(n, body, cls='', foot=True):
    f = ''
    if foot:
        f = (f'<div class="foot">{mr_logo(h="3.6mm")}<i></i><img src="{M}/for/mr-group/hm-logo.svg" alt="">'
             f'<span>«Наша школа» 2026 · предложение Hand Marketing</span><b>{n:02d}</b></div>')
    return f'<section class="pg {cls}">{body}{f}</section>'


def head(num, eyebrow, title):
    return f'<div class="eb"><b>{num}</b>{eyebrow}</div><h2>{title}</h2>'


pages = []

# 01 · Обложка
pages.append(page(1, f'''
  <img class="bleed" src="{IMG}/stand-city.jpg" alt="">
  <div class="cover-shade"></div>
  <div class="cover-top">{mr_logo('#fff', '7mm')}<i></i><img src="{M}/for/mr-group/hm-logo.svg" alt=""></div>
  <div class="cover-in">
    <span class="pill glass"><span class="gem"></span>MR · «Наша школа» 2026 · Гостиный двор · 24–26 ноября</span>
    <h1>Два стенда,<br>одна история <em>MR</em></h1>
    <p>Подкаст-студия в прозрачном кубе (C7.2) и игра «Город MR» (C8.1) через проход друг от друга. Как мы их построим, нарисуем и запустим.</p>
  </div>
  <div class="cover-qr">{qr_block(LIVE, 'Живая версия с игрой', 'hand-marketing.ru/for/mr-group<br>пароль: <b>mr-group</b>', '34mm')}</div>
''', 'cover', foot=False))

# 02 · Задача
pages.append(page(2, f'''
  <div class="split-2">
    <div class="ph"><img src="{IMG}/mr-edu.jpg" alt=""><span class="pill sky">MR Образование</span></div>
    <div>
      {head('01', 'задача MR', 'MR, генеральный спонсор <em>X фестиваля</em> «Наша школа»')}
      <p class="lead">Фестиваль о проектировании и строительстве школ, садов и образовательной среды. Гостям не нужна реклама квартир. Им нужна история, в которой MR строит не только дома, но и то, где учатся.</p>
      <div class="chips"><span>органы власти</span><span>архитекторы и бюро</span><span>проектные институты</span><span>студенты профильных вузов</span><span>девелоперы</span><span>edtech и оснащение школ</span></div>
      <div class="kpis"><div><b>3 дня</b><span>24–26 ноября, 10:00–20:00</span></div><div><b>2 × 11 м²</b><span>стенды C7.2 и C8.1 через проход</span></div><div><b>400</b><span>историй жителей, цель MR</span></div></div>
    </div>
  </div>
'''))

# 03 · Идея и зал
pages.append(page(3, f'''
  {head('02', 'идея', 'Два стенда через проход работают <em>как одна экспозиция</em>')}
  <div class="split-2 mid">
    <img class="shot" src="{CAP}/hall.png" alt="">
    <div>
      <p class="lead">Экран города виден из куба. Гости подкаста тоже проходят игру и появляются в городе с отметкой. Одна айдентика, один ромб, одна история MR на обе стороны прохода.</p>
      <div class="legend"><span class="tag sky">C7.2</span><div><b>Подкаст-студия</b><p>Прозрачный куб, где идут разговоры с лидерами отрасли. Гость уходит с готовым выпуском.</p></div></div>
      <div class="legend"><span class="tag v">C8.1</span><div><b>Город MR</b><p>Гость создаёт жителя и переезжает в проект MR. Уходит с открыткой и ободком с ромбом.</p></div></div>
    </div>
  </div>
'''))

# 04 · Подкаст-куб: инженерия
pages.append(page(4, f'''
  {head('03', 'стенд C7.2 · подкаст-студия', 'Прозрачный куб, <i>в котором тихо</i>')}
  <div class="split-2 cube-pg">
    <img class="shot dark" src="{CAP}/cube.png" alt="">
    <div>
      <div class="grid2">
        <div class="box"><b><i style="background:#5ec4f7"></i>Стекло и тишина</b><p>Двойное остекление, закрытый потолок, плавающий пол. Запись звучит как студийная, снаружи куб прозрачный.</p></div>
        <div class="box"><b><i style="background:#2dbe6c"></i>Воздух без шума</b><p>Вентиляция вынесена за стенку куба и идёт через глушители. В микрофонах вентиляторов не слышно.</p></div>
        <div class="box"><b><i style="background:#754be9"></i>Звук для зрителей</b><p>Разговор идёт в беспроводные наушники у стенда: слышно каждое слово, соседи не мешают.</p></div>
        <div class="box"><b><i style="background:#ff4c4c"></i>Выпуск в тот же день</b><p>Три камеры, эфирные микрофоны, монтажёр на стенде. Гость уходит с видео, аудио и роликами.</p></div>
      </div>
      <div class="warn"><b>Правило Гостиного двора:</b> мероприятия со звуком на стендах запрещены, штраф 25 000 ₽. Поэтому звук только в наушниках. Такую схему мы уже ставили на стенде Самарской области на ВДНХ.</div>
    </div>
  </div>
'''))

# 05 · Подкаст: механизм
pages.append(page(5, f'''
  {head('03', 'подкаст-студия · как работает', 'Площадка, которую <i>распространяют гости</i>')}
  <div class="steps4">
    <div><span class="n sky">1</span><b>Программа заранее</b><p>Приглашаем спикеров, утверждаем темы и расписание. Записи в часы пик по трафику зала, без импровизации.</p></div>
    <div><span class="n sky">2</span><b>Запись с героем</b><p>Ведущие из «Москвы глазами инженера» меняются по графику. Зрители слушают в наушниках.</p></div>
    <div><span class="n sky">3</span><b>Файлы сразу</b><p>После записи гость получает аудио, видео из брендированного куба и короткие ролики.</p></div>
    <div><span class="n sky">4</span><b>Гость публикует сам</b><p>Telegram, соцсети, сайт компании. Контент расходится по 10–15 каналам участников.</p></div>
  </div>
  <div class="res3">
    <div><b>10–15</b><span>каналов участников, куда уходит каждый выпуск</span></div>
    <div><b>3 камеры</b><span>видео из брендированного куба, а не только звук</span></div>
    <div><b>в тот же день</b><span>гость уходит с аудио, видео и короткими роликами</span></div>
  </div>
  <div class="band">Мы не распространяем контент сами. Мы создаём площадку, а участники распространяют его на своих платформах.<small>Из концепции MR для стенда C7.2</small></div>
'''))

# 06 · Город MR: стенд
pages.append(page(6, f'''
  {head('04', 'стенд C8.1 · город MR', 'Игра, после которой гость <em>живёт в проекте MR</em>')}
  <div class="split-3">
    <div class="ph tall"><img src="{IMG}/family.jpg" alt=""><span class="pill dim">Визуализация</span></div>
    <img class="shot" src="{CAP}/layout.png" alt="">
    <div class="zl">
      <h3>Четыре станции, экран и выдача на 11 м²</h3>
      <div><i style="background:#754be9"></i><b>Экран 86″</b><p>На задней стене. Карту видно из прохода и из куба напротив.</p></div>
      <div><i style="background:#2dbe6c"></i><b>4 игровые станции</b><p>Стойки-домики по бокам, лицом к центру. Пятый iPad в резерве.</p></div>
      <div><i style="background:#ffb020"></i><b>Стойка выдачи</b><p>Принтер открыток, ободки, промоутер. Внутри тумбы сервер игры.</p></div>
      <div><i style="background:#5ec4f7"></i><b>Центр свободен</b><p>Очередь по разметке и фото на фоне карты.</p></div>
      <p class="note">Станция принимает 8–10 гостей в час, четыре станции 30–40. Цель в 400 историй за три дня закрывается с запасом.</p>
    </div>
  </div>
'''))

# 07 · Игра: экраны планшета
pages.append(page(7, f'''
  {head('05', 'прототип игры · экраны планшета', 'Пять минут, после которых <em>гость живёт в городе MR</em>')}
  <div class="play-pg">
    <div class="screens2">
      <figure><img src="{CAP}/g0-start.png" alt=""><figcaption><b>1</b>Старт: что будет и сколько займёт</figcaption></figure>
      <figure><img src="{CAP}/g1-ctor.png" alt=""><figcaption><b>2</b>Житель: 7 параметров и имя</figcaption></figure>
      <figure><img src="{CAP}/g2-question.png" alt=""><figcaption><b>3</b>5 вопросов, ответ в один тап</figcaption></figure>
      <figure><img src="{CAP}/g3-result.png" alt=""><figcaption><b>4</b>Дом, учёба, профессия, история</figcaption></figure>
    </div>
    <div class="play-side">
      <p class="lead">Это рабочий прототип, а не картинки: его можно пройти на живой странице, житель появится на карте.</p>
      <p class="note">Графику, вопросы и веса согласуем с MR и социологами. Ответы анонимные, контакты не собираем. Больше 20 тысяч сочетаний внешности: двух одинаковых жителей почти не бывает.</p>
      <div style="margin-top:auto">{qr_block(LIVE + '#play', 'Пройдите игру сами', 'пароль: <b>mr-group</b>', '30mm')}</div>
    </div>
  </div>
'''))

# 08 · Житель в городе и открытка
pages.append(page(8, f'''
  {head('05', 'большой экран и открытка', 'Житель приземляется <em>в свой квартал</em>')}
  <div class="split-map">
    <img class="shot" src="{CAP}/g4-map.png" alt="">
    <div>
      <img class="card-img" src="{CAP}/g5-card.png" alt="">
      <p class="note">Открытка 10 × 15 печатается за 10–15 секунд: житель, имя, профессия, дом и учёба, QR на историю. Экран наезжает на квартал нового жителя, к вечеру на карте сотни жителей. Эскиз графики: условные кварталы заменим на реальные проекты MR.</p>
    </div>
  </div>
'''))

# 09 · Путь гостя и ромбы
steps = [('Притяжение', 'видит город и ромбы', 'из прохода'), ('Старт', 'согласие одной строкой', '20 с'),
         ('Житель', '20 тысяч сочетаний', '1,5–2 мин'), ('Вопросы', 'ответ в один тап', '1–1,5 мин'),
         ('Переезд', 'проект MR и история', '40 с'), ('В город', 'житель на экране', '15 с'),
         ('Открытка', 'печать и ободок', '30 с'), ('После', 'история по QR', 'дома')]
path = ''.join(f'<div><span>{i+1}</span><b>{a}</b><p>{b}</p><em>{c}</em></div>' for i, (a, b, c) in enumerate(steps))
pages.append(page(9, f'''
  {head('06', 'путь гостя и эффект', 'Восемь шагов, пять минут <em>и ромб на голове</em>')}
  <div class="path">{path}</div>
  <div class="gems">
    <div class="ph"><img src="{IMG}/crowd.jpg" alt=""><span class="pill dim">Визуализация</span><div class="cap">К концу первого дня ободки MR видно в каждом зале. Каждый ромб ведёт к стенду.</div></div>
    <div class="ph"><img src="{IMG}/handout.jpg" alt=""><span class="pill dim">Визуализация</span></div>
    <div class="ph"><img src="{IMG}/headbands.jpg" alt=""><span class="pill dim">Визуализация</span></div>
  </div>
'''))

# 10 · Данные и надёжность
pages.append(page(10, f'''
  {head('07', 'данные для MR', 'Каждое прохождение <em>становится строкой</em> для социологов')}
  <div class="grid3">
    <div class="box"><b>Что сохраняем</b><ul><li>время и номер станции</li><li>ответы на все вопросы</li><li>параметры жителя</li><li>дом, учёба, профессия</li><li>длительность прохождения</li></ul></div>
    <div class="box"><b>Как отдаём</b><ul><li>Excel в любой момент из админки</li><li>листы: ответы, распределение, по часам</li><li>CSV для SPSS и R</li><li>финальная выгрузка с актом</li></ul></div>
    <div class="box"><b>Без персональных данных</b><ul><li>имя жителя вымышленное</li><li>контакты, фото и ФИО не собираем</li><li>152-ФЗ не затрагивается</li><li>нужны контакты: отдельное согласие</li></ul></div>
  </div>
  <div class="grid4 darkrow">
    <div><b>Сервер на стенде</b><p>Мини-ПК в стойке выдачи держит игру, базу и очередь печати.</p></div>
    <div><b>Облако только зеркало</b><p>Пропал интернет площадки, стенд работает, данные досылаются позже.</p></div>
    <div><b>Админка</b><p>Статистика по часам, модерация имён, повторная печать.</p></div>
    <div><b>Резерв</b><p>Пятый iPad, запасной принтер, копия базы каждые 15 минут.</p></div>
  </div>
  <div class="xlwrap"><div class="xlcap">Так выглядит выгрузка: пример строк, данные условные</div><table class="xl"><thead><tr><th>время</th><th>станция</th><th>житель</th><th>дом</th><th>учёба</th><th>профессия</th><th>время прохождения</th></tr></thead><tbody><tr><td>24.11 10:14</td><td>2</td><td>Мира</td><td>Квартал у набережной</td><td>Факультет девелопмента ВШЭ</td><td>Архитектор общественных пространств</td><td>4:52</td></tr><tr><td>24.11 10:16</td><td>4</td><td>Тимур</td><td>Квартал у метро</td><td>Факультет девелопмента ВШЭ</td><td>Инженер умного дома</td><td>5:10</td></tr><tr><td>24.11 10:19</td><td>1</td><td>Ася</td><td>Семейный квартал</td><td>Детский сад в квартале</td><td>Дизайнер детских пространств</td><td>4:31</td></tr><tr><td>24.11 10:21</td><td>3</td><td>Лев</td><td>Квартал у новой школы</td><td>Школа в квартале</td><td>Учитель проектной школы</td><td>5:47</td></tr></tbody></table></div>
'''))

# 11 · Гостиный двор
rules = [('Аккредитация застройщика', 'До 8 октября у ООО «Экспо-Сервис»', 'Сторонний застройщик допускается после экспертизы документации. Этот срок заложен в график.', True),
         ('Звук на стендах', 'Запрещён, штраф 25 000 ₽', 'В кубе звук только в беспроводных наушниках. Игра без звука, привлекает картинкой и ромбом.', False),
         ('Монтаж', '22–23 ноября и до 06:00 24 ноября', 'Куб и конструктив собираем на складе заранее, на площадке только сборка и настройка.', False),
         ('Стены и крепёж', 'Панели 3,5 м, сверлить нельзя, гипсокартон запрещён', 'Куб самонесущий. Экран и брендинг на своих конструкциях или за верхний торец панели.', False),
         ('Электричество', 'До 2,5 кВт на стенд', 'Экран, пять iPad, принтер и мини-ПК укладываются. Свет и вентиляцию куба считаем отдельно.', False),
         ('Демонтаж', '26 ноября с 20:00 до 08:00 27 ноября', 'Разбираем и вывозим за ночь, мусор вывозим сами.', False)]
rh = ''.join(f'<div class="rule{" hot" if hot else ""}"><span>{a}</span><b>{b}</b><p>{c}</p></div>' for a, b, c, hot in rules)
pages.append(page(11, f'''
  {head('08', 'Гостиный двор', 'Руководство участника <em>уже учли в проекте</em>')}
  <div class="rules">{rh}</div>
'''))

# 12 · График и зона ответственности
tl = [('до 8 октября', 'Решение MR, аккредитация застройщика, первые эскизы стендов', '#754be9'),
      ('до 10 октября', 'От MR: список проектов, вопросы для игры, брендбук', '#5ec4f7'),
      ('октябрь', 'Концепция и 3D обоих стендов, согласование, график спикеров', '#9d7cff'),
      ('октябрь – ноябрь', 'Производство куба и стендов, разработка игры, графика города', '#2dbe6c'),
      ('середина ноября', 'Полный прогон на складе: сборка, замеры тишины, игра с печатью', '#ffb020'),
      ('22–23 ноября', 'Монтаж на площадке и настройка', '#ff4c4c'),
      ('24–26 ноября', 'Фестиваль: команда на стендах все три дня, выгрузка данных', '#090714')]
tlh = ''.join(f'<div><b><i style="background:{c}"></i>{a}</b><span>{b}</span></div>' for a, b, c in tl)
pages.append(page(12, f'''
  {head('09', 'график и роли', 'Как дойдём до открытия <em>24 ноября</em>')}
  <div class="split-2 top">
    <div class="tl">{tlh}</div>
    <div>
      <div class="box"><b>Hand Marketing</b><ul class="cols2"><li>концепция и 3D обоих стендов</li><li>рабочий проект, аккредитация</li><li>производство куба и конструктива</li><li>звук, видео, свет, вентиляция</li><li>разработка игры и графика города</li><li>открытки, ободки, брендинг</li><li>команда на стендах все дни</li><li>монтаж, демонтаж, вывоз</li><li>выпуски подкаста и выгрузка ответов</li></ul></div>
      <div class="box sky"><b>MR</b><ul><li>спикеры и расписание подкаста</li><li>проекты MR и вопросы для игры</li><li>брендбук и согласования</li></ul><p class="note">Драфт бюджета по двум стендам у вас отдельным файлом.</p></div>
    </div>
  </div>
'''))

# 13 · Мы это уже делали
cases = [('/images/lib/custom-samara-vdnh/stand-hero.jpg', 'ВДНХ · 248 дней', 'Стенд Самарской области', 'Проект, застройка, 20+ мультимедийных систем, игры для восьми тач-панелей, звук в ИК-наушниках. 16 млн посетителей стенда.', '/portfolio/samara-stand-vdnh/'),
         ('/images/becar-pm/photo-stand-full.jpg', 'Девелопер · министенд', 'Министенд Becar на Private Money Expo', 'Маленькая площадь и семь брендов. Два эскиза и финал в 3D, застройка в ночь до открытия, дежурство, демонтаж.', '/portfolio/becar-private-money/'),
         ('/portfolio/samara-exhibition/photos/VR_Samara.jpg', 'Музей Алабина · интерактив', 'Выставка «Самара»', 'Пять комплектов VR с виртуальной сборкой ракеты «Союз», Kinect-игры, тач-панели с голосованиями.', '/portfolio/samara-exhibition/')]
ch = ''.join(f'<div class="case"><img src="{M}{img}" alt=""><div class="cb"><span>{k}</span><b>{t}</b><p>{d}</p>'
             f'<div class="mini-qr">{qr(SITE + url)}<small>кейс</small></div></div></div>' for img, k, t, d, url in cases)
pages.append(page(13, f'''
  {head('10', 'мы это уже делали', 'Стенды, игры и звук <em>в наушниках</em>')}
  <div class="cases">{ch}</div>
  <div class="quotes">
    <div class="q v">«…мы рады возможности решать задачи разного уровня и направлений (от разработки и производства сувенирной продукции до оформления стендов и проведение клиентских мероприятий) в рамках взаимодействия с одной компанией.»<span>Д. С. Сороколетов, вице-президент Becar Asset Management</span></div>
    <div class="q">«Агентством были выполнены все поставленные задачи в сжатые сроки, что свидетельствует о высоком профессионализме сотрудников.»<span>Т. В. Левченко, генеральный директор МФК «Саларис»</span></div>
    <div class="q">«Нас впечатлила Ваша эффективная манера работы, творческий подход к разработке концепции мероприятия, терпение и желание выполнять все, даже самые неожиданные, пожелания заказчика.»<span>Томас Штенцель, генеральный директор Messe Düsseldorf Moscow</span></div>
  </div>
'''))

# 14 · Креатив
cr = [(IMG + '/samara-mascot.jpg', 'Правительство Самарской области', 'Фирменный стиль выставки «Самара»', 'Брендбук на 28 полос, маскот Ладушка в 16 образах, навигация, экраны.', '/creative/samara/'),
      (M + '/images/sgsuitcase/view-front.jpg', 'Saint-Gobain', 'Проектный чемодан «Две комнаты»', 'Звукоизоляция Gyproc и ISOVER, которую показывают руками.', '/creative/saintgobain/suitcase/'),
      (M + '/images/skolkovo/mock-spread.png', 'СКОЛКОВО', 'Доклад «Цифровое производство»', 'Книга на 86 полос: вёрстка, инфографика, модели зрелости.', '/creative/skolkovo/'),
      (M + '/images/metra/m-mtg-city.jpg', 'Metra Technology Group', 'Брендбук на пять брендов', 'Одна система для всей экосистемы, от визитки до сити-формата.', '/creative/metra/'),
      (IMG + '/sg-calendar.jpg', 'Saint-Gobain · концепция', 'Новогодний календарь', 'Продукт Gyproc или ISOVER в авторской графике на каждый месяц.', '/creative/saintgobain/calendar/'),
      (IMG + '/patriki.jpg', 'Patriki Times', 'Журнал Patriki Times', 'Дизайн и вёрстка двух номеров на 52 и 68 полос.', '/creative/patriki/')]
crh = ''.join(f'<div class="cr"><img src="{img}" alt=""><div class="cb"><span>{k}</span><b>{t}</b><p>{d}</p>'
              f'<div class="mini-qr sm">{qr(SITE + url)}</div></div></div>' for img, k, t, d, url in cr)
pages.append(page(14, f'''
  {head('11', 'креатив и дизайн', 'Айдентика, книги и объекты, <em>которые держат в руках</em>')}
  <div class="crg">{crh}</div>
'''))

# 15 · Видео
vids = [(M + '/images/vivax/rest-smile.jpg', 'VIVAX SPORT · реклама', 'Ролик с Настасьей Самбурской', 'Три средства линейки внутри одной тренировки. Звезда в кадре, продукт в каждой сцене.', '/video/vivax/'),
        (M + '/images/patriot/poster.jpg', 'УАЗ × Eaton · реклама', 'УАЗ Патриот с блокировкой Eaton', 'Грязь, брод и бездорожье. Ролик показывает, что даёт блокировка дифференциала, без технической лекции.', '/video/patriot/')]
vh = ''.join(f'<div class="vc"><div class="poster"><img src="{img}" alt=""></div><div class="cb row"><div><span>{k}</span><b>{t}</b><p>{d}</p></div>'
             f'<div class="qrcol"><div class="mini-qr">{qr(SITE + url)}</div><small>смотреть ролик</small></div></div></div>' for img, k, t, d, url in vids)
pages.append(page(15, f'''
  {head('12', 'видеопродакшн', 'Снимаем <em>своей группой</em>')}
  <p class="lead" style="margin-top:0">Камеры, свет и операторы свои. Та же команда запишет выпуски в кубе и снимет ролик о стендах MR на фестивале.</p>
  <div class="vids">{vh}</div>
'''))

# 16 · Контакты
pages.append(page(16, f'''
  <div class="big-gem"></div>
  <div class="cover-top">{mr_logo('#fff', '7mm')}<i></i><img src="{M}/for/mr-group/hm-logo.svg" alt=""></div>
  <div class="contact-in">
    <h1>Готовы начать</h1>
    <p>Команда под MR собрана, сроки площадки заложены в график.</p>
    <div class="person"><div class="av">АН</div><div><b>Александр Народецкий</b><span>Client Service Director, Hand Marketing</span></div></div>
    <div class="lines"><div><small>телефон</small>+7 985 999-87-83</div><div><small>почта</small>anarodetsky@hand-marketing.ru</div><div><small>сайт</small>hand-marketing.ru</div></div>
    <div class="qrs">
      {qr_block('https://t.me/narodetskii', 'Telegram', 't.me/narodetskii', '30mm', True)}
      {qr_block('tel:+79859998783', 'Позвонить', '+7 985 999-87-83', '30mm', True)}
      {qr_block(LIVE, 'Живая версия', 'пароль: <b>mr-group</b>', '30mm', True)}
    </div>
  </div>
''', 'dark', foot=False))

CSS = open(os.path.join(HERE, 'print.css'), encoding='utf-8').read()
html = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<link rel="stylesheet" href="{M}/fonts/unbounded-fira.css"><link rel="stylesheet" href="{M}/fonts/react-main.css">
<style>{CSS}</style></head><body>{''.join(pages)}</body></html>'''
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
out = os.path.join(HERE, 'out', 'print.html')
open(out, 'w', encoding='utf-8').write(html)
print(out, len(pages), 'листов')
