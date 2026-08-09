#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/event/marieclaire/index.html: кейс «Кросс-мероприятия
Marie Claire» — серия активностей журнала в торговых центрах Москвы
(ГУМ, Европейский, Атриум, Метрополис), 2011-2013, и финальный вечер.

Что было раньше: запечённая Tilda-страница на три абзаца «Задачи → Решение →
Результат». Ни одной фотографии, хотя в общем каталоге лежит 25 кадров съёмки
проекта. Видео висело в мёртвом t868-попапе и вело на /media/event-marieclaire.mp4,
которого на сервере нет (рабочий адрес — /media/marie-claire-event.mp4,
см. scripts/a2/video_map.json).

Идея страницы. Кейс не про одно мероприятие, а про тиражируемый формат: один
и тот же набор модулей застройки пересобирался под каждого партнёра и каждый
ТЦ. Отсюда две механики:

1. «Разбор застройки» (сигнатурная). Шесть реальных сборок — базовый корпус
   marie claire, «Приз великолепия», Fan di FENDI, Clarins, Estée Lauder, Dior.
   Поверх каждой ФОТОГРАФИИ размечены модули: стена с графикой, витрина,
   стойка, посадка, фигурный элемент, оборудование, подиум. Наводишь на модуль
   в наборе — он подсвечивается на снимке; переключаешь партнёра — видно, что
   набор тот же, а «одёжка» другая. Разметка снята с самих кадров, ничего не
   дорисовано и не смоделировано.
2. Лента финального вечера в «Метрополисе»: 13 кадров из ролика в хронологии
   смены, от дневной стойки регистрации до ночного шоу, листается по горизонтали.

Спина страницы — пятёрка глаголов с торцов самой застройки: «информирует /
вдохновляет / развлекает / соблазняет / бросает вызов». Это не копирайт
страницы, а надпись на стенах корпуса, её видно на кадрах stand-arch и
stand-makeup; на пресс-волле финального вечера та же формула с «удивляет».

Честность цифр: ТЦ, состав работ и результат — из текста кейса. Условия акций
(3000 ₽ в Oxette в ночь со 2 на 3 ноября 20:00-3:00; 5000 ₽ с 30 марта по
1 апреля) прочитаны с табличек на кадрах promo-team и в ролике. Годы премии —
с самих застроек (2011, 2012, 2013). Бренды-партнёры — по вывескам и POSm
в кадре. Ничего сверх этого не придумано.

Шрифты Playfair Display + Jost, локальные (/fonts/playfair-jost.css),
кадры и фото готовит scripts/marieclaire-assets.py.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/marieclaire'
VIDEO = '/media/marie-claire-event.mp4'
URL = 'https://hand-marketing.ru/event/marieclaire/'

# размеры готовых файлов — проставляем в width/height, чтобы вёрстка
# не прыгала, пока грузится картинка
SIZE = {
    'clarins-sail': (1102, 787), 'corner-mall': (1600, 1200), 'dior-corner': (1600, 1200),
    'expo-girls': (1600, 1066), 'expo-intercharm': (1600, 1066), 'expo-model': (1600, 2400),
    'expo-promo': (1600, 1200), 'expo-sport': (1600, 1200), 'expo-stand': (1600, 1200),
    'expo-table': (1600, 1066), 'expo-tennis': (1600, 1200), 'fendi-bar': (1600, 1066),
    'fendi-desk': (1600, 2400), 'fendi-stand': (1600, 1066), 'fendi-wall': (1600, 1066),
    'gift-bags': (1600, 1200), 'prix-2011': (1600, 1446), 'prix-2012': (1600, 1200),
    'prix-2013': (1600, 1200), 'promo-team': (800, 600), 'stand-arch': (800, 600),
    'stand-makeup': (800, 600), 'stand-shoot': (800, 600), 'viz-clarins': (1024, 768),
    'viz-esteelauder': (1771, 1771),
}
for _n in ('award', 'band', 'crowd', 'desk', 'gift', 'hair', 'looks', 'makeup',
           'nails', 'photo', 'podium', 'poster', 'show', 'tag'):
    SIZE['night-' + _n] = (1280, 720)


def pic(name, alt, cls='', lazy=True, sizes=''):
    w, h = SIZE[name]
    return ('<img src="%s/%s.jpg" alt="%s" width="%d" height="%d"%s%s%s>'
            % (IMG, name, alt, w, h,
               ' class="%s"' % cls if cls else '',
               ' loading="lazy" decoding="async"' if lazy else '',
               ' sizes="%s"' % sizes if sizes else ''))


# ─── паспорт проекта ────────────────────────────────────────────────────────
FACTS = [
    ('Клиент', 'Журнал Marie Claire'),
    ('Площадки', 'ГУМ, Европейский, Атриум, Метрополис'),
    ('Годы', '2011 — 2013'),
    ('Формат', 'Застройка галерей, семплинг, кросс-промо'),
    ('Финал', 'Вечер в «Метрополисе» до 3 ночи'),
]

# ─── пятёрка глаголов с торцов застройки ────────────────────────────────────
# (глагол, фото, alt, что за этим стояло на площадке)
VERBS = [
    ('Информирует', 'promo-team',
     'Промо-группа Marie Claire у стойки в галерее торгового центра с условиями акции',
     'Промо-группа в фирменных платках раздавала свежий номер и объясняла условия: '
     'что купить, где предъявить чек, какой подарок за это будет. Журнал в руки — '
     'первое касание, всё остальное строилось на нём.'),
    ('Вдохновляет', 'night-looks',
     'Образы сезона на манекенах за красной лентой в галерее торгового центра',
     'Образы сезона стояли не на страницах, а в галерее: манекены с полными '
     'комплектами из магазинов этого же центра. Читательница видела вещь и через '
     'сто метров могла её примерить.'),
    ('Развлекает', 'night-podium',
     'Подиум с зеркальным шаром и шоу-программой на финальном вечере',
     'Подиум, шоу-программа, живое выступление группы. Торговый центр на вечер '
     'переставал быть местом, куда заходят за покупкой, и становился местом, '
     'куда идут специально.'),
    ('Соблазняет', 'stand-makeup',
     'Make-up бар со свето-зеркалом на стенде Marie Claire в торговом центре',
     'Make-up бар с гримёрным зеркалом, консультации визажистов ведущих марок, '
     'стайлинг и маникюр. Не выкладка, а услуга: посетительница уходила с готовым '
     'образом, а бренд — с демонстрацией продукта на живом лице.'),
    ('Бросает вызов', 'stand-shoot',
     'Съёмка посетительницы на фотозоне стенда Marie Claire',
     'Фотозона со съёмкой: сесть в кресло, попасть в кадр рядом с логотипом '
     'журнала. Самая рабочая механика вовлечения — снимок гостья уносила с собой '
     'и показывала сама.'),
]

# ─── разбор застройки: шесть сборок одного набора модулей ───────────────────
# hotspot = (модуль-набор, подпись, x%, y%, w%, h%) — рамки сняты с самих кадров
KIT = [
    ('wall', 'Стена с графикой'),
    ('shape', 'Фигурный элемент'),
    ('case', 'Витрина'),
    ('desk', 'Стойка и стол'),
    ('seat', 'Посадка'),
    ('gear', 'Оборудование'),
    ('goods', 'Образы и продукт'),
    ('floor', 'Подиум и настил'),
]

BUILDS = [
    ('base', 'marie claire', 'Европейский · Атриум · ГУМ', 'stand-arch',
     'Базовый корпус: три стены с графикой, фигурный торец, красный подиум',
     'Опорная сборка серии. Три стеновых панели с фирменной пятёркой глаголов, '
     'скруглённый торец с «Призом великолепия», красный подиум, который отделяет '
     'площадку от общего пола галереи. Внутри — стойка, манекены и make-up консоль.',
     [('wall', 'Стена: информирует', 27, 20, 17, 27),
      ('wall', 'Стена: логотип', 44, 20, 16, 27),
      ('wall', 'Стена: соблазняет', 60, 19, 14, 31),
      ('shape', 'Скруглённый торец', 74, 15, 16, 57),
      ('goods', 'Манекены с образами', 29, 26, 16, 27),
      ('desk', 'Стойка-ресепшн', 7, 40, 20, 33),
      ('gear', 'Make-up консоль', 46, 39, 18, 46),
      ('floor', 'Красный подиум', 10, 56, 70, 37)]),

    ('prix', 'Приз великолепия', 'Премия Prix d’Excellence de la Beauté', 'prix-2011',
     'Та же логика в золоте: фриз, стена премии и две подсвеченные витрины',
     'Под премию корпус пересобран целиком: сплошной фриз с названием, тёмная '
     'стена с логотипом и годом, две стеклянные витрины-колонны с лауреатами. '
     'Посадка осталась — на стульях по краям работали косметологи и визажисты.',
     [('wall', 'Фриз премии', 2, 10, 94, 14),
      ('wall', 'Стена премии', 2, 24, 94, 49),
      ('case', 'Витрина лауреатов', 23, 38, 15, 48),
      ('case', 'Витрина лауреатов', 59, 38, 16, 48),
      ('seat', 'Барный стул', 9, 48, 13, 35),
      ('seat', 'Барный стул', 74, 48, 16, 32),
      ('floor', 'Подиум площадки', 0, 73, 100, 23)]),

    ('fendi', 'Fan di FENDI', 'Аромат-бар и пресс-волл', 'fendi-stand',
     'Чёрно-жёлтая сборка: пресс-волл, пилоны, аромат-бар',
     'Запуск аромата: вместо витрин — пресс-волл во всю заднюю стену, вместо '
     'стульев — кресла, вместо ресепшна — жёлтый аромат-бар. Пилоны по краям '
     'держат площадку в общем потоке галереи и работают как выкладка.',
     [('wall', 'Пресс-волл', 36, 5, 32, 53),
      ('goods', 'Постер и выкладка', 39, 13, 27, 32),
      ('shape', 'Пилон', 24, 8, 10, 84),
      ('shape', 'Пилон', 66, 12, 11, 78),
      ('shape', 'Пилон', 77, 20, 12, 52),
      ('desk', 'Аромат-бар', 17, 47, 17, 45),
      ('seat', 'Кресло', 36, 47, 14, 28),
      ('seat', 'Кресло', 58, 47, 17, 26),
      ('floor', 'Чёрный подиум', 10, 58, 82, 40)]),

    ('clarins', 'Clarins', 'Корнер в галерее · визуализация', 'viz-clarins',
     'Корнер на четыре модуля: парус, стенка, стол и посадка',
     'Проект корнера до постройки. Тот же набор ужат до размера торгового '
     'островка: фигурная панель-парус вместо стены, стенка с продуктом, стол '
     'и один барный стул. Панель двусторонняя, у неё две разные лицевые стороны.',
     [('shape', 'Панель-парус', 47, 5, 26, 58),
      ('goods', 'Стенка с продуктом', 25, 36, 15, 45),
      ('desk', 'Стол', 33, 38, 14, 25),
      ('seat', 'Барный стул', 40, 38, 15, 26),
      ('case', 'Колонна-витрина', 41, 25, 9, 25),
      ('floor', 'Настил корнера', 16, 55, 63, 33)]),

    ('esteelauder', 'Estée Lauder', 'Визажный корнер · визуализация', 'viz-esteelauder',
     'Визажный корнер: кофр, свет и две посадки',
     'Здесь набор собран вокруг услуги. Постер держит бренд, стойка и два стула — '
     'рабочие места визажиста и гостьи, визажный кофр и софтбокс превращают угол '
     'галереи в подобие съёмочной площадки.',
     [('wall', 'Постер бренда', 21, 15, 25, 25),
      ('desk', 'Стойка-стол', 27, 40, 30, 30),
      ('seat', 'Стул', 19, 40, 14, 29),
      ('seat', 'Стул', 34, 49, 20, 37),
      ('gear', 'Визажный кофр', 56, 26, 26, 40),
      ('gear', 'Софтбокс', 55, 7, 28, 25),
      ('floor', 'Настил корнера', 17, 40, 70, 48)]),

    ('dior', 'Dior', 'Корнер в галерее', 'dior-corner',
     'Чёрный лак: пилоны, стойка и экран',
     'Финальная степень сжатия: два пилона, стойка, экран и две посадки на '
     'чёрном настиле. Ни одной несущей стены — площадка держится на пилонах, '
     'зато читается через всю галерею.',
     [('shape', 'Пилон Dior', 26, 12, 14, 68),
      ('shape', 'Пилон Dior', 58, 17, 14, 57),
      ('desk', 'Стойка', 33, 32, 27, 28),
      ('gear', 'Экран', 40, 20, 18, 12),
      ('seat', 'Барный стул', 34, 44, 14, 31),
      ('seat', 'Барный стул', 48, 47, 14, 33),
      ('case', 'Тумба-витрина', 15, 48, 18, 36),
      ('floor', 'Чёрный настил', 10, 52, 75, 36)]),
]

# ─── «Приз великолепия»: три года подряд ────────────────────────────────────
PRIX = [
    ('2011', 'prix-2011',
     'Застройка премии «Приз великолепия» Marie Claire 2011 года: золотой фриз и витрины лауреатов',
     'Золотой фриз «За достижения в индустрии красоты», две подсвеченные витрины '
     'с лауреатами, консультации косметологов и make-up ведущих марок по краям.'),
    ('2012', 'prix-2012',
     'Площадка премии «Приз великолепия» 2012 года с роллапами Garnier и Vichy в галерее торгового центра',
     'Год спустя премия ушла в галерею к партнёрам: стела «Приз великолепия» '
     'работает рядом с выкладкой Garnier и Vichy, посадка одна, а не две.'),
    ('2013', 'prix-2013',
     'Витрина премии «Приз великолепия» 2013 года с обложкой Marie Claire в торговом центре',
     'В 2013-м фасад держит уже сама обложка номера, вынесенная на всю стену, '
     'а лауреаты стоят в ряду подсвеченных витрин по всей длине площадки.'),
]

# ─── механика подарка за покупку: реальные условия с табличек ───────────────
GIFT = [
    ('3000 ₽', 'Oxette', 'Со 2 на 3 ноября, 20:00 — 3:00',
     'Ночная механика: чек от трёх тысяч в магазинах-участниках обменивался '
     'на подарок от журнала. Работала всю ночь распродаж, до трёх часов.'),
    ('5000 ₽', 'Партнёры акции', 'С 30 марта по 1 апреля',
     'Весенняя волна с более высоким порогом и коротким окном в три дня: '
     'промо-группа держала стойку в галерее весь период.'),
    ('Бирка', 'Витрины магазинов', '«marie claire рекомендует»',
     'Красные бирки в витринах участников: журнал приходил не только на свою '
     'площадку, но и внутрь чужого зала, к конкретной вещи на полке.'),
]

# ─── лента финального вечера в «Метрополисе» ────────────────────────────────
NIGHT = [
    ('night-desk', 'Стойка регистрации',
     'Стойка регистрации гостей вечера Marie Claire в галерее ТЦ Метрополис',
     'Стойка открывается засветло: регистрация, анкеты, условия розыгрыша.'),
    ('night-tag', 'Бирка в витрине',
     'Красная бирка «marie claire рекомендует» на украшениях в витрине магазина',
     'В залах магазинов-участников — бирки «marie claire рекомендует».'),
    ('night-looks', 'Образы сезона',
     'Манекены с образами сезона за красной лентой в галерее торгового центра',
     'Образы собраны из вещей магазинов этого же центра.'),
    ('night-hair', 'Стайлинг',
     'Зона стайлинга волос Cloud Nine на вечере Marie Claire',
     'Зона стайлинга: укладка за то время, пока идёт программа.'),
    ('night-nails', 'Nail-бар',
     'Мастер делает маникюр гостье на nail-баре вечера Marie Claire',
     'Nail-бар работает без записи, в порядке живой очереди.'),
    ('night-makeup', 'Make-up бар',
     'Визажист работает с гостьей на make-up баре вечера Marie Claire',
     'Визажисты марок-партнёров: макияж как демонстрация продукта.'),
    ('night-photo', 'Фотозона',
     'Гостьи вечера позируют у пресс-волла Marie Claire',
     'Пресс-волл: кадр, который гостья уносит и показывает сама.'),
    ('night-show', 'Показ мод',
     'Ведущая показа мод разбирает образы на сцене вечера Marie Claire',
     'Показ мод с разбором: почему этот образ работает, а этот нет.'),
    ('night-podium', 'Шоу-программа',
     'Танцевальный номер на подиуме с зеркальным шаром на вечере в ТЦ Метрополис',
     'Подиум, зеркальный шар и светодиодный экран во всю стену.'),
    ('night-band', 'Живое выступление',
     'Выступление музыкальной группы на сцене вечера Marie Claire в ТЦ Метрополис',
     'Живое выступление группы — финал шоу-программы.'),
    ('night-crowd', 'Зрители',
     'Зрители на всех ярусах галереи торгового центра смотрят программу вечера',
     'Смотрят с трёх ярусов галереи: сцена видна отовсюду.'),
    ('night-award', 'Награждение',
     'Ведущий вечера берёт интервью у гостьи перед награждением',
     'Розыгрыш и награждение: ведущий работает с залом напрямую.'),
    ('night-gift', 'Подарок',
     'Гостья с подарком от журнала Marie Claire у пресс-волла',
     'Подарок от журнала за покупку — то, ради чего механика затевалась.'),
]

# ─── выставки, турниры и площадки вне ТЦ ────────────────────────────────────
EXPO = [
    ('expo-intercharm', 'Витрина с номерами и разворотами на выставочном стенде Marie Claire',
     'Выставка индустрии красоты'),
    ('expo-stand', 'Стенд Marie Claire с манекеном и стойками с номерами журнала',
     'Стенд с образами и выкладкой'),
    ('expo-girls', 'Промо-группа Marie Claire на выставочном стенде',
     'Промо-группа на стенде'),
    ('expo-tennis', 'Теннисисты с фирменными пакетами Marie Claire на турнире',
     'Турнир: подарки участникам'),
    ('expo-model', 'Девушка в образе у баннера Marie Claire на выставке',
     'Образы у баннера'),
    ('expo-sport', 'Стенд Marie Claire с роллапами и стойкой в спортивном комплексе',
     'Мобильная сборка на роллапах'),
    ('expo-table', 'Стол с номерами журнала Marie Claire и цветами в зоне переговоров',
     'Зона переговоров'),
    ('expo-promo', 'Две девушки промо-группы у стойки Marie Claire на выставке',
     'Работа с потоком'),
]

PAGE_CSS = """<style id="mc-css">
:root{
 --mc-paper:#F6F2ED; --mc-paper2:#EDE6DE; --mc-ink:#15110F; --mc-ink2:#241D1A;
 --mc-red:#D2042D; --mc-red-d:#9C0322; --mc-gold:#A87C2A; --mc-gold-l:#D9B978;
 --mc-night:#2A1240; --mc-violet:#8347B0;
 --mc-dim:#6E635C; --mc-line:rgba(21,17,15,.15);
}
.mc{font-family:'Jost',-apple-system,Arial,sans-serif;color:var(--mc-ink);
 background:var(--mc-paper);-webkit-font-smoothing:antialiased;overflow-x:clip}
.mc *{box-sizing:border-box}
.mc img{max-width:100%;height:auto;display:block}
.mc p{margin:0}
.mc h1,.mc h2,.mc h3{margin:0;font-family:'Playfair Display',Georgia,serif;
 font-weight:700;line-height:1.02;letter-spacing:-.015em}
.mc__wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.mc__eyebrow{font-size:12px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;
 color:var(--mc-red)}
.mc__lead{font-size:clamp(16px,1.5vw,19px);line-height:1.62;color:var(--mc-dim)}
.mc__note{margin-top:clamp(20px,2.4vw,32px);font-size:12.5px;line-height:1.55;color:#8B807A}
.mc-sec{padding:clamp(56px,7vw,112px) 0;position:relative}
.mc-sec__h{font-size:clamp(30px,4.2vw,58px);max-width:19ch}
.mc-sec__sub{margin-top:clamp(20px,2.2vw,30px);max-width:62ch;font-size:clamp(15px,1.3vw,17.5px);
 line-height:1.68;color:var(--mc-dim)}
.mc-r{opacity:0;transform:translateY(20px);transition:opacity .8s ease,transform .8s ease}
.mc-r.in{opacity:1;transform:none}
.mc-rule{height:2px;background:var(--mc-red);width:64px;margin:0 0 22px}
.mc-cap{margin-top:12px;font-size:12.5px;line-height:1.5;color:#8B807A}
.mc-fig{margin:0}
.mc-fig img{width:100%}

/* ── ГЕРОЙ ── */
.mc-hero{position:relative;background:var(--mc-ink);color:#fff;overflow:hidden}
.mc-hero__bg{position:absolute;inset:0}
.mc-hero__bg img{width:100%;height:100%;object-fit:cover;opacity:.42;
 filter:grayscale(.25) contrast(1.05)}
.mc-hero__bg:after{content:'';position:absolute;inset:0;
 background:linear-gradient(180deg,rgba(21,17,15,.72),rgba(21,17,15,.55) 45%,rgba(21,17,15,.94))}
.mc-hero__in{position:relative;padding:clamp(28px,4vw,54px) 0 clamp(44px,5vw,80px)}
.mc-back{display:inline-flex;align-items:center;gap:9px;font-size:13px;font-weight:500;
 letter-spacing:.04em;color:rgba(255,255,255,.66);text-decoration:none;transition:color .2s}
.mc-back:hover{color:#fff}
.mc-hero h1{margin-top:clamp(30px,5vw,72px);font-size:clamp(38px,7.2vw,104px);
 line-height:.94;letter-spacing:-.025em;max-width:15ch;color:#fff}
.mc-hero h1 em{font-style:italic;color:var(--mc-red)}
.mc-hero__lead{margin-top:clamp(26px,2.6vw,36px);max-width:56ch;font-size:clamp(16px,1.6vw,20px);
 line-height:1.6;color:rgba(255,255,255,.8)}
.mc-hero__facts{margin-top:clamp(34px,5vw,64px);display:grid;
 grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1px;background:rgba(255,255,255,.16)}
.mc-hero__f{background:var(--mc-ink);padding:18px 16px}
.mc-hero__f dt{font-size:10.5px;font-weight:600;letter-spacing:.19em;text-transform:uppercase;
 color:rgba(255,255,255,.5)}
.mc-hero__f dd{margin:7px 0 0;font-size:15px;line-height:1.34;font-weight:500;color:#fff}

/* ── ЗАДАЧА ── */
.mc-task{background:var(--mc-paper)}
.mc-task__grid{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(30px,5vw,72px);
 align-items:start}
.mc-task__body p+p{margin-top:17px}
.mc-task__body p{font-size:clamp(15.5px,1.35vw,18px);line-height:1.68}
.mc-task__side{border-top:2px solid var(--mc-ink);padding-top:22px}
.mc-task__side dl{margin:0;display:grid;gap:16px}
.mc-task__side dt{font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;
 color:var(--mc-red)}
.mc-task__side dd{margin:5px 0 0;font-size:15px;line-height:1.55;color:var(--mc-dim)}

/* ── ПЯТЬ ГЛАГОЛОВ ── */
.mc-verbs{background:var(--mc-ink);color:#fff}
.mc-verbs .mc-sec__h{color:#fff}
.mc-verbs .mc-sec__sub{color:rgba(255,255,255,.62)}
.mc-verbs__list{margin-top:clamp(30px,4vw,54px);border-top:1px solid rgba(255,255,255,.18)}
.mc-verb{border-bottom:1px solid rgba(255,255,255,.18)}
.mc-verb__b{display:flex;align-items:baseline;gap:clamp(12px,2vw,26px);width:100%;
 padding:clamp(15px,2vw,25px) 0;background:none;border:0;cursor:pointer;text-align:left;
 color:rgba(255,255,255,.55);font-family:'Playfair Display',Georgia,serif;
 font-size:clamp(27px,5.4vw,64px);line-height:1.02;font-weight:700;letter-spacing:-.02em;
 transition:color .3s}
.mc-verb__b:hover{color:rgba(255,255,255,.85)}
.mc-verb.is-on .mc-verb__b{color:#fff}
.mc-verb.is-on .mc-verb__b em{color:var(--mc-red)}
.mc-verb__n{font-family:'Jost',Arial,sans-serif;font-size:11px;font-weight:600;
 letter-spacing:.2em;color:var(--mc-red);flex:0 0 auto}
.mc-verb__p{overflow:hidden;max-height:0;transition:max-height .55s cubic-bezier(.4,0,.2,1)}
.mc-verb.is-on .mc-verb__p{max-height:900px}
.mc-verb__in{display:grid;grid-template-columns:.85fr 1.15fr;gap:clamp(18px,3vw,40px);
 padding:0 0 clamp(24px,3vw,38px);align-items:center}
.mc-verb__in p{font-size:clamp(15px,1.4vw,17.5px);line-height:1.68;color:rgba(255,255,255,.76)}
.mc-verb__in img{width:100%;aspect-ratio:4/3;object-fit:cover}

/* ── РАЗБОР ЗАСТРОЙКИ (сигнатура) ── */
.mc-build{background:var(--mc-paper2)}
.mc-build__tabs{display:flex;flex-wrap:wrap;gap:8px;margin-top:clamp(26px,3.5vw,44px)}
.mc-build__tab{border:1px solid var(--mc-line);background:transparent;cursor:pointer;
 padding:10px 17px;border-radius:999px;font:500 14px/1 'Jost',Arial,sans-serif;
 color:var(--mc-ink);transition:background .2s,color .2s,border-color .2s}
.mc-build__tab:hover{border-color:var(--mc-ink)}
.mc-build__tab.is-on{background:var(--mc-ink);border-color:var(--mc-ink);color:#fff}
.mc-build__stage{margin-top:22px;display:grid;grid-template-columns:1.5fr .85fr;
 gap:clamp(20px,3vw,40px);align-items:start}
.mc-shot{position:relative;background:var(--mc-ink);overflow:hidden}
.mc-shot__l{display:none}
.mc-shot__l.is-on{display:block}
.mc-shot img{width:100%}
.mc-hot{position:absolute;margin:0;padding:0;background:transparent;cursor:pointer;
 border:1.5px solid rgba(255,255,255,.42);border-radius:2px;
 box-shadow:0 0 0 1px rgba(0,0,0,.22);transition:border-color .25s,background .25s,
 box-shadow .25s}
.mc-hot:hover,.mc-hot:focus-visible,.mc-hot.is-lit{border-color:var(--mc-red);
 background:rgba(210,4,45,.18);box-shadow:0 0 0 1px rgba(255,255,255,.45);outline:none}
/* подпись — только у того модуля, на который навели; подсветка от списка
   набора зажигает рамки, но не вываливает пачку ярлыков поверх снимка */
.mc-hot__t{position:absolute;left:0;top:100%;margin-top:5px;
 background:var(--mc-red);color:#fff;font:600 11px/1.32 'Jost',Arial,sans-serif;
 letter-spacing:.04em;padding:6px 9px;opacity:0;transform:translateY(-4px);
 transition:opacity .2s,transform .2s;pointer-events:none;
 width:max-content;max-width:min(210px,42vw);z-index:2}
.mc-hot:hover .mc-hot__t,.mc-hot:focus-visible .mc-hot__t{opacity:1;transform:none}
.mc-hot:hover,.mc-hot:focus-visible{z-index:3}
.mc-hot.is-low .mc-hot__t{top:auto;bottom:100%;margin:0 0 5px}
.mc-hot.is-right .mc-hot__t{left:auto;right:0}
.mc-build__side{position:sticky;top:22px}
.mc-build__s{display:none}
.mc-build__s.is-on{display:block}
.mc-build__name{font-family:'Playfair Display',Georgia,serif;font-size:clamp(24px,2.6vw,34px);
 font-weight:700;line-height:1.06}
.mc-build__where{margin-top:7px;font-size:12px;font-weight:600;letter-spacing:.15em;
 text-transform:uppercase;color:var(--mc-red)}
.mc-build__txt{margin-top:16px;font-size:15px;line-height:1.66;color:var(--mc-dim)}
.mc-kit{margin-top:24px;border-top:2px solid var(--mc-ink);padding-top:16px}
.mc-kit__h{font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;
 color:var(--mc-ink)}
.mc-kit__l{margin:14px 0 0;padding:0;list-style:none;display:grid;gap:2px}
.mc-kit__i{display:flex;align-items:center;gap:10px;width:100%;border:0;background:none;
 cursor:pointer;padding:8px 10px;margin:0 -10px;text-align:left;border-radius:3px;
 font:500 14.5px/1.3 'Jost',Arial,sans-serif;color:#B5ADA7;transition:color .2s,background .2s}
.mc-kit__i:before{content:'';width:9px;height:9px;flex:0 0 9px;border:1.5px solid currentColor;
 border-radius:2px;transition:background .2s}
.mc-kit__i.on{color:var(--mc-ink)}
.mc-kit__i.on:before{background:var(--mc-red);border-color:var(--mc-red)}
.mc-kit__i.on:hover,.mc-kit__i.on:focus-visible{background:rgba(21,17,15,.06);outline:none}
.mc-kit__i:not(.on){cursor:default}
.mc-kit__n{margin-left:auto;font-size:12px;font-weight:600;color:#B5ADA7}
.mc-kit__i.on .mc-kit__n{color:var(--mc-red)}

/* ── ПРИЗ ВЕЛИКОЛЕПИЯ ── */
.mc-prix{background:var(--mc-ink2);color:#fff;
 background-image:radial-gradient(90% 60% at 50% 0,rgba(168,124,42,.35),transparent 65%)}
.mc-prix .mc-sec__h{color:#fff}
.mc-prix .mc-sec__sub{color:rgba(255,255,255,.62)}
.mc-prix .mc-rule{background:var(--mc-gold)}
.mc-prix .mc__eyebrow{color:var(--mc-gold-l)}
.mc-prix__g{margin-top:clamp(30px,4vw,54px);display:grid;
 grid-template-columns:repeat(3,1fr);gap:clamp(16px,2vw,30px)}
.mc-prix__c{border-top:2px solid var(--mc-gold);padding-top:16px}
.mc-prix__y{font-family:'Playfair Display',Georgia,serif;font-size:clamp(34px,4vw,56px);
 font-weight:700;line-height:1;color:var(--mc-gold-l)}
.mc-prix__c img{margin-top:16px;width:100%;aspect-ratio:4/3;object-fit:cover}
.mc-prix__c p{margin-top:14px;font-size:14.5px;line-height:1.62;color:rgba(255,255,255,.72)}

/* ── FENDI ── */
.mc-fendi{background:#0E0C09;color:#fff}
.mc-fendi .mc-sec__h{color:#fff}
.mc-fendi .mc-sec__sub{color:rgba(255,255,255,.6)}
.mc-fendi .mc-rule{background:#F2C300}
.mc-fendi .mc__eyebrow{color:#F2C300}
.mc-fendi__g{margin-top:clamp(28px,4vw,50px);display:grid;
 grid-template-columns:1.35fr 1fr;grid-template-rows:auto auto;gap:clamp(14px,1.8vw,24px)}
.mc-fendi__g figure{display:flex;flex-direction:column;min-width:0;margin:0}
.mc-fendi__g figure:first-child{grid-row:span 2}
.mc-fendi__g img{width:100%;flex:1 1 auto;min-height:0;object-fit:cover}
.mc-fendi__g figure:first-child img{aspect-ratio:3/4}
.mc-fendi__g figure+figure img{aspect-ratio:3/2}
.mc-fendi .mc-cap{color:rgba(255,255,255,.5)}

/* ── ПОДАРОК ЗА ПОКУПКУ ── */
.mc-gift{background:var(--mc-red);color:#fff}
.mc-gift .mc-sec__h{color:#fff}
.mc-gift .mc-sec__sub{color:rgba(255,255,255,.82)}
.mc-gift .mc-rule{background:#fff}
.mc-gift .mc__eyebrow{color:rgba(255,255,255,.75)}
.mc-gift__g{margin-top:clamp(30px,4vw,52px);display:grid;
 grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,.3)}
.mc-gift__c{background:var(--mc-red);padding:clamp(20px,2.6vw,32px)}
.mc-gift__v{font-family:'Playfair Display',Georgia,serif;font-size:clamp(32px,3.8vw,52px);
 font-weight:700;line-height:1}
.mc-gift__w{margin-top:10px;font-size:12px;font-weight:600;letter-spacing:.16em;
 text-transform:uppercase;color:rgba(255,255,255,.8)}
.mc-gift__d{margin-top:4px;font-size:14px;font-weight:500;color:#fff}
.mc-gift__c p{margin-top:15px;font-size:14.5px;line-height:1.62;color:rgba(255,255,255,.86)}
.mc-gift__ph{margin-top:clamp(22px,3vw,36px);display:grid;grid-template-columns:1fr 1fr;
 gap:clamp(14px,2vw,24px)}
.mc-gift__ph img{width:100%;aspect-ratio:4/3;object-fit:cover}
.mc-gift .mc-cap{color:rgba(255,255,255,.72)}

/* ── ФИНАЛЬНЫЙ ВЕЧЕР ── */
.mc-night{background:var(--mc-night);color:#fff;
 background-image:radial-gradient(100% 70% at 20% 0,rgba(131,71,176,.5),transparent 60%)}
.mc-night .mc-sec__h{color:#fff}
.mc-night .mc-sec__sub{color:rgba(255,255,255,.68)}
.mc-night .mc-rule{background:var(--mc-violet)}
.mc-night .mc__eyebrow{color:#D6AEF5}
.mc-ribbon{margin-top:clamp(28px,3.5vw,46px);position:relative}
.mc-ribbon__t{display:flex;gap:clamp(12px,1.6vw,20px);overflow-x:auto;
 scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:18px;
 scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.3) transparent}
.mc-ribbon__t::-webkit-scrollbar{height:4px}
.mc-ribbon__t::-webkit-scrollbar-thumb{background:rgba(255,255,255,.3);border-radius:4px}
.mc-ribbon__c{flex:0 0 clamp(230px,32vw,380px);scroll-snap-align:start}
.mc-ribbon__c img{width:100%;aspect-ratio:16/9;object-fit:cover}
.mc-ribbon__n{margin-top:12px;display:flex;align-items:baseline;gap:9px;
 font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#D6AEF5}
.mc-ribbon__h{margin-top:5px;font-family:'Playfair Display',Georgia,serif;font-size:19px;
 font-weight:700;line-height:1.15}
.mc-ribbon__p{margin-top:7px;font-size:14px;line-height:1.55;color:rgba(255,255,255,.66)}
.mc-ribbon__nav{display:flex;gap:8px;margin-top:6px}
.mc-ribbon__b{width:42px;height:42px;border-radius:50%;border:1px solid rgba(255,255,255,.28);
 background:transparent;color:#fff;cursor:pointer;font-size:17px;line-height:1;
 transition:background .2s,border-color .2s}
.mc-ribbon__b:hover{background:rgba(255,255,255,.14);border-color:#fff}
.mc-ribbon__b[disabled]{opacity:.3;cursor:default}
.mc-player{margin-top:clamp(30px,4vw,52px)}
.mc-player video{width:100%;display:block;background:#000;aspect-ratio:16/9}

/* ── ВЫСТАВКИ ── */
.mc-expo{background:var(--mc-paper)}
.mc-expo__g{margin-top:clamp(28px,4vw,48px);display:grid;
 grid-template-columns:repeat(4,1fr);gap:clamp(12px,1.6vw,20px)}
.mc-expo__g img{width:100%;aspect-ratio:3/2;object-fit:cover}
.mc-expo__g figcaption{margin-top:9px;font-size:13px;line-height:1.45;color:var(--mc-dim)}

/* ── РЕЗУЛЬТАТ ── */
.mc-res{background:var(--mc-ink);color:#fff}
.mc-res .mc-sec__h{color:#fff}
.mc-res__g{margin-top:clamp(30px,4vw,52px);display:grid;
 grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:clamp(20px,2.6vw,36px)}
.mc-res__c{border-top:2px solid var(--mc-red);padding-top:16px}
.mc-res__c h3{font-size:clamp(19px,1.8vw,23px);line-height:1.2}
.mc-res__c p{margin-top:11px;font-size:14.5px;line-height:1.62;color:rgba(255,255,255,.68)}

@media(max-width:1000px){
 .mc-task__grid,.mc-build__stage,.mc-verb__in,.mc-fendi__g{grid-template-columns:1fr}
 .mc-fendi__g figure:first-child{grid-row:auto}
 .mc-fendi__g figure:first-child img{aspect-ratio:3/2}
 .mc-build__side{position:static}
 .mc-expo__g{grid-template-columns:repeat(3,1fr)}
 .mc-verb__in img{aspect-ratio:16/9}
}
@media(max-width:720px){
 .mc__wrap{padding:0 16px}
 .mc-prix__g,.mc-gift__g,.mc-gift__ph{grid-template-columns:1fr}
 .mc-expo__g{grid-template-columns:repeat(2,1fr)}
 .mc-hot__t{font-size:10px;padding:5px 7px;max-width:56vw}
 .mc-ribbon__nav{display:none}
}
@media(max-width:480px){
 .mc-hero__facts{grid-template-columns:1fr 1fr}
}
@media(prefers-reduced-motion:reduce){
 .mc-r{opacity:1;transform:none;transition:none}
 .mc-verb__p{transition:none}
}
</style>"""


# ─── сборка секций ──────────────────────────────────────────────────────────
def hero():
    facts = ''.join('<div class="mc-hero__f"><dt>%s</dt><dd>%s</dd></div>' % (k, v)
                    for k, v in FACTS)
    return f'''<section class="mc-hero">
<div class="mc-hero__bg">{pic('stand-arch', 'Застройка Marie Claire в галерее торгового центра: стены с графикой, красный подиум и скруглённый торец', lazy=False)}</div>
<div class="mc-hero__in"><div class="mc__wrap">
<a class="mc-back" href="/project/">← Проекты</a>
<h1>Marie Claire выходит <em>из&nbsp;киоска</em> в&nbsp;галерею</h1>
<p class="mc-hero__lead">Серия кросс-мероприятий журнала в торговых центрах Москвы: застройка галерей,
семплинг и кросс-промо с косметическими и модными брендами, финальный вечер для покупателей.</p>
<dl class="mc-hero__facts">{facts}</dl>
</div></div></section>'''


def task():
    return f'''<section class="mc-sec mc-task"><div class="mc__wrap">
<div class="mc-task__grid">
<div class="mc-r">
<div class="mc-rule"></div>
<h2 class="mc-sec__h">Журнал читают дома. Покупают — здесь</h2>
<div class="mc-task__body" style="margin-top:24px">
<p>Marie Claire — французский женский журнал, издаётся с 1937 года, российское издание
выходит с конца девяностых. Аудитория известна и точно описана, но живёт она в тираже:
читательница берёт номер, уносит домой и там остаётся один на один с рекламой бренда.</p>
<p>Задача была развернуть эту связь: привести журнал туда, где та же женщина уже тратит
деньги, — в галерею торгового центра. Тогда бренд-партнёр получает не полосу, а живой
контакт с продуктом, а торговый центр — повод, по которому в него идут специально.</p>
<p>Мы сделали серию: застроили основные галереи ГУМа, Европейского, Атриума и Метрополиса
корпусом Marie Claire, разработали POSm в точках продаж брендов-участников, вели семплинг
и промо-механику подарка за покупку, а закрыли серию вечером для покупателей — с показом
мод, разбором образов от экспертов и выступлением группы.</p>
</div></div>
<div class="mc-task__side mc-r">
<dl>
<dt>Площадки</dt><dd>ГУМ, Европейский, Атриум, Метрополис. Плюс выставки индустрии
красоты, турниры и спортивные комплексы.</dd>
<dt>Бренды-партнёры</dt><dd>Clarins, Estée Lauder, Dior, Yves Saint Laurent, Fendi,
Garnier, Vichy, L’Occitane, Oxette, Pilgrim, Cloud Nine.</dd>
<dt>Состав работ</dt><dd>Застройка галерей, разработка и производство POSm, промо-персонал
и семплинг, кросс-промо с магазинами центра, финальное мероприятие.</dd>
</dl>
</div></div></div></section>'''


def verbs():
    items = []
    for i, (verb, img, alt, txt) in enumerate(VERBS):
        on = ' is-on' if i == 0 else ''
        items.append(f'''<div class="mc-verb{on}">
<button class="mc-verb__b" type="button" data-i="{i}" aria-expanded="{'true' if i == 0 else 'false'}">
<span class="mc-verb__n">{i + 1:02d}</span><span>{verb}</span></button>
<div class="mc-verb__p"><div class="mc-verb__in">
{pic(img, alt)}
<p>{txt}</p>
</div></div></div>''')
    return f'''<section class="mc-sec mc-verbs"><div class="mc__wrap">
<div class="mc-r">
<p class="mc__eyebrow">Надпись на стенах корпуса</p>
<h2 class="mc-sec__h" style="margin-top:18px">Пять глаголов, по которым собрана площадка</h2>
<p class="mc-sec__sub">Формулу придумали не мы: она напечатана на торцах самой застройки и
повторяется на пресс-волле финального вечера. Мы взяли её как техническое задание —
каждый глагол должен был получить на площадке свою рабочую зону.</p>
</div>
<div class="mc-verbs__list mc-r">{''.join(items)}</div>
</div></section>'''


def build():
    tabs, shots, sides = [], [], []
    for i, (bid, name, where, img, cap, txt, hots) in enumerate(BUILDS):
        on = ' is-on' if i == 0 else ''
        tabs.append('<button class="mc-build__tab%s" type="button" data-b="%d">%s</button>'
                    % (on, i, name))
        hh = []
        for kind, label, x, y, w, h in hots:
            cls = 'mc-hot'
            if y + h > 74:
                cls += ' is-low'
            if x + w > 78:
                cls += ' is-right'
            hh.append('<button class="%s" type="button" data-k="%s" '
                      'style="left:%s%%;top:%s%%;width:%s%%;height:%s%%" '
                      'aria-label="%s"><span class="mc-hot__t">%s</span></button>'
                      % (cls, kind, x, y, w, h, label, label))
        shots.append('<div class="mc-shot__l%s" data-b="%d">%s%s</div>'
                     % (on, i, pic(img, cap, lazy=(i != 0)), ''.join(hh)))
        kinds = [k for k, _l, _x, _y, _w, _h in hots]
        kit = []
        for kid, klabel in KIT:
            n = kinds.count(kid)
            cls = 'mc-kit__i on' if n else 'mc-kit__i'
            kit.append('<li><button class="%s" type="button" data-k="%s"%s>%s'
                       '<span class="mc-kit__n">%s</span></button></li>'
                       % (cls, kid, '' if n else ' tabindex="-1" aria-disabled="true"',
                          klabel, ('×%d' % n) if n else '—'))
        sides.append(f'''<div class="mc-build__s{on}" data-b="{i}">
<div class="mc-build__name">{name}</div>
<div class="mc-build__where">{where}</div>
<p class="mc-build__txt">{txt}</p>
<div class="mc-kit"><div class="mc-kit__h">Набор модулей</div>
<ul class="mc-kit__l">{''.join(kit)}</ul></div>
</div>''')
    return f'''<section class="mc-sec mc-build" id="build"><div class="mc__wrap">
<div class="mc-r">
<div class="mc-rule"></div>
<p class="mc__eyebrow">Разбор застройки</p>
<h2 class="mc-sec__h" style="margin-top:18px">Один набор модулей — шесть разных площадок</h2>
<p class="mc-sec__sub">Серия держалась на том, что застройка не проектировалась каждый раз
с нуля. Один набор модулей — стены с графикой, витрины, стойки, посадка, фигурные элементы,
оборудование и подиум — пересобирался под бренд, под площадь в галерее и под задачу.
Переключите партнёра и наведите на модуль в списке: на снимке видно, что набор тот же,
а площадка каждый раз другая.</p>
</div>
<div class="mc-build__tabs mc-r" role="tablist">{''.join(tabs)}</div>
<div class="mc-build__stage mc-r">
<div class="mc-shot">{''.join(shots)}</div>
<div class="mc-build__side">{''.join(sides)}</div>
</div>
<p class="mc__note">Рамки модулей размечены по самим фотографиям и визуализациям проекта.
Кадры Clarins и Estée Lauder — проектные визуализации корнеров до постройки, остальные —
съёмка готовых площадок.</p>
</div></section>'''


def prix():
    cards = ''.join(f'''<div class="mc-prix__c mc-r">
<div class="mc-prix__y">{year}</div>{pic(img, alt)}<p>{txt}</p></div>''' for year, img, alt, txt in PRIX)
    return f'''<section class="mc-sec mc-prix"><div class="mc__wrap">
<div class="mc-r">
<div class="mc-rule"></div>
<p class="mc__eyebrow">Prix d’Excellence de la Beauté</p>
<h2 class="mc-sec__h" style="margin-top:18px">«Приз великолепия» — три года подряд</h2>
<p class="mc-sec__sub">Премия журнала за достижения в индустрии красоты — единственный
формат серии, который повторялся из года в год. Площадка каждый раз собиралась заново,
но задача оставалась одна: лауреаты должны стоять так, чтобы к ним подходили, а рядом
работали косметолог и визажист.</p>
</div>
<div class="mc-prix__g">{cards}</div>
<p class="mc__note">Годы взяты с самих застроек: 2011 и 2012 — на стеле премии,
2013 — на витрине с обложкой номера.</p>
</div></section>'''


def fendi():
    return f'''<section class="mc-sec mc-fendi"><div class="mc__wrap">
<div class="mc-r">
<div class="mc-rule"></div>
<p class="mc__eyebrow">Fan di FENDI</p>
<h2 class="mc-sec__h" style="margin-top:18px">Запуск аромата посреди торговой галереи</h2>
<p class="mc-sec__sub">Отдельная сборка под запуск: чёрно-жёлтая площадка с пресс-воллом
во всю заднюю стену, аромат-баром и креслами. Логика та же, что и в белом корпусе, но
набор смещён от выкладки к тестированию — гостья садится, пробует и остаётся.</p>
</div>
<div class="mc-fendi__g mc-r">
<figure class="mc-fig">{pic('fendi-desk', 'Жёлтый аромат-бар Fan di FENDI с флаконами и раздаточными материалами')}
<figcaption class="mc-cap">Аромат-бар: тестирование и раздаточные материалы</figcaption></figure>
<figure class="mc-fig">{pic('fendi-wall', 'Пресс-волл с повторяющимися логотипами Fan di FENDI и marie claire')}
<figcaption class="mc-cap">Пресс-волл: логотипы бренда и журнала в один ритм</figcaption></figure>
<figure class="mc-fig">{pic('fendi-bar', 'Консультация с гостьей за столом на площадке Fan di FENDI')}
<figcaption class="mc-cap">Работа с гостьей за столом площадки</figcaption></figure>
</div>
</div></section>'''


def gift():
    cards = ''.join(f'''<div class="mc-gift__c mc-r">
<div class="mc-gift__v">{v}</div><div class="mc-gift__w">{w}</div>
<div class="mc-gift__d">{d}</div><p>{t}</p></div>''' for v, w, d, t in GIFT)
    return f'''<section class="mc-sec mc-gift"><div class="mc__wrap">
<div class="mc-r">
<div class="mc-rule"></div>
<p class="mc__eyebrow">Кросс-промо</p>
<h2 class="mc-sec__h" style="margin-top:18px">Подарок от журнала за чек в магазине центра</h2>
<p class="mc-sec__sub">Механика, которая связывала журнал, магазины и покупателя в одну
цепочку: покупка у партнёра — чек на стойке Marie Claire — подарок. Она же давала торговому
центру измеримый эффект, а брендам — причину участвовать.</p>
</div>
<div class="mc-gift__g">{cards}</div>
<div class="mc-gift__ph mc-r">
<figure class="mc-fig">{pic('promo-team', 'Промо-группа Marie Claire у стойки с условиями акции в галерее торгового центра')}
<figcaption class="mc-cap">Стойка в галерее: условия акции на руках у промо-группы</figcaption></figure>
<figure class="mc-fig">{pic('gift-bags', 'Подготовленные фирменные пакеты Marie Claire с подарками перед выдачей')}
<figcaption class="mc-cap">Подарки, собранные до открытия площадки</figcaption></figure>
</div>
<p class="mc__note">Пороги и даты — с табличек на стойках промо-группы и из съёмки вечера.</p>
</div></section>'''


def night():
    cards = ''.join(f'''<article class="mc-ribbon__c">{pic(img, alt)}
<div class="mc-ribbon__n">{i + 1:02d}</div>
<h3 class="mc-ribbon__h">{title}</h3>
<p class="mc-ribbon__p">{txt}</p></article>'''
                    for i, (img, title, alt, txt) in enumerate(NIGHT))
    w, h = SIZE['night-poster']
    return f'''<section class="mc-sec mc-night"><div class="mc__wrap">
<div class="mc-r">
<div class="mc-rule"></div>
<p class="mc__eyebrow">ТЦ «Метрополис» · финал серии</p>
<h2 class="mc-sec__h" style="margin-top:18px">Вечер, который начинался засветло и кончался в три ночи</h2>
<p class="mc-sec__sub">Финальное мероприятие собрало на одной площадке всё, что серия
отрабатывала по частям: сервисные зоны, показ мод с разбором образов, шоу-программу
с живым выступлением и награждение. Ниже — смена по порядку, как её снял оператор.</p>
</div>
<div class="mc-ribbon mc-r">
<div class="mc-ribbon__t" id="mcRibbon" tabindex="0" role="group" aria-label="Хроника вечера">{cards}</div>
<div class="mc-ribbon__nav"><button class="mc-ribbon__b" type="button" data-d="-1" aria-label="Назад">←</button>
<button class="mc-ribbon__b" type="button" data-d="1" aria-label="Вперёд">→</button></div>
</div>
<div class="mc-player mc-r">
<video controls preload="none" playsinline poster="{IMG}/night-poster.jpg" width="{w}" height="{h}">
<source src="{VIDEO}" type="video/mp4">Ваш браузер не поддерживает видео.</video>
<p class="mc-cap">Съёмка финального вечера в ТЦ «Метрополис», 2 минуты 37 секунд</p>
</div>
</div></section>'''


def expo():
    cards = ''.join(f'''<figure class="mc-fig mc-r">{pic(img, alt)}
<figcaption>{cap}</figcaption></figure>''' for img, alt, cap in EXPO)
    return f'''<section class="mc-sec mc-expo"><div class="mc__wrap">
<div class="mc-r">
<div class="mc-rule"></div>
<h2 class="mc-sec__h">За пределами торговых центров</h2>
<p class="mc-sec__sub">Тот же набор модулей уезжал на выставки индустрии красоты,
турниры и спортивные площадки — там он собирался в мобильном варианте, на роллапах
и разборной стойке, без подиума и капитальных стен.</p>
</div>
<div class="mc-expo__g">{cards}</div>
</div></section>'''


def result():
    cards = [
        ('KPI выполнены во всех центрах',
         'По числу участников и по уровню организации проект закрыл показатели на всех '
         'площадках серии — в ГУМе, Европейском, Атриуме и Метрополисе.'),
        ('Формат оказался тиражируемым',
         'Один набор модулей отработал шесть разных сборок и три года подряд держал '
         'премию «Приз великолепия». Каждая следующая площадка обходилась дешевле '
         'проектирования с нуля.'),
        ('Журнал стал точкой на карте центра',
         'Кросс-промо связало полосу в журнале, витрину магазина и стойку в галерее: '
         'бренд-партнёр получал не только контакт, но и чек.'),
    ]
    g = ''.join(f'<div class="mc-res__c mc-r"><h3>{h}</h3><p>{p}</p></div>' for h, p in cards)
    return f'''<section class="mc-sec mc-res"><div class="mc__wrap">
<div class="mc-r"><div class="mc-rule"></div><h2 class="mc-sec__h">Результат</h2></div>
<div class="mc-res__g">{g}</div>
</div></section>'''


PAGE_JS = """<script>(function(){
var d=document,RM=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;

// ── появление блоков ──
var rs=[].slice.call(d.querySelectorAll('.mc-r'));
if(RM||!window.IntersectionObserver){rs.forEach(function(e){e.classList.add('in');});}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){
 if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},
 {rootMargin:'0px 0px -8% 0px'});rs.forEach(function(e){io.observe(e);});}

// ── пять глаголов: раскрывается один ──
var verbs=[].slice.call(d.querySelectorAll('.mc-verb'));
verbs.forEach(function(v){
 var b=v.querySelector('.mc-verb__b');
 b.addEventListener('click',function(){
  var on=v.classList.contains('is-on');
  verbs.forEach(function(o){o.classList.remove('is-on');
   o.querySelector('.mc-verb__b').setAttribute('aria-expanded','false');});
  if(!on){v.classList.add('is-on');b.setAttribute('aria-expanded','true');}
 });
});

// ── разбор застройки ──
var tabs=[].slice.call(d.querySelectorAll('.mc-build__tab')),
    shots=[].slice.call(d.querySelectorAll('.mc-shot__l')),
    sides=[].slice.call(d.querySelectorAll('.mc-build__s'));
function showBuild(i){
 tabs.forEach(function(t,k){t.classList.toggle('is-on',k===i);});
 shots.forEach(function(s,k){s.classList.toggle('is-on',k===i);});
 sides.forEach(function(s,k){s.classList.toggle('is-on',k===i);});
}
tabs.forEach(function(t){t.addEventListener('click',function(){showBuild(+t.getAttribute('data-b'));});});
// подсветка модулей набора: с наведения на пункт списка загораются рамки на снимке
function lit(kind,on){
 var box=d.querySelector('.mc-shot__l.is-on');if(!box)return;
 [].slice.call(box.querySelectorAll('.mc-hot')).forEach(function(h){
  if(!kind||h.getAttribute('data-k')===kind)h.classList.toggle('is-lit',on);});
}
[].slice.call(d.querySelectorAll('.mc-kit__i.on')).forEach(function(b){
 var k=b.getAttribute('data-k');
 ['mouseenter','focus'].forEach(function(ev){b.addEventListener(ev,function(){lit(k,true);});});
 ['mouseleave','blur'].forEach(function(ev){b.addEventListener(ev,function(){lit(k,false);});});
 // тач: подсветка держится, пока не тронут другой пункт
 b.addEventListener('click',function(){lit(null,false);lit(k,true);});
});

// ── лента вечера ──
var rib=d.getElementById('mcRibbon');
if(rib){
 [].slice.call(d.querySelectorAll('.mc-ribbon__b')).forEach(function(b){
  b.addEventListener('click',function(){
   var c=rib.querySelector('.mc-ribbon__c');
   var step=c?c.getBoundingClientRect().width+16:300;
   rib.scrollBy({left:step*(+b.getAttribute('data-d')),behavior:RM?'auto':'smooth'});
  });
 });
 function ends(){
  var b=[].slice.call(d.querySelectorAll('.mc-ribbon__b'));
  if(b.length<2)return;
  b[0].disabled=rib.scrollLeft<4;
  b[1].disabled=rib.scrollLeft>=rib.scrollWidth-rib.clientWidth-4;
 }
 rib.addEventListener('scroll',ends);window.addEventListener('resize',ends);ends();
}
})();</script>"""

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
                 '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"Кросс-мероприятия Marie Claire в торговых центрах Москвы",'
                 '"item":"' + URL + '"}]}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Кросс-мероприятия Marie Claire в ТЦ Москвы | кейс Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: серия мероприятий журнала Marie Claire в торговых центрах Москвы — ГУМ, Европейский, Атриум, Метрополис. Застройка галерей, POSm для брендов-партнёров, семплинг и кросс-промо с подарком за покупку, премия «Приз великолепия» три года подряд и финальный вечер с показом мод и шоу-программой.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Кросс-мероприятия Marie Claire в торговых центрах Москвы | Hand Marketing">
<meta property="og:description" content="Один набор модулей застройки, шесть площадок и три года: как журнал вышел из киоска в галерею ТЦ. Семплинг, кросс-промо с чеком и финальный вечер до трёх ночи.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/stand-arch.jpg">
<meta property="og:site_name" content="Hand Marketing"><meta property="og:locale" content="ru_RU">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/playfair-jost.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def page():
    return (HEAD + rc.header() + '<main class="mc">' + hero() + task() + verbs() +
            build() + prix() + fendi() + gift() + night() + expo() + result() +
            '</main><a id="lead"></a>' + rc.footer() + rc.JS + PAGE_JS +
            BREADCRUMB_LD + '</body></html>')


if __name__ == '__main__':
    out = os.path.join(ROOT, 'event', 'marieclaire')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page())
    # index-a2.html — деплой-источник (workflow переименовывает его в index.html)
    # и затёр бы кастомную страницу на проде.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('удалён устаревший index-a2.html')
    print('written', os.path.join(out, 'index.html'))
