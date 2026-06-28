import json, re, os, glob, html as H
API='mirror/api'
def strip(s): return re.sub('<[^>]+>','',s or '').strip()
data={}
for f in glob.glob(API+'/getproductslist_*.json'):
    try: d=json.load(open(f))
    except: continue
    for p in d.get('products',[]):
        url=p.get('url') or ''
        if not url: continue
        title=(p.get('title') or '').strip()
        if title=='⠀': title=''
        cur=data.get(url,{})
        if title and not cur.get('title'):
            g=json.loads(p['gallery']) if p.get('gallery') else []
            cur.update(title=title, descr=(p.get('descr') or '').strip(), cat=strip(p.get('text')), img=(g[0]['img'] if g else cur.get('img','')))
        if not cur.get('img'):
            g=json.loads(p['gallery']) if p.get('gallery') else []
            if g: cur['img']=g[0]['img']
        data[url]=cur
order=json.load(open(API+'/getproductslist_689558768071.json'))['products']
FB={'/portfolio/samara-stand-vdnh':('Стенд Самарской области','Выставка-форум «Россия», ВДНХ','Exhibition Build'),
    '/portfolio/samara-exhibition':('Выставка «Самара»','Музей им. Алабина','Exhibition Build'),
    '/portfolio/stavropol-stand-vdnh':('Стенд Ставропольского края','Выставка-форум «Россия», ВДНХ','Exhibition Build')}
COL={'event':'#C12164','exhibition':'#673A7E','creative':'#C12164','video':'#CF6F19','digital':'#5E9A2E','3d':'#7E3FA0','btl':'#D6357E','print':'#E08A2B'}
def cat_key(cat):
    c=cat.lower()
    for k in COL:
        if k in c: return k
    return ''
def card(url,title,descr,cat,img):
    k=cat_key(cat); color=COL.get(k,'#14171C')
    return f'''<a class="mcase" href="{H.escape(url)}"><div class="mcase__img"><img src="{H.escape(img)}" alt="" loading="lazy"><span class="mcase__cat" style="--c:{color}">{H.escape(cat)}</span></div><div class="mcase__b"><div class="mcase__t">{H.escape(title)}</div><div class="mcase__d">{H.escape(descr)}</div></div></a>'''
allcards=[]; bycat={}
for p in order:
    url=p.get('url') or ''
    g=json.loads(p['gallery']) if p.get('gallery') else []
    img=(g[0]['img'] if g else '')
    info=data.get(url,{}); title=info.get('title') or ''; descr=info.get('descr') or ''; cat=info.get('cat') or ''
    if url in FB and not title: title,descr,cat=FB[url]
    if not img: img=info.get('img','')
    if not title and not img: continue
    c=card(url,title,descr,cat,img); allcards.append(c)
    k=cat_key(cat); bycat.setdefault(k,[]).append(c)
def wrap(cards): return '<div class="mcases" data-mcases><div class="mcases__track">'+''.join(cards)+'</div></div>'
os.makedirs('scripts/a2/carousels',exist_ok=True)
open('scripts/a2/carousels/all.html','w').write(wrap(allcards))
for k,cs in bycat.items():
    if k: open(f'scripts/a2/carousels/{k}.html','w').write(wrap(cs))
print('all:',len(allcards),'| by cat:',{k:len(v) for k,v in bycat.items()})
