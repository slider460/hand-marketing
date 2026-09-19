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
]

METRIKA = ('<!-- Yandex.Metrika counter --><script type="text/javascript">'
           '(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
           'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
           'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
           '(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
           'ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});'
           '</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" '
           'style="position:absolute;left:-9999px" alt=""></div></noscript>')

CSS = """<style id="rv-css">
.rv{--ink:#14171C;--mut:#5A616A;--a:#673A7E;--line:rgba(20,23,28,.12);
 font-family:'Montserrat',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff}
.rv *{box-sizing:border-box}
.rv__wrap{max-width:1180px;margin:0 auto;padding:0 40px}
.rv-hero{padding:64px 0 40px;border-bottom:1px solid var(--line)}
.rv-hero h1{margin:0 0 16px;font-size:clamp(28px,4vw,48px);font-weight:800;letter-spacing:-.025em;line-height:1.08}
.rv-hero p{margin:0;max-width:70ch;font-size:16.5px;line-height:1.65;color:var(--mut)}
.rv-nums{display:flex;flex-wrap:wrap;gap:34px;margin-top:28px}
.rv-nums div b{display:block;font-size:30px;font-weight:800;letter-spacing:-.02em;color:var(--a)}
.rv-nums div span{font-size:13.5px;color:var(--mut)}
.rv-list{display:grid;gap:22px;padding:44px 0 10px}
.rv-item{display:grid;grid-template-columns:300px minmax(0,1fr);gap:26px;align-items:start;
 border:1px solid var(--line);border-radius:20px;padding:22px;background:#fff}
.rv-scan{display:block;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#F7F5F3}
.rv-scan img{width:100%;height:auto;display:block;transition:transform .25s}
.rv-scan:hover img{transform:scale(1.02)}
.rv-item__cap{display:block;margin-top:8px;font-size:12.5px;color:var(--mut)}
.rv-tag{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
 color:var(--a);border:1px solid rgba(103,58,126,.35);border-radius:20px;padding:5px 12px;margin-bottom:14px}
.rv-item blockquote{margin:0 0 16px;font-size:clamp(16px,1.7vw,19px);line-height:1.62;font-weight:500}
.rv-item blockquote + blockquote{font-size:15.5px;color:var(--mut);font-weight:400}
.rv-who{margin:18px 0 0;font-size:14.5px;line-height:1.6}
.rv-who b{display:block;font-size:16px}
.rv-who span{color:var(--mut)}
.rv-who a{display:inline-block;margin-top:8px;color:var(--a);font-weight:700;text-decoration:none;
 border-bottom:1px solid rgba(103,58,126,.4)}
.rv-note{margin:34px 0 0;padding:20px 22px;border-left:3px solid var(--a);background:#F8F6FA;
 font-size:14.5px;line-height:1.65;color:var(--mut);border-radius:0 12px 12px 0;max-width:80ch}
.rv-links{padding:44px 0 64px;border-top:1px solid var(--line);margin-top:40px}
.rv-links h2{margin:0 0 14px;font-size:22px;font-weight:800;letter-spacing:-.02em}
.rv-links p{margin:0 0 16px;font-size:15.5px;line-height:1.65;color:var(--mut)}
.rv-links a{display:inline-block;margin:0 14px 10px 0;font-size:15px;color:var(--ink);
 text-decoration:none;border-bottom:1px solid rgba(20,23,28,.25)}
.rv-links a:hover{color:var(--a);border-color:var(--a)}
@media(max-width:820px){.rv-item{grid-template-columns:1fr}.rv__wrap{padding:0 18px}}
</style>"""

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


def item(key):
    r = REVIEWS[key]
    scan, year, work = SCANS[key]
    who = f'{esc(r["person"])}, {esc(r["role"])}'
    # у четырёх писем в reviews.json поля about нет: берём направление работы из SCANS
    about = r.get('about') or work.lower()
    case = (f'<a href="{r["case"]}">Смотреть проект →</a>' if r.get('case') else '')
    q2 = f'<blockquote>«{esc(r["quote2"])}»</blockquote>' if r.get('quote2') else ''
    alt = f'Благодарственное письмо: {esc(r["company"])}'
    cap = f'{work}{", " + year if year else ""}'
    return (
        f'<article class="rv-item">'
        f'<div><a class="rv-scan" href="{scan}" data-alt="{H.escape(alt)}">'
        f'<img src="{scan}" alt="{H.escape(alt)}" loading="lazy"></a>'
        f'<span class="rv-item__cap">{esc(cap)}. Нажмите, чтобы прочитать письмо целиком</span></div>'
        f'<div><span class="rv-tag">{esc(about)}</span>'
        f'<blockquote>«{esc(r["quote"])}»</blockquote>{q2}'
        f'<p class="rv-who"><b>{esc(r["company"])}</b><span>{who}</span><br>{case}</p></div>'
        f'</article>')


def page():
    items = ''.join(item(k) for k in ORDER)
    links = ''.join(f'<a href="{h}">{esc(t)}</a>' for h, t in LINKS)
    title = 'Отзывы клиентов и благодарственные письма | Hand Marketing'
    descr = ('Одиннадцать благодарственных писем от клиентов агентства: Saint-Gobain, '
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
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')

    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Главная', 'item': 'https://hand-marketing.ru/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Отзывы', 'item': URL}]}

    body = (
        f'{rc.header()}<main class="rv">'
        '<section class="rv-hero"><div class="rv__wrap">'
        '<h1>Отзывы клиентов и благодарственные письма</h1>'
        '<p>Это письма, которые компании присылали нам после проектов. Сканы лежат целиком, '
        'без вырезанных абзацев: можно открыть любое и прочитать полностью, вместе с подписью '
        'и датой. Цитаты рядом приведены дословно.</p>'
        '<div class="rv-nums">'
        '<div><b>11</b><span>писем от клиентов</span></div>'
        '<div><b>7</b><span>компаний, включая Saint-Gobain, Eaton, РЖД</span></div>'
        '<div><b>с 2012</b><span>года работаем с повторными заказчиками</span></div>'
        '</div></div></section>'
        f'<div class="rv__wrap"><div class="rv-list">{items}</div>'
        '<p class="rv-note">Все письма опубликованы с согласия компаний. Мы не размечаем их '
        'как отзывы для поисковика и не выводим звёзды рейтинга: оценку своей работы на своём '
        'сайте считать объективной нельзя, а письмо с подписью и печатью говорит само за себя.</p>'
        '</div>'
        '<section class="rv-links"><div class="rv__wrap">'
        '<h2>Чем мы занимаемся</h2>'
        '<p>Письма выше относятся к разным направлениям: съёмке, мероприятиям, дизайну, '
        'печати и выставочным стендам.</p>'
        f'<div>{links}</div></div></section>'
        '</main>'
        f'<a id="lead"></a>{rc.footer()}{rc.JS}{LIGHTBOX}'
        f'<script type="application/ld+json">'
        f'{json.dumps(crumbs, ensure_ascii=False, separators=(",", ":"))}</script>'
        '</body></html>')
    return head + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'reviews')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('создано:', p, os.path.getsize(p) // 1024, 'КБ')
