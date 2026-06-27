# Кастомные мобильные страницы (project, service overview, service pages, contacts, about) — переиспуют компоненты mhome.
import os, re, html as H
HERE=os.path.dirname(os.path.abspath(__file__))
P='static/cdn/'
HM='as3365-6332-4339-a263-313566616365/152.png'

HEADER=f'''<header class="mh-hdr"><a class="mh-hdr__b" href="/"><img src="/{P}{HM}" alt="" width="36" height="36"><b>HAND MARKETING</b></a>'''+'''
<button class="mh-burger" aria-label="Меню" aria-expanded="false"><span></span><span></span><span></span></button></header>
<nav class="mh-menu" hidden><a href="/project">Проекты</a><a href="/service">Услуги</a><a href="/about">О нас</a><a href="/clients">Клиенты</a><a href="/contacts">Контакты</a><a class="mh-menu__cta" href="/contacts">Обсудить проект</a></nav>'''
FOOTER='''<footer class="mh-foot"><b>HAND MARKETING</b>
<p>м. Краснопресненская / Баррикадная<br>123022, Москва, Рочдельская, 14А</p>
<div class="mh-foot__c"><a href="tel:+74955807537">+7 495 580 75 37</a><a href="mailto:info@hand-marketing.ru">info@hand-marketing.ru</a></div>
<div class="mh-foot__s"><a href="https://t.me/" aria-label="Telegram">TG</a><a href="https://wa.me/74955807537" aria-label="WhatsApp">WA</a></div>
<nav class="mh-foot__nav"><a href="/about">О нас</a><a href="/service">Услуги</a><a href="/project">Проекты</a><a href="/clients">Клиенты</a><a href="/contacts">Контакты</a></nav>
<small>© 2026 ООО «Хэнд-маркетинг»</small></footer>'''
FORM='''<section class="mh-form" id="mh-form"><h2>Давайте сделаем проект вместе?</h2><p>Оставьте контакты — перезвоним и обсудим задачу.</p>
<form class="mh-f" onsubmit="return false"><input type="text" name="name" placeholder="Как вас зовут" autocomplete="name"><input type="tel" name="phone" placeholder="+7 ___ ___ __ __" autocomplete="tel" inputmode="tel"><button type="submit">Отправить заявку</button><span class="mh-f__note">Нажимая кнопку, вы соглашаетесь с обработкой персональных данных</span></form></section>'''

SERVICES=[("Event","/event","#673A7E","Мероприятия под ключ: концепция, площадка, продакшн, режиссура"),
 ("Creative & Design","/creativedesign","#C12164","Брендинг, дизайн, креативные концепции и POSm"),
 ("Video Production","/videoproduction","#CF6F19","Имиджевые и рекламные ролики, съёмка и пост-продакшн"),
 ("Digital","/digital","#5E9A2E","Сайты, лендинги и digital-продвижение"),
 ("3D Mapping","/3dmapping","#7E3FA0","Мультимедийные 3D-mapping шоу любого масштаба"),
 ("Print & Production","/printandproduction","#E08A2B","Полиграфия, сувениры и производство любой сложности"),
 ("BTL","/btl","#D6357E","Промо-акции, активации и нестандартный BTL")]

def car(name):
    p=os.path.join(HERE,'carousels',name+'.html'); return open(p).read() if os.path.exists(p) else ''
def cards_of(name):  # внутренние .mcase из карусели
    m=re.search(r'<div class="mcases__track">(.*)</div></div>', car(name), re.S); return m.group(1) if m else ''

def wrap(inner): return f'<div class="mhome mpage" id="mhome">{HEADER}{inner}{FOOTER}</div>'

PAGES={}
# ПРОЕКТЫ — все кейсы 1 колонкой
PAGES['project']=wrap(f'''<section class="mh-hero mh-hero_sm"><p class="mh-eyebrow">Портфолио</p><h1 class="mh-h1 mh-h1_sm">Проекты</h1><p class="mh-lead">Кейсы по всем направлениям — от event до 3D-mapping.</p></section>
<section class="mh-sec"><div class="mh-grid">{cards_of('all')}</div></section>''')
# УСЛУГИ — обзор
svc_cards=''.join(f'<a class="mh-scard" href="{u}" style="--c:{c}"><span class="mh-scard__ghost" aria-hidden="true">{H.escape(n[0])}</span><span class="mh-scard__tag">Услуга</span><h3 class="mh-scard__t">{H.escape(n)}</h3><p class="mh-scard__d">{H.escape(d)}</p><span class="mh-scard__go" aria-hidden="true"></span></a>' for n,u,c,d in SERVICES)
PAGES['service']=wrap(f'''<section class="mh-hero mh-hero_sm"><p class="mh-eyebrow">Что мы делаем</p><h1 class="mh-h1 mh-h1_sm">Услуги</h1><p class="mh-lead">Полный цикл маркетинговых коммуникаций.</p></section>
<section class="mh-sec"><div class="mh-scards">{svc_cards}</div></section>''')
# СТРАНИЦЫ УСЛУГ
SCAR={'event':'event','creativedesign':'creative','videoproduction':'video','digital':'digital','3dmapping':'3d'}
for n,u,c,d in SERVICES:
    route=u.strip('/'); cat=SCAR.get(route)
    cases=f'<section class="mh-sec"><div class="mh-sec__h"><h2>Кейсы</h2><a class="mh-all" href="/project">Все →</a></div><div class="mcases" data-mcases><div class="mcases__track">{cards_of(cat)}</div></div></section>' if cat else ''
    PAGES[route]=wrap(f'''<section class="mh-hero mh-hero_sm" style="--c:{c}"><p class="mh-eyebrow" style="color:{c}">Услуга</p><h1 class="mh-h1 mh-h1_sm">{H.escape(n)}</h1><p class="mh-lead">{H.escape(d)}.</p><a class="mh-showreel" href="#mh-form">Обсудить проект</a></section>{cases}{FORM}''')
# КОНТАКТЫ
PAGES['contacts']=wrap(f'''<section class="mh-hero mh-hero_sm"><p class="mh-eyebrow">Свяжитесь с нами</p><h1 class="mh-h1 mh-h1_sm">Контакты</h1></section>
<section class="mh-sec"><div class="mh-contacts">
<a class="mh-crow" href="tel:+74955807537"><span>Телефон</span><b>+7 495 580 75 37</b></a>
<a class="mh-crow" href="mailto:info@hand-marketing.ru"><span>E-mail</span><b>info@hand-marketing.ru</b></a>
<div class="mh-crow"><span>Адрес</span><b>123022, Москва, Рочдельская, 14А<br>м. Краснопресненская / Баррикадная</b></div>
<div class="mh-csoc"><a href="https://t.me/">Telegram</a><a href="https://wa.me/74955807537">WhatsApp</a></div>
</div></section>{FORM}''')
# О НАС
ABOUT=[("Более 10 лет","Делаем эффективные маркетинговые коммуникации","#C12164"),("Full service","Любые услуги в области маркетинговых коммуникаций","#CF6F19"),("Сотрудничество","Целеустремлённость и внимание к партнёрам — залог долгосрочного партнёрства","#5E9A2E"),("Локация","Офис в центре Москвы. Региональная сеть с охватом 100+ городов России","#673A7E")]
ab=''.join(f'<div class="mh-val" style="--c:{c}"><div class="mh-val__dot"></div><div><div class="mh-val__t">{H.escape(t)}</div><div class="mh-val__d">{H.escape(d)}</div></div></div>' for t,d,c in ABOUT)
PAGES['about']=wrap(f'''<section class="mh-hero mh-hero_sm"><p class="mh-eyebrow">Агентство</p><h1 class="mh-h1 mh-h1_sm">О нас</h1><p class="mh-lead">Рекламное агентство полного цикла с 2012 года.</p></section>
<section class="mh-sec mh-about"><div class="mh-vals">{ab}</div></section>
<section class="mh-sec"><p style="padding:0 20px;color:#5A616A;line-height:1.6">Основная философия агентства — «прозрачность»: клиент наблюдает за исполнением на каждом этапе. Главная движущая сила — сотрудники с богатым опытом в рекламном бизнесе. Принцип работы — комплексное обеспечение клиентского сервиса на основе анализа потребностей.</p></section>{FORM}''')

os.makedirs(os.path.join(HERE,'mpages'),exist_ok=True)
for r,html in PAGES.items():
    open(os.path.join(HERE,'mpages',(r or 'index').replace('/','__')+'.html'),'w').write(html)
print('mpages:',sorted(PAGES.keys()))
