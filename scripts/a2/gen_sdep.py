#!/usr/bin/env python3
"""Генерит mirror/creative/becar/sdep/index.html — кейс «Фирменный стиль отдела
продаж Becar» (SALESDEP): логотип, паттерн, палитра и гайдлайн на 29 полос.

Дизайн-концепция: страница говорит на языке самой айдентики. Знак и паттерн
вынуты из гайдлайна кривыми (шрифт Grifter Bold нам не принадлежит, поэтому
никакого веб-шрифта: только контуры) и живут на странице как SVG. Отсюда три
интерактива, которых не бывает на скриншотах гайдлайна:
  • знак перекрашивается в фирменные пары прямо на странице (правило гайдлайна:
    любой фирменный цвет, но SALES и DEP каждый одного цвета);
  • паттерн переключается между четырьмя режимами, стена собирается маской
    из того же контура, а цвет даёт слой под ней;
  • палитра отдаёт HEX в буфер по клику.
Дальше носители крупными планами и вся раскладка гайдлайна в лайтбоксе.

Ассеты: mirror/images/sdep/ (scripts/sdep-assets.py).

URL кейса прежний (он в sitemap, каталоге проектов и на /creativedesign).
Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import os
import re
import importlib.util
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/sdep'
URL = 'https://hand-marketing.ru/creative/becar/sdep/'

def inline_logo(name):
    """Знак кладём инлайном: только так CSS-переменные красят SALES и DEP по клику.

    Свой <style> из файла выбрасываем (внутри документа он утёк бы на всю страницу),
    классы переименовываем в sd-a/sd-b — они описаны в PAGE_CSS.
    """
    svg = open(os.path.join(ROOT, 'images', 'sdep', name + '.svg'), encoding='utf-8').read()
    svg = re.sub(r'<style>.*?</style>', '', svg, flags=re.S)
    return svg.replace('class="a"', 'class="sd-a"').replace('class="b"', 'class="sd-b"')


LOGO_SVG = inline_logo('logo')
SDEP_SVG = inline_logo('logo-sdep')

# ─── палитра гайдлайна: (hex, rgb, имя, роль) ────────────────────────────────
PALETTE = [
    ('#FF1071', '255 16 113', 'Розовый',      'Основной'),
    ('#00CADA', '0 202 218',  'Бирюзовый',    'Основной'),
    ('#601AAA', '96 26 170',  'Фиолетовый',   'Основной'),
    ('#006837', '0 104 55',   'Тёмно-зелёный','Дополнительный'),
    ('#8CC63F', '140 198 63', 'Зелёный',      'Дополнительный'),
    ('#FFFF00', '255 255 0',  'Жёлтый',       'Дополнительный'),
    ('#1B1464', '27 20 100',  'Тёмно-синий',  'Вспомогательный'),
    ('#000000', '0 0 0',      'Чёрный',       'Вспомогательный'),
    ('#DADADA', '218 218 218','Светло-серый', 'Вспомогательный'),
]

# ─── пары для перекраски знака: (SALES, DEP, фон, подпись) ───────────────────
COMBOS = [
    ('#00CADA', '#FF1071', '#1B1464', 'Основная'),
    ('#FF1071', '#00CADA', '#FFFFFF', 'На белом'),
    ('#601AAA', '#FF1071', '#FFFF00', 'На жёлтом'),
    ('#FFFFFF', '#FFFFFF', '#601AAA', 'Одним цветом'),
    ('#1B1464', '#1B1464', '#DADADA', 'Вывороткой'),
]

# ─── режимы паттерна: (ключ, подпись, пояснение) ─────────────────────────────
MODES = [
    ('grad',  'Градиент',   'Стена для обложек, пресс-волла и пакетов: слово уходит из фона в акцент.'),
    ('line',  'Контур',     'Заполняет пустоту на светлых полосах и бланках, читается как фактура бумаги.'),
    ('tone',  'Тон в тон',  'Тише всего: тот же цвет на пару шагов светлее, работает под текстом.'),
    ('flat',  'Выворотка',  'Белым по фирменному цвету, когда нужен акцентный блок целиком.'),
]

# ─── носители крупным планом: (файл, надзаголовок, заголовок, текст, alt) ────
SHOTS = [
    ('shot-social', 'Соцсети',
     'Логотип всегда в левом верхнем углу',
     'Аккаунт собирается из трёх слоёв: фон, знак, паттерн. Цвета не повторяются, поэтому '
     'даже случайный набор постов держится вместе. Текст всегда ложится на плашку, иначе он '
     'тонет в фотографии.',
     'Оформление аккаунта SALESDEP: обложка Facebook и лента Instagram с фирменным паттерном'),
    ('shot-stickers', 'Стикеры',
     '«Этеншен», «Не балуй», «Горим»',
     'Отдел продаж живёт в чатах, поэтому в стиль вошёл стикерпак. Схема сборки простая: '
     'круг фирменного цвета, вырезанная с фона картинка и плашка с репликой под наклоном '
     'в 10 градусов. По этой схеме новый стикер собирают за пару минут.',
     'Стикерпак SALESDEP в Telegram: реплики на плашках фирменных цветов'),
    ('shot-business', 'Деловые материалы',
     'Папка, конверт, визитка, бейдж',
     'Комплект, который клиент видит на сделке. Визитка держит два фирменных цвета встык, '
     'бейдж и папка уходят в тёмно-синий с паттерном, стикер с адресом закрывает конверт.',
     'Деловые материалы SALESDEP: папка для договоров, бейджи, визитка и конверт'),
    ('shot-expo', 'Выставки',
     'Стенд, который читается с двадцати метров',
     'На выставке от стиля остаётся только градиентная стена и знак: этого достаточно, чтобы '
     'стенд нашли в толпе. Ролл-ап и карта участника собраны из тех же элементов, что и посты '
     'в ленте.',
     'Выставочный комплект SALESDEP: пресс-волл, ролл-ап, pop-up и мобильный стенд'),
    ('shot-office', 'Офис',
     'Стиль на стенах, а не только в файлах',
     'Крупноформатная запечатка стен, паттерн в переговорной и жёлтая лента «зона повышенной '
     'ответственности» на кухне. Отдел продаж работает внутри своего стиля, а не открывает его '
     'в презентации раз в квартал.',
     'Оформление офиса отдела продаж: паттерн на стенах переговорной и лента SDEP на кухне'),
    ('shot-gifts', 'Сувенирка',
     'Стакан, блокнот, зонт, кружка, чехол',
     'Мелочи собраны на одном приёме: фирменный цвет плюс паттерн, знак сверху. Подрядчику '
     'уходит готовый макет, согласовывать нечего.',
     'Сувенирная продукция SALESDEP: стакан, блокнот, зонт, кружка и чехол на телефон'),
    ('shot-fc', 'Футбольный клуб',
     'Флаг, форма и мяч',
     'У отдела продаж есть своя команда, и ей тоже нужен комплект. Тот же тёмно-синий, тот же '
     'паттерн, знак на груди.',
     'Атрибутика футбольного клуба SALESDEP: флаг, форма и мяч'),
]

# ─── полосы гайдлайна для галереи: (файл, заголовок, подпись) ────────────────
SLIDES = [
    ('logo', 'Логотип',
     'Основная и сокращённая версии, область безопасности и запрет на искажения.'),
    ('colors', 'Цвета',
     'Девять цветов, разбитых на основные, дополнительные и вспомогательные, плюс готовые схемы сочетаний.'),
    ('type', 'Шрифт',
     'Gotham: Bold для заголовков, Light для дополнительного текста.'),
    ('pattern', 'Паттерн',
     'Четыре варианта, от тихого фонового до агрессивного для соцсетей и брендирования.'),
    ('infographic', 'Инфографика',
     'Цвета в графиках берутся по приоритету. Если типов данных больше трёх, последним идёт светло-серый.'),
    ('deck-cover', 'Обложка презентации',
     'Два варианта: для презентаций с большим объёмом данных и для имиджевых.'),
    ('deck-body', 'Тело презентации',
     'Сетка слайдов: с картинкой, с делением на цветные блоки, с графиком.'),
    ('social-rules', 'Соцсети: правила',
     'Логотип в левом верхнем углу, дополнительный текст на плашке, паттерн выравнивает композицию.'),
    ('social-avatar', 'Аватар и обложка',
     'Фон, знак и паттерн разными цветами: повторяться нельзя.'),
    ('instagram', 'Инстаграм',
     'Три типа постов: полезные, вовлекающие и продающие.'),
    ('facebook', 'Фейсбук',
     'Обложка сообщества и посты в ленте.'),
    ('stickers', 'Стикеры: схема',
     'Круг, плашки под 10 градусов против часовой стрелки и картинки, вырезанные с фона.'),
    ('stickers-tg', 'Стикеры: пак',
     'Готовый набор реплик для рабочих чатов.'),
    ('office-1', 'Офис: стены',
     'Крупноформатная запечатка с логотипом, паттерном и текстом.'),
    ('office-2', 'Офис: кухня и переговорная',
     'Паттерн в переговорной и лента «зона повышенной ответственности» на кухне.'),
    ('docs', 'Бланки',
     'Благодарственное письмо и договор: паттерн уходит в правое поле листа.'),
    ('business', 'Деловые материалы: макеты',
     'Папка А4, евроконверт, визитка, стикер с адресом и бейдж.'),
    ('business-3d', 'Деловые материалы: визуализация',
     'Тот же комплект в предметной съёмке для типографии.'),
    ('expo', 'Выставки: макеты',
     'Ролл-ап, пресс-волл, пакеты и карта участника.'),
    ('expo-3d', 'Выставки: визуализация',
     'Pop-up, мобильный стенд и стойка ресепшена.'),
    ('fc', 'Футбольный клуб: макеты',
     'Флаг, футболка и мяч.'),
    ('fc-3d', 'Футбольный клуб: визуализация',
     'Комплект команды в предметной съёмке.'),
    ('gifts', 'Сувенирка: макеты',
     'Пластиковый стакан, блокнот, зонт, кружка и чехол на телефон.'),
    ('gifts-3d', 'Сувенирка: визуализация',
     'Сувенирка в предметной съёмке.'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 5l-7 7 7 7"/></svg>')

PAGE_CSS = """<style id="sd-css">
:root{
 --sd-pink:#FF1071;--sd-cyan:#00CADA;--sd-violet:#601AAA;--sd-navy:#1B1464;
 --sd-green:#8CC63F;--sd-dgreen:#006837;--sd-yellow:#FFFF00;--sd-grey:#DADADA;
 --sd-ink:#10111a;--sd-ink2:#585c6b;
 --sd-df:'Montserrat',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --sd-bf:'Onest',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --sd-tile:751px 115px}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.sd{font-family:var(--sd-bf);color:var(--sd-ink);background:#fff;line-height:1.62;
 font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.sd *{box-sizing:border-box}
.sd img{max-width:100%;height:auto;display:block}
.sd a{color:inherit}
.sd h1,.sd h2,.sd h3{font-family:var(--sd-df);font-weight:800;line-height:1.03;
 letter-spacing:-.03em;margin:0;text-wrap:balance}
.sd p{text-wrap:pretty}
.sd-w{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,52px)}
/* блоки знака: цвет каждого задаётся переменной на родителе */
.sd svg .sd-a{fill:var(--sd-a,#00CADA)}
.sd svg .sd-b{fill:var(--sd-b,#FF1071)}
.sd-kick{font-family:var(--sd-df);font-weight:700;font-size:12.5px;letter-spacing:.16em;
 text-transform:uppercase;display:inline-flex;align-items:center;gap:10px}
.sd-kick::before{content:"";width:22px;height:4px;background:currentColor}
.sd-btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--sd-df);
 font-weight:800;font-size:15px;padding:.95em 1.5em;border:0;cursor:pointer;
 text-decoration:none;transition:transform .25s,background .25s,color .25s,border-color .25s}
.sd-btn svg{width:1.1em;height:1.1em}
.sd-btn--p{background:var(--sd-pink);color:#fff}
.sd-btn--p:hover{transform:translateY(-2px);background:#fff;color:var(--sd-violet)}
.sd-btn--gh{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.4)}
.sd-btn--gh:hover{border-color:#fff;transform:translateY(-2px)}

/* ── ПАТТЕРН ──
   Тайл (реальные кривые знака) работает маской, цвет даёт слой под ней: так одна
   картинка закрывает и градиентную стену, и контур на белом. Если маски нет,
   @supports ниже возвращает обычный фон. */
.sd-pat{position:absolute;inset:0;pointer-events:none;
 -webkit-mask-image:url(/images/sdep/pattern-solid.svg);mask-image:url(/images/sdep/pattern-solid.svg);
 -webkit-mask-size:var(--sd-tile);mask-size:var(--sd-tile);
 -webkit-mask-repeat:repeat;mask-repeat:repeat}
.sd-pat--line{-webkit-mask-image:url(/images/sdep/pattern-line.svg);mask-image:url(/images/sdep/pattern-line.svg)}
@supports not ((-webkit-mask-image:url(#a)) or (mask-image:url(#a))){
 .sd-pat{background:none!important;opacity:.16;
  background-image:url(/images/sdep/pattern-solid.svg)!important;background-size:var(--sd-tile)}
}
@keyframes sd-drift{to{-webkit-mask-position:-751px 0;mask-position:-751px 0}}

/* ── HERO ── */
.sd-hero{position:relative;background:var(--sd-violet);color:#fff;overflow:hidden;isolation:isolate}
.sd-hero .sd-pat{background:linear-gradient(178deg,rgba(255,255,255,.14) 0%,rgba(255,255,255,.1) 34%,
 var(--sd-pink) 100%);animation:sd-drift 34s linear infinite;z-index:0}
.sd-hero__in{position:relative;z-index:2;padding-top:clamp(40px,6vw,84px);
 padding-bottom:clamp(46px,6vw,74px)}
.sd-hero__logo{width:min(760px,86%);display:block}
.sd-hero__logo svg{width:100%;height:auto;display:block;filter:drop-shadow(0 26px 60px rgba(0,0,0,.28))}
.sd-hero__rule{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
 flex-wrap:wrap;margin:clamp(14px,2vw,20px) 0 clamp(30px,5vw,58px);
 font-size:clamp(13px,1.35vw,16px);color:rgba(255,255,255,.82);
 border-top:2px solid rgba(255,255,255,.28);padding-top:14px}
/* правило гайдлайна: текст поверх паттерна кладут на плашку, иначе он тонет */
.sd-hero__plate{background:rgba(43,8,86,.62);padding:clamp(22px,3vw,34px) clamp(20px,3vw,36px);
 max-width:min(760px,100%)}
.sd-hero h1{font-size:clamp(31px,4.6vw,58px);max-width:19ch}
.sd-hero__sub{margin:clamp(16px,2vw,24px) 0 0;font-size:clamp(16px,1.4vw,19px);
 color:rgba(255,255,255,.84);max-width:56ch}
.sd-chips{display:flex;flex-wrap:wrap;gap:8px;margin:clamp(22px,2.6vw,30px) 0 0;padding:0;list-style:none}
.sd-chips li{padding:7px 14px;border:2px solid rgba(255,255,255,.3);font-size:12.5px;
 font-weight:600;color:rgba(255,255,255,.92)}
.sd-hero__cta{margin-top:clamp(24px,3vw,34px);display:flex;gap:12px;flex-wrap:wrap}
.sd-spec{position:relative;z-index:2;background:var(--sd-navy);color:#fff}
.sd-spec__in{max-width:1240px;margin:0 auto;padding:22px clamp(20px,4vw,52px);
 display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.sd-spec div{padding-left:15px;border-left:4px solid var(--sd-cyan)}
.sd-spec div:nth-child(2){border-color:var(--sd-pink)}
.sd-spec div:nth-child(3){border-color:var(--sd-yellow)}
.sd-spec div:nth-child(4){border-color:var(--sd-green)}
.sd-spec dt{font-family:var(--sd-df);font-weight:800;font-size:clamp(20px,2vw,26px);letter-spacing:-.02em}
.sd-spec dd{margin:3px 0 0;font-size:12.5px;color:rgba(255,255,255,.62);line-height:1.4}

/* ── ЗАДАЧА ── */
.sd-task{padding:clamp(58px,7.5vw,104px) 0}
.sd-task .sd-kick{color:var(--sd-pink)}
.sd-task__grid{display:grid;grid-template-columns:1.06fr .94fr;gap:clamp(28px,5vw,66px);align-items:start}
.sd-task h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px}
.sd-task p{margin:20px 0 0;font-size:clamp(15.5px,1.3vw,17.5px);color:#33374a;max-width:60ch}
.sd-task b{font-weight:700;color:var(--sd-ink)}
.sd-task__side{border-left:4px solid var(--sd-cyan);padding-left:clamp(18px,2.4vw,28px)}
.sd-task__side h3{font-size:clamp(18px,1.8vw,22px);margin-bottom:10px}
.sd-task__side p{margin-top:12px;font-size:15.5px}
/* селектор с .sd-task: иначе размер перебьёт .sd-task p */
.sd-task .sd-quote{margin:clamp(34px,4.5vw,54px) 0 0;max-width:26ch;padding:clamp(24px,3.4vw,40px);background:var(--sd-yellow);
 font-family:var(--sd-df);font-weight:800;font-size:clamp(19px,2.4vw,30px);line-height:1.22;
 letter-spacing:-.02em;color:var(--sd-navy);max-width:24ch}

/* ── ЗНАК ── */
.sd-logo{background:var(--sd-navy);color:#fff;padding:clamp(58px,7.5vw,104px) 0;position:relative;overflow:hidden}
.sd-logo>.sd-pat{background:rgba(255,255,255,.055);z-index:0}
.sd-logo .sd-w{position:relative;z-index:1}
.sd-logo .sd-kick{color:var(--sd-cyan)}
.sd-logo h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:18ch}
.sd-logo__lede{margin:18px 0 0;max-width:58ch;color:rgba(255,255,255,.78);font-size:clamp(15.5px,1.3vw,17.5px)}
.sd-stage{margin-top:clamp(30px,4vw,46px);background:var(--sd-navy);border:2px solid rgba(255,255,255,.16);
 padding:clamp(34px,6vw,80px) clamp(20px,4vw,56px);display:flex;align-items:center;justify-content:center;
 transition:background .45s}
.sd-stage svg{width:min(700px,100%);height:auto;transition:opacity .3s}
.sd-stage--sm{margin-top:14px;padding:clamp(24px,3.4vw,44px)}
.sd-stage--sm svg{width:min(300px,62%)}
.sd-swap{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.sd-swap button{display:inline-flex;align-items:center;gap:9px;cursor:pointer;
 background:transparent;border:2px solid rgba(255,255,255,.22);color:#fff;padding:9px 15px 9px 11px;
 font:600 13px var(--sd-bf);transition:border-color .2s,background .2s}
.sd-swap button:hover{border-color:rgba(255,255,255,.55)}
.sd-swap button[aria-pressed=true]{border-color:#fff;background:rgba(255,255,255,.1)}
.sd-swap i{display:flex;width:34px;height:18px;border:1px solid rgba(255,255,255,.3)}
.sd-swap i b{flex:1}
.sd-rules{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2.4vw,28px);
 margin-top:clamp(30px,4vw,48px)}
.sd-rules div{border-top:4px solid var(--sd-pink);padding-top:14px}
.sd-rules div:nth-child(2){border-color:var(--sd-cyan)}
.sd-rules div:nth-child(3){border-color:var(--sd-yellow)}
.sd-rules h3{font-size:16px;letter-spacing:-.01em}
.sd-rules p{margin:8px 0 0;font-size:14.5px;color:rgba(255,255,255,.7);line-height:1.55}
.sd-short{display:grid;grid-template-columns:1fr 1fr;gap:clamp(20px,3vw,40px);
 margin-top:clamp(30px,4vw,48px);align-items:center}
.sd-short h3{font-size:clamp(19px,2vw,25px)}
.sd-short p{margin:12px 0 0;color:rgba(255,255,255,.74);font-size:15.5px;max-width:44ch}

/* ── ПАЛИТРА ── */
.sd-pal{padding:clamp(58px,7.5vw,104px) 0}
.sd-pal .sd-kick{color:var(--sd-violet)}
.sd-pal h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:20ch}
.sd-pal__lede{margin:18px 0 0;max-width:60ch;color:#33374a;font-size:clamp(15.5px,1.3vw,17.5px)}
.sd-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(12px,1.6vw,20px);
 margin-top:clamp(28px,3.6vw,44px)}
.sd-sw{position:relative;border:0;padding:0;cursor:pointer;text-align:left;font:inherit;color:inherit;
 background:#fff;box-shadow:0 0 0 1px rgba(16,17,26,.1);transition:transform .2s,box-shadow .2s}
.sd-sw:hover{transform:translateY(-3px);box-shadow:0 14px 28px -14px rgba(16,17,26,.5)}
.sd-sw span{display:block;height:clamp(78px,9vw,116px)}
.sd-sw div{padding:12px 14px 14px}
.sd-sw b{display:block;font-family:var(--sd-df);font-weight:800;font-size:15px;letter-spacing:.01em}
.sd-sw small{display:block;margin-top:3px;font-size:12.5px;color:var(--sd-ink2)}
.sd-sw em{display:block;font-style:normal;font-size:10.5px;font-weight:700;letter-spacing:.1em;
 text-transform:uppercase;color:var(--sd-ink2);margin-bottom:5px}
.sd-sw .sd-copied{position:absolute;left:14px;top:12px;background:#fff;color:var(--sd-ink);
 font:700 11px var(--sd-bf);padding:4px 8px;opacity:0;transition:opacity .2s}
.sd-sw.is-copied .sd-copied{opacity:1}
.sd-prop{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(12px,1.6vw,20px);
 margin-top:clamp(24px,3vw,36px)}
.sd-prop__b{aspect-ratio:1/.72;display:grid;gap:4px}
.sd-prop__b i{display:block}
.sd-prop p{margin:10px 0 0;font-size:13.5px;color:var(--sd-ink2);line-height:1.5}
.sd-p1{grid-template-rows:1.6fr .5fr 1fr;background:var(--sd-pink)}
.sd-p1 i:nth-child(1){background:var(--sd-pink)}
.sd-p1 i:nth-child(2){background:var(--sd-green)}
.sd-p1 i:nth-child(3){background:var(--sd-cyan)}
.sd-p2{grid-template-columns:1fr 1fr;grid-template-rows:1.5fr 1fr}
.sd-p2 i:nth-child(1){background:var(--sd-cyan)}
.sd-p2 i:nth-child(2){background:var(--sd-violet)}
.sd-p2 i:nth-child(3){background:var(--sd-pink)}
.sd-p2 i:nth-child(4){background:var(--sd-cyan)}
.sd-p3{grid-template-columns:.5fr 1.6fr;grid-template-rows:1fr 1fr}
.sd-p3 i:nth-child(1){background:var(--sd-violet);grid-row:span 2}
.sd-p3 i:nth-child(2){background:var(--sd-pink)}
.sd-p3 i:nth-child(3){background:var(--sd-cyan)}

/* ── ПАТТЕРН-ЛАБОРАТОРИЯ ── */
.sd-lab{background:var(--sd-cyan);color:var(--sd-navy);padding:clamp(58px,7.5vw,104px) 0}
.sd-lab .sd-kick{color:var(--sd-navy)}
.sd-lab h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:18ch}
.sd-lab__lede{margin:18px 0 0;max-width:58ch;font-size:clamp(15.5px,1.3vw,17.5px);color:rgba(11,17,60,.78)}
.sd-lab__box{margin-top:clamp(28px,3.6vw,44px);position:relative;aspect-ratio:16/7;overflow:hidden;
 background:var(--sd-violet);transition:background .4s}
.sd-lab__box .sd-pat{animation:sd-drift 34s linear infinite}
.sd-lab__box[data-mode=grad]{background:var(--sd-navy)}
.sd-lab__box[data-mode=grad] .sd-pat{background:linear-gradient(160deg,var(--sd-violet) 8%,var(--sd-pink) 92%)}
.sd-lab__box[data-mode=line]{background:#fff}
.sd-lab__box[data-mode=line] .sd-pat{background:var(--sd-navy)}
.sd-lab__box[data-mode=tone]{background:var(--sd-violet)}
.sd-lab__box[data-mode=tone] .sd-pat{background:rgba(255,255,255,.14)}
.sd-lab__box[data-mode=flat]{background:var(--sd-pink)}
.sd-lab__box[data-mode=flat] .sd-pat{background:#fff}
.sd-modes{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.sd-modes button{cursor:pointer;background:transparent;border:2px solid rgba(11,17,60,.25);
 color:var(--sd-navy);padding:10px 17px;font:800 13.5px var(--sd-df);letter-spacing:.01em;
 transition:background .2s,border-color .2s,color .2s}
.sd-modes button:hover{border-color:var(--sd-navy)}
.sd-modes button[aria-pressed=true]{background:var(--sd-navy);border-color:var(--sd-navy);color:#fff}
.sd-lab__note{margin:14px 0 0;font-size:14.5px;color:rgba(11,17,60,.8);min-height:3em;max-width:58ch}
.sd-lab__foot{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2.4vw,28px);
 margin-top:clamp(30px,4vw,46px)}
.sd-lab__foot div{border-top:4px solid var(--sd-navy);padding-top:14px}
.sd-lab__foot h3{font-size:16px}
.sd-lab__foot p{margin:8px 0 0;font-size:14.5px;color:rgba(11,17,60,.78);line-height:1.55}

/* ── НОСИТЕЛИ ── */
.sd-media{padding:clamp(58px,7.5vw,104px) 0 clamp(20px,3vw,34px)}
.sd-media .sd-kick{color:var(--sd-pink)}
.sd-media h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:20ch}
.sd-media__lede{margin:18px 0 0;max-width:60ch;color:#33374a;font-size:clamp(15.5px,1.3vw,17.5px)}
.sd-shot{display:grid;grid-template-columns:.86fr 1.14fr;gap:clamp(24px,4vw,58px);
 align-items:center;padding:clamp(34px,5vw,68px) 0;border-bottom:1px solid rgba(16,17,26,.1)}
.sd-shot:nth-child(even){grid-template-columns:1.14fr .86fr}
.sd-shot:nth-child(even) .sd-shot__t{order:2}
.sd-shot__n{font-family:var(--sd-df);font-weight:800;font-size:12.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--sd-violet)}
.sd-shot h3{font-size:clamp(21px,2.4vw,31px);margin-top:10px;max-width:17ch}
.sd-shot p{margin:14px 0 0;font-size:16px;color:#33374a;max-width:46ch}
.sd-shot img{box-shadow:0 30px 60px -34px rgba(16,17,26,.6)}

/* ── ГАЙДЛАЙН ── */
.sd-book{background:var(--sd-ink);color:#fff;padding:clamp(58px,7.5vw,104px) 0}
.sd-book .sd-kick{color:var(--sd-yellow)}
.sd-book h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px;max-width:18ch}
.sd-book__lede{margin:18px 0 0;max-width:58ch;color:rgba(255,255,255,.72);font-size:clamp(15.5px,1.3vw,17.5px)}
.sd-book__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(10px,1.4vw,18px);
 margin-top:clamp(28px,3.6vw,44px);padding:0;list-style:none}
.sd-book__grid button{display:block;width:100%;padding:0;border:0;background:transparent;cursor:pointer;
 text-align:left;color:inherit;font:inherit}
.sd-book__grid img{width:100%;aspect-ratio:16/9;object-fit:cover;background:#22232e;
 transition:transform .3s,opacity .3s}
.sd-book__grid button:hover img,.sd-book__grid button:focus-visible img{transform:scale(1.03);opacity:.85}
.sd-book__grid span{display:block;margin-top:9px;font-size:13px;font-weight:600;color:rgba(255,255,255,.82)}
.sd-book__hint{margin-top:22px;font-size:13.5px;color:rgba(255,255,255,.5)}

/* лайтбокс */
.sd-lb{position:fixed;inset:0;z-index:1200;background:rgba(9,10,16,.94);display:none;
 align-items:center;justify-content:center;padding:clamp(16px,4vw,52px)}
.sd-lb.is-open{display:flex}
.sd-lb__box{position:relative;width:min(1400px,100%)}
.sd-lb img{width:100%;height:auto;max-height:76vh;object-fit:contain}
.sd-lb__cap{margin-top:14px;color:rgba(255,255,255,.82);font-size:14.5px;display:flex;gap:14px;
 flex-wrap:wrap;align-items:baseline}
.sd-lb__cap b{font-family:var(--sd-df);font-weight:800;color:#fff;font-size:16px}
.sd-lb__x,.sd-lb__nav{position:absolute;border:0;cursor:pointer;background:rgba(255,255,255,.12);
 color:#fff;width:48px;height:48px;display:flex;align-items:center;justify-content:center;
 transition:background .2s}
.sd-lb__x:hover,.sd-lb__nav:hover{background:rgba(255,255,255,.3)}
.sd-lb__x{top:-58px;right:0;font-size:26px;line-height:1}
.sd-lb__nav{top:calc(38vh - 24px)}
.sd-lb__nav svg{width:22px;height:22px}
.sd-lb__nav--p{left:-58px}
.sd-lb__nav--n{right:-58px;transform:scaleX(-1)}

/* ── РЕЗУЛЬТАТ ── */
.sd-res{padding:clamp(58px,7.5vw,104px) 0}
.sd-res .sd-kick{color:var(--sd-pink)}
.sd-res__grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(28px,5vw,66px);align-items:start}
.sd-res h2{font-size:clamp(26px,3.3vw,42px);margin-top:14px}
.sd-res__more{margin:20px 0 0;font-size:16px;color:#33374a}
.sd-res__more a{color:var(--sd-violet);font-weight:700}
.sd-res__list{list-style:none;margin:0;padding:0;display:grid;gap:clamp(14px,2vw,22px)}
.sd-res__list li{display:grid;grid-template-columns:auto 1fr;gap:clamp(14px,2vw,22px);
 align-items:start;border-top:1px solid rgba(16,17,26,.14);padding-top:clamp(14px,2vw,20px)}
.sd-num{font-family:var(--sd-df);font-weight:800;font-variant-numeric:tabular-nums;
 font-size:clamp(28px,3.6vw,44px);line-height:1;letter-spacing:-.04em;color:var(--sd-pink);min-width:2.2ch}
.sd-res__list li:nth-child(2) .sd-num{color:var(--sd-cyan)}
.sd-res__list li:nth-child(3) .sd-num{color:var(--sd-violet)}
.sd-res__list li:nth-child(4) .sd-num{color:var(--sd-navy)}
.sd-res__list span:last-child{font-size:15.5px;color:#33374a}
.sd-res__list b{color:var(--sd-ink)}

/* появление */
html.no-js .sd-r{opacity:1!important;transform:none!important}
.sd-r{opacity:0;transform:translateY(22px);
 transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.sd-r.is-in{opacity:1;transform:none}

/* ── АДАПТИВ ── */
@media(max-width:1020px){
 .sd-task__grid,.sd-res__grid,.sd-short,.sd-shot,.sd-shot:nth-child(even){grid-template-columns:1fr;gap:26px}
 .sd-shot:nth-child(even) .sd-shot__t{order:0}
 .sd-spec__in{grid-template-columns:repeat(2,1fr)}
 .sd-book__grid{grid-template-columns:repeat(3,1fr)}
 .sd-lb__nav--p{left:0}.sd-lb__nav--n{right:0}
 .sd-lb__nav{top:auto;bottom:-58px}
}
@media(max-width:680px){
 .sd{font-size:16px}
 :root{--sd-tile:420px 64px}
 .sd-grid,.sd-rules,.sd-lab__foot{grid-template-columns:repeat(2,1fr)}
 .sd-prop{grid-template-columns:1fr}
 .sd-book__grid{grid-template-columns:repeat(2,1fr)}
 .sd-lab__box{aspect-ratio:4/3}
 .sd-quote{max-width:none}
}
@media(max-width:420px){
 .sd-spec__in{grid-template-columns:1fr}
 .sd-grid{grid-template-columns:1fr 1fr}
 .sd-rules{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){
 .sd-r{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .sd *{transition-duration:.01ms!important;scroll-behavior:auto}
 .sd-pat{animation:none!important}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Фирменный стиль отдела продаж Becar: логотип SALESDEP, паттерн и гайдлайн | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: айдентика SALESDEP для отдела продаж Becar Asset Management. Логотип из двух блоков, паттерн из повторяющегося слова, палитра из 9 цветов и гайдлайн на 29 полос с готовыми макетами: презентации, соцсети, стикеры, деловые материалы, выставки, сувенирка.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Фирменный стиль отдела продаж Becar (SALESDEP) | кейс Hand Marketing">
<meta property="og:description" content="Логотип, паттерн, палитра из 9 цветов и гайдлайн на 29 полос: стиль, которым отдел продаж пользуется без дизайнера.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/slide-logo.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def hero():
    chips = ''.join(f'<li>{c}</li>' for c in (
        'Логотип', 'Паттерн', 'Палитра', 'Гайдлайн', 'Носители', 'Стикерпак'))
    spec = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in (
        ('2020', 'год разработки'),
        ('29', 'полос гайдлайна'),
        ('9', 'фирменных цветов'),
        ('40+', 'готовых макетов'),
    ))
    return (
      '<header class="sd-hero">'
      '<div class="sd-pat" aria-hidden="true"></div>'
      '<div class="sd-w sd-hero__in">'
      f'<div class="sd-hero__logo">{LOGO_SVG}</div>'
      '<div class="sd-hero__rule"><span>Becar Asset Management, отдел продаж</span>'
      '<span>Фирменный стиль и гайдлайн, 2020</span></div>'
      '<div class="sd-hero__plate">'
      '<h1>Стиль, которым пользуются без дизайнера</h1>'
      '<p class="sd-hero__sub">Отделу продаж Becar нужна была собственная айдентика, '
      'а собирать по ней макеты предстояло менеджерам. Поэтому знак, паттерн и палитру '
      'мы свели к нескольким правилам, которые держатся в голове.</p>'
      f'<ul class="sd-chips">{chips}</ul>'
      '<div class="sd-hero__cta">'
      f'<a class="sd-btn sd-btn--p" href="#sd-book">Открыть гайдлайн {ARROW}</a>'
      '<a class="sd-btn sd-btn--gh" href="#lead">Обсудить проект</a>'
      '</div></div></div>'
      f'<div class="sd-spec"><div class="sd-spec__in">{spec}</div></div>'
      '</header>')


def task():
    return (
      '<section class="sd-task"><div class="sd-w">'
      '<div class="sd-task__grid">'
      '<div class="sd-r"><span class="sd-kick">Задача</span>'
      '<h2>Фирменный стиль для отдела внутри большой компании</h2>'
      '<p>Becar Asset Management работает на рынке недвижимости с 1992 года: Россия, США, '
      'Европа, страны СНГ и Ближний Восток. У группы есть свой корпоративный стиль, но отделу '
      'продаж он был велик: продавцам нужен был <b>отдельный голос</b>, узнаваемый на выставке, '
      'в ленте соцсетей и в рабочем чате.</p>'
      '<p>Мы погрузились в то, как отдел живёт день за днём, и увидели главное ограничение. '
      'Макеты будут собирать не дизайнеры, а менеджеры, между звонками, в PowerPoint. '
      'Стиль, который требует дизайнера на каждый пост, здесь просто не заработает.</p>'
      '</div>'
      '<div class="sd-task__side sd-r"><h3>Что сделали</h3>'
      '<p>Название SALESDEP и знак из двух блоков, которые можно красить в любые '
      'фирменные цвета.</p>'
      '<p>Паттерн из того же слова: он собирается повтором и закрывает пустоту в любом макете.</p>'
      '<p>Палитру из девяти цветов с приоритетами и готовыми схемами сочетаний.</p>'
      '<p>Гайдлайн на 29 полос, где для каждого носителя есть и правило, и готовый макет.</p>'
      '</div></div>'
      '<p class="sd-quote sd-r">Правило одно: сохранять единый цвет для каждого блока, '
      'SALES и DEP.</p>'
      '</div></section>')


def logo():
    swaps = ''.join(
      f'<button type="button" data-a="{a}" data-b="{b}" data-bg="{bg}" aria-pressed="false">'
      f'<i aria-hidden="true"><b style="background:{a}"></b><b style="background:{b}"></b></i>'
      f'{H.escape(cap)}</button>' for a, b, bg, cap in COMBOS)
    rules = ''.join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in (
      ('Любой фирменный цвет',
       'Знак живёт в бирюзовом, розовом, фиолетовом, белом. Ограничение одно: внутри блока '
       'SALES один цвет, внутри DEP другой или тот же.'),
      ('Область безопасности',
       'Вокруг знака остаётся поле в высоту буквы S. Внутрь этого поля не заходит ни текст, '
       'ни картинка, ни край макета.'),
      ('Искажения запрещены',
       'Знак не растягивают, не наклоняют и не обводят. Это единственный жёсткий запрет '
       'в гайдлайне.'),
    ))
    return (
      '<section class="sd-logo" id="sd-logo">'
      '<div class="sd-pat" aria-hidden="true"></div>'
      '<div class="sd-w">'
      '<div class="sd-r"><span class="sd-kick">Знак</span>'
      '<h2>Два блока, которые красятся под ситуацию</h2>'
      '<p class="sd-logo__lede">Логотип собран из двух слов, набранных Grifter Bold встык. '
      'Цвет блока меняется под носитель, поэтому знак не спорит ни с фотографией, ни с '
      'плашкой, ни с фоном стенда. Нажмите на пару, чтобы посмотреть.</p></div>'
      f'<div class="sd-stage sd-r" id="sd-stage">{LOGO_SVG}</div>'
      f'<div class="sd-swap sd-r" id="sd-swap" role="group" aria-label="Цветовые пары знака">{swaps}</div>'
      '<div class="sd-short sd-r">'
      '<div><h3>Сокращённая версия</h3>'
      '<p>Там, где полное написание не читается, знак ужимается до SDEP: аватар в соцсетях, '
      'лента на кухне, стикер, бейдж. Логика цвета остаётся прежней.</p></div>'
      f'<div class="sd-stage sd-stage--sm" id="sd-stage2">{SDEP_SVG}</div>'
      '</div>'
      f'<div class="sd-rules sd-r">{rules}</div>'
      '</div></section>')


def palette():
    sws = ''.join(
      f'<button class="sd-sw" type="button" data-hex="{hexv}">'
      f'<span style="background:{hexv}"></span>'
      f'<div><em>{H.escape(role)}</em><b>{H.escape(name)}</b><small>{hexv} · {rgb}</small></div>'
      '<span class="sd-copied">Скопировано</span></button>'
      for hexv, rgb, name, role in PALETTE)
    return (
      '<section class="sd-pal"><div class="sd-w">'
      '<div class="sd-r"><span class="sd-kick">Палитра</span>'
      '<h2>Девять цветов и правило пропорций</h2>'
      '<p class="sd-pal__lede">Основные три цвета держат узнаваемость, дополнительные заходят '
      'малыми пятнами, вспомогательные отвечают за текст и паузу. Главное правило гайдлайна: '
      'не мешать цвета в равных долях, иначе макет разваливается. Нажмите на плашку, чтобы '
      'скопировать HEX.</p></div>'
      f'<div class="sd-grid sd-r">{sws}</div>'
      '<div class="sd-prop sd-r">'
      '<div><div class="sd-prop__b sd-p1"><i></i><i></i><i></i></div>'
      '<p>Один цвет ведёт, второй поддерживает, третий заходит полосой.</p></div>'
      '<div><div class="sd-prop__b sd-p2"><i></i><i></i><i></i><i></i></div>'
      '<p>Деление на блоки, когда на одном макете живёт разная информация.</p></div>'
      '<div><div class="sd-prop__b sd-p3"><i></i><i></i><i></i></div>'
      '<p>Узкая вертикаль третьего цвета вместо равной трети.</p></div>'
      '</div></div></section>')


def lab():
    btns = ''.join(
      f'<button type="button" data-mode="{k}" data-note="{H.escape(note)}" '
      f'aria-pressed="{"true" if i == 0 else "false"}">{H.escape(cap)}</button>'
      for i, (k, cap, note) in enumerate(MODES))
    foot = ''.join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in (
      ('Собирается повтором',
       'Паттерн не рисуют заново: слово ставят встык и множат. Это можно сделать в PowerPoint '
       'и в любом редакторе, который есть у менеджера.'),
      ('Закрывает пустоту',
       'Если текста мало, а поле большое, паттерн выравнивает композицию вместо случайной '
       'картинки из стока.'),
      ('Работает и на скотче',
       'Из сокращённой версии складывается агрессивная лента для брендирования офиса и '
       'сторис: чёрно-жёлтая полоса с SDEP под наклоном.'),
    ))
    return (
      '<section class="sd-lab"><div class="sd-w">'
      '<div class="sd-r"><span class="sd-kick">Паттерн</span>'
      '<h2>Само название и есть фактура</h2>'
      '<p class="sd-lab__lede">Второй обязательный элемент айдентики сделан из первого. '
      'Слово повторяется рядами и меняет только режим: от градиентной стены до тихого контура. '
      'Ниже настоящие контуры знака, а не картинка из гайдлайна.</p></div>'
      '<div class="sd-lab__box sd-r" id="sd-lab" data-mode="grad">'
      '<div class="sd-pat" aria-hidden="true"></div></div>'
      f'<div class="sd-modes sd-r" id="sd-modes" role="group" aria-label="Режимы паттерна">{btns}</div>'
      f'<p class="sd-lab__note" id="sd-note">{H.escape(MODES[0][2])}</p>'
      f'<div class="sd-lab__foot sd-r">{foot}</div>'
      '</div></section>')


def media():
    shots = ''
    for f, kick, title, text, alt in SHOTS:
        shots += (
          '<article class="sd-shot sd-r">'
          f'<div class="sd-shot__t"><span class="sd-shot__n">{H.escape(kick)}</span>'
          f'<h3>{H.escape(title)}</h3><p>{text}</p></div>'
          f'<div><img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" loading="lazy" '
          'width="1700" height="1391"></div></article>')
    return (
      '<section class="sd-media"><div class="sd-w">'
      '<div class="sd-r"><span class="sd-kick">Носители</span>'
      '<h2>От аватара в соцсетях до мяча футбольной команды</h2>'
      '<p class="sd-media__lede">Стиль проверяется на носителях, поэтому в гайдлайн вошли не '
      'рекомендации, а собранные макеты. Менеджеру остаётся поменять текст, подрядчику '
      'отправить файл в печать.</p></div>'
      f'{shots}</div></section>')


def book():
    cards = ''
    for i, (f, title, cap) in enumerate(SLIDES):
        cards += (
          f'<li><button type="button" data-i="{i}" data-src="{IMG}/slide-{f}.jpg" '
          f'data-title="{H.escape(title)}" data-cap="{H.escape(cap)}">'
          f'<img src="{IMG}/thumb-{f}.jpg" alt="Полоса гайдлайна SALESDEP: {H.escape(title.lower())}" '
          'loading="lazy" width="300" height="169">'
          f'<span>{H.escape(title)}</span></button></li>')
    return (
      '<section class="sd-book" id="sd-book"><div class="sd-w">'
      '<div class="sd-r"><span class="sd-kick">Гайдлайн</span>'
      '<h2>29 полос, по которым собирают всё остальное</h2>'
      '<p class="sd-book__lede">Документ устроен так, чтобы его открывали на нужной странице: '
      'слева правило, справа готовый макет. Ниже раскладка целиком, можно открыть любую полосу.</p></div>'
      f'<ul class="sd-book__grid sd-r">{cards}</ul>'
      '<p class="sd-book__hint">Нажмите на полосу, чтобы открыть её крупно. Стрелки листают.</p>'
      '</div></section>')


def result():
    items = [
      ('29', 'Гайдлайн на <b>29 полос</b>: правила знака, палитры и паттерна плюс собранные '
       'макеты для каждого носителя.'),
      ('40+', '<b>Больше сорока готовых макетов</b>: презентации, посты, стикеры, бланки, '
       'бейджи, выставочный комплект, сувенирка и форма футбольной команды.'),
      ('9', '<b>Девять цветов</b> с приоритетами и правилом пропорций, из которых любая '
       'инфографика собирается без дизайнера.'),
      ('1', '<b>Одно правило на знак</b>: единый цвет внутри блока. Всё остальное отдано '
       'на усмотрение того, кто делает макет.'),
    ]
    lis = ''.join(f'<li><span class="sd-num">{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="sd-res"><div class="sd-w sd-res__grid">'
      '<div class="sd-r"><span class="sd-kick">Результат</span>'
      '<h2>Что получил клиент</h2>'
      '<p class="sd-res__more">Нейминг, знак, паттерн, палитра, гайдлайн и макеты носителей. '
      'Больше о направлении: <a href="/creativedesign">услуга «Creative&nbsp;&amp;&nbsp;Design»</a></p></div>'
      f'<ul class="sd-res__list sd-r">{lis}</ul>'
      '</div></section>')


LIGHTBOX = ('<div class="sd-lb" id="sd-lb" aria-hidden="true">'
            '<div class="sd-lb__box">'
            '<button class="sd-lb__x" id="sd-lb-x" type="button" aria-label="Закрыть">&times;</button>'
            f'<button class="sd-lb__nav sd-lb__nav--p" id="sd-lb-p" type="button" aria-label="Предыдущая полоса">{CHEV}</button>'
            f'<button class="sd-lb__nav sd-lb__nav--n" id="sd-lb-n" type="button" aria-label="Следующая полоса">{CHEV}</button>'
            '<img id="sd-lb-img" src="" alt="">'
            '<div class="sd-lb__cap"><b id="sd-lb-t"></b><span id="sd-lb-c"></span></div>'
            '</div></div>')

PAGE_JS = """<script>(function(){
 // ── знак: перекраска пары SALES/DEP
 var swap=document.getElementById('sd-swap'),stage=document.getElementById('sd-stage'),
     stage2=document.getElementById('sd-stage2');
 if(swap&&stage){
  var btns=[].slice.call(swap.querySelectorAll('button'));
  function paint(b){
   [stage,stage2].forEach(function(s){if(!s)return;
    s.style.setProperty('--sd-a',b.getAttribute('data-a'));
    s.style.setProperty('--sd-b',b.getAttribute('data-b'));
    s.style.background=b.getAttribute('data-bg');});
   btns.forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});
  }
  btns.forEach(function(b){b.addEventListener('click',function(){paint(b);});});
  paint(btns[0]);
 }
 // ── паттерн: режимы
 var modes=document.getElementById('sd-modes'),box=document.getElementById('sd-lab'),
     note=document.getElementById('sd-note');
 if(modes&&box){
  var mb=[].slice.call(modes.querySelectorAll('button'));
  mb.forEach(function(b){b.addEventListener('click',function(){
   var m=b.getAttribute('data-mode');
   box.setAttribute('data-mode',m);
   box.querySelector('.sd-pat').classList.toggle('sd-pat--line',m==='line');
   note.textContent=b.getAttribute('data-note');
   mb.forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});});});
 }
 // ── палитра: HEX в буфер
 [].forEach.call(document.querySelectorAll('.sd-sw'),function(sw){
  sw.addEventListener('click',function(){
   var hex=sw.getAttribute('data-hex');
   function done(){sw.classList.add('is-copied');
    setTimeout(function(){sw.classList.remove('is-copied');},1100);}
   if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(hex).then(done,function(){});
   }else{
    var t=document.createElement('textarea');t.value=hex;document.body.appendChild(t);
    t.select();try{document.execCommand('copy');done();}catch(e){}document.body.removeChild(t);
   }});});
 // ── гайдлайн: лайтбокс
 var cards=[].slice.call(document.querySelectorAll('.sd-book__grid button')),
     lb=document.getElementById('sd-lb'),img=document.getElementById('sd-lb-img'),
     ttl=document.getElementById('sd-lb-t'),cap=document.getElementById('sd-lb-c'),
     x=document.getElementById('sd-lb-x'),p=document.getElementById('sd-lb-p'),
     n=document.getElementById('sd-lb-n'),cur=0;
 function show(i){
  if(i<0)i=cards.length-1; if(i>=cards.length)i=0; cur=i;
  var c=cards[i];
  img.src=c.getAttribute('data-src');
  img.alt='Полоса гайдлайна SALESDEP: '+c.getAttribute('data-title').toLowerCase();
  ttl.textContent=c.getAttribute('data-title');
  cap.textContent=c.getAttribute('data-cap');
 }
 function open(i){show(i);lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';x.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  img.removeAttribute('src');document.body.style.overflow='';}
 cards.forEach(function(c,i){c.addEventListener('click',function(){open(i);});});
 x.addEventListener('click',close);
 p.addEventListener('click',function(){show(cur-1);});
 n.addEventListener('click',function(){show(cur+1);});
 lb.addEventListener('click',function(e){if(e.target===lb)close();});
 document.addEventListener('keydown',function(e){
  if(!lb.classList.contains('is-open'))return;
  if(e.key==='Escape')close();
  if(e.key==='ArrowRight'){e.preventDefault();show(cur+1);}
  if(e.key==='ArrowLeft'){e.preventDefault();show(cur-1);}});
 // ── появление блоков
 var els=[].slice.call(document.querySelectorAll('.sd-r'));
 function inn(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(n);else io.observe(n);});
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Фирменный стиль отдела продаж Becar",'
  f'"item":"{URL}"}}]}}</script>')


def build():
    # своего блока «обсудить проект» нет: фиолетовая форма из rc.footer() закрывает
    # страницу, второй CTA был бы дублем (как на CeramicaNova, OBO и We&I)
    body = (f'{rc.header()}<main class="sd">{hero()}{task()}{logo()}{palette()}{lab()}'
            f'{media()}{book()}{result()}</main>{LIGHTBOX}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'becar', 'sdep')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
    # CI переименовывает index-a2.html в index.html, поэтому старый A2-файл надо убрать,
    # иначе он затрёт кастомную страницу прямо на деплое. Tilda-версия остаётся в истории git.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
