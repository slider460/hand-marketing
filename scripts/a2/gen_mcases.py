import json, os, re, html as H
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(HERE))
P='static/cdn/'; HM='as3637-6665-4238-b166-636533313130/_hm-64.svg'
HEADER=f'''<header class="mh-hdr"><a class="mh-hdr__b" href="/"><img src="/{P}{HM}" width="34" height="34" alt=""><b>HAND MARKETING</b></a><button class="mh-burger" aria-label="Меню" aria-expanded="false"><span></span><span></span><span></span></button></header><nav class="mh-menu" hidden><a href="/project">Проекты</a><a href="/service">Услуги</a><a href="/about">О нас</a><a href="/clients">Клиенты</a><a href="/contacts">Контакты</a><a class="mh-menu__cta" href="/contacts">Обсудить проект</a></nav>'''
FOOTER='''<footer class="mh-foot"><b>HAND MARKETING</b><p>м. Краснопресненская / Баррикадная<br>123022, Москва, Рочдельская, 14А</p><div class="mh-foot__c"><a href="tel:+74955807537">+7 495 580 75 37</a><a href="mailto:info@hand-marketing.ru">info@hand-marketing.ru</a></div><div class="mh-foot__s"><a href="https://t.me/">TG</a><a href="https://wa.me/74955807537">WA</a></div><nav class="mh-foot__nav"><a href="/about">О нас</a><a href="/service">Услуги</a><a href="/project">Проекты</a><a href="/clients">Клиенты</a><a href="/contacts">Контакты</a></nav><small>© 2026 ООО «Хэнд-маркетинг»</small></footer>'''
FORM='''<section class="mh-form" id="mh-form"><h2>Хотите так же?</h2><p>Оставьте контакты — обсудим ваш проект.</p><form class="mh-f" onsubmit="return false"><input type="text" name="name" placeholder="Как вас зовут" autocomplete="name"><input type="tel" name="phone" placeholder="+7 ___ ___ __ __" autocomplete="tel" inputmode="tel"><button type="submit">Отправить заявку</button><span class="mh-f__note">Нажимая кнопку, вы соглашаетесь с обработкой персональных данных</span></form></section>'''
COL={'event':'#673A7E','creative':'#C12164','video':'#CF6F19','digital':'#5E9A2E','3dmapping':'#7E3FA0','print':'#E08A2B','btl':'#D6357E'}
LABELS={'Задача','Задачи','Решение','Результат','Компания','Цель','Идея'}
_vm=os.path.join(HERE,'video_map.json')
VIDEOS=json.load(open(_vm)).get('videos',{}) if os.path.exists(_vm) else {}
_gm=os.path.join(HERE,'gallery_map.json')
GALLERY=json.load(open(_gm)) if os.path.exists(_gm) else {}
# Денлист мусора для fallback-галерей (page JSON): постер видео, декор-акценты Zero-блоков,
# иконки, заглушки, svg-разделители — оставляем только реальные фото/мокапы.
JUNK=re.compile(r'(icons-\d+|noroot|pngegg|_{2,}-?\d|_{2,}\d-\d|4234242|1234567890|\.svg$)',re.I)
def clean(urls):
    return [u for u in urls if not JUNK.search(u.split('/')[-1])]
cases=json.load(open(os.path.join(ROOT,'src/data/cases.json')))
made=0
os.makedirs(os.path.join(HERE,'mcases'),exist_ok=True)
for c in cases:
    slug=c['slug']; route=c['route'].strip('/')
    pj=os.path.join(ROOT,'src/data/pages',slug+'.json')
    if not os.path.exists(pj): continue
    d=json.load(open(pj))
    texts=[]; imgs=[]
    for b in d.get('blocks',[]):
        for t in b.get('texts',[]):
            tt=(t.get('text') or '').strip()
            if tt: texts.append(tt)
        for im in b.get('images',[]):
            loc=im.get('local')
            if loc and loc not in imgs: imgs.append(loc.replace('/assets/','/case-assets/'))
    # история: только содержательные абзацы (метки-заголовки в исходнике разрознены — пропускаем)
    seen=set(); story=[]
    for t in texts:
        if len(t)>=90 and t not in seen:
            seen.add(t); story.append(t)
    storyhtml=''.join(f'<p>{H.escape(v)}</p>' for v in story)
    color=COL.get(c['category'],'#14171C')
    # обложка — из cases.json; но если это общий мусор-постер, берём первое реальное фото
    cover=(c.get('cover') or (imgs[0] if imgs else '')).replace('/assets/','/case-assets/')
    if JUNK.search(cover.split('/')[-1]):
        real=clean(imgs)
        if real: cover=real[0]
    # галерея — реальные фото с мероприятия из отрендеренной Тильды; иначе fallback на page JSON
    extracted=GALLERY.get(route,[])
    if extracted:
        gallery=extracted
    else:
        gallery=clean([i for i in imgs if i!=cover])
    galhtml=''.join(f'<img src="{H.escape(g)}" alt="" loading="lazy">' for g in gallery)
    inner=f'''<section class="mh-hero mh-hero_sm" style="--c:{color}"><a class="mh-back" href="/project">← Все проекты</a><p class="mh-eyebrow" style="color:{color}">{H.escape(c['categoryLabel'])}</p><h1 class="mh-h1 mh-h1_sm">{H.escape(c['client'])}</h1><p class="mh-lead">{H.escape(c['title'])}</p></section>'''
    if cover: inner+=f'<div class="mh-cover"><img src="{H.escape(cover)}" alt="{H.escape(c["title"])}"></div>'
    if storyhtml: inner+=f'<section class="mh-sec mh-story">{storyhtml}</section>'
    vids=VIDEOS.get(route,[])
    if vids:
        cov=H.escape(cover) if cover else ''
        vhtml=''.join(f'<video class="mh-video" controls preload="none" playsinline poster="{cov}"><source src="{u}" type="video/mp4"></video>' for u in vids)
        inner+=f'<section class="mh-sec"><h2 style="padding:0 20px">Видео</h2><div class="mh-videos">{vhtml}</div></section>'
    if galhtml: inner+=f'<section class="mh-sec"><h2 style="padding:0 20px">Галерея</h2><div class="mh-gallery">{galhtml}</div></section>'
    inner+=FORM
    html=f'<div class="mhome mpage mcase-page" id="mhome">{HEADER}{inner}{FOOTER}</div>'
    open(os.path.join(HERE,'mcases',route.replace('/','__')+'.html'),'w').write(html)
    made+=1
print('case mobile pages:',made)
