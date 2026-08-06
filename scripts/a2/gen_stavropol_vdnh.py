#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/portfolio/stavropol-stand-vdnh/index.html: кейс «Стенд
Ставропольского края на выставке „Россия“» (ВДНХ, павильон №75, 2023-2024).

Что здесь вместо прежней страницы. Раньше по этому адресу жил остаток старого
React-SPA: shadcn-карточки, плитка придуманных цифр («1 800 000 за первые три
месяца», «∞ виртуальных терренкуров»), секция «Долгосрочное влияние» и список
чипов «Использованные технологии». Страница переписана с нуля по тому, что
реально видно на съёмке и фотографиях.

Идея страницы: у стенда есть один физический принцип, вокруг которого всё
собрано, и это анаморфоза. Изображение на LED-коробе рассчитано под конкретное
место в зале: оттуда сноп колосьев выходит за грань, из любого другого места
объём распадается на плоскости. Поэтому главный блок страницы не картинка, а
работающая схема: слои сцены нормированы по перспективе и сходятся в одну
картинку ровно в расчётной точке (масштаб слоя s = (d - z) / d, где d это
perspective, z это глубина). Сдвигаешь зрителя и видишь, из чего собран объём.
Вторая механика того же рода: бинокуляр на панораме 17 гор-лакколитов КМВ
(круглая линза с увеличением, повторяет зону стенда с бинокулярами).

Цифры: в кейсе только то, что подтверждается. 248 дней работы считаются по
датам выставки, 18 млн посетителей это посещаемость ВСЕЙ выставки, о чём прямо
сказано в тексте. Придуманные метрики прежней страницы не переносятся.

Шрифты Prata + Commissioner, локальные (/fonts/prata-commissioner.css),
кадры и стоп-кадры готовит scripts/stavropol-assets.py.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import html as H
import importlib.util
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/stavropol'          # кадры из съёмки (scripts/stavropol-assets.py)
PHOTO = '/portfolio/stavropol-vdnh'  # фотографии, лежат тут с прошлой версии
MEDIA = '/media'                    # ролики, см. scripts/a2/video_map.json
CLIP = '/videos/stavropol-stand.mp4'  # короткая версия, едет с обычным деплоем
URL = 'https://hand-marketing.ru/portfolio/stavropol-stand-vdnh/'

# ─── паспорт проекта ────────────────────────────────────────────────────────
FACTS = [
    ('Выставка', 'Международная выставка-форум «Россия»'),
    ('Площадка', 'Павильон №75, ВДНХ'),
    ('Работа стенда', '4 ноября 2023 по 8 июля 2024'),
    ('Дней в экспозиции', '248'),
    ('Наша часть', 'Мультимедийное оснащение экспозиции'),
]

# ─── сюжеты на кубе: кадры сняты с 3:41 съёмки, идут одним циклом ────────────
CUBE = [
    ('field',    'Сноп колосьев', 'Единственный кадр, ради которого куб и строили: колосья выходят за переднюю грань.'),
    ('dance',    'Танец', 'Фигура в синем платье стоит над полем, ноги ниже линии экрана.'),
    ('elephant', 'Слон', 'Тот самый южный слон, скелет которого нашли в крае.'),
    ('wings',    'Крылья из колосьев', 'Поле собирается в симметричную фигуру и разлетается.'),
    ('water',    'Вода', 'Поток идёт сверху вниз и продолжается на нижней грани.'),
    ('harvest',  'Уборочная', 'Комбайны едут по кадру поперёк, техника уходит за грань.'),
    ('gate',     'Тифлисские ворота', 'Ставропольская арка 1841 года, ночная подсветка.'),
    ('wind',     'Ветропарк', 'Ветроэнергетика края, лопасти проходят через угол короба.'),
    ('flag',     'Флаг края', 'Полотнище идёт по двум граням сразу.'),
    ('title',    'Заставка', 'Логотип экспозиции «Ставрополье, край для жизни», 2023-2024.'),
]

# ─── маршрут по стенду ──────────────────────────────────────────────────────
# (номер, заголовок, текст, главный кадр+alt, дополнительные кадры)
ZONES = [
    ('01', 'Стекло, за которым живёт картинка',
     ['Прозрачная тач-панель стоит перед большим LED-экраном. Палец ведёт меню по стеклу, '
      'а сцена живёт за ним, в полутора метрах. Интерфейс и картинка оказываются на разной '
      'глубине, поэтому объём читается без очков и без шлема.',
      'На панели показывали жилой квартал в Ставрополе от компании А101: кварталы, '
      'спортивный и образовательный кластеры, транспорт.'],
     (f'{IMG}/glass-panel.jpg', 'Прозрачная тач-панель стенда, за стеклом LED-экран с домом квартала'),
     [(f'{PHOTO}/a101-touch-panel-1.jpg', 'Интерфейс панели: дорожка через двор квартала'),
      (f'{PHOTO}/a101-touch-panel-2.jpg', 'Интерфейс панели: разделы квартала на прозрачном экране'),
      (f'{IMG}/city-panels.jpg', 'Подсвеченные панели с кварталами и кластерами города')]),
    ('02', 'Терренкур, который проезжают сидя',
     ['Терренкур это размеченный маршрут для лечебной ходьбы, ради которого на Кавказские '
      'Минеральные Воды ездят с позапрошлого века. На стенде маршрут проходили на '
      'велотренажёре: педали крутятся, съёмка тропы на экранах едет с той же скоростью, '
      'перестал крутить и пейзаж встал.',
      'Тропы снимали в разные сезоны, поэтому на экранах встречались и осенняя аллея, '
      'и весенний лес на просвет.'],
     (f'{IMG}/terrenkur-bike.jpg', 'Посетитель крутит педали велотренажёра перед экранами с лесной тропой'),
     [(f'{IMG}/terrenkur-road.jpg', 'Кадр съёмки тропы: аллея на просвет'),
      (f'{PHOTO}/terrenkur.jpg', 'Зона терренкура на стенде, велотренажёр и вертикальные экраны')]),
    ('03', 'Картина красками края',
     ['Тач-экран предлагает нарисовать картину красками края. Рисуешь пальцем, готовая '
      'работа встаёт в золотую раму рядом с экраном, а потом уезжает к автору в телефон.',
      'Пока человек рисует, он стоит у стенда: это дольше, чем идёт любой ролик, '
      'и запоминается лучше.'],
     (f'{PHOTO}/gallery-3.jpg', 'Посетительница рисует на тач-экране стенда Ставрополья'),
     [(f'{IMG}/draw-frame.jpg', 'Готовая работа в золотой раме: стела «Я люблю Ставрополь»'),
      (f'{IMG}/draw-phone.jpg', 'Готовая работа открыта на телефоне посетителя')]),
    ('04', 'Слон, на которого ложится свет',
     ['В Ставропольском крае нашли скелет южного слона, отсюда и присказка про родину слонов, '
      'и слон на стенде. Скульптуру оставили белой, чтобы она работала поверхностью для света: '
      'на одних кадрах она белая, на других сиреневая.',
      'Рядом стояли VR-станции, поэтому вокруг слона всё время кто-то был.'],
     (f'{PHOTO}/interactive-elephant.jpg', 'Белая скульптура слона на стенде, рядом посетители в VR-очках'),
     [(f'{PHOTO}/gallery-5.jpg', 'Скульптура слона в сиреневой подсветке'),
      (f'{IMG}/postcard.jpg', 'Экран «С любовью из Ставрополья»')]),
    ('05', 'Зелёный зал',
     ['Мшистые холмы, светящийся источник, звук воды. Место, куда приходят не смотреть, '
      'а сесть и отдышаться после павильона.',
      'По первоначальному эскизу здесь же собирались посадить «Дух ставропольских курортов», '
      'рассказчика на холме.'],
     (f'{IMG}/spirit-hall.jpg', 'Зелёная зона стенда: мшистые холмы и светящийся источник'),
     [(f'{PHOTO}/spirit-installation.jpg', 'Эскиз зоны «Дух ставропольских курортов»'),
      (f'{PHOTO}/gallery-1.jpg', 'Общий вид стенда в дни новогодних праздников')]),
]

# ─── 17 гор-лакколитов КМВ: (имя, высота в метрах) ──────────────────────────
# «недоразвитые вулканы»: магма подняла осадочные слои куполом и застыла внутри
LACCOLITHS = [
    ('Кокуртлы', 406), ('Медовая', 721), ('Лысая', 739), ('Тупая', 772),
    ('Бык', 817), ('Железная', 851), ('Острая', 881), ('Золотой курган', 884),
    ('Верблюд', 885), ('Развалка', 926), ('Бештау', 1401), ('Джуца', 1189),
    ('Змейка', 994), ('Машук', 993), ('Юца', 972), ('Шелудивая', 874),
    ('Кинжал', 507),
]

PAGE_CSS = """<style id="sv-css">
:root{
 --paper:#F6F1E6; --paper-2:#EFE7D6; --ink:#17233B; --ink-2:#4E5972;
 --line:rgba(23,35,59,.16); --orange:#DC6F0B; --gold:#F0AE28;
 --led:#1B62C6; --teal:#2BB6C8; --dark:#0D1422; --dark-2:#131E33;
}
.sv{font-family:'Commissioner',-apple-system,Arial,sans-serif;color:var(--ink);
 background:var(--paper);-webkit-font-smoothing:antialiased;overflow-x:clip}
.sv *{box-sizing:border-box}
.sv img{max-width:100%;height:auto;display:block}
.sv h1,.sv h2,.sv h3{font-family:'Prata',Georgia,serif;font-weight:400;letter-spacing:-.01em;margin:0}
.sv p{margin:0}
.sv__wrap{max-width:1180px;margin:0 auto;padding:0 28px}
.sv__eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--orange)}
.sv__lead{font-size:clamp(17px,1.5vw,20px);line-height:1.6;color:var(--ink-2)}
.sv-sec{padding:clamp(64px,8vw,120px) 0}
.sv-sec__h{font-size:clamp(28px,3.6vw,50px);line-height:1.1;max-width:20ch}
.sv-sec__sub{margin-top:18px;max-width:62ch;font-size:clamp(15px,1.3vw,18px);line-height:1.65;color:var(--ink-2)}

/* ── ГЕРОЙ ── */
.sv-hero{padding:clamp(28px,4vw,54px) 0 clamp(48px,6vw,86px);
 background:linear-gradient(180deg,var(--paper) 0%,var(--paper-2) 100%)}
.sv-back{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:600;
 color:var(--ink-2);text-decoration:none;margin-bottom:clamp(26px,4vw,52px)}
.sv-back:hover{color:var(--orange)}
.sv-hero__grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);
 gap:clamp(26px,4vw,58px);align-items:end}
.sv-hero h1{font-size:clamp(34px,5.4vw,74px);line-height:1.03;margin:14px 0 0}
.sv-hero h1 em{font-style:normal;color:var(--orange)}
.sv-hero__lead{margin-top:22px;max-width:46ch}
.sv-hero__shot{position:relative;border-radius:4px;overflow:hidden;background:var(--dark);
 box-shadow:0 30px 60px -34px rgba(13,20,34,.7)}
.sv-hero__shot img{width:100%}
.sv-hero__cap{position:absolute;left:0;right:0;bottom:0;padding:34px 18px 12px;
 background:linear-gradient(180deg,transparent,rgba(13,20,34,.86));
 color:#fff;font-size:12.5px;line-height:1.4}
/* паспорт */
.sv-facts{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--line);
 border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:clamp(34px,5vw,64px)}
.sv-facts div{background:var(--paper-2);padding:18px 16px}
.sv-facts dt{font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:var(--ink-2);font-weight:600}
.sv-facts dd{margin:7px 0 0;font-family:'Prata',Georgia,serif;font-size:clamp(15px,1.35vw,19px);line-height:1.25}

/* ── ЗАДАЧА ── */
.sv-task{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(26px,4vw,60px);align-items:center}
.sv-task__t p+p{margin-top:16px}
.sv-task__t p{font-size:clamp(15px,1.35vw,18px);line-height:1.68;color:var(--ink-2)}
.sv-task__t b{color:var(--ink);font-weight:600}
.sv-fig figcaption{margin-top:10px;font-size:12.5px;color:var(--ink-2);line-height:1.45}

/* ── ТЁМНЫЕ СЕКЦИИ ── */
.sv-dark{background:var(--dark);color:#EDE7DA}
.sv-dark .sv-sec__sub,.sv-dark .sv-fig figcaption{color:rgba(237,231,218,.62)}
.sv-dark .sv__eyebrow{color:var(--gold)}

/* ── АНАМОРФОЗА ── */
.sv-nk{margin-top:clamp(30px,4vw,52px);display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,.6fr);
 gap:clamp(22px,3vw,44px);align-items:start}
.sv-nk__stage{perspective:1200px;perspective-origin:calc(50% + var(--dx,0px)) 44%;
 touch-action:pan-y;cursor:ew-resize;position:relative;padding:7% 9% 9%}
.sv-nk__box{position:relative;aspect-ratio:16/10;transform-style:preserve-3d}
.sv-nk__layer{position:absolute;inset:0;transform:translateZ(var(--z,0px)) scale(var(--s,1));
 will-change:transform}
.sv-nk__layer svg{width:100%;height:100%;display:block;overflow:visible}
.sv-nk__edge{position:absolute;inset:0;outline:1px solid rgba(240,174,40,.4);outline-offset:-1px}
.sv-nk__layer--frame .sv-nk__edge{display:none}
.sv-nk__hint{position:absolute;left:50%;bottom:6px;transform:translateX(-50%);
 font-size:12px;color:rgba(237,231,218,.5);pointer-events:none;transition:opacity .3s}
.sv-nk.is-touched .sv-nk__hint{opacity:0}
.sv-nk__panel{background:var(--dark-2);border:1px solid rgba(240,174,40,.2);padding:22px 20px 24px}
.sv-nk__plan{width:100%;max-width:330px;height:auto;display:block;margin:0 auto 18px}
.sv-nk__range{-webkit-appearance:none;appearance:none;width:100%;height:3px;background:rgba(237,231,218,.25);
 border-radius:2px;outline:none;margin:6px 0 0}
.sv-nk__range::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;border-radius:50%;
 background:var(--gold);border:0;cursor:grab;box-shadow:0 0 0 6px rgba(240,174,40,.14)}
.sv-nk__range::-moz-range-thumb{width:26px;height:26px;border-radius:50%;background:var(--gold);
 border:0;cursor:grab}
.sv-nk__range:focus-visible{box-shadow:0 0 0 3px rgba(240,174,40,.5)}
.sv-nk__scale{display:flex;justify-content:space-between;font-size:11px;letter-spacing:.06em;
 text-transform:uppercase;color:rgba(237,231,218,.45);margin-top:10px}
.sv-nk__read{margin-top:24px;font-family:'Prata',Georgia,serif;font-size:19px;line-height:1.3}
.sv-nk__read span{display:block;font-family:'Commissioner',Arial,sans-serif;font-size:13.5px;
 line-height:1.5;color:rgba(237,231,218,.6);margin-top:8px}
.sv-nk__note{margin-top:18px;padding-top:16px;border-top:1px solid rgba(237,231,218,.12);
 font-size:12.5px;line-height:1.5;color:rgba(237,231,218,.45)}

/* ── ПЛЕЙЛИСТ КУБА ── */
.sv-cube{margin-top:clamp(44px,6vw,80px)}
.sv-cube__strip{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(268px,1fr);gap:16px;
 overflow-x:auto;padding-bottom:14px;scroll-snap-type:x mandatory;
 scrollbar-color:rgba(240,174,40,.5) transparent}
.sv-cube__strip::-webkit-scrollbar{height:5px}
.sv-cube__strip::-webkit-scrollbar-thumb{background:rgba(240,174,40,.5);border-radius:3px}
.sv-cube__item{scroll-snap-align:start}
.sv-cube__item img{width:100%;border:1px solid rgba(237,231,218,.12)}
.sv-cube__item b{display:block;margin-top:12px;font-family:'Prata',Georgia,serif;font-weight:400;font-size:17px}
.sv-cube__item span{display:block;margin-top:6px;font-size:13px;line-height:1.5;color:rgba(237,231,218,.55)}

/* ── ВИДЕО ── */
.sv-video{margin-top:clamp(30px,4vw,52px);position:relative;background:#000;
 box-shadow:0 30px 70px -40px rgba(0,0,0,.9)}
.sv-video video{width:100%;display:block;aspect-ratio:16/9;object-fit:cover;background:#000}
.sv-video--tall video{aspect-ratio:16/9}

/* ── МАРШРУТ ── */
.sv-zone{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);
 gap:clamp(24px,3.4vw,56px);align-items:start;padding:clamp(38px,5vw,72px) 0;border-top:1px solid var(--line)}
.sv-zone:first-of-type{border-top:0}
.sv-zone--alt .sv-zone__media{order:2}
.sv-zone__num{font-family:'Prata',Georgia,serif;font-size:15px;color:var(--orange);letter-spacing:.08em}
.sv-zone h3{margin:10px 0 16px;font-size:clamp(22px,2.4vw,32px);line-height:1.15}
.sv-zone p{font-size:15.5px;line-height:1.68;color:var(--ink-2)}
.sv-zone p+p{margin-top:14px}
.sv-zone__media img{width:100%}
.sv-zone__thumbs{display:grid;grid-template-columns:repeat(var(--n,3),1fr);gap:10px;margin-top:10px}
.sv-zone__thumbs img{aspect-ratio:4/3;object-fit:cover}
.sv-zone__thumbs figure{margin:0}
.sv-zone__thumbs figcaption{margin-top:6px;font-size:11.5px;line-height:1.35;color:var(--ink-2)}

/* ── ПАНОРАМА С БИНОКУЛЯРОМ ── */
.sv-mt{margin-top:clamp(28px,4vw,48px)}
.sv-mt__frame{position:relative;background:linear-gradient(180deg,#0E1A2E 0%,#132741 60%,#16304E 100%);
 border:1px solid rgba(240,174,40,.18);overflow:hidden;touch-action:pan-y;cursor:none}
.sv-mt__frame svg{width:100%;height:auto;display:block}
/* на узком экране семнадцать куполов в 350px не читаются: даём панораме
   собственную ширину и листаем её вбок, линза едет за пальцем */
@media(max-width:900px){
 .sv-mt__frame{overflow-x:auto;overflow-y:hidden;touch-action:pan-x pan-y;
  scrollbar-color:rgba(240,174,40,.5) transparent}
 .sv-mt__frame svg{width:940px;max-width:none}
 .sv-mt__frame::-webkit-scrollbar{height:4px}
 .sv-mt__frame::-webkit-scrollbar-thumb{background:rgba(240,174,40,.5)}
}
.sv-mt__hint{position:absolute;left:50%;top:14px;transform:translateX(-50%);font-size:12px;
 letter-spacing:.08em;text-transform:uppercase;color:rgba(237,231,218,.5);pointer-events:none;transition:opacity .3s}
.sv-mt.is-touched .sv-mt__hint{opacity:0}
.sv-mt__foot{display:flex;flex-wrap:wrap;gap:18px 34px;margin-top:20px;font-size:13px;color:rgba(237,231,218,.55)}
.sv-mt__foot b{color:#EDE7DA;font-weight:600}

/* ── ИТОГ ── */
.sv-end{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(26px,4vw,56px);
 align-items:center;margin-top:clamp(28px,4vw,48px)}
.sv-end p{font-size:clamp(15px,1.35vw,18px);line-height:1.68;color:var(--ink-2)}
.sv-end p+p{margin-top:16px}
.sv-big{font-family:'Prata',Georgia,serif;font-size:clamp(44px,7vw,86px);line-height:1;color:var(--ink)}
.sv-big small{display:block;font-family:'Commissioner',Arial,sans-serif;font-size:13.5px;
 letter-spacing:.04em;color:var(--ink-2);margin-top:12px;max-width:36ch;line-height:1.5}

/* ── появление ── */
.sv-r{opacity:0;transform:translateY(20px);transition:opacity .7s ease,transform .7s ease}
.sv-r.in{opacity:1;transform:none}
.no-js .sv-r{opacity:1;transform:none}

/* ── планшет ── */
@media(max-width:1000px){
 .sv-hero__grid,.sv-task,.sv-nk,.sv-zone,.sv-end{grid-template-columns:1fr}
 .sv-zone--alt .sv-zone__media{order:0}
 .sv-facts{grid-template-columns:repeat(3,1fr)}
 .sv-nk__panel{order:2}
}
@media(max-width:640px){
 .sv__wrap{padding:0 18px}
 .sv-facts{grid-template-columns:repeat(2,1fr)}
 .sv-facts div:last-child{grid-column:1/-1}
 .sv-zone__thumbs{grid-template-columns:repeat(2,1fr)}
 .sv-cube__strip{grid-auto-columns:minmax(230px,1fr)}
 .sv-mt__frame{cursor:default}
}
/* ландшафт телефона: высокие блоки не должны занимать три экрана */
@media(max-height:480px) and (orientation:landscape){
 .sv-sec{padding:48px 0}
 .sv-hero__shot img{max-height:64vh;object-fit:cover}
}
@media(prefers-reduced-motion:reduce){
 .sv-r{opacity:1!important;transform:none!important;transition:none}
 .sv *{transition-duration:.01ms!important;animation-duration:.01ms!important}
}
</style>"""


# ─── графика: купол лакколита ───────────────────────────────────────────────
def dome(cx, w, h, base):
    """Сглаженный купол: лакколит это застывшая магма, поднявшая слои горбом."""
    x0, x1 = cx - w / 2, cx + w / 2
    return (f'M{x0:.0f},{base} C{x0 + w * .18:.0f},{base - h * .52:.0f} '
            f'{cx - w * .24:.0f},{base - h:.0f} {cx:.0f},{base - h:.0f} '
            f'C{cx + w * .24:.0f},{base - h:.0f} {x1 - w * .18:.0f},{base - h * .52:.0f} '
            f'{x1:.0f},{base}Z')


def nk_scene():
    """Слои сцены для короба. Каждый слой рисуется в одной системе координат
    0 0 800 500, поэтому в расчётной точке они совпадают пиксель в пиксель."""
    # дальние горы
    far = ''.join(f'<path d="{dome(x, w, h, 372)}" fill="#2C4A76"/>'
                  for x, w, h in ((120, 300, 96), (330, 260, 132), (520, 340, 78), (720, 300, 110)))
    # ближние холмы
    near = ''.join(f'<path d="{dome(x, w, h, 400)}" fill="#20365B"/>'
                   for x, w, h in ((60, 320, 70), (300, 380, 96), (600, 340, 62)))
    # поле: штрихи колосьев
    strokes = []
    for i in range(150):
        x = (i * 37 % 800) + (i % 7)
        y = 398 + (i * 13 % 96)
        ln = 12 + (i % 5) * 3
        strokes.append(f'<path d="M{x},{y} q{2 + i % 4},{-ln * .6:.0f} {1 - i % 3},{-ln}" '
                       f'stroke="#B5732A" stroke-width="1.6" fill="none" opacity=".75"/>')
    field = ''.join(strokes)
    # сноп: пучок колосьев из одной точки, верхушки уходят выше рамки короба
    # (у svg снят overflow, поэтому слой рисует за своими границами: ровно это
    # и делает naked-eye, картинка выходит за плоскость экрана)
    sheaf = ['<path d="M368,470 h64 v18 h-64Z" fill="#8A5A22"/>']
    for i in range(23):
        a = -0.46 + i * (0.92 / 22)
        ln = 500 - abs(a) * 150
        tipx = 400 + math.sin(a) * ln * .62
        tipy = 470 - math.cos(a) * ln
        c1x, c1y = 400 + math.sin(a) * 40, 470 - math.cos(a) * ln * .45
        sheaf.append(f'<path d="M400,472 C{c1x:.0f},{c1y:.0f} {tipx - math.sin(a) * 60:.0f},'
                     f'{tipy + ln * .22:.0f} {tipx:.0f},{tipy:.0f}" stroke="#C8792A" '
                     f'stroke-width="{2.6 - abs(a) * 1.4:.1f}" fill="none" stroke-linecap="round"/>')
        for k in range(4):
            # сдвиг по стеблю разный, иначе зёрна выстраиваются в ровные дуги
            t = .54 + k * .145 + ((i * 7 + k * 3) % 5) * .012
            ex = 400 + math.sin(a) * ln * .62 * t * t
            ey = 470 - math.cos(a) * ln * t
            sheaf.append(f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="6.5" ry="14" fill="#E5A244" '
                         f'transform="rotate({a * 57:.0f} {ex:.0f} {ey:.0f})" opacity=".9"/>')
    sheaf = ''.join(sheaf)

    layers = [
        (200, 'Небо и дальние горы',
         '<defs><linearGradient id="svSky" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#0F2E63"/><stop offset=".62" stop-color="#2E6FA8"/>'
         '<stop offset="1" stop-color="#7FA8C4"/></linearGradient></defs>'
         '<rect width="800" height="500" fill="url(#svSky)"/>'
         '<circle cx="132" cy="118" r="38" fill="#F2C35A" opacity=".85"/>' + far),
        (130, 'Ближние холмы', near),
        (60, 'Поле', '<rect y="392" width="800" height="108" fill="#8C5620"/>' + field),
        (-60, 'Сноп колосьев', sheaf),
    ]
    out = []
    for depth, title, body in layers:
        out.append(f'<div class="sv-nk__layer" data-depth="{depth}">'
                   f'<svg viewBox="0 0 800 500" role="img" aria-label="{H.escape(title)}, '
                   f'слой сцены">{body}</svg><i class="sv-nk__edge"></i></div>')
    # Передняя грань короба, глубина 0. Паспарту закрывает то, что дальние слои
    # выносят за окно (они крупнее по построению). Сноп лежит ближе к зрителю,
    # поэтому браузер рисует его ПОВЕРХ паспарту, и колосья выходят за грань.
    out.append('<div class="sv-nk__layer sv-nk__layer--frame" data-depth="0">'
               '<svg viewBox="0 0 800 500" aria-hidden="true">'
               '<path d="M-130,-110 H930 V610 H-130Z M0,0 H800 V500 H0Z" fill="#0D1422" '
               'fill-rule="evenodd"/>'
               '<rect x="2" y="2" width="796" height="496" fill="none" stroke="#F0AE28" '
               'stroke-width="4" opacity=".9"/>'
               '<path d="M2,392 H798" stroke="#F0AE28" stroke-width="2" opacity=".45"/>'
               '<path d="M400,392 V498" stroke="#F0AE28" stroke-width="2" opacity=".45"/>'
               '</svg></div>')
    return ''.join(out)


def nk_plan():
    """Вид сверху: короб, расчётная ось и точка, где стоит зритель."""
    return ('<svg class="sv-nk__plan" viewBox="0 0 300 150" role="img" '
            'aria-label="Вид сверху: короб и место зрителя в зале">'
            '<rect x="106" y="16" width="88" height="26" fill="none" stroke="#F0AE28" stroke-width="2"/>'
            '<text x="150" y="12" text-anchor="middle" font-size="10" fill="#EDE7DA" '
            'opacity=".65" font-family="Commissioner,Arial">короб</text>'
            '<path d="M150,42 V126" stroke="#F0AE28" stroke-width="1" stroke-dasharray="4 5" opacity=".55"/>'
            '<path d="M40,126 H260" stroke="#EDE7DA" stroke-width="1" opacity=".22"/>'
            '<text x="150" y="144" text-anchor="middle" font-size="9.5" fill="#EDE7DA" opacity=".45" '
            'font-family="Commissioner,Arial">проход по павильону</text>'
            '<g id="svViewer"><circle cx="150" cy="126" r="7" fill="#F0AE28"/>'
            '<path d="M150,119 L134,46 M150,119 L166,46" stroke="#F0AE28" stroke-width="1" opacity=".5"/></g>'
            '</svg>')


def mountains_svg():
    """Панорама 17 лакколитов КМВ. Рисунок идёт двумя копиями: нижняя обычная,
    верхняя увеличена и лежит под круглой маской. Это и есть бинокуляр.
    Заодно считаем линию гребня: по ней линза едет, чтобы всегда держать в
    поле зрения вершину, а не пустое небо."""
    W, VH, BASE, HMAX = 1800, 480, 424, 322
    # раскладка «горой»: самая высокая ближе к центру, остальные расходятся
    # по сторонам. Иначе семнадцать куполов подряд читаются как забор.
    desc = sorted(LACCOLITHS, key=lambda m: -m[1])
    left, right = [], []
    for i, item in enumerate(desc):
        (left if i % 2 else right).append(item)
    order = list(reversed(left)) + right
    xs, x = [], 30
    for name, h in order:
        w = 150 + h * .16
        xs.append([x + w / 2, w, h, name])
        x += w * .72
    scale = (W - 60) / (x - 30)
    peaks, body, labels = [], [], []
    for item in xs:
        cx, w, h, name = item
        cx = 30 + (cx - 30) * scale
        w *= scale
        hp = h / 1401 * HMAX
        peaks.append((cx, BASE - hp, w))
        shade = '#1B3355' if hp < 140 else '#22436E'
        body.append(f'<path d="{dome(cx, w, hp, BASE)}" fill="{shade}" '
                    f'stroke="#3E6B9E" stroke-width="1.2"/>')
        fs = max(13, 21 - max(0, len(name) - 8) * 1.2)
        labels.append(f'<g><text x="{cx:.0f}" y="{BASE - hp - 15:.0f}" text-anchor="middle" '
                      f'font-size="{fs:.0f}" font-weight="600" fill="#F6EFDF" '
                      f'font-family="Commissioner,Arial">{H.escape(name)}</text>'
                      f'<text x="{cx:.0f}" y="{BASE - hp + 8:.0f}" text-anchor="middle" font-size="15" '
                      f'fill="#F0AE28" font-family="Commissioner,Arial">{h} м</text>'
                      f'<circle cx="{cx:.0f}" cy="{BASE - hp:.0f}" r="4" fill="#F0AE28"/></g>')
    # координаты вершин для JS: линза защёлкивается на ближайшую, как бинокуляр
    peak_data = ';'.join(f'{px:.0f},{py:.0f}' for px, py, _ in peaks)
    ridge = ''.join(body)
    # шкала высот: без неё панорама читается просто как узор
    grid = []
    for m in (500, 1000, 1500):
        gy = BASE - m / 1401 * HMAX
        grid.append(f'<path d="M0,{gy:.0f} H{W}" stroke="#8FB6DC" stroke-width="1" '
                    f'stroke-dasharray="2 10" opacity=".28"/>'
                    f'<text x="14" y="{gy - 7:.0f}" font-size="15" fill="#8FB6DC" opacity=".6" '
                    f'font-family="Commissioner,Arial">{m} м</text>')
    horizon = (f'<path d="M0,{BASE} H{W}" stroke="#F0AE28" stroke-width="1" opacity=".3"/>'
               + ''.join(grid))
    svg = (f'<svg viewBox="0 0 {W} {VH}" data-peaks="{peak_data}" data-vw="{W}" '
           f'data-vh="{VH}" role="img" aria-label="Панорама семнадцати гор-лакколитов '
           f'Кавказских Минеральных Вод с высотами: от Кокуртлы 406 метров до Бештау 1401 метр">'
           f'<defs><clipPath id="svLens"><circle id="svLensC" cx="{W // 2}" cy="240" r="132"/></clipPath>'
           f'<linearGradient id="svHaze" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="#16304E" stop-opacity="0"/>'
           f'<stop offset="1" stop-color="#16304E" stop-opacity=".55"/></linearGradient></defs>'
           f'<g opacity=".92">{ridge}</g><rect width="{W}" height="{VH}" fill="url(#svHaze)"/>{horizon}'
           f'<g clip-path="url(#svLens)"><g id="svLensG">'
           f'<rect x="-{W}" y="-{VH}" width="{W * 3}" height="{VH * 3}" fill="#0E1A2E"/>'
           f'{ridge}{horizon}{"".join(labels)}</g></g>'
           f'<circle id="svLensR" cx="{W // 2}" cy="240" r="132" fill="none" stroke="#F0AE28" '
           f'stroke-width="3"/>'
           f'<circle id="svLensD" cx="{W // 2}" cy="230" r="4" fill="#F0AE28" opacity=".8"/></svg>')
    return svg


# ─── секции ─────────────────────────────────────────────────────────────────
def hero():
    facts = ''.join(f'<div><dt>{H.escape(k)}</dt><dd>{H.escape(v)}</dd></div>' for k, v in FACTS)
    return f'''<section class="sv-hero"><div class="sv__wrap">
<a class="sv-back" href="/project/">← Все проекты</a>
<div class="sv-hero__grid">
 <div>
  <div class="sv__eyebrow">Выставка «Россия», ВДНХ, павильон №75</div>
  <h1>Стенд Ставропольского края, <em>собранный вокруг одной точки</em></h1>
  <p class="sv__lead sv-hero__lead">248 дней экспозиции края в главном павильоне регионов.
  Мы отвечали за мультимедийную часть: LED-короб с изображением, рассчитанным под конкретное
  место в зале, велотренажёр вместо горной тропы, экраны, которые отдают посетителю его
  собственный рисунок.</p>
 </div>
 <figure class="sv-hero__shot" style="margin:0">
  <img src="{IMG}/cube-field.jpg" width="892" height="544" loading="eager" decoding="async"
   alt="LED-короб над стендом Ставрополья: сноп колосьев выходит за переднюю грань экрана">
  <figcaption class="sv-hero__cap">Тот самый кадр: сноп читается объёмным, потому что
  картинка построена под место, откуда сделан снимок</figcaption>
 </figure>
</div>
<dl class="sv-facts">{facts}</dl>
</div></section>'''


def task():
    return f'''<section class="sv-sec"><div class="sv__wrap">
<div class="sv-task sv-r">
 <div class="sv-task__t">
  <div class="sv__eyebrow">Задача</div>
  <h2 class="sv-sec__h" style="margin-top:14px">Не показать край, а задержать у стенда</h2>
  <p style="margin-top:22px">В павильоне №75 регионы стоят рядами, у каждого свои экраны, свои
  ростовые буквы и своя очередь. Человек идёт мимо десятков таких экспозиций подряд и к середине
  зала перестаёт различать их между собой.</p>
  <p>Поэтому <b>почти всё на стенде требует действия</b>: сесть на велотренажёр, провести
  ладонью по стеклу, раскрасить картину, выбрать открытку. Единственное, на что тут можно
  просто смотреть, висит над головой и видно его из соседнего прохода.</p>
 </div>
 <figure class="sv-fig" style="margin:0">
  <img src="{IMG}/stand-wide.jpg" width="1080" height="606" loading="lazy" decoding="async"
   alt="Общий вид стенда Ставропольского края в павильоне №75: оранжевые объёмные буквы и поток посетителей">
  <figcaption>Павильон №75, обычный день работы выставки</figcaption>
 </figure>
</div>
</div></section>'''


def naked_eye():
    items = ''.join(
        f'<div class="sv-cube__item"><img src="{IMG}/cube-{slug}.jpg" width="892" height="544" '
        f'loading="lazy" decoding="async" alt="Сюжет на LED-коробе стенда: {H.escape(title.lower())}">'
        f'<b>{H.escape(title)}</b><span>{H.escape(desc)}</span></div>'
        for slug, title, desc in CUBE)
    return f'''<section class="sv-sec sv-dark"><div class="sv__wrap">
<div class="sv-r">
 <div class="sv__eyebrow">Как устроен короб</div>
 <h2 class="sv-sec__h" style="margin-top:14px;color:#F6EFDF">Картинка, рассчитанная под место в зале</h2>
 <p class="sv-sec__sub">Naked-eye 3D это анаморфоза: изображение строят не для экрана, а для точки,
 где стоит зритель. Оттуда две грани короба перестают читаться как две плоскости, и сноп выходит
 за границу экрана. Отойдите на несколько шагов, и объём распадётся на слои, из которых он собран.</p>
</div>
<div class="sv-nk sv-r" id="svNk">
 <div>
  <div class="sv-nk__stage" id="svStage">
   <div class="sv-nk__box">{nk_scene()}</div>
   <div class="sv-nk__hint">потяните вбок или двигайте ползунок</div>
  </div>
 </div>
 <div class="sv-nk__panel">
  {nk_plan()}
  <label for="svRange" class="sv__eyebrow" style="display:block;margin-bottom:6px">Где стоит зритель</label>
  <input class="sv-nk__range" type="range" id="svRange" min="-100" max="100" value="0" step="1"
   aria-describedby="svRead">
  <div class="sv-nk__scale"><span>левее</span><span>расчётная точка</span><span>правее</span></div>
  <p class="sv-nk__read" id="svRead" aria-live="polite">Изображение собрано
   <span>Слои совпали: короб выглядит одним объёмом.</span></p>
  <p class="sv-nk__note">Схема, а не съёмка. Слои нормированы по перспективе, поэтому в расчётной
  точке их границы совпадают до пикселя.</p>
 </div>
</div>
<div class="sv-video sv-r">
 <video controls preload="none" playsinline poster="{IMG}/poster-cube.jpg"
  aria-label="Съёмка LED-короба стенда Ставрополья: полный цикл сюжетов">
  <source src="{MEDIA}/stavropol-vdnh-nakedeye.mp4" type="video/mp4">
 </video>
</div>
<p class="sv-sec__sub" style="margin-top:14px">Три с половиной минуты съёмки с той самой точки:
полный круг сюжетов, которые сменяли друг друга на коробе.</p>
<div class="sv-cube sv-r">
 <h3 style="font-size:clamp(20px,2vw,26px);color:#F6EFDF">Что показывали на коробе</h3>
 <p class="sv-sec__sub" style="margin:12px 0 24px">Десять кадров из этой съёмки. Сюжеты сделаны
 так, чтобы важное всегда происходило на стыке граней: только там работает выход за плоскость.</p>
 <div class="sv-cube__strip">{items}</div>
</div>
</div></section>'''


def route():
    out = []
    for i, (num, title, paras, main, thumbs) in enumerate(ZONES):
        ps = ''.join(f'<p>{H.escape(p)}</p>' for p in paras)
        th = ''.join(f'<figure><img src="{src}" loading="lazy" decoding="async" '
                     f'alt="{H.escape(alt)}"></figure>' for src, alt in thumbs)
        alt_cls = ' sv-zone--alt' if i % 2 else ''
        out.append(f'''<article class="sv-zone{alt_cls} sv-r">
 <div class="sv-zone__media">
  <img src="{main[0]}" loading="lazy" decoding="async" alt="{H.escape(main[1])}">
  <div class="sv-zone__thumbs" style="--n:{len(thumbs)}">{th}</div>
 </div>
 <div><div class="sv-zone__num">{num}</div><h3>{H.escape(title)}</h3>{ps}</div>
</article>''')
    return f'''<section class="sv-sec"><div class="sv__wrap">
<div class="sv-r"><div class="sv__eyebrow">Маршрут</div>
<h2 class="sv-sec__h" style="margin-top:14px">Что на стенде можно было потрогать</h2></div>
<div style="margin-top:clamp(20px,3vw,40px)">{''.join(out)}</div>
</div></section>'''


def mountains():
    return f'''<section class="sv-sec sv-dark"><div class="sv__wrap">
<div class="sv-r">
 <div class="sv__eyebrow">Тропа с бинокулярами</div>
 <h2 class="sv-sec__h" style="margin-top:14px;color:#F6EFDF">Семнадцать гор, которые так и не стали вулканами</h2>
 <p class="sv-sec__sub">Лакколиты Кавказских Минеральных Вод: магма подняла осадочные слои горбом
 и застыла внутри, не пробившись наружу. На стенде их разглядывали в бинокуляры вдоль тропинки.
 Здесь то же самое: ведите линзой по хребту.</p>
</div>
<div class="sv-mt sv-r" id="svMt">
 <div class="sv-mt__frame" id="svMtFrame">{mountains_svg()}
  <div class="sv-mt__hint">наведите линзу на вершину</div>
 </div>
 <div class="sv-mt__foot">
  <div><b>1401 м</b> Бештау, высшая точка</div>
  <div><b>17</b> гор в группе</div>
  <div><b>406 м</b> Кокуртлы, самая низкая</div>
  <div>Высоты даны по вершинам, силуэты схематичны</div>
 </div>
</div>
<figure class="sv-fig sv-r" style="margin:clamp(28px,4vw,48px) 0 0">
 <img src="{PHOTO}/binoculars-path.jpg" width="2137" height="1217" loading="lazy" decoding="async"
  alt="Эскиз зоны с бинокулярами: смотровая труба на фоне панорамы Кавминвод">
 <figcaption>Эскиз зоны с бинокулярами, по которому её строили</figcaption>
</figure>
</div></section>'''


def finale():
    return f'''<section class="sv-sec"><div class="sv__wrap">
<div class="sv-r"><div class="sv__eyebrow">Ролик</div>
<h2 class="sv-sec__h" style="margin-top:14px">Стенд за минуту</h2></div>
<div class="sv-video sv-r">
 <video controls preload="none" playsinline poster="{IMG}/poster-main.jpg"
  aria-label="Ролик о стенде Ставропольского края на выставке «Россия»">
  <source src="/videos/stavropol-stand.mp4" type="video/mp4">
 </video>
</div>
<p class="sv-sec__sub sv-r" style="margin-top:14px">Съёмка на стенде, собранная без
закадрового текста: вход на выставку, зелёный зал, тропы терренкура, экраны и куб.</p>
<div class="sv-end sv-r">
 <div>
  <div class="sv-big">18 млн+<small>Столько человек прошло через выставку «Россия» за всё
  время работы. Это цифра всей выставки, а не отдельного стенда: посчитать поток одной
  экспозиции внутри павильона нельзя.</small></div>
 </div>
 <div>
  <p>Стенд Ставрополья получил приз зрительских симпатий по голосованию посетителей выставки.</p>
  <p>Экспозиция закрылась 8 июля 2024 года вместе со всей выставкой, стенд разобрали.
  Съёмка короба и зон осталась: по ней и собран этот кейс.</p>
  <figure class="sv-fig" style="margin:22px 0 0">
   <img src="{PHOTO}/award-ceremony.jpg" width="914" height="508" loading="lazy" decoding="async"
    alt="Церемония награждения на выставке «Россия»">
   <figcaption>Церемония награждения на выставке</figcaption>
  </figure>
 </div>
</div>
</div></section>'''


PAGE_JS = """<script>(function(){
var d=document;
// появление секций
var io=window.IntersectionObserver?new IntersectionObserver(function(es){
 es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});
},{rootMargin:'0px 0px -8% 0px'}):null;
[].forEach.call(d.querySelectorAll('.sv-r'),function(n){io?io.observe(n):n.classList.add('in');});

// ── анаморфоза: слои нормируем по перспективе ──
var stage=d.getElementById('svStage'),range=d.getElementById('svRange'),
    read=d.getElementById('svRead'),viewer=d.getElementById('svViewer'),
    nk=d.getElementById('svNk');
if(stage&&range){
 var D=1200, layers=[].slice.call(stage.querySelectorAll('.sv-nk__layer'));
 layers.forEach(function(l){
  var depth=parseFloat(l.getAttribute('data-depth'))||0, z=-depth;
  l.style.setProperty('--z',z+'px');
  l.style.setProperty('--s',((D-z)/D).toFixed(4));
 });
 function paint(v){
  stage.style.setProperty('--dx',(v*2.4).toFixed(1)+'px');
  if(viewer)viewer.setAttribute('transform','translate('+(v*0.62).toFixed(1)+',0)');
  var a=Math.abs(v),t,s;
  if(a<6){t='Изображение собрано';s='Слои совпали: короб выглядит одним объёмом.';}
  else if(a<30){t='Шаг в сторону';s='Границы слоёв разошлись, сноп сползает с поля.';}
  else if(a<65){t='Объём поплыл';s='Видно, что «глубина» это несколько плоскостей на разном удалении.';}
  else{t='Трюк развалился';s='С этого места короб читается как то, чем он и является: экран с углом.';}
  read.innerHTML=t+'<span>'+s+'</span>';
 }
 range.addEventListener('input',function(){paint(+range.value);nk&&nk.classList.add('is-touched');});
 // тянуть можно и саму сцену
 var drag=false,x0=0,v0=0;
 stage.addEventListener('pointerdown',function(e){drag=true;x0=e.clientX;v0=+range.value;
  stage.setPointerCapture&&stage.setPointerCapture(e.pointerId);nk&&nk.classList.add('is-touched');});
 stage.addEventListener('pointermove',function(e){if(!drag)return;
  var v=Math.max(-100,Math.min(100,v0+(e.clientX-x0)*0.36));range.value=v;paint(v);});
 ['pointerup','pointercancel','pointerleave'].forEach(function(ev){
  stage.addEventListener(ev,function(){drag=false;});});
 paint(0);
}

// ── бинокуляр по панораме: линза едет по линии гребня ──
var frame=d.getElementById('svMtFrame');
if(frame){
 var svg=frame.querySelector('svg'),c=d.getElementById('svLensC'),
     ring=d.getElementById('svLensR'),dot=d.getElementById('svLensD'),
     g=d.getElementById('svLensG'),mt=d.getElementById('svMt'),
     K=1.85,VW=+svg.getAttribute('data-vw'),VH=+svg.getAttribute('data-vh'),
     PEAKS=svg.getAttribute('data-peaks').split(';').map(function(s){
       var a=s.split(',');return {x:+a[0],y:+a[1]};}),
     idle=true,t0=Date.now(),R=132,cx=VW/2,cy=240,tx=VW/2,ty=240;
 function nearest(x){                      // ближайшая вершина к точке x
  var best=PEAKS[0],bd=1e9;
  PEAKS.forEach(function(p){var d=Math.abs(p.x-x);if(d<bd){bd=d;best=p;}});
  return best;
 }
 function draw(){
  cx+=(tx-cx)*0.18;cy+=(ty-cy)*0.18;
  var x=cx.toFixed(1),y=cy.toFixed(1);
  c.setAttribute('cx',x);c.setAttribute('cy',y);
  ring.setAttribute('cx',x);ring.setAttribute('cy',y);
  dot.setAttribute('cx',x);dot.setAttribute('cy',y);
  g.setAttribute('transform','translate('+((1-K)*cx).toFixed(1)+','+((1-K)*cy).toFixed(1)+') scale('+K+')');
 }
 function aim(x){var p=nearest(x);
  tx=Math.max(R*0.5,Math.min(VW-R*0.5,p.x));
  ty=Math.max(R+4,Math.min(VH-R-4,p.y+22));}
 function move(e){
  var r=svg.getBoundingClientRect();   // именно svg: на мобильном он шире рамки
  idle=false;mt&&mt.classList.add('is-touched');
  aim((e.clientX-r.left)/r.width*VW);
 }
 frame.addEventListener('pointermove',move);
 frame.addEventListener('pointerdown',move);
 function visible(){                       // видимый кусок панорамы в координатах svg
  var r=svg.getBoundingClientRect(),f=frame.getBoundingClientRect(),
      a=(Math.max(f.left,r.left)-r.left)/r.width*VW,
      b=(Math.min(f.right,r.right)-r.left)/r.width*VW;
  return [a,b];
 }
 (function loop(){
  var v=visible();
  if(idle){                                // сама гуляет, но только по видимому
   var m=(v[0]+v[1])/2,amp=(v[1]-v[0])*0.42;
   aim(m+Math.sin((Date.now()-t0)/6400)*amp);
  }else if(tx<v[0]||tx>v[1]){aim((v[0]+v[1])/2);}
  draw();requestAnimationFrame(loop);
 })();
 aim(VW/2);cx=tx;cy=ty;draw();
}
})();</script>"""

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
                 '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"Стенд Ставропольского края на выставке «Россия»",'
                 '"item":"' + URL + '"}]}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Стенд Ставропольского края на выставке «Россия» на ВДНХ | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: мультимедийное оснащение стенда Ставропольского края на выставке «Россия» (ВДНХ, павильон №75, 248 дней). LED-короб с naked-eye 3D, виртуальный терренкур на велотренажёре, прозрачные тач-панели, интерактивная картина, зелёный зал.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Стенд Ставропольского края на выставке «Россия» | кейс Hand Marketing">
<meta property="og:description" content="LED-короб с изображением, рассчитанным под точку в зале, терренкур на велотренажёре и экраны, которые отдают посетителю его рисунок. 248 дней в павильоне №75 на ВДНХ.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/cube-field.jpg">
<meta property="og:site_name" content="Hand Marketing"><meta property="og:locale" content="ru_RU">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/prata-commissioner.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def build():
    return (HEAD + rc.header() + '<main class="sv">' + hero() + task() + naked_eye() +
            route() + mountains() + finale() + '</main><a id="lead"></a>' +
            rc.footer() + rc.JS + PAGE_JS + BREADCRUMB_LD + '</body></html>')


if __name__ == '__main__':
    out = os.path.join(ROOT, 'portfolio', 'stavropol-stand-vdnh')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    # index-a2.html это деплой-источник (workflow переименовывает его в index.html).
    # Для кастомной страницы он не нужен и затёр бы её на проде.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('удалён устаревший index-a2.html')
    print('written', os.path.join(out, 'index.html'))
