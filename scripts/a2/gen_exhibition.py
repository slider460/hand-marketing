#!/usr/bin/env python3
"""Генерит mirror/exhibition/index.html — страницу услуги «Exhibition Build»
(застройка выставочных стендов). Светлая страница в стиле остальных услуг сайта:
огромный H1 слева, справа — «чертёж» стенда (арка на изометрической сетке с выносками,
анимация посборочного монтажа), процесс 5 шагов, компактные кейсы в масштабе родного стора,
фиолетовая форма + тёмный футер из react-chrome.py.
build_v1 её пропускает по маркеру <!--custom-page-->. Деплой CI не трогает (нет index-a2.html)."""
import os, importlib.util, html as H

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,'..','..','mirror'))

# подключаем chrome (header/footer/CSS/JS/FONT) из react-chrome.py
spec=importlib.util.spec_from_file_location("rc", os.path.join(HERE,"react-chrome.py"))
rc=importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

CASES=[
 ("/portfolio/samara-stand-vdnh","Стенд Самарской области","Выставка-форум «Россия», ВДНХ","/images/lib/custom-samara-vdnh/cover-main.png"),
 ("/portfolio/stavropol-stand-vdnh","Стенд Ставропольского края","Выставка-форум «Россия», ВДНХ","/images/lib/custom-stavropol-vdnh/cover-main.png"),
 ("/portfolio/samara-exhibition","Выставка «Самара»","Музей им. Алабина","/images/lib/custom-samara-exhibition/cover-main.png"),
 ("/eaton_online","Виртуальный стенд Eaton","Онлайн-трансляция выставки","/images/lib/as6438-6362-4632-b262-313335333833/image_2021-03-06_22-.png"),
]
STEPS=[
 ("Дизайн и 3D-визуализация","Концепция, зонирование и фотореалистичная визуализация будущего стенда"),
 ("Конструктив и инженерия","Проектирование каркаса, расчёт нагрузок, свет и инженерные системы"),
 ("Производство","Собственная и партнёрская база — печать, дерево, металл, пластик, акрил"),
 ("Мультимедиа и интерактив","LED-экраны, проекции, сенсорные панели, AR/VR и 3D-маппинг"),
 ("Логистика и монтаж","Доставка, монтаж и демонтаж на площадке в любом городе России"),
]

METRIKA='<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

PAGE_CSS="""<style id="ex-css">
body{margin:0}
/* Шапка — точная реплика Tilda-шапки сайта (rec237851314, координаты сняты с движка):
   высота 140, сетка 1200/960, тексты Raleway 700 20px #000, лого 90px по центру окна,
   телефон 20px + почта 14px правым краем по одной кромке, НЕ sticky.
   Только десктоп ≥861px — мобильная компакт-шапка хрома остаётся как есть. */
@media(min-width:861px){
 .hm-hdr{position:relative;display:block;height:140px;border-bottom:0;padding:0;background:#fff}
 .hm-hdr__nav,.hm-hdr__contacts{display:contents}
 .hm-hdr a{position:absolute;top:50px;width:100px;font-family:'Raleway',Arial,sans-serif;
  font-size:20px;font-weight:700;line-height:.95;color:#000;white-space:nowrap;transition:opacity .15s}
 .hm-hdr a:hover{opacity:.6}
 .hm-hdr__contacts .ph{width:160px;text-align:right;font-size:20px;color:#000}
 .hm-hdr__contacts .em{top:75px;width:260px;text-align:right;font-size:14px;color:#000}
 .hm-hdr a.hm-hdr__logo{width:90px;top:30px;left:calc(50% - 45px)}
 .hm-hdr a.hm-hdr__logo img{width:90px;height:auto;display:block}}
@media(min-width:1200px){
 .hm-hdr a[href="/about"]{left:calc(50% - 600px + 24px)}
 .hm-hdr a[href="/service"]{left:calc(50% - 600px + 180px)}
 .hm-hdr a[href="/project"]{left:calc(50% - 600px + 324px)}
 .hm-hdr a[href="/clients"]{right:calc(50% - 600px + 372px)}
 .hm-hdr a[href="/contacts"]{right:calc(50% - 600px + 216px)}
 .hm-hdr__contacts .ph,.hm-hdr__contacts .em{right:calc(50% - 600px + 24px)}}
@media(min-width:960px) and (max-width:1199px){
 .hm-hdr a[href="/about"]{left:calc(50% - 480px + 19px)}
 .hm-hdr a[href="/service"]{left:calc(50% - 480px + 144px)}
 .hm-hdr a[href="/project"]{left:calc(50% - 480px + 259px)}
 .hm-hdr a[href="/clients"]{right:calc(50% - 480px + 298px)}
 .hm-hdr a[href="/contacts"]{right:calc(50% - 480px + 173px)}
 .hm-hdr__contacts .ph,.hm-hdr__contacts .em{right:calc(50% - 480px + 19px)}}
@media(min-width:861px) and (max-width:959px){
 .hm-hdr a[href="/about"]{left:2%}
 .hm-hdr a[href="/service"]{left:15%}
 .hm-hdr a[href="/project"]{left:27%}
 .hm-hdr a[href="/clients"]{right:31%}
 .hm-hdr a[href="/contacts"]{right:18%}
 .hm-hdr__contacts .ph,.hm-hdr__contacts .em{right:2%}}
.ex-main{font-family:'Montserrat',-apple-system,Arial,sans-serif;color:#14171C}
.ex-main a:focus-visible,.ex-main button:focus-visible{outline:3px solid #673A7E;outline-offset:3px;border-radius:4px}
/* ------- герой: чертёж стенда ------- */
.ex-hero{position:relative;background:#fff;overflow:hidden}
.ex-hero__in{position:relative;max-width:1180px;margin:0 auto;padding:64px 40px 72px;display:grid;grid-template-columns:1.05fr .95fr;gap:32px;align-items:center}
.ex-hero__blueprint{position:absolute;inset:0;left:42%;
 background:
  repeating-linear-gradient(60deg,rgba(20,23,28,.05) 0 1px,transparent 1px 34px),
  repeating-linear-gradient(-60deg,rgba(20,23,28,.05) 0 1px,transparent 1px 34px),
  repeating-linear-gradient(0deg,rgba(20,23,28,.035) 0 1px,transparent 1px 34px);
 -webkit-mask-image:radial-gradient(75% 85% at 60% 50%,#000 55%,transparent 100%);
 mask-image:radial-gradient(75% 85% at 60% 50%,#000 55%,transparent 100%)}
.ex-eyebrow{margin:0 0 18px;font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#673A7E}
.ex-hero h1{margin:0;font-size:clamp(44px,6.6vw,88px);line-height:.98;font-weight:800;letter-spacing:-.025em}
.ex-hero__sub{margin:20px 0 0;font-size:clamp(18px,2vw,24px);font-weight:700}
.ex-hero__lead{margin:18px 0 0;max-width:520px;font-size:17px;line-height:1.65;color:#5A616A}
.ex-hero__act{margin-top:34px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.ex-cta{display:inline-block;background:#FCB724;color:#14171C;font-weight:800;font-size:16px;text-decoration:none;padding:16px 42px;border-radius:30px;transition:transform .15s,box-shadow .15s}
.ex-cta:hover{transform:translateY(-2px);box-shadow:0 14px 26px -14px rgba(252,183,36,.9)}
.ex-cta_ghost{background:transparent;box-shadow:inset 0 0 0 2px rgba(20,23,28,.16);font-weight:700}
.ex-cta_ghost:hover{box-shadow:inset 0 0 0 2px #673A7E}
/* чертёж (SVG): сборка арки + выноски */
.ex-draft{position:relative;width:100%;max-width:560px;margin:0 auto;display:block}
.ex-part{opacity:0;transform:translateY(14px);animation:exUp .55s cubic-bezier(.2,.7,.2,1) forwards}
.ex-part_1{animation-delay:.15s}.ex-part_2{animation-delay:.3s}.ex-part_3{animation-delay:.45s}.ex-part_4{animation-delay:.62s}.ex-part_5{animation-delay:.8s}
@keyframes exUp{to{opacity:1;transform:none}}
.ex-note{font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;fill:#673A7E;opacity:0;animation:exIn .5s ease forwards 1s}
@keyframes exIn{to{opacity:1}}
.ex-dim{stroke:#673A7E;stroke-width:1;opacity:0;animation:exIn .5s ease forwards 1s}
@media (prefers-reduced-motion:reduce){
 .ex-part,.ex-note,.ex-dim{animation:none;opacity:1;transform:none}
 .ex-rev{transition:none!important;opacity:1!important;transform:none!important}}
/* ------- секции ------- */
.ex-sec{max-width:1180px;margin:0 auto;padding:76px 40px}
.ex-sec__head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;margin-bottom:40px}
.ex-sec__h{font-size:clamp(26px,3vw,38px);font-weight:800;letter-spacing:-.02em;margin:0}
.ex-all{font-weight:700;font-size:15px;color:#673A7E;text-decoration:none;white-space:nowrap}
.ex-all:hover{text-decoration:underline}
/* появление при скролле — как плитки услуг */
.ex-rev{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1)}
.ex-rev.is-in{opacity:1;transform:none}
/* процесс: монтажная направляющая */
.ex-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:26px;position:relative;counter-reset:exstep}
.ex-steps::before{content:"";position:absolute;left:24px;right:24px;top:23px;height:2px;background:linear-gradient(90deg,#673A7E 0%,rgba(103,58,126,.15) 100%)}
.ex-step{position:relative;counter-increment:exstep}
.ex-step__n{position:relative;z-index:1;display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:50%;background:#673A7E;color:#fff;font-weight:800;font-size:15px;margin-bottom:18px;box-shadow:0 0 0 6px #fff}
.ex-step__n::before{content:"0" counter(exstep)}
.ex-step h3{margin:0 0 8px;font-size:17px;font-weight:700;line-height:1.3}
.ex-step p{margin:0;font-size:14px;line-height:1.55;color:#5A616A}
.ex-steps__note{margin:44px 0 0;text-align:center;font-size:16px;color:#5A616A}
.ex-steps__note b{color:#14171C}
/* кейсы: масштаб родного стора (~295px), фото без апскейла */
.ex-cases-wrap{background:#F5F5F7}
.ex-cases{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.ex-card{display:block;text-decoration:none;color:inherit;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 8px 22px -16px rgba(0,0,0,.25);transition:transform .2s,box-shadow .2s}
.ex-card:hover{transform:translateY(-4px);box-shadow:0 22px 38px -22px rgba(0,0,0,.32)}
.ex-card__img{position:relative;aspect-ratio:477/396;overflow:hidden;background:#e9ebee}
.ex-card__img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .35s}
.ex-card:hover .ex-card__img img{transform:scale(1.05)}
.ex-card__cat{position:absolute;left:12px;top:12px;background:#673A7E;color:#fff;font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:11px;letter-spacing:.06em;padding:5px 10px;border-radius:999px}
.ex-card__b{padding:16px 18px 20px}
.ex-card__t{font-size:16px;font-weight:800;letter-spacing:-.01em;margin:0 0 5px;line-height:1.3}
.ex-card__d{font-size:13.5px;color:#5A616A;margin:0}
/* ------- адаптив ------- */
@media(max-width:1020px){
 .ex-hero__in{grid-template-columns:1fr;padding:48px 24px 56px}
 .ex-hero__blueprint{left:0;top:46%}
 .ex-draft{max-width:440px;margin-top:10px}
 .ex-steps{grid-template-columns:1fr 1fr;gap:30px 26px}
 .ex-steps::before{display:none}
 .ex-cases{grid-template-columns:1fr 1fr}
 .ex-sec{padding:56px 24px}}
@media(max-width:560px){
 .ex-hero__in{padding:36px 16px 44px}
 .ex-hero__lead{font-size:15.5px}
 .ex-cta{padding:14px 32px;font-size:15px}
 .ex-sec{padding:44px 16px}
 .ex-sec__head{margin-bottom:24px}
 .ex-steps{grid-template-columns:1fr;gap:22px}
 .ex-step__n{margin-bottom:10px}
 .ex-steps__note{margin-top:28px;text-align:left}
 /* кейсы — горизонтальный свайп, как родная мобильная карусель */
 .ex-cases{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:8px;margin:0 -16px;padding-left:16px;padding-right:16px;-webkit-overflow-scrolling:touch}
 .ex-card{flex:0 0 78%;scroll-snap-align:start}}
</style>"""

# арка exhibition-build крупно на изометрической сетке + размерная линия снизу.
# Геометрия арки — из mirror/images/services/exhibition-build.svg (viewBox 110 40 204 220).
DRAFT_SVG="""<svg class="ex-draft" viewBox="0 0 560 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Выставочный стенд-арка: от идеи до монтажа — под ключ">
<defs>
 <linearGradient id="exf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E5FB0"/><stop offset="1" stop-color="#5A3473"/></linearGradient>
 <linearGradient id="ext" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#BD96D8"/><stop offset="1" stop-color="#9A6CBE"/></linearGradient>
 <linearGradient id="exs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A3473"/><stop offset="1" stop-color="#3E2553"/></linearGradient>
</defs>
<g transform="translate(126,26) scale(1.55)">
 <g class="ex-part ex-part_1"><polygon points="270,70 270,250 304,230 304,50" fill="url(#exs)" transform="translate(-110,-40)"/></g>
 <g class="ex-part ex-part_2"><polygon points="230,110 230,250 264,230 264,90" fill="#4A2A5E" transform="translate(-110,-40)"/><polygon points="160,110 230,110 264,90 194,90" fill="#7B4E9E" transform="translate(-110,-40)"/></g>
 <g class="ex-part ex-part_3"><path d="M120,250 L120,70 L270,70 L270,250 L230,250 L230,110 L160,110 L160,250 Z" fill="url(#exf)" transform="translate(-110,-40)"/></g>
 <g class="ex-part ex-part_4"><polygon points="120,70 270,70 304,50 154,50" fill="url(#ext)" transform="translate(-110,-40)"/></g>
 <g class="ex-part ex-part_5"><polygon points="176,96 214,96 214,82 176,82" fill="#FFE000" transform="translate(-110,-40)"/><polygon points="214,96 214,82 226,75 226,89" fill="#E6C800" transform="translate(-110,-40)"/></g>
</g>
<!-- размерная линия -->
<g class="ex-dim"><line x1="142" y1="372" x2="374" y2="372"/><line x1="142" y1="364" x2="142" y2="380"/><line x1="374" y1="364" x2="374" y2="380"/></g>
<text class="ex-note" x="120" y="398">От идеи до монтажа — под ключ</text>
</svg>"""

REVEAL_JS="""<noscript><style>.ex-rev{opacity:1!important;transform:none!important}</style></noscript>
<script>(function(){
var els=[].slice.call(document.querySelectorAll('.ex-rev'));
function showAll(){els.forEach(function(n){n.classList.add('is-in');});}
if(!('IntersectionObserver' in window)){showAll();return;}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
els.forEach(function(n,i){n.style.transitionDelay=Math.min(i%4*90,270)+'ms';io.observe(n);});
setTimeout(function(){els.forEach(function(n){if(!n.classList.contains('is-in'))io.unobserve(n);});},12000);
})();</script>"""

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

def steps():
    return ''.join(f'<div class="ex-step ex-rev"><span class="ex-step__n" aria-hidden="true"></span><h3>{H.escape(t)}</h3><p>{H.escape(d)}</p></div>' for t,d in STEPS)

def cases():
    out=''
    for url,t,d,img in CASES:
        out+=(f'<a class="ex-card ex-rev" href="{url}"><div class="ex-card__img">'
              f'<img src="{img}" alt="{H.escape(t)}" loading="lazy">'
              f'<span class="ex-card__cat">Exhibition Build</span></div>'
              f'<div class="ex-card__b"><div class="ex-card__t">{H.escape(t)}</div>'
              f'<div class="ex-card__d">{H.escape(d)}</div></div></a>')
    return out

def build():
    hero=(f'<section class="ex-hero"><div class="ex-hero__blueprint" aria-hidden="true"></div><div class="ex-hero__in">'
          f'<div><p class="ex-eyebrow">Услуга</p>'
          f'<h1>Exhibition<br>Build</h1>'
          f'<p class="ex-hero__sub">Застройка выставочных стендов под&nbsp;ключ</p>'
          f'<p class="ex-hero__lead">Проектируем и строим выставочные стенды любого масштаба — от концепции и дизайна до производства, мультимедиа-наполнения и монтажа на площадке в любом городе России.</p>'
          f'<div class="ex-hero__act"><a class="ex-cta" href="#lead">Обсудить проект</a>'
          f'<a class="ex-cta ex-cta_ghost" href="#ex-cases">Смотреть кейсы</a></div></div>'
          f'<div>{DRAFT_SVG}</div>'
          f'</div></section>')
    steps_sec=(f'<section class="ex-sec"><div class="ex-sec__head"><h2 class="ex-sec__h ex-rev">Как мы строим стенд</h2></div>'
          f'<div class="ex-steps">{steps()}</div>'
          f'<p class="ex-steps__note ex-rev">Один подрядчик на весь цикл: <b>сдаём готовый стенд точно в срок</b> — включая экспозиции в виртуальном формате.</p></section>')
    case_sec=(f'<div class="ex-cases-wrap" id="ex-cases"><section class="ex-sec">'
          f'<div class="ex-sec__head"><h2 class="ex-sec__h ex-rev">Кейсы</h2><a class="ex-all ex-rev" href="/project">Все проекты →</a></div>'
          f'<div class="ex-cases">{cases()}</div></section></div>')
    body=f'{rc.header()}<main class="ex-main">{hero}{steps_sec}{case_sec}</main><a id="lead"></a>{rc.footer()}{rc.JS}{REVEAL_JS}</body></html>'
    return HEAD+body

if __name__=='__main__':
    out=os.path.join(ROOT,'exhibition'); os.makedirs(out,exist_ok=True)
    open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(build())
    print("создано: mirror/exhibition/index.html")
