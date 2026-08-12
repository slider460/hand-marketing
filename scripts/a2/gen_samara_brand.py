#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/creative/samara/index.html: кейс «Фирменный стиль выставки
„Самара“» — руководство по использованию фирменного стиля Самарской области,
по которому оформлена выставка «Самара» в Музее им. П. В. Алабина.

Первоисточник один: brandbook_v2_2.pdf, 28 полос. Ничего не придумано —
логотип, поля, палитра с точными hex, линейка Manrope, 16 образов маскота,
46 слов семантического ядра, принципы бенто-макетов, геометрия навигационной
таблички и все носители читаются с полос гайда. Знак, кривая паттерна и обе
группы иконок вынуты из PDF кривыми (не скриншотами) и лежат в
samara_vectors.json; растр готовит scripts/samara-brand-assets.py.

Идея страницы. Брендбук — не альбом с картинками, а работающая система: по
нему подрядчик собирает макет зоны, табличку и пост без дизайнера. Значит
и страница должна не показывать полосы, а давать этой системой пользоваться.
Отсюда четыре механики:

1. «Стена зоны» (сигнатурная). Выбираешь зону выставки — Ладушка переодевается
   настоящим рендером из гайда, фон уходит в заливку зоны, а слова ядра
   разлетаются и садятся в композицию алгоритмом раскладки без пересечений,
   с чередованием трёх типов чипа (белый / персиковый / синий). «Пересобрать»
   даёт новую раскладку: видно, что это правило, а не один нарисованный макет.
   Игровая зона и лекторий показаны в самом гайде, остальные собраны по тому
   же правилу — об этом сказано в подписи, чтобы не выдавать своё за клиентское.
2. «Гардероб Ладушки» — 16 образов одного персонажа; наложение силуэтов
   показывает, что меняются одежда и атрибут, а каркас остаётся.
3. Конструктор навигационной таблички по модулю X: слово, иконка, стрелка,
   поверх — красная сетка замеров 3/4X, X и 0,5X с полосы 27. Ползунок X
   доказывает, что правило масштабируется, а не нарисовано в одном размере.
4. Парус: контур знака по скроллу разворачивается в кривую фонового паттерна.

Шрифт — Manrope, один на всю страницу: гайд предписывает его и для заголовков,
и для текста, и для подписей, различаем только весами 200→800
(/fonts/manrope-samara.css, self-host). Палитра — ровно из гайда.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

VEC = json.load(open(os.path.join(HERE, 'samara_vectors.json'), encoding='utf-8'))
# доля ширины, на которой стоят ступни: по ней совмещаются силуэты
ANCHOR = json.load(open(os.path.join(HERE, 'samara_mascots.json'), encoding='utf-8'))

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/samara-brand'
PHOTO = '/portfolio/samara-exhibition/photos'
URL = 'https://hand-marketing.ru/creative/samara/'

# размеры готовых файлов из scripts/samara-brand-assets.py
SIZE = {"app-schedule": [430, 915], "app-welcome": [442, 791], "art": [368, 811], "banner-welcome": [1311, 735], "banner-win": [593, 333], "basketball": [254, 817], "business": [294, 872], "city": [359, 858], "citylight": [1042, 761], "education": [308, 848], "football": [265, 1062], "future": [318, 808], "games": [201, 848], "gifts": [210, 859], "health": [248, 873], "hero": [360, 1033], "hockey": [316, 836], "lecture": [208, 597], "museum": [773, 425], "patriotism": [341, 907], "screen-level": [126, 226], "screen-players": [616, 353], "tablet": [1332, 932], "tourism": [276, 802], "wall-volga": [1515, 476], "youth": [337, 835]}
PHOTO_SIZE = {"Game_kinect": [1600, 1200], "Inform_samara": [2560, 1920],
              "LED_Lector_Samara": [2560, 1920], "VR_Samara": [1085, 836],
              "Ekran_parus": [1600, 1066]}


def png(name, alt, cls='', lazy=True):
    w, h = SIZE[name]
    l = ' loading="lazy" decoding="async"' if lazy else ''
    c = f' class="{cls}"' if cls else ''
    return (f'<img src="{IMG}/{name}.png" alt="{alt}" width="{w}" height="{h}"{c}{l}>')


def jpg(name, alt, cls='', lazy=True):
    w, h = SIZE[name]
    l = ' loading="lazy" decoding="async"' if lazy else ''
    c = f' class="{cls}"' if cls else ''
    return (f'<img src="{IMG}/{name}.jpg" alt="{alt}" width="{w}" height="{h}"{c}{l}>')


def photo(name, alt, cls=''):
    w, h = PHOTO_SIZE[name]
    c = f' class="{cls}"' if cls else ''
    return (f'<img src="{PHOTO}/{name}.jpg" alt="{alt}" width="{w}" height="{h}"{c}'
            f' loading="lazy" decoding="async">')


def _paths(key):
    """Пути фигуры; цвет всегда currentColor — задаём его на родителе."""
    body = []
    for p in VEC[key]['paths']:
        rule = ' fill-rule="evenodd"' if p['even_odd'] else ''
        if p['fill']:
            body.append(f'<path d="{p["d"]}" fill="currentColor"{rule}/>')
        else:
            body.append(f'<path d="{p["d"]}" fill="none" stroke="currentColor" '
                        f'stroke-width="{p["w"] or 2}" stroke-linecap="round" '
                        f'stroke-linejoin="round"/>')
    return ''.join(body)


def sprite():
    """Один спрайт на страницу: знак и кривая паруса встречаются по десять раз,
    инлайнить их каждый раз — лишние сто килобайт."""
    syms = ''.join(f'<symbol id="sb-{k}" viewBox="{VEC[k]["viewBox"]}">{_paths(k)}</symbol>'
                   for k in VEC)
    return (f'<svg class="sb-sprite" aria-hidden="true" focusable="false" '
            f'style="position:absolute;width:0;height:0;overflow:hidden">{syms}</svg>')


def svg(key, cls='', color='', inline=False):
    """Фигура из брендбука кривыми: см. scripts/samara-brand-assets.py.
    По умолчанию ссылается на спрайт; inline=True — когда фигуру нужно
    измерить скриптом (длина кривой для анимации рисования)."""
    c = f' class="{cls}"' if cls else ''
    s = f' style="color:{color}"' if color else ''
    vb = VEC[key]['viewBox']
    if inline:
        inner = _paths(key)
    else:
        # <use> кладёт символ в прямоугольник от нуля, поэтому внешний viewBox
        # тоже начинается с нуля: иначе фигура уезжает на смещение исходной полосы
        w, h = vb.split()[2:]
        vb = f'0 0 {w} {h}'
        inner = f'<use href="#sb-{key}"/>'
    return (f'<svg viewBox="{vb}"{c}{s} aria-hidden="true" '
            f'focusable="false">{inner}</svg>')


def pressed(flag):
    """aria-pressed для кнопок-переключателей."""
    return ' aria-pressed="true"' if flag else ' aria-pressed="false"'


# ─── герой ──────────────────────────────────────────────────────────────────
FACTS = [
    ('28', 'полос руководства'),
    ('16', 'образов маскота'),
    ('46', 'слов семантического ядра'),
    ('12', 'цветов и 2 градиента'),
]

# разделы гайда — из содержания на полосе 2
SECTIONS = ['Логотип', 'Шрифты', 'Цвета', 'Паттерны и стилеобразующие элементы',
            'Семантическое ядро', 'Маскот', 'Принципы построения дизайн-макетов',
            'Оформление пространств', 'Web', 'Работа с фотографиями',
            'Брендированная продукция', 'Принципы оформления социальных сетей',
            'Навигация и принципы построения', 'Примеры использования брендбука',
            'Ко-брендинг']

TASK = [
    ('Контекст',
     'Выставка «Самара» открылась в Музее им. П. В. Алабина и продолжила проект '
     'региона с выставки-форума «Россия» на ВДНХ. Стенд с ладьёй и парусом '
     'закончился, а его визуальный язык должен был переехать в музейные залы '
     'и жить дальше.'),
    ('Задача',
     'Не альбом с картинками, а рабочая система. Зон много, носителей ещё больше: '
     'стены, экраны, ситиформаты, приложение, навигация, сувенирка. Собирать '
     'каждый макет с дизайнером — не вариант, значит правила должны быть '
     'такими, чтобы по ним собирал подрядчик.'),
    ('Решение',
     'Руководство на 28 полос, где каждый раздел заканчивается не примером, '
     'а правилом: как строится логотипный блок, из чего собирается стена зоны, '
     'по какому модулю режется навигационная табличка, чем маскот в спортзоне '
     'отличается от маскота в лектории.'),
]

SCOPE = [
    'Логотип: две версии, поля, монохром, фирменные блоки',
    'Палитра: шесть основных цветов, шесть дополнительных, два градиента',
    'Типографика на одном шрифте — Manrope, шесть весов',
    'Маскот «Ладушка»: базовый образ и 15 тематических',
    'Семантическое ядро: 46 слов и правило их вёрстки',
    'Паттерн и стилеобразующие элементы из знака',
    'Иконки: тематические и навигационные',
    'Принципы бенто-макетов для печати и цифры',
    'Оформление стен выставочных зон',
    'Web и мобильное приложение выставки',
    'Навигация: геометрия таблички по модулю X',
    'Ко-брендинг и правила работы с фотографиями',
]

# ─── логотип: поля из полосы «Область безопасности» ─────────────────────────
# Числа не на глаз: красные линии-замеры на полосе 4 сняты из PDF. Для
# горизонтальной версии X = 18,5 pt, охранное поле вокруг блока = 3X
# (531,8 × 231,5 против блока 420,8 × 120,6), зазор знак↔надпись = 1,25X.
# Для вертикальной X = 24,1 pt, поле = 2X, зазор = 1,25X.
SAFETY = [
    ('Горизонтальная версия', [
        ('1X', 'модуль: высота нижнего элемента знака'),
        ('1,25X', 'от знака до наборной части'),
        ('3X', 'охранное поле вокруг блока'),
    ]),
    ('Вертикальная версия', [
        ('1X', 'тот же модуль по знаку'),
        ('1,25X', 'от знака до надписи'),
        ('2X', 'охранное поле вокруг блока'),
    ]),
]

# ─── палитра: точные значения с полос «Иерархия цветов» ────────────────────
MAIN_COLORS = [
    ('2D3051', 'Основной тёмно-синий', 'light'),
    ('368AB5', 'Синий', 'light'),
    ('F4E3DB', 'Розово-бежевый', 'dark'),
    ('F7D5B1', 'Персиковый', 'dark'),
    ('FFFFFF', 'Белый', 'dark'),
    ('000000', 'Чёрный', 'light'),
]
ADD_COLORS = [
    ('046081', 'Морской', 'light'),
    ('063A5A', 'Глубокий синий', 'light'),
    ('F6A4B1', 'Розовый', 'dark'),
    ('567EF3', 'Акцентный синий', 'light'),
    ('B8C5EC', 'Градиент B8C5EC → EACEB6', 'dark'),
    ('307FA9', 'Градиент 307FA9 → 014A6D', 'light'),
]

# ─── шрифт: линейка с полосы «Шрифты» ──────────────────────────────────────
WEIGHTS = [(200, 'ExtraLight'), (300, 'Light'), (400, 'Regular'),
           (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold')]

TYPE_ROLES = [
    ('Заголовки', 'ПОЕХАЛИ<br>В САМАРУ', 'sb-t-h'),
    ('Основной текст',
     'Здорово съездили в Самарскую область на прошлой неделе! Мне больше всего '
     'понравилась Волга и музей космонавтики.', 'sb-t-b'),
    ('Подписи', 'САМАРСКАЯ ЛУКА', 'sb-t-c'),
]

# ─── маскот: 16 образов, подписи из гайда ──────────────────────────────────
MASCOTS = [
    ('hero', 'Базовый', 'Белая блузка, синяя юбка, приветственный жест'),
    ('business', 'Бизнес', 'Деловой костюм и планшет'),
    ('city', 'Благоустройство', 'Каска и лейка'),
    ('patriotism', 'Патриотизм', 'Полевой китель и гвоздики'),
    ('health', 'Здравоохранение', 'Халат и стетоскоп'),
    ('games', 'Игры', 'Геймпад'),
    ('future', 'Будущее', 'Костюм с оранжевыми вставками'),
    ('education', 'Обучение', 'Мантия и конфедератка'),
    ('youth', 'Молодость', 'Скейт, рюкзак, книги'),
    ('art', 'Искусство', 'Театральные маски'),
    ('tourism', 'Туризм', 'Карта и рюкзак'),
    ('hockey', 'Спорт', 'Форма ХК «Лада»'),
    ('football', 'Спорт', 'Форма ФК «Крылья Советов»'),
    ('basketball', 'Спорт', 'Форма БК «Самара»'),
    ('gifts', 'Подарки', 'Коробка с лентой'),
    ('lecture', 'Лекторий', 'Базовый образ у экрана'),
]

# ─── семантическое ядро: 46 слов с полос 13-14 ─────────────────────────────
CORE = ['Инновации', 'Технологии', 'Культура', 'Искусство', 'Мастер-классы',
        'Достижения', 'Наука', 'Открытия', 'Образование', 'Демонстрации',
        'Дискуссии', 'Экспозиции', 'Премьеры', 'Эксперименты', 'Обсуждения',
        'Форумы', 'Встречи', 'Показ', 'Прогресс', 'Виртуальная реальность',
        'Презентации', 'Перформансы', 'Новинки', 'Исследования', 'Перспективы',
        'Вдохновение', 'Креативность', 'Сотрудничество', 'Интерактив', 'Опыты',
        'Лекции', 'Тренды', 'Новаторство', 'Творчество', 'Возможности',
        'Актуальность', 'Прорывы', 'Цифровизация', 'Моделирование', 'Эволюция',
        'Вебинары', 'Аналитика', 'Консультации', 'Разработки', 'Инсталляции',
        'Продуктивность']

# ─── зоны: (ключ, название, маскот, фон, цвет текста, центральное слово,
#            слова вокруг, откуда) ─────────────────────────────────────────
# Игровая зона и лекторий разобраны в самом гайде (полосы 19-20), остальные
# собраны по тому же правилу — это честно сказано в подписи к блоку.
ZONES = [
    ('games', 'Игровая зона', 'games', 'linear-gradient(100deg,#B8C5EC,#EACEB6)',
     '#2D3051', 'ИГРЫ',
     ['Спорт', 'Разработки', 'Инновации', 'Новаторство', 'Развитие', 'Тренды',
      'Новинки', 'Виртуальная реальность', 'Технологии', 'Интерактив'], 'гайд'),
    ('lecture', 'Зона лектория', 'lecture', '#368AB5', '#FFFFFF', 'ЛЕКЦИИ',
     ['Культура', 'Обсуждения', 'Вебинары', 'Развитие', 'Презентации',
      'Эксперименты', 'Дискуссии', 'Форумы', 'Интерактив', 'Встречи'], 'гайд'),
    ('sport', 'Спортивная зона', 'football', '#046081', '#FFFFFF', 'СПОРТ',
     ['Достижения', 'Тренды', 'Прорывы', 'Наука', 'Актуальность', 'Эволюция',
      'Исследования', 'Технологии', 'Творчество'], 'правило'),
    ('education', 'Зона образования', 'education', '#063A5A', '#FFFFFF', 'ОБРАЗОВАНИЕ',
     ['Культура', 'Прогресс', 'Продуктивность', 'Исследования', 'Моделирование',
      'Интерактив', 'Разработки', 'Технологии', 'Инновации'], 'правило'),
    ('tourism', 'Зона туризма', 'tourism', '#F4E3DB', '#2D3051', 'ОТКРЫТИЯ',
     ['Вдохновение', 'Встречи', 'Культура', 'Перспективы', 'Экспозиции',
      'Показ', 'Опыты', 'Актуальность'], 'правило'),
    ('business', 'Деловая зона', 'business', '#2D3051', '#FFFFFF', 'ИННОВАЦИИ',
     ['Технологии', 'Аналитика', 'Консультации', 'Сотрудничество', 'Разработки',
      'Продуктивность', 'Перспективы', 'Презентации', 'Форумы'], 'правило'),
]

# ─── иконки: тематические с полосы 17 ──────────────────────────────────────
THEME_ICONS = [('ic-heart', 'Сердце'), ('ic-waves', 'Волны'),
               ('ic-gamepad', 'Геймпад'), ('ic-boat', 'Теплоход'),
               ('ic-plane', 'Самолёт'), ('ic-cap', 'Конфедератка')]

ICON_RULES = [
    ('Единая толщина линий', 'Новая иконка держит ту же толщину, что и набор.'),
    ('Простота и минимализм', 'Никакой лишней детализации: форма читается в размер таблички.'),
    ('Фирменные цвета', 'Только палитра бренда, без посторонних оттенков.'),
    ('Согласованность форм', 'Геометрия новых иконок совпадает с существующими.'),
]

# ─── бенто: принципы с полосы «Принципы построения дизайн макетов» ─────────
BENTO_RULES = [
    ('Модульность и структура', 'Сетка из блоков: текст, изображение и графика живут в своих модулях.'),
    ('Баланс и пропорции', 'Ни один блок не перегружает макет, у каждого есть воздух.'),
    ('Единообразие', 'Цвета, типографика и иконки подчиняются одним правилам во всех форматах.'),
    ('Чёткость', 'Минимум декора, информация подаётся коротко.'),
]

BENTO_FORMATS = [
    ('wide', 'Горизонтальный экран'),
    ('post', 'Пост в соцсетях'),
    ('story', 'Вертикальная сторис'),
]

# ─── навигация: слова и иконки с полос 27-28 ───────────────────────────────
NAV_WORDS = ['КАФЕ', 'ТУАЛЕТ', 'ГАРДЕРОБ', 'ВХОД', 'ВЫХОД', 'ИНФОРМАЦИЯ', 'ЛЕКТОРИЙ']
NAV_ICONS = [('nav-coffee', 'Кафе'), ('nav-wc', 'Туалет'), ('nav-hanger', 'Гардероб'),
             ('nav-enter', 'Вход'), ('nav-exit', 'Выход'), ('nav-info', 'Информация')]
NAV_ARROWS = [('nav-right', 'Прямо'), ('nav-up', 'Вверх'),
              ('nav-down-l', 'Налево вниз'), ('nav-down-r', 'Направо вниз')]

# ─── носители ──────────────────────────────────────────────────────────────
MEDIA = [
    ('citylight', 'Ситиформаты выставки «Самара» в переходе метро', 'Печать',
     'Три ситиформата подряд: маскот, столбик слов ядра и QR. Меняется только образ '
     'Ладушки и набор слов, каркас макета один.'),
    ('tablet', 'Расписание событий выставки на планшете', 'Цифра',
     'Тот же макет на планшете: логотипный блок, маскот, кнопка. Фон — кривая паруса.'),
    ('banner-welcome', 'Баннер «Познакомься с Самарской областью»', 'Web',
     'Градиент B8C5EC → EACEB6, лента с приветствием, фотография Волги в правой части.'),
    ('app-welcome', 'Стартовый экран приложения', 'Приложение',
     'Маскот в образе для туризма, кнопка «Начать» персиковым — акцент из палитры.'),
    ('app-schedule', 'Экран расписания активностей', 'Приложение',
     'Таблица дня в тёмно-синем: время слева, событие справа, маскот в шапке.'),
    ('banner-win', 'Баннер розыгрыша', 'Web',
     'Маскот с подарком, лента «Добро пожаловать», фотография набережной.'),
]

WALLS = [
    ('wall-volga', 'Стена зоны: волна, экран и слова ядра',
     'Стена целиком: волна из иконки «Волны», экран с датами 1586 и 1737, '
     'вертикальные панели и слова ядра поверх заливки.', ''),
    ('screen-players', 'Экран с игроками ФК «Крылья Советов»',
     'Ко-брендинг: знак выставки «Россия» рядом со знаком региона, слова ядра '
     'по краям кадра.', ''),
    ('screen-level', 'Экран выбора уровня',
     'Интерфейс интерактива: маскот в мантии и четыре уровня сложности.', 'sm'),
]

# ─── стиль в зале: съёмка выставки ─────────────────────────────────────────
LIVE = [
    ('Game_kinect', 'Спортивная зона выставки «Самара»',
     'Маскот в трёх спортивных образах прямо на стене, слова ядра поверх '
     'волны — та же раскладка, что в гайде.'),
    ('Inform_samara', 'Информационные панели выставки',
     'Чипы «Творчество» и «Прогресс» над панелями, знак региона в углу.'),
    ('LED_Lector_Samara', 'Экран лектория',
     'Заставка «История и архитектура»: логотипный блок, линейная графика '
     'и тёмно-синий фон из палитры.'),
    ('VR_Samara', 'Экран муниципальных образований',
     'Плитка карточек по бенто-принципу: крупный блок и ряд мелких.'),
]

OUT = [
    ('Система, а не альбом',
     'Каждый раздел заканчивается правилом, по которому собирается новый макет, '
     'а не единственным готовым примером.'),
    ('Один шрифт на всё',
     'Manrope в шести весах закрывает заголовки, текст и подписи — на печати, '
     'на экранах и в навигации.'),
    ('Маскот держит пространство',
     'Ладушка появляется в каждой зоне в своём образе и связывает залы между собой.'),
    ('Стиль пережил площадку',
     'Язык стенда с ВДНХ переехал в музейные залы без перерисовки: те же цвета, '
     'слова и маскот.'),
]


def hero():
    facts = ''.join(f'<div class="sb-fact"><b>{v}</b><span>{c}</span></div>'
                    for v, c in FACTS)
    chips = ''.join(f'<span class="sb-hchip sb-c{i % 3}">{w}</span>'
                    for i, w in enumerate(['Инновации', 'Культура', 'Открытия',
                                           'Технологии', 'Творчество', 'Встречи']))
    return f'''<section class="sb-hero">
<div class="sb-hero-bg">{svg('sail', 'sb-sail-bg', '#F4E3DB')}</div>
<div class="sb-wrap sb-hero-in">
 <div class="sb-hero-tx">
  <div class="sb-hero-mark">{svg('mark')}</div>
  <p class="sb-eyebrow">Creative &amp; Design · Правительство Самарской области · 2024</p>
  <h1>Фирменный стиль<br>выставки «Самара»</h1>
  <p class="sb-lead">Руководство по использованию фирменного стиля на 28 полос: логотип,
   палитра, шрифт, маскот «Ладушка» в шестнадцати образах и правила, по которым
   собирается любая стена, табличка и экран выставки в Музее им. П. В. Алабина.</p>
  <div class="sb-hchips">{chips}</div>
  <div class="sb-facts">{facts}</div>
 </div>
 <div class="sb-hero-fig">{png('hero', 'Маскот «Ладушка» — базовый образ', 'sb-hero-mascot', lazy=False)}</div>
</div></section>'''


def task():
    cards = ''.join(f'<article class="sb-task-c sb-r"><h3>{t}</h3><p>{b}</p></article>'
                    for t, b in TASK)
    scope = ''.join(f'<li>{s}</li>' for s in SCOPE)
    secs = ''.join(f'<span class="sb-sec">{s}</span>' for s in SECTIONS)
    return f'''<section class="sb-sec-task" id="task"><div class="sb-wrap">
<div class="sb-task-grid">{cards}</div>
<div class="sb-task-two">
 <div class="sb-r"><h3 class="sb-h3">Что вошло в руководство</h3><ul class="sb-scope">{scope}</ul></div>
 <div class="sb-r"><h3 class="sb-h3">Пятнадцать разделов гайда</h3>
  <div class="sb-secs">{secs}</div>
  <p class="sb-note">Содержание с полосы 2. Дальше на этой странице — то, чем
   пользуются каждый день: знак, цвет, шрифт, маскот, ядро, макет, навигация.</p>
 </div>
</div></div></section>'''


def mark():
    rows = ''
    for title, items in SAFETY:
        li = ''.join(f'<li><b>{x}</b><span>{d}</span></li>' for x, d in items)
        rows += f'<div class="sb-safe-c"><h4>{title}</h4><ul>{li}</ul></div>'
    blocks = ''.join(
        f'<div class="sb-lblock" style="background:{bg};color:{fg}">'
        f'{svg("mark", "sb-lblock-m", fg)}<span>Самарская<br>область</span></div>'
        for bg, fg in [('#2D3051', '#FFFFFF'), ('#368AB5', '#FFFFFF'),
                       ('#F7D5B1', '#2D3051'), ('#046081', '#FFFFFF'),
                       ('#F4E3DB', '#2D3051'),
                       ('linear-gradient(120deg,#B8C5EC,#EACEB6)', '#2D3051')])
    return f'''<section class="sb-sec-mark" id="mark"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Логотип</p>
 <h2>Ладья с парусом и два способа её поставить</h2>
 <p class="sb-sub">Знак вынут из гайда кривыми, а не картинкой: рядом с ним живут
  поля, по которым логотипный блок собирается на любом носителе.</p></header>
<div class="sb-mark-grid sb-r">
 <figure class="sb-mark-fig">
  <figcaption>Горизонтальная версия</figcaption>
  <div class="sb-logo sb-logo-h">
   <div class="sb-logo-in">
    <div class="sb-logo-m">{svg('mark')}</div>
    <span class="sb-gap" data-lab="1,25X"></span>
    <div class="sb-logo-w">Самарская<br>область</div>
    <span class="sb-field-lab">3X</span>
   </div>
   <span class="sb-guide sb-g-unit"><i>1X</i></span>
  </div>
 </figure>
 <figure class="sb-mark-fig">
  <figcaption>Вертикальная версия</figcaption>
  <div class="sb-logo sb-logo-v">
   <div class="sb-logo-in">
    <div class="sb-logo-m">{svg('mark')}</div>
    <span class="sb-gap" data-lab="1,25X"></span>
    <div class="sb-logo-w">Самарская<br>область</div>
    <span class="sb-field-lab">2X</span>
   </div>
   <span class="sb-guide sb-g-unit"><i>1X</i></span>
  </div>
 </figure>
</div>
<div class="sb-safe-row sb-r"><button class="sb-btn" type="button" data-safe-toggle
  aria-pressed="false">Показать поля</button>{rows}</div>
<div class="sb-lblocks sb-r">{blocks}</div>
<p class="sb-note sb-r">Монохромная версия допускается в чёрном и белом. Шесть
 фирменных блоков — это те же два логотипа на заливках из палитры.</p>
</div></section>'''


def palette():
    def chips(rows):
        out = ''
        for hexv, name, mode in rows:
            style = f'background:#{hexv}'
            if hexv == 'B8C5EC':
                style = 'background:linear-gradient(160deg,#B8C5EC,#EACEB6)'
            if hexv == '307FA9':
                style = 'background:linear-gradient(160deg,#307FA9,#014A6D)'
            border = ' sb-col-b' if hexv in ('FFFFFF',) else ''
            out += (f'<button class="sb-col sb-col-{mode}{border}" type="button" '
                    f'style="{style}" data-hex="#{hexv}">'
                    f'<span class="sb-col-h">#{hexv}</span>'
                    f'<span class="sb-col-n">{name}</span>'
                    f'<span class="sb-col-copy">Скопировано</span></button>')
        return out
    return f'''<section class="sb-sec-pal" id="palette"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Цвета</p>
 <h2>Шесть основных, шесть дополнительных</h2>
 <p class="sb-sub">Тёмно-синий держит фон и текст, синий отвечает за зоны,
  бежевый и персиковый — за тепло и акценты. Нажмите на плашку, чтобы скопировать код.</p></header>
<h3 class="sb-h3 sb-r">Основные цвета</h3>
<div class="sb-cols sb-r">{chips(MAIN_COLORS)}</div>
<h3 class="sb-h3 sb-r">Дополнительные цвета и градиенты</h3>
<div class="sb-cols sb-r">{chips(ADD_COLORS)}</div>
</div></section>'''


def typo():
    ws = ''.join(f'<div class="sb-w"><span style="font-weight:{w}">Самара</span>'
                 f'<i>{n} · {w}</i></div>' for w, n in WEIGHTS)
    roles = ''.join(f'<div class="sb-role sb-r"><p class="sb-role-t">{t}</p>'
                    f'<div class="{cls}">{b}</div></div>' for t, b, cls in TYPE_ROLES)
    return f'''<section class="sb-sec-type" id="type"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Шрифты</p>
 <h2>Manrope и больше ничего</h2>
 <p class="sb-sub">Гайд отдаёт одному шрифту все роли: заголовки, основной текст
  и подписи. Разница только в весе и трекинге — эта страница набрана по тому же правилу.</p></header>
<div class="sb-type-hero sb-r"><span>Manrope</span></div>
<div class="sb-ws sb-r">{ws}</div>
<div class="sb-roles">{roles}</div>
</div></section>'''


def mascot():
    thumbs = ''.join(
        f'<button class="sb-mt" type="button" data-m="{k}"'
        f'{pressed(i == 0)}>'
        f'{png(k, f"Маскот «Ладушка»: {t.lower()}")}'
        f'<span>{t}</span></button>' for i, (k, t, _d) in enumerate(MASCOTS))
    return f'''<section class="sb-sec-mascot" id="mascot"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Маскот</p>
 <h2>Ладушка переодевается, но остаётся собой</h2>
 <p class="sb-sub">Шестнадцать образов одного персонажа. Меняются одежда, атрибут
  и поза — под тему зоны; лицо, коса и пропорции не меняются никогда.</p></header>
<div class="sb-mascot sb-r">
 <div class="sb-mstage">
  <div class="sb-mstage-fig">
   <img class="sb-ghost" src="{IMG}/business.png" alt="" width="{SIZE['business'][0]}"
    height="{SIZE['business'][1]}" style="--ax:{ANCHOR['business']}" loading="lazy"
    decoding="async" hidden>
   <img class="sb-mbig" src="{IMG}/hero.png" alt="Маскот «Ладушка»"
    width="{SIZE['hero'][0]}" height="{SIZE['hero'][1]}" style="--ax:{ANCHOR['hero']}"
    decoding="async"></div>
  <div class="sb-mstage-tx">
   <p class="sb-mzone">Базовый</p>
   <p class="sb-mdesc">Белая блузка, синяя юбка, приветственный жест</p>
   <button class="sb-btn sb-btn-l" type="button" data-stack aria-pressed="false">Сравнить силуэты</button>
   <p class="sb-note">Под фигурой встаёт силуэт другого образа, совмещённый по
    точке опоры. Видно, что рост, разворот плеч и посадка головы у всех образов
    одни и те же: это один персонаж, а не серия иллюстраций.</p>
  </div>
 </div>
 <div class="sb-mts">{thumbs}</div>
</div></div></section>'''


def core():
    words = ''.join(f'<span class="sb-cw sb-c{i % 3}">{w}</span>'
                    for i, w in enumerate(CORE))
    tabs = ''.join(
        f'<button class="sb-zt" type="button" data-z="{k}"'
        f'{pressed(i == 0)}>{n}</button>'
        for i, (k, n, *_r) in enumerate(ZONES))
    walls = ''.join(
        f'<figure class="sb-wall sb-wall-{m} sb-r">{jpg(k, a)}'
        f'<figcaption>{c}</figcaption></figure>' for k, a, c, m in WALLS)
    return f'''<section class="sb-sec-core" id="core"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Семантическое ядро и оформление пространств</p>
 <h2>Сорок шесть слов, из которых собирается стена</h2>
 <p class="sb-sub">Ядро — это список того, о чём выставка говорит с гостем.
  Слова верстаются чипами трёх типов: белым, персиковым и синим. Из них и маскота
  собирается любая зона.</p></header>
<div class="sb-core-words sb-r">{words}</div>
<div class="sb-builder sb-r">
 <div class="sb-b-head">
  <div class="sb-zts">{tabs}</div>
  <button class="sb-btn sb-btn-l" type="button" data-reshuffle>Пересобрать</button>
 </div>
 <div class="sb-stage" data-stage>
  <div class="sb-stage-m"></div>
  <div class="sb-stage-w"></div>
  <p class="sb-stage-note"></p>
 </div>
 <p class="sb-note">Раскладка каждый раз считается заново: слова расставляются
  случайно и расталкиваются, пока не перестанут пересекаться. Игровая зона и
  лекторий разобраны в самом гайде, остальные четыре собраны по тому же правилу.</p>
</div>
<div class="sb-walls">{walls}</div>
</div></section>'''


def pattern():
    icons = ''.join(f'<figure class="sb-ic">{svg(k)}'
                    f'<figcaption>{n}</figcaption></figure>' for k, n in THEME_ICONS)
    rules = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in ICON_RULES)
    return f'''<section class="sb-sec-pat" id="pattern"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Паттерны и стилеобразующие элементы</p>
 <h2>Парус со знака становится фоном</h2>
 <p class="sb-sub">Основа фоновых паттернов — та же кривая, что в логотипе.
  Её увеличивают, обрезают краем макета и кладут светлым тоном под контент.</p></header>
<div class="sb-pat sb-r" data-pat>
 <div class="sb-pat-step"><div class="sb-pat-box">{svg('mark', 'sb-pat-mark')}</div><p>Знак</p></div>
 <div class="sb-pat-step"><div class="sb-pat-box">{svg('sail', 'sb-pat-line', inline=True)}</div><p>Кривая паруса</p></div>
 <div class="sb-pat-step"><div class="sb-pat-box sb-pat-fill">{svg('sail', 'sb-pat-big', '#E3C8B8')}
  <div class="sb-pat-mock"><span class="sb-pat-mock-l">{svg('mark')}<i>Самарская<br>область</i></span>
   <b>Расписание событий выставки «Самара»</b><em>Узнать больше</em></div>
  </div><p>Фон макета</p></div>
</div>
<div class="sb-icons sb-r">
 <div><h3 class="sb-h3">Иконки</h3><div class="sb-ics">{icons}</div></div>
 <ul class="sb-irules">{rules}</ul>
</div>
</div></section>'''


def bento():
    rules = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in BENTO_RULES)
    tabs = ''.join(
        f'<button class="sb-ft" type="button" data-f="{k}"'
        f'{pressed(i == 0)}>{n}</button>'
        for i, (k, n) in enumerate(BENTO_FORMATS))
    cells = ''.join(f'<div class="sb-bcell sb-bc{i}"><span></span></div>' for i in range(7))
    return f'''<section class="sb-sec-bento" id="bento"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Принципы построения макетов</p>
 <h2>Бенто: макет собирается из блоков</h2>
 <p class="sb-sub">Каждый элемент живёт в своём модуле — как в бенто-ланче.
  Меняется формат, а не композиция: блоки перестраиваются, правила остаются.</p></header>
<div class="sb-bento sb-r">
 <div class="sb-fts">{tabs}</div>
 <div class="sb-bgrid" data-bento data-f="wide">{cells}</div>
</div>
<ul class="sb-brules sb-r">{rules}</ul>
</div></section>'''


def nav():
    words = ''.join(f'<button class="sb-nw" type="button" data-w="{w}"'
                    f'{pressed(i == 0)}>{w}</button>'
                    for i, w in enumerate(NAV_WORDS))
    icons = ''.join(f'<button class="sb-ni" type="button" data-i="{k}" title="{n}"'
                    f'{pressed(i == 0)}>'
                    f'{svg(k)}</button>'
                    for i, (k, n) in enumerate(NAV_ICONS))
    arrows = ''.join(f'<button class="sb-ni" type="button" data-a="{k}" title="{n}"'
                     f'{pressed(i == 0)}>'
                     f'{svg(k)}</button>'
                     for i, (k, n) in enumerate(NAV_ARROWS))
    return f'''<section class="sb-sec-nav" id="nav"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Навигация</p>
 <h2>Табличка режется по модулю X</h2>
 <p class="sb-sub">В гайде нет «примерно так»: высота знака — это X, поля сверху
  и снизу — 3/4X, зазор между блоками — 1/2X. Соберите свою табличку и включите
  сетку — размеры пересчитаются сами.</p></header>
<div class="sb-navb sb-r">
 <div class="sb-nav-stage">
  <div class="sb-sign" data-sign style="--x:48px">
   <span class="sb-sign-ic" data-sign-ic>{svg('nav-coffee')}</span>
   <span class="sb-sign-tx" data-sign-tx>КАФЕ</span>
   <span class="sb-sign-ar" data-sign-ar>{svg('nav-right')}</span>
   <span class="sb-mes sb-mes-t"><i>3/4X</i></span>
   <span class="sb-mes sb-mes-b"><i>3/4X</i></span>
   <span class="sb-mes sb-mes-x"><i>X</i></span>
   <span class="sb-mes sb-mes-g"><i>1/2X</i></span>
  </div>
 </div>
 <div class="sb-nav-ctl">
  <div class="sb-ctl"><p class="sb-ctl-t">Надпись</p><div class="sb-nws">{words}</div>
   <label class="sb-inp"><span>Своё слово</span>
    <input type="text" maxlength="16" data-sign-input placeholder="НАПРИМЕР, ЛЕКТОРИЙ"></label></div>
  <div class="sb-ctl"><p class="sb-ctl-t">Иконка</p><div class="sb-nis">{icons}</div>
   <label class="sb-chk"><input type="checkbox" data-sign-noic> Без иконки</label></div>
  <div class="sb-ctl"><p class="sb-ctl-t">Стрелка</p><div class="sb-nis">{arrows}</div></div>
  <div class="sb-ctl"><p class="sb-ctl-t">Модуль X <b data-xv>48</b> px</p>
   <input type="range" min="24" max="64" value="48" data-sign-x class="sb-range">
   <label class="sb-chk"><input type="checkbox" data-sign-grid checked> Показывать сетку</label></div>
 </div>
</div>
</div></section>'''


def media():
    cards = ''.join(
        f'<figure class="sb-md sb-r"><div class="sb-md-i">{jpg(k, a)}</div>'
        f'<figcaption><span class="sb-md-t">{t}</span><b>{a}</b><p>{d}</p></figcaption></figure>'
        for k, a, t, d in MEDIA)
    return f'''<section class="sb-sec-media" id="media"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Носители</p>
 <h2>Одни правила — печать, экран, приложение</h2>
 <p class="sb-sub">Примеры из гайда: везде один логотипный блок, один шрифт,
  один набор цветов и маскот в подходящем образе.</p></header>
<div class="sb-mds">{cards}</div>
</div></section>'''


def live():
    cards = ''.join(
        f'<figure class="sb-lv sb-r">{photo(k, a)}'
        f'<figcaption><b>{a}</b><p>{d}</p></figcaption></figure>' for k, a, d in LIVE)
    return f'''<section class="sb-sec-live" id="live"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Стиль в зале</p>
 <h2>Как это выглядит на выставке</h2>
 <p class="sb-sub">Съёмка выставки «Самара» в Музее им. П. В. Алабина: те же чипы
  слов, тот же маскот и та же палитра, что на полосах руководства.</p></header>
<div class="sb-lvs">{cards}</div>
<p class="sb-note sb-r">Оснащение и мультимедиа выставки — отдельный кейс:
 <a href="/portfolio/samara-exhibition/">выставка «Самара» в Музее им. П. В. Алабина</a>.
 Стенд, с которого стиль переехал в музей, — <a href="/samara_vdnh/">на выставке-форуме
 «Россия» на ВДНХ</a>.</p>
</div></section>'''


def out():
    cards = ''.join(f'<article class="sb-out-c sb-r"><h3>{t}</h3><p>{d}</p></article>'
                    for t, d in OUT)
    return f'''<section class="sb-sec-out" id="out"><div class="sb-wrap">
<header class="sb-head sb-r"><p class="sb-kicker">Итог</p>
 <h2>Что даёт такое руководство</h2></header>
<div class="sb-outs">{cards}</div>
<figure class="sb-museum sb-r">{jpg('museum', 'Музей им. П. В. Алабина, Самара')}
 <figcaption>Музей им. П. В. Алабина, Самара, ул. Ленинская, 142 — площадка выставки «Самара».</figcaption></figure>
</div></section>'''


PAGE_CSS = """<style>
.sb{--ink:#2D3051;--blue:#368AB5;--sand:#F4E3DB;--peach:#F7D5B1;--deep:#046081;
 --navy:#063A5A;--pink:#F6A4B1;--royal:#567EF3;--lilac:#B8C5EC;--clay:#EACEB6;
 --paper:#FFFFFF;--line:rgba(45,48,81,.14);
 font-family:'Manrope',system-ui,-apple-system,'Segoe UI',sans-serif;
 color:var(--ink);background:var(--paper);overflow-x:hidden;}
.sb *{box-sizing:border-box;}
.sb-wrap{max-width:1240px;margin:0 auto;padding:0 24px;}
.sb h1,.sb h2,.sb h3,.sb h4,.sb p,.sb ul,.sb figure,.sb figcaption{margin:0;}
.sb ul{list-style:none;padding:0;}
.sb img{max-width:100%;height:auto;display:block;}
.sb a{color:inherit;}
.sb-r{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease;}
.sb-r.is-in{opacity:1;transform:none;}
.no-js .sb-r{opacity:1;transform:none;}
.sb-btn{font:inherit;font-weight:600;color:var(--ink);background:transparent;
 border:1.5px solid var(--ink);border-radius:999px;padding:11px 22px;cursor:pointer;
 transition:background .2s,color .2s;}
.sb-btn:hover{background:var(--ink);color:#fff;}
.sb-btn[aria-pressed="true"]{background:var(--ink);color:#fff;}
.sb-btn-l{border-color:rgba(45,48,81,.3);}
.sb-kicker{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
 color:var(--blue);margin-bottom:14px;}
.sb-head{max-width:820px;margin-bottom:44px;}
.sb-head h2{font-size:clamp(28px,4.4vw,50px);font-weight:700;line-height:1.08;
 letter-spacing:-.02em;}
.sb-sub{margin-top:18px;font-size:clamp(15px,1.7vw,18px);line-height:1.62;font-weight:400;
 color:rgba(45,48,81,.78);}
.sb-h3{font-size:clamp(18px,2.2vw,22px);font-weight:700;margin-bottom:18px;}
.sb-note{font-size:14px;line-height:1.6;color:rgba(45,48,81,.6);max-width:760px;}
.sb-note a{color:var(--blue);text-decoration:underline;text-underline-offset:3px;}
.sb section{position:relative;}

/* ── герой ─────────────────────────────────────────────────────────────── */
.sb-hero{background:var(--ink);color:#fff;padding:clamp(96px,12vw,150px) 0 clamp(56px,7vw,90px);
 position:relative;overflow:hidden;}
.sb-hero-bg{position:absolute;inset:0;pointer-events:none;}
.sb-sail-bg{position:absolute;right:-22%;top:-24%;height:184%;width:auto;opacity:.13;
 stroke-width:2.4;}
.sb-hero-in{display:grid;grid-template-columns:minmax(0,1.28fr) minmax(0,.72fr);gap:40px;
 align-items:center;position:relative;}
.sb-eyebrow{font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;
 color:var(--peach);margin-bottom:22px;}
.sb-hero h1{font-size:clamp(32px,5.2vw,64px);font-weight:800;line-height:1.02;
 letter-spacing:-.03em;}
.sb-lead{margin-top:26px;max-width:620px;font-size:clamp(15px,1.8vw,19px);line-height:1.62;
 color:rgba(255,255,255,.82);font-weight:300;}
.sb-hchips{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px;}
.sb-hchip,.sb-cw{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
 padding:7px 13px;border-radius:6px;white-space:nowrap;}
.sb-c0{background:#fff;color:var(--ink);}
.sb-c1{background:var(--peach);color:var(--ink);}
.sb-c2{background:var(--royal);color:#fff;}
.sb-facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-top:42px;
 border-top:1px solid rgba(255,255,255,.2);padding-top:26px;}
.sb-fact b{display:block;font-size:clamp(26px,3.6vw,42px);font-weight:800;line-height:1;
 letter-spacing:-.02em;}
.sb-fact span{display:block;margin-top:8px;font-size:13px;line-height:1.4;font-weight:400;
 color:rgba(255,255,255,.65);}
.sb-hero-fig{position:relative;display:flex;justify-content:center;align-items:flex-end;}
.sb .sb-hero-mascot{height:clamp(300px,34vw,470px);width:auto;
 filter:drop-shadow(0 30px 60px rgba(0,0,0,.35));}
.sb-hero-mark{width:clamp(52px,5vw,68px);margin-bottom:20px;color:var(--peach);}
.sb-hero-mark svg{width:100%;height:auto;}

/* ── задача ────────────────────────────────────────────────────────────── */
.sb-sec-task{padding:clamp(64px,8vw,110px) 0;}
.sb-task-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;}
.sb-task-c{background:var(--sand);border-radius:20px;padding:32px;}
.sb-task-c h3{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
 color:var(--blue);margin-bottom:16px;}
.sb-task-c p{font-size:16px;line-height:1.62;font-weight:400;}
.sb-task-two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:44px;margin-top:56px;}
.sb-scope li{position:relative;padding:12px 0 12px 28px;border-bottom:1px solid var(--line);
 font-size:15px;line-height:1.5;}
.sb-scope li:before{content:"";position:absolute;left:4px;top:19px;width:8px;height:8px;
 border-radius:50%;background:var(--peach);}
.sb-secs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;}
.sb-sec{font-size:13px;font-weight:500;padding:8px 14px;border-radius:999px;
 border:1px solid var(--line);}

/* ── логотип ───────────────────────────────────────────────────────────── */
.sb-sec-mark{padding:clamp(64px,8vw,110px) 0;background:#F7F7F9;}
.sb-mark-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;}
.sb-mark-fig figcaption{font-size:14px;font-weight:600;color:rgba(45,48,81,.6);margin-bottom:14px;}
/* Геометрия честная: X снят с красных линий-замеров полосы 4 брендбука.
   Ширина знака = 8,55X (горизонтальная версия) и 6,56X (вертикальная),
   охранное поле = 3X и 2X, зазор до наборной части = 1,25X. */
.sb-logo{position:relative;background:#fff;border-radius:20px;display:flex;
 align-items:center;justify-content:center;min-height:clamp(200px,24vw,280px);}
.sb-logo-h{--x:clamp(7px,1vw,11px);padding:calc(var(--x)*3);}
.sb-logo-v{--x:clamp(9px,1.25vw,14px);padding:calc(var(--x)*2);}
.sb-logo-in{display:flex;align-items:center;}
.sb-gap{flex:none;width:calc(var(--x)*1.25);align-self:stretch;position:relative;}
.sb-logo-v .sb-gap{width:auto;height:calc(var(--x)*1.25);}
.sb-logo.is-safe .sb-gap{border-left:1px solid #E2372F;border-right:1px solid #E2372F;}
.sb-logo-v.is-safe .sb-gap{border:0;border-top:1px solid #E2372F;border-bottom:1px solid #E2372F;}
.sb-logo.is-safe .sb-gap:after{content:attr(data-lab);position:absolute;left:50%;
 transform:translateX(-50%);top:-18px;font-size:10px;font-weight:700;color:#E2372F;
 background:#fff;padding:1px 4px;white-space:nowrap;}
.sb-logo-v.is-safe .sb-gap:after{left:auto;right:-2px;transform:none;top:calc(50% - 8px);}
.sb-logo-v .sb-logo-in{flex-direction:column;}
.sb-logo-m{flex:none;}
.sb-logo-h .sb-logo-m{width:calc(var(--x)*8.55);}
.sb-logo-v .sb-logo-m{width:calc(var(--x)*6.56);}
.sb-logo-m svg{width:100%;height:auto;}
.sb-logo-w{font-size:calc(var(--x)*1.62);font-weight:500;line-height:1.08;
 letter-spacing:.01em;text-transform:uppercase;}
.sb-logo-v .sb-logo-w{text-align:center;}
.sb-guide{position:absolute;border:1px solid #E2372F;opacity:0;transition:opacity .25s;
 pointer-events:none;}
.sb-guide i{position:absolute;font-size:10px;font-style:normal;font-weight:700;
 color:#E2372F;background:#fff;padding:1px 4px;white-space:nowrap;}
.sb-logo.is-safe .sb-guide{opacity:1;}
/* охранное поле рисуем контуром вокруг самого блока: outline-offset и есть поле */
.sb-logo.is-safe .sb-logo-in{outline:1px solid #E2372F;outline-offset:calc(var(--x)*3);}
.sb-logo-v.is-safe .sb-logo-in{outline-offset:calc(var(--x)*2);}
.sb-field-lab{position:absolute;right:calc(var(--x)*-3);top:calc(var(--x)*-3 - 18px);
 font-size:10px;font-weight:700;color:#E2372F;background:#fff;padding:1px 4px;opacity:0;
 transition:opacity .25s;}
.sb-logo-v .sb-field-lab{right:calc(var(--x)*-2);top:calc(var(--x)*-2 - 18px);}
.sb-logo.is-safe .sb-field-lab{opacity:1;}
.sb-logo-in{position:relative;}
/* модуль X: квадрат в углу охранного поля */
.sb-g-unit{left:calc(var(--x)*1.4);bottom:calc(var(--x)*1.4);width:var(--x);height:var(--x);
 background:rgba(226,55,47,.14);}
.sb-g-unit i{left:calc(100% + 4px);top:calc(50% - 8px);}
.sb-safe-row{display:grid;grid-template-columns:auto repeat(2,minmax(0,1fr));gap:24px;
 align-items:start;margin-top:28px;}
.sb-safe-c h4{font-size:14px;font-weight:700;margin-bottom:10px;}
.sb-safe-c li{display:flex;gap:10px;font-size:14px;line-height:1.5;padding:5px 0;
 color:rgba(45,48,81,.75);}
.sb-safe-c li b{flex:none;min-width:44px;color:#E2372F;}
.sb-lblocks{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin-top:44px;}
.sb-lblock{border-radius:14px;padding:22px 16px;display:flex;flex-direction:column;
 align-items:flex-start;gap:12px;min-height:126px;justify-content:center;}
.sb-lblock-m{width:34px;height:auto;stroke-width:8;}
.sb-lblock span{font-size:11px;font-weight:600;line-height:1.2;text-transform:uppercase;
 letter-spacing:.04em;}

/* ── палитра ───────────────────────────────────────────────────────────── */
.sb-sec-pal{padding:clamp(64px,8vw,110px) 0;}
.sb-cols{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin-bottom:44px;}
.sb-col{position:relative;border:0;border-radius:14px;min-height:clamp(150px,18vw,210px);
 padding:18px;text-align:left;cursor:pointer;font:inherit;display:flex;
 flex-direction:column;justify-content:flex-end;gap:4px;transition:transform .2s;}
.sb-col:hover{transform:translateY(-4px);}
.sb-col-b{box-shadow:inset 0 0 0 1px var(--line);}
.sb-col-h{font-size:14px;font-weight:700;letter-spacing:.04em;}
.sb-col-n{font-size:12px;font-weight:400;opacity:.75;}
.sb-col-light{color:#fff;}
.sb-col-dark{color:var(--ink);}
.sb-col-copy{position:absolute;left:18px;top:16px;font-size:11px;font-weight:700;
 letter-spacing:.08em;text-transform:uppercase;opacity:0;transition:opacity .2s;}
.sb-col.is-copied .sb-col-copy{opacity:1;}

/* ── шрифт ─────────────────────────────────────────────────────────────── */
.sb-sec-type{padding:clamp(64px,8vw,110px) 0;background:var(--sand);}
.sb-type-hero{font-size:clamp(64px,17vw,220px);font-weight:200;line-height:.9;
 letter-spacing:-.04em;margin-bottom:26px;}
.sb-ws{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;
 border-top:1px solid rgba(45,48,81,.2);padding-top:24px;}
.sb-w span{display:block;font-size:clamp(20px,2.6vw,30px);line-height:1.2;}
.sb-w i{display:block;margin-top:6px;font-size:11px;font-style:normal;font-weight:600;
 letter-spacing:.06em;text-transform:uppercase;color:rgba(45,48,81,.55);}
.sb-roles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:52px;}
.sb-role-t{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
 color:var(--blue);margin-bottom:14px;}
.sb-t-h{font-size:clamp(24px,3.2vw,38px);font-weight:600;line-height:1.06;text-transform:uppercase;
 letter-spacing:-.01em;}
.sb-t-b{font-size:16px;line-height:1.6;font-weight:400;}
.sb-t-c{font-size:14px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;}

/* ── маскот ────────────────────────────────────────────────────────────── */
.sb-sec-mascot{padding:clamp(64px,8vw,110px) 0;}
.sb-mstage{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:36px;
 align-items:center;background:linear-gradient(140deg,var(--lilac),var(--clay));
 border-radius:24px;padding:clamp(24px,4vw,44px);}
.sb-mstage-fig{position:relative;min-height:clamp(300px,38vw,440px);}
.sb .sb-mbig,.sb .sb-ghost{position:absolute;bottom:0;left:50%;height:clamp(260px,36vw,420px);
 width:auto;transform:translateX(calc(var(--ax,.5) * -100%));}
.sb .sb-mbig{filter:drop-shadow(0 24px 40px rgba(45,48,81,.28));}
/* силуэт: плоская заливка по альфе, никакого просвечивающего рендера.
   Сдвиг на десятую долю ширины — иначе он целиком прячется за фигурой */
.sb .sb-ghost{filter:brightness(0) saturate(0);opacity:.26;
 transform:translateX(calc(var(--ax,.5) * -100% - 9%));}
.sb .sb-ghost[hidden]{display:none;}
.sb-mzone{font-size:clamp(24px,3.4vw,40px);font-weight:700;letter-spacing:-.02em;}
.sb-mdesc{margin:12px 0 24px;font-size:16px;line-height:1.6;color:rgba(45,48,81,.78);}
.sb-mstage-tx .sb-note{margin-top:18px;}
.sb-mts{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:10px;margin-top:22px;}
.sb-mt{border:1px solid var(--line);border-radius:14px;background:#fff;cursor:pointer;
 padding:10px 6px 8px;font:inherit;display:flex;flex-direction:column;align-items:center;
 gap:6px;transition:border-color .2s,transform .2s,background .2s;}
.sb-mt:hover{transform:translateY(-3px);}
.sb-mt img{height:74px;width:auto;}
.sb-mt span{font-size:10px;font-weight:600;letter-spacing:.03em;text-transform:uppercase;
 color:rgba(45,48,81,.6);text-align:center;overflow-wrap:anywhere;line-height:1.15;}
.sb-mt[aria-pressed="true"]{border-color:var(--ink);background:var(--sand);}
.sb-mt[aria-pressed="true"] span{color:var(--ink);}

/* ── ядро и стена зоны ─────────────────────────────────────────────────── */
.sb-sec-core{padding:clamp(64px,8vw,110px) 0;background:#F7F7F9;}
.sb-core-words{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:46px;}
.sb-core-words .sb-c0{box-shadow:inset 0 0 0 1px var(--line);}
.sb-builder{background:#fff;border-radius:24px;padding:clamp(18px,3vw,30px);}
.sb-b-head{display:flex;flex-wrap:wrap;gap:14px;justify-content:space-between;
 align-items:center;margin-bottom:20px;}
.sb-zts{display:flex;flex-wrap:wrap;gap:8px;}
.sb-zt{font:inherit;font-size:13px;font-weight:600;padding:9px 16px;border-radius:999px;
 border:1px solid var(--line);background:#fff;color:rgba(45,48,81,.7);cursor:pointer;
 transition:.2s;}
.sb-zt:hover{border-color:var(--ink);color:var(--ink);}
.sb-zt[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#fff;}
.sb-stage{position:relative;border-radius:18px;overflow:hidden;min-height:clamp(340px,44vw,520px);
 display:flex;transition:background .45s ease,color .45s ease;padding:clamp(14px,2vw,26px);}
.sb-stage-m{position:relative;flex:none;width:clamp(120px,20%,240px);
 display:flex;align-items:flex-end;justify-content:center;}
.sb-stage-m img{max-height:clamp(240px,36vw,430px);width:auto;
 filter:drop-shadow(0 18px 30px rgba(0,0,0,.22));transition:opacity .35s ease;}
.sb-stage-w{position:relative;flex:1;min-width:0;}
.sb-chip{position:absolute;font-size:clamp(9px,1vw,12px);font-weight:700;letter-spacing:.06em;
 text-transform:uppercase;padding:6px 11px;border-radius:6px;white-space:nowrap;
 opacity:0;transform:scale(.9);transition:opacity .4s ease,transform .4s ease;}
.sb-chip.is-on{opacity:1;transform:none;}
.sb-chip-big{font-size:clamp(20px,3.4vw,44px);font-weight:800;letter-spacing:-.01em;
 padding:10px 22px;border-radius:12px;}
.sb-stage-note{position:absolute;right:clamp(14px,2vw,26px);bottom:14px;font-size:11px;
 font-weight:600;letter-spacing:.08em;text-transform:uppercase;opacity:.65;}
.sb-walls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:48px;}
.sb-wall:first-child{grid-column:1/-1;}
.sb-wall img{border-radius:16px;width:100%;}
.sb-wall-sm img{width:auto;max-width:min(100%,340px);margin:0 auto;image-rendering:auto;}
.sb-wall figcaption{margin-top:12px;font-size:14px;line-height:1.55;color:rgba(45,48,81,.7);}

/* ── паттерн и иконки ──────────────────────────────────────────────────── */
.sb-sec-pat{padding:clamp(64px,8vw,110px) 0;}
.sb-pat{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;}
.sb-pat-box{position:relative;height:clamp(200px,26vw,320px);border-radius:20px;
 background:#F7F7F9;display:flex;align-items:center;justify-content:center;overflow:hidden;
 padding:26px;}
.sb-pat-box svg{height:100%;width:auto;max-width:100%;}
.sb-pat-mark{stroke-width:6;}
.sb-pat-line{fill:none;stroke-width:6;stroke-dasharray:var(--len,3000);
 stroke-dashoffset:var(--len,3000);}
.sb-pat.is-in .sb-pat-line{transition:stroke-dashoffset 1.6s ease .2s;stroke-dashoffset:0;}
.sb-pat-fill{background:var(--sand);align-items:flex-start;justify-content:flex-end;
 flex-direction:column;}
.sb-pat-big{position:absolute;right:-38%;top:-18%;height:150%;stroke-width:4;}
.sb-pat-mock{position:relative;z-index:1;width:100%;display:flex;flex-direction:column;
 align-items:flex-start;gap:10px;}
.sb-pat-mock-l{display:flex;align-items:center;gap:8px;color:var(--ink);}
.sb-pat-mock-l svg{width:26px;height:auto;}
.sb-pat-mock-l i{font-size:9px;font-style:normal;font-weight:600;line-height:1.1;
 text-transform:uppercase;letter-spacing:.04em;}
.sb-pat-mock b{font-size:clamp(15px,1.7vw,20px);font-weight:700;line-height:1.15;}
.sb-pat-mock em{font-style:normal;font-size:11px;font-weight:700;letter-spacing:.06em;
 text-transform:uppercase;color:#fff;background:var(--royal);padding:8px 14px;
 border-radius:8px;}
.sb-pat p{margin-top:12px;font-size:13px;font-weight:600;letter-spacing:.06em;
 text-transform:uppercase;color:rgba(45,48,81,.6);}
.sb-icons{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:44px;
 margin-top:56px;align-items:start;}
.sb-ics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;}
.sb-ic{background:#F7F7F9;border-radius:16px;padding:22px 14px 14px;text-align:center;}
.sb-ic svg{height:52px;width:auto;margin:0 auto;color:var(--blue);}
.sb-ic figcaption{margin-top:12px;font-size:12px;font-weight:600;letter-spacing:.04em;
 text-transform:uppercase;color:rgba(45,48,81,.55);}
.sb-irules li{padding:16px 0;border-bottom:1px solid var(--line);}
.sb-irules b{display:block;font-size:16px;font-weight:700;margin-bottom:6px;}
.sb-irules span{font-size:14px;line-height:1.55;color:rgba(45,48,81,.7);}

/* ── бенто ─────────────────────────────────────────────────────────────── */
.sb-sec-bento{padding:clamp(64px,8vw,110px) 0;background:var(--navy);color:#fff;}
.sb-sec-bento .sb-sub{color:rgba(255,255,255,.72);}
.sb-sec-bento .sb-kicker{color:var(--peach);}
.sb-fts{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px;}
.sb-ft{font:inherit;font-size:13px;font-weight:600;padding:9px 16px;border-radius:999px;
 border:1px solid rgba(255,255,255,.28);background:transparent;color:rgba(255,255,255,.75);
 cursor:pointer;transition:.2s;}
.sb-ft:hover{border-color:#fff;color:#fff;}
.sb-ft[aria-pressed="true"]{background:#fff;border-color:#fff;color:var(--navy);}
.sb-bgrid{display:grid;gap:12px;transition:.5s;}
.sb-bgrid[data-f="wide"]{grid-template-columns:repeat(4,1fr);grid-auto-rows:clamp(56px,7vw,86px);}
.sb-bgrid[data-f="wide"] .sb-bc0{grid-column:span 2;grid-row:span 2;}
.sb-bgrid[data-f="wide"] .sb-bc1{grid-column:span 2;}
.sb-bgrid[data-f="wide"] .sb-bc2{grid-column:span 1;grid-row:span 2;}
.sb-bgrid[data-f="wide"] .sb-bc3{grid-column:span 1;}
.sb-bgrid[data-f="wide"] .sb-bc6{grid-column:span 2;}
.sb-bgrid[data-f="post"]{grid-template-columns:repeat(3,1fr);grid-auto-rows:clamp(62px,8vw,96px);
 max-width:640px;}
.sb-bgrid[data-f="post"] .sb-bc0{grid-column:span 3;grid-row:span 2;}
.sb-bgrid[data-f="post"] .sb-bc1{grid-column:span 2;}
.sb-bgrid[data-f="post"] .sb-bc4{grid-column:span 2;}
.sb-bgrid[data-f="story"]{grid-template-columns:repeat(2,1fr);grid-auto-rows:clamp(54px,7vw,80px);
 max-width:400px;}
.sb-bgrid[data-f="story"] .sb-bc0{grid-column:span 2;grid-row:span 3;}
.sb-bgrid[data-f="story"] .sb-bc1{grid-column:span 2;}
.sb-bgrid[data-f="story"] .sb-bc5{grid-column:span 2;}
.sb-bcell{border-radius:14px;background:rgba(255,255,255,.09);position:relative;
 overflow:hidden;transition:.5s;}
.sb-bcell span{position:absolute;left:14px;right:14px;top:16px;height:8px;border-radius:4px;
 background:rgba(255,255,255,.22);}
.sb-bc0{background:var(--blue);}
.sb-bc0 span{background:rgba(255,255,255,.45);}
.sb-bc2{background:rgba(247,213,177,.85);}
.sb-bc2 span{background:rgba(45,48,81,.28);}
.sb-bc4{background:rgba(86,126,243,.75);}
.sb-brules{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px;margin-top:44px;}
.sb-brules li{border-top:1px solid rgba(255,255,255,.24);padding-top:16px;}
.sb-brules b{display:block;font-size:15px;font-weight:700;margin-bottom:8px;}
.sb-brules span{font-size:14px;line-height:1.55;color:rgba(255,255,255,.7);}

/* ── навигация ─────────────────────────────────────────────────────────── */
.sb-sec-nav{padding:clamp(64px,8vw,110px) 0;}
.sb-navb{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:36px;
 align-items:start;}
.sb-nav-stage{background:#F7F7F9;border-radius:22px;padding:clamp(28px,5vw,56px) 20px;
 display:flex;align-items:center;justify-content:center;min-height:clamp(240px,30vw,340px);
 overflow-x:auto;}
.sb-sign{position:relative;display:flex;align-items:stretch;
 border-radius:calc(var(--x)*.32);overflow:visible;flex:none;}
.sb-sign-ic{flex:none;width:calc(var(--x)*2.5);background:var(--ink);
 border-radius:calc(var(--x)*.32) 0 0 calc(var(--x)*.32);
 display:flex;align-items:center;justify-content:center;}
.sb-sign-ic svg{width:var(--x);height:var(--x);color:#fff;}
.sb-sign-tx{background:var(--royal);color:#fff;font-size:var(--x);font-weight:600;
 line-height:1;letter-spacing:.02em;padding:calc(var(--x)*.75) 0 calc(var(--x)*.75) calc(var(--x)*.5);
 display:flex;align-items:center;}
.sb-sign-ar{background:var(--royal);display:flex;align-items:center;
 padding:0 var(--x) 0 var(--x);border-radius:0 calc(var(--x)*.32) calc(var(--x)*.32) 0;}
.sb-sign-ar svg{width:calc(var(--x)*.9);height:calc(var(--x)*.9);color:#fff;}
.sb-sign.is-noic .sb-sign-ic{display:none;}
.sb-sign.is-noic .sb-sign-tx{border-radius:calc(var(--x)*.32) 0 0 calc(var(--x)*.32);
 padding-left:var(--x);}
.sb-sign.is-noar .sb-sign-ar{padding-left:0;padding-right:calc(var(--x)*.8);}
.sb-sign.is-noar .sb-sign-ar svg{display:none;}
.sb-mes{position:absolute;opacity:0;transition:opacity .25s;pointer-events:none;
 border:1px solid #E2372F;}
.sb-sign.is-grid .sb-mes{opacity:1;}
.sb-mes i{position:absolute;font-size:10px;font-style:normal;font-weight:700;color:#E2372F;
 background:#fff;padding:1px 4px;white-space:nowrap;}
.sb-mes-t{left:0;right:0;top:0;height:calc(var(--x)*.75);}
.sb-mes-t i{left:-38px;top:calc(50% - 8px);}
.sb-mes-b{left:0;right:0;bottom:0;height:calc(var(--x)*.75);}
.sb-mes-b i{left:-38px;top:calc(50% - 8px);}
.sb-mes-x{left:0;right:0;top:calc(var(--x)*.75);height:var(--x);border-left:0;border-right:0;}
.sb-mes-x i{left:-24px;top:calc(50% - 8px);}
.sb-mes-g{left:calc(var(--x)*2.5);top:-16px;bottom:-16px;width:calc(var(--x)*.5);
 border-top:0;border-bottom:0;}
.sb-mes-g i{left:50%;transform:translateX(-50%);top:-18px;}
.sb-sign.is-noic .sb-mes-g{display:none;}
.sb-nav-ctl{display:grid;gap:22px;}
.sb-ctl-t{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
 color:rgba(45,48,81,.55);margin-bottom:12px;}
.sb-ctl-t b{color:var(--ink);}
.sb-nws{display:flex;flex-wrap:wrap;gap:7px;}
.sb-nw{font:inherit;font-size:12px;font-weight:700;letter-spacing:.04em;padding:8px 13px;
 border-radius:999px;border:1px solid var(--line);background:#fff;cursor:pointer;
 color:rgba(45,48,81,.72);transition:.2s;}
.sb-nw[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#fff;}
.sb-nis{display:flex;flex-wrap:wrap;gap:8px;}
.sb-ni{width:46px;height:46px;border-radius:12px;border:1px solid var(--line);background:#fff;
 cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--ink);
 transition:.2s;padding:10px;}
.sb-ni svg{width:100%;height:100%;}
.sb-ni[aria-pressed="true"]{background:var(--ink);color:#fff;border-color:var(--ink);}
.sb-inp{display:block;margin-top:12px;}
.sb-inp span{display:block;font-size:12px;color:rgba(45,48,81,.55);margin-bottom:6px;}
.sb-inp input{font:inherit;font-size:14px;font-weight:600;letter-spacing:.04em;
 text-transform:uppercase;width:100%;padding:11px 14px;border:1px solid var(--line);
 border-radius:12px;background:#fff;color:var(--ink);}
.sb-inp input:focus{outline:2px solid var(--royal);outline-offset:1px;}
.sb-chk{display:flex;align-items:center;gap:8px;margin-top:12px;font-size:14px;
 color:rgba(45,48,81,.75);cursor:pointer;}
.sb-range{width:100%;accent-color:var(--ink);}

/* ── носители ──────────────────────────────────────────────────────────── */
.sb-sec-media{padding:clamp(64px,8vw,110px) 0;background:#F7F7F9;}
.sb-mds{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;}
.sb-md{background:#fff;border-radius:20px;overflow:hidden;display:flex;flex-direction:column;}
.sb-md-i{background:var(--sand);display:flex;align-items:center;justify-content:center;
 padding:18px;min-height:clamp(180px,22vw,250px);}
.sb-md-i img{max-height:clamp(160px,20vw,220px);width:auto;border-radius:8px;}
.sb-md figcaption{padding:22px;}
.sb-md-t{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.1em;
 text-transform:uppercase;color:var(--blue);margin-bottom:10px;}
.sb-md b{display:block;font-size:16px;font-weight:700;line-height:1.35;margin-bottom:8px;}
.sb-md p{font-size:14px;line-height:1.55;color:rgba(45,48,81,.7);}

/* ── стиль в зале ──────────────────────────────────────────────────────── */
.sb-sec-live{padding:clamp(64px,8vw,110px) 0;}
.sb-lvs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-bottom:28px;}
.sb-lv img{border-radius:18px;width:100%;aspect-ratio:4/3;object-fit:cover;}
.sb-lv figcaption{margin-top:14px;}
.sb-lv b{display:block;font-size:16px;font-weight:700;margin-bottom:6px;}
.sb-lv p{font-size:14px;line-height:1.55;color:rgba(45,48,81,.7);}

/* ── итог ──────────────────────────────────────────────────────────────── */
.sb-sec-out{padding:clamp(64px,8vw,110px) 0 clamp(72px,9vw,120px);background:var(--ink);color:#fff;}
.sb-sec-out .sb-kicker{color:var(--peach);}
.sb-outs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px;}
.sb-out-c{border-top:1px solid rgba(255,255,255,.24);padding-top:18px;}
.sb-out-c h3{font-size:16px;font-weight:700;margin-bottom:10px;}
.sb-out-c p{font-size:14px;line-height:1.6;color:rgba(255,255,255,.72);}
.sb-museum{margin-top:48px;}
.sb-museum img{border-radius:20px;width:100%;}
.sb-museum figcaption{margin-top:12px;font-size:13px;color:rgba(255,255,255,.6);}

/* ── адаптив ───────────────────────────────────────────────────────────── */
@media (max-width:1080px){
 .sb-mts{grid-template-columns:repeat(6,minmax(0,1fr));}
 .sb-cols{grid-template-columns:repeat(3,minmax(0,1fr));}
 .sb-ws{grid-template-columns:repeat(3,minmax(0,1fr));}
 .sb-lblocks{grid-template-columns:repeat(3,minmax(0,1fr));}
 .sb-mds{grid-template-columns:repeat(2,minmax(0,1fr));}
 .sb-brules{grid-template-columns:repeat(2,minmax(0,1fr));}
 .sb-outs{grid-template-columns:repeat(2,minmax(0,1fr));}
 .sb-navb{grid-template-columns:1fr;}
 .sb-icons{grid-template-columns:1fr;gap:32px;}
 .sb-task-grid{grid-template-columns:1fr;}
 .sb-task-two{grid-template-columns:1fr;gap:32px;}
 .sb-safe-row{grid-template-columns:1fr;gap:18px;}
 .sb-roles{grid-template-columns:1fr;gap:24px;}
}
@media (max-width:860px){
 .sb-hero-in{grid-template-columns:1fr;}
 .sb-hero-fig{order:-1;justify-content:flex-start;}
 .sb .sb-hero-mascot{height:clamp(240px,52vw,340px);}
 .sb-hero-mark{left:auto;right:6%;bottom:auto;top:0;width:64px;}
 .sb-facts{grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;}
 .sb-mstage{grid-template-columns:1fr;gap:20px;}
 .sb-mstage-fig{min-height:clamp(258px,68vw,340px);}
 .sb .sb-mbig,.sb .sb-ghost{height:clamp(248px,66vw,330px);}
 .sb-mark-grid{grid-template-columns:1fr;}
 .sb-pat{grid-template-columns:1fr;}
 .sb-pat-box{height:clamp(180px,44vw,240px);}
 .sb-walls{grid-template-columns:1fr;}
 .sb-lvs{grid-template-columns:1fr;}
}
@media (max-width:640px){
 .sb-wrap{padding:0 18px;}
 .sb-mts{grid-template-columns:repeat(4,minmax(0,1fr));}
 .sb-mt img{height:58px;}
 .sb-mt span{font-size:9px;letter-spacing:0;}
 .sb-cols{grid-template-columns:repeat(2,minmax(0,1fr));}
 .sb-ws{grid-template-columns:repeat(2,minmax(0,1fr));}
 .sb-lblocks{grid-template-columns:repeat(2,minmax(0,1fr));}
 .sb-mds{grid-template-columns:1fr;}
 .sb-brules{grid-template-columns:1fr;}
 .sb-outs{grid-template-columns:1fr;}
 .sb-ics{grid-template-columns:repeat(3,minmax(0,1fr));}
 .sb-stage{flex-direction:column;min-height:0;}
 .sb-stage-m{flex:none;width:100%;height:clamp(150px,42vw,210px);align-items:flex-end;}
 .sb-stage-m img{max-height:100%;}
 .sb-stage-w{flex:none;width:100%;height:clamp(300px,78vw,380px);margin-top:10px;}
 .sb-chip{font-size:11px;padding:5px 9px;}
 .sb-chip-big{font-size:26px;padding:8px 16px;}
 .sb-stage-note{position:static;margin-top:10px;text-align:right;}
 .sb-b-head{flex-direction:column;align-items:stretch;}
 .sb-b-head .sb-btn{width:100%;}
 .sb-nav-stage{padding:34px 14px;justify-content:flex-start;}
 .sb-mes i{display:none;}
 .sb-md-i img{max-height:180px;}
}
@media (max-height:520px) and (orientation:landscape){
 .sb-hero{padding-top:84px;}
 .sb .sb-hero-mascot{height:min(60vh,320px);}
 .sb .sb-mbig,.sb .sb-ghost{height:min(58vh,300px);}
}
@media (prefers-reduced-motion:reduce){
 .sb-r,.sb-chip,.sb-pat-line{transition:none!important;}
 .sb-r{opacity:1;transform:none;}
}
</style>"""


PAGE_JS = """<script>(function(){
 var ZONES=%ZONES%, MASC=%MASC%, IMG='%IMG%';
 function $(s,r){return (r||document).querySelector(s);}
 function $$(s,r){return [].slice.call((r||document).querySelectorAll(s));}

 // ── логотип: поля 1X/1,25X/3X ─────────────────────────────────────────
 var safeBtn=$('[data-safe-toggle]');
 if(safeBtn){safeBtn.addEventListener('click',function(){
  var on=safeBtn.getAttribute('aria-pressed')!=='true';
  safeBtn.setAttribute('aria-pressed',on?'true':'false');
  safeBtn.textContent=on?'Скрыть поля':'Показать поля';
  $$('.sb-logo').forEach(function(l){l.classList.toggle('is-safe',on);});
 });}

 // ── палитра: клик копирует hex ────────────────────────────────────────
 $$('.sb-col').forEach(function(b){
  b.addEventListener('click',function(){
   var hex=b.getAttribute('data-hex');
   var done=function(){b.classList.add('is-copied');
    setTimeout(function(){b.classList.remove('is-copied');},1300);};
   if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(hex).then(done,done);
   }else{
    var t=document.createElement('textarea');t.value=hex;document.body.appendChild(t);
    t.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(t);done();
   }
  });
 });

 // ── маскот: гардероб и сравнение силуэтов ─────────────────────────────
 var big=$('.sb-mbig'), ghost=$('.sb-ghost'), zone=$('.sb-mzone'), desc=$('.sb-mdesc'),
     cur='hero';
 function setFig(el,k){
  var m=MASC[k];
  el.src=IMG+'/'+k+'.png'; el.width=m.w; el.height=m.h;
  el.style.setProperty('--ax',m.ax);
 }
 function ghostFor(k){
  // сравниваем с базовым образом, а для самого базового — с деловым
  return k==='hero'?'business':'hero';
 }
 $$('.sb-mt').forEach(function(b){
  b.addEventListener('click',function(){
   var k=b.getAttribute('data-m'), m=MASC[k];
   if(!m||!big) return;
   $$('.sb-mt').forEach(function(o){o.setAttribute('aria-pressed',o===b?'true':'false');});
   cur=k; setFig(big,k);
   big.alt='Маскот «Ладушка»: '+m.t.toLowerCase();
   zone.textContent=m.t; desc.textContent=m.d;
   if(ghost&&!ghost.hidden) setFig(ghost,ghostFor(k));
  });
 });
 var stackBtn=$('[data-stack]');
 if(stackBtn&&ghost){stackBtn.addEventListener('click',function(){
  var on=stackBtn.getAttribute('aria-pressed')!=='true';
  stackBtn.setAttribute('aria-pressed',on?'true':'false');
  stackBtn.textContent=on?'Убрать силуэт':'Сравнить силуэты';
  if(on) setFig(ghost,ghostFor(cur));
  ghost.hidden=!on;
 });}

 // ── стена зоны: раскладка слов без пересечений ────────────────────────
 var stage=$('[data-stage]'), sm=$('.sb-stage-m'), sw=$('.sb-stage-w'),
     snote=$('.sb-stage-note'), cur=ZONES[0], seed=1;
 function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff;}
 function place(){
  if(!stage||!sw) return;
  sw.innerHTML='';
  var W=sw.clientWidth, H=sw.clientHeight;
  if(!W||!H) return;
  var mob=W<420, words=cur.w.slice(0,mob?6:cur.w.length), boxes=[];
  // центральное слово зоны: крупный чип, ставим правее середины
  var mid=document.createElement('span');
  mid.className='sb-chip sb-chip-big sb-c0';
  mid.textContent=cur.c; sw.appendChild(mid);
  var mw=mid.offsetWidth, mh=mid.offsetHeight;
  var mx=Math.max(0,Math.min(W-mw,W*(mob?.5:.56)-mw/2)), my=H*.42-mh/2;
  mid.style.left=mx+'px'; mid.style.top=my+'px';
  boxes.push({x:mx-10,y:my-10,w:mw+20,h:mh+20});
  // поле делим на секторы 3×3 и каждое слово кидаем в самый свободный:
  // чистый рандом сбивает чипы в кучу и оставляет пустые углы
  var cols=3, rows=3, used=[];
  for(var s=0;s<cols*rows;s++) used.push(0);
  function sector(x,y,w,h){
   var cx=Math.min(cols-1,Math.max(0,Math.floor((x+w/2)/(W/cols))));
   var cy=Math.min(rows-1,Math.max(0,Math.floor((y+h/2)/(H/rows))));
   return cy*cols+cx;
  }
  used[sector(mx,my,mw,mh)]+=2;
  words.forEach(function(t,i){
   var el=document.createElement('span');
   el.className='sb-chip sb-c'+((i+1)%3);
   el.textContent=t; sw.appendChild(el);
   var w=el.offsetWidth, h=el.offsetHeight, put=null;
   var free=used.indexOf(Math.min.apply(null,used));
   var fx=(free%cols)*(W/cols), fy=Math.floor(free/cols)*(H/rows);
   for(var pad=14;pad>=2&&!put;pad-=6){
    for(var k=0;k<260;k++){
     // первые попытки — внутри самого свободного сектора, дальше по всему полю
     var inSec=k<120;
     var x=inSec?fx+rnd()*Math.max(1,W/cols-w):rnd()*Math.max(1,W-w);
     var y=inSec?fy+rnd()*Math.max(1,H/rows-h):rnd()*Math.max(1,H-h);
     x=Math.min(x,Math.max(0,W-w)); y=Math.min(y,Math.max(0,H-h));
     var ok=true;
     for(var j=0;j<boxes.length;j++){
      var b=boxes[j];
      if(x<b.x+b.w+pad&&x+w+pad>b.x&&y<b.y+b.h+pad&&y+h+pad>b.y){ok=false;break;}
     }
     if(ok){put={x:x,y:y};break;}
    }
   }
   if(!put){el.remove();return;}
   el.style.left=put.x+'px'; el.style.top=put.y+'px';
   boxes.push({x:put.x,y:put.y,w:w,h:h});
   used[sector(put.x,put.y,w,h)]+=1;
   setTimeout(function(){el.classList.add('is-on');},60+i*45);
  });
  setTimeout(function(){mid.classList.add('is-on');},40);
 }
 function paint(z,keepSeed){
  cur=z;
  if(!keepSeed) seed=(z.k.charCodeAt(0)*7919+z.w.length*13)|1;
  stage.style.background=z.bg; stage.style.color=z.fg;
  var m=MASC[z.m];
  sm.innerHTML='<img src="'+IMG+'/'+z.m+'.png" alt="Маскот «Ладушка» в оформлении '+
   z.n.toLowerCase()+'" width="'+m.w+'" height="'+m.h+'" loading="lazy" decoding="async">';
  snote.textContent=z.src==='гайд'?'разобрано в гайде':'собрано по правилу гайда';
  place();
 }
 if(stage){
  $$('.sb-zt').forEach(function(b){
   b.addEventListener('click',function(){
    var z=ZONES.filter(function(x){return x.k===b.getAttribute('data-z');})[0];
    if(!z) return;
    $$('.sb-zt').forEach(function(o){o.setAttribute('aria-pressed',o===b?'true':'false');});
    paint(z);
   });
  });
  var rb=$('[data-reshuffle]');
  if(rb) rb.addEventListener('click',function(){seed=(Date.now()&0x7fffffff)|1;place();});
  var rt;
  addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(place,220);});
  paint(ZONES[0]);
 }

 // ── паттерн: кривая рисуется по скроллу ───────────────────────────────
 var patLine=$('.sb-pat-line');
 if(patLine){
  try{var len=Math.ceil(patLine.getTotalLength?patLine.getTotalLength():0);}catch(e){len=0;}
  if(!len){var p=patLine.querySelector('path'); if(p&&p.getTotalLength) len=Math.ceil(p.getTotalLength());}
  if(len) patLine.style.setProperty('--len',len);
 }

 // ── бенто: смена формата ──────────────────────────────────────────────
 var bgrid=$('[data-bento]');
 $$('.sb-ft').forEach(function(b){
  b.addEventListener('click',function(){
   $$('.sb-ft').forEach(function(o){o.setAttribute('aria-pressed',o===b?'true':'false');});
   if(bgrid) bgrid.setAttribute('data-f',b.getAttribute('data-f'));
  });
 });

 // ── навигационная табличка ────────────────────────────────────────────
 var sign=$('[data-sign]'), stx=$('[data-sign-tx]'), sic=$('[data-sign-ic]'),
     sar=$('[data-sign-ar]'), xv=$('[data-xv]');
 function setPressed(list,b){list.forEach(function(o){o.setAttribute('aria-pressed',o===b?'true':'false');});}
 if(sign){
  var wbs=$$('.sb-nw');
  wbs.forEach(function(b){
   b.addEventListener('click',function(){
    setPressed(wbs,b); stx.textContent=b.getAttribute('data-w');
    var inp=$('[data-sign-input]'); if(inp) inp.value='';
   });
  });
  var ibs=$$('[data-i]');
  ibs.forEach(function(b){
   b.addEventListener('click',function(){
    setPressed(ibs,b);
    sic.innerHTML=b.innerHTML;
    var cb=$('[data-sign-noic]'); if(cb&&cb.checked){cb.checked=false;sign.classList.remove('is-noic');}
   });
  });
  var abs=$$('[data-a]');
  abs.forEach(function(b){
   b.addEventListener('click',function(){setPressed(abs,b);sar.innerHTML=b.innerHTML;});
  });
  var inp=$('[data-sign-input]');
  if(inp) inp.addEventListener('input',function(){
   var v=inp.value.toUpperCase().replace(/\\s+/g,' ').trim();
   stx.textContent=v||'КАФЕ';
   if(v) setPressed(wbs,null);
  });
  var noic=$('[data-sign-noic]');
  if(noic) noic.addEventListener('change',function(){sign.classList.toggle('is-noic',noic.checked);});
  var grid=$('[data-sign-grid]');
  if(grid){sign.classList.toggle('is-grid',grid.checked);
   grid.addEventListener('change',function(){sign.classList.toggle('is-grid',grid.checked);});}
  var rx=$('[data-sign-x]');
  if(rx){
   rx.addEventListener('input',function(){
    sign.style.setProperty('--x',rx.value+'px'); if(xv) xv.textContent=rx.value;
   });
   // на узком экране табличка в 48 px уезжает в скролл — стартуем с меньшего модуля
   if(innerWidth<640){rx.value=28;rx.dispatchEvent(new Event('input'));}
  }
 }

 // ── появление блоков ──────────────────────────────────────────────────
 var els=$$('.sb-r');
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
<title>Фирменный стиль выставки «Самара» — брендбук Самарской области | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: руководство по использованию фирменного стиля выставки «Самара» в Музее им. П. В. Алабина. 28 полос: логотип и охранные поля, палитра, Manrope, маскот «Ладушка» в 16 образах, семантическое ядро из 46 слов, бенто-макеты, навигация по модулю X, носители.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Фирменный стиль выставки «Самара» — брендбук Самарской области">
<meta property="og:description" content="Брендбук как рабочая система: соберите стену зоны из слов ядра, переоденьте маскота и нарежьте навигационную табличку по модулю X прямо на странице.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/banner-welcome.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-samara.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Фирменный стиль выставки «Самара»",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    zones = [{'k': k, 'n': n, 'm': m, 'bg': bg, 'fg': fg, 'c': c, 'w': w, 'src': src}
             for k, n, m, bg, fg, c, w, src in ZONES]
    masc = {k: {'t': t, 'd': d, 'w': SIZE[k][0], 'h': SIZE[k][1], 'ax': ANCHOR[k]}
            for k, t, d in MASCOTS}
    js = (PAGE_JS.replace('%ZONES%', json.dumps(zones, ensure_ascii=False))
                 .replace('%MASC%', json.dumps(masc, ensure_ascii=False))
                 .replace('%IMG%', IMG))
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="sb">{sprite()}{hero()}{task()}{mark()}{palette()}'
            f'{typo()}{mascot()}{core()}{pattern()}{bento()}{nav()}{media()}'
            f'{live()}{out()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'creative', 'samara')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
