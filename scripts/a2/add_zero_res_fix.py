#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Фикс десктопной вёрстки Zero-блоков на мобильном.

Движок Tilda (t396) один раз замеряет ширину окна и по ней выбирает брейкпоинт
Zero-блоков (320/480/640/960/1200). Замер идёт во время парсинга страницы, и
если в этот момент что-то ещё не разложено (у нас это футер-артборд, элементы
которого до инициализации занимают ~1220px), layout viewport на мобильном
растягивается под контент. Движок видит «1169px», выбирает брейкпоинт 960 и
раскладывает кейс по десктопной сетке: заголовки и абзацы уезжают за края
экрана, текст обрезан слева и справа.

Гонка по своей природе плавающая: на /video/eaton/ она воспроизводится всегда,
на соседних кейсах с тем же футером - нет. Поэтому страховка ставится на все
страницы с Zero-блоками.

Фикс: после load сверяем закэшированную ширину с фактической. Если замер был
верным, не делаем ничего вообще. Если ширина разошлась, пересчитываем артборды
штатным t396_doResize - тем же путём, каким движок отрабатывает поворот экрана.

Идемпотентен (маркер hm-zero-res-fix).
"""
import os, glob

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'mirror')
MARK = 'hm-zero-res-fix'

JS = """<script id="hm-zero-res-fix">(function(){
function fix(){
 var tn=window.tn;
 if(!tn||!window.t396__updateWindowDimensions||!window.t396_doResize)return;
 var was=tn.window_width_css;
 window.t396__updateWindowDimensions();
 if(tn.window_width_css===was)return; // замер был верный, вёрстку не трогаем
 Object.keys(tn).forEach(function(k){
  if(k.indexOf('ab')!==0||k==='ab_fields'||!tn[k]||!tn[k].screens)return;
  try{window.t396_doResize(k.slice(2),true);}catch(e){}
 });
}
window.addEventListener('load',function(){fix();setTimeout(fix,300);});
})();</script>"""

patched = skipped = 0
for f in sorted(glob.glob(os.path.join(ROOT, '**', 'index*.html'), recursive=True)):
    with open(f, encoding='utf-8') as fh:
        h = fh.read()
    if MARK in h:
        skipped += 1
        continue
    # только страницы с Zero-блоками (t396) и нормальным закрытием body
    if 't396_init' not in h or '</body>' not in h:
        continue
    h = h.replace('</body>', JS + '</body>', 1)
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(h)
    patched += 1
print(f'Пропатчено: {patched}, уже были: {skipped}')
