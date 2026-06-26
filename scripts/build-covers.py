#!/usr/bin/env python3
"""Обложки каталога samara-exhibition / samara-vdnh (477x396) в нативном стиле:
круглое фото + кубики HM (из EATON) + крупная плашка. У каждой обложки СВОЯ
расстановка кубиков (углы + отражения), чтобы края не были одинаковыми."""
from PIL import Image, ImageDraw, ImageFont
import os
W,H=477,396; CX,CY,R=238,198,184
_FONT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts','Montserrat.ttf')
def font(sz,w='ExtraBold'):
    f=ImageFont.truetype(_FONT,sz)
    try: f.set_variation_by_name(w)
    except: pass
    return f
E=Image.open('mirror/static/cdn/as6135-3563-4735-a365-643234376439/icons-112.png').convert('RGBA')
CUBE={'green':E.crop((19,12,160,134)),'orange':E.crop((318,25,444,134)),
      'red':E.crop((13,262,160,373)),'magenta':E.crop((318,262,452,383))}
# якоря углов (куда «прижимать» кубик)
ANCH={'TL':(8,8),'TR':(W-8,8),'BL':(8,H-8),'BR':(W-8,H-8)}
def place(base,name,corner,flip=False,scale=1.0):
    spr=CUBE[name]
    if scale!=1.0: spr=spr.resize((int(spr.width*scale),int(spr.height*scale)),Image.LANCZOS)
    if flip: spr=spr.transpose(Image.FLIP_LEFT_RIGHT)
    ax,ay=ANCH[corner]; w,h=spr.size
    x = ax if 'L' in corner else ax-w
    y = ay if 'T' in corner else ay-h
    base.alpha_composite(spr,(x,y))
def make(photo,focus,band,lines,cubes,out,sz=46):
    base=Image.new('RGBA',(W,H),(0,0,0,0))
    im=Image.open(photo).convert('RGB'); w,h=im.size; side=min(w,h)
    left=int((w-side)*focus); top=(h-side)//2
    ph=im.crop((left,top,left+side,top+side)).resize((2*R,2*R),Image.LANCZOS)
    m=Image.new('L',(2*R,2*R),0); ImageDraw.Draw(m).ellipse([0,0,2*R,2*R],fill=255)
    base.paste(ph,(CX-R,CY-R),m)
    for c in cubes: place(base,*c)
    d=ImageDraw.Draw(base); f=font(sz); lh=int(sz*1.0)
    while max(d.textlength(t,font=f) for t in lines)>W-78 and sz>28:
        sz-=2; f=font(sz); lh=int(sz*1.0)
    total=lh*len(lines); by0=CY-R+40
    mw=max(d.textlength(t,font=f) for t in lines); padx=22
    bw=max(mw+2*padx, W-52)  # единая минимальная ширина плашки для всех карточек
    d.rounded_rectangle([CX-bw/2,by0-12,CX+bw/2,by0+total+10],16,fill=band)
    y=by0
    for t in lines:
        tw=d.textlength(t,font=f); d.text((CX-tw/2,y),t,font=f,fill=(255,255,255)); y+=lh
    os.makedirs(os.path.dirname(out),exist_ok=True); base.save(out,'PNG'); print('saved',out)

# Выставка «Самара» — зелёная плашка, расстановка A
make('mirror/portfolio/samara-exhibition/photos/Ekran_parus.jpg',0.30,(94,178,46),
     ['ВЫСТАВКА','«САМАРА»'],
     [('green','TL',False,1.0),('orange','TR',False,1.0),('magenta','BL',False,1.05),('red','BR',True,0.9)],
     'mirror/static/cdn/custom-samara-exhibition/cover-main.png',48)
# Стенд Самарской области — красная плашка, расстановка B (другие кубики/углы/флипы)
make('mirror/portfolio/samara-vdnh/Card_Samara_stend.jpg',0.5,(196,38,46),
     ['СТЕНД САМАРСКОЙ','ОБЛАСТИ'],
     [('orange','TL',True,1.05),('green','TR',True,0.92),('red','BL',False,1.0),('magenta','BR',True,1.0)],
     'mirror/static/cdn/custom-samara-vdnh/cover-main.png',40)
