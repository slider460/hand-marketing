#!/usr/bin/env python3
"""Генерит mirror/bekobod1/index.html — кейс «Презентационный ролик технопарка «Бекабад»».

Что было: общий шаблон build-technopark.py (белый «industrial modernism»),
одинаковый для Бекабада и Зубова, плюс подключение шрифтов с внешнего CDN.
Страница пересказывала ролик текстом и ничего из него не показывала.

Дизайн-концепция: язык самого фильма. Ролик снят в тёмной зелёно-бирюзовой
палитре и целиком построен на гексагонах (знак BEKOBOD, соты в переходах,
кадры в шестиугольных рамках), поэтому и страница живёт в этой же сетке.

Главный ход — эпизод 1:16. Камера висит над реальной площадкой, и поверх
неподвижного кадра за пять секунд поднимается 3D-мастер-план: проезды,
кварталы, контуры, каркасы, кровли. Это и есть аргумент проекта «не идея на
бумаге», поэтому на странице он вынесен в ползунок: девять кадров ролика,
которые зритель прокручивает сам.

Дальше страница даёт то, за чем инвестор приходит:
  • главы фильма кликают плеер на нужную секунду (2:34 разложены на 10 эпизодов);
  • схема коридоров повторяет анимированную карту из ролика;
  • калькулятор считает срок нулевой ставки по объёму инвестиций, цифры взяты
    с инфографики фильма и материалов СЭЗ «Бекабад»;
  • тур по 3D-визуализации: шесть кадров, каждый перематывает плеер.

Своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма из
react-chrome. Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает
по маркеру <!--custom-page-->, index-a2.html удаляется (иначе деплой
переименует его поверх нашей страницы).

Кадры готовит scripts/bekabad-assets.py.
"""
import os
import importlib.util
import math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

URL = 'https://hand-marketing.ru/bekobod1/'
IMG = '/images/bekabad'
VIDEO = '/portfolio/bekobod/brand-video.mp4'
DUR = 155  # 2:34


# ─── главы фильма ───────────────────────────────────────────────────────────
# секунда, имя, подпись
CHAPTERS = [
    (0,   'Пролог',       'Знак и слоган'),
    (9,   'Узбекистан',   'Экономика Центральной Азии'),
    (24,  'Коридоры',     'Выход на пять рынков'),
    (39,  'Регион',       'Ташкентская область'),
    (51,  'Логистика',    '6 км, 133 км, КПП «Ойбек»'),
    (63,  'Партнёрство',  'Россия и Узбекистан'),
    (76,  'Мастер-план',  'Поле превращается в технопарк'),
    (83,  'Тур',          'Въезд, корпуса, склады'),
    (104, 'Льготы СЭЗ',   'Нулевые ставки и таможня'),
    (142, 'Финал',        'Энергия развития'),
]

# ─── морф «поле → технопарк», секунда каждого кадра ─────────────────────────
MORPH = [
    (76.0, 'Реальная площадка', 'Аэросъёмка. Сто гектаров подготовленной земли, техника на дальней границе участка.'),
    (76.9, 'Первый проезд',     'Из кадра проступает главная ось будущего технопарка.'),
    (77.6, 'Сетка дорог',       'Улицы режут территорию: транспортный каркас площадки готов раньше корпусов.'),
    (78.2, 'Кварталы',          'Шестьдесят восемь гектаров под застройку разложены на кварталы.'),
    (78.7, 'Контуры участков',  'Границы участков будущих резидентов подсвечиваются по одному.'),
    (79.2, 'Каркасы',           'Объёмы корпусов встают из земли голограммой.'),
    (79.8, 'Объёмы',            'Производства, склады и административный блок занимают свои места.'),
    (80.4, 'Материалы',         'Кровли, солнечные панели, озеленение и парковки.'),
    (81.0, 'Технопарк целиком', 'Ровно то, что получит резидент. Кадр, ради которого снимали площадку.'),
]

# ─── коридоры: подпись, угол в градусах, пояснение ──────────────────────────
CORRIDORS = [
    ('Россия',         106, 'Ключевой партнёр проекта: соглашение подписано с Башкортостаном'),
    ('Европа',         168, 'Транзит через Каспий и Кавказ'),
    ('Ближний Восток', 226, 'Юго-западное направление через Иран'),
    ('Южная Азия',     298, 'Афганистан, Пакистан, Индия'),
    ('Китай',           32, 'Восточное плечо через Ферганскую долину'),
]

# ─── страна в цифрах: кадр, число, подпись, секунда ─────────────────────────
COUNTRY = [
    ('sc-growth', '7%',   'Ежегодный рост экономики Узбекистана', 22),
    ('sc-growth', '18%',  'Ежегодный рост инвестиций', 22),
    ('sc-trade',  '13 млрд $', 'Товарооборот России и Узбекистана в 2025 году против 9 млрд в 2022-м', 66),
]

# ─── факты логистики: кадр, число, подпись, секунда ─────────────────────────
LOGISTICS = [
    ('sc-rail',   '6 км',   'До города Бекабада, ж/д пути и автодороги на площадке', 54),
    ('sc-air',    '133 км', 'До Ташкента и международного аэропорта', 29),
    ('sc-oybek',  'КПП «Ойбек»', 'Прямой выход в Таджикистан через пограничный пост', 57),
    ('sc-region', 'СЭЗ',    'Площадка внутри особой экономической зоны «Бекабад»', 45),
]

# ─── льготы: пороги инвестиций в млн $ и срок нулевой ставки в годах ────────
PROFIT = [(3, 5, 3, 'от 3 до 5 млн $'), (5, 15, 5, 'от 5 до 15 млн $'), (15, None, 10, 'свыше 15 млн $')]
PROPERTY = [(0.33, 3, 3, 'от 0,33 до 3 млн $'), (3, 5, 5, 'от 3 до 5 млн $'),
            (5, 10, 7, 'от 5 до 10 млн $'), (10, None, 10, 'свыше 10 млн $')]

CUSTOMS = [
    ('Оборудование', 'Ноль таможенных платежей при ввозе технологического оборудования по утверждённому перечню, если аналоги не производятся в Узбекистане'),
    ('Стройматериалы', 'Ноль платежей на стройматериалы для инвестиционного проекта, кроме НДС и сборов за оформление'),
    ('Отсрочка НДС', 'До 120 дней на уплату НДС при импорте товаров'),
    ('Возврат НДС', 'Возмещение в упрощённом порядке за 7 дней'),
]

# ─── инфографика льгот в кадре: кадр, секунда, подпись ─────────────────────
SEZ_SHOTS = [
    ('sc-support',  99, 'Сопровождение: регистрация компании и заявка в реестр участников СЭЗ'),
    ('sc-profit',  117, 'Ступени нулевого налога на прибыль прямо поверх 3D-квартала'),
    ('sc-prop',    128, 'Земельный и имущественный налог: четыре порога инвестиций'),
]

# ─── тур по 3D-визуализации: кадр, секунда, заголовок, подпись ──────────────
TOUR = [
    ('v-gate',   84.0,  'Въездная группа',      'Контрольно-пропускной пункт и стела BEKOBOD INDUSTRIAL TEXNOPARK'),
    ('v-admin',  108.0, 'Административный центр', 'Управляющая компания, сервисы для резидентов, конференц-зона'),
    ('v-street', 144.0, 'Улица технопарка',     'Проезды рассчитаны на фуры, между кварталами озеленение'),
    ('v-dock',   86.0,  'Погрузочные доки',     'Готовые складские корпуса с рампами под еврофуру'),
    ('v-lc',     123.0, 'Логистический центр',  'Bekobod Logistics Center: обработка и хранение грузов'),
    ('v-aerial', 150.0, 'Производственные корпуса', 'Кровли с солнечными панелями, парковки, внутренние дворы'),
]

# ─── что вошло в ролик ──────────────────────────────────────────────────────
CRAFT = [
    ('Аэросъёмка площадки', 'Реальные 100 гектаров с воздуха: без этого кадра 3D-модель осталась бы рендером'),
    ('3D-визуализация', 'Мастер-план, корпуса, склады, въездная группа и логистический центр'),
    ('Анимированные карты', 'Глобус, транспортные коридоры, Ташкентская область и граница с Таджикистаном'),
    ('Инфографика льгот', 'Ступени нулевых ставок по объёму инвестиций прямо в кадре'),
    ('Хроника переговоров', 'Форумы, подписания и визиты делегаций из архива проекта'),
    ('Гексагональная графика', 'Соты из фирменного знака работают как рамки кадров и переходы'),
]

PLAY = '<svg viewBox="0 0 12 14" aria-hidden="true"><path d="M0 0l12 7-12 7z"/></svg>'


def esc(t):
    import html
    return html.escape(t, quote=False)


def mmss(s):
    s = int(s)
    return '%d:%02d' % (s // 60, s % 60)


# ─── CSS ────────────────────────────────────────────────────────────────────
PAGE_CSS = """<style>
.bk{--bg:#04100D;--bg2:#071813;--panel:#0A211B;--panel2:#0D2A22;
 --line:rgba(110,235,180,.15);--line2:rgba(110,235,180,.3);
 --txt:#D7E7E0;--dim:#8AA69C;--faint:#5E7A71;
 --acc:#3FD98A;--acc2:#5FD2FF;--warm:#FFC96B;
 --ease:cubic-bezier(.16,1,.3,1);
 background:var(--bg);color:var(--txt);font-family:'Onest',system-ui,-apple-system,sans-serif;
 font-size:17px;line-height:1.62;-webkit-font-smoothing:antialiased;position:relative;overflow:clip}
.bk *{box-sizing:border-box}
.bk ::selection{background:var(--acc);color:#04100D}
.bk img{max-width:100%;height:auto;display:block}
.bk h1,.bk h2,.bk h3,.bk h4{font-family:'Geologica',system-ui,sans-serif;color:#fff;letter-spacing:-.02em}
.bk button{font-family:inherit}
.bk__w{max-width:1180px;margin:0 auto;padding:0 26px;position:relative;z-index:2}
.bk__s{padding:76px 0;position:relative;border-top:1px solid var(--line)}
.bk__s--flat{border-top:0}
/* соты фоном */
.bk__hex{position:absolute;inset:0;z-index:0;pointer-events:none;opacity:.5}
.bk__glow{position:absolute;z-index:0;pointer-events:none;border-radius:50%;filter:blur(90px)}
/* лейблы секций */
.bk__lab{display:flex;align-items:center;gap:11px;margin:0 0 20px;
 font-size:12.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--acc)}
.bk__lab i{width:11px;height:12px;background:var(--acc);flex:none;
 clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
.bk__lab s{text-decoration:none;color:var(--faint);letter-spacing:.08em}
.bk__h2{font-size:clamp(27px,5.4vw,44px);font-weight:700;line-height:1.06;margin:0 0 18px;max-width:19ch}
.bk__h2--wide{max-width:26ch}
.bk__intro{max-width:62ch;color:var(--dim);margin:0 0 34px;font-size:clamp(15.5px,3.6vw,17.5px)}
.bk__intro b{color:var(--txt);font-weight:500}
/* ── ГЕРОЙ ───────────────────────────────────────────────────────────── */
.bk__hero{padding:44px 0 6px}
.bk__kick{display:flex;flex-wrap:wrap;align-items:center;gap:9px 16px;margin:0 0 24px;
 font-size:12.5px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--acc)}
.bk__kick span{color:var(--faint)}
.bk__kick i{width:12px;height:13px;background:var(--acc);flex:none;
 clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
.bk__t{font-size:clamp(42px,11.4vw,104px);font-weight:800;line-height:.94;margin:0 0 20px;letter-spacing:-.035em}
.bk__t em{font-style:normal;color:var(--acc);
 text-shadow:0 0 44px rgba(63,217,138,.35)}
.bk__lead{max-width:60ch;font-size:clamp(16px,4vw,20px);color:#B9CFC7;margin:0 0 36px}
.bk__spec{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);
 border:1px solid var(--line);margin:0 0 40px}
@media(min-width:760px){.bk__spec{grid-template-columns:repeat(4,1fr)}}
.bk__spec div{background:var(--bg2);padding:17px 18px}
.bk__spec b{display:block;font-family:'Geologica',sans-serif;font-weight:700;font-size:26px;color:#fff;
 line-height:1;font-variant-numeric:tabular-nums}
.bk__spec i{display:block;font-style:normal;margin-top:7px;font-size:12.5px;letter-spacing:.05em;
 text-transform:uppercase;color:var(--faint)}
/* ── ПЛЕЕР ───────────────────────────────────────────────────────────── */
.bk__stage{position:relative;border:1px solid var(--line2);background:#000;overflow:hidden}
.bk__stage video{width:100%;aspect-ratio:16/9;display:block;background:#000}
.bk__pb{position:absolute;inset:0;width:100%;padding:0;border:0;cursor:pointer;background:center/cover no-repeat;
 display:grid;place-items:center;transition:opacity .45s var(--ease)}
.bk__pb::after{content:"";position:absolute;inset:0;
 background:radial-gradient(60% 60% at 50% 50%,rgba(4,16,13,.15),rgba(4,16,13,.6))}
.bk__play{position:relative;z-index:1;width:96px;height:106px;display:grid;place-items:center;
 background:rgba(63,217,138,.92);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%);
 transition:transform .35s var(--ease),background .35s}
.bk__play svg{width:26px;height:30px;fill:#04100D;margin-left:5px}
.bk__pb:hover .bk__play{transform:scale(1.07);background:#5FF0A4}
.bk__corner{position:absolute;width:15px;height:15px;z-index:1;border-color:var(--acc);opacity:.9}
.bk__corner.tl{top:10px;left:10px;border-top:2px solid;border-left:2px solid}
.bk__corner.tr{top:10px;right:10px;border-top:2px solid;border-right:2px solid}
.bk__corner.bl{bottom:10px;left:10px;border-bottom:2px solid;border-left:2px solid}
.bk__corner.br{bottom:10px;right:10px;border-bottom:2px solid;border-right:2px solid}
/* ── ГЛАВЫ ───────────────────────────────────────────────────────────── */
.bk__chaps{display:flex;gap:1px;background:var(--line);border:1px solid var(--line);
 overflow-x:auto;scrollbar-width:thin;margin-top:1px}
@media(min-width:820px){.bk__chaps{display:grid;grid-template-columns:repeat(5,1fr);overflow:visible}}
.bk__chap{flex:1 0 152px;background:var(--bg2);border:0;padding:15px 15px 17px;text-align:left;cursor:pointer;
 color:var(--dim);transition:background .3s,color .3s;position:relative}
.bk__chap:hover{background:var(--panel2);color:var(--txt)}
.bk__chap[aria-current=true]{background:var(--panel2);color:#fff}
.bk__chap[aria-current=true]::before{content:"";position:absolute;left:0;right:0;top:0;height:2px;background:var(--acc)}
.bk__chap u{display:block;text-decoration:none;font-size:12px;font-weight:600;letter-spacing:.08em;
 color:var(--acc);font-variant-numeric:tabular-nums}
.bk__chap b{display:block;font-family:'Geologica',sans-serif;font-weight:600;font-size:15.5px;color:inherit;margin:6px 0 3px}
.bk__chap i{font-style:normal;font-size:12.5px;line-height:1.4;color:var(--faint);display:block}
/* ── МОРФ ────────────────────────────────────────────────────────────── */
.bk__morph{position:relative;border:1px solid var(--line2);background:#04100D;overflow:hidden}
.bk__mstack{position:relative;aspect-ratio:1200/470}
.bk__mstack img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;
 transition:opacity .16s linear}
.bk__mstack img.on{opacity:1}
.bk__mtag{position:absolute;left:0;bottom:0;right:0;z-index:2;padding:44px 22px 18px;
 background:linear-gradient(180deg,transparent,rgba(4,16,13,.9) 55%)}
.bk__mtag b{font-family:'Geologica',sans-serif;font-size:clamp(17px,4.4vw,24px);font-weight:700;color:#fff;display:block}
.bk__mtag i{font-style:normal;color:#9FBDB2;font-size:14px;display:block;margin-top:4px;max-width:64ch}
.bk__mtime{position:absolute;right:14px;top:14px;z-index:2;background:rgba(4,16,13,.82);
 border:1px solid var(--line2);color:var(--acc);font-family:'Geologica',sans-serif;font-size:12px;
 font-weight:600;letter-spacing:.1em;padding:6px 10px;font-variant-numeric:tabular-nums}
.bk__mctl{display:flex;align-items:center;gap:18px;padding:20px 22px;background:var(--bg2);
 border-top:1px solid var(--line);flex-wrap:wrap}
.bk__range{flex:1 1 240px;-webkit-appearance:none;appearance:none;background:transparent;height:26px;cursor:pointer}
.bk__range::-webkit-slider-runnable-track{height:4px;background:linear-gradient(90deg,var(--acc),var(--acc2));border-radius:2px}
.bk__range::-moz-range-track{height:4px;background:linear-gradient(90deg,var(--acc),var(--acc2));border-radius:2px}
.bk__range::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:28px;margin-top:-12px;background:#fff;
 clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%);cursor:grab}
.bk__range::-moz-range-thumb{width:26px;height:28px;border:0;background:#fff;
 clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%);cursor:grab}
.bk__range:focus-visible{outline:2px solid var(--acc2);outline-offset:6px}
.bk__ticks{display:flex;justify-content:space-between;font-size:11.5px;letter-spacing:.08em;
 text-transform:uppercase;color:var(--faint);padding:0 22px 18px;background:var(--bg2)}
.bk__btn{display:inline-flex;align-items:center;gap:10px;border:1px solid var(--line2);background:transparent;
 color:var(--txt);padding:11px 20px;font-size:14px;font-weight:600;cursor:pointer;transition:.3s var(--ease)}
.bk__btn svg{width:11px;height:13px;fill:var(--acc)}
.bk__btn:hover{background:var(--acc);color:#04100D;border-color:var(--acc)}
.bk__btn:hover svg{fill:#04100D}
/* ── СХЕМА КОРИДОРОВ ─────────────────────────────────────────────────── */
.bk__geo{display:grid;gap:34px}
@media(min-width:940px){.bk__geo{grid-template-columns:1.05fr .95fr;gap:56px;align-items:center}}
.bk__map{width:100%;height:auto;overflow:visible}
.bk__ray{cursor:default}
.bk__ray line{stroke:var(--line2);stroke-width:1.4;stroke-dasharray:5 7;
 animation:bkdash 2.4s linear infinite}
.bk__ray line.hit{stroke:transparent;stroke-width:34;stroke-dasharray:none;animation:none}
.bk__ray:focus-visible{outline:none}
.bk__ray:focus-visible line:not(.hit){stroke:var(--acc2);stroke-dasharray:none}
.bk__ray:focus-visible polygon{fill:var(--acc2);stroke:var(--acc2)}
.bk__ray:focus-visible text{fill:#fff}
@keyframes bkdash{to{stroke-dashoffset:-24}}
.bk__ray polygon{fill:var(--bg2);stroke:var(--line2);stroke-width:1.4;transition:.3s}
.bk__ray text{fill:var(--dim);font-family:'Geologica',sans-serif;font-size:14px;font-weight:600;transition:.3s}
.bk__ray:hover line:not(.hit){stroke:var(--acc2);stroke-dasharray:none}
.bk__ray:hover polygon{fill:var(--acc2);stroke:var(--acc2)}
.bk__ray:hover text{fill:#fff}
.bk__ray desc{display:none}
.bk__grid-hex{fill:none;stroke:var(--line);stroke-width:1}
.bk__core{fill:rgba(63,217,138,.12);stroke:var(--acc);stroke-width:1.6}
.bk__core-t{fill:#fff;font-family:'Geologica',sans-serif;font-weight:700;font-size:17px;letter-spacing:.04em}
.bk__core-s{fill:var(--acc);font-family:'Onest',sans-serif;font-size:11.5px;letter-spacing:.12em}
.bk__facts{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
.bk__fact{background:var(--bg2);padding:19px 20px;display:grid;grid-template-columns:1fr auto;
 gap:14px;align-items:center;cursor:pointer;border:0;text-align:left;color:inherit;transition:background .3s}
.bk__fact:hover{background:var(--panel2)}
.bk__fact b{display:block;font-family:'Geologica',sans-serif;font-weight:700;font-size:23px;color:#fff;line-height:1.1}
.bk__fact i{font-style:normal;font-size:13.5px;color:var(--dim);display:block;margin-top:5px}
.bk__fact img{width:124px;height:70px;object-fit:cover;border:1px solid var(--line)}
/* ── ЦИФРЫ СТРАНЫ ────────────────────────────────────────────────────── */
.bk__nums{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);margin-top:36px}
@media(min-width:760px){.bk__nums{grid-template-columns:repeat(3,1fr)}}
.bk__num{background:var(--bg2);padding:26px 22px;border:0;text-align:left;color:inherit;cursor:pointer;
 transition:background .3s}
.bk__num:hover{background:var(--panel2)}
.bk__num b{display:block;font-family:'Geologica',sans-serif;font-weight:800;font-size:clamp(34px,8vw,52px);
 line-height:.95;color:var(--acc);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.bk__num i{font-style:normal;display:block;margin-top:12px;font-size:14.5px;color:var(--dim)}
/* ── КАЛЬКУЛЯТОР ─────────────────────────────────────────────────────── */
.bk__calc{border:1px solid var(--line2);background:var(--bg2)}
.bk__calc-top{padding:28px 26px 24px;border-bottom:1px solid var(--line)}
.bk__calc-val{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:6px}
.bk__calc-val b{font-family:'Geologica',sans-serif;font-weight:800;font-size:clamp(38px,9vw,60px);color:#fff;
 line-height:1;font-variant-numeric:tabular-nums;letter-spacing:-.03em}
.bk__calc-val span{font-size:15px;color:var(--dim)}
.bk__calc-top .bk__range{width:100%;display:block}
.bk__calc-lab{font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 20px}
.bk__out{display:grid;gap:1px;background:var(--line)}
@media(min-width:800px){.bk__out{grid-template-columns:1fr 1fr}}
.bk__oc{background:var(--panel);padding:24px 26px}
.bk__oc>u{display:block;text-decoration:none;font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--faint);margin-bottom:14px}
.bk__oy{font-family:'Geologica',sans-serif;font-weight:800;font-size:clamp(30px,7vw,44px);color:var(--acc);
 line-height:1;font-variant-numeric:tabular-nums}
.bk__oy.none{color:var(--faint);font-size:clamp(19px,4.6vw,26px)}
.bk__steps{margin:18px 0 0;padding:0;list-style:none;display:grid;gap:0}
.bk__steps li{display:flex;justify-content:space-between;gap:14px;padding:9px 0;border-top:1px solid var(--line);
 font-size:14px;color:var(--faint);transition:color .3s}
.bk__steps li span{font-variant-numeric:tabular-nums}
.bk__steps li.on{color:#fff}
.bk__steps li.on span{color:var(--acc)}
.bk__cust{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);border-top:0}
@media(min-width:720px){.bk__cust{grid-template-columns:repeat(2,1fr)}}
.bk__cust div{background:var(--bg2);padding:20px 22px}
.bk__cust b{display:block;font-family:'Geologica',sans-serif;font-weight:600;font-size:15.5px;color:#fff;margin-bottom:6px}
.bk__cust p{margin:0;font-size:13.5px;color:var(--dim);line-height:1.55}
.bk__note{margin:16px 0 0;font-size:12.5px;color:var(--faint);max-width:76ch}
/* ── полоса кадров инфографики ───────────────────────────────────────── */
.bk__strip{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);border-top:0}
@media(min-width:760px){.bk__strip{grid-template-columns:repeat(3,1fr)}}
.bk__sh{background:var(--bg2);border:0;padding:0;cursor:pointer;text-align:left;color:inherit;
 display:block;width:100%;transition:background .3s}
.bk__sh:hover{background:var(--panel2)}
.bk__sh figure{margin:0;position:relative}
.bk__sh img{width:100%;aspect-ratio:16/9;object-fit:cover;opacity:.86;transition:opacity .3s}
.bk__sh:hover img{opacity:1}
.bk__sh figcaption{position:absolute;left:10px;top:10px;background:rgba(4,16,13,.82);color:var(--acc);
 font-size:11px;font-weight:600;letter-spacing:.08em;padding:4px 8px;font-variant-numeric:tabular-nums}
.bk__sh p{margin:0;padding:14px 18px 18px;font-size:13.5px;color:var(--dim);line-height:1.5}
/* ── ТУР ─────────────────────────────────────────────────────────────── */
.bk__tour{display:grid;gap:22px}
@media(min-width:700px){.bk__tour{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1040px){.bk__tour{grid-template-columns:repeat(3,1fr)}}
.bk__tc{border:1px solid var(--line);background:var(--bg2);padding:0;text-align:left;color:inherit;cursor:pointer;
 transition:border-color .35s,transform .35s var(--ease);display:block;width:100%}
.bk__tc:hover{border-color:var(--acc);transform:translateY(-4px)}
.bk__tc figure{margin:0;position:relative;overflow:hidden}
.bk__tc img{width:100%;aspect-ratio:16/9;object-fit:cover;transition:transform .6s var(--ease)}
.bk__tc:hover img{transform:scale(1.05)}
.bk__tc figcaption{position:absolute;left:12px;top:12px;background:rgba(4,16,13,.82);color:var(--acc);
 font-size:11.5px;font-weight:600;letter-spacing:.08em;padding:5px 9px;font-variant-numeric:tabular-nums}
.bk__tc div{padding:17px 19px 20px}
.bk__tc b{display:block;font-family:'Geologica',sans-serif;font-weight:600;font-size:17.5px;color:#fff;margin-bottom:6px}
.bk__tc p{margin:0;font-size:14px;color:var(--dim);line-height:1.5}
/* ── ЭТАПЫ ───────────────────────────────────────────────────────────── */
.bk__steps-w{display:grid;gap:0}
.bk__step{display:grid;grid-template-columns:auto 1fr;gap:30px;padding:34px 0;border-top:1px solid var(--line)}
@media(max-width:660px){.bk__step{grid-template-columns:1fr;gap:12px}}
.bk__step>u{text-decoration:none;font-family:'Geologica',sans-serif;font-weight:700;font-size:13px;
 letter-spacing:.1em;color:var(--acc);padding-top:9px;white-space:nowrap}
.bk__step h3{font-size:clamp(21px,5vw,29px);font-weight:700;margin:0 0 13px;line-height:1.12}
.bk__step p{margin:0 0 12px;color:var(--dim);max-width:66ch}
.bk__step p b{color:var(--txt);font-weight:500}
.bk__craft{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);margin-top:14px}
@media(min-width:720px){.bk__craft{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1040px){.bk__craft{grid-template-columns:repeat(3,1fr)}}
.bk__craft div{background:var(--bg2);padding:20px 22px}
.bk__craft b{display:block;font-family:'Geologica',sans-serif;font-weight:600;font-size:16px;color:#fff;margin-bottom:7px}
.bk__craft p{margin:0;font-size:13.5px;color:var(--dim);line-height:1.55}
/* ── ФИНАЛ ───────────────────────────────────────────────────────────── */
.bk__fin{position:relative;border:1px solid var(--line2);overflow:hidden}
.bk__fin img{width:100%;aspect-ratio:16/7;object-fit:cover;opacity:.5}
.bk__fin-in{position:absolute;inset:0;display:grid;align-content:center;justify-items:start;
 padding:clamp(20px,5vw,54px);background:linear-gradient(90deg,rgba(4,16,13,.92),rgba(4,16,13,.35))}
.bk__fin b{font-family:'Geologica',sans-serif;font-weight:800;font-size:clamp(21px,5.4vw,42px);color:#fff;
 line-height:1.05;letter-spacing:-.02em;max-width:16ch}
.bk__fin i{font-style:normal;color:var(--acc);font-size:clamp(12px,3vw,16px);letter-spacing:.12em;
 text-transform:uppercase;margin:12px 0 clamp(14px,3vw,26px);display:block}
/* ── появление ───────────────────────────────────────────────────────── */
.bk .r{opacity:0;transform:translateY(26px);transition:opacity .85s var(--ease),transform .85s var(--ease)}
.bk .r.is-in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
 .bk .r{opacity:1;transform:none;transition:none}
 .bk__ray line{animation:none}}
@media(max-width:640px){
 .bk__s{padding:52px 0}
 .bk__w{padding:0 16px}
 .bk__fact{grid-template-columns:1fr}
 .bk__fact img{width:100%;height:auto;aspect-ratio:16/9}
 .bk__mtag{position:static;background:var(--bg2);border-top:1px solid var(--line);padding:14px 16px 16px}
 .bk__mtag i{font-size:13.5px}
 .bk__mctl,.bk__ticks{padding-left:16px;padding-right:16px}
 .bk__play{width:74px;height:82px}
}
</style>"""


# ─── фоновые соты ───────────────────────────────────────────────────────────
def hexbg(idp):
    """SVG-паттерн из сот на фон секции."""
    return (f'<svg class="bk__hex" aria-hidden="true"><defs>'
            f'<pattern id="{idp}" width="56" height="97" patternUnits="userSpaceOnUse" '
            f'patternTransform="scale(1.15)">'
            f'<path d="M28 0 56 16v32L28 64 0 48V16z" fill="none" stroke="rgba(63,217,138,.09)" stroke-width="1"/>'
            f'<path d="M0 48v32M56 48v32M28 64v33" stroke="rgba(63,217,138,.05)" stroke-width="1"/>'
            f'</pattern></defs><rect width="100%" height="100%" fill="url(#{idp})"/></svg>')


def hexpts(cx, cy, r, rot=0.0):
    pts = []
    for i in range(6):
        a = math.radians(60 * i + rot)
        pts.append('%.1f,%.1f' % (cx + r * math.cos(a), cy - r * math.sin(a)))
    return ' '.join(pts)


# ─── секции ─────────────────────────────────────────────────────────────────
def hero():
    spec = ''.join(f'<div><b>{b}</b><i>{esc(i)}</i></div>' for b, i in [
        ('100 га', 'Общая площадь'), ('68 га', 'Площадь застройки'),
        ('6 км', 'До Бекабада'), ('133 км', 'До Ташкента')])
    return f'''<section class="bk__s bk__s--flat bk__hero">
{hexbg('bkhx1')}
<div class="bk__glow" style="width:640px;height:640px;background:rgba(63,217,138,.13);top:-260px;right:-160px"></div>
<div class="bk__glow" style="width:520px;height:520px;background:rgba(95,210,255,.09);top:280px;left:-240px"></div>
<div class="bk__w">
<p class="bk__kick"><i></i>Презентационный ролик · 2:34 <span>Бекабадский район · Ташкентская обл.</span></p>
<h1 class="bk__t">Технопарк <em>Бекабад</em></h1>
<p class="bk__lead">Промышленная площадка в Ташкентской области, которую Республика Башкортостан
строит вместе с Узбекистаном. Ролик должен был доказать инвестору главное: это не намерение,
а нарезанные кварталы, инженерия и понятные условия входа.</p>
<div class="bk__spec">{spec}</div>
<div class="bk__stage r">
 <video id="bk-film" playsinline preload="none" controls poster="{IMG}/poster.jpg"
  aria-label="Презентационный ролик технопарка «Бекабад»"><source src="{VIDEO}" type="video/mp4"></video>
 <button class="bk__pb" id="bk-pb" style="background-image:url('{IMG}/poster.jpg')"
  aria-label="Смотреть ролик"><span class="bk__play">{PLAY}</span></button>
 <i class="bk__corner tl"></i><i class="bk__corner tr"></i><i class="bk__corner bl"></i><i class="bk__corner br"></i>
</div>
{chapters()}
</div></section>'''


def chapters():
    ch = ''.join(
        f'<button class="bk__chap" type="button" data-seek="{s}" data-chap="{s}">'
        f'<u>{mmss(s)}</u><b>{esc(n)}</b><i>{esc(d)}</i></button>'
        for s, n, d in CHAPTERS)
    return f'<div class="bk__chaps r" role="group" aria-label="Главы ролика">{ch}</div>'


def morph():
    imgs = ''.join(
        f'<img src="{IMG}/morph-{i + 1}.jpg" width="1200" height="470"'
        f'{" " if i == 0 else " loading=lazy "}alt="Кадр ролика {mmss(s)}: {esc(t.lower())}"'
        f' class="{"on" if i == 0 else ""}">'
        for i, (s, t, d) in enumerate(MORPH))
    return f'''<section class="bk__s">
{hexbg('bkhx2')}
<div class="bk__w">
<p class="bk__lab"><i></i>Эпизод 1:16 <s>ключевой кадр</s></p>
<h2 class="bk__h2 bk__h2--wide">Поле превращается в технопарк за пять секунд</h2>
<p class="bk__intro">Камера висит над реальной площадкой и не двигается. За пять секунд поверх
съёмки поднимается мастер-план: проезды, кварталы, контуры участков, каркасы, кровли.
<b>Инвестор видит одновременно и землю, которая уже есть, и завод, который на ней будет.</b>
Ползунок ниже проходит эти секунды кадр за кадром.</p>
<div class="bk__morph r">
 <div class="bk__mstack" id="bk-mstack">{imgs}
  <div class="bk__mtime" id="bk-mtime">1:16</div>
  <div class="bk__mtag"><b id="bk-mtitle">{esc(MORPH[0][1])}</b>
   <i id="bk-mdesc">{esc(MORPH[0][2])}</i></div>
 </div>
 <div class="bk__mctl">
  <input class="bk__range" id="bk-mrange" type="range" min="0" max="{len(MORPH) - 1}" value="0" step="1"
   aria-label="Стадия застройки" aria-valuetext="{esc(MORPH[0][1])}">
  <button class="bk__btn" type="button" id="bk-mplay">{PLAY}Прокрутить</button>
  <button class="bk__btn" type="button" data-seek="76">{PLAY}Смотреть в ролике</button>
 </div>
 <div class="bk__ticks"><span>Поле</span><span>Дороги</span><span>Каркасы</span><span>Технопарк</span></div>
</div>
</div></section>'''


def geo():
    cx, cy, r = 300, 300, 300
    rays = ''
    for name, ang, note in CORRIDORS:
        a = math.radians(ang)
        x1, y1 = cx + 78 * math.cos(a), cy - 78 * math.sin(a)
        x2, y2 = cx + 212 * math.cos(a), cy - 212 * math.sin(a)
        tx, ty = cx + 236 * math.cos(a), cy - 236 * math.sin(a)
        anchor = 'middle'
        if tx < cx - 40:
            anchor = 'end'
        elif tx > cx + 40:
            anchor = 'start'
        rays += (f'<g class="bk__ray" tabindex="0" role="img" aria-label="{esc(name)}: {esc(note)}">'
                 f'<title>{esc(name)}. {esc(note)}</title>'
                 f'<line class="hit" x1="{x1:.1f}" y1="{y1:.1f}" x2="{tx:.1f}" y2="{ty:.1f}"/>'
                 f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'
                 f'<polygon points="{hexpts(x2, y2, 11, 30)}"/>'
                 f'<text x="{tx:.1f}" y="{ty + 5:.1f}" text-anchor="{anchor}">{esc(name)}</text></g>')
    rings = ''.join(f'<polygon class="bk__grid-hex" points="{hexpts(cx, cy, rr, 30)}"/>'
                    for rr in (120, 168, 212))
    facts = ''.join(
        f'<button class="bk__fact" type="button" data-seek="{s}">'
        f'<span><b>{esc(v)}</b><i>{esc(t)}</i></span>'
        f'<img src="{IMG}/{n}.jpg" width="124" height="70" loading="lazy" alt="Кадр ролика: {esc(t.lower())}">'
        f'</button>' for n, v, t, s in LOGISTICS)
    nums = ''.join(f'<button class="bk__num" type="button" data-seek="{sec}">'
                   f'<b>{esc(v)}</b><i>{esc(t)}</i></button>'
                   for _, v, t, sec in COUNTRY)
    return f'''<section class="bk__s">
<div class="bk__glow" style="width:560px;height:560px;background:rgba(95,210,255,.08);top:120px;right:-220px"></div>
<div class="bk__w">
<p class="bk__lab"><i></i>Эпизоды 0:24 и 0:51 <s>география</s></p>
<h2 class="bk__h2 bk__h2--wide">Точка входа на рынки Центральной Азии</h2>
<p class="bk__intro">Первая треть ролика отвечает на вопрос «почему здесь». Узбекистан показан как
перекрёсток пяти направлений, а Бекабад как площадка у самой границы с Таджикистаном.
Наведите на луч, чтобы увидеть направление; карточки справа перематывают плеер на нужный эпизод.</p>
<div class="bk__geo r">
<div><svg class="bk__map" viewBox="0 0 600 600" role="group" aria-label="Схема транспортных направлений">
{rings}
{rays}
<polygon class="bk__core" points="{hexpts(cx, cy, 76, 30)}"/>
<text class="bk__core-t" x="{cx}" y="{cy - 2}" text-anchor="middle">БЕКАБАД</text>
<text class="bk__core-s" x="{cx}" y="{cy + 20}" text-anchor="middle">UZ · СЭЗ</text>
</svg></div>
<div class="bk__facts">{facts}</div>
</div>
<div class="bk__nums r">{nums}</div>
</div></section>'''


def calc():
    def steps(rows, cid):
        li = ''.join(f'<li data-min="{a}" data-max="{b if b is not None else 999}">'
                     f'{esc(lab)}<span>{y} {"год" if y == 1 else ("года" if y < 5 else "лет")}</span></li>'
                     for a, b, y, lab in rows)
        return f'<ul class="bk__steps" id="{cid}">{li}</ul>'
    cust = ''.join(f'<div><b>{esc(t)}</b><p>{esc(d)}</p></div>' for t, d in CUSTOMS)
    strip = ''.join(
        f'<button class="bk__sh" type="button" data-seek="{sec}">'
        f'<figure><img src="{IMG}/{n}.jpg" width="900" height="506" loading="lazy"'
        f' alt="Кадр ролика: {esc(cap.lower())}"><figcaption>{mmss(sec)}</figcaption></figure>'
        f'<p>{esc(cap)}</p></button>' for n, sec, cap in SEZ_SHOTS)
    return f'''<section class="bk__s">
{hexbg('bkhx3')}
<div class="bk__w">
<p class="bk__lab"><i></i>Эпизод 1:44 <s>условия резидента</s></p>
<h2 class="bk__h2 bk__h2--wide">Сколько лет резидент платит ноль</h2>
<p class="bk__intro">В ролике льготы СЭЗ показаны ступенями: чем больше инвестиции, тем дольше
нулевая ставка. Мы перенесли эту инфографику на страницу живой: <b>двиньте ползунок и увидите
срок для своего объёма вложений.</b></p>
<div class="bk__calc r">
 <div class="bk__calc-top">
  <p class="bk__calc-lab">Объём инвестиций резидента</p>
  <div class="bk__calc-val"><b id="bk-cv">5,0</b><span>млн долларов</span></div>
  <input class="bk__range" id="bk-crange" type="range" min="0.33" max="20" step="0.01" value="5"
   aria-label="Объём инвестиций, млн долларов">
  <div class="bk__ticks" style="padding:6px 0 0;background:transparent">
   <span>0,33</span><span>5</span><span>10</span><span>15</span><span>20+</span></div>
 </div>
 <div class="bk__out">
  <div class="bk__oc"><u>Налог на прибыль</u><div class="bk__oy" id="bk-o1">5 лет</div>
   {steps(PROFIT, 'bk-s1')}</div>
  <div class="bk__oc"><u>Земельный, имущественный, водный</u><div class="bk__oy" id="bk-o2">7 лет</div>
   {steps(PROPERTY, 'bk-s2')}</div>
 </div>
</div>
<div class="bk__cust r">{cust}</div>
<div class="bk__strip r">{strip}</div>
<p class="bk__note">Ставки и пороги взяты с инфографики ролика и открытых материалов СЭЗ «Бекабад».
Это иллюстрация кейса, а не юридическая консультация: актуальные условия резидентства
подтверждает управляющая компания технопарка.</p>
</div></section>'''


def tour():
    cards = ''.join(
        f'<button class="bk__tc r" type="button" data-seek="{int(s)}">'
        f'<figure><img src="{IMG}/{n}.jpg" width="900" height="506" loading="lazy"'
        f' alt="Кадр ролика: {esc(t.lower())}"><figcaption>{mmss(s)}</figcaption></figure>'
        f'<div><b>{esc(t)}</b><p>{esc(d)}</p></div></button>'
        for n, s, t, d in TOUR)
    return f'''<section class="bk__s">
<div class="bk__w">
<p class="bk__lab"><i></i>Эпизоды 1:23 и 2:24 <s>3D-визуализация</s></p>
<h2 class="bk__h2 bk__h2--wide">Экскурсия по технопарку, которого ещё нет</h2>
<p class="bk__intro">Вторая половина ролика сделана как проезд по будущей площадке: от въездной
группы до погрузочных доков. Резидент понимает, что именно он арендует, ещё до первого визита.
Клик по кадру перематывает плеер на этот эпизод.</p>
<div class="bk__tour">{cards}</div>
</div></section>'''


def story():
    craft = ''.join(f'<div><b>{esc(t)}</b><p>{esc(d)}</p></div>' for t, d in CRAFT)
    return f'''<section class="bk__s">
{hexbg('bkhx4')}
<div class="bk__w">
<p class="bk__lab"><i></i>Работа <s>как мы это сделали</s></p>
<div class="bk__steps-w">
<div class="bk__step r"><u>01 / ЗАДАЧА</u><div>
<h3>Доказать, что площадка существует</h3>
<p>Технопарк создаётся с нуля, и у переговорной команды не было ничего, кроме проектной
документации и слов. Инвестору из другой страны этого мало: он не поедет смотреть поле
в Ташкентской области, пока не поймёт масштаб, инженерию и условия входа.</p>
<p>Ролик должен был за две с половиной минуты снять четыре возражения: <b>где это находится,
что там будет построено, кто за этим стоит и сколько стоит вход.</b></p>
</div></div>
<div class="bk__step r"><u>02 / РЕШЕНИЕ</u><div>
<h3>Маршрут от страны до участка резидента</h3>
<p>Собрали фильм как воронку. Сначала страна и её транспортные коридоры, потом Ташкентская
область и километры до Бекабада и Ташкента, затем сама площадка, и только в конце условия СЭЗ.
Каждый следующий эпизод сужает масштаб, зритель не теряет нить.</p>
<p>Опорная сцена одна: реальная аэросъёмка, поверх которой вырастает 3D-мастер-план.
Она склеивает две части фильма и снимает главное сомнение про идею на бумаге.</p>
</div></div>
<div class="bk__step r"><u>03 / РЕЗУЛЬТАТ</u><div>
<h3>Инструмент переговоров, а не имиджевый ролик</h3>
<p>Ролик работает на встречах с инвесторами, делегациями и потенциальными резидентами,
на форумах и в цифровых каналах технопарка. Он заменяет получасовую презентацию и
не требует проектной документации.</p>
<p>Для международного инвестора это ещё и сигнал управляемости: у проекта есть мастер-план,
партнёрское соглашение между Башкортостаном и Ташкентской областью и понятная механика льгот.</p>
</div></div>
</div>
<div class="bk__craft r">{craft}</div>
</div></section>'''


def final():
    return f'''<section class="bk__s">
<div class="bk__w"><div class="bk__fin r">
<img src="{IMG}/sc-final.jpg" width="900" height="506" loading="lazy"
 alt="Финальный кадр ролика: флаги России, Узбекистана и Башкортостана">
<div class="bk__fin-in">
<b>Энергия развития. Пространство возможностей</b>
<i>Финал ролика · 2:32</i>
<button class="bk__btn" type="button" data-seek="142">{PLAY}Посмотреть финал</button>
</div></div></div></section>'''


# ─── JS ─────────────────────────────────────────────────────────────────────
MORPH_JSON = '[' + ','.join(
    '{"s":%s,"t":"%s","d":"%s"}' % (s, t.replace('"', '\\"'), d.replace('"', '\\"'))
    for s, t, d in MORPH) + ']'

PAGE_JS = """<script>(function(){
 var M=""" + MORPH_JSON + """;
 var v=document.getElementById('bk-film'),pb=document.getElementById('bk-pb');
 // ── плеер: фасад с постером ─────────────────────────────────────────────
 if(v&&pb){pb.addEventListener('click',function(){pb.style.opacity=0;pb.style.pointerEvents='none';
  v.play().catch(function(){});});
  v.addEventListener('pause',function(){if(v.currentTime===0){pb.style.opacity='';pb.style.pointerEvents='';}});}
 // ── любая кнопка с data-seek перематывает один плеер ────────────────────
 function seek(sec){
  if(!v)return;
  if(pb){pb.style.opacity=0;pb.style.pointerEvents='none';}
  var go=function(){try{v.currentTime=sec;}catch(e){}v.play().catch(function(){});};
  if(v.readyState<1){v.addEventListener('loadedmetadata',go,{once:true});v.load();}else{go();}
  var r=v.getBoundingClientRect();
  if(r.top<0||r.bottom>innerHeight)v.scrollIntoView({behavior:'smooth',block:'center'});
 }
 document.addEventListener('click',function(e){
  var b=e.target.closest?e.target.closest('[data-seek]'):null;
  if(!b)return;e.preventDefault();seek(parseFloat(b.getAttribute('data-seek')));});
 // ── подсветка активной главы ────────────────────────────────────────────
 var chaps=[].slice.call(document.querySelectorAll('[data-chap]'));
 if(v&&chaps.length){var last=-1;
  v.addEventListener('timeupdate',function(){
   var t=v.currentTime,cur=0;
   chaps.forEach(function(c,i){if(t>=parseFloat(c.getAttribute('data-chap')))cur=i;});
   if(cur===last)return;last=cur;
   chaps.forEach(function(c,i){c.setAttribute('aria-current',i===cur?'true':'false');});
   var a=chaps[cur],w=a.parentNode;
   if(w.scrollWidth>w.clientWidth)w.scrollTo({left:a.offsetLeft-w.clientWidth/2+a.offsetWidth/2,behavior:'smooth'});
  });}
 // ── морф: ползунок «поле → технопарк» ───────────────────────────────────
 var st=document.getElementById('bk-mstack'),rg=document.getElementById('bk-mrange'),
     mt=document.getElementById('bk-mtitle'),md=document.getElementById('bk-mdesc'),
     mm=document.getElementById('bk-mtime'),mp=document.getElementById('bk-mplay'),tm=null;
 function fmt(s){s=Math.floor(s);return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2);}
 if(st&&rg){
  var frames=[].slice.call(st.querySelectorAll('img'));
  function show(i){
   i=Math.max(0,Math.min(frames.length-1,i));
   frames.forEach(function(f,k){f.classList.toggle('on',k===i);});
   mt.textContent=M[i].t;md.textContent=M[i].d;mm.textContent=fmt(M[i].s);
   rg.setAttribute('aria-valuetext',M[i].t);
  }
  rg.addEventListener('input',function(){if(tm){clearInterval(tm);tm=null;mp.setAttribute('aria-pressed','false');}
   show(+rg.value);});
  mp.addEventListener('click',function(){
   if(tm){clearInterval(tm);tm=null;return;}
   var i=(+rg.value>=frames.length-1)?0:+rg.value;
   rg.value=i;show(i);
   tm=setInterval(function(){
    i++;if(i>frames.length-1){clearInterval(tm);tm=null;return;}
    rg.value=i;show(i);},420);
  });
 }
 // ── калькулятор льгот СЭЗ ───────────────────────────────────────────────
 var cr=document.getElementById('bk-crange'),cv=document.getElementById('bk-cv');
 function years(n){var a=n%10,b=n%100;
  if(a===1&&b!==11)return n+' год';
  if(a>=2&&a<=4&&(b<10||b>20))return n+' года';
  return n+' лет';}
 function fill(listId,outId){
  var ul=document.getElementById(listId),out=document.getElementById(outId);
  if(!ul)return;
  var val=parseFloat(cr.value),hit=null;
  [].slice.call(ul.children).forEach(function(li){
   var mn=parseFloat(li.getAttribute('data-min')),mx=parseFloat(li.getAttribute('data-max')),
       on=val>=mn&&val<mx;
   li.classList.toggle('on',on);
   if(on)hit=li.querySelector('span').textContent;});
  if(hit){out.textContent=hit;out.classList.remove('none');}
  else{out.textContent='льготы нет';out.classList.add('none');}
 }
 function recalc(){
  var val=parseFloat(cr.value);
  cv.textContent=(val>=20?'20+':val.toFixed(val<10?1:1).replace('.',','));
  fill('bk-s1','bk-o1');fill('bk-s2','bk-o2');
 }
 if(cr){cr.addEventListener('input',recalc);recalc();}
 // ── появление блоков ────────────────────────────────────────────────────
 var els=[].slice.call(document.querySelectorAll('.bk .r'));
 function inn(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -7% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(n);else io.observe(n);});
})();</script>"""


VIDEO_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"VideoObject","name":"Презентационный ролик технопарка «Бекабад»",'
            '"description":"Презентационный фильм промышленного технопарка «Бекабад» в Ташкентской '
            'области: транспортные коридоры Центральной Азии, аэросъёмка площадки со 3D-мастер-планом, '
            '3D-визуализация корпусов и льготы СЭЗ для резидентов.",'
            '"thumbnailUrl":"https://hand-marketing.ru' + IMG + '/poster.jpg",'
            '"contentUrl":"https://hand-marketing.ru' + VIDEO + '","duration":"PT2M34S",'
            '"uploadDate":"2026-06-01","publisher":{"@type":"Organization",'
            '"name":"Hand Marketing","logo":{"@type":"ImageObject",'
            '"url":"https://hand-marketing.ru/images/lib/as3365-6332-4339-a263-313566616365/152.png"}}}'
            '</script>')

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
                 '"@type":"BreadcrumbList","itemListElement":['
                 '{"@type":"ListItem","position":1,"name":"Проекты",'
                 '"item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"Video Production",'
                 '"item":"https://hand-marketing.ru/videoproduction/"},'
                 '{"@type":"ListItem","position":3,"name":"Технопарк «Бекабад»",'
                 f'"item":"{URL}"}}]}}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Презентационный ролик технопарка «Бекабад»: кейс видеопродакшна | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: презентационный ролик промышленного технопарка «Бекабад» в Ташкентской области. Аэросъёмка площадки, из которой вырастает 3D-мастер-план на 100 гектаров, карты транспортных коридоров Центральной Азии, экскурсия по будущим корпусам и калькулятор льгот СЭЗ.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Технопарк «Бекабад» | кейс Hand Marketing">
<meta property="og:description" content="Презентационный ролик промышленной площадки в Ташкентской области: поле на глазах превращается в технопарк на 100 гектаров.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/poster.jpg">
<meta name="theme-color" content="#04100D">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/raleway-700.css" rel="stylesheet"><link href="/fonts/geologica-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def build():
    body = (f'{rc.header()}<main class="bk">{hero()}{morph()}{geo()}{calc()}{tour()}'
            f'{story()}{final()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{VIDEO_LD}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'bekobod1')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(build())
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
