#!/usr/bin/env python3
"""Генерит mirror/content/index.html — страницу услуги «Content» (мультимедийный
контент) по структуре weshow.su/services/multimedia-content: hero, 4 направления,
детальные секции с примерами (модалка поверх страницы, фасадный паттерн — до клика
грузится только постер), autoplay-луп в «Адаптации», CTA. Вместо имиджа weshow в
hero — собственная SVG-сцена в фирменных цветах (светящаяся сфера, неоновые лучи,
парящие LED-экраны). Стандартные шапка/подвал из react-chrome.py.
Видео self-host /media/*.mp4 (заливаются вручную, список в VIDEO-UPLOAD.md);
Naked Eye переиспользует уже залитый /media/stavropol-vdnh-nakedeye.mp4.
build_v1 страницу пропускает по маркеру <!--custom-page-->."""
import os, importlib.util, html as H

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
/* ------- герой: тёмная сцена с SVG-артом ------- */
.ct-hero{position:relative;overflow:hidden;background:#0E1116;color:#fff}
.ct-hero__in{position:relative;max-width:1180px;margin:0 auto;padding:88px 40px 96px;display:grid;grid-template-columns:1.05fr .95fr;gap:40px;align-items:center}
.ct-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;background:rgba(255,224,0,.1);
 box-shadow:inset 0 0 0 1px rgba(255,224,0,.35);color:#FFE000;font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;font-family:'Raleway',Arial,sans-serif}
.ct-hero h1{margin:22px 0 0;font-size:clamp(44px,6.6vw,88px);line-height:.98;font-weight:800;letter-spacing:-.025em;color:#fff}
.ct-hero__sub{margin:18px 0 0;font-size:clamp(19px,2.2vw,26px);font-weight:700;line-height:1.25;
 background:linear-gradient(92deg,#8BC34A,#FFB84D 38%,#FF5CA8 70%,#B36BE0);-webkit-background-clip:text;background-clip:text;color:transparent}
.ct-hero__lead{margin:18px 0 0;max-width:520px;font-size:17px;line-height:1.65;color:rgba(255,255,255,.82)}
.ct-hero__act{margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.ct-cta{display:inline-block;background:#FCB724;color:#14171C;font-weight:800;font-size:16px;text-decoration:none;padding:16px 42px;border-radius:30px;transition:transform .15s,box-shadow .15s;border:0;cursor:pointer}
.ct-cta:hover{transform:translateY(-2px);box-shadow:0 14px 26px -14px rgba(252,183,36,.9)}
.ct-cta_ghost{background:transparent;color:#fff;box-shadow:inset 0 0 0 2px rgba(255,255,255,.42);font-weight:700}
.ct-cta_ghost:hover{box-shadow:inset 0 0 0 2px #fff}
/* SVG-арт */
.ct-art{width:100%;max-width:560px;margin:0 auto;display:block}
@media (prefers-reduced-motion:no-preference){
 .ct-art .ray{animation:ctRay 3.6s ease-in-out infinite}
 .ct-art .ray:nth-child(2n){animation-delay:1.2s}.ct-art .ray:nth-child(3n){animation-delay:2.1s}
 @keyframes ctRay{0%,100%{opacity:.55}50%{opacity:1}}
 .ct-art .orbglow{transform-origin:340px 300px;animation:ctOrb 5s ease-in-out infinite}
 @keyframes ctOrb{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}
 .ct-art .scr{animation:ctFloat 7s ease-in-out infinite}
 .ct-art .scr_2{animation-delay:1.6s}.ct-art .scr_3{animation-delay:3.2s}
 @keyframes ctFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}}
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
.ct-loop video{width:100%;height:100%;object-fit:cover;display:block}
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
 .ct-hero__in{grid-template-columns:1fr;padding:56px 24px 64px}
 .ct-art{max-width:460px;margin-top:8px}
 .ct-sec{padding:48px 24px}
 .ct-feats{grid-template-columns:1fr 1fr}
 .ct-row{grid-template-columns:1fr;gap:24px;padding:36px 0}
 .ct-row_rev .ct-row__media{order:0}}
@media(max-width:560px){
 .ct-hero__in{padding:44px 16px 52px}
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

# SVG-сцена героя: светящаяся сфера с неоновыми лучами и парящими LED-экранами,
# фирменная палитра HM (аналог имиджа weshow, отрисован с нуля).
HERO_SVG="""<svg class="ct-art" viewBox="0 0 640 520" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Мультимедийный контент: светящаяся сфера, лучи света и LED-экраны">
<defs>
 <radialGradient id="ctOrb" cx="46%" cy="42%" r="60%">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset=".35" stop-color="#FFE000"/><stop offset=".7" stop-color="#E0427E"/><stop offset="1" stop-color="#673A7E"/>
 </radialGradient>
 <radialGradient id="ctGlow" cx="50%" cy="50%" r="50%">
  <stop offset="0" stop-color="#E0427E" stop-opacity=".55"/><stop offset="1" stop-color="#E0427E" stop-opacity="0"/>
 </radialGradient>
 <linearGradient id="ctScr1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A3040"/><stop offset="1" stop-color="#161B24"/></linearGradient>
 <linearGradient id="ctScr2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#232936"/><stop offset="1" stop-color="#121620"/></linearGradient>
 <linearGradient id="ctWave" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8BC34A"/><stop offset=".5" stop-color="#FFB84D"/><stop offset="1" stop-color="#FF5CA8"/></linearGradient>
 <filter id="ctBlur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.2"/></filter>
</defs>
<!-- звёздное поле -->
<g fill="#fff" opacity=".5">
 <circle cx="60" cy="70" r="1.4"/><circle cx="150" cy="40" r="1"/><circle cx="250" cy="90" r="1.2"/><circle cx="420" cy="50" r="1.4"/>
 <circle cx="560" cy="90" r="1"/><circle cx="80" cy="240" r="1"/><circle cx="600" cy="210" r="1.3"/><circle cx="500" cy="330" r="1"/>
 <circle cx="120" cy="430" r="1.2"/><circle cx="330" cy="60" r="1"/><circle cx="590" cy="450" r="1.2"/><circle cx="40" cy="350" r="1"/>
 <circle cx="240" cy="480" r="1.3"/><circle cx="460" cy="470" r="1"/><circle cx="380" cy="150" r="1"/>
</g>
<!-- тонкая сеть -->
<g stroke="#3A4152" stroke-width=".7" opacity=".4">
 <path d="M40 120 L220 210 L110 330 Z" fill="none"/><path d="M540 120 L430 220 L600 300" fill="none"/><path d="M200 470 L330 380 L500 440" fill="none"/>
</g>
<!-- лучи из сферы -->
<g stroke-linecap="round">
 <g class="ray"><line x1="320" y1="286" x2="70" y2="60" stroke="#FF5CA8" stroke-width="2.4"/><line x1="320" y1="286" x2="70" y2="60" stroke="#FF5CA8" stroke-width="5" opacity=".35" filter="url(#ctBlur)"/></g>
 <g class="ray"><line x1="330" y1="280" x2="330" y2="30" stroke="#B36BE0" stroke-width="2"/><line x1="330" y1="280" x2="330" y2="30" stroke="#B36BE0" stroke-width="4.6" opacity=".3" filter="url(#ctBlur)"/></g>
 <g class="ray"><line x1="350" y1="288" x2="600" y2="80" stroke="#4FB7E8" stroke-width="2.4"/><line x1="350" y1="288" x2="600" y2="80" stroke="#4FB7E8" stroke-width="5" opacity=".35" filter="url(#ctBlur)"/></g>
 <g class="ray"><line x1="352" y1="300" x2="630" y2="270" stroke="#FFB84D" stroke-width="2"/><line x1="352" y1="300" x2="630" y2="270" stroke="#FFB84D" stroke-width="4.4" opacity=".3" filter="url(#ctBlur)"/></g>
 <g class="ray"><line x1="348" y1="312" x2="610" y2="470" stroke="#FF5CA8" stroke-width="2.2"/><line x1="348" y1="312" x2="610" y2="470" stroke="#FF5CA8" stroke-width="4.8" opacity=".32" filter="url(#ctBlur)"/></g>
 <g class="ray"><line x1="332" y1="318" x2="350" y2="510" stroke="#8BC34A" stroke-width="2"/><line x1="332" y1="318" x2="350" y2="510" stroke="#8BC34A" stroke-width="4.4" opacity=".3" filter="url(#ctBlur)"/></g>
 <g class="ray"><line x1="312" y1="314" x2="90" y2="480" stroke="#B36BE0" stroke-width="2.2"/><line x1="312" y1="314" x2="90" y2="480" stroke="#B36BE0" stroke-width="4.8" opacity=".32" filter="url(#ctBlur)"/></g>
 <g class="ray"><line x1="306" y1="298" x2="20" y2="300" stroke="#FFE000" stroke-width="2"/><line x1="306" y1="298" x2="20" y2="300" stroke="#FFE000" stroke-width="4.4" opacity=".3" filter="url(#ctBlur)"/></g>
</g>
<!-- сфера -->
<circle class="orbglow" cx="330" cy="300" r="86" fill="url(#ctGlow)"/>
<circle cx="330" cy="300" r="30" fill="url(#ctOrb)"/>
<circle cx="330" cy="300" r="30" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="1"/>
<path d="M300 300 a30 30 0 0 0 60 0" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1"/>
<path d="M330 270 a30 30 0 0 1 0 60" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1"/>
<!-- экран 1: башня с абстрактным контентом -->
<g class="scr">
 <g transform="translate(96,128) skewY(-6)">
  <rect x="0" y="0" width="96" height="200" rx="10" fill="url(#ctScr1)" stroke="#4A5266" stroke-width="1"/>
  <rect x="10" y="14" width="34" height="42" rx="6" fill="#E0427E" opacity=".85"/>
  <rect x="50" y="26" width="36" height="30" rx="6" fill="#8BC34A" opacity=".8"/>
  <rect x="14" y="66" width="46" height="52" rx="8" fill="#B36BE0" opacity=".8"/>
  <rect x="52" y="96" width="32" height="40" rx="6" fill="#FFB84D" opacity=".85"/>
  <rect x="12" y="130" width="30" height="26" rx="6" fill="#FFE000" opacity=".7"/>
  <rect x="10" y="166" width="76" height="6" rx="3" fill="#fff" opacity=".18"/>
  <rect x="10" y="180" width="52" height="6" rx="3" fill="#fff" opacity=".12"/>
 </g>
</g>
<!-- экран 2: концентрические дуги -->
<g class="scr scr_2">
 <g transform="translate(400,120) skewY(5)">
  <rect x="0" y="0" width="118" height="92" rx="9" fill="url(#ctScr2)" stroke="#4A5266" stroke-width="1"/>
  <g fill="none" stroke-linecap="round">
   <path d="M38 66 a26 26 0 1 1 0 -1" stroke="#FF5CA8" stroke-width="5" opacity=".9"/>
   <path d="M52 66 a40 40 0 0 1 40 -40" stroke="#B36BE0" stroke-width="5"/>
   <path d="M66 66 a54 54 0 0 1 46 -53" stroke="#4FB7E8" stroke-width="5" opacity=".85"/>
  </g>
  <circle cx="38" cy="52" r="7" fill="#FFE000"/>
 </g>
</g>
<!-- экран 3: волновые линии -->
<g class="scr scr_3">
 <g transform="translate(468,300) skewY(-7)">
  <rect x="0" y="0" width="150" height="104" rx="9" fill="url(#ctScr2)" stroke="#4A5266" stroke-width="1"/>
  <g fill="none" stroke="url(#ctWave)" stroke-width="2.6" opacity=".9">
   <path d="M10 34 q18 -16 36 0 t36 0 t36 0 t22 0"/>
   <path d="M10 56 q18 -16 36 0 t36 0 t36 0 t22 0" opacity=".7"/>
   <path d="M10 78 q18 -16 36 0 t36 0 t36 0 t22 0" opacity=".45"/>
  </g>
  <rect x="112" y="12" width="28" height="14" rx="4" fill="#FFE000" opacity=".9"/>
 </g>
</g>
</svg>"""

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
// автолуп «Адаптации»: пауза вне вьюпорта и при prefers-reduced-motion
var lv=document.querySelector('.ct-loop video');
if(lv){
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){lv.removeAttribute('autoplay');lv.pause();}
 else if('IntersectionObserver' in window){
  new IntersectionObserver(function(es){es.forEach(function(en){
   if(en.isIntersecting){lv.play&&lv.play().catch(function(){});}else{lv.pause&&lv.pause();}
  });}).observe(lv);}
}
})();</script>"""

REVEAL_JS="""<noscript><style>.ct-rev{opacity:1!important;transform:none!important}</style></noscript>
<script>(function(){
var els=[].slice.call(document.querySelectorAll('.ct-rev'));
if(!('IntersectionObserver' in window)){els.forEach(function(n){n.classList.add('is-in');});return;}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
els.forEach(function(n,i){n.style.transitionDelay=Math.min(i%4*90,270)+'ms';io.observe(n);});
})();</script>"""

RALEWAY='<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@700&display=swap" rel="stylesheet">'

HEAD=f'''<!doctype html><html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Content — мультимедийный контент для мероприятий | Hand Marketing</title>
<meta name="description" content="Мультимедийный контент от идеи до воплощения: графическое оформление и заставки, 3D-контент и мэппинг, Naked Eye 3D, VR, контент для инфо-панелей, брендинг мероприятий и адаптация под любые форматы.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hand-marketing.ru/content/">
<meta property="og:type" content="website"><meta property="og:title" content="Content — мультимедийный контент | Hand Marketing">
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

def build():
    hero=(f'<section class="ct-hero"><div class="ct-hero__in"><div>'
          f'<span class="ct-badge">Новое поколение визуальных решений</span>'
          f'<h1>Content</h1>'
          f'<p class="ct-hero__sub">Мультимедийный контент — от идеи до воплощения</p>'
          f'<p class="ct-hero__lead">Мы создаём цифровые миры, которые оживляют ваши идеи. Передовые технологии и креативный подход для незабываемых впечатлений.</p>'
          f'<div class="ct-hero__act"><a class="ct-cta" href="#lead">Обсудить проект</a>'
          f'<a class="ct-cta ct-cta_ghost" href="#ct-works">Смотреть примеры</a></div>'
          f'</div><div>{HERO_SVG}</div></div></section>')

    duo=(f'<div class="ct-duo">'
         f'<figure>{facade("3D-контент и мэппинг: мэппинг на архитектуре","/images/content/mapping-arch.jpg","/media/content-mapping-arch.mp4")}'
         f'<figcaption class="ct-cap">Мэппинг на архитектуре</figcaption></figure>'
         f'<figure>{facade("3D-контент и мэппинг: контент для изогнутых экранов","/images/content/mapping-curved.jpg","/media/content-mapping-curved.mp4")}'
         f'<figcaption class="ct-cap">Контент для изогнутых экранов</figcaption></figure></div>')

    loop=('<div class="ct-loop"><video autoplay muted loop playsinline preload="metadata" '
          'poster="/images/content/adaptation.jpg" aria-label="Адаптация контента под изогнутый экран"><source src="/media/content-adaptation-loop.mp4" type="video/mp4"></video></div>')

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

    final=(f'<section class="ct-sec"><div class="ct-final ct-rev">'
           f'<h2>Готовы воплотить вашу идею?</h2>'
           f'<p>Свяжитесь с нами, чтобы обсудить проект — поможем создать незабываемый мультимедийный опыт для вашей аудитории.</p>'
           f'<a class="ct-cta" href="#lead">Обсудить проект</a></div></section>')

    body=(f'{rc.header()}<main class="ct-main">{hero}{feats()}{works}{final}</main>'
          f'<a id="lead"></a>{rc.footer()}{rc.JS}{VIDEO_JS}{REVEAL_JS}</body></html>')
    return HEAD+body

if __name__=='__main__':
    out=os.path.join(ROOT,'content'); os.makedirs(out,exist_ok=True)
    open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(build())
    print("создано: mirror/content/index.html")
