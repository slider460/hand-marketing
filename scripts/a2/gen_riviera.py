#!/usr/bin/env python3
"""Генерит mirror/event/riviera/index.html: кейс «Внутри стихии», передача
помещения ТРЦ Ривьера под отделку якорному арендатору «Ашан Сити» (2015).

Идея страницы: у проекта есть собственный графический знак, четыре набора
линий на бейджах, флаконах, навигации и кирпичах. Это одна и та же кривая с
разной амплитудой и поворотом: прямая это земля, лёгкая рябь воздух, крупная
волна вода, та же волна на боку огонь. Поэтому знак на странице не картинка,
а живой SVG: пульт стихий перерисовывает линии и одновременно переводит
стихию в инженерную систему здания, ради которой метафора и бралась.

Дальше страница идёт по документам проекта:
  • бриф от 05.06.2015 (задача, аудитория, KPI 75+ при базе 320);
  • предложение от 22.06.2015 (концепция, сценарий, смета по статьям);
  • финальный отчёт (репортаж вечера, макеты, выводы).
Отдельный блок сравнивает предложение с тем, что реально произошло 1 октября.

Ассеты: mirror/images/riviera/ (scripts/riviera-assets.py).

НЕ публикуем: рубли сметы и agency fee (только доли статей), имена и контакты
сотрудников клиента из контакт-репорта, персональные данные гостей.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/riviera'
URL = 'https://hand-marketing.ru/event/riviera/'

# ─── стихии: ключ, имя, цвет, параметры знака, инженерная система ────────────
# цвета сняты пипеткой с финальных бейджей, амплитуда и поворот с самих знаков
ELEMENTS = [
    ('earth', 'Земля', '#63A927', 0.0, 0,
     'Освоить землю', 'поставить фундамент и стены',
     'К октябрю каркас комплекса стоял целиком. Гости шли по этажам, где были '
     'только бетон и разметка, и это работало лучше любого рендера: здание '
     'существует, его можно потрогать.'),
    ('air', 'Воздух', '#00AECE', 2.3, 0,
     'Наполнить воздухом', 'установить вентиляцию и кондиционирование',
     'Вентиляция уже была смонтирована и висела над головой на всём маршруте '
     'экскурсии. Серебристые короба на потолке стали частью декораций.'),
    ('water', 'Вода', '#2F7DC4', 4.8, 0,
     'Запустить воду', 'провести водопровод и канализацию',
     'Инженерия, которую арендатор проверяет первой, когда считает, встанет ли '
     'у него кухня или примерочная. На вечере это была тема номер один в '
     'разговорах у фуршетных островов.'),
    ('fire', 'Огонь', '#B80066', 4.8, -90,
     'Зажечь огонь', 'отладить отопление и освещение',
     'Отопления на площадке ещё не было, поэтому в зале работали газовые '
     'тепловые пушки, а свет ставили мы. Единственная стихия, которую на этом '
     'вечере полностью привезли с собой.'),
]

# ─── бриф от 05.06.2015 ─────────────────────────────────────────────────────
BRIEF = [
    ('Повод', 'Передача первого помещения под отделку якорному арендатору '
     '«Ашан Сити». Формальная процедура, которую нужно было превратить в '
     'публичное доказательство сроков.'),
    ('Аудитория', 'Первые лица российских и западных компаний, которые решают '
     'об аренде коммерческой недвижимости, плюс профильные СМИ.'),
    ('Что требовалось', 'Подтвердить сроки открытия, показать уровень комплекса '
     'и подготовить почву для будущих переговоров об аренде.'),
    ('Что делает агентство', 'Всё: концепцию и её элементы, приглашения, '
     'сценарий, оформление, технику, кейтеринг, сувениры и обзвон базы.'),
]

# ─── сценарий вечера по отчёту ──────────────────────────────────────────────
EVENING = [
    ('17:00', 'welcome-hostess', 'Встреча',
     'Гостей встречают девушки в платьях фирменного бирюзового цвета. Каждый '
     'получает именной бейдж со знаком одной из четырёх стихий, и этот знак '
     'потом определит, в какой группе человек пойдёт на экскурсию.',
     'Хостес в бирюзовых платьях у стойки регистрации с бейджами'),
    ('17:20', 'welcome-drink', 'Сбор',
     'На главной площадке напитки и лёгкие закуски, на экранах фоновая '
     'заставка, спокойная музыка. Всё это происходит на бетонном полу '
     'недостроенного торгового центра, между колонн со строительной '
     'разметкой.',
     'Официант с приветственными напитками среди гостей на строительной площадке'),
    ('17:40', 'host', 'Открытие',
     'Ведущий открывает вечер рассказом о четырёх стихиях и о том, что за ними '
     'стоит в языке стройки. Дальше слово берёт команда ТРЦ.',
     'Ведущий с микрофоном на фоне экрана с водой'),
    ('18:00', 'stage-award', 'Передача помещений',
     'Официальная часть заканчивается церемонией: помещения передают якорным '
     'арендаторам. Ради этой минуты и собирали вечер, дальше её пересказывают '
     'в СМИ и в переговорах с другими арендаторами.',
     'Церемония передачи помещений на сцене'),
    ('18:30', 'tour-amulet', 'Следуйте за своим знаком',
     'Ведущий приглашает гостей «следовать своим амулетам». Знак стихии с '
     'бейджа превращается в табличку в руках сопровождающего, и зал делится '
     'на группы без единого списка и переклички.',
     'Гостья с бирюзовой табличкой «Воздух» на экскурсии'),
    ('18:45', 'tour-arch', 'Экскурсия',
     'Пешеходный маршрут проходит через две зоны со звуковыми иллюзиями. В '
     'зоне будущего кинотеатра звучат блокбастеры, в зоне фуд-корта шум '
     'ресторанного дворика. Пустой бетон начинает звучать так, каким он станет '
     'после открытия.',
     'Группа гостей в касках под арками галереи комплекса'),
    ('19:30', 'drummers', 'Шоу',
     'После возвращения гостей идёт 3D mapping на трёх экранах обратной '
     'проекции, собранных в одну композицию. Вечер закрывает барабанный '
     'коллектив Vasiliev Groove.',
     'Барабанщики Vasiliev Groove на сцене'),
    ('20:00', 'catering', 'Четыре острова',
     'Фуршет разложен на четыре линии по стихиям, у каждой своё меню: земля с '
     'чёрным пармезаном и хумусом, воздух с азотным сорбетом, вода с '
     'морепродуктами, огонь с блинчиками фламбе, которые поджигают при гостях.',
     'Фуршетные острова с гостями в зале'),
    ('21:00', 'umbrella-gift', 'Выход',
     'На выходе каждому вручают зонт с логотипом ТРЦ. Предмет, который в '
     'октябре в Москве достают из машины на следующий же день.',
     'Хостес у стола с зонтами ТРЦ Ривьера'),
]

# ─── предложение 22.06 против того, что было 01.10 ──────────────────────────
DIFF = [
    ('Дата', '3 сентября, 17:30 до 20:00',
     '1 октября, 17:00 до 21:00',
     'Сроки стройки сдвинулись, вместе с ними уехало и мероприятие. Вечер стал '
     'на полтора часа длиннее.'),
    ('Выбор стихии', 'Тест на планшете при входе: гость отвечает на несколько '
     'вопросов и получает свою стихию',
     'Знак стихии напечатан на именном бейдже заранее',
     'Регистрация 198 человек с планшетами растянула бы вход. Персонализацию '
     'перенесли в печать, и очередь на входе исчезла.'),
    ('Экскурсия', 'Четыре маршрута, шесть зон со звуковыми иллюзиями',
     'Один маршрут, две звуковые зоны: кинотеатр и фуд-корт',
     'Готовых к проходу зон на площадке оказалось меньше, чем в июне. Вместо '
     'шести слабых сцен сделали две, которые точно читаются.'),
    ('Барабанщики', 'Появляются по одной стихии на эскалаторах во время '
     'церемонии',
     'Отдельный номер в финале вечера после 3D mapping',
     'Эскалаторы к октябрю ещё не запустили. Номер перенесли в конец, где он '
     'держит внимание сам по себе.'),
    ('Оформление площадки', 'Гранит, дым-машина, аквариумы с рыбками, лазеры',
     'Свет, проекция на трёх экранах и сама стройка как декорация',
     'Бетон, арматура и подсветка колонн оказались сильнее реквизита. Бюджет '
     'ушёл в свет и звук, это самая большая статья после кейтеринга.'),
    ('Подарок', 'Аромат выбранной стихии в фирменной упаковке',
     'Зонт с логотипом ТРЦ',
     'Аромат работает дома у гостя, зонт работает на улице и попадается на '
     'глаза каждому. Для повода, где нужна узнаваемость комплекса, выбрали '
     'второе.'),
]

# ─── макеты: (файл, подпись, статус, комментарий) ───────────────────────────
INVITES = [
    ('inv-wave-ru', 'Волна, русская версия', 'work',
     'Рассылка шла за две недели до вечера на двух языках. Русская версия '
     'собрала программу в короткий список: церемония, экскурсия, программа, '
     'фуршет и подарки.'),
    ('inv-wave-en', 'Волна, английская версия', 'work',
     'Тот же макет для западных компаний. Знак стихий в шапке ведёт себя как '
     'логотип события и дальше повторяется на бейдже, навигации и баннере.'),
    ('inv-deep', 'Глубина', 'draft',
     'Первый вариант: тёмная вода и пузыри воздуха. Читается как приглашение '
     'на погружение, но плохо переносил длинный текст программы.'),
    ('inv-sunset', 'Закат', 'draft',
     'Вариант с песком и водой на рассвете. Красивый, но слишком спокойный '
     'для повода, который должен доказывать темп стройки.'),
]

BADGES = [
    ('badge-flat', 'Знак стихии и цветная плашка', 'work',
     'Финальная версия. Знак крупно, фамилия и компания на белом, цвет плашки '
     'повторяет стихию. Такой бейдж читается на расстоянии вытянутой руки, а '
     'на экскурсии работает пропуском в свою группу.'),
    ('badge-aqua', 'Акварельные стихии', 'draft',
     'Каждой стихии своя иллюстрация: пламя, листья, волна, перо. Красиво в '
     'руках, но имя тонет в рисунке.'),
    ('badge-pocket', 'Карман с цветной вкладкой', 'draft',
     'Стандартный карман и вкладыш под цвет стихии. Дёшево в производстве, '
     'ничего не добавляет к вечеру.'),
    ('badge-tassel', 'Кисти по цвету стихии', 'draft',
     'Стихию отмечает цветная кисть на шнуре. Заметно издалека, но путается '
     'и цепляется за одежду.'),
    ('badge-cord', 'Шнуры-браслеты', 'draft',
     'Цветной шнур вместо ленты, потом остаётся на руке как браслет. '
     'Сувенирная идея, для стойки регистрации на 198 человек слишком медленная.'),
]

KEYS = [
    ('key-frame', 'Ключ-визитка в раме',
     'Ключ вырезан из плотного картона, на бородке волны знака, на головке '
     'логотипы «Ашан» и ТРЦ. В раме под стекло, чтобы повесить в офисе.'),
    ('key-usb', 'Флешка в форме ключа',
     'Внутри презентация комплекса и планировки. Ключ, который остаётся в '
     'связке и открывает файлы, а не дверь.'),
    ('key-capsule', 'Капсула с грамотой',
     'Металлическая туба с сертификатом о передаче помещения. Вручается с '
     'сцены и хорошо читается в кадре.'),
    ('key-box-open', 'Куб с якорем',
     'Белый куб, внутри серебряный якорь. Якорь как якорный арендатор, шутка '
     'ровно того уровня, который считывают на такой сцене.'),
    ('key-box-pair', 'Куб с запонками',
     'Тот же куб в закрытом виде и с парой запонок-якорей. Подарок первому '
     'лицу компании, а не отделу.'),
]

SOUVENIR = [
    ('helmet-c', 'Каски с логотипом', 'work',
     'Без каски на площадку не пускают, поэтому каска стала носителем: '
     'бирюзовый знак на белом, свой знак стихии сбоку. На фотографиях вечера '
     'она в каждом кадре.'),
    ('gift-umbrella', 'Зонт', 'work',
     'Финальный подарок на выходе. Октябрь, Москва, зонт с логотипом уезжает '
     'с гостем и работает дальше сам.'),
    ('gift-aroma', 'Аромат стихии', 'draft',
     'Диффузор и флаконы четырёх цветов, у каждого свой знак. Красивая '
     'история про то, что стихия остаётся с гостем дома.'),
    ('presswall', 'Пресс-волл', 'work',
     'Паттерн из логотипов на двух языках, 2 на 3 метра. Работал точкой сбора: '
     'общее фото команды вечера снято именно у него.'),
    ('banner-street', 'Уличный баннер', 'work',
     'Четыре на полтора метра на въезде. Знак стихий в ряд и название события '
     'без пояснений: к моменту приезда гость уже знает, что такое «Внутри '
     'стихии».'),
    ('navigation', 'Навигация', 'work',
     'Мобильные указатели по площадке. По выводам отчёта их оказалось мало: '
     'на такой объём нужна отдельная команда навигации.'),
]

# ─── смета по статьям, только доли ──────────────────────────────────────────
BUDGET = [
    ('Кейтеринг', 36, 'Приветственный коктейль и четыре фуршетных острова со '
     'своим меню у каждого.'),
    ('Свет и звук', 22, 'Три экрана обратной проекции, световой парк на всю '
     'площадку, звук на зал и на маршрут экскурсии.'),
    ('Закупки и производство', 18, 'Бейджи, каски, навигация, пресс-волл, '
     'баннер, подарки.'),
    ('Персонал', 15, 'Хостес, супервайзеры, хелперы, техники, фото и видео.'),
    ('Ролик', 9, 'Съёмка площадки и монтаж видео для экранов.'),
    ('Дизайн', 1, 'Приглашения, бейджи, навигация, макеты производства.'),
]

# ─── команда ────────────────────────────────────────────────────────────────
TEAM = [
    ('Агентство', 7, 'Менеджер по работе с клиентами, координатор, креативный '
     'директор, менеджер производства, HR, дизайнер, юрист.'),
    ('На площадке', 14, 'Ведущий, четыре хостес, два супервайзера, три хелпера, '
     'фотограф, два техника, звукорежиссёр, видеооператор.'),
    ('Артисты', 5, 'Барабанный коллектив и администратор.'),
    ('Кейтеринг', 15, 'Менеджер, шесть официантов, четыре повара, подсобные '
     'рабочие.'),
]

# ─── CPS: направление, недели (от 26-й), подпись ────────────────────────────
CPS = [
    ('Тендер', 26, 27, 'Драфт презентации, вопросы клиента, согласование '
     'программы и выбор агентства.'),
    ('Документация', 27, 36, 'Договор, три этапа оплаты, закрывающие документы.'),
    ('Рабочая документация', 27, 28, 'Доработка предложения по комментариям, '
     'рабочая документация проекта и сам этот график.'),
    ('Персонал', 28, 34, 'Рекрутинг, кастинг, согласование с клиентом и тренинг '
     'перед вечером.'),
    ('Ролик', 30, 34, 'Согласование ТЗ, съёмка площадки с дрона, монтаж, '
     'утверждение.'),
    ('Производство', 28, 33, 'Подарки, промоформа хостес, оформление площадки.'),
    ('Оборудование', 28, 36, 'Брифинг технической службы, расчёт мощности, '
     'букинг, логистика, монтаж и демонтаж.'),
    ('Мероприятие', 36, 36, 'Один вечер, к которому вели одиннадцать недель.'),
]

# ─── выводы из отчёта ───────────────────────────────────────────────────────
LEARNINGS = [
    ('Креатив после брифа', 'Разрабатывать концепцию имеет смысл только после '
     'брифа, и референсы от клиента этому помогают, а не мешают.'),
    ('Станция регистрации на каждые 70 человек', 'При именных бейджах одна '
     'стойка на 198 гостей превращается в очередь. Нужна автономная станция на '
     'каждые семьдесят человек.'),
    ('Отдельная команда навигации', 'На объекте такого размера указателей мало, '
     'нужны живые люди на развилках маршрута.'),
    ('Одна встреча всех согласантов', 'Контент вечера должны утверждать все '
     'причастные за один раз, иначе правки приходят по кругу.'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

PAGE_CSS = """<style id="rv-css">
:root{
 --rv-cyan:#00B5D4;--rv-earth:#63A927;--rv-air:#00AECE;--rv-water:#2F7DC4;--rv-fire:#B80066;
 --rv-gold:#C7A70A;
 --rv-bg:#101316;--rv-bg2:#171b20;--rv-card:#1c2127;--rv-line:rgba(255,255,255,.12);
 --rv-ink:#eef2f5;--rv-ink2:#9aa5b1;
 --rv-df:'Raleway',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --rv-bf:'Onest',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --rv-mf:'JetBrains Mono',ui-monospace,SFMono-Regular,Consolas,monospace;
 --rv-el:var(--rv-air)}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.rv{font-family:var(--rv-bf);color:var(--rv-ink);background:var(--rv-bg);line-height:1.62;
 font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.rv *{box-sizing:border-box}
.rv img{max-width:100%;height:auto;display:block}
.rv a{color:inherit}
/* дисплейная гарнитура повторяет тонкий широкий гротеск логотипа ТРЦ */
.rv h1,.rv h2,.rv h3{font-family:var(--rv-df);font-weight:200;line-height:1.06;
 letter-spacing:-.005em;margin:0;text-wrap:balance}
.rv p{text-wrap:pretty}
.rv-w{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,52px)}
.rv-sec{padding:clamp(56px,8vw,110px) 0}
.rv-sec--alt{background:var(--rv-bg2)}
.rv-kick{font-family:var(--rv-mf);font-weight:700;font-size:11.5px;letter-spacing:.16em;
 text-transform:uppercase;display:inline-flex;align-items:center;gap:10px;color:var(--rv-ink2)}
.rv-kick::before{content:"";width:26px;height:2px;background:var(--rv-el);transition:background .5s}
.rv-h2{font-size:clamp(28px,4.2vw,52px);margin:clamp(14px,1.8vw,20px) 0 0;max-width:20ch}
.rv-h3{font-size:clamp(21px,2.4vw,30px)!important;max-width:32ch}
.rv-lead{margin:clamp(14px,1.8vw,20px) 0 0;font-size:clamp(16px,1.35vw,19px);color:#c3ccd5;
 max-width:62ch}
.rv-btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--rv-bf);
 font-weight:700;font-size:15px;padding:.95em 1.5em;border:0;cursor:pointer;border-radius:999px;
 text-decoration:none;transition:transform .25s,background .25s,color .25s,border-color .25s}
.rv-btn svg{width:1.1em;height:1.1em}
.rv a.rv-btn--p,.rv-btn--p{background:var(--rv-cyan);color:#06181d}
.rv-btn--p:hover{transform:translateY(-2px);background:#3fd0e8}
.rv a.rv-btn--gh,.rv-btn--gh{background:transparent;color:var(--rv-ink);
 border:2px solid var(--rv-line)}
.rv-btn--gh:hover{border-color:var(--rv-cyan);transform:translateY(-2px)}
.rv-r{opacity:0;transform:translateY(18px);transition:opacity .7s,transform .7s}
.rv-r.is-in{opacity:1;transform:none}

/* ── ГЕРОЙ ── */
.rv-hero{position:relative;padding:clamp(26px,4vw,50px) 0 clamp(40px,6vw,72px);
 background:radial-gradient(120% 90% at 78% 8%,rgba(0,181,212,.16),transparent 62%),
 linear-gradient(180deg,#0c0f12,var(--rv-bg))}
.rv-hero__grid{display:grid;grid-template-columns:1.06fr .94fr;gap:clamp(26px,4.5vw,60px);
 align-items:center}
.rv-hero__client{display:flex;align-items:center;gap:16px;margin-bottom:clamp(18px,2.4vw,26px)}
.rv-hero__client img{width:clamp(132px,14vw,178px)}
.rv-hero__client span{font-family:var(--rv-mf);font-size:11px;letter-spacing:.13em;
 text-transform:uppercase;color:var(--rv-ink2);border-left:1px solid var(--rv-line);
 padding-left:16px;line-height:1.5}
.rv-hero h1{font-size:clamp(40px,7.2vw,90px);letter-spacing:.02em}
.rv-hero h1 b{font-weight:200;color:var(--rv-el);transition:color .5s}
.rv-hero__sub{margin:clamp(16px,2vw,24px) 0 0;font-size:clamp(16px,1.4vw,19px);
 color:#c3ccd5;max-width:52ch}
.rv-chips{display:flex;flex-wrap:wrap;gap:8px;margin:clamp(18px,2.2vw,26px) 0 0;padding:0;
 list-style:none}
.rv-chips li{padding:6px 14px;border:1px solid var(--rv-line);border-radius:999px;
 font-size:12.5px;font-weight:600;color:var(--rv-ink2)}
.rv-hero__cta{margin-top:clamp(20px,2.6vw,30px);display:flex;gap:12px;flex-wrap:wrap}

/* пульт стихий: живой знак вместо картинки */
.rv-sign{background:linear-gradient(160deg,#1a2027,#12161a);border:1px solid var(--rv-line);
 border-radius:26px;padding:clamp(20px,2.6vw,30px);position:relative;overflow:hidden}
.rv-sign::after{content:"";position:absolute;inset:auto -30% -55% -30%;height:70%;
 background:radial-gradient(50% 50% at 50% 50%,var(--rv-el),transparent 70%);opacity:.2;
 transition:background .5s;pointer-events:none}
.rv-sign__art{aspect-ratio:1/.78;display:grid;place-items:center}
.rv-sign__art svg{width:min(64%,250px);height:auto;overflow:visible}
.rv-sign__art path{fill:none;stroke:var(--rv-el);stroke-width:3.6;stroke-linecap:round;
 transition:stroke .5s}
.rv-sign__tabs{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;position:relative;z-index:1}
.rv-sign__tabs button{cursor:pointer;background:transparent;border:1px solid var(--rv-line);
 border-radius:12px;padding:10px 6px;font:600 13px var(--rv-bf);color:var(--rv-ink2);
 transition:border-color .2s,color .2s,background .2s}
.rv-sign__tabs button:hover{color:var(--rv-ink)}
.rv-sign__tabs button[aria-pressed=true]{color:#06181d;background:var(--rv-el);
 border-color:var(--rv-el)}
.rv-sign__cap{margin:clamp(16px,2vw,22px) 0 0;position:relative;z-index:1;min-height:8.6em}
.rv-sign__cap dt{font-family:var(--rv-df);font-weight:300;font-size:clamp(19px,2vw,25px);
 line-height:1.15;color:var(--rv-ink)}
.rv-sign__cap dt i{display:block;font-style:normal;font-size:.82em;color:var(--rv-el);transition:color .5s;margin-top:4px}
.rv-sign__cap dd{margin:10px 0 0;font-size:14.5px;color:var(--rv-ink2);line-height:1.6}

/* ── цифры ── */
.rv-nums{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(12px,2vw,26px);
 margin-top:clamp(30px,4vw,52px);border-top:1px solid var(--rv-line);padding-top:clamp(22px,3vw,34px)}
.rv-nums dt{font-family:var(--rv-df);font-weight:200;font-size:clamp(30px,4.6vw,56px);
 line-height:1;letter-spacing:-.01em}
.rv-nums dd{margin:8px 0 0;font-size:13.5px;color:var(--rv-ink2);line-height:1.45}

/* ── бриф ── */
.rv-brief{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,72px);align-items:start}
.rv-brief__list{margin:0;padding:0}
.rv-brief__list>div{padding:clamp(18px,2.4vw,26px) 0;border-top:1px solid var(--rv-line)}
.rv-brief__list>div:first-child{border-top:0;padding-top:0}
.rv-brief__list dt{font-family:var(--rv-mf);font-size:11.5px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--rv-cyan)}
.rv-brief__list dd{margin:10px 0 0;color:#c3ccd5}
.rv-figure figcaption{margin-top:12px;font-size:13.5px;color:var(--rv-ink2)}
.rv-figure img{border-radius:16px}

/* ── идея ── */
.rv-idea__quote{font-family:var(--rv-df);font-weight:200;font-size:clamp(22px,3vw,38px);
 line-height:1.22;max-width:22ch;margin:0}
.rv-bricks{margin:clamp(26px,4vw,44px) 0 0}
.rv-el-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(12px,1.8vw,20px);
 margin-top:clamp(26px,4vw,44px)}
.rv-el-card{background:var(--rv-card);border:1px solid var(--rv-line);border-radius:18px;
 padding:clamp(18px,2.2vw,26px);border-top:3px solid var(--c)}
.rv-el-card svg{width:52px;height:52px;overflow:visible}
.rv-el-card svg path{fill:none;stroke:var(--c);stroke-width:4.2;stroke-linecap:round}
.rv-el-card h3{font-size:clamp(17px,1.6vw,21px);font-weight:300;margin:16px 0 0}
.rv-el-card b{display:block;font:600 13px/1.5 var(--rv-bf);color:var(--c);margin-top:6px}
.rv-el-card p{margin:12px 0 0;font-size:14.5px;color:var(--rv-ink2)}

/* ── вечер ── */
.rv-ev{display:grid;grid-template-columns:clamp(200px,22vw,264px) 1fr;
 gap:clamp(24px,3.4vw,48px);margin-top:clamp(30px,4vw,50px);align-items:start}
.rv-ev__nav{position:sticky;top:96px;display:flex;flex-direction:column;gap:2px;margin:0;
 padding:0;list-style:none}
.rv-ev__nav button{width:100%;text-align:left;cursor:pointer;background:transparent;border:0;
 border-left:2px solid var(--rv-line);padding:11px 16px;color:var(--rv-ink2);
 font:600 14.5px var(--rv-bf);display:flex;gap:12px;transition:color .2s,border-color .2s}
.rv-ev__nav button time{font:600 12px var(--rv-mf);opacity:.7;padding-top:2px}
.rv-ev__nav button:hover{color:var(--rv-ink)}
.rv-ev__nav button[aria-selected=true]{color:var(--rv-cyan);border-color:var(--rv-cyan)}
.rv-ev__panel[hidden]{display:none}
.rv-ev__panel img{border-radius:18px;width:100%}
.rv-ev__body{display:grid;grid-template-columns:auto 1fr;gap:clamp(16px,2.4vw,30px);
 margin-top:clamp(16px,2vw,24px);align-items:start}
.rv-ev__body h3{font-size:clamp(21px,2.4vw,30px);font-weight:300}
.rv-ev__body time{font-family:var(--rv-mf);font-size:13px;color:var(--rv-cyan);
 letter-spacing:.06em}
.rv-ev__body p{margin:12px 0 0;color:#c3ccd5;max-width:56ch}

/* ── видео ── */
.rv-video{margin-top:clamp(30px,4vw,50px);border-radius:20px;overflow:hidden;
 border:1px solid var(--rv-line);background:#000}
.rv-video video{width:100%;display:block}

/* ── план против факта ── */
.rv-diff{margin-top:clamp(28px,4vw,46px);border-top:1px solid var(--rv-line)}
.rv-diff__row{display:grid;grid-template-columns:clamp(120px,14vw,180px) 1fr 1fr;
 gap:clamp(14px,2.4vw,32px);padding:clamp(20px,2.6vw,30px) 0;
 border-bottom:1px solid var(--rv-line);align-items:start}
.rv-diff__k{font-family:var(--rv-mf);font-size:11.5px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--rv-ink2);padding-top:4px}
.rv-diff__cell{font-size:15.5px;line-height:1.55}
.rv-diff__cell b{display:block;font:700 10.5px/1 var(--rv-mf);letter-spacing:.16em;
 text-transform:uppercase;margin-bottom:9px}
.rv-diff__cell--plan{color:var(--rv-ink2)}
.rv-diff__cell--plan b{color:var(--rv-ink2)}
.rv-diff__cell--fact b{color:var(--rv-cyan)}
.rv-diff__why{grid-column:2/-1;margin:10px 0 0;font-size:14px;color:var(--rv-ink2);
 border-left:2px solid var(--rv-line);padding-left:14px}

/* ── дизайн: варианты и выбранное ── */
.rv-pick{margin-top:clamp(26px,3.4vw,42px);display:grid;
 grid-template-columns:1fr clamp(210px,24vw,290px);gap:clamp(20px,3vw,40px);align-items:start}
.rv-pick__stage{background:var(--rv-card);border:1px solid var(--rv-line);border-radius:20px;
 padding:clamp(16px,2.4vw,30px)}
.rv-pick__shot{display:grid;place-items:center;background:#fff;border-radius:14px;
 padding:clamp(12px,2vw,24px);min-height:clamp(260px,36vw,520px)}
.rv-pick__shot img{max-height:clamp(240px,34vw,500px);width:auto;object-fit:contain}
.rv-pick__meta{margin-top:clamp(14px,2vw,20px)}
.rv-pick__meta h3{font-size:clamp(19px,2vw,25px);font-weight:300;display:flex;
 align-items:center;gap:12px;flex-wrap:wrap}
.rv-pick__meta p{margin:10px 0 0;color:#c3ccd5;font-size:15.5px;max-width:60ch}
.rv-tag{font:700 10px/1 var(--rv-mf);letter-spacing:.14em;text-transform:uppercase;
 padding:6px 10px;border-radius:999px;white-space:nowrap}
.rv-tag--work{background:var(--rv-cyan);color:#06181d}
.rv-tag--draft{border:1px solid var(--rv-line);color:var(--rv-ink2)}
.rv-pick__thumbs{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:0;padding:0;
 list-style:none}
.rv-pick__thumbs button{width:100%;cursor:pointer;background:#fff;border:2px solid transparent;
 border-radius:12px;padding:8px;transition:border-color .2s,transform .2s;position:relative;
 display:block}
.rv-pick__thumbs button:hover{transform:translateY(-2px)}
.rv-pick__thumbs button[aria-pressed=true]{border-color:var(--rv-cyan)}
.rv-pick__thumbs img{height:clamp(64px,7vw,96px);width:100%;object-fit:contain}
.rv-pick__thumbs i{position:absolute;top:6px;right:6px;width:9px;height:9px;border-radius:50%;
 background:var(--rv-cyan)}
.rv-pick__hint{margin:14px 0 0;font-size:13px;color:var(--rv-ink2);display:flex;
 align-items:center;gap:8px}
.rv-pick__hint i{width:9px;height:9px;border-radius:50%;background:var(--rv-cyan);flex:none}
.rv-keys{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
 gap:clamp(14px,2vw,22px);margin-top:clamp(24px,3.4vw,40px)}
.rv-keys figure{margin:0}
.rv-keys img{background:#fff;border-radius:14px;width:100%;aspect-ratio:4/3;object-fit:contain;
 padding:10px}
.rv-keys h4{margin:12px 0 0;font:600 15px var(--rv-bf)}
.rv-keys p{margin:6px 0 0;font-size:13.5px;color:var(--rv-ink2)}

/* ── подготовка: график ── */
.rv-cps{margin-top:clamp(26px,3.4vw,44px);overflow-x:auto;padding-bottom:6px}
.rv-cps__grid{min-width:660px;display:grid;
 grid-template-columns:clamp(150px,17vw,210px) repeat(11,1fr);gap:6px 0;align-items:center}
.rv-cps__head{font:600 10.5px/1 var(--rv-mf);color:var(--rv-ink2);text-align:center;
 padding-bottom:8px;letter-spacing:.04em}
.rv-cps__name{font-size:14px;font-weight:600;padding-right:14px}
.rv-cps__bar{grid-column:var(--s)/var(--e);height:12px;border-radius:999px;
 background:linear-gradient(90deg,var(--rv-cyan),rgba(0,181,212,.42));margin:0 2px}
.rv-cps__bar--last{background:var(--rv-fire)}
.rv-cps__note{grid-column:2/-1;font-size:13px;color:var(--rv-ink2);margin:0 0 8px 2px}
.rv-cps__legend{margin-top:14px;font-size:13.5px;color:var(--rv-ink2)}

/* ── бюджет и команда ── */
.rv-two{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(28px,5vw,70px);
 align-items:start;margin-top:clamp(28px,4vw,46px)}
.rv-bud{margin:0;padding:0}
.rv-bud>div{padding:16px 0;border-bottom:1px solid var(--rv-line)}
.rv-bud dt{display:flex;justify-content:space-between;align-items:baseline;gap:16px;
 font-weight:600;font-size:15.5px}
.rv-bud dt span{font-family:var(--rv-mf);font-size:13px;color:var(--rv-cyan)}
.rv-bud__bar{height:5px;border-radius:999px;background:rgba(255,255,255,.09);margin:10px 0 0;
 overflow:hidden}
.rv-bud__bar i{display:block;height:100%;border-radius:999px;background:var(--rv-cyan);
 width:var(--w);transform-origin:left;transform:scaleX(0);transition:transform 1s cubic-bezier(.22,.72,.24,1)}
.is-in .rv-bud__bar i{transform:scaleX(1)}
.rv-bud dd{margin:8px 0 0;font-size:13.5px;color:var(--rv-ink2)}
.rv-team{margin:0;padding:0;list-style:none}
.rv-team li{display:grid;grid-template-columns:auto 1fr;gap:16px;padding:16px 0;
 border-bottom:1px solid var(--rv-line);align-items:baseline}
.rv-team b{font-family:var(--rv-df);font-weight:200;font-size:clamp(26px,3vw,38px);
 line-height:1;color:var(--rv-cyan)}
.rv-team span{font-weight:600;font-size:15px}
.rv-team p{margin:4px 0 0;font-size:13.5px;color:var(--rv-ink2)}

/* ── результат ── */
.rv-res{background:var(--rv-bg2)}
.rv-res__grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,70px);
 align-items:start}
.rv-res__list{margin:clamp(6px,1vw,10px) 0 0;padding:0;list-style:none;counter-reset:l}
.rv-res__list li{counter-increment:l;padding:clamp(16px,2.2vw,24px) 0;
 border-top:1px solid var(--rv-line);display:grid;grid-template-columns:auto 1fr;gap:18px}
.rv-res__list li::before{content:counter(l,decimal-leading-zero);font:700 12px var(--rv-mf);
 color:var(--rv-cyan);padding-top:5px}
.rv-res__list b{font-weight:600;font-size:16px}
.rv-res__list p{margin:6px 0 0;font-size:14.5px;color:var(--rv-ink2)}
.rv-res__kpi{background:var(--rv-card);border:1px solid var(--rv-line);border-radius:20px;
 padding:clamp(22px,3vw,34px)}
.rv-res__kpi strong{display:block;font-family:var(--rv-df);font-weight:200;
 font-size:clamp(38px,5.4vw,68px);line-height:1;color:var(--rv-cyan)}
.rv-res__kpi p{margin:14px 0 0;color:#c3ccd5}
.rv-res__more{margin:clamp(22px,3vw,32px) 0 0;font-size:15px;color:var(--rv-ink2)}
.rv-res__more a{color:var(--rv-cyan);text-decoration:underline;text-underline-offset:3px}

@media (max-width:1000px){
 .rv-hero__grid,.rv-brief,.rv-two,.rv-res__grid{grid-template-columns:1fr}
 .rv-pick{grid-template-columns:1fr}
 .rv-pick__thumbs{grid-template-columns:repeat(4,1fr)}
 .rv-el-grid{grid-template-columns:repeat(2,1fr)}
 .rv-ev{grid-template-columns:1fr}
 .rv-ev__nav{position:static;flex-direction:row;overflow-x:auto;gap:6px;padding-bottom:6px}
 .rv-ev__nav button{border-left:0;border-bottom:2px solid var(--rv-line);white-space:nowrap;
  flex-direction:column;gap:2px;padding:8px 12px}
 .rv-ev__nav button[aria-selected=true]{border-color:var(--rv-cyan)}
}
@media (max-width:720px){
 .rv{font-size:16px}
 .rv-nums{grid-template-columns:repeat(2,1fr);gap:20px}
 .rv-diff__row{grid-template-columns:1fr;gap:14px}
 .rv-diff__why{grid-column:1/-1}
 .rv-el-grid{grid-template-columns:1fr}
 .rv-ev__body{grid-template-columns:1fr}
 .rv-pick__thumbs{grid-template-columns:repeat(3,1fr)}
 .rv-sign__tabs{grid-template-columns:repeat(2,1fr)}
}
@media (prefers-reduced-motion:reduce){
 .rv *{transition-duration:.01ms!important;animation-duration:.01ms!important}
 .rv-r{opacity:1;transform:none}
}
</style>""".replace('IMGSRC', IMG)

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>«Внутри стихии»: презентация ТРЦ Ривьера арендаторам | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: мероприятие «Внутри стихии» для ТРЦ Ривьера, 1 октября 2015 года. Передача помещения под отделку якорному арендатору «Ашан Сити» на строительной площадке: концепция четырёх стихий, экскурсия по недострою со звуковыми иллюзиями, 3D mapping, четыре фуршетных острова.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="«Внутри стихии»: презентация ТРЦ Ривьера арендаторам | Hand Marketing">
<meta property="og:description" content="198 первых лиц в строительных касках на площадке будущего ТРЦ. Четыре стихии как метафора инженерии здания: земля это фундамент, воздух вентиляция, вода водопровод, огонь свет и отопление.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/stage.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/raleway.css" rel="stylesheet"><link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def sign_svg(cls=''):
    """Пустой каркас знака: пути рисует JS, чтобы стихии перетекали друг в друга."""
    paths = ''.join('<path d=""></path>' for _ in range(6))
    return (f'<svg{cls} viewBox="0 0 100 100" aria-hidden="true">{paths}</svg>')


def sign_static(amp, rot):
    """Тот же знак, но посчитанный на сборке: для карточек стихий и no-js."""
    import math
    out = []
    for i in range(6):
        y = 16 + i * 13.6
        pts = []
        for s in range(25):
            x = 12 + s * 3.0
            pts.append(f'{x:.1f} {y - amp * math.sin(s / 24 * math.pi * 2 + math.pi):.1f}')
        out.append('<path d="M' + 'L'.join(pts) + '"/>')
    g = f'<g transform="rotate({rot} 50 50)">' + ''.join(out) + '</g>' if rot else ''.join(out)
    return f'<svg viewBox="0 0 100 100" aria-hidden="true">{g}</svg>'


def hero():
    chips = ''.join(f'<li>{c}</li>' for c in (
        'Концепция', 'Приглашения и обзвон базы', 'Сценарий', 'Оформление и навигация',
        'Свет, звук, 3D mapping', 'Кейтеринг', 'Сувениры'))
    nums = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in (
        ('198', 'человек в списке приглашённых за три дня до вечера'),
        ('75+', 'KPI по числу пришедших, выполнен'),
        ('298&nbsp;000', 'м² комплекса, по которому шла экскурсия'),
        ('4', 'стихии, они же четыре инженерные системы'),
    ))
    tabs = ''.join(
        f'<button type="button" data-el="{k}" aria-pressed="{"true" if k == "air" else "false"}">'
        f'{n}</button>' for k, n, *_ in ELEMENTS)
    art_id = ' id="rv-sign-art"'
    return (
      '<header class="rv-hero"><div class="rv-w">'
      '<div class="rv-hero__grid">'
      '<div class="rv-r">'
      f'<div class="rv-hero__client"><img src="{IMG}/logo-riviera.png" '
      'alt="ТРЦ Ривьера" width="1662" height="378" fetchpriority="high">'
      '<span>Передача помещения<br>под отделку арендатору</span></div>'
      '<h1>Внутри <b>стихии</b></h1>'
      '<p class="rv-hero__sub">1 октября 2015 года почти двести руководителей '
      'компаний надели строительные каски и приехали на площадку, где не было '
      'ни полов, ни витрин, ни отопления. ТРЦ Ривьера передавал первое '
      'помещение под отделку якорному арендатору «Ашан Сити», и этот вечер '
      'должен был доказать будущим арендаторам, что комплекс откроется в срок.</p>'
      f'<ul class="rv-chips">{chips}</ul>'
      '<div class="rv-hero__cta">'
      f'<a class="rv-btn rv-btn--p" href="#evening">Как прошёл вечер {ARROW}</a>'
      '<a class="rv-btn rv-btn--gh" href="#design">Варианты дизайна</a>'
      '</div></div>'
      # пульт стихий
      '<div class="rv-sign rv-r" id="rv-sign">'
      f'<div class="rv-sign__art">{sign_svg(art_id)}</div>'
      f'<div class="rv-sign__tabs" id="rv-sign-tabs">{tabs}</div>'
      '<dl class="rv-sign__cap" id="rv-sign-cap"><dt></dt><dd></dd></dl>'
      '</div>'
      '</div>'
      f'<dl class="rv-nums rv-r">{nums}</dl>'
      '</div></header>')


def brief():
    items = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in BRIEF)
    return (
      '<section class="rv-sec rv-sec--alt"><div class="rv-w">'
      '<div class="rv-brief">'
      '<div class="rv-r">'
      '<span class="rv-kick">Задача</span>'
      '<h2 class="rv-h2">Продать здание, которого ещё нет</h2>'
      '<p class="rv-lead">ТРЦ Ривьера строится на берегу Москвы-реки у ТТК, '
      'между станциями «Автозаводская» и «Тульская»: 298 000 м², три торговых '
      'этажа и трёхэтажный подземный паркинг, больше трёхсот магазинов и '
      'ресторанов. В июне 2015 года всё это ещё было бетонным каркасом, а '
      'арендаторам нужно было принимать решения уже сейчас.</p>'
      '<p class="rv-lead">Клиент дал базу на 320 контактов и KPI: минимум '
      'семьдесят пять пришедших. Полтора-два часа на вечер, двадцать минут на '
      'официальную часть, пятнадцать на маршрут экскурсии. Концепцию, '
      'приглашения, подарки, технику и оформление придумывает агентство.</p>'
      '</div>'
      '<div class="rv-r">'
      f'<dl class="rv-brief__list">{items}</dl>'
      '<figure class="rv-figure" style="margin:clamp(22px,3vw,32px) 0 0">'
      f'<img src="{IMG}/facade.jpg" width="1272" height="640" loading="lazy" '
      'alt="Рендер фасада будущего ТРЦ Ривьера с подсветкой и вывесками арендаторов">'
      '<figcaption>Таким комплекс должен был стать. На вечере гости видели '
      'бетон, арматуру и разметку секторов на колоннах.</figcaption></figure>'
      '</div>'
      '</div></div></section>')


def idea():
    cards = ''.join(
      f'<article class="rv-el-card rv-r" style="--c:{col}">{sign_static(amp, rot)}'
      f'<h3>{verb}</h3><b>{what}</b><p>{note}</p></article>'
      for k, name, col, amp, rot, verb, what, note in ELEMENTS)
    return (
      '<section class="rv-sec" id="idea"><div class="rv-w">'
      '<div class="rv-r"><span class="rv-kick">Идея</span>'
      '<h2 class="rv-h2">Четыре стихии и четыре инженерные системы</h2></div>'
      '<div class="rv-brief" style="margin-top:clamp(22px,3vw,34px)">'
      '<div class="rv-r">'
      '<p class="rv-idea__quote">Стихии это кирпичики мироздания четырёх '
      'сортов.</p>'
      '<p class="rv-lead">Понятие о четырёх первоэлементах пришло из античной '
      'философии и до сих пор живёт в нашей картине мира. Мы взяли его не ради '
      'красоты: в наши дни каждая стихия требует пересмотра качества её '
      'воплощения, и в языке стройки у каждой есть точный технический '
      'эквивалент.</p>'
      '<p class="rv-lead">Так метафора перестала быть украшением. Знак стихии '
      'печатался на бейдже, вёл группу по маршруту, отмечал остров на фуршете '
      'и стоял на флаконе подарка. Четыре знака это одна и та же линия с '
      'разной амплитудой: прямая, рябь, волна и та же волна на боку.</p>'
      f'<div class="rv-bricks"><img src="{IMG}/bricks.png" width="959" height="370" '
      'loading="lazy" alt="Четыре кирпича со знаками стихий: прямые линии, рябь, '
      'волна и вертикальная волна"></div>'
      '</div>'
      '<div class="rv-r">'
      '<p class="rv-lead" style="margin-top:0">Технологии определяют прогресс, '
      'но прогресс возможен только тогда, когда он направлен на человека. '
      'Команда ТРЦ внимательна к техническим требованиям каждого арендатора, '
      'и об этом стоило говорить на языке, который работает и для инженера, и '
      'для владельца бизнеса.</p>'
      f'<figure class="rv-figure"><img src="{IMG}/badges-photo.jpg" width="1200" '
      'height="608" loading="lazy" alt="Именные бейджи со знаками стихий на стойке '
      'регистрации">'
      '<figcaption>Знак с бейджа определял группу на экскурсии: «следуйте за '
      'своим амулетом» вместо переклички по списку.</figcaption></figure>'
      '</div></div>'
      f'<div class="rv-el-grid">{cards}</div>'
      '</div></section>')


def evening():
    nav = ''.join(
      f'<li><button type="button" role="tab" id="rv-ev-t{i}" aria-controls="rv-ev-p{i}" '
      f'aria-selected="{"true" if i == 0 else "false"}"><time>{t}</time>{title}</button></li>'
      for i, (t, _, title, _, _) in enumerate(EVENING))
    panels = ''.join(
      f'<div class="rv-ev__panel" role="tabpanel" id="rv-ev-p{i}" aria-labelledby="rv-ev-t{i}"'
      f'{"" if i == 0 else " hidden"}>'
      f'<img src="{IMG}/{f}.jpg" width="1200" height="610" loading="lazy" alt="{alt}">'
      f'<div class="rv-ev__body"><div><time>{t}</time><h3>{title}</h3></div>'
      f'<p>{txt}</p></div></div>'
      for i, (t, f, title, txt, alt) in enumerate(EVENING))
    return (
      '<section class="rv-sec rv-sec--alt" id="evening"><div class="rv-w">'
      '<div class="rv-r"><span class="rv-kick">Вечер</span>'
      '<h2 class="rv-h2">Четыре часа на стройке</h2>'
      '<p class="rv-lead">Площадку готовили как обычный зал, только вместо стен '
      'был бетон, вместо отопления газовые пушки, а вместо декораций '
      'подсвеченные колонны с разметкой секторов. Ниже вечер по шагам, '
      'фотографии из отчёта клиенту.</p></div>'
      '<div class="rv-ev rv-r">'
      f'<ul class="rv-ev__nav" role="tablist" id="rv-ev-nav">{nav}</ul>'
      f'<div>{panels}</div>'
      '</div>'
      '<figure class="rv-video rv-r">'
      '<video controls preload="none" playsinline '
      f'poster="{IMG}/stage.jpg" width="1280" height="720">'
      '<source src="/media/event-riviera.mp4" type="video/mp4">'
      '</video></figure>'
      '</div></section>')


def diff():
    rows = ''.join(
      '<div class="rv-diff__row rv-r">'
      f'<div class="rv-diff__k">{k}</div>'
      f'<div class="rv-diff__cell rv-diff__cell--plan"><b>Предложение, 22 июня</b>{plan}</div>'
      f'<div class="rv-diff__cell rv-diff__cell--fact"><b>Вечер, 1 октября</b>{fact}</div>'
      f'<p class="rv-diff__why">{why}</p>'
      '</div>' for k, plan, fact, why in DIFF)
    return (
      '<section class="rv-sec"><div class="rv-w">'
      '<div class="rv-r"><span class="rv-kick">Предложение и реальность</span>'
      '<h2 class="rv-h2">Что изменилось за три месяца</h2>'
      '<p class="rv-lead">Между презентацией концепции и вечером прошло сто дней, '
      'и стройка за это время диктовала свои правила. Концепция не изменилась '
      'ни на слово, изменились способы её показать.</p></div>'
      f'<div class="rv-diff">{rows}</div>'
      '<figure class="rv-figure rv-r" style="margin:clamp(24px,3vw,36px) 0 0;max-width:560px">'
      f'<img src="{IMG}/ipad-test.jpg" width="1251" height="661" loading="lazy" '
      'alt="Макет теста на планшете: гость выбирает свою стихию, отвечая на вопросы">'
      '<figcaption>Тест на планшете из июньского предложения. Идея хорошая, но '
      'на входе с ней встали бы в очередь двести человек.</figcaption></figure>'
      '</div></section>')


def picker(pid, title, items, hint=True):
    """Крупный кадр плюс миниатюры вариантов."""
    thumbs = ''.join(
      f'<li><button type="button" data-pick="{pid}" data-i="{i}" '
      f'aria-pressed="{"true" if i == 0 else "false"}" aria-label="{cap}">'
      f'<img src="{IMG}/{f}.jpg" alt="" loading="lazy">'
      f'{"<i></i>" if st == "work" else ""}</button></li>'
      for i, (f, cap, st, _) in enumerate(items))
    f0, cap0, st0, txt0 = items[0]
    tag0 = ('<span class="rv-tag rv-tag--work">в работе</span>' if st0 == 'work'
            else '<span class="rv-tag rv-tag--draft">вариант</span>')
    data = ''.join(
      f'<script type="application/json" data-pick-data="{pid}" data-i="{i}">'
      f'{{"src":"{IMG}/{f}.jpg","cap":"{cap}","st":"{st}","txt":"{txt}"}}</script>'
      for i, (f, cap, st, txt) in enumerate(items))
    return (
      f'<div class="rv-pick rv-r" data-pick-root="{pid}">'
      '<div class="rv-pick__stage">'
      f'<div class="rv-pick__shot"><img id="rv-shot-{pid}" src="{IMG}/{f0}.jpg" alt="{cap0}"></div>'
      f'<div class="rv-pick__meta"><h3 id="rv-cap-{pid}">{cap0}{tag0}</h3>'
      f'<p id="rv-txt-{pid}">{txt0}</p></div></div>'
      f'<div><ul class="rv-pick__thumbs" id="rv-thumbs-{pid}">{thumbs}</ul>'
      + ('<p class="rv-pick__hint"><i></i>точкой отмечено то, что ушло в работу</p>'
         if hint else '')
      + f'</div>{data}</div>')


def design():
    keys = ''.join(
      f'<figure><img src="{IMG}/{f}.jpg" loading="lazy" alt="{cap}">'
      f'<h4>{cap}</h4><p>{txt}</p></figure>' for f, cap, txt in KEYS)
    return (
      '<section class="rv-sec rv-sec--alt" id="design"><div class="rv-w">'
      '<div class="rv-r"><span class="rv-kick">Дизайн</span>'
      '<h2 class="rv-h2">Варианты и то, что ушло в работу</h2>'
      '<p class="rv-lead">Каждый носитель проходил через несколько версий. Ниже '
      'все они рядом: нажмите на миниатюру, чтобы посмотреть вариант крупно.</p></div>'
      '<h3 class="rv-h2 rv-h3 rv-r" style="margin-top:clamp(30px,4vw,50px)">Электронное приглашение</h3>'
      '<p class="rv-lead rv-r">Рассылка стартовала за две недели, на двух языках. '
      'Через десять дней операторы агентства начали работать по базе клиента: '
      'подтвердить получение, ответить на вопросы, уточнить решение и напомнить '
      'за два дня. К вечеру список сошёлся на 198 именах.</p>'
      + picker('inv', 'Приглашение', INVITES)
      + '<h3 class="rv-h2 rv-h3 rv-r" style="margin-top:clamp(40px,5vw,66px)">Бейдж</h3>'
      '<p class="rv-lead rv-r">Бейдж здесь не формальность, а рабочий инструмент '
      'вечера: он же именной, он же знак стихии, он же пропуск в свою группу на '
      'экскурсии.</p>'
      + picker('bdg', 'Бейдж', BADGES)
      + '<h3 class="rv-h2 rv-h3 rv-r" style="margin-top:clamp(40px,5vw,66px)">Ключ для передачи помещения</h3>'
      '<p class="rv-lead rv-r">Церемония требует предмета, который вручают с '
      'сцены и который потом стоит в офисе арендатора. Пять решений одной '
      'задачи.</p>'
      f'<div class="rv-keys rv-r">{keys}</div>'
      + '<h3 class="rv-h2 rv-h3 rv-r" style="margin-top:clamp(40px,5vw,66px)">Оформление и сувениры</h3>'
      + picker('sov', 'Сувениры', SOUVENIR)
      + '</div></section>')


def prep():
    heads = ''.join(f'<div class="rv-cps__head">{w}</div>' for w in range(26, 37))
    rows = ''
    for i, (name, s, e, note) in enumerate(CPS):
        last = ' rv-cps__bar--last' if i == len(CPS) - 1 else ''
        rows += (f'<div class="rv-cps__name">{name}</div>'
                 f'<div class="rv-cps__bar{last}" style="--s:{s - 24};--e:{e - 23}"></div>'
                 f'<p class="rv-cps__note">{note}</p>')
    bud = ''.join(
      f'<div><dt>{k}<span>{p}%</span></dt>'
      f'<div class="rv-bud__bar"><i style="--w:{p}%"></i></div><dd>{note}</dd></div>'
      for k, p, note in BUDGET)
    team = ''.join(
      f'<li><b>{n}</b><div><span>{k}</span><p>{note}</p></div></li>'
      for k, n, note in TEAM)
    return (
      '<section class="rv-sec"><div class="rv-w">'
      '<div class="rv-r"><span class="rv-kick">Подготовка</span>'
      '<h2 class="rv-h2">Одиннадцать недель до одного вечера</h2>'
      '<p class="rv-lead">График подготовительных работ шёл параллельно по восьми '
      'направлениям. Съёмка ролика с дрона, кастинг хостес, расчёт мощности на '
      'площадке без электрощита и производство подарков жили каждый своим '
      'сроком и сходились в последнюю неделю.</p></div>'
      '<div class="rv-cps rv-r"><div class="rv-cps__grid">'
      '<div></div>' + heads + rows + '</div></div>'
      '<p class="rv-cps__legend rv-r">Номера сверху это недели года: с 26-й, когда '
      'клиент выбирал агентство, по 36-ю, когда прошло мероприятие.</p>'
      '<div class="rv-two">'
      '<div class="rv-r"><h3 class="rv-h2 rv-h3">'
      'Куда ушёл бюджет</h3>'
      '<p class="rv-lead">Клиент дал вилку, мы уложились в неё вместе с '
      'агентской комиссией. Доли статей в финальной смете:</p>'
      f'<dl class="rv-bud">{bud}</dl></div>'
      '<div class="rv-r"><h3 class="rv-h2 rv-h3">'
      'Сорок один человек</h3>'
      '<p class="rv-lead">Столько людей работало на вечер, считая кухню и '
      'артистов.</p>'
      f'<ul class="rv-team">{team}</ul></div>'
      '</div></div></section>')


def result():
    lis = ''.join(f'<li><div><b>{k}</b><p>{v}</p></div></li>' for k, v in LEARNINGS)
    return (
      '<section class="rv-sec rv-res"><div class="rv-w">'
      '<div class="rv-res__grid">'
      '<div class="rv-r">'
      '<span class="rv-kick">Результат</span>'
      '<h2 class="rv-h2">KPI выполнен</h2>'
      '<div class="rv-res__kpi" style="margin-top:clamp(20px,2.6vw,30px)">'
      '<strong>198</strong>'
      '<p>человек в основном списке приглашённых за три дня до вечера при базе '
      'в 320 контактов и KPI в 75 пришедших. Помещения передали якорным '
      'арендаторам публично, вечер попал в отраслевые СМИ и в переговоры '
      'с другими арендаторами.</p></div>'
      '<p class="rv-res__more">Мероприятия под ключ это наша '
      '<a href="/event">услуга Event</a>. Другие проекты рядом: '
      '<a href="/event/samsung">новогодний вечер Samsung</a> и '
      '<a href="/btl/salaris-xmas">акция «Ком подарков» в ТРЦ Саларис</a>.</p>'
      '</div>'
      '<div class="rv-r">'
      '<h3 class="rv-h2 rv-h3">Что мы забрали '
      'себе на будущее</h3>'
      f'<ul class="rv-res__list">{lis}</ul>'
      '</div></div></div></section>')


PAGE_JS = """<script>(function(){
 var EL=%ELEMENTS%;
 // ── знак стихии рисуем сами: одна кривая, у стихий разная амплитуда и поворот
 function paths(node,amp,rot){
  var ps=node.querySelectorAll('path'),i,s,d,x,y;
  for(i=0;i<ps.length;i++){
   y=16+i*13.6;d='';
   for(s=0;s<25;s++){
    x=12+s*3;
    d+=(s?'L':'M')+x.toFixed(1)+' '+(y-amp*Math.sin(s/24*Math.PI*2+Math.PI)).toFixed(1);
   }
   ps[i].setAttribute('d',d);
  }
  node.style.transform='rotate('+rot+'deg)';
 }
 var art=document.getElementById('rv-sign-art'),
     tabs=document.getElementById('rv-sign-tabs'),
     cap=document.getElementById('rv-sign-cap'),
     hero=document.querySelector('.rv-hero'),
     sign=document.getElementById('rv-sign'),
     cur=null,anim=null;
 function show(key){
  var e=EL[key];if(!e||cur===key)return;
  var from=cur?EL[cur]:{amp:e.amp,rot:e.rot};cur=key;
  if(tabs)[].forEach.call(tabs.querySelectorAll('button'),function(b){
   b.setAttribute('aria-pressed',String(b.getAttribute('data-el')===key));});
  [hero,sign].forEach(function(n){if(n)n.style.setProperty('--rv-el',e.col);});
  if(cap){cap.querySelector('dt').innerHTML=e.verb+'<i>'+e.what+'</i>';
   cap.querySelector('dd').textContent=e.note;}
  if(!art)return;
  // перетекание между знаками: интерполируем амплитуду и угол
  var t0=performance.now(),dur=520;
  if(anim)cancelAnimationFrame(anim);
  (function step(now){
   var k=Math.min(1,(now-t0)/dur),p=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
   paths(art,from.amp+(e.amp-from.amp)*p,from.rot+(e.rot-from.rot)*p);
   if(k<1)anim=requestAnimationFrame(step);
  })(t0);
 }
 if(tabs)tabs.addEventListener('click',function(ev){
  var b=ev.target.closest('button');if(b)show(b.getAttribute('data-el'));});
 show('air');
 // ── шаги вечера
 var nav=document.getElementById('rv-ev-nav');
 if(nav){
  var btns=[].slice.call(nav.querySelectorAll('button'));
  btns.forEach(function(b){b.addEventListener('click',function(){
   btns.forEach(function(o){
    var on=o===b;o.setAttribute('aria-selected',String(on));
    var p=document.getElementById(o.getAttribute('aria-controls'));
    if(p)p.hidden=!on;});});});
  nav.addEventListener('keydown',function(e){
   var i=btns.indexOf(document.activeElement);if(i<0)return;
   var d=(e.key==='ArrowRight'||e.key==='ArrowDown')?1:
         (e.key==='ArrowLeft'||e.key==='ArrowUp')?-1:0;
   if(!d)return;
   e.preventDefault();
   var n=(i+d+btns.length)%btns.length;btns[n].focus();btns[n].click();});
 }
 // ── варианты дизайна: миниатюра открывает крупный кадр
 [].forEach.call(document.querySelectorAll('[data-pick-root]'),function(root){
  var pid=root.getAttribute('data-pick-root'),
      shot=document.getElementById('rv-shot-'+pid),
      capn=document.getElementById('rv-cap-'+pid),
      txt=document.getElementById('rv-txt-'+pid),
      data={};
  [].forEach.call(root.querySelectorAll('[data-pick-data]'),function(s){
   try{data[s.getAttribute('data-i')]=JSON.parse(s.textContent);}catch(err){}});
  root.addEventListener('click',function(ev){
   var b=ev.target.closest('[data-pick]');if(!b)return;
   var d=data[b.getAttribute('data-i')];if(!d)return;
   [].forEach.call(root.querySelectorAll('[data-pick]'),function(o){
    o.setAttribute('aria-pressed',String(o===b));});
   shot.src=d.src;shot.alt=d.cap;
   capn.innerHTML=d.cap+(d.st==='work'
    ?'<span class="rv-tag rv-tag--work">в работе</span>'
    :'<span class="rv-tag rv-tag--draft">вариант</span>');
   txt.textContent=d.txt;
  });
 });
 // ── появление блоков
 var els=[].slice.call(document.querySelectorAll('.rv-r'));
 function inn(nd){nd.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(nd){var r=nd.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(nd);else io.observe(nd);});
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Event","item":"https://hand-marketing.ru/event/"},'
  '{"@type":"ListItem","position":3,"name":"Внутри стихии, ТРЦ Ривьера",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    import json
    els = {k: {'col': col, 'amp': amp, 'rot': rot, 'verb': verb, 'what': what, 'note': note}
           for k, name, col, amp, rot, verb, what, note in ELEMENTS}
    js = PAGE_JS.replace('%ELEMENTS%', json.dumps(els, ensure_ascii=False))
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="rv">{hero()}{brief()}{idea()}{evening()}'
            f'{diff()}{design()}{prep()}{result()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'event', 'riviera')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
