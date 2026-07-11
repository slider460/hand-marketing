#!/usr/bin/env python3
"""Генерит mirror/videoproduction/index.html — страницу услуги «Video Production»
по логике weshow.su/services/video-production: hero с зацикленным лёгким видео
(/media/vp-hero-loop.mp4, ~1.9 МБ, пауза вне вьюпорта), секция «Что мы снимаем»
(виды работ с примерами-роликами по клику, фасадный паттерн — до клика грузится
только постер), кейсы в масштабе родного стора (как /exhibition, мобайл — свайп),
фиолетовая форма + тёмный футер из react-chrome.py (стандартные шапка/подвал).
Ролики примеров — self-hosted /media/*.mp4 (контент weshow); недостающие файлы
перечислены в VIDEO-UPLOAD.md (заливаются вручную).
build_v1 страницу пропускает по маркеру <!--custom-page-->.
ВНИМАНИЕ: скрипт удаляет mirror/videoproduction/index-a2.html (иначе деплой-своп
затрёт index.html старой Tilda-страницей)."""
import os, importlib.util, html as H

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,'..','..','mirror'))

# подключаем chrome (header/footer/CSS/JS/FONT) из react-chrome.py
spec=importlib.util.spec_from_file_location("rc", os.path.join(HERE,"react-chrome.py"))
rc=importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

ACCENT='#CF6F19'  # фирменный оранж Video Production

# Виды работ (контент weshow): (заголовок, описание, [(кейс, постер, видео)])
WORK_TYPES=[
 ("Рекламные ролики",
  "Создаём яркие, цепляющие и запоминающиеся рекламные видео, которые продают ваш продукт и повышают узнаваемость бренда. Фокус — на креативе, качестве исполнения и достижении KPI.",
  [("VIVAX","/images/vp/cadr_samburskaya.jpg","/media/vivax-samburskaya.mp4"),
   ("УАЗ Патриот","/images/vp/cadr_yaz.jpg","/media/eaton-yaz.mp4")]),
 ("Корпоративные фильмы",
  "Рассказываем историю вашей компании. Снимаем имиджевые и HR-фильмы, которые укрепляют репутацию, мотивируют сотрудников и производят впечатление на партнёров и инвесторов.",
  [("АО «РЖД»","/images/vp/cadr_rgd.jpg","/media/transrzhd.mp4"),
   ("Power Technology","/images/vp/cadr_power_tech.jpg","/media/pt-film-long.mp4")]),
 ("Репортажные ролики",
  "Ловим живые эмоции и ключевые моменты. Создаём динамичные репортажные видео с выставок, конференций, форумов и мероприятий, передавая атмосферу и масштаб события.",
  [("Выставка-форум «Россия»","/images/vp/cadr_samara_vdnh.jpg","/media/samara-vdnh-report.mp4"),
   ("Event ТРЦ «Саларис»","/images/vp/cadr_salaris.jpg","/media/salaris-event-fin180416.mp4"),
   ("Event ТРЦ «Ривьера»","/images/vp/cadr_riviera.jpg","/media/event-riviera.mp4")]),
 ("Вирусные ролики",
  "Разрабатываем нестандартные идеи и креативные концепции, которые выходят за рамки обычного. Наша цель — контент, который удивляет и которым хочется делиться.",
  [("Газель-трансформер","/images/vp/cadr_gazell.jpg","/media/gazelle-transformer.mp4")]),
 ("Обучающие видео",
  "Переводим сложное на простой и понятный язык. Производим структурированные обучающие материалы, видеоинструкции, HR-онбординги и курсы для сотрудников и клиентов.",
  [("Saint-Gobain","/images/vp/Cadr_SG_obushenie.jpg","/media/saint-gobain-training.mp4")]),
]

# Видеопрезентации: проект стенда Самарской области (форум «Россия — спортивная держава»)
PRESENTATIONS=[
 ("Концепция «4 стихии»","/images/vp/4-stihii_samara.jpg","/media/samara-pres-4elements.mp4"),
 ("Концепция «5 духов»","/images/vp/5-stihy_samara.jpg","/media/samara-pres-5spirits.mp4"),
 ("Визуализация стенда 1","/images/vp/vizual_1_samara.jpg","/media/samara-pres-vizual-1.mp4"),
 ("Визуализация стенда 2","/images/vp/vizual_2_samara.jpg","/media/samara-pres-vizual-2.mp4"),
 ("Концепция контента","/images/vp/content_samara.jpg","/media/samara-pres-content.mp4"),
]

# Кейсы — 1:1 плитки родного Tilda-каталога старой страницы (storepart 951929931011):
# те же 15 круглых картинок, тот же порядок; при наведении — вторая картинка галереи
# с информацией, как в родном сторе. (url, alt, картинка, hover-картинка)
CASES=[
 ("/video/patriot","УАЗ Патриот & Eaton","/images/lib/as3532-3737-4330-b333-386531636666/__-03.png","/images/lib/as6461-6261-4036-a666-313230363264/__-04.png"),
 ("/video/gaz","Газель-трансформер","/images/lib/as3233-3363-4138-b265-353738653739/__-20.png","/images/lib/as3438-6330-4463-b039-336563616535/__-21.png"),
 ("/video/rgd/history","РЖД","/images/lib/as3539-3461-4137-b062-323338303166/__-49.png","/images/lib/as3262-3561-4561-a132-303535353162/__-48.png"),
 ("/video/vivax","VIVAX","/images/lib/as6163-3132-4061-a536-363936336533/__-52.png","/images/lib/as3863-3166-4537-b165-666530633530/__-53.png"),
 ("/video/powertechnologies","Power Technologies","/images/lib/as3161-3132-4333-b964-323537373462/__-30.png","/images/lib/as6461-3331-4335-b938-303861386461/__-31.png"),
 ("/video/silkway","Silk Way rally","/images/lib/as6164-6432-4132-a361-613136626438/__-51.png","/images/lib/as6533-3762-4130-b261-623063313634/__-50.png"),
 ("/video/eaton","Eaton","/images/lib/as3935-3832-4662-a132-383864613435/__-35.png","/images/lib/as3230-6137-4239-a364-633132313630/__-34.png"),
 ("/video/lingerie","Lingerie","/images/lib/as3439-3739-4562-a533-616631333163/__-37.png","/images/lib/as6538-3664-4239-b165-373961323065/__-36.png"),
 ("/video/mozaika","ТРЦ Мозаика","/images/lib/as6537-6538-4133-b832-383637333832/__-45.png","/images/lib/as6430-3038-4564-b866-656564353862/__-44.png"),
 ("/video/interplastika","Выставка Интерпластика","/images/lib/as3331-3035-4965-a439-613266363431/__-54.png","/images/lib/as3236-3931-4830-b430-613039636464/__-55.png"),
 ("/video/salaris","ТРЦ Саларис","/images/lib/as3933-3462-4563-b861-383364333966/__-15.png","/images/lib/as6562-6336-4135-b963-663236626332/__-17.png"),
 ("/mmg","MMG Павелецкая Плаза","/images/lib/stor3435-6339-4163-a433-646336343434/88889dcf73b126c47c1dec4a187d308a.png","/images/lib/stor3537-3038-4132-b037-366562353233/087b9c742259d2a29447378822e54430.png"),
 ("/bekobod1","Технопарк «Бекабад»","/images/lib/stor3864-3666-4061-a664-313234373466/3c39f9f2139e90b9e968795284629146.png","/images/lib/stor6536-3434-4334-a338-306338373661/570b6c04bb5e452b49c025c5dccfeb19.png"),
 ("/zubovo","Технопарк «Зубово»","/images/lib/stor6538-6135-4162-a565-653035323933/f16af483ac499f1871910e5ee28eb3e7.png","/images/lib/stor3531-3862-4630-b831-643033613835/6468eab2f57a08f7ba31e66b5ff33bc2.png"),
 ("/isotec","Isotec","/images/lib/stor3039-3238-4836-b039-616562373464/11635b224858f8c0034b3ee15dc4687f.png","/images/lib/stor6232-3038-4866-b438-393133613665/f677d5c057c5689fb807659ff68e24f9.png"),
]

METRIKA='<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

PAGE_CSS="""<style id="vp-css">
/* точная Tilda-шапка приходит из общего хрома (react-chrome.py, TILDA_HDR_CSS) */
.vp-main{font-family:'Montserrat',-apple-system,Arial,sans-serif;color:#14171C}
.vp-main a:focus-visible,.vp-main button:focus-visible{outline:3px solid #CF6F19;outline-offset:3px;border-radius:4px}
/* ------- герой: зацикленный шоурил ------- */
/* постер-подложка всегда под видео; видео невидимо до реального старта
   воспроизведения ('playing' -> .is-on): на мобильных с заблокированным
   autoplay виден только красивый кадр, никакой системной кнопки плей */
.vp-hero{position:relative;overflow:hidden;background:#14171C;color:#fff}
.vp-hero__poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.vp-hero__v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s ease;pointer-events:none}
.vp-hero__v.is-on{opacity:1}
.vp-hero__shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,23,28,.62) 0%,rgba(20,23,28,.34) 46%,rgba(20,23,28,.74) 100%)}
.vp-hero__in{position:relative;max-width:1180px;margin:0 auto;padding:110px 40px 120px;min-height:min(66vh,560px);display:flex;flex-direction:column;justify-content:center}
.vp-hero__t{margin:0;font-size:clamp(44px,6.6vw,88px);line-height:.98;font-weight:800;letter-spacing:-.025em;color:#fff}
.vp-hero__sub{margin:20px 0 0;font-size:clamp(18px,2vw,24px);font-weight:700;color:#fff}
.vp-hero__lead{margin:18px 0 0;max-width:560px;font-size:17px;line-height:1.65;color:rgba(255,255,255,.85)}
.vp-hero__act{margin-top:34px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.vp-cta{display:inline-block;background:#FCB724;color:#14171C;font-weight:800;font-size:16px;text-decoration:none;padding:16px 42px;border-radius:30px;transition:transform .15s,box-shadow .15s}
.vp-cta:hover{transform:translateY(-2px);box-shadow:0 14px 26px -14px rgba(252,183,36,.9)}
.vp-cta_ghost{background:transparent;color:#fff;box-shadow:inset 0 0 0 2px rgba(255,255,255,.42);font-weight:700}
.vp-cta_ghost:hover{box-shadow:inset 0 0 0 2px #fff}
/* ------- секции ------- */
.vp-sec{max-width:1180px;margin:0 auto;padding:76px 40px}
.vp-sec__head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;margin-bottom:14px}
.vp-sec__h{font-size:clamp(26px,3vw,38px);font-weight:800;letter-spacing:-.02em;margin:0}
.vp-sec__lead{margin:0 0 8px;max-width:640px;font-size:16px;line-height:1.6;color:#5A616A}
.vp-all{font-weight:700;font-size:15px;color:#CF6F19;text-decoration:none;white-space:nowrap}
.vp-all:hover{text-decoration:underline}
/* появление при скролле — как плитки услуг */
.vp-rev{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1)}
.vp-rev.is-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.vp-rev{transition:none!important;opacity:1!important;transform:none!important}}
/* вид работ: описание слева, примеры справа */
.vp-wt{display:grid;grid-template-columns:minmax(240px,4fr) 8fr;gap:34px;padding:40px 0;border-top:1px solid rgba(20,23,28,.1)}
.vp-wt:first-of-type{border-top:0;padding-top:26px}
.vp-wt__t{display:flex;align-items:center;gap:12px;margin:0;font-size:clamp(20px,2.2vw,27px);font-weight:800;letter-spacing:-.02em;line-height:1.15}
.vp-wt__sq{flex:none;width:13px;height:13px;border-radius:4px;background:#CF6F19}
.vp-wt__d{margin:12px 0 0;font-size:15px;line-height:1.65;color:#5A616A}
.vp-wt__ex{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;align-content:start}
.vp-wt__ex_three{grid-template-columns:repeat(3,1fr)}
/* пример: фасад — постер + плей, видео грузится по клику */
.vp-ex__cap{margin-top:10px;font-weight:700;font-size:14px}
.vp-ex__cap::before{content:"";display:inline-block;width:8px;height:8px;border-radius:2px;background:#CF6F19;margin-right:8px;vertical-align:1px}
.vp-ex{margin:0}
.vp-facade{position:relative;display:block;width:100%;aspect-ratio:16/9;padding:0;border:0;border-radius:14px;overflow:hidden;background:#14171C;cursor:pointer;box-shadow:0 8px 22px -16px rgba(0,0,0,.25)}
.vp-facade img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .35s}
.vp-facade:hover img{transform:scale(1.05)}
.vp-facade__play{position:absolute;left:50%;top:50%;width:62px;height:62px;transform:translate(-50%,-50%);border-radius:50%;background:#FFE000;transition:transform .2s;box-shadow:0 10px 26px -8px rgba(0,0,0,.5)}
.vp-facade__play::after{content:"";position:absolute;left:55%;top:50%;transform:translate(-50%,-50%);border-style:solid;border-width:11px 0 11px 18px;border-color:transparent transparent transparent #14171C}
.vp-facade:hover .vp-facade__play{transform:translate(-50%,-50%) scale(1.1)}
/* модалка: видео поверх страницы нормального размера */
.vp-modal{position:fixed;inset:0;z-index:2000;display:flex;align-items:center;justify-content:center;padding:24px;background:rgba(10,12,16,.9);animation:vpFade .2s ease}
@keyframes vpFade{from{opacity:0}to{opacity:1}}
.vp-modal__box{position:relative;width:min(1100px,96vw)}
.vp-modal video{display:block;width:100%;max-height:82vh;aspect-ratio:16/9;object-fit:contain;background:#000;border-radius:14px;box-shadow:0 40px 90px -30px rgba(0,0,0,.8)}
.vp-modal__cap{margin-top:12px;color:#fff;font-weight:700;font-size:15px;font-family:'Montserrat',Arial,sans-serif}
.vp-modal__close{position:absolute;top:-14px;right:-14px;z-index:1;width:44px;height:44px;border:0;border-radius:50%;background:#FFE000;cursor:pointer;box-shadow:0 10px 24px -8px rgba(0,0,0,.6);transition:transform .15s}
.vp-modal__close:hover{transform:scale(1.08)}
.vp-modal__close::before,.vp-modal__close::after{content:"";position:absolute;left:50%;top:50%;width:20px;height:2.5px;background:#14171C;border-radius:2px}
.vp-modal__close::before{transform:translate(-50%,-50%) rotate(45deg)}
.vp-modal__close::after{transform:translate(-50%,-50%) rotate(-45deg)}
@media(max-width:560px){.vp-modal{padding:12px}.vp-modal__close{top:-10px;right:-4px;width:40px;height:40px}}
/* лента видеопрезентаций */
.vp-pres{display:grid;grid-auto-flow:column;grid-auto-columns:300px;gap:20px;overflow-x:auto;scroll-snap-type:x proximity;padding:4px 2px 10px;-webkit-overflow-scrolling:touch}
.vp-pres .vp-ex{scroll-snap-align:start}
/* кейсы: 1:1 плитки родного Tilda-каталога (круглые картинки, 4 колонки),
   при наведении — вторая картинка галереи с информацией, как в родном сторе */
.vp-cases-wrap{background:#fff}
.vp-cases{display:grid;grid-template-columns:repeat(4,1fr);gap:40px;margin-top:26px}
.vp-card{position:relative;display:block}
.vp-card img{width:100%;height:auto;display:block;aspect-ratio:1/1;object-fit:contain}
.vp-card__hov{position:absolute;inset:0;opacity:0;transition:opacity .25s ease}
@media(hover:hover){
 .vp-card:hover .vp-card__hov,.vp-card:focus-visible .vp-card__hov{opacity:1}
 .vp-card:hover img:first-child,.vp-card:focus-visible img:first-child{opacity:0;transition:opacity .25s ease}}
/* ------- адаптив ------- */
@media(max-width:1020px){
 .vp-hero__in{padding:84px 24px 92px}
 .vp-sec{padding:56px 24px}
 .vp-wt{grid-template-columns:1fr;gap:22px;padding:32px 0}
 .vp-wt__ex_three{grid-template-columns:repeat(2,1fr)}
 .vp-cases{grid-template-columns:1fr 1fr}}
@media(max-width:560px){
 .vp-hero__in{padding:64px 16px 72px;min-height:60vh}
 .vp-hero__lead{font-size:15.5px}
 .vp-cta{padding:14px 32px;font-size:15px}
 .vp-sec{padding:44px 16px}
 .vp-wt__ex,.vp-wt__ex_three{grid-template-columns:1fr}
 .vp-pres{grid-auto-columns:78vw}
 /* кейсы — 2 колонки, как родной мобильный каталог */
 .vp-cases{grid-template-columns:1fr 1fr;gap:18px}}
</style>"""

# Фасад видео: по клику открывается модалка поверх страницы с <video>
# (ролик грузится только в этот момент). Закрытие: крестик, клик по фону, Esc.
# Плюс экономия на герое: пауза вне вьюпорта и при prefers-reduced-motion.
VIDEO_JS="""<script>(function(){
var opener=null;
function closeModal(){
 var m=document.querySelector('.vp-modal');if(!m)return;
 var v=m.querySelector('video');if(v){v.pause();v.removeAttribute('src');v.load();}
 m.remove();document.body.style.overflow='';
 if(opener&&opener.focus)opener.focus();opener=null;
}
function openModal(src,title){
 closeModal();
 var m=document.createElement('div');m.className='vp-modal';
 m.setAttribute('role','dialog');m.setAttribute('aria-modal','true');
 m.setAttribute('aria-label',title||'Видео');
 var box=document.createElement('div');box.className='vp-modal__box';
 var x=document.createElement('button');x.type='button';x.className='vp-modal__close';x.setAttribute('aria-label','Закрыть видео');
 var v=document.createElement('video');
 v.controls=true;v.playsInline=true;v.preload='metadata';v.autoplay=true;
 v.setAttribute('playsinline','');v.src=src;
 if(title)v.setAttribute('aria-label',title);
 box.appendChild(x);box.appendChild(v);
 if(title){var c=document.createElement('div');c.className='vp-modal__cap';c.textContent=title;box.appendChild(c);}
 m.appendChild(box);document.body.appendChild(m);
 document.body.style.overflow='hidden';
 v.play().catch(function(){});x.focus();
}
document.addEventListener('click',function(e){
 var b=e.target.closest&&e.target.closest('.vp-facade');
 if(b){opener=b;openModal(b.getAttribute('data-video'),(b.getAttribute('aria-label')||'').replace(/^Смотреть видео: /,''));return;}
 if(e.target.closest&&e.target.closest('.vp-modal__close')){closeModal();return;}
 var m=e.target.classList&&e.target.classList.contains('vp-modal');
 if(m)closeModal();
});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal();});
var hv=document.querySelector('.vp-hero__v');
if(hv){
 hv.addEventListener('playing',function(){hv.classList.add('is-on');});
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){hv.removeAttribute('autoplay');hv.pause();}
 else if('IntersectionObserver' in window){
  new IntersectionObserver(function(es){es.forEach(function(en){
   if(en.isIntersecting){hv.play&&hv.play().catch(function(){});}else{hv.pause&&hv.pause();}
  });}).observe(hv);}
}
})();</script>"""

REVEAL_JS="""<noscript><style>.vp-rev{opacity:1!important;transform:none!important}</style></noscript>
<script>(function(){
var els=[].slice.call(document.querySelectorAll('.vp-rev'));
function showAll(){els.forEach(function(n){n.classList.add('is-in');});}
if(!('IntersectionObserver' in window)){showAll();return;}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
els.forEach(function(n,i){n.style.transitionDelay=Math.min(i%4*90,270)+'ms';io.observe(n);});
})();</script>"""

RALEWAY='<link href="/fonts/raleway-700.css" rel="stylesheet">'  # self-host, см. mirror/fonts/

HEAD=f'''<!doctype html><html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Видеопродакшн полного цикла в Москве и по всей России — Hand Marketing</title>
<meta name="description" content="Видеопродакшн полного цикла: съёмка рекламных и корпоративных видеороликов, репортажи с мероприятий, обучающие видео и видеопрезентации. Съёмка, монтаж, графика — Hand Marketing, Москва и вся Россия.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hand-marketing.ru/videoproduction/">
<meta property="og:type" content="website"><meta property="og:title" content="Видеопродакшн полного цикла в Москве и по всей России — Hand Marketing">
<meta property="og:description" content="Видеопродакшн полного цикла: рекламные, репортажные, вирусные ролики, корпоративные фильмы, обучающие видео и видеопрезентации.">
<meta property="og:url" content="https://hand-marketing.ru/videoproduction/">
<meta property="og:image" content="https://hand-marketing.ru/images/vp/hero-poster.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
{rc.FONT}{RALEWAY}{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''

def facade(title,poster,video):
    return (f'<button type="button" class="vp-facade" data-video="{video}" aria-label="Смотреть видео: {H.escape(title)}">'
            f'<img src="{poster}" alt="{H.escape(title)}" loading="lazy" width="960" height="540">'
            f'<span class="vp-facade__play" aria-hidden="true"></span></button>')

def work_types():
    out=''
    for t,d,exs in WORK_TYPES:
        cards=''.join(f'<figure class="vp-ex">{facade(f"{t}: {et}",ep,ev)}'
                      f'<figcaption class="vp-ex__cap">Кейс: {H.escape(et)}</figcaption></figure>'
                      for et,ep,ev in exs)
        three=' vp-wt__ex_three' if len(exs)==3 else ''
        out+=(f'<section class="vp-wt vp-rev"><div class="vp-wt__info">'
              f'<h3 class="vp-wt__t"><i class="vp-wt__sq" aria-hidden="true"></i>{H.escape(t)}</h3>'
              f'<p class="vp-wt__d">{H.escape(d)}</p></div>'
              f'<div class="vp-wt__ex{three}">{cards}</div></section>')
    # видеопрезентации — лента
    pres=''.join(f'<figure class="vp-ex">{facade(f"Видеопрезентация: {et}",ep,ev)}'
                 f'<figcaption class="vp-ex__cap">{H.escape(et)}</figcaption></figure>'
                 for et,ep,ev in PRESENTATIONS)
    out+=(f'<section class="vp-wt vp-rev"><div class="vp-wt__info">'
          f'<h3 class="vp-wt__t"><i class="vp-wt__sq" aria-hidden="true"></i>Видеопрезентации</h3>'
          f'<p class="vp-wt__d">Презентация проекта стенда Самарской области для форума «Россия — спортивная держава»: концепции, визуализации и контент стенда.</p></div>'
          f'<div class="vp-pres">{pres}</div></section>')
    return out

def cases():
    return ''.join(f'<a class="vp-card vp-rev" href="{url}">'
                   f'<img src="{img}" alt="{H.escape(t)}" loading="lazy">'
                   f'<img class="vp-card__hov" src="{hov}" alt="" loading="lazy" aria-hidden="true"></a>'
                   for url,t,img,hov in CASES)

def build():
    hero=(f'<section class="vp-hero">'
          f'<img class="vp-hero__poster" src="/images/vp/hero-poster.jpg" alt="" aria-hidden="true">'
          f'<video class="vp-hero__v" autoplay muted loop playsinline preload="metadata" aria-hidden="true">'
          f'<source src="/media/vp-hero-loop.mp4" type="video/mp4"></video>'
          f'<div class="vp-hero__shade" aria-hidden="true"></div>'
          f'<div class="vp-hero__in">'
          # SEO: русский запрос — в <h1>, английское слово — крупный видимый акцент (вид не меняется)
          f'<div class="vp-hero__t">Video Production</div>'
          f'<h1 class="vp-hero__sub">Видеопродакшн полного цикла</h1>'
          f'<p class="vp-hero__lead">Технологичные и кинематографичные видеорешения для вашего бизнеса: съёмка рекламных роликов, производство корпоративных фильмов, монтаж и графика.</p>'
          f'<div class="vp-hero__act"><a class="vp-cta" href="#lead">Обсудить проект</a>'
          f'<a class="vp-cta vp-cta_ghost" href="#vp-cases">Смотреть кейсы</a></div></div></section>')
    works=(f'<section class="vp-sec" id="vp-works">'
           f'<div class="vp-sec__head"><h2 class="vp-sec__h vp-rev">Что мы снимаем</h2></div>'
           f'<p class="vp-sec__lead vp-rev">Каждое направление — с живыми примерами: нажмите на кадр, чтобы посмотреть ролик.</p>'
           f'{work_types()}</section>')
    case_sec=(f'<div class="vp-cases-wrap" id="vp-cases"><section class="vp-sec">'
          f'<div class="vp-sec__head"><h2 class="vp-sec__h vp-rev">Кейсы</h2><a class="vp-all vp-rev" href="/project">Все проекты →</a></div>'
          f'<div class="vp-cases">{cases()}</div></section></div>')
    body=f'{rc.header()}<main class="vp-main">{hero}{works}{case_sec}</main><a id="lead"></a>{rc.footer()}{rc.JS}{VIDEO_JS}{REVEAL_JS}</body></html>'
    return HEAD+body

if __name__=='__main__':
    out=os.path.join(ROOT,'videoproduction')
    os.makedirs(out,exist_ok=True)
    open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(build())
    print("создано: mirror/videoproduction/index.html")
    old=os.path.join(out,'index-a2.html')
    if os.path.exists(old):
        os.remove(old)
        print("удалено: mirror/videoproduction/index-a2.html (иначе деплой-своп затёр бы новую страницу)")
