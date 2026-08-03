#!/usr/bin/env python3
"""Генерит mirror/mmg/index.html — кейс «Рекламный фильм ТРЦ „Павелецкая Плаза"» (MMG).

Что было: запечённая Tilda-страница с одной сверстанной вручную секцией — текст
пересказывал бриф («задача / решение / результат»), а сам фильм лежал под кнопкой
и никак не был связан с текстом.

Дизайн-концепция: фильм снимали не «про красоту», а под лизинг — он должен был
продать метры в ТРЦ, который ещё строился. Поэтому страница разобрана как
аргументация для арендатора и повторяет графику самого фильма: бордовые плашки
MMG, цифры прямо из кадра, tenant mix и зоны охвата.

  • монтажный лист: одиннадцать глав, клик перематывает плеер и подсвечивает
    текущую главу по ходу воспроизведения;
  • каждая цифра локации — кнопка: открывает эпизод, где эта плашка появляется
    в фильме, картинка в карточке снята с того же места;
  • интерактив, который в фильме показан анимацией: зоны охвата (первичная и
    20-минутная), кольцевые датчики готовности 70 % и 56,4 % GLA, живой
    tenant-mix-пончик по восьми категориям;
  • шторка «архив → проект» на Павелецкой площади — тот самый кросс-фейд с 0:38;
  • картинки — кадры фильма (scripts/mmg-assets.py), рендеры и съёмка принадлежат
    проекту, своей фотосъёмки по кейсу нет.

Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import os
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

URL = 'https://hand-marketing.ru/mmg/'
IMG = '/images/mmg'
VIDEO = '/portfolio/mmg/brand-video.mp4'
DUR = 337  # 5:37


# ─── монтажный лист фильма ──────────────────────────────────────────────────
# секунда, название главы, что в кадре
CHAPTERS = [
    (0,   'Пролог',      'MMG представляет'),
    (24,  'Место',       'Павелецкая площадь, архив'),
    (60,  'Тренды',      'Восемь принципов'),
    (76,  'Архитектура', 'Бюро 5+ design'),
    (92,  'Локация',     'Цифры вокруг ТРЦ'),
    (140, 'Охват',       'Зоны и радиусы'),
    (184, 'Аудитория',   'Уличные интервью'),
    (212, 'Стройка',     'Готовность 70 %'),
    (236, 'Арендаторы',  'Подписано 56,4 % GLA'),
    (250, 'Голоса',      '«Эконика» и «Теремок»'),
    (302, 'Финал',       'Команда проекта'),
]

# ─── четыре слоя материала, из которых собран фильм ─────────────────────────
LAYERS = [
    ('Аэросъёмка', 100,
     'Локация и масштаб: Садовое кольцо, вокзал, пятно застройки с воздуха.'),
    ('Коммерческие кадры', 118,
     'Фон под инфографику: трафик, потоки людей, фасады вокруг площадки.'),
    ('Интервью арендаторов', 250,
     'Основатели сетей, которые уже подписали договор, — залог успешности объекта.'),
    ('Уличные интервью', 184,
     'Будущие покупатели у вокзала — подтверждение выбора места и концепции.'),
]

# ─── цифры локации: значение, подпись, секунда, кадр ────────────────────────
NUMBERS = [
    ('3,1 млн',   'человек в зоне охвата',                104, 'num-1'),
    ('120 тыс.',  'автомобилей в сутки по Садовому',      118, 'num-2'),
    ('73 000 м²', 'GBA — общая площадь комплекса',        124, 'num-3'),
    ('33 000 м²', 'GLA — площади под аренду',             126, 'num-3b'),
    ('12',        'маршрутов общественного транспорта',   130, 'num-4'),
    ('140 тыс.',  'человек в сутки через вокзал и метро', 133, 'num-5'),
    ('125 тыс.',  'человек «дневного» населения района',  137, 'num-6'),
]

# ─── зоны охвата: подпись, радиус на схеме (%), цифра, пояснение, секунда ───
ZONES = [
    ('Первичная зона', 42, '450 тыс.', 'человек живут и работают рядом с площадью', 170),
    ('15–20 минут на авто', 86, 'более 3 млн', 'человек в транспортной доступности', 166),
]

# ─── уличные интервью ───────────────────────────────────────────────────────
STREET = [
    ('Сергей', 'офисный сотрудник', 186, 'st-1'),
    ('Василий', 'студент',          194, 'st-2'),
    ('Юлия',   'домохозяйка',       204, 'st-3'),
]

# ─── говорящие головы: имя, роль, секунда, кадр, о чём эпизод ───────────────
VOICES = [
    ('Анаделия Роблес', 'Старший партнёр архитектурного бюро 5+ design', 76, 'ex-1',
     'Архитектор объекта объясняет концепцию: почему у комплекса зелёная кровля, '
     'общественные пространства и стеклянный купол.'),
    ('Сергей Саркисов', 'Основатель обувной сети «Эконика»', 250, 'ex-2',
     'Арендатор, который зашёл в проект на стадии стройки, — про решение и ожидания '
     'от локации.'),
    ('Михаил Гончаров', 'Основатель компании «Теремок»', 276, 'ex-3',
     'Второй якорный голос: как сеть общепита оценивает трафик Павелецкой площади.'),
]

# ─── tenant mix: доля, категория (сумма 100 %) ──────────────────────────────
MIX = [
    (47, 'Одежда и обувь'),
    (20, 'Еда и гастрономия'),
    (11, 'Спорт'),
    (9,  'Красота и здоровье'),
    (5,  'Товары для дома'),
    (4,  'Ювелирные изделия и аксессуары'),
    (2,  'Электроника'),
    (2,  'Услуги и сервисы'),
]

# бренды, которые фильм показывает на слайде подписанных договоров
BRANDS = ['HENDERSON', '«Эконика»', 'Reebok', '«Перекрёсток»', 'STREET BEAT', 'adidas',
          '«Золотое яблоко»', 're:Store', 'Samsung', '«Рив Гош»', 'Soul in the Bowl',
          '«Гамарджоба, генацвале!»', '«Слепая курица»', 'Greek Street', '12STOREEZ',
          'Hunkemöller', 'Osteria Mario']

# ─── восемь трендов торговой недвижимости (слайд 1:14) ──────────────────────
# подпись, path иконки в сетке 24×24
TRENDS = [
    ('Окружающая среда',
     'M20.5 3.5c0 9.6-4.8 14.4-12 14.4H4.6c0-8.2 5.2-13.3 12.3-13.5 1.7 0 2.8-.4 3.6-.9z'
     ' M4.6 20.5c2.6-6.7 6.4-10.7 11.4-12.4'),
    ('Общественные пространства',
     'M3.5 13.2h17 M3.5 16.4h17 M6.2 13.2v6.6 M17.8 13.2v6.6'
     ' M5.4 9.6h13.2 M5.4 9.6v3.6 M18.6 9.6v3.6'),
    ('Развлечения',
     'M12 3.5v3 M12 17.5v3 M4.4 4.4l2.1 2.1 M17.5 17.5l2.1 2.1 M3.5 12h3 M17.5 12h3'
     ' M4.4 19.6l2.1-2.1 M17.5 6.5l2.1-2.1 M12 9.6a2.4 2.4 0 1 0 0 4.8 2.4 2.4 0 0 0 0-4.8z'),
    ('Культура',
     'M4.6 4.2h14.8v6.6c0 4.3-3.3 7.8-7.4 7.8s-7.4-3.5-7.4-7.8z'
     ' M9.2 9.2v1.6 M14.8 9.2v1.6 M9 13.6c1.9 1.6 4.1 1.6 6 0'),
    ('Дети',
     'M9 7.5a2.1 2.1 0 1 0 0-4.2 2.1 2.1 0 0 0 0 4.2z'
     ' M16.6 8.4a2 2 0 1 0 0-4 2 2 0 0 0 0 4z'
     ' M4.5 20.5v-4.2A4.5 4.5 0 0 1 9 11.8a4.5 4.5 0 0 1 4.5 4.5v4.2'
     ' M15 20.5v-3.2a3.4 3.4 0 0 1 3.4-3.4 3.1 3.1 0 0 1 3.1 3.1v3.5'),
    ('Питание',
     'M6.4 3v4.4 M9.4 3v4.4 M12.4 3v4.4'
     ' M6.4 7.4h6a3 3 0 0 1-3 3 3 3 0 0 1-3-3z M9.4 10.4V21'
     ' M18.6 3c1.6 1.3 2.3 3.1 2.3 5.1s-1 3.2-2.3 3.2V21'),
    ('Пункты выдачи',
     'M4 8.4 12 4l8 4.4v7.2L12 20l-8-4.4z M4 8.4 12 12.9l8-4.5 M12 12.9V20 M8 6.2l8 4.4'),
    ('Лояльность',
     'M12 20.4S4.2 15.8 4.2 10.7A4.5 4.5 0 0 1 12 7.5a4.5 4.5 0 0 1 7.8 3.2'
     'c0 5.1-7.8 9.7-7.8 9.7z'),
]

# ─── команда проекта (финальный слайд 5:32) ─────────────────────────────────
TEAM = [
    ('Plaza B.V.',   'Собственник и девелопер'),
    ('5+ design',    'Архитектор'),
    ('MMG',          'Управляющая компания и брокер'),
    ('Apex project bureau', 'Проектное бюро'),
    ('ANT YAPI',     'Генеральный подрядчик'),
    ('CBRE',         'Консультант проекта'),
    ('Knight Frank', 'Консультант проекта'),
]

# ─── что вошло в производство ───────────────────────────────────────────────
CRAFT = [
    ('Сценарий',
     'Не хроника стройки, а аргументация: локация → трафик → аудитория → '
     'готовность → спрос. Каждый эпизод закрывает своё возражение арендатора.'),
    ('Аэросъёмка',
     'Садовое кольцо, вокзал, пятно застройки и стройплощадка с воздуха — '
     'масштаб проекта одним кадром.'),
    ('Съёмка на действующей стройке',
     'Работа на объекте в финальной стадии: согласование доступа, СИЗ, '
     'графика смен и техники.'),
    ('Шесть интервью',
     'Архитектор проекта, два основателя сетей-арендаторов и три горожанина '
     'у вокзала — разные типы доказательства в одном фильме.'),
    ('Инфографика',
     'Плашки с цифрами, карта квартала, зоны охвата и диаграмма tenant mix — '
     'графика ложится на коммерческие кадры, снятые под неё заранее.'),
    ('Постпродакшн',
     'Монтаж, цветокоррекция, звук и дикторский текст: 5 минут 37 секунд '
     'финального хронометража.'),
]


def mmss(sec):
    return f'{sec // 60}:{sec % 60:02d}'


# ─── CSS ────────────────────────────────────────────────────────────────────
PAGE_CSS = """<style id="pp-css">
.pp{
 --paper:#FFFFFF;--bg:#F1EDE7;--bg2:#E7E1D8;
 --ink:#15171B;--ink2:#3A3D44;--mut:#767069;
 --wine:#75182D;--wine2:#9E2338;--wine-d:#54101F;
 --amber:#C08A2E;--line:rgba(21,23,27,.12);--line2:rgba(21,23,27,.22);
 --mono:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;
 --e:cubic-bezier(.16,1,.3,1);
 background:var(--bg);color:var(--ink2);
 font-family:'Onest',-apple-system,BlinkMacSystemFont,Arial,sans-serif;
 font-size:17px;line-height:1.62;-webkit-font-smoothing:antialiased;overflow-x:clip}
.pp *{box-sizing:border-box}
.pp ::selection{background:var(--wine);color:#fff}
/* height:auto обязателен: атрибут height у <img> иначе перебивает aspect-ratio */
.pp img{max-width:100%;display:block;height:auto}
.pp h1,.pp h2,.pp h3,.pp h4{font-family:'Manrope',Arial,sans-serif;color:var(--ink);
 letter-spacing:-.025em;margin:0;font-weight:800;line-height:1.08}
.pp p{margin:0 0 16px}
.pp__w{max-width:1180px;margin:0 auto;padding:0 28px}
@media(max-width:640px){.pp__w{padding:0 18px}}
.pp__s{padding:74px 0}
@media(min-width:840px){.pp__s{padding:96px 0}}
.pp__s--paper{background:var(--paper)}
.pp__s--dark{background:#141013;color:#C9C2BC}
.pp__s--dark h2,.pp__s--dark h3{color:#fff}

/* метка секции */
.pp__lab{display:flex;align-items:center;gap:13px;font-family:var(--mono);font-size:12px;
 letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin:0 0 20px}
.pp__lab::before{content:"";width:24px;height:3px;background:var(--wine)}
.pp__lab b{color:var(--ink);font-weight:600}
.pp__s--dark .pp__lab b{color:#fff}
.pp__h2{font-size:clamp(27px,5.2vw,42px);max-width:16em;margin:0 0 18px}
.pp__intro{max-width:60ch;color:var(--ink2);font-size:clamp(16px,3.6vw,18px)}
.pp__s--dark .pp__intro{color:#B5ACA6}

/* плашка-цитата графики фильма */
.pp__plate{display:inline-block;background:var(--wine);color:#fff;padding:6px 14px;
 font:700 13px/1.2 'Manrope',Arial,sans-serif;letter-spacing:.02em}

/* ── ГЕРОЙ ── */
.pp__hero{position:relative;isolation:isolate;overflow:hidden;color:#EDE7E2;
 padding:86px 0 66px;background:#100C0E}
.pp__hero::before{content:"";position:absolute;inset:0;z-index:-2;
 background:#100C0E url('""" + IMG + """/hero.jpg') center 30%/cover no-repeat;opacity:.52}
.pp__hero::after{content:"";position:absolute;inset:0;z-index:-1;
 background:linear-gradient(104deg,rgba(16,12,14,.95) 0%,rgba(16,12,14,.72) 46%,rgba(117,24,45,.42) 100%),
 linear-gradient(180deg,rgba(16,12,14,.2) 40%,rgba(16,12,14,.9) 100%)}
.pp__hero h1{color:#fff;font-size:clamp(38px,8.2vw,80px);margin:0 0 6px}
.pp__hero h1 em{font-style:normal;color:#E8A0AE}
.pp__kick{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:center;margin:0 0 26px;
 font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase}
.pp__kick span{border:1px solid rgba(255,255,255,.28);padding:5px 12px;color:#E3DAD5}
.pp__kick span.hot{background:var(--wine);border-color:var(--wine);color:#fff;font-weight:600}
.pp__sub{font-size:clamp(17px,4.2vw,21px);color:#D8CFC9;max-width:640px;margin:20px 0 30px}
.pp__act{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.pp__btn{display:inline-flex;align-items:center;gap:10px;border:0;cursor:pointer;
 padding:15px 26px;background:var(--wine);color:#fff;white-space:nowrap;
 font:700 15px 'Manrope',Arial,sans-serif;transition:background .2s var(--e),transform .2s var(--e)}
.pp__btn:hover{background:var(--wine2);transform:translateY(-2px)}
.pp__btn svg{width:14px;height:14px;fill:currentColor}
.pp__ghost{display:inline-flex;align-items:center;gap:9px;border:1px solid rgba(255,255,255,.34);
 background:transparent;color:#fff;padding:14px 24px;cursor:pointer;white-space:nowrap;
 font:600 15px 'Manrope',Arial,sans-serif;text-decoration:none;transition:.2s var(--e)}
.pp__ghost:hover{border-color:#fff;background:rgba(255,255,255,.08)}
.pp__ghost svg{width:13px;height:13px;fill:currentColor}
.pp__award{display:inline-flex;align-items:center;gap:11px;margin:30px 0 0;padding:11px 18px 11px 14px;
 border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.05);max-width:420px}
.pp__award svg{width:26px;height:26px;flex:none;fill:none;stroke:#E8A0AE;stroke-width:1.6}
.pp__award b{display:block;color:#fff;font:700 13px 'Manrope',Arial,sans-serif;letter-spacing:.01em}
.pp__award i{font-style:normal;font-size:12px;color:#B9AEA9}
.pp__facts{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;margin:44px 0 0;max-width:820px;
 background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.16)}
@media(min-width:780px){.pp__facts{grid-template-columns:repeat(4,1fr)}}
.pp__facts div{background:rgba(16,12,14,.72);padding:15px 17px}
.pp__facts dt{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
 color:#B0A49F;margin:0 0 5px}
.pp__facts dd{margin:0;color:#fff;font:700 15px 'Manrope',Arial,sans-serif}

/* ── ПЛЕЁР И МОНТАЖНЫЙ ЛИСТ ── */
.pp__film{background:#000;border:1px solid var(--line);overflow:hidden}
.pp__film video{width:100%;height:auto;display:block;aspect-ratio:16/9;background:#000}
.pp__chaps{display:grid;gap:1px;margin:1px 0 0;background:var(--line);
 grid-template-columns:repeat(2,1fr);border:1px solid var(--line);border-top:0}
/* глав 11, цифр 7 — хвост сетки добираем пустой плиткой, иначе в углу зияет фон */
.pp__fill{background:var(--paper)}
@media(min-width:700px){.pp__chaps{grid-template-columns:repeat(4,1fr)}}
@media(min-width:1000px){.pp__chaps{grid-template-columns:repeat(6,1fr)}}
.pp__chap{background:var(--paper);border:0;cursor:pointer;text-align:left;padding:13px 14px 15px;
 font-family:inherit;transition:background .18s var(--e)}
.pp__chap b{display:block;color:var(--ink);font:700 14px 'Manrope',Arial,sans-serif;margin-bottom:3px}
.pp__chap i{font-style:normal;display:block;font-family:var(--mono);font-size:11px;
 letter-spacing:.04em;color:var(--mut);line-height:1.35}
.pp__chap:hover{background:var(--bg2)}
.pp__chap[aria-current=true]{background:var(--wine)}
.pp__chap[aria-current=true] b{color:#fff}
.pp__chap[aria-current=true] i{color:rgba(255,255,255,.72)}

/* ── ЗАДАЧА И СЛОИ ── */
.pp__task{display:grid;gap:34px}
@media(min-width:900px){.pp__task{grid-template-columns:1fr 1fr;gap:56px}}
.pp__quote{border-left:3px solid var(--wine);padding:4px 0 4px 22px;margin:0 0 22px;
 font:600 clamp(19px,4.4vw,24px)/1.35 'Manrope',Arial,sans-serif;color:var(--ink);
 letter-spacing:-.02em}
.pp__layers{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
.pp__layer{background:var(--paper);border:0;text-align:left;cursor:pointer;padding:18px 20px;
 display:grid;grid-template-columns:34px 1fr;gap:14px;font-family:inherit;
 transition:background .18s var(--e)}
.pp__layer:hover{background:var(--bg2)}
.pp__layer span{font-family:var(--mono);font-size:12px;color:var(--wine);padding-top:3px}
.pp__layer b{display:block;color:var(--ink);font:700 16px 'Manrope',Arial,sans-serif;margin-bottom:4px}
.pp__layer p{margin:0;font-size:14.5px;color:var(--mut);line-height:1.5}
.pp__layer i{font-style:normal;font-family:var(--mono);font-size:11px;color:var(--wine);
 display:block;margin-top:7px}
.pp__dev{border:1px solid var(--line);background:var(--paper);padding:24px 24px 8px;margin:0 0 26px}
.pp__dev h3{font-size:19px;margin:0 0 10px}
.pp__dev p{font-size:15px;color:var(--mut)}

/* ── ШТОРКА АРХИВ/ПРОЕКТ ── */
.pp__ba{position:relative;overflow:hidden;border:1px solid var(--line);background:#000;
 aspect-ratio:16/9;touch-action:pan-y}
.pp__ba img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.pp__ba-top{clip-path:inset(0 0 0 var(--x,50%))}
.pp__ba-line{position:absolute;top:0;bottom:0;left:var(--x,50%);width:2px;background:#fff;
 box-shadow:0 0 0 1px rgba(0,0,0,.35);pointer-events:none}
.pp__ba-line::after{content:"";position:absolute;top:50%;left:50%;width:44px;height:44px;
 transform:translate(-50%,-50%);border:2px solid #fff;border-radius:50%;
 background:rgba(117,24,45,.85)}
.pp__ba input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;margin:0}
.pp__ba figcaption{position:absolute;left:0;right:0;bottom:0;display:flex;justify-content:space-between;
 padding:12px 14px;pointer-events:none}
.pp__ba figcaption span{background:rgba(16,12,14,.72);color:#fff;padding:5px 11px;
 font:600 12px/1.2 'Manrope',Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase}

/* ── ЦИФРЫ ЛОКАЦИИ ── */
.pp__nums{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
@media(min-width:620px){.pp__nums{grid-template-columns:repeat(2,1fr)}}
@media(min-width:960px){.pp__nums{grid-template-columns:repeat(4,1fr)}}
.pp__n{position:relative;background:var(--paper);border:0;cursor:pointer;text-align:left;
 padding:0;overflow:hidden;font-family:inherit;transition:background .18s var(--e)}
.pp__n img{width:100%;aspect-ratio:16/9;object-fit:cover;filter:saturate(.86);
 transition:transform .5s var(--e),filter .3s var(--e)}
.pp__n:hover img{transform:scale(1.045);filter:saturate(1)}
.pp__n-b{padding:16px 18px 20px}
.pp__n b{display:block;font:800 clamp(24px,4.6vw,30px)/1 'Manrope',Arial,sans-serif;
 color:var(--wine);letter-spacing:-.03em;margin-bottom:7px}
.pp__n span{display:block;font-size:14px;color:var(--ink2);line-height:1.45}
.pp__n i{font-style:normal;position:absolute;top:0;right:0;background:rgba(16,12,14,.72);color:#fff;
 font-family:var(--mono);font-size:11px;padding:4px 8px}
.pp__maps{display:grid;gap:18px;margin:34px 0 0}
@media(min-width:780px){.pp__maps{grid-template-columns:1.15fr 1fr}}
.pp__maps figure{margin:0;border:1px solid var(--line);background:var(--paper);
 display:flex;flex-direction:column}
.pp__maps figcaption{margin-top:auto}
.pp__maps img{width:100%;aspect-ratio:16/9;object-fit:cover}
.pp__maps figcaption{padding:12px 16px;font-size:13.5px;color:var(--mut)}
.pp__figbtn{display:block;width:100%;padding:0;border:0;background:none;cursor:pointer;
 overflow:hidden}
.pp__figbtn img{transition:transform .5s var(--e)}
.pp__wide{aspect-ratio:21/9;object-fit:cover;object-position:center 38%}
.pp__figbtn:hover img{transform:scale(1.035)}

/* ── ЗОНЫ ОХВАТА ── */
.pp__zone{display:grid;gap:34px;align-items:center}
@media(min-width:860px){.pp__zone{grid-template-columns:minmax(0,420px) 1fr;gap:56px}}
.pp__radar{position:relative;width:100%;max-width:420px;margin:0 auto}
.pp__radar svg{width:100%;height:auto;display:block}
.pp__radar .g{stroke:rgba(255,255,255,.14);fill:none}
.pp__radar .z,.pp__radar .z2{fill:none;stroke:rgba(232,118,138,.55);stroke-width:1.2;
 stroke-dasharray:5 6;transition:fill .5s var(--e),stroke .5s var(--e),stroke-width .5s var(--e)}
.pp__radar .z.act,.pp__radar .z2.act{fill:rgba(158,35,56,.32);stroke:#E8768A;stroke-width:2;
 stroke-dasharray:none}
.pp__radar .pin{fill:#fff}
.pp__radar .lbl{fill:#fff;font:600 13px 'Manrope',Arial,sans-serif}
.pp__zshot{display:block;width:100%;margin:14px 0 0;padding:0;border:1px solid rgba(255,255,255,.18);
 background:#1B1518;cursor:pointer;position:relative;overflow:hidden}
.pp__zshot img{width:100%;aspect-ratio:16/9;object-fit:cover;transition:opacity .3s var(--e)}
.pp__zshot:hover img{opacity:.85}
.pp__zshot span{position:absolute;left:0;bottom:0;background:rgba(16,12,14,.76);color:#fff;
 font:600 11px/1.2 'Manrope',Arial,sans-serif;padding:6px 10px;letter-spacing:.03em}
.pp__ztabs{display:flex;flex-wrap:wrap;gap:1px;background:rgba(255,255,255,.18);
 border:1px solid rgba(255,255,255,.18);margin:0 0 26px}
.pp__ztab{flex:1 1 180px;background:#1B1518;border:0;color:#C9C2BC;cursor:pointer;
 padding:13px 16px;text-align:left;font:600 14px 'Manrope',Arial,sans-serif;
 transition:background .2s var(--e),color .2s var(--e)}
.pp__ztab[aria-selected=true]{background:var(--wine);color:#fff}
.pp__zval{font:800 clamp(38px,8vw,64px)/1 'Manrope',Arial,sans-serif;color:#fff;
 letter-spacing:-.035em;margin:0 0 10px;display:block}
.pp__zdesc{color:#B5ACA6;max-width:34ch;margin:0 0 22px}
.pp__spend{display:grid;gap:1px;background:rgba(255,255,255,.18);
 border:1px solid rgba(255,255,255,.18);margin:34px 0 0}
@media(min-width:600px){.pp__spend{grid-template-columns:1fr 1fr}}
.pp__spend div{background:#1B1518;padding:20px 22px}
.pp__spend b{display:block;font:800 32px/1 'Manrope',Arial,sans-serif;color:#E8A0AE;margin-bottom:6px}
.pp__spend span{font-size:14px;color:#B5ACA6}
.pp__spend-shot{grid-column:1/-1;padding:0;border:0;background:#1B1518;cursor:pointer;display:block}
.pp__spend-shot img{width:100%;aspect-ratio:16/6;object-fit:cover;object-position:center 42%;
 transition:opacity .3s var(--e)}
.pp__spend-shot:hover img{opacity:.86}

/* ── КАРТОЧКИ-ПОРТРЕТЫ ── */
.pp__people{display:grid;gap:20px}
@media(min-width:640px){.pp__people{grid-template-columns:repeat(3,1fr)}}
.pp__p{position:relative;background:var(--paper);border:1px solid var(--line);cursor:pointer;
 text-align:left;padding:0;font-family:inherit;overflow:hidden;
 transition:transform .25s var(--e),box-shadow .25s var(--e)}
.pp__p:hover{transform:translateY(-3px);box-shadow:0 16px 34px -22px rgba(21,23,27,.6)}
.pp__p img{width:100%;aspect-ratio:1/1;object-fit:cover}
.pp__p-b{padding:15px 17px 18px}
.pp__p b{display:block;color:var(--ink);font:700 17px 'Manrope',Arial,sans-serif;margin-bottom:3px}
.pp__p span{display:block;font-size:14px;color:var(--mut)}
.pp__p p{margin:10px 0 0;font-size:14px;color:var(--ink2);line-height:1.5}
.pp__p i{font-style:normal;position:absolute;top:0;left:0;background:var(--wine);color:#fff;
 font-family:var(--mono);font-size:11px;padding:4px 9px}

/* ── ГОТОВНОСТЬ ── */
.pp__ready{display:grid;gap:30px;align-items:center}
@media(min-width:860px){.pp__ready{grid-template-columns:1fr 1fr;gap:50px}}
.pp__gauges{display:grid;grid-template-columns:1fr 1fr;gap:22px;max-width:460px}
.pp__g{text-align:center}
.pp__g svg{width:100%;height:auto;display:block}
.pp__g .tr{fill:none;stroke:var(--line);stroke-width:10}
.pp__g .bar{fill:none;stroke:var(--wine);stroke-width:10;stroke-linecap:round;
 transition:stroke-dashoffset 1.4s var(--e)}
.pp__g text{font-family:'Manrope',Arial,sans-serif;font-weight:800;fill:var(--ink)}
.pp__g b{display:block;margin:12px 0 2px;font:700 15px 'Manrope',Arial,sans-serif;color:var(--ink)}
.pp__g span{font-size:13.5px;color:var(--mut)}
.pp__shots{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:30px 0 0}
@media(min-width:760px){.pp__shots{grid-template-columns:repeat(4,1fr)}}
.pp__shots button{padding:0;border:1px solid var(--line);background:var(--paper);cursor:pointer;
 overflow:hidden;transition:transform .25s var(--e)}
.pp__shots button:hover{transform:translateY(-2px)}
.pp__shots img{width:100%;aspect-ratio:4/3;object-fit:cover}

/* ── TENANT MIX ── */
.pp__mix{display:grid;gap:34px;align-items:center}
@media(min-width:880px){.pp__mix{grid-template-columns:minmax(0,400px) 1fr;gap:52px}}
.pp__donut{position:relative;max-width:400px;margin:0 auto;width:100%}
.pp__donut svg{width:100%;height:auto;display:block;transform:rotate(-90deg)}
.pp__donut .sg{fill:none;stroke-width:30;cursor:pointer;transition:stroke-width .25s var(--e),opacity .25s var(--e)}
.pp__donut .sg:hover,.pp__donut .sg.on{stroke-width:38}
.pp__donut.has .sg:not(.on){opacity:.42}
.pp__dc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
 justify-content:center;text-align:center;pointer-events:none;padding:0 18%}
.pp__dc b{font:800 clamp(30px,7vw,44px)/1 'Manrope',Arial,sans-serif;color:var(--ink);
 letter-spacing:-.03em}
.pp__dc span{font-size:13px;color:var(--mut);line-height:1.35;margin-top:6px}
.pp__legend{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
.pp__legend button{display:grid;grid-template-columns:12px 1fr auto;gap:12px;align-items:center;
 background:var(--paper);border:0;cursor:pointer;text-align:left;padding:11px 16px;
 font-family:inherit;font-size:15px;color:var(--ink2);transition:background .18s var(--e)}
.pp__legend button:hover,.pp__legend button.on{background:var(--bg2)}
.pp__legend em{width:12px;height:12px;display:block}
.pp__legend b{font:700 15px 'Manrope',Arial,sans-serif;color:var(--ink)}
.pp__brands{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0 0}
.pp__brands span{border:1px solid var(--line2);padding:6px 13px;font-size:14px;color:var(--ink2);
 background:var(--paper)}
.pp__gla{display:grid;gap:20px;margin:0 0 40px;align-items:center}
@media(min-width:760px){.pp__gla{grid-template-columns:1fr 1fr}}
.pp__gla img{width:100%;aspect-ratio:16/9;object-fit:cover;border:1px solid var(--line)}

/* ── ТРЕНДЫ ── */
.pp__trends{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
@media(min-width:560px){.pp__trends{grid-template-columns:repeat(2,1fr)}}
@media(min-width:900px){.pp__trends{grid-template-columns:repeat(4,1fr)}}
.pp__t{background:var(--paper);padding:22px 20px 24px}
.pp__t svg{width:30px;height:30px;fill:none;stroke:var(--wine);stroke-width:1.5;
 stroke-linecap:round;stroke-linejoin:round;margin-bottom:12px}
.pp__t b{display:block;font:700 15px 'Manrope',Arial,sans-serif;color:var(--ink)}

/* галерея рендеров */
.pp__gal{display:grid;gap:12px;grid-template-columns:repeat(2,1fr)}
@media(min-width:820px){.pp__gal{grid-template-columns:repeat(3,1fr)}}
.pp__gal button{position:relative;padding:0;border:1px solid var(--line);background:var(--paper);
 cursor:pointer;overflow:hidden;display:block}
.pp__gal img{width:100%;aspect-ratio:16/9;object-fit:cover;transition:transform .5s var(--e)}
.pp__gal button:hover img{transform:scale(1.04)}
.pp__gal span{position:absolute;left:0;bottom:0;background:rgba(16,12,14,.76);color:#fff;
 font:600 12px/1.2 'Manrope',Arial,sans-serif;padding:6px 10px;letter-spacing:.02em}

/* ── КОМАНДА И ПРОДАКШН ── */
.pp__team{display:grid;gap:1px;background:rgba(255,255,255,.16);
 border:1px solid rgba(255,255,255,.16)}
@media(min-width:640px){.pp__team{grid-template-columns:repeat(2,1fr)}}
.pp__team div{background:#1B1518;padding:16px 20px;display:flex;flex-wrap:wrap;gap:4px 14px;
 align-items:baseline;justify-content:space-between}
.pp__team b{font:700 16px 'Manrope',Arial,sans-serif;color:#fff}
.pp__team span{font-size:13.5px;color:#B5ACA6}
.pp__team-fill{background:#1B1518}
.pp__craft{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
@media(min-width:700px){.pp__craft{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1040px){.pp__craft{grid-template-columns:repeat(3,1fr)}}
.pp__c{background:var(--paper);padding:24px 22px 26px}
.pp__c em{font-style:normal;font-family:var(--mono);font-size:11px;letter-spacing:.1em;
 color:var(--wine);display:block;margin-bottom:10px}
.pp__c b{display:block;font:700 17px 'Manrope',Arial,sans-serif;color:var(--ink);margin-bottom:8px}
.pp__c p{margin:0;font-size:14.5px;color:var(--mut);line-height:1.55}
.pp__fin{display:grid;gap:26px;align-items:center;margin:38px 0 0}
@media(min-width:820px){.pp__fin{grid-template-columns:1fr 1fr;gap:44px}}
.pp__fin img{width:100%;object-fit:cover;border:1px solid rgba(255,255,255,.16)}

/* появление */
.pp .r{opacity:0;transform:translateY(20px);transition:opacity .75s var(--e),transform .75s var(--e)}
.pp .r.is-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
 .pp .r{opacity:1;transform:none;transition:none}
 .pp *{transition:none!important;animation:none!important}}
.pp :focus-visible{outline:2px solid var(--wine2);outline-offset:2px}
.pp__s--dark :focus-visible{outline-color:#E8A0AE}
</style>"""


# ─── секции ─────────────────────────────────────────────────────────────────
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'
CUP = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4h10v5a5 5 0 0 1-10 0z"/>'
       '<path d="M7 6H4v1a4 4 0 0 0 3 3.9M17 6h3v1a4 4 0 0 1-3 3.9"/>'
       '<path d="M12 14v4M9 20h6"/></svg>')


def hero():
    facts = ''.join(f'<div><dt>{t}</dt><dd>{v}</dd></div>' for t, v in [
        ('Клиент', 'Mall Management Group'),
        ('Объект', 'ТРЦ «Павелецкая Плаза»'),
        ('Формат', 'Рекламный фильм'),
        ('Хронометраж', '5:37'),
    ])
    return f'''<section class="pp__hero"><div class="pp__w">
<div class="pp__kick"><span>Mall Management Group</span><span>Москва</span>
<span class="hot">Видеопродакшн</span></div>
<h1>Фильм, который<br><em>сдаёт метры</em></h1>
<p class="pp__sub">Рекламный ролик ТРЦ «Павелецкая Плаза» для будущих арендаторов.
Объект ещё строился, поэтому фильм должен был показать не бетон, а готовый поток:
локацию, трафик, аудиторию и спрос.</p>
<div class="pp__act">
<button class="pp__btn" type="button" data-seek="0">{PLAY}Смотреть фильм</button>
<a class="pp__ghost" href="#numbers">Цифры локации</a></div>
<div class="pp__award">{CUP}<span><b>MIPIM / AR Future Project Awards 2020</b>
<i>Победитель — знак стоит в открывающем кадре фильма</i></span></div>
<dl class="pp__facts">{facts}</dl>
</div></section>'''


def film():
    chaps = ''.join(
        f'<button class="pp__chap" type="button" data-seek="{s}" data-chap="{s}"'
        f' aria-current="{"true" if i == 0 else "false"}">'
        f'<b>{n}</b><i>{mmss(s)} · {c}</i></button>'
        for i, (s, n, c) in enumerate(CHAPTERS))
    return f'''<section class="pp__s pp__s--paper" id="film"><div class="pp__w">
<p class="pp__lab"><b>Фильм</b> · 5 минут 37 секунд</p>
<div class="pp__film r"><video id="pp-video" controls preload="none" playsinline
 poster="{IMG}/poster.jpg" width="1280" height="720">
<source src="{VIDEO}" type="video/mp4">Ваш браузер не воспроизводит видео.</video></div>
<div class="pp__chaps r" role="group" aria-label="Главы фильма">{chaps}<div class="pp__fill" aria-hidden="true"></div></div>
</div></section>'''


def task():
    layers = ''.join(
        f'<button class="pp__layer" type="button" data-seek="{s}">'
        f'<span>0{i + 1}</span><span><b>{n}</b><p>{d}</p>'
        f'<i>{mmss(s)} · открыть эпизод</i></span></button>'
        for i, (n, s, d) in enumerate(LAYERS))
    return f'''<section class="pp__s"><div class="pp__w">
<p class="pp__lab"><b>Задача</b> · зачем этот фильм</p>
<div class="pp__task">
<div>
<p class="pp__quote">Продать метры в торговом центре, которого ещё нет.</p>
<p class="pp__intro">ТРЦ был на финальной стадии строительства, а брокерам уже нужно было
показывать объект сетям. Задача звучала так: разработать сценарий ролика, который
демонстрирует высокую стадию готовности и ключевые преимущества для арендаторов,
снять и смонтировать фильм под этот нарратив.</p>
<p class="pp__intro">Мы собрали его не как экскурсию по стройке, а как аргументацию:
локация, трафик, аудитория, готовность, уже подписанные бренды. Стройку показали так,
чтобы арендатор увидел будущий поток — людей, место и спрос, а не бетон.</p>
<div class="pp__dev"><h3>О девелопере</h3>
<p>Mall Management Group занимается девелопментом объектов коммерческой недвижимости и
сопровождением полного цикла жизни проектов. MMG входит в группу Plaza B.V. и управляет
портфелем коммерческой недвижимости; «Павелецкая Плаза» — один из флагманских объектов
компании в Москве.</p></div>
</div>
<div><p class="pp__lab"><b>Материал</b> · четыре слоя съёмки</p>
<div class="pp__layers r">{layers}</div></div>
</div></div></section>'''


def place():
    return f'''<section class="pp__s pp__s--paper"><div class="pp__w">
<p class="pp__lab"><b>Место</b> · эпизод 0:24</p>
<h2 class="pp__h2">Площадь, у которой уже есть трафик</h2>
<p class="pp__intro">Фильм начинает разговор не с проекта, а с места: Павелецкая площадь
больше века собирает людей — вокзал, извозчики, рынок, метро. Кросс-фейд из архивной
съёмки в рендер — тот самый переход с 0:38, здесь он вынесен в ползунок.</p>
<figure class="pp__ba r" id="pp-ba" style="--x:52%">
<img src="{IMG}/was.jpg" width="1200" height="675" loading="lazy"
 alt="Павелецкая площадь на архивной съёмке из фильма">
<img class="pp__ba-top" src="{IMG}/now.jpg" width="1200" height="675" loading="lazy"
 alt="Павелецкая площадь в проекте ТРЦ «Павелецкая Плаза»">
<span class="pp__ba-line" aria-hidden="true"></span>
<input type="range" min="0" max="100" value="52" id="pp-ba-x"
 aria-label="Сравнить архивный кадр и проект">
<figcaption><span>Архив</span><span>Проект</span></figcaption>
</figure>
<div class="pp__maps r">
<figure><button type="button" data-seek="26" class="pp__figbtn">
<img src="{IMG}/hist-1.jpg" width="900" height="506" loading="lazy"
 alt="Кадр фильма: Павелецкий вокзал и извозчики на архивном снимке"></button>
<figcaption>Архивные снимки вокзала вошли в фильм отдельным эпизодом: 0:26.</figcaption></figure>
<figure><button type="button" data-seek="33" class="pp__figbtn">
<img src="{IMG}/hist-2.jpg" width="900" height="506" loading="lazy"
 alt="Кадр фильма: Павелецкий вокзал, архивная съёмка в сепии"></button>
<figcaption>Площадь больше века работает как точка притяжения: 0:33.</figcaption></figure>
</div>
<div class="pp__maps r">
<figure><button type="button" data-seek="100" class="pp__figbtn">
<img src="{IMG}/map-1.jpg" width="1200" height="675" loading="lazy"
 alt="Аэросъёмка: Садовое кольцо и пятно ТРЦ «Павелецкая Плаза»"></button>
<figcaption>Аэросъёмка привязывает объект к городу: Садовое кольцо, вокзал,
БЦ «Павелецкая Плаза».</figcaption></figure>
<figure><button type="button" data-seek="148" class="pp__figbtn">
<img src="{IMG}/map-2.jpg" width="1200" height="675" loading="lazy"
 alt="Схема квартала вокруг Павелецкой площади из фильма"></button>
<figcaption>Схема квартала: пятно комплекса, вокзал и выходы метро.</figcaption></figure>
</div>
</div></section>'''


def numbers():
    cards = ''.join(
        f'<button class="pp__n" type="button" data-seek="{s}">'
        f'<img src="{IMG}/{im}.jpg" width="760" height="428" loading="lazy"'
        f' alt="Кадр фильма: {v} — {d}"><i>{mmss(s)}</i>'
        f'<span class="pp__n-b"><b>{v}</b><span>{d}</span></span></button>'
        for v, d, s, im in NUMBERS)
    return f'''<section class="pp__s" id="numbers"><div class="pp__w">
<p class="pp__lab"><b>Локация</b> · эпизод 1:32</p>
<h2 class="pp__h2">Семь цифр, которые фильм показывает прямо в кадре</h2>
<p class="pp__intro">Инфографику не рисовали поверх готового монтажа: коммерческие кадры
снимали заранее как фон под плашки, поэтому цифра всегда стоит на своём объекте —
поток машин по Садовому, пассажиры вокзала, пятно застройки. Клик по карточке открывает
её эпизод в плеере.</p>
<div class="pp__nums r">{cards}<div class="pp__fill" aria-hidden="true"></div></div>
</div></section>'''


def zone():
    tabs = ''.join(
        f'<button class="pp__ztab" type="button" role="tab" data-z="{i}" data-seek="{s}"'
        f' aria-selected="{"true" if i == 0 else "false"}"'
        f' aria-controls="pp-zpanel">{n}</button>'
        for i, (n, _r, _v, _d, s) in enumerate(ZONES))
    z0 = ZONES[0]
    return f'''<section class="pp__s pp__s--dark"><div class="pp__w">
<p class="pp__lab"><b>Охват</b> · эпизод 2:20</p>
<h2 class="pp__h2">Две зоны, из которых придёт покупатель</h2>
<p class="pp__intro">В фильме это анимированная карта: сначала подсвечивается первичная
зона вокруг площади, потом кольцо двадцатиминутной доступности. Здесь она собрана
интерактивом — переключите зону, а кнопка откроет тот же момент в плеере.</p>
<div class="pp__zone r">
<div class="pp__radar"><svg viewBox="0 0 400 400" role="img"
 aria-label="Схема зон охвата ТРЦ «Павелецкая Плаза»">
<circle class="g" cx="200" cy="200" r="60"/><circle class="g" cx="200" cy="200" r="110"/>
<circle class="g" cx="200" cy="200" r="160"/><circle class="g" cx="200" cy="200" r="190"/>
<line class="g" x1="200" y1="8" x2="200" y2="392"/>
<line class="g" x1="8" y1="200" x2="392" y2="200"/>
<circle class="z2" id="pp-z2" cx="200" cy="200" r="176"/>
<circle class="z act" id="pp-z1" cx="200" cy="200" r="84"/>
<circle class="pin" cx="200" cy="200" r="6"/>
<text class="lbl" x="200" y="232" text-anchor="middle">Павелецкая</text>
</svg>
<button type="button" data-seek="168" class="pp__zshot">
<img src="{IMG}/zone.jpg" width="1100" height="619" loading="lazy"
 alt="Кадр фильма: карта зон охвата с цифрами 450 тыс. и более 3 млн человек">
<span>Кадр 2:48 в фильме</span></button></div>
<div id="pp-zpanel" role="tabpanel">
<div class="pp__ztabs" role="tablist" aria-label="Зоны охвата">{tabs}</div>
<b class="pp__zval" id="pp-zval">{z0[2]}</b>
<p class="pp__zdesc" id="pp-zdesc">{z0[3]}</p>
<button class="pp__ghost" type="button" id="pp-zseek" data-seek="{z0[4]}">{PLAY}Смотреть эпизод</button>
</div></div>
<div class="pp__spend r">
<div><b>+35 %</b><span>расходы аудитории района выше средних по городу</span></div>
<div><b>+18 %</b><span>доходы аудитории района выше средних по городу</span></div>
<button type="button" data-seek="176" class="pp__spend-shot">
<img src="{IMG}/spend.jpg" width="1000" height="563" loading="lazy"
 alt="Кадр фильма: плашки «расходы выше на 35 %» и «доходы выше на 18 %»"></button>
</div>
</div></section>'''


def street():
    cards = ''.join(
        f'<button class="pp__p" type="button" data-seek="{s}">'
        f'<i>{mmss(s)}</i><img src="{IMG}/{im}.jpg" width="620" height="620" loading="lazy"'
        f' alt="Кадр фильма: уличное интервью, {n}">'
        f'<span class="pp__p-b"><b>{n}</b><span>{r}</span></span></button>'
        for n, r, s, im in STREET)
    return f'''<section class="pp__s pp__s--paper"><div class="pp__w">
<p class="pp__lab"><b>Аудитория</b> · эпизод 3:04</p>
<h2 class="pp__h2">Спрос подтверждают не слайды, а люди у вокзала</h2>
<p class="pp__intro">Три коротких уличных интервью закрывают вопрос «а придёт ли сюда
покупатель»: офисный сотрудник, студент и мама с ребёнком — типажи, которые и формируют
дневной трафик площади.</p>
<div class="pp__people r">{cards}</div>
</div></section>'''


def ready():
    shots = ''.join(
        f'<button type="button" data-seek="{s}">'
        f'<img src="{IMG}/{im}.jpg" width="900" height="675" loading="lazy" alt="{a}"></button>'
        for im, s, a in [
            ('bd-1', 214, 'Кадр фильма: аэросъёмка стройплощадки'),
            ('bd-2', 222, 'Кадр фильма: купол комплекса изнутри'),
            ('bd-3', 226, 'Кадр фильма: монтаж светопрозрачной кровли'),
            ('bd-4', 229, 'Кадр фильма: чистовая отделка галереи')])
    return f'''<section class="pp__s"><div class="pp__w">
<p class="pp__lab"><b>Готовность</b> · эпизод 3:32</p>
<div class="pp__ready">
<div><h2 class="pp__h2">Стройка как аргумент, а не как оправдание</h2>
<p class="pp__intro">Съёмка шла на действующей площадке: аэросъёмка объёма, купол изнутри,
монтаж кровли, чистовая отделка галерей. Две цифры из фильма отвечают на главный вопрос
арендатора — успеет ли объект и есть ли на него спрос.</p></div>
<div class="pp__gauges r">
<div class="pp__g"><svg viewBox="0 0 120 120" role="img" aria-label="Готовность проекта 70 %">
<circle class="tr" cx="60" cy="60" r="50"/>
<circle class="bar" data-val="70" cx="60" cy="60" r="50" transform="rotate(-90 60 60)"
 stroke-dasharray="314" stroke-dashoffset="314"/>
<text x="60" y="67" text-anchor="middle" font-size="26">70 %</text></svg>
<b>Проект завершён</b><span>стадия на момент съёмки</span></div>
<div class="pp__g"><svg viewBox="0 0 120 120" role="img" aria-label="Подписано 56,4 % GLA">
<circle class="tr" cx="60" cy="60" r="50"/>
<circle class="bar" data-val="56.4" cx="60" cy="60" r="50" transform="rotate(-90 60 60)"
 stroke-dasharray="314" stroke-dashoffset="314"/>
<text x="60" y="67" text-anchor="middle" font-size="22">56,4 %</text></svg>
<b>Подписано GLA</b><span>договоры на момент выхода фильма</span></div>
</div></div>
<div class="pp__shots r">{shots}</div>
</div></section>'''


def mix():
    # сегменты пончика: окружность r=80, длина 502.65
    palette = ['#75182D', '#9E2338', '#B7404F', '#C86273', '#D68A95', '#C6B6AC',
               '#A79C93', '#8B8078']
    circ = 2 * 3.141592653589793 * 80
    segs, legend, off = '', '', 0.0
    for i, (pct, name) in enumerate(MIX):
        ln = circ * pct / 100
        segs += (f'<circle class="sg" data-i="{i}" cx="100" cy="100" r="80" '
                 f'stroke="{palette[i]}" stroke-dasharray="{ln:.2f} {circ - ln:.2f}" '
                 f'stroke-dashoffset="{-off:.2f}" tabindex="0" role="button" '
                 f'aria-label="{name} — {pct} процентов"></circle>')
        legend += (f'<button type="button" data-i="{i}"><em style="background:{palette[i]}"></em>'
                   f'<span>{name}</span><b>{pct} %</b></button>')
        off += ln
    brands = ''.join(f'<span>{b}</span>' for b in BRANDS)
    return f'''<section class="pp__s pp__s--paper"><div class="pp__w">
<p class="pp__lab"><b>Арендаторы</b> · эпизод 3:56</p>
<h2 class="pp__h2">К выходу фильма было подписано 56,4 % GLA</h2>
<div class="pp__gla r">
<img src="{IMG}/gla.jpg" width="900" height="506" loading="lazy"
 alt="Кадр фильма: плашка «Подписано уже 56,4 % GLA»">
<p class="pp__intro">Для арендатора это главный аргумент: половину площадей уже разобрали,
и структура пула понятна. Диаграмма tenant mix из фильма собрана здесь живой — наведите
на сегмент или выберите категорию в списке.</p>
</div>
<div class="pp__mix r">
<div class="pp__donut" id="pp-donut"><svg viewBox="0 0 200 200" role="img"
 aria-label="Структура арендаторов по категориям">{segs}</svg>
<div class="pp__dc"><b id="pp-dv">100 %</b><span id="pp-dn">площадей распределены
по восьми категориям</span></div></div>
<div><div class="pp__legend" id="pp-legend">{legend}</div>
<div class="pp__brands">{brands}</div></div>
</div>
<div class="pp__maps r" style="grid-template-columns:1fr;margin-top:34px">
<figure><button type="button" data-seek="246" class="pp__figbtn">
<img src="{IMG}/mix.jpg" width="1200" height="675" loading="lazy"
 alt="Кадр фильма: диаграмма tenant mix и логотипы подписанных брендов"></button>
<figcaption>Кадр 4:06 — слайд подписанных брендов в фильме.</figcaption></figure>
</div>
</div></section>'''


def voices():
    cards = ''.join(
        f'<button class="pp__p" type="button" data-seek="{s}">'
        f'<i>{mmss(s)}</i><img src="{IMG}/{im}.jpg" width="620" height="620" loading="lazy"'
        f' alt="Кадр фильма: {n}">'
        f'<span class="pp__p-b"><b>{n}</b><span>{r}</span><p>{d}</p></span></button>'
        for n, r, s, im, d in VOICES)
    return f'''<section class="pp__s"><div class="pp__w">
<p class="pp__lab"><b>Голоса</b> · эпизоды 1:16 и 4:10</p>
<h2 class="pp__h2">Три интервью вместо трёх обещаний</h2>
<p class="pp__intro">Архитектор объясняет замысел, основатели сетей рассказывают, почему
зашли в проект на стадии стройки. Для брокера это готовые референсы: если сюда идут
«Эконика» и «Теремок», объекту можно верить.</p>
<div class="pp__people r">{cards}</div>
</div></section>'''


def trends():
    items = ''.join(
        f'<div class="pp__t"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{p}"/></svg>'
        f'<b>{n}</b></div>' for n, p in TRENDS)
    gal = ''.join(
        f'<button type="button" data-seek="{s}">'
        f'<img src="{IMG}/{im}.jpg" width="1000" height="563" loading="lazy" alt="{a}">'
        f'<span>{c}</span></button>'
        for im, s, c, a in [
            ('ren-1', 14, 'Кровля-парк · 0:14', 'Рендер: парк на кровле комплекса'),
            ('ren-2', 16, 'Галерея · 0:16', 'Рендер: галерея под решётчатым куполом'),
            ('ren-3', 19, 'Атриум · 0:19', 'Рендер: атриум торговой галереи'),
            ('ren-6', 52, 'Площадь · 0:52', 'Рендер: площадь перед комплексом осенью'),
            ('ren-4', 312, 'Входная группа · 5:12', 'Рендер: входная группа комплекса'),
            ('ren-5', 318, 'Променад · 5:18', 'Рендер: променад под куполом')])
    return f'''<section class="pp__s pp__s--paper"><div class="pp__w">
<p class="pp__lab"><b>Концепция</b> · эпизод 1:00</p>
<h2 class="pp__h2">Восемь трендов, на которых построен объект</h2>
<p class="pp__intro">Этот слайд в фильме объясняет, чем «Павелецкая Плаза» отличается от
классического молла: половина смысла — не торговля, а среда. Иконки перерисованы
векторами по кадру 1:14.</p>
<div class="pp__trends r">{items}</div>
<div class="pp__maps r" style="grid-template-columns:1fr">
<figure><button type="button" data-seek="66" class="pp__figbtn">
<img src="{IMG}/trends.jpg" width="1000" height="563" loading="lazy"
 alt="Кадр фильма: слайд «Мы следуем мировым трендам в торговой недвижимости»"></button>
<figcaption>Кадр 1:14 — тот самый слайд в фильме.</figcaption></figure>
</div>
<p class="pp__lab" style="margin:56px 0 18px"><b>Объект</b> · рендеры из пролога и финала</p>
<div class="pp__gal r">{gal}</div>
</div></section>'''


def craft():
    items = ''.join(
        f'<div class="pp__c"><em>0{i + 1}</em><b>{n}</b><p>{d}</p></div>'
        for i, (n, d) in enumerate(CRAFT))
    team = ''.join(f'<div><b>{n}</b><span>{r}</span></div>' for n, r in TEAM)
    return f'''<section class="pp__s"><div class="pp__w">
<p class="pp__lab"><b>Продакшн</b> · что вошло в работу</p>
<h2 class="pp__h2">Сценарий, съёмка, графика, монтаж</h2>
<div class="pp__maps r" style="grid-template-columns:1fr;margin:0 0 26px">
<figure><button type="button" data-seek="304" class="pp__figbtn">
<img src="{IMG}/bd-5.jpg" width="900" height="506" loading="lazy" class="pp__wide"
 alt="Кадр фильма: обход стройплощадки ТРЦ «Павелецкая Плаза» с заказчиком"></button>
<figcaption>Съёмка шла на действующей площадке, вместе с обходами заказчика: 5:04.</figcaption>
</figure></div>
<div class="pp__craft r">{items}</div>
</div></section>
<section class="pp__s pp__s--dark"><div class="pp__w">
<p class="pp__lab"><b>Команда проекта</b> · финальный слайд 5:32</p>
<h2 class="pp__h2">Кто делал «Павелецкую Плазу»</h2>
<div class="pp__fin r">
<div class="pp__team">{team}<div class="pp__team-fill" aria-hidden="true"></div></div>
<div><button type="button" data-seek="330" class="pp__figbtn">
<img src="{IMG}/team.jpg" width="1100" height="619" loading="lazy"
 alt="Кадр фильма: финальный слайд «Команда проекта»"></button>
<p class="pp__intro" style="margin:18px 0 0">Фильм закрывается тем же, с чего начинался:
проектом, который к моменту выхода ролика был готов на 70 % и наполовину сдан.</p>
<button class="pp__ghost" type="button" data-seek="302" style="margin-top:18px">{PLAY}
Смотреть финал</button></div>
</div>
</div></section>'''


PAGE_JS = """<script>(function(){
 var v=document.getElementById('pp-video');
 // ── перемотка по любому [data-seek] ─────────────────────────────────────
 function seek(s){
  if(!v)return;
  var go=function(){try{v.currentTime=s;}catch(e){}var p=v.play();if(p&&p.catch)p.catch(function(){});};
  if(v.readyState>0)go();
  else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}
  var t=v.getBoundingClientRect().top+scrollY-90;
  if(Math.abs(scrollY-t)>240)scrollTo({top:t,behavior:'smooth'});
 }
 document.addEventListener('click',function(e){
  var b=e.target.closest?e.target.closest('[data-seek]'):null;
  if(!b)return;e.preventDefault();seek(parseFloat(b.getAttribute('data-seek')));});
 // ── подсветка текущей главы ─────────────────────────────────────────────
 var chaps=[].slice.call(document.querySelectorAll('.pp__chap')),last=0;
 if(v&&chaps.length){v.addEventListener('timeupdate',function(){
  var t=v.currentTime,cur=0;
  chaps.forEach(function(c,i){if(t>=parseFloat(c.getAttribute('data-chap')))cur=i;});
  if(cur===last)return;last=cur;
  chaps.forEach(function(c,i){c.setAttribute('aria-current',i===cur?'true':'false');});});}
 // ── шторка «архив → проект» ─────────────────────────────────────────────
 var ba=document.getElementById('pp-ba'),bax=document.getElementById('pp-ba-x');
 if(ba&&bax)bax.addEventListener('input',function(){ba.style.setProperty('--x',bax.value+'%');});
 // ── зоны охвата ─────────────────────────────────────────────────────────
 var Z=__ZONES__,zt=[].slice.call(document.querySelectorAll('.pp__ztab')),
     z1=document.getElementById('pp-z1'),z2=document.getElementById('pp-z2'),
     zv=document.getElementById('pp-zval'),zd=document.getElementById('pp-zdesc'),
     zs=document.getElementById('pp-zseek');
 function zone(i){
  var d=Z[i];
  zt.forEach(function(b,k){b.setAttribute('aria-selected',k===i?'true':'false');});
  if(z1)z1.classList.toggle('act',i===0);
  if(z2)z2.classList.toggle('act',i===1);
  zv.textContent=d.v;zd.textContent=d.d;zs.setAttribute('data-seek',d.s);
 }
 zt.forEach(function(b,i){b.addEventListener('click',function(){zone(i);});});
 if(zt.length)zone(0);
 // ── tenant mix ──────────────────────────────────────────────────────────
 var M=__MIX__,dn=document.getElementById('pp-donut'),
     dv=document.getElementById('pp-dv'),dnm=document.getElementById('pp-dn'),
     lg=document.getElementById('pp-legend');
 function mix(i){
  var segs=dn?[].slice.call(dn.querySelectorAll('.sg')):[],
      btns=lg?[].slice.call(lg.querySelectorAll('button')):[];
  segs.forEach(function(s,k){s.classList.toggle('on',k===i);});
  btns.forEach(function(b,k){b.classList.toggle('on',k===i);});
  if(dn)dn.classList.toggle('has',i>=0);
  if(i<0){dv.textContent='100 %';dnm.textContent='площадей распределены по восьми категориям';}
  else{dv.textContent=M[i].p+' %';dnm.textContent=M[i].n;}
 }
 if(dn){
  dn.addEventListener('mouseover',function(e){
   var s=e.target.closest?e.target.closest('.sg'):null;
   if(s)mix(+s.getAttribute('data-i'));});
  dn.addEventListener('mouseleave',function(){mix(-1);});
  dn.addEventListener('focusin',function(e){
   var s=e.target.closest?e.target.closest('.sg'):null;
   if(s)mix(+s.getAttribute('data-i'));});
 }
 if(lg){
  lg.addEventListener('mouseover',function(e){
   var b=e.target.closest?e.target.closest('button'):null;
   if(b)mix(+b.getAttribute('data-i'));});
  lg.addEventListener('mouseleave',function(){mix(-1);});
  lg.addEventListener('click',function(e){
   var b=e.target.closest?e.target.closest('button'):null;
   if(b)mix(+b.getAttribute('data-i'));});
 }
 // ── датчики готовности + появление блоков ───────────────────────────────
 function gauge(n){
  var b=n.querySelector?n.querySelector('.bar'):null;
  if(!b||b.dataset.done)return;b.dataset.done='1';
  var c=314,val=parseFloat(b.getAttribute('data-val'));
  requestAnimationFrame(function(){b.style.strokeDashoffset=(c*(1-val/100)).toFixed(1);});
 }
 var els=[].slice.call(document.querySelectorAll('.pp .r'));
 function inn(n){n.classList.add('is-in');
  [].slice.call(n.querySelectorAll('.pp__g')).forEach(gauge);}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(n);else io.observe(n);});
})();</script>"""


VIDEO_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"VideoObject","name":"Рекламный фильм ТРЦ «Павелецкая Плаза» (MMG)",'
            '"description":"Рекламный ролик торгово-развлекательного центра «Павелецкая Плаза» '
            'для арендаторов: локация и трафик Павелецкой площади, зоны охвата, интервью '
            'архитектора и основателей сетей-арендаторов, стадия готовности объекта.",'
            '"thumbnailUrl":"https://hand-marketing.ru' + IMG + '/poster.jpg",'
            '"contentUrl":"https://hand-marketing.ru' + VIDEO + '","duration":"PT5M37S",'
            '"uploadDate":"2020-11-01","publisher":{"@type":"Organization",'
            '"name":"Hand Marketing","logo":{"@type":"ImageObject",'
            '"url":"https://hand-marketing.ru/images/lib/as3365-6332-4339-a263-313566616365/152.png"}}}'
            '</script>')

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
                 '"@type":"BreadcrumbList","itemListElement":['
                 '{"@type":"ListItem","position":1,"name":"Проекты",'
                 '"item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"Video Production",'
                 '"item":"https://hand-marketing.ru/videoproduction/"},'
                 '{"@type":"ListItem","position":3,"name":"Рекламный фильм ТРЦ «Павелецкая Плаза»",'
                 f'"item":"{URL}"}}]}}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Рекламный фильм ТРЦ «Павелецкая Плаза» (MMG): кейс видеопродакшна | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: рекламный ролик ТРЦ «Павелецкая Плаза» для Mall Management Group. Фильм под задачи лизинга — локация и трафик Павелецкой площади, зоны охвата, tenant mix, интервью архитектора и основателей сетей-арендаторов, стадия готовности объекта.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Рекламный фильм ТРЦ «Павелецкая Плаза» | кейс Hand Marketing">
<meta property="og:description" content="Фильм для арендаторов ТРЦ «Павелецкая Плаза»: локация, трафик, аудитория и спрос вместо кадров стройки.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/poster.jpg">
<meta name="theme-color" content="#100C0E">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def build():
    zones = '[' + ','.join(
        '{{"r":{},"v":"{}","d":"{}","s":{}}}'.format(r, v, d, s)
        for _n, r, v, d, s in ZONES) + ']'
    mixjs = '[' + ','.join('{{"p":{},"n":"{}"}}'.format(p, n) for p, n in MIX) + ']'
    js = PAGE_JS.replace('__ZONES__', zones).replace('__MIX__', mixjs)
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма из rc.footer()
    body = (f'{rc.header()}<main class="pp">{hero()}{film()}{task()}{place()}{numbers()}'
            f'{zone()}{street()}{ready()}{mix()}{voices()}{trends()}{craft()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{VIDEO_LD}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'mmg')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(build())
    # A2-файла быть не должно: деплой переименует его поверх нашей страницы
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
