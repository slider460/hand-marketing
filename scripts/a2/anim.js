/* A2 анимации (без движка Тильды): мышь+скролл парралакс, появление при скролле (stagger), слайдер, «загрузить ещё» */
(function(){
 var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
 /* 1. ПАРРАЛАКС от мыши */
 if(!RM){ var mEls=[].slice.call(document.querySelectorAll('[data-animate-prx="mouse"]'));
  mEls.forEach(function(e){e._dx=parseFloat(e.getAttribute('data-animate-prx-dx'))||0;e._dy=parseFloat(e.getAttribute('data-animate-prx-dy'))||0;e.style.transition='translate .3s cubic-bezier(.16,1,.3,1)';});
  if(mEls.length){var raf=0;addEventListener('mousemove',function(ev){if(raf)return;raf=requestAnimationFrame(function(){raf=0;var nx=(ev.clientX/innerWidth-0.5)*2,ny=(ev.clientY/innerHeight-0.5)*2;for(var i=0;i<mEls.length;i++){var e=mEls[i];e.style.translate=(nx*e._dx).toFixed(1)+'px '+(ny*e._dy).toFixed(1)+'px';}});},{passive:true});}
 }
 /* 2. ПАРРАЛАКС от вертикального скролла */
 if(!RM){ var sEls=[].slice.call(document.querySelectorAll('[data-animate-prx="scroll"]'));
  sEls.forEach(function(e){e._s=parseFloat(e.getAttribute('data-animate-prx-s'))||0;e._ty=0;e.style.transition='translate .12s linear';e.style.willChange='translate';});
  if(sEls.length){var last=-1;function tick(){var y=pageYOffset;if(y!==last){last=y;var vh=innerHeight;for(var i=0;i<sEls.length;i++){var e=sEls[i];var r=e.getBoundingClientRect();if(r.height){var center=(r.top-e._ty)+r.height/2;var prog=((vh/2)-center)/vh;e._ty=prog*e._s*0.5;e.style.translate='0px '+e._ty.toFixed(1)+'px';}}}requestAnimationFrame(tick);}requestAnimationFrame(tick);}
 }
 /* 3. ПОЯВЛЕНИЕ при скролле (intoview) со stagger; объекты-парралакс пропускаем (видны сразу) */
 if(!RM && 'IntersectionObserver'in window){
  var items=[].slice.call(document.querySelectorAll('[data-animate-sbs-event="intoview"]')).filter(function(e){return !e.hasAttribute('data-animate-prx');});
  var cnt={};
  items.forEach(function(e){var rec=e.closest('.t-rec');var key=rec?rec.id:'x';cnt[key]=(cnt[key]||0);var d=Math.min(cnt[key],9)*0.09;cnt[key]++;e.style.setProperty('opacity','0','important');e.style.setProperty('transform','translateY(26px)','important');e.style.setProperty('transition','opacity .6s ease '+d+'s, transform .6s cubic-bezier(.16,1,.3,1) '+d+'s','important');});
  var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){var el=en.target;el.style.setProperty('opacity','1','important');el.style.setProperty('transform','none','important');io.unobserve(el);}});},{threshold:0.12,rootMargin:'0px 0px -6% 0px'});
  items.forEach(function(e){io.observe(e);});
 }
 /* 4. СЛАЙДЕР галерей */
 function initSlds(){document.querySelectorAll('.t-slds').forEach(function(sl){if(sl._a2)return;var items=[].slice.call(sl.querySelectorAll('.t-slds__item'));if(items.length<2)return;sl._a2=1;var main=sl.querySelector('.t-slds__main');if(main)main.style.position='relative';items.forEach(function(it){it.style.position='absolute';it.style.top='0';it.style.left='0';it.style.right='0';it.style.margin='auto';it.style.transition='opacity .4s ease';});var bullets=[].slice.call(sl.querySelectorAll('.t-slds__bullet'));var idx=items.findIndex(function(it){return it.style.opacity!=='0'&&getComputedStyle(it).opacity!=='0';});if(idx<0)idx=0;function show(i){idx=(i+items.length)%items.length;items.forEach(function(it,j){it.style.opacity=j===idx?'1':'0';it.style.zIndex=j===idx?'2':'1';});if(bullets.length)bullets.forEach(function(b,j){b.classList.toggle('t-slds__bullet_active',j===idx%bullets.length);});}sl.querySelectorAll('.t-slds__arrow-left').forEach(function(a){a.style.cursor='pointer';a.addEventListener('click',function(e){e.preventDefault();show(idx-1);});});sl.querySelectorAll('.t-slds__arrow-right').forEach(function(a){a.style.cursor='pointer';a.addEventListener('click',function(e){e.preventDefault();show(idx+1);});});bullets.forEach(function(b,j){b.style.cursor='pointer';b.addEventListener('click',function(){show(j);});});show(idx);});}
 /* 5. ЗАГРУЗИТЬ ЕЩЁ — кейсы по 8, ТОЛЬКО на главной; на остальных все сразу */
 function isHome(){return location.pathname.replace(/index(-a2)?\.html$/,'').replace(/\/+$/,'')==='';}
 function initLoadMore(){if(!isHome())return;var cards=[].slice.call(document.querySelectorAll('.t-store__card'));if(cards.length<=8)return;var box=cards[0].parentNode;var STEP=8,shown=8;function apply(){cards.forEach(function(c,i){c.style.display=i<shown?'':'none';});btn.style.display=shown>=cards.length?'none':'';}
  var btn=document.createElement('button');btn.textContent='Загрузить ещё';btn.style.cssText='display:block;margin:30px auto;padding:14px 38px;font:700 16px Montserrat,Arial,sans-serif;color:#fff;background:#000;border:0;border-radius:30px;cursor:pointer';btn.addEventListener('click',function(){shown+=STEP;apply();});box.parentNode.insertBefore(btn,box.nextSibling);apply();}
 function boot(){initSlds();initLoadMore();}
 if(document.readyState!=='loading')boot();else document.addEventListener('DOMContentLoaded',boot);
})();
