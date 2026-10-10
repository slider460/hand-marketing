# -*- coding: utf-8 -*-
"""
Дизайн-система новых страниц услуг (v3, октябрь 2026): стиль исходного верха главной.

Призрачное слово за заголовком, размытые 3D-фигуры, жёлтая кнопка, тёмный баннер кейса
с синей чертой, круглые обложки кейсов из каталога, фиолетовая секция, шаги с бледными
цифрами, вопросы с жёлтым плюсом. Макеты всех страниц лежат на холсте
«Новые страницы в дизайн-системе HM» (claude.ai, артефакт 77XcoywYo2qLxkzi3qhpVb).

    import hm_ds as ds
    ds.CSS                         -> <style> в HEAD (после rc.CSS)
    ds.hero(...), ds.sec(...), ds.cases(...), ds.cost('ad'), ds.faq(...)

Все классы в пространстве .hd-*, корень <main class="hd" style="--a:#цвет">.
Призрачное слово выводится через ::before из data-ghost: в текст страницы оно не попадает.
Шрифт только локальный /fonts/montserrat.css (rc.FONT), внешних CDN нет.
Длинного тире в текстах нет (правило сайта).
"""
import html as H
import json
import os
import re

import commerce_block as cb

HERE = os.path.dirname(os.path.abspath(__file__))

# цвета направлений, как в метках сервисов на главной
EXH, EV, VID, CON, MAP, CRE = '#8E5FB0', '#673A7E', '#CF6F19', '#E0427E', '#7E3FA0', '#C12164'
PRN, PHO, BTL, DIG, VIOLET = '#E08A2B', '#3B729D', '#D6357E', '#5E9A2E', '#730FBF'

# 3D-фигуры: чёткие маленькие (иконки) и размытые большие (фон героя)
FIG = [f'/images/ds/fig-{n}.svg' for n in ('01', '03', '05', '07', '09', '11', '13', '15')]
BLUR = {
    'disc': '/images/lib/as3436-6364-4661-a130-303235663166/__-25.png',
    'blocks': '/images/lib/as6563-6234-4536-b165-656236646638/__-26.png',
    'h': '/images/lib/as3633-3432-4235-b433-346566646565/__-27.png',
}


def _covers():
    """Круглые обложки кейсов из карусели каталога: те же, что на главной и /project."""
    car = open(os.path.join(HERE, 'carousels', 'all.html'), encoding='utf-8').read()
    return {m.group(1).rstrip('/'): m.group(2) for m in
            re.finditer(r'<a class="mcase" href="([^"]+)"[^>]*>.*?<img[^>]+src="([^"]+)"', car, re.S)}


COVERS = _covers()


def esc(s):
    return H.escape(s, quote=False)


def attr(s):
    return H.escape(s, quote=True)


CSS = """<style id="hm-ds-css">
.hd{--a:#730FBF;--ink:#111;--mut:#4C4C4C;--soft:#8A8A8A;--line:#E6E6E6;--ghost:#ECECEC;--tint:#F6F4F9;
 --y:#FFF700;--amber:#FCB724;--dark:#14171C;--violet:#730FBF;--blue:#4A9FFF;
 font-family:'Montserrat',Arial,sans-serif;font-weight:500;color:#222;background:#fff;overflow-x:clip;-webkit-font-smoothing:antialiased}
.hd *,.hd *::before,.hd *::after{box-sizing:border-box}
.hd img{max-width:100%;height:auto}
.hd a{color:inherit}
.hd-w{max-width:1180px;margin:0 auto;padding:0 40px;position:relative}
.hd-crumbs{font-size:13px;color:var(--soft);padding:18px 0 0;margin:0}
.hd-crumbs a{color:var(--soft);text-decoration:none}
.hd-crumbs a:hover{color:var(--ink)}
/* герой */
.hd-hero{position:relative;text-align:center;padding:26px 0 60px;overflow:hidden}
.hd-hero__g{margin:0;font-weight:800;font-size:clamp(46px,9vw,128px);line-height:1;color:var(--ghost);letter-spacing:-.02em;white-space:nowrap;user-select:none}
.hd-hero__g::before{content:attr(data-ghost)}
.hd-k{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--a)}
.hd-hero .hd-k{margin:14px 0 12px}
.hd-hero h1{margin:0 auto;max-width:20ch;font-size:clamp(30px,4vw,52px);font-weight:700;line-height:1.08;color:var(--ink);letter-spacing:-.01em}
.hd-hero__lede{margin:20px auto 0;max-width:64ch;font-size:17px;line-height:1.65;color:var(--mut)}
.hd-hero__lede a{color:var(--ink);text-decoration:none;border-bottom:2px solid var(--y)}
.hd-chips{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:24px 0 0;padding:0;list-style:none}
.hd-chips li{border:1.5px solid var(--ink);border-radius:30px;padding:8px 16px;font-size:13px;font-weight:600;color:var(--ink)}
.hd-acts{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:28px}
.hd-btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 30px;border-radius:30px;font:800 15px/1 'Montserrat',Arial,sans-serif;text-decoration:none;border:1.5px solid transparent;cursor:pointer;transition:transform .15s}
.hd-btn:hover{transform:translateY(-2px)}
.hd .hd-btn--y{background:var(--y);color:#000}
.hd .hd-btn--d{background:var(--dark);color:#fff}
.hd .hd-btn--o{background:transparent;color:var(--ink);border-color:var(--ink)}
.hd-fig{position:absolute;pointer-events:none;user-select:none;height:auto}
.hd-fig--b{filter:blur(2px);opacity:.9}
/* баннер кейса */
.hd .hd-banner{color:#fff}
.hd-banner{position:relative;display:block;max-width:940px;margin:0 auto;aspect-ratio:940/420;background:var(--dark);overflow:hidden;text-decoration:none;color:#fff}
.hd-banner>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
.hd-banner:hover>img{transform:scale(1.03)}
.hd-banner__v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s ease}
.hd-banner__v.is-on{opacity:1}
@media(prefers-reduced-motion:reduce){.hd-banner__v{display:none}}
.hd-banner__sh{position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,16,22,.92) 0%,rgba(14,16,22,.7) 45%,rgba(14,16,22,.05) 80%)}
.hd-banner__in{position:absolute;left:48px;top:50%;transform:translateY(-50%);max-width:480px}
.hd-banner .hd-k{color:var(--blue)}
.hd-banner__t{display:block;margin:12px 0 0;font-size:clamp(26px,3vw,40px);font-weight:700;line-height:1.1}
.hd-banner__t::after{content:"";display:inline-block;width:64px;height:4px;background:var(--blue);margin-left:14px;vertical-align:middle;border-radius:2px}
.hd-banner__p{display:block;margin:14px 0 0;font-size:16px;line-height:1.55;color:rgba(255,255,255,.86)}
.hd-banner .hd-chips{justify-content:flex-start;margin-top:18px}
.hd-banner .hd-chips li{border-color:rgba(255,255,255,.75);color:#fff}
/* секции */
.hd-sec{padding:76px 0;position:relative}
.hd-sec--alt{background:var(--tint)}
.hd-sec--top{padding-top:96px}
.hd-sh{display:flex;align-items:center;gap:28px;margin:0 0 36px}
.hd-sh h2{margin:0;font-size:clamp(28px,3.4vw,46px);font-weight:700;line-height:1.1;color:var(--ink);letter-spacing:-.01em}
.hd-sh__row{display:flex;gap:42px;align-items:center;flex:1;justify-content:flex-end}
.hd-sh__row img{width:22px;height:22px}
.hd-lead{margin:-18px 0 34px;max-width:70ch;font-size:16px;line-height:1.65;color:var(--mut)}
.hd-lead a,.hd-txt a,.hd-feat p a,.hd-step p a{color:var(--ink);text-decoration:none;border-bottom:2px solid var(--y)}
.hd-note{margin:30px 0 0;max-width:80ch;font-size:14.5px;line-height:1.65;color:var(--mut)}
.hd-note a{color:var(--ink);text-decoration:none;border-bottom:2px solid var(--y)}
/* круглые обложки кейсов */
.hd-cases{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:44px 28px}
.hd-cases--3{grid-template-columns:repeat(3,minmax(0,1fr));gap:52px 40px}
.hd-case{text-decoration:none;color:var(--ink);display:block}
.hd-case__img{display:block;width:100%;aspect-ratio:477/396;object-fit:contain;transition:transform .3s ease}
.hd-case__img--ph{object-fit:cover;border-radius:50%;aspect-ratio:1/1;width:82%;margin:0 auto}
.hd-case:hover .hd-case__img{transform:translateY(-6px)}
.hd-case i{display:block;margin-top:14px;font-style:normal;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--a)}
.hd-case i+b{margin-top:6px}
.hd-case b{display:block;margin-top:14px;font-size:16px;font-weight:700;line-height:1.3}
.hd-case span{display:block;margin-top:6px;font-size:14px;line-height:1.5;color:var(--mut)}
.hd-case em{display:inline-block;margin-top:10px;font-style:normal;font-size:13px;font-weight:700;border-bottom:2px solid var(--y)}
/* колонки с 3D-иконкой */
.hd-feats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:44px 36px}
.hd-feats--4{grid-template-columns:repeat(4,minmax(0,1fr))}
.hd-feats--2{grid-template-columns:repeat(2,minmax(0,1fr))}
.hd-feat>img{width:34px;height:34px;display:block;margin-bottom:14px}
.hd-feat b{display:block;font-size:17px;font-weight:700;line-height:1.3;color:var(--ink)}
.hd-feat p{margin:8px 0 0;font-size:14.5px;line-height:1.6;color:var(--mut)}
.hd-feat__tag{display:inline-block;margin-top:12px;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--a)}
/* фото с подписью */
.hd-tiles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:36px 28px}
.hd-tiles--4{grid-template-columns:repeat(4,minmax(0,1fr));gap:24px 20px}
.hd-tiles--2{grid-template-columns:repeat(2,minmax(0,1fr))}
.hd-tile{margin:0}
.hd-tile img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
.hd-tiles--4 .hd-tile img{aspect-ratio:4/5}
.hd-tile figcaption{margin-top:14px}
.hd-tile b{display:block;font-size:17px;font-weight:700;line-height:1.3;color:var(--ink)}
.hd-tile span{display:block;margin-top:6px;font-size:14.5px;line-height:1.6;color:var(--mut)}
.hd-tile small{display:block;font-size:13.5px;line-height:1.55;color:var(--mut)}
/* фиолетовая и тёмная секции */
.hd-violet,.hd-dark{color:#fff;padding:84px 0;position:relative;overflow:hidden}
.hd-violet{background:var(--violet)}
.hd-dark{background:var(--dark)}
.hd-violet h2,.hd-dark h2{margin:0 0 16px;font-size:clamp(30px,3.6vw,48px);font-weight:700;line-height:1.1;color:#fff}
.hd-violet .hd-k,.hd-dark .hd-k{color:var(--amber);margin-bottom:12px}
.hd-dlead{margin:0 0 40px;max-width:64ch;font-size:16px;line-height:1.7;color:rgba(255,255,255,.84)}
.hd-dlead a{color:#fff;text-decoration:none;border-bottom:2px solid var(--amber)}
.hd-violet .hd-feat b,.hd-dark .hd-feat b,.hd-violet .hd-tile b,.hd-dark .hd-tile b{color:#fff}
.hd-violet .hd-feat p,.hd-dark .hd-feat p,.hd-violet .hd-tile span,.hd-dark .hd-tile span,.hd-dark .hd-tile small{color:rgba(255,255,255,.8)}
.hd-violet .hd-step p a,.hd-dark .hd-step p a,.hd-violet .hd-feat p a,.hd-dark .hd-feat p a{color:#fff;border-bottom-color:var(--amber)}
.hd-dark .hd-note,.hd-violet .hd-note{color:rgba(255,255,255,.72)}
.hd-dark .hd-note a,.hd-violet .hd-note a{color:#fff}
/* цифры */
.hd-nums{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px}
.hd-nums--3{grid-template-columns:repeat(3,minmax(0,1fr))}
.hd-num b{display:block;font-size:clamp(34px,3.4vw,46px);font-weight:800;line-height:1;letter-spacing:-.02em;color:var(--a)}
.hd-num span{display:block;margin-top:10px;font-size:14px;line-height:1.55;color:var(--mut)}
.hd-violet .hd-num b{color:var(--y)}
.hd-dark .hd-num b{color:var(--amber)}
.hd-violet .hd-num span,.hd-dark .hd-num span{color:rgba(255,255,255,.82)}
.hd-split .hd-num b{font-size:clamp(26px,2.4vw,34px)}
.hd-h2--gap{margin-bottom:48px!important}
.hd-nums--c{text-align:center;max-width:960px;margin:44px auto 0}
.hd-nums--c .hd-num b{font-size:clamp(40px,4.4vw,58px)}
/* шаги с бледными цифрами */
.hd-steps{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:30px 26px;counter-reset:hds}
.hd-steps--3{grid-template-columns:repeat(3,minmax(0,1fr))}
.hd-steps--4{grid-template-columns:repeat(4,minmax(0,1fr))}
.hd-step i{display:block;font-style:normal;font-size:64px;font-weight:800;line-height:1;color:var(--ghost)}
.hd-step b{display:block;margin-top:-18px;font-size:16.5px;font-weight:700;line-height:1.3;color:var(--ink);position:relative}
.hd-step p{margin:8px 0 0;font-size:14.5px;line-height:1.6;color:var(--mut)}
.hd-violet .hd-step i{color:rgba(255,255,255,.16)}
.hd-dark .hd-step i{color:rgba(255,255,255,.1)}
.hd-violet .hd-step b,.hd-dark .hd-step b{color:#fff}
.hd-violet .hd-step p,.hd-dark .hd-step p{color:rgba(255,255,255,.82)}
/* полосы хронометража */
.hd-bars{display:grid;gap:30px;max-width:1080px}
.hd-bar__h{display:flex;justify-content:space-between;align-items:baseline;gap:16px}
.hd-bar__h b{font-size:18px;font-weight:700;color:var(--ink)}
.hd-bar__h strong{font-size:28px;font-weight:800;color:var(--a);white-space:nowrap}
.hd-bar__t{height:14px;margin:10px 0;background:#F1ECE6}
.hd-bar__t span{display:block;height:100%;background:var(--a)}
.hd-bar p{margin:0;font-size:14.5px;line-height:1.6;color:var(--mut)}
.hd-bar p a{color:var(--ink);text-decoration:none;border-bottom:2px solid var(--y)}
/* строки «задача / ответ» */
.hd-rows{border-top:1.5px solid var(--ink);max-width:1080px}
.hd-row{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.5fr);gap:32px;padding:22px 0;border-bottom:1px solid var(--line)}
.hd-row b{font-size:18px;font-weight:700;line-height:1.35;color:var(--a)}
.hd-row span{font-size:15px;line-height:1.65;color:#222}
.hd-row span a{color:var(--ink);text-decoration:none;border-bottom:2px solid var(--y)}
/* таблица «кто за что» */
.hd-duty{border-top:1.5px solid var(--ink);max-width:920px}
.hd-duty>div{display:grid;grid-template-columns:minmax(0,1fr) 150px 150px;align-items:center;border-bottom:1px solid var(--line);padding:14px 0;font-size:15px}
.hd-duty i{font-style:normal;text-align:center;font-weight:800;color:var(--a);font-size:18px}
.hd-duty .hd-duty__h{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.hd-duty .hd-duty__h i{font-size:12px;color:var(--mut)}
.hd-duty small{display:block;margin-top:3px;font-size:13px;color:var(--mut)}
/* стоимость и отзывы */
.hd-cost{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:56px;align-items:start}
.hd-cost--solo{grid-template-columns:minmax(0,1fr)}
.hd-cost__p{border-top:1.5px solid var(--ink)}
.hd-cost__row{padding:24px 0;border-bottom:1px solid var(--line)}
.hd-cost__row small{display:block;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--a)}
.hd-cost__row b{display:block;margin-top:10px;font-size:clamp(28px,3vw,36px);font-weight:800;color:var(--ink);letter-spacing:-.01em}
.hd-cost__f{margin:20px 0 0;padding:0;list-style:none;display:grid;gap:10px}
.hd-cost__f li{position:relative;padding-left:22px;font-size:14.5px;line-height:1.6;color:var(--mut)}
.hd-cost__f li::before{content:"";position:absolute;left:0;top:.45em;width:10px;height:10px;border-radius:50%;background:var(--y);box-shadow:0 0 0 1.5px var(--ink)}
.hd-cost .hd-btn{margin-top:24px}
.hd-cost__r{display:grid;gap:18px}
.hd-q{margin:0;background:var(--tint);padding:34px 38px 30px;position:relative}
.hd-sec--alt .hd-q{background:#fff}
.hd-q::before{content:"«";display:block;font-size:84px;line-height:.62;font-weight:800;color:var(--violet)}
.hd-q blockquote{margin:12px 0 0;font-size:18px;line-height:1.55;font-weight:500;color:var(--ink)}
.hd-q figcaption{margin-top:18px;display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap;font-size:13.5px;line-height:1.5;color:var(--mut)}
.hd-q figcaption b{display:block;font-size:15px;color:var(--ink)}
.hd-q figcaption a,.hd-cost__all{font-size:13.5px;font-weight:700;text-decoration:none;border-bottom:2px solid var(--y);color:var(--ink);white-space:nowrap}
.hd-cost__all{display:inline-block;margin-top:4px;justify-self:start}
/* вопросы */
.hd-faq{max-width:880px;border-top:1.5px solid var(--ink)}
.hd-faq details{border-bottom:1px solid var(--line)}
.hd-faq summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:24px;padding:22px 0;font-size:17px;font-weight:700;color:var(--ink);cursor:pointer}
.hd-faq summary::-webkit-details-marker{display:none}
.hd-faq summary::after{content:"+";flex:0 0 36px;height:36px;border-radius:50%;background:var(--y);display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:600;line-height:1;color:#000}
.hd-faq details[open] summary::after{content:"−"}
.hd-faq p{margin:0 0 22px;max-width:72ch;font-size:15px;line-height:1.7;color:var(--mut)}
.hd-faq p a{color:var(--ink);text-decoration:none;border-bottom:2px solid var(--y)}
/* лента по шагам (горизонтальная) */
.hd-strip{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);border-top:2px solid var(--amber)}
.hd-strip>div{padding:24px 22px 0 0}
.hd-strip__n{display:block;font-size:52px;font-weight:800;line-height:1;color:var(--amber)}
.hd-strip__u{display:block;margin-top:4px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.6)}
.hd-strip b{display:block;margin-top:18px;font-size:16px;font-weight:700;color:#fff}
.hd-strip p{margin:8px 0 0;font-size:13.5px;line-height:1.6;color:rgba(255,255,255,.78)}
.hd-strip img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;margin-top:16px}
/* ступени форматов */
.hd-ladder{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);gap:16px;align-items:end}
.hd-ladder>div{background:#fff;border-top:4px solid var(--a);padding:26px 24px;display:flex;flex-direction:column}
.hd-ladder i{font-style:normal;font-size:48px;font-weight:800;line-height:1;color:var(--ghost)}
.hd-ladder b{margin-top:14px;font-size:19px;font-weight:700;color:var(--ink)}
.hd-ladder p{margin:8px 0 0;font-size:14.5px;line-height:1.6;color:var(--mut);flex:1}
.hd-ladder small{margin-top:16px;font-size:13px;font-weight:700;color:var(--a)}
.hd-ladder>div:last-child{background:var(--a);color:#fff}
.hd-ladder>div:last-child i{color:rgba(255,255,255,.35)}
.hd-ladder>div:last-child b{color:#fff}
.hd-ladder>div:last-child p{color:rgba(255,255,255,.86)}
.hd-ladder>div:last-child small{color:var(--y)}
/* две колонки и фотомозаика */
.hd-split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:52px;align-items:start}
.hd-split--r{grid-template-columns:minmax(0,1fr) minmax(0,1.2fr)}
.hd-split--c{align-items:center}
.hd-mosaic{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.hd-mosaic figure{margin:0}
.hd-mosaic img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.hd-mosaic figure:first-child{grid-column:1/-1}
.hd-mosaic figure:first-child img{aspect-ratio:2/1}
.hd-mosaic figcaption{margin-top:10px;font-size:13px;line-height:1.5;color:var(--mut)}
.hd-violet .hd-mosaic figcaption,.hd-dark .hd-mosaic figcaption{color:rgba(255,255,255,.72)}
.hd-steps--1{grid-template-columns:minmax(0,1fr);gap:24px}
/* внутренние ссылки-метки */
.hd-links{display:grid;grid-template-columns:auto minmax(0,1fr);gap:16px 24px;align-items:center}
.hd-links>b{font-size:14px;color:var(--ink)}
.hd-links ul{display:flex;flex-wrap:wrap;gap:10px;margin:0;padding:0;list-style:none}
.hd-links a{display:inline-block;border:1.5px solid var(--ink);border-radius:30px;padding:8px 16px;font-size:13px;font-weight:600;text-decoration:none;color:var(--ink);transition:background .15s}
.hd-links a:hover{background:var(--y)}
@media(max-width:980px){
 .hd-cases,.hd-cases--3,.hd-feats,.hd-feats--4,.hd-tiles,.hd-tiles--4,.hd-nums{grid-template-columns:repeat(2,minmax(0,1fr))}
 .hd-steps,.hd-steps--3,.hd-steps--4{grid-template-columns:repeat(2,minmax(0,1fr))}
 .hd-cost{grid-template-columns:minmax(0,1fr);gap:36px}
 .hd-split,.hd-split--r{grid-template-columns:minmax(0,1fr);gap:36px}
 .hd-ladder{grid-auto-flow:row;grid-template-columns:repeat(2,minmax(0,1fr))}
 .hd-ladder>div{min-height:0!important}
 .hd-strip{grid-auto-flow:row;grid-template-columns:repeat(3,minmax(0,1fr));row-gap:28px}
 .hd-sh__row{gap:24px}
}
@media(max-width:860px){
 .hd-banner{aspect-ratio:auto;min-height:460px}
 .hd-banner__in{left:22px;right:22px;top:auto;bottom:26px;transform:none;max-width:none}
 .hd-banner__sh{background:linear-gradient(0deg,rgba(14,16,22,.95) 0%,rgba(14,16,22,.62) 58%,rgba(14,16,22,.08) 100%)}
 .hd-row{grid-template-columns:minmax(0,1fr);gap:8px}
}
@media(max-width:640px){
 .hd-w{padding:0 18px}
 .hd-hero{padding:18px 0 44px}
 .hd-hero__lede{font-size:16px}
 .hd-sec{padding:56px 0}
 .hd-sec--top{padding-top:64px}
 .hd-violet,.hd-dark{padding:60px 0}
 .hd-sh{margin-bottom:28px}
 .hd-sh__row{display:none}
 .hd-lead{margin:-12px 0 28px}
 .hd-cases,.hd-cases--3{grid-template-columns:repeat(2,minmax(0,1fr));gap:30px 14px}
 .hd-case b{font-size:14.5px}
 .hd-case span{font-size:13px}
 .hd-feats,.hd-feats--4,.hd-feats--2,.hd-tiles,.hd-tiles--2,.hd-steps,.hd-steps--3,.hd-steps--4{grid-template-columns:minmax(0,1fr)}
 .hd-tiles--4{grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 12px}
 .hd-nums,.hd-nums--3{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 16px}
 .hd-nums--c{grid-template-columns:minmax(0,1fr)}
 .hd-ladder{grid-template-columns:minmax(0,1fr)}
 .hd-strip{grid-template-columns:repeat(2,minmax(0,1fr))}
 .hd-strip__n{font-size:42px}
 .hd-duty>div{grid-template-columns:minmax(0,1fr) 56px 88px;font-size:14px}
 .hd-duty .hd-duty__h{font-size:10px;letter-spacing:.02em}
 .hd-duty .hd-duty__h i{font-size:10px}
 .hd-violet>.hd-fig,.hd-dark>.hd-fig{top:14px!important;right:14px!important;width:60px!important;opacity:.55}
 .hd-q{padding:28px 22px 24px}
 .hd-q blockquote{font-size:16.5px}
 .hd-faq summary{font-size:15.5px;padding:18px 0}
 .hd-links{grid-template-columns:minmax(0,1fr);gap:10px}
 .hd-links>b{margin-top:8px}
 .hd-fig{max-width:22vw}
 .hd-hero .hd-fig--b{top:34px!important;max-width:16vw}
 .hd-fig--hide{display:none}
}
@media(max-width:400px){
 .hd-cases,.hd-cases--3{grid-template-columns:minmax(0,1fr)}
 .hd-case__img{max-width:300px;margin:0 auto}
}
@media(prefers-reduced-motion:reduce){.hd-btn,.hd-banner>img,.hd-case__img{transition:none}}
</style>"""


def figs_row(n=3, start=0):
    """Ряд маленьких 3D-фигур справа от заголовка секции, как «О нас» на главной."""
    pics = ''.join(f'<img src="{FIG[(start + i) % len(FIG)]}" alt="" width="22" height="22">'
                   for i in range(n))
    return f'<div class="hd-sh__row" aria-hidden="true">{pics}</div>'


def crumbs(items):
    """items: [(текст, href|None)], последний без ссылки."""
    parts = [f'<a href="{href}">{esc(t)}</a>' if href else esc(t) for t, href in items]
    return (f'<div class="hd-w"><nav class="hd-crumbs" aria-label="Навигация по разделам">'
            f'{" · ".join(parts)}</nav></div>')


HERO_FIGS = {
    0: [('b', 'disc', 'width:120px;left:5%;top:96px'), ('s', 1, 'width:34px;left:23%;top:30px'),
        ('b', 'blocks', 'width:112px;right:6%;top:160px')],
    1: [('b', 'blocks', 'width:118px;left:5%;top:110px'), ('s', 3, 'width:32px;right:25%;top:28px'),
        ('b', 'h', 'width:104px;right:6%;top:190px')],
    2: [('b', 'h', 'width:104px;left:6%;top:120px'), ('s', 4, 'width:34px;left:22%;top:26px'),
        ('b', 'disc', 'width:118px;right:6%;top:150px')],
}


def _hero_figs(variant):
    out = ''
    for i, (kind, ref, style) in enumerate(HERO_FIGS[variant % len(HERO_FIGS)]):
        hide = ' hd-fig--hide' if i == 1 else ''
        if kind == 'b':
            out += (f'<img class="hd-fig hd-fig--b{hide}" src="{BLUR[ref]}" alt="" aria-hidden="true" '
                    f'style="{style}" width="240" height="240">')
        else:
            out += (f'<img class="hd-fig{hide}" src="{FIG[ref]}" alt="" aria-hidden="true" '
                    f'style="{style}" width="34" height="34">')
    return out


def hero(ghost, kicker, h1, lede_html, chips=(), ctas=(), figs=0):
    """lede_html уже экранирован (может содержать ссылки). ctas: [(текст, href, 'y'|'d'|'o')]."""
    chips_html = ''.join(f'<li>{esc(c)}</li>' for c in chips)
    chips_html = f'<ul class="hd-chips">{chips_html}</ul>' if chips_html else ''
    acts = ''.join(f'<a class="hd-btn hd-btn--{kind}" href="{href}">{esc(t)}</a>' for t, href, kind in ctas)
    acts = f'<div class="hd-acts">{acts}</div>' if acts else ''
    return (f'<section class="hd-hero">{_hero_figs(figs)}<div class="hd-w">'
            f'<p class="hd-hero__g" data-ghost="{attr(ghost)}" aria-hidden="true"></p>'
            f'<p class="hd-k">{esc(kicker)}</p><h1>{esc(h1)}</h1>'
            f'<p class="hd-hero__lede">{lede_html}</p>{chips_html}{acts}</div></section>')


def banner(href, img, alt, kicker, title, text, chips=(), priority=True, video=None):
    """video: немой луп поверх постера, включается BANNER_JS после реального старта."""
    vid = (f'<video class="hd-banner__v" autoplay muted loop playsinline preload="auto" aria-hidden="true">'
           f'<source src="{video}" type="video/mp4"></video>') if video else ''
    chips_html = ''.join(f'<li>{esc(c)}</li>' for c in chips)
    chips_html = f'<ul class="hd-chips">{chips_html}</ul>' if chips_html else ''
    load = 'fetchpriority="high" decoding="async"' if priority else 'loading="lazy" decoding="async"'
    tag, href_attr = ('a', f' href="{href}"') if href else ('div', '')
    return (f'<div class="hd-w"><{tag} class="hd-banner"{href_attr}>'
            f'<img src="{img}" alt="{attr(alt)}" width="1600" height="900" {load}>{vid}'
            f'<span class="hd-banner__sh" aria-hidden="true"></span><span class="hd-banner__in">'
            f'<span class="hd-k">{esc(kicker)}</span><span class="hd-banner__t">{esc(title)}</span>'
            f'<span class="hd-banner__p">{esc(text)}</span>{chips_html}</span></{tag}></div>')


def sec(inner, h2=None, lead_html=None, alt=False, icons=0, icon_start=0, top=False, sid=None):
    cls = 'hd-sec' + (' hd-sec--alt' if alt else '') + (' hd-sec--top' if top else '')
    sid = f' id="{sid}"' if sid else ''
    head = ''
    if h2:
        head = f'<div class="hd-sh"><h2>{esc(h2)}</h2>{figs_row(icons, icon_start) if icons else ""}</div>'
    lead = f'<p class="hd-lead">{lead_html}</p>' if lead_html else ''
    return f'<section class="{cls}"{sid}><div class="hd-w">{head}{lead}{inner}</div></section>'


def band(inner, h2, lead_html=None, kicker=None, dark=False, fig='disc'):
    """Фиолетовая (как «О нас» на главной) или тёмная полоса."""
    cls = 'hd-dark' if dark else 'hd-violet'
    k = f'<p class="hd-k">{esc(kicker)}</p>' if kicker else ''
    lead = f'<p class="hd-dlead">{lead_html}</p>' if lead_html else ''
    gap = '' if lead_html else ' class="hd-h2--gap"'
    return (f'<section class="{cls}"><img class="hd-fig hd-fig--b" src="{BLUR[fig]}" alt="" '
            f'aria-hidden="true" style="width:118px;right:5%;top:40px" width="240" height="240">'
            f'<div class="hd-w">{k}<h2{gap}>{esc(h2)}</h2>{lead}{inner}</div></section>')


def cover(href):
    return COVERS.get(href.rstrip('/'))


def cases(items, cols=3, more='Смотреть кейс'):
    """items: [(href, заголовок, текст, запасное_фото|None[, метка])]. Обложка из каталога по href."""
    cards = ''
    for it in items:
        href, title, text, photo = it[:4]
        tag = f'<i>{esc(it[4])}</i>' if len(it) > 4 and it[4] else ''
        img = cover(href)
        if img:
            pic = f'<img class="hd-case__img" src="{img}" alt="" width="477" height="396" loading="lazy">'
        else:
            pic = (f'<img class="hd-case__img hd-case__img--ph" src="{photo}" alt="" width="400" '
                   f'height="400" loading="lazy">')
        more_html = f'<em>{esc(more)}</em>' if more else ''
        cards += (f'<a class="hd-case" href="{href}">{pic}{tag}<b>{esc(title)}</b>'
                  f'<span>{esc(text)}</span>{more_html}</a>')
    mod = ' hd-cases--3' if cols == 3 else ''
    return f'<div class="hd-cases{mod}">{cards}</div>'


def feats(items, cols=3, start=0, icons=True):
    """items: [(заголовок, текст_html)] или [(заголовок, текст_html, метка)]."""
    out = ''
    for i, it in enumerate(items):
        t, d = it[0], it[1]
        tag = f'<span class="hd-feat__tag">{esc(it[2])}</span>' if len(it) > 2 and it[2] else ''
        ico = (f'<img src="{FIG[(start + i) % len(FIG)]}" alt="" aria-hidden="true" width="34" height="34">'
               if icons else '')
        out += f'<div class="hd-feat">{ico}<b>{esc(t)}</b><p>{d}</p>{tag}</div>'
    mod = {4: ' hd-feats--4', 2: ' hd-feats--2'}.get(cols, '')
    return f'<div class="hd-feats{mod}">{out}</div>'


def tiles(items, cols=3):
    """items: [(img, alt, заголовок|None, текст)]."""
    out = ''
    for img, alt, t, d in items:
        cap = (f'<b>{esc(t)}</b><span>{esc(d)}</span>' if t else f'<small>{esc(d)}</small>')
        out += (f'<figure class="hd-tile"><img src="{img}" alt="{attr(alt)}" width="800" height="600" '
                f'loading="lazy"><figcaption>{cap}</figcaption></figure>')
    mod = {4: ' hd-tiles--4', 2: ' hd-tiles--2'}.get(cols, '')
    return f'<div class="hd-tiles{mod}">{out}</div>'


def nums(items, cols=4, center=False):
    out = ''.join(f'<div class="hd-num"><b>{esc(b)}</b><span>{s}</span></div>' for b, s in items)
    mod = (' hd-nums--3' if cols == 3 else '') + (' hd-nums--c' if center else '')
    return f'<div class="hd-nums{mod}">{out}</div>'


def steps(items, cols=5):
    """items: [(заголовок, текст_html)]."""
    out = ''.join(f'<div class="hd-step"><i aria-hidden="true">{i + 1:02d}</i><b>{esc(t)}</b><p>{d}</p></div>'
                  for i, (t, d) in enumerate(items))
    mod = {1: ' hd-steps--1', 3: ' hd-steps--3', 4: ' hd-steps--4'}.get(cols, '')
    return f'<div class="hd-steps{mod}">{out}</div>'


def mosaic(items):
    """items: [(img, alt, подпись|None)]: первый кадр широкий, остальные парами."""
    out = ''
    for img, alt, cap in items:
        fc = f'<figcaption>{esc(cap)}</figcaption>' if cap else ''
        out += (f'<figure><img src="{img}" alt="{attr(alt)}" width="800" height="600" loading="lazy">'
                f'{fc}</figure>')
    return f'<div class="hd-mosaic">{out}</div>'


def split(left, right, mod=''):
    return f'<div class="hd-split{mod}"><div>{left}</div><div>{right}</div></div>'


def mmss(sec_):
    return f'{sec_ // 60}:{sec_ % 60:02d}'


def bars(items):
    """items: [(название, секунды, текст_html, href|None)]. Длина полосы пропорциональна длительности."""
    top = max(s for _, s, _, _ in items)
    out = ''
    for name, s, text, href in items:
        title = f'<a href="{href}" style="text-decoration:none">{esc(name)}</a>' if href else esc(name)
        out += (f'<div class="hd-bar"><div class="hd-bar__h"><b>{title}</b><strong>{mmss(s)}</strong></div>'
                f'<div class="hd-bar__t" aria-hidden="true"><span style="width:{s / top * 100:.1f}%"></span></div>'
                f'<p>{text}</p></div>')
    return f'<div class="hd-bars">{out}</div>'


def rows(items):
    """items: [(слева, справа_html)]: задача и ответ, формат и пример."""
    out = ''.join(f'<div class="hd-row"><b>{esc(a)}</b><span>{b}</span></div>' for a, b in items)
    return f'<div class="hd-rows">{out}</div>'


def links(groups):
    """groups: [(подпись, [(текст, href)])] — блок внутренних ссылок."""
    out = ''
    for label, items in groups:
        lis = ''.join(f'<li><a href="{h}">{esc(t)}</a></li>' for t, h in items)
        out += f'<b>{esc(label)}</b><ul>{lis}</ul>'
    return f'<div class="hd-links">{out}</div>'


def rub(n):
    return f'{n:,}'.replace(',', ' ') + ' ₽'


def cost(key, with_ld=True):
    """Стоимость и отзывы в стиле дизайн-системы. Данные и schema.org из commerce_block."""
    p = cb.PAGES[key]
    rows_ = ''.join(f'<div class="hd-cost__row"><small>{esc(name)}</small><b>от {rub(price)}</b></div>'
                    for name, price in p['prices'])
    if not rows_:
        rows_ = ('<div class="hd-cost__row"><small>Как считаем смету</small><b>по объёму</b></div>')
    facts = ''.join(f'<li>{esc(f)}</li>' for f in p['facts'])
    price = (f'<div class="hd-cost__p">{rows_}<ul class="hd-cost__f">{facts}</ul>'
             f'<a class="hd-btn hd-btn--d" href="/price/">Все цены</a></div>')
    rev = ''
    if p['reviews']:
        qs = ''
        for k in p['reviews']:
            r = cb.REVIEWS[k]
            link = f'<a href="{r["case"]}">Кейс</a>' if r.get('case') else ''
            qs += (f'<figure class="hd-q"><blockquote>{esc(r["quote"])}</blockquote>'
                   f'<figcaption><span><b>{esc(r["company"])}</b>{esc(r["person"])}, {esc(r["role"])}</span>'
                   f'{link}</figcaption></figure>')
        rev = (f'<div class="hd-cost__r">{qs}<a class="hd-cost__all" href="/reviews/">'
               f'Все благодарственные письма</a></div>')
    solo = '' if rev else ' hd-cost--solo'
    return (f'<div class="hd-cost{solo}" data-hmc="{key}">{price}{rev}</div>'
            + (cb.jsonld(key) if with_ld else ''))


def faq(items, ld=True):
    """items: [(вопрос, ответ_текст)]: ответ экранируется; разметка FAQPage рядом."""
    out = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in items)
    html = f'<div class="hd-faq">{out}</div>'
    if ld:
        data = {'@context': 'https://schema.org', '@type': 'FAQPage',
                'mainEntity': [{'@type': 'Question', 'name': q,
                                'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}
        html += ('<script type="application/ld+json">'
                 + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '</script>')
    return html


BANNER_JS = """<script>(function(){
var v=document.querySelector('.hd-banner__v');if(!v)return;
function show(){v.classList.add('is-on')}
function hide(){v.classList.remove('is-on')}
// Пока ролик не поехал, в баннере остаётся постер. Слой с видео показываем только
// после реального старта: Safari в энергосбережении рисует поверх остановленного
// видео свою кнопку Play, и вместо баннера получается мёртвый плеер.
if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){
 hide();v.removeAttribute('autoplay');v.pause();return}
v.muted=true;
var tries=0;
function attempt(){
 if(v.readyState<3)return;
 var p=v.play();
 if(!p||!p.then){v.paused?hide():show();return}
 p.then(show).catch(function(){hide();if(++tries<12)setTimeout(attempt,700)});
}
['loadeddata','canplay','canplaythrough','progress'].forEach(function(e){
 v.addEventListener(e,attempt)});
attempt();
document.addEventListener('visibilitychange',function(){if(!document.hidden)attempt()});
['pointerdown','touchstart','scroll','keydown'].forEach(function(e){
 window.addEventListener(e,attempt,{passive:true})});
if('IntersectionObserver' in window){
 new IntersectionObserver(function(en){en[0].isIntersecting?attempt():v.pause()},
  {threshold:.05}).observe(v)}
})();</script>"""
