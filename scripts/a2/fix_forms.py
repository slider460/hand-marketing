#!/usr/bin/env python3
"""Чинит формы в уже собранных страницах: меняет старый FORM_JS на новый (перехват КЛИКА в
capture-фазе, опережает Tilda lib-forms) и снимает Tilda-маркер js-form-proccess.
Идемпотентно. Цель — все mirror/**/index-a2.html (React-страницы /portfolio с id=root пропускаем —
у них своя форма .hm-cta-form, Tilda там нет)."""
import os, re, glob

NEW_FORM_JS='''<script>(function(){function msg(f,t,ok){var d=document.createElement('div');d.textContent=t;d.style.cssText='font:600 16px/1.45 Montserrat,Arial,sans-serif;padding:14px 0;color:'+(ok?'#1b8a3a':'#c0392b');(f.parentNode||document.body).insertBefore(d,f.nextSibling);}
function isOur(f){return f&&f.classList&&(f.classList.contains('mh-f')||f.classList.contains('t-form'));}
function send(f){if(f.__sending)return;var tel=f.querySelector('input[type=tel],input[name=phone],input[name=Phone],input[name=tel],input[name=Tel]');if(tel&&tel.value.replace(/\\D/g,'').length<6){tel.focus();tel.style.borderColor='#c0392b';return;}f.__sending=true;var b=f.querySelector('button,input[type=submit]');var o=b?(b.textContent||b.value):'';if(b){b.disabled=true;if('textContent' in b&&b.tagName==='BUTTON')b.textContent='Отправляем…';else b.value='Отправляем…';}
fetch('/api/lead.php',{method:'POST',body:new FormData(f)}).then(function(r){return r.json();}).then(function(j){if(!j||!j.success)throw 0;f.style.display='none';msg(f,'Спасибо! Мы свяжемся с вами в ближайшее время.',true);}).catch(function(){f.__sending=false;if(b){b.disabled=false;if(b.tagName==='BUTTON')b.textContent=o;else b.value=o;}msg(f,'Не удалось отправить. Позвоните: +7 495 580 75 37',false);});}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('button,input[type=submit],.t-submit');if(!b)return;var f=b.closest('form');if(!isOur(f))return;e.preventDefault();e.stopImmediatePropagation();send(f);},true);
document.addEventListener('submit',function(e){var f=e.target;if(!isOur(f))return;e.preventDefault();e.stopImmediatePropagation();send(f);},true);})();
(function(){function fb(){var ls=document.querySelectorAll('link[href*="blackhole.invalid.com"]');for(var i=0;i<ls.length;i++)ls[i].href='/static/cdn/css/lib-zero-form-errorbox.min.css';}var t=0,iv=setInterval(function(){fb();if(++t>20)clearInterval(iv);},300);fb();})();</script>'''

OLD_RE=re.compile(r"<script>\(function\(\)\{function msg\(f,t,ok\).*?</script>", re.S)

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','mirror'))
changed=0; jfp=0
for p in glob.glob(os.path.join(ROOT,'**','index-a2.html'),recursive=True):
    h=open(p,encoding='utf-8').read()
    if 'id="root"' in h: continue  # React-шеллы не трогаем
    o=h
    h,_=OLD_RE.subn(lambda m: NEW_FORM_JS, h)  # lambda -> замена литеральна (без интерпретации \D)
    if ' js-form-proccess' in h:
        h=h.replace(' js-form-proccess',''); jfp+=1
    if h!=o:
        open(p,'w',encoding='utf-8').write(h); changed+=1
print(f"FORM_JS обновлён + js-form-proccess снят: {changed} файлов (с js-form-proccess было {jfp})")
# контроль
miss=[p for p in glob.glob(os.path.join(ROOT,'**','index-a2.html'),recursive=True)
      if 'id="root"' not in open(p,encoding='utf-8').read()
      and "e.target.closest('button" not in open(p,encoding='utf-8').read()]
print("без нового обработчика осталось:",len(miss), miss[:3])
