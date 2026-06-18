#!/usr/bin/env python3
"""Обложки каталога samara-exhibition / samara-vdnh в нативном стиле (477x396):
круглое фото + 4 кубика HM (спрайты из обложки EATON) + крупная плашка."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
W,H=477,396; CX,CY,R=238,198,184
def font(sz,w='ExtraBold'):
    f=ImageFont.truetype('/tmp/fonts/Montserrat.ttf',sz)
    try: f.set_variation_by_name(w)
    except: pass
    return f
# извлекаем 4 кубика-спрайта из EATON по их bbox
E=Image.open('mirror/static/cdn/as6135-3563-4735-a365-643234376439/icons-112.png').convert('RGBA')
ea=np.array(E)
CUBES=[]
for (x0,y0,x1,y1) in [(15,12,160,134),(316,25,444,134),(13,262,160,373),(316,262,450,383)]:
    spr=E.crop((x0,y0,x1,y1))
    CUBES.append((spr,x0,y0))
def make(photo,focus,band,lines,out,sz=46):
    base=Image.new('RGBA',(W,H),(0,0,0,0))
    im=Image.open(photo).convert('RGB'); w,h=im.size; side=min(w,h)
    left=int((w-side)*focus); top=(h-side)//2
    ph=im.crop((left,top,left+side,top+side)).resize((2*R,2*R),Image.LANCZOS)
    m=Image.new('L',(2*R,2*R),0); ImageDraw.Draw(m).ellipse([0,0,2*R,2*R],fill=255)
    base.paste(ph,(CX-R,CY-R),m)
    for spr,x0,y0 in CUBES: base.alpha_composite(spr,(x0,y0))
    d=ImageDraw.Draw(base); f=font(sz); lh=int(sz*1.0)
    while max(d.textlength(t,font=f) for t in lines)>W-78 and sz>28:
        sz-=2; f=font(sz); lh=int(sz*1.0)
    total=lh*len(lines); by0=CY-R+40
    mw=max(d.textlength(t,font=f) for t in lines); padx=22
    d.rounded_rectangle([CX-mw/2-padx,by0-12,CX+mw/2+padx,by0+total+10],14,fill=band)
    y=by0
    for t in lines:
        tw=d.textlength(t,font=f); d.text((CX-tw/2,y),t,font=f,fill=(255,255,255)); y+=lh
    os.makedirs(os.path.dirname(out),exist_ok=True); base.save(out,'PNG'); print('saved',out)
make('mirror/portfolio/samara-exhibition/photos/Ekran_parus.jpg',0.30,(94,178,46),
     ['ВЫСТАВКА','«САМАРА»'],'mirror/static/cdn/custom-samara-exhibition/cover-main.png',48)
make('mirror/portfolio/samara-vdnh/Card_Samara_stend.jpg',0.5,(196,38,46),
     ['СТЕНД САМАРСКОЙ','ОБЛАСТИ'],'mirror/static/cdn/custom-samara-vdnh/cover-main.png',40)
