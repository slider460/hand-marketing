#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/gaz/index.html: кейс «Газель-трансформер» —
вирусный ролик 2013 года про блокировку дифференциала Eaton для ГАЗели.

Что было раньше: запечённая Tilda-страница «задача → решение → результат»
сплошным текстом. Сам ролик лежал в конце, кадров не было ни одного, про
то, как ролик разошёлся, было сказано общими словами.

Идея страницы: в ролике всё держится на одном предмете — синей кнопке
блокировки на панели. Кнопка вынесена на страницу как настоящий орган
управления: нажатие переключает состояние всей страницы (палитра, кадр
героя, подписи), ровно как в сюжете оно переключает машину. Кнопка едет
за читателем в липкой панели и работает в любой момент.

Четыре механики:
1. Кнопка блокировки: data-lock на <html>, кадр «пробка» гаснет, из-под
   него выходит кадр «робот» на той же обочине, палитра уходит в синий.
2. Сториборд: 31 карандашный лист из презентации проекта, переключатель
   «раскадровка / как сняли» разом меняет рисунки на кадры ролика (30 из
   31 листа имеют пару), клик по листу перематывает плеер на этот момент.
   Единственный неснятый лист в режиме «как сняли» гаснет.
3. Критерии вирусности из брифа: шесть требований раскрываются ответом
   готового ролика.
4. Лента расползания 2013 → 2025: точки копий проявляются по очереди,
   когда секция попадает в экран, клик открывает карточку копии.

Источник фактуры о производстве — презентация проекта «eaton gaz.pptx»
(бриф, критерии вирусного ролика, три захода, сториборд, тракт из 12
этапов, три съёмочных дня, состав смены и техника, локация, графика).
Бюджет из презентации на страницу намеренно не вынесен.

Честность фактуры: даты, площадки и заголовки перезаливов — выборка
копий, которые находятся поиском (так и подписано в секции). Первое место
в подборке «10 лучших роликов про наш автопром» и 20 000 просмотров за
первые сутки — из материала Auto.Mail.ru от 09.01.2014, на него стоит
ссылка. Титры съёмочной группы и трек — из пресс-релиза кампании.

Шрифты Tektur + Rubik, локальные (/fonts/tektur-rubik.css),
кадры и фото готовит scripts/gaz-assets.py.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/gaz'
FILM = '/media/gazelle-transformer.mp4'
URL = 'https://hand-marketing.ru/video/gaz/'
MAILRU = ('https://auto.mail.ru/article/44945-lada_kalina_sobrana_na_kolenke_'
          'ili_10_luchshih_rolikov_pro_nash_avtoprom/')

# ─── паспорт проекта ────────────────────────────────────────────────────────
FACTS = [
    ('Клиент', 'ГАЗ и Eaton'),
    ('Год', '2013'),
    ('Формат', 'Вирусный ролик, 1:42'),
    ('Съёмка', 'Три смены'),
    ('Сториборд', '31 лист'),
]

# ─── рамки брифа: (что, значение) ───────────────────────────────────────────
# Бюджет из презентации на страницу намеренно не выносим.
FRAME = [
    ('Хронометраж', '30–60 секунд'),
    ('Съёмка', 'На натуре'),
    ('Графика', 'Не предполагалась'),
    ('План смен', 'Одна, без переработок'),
]

# ─── критерии вирусного ролика из брифа: (критерий, требование, наш ответ) ──
VIRAL = [
    ('Невероятность сценария',
     'Сюжет должен «взрывать» мозг: необычный взгляд на привычные вещи или '
     'что-то принципиально новое.',
     'Маршрутка из утренней пробки встаёт на ноги и уходит по грязи. '
     'Привычнее сюжета в стране нет, а такого поворота в нём никто не ждёт.'),
    ('Тонкая связь с брендом',
     'Если ролик откровенно рекламный, зрители не станут им делиться и вирусная '
     'раскрутка не сработает.',
     'Ни одного кадра с логотипом до самого конца. Продукт показан как деталь '
     'сюжета: кнопка на панели, без которой ничего бы не случилось.'),
    ('Удобство распространения',
     'Насколько просто опубликовать ролик у себя или отправить другу.',
     'Полтора десятка перезаливов на разных площадках за первые два года: '
     'ролик забирали себе целиком, без ссылок и условий.'),
    ('Вирусный потенциал',
     'Насколько ролик вызывает желание показать его знакомым.',
     'Шутка держится на общем опыте: её понимает любой, кто стоял в пробке '
     'и видел, как маршрутка объезжает её по обочине.'),
    ('Актуальность',
     'Насколько сюжет попадает в текущие настроения и разговоры.',
     'Год выхода «Трансформеров» в прокате и вечная московская пробка '
     'в одном кадре.'),
    ('Скорость распространения',
     'Основная волна должна прийтись на первые две-три недели: у удачных '
     'роликов 40% просмотров набирается уже за первую неделю.',
     'Двадцать тысяч просмотров за первые сутки после появления в сети.'),
]

# ─── заходы, которые обсуждались: (название, описание, статус) ──────────────
IDEAS = [
    ('Чёрный юмор',
     'Стройка, сельская местность, ухабистая земляная дорога. В кузове грузовой '
     'ГАЗели едут строители, машина застревает в грязи и буксует. Водитель '
     'просит пассажиров подтолкнуть, и рабочие со знанием дела берутся '
     'вызволять машину.',
     'Отклонено'),
    ('Псевдодокументальная история',
     'Обычная московская пробка, снятая будто бы видеорегистратором или '
     'телефоном, — при том что снимает камера высокой чёткости. Ставка на то, '
     'что зритель принимает картинку за случайную запись.',
     'Отклонено'),
    ('Дорожная пробка',
     'Заявочные планы пробки, маршрутка, кнопка на панели. Машина '
     'трансформируется в робота, обходит пробку и снова становится маршруткой. '
     'В финале водитель просыпается от похлопывания по плечу: ему подают '
     'деньги за проезд.',
     'В работу'),
]

# ─── ограничения брифа: (заголовок, текст) ──────────────────────────────────
LIMITS = [
    ('Рекламируем не машину',
     'Продукт кампании: одна опция в прайсе, блокируемый дифференциал Eaton '
     'на ГАЗель Бизнес и Соболь. Снаружи машина с ней и без неё выглядит '
     'одинаково, показать нечего.'),
    ('Сравнивать нельзя',
     'Категорически запрещалось ставить рядом автомобиль с блокировкой и без '
     'неё. Прямая демонстрация преимущества, с которой начинается любой ролик '
     'про проходимость, отпадала сразу.'),
    ('Позиционирование консервативное',
     'Почти все идеи с вирусным потенциалом заворачивались PR-службой: марка '
     'на рынке держится серьёзного тона, шутить над собственной машиной '
     'она не готова.'),
]

# ─── сториборд: (подпись, секунда в ролике или None) ────────────────────────
# Порядок = порядок листов в презентации проекта. Секунда — момент, на
# котором в готовом ролике стоит тот же кадр; None у листов, которых на
# экране нет. Пары должны совпадать с PAIRS в scripts/gaz-assets.py.
STORY = [
    ('Пробка на вылетной магистрали, внизу кадра разбитая обочина', 1.5),
    ('Водитель легковушки жмёт на клаксон', 6.0),
    ('Мужчина вышел из машины и звонит: он застрял', 9.5),
    ('Маршрутка в общем потоке', 11.0),
    ('Салон: пассажиры нервничают, ребёнок на заднем сиденье', 12.0),
    ('Водитель смотрит вперёд и знает про машину то, чего не знают они', 16.0),
    ('Панель приборов, кнопка блокировки', 20.5),
    ('Рука на рычаге коробки', 23.5),
    ('Руки на руле', 13.5),
    ('Нога на педали', 24.0),
    ('Колесо трогается с места', 27.0),
    ('Маршрутка уходит с асфальта на грунтовую обочину', 26.0),
    ('Колесо в грязи', 29.0),
    ('Водитель тянется к панели', 30.0),
    ('Палец нажимает кнопку', 30.5),
    ('Машина раскладывается прямо в поле', 33.0),
    ('Парень с телефоном не верит своим глазам', 36.0),
    ('Робот в полный рост выходит на обочину', 40.0),
    ('Женщина на остановке оборачивается', 44.0),
    ('Крупный план механики: сустав робота', None),  # единственный неснятый лист
    ('Робот бежит вдоль пробки', 57.0),
    ('Робот проходит над женщиной', 50.0),
    ('Взгляд сверху: робот шагает через кадр', 48.0),
    ('Робот уходит вперёд по обочине', 58.0),
    ('Маршрутка снова маршрутка: обратная трансформация', 67.5),
    ('Салон: пассажиры смеются', 72.0),
    ('Водителя трогают за плечо', 79.0),
    ('Пассажир протягивает деньги за проезд', 74.0),
    ('Водитель оборачивается: это был сон', 89.0),
    ('Финальный кадр, та же кнопка на панели', 93.5),
    ('Пэкшот. На листе стоит «www.сайт.com»', 97.0),
]

# ─── бумага против экрана: (что было на листах, что вышло, подпись) ─────────
DIFFS = [
    ('Кнопка красная', 'Кнопка синяя',
     'На всех листах сториборда кнопка нарисована красной: художник рисовал '
     '«тревожную кнопку» по смыслу. У настоящего ELocker на панели ГАЗели '
     'она синяя, и в кадр пошла именно она.'),
    ('Без графики', 'Робот и аниматика',
     'Бриф описывал простой ролик на натуре без графики и сложных трюков. '
     'Робота собрали моделью, согласовали аниматику — траекторию его '
     'перемещения — и только потом детализировали до финального качества.'),
    ('Одна смена', 'Три съёмочных дня',
     'План был снять всё за одну смену без переработок. В итоге первый день '
     'ушёл на панорамы, второй на крупные планы водителя и пассажиров, '
     'третий на досъёмку того, что не успели.'),
]

# ─── тракт производства: 12 этапов из презентации ──────────────────────────
STAGES = [
    'Согласование идеи', 'Разработка сценария', 'Утверждение сценария',
    'Отрисовка сториборда', 'Согласование сториборда', 'Подготовка к съёмке',
    'Съёмка', 'Черновой монтаж', 'Графика', 'Разработка звука',
    'Сборка: видео, графика, звук', 'Цветокоррекция',
]

# ─── съёмочные дни: (номер, что снимали) ───────────────────────────────────
SHIFTS = [
    ('День 1', 'Все панорамные кадры'),
    ('День 2', 'Крупные планы водителя и пассажиров'),
    ('День 3', 'Досъёмка кадров, которые не успели в первый день'),
]

CREW_LIST = ['Режиссёр', 'Второй режиссёр', 'Оператор', 'Ассистент оператора',
             'Администратор площадки', 'Техник', 'Гафер', 'Актёры']
GEAR_LIST = ['Камера RED Scarlet в обвесе', 'Набор объективов', 'Штатив и кран',
             'Осветительное оборудование', 'Генератор', 'Светоотражатели',
             'Отдельное звукозаписывающее устройство', 'Хлопушка']

# ─── съёмка и кадр: (фото, кадр, заголовок, текст, подпись 1, подпись 2) ───
BTS = [
    ('shoot-crew.jpg', 'shot-pylon.jpg', 'Опора ЛЭП',
     'Оператор снимает с крана вверх, в пустое небо над опорой. В готовом '
     'ролике по этой точке пойдёт робот: опора на фотографии со съёмки и '
     'опора в кадре одна и та же, поэтому графика стоит в настоящей '
     'перспективе места, а не поверх произвольного фона.',
     'Съёмочная группа на локации', 'Тот же ракурс в готовом ролике'),
    ('shoot-cab.jpg', 'shot-driver.jpg', 'Кабина',
     'Вся линия водителя снята в одной кабине: пробка, сон и пробуждение '
     'идут в том же салоне и в том же пасмурном свете. На этом держится '
     'финал: до последнего кадра зритель не отличает сон от яви.',
     'Актёр перед дублем', 'Тот же кадр в ролике'),
]

# ─── расползание копий: (дата, площадка, подпись, класс) ────────────────────
# Выборка копий, которые находятся поиском. Полного списка не существует:
# ролик разошёлся по частным аккаунтам и пабликам без единого источника.
SPREAD = [
    ('10.06.2013', 'Rutube', 'Самая ранняя копия, которая находится в поиске. Заголовок ещё простой: «Газель трансформер».', ''),
    ('15.06.2013', 'YouTube', 'Копия с заголовком «Новая креативная реклама ГАЗель Трансформер». Под этим именем ролик расходится дальше всего.', ''),
    ('20.06.2013', 'Пресса', 'Выходит пресс-релиз кампании: маршрутка, синяя кнопка, блокировка Eaton для ГАЗель Бизнес и Соболь.', ''),
    ('27.12.2013', 'ВКонтакте', 'Ролик забирают себе автомобильные паблики и магазины: салон литых дисков выкладывает его как «Реклама автомобилей ГАЗель (Трансформер)».', ''),
    ('09.01.2014', 'Auto.Mail.ru', 'Подборка «10 лучших роликов про наш автопром»: ролик стоит первым, рядом с камазовским «Танки грязи не боятся».', 'is-press'),
    ('31.03.2014', 'Одноклассники', 'Заголовок мутирует в «ГАЗель Трансформер. Прикольная реклама», под ним ролик репостят следующие полтора года.', ''),
    ('11.04.2014', 'Мой Мир', 'Копия расходится по личным видеоальбомам: у ролика больше нет владельца, есть только пересказ.', ''),
    ('13.07.2014', 'ВКонтакте', 'Год спустя ролик всё ещё выкладывают как новинку.', ''),
    ('31.01.2015', 'Одноклассники', 'Очередной заголовок: «Бомбовый рекламный ролик ГАЗели».', ''),
    ('21.03.2015', 'ВКонтакте', 'Ролик используют как контент сети шиномонтажей: реклама опции работает на чужой бизнес.', ''),
    ('04.08.2016', 'ВКонтакте', 'Крупный автомобильный паблик выкладывает копию заново, спустя три года после съёмок.', ''),
    ('07.01.2019', 'Одноклассники', 'Шестой год жизни ролика. Про блокировку дифференциала в подписях уже никто не пишет.', ''),
    ('27.01.2024', 'Rutube', 'Одиннадцатый год. Ролик перезаливают на площадку, которой в 2013 году в этой роли не было.', ''),
    ('28.04.2025', 'Rutube', 'Последний перезалив, который нашёлся при сборке этой страницы. Спустя двенадцать лет заголовок всё ещё «Новая креативная реклама».', 'is-last'),
]

# ─── титры: (роль, имена) ───────────────────────────────────────────────────
CREDITS = [
    ('Продюсер', 'Александр Народецкий'),
    ('Сценарий', 'Дмитрий Багин, Александр Народецкий'),
    ('Режиссёр', 'Дмитрий Багин'),
    ('Второй режиссёр', 'Мария Бедарева'),
    ('Оператор', 'Александр Барышников'),
    ('Техник камеры', 'Пётр Королев'),
    ('Бригадир по свету', 'Константин Лещенко'),
    ('Монтаж и цветоустановка', 'Яна Смирнова'),
    ('Музыка', 'Becks V Menthol — Ultra Lust'),
]


def pic(name, alt, cls='', width=None, height=None, lazy=True):
    """<picture> с webp: все кадры кейса лежат парами .jpg + .jpg.webp."""
    src = f'{IMG}/{name}'
    wh = (f' width="{width}" height="{height}"' if width else '')
    return (f'<picture><source srcset="{src}.webp" type="image/webp">'
            f'<img src="{src}" alt="{alt}"{" class=" + chr(34) + cls + chr(34) if cls else ""}'
            f'{wh}{" loading=" + chr(34) + "lazy" + chr(34) + " decoding=" + chr(34) + "async" + chr(34) if lazy else ""}></picture>')


PAGE_CSS = '''<style id="gz-css">
.gz{--bg:#0E1013;--panel:#161A20;--ink:#EEF1F5;--dim:#98A2AE;--line:rgba(255,255,255,.11);
 --acc:#2B8FEB;--acc2:#7FC2FF;--mud:#7A6A50;--rad:4px;
 background:var(--bg);color:var(--ink);font-family:'Rubik',-apple-system,Arial,sans-serif;
 font-size:17px;line-height:1.6;overflow-x:clip;
 transition:background .5s ease}
html[data-lock="on"] .gz{--bg:#070C15;--panel:#0D1622;--line:rgba(127,194,255,.2);--dim:#93B6D6;--mud:#3C6E9E}
.gz *,.gz *::before,.gz *::after{box-sizing:border-box}
.gz img{max-width:100%;height:auto;display:block}
.gz h1,.gz h2,.gz h3,.gz .tk{font-family:'Tektur','Rubik',Arial,sans-serif;font-weight:700;
 letter-spacing:.01em;line-height:1.02;margin:0;text-transform:uppercase}
.gz p{margin:0 0 14px}
.gz section{position:relative}
.gz__in{max-width:1180px;margin:0 auto;padding:0 clamp(16px,4vw,40px)}
.gz-r{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.gz-r.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.gz-r{opacity:1;transform:none;transition:none}}
.gz-eyebrow{font-family:'Tektur',Arial,sans-serif;font-size:12px;letter-spacing:.22em;
 text-transform:uppercase;color:var(--acc2);margin-bottom:14px;display:flex;align-items:center;gap:10px}
.gz-eyebrow::before{content:"";width:26px;height:2px;background:var(--acc);flex:none}
.gz-h2{font-size:clamp(26px,4.4vw,50px);margin-bottom:16px}
.gz-sub{color:var(--dim);max-width:66ch;font-size:clamp(15px,1.5vw,18px)}

/* ── ГЕРОЙ ───────────────────────────────────────────────────────────── */
.gz-hero{min-height:min(92vh,760px);display:flex;align-items:flex-end;padding:clamp(28px,7vh,80px) 0 clamp(24px,5vh,54px);overflow:hidden}
.gz-hero__bg{position:absolute;inset:0;z-index:0}
.gz-hero__bg picture{position:absolute;inset:0}
.gz-hero__bg img{width:100%;height:100%;object-fit:cover;object-position:center 62%}
.gz-hero__bg .b{opacity:0;transition:opacity .9s ease}
html[data-lock="on"] .gz-hero__bg .a{opacity:0}
html[data-lock="on"] .gz-hero__bg .b{opacity:1}
.gz-hero__bg::after{content:"";position:absolute;inset:0;transition:background .9s ease;
 background:linear-gradient(180deg,rgba(14,16,19,.72) 0%,rgba(14,16,19,.35) 34%,rgba(14,16,19,.92) 100%)}
/* в режиме блокировки затемнение отпускает середину кадра: робот должен читаться */
html[data-lock="on"] .gz-hero__bg::after{
 background:linear-gradient(180deg,rgba(6,10,18,.6) 0%,rgba(6,10,18,.14) 38%,rgba(6,10,18,.93) 100%)}
html[data-lock="on"] .gz-hero__bg .b img{filter:contrast(1.08) saturate(1.1)}
.gz-hero .gz__in{position:relative;z-index:1;width:100%}
/* в режиме блокировки за надстрочником светлое небо — держим контраст */
.gz-hero .gz-eyebrow{text-shadow:0 2px 14px rgba(0,0,0,.85)}
html[data-lock="on"] .gz-hero .gz-eyebrow{color:#CFE6FF}
.gz-hero h1{font-size:clamp(38px,8.4vw,104px);line-height:.92;letter-spacing:-.01em;
 text-shadow:0 6px 40px rgba(0,0,0,.55)}
.gz-lead{margin-top:18px;max-width:44ch;font-size:clamp(16px,1.7vw,20px);color:#D6DCE4}
.gz-swap>span{display:none}
.gz-swap>.off{display:inline}
html[data-lock="on"] .gz-swap>.off{display:none}
html[data-lock="on"] .gz-swap>.on{display:inline}
.gz-facts{list-style:none;display:flex;flex-wrap:wrap;gap:8px 10px;margin:24px 0 0;padding:0}
.gz-facts li{border:1px solid var(--line);border-radius:var(--rad);padding:8px 14px;
 background:rgba(10,12,16,.5);backdrop-filter:blur(4px)}
.gz-facts b{display:block;font-family:'Tektur',Arial,sans-serif;font-size:10.5px;letter-spacing:.18em;
 text-transform:uppercase;color:var(--dim);font-weight:500;margin-bottom:2px}
.gz-facts span{font-size:15px;font-weight:500;white-space:nowrap}

/* ── КНОПКА БЛОКИРОВКИ ───────────────────────────────────────────────── */
.gz-lock{display:inline-flex;align-items:center;gap:16px;margin-top:30px;padding:12px 22px 12px 14px;
 border:1px solid var(--line);border-radius:10px;cursor:pointer;color:inherit;text-align:left;
 background:linear-gradient(180deg,#23262C,#15181D);font:inherit;
 box-shadow:0 10px 30px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.06);
 transition:transform .15s ease,border-color .3s ease}
.gz-lock:hover{transform:translateY(-2px)}
.gz-lock:active{transform:translateY(1px)}
.gz-lock__b{position:relative;flex:none;width:46px;height:46px;border-radius:50%;
 background:radial-gradient(circle at 34% 30%,#2A2E35,#101318);
 border:1px solid rgba(255,255,255,.14);display:grid;place-items:center;
 box-shadow:inset 0 2px 5px rgba(0,0,0,.7)}
.gz-lock__b i{width:26px;height:26px;border-radius:50%;display:block;
 background:radial-gradient(circle at 36% 30%,#4EA6F5,#0E5FB0 62%,#083B72);
 box-shadow:0 0 0 1px rgba(0,0,0,.5),0 0 10px rgba(43,143,235,.25);transition:box-shadow .35s ease}
html[data-lock="on"] .gz-lock__b i{box-shadow:0 0 0 1px rgba(0,0,0,.5),0 0 22px 4px rgba(79,168,255,.75)}
.gz-lock__t{font-family:'Tektur',Arial,sans-serif;font-size:13px;letter-spacing:.14em;text-transform:uppercase;line-height:1.25}
.gz-lock__t small{display:block;font-family:'Rubik',Arial,sans-serif;font-size:12.5px;letter-spacing:0;
 text-transform:none;color:var(--dim);margin-top:3px}
/* липкая кнопка: появляется, когда герой ушёл вверх */
.gz-dock{position:fixed;right:16px;bottom:16px;z-index:900;padding:10px 16px 10px 10px;gap:12px;
 margin:0;opacity:0;visibility:hidden;transform:translateY(14px);transition:opacity .3s,transform .3s,visibility .3s}
.gz-dock.on{opacity:1;visibility:visible;transform:none}
.gz-dock .gz-lock__b{width:38px;height:38px}
.gz-dock .gz-lock__b i{width:21px;height:21px}
.gz-dock .gz-lock__t small{display:none}
@media(max-width:520px){.gz-dock{right:10px;bottom:10px;padding:8px}.gz-dock .gz-lock__t{display:none}}

/* ── ЗАДАЧА ──────────────────────────────────────────────────────────── */
.gz-task{padding:clamp(56px,9vw,110px) 0}
.gz-task__grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:18px;margin-top:38px}
.gz-card{border:1px solid var(--line);border-radius:var(--rad);padding:24px;background:var(--panel);
 position:relative;overflow:hidden}
.gz-card::before{content:"";position:absolute;left:0;top:0;width:3px;height:100%;background:var(--mud);
 transition:background .5s ease}
html[data-lock="on"] .gz-card::before{background:var(--acc)}
.gz-card h3{font-size:17px;margin-bottom:10px}
.gz-card p{color:var(--dim);font-size:15.5px;margin:0}
.gz-solve{margin-top:36px;border:1px solid var(--line);border-radius:var(--rad);
 background:linear-gradient(135deg,rgba(43,143,235,.11),transparent 62%);padding:clamp(22px,3.4vw,38px)}
.gz-solve h3{font-size:clamp(19px,2.4vw,27px);margin-bottom:14px;color:var(--acc2)}
.gz-solve p:last-child{margin-bottom:0}
.gz-solve p{max-width:70ch}

/* ── РАСКАДРОВКА ─────────────────────────────────────────────────────── */
.gz-sb{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
.gz-sb__grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:14px;margin-top:34px}
.gz-sb__i{padding:0;border:1px solid var(--line);border-radius:var(--rad);background:var(--panel);
 cursor:pointer;color:inherit;text-align:left;font:inherit;overflow:hidden;display:block;
 transition:border-color .2s ease,transform .2s ease}
.gz-sb__i:hover{border-color:var(--acc);transform:translateY(-3px)}
/* внутренности карточки — span'ы (лежат внутри <button>), им нужен display:block */
.gz-sb__ph{display:block;position:relative;aspect-ratio:1280/528;background:#000}  /* широкий кадр ролика */
.gz-sb__ph picture{display:block;height:100%}
.gz-sb__ph img{width:100%;height:100%;object-fit:cover}
.gz-sb__tc{position:absolute;left:8px;bottom:8px;font-family:'Tektur',Arial,sans-serif;font-size:11px;
 letter-spacing:.1em;padding:3px 7px;background:rgba(6,8,12,.82);border-radius:3px;color:var(--acc2)}
.gz-sb__tx{display:block;padding:13px 15px 16px}
.gz-sb__tx b{font-family:'Tektur',Arial,sans-serif;font-size:13.5px;text-transform:uppercase;
 letter-spacing:.04em;display:block;margin-bottom:5px}
.gz-sb__tx span{color:var(--dim);font-size:14px;line-height:1.45;display:block}
.gz-sb__hint{margin-top:16px;color:var(--dim);font-size:14px}

/* ── ПЛЕЕР ───────────────────────────────────────────────────────────── */
.gz-film{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
.gz-film__box{margin-top:30px;border:1px solid var(--line);border-radius:var(--rad);overflow:hidden;
 background:#000;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.gz-film video{width:100%;height:auto;display:block;aspect-ratio:16/9;background:#000}
.gz-film__cap{display:flex;flex-wrap:wrap;gap:6px 26px;margin-top:16px;color:var(--dim);font-size:14px}
.gz-film__cap b{color:var(--ink);font-weight:500}

/* ── СЪЁМКА ──────────────────────────────────────────────────────────── */
.gz-shoot{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
/* фото со съёмки вертикальные, кадр ролика широкий: фото держит обе строки
   левой колонки, справа кадр и текст — так колонки сходятся по высоте */
.gz-pair{margin-top:40px;display:grid;grid-template-columns:.86fr 1.14fr;
 grid-template-rows:auto 1fr;gap:18px 22px;align-items:start}
.gz-pair figure{margin:0}
.gz-pair figure:first-child{grid-row:1/3}
.gz-pair figcaption{margin-top:9px;font-family:'Tektur',Arial,sans-serif;font-size:11px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--dim)}
.gz-pair img{border:1px solid var(--line);border-radius:var(--rad);width:100%}
.gz-pair__tx{grid-column:2;max-width:60ch}
.gz-pair__tx h3{font-size:clamp(18px,2.2vw,24px);margin-bottom:12px}
.gz-pair__tx p{color:var(--dim);margin:0}
.gz-pair+.gz-pair{margin-top:54px;padding-top:54px;border-top:1px solid var(--line)}
@media(max-width:760px){
 .gz-pair{grid-template-columns:1fr;grid-template-rows:none}
 .gz-pair figure:first-child{grid-row:auto}
 .gz-pair__tx{grid-column:1;max-width:none}
}

/* ── РАСПОЛЗАНИЕ ─────────────────────────────────────────────────────── */
.gz-spread{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
.gz-stat{display:grid;grid-template-columns:repeat(auto-fit,minmax(212px,1fr));gap:16px;margin-top:34px}
.gz-stat div{border:1px solid var(--line);border-radius:var(--rad);padding:22px;background:var(--panel)}
.gz-stat b{display:block;font-family:'Tektur',Arial,sans-serif;font-size:clamp(28px,4.6vw,44px);
 line-height:1;color:var(--acc2);margin-bottom:9px}
.gz-stat span{color:var(--dim);font-size:14.5px;line-height:1.45;display:block}
.gz-rail{margin-top:44px;position:relative}
.gz-rail__line{position:absolute;left:0;right:0;top:23px;height:2px;background:var(--line)}
/* на узких экранах лента прокручивается вбок: подсказываем это затуханием справа */
.gz-rail::after{content:"";position:absolute;right:0;top:0;bottom:10px;width:52px;pointer-events:none;
 background:linear-gradient(90deg,rgba(0,0,0,0),var(--bg));opacity:0;transition:opacity .3s}
@media(max-width:920px){.gz-rail::after{opacity:1}}
.gz-rail__dots{display:flex;gap:0;position:relative;overflow-x:auto;padding-bottom:10px;
 scrollbar-width:thin}
.gz-dot{flex:1 0 62px;background:none;border:0;padding:0;cursor:pointer;color:inherit;font:inherit;
 display:flex;flex-direction:column;align-items:center;gap:9px;opacity:0;transform:translateY(8px);
 transition:opacity .45s ease,transform .45s ease}
.gz-rail.in .gz-dot{opacity:1;transform:none}
.gz-dot__y{font-family:'Tektur',Arial,sans-serif;font-size:11px;letter-spacing:.08em;color:var(--dim);
 height:14px}
.gz-dot__d{width:13px;height:13px;border-radius:50%;border:2px solid var(--dim);background:var(--bg);
 transition:background .25s,border-color .25s,box-shadow .25s;position:relative;z-index:1}
.gz-dot:hover .gz-dot__d{border-color:var(--acc2)}
.gz-dot.is-on .gz-dot__d{background:var(--acc);border-color:var(--acc2);
 box-shadow:0 0 0 5px rgba(43,143,235,.18)}
.gz-dot.is-press .gz-dot__d{border-color:#FCB724}
.gz-dot.is-press.is-on .gz-dot__d{background:#FCB724;border-color:#FFD97A;box-shadow:0 0 0 5px rgba(252,183,36,.2)}
.gz-dot__p{font-size:11px;color:var(--dim);writing-mode:vertical-rl;height:86px;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.gz-rail__hint{display:none;margin-top:10px;color:var(--dim);font-size:12.5px}
@media(max-width:860px){
 /* на телефоне лента шире экрана: подсказка + затухание правого края */
 .gz-rail__hint{display:block}
 .gz-rail__dots{-webkit-mask-image:linear-gradient(90deg,#000 84%,transparent);
  mask-image:linear-gradient(90deg,#000 84%,transparent)}
}
.gz-note{margin-top:26px;border:1px solid var(--line);border-radius:var(--rad);padding:22px;
 background:var(--panel);min-height:132px}
.gz-note b{font-family:'Tektur',Arial,sans-serif;font-size:13px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--acc2);display:block;margin-bottom:8px}
.gz-note p{margin:0;color:var(--dim);font-size:15.5px}
.gz-press{margin-top:30px;border-left:3px solid #FCB724;padding:6px 0 6px 20px;max-width:74ch}
.gz-press p{font-size:clamp(16px,1.9vw,20px);margin-bottom:10px}
.gz-press a{color:var(--acc2)}
.gz-press small{color:var(--dim);font-size:13.5px}
.gz-disc{margin-top:26px;color:var(--dim);font-size:13.5px;max-width:74ch}

/* ── РАМКИ БРИФА ─────────────────────────────────────────────────────── */
.gz-frame{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));gap:1px;
 margin-top:32px;background:var(--line);border:1px solid var(--line);border-radius:var(--rad);
 overflow:hidden}
.gz-frame div{background:var(--panel);padding:18px 20px}
.gz-frame b{display:block;font-family:'Tektur',Arial,sans-serif;font-size:10.5px;letter-spacing:.18em;
 text-transform:uppercase;color:var(--dim);font-weight:500;margin-bottom:6px}
.gz-frame span{font-size:15.5px}

/* ── КРИТЕРИИ ВИРУСНОСТИ ─────────────────────────────────────────────── */
.gz-viral{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
.gz-cr__list{margin-top:32px;border-top:1px solid var(--line)}
.gz-cr{border-bottom:1px solid var(--line)}
.gz-cr summary{display:grid;grid-template-columns:minmax(190px,.9fr) 1.6fr;gap:10px 28px;
 padding:20px 44px 20px 0;cursor:pointer;position:relative;list-style:none;align-items:baseline}
.gz-cr summary::-webkit-details-marker{display:none}
.gz-cr summary::after{content:"+";position:absolute;right:8px;top:18px;font-family:'Tektur',Arial,sans-serif;
 font-size:20px;line-height:1;color:var(--acc2);transition:transform .25s ease}
.gz-cr[open] summary::after{content:"–"}
.gz-cr summary b{font-family:'Tektur',Arial,sans-serif;font-size:15px;text-transform:uppercase;
 letter-spacing:.03em;font-weight:700}
.gz-cr summary span{color:var(--dim);font-size:15px}
.gz-cr p{margin:0 44px 22px 0;padding:16px 20px;border-left:3px solid var(--acc);
 background:rgba(43,143,235,.07);max-width:80ch}
@media(max-width:760px){.gz-cr summary{grid-template-columns:1fr;padding-right:38px}}

/* ── ЗАХОДЫ ──────────────────────────────────────────────────────────── */
.gz-ideas{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
.gz-idea__tabs{display:flex;flex-wrap:wrap;gap:8px;margin-top:32px}
.gz-idea__t{border:1px solid var(--line);background:var(--panel);color:var(--dim);cursor:pointer;
 border-radius:var(--rad);padding:11px 18px;font:500 14.5px 'Rubik',Arial,sans-serif;
 transition:color .2s,border-color .2s,background .2s}
.gz-idea__t:hover{color:var(--ink)}
.gz-idea__t.is-on{color:var(--ink);border-color:var(--acc);background:rgba(43,143,235,.13)}
.gz-idea__panes{margin-top:18px;border:1px solid var(--line);border-radius:var(--rad);
 background:var(--panel);padding:clamp(20px,3vw,32px);min-height:170px}
.gz-idea__p{display:none}
.gz-idea__p.is-on{display:block}
.gz-idea__p p{margin:0;max-width:76ch;color:var(--dim);font-size:16px}
.gz-idea__st{display:inline-block;margin-bottom:12px;font-family:'Tektur',Arial,sans-serif;
 font-size:11px;letter-spacing:.16em;text-transform:uppercase;padding:5px 11px;border-radius:3px;
 background:rgba(255,255,255,.07);color:var(--dim)}
.gz-idea__st.ok{background:rgba(43,143,235,.2);color:var(--acc2)}

/* ── СТОРИБОРД ───────────────────────────────────────────────────────── */
.gz-st{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
.gz-seg{display:inline-flex;margin-top:28px;border:1px solid var(--line);border-radius:var(--rad);
 overflow:hidden;background:var(--panel)}
.gz-seg__b{border:0;background:none;color:var(--dim);cursor:pointer;padding:11px 20px;
 font:500 14px 'Tektur',Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;
 transition:background .2s,color .2s}
.gz-seg__b.is-on{background:var(--acc);color:#fff}
.gz-st__grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(212px,1fr));gap:12px;margin-top:26px}
/* height:100% — <button> в гриде не тянется по строке сам, и карточки
   с подписью в одну строку оказываются ниже соседей */
.gz-st__i{padding:0;border:1px solid var(--line);border-radius:var(--rad);background:var(--panel);
 color:inherit;text-align:left;font:inherit;overflow:hidden;display:block;height:100%;
 transition:border-color .2s ease,transform .2s ease}
button.gz-st__i{cursor:pointer}
button.gz-st__i:hover{border-color:var(--acc);transform:translateY(-3px)}
.gz-st__ph{position:relative;display:block;aspect-ratio:440/271;background:#f4f2ee}
.gz-st__ph picture{display:block;height:100%}
.gz-st__ph img{width:100%;height:100%;object-fit:cover}
.gz-st__a,.gz-st__b{position:absolute;inset:0;transition:opacity .45s ease}
.gz-st__b{opacity:0;background:#000;display:block}
.gz-st__b img{object-fit:contain;background:#000}
.gz-st.is-film .gz-st__i:not(.no-pair) .gz-st__a{opacity:0}
.gz-st.is-film .gz-st__i:not(.no-pair) .gz-st__b{opacity:1}
.gz-st.is-film .no-pair .gz-st__a{opacity:.32}
.gz-st__n{position:absolute;left:7px;top:7px;font-family:'Tektur',Arial,sans-serif;font-size:11px;
 letter-spacing:.06em;padding:3px 7px;border-radius:3px;background:rgba(6,8,12,.72);color:#fff}
.gz-st__tc{position:absolute;right:7px;bottom:7px;font-family:'Tektur',Arial,sans-serif;font-size:10.5px;
 letter-spacing:.08em;padding:3px 7px;border-radius:3px;background:rgba(6,8,12,.82);color:var(--acc2)}
.gz-st__tc.no{color:#C9A227;background:rgba(6,8,12,.86);text-transform:none;letter-spacing:.02em}
.gz-st__c{display:block;padding:11px 13px 14px;color:var(--dim);font-size:13.5px;line-height:1.42}

/* ── БУМАГА ПРОТИВ ЭКРАНА ────────────────────────────────────────────── */
.gz-diffs{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
.gz-diffs__grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(268px,1fr));gap:16px;margin-top:34px}
.gz-diff{border:1px solid var(--line);border-radius:var(--rad);background:var(--panel);padding:22px}
.gz-diff__h{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-bottom:12px;
 font-family:'Tektur',Arial,sans-serif;font-size:14px;text-transform:uppercase;letter-spacing:.03em}
.gz-diff__h .was{color:var(--dim);text-decoration:line-through;text-decoration-color:rgba(255,255,255,.3)}
.gz-diff__h .arr{color:var(--acc2)}
.gz-diff__h .now{color:var(--ink)}
.gz-diff p{margin:0;color:var(--dim);font-size:15px}

/* ── ПРОИЗВОДСТВО ────────────────────────────────────────────────────── */
.gz-prod{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
.gz-stages{list-style:none;margin:32px 0 0;padding:0;display:grid;
 grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:1px;background:var(--line);
 border:1px solid var(--line);border-radius:var(--rad);overflow:hidden}
.gz-stages li{background:var(--panel);padding:15px 18px;display:flex;gap:12px;align-items:baseline;
 font-size:15px}
.gz-stage__n{font-family:'Tektur',Arial,sans-serif;font-size:11px;color:var(--acc2);flex:none}
.gz-shifts{display:grid;grid-template-columns:repeat(auto-fit,minmax(226px,1fr));gap:16px;margin-top:22px}
.gz-shifts div{border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:var(--rad);
 background:var(--panel);padding:18px 20px}
.gz-shifts b{display:block;font-family:'Tektur',Arial,sans-serif;font-size:13px;letter-spacing:.1em;
 text-transform:uppercase;margin-bottom:6px}
.gz-shifts span{color:var(--dim);font-size:14.5px}
.gz-lists{display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:18px;margin-top:22px}
.gz-lists h3{font-size:14px;margin-bottom:12px;color:var(--acc2)}
.gz-lists ul{list-style:none;margin:0;padding:0}
.gz-lists li{padding:9px 0;border-bottom:1px solid var(--line);color:var(--dim);font-size:14.5px}

/* ── ЛОКАЦИЯ И ГРАФИКА ───────────────────────────────────────────────── */
.gz-loc,.gz-gfx{padding:clamp(50px,8vw,96px) 0;border-top:1px solid var(--line)}
.gz-loc__grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:16px;margin-top:34px}
.gz-gfx__grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-top:34px}
.gz-loc figure,.gz-gfx figure{margin:0}
.gz-loc img,.gz-gfx img{border:1px solid var(--line);border-radius:var(--rad);width:100%}
.gz-loc figcaption,.gz-gfx figcaption{margin-top:9px;font-family:'Tektur',Arial,sans-serif;font-size:11px;
 letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}

/* ── ТИТРЫ ───────────────────────────────────────────────────────────── */
.gz-credits{padding:clamp(50px,8vw,96px) 0 clamp(56px,9vw,110px);border-top:1px solid var(--line)}
.gz-credits__grid{margin-top:32px;display:grid;grid-template-columns:repeat(auto-fit,minmax(272px,1fr));
 gap:0 40px}
.gz-credits__grid div{display:flex;justify-content:space-between;gap:18px;padding:13px 0;
 border-bottom:1px solid var(--line)}
.gz-credits__grid dt,.gz-credits__grid b{font-weight:400;color:var(--dim);font-size:14.5px}
.gz-credits__grid span{text-align:right;font-size:15px}
.gz-pack{margin-top:34px;display:inline-flex;align-items:center;gap:12px;border:1px solid var(--line);
 border-radius:var(--rad);padding:14px 20px;background:var(--panel);font-family:'Tektur',Arial,sans-serif;
 font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim)}
.gz-pack em{font-style:normal;color:var(--ink)}

@media(max-width:860px){
 .gz{font-size:16px}
 .gz-hero{min-height:auto;padding-top:34px}
 .gz-hero__bg img{object-position:center 55%}
 .gz-facts span{font-size:14px}
}
/* ландшафт телефона: герой не должен занимать три экрана */
@media(max-height:460px) and (orientation:landscape){
 .gz-hero{min-height:auto;padding:26px 0 30px}
 .gz-hero h1{font-size:clamp(30px,6vw,46px)}
 .gz-lead{margin-top:12px;font-size:15px}
 .gz-lock{margin-top:18px}
}
</style>'''


def hero():
    facts = ''.join(f'<li><b>{k}</b><span>{v}</span></li>' for k, v in FACTS)
    return f'''<section class="gz-hero">
<div class="gz-hero__bg">
{pic('hero-jam.jpg', 'Разбитая обочина вдоль пробки на вылетной магистрали', 'a', 1600, 900, lazy=False)}
{pic('hero-robot.jpg', 'Робот из ГАЗели шагает по той же обочине вдоль пробки', 'b', 1600, 900, lazy=False)}
</div>
<div class="gz__in">
<div class="gz-eyebrow">Video Production · ГАЗ + Eaton · 2013</div>
<h1>Газель-трансформер</h1>
<p class="gz-lead gz-swap"><span class="off">Вирусный ролик про блокировку дифференциала Eaton.
Реклама не машины, а одной опции в прайсе: синей кнопки на панели.</span><span class="on">Кнопка нажата.
Обочина, по которой не поедет ни одна маршрутка, стала дорогой.</span></p>
{lock_btn()}
<ul class="gz-facts">{facts}</ul>
</div></section>'''


def lock_btn(dock=False):
    cls = 'gz-lock gz-dock' if dock else 'gz-lock'
    idd = 'gzDock' if dock else 'gzLock'
    return (f'<button class="{cls}" id="{idd}" type="button" aria-pressed="false">'
            f'<span class="gz-lock__b" aria-hidden="true"><i></i></span>'
            f'<span class="gz-lock__t gz-swap"><span class="off">Включить блокировку</span>'
            f'<span class="on">Блокировка включена</span>'
            f'<small class="gz-swap"><span class="off">та самая синяя кнопка</span>'
            f'<span class="on">нажмите ещё раз, чтобы вернуть пробку</span></small></span></button>')


def tc(sec):
    return '%d:%02d' % (int(sec) // 60, int(sec) % 60)


def brief():
    frame = ''.join(f'<div><b>{k}</b><span>{v}</span></div>' for k, v in FRAME)
    cards = ''.join(f'<div class="gz-card"><h3>{t}</h3><p>{p}</p></div>' for t, p in LIMITS)
    return f'''<section class="gz-task gz-r"><div class="gz__in">
<div class="gz-eyebrow">Бриф</div>
<h2 class="gz-h2">Ролик, в котором нельзя ничего сравнивать</h2>
<p class="gz-sub">Заказчик просил видео по автотранспортной тематике, которое
показывает: с включённой блокировкой машина проходит там, где обычная встаёт.
Ролик нужен был как вирусный контент. Дальше начинались ограничения.</p>
<div class="gz-frame">{frame}</div>
<div class="gz-task__grid">{cards}</div>
<div class="gz-solve">
<h3>Решение: пусть это будет сон</h3>
<p>Во сне сравнивать не с чем и претензий к достоверности нет. Мы взяли ситуацию,
в которой бывал каждый: утро, пробка, маршрутка, все опаздывают, пассажиры давят
на водителя. Водитель знает, что у его машины есть суперсила, и решает ей
воспользоваться.</p>
<p>Так марка не сравнивает себя ни с кем, не шутит над собственной машиной и
не обещает лишнего: всё, что происходит на экране, происходит в голове у водителя.
А в последнем кадре камера возвращается на панель, и синяя кнопка оказывается
настоящей.</p>
</div></div></section>'''


def viral():
    rows = ''.join(
        f'<details class="gz-cr"{" open" if i == 0 else ""}>'
        f'<summary><b>{name}</b><span>{req}</span></summary>'
        f'<p>{ans}</p></details>'
        for i, (name, req, ans) in enumerate(VIRAL))
    return f'''<section class="gz-viral gz-r"><div class="gz__in">
<div class="gz-eyebrow">Что считать вирусным</div>
<h2 class="gz-h2">Шесть требований к ролику</h2>
<p class="gz-sub">Вирусным ролик делает не бюджет, а сходимость нескольких условий
сразу. Они были прописаны ещё до сценария: ниже требование из брифа и то, чем
на него ответил готовый ролик.</p>
<div class="gz-cr__list">{rows}</div>
</div></section>'''


def ideas():
    tabs = ''.join(
        f'<button class="gz-idea__t{" is-on" if i == len(IDEAS) - 1 else ""}" '
        f'type="button" data-i="{i}">{name}</button>'
        for i, (name, _d, _s) in enumerate(IDEAS))
    panes = ''.join(
        f'<div class="gz-idea__p{" is-on" if i == len(IDEAS) - 1 else ""}" data-i="{i}">'
        f'<span class="gz-idea__st{" ok" if st == "В работу" else ""}">{st}</span>'
        f'<p>{d}</p></div>'
        for i, (_n, d, st) in enumerate(IDEAS))
    return f'''<section class="gz-ideas gz-r"><div class="gz__in">
<div class="gz-eyebrow">Заходы</div>
<h2 class="gz-h2">Три сюжета на одну кнопку</h2>
<p class="gz-sub">До съёмки сюжет искали в трёх разных направлениях. Два первых
упирались в то же ограничение: машина в них выглядела беспомощной.</p>
<div class="gz-idea__tabs">{tabs}</div>
<div class="gz-idea__panes">{panes}</div>
</div></section>'''


def story():
    paired = sum(1 for _c, s in STORY if s is not None)
    items = []
    for i, (cap, sec) in enumerate(STORY, 1):
        num = '%02d' % i
        badge = (f'<span class="gz-st__tc">{tc(sec)}</span>' if sec is not None
                 else '<span class="gz-st__tc no">нет в ролике</span>')
        shot = (f'<span class="gz-st__b">{pic("f-%s.jpg" % num, cap)}</span>'
                if sec is not None else '')
        tag = 'button' if sec is not None else 'div'
        attr = (f' type="button" data-t="{sec}" '
                f'aria-label="Перемотать ролик на {tc(sec)}: {cap}"'
                if sec is not None else '')
        items.append(
            f'<{tag} class="gz-st__i{"" if sec is not None else " no-pair"}"{attr}>'
            f'<span class="gz-st__ph"><span class="gz-st__a">'
            f'{pic("sb/%s.jpg" % num, "Лист сториборда %d: %s" % (i, cap))}</span>'
            f'{shot}<span class="gz-st__n">{num}</span>{badge}</span>'
            f'<span class="gz-st__c">{cap}</span></{tag}>')
    return f'''<section class="gz-st gz-r" id="gzStory"><div class="gz__in">
<div class="gz-eyebrow">Сториборд</div>
<h2 class="gz-h2">Весь ролик нарисован до съёмки</h2>
<p class="gz-sub">Отрисовка и согласование сториборда — отдельные этапы тракта:
пока лист не утверждён, площадка не бронируется. Тридцать листов сюжета плюс
пэкшот, ниже они идут по порядку. {paired} из {len(STORY)} листов стоят в ролике
ровно так, как были нарисованы: не дошёл до экрана только крупный план механики.</p>
<div class="gz-seg" role="group" aria-label="Что показывать">
<button class="gz-seg__b is-on" type="button" data-m="art">Раскадровка</button>
<button class="gz-seg__b" type="button" data-m="film">Как сняли</button>
</div>
<div class="gz-st__grid">{''.join(items)}</div>
<p class="gz-sb__hint">Переключатель меняет все кадры разом. Клик по кадру
перематывает плеер ниже на этот момент.</p>
</div></section>'''


def diffs():
    cards = ''.join(
        f'<div class="gz-diff"><div class="gz-diff__h"><span class="was">{a}</span>'
        f'<span class="arr" aria-hidden="true">→</span><span class="now">{b}</span></div>'
        f'<p>{t}</p></div>' for a, b, t in DIFFS)
    return f'''<section class="gz-diffs gz-r"><div class="gz__in">
<div class="gz-eyebrow">Бумага против экрана</div>
<h2 class="gz-h2">Что изменилось по дороге</h2>
<p class="gz-sub">Сториборд рисуют, чтобы спорить на бумаге, а не на площадке.
Три вещи всё-таки поменялись между листом и монтажом.</p>
<div class="gz-diffs__grid">{cards}</div>
</div></section>'''


def production():
    stages = ''.join(
        f'<li><span class="gz-stage__n">{i:02d}</span>{s}</li>'
        for i, s in enumerate(STAGES, 1))
    shifts = ''.join(f'<div><b>{d}</b><span>{w}</span></div>' for d, w in SHIFTS)
    crew = ''.join(f'<li>{c}</li>' for c in CREW_LIST)
    gear = ''.join(f'<li>{g}</li>' for g in GEAR_LIST)
    pairs = ''.join(
        f'<div class="gz-pair">'
        f'<figure>{pic(photo, cap1)}<figcaption>{cap1}</figcaption></figure>'
        f'<figure>{pic(frame, cap2)}<figcaption>{cap2}</figcaption></figure>'
        f'<div class="gz-pair__tx"><h3>{title}</h3><p>{text}</p></div>'
        f'</div>' for photo, frame, title, text, cap1, cap2 in BTS)
    return f'''<section class="gz-prod gz-r"><div class="gz__in">
<div class="gz-eyebrow">Производство</div>
<h2 class="gz-h2">Двенадцать этапов и три смены</h2>
<p class="gz-sub">Тракт был расписан до старта, от согласования идеи до
цветокоррекции. Съёмка стоит в нём седьмым пунктом: к моменту выезда на площадку
спорить уже не о чем.</p>
<ol class="gz-stages">{stages}</ol>
<div class="gz-shifts">{shifts}</div>
<div class="gz-lists">
<div><h3>Смена</h3><ul>{crew}</ul></div>
<div><h3>Техника</h3><ul>{gear}</ul></div>
</div>
{pairs}
</div></section>'''


def location():
    return f'''<section class="gz-loc gz-r"><div class="gz__in">
<div class="gz-eyebrow">Локация</div>
<h2 class="gz-h2">Дорога, вдоль которой идёт другая дорога</h2>
<p class="gz-sub">Под сюжет нужна была не просто трасса, а трасса с параллельной
разбитой дорогой — и с разрешённым съездом на неё, чтобы знак стоял в кадре
и к съёмке не было вопросов. Такую нашли недалеко от Москвы.</p>
<div class="gz-loc__grid">
<figure>{pic('loc-1.jpg', 'Съезд с трассы на грунтовую дорогу, скаутинг локации')}
<figcaption>Скаутинг: съезд и знак</figcaption></figure>
<figure>{pic('loc-2.jpg', 'Размытая параллельная дорога в лужах, скаутинг локации')}
<figcaption>Скаутинг: та самая параллельная колея</figcaption></figure>
<figure>{pic('f-12.jpg', 'Кадр ролика: маршрутка уходит с асфальта мимо знака')}
<figcaption>Кадр из ролика: знак съезда в кадре</figcaption></figure>
</div>
</div></section>'''


def graphics():
    return f'''<section class="gz-gfx gz-r"><div class="gz__in">
<div class="gz-eyebrow">Графика</div>
<h2 class="gz-h2">Робот появился после съёмки</h2>
<p class="gz-sub">Сначала собрали модель, затем согласовали аниматику — траекторию
перемещения робота по кадру — и только после этого довели модель до финального
качества. Порядок важен: пока траектория не сходится с реальной перспективой
площадки, детализировать нечего.</p>
<div class="gz-gfx__grid">
<figure>{pic('f-16.jpg', 'Кадр ролика: маршрутка раскладывается в поле')}
<figcaption>Трансформация</figcaption></figure>
<figure>{pic('f-18.jpg', 'Кадр ролика: робот в полный рост на обочине')}
<figcaption>Финальная модель в кадре</figcaption></figure>
</div>
</div></section>'''


def film():
    return f'''<section class="gz-film gz-r"><div class="gz__in">
<div class="gz-eyebrow">Ролик</div>
<h2 class="gz-h2">Газель-трансформер</h2>
<div class="gz-film__box">
<video id="gzFilm" controls preload="none" playsinline
 poster="{IMG}/poster.jpg" width="1280" height="720">
<source src="{FILM}" type="video/mp4">
Ваш браузер не умеет показывать видео. <a href="{FILM}">Скачать ролик</a>.
</video></div>
<div class="gz-film__cap"><span>Хронометраж <b>1:42</b></span>
<span>Музыка <b>Becks V Menthol — Ultra Lust</b></span>
<span>Пэкшот кампании <b>azgaz.ru/elocker</b></span></div>
</div></section>'''


def spread():
    dots, prev = [], ''
    for i, (date, place, _txt, cls) in enumerate(SPREAD):
        year = date[-4:]
        # год подписываем только там, где он меняется: иначе шкала выглядит
        # как четыре одинаковых «2013» подряд
        label = year if year != prev else ''
        prev = year
        dots.append(
            f'<button class="gz-dot {cls}" type="button" data-i="{i}" '
            f'aria-label="{date}, {place}"><span class="gz-dot__y">{label}</span>'
            f'<span class="gz-dot__d"></span><span class="gz-dot__p">{place}</span></button>')
    dots = ''.join(dots)
    return f'''<section class="gz-spread gz-r"><div class="gz__in">
<div class="gz-eyebrow">Результат</div>
<h2 class="gz-h2">Ролик забрали себе</h2>
<p class="gz-sub">Никакого медийного размещения у ролика не было. Он разошёлся сам:
его выкладывали автомобильные паблики, магазины запчастей, шиномонтажи и просто
люди, каждый под своим заголовком.</p>
<div class="gz-stat">
<div><b>20 000</b><span>просмотров за первые сутки после появления в сети</span></div>
<div><b>1 место</b><span>в подборке Auto.Mail.ru «10 лучших роликов про наш автопром»</span></div>
<div><b>12 лет</b><span>ролик перезаливают до сих пор: последняя найденная копия датирована апрелем 2025</span></div>
</div>
<div class="gz-rail" id="gzRail">
<div class="gz-rail__line"></div>
<div class="gz-rail__dots">{dots}</div>
<p class="gz-rail__hint">Лента прокручивается вбок. Нажмите на точку — откроется копия.</p>
</div>
<div class="gz-note" id="gzNote"><b>10.06.2013 · Rutube</b>
<p>{SPREAD[0][2]}</p></div>
<blockquote class="gz-press"><p>«Реклама не конкретного автомобиля, а всего лишь опции!
Не перейдя по ссылке, трудно догадаться, что захватывающее и качественно снятое
видео рекламирует… блокировку межколёсного дифференциала»</p>
<small>Auto.Mail.ru, <a href="{MAILRU}" target="_blank" rel="noopener nofollow">подборка
«10 лучших роликов про наш автопром»</a>, 9 января 2014</small></blockquote>
<p class="gz-disc">На ленте собраны копии, которые находятся поиском на 2026 год. Полного
списка не существует: ролик расползся по частным аккаунтам и пабликам, и свести
просмотры по всем копиям невозможно.</p>
</div></section>'''


def credits():
    rows = ''.join(f'<div><b>{role}</b><span>{who}</span></div>' for role, who in CREDITS)
    return f'''<section class="gz-credits gz-r"><div class="gz__in">
<div class="gz-eyebrow">Титры</div>
<h2 class="gz-h2">Кто это снимал</h2>
<div class="gz-credits__grid">{rows}</div>
<div class="gz-pack">Пэкшот кампании&nbsp;&nbsp;<em>www.azgaz.ru/elocker</em></div>
</div></section>'''


PAGE_JS = """<script>(function(){
var d=document,root=d.documentElement;

// появление секций
var io=window.IntersectionObserver?new IntersectionObserver(function(es){
 es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});
},{rootMargin:'0px 0px -8% 0px'}):null;
[].forEach.call(d.querySelectorAll('.gz-r,.gz-rail'),function(n){io?io.observe(n):n.classList.add('in');});

// ── синяя кнопка: переключает состояние всей страницы ──
var locks=[].slice.call(d.querySelectorAll('.gz-lock'));
function setLock(on){
 root.setAttribute('data-lock',on?'on':'off');
 locks.forEach(function(b){b.setAttribute('aria-pressed',on?'true':'false');});
 if(on&&window.ym)try{ym(71125393,'reachGoal','gaz_lock');}catch(e){}
}
locks.forEach(function(b){b.addEventListener('click',function(){
 setLock(root.getAttribute('data-lock')!=='on');});});
setLock(false);

// липкая кнопка показывается, когда герой ушёл вверх
var hero=d.querySelector('.gz-hero'),dock=d.getElementById('gzDock');
if(hero&&dock&&window.IntersectionObserver){
 new IntersectionObserver(function(es){
  dock.classList.toggle('on',!es[0].isIntersecting);
 },{rootMargin:'-40% 0px 0px 0px'}).observe(hero);
}

// ── сториборд: переключатель «раскадровка / как сняли» ──
var story=d.getElementById('gzStory');
[].forEach.call(d.querySelectorAll('.gz-seg__b'),function(b){
 b.addEventListener('click',function(){
  var film=b.getAttribute('data-m')==='film';
  if(story)story.classList.toggle('is-film',film);
  [].forEach.call(d.querySelectorAll('.gz-seg__b'),function(n){
   n.classList.toggle('is-on',n===b);});
 });
});

// ── заходы: вкладки ──
var tabs=[].slice.call(d.querySelectorAll('.gz-idea__t')),
    panes=[].slice.call(d.querySelectorAll('.gz-idea__p'));
tabs.forEach(function(b){b.addEventListener('click',function(){
 var i=b.getAttribute('data-i');
 tabs.forEach(function(n){n.classList.toggle('is-on',n===b);});
 panes.forEach(function(n){n.classList.toggle('is-on',n.getAttribute('data-i')===i);});
});});

// ── лист сториборда перематывает плеер ──
var film=d.getElementById('gzFilm');
[].forEach.call(d.querySelectorAll('.gz-st__i[data-t]'),function(b){
 b.addEventListener('click',function(){
  if(!film)return;
  var t=parseFloat(b.getAttribute('data-t'))||0;
  film.scrollIntoView({block:'center',behavior:'smooth'});
  function seek(){film.currentTime=t;var p=film.play();if(p&&p.catch)p.catch(function(){});}
  if(film.readyState>0){seek();}
  else{film.preload='auto';film.load();film.addEventListener('loadedmetadata',seek,{once:true});}
 });
});

// ── лента расползания ──
var NOTES=[__NOTES__],dots=[].slice.call(d.querySelectorAll('.gz-dot')),note=d.getElementById('gzNote');
function show(i){
 dots.forEach(function(n,k){n.classList.toggle('is-on',k===i);});
 if(note)note.innerHTML='<b>'+NOTES[i][0]+' · '+NOTES[i][1]+'</b><p>'+NOTES[i][2]+'</p>';
}
dots.forEach(function(b){
 b.addEventListener('click',function(){show(+b.getAttribute('data-i'));});
 b.addEventListener('mouseenter',function(){show(+b.getAttribute('data-i'));});
});
// точки проявляются по очереди — как копии, расходящиеся по площадкам
dots.forEach(function(n,k){n.style.transitionDelay=(k*0.06).toFixed(2)+'s';});
show(0);
})();</script>"""

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
                 '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"Газель-трансформер: вирусный ролик для ГАЗ и Eaton",'
                 '"item":"' + URL + '"}]}</script>')

VIDEO_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"VideoObject",'
            '"name":"Газель-трансформер","description":"Вирусный ролик о блокировке дифференциала Eaton '
            'для автомобилей ГАЗель Бизнес и Соболь. Маршрутка в утренней пробке превращается в робота '
            'и уходит по бездорожью.","thumbnailUrl":"https://hand-marketing.ru' + IMG + '/poster.jpg",'
            '"uploadDate":"2013-06-15","duration":"PT1M42S",'
            '"contentUrl":"https://hand-marketing.ru' + FILM + '",'
            '"publisher":{"@type":"Organization","name":"Hand Marketing"}}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Газель-трансформер: вирусный ролик для ГАЗ и Eaton | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: вирусный ролик «Газель-трансформер» о блокировке дифференциала Eaton для ГАЗель Бизнес и Соболь. Реклама одной опции, снятая за два дня на двух локациях: маршрутка в пробке превращается в робота. Ролик разошёлся сам и перезаливается с 2013 года.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Газель-трансформер | вирусный ролик для ГАЗ и Eaton">
<meta property="og:description" content="Рекламировать нужно было не машину, а опцию: блокировку дифференциала. Сравнивать было нельзя. Так родился сон водителя маршрутки, в котором ГАЗель становится роботом.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/og.jpg">
<meta property="og:site_name" content="Hand Marketing"><meta property="og:locale" content="ru_RU">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/tektur-rubik.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def js():
    notes = ','.join("['%s','%s','%s']" % (dt, pl, tx.replace("'", "\\'"))
                     for dt, pl, tx, _c in SPREAD)
    return PAGE_JS.replace('__NOTES__', notes)


def build():
    return (HEAD + rc.header() + '<main class="gz">' + hero() + brief() + viral() +
            ideas() + story() + film() + diffs() + production() + location() +
            graphics() + spread() + credits() + lock_btn(dock=True) +
            '</main><a id="lead"></a>' +
            rc.footer() + rc.JS + js() + BREADCRUMB_LD + VIDEO_LD + '</body></html>')


if __name__ == '__main__':
    out = os.path.join(ROOT, 'video', 'gaz')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    # index-a2.html это деплой-источник (workflow переименовывает его в index.html)
    # и затёр бы кастомную страницу на проде.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('удалён устаревший index-a2.html')
    print('written', os.path.join(out, 'index.html'))
