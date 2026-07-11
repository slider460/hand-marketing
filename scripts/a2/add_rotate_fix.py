#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Фикс развала страниц при повороте телефона. Архитектура A2: Tilda-движок
(отложенные скрипты type="td") инициализируется только если в момент загрузки
innerWidth > 640. Если страница открыта в портрете (мобильная версия .mhome),
а телефон повернули в альбомную — CSS показывает десктопные Zero-блоки,
но движок не запущен: страница разваливается.
Фикс: если старт был мобильным, при устойчивом переходе ширины за 640px —
перезагрузка страницы (движок инициализируется как надо). Обратный переход
(десктоп -> портрет) безопасен: мобильную версию рисует чистый CSS.
Ставится на страницы, где есть и .mhome, и отложенный движок (type="td").
Идемпотентен (маркер hm-rotate-fix).
"""
import os, glob

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'mirror')
MARK = 'hm-rotate-fix'

JS = """<script id="hm-rotate-fix">(function(){
if(window.innerWidth>640)return; // движок уже инициализируется штатно
var t;
function chk(){clearTimeout(t);t=setTimeout(function(){
 if(window.innerWidth>640)location.reload();
},250);}
window.addEventListener('resize',chk);
window.addEventListener('orientationchange',chk);
})();</script>"""

patched = skipped = 0
for f in sorted(glob.glob(os.path.join(ROOT, '**', 'index*.html'), recursive=True)):
    with open(f, encoding='utf-8') as fh:
        h = fh.read()
    if MARK in h:
        skipped += 1
        continue
    # ставим на все страницы с отложенным Tilda-движком (mhome не обязателен:
    # /clients и /privacy без мобильной версии страдают от того же эффекта)
    if 'type="td"' not in h or '</body>' not in h:
        continue
    h = h.replace('</body>', JS + '</body>', 1)
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(h)
    patched += 1
print(f'Пропатчено: {patched}, уже были: {skipped}')
