#!/usr/bin/env python3
"""Генерит mirror/event/mozaika/index.html — кейс «Пора выходить на свет»:
вечер для арендаторов ТЦ «Мозаика», театр NOL, 31 октября 2018, 134 гостя.

Суть вечера: обновлённый знак «Мозаики» включили не кнопкой со сцены. Зал
держали в синем монохроме, каждый гость получал конверт с заданием, искал
в зале проводника света, проходил проверку на доброту намерений и получал
цветную лампочку. Лампочка занимала своё гнездо в световой панели-логотипе.
Последняя лампочка зажгла знак целиком, и освещение зала сменилось на цветное.

Отсюда драматургия страницы: она идёт из темноты в свет тем же жестом.

  • стена в шапке живая. Контур логотипа вынут кривыми из презентации идеи,
    гнёзда расставлены по нему решёткой, и их ровно столько, сколько лампочек
    было в зале: 134 гостевых плюс шесть организаторских, последнее у спикера
    (scripts/mozaika-assets.py). Лампочки вкручиваются кликом и протяжкой,
    загораются цветами, как на съёмке; собранная стена даёт вспышку и включает
    цвет на всей странице;
  • шторка «замысел / что получилось»: рендер стены из презентации идеи
    и кадр собранной стены с вечера;
  • «что меняется в Момент Х» — плитки, которые окрашиваются вместе со светом;
  • план зала: 348 путей схемы из отчёта, перерисованных живым SVG, зоны
    кликаются и подписаны;
  • программа вечера по часам с отметкой Момента Х.

Ассеты: mirror/images/mozaika/ (scripts/mozaika-assets.py), съёмка из нашего
финального отчёта клиенту.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->. index-a2.html в каталоге кейса быть не должно: деплой
переименовал бы его в index.html и затёр кастомную страницу."""
import html as H
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/mozaika'
URL = 'https://hand-marketing.ru/event/mozaika/'
LOGO = json.load(open(os.path.join(ROOT, 'images', 'mozaika', 'logo.json')))
PLAN = json.load(open(os.path.join(ROOT, 'images', 'mozaika', 'plan.json')))
GUESTS = LOGO['guests']

# ─── путь гостя: (кадр, alt, заголовок, текст) ──────────────────────────────
STEPS = [
    ('reception', 'Гости на стойке регистрации у входа в театр NOL',
     'Регистрация',
     'В зоне ресепшена гостей встречали три хостес: отметка в списке, именной '
     'бейдж, гардеробная бирка. По программе дальше значился обычный деловой '
     'вечер с презентацией.'),
    ('handover', 'Девушка в белом костюме передаёт гостю светящуюся лампочку',
     'Проводник света',
     'Вместо этого каждый получал конверт с заданием: найти в зале проводника '
     'света и отдать ему своё письмо. Пройдя проверку на доброту намерений, '
     'гость получал цветную лампочку.'),
    ('wall-empty', 'Панель-логотип «Мозаики» с пустыми гнёздами и первыми лампочками',
     'Своё место в знаке',
     'Лампочку гость ставил в панель, собранную по форме обновлённого знака '
     '«Мозаики». Пока гнёзда пустые, буквы читаются силуэтом: знак есть, '
     'но он не горит.'),
]

# ─── что меняется в Момент Х ────────────────────────────────────────────────
LIT = [
    ('Знак', 'Панель загорается целиком, тем светом, который принесли в зал '
     'сами гости.'),
    ('Свет в зале', 'Синий монохром уходит, помещение забирает полный цвет.'),
    ('Экран', 'На заставке новый знак «Мозаики» и подпись «Делай интересно».'),
    ('Сцена', 'Дальше говорят о конкретике: изменения в комплексе, планы, сроки.'),
    ('Фуршет', 'Открывается кейтеринг: горячая линия плюс станции крем-брюле '
     'и сорбета.'),
    ('Разговор', 'Переговоры идут там, где минуту назад весь зал вместе '
     'включал свет.'),
]

# ─── что было после официальной части ───────────────────────────────────────
AFTER = [
    ('catering', 'Линия фуршета в зале, накрытая до конца вечера',
     'Фуршет', 'После официальной части и до конца вечера работал фуршет. '
     'Помимо основного стола гостей ждали две станции: крем-брюле и сорбет.'),
    ('lottery', 'Ведущий и гостья на сцене вручают сертификат победителю лотереи',
     'Лотерея', 'Розыгрыш призов закрывал официальную часть и заодно собирал '
     'зал обратно к сцене.'),
    ('presswall', 'Гости фотографируются на цветном пресс-волле «Мозаики»',
     'Пресс-волл', 'Фон фотозоны собран из цветных квадратов с новым знаком '
     'и подписью «Делай интересно».'),
    ('gift', 'Фонарики-пауэрбанки с логотипом «Мозаики» на стойке',
     'Подарок', 'На выходе каждый получал фонарик-пауэрбанк с логотипом '
     'комплекса: продолжение истории про свет, который уносят с собой.'),
]

# ─── полиграфия и экран ─────────────────────────────────────────────────────
PRINT = [
    ('badges', 'Именные бейджи на синих лентах',
     'Именные бейджи', 'Печатали заранее по списку: имя, компания, знак.'),
    ('tags', 'Гардеробные бирки с номерами и логотипом',
     'Гардеробные бирки', 'Номерные бирки в фирменном синем: мелочь, которую '
     'гость держит в руках весь вечер.'),
    ('video', 'Кадр из ролика об объекте на большом экране в зале',
     'Ролик об объекте', 'Сняли и смонтировали видео об объекте и его '
     'инфраструктуре: от техзадания до финального монтажа.'),
    ('screen', 'Ведущий на сцене, на экране новый знак «Мозаики» и подпись «Делай интересно»',
     'Экранная графика', 'Заставки и видео-лупы на новом знаке держали зал '
     'между блоками программы.'),
]

# ─── зоны площадки: (ключ, заголовок, текст, X, Y в системе плана) ──────────
ZONES = [
    ('rec', 'Ресепшн', 'Три хостес, список гостей, именные бейджи '
     'и гардеробные бирки.', 598, 112),
    ('wel', 'Велком-дринк', 'Первая точка после регистрации: напитки '
     'и лёгкие закуски, пока собирается зал.', 429, 145),
    ('press', 'Пресс-волл', 'Фотозона у входа в зал, работала весь вечер.', 581, 233),
    ('cat', 'Кейтеринг', 'Линия фуршета и две десертные станции: открывались '
     'после официальной части.', 126, 352),
    ('hall', 'Зал на 200 мест', '170 стульев в основном блоке и ещё 30: '
     '134 гостя разместились свободно.', 497, 560),
    ('logo', 'Свето-лого и проводники', 'Панель-знак стояла у сцены, рядом '
     'работали проводники света с лампочками для гостей.', 336, 660),
]

# ─── программа вечера ───────────────────────────────────────────────────────
PROGRAM = [
    ('16:00', '17:00', 'Встреча гостей',
     'Регистрация, велком-дринк, фотозона. Здесь же конверт, проводник света '
     'и лампочка: к началу официальной части знак был почти собран.', 0),
    ('17:00', '18:10', 'Официальная часть',
     'Ведущий открыл вечер, выступила команда «Мозаики», затем презентацию '
     'продолжили якорные арендаторы. Внутри этого блока и случился Момент Х.', 1),
    ('18:10', '18:30', 'Переговоры и фуршет',
     'Зал уже в цвете, работает кейтеринг, разговоры идут один на один.', 2),
    ('18:30', '18:40', 'Лотерея и закрытие',
     'Розыгрыш призов и официальное закрытие вечера.', 2),
    ('18:40', '21:00', 'Свободное время',
     'Неофициальная часть: музыка, свет, общение без регламента.', 2),
]

# ─── что делало агентство ───────────────────────────────────────────────────
SCOPE = [
    'Концепция и график работ', 'Программа вечера', 'Оформление зала и свет',
    'Свето-панель с логотипом', 'Звук и оборудование презентации', 'Кейтеринг',
    'Дизайн и макеты', 'Полиграфия', 'Сувенирная продукция',
    'Ролик об объекте', 'Экранная графика', 'Персонал и координация',
    'Развлекательная часть', 'Фото- и видеоотчёт',
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
BULB = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.5.4.8 1 .9 1.6h5.2c.1-.6.4-1.2.9-1.6'
        'A6 6 0 0012 3z"/></svg>')

PAGE_CSS = """<style id="mz-css">
:root{
 --mz-ink:#05060E;--mz-navy:#030957;--mz-violet:#4827D8;--mz-pink:#FF3B61;
 --mz-lime:#E0FF00;--mz-mint:#5EFDD4;--mz-amber:#FFC300;
 --mz-paper:#F4F5F8;--mz-dim:#8E93A8;
 --mz-df:'Geologica',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --mz-bf:'Onest',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --mz-mf:'JetBrains Mono',ui-monospace,SFMono-Regular,Consolas,monospace}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.mz{font-family:var(--mz-bf);font-size:17px;line-height:1.62;color:#EDEFF7;
 background:var(--mz-ink);overflow-x:hidden;-webkit-font-smoothing:antialiased}
.mz *{box-sizing:border-box}
.mz img{max-width:100%;height:auto;display:block}
.mz a{color:inherit}
.mz h1,.mz h2,.mz h3{font-family:var(--mz-df);font-weight:800;line-height:1.02;
 letter-spacing:-.035em;margin:0;text-wrap:balance}
.mz p{margin:0 0 1em;text-wrap:pretty}
.mz p:last-child{margin-bottom:0}
.mz-w{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,52px)}
.mz-sec{padding:clamp(56px,8vw,112px) 0;position:relative}
.mz-sec--tight{padding-top:0}
.mz-kick{font-family:var(--mz-mf);font-weight:700;font-size:12px;letter-spacing:.16em;
 text-transform:uppercase;display:inline-flex;align-items:center;gap:10px;color:var(--mz-dim)}
.mz-kick::before{content:"";width:24px;height:10px;flex:none;
 background:linear-gradient(90deg,var(--mz-pink) 0 25%,var(--mz-violet) 25% 50%,
 var(--mz-mint) 50% 75%,var(--mz-lime) 75%)}
.mz h2{font-size:clamp(30px,4.6vw,56px);margin:.36em 0 .5em}
.mz-lead{font-size:clamp(18px,2vw,22px);line-height:1.5;color:#C9CEE2}
.mz-note{font-family:var(--mz-mf);font-size:12px;letter-spacing:.04em;color:var(--mz-dim)}
.mz-btn{display:inline-flex;align-items:center;justify-content:center;gap:.55em;
 font-family:var(--mz-bf);font-weight:700;font-size:15px;padding:.9em 1.5em;border:0;
 cursor:pointer;border-radius:999px;text-decoration:none;
 transition:transform .2s,background .2s,color .2s,border-color .2s,opacity .2s}
.mz-btn svg{width:1.15em;height:1.15em;flex:none}
.mz a.mz-btn--p,.mz-btn--p{background:var(--mz-lime);color:#0B0D16}
.mz-btn--p:hover{transform:translateY(-2px);background:#fff}
.mz a.mz-btn--gh,.mz-btn--gh{background:transparent;color:inherit;
 border:2px solid rgba(237,239,247,.24)}
.mz-btn--gh:hover{border-color:currentColor;transform:translateY(-2px)}
.mz-btn[disabled]{opacity:.35;cursor:default;transform:none}
.mz-r{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.mz-r.is-in{opacity:1;transform:none}

/* ── ШАПКА ── */
.mz-hero{padding:clamp(30px,5vw,60px) 0 clamp(40px,6vw,76px);position:relative;
 background:radial-gradient(120% 80% at 78% 10%,rgba(72,39,216,.45),transparent 62%),
 radial-gradient(90% 70% at 6% 96%,rgba(3,9,87,.9),transparent 72%)}
.mz-hero__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.92fr);
 gap:clamp(30px,4.5vw,58px);align-items:center}
.mz h1{font-size:clamp(42px,7.6vw,96px);margin:.18em 0 .3em;text-transform:uppercase}
.mz h1 em{font-style:normal;display:block;color:var(--mz-lime)}
.mz-hero__chips{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:26px 0 0}
.mz-hero__chips li{font-size:13px;font-weight:600;padding:.42em .9em;border-radius:999px;
 border:1px solid rgba(237,239,247,.2);color:#C9CEE2}
.mz-spec{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin:32px 0 0;
 border-top:1px solid rgba(237,239,247,.14);padding-top:22px}
.mz-spec dt{font-family:var(--mz-df);font-weight:800;font-size:clamp(23px,2.9vw,33px);
 line-height:1;letter-spacing:-.04em}
.mz-spec dd{margin:6px 0 0;font-size:13px;line-height:1.35;color:var(--mz-dim)}
.mz-spec div:nth-child(1) dt{color:var(--mz-amber)}
.mz-spec div:nth-child(2) dt{color:var(--mz-mint)}
.mz-spec div:nth-child(3) dt{color:var(--mz-pink)}
.mz-spec div:nth-child(4) dt{color:var(--mz-lime)}

/* ── ЖИВАЯ ПАНЕЛЬ-ЗНАК ── */
.mz-wall__panel{position:relative;background:#0A0B14;border:1px solid rgba(237,239,247,.14);
 border-radius:6px;padding:clamp(14px,2.4vw,26px);touch-action:pan-y;
 box-shadow:0 30px 90px rgba(0,0,0,.55)}
.mz-wall__panel svg{width:100%;height:auto;display:block;cursor:crosshair}
.mz-s{fill:#0D0E18;stroke:#2C3050;stroke-width:2;transition:fill .3s ease}
.mz-s.is-on{fill:url(#mz-b0)}
.mz-s.c1{fill:url(#mz-b1)}.mz-s.c2{fill:url(#mz-b2)}.mz-s.c3{fill:url(#mz-b3)}
.mz-s.c4{fill:url(#mz-b4)}.mz-s.c5{fill:url(#mz-b5)}
.mz.is-lit .mz-s.is-on,.mz.is-lit .mz-s.c1,.mz.is-lit .mz-s.c2,.mz.is-lit .mz-s.c3,
.mz.is-lit .mz-s.c4,.mz.is-lit .mz-s.c5{fill:url(#mz-b0)}
.mz-s--staff{stroke:rgba(224,255,0,.5);stroke-dasharray:4 4}
.mz-bulbs{filter:url(#mz-glow)}
.mz-wall__flash{position:absolute;inset:0;border-radius:6px;background:#fff;opacity:0;
 pointer-events:none}
.mz-wall__panel.is-flash .mz-wall__flash{animation:mz-flash 1.5s ease-out}
@keyframes mz-flash{0%{opacity:0}8%{opacity:.92}100%{opacity:0}}
.mz-hud{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;margin-top:18px}
.mz-hud__count{font-family:var(--mz-mf);font-size:13px;letter-spacing:.06em;color:#C9CEE2;
 flex:1 1 190px;min-width:170px}
.mz-hud__count b{display:block;font-family:var(--mz-df);font-size:26px;font-weight:800;
 letter-spacing:-.03em;color:var(--mz-amber);line-height:1.1}
.mz-hud__bar{display:block;height:4px;border-radius:2px;background:rgba(237,239,247,.14);
 margin-top:8px;overflow:hidden}
.mz-hud__bar i{display:block;height:100%;width:0;background:var(--mz-amber);
 transition:width .3s ease}
.mz-hud__hint{flex:1 1 100%;font-family:var(--mz-mf);font-size:12px;color:var(--mz-dim);
 letter-spacing:.03em;margin:0}
.mz-hud .mz-btn{font-size:14px;padding:.75em 1.25em}

/* ── ТЕКСТ И КАДРЫ ── */
.mz-two{display:grid;grid-template-columns:minmax(0,.86fr) minmax(0,1fr);
 gap:clamp(26px,4vw,58px);align-items:start}
.mz-quote{border-left:3px solid var(--mz-pink);padding:2px 0 2px 22px;margin:0 0 26px;
 font-family:var(--mz-df);font-weight:500;font-size:clamp(19px,2.4vw,25px);line-height:1.32;
 letter-spacing:-.02em;color:#fff}
.mz-quote cite{display:block;margin-top:12px;font:400 13px/1.4 var(--mz-mf);
 font-style:normal;color:var(--mz-dim);letter-spacing:.04em}
.mz-fig{margin:0}
.mz-fig img{border-radius:4px}
.mz-fig figcaption{margin-top:10px;font-family:var(--mz-mf);font-size:12px;color:var(--mz-dim)}
.mz-pair{display:grid;grid-template-columns:1fr 1fr;gap:clamp(12px,1.8vw,20px);
 margin-top:clamp(24px,3.4vw,42px)}
.mz-pair figure{margin:0;position:relative}
.mz-pair img{border-radius:4px;aspect-ratio:16/10;object-fit:cover;width:100%}
.mz-pair figcaption{position:absolute;left:12px;top:12px;font:700 11px/1 var(--mz-mf);
 letter-spacing:.14em;text-transform:uppercase;padding:.6em .85em;border-radius:999px;
 background:rgba(5,6,14,.62);backdrop-filter:blur(6px);color:#fff}
.mz-pair figure:last-child figcaption{background:rgba(255,255,255,.8);color:#0B0D16}

/* ── ШТОРКА ЗАМЫСЕЛ/РЕЗУЛЬТАТ ── */
.mz-vs{position:relative;border-radius:4px;overflow:hidden;user-select:none;
 aspect-ratio:4/3;background:#0A0B14}
.mz-vs img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.mz-vs__top{clip-path:inset(0 0 0 var(--mz-x,50%))}
.mz-vs__lb{position:absolute;top:14px;font:700 11px/1 var(--mz-mf);letter-spacing:.14em;
 text-transform:uppercase;padding:.6em .9em;border-radius:999px;backdrop-filter:blur(6px);
 background:rgba(5,6,14,.6);color:#fff;pointer-events:none}
.mz-vs__lb.l{left:14px}
.mz-vs__lb.r{right:14px;background:rgba(255,255,255,.78);color:#0B0D16}
.mz-vs input{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;
 cursor:ew-resize;-webkit-appearance:none;appearance:none;background:transparent}
.mz-vs__hd{position:absolute;top:0;bottom:0;left:var(--mz-x,50%);width:2px;
 background:#fff;pointer-events:none;box-shadow:0 0 18px rgba(0,0,0,.5)}
.mz-vs__hd::after{content:"";position:absolute;top:50%;left:50%;width:44px;height:44px;
 transform:translate(-50%,-50%);border-radius:50%;background:#fff;
 box-shadow:0 6px 22px rgba(0,0,0,.4)}
.mz-vs__hd::before{content:"";position:absolute;top:50%;left:50%;width:16px;height:10px;
 transform:translate(-50%,-50%);z-index:1;background:#0B0D16;
 clip-path:polygon(0 50%,40% 0,40% 100%,60% 0,60% 100%,100% 50%)}
.mz-vs:focus-within .mz-vs__hd::after{box-shadow:0 0 0 4px var(--mz-lime)}

/* ── КАРТОЧКИ ── */
.mz-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(16px,2.4vw,28px);
 margin-top:clamp(28px,4vw,50px);list-style:none;padding:0}
.mz-cards--4{grid-template-columns:repeat(4,minmax(0,1fr))}
.mz-card{background:#0A0B14;border:1px solid rgba(237,239,247,.12);border-radius:4px;
 overflow:hidden;display:flex;flex-direction:column}
.mz-card img{aspect-ratio:4/3;object-fit:cover;width:100%}
.mz-card__b{padding:clamp(16px,2vw,24px)}
.mz-card__n{font:700 12px/1 var(--mz-mf);letter-spacing:.14em;color:var(--mz-mint);margin:0}
.mz-card h3{font-size:clamp(18px,2vw,24px);margin:12px 0 10px}
.mz-card p{font-size:15px;color:#C9CEE2;margin:0}
.mz-sec--light .mz-card{background:#fff;border-color:rgba(11,13,22,.1)}
.mz-sec--light .mz-card p{color:#41465C}
.mz-sec--light .mz-card__n{color:var(--mz-violet)}

/* ── МОМЕНТ Х ── */
.mz-x{background:radial-gradient(80% 60% at 50% 0%,rgba(72,39,216,.5),transparent 70%),
 var(--mz-navy)}
.mz-x img{filter:saturate(.2) brightness(.62);transition:filter 1.1s ease}
.mz.is-lit .mz-x img{filter:none}
.mz-lit-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;
 list-style:none;padding:0;margin:clamp(24px,3vw,40px) 0 0}
.mz-lit-grid li{border:1px solid rgba(237,239,247,.16);border-radius:4px;padding:18px;
 transition:background .8s ease,border-color .8s ease,color .8s ease}
.mz-lit-grid h3{font-size:17px;margin:0 0 6px;letter-spacing:-.02em}
.mz-lit-grid p{font-size:14px;color:#C9CEE2;margin:0}
.mz.is-lit .mz-lit-grid li{color:#0B0D16;border-color:transparent}
.mz.is-lit .mz-lit-grid p{color:rgba(11,13,22,.72)}
.mz.is-lit .mz-lit-grid li:nth-child(6n+1){background:var(--mz-lime)}
.mz.is-lit .mz-lit-grid li:nth-child(6n+2){background:var(--mz-mint)}
.mz.is-lit .mz-lit-grid li:nth-child(6n+3){background:var(--mz-amber)}
.mz.is-lit .mz-lit-grid li:nth-child(6n+4){background:var(--mz-pink);color:#fff}
.mz.is-lit .mz-lit-grid li:nth-child(6n+4) p{color:rgba(255,255,255,.82)}
.mz.is-lit .mz-lit-grid li:nth-child(6n+5){background:#fff}
.mz.is-lit .mz-lit-grid li:nth-child(6n+6){background:var(--mz-violet);color:#fff}
.mz.is-lit .mz-lit-grid li:nth-child(6n+6) p{color:rgba(255,255,255,.82)}
.mz-x__state{font-family:var(--mz-mf);font-size:12px;letter-spacing:.06em;color:var(--mz-dim);
 margin-top:18px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.mz-x__state i{width:9px;height:9px;border-radius:50%;background:#3A3E52;flex:none}
.mz.is-lit .mz-x__state i{background:var(--mz-lime);box-shadow:0 0 12px var(--mz-lime)}

/* ── СВЕТЛЫЕ СЕКЦИИ ── */
.mz-sec--light{background:var(--mz-paper);color:#0B0D16}
.mz-sec--light .mz-lead{color:#41465C}
.mz-sec--light .mz-kick,.mz-sec--light .mz-note,.mz-sec--light .mz-fig figcaption{color:#6B7188}
.mz-sec--light .mz-quote{color:#0B0D16}
.mz-sec--light .mz-btn--gh{border-color:rgba(11,13,22,.18)}

/* ── ПЛАН ЗАЛА ── */
.mz-plan{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);
 gap:clamp(22px,3vw,44px);align-items:start;margin-top:clamp(26px,3.6vw,44px)}
.mz-plan__map{background:#0B0D16;border-radius:4px;padding:clamp(10px,1.6vw,18px)}
.mz-plan__map svg{width:100%;height:auto;display:block}
.mz-plan__pin{cursor:pointer}
.mz-plan__pin circle{transition:r .25s ease,opacity .25s ease}
.mz-plan__pin .dot{fill:var(--mz-amber)}
.mz-plan__pin .halo{fill:var(--mz-amber);opacity:.22}
.mz-plan__pin[aria-pressed="true"] .halo{opacity:.42}
.mz-plan__list{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px}
.mz-plan__list button{width:100%;text-align:left;background:#fff;border:1px solid rgba(11,13,22,.12);
 border-radius:4px;padding:14px 16px;cursor:pointer;font-family:var(--mz-bf);color:inherit;
 transition:border-color .2s,transform .2s}
.mz-plan__list button:hover{transform:translateX(3px)}
.mz-plan__list button[aria-pressed="true"]{border-color:var(--mz-violet);
 box-shadow:inset 3px 0 0 var(--mz-violet)}
.mz-plan__list h3{font-size:16px;margin:0 0 4px}
.mz-plan__list p{font-size:14px;color:#41465C;margin:0;display:none}
.mz-plan__list button[aria-pressed="true"] p{display:block}

/* ── ПРОГРАММА ── */
.mz-prog{margin-top:clamp(26px,3.6vw,44px);border-top:1px solid rgba(11,13,22,.14)}
.mz-prog__row{display:grid;grid-template-columns:150px 1fr;gap:clamp(14px,3vw,38px);
 padding:22px 0;border-bottom:1px solid rgba(11,13,22,.14);position:relative}
.mz-prog__t{font-family:var(--mz-mf);font-size:14px;font-weight:700;color:#0B0D16;
 white-space:nowrap;margin:0}
.mz-prog__t span{display:block;font-weight:400;color:#6B7188;font-size:12px;margin-top:4px}
.mz-prog h3{font-size:clamp(19px,2vw,23px);margin:0 0 8px}
.mz-prog p{font-size:15px;color:#41465C;margin:0}
.mz-prog__row::before{content:"";position:absolute;left:-14px;top:26px;width:6px;height:6px;
 border-radius:50%;background:#C6CAD6}
.mz-prog__row[data-ph="1"]::before{background:var(--mz-amber);
 box-shadow:0 0 0 5px rgba(255,195,0,.22)}
.mz-prog__row[data-ph="2"]::before{background:var(--mz-violet)}
.mz-prog__x{display:inline-flex;align-items:center;gap:8px;margin-top:12px;
 font:700 12px/1 var(--mz-mf);letter-spacing:.12em;text-transform:uppercase;
 background:var(--mz-amber);color:#0B0D16;padding:.62em .9em;border-radius:999px}
.mz-prog__x svg{width:14px;height:14px}

/* ── ИТОГ И ОБЪЁМ РАБОТ ── */
.mz-out{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(18px,2.6vw,34px);
 margin-top:clamp(26px,3.6vw,44px);list-style:none;padding:0}
.mz-out li{border-top:3px solid var(--mz-violet);padding-top:18px}
.mz-out li:nth-child(2){border-color:var(--mz-pink)}
.mz-out li:nth-child(3){border-color:var(--mz-mint)}
.mz-out h3{font-size:clamp(18px,1.9vw,22px);margin:0 0 10px}
.mz-out p{font-size:15px;color:#41465C;margin:0}
.mz-scope{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;
 margin:clamp(22px,3vw,34px) 0 0}
.mz-scope li{font-size:14px;font-weight:600;padding:.5em 1em;border-radius:999px;
 background:#fff;border:1px solid rgba(11,13,22,.1)}

@media (max-width:980px){
 .mz-hero__grid,.mz-two,.mz-plan{grid-template-columns:1fr}
 .mz-cards,.mz-cards--4,.mz-lit-grid,.mz-out{grid-template-columns:1fr 1fr}
 .mz-spec{grid-template-columns:repeat(2,1fr);gap:14px}
}
@media (max-width:640px){
 .mz{font-size:16px}
 .mz-cards,.mz-cards--4,.mz-lit-grid,.mz-out,.mz-pair{grid-template-columns:1fr}
 .mz-prog__row{grid-template-columns:1fr;gap:8px}
 .mz-vs{aspect-ratio:4/3}
 .mz-hud .mz-btn{flex:1 1 100%}
}
@media (prefers-reduced-motion:reduce){
 html{scroll-behavior:auto}
 .mz-r{opacity:1;transform:none;transition:none}
 .mz *,.mz *::before,.mz *::after{animation-duration:.01ms!important;transition-duration:.01ms!important}
}
</style>"""


# ─── живая панель-знак ──────────────────────────────────────────────────────
def wall_svg():
    pts = LOGO['sockets']
    n = len(pts)
    staff_n = LOGO['staff']
    # гнёзда организаторов раскиданы по всей панели, последнее достаётся спикеру
    staff = {round(i * (n - 1) / (staff_n - 1)) for i in range(staff_n)}
    r = LOGO['step'] * .40
    circles = []
    for i, (x, y) in enumerate(pts):
        cls = 'mz-s mz-s--staff' if i in staff else 'mz-s'
        flag = ' data-staff="1"' if i in staff else ''
        circles.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r:.1f}" '
                       f'data-i="{i}"{flag}/>')
    # цвета лампочек с вечера: тёплый белый, жёлтый, красный, зелёный, синий
    grads = ''.join(
        f'<radialGradient id="mz-b{i}" cx="38%" cy="34%" r="72%">'
        f'<stop offset="0" stop-color="{a}"/><stop offset=".5" stop-color="{b}"/>'
        f'<stop offset="1" stop-color="{c}"/></radialGradient>'
        for i, (a, b, c) in enumerate((
            ('#FFFDF2', '#FFE9A8', '#FFB020'),   # 0: общий свет после Момента Х
            ('#FFFBE8', '#FFE06A', '#F2A100'),   # 1: жёлтая
            ('#FFE2E8', '#FF6B84', '#D8123C'),   # 2: красная
            ('#E8FFE9', '#66E06B', '#0C9B2E'),   # 3: зелёная
            ('#E4F0FF', '#5B9BFF', '#0B3ED8'),   # 4: синяя
            ('#FFFFFF', '#D8DEF0', '#8E9AC0'),   # 5: белая
        )))
    return (
      f'<svg viewBox="0 0 {LOGO["w"]} {LOGO["h"]}" role="img" aria-labelledby="mz-wall-t" '
      'data-wall>'
      f'<title id="mz-wall-t">Панель-логотип «Мозаики» из ламповых гнёзд: {n} гнёзд, '
      'каждое ждёт свою лампочку</title>'
      f'<defs>{grads}'
      '<filter id="mz-glow" x="-25%" y="-25%" width="150%" height="150%">'
      '<feGaussianBlur stdDeviation="4" result="b"/>'
      '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
      '</defs>'
      f'<path d="{LOGO["d"]}" fill="#191C36" fill-rule="evenodd"/>'
      f'<g class="mz-bulbs">{"".join(circles)}</g></svg>'), n, staff_n


def hero():
    svg, total, staff = wall_svg()
    chips = ''.join(f'<li>{c}</li>' for c in (
        'Концепция', 'Программа', 'Оформление зала', 'Свето-панель',
        'Кейтеринг', 'Полиграфия', 'Ролик об объекте'))
    spec = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in (
        (f'{GUESTS}', 'гостя на вечере'),
        ('5', 'часов программы'),
        ('2', 'части вечера: синяя и цветная'),
        ('1', 'выключатель на весь зал'),
    ))
    return (
      '<header class="mz-hero" id="top"><div class="mz-w"><div class="mz-hero__grid">'
      '<div class="mz-r is-in">'
      '<p class="mz-kick">Event · ТЦ «Мозаика» · Москва · 31 октября 2018</p>'
      '<h1>Пора выходить<em>на свет</em></h1>'
      '<p class="mz-lead">Вечер для арендаторов торгового центра, на котором '
      'обновлённый знак «Мозаики» включили не кнопкой со сцены. Свет в зале '
      f'собрали сами гости: {GUESTS} человека, у каждого своя лампочка.</p>'
      f'<ul class="mz-hero__chips">{chips}</ul>'
      f'<dl class="mz-spec">{spec}</dl>'
      '</div>'
      '<div class="mz-wall mz-r is-in">'
      f'<div class="mz-wall__panel" data-panel>{svg}<span class="mz-wall__flash"></span></div>'
      '<div class="mz-hud">'
      '<p class="mz-hud__count" role="status" aria-live="polite">'
      f'<b><span data-on>0</span> / {total - staff}</b>лампочек в гнёздах'
      '<span class="mz-hud__bar"><i data-bar></i></span></p>'
      '<button class="mz-btn mz-btn--gh" type="button" data-all>Собрать всем залом</button>'
      f'<button class="mz-btn mz-btn--p" type="button" data-x disabled>{BULB}'
      'Лампочка спикера</button>'
      '<p class="mz-hud__hint" data-hint>Проведите по панели или нажмите на гнездо, '
      f'и лампочка встанет на место. {staff} гнёзд оставлены организаторам.</p>'
      '</div></div>'
      '</div></div></header>')


def task():
    return (
      '<section class="mz-sec"><div class="mz-w"><div class="mz-two">'
      '<div class="mz-r"><p class="mz-kick">Задача</p>'
      '<h2>Сменить оптику,<br>а не показать слайд</h2></div>'
      '<div class="mz-r"><p class="mz-lead">У «Мозаики» шло обновление: новый '
      'знак, новая программа развития комплекса. Но бизнес-аудитория смотрела '
      'на объект по инерции и считала его тусклым и отстающим.</p>'
      '<p>Клиент ставил две задачи: переломить это восприятие и рассказать '
      'ритейлерам о происходящих и предстоящих изменениях. Обычная связка '
      '«презентация плюс фуршет» решает только вторую: информацию донесёт, '
      'а ощущение оставит прежним.</p>'
      '<p>Значит, менять надо не текст доклада, а состояние зала. И сделать так, '
      'чтобы это состояние переключили сами арендаторы.</p></div>'
      '</div>'
      '<figure class="mz-fig mz-r" style="margin-top:clamp(26px,3.6vw,44px)">'
      f'<img src="{IMG}/task.jpg" alt="Зал в синем свете, выступление на сцене '
      'перед арендаторами" width="1600" height="962" loading="lazy" decoding="async">'
      '<figcaption>Театр NOL внутри самого комплекса: зал держали в синем '
      'монохроме до Момента Х</figcaption></figure>'
      '</div></section>')


def idea():
    return (
      '<section class="mz-sec"><div class="mz-w">'
      '<div class="mz-two">'
      '<div class="mz-r">'
      '<p class="mz-kick">Идея</p>'
      '<h2>Из темноты<br>в цвет</h2>'
      '<blockquote class="mz-quote">После долгого нахождения в темноте солнечный '
      'свет на мгновение ослепляет. Но всё постепенно становится понятным '
      'и обретает краски.<cite>Из презентации идеи клиенту</cite></blockquote>'
      '<p>Программу поделили на две части. Первую зал проводит в синем монохроме: '
      'видно очертания, соседа и сцену, но не цвет. Вторая начинается в секунду, '
      'когда знак «Мозаики» загорается целиком.</p>'
      '<p>Между частями нет перерыва в программе. Есть действие, которое зал '
      'выполняет вместе: у каждого гостя своя лампочка, и знак не горит, пока '
      'в нём остаётся хотя бы одно пустое гнездо.</p>'
      '</div>'
      '<div class="mz-r"><p class="mz-lead">Панель-знак стояла у сцены весь вечер '
      'и работала счётчиком: по ней было видно, сколько человек уже дошло '
      'до проводника света, и сколько гнёзд ещё пустует.</p>'
      '<p>Это же снимало неловкость первого часа. Гость приходил не «постоять '
      'до начала», а сделать конкретное дело, у которого есть видимый результат '
      'на стене.</p></div>'
      '</div>'
      '<div class="mz-r" style="margin-top:clamp(30px,4vw,52px)">'
      '<div class="mz-vs" data-vs>'
      f'<img src="{IMG}/concept-wall.jpg" alt="Рендер стены-логотипа из презентации '
      'идеи" width="834" height="816" loading="lazy" decoding="async">'
      f'<img class="mz-vs__top" src="{IMG}/wall-lit.jpg" '
      'alt="Собранная панель-знак «Мозаики» горит целиком" '
      'width="1220" height="1203" loading="lazy" decoding="async">'
      '<span class="mz-vs__lb l">Замысел</span>'
      '<span class="mz-vs__lb r">Что получилось</span>'
      '<span class="mz-vs__hd" data-hd></span>'
      '<input type="range" min="0" max="100" value="50" step="1" '
      'aria-label="Граница между рендером из презентации и кадром с вечера" data-range>'
      '</div>'
      '<p class="mz-note" style="margin-top:10px">Слева рендер, который мы '
      'показывали клиенту до вечера. Справа тот же знак, собранный гостями.</p>'
      '</div>'
      '</div></section>')


def path_of_guest():
    steps = ''.join(
        f'<li class="mz-card mz-r"><img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" '
        'loading="lazy" decoding="async">'
        f'<div class="mz-card__b"><p class="mz-card__n">Шаг {i + 1}</p>'
        f'<h3>{t}</h3><p>{txt}</p></div></li>'
        for i, (f, alt, t, txt) in enumerate(STEPS))
    return (
      '<section class="mz-sec mz-sec--tight"><div class="mz-w">'
      '<div class="mz-two"><div class="mz-r"><p class="mz-kick">Путь гостя</p>'
      '<h2>Час до начала,<br>занятый делом</h2></div>'
      '<div class="mz-r"><p class="mz-lead">Первый час деловых вечеров обычно '
      'уходит впустую: гости стоят с бокалом и ждут регламент. Мы заняли его '
      'действием, у которого есть продолжение в официальной части.</p></div></div>'
      f'<ul class="mz-cards">{steps}</ul>'
      '</div></section>')


def moment_x():
    tiles = ''.join(f'<li><h3>{t}</h3><p>{txt}</p></li>' for t, txt in LIT)
    return (
      '<section class="mz-sec mz-x" id="momentx"><div class="mz-w">'
      '<div class="mz-two"><div class="mz-r"><p class="mz-kick">Момент Х</p>'
      '<h2>Последняя<br>лампочка</h2></div>'
      '<div class="mz-r"><p class="mz-lead">В официальной части спикер вкручивает '
      'лампочку в последнее свободное гнездо. Знак загорается целиком, и свет '
      'уходит с панели в зал.</p>'
      '<p>Синяя заливка сменяется цветной, зал буквально проживает переход из '
      'одного состояния в другое. Дальше разговор о комплексе идёт уже в другой '
      'температуре: люди только что вместе сделали то, о чём им рассказывают.</p>'
      '<p class="mz-x__state"><i></i><span data-xstate>Свет выключен: '
      'знак ещё не собран</span></p></div></div>'
      '<figure class="mz-fig mz-r" style="margin-top:clamp(26px,3.6vw,42px)">'
      f'<img src="{IMG}/lighting.jpg" alt="Спикер вкручивает последнюю лампочку '
      'в светящуюся панель-логотип «Мозаики»" width="1600" height="961" '
      'loading="lazy" decoding="async">'
      '<figcaption>Та самая последняя лампочка</figcaption></figure>'
      '<div class="mz-pair mz-r">'
      f'<figure><img src="{IMG}/hall-blue.jpg" alt="Зал в синем монохромном свете '
      'до Момента Х" width="1600" height="962" loading="lazy" decoding="async">'
      '<figcaption>До</figcaption></figure>'
      f'<figure><img src="{IMG}/hall-color.jpg" alt="Зал в цветном свете после '
      'Момента Х" width="1000" height="605" loading="lazy" decoding="async">'
      '<figcaption>После</figcaption></figure>'
      '</div>'
      f'<ul class="mz-lit-grid mz-r">{tiles}</ul>'
      '</div></section>')


def official():
    return (
      '<section class="mz-sec mz-sec--light"><div class="mz-w"><div class="mz-two">'
      '<div class="mz-r"><p class="mz-kick">Официальная часть</p>'
      '<h2>Кто выходил<br>на сцену</h2></div>'
      '<div class="mz-r"><p class="mz-lead">Ведущий открыл вечер и объяснил '
      'структуру. Дальше выступала команда «Мозаики», затем презентацию '
      'продолжили якорные арендаторы.</p>'
      '<p>Между блоками работал экран: ролик об объекте и его инфраструктуре мы '
      'сняли и смонтировали сами, заставки и лупы собраны на новом знаке '
      'с подписью «Делай интересно».</p></div></div>'
      '<div class="mz-pair mz-r">'
      f'<figure><img src="{IMG}/host.jpg" alt="Ведущий открывает вечер, справа '
      'светится панель-знак" width="1600" height="974" loading="lazy" decoding="async">'
      '</figure>'
      f'<figure><img src="{IMG}/official.jpg" alt="Выступление на сцене во время '
      'официальной части" width="1600" height="962" loading="lazy" decoding="async">'
      '</figure>'
      '</div></div></section>')


def after():
    cards = ''.join(
        f'<li class="mz-card mz-r"><img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" '
        f'loading="lazy" decoding="async"><div class="mz-card__b"><h3>{t}</h3>'
        f'<p>{txt}</p></div></li>' for f, alt, t, txt in AFTER)
    return (
      '<section class="mz-sec mz-sec--light mz-sec--tight"><div class="mz-w">'
      '<div class="mz-two"><div class="mz-r"><p class="mz-kick">Дальше</p>'
      '<h2>Вечер<br>в цвете</h2></div>'
      '<div class="mz-r"><p class="mz-lead">После официальной части зал перешёл '
      'в свободный режим: фуршет, лотерея, фотозона. К этому моменту тема '
      'мозаики жила уже не на экране, а на предметах, к которым гость '
      'прикасается.</p></div></div>'
      f'<ul class="mz-cards mz-cards--4">{cards}</ul>'
      '</div></section>')


def print_part():
    cards = ''.join(
        f'<li class="mz-card mz-r"><img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" '
        f'loading="lazy" decoding="async"><div class="mz-card__b"><h3>{t}</h3>'
        f'<p>{txt}</p></div></li>' for f, alt, t, txt in PRINT)
    return (
      '<section class="mz-sec mz-sec--light mz-sec--tight"><div class="mz-w">'
      '<div class="mz-two"><div class="mz-r"><p class="mz-kick">Материалы</p>'
      '<h2>Всё, что гость<br>держал в руках</h2></div>'
      '<div class="mz-r"><p class="mz-lead">Полиграфию, сувенирку и экранную '
      'графику готовили в одном ключе с новым знаком: от именного бейджа '
      'до фонарика, который гость уносил домой.</p></div></div>'
      f'<ul class="mz-cards mz-cards--4">{cards}</ul>'
      '</div></section>')


def venue():
    pins = ''.join(
        f'<g class="mz-plan__pin" data-pin="{k}" role="button" tabindex="0" '
        f'aria-pressed="{"true" if i == 0 else "false"}" aria-label="{H.escape(t)}">'
        f'<circle class="halo" cx="{x}" cy="{y}" r="26"/>'
        f'<circle class="dot" cx="{x}" cy="{y}" r="9"/></g>'
        for i, (k, t, txt, x, y) in enumerate(ZONES))
    items = ''.join(
        f'<li><button type="button" data-zone="{k}" '
        f'aria-pressed="{"true" if i == 0 else "false"}">'
        f'<h3>{t}</h3><p>{txt}</p></button></li>'
        for i, (k, t, txt, x, y) in enumerate(ZONES))
    return (
      '<section class="mz-sec mz-sec--light mz-sec--tight"><div class="mz-w">'
      '<div class="mz-two"><div class="mz-r"><p class="mz-kick">Площадка</p>'
      '<h2>Театр NOL<br>внутри комплекса</h2></div>'
      '<div class="mz-r"><p class="mz-lead">Вечер собрали на втором этаже самой '
      '«Мозаики»: Москва, 7-я Кожуховская, 9. Гостю не нужно было никуда ехать, '
      'а сам объект работал декорацией к разговору о нём.</p>'
      '<p>Схема зала из нашего отчёта: 200 стульев в двух блоках, зоны '
      'велком-дринка, кейтеринга и фотозоны по периметру, панель-знак '
      'и проводники света у сцены.</p></div></div>'
      '<div class="mz-plan mz-r">'
      '<div class="mz-plan__map">'
      f'<svg viewBox="0 0 {PLAN["w"]} {PLAN["h"]}" role="img" '
      'aria-label="План зала театра NOL с зонами вечера">'
      f'<path d="{PLAN["d"]}" fill="#F4F5F8"/>{pins}</svg></div>'
      f'<ul class="mz-plan__list" data-zones>{items}</ul>'
      '</div></div></section>')


def program():
    rows = ''
    for a, b, t, txt, ph in PROGRAM:
        x = ('<p class="mz-prog__x">' + BULB + 'Момент Х</p>') if ph == 1 else ''
        span = f'<span>до {b}</span>' if b else ''
        rows += (f'<div class="mz-prog__row" data-ph="{ph}">'
                 f'<p class="mz-prog__t">{a}{span}</p>'
                 f'<div><h3>{t}</h3><p>{txt}</p>{x}</div></div>')
    return (
      '<section class="mz-sec mz-sec--light mz-sec--tight"><div class="mz-w">'
      '<div class="mz-two"><div class="mz-r"><p class="mz-kick">Программа</p>'
      '<h2>Вечер<br>по часам</h2></div>'
      '<div class="mz-r"><p class="mz-lead">Тёмная часть занимает первый час '
      'с небольшим: ровно столько, сколько нужно, чтобы все гости успели дойти '
      'до панели. Дальше зал работает в цвете до самого закрытия.</p></div></div>'
      f'<div class="mz-prog mz-r">{rows}</div>'
      '</div></section>')


def outro():
    cards = ''.join(f'<li class="mz-r"><h3>{t}</h3><p>{txt}</p></li>' for t, txt in (
        (f'{GUESTS} гостя, {GUESTS} действия',
         'Арендаторы и сотрудники комплекса. Каждый нашёл проводника, получил '
         'лампочку и поставил её в знак: зрителей на вечере не было.'),
        ('Новый знак не показали, а зажгли',
         'Обновлённая «Мозаика» появилась в зале не слайдом, а светом, '
         'который включили те самые люди, ради которых шло обновление.'),
        ('KPI проекта выполнены',
         'Формулировка из финального отчёта клиенту. Вечер прошёл по программе '
         'от регистрации до свободной части, без сдвигов тайминга.'),
    ))
    scope = ''.join(f'<li>{s}</li>' for s in SCOPE)
    return (
      '<section class="mz-sec mz-sec--light mz-sec--tight"><div class="mz-w">'
      '<div class="mz-r"><p class="mz-kick">Итог</p>'
      '<h2>Что осталось<br>после вечера</h2></div>'
      f'<ul class="mz-out">{cards}</ul>'
      '<figure class="mz-fig mz-r" style="margin-top:clamp(30px,4vw,52px)">'
      f'<img src="{IMG}/team.jpg" alt="Общий кадр команды «Мозаики» на сцене '
      'в финале вечера" width="1002" height="600" loading="lazy" decoding="async">'
      '<figcaption>Финал вечера: команда «Мозаики» на сцене</figcaption></figure>'
      '<div class="mz-r" style="margin-top:clamp(36px,5vw,64px)">'
      '<p class="mz-kick">Что делало агентство</p>'
      f'<ul class="mz-scope">{scope}</ul></div>'
      '</div></section>')


PAGE_JS = """<script>(function(){
 var main=document.querySelector('.mz');if(!main)return;
 var calm=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;
 // ── панель-знак: гнёзда, счётчик, Момент Х ───────────────────────────────
 var wall=document.querySelector('[data-wall]'),panel=document.querySelector('[data-panel]'),
     lit=false;
 if(wall){
  var socks=[].slice.call(wall.querySelectorAll('.mz-s')),
      guests=socks.filter(function(s){return !s.getAttribute('data-staff');}),
      staff=socks.filter(function(s){return s.getAttribute('data-staff');}),
      out=document.querySelector('[data-on]'),bar=document.querySelector('[data-bar]'),
      bAll=document.querySelector('[data-all]'),bX=document.querySelector('[data-x]'),
      hint=document.querySelector('[data-hint]'),state=document.querySelector('[data-xstate]'),
      on=0,drag=false;
  function upd(){
   if(out)out.textContent=on;
   if(bar)bar.style.width=(on/guests.length*100)+'%';
   var full=on>=guests.length;
   if(bX)bX.disabled=!full||lit;
   if(bAll)bAll.disabled=full;
   if(hint&&!lit)hint.textContent=full
    ?'Все гостевые лампочки на месте. Осталась лампочка спикера.'
    :'Проведите по панели или нажмите на гнездо, и лампочка встанет на место. '
     +staff.length+' гнёзд оставлены организаторам.';
  }
  function turn(el){
   if(!el||!el.classList||!el.classList.contains('mz-s'))return;
   if(el.getAttribute('data-staff')||el.classList.contains('is-on'))return;
   // цвет лампочки случайный, как в коробках у проводников света
   el.classList.add('is-on','c'+(1+Math.floor(Math.random()*5)));
   on++;upd();
  }
  function at(x,y){turn(document.elementFromPoint(x,y));}
  panel.addEventListener('pointerdown',function(e){drag=true;at(e.clientX,e.clientY);});
  panel.addEventListener('pointermove',function(e){
   if(drag){e.preventDefault();at(e.clientX,e.clientY);}});
  ['pointerup','pointercancel','pointerleave'].forEach(function(t){
   panel.addEventListener(t,function(){drag=false;});});
  function light(flash){
   if(lit)return;lit=true;
   socks.forEach(function(s){s.classList.add('is-on');});on=guests.length;
   main.classList.add('is-lit');upd();
   if(bX)bX.disabled=true;if(bAll)bAll.disabled=true;
   if(hint)hint.textContent='Момент Х: знак горит целиком, зал уходит в цвет.';
   if(state)state.textContent='Свет включён: знак собран, начинается вторая часть вечера';
   if(flash&&!calm&&panel){panel.classList.add('is-flash');
    setTimeout(function(){panel.classList.remove('is-flash');},1600);}
  }
  if(bAll)bAll.addEventListener('click',function(){
   var left=guests.filter(function(s){return !s.classList.contains('is-on');});
   for(var i=left.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=left[i];
    left[i]=left[j];left[j]=t;}
   if(calm){left.forEach(turn);return;}
   var k=0,per=Math.max(1,Math.ceil(left.length/48));
   (function step(){
    for(var i=0;i<per&&k<left.length;i++,k++)turn(left[k]);
    if(k<left.length)requestAnimationFrame(step);})();
  });
  if(bX)bX.addEventListener('click',function(){
   if(calm){light(false);return;}
   var k=0;(function step(){
    if(k<staff.length){staff[k].classList.add('is-on');k++;setTimeout(step,90);}
    else light(true);})();
  });
  // доскроллил до Момента Х, но панель не тронул: свет включаем сами
  var mx=document.getElementById('momentx');
  if(mx&&'IntersectionObserver' in window){
   var io2=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){light(false);io2.disconnect();}});},{threshold:.28});
   io2.observe(mx);
  }
  upd();
 }
 // ── шторка «замысел / что получилось» ────────────────────────────────────
 var vs=document.querySelector('[data-vs]');
 if(vs){var rg=vs.querySelector('[data-range]');
  var move=function(){vs.style.setProperty('--mz-x',rg.value+'%');};
  rg.addEventListener('input',move);move();}
 // ── план зала: список зон и точки на схеме синхронны ─────────────────────
 var zl=document.querySelector('[data-zones]');
 if(zl){
  var btns=[].slice.call(zl.querySelectorAll('[data-zone]')),
      pins=[].slice.call(document.querySelectorAll('[data-pin]'));
  function pick(k){
   btns.forEach(function(b){b.setAttribute('aria-pressed',
    String(b.getAttribute('data-zone')===k));});
   pins.forEach(function(p){p.setAttribute('aria-pressed',
    String(p.getAttribute('data-pin')===k));});
  }
  btns.forEach(function(b){b.addEventListener('click',function(){
   pick(b.getAttribute('data-zone'));});});
  pins.forEach(function(p){
   function go(){var k=p.getAttribute('data-pin');pick(k);
    var b=zl.querySelector('[data-zone="'+k+'"]');if(b)b.focus();}
   p.addEventListener('click',go);
   p.addEventListener('keydown',function(e){
    if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});});
 }
 // ── появление блоков ─────────────────────────────────────────────────────
 var els=[].slice.call(document.querySelectorAll('.mz-r'));
 function inn(nd){nd.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(nd){var r=nd.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(nd);else io.observe(nd);});
})();</script>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Мероприятие для арендаторов ТЦ «Мозаика» | кейс Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: организация мероприятия для арендаторов ТЦ «Мозаика» в Москве, 31 октября 2018, 134 гостя. Концепция «Пора выходить на свет»: зал в синем монохроме, световая панель с логотипом, которую гости собирают своими лампочками, кейтеринг, пресс-волл, полиграфия и ролик об объекте.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Мероприятие для арендаторов ТЦ «Мозаика» | кейс Hand Marketing">
<meta property="og:description" content="Концепция «Пора выходить на свет»: обновлённый знак «Мозаики» зажгли 134 гостя, каждый своей лампочкой.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/wall-lit.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/geologica-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Event","item":"https://hand-marketing.ru/event/"},'
  '{"@type":"ListItem","position":3,"name":"ТЦ «Мозаика»",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="mz">{hero()}{task()}{idea()}{path_of_guest()}'
            f'{moment_x()}{official()}{after()}{print_part()}{venue()}{program()}'
            f'{outro()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'event', 'mozaika')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
