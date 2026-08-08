#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/3d/stavropol/index.html: кейс «3D Mapping шоу в Ставрополе»
(открытие новогодних мероприятий, площадь Ленина, 13 декабря 2019).

Что было раньше: запечённая Tilda-страница «задача → решение → результат»
сплошным текстом. Вся техника кейса (27 проекторов, 410 000 лм, 97 м, 150 лк/м²)
лежала одним абзацем, а из графики были четыре фотографии в галерее.

Идея страницы: показать шоу так, как его собирали, то есть с пульта.
Отсюда три механики, которых на сайте ещё не было:

1. Пульт мэппинга. Верхняя камера в съёмке стоит неподвижно всю программу,
   поэтому шесть сцен шоу лежат в одной геометрии фасада. На кадр положены
   девять зон проекции в перспективе здания: гасишь стек, зона на фасаде
   темнеет с мягкими краями (соседи перекрывают только стык), а счётчик
   пересчитывает люмены и люксы на квадратный метр.
2. Разрез площади в SVG: башня, 97 метров, луч над головами зрителей.
   Кнопка опускает приборы на землю и рисует тени от толпы и декораций на
   фасаде, то есть показывает, зачем нужны были башни.
3. Туман по скроллу: главный сюжет вечера (площадь накрыло туманом за час
   до старта) отыгран прокруткой, туман поднимается на высоту здания.

Честность цифр: 27 проекторов Epson EB-L1755U, стек, башни, 97 м, 410 000 лм,
150 лк/м², ELPLM10, 24 кг, 8 минут, более 25 000 зрителей, туман и AR-приложение
из текста кейса. Дата 13.12.2019, площадь Ленина, ёлка 25 м и место в рейтинге
ТурСтата, четыре лазера, зенитные прожекторы на 4 км, 100 кВт звука, название
и персонажи приложения StavAR, программа из 150+ мероприятий — из публикаций
о вечере (КП-Ставрополь, «Своё ТВ», «Победа26»). Южные слоны как символ края —
по материалам Ставропольского краеведческого музея. Разбивка проекции на девять
зон — реконструкция по съёмке, на странице подписана.

Шрифты Unbounded + Fira Sans, локальные (/fonts/unbounded-fira.css),
кадры готовит scripts/stavropol-3d-assets.py.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/stavropol-3d'
LIB = '/images/lib'
URL = 'https://hand-marketing.ru/3d/stavropol/'
VIDEO = '/media/stavropol-3dmapping.mp4'

# фотографии вечера, оставшиеся от старой страницы (общий каталог зеркала)
PH_ANGELS = LIB + '/as3130-6433-4331-b864-383333663738/-3-1.jpg'
PH_TREES = LIB + '/as3564-6366-4465-b066-336636633266/-6-1.jpg'
PH_ELEPH = LIB + '/as3935-3430-4336-a233-353836626537/0039-2.jpg'
PH_CARPET = LIB + '/as3261-3734-4335-b536-346564646634/0055-1.jpg'
PH_BEAMS = '/case-assets/7e5bfc88_0001-2.jpg'

# ─── паспорт проекта ────────────────────────────────────────────────────────
FACTS = [
    ('Клиент', 'Администрация города Ставрополя'),
    ('Дата', '13 декабря 2019'),
    ('Площадка', 'Площадь Ленина'),
    ('Проекторов', '27 в стеках'),
    ('Зрителей', 'более 25 000'),
]

# ─── геометрия фасада на кадрах верхней камеры ──────────────────────────────
# Кадры режутся одинаково (crop 960×300 от 120,270 в scripts/stavropol-3d-assets.py),
# камера неподвижна, поэтому фасад везде лежит одним четырёхугольником.
QUAD = [(30.0, 26.0), (938.0, 42.0), (938.0, 251.0), (31.0, 187.0)]
ZONES = 9          # 9 зон по 3 проектора в стеке = 27 приборов
PROJ_TOTAL = 27
LM_TOTAL = 410000  # суммарный световой поток, лм
LUX_TOTAL = 150    # люкс на квадратный метр на поверхности фасада

# ─── сцены шоу: (файл, короткое имя, подпись) ───────────────────────────────
SCENES = [
    ('scene-arcade', 'Аркада',
     'Первым делом шоу ломает привычные очертания здания: фасад разбирается '
     'и собирается заново античной аркадой.'),
    ('scene-carpet', 'Ковёр',
     'Орнамент из ромбов расходится от центра и ложится по окнам, как узор по ткани. '
     'Окна работают не помехой, а частью рисунка.'),
    ('scene-deer', 'Олени',
     'Светящееся стадо идёт вдоль всей длины фасада. Кадр держится на движении, '
     'поэтому яркость здесь важнее детали.'),
    ('scene-elephants', 'Слоны',
     'Символ края выходит на здание Правительства: южные слоны идут по фасаду '
     'и затем поднимаются на крышу.'),
    ('scene-tree', 'Золотой зал',
     'Золотой орнамент во всю длину и ёлка в центре: самая плотная по свету сцена, '
     'здесь работают все 27 проекторов сразу.'),
    ('scene-laser', 'Лазер',
     'Лазерная графика ложится поверх проекции и уводит шоу к финалу: '
     'дальше свет уйдёт с фасада в ёлку.'),
]

# ─── свет, лазеры, звук ─────────────────────────────────────────────────────
NUMBERS = [
    ('410 000', 'люмен', 'Суммарный световой поток 27 проекторов Epson EB-L1755U.'),
    ('150', 'люкс/м²', 'Освещённость, которую эта связка дала на поверхности фасада.'),
    ('≈2 700', 'м²', 'Столько площади закрывает такой поток при такой освещённости: '
                     'расчёт 410 000 / 150.'),
    ('97', 'метров', 'Дистанция от башен с проекторами до здания Правительства.'),
    ('4', 'лазера', 'Мощные лазеры работали и по фасаду, и по небу над площадью.'),
    ('4', 'километра', 'На такую высоту били зенитные прожекторы: их лучи видно с окраин.'),
    ('100', 'кВт звука', 'Звуковой комплект площади, рассчитанный на 25 тысяч человек.'),
    ('25', 'метров', 'Высота главной ёлки края: в тот год она вошла в топ-25 России '
                     'по версии ТурСтата.'),
]

# ─── персонажи приложения StavAR ────────────────────────────────────────────
AR_HEROES = [
    ('Дед Мороз', 'Главный персонаж вечера, к нему выстраивалась очередь за селфи.'),
    ('Слонёнок', 'Тот самый символ края, только маленький и виртуальный.'),
    ('Крылатый монстр', 'Сказочная нечисть, которую искали по площади как в квесте.'),
    ('Гигантская мышь', 'Символ наступавшего года, ростом с человека.'),
]

# ─── галерея вечера ─────────────────────────────────────────────────────────
GALLERY = [
    (PH_ANGELS, 'Ангелы и крест на фасаде здания Правительства Ставропольского края'),
    (PH_CARPET, 'Ковровый орнамент во всю длину фасада, вид сверху'),
    (PH_ELEPH, 'Слоны на фасаде здания Правительства, вид сверху'),
    (PH_TREES, 'Ёлки на площади Ленина и зелёные лучи лазеров'),
    (IMG + '/facade-laser.jpg', 'Лазерная графика по фасаду и толпа на площади'),
    (PH_BEAMS, 'Лучи лазеров уходят в небо над площадью Ленина'),
]


def zone_pts(i):
    """Полигон i-й зоны проекции в перспективе фасада."""
    tl, tr, br, bl = QUAD
    a, b = i / ZONES, (i + 1) / ZONES

    def top(t):
        return (tl[0] + (tr[0] - tl[0]) * t, tl[1] + (tr[1] - tl[1]) * t)

    def bot(t):
        return (bl[0] + (br[0] - bl[0]) * t, bl[1] + (br[1] - bl[1]) * t)

    pts = [top(a), top(b), bot(b), bot(a)]
    return ' '.join('%.1f,%.1f' % p for p in pts)


PAGE_CSS = """<style id="sv-css">
:root{
 --sv-bg:#05070B; --sv-bg2:#0A0E15; --sv-panel:#0E141D; --sv-line:rgba(255,255,255,.13);
 --sv-txt:#EEF2F8; --sv-dim:#8E9BAE; --sv-mute:#66717F;
 --sv-laser:#3CE07E; --sv-amber:#E8B04A; --sv-blue:#4A76F0; --sv-off:#FF5140;
}
.sv{font-family:'Fira Sans',-apple-system,Arial,sans-serif;color:var(--sv-txt);
 background:var(--sv-bg);-webkit-font-smoothing:antialiased;overflow-x:clip;
 background-image:radial-gradient(120% 70% at 50% 0,rgba(60,224,126,.09),transparent 62%)}
.sv *{box-sizing:border-box}
.sv img{max-width:100%;height:auto;display:block}
.sv h1,.sv h2,.sv h3{font-family:'Unbounded','Fira Sans',Arial,sans-serif;font-weight:500;
 letter-spacing:-.02em;margin:0;line-height:1.12}
.sv p{margin:0}
.sv__wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.sv__eyebrow{font-family:'Unbounded','Fira Sans',Arial,sans-serif;font-size:11px;
 font-weight:400;letter-spacing:.2em;text-transform:uppercase;color:var(--sv-laser)}
.sv__lead{font-size:clamp(16px,1.5vw,19px);line-height:1.65;color:var(--sv-dim)}
.sv-sec{padding:clamp(56px,7vw,110px) 0;position:relative}
.sv-sec__h{font-size:clamp(25px,3.3vw,44px);max-width:20ch;margin-top:14px}
.sv-sec__sub{margin-top:22px;max-width:66ch;font-size:clamp(15px,1.3vw,17px);
 line-height:1.75;color:var(--sv-dim)}
.sv-sec__sub b{color:var(--sv-txt);font-weight:500}
.sv-note{margin-top:14px;font-size:12.5px;line-height:1.6;color:var(--sv-mute);max-width:70ch}
.sv-r{opacity:0;transform:translateY(18px);transition:opacity .7s ease,transform .7s ease}
.sv-r.in{opacity:1;transform:none}
.sv-num{font-family:'Unbounded','Fira Sans',Arial,sans-serif;font-variant-numeric:tabular-nums}

/* ── ГЕРОЙ ── */
.sv-hero{position:relative;padding:clamp(18px,3vw,34px) 0 clamp(44px,6vw,86px);overflow:hidden}
.sv-hero__bg{position:absolute;inset:0;z-index:0}
.sv-hero__bg img{width:100%;height:100%;object-fit:cover;object-position:50% 62%;opacity:.72}
.sv-hero__bg::after{content:'';position:absolute;inset:0;background:
 linear-gradient(180deg,rgba(5,7,11,.86) 0%,rgba(5,7,11,.66) 30%,rgba(5,7,11,.42) 56%,
  rgba(5,7,11,.86) 82%,var(--sv-bg) 100%)}
.sv-hero__in{position:relative;z-index:1}
.sv-back{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:500;
 color:var(--sv-dim);text-decoration:none;margin-bottom:clamp(28px,6vw,72px)}
.sv-back:hover{color:var(--sv-laser)}
.sv-hero h1{font-size:clamp(28px,4.5vw,58px);margin:16px 0 0;max-width:17ch;font-weight:700}
.sv-hero h1 em{font-style:normal;color:var(--sv-laser)}
.sv-hero__lead{margin-top:22px;max-width:52ch}
.sv-facts{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--sv-line);
 border:1px solid var(--sv-line);margin-top:clamp(30px,4.5vw,58px)}
.sv-facts div{background:rgba(10,14,21,.86);padding:16px 15px}
.sv-facts dt{font-size:10.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--sv-mute)}
.sv-facts dd{margin:8px 0 0;font-size:clamp(13.5px,1.2vw,16px);line-height:1.35;font-weight:500}

/* ── ЗАДАЧА ── */
.sv-task{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);
 gap:clamp(24px,3.6vw,60px)}
.sv-task p{font-size:clamp(15px,1.35vw,17px);line-height:1.75;color:var(--sv-dim)}
.sv-task p+p{margin-top:16px}
.sv-task b{color:var(--sv-txt);font-weight:600}
.sv-quote{margin-top:24px;border-left:2px solid var(--sv-laser);padding:6px 0 6px 20px;
 font-family:'Unbounded','Fira Sans',Arial,sans-serif;font-weight:400;
 font-size:clamp(16px,1.7vw,21px);line-height:1.5;letter-spacing:-.01em}

/* ── ТУМАН ── */
.sv-fog{position:relative;border:1px solid var(--sv-line);background:#000;overflow:hidden;
 margin-top:clamp(26px,3.6vw,44px)}
.sv-fog img{width:100%;display:block;opacity:.92}
.sv-fog__veil{position:absolute;left:0;right:0;bottom:0;top:0;pointer-events:none;
 background:linear-gradient(0deg,rgba(214,222,232,.92) 0%,rgba(200,210,224,.7) 34%,
  rgba(190,202,218,.34) 62%,rgba(190,202,218,0) 88%);
 transform:translateY(var(--fy,0%));opacity:var(--fo,1);
 transition:transform .18s linear,opacity .18s linear}
.sv-fog__cap{position:absolute;left:0;right:0;bottom:0;padding:20px 22px;
 background:linear-gradient(0deg,rgba(5,7,11,.92),rgba(5,7,11,0));
 font-size:13.5px;line-height:1.6;color:var(--sv-txt)}
.sv-fog__cap b{font-family:'Unbounded','Fira Sans',Arial,sans-serif;font-weight:500;
 display:block;margin-bottom:5px;color:var(--sv-laser);font-size:12px;letter-spacing:.06em}
.sv-fog__scale{position:absolute;right:14px;top:14px;bottom:88px;width:52px;
 display:flex;flex-direction:column;justify-content:space-between;align-items:flex-end;
 font-size:10px;letter-spacing:.08em;color:rgba(255,255,255,.7);text-align:right}

/* ── ПУЛЬТ МЭППИНГА ── */
.sv-desk{margin-top:clamp(26px,3.6vw,44px);border:1px solid var(--sv-line);
 background:var(--sv-panel);box-shadow:0 50px 90px -60px #000}
.sv-desk__bar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;padding:13px 16px;
 border-bottom:1px solid var(--sv-line);font-size:11.5px;letter-spacing:.05em;color:var(--sv-dim)}
.sv-desk__live{display:inline-flex;align-items:center;gap:7px;color:var(--sv-laser);font-weight:600}
.sv-desk__live i{width:8px;height:8px;border-radius:50%;background:currentColor;
 animation:sv-blink 1.8s steps(1,end) infinite}
@keyframes sv-blink{0%,60%{opacity:1}61%,100%{opacity:.2}}
.sv-desk__read{margin-left:auto;display:flex;gap:16px;flex-wrap:wrap}
.sv-desk__read b{font-family:'Unbounded','Fira Sans',Arial,sans-serif;font-weight:500;
 color:var(--sv-txt);font-variant-numeric:tabular-nums}
.sv-desk__screen{position:relative;aspect-ratio:960/300;background:#000;overflow:hidden}
.sv-desk__screen img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 opacity:0;transition:opacity .4s ease}
.sv-desk__screen img.is-on{opacity:1}
.sv-zones{position:absolute;inset:0;width:100%;height:100%}
.sv-zones polygon{cursor:pointer;transition:opacity .28s ease;pointer-events:all}
.sv-zones .z-dark{fill:url(#svFade);opacity:0}
.sv-zones .z-on .z-dark{opacity:.94}
.sv-zones .z-hit{fill:transparent;stroke:rgba(255,255,255,.14);stroke-width:1;
 transition:stroke .2s ease,stroke-width .2s ease;vector-effect:non-scaling-stroke}
.sv-zones g:hover .z-hit{stroke:rgba(60,224,126,.9);stroke-width:2}
.sv-zones .z-on .z-hit{stroke:rgba(255,81,64,.9);stroke-width:2}
.sv-desk__tag{position:absolute;left:12px;top:11px;padding:4px 9px;background:rgba(5,7,11,.8);
 border:1px solid var(--sv-line);font-size:10.5px;letter-spacing:.14em;color:var(--sv-txt)}
.sv-stacks{display:grid;grid-template-columns:repeat(9,1fr);gap:1px;background:var(--sv-line);
 border-top:1px solid var(--sv-line)}
.sv-stack{background:var(--sv-bg2);border:0;padding:12px 4px 11px;cursor:pointer;color:var(--sv-dim);
 font:500 11px 'Fira Sans',Arial,sans-serif;text-align:center;transition:color .2s,background .2s}
.sv-stack b{display:block;font-family:'Unbounded','Fira Sans',Arial,sans-serif;font-weight:500;
 font-size:14px;color:var(--sv-laser);margin-bottom:4px;transition:color .2s}
.sv-stack:hover{background:#121924}
.sv-stack.is-off{color:var(--sv-mute)}
.sv-stack.is-off b{color:var(--sv-off)}
.sv-desk__scenes{display:grid;grid-template-columns:repeat(6,1fr);gap:1px;background:var(--sv-line);
 border-top:1px solid var(--sv-line)}
.sv-scene{position:relative;background:var(--sv-bg2);border:0;padding:0;cursor:pointer;display:block;
 overflow:hidden;aspect-ratio:16/7}
.sv-scene img{width:100%;height:100%;object-fit:cover;opacity:.45;transition:opacity .2s}
.sv-scene:hover img{opacity:.8}
.sv-scene.is-on img{opacity:1}
.sv-scene span{position:absolute;left:0;right:0;bottom:0;padding:12px 6px 5px;font-size:10.5px;
 font-weight:500;color:#fff;background:linear-gradient(0deg,rgba(5,7,11,.92),transparent)}
.sv-scene.is-on::after{content:'';position:absolute;inset:0;border:2px solid var(--sv-laser)}
.sv-desk__foot{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;
 padding:16px;border-top:1px solid var(--sv-line)}
.sv-desk__cap{font-size:13px;line-height:1.6;color:var(--sv-dim);max-width:64ch}
.sv-desk__cap b{color:var(--sv-txt);font-weight:600}
.sv-btn{font:600 12.5px 'Fira Sans',Arial,sans-serif;padding:11px 18px;cursor:pointer;
 background:transparent;border:1px solid var(--sv-line);color:var(--sv-txt);
 transition:border-color .2s,color .2s,background .2s;white-space:nowrap}
.sv-btn:hover{border-color:var(--sv-laser);color:var(--sv-laser)}
.sv-btn--fill{background:var(--sv-laser);border-color:var(--sv-laser);color:#04120A}
.sv-btn--fill:hover{color:#04120A;filter:brightness(1.08)}

/* ── РАЗРЕЗ ПЛОЩАДИ ── */
.sv-cut{margin-top:clamp(26px,3.6vw,44px);border:1px solid var(--sv-line);background:var(--sv-bg2)}
.sv-cut__scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.sv-cut svg{display:block;width:100%;height:auto;background:#05070B}
.sv-cut__foot{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;
 padding:16px;border-top:1px solid var(--sv-line)}
.sv-cut__cap{font-size:13px;line-height:1.6;color:var(--sv-dim);max-width:60ch}
.sv-cut__cap b{color:var(--sv-txt);font-weight:600}
.sv-cut .beam-ground,.sv-cut .shadow,.sv-cut .lbl-ground,.sv-cut .ground-rig{opacity:0;
 transition:opacity .45s ease}
.sv-cut .beam-tower,.sv-cut .tower,.sv-cut .lbl-tower{opacity:1;transition:opacity .45s ease}
.sv-cut.is-ground .beam-ground,.sv-cut.is-ground .shadow,.sv-cut.is-ground .lbl-ground,
.sv-cut.is-ground .ground-rig{opacity:1}
.sv-cut.is-ground .beam-tower,.sv-cut.is-ground .lbl-tower{opacity:0}
.sv-cut.is-ground .tower{opacity:.15}

/* ── КАРТОЧКИ ТЕХНИКИ ── */
.sv-kit{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:clamp(24px,3.4vw,42px)}
.sv-fig{margin:0;border:1px solid var(--sv-line);background:var(--sv-bg2)}
.sv-fig img{width:100%}
.sv-fig figcaption{padding:13px 15px;font-size:12.5px;line-height:1.6;color:var(--sv-dim)}
.sv-fig figcaption b{display:block;color:var(--sv-txt);font-weight:600;margin-bottom:4px}

/* ── ЦИФРЫ ── */
.sv-nums{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--sv-line);
 border:1px solid var(--sv-line);margin-top:clamp(26px,3.6vw,44px)}
.sv-nums div{background:var(--sv-bg2);padding:22px 18px}
.sv-nums b{display:block;font-family:'Unbounded','Fira Sans',Arial,sans-serif;font-weight:500;
 font-size:clamp(24px,2.8vw,34px);letter-spacing:-.03em;color:var(--sv-laser);line-height:1}
.sv-nums i{display:block;font-style:normal;margin-top:7px;font-size:12px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--sv-amber)}
.sv-nums span{display:block;margin-top:11px;font-size:12.5px;line-height:1.6;color:var(--sv-dim)}

/* ── СЛОНЫ ── */
.sv-split{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);
 gap:clamp(24px,3.4vw,54px);align-items:center}
.sv-split p{font-size:clamp(15px,1.35vw,17px);line-height:1.75;color:var(--sv-dim)}
.sv-split p+p{margin-top:16px}
.sv-split b{color:var(--sv-txt);font-weight:600}

/* ── ПРИЛОЖЕНИЕ ── */
.sv-ar{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);
 gap:clamp(24px,3.4vw,54px);align-items:center;margin-top:clamp(26px,3.6vw,44px)}
.sv-phone{border:1px solid var(--sv-line);border-radius:26px;padding:10px;background:#0A0E15;
 position:relative;box-shadow:0 40px 70px -50px #000}
.sv-phone__scr{position:relative;border-radius:18px;overflow:hidden;aspect-ratio:9/16;background:#000}
.sv-phone__scr img{width:100%;height:100%;object-fit:cover;opacity:.72}
.sv-phone__hud{position:absolute;inset:0}
.sv-phone__mark{position:absolute;width:76px;height:76px;margin:-38px 0 0 -38px;
 border:1.5px solid var(--sv-laser);border-radius:50%;
 transition:left .5s cubic-bezier(.4,0,.2,1),top .5s cubic-bezier(.4,0,.2,1)}
.sv-phone__mark::after{content:'';position:absolute;inset:-7px;border-radius:50%;
 border:1px dashed rgba(60,224,126,.4);animation:sv-spin 9s linear infinite}
@keyframes sv-spin{to{transform:rotate(360deg)}}
.sv-phone__name{position:absolute;left:12px;right:12px;bottom:12px;padding:10px 12px;
 background:rgba(5,7,11,.82);border:1px solid var(--sv-line);font-size:12px;line-height:1.5;
 color:var(--sv-txt)}
.sv-phone__name b{display:block;font-family:'Unbounded','Fira Sans',Arial,sans-serif;
 font-weight:500;font-size:12.5px;margin-bottom:4px;color:var(--sv-laser)}
.sv-phone__top{position:absolute;left:12px;top:12px;font-size:10px;letter-spacing:.16em;
 color:rgba(255,255,255,.75)}
.sv-chips{display:flex;flex-wrap:wrap;gap:9px;margin-top:22px}
.sv-chip{font:500 12.5px 'Fira Sans',Arial,sans-serif;padding:10px 15px;cursor:pointer;
 background:transparent;border:1px solid var(--sv-line);color:var(--sv-dim);transition:.2s}
.sv-chip:hover{color:var(--sv-txt);border-color:rgba(255,255,255,.3)}
.sv-chip.is-on{border-color:var(--sv-laser);color:var(--sv-laser)}

/* ── ФИНАЛ ── */
.sv-final{border-top:1px solid var(--sv-line);padding-top:clamp(28px,4vw,54px);
 display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,3.4vw,56px)}
.sv-final p{font-size:clamp(15px,1.35vw,17px);line-height:1.75;color:var(--sv-dim)}
.sv-final p+p{margin-top:15px}
.sv-final b{color:var(--sv-txt);font-weight:600}
.sv-big{font-family:'Unbounded','Fira Sans',Arial,sans-serif;font-size:clamp(40px,7vw,90px);
 font-weight:700;line-height:.96;letter-spacing:-.045em;color:var(--sv-laser)}
.sv-big small{display:block;margin-top:18px;font-family:'Fira Sans',Arial,sans-serif;
 font-size:clamp(14px,1.35vw,16px);font-weight:400;line-height:1.7;color:var(--sv-dim);
 letter-spacing:0;max-width:40ch}
.sv-beams{display:block;width:100%;height:auto;margin-top:clamp(24px,3.4vw,40px);
 border:1px solid var(--sv-line);background:#05070B}
.sv-beams .ray{stroke-dasharray:4 8;animation:sv-ray 2.4s linear infinite}
@keyframes sv-ray{to{stroke-dashoffset:-24}}

/* ── ВИДЕО И ГАЛЕРЕЯ ── */
.sv-video{margin-top:clamp(26px,3.6vw,44px);border:1px solid var(--sv-line);background:#000}
.sv-video video{display:block;width:100%;height:auto;background:#000}
.sv-gal{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:clamp(26px,3.6vw,44px)}
.sv-gal figure{margin:0;border:1px solid var(--sv-line);background:var(--sv-bg2);overflow:hidden}
.sv-gal img{width:100%;aspect-ratio:3/2;object-fit:cover;transition:transform .5s ease}
.sv-gal figure:hover img{transform:scale(1.03)}

/* ── ПЛАНШЕТ ── */
@media (max-width:980px){
 .sv-facts{grid-template-columns:repeat(3,1fr)}
 .sv-facts div:nth-child(4),.sv-facts div:nth-child(5){grid-column:span 1}
 .sv-task,.sv-split,.sv-ar,.sv-final{grid-template-columns:1fr;gap:24px}
 .sv-nums{grid-template-columns:repeat(2,1fr)}
 .sv-kit{grid-template-columns:1fr 1fr}
 .sv-kit figure:last-child{grid-column:1/-1}
 .sv-gal{grid-template-columns:repeat(2,1fr)}
 .sv-desk__read{margin-left:0;width:100%}
 .sv-ar{max-width:640px}
}
/* ── ТЕЛЕФОН ── */
@media (max-width:640px){
 .sv__wrap{padding:0 18px}
 .sv-facts{grid-template-columns:repeat(2,1fr)}
 .sv-facts div:last-child{grid-column:1/-1}
 .sv-nums{grid-template-columns:1fr}
 .sv-kit{grid-template-columns:1fr}
 .sv-gal{grid-template-columns:1fr}
 .sv-desk__scenes{grid-template-columns:repeat(3,1fr)}
 .sv-stacks{grid-template-columns:repeat(9,1fr)}
 .sv-stack{padding:9px 1px;font-size:0}
 .sv-stack b{font-size:12px;margin-bottom:0}
 .sv-desk__bar{font-size:10.5px;gap:6px 12px}
 .sv-desk__read{gap:10px}
 .sv-btn{width:100%;text-align:center}
 .sv-desk__foot,.sv-cut__foot{flex-direction:column;align-items:stretch}
 .sv-fog__cap{padding:14px 15px;font-size:12.5px}
 .sv-phone{max-width:300px;margin:0 auto}
 /* схему разреза на телефоне листаем вбок, иначе подписи нечитаемы */
 .sv-cut svg{min-width:660px}
}
/* ── ЛАНДШАФТ ТЕЛЕФОНА ── */
@media (max-height:460px) and (orientation:landscape){
 .sv-sec{padding:44px 0}
 .sv-hero{padding-bottom:40px}
 .sv-back{margin-bottom:20px}
 .sv-phone{max-width:220px}
}
@media (prefers-reduced-motion:reduce){
 .sv-r{opacity:1;transform:none;transition:none}
 .sv-desk__live i,.sv-phone__mark::after,.sv-beams .ray{animation:none}
 .sv-fog__veil{transition:none}
}
</style>"""


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ─── секции ─────────────────────────────────────────────────────────────────
def hero():
    facts = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(k), esc(v)) for k, v in FACTS)
    return f'''<section class="sv-hero">
<div class="sv-hero__bg"><img src="{PH_ANGELS}" width="1262" height="841"
 alt="Проекция ангелов на фасаде здания Правительства Ставропольского края"
 fetchpriority="high" decoding="async"></div>
<div class="sv__wrap sv-hero__in">
<a class="sv-back" href="/project">← Проекты</a>
<div class="sv__eyebrow">3D Mapping · Ставрополь · 13 декабря 2019</div>
<h1>Восемь минут, за которые здание Правительства <em>перестало быть зданием</em></h1>
<p class="sv__lead sv-hero__lead">Открытие новогодних мероприятий на площади Ленина.
27 проекторов в башнях за 97 метров от фасада, четыре лазера, зенитные прожекторы
и дополненная реальность на площади, куда пришли больше 25 тысяч человек.</p>
<dl class="sv-facts">{facts}</dl>
</div></section>'''


def task():
    return f'''<section class="sv-sec"><div class="sv__wrap"><div class="sv-task sv-r">
<div><div class="sv__eyebrow">Задача</div>
<h2 class="sv-sec__h">Собрать площадь и удержать её</h2>
<div class="sv-quote">Шоу открывало новогоднюю программу города: следом шли ещё
полторы сотни мероприятий.</div></div>
<div>
<p>Администрация города Ставрополя заказала 3D mapping шоу на открытие новогодних
мероприятий. Площадкой стала площадь Ленина, экраном: здание Правительства
Ставропольского края, поводом: зажжение главной ёлки края высотой 25 метров.</p>
<p><b>Главный вопрос был не в картинке, а в людях.</b> На площадь ожидали больше
25 тысяч человек. Им нужно было где-то стоять, что-то видеть с любой точки
и чем-то заняться в час ожидания до старта.</p>
<p>Из этого выросли три решения, которые определили проект: технику убрать
с площади в башни, картинку строить на перекрытии проекторных стеков, а ожидание
занять приложением дополненной реальности.</p>
</div></div></div></section>'''


def fog():
    return f'''<section class="sv-sec" id="svFogSec"><div class="sv__wrap">
<div class="sv-r"><div class="sv__eyebrow">13 декабря, вечер</div>
<h2 class="sv-sec__h">За час до старта площадь исчезла</h2>
<p class="sv-sec__sub">На Ставрополь опустился густой туман. Он плотно лёг на площадь
и скрыл от глаз декорации и здания. Со стороны это выглядело как сорванное
мероприятие: проекция на фасад, которого не видно, невозможна.</p></div>
<div class="sv-fog sv-r" id="svFog">
<img src="{IMG}/fog.jpg" width="1120" height="510" loading="lazy" decoding="async"
 alt="Ковровый орнамент на фасаде и туман над площадью Ленина в Ставрополе">
<div class="sv-fog__veil" aria-hidden="true"></div>
<div class="sv-fog__scale" aria-hidden="true"><span>крыша</span><span>карниз</span><span>площадь</span></div>
<p class="sv-fog__cap"><b id="svFogTag">Туман на уровне площади</b>
<span id="svFogTxt">Прокрутите страницу: туман поведёт себя так же, как в тот вечер.</span></p>
</div>
<p class="sv-sec__sub">Шоу не отменили. Площадь заполнили зрители, и тёплый воздух
над толпой поднял низкий туман до высоты здания. Внизу осталась прозрачная среда,
достаточная для качественной проекции, а поднявшийся слой сработал на нас:
<b>в тумане лучи проекторов и лазеров получили объём</b>, которого не бывает
в чистом воздухе.</p>
<p class="sv-note">Логика вечера описана в отчёте по проекту. Анимация тумана на этой
странице: иллюстрация, а не запись метеоданных.</p>
</div></section>'''


def desk():
    imgs = ''.join(
        '<img src="%s/%s.jpg" width="960" height="300" alt="Сцена шоу: %s"%s%s decoding="async">'
        % (IMG, f, esc(name.lower()), ' class="is-on"' if i == 0 else '',
           '' if i == 0 else ' loading="lazy"')
        for i, (f, name, _cap) in enumerate(SCENES))
    zones = ''.join(
        '<g data-z="%d"><polygon class="z-dark" points="%s"></polygon>'
        '<polygon class="z-hit" points="%s"><title>Стек %d: 3 проектора</title></polygon></g>'
        % (i, zone_pts(i), zone_pts(i), i + 1)
        for i in range(ZONES))
    stacks = ''.join(
        '<button class="sv-stack" type="button" data-z="%d"'
        ' aria-label="Выключить стек %d">'
        '<b>%d</b>3 прибора</button>' % (i, i + 1, i + 1)
        for i in range(ZONES))
    scenes = ''.join(
        '<button class="sv-scene%s" type="button" data-s="%d" aria-label="Сцена: %s">'
        '<img src="%s/%s.jpg" width="480" height="150" loading="lazy" decoding="async" alt="">'
        '<span>%s</span></button>'
        % (' is-on' if i == 0 else '', i, esc(name), IMG, f, esc(name))
        for i, (f, name, _cap) in enumerate(SCENES))
    return f'''<section class="sv-sec"><div class="sv__wrap">
<div class="sv-r"><div class="sv__eyebrow">Решение · свет</div>
<h2 class="sv-sec__h">Пульт: 27 проекторов на один фасад</h2>
<p class="sv-sec__sub">27 проекторов <b>Epson EB-L1755U</b> собрали в стеки и развели
по башням в 97 метрах от здания. Суммарный поток: <b>410 000 люмен</b>, на поверхности
фасада это дало <b>150 люкс на квадратный метр</b>. Каждый стек светит в свою зону,
зоны перекрываются по краям: так собирается одна непрерывная картинка и так же
страхуется отказ отдельного прибора.</p></div>
<div class="sv-desk sv-r" id="svDesk">
<div class="sv-desk__bar">
<span class="sv-desk__live"><i></i>LIVE</span>
<span id="svSceneName">{esc(SCENES[0][1])}</span>
<span class="sv-desk__read">
<span>в работе <b id="svProj">{PROJ_TOTAL}/{PROJ_TOTAL}</b></span>
<span>поток <b id="svLm">410 000</b> лм</span>
<span>на фасаде <b id="svLux">150</b> лк/м²</span></span></div>
<div class="sv-desk__screen">{imgs}
<svg class="sv-zones" id="svZones" viewBox="0 0 960 300" preserveAspectRatio="none"
 role="group" aria-label="Зоны проекции на фасаде">
<defs><linearGradient id="svFade" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#04070C" stop-opacity="0"></stop>
<stop offset="0.16" stop-color="#04070C" stop-opacity="1"></stop>
<stop offset="0.84" stop-color="#04070C" stop-opacity="1"></stop>
<stop offset="1" stop-color="#04070C" stop-opacity="0"></stop></linearGradient></defs>
{zones}</svg>
<div class="sv-desk__tag">ФАСАД · 9 ЗОН</div></div>
<div class="sv-stacks">{stacks}</div>
<div class="sv-desk__scenes">{scenes}</div>
<div class="sv-desk__foot">
<p class="sv-desk__cap" id="svDeskCap"><b>{esc(SCENES[0][1])}.</b> {esc(SCENES[0][2])}</p>
<button class="sv-btn sv-btn--fill" type="button" id="svAllOn">Включить все стеки</button>
</div></div>
<p class="sv-note">Нажмите на зону прямо на фасаде или на номер стека внизу:
зона погаснет, а соседние стеки удержат только стык. Разбивка на девять зон:
наша реконструкция по съёмке. В кейсе зафиксированы 27 проекторов, стековая
установка, башни и дистанция 97 метров. Кадры сняты неподвижной верхней камерой,
поэтому геометрия фасада во всех сценах одна и та же.</p>
</div></section>'''


def cut():
    return f'''<section class="sv-sec"><div class="sv__wrap">
<div class="sv-r"><div class="sv__eyebrow">Решение · оптика</div>
<h2 class="sv-sec__h">Почему башни, а не приборы на площади</h2>
<p class="sv-sec__sub">Проекторы весят 24 килограмма и допускают проецирование
под любым углом, а среднефокусные объективы <b>ELPLM10</b> позволили увести луч
выше голов и декораций. Приборы подняли в специальные башни и отнесли на 97 метров:
площадь осталась под зрителей, а на фасаде нет теней от ёлок, конструкций
и самих зрителей.</p></div>
<div class="sv-cut sv-r" id="svCut">
<div class="sv-cut__scroll">
<svg viewBox="0 148 960 264" role="img"
 aria-label="Разрез площади: башня с проекторами в 97 метрах от фасада, луч проходит над головами зрителей">
<defs>
<linearGradient id="svBeam" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#3CE07E" stop-opacity=".5"></stop>
<stop offset="1" stop-color="#3CE07E" stop-opacity=".1"></stop></linearGradient>
<linearGradient id="svBeamG" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#FF5140" stop-opacity=".45"></stop>
<stop offset="1" stop-color="#FF5140" stop-opacity=".1"></stop></linearGradient>
</defs>
<!-- масштаб схемы: 1 метр = 8 px, земля на y=340 -->
<line x1="0" y1="340" x2="960" y2="340" stroke="#243040" stroke-width="1"></line>
<!-- здание Правительства: около 20 метров высотой -->
<rect x="831" y="180" width="119" height="160" fill="#0E141D" stroke="#2A3648"></rect>
<g fill="#182231">
<rect x="845" y="200" width="12" height="16"></rect><rect x="869" y="200" width="12" height="16"></rect>
<rect x="893" y="200" width="12" height="16"></rect><rect x="917" y="200" width="12" height="16"></rect>
<rect x="845" y="232" width="12" height="16"></rect><rect x="869" y="232" width="12" height="16"></rect>
<rect x="893" y="232" width="12" height="16"></rect><rect x="917" y="232" width="12" height="16"></rect>
<rect x="845" y="264" width="12" height="16"></rect><rect x="869" y="264" width="12" height="16"></rect>
<rect x="893" y="264" width="12" height="16"></rect><rect x="917" y="264" width="12" height="16"></rect>
<rect x="845" y="296" width="12" height="16"></rect><rect x="869" y="296" width="12" height="16"></rect>
<rect x="893" y="296" width="12" height="16"></rect><rect x="917" y="296" width="12" height="16"></rect></g>
<!-- луч из башни: проходит над головами и накрывает фасад целиком -->
<polygon class="beam-tower" points="70,258 831,180 831,340 70,278" fill="url(#svBeam)"></polygon>
<!-- луч с уровня площади и тени на фасаде -->
<polygon class="beam-ground" points="70,318 831,180 831,340 70,334" fill="url(#svBeamG)"></polygon>
<g class="shadow" fill="#1A0A08" stroke="#FF5140" stroke-opacity=".45">
<rect x="831" y="300" width="119" height="40"></rect>
<rect x="831" y="250" width="119" height="16"></rect>
<rect x="831" y="220" width="119" height="10"></rect></g>
<g class="ground-rig">
<rect x="40" y="316" width="30" height="24" fill="#0E141D" stroke="#FF5140" stroke-opacity=".5"></rect>
<rect x="44" y="320" width="22" height="6" fill="#FF5140"></rect>
<rect x="44" y="328" width="22" height="6" fill="#FF5140" fill-opacity=".6"></rect></g>
<!-- башня со стеком из трёх приборов -->
<g class="tower">
<rect x="40" y="252" width="30" height="88" fill="#0E141D" stroke="#3CE07E" stroke-opacity=".45"></rect>
<line x1="40" y1="274" x2="70" y2="274" stroke="#243040"></line>
<line x1="40" y1="296" x2="70" y2="296" stroke="#243040"></line>
<line x1="40" y1="318" x2="70" y2="318" stroke="#243040"></line>
<rect x="44" y="256" width="22" height="6" fill="#3CE07E"></rect>
<rect x="44" y="264" width="22" height="6" fill="#3CE07E" fill-opacity=".72"></rect>
<rect x="44" y="272" width="22" height="6" fill="#3CE07E" fill-opacity=".48"></rect>
</g>
<!-- зрители: рост около 1,7 метра в том же масштабе -->
<g fill="#1B2534">
<rect x="120" y="326" width="6" height="14" rx="3"></rect><rect x="146" y="327" width="6" height="13" rx="3"></rect>
<rect x="172" y="326" width="6" height="14" rx="3"></rect><rect x="198" y="328" width="6" height="12" rx="3"></rect>
<rect x="224" y="326" width="6" height="14" rx="3"></rect><rect x="250" y="327" width="6" height="13" rx="3"></rect>
<rect x="276" y="326" width="6" height="14" rx="3"></rect><rect x="302" y="328" width="6" height="12" rx="3"></rect>
<rect x="328" y="326" width="6" height="14" rx="3"></rect><rect x="354" y="327" width="6" height="13" rx="3"></rect>
<rect x="380" y="326" width="6" height="14" rx="3"></rect><rect x="406" y="328" width="6" height="12" rx="3"></rect>
<rect x="432" y="326" width="6" height="14" rx="3"></rect><rect x="458" y="327" width="6" height="13" rx="3"></rect>
<rect x="484" y="326" width="6" height="14" rx="3"></rect><rect x="510" y="328" width="6" height="12" rx="3"></rect>
<rect x="536" y="326" width="6" height="14" rx="3"></rect><rect x="562" y="327" width="6" height="13" rx="3"></rect>
<rect x="588" y="326" width="6" height="14" rx="3"></rect><rect x="614" y="328" width="6" height="12" rx="3"></rect>
<rect x="640" y="326" width="6" height="14" rx="3"></rect></g>
<!-- у самого фасада зрителей нет: там ограждение и декорации -->
<line x1="676" y1="322" x2="676" y2="340" stroke="#243040" stroke-dasharray="3 4"></line>
<text x="684" y="334" fill="#4E5A69" font-size="11" font-family="Fira Sans, Arial">
ограждение</text>
<!-- размеры -->
<line x1="70" y1="372" x2="831" y2="372" stroke="#66717F" stroke-width="1"
 stroke-dasharray="3 5"></line>
<line x1="70" y1="366" x2="70" y2="378" stroke="#66717F"></line>
<line x1="831" y1="366" x2="831" y2="378" stroke="#66717F"></line>
<text x="450" y="394" fill="#8E9BAE" font-size="13" font-family="Fira Sans, Arial"
 text-anchor="middle">97 метров от башни до фасада</text>
<text x="40" y="240" fill="#3CE07E" font-size="13" font-family="Fira Sans, Arial"
 class="lbl-tower">Башня: стек из трёх приборов</text>
<text x="40" y="240" fill="#FF5140" font-size="13" font-family="Fira Sans, Arial"
 class="lbl-ground">Приборы на уровне площади</text>
<text x="950" y="172" fill="#8E9BAE" font-size="13" font-family="Fira Sans, Arial"
 text-anchor="end">Фасад, около 20 метров</text>
<text x="120" y="356" fill="#66717F" font-size="12" font-family="Fira Sans, Arial">
зрители, рост 1,7 м в том же масштабе</text>
<text x="825" y="316" fill="#FF5140" font-size="12" font-family="Fira Sans, Arial"
 text-anchor="end" class="lbl-ground">тени на фасаде</text>
<text x="950" y="404" fill="#4E5A69" font-size="11" font-family="Fira Sans, Arial"
 text-anchor="end">схема в масштабе 1 метр = 8 пикселей</text>
</svg></div>
<div class="sv-cut__foot">
<p class="sv-cut__cap" id="svCutCap"><b>Как сделали.</b> Луч идёт из башни поверх голов
и упирается в фасад целиком: зрители стоят прямо под ним и ничего не перекрывают.</p>
<button class="sv-btn" type="button" id="svCutBtn">Опустить приборы на площадь</button>
</div></div>
<div class="sv-kit sv-r">
<figure class="sv-fig"><img src="{IMG}/tower.jpg" width="1120" height="510" loading="lazy"
 decoding="async" alt="Башня с проекторами на площади Ленина"><figcaption>
<b>Башня</b>Стек приборов поднят над площадью, лучи идут поверх зрителей и декораций.
</figcaption></figure>
<figure class="sv-fig"><img src="{IMG}/rig.jpg" width="1120" height="510" loading="lazy"
 decoding="async" alt="Монтаж проекционного оборудования на ферме"><figcaption>
<b>Монтаж</b>Сборка и наводка шли днём, при свете: ночью выравнивать 27 зон уже поздно.
</figcaption></figure>
<figure class="sv-fig"><img src="{IMG}/laser-soft.jpg" width="1120" height="510" loading="lazy"
 decoding="async" alt="Лазерная графика в программе на планшете"><figcaption>
<b>Лазерная графика</b>Рисунок лазеров готовится и правится на площадке, прямо перед стартом.
</figcaption></figure>
</div></div></section>'''


def numbers():
    tiles = ''.join('<div><b class="sv-num">%s</b><i>%s</i><span>%s</span></div>'
                    % (esc(n), esc(u), esc(t)) for n, u, t in NUMBERS)
    return f'''<section class="sv-sec"><div class="sv__wrap">
<div class="sv-r"><div class="sv__eyebrow">Комплект</div>
<h2 class="sv-sec__h">Чем светили, чем били и чем звучали</h2>
<p class="sv-sec__sub">Проекция была только частью вечера. Вместе с ней работали лазеры,
зенитные прожекторы и фальконы, а всю программу вёл звуковой комплект на сто киловатт.</p></div>
<div class="sv-nums sv-r">{tiles}</div>
<div class="sv-kit sv-r">
<figure class="sv-fig"><img src="{IMG}/projector.jpg" width="1120" height="510" loading="lazy"
 decoding="async" alt="Проекционный блок на площади"><figcaption>
<b>Проектор</b>Epson EB-L1755U: 24 кг, лазерный источник света, среднефокусный объектив ELPLM10.
</figcaption></figure>
<figure class="sv-fig"><img src="{IMG}/desk.jpg" width="1120" height="510" loading="lazy"
 decoding="async" alt="Микшерный пульт на площадке"><figcaption>
<b>Пульт</b>Свет, видео и звук сводятся в одной точке: шоу идёт по таймкоду без права на дубль.
</figcaption></figure>
<figure class="sv-fig"><img src="{IMG}/flags.jpg" width="1120" height="510" loading="lazy"
 decoding="async" alt="Флаги России и Ставропольского края над площадью"><figcaption>
<b>Площадь Ленина</b>Главная площадь края: здание Правительства, ёлка 25 метров и место
для 25 тысяч человек.</figcaption></figure>
</div></div></section>'''


def elephants():
    return f'''<section class="sv-sec"><div class="sv__wrap"><div class="sv-split sv-r">
<div><div class="sv__eyebrow">Содержание</div>
<h2 class="sv-sec__h">Слоны на крыше парламента</h2>
<p>Восьмиминутное шоу ломало привычные очертания здания и закручивало в нём образы края.
В финале на крыше здания Правительства появились слоны, затрубили и дали сигнал
к яркой развязке.</p>
<p><b>Слон для Ставрополья не случайный зверь.</b> Край называют родиной слонов:
здесь нашли больше сотни остатков древних хоботных, а в краевом музее стоят два скелета
южного слона Archidiskodon meridionalis, которые жили около двух миллионов лет назад.
Один из них, найденный в 1960 году под Георгиевском, сохранился на 80 процентов.</p>
<p>Поэтому образ читался без пояснений: жители узнали своего слона на своём здании.</p>
<p class="sv-note">Факты о южных слонах: по материалам Ставропольского краеведческого музея
и публикациям о его коллекции.</p></div>
<figure class="sv-fig"><img src="{PH_ELEPH}" width="1262" height="841" loading="lazy"
 decoding="async" alt="Слоны на фасаде здания Правительства Ставропольского края">
<figcaption><b>Финал шоу</b>Слоны идут по фасаду длиной в целый квартал.</figcaption></figure>
</div></div></section>'''


def ar():
    chips = ''.join('<button class="sv-chip%s" type="button" data-h="%d">%s</button>'
                    % (' is-on' if i == 0 else '', i, esc(n))
                    for i, (n, _d) in enumerate(AR_HEROES))
    return f'''<section class="sv-sec"><div class="sv__wrap">
<div class="sv-r"><div class="sv__eyebrow">Решение · ожидание</div>
<h2 class="sv-sec__h">StavAR: чем занять площадь до старта</h2>
<p class="sv-sec__sub">Люди приходят на площадь заранее и стоят в темноте и на морозе.
Час ожидания способен испортить впечатление от любого шоу, поэтому под вечер сделали
бесплатное приложение дополненной реальности. Любой желающий скачивал его, искал
по площади сказочных персонажей и снимал с ними селфи. Приложению нужны были только
интернет и калибровка компаса.</p></div>
<div class="sv-ar sv-r" id="svAr">
<div class="sv-phone">
<div class="sv-phone__scr">
<img src="{IMG}/crowd.jpg" width="1120" height="510" loading="lazy" decoding="async"
 alt="Площадь Ленина, зрители с телефонами">
<div class="sv-phone__hud">
<div class="sv-phone__top">STAVAR · ПЛОЩАДЬ ЛЕНИНА</div>
<div class="sv-phone__mark" id="svArMark" style="left:52%;top:44%"></div>
<p class="sv-phone__name"><b id="svArName">{esc(AR_HEROES[0][0])}</b>
<span id="svArDesc">{esc(AR_HEROES[0][1])}</span></p>
</div></div></div>
<div><p class="sv-sec__sub" style="margin-top:0">Персонажи стояли по разным точкам площади,
поэтому ожидание превращалось в маршрут: чтобы собрать всех, нужно было пройти площадь
насквозь. Это же развело толпу равномернее по площадке.</p>
<div class="sv-chips">{chips}</div>
<p class="sv-note">Персонажи и механика приложения: по публикациям о вечере.
Снимок в рамке телефона: реальный кадр площади, метка условная.</p></div>
</div></div></section>'''


def finale():
    return f'''<section class="sv-sec"><div class="sv__wrap"><div class="sv-final sv-r">
<div><div class="sv__eyebrow">Финал</div>
<div class="sv-big sv-num">8:00<small>Столько длилось 3D mapping шоу. После него площадь
не разошлась: фасад превратился в экран под управлением виджея, и началась дискотека.</small></div>
</div>
<div><p>Вся световая энергия проекции собралась в четырёх точках здания, и мощные лучи
ушли из Правительства в огромную мультимедийную ёлку. <b>Это был переход, а не финал:</b>
свет ушёл с фасада и вернулся на площадь, к зрителям.</p>
<p>Дальше работали все приборы площадки сразу. Лазеры задавали пульсацию над головами,
зенитные прожекторы рисовали в небе фигуры длиной в несколько километров, а здание
Правительства держало ритм как самый большой в городе экран.</p>
<p>Туман, который утром считали угрозой срыва, к этому моменту стал материалом:
в нём было видно каждый луч.</p></div></div>
<svg class="sv-beams sv-r" viewBox="0 0 960 220" role="img"
 aria-label="Схема финала: четыре луча из здания Правительства уходят в ёлку">
<rect x="40" y="96" width="470" height="86" fill="#0A0E15" stroke="#243040"></rect>
<g fill="#3CE07E"><circle cx="90" cy="104" r="4"></circle><circle cx="230" cy="104" r="4"></circle>
<circle cx="360" cy="104" r="4"></circle><circle cx="480" cy="104" r="4"></circle></g>
<g stroke="#3CE07E" stroke-width="1.6" class="ray" fill="none">
<line x1="90" y1="104" x2="770" y2="40"></line><line x1="230" y1="104" x2="770" y2="40"></line>
<line x1="360" y1="104" x2="770" y2="40"></line><line x1="480" y1="104" x2="770" y2="40"></line></g>
<polygon points="770,40 812,182 728,182" fill="#0E1B16" stroke="#3CE07E" stroke-opacity=".6"></polygon>
<circle cx="770" cy="40" r="6" fill="#3CE07E"></circle>
<text x="40" y="206" fill="#8E9BAE" font-size="13" font-family="Fira Sans, Arial">
Здание Правительства, четыре точки сбора света</text>
<text x="836" y="126" fill="#8E9BAE" font-size="13" font-family="Fira Sans, Arial">Ёлка, 25 м</text>
</svg>
<div class="sv-kit sv-r">
<figure class="sv-fig"><img src="{IMG}/tree-laser.jpg" width="1120" height="510" loading="lazy"
 decoding="async" alt="Зелёный лазерный луч уходит в вершину ёлки"><figcaption>
<b>Луч в ёлку</b>Тот самый переход от фасада к площади.</figcaption></figure>
<figure class="sv-fig"><img src="{IMG}/facade-laser.jpg" width="1120" height="510" loading="lazy"
 decoding="async" alt="Лазерная графика по фасаду и зрители на площади"><figcaption>
<b>Лазеры по фасаду</b>Графика лазеров ложилась поверх проекции, не споря с ней по яркости.
</figcaption></figure>
<figure class="sv-fig"><img src="{IMG}/crowd.jpg" width="1120" height="510" loading="lazy"
 decoding="async" alt="Дискотека на площади Ленина под лучами лазеров"><figcaption>
<b>Дискотека</b>Площадь осталась стоять и после шоу: это и есть результат вечера.
</figcaption></figure>
</div></div></section>'''


def video():
    gal = ''.join('<figure><img src="%s" width="1262" height="841" loading="lazy"'
                  ' decoding="async" alt="%s"></figure>' % (src, esc(alt))
                  for src, alt in GALLERY)
    return f'''<section class="sv-sec"><div class="sv__wrap">
<div class="sv-r"><div class="sv__eyebrow">Съёмка вечера</div>
<h2 class="sv-sec__h">Как это выглядело с площади</h2></div>
<div class="sv-video sv-r"><video controls preload="none" playsinline
 poster="{IMG}/poster.jpg" width="1280" height="720">
<source src="{VIDEO}" type="video/mp4">Ваш браузер не поддерживает видео.</video></div>
<div class="sv-gal sv-r">{gal}</div>
</div></section>'''


PAGE_JS = """<script>(function(){
var d=document,RM=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;

// ── появление блоков ──
var rev=[].slice.call(d.querySelectorAll('.sv-r'));
if(window.IntersectionObserver&&!RM){
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},
  {rootMargin:'0px 0px -8% 0px'});
 rev.forEach(function(n){io.observe(n);});
}else{rev.forEach(function(n){n.classList.add('in');});}

// ── пульт мэппинга ──
var SCENES=[__SCENES__],TOTAL=__TOTAL__,ZN=__ZONES__,LM=__LM__,LUX=__LUX__;
var zonesSvg=d.getElementById('svZones'),deskCap=d.getElementById('svDeskCap'),
    sceneName=d.getElementById('svSceneName'),projEl=d.getElementById('svProj'),
    lmEl=d.getElementById('svLm'),luxEl=d.getElementById('svLux'),
    allBtn=d.getElementById('svAllOn'),
    shots=[].slice.call(d.querySelectorAll('.sv-desk__screen img')),
    sceneBtns=[].slice.call(d.querySelectorAll('.sv-scene')),
    stackBtns=[].slice.call(d.querySelectorAll('.sv-stack')),
    zoneGs=zonesSvg?[].slice.call(zonesSvg.querySelectorAll('g[data-z]')):[],
    off=[];

function fmt(n){return String(Math.round(n)).replace(/\\B(?=(\\d{3})+(?!\\d))/g,'\\u00A0');}

function paintDesk(){
 var on=TOTAL-off.length*(TOTAL/ZN);
 if(projEl)projEl.textContent=Math.round(on)+'/'+TOTAL;
 if(lmEl)lmEl.textContent=fmt(LM*on/TOTAL);
 if(luxEl)luxEl.textContent=fmt(LUX*on/TOTAL);
 zoneGs.forEach(function(g,i){g.classList.toggle('z-on',off.indexOf(i)>=0);});
 stackBtns.forEach(function(b,i){b.classList.toggle('is-off',off.indexOf(i)>=0);
  b.setAttribute('aria-pressed',off.indexOf(i)>=0?'true':'false');});
 if(allBtn)allBtn.hidden=!off.length;
 if(deskCap){
  if(!off.length){var s=SCENES[cur];deskCap.innerHTML='<b>'+s[0]+'.</b> '+s[1];}
  else if(off.length===1)deskCap.innerHTML='<b>Стек '+(off[0]+1)+' погас.</b> '+
   'На фасаде тёмная полоса: соседние стеки достают только до стыка, потому что '+
   'перекрытие рассчитано на сведение картинки, а не на подмену целой зоны.';
  else deskCap.innerHTML='<b>Выключено стеков: '+off.length+'.</b> '+
   'Картинка распалась на куски. Так выглядит фасад, если экономить на резерве '+
   'и на количестве приборов.';
 }
}

function toggle(i){
 var k=off.indexOf(i);
 if(k>=0)off.splice(k,1);else off.push(i);
 paintDesk();
}
zoneGs.forEach(function(g){g.addEventListener('click',function(){toggle(+g.getAttribute('data-z'));});});
stackBtns.forEach(function(b){b.addEventListener('click',function(){toggle(+b.getAttribute('data-z'));});});
if(allBtn)allBtn.addEventListener('click',function(){off=[];paintDesk();});

var cur=0;
function setScene(i){
 cur=i;
 shots.forEach(function(n,k){n.classList.toggle('is-on',k===i);});
 sceneBtns.forEach(function(b,k){b.classList.toggle('is-on',k===i);});
 if(sceneName)sceneName.textContent=SCENES[i][0];
 paintDesk();
}
sceneBtns.forEach(function(b){b.addEventListener('click',function(){setScene(+b.getAttribute('data-s'));});});
if(zoneGs.length)paintDesk();

// ── разрез площади ──
var cut=d.getElementById('svCut'),cutBtn=d.getElementById('svCutBtn'),
    cutCap=d.getElementById('svCutCap');
if(cutBtn)cutBtn.addEventListener('click',function(){
 var g=cut.classList.toggle('is-ground');
 cutBtn.textContent=g?'Вернуть приборы в башню':'Опустить приборы на площадь';
 cutCap.innerHTML=g?'<b>Если поставить приборы на площадь.</b> Луч идёт снизу вверх '+
  'через толпу и декорации: на фасаде появляются тени, а сама техника занимает место, '+
  'где должны стоять зрители.'
  :'<b>Как сделали.</b> Луч идёт из башни поверх голов и упирается в фасад целиком: '+
  'зрители стоят прямо под ним и ничего не перекрывают.';
});

// ── туман по скроллу ──
var fog=d.getElementById('svFog'),fogTag=d.getElementById('svFogTag'),
    fogTxt=d.getElementById('svFogTxt'),fogVis=false;
var FOG=[['Туман на уровне площади',
  'Плотный слой лёг на площадь и скрыл декорации и здания. Проекции не на что ложиться.'],
 ['Площадь заполняется',
  'Зрители занимают площадь. Тёплый воздух над толпой поднимает нижний слой тумана.'],
 ['Туман поднялся до крыши',
  'Внизу осталась прозрачная среда, достаточная для проекции, а поднявшийся слой дал лучам объём.']];
if(fog&&window.IntersectionObserver){
 new IntersectionObserver(function(es){fogVis=es[0].isIntersecting;if(fogVis)fogPaint();},
  {rootMargin:'80px'}).observe(fog);
}
function fogPaint(){
 if(!fog)return;
 var r=fog.getBoundingClientRect(),vh=window.innerHeight||1;
 // 0 в момент появления снизу, 1 когда блок уходит вверх
 var p=1-(r.top+r.height*0.35)/(vh*0.92);
 p=Math.max(0,Math.min(1,p));
 fog.style.setProperty('--fy',(-p*86).toFixed(1)+'%');
 fog.style.setProperty('--fo',(1-p*0.55).toFixed(3));
 var i=p<0.34?0:(p<0.68?1:2);
 if(fogTag&&fogTag.getAttribute('data-i')!==String(i)){
  fogTag.setAttribute('data-i',String(i));
  fogTag.textContent=FOG[i][0];fogTxt.textContent=FOG[i][1];
 }
}
function onScroll(){if(fogVis&&!RM)fogPaint();}
window.addEventListener('scroll',onScroll,{passive:true});
window.addEventListener('resize',onScroll);
fogPaint();

// ── персонажи StavAR ──
var HEROES=[__HEROES__],POS=[['52%','44%'],['30%','62%'],['70%','30%'],['42%','74%']];
var arName=d.getElementById('svArName'),arDesc=d.getElementById('svArDesc'),
    arMark=d.getElementById('svArMark'),
    chips=[].slice.call(d.querySelectorAll('.sv-chip'));
chips.forEach(function(b){b.addEventListener('click',function(){
 var i=+b.getAttribute('data-h');
 chips.forEach(function(n,k){n.classList.toggle('is-on',k===i);});
 if(arName)arName.textContent=HEROES[i][0];
 if(arDesc)arDesc.textContent=HEROES[i][1];
 if(arMark){arMark.style.left=POS[i][0];arMark.style.top=POS[i][1];}
});});
})();</script>"""

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
                 '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
                 '{"@type":"ListItem","position":2,"name":"3D Mapping шоу в Ставрополе",'
                 '"item":"' + URL + '"}]}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>3D Mapping шоу в Ставрополе: 27 проекторов на здание Правительства | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: 3D mapping шоу на открытии новогодних мероприятий в Ставрополе 13 декабря 2019. 27 проекторов Epson EB-L1755U в башнях за 97 метров от фасада, 410 000 люмен, четыре лазера, дополненная реальность и более 25 000 зрителей на площади Ленина.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="3D Mapping шоу в Ставрополе | кейс Hand Marketing">
<meta property="og:description" content="Восемь минут проекции на здание Правительства края: 27 проекторов в башнях, 410 000 люмен, лазеры в ёлку и 25 тысяч человек на площади.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{PH_ANGELS}">
<meta property="og:site_name" content="Hand Marketing"><meta property="og:locale" content="ru_RU">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/unbounded-fira.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def js():
    scenes = ','.join("['%s','%s']" % (name.replace("'", "\\'"), cap.replace("'", "\\'"))
                      for _f, name, cap in SCENES)
    heroes = ','.join("['%s','%s']" % (n.replace("'", "\\'"), t.replace("'", "\\'"))
                      for n, t in AR_HEROES)
    return (PAGE_JS.replace('__SCENES__', scenes).replace('__HEROES__', heroes)
            .replace('__TOTAL__', str(PROJ_TOTAL)).replace('__ZONES__', str(ZONES))
            .replace('__LM__', str(LM_TOTAL)).replace('__LUX__', str(LUX_TOTAL)))


def build():
    return (HEAD + rc.header() + '<main class="sv">' + hero() + task() + fog() + desk() +
            cut() + numbers() + elephants() + ar() + finale() + video() +
            '</main><a id="lead"></a>' + rc.footer() + rc.JS + js() + BREADCRUMB_LD +
            '</body></html>')


if __name__ == '__main__':
    out = os.path.join(ROOT, '3d', 'stavropol')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    # index-a2.html это деплой-источник (workflow переименовывает его в index.html)
    # и затёр бы кастомную страницу на проде.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('удалён устаревший index-a2.html')
    print('written', os.path.join(out, 'index.html'))
