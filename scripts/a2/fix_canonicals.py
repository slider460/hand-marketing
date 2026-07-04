#!/usr/bin/env python3
"""Абсолютные canonical на всех страницах: <link rel="canonical" href="/route">
-> href="https://hand-marketing.ru/route/". URL выводится из ПУТИ файла
(mirror/<route>/index*.html -> /<route>/), старый href сверяется с маршрутом —
при расхождении файл пропускается с предупреждением. Идемпотентен."""
import glob, os, re

ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','mirror'))
BASE='https://hand-marketing.ru'
PAT=re.compile(r'<link rel="canonical" href="([^"]*)"\s*/?>')

def route_of(path):
    rel=os.path.relpath(os.path.dirname(path),ROOT).replace(os.sep,'/')
    return '/' if rel=='.' else f'/{rel}/'

changed=skipped=already=0
for p in sorted(glob.glob(os.path.join(ROOT,'**','index*.html'),recursive=True)):
    if os.path.basename(p) not in ('index.html','index-a2.html'): continue
    h=open(p,encoding='utf-8',errors='replace').read()
    m=PAT.search(h)
    if not m: continue
    href=m.group(1); route=route_of(p)
    want=BASE+route
    if href==want: already+=1; continue
    # сверка: старый относительный href должен соответствовать маршруту файла
    norm=href if href.endswith('/') else href+'/'
    if norm not in (route, BASE+route):
        print(f'ПРОПУСК (href "{href}" != маршрут "{route}"): {p}'); skipped+=1; continue
    h=h[:m.start()]+f'<link rel="canonical" href="{want}">'+h[m.end():]
    open(p,'w',encoding='utf-8').write(h); changed+=1

print(f'изменено: {changed}, уже абсолютные: {already}, пропущено: {skipped}')
