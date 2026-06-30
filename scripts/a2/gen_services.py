#!/usr/bin/env python3
"""Кастомная адаптивная сетка услуг (8 шт, Exhibition Build первой) — переиспользует
существующие 7 SVG-иконок Тильды + новую арку. Возвращает HTML+CSS секции (SERVICES_SECTION)
для встраивания в /service (и при желании на главную). Тут же — превью-страница для локального показа."""
import os, importlib.util, html as H

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,'..','..','mirror'))

# услуги: (название, ссылка, иконка, цвет-акцент, краткое описание). Exhibition Build — первая.
SERVICES=[
 ("Exhibition Build","/exhibition","/images/services/exhibition-build.svg","#673A7E","Застройка выставочных стендов под ключ"),
 ("Event","/event","/static/cdn/as3638-3032-4737-a561-386433393934/__-104.svg","#EAB400","Мероприятия под ключ: концепция, продакшн, режиссура"),
 ("Creative & Design","/creativedesign","/static/cdn/as6230-3736-4036-b166-373633323062/__-105.svg","#E8820E","Брендинг, дизайн и креативные концепции"),
 ("Video production","/videoproduction","/static/cdn/as6466-3266-4538-b932-666638343532/__-106.svg","#7DB52E","Имиджевые и рекламные ролики, съёмка и пост"),
 ("Print & Production","/printandproduction","/static/cdn/as6235-3538-4131-b365-396330653938/__-107.svg","#E5197D","Полиграфия, сувениры и производство"),
 ("BTL","/btl","/static/cdn/as3035-6338-4635-b134-343563663832/__-108.svg","#36B5E0","Промо-акции, активации, нестандартный BTL"),
 ("Digital","/digital","/static/cdn/as3837-3730-4563-b161-323535303661/__-109.svg","#E8470E","Сайты, лендинги и digital-продвижение"),
 ("3D Mapping","/3dmapping","/static/cdn/as6138-6261-4038-a434-666430383535/__-110.svg","#F2B400","Мультимедийные 3D-mapping шоу любого масштаба"),
]

CSS="""<style id="hm-svc-css">
.hm-svc{max-width:1200px;margin:0 auto;padding:64px 40px;font-family:'Montserrat',-apple-system,Arial,sans-serif}
.hm-svc__h{text-align:center;margin:0 0 8px;font-size:34px;font-weight:800;letter-spacing:-.02em;color:#14171C}
.hm-svc__sub{text-align:center;margin:0 0 44px;font-size:17px;color:#5A616A}
.hm-svc__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.hm-svc__card{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;
  text-decoration:none;color:inherit;background:#fff;border:1px solid rgba(20,23,28,.08);border-radius:20px;
  padding:34px 22px 28px;transition:transform .22s,box-shadow .22s,border-color .22s;overflow:hidden}
.hm-svc__card::after{content:"";position:absolute;left:0;right:0;bottom:0;height:4px;background:var(--c);transform:scaleX(0);transform-origin:left;transition:transform .25s}
.hm-svc__card:hover{transform:translateY(-6px);box-shadow:0 28px 50px -30px rgba(0,0,0,.28);border-color:transparent}
.hm-svc__card:hover::after{transform:scaleX(1)}
.hm-svc__ic{height:96px;display:flex;align-items:center;justify-content:center;margin-bottom:18px}
.hm-svc__ic img{height:90px;width:auto;transition:transform .25s}
.hm-svc__card:hover .hm-svc__ic img{transform:scale(1.08) translateY(-2px)}
.hm-svc__name{font-size:19px;font-weight:800;letter-spacing:-.01em;margin:0 0 8px;color:#14171C}
.hm-svc__d{font-size:14px;line-height:1.5;color:#6A7078;margin:0}
.hm-svc__card_first{border-color:rgba(103,58,126,.35);box-shadow:0 18px 40px -26px rgba(103,58,126,.45)}
.hm-svc__tag{position:absolute;top:14px;right:14px;background:#673A7E;color:#fff;font-size:11px;font-weight:700;padding:4px 10px;border-radius:999px}
@media(max-width:1080px){.hm-svc__grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:880px){.hm-svc{padding:44px 16px}.hm-svc__h{font-size:26px}.hm-svc__grid{gap:14px}}
@media(max-width:480px){.hm-svc__grid{grid-template-columns:1fr 1fr}.hm-svc__card{padding:24px 12px 20px}.hm-svc__ic img{height:68px}.hm-svc__name{font-size:16px}.hm-svc__d{display:none}}
</style>"""

def cards():
    out=''
    for i,(n,u,ic,c,d) in enumerate(SERVICES):
        first=' hm-svc__card_first' if i==0 else ''
        tag='<span class="hm-svc__tag">Новое</span>' if i==0 else ''
        out+=(f'<a class="hm-svc__card{first}" href="{u}" style="--c:{c}">{tag}'
              f'<span class="hm-svc__ic"><img src="{ic}" alt="{H.escape(n)}" loading="lazy"></span>'
              f'<h3 class="hm-svc__name">{H.escape(n)}</h3>'
              f'<p class="hm-svc__d">{H.escape(d)}</p></a>')
    return out

def section():
    return (CSS+'<section class="hm-svc"><h2 class="hm-svc__h">Услуги</h2>'
            '<p class="hm-svc__sub">Полный цикл маркетинговых коммуникаций — от идеи до реализации</p>'
            f'<div class="hm-svc__grid">{cards()}</div></section>')

if __name__=='__main__':
    # превью-страница с chrome для локального показа
    spec=importlib.util.spec_from_file_location("rc", os.path.join(HERE,"react-chrome.py"))
    rc=importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
    page=('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
          '<title>Услуги — превью</title>'+rc.FONT+rc.CSS+'<!--custom-page--></head><body>'
          +rc.header()+'<main>'+section()+'</main>'+rc.footer()+rc.JS+'</body></html>')
    out=os.path.join(ROOT,'_preview_services.html')
    open(out,'w',encoding='utf-8').write(page)
    print("превью:", out)
