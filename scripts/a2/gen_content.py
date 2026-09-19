#!/usr/bin/env python3
"""Генерит mirror/content/index.html — страницу услуги «Content» (мультимедийный
контент) по структуре weshow.su/services/multimedia-content: hero, 4 направления,
детальные секции с примерами (модалка поверх страницы, фасадный паттерн — до клика
грузится только постер), autoplay-луп в «Адаптации», CTA. В hero — зацикленная
нарезка из наших роликов /media/content-hero-loop.mp4 (~20 с, 2 МБ: нога в лужу и
робот из Газели-трансформера, маппинг Ставрополя, заставки, 3D Шёлкового пути,
Волга с ладьями и мостом, закат с лодками, ракета), как на /videoproduction.
Стандартные шапка/подвал из react-chrome.py.
Видео self-host /media/*.mp4 (заливаются вручную, список в VIDEO-UPLOAD.md);
Naked Eye переиспользует уже залитый /media/stavropol-vdnh-nakedeye.mp4.
build_v1 страницу пропускает по маркеру <!--custom-page-->."""
import os, importlib.util, html as H
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import commerce_block as cb  # цена «от», отзывы, Service/Breadcrumb (14.09.2026)

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,'..','..','mirror'))

spec=importlib.util.spec_from_file_location("rc", os.path.join(HERE,"react-chrome.py"))
rc=importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

# 4 направления (карточки под hero): (цвет, заголовок, текст)
FEATS=[
 ("#5E9A2E","Графическое оформление","Яркие и динамичные заставки, титры и оформление для экранов любых размеров. Задаём тон вашему мероприятию."),
 ("#CF6F19","3D-контент и мэппинг","Контент для сложных поверхностей, изогнутых экранов и архитектурных форм с точностью до пикселя."),
 ("#C12164","Naked Eye 3D","Впечатляющий объёмный контент, который зрители видят без специальных очков. Эффект выхода за рамки экрана."),
 ("#673A7E","Брендинг мероприятий","Комплексная разработка визуального стиля: Key Vision, мультимедиа-контент и брендирование физических поверхностей."),
]

METRIKA='<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

PAGE_CSS="""<style id="ct-css">
.ct-main{font-family:'Montserrat',-apple-system,Arial,sans-serif;color:#14171C}
.ct-main a:focus-visible,.ct-main button:focus-visible{outline:3px solid #673A7E;outline-offset:3px;border-radius:4px}
/* ------- герой: зацикленная нарезка из наших роликов (как /videoproduction) ------- */
/* постер-подложка всегда под видео; видео невидимо до реального старта
   воспроизведения ('playing' -> .is-on): на мобильных с заблокированным
   autoplay виден только красивый кадр, никакой системной кнопки плей */
.ct-hero{position:relative;overflow:hidden;background:#0E1116;color:#fff}
.ct-hero__poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ct-hero__v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s ease;pointer-events:none}
.ct-hero__v.is-on{opacity:1}
.ct-hero__shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,17,22,.62) 0%,rgba(14,17,22,.34) 46%,rgba(14,17,22,.74) 100%)}
.ct-hero__in{position:relative;max-width:1180px;margin:0 auto;padding:110px 40px 120px;min-height:min(66vh,560px);display:flex;flex-direction:column;justify-content:center;align-items:flex-start}
.ct-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;background:rgba(255,224,0,.1);
 box-shadow:inset 0 0 0 1px rgba(255,224,0,.35);color:#FFE000;font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;font-family:'Raleway',Arial,sans-serif}
.ct-hero__t{margin:22px 0 0;font-size:clamp(44px,6.6vw,88px);line-height:.98;font-weight:800;letter-spacing:-.025em;color:#fff}
.ct-hero__sub{margin:18px 0 0;font-size:clamp(19px,2.2vw,26px);font-weight:700;line-height:1.25;
 background:linear-gradient(92deg,#8BC34A,#FFB84D 38%,#FF5CA8 70%,#B36BE0);-webkit-background-clip:text;background-clip:text;color:transparent}
.ct-hero__lead{margin:18px 0 0;max-width:520px;font-size:17px;line-height:1.65;color:rgba(255,255,255,.82)}
.ct-hero__act{margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.ct-cta{display:inline-block;background:#FCB724;color:#14171C;font-weight:800;font-size:16px;text-decoration:none;padding:16px 42px;border-radius:30px;transition:transform .15s,box-shadow .15s;border:0;cursor:pointer}
.ct-cta:hover{transform:translateY(-2px);box-shadow:0 14px 26px -14px rgba(252,183,36,.9)}
.ct-cta_ghost{background:transparent;color:#fff;box-shadow:inset 0 0 0 2px rgba(255,255,255,.42);font-weight:700}
.ct-cta_ghost:hover{box-shadow:inset 0 0 0 2px #fff}
/* ------- секции ------- */
.ct-sec{max-width:1180px;margin:0 auto;padding:64px 40px}
.ct-rev{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1)}
.ct-rev.is-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.ct-rev{transition:none!important;opacity:1!important;transform:none!important}}
/* 4 направления */
.ct-feats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.ct-feat{background:#fff;border:1px solid rgba(20,23,28,.1);border-radius:18px;padding:26px 24px;box-shadow:0 8px 22px -18px rgba(0,0,0,.25)}
.ct-feat__sq{width:15px;height:15px;border-radius:4px;background:var(--c);margin-bottom:16px}
.ct-feat h3{margin:0 0 8px;font-size:17px;font-weight:800;letter-spacing:-.01em;line-height:1.3}
.ct-feat p{margin:0;font-size:14px;line-height:1.55;color:#5A616A}
/* детальные ряды */
.ct-row{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;padding:44px 0;border-top:1px solid rgba(20,23,28,.08)}
.ct-row:first-of-type{border-top:0}
.ct-row__t{display:flex;align-items:flex-start;gap:12px;margin:0;font-size:clamp(24px,2.6vw,32px);font-weight:800;letter-spacing:-.02em;line-height:1.12}
.ct-row__sq{flex:none;width:14px;height:14px;border-radius:4px;background:var(--accent);margin-top:10px}
.ct-row__d{margin:14px 0 0;font-size:16px;line-height:1.7;color:#5A616A}
.ct-row__list{margin:16px 0 0;padding:0;list-style:none}
.ct-row__list li{position:relative;padding-left:22px;margin-top:10px;font-size:16px;color:#5A616A}
.ct-row__list li::before{content:"";position:absolute;left:0;top:.5em;width:10px;height:10px;border-radius:3px;background:var(--accent)}
.ct-row_rev .ct-row__media{order:-1}
/* медиа: фасад с плеем / картинка / автолуп */
.ct-facade{position:relative;display:block;width:100%;aspect-ratio:16/9;padding:0;border:0;border-radius:16px;overflow:hidden;background:#14171C;cursor:pointer;box-shadow:0 24px 48px -28px rgba(20,23,28,.5)}
.ct-facade img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s}
.ct-facade:hover img{transform:scale(1.04)}
.ct-facade__play{position:absolute;left:50%;top:50%;width:64px;height:64px;transform:translate(-50%,-50%);border-radius:50%;background:#FFE000;transition:transform .2s;box-shadow:0 10px 26px -8px rgba(0,0,0,.5)}
.ct-facade__play::after{content:"";position:absolute;left:55%;top:50%;transform:translate(-50%,-50%);border-style:solid;border-width:11px 0 11px 18px;border-color:transparent transparent transparent #14171C}
.ct-facade:hover .ct-facade__play{transform:translate(-50%,-50%) scale(1.1)}
.ct-img{width:100%;border-radius:16px;display:block;box-shadow:0 24px 48px -28px rgba(20,23,28,.5)}
.ct-img_contain{background:#F5F5F7;padding:18px;box-sizing:border-box;object-fit:contain;box-shadow:none;border:1px solid rgba(20,23,28,.08)}
.ct-duo{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.ct-duo figure{margin:0}
.ct-duo .ct-facade{border-radius:14px}
.ct-duo .ct-facade__play{width:50px;height:50px}
.ct-duo .ct-facade__play::after{border-width:9px 0 9px 14px}
.ct-cap{margin-top:9px;font-weight:700;font-size:13.5px}
.ct-cap::before{content:"";display:inline-block;width:8px;height:8px;border-radius:2px;background:var(--accent);margin-right:8px;vertical-align:1px}
.ct-loop{position:relative;border-radius:16px;overflow:hidden;box-shadow:0 24px 48px -28px rgba(20,23,28,.5);aspect-ratio:16/9;background:#14171C}
.ct-loop__poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ct-loop video{position:relative;width:100%;height:100%;object-fit:cover;display:block;opacity:0;transition:opacity .6s ease;pointer-events:none}
.ct-loop video.is-on{opacity:1}
/* финальный CTA */
.ct-final{position:relative;overflow:hidden;background:#14171C;border-radius:28px;padding:clamp(44px,6vw,84px) clamp(24px,5vw,72px);text-align:center;color:#fff}
.ct-final::before,.ct-final::after{content:"";position:absolute;width:420px;height:420px;border-radius:50%;filter:blur(110px);opacity:.32}
.ct-final::before{right:-120px;top:-140px;background:#673A7E}
.ct-final::after{left:-120px;bottom:-160px;background:#C12164}
.ct-final>*{position:relative;z-index:1}
.ct-final h2{margin:0;font-size:clamp(26px,3.6vw,44px);font-weight:800;letter-spacing:-.02em;color:#fff}
.ct-final p{margin:16px auto 0;max-width:52ch;font-size:17px;line-height:1.6;color:rgba(255,255,255,.8)}
.ct-final .ct-cta{margin-top:30px}
/* ------- адаптив ------- */
@media(max-width:1020px){
 .ct-hero__in{padding:84px 24px 92px}
 .ct-sec{padding:48px 24px}
 .ct-feats{grid-template-columns:1fr 1fr}
 .ct-row{grid-template-columns:1fr;gap:24px;padding:36px 0}
 .ct-row_rev .ct-row__media{order:0}}
@media(max-width:560px){
 .ct-hero__in{padding:64px 16px 72px;min-height:60vh}
 .ct-sec{padding:40px 16px}
 .ct-feats{grid-template-columns:1fr}
 .ct-duo{grid-template-columns:1fr}
 .ct-cta{padding:14px 32px;font-size:15px}}
/* модалка видео (как на /videoproduction) */
.ct-modal{position:fixed;inset:0;z-index:2000;display:flex;align-items:center;justify-content:center;padding:24px;background:rgba(10,12,16,.9);animation:ctFade .2s ease}
@keyframes ctFade{from{opacity:0}to{opacity:1}}
.ct-modal__box{position:relative;width:min(1100px,96vw)}
.ct-modal video{display:block;width:100%;max-height:82vh;aspect-ratio:16/9;object-fit:contain;background:#000;border-radius:14px;box-shadow:0 40px 90px -30px rgba(0,0,0,.8)}
.ct-modal__cap{margin-top:12px;color:#fff;font-weight:700;font-size:15px;font-family:'Montserrat',Arial,sans-serif}
.ct-modal__close{position:absolute;top:-14px;right:-14px;z-index:1;width:44px;height:44px;border:0;border-radius:50%;background:#FFE000;cursor:pointer;box-shadow:0 10px 24px -8px rgba(0,0,0,.6);transition:transform .15s}
.ct-modal__close:hover{transform:scale(1.08)}
.ct-modal__close::before,.ct-modal__close::after{content:"";position:absolute;left:50%;top:50%;width:20px;height:2.5px;background:#14171C;border-radius:2px}
.ct-modal__close::before{transform:translate(-50%,-50%) rotate(45deg)}
.ct-modal__close::after{transform:translate(-50%,-50%) rotate(-45deg)}
@media(max-width:560px){.ct-modal{padding:12px}.ct-modal__close{top:-10px;right:-4px;width:40px;height:40px}}
</style>"""

VIDEO_JS="""<script>(function(){
var opener=null;
function closeModal(){
 var m=document.querySelector('.ct-modal');if(!m)return;
 var v=m.querySelector('video');if(v){v.pause();v.removeAttribute('src');v.load();}
 m.remove();document.body.style.overflow='';
 if(opener&&opener.focus)opener.focus();opener=null;
}
function openModal(src,title){
 closeModal();
 var m=document.createElement('div');m.className='ct-modal';
 m.setAttribute('role','dialog');m.setAttribute('aria-modal','true');
 m.setAttribute('aria-label',title||'Видео');
 var box=document.createElement('div');box.className='ct-modal__box';
 var x=document.createElement('button');x.type='button';x.className='ct-modal__close';x.setAttribute('aria-label','Закрыть видео');
 var v=document.createElement('video');
 v.controls=true;v.playsInline=true;v.preload='metadata';v.autoplay=true;
 v.setAttribute('playsinline','');v.src=src;
 if(title)v.setAttribute('aria-label',title);
 box.appendChild(x);box.appendChild(v);
 if(title){var c=document.createElement('div');c.className='ct-modal__cap';c.textContent=title;box.appendChild(c);}
 m.appendChild(box);document.body.appendChild(m);
 document.body.style.overflow='hidden';
 v.play().catch(function(){});x.focus();
}
document.addEventListener('click',function(e){
 var b=e.target.closest&&e.target.closest('.ct-facade');
 if(b){opener=b;openModal(b.getAttribute('data-video'),(b.getAttribute('aria-label')||'').replace(/^Смотреть видео: /,''));return;}
 if(e.target.closest&&e.target.closest('.ct-modal__close')){closeModal();return;}
 if(e.target.classList&&e.target.classList.contains('ct-modal'))closeModal();
});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal();});
// автолупы (герой + «Адаптация»): видимы только после реального старта ('playing'),
// пауза вне вьюпорта и при prefers-reduced-motion
var lvs=document.querySelectorAll('.ct-loop video,.ct-hero__v');
[].forEach.call(lvs,function(lv){
 lv.addEventListener('playing',function(){lv.classList.add('is-on');});
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){lv.removeAttribute('autoplay');lv.pause();}
 else if('IntersectionObserver' in window){
  new IntersectionObserver(function(es){es.forEach(function(en){
   if(en.isIntersecting){lv.play&&lv.play().catch(function(){});}else{lv.pause&&lv.pause();}
  });}).observe(lv);}
});
})();</script>"""

REVEAL_JS="""<noscript><style>.ct-rev{opacity:1!important;transform:none!important}</style></noscript>
<script>(function(){
var els=[].slice.call(document.querySelectorAll('.ct-rev'));
if(!('IntersectionObserver' in window)){els.forEach(function(n){n.classList.add('is-in');});return;}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
els.forEach(function(n,i){n.style.transitionDelay=Math.min(i%4*90,270)+'ms';io.observe(n);});
})();</script>"""

RALEWAY='<link href="/fonts/raleway-700.css" rel="stylesheet">'  # self-host, см. mirror/fonts/

HEAD=f'''<!doctype html><html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Мультимедийный контент для мероприятий и выставок | Hand Marketing</title>
<meta name="description" content="Видеомаппинг и 3D-графика, интерактивные инсталляции и стенды, Naked Eye 3D, VR и контент для инфо-панелей. Мультимедиа для мероприятий и выставок.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hand-marketing.ru/content/">
<meta property="og:type" content="website"><meta property="og:title" content="Мультимедийный контент для мероприятий и выставок | Hand Marketing">
<meta property="og:description" content="Графическое оформление, 3D-мэппинг, Naked Eye 3D, VR, инфо-панели, брендинг мероприятий и адаптация контента.">
<meta property="og:url" content="https://hand-marketing.ru/content/">
<meta property="og:image" content="https://hand-marketing.ru/images/content/nakedeye.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
{rc.FONT}{RALEWAY}{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''

def facade(title,poster,video,small=False):
    return (f'<button type="button" class="ct-facade" data-video="{video}" aria-label="Смотреть видео: {H.escape(title)}">'
            f'<img src="{poster}" alt="{H.escape(title)}" loading="lazy" width="960" height="540">'
            f'<span class="ct-facade__play" aria-hidden="true"></span></button>')

def feats():
    cards=''.join(f'<div class="ct-feat ct-rev" style="--c:{c}"><div class="ct-feat__sq" aria-hidden="true"></div>'
                  f'<h3>{H.escape(t)}</h3><p>{H.escape(d)}</p></div>' for c,t,d in FEATS)
    return f'<section class="ct-sec"><div class="ct-feats">{cards}</div></section>'

def row(accent,title,desc,media,rev=False,lst=None):
    lis=''.join(f'<li>{H.escape(x)}</li>' for x in (lst or []))
    lst_html=f'<ul class="ct-row__list">{lis}</ul>' if lis else ''
    cls='ct-row ct-rev'+(' ct-row_rev' if rev else '')
    return (f'<section class="{cls}" style="--accent:{accent}">'
            f'<div><h2 class="ct-row__t"><i class="ct-row__sq" aria-hidden="true"></i>{H.escape(title)}</h2>'
            f'<p class="ct-row__d">{H.escape(desc)}</p>{lst_html}</div>'
            f'<div class="ct-row__media">{media}</div></section>')

# SEO-блок: FAQ со schema.org (семантика: «мультимедийный контент» 1713 шир.,
# «интерактивные инсталляции» 43, «интерактивный стол» 395, «видеомаппинг»)
# ─── кейсы: (название, ссылка, цифра, что было сделано) ─────────────────────
CT_CASES = [
    ('Стенд Самарской области на ВДНХ', '/portfolio/samara-stand-vdnh/', '817',
     'слотов в расписании стенда: кинетический экран, naked eye 3D и зона истории работали '
     '248 дней подряд.'),
    ('3D-шоу в Ставрополе', '/3d/stavropol/', '27',
     'проекторов на фасаде Правительства края, девять зон по зданию и один пульт '
     'на всё шоу.'),
    ('Стенд Ставропольского края', '/portfolio/stavropol-stand-vdnh/', '17',
     'лакколитов в бинокуляре и куб с анаморфозой, который читается только '
     'с точки съёмки.'),
    ('Выставка «Самара»', '/creative/samara/', '46',
     'слов фирменного ядра, из которых алгоритм собирает стену зоны.'),
    ('Онлайн-трансляция Eaton', '/eaton_online/', '7',
     'часов эфира: мультивью, титры и вывод спикеров в прямой эфир с режиссёрского пульта.'),
    ('Презентация Changan CS35', '/event/changan/', '3',
     'проектора на кузов машины: раскраска корпуса светом прямо в дилерском центре.'),
]

# ─── поверхности, под которые считаем контент ───────────────────────────────
CT_SURFACES = [
    ('LED-экраны и видеостены',
     'Считаем композицию под реальный пиксельный шаг и физические размеры, а не под '
     'абстрактный 16:9. На стыке модулей картинка не рвётся.'),
    ('Медиафасады и архитектура',
     'Проекция на здание требует расчёта по геометрии фасада: окна, выступы, карнизы. '
     'На шоу в Ставрополе фасад разбивался на девять зон.'),
    ('Изогнутые экраны и купола',
     'Пересобираем кадр с учётом кривизны, чтобы горизонт не заваливался, а объекты '
     'не растягивались по краям.'),
    ('Кинетические конструкции',
     'Экран из подвижных модулей показывает изображение и рельеф одновременно. '
     'Контент под него считается кадр за кадром вместе с механикой.'),
    ('Naked eye 3D',
     'Объём без очков работает только из расчётной точки: мы считаем угол обзора '
     'и глубину сцены до того, как начнётся анимация.'),
    ('Пол, стены и потолок',
     'Проекция на пол и интерактивные стены: контент реагирует на людей, а не крутится '
     'по кругу.'),
    ('Тач-панели и инфокиоски',
     'Интерфейс, навигация и сценарии касаний. Посетитель должен находить нужное '
     'за два касания.'),
    ('VR и 360°',
     'Съёмка и сборка сред для очков: симуляции, обучающие сценарии, VR-кинотеатр '
     'для коллективного просмотра.'),
]

# ─── как идёт работа ────────────────────────────────────────────────────────
CT_STEPS = [
    ('Замеры и параметры', 'Разрешение, физические размеры, тип поверхности, точка '
     'обзора и условия освещения. От этого зависит всё остальное.'),
    ('Идея и раскадровка', 'Сценарий показа и раскадровка. Согласуем до того, как '
     'начнётся рендер, потому что переделка анимации дороже переделки эскиза.'),
    ('Производство', 'Графика, 3D, съёмка, звук. Работает наша команда, подрядчиков '
     'на контент не привлекаем.'),
    ('Сборка под поверхность', 'Нарезка под карту экранов, тесты на площадке, '
     'подгонка яркости и контраста под конкретную технику.'),
    ('Запуск и поддержка', 'Запуск на объекте, обучение оператора, обновление '
     'контента в течение работы проекта.'),
]

CT_FAQ=[
 ('Какой мультимедийный контент вы создаёте?',
  'Контент для LED-экранов и медиафасадов, видеомаппинг и 3D-графику, интерактивные инсталляции и сенсорные столы, Naked Eye 3D, VR-среды, контент для тач-панелей и инфокиосков, графические заставки и брендинг мероприятий.'),
 ('Делаете ли вы контент для выставочных стендов?',
  'Да, это одна из главных специализаций: контент проектируется вместе со стендом — под конкретные экраны, медиапотолки, пилоны и интерактивные зоны. Пример разбора такого проекта — на странице застройки выставочных стендов.'),
 ('Сколько стоит создание мультимедийного контента?',
  'Мультимедийная зона стоит от 150 000 ₽. Итог зависит от хронометража, разрешения поверхностей и сложности графики: контент для нестандартного медиафасада и заставка для LED-экрана — разные бюджеты. После брифа считаем смету бесплатно.'),
 ('Что нужно, чтобы адаптировать наш существующий контент под новые экраны?',
  'Исходники в максимальном качестве и параметры поверхностей: разрешение, физические размеры, тип экрана. Дальше мы пересоберём композицию под каждую поверхность — от изогнутых экранов до пола.'),
 ('Интерактивные инсталляции — это только для выставок?',
  'Нет: сенсорные столы, интерактивные стены и игровые механики работают в шоурумах, музеях, офисах продаж и на мероприятиях — везде, где нужно вовлечь посетителя, а не просто показать ролик.'),
 ('Сколько времени занимает производство контента?',
  'Заставки и графическое оформление делаем за неделю. Контент для мультимедийной зоны или стенда занимает 2–4 недели: неделя на идею и раскадровку, остальное на производство и тесты на площадке. Если поверхность нестандартная, к сроку добавляется время на замеры.'),
 ('Вы работаете с чужой техникой и чужим стендом?',
  'Да. Нам нужны карта экранов, разрешения и тип оборудования. Контент соберём под эту схему и приедем на тесты. Если техники ещё нет, поможем составить техническое задание для поставщика.'),
 ('Что нужно от заказчика, чтобы начать?',
  'Задача и аудитория, параметры поверхностей, фирменный стиль и материалы: логотипы, шрифты, фотографии, видео, тексты. Если чего-то нет, снимем и нарисуем сами: у нас свой видеопродакшн и дизайн-команда.'),
]

def ct_faq():
    import json
    items, ld = '', []
    for q,a in CT_FAQ:
        items += f'<details class="ct-faq__i ct-rev"><summary>{q}</summary><p>{a}</p></details>'
        ld.append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
    schema=json.dumps({'@context':'https://schema.org','@type':'FAQPage','mainEntity':ld},ensure_ascii=False)
    css=('<style id="ct-faq-css">'
         '.ct-seo__h{margin:0 0 14px;font-size:clamp(24px,3vw,34px);font-weight:800;letter-spacing:-.02em;color:#14171C}'
         '.ct-seo__lead{max-width:70ch;margin:0 0 26px;font-size:16px;line-height:1.65;color:#5A616A}'
         '.ct-seo__lead a{color:#673A7E;font-weight:600}'
         '.ct-faq{display:grid;gap:10px;max-width:820px}'
         '.ct-faq__i{border:1px solid rgba(20,23,28,.1);border-radius:14px;background:#fff;padding:0 20px}'
         '.ct-faq__i summary{cursor:pointer;list-style:none;position:relative;padding:15px 36px 15px 0;font-size:15.5px;font-weight:700}'
         '.ct-faq__i summary::-webkit-details-marker{display:none}'
         '.ct-faq__i summary::after{content:"";position:absolute;right:2px;top:50%;width:11px;height:11px;'
         'transform:translateY(-70%) rotate(45deg);border-right:2.5px solid #C12164;border-bottom:2.5px solid #C12164;transition:transform .2s}'
         '.ct-faq__i[open] summary::after{transform:translateY(-30%) rotate(225deg)}'
         '.ct-faq__i p{margin:0 0 16px;font-size:14.5px;line-height:1.65;color:#5A616A}'
         '</style>')
    return (f'<section class="ct-sec" id="ct-seo">{css}'
            f'<h2 class="ct-seo__h ct-rev">Вопросы о мультимедийном контенте</h2>'
            f'<p class="ct-seo__lead ct-rev">Создание мультимедийного контента у нас связано с реальными поверхностями: '
            f'мы сами строим <a href="/exhibition/">выставочные стенды</a> и снимаем <a href="/videoproduction/">видео</a>, '
            f'поэтому контент, интерактивные инсталляции и сенсорные столы проектируются под конкретные экраны, залы и задачи — '
            f'а не «в вакууме».</p>'
            f'<div class="ct-faq">{items}</div>'
            f'<script type="application/ld+json">{schema}</script></section>')

def ct_extra():
    """Кейсы, поверхности и процесс. Текста на странице было 476 слов против
    медианы 569 в нише (замер 19.09.2026, SEO-PLAN.md): в тонкой нише объём
    выигрывает дёшево, но только если он несёт цифры и разбор, а не воду."""
    cases = ''.join(
        f'<a class="ct-case ct-rev" href="{href}"><b>{num}</b><span>{txt}</span>'
        f'<em>{name}</em></a>' for name, href, num, txt in CT_CASES)
    surf = ''.join(f'<div class="ct-surf ct-rev"><h3>{t}</h3><p>{d}</p></div>'
                   for t, d in CT_SURFACES)
    steps = ''.join(f'<div class="ct-step ct-rev"><h3>{t}</h3><p>{d}</p></div>'
                    for t, d in CT_STEPS)
    css = ('<style id="ct-extra-css">'
           '.ct-cases{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:10px}'
           '.ct-case{display:block;border:1px solid rgba(20,23,28,.1);border-radius:16px;padding:20px;'
           'text-decoration:none;color:inherit;background:#fff;transition:border-color .2s,transform .2s}'
           '.ct-case:hover{border-color:#C12164;transform:translateY(-3px)}'
           '.ct-case b{display:block;font-size:30px;font-weight:800;letter-spacing:-.02em;color:#C12164}'
           '.ct-case span{display:block;margin:6px 0 12px;font-size:14px;line-height:1.55;color:#5A616A}'
           '.ct-case em{font-style:normal;font-size:14.5px;font-weight:700;'
           'border-bottom:1px solid rgba(193,33,100,.4)}'
           '.ct-surfs{display:grid;grid-template-columns:repeat(4,1fr);gap:18px 22px}'
           '.ct-surf{border-top:2px solid #C12164;padding-top:12px}'
           '.ct-surf h3{margin:0 0 6px;font-size:15px;font-weight:800;color:#14171C}'
           '.ct-surf p{margin:0;font-size:13.5px;line-height:1.55;color:#5A616A}'
           '.ct-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;counter-reset:cts}'
           '.ct-step{counter-increment:cts;border-top:2px solid #673A7E;padding-top:12px}'
           '.ct-step::before{content:"0" counter(cts);font-weight:800;font-size:13px;color:#673A7E;letter-spacing:.08em}'
           '.ct-step h3{margin:6px 0 6px;font-size:14.5px;font-weight:700;line-height:1.35;color:#14171C}'
           '.ct-step p{margin:0;font-size:13px;line-height:1.5;color:#5A616A}'
           '@media(max-width:1100px){.ct-surfs{grid-template-columns:repeat(2,1fr)}'
           '.ct-steps{grid-template-columns:repeat(2,1fr)}.ct-cases{grid-template-columns:repeat(2,1fr)}}'
           '@media(max-width:640px){.ct-surfs,.ct-steps,.ct-cases{grid-template-columns:1fr}}'
           '</style>')
    return (f'<section class="ct-sec" id="ct-cases">{css}'
            f'<h2 class="ct-seo__h ct-rev">Мультимедийные проекты, которые мы сделали</h2>'
            f'<p class="ct-seo__lead ct-rev">Контент для стендов, площадей и залов. У каждого '
            f'проекта на сайте есть разбор: что считали, как собирали и что получилось.</p>'
            f'<div class="ct-cases">{cases}</div>'
            f'<h2 class="ct-seo__h ct-rev" style="margin-top:54px">Под какие поверхности считаем контент</h2>'
            f'<p class="ct-seo__lead ct-rev">Ролик, снятый «в формате 16:9 и потом обрежем», '
            f'на нестандартной поверхности разваливается. Мы считаем картинку под конкретный '
            f'экран с самого начала.</p>'
            f'<div class="ct-surfs">{surf}</div>'
            f'<h2 class="ct-seo__h ct-rev" style="margin-top:54px">Как идёт работа</h2>'
            f'<div class="ct-steps">{steps}</div>'
            f'</section>')

def build():
    hero=(f'<section class="ct-hero">'
          f'<img class="ct-hero__poster" src="/images/content/hero-poster.jpg" alt="" aria-hidden="true">'
          f'<video class="ct-hero__v" autoplay muted loop playsinline preload="metadata" aria-hidden="true">'
          f'<source src="/media/content-hero-loop.mp4" type="video/mp4"></video>'
          f'<div class="ct-hero__shade" aria-hidden="true"></div>'
          f'<div class="ct-hero__in">'
          f'<span class="ct-badge">Новое поколение визуальных решений</span>'
          # SEO: русский запрос — в <h1>, английское слово — крупный видимый акцент (вид не меняется)
          f'<div class="ct-hero__t">Content</div>'
          f'<h1 class="ct-hero__sub">Мультимедийный контент — от идеи до воплощения</h1>'
          f'<p class="ct-hero__lead">Мы создаём цифровые миры: интерактивные инсталляции, видеомаппинг и контент для мультимедийных стендов. Передовые технологии и креативный подход для незабываемых впечатлений.</p>'
          f'<div class="ct-hero__act"><a class="ct-cta" href="#lead">Обсудить проект</a>'
          f'<a class="ct-cta ct-cta_ghost" href="#ct-works">Смотреть примеры</a></div>'
          f'</div></section>')

    duo=(f'<div class="ct-duo">'
         f'<figure>{facade("3D-контент и мэппинг: мэппинг на архитектуре","/images/content/mapping-arch.jpg","/media/content-mapping-arch.mp4")}'
         f'<figcaption class="ct-cap">Мэппинг на архитектуре</figcaption></figure>'
         f'<figure>{facade("3D-контент и мэппинг: контент для изогнутых экранов","/images/content/mapping-curved.jpg","/media/content-mapping-curved.mp4")}'
         f'<figcaption class="ct-cap">Контент для изогнутых экранов</figcaption></figure></div>')

    loop=('<div class="ct-loop"><img class="ct-loop__poster" src="/images/content/adaptation.jpg" alt="" aria-hidden="true">'
          '<video autoplay muted loop playsinline preload="metadata" '
          'aria-label="Адаптация контента под изогнутый экран"><source src="/media/content-adaptation-loop.mp4" type="video/mp4"></video></div>')

    rows=(
     row('#5E9A2E','Графическое оформление и заставки',
         'Создаём яркие и динамичные заставки, титры и графическое оформление для экранов любых размеров, которые задают тон вашему мероприятию и подчёркивают его статус.',
         facade('Графическое оформление','/images/content/graf.jpg','/media/content-graphics.mp4'))
     +row('#CF6F19','3D-контент и мэппинг',
         'Создание 3D-контента для изогнутых экранов, нестандартных конструкций и архитектурных поверхностей с расчётом «пиксель в пиксель». Мы учитываем геометрию каждой поверхности для идеальной оптической иллюзии.',
         duo, rev=True)
     +row('#C12164','Naked Eye 3D технологии',
         'Создаём впечатляющий 3D-контент для экранов с технологией Naked Eye: зрители видят объёмное изображение без специальных очков. Эффект выхода изображения за рамки экрана гарантирует вау-эффект.',
         facade('Naked Eye 3D','/images/content/nakedeye.jpg','/media/stavropol-vdnh-nakedeye.mp4'))
     +row('#673A7E','Комплексный брендинг мероприятий',
         'Разрабатываем единый визуальный стиль: Key Vision, контент для всех мультимедиа-носителей и брендирование физических поверхностей. Целостный подход обеспечивает максимальное погружение аудитории в атмосферу бренда.',
         '<img class="ct-img ct-img_contain" src="/images/content/branding.jpg" alt="Комплексный брендинг мероприятий: макеты носителей" loading="lazy">', rev=True)
     +row('#5E9A2E','VR-контент и иммерсивные среды',
         'Погружаем пользователей в виртуальную реальность с помощью интерактивных VR-проектов.',
         '<img class="ct-img" src="/images/content/vr.jpg" alt="VR-контент: посетители в VR-очках" loading="lazy">',
         lst=['Персонализированные VR-среды и симуляции','Производство 360°-видео: съёмка и постпродакшн','VR-кинотеатры для коллективного опыта'])
     +row('#CF6F19','Контент для инфо-панелей',
         'Разрабатываем информативный и привлекательный контент для тач-панелей, интерактивных столов и киосков. Делаем навигацию удобной, а получение информации — интуитивно понятным и увлекательным процессом.',
         facade('Контент для инфо-панелей','/images/content/infopanels.jpg','/media/content-infopanels.mp4'), rev=True)
     +row('#C12164','Адаптация контента',
         'Профессионально адаптируем существующий контент под любые форматы: архитектурные фасады, сложные LED-инсталляции, изогнутые экраны и интерактивные поверхности.',
         loop)
    )
    works=f'<div class="ct-sec" id="ct-works">{rows}</div>'

    # Финальный CTA-блок убран 10.07.2026 по просьбе пользователя:
    # он дублировал форму заявки hm-cta, которая идёт сразу за ним (#lead)

    body=(f'{rc.header()}<main class="ct-main">{hero}{feats()}{works}{ct_extra()}<section class="ct-sec" id="ct-price"><h2 class="ct-seo__h ct-rev">Стоимость</h2>{cb.render("content")}</section>{ct_faq()}</main>'
          f'<a id="lead"></a>{rc.footer()}{rc.JS}{VIDEO_JS}{REVEAL_JS}</body></html>')
    return HEAD+body

if __name__=='__main__':
    out=os.path.join(ROOT,'content'); os.makedirs(out,exist_ok=True)
    open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(build())
    print("создано: mirror/content/index.html")
