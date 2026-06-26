import os, re, shutil
ROOT='/Users/aleksandrnarodetskii/Downloads/hand-marketing-react/mirror'
HERE=os.path.dirname(os.path.abspath(__file__))
MOBILE='<style>'+open(os.path.join(HERE,'mobile.css')).read()+'</style>'
MHOME_CSS='<style>'+open(os.path.join(HERE,'mhome.css')).read()+'</style>'
MHOME_HTML=open(os.path.join(HERE,'mhome.html')).read()
MPAGES={}
for _dir in ('mpages','mcases'):
    _d=os.path.join(HERE,_dir)
    if os.path.isdir(_d):
        for f in os.listdir(_d):
            if f.endswith('.html'):
                key=f[:-5].replace('__','/'); key='' if key=='index' else key
                MPAGES[key]=open(os.path.join(_d,f)).read()
MHOME_JS='''<script>(function(){var b=document.querySelector('.mh-burger'),m=document.querySelector('.mh-menu');if(b&&m){b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!o));m.hidden=o;});m.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){b.setAttribute('aria-expanded','false');m.hidden=true;});});}var h=document.querySelector('.mh-hdr');if(h)addEventListener('scroll',function(){h.style.boxShadow=pageYOffset>8?'0 8px 22px -12px rgba(0,0,0,.28)':'none';},{passive:true});})();</script>'''
def car(name):
    p=os.path.join(HERE,'carousels',name+'.html')
    return ('<!--MCASES-->'+open(p).read()+'<!--/MCASES-->') if os.path.exists(p) else None
PAGE_CAR={'':'all','project':'all','event':'event','creativedesign':'creative',
          'videoproduction':'video','digital':'digital','3dmapping':'3d'}
LOADMORE='''<script>
(function(){function home(){return location.pathname.replace(/index\\.html$/,'').replace(/\\/+$/,'')==='';}
if(!home())return;var STEP=8,n=STEP,btn=null;
function grid(){ var gs=document.querySelectorAll('.js-store-grid-cont,.t-store__card-list'); var best=null,bn=0; gs.forEach(function(g){var k=g.querySelectorAll('.t-store__card').length; if(k>bn){bn=k;best=g;}}); return bn>STEP?best:null; }
function apply(){ var g=grid(); if(!g)return; var cards=[].slice.call(g.querySelectorAll('.t-store__card'));
  cards.forEach(function(x,i){var d=i<n?'':'none'; if(x.style.display!==d)x.style.display=d;});
  if(!btn||!btn.isConnected){ btn=document.createElement('button'); btn.textContent='Загрузить ещё'; btn.style.cssText='display:block;margin:30px auto;padding:14px 38px;font:700 16px Montserrat,Arial,sans-serif;color:#fff;background:#000;border:0;border-radius:30px;cursor:pointer'; btn.onclick=function(){n+=STEP;apply();}; g.parentNode.insertBefore(btn,g.nextSibling); }
  btn.style.display=n>=cards.length?'none':'block'; }
new MutationObserver(apply).observe(document.body,{childList:true,subtree:true});
var t=0,iv=setInterval(function(){apply();if(++t>40)clearInterval(iv);},350);
})();
</script>'''

DROP_LIBS=('lib-polyfill','lib-cards-','lib-menu-widgeticons')  # неиспользуемое / для старых браузеров
CIRCE_LINK='<link rel="stylesheet" href="/static/fonts/circe.css" media="all">'
# грузим JS Тильды только на десктопе (>640); на мобиле всё кастомное — движок не нужен
BOOT='''<script>(function(){if(innerWidth<=640)return;var ns=[].slice.call(document.querySelectorAll('script[type="td"]'));(function go(i){if(i>=ns.length)return;var n=ns[i];if(n.getAttribute('data-src')){var s=document.createElement('script');s.src=n.getAttribute('data-src');s.async=false;s.onload=s.onerror=function(){go(i+1)};document.head.appendChild(s);}else{try{var s=document.createElement('script');s.text=n.textContent;document.head.appendChild(s);}catch(e){}go(i+1);}})(0);})();</script>'''

def strip_trackers(h):
    h=re.sub(r'<!-- Yandex\.Metrika counter -->.*?<!-- /Yandex\.Metrika counter -->','',h,flags=re.S)
    h=re.sub(r'<script[^>]*>[^<]*?(mc\.yandex|mainMetrikaId|dataLayer|gtag)[^<]*?</script>','',h,flags=re.S)
    # выкинуть неиспользуемые либы
    h=re.sub(r'<script[^>]+src="[^"]*('+'|'.join(DROP_LIBS)+r')[^"]*"[^>]*></script>','',h)
    return h

def defer_scripts(h):
    """JS-скрипты Тильды -> type=td (грузятся бутстрапом только на десктопе)."""
    def repl(m):
        attrs=m.group(1); inner=m.group(2)
        tm=re.search(r'type=(["\'])(.*?)\1',attrs)
        typ=(tm.group(2) if tm else '').lower()
        if typ and 'javascript' not in typ: return m.group(0)  # ld+json и пр. не трогаем
        sm=re.search(r'\ssrc=(["\'])(.*?)\1',attrs)
        if sm: return '<script type="td" data-src="'+sm.group(2)+'"></script>'
        return '<script type="td">'+inner+'</script>'
    return re.sub(r'<script\b([^>]*)>(.*?)</script>', repl, h, flags=re.S)

# Десктопные <video> Тильды ссылались на /media в своей схеме имён — приводим к тем же
# файлам, что в мобильном манифесте (VIDEO-UPLOAD.md), чтобы на сервере был один файл на ролик.
MEDIA_REMAP={
 'event-samsung.mp4':'samsung-new-year-2020.mp4',
 'event-changan.mp4':'changan-hm-180220.mp4',
 'event-eaton.mp4':'eaton-almaty.mp4',
 'event-marieclaire.mp4':'marie-claire-event.mp4',
 'event-salaris.mp4':'salaris-event-fin180416.mp4',
 'event-mozaika.mp4':'as-mozaika.mp4',
 'gaz-transformer.mp4':'gazelle-transformer.mp4',
 'interplastica.mp4':'interplastica-messe-duesseldorf.mp4',
 'patriot-eaton-yaz.mp4':'eaton-yaz.mp4',
 'powertech-long.mp4':'pt-film-long.mp4',
 'powertech-short.mp4':'pt-film-short.mp4',
 'rgd-history.mp4':'transrzhd.mp4',
 'video-lingerie.mp4':'video-lingerie-hand-marketing.mp4',
 'vivax.mp4':'vivax-samburskaya.mp4',
}
def remap_media(h):
    for a,b in MEDIA_REMAP.items():
        h=h.replace('/media/'+a,'/media/'+b)
    return h

def process(p, route):
    h=open(p,encoding='utf-8').read()
    if 'id="root"' in h:  # React-страницы не трогаем тут (у них свой A2)
        return None
    h=strip_trackers(h)
    h=remap_media(h)  # десктопные /media-ссылки -> имена из манифеста
    h=defer_scripts(h)  # JS Тильды -> только десктоп (мобайл кастомный, движок не нужен)
    # Tilda прячет .t-records (opacity:0) до reveal-скрипта по window.load; мы часть JS
    # откладываем/выпиливаем — reveal может не сработать -> белый экран. Форсим видимость.
    h=re.sub(r'(<head[^>]*>)', r'\1<style>.t-records{opacity:1!important}</style>', h, count=1)
    if route=='':  # ГЛАВНАЯ — кастомная мобильная версия (десктоп Тильда 1:1)
        G='#rec249749070 .t-store__card-list .t-store__card'
        lvl=G+':nth-child(n+9){display:none!important}'
        for s in range(2,7):
            lvl+=f'body.lm{s} {G}:nth-child(n+9){{display:revert!important}}'
            lvl+=f'body.lm{s} {G}:nth-child(n+{8*s+1}){{display:none!important}}'
        DESK_CSS='<style>@media(min-width:641px){#rec249926772{display:none!important}}'+lvl+'.mh-loadmore{display:block;margin:34px auto 0;padding:15px 44px;font:700 16px Montserrat,Arial,sans-serif;color:#fff;background:#14171C;border:0;border-radius:999px;cursor:pointer;transition:transform .2s}.mh-loadmore:hover{transform:translateY(-2px)}</style>'
        DESK_JS='''<script>(function(){function home(){return location.pathname.replace(/index\\.html$/,'').replace(/\\/+$/,'')==='';}if(!home())return;var step=1,btn=null;function place(){var b=document.getElementById('rec249749070');if(!b)return;var g=b.querySelector('.t-store__card-list')||b.querySelector('.js-store-grid-cont');if(!g)return;var total=g.querySelectorAll('.t-store__card').length;if(total<=8){if(btn)btn.style.display='none';return;}if(!btn||!btn.isConnected){btn=document.createElement('button');btn.className='mh-loadmore';btn.textContent='Загрузить ещё';btn.onclick=function(e){e.preventDefault();step++;document.body.className=document.body.className.replace(/\\blm\\d\\b/g,'').trim();if(step>1)document.body.classList.add('lm'+Math.min(step,6));place();};g.parentNode.insertBefore(btn,g.nextSibling);}btn.style.display=(8*step>=total)?'none':'block';}new MutationObserver(place).observe(document.body,{childList:true,subtree:true});var t=0,iv=setInterval(function(){place();if(++t>50)clearInterval(iv);},300);})();</script>'''
        h=h.replace('</head>', MHOME_CSS+DESK_CSS+CIRCE_LINK+'</head>',1)
        h=re.sub(r'(<body[^>]*>)', r'\1'+MHOME_HTML, h, count=1)
        h=h.replace('</body>', MHOME_JS+DESK_JS+BOOT+'</body>',1)
        return h
    if route in MPAGES:  # кастомная мобильная версия страницы (десктоп Тильда 1:1)
        h=h.replace('</head>', MHOME_CSS+CIRCE_LINK+'</head>',1)
        h=re.sub(r'(<body[^>]*>)', r'\1'+MPAGES[route], h, count=1)
        h=h.replace('</body>', MHOME_JS+BOOT+'</body>',1)
        return h
    # остальные страницы — карусель кейсов (мобайл) + Вариант 1
    cname=PAGE_CAR.get(route)
    if cname:
        CAR=car(cname)
        if CAR:
            m=re.search(r'<div class="[^"]*js-store-grid-cont', h)
            if m: h=h[:m.start()]+CAR+h[m.start():]
    h=h.replace('</head>', MOBILE+CIRCE_LINK+'</head>',1)
    h=h.replace('</body>', LOADMORE+BOOT+'</body>',1)
    return h

n=0
for dp,_,fns in os.walk(ROOT):
    if 'index.html' not in fns: continue
    rel=os.path.relpath(dp,ROOT); route='' if rel=='.' else rel
    out=process(os.path.join(dp,'index.html'), route)
    if out is None: continue
    open(os.path.join(dp,'index-a2.html'),'w',encoding='utf-8').write(out); n+=1
print('built', n, 'pages (Variant 1: движок Тильды + карусель, трекеры убраны)')
