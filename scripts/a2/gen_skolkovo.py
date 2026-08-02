#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/creative/skolkovo/index.html — кейс «Цифровое производство»
для Московской школы управления СКОЛКОВО: рабочий доклад Департамента
корпоративного обучения на 86 полос, октябрь 2017.

Задача клиента была из двух частей: сверстать издание по брендбуку СКОЛКОВО
и переработать инфографику так, чтобы её читал не только автор. Поэтому
страница построена вокруг схем, а не вокруг обложки.

Дизайн-концепция «косая полоса»: фирменный элемент издания это лесенка
наклонных параллелограммов (красный, бордо, сине-серый). Она же и есть
графика диффузии: полосы набегают одна на другую. Шрифты Golos Text
(гротеск вместо PF Centro Sans) + PT Serif (наборный сериф издания),
локальные, /fonts/golos-ptserif.css.

Живые блоки:
  • «ромашка» ODM3: 15 сегментов диагностики × 5 уровней зрелости, как на
    рисунке 19 доклада. Уровень ставится кликом по кольцу или кнопками
    в списке, страница считает средний балл и называет ступень;
  • 15 ключевых компонентов производства: карточки с кодами из рисунка 7;
  • скорость диффузии: четыре технологии из вступления доклада, полосы
    прочерчиваются по скроллу;
  • листалка 12 разворотов и галерея одиннадцати схем с лайтбоксом.

Ассеты: mirror/images/skolkovo/ (scripts/skolkovo-assets.py).

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

IMG = '/images/skolkovo'
URL = 'https://hand-marketing.ru/creative/skolkovo/'

RED = '#EE2837'      # акцент издания
WINE = '#AA112D'     # бордо плашек
STEEL = '#486C84'    # сине-серый

# ─── 15 ключевых компонентов (рисунок 7 и глава 1) ───────────────────────────
# (номер, код, группа 0-2, название, что стоит за пунктом в докладе)
COMPONENTS = [
 (1, 'EIM', 0, 'Информационная платформа предприятия',
  'EIM = PLM + MES + ERP. Централизованный цифровой хаб на всех стадиях жизненного '
  'цикла проекта: конструирование, цех, цепь поставок, логистика, адаптация продукта '
  'под потребителя при продажах и сервисе.'),
 (2, 'DM', 0, 'Моделирование и оптимизация',
  'Инженерный анализ как отдельное бизнес-направление: виртуальное прототипирование, '
  'численный эксперимент, анализ методом конечных элементов, моделирование '
  'в гидродинамике. Влияет на сроки разработки сильнее всего остального.'),
 (3, 'DT', 0, 'Цифровые двойники',
  'Полная информационная модель выпускаемого продукта, продажи через виртуальную '
  'реальность и сервис с дополненной. Caterpillar возит в представительство не грейдер, '
  'а его 3D-модель, и предиктивная аналитика ведёт «точечный» ремонт.'),
 (4, 'CA', 0, 'Корпоративный акселератор',
  'Акселераторы, инновационные центры и лаборатории как ключевой драйвер роста: '
  'они держат компанию в готовности к непрерывной адаптации и ускоренной диффузии '
  'технологий.'),
 (5, 'IAS', 0, 'Интеллектуальная собственность',
  'Нематериальные активы не обязательно в форме патентов, но обязательно в форме '
  'секретов производства и ноу-хау, интегрированных в хозяйственную деятельность '
  'и зафиксированных в балансе.'),
 (6, 'DRE', 1, 'Цифровой реверс-инжиниринг',
  'Сервисная база рядом с потребителем сканирует изношенные детали и передаёт 3D-модели '
  'на домашнее предприятие. Банки данных PDM наполняются реальными составами изделий '
  'работающего оборудования.'),
 (7, 'AM', 1, 'Аддитивное производство',
  '3D-печать для модельных испытаний и быстрого прототипирования. Без своего принтера '
  'или партнёра-студии компания не будет такой же быстрой в выпуске новых продуктов, '
  'как те, кто аддитивные методы освоил.'),
 (8, 'EE', 1, 'Энергоэффективность',
  'Сертификация по LEED и BREEAM, сокращение эксплуатационных затрат на 25% и более. '
  'Прямо влияет на себестоимость продукции и снижает накладные расходы предприятия.'),
 (9, 'CAW', 1, 'Автоматизированные рабочие места в цехах',
  'Слесари-сборщики работают с интерактивными электронными руководствами, операторы ЧПУ '
  'с цифровыми ассистентами процессов, начальник цеха видит производительность участков '
  'с пульта, как в цехе «Высота 239» на ЧТПЗ.'),
 (10, 'L', 1, 'Производственная система',
  'Технологии бережливого производства, планировка цеха, стандартизация процесса '
  'и культура порядка в цехах. В неухоженном цехе конкурентоспособный продукт '
  'не производится.'),
 (11, 'DL', 2, 'Цифровая логистика',
  'Управление материальными потоками с радиочастотной идентификацией (RFID), контроль '
  'передвижения сырья и материалов, автономная логистическая робототехника '
  'и роботизированные системы обслуживания складов.'),
 (12, 'TT', 2, 'Трансфер технологий',
  'Купив иностранное оборудование, компания планирует локализацию его производства. '
  'Иначе через пять лет она собственник морально устаревших металлоконструкций, '
  'а сервис европейского инженера стоит от 100 евро в час.'),
 (13, 'CIC', 2, 'Кросс-отраслевая кооперация',
  'Эффект платформы и обмен ресурсами. Hewlett-Packard, National Instruments, PTC '
  'и Flowserve выпускают насосные агрегаты на промышленном интернете вещей, '
  'Yandex Data Factory и ММК оптимизируют расход ферросплавов.'),
 (14, 'EDU', 2, 'Партнёрство с образовательными платформами',
  'Учебные производственные центры на предприятии, фаблабы в регионе, участие цеховых '
  'специалистов в WorldSkills и EuroSkills, развитие команд руководителей в школах '
  'управления.'),
 (15, 'PM', 2, 'Управление проектами',
  'Обеспечить сроки поставки сложных видов оборудования и требуемое качество '
  'без специалистов, ведущих проекты по международным методологиям, невозможно.'),
]

GROUPS = [
 ('Раздел 1', 'Проектирование и технологическая подготовка производства', RED),
 ('Раздел 2', 'Производство', WINE),
 ('Раздел 3', 'Управление и материально-техническое снабжение', STEEL),
]

# ─── пять ступеней зрелости ODM3 (глава 3) ───────────────────────────────────
LEVELS = [
 ('A', 'Ad-Hoc', 'случайный',
  'Технологии внедряются нерегулярно и внепланово, правила использования не определены. '
  'Связь технологии и производительности для руководства не установлена.'),
 ('B', 'Defined', 'базовый',
  'Определён единый подход к внедрению, реализованы отдельные технологические модули, '
  'потребность в изменениях осознана через референс-визиты.'),
 ('C', 'Managed', 'управляемый',
  'Технологии работают в промышленной эксплуатации и синхронизированы с продуктами '
  'других систем. Развитие основано на документированных результатах.'),
 ('D', 'Integrated', 'интегрируемый',
  'Ключевые модули PLM внедрены, составы изделий передаются в ERP, общая шина данных '
  'стала основанием долгосрочной стратегии.'),
 ('E', 'Optimized', 'оптимизируемый',
  'Документированных процедур хватает для тиражирования в глобальной экспансии, '
  'ноу-хау и лучшие практики уходят на новые рынки через сеть дочерних предприятий.'),
]

# ─── развороты листалки: (левая полоса, глава, заголовок, описание) ──────────
SPREADS = [
 (8, 'Структура доклада',
  'Алгоритм из семи шагов',
  'Шмуцтитул с косой лесенкой и цитатой Тойнби, справа рисунок 1: система развития '
  'цифровых предприятий свёрнута в круг из пяти шагов, от осознания до результатов '
  'для компании. В исходном тексте это был нумерованный список на семь пунктов.'),
 (10, 'Ускорение диффузии',
  'Сто десять лет за один разворот',
  'Рисунок 2 показывает степень внедрения десяти потребительских технологий с 1900 года. '
  'Чем ближе к нашему времени, тем вертикальнее кривая: интернету, чтобы дойти '
  'до большинства, потребовалось в разы меньше времени, чем телефону.'),
 (12, 'Ускорение диффузии',
  'Стоимость, упавшая в разы',
  'Рисунок 3 собран из семи плиток: беспилотник со 100 тысяч долларов до 700, '
  'секвенирование ДНК с 40 тысяч до 100, киловатт-час солнечной энергии с 30 долларов '
  'до 16 центов. Кадры техники держат ряд, цифры лежат на сине-серых плашках.'),
 (18, 'Глава 1',
  '15 ключевых компонентов',
  'Главная схема доклада, рисунок 7. Сто систем и технологий сведены к пятнадцати '
  'направлениям, у каждого свой код и цвет: EIM, DM, DT, CA, IAS, DRE, AM, EE, CAW, L, '
  'DL, TT, CIC, EDU, PM. Дальше эти коды работают навигацией по всему изданию.'),
 (26, 'Глава 2',
  'Традиционное и передовое производство',
  'Рисунок 9: два графика рядом. Слева стоимость изменений взлетает в конце цикла, '
  'справа «умная» модель переносит пик изменений в начало разработки. Один разворот '
  'объясняет, зачем нужен цифровой двойник.'),
 (30, 'Глава 2',
  'Экосистема технологий',
  'Рисунок 11: испытательный полигон, цифровая платформа CML-Bench и экспертная '
  'система CML-AI показаны слоями в изометрии, снизу вверх, от инструментов CAD и CAE '
  'до цифровых фабрик.'),
 (32, 'Глава 2',
  'Цикл Гартнера и Фабрики Будущего',
  'На левой полосе рисунок 13: технологии разложены по циклу зрелости Гартнера 2017 года, '
  'форма кривой перерисована в цветах издания. Справа рисунок 14, трёхуровневая схема '
  'Фабрик Будущего с заседания президиума Совета при Президенте.'),
 (40, 'Глава 3',
  'Ромашка зрелости и метасистема EIM',
  'Слева рисунок 15: пятнадцать направлений и пять уровней собраны в круговую диаграмму, '
  'по которой видно место компании. Справа рисунок 16: модули метасистемы EIM от RE и CAD '
  'до BI, связанные линиями данных на семи этапах жизненного цикла.'),
 (48, 'Глава 4',
  'Трансфер технологий по этапам',
  'Рисунок 18 разложен на семь ступеней производительности и пять ролей: интегратор, '
  'носитель, преемник технологий, совместное предприятие и инвестор. Кружки с ролями '
  'стоят там, где участник вступает в дело.'),
 (50, 'Глава 3',
  'Бенчмаркинг двух компаний',
  'Рисунок 19, ради которого затевалась вся система кодов: две компании положены '
  'на одну ромашку, красным заполнены уровни первой, голубым второй. Разрыв виден '
  'без единой цифры.'),
 (72, 'Глава 6',
  'Автономные производства',
  'Заключительная глава про управление цифровым жизненным циклом: блокчейн, цифровое '
  'удостоверение личности изделия, дополненная реальность в сервисе.'),
 (80, 'Приложение 1',
  'Опросный лист диагностики',
  'Тот самый инструмент, ради которого писался доклад: пятнадцать сегментов, в каждом '
  'вопросы с пятью вариантами ответа и баллом от 0 до 4. Табличная вёрстка со сквозной '
  'нумерацией и колонкой баллов справа.'),
]

# ─── галерея схем: (файл, номер, заголовок, что было сложным) ────────────────
FIGURES = [
 ('fig-cycle.jpg', 'Рисунок 1', 'Система развития цифровых предприятий',
  'Семь шагов алгоритма свёрнуты в круг из пяти секторов со сквозной нумерацией.'),
 ('fig-diffusion.jpg', 'Рисунок 2', 'Диффузия потребительских технологий',
  'Десять кривых за 110 лет, каждая подписана номером у точки старта, чтобы '
  'легенда не спорила с графиком.'),
 ('fig-cost.jpg', 'Рисунок 3', 'Падение стоимости ключевых технологий',
  'Семь плиток с фотографией техники и парой «было, стало» вместо таблицы из отчёта WEF.'),
 ('fig-15.jpg', 'Рисунок 7', '15 компонентов современного производства',
  'Сто систем и технологий сведены в сетку карточек, у каждой свой код и цвет.'),
 ('fig-compare.jpg', 'Рисунок 9', 'Традиционный и передовой подходы',
  'Два графика на одном развороте: пик стоимости изменений уезжает в начало цикла.'),
 ('fig-gartner.jpg', 'Рисунок 12', 'Цикл зрелости технологий Гартнера',
  'Кривая перерисована в цветах издания, зоны цикла лежат внизу цветной шкалой.'),
 ('fig-factories.jpg', 'Рисунок 14', 'Трёхуровневая схема Фабрик Будущего',
  'Три слоя в изометрии: цифровая платформа, «умные» модели, тотальная цифровизация цикла.'),
 ('fig-flowers.jpg', 'Рисунок 15', 'Уровни развития и результат диагностики',
  'Две ромашки рядом: слева шкала уровней, справа заполненная оценка компании.'),
 ('fig-eim.jpg', 'Рисунок 16', 'Модули и системы метасистемы EIM',
  'Семь этапов жизненного цикла слева, модули от RE до BI связаны линиями данных.'),
 ('fig-transfer.jpg', 'Рисунок 18', 'Система трансфера технологий',
  'Семь ступеней производительности, пять ролей участников и время по горизонтали.'),
 ('fig-bench.jpg', 'Рисунок 19', 'Бенчмаркинг двух компаний',
  'Красная и голубая компании на одной ромашке: разрыв читается без цифр.'),
]

# ─── скорость диффузии: из вступления Максима Шерейкина ──────────────────────
DIFFUSION = [
 ('Электричество', 30, 'чтобы охватить максимальное количество пользователей'),
 ('Телефон', 20, 'на тот же путь к массовому пользователю'),
 ('Сотовый телефон', 5, 'меньше пяти лет на адаптацию'),
 ('Планшет', 3, 'и вовсе три года, это последняя цифра ряда'),
]


# ─── «ромашка» ODM3: кольцевые секторы ───────────────────────────────────────
def ring_path(cx, cy, r0, r1, a0, a1):
    """Кольцевой сектор: углы в градусах, 0 сверху, по часовой."""
    def pt(r, a):
        rad = math.radians(a - 90)
        return f'{cx + r * math.cos(rad):.2f} {cy + r * math.sin(rad):.2f}'
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'M{pt(r0, a0)} L{pt(r1, a0)} A{r1} {r1} 0 {large} 1 {pt(r1, a1)} '
            f'L{pt(r0, a1)} A{r0} {r0} 0 {large} 0 {pt(r0, a0)} Z')


def flower():
    cx = cy = 260
    r_in, r_out = 66, 222
    step = (r_out - r_in) / 5
    gap = 2.6
    seg = 360 / 15
    petals = []
    labels = []
    for i, (num, code, grp, name, _) in enumerate(COMPONENTS):
        a0 = i * seg + gap / 2 - seg / 2      # первый сегмент строго на 12 часах
        a1 = (i + 1) * seg - gap / 2 - seg / 2
        for lv in range(5):
            r0 = r_in + step * lv + 1.6
            r1 = r_in + step * (lv + 1) - 1.6
            petals.append(
              f'<path class="sk-fl__cell" data-seg="{i}" data-lv="{lv + 1}" '
              f'data-grp="{grp}" d="{ring_path(cx, cy, r0, r1, a0, a1)}">'
              f'<title>{code}, уровень {lv + 1}: {LEVELS[lv][1]}</title></path>')
        mid = math.radians((a0 + a1) / 2 - 90)
        lr = r_out + 20
        x, y = cx + lr * math.cos(mid), cy + lr * math.sin(mid)
        anchor = 'middle'
        if x < cx - 24:
            anchor = 'end'
        elif x > cx + 24:
            anchor = 'start'
        labels.append(f'<text class="sk-fl__lb" data-seg="{i}" x="{x:.1f}" y="{y:.1f}" '
                      f'text-anchor="{anchor}" dominant-baseline="middle">{code}</text>')
    core = (f'<circle class="sk-fl__core" cx="{cx}" cy="{cy}" r="{r_in - 8}"/>'
            f'<text class="sk-fl__score" x="{cx}" y="{cy - 4}" text-anchor="middle">0.0</text>'
            f'<text class="sk-fl__grade" x="{cx}" y="{cy + 22}" text-anchor="middle">балл</text>')
    return ('<svg class="sk-fl__svg" viewBox="-26 -18 572 556" role="img" '
            'aria-label="Круговая диаграмма зрелости: 15 сегментов по пяти уровням">'
            + ''.join(petals) + ''.join(labels) + core + '</svg>')


PAGE_CSS = """<style id="sk-css">
.sk{--red:#EE2837;--wine:#AA112D;--steel:#486C84;--ink:#1D2329;--mute:#66727E;
  --line:rgba(29,35,41,.12);--mist:#F2F4F6;--capt:#6C8FB0;
  font-family:'Golos Text',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff;
  overflow-x:hidden}
.sk *{box-sizing:border-box}
/* у картинок проставлены width/height атрибутами, без height:auto они тянутся */
.sk img{max-width:100%;height:auto}
.sk section{padding:96px 40px}
.sk__in{max-width:1180px;margin:0 auto}
.sk h2{font-size:clamp(28px,3.6vw,46px);line-height:1.06;font-weight:600;margin:0 0 18px;
  letter-spacing:-.02em}
.sk h3{font-size:22px;font-weight:600;margin:0 0 10px;line-height:1.2}
.sk p{margin:0 0 16px;font-size:17px;line-height:1.62;color:#3A444E}
.sk .sk__lead{font-family:'PT Serif',Georgia,serif;font-size:20px;line-height:1.6;color:#2B333B}
.sk .sk__kicker{font-size:12px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;
  color:var(--capt);margin:0 0 14px}
.sk .sk__cap{font-size:14px;color:var(--capt);margin:10px 0 0;line-height:1.45}
.sk .sk__note{font-size:14.5px;color:var(--mute);line-height:1.55}

/* лесенка косых полос: фирменный элемент издания */
.sk-st{display:block}
.sk-st span{display:block;height:var(--h,18px);width:var(--w,120px);
  transform:skewY(-9deg);margin-bottom:9px}

/* ГЕРОЙ */
.sk-hero{position:relative;padding:0;background:#fff;border-bottom:1px solid var(--line)}
.sk-hero__in{max-width:1180px;margin:0 auto;padding:64px 40px 72px;display:grid;
  grid-template-columns:1.08fr .92fr;gap:52px;align-items:center;position:relative;z-index:2}
.sk .sk-hero__logo{height:44px;width:auto;display:block;margin:0 0 24px}
.sk-hero h1{font-size:clamp(38px,6vw,80px);line-height:.96;font-weight:500;margin:0 0 10px;
  letter-spacing:-.03em;text-transform:uppercase}
.sk-hero__sub{font-size:clamp(16px,2vw,26px);font-weight:400;color:var(--steel);
  text-transform:uppercase;letter-spacing:.02em;margin:0 0 26px}
.sk-hero__txt{font-family:'PT Serif',Georgia,serif;font-size:18px;line-height:1.6;
  color:#2B333B;max-width:30em;margin:0 0 30px}
.sk-hero__spec{display:flex;flex-wrap:wrap;gap:10px 34px;margin:0;padding:0;list-style:none}
.sk-hero__spec b{display:block;font-size:30px;font-weight:600;line-height:1;letter-spacing:-.02em}
.sk-hero__spec span{font-size:13px;color:var(--mute)}
.sk-hero__art{position:relative}
.sk-hero__art img.cover{width:100%;display:block;box-shadow:0 30px 60px rgba(29,35,41,.22);
  position:relative;z-index:2}
.sk-hero__bars{position:absolute;right:-78px;bottom:-46px;z-index:3;pointer-events:none;
  display:flex;flex-direction:column;align-items:flex-end}
.sk-hero__bars span{opacity:0;animation:sk-bar .6s cubic-bezier(.2,.7,.3,1) forwards}
@keyframes sk-bar{from{opacity:0;transform:skewY(-9deg) translateX(-38px)}
  to{opacity:1;transform:skewY(-9deg) translateX(0)}}

/* ЗАДАЧА */
.sk-task{background:var(--mist)}
.sk-task__grid{display:grid;grid-template-columns:1fr 1fr;gap:52px;align-items:start}
.sk-task__box{background:#fff;padding:30px 32px;border-top:6px solid var(--red)}
.sk-task__box.b2{border-top-color:var(--steel)}
.sk-task__box h3{font-size:15px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);
  font-weight:600;margin-bottom:14px}
.sk-task__box p:last-child{margin-bottom:0}
.sk-task__quote{font-family:'PT Serif',Georgia,serif;font-size:19px;line-height:1.55;
  color:var(--ink);margin:0 0 12px}

/* СИСТЕМА */
.sk-sys__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:36px}
.sk-sys__card{border:1px solid var(--line);padding:26px 24px 28px}
.sk-sys__card h3{font-size:18px}
.sk-sys__card p{font-size:15px;line-height:1.55;margin:0}
.sk-sys__swatch{display:flex;gap:0;margin:0 0 20px}
.sk-sys__swatch i{display:block;height:56px;flex:1;transform:skewX(-14deg)}
.sk-sys__type{margin:0 0 18px}
.sk-sys__type b{display:block;font-size:34px;font-weight:600;line-height:1.05;letter-spacing:-.02em}
.sk-sys__type em{display:block;font-family:'PT Serif',Georgia,serif;font-style:normal;
  font-size:17px;line-height:1.4;color:#3A444E;margin-top:6px}
.sk-sys__fig{margin:0 0 18px;font-size:15px;color:var(--capt);border-left:3px solid var(--capt);
  padding-left:12px;line-height:1.4}

/* ДИФФУЗИЯ */
.sk-dif{background:var(--ink);color:#fff}
.sk-dif h2,.sk-dif h3{color:#fff}
.sk-dif p{color:rgba(255,255,255,.78)}
.sk-dif__grid{display:grid;grid-template-columns:1fr 1.05fr;gap:56px;align-items:center}
.sk-dif__rows{margin:0;padding:0;list-style:none}
.sk-dif__row{padding:16px 0;border-bottom:1px solid rgba(255,255,255,.14)}
.sk-dif__row:last-child{border-bottom:0}
.sk-dif__hd{display:flex;justify-content:space-between;align-items:baseline;gap:16px;
  margin-bottom:10px}
.sk-dif__hd b{font-size:19px;font-weight:600}
.sk-dif__hd i{font-style:normal;font-size:15px;color:rgba(255,255,255,.6)}
.sk-dif__bar{height:12px;background:rgba(255,255,255,.12);position:relative;overflow:hidden}
.sk-dif__bar i{position:absolute;inset:0 auto 0 0;width:0;background:var(--red);
  transition:width 1.1s cubic-bezier(.2,.7,.3,1)}
.sk-dif.on .sk-dif__bar i{width:var(--w)}
.sk-dif__fig{margin:0}
.sk-dif__fig img{width:100%;display:block;background:#fff;padding:14px}

/* 15 КОМПОНЕНТОВ */
.sk-cmp__legend{display:flex;flex-wrap:wrap;gap:12px 26px;margin:0 0 30px;padding:0;list-style:none}
.sk-cmp__legend li{font-size:14px;color:var(--mute);display:flex;align-items:center;gap:8px}
.sk-cmp__legend i{width:22px;height:10px;display:block;transform:skewX(-14deg)}
.sk-cmp__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.sk-cmp__card{border:1px solid var(--line);padding:20px 20px 18px;background:#fff;
  transition:border-color .18s,transform .18s,box-shadow .18s}
.sk-cmp__card:hover{border-color:rgba(29,35,41,.28);transform:translateY(-2px);
  box-shadow:0 12px 26px rgba(29,35,41,.09)}
.sk-cmp__top{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.sk-cmp__num{font-size:13px;color:var(--mute);font-variant-numeric:tabular-nums}
.sk-cmp__code{font-size:12px;font-weight:700;letter-spacing:.08em;color:#fff;padding:4px 9px;
  transform:skewX(-14deg)}
.sk-cmp__code span{display:block;transform:skewX(14deg)}
.sk-cmp__card h3{font-size:16px;line-height:1.25;margin:0}
.sk-cmp__body p{font-size:14.5px;line-height:1.55;margin:12px 0 0;color:#3A444E}

/* РОМАШКА ODM3 */
.sk-odm{background:var(--mist)}
.sk-odm__grid{display:grid;grid-template-columns:minmax(0,520px) minmax(0,1fr);gap:48px;
  align-items:start;margin-top:38px}
.sk-fl{position:sticky;top:104px}
.sk-fl__svg{width:100%;height:auto;display:block}
.sk-fl__cell{fill:#D8DEE4;stroke:#F2F4F6;stroke-width:1;cursor:pointer;
  transition:fill .18s,opacity .18s}
.sk-fl__cell:hover{opacity:.72}
.sk-fl__cell.on[data-grp="0"]{fill:#EE2837}
.sk-fl__cell.on[data-grp="1"]{fill:#AA112D}
.sk-fl__cell.on[data-grp="2"]{fill:#486C84}
.sk-fl__lb{font-size:12px;font-weight:600;fill:#66727E}
.sk-fl__lb.on{fill:#1D2329}
.sk-fl__core{fill:#fff;stroke:rgba(29,35,41,.1)}
.sk-fl__score{font-size:30px;font-weight:600;fill:#1D2329}
.sk-fl__grade{font-size:12px;fill:#66727E;letter-spacing:.04em}
.sk-odm__verdict{background:#fff;padding:22px 24px;border-left:6px solid var(--red);
  margin:0 0 24px}
.sk-odm__verdict b{display:block;font-size:20px;margin-bottom:6px}
.sk-odm__verdict p{margin:0;font-size:15px;line-height:1.55}
.sk-odm__ctl{display:flex;gap:12px;margin:0 0 22px;flex-wrap:wrap}
.sk-btn{border:1px solid rgba(29,35,41,.2);background:#fff;padding:11px 20px;font:600 14px 'Golos Text',Arial,sans-serif;
  cursor:pointer;color:var(--ink);transition:background .15s,color .15s,border-color .15s}
.sk-btn:hover{background:var(--ink);border-color:var(--ink);color:#fff}
.sk-odm__rows{margin:0;padding:0;list-style:none;background:#fff}
.sk-odm__row{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:center;
  padding:11px 18px;border-bottom:1px solid var(--line)}
.sk-odm__row:last-child{border-bottom:0}
.sk-odm__row.hl{background:#FDF2F3}
.sk-odm__row code{font:700 12px 'Golos Text',Arial,sans-serif;letter-spacing:.06em;color:#fff;
  padding:4px 8px;transform:skewX(-14deg);display:block}
.sk-odm__row code span{display:block;transform:skewX(14deg)}
.sk-odm__row .nm{font-size:14.5px;line-height:1.3}
.sk-odm__steps{display:flex;gap:4px}
.sk-odm__steps button{width:30px;height:30px;border:1px solid var(--line);background:#fff;
  cursor:pointer;font:600 12px 'Golos Text',Arial,sans-serif;color:var(--mute);transition:.15s}
.sk-odm__steps button:hover{border-color:var(--ink);color:var(--ink)}
.sk-odm__steps button.on{background:var(--ink);border-color:var(--ink);color:#fff}
.sk-odm__levels{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:34px}
.sk-odm__lv{border-top:4px solid var(--line);padding-top:14px}
.sk-odm__lv b{display:block;font-size:15px;margin-bottom:4px}
.sk-odm__lv i{font-style:normal;font-size:12px;color:var(--mute);display:block;margin-bottom:8px}
.sk-odm__lv p{font-size:13px;line-height:1.45;margin:0;color:#3A444E}

/* ЛИСТАЛКА */
.sk-book__track{display:flex;gap:26px;overflow-x:auto;scroll-snap-type:x mandatory;
  padding:6px 0 22px;scrollbar-width:thin}
.sk-book__item{flex:0 0 min(880px,84vw);scroll-snap-align:center}
.sk-book__item img{width:100%;display:block;box-shadow:0 18px 40px rgba(29,35,41,.14);cursor:zoom-in}
.sk-book__meta{display:grid;grid-template-columns:auto 1fr;gap:18px;margin-top:16px;align-items:start}
.sk-book__folio{font-size:13px;color:var(--capt);font-weight:600;white-space:nowrap;
  letter-spacing:.06em;text-transform:uppercase}
.sk-book__meta h3{font-size:18px;margin:0 0 6px}
.sk-book__meta p{font-size:14.5px;line-height:1.5;margin:0;color:#3A444E;max-width:62ch}
.sk-book__thumbs{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}
.sk-book__thumbs button{border:1px solid var(--line);padding:0;background:none;cursor:pointer;
  line-height:0;transition:border-color .15s,opacity .15s;opacity:.62}
.sk-book__thumbs button.on,.sk-book__thumbs button:hover{opacity:1;border-color:var(--ink)}
.sk-book__thumbs img{width:88px;height:auto;display:block}

/* СХЕМЫ */
.sk-fig__grid{display:grid;grid-template-columns:repeat(2,1fr);gap:34px;margin-top:36px}
.sk-fig__card figure{margin:0}
/* схемы разной пропорции: вписываем в один бокс, чтобы сетка не рвалась,
   детали смотрятся в лайтбоксе */
.sk .sk-fig__card img{width:100%;height:300px;object-fit:contain;display:block;
  border:1px solid var(--line);cursor:zoom-in;background:#fff;padding:12px}
.sk-fig__card figcaption{margin-top:12px}
.sk-fig__no{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  color:var(--capt);display:block;margin-bottom:5px}
.sk-fig__card h3{font-size:17px;margin:0 0 6px}
.sk-fig__card p{font-size:14.5px;line-height:1.5;margin:0;color:#3A444E}

/* МОКАПЫ */
.sk-mock{background:var(--mist)}
.sk-mock__grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:34px}
.sk-mock__grid img{width:100%;display:block}
.sk-mock__grid figure{margin:0}
.sk-mock__grid .wide{grid-column:1/-1}

/* ИТОГ */
.sk-res__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:34px}
.sk-res__card{border-top:4px solid var(--ink);padding-top:16px}
.sk-res__card b{display:block;font-size:15px;margin-bottom:6px}
.sk-res__card p{font-size:14px;line-height:1.5;margin:0;color:#3A444E}
.sk-res__ph{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:44px}
.sk .sk-res__ph img{width:100%;height:200px;object-fit:cover;display:block}

/* ЛАЙТБОКС */
.sk-lb{position:fixed;inset:0;background:rgba(15,19,23,.94);z-index:9000;display:none;
  align-items:center;justify-content:center;padding:28px;cursor:zoom-out}
.sk-lb.on{display:flex}
.sk-lb img{max-width:100%;max-height:100%;display:block}
.sk-lb__x{position:absolute;top:18px;right:22px;background:none;border:0;color:#fff;font-size:34px;
  line-height:1;cursor:pointer}

/* появление */
.sk-r{opacity:0;transform:translateY(22px);transition:opacity .6s ease,transform .6s ease}
.sk-r.on{opacity:1;transform:none}
.no-js .sk-r{opacity:1;transform:none}

@media (max-width:980px){
  .sk section{padding:64px 22px}
  .sk-hero__in{grid-template-columns:1fr;gap:34px;padding:44px 22px 56px}
  .sk-hero__bars{display:none}
  .sk-task__grid,.sk-dif__grid,.sk-odm__grid,.sk-mock__grid{grid-template-columns:1fr;gap:28px}
  .sk-fig__grid{grid-template-columns:1fr}
  .sk .sk-fig__card img{height:230px}
  .sk-sys__grid,.sk-cmp__grid{grid-template-columns:1fr}
  .sk-res__grid{grid-template-columns:1fr 1fr}
  .sk-odm__levels{grid-template-columns:1fr 1fr}
  .sk-fl{position:static}
  .sk-res__ph{grid-template-columns:1fr 1fr}
  .sk-book__item{flex:0 0 92vw}
  .sk-book__meta{grid-template-columns:1fr;gap:8px}
}
@media (prefers-reduced-motion:reduce){
  .sk-r{opacity:1;transform:none;transition:none}
  .sk-hero__bars span{animation:none;opacity:1}
  .sk-dif__bar i{transition:none}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Доклад «Цифровое производство» для СКОЛКОВО: дизайн и вёрстка 86 полос | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: рабочий доклад Департамента корпоративного обучения Московской школы управления СКОЛКОВО «Цифровое производство. Методы, экосистемы, технологии». 86 полос, шесть глав, переработанная инфографика: 15 ключевых компонентов производства, модель зрелости ODM3, цикл Гартнера и Фабрики Будущего.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Доклад «Цифровое производство» для СКОЛКОВО | кейс Hand Marketing">
<meta property="og:description" content="86 полос по брендбуку СКОЛКОВО и переработанная инфографика: 15 компонентов цифрового производства и модель зрелости ODM3 на пятнадцать сегментов.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/cover.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/golos-ptserif.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def stripes(spec, cls=''):
    """Лесенка косых полос: spec — список (цвет, ширина, высота, задержка)."""
    out = []
    for col, w, h, d in spec:
        out.append(f'<span style="--w:{w}px;--h:{h}px;background:{col};'
                   f'animation-delay:{d}ms"></span>')
    return f'<span class="sk-st {cls}">' + ''.join(out) + '</span>'


HERO_BARS = [
    (WINE, 116, 18, 60), (RED, 152, 22, 140), (STEEL, 96, 16, 220),
    (WINE, 168, 24, 300), (RED, 112, 18, 380), (STEEL, 136, 20, 460),
]


def hero():
    spec = [('86', 'полос A4'), ('6', 'глав'), ('15', 'компонентов'),
            ('30', 'схем и таблиц'), ('46', 'источников')]
    li = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in spec)
    return f'''<section class="sk-hero">
<div class="sk-hero__in">
  <div class="sk-hero__txt-col">
    <img class="sk-hero__logo" src="{IMG}/logo-skolkovo.png" alt="Московская школа управления СКОЛКОВО" width="240" height="46" loading="eager">
    <p class="sk__kicker">Creative &amp; Design, издание</p>
    <h1>Цифровое<br>производство</h1>
    <p class="sk-hero__sub">Методы, экосистемы, технологии</p>
    <p class="sk-hero__txt">Рабочий доклад Департамента корпоративного обучения Московской школы
      управления СКОЛКОВО. Мы сверстали издание по брендбуку школы и переработали инфографику:
      сто систем и технологий нового уклада превратились в пятнадцать читаемых направлений
      и модель зрелости, по которой предприятие может оценить себя само.</p>
    <ul class="sk-hero__spec">{li}</ul>
  </div>
  <div class="sk-hero__art">
    <div class="sk-hero__bars">{stripes(HERO_BARS)}</div>
    <img class="cover" src="{IMG}/cover.jpg" alt="Обложка доклада «Цифровое производство. Методы, экосистемы, технологии», Московская школа управления СКОЛКОВО" width="1200" height="1698" loading="eager">
  </div>
</div>
</section>'''


def task():
    return f'''<section class="sk-task"><div class="sk__in sk-r">
<p class="sk__kicker">Задача</p>
<div class="sk-task__grid">
  <div>
    <p class="sk-task__quote">«Сверстать книгу, следуя брендбуку СКОЛКОВО.
      Переработать инфографику для лучшего восприятия».</p>
    <p class="sk__note">Формулировка брифа целиком. За ней стоял рукописный материал
      на шесть глав: авторы из Инжинирингового центра СПбПУ, Агентства по технологическому
      развитию и самой школы собрали опыт машиностроительных корпораций, но в виде текста
      он читался тяжело. Схемы приходили из разных источников, в разной стилистике
      и разного качества.</p>
  </div>
  <div>
    <div class="sk-task__box">
      <h3>Что сделали</h3>
      <p>Собрали макет на 86 полос A4: сетка в две колонки, наборный сериф издания,
        шмуцтитулы глав с косой лесенкой, колонтитулы с названием главы и сквозная
        нумерация рисунков.</p>
      <p>Перерисовали тридцать схем и таблиц в единой системе: одна палитра, один шрифт,
        одна логика подписей. Каждый рисунок подписан синим над картинкой и снабжён
        источником под ней.</p>
    </div>
    <div class="sk-task__box b2" style="margin-top:20px">
      <h3>Зачем это клиенту</h3>
      <p>Доклад работает раздаточным материалом образовательных программ школы
        по направлению Индустрии 4.0 и инструментом диагностики: по опросному листу
        из приложения предприятие считает свою цифровую зрелость.</p>
    </div>
  </div>
</div>
</div></section>'''


def system():
    sw = ''.join(f'<i style="background:{c}"></i>' for c in (WINE, RED, STEEL, '#D8DEE4'))
    return f'''<section class="sk-sys"><div class="sk__in sk-r">
<p class="sk__kicker">Графическая система</p>
<h2>Три цвета, косая полоса и синяя подпись</h2>
<p class="sk__lead" style="max-width:60ch">Брендбук школы задаёт немного: красный, бордо
  и сине-серый. Остальное держит наклон. Полосы под углом девять градусов работают
  и обложкой, и шмуцтитулом, и маркером уровня внутри схем.</p>
<div class="sk-sys__grid">
  <div class="sk-sys__card">
    <div class="sk-sys__swatch">{sw}</div>
    <h3>Палитра</h3>
    <p>Красный {RED} для акцента и первого плана, бордо {WINE} для плашек и заливок,
      сине-серый {STEEL} для второго плана и данных сравнения. Серый работает фоном
      схем, чтобы цветное читалось.</p>
  </div>
  <div class="sk-sys__card">
    <div class="sk-sys__type">
      <b>Заголовок</b>
      <em>А наборный текст идёт серифом в две колонки, с абзацным отступом
        и переносами.</em>
    </div>
    <h3>Типографика</h3>
    <p>Светлый гротеск в заголовках и шмуцтитулах, сериф в наборе. Кегль основного текста
      не меняется на протяжении всех 86 полос, схемы набраны узким гротеском.</p>
  </div>
  <div class="sk-sys__card">
    <div class="sk-sys__fig">Рисунок 7. 15 ключевых компонентов и систем
      современного производственного предприятия</div>
    <h3>Подписи</h3>
    <p>Каждый рисунок получил номер, подпись синим над картинкой и ссылку на источник
      под ней. Сквозная нумерация позволяет ссылаться на схему из любой главы,
      чем текст доклада активно пользуется.</p>
  </div>
</div>
</div></section>'''


def diffusion():
    mx = max(v for _, v, _ in DIFFUSION)
    rows = ''.join(
      f'<li class="sk-dif__row"><div class="sk-dif__hd"><b>{n}</b><i>{years}</i></div>'
      f'<div class="sk-dif__bar" style="--w:{v / mx * 100:.0f}%"><i></i></div>'
      f'<p class="sk__note" style="margin:8px 0 0;color:rgba(255,255,255,.55)">{note}</p></li>'
      for n, v, note in DIFFUSION
      for years in [f'{v} года' if v in (2, 3, 4) else f'{v} лет'])
    return f'''<section class="sk-dif"><div class="sk__in sk-r">
<p class="sk__kicker" style="color:#E4A0A6">Ускорение диффузии технологий</p>
<div class="sk-dif__grid">
  <div>
    <h2>Электричеству нужно было тридцать лет. Планшету три</h2>
    <p>Первая содержательная глава доклада отвечает на вопрос, почему разговор
      про цифровое производство стал срочным. Скорость, с которой технология доходит
      до большинства пользователей, за сто лет сжалась в десять раз.</p>
    <ul class="sk-dif__rows">{rows}</ul>
    <p class="sk__note" style="color:rgba(255,255,255,.5);margin-top:18px">
      Цифры из вступительного слова генерального директора Агентства
      по технологическому развитию Максима Шерейкина.</p>
  </div>
  <figure class="sk-dif__fig">
    <img src="{IMG}/fig-diffusion.jpg" alt="Рисунок 2 доклада: диффузия десяти потребительских технологий за 110 лет" width="1600" height="988" loading="lazy">
    <figcaption class="sk__cap" style="color:rgba(255,255,255,.55)">Рисунок 2: десять кривых
      от телефона до планшетов. Чем позже технология, тем вертикальнее её линия.</figcaption>
  </figure>
</div>
</div></section>'''


def components():
    leg = ''.join(f'<li><i style="background:{c}"></i>{n}. {t}</li>'
                  for (n, t, c) in GROUPS)
    cards = []
    for num, code, grp, name, body in COMPONENTS:
        col = GROUPS[grp][2]
        cards.append(
          f'<div class="sk-cmp__card">'
          f'<span class="sk-cmp__top"><span class="sk-cmp__num">{num:02d}</span>'
          f'<span class="sk-cmp__code" style="background:{col}"><span>{code}</span></span></span>'
          f'<h3>{name}</h3>'
          f'<div class="sk-cmp__body"><p>{body}</p></div></div>')
    return f'''<section class="sk-cmp"><div class="sk__in sk-r">
<p class="sk__kicker">Рисунок 7</p>
<h2>Сто технологий сведены к пятнадцати направлениям</h2>
<p class="sk__lead" style="max-width:62ch">Ключевая схема доклада и одновременно его
  оглавление. У каждого направления свой код, и дальше по этому коду его находят
  и в опросном листе, и в диаграмме зрелости, и в круговой диаграмме бенчмаркинга.</p>
<ul class="sk-cmp__legend">{leg}</ul>
<div class="sk-cmp__grid">{''.join(cards)}</div>
</div></section>'''


def odm3():
    rows = []
    for i, (num, code, grp, name, _) in enumerate(COMPONENTS):
        col = GROUPS[grp][2]
        steps = ''.join(
          f'<button type="button" data-seg="{i}" data-lv="{lv}" '
          f'aria-label="{code}, уровень {lv}">{lv}</button>' for lv in range(1, 6))
        rows.append(
          f'<li class="sk-odm__row" data-seg="{i}">'
          f'<code style="background:{col}"><span>{code}</span></code>'
          f'<span class="nm">{name}</span>'
          f'<span class="sk-odm__steps">{steps}</span></li>')
    lv = ''.join(
      f'<div class="sk-odm__lv" style="border-top-color:{c}"><b>{k}. {en}</b>'
      f'<i>{ru}</i><p>{txt}</p></div>'
      for (k, en, ru, txt), c in zip(LEVELS, ['#D8DEE4', '#C4CFD8', STEEL, WINE, RED]))
    return f'''<section class="sk-odm"><div class="sk__in sk-r">
<p class="sk__kicker">Рисунок 19, живая версия</p>
<h2>Модель зрелости ODM3: пятнадцать направлений, пять ступеней</h2>
<p class="sk__lead" style="max-width:64ch">В докладе диагностика занимает целую главу
  и приложение с опросным листом, а результат сводится в одну круговую диаграмму.
  Мы собрали её работающей: поставьте себе уровень по каждому направлению
  и посмотрите, как заполняется ромашка.</p>
<div class="sk-odm__grid">
  <div class="sk-fl">{flower()}
    <p class="sk__cap">Кольца считаются от центра: первое это Ad-Hoc, пятое Optimized.
      Цвет лепестка соответствует разделу опросного листа.</p>
  </div>
  <div>
    <div class="sk-odm__verdict" id="sk-verdict">
      <b>Оценка не заполнена</b>
      <p>Отметьте уровень хотя бы по одному направлению. Диагностику доклад советует
        проводить командой и сверять с отраслевым бенчмарком.</p>
    </div>
    <div class="sk-odm__ctl">
      <button class="sk-btn" type="button" id="sk-reset">Сбросить</button>
      <button class="sk-btn" type="button" id="sk-fill">Заполнить средним уровнем</button>
    </div>
    <ul class="sk-odm__rows">{''.join(rows)}</ul>
  </div>
</div>
<div class="sk-odm__levels">{lv}</div>
</div></section>'''


def book():
    items, thumbs = [], []
    for idx, (folio, chap, title, body) in enumerate(SPREADS):
        items.append(
          f'<div class="sk-book__item" data-i="{idx}">'
          f'<img src="{IMG}/spread-{folio:02d}.jpg" alt="Разворот {folio}-{folio + 1} доклада «Цифровое производство»: {title}" '
          f'width="2400" height="1698" loading="lazy" data-full="{IMG}/spread-{folio:02d}.jpg">'
          f'<div class="sk-book__meta"><span class="sk-book__folio">{folio}-{folio + 1}<br>{chap}</span>'
          f'<div><h3>{title}</h3><p>{body}</p></div></div></div>')
        thumbs.append(
          f'<button type="button" data-i="{idx}" aria-label="Разворот {folio}-{folio + 1}">'
          f'<img src="{IMG}/thumb-{folio:02d}.jpg" alt="" width="88" height="62" loading="lazy"></button>')
    return f'''<section class="sk-book"><div class="sk__in sk-r">
<p class="sk__kicker">Издание</p>
<h2>Двенадцать разворотов из восьмидесяти шести полос</h2>
<p class="sk__lead" style="max-width:62ch">Шмуцтитулы, схемы и приложение с опросным листом.
  Листайте вбок, клик по развороту открывает его целиком.</p>
</div>
<div class="sk__in"><div class="sk-book__track" id="sk-track">{''.join(items)}</div>
<div class="sk-book__thumbs" id="sk-thumbs">{''.join(thumbs)}</div></div>
</section>'''


def figures():
    cards = ''.join(
      f'<div class="sk-fig__card sk-r"><figure>'
      f'<img src="{IMG}/{f}" alt="{no} доклада «Цифровое производство»: {t}" loading="lazy" data-full="{IMG}/{f}">'
      f'<figcaption><span class="sk-fig__no">{no}</span><h3>{t}</h3><p>{d}</p></figcaption>'
      f'</figure></div>' for f, no, t, d in FIGURES)
    return f'''<section class="sk-fig"><div class="sk__in">
<div class="sk-r"><p class="sk__kicker">Инфографика</p>
<h2>Одиннадцать схем из тридцати</h2>
<p class="sk__lead" style="max-width:64ch">Часть схем приходила от авторов скриншотами
  из презентаций, часть существовала только в виде абзаца текста. Перерисовали все
  в одной системе: сквозная нумерация, синяя подпись сверху, источник снизу.</p></div>
<div class="sk-fig__grid">{cards}</div>
</div></section>'''


def mockups():
    return f'''<section class="sk-mock"><div class="sk__in sk-r">
<p class="sk__kicker">В печати</p>
<h2>Как это выглядит на бумаге</h2>
<div class="sk-mock__grid">
  <figure><img src="{IMG}/mock-cover.png" alt="Обложка доклада «Цифровое производство» в печати" loading="lazy"></figure>
  <figure><img src="{IMG}/mock-stack.png" alt="Раскрытый доклад и обложка следующей редакции издания" loading="lazy"></figure>
  <figure class="wide"><img src="{IMG}/mock-spread.png" alt="Разворот 40-41: диаграммы зрелости и метасистема EIM" loading="lazy"></figure>
  <figure class="wide"><img src="{IMG}/mock-charts.png" alt="Разворот с диаграммами уровня цифровизации продуктов и отраслей" loading="lazy"></figure>
</div>
</div></section>'''


def result():
    cards = [
      ('Концепция и макет', 'Сетка на две колонки, шмуцтитулы глав, колонтитулы, '
       'сквозная нумерация рисунков и таблиц.'),
      ('Инфографика', 'Тридцать схем и таблиц в единой системе, включая круговую '
       'диаграмму зрелости и карту метасистемы EIM.'),
      ('Вёрстка 86 полос', 'Полный набор с приложениями: опросный лист диагностики, '
       'список из 46 источников, авторы и партнёры.'),
      ('Препресс', 'Файл под печать и электронная редакция, которая обновляется '
       'вместе с новыми выпусками доклада.'),
    ]
    cs = ''.join(f'<div class="sk-res__card"><b>{t}</b><p>{d}</p></div>' for t, d in cards)
    ph = ''.join(f'<img src="{IMG}/photo-{i}.jpg" alt="Фотография с обложки доклада: цифровое производство" loading="lazy">'
                 for i in (3, 2, 1, 4))
    return f'''<section class="sk-res"><div class="sk__in sk-r">
<p class="sk__kicker">Состав работ</p>
<h2>Издание, которое читают не по диагонали</h2>
<p class="sk__lead" style="max-width:62ch">Доклад вышел в октябре 2017 года и дальше
  переиздавался: следующая редакция появилась уже в 2018-м, с тем же макетом
  и обновлёнными данными.</p>
<div class="sk-res__grid">{cs}</div>
<div class="sk-res__ph">{ph}</div>
</div></section>'''


LIGHTBOX = ('<div class="sk-lb" id="sk-lb" role="dialog" aria-modal="true" aria-label="Просмотр">'
            '<button class="sk-lb__x" type="button" aria-label="Закрыть">&times;</button>'
            '<img src="" alt=""></div>')

PAGE_JS = """<script>(function(){
  var LEVELS=%LEVELS%;
  // появление секций
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('on'); io.unobserve(e.target);} });
  },{rootMargin:'0px 0px -8% 0px'}):null;
  var rs=document.querySelectorAll('.sk-r,.sk-dif');
  if(io){ rs.forEach(function(n){io.observe(n)}); }
  else { rs.forEach(function(n){n.classList.add('on')}); }
  // страховка: если наблюдатель не отработал (скрытая вкладка), показываем через 1.2 с
  setTimeout(function(){ rs.forEach(function(n){n.classList.add('on')}); },1200);

  // ромашка ODM3
  var state=new Array(15).fill(0);
  var cells=document.querySelectorAll('.sk-fl__cell');
  var labels=document.querySelectorAll('.sk-fl__lb');
  var rows=document.querySelectorAll('.sk-odm__row');
  var score=document.querySelector('.sk-fl__score');
  var grade=document.querySelector('.sk-fl__grade');
  var verdict=document.getElementById('sk-verdict');
  function paint(){
    cells.forEach(function(c){
      var s=+c.dataset.seg, l=+c.dataset.lv;
      c.classList.toggle('on', l<=state[s]);
    });
    labels.forEach(function(t){ t.classList.toggle('on', state[+t.dataset.seg]>0); });
    rows.forEach(function(r){
      var s=+r.dataset.seg;
      r.classList.toggle('hl', state[s]>0);
      r.querySelectorAll('.sk-odm__steps button').forEach(function(b){
        b.classList.toggle('on', +b.dataset.lv<=state[s]);
      });
    });
    var filled=state.filter(function(v){return v>0});
    if(!filled.length){
      score.textContent='0.0'; grade.textContent='балл';
      verdict.innerHTML='<b>Оценка не заполнена</b><p>Отметьте уровень хотя бы по одному '+
        'направлению. Диагностику доклад советует проводить командой и сверять '+
        'с отраслевым бенчмарком.</p>';
      return;
    }
    var avg=filled.reduce(function(a,b){return a+b},0)/filled.length;
    score.textContent=avg.toFixed(1);
    grade.textContent=filled.length+' из 15';
    var idx=Math.min(4,Math.max(0,Math.round(avg)-1));
    var L=LEVELS[idx];
    verdict.innerHTML='<b>'+L[0]+'. '+L[1]+', '+L[2]+'</b><p>'+L[3]+'</p>';
  }
  function set(seg,lv){ state[seg]=(state[seg]===lv)?lv-1:lv; paint(); }
  cells.forEach(function(c){ c.addEventListener('click',function(){ set(+c.dataset.seg,+c.dataset.lv); }); });
  document.querySelectorAll('.sk-odm__steps button').forEach(function(b){
    b.addEventListener('click',function(){ set(+b.dataset.seg,+b.dataset.lv); });
  });
  var rst=document.getElementById('sk-reset');
  if(rst) rst.addEventListener('click',function(){ state=new Array(15).fill(0); paint(); });
  var fil=document.getElementById('sk-fill');
  if(fil) fil.addEventListener('click',function(){ state=new Array(15).fill(3); paint(); });
  paint();

  // листалка
  var track=document.getElementById('sk-track');
  var thumbs=document.getElementById('sk-thumbs');
  if(track&&thumbs){
    var items=track.querySelectorAll('.sk-book__item');
    var btns=thumbs.querySelectorAll('button');
    btns.forEach(function(b){
      b.addEventListener('click',function(){
        var it=items[+b.dataset.i];
        track.scrollTo({left:it.offsetLeft-(track.clientWidth-it.clientWidth)/2,behavior:'smooth'});
      });
    });
    var mark=function(){
      var c=track.scrollLeft+track.clientWidth/2, best=0, bd=1e9;
      items.forEach(function(it,i){
        var d=Math.abs(it.offsetLeft+it.clientWidth/2-c);
        if(d<bd){bd=d;best=i;}
      });
      btns.forEach(function(b,i){ b.classList.toggle('on',i===best); });
    };
    track.addEventListener('scroll',function(){ window.requestAnimationFrame(mark); });
    mark();
  }

  // лайтбокс
  var lb=document.getElementById('sk-lb'), lbi=lb?lb.querySelector('img'):null;
  document.querySelectorAll('img[data-full]').forEach(function(im){
    im.addEventListener('click',function(){
      if(!lb) return;
      lbi.src=im.dataset.full; lbi.alt=im.alt; lb.classList.add('on');
      document.body.style.overflow='hidden';
    });
  });
  function close(){ if(!lb) return; lb.classList.remove('on'); lbi.src=''; document.body.style.overflow=''; }
  if(lb){ lb.addEventListener('click',close);
    document.addEventListener('keydown',function(e){ if(e.key==='Escape') close(); }); }
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Доклад «Цифровое производство» для СКОЛКОВО",'
  f'"item":"{URL}"}}]}}</script>')


def build():
    js = PAGE_JS.replace('%LEVELS%', str([[k, en, ru, txt] for k, en, ru, txt in LEVELS])
                         .replace("'", '"'))
    # Отдельного CTA нет: фиолетовая форма из rc.footer() закрывает страницу
    body = (f'{rc.header()}<main class="sk">{hero()}{task()}{system()}{diffusion()}'
            f'{components()}{odm3()}{book()}{figures()}{mockups()}{result()}'
            f'</main>{LIGHTBOX}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'skolkovo')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    # index-a2.html — старая запечённая Tilda-страница; если её оставить,
    # CI зальёт именно её и кастомная страница пропадёт
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', os.path.join(out, 'index.html'))
