#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Цели Яндекс.Метрики (71125393) на все страницы зеркала.
JS-события (создать цели типа «JavaScript-событие» в интерфейсе Метрики):
  form_submit — отправка любой формы (hm-cta-form, lead-формы страниц)
  phone_click — клик по ссылке tel:
  email_click — клик по ссылке mailto:
  (quiz_start / quiz_submit шлёт сам квиз на /exhibition)
Идемпотентен (маркер hm-metrika-goals). Ставится только на страницы, где уже есть Метрика.
"""
import os, glob

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'mirror')
MARK = 'hm-metrika-goals'

JS = """<script id="hm-metrika-goals">(function(){
function g(id){try{if(window.ym)ym(71125393,'reachGoal',id);}catch(e){}}
document.addEventListener('submit',function(e){
 var f=e.target;if(!f||f.tagName!=='FORM')return;
 if(f.closest&&f.closest('[data-quiz]'))return; // у квиза свои цели
 g('form_submit');
},true);
document.addEventListener('click',function(e){
 var a=e.target.closest&&e.target.closest('a[href^="tel:"],a[href^="mailto:"]');
 if(!a)return;
 g(a.getAttribute('href').indexOf('tel:')===0?'phone_click':'email_click');
},true);
})();</script>"""

patched = skipped = 0
for f in sorted(glob.glob(os.path.join(ROOT, '**', 'index*.html'), recursive=True)):
    with open(f, encoding='utf-8') as fh:
        h = fh.read()
    if MARK in h:
        skipped += 1
        continue
    if 'mc.yandex.ru/metrika' not in h or '</body>' not in h:
        continue
    h = h.replace('</body>', JS + '</body>', 1)
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(h)
    patched += 1
print(f'Пропатчено: {patched}, уже были: {skipped}')
