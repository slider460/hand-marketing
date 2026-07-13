#!/usr/bin/env python3
"""Привести шапку/подвал React-кейсов (/portfolio/*) к единому виду с Tilda-страницами.
Лёгкая самодостаточная копия (свой CSS, без Tilda-CSS). Прячет родные React header/footer/CTA,
вставляет белую шапку (куб-логотип + меню + телефон) и подвал (фиолетовая форма + тёмный футер).
Идемпотентно. Цель — index-a2.html (деплой-источник) и index.html в mirror/portfolio/*."""
import os, glob, re

LOGO   = "/static/cdn/as3937-3563-4839-b138-383963656435/pizdapattrtn-63.svg"  # цветной куб HM
SBER   = "/images/lib/as6562-3737-4062-a266-336439646532/sberkorus.png"  # перенесён миграцией static/cdn->images/lib
PHONE_T= "+74955807537"; PHONE="+7 495 580 75 37"; MAIL="info@hand-marketing.ru"
TG     = "https://t.me/narodetskii"
WA     = "https://wa.me/79859998783"
YT     = "https://youtube.com/channel/UCKBNvpFhrJXQjzZdTnIFYxw"
NAV    = [("О нас","/about"),("Услуги","/service"),("Проекты","/project"),
          ("Клиенты","/clients"),("Контакты","/contacts")]

FONT = '<link href="/fonts/montserrat.css" rel="stylesheet">'  # self-host, см. mirror/fonts/

CSS = """<style id="hm-chrome-css">
/* спрятать родные шапку/подвал React-кейса. .hm-topbar — шапка React (div, потомок body, ВНЕ #root) */
#root header,#root footer{display:none!important}
body>.hm-topbar,.hm-topbar{display:none!important}
/* React-CTA внизу кейса (синий/зелёный градиент с кнопкой «Обсудить проект») — */
/* заменён нашей фиолетовой формой; скрытие основным образом делает JS по тексту кнопки */
#root section.from-blue-700,#root section.from-emerald-600{display:none!important}
.hm-chrome,.hm-chrome *{box-sizing:border-box}
.hm-chrome{font-family:'Montserrat',-apple-system,Arial,sans-serif}
/* ШАПКА */
.hm-hdr{position:sticky;top:0;z-index:1000;background:#fff;border-bottom:1px solid rgba(20,23,28,.08);
  display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:18px;height:80px;padding:0 40px}
.hm-hdr__nav{display:flex;align-items:center;gap:34px}
.hm-hdr__nav.r{justify-content:flex-end}
.hm-hdr a{color:#14171C;text-decoration:none}
.hm-hdr__nav a{font-weight:700;font-size:16px;white-space:nowrap;transition:opacity .15s}
.hm-hdr__nav a:hover{opacity:.6}
.hm-hdr__logo{display:flex;justify-content:center}
.hm-hdr__logo img{height:54px;width:auto;display:block}
.hm-hdr__contacts{display:flex;flex-direction:column;align-items:flex-end;margin-left:18px;line-height:1.25}
.hm-hdr__contacts .ph{font-weight:800;font-size:17px;color:#14171C}
.hm-hdr__contacts .em{font-size:13px;color:#6A7078}
/* ПОДВАЛ — фиолетовая форма */
.hm-cta{background:#77449E;color:#fff;padding:62px 40px}
.hm-cta__in{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}
.hm-cta h2{font-size:40px;font-weight:800;line-height:1.05;margin:0 0 14px}
.hm-cta p{margin:0;font-size:18px;color:rgba(255,255,255,.85)}
.hm-cta__consent{margin-top:16px;font-size:12px;color:rgba(255,255,255,.7)}
.hm-cta__consent a{color:#fff}
.hm-cta form{display:flex;flex-direction:column;gap:14px}
.hm-cta input{height:56px;border:0;border-radius:30px;padding:0 26px;font:500 16px Montserrat,Arial,sans-serif;color:#14171C}
.hm-cta button{align-self:flex-start;height:54px;border:0;border-radius:30px;padding:0 42px;cursor:pointer;
  background:#FCB724;color:#14171C;font:800 16px Montserrat,Arial,sans-serif;transition:transform .15s}
.hm-cta button:hover{transform:translateY(-2px)}
.hm-cta__msg{font-weight:700;padding:8px 0}
/* ПОДВАЛ — тёмный футер */
.hm-foot{background:#242424;color:#cfd2d6;padding:42px 40px 30px}
.hm-foot__in{max-width:1080px;margin:0 auto}
.hm-foot__nav{display:flex;flex-wrap:wrap;gap:30px;padding-bottom:22px;border-bottom:2px solid #FFE000}
.hm-foot__nav a{color:#fff;text-decoration:none;font-weight:700;font-size:16px}
.hm-foot__nav a:hover{color:#FFE000}
.hm-foot__cols{display:grid;grid-template-columns:1fr 1fr 1fr;gap:30px;padding-top:26px;font-size:13px;line-height:1.6}
.hm-foot a{color:#cfd2d6}
.hm-foot__c .ph{display:block;font-weight:800;font-size:17px;color:#fff;margin-bottom:4px}
.hm-foot__soc{display:flex;gap:12px;margin-top:14px}
.hm-foot__soc a{display:inline-flex;width:34px;height:34px;border-radius:50%;background:#3a3a3a;align-items:center;justify-content:center}
.hm-foot__soc svg{width:18px;height:18px;fill:#fff}
.hm-foot__sber{display:flex;align-items:center;gap:8px;margin-top:10px}
.hm-foot__sber img{height:20px;width:auto;filter:brightness(0) invert(1);opacity:.85}
.hm-foot__cp{margin-top:22px;font-size:12px;color:#8a8f96}
@media(max-width:860px){
  .hm-hdr{grid-template-columns:auto 1fr;height:64px;padding:0 16px}
  .hm-hdr__nav.l{display:none}
  .hm-hdr__nav.r>a,.hm-hdr__contacts .em{display:none}  /* скрыть пункты меню, оставить телефон */
  .hm-hdr__logo{justify-content:flex-start}
  .hm-hdr__logo img{height:40px}
  .hm-hdr__contacts{margin-left:0}
  .hm-cta{padding:40px 18px}.hm-cta__in{grid-template-columns:1fr;gap:24px}.hm-cta h2{font-size:28px}
  .hm-foot{padding:30px 18px}.hm-foot__cols{grid-template-columns:1fr;gap:20px}
}

/* === TILDA_HDR_CSS: шапка — точная реплика Tilda-шапки сайта (rec237851314) ===
   Координаты сняты с движка: высота 140, сетка 1200/960, Raleway 700 20px #000,
   лого 90px по центру окна, телефон 20px + почта 14px правым краем, НЕ sticky.
   Только десктоп >=861px — мобильная компакт-шапка остаётся как есть. */
body{margin:0}
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
</style>"""

def header():
    left = "".join(f'<a href="{h}">{t}</a>' for t,h in NAV[:3])
    right= "".join(f'<a href="{h}">{t}</a>' for t,h in NAV[3:])
    return ('<div class="hm-chrome hm-hdr" role="banner">'
      f'<nav class="hm-hdr__nav l">{left}</nav>'
      f'<a class="hm-hdr__logo" href="/" aria-label="Hand Marketing"><img src="{LOGO}" alt="Hand Marketing"></a>'
      f'<nav class="hm-hdr__nav r">{right}'
      f'<span class="hm-hdr__contacts"><a class="ph" href="tel:{PHONE_T}">{PHONE}</a>'
      f'<a class="em" href="mailto:{MAIL}">{MAIL}</a></span></nav></div>')

TG_SVG='<svg viewBox="0 0 24 24"><path d="M9.8 16.6l-.4 4c.5 0 .8-.2 1-.5l2.5-2.3 5 3.7c.9.5 1.6.2 1.8-.8l3.3-15.3c.3-1.2-.5-1.7-1.3-1.4L1.6 10c-1.2.5-1.2 1.1-.2 1.4l5 1.6L18 5.7c.5-.3 1-.2.6.2"/></svg>'
WA_SVG='<svg viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.817 11.817 0 018.413 3.488 11.824 11.824 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884a9.87 9.87 0 001.51 5.26l-.999 3.648 3.978-1.607zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>'
YT_SVG='<svg viewBox="0 0 24 24"><path d="M23 7.5a3 3 0 00-2.1-2.1C19 5 12 5 12 5s-7 0-8.9.4A3 3 0 001 7.5 31 31 0 001 12a31 31 0 00.1 4.5 3 3 0 002.1 2.1C5 19 12 19 12 19s7 0 8.9-.4a3 3 0 002.1-2.1A31 31 0 0023 12a31 31 0 00-.1-4.5zM10 15V9l5 3z"/></svg>'

def footer():
    nav = "".join(f'<a href="{h}">{t}</a>' for t,h in NAV)
    return ('<div class="hm-chrome">'
      # фиолетовая форма
      '<section class="hm-cta"><div class="hm-cta__in">'
      '<div><h2>Давайте сделаем проект вместе?</h2>'
      '<p>Отправьте свои данные и мы вам перезвоним</p>'
      '<div class="hm-cta__consent">Нажимая на кнопку, вы даёте согласие на обработку '
      '<a href="/privacy">своих персональных данных</a></div></div>'
      '<form class="hm-cta-form" novalidate>'
      '<input type="tel" name="phone" placeholder="+X XXX XXX XX XX" required>'
      '<input type="text" name="name" placeholder="Имя">'
      '<button type="submit">отправить</button></form>'
      '</div></section>'
      # тёмный футер (div, не <footer>, чтобы правило скрытия React-футера не задело)
      '<div class="hm-foot" role="contentinfo"><div class="hm-foot__in">'
      f'<nav class="hm-foot__nav">{nav}</nav>'
      '<div class="hm-foot__cols">'
      f'<div class="hm-foot__c"><a class="ph" href="tel:{PHONE_T}">{PHONE}</a>'
      f'<a href="mailto:{MAIL}">{MAIL}</a>'
      f'<div class="hm-foot__soc"><a href="{TG}" target="_blank" rel="noopener" aria-label="Telegram">{TG_SVG}</a>'
      f'<a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a>'
      f'<a href="{YT}" target="_blank" rel="noopener" aria-label="YouTube">{YT_SVG}</a></div></div>'
      '<div>© 2026 ООО «Хэнд-маркетинг»<br>ИНН 7709931482 КПП 770901001<br>ОГРН 1137746525608<br>'
      '<a href="/privacy">Политика конфиденциальности</a></div>'
      '<div>Использование материалов Hand Marketing разрешено только с согласия правообладателя'
      f'<div class="hm-foot__sber"><img src="{SBER}" alt="СберКорус"></div></div>'
      '</div>'
      '<div class="hm-foot__cp">2012 — 2026 Hand Marketing</div>'
      '</div></div></div>')

JS = """<script>(function(){
// убрать CTA «Готовы к совместному проекту» (заменён фиолетовой формой)
function hideCTA(){var n=[].slice.call(document.querySelectorAll('#root section,#root div'));
 n.forEach(function(e){var t=e.textContent||'';if(/Обсудить проект/i.test(t)&&t.length<500&&e.style.display!=='none')e.style.display='none';});}
// форма -> /api/lead.php
function msg(f,t,ok){var d=document.createElement('div');d.className='hm-cta__msg';d.textContent=t;d.style.color=ok?'#fff':'#FFE0E0';f.parentNode.insertBefore(d,f.nextSibling);}
document.addEventListener('submit',function(e){var f=e.target;if(!f.classList||!f.classList.contains('hm-cta-form'))return;e.preventDefault();
 var tel=f.querySelector('input[type=tel]');if(tel&&tel.value.replace(/\\D/g,'').length<6){tel.focus();return;}
 var b=f.querySelector('button');if(b){b.disabled=true;b.textContent='Отправляем…';}
 fetch('/api/lead.php',{method:'POST',body:new FormData(f)}).then(function(r){return r.json();}).then(function(j){if(!j||!j.success)throw 0;f.style.display='none';msg(f,'Спасибо! Мы свяжемся с вами в ближайшее время.',true);}).catch(function(){if(b){b.disabled=false;b.textContent='отправить';}msg(f,'Не удалось отправить. Позвоните: +7 495 580 75 37',false);});});
var t=0,iv=setInterval(function(){hideCTA();if(++t>40)clearInterval(iv);},300);
if(window.MutationObserver)new MutationObserver(hideCTA).observe(document.documentElement,{childList:true,subtree:true});
})();</script>"""

def inject(p):
    h=open(p,encoding='utf-8').read()
    if 'hm-chrome-css' in h: return False
    head_add = FONT+CSS
    h = h.replace('</head>', head_add+'</head>', 1)
    # шапку — сразу после <body>, футер+JS — перед </body>
    h = re.sub(r'(<body[^>]*>)', lambda m:m.group(1)+header(), h, count=1)
    h = h.replace('</body>', footer()+JS+'</body>', 1)
    open(p,'w',encoding='utf-8').write(h); return True

if __name__=='__main__':
    ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','mirror'))
    targets=glob.glob(os.path.join(ROOT,'portfolio','*','index-a2.html'))+\
            glob.glob(os.path.join(ROOT,'portfolio','*','index.html'))
    done=0
    for t in sorted(targets):
        if inject(t): print("chrome+",t.replace(ROOT,'mirror')); done+=1
    print("изменено:",done,"из",len(targets))
