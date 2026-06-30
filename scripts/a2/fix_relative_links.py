#!/usr/bin/env python3
"""Чинит относительные nav-ссылки Тильды (href="about" и т.п.) -> абсолютные (href="/about").
Баг: без <base> такие ссылки с подстраниц (/service/, /event/...) ведут в /service/about -> 404.
Делает абсолютными ссылки на известные верхнеуровневые маршруты во всех собранных страницах. Идемпотентно."""
import os, re, glob

ROUTES=['about','service','clients','contacts','project','privacy','exhibition',
        'event','creativedesign','videoproduction','printandproduction','btl','digital','3dmapping']

def fix(h):
    n=0
    for r in ROUTES:
        # точное относительное href="route" (закрывающая кавычка сразу) -> "/route"
        new=h.replace(f'href="{r}"', f'href="/{r}"')
        n+=h.count(f'href="{r}"'); h=new
    # относительные ссылки на кейсы вида href="event/eaton" (сегмент-маршрут без слеша)
    h2=re.sub(r'href="('+'|'.join(['event','video','creative','digital','3d'])+r')/', r'href="/\1/', h)
    return h2, n

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','mirror'))
files=glob.glob(os.path.join(ROOT,'**','index-a2.html'),recursive=True)
files+=glob.glob(os.path.join(ROOT,'portfolio','*','index.html'))
changed=0; total=0
for p in files:
    h=open(p,encoding='utf-8').read(); o=h
    h,n=fix(h)
    if h!=o: open(p,'w',encoding='utf-8').write(h); changed+=1; total+=n
print(f"страниц исправлено: {changed}, относительных nav-ссылок -> абсолютных: {total}")
# контроль: остались ли относительные href на наши маршруты?
left=0
for p in files:
    h=open(p,encoding='utf-8').read()
    for r in ROUTES: left+=h.count(f'href="{r}"')
print("осталось относительных (должно быть 0):", left)
