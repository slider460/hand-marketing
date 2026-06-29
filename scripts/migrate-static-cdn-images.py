#!/usr/bin/env python3
"""Перенести РАСТРОВЫЕ картинки из mirror/static/cdn/ -> mirror/images/cdn/, чтобы их
отдавал Apache (а не nginx напрямую) и заработала WebP-негоциация из .htaccess.
Переносятся .png/.jpg/.jpeg + их .webp. SVG/CSS/JS/шрифты и static/thb НЕ трогаем.
Ссылки в текстовых файлах переписываются static/cdn/<...>.(png|jpg|jpeg) -> images/cdn/<...>.
Идемпотентно (повторный запуск ничего не ломает)."""
import os, re, shutil

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','mirror'))
SRC=os.path.join(ROOT,'static','cdn')
DST=os.path.join(ROOT,'images','cdn')
RASTER=('.png','.jpg','.jpeg')

def move_files():
    moved=0
    for dp,_,fns in os.walk(SRC):
        for f in fns:
            low=f.lower()
            is_raster = low.endswith(RASTER)
            is_raster_webp = low.endswith('.webp') and any(low[:-5].endswith(e) for e in RASTER)
            if not (is_raster or is_raster_webp): continue
            src=os.path.join(dp,f)
            rel=os.path.relpath(src,SRC)
            dst=os.path.join(DST,rel)
            os.makedirs(os.path.dirname(dst),exist_ok=True)
            shutil.move(src,dst); moved+=1
    return moved

# безопасный класс символов (НЕ включает & ; , " ' пробел) чтобы не «перепрыгнуть»
# через &quot;-границы в JSON-галереях; case-insensitive для .JPG/.JPEG
REF=re.compile(r'static/cdn/([A-Za-z0-9][A-Za-z0-9._/-]*?\.(?:png|jpe?g))', re.IGNORECASE)
# Экранированные слеши во встроенных JS-данных Тильды: static\/cdn\/... и static\\\/cdn\\\/...
# SEP = слеш с 0..3 предшествующими бэкслешами. Меняем только static->images (разделители \1 сохраняются).
SEP=r'\\{0,3}/'
ESC=re.compile(r'static('+SEP+r'cdn'+SEP+r'(?:[A-Za-z0-9._-]|'+SEP+r')*?\.(?:png|jpe?g))', re.IGNORECASE)
def rewrite_refs():
    exts=('.html','.htm','.json','.xml','.css','.js','.txt')
    files=0; subs=0
    for dp,_,fns in os.walk(ROOT):
        for f in fns:
            if not f.lower().endswith(exts): continue
            p=os.path.join(dp,f)
            try: h=open(p,encoding='utf-8').read()
            except: continue
            new,n1=REF.subn(r'images/cdn/\1',h)
            new,n2=ESC.subn(r'images\1',new)
            if n1+n2:
                open(p,'w',encoding='utf-8').write(new); files+=1; subs+=n1+n2
    return files,subs

if __name__=='__main__':
    m=move_files()
    files,subs=rewrite_refs()
    # на всякий: остались ли ссылки на растр в static/cdn?
    left=0
    for dp,_,fns in os.walk(ROOT):
        for f in fns:
            if f.lower().endswith(('.html','.json','.css','.js','.xml','.txt')):
                try: h=open(os.path.join(dp,f),encoding='utf-8').read()
                except: continue
                left+=len(REF.findall(h))+len(ESC.findall(h))
    print(f"перенесено файлов: {m}")
    print(f"переписано ссылок: {subs} в {files} файлах")
    print(f"осталось ссылок static/cdn на растр: {left} (должно быть 0)")
