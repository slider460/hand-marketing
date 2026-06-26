# Генерит кастомную мобильную главную (mhome.html) из реальных данных.
import re, os, json, html as H
HERE=os.path.dirname(os.path.abspath(__file__))
P='static/cdn/'
_vm=os.path.join(HERE,'video_map.json')
SHOWREEL=(json.load(open(_vm)).get('showreel') if os.path.exists(_vm) else None) or '/media/hm-showreel.mp4'
# Готовые карточки команды Тильды (фото+имя+должность запечены вместе) — эталон,
# исключает путаницу подписей. Имя в alt — для доступности/SEO.
TEAM=[
 ("Народецкий Александр","as3230-6663-4363-b038-333866373133/__76876-145.png"),
 ("Семёнов Эдуард","as6534-3130-4535-b834-393262383437/__76876-149.png"),
 ("Сергей Кличановский","as3764-6333-4063-b531-396238386537/__76876-147.png"),
 ("Дементьев Святослав","as6136-6132-4639-a162-346433313762/__76876-151.png"),
 ("Осотов Алексей","as3939-3635-4033-a436-386536353930/__76876-150.png"),
 ("Агафонова Илона","as6561-6361-4236-b763-656565643230/__76876-148.png"),
 ("Муратов Денис","as3232-3531-4665-b739-626634306233/__76876-146.png"),
]
SERVICES=[("Event","/event","#673A7E"),("Creative & Design","/creativedesign","#C12164"),
 ("Video Production","/videoproduction","#CF6F19"),("Digital","/digital","#5E9A2E"),
 ("3D Mapping","/3dmapping","#7E3FA0"),("Print & Production","/printandproduction","#E08A2B"),("BTL","/btl","#D6357E")]
ABOUT=[("Более 10 лет","Делаем эффективные маркетинговые коммуникации","#C12164"),
 ("Full service","Любые услуги в области маркетинговых коммуникаций","#CF6F19"),
 ("Сотрудничество","Целеустремлённость и внимание к партнёрам — залог долгосрочного партнёрства","#5E9A2E"),
 ("Локация","Офис в центре Москвы. Региональная сеть с охватом 100+ городов России","#673A7E")]
LOGOS="""as3432-6564-4939-b661-323662313364/-1___1.png|as3066-3236-4161-b334-323334656232/samregion.png|as3832-3339-4933-b862-313162643738/-1___1_.png|as3838-3739-4632-b934-633966616665/tb-drone-logo-footer.svg|as3131-3864-4362-a232-336664366339/-1___1__23.png|as3464-6230-4430-a663-383430313964/logo_1.svg|as6136-3365-4733-b532-356530633965/-1___1__22.png|as6336-3333-4338-b864-363563663130/-1___1__21.png|as3561-6236-4939-a632-626362373038/-1___1__20.png|as6136-6532-4434-b338-356238363733/-1___1__19.png|as3566-6666-4236-b331-353564393064/-1___1__18.png|as6136-6462-4631-b130-616639666233/-1___1__17.png""".split('|')

cases=open(os.path.join(HERE,'carousels','all.html')).read()
m=re.search(r'<div class="mcases__track">(.*)</div></div>', cases, re.S)
cards=m.group(1) if m else ''

svc=''.join(f'<a class="mh-chip" href="{u}" style="--c:{c}">{H.escape(n)}</a>' for n,u,c in SERVICES)
ab=''.join(f'<div class="mh-val" style="--c:{c}"><div class="mh-val__dot"></div><div><div class="mh-val__t">{H.escape(t)}</div><div class="mh-val__d">{H.escape(d)}</div></div></div>' for t,d,c in ABOUT)
team=''.join(f'<div class="mh-mate"><img src="{P}{ph}" alt="{H.escape(n)}" loading="lazy"></div>' for n,ph in TEAM)
logos=''.join(f'<div class="mh-logo"><img src="{P}{l}" alt="" loading="lazy"></div>' for l in LOGOS)

mh=f'''<div class="mhome" id="mhome">
<header class="mh-hdr"><a class="mh-hdr__b" href="/"><img src="{P}as3365-6332-4339-a263-313566616365/152.png" alt="" width="36" height="36"><b>HAND MARKETING</b></a>
<button class="mh-burger" aria-label="Меню" aria-expanded="false"><span></span><span></span><span></span></button></header>
<nav class="mh-menu" hidden><a href="/project">Проекты</a><a href="/service">Услуги</a><a href="/about">О нас</a><a href="/clients">Клиенты</a><a href="/contacts">Контакты</a><a class="mh-menu__cta" href="#mh-form">Обсудить проект</a></nav>

<section class="mh-hero">
  <p class="mh-eyebrow">Рекламное агентство полного цикла · с 2012</p>
  <h1 class="mh-h1">Hand<br>Marketing</h1>
  <p class="mh-lead">Делаем маркетинг, <b>который видно</b> — от идеи до реализации.</p>
  <div class="mh-chips">{svc}</div>
</section>
<section class="mh-reel" id="mh-reel"><div class="mh-reel__cap">Шоурил</div><video controls preload="metadata" playsinline><source src="{SHOWREEL}" type="video/mp4"></video></section>

<section class="mh-sec" id="mh-cases">
  <div class="mh-sec__h"><h2>Кейсы</h2><a class="mh-all" href="/project">Все проекты →</a></div>
  <div class="mcases" data-mcases><div class="mcases__track">{cards}</div></div>
</section>

<section class="mh-sec mh-about">
  <h2>О нас</h2>
  <div class="mh-vals">{ab}</div>
</section>

<section class="mh-sec mh-team">
  <h2>Наша команда</h2>
  <div class="mh-mates" data-team><div class="mh-mates__track">{team}</div></div>
  <div class="mh-mates__dots" aria-hidden="true"></div>
</section>

<section class="mh-sec mh-clients">
  <h2>С нами работают</h2>
  <div class="mh-logos">{logos}</div>
</section>

<section class="mh-form" id="mh-form">
  <h2>Давайте сделаем проект вместе?</h2>
  <p>Оставьте контакты — перезвоним и обсудим задачу.</p>
  <form class="mh-f" onsubmit="return false">
    <input type="text" name="name" placeholder="Как вас зовут" autocomplete="name">
    <input type="tel" name="phone" placeholder="+7 ___ ___ __ __" autocomplete="tel" inputmode="tel">
    <button type="submit">Отправить заявку</button>
    <span class="mh-f__note">Нажимая кнопку, вы соглашаетесь с обработкой персональных данных</span>
  </form>
</section>

<footer class="mh-foot">
  <b>HAND MARKETING</b>
  <p>м. Краснопресненская / Баррикадная<br>123022, Москва, Рочдельская, 14А</p>
  <div class="mh-foot__c"><a href="tel:+74955807537">+7 495 580 75 37</a><a href="mailto:info@hand-marketing.ru">info@hand-marketing.ru</a></div>
  <div class="mh-foot__s"><a href="https://t.me/" aria-label="Telegram">TG</a><a href="https://wa.me/74955807537" aria-label="WhatsApp">WA</a></div>
  <nav class="mh-foot__nav"><a href="/about">О нас</a><a href="/service">Услуги</a><a href="/project">Проекты</a><a href="/clients">Клиенты</a><a href="/contacts">Контакты</a></nav>
  <small>© {2026} ООО «Хэнд-маркетинг»</small>
</footer>
</div>'''
open(os.path.join(HERE,'mhome.html'),'w').write(mh)
print('mhome.html:',len(mh),'bytes | cases cards:',cards.count('mcase__t'),'| team cards:',len(TEAM),'| logos:',len(LOGOS))
