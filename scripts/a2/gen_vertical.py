#!/usr/bin/env python3
"""Генерит mirror/creative/becar/vertical/index.html — кейс «Брошюра Vertical BW
Signature Collection» для Becar Asset Management: печатный буклет на 24 полосы, которым
отдел продаж объяснял инвесторам покупку номера в кондо-отеле на Таганской.

Дизайн-концепция: «острый угол». Айдентика Vertical держится на треугольниках, которые
режут фотографию и плашку по диагонали, и на узком капсе PF DIN Condensed. Веб-аналог:
Oswald (дисплей) + Onest (текст) из /fonts/oswald-onest.css, clip-path-треугольники
вместо рамок, малиновый и алый как основные, голубой для цифр.

Главный блок — листалка из 11 разворотов, собранных из печатного PDF (вылеты обрезаны,
полосы склеены попарно). Скролл-снап, стрелки, миниатюры, лайтбокс.
Ассеты: mirror/images/vertical/ (scripts/vertical-assets.py).

URL кейса прежний (он в sitemap и каталогах). Правки — ТОЛЬКО через этот скрипт;
build_v1 страницу пропускает по маркеру <!--custom-page-->."""
import os
import importlib.util
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/vertical'
URL = 'https://hand-marketing.ru/creative/becar/vertical/'

# ─── 11 разворотов: (полосы, глава, заголовок, описание, alt) ────────────────
SPREADS = [
 ('2-3', 'Продукт',
  'Всё предложение на первом развороте',
  'Слева одна строка про то, что это четыре этажа под международным брендом. Справа '
  'колонка цифр, ради которых буклет и открывают: от 6,5 млн за номер, до 13% годовых, '
  'от 460 тысяч дохода в год, 100% в собственности, 83% заполняемости. Рядом дата '
  'открытия и красная плашка «всего 82 номера», чтобы предложение читалось как ограниченное.',
  'Разворот брошюры Vertical: цифры доходности номера и фотография здания отеля на Таганской'),
 ('4-5', 'Продукт',
  'Что такое Vertical и кто в нём живёт',
  'Слева объяснение бренда: дизайнерская сеть для миллениалов внутри Best Western '
  'Signature Collection. Справа то, из чего складывается заполняемость: 60 каналов '
  'продаж, 300 корпоративных договоров, больше половины броней напрямую. Логотипы '
  'РЖД, S7, Huawei и Philip Morris стоят как доказательство, а не как украшение.',
  'Разворот брошюры Vertical: описание бренда отеля и структура заполняемости с логотипами компаний'),
 ('6-7', 'Продукт',
  'Почему это выгоднее квартиры',
  'Разворот отвечает на главное возражение. Номер в кондо-отеле сравнивается со '
  'стрит-ритейлом и квартирой: за пять лет первый Vertical на Московском проспекте '
  'вырос в цене на 40%, пока рынок квартир просел. Тут же схема win-win-win, где '
  'управляющая компания зарабатывает последней.',
  'Разворот брошюры Vertical: доходность кондо-отеля в сравнении с квартирой и стратегия win-win-win'),
 ('8-9', 'Сценарии',
  'Кейс инвестора и деньги для ребёнка',
  'Слева история с датами: купил лот в 2013 году, получал ренту до 14%, вышел из '
  'актива в 2017 году с 2,8 млн чистого дохода. Справа тот же расчёт, но на языке '
  'семьи: покупка номера сегодня превращается в квартиру или обучение к '
  'восемнадцатилетию ребёнка.',
  'Разворот брошюры Vertical: реальный кейс инвестора и стратегия накоплений на будущее ребёнка'),
 ('10-11', 'Сценарии',
  'Родители, пенсия и жизнь сейчас',
  'Два сюжета подряд без единой таблицы. Яхта и фраза про то, что ждать прибавки '
  'к пенсии бессмысленно. Пляж и три способа распорядиться номером: получать доход, '
  'подарить или передать по наследству, быстро продать по подтверждённой доходности. '
  'Разворот держит эмоцию, а цифры уже прочитаны раньше.',
  'Разворот брошюры Vertical: сюжеты про заботу о родителях и свободу распоряжаться номером'),
 ('12-13', 'Объект',
  'Таганка и тайминги',
  'Тут буклет переключается на адрес. Слева про исторический центр, Театр на Таганке '
  'и дом-музей Высоцкого. Справа сухая схема расстояний: 500 метров до метро, '
  '3 километра до Курского вокзала, 30 до Шереметьево. Инвестор проверяет локацию '
  'не по эпитетам, а по минутам.',
  'Разворот брошюры Vertical: район Таганки и расстояния до метро, вокзалов и аэропортов'),
 ('14-15', 'Объект',
  'Ночной город и доступная роскошь',
  'Самый тёмный разворот буклета. Ночная Москва сверху, поверх неё обещание: 82 номера '
  'дают домашнюю атмосферу, а всё остальное в пяти минутах ходьбы. Справа формула '
  'affordable luxury одной строкой: дизайнерский интерьер без дизайнерской цены.',
  'Разворот брошюры Vertical: ночная панорама Москвы и принцип доступной роскоши'),
 ('16-17', 'Объект',
  'Большое на малом',
  'Разворот про «котловой» метод: доход считается по всему отелю, поэтому номер '
  'зарабатывает даже в те дни, когда стоит пустым. Под этим четыре причины, по которым '
  'схема работает: мало номеров, центр, международный бренд, объект уже построен.',
  'Разворот брошюры Vertical: котловой метод распределения дохода и четыре аргумента за объект'),
 ('18-19', 'Объект',
  'Что входит в стоимость номера',
  'Слева честный список: не только пол и стены, но мебель, сантехника, кухонная зона, '
  'техника, места хранения и вай-фай по всему отелю. Справа первая категория, Private '
  'на одного гостя, с планировкой и фотографией интерьера. Дальше номера идут по '
  'нарастанию.',
  'Разворот брошюры Vertical: комплектация номера и категория Private с планировкой'),
 ('20-21', 'Объект',
  'Studio и Comfort с планировками',
  'Основа номерного фонда: 64 студии на двоих и 9 номеров Comfort до четырёх спальных '
  'мест. На каждой полосе чертёж рядом с фотографией, чтобы метраж и картинка читались '
  'вместе. Кирпич, дерево и графика на стене повторяются из полосы в полосу, поэтому '
  'отель выглядит одним пространством.',
  'Разворот брошюры Vertical: категории номеров Studio и Comfort с планировками и интерьерами'),
 ('22-23', 'Объект',
  'Кто за этим стоит',
  'Финал: сеть кондо-отелей Vertical и группа Becar Asset Management с цифрами '
  'о 25 000 объектов недвижимости, 8 млн кв. м в управлении и 5000 сотрудников. '
  'Инвестор дочитывает буклет там же, где начал, но теперь под обещанием дохода стоит '
  'вес компании.',
  'Разворот брошюры Vertical: сеть кондо-отелей и цифры группы Becar Asset Management'),
]

# mock-cover.jpg тут не повторяем: он стоит в герое. Каждый кадр — свой разворот
MOCKUPS = [
 ('mock-numbers.jpg', 'Первый разворот: цифры предложения, ранняя редакция буклета'),
 ('mock-what.jpg', 'Разворот «Что такое Vertical» переходит через сгиб'),
 ('mock-becar.jpg', 'Финальный разворот про сеть и группу Becar'),
 ('mock-life.jpg', 'Разворот про жизнь после покупки: диагональ через сгиб'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 5l-7 7 7 7"/></svg>')
GRIP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M9 6l-5 6 5 6M15 6l5 6-5 6"/></svg>')

PAGE_CSS = """<style id="vt-css">
:root{
 --vt-berry:#a2195b;--vt-berry-d:#7d0f44;--vt-red:#e3063f;--vt-blue:#35a7df;
 --vt-teal:#139bb3;--vt-ink:#16161a;--vt-ink2:#5b6068;--vt-paper:#f5f2ef;
 --vt-df:'Oswald',Impact,system-ui,Arial,sans-serif;
 --vt-bf:'Onest',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --vt-z:1000}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.vt{font-family:var(--vt-bf);color:var(--vt-ink);background:#fff;line-height:1.62;
 font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.vt *{box-sizing:border-box}
.vt img{max-width:100%;height:auto;display:block}
.vt a{color:inherit;text-decoration:none}
.vt h1,.vt h2,.vt h3,.vt h4{font-family:var(--vt-df);font-weight:600;line-height:1.02;
 letter-spacing:.01em;margin:0;text-transform:uppercase;text-wrap:balance}
.vt p{text-wrap:pretty}
.vt-w{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,52px)}
/* маленький треугольник вместо буллета и вместо линейки в надзаголовке */
.vt-kick{font-family:var(--vt-df);font-weight:500;font-size:13px;letter-spacing:.18em;
 text-transform:uppercase;display:inline-flex;align-items:center;gap:10px}
.vt-kick::before{content:"";width:13px;height:11px;background:currentColor;
 clip-path:polygon(0 0,100% 0,50% 100%)}
.vt-num{font-family:var(--vt-df);font-weight:600;font-variant-numeric:tabular-nums;
 letter-spacing:0}
.vt-btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--vt-df);
 font-weight:500;font-size:15px;letter-spacing:.06em;text-transform:uppercase;
 padding:.95em 1.5em;border:0;cursor:pointer;transition:transform .25s,background .25s,
 color .25s,border-color .25s}
.vt-btn svg{width:1.1em;height:1.1em}
.vt-btn--b{background:var(--vt-berry);color:#fff}
.vt-btn--b:hover{background:var(--vt-red);transform:translateY(-2px)}
.vt-btn--gh{background:transparent;color:var(--vt-ink);box-shadow:inset 0 0 0 1.6px rgba(22,22,26,.22)}
.vt-btn--gh:hover{box-shadow:inset 0 0 0 1.6px var(--vt-berry);color:var(--vt-berry);
 transform:translateY(-2px)}

/* ── HERO ── */
.vt-hero{position:relative;background:#fff;overflow:hidden}
/* те же треугольники, что держат обложку буклета */
.vt-tri{position:absolute;pointer-events:none;z-index:1}
.vt-tri--tr{top:0;right:0;width:min(30vw,340px);aspect-ratio:1/.62;background:var(--vt-berry);
 clip-path:polygon(0 0,100% 0,100% 100%)}
.vt-tri--bl{left:0;bottom:0;width:min(22vw,240px);aspect-ratio:1/.8;background:var(--vt-berry);
 clip-path:polygon(0 100%,0 0,100% 100%)}
.vt-hero__in{position:relative;z-index:2;padding-top:clamp(28px,3.6vw,44px);
 padding-bottom:clamp(46px,5.6vw,72px)}
.vt-hero__top{display:flex;align-items:baseline;gap:8px 18px;flex-wrap:wrap;
 padding-bottom:clamp(34px,5vw,62px)}
.vt-logo{font-family:var(--vt-df);font-weight:600;font-size:clamp(22px,2.5vw,29px);
 letter-spacing:.06em;text-transform:uppercase;color:var(--vt-berry)}
.vt-logo span{color:var(--vt-ink2);font-weight:400;font-size:.62em;letter-spacing:.1em}
.vt-hero__by{font-size:13.5px;color:var(--vt-ink2)}
.vt-hero__grid{display:grid;grid-template-columns:1.04fr .96fr;gap:clamp(28px,4vw,58px);
 align-items:center}
.vt-hero .vt-kick{color:var(--vt-red)}
/* Oswald узкий: при том же кегле в строку влезает больше, поэтому заголовок
   мельче и шире по мере, чем на других кейсах */
.vt-hero h1{font-size:clamp(34px,4.6vw,58px);margin:16px 0 0;max-width:19ch;
 letter-spacing:.005em;line-height:1.06}
.vt-hero h1 em{font-style:normal;color:var(--vt-berry)}
.vt-hero__sub{margin:clamp(18px,2.4vw,26px) 0 0;font-size:clamp(16px,1.45vw,18.5px);
 color:#3a3f45;max-width:52ch}
.vt-chips{display:flex;flex-wrap:wrap;gap:8px;margin:clamp(22px,2.6vw,30px) 0 0;padding:0;
 list-style:none}
.vt-chips li{padding:7px 14px;box-shadow:inset 0 0 0 1.4px rgba(22,22,26,.16);font-size:12.5px;
 font-weight:600;color:#41464d}
.vt-hero__cta{margin-top:clamp(24px,3vw,34px);display:flex;gap:12px;flex-wrap:wrap}
.vt-hero__ph{position:relative}
.vt-hero__ph img{box-shadow:0 40px 80px -46px rgba(22,22,26,.6)}
.vt-hero__stamp{position:absolute;left:-8px;top:-18px;z-index:2;background:var(--vt-red);
 color:#fff;font-family:var(--vt-df);font-weight:500;font-size:12.5px;letter-spacing:.08em;
 text-transform:uppercase;padding:12px 16px;line-height:1.2;text-align:center;
 box-shadow:0 12px 26px rgba(227,6,63,.3)}
.vt-hero__stamp b{display:block;font-size:21px;letter-spacing:.02em;font-weight:600}
/* спец-строка */
.vt-spec{position:relative;z-index:2;background:var(--vt-berry)}
.vt-spec__in{max-width:1240px;margin:0 auto;padding:24px clamp(20px,4vw,52px);
 display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.vt-spec div{padding-left:16px;position:relative}
.vt-spec div::before{content:"";position:absolute;left:0;top:.42em;width:9px;height:8px;
 background:#fff;clip-path:polygon(0 0,100% 50%,0 100%)}
.vt-spec dt{font-family:var(--vt-df);font-weight:500;font-size:clamp(20px,2.1vw,26px);
 color:#fff;text-transform:uppercase;letter-spacing:.03em;line-height:1.1}
.vt-spec dd{margin:4px 0 0;font-size:12.5px;color:rgba(255,255,255,.72);line-height:1.45}

/* ── О КЛИЕНТЕ ── */
.vt-about{background:var(--vt-paper);padding:clamp(58px,7.5vw,100px) 0}
.vt-about .vt-kick{color:var(--vt-berry)}
.vt-about__grid{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(28px,5vw,64px);
 align-items:start}
.vt-about h2{font-size:clamp(27px,3.3vw,42px);margin-top:14px}
.vt-about p{margin:20px 0 0;font-size:clamp(15.5px,1.3vw,17.5px);color:#333940;max-width:60ch}
.vt-about b{font-weight:700;color:var(--vt-ink)}
.vt-geo{display:flex;flex-wrap:wrap;gap:7px;margin:24px 0 0;padding:0;list-style:none}
.vt-geo li{background:#fff;box-shadow:inset 0 0 0 1px #e4ded8;padding:6px 12px;font-size:13px;
 color:#41464d}
.vt-about__facts{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:#e4ded8;
 box-shadow:0 0 0 1px #e4ded8}
.vt-about__fact{background:#fff;padding:22px 20px 24px}
.vt-about__fact b{display:block;font-family:var(--vt-df);font-weight:600;
 font-size:clamp(25px,2.7vw,33px);line-height:1;color:var(--vt-berry);letter-spacing:.01em}
.vt-about__fact span{display:block;margin-top:8px;font-size:13px;color:var(--vt-ink2);line-height:1.4}
.vt-about__note{margin-top:2px;background:var(--vt-ink);color:#fff;padding:22px}
.vt-about__note b{display:block;font-family:var(--vt-df);font-weight:500;font-size:16px;
 letter-spacing:.04em;text-transform:uppercase;color:var(--vt-blue);margin-bottom:8px}
.vt-about__note span{font-size:14px;color:rgba(255,255,255,.82);line-height:1.55}

/* ── ЗАДАЧА ── */
.vt-task{padding:clamp(60px,8vw,110px) 0;background:#fff}
.vt-task__grid{display:grid;grid-template-columns:1.12fr .88fr;gap:clamp(28px,5vw,66px);
 align-items:start}
.vt-task .vt-kick{color:var(--vt-red)}
.vt-task h2{font-size:clamp(29px,3.7vw,48px);margin-top:14px}
.vt-task__lede p{margin:0 0 1.1em;font-size:clamp(16px,1.35vw,18.5px);color:#333940;max-width:62ch}
.vt-task__lede p:last-child{margin-bottom:0}
.vt-task__lede b{font-weight:700;color:var(--vt-ink)}
.vt-note{position:relative;background:var(--vt-berry);color:#fff;padding:32px 28px 34px;
 overflow:hidden}
.vt-note::after{content:"";position:absolute;right:0;bottom:0;width:118px;height:96px;
 background:var(--vt-red);clip-path:polygon(100% 0,100% 100%,0 100%)}
.vt-note h3{font-size:22px;margin:0 0 12px;position:relative;z-index:1}
.vt-note p{margin:0;font-size:15.5px;line-height:1.6;color:rgba(255,255,255,.9);
 position:relative;z-index:1}
.vt-note__tag{display:inline-block;background:#fff;color:var(--vt-berry);
 font-family:var(--vt-df);font-weight:500;font-size:12px;letter-spacing:.12em;
 text-transform:uppercase;padding:6px 12px;margin-bottom:16px}

/* ── ШТОРКА «РЕДАКЦИЯ И ОБНОВЛЕНИЕ» ── */
.vt-cmp{background:var(--vt-paper);padding:clamp(60px,8vw,110px) 0}
.vt-cmp .vt-kick{color:var(--vt-berry)}
.vt-cmp__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:22px;
 flex-wrap:wrap;padding-bottom:clamp(24px,3vw,36px)}
.vt-cmp__hd h2{font-size:clamp(29px,3.7vw,48px);margin-top:14px;max-width:18ch}
.vt-cmp__hint{font-size:15px;color:var(--vt-ink2);max-width:40ch}
.vt-cmp__box{position:relative;aspect-ratio:2/1;overflow:hidden;background:#fff;
 --p:50%;box-shadow:0 26px 60px -40px rgba(22,22,26,.55)}
.vt-cmp__box img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.vt-cmp__box img.b{clip-path:inset(0 0 0 var(--p))}
.vt-cmp__lbl{position:absolute;top:14px;z-index:3;background:rgba(22,22,26,.78);color:#fff;
 font-family:var(--vt-df);font-weight:500;font-size:12px;letter-spacing:.12em;
 text-transform:uppercase;padding:7px 12px;backdrop-filter:blur(6px);pointer-events:none}
.vt-cmp__lbl.l{left:14px}
.vt-cmp__lbl.r{right:14px;background:var(--vt-berry)}
.vt-cmp__bar{position:absolute;top:0;bottom:0;left:var(--p);width:3px;z-index:2;
 background:var(--vt-berry);pointer-events:none;transform:translateX(-1.5px)}
.vt-cmp__grip{position:absolute;top:50%;left:var(--p);z-index:3;width:46px;height:46px;
 margin:-23px 0 0 -23px;border-radius:50%;background:var(--vt-berry);color:#fff;
 display:grid;place-items:center;pointer-events:none;box-shadow:0 8px 22px rgba(0,0,0,.3)}
.vt-cmp__grip svg{width:22px;height:22px}
.vt-cmp__range{position:absolute;inset:0;z-index:4;width:100%;height:100%;margin:0;
 opacity:0;cursor:ew-resize;-webkit-appearance:none;appearance:none;background:none}
.vt-cmp__range::-webkit-slider-thumb{-webkit-appearance:none;width:46px;height:100%}
.vt-cmp__range::-moz-range-thumb{width:46px;height:400px;border:0;background:none}
.vt-cmp__range:focus-visible{outline:3px solid var(--vt-berry);outline-offset:3px}
.vt-cmp__cap{margin:18px 0 0;font-size:15px;color:var(--vt-ink2);max-width:78ch}

/* ── ТРИ ГЛАВЫ ── */
.vt-plot{background:#fff;padding:clamp(60px,8vw,110px) 0}
.vt-plot .vt-kick{color:var(--vt-red)}
.vt-plot h2{font-size:clamp(29px,3.7vw,48px);margin-top:14px;max-width:20ch}
.vt-plot__lede{margin:18px 0 0;font-size:clamp(16px,1.35vw,18.5px);color:#333940;max-width:66ch}
.vt-plot__row{margin-top:clamp(34px,4.4vw,54px);display:grid;grid-template-columns:repeat(3,1fr);
 gap:2px}
.vt-ch{position:relative;padding:34px 28px 36px;color:#fff;overflow:hidden}
.vt-ch::after{content:"";position:absolute;left:0;bottom:0;width:88px;height:74px;
 background:rgba(255,255,255,.12);clip-path:polygon(0 0,0 100%,100% 100%)}
.vt-ch--1{background:var(--vt-berry)}
.vt-ch--2{background:var(--vt-red)}
.vt-ch--3{background:var(--vt-ink)}
.vt-ch__n{font-family:var(--vt-df);font-weight:500;font-size:12.5px;letter-spacing:.16em;
 text-transform:uppercase;color:rgba(255,255,255,.72);position:relative;z-index:1}
.vt-ch h3{font-size:clamp(22px,2.3vw,28px);margin:12px 0 12px;position:relative;z-index:1}
.vt-ch p{margin:0 0 18px;font-size:15.5px;color:rgba(255,255,255,.86);position:relative;z-index:1}
.vt-ch ul{list-style:none;margin:0;padding:0;display:grid;gap:9px;position:relative;z-index:1}
.vt-ch li{position:relative;padding-left:20px;font-size:14.5px;color:rgba(255,255,255,.94)}
.vt-ch li::before{content:"";position:absolute;left:0;top:.52em;width:9px;height:8px;
 background:#fff;clip-path:polygon(0 0,100% 50%,0 100%)}
.vt-ch--3 li::before{background:var(--vt-blue)}

/* ── ЛИСТАЛКА РАЗВОРОТОВ ── */
.vt-book{background:var(--vt-ink);color:#fff;padding:clamp(58px,7.5vw,104px) 0;overflow:hidden}
.vt-book .vt-kick{color:var(--vt-blue)}
.vt-book__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:22px;
 flex-wrap:wrap;padding-bottom:clamp(26px,3.4vw,42px)}
.vt-book__hd h2{font-size:clamp(29px,3.9vw,50px);margin-top:12px}
.vt-book__hint{font-size:14px;color:rgba(255,255,255,.58);max-width:32ch}
.vt-track{display:flex;gap:clamp(14px,2vw,26px);overflow-x:auto;scroll-snap-type:x mandatory;
 scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.vt-track::-webkit-scrollbar{display:none}
.vt-slide{flex:0 0 100%;scroll-snap-align:center;margin:0}
.vt-slide__ph{position:relative;background:#0e0e11;cursor:zoom-in;overflow:hidden}
.vt-slide__ph img{width:100%;aspect-ratio:2/1;object-fit:cover}
.vt-slide__ph::after{content:"";position:absolute;top:0;bottom:0;left:50%;width:2px;
 background:linear-gradient(180deg,rgba(0,0,0,.16),rgba(0,0,0,.05));pointer-events:none}
.vt-slide__pg{position:absolute;left:0;top:0;z-index:2;background:var(--vt-berry);
 color:#fff;font-family:var(--vt-df);font-weight:500;font-size:12px;
 letter-spacing:.1em;text-transform:uppercase;padding:8px 14px}
.vt-slide__ch{position:absolute;right:0;top:0;z-index:2;background:rgba(22,22,26,.72);
 color:#fff;font-size:11.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
 padding:8px 13px;backdrop-filter:blur(6px)}
.vt-slide__zoom{position:absolute;right:12px;bottom:12px;z-index:2;background:rgba(22,22,26,.72);
 color:#fff;font-size:12px;font-weight:600;padding:7px 12px;backdrop-filter:blur(6px);
 opacity:0;transition:opacity .25s}
.vt-slide__ph:hover .vt-slide__zoom{opacity:1}
.vt-slide figcaption{padding:24px 2px 0;display:grid;grid-template-columns:.62fr 1.38fr;
 gap:clamp(14px,3vw,40px);align-items:start;min-height:138px}
.vt-slide figcaption h3{font-size:clamp(20px,2.1vw,26px);color:#fff}
.vt-slide figcaption p{margin:0;font-size:15.5px;color:rgba(255,255,255,.72);max-width:64ch}
.vt-nav{margin-top:clamp(18px,2.4vw,28px);display:flex;align-items:center;
 justify-content:space-between;gap:18px;flex-wrap:wrap}
.vt-nav__btns{display:flex;align-items:center;gap:10px}
.vt-arrow{width:46px;height:46px;display:grid;place-items:center;background:transparent;
 border:1.6px solid rgba(255,255,255,.3);color:#fff;cursor:pointer;
 transition:background .2s,border-color .2s,opacity .2s}
.vt-arrow svg{width:20px;height:20px}
.vt-arrow--next svg{transform:rotate(180deg)}
.vt-arrow:hover{background:var(--vt-berry);border-color:var(--vt-berry)}
.vt-arrow[disabled]{opacity:.28;cursor:default}
.vt-arrow[disabled]:hover{background:transparent;border-color:rgba(255,255,255,.3)}
.vt-count{font-family:var(--vt-df);font-weight:500;font-size:16px;letter-spacing:.08em;
 color:rgba(255,255,255,.55);min-width:5.5em}
.vt-count b{color:var(--vt-blue);font-weight:600}
.vt-thumbs{display:flex;gap:7px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.vt-thumbs::-webkit-scrollbar{display:none}
.vt-thumb{flex:0 0 auto;width:74px;padding:0;border:0;background:none;cursor:pointer;
 opacity:.42;transition:opacity .22s,outline-color .22s;outline:2px solid transparent;
 outline-offset:2px}
.vt-thumb img{width:100%;aspect-ratio:2/1;object-fit:cover}
.vt-thumb:hover{opacity:.8}
.vt-thumb.is-on{opacity:1;outline-color:var(--vt-blue)}

/* ── ГРАФИКА ── */
.vt-craft{padding:clamp(60px,8vw,110px) 0;background:#fff}
.vt-craft__grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,64px);
 align-items:center}
.vt-craft .vt-kick{color:var(--vt-red)}
.vt-craft h2{font-size:clamp(29px,3.7vw,48px);margin-top:14px}
.vt-craft p{font-size:clamp(16px,1.35vw,18.5px);color:#333940;max-width:58ch}
.vt-craft p+p{margin-top:1.05em}
.vt-pal{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;margin-top:clamp(26px,3vw,36px)}
.vt-sw{position:relative;padding:66px 12px 14px;color:#fff;overflow:hidden}
.vt-sw::after{content:"";position:absolute;right:0;top:0;width:42px;height:36px;
 background:rgba(255,255,255,.18);clip-path:polygon(100% 0,100% 100%,0 0)}
.vt-sw span{display:block;font-family:var(--vt-df);font-weight:500;font-size:12.5px;
 letter-spacing:.1em;text-transform:uppercase}
.vt-sw small{display:block;font-size:11.5px;opacity:.78;margin-top:2px}
.vt-sw--b{background:var(--vt-berry)}
.vt-sw--r{background:var(--vt-red)}
.vt-sw--l{background:var(--vt-blue)}
.vt-sw--i{background:var(--vt-ink)}
.vt-craft__ph figure{margin:0}
.vt-craft__ph img{box-shadow:0 30px 60px -36px rgba(22,22,26,.5)}
.vt-craft__ph figcaption{margin-top:14px;font-size:14px;color:var(--vt-ink2)}

/* ── В ПЕЧАТИ ── */
.vt-print{background:var(--vt-paper);padding:clamp(58px,7.5vw,104px) 0}
.vt-print .vt-kick{color:var(--vt-berry)}
.vt-print h2{font-size:clamp(29px,3.7vw,48px);margin-top:14px}
.vt-print__lede{margin:16px 0 0;font-size:clamp(16px,1.35vw,18.5px);color:#3a3f45;max-width:60ch}
.vt-print__grid{margin-top:clamp(32px,4vw,48px);display:grid;grid-template-columns:repeat(2,1fr);
 gap:clamp(16px,2vw,26px)}
.vt-print figure{margin:0;background:#fff}
.vt-print figure img{width:100%;aspect-ratio:4/3;object-fit:cover}
.vt-print figcaption{padding:14px 16px 16px;font-size:14px;color:var(--vt-ink2)}
.vt-print__specs{margin-top:clamp(28px,3.4vw,40px);display:flex;flex-wrap:wrap;gap:10px}
.vt-print__specs span{background:var(--vt-ink);color:#fff;font-family:var(--vt-df);
 font-weight:400;font-size:13px;letter-spacing:.08em;text-transform:uppercase;padding:9px 15px}

/* ── РЕЗУЛЬТАТ ── */
.vt-res{padding:clamp(60px,8vw,110px) 0;background:#fff}
.vt-res__grid{display:grid;grid-template-columns:.78fr 1.22fr;gap:clamp(24px,5vw,64px);
 align-items:start}
.vt-res .vt-kick{color:var(--vt-red)}
.vt-res h2{font-size:clamp(29px,3.7vw,48px);margin-top:14px}
.vt-res__list{list-style:none;margin:0;padding:0;display:grid;gap:18px}
.vt-res__list li{display:flex;gap:18px;font-size:clamp(16px,1.3vw,18px);color:#333940;
 padding-bottom:18px;border-bottom:1px solid #e9e4df}
.vt-res__list li:last-child{border-bottom:0;padding-bottom:0}
.vt-res__list b{font-weight:700;color:var(--vt-ink)}
.vt-res__list .vt-num{color:var(--vt-berry);flex:none;font-size:20px;min-width:2.2em;
 line-height:1.35}
.vt-res__more{margin:20px 0 0;font-size:15px;color:var(--vt-ink2);max-width:34ch}
.vt-res__more a{color:var(--vt-berry);font-weight:600;text-decoration:underline;
 text-underline-offset:3px}

/* ── ЛАЙТБОКС ── */
.vt-lb{position:fixed;inset:0;z-index:var(--vt-z);display:none;align-items:center;
 justify-content:center;padding:clamp(12px,3vw,44px);background:rgba(12,12,15,.95)}
.vt-lb.is-open{display:flex}
.vt-lb__box{position:relative;width:min(1500px,100%)}
.vt-lb__box img{width:100%;height:auto;max-height:82vh;object-fit:contain}
.vt-lb__cap{margin-top:14px;color:rgba(255,255,255,.8);font-size:14px}
.vt-lb__x{position:absolute;top:-46px;right:0;width:38px;height:38px;
 border:1.4px solid rgba(255,255,255,.4);background:transparent;color:#fff;font-size:22px;
 line-height:1;cursor:pointer;transition:background .2s,border-color .2s}
.vt-lb__x:hover{background:rgba(255,255,255,.14);border-color:#fff}

/* ── REVEAL ── */
html.no-js .vt-r{opacity:1!important;transform:none!important}
.vt-r{opacity:0;transform:translateY(22px);
 transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.vt-r.is-in{opacity:1;transform:none}

/* ── АДАПТИВ ── */
@media(max-width:1020px){
 .vt-hero__grid{grid-template-columns:1fr;gap:30px}
 .vt-hero__ph{order:-1}
 .vt-tri--tr{width:36vw}
 .vt-spec__in{grid-template-columns:repeat(2,1fr)}
 .vt-task__grid,.vt-craft__grid,.vt-res__grid,.vt-about__grid{grid-template-columns:1fr;gap:26px}
 .vt-plot__row{grid-template-columns:1fr}
 .vt-slide figcaption{grid-template-columns:1fr;gap:10px;min-height:0}
}
@media(max-width:680px){
 .vt{font-size:16px}
 .vt-hero__stamp{font-size:11.5px;padding:9px 12px}
 .vt-hero__stamp b{font-size:18px}
 .vt-print__grid{grid-template-columns:1fr}
 .vt-about__facts{grid-template-columns:1fr}
 .vt-pal{grid-template-columns:repeat(2,1fr)}
 .vt-sw{padding:46px 12px 12px}
 .vt-nav{gap:12px}
 .vt-thumbs{order:3;width:100%}
 .vt-lb__x{top:-38px}
 .vt-slide__ch{display:none}
}
@media(max-width:420px){
 .vt-spec__in{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){
 .vt-r{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .vt *{transition-duration:.01ms!important;scroll-behavior:auto}
 .vt-track{scroll-behavior:auto}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Брошюра Vertical BW Signature Collection для Becar: 24 полосы про кондо-отель | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: печатная брошюра бутик-отеля Vertical BW Signature Collection на Таганской для Becar Asset Management. 24 полосы, 11 разворотов, квадрат 210×210 мм, полноцвет 4+4. Копирайтинг, вёрстка и препресс: буклет объясняет инвестору покупку номера в кондо-отеле.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Брошюра Vertical BW Signature Collection | кейс Hand Marketing">
<meta property="og:description" content="24 полосы и 11 разворотов, которыми отдел продаж Becar продавал номера в кондо-отеле на Таганской. Копирайтинг, вёрстка, препресс, печать 4+4.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/mock-cover.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/oswald-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def hero():
    return (
      '<header class="vt-hero">'
      '<div class="vt-tri vt-tri--tr" aria-hidden="true"></div>'
      '<div class="vt-tri vt-tri--bl" aria-hidden="true"></div>'
      '<div class="vt-w vt-hero__in">'
      '<div class="vt-hero__top">'
      '<span class="vt-logo">Vertical <span>BW Signature Collection</span></span>'
      '<span class="vt-hero__by">Becar Asset Management, отель на Таганской</span>'
      '</div>'
      '<div class="vt-hero__grid">'
      '<div>'
      '<span class="vt-kick">Полиграфия и копирайтинг</span>'
      '<h1>Буклет, который продаёт <em>номер в отеле</em> как вклад</h1>'
      '<p class="vt-hero__sub">Becar открывал в Москве бутик-отель на 82 номера и продавал '
      'эти номера частным инвесторам. Мы собрали брошюру на 24 полосы: она отвечает на '
      'вопросы про доход, показывает сам отель и остаётся у человека на столе после встречи.</p>'
      '<ul class="vt-chips"><li>Концепция издания</li><li>Копирайтинг</li>'
      '<li>Вёрстка разворотов</li><li>Препресс и печать</li></ul>'
      '<div class="vt-hero__cta">'
      f'<a class="vt-btn vt-btn--b" href="#vt-book">Листать развороты {ARROW}</a>'
      '<a class="vt-btn vt-btn--gh" href="#vt-print">Как выглядит в печати</a>'
      '</div></div>'
      '<div class="vt-hero__ph">'
      '<div class="vt-hero__stamp">Номеров в отеле<b>82</b></div>'
      f'<img src="{IMG}/mock-cover.jpg" width="1680" height="1260" '
      'alt="Печатная брошюра Vertical BW Signature Collection: обложка и раскрытый разворот" '
      'loading="eager" fetchpriority="high">'
      '</div></div></div>'
      '<div class="vt-spec"><dl class="vt-spec__in">'
      '<div><dt>24 полосы</dt><dd>11 разворотов плюс обложка и задник</dd></div>'
      '<div><dt>210×210 мм</dt><dd>квадрат в руках и на столе переговорной</dd></div>'
      '<div><dt>4+4</dt><dd>полноцвет с двух сторон, вылеты под обрез</dd></div>'
      '<div><dt>2020 год</dt><dd>к открытию отеля и старту продаж номеров</dd></div>'
      '</dl></div></header>')


def about():
    """Справка о клиенте. Цифры взяты с полосы 23 самой брошюры."""
    facts = [('25 000', 'объектов недвижимости'),
             ('8 млн кв. м', 'в управлении группы'),
             ('5000', 'сотрудников'),
             ('с 1992 года', 'на рынке недвижимости')]
    cells = ''.join(f'<div class="vt-about__fact"><b>{k}</b><span>{H.escape(v)}</span></div>'
                    for k, v in facts)
    geo = ''.join(f'<li>{g}</li>' for g in
                  ('Россия', 'США', 'Европа', 'СНГ', 'Ближний Восток'))
    return (
      '<section class="vt-about"><div class="vt-w vt-about__grid">'
      '<div class="vt-r"><span class="vt-kick">О клиенте</span>'
      '<h2>Becar Asset Management</h2>'
      '<p>Международная группа компаний, основанная в 1992 году: управление недвижимостью '
      'и техническая эксплуатация, девелопмент, инвестиции, собственные сети апарт- и '
      'кондо-отелей. Собственные офисы в Москве, Петербурге и Лондоне, представительства '
      'в других городах России.</p>'
      '<p><b>Vertical BW Signature Collection</b> входит в сеть кондо-отелей Vertical и '
      'работает под международным брендом Best Western. Для инвестора это половина '
      'аргумента: он покупает не отдельный номер с ремонтом, а место в сети с общими '
      'каналами бронирования, корпоративными договорами и управляющей компанией.</p>'
      f'<ul class="vt-geo">{geo}</ul></div>'
      '<div class="vt-r">'
      f'<div class="vt-about__facts">{cells}</div>'
      '<div class="vt-about__note"><b>Что это меняло для брошюры</b>'
      '<span>Доход обещает не отель, а тот, кто им управляет. Поэтому цифры группы стоят '
      'на финальном развороте: буклет заканчивается не эмоцией, а весом компании.</span></div>'
      '</div></div></section>')


def task():
    return (
      '<section class="vt-task"><div class="vt-w vt-task__grid">'
      '<div class="vt-r"><span class="vt-kick">Задача</span>'
      '<h2>Объяснить продукт, которого человек не покупал ни разу</h2>'
      '<div class="vt-task__lede" style="margin-top:22px">'
      '<p>Номер в кондо-отеле выглядит как недвижимость, а работает как вклад. Покупатель '
      'сравнивает его с квартирой под сдачу и сразу достраивает знакомую картину: искать '
      'жильцов, чинить, разбираться с ремонтом. Продавать нужно было обратное, '
      '<b>схему, где всей операционкой занимается управляющая компания</b>, а собственник '
      'получает доход на карту.</p>'
      '<p>Материалы у клиента были: доходность, кейс инвестора с Московского проспекта, '
      'планировки, фотографии интерьеров и района. Не было издания, которое проводит '
      'человека от первого вопроса до подписи и работает без менеджера рядом.</p>'
      '</div></div>'
      '<div class="vt-note vt-r"><span class="vt-note__tag">Сложность</span>'
      '<h3>Инвестору мало цифр</h3>'
      '<p>Доходность считают на калькуляторе за минуту, а решение принимают дольше. '
      'Человеку нужно увидеть здание, район, номер и понять, кто будет здесь жить. '
      'Поэтому в буклете деньги и отель идут не по очереди, а по нарастанию.</p></div>'
      '</div></section>')


def compare():
    """Шторка «ТЗ и дизайн»: слева текст клиента, справа финальный разворот 22-23."""
    return (
      '<section class="vt-cmp"><div class="vt-w">'
      '<div class="vt-cmp__hd vt-r"><div><span class="vt-kick">С чего начинали</span>'
      '<h2>ТЗ и дизайн</h2></div>'
      '<p class="vt-cmp__hint">Потяните ползунок: слева текст, который пришёл от клиента, '
      'справа тот же смысл в развороте буклета.</p></div>'
      '<div class="vt-cmp__box vt-r" id="vt-cmp">'
      f'<img class="a" src="{IMG}/brief.jpg" width="1680" height="840" '
      'alt="Исходный текст клиента про арендный доход и цифры компании, без вёрстки" '
      'loading="lazy">'
      f'<img class="b" src="{IMG}/spread-11.jpg" width="2500" height="1250" '
      'alt="Тот же смысл в готовом развороте брошюры Vertical: сеть кондо-отелей и цифры Becar" '
      'loading="lazy">'
      '<span class="vt-cmp__lbl l">ТЗ</span>'
      '<span class="vt-cmp__lbl r">Дизайн</span>'
      '<span class="vt-cmp__bar"></span>'
      f'<span class="vt-cmp__grip">{GRIP}</span>'
      '<input class="vt-cmp__range" id="vt-cmp-range" type="range" min="0" max="100" '
      'value="50" step="0.5" aria-label="Сравнить ТЗ и готовый разворот">'
      '</div>'
      '<p class="vt-cmp__cap vt-r">Смысл и цифры те же: доход без личного участия, вес '
      'управляющей компании, сеть вместо отдельного номера. Разница в том, что слева это '
      'надо читать подряд, а справа видно сразу: заголовок, пять показателей группы, карта '
      'офисов и абзац, который менеджер уже не пересказывает.</p>'
      '</div></section>')


def plot():
    ch = [
      ('Развороты 1-3', 'Продукт', 'vt-ch--1',
       'Сначала считаем: сколько стоит номер, сколько приносит и почему это не квартира.',
       ['Цифры доходности в первом же развороте',
        'Бренд Best Western и структура заполняемости',
        'Сравнение с квартирой и стрит-ритейлом']),
      ('Развороты 4-5', 'Сценарии', 'vt-ch--2',
       'Потом переводим доход на язык жизни, где у денег есть назначение.',
       ['Кейс инвестора с датами и суммами',
        'Накопить ребёнку к восемнадцати годам',
        'Помочь родителям и не ждать пенсию']),
      ('Развороты 6-11', 'Объект', 'vt-ch--3',
       'В конце показываем сам отель: район, номера и того, кто всем этим управляет.',
       ['Таганка, метро и тайминги до вокзалов',
        'Три категории номеров с планировками',
        'Сеть Vertical и группа Becar']),
    ]
    cards = ''.join(
      f'<div class="vt-ch {cls}"><span class="vt-ch__n">{n}</span><h3>{t}</h3>'
      f'<p>{lede}</p><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>'
      for n, t, cls, lede, items in ch)
    return (
      '<section class="vt-plot"><div class="vt-w">'
      '<div class="vt-r" style="max-width:70ch"><span class="vt-kick">Решение</span>'
      '<h2>Три главы вместо каталога метров</h2>'
      '<p class="vt-plot__lede">Буклет собран как разговор, который менеджер и так ведёт '
      'на встрече, только по порядку и без потерь. Сначала деньги, потом жизненный '
      'сценарий, в конце сам объект. Каждый разворот закрывает один вопрос и '
      'заканчивается цифрой, поэтому его можно открыть отдельно и показать через стол.</p></div>'
      f'<div class="vt-plot__row vt-r">{cards}</div>'
      '</div></section>')


def book():
    slides, thumbs = '', ''
    total = len(SPREADS)
    for i, (pg, chap, title, text, alt) in enumerate(SPREADS, 1):
        src = f'{IMG}/spread-{i:02d}.jpg'
        eager = 'eager' if i == 1 else 'lazy'
        slides += (
          f'<figure class="vt-slide" data-i="{i}">'
          f'<div class="vt-slide__ph vt-zoom" role="button" tabindex="0" data-src="{src}" '
          f'data-cap="Разворот {i} из {total}: {H.escape(title)}. Полосы {pg}" '
          f'aria-label="Открыть разворот {i} на весь экран">'
          f'<span class="vt-slide__pg">Полосы {pg}</span>'
          f'<span class="vt-slide__ch">{chap}</span>'
          f'<img src="{src}" width="2500" height="1250" alt="{alt}" loading="{eager}">'
          f'<span class="vt-slide__zoom">Открыть крупно</span></div>'
          f'<figcaption><h3>{H.escape(title)}</h3><p>{text}</p></figcaption></figure>')
        thumbs += (f'<button class="vt-thumb{" is-on" if i == 1 else ""}" data-go="{i}" '
                   f'type="button" aria-label="Разворот {i}, полосы {pg}">'
                   f'<img src="{IMG}/thumb-{i:02d}.jpg" width="220" height="110" alt="" '
                   f'loading="lazy"></button>')
    return (
      '<section class="vt-book" id="vt-book"><div class="vt-w">'
      '<div class="vt-book__hd vt-r"><div><span class="vt-kick">Развороты</span>'
      f'<h2>{total} разворотов, {total * 2 + 2} полосы</h2></div>'
      '<p class="vt-book__hint">Буклет читали в руках, поэтому здесь он тоже собран '
      'разворотами. Нажмите на разворот, чтобы рассмотреть его целиком.</p></div>'
      f'<div class="vt-track" id="vt-track">{slides}</div>'
      '<div class="vt-nav"><div class="vt-nav__btns">'
      f'<button class="vt-arrow vt-arrow--prev" id="vt-prev" type="button" aria-label="Предыдущий разворот">{CHEV}</button>'
      f'<button class="vt-arrow vt-arrow--next" id="vt-next" type="button" aria-label="Следующий разворот">{CHEV}</button>'
      f'<span class="vt-count" id="vt-count"><b>01</b> / {total:02d}</span></div>'
      f'<div class="vt-thumbs" id="vt-thumbs">{thumbs}</div>'
      '</div></div></section>')


def craft():
    return (
      '<section class="vt-craft"><div class="vt-w vt-craft__grid">'
      '<div class="vt-r"><span class="vt-kick">Графика</span>'
      '<h2>Треугольник вместо рамки</h2>'
      '<p style="margin-top:22px">Логотип Vertical построен на острых углах, и мы сделали '
      'этот угол рабочим инструментом вёрстки. Треугольник режет фотографию по диагонали, '
      'выводит текст на цвет и уводит взгляд к следующему блоку. Границы полосы держит '
      'не рамка, а срез, поэтому <b>разворот читается как одна плоскость</b>, а фотография '
      'спокойно переходит через сгиб.</p>'
      '<p>Цвет работает как навигация. Малиновый отвечает за бренд и заголовки, алый за '
      'то, что нужно заметить прямо сейчас, голубой за цифры и расчёты, графит за '
      'вечерние развороты про город и номера.</p>'
      '<div class="vt-pal">'
      '<div class="vt-sw vt-sw--b"><span>Малиновый</span><small>#A2195B</small></div>'
      '<div class="vt-sw vt-sw--r"><span>Алый</span><small>#E3063F</small></div>'
      '<div class="vt-sw vt-sw--l"><span>Голубой</span><small>#35A7DF</small></div>'
      '<div class="vt-sw vt-sw--i"><span>Графит</span><small>#16161A</small></div>'
      '</div></div>'
      # разворот 14-15, а не 10-11: тот показан мокапом в секции «В печати», рядом
      # два одинаковых разворота смотрелись бы повтором
      '<div class="vt-craft__ph vt-r"><figure>'
      f'<img src="{IMG}/spread-07.jpg" width="2500" height="1250" '
      'alt="Разворот брошюры Vertical: ночная панорама Москвы на две полосы с треугольниками по краям" '
      'loading="lazy">'
      '<figcaption>Ночная панорама идёт через оба разворота, поэтому сгиб перестаёт быть '
      'границей: две полосы читаются как один кадр, а треугольники по краям подкрашивают '
      'фотографию в цвета бренда.</figcaption>'
      '</figure></div>'
      '</div></section>')


def printing():
    figs = ''.join(
      f'<figure><img src="{IMG}/{f}" alt="Мокап печатной брошюры Vertical: {H.escape(c.lower())}" '
      f'loading="lazy"><figcaption>{H.escape(c)}</figcaption></figure>' for f, c in MOCKUPS)
    return (
      '<section class="vt-print" id="vt-print"><div class="vt-w">'
      '<div class="vt-r" style="max-width:64ch"><span class="vt-kick">В печати</span>'
      '<h2>Квадрат, который остаётся на столе</h2>'
      '<p class="vt-print__lede">Формат выбрали под сценарий встречи: квадрат удобно '
      'держать вдвоём и он не выглядит как очередной каталог новостройки. Буклет ушёл '
      'в печать полноцветом с двух сторон, с вылетами под обрез и клеевым скреплением.</p></div>'
      f'<div class="vt-print__grid vt-r">{figs}</div>'
      '<div class="vt-print__specs vt-r"><span>24 полосы</span><span>210×210 мм</span>'
      '<span>Полноцвет 4+4</span><span>Вылеты под обрез</span><span>Клеевое скрепление</span></div>'
      '</div></section>')


def result():
    items = [
      ('24', 'Готовый макет на <b>24 полосы</b> с препрессом: вылеты, полноцвет, файл '
       'для типографии. Клиент получил издание, а не набор макетов.'),
      ('11', '<b>Одиннадцать разворотов</b>, каждый отвечает на один вопрос инвестора '
       'и заканчивается цифрой. Менеджер открывает нужный разворот вместо пересказа.'),
      ('3', '<b>Три главы</b>: продукт, сценарий и объект. Такая структура позволяет '
       'вести разговор с любого места, а не читать буклет подряд.'),
      ('1', '<b>Один визуальный язык</b> на всё издание: треугольник, четыре цвета и '
       'крупная цифра как точка в конце разворота. Когда у проекта менялись цены и сроки, '
       'буклет переиздавали по цифрам, не переверстывая развороты заново.'),
    ]
    lis = ''.join(f'<li><span class="vt-num">{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="vt-res"><div class="vt-w vt-res__grid">'
      '<div class="vt-r"><span class="vt-kick">Результат</span>'
      '<h2>Что получил клиент</h2>'
      '<p class="vt-res__more">Концепция, тексты, вёрстка и препресс. Больше о направлении: '
      '<a href="/creativedesign">услуга «Creative&nbsp;&amp;&nbsp;Design»</a></p></div>'
      f'<ul class="vt-res__list vt-r">{lis}</ul>'
      '</div></section>')


LIGHTBOX = ('<div class="vt-lb" id="vt-lb" aria-hidden="true">'
            '<div class="vt-lb__box">'
            '<button class="vt-lb__x" id="vt-lb-x" type="button" aria-label="Закрыть">&times;</button>'
            '<img id="vt-lb-img" src="" alt="">'
            '<div class="vt-lb__cap" id="vt-lb-cap"></div></div></div>')

PAGE_JS = """<script>(function(){
 var track=document.getElementById('vt-track');
 if(track){
  var slides=[].slice.call(track.querySelectorAll('.vt-slide')),
      thumbs=[].slice.call(document.querySelectorAll('.vt-thumb')),
      prev=document.getElementById('vt-prev'),next=document.getElementById('vt-next'),
      count=document.getElementById('vt-count'),cur=1,total=slides.length;
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
  // активный слайд по скроллу (свайп на телефоне)
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
 // шторка «редакция и обновление»
 var cmp=document.getElementById('vt-cmp'),cr=document.getElementById('vt-cmp-range');
 if(cmp&&cr){var set=function(){cmp.style.setProperty('--p',cr.value+'%');};
  cr.addEventListener('input',set);set();}
 // лайтбокс разворотов
 var lb=document.getElementById('vt-lb'),lbi=document.getElementById('vt-lb-img'),
     lbc=document.getElementById('vt-lb-cap'),lbx=document.getElementById('vt-lb-x');
 function open(src,cap,alt){lbi.src=src;lbi.alt=alt||'';lbc.textContent=cap||'';
  lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';lbx.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  lbi.removeAttribute('src');document.body.style.overflow='';}
 [].forEach.call(document.querySelectorAll('.vt-zoom'),function(z){
  function fire(){var im=z.querySelector('img');
   open(z.getAttribute('data-src'),z.getAttribute('data-cap'),im?im.alt:'');}
  z.addEventListener('click',fire);
  z.addEventListener('keydown',function(e){
   if(e.key==='Enter'||e.key===' '){e.preventDefault();fire();}});});
 lbx.addEventListener('click',close);
 lb.addEventListener('click',function(e){if(e.target===lb||e.target===lb.firstChild)close();});
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape'&&lb.classList.contains('is-open'))close();});
 // reveal
 var els=[].slice.call(document.querySelectorAll('.vt-r'));
 function show(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(show);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){show(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)show(n);else io.observe(n);});
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Брошюра Vertical BW Signature Collection",'
  f'"item":"{URL}"}}]}}</script>')


def build():
    # Отдельного CTA-блока нет: фиолетовая форма из rc.footer() уже закрывает страницу,
    # второй «Обсудить проект» был бы дублем (как на We&I, CeramicaNova и OBO)
    body = (f'{rc.header()}<main class="vt">{hero()}{about()}{task()}{compare()}{plot()}{book()}'
            f'{craft()}{printing()}{result()}</main>{LIGHTBOX}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'becar', 'vertical')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
    # CI переименовывает index-a2.html в index.html, поэтому старый A2-файл надо убрать,
    # иначе он затрёт кастомную страницу прямо на деплое. Прежняя Tilda-версия остаётся
    # в истории git.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
