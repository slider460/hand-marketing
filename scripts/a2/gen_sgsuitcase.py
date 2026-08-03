#!/usr/bin/env python3
"""Генерит mirror/creative/saintgobain/suitcase/index.html: кейс «Проектный
чемодан Saint-Gobain», концепция «Две комнаты» (2019).

Идея страницы: сам чемодан это фрагмент стены. У стены две стороны и разрез,
и у чемодана ровно то же самое, поэтому:
  • в шапке стоит объёмный чемодан, собранный CSS-трансформами из трёх реальных
    граней (лицевая 1236×915, торец 392×914, оборот 1235×914). Пропорция коробки
    взята из самих кадров, поворот идёт мышью, ползунком или тремя кнопками
    «Ремонт → Стена → Тишина», вместе с поворотом гаснет шумовая дорожка;
  • сюжет «за стенкой» показан шторкой между двумя фотографиями презентации;
  • торец разобран живым SVG: четыре слоя, каждый кликается;
  • вторая концепция («Стартовая площадка») лежит в переключателе рядом с первой,
    вместе с проверкой на подмену бренда: плашка логотипов замыливается по кнопке.

Ассеты: mirror/images/sgsuitcase/ (scripts/sgsuitcase-assets.py).

Из брифа НЕ публикуем то, что может быть коммерческой тайной: конструктив и
полиграфию (размеры, картон, кашировка, красочность, ламинация), референс
чужого бренда, дословные формулировки внутренних требований клиента и
номенклатуру со ссылками.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import html as H
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/sgsuitcase'
URL = 'https://hand-marketing.ru/creative/saintgobain/suitcase/'

# пропорции коробки взяты из кадров: лицевая 1236×915, торец 392 по ширине
BOX_D = 392 / 1236          # глубина к ширине
BOX_H = 915 / 1236          # высота к ширине

# ─── слои торца: (ключ, доля ширины, заливка, имя, подпись) ──────────────────
LAYERS = [
    ('l1', .17, 'url(#su-gyp)', 'Лист Gyproc',
     'Гипсовая строительная плита. Наружная сторона стены: та, которую потом '
     'шпаклюют, красят и на которую вешают полки.'),
    ('l2', .20, 'url(#su-met)', 'Металлический профиль',
     'Каркас задаёт толщину стены и шаг листов. На торце чемодана он виден '
     'перфорированной лентой между двумя плитами.'),
    ('l3', .46, 'url(#su-wool)', 'ISOVER Звукозащита',
     'Минеральная вата заполняет полость каркаса. Это и есть та часть стены, '
     'из-за которой в соседней комнате становится тихо.'),
    ('l4', .17, 'url(#su-gyp)', 'Лист Gyproc',
     'Второй лист замыкает конструкцию. За ним начинается уже другая комната '
     'и другая жизнь.'),
]

# ─── свойства, ради которых собирали чемодан ────────────────────────────────
PROPS = [
    ('Звукоизоляция', 'Главная тема лицевой стороны и единственная, которую '
     'собеседник может проверить на собственном опыте.'),
    ('Огнестойкость', 'Вторая тема, ради которой в чемодане лежат образцы плит '
     'разных типов.'),
    ('Прочность', 'Аргумент, который дал сам клиент: полка, прикрученная к плите, '
     'спокойно выдерживает взрослого человека.'),
]

# ─── стороны чемодана: (ключ, файл, кнопка, название, текст, alt) ────────────
SIDES = [
    ('front', 'view-front', 'Лицевая сторона', 'Стены с качеством',
     'Красная сторона говорит на языке стройки: каркас, вата в ячейках, человек '
     'с шуруповёртом на стремянке. Три слова под названием (прочные, '
     'звукоизолирующие, огнеупорные) закрывают сразу все темы, ради которых '
     'чемодан и собирали. Это же название работает именем всего носителя, '
     'которое остаётся в памяти после встречи.',
     'Лицевая сторона проектного чемодана Saint-Gobain: красно-оранжевая диагональ, '
     'название «Стены с качеством» и фотография монтажа стены из плит Gyproc '
     'с утеплителем ISOVER'),
    ('back', 'view-back', 'Оборот', 'С нами вы, как за стеной',
     'Оборот показывает то, ради чего всё делалось: детская комната, в которой '
     'ничего не происходит. Ни одного материала в кадре нет, и это осознанно: '
     'хорошая стена незаметна, о ней вспоминают только тогда, когда она не '
     'справилась.',
     'Оборот проектного чемодана Saint-Gobain: синяя диагональ, фраза «С нами вы, '
     'как за стеной» и фотография тихой детской комнаты'),
]

# ─── шаги презентации ───────────────────────────────────────────────────────
STEPS = [
    ('01', 'Ставят на стол', 'Первой видна красная сторона. Разговор начинается '
     'с проблемы, которую собеседник знает по своему опыту, а не с перечисления '
     'артикулов.'),
    ('02', 'Разворачивают', 'Синяя сторона показывает результат. Между двумя '
     'кадрами проходит вся логика продажи: было шумно, стало тихо.'),
    ('03', 'Открывают', 'Внутри образцы плит, профиля и звукоизоляции плюс '
     'печатные каталоги. Схема сборки к этому моменту уже показана торцом.'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

PAGE_CSS = """<style id="su-css">
:root{
 --su-wine:#8E2038;--su-red:#B12A21;--su-orange:#D24005;--su-blue:#294898;
 --su-blue2:#4B7FBC;--su-wool:#C8912F;
 --su-ink:#15181d;--su-ink2:#5d6470;--su-line:rgba(21,24,29,.13);--su-bg:#f4f5f6;
 --su-df:'Raleway',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --su-bf:'Onest',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --su-mf:'JetBrains Mono',ui-monospace,SFMono-Regular,Consolas,monospace;
 --su-grad:linear-gradient(90deg,#8E2038,#D24005 42%,#294898 58%,#4B7FBC)}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.su{font-family:var(--su-bf);color:var(--su-ink);background:#fff;line-height:1.62;
 font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.su *{box-sizing:border-box}
.su img{max-width:100%;height:auto;display:block}
.su a{color:inherit}
/* дисплейная гарнитура повторяет тонкий широкий гротеск с самого чемодана */
.su h1,.su h2,.su h3{font-family:var(--su-df);font-weight:300;line-height:1.06;
 letter-spacing:-.01em;margin:0;text-wrap:balance}
.su p{text-wrap:pretty}
.su-w{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,52px)}
.su-kick{font-family:var(--su-mf);font-weight:700;font-size:12px;letter-spacing:.14em;
 text-transform:uppercase;display:inline-flex;align-items:center;gap:10px;color:var(--su-ink2)}
.su-kick::before{content:"";width:26px;height:3px;background:var(--su-grad)}
.su-btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--su-bf);
 font-weight:700;font-size:15px;padding:.95em 1.5em;border:0;cursor:pointer;border-radius:999px;
 text-decoration:none;transition:transform .25s,background .25s,color .25s,border-color .25s}
.su-btn svg{width:1.1em;height:1.1em}
/* цвет у ссылок-кнопок задаём с тегом: .su a{color:inherit} специфичнее класса */
.su a.su-btn--p,.su-btn--p{background:var(--su-ink);color:#fff}
.su-btn--p:hover{transform:translateY(-2px);background:var(--su-wine)}
.su a.su-btn--gh,.su-btn--gh{background:transparent;color:var(--su-ink);
 border:2px solid var(--su-line)}
.su-btn--gh:hover{border-color:var(--su-ink);transform:translateY(-2px)}

/* ── ГЕРОЙ ── */
.su-hero{padding:clamp(28px,4vw,54px) 0 0}
.su-hero__grid{display:grid;grid-template-columns:.92fr 1.08fr;gap:clamp(26px,4.5vw,64px);
 align-items:center}
.su-hero__client{display:flex;align-items:center;gap:14px;margin-bottom:clamp(16px,2.2vw,24px)}
.su-hero__client img{width:clamp(112px,12vw,150px)}
.su-hero__client span{font-family:var(--su-mf);font-size:11.5px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--su-ink2);border-left:1px solid var(--su-line);padding-left:14px}
.su-hero h1{font-size:clamp(34px,5.4vw,68px);max-width:13ch}
/* слово «стена» покрашено ровно пополам: слева комната с ремонтом, справа тихая */
.su-hero h1 b{font-weight:300;background:linear-gradient(90deg,#B12A21 0 50%,#294898 50%);
 -webkit-background-clip:text;background-clip:text;color:transparent}
.su-hero__sub{margin:clamp(16px,2vw,24px) 0 0;font-size:clamp(16px,1.4vw,19px);
 color:#33374a;max-width:50ch}
.su-chips{display:flex;flex-wrap:wrap;gap:8px;margin:clamp(18px,2.2vw,26px) 0 0;padding:0;list-style:none}
.su-chips li{padding:6px 14px;border:1px solid var(--su-line);border-radius:999px;
 font-size:12.5px;font-weight:600;color:var(--su-ink2)}
.su-hero__cta{margin-top:clamp(20px,2.6vw,30px);display:flex;gap:12px;flex-wrap:wrap}

/* объёмный чемодан: --bw это ширина лицевой грани, от неё считается вся коробка
   (глубина 0.317 и высота 0.740 взяты из пропорций самих кадров) */
.su-stage{--bw:clamp(230px,40vw,520px);perspective:1600px;
 padding:clamp(10px,2vw,26px) 0 0;touch-action:pan-y}
.su-box{--a:18;position:relative;width:var(--bw);height:calc(var(--bw) * 0.740);
 margin:0 auto;transform-style:preserve-3d;cursor:grab;
 transform:rotateX(5deg) rotateY(calc(var(--a) * -1deg));
 transition:transform .85s cubic-bezier(.22,.72,.24,1)}
.su-box.is-drag{cursor:grabbing;transition:none}
.su-box>div{position:absolute;background-size:cover;background-position:center;
 background-repeat:no-repeat;backface-visibility:hidden;
 box-shadow:inset 0 0 0 1px rgba(21,24,29,.1)}
.su-f-front,.su-f-back{inset:0}
.su-f-front{background-image:url(IMGSRC/face-front.jpg);transform:translateZ(calc(var(--bw) * 0.1585))}
.su-f-back{background-image:url(IMGSRC/face-back.jpg);
 transform:rotateY(180deg) translateZ(calc(var(--bw) * 0.1585))}
.su-f-r,.su-f-l{top:0;height:100%;width:calc(var(--bw) * 0.317);
 left:calc((100% - var(--bw) * 0.317) / 2);background-image:url(IMGSRC/face-edge.jpg)}
.su-f-r{transform:rotateY(90deg) translateZ(calc(var(--bw) / 2))}
.su-f-l{transform:rotateY(-90deg) translateZ(calc(var(--bw) / 2))}
.su-f-t{left:0;width:100%;height:calc(var(--bw) * 0.317);
 top:calc((var(--bw) * 0.740 - var(--bw) * 0.317) / 2);
 background:linear-gradient(180deg,#e8e9ea,#cfd2d5);
 transform:rotateX(90deg) translateZ(calc(var(--bw) * 0.370))}
.su-shadow{margin:0 auto;width:min(86%,calc(var(--bw) * .86));height:26px;
 background:radial-gradient(50% 50% at 50% 50%,rgba(21,24,29,.32),transparent 72%);
 filter:blur(2px)}
/* пульт: ползунок, три кнопки и шумовая дорожка */
.su-ctrl{margin:clamp(14px,2vw,22px) auto 0;max-width:520px}
.su-ctrl__row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.su-ctrl__row button{cursor:pointer;background:transparent;border:1px solid var(--su-line);
 border-radius:999px;padding:8px 16px;font:600 13px var(--su-bf);color:var(--su-ink2);
 transition:border-color .2s,color .2s,background .2s}
.su-ctrl__row button:hover{border-color:var(--su-ink)}
.su-ctrl__row button[aria-pressed=true]{background:var(--su-ink);border-color:var(--su-ink);color:#fff}
.su-ctrl input[type=range]{width:100%;margin:14px 0 0;accent-color:var(--su-wine)}
.su-noise{display:flex;align-items:flex-end;justify-content:center;gap:3px;height:34px;
 margin-top:10px}
.su-noise i{width:4px;border-radius:2px;background:var(--su-orange);
 height:calc(6px + var(--loud,1) * var(--k) * 26px);opacity:calc(.25 + var(--loud,1) * .75);
 transition:height .25s,opacity .25s,background .35s}
.su-noise.is-quiet i{background:var(--su-blue2)}
.su-cap{margin:12px 0 0;font-size:13.5px;line-height:1.55;color:var(--su-ink2);text-align:center}
.su-cap b{color:var(--su-ink);font-weight:700}
.su-spec{margin-top:clamp(30px,4.5vw,60px);border-top:1px solid var(--su-line);
 border-bottom:1px solid var(--su-line)}
.su-spec__in{max-width:1240px;margin:0 auto;padding:22px clamp(20px,4vw,52px);
 display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.su-spec dt{font-family:var(--su-df);font-weight:300;font-size:clamp(26px,2.8vw,38px);
 letter-spacing:-.02em;line-height:1}
.su-spec div:nth-child(1) dt{color:var(--su-wine)}
.su-spec div:nth-child(2) dt{color:var(--su-orange)}
.su-spec div:nth-child(3) dt{color:var(--su-blue)}
.su-spec div:nth-child(4) dt{color:var(--su-blue2)}
.su-spec dd{margin:6px 0 0;font-family:var(--su-mf);font-size:11.5px;letter-spacing:.08em;
 text-transform:uppercase;color:var(--su-ink2);line-height:1.4}

/* ── ЗАДАЧА ── */
.su-task{padding:clamp(56px,7vw,100px) 0}
.su-task__grid{display:grid;grid-template-columns:1.06fr .94fr;gap:clamp(28px,5vw,66px);align-items:start}
.su-task h2{font-size:clamp(26px,3.4vw,44px);margin-top:14px;max-width:16ch}
.su-task p{margin:20px 0 0;font-size:clamp(15.5px,1.3vw,17.5px);color:#33374a;max-width:56ch}
.su-task b{font-weight:700;color:var(--su-ink)}
.su-task__side{border-left:3px solid transparent;border-image:var(--su-grad) 1;
 padding-left:clamp(18px,2.4vw,28px)}
.su-task__side h3{font-size:clamp(18px,1.8vw,22px);font-weight:600}
.su-task__side ul{margin:14px 0 0;padding:0;list-style:none;display:grid;gap:12px}
.su-task__side li{font-size:15.5px;color:#33374a;padding-left:22px;position:relative}
.su-task__side li::before{content:"";position:absolute;left:0;top:.62em;width:10px;height:2px;
 background:var(--su-orange)}
.su-quote{margin:clamp(32px,4.5vw,54px) 0 0;padding:clamp(24px,3.4vw,40px) 0;
 border-top:1px solid var(--su-line);border-bottom:1px solid var(--su-line);
 font-family:var(--su-df);font-weight:300;font-size:clamp(20px,2.8vw,34px);line-height:1.16;
 letter-spacing:-.01em;max-width:26ch}
.su-quote span{background:var(--su-grad);-webkit-background-clip:text;background-clip:text;color:transparent}

/* ── ИДЕЯ: ШТОРКА ── */
.su-idea{background:var(--su-bg);padding:clamp(56px,7vw,100px) 0}
.su-idea h2{font-size:clamp(26px,3.4vw,44px);margin-top:14px;max-width:18ch}
.su-idea__lede{margin:18px 0 0;max-width:58ch;color:#33374a;font-size:clamp(15.5px,1.3vw,17.5px)}
/* оба кадра из презентации маленькие (800×568 и 522×365), поэтому шторку
   держим в 900 px: во всю ширину полосы они бы заметно мылили */
.su-ba{position:relative;overflow:hidden;background:#000;aspect-ratio:3/2;
 max-width:900px;margin:clamp(26px,3.4vw,44px) 0 0;touch-action:pan-y}
.su-ba img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.su-ba__top{clip-path:inset(0 0 0 var(--x,52%))}
/* ручка шторки нарисована как разрез стены: два листа, каркас и вата между ними */
.su-ba__line{position:absolute;top:0;bottom:0;left:var(--x,52%);width:18px;
 transform:translateX(-9px);pointer-events:none;
 background:linear-gradient(90deg,#f1eeea 0 22%,#a9a89f 22% 34%,#C8912F 34% 66%,
  #a9a89f 66% 78%,#f1eeea 78% 100%);box-shadow:0 0 0 1px rgba(0,0,0,.35)}
.su-ba__line::after{content:"";position:absolute;top:50%;left:50%;width:46px;height:46px;
 transform:translate(-50%,-50%);border-radius:50%;border:2px solid #fff;
 background:rgba(21,24,29,.62)}
.su-ba input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;margin:0}
.su-ba figcaption{position:absolute;left:0;right:0;bottom:0;display:flex;
 justify-content:space-between;padding:12px 14px;pointer-events:none}
.su-ba figcaption span{background:rgba(16,18,22,.72);color:#fff;padding:5px 11px;
 font:600 12px/1.2 var(--su-bf);letter-spacing:.04em;text-transform:uppercase}
.su-idea__after{margin:clamp(20px,2.6vw,30px) 0 0;max-width:56ch;font-size:clamp(16px,1.4vw,19px)}
.su-idea__after b{font-weight:700}

/* ── ДВЕ СТОРОНЫ ── */
.su-sides{padding:clamp(56px,7vw,100px) 0}
.su-sides h2{font-size:clamp(26px,3.4vw,44px);margin-top:14px;max-width:18ch}
.su-sides__lede{margin:18px 0 0;max-width:58ch;color:#33374a;font-size:clamp(15.5px,1.3vw,17.5px)}
.su-tabs{display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(24px,3vw,36px)}
.su-tabs button{cursor:pointer;background:transparent;border:2px solid var(--su-line);
 color:var(--su-ink2);padding:9px 20px;border-radius:999px;font:700 13.5px var(--su-bf);
 transition:background .2s,border-color .2s,color .2s}
.su-tabs button:hover{border-color:var(--su-ink)}
.su-tabs button[aria-selected=true]{background:var(--su-ink);border-color:var(--su-ink);color:#fff}
.su-side{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(24px,4vw,56px);
 align-items:center;margin-top:clamp(22px,3vw,34px)}
.su-side[hidden]{display:none}
.su-shot{position:relative}
.su-shot img{width:100%}
/* оверлей стоит на самой панели, а не на всём кадре: сверху ручка, снизу тень */
.su-anat{position:absolute;left:2.75%;top:10.91%;width:94.4%;height:89.1%;opacity:0;
 transition:opacity .4s;pointer-events:none}
.su-shot img{transition:filter .4s}
.su-shot.is-anat img{filter:brightness(.74) saturate(.9)}
.su-shot.is-anat .su-anat{opacity:1}
.su-side h3{font-family:var(--su-df);font-weight:300;font-size:clamp(23px,2.6vw,34px);
 letter-spacing:-.01em}
.su-side h3::before{content:"«"}.su-side h3::after{content:"»"}
.su-side__t p{margin:16px 0 0;font-size:16px;color:#33374a;max-width:44ch}
.su-anatbtn{margin-top:22px;background:transparent;border:1px solid var(--su-line);
 border-radius:999px;padding:9px 18px;cursor:pointer;font:600 13px var(--su-bf);
 color:var(--su-ink);transition:border-color .2s,background .2s}
.su-anatbtn:hover{border-color:var(--su-ink)}
.su-anatbtn[aria-pressed=true]{background:var(--su-ink);border-color:var(--su-ink);color:#fff}
.su-sides__note{margin:clamp(22px,2.6vw,30px) 0 0;font-size:15px;color:var(--su-ink2);max-width:62ch}

/* ── ТОРЕЦ ── */
.su-edge{background:var(--su-ink);color:#fff;padding:clamp(56px,7vw,100px) 0}
.su-edge .su-kick{color:rgba(255,255,255,.6)}
.su-edge h2{font-size:clamp(26px,3.4vw,44px);margin-top:14px;max-width:16ch}
.su-edge__lede{margin:18px 0 0;max-width:56ch;color:rgba(255,255,255,.74);
 font-size:clamp(15.5px,1.3vw,17.5px)}
.su-edge__grid{display:grid;grid-template-columns:.42fr .58fr;gap:clamp(24px,4vw,56px);
 align-items:center;margin-top:clamp(26px,3.4vw,44px)}
/* фотография торца и его схема стоят рядом одного роста и в одной пропорции */
.su-cut{display:flex;gap:clamp(16px,2.6vw,30px);align-items:stretch;
 justify-content:center;height:clamp(260px,32vw,380px)}
.su-cut__ph{width:clamp(62px,7vw,88px);object-fit:cover;height:100%}
.su-cut svg{height:100%;width:auto;overflow:visible}
.su-cut__seg{cursor:pointer;transition:opacity .25s}
.su-cut__seg:hover{opacity:.82}
.su-cut__pin{transition:opacity .25s}
.su-layers{display:grid;gap:1px;background:rgba(255,255,255,.16);
 border:1px solid rgba(255,255,255,.16)}
.su-layer{background:var(--su-ink);border:0;text-align:left;cursor:pointer;padding:16px 18px;
 display:grid;grid-template-columns:30px 1fr;gap:12px;font-family:inherit;color:#fff;
 transition:background .2s}
.su-layer:hover,.su-layer[aria-pressed=true]{background:#22262e}
.su-layer i{font-style:normal;font-family:var(--su-mf);font-size:12px;
 color:rgba(255,255,255,.5);padding-top:3px}
.su-layer[aria-pressed=true] i{color:var(--su-wool)}
.su-layer b{display:block;font:600 16px var(--su-bf);margin-bottom:4px}
.su-layer p{margin:0;font-size:14.5px;color:rgba(255,255,255,.66);line-height:1.5}
.su-props{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2.4vw,28px);
 margin-top:clamp(30px,4vw,54px);padding-top:clamp(24px,3vw,36px);
 border-top:1px solid rgba(255,255,255,.16);list-style:none}
.su-props h3{font-family:var(--su-mf);font-weight:700;font-size:11.5px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--su-wool)}
.su-props p{margin:10px 0 0;font-size:15px;color:rgba(255,255,255,.72)}

/* ── ВЫБОР КОНЦЕПЦИИ ── */
.su-alt{padding:clamp(56px,7vw,100px) 0}
.su-alt h2{font-size:clamp(26px,3.4vw,44px);margin-top:14px;max-width:16ch}
.su-alt__lede{margin:18px 0 0;max-width:58ch;color:#33374a;font-size:clamp(15.5px,1.3vw,17.5px)}
.su-alt__grid{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(24px,4vw,56px);
 align-items:center;margin-top:clamp(22px,3vw,34px)}
.su-alt__pane[hidden]{display:none}
.su-alt__pic{position:relative}
.su-alt__pic img{width:100%}
/* «подмена бренда»: плашку логотипов замыливаем, координаты сняты с макетов */
.su-hide{position:absolute;opacity:0;transition:opacity .35s;
 backdrop-filter:blur(9px);-webkit-backdrop-filter:blur(9px);
 background:rgba(255,255,255,.12);box-shadow:0 0 0 1px rgba(21,24,29,.15)}
.su-alt__pic.is-hidden .su-hide{opacity:1}
.su-alt h3{font-size:clamp(22px,2.4vw,30px);font-weight:300}
.su-alt__t p{margin:16px 0 0;font-size:16px;color:#33374a;max-width:46ch}
.su-alt__t p b{font-weight:700}
.su-badge{display:inline-flex;align-items:center;gap:8px;margin-bottom:14px;
 font:700 11.5px var(--su-mf);letter-spacing:.1em;text-transform:uppercase;
 color:var(--su-wine);border:1px solid currentColor;border-radius:999px;padding:5px 12px}
.su-alt__ctrl{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}

/* ── СЦЕНАРИЙ ── */
.su-meet{background:var(--su-bg);padding:clamp(56px,7vw,100px) 0}
.su-meet h2{font-size:clamp(26px,3.4vw,44px);margin-top:14px;max-width:16ch}
.su-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--su-line);
 border:1px solid var(--su-line);margin-top:clamp(26px,3.4vw,44px);padding:0;list-style:none}
.su-steps li{background:#fff;padding:clamp(22px,2.6vw,32px)}
.su-steps b{display:block;font-family:var(--su-df);font-weight:300;
 font-size:clamp(30px,3.6vw,44px);line-height:1;color:var(--su-orange);
 letter-spacing:-.02em;margin-bottom:14px}
.su-steps h3{font-size:19px;font-weight:600;font-family:var(--su-bf)}
.su-steps p{margin:10px 0 0;font-size:15px;color:#33374a}

/* ── РЕЗУЛЬТАТ ── */
.su-res{padding:clamp(56px,7vw,100px) 0}
.su-res__grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(28px,5vw,66px);align-items:start}
.su-res h2{font-size:clamp(26px,3.4vw,44px);margin-top:14px}
.su-res__more{margin:20px 0 0;font-size:16px;color:#33374a;max-width:42ch}
.su-res__more a{font-weight:700;color:var(--su-blue);text-decoration:underline;
 text-underline-offset:3px}
.su-brands{display:flex;align-items:center;gap:clamp(18px,3vw,34px);flex-wrap:wrap;
 margin-top:clamp(24px,3vw,34px);padding-top:clamp(20px,2.4vw,28px);
 border-top:1px solid var(--su-line)}
.su-brands img{height:clamp(22px,2.4vw,30px);width:auto;opacity:.8}
.su-brands img.sg{height:clamp(34px,3.6vw,46px)}
.su-res__list{list-style:none;margin:0;padding:0;display:grid;gap:clamp(14px,2vw,22px)}
.su-res__list li{display:grid;grid-template-columns:auto 1fr;gap:clamp(14px,2vw,22px);
 align-items:start;border-top:1px solid var(--su-line);padding-top:clamp(14px,2vw,20px)}
.su-num{font-family:var(--su-df);font-weight:300;font-variant-numeric:tabular-nums;
 font-size:clamp(30px,3.6vw,46px);line-height:1;letter-spacing:-.02em;min-width:2ch;
 color:var(--su-wine)}
.su-res__list li:nth-child(2) .su-num{color:var(--su-orange)}
.su-res__list li:nth-child(3) .su-num{color:var(--su-blue)}
.su-res__list li:nth-child(4) .su-num{color:var(--su-blue2)}
.su-res__list span:last-child{font-size:15.5px;color:#33374a}
.su-res__list b{color:var(--su-ink);font-weight:700}

/* появление */
html.no-js .su-r{opacity:1!important;transform:none!important}
.su-r{opacity:0;transform:translateY(22px);
 transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.su-r.is-in{opacity:1;transform:none}

/* ── АДАПТИВ ── */
@media(max-width:1020px){
 .su-hero__grid,.su-task__grid,.su-side,.su-edge__grid,.su-alt__grid,
 .su-res__grid{grid-template-columns:1fr;gap:28px}
 .su-spec__in{grid-template-columns:repeat(2,1fr)}
 .su-steps{grid-template-columns:1fr}
 .su-props{grid-template-columns:1fr;gap:20px}
 .su-stage{--bw:clamp(240px,62vw,440px)}
}
@media(max-width:680px){
 .su{font-size:16px}
 .su-cut{height:clamp(240px,58vw,300px)}
 .su-ba{aspect-ratio:4/3}
}
@media(max-width:420px){
 .su-spec__in{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){
 .su-r{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .su *{transition-duration:.01ms!important;scroll-behavior:auto}
}
</style>""".replace('IMGSRC', IMG)

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Проектный чемодан Saint-Gobain: концепция «Две комнаты» | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: дизайн проектного чемодана Saint-Gobain с образцами Gyproc и ISOVER. Концепция «Две комнаты»: снаружи чемодан работает как фрагмент стены, у которого две стороны (ремонт и тишина) и разрез по торцу со схемой сборки.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Проектный чемодан Saint-Gobain | кейс Hand Marketing">
<meta property="og:description" content="Концепция «Две комнаты»: у чемодана две стороны и разрез по торцу, как у настоящей стены. Ремонт с одной стороны, детский сон с другой.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/view-front.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/raleway.css" rel="stylesheet"><link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def hero():
    chips = ''.join(f'<li>{c}</li>' for c in (
        'Название', 'Дизайн трёх граней', 'Сюжет', 'Сценарий презентации', 'Две концепции'))
    spec = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in (
        ('2019', 'год проекта'),
        ('3', 'бренда в одном носителе'),
        ('2', 'стороны, два разговора'),
        ('1', 'разрез по торцу'),
    ))
    stops = ''.join(
        f'<button type="button" data-a="{a}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'{t}</button>' for i, (a, t) in enumerate(
            ((18, 'Ремонт'), (90, 'Стена'), (162, 'Тишина'))))
    # 21 полоса шумовой дорожки, коэффициент высоты у каждой свой
    ks = (.35, .62, .9, .55, 1, .72, .44, .86, .6, 1, .78, .5, .93, .66, 1, .58, .82, .4, .7, .48, .3)
    bars = ''.join(f'<i style="--k:{k}"></i>' for k in ks)
    return (
      '<header class="su-hero"><div class="su-w">'
      '<div class="su-hero__grid">'
      '<div class="su-r">'
      f'<div class="su-hero__client"><img src="{IMG}/logo-sg.png" alt="Saint-Gobain" '
      'width="959" height="401"><span>Проектный чемодан<br>Gyproc и ISOVER</span></div>'
      '<h1>Две комнаты и <b>стена</b> между ними</h1>'
      '<p class="su-hero__sub">Торговый представитель Saint-Gobain приезжает к '
      'проектировщикам и подрядчикам с чемоданом образцов. Мы сделали так, что чемодан '
      'начинает работать раньше, чем его откроют: снаружи это фрагмент стены, у которого '
      'есть две стороны и разрез по торцу.</p>'
      f'<ul class="su-chips">{chips}</ul>'
      '<div class="su-hero__cta">'
      f'<a class="su-btn su-btn--p" href="#su-edge">Смотреть разрез {ARROW}</a>'
      '<a class="su-btn su-btn--gh" href="#su-alt">Была и вторая концепция</a>'
      '</div></div>'
      '<div class="su-r">'
      '<div class="su-stage" id="su-stage">'
      '<div class="su-box" id="su-box" role="img" aria-label="Проектный чемодан '
      'Saint-Gobain: красная лицевая сторона, торец с разрезом стены и синий оборот">'
      '<div class="su-f-front"></div><div class="su-f-back"></div>'
      '<div class="su-f-r"></div><div class="su-f-l"></div><div class="su-f-t"></div>'
      '</div><div class="su-shadow"></div></div>'
      '<div class="su-ctrl">'
      f'<div class="su-ctrl__row" id="su-stops">{stops}</div>'
      '<input type="range" id="su-angle" min="0" max="180" value="18" step="1" '
      'aria-label="Поворот чемодана: от лицевой стороны через торец к обороту">'
      f'<div class="su-noise" id="su-noise" aria-hidden="true">{bars}</div>'
      '<p class="su-cap" id="su-cap"><b>За стенкой идёт ремонт.</b> '
      'Поверните чемодан мышью или ползунком.</p>'
      '</div></div>'
      '</div></div>'
      f'<div class="su-spec"><div class="su-spec__in">{spec}</div></div>'
      '</header>')


def task():
    side = ''.join(f'<li>{t}</li>' for t in (
      'Один носитель на три темы сразу: звукоизоляция, внутренняя облицовка, огнезащита.',
      'Простая конструкция, чтобы чемодан можно было быстро запустить в производство.',
      'Макет про конкретные бренды, а не универсальная картинка, к которой подойдёт '
      'любой логотип.',
      'Ёмкое название, которое останется в памяти после встречи.',
    ))
    return (
      '<section class="su-task"><div class="su-w">'
      '<div class="su-task__grid">'
      '<div class="su-r"><span class="su-kick">Задача</span>'
      '<h2>Носитель для разговора с профессионалами</h2>'
      '<p>Чемодан собирали для проектного строительства. Внутри образцы гипсовых плит, '
      'металлического профиля и звукоизоляции плюс печатные каталоги, а приходят с ним '
      'к тем, кто выбирает материалы задолго до стройки: к проектировщикам, девелоперам, '
      'подрядчикам и дистрибьюторам.</p>'
      '<p>Эта аудитория знает продукт лучше любой рекламы, поэтому показывать ей плиту '
      'бессмысленно: таких плит они видели тысячи. Показывать нужно <b>задачу, которую '
      'плита решает</b>, и укладываться в те несколько секунд, пока чемодан ставят '
      'на стол.</p>'
      '</div>'
      '<div class="su-task__side su-r"><h3>Условия</h3>'
      f'<ul>{side}</ul></div></div>'
      '<p class="su-quote su-r">Конструкцию мы упростили до предела, а все креативные '
      'силы отдали тому, что <span>напечатано снаружи</span>.</p>'
      '</div></section>')


def idea():
    return (
      '<section class="su-idea"><div class="su-w">'
      '<div class="su-r"><span class="su-kick">Идея</span>'
      '<h2>Ремонт за стенкой понятен каждому</h2>'
      '<p class="su-idea__lede">Ощущения и звуки возникают при одной только мысли о нём. '
      'Мы взяли этот общий опыт точкой входа: в нём уже есть и проблема, и продукт, '
      'и результат, объяснять ничего не нужно.</p></div>'
      # спящий ребёнок стоит слева своего кадра, а мужчина с перфоратором справа
      # своего, поэтому тихая комната лежит нижним слоем, а ремонт наезжает справа:
      # при любом положении шторки в кадре виден и тот, и другой
      '<figure class="su-ba su-r" id="su-ba">'
      f'<img src="{IMG}/room-sleep.jpg" alt="Младенец спит в кроватке в полумраке '
      'детской комнаты" loading="lazy" width="522" height="365">'
      f'<img class="su-ba__top" src="{IMG}/room-work.jpg" alt="Мужчина сверлит '
      'перфоратором бетонную стену в комнате во время ремонта" loading="lazy" '
      'width="800" height="568">'
      '<span class="su-ba__line"></span>'
      '<input type="range" min="0" max="100" value="48" id="su-ba-x" '
      'aria-label="Шторка: с одной стороны стены тишина, с другой ремонт">'
      '<figcaption><span>За стенкой тихо</span><span>За стенкой ремонт</span></figcaption>'
      '</figure>'
      '<p class="su-idea__after su-r">Но может ли быть так, что за стенкой царит покой '
      'и ничего не тревожит детский сон? <b>Ответ на этот вопрос и стал сюжетом '
      'чемодана.</b></p>'
      '</div></section>')


def anatomy(kind):
    """Оверлей разбора стороны: диагональ, поле названия и плашка брендов.

    Кадр из презентации это не только панель: сверху ручка, снизу тень. Панель
    внутри кадра занимает 2.75% слева, 10.91% сверху, 94.4% ширины и 89.1%
    высоты (замерено по обоим видам, они совпадают), поэтому оверлей стоит
    именно на этой области, а не на всём кадре.

    Внутри координаты панельные: viewBox 100×74 (панель 1236×915). Диагональ
    снята с самих макетов: и на лицевой, и на обороте цветной клин уходит из
    48% высоты у левого края в 22% у правого, то есть линия у обеих сторон
    одна и та же."""
    y0, y1 = 74 * .48, 74 * .22
    # поле названия замерено по самому макету: на обороте под фразой стоит ещё
    # абзац про компанию, поэтому блок ниже
    nx, ny, nw, nh = (4, 7, 48, 18.5) if kind == 'front' else (3.5, 7, 49, 21)
    plot = ('сюжет: как эту стену ставят' if kind == 'front'
            else 'сюжет: как за этой стеной живут')
    return (
      '<svg class="su-anat" viewBox="0 0 100 74" preserveAspectRatio="none" '
      'aria-hidden="true">'
      '<g fill="none" stroke="#fff" vector-effect="non-scaling-stroke" opacity=".95">'
      f'<path d="M0,{y0:.1f} L100,{y1:.1f}" stroke-width="1.4"/>'
      f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" stroke-width="1" '
      'stroke-dasharray="4 4"/>'
      '<rect x="81.3" y="47.4" width="15.9" height="22.4" stroke-width="1" '
      'stroke-dasharray="4 4"/>'
      '</g>'
      # подписи ложатся и на светлый кадр, и на цветной клин, поэтому у них
      # тёмная обводка: без неё белый текст пропадает на белой стене
      '<g fill="#fff" stroke="#15181d" stroke-width=".9" paint-order="stroke" '
      'stroke-linejoin="round" font-family="monospace" font-size="2.4">'
      f'<text x="{nx}" y="{ny - 1.6:.1f}">поле названия</text>'
      '<text x="97.2" y="45.6" text-anchor="end">плашка брендов</text>'
      f'<text x="20" y="{y0 - .192 * 20 - 3:.1f}">диагональ повторяет разрез стены</text>'
      f'<text x="6" y="66">{plot}</text>'
      '</g></svg>')


def sides():
    tabs = ''.join(
      f'<button type="button" role="tab" id="tab-{k}" aria-controls="pane-{k}" '
      f'aria-selected="{"true" if i == 0 else "false"}">{H.escape(cap)}</button>'
      for i, (k, f, cap, title, text, alt) in enumerate(SIDES))
    panes = ''
    for i, (k, f, cap, title, text, alt) in enumerate(SIDES):
        panes += (
          f'<div class="su-side" id="pane-{k}" role="tabpanel" aria-labelledby="tab-{k}"'
          f'{"" if i == 0 else " hidden"}>'
          f'<div class="su-shot" data-shot="{k}">'
          f'<img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" loading="lazy" '
          f'width="1310" height="1027">{anatomy(k)}</div>'
          f'<div class="su-side__t"><h3>{H.escape(title)}</h3><p>{text}</p>'
          f'<button class="su-anatbtn" type="button" data-anat="{k}" aria-pressed="false">'
          'Показать разбор</button></div>'
          '</div>')
    return (
      '<section class="su-sides"><div class="su-w">'
      '<div class="su-r"><span class="su-kick">Две стороны</span>'
      '<h2>Один предмет, два разных разговора</h2>'
      '<p class="su-sides__lede">Обе стороны напечатаны на одном чемодане, и показывают '
      'их по очереди. Сначала ту, что про работу, потом ту, что про результат.</p></div>'
      f'<div class="su-tabs su-r" id="su-tabs" role="tablist" '
      f'aria-label="Стороны чемодана">{tabs}</div>'
      f'<div class="su-r">{panes}</div>'
      '<p class="su-sides__note">Диагональ делит плоскость так же, как разрез делит стену: '
      'выше линии обещание, ниже сюжет. Плашка с тремя логотипами на обеих сторонах стоит '
      'на одном месте, поэтому чемодан читается как один предмет, а не как две разные '
      'печатные плоскости.</p>'
      '</div></section>')


def edge():
    # живой разрез: четыре слоя в ряд, ширина каждого пропорциональна реальной
    W, HGT, x = 100.0, 200.0, 0.0
    segs, pins = '', ''
    for i, (k, frac, fill, name, text) in enumerate(LAYERS):
        w = W * frac
        segs += (f'<rect class="su-cut__seg" data-seg="{k}" x="{x:.2f}" y="0" '
                 f'width="{w:.2f}" height="{HGT}" fill="{fill}" '
                 f'stroke="#15181d" stroke-width=".5"><title>{H.escape(name)}</title></rect>')
        pins += (f'<g class="su-cut__pin" data-pin="{k}" opacity="{1 if i == 0 else 0}">'
                 f'<rect x="{x:.2f}" y="0" width="{w:.2f}" height="{HGT}" fill="none" '
                 'stroke="#fff" stroke-width="2"/>'
                 f'<text x="{x + w / 2:.2f}" y="-5" fill="#fff" text-anchor="middle" '
                 f'font-family="monospace" font-size="9">{i + 1:02d}</text></g>')
        x += w
    layers = ''.join(
      f'<button class="su-layer" type="button" data-layer="{k}" '
      f'aria-pressed="{"true" if i == 0 else "false"}">'
      f'<i>{i + 1:02d}</i><span><b>{H.escape(name)}</b><p>{text}</p></span></button>'
      for i, (k, frac, fill, name, text) in enumerate(LAYERS))
    props = ''.join(f'<li><h3>{H.escape(t)}</h3><p>{d}</p></li>' for t, d in PROPS)
    return (
      '<section class="su-edge" id="su-edge"><div class="su-w">'
      '<div class="su-r"><span class="su-kick">Торец</span>'
      '<h2>Разрез стены, который берут в руку</h2>'
      '<p class="su-edge__lede">На торцах напечатана та самая стена в разрезе: два листа, '
      'каркас и звукоизоляция между ними. Пока чемодан ставят на стол, собеседник уже '
      'видит схему сборки, и её не нужно объяснять словами.</p></div>'
      '<div class="su-edge__grid">'
      '<div class="su-cut su-r">'
      f'<img class="su-cut__ph" src="{IMG}/face-edge.jpg" alt="Торец чемодана '
      'Saint-Gobain с напечатанным разрезом стены: гипсовые плиты, металлический профиль '
      'и минеральная вата" loading="lazy" width="392" height="914">'
      f'<svg viewBox="0 -14 100 214" role="group" aria-label="Схема разреза стены">'
      '<defs>'
      '<linearGradient id="su-gyp" x1="0" x2="1"><stop offset="0" stop-color="#f4f1ed"/>'
      '<stop offset="1" stop-color="#ddd8d1"/></linearGradient>'
      '<linearGradient id="su-met" x1="0" x2="1"><stop offset="0" stop-color="#b8b7ae"/>'
      '<stop offset="1" stop-color="#8f8e86"/></linearGradient>'
      '<linearGradient id="su-wool" x1="0" x2="1"><stop offset="0" stop-color="#e0b45c"/>'
      '<stop offset=".5" stop-color="#C8912F"/><stop offset="1" stop-color="#dcae55"/>'
      '</linearGradient></defs>'
      f'{segs}{pins}</svg></div>'
      f'<div class="su-layers su-r" id="su-layers">{layers}</div>'
      '</div>'
      f'<ul class="su-props su-r">{props}</ul>'
      '</div></section>')


def alt():
    return (
      '<section class="su-alt" id="su-alt"><div class="su-w">'
      '<div class="su-r"><span class="su-kick">Выбор</span>'
      '<h2>Была и вторая концепция</h2>'
      '<p class="su-alt__lede">Клиенту показали две. Вторая, «Стартовая площадка», '
      'строилась на метафоре: космодром требует той же прочности и огнестойкости, что '
      'и стена из этих материалов. Кадр сильный, но метафора живёт отдельно от продукта.</p>'
      '</div>'
      '<div class="su-tabs su-r" id="su-alt-tabs" role="tablist" aria-label="Концепции">'
      '<button type="button" role="tab" id="tab-c1" aria-controls="pane-c1" '
      'aria-selected="true">Две комнаты</button>'
      '<button type="button" role="tab" id="tab-c2" aria-controls="pane-c2" '
      'aria-selected="false">Стартовая площадка</button></div>'
      '<div class="su-r">'
      '<div class="su-alt__grid su-alt__pane" id="pane-c1" role="tabpanel" '
      'aria-labelledby="tab-c1">'
      '<div class="su-alt__pic" data-pic>'
      f'<img src="{IMG}/view-front.jpg" alt="Концепция «Две комнаты»: лицевая сторона '
      'чемодана с монтажом стены" loading="lazy" width="1310" height="1027">'
      '<span class="su-hide" style="left:79.5%;top:68%;width:15%;height:27%"></span></div>'
      '<div class="su-alt__t"><span class="su-badge">В тираже</span>'
      '<h3>Две комнаты</h3>'
      '<p>Сюжет собран из самих материалов: в кадре каркас, вата, плиты и человек, '
      'который их ставит. <b>Закройте плашку с логотипами, и принадлежность макета '
      'никуда не денется</b>: другой бренд в эту картинку просто не встанет.</p></div>'
      '</div>'
      '<div class="su-alt__grid su-alt__pane" id="pane-c2" role="tabpanel" '
      'aria-labelledby="tab-c2" hidden>'
      '<div class="su-alt__pic" data-pic>'
      f'<img src="{IMG}/alt-space.jpg" alt="Концепция «Стартовая площадка»: чемодан '
      'с фотографией старта шаттла и разрезом стены по нижнему краю" loading="lazy" '
      'width="1400" height="1100">'
      '<span class="su-hide" style="left:79.5%;top:66.5%;width:13.5%;height:29.5%"></span></div>'
      '<div class="su-alt__t">'
      '<h3>Стартовая площадка</h3>'
      '<p>Здесь работает эмоция и общее слово «качество», а разрез стены уходит в узкую '
      'полосу внизу. <b>Закройте плашку, и макет перестанет принадлежать кому-либо '
      'конкретно</b>: старт шаттла подошёл бы почти любому производителю.</p></div>'
      '</div></div>'
      '<div class="su-alt__ctrl su-r">'
      '<button class="su-btn su-btn--gh" type="button" id="su-hide" aria-pressed="false">'
      'Скрыть логотипы</button></div>'
      '<p class="su-sides__note">Проверка простая: если под плашкой остаётся сюжет, '
      'собранный из самих материалов, макет принадлежит бренду. Если остаётся только '
      'красивая картинка, её можно отдать кому угодно. В производство пошли '
      '«Две комнаты».</p>'
      '</div></section>')


def meeting():
    steps = ''.join(
      f'<li><b>{n}</b><h3>{H.escape(t)}</h3><p>{d}</p></li>' for n, t, d in STEPS)
    return (
      '<section class="su-meet"><div class="su-w">'
      '<div class="su-r"><span class="su-kick">Сценарий</span>'
      '<h2>Как чемодан работает на встрече</h2></div>'
      f'<ul class="su-steps su-r">{steps}</ul>'
      '</div></section>')


def result():
    items = [
      ('3', '<b>Три грани с законченной коммуникацией</b>: лицевая про работу, оборот '
       'про результат, торец про то, как эта стена устроена.'),
      ('1', '<b>Одно название</b>, «Стены с качеством», которое закрывает сразу три темы '
       'и остаётся в памяти после встречи.'),
      ('2', '<b>Две концепции на выбор</b>, обе доведены до макета. В производство ушла '
       'первая.'),
      ('3', '<b>Три бренда в одном носителе</b>: Saint-Gobain, Gyproc и ISOVER стоят '
       'на обеих сторонах в одной плашке.'),
    ]
    lis = ''.join(f'<li><span class="su-num">{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="su-res"><div class="su-w su-res__grid">'
      '<div class="su-r"><span class="su-kick">Результат</span>'
      '<h2>Что вошло в проект</h2>'
      '<p class="su-res__more">Проект 2019 года. Больше о направлении: '
      '<a href="/creativedesign">услуга «Creative&nbsp;&amp;&nbsp;Design»</a>. '
      'Ещё один проект для этого клиента: '
      '<a href="/creative/saintgobain/calendar">концепция новогоднего календаря '
      'Saint-Gobain</a>.</p>'
      '<div class="su-brands">'
      f'<img class="sg" src="{IMG}/logo-sg.png" alt="Saint-Gobain" width="959" height="401">'
      f'<img src="{IMG}/logo-gyproc.png" alt="Gyproc" width="1298" height="444">'
      f'<img src="{IMG}/logo-isover.png" alt="ISOVER" width="511" height="164">'
      '</div></div>'
      f'<ul class="su-res__list su-r">{lis}</ul>'
      '</div></section>')


PAGE_JS = """<script>(function(){
 // ── поворот чемодана: ползунок, кнопки, перетаскивание
 var box=document.getElementById('su-box'),stage=document.getElementById('su-stage'),
     rng=document.getElementById('su-angle'),stops=document.getElementById('su-stops'),
     noise=document.getElementById('su-noise'),cap=document.getElementById('su-cap'),
     ang=18;
 function words(a){
  if(a<52)return '<b>За стенкой идёт ремонт.</b> Поверните чемодан мышью или ползунком.';
  if(a<128)return '<b>Между вами стена.</b> На торце напечатан её разрез: два листа, каркас и вата.';
  return '<b>За стенкой тихо.</b> Та же стена с другой стороны, и в кадре ни одного материала.';
 }
 function apply(a,anim){
  ang=Math.max(0,Math.min(180,a));
  if(box){box.classList.toggle('is-drag',!anim);box.style.setProperty('--a',ang);}
  var loud=(1+Math.cos(ang*Math.PI/180))/2;
  if(noise){noise.style.setProperty('--loud',loud.toFixed(3));
   noise.classList.toggle('is-quiet',ang>90);}
  if(cap)cap.innerHTML=words(ang);
  if(rng&&+rng.value!==Math.round(ang))rng.value=Math.round(ang);
  if(stops)[].forEach.call(stops.querySelectorAll('button'),function(b){
   b.setAttribute('aria-pressed',String(Math.abs(+b.getAttribute('data-a')-ang)<9));});
 }
 if(box){
  apply(18,true);
  if(rng)rng.addEventListener('input',function(){apply(+rng.value,false);});
  if(stops)stops.addEventListener('click',function(e){
   var b=e.target.closest('button');if(!b)return;apply(+b.getAttribute('data-a'),true);});
  // перетаскивание: 180 градусов примерно на ширину сцены
  var drag=false,x0=0,a0=0;
  box.addEventListener('pointerdown',function(e){
   drag=true;x0=e.clientX;a0=ang;
   if(box.setPointerCapture)try{box.setPointerCapture(e.pointerId);}catch(err){}
   e.preventDefault();});
  box.addEventListener('pointermove',function(e){
   if(!drag)return;
   var w=(stage&&stage.offsetWidth)||420;
   apply(a0+(e.clientX-x0)/w*200,false);});
  ['pointerup','pointercancel','pointerleave'].forEach(function(t){
   box.addEventListener(t,function(){if(drag){drag=false;box.classList.remove('is-drag');}});});
 }
 // ── шторка «ремонт / тишина»
 var ba=document.getElementById('su-ba'),bax=document.getElementById('su-ba-x');
 if(ba&&bax){var setx=function(){ba.style.setProperty('--x',bax.value+'%');};
  bax.addEventListener('input',setx);setx();}
 // ── вкладки (стороны чемодана и концепции)
 function tabs(id){
  var t=document.getElementById(id);if(!t)return;
  var tb=[].slice.call(t.querySelectorAll('button'));
  tb.forEach(function(b){b.addEventListener('click',function(){
   tb.forEach(function(o){
    var on=o===b;o.setAttribute('aria-selected',String(on));
    var p=document.getElementById(o.getAttribute('aria-controls'));
    if(p)p.hidden=!on;});});});
  t.addEventListener('keydown',function(e){
   var i=tb.indexOf(document.activeElement);if(i<0)return;
   var n=e.key==='ArrowRight'?i+1:e.key==='ArrowLeft'?i-1:-1;
   if(n<0)return;e.preventDefault();n=(n+tb.length)%tb.length;tb[n].focus();tb[n].click();});
 }
 tabs('su-tabs');tabs('su-alt-tabs');
 // ── разбор стороны
 [].forEach.call(document.querySelectorAll('[data-anat]'),function(b){
  b.addEventListener('click',function(){
   var on=b.getAttribute('aria-pressed')!=='true';
   b.setAttribute('aria-pressed',String(on));
   b.textContent=on?'Убрать разбор':'Показать разбор';
   var s=document.querySelector('[data-shot="'+b.getAttribute('data-anat')+'"]');
   if(s)s.classList.toggle('is-anat',on);});});
 // ── слои разреза: кнопки и сегменты синхронны
 var lay=document.getElementById('su-layers');
 if(lay){
  var btns=[].slice.call(lay.querySelectorAll('[data-layer]')),
      pins=[].slice.call(document.querySelectorAll('[data-pin]'));
  function pick(k){
   btns.forEach(function(b){b.setAttribute('aria-pressed',
    String(b.getAttribute('data-layer')===k));});
   pins.forEach(function(p){p.setAttribute('opacity',p.getAttribute('data-pin')===k?'1':'0');});
  }
  btns.forEach(function(b){b.addEventListener('click',function(){
   pick(b.getAttribute('data-layer'));});});
  [].forEach.call(document.querySelectorAll('[data-seg]'),function(s){
   s.addEventListener('click',function(){
    var k=s.getAttribute('data-seg');pick(k);
    var b=lay.querySelector('[data-layer="'+k+'"]');if(b)b.focus();});});
 }
 // ── проверка на подмену бренда
 var hb=document.getElementById('su-hide');
 if(hb)hb.addEventListener('click',function(){
  var on=hb.getAttribute('aria-pressed')!=='true';
  hb.setAttribute('aria-pressed',String(on));
  hb.textContent=on?'Вернуть логотипы':'Скрыть логотипы';
  [].forEach.call(document.querySelectorAll('[data-pic]'),function(p){
   p.classList.toggle('is-hidden',on);});});
 // ── появление блоков
 var els=[].slice.call(document.querySelectorAll('.su-r'));
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
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Проектный чемодан Saint-Gobain",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="su">{hero()}{task()}{idea()}{sides()}'
            f'{edge()}{alt()}{meeting()}{result()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'saintgobain', 'suitcase')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
