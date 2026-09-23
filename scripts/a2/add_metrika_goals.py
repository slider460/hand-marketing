#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Цели Яндекс.Метрики (71125393) на все страницы зеркала.
JS-события (создать цели типа «JavaScript-событие» в интерфейсе Метрики):
  form_start      — начали заполнять форму (первый фокус в поле, раз за страницу)
  form_submit     — отправка любой формы (hm-cta-form, lead-формы страниц)
  phone_click     — клик по ссылке tel:
  phone_copy      — скопировали номер телефона (выделением или через меню ссылки)
  email_click     — клик по ссылке mailto: (открыли почтовую программу)
  email_copy      — скопировали адрес почты (выделением или через меню ссылки)
  telegram_click  — переход в Telegram (t.me)
  whatsapp_click  — переход в WhatsApp (wa.me)
  file_download   — скачивание файла (pdf, ppt, doc, xls, zip)
  video_play      — запустили ролик сами (автозапуск без звука не считается), раз за страницу
  scroll_75       — долистали страницу до 75 %, раз за страницу
  (quiz_start / quiz_submit шлёт сам квиз на /exhibition)
Идемпотентен (маркер hm-metrika-goals): старый блок заменяется на актуальный.
Ставится только на страницы, где уже есть Метрика.
"""
import os, glob, re

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'mirror')
MARK = 'hm-metrika-goals'
OLD = re.compile(r'<script id="hm-metrika-goals">.*?</script>', re.S)

JS = """<script id="hm-metrika-goals">(function(){
var sent={};
function g(id,once){if(once){if(sent[id])return;sent[id]=1;}try{if(window.ym)ym(71125393,'reachGoal',id);}catch(e){}}
function inQuiz(el){return el&&el.closest&&el.closest('[data-quiz]');} // у квиза свои цели
document.addEventListener('submit',function(e){
 var f=e.target;if(!f||f.tagName!=='FORM'||inQuiz(f))return;
 g('form_submit');
},true);
document.addEventListener('focusin',function(e){
 var t=e.target;if(!t||!/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)||t.type==='hidden')return;
 var f=t.form||(t.closest&&t.closest('form'));if(!f||inQuiz(f))return;
 g('form_start',1);
},true);
function kind(h){
 h=(h||'').toLowerCase();
 if(h.indexOf('tel:')===0)return 'phone';
 if(h.indexOf('mailto:')===0)return 'email';
 if(/\\/\\/(www\\.)?(t\\.me|telegram\\.me)\\//.test(h))return 'telegram';
 if(/\\/\\/(wa\\.me|api\\.whatsapp\\.com)\\//.test(h))return 'whatsapp';
 if(/\\.(pdf|pptx?|docx?|xlsx?|zip)([?#]|$)/.test(h))return 'file';
 return '';
}
var CLICK={phone:'phone_click',email:'email_click',telegram:'telegram_click',whatsapp:'whatsapp_click',file:'file_download'};
function link(e){var a=e.target&&e.target.closest&&e.target.closest('a[href]');return a?kind(a.getAttribute('href')):'';}
document.addEventListener('click',function(e){var k=link(e);if(k)g(CLICK[k]);},true);
// правая кнопка или долгое нажатие на телефоне: «Скопировать адрес» из меню ссылки
document.addEventListener('contextmenu',function(e){var k=link(e);if(k==='email')g('email_copy');else if(k==='phone')g('phone_copy');},true);
document.addEventListener('copy',function(){
 var s='';try{s=String(window.getSelection()).trim();}catch(e){}
 if(/[\\w.+-]+@[\\w-]+\\.[\\w.-]+/.test(s))g('email_copy');
 else if(/^[\\s\\d()+-]+$/.test(s)&&s.replace(/\\D/g,'').length>=10)g('phone_copy');
},true);
document.addEventListener('play',function(e){
 var v=e.target;if(!v||v.tagName!=='VIDEO')return;
 var ua=navigator.userActivation;if(ua?!ua.isActive:v.muted)return;
 g('video_play',1);
},true);
window.addEventListener('scroll',function(){
 if(sent.scroll_75)return;
 var d=document.documentElement,h=d.scrollHeight-window.innerHeight;
 if(h>0&&(window.pageYOffset||d.scrollTop)/h>=0.75)g('scroll_75',1);
},{passive:true});
})();</script>"""

patched = updated = same = 0
for f in sorted(glob.glob(os.path.join(ROOT, '**', 'index*.html'), recursive=True)):
    with open(f, encoding='utf-8') as fh:
        h = fh.read()
    if MARK in h:
        new = OLD.sub(lambda m: JS, h, count=1)
        if new == h:
            same += 1
            continue
        h = new
        updated += 1
    elif 'mc.yandex.ru/metrika' in h and '</body>' in h:
        h = h.replace('</body>', JS + '</body>', 1)
        patched += 1
    else:
        continue
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(h)
print(f'Новых: {patched}, обновлено: {updated}, уже актуальны: {same}')
