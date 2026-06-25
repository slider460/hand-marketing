import json, glob, os, re, urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def kebab(name):
    n=name.rsplit('.',1)[0]
    n=urllib.parse.unquote(n)
    n=re.sub(r'[^A-Za-z0-9]+','-',n).strip('-').lower()
    return (n or 'video')+'.mp4'
# известные псевдонимы (общие ролики + уже существующие в /media)
ALIAS={'3D Silk Way.mp4':'silkway-3d.mp4','Samsung 2020.mp4':'samsung-new-year-2020.mp4','HM_Showreel.mp4':'hm-showreel.mp4'}
cases=json.load(open(os.path.join(ROOT,'src/data/cases.json')))
route_by_slug={c['slug']:c['route'] for c in cases}
seen={}   # original name -> kebab (dedup shared)
manifest=[]  # (slug, route, original_src_name, kebab)
vmap={}      # route -> [ /media/kebab ]
showreel=None
i_multi={}
for f in sorted(glob.glob(os.path.join(ROOT,'src/data/pages/*.json'))):
    slug=os.path.basename(f)[:-5]
    d=json.load(open(f))
    vids=[v.get('src') for b in d.get('blocks',[]) for v in b.get('videos',[]) if v.get('src')]
    if not vids: continue
    route=route_by_slug.get(slug)
    for s in vids:
        orig=urllib.parse.unquote(s.split('/')[-1].split('?')[0])
        if orig in ALIAS: kb=ALIAS[orig]
        elif orig in seen: kb=seen[orig]
        else:
            kb=kebab(orig)
            # для мусорных имён вида 1_,2_ — по слагу
            if re.match(r'^\d+-?\.?mp4$', kb) or len(kb)<7:
                i_multi[slug]=i_multi.get(slug,0)+1; kb=slug.replace('__','-')+f'-{i_multi[slug]}.mp4'
            seen[orig]=kb
        manifest.append((slug, route or '', orig, kb))
        if slug=='index': showreel='/media/'+kb
        elif route: vmap.setdefault(route.strip('/'),[])
        if route and slug!='index':
            u='/media/'+kb
            if u not in vmap[route.strip('/')]: vmap[route.strip('/')].append(u)
json.dump({'videos':vmap,'showreel':showreel}, open(os.path.join(os.path.dirname(__file__),'video_map.json'),'w'), ensure_ascii=False, indent=1)
# манифест для пользователя
lines=['# Видео для загрузки в /media/ (на хостинг)','',f'Всего файлов: {len(set(k for *_,k in manifest))} (некоторые ролики общие для нескольких кейсов).','','| Кейс | Файл на хостинге | Исходник |','|---|---|---|']
for slug,route,orig,kb in manifest:
    lines.append(f'| {route or slug} | `/media/{kb}` | {orig} |')
open(os.path.join(ROOT,'VIDEO-UPLOAD.md'),'w').write('\n'.join(lines))
print('файлов уникальных:',len(set(k for *_,k in manifest)),'| кейсов с видео:',len(vmap),'| showreel:',showreel)
print('манифест: VIDEO-UPLOAD.md  | карта: scripts/a2/video_map.json')
