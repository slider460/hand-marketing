#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/patriot/index.html: кейс «Рекламный ролик УАЗ Патриот & Eaton»
(ролик о блокировке дифференциала Eaton для УАЗ Патриот, хронометраж 60 секунд).

Что было раньше: запечённая Tilda-страница — четыре абзаца «задача → компания →
решение → результат», из графики один кадр из ролика и ссылка на видео.

Идея страницы: ролик держится на противопоставлении «схема в переговорке ↔ вода
по пороги», и страница повторяет этот приём. Светлая половина — кабинет (бумага
флипчарта), тёмная — грунт. Главный экран не рассказывает про блокировку, а
показывает её работающей.

Механики:
1. Стенд «Дифференциал» — живой SVG-разрез по оси сателлитов: корпус, крестовина,
   два сателлита, две полуосевые шестерни, два колеса. Тумблер «открытый /
   заблокирован». Кинематика честная: у открытого дифференциала сумма оборотов
   колёс всегда равна удвоенным оборотам корпуса (wL + wR = 2wc), поэтому в жиже
   левое идёт вдвое быстрее корпуса, а правое стоит; сателлиты крутятся на
   разнице. В блокировке разница обнуляется, оба колеса идут с корпусом, одометр
   начинает считать метры. Это ровно тот кадр с ноутбука на 36-й секунде, только
   рабочий. Сам разрез неподвижен (как схема в ролике): вращение корпуса
   показывает кольцо с рёбрами, иначе в 2D сателлиты уезжали бы по орбите
   сквозь полуосевые шестерни.
2. Разбор монтажа на 60 секунд двумя колонками (переговорка ↔ полигон),
   которые сходятся в кульминации: палец на кнопке блокировки на 0:40.

Честность цифр: 3 съёмочных дня, 4 недели постпродакшна, согласование сценария
с российской и международной компанией, прешутинг с представителем Eaton — из
текста кейса. Хронометраж 60 с и все таймкоды — из самого файла ролика.
Обороты и моменты на стенде — модель, показывающая принцип, а не паспортные
данные узла; так и подписано под стендом.

Шрифты Alumni Sans + Fira Sans, локальные (/fonts/alumni-fira.css),
кадры готовит scripts/patriot-assets.py.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/patriot'
VIDEO = '/media/eaton-yaz.mp4'
URL = 'https://hand-marketing.ru/video/patriot/'

# ─── паспорт проекта ────────────────────────────────────────────────────────
FACTS = [
    ('Клиенты', 'УАЗ и Eaton'),
    ('Формат', 'Рекламный ролик, 60 секунд'),
    ('Съёмка', '3 смены на локациях'),
    ('Постпродакшн', '4 недели'),
    ('Согласование', 'Два рынка сразу'),
]

# ─── три испытания: (кадр, alt, заголовок, текст) ───────────────────────────
TRIALS = [
    ('dust', 'УАЗ Патриот идёт по сухой грунтовке, из-под колёс поднимается пыль',
     'Сухая грунтовка',
     'Разгон по разбитой грунтовке: машина идёт боком, задняя ось сносит, из-под '
     'колёс встаёт стена пыли. Кадр открывает полевую часть и задаёт скорость.'),
    ('mud', 'Грязь заливает капот и лобовое стекло УАЗ Патриот',
     'Вязкая колея',
     'Грязь летит на капот и стекло, дворники работают прямо в кадре. Снимали без '
     'подстраховки лебёдкой: колея должна выглядеть тем, чем она была.'),
    ('ford', 'Колесо УАЗ Патриот уходит под воду на броде',
     'Брод',
     'Вода выше порогов, колесо теряет опору и начинает срываться. Это и есть тот '
     'момент, ради которого в ролике существует кнопка.'),
]

# ─── монтаж: (таймкод, кадр, alt, подпись) ──────────────────────────────────
OFFICE = [
    ('0:02', 'city', 'Москва-Сити на рассвете, начало рабочего дня',
     'Город просыпается, герой идёт на работу'),
    ('0:13', 'office', 'Двое инженеров разбирают схему у ноутбука с логотипом Eaton',
     'Разбор узла вдвоём, на ноутбуке логотип Eaton'),
    ('0:15', 'laptop-open', 'Экран ноутбука: работа дифференциала в открытом состоянии',
     '«Работа в открытом состоянии»: теория на экране'),
    ('0:19', 'marker', 'Рука с маркером у флипчарта со схемой',
     'Схема на флипчарте, маркер идёт по линии момента'),
    ('0:28', 'night', 'Инженер один ночью в переговорке за ноутбуком',
     'Ночь, переговорка, сомнение'),
    ('0:36', 'elocker', 'Экран с анимацией Eaton ELocker: момент распределяется на оба колеса',
     'ELocker: момент распределяется на оба колеса'),
]
FIELD = [
    ('0:11', 'bridge', 'УАЗ Патриот едет по городской эстакаде',
     'Машина выходит из города'),
    ('0:18', 'dust', 'УАЗ Патриот поднимает пыль на грунтовке',
     'Грунтовка, пыль, первая проверка'),
    ('0:22', 'mud', 'Грязь заливает капот УАЗ Патриот',
     'Грязь на капоте и стекле'),
    ('0:25', 'splash', 'Брызги воды из-под колеса УАЗ Патриот',
     'Вода из-под колеса летит в объектив'),
    ('0:31', 'hero', 'УАЗ Патриот в тумане идёт через брод',
     'Туман над водой, машина входит в брод'),
    ('0:34', 'ford', 'Колесо УАЗ Патриот в воде на броде',
     'Колесо срывается, тяги нет'),
]
FINALE = [
    ('0:43', 'tacho', 'Тахометр УАЗ Патриот, стрелка идёт вверх',
     'Обороты пошли вверх'),
    ('0:46', 'wheel', 'Колесо УАЗ Патриот выходит из воды',
     'Колесо цепляется за дно'),
    ('0:48', 'out', 'УАЗ Патриот выходит из брода на берег',
     'Машина выходит на берег'),
    ('0:57', 'packshot', 'Пэкшот: блокировка дифференциала Eaton для УАЗ Патриот, логотипы УАЗ и EATON',
     'Пэкшот: УАЗ и Eaton в одном кадре'),
]

# ─── производство ───────────────────────────────────────────────────────────
STAGES = [
    ('Сценарий', 'Две компании, один текст',
     'Сценарий согласовывали и с российским заводом, и с международной корпорацией. '
     'Каждая формулировка про работу узла проходила через обе стороны.'),
    ('Прешутинг', 'Эксперт Eaton на локации',
     'На разведку локаций ездили с представителем компании: он давал экспертную оценку '
     'того, что машина реально сделает на этом грунте, а что придётся имитировать.'),
    ('Съёмка', 'Три смены',
     'За три съёмочных дня сняли город, интерьер переговорной и всю полевую часть: '
     'грунтовку, колею и брод.'),
    ('Постпродакшн', 'Четыре недели',
     'Монтаж, цветокоррекция, графика узла и звук. Через месяц после съёмок ролик вышел.'),
]

PAGE_CSS = """<style id="uz-css">
:root{
 --paper:#F2EFE8; --paper-2:#E7E2D7; --ink:#141819; --ink-2:#5B6467;
 --line:rgba(20,24,25,.16); --grunt:#0E1112; --grunt-2:#191E1F;
 --torque:#5CB930; --torque-d:#3C7F1F; --mud:#B0762E;
}
.uz{font-family:'Fira Sans',-apple-system,Arial,sans-serif;color:var(--ink);
 background:var(--paper);-webkit-font-smoothing:antialiased;overflow-x:clip}
.uz *{box-sizing:border-box}
.uz img{max-width:100%;height:auto;display:block}
.uz h1,.uz h2,.uz h3,.uz .uz-num{font-family:'Alumni Sans','Fira Sans',Arial,sans-serif;
 font-weight:800;text-transform:uppercase;letter-spacing:.005em;line-height:.94;margin:0}
.uz p{margin:0}
.uz__w{max-width:1180px;margin:0 auto;padding:0 28px}
.uz__eyebrow{font-size:12px;letter-spacing:.18em;text-transform:uppercase;font-weight:700;
 color:var(--torque-d)}
.uz-sec{padding:clamp(60px,7.5vw,116px) 0}
.uz-sec__h{font-size:clamp(38px,5.4vw,76px);max-width:18ch}
.uz-sec__sub{margin-top:22px;max-width:62ch;font-size:clamp(15px,1.3vw,18px);line-height:1.65;
 color:var(--ink-2)}
.uz__eyebrow+.uz-sec__h{margin-top:12px}
.uz-fig figcaption{margin-top:10px;font-size:12.5px;color:var(--ink-2);line-height:1.45}

/* тёмные секции — «грунт» */
.uz-dark{background:var(--grunt);color:#E6E9E7}
.uz-dark .uz-sec__sub,.uz-dark .uz-fig figcaption{color:rgba(230,233,231,.62)}
.uz-dark .uz__eyebrow{color:var(--torque)}

/* ── ГЕРОЙ ── */
.uz-hero{position:relative;background:var(--grunt);color:#fff;isolation:isolate;
 padding:clamp(22px,3.4vw,40px) 0 clamp(40px,5vw,68px);overflow:hidden}
.uz-hero__bg{position:absolute;inset:0;z-index:-2}
.uz-hero__bg img{width:100%;height:100%;object-fit:cover;object-position:50% 46%;opacity:.72}
.uz-hero::after{content:'';position:absolute;inset:0;z-index:-1;
 background:linear-gradient(180deg,rgba(14,17,18,.8) 0%,rgba(14,17,18,.34) 40%,rgba(14,17,18,.92) 100%)}
.uz-back{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:500;
 color:rgba(255,255,255,.72);text-decoration:none;margin-bottom:clamp(40px,7vw,96px)}
.uz-back:hover{color:#fff}
.uz-hero__kick{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px}
.uz-hero__kick span{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;
 padding:6px 12px;border:1px solid rgba(255,255,255,.28);border-radius:2px;color:rgba(255,255,255,.8)}
.uz-hero__kick span.on{background:var(--torque);border-color:var(--torque);color:#0B1207}
.uz-hero h1{font-size:clamp(52px,11vw,146px);max-width:14ch}
.uz-hero h1 em{font-style:normal;color:var(--torque)}
.uz-hero__lead{margin-top:22px;max-width:52ch;font-size:clamp(16px,1.5vw,21px);line-height:1.55;
 color:rgba(255,255,255,.82)}
.uz-facts{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:rgba(255,255,255,.16);
 border:1px solid rgba(255,255,255,.16);margin-top:clamp(34px,5vw,62px)}
.uz-facts>div{background:rgba(10,13,14,.72);padding:16px 15px}
.uz-facts dt{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;
 color:rgba(255,255,255,.55)}
.uz-facts dd{margin:8px 0 0;font-family:'Alumni Sans','Fira Sans',Arial,sans-serif;font-weight:700;
 text-transform:uppercase;line-height:1;font-size:clamp(20px,2.1vw,29px)}

/* ── ЗАДАЧА ── */
.uz-task__grid{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);
 gap:clamp(26px,4vw,58px);align-items:start;margin-top:clamp(26px,3.4vw,44px)}
.uz-task__t p+p{margin-top:15px}
.uz-task__t p{font-size:clamp(15px,1.35vw,18px);line-height:1.68;color:var(--ink-2)}
.uz-task__t b{color:var(--ink);font-weight:600}
.uz-quote{margin-top:26px;padding:22px 24px;background:var(--paper-2);border-left:3px solid var(--torque)}
.uz-quote p{font-size:clamp(16px,1.5vw,20px);line-height:1.5;color:var(--ink)}
.uz-brands{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px}
.uz-brands div{border:1px solid var(--line);padding:16px 17px;background:#fff}
.uz-brands h3{font-size:26px}
.uz-brands p{margin-top:8px;font-size:13.5px;line-height:1.5;color:var(--ink-2)}

/* ── СТЕНД: ДИФФЕРЕНЦИАЛ ── */
.uz-stand{background:var(--grunt-2)}
.uz-stand__top{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.86fr);
 gap:clamp(24px,3.4vw,52px);align-items:end}
.uz-rig{margin-top:clamp(26px,3.4vw,44px);border:1px solid rgba(255,255,255,.14);
 background:linear-gradient(180deg,#0B0E0F,#141819)}
.uz-rig__bar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;
 padding:14px 18px;border-bottom:1px solid rgba(255,255,255,.12)}
.uz-rig__mode{display:flex;gap:8px;flex-wrap:wrap}
.uz-rig__mode button{font:600 12px/1 'Fira Sans',Arial,sans-serif;letter-spacing:.09em;
 text-transform:uppercase;color:rgba(255,255,255,.68);background:transparent;cursor:pointer;
 border:1px solid rgba(255,255,255,.26);border-radius:2px;padding:11px 16px;transition:.18s}
.uz-rig__mode button:hover{color:#fff;border-color:rgba(255,255,255,.5)}
.uz-rig__mode button[aria-pressed=true]{background:var(--torque);border-color:var(--torque);color:#0B1207}
.uz-rig__hint{font-size:12px;color:rgba(255,255,255,.5)}
.uz-rig__stage{position:relative}
.uz-rig__stage svg{width:100%;height:auto;display:block}
.uz-read{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,.13);
 border-top:1px solid rgba(255,255,255,.13)}
.uz-read>div{background:#0B0E0F;padding:14px 16px}
.uz-read dt{font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;font-weight:600;
 color:rgba(255,255,255,.5)}
.uz-read dd{margin:7px 0 0;font-family:'Alumni Sans','Fira Sans',Arial,sans-serif;font-weight:700;
 font-size:30px;line-height:1;color:#fff;font-variant-numeric:tabular-nums}
.uz-read dd span.u{font-family:'Fira Sans',Arial,sans-serif;font-weight:400;font-size:13px;
 color:rgba(255,255,255,.5);margin-left:5px;text-transform:none}
.uz-read dd.on{color:var(--torque)}
.uz-rig__note{margin-top:16px;font-size:13px;line-height:1.6;color:rgba(230,233,231,.55);max-width:88ch}
.uz-rig__law{margin-top:20px;display:grid;grid-template-columns:1fr 1fr;gap:14px}
.uz-rig__law div{border:1px solid rgba(255,255,255,.14);padding:16px 18px}
.uz-rig__law h3{font-size:25px;color:#fff}
.uz-rig__law p{margin-top:8px;font-size:13.5px;line-height:1.55;color:rgba(230,233,231,.62)}
.uz-rig__law b{color:var(--torque);font-weight:600}

/* ── ПЛЕЕР ── */
.uz-film__screen{margin-top:clamp(24px,3vw,40px);background:#000;border:1px solid var(--line)}
.uz-film__screen video{width:100%;height:auto;display:block}
.uz-film__meta{display:flex;flex-wrap:wrap;gap:22px;margin-top:16px;font-size:12.5px;
 color:var(--ink-2)}
.uz-film__meta b{color:var(--ink);font-weight:600}

/* ── ИСПЫТАНИЯ ── */
.uz-trials{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2vw,26px);
 margin-top:clamp(28px,3.6vw,48px)}
.uz-trial img{width:100%;aspect-ratio:16/10;object-fit:cover}
.uz-trial h3{margin-top:16px;font-size:30px;color:#fff}
.uz-trial p{margin-top:9px;font-size:14px;line-height:1.6;color:rgba(230,233,231,.62)}

/* ── МОНТАЖ ── */
.uz-cols{display:grid;grid-template-columns:1fr 1fr;gap:clamp(18px,3vw,44px);
 margin-top:clamp(28px,3.6vw,46px)}
.uz-col__h{display:flex;align-items:baseline;gap:10px;padding-bottom:12px;
 border-bottom:2px solid var(--ink)}
.uz-col__h h3{font-size:32px}
.uz-col__h span{font-size:12px;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-2);
 font-weight:600}
.uz-col--field .uz-col__h{border-bottom-color:var(--mud)}
.uz-shot{display:grid;grid-template-columns:140px minmax(0,1fr);gap:16px;align-items:start;
 padding:16px 0;border-bottom:1px solid var(--line)}
.uz-shot img{width:140px;aspect-ratio:16/10;object-fit:cover}
.uz-shot__tc{font-family:'Alumni Sans','Fira Sans',Arial,sans-serif;font-weight:700;font-size:22px;
 line-height:1;color:var(--torque-d)}
.uz-col--field .uz-shot__tc{color:var(--mud)}
.uz-shot p{margin-top:6px;font-size:13.5px;line-height:1.5;color:var(--ink-2)}
/* кульминация */
.uz-pivot{margin-top:clamp(30px,4vw,56px);display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);
 gap:clamp(20px,3vw,44px);align-items:center;background:var(--grunt);color:#fff;
 padding:clamp(20px,2.6vw,32px)}
.uz-pivot img{width:100%;aspect-ratio:16/9;object-fit:cover}
.uz-pivot .uz-num{font-size:64px;color:var(--torque);line-height:.9}
.uz-pivot h3{margin-top:10px;font-size:clamp(30px,3.4vw,48px)}
.uz-pivot p{margin-top:14px;font-size:15px;line-height:1.6;color:rgba(255,255,255,.72)}
.uz-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(12px,1.6vw,20px);
 margin-top:clamp(20px,2.6vw,32px)}
.uz-strip img{width:100%;aspect-ratio:16/10;object-fit:cover}
.uz-strip .uz-shot__tc{margin-top:10px;color:var(--ink)}
.uz-strip p{margin-top:5px;font-size:13px;line-height:1.5;color:var(--ink-2)}

/* ── ПРОИЗВОДСТВО ── */
.uz-stages{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);
 border:1px solid var(--line);margin-top:clamp(28px,3.6vw,46px)}
.uz-stages>div{background:#fff;padding:22px 20px 24px}
.uz-stages dt{font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;
 color:var(--torque-d)}
.uz-stages h3{margin-top:12px;font-size:29px}
.uz-stages p{margin-top:9px;font-size:13.5px;line-height:1.6;color:var(--ink-2)}
.uz-out{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);
 gap:clamp(22px,3.4vw,52px);align-items:center;margin-top:clamp(34px,4.6vw,68px)}
.uz-out h2{font-size:clamp(32px,4.2vw,60px)}
.uz-out p{margin-top:16px;font-size:clamp(15px,1.35vw,18px);line-height:1.65;color:var(--ink-2)}

/* появление */
.uz .r{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}
.uz .r.on{opacity:1;transform:none}

@media(max-width:1000px){
 .uz-facts{grid-template-columns:repeat(2,1fr)}
 .uz-facts>div:last-child{grid-column:1/-1}
 .uz-read{grid-template-columns:1fr 1fr}
 .uz-task__grid,.uz-stand__top,.uz-pivot,.uz-out{grid-template-columns:1fr}
 .uz-stages{grid-template-columns:1fr 1fr}
 .uz-trials{grid-template-columns:1fr;max-width:520px}
 .uz-cols{grid-template-columns:1fr;gap:34px}
 .uz-strip{grid-template-columns:1fr 1fr}
 .uz-rig__law{grid-template-columns:1fr}
 .uz-pivot .uz-num{font-size:48px}
}
@media(max-width:560px){
 .uz__w{padding:0 16px}
 .uz-hero h1{font-size:clamp(44px,13vw,68px)}
 .uz-brands,.uz-stages{grid-template-columns:1fr}
 .uz-strip{grid-template-columns:1fr}
 .uz-shot{grid-template-columns:78px minmax(0,1fr);gap:12px}
 .uz-shot img{width:78px}
 .uz-read dd{font-size:25px}
}
@media(prefers-reduced-motion:reduce){
 .uz .r{opacity:1;transform:none;transition:none}
}
</style>"""


def hero():
    facts = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in FACTS)
    return f'''<section class="uz-hero">
<div class="uz-hero__bg"><img src="{IMG}/hero.jpg" alt="" width="1280" height="720" fetchpriority="high"></div>
<div class="uz__w">
<a class="uz-back" href="/project/">← Все проекты</a>
<div class="uz-hero__kick"><span>УАЗ × Eaton</span><span>Video Production</span><span class="on">60 секунд</span></div>
<h1>Блокировка,<br>в которую <em>верят</em></h1>
<p class="uz-hero__lead">Рекламный ролик о блокировке дифференциала Eaton для УАЗ Патриот.
Задача звучала просто: показать, что даёт узел. Сложность была в том, чтобы зритель
поверил в испытание, а не увидел очередное вывешивание колёс на полигоне.</p>
<dl class="uz-facts">{facts}</dl>
</div></section>'''


def task():
    return f'''<section class="uz-sec" id="task"><div class="uz__w">
<p class="uz__eyebrow">Задача</p>
<div class="uz-task__grid">
<div class="uz-task__t">
<h2 class="uz-sec__h">Объяснить узел, который не видно</h2>
<p>Блокировка дифференциала живёт под днищем и в обычной жизни не проявляет себя никак.
Всё, что о ней можно сказать словами, помещается в одно предложение про перераспределение
крутящего момента, и это предложение ничего не продаёт.</p>
<p><b>Ролик должен был сделать узел ощутимым.</b> Значит, нужен был не полигон с ровной
площадкой, а грунт, на котором машина реально садится: разбитая колея, вязкая грязь,
брод выше порогов.</p>
<p>Отдельная сложность была не на площадке. Сценарий согласовывали одновременно с
российским заводом и с международной корпорацией: у каждой стороны свои требования
к тому, как показывают и называют технику.</p>
<div class="uz-quote"><p>«Нам было необходимо, чтобы зритель поверил в серьёзное испытание,
а не просто увидел диагональное вывешивание колёс»</p></div>
<div class="uz-brands">
<div><h3>УАЗ</h3><p>Завод в Ульяновске, основан в июле 1941 года. Внедорожники, лёгкие
грузовики и микроавтобусы. Входит в холдинг «Соллерс».</p></div>
<div><h3>Eaton</h3><p>Американская машиностроительная корпорация, основана в 1911 году.
Электротехника, гидравлика, автокомпоненты, компоненты для авиации.</p></div>
</div>
</div>
<figure class="uz-fig r"><img src="{IMG}/office.jpg" width="1080" height="608"
 alt="Двое инженеров разбирают схему дифференциала у ноутбука с логотипом Eaton" loading="lazy">
<figcaption>Первая часть ролика идёт в переговорке: узел разбирают на схеме
и на анимации производителя.</figcaption></figure>
</div></div></section>'''


# ─── стенд «Дифференциал» ───────────────────────────────────────────────────
def gear(cx, cy, r, teeth, cls):
    """Зубчатое колесо: тело + зубья по окружности. Возвращает содержимое <g>."""
    import math
    body = (f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{cls}-body"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.30:.1f}" class="{cls}-hub"/>')
    t = ''
    for i in range(teeth):
        a = 2 * math.pi * i / teeth
        x1, y1 = cx + math.cos(a) * (r - 1), cy + math.sin(a) * (r - 1)
        x2, y2 = cx + math.cos(a) * (r + r * 0.17), cy + math.sin(a) * (r + r * 0.17)
        t += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}-tooth"/>'
    return body + t


def wheel(cx, cy, r, cls):
    """Колесо: покрышка с протектором + диск с пятью спицами."""
    import math
    s = ''
    for i in range(24):
        a = 2 * math.pi * i / 24
        x1, y1 = cx + math.cos(a) * (r - 12), cy + math.sin(a) * (r - 12)
        x2, y2 = cx + math.cos(a) * r, cy + math.sin(a) * r
        s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="uz-tread"/>'
    for i in range(5):
        a = 2 * math.pi * i / 5 - math.pi / 2
        x2, y2 = cx + math.cos(a) * (r - 26), cy + math.sin(a) * (r - 26)
        s += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" class="uz-spoke"/>'
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" class="uz-tyre"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 12}" class="uz-rim"/>' + s +
            f'<circle cx="{cx}" cy="{cy}" r="8" class="{cls}-hub"/>')


def rig_svg():
    """Разрез дифференциала по оси сателлитов: два колеса, полуоси, корпус,
    крестовина с двумя сателлитами. Разрез неподвижен (как на схеме в ролике):
    вращение корпуса показывает кольцо с рёбрами, сателлиты крутятся на месте.
    Все вращающиеся узлы вынесены в отдельные <g> — их крутит скрипт."""
    # геометрия: колёса 150 и 750, корпус 450, полуосевые шестерни 396 и 504
    left_gear = gear(396, 250, 34, 14, 'uz-g')
    right_gear = gear(504, 250, 34, 14, 'uz-g')
    spider_t = gear(450, 194, 24, 12, 'uz-g')
    spider_b = gear(450, 306, 24, 12, 'uz-g')
    return f'''<svg viewBox="0 0 900 420" role="img" class="uz-rig__svg"
 aria-label="Схема дифференциала в разрезе: корпус, сателлит, две полуосевые шестерни и два колеса">
<defs>
 <linearGradient id="uz-mud" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#4A3A22"/><stop offset="1" stop-color="#241C11"/></linearGradient>
 <linearGradient id="uz-soil" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#3A3A32"/><stop offset="1" stop-color="#20201B"/></linearGradient>
 <marker id="uz-arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.5" markerHeight="4.5"
  orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#5CB930"/></marker>
</defs>
<!-- грунт -->
<path d="M0 330 L450 330 L450 420 L0 420 z" fill="url(#uz-mud)"/>
<path d="M450 330 L900 330 L900 420 L450 420 z" fill="url(#uz-soil)"/>
<path d="M0 330 C60 322 110 340 170 332 C230 324 280 342 340 334 C390 328 420 336 450 330"
 fill="none" stroke="#6B5330" stroke-width="3"/>
<path d="M450 330 L900 330" fill="none" stroke="#585850" stroke-width="3"/>
<text x="150" y="374" class="uz-svg-lab c">жижа</text>
<text x="750" y="374" class="uz-svg-lab c">твёрдый грунт</text>
<!-- полуоси -->
<line x1="150" y1="250" x2="396" y2="250" class="uz-shaft"/>
<line x1="504" y1="250" x2="750" y2="250" class="uz-shaft"/>
<!-- стрелки крутящего момента: над полуосями, чтобы не терялись на металле -->
<line id="uz-tq-l" x1="330" y1="206" x2="206" y2="206" class="uz-tq" marker-end="url(#uz-arrow)"/>
<line id="uz-tq-r" x1="570" y1="206" x2="694" y2="206" class="uz-tq" marker-end="url(#uz-arrow)"/>
<text x="268" y="190" class="uz-svg-lab c s">момент</text>
<text x="632" y="190" class="uz-svg-lab c s">момент</text>
<!-- подвод момента на корпус -->
<line x1="450" y1="62" x2="450" y2="122" class="uz-tq on" marker-end="url(#uz-arrow)"/>
<text x="450" y="48" class="uz-svg-lab c">момент от двигателя</text>
<!-- корпус дифференциала: вращается только кольцо с рёбрами -->
<g id="uz-carrier">
 <circle cx="450" cy="250" r="98" class="uz-case"/>
 <circle cx="450" cy="250" r="86" class="uz-case-in"/>
 <g class="uz-case-rib">
  <line x1="450" y1="152" x2="450" y2="180"/><line x1="450" y1="320" x2="450" y2="348"/>
  <line x1="352" y1="250" x2="380" y2="250"/><line x1="520" y1="250" x2="548" y2="250"/>
 </g>
</g>
<!-- крестовина: ось сателлитов -->
<line x1="450" y1="168" x2="450" y2="332" class="uz-pin"/>
<!-- полуосевые шестерни -->
<g id="uz-gear-l">{left_gear}</g>
<g id="uz-gear-r">{right_gear}</g>
<!-- сателлиты: сидят на крестовине, крутятся на разнице оборотов колёс -->
<g id="uz-spider">{spider_t}</g>
<g id="uz-spider-b">{spider_b}</g>
<!-- колёса -->
<g id="uz-wheel-l">{wheel(150, 250, 80, 'uz-g')}</g>
<g id="uz-wheel-r">{wheel(750, 250, 80, 'uz-g')}</g>
<!-- брызги из-под буксующего колеса -->
<g id="uz-spray" opacity="0">
 <circle cx="126" cy="150" r="6" class="uz-spray-d"/><circle cx="62" cy="176" r="8" class="uz-spray-d"/>
 <circle cx="30" cy="228" r="5" class="uz-spray-d"/><circle cx="92" cy="128" r="4" class="uz-spray-d"/>
 <circle cx="170" cy="120" r="7" class="uz-spray-d"/><circle cx="24" cy="286" r="6" class="uz-spray-d"/>
 <circle cx="212" cy="146" r="4" class="uz-spray-d"/><circle cx="58" cy="312" r="4" class="uz-spray-d"/>
</g>
<text x="150" y="118" class="uz-svg-lab c">левое колесо</text>
<text x="750" y="118" class="uz-svg-lab c">правое колесо</text>
<text x="450" y="410" class="uz-svg-lab c">корпус, крестовина и два сателлита</text>
</svg>'''


def stand():
    return f'''<section class="uz-sec uz-dark uz-stand" id="stand"><div class="uz__w">
<div class="uz-stand__top">
<div><p class="uz__eyebrow">Как это работает</p>
<h2 class="uz-sec__h">Стенд: один узел, два состояния</h2>
<p class="uz-sec__sub">В ролике принцип объясняет анимация производителя на экране ноутбука.
Здесь тот же узел собран заново и работает: включите блокировку и посмотрите,
что происходит с колёсами, моментом и метрами.</p></div>
<figure class="uz-fig r"><img src="{IMG}/elocker.jpg" width="1080" height="608"
 alt="Кадр из ролика: экран с анимацией Eaton ELocker, момент распределяется на оба колеса"
 loading="lazy"><figcaption>Кадр 0:36, та самая схема на экране.</figcaption></figure>
</div>

<div class="uz-rig" id="uz-rig">
<div class="uz-rig__bar">
<div class="uz-rig__mode" role="group" aria-label="Состояние дифференциала">
<button type="button" data-mode="open" aria-pressed="true">Открытый</button>
<button type="button" data-mode="lock" aria-pressed="false">Блокировка ELocker</button>
</div>
<p class="uz-rig__hint" id="uz-hint">Левое колесо в жиже, правое на грунте. Двигатель работает.</p>
</div>
<div class="uz-rig__stage">{rig_svg()}</div>
<dl class="uz-read">
<div><dt>Левое колесо</dt><dd><span id="uz-rpm-l">240</span><span class="u">об/мин</span></dd></div>
<div><dt>Правое колесо</dt><dd><span id="uz-rpm-r">0</span><span class="u">об/мин</span></dd></div>
<div><dt>Момент на правом</dt><dd id="uz-tq-val"><span id="uz-nm">40</span><span class="u">Н·м</span></dd></div>
<div><dt>Пройдено</dt><dd id="uz-odo-d"><span id="uz-odo">0</span><span class="u">м</span></dd></div>
</dl>
</div>

<div class="uz-rig__law">
<div><h3>Открытый</h3><p>Сумма оборотов колёс всегда равна <b>удвоенным оборотам корпуса</b>.
Если одно колесо стоит на грунте, всё вращение уходит во второе: оно крутится вдвое быстрее
корпуса и месит жижу. Момент делится поровну, но поровну с тем колесом, которое почти ничего
не держит. Значит, и на грунте его столько же, то есть почти ноль.</p></div>
<div><h3>Заблокированный</h3><p>Сателлиты застопорены, разница оборотов обнуляется:
<b>оба колеса идут со скоростью корпуса</b>. Колесо на твёрдом грунте получает столько момента,
сколько способно передать, и машина выходит из колеи.</p></div>
</div>
<p class="uz-rig__note">Разрез показан по оси сателлитов, поэтому сам он неподвижен: скорость
корпуса видно по кольцу с рёбрами. Стенд показывает принцип, а не паспорт узла: кинематика в нём
честная (обороты колёс и сателлитов связаны так же, как в железе), а конкретные обороты и Н·м
взяты удобными для чтения. Настоящий ELocker включается кнопкой в салоне, она в ролике на 0:40.</p>
</div></section>'''


def film():
    return f'''<section class="uz-sec" id="film"><div class="uz__w">
<p class="uz__eyebrow">Ролик</p>
<h2 class="uz-sec__h">Шестьдесят секунд</h2>
<p class="uz-sec__sub">Полная версия, вышедшая в эфир и в сеть.</p>
<div class="uz-film__screen r"><video controls preload="none" playsinline
 poster="{IMG}/poster.jpg" width="1280" height="720">
<source src="{VIDEO}" type="video/mp4">Ваш браузер не воспроизводит видео.</video></div>
<p class="uz-film__meta"><span><b>Хронометраж</b> 60 секунд</span>
<span><b>Съёмка</b> 3 смены</span><span><b>Постпродакшн</b> 4 недели</span>
<span><b>Продакшн</b> Hand Marketing</span></p>
</div></section>'''


def trials():
    cards = ''.join(f'''<article class="uz-trial r"><img src="{IMG}/{f}.jpg" width="1080" height="608"
 alt="{alt}" loading="lazy"><h3>{h}</h3><p>{t}</p></article>''' for f, alt, h, t in TRIALS)
    return f'''<section class="uz-sec uz-dark" id="trials"><div class="uz__w">
<p class="uz__eyebrow">Съёмка</p>
<h2 class="uz-sec__h">Не полигон, а бездорожье</h2>
<p class="uz-sec__sub">Диагональное вывешивание на площадке снимается за час и выглядит
как аттракцион. Мы взяли тестовую машину и поехали искать грунт, на котором она садится
по-настоящему. На разведке локаций с нами был представитель Eaton: он подтверждал,
что машина действительно проходит то, что мы собираемся снимать.</p>
<div class="uz-trials">{cards}</div>
</div></section>'''


def montage():
    def col(items):
        return ''.join(f'''<div class="uz-shot"><img src="{IMG}/{f}.jpg" width="1080" height="608"
 alt="{alt}" loading="lazy"><div><p class="uz-shot__tc">{tc}</p><p>{cap}</p></div></div>'''
                       for tc, f, alt, cap in items)
    fin = ''.join(f'''<figure class="uz-fig"><img src="{IMG}/{f}.jpg" width="1080" height="608"
 alt="{alt}" loading="lazy"><p class="uz-shot__tc">{tc}</p><p>{cap}</p></figure>'''
                  for tc, f, alt, cap in FINALE)
    return f'''<section class="uz-sec" id="montage"><div class="uz__w">
<p class="uz__eyebrow">Монтаж</p>
<h2 class="uz-sec__h">Два мира одного ролика</h2>
<p class="uz-sec__sub">Первая половина идёт на два фронта. В переговорке узел разбирают
на схеме и на анимации, в поле машина проверяет каждое утверждение грунтом. Линии
сходятся ровно посередине хронометража.</p>
<div class="uz-cols">
<div class="uz-col r"><div class="uz-col__h"><h3>Переговорка</h3><span>теория</span></div>
{col(OFFICE)}</div>
<div class="uz-col uz-col--field r"><div class="uz-col__h"><h3>Полигон</h3><span>практика</span></div>
{col(FIELD)}</div>
</div>
<div class="uz-pivot r">
<img src="{IMG}/button.jpg" width="1080" height="608"
 alt="Палец нажимает кнопку блокировки дифференциала на панели УАЗ Патриот" loading="lazy">
<div><p class="uz-num">0:40</p><h3>Палец на кнопке</h3>
<p>Вся схема с флипчарта, весь разбор в переговорке и все проваленные попытки в колее
существуют ради одного плана: крупно, кнопка, щелчок. После него ролик уже не объясняет,
а показывает результат.</p></div>
</div>
<div class="uz-strip">{fin}</div>
</div></section>'''


def production():
    st = ''.join(f'<div><dt>{k}</dt><h3>{h}</h3><p>{t}</p></div>' for k, h, t in STAGES)
    return f'''<section class="uz-sec" id="production"><div class="uz__w">
<p class="uz__eyebrow">Производство</p>
<h2 class="uz-sec__h">Как это собиралось</h2>
<dl class="uz-stages r">{st}</dl>
<div class="uz-out">
<div><h2>Результат</h2>
<p>Ролик вышел одним материалом сразу для двух брендов: завод показывает возможности
машины, производитель узла показывает работу своей блокировки. Одна съёмочная группа, три смены,
месяц постпродакшна и шестьдесят секунд, после которых про блокировку дифференциала
не нужно объяснять словами.</p></div>
<figure class="uz-fig r"><img src="{IMG}/packshot.jpg" width="1280" height="720"
 alt="Финальный кадр ролика: блокировка дифференциала Eaton для УАЗ Патриот, логотипы УАЗ и EATON"
 loading="lazy"><figcaption>Финальный кадр: два бренда в одном пэкшоте.</figcaption></figure>
</div>
</div></section>'''


PAGE_JS = """<script>(function(){
var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
// появление блоков
if(window.IntersectionObserver&&!rm){
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);}});},{threshold:.12});
 [].forEach.call(document.querySelectorAll('.uz .r'),function(n){io.observe(n);});
}else{[].forEach.call(document.querySelectorAll('.uz .r'),function(n){n.classList.add('on');});}

// ─── стенд «Дифференциал» ───────────────────────────────────────────────
var rig=document.getElementById('uz-rig');
if(rig){
 var WC=120,                     // обороты корпуса, об/мин (постоянные)
     el={carrier:document.getElementById('uz-carrier'),
         spider:document.getElementById('uz-spider'),
         spiderb:document.getElementById('uz-spider-b'),
         gl:document.getElementById('uz-gear-l'),gr:document.getElementById('uz-gear-r'),
         wl:document.getElementById('uz-wheel-l'),wr:document.getElementById('uz-wheel-r'),
         spray:document.getElementById('uz-spray'),
         tql:document.getElementById('uz-tq-l'),tqr:document.getElementById('uz-tq-r'),
         rl:document.getElementById('uz-rpm-l'),rr:document.getElementById('uz-rpm-r'),
         nm:document.getElementById('uz-nm'),odo:document.getElementById('uz-odo'),
         tqv:document.getElementById('uz-tq-val'),odod:document.getElementById('uz-odo-d'),
         hint:document.getElementById('uz-hint')},
     mode='open',
     // текущие (сглаженные) обороты колёс и целевые по режиму
     wl=2*WC,wr=0,odo=0,aC=0,aL=0,aR=0,aS=0,last=0,shown={l:-1,r:-1,nm:-1,odo:-1};
 var HINT={open:'Левое колесо в жиже, правое на грунте. Двигатель работает.',
           lock:'Сателлиты застопорены: колёса связаны между собой жёстко.'};
 function targets(){return mode==='open'?[2*WC,0]:[WC,WC];}
 function set(id,v){if(shown[id]!==v){shown[id]=v;return true;}return false;}
 function paint(){
  var l=Math.round(wl),r=Math.round(wr),
      nm=Math.round(40+(340-40)*Math.min(1,r/WC));   // момент растёт вместе с правым колесом
  if(set('l',l))el.rl.textContent=l;
  if(set('r',r))el.rr.textContent=r;
  if(set('nm',nm))el.nm.textContent=nm;
  var m=Math.round(odo);if(set('odo',m))el.odo.textContent=m;
  el.tqv.classList.toggle('on',r>WC*0.5);
  el.odod.classList.toggle('on',odo>0.5);
  // момент у открытого дифференциала одинаков на обоих колёсах — стрелки живут парой
  var k=Math.min(1,r/WC),op=(0.3+0.7*k).toFixed(2),sw=(3+5*k).toFixed(1);
  el.tql.style.opacity=op;el.tql.style.strokeWidth=sw;
  el.tqr.style.opacity=op;el.tqr.style.strokeWidth=sw;
  el.spray.setAttribute('opacity',Math.max(0,Math.min(1,(l-WC*1.2)/(WC*0.8))).toFixed(2));
 }
 function frame(t){
  var dt=last?Math.min(0.05,(t-last)/1000):0;last=t;
  var g=targets(),k=1-Math.pow(0.0025,dt);      // плавный переход режима
  wl+=(g[0]-wl)*k;wr+=(g[1]-wr)*k;
  var wc=(wl+wr)/2;                              // свойство дифференциала: wc=(wL+wR)/2
  aC+=wc*6*dt;aL+=wl*6*dt;aR+=wr*6*dt;           // об/мин -> градусы в секунду
  aS+=(wl-wr)*9*dt;                              // сателлит крутится на разнице
  el.carrier.setAttribute('transform','rotate('+(aC%360).toFixed(2)+' 450 250)');
  el.spider.setAttribute('transform','rotate('+(aS%360).toFixed(2)+' 450 194)');
  el.spiderb.setAttribute('transform','rotate('+(-aS%360).toFixed(2)+' 450 306)');
  el.gl.setAttribute('transform','rotate('+(aL%360).toFixed(2)+' 396 250)');
  el.gr.setAttribute('transform','rotate('+(aR%360).toFixed(2)+' 504 250)');
  el.wl.setAttribute('transform','rotate('+(aL%360).toFixed(2)+' 150 250)');
  el.wr.setAttribute('transform','rotate('+(aR%360).toFixed(2)+' 750 250)');
  // метры считаются по колесу с грунтом и только в блокировке: в открытом
  // машина стоит на месте, счётчик не должен доползать на затухании оборотов
  if(mode==='lock')odo+=Math.max(0,wr)/60*2.2*dt;
  paint();requestAnimationFrame(frame);
 }
 [].forEach.call(rig.querySelectorAll('.uz-rig__mode button'),function(b){
  b.addEventListener('click',function(){
   mode=b.getAttribute('data-mode');
   [].forEach.call(rig.querySelectorAll('.uz-rig__mode button'),function(o){
    o.setAttribute('aria-pressed',String(o===b));});
   el.hint.textContent=HINT[mode];
   if(mode==='open'){odo=0;}
   if(window.ym)try{ym(71125393,'reachGoal','patriot_diff_'+mode);}catch(e){}
  });
 });
 if(rm){wl=2*WC;wr=0;paint();}else{requestAnimationFrame(frame);}
}
})();</script>"""

RIG_SVG_CSS = """<style id="uz-svg-css">
.uz-rig__svg{background:radial-gradient(120% 90% at 50% 22%,#1A1F20 0%,#0B0E0F 70%)}
.uz-shaft{stroke:#8A9490;stroke-width:13;stroke-linecap:round}
.uz-tyre{fill:#1B1F20;stroke:#6E7874;stroke-width:3}
.uz-rim{fill:#2A302F;stroke:#8A9490;stroke-width:2}
.uz-tread{stroke:#79837F;stroke-width:3;stroke-linecap:round}
.uz-spoke{stroke:#9AA49F;stroke-width:5;stroke-linecap:round}
.uz-g-hub{fill:#C6CFCA}
.uz-case{fill:rgba(92,185,48,.10);stroke:#5CB930;stroke-width:3}
.uz-case-in{fill:none;stroke:rgba(92,185,48,.35);stroke-width:1.5;stroke-dasharray:5 7}
.uz-case-rib line{stroke:#5CB930;stroke-width:5;stroke-linecap:round}
.uz-pin{stroke:#8A9490;stroke-width:9;stroke-linecap:round}
.uz-g-body{fill:#39413F;stroke:#B6C0BB;stroke-width:2.5}
.uz-g-tooth{stroke:#B6C0BB;stroke-width:4;stroke-linecap:round}
.uz-tq{stroke:#5CB930;stroke-width:5;stroke-linecap:round;opacity:.85}
.uz-tq.on{opacity:1;stroke-width:6}
.uz-spray-d{fill:#6B5330;opacity:.85}
.uz-svg-lab{fill:rgba(230,233,231,.55);font:500 15px 'Fira Sans',Arial,sans-serif;
 letter-spacing:.04em}
.uz-svg-lab.c{text-anchor:middle}
.uz-svg-lab.s{font-size:13px;fill:rgba(92,185,48,.9)}
/* подписи внутри SVG живут в единицах viewBox: чем уже экран, тем сильнее их
   ужимает масштаб, поэтому на телефоне размер поднимаем в два раза */
@media(max-width:900px){.uz-svg-lab{font-size:22px}.uz-svg-lab.s{font-size:19px}}
@media(max-width:520px){.uz-svg-lab{font-size:30px}.uz-svg-lab.s{font-size:26px}}
</style>"""

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
                 '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"Рекламный ролик УАЗ Патриот и Eaton",'
                 '"item":"' + URL + '"}]}</script>')

VIDEO_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"VideoObject",'
            '"name":"Рекламный ролик УАЗ Патриот и блокировка дифференциала Eaton",'
            '"description":"Рекламный ролик Hand Marketing о блокировке дифференциала Eaton для УАЗ Патриот: '
            'разбор узла в переговорной и полевые испытания на грунтовке, в грязи и на броде.",'
            '"thumbnailUrl":"https://hand-marketing.ru' + IMG + '/poster.jpg",'
            '"uploadDate":"2020-10-10","duration":"PT1M",'
            '"contentUrl":"https://hand-marketing.ru' + VIDEO + '",'
            '"publisher":{"@type":"Organization","name":"Hand Marketing"}}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Рекламный ролик УАЗ Патриот и блокировка Eaton | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: рекламный ролик о блокировке дифференциала Eaton для УАЗ Патриот. Сценарий на два рынка, прешутинг с экспертом Eaton, три съёмочные смены на грунтовке, в грязи и на броде, четыре недели постпродакшна. Интерактивный разрез дифференциала.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Рекламный ролик УАЗ Патриот &amp; Eaton | кейс Hand Marketing">
<meta property="og:description" content="Как показать узел, который не видно: разбор в переговорной, брод выше порогов и кнопка блокировки на сороковой секунде.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/hero.jpg">
<meta property="og:site_name" content="Hand Marketing"><meta property="og:locale" content="ru_RU">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/alumni-fira.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{RIG_SVG_CSS}{METRIKA}
</head>
<body>'''


def build():
    return (HEAD + rc.header() + '<main class="uz">' + hero() + task() + stand() +
            film() + trials() + montage() + production() +
            '</main><a id="lead"></a>' +
            rc.footer() + rc.JS + PAGE_JS + BREADCRUMB_LD + VIDEO_LD + '</body></html>')


if __name__ == '__main__':
    out = os.path.join(ROOT, 'video', 'patriot')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    # index-a2.html — деплой-источник Tilda-страницы, для кастомной он затёр бы её на проде
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('удалён устаревший index-a2.html')
    print('written', os.path.join(out, 'index.html'))
