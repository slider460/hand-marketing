#!/usr/bin/env python3
"""Впрыснуть Яндекс.Метрику (счётчик 71125393) в уже собранные страницы.
Идемпотентно: пропускает, где счётчик уже есть. Цель — все index-a2.html (деплой-источники)
+ React-шеллы portfolio/*/index.html. Для будущих Tilda-сборок Метрика уже в build_v1.py."""
import os, glob
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','mirror')
ROOT=os.path.abspath(ROOT)
M='<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'
targets=set(glob.glob(os.path.join(ROOT,'**','index-a2.html'),recursive=True))
targets|=set(glob.glob(os.path.join(ROOT,'portfolio','*','index.html')))
done=skip=0
for p in sorted(targets):
    h=open(p,encoding='utf-8').read()
    if 'ym(71125393' in h: skip+=1; continue
    if '</head>' not in h: skip+=1; continue
    h=h.replace('</head>', M+'</head>', 1)
    open(p,'w',encoding='utf-8').write(h); done+=1
print(f"Метрика добавлена: {done} | пропущено (уже есть/нет head): {skip} | всего целей: {len(targets)}")
