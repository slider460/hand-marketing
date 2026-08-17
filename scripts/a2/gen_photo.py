#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/photo/index.html: страница услуги «Фотопродакшн».

Зачем отдельная страница, а не абзац на /videoproduction: фотосъёмку заказывают
и оценивают отдельно, в тендерах на неё отдельная строка квалификации. Проверяющему
нужен адрес, который сам себя объясняет, и на нём — не только витрина работ, но и
условия сдачи файлов, по которым видно, что каталоги мы уже снимали.

Семантика проверена по Вордстату (Москва и область, 30 дней, август 2026):
  предметная съёмка ........... 1717 широкая / 65 точная
  съёмка оборудования .......... 393
  фотосъёмка для маркетплейсов . 134
  каталожная съёмка ............ 92
  фотосъёмка товаров ........... 50
  фотосъёмка интерьеров ........ 36
  съёмка продукции ............. 28
  бизнес-портрет ............... 19
  фотопродакшн ................. 15 (почти нулевая: держим как имя раздела,
                                     в title и H1 ведёт «предметная съёмка»)

Витрина: сначала опорный фотокейс Saint-Gobain, затем проекты, где съёмка была
наша. У каждой карточки подпись, что именно снимали, чтобы не выдавать
видеокейс за фотографический.

Шрифты общие с кейсом: Exo 2 + Spectral, /fonts/exo2-spectral.css.
Правки: ТОЛЬКО через этот скрипт (маркер <!--custom-page-->)."""
import html as H
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

SG = json.load(open(os.path.join(HERE, 'sgphoto_map.json'), encoding='utf-8'))['stats']

URL = 'https://hand-marketing.ru/photo'
TITLE = 'Предметная съёмка товаров и оборудования для каталогов | Hand Marketing'
DESCR = ('Предметная и каталожная съёмка товаров, оборудования и интерьеров: '
         'вырезанный по контуру фон, кадрирование под квадратные карточки, '
         'ретушь и сдача под печатный каталог, сайт и маркетплейсы. Выезд на '
         'производство и объекты.')

# ─── что снимаем ────────────────────────────────────────────────────────────
KINDS = [
    ('Предметная и каталожная съёмка',
     'Товары и комплектующие на белом: несколько ракурсов на артикул, единая '
     'геометрия по всей линейке, вырезанный по контуру фон. Основной формат для '
     'каталогов и карточек товара.'),
    ('Съёмка оборудования на объекте',
     'Станки, узлы и системы там, где они стоят: на производстве, в цеху, в '
     'учебном центре. Свет привозим с собой, съёмочный стол разворачиваем на месте.'),
    ('Продукт внутри системы',
     'Не только позиция отдельно, но и то, как она работает в сборке. Для '
     'технических каталогов это вторая обязательная картинка на артикул.'),
    ('Съёмка для маркетплейсов',
     'Карточка под требования площадок: квадрат и вертикаль, белый фон, '
     'инфографика по вашему шаблону, именование файлов по артикулам.'),
    ('Репортаж и мероприятия',
     'Съёмка деловых событий, конференций и презентаций: зал, спикеры, гости, '
     'детали застройки. Отбор и цветокор отдаём в течение нескольких дней.'),
    ('Портрет и команда',
     'Бизнес-портрет руководителя, портреты команды и съёмка для годового '
     'отчёта: единый свет и фон на всю серию, чтобы портреты стояли рядом.'),
]

# ─── как сдаём ──────────────────────────────────────────────────────────────
DELIVERY = [
    ('Исходники', 'RAW со съёмки, мастер-файлы 5760×3240 и выше. Кадрируются '
     'без потери качества под разворот каталога.'),
    ('Вырезанный фон', 'У отдельных позиций фон вырезается по контуру, а не '
     'прямоугольником: вместе с контуром вырезается перфорация, прорези и '
     'просветы. Сдаём с альфа-каналом.'),
    ('Кадрирование', 'Каждый кадр снимается с запасом под квадрат 1:1 и '
     'вертикаль 4:5, чтобы одна съёмка закрывала каталог, сайт и маркетплейс '
     'без пересъёмки.'),
    ('Именование', 'Файлы называем по вашим артикулам и складываем в структуру '
     'папок заказчика. Каталог собирается из пакета без ручного разбора.'),
    ('Обработка', 'Общая цветокоррекция по всей серии, ретушь дефектов, '
     'согласование по контрольным кадрам до того, как в обработку уйдёт вся партия.'),
    ('Форматы сдачи', 'PNG и TIFF с прозрачностью, JPEG и WebP под веб, '
     'подготовка макетов под печать вместе с нашей типографской группой.'),
]

# ─── витрина ────────────────────────────────────────────────────────────────
# (url, клиент, что снимали, круглая обложка, обложка при наведении)
CASES = [
    ('/photo/saint-gobain', 'Saint-Gobain', 'Предметная съёмка продукции Gyproc',
     '/images/lib/custom-sgphoto/cover-main.png',
     '/images/lib/custom-sgphoto/cover-hover.png'),
    ('/portfolio/ceramicanova', 'CeramicaNova', 'Студийная съёмка санфарфора',
     '/images/lib/custom-ceramicanova/cover-main.png',
     '/images/lib/custom-ceramicanova/cover-hover.png'),
    ('/portfolio/obo-academy', 'OBO Bettermann', 'Съёмка продукции в Академии OBO',
     '/images/lib/custom-obo-academy/cover-main.png',
     '/images/lib/custom-obo-academy/cover-hover.png'),
    ('/video/lingerie', 'Lingerie Show-Forum', 'Подиум и лукбук на 54 выхода',
     '/images/lib/as3439-3739-4562-a533-616631333163/__-37.png',
     '/images/lib/as6538-3664-4239-b165-373961323065/__-36.png'),
    ('/event/marieclaire', 'Marie Claire', 'Репортаж с кросс-мероприятий',
     '/images/lib/as3731-3666-4163-a661-383336646133/__-13.png',
     '/images/lib/as3631-3366-4331-b933-653734353566/__-14.png'),
    ('/event/mozaika', 'ТРЦ «Мозаика»', 'Репортаж с вечера открытия',
     '/images/lib/as6263-3532-4466-b765-323663363739/__-28.png',
     '/images/lib/as6662-3466-4461-a163-356635363933/__-29.png'),
    ('/event/riviera', 'ТРЦ «Ривьера»', 'Съёмка застройки и вечера',
     '/images/lib/as3062-3363-4134-b333-623232303134/__-22.png',
     '/images/lib/as3962-3736-4130-b434-343833336331/__-23.png'),
    ('/creative/becar/ramada', 'Becar', 'Съёмка для брошюры Ramada Encore',
     '/images/lib/as6534-3037-4839-a432-383536343433/__-56.png',
     '/images/lib/as6561-3234-4363-b930-306439303437/__-57.png'),
]

FAQ = [
    ('Сколько стоит предметная съёмка?',
     'Считаем по числу позиций и ракурсов, а не по часам. В смете отдельно стоят '
     'съёмочный день, обработка и вырезание фона, потому что объём ретуши на '
     'технических изделиях с перфорацией и на гладкой упаковке отличается в разы. '
     'После списка позиций даём смету бесплатно.'),
    ('Сколько позиций можно снять за один день?',
     'На съёмке продукции Gyproc для Saint-Gobain за одну смену прошло 63 позиции: '
     'отдельные изделия и собранные из них системы. Это рабочий ориентир для '
     'технических изделий, когда заказчик заранее собрал продукцию на площадке.'),
    ('Вы вырезаете фон у товаров?',
     'Да, и вырезаем по контуру, а не прямоугольником. В кейсе Saint-Gobain вместе '
     'с контуром вырезано 615 сквозных отверстий: перфорация подвесов и прорези '
     'профиля. Файлы отдаются с прозрачностью, их можно класть на любой фон.'),
    ('Подойдут ли фото для маркетплейсов и печатного каталога сразу?',
     'Да, если требования собраны в бриф до съёмки. Мы снимаем с запасом под '
     'квадратное и вертикальное кадрирование, поэтому одна съёмка закрывает '
     'печатный каталог, карточку на сайте и площадки без пересъёмки.'),
    ('Снимаете ли вы на территории заказчика?',
     'Да. Чаще всего так и снимаем оборудование: студию разворачиваем на площадке '
     'заказчика, где лежит продукция и есть специалист, который соберёт систему '
     'в кадре. Выезжаем по Москве и в регионы.'),
]

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px;" alt="" /></div></noscript>'
           '<!-- /Yandex.Metrika counter -->')

LD = ('<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "Service",
    "name": "Фотопродакшн: предметная и каталожная съёмка",
    "serviceType": "Предметная съёмка товаров и оборудования",
    "provider": {"@type": "Organization", "name": "Hand Marketing",
                 "url": "https://hand-marketing.ru/"},
    "areaServed": {"@type": "Country", "name": "Россия"},
    "url": URL,
}, ensure_ascii=False) + '</script>'
      + '<script type="application/ld+json">' + json.dumps({
          "@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}}
                         for q, a in FAQ]}, ensure_ascii=False) + '</script>')

CSS = """<style id="ph-css">
.ph{--ink:#16191C;--paper:#fff;--mist:#F2F4F6;--line:rgba(22,25,28,.12);
 --blue:#4CA4E8;--deep:#3B729D;
 font-family:'Spectral',Georgia,serif;color:var(--ink);background:var(--paper);
 -webkit-font-smoothing:antialiased}
.ph *{box-sizing:border-box}
.ph h1,.ph h2,.ph h3,.ph .ui{font-family:'Exo 2','Montserrat',-apple-system,Arial,sans-serif}
.ph :focus-visible{outline:3px solid var(--deep);outline-offset:3px;border-radius:3px}
.ph__wrap{max-width:1240px;margin:0 auto;padding:0 40px}
.ph__sec{padding:84px 0;border-top:1px solid var(--line)}
.ph__kicker{font-family:'Exo 2',sans-serif;font-size:12px;font-weight:700;letter-spacing:.16em;
 text-transform:uppercase;color:var(--deep);margin:0 0 14px}
.ph__h{font-size:clamp(26px,3.2vw,40px);font-weight:700;letter-spacing:-.02em;line-height:1.12;margin:0 0 16px}
.ph__lead{font-size:clamp(16px,1.5vw,19px);line-height:1.65;max-width:66ch;margin:0}

/* герой */
.ph-hero{padding:60px 0 76px;border-top:0}
.ph-hero__g{display:grid;grid-template-columns:1.08fr .92fr;gap:46px;align-items:center}
.ph-hero h1{font-size:clamp(30px,4.4vw,56px);font-weight:800;line-height:1.04;letter-spacing:-.03em;margin:0 0 20px}
.ph-hero h1 em{font-style:normal;color:var(--deep)}
.ph-hero__st{border:1px solid var(--line);border-radius:20px;background:var(--mist);
 display:flex;align-items:center;justify-content:center;padding:30px;min-height:330px}
.ph-hero__st img{max-width:100%;max-height:400px;width:auto;height:auto;display:block}
.ph-cta{display:inline-block;margin-top:26px;font-family:'Exo 2',sans-serif;font-size:15px;font-weight:700;
 text-decoration:none;padding:14px 28px;border-radius:999px;background:var(--ink);color:#fff}
.ph-cta:hover{background:var(--deep)}
.ph-cta_g{background:transparent;color:var(--ink);border:1px solid var(--ink);margin-left:10px}
.ph-cta_g:hover{background:var(--ink);color:#fff}

/* сетки */
.ph-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:34px}
.ph-card{border:1px solid var(--line);border-radius:16px;padding:24px 24px 22px;background:#fff}
.ph-card h3{font-size:19px;font-weight:700;margin:0 0 10px}
.ph-card p{font-size:15.5px;line-height:1.62;margin:0;color:#3D444A}
.ph-del{display:grid;grid-template-columns:repeat(2,1fr);gap:0 40px;margin-top:30px}
.ph-del__i{display:grid;grid-template-columns:190px 1fr;gap:18px;padding:20px 0;border-top:1px solid var(--line)}
.ph-del__t{font-family:'Exo 2',sans-serif;font-size:15px;font-weight:700}
.ph-del__d{font-size:15.5px;line-height:1.6;color:#3D444A}

/* врезка кейса */
.ph-hl{margin-top:34px;border-radius:20px;overflow:hidden;border:1px solid var(--line);
 display:grid;grid-template-columns:1.02fr .98fr}
.ph-hl__t{padding:38px 40px}
.ph-hl__t h3{font-size:clamp(21px,2.4vw,29px);font-weight:700;line-height:1.15;margin:0 0 14px}
.ph-hl__t p{font-size:16px;line-height:1.65;color:#3D444A;margin:0 0 18px}
.ph-hl__n{display:flex;flex-wrap:wrap;gap:26px;margin:0 0 22px;padding:0;list-style:none}
.ph-hl__n b{font-family:'Exo 2',sans-serif;display:block;font-size:30px;font-weight:800;line-height:1}
.ph-hl__n span{font-family:'Exo 2',sans-serif;font-size:13px;color:#6B7178}
.ph-hl__i{background:var(--mist);display:flex;align-items:center;justify-content:center;padding:26px}
.ph-hl__i img{max-width:100%;max-height:330px;width:auto;display:block}

/* витрина */
.ph-cases{display:grid;grid-template-columns:repeat(4,1fr);gap:34px;margin-top:34px}
.ph-case{text-decoration:none;color:inherit;display:block}
/* круг нарисован внутри самой обложки (PNG с прозрачными углами), а при
   наведении вторая обложка — цветной КВАДРАТ. Поэтому контейнер не режем
   ни маской, ни border-radius: иначе квадрат обрезается в круг. */
.ph-case__p{display:block;position:relative;aspect-ratio:1/1}
.ph-case__p img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;transition:opacity .25s}
.ph-case__p img+img{opacity:0}
.ph-case:hover .ph-case__p img+img{opacity:1}
.ph-case__c{display:block;font-family:'Exo 2',sans-serif;font-size:16px;font-weight:700;margin:14px 0 4px}
.ph-case__w{display:block;font-size:14.5px;line-height:1.5;color:#6B7178;margin:0}

/* faq */
.ph-faq{margin-top:30px;border-top:1px solid var(--line)}
.ph-faq details{border-bottom:1px solid var(--line)}
.ph-faq summary{font-family:'Exo 2',sans-serif;font-size:17px;font-weight:600;padding:20px 40px 20px 0;
 cursor:pointer;position:relative;list-style:none}
.ph-faq summary::-webkit-details-marker{display:none}
.ph-faq summary::after{content:"+";position:absolute;right:6px;top:18px;font-size:24px;color:var(--deep)}
.ph-faq details[open] summary::after{content:"–"}
.ph-faq p{font-size:15.5px;line-height:1.68;color:#3D444A;margin:0 0 22px;max-width:82ch}

@media(max-width:1080px){
 .ph__wrap{padding:0 28px}
 .ph-hero__g,.ph-hl{grid-template-columns:1fr}
 .ph-grid{grid-template-columns:repeat(2,1fr)}
 .ph-cases{grid-template-columns:repeat(3,1fr);gap:26px}
 .ph-del{grid-template-columns:1fr;gap:0}
}
@media(max-width:880px){
 .ph__sec{padding:56px 0}
 .ph-hl__t{padding:28px 24px}
}
@media(max-width:640px){
 .ph__wrap{padding:0 18px}
 .ph-grid{grid-template-columns:1fr}
 .ph-cases{grid-template-columns:1fr 1fr;gap:20px}
 .ph-del__i{grid-template-columns:1fr;gap:6px}
 .ph-cta_g{margin-left:0;margin-top:10px}
 .ph-hero__st{min-height:220px;padding:18px}
}
@media(max-height:520px) and (orientation:landscape){
 .ph__sec{padding:40px 0}
 .ph-cases{grid-template-columns:repeat(4,1fr)}
}
</style>"""


def hero():
    return f'''<header class="ph__sec ph-hero"><div class="ph__wrap"><div class="ph-hero__g">
<div>
 <p class="ph__kicker">Фотопродакшн Hand Marketing</p>
 <h1>Предметная съёмка товаров и <em>оборудования</em></h1>
 <p class="ph__lead">Снимаем продукцию для печатных каталогов, сайтов, маркетплейсов
  и POS-материалов. Работаем не кадрами, а линейками: единая геометрия по всем
  артикулам, вырезанный по контуру фон, кадрирование с запасом под квадратную
  карточку. Выезжаем на производство и объекты, где стоит оборудование.</p>
 <a class="ph-cta" href="#lead">Обсудить съёмку</a>
 <a class="ph-cta ph-cta_g" href="/photo/saint-gobain">Разбор съёмки для Saint-Gobain</a>
</div>
<figure class="ph-hero__st" style="margin:0">
 <img src="/images/sgphoto/item-2140.webp" width="900" height="700"
  alt="Предметная съёмка комплектующих: подвес с вырезанным по контуру фоном" fetchpriority="high">
</figure>
</div></div></header>'''


def kinds():
    cards = ''.join(f'<article class="ph-card"><h3>{H.escape(t)}</h3><p>{H.escape(d)}</p></article>'
                    for t, d in KINDS)
    return f'''<section class="ph__sec"><div class="ph__wrap">
<p class="ph__kicker">Что снимаем</p>
<h2 class="ph__h">Шесть форматов съёмки</h2>
<p class="ph__lead">Чаще всего заказывают первые три: каталог продукции, съёмку
 оборудования на объекте и продукт внутри системы.</p>
<div class="ph-grid">{cards}</div>
</div></section>'''


def delivery():
    items = ''.join(f'<div class="ph-del__i"><div class="ph-del__t">{H.escape(t)}</div>'
                    f'<div class="ph-del__d">{H.escape(d)}</div></div>' for t, d in DELIVERY)
    return f'''<section class="ph__sec"><div class="ph__wrap">
<p class="ph__kicker">Как сдаём</p>
<h2 class="ph__h">Условия сдачи файлов</h2>
<p class="ph__lead">Съёмка каталога заканчивается не карточкой в портфолио,
 а пакетом файлов, который без ручной доработки уходит в вёрстку и на сайт.
 Вот из чего он состоит.</p>
<div class="ph-del">{items}</div>
</div></section>'''


def highlight():
    return f'''<section class="ph__sec"><div class="ph__wrap">
<p class="ph__kicker">Опорный кейс</p>
<h2 class="ph__h">Съёмка продукции Gyproc для Saint-Gobain</h2>
<div class="ph-hl">
 <div class="ph-hl__t">
  <h3>63 позиции за один съёмочный день</h3>
  <ul class="ph-hl__n">
   <li><b>{SG['shots']}</b><span>кадра в сдаче</span></li>
   <li><b>{SG['holes']}</b><span>отверстий вырезано</span></li>
   <li><b>1</b><span>съёмочный день</span></li>
  </ul>
  <p>Комплектующие для гипсокартонных систем: подвесы, соединители, ленты, крепёж
   и профили, а следом собранные из них потолок и перегородка. Сдача шла сразу
   в три канала: печатные каталоги, сайт компании и POS-материалы.</p>
  <p>На странице кейса лист сдачи можно переключить в квадрат и посмотреть, что
   останется в кадрировании у каждого файла, а подложку сменить на шахматку и
   увидеть границу выреза.</p>
  <a class="ph-cta" href="/photo/saint-gobain">Открыть разбор кейса</a>
 </div>
 <div class="ph-hl__i"><img src="/images/sgphoto/item-2105.webp" width="900" height="600"
  loading="lazy" alt="Соединитель «краб» Gyproc, предметная съёмка с вырезанным фоном"></div>
</div>
</div></section>'''


def cases():
    tiles = ''
    for url, client, what, img, hov in CASES:
        tiles += (f'<a class="ph-case" href="{url}">'
                  f'<span class="ph-case__p"><img src="{img}" alt="{H.escape(client)}" loading="lazy">'
                  f'<img src="{hov}" alt="" aria-hidden="true" loading="lazy"></span>'
                  f'<span class="ph-case__c">{H.escape(client)}</span>'
                  f'<span class="ph-case__w">{H.escape(what)}</span></a>')
    return f'''<section class="ph__sec"><div class="ph__wrap">
<p class="ph__kicker">Проекты</p>
<h2 class="ph__h">Съёмки, которые делали сами</h2>
<p class="ph__lead">Под каждой карточкой написано, что именно снимали: предметную
 продукцию, подиум, репортаж или съёмку на объекте.</p>
<div class="ph-cases">{tiles}</div>
</div></section>'''


def faq():
    items = ''.join(f'<details><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                    for q, a in FAQ)
    return f'''<section class="ph__sec"><div class="ph__wrap">
<p class="ph__kicker">Вопросы</p>
<h2 class="ph__h">Что спрашивают до съёмки</h2>
<div class="ph-faq">{items}</div>
</div></section>'''


HEAD = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<!--custom-page-->'
        f'<title>{TITLE}</title>'
        f'<meta name="description" content="{DESCR}">'
        f'<link rel="canonical" href="{URL}">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{TITLE}">'
        f'<meta property="og:description" content="{DESCR}">'
        f'<meta property="og:url" content="{URL}">'
        '<meta property="og:image" content="https://hand-marketing.ru/images/sgphoto/backstage-setup.jpg">'
        '<link rel="stylesheet" href="/fonts/exo2-spectral.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    body = (f'{rc.header()}<main class="ph">{hero()}{kinds()}{delivery()}'
            f'{highlight()}{cases()}{faq()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'photo')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('written', p, os.path.getsize(p) // 1024, 'KB')
