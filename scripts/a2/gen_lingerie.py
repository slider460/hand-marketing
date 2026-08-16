#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/lingerie/index.html: кейс «Подиумная съёмка для
журнала Lingerie» — «Гранд-дефиле Lingerie», Осень-Зима 2014/2015, выставка CPM.

Первоисточник один: отчётный ролик media/lingerie.mp4, 7:08, 1280×720, 25 fps.
Ничего не придумано и не взято из интернета. Порядок брендов, их написания,
тайм-коды блоков, длительности и все 54 выхода сняты с файла скриптом
scripts/lingerie-assets.py; организаторы и производство видео — с титров ролика.

Идея страницы. Отчётный ролик показа — это архив, запертый в семи минутах:
чтобы увидеть выход конкретного бренда, надо мотать. Монтаж собран строго по
структуре показа (одиннадцать блоков почти по тридцать секунд, каждый открыт
нижней плашкой с именем марки), и эту структуру страница разворачивает обратно
в плоскость, где всё видно сразу.

Отсюда механики:

1. «Лукбук из ролика» (сигнатурная). Камера стоит неподвижно в торце подиума,
   поэтому силуэт модели растёт по мере приближения к отметке. Скрипт считает
   фон локальной медианой, берёт крупнейший силуэт на подиуме и ищет максимумы
   его площади — это момент позы. 54 таких кадра нарезаны в портреты и лежат
   по одиннадцати брендам плюс финал. Клик по выходу перематывает плеер на эту
   секунду: сетка и ролик — одно и то же, показанное двумя способами.
2. Пульс показа: площадь силуэта за все 428 секунд, canvas-кривая с зубцом на
   каждый выход. Поверх лежат границы блоков, и видно ритм: Massana гонит пять
   выходов за 35 секунд, Zimmerli выпускает три за те же полминуты.
3. Дорожка показа: одиннадцать блоков в реальных длительностях с засечками
   выходов, она же шкала плеера.

Шрифты — Oranienbaum (заголовки) и Mulish (текст), self-host:
/fonts/oranienbaum-mulish.css. Oranienbaum — дидон с родной кириллицей,
нарисован под русский и рифмуется с высококонтрастной антиквой в логотипе
самого журнала; Mulish держит длинный текст и цифры. Палитра снята с кадров
зала: чёрный зал, белый подиум, голубой экран задника, плюс маджента журнала.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

MAP = json.load(open(os.path.join(HERE, 'lingerie_map.json'), encoding='utf-8'))

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/lingerie'
VIDEO = '/media/video-lingerie-hand-marketing.mp4'
URL = 'https://hand-marketing.ru/video/lingerie/'
TITLE = 'Подиумная съёмка показа для журнала Lingerie | Hand Marketing'
DESCR = ('Съёмка и монтаж отчётного ролика «Гранд-дефиле Lingerie», Осень-Зима '
         '2014/2015 на выставке CPM: одиннадцать марок, 54 выхода, две камеры, '
         'семь минут.')

DUR = MAP['duration']
BLOCKS = MAP['blocks']
BRANDS = [b for b in BLOCKS if b['slug'] != 'finale']
FINALE = [b for b in BLOCKS if b['slug'] == 'finale'][0]
TOTAL = MAP['total_looks']

# Страны марок: сняты с их же логотипов на финальной стенке ролика
# (MASSANA BARCELONA, ARTESANIA J&C MADRID, zimmerli of Switzerland,
# VANDACATUCCI MILANO, RITRATTI Milano). Где на логотипе города нет,
# поле пустое — выдумывать не из чего.
COUNTRY = {
    'gattina': '', 'vonfollies': '', 'parah': '', 'vandacatucci': 'Милан',
    'dorofeeva': '', 'dana': '', 'massana': 'Барселона', 'jc': 'Мадрид',
    'nightdreams': '', 'zimmerli': 'Швейцария', 'ritratti': 'Милан',
}

# Короткие имена для дорожки: блок в тридцать секунд занимает на ней ~7 %
# ширины, полное «Von Follies by Dita Von Teese» туда не влезает ни при каком
# кегле. Полные написания остаются в лукбуке.
# ­ — мягкий перенос: одно длинное слово без пробелов иначе просто
# обрезается краем колонки, а рвать его посреди слога нельзя.
SHORT = {
    'vonfollies': 'Von Follies', 'vandacatucci': 'Catucci',
    'dorofeeva': 'Дорофеева', 'dana': 'Dana',
    'nightdreams': 'Night­dreams',
}


def mmss(t):
    # Отбрасываем дробь, а не округляем: плеер показывает время именно так,
    # и подпись под кадром должна совпадать с тем, что видно на его шкале
    # (хронометраж 427,88 с — это 7:07, а не 7:08).
    t = int(t)
    return f'{t // 60}:{t % 60:02d}'


def plural(n, one, few, many):
    """Русское согласование: 1 модель, 3 модели, 5 моделей."""
    n = abs(int(n))
    if n % 100 // 10 == 1:
        return many
    return {1: one, 2: few, 3: few, 4: few}.get(n % 10, many)


# ─── шапка ──────────────────────────────────────────────────────────────────
def hero():
    stats = [(str(len(BRANDS)), 'марок в показе'),
             (str(TOTAL), 'выходов в кадре'),
             (mmss(DUR), 'хронометраж'),
             ('2', 'камеры на подиуме')]
    cells = ''.join(f'<div class="lg-stat"><b>{v}</b><span>{k}</span></div>'
                    for v, k in stats)
    return ('<section class="lg-hero">'
      f'<img class="lg-hero__bg" src="{IMG}/hall.jpg" alt="" aria-hidden="true">'
      '<div class="lg-hero__wash"></div>'
      '<div class="in">'
      '<p class="lg-kick">Video Production · 2014</p>'
      '<h1>Гранд-дефиле<br><span class="lg-serif-it">Lingerie</span></h1>'
      '<p class="lg-hero__sub">Осень-Зима 2014/2015 · выставка CPM, Москва</p>'
      '<p class="lg-lead">Показ идёт полтора часа и не повторяется. Наша задача '
      'была снять его так, чтобы через семь минут человек, которого в зале не '
      'было, увидел все одиннадцать марок в том порядке, в каком они выходили.</p>'
      f'<div class="lg-stats">{cells}</div>'
      '</div></section>')


# ─── задача и решение ───────────────────────────────────────────────────────
def brief():
    return ('<section class="lg-brief"><div class="in lg-brief__in">'
      '<div class="lg-r">'
      '<p class="lg-kick">Клиент</p>'
      '<h2>Журнал о белье<br>и бельевом бизнесе</h2>'
      '<p>Lingerie — одно из самых читаемых в России изданий о нижнем белье. '
      'Журнал работает информационным партнёром отраслевых выставок: '
      'Salon International de la Lingerie и Interfilière в Париже, Unique by '
      'Mode City, Maredamare, CPM Body &amp; Beach, Interfilière в Гонконге '
      'и Шанхае, Fashion World в Токио, «Текстильлегпром» в Москве.</p>'
      '<p>Гранд-дефиле — собственный показ издания на CPM. Одиннадцать марок '
      'в одной программе: испанские, итальянские, швейцарская, немецкая, '
      'российская.</p>'
      '</div>'
      '<div class="lg-r">'
      '<div class="lg-task">'
      '<p class="lg-kick">Задача</p>'
      '<p class="lg-task__t">Снять показ мод и собрать отчётный ролик.</p>'
      '</div>'
      '<div class="lg-task">'
      '<p class="lg-kick">Решение</p>'
      '<p class="lg-task__t">Две камеры в торце подиума: одна берёт крупный '
      'план, вторая общий. На монтаже ролик собран по структуре показа: '
      'блок на марку, плашка с именем на входе в блок.</p>'
      '</div>'
      '<div class="lg-two">'
      f'<figure><img src="{IMG}/hall.jpg" alt="Общий план: подиум, зрители, экран задника" loading="lazy" decoding="async"><figcaption>Общий план</figcaption></figure>'
      f'<figure><img src="{IMG}/close.jpg" alt="Крупный план: модель на отметке в торце подиума" loading="lazy" decoding="async"><figcaption>Крупный план</figcaption></figure>'
      '</div>'
      '</div>'
      '</div></section>')


# ─── дорожка показа ─────────────────────────────────────────────────────────
def track():
    segs = ''
    for b in BLOCKS:
        w = (b['end'] - b['start']) / DUR * 100
        ticks = ''.join(
            '<i style="left:{:.3f}%"></i>'.format(
                (l['t'] - b['start']) / (b['end'] - b['start']) * 100)
            for l in b['looks'])
        fin = ' is-finale' if b['slug'] == 'finale' else ''
        segs += (f'<button class="lg-seg{fin}" type="button" data-seek="{b["start"]:.2f}" '
                 f'data-slug="{b["slug"]}" style="width:{w:.4f}%" '
                 f'aria-label="{b["name"]}, {mmss(b["start"])}">'
                 f'<span class="lg-seg__n">{SHORT.get(b["slug"], b["name"])}</span>'
                 f'<span class="lg-seg__t">{mmss(b["start"])}</span>'
                 f'<span class="lg-seg__ticks">{ticks}</span></button>')
    return ('<section class="lg-track"><div class="in">'
      '<p class="lg-kick">Структура ролика</p>'
      '<h2>Одиннадцать блоков<br>и финал</h2>'
      '<p class="lg-lead">Каждый блок открывается плашкой с именем марки и длится '
      'почти ровно полминуты. Дольше только Gattina, которая открывает показ, '
      'и финал, где марки выходят вперемешку. Полоса ниже нарисована по реальным '
      'длительностям, засечки на ней — выходы моделей. Клик перематывает ролик.</p>'
      f'<div class="lg-bar" id="lg-bar">{segs}<span class="lg-bar__play" id="lg-play"></span></div>'
      '<div class="lg-bar__legend"><span>0:00</span><span>плашка марки · '
      f'{TOTAL} засечек · выход модели</span><span>{mmss(DUR)}</span></div>'
      '</div></section>')


# ─── лукбук ─────────────────────────────────────────────────────────────────
def look_card(slug, l):
    return (f'<button class="lg-look" type="button" data-seek="{l["t"]:.2f}">'
            f'<img src="{IMG}/looks/{slug}-{l["n"]:02d}.jpg" '
            f'alt="Выход {l["n"]}, стоп-кадр на {mmss(l["t"])}" '
            f'loading="lazy" decoding="async" width="560" height="746">'
            f'<span class="lg-look__t">{mmss(l["t"])}</span></button>')


def lookbook():
    rows = ''
    for b in BRANDS:
        n = len(b['looks'])
        meta = f'{n} {plural(n, "выход", "выхода", "выходов")}'
        chips = []
        # написание с финальной стенки показываем, только если оно добавляет
        # что-то к заголовку (у Gattina или Parah оно совпадает дословно)
        if b['wall'].lower() != b['name'].lower():
            chips.append(b['wall'])
        if COUNTRY[b['slug']]:
            chips.append(COUNTRY[b['slug']])
        chips += [mmss(b['start']), meta]
        cards = ''.join(look_card(b['slug'], l) for l in b['looks'])
        rows += ('<article class="lg-brand lg-r">'
          '<header class="lg-brand__h">'
          f'<h3>{b["name"]}</h3>'
          f'<p class="lg-brand__m">{"".join(f"<span>{c}</span>" for c in chips)}</p>'
          '</header>'
          f'<div class="lg-looks">{cards}</div></article>')
    nf = len(FINALE['looks'])
    fin = ''.join(look_card('finale', l) for l in FINALE['looks'])
    rows += ('<article class="lg-brand lg-brand--fin lg-r">'
      '<header class="lg-brand__h"><h3>Финал</h3>'
      f'<p class="lg-brand__m"><span>все марки вместе</span>'
      f'<span>{mmss(FINALE["start"])}</span>'
      f'<span>{nf} {plural(nf, "выход", "выхода", "выходов")}</span></p></header>'
      f'<div class="lg-looks">{fin}</div></article>')
    return ('<section class="lg-book"><div class="in">'
      '<p class="lg-kick">Лукбук</p>'
      f'<h2>{TOTAL} выходов,<br>вынутых из ролика</h2>'
      '<p class="lg-lead">Этих кадров не снимал фотограф. Камера на показе стоит '
      'неподвижно в торце подиума, поэтому силуэт модели растёт по мере '
      'приближения к отметке. Скрипт прошёл по всем 10 697 кадрам ролика, '
      'нашёл момент, когда силуэт крупнее всего, а движения почти нет, и вырезал '
      'портрет. Получился лукбук показа. Клик по выходу перематывает ролик '
      'на эту секунду.</p>'
      f'<div class="lg-brands">{rows}</div>'
      '</div></section>')


# ─── пульс ──────────────────────────────────────────────────────────────────
def pulse():
    marks = ''.join(
        f'<i style="left:{b["start"] / DUR * 100:.3f}%" data-n="{b["name"]}"></i>'
        for b in BLOCKS)
    fastest = max(BRANDS, key=lambda b: len(b['looks']) / (b['end'] - b['start']))
    slowest = min(BRANDS, key=lambda b: len(b['looks']) / (b['end'] - b['start']))
    def rate(b):
        return (b['end'] - b['start']) / max(1, len(b['looks']))

    def models(b):
        n = len(b['looks'])
        return f'{n} {plural(n, "модель", "модели", "моделей")}'

    def secs(b):
        return f'{b["end"] - b["start"]:.0f} с'

    return ('<section class="lg-pulse"><div class="in">'
      '<p class="lg-kick">Ритм</p>'
      '<h2>Пульс показа</h2>'
      '<p class="lg-lead">Тот же силуэт, но не кадрами, а кривой: как далеко '
      'модель от камеры в каждый момент семи минут. Один зубец — один проход: '
      'вышла из-за экрана, дошла до отметки, встала, ушла. Ритм у марок разный, '
      'и это видно без единой цифры.</p>'
      '<div class="lg-canvas-wrap">'
      '<canvas id="lg-pulse" width="1600" height="300" role="img" '
      'aria-label="Кривая приближения моделей к камере за семь минут ролика"></canvas>'
      f'<div class="lg-canvas-marks">{marks}</div>'
      '</div>'
      '<div class="lg-rate">'
      f'<div class="lg-rate__c"><b>{rate(fastest):.0f} с</b>'
      f'<span>на выход у марки {fastest["name"]}: '
      f'{models(fastest)} за {secs(fastest)}, '
      'самый плотный блок показа</span></div>'
      f'<div class="lg-rate__c"><b>{rate(slowest):.0f} с</b>'
      f'<span>на выход у марки {slowest["name"]}: {models(slowest)} '
      f'за {secs(slowest)}, самый просторный</span></div>'
      f'<div class="lg-rate__c"><b>{DUR / TOTAL:.0f} с</b>'
      '<span>средний интервал между выходами по всему ролику</span></div>'
      '</div></div></section>')


# ─── плеер ──────────────────────────────────────────────────────────────────
def player():
    return ('<section class="lg-player" id="lg-player-sec"><div class="in">'
      '<p class="lg-kick">Ролик целиком</p>'
      '<h2>Отчёт о показе</h2>'
      '<div class="lg-video">'
      f'<video id="lg-video" controls preload="metadata" playsinline '
      f'poster="{IMG}/title.jpg"><source src="{VIDEO}" type="video/mp4">'
      'Ваш браузер не поддерживает видео.</video>'
      '</div>'
      '<p class="lg-now" id="lg-now">Нажмите любой выход выше — ролик '
      'перемотается на эту секунду.</p>'
      '</div></section>')


# ─── титры ──────────────────────────────────────────────────────────────────
def credits():
    # фоновой подложки нет: та же стенка логотипов стоит ниже картинкой,
    # два раза подряд она читалась как грязь под текстом
    return ('<section class="lg-cred">'
      '<div class="in">'
      '<p class="lg-kick">Кто делал показ</p>'
      '<h2>Титры ролика</h2>'
      '<div class="lg-cred__grid">'
      '<div><span>Организатор</span><b>ИД «Нимал»</b><i>журнал Lingerie</i></div>'
      '<div><span>При поддержке</span><b>ООО «Мессе Дюссельдорф Москва»</b>'
      '<i>выставка CPM</i></div>'
      '<div><span>Производство видео</span><b>Hand Marketing</b>'
      '<i>съёмка двумя камерами и монтаж</i></div>'
      '</div>'
      f'<figure class="lg-cred__wall"><img src="{IMG}/wall.jpg" '
      'alt="Финальная плашка ролика: логотипы одиннадцати марок показа" '
      'loading="lazy" decoding="async"><figcaption>Финальная плашка ролика: '
      'все одиннадцать марок показа</figcaption></figure>'
      '</div></section>')


CSS = """<style>
:root{
  --hall:#0e0e10; --hall2:#17161a; --runway:#f2ede9; --screen:#7f9ab8;
  --ink:#f6f2ef; --mut:rgba(246,242,239,.62); --mut2:rgba(246,242,239,.38);
  --mag:#e6007e; --line:rgba(246,242,239,.14);
}
.lg *{box-sizing:border-box}
.lg{background:var(--hall);color:var(--ink);
  font-family:'Mulish',-apple-system,Segoe UI,Arial,sans-serif;
  font-size:17px;line-height:1.62;overflow-x:clip}
.lg .in{max-width:1180px;margin:0 auto;padding:0 32px}
.lg h1,.lg h2,.lg h3{font-family:'Oranienbaum',Georgia,serif;font-weight:400;
  line-height:1.02;letter-spacing:.01em;margin:0}
.lg h1{font-size:clamp(52px,10.5vw,148px)}
.lg h2{font-size:clamp(34px,5.4vw,72px);margin-bottom:22px}
.lg h3{font-size:clamp(26px,3.4vw,42px)}
.lg p{margin:0 0 18px}
.lg-serif-it{font-style:italic;color:var(--mag)}
.lg-kick{font-family:'Mulish',sans-serif;font-size:12px;font-weight:800;
  letter-spacing:.22em;text-transform:uppercase;color:var(--mut2);margin:0 0 14px}
.lg-lead{font-size:clamp(17px,1.5vw,20px);color:var(--mut);max-width:68ch}
.lg section{padding:clamp(64px,9vw,120px) 0}

/* шапка */
.lg-hero{position:relative;padding:clamp(96px,14vw,180px) 0 clamp(56px,7vw,90px);
  min-height:78vh;display:flex;align-items:flex-end;overflow:hidden}
.lg-hero__bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  opacity:.5;filter:grayscale(.25)}
.lg-hero__wash{position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(14,14,16,.78) 0%,rgba(14,14,16,.35) 40%,
    rgba(14,14,16,.92) 100%)}
.lg-hero .in{position:relative;z-index:2;width:100%}
.lg-hero__sub{font-size:clamp(15px,1.6vw,19px);color:var(--mut);
  letter-spacing:.04em;margin:18px 0 26px}
.lg-hero .lg-lead{max-width:56ch}
.lg-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;
  margin-top:clamp(34px,5vw,56px);border-top:1px solid var(--line);padding-top:26px}
.lg-stat b{display:block;font-family:'Oranienbaum',Georgia,serif;font-weight:400;
  font-size:clamp(32px,4.4vw,58px);line-height:1}
.lg-stat span{display:block;font-size:13px;color:var(--mut2);margin-top:8px;
  letter-spacing:.02em}

/* клиент, задача, решение */
.lg-brief__in{display:grid;grid-template-columns:1fr 1fr;gap:clamp(32px,5vw,72px)}
.lg-brief p{color:var(--mut)}
.lg-task{border-top:1px solid var(--line);padding-top:20px;margin-bottom:30px}
.lg-task__t{color:var(--ink);font-size:clamp(17px,1.6vw,20px);margin:0}
.lg-two{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:34px}
.lg-two figure{margin:0}
.lg-two img{width:100%;height:auto;display:block;border-radius:2px}
.lg-two figcaption{font-size:12px;color:var(--mut2);margin-top:8px;
  letter-spacing:.16em;text-transform:uppercase}

/* дорожка */
.lg-bar{display:flex;width:100%;height:118px;margin-top:clamp(30px,4vw,48px);
  position:relative;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.lg-seg{position:relative;flex:0 0 auto;background:transparent;border:0;
  border-right:1px solid var(--line);cursor:pointer;padding:14px 8px 0;
  text-align:left;color:inherit;font:inherit;overflow:hidden;
  transition:background .18s}
.lg-seg:first-child{border-left:1px solid var(--line)}
.lg-seg:hover,.lg-seg.is-on{background:rgba(230,0,126,.16)}
.lg-seg.is-finale{background:rgba(246,242,239,.05)}
.lg-seg.is-finale:hover,.lg-seg.is-finale.is-on{background:rgba(230,0,126,.16)}
/* Переносим только по пробелам: word-break рвал NIGHTDREAMS посреди слова.
   Кегль в vw, потому что ширина колонки тоже доля вьюпорта: самое длинное имя
   должно влезать в тридцатисекундный блок на любой ширине, где полоса живёт. */
.lg-seg__n{display:block;font-size:clamp(8px,.66vw,11px);font-weight:800;
  letter-spacing:.02em;text-transform:uppercase;line-height:1.24;
  word-break:normal;overflow-wrap:normal;hyphens:manual}
.lg-seg__t{display:block;font-size:clamp(9px,.62vw,11px);color:var(--mut2);
  margin-top:6px;font-variant-numeric:tabular-nums}
.lg-seg__ticks{position:absolute;left:0;right:0;bottom:0;height:34px;display:block}
.lg-seg__ticks i{position:absolute;bottom:0;width:2px;height:16px;
  background:var(--mag);opacity:.85}
.lg-bar__play{position:absolute;top:0;bottom:0;width:2px;background:var(--ink);
  left:0;pointer-events:none;opacity:0;transition:opacity .2s}
.lg-bar__play.is-on{opacity:1}
.lg-bar__legend{display:flex;justify-content:space-between;gap:16px;margin-top:12px;
  font-size:12px;color:var(--mut2);letter-spacing:.04em}

/* лукбук */
.lg-book{background:var(--hall2)}
.lg-brands{margin-top:clamp(36px,5vw,64px)}
.lg-brand{padding:clamp(28px,4vw,48px) 0;border-top:1px solid var(--line)}
.lg-brand__h{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 26px;
  margin-bottom:22px}
.lg-brand__m{display:flex;flex-wrap:wrap;gap:8px 20px;margin:0;font-size:12px;
  color:var(--mut2);letter-spacing:.1em;text-transform:uppercase}
.lg-brand--fin h3{color:var(--mag)}
.lg-looks{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));
  gap:10px}
.lg-look{position:relative;padding:0;border:0;background:#000;cursor:pointer;
  display:block;overflow:hidden;border-radius:2px;line-height:0}
.lg-look img{width:100%;height:auto;display:block;transition:transform .4s ease,
  filter .3s}
.lg-look:hover img,.lg-look:focus-visible img{transform:scale(1.045);filter:brightness(1.08)}
.lg-look__t{position:absolute;left:8px;bottom:8px;font-size:11px;font-weight:700;
  letter-spacing:.06em;color:#fff;background:rgba(14,14,16,.72);padding:3px 7px;
  border-radius:2px;line-height:1.4;font-variant-numeric:tabular-nums}
.lg-look:focus-visible{outline:2px solid var(--mag);outline-offset:2px}

/* пульс */
.lg-canvas-wrap{position:relative;margin-top:clamp(30px,4vw,48px);
  border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  padding:18px 0 0}
.lg-canvas-wrap canvas{width:100%;height:auto;display:block}
.lg-canvas-marks{position:relative;height:30px}
.lg-canvas-marks i{position:absolute;top:0;width:1px;height:9px;
  background:var(--mut2)}
.lg-rate{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(18px,3vw,44px);
  margin-top:clamp(30px,4vw,48px)}
.lg-rate__c b{display:block;font-family:'Oranienbaum',Georgia,serif;font-weight:400;
  font-size:clamp(34px,4.6vw,60px);line-height:1;color:var(--mag)}
.lg-rate__c span{display:block;font-size:15px;color:var(--mut);margin-top:12px}

/* плеер */
.lg-player{background:var(--hall2)}
.lg-video{margin-top:clamp(24px,3vw,40px);background:#000;border-radius:2px;
  overflow:hidden;line-height:0}
.lg-video video{width:100%;height:auto;display:block}
.lg-now{margin-top:16px;font-size:14px;color:var(--mut2)}

/* титры */
.lg-cred{position:relative;overflow:hidden}
.lg-cred__grid{display:grid;grid-template-columns:repeat(3,1fr);
  gap:clamp(18px,3vw,44px);margin-top:clamp(26px,4vw,44px)}
.lg-cred__grid>div{border-top:1px solid var(--line);padding-top:18px}
.lg-cred__grid span{display:block;font-size:11px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--mut2);margin-bottom:10px}
.lg-cred__grid b{display:block;font-size:clamp(17px,1.7vw,21px);font-weight:700}
.lg-cred__grid i{display:block;font-style:normal;font-size:14px;color:var(--mut);
  margin-top:6px}
.lg-cred__wall{margin:clamp(34px,5vw,58px) 0 0}
.lg-cred__wall img{width:100%;height:auto;display:block;border-radius:2px}
.lg-cred__wall figcaption{font-size:12px;color:var(--mut2);margin-top:10px;
  letter-spacing:.06em}

/* появление */
.lg-r{opacity:0;transform:translateY(18px);
  transition:opacity .6s ease,transform .6s ease}
.lg-r.is-in{opacity:1;transform:none}

/* планшет */
@media (max-width:1000px){
  .lg-rate,.lg-cred__grid{grid-template-columns:1fr 1fr}
  .lg-brief__in{grid-template-columns:1fr;gap:44px}
}
/* Дорожка: ниже 1100 px тридцатисекундный блок даёт колонку уже 60 px, имя
   в неё влезает только нечитаемым кеглем. Отдаём вертикальный список:
   те же данные, тот же клик, читаемый размер. */
@media (max-width:1100px){
  .lg-bar{display:block;height:auto;border:0}
  .lg-seg{display:flex;align-items:baseline;gap:12px;width:100%!important;
    border:0;border-top:1px solid var(--line);padding:11px 4px;overflow:visible}
  .lg-seg:first-child{border-left:0}
  .lg-seg:last-of-type{border-bottom:1px solid var(--line)}
  .lg-seg__n{font-size:13px;flex:1 1 auto}
  .lg-seg__t{margin:0;flex:0 0 auto}
  .lg-seg__ticks{position:static;height:auto;display:flex;gap:3px;flex:0 0 auto}
  .lg-seg__ticks i{position:static;width:2px;height:11px}
  .lg-bar__play{display:none}
}
/* телефон */
@media (max-width:760px){
  .lg{font-size:16px}
  .lg .in{padding:0 20px}
  .lg-hero{min-height:auto}
  .lg-stats{grid-template-columns:1fr 1fr;gap:22px 8px}
  .lg-rate,.lg-cred__grid{grid-template-columns:1fr}
  .lg-two{grid-template-columns:1fr}
  .lg-looks{grid-template-columns:repeat(auto-fill,minmax(126px,1fr));gap:8px}
  .lg-brand__h{gap:6px 16px}
  .lg-bar__legend span:nth-child(2){display:none}
}
/* ландшафт телефона */
@media (max-height:520px) and (orientation:landscape){
  .lg-hero{min-height:auto;padding-top:72px}
  .lg h1{font-size:clamp(40px,7vw,72px)}
}
@media (prefers-reduced-motion:reduce){
  .lg-r{opacity:1;transform:none;transition:none}
  .lg-look img{transition:none}
}
</style>"""


PAGE_JS = """<script>(function(){
 var slow=matchMedia('(prefers-reduced-motion:reduce)').matches;
 var MAP=%MAP%;
 var v=document.getElementById('lg-video');

 // ── перемотка: и сетка лукбука, и дорожка ведут в один плеер ─────────────
 var now=document.getElementById('lg-now'),sec=document.getElementById('lg-player-sec');
 function label(t){
  var b=null;
  for(var i=0;i<MAP.blocks.length;i++)if(t>=MAP.blocks[i].start-0.2)b=MAP.blocks[i];
  return b?b.name:'';
 }
 function mmss(t){t=Math.floor(t);return Math.floor(t/60)+':'+('0'+(t%60)).slice(-2);}
 function seek(t){
  if(!v)return;
  var go=function(){try{v.currentTime=t;}catch(e){}v.play().catch(function(){});};
  if(v.readyState>0)go();else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}
  if(now)now.textContent=label(t)+' · '+mmss(t);
  if(sec)sec.scrollIntoView({behavior:slow?'auto':'smooth',block:'center'});
 }
 document.addEventListener('click',function(e){
  var b=e.target.closest('[data-seek]');if(!b)return;
  seek(parseFloat(b.dataset.seek));
 });

 // ── дорожка: подсветка блока и бегунок по ходу ролика ────────────────────
 var bar=document.getElementById('lg-bar'),play=document.getElementById('lg-play'),
     segs=[].slice.call(document.querySelectorAll('.lg-seg'));
 if(v&&bar)v.addEventListener('timeupdate',function(){
  var t=v.currentTime,k=t/MAP.duration;
  if(play){play.classList.add('is-on');play.style.left=(k*100).toFixed(3)+'%';}
  var cur=null;
  for(var i=0;i<MAP.blocks.length;i++)if(t>=MAP.blocks[i].start-0.2)cur=MAP.blocks[i].slug;
  segs.forEach(function(s){s.classList.toggle('is-on',s.dataset.slug===cur);});
 });

 // ── пульс: кривая приближения модели к камере за весь ролик ──────────────
 var cv=document.getElementById('lg-pulse');
 if(cv&&MAP.pulse&&MAP.pulse.length){
  var draw=function(){
   var dpr=Math.min(2,window.devicePixelRatio||1),
       w=cv.clientWidth||1200,h=Math.max(180,Math.round(w*0.19));
   cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr);
   cv.style.height=h+'px';
   var g=cv.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,w,h);
   var P=MAP.pulse,n=P.length,pad=10,H=h-pad*2;
   // границы блоков — вертикали под кривой
   g.strokeStyle='rgba(246,242,239,.10)';g.lineWidth=1;
   MAP.blocks.forEach(function(b){
    var x=Math.round(b.start/MAP.duration*w)+0.5;
    g.beginPath();g.moveTo(x,pad);g.lineTo(x,h-pad);g.stroke();
   });
   // заливка под кривой
   var grad=g.createLinearGradient(0,pad,0,h-pad);
   grad.addColorStop(0,'rgba(230,0,126,.42)');
   grad.addColorStop(1,'rgba(230,0,126,0)');
   g.beginPath();g.moveTo(0,h-pad);
   for(var i=0;i<n;i++)g.lineTo(i/(n-1)*w,h-pad-P[i]/1000*H);
   g.lineTo(w,h-pad);g.closePath();g.fillStyle=grad;g.fill();
   // сама кривая
   g.beginPath();
   for(var j=0;j<n;j++){var x=j/(n-1)*w,y=h-pad-P[j]/1000*H;
    if(j)g.lineTo(x,y);else g.moveTo(x,y);}
   g.strokeStyle='rgba(246,242,239,.85)';g.lineWidth=1.2;g.stroke();
   // засечки выходов
   g.fillStyle='#e6007e';
   MAP.blocks.forEach(function(b){b.looks.forEach(function(l){
    g.fillRect(l.t/MAP.duration*w-1,h-pad-4,2,4);
   });});
  };
  draw();
  var to=null;
  addEventListener('resize',function(){clearTimeout(to);to=setTimeout(draw,150);});
 }

 // ── появление блоков: свип по скроллу, а не IntersectionObserver.
 // Наблюдатель отдаёт колбэк на следующем кадре, и при быстрой прокрутке
 // до низа нижние блоки остаются с opacity:0. Свип считает геометрию
 // синхронно, невидимого контента не остаётся.
 var els=[].slice.call(document.querySelectorAll('.lg-r'));
 function sweep(){
  for(var i=els.length-1;i>=0;i--){
   var r=els[i].getBoundingClientRect();
   if(r.top<innerHeight*1.1&&r.bottom>-120){els[i].classList.add('is-in');els.splice(i,1);}
  }
  if(!els.length){removeEventListener('scroll',sweep);removeEventListener('resize',sweep);}
 }
 addEventListener('scroll',sweep,{passive:true});
 addEventListener('resize',sweep);
 sweep();
})();</script>"""


BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Видеопродакшн","item":"https://hand-marketing.ru/videoproduction/"},'
  '{"@type":"ListItem","position":3,"name":"Подиумная съёмка для журнала Lingerie",'
  f'"item":"{URL}"}}]}}</script>')


HEAD = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<!--custom-page-->'
        f'<title>{TITLE}</title>'
        f'<meta name="description" content="{DESCR}">'
        f'<link rel="canonical" href="{URL}">'
        '<meta property="og:type" content="article">'
        f'<meta property="og:title" content="{TITLE}">'
        f'<meta property="og:description" content="{DESCR}">'
        f'<meta property="og:url" content="{URL}">'
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/hall.jpg">'
        '<link rel="stylesheet" href="/fonts/oranienbaum-mulish.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    thin = {'duration': DUR,
            'blocks': [{'slug': b['slug'], 'name': b['name'], 'start': b['start'],
                        'looks': [{'t': l['t']} for l in b['looks']]}
                       for b in BLOCKS],
            'pulse': MAP['pulse']}
    js = PAGE_JS.replace('%MAP%', json.dumps(thin, ensure_ascii=False,
                                             separators=(',', ':')))
    # своего блока «обсудить проект» нет: страницу закрывает фиолетовая форма
    # из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="lg">{hero()}{brief()}{track()}'
            f'{lookbook()}{pulse()}{player()}{credits()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'lingerie')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
    print('written', p, os.path.getsize(p) // 1024, 'KB')
