#!/usr/bin/env python3
"""Генерит mirror/exhibition/index.html — страницу услуги «Exhibition Build»
(застройка выставочных стендов). Чистая адаптивная страница (десктоп+мобайл) в стиле сайта:
шапка-куб+меню, фиолетовая форма, тёмный футер (переиспользуем из react-chrome.py).
build_v1 её пропускает по маркеру <!--custom-page-->. Деплой CI не трогает (нет index-a2.html)."""
import os, importlib.util, html as H

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,'..','..','mirror'))

# подключаем chrome (header/footer/CSS/JS/FONT) из react-chrome.py
spec=importlib.util.spec_from_file_location("rc", os.path.join(HERE,"react-chrome.py"))
rc=importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

PURPLE="#673A7E"
CASES=[
 ("/portfolio/samara-stand-vdnh","Стенд Самарской области","Выставка-форум «Россия», ВДНХ","/images/lib/custom-samara-vdnh/cover-main.png"),
 ("/portfolio/stavropol-stand-vdnh","Стенд Ставропольского края","Выставка-форум «Россия», ВДНХ","/images/lib/custom-stavropol-vdnh/cover-main.png"),
 ("/portfolio/samara-exhibition","Выставка «Самара»","Музей им. Алабина","/images/lib/custom-samara-exhibition/cover-main.png"),
 ("/eaton_online","Виртуальный стенд Eaton","Онлайн-трансляция выставки","/images/lib/as6438-6362-4632-b262-313335333833/image_2021-03-06_22-.png"),
]
FEATS=[
 ("Дизайн и 3D-визуализация","Концепция, зонирование и фотореалистичная визуализация будущего стенда"),
 ("Конструктив и инженерия","Проектирование каркаса, расчёт нагрузок, свет и инженерные системы"),
 ("Производство","Собственная и партнёрская база — печать, дерево, металл, пластик, акрил"),
 ("Мультимедиа и интерактив","LED-экраны, проекции, сенсорные панели, AR/VR и 3D-маппинг"),
 ("Логистика и монтаж","Доставка, монтаж и демонтаж на площадке в любом городе России"),
 ("Под ключ","Полный цикл — от идеи до сдачи готового стенда точно в срок"),
]

METRIKA='<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

PAGE_CSS="""<style id="ex-css">
.ex-main{font-family:'Montserrat',-apple-system,Arial,sans-serif;color:#14171C}
.ex-hero{background:#14171C;color:#fff;padding:84px 40px 76px;text-align:center}
.ex-hero__in{max-width:920px;margin:0 auto}
.ex-eyebrow{margin:0 0 16px;font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#FFE000}
.ex-hero h1{margin:0;font-size:64px;line-height:1.02;font-weight:800;letter-spacing:-.02em}
.ex-hero__sub{margin:14px 0 0;font-size:24px;font-weight:700;color:#cfd2d6}
.ex-hero__lead{margin:24px auto 0;max-width:760px;font-size:18px;line-height:1.6;color:#aeb3b9}
.ex-hero__cta{display:inline-block;margin-top:32px;background:#FCB724;color:#14171C;font-weight:800;font-size:16px;text-decoration:none;padding:16px 44px;border-radius:30px;transition:transform .15s}
.ex-hero__cta:hover{transform:translateY(-2px)}
.ex-sec{max-width:1180px;margin:0 auto;padding:72px 40px}
.ex-sec__h{font-size:34px;font-weight:800;letter-spacing:-.02em;margin:0 0 36px;text-align:center}
.ex-feats{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.ex-feat{border:1px solid rgba(20,23,28,.10);border-radius:18px;padding:28px 26px;transition:box-shadow .2s,transform .2s}
.ex-feat:hover{box-shadow:0 24px 44px -28px rgba(0,0,0,.25);transform:translateY(-3px)}
.ex-feat__n{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:#673A7E;color:#fff;font-weight:800;margin-bottom:16px}
.ex-feat h3{margin:0 0 8px;font-size:19px;font-weight:700}
.ex-feat p{margin:0;font-size:15px;line-height:1.55;color:#5A616A}
.ex-cases-wrap{background:#F7F8FA}
.ex-cases{display:grid;grid-template-columns:repeat(2,1fr);gap:28px}
.ex-card{display:block;text-decoration:none;color:inherit;background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 10px 30px -20px rgba(0,0,0,.3);transition:transform .2s,box-shadow .2s}
.ex-card:hover{transform:translateY(-4px);box-shadow:0 30px 50px -28px rgba(0,0,0,.35)}
.ex-card__img{position:relative;aspect-ratio:16/10;overflow:hidden;background:#e9ebee}
.ex-card__img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.ex-card:hover .ex-card__img img{transform:scale(1.04)}
.ex-card__cat{position:absolute;left:16px;top:16px;background:#673A7E;color:#fff;font-weight:700;font-size:12px;padding:6px 12px;border-radius:999px}
.ex-card__b{padding:22px 24px 26px}
.ex-card__t{font-size:21px;font-weight:800;letter-spacing:-.01em;margin:0 0 6px}
.ex-card__d{font-size:15px;color:#5A616A;margin:0}
@media(max-width:860px){
 .ex-hero{padding:54px 18px 48px}
 .ex-hero h1{font-size:40px}.ex-hero__sub{font-size:19px}.ex-hero__lead{font-size:16px}
 .ex-sec{padding:48px 16px}.ex-sec__h{font-size:26px;margin-bottom:26px}
 .ex-feats{grid-template-columns:1fr;gap:16px}
 .ex-cases{grid-template-columns:1fr;gap:18px}
}
</style>"""

def feats():
    return ''.join(f'<div class="ex-feat"><span class="ex-feat__n">{i+1}</span><h3>{H.escape(t)}</h3><p>{H.escape(d)}</p></div>' for i,(t,d) in enumerate(FEATS))
def cases():
    out=''
    for url,t,d,img in CASES:
        out+=(f'<a class="ex-card" href="{url}"><div class="ex-card__img">'
              f'<img src="{img}" alt="{H.escape(t)}" loading="lazy">'
              f'<span class="ex-card__cat">Exhibition Build</span></div>'
              f'<div class="ex-card__b"><div class="ex-card__t">{H.escape(t)}</div>'
              f'<div class="ex-card__d">{H.escape(d)}</div></div></a>')
    return out

HEAD=f'''<!doctype html><html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Exhibition Build — застройка выставочных стендов под ключ | Hand Marketing</title>
<meta name="description" content="Проектирование и застройка выставочных стендов под ключ: дизайн, 3D-визуализация, производство, мультимедиа и монтаж. Кейсы: ВДНХ, Самара, Ставрополь, виртуальный стенд Eaton.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hand-marketing.ru/exhibition">
<meta property="og:type" content="website"><meta property="og:title" content="Exhibition Build — застройка выставочных стендов | Hand Marketing">
<meta property="og:description" content="Выставочные стенды под ключ: дизайн, производство, мультимедиа, монтаж.">
<meta property="og:url" content="https://hand-marketing.ru/exhibition">
<meta property="og:image" content="https://hand-marketing.ru/images/lib/custom-samara-vdnh/cover-main.png">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
{rc.FONT}{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''

def build():
    hero=(f'<section class="ex-hero"><div class="ex-hero__in">'
          f'<p class="ex-eyebrow">Услуга</p>'
          f'<h1>Exhibition Build</h1>'
          f'<p class="ex-hero__sub">Застройка выставочных стендов под&nbsp;ключ</p>'
          f'<p class="ex-hero__lead">Проектируем и строим выставочные стенды любого масштаба — от концепции и дизайна до производства, мультимедиа-наполнения и монтажа на площадке. Реализуем экспозиции для форумов, выставок и корпоративных мероприятий, в&nbsp;том числе в&nbsp;виртуальном формате.</p>'
          f'<a class="ex-hero__cta" href="#lead">Обсудить проект</a></div></section>')
    feat_sec=f'<section class="ex-sec"><h2 class="ex-sec__h">Что входит в&nbsp;услугу</h2><div class="ex-feats">{feats()}</div></section>'
    case_sec=f'<div class="ex-cases-wrap"><section class="ex-sec"><h2 class="ex-sec__h">Кейсы</h2><div class="ex-cases">{cases()}</div></section></div>'
    body=f'{rc.header()}<main class="ex-main">{hero}{feat_sec}{case_sec}</main><a id="lead"></a>{rc.footer()}{rc.JS}</body></html>'
    return HEAD+body

if __name__=='__main__':
    out=os.path.join(ROOT,'exhibition'); os.makedirs(out,exist_ok=True)
    open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(build())
    print("создано: mirror/exhibition/index.html")
