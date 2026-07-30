#!/usr/bin/env python3
"""Генерит mirror/creative/becar/smile/index.html — кейс «Брошюра ТЦ „Смайл“»
для Becar Asset Management: издание на 22 полосы, которым продавали лоты
в действующем торговом центре у метро Дыбенко в Петербурге.

Дизайн-концепция: «жёлтая дуга сшивает две половины». В брошюре лист всегда
поделён на две зоны: мятная это район, люди и эмоция, фиолетовая это деньги
и инвестор. Единственное, что их сшивает, жёлтая дуга, и на ней же нанизаны
цифры объекта. Веб-аналог: Manrope (дисплей) + Onest (текст) из
/fonts/manrope-onest.css, деление секций по дуге, три опознаваемых приёма
издания (текст-эхо во всю полосу, жёлтые цифры в неоне на фиолетовом,
смайл вместо маркера списка).

Живые блоки:
  • дуга с цифрами объекта: SVG прочерчивается по скроллу, кружки нанизаны
    на путь через сэмплирование безье, подпись раскрывается по наведению;
  • «стрит-ритейл или кондо-ТЦ» — тумблер на смысловом ядре первого разворота;
  • калькулятор дохода по трём доходным продуктам Becar из брошюры
    (ТЦ «Смайл» до 13%, БЦ «Станция» от 10%, апарт-отель «Вертикаль» до 17%);
  • зоны охвата на карте издания: первичная 28 000, вторичная 105 000;
  • листалка из 10 разворотов со скролл-снапом и лайтбоксом.

Ассеты: mirror/images/smile-broch/ (scripts/smile-broch-assets.py), логотипы
сетевых арендаторов переиспользуем из кейса посадочной страницы /images/smile.

Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import os
import importlib.util
import math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/smile-broch'
TEN = '/images/smile/tenants'          # логотипы сетей из кейса посадочной страницы
URL = 'https://hand-marketing.ru/creative/becar/smile/'

# ─── 10 разворотов: (полосы, глава, заголовок, описание, alt) ────────────────
SPREADS = [
 ('2-3', 'Формат',
  'Стрит-ритейл или торговый центр',
  'Первый разворот отвечает на самый частый запрос частного инвестора. Слева пять '
  'причин, почему покупка стрит-ритейла сложнее, чем кажется: один арендатор решает '
  'одну задачу покупателя, а если покупатели не приходят, платить инвестору не с чего. '
  'Справа кондо-ТЦ: синергия арендаторов, доход с мест общего пользования и три '
  'гарантии дохода.',
  'Разворот брошюры ТЦ «Смайл»: сравнение стрит-ритейла и кондо-ТЦ, гарантии дохода'),
 ('4-5', 'Формат',
  'Как владеть и стабильно получать доход',
  'Разворот про миссию объекта: торговый центр как центр коммуникации жителей района. '
  'Справа три опоры арендного дохода, лояльные посетители, лояльные арендаторы '
  'и единая концепция управления, каждая разложена на конкретные пункты. Фотография '
  'цепи работает метафорой связки, в которой нет слабого звена.',
  'Разворот брошюры ТЦ «Смайл»: миссия объекта и три опоры арендного дохода'),
 ('6-7', 'Объект',
  'Действующий торговый центр',
  'Главный разворот издания и самый чистый пример приёма. Слева мятная половина '
  'с контурным логотипом и определением объекта, справа фиолетовая с цифрами: '
  '100% заполняемость, 133 000 потенциальных покупателей в зоне охвата, '
  '7160 посетителей в сутки. Дугу от одной половины к другой ведёт жёлтая линия, '
  'на неё нанизаны 15+ тыс. кв. м, три этажа, 60 арендаторов и лоты от 2 млн рублей.',
  'Разворот брошюры ТЦ «Смайл»: цифры действующего торгового центра на жёлтой дуге'),
 ('8-9', 'Объект',
  '80% площадей у сетевых арендаторов',
  'Шесть причин вложиться собраны в столбик со смайлами вместо маркеров: '
  '15 000 кв. м, доступный порог входа, опробованная концепция, проработанный микс '
  'арендаторов, стандарты управления и собственное event-агентство. Справа '
  'доказательство одной цифрой и логотипами сетей, а QR-код ведёт на планировки '
  'и предложения в продаже.',
  'Разворот брошюры ТЦ «Смайл»: шесть причин инвестировать и логотипы сетевых арендаторов'),
 ('10-11', 'Управление',
  'Секрет успеха: семь лет управления',
  'Разворот про управляющую компанию. За семь лет команда Becar сделала из '
  'неприметного полупустого объекта центр притяжения района, и это показано не '
  'словами, а девятью цифрами роста: посещаемость +115%, доходность +54,4%, '
  'арендопригодная площадь +34%, доход с кв. м на 12% выше рынка. Внизу полосы '
  'фотографии объекта, чтобы цифры не висели в воздухе.',
  'Разворот брошюры ТЦ «Смайл»: цифры роста объекта за семь лет управления Becar'),
 ('12-13', 'Промо',
  'Smile Family, центр притяжения района',
  'Программа продвижения вынесена в отдельный разворот, потому что она и держит '
  'посещаемость. Слева описание добрососедской программы, справа цифры в неоновом '
  'свечении: 300 бесплатных мастер-классов, 14 уличных праздников, 35 экологических '
  'акций, больше 8000 подписчиков. Внизу отзывы жителей района без правки.',
  'Разворот брошюры ТЦ «Смайл»: программа Smile Family, цифры промо и отзывы жителей'),
 ('14-15', 'Локация',
  'Расположение и зона охвата',
  'Карта нарисована в цветах издания, поэтому она читается как часть брошюры, '
  'а не как скриншот. Жёлтые улицы, фиолетовая Нева, объект отмечен точкой '
  'у метро Дыбенко. Зона охвата залита подписями, а справа разложена на цифры: '
  '28 000 покупателей в первичной зоне и 105 000 во вторичной.',
  'Разворот брошюры ТЦ «Смайл»: карта района у метро Дыбенко и цифры зоны охвата'),
 ('16-17', 'Becar',
  'Доходные продукты на недвижимости',
  'Здесь издание переходит от объекта к компании. Четыре свойства продукта, '
  'основательность, управляемость, проверенность и сравнимость, объясняют, почему '
  'инвестор получает готовый инструмент, а не стройку. Справа вес группы цифрами: '
  '8 млн кв. м в управлении, 25 000 объектов, 5000 сотрудников, офисы в Лондоне, '
  'Петербурге и Москве.',
  'Разворот брошюры ТЦ «Смайл»: доходные продукты Becar и цифры группы компаний'),
 ('18-19', 'Becar',
  'БЦ «Станция»: платежи от структур РЖД',
  'Первый из двух соседних продуктов в линейке. Готовый арендный бизнес под ключ: '
  'структуры ОАО «РЖД» занимают 95% площади с 2009 года, долгосрочные договоры '
  'подписаны в 2016 и пролонгированы в 2019. Ниже аргумент, который сильнее ставки: '
  '35% повторных сделок, средний чек повторной покупки выше на 54%, 0% перепродаж '
  'в рынок.',
  'Разворот брошюры ТЦ «Смайл»: БЦ «Станция», арендные платежи от структур РЖД'),
 ('20-21', 'Becar',
  'Апарт-отель «Вертикаль» и кейс инвестора',
  'Финальный разворот показывает доходность на реальной истории. Первый '
  'сертифицированный кондо-отель категории 3* работает с 2014 года: средняя загрузка '
  '63% в первый год, на 15% выше сопоставимых отелей Петербурга. Рядом путь одного '
  'инвестора: купил лот в 2013 году, получал до 14% годовых, в 2017 продал '
  'под 10% доходности и заработал 2,8 млн рублей.',
  'Разворот брошюры ТЦ «Смайл»: апарт-отель «Вертикаль» и кейс инвестора с цифрами дохода'),
]

# ─── Дуга с цифрами объекта: (значение, единица, заголовок, подпись) ─────────
ARC = [
 ('15+', 'тыс. м²', '15 000 кв. м арендопригодной площади',
  'Площадь трёх этажей. В брошюре она стоит первой цифрой: с неё инвестор '
  'считает всё остальное.'),
 ('3', 'этажа', 'Три этажа с якорными арендаторами',
  'На каждом уровне свой якорь, поэтому посетитель поднимается выше: наверху '
  'есть за чем.'),
 ('60', 'арендаторов', '60 арендаторов сегмента эконом',
  'Сбалансированный пул: товары и услуги повседневного спроса, которые нужны '
  'каждый день.'),
 ('от 2', 'млн ₽', 'Лоты от 2 млн рублей',
  'Порог входа. Это та цифра, из-за которой частный инвестор вообще открывает '
  'брошюру про торговую недвижимость.'),
 ('13%', 'годовых, до', 'Доходность до 13% годовых',
  'Дуга заканчивается на ставке, дальше в издании идут только доказательства.'),
]

# ─── Стрит-ритейл против кондо-ТЦ: смысловое ядро первого разворота ──────────
STREET = [
 ('Один арендатор', 'Стрит-ритейл это один арендатор, а он решает только одну '
                    'задачу покупателя.'),
 ('Нет покупателей, нет дохода', 'Если к арендатору не приходят покупатели, '
                                 'платить инвестору ему нечем.'),
 ('Цена завышена', 'Стоимость стрит-ритейла, как правило, неоправданно завышена.'),
 ('Легко ошибиться', 'Историю арендатора на объекте и техническое соответствие '
                     'помещения проверяют редко, а ошибка стоит доходности.'),
 ('Простота только внешняя', 'Выбор помещения, арендатора и управление требуют '
                             'внимания к десяткам мелочей.'),
]
MALL = [
 ('Синергия арендаторов', 'Арендаторы дополняют друг друга и добавляют спрос: '
                          'один приводит клиентов другому.'),
 ('Доход шире аренды', 'Кроме платы арендатора инвестор получает доход с мест '
                       'общего пользования.'),
 ('Замену найти проще', 'Синергия внутри объекта не привязывает арендатора '
                        'к внешнему трафику и локации.'),
 ('Три гарантии дохода', 'Лояльность аудитории, лояльность арендаторов и единая '
                         'концепция управления.'),
]

# ─── Калькулятор: три доходных продукта из брошюры ──────────────────────────
PRODUCTS = [
 ('smile', 'ТЦ «Смайл»', 'до 13%', 13.0, 'Кондо-ТЦ, Петербург, лоты от 2 млн рублей'),
 ('station', 'БЦ «Станция»', 'от 10%', 10.0, 'Офисы, Москва, арендатор структуры РЖД'),
 ('vertical', 'Апарт-отель «Вертикаль»', 'до 17%', 17.0, 'Кондо-отель 3*, Петербург'),
]

# ─── Цифры управляющей компании с разворота 10-11 ───────────────────────────
SECRET = [
 ('+115%', 'выросла посещаемость объекта'),
 ('+54,4%', 'выросла доходность объекта'),
 ('+34%', 'увеличена арендопригодная площадь'),
 ('+12%', 'доход с кв. м выше рынка'),
 ('+18%', 'посещаемость выше средней по городу'),
 ('7160', 'посетителей в сутки'),
 ('4-6 раз', 'в месяц житель района заходит в ТЦ'),
 ('&gt;80%', 'площадей у сетевых арендаторов'),
]

# ─── Цифры промо с разворота 12-13 ──────────────────────────────────────────
FAMILY = [
 ('&gt;8000', 'лояльных подписчиков в соцсетях'),
 ('&gt;2000', 'публикаций в СМИ и соцсетях'),
 ('300', 'бесплатных мастер-классов'),
 ('14', 'больших уличных праздников'),
 ('35', 'экологических акций'),
 ('10', 'соцпроектов с гос. учреждениями'),
 ('5', 'фестивалей для молодёжи района'),
 ('6', 'арт-выставок детского творчества'),
]
SAYS = [
 ('С ребёнком не очень удобно добираться до крупных торговых центров, здорово, '
  'что в нашем районе есть ТЦ «Смайл», в нём можно купить всё необходимое'),
 ('С помощью ТЦ «Смайл» я могу реализовать свою экологическую инициативу: '
  'сдавать вещи и батарейки, обмениваться книгами, посещать лекции'),
 ('Спасибо за вчерашний мастер-класс «Квесты». Ребёнок и я в полном восторге, '
  'организация на высшем уровне, море впечатлений'),
]

# ─── Зоны охвата: (код, название, цифра, подпись, показывать первичную/вторичную) ──
ZONES = [
 ('first', 'Первичная зона', '28 000', 'покупателей живут в шаговой доступности '
  'от торгового центра', (True, False)),
 ('second', 'Вторичная зона', '105 000', 'покупателей приходят из соседних '
  'кварталов района', (False, True)),
 ('all', 'Зона охвата', '133 000', 'потенциальных покупателей в сумме, это цифра '
  'с обложки издания', (True, True)),
]
# точка объекта на карте (доли ширины и высоты кадра) и радиусы зон
MAP_X, MAP_Y = 0.738, 0.464
R_FIRST, R_SECOND = 0.23, 0.47

# ─── Логотипы сетей: (файл, подпись) ────────────────────────────────────────
TENANTS = [
 ('perekrestok', 'Перекрёсток'), ('sberbank', 'Сбербанк'), ('familiya', 'Familia'),
 ('modis', 'Modis'), ('kari', 'Kari'), ('trial_sport', 'Триал-Спорт'),
 ('redmond', 'Redmond'), ('detki', 'Детки'), ('bukvoed', 'Буквоед'),
 ('mts', 'МТС'), ('beeline', 'Билайн'), ('obuv-com', 'Obuv.com'),
 ('equipment', 'ВсеИнструменты'), ('kotofei', 'Котофей'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 5l-7 7 7 7"/></svg>')

# Смайл вместо маркера списка: в брошюре это жёлтый круг с белыми глазами
# и улыбкой. Тот же знак стоит в герое и моргает.
def smile_svg(cls='', blink=False):
    eyes = ('<g class="sb-smile__eyes"><path d="M40 40v12" /><path d="M60 40v12" /></g>'
            if blink else '<path d="M40 40v12" /><path d="M60 40v12" />')
    return (f'<svg class="sb-smile {cls}" viewBox="0 0 100 100" aria-hidden="true">'
            '<circle cx="50" cy="50" r="46" fill="#ffc324"/>'
            '<g fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round">'
            + eyes +
            '<path d="M33 60c4.6 8.4 10.2 12.6 17 12.6S63.4 68.4 68 60"/></g></svg>')


# ─── Точки на дуге: путь сэмплируем безье, чтобы кружки легли ровно ──────────
ARC_VB = (1200, 360)
ARC_SEGS = [                       # два кубических сегмента, как волна на полосе
    ((0, 74), (250, 74), (300, 292), (600, 292)),
    ((600, 292), (900, 292), (960, 96), (1200, 44)),
]
ARC_D = ('M0 74 C250 74 300 292 600 292 C900 292 960 96 1200 44')
ARC_T = [0.09, 0.30, 0.50, 0.72, 0.93]     # положение кружков по всей дуге


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u ** 3 * p0[i] + 3 * u * u * t * p1[i] + 3 * u * t * t * p2[i]
                 + t ** 3 * p3[i] for i in range(2))


def arc_point(u):
    """u от 0 до 1 по всей волне; сегменты равной длины по параметру."""
    seg = 0 if u < 0.5 else 1
    t = u * 2 if seg == 0 else (u - 0.5) * 2
    return bez(*ARC_SEGS[seg], t)


ARC_PTS = [arc_point(u) for u in ARC_T]

PAGE_CSS = """<style id="sb-css">
:root{
 --sb-vio:#4a3b9e;--sb-vio-d:#332a75;--sb-mint:#5fc1a8;--sb-teal:#29b8c4;
 --sb-yel:#ffc324;--sb-acid:#e4f03c;
 --sb-ink:#181a2c;--sb-ink2:#5f6480;--sb-paper:#f4f3fa;
 --sb-df:'Manrope',system-ui,-apple-system,Arial,sans-serif;
 --sb-tf:'Onest',system-ui,-apple-system,Arial,sans-serif;
 /* две половины листа. Мяту держим справа: слева идёт текст, а белое по мяте
    не вычитывается, в брошюре на мятной половине текст тоже тёмный */
 --sb-two:linear-gradient(100deg,#4a3b9e 0%,#4a3b9e 52%,#37b7bd 52%,#5fc1a8 100%);
}
.sb{font-family:var(--sb-tf);font-size:17px;line-height:1.62;color:var(--sb-ink);
 background:#fff;-webkit-font-smoothing:antialiased}
.sb *{box-sizing:border-box}
.sb h1,.sb h2,.sb h3,.sb h4{font-family:var(--sb-df);font-weight:800;line-height:1.05;
 letter-spacing:-.022em;margin:0;text-wrap:balance}
.sb p{margin:14px 0 0}
.sb a{color:inherit}
.sb-w{width:min(1240px,100% - 40px);margin-inline:auto}
.sb-kick{font-family:var(--sb-df);font-weight:700;font-size:12px;letter-spacing:.18em;
 text-transform:uppercase;display:block}
.sb-r{opacity:0;transform:translateY(22px);transition:opacity .7s cubic-bezier(.2,.7,.3,1),
 transform .7s cubic-bezier(.2,.7,.3,1)}
.sb-r.is-in{opacity:1;transform:none}
.sb-num{font-family:var(--sb-df);font-weight:800;font-variant-numeric:tabular-nums}

/* смайл вместо маркера: знак издания */
.sb-smile{width:26px;height:26px;flex:0 0 auto;display:block}
.sb-smile__eyes{transform-box:fill-box;transform-origin:center;
 animation:sb-blink 6.5s infinite}
@keyframes sb-blink{0%,90%,100%{transform:scaleY(1)}94%{transform:scaleY(.06)}}

/* ── ГЕРОЙ: две половины и дуга ── */
.sb-hero{position:relative;background:var(--sb-two);color:#fff;overflow:hidden;
 padding:clamp(46px,6vw,76px) 0 0}
.sb-hero__wave{position:absolute;inset:0;width:100%;height:100%;z-index:1;
 pointer-events:none}
.sb-hero__in{position:relative;z-index:2}
.sb-hero__top{display:flex;justify-content:space-between;align-items:center;gap:18px;
 flex-wrap:wrap;padding-bottom:clamp(28px,4vw,52px);
 border-bottom:1px solid rgba(255,255,255,.26)}
.sb-logo{display:flex;align-items:center;gap:12px;font-family:var(--sb-df);
 font-weight:800;font-size:21px;letter-spacing:.04em}
.sb-logo .sb-smile{width:30px;height:30px}
.sb-logo span{font-weight:500;opacity:.76;font-size:14px;letter-spacing:.02em}
/* правый край шапки героя приходится на мятную половину: там тёмная строка */
.sb-hero__by{font-size:13.5px;color:rgba(8,42,40,.78);text-align:right}
.sb-hero__grid{display:grid;grid-template-columns:1.08fr .92fr;
 gap:clamp(26px,4.4vw,64px);align-items:center;padding:clamp(34px,5vw,66px) 0 0}
.sb-hero .sb-kick{color:rgba(255,255,255,.7)}
.sb-hero h1{font-size:clamp(33px,5vw,64px);margin-top:16px}
.sb-hero h1 em{font-style:normal;color:var(--sb-yel)}
.sb-hero__sub{font-size:clamp(16px,1.4vw,19px);color:rgba(255,255,255,.86);max-width:52ch}
.sb-chips{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 0;padding:0;list-style:none}
.sb-chips li{font-size:13px;font-weight:600;padding:8px 14px;border-radius:999px;
 border:1px solid rgba(255,255,255,.36);color:rgba(255,255,255,.94)}
.sb-hero__cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:clamp(24px,3vw,34px)}
.sb-btn{display:inline-flex;align-items:center;gap:10px;font-family:var(--sb-df);
 font-weight:700;font-size:15px;padding:15px 26px;border-radius:999px;text-decoration:none;
 border:1.6px solid transparent;cursor:pointer;transition:transform .2s,background .2s,color .2s}
.sb-btn svg{width:19px;height:19px}
/* .sb a{color:inherit} специфичнее одиночного класса, поэтому цвет кнопок
   задаём через .sb .sb-btn--*, иначе белый текст ложится на белую плашку */
.sb .sb-btn--y{background:var(--sb-yel);color:#241a05}
.sb .sb-btn--gh{border-color:rgba(255,255,255,.52);color:#fff}
.sb-btn:hover{transform:translateY(-2px)}
.sb-btn--gh:hover{background:rgba(255,255,255,.15)}
.sb-hero__art{position:relative;aspect-ratio:1/1;display:grid;place-items:center}
.sb-hero__cover{position:relative;width:84%;
 box-shadow:0 44px 100px -44px rgba(12,8,40,.8)}
.sb-hero__cover img{display:block;width:100%;height:auto}
.sb-hero__badge{position:absolute;right:-7%;bottom:-6%;width:30%;
 filter:drop-shadow(0 18px 40px rgba(12,8,40,.5))}
/* .sb-smile задаёт знаку фиксированные 26px, в герое знак растягиваем */
.sb-hero__badge .sb-smile{width:100%;height:auto}
.sb-spec{position:relative;z-index:2;margin-top:clamp(34px,5vw,66px);
 background:var(--sb-vio-d)}
.sb-spec__in{display:grid;grid-template-columns:repeat(4,1fr);margin:0;
 width:min(1240px,100% - 40px);margin-inline:auto}
.sb-spec__in>div{padding:24px 22px 34px 0}
.sb-spec dt{font-family:var(--sb-df);font-weight:800;font-size:clamp(18px,2vw,25px)}
.sb-spec dd{margin:6px 0 0;font-size:14px;color:rgba(255,255,255,.74);max-width:24ch}

/* ── ОБЪЕКТ ── */
.sb-obj{padding:clamp(58px,8vw,106px) 0;background:#fff}
.sb-obj .sb-kick{color:var(--sb-teal)}
.sb-obj h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:22ch}
.sb-obj__lede{font-size:clamp(16px,1.35vw,18.5px);color:#333850;max-width:64ch}
.sb-obj__grid{margin-top:clamp(32px,4.4vw,54px);display:grid;
 grid-template-columns:1.05fr .95fr;gap:clamp(24px,4vw,54px);align-items:center}
.sb-facts{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:#e6e3f2}
.sb-fact{background:#fff;padding:22px 20px 24px}
.sb-fact b{display:block;font-family:var(--sb-df);font-weight:800;
 font-size:clamp(24px,2.8vw,36px);letter-spacing:-.03em;color:var(--sb-vio)}
.sb-fact span{display:block;margin-top:6px;font-size:14px;color:var(--sb-ink2);
 line-height:1.4}
.sb-obj__ph figure{margin:0}
.sb-obj__ph img{width:100%;height:auto;display:block;border-radius:16px;
 box-shadow:0 30px 70px -44px rgba(12,8,40,.55)}
.sb-obj__ph figcaption{margin-top:14px;font-size:14.5px;color:var(--sb-ink2)}
.sb-ten{margin-top:clamp(32px,4.4vw,52px)}
.sb-ten__hd{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.sb-ten__hd b{font-family:var(--sb-df);font-weight:800;font-size:clamp(28px,3.4vw,44px);
 color:var(--sb-vio);letter-spacing:-.03em}
.sb-ten__hd span{font-size:15.5px;color:var(--sb-ink2);max-width:34ch}
.sb-ten__grid{margin-top:22px;display:grid;grid-template-columns:repeat(7,1fr);gap:10px}
.sb-ten__grid div{background:var(--sb-paper);border-radius:12px;height:66px;
 display:grid;place-items:center;padding:12px}
.sb-ten__grid img{max-width:100%;max-height:34px;width:auto;height:auto;display:block;
 mix-blend-mode:multiply}

/* ── ЗАДАЧА ── */
.sb-task{padding:clamp(58px,8vw,106px) 0;background:var(--sb-vio-d);color:#fff}
.sb-task .sb-kick{color:var(--sb-acid)}
.sb-task__grid{display:grid;grid-template-columns:.86fr 1.14fr;gap:clamp(26px,5vw,62px)}
.sb-task h2{font-size:clamp(28px,3.7vw,48px);margin-top:14px}
.sb-task ul{margin:0;padding:0;list-style:none}
.sb-task li{padding:20px 0;border-top:1px solid rgba(255,255,255,.18);display:grid;
 grid-template-columns:34px 1fr;gap:16px;align-items:start}
.sb-task li:last-child{border-bottom:1px solid rgba(255,255,255,.18)}
.sb-task li p{margin:0;font-size:16.5px;color:rgba(255,255,255,.84);max-width:62ch}

/* ── ДУГА С ЦИФРАМИ ── */
.sb-arc{position:relative;padding:clamp(58px,8vw,106px) 0;background:var(--sb-two);
 color:#fff;overflow:hidden}
.sb-arc .sb-kick{color:rgba(255,255,255,.7)}
.sb-arc h2{font-size:clamp(28px,3.7vw,48px);margin-top:14px;max-width:26ch}
.sb-arc__lede{font-size:clamp(16px,1.35vw,18.5px);color:rgba(255,255,255,.84);max-width:62ch}
.sb-arc__box{margin-top:clamp(28px,4vw,46px);position:relative}
.sb-arc__svg{display:block;width:100%;height:auto}
.sb-arc__svg .line{fill:none;stroke:var(--sb-yel);stroke-width:14;stroke-linecap:round;
 stroke-dasharray:var(--len);stroke-dashoffset:var(--len);
 transition:stroke-dashoffset 1.8s cubic-bezier(.4,.5,.2,1)}
.sb-arc__box.is-in .sb-arc__svg .line{stroke-dashoffset:0}
.sb-arc__svg .dot{cursor:pointer}
.sb-arc__svg .dot circle{fill:#fff;stroke:var(--sb-yel);stroke-width:5;
 transition:fill .25s,stroke .25s,r .25s}
.sb-arc__svg .dot text{font-family:var(--sb-df);font-weight:800;
 fill:var(--sb-vio);text-anchor:middle;font-variant-numeric:tabular-nums}
.sb-arc__svg .dot .v{font-size:34px}
.sb-arc__svg .dot .u{font-size:15px;font-weight:600;fill:#5f6480}
.sb-arc__svg .dot.is-on circle{fill:var(--sb-yel);stroke:#fff}
.sb-arc__svg .dot.is-on text{fill:#241a05}
.sb-arc__svg .dot.is-on .u{fill:#4a3b0e}
.sb-arc__say{margin-top:clamp(18px,2.4vw,28px);min-height:96px;
 background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.22);
 border-radius:18px;padding:22px 24px;max-width:54ch}
.sb-arc__say b{display:block;font-family:var(--sb-df);font-weight:800;
 font-size:clamp(19px,2vw,24px)}
.sb-arc__say span{display:block;margin-top:8px;font-size:16px;
 color:rgba(255,255,255,.82)}
.sb-arc__note{margin-top:16px;font-size:14px;color:rgba(255,255,255,.62);max-width:54ch}

/* ── СТРИТ ИЛИ ТЦ ── */
.sb-two{padding:clamp(58px,8vw,106px) 0;background:var(--sb-paper)}
.sb-two .sb-kick{color:var(--sb-vio)}
.sb-two__hd{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(24px,4vw,54px);
 align-items:end}
.sb-two__hd h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:20ch}
.sb-two__hint{font-size:15px;color:var(--sb-ink2);max-width:44ch}
.sb-seg{margin-top:clamp(26px,3.4vw,42px);display:inline-grid;
 grid-template-columns:1fr 1fr;gap:6px;padding:6px;border-radius:999px;
 background:#e6e3f2}
.sb-seg button{font-family:var(--sb-df);font-weight:700;font-size:15px;
 padding:13px 28px;border-radius:999px;border:0;background:transparent;
 color:var(--sb-ink2);cursor:pointer;transition:background .25s,color .25s}
.sb-seg button.is-on{background:#fff;color:var(--sb-vio);
 box-shadow:0 6px 20px -8px rgba(12,8,40,.35)}
.sb-two__panes{margin-top:clamp(24px,3vw,38px)}
.sb-pane{display:none}
.sb-pane.is-on{display:block;animation:sb-fade .5s cubic-bezier(.2,.7,.3,1) both}
@keyframes sb-fade{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.sb-pane__top{display:flex;align-items:center;gap:16px;flex-wrap:wrap;
 padding:0 0 22px}
.sb-pane__top b{font-family:var(--sb-df);font-weight:800;font-size:clamp(22px,2.5vw,32px)}
.sb-pane__top i{font-style:normal;font-size:14.5px;color:var(--sb-ink2)}
/* минимум 200px: пять доводов встают в одну строку и в сетке нет пустой ячейки */
.sb-list{margin:0;padding:0;list-style:none;display:grid;
 grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:2px;background:#e6e3f2}
.sb-list li{background:#fff;padding:24px 22px 26px}
.sb-list b{display:block;font-family:var(--sb-df);font-weight:800;font-size:18px}
.sb-list span{display:block;margin-top:8px;font-size:15.5px;color:var(--sb-ink2)}
.sb-pane--m .sb-list li{background:linear-gradient(180deg,#fff,#f7fdfb)}
.sb-pane--m .sb-list b{color:#1c7f6f}
.sb-pane--s .sb-list b{color:var(--sb-vio)}
.sb-pane__echo{margin-top:22px;font-family:var(--sb-df);font-weight:800;
 font-size:clamp(34px,7vw,84px);letter-spacing:-.04em;line-height:.9;
 color:rgba(74,59,158,.1);text-transform:uppercase;user-select:none}

/* ── КАЛЬКУЛЯТОР ── */
.sb-calc{padding:clamp(58px,8vw,106px) 0;background:#fff}
.sb-calc .sb-kick{color:var(--sb-teal)}
.sb-calc h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:22ch}
.sb-calc__lede{font-size:clamp(16px,1.35vw,18.5px);color:#333850;max-width:64ch}
.sb-calc__box{margin-top:clamp(30px,4vw,48px);display:grid;
 grid-template-columns:.92fr 1.08fr;gap:2px;background:#e6e3f2;border-radius:20px;
 overflow:hidden;box-shadow:0 30px 70px -46px rgba(12,8,40,.5)}
.sb-calc__in{background:#fff;padding:clamp(24px,3vw,38px)}
.sb-field+.sb-field{margin-top:26px}
.sb-field>label{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
 font-size:13.5px;color:var(--sb-ink2);font-weight:600}
.sb-field>label b{font-family:var(--sb-df);font-weight:800;font-size:20px;color:var(--sb-ink)}
.sb-range{-webkit-appearance:none;appearance:none;width:100%;height:4px;margin:16px 0 0;
 border-radius:999px;background:linear-gradient(90deg,var(--sb-teal) var(--f,50%),
 #e2dcee var(--f,50%));cursor:pointer}
.sb-range::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;
 border-radius:50%;background:#fff;border:5px solid var(--sb-teal);cursor:grab;
 box-shadow:0 4px 14px rgba(0,0,0,.2)}
.sb-range::-moz-range-thumb{width:24px;height:24px;border-radius:50%;background:#fff;
 border:5px solid var(--sb-teal);cursor:grab}
.sb-range:focus-visible{outline:3px solid var(--sb-vio);outline-offset:4px}
.sb-prods{display:grid;gap:8px;margin-top:16px}
.sb-prods button{font-family:var(--sb-tf);font-size:13.5px;line-height:1.35;
 text-align:left;padding:14px 16px;border-radius:14px;border:1.6px solid #e2dcee;
 background:#fff;color:var(--sb-ink2);cursor:pointer;
 transition:border-color .2s,background .2s,color .2s}
.sb-prods button b{display:block;font-family:var(--sb-df);font-weight:800;font-size:17px;
 color:var(--sb-ink)}
.sb-prods button.is-on{border-color:var(--sb-teal);background:#f2fbfc;color:#1b6f77}
.sb-prods button.is-on b{color:#12656d}
.sb-calc__out{background:var(--sb-vio);color:#fff;padding:clamp(24px,3vw,38px);
 display:flex;flex-direction:column;justify-content:center}
.sb-outs{display:grid;grid-template-columns:1fr 1fr;gap:2px;
 background:rgba(255,255,255,.18)}
.sb-out{background:var(--sb-vio);padding:20px 18px}
.sb-out span{display:block;font-size:12.5px;letter-spacing:.06em;text-transform:uppercase;
 color:rgba(255,255,255,.6);font-weight:600}
.sb-out b{display:block;margin-top:8px;font-family:var(--sb-df);font-weight:800;
 font-size:clamp(23px,2.7vw,34px);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.sb-out--k b{color:var(--sb-yel)}
.sb-calc__note{margin-top:20px;font-size:13px;color:rgba(255,255,255,.6);max-width:56ch}

/* ── СЕКРЕТ УСПЕХА ── */
.sb-secret{padding:clamp(58px,8vw,106px) 0;background:var(--sb-paper)}
.sb-secret .sb-kick{color:var(--sb-vio)}
.sb-secret__hd{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,54px);
 align-items:end}
.sb-secret__hd h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:20ch}
.sb-secret__lede{font-size:clamp(16px,1.35vw,18.5px);color:#333850;max-width:60ch}
.sb-grid{margin-top:clamp(30px,4vw,48px);display:grid;
 grid-template-columns:repeat(4,1fr);gap:2px;background:#e6e3f2}
.sb-cell{background:#fff;padding:26px 20px 28px}
.sb-cell b{display:block;font-family:var(--sb-df);font-weight:800;
 font-size:clamp(26px,3vw,40px);letter-spacing:-.03em;color:var(--sb-vio)}
.sb-cell span{display:block;margin-top:8px;font-size:14.5px;color:var(--sb-ink2);
 line-height:1.4}
.sb-award{margin-top:2px;background:var(--sb-vio);color:#fff;padding:26px 24px;
 display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.sb-award b{font-family:var(--sb-df);font-weight:800;font-size:clamp(19px,2vw,24px);
 color:var(--sb-yel)}
.sb-award span{font-size:15.5px;color:rgba(255,255,255,.84);max-width:64ch}
.sb-shots{margin-top:clamp(26px,3.4vw,40px);display:grid;
 grid-template-columns:repeat(3,1fr);gap:clamp(12px,2vw,20px)}
.sb-shots figure{margin:0}
.sb-shots img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block;
 border-radius:14px}
.sb-shots figcaption{margin-top:10px;font-size:13.5px;color:var(--sb-ink2)}

/* ── SMILE FAMILY: ЦИФРЫ В НЕОНЕ ── */
.sb-fam{position:relative;padding:clamp(58px,8vw,106px) 0;
 background:linear-gradient(150deg,#4a3b9e 0%,#3f43a6 44%,#29b8c4 100%);
 color:#fff;overflow:hidden}
.sb-fam .sb-kick{color:rgba(255,255,255,.7)}
.sb-fam h2{font-size:clamp(28px,3.7vw,48px);margin-top:14px;max-width:24ch}
.sb-fam__lede{font-size:clamp(16px,1.35vw,18.5px);color:rgba(255,255,255,.84);max-width:64ch}
.sb-neon{margin-top:clamp(30px,4vw,48px);display:grid;
 grid-template-columns:repeat(4,1fr);gap:clamp(18px,2.6vw,32px)}
.sb-neon div b{display:block;font-family:var(--sb-df);font-weight:800;
 font-size:clamp(30px,4vw,54px);letter-spacing:-.03em;color:var(--sb-acid);
 text-shadow:0 0 26px rgba(228,240,60,.55),0 0 60px rgba(228,240,60,.3)}
.sb-neon div span{display:block;margin-top:8px;font-size:14.5px;
 color:rgba(255,255,255,.82);line-height:1.4}
.sb-says{margin-top:clamp(32px,4.4vw,56px);display:grid;
 grid-template-columns:repeat(3,1fr);gap:clamp(14px,2.2vw,24px)}
.sb-say{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);
 border-radius:18px;padding:24px 22px 26px;font-size:15.5px;
 color:rgba(255,255,255,.9);position:relative}
.sb-say::before{content:"«";position:absolute;left:16px;top:2px;
 font-family:var(--sb-df);font-weight:800;font-size:52px;
 color:rgba(255,255,255,.28);line-height:1}
.sb-say p{margin:0;padding-left:26px}
.sb-says__note{margin-top:16px;font-size:13.5px;color:rgba(255,255,255,.6)}

/* ── ЗОНЫ ОХВАТА ── */
.sb-zone{padding:clamp(58px,8vw,106px) 0;background:#fff}
.sb-zone .sb-kick{color:var(--sb-teal)}
.sb-zone h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:22ch}
.sb-zone__grid{margin-top:clamp(30px,4vw,48px);display:grid;
 grid-template-columns:1.05fr .95fr;gap:clamp(24px,4.4vw,58px);align-items:center}
.sb-map{position:relative;border-radius:20px;overflow:hidden;
 box-shadow:0 30px 70px -44px rgba(12,8,40,.55)}
.sb-map img{display:block;width:100%;height:auto}
.sb-map svg{position:absolute;inset:0;width:100%;height:100%}
.sb-map .z{fill:rgba(255,255,255,.16);stroke:#fff;stroke-width:.5;
 stroke-dasharray:3 2;opacity:0;transition:opacity .45s}
.sb-map .z.is-on{opacity:1}
.sb-map .z2{fill:rgba(74,59,158,.16);stroke:#4a3b9e;stroke-width:.7;
 stroke-dasharray:2 1.4}
.sb-map .pin{fill:var(--sb-vio);stroke:#fff;stroke-width:1}
.sb-zone__tabs{display:grid;gap:8px}
.sb-ztab{text-align:left;padding:20px 22px;border-radius:16px;border:1.6px solid #e2dcee;
 background:#fff;cursor:pointer;transition:border-color .22s,background .22s;
 display:grid;grid-template-columns:auto 1fr;gap:4px 16px;align-items:baseline}
.sb-ztab b{font-family:var(--sb-df);font-weight:800;font-size:clamp(24px,2.8vw,34px);
 letter-spacing:-.03em;color:var(--sb-vio);font-variant-numeric:tabular-nums}
.sb-ztab i{font-style:normal;font-family:var(--sb-df);font-weight:700;font-size:13px;
 letter-spacing:.1em;text-transform:uppercase;color:var(--sb-teal)}
.sb-ztab span{grid-column:1/-1;font-size:15px;color:var(--sb-ink2)}
.sb-ztab.is-on{border-color:var(--sb-teal);background:#f2fbfc}
.sb-zone__addr{margin-top:22px;padding-top:22px;border-top:1px solid #e6e3f2;
 font-size:15.5px;color:var(--sb-ink2)}
.sb-zone__addr b{display:block;font-family:var(--sb-df);font-weight:800;font-size:18px;
 color:var(--sb-ink)}

/* ── ЛИСТАЛКА РАЗВОРОТОВ ── */
.sb-book{background:var(--sb-paper);padding:clamp(58px,8vw,106px) 0;overflow:hidden}
.sb-book .sb-kick{color:var(--sb-vio)}
.sb-book__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:22px;
 flex-wrap:wrap;padding-bottom:clamp(24px,3.2vw,40px)}
.sb-book__hd h2{font-size:clamp(28px,3.8vw,50px);margin-top:12px}
.sb-book__hint{font-size:14.5px;color:var(--sb-ink2);max-width:34ch}
.sb-track{display:flex;gap:clamp(14px,2vw,26px);overflow-x:auto;
 scroll-snap-type:x mandatory;scrollbar-width:none;-ms-overflow-style:none;
 scroll-behavior:smooth}
.sb-track::-webkit-scrollbar{display:none}
.sb-slide{flex:0 0 100%;scroll-snap-align:center;margin:0}
.sb-slide__ph{position:relative;background:#e9e5f4;cursor:zoom-in;overflow:hidden;
 border-radius:14px}
/* height:auto обязателен: атрибут height у <img> это презентационный хинт, и без
   сброса он перебивает aspect-ratio, а разворот показывается обрезанным по центру */
.sb-slide__ph img{width:100%;height:auto;aspect-ratio:2/1;object-fit:cover;display:block}
.sb-slide__ph::after{content:"";position:absolute;top:0;bottom:0;left:50%;width:2px;
 background:linear-gradient(180deg,rgba(0,0,0,.16),rgba(0,0,0,.04));pointer-events:none}
.sb-slide__pg{position:absolute;left:14px;bottom:14px;z-index:2;background:var(--sb-vio);
 color:#fff;font-family:var(--sb-df);font-weight:700;font-size:11.5px;
 letter-spacing:.1em;text-transform:uppercase;padding:7px 13px;border-radius:999px}
.sb-slide__ch{position:absolute;right:14px;bottom:14px;z-index:2;
 background:rgba(24,26,44,.72);color:#fff;font-size:11px;font-weight:600;
 letter-spacing:.08em;text-transform:uppercase;padding:7px 13px;border-radius:999px;
 backdrop-filter:blur(6px)}
.sb-slide__zoom{position:absolute;right:14px;top:14px;z-index:2;
 background:rgba(24,26,44,.72);color:#fff;font-size:12px;font-weight:600;
 padding:7px 13px;border-radius:999px;backdrop-filter:blur(6px);opacity:0;
 transition:opacity .25s}
.sb-slide__ph:hover .sb-slide__zoom{opacity:1}
.sb-slide figcaption{padding:24px 2px 0;display:grid;grid-template-columns:.6fr 1.4fr;
 gap:clamp(14px,3vw,40px);align-items:start;min-height:150px}
.sb-slide figcaption h3{font-size:clamp(20px,2.1vw,27px)}
.sb-slide figcaption p{margin:0;font-size:15.5px;color:var(--sb-ink2);max-width:64ch}
.sb-nav{margin-top:clamp(18px,2.4vw,28px);display:flex;align-items:center;
 justify-content:space-between;gap:18px;flex-wrap:wrap}
.sb-nav__btns{display:flex;align-items:center;gap:10px}
.sb-arrow{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;
 background:#fff;border:1.6px solid #ddd7ea;color:var(--sb-ink);cursor:pointer;
 transition:background .2s,border-color .2s,color .2s,opacity .2s}
.sb-arrow svg{width:20px;height:20px}
.sb-arrow--next svg{transform:rotate(180deg)}
.sb-arrow:hover{background:var(--sb-vio);border-color:var(--sb-vio);color:#fff}
.sb-arrow[disabled]{opacity:.3;cursor:default}
.sb-arrow[disabled]:hover{background:#fff;border-color:#ddd7ea;color:var(--sb-ink)}
.sb-count{font-family:var(--sb-df);font-weight:700;font-size:16px;letter-spacing:.06em;
 color:var(--sb-ink2);min-width:5.5em;font-variant-numeric:tabular-nums}
.sb-count b{color:var(--sb-vio);font-weight:800}
.sb-thumbs{display:flex;gap:7px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.sb-thumbs::-webkit-scrollbar{display:none}
.sb-thumb{flex:0 0 auto;width:74px;padding:0;border:0;background:none;cursor:pointer;
 opacity:.42;transition:opacity .22s,outline-color .22s;outline:2px solid transparent;
 outline-offset:2px;border-radius:4px}
.sb-thumb img{width:100%;height:auto;aspect-ratio:2/1;object-fit:cover;display:block;
 border-radius:4px}
.sb-thumb:hover{opacity:.78}
.sb-thumb.is-on{opacity:1;outline-color:var(--sb-vio)}
.sb-covers{margin-top:clamp(30px,4vw,48px);display:grid;grid-template-columns:1fr 1fr;
 gap:clamp(14px,2.4vw,28px)}
.sb-covers figure{margin:0}
.sb-covers img{width:100%;height:auto;display:block;border-radius:14px;
 box-shadow:0 24px 60px -40px rgba(12,8,40,.5)}
.sb-covers figcaption{margin-top:12px;font-size:14px;color:var(--sb-ink2)}

/* ── ПРИЁМЫ ── */
.sb-craft{padding:clamp(58px,8vw,106px) 0;background:#fff}
.sb-craft .sb-kick{color:var(--sb-teal)}
.sb-craft h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:22ch}
.sb-craft__lede{font-size:clamp(16px,1.35vw,18.5px);color:#333850;max-width:64ch}
.sb-craft__grid{margin-top:clamp(30px,4vw,48px);display:grid;
 grid-template-columns:repeat(3,1fr);gap:clamp(16px,2.4vw,28px)}
.sb-craft__grid figure{margin:0}
.sb-craft__grid img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;
 display:block;border-radius:14px}
.sb-craft__grid h3{margin-top:16px;font-size:19px}
.sb-craft__grid figcaption{margin-top:8px;font-size:14.5px;color:var(--sb-ink2)}
.sb-pal{margin-top:clamp(28px,3.6vw,44px);display:grid;
 grid-template-columns:repeat(5,1fr);gap:2px}
.sb-sw{padding:44px 12px 14px;color:#fff}
.sb-sw span{display:block;font-family:var(--sb-df);font-weight:700;font-size:13px}
.sb-sw small{font-size:11.5px;opacity:.8;font-variant-numeric:tabular-nums}
.sb-sw--v{background:var(--sb-vio)}
.sb-sw--m{background:var(--sb-mint);color:#0b2b26}
.sb-sw--t{background:var(--sb-teal)}
.sb-sw--y{background:var(--sb-yel);color:#241a05}
.sb-sw--a{background:var(--sb-acid);color:#242a05}

/* ── РЕЗУЛЬТАТ ── */
.sb-res{padding:clamp(58px,8vw,106px) 0;background:var(--sb-paper)}
.sb-res__grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(26px,5vw,62px)}
.sb-res .sb-kick{color:var(--sb-vio)}
.sb-res h2{font-size:clamp(28px,3.7vw,48px);margin-top:14px}
.sb-res__more{font-size:15px;color:var(--sb-ink2);margin-top:22px}
.sb-res__more a{color:var(--sb-vio);font-weight:600}
.sb-res__list{margin:0;padding:0;list-style:none}
.sb-res__list li{display:grid;grid-template-columns:74px 1fr;gap:18px;align-items:start;
 padding:22px 0;border-top:1px solid #e2dcee}
.sb-res__list li:last-child{border-bottom:1px solid #e2dcee}
.sb-res__list span:first-child{font-family:var(--sb-df);font-weight:800;
 font-size:clamp(32px,3.6vw,46px);line-height:.9;color:var(--sb-vio)}
.sb-res__list span:last-child{font-size:16.5px;color:#333850}

/* ── ЛАЙТБОКС ── */
.sb-lb{position:fixed;inset:0;z-index:9999;background:rgba(10,8,26,.95);display:none;
 padding:clamp(16px,4vw,48px);overflow:auto}
.sb-lb.is-open{display:grid;place-items:center}
.sb-lb__box{position:relative;max-width:1400px;width:100%}
.sb-lb__box img{width:100%;height:auto;display:block;border-radius:10px}
.sb-lb__x{position:absolute;right:0;top:-44px;width:36px;height:36px;border-radius:50%;
 border:1.6px solid rgba(255,255,255,.4);background:none;color:#fff;font-size:22px;
 line-height:1;cursor:pointer}
.sb-lb__cap{margin-top:14px;font-size:14px;color:rgba(255,255,255,.74);text-align:center}

@media(max-width:1000px){
 /* на телефоне лист режется поперёк: текст на фиолетовой части, обложка на мятной.
    Мяту здесь берём глубже: в одну колонку на неё попадают и строки текста,
    а белое по светлой мяте не вычитывается */
 :root{--sb-two:linear-gradient(196deg,#4a3b9e 0%,#4a3b9e 58%,#23808f 58%,#1b7f7c 100%)}
 .sb-hero__grid,.sb-task__grid,.sb-obj__grid,.sb-calc__box,.sb-res__grid,
 .sb-two__hd,.sb-secret__hd,.sb-zone__grid{grid-template-columns:1fr}
 .sb-list{grid-template-columns:1fr 1fr}
 .sb-hero__by{text-align:left;color:rgba(255,255,255,.78)}
 .sb-hero__art{max-width:520px}
 .sb-spec__in{grid-template-columns:1fr 1fr}
 .sb-grid,.sb-neon{grid-template-columns:1fr 1fr}
 .sb-ten__grid{grid-template-columns:repeat(4,1fr)}
 .sb-says,.sb-craft__grid,.sb-shots{grid-template-columns:1fr 1fr}
 .sb-slide figcaption{grid-template-columns:1fr;min-height:0}
}
@media(max-width:680px){
 .sb{font-size:16px}
 .sb-facts,.sb-outs,.sb-says,.sb-craft__grid,.sb-shots,.sb-covers{grid-template-columns:1fr}
 .sb-grid,.sb-neon{grid-template-columns:1fr 1fr;gap:2px}
 .sb-ten__grid{grid-template-columns:repeat(3,1fr)}
 .sb-pal{grid-template-columns:repeat(3,1fr)}
 .sb-sw{padding:34px 10px 12px}
 .sb-seg{display:grid;grid-template-columns:1fr;border-radius:22px}
 .sb-seg button{border-radius:18px}
 .sb-thumbs{order:3;width:100%}
 .sb-slide__ch{display:none}
 .sb-lb__x{top:-38px}
 .sb-arc__box{overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
 .sb-arc__box::-webkit-scrollbar{display:none}
 .sb-arc__svg{width:760px}
}
@media(prefers-reduced-motion:reduce){
 .sb-r{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .sb *{transition-duration:.01ms!important;scroll-behavior:auto;animation:none!important}
 .sb-track{scroll-behavior:auto}
 .sb-arc__svg .line{stroke-dashoffset:0!important}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Брошюра ТЦ «Смайл» для Becar: 22 полосы про инвестиции в торговую недвижимость | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: печатная брошюра действующего торгового центра «Смайл» в Санкт-Петербурге для Becar Asset Management. 22 полосы, 10 разворотов, квадрат 210×210 мм. Концепция, копирайтинг, инфографика, вёрстка и препресс: издание объясняет частному инвестору формат кондо-ТЦ и доходность лота до 13% годовых.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Брошюра ТЦ «Смайл» для Becar Asset Management | кейс Hand Marketing">
<meta property="og:description" content="22 полосы про доход с торговых метров: формат кондо-ТЦ, цифры действующего ТЦ у метро Дыбенко и три доходных продукта группы Becar.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/cover.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''

# Дуга на фоне героя: поднимается из-под обложки к правому краю, как на полосе 6-7.
# Держим её правее текстовой колонки, иначе жёлтая линия проходит по строкам.
HERO_WAVE = (
  '<svg class="sb-hero__wave" viewBox="0 0 1200 700" preserveAspectRatio="none" '
  'aria-hidden="true" fill="none">'
  '<path d="M600 660 C860 660 1000 600 1300 240" '
  'stroke="#ffc324" stroke-width="26" stroke-linecap="round" opacity=".92"/>'
  '<path d="M600 596 C860 596 1000 536 1300 176" '
  'stroke="#ffffff" stroke-width="2" opacity=".22"/>'
  '</svg>')


def hero():
    spec = [('22 полосы', 'обложка, десять разворотов и задник'),
            ('210×210 мм', 'квадрат, полноцвет'),
            ('2020 год', 'издание к продаже лотов'),
            ('Becar', 'Asset Management Group')]
    cells = ''.join(f'<div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in spec)
    return (
      '<header class="sb-hero">' + HERO_WAVE +
      '<div class="sb-w sb-hero__in">'
      '<div class="sb-hero__top">'
      f'<span class="sb-logo">{smile_svg(blink=True)}СМАЙЛ<span>торговый центр</span></span>'
      '<span class="sb-hero__by">Becar Asset Management, Петербург, '
      'пр. Большевиков, 27 лит. А</span>'
      '</div>'
      '<div class="sb-hero__grid">'
      '<div>'
      '<span class="sb-kick">Полиграфия и копирайтинг</span>'
      '<h1>Брошюра, которая продаёт <em>метры</em> в действующем ТЦ</h1>'
      '<p class="sb-hero__sub">Becar Asset Management продавал частным инвесторам '
      'лоты в торговом центре «Смайл» у метро Дыбенко. Мы собрали издание на '
      '22 полосы: незнакомый формат кондо-ТЦ, цифры работающего объекта '
      'и три доходных продукта группы.</p>'
      '<ul class="sb-chips"><li>Концепция издания</li><li>Копирайтинг</li>'
      '<li>Инфографика</li><li>Вёрстка</li><li>Препресс</li></ul>'
      '<div class="sb-hero__cta">'
      f'<a class="sb-btn sb-btn--y" href="#sb-book">Листать развороты {ARROW}</a>'
      '<a class="sb-btn sb-btn--gh" href="#sb-calc">Посчитать доход</a>'
      '</div></div>'
      '<div class="sb-hero__art">'
      '<div class="sb-hero__cover">'
      f'<img src="{IMG}/cover.jpg" width="1200" height="1197" '
      'alt="Обложка брошюры ТЦ «Смайл»: жёлтый логотип на фиолетовом, '
      '15 000 кв. м, приносящих стабильный доход" fetchpriority="high">'
      f'<div class="sb-hero__badge">{smile_svg(blink=True)}</div>'
      '</div></div>'
      '</div></div>'
      f'<div class="sb-spec"><dl class="sb-spec__in">{cells}</dl></div>'
      '</header>')


def obj():
    facts = [('15 000', 'кв. м, приносящих стабильный доход'),
             ('100%', 'заполняемость на момент выпуска издания'),
             ('60', 'арендаторов сегмента эконом'),
             ('7160', 'посетителей в сутки'),
             ('3', 'этажа с якорными арендаторами'),
             ('до 13%', 'годовых доходность лота')]
    cells = ''.join(f'<div class="sb-fact"><b>{v}</b><span>{t}</span></div>'
                    for v, t in facts)
    logos = ''.join(
      f'<div><img src="{TEN}/{f}.png" width="200" height="48" alt="Логотип {n}" '
      'loading="lazy"></div>' for f, n in TENANTS)
    return (
      '<section class="sb-obj"><div class="sb-w">'
      '<div class="sb-r"><span class="sb-kick">Объект</span>'
      '<h2>Не стройка, а работающий торговый центр</h2>'
      '<p class="sb-obj__lede">«Смайл» это многофункциональный семейный торговый '
      'центр с социальным фокусом на первой линии у метро Дыбенко. К 2020 году '
      'объект уже семь лет был под управлением Becar Asset Management и приносил '
      'доход, поэтому у издания была редкая для инвестиционной брошюры возможность: '
      'говорить фактами, а не обещаниями.</p></div>'
      '<div class="sb-obj__grid">'
      f'<div class="sb-facts sb-r">{cells}</div>'
      '<div class="sb-obj__ph sb-r"><figure>'
      f'<img src="{IMG}/ph-facade.jpg" width="712" height="410" '
      'alt="Фасад торгового центра «Смайл» с вывесками арендаторов и парковкой" '
      'loading="lazy">'
      '<figcaption>Фотографии объекта в брошюре стоят внизу полосы узкой лентой: '
      'они подтверждают цифры и не спорят с ними за внимание.</figcaption>'
      '</figure></div>'
      '</div>'
      '<div class="sb-ten sb-r">'
      '<div class="sb-ten__hd"><b>80%</b>'
      '<span>площадей заняты сетевыми арендаторами, и в брошюре это доказано '
      'логотипами, а не словами</span></div>'
      f'<div class="sb-ten__grid">{logos}</div>'
      '</div>'
      '</div></section>')


def task():
    items = [
      'Объяснить частному инвестору незнакомый формат. Кондо-ТЦ конкурирует '
      'не с другими торговыми центрами, а с привычным стрит-ритейлом.',
      'Показать, что объект действующий. Заполняемость, посещаемость и пул '
      'арендаторов работают лучше любого рендера.',
      'Свести доход к трём понятным цифрам: порог входа, ставка, срок. '
      'Без таблиц и сносок мелким кеглем.',
      'Сделать издание для встречи. У менеджера на каждый вопрос инвестора '
      'должен быть свой разворот.',
    ]
    lis = ''.join(f'<li>{smile_svg()}<p>{t}</p></li>' for t in items)
    return (
      '<section class="sb-task"><div class="sb-w sb-task__grid">'
      '<div class="sb-r"><span class="sb-kick">Задача</span>'
      '<h2>Продать метры тому, кто искал стрит-ритейл</h2></div>'
      f'<ul class="sb-r">{lis}</ul>'
      '</div></section>')


def arc():
    w, h = ARC_VB
    dots = ''
    for i, ((x, y), (v, u, label, note)) in enumerate(zip(ARC_PTS, ARC)):
        dots += (
          f'<g class="sb-dot dot{" is-on" if i == 0 else ""}" id="sb-dot-{i}" '
          f'data-i="{i}" role="button" tabindex="0" '
          f'aria-label="{label}">'
          f'<circle cx="{x:.0f}" cy="{y:.0f}" r="58"/>'
          f'<text class="v" x="{x:.0f}" y="{y + 4:.0f}">{v}</text>'
          f'<text class="u" x="{x:.0f}" y="{y + 28:.0f}">{u}</text>'
          '</g>')
    # длина дуги для прочерчивания: считаем по сэмплам, точнее хардкода
    pts = [arc_point(k / 240) for k in range(241)]
    ln = sum(math.dist(pts[k], pts[k + 1]) for k in range(240))
    return (
      '<section class="sb-arc"><div class="sb-w">'
      '<div class="sb-r" style="max-width:62ch">'
      '<span class="sb-kick">Живой блок, разворот 6-7</span>'
      '<h2>Жёлтая дуга сшивает две половины</h2>'
      '<p class="sb-arc__lede">Лист брошюры всегда поделён на две зоны. Мятная это '
      'район, люди и эмоция, фиолетовая это деньги и инвестор. Единственное, что '
      'их связывает, жёлтая дуга, и на неё нанизаны цифры объекта. Так разворот '
      'читается за один взгляд: линия сама ведёт от площади к доходности.</p></div>'
      '<div class="sb-arc__box sb-r" id="sb-arc">'
      f'<svg class="sb-arc__svg" viewBox="-70 -24 {w + 140} {h + 60}" role="group" '
      'aria-label="Цифры объекта на дуге">'
      f'<path class="line" d="{ARC_D}" style="--len:{ln:.0f}"/>{dots}</svg>'
      '</div>'
      '<div class="sb-arc__say" id="sb-arc-say" aria-live="polite">'
      f'<b>{ARC[0][2]}</b><span>{ARC[0][3]}</span></div>'
      '<p class="sb-arc__note">Наведите на цифру, коснитесь её или откройте с клавиатуры: '
      'подпись меняется так же, как менялся текст рядом с кружком на полосе.</p>'
      '</div></section>')


def two():
    def pane(code, cls, title, note, rows, echo):
        lis = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in rows)
        return (f'<div class="sb-pane sb-pane--{cls}{" is-on" if code == "street" else ""}" '
                f'id="sb-pane-{code}">'
                f'<div class="sb-pane__top"><b>{title}</b><i>{note}</i></div>'
                f'<ul class="sb-list">{lis}</ul>'
                f'<div class="sb-pane__echo" aria-hidden="true">{echo}</div>'
                '</div>')
    return (
      '<section class="sb-two"><div class="sb-w">'
      '<div class="sb-two__hd sb-r">'
      '<div><span class="sb-kick">Живой блок, разворот 2-3</span>'
      '<h2>Стрит-ритейл или торговый центр</h2></div>'
      '<p class="sb-two__hint">Первый разворот издания это спор с ожиданием '
      'инвестора. Мы не хвалим объект, а разбираем формат, который инвестор '
      'считал безопасным.</p></div>'
      '<div class="sb-seg sb-r" id="sb-seg" role="group" aria-label="Выбор формата">'
      '<button type="button" class="is-on" data-pane="street" aria-pressed="true">'
      'Стрит-ритейл</button>'
      '<button type="button" data-pane="mall" aria-pressed="false">Кондо-ТЦ</button>'
      '</div>'
      '<div class="sb-two__panes sb-r">'
      + pane('street', 's', 'Самый частый запрос частного инвестора',
             'но пять доводов против', STREET, 'Один арендатор')
      + pane('mall', 'm', 'Синергия вместо одного арендатора',
             'и три гарантии дохода', MALL, 'Синергия')
      + '</div></div></section>')


def calc():
    prods = ''.join(
      f'<button type="button" class="{"is-on" if i == 0 else ""}" data-rate="{r}" '
      f'aria-pressed="{"true" if i == 0 else "false"}">'
      f'<b>{name}, {label} годовых</b>{note}</button>'
      for i, (code, name, label, r, note) in enumerate(PRODUCTS))
    return (
      '<section class="sb-calc" id="sb-calc"><div class="sb-w">'
      '<div class="sb-r"><span class="sb-kick">Живой блок</span>'
      '<h2>Доход по цифрам издания</h2>'
      '<p class="sb-calc__lede">В брошюре доходность заявлена коротко: лоты '
      'от 2 млн рублей, до 13% годовых, платежи ежемесячно. Тем же способом '
      'в конце издания показаны два соседних продукта группы, поэтому '
      'калькулятор считает по всем трём.</p></div>'
      '<div class="sb-calc__box sb-r">'
      '<div class="sb-calc__in">'
      '<div class="sb-field">'
      '<label for="sb-sum">Стоимость лота, млн рублей <b id="sb-sum-v">2,0</b></label>'
      '<input class="sb-range" type="range" id="sb-sum" min="2" max="20" step="0.5" '
      'value="2"></div>'
      '<div class="sb-field">'
      '<label for="sb-years">Срок владения, лет <b id="sb-years-v">5</b></label>'
      '<input class="sb-range" type="range" id="sb-years" min="1" max="10" step="1" '
      'value="5"></div>'
      f'<div class="sb-prods" id="sb-prods" role="group" '
      f'aria-label="Доходный продукт">{prods}</div>'
      '</div>'
      '<div class="sb-calc__out">'
      '<div class="sb-outs">'
      '<div class="sb-out"><span>В месяц</span><b id="sb-o-month">21 667 ₽</b></div>'
      '<div class="sb-out"><span>В год</span><b id="sb-o-year">260 000 ₽</b></div>'
      '<div class="sb-out sb-out--k"><span>За срок владения</span>'
      '<b id="sb-o-total">1,30 млн ₽</b></div>'
      '<div class="sb-out"><span>Лот плюс доход</span>'
      '<b id="sb-o-sum">3,30 млн ₽</b></div>'
      '</div>'
      '<p class="sb-calc__note">Расчёт линейный, по ставке из брошюры 2020 года: '
      'реинвестирование, налоги и рост стоимости актива не учтены. Блок '
      'показывает логику издания, а не инвестиционное предложение.</p>'
      '</div></div></div></section>')


def secret():
    cells = ''.join(f'<div class="sb-cell"><b>{v}</b><span>{t}</span></div>'
                    for v, t in SECRET)
    shots = [
      ('ph-familia.jpg', 'Вход в Familia на втором этаже: сетевой арендатор '
       'как якорь для целого уровня'),
      ('ph-kidster.jpg', 'Kidster с товарами для мам: пул подобран под '
       'семейную аудиторию района'),
      ('ph-facade.jpg', 'Фасад с вывесками: состав арендаторов виден '
       'ещё с парковки'),
    ]
    figs = ''.join(
      f'<figure><img src="{IMG}/{f}" width="712" height="400" alt="{c}" '
      f'loading="lazy"><figcaption>{c}</figcaption></figure>' for f, c in shots)
    return (
      '<section class="sb-secret"><div class="sb-w">'
      '<div class="sb-secret__hd sb-r">'
      '<div><span class="sb-kick">Разворот 10-11</span>'
      '<h2>Семь лет управления в девяти цифрах</h2></div>'
      '<p class="sb-secret__lede">Самый сильный аргумент издания принадлежит не '
      'объекту, а управляющей компании. За семь лет команда Becar сделала из '
      'неприметного полупустого объекта центр притяжения района, и разворот '
      'показывает это только цифрами роста.</p></div>'
      f'<div class="sb-grid sb-r">{cells}</div>'
      '<div class="sb-award sb-r"><b>RCSC Awards 2017</b>'
      '<span>ТЦ «Смайл» финалист номинации «Действующий ТЦ» в категории '
      '«Малый ТЦ». В брошюре награда стоит последней в столбце цифр, как '
      'внешнее подтверждение всего предыдущего.</span></div>'
      f'<div class="sb-shots sb-r">{figs}</div>'
      '</div></section>')


def family():
    cells = ''.join(f'<div><b>{v}</b><span>{t}</span></div>' for v, t in FAMILY)
    says = ''.join(f'<div class="sb-say"><p>{s}</p></div>' for s in SAYS)
    return (
      '<section class="sb-fam"><div class="sb-w">'
      '<div class="sb-r" style="max-width:64ch">'
      '<span class="sb-kick">Разворот 12-13</span>'
      '<h2>Smile Family: промо, которое держит посещаемость</h2>'
      '<p class="sb-fam__lede">Программа продвижения вынесена в отдельный разворот, '
      'потому что она и объясняет цифры трафика. Добрососедские отношения с районом '
      'строятся детским клубом, бесплатными мастер-классами, экологическими акциями '
      'и уличными праздниками. На полосе цифры набраны жёлтым в неоновом свечении: '
      'единственное место в издании, где графика позволяет себе громкость.</p></div>'
      f'<div class="sb-neon sb-r">{cells}</div>'
      f'<div class="sb-says sb-r">{says}</div>'
      '<p class="sb-says__note">Отзывы жителей района напечатаны в брошюре '
      'без редактуры, поэтому и здесь оставлены почти дословно.</p>'
      '</div></section>')


def zones():
    tabs = ''
    for i, (code, name, num, note, _) in enumerate(ZONES):
        tabs += (f'<button type="button" class="sb-ztab{" is-on" if i == 0 else ""}" '
                 f'data-z="{code}" aria-pressed="{"true" if i == 0 else "false"}">'
                 f'<b>{num}</b><i>{name}</i><span>{note}</span></button>')
    x, y = MAP_X * 100, MAP_Y * 100
    return (
      '<section class="sb-zone"><div class="sb-w">'
      '<div class="sb-r" style="max-width:60ch">'
      '<span class="sb-kick">Живой блок, разворот 14-15</span>'
      '<h2>Зона охвата нарисована, а не описана</h2>'
      '<p class="sb-obj__lede">Карта на полосе сделана в цветах издания: жёлтые '
      'улицы, фиолетовая Нева, объект точкой у метро Дыбенко. Фон залит '
      'повторяющейся подписью «зона охвата», поэтому границы читаются без легенды. '
      'Переключите зону, чтобы увидеть, из чего складываются 133 000 покупателей.</p>'
      '</div>'
      '<div class="sb-zone__grid">'
      '<div class="sb-map sb-r">'
      f'<img src="{IMG}/map.jpg" width="1100" height="1101" '
      'alt="Карта района у метро Дыбенко из брошюры ТЦ «Смайл»: жёлтые улицы, '
      'фиолетовая Нева, объект отмечен точкой" loading="lazy">'
      '<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
      f'<circle class="z z2 is-on" id="sb-z-2" cx="{x:.1f}" cy="{y:.1f}" '
      f'r="{R_SECOND * 100:.1f}"/>'
      f'<circle class="z z1 is-on" id="sb-z-1" cx="{x:.1f}" cy="{y:.1f}" '
      f'r="{R_FIRST * 100:.1f}"/>'
      f'<circle class="pin" cx="{x:.1f}" cy="{y:.1f}" r="1.6"/>'
      '</svg></div>'
      '<div>'
      f'<div class="sb-zone__tabs sb-r" id="sb-zones" role="group" '
      f'aria-label="Зоны охвата">{tabs}</div>'
      '<div class="sb-zone__addr sb-r"><b>Санкт-Петербург, пр. Большевиков, '
      '27 лит. А</b>Метро Дыбенко, первая линия. Адрес и два телефона отделов '
      'продаж стоят на задней обложке издания, и это вся контактная информация '
      'в брошюре.</div>'
      '</div></div></div></section>')


def book():
    slides, thumbs = '', ''
    total = len(SPREADS)
    for i, (pages, chap, title, text, alt) in enumerate(SPREADS, start=1):
        src = f'{IMG}/spread-{i:02d}.jpg'
        slides += (
          f'<figure class="sb-slide" data-i="{i}">'
          f'<div class="sb-slide__ph sb-zoom" role="button" tabindex="0" data-src="{src}" '
          f'data-cap="Полосы {pages}. {title}">'
          f'<img src="{src}" width="2400" height="1201" alt="{alt}" loading="lazy">'
          f'<span class="sb-slide__pg">Полосы {pages}</span>'
          f'<span class="sb-slide__ch">{chap}</span>'
          '<span class="sb-slide__zoom">Открыть крупно</span></div>'
          f'<figcaption><h3>{title}</h3><p>{text}</p></figcaption></figure>')
        thumbs += (
          f'<button class="sb-thumb{" is-on" if i == 1 else ""}" data-go="{i}" '
          f'type="button" aria-label="Развороты {pages}">'
          f'<img src="{IMG}/thumb-{i:02d}.jpg" width="240" height="120" alt="" '
          'loading="lazy"></button>')
    return (
      '<section class="sb-book" id="sb-book"><div class="sb-w">'
      '<div class="sb-book__hd sb-r"><div><span class="sb-kick">Развороты</span>'
      '<h2>Десять разворотов подряд</h2></div>'
      '<p class="sb-book__hint">Издание квадратное, развороты открываются '
      'широкими: листайте стрелками, миниатюрами или свайпом.</p></div>'
      f'<div class="sb-track" id="sb-track" tabindex="0" role="group" '
      f'aria-label="Развороты брошюры">{slides}</div>'
      '<div class="sb-nav"><div class="sb-nav__btns">'
      f'<button class="sb-arrow sb-arrow--prev" id="sb-prev" type="button" '
      f'aria-label="Предыдущий разворот">{CHEV}</button>'
      f'<button class="sb-arrow sb-arrow--next" id="sb-next" type="button" '
      f'aria-label="Следующий разворот">{CHEV}</button>'
      f'<span class="sb-count" id="sb-count"><b>01</b> / {total:02d}</span></div>'
      f'<div class="sb-thumbs" id="sb-thumbs">{thumbs}</div>'
      '</div>'
      '<div class="sb-covers sb-r">'
      '<figure><img src="' + IMG + '/cover.jpg" width="1200" height="1197" '
      'alt="Обложка брошюры ТЦ «Смайл»: жёлтый логотип со свечением на фиолетовом '
      'и 15 000 кв. м" loading="lazy">'
      '<figcaption>Обложка: логотип со свечением, обещание доступных инвестиций '
      'и одна цифра площади. Ни фотографии объекта, ни плана.</figcaption></figure>'
      '<figure><img src="' + IMG + '/back.jpg" width="1200" height="1197" '
      'alt="Задняя обложка брошюры ТЦ «Смайл»: адрес объекта и телефоны отделов '
      'продаж в Москве и Петербурге" loading="lazy">'
      '<figcaption>Задник: адрес объекта, два телефона и мятные линейки, '
      'которые повторяют деление листа на две половины.</figcaption></figure>'
      '</div></div></section>')


def craft():
    figs = [
      ('craft-arc.jpg', 'Дуга и контурный логотип',
       'На мятной половине логотип набран контуром, а дуга уходит на фиолетовую '
       'половину и меняет цвет на жёлтый. Смайл в круге сидит прямо на линии.',
       'Полоса брошюры: контурный логотип СМАЙЛ на мятном фоне, дуга и смайл в круге'),
      ('craft-echo.jpg', 'Текст-эхо во всю полосу',
       'Ключевое слово разворота набирается кеглем во всю полосу и уходит '
       'в фон почти без контраста. Читается сначала смысл, потом слово.',
       'Полоса брошюры: слово СИНЕРГИЯ набрано во всю полосу как фоновое эхо'),
      ('craft-neon.jpg', 'Цифры в неоне',
       'Жёлтые цифры на фиолетовом получают свечение, и разворот про промо '
       'звучит громче остальных, не меняя ни шрифта, ни сетки.',
       'Полоса брошюры: жёлтые цифры промо в неоновом свечении на фиолетовом фоне'),
    ]
    cards = ''.join(
      f'<figure><img src="{IMG}/{f}" width="1100" height="825" alt="{alt}" '
      f'loading="lazy"><h3>{t}</h3><figcaption>{c}</figcaption></figure>'
      for f, t, c, alt in figs)
    return (
      '<section class="sb-craft"><div class="sb-w">'
      '<div class="sb-r"><span class="sb-kick">Графика</span>'
      '<h2>Три приёма держат все 22 полосы</h2>'
      '<p class="sb-craft__lede">Издание собрано на минимуме средств: два цвета '
      'фона, жёлтая линия и один знак. За счёт этого брошюру можно было продолжать '
      'новыми полосами, не переверстывая старые, и переносить графику в баннеры '
      'и на посадочную страницу объекта.</p></div>'
      f'<div class="sb-craft__grid sb-r">{cards}</div>'
      '<div class="sb-pal sb-r">'
      '<div class="sb-sw sb-sw--v"><span>Фиолетовый</span><small>#4A3B9E</small></div>'
      '<div class="sb-sw sb-sw--m"><span>Мята</span><small>#5FC1A8</small></div>'
      '<div class="sb-sw sb-sw--t"><span>Бирюза</span><small>#29B8C4</small></div>'
      '<div class="sb-sw sb-sw--y"><span>Жёлтый</span><small>#FFC324</small></div>'
      '<div class="sb-sw sb-sw--a"><span>Кислотный</span><small>#E4F03C</small></div>'
      '</div></div></section>')


def result():
    items = [
      ('22', 'Готовое издание на <b>22 полосы</b> с препрессом: концепция, тексты, '
       'инфографика, вёрстка, файл для типографии.'),
      ('2', '<b>Две половины листа</b> вместо двух брошюр. Район и деньги живут '
       'в одном издании и не спорят за внимание инвестора.'),
      ('13', '<b>Доходность до 13% годовых</b> объяснена без таблиц: цифры нанизаны '
       'на дугу и читаются за один взгляд.'),
      ('3', '<b>Три доходных продукта</b> Becar в одной логике подачи, поэтому '
       'разговор с инвестором продолжается и после ТЦ «Смайл».'),
    ]
    lis = ''.join(f'<li><span>{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="sb-res"><div class="sb-w sb-res__grid">'
      '<div class="sb-r"><span class="sb-kick">Результат</span>'
      '<h2>Что получил клиент</h2>'
      '<p class="sb-res__more">Тот же объект мы вели и в digital: '
      '<a href="/digital/becar/smile">посадочная страница ТЦ «Смайл»</a>. '
      'Больше о направлении: '
      '<a href="/creativedesign">услуга «Creative&nbsp;&amp;&nbsp;Design»</a></p></div>'
      f'<ul class="sb-res__list sb-r">{lis}</ul>'
      '</div></section>')


LIGHTBOX = ('<div class="sb-lb" id="sb-lb" aria-hidden="true">'
            '<div class="sb-lb__box">'
            '<button class="sb-lb__x" id="sb-lb-x" type="button" aria-label="Закрыть">&times;</button>'
            '<img id="sb-lb-img" src="" alt="">'
            '<div class="sb-lb__cap" id="sb-lb-cap"></div></div></div>')

ARC_JS_DATA = ',\n  '.join(
  '{{t:"{0}",n:"{1}"}}'.format(label, n.replace('"', '\\"'))
  for v, u, label, n in ARC)

ZONE_JS_DATA = ',\n  '.join(
  '{0}:[{1},{2}]'.format(code, str(a).lower(), str(b).lower())
  for code, name, num, note, (a, b) in ZONES)

PAGE_JS = """<script>(function(){
 // ── листалка разворотов ──
 var track=document.getElementById('sb-track');
 if(track){
  var slides=[].slice.call(track.querySelectorAll('.sb-slide')),
      thumbs=[].slice.call(document.querySelectorAll('.sb-thumb')),
      prev=document.getElementById('sb-prev'),next=document.getElementById('sb-next'),
      count=document.getElementById('sb-count'),cur=1,total=slides.length;
  function pad(n){return n<10?'0'+n:''+n;}
  function mark(i){cur=i;
   count.innerHTML='<b>'+pad(i)+'</b> / '+pad(total);
   thumbs.forEach(function(t,k){t.classList.toggle('is-on',k===i-1);});
   prev.disabled=(i===1);next.disabled=(i===total);
   var t=thumbs[i-1];
   if(t&&t.parentNode.scrollWidth>t.parentNode.clientWidth){
    var box=t.parentNode,l=t.offsetLeft-(box.clientWidth-t.offsetWidth)/2;
    box.scrollTo({left:l,behavior:'smooth'});}
  }
  function go(i){i=Math.min(total,Math.max(1,i));
   track.scrollTo({left:slides[i-1].offsetLeft-track.offsetLeft,behavior:'smooth'});mark(i);}
  prev.addEventListener('click',function(){go(cur-1);});
  next.addEventListener('click',function(){go(cur+1);});
  thumbs.forEach(function(t){t.addEventListener('click',function(){go(+t.getAttribute('data-go'));});});
  var tmr;
  track.addEventListener('scroll',function(){clearTimeout(tmr);tmr=setTimeout(function(){
   var mid=track.scrollLeft+track.clientWidth/2,best=1,d=1e9;
   slides.forEach(function(s,k){var c=s.offsetLeft-track.offsetLeft+s.offsetWidth/2,
    dd=Math.abs(c-mid);if(dd<d){d=dd;best=k+1;}});
   if(best!==cur)mark(best);},90);});
  track.addEventListener('keydown',function(e){
   if(e.key==='ArrowRight'){e.preventDefault();go(cur+1);}
   if(e.key==='ArrowLeft'){e.preventDefault();go(cur-1);}});
  mark(1);
 }
 // ── дуга с цифрами ──
 var AR=[__ARC__];
 var say=document.getElementById('sb-arc-say');
 if(say){
  var dots=[].slice.call(document.querySelectorAll('.sb-dot'));
  dots.forEach(function(g){
   function on(){var d=AR[+g.getAttribute('data-i')];
    dots.forEach(function(x){x.classList.toggle('is-on',x===g);});
    say.innerHTML='<b>'+d.t+'</b><span>'+d.n+'</span>';}
   g.addEventListener('mouseenter',on);
   g.addEventListener('focus',on);
   g.addEventListener('click',on);
   g.addEventListener('keydown',function(e){
    if(e.key==='Enter'||e.key===' '){e.preventDefault();on();}});
  });
 }
 // ── стрит-ритейл или кондо-ТЦ ──
 var seg=document.getElementById('sb-seg');
 if(seg){
  var btns=[].slice.call(seg.querySelectorAll('button'));
  btns.forEach(function(b){b.addEventListener('click',function(){
   var id=b.getAttribute('data-pane');
   btns.forEach(function(x){var on=(x===b);x.classList.toggle('is-on',on);
    x.setAttribute('aria-pressed',on?'true':'false');});
   [].forEach.call(document.querySelectorAll('.sb-pane'),function(p){
    p.classList.toggle('is-on',p.id==='sb-pane-'+id);});
  });});
 }
 // ── зоны охвата ──
 var zt=document.getElementById('sb-zones');
 if(zt){
  var Z={__ZONES__},z1=document.getElementById('sb-z-1'),
      z2=document.getElementById('sb-z-2'),
      zb=[].slice.call(zt.querySelectorAll('.sb-ztab'));
  zb.forEach(function(b){b.addEventListener('click',function(){
   var s=Z[b.getAttribute('data-z')];
   zb.forEach(function(x){var on=(x===b);x.classList.toggle('is-on',on);
    x.setAttribute('aria-pressed',on?'true':'false');});
   z1.classList.toggle('is-on',s[0]);z2.classList.toggle('is-on',s[1]);
  });});
 }
 // ── калькулятор дохода ──
 var sum=document.getElementById('sb-sum'),yrs=document.getElementById('sb-years'),
     prods=document.getElementById('sb-prods');
 if(sum&&yrs&&prods){
  var rate=13;
  function fmt(n){return Math.round(n).toLocaleString('ru-RU');}
  function mln(n){return (Math.round(n*100)/100).toLocaleString('ru-RU',
   {minimumFractionDigits:2,maximumFractionDigits:2});}
  function fill(el){var min=+el.min,max=+el.max;
   el.style.setProperty('--f',((el.value-min)/(max-min)*100)+'%');}
  function calc(){
   var s=+sum.value*1e6,y=+yrs.value,year=s*rate/100;
   document.getElementById('sb-sum-v').textContent=(+sum.value).toLocaleString('ru-RU',
    {minimumFractionDigits:1,maximumFractionDigits:1});
   document.getElementById('sb-years-v').textContent=y;
   document.getElementById('sb-o-month').textContent=fmt(year/12)+' \\u20bd';
   document.getElementById('sb-o-year').textContent=fmt(year)+' \\u20bd';
   document.getElementById('sb-o-total').textContent=mln(year*y/1e6)+' \\u043c\\u043b\\u043d \\u20bd';
   document.getElementById('sb-o-sum').textContent=mln((s+year*y)/1e6)+' \\u043c\\u043b\\u043d \\u20bd';
   fill(sum);fill(yrs);
  }
  [sum,yrs].forEach(function(el){el.addEventListener('input',calc);});
  [].forEach.call(prods.querySelectorAll('button'),function(b){
   b.addEventListener('click',function(){
    rate=+b.getAttribute('data-rate');
    [].forEach.call(prods.querySelectorAll('button'),function(x){
     var on=(x===b);x.classList.toggle('is-on',on);
     x.setAttribute('aria-pressed',on?'true':'false');});
    calc();});});
  calc();
 }
 // ── лайтбокс разворотов ──
 var lb=document.getElementById('sb-lb'),lbi=document.getElementById('sb-lb-img'),
     lbc=document.getElementById('sb-lb-cap'),lbx=document.getElementById('sb-lb-x');
 function open(src,cap,alt){lbi.src=src;lbi.alt=alt||'';lbc.textContent=cap||'';
  lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';lbx.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  lbi.removeAttribute('src');document.body.style.overflow='';}
 [].forEach.call(document.querySelectorAll('.sb-zoom'),function(z){
  function fire(){var im=z.querySelector('img');
   open(z.getAttribute('data-src'),z.getAttribute('data-cap'),im?im.alt:'');}
  z.addEventListener('click',fire);
  z.addEventListener('keydown',function(e){
   if(e.key==='Enter'||e.key===' '){e.preventDefault();fire();}});});
 lbx.addEventListener('click',close);
 lb.addEventListener('click',function(e){if(e.target===lb||e.target===lb.firstChild)close();});
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape'&&lb.classList.contains('is-open'))close();});
 // ── reveal ──
 var els=[].slice.call(document.querySelectorAll('.sb-r'));
 function show(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(show);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){show(e.target);io.unobserve(e.target);}});},
  {rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)show(n);else io.observe(n);});
})();</script>""".replace('__ARC__', ARC_JS_DATA).replace('__ZONES__', ZONE_JS_DATA)

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Брошюра ТЦ «Смайл»",'
  f'"item":"{URL}"}}]}}</script>')


def build():
    # Отдельного CTA-блока нет: фиолетовая форма из rc.footer() уже закрывает страницу
    body = (f'{rc.header()}<main class="sb">{hero()}{obj()}{task()}{arc()}{two()}'
            f'{calc()}{secret()}{family()}{zones()}{book()}{craft()}{result()}'
            f'</main>{LIGHTBOX}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'becar', 'smile')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
