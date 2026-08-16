#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/eaton/index.html: кейс «Презентационный ролик Eaton
для международной выставки».

Первоисточник один: сам ролик media/eaton-presentation.mp4 (3:37, 1024×576,
английская дорожка, русские субтитры вшиты в картинку). Ничего не придумано.
Монтажная раскладка (79 склеек, девять источников), три московских блока и
58 реплик закадрового текста сняты с файла скриптом
scripts/video-eaton-assets.py, результат лежит в video_eaton_map.json.

Идея страницы. Работа тут была не «снять красиво», а собрать одно целое из
материала, у которого нет ничего общего: корпоративные слайды на английском,
эфир RT со студийным светом, записи с экрана браузера, зимняя съёмка
мероприятия, архив клиента. Значит, страница должна показывать не кадры,
а швы: откуда каждый кусок и чем закрыты дыры.

Отсюда механики:

1. «Монтажный лист» (сигнатурная). Вся лента 217 секунд одной полосой, каждый
   кадр блоком в реальную длину и цветом источника. Клик перематывает плеер.
   Фильтр по источнику гасит всё остальное в штриховку: нажимаешь «съёмка
   Москвы», и от ролика остаются три островка на 35 секунд, а счётчик
   пересчитывает метраж. Такого разбора на сайте ещё не было.
2. Три московских блока с контекстом: что стоит слева и справа от каждого.
   Видно, что съёмка города это не украшение, а стыковочный материал.
3. Дорожка голоса на той же оси: 58 реплик, внутри каждой полосы отмечены
   склейки, которые она перекрывает. 31 реплика из 58 тянется через монтажный
   стык, поэтому разнородная картинка читается как один рассказ.

Шрифты — Piazzolla (заголовки и текст) и Martian Mono (таймкоды, номера
склеек), self-host: /fonts/piazzolla-martian.css. Сериф взят намеренно:
страница это разбор чужого монтажа, документ, а не витрина. Палитра снята
с ролика: бумага, графит, голубой Eaton, бирюза плашки субтитров, амбра на
всё, что снято нами, и красный эфирной плашки RT.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

MAP = json.load(open(os.path.join(HERE, 'video_eaton_map.json'), encoding='utf-8'))
SHOTS, LINES, SOURCES = MAP['shots'], MAP['lines'], MAP['sources']
STAT, VIDEO = MAP['stat'], MAP['video']
DUR = VIDEO['dur']

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/video-eaton'
URL = 'https://hand-marketing.ru/video/eaton/'

# цвет источника: амбра у того, что снято нами, красный у эфира, остальное
# в холодной части палитры ролика
COLOR = {'event': '#1E6E96', 'moscow': '#C97B22', 'sync': '#0B3F5C',
         'archive': '#6FAFB2', 'broadcast': '#C6362C', 'screen': '#8A97A0',
         'graphics': '#93C9E4', 'nature': '#6E8F5B', 'titles': '#B9BEB6'}

# представительные кадры источника в инвентаризации
SRC_THUMBS = {'event': [22, 44, 56], 'moscow': [5, 12, 63], 'sync': [51],
              'archive': [32, 37, 36], 'broadcast': [10], 'screen': [19, 21],
              'graphics': [9, 15, 34], 'nature': [7, 8], 'titles': [1, 77]}

SRC_NAME = {s['key']: s['name'] for s in SOURCES}
MOS = next(s for s in SOURCES if s['key'] == 'moscow')

# ─── подписи блоков съёмки Москвы ───────────────────────────────────────────
BLOCK_TEXT = [
    ('Открытие', 'Пять кадров подряд после логотипа: панорама с реки, высотка, '
     'башни Сити, Красная площадь, мост. Ролик начинается с города, а не с '
     'продукции, поэтому у иностранного зала сразу появляется место действия.'),
    ('Середина', 'Четыре ночных кадра сразу после эфира RT. Студийная картинка '
     'новостей уходит в поток машин и подсвеченные башни, и разговор про '
     'энергоёмкость экономики получает изображение вместо слайда.'),
    ('Подводка к финалу', 'Пять летних кадров разрезают долгую череду съёмки '
     'мероприятия. После них финальные слова про инфраструктурные проекты '
     'звучат на масштабе города, а не павильона.'),
]


def fmt(t):
    return f'{int(t) // 60}:{int(t) % 60:02d}'


def sec(v):
    return f'{v:.1f}'.replace('.', ',')


def pct(v):
    return f'{v:.1f}'.replace('.', ',')


def thumb(i, cls='ve-th', lazy=True):
    """Кадр из спрайта: 10 колонок × 8 рядов."""
    c, r = i % STAT['sprite_cols'], i // STAT['sprite_cols']
    x = c / (STAT['sprite_cols'] - 1) * 100
    y = r / (STAT['sprite_rows'] - 1) * 100
    return (f'<span class="{cls}" style="background-position:{x:.4f}% {y:.4f}%"'
            f' role="img" aria-label="{SHOTS[i]["title"]}"></span>')


# ─── секции ─────────────────────────────────────────────────────────────────

def hero():
    facts = [('3:37', 'хронометраж'), (str(STAT['shots']), 'склеек'),
             (str(len(SOURCES)), 'источников материала'),
             (str(STAT['lines']), 'реплик закадрового текста')]
    fl = ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in facts)
    return (
      '<section class="ve-hero">'
      f'<img class="ve-hero__bg" src="{IMG}/hero.jpg" alt="Кадр ролика Eaton: Кремль с Москвы-реки" fetchpriority="high">'
      '<div class="ve-hero__in">'
      '<a class="ve-back" href="/project/">Все проекты</a>'
      '<div class="ve-kick">Video Production, Eaton</div>'
      '<h1>Ролик для международной выставки</h1>'
      '<p class="ve-hero__lead">Три с половиной минуты про Россию для зала, '
      'который по-русски не понимает. Дорожка английская, русские субтитры '
      'вшиты в картинку. Материал пришёл девятью разными кусками, связки '
      'между ними мы досняли сами.</p>'
      f'<div class="ve-facts">{fl}</div>'
      '</div></section>')


def task():
    return (
      '<section class="ve-sec ve-task">'
      '<div class="ve-wrap ve-task__grid">'
      '<div class="ve-rev">'
      '<h2 class="ve-h2">Задача</h2>'
      '<p class="ve-p ve-p--big">Собрать презентационный ролик для участия '
      'Eaton в международной выставке: смонтировать присланный материал, '
      'записать английскую озвучку и доснять недостающие кадры.</p>'
      '</div>'
      '<div class="ve-rev">'
      '<h3 class="ve-h3">Что лежало на входе</h3>'
      '<p class="ve-p">Куски не стыковались вообще ничем. Корпоративные '
      'слайды на английском и рендер самолёта. Репортаж RT со студийным '
      'светом и своей эфирной плашкой. Записи с экрана браузера вместе со '
      'шрифтом сайта и полосой прокрутки. Зимняя съёмка «Дня технологий и '
      'инноваций» на одной площадке. Архив клиента: цех, Ми-8, «Газели» на '
      'снегу.</p>'
      '<h3 class="ve-h3">Что сделали</h3>'
      '<p class="ve-p">Разложили материал по источникам, собрали ленту из '
      f'{STAT["shots"]} склеек, досняли Москву на тех местах, где ролик '
      'рассыпался, и записали английскую дикторскую дорожку под уже '
      'существующую картинку.</p>'
      '</div></div></section>')


def sources():
    tot = sum(s['sec'] for s in SOURCES)
    cards = []
    for s in SOURCES:
        share = s['sec'] / tot * 100
        ths = ''.join(thumb(i) for i in SRC_THUMBS.get(s['key'], []))
        cards.append(
          f'<article class="ve-src ve-rev" style="--c:{COLOR[s["key"]]}">'
          f'<div class="ve-src__ths">{ths}</div>'
          f'<h3 class="ve-src__name">{s["name"]}</h3>'
          f'<div class="ve-src__num"><b>{s["shots"]}</b> кадров'
          f'<i></i><b>{sec(s["sec"])}</b> с</div>'
          f'<div class="ve-src__bar"><span style="width:{share:.1f}%"></span></div>'
          f'<div class="ve-src__share">{pct(share)}% хронометража</div>'
          f'<p class="ve-src__txt">{s["text"]}</p></article>')
    return (
      '<section class="ve-sec ve-srcs"><div class="ve-wrap">'
      '<h2 class="ve-h2 ve-rev">Девять источников</h2>'
      '<p class="ve-p ve-p--big ve-rev">Первое, что пришлось сделать, это '
      'разобрать присланное по происхождению. У каждой группы свой свет, своя '
      'оптика, свой язык на экране и своя частота кадров восприятия. Дальше '
      'весь монтаж строился на том, чтобы соседние куски не спорили.</p>'
      f'<div class="ve-src__grid">{"".join(cards)}</div>'
      '</div></section>')


def film():
    return (
      '<section class="ve-sec ve-film" id="film"><div class="ve-wrap">'
      '<h2 class="ve-h2 ve-rev">Ролик целиком</h2>'
      '<div class="ve-player ve-rev">'
      f'<video id="veVid" controls preload="none" playsinline '
      f'poster="{IMG}/poster.jpg">'
      f'<source src="{VIDEO["src"]}" type="video/mp4">'
      'Ваш браузер не воспроизводит видео.</video></div>'
      '<p class="ve-cap ve-rev">3 минуты 37 секунд, английская дикторская '
      'дорожка, русские субтитры в кадре. Дальше на странице этот же плеер '
      'слушается монтажного листа: клик по любому кадру перематывает ролик '
      'на нужную секунду.</p>'
      '</div></section>')


def edl():
    chips = ['<button type="button" class="ve-chip is-on" data-src="all">'
             'Весь ролик</button>']
    for s in SOURCES:
        chips.append(
          f'<button type="button" class="ve-chip" data-src="{s["key"]}" '
          f'style="--c:{COLOR[s["key"]]}"><i></i>{s["name"]}</button>')

    segs = ''.join(
      f'<button type="button" class="ve-seg" data-i="{s["i"]}" '
      f'data-src="{s["src"]}" style="flex-grow:{s["d"]};--c:{COLOR[s["src"]]}" '
      f'aria-label="Кадр {s["i"] + 1}, {fmt(s["a"])}, {s["title"]}"></button>'
      for s in SHOTS)

    marks = ''.join(
      f'<span style="left:{t / DUR * 100:.2f}%">{fmt(t)}</span>'
      for t in (0, 60, 120, 180))

    cards = ''.join(
      f'<button type="button" class="ve-card" data-i="{s["i"]}" '
      f'data-src="{s["src"]}" style="--c:{COLOR[s["src"]]}">'
      f'{thumb(s["i"], "ve-card__th")}'
      f'<span class="ve-card__no">{s["i"] + 1:02d}</span>'
      f'<span class="ve-card__tc">{fmt(s["a"])}<i>{sec(s["d"])} с</i></span>'
      f'<span class="ve-card__tt">{s["title"]}</span></button>'
      for s in SHOTS)

    return (
      '<section class="ve-sec ve-edl"><div class="ve-wrap">'
      '<h2 class="ve-h2 ve-rev">Монтажный лист</h2>'
      '<p class="ve-p ve-p--big ve-rev">Вся лента в реальном масштабе времени: '
      f'{STAT["shots"]} кадров, ширина блока это его длина, цвет это источник. '
      'Выберите источник, и остальное уйдёт в штриховку. Клик по блоку или по '
      'карточке перематывает ролик на этот кадр.</p>'
      f'<div class="ve-chips ve-rev" role="group" aria-label="Фильтр по источнику">{"".join(chips)}</div>'
      '<div class="ve-barwrap ve-rev">'
      f'<div class="ve-bar" id="veBar">{segs}<span class="ve-head" id="veHead"></span></div>'
      f'<div class="ve-scale">{marks}</div></div>'
      '<div class="ve-read ve-rev">'
      '<div class="ve-read__shot" id="veShot"></div>'
      '<div class="ve-read__num" id="veCount"></div>'
      '</div>'
      f'<div class="ve-cards" id="veCards">{cards}</div>'
      '</div></section>')


def moscow():
    idx = [s['i'] for s in SHOTS if s['src'] == 'moscow']
    n = {v: k + 1 for k, v in enumerate(idx)}
    arts = []
    for k, blk in enumerate(MAP['blocks']):
        head, txt = BLOCK_TEXT[k]
        ids = [s['i'] for s in SHOTS
               if s['src'] == 'moscow' and blk['a'] <= s['a'] < blk['b']]
        shots = ''.join(
          f'<figure class="ve-mos__f"><img src="{IMG}/moscow-{n[i]:02d}.jpg" '
          f'alt="{SHOTS[i]["title"]}" loading="lazy" width="800" height="450">'
          f'<figcaption><b>{fmt(SHOTS[i]["a"])}</b> {SHOTS[i]["title"]}</figcaption>'
          '</figure>' for i in ids)
        arts.append(
          f'<article class="ve-mos ve-rev">'
          f'<div class="ve-mos__head"><span class="ve-mos__no">{k + 1:02d}</span>'
          f'<h3 class="ve-h3">{head}</h3>'
          f'<div class="ve-mos__meta">с {fmt(blk["a"])} по {fmt(blk["b"])} · '
          f'{sec(blk["d"])} с · {blk["n"]} кадров</div></div>'
          f'<div class="ve-mos__ctx">'
          f'<span>до: {SRC_NAME.get(blk["before"], "начало")}</span>'
          f'<span>после: {SRC_NAME.get(blk["after"], "конец")}</span></div>'
          f'<p class="ve-p">{txt}</p>'
          f'<div class="ve-mos__grid">{shots}</div></article>')
    return (
      '<section class="ve-sec ve-moss"><div class="ve-wrap">'
      '<h2 class="ve-h2 ve-rev">Три блока, которых не было</h2>'
      '<p class="ve-p ve-p--big ve-rev">Съёмка Москвы это '
      f'{sec(MOS["sec"])} секунды из {int(DUR)}, '
      f'{pct(MOS["sec"] / DUR * 100)} процента хронометража. '
      'Но стоят они там, где ролик иначе распадается: между '
      'заставкой и материалом клиента, сразу после эфира и перед финалом.</p>'
      f'{"".join(arts)}</div></section>')


def voice():
    mx = max(l['d'] for l in LINES)
    rows = []
    for l in LINES:
        ticks = ''.join(f'<i style="left:{c * 100:.2f}%"></i>' for c in l['cuts'])
        rows.append(
          f'<li><button type="button" class="ve-line" data-t="{l["a"]}">'
          f'<span class="ve-line__tc">{fmt(l["a"])}</span>'
          f'<span class="ve-line__bar" style="width:{l["d"] / mx * 100:.1f}%">'
          f'{ticks}</span>'
          f'<span class="ve-line__d">{sec(l["d"])} с</span>'
          f'<span class="ve-line__tx">{l["text"]}</span></button></li>')
    stats = [(str(STAT['across']), f'реплики из {STAT["lines"]} тянутся через склейку'),
             (sec(STAT['avg_line']) + ' с', 'средняя реплика'),
             (sec(STAT['avg_shot']) + ' с', 'средний кадр'),
             (f'{STAT["covered"] / DUR * 100:.0f}%', 'хронометража идёт под текстом')]
    sl = ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in stats)
    return (
      '<section class="ve-sec ve-voice"><div class="ve-wrap">'
      '<h2 class="ve-h2 ve-rev">Голос длиннее кадра</h2>'
      '<p class="ve-p ve-p--big ve-rev">Английскую дорожку писали под картинку, '
      'которая уже была смонтирована, поэтому длина каждой фразы задана '
      'заранее. Внутри полосы реплики отмечены склейки, которые она '
      f'перекрывает: {STAT["across"]} реплики из {STAT["lines"]} звучат поверх '
      'монтажного стыка. Это и держит разнородную картинку вместе. Клик по '
      'строке перематывает ролик.</p>'
      f'<div class="ve-vstat ve-rev">{sl}</div>'
      f'<ol class="ve-lines ve-rev">{"".join(rows)}</ol>'
      '<p class="ve-cap ve-rev">Текст снят с кадров: субтитры вшиты в '
      'изображение, отдельного файла с ними не существует. Титр '
      f'«{MAP["lower_third"]["text"]}» появляется на '
      f'{fmt(MAP["lower_third"]["a"])}.</p>'
      '</div></section>')


def result():
    return (
      '<section class="ve-sec ve-res"><div class="ve-wrap ve-rev">'
      '<h2 class="ve-h2">Результат</h2>'
      '<p class="ve-p ve-p--big">Готовый англоязычный ролик Eaton показала на '
      'международной выставке. Материал собран так, что зритель не считывает '
      'происхождение кусков: эфир, слайд, скриншот браузера и съёмка города '
      'идут одной дорогой, а английский диктор ведёт по ней без разрывов.</p>'
      '</div></section>')


# ─── стили ──────────────────────────────────────────────────────────────────

PAGE_CSS = """<style>
.ve,.ve *{box-sizing:border-box}
.ve{--pp:#F3F1EC;--pp2:#E7E4DC;--ink:#14181B;--ink2:rgba(20,24,27,.64);
 --line:rgba(20,24,27,.14);--sky:#2BA8DE;--blue:#1E6E96;--amber:#C97B22;
 --serif:'Piazzolla',Georgia,'Times New Roman',serif;
 --mono:'Martian Mono',ui-monospace,'SFMono-Regular',Menlo,monospace;
 background:var(--pp);color:var(--ink);font-family:var(--serif);
 font-size:17px;line-height:1.6;overflow-x:hidden}
.ve img{max-width:100%;display:block}
.ve h1,.ve h2,.ve h3{margin:0;font-weight:800;line-height:1.08;letter-spacing:-.01em}
.ve p{margin:0}
.ve button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
.ve-wrap{max-width:1180px;margin:0 auto;padding:0 clamp(16px,4vw,40px)}
.ve-sec{padding:clamp(52px,8vw,110px) 0}
.ve-h2{font-size:clamp(28px,4.4vw,54px)}
.ve-h3{font-size:clamp(19px,2vw,24px);margin-top:26px}
.ve-p{margin-top:14px;color:var(--ink2);max-width:66ch;overflow-wrap:anywhere}
.ve-p--big{font-size:clamp(17px,1.7vw,21px);color:var(--ink);margin-top:20px}
.ve-cap{margin-top:18px;font-size:14px;color:var(--ink2);max-width:70ch}
.ve-rev{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.ve-rev.is-in{opacity:1;transform:none}
.no-js .ve-rev{opacity:1;transform:none}

/* ГЕРОЙ */
.ve-hero{position:relative;min-height:clamp(430px,80vh,760px);display:flex;
 align-items:flex-end;background:#0B1418;overflow:hidden}
.ve-hero__bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 opacity:.74}
.ve-hero:after{content:"";position:absolute;inset:0;
 background:linear-gradient(180deg,rgba(11,20,24,.75) 0,rgba(11,20,24,.15) 38%,rgba(11,20,24,.92) 100%)}
.ve-hero__in{position:relative;z-index:2;width:100%;max-width:1180px;margin:0 auto;
 padding:clamp(90px,14vh,150px) clamp(16px,4vw,40px) clamp(34px,6vw,64px);color:#fff}
.ve-back{display:inline-block;font-family:var(--mono);font-size:11px;
 letter-spacing:-.04em;text-transform:uppercase;color:rgba(255,255,255,.72);
 text-decoration:none;border-bottom:1px solid rgba(255,255,255,.4);padding-bottom:2px}
.ve-back:hover{color:#fff}
.ve-kick{margin-top:26px;font-family:var(--mono);font-size:12px;letter-spacing:-.03em;
 text-transform:uppercase;color:var(--sky)}
.ve-hero h1{margin-top:12px;font-size:clamp(32px,6.4vw,78px);color:#fff}
.ve-hero__lead{margin-top:18px;max-width:60ch;font-size:clamp(16px,1.8vw,20px);
 color:rgba(255,255,255,.86)}
.ve-facts{margin-top:clamp(24px,4vw,44px);display:grid;gap:14px 26px;
 grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
 border-top:1px solid rgba(255,255,255,.24);padding-top:20px}
.ve-facts b{display:block;font-family:var(--mono);font-size:clamp(20px,2.6vw,30px);
 font-weight:700;letter-spacing:-.05em;color:#fff}
.ve-facts span{display:block;margin-top:4px;font-size:13px;color:rgba(255,255,255,.68)}

/* ЗАДАЧА */
.ve-task{background:var(--pp)}
.ve-task__grid{display:grid;gap:clamp(24px,4vw,60px);
 grid-template-columns:repeat(auto-fit,minmax(280px,1fr));align-items:start}

/* ИСТОЧНИКИ */
.ve-srcs{background:var(--pp2)}
.ve-src__grid{margin-top:clamp(28px,4vw,52px);display:grid;gap:clamp(14px,2vw,24px);
 grid-template-columns:repeat(auto-fill,minmax(268px,1fr))}
.ve-src{background:var(--pp);border-top:4px solid var(--c);padding:16px 18px 20px}
.ve-src__ths{display:grid;grid-template-columns:repeat(3,1fr);gap:4px}
.ve-th{min-width:0;aspect-ratio:16/9;background-image:url(IMGSRC/shots.jpg);
 background-size:1000% 800%;background-repeat:no-repeat;display:block}
.ve-src__name{margin-top:14px;font-size:19px}
.ve-src__num{margin-top:8px;font-family:var(--mono);font-size:12px;letter-spacing:-.04em;
 display:flex;align-items:center;gap:8px;color:var(--ink2)}
.ve-src__num b{color:var(--ink);font-weight:700}
.ve-src__num i{width:1px;height:12px;background:var(--line)}
.ve-src__bar{margin-top:10px;height:5px;background:rgba(20,24,27,.1)}
.ve-src__bar span{display:block;height:100%;background:var(--c)}
.ve-src__share{margin-top:6px;font-family:var(--mono);font-size:11px;
 letter-spacing:-.04em;color:var(--ink2)}
.ve-src__txt{margin-top:12px;font-size:15px;color:var(--ink2);overflow-wrap:anywhere}

/* ПЛЕЕР */
.ve-player{margin-top:clamp(20px,3vw,36px);background:#0B1418;
 box-shadow:0 20px 60px rgba(11,20,24,.18)}
.ve-player video{width:100%;height:auto;aspect-ratio:16/9;display:block;background:#0B1418}

/* МОНТАЖНЫЙ ЛИСТ */
.ve-edl{background:var(--ink);color:#EDEAE3}
.ve-edl .ve-h2{color:#fff}
.ve-edl .ve-p{color:rgba(237,234,227,.72)}
.ve-edl .ve-p--big{color:rgba(237,234,227,.92)}
.ve-chips{margin-top:clamp(22px,3vw,34px);display:flex;flex-wrap:wrap;gap:8px}
.ve .ve-chip{display:inline-flex;align-items:center;gap:7px;padding:7px 13px;
 border:1px solid rgba(237,234,227,.26);border-radius:999px;font-size:13px;
 color:rgba(237,234,227,.8);transition:background .2s,color .2s,border-color .2s}
.ve-chip i{width:9px;height:9px;border-radius:2px;background:var(--c);flex:none}
.ve-chip:hover{border-color:rgba(237,234,227,.6);color:#fff}
.ve .ve-chip.is-on{background:#EDEAE3;color:var(--ink);border-color:#EDEAE3}
.ve-barwrap{margin-top:20px}
.ve-bar{position:relative;display:flex;height:clamp(38px,6vw,58px);width:100%;
 background:rgba(237,234,227,.08)}
.ve .ve-seg{flex-basis:0;min-width:0;background:var(--c);
 box-shadow:inset -1px 0 0 var(--ink);transition:opacity .25s,filter .25s}
.ve-seg:hover{filter:brightness(1.25)}
.ve .ve-seg.is-off{opacity:.16;background:repeating-linear-gradient(135deg,
 rgba(237,234,227,.5) 0 2px,transparent 2px 5px)}
.ve-seg.is-sel{box-shadow:inset 0 0 0 2px #fff}
.ve-head{position:absolute;top:-4px;bottom:-4px;width:2px;background:#fff;
 left:0;pointer-events:none;opacity:0;transition:opacity .2s}
.ve-head.is-on{opacity:1}
.ve-scale{position:relative;height:20px;margin-top:6px;font-family:var(--mono);
 font-size:10px;letter-spacing:-.04em;color:rgba(237,234,227,.5)}
.ve-scale span{position:absolute;top:0;transform:translateX(-1px);
 border-left:1px solid rgba(237,234,227,.3);padding-left:4px}
.ve-read{margin-top:22px;display:grid;gap:18px;
 grid-template-columns:minmax(0,1fr) minmax(0,auto);align-items:center}
.ve-read__shot{display:flex;gap:14px;align-items:center;min-height:74px}
.ve-read__shot .ve-th{flex:none;width:132px}
.ve-read__no{display:block;font-family:var(--mono);font-size:11px;letter-spacing:-.04em;
 color:rgba(237,234,227,.55)}
.ve-read__tt{display:block;margin-top:4px;font-size:17px;color:#fff;overflow-wrap:anywhere}
.ve-read__src{display:block;margin-top:4px;font-size:13px;color:var(--c)}
.ve-read__num{font-family:var(--mono);font-size:12px;letter-spacing:-.04em;
 line-height:1.7;color:rgba(237,234,227,.72);text-align:right}
.ve-read__num b{color:#fff;font-weight:700}
.ve-cards{margin-top:22px;max-height:min(60vh,520px);overflow-y:auto;
 display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));
 padding-right:4px;scrollbar-width:thin}
.ve .ve-card{text-align:left;background:rgba(237,234,227,.06);padding:8px;
 border-left:3px solid var(--c);transition:background .2s,opacity .25s}
.ve .ve-card:hover{background:rgba(237,234,227,.14)}
.ve-card.is-off{opacity:.28}
.ve .ve-card.is-sel{background:rgba(237,234,227,.2)}
.ve-card__th{display:block;width:100%;aspect-ratio:16/9;
 background-image:url(IMGSRC/shots.jpg);background-size:1000% 800%;
 background-repeat:no-repeat}
.ve-card__no{float:right;font-family:var(--mono);font-size:10px;letter-spacing:-.05em;
 color:rgba(237,234,227,.45);margin-top:7px}
.ve-card__tc{display:block;margin-top:7px;font-family:var(--mono);font-size:11px;
 letter-spacing:-.05em;color:#fff}
.ve-card__tc i{font-style:normal;color:rgba(237,234,227,.5);margin-left:6px}
.ve-card__tt{display:block;margin-top:4px;font-size:13px;line-height:1.35;
 color:rgba(237,234,227,.8);overflow-wrap:anywhere}

/* МОСКВА */
.ve-moss{background:var(--pp)}
.ve-mos{margin-top:clamp(34px,5vw,64px);border-top:1px solid var(--line);padding-top:22px}
.ve-mos__head{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 16px}
.ve-mos__no{font-family:var(--mono);font-size:12px;letter-spacing:-.05em;color:var(--amber)}
.ve-mos__meta{font-family:var(--mono);font-size:11px;letter-spacing:-.04em;color:var(--ink2)}
.ve-mos__ctx{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px}
.ve-mos__ctx span{font-family:var(--mono);font-size:11px;letter-spacing:-.04em;
 padding:5px 10px;background:var(--pp2);color:var(--ink2)}
.ve-mos__grid{margin-top:20px;display:grid;gap:12px;
 grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}
.ve-mos__f{margin:0}
.ve-mos__f img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.ve-mos__f figcaption{margin-top:7px;font-size:13px;color:var(--ink2);overflow-wrap:anywhere}
.ve-mos__f b{font-family:var(--mono);font-size:11px;letter-spacing:-.05em;
 color:var(--amber);font-weight:400;margin-right:6px}

/* ГОЛОС */
.ve-voice{background:var(--pp2)}
.ve-vstat{margin-top:clamp(24px,3vw,40px);display:grid;gap:16px 24px;
 grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
 border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:20px 0}
.ve-vstat b{display:block;font-family:var(--mono);font-size:clamp(18px,2.2vw,26px);
 font-weight:700;letter-spacing:-.05em}
.ve-vstat span{display:block;margin-top:4px;font-size:13px;color:var(--ink2)}
.ve-lines{margin:clamp(22px,3vw,34px) 0 0;padding:0;list-style:none}
.ve-line{display:grid;width:100%;text-align:left;padding:9px 0;
 border-bottom:1px solid var(--line);align-items:center;
 grid-template-columns:52px minmax(60px,120px) 54px minmax(0,1fr);gap:12px}
.ve .ve-line:hover{background:rgba(20,24,27,.04)}
.ve-line__tc,.ve-line__d{font-family:var(--mono);font-size:11px;letter-spacing:-.05em;
 color:var(--ink2)}
.ve-line__bar{position:relative;height:8px;background:var(--blue);display:block}
.ve-line__bar i{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--amber)}
.ve-line__tx{font-size:15px;overflow-wrap:anywhere}

/* РЕЗУЛЬТАТ */
.ve-res{background:var(--pp);padding-bottom:clamp(60px,9vw,120px)}

@media(max-width:860px){
 .ve-read{grid-template-columns:1fr}
 .ve-read__num{text-align:left}
 .ve-read__shot .ve-th{width:104px}
}
@media(max-width:640px){
 .ve{font-size:16px}
 .ve-line{grid-template-columns:46px 1fr 48px;gap:8px}
 .ve-line__tx{grid-column:1/-1;margin-top:2px}
 .ve-cards{grid-template-columns:repeat(auto-fill,minmax(126px,1fr))}
 .ve-facts{grid-template-columns:repeat(2,1fr)}
}
@media(prefers-reduced-motion:reduce){
 .ve-rev{opacity:1;transform:none;transition:none}
 .ve *{transition:none!important}
}
</style>""".replace('IMGSRC', IMG)


# ─── скрипты ────────────────────────────────────────────────────────────────

PAGE_JS = """<script>(function(){
var D=%DATA%;
var vid=document.getElementById('veVid'),bar=document.getElementById('veBar'),
    head=document.getElementById('veHead'),shot=document.getElementById('veShot'),
    cnt=document.getElementById('veCount'),cards=document.getElementById('veCards');
if(!vid||!bar)return;
var segs=[].slice.call(bar.querySelectorAll('.ve-seg')),
    cds=[].slice.call(cards.querySelectorAll('.ve-card')),
    chips=[].slice.call(document.querySelectorAll('.ve-chip')),
    cur=-1,flt='all';
function tc(t){return Math.floor(t/60)+':'+('0'+Math.floor(t%60)).slice(-2);}
function nm(v){return v.toFixed(1).replace('.',',');}
function draw(i){
 var s=D.s[i];cur=i;
 segs.forEach(function(e,k){e.classList.toggle('is-sel',k===i);});
 cds.forEach(function(e,k){e.classList.toggle('is-sel',k===i);});
 var col=D.c[s[2]],r=Math.floor(i/D.gc),c=i%D.gc;
 shot.innerHTML='<span class="ve-th" style="background-position:'+
  (c/(D.gc-1)*100).toFixed(4)+'% '+(r/(D.gr-1)*100).toFixed(4)+'%"></span>'+
  '<span><span class="ve-read__no">кадр '+(i+1)+' из '+D.s.length+' · '+
  tc(s[0])+' · '+nm(s[1])+' с</span>'+
  '<span class="ve-read__tt">'+s[3]+'</span>'+
  '<span class="ve-read__src" style="--c:'+col+'">'+D.n[s[2]]+'</span></span>';
}
function count(){
 var n=0,sum=0;
 D.s.forEach(function(s){if(flt==='all'||s[2]===flt){n++;sum+=s[1];}});
 cnt.innerHTML='<b>'+n+'</b> кадров<br><b>'+nm(sum)+'</b> секунд<br><b>'+
  (sum/D.d*100).toFixed(1).replace('.',',')+'%</b> хронометража';
}
function filter(k){
 flt=k;
 chips.forEach(function(e){e.classList.toggle('is-on',e.dataset.src===k);});
 segs.forEach(function(e){e.classList.toggle('is-off',k!=='all'&&e.dataset.src!==k);});
 cds.forEach(function(e){e.classList.toggle('is-off',k!=='all'&&e.dataset.src!==k);});
 count();
}
function seek(t,play){
 try{vid.currentTime=t;}catch(e){}
 var r=vid.getBoundingClientRect();
 if(r.bottom<60||r.top>innerHeight-60)vid.scrollIntoView({block:'center',behavior:'smooth'});
 if(play!==false){var p=vid.play();if(p&&p.catch)p.catch(function(){});}
}
bar.addEventListener('click',function(e){
 var b=e.target.closest('.ve-seg');if(!b)return;
 var i=+b.dataset.i;draw(i);seek(D.s[i][0]);});
bar.addEventListener('mousemove',function(e){
 var b=e.target.closest('.ve-seg');if(b&&+b.dataset.i!==cur)draw(+b.dataset.i);});
cards.addEventListener('click',function(e){
 var b=e.target.closest('.ve-card');if(!b)return;
 var i=+b.dataset.i;draw(i);seek(D.s[i][0]);});
chips.forEach(function(e){e.addEventListener('click',function(){filter(e.dataset.src);});});
document.addEventListener('click',function(e){
 var b=e.target.closest('.ve-line');if(!b)return;seek(+b.dataset.t);});
vid.addEventListener('timeupdate',function(){
 var t=vid.currentTime;head.classList.add('is-on');
 head.style.left=(t/D.d*100)+'%';
 for(var i=D.s.length-1;i>=0;i--){if(t>=D.s[i][0]){if(i!==cur)draw(i);break;}}
});
draw(2);count();
})();</script>"""

REVEAL_JS = """<script>(function(){
var els=[].slice.call(document.querySelectorAll('.ve-rev'));
if(!els.length)return;
if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('is-in');});return;}
var io=new IntersectionObserver(function(en){
 en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('is-in');io.unobserve(x.target);}});
},{rootMargin:'0px 0px -8% 0px'});
els.forEach(function(e){io.observe(e);});
})();</script>"""


def page_js():
    data = {
        'd': DUR, 'gc': STAT['sprite_cols'], 'gr': STAT['sprite_rows'],
        'c': COLOR, 'n': SRC_NAME,
        's': [[s['a'], s['d'], s['src'], s['title']] for s in SHOTS],
    }
    return PAGE_JS.replace('%DATA%', json.dumps(data, ensure_ascii=False,
                                                separators=(',', ':')))


HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Презентационный ролик Eaton для международной выставки | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing для Eaton: ролик 3:37 для международной выставки. Монтаж из девяти источников, 79 склеек, съёмка Москвы для недостающих сцен, английская дикторская дорожка под готовую картинку.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Презентационный ролик Eaton для международной выставки">
<meta property="og:description" content="Девять источников материала, 79 склеек, три блока съёмки Москвы и английская озвучка под уже смонтированную картинку. Монтажный лист ролика целиком.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/og.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/piazzolla-martian.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''

LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Video Production","item":"https://hand-marketing.ru/videoproduction/"},'
  '{"@type":"ListItem","position":3,"name":"Презентационный ролик Eaton для международной выставки",'
  f'"item":"{URL}"}}]}}</script>')


def page():
    body = (f'{rc.header()}<main class="ve">{hero()}{task()}{sources()}{film()}'
            f'{edl()}{moscow()}{voice()}{result()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{page_js()}{REVEAL_JS}{LD}'
            '</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'eaton')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    # index-a2.html это деплой-источник (workflow переименовывает его в index.html)
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
