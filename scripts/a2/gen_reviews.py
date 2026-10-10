#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/reviews/index.html: страница «Отзывы клиентов».

Зачем отдельная страница: одиннадцать благодарственных писем лежали в попапе на
/about (запись rec248612564), где их не видит ни посетитель, ни поисковик. Отзывы
на странице услуги закрывают коммерческий фактор, а отдельная страница собирает
все письма в одном адресе и работает узлом перелинковки.

Сканы сопоставлены с цитатами вручную 19.09.2026 по шапкам и подписям писем:
Becar различаются по дате (27.12.2019 и 25.12.2018), Eaton по подписи
(директор по маркетингу и специалист по маркетинговым коммуникациям, 14.07.2016).

Разметку Review намеренно не ставим: отзывы о себе на своём сайте поисковики
звёздами не показывают, а разметку считают попыткой накрутки (см. commerce_block).

Правки: ТОЛЬКО через этот скрипт.
Прогон: python3 scripts/a2/finalize_page.py gen_reviews.py
"""
import html as H
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
sys.path.insert(0, HERE)
import hm_ds as ds  # noqa: E402

spec = importlib.util.spec_from_file_location('rc', os.path.join(HERE, 'react-chrome.py'))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

REVIEWS = json.load(open(os.path.join(HERE, 'reviews.json'), encoding='utf-8'))
URL = 'https://hand-marketing.ru/reviews/'

# ключ отзыва -> (скан письма, год, направление работы)
SCANS = {
    'laut': ('/images/lib/as6331-6164-4934-b839-303939343038/-01.jpg', '2018', 'Мероприятие'),
    'messe': ('/images/lib/as3766-6665-4430-b638-313233313964/-02.jpg', '', 'Мероприятие'),
    'rzd': ('/images/lib/as6566-3935-4034-b332-346662616130/-03.jpg', '2019', 'Видео и печать'),
    'becar_2019': ('/images/lib/as3063-3863-4561-b837-643834373564/-04.jpg', '2019', 'Дизайн, сайты, стенды'),
    'eaton_2019': ('/images/lib/as6334-3234-4632-a230-323138316437/-05.jpg', '2019', 'Видео и мероприятия'),
    'morton': ('/images/lib/as3832-6432-4833-a637-623537633861/-06.jpg', '', 'Реклама'),
    'teoxane': ('/images/lib/as6361-6662-4432-a636-396261633062/-07.jpg', '', 'Дизайн'),
    'eaton_2016': ('/images/lib/as3737-3433-4938-a130-346363323664/-08.jpg', '2016', 'Реклама и продакшн'),
    'becar_2018': ('/images/lib/as6638-6637-4764-b463-613236316663/-09.jpg', '2018', 'Дизайн и сувениры'),
    'sg_design': ('/images/lib/as3661-6135-4566-b436-353434393862/_9324-01.jpg', '2020', 'Дизайн рекламных материалов'),
    'sg_video': ('/images/lib/as6739-3465-4238-b064-323735316130/sg-video-letter.jpg', '', 'Корпоративный фильм'),
}

# порядок на странице: сначала письма с самыми содержательными цитатами
ORDER = ['sg_video', 'messe', 'laut', 'eaton_2019', 'becar_2019', 'rzd',
         'becar_2018', 'morton', 'teoxane', 'eaton_2016', 'sg_design']

LINKS = [
    ('/videoproduction/', 'Видеопродакшн'), ('/event/', 'Мероприятия'),
    ('/exhibition/', 'Выставочные стенды'), ('/content/', 'Мультимедийный контент'),
    ('/creativedesign/', 'Креатив и дизайн'), ('/printandproduction/', 'Печать и производство'),
    ('/photo', 'Фотопродакшн'), ('/project', 'Все проекты'),
    ('/team/', 'Команда'), ('/price/', 'Цены'),
]

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px" alt=""></div></noscript>')


LIGHTBOX = """<script>(function(){
// скан письма открывается во весь экран: на телефоне мелкий текст иначе не прочитать
var box=document.createElement('div');
box.style.cssText='position:fixed;inset:0;background:rgba(14,13,17,.92);display:none;z-index:9999;'+
 'align-items:center;justify-content:center;padding:24px;cursor:zoom-out;overflow:auto';
var im=document.createElement('img');
im.style.cssText='max-width:min(980px,100%);width:auto;height:auto;border-radius:6px;background:#fff';
box.appendChild(im);document.body.appendChild(box);
function close(){box.style.display='none';im.src=''}
box.addEventListener('click',close);
document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
document.querySelectorAll('.rv-scan').forEach(function(a){
 a.addEventListener('click',function(e){e.preventDefault();
  im.src=a.getAttribute('href');im.alt=a.getAttribute('data-alt')||'';
  box.style.display='flex'})});
})();</script>"""


def esc(t):
    return H.escape(t, quote=False)


# метка направления письма: цвет по первому слову работы из SCANS
TAG_COLORS = (('Мероприятие', ds.EV), ('Видео', ds.VID), ('Корпоративный', ds.VID), ('Дизайн', ds.CRE),
              ('Реклама', ds.PRN))

CSS = """<style id="rv-css">
.rv-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.rv-item{display:grid;grid-template-columns:170px minmax(0,1fr);gap:30px;align-items:start;background:#fff;padding:30px;box-shadow:0 1px 0 #ECECEC,0 18px 40px -28px rgba(20,23,28,.35)}
.rv-scan{display:block;cursor:zoom-in}
.rv-scan img{display:block;width:100%;aspect-ratio:210/297;object-fit:cover;object-position:top;border:1px solid #ECECEC;box-shadow:0 10px 24px -10px rgba(0,0,0,.35);transform:rotate(var(--r));transition:transform .25s ease}
.rv-scan:hover img,.rv-scan:focus-visible img{transform:rotate(0) scale(1.03)}
.rv-item__cap{display:block;margin-top:14px;font-size:12px;line-height:1.45;color:#8A8A8A}
.rv-tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--c);border:1.5px solid var(--c);border-radius:999px;padding:4px 11px}
.rv-item blockquote{margin:16px 0 0;font-size:17px;line-height:1.55;font-weight:500;color:#111}
.rv-item blockquote+blockquote{margin-top:10px;font-size:15px;color:#4C4C4C}
.rv-who{margin:18px 0 0;font-size:13.5px;line-height:1.5;color:#4C4C4C}
.rv-who b{display:block;font-size:15px;color:#111}
.rv-who a{display:inline-block;margin-top:10px;font-size:13.5px;font-weight:700;color:#111;text-decoration:none;border-bottom:2px solid #FFF700}
@media(max-width:1100px){.rv-list{grid-template-columns:minmax(0,1fr)}}
@media(max-width:560px){.rv-item{grid-template-columns:minmax(0,1fr);padding:24px 20px}.rv-scan{max-width:200px}}
</style>"""


def item(key, i):
    r = REVIEWS[key]
    scan, year, work = SCANS[key]
    who = f'{esc(r["person"])}, {esc(r["role"])}'
    # у четырёх писем в reviews.json поля about нет: берём направление работы из SCANS
    about = r.get('about') or work.lower()
    color = next((c for w, c in TAG_COLORS if work.startswith(w)), ds.VIOLET)
    case = (f'<a href="{r["case"]}">Смотреть проект</a>' if r.get('case') else '')
    q2 = f'<blockquote>«{esc(r["quote2"])}»</blockquote>' if r.get('quote2') else ''
    alt = f'Благодарственное письмо: {esc(r["company"])}'
    cap = f'{work}{", " + year if year else ""}'
    tilt = ('-1.6deg', '1.2deg', '-0.8deg', '1.6deg')[i % 4]
    return (
        f'<article class="rv-item" style="--c:{color};--r:{tilt}">'
        f'<div><a class="rv-scan" href="{scan}" data-alt="{H.escape(alt)}">'
        f'<img src="{scan}" alt="{H.escape(alt)}" loading="lazy" width="420" height="594"></a>'
        f'<span class="rv-item__cap">{esc(cap)}. Нажмите, чтобы прочитать письмо целиком</span></div>'
        f'<div><span class="rv-tag">{esc(about)}</span>'
        f'<blockquote>«{esc(r["quote"])}»</blockquote>{q2}'
        f'<p class="rv-who"><b>{esc(r["company"])}</b><span>{who}</span><br>{case}</p></div>'
        f'</article>')


def page():
    items = ''.join(item(k, i) for i, k in enumerate(ORDER))
    title = 'Отзывы клиентов и благодарственные письма | Hand Marketing'
    descr = ('Благодарственные письма от клиентов агентства: Saint-Gobain, '
             'Eaton, РЖД, Messe Düsseldorf, Becar, МФК «Саларис». Сканы писем целиком '
             'и ссылки на проекты.')
    head = (
        '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{title}</title>'
        f'<meta name="description" content="{H.escape(descr)}">'
        f'<link rel="canonical" href="{URL}">'
        '<meta name="robots" content="index, follow">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{H.escape(title)}">'
        f'<meta property="og:description" content="{H.escape(descr)}">'
        f'<meta property="og:url" content="{URL}">'
        '<meta property="og:image" content="https://hand-marketing.ru/images/lib/as6739-3465-4238-b064-323735316130/sg-video-letter.jpg">'
        + rc.FONT + rc.CSS + ds.CSS + CSS + METRIKA + '</head><body>')

    crumbs_ld = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Главная', 'item': 'https://hand-marketing.ru/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Отзывы', 'item': URL}]}

    lede = ('Это письма, которые компании присылали нам после проектов. Сканы лежат целиком, без '
            'вырезанных абзацев: можно открыть любое и прочитать полностью, вместе с подписью и датой. '
            'Цитаты рядом приведены дословно.')
    hero = ds.hero('Letters', 'Об агентстве · Отзывы', 'Отзывы клиентов и благодарственные письма',
                   esc(lede), figs=2)
    crumbs = ds.crumbs([('Главная', '/'), ('Отзывы', None)])
    banner = ds.banner(None, '/videos/reviews-hero-poster.jpg', 'Кадры из проектов клиентов, приславших письма',
                       'Проекты, о которых эти письма', 'Saint-Gobain, Eaton, «Саларис», ЦМ РЖД',
                       'Кадры из фильмов и с мероприятий, после которых клиенты присылали благодарственные письма.',
                       video='/videos/reviews-hero-loop.mp4')
    letters = ds.sec(f'<div class="rv-list">{items}</div>'
                     '<p class="hd-note">Все письма опубликованы с согласия компаний. Мы не размечаем их '
                     'как отзывы для поисковика и не выводим звёзды рейтинга: оценку своей работы на своём '
                     'сайте считать объективной нельзя, а письмо с подписью и печатью говорит само за себя.</p>',
                     'Письма целиком', alt=True, icons=3)
    links = ds.sec(ds.links([('Направления', [(t, h) for h, t in LINKS[:7]]),
                             ('Об агентстве', [(t, h) for h, t in LINKS[7:]])]),
                   'Чем мы занимаемся',
                   esc('Письма выше относятся к разным направлениям: съёмке, мероприятиям, дизайну, '
                       'печати и выставочным стендам.'))
    body = (f'{rc.header()}<main class="hd" style="--a:{ds.VIOLET}">{crumbs}{hero}{banner}{letters}{links}</main>'
            f'{ds.BANNER_JS}<a id="lead"></a>{rc.footer()}{rc.JS}{LIGHTBOX}'
            f'<script type="application/ld+json">'
            f'{json.dumps(crumbs_ld, ensure_ascii=False, separators=(",", ":"))}</script>'
            '</body></html>')
    return head + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'reviews')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('создано:', p, os.path.getsize(p) // 1024, 'КБ')
