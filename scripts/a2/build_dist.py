import os, shutil
SRC='/Users/aleksandrnarodetskii/Downloads/hand-marketing-react/mirror'
DIST='/Users/aleksandrnarodetskii/Downloads/hand-marketing-react/dist'
if os.path.islink(DIST) or os.path.isfile(DIST): os.remove(DIST)
if os.path.exists(DIST): shutil.rmtree(DIST)
os.makedirs(DIST)
def has_page(d):
    for dp,_,fns in os.walk(d):
        if 'index-a2.html' in fns: return True
    return False
def build(srcdir,dstdir):
    os.makedirs(dstdir,exist_ok=True)
    if 'index-a2.html' in os.listdir(srcdir):
        shutil.copyfile(os.path.join(srcdir,'index-a2.html'),os.path.join(dstdir,'index.html'))
    for name in os.listdir(srcdir):
        if name in ('index.html','index-a2.html'): continue
        s=os.path.join(srcdir,name); d=os.path.join(dstdir,name)
        if os.path.isdir(s):
            if has_page(s): build(s,d)
            else: os.symlink(s,d)
        else: os.symlink(s,d)
build(SRC,DIST)
# /media — ролики из корневой папки media/ (для локального превью видео)
import os as _o2
_md=_o2.path.join(_o2.path.dirname(SRC),'media')
if _o2.path.exists(_md) and not _o2.path.exists(_o2.path.join(DIST,'media')): _o2.symlink(_md,_o2.path.join(DIST,'media'))
# кейс-картинки из public/assets
import os as _o
_pa=_o.path.join(_o.path.dirname(SRC),'public','assets')
if _o.path.exists(_pa) and not _o.path.exists(_o.path.join(DIST,'case-assets')): _o.symlink(_pa,_o.path.join(DIST,'case-assets'))
print('dist rebuilt')
