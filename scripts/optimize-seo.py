#!/usr/bin/env python3
"""SEO/скорость-оптимизация mirror/: sitemap, robots, lang, описания,
JSON-LD (Organization + VideoObject на кейсах), семантический h1, фикс Метрики.
Идемпотентно — повторный запуск не дублирует."""
import glob, re, os, html, json, datetime
M='mirror'; DOMAIN='https://hand-marketing.ru'
LOGO=DOMAIN+'/static/cdn/as3365-6332-4339-a263-313566616365/152.png'
def url_of(f):
    rel=os.path.relpath(f,M); p=rel[:-len('index.html')].strip('/')
    return '/'+p if p else '/'
pages=sorted(glob.glob(M+'/**/index.html',recursive=True))
ORG={"@context":"https://schema.org","@type":"Organization","name":"Hand Marketing",
 "alternateName":"Хэнд-маркетинг","url":DOMAIN,"logo":LOGO,"telephone":"+7-495-580-75-37",
 "email":"info@hand-marketing.ru","foundingDate":"2012",
 "address":{"@type":"PostalAddress","addressCountry":"RU","addressLocality":"Москва",
   "postalCode":"105005","streetAddress":"наб. Академика Туполева, 15"}}
# кейсы с локальным видео -> VideoObject
VIDEOS={'isotec':('Бренд-ролик «Изотек»','/portfolio/isotec/brand-video.mp4','/portfolio/isotec/poster.jpg'),
 'mmg':('Рекламный ролик «Павелецкая Плаза»','/portfolio/mmg/brand-video.mp4','/portfolio/mmg/poster.jpg'),
 'bekobod1':('Технопарк «Бекабад»','/portfolio/bekobod/brand-video.mp4','/portfolio/bekobod/poster.jpg'),
 'zubovo':('Технопарк «Зубово»','/portfolio/zubovo/brand-video.mp4','/portfolio/zubovo/poster.jpg')}
H1CSS='position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0'
stats={'lang':0,'desc':0,'jsonld':0,'h1':0,'metrica':0,'video':0}
for f in pages:
    s=open(f,encoding='utf-8',errors='ignore').read(); s0=s
    key=os.path.relpath(f,M).split('/')[0] if '/' in os.path.relpath(f,M) else os.path.relpath(f,M).replace('/index.html','')
    folder=os.path.dirname(os.path.relpath(f,M)) or '/'
    # lang
    if not re.search(r'<html[^>]*\blang=',s):
        s=re.sub(r'<html(?![^>]*\blang=)',r'<html lang="ru"',s,1); stats['lang']+=1
    # description
    if 'name="description"' not in s:
        m=re.search(r'property="og:description" content="([^"]*)"',s) or re.search(r'<title>([^<]*)</title>',s)
        d=html.unescape(m.group(1)).strip() if m else 'Hand Marketing — рекламное агентство полного цикла.'
        if len(d)<30: d+=' — Hand Marketing, рекламное агентство полного цикла.'
        s=s.replace('</head>','<meta name="description" content="%s">\n</head>'%html.escape(d,quote=True),1); stats['desc']+=1
    # JSON-LD Organization
    if 'application/ld+json' not in s:
        s=s.replace('</head>','<script type="application/ld+json">%s</script>\n</head>'%json.dumps(ORG,ensure_ascii=False),1); stats['jsonld']+=1
        # VideoObject для кейсов с видео
        casek=folder.strip('/').split('/')[0]
        if casek in VIDEOS:
            nm,vid,pos=VIDEOS[casek]
            vo={"@context":"https://schema.org","@type":"VideoObject","name":nm,
                "description":nm+" — видеопродакшн Hand Marketing.","thumbnailUrl":DOMAIN+pos,
                "contentUrl":DOMAIN+vid,"uploadDate":"2024-01-01","publisher":{"@type":"Organization","name":"Hand Marketing","logo":{"@type":"ImageObject","url":LOGO}}}
            s=s.replace('</head>','<script type="application/ld+json">%s</script>\n</head>'%json.dumps(vo,ensure_ascii=False),1); stats['video']+=1
    # h1 если нет
    if not re.search(r'<h1[\s>]',s):
        m=re.search(r'<title>([^<]*)</title>',s); t=html.unescape(m.group(1)).strip() if m else 'Hand Marketing'
        t=re.sub(r'\s*[—-]\s*Hand Marketing.*$','',t).strip() or 'Hand Marketing'
        s=re.sub(r'(<body[^>]*>)',r'\1<h1 style="%s">%s</h1>'%(H1CSS,html.escape(t)),s,1); stats['h1']+=1
    # фикс счётчика Метрики weshow -> hand-marketing
    if '106784795' in s:
        s=s.replace('106784795','71125393'); stats['metrica']+=1
    if s!=s0: open(f,'w').write(s)
# sitemap.xml
now=datetime.date.today().isoformat()
us=''.join('<url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>'%(DOMAIN,url_of(f),now,'1.0' if url_of(f)=='/' else '0.7') for f in pages)
open(M+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>'%us)
# robots.txt
open(M+'/robots.txt','w').write("User-agent: *\nAllow: /\nDisallow: /api/leads.csv\n\nSitemap: %s/sitemap.xml\nHost: hand-marketing.ru\n"%DOMAIN)
print('Оптимизация:',stats)
print('sitemap: %d URL | robots.txt создан'%len(pages))
