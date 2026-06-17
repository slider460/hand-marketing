#!/usr/bin/env python3
"""Индустриальный showcase-дизайн технопарков (BEKOBOD, ЗУБОВО).
Тема: industrial modernism / master-plan. Заменяет только контент-rec.
Шапка/CTA/подвал — родные."""
import re

CSS = '''<style>
@import url('https://fonts.googleapis.com/css2?family=Geologica:wght@400;500;600;700;800&family=Onest:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');
.tp{--bg:#FFFFFF;--bg2:#F6F7F5;--text:#474C54;--head:#14171C;--dim:#8A909A;--faint:#AEB4BC;
 --acc:__ACC__;--acc2:__ACC2__;--line:rgba(20,23,28,.11);--grid:__GRID__;--ease:cubic-bezier(.16,1,.3,1);
 background:var(--bg);color:var(--text);font-family:'Onest',system-ui,sans-serif;font-size:17px;line-height:1.62;
 -webkit-font-smoothing:antialiased;position:relative;overflow:hidden}
.tp *{box-sizing:border-box}
.tp ::selection{background:var(--acc);color:#fff}
/* blueprint grid signature */
.tp__grid{position:absolute;inset:0;z-index:0;pointer-events:none;opacity:.7;
 background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
 background-size:54px 54px;mask:radial-gradient(120% 80% at 75% 0,#000,transparent 72%)}
.tp__wrap{max-width:1160px;margin:0 auto;padding:0 24px;position:relative;z-index:2}
/* hero */
.tp__hero{padding:34px 0 30px;position:relative}
.tp__kick{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--acc);
 margin:0 0 22px;display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;font-weight:500}
.tp__kick .coord{color:var(--dim)}
.tp__kick .sq{width:9px;height:9px;background:var(--acc);display:inline-block}
.tp__title{font-family:'Geologica',sans-serif;font-weight:700;color:var(--head);
 font-size:clamp(40px,11vw,92px);line-height:.98;letter-spacing:-.02em;margin:0 0 18px}
.tp__title b{color:var(--acc);font-weight:800}
.tp__lead{max-width:600px;font-size:clamp(16px,4.2vw,20px);color:#3D434B;margin:0 0 34px}
/* spec sheet */
.tp__spec{display:grid;grid-template-columns:repeat(2,1fr);border:1px solid var(--line);max-width:640px;margin:0 0 40px;background:var(--bg2)}
@media(min-width:720px){.tp__spec{grid-template-columns:repeat(4,1fr)}}
.tp__spec div{padding:15px 16px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.tp__spec dt{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--dim);margin:0 0 6px}
.tp__spec dd{margin:0;font-weight:600;color:var(--head);font-size:14.5px}
/* video */
.tp__stage{position:relative;border:1px solid var(--line);overflow:hidden;background:#0c0d10;
 box-shadow:0 30px 70px -42px rgba(20,23,28,.4)}
.tp__stage video,.tp__stage img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#000}
.tp__pb{position:absolute;inset:0;border:0;width:100%;padding:0;cursor:pointer;background-size:cover;background-position:center;
 display:flex;align-items:center;justify-content:center;transition:.5s var(--ease)}
.tp__pb::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,12,15,.05),rgba(10,12,15,.4))}
.tp__play{position:relative;width:84px;height:84px;border:1.5px solid var(--acc);display:grid;place-items:center;
 background:rgba(255,255,255,.92);transition:.35s var(--ease);z-index:1}
.tp__play::after{content:"";margin-left:5px;border-style:solid;border-width:11px 0 11px 18px;border-color:transparent transparent transparent var(--acc)}
.tp__pb:hover .tp__play{transform:scale(1.08);background:#fff}
.tp__tick{position:absolute;width:13px;height:13px;border-color:#fff;z-index:1;opacity:.85}
.tp__tick.tl{top:9px;left:9px;border-top:1.5px solid;border-left:1.5px solid}
.tp__tick.tr{top:9px;right:9px;border-top:1.5px solid;border-right:1.5px solid}
.tp__tick.bl{bottom:9px;left:9px;border-bottom:1.5px solid;border-left:1.5px solid}
.tp__tick.br{bottom:9px;right:9px;border-bottom:1.5px solid;border-right:1.5px solid}
.tp__cap{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:16px;font-family:'JetBrains Mono',monospace;font-size:11.5px;letter-spacing:.06em;color:var(--faint);text-transform:uppercase}
.tp__cap b{color:var(--dim);font-weight:500}
/* sections */
.tp__sec{padding:58px 0;border-top:1px solid var(--line)}
.tp__label{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 26px;display:flex;align-items:center;gap:12px;font-weight:500}
.tp__label::before{content:"";width:22px;height:2px;background:var(--acc)}
.tp__about{display:grid;gap:30px}
@media(min-width:860px){.tp__about{grid-template-columns:1fr 1.15fr;gap:56px;align-items:start}}
.tp__about h2{font-family:'Geologica',sans-serif;font-weight:700;font-size:clamp(26px,6vw,40px);line-height:1.05;margin:0 0 18px;color:var(--head)}
.tp__about p{margin:0 0 15px;color:#4A4F57}
.tp__stat{margin-top:24px;border-top:1px solid var(--line);padding-top:20px}
.tp__stat .big{font-family:'Geologica',sans-serif;font-weight:800;font-size:clamp(46px,12vw,84px);color:var(--acc);line-height:.9;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.tp__stat .cap{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin-top:8px}
/* steps */
.tp__steps{display:grid;gap:0}
.tp__step{display:grid;grid-template-columns:auto 1fr;gap:26px;padding:32px 0;border-top:1px solid var(--line)}
@media(max-width:620px){.tp__step{grid-template-columns:1fr;gap:12px}}
.tp__num{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:14px;color:var(--acc);letter-spacing:.05em;padding-top:8px}
.tp__step h3{font-family:'Geologica',sans-serif;font-weight:600;font-size:clamp(21px,5vw,28px);margin:0 0 12px;color:var(--head);line-height:1.1}
.tp__step p{margin:0 0 12px;color:#4A4F57}
.tp__step ul{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:0}
.tp__step li{position:relative;padding:12px 0 12px 24px;border-top:1px solid var(--line);font-size:15.5px}
.tp__step li::before{content:"";position:absolute;left:0;top:18px;width:8px;height:8px;background:var(--acc)}
.tp__step b{color:var(--head)}
/* three directions cards */
.tp__cards{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);margin-top:8px}
@media(min-width:760px){.tp__cards{grid-template-columns:repeat(3,1fr)}}
.tp__card{background:var(--bg);padding:26px 22px}
.tp__card .ix{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--acc);letter-spacing:.08em}
.tp__card h4{font-family:'Geologica',sans-serif;font-weight:600;font-size:19px;color:var(--head);margin:10px 0 8px}
.tp__card p{margin:0;font-size:14.5px;color:var(--dim)}
/* reveal */
.tp .rv{opacity:0;transform:translateY(24px);transition:opacity .9s var(--ease),transform .9s var(--ease)}
.tp .rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.tp .rv{opacity:1;transform:none;transition:none}}
</style>'''

def esc(t):
    import html
    return html.escape(t, quote=False)

def render(cfg):
    spec = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in cfg['spec'])
    cap = ''.join(f'<span><b>{esc(c)}</b></span>' for c in cfg['cap'])
    # steps
    steps = ''
    for st in cfg['steps']:
        body = ''.join(f'<p>{esc(p)}</p>' for p in st.get('p', []))
        if st.get('ul'):
            body += '<ul>' + ''.join(f'<li>{b}</li>' for b in st['ul']) + '</ul>'
        steps += (f'<div class="tp__step"><div class="tp__num">{esc(st["n"])}</div>'
                  f'<div><h3>{esc(st["h"])}</h3>{body}</div></div>')
    cards = ''
    if cfg.get('cards'):
        cc = ''.join(f'<div class="tp__card"><div class="ix">{esc(i)}</div><h4>{esc(h)}</h4><p>{esc(p)}</p></div>'
                     for i, h, p in cfg['cards'])
        cards = (f'<section class="tp__sec rv"><p class="tp__label">{esc(cfg["cards_label"])}</p>'
                 f'<div class="tp__cards">{cc}</div></section>')
    stat = ''
    if cfg.get('stat'):
        stat = f'<div class="tp__stat"><div class="big">{esc(cfg["stat"][0])}</div><div class="cap">{esc(cfg["stat"][1])}</div></div>'
    css = (CSS.replace('__ACC2__', cfg['acc2']).replace('__ACC__', cfg['acc'])
           .replace('__GRID__', cfg['grid']).replace('var(--accrgb)', cfg['accrgb']))
    return (f'<div id="{cfg["rec"]}" class="r t-rec" style="background:#FFFFFF;" data-record-type="custom">'
            f'<section class="tp">{css}<div class="tp__grid"></div>'
            f'<div class="tp__wrap"><header class="tp__hero">'
            f'<p class="tp__kick"><span class="sq"></span>{esc(cfg["kick"])} <span class="coord">{esc(cfg["coord"])}</span></p>'
            f'<h1 class="tp__title rv">{cfg["title"]}</h1>'
            f'<p class="tp__lead rv">{esc(cfg["lead"])}</p>'
            f'<dl class="tp__spec rv">{spec}</dl>'
            f'<div class="tp__stage rv">'
            f'<video id="tpfilm" playsinline preload="none" controls poster="{cfg["poster"]}"><source src="{cfg["video"]}" type="video/mp4"></video>'
            f'<button class="tp__pb" id="tppb" style="background-image:url(\'{cfg["poster"]}\')" aria-label="Смотреть ролик"><span class="tp__play"></span></button>'
            f'<i class="tp__tick tl"></i><i class="tp__tick tr"></i><i class="tp__tick bl"></i><i class="tp__tick br"></i></div>'
            f'<div class="tp__cap rv">{cap}</div>'
            f'</header></div>'
            f'<div class="tp__wrap"><section class="tp__sec tp__about rv">'
            f'<div><p class="tp__label">{esc(cfg["about_label"])}</p><h2>{esc(cfg["about_h"])}</h2>{stat}</div>'
            f'<div>{"".join(f"<p>{esc(p)}</p>" for p in cfg["about_p"])}</div></section>'
            f'<section class="tp__sec rv"><p class="tp__label">Как мы это сделали</p><div class="tp__steps">{steps}</div></section>'
            f'{cards}</div>'
            f'<script>(function(){{var v=document.getElementById("tpfilm"),p=document.getElementById("tppb");'
            f'if(v&&p){{p.addEventListener("click",function(){{p.style.opacity="0";p.style.pointerEvents="none";v.play();}});'
            f'v.addEventListener("pause",function(){{if(v.currentTime===0){{p.style.opacity="1";p.style.pointerEvents="";}}}});}}'
            f'if(matchMedia("(prefers-reduced-motion:reduce)").matches){{document.querySelectorAll(".tp .rv").forEach(function(e){{e.classList.add("in")}});return;}}'
            f'var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add("in");io.unobserve(e.target);}}}});}},{{threshold:.14}});'
            f'document.querySelectorAll(".tp .rv").forEach(function(e){{io.observe(e)}});}})();</script>'
            f'</section></div>')

CASES = {
 'bekobod1': {
  'rec':'rec2206284071','file':'mirror/bekobod1/index.html',
  'acc':'#2F8C20','acc2':'#43B02A','accrgb':'67,176,42','grid':'rgba(47,140,32,.12)',
  'kick':'Технопарк · Презентационный ролик','coord':'41.01°N 69.24°E · Ташкентская обл.',
  'title':'Технопарк <b>Бекабад</b>',
  'lead':'Промышленная площадка в Ташкентской области, создаваемая при участии Республики Башкортостан — как готовый инфраструктурный проект, а не идея на бумаге.',
  'spec':[('Клиент','Технопарк «Бекабад»'),('Регион','Ташкентская обл.'),('Партнёрство','UZ · Башкортостан'),('Формат','Презентация')],
  'video':'/portfolio/bekobod/brand-video.mp4','poster':'/portfolio/bekobod/poster.jpg',
  'cap':['Концепция','Мастер-план','Инфраструктура','Презентация инвесторам'],
  'about_label':'О площадке','about_h':'«Бекабад» — точка входа на рынки Центральной Азии',
  'stat':('UZ × RB','Межгосударственная кооперация'),
  'about_p':['Промышленная площадка, создаваемая при участии Республики Башкортостан на территории Ташкентской области. Ориентирована на размещение производственных, логистических и сервисных компаний, развитие научно-технологической и образовательной инфраструктуры вокруг резидентов.',
             'Задача технопарка — стать точкой входа для российского и международного бизнеса на рынки Центральной Азии через отстроенную инфраструктуру и механизмы межгосударственной кооперации.'],
  'steps':[
    {'n':'01 / ЗАДАЧА','h':'Показать готовый инфраструктурный проект',
     'p':['Объяснить понятно и наглядно, что «Бекабад» — реальный проект с продуманной архитектурой, логистикой и управлением. Важно было:'],
     'ul':['Показать масштаб территории и будущую инфраструктуру.','Объяснить условия для инвесторов и резидентов.','Подчеркнуть стратегическое значение площадки как выхода на рынки Центральной Азии.','Передать управляемость и готовность к приёму резидентов.']},
    {'n':'02 / РЕШЕНИЕ','h':'Визуальная экскурсия по будущему технопарку',
     'p':['Выстроили ролик как экскурсию: от общей концепции и мастер-плана до ключевых зон и возможностей для бизнеса.']},
    {'n':'03 / РЕЗУЛЬТАТ','h':'Инструмент презентации для инвесторов',
     'p':['Видео стало удобным инструментом презентации для инвесторов, делегаций и партнёров — быстро доносит суть и потенциал без погружения в проектную документацию.',
          'Визуализация территории показала «Бекабад» как готовое решение для бизнеса, а не план на бумаге — это особенно важно для международных инвесторов.']},
  ],
  'cards_label':'Три направления','cards':[
    ('01','Инфраструктура','Инженерные сети, транспортная доступность, производственные площади.'),
    ('02','Этапность','Что готово сейчас, что появится в следующих очередях, как масштабируется площадка.'),
    ('03','Управление','Кто стоит за проектом и как устроена поддержка резидентов.')],
 },
 'zubovo': {
  'rec':'rec2206287151','file':'mirror/zubovo/index.html',
  'acc':'#C4521A','acc2':'#E2571F','accrgb':'226,87,31','grid':'rgba(196,82,26,.12)',
  'kick':'Технопарк · Презентационный ролик','coord':'54.66°N 55.84°E · Уфа',
  'title':'Технопарк <b>Зубово</b>',
  'lead':'Индустриальная площадка рядом с Уфой — с действующими резидентами и готовой инфраструктурой. Живая площадка, а не проект «на бумаге».',
  'spec':[('Клиент','Технопарк «Зубово»'),('Регион','Башкортостан, Уфа'),('Площадь','≈ 78 га'),('Формат','Презентация')],
  'video':'/portfolio/zubovo/brand-video.mp4','poster':'/portfolio/zubovo/poster.jpg',
  'cap':['Сценарий','Съёмка территории','Производства','Презентация резидентам'],
  'about_label':'О площадке','about_h':'«Зубово» — живая промышленная площадка под Уфой',
  'stat':('78 ГА','Площадь индустриальной площадки'),
  'about_p':['Индустриальная площадка около 78 гектаров в непосредственной близости от Уфы, с удобным доступом к основным транспортным магистралям. Резидентам предоставляются готовые производственные корпуса, административные помещения и земельные участки с подведёнными инженерными сетями.',
             'На территории уже работают крупные резиденты, в том числе компании, инвестировавшие сотни миллионов и миллиарды рублей в собственные производства, создавая рабочие места и ядро промышленного кластера региона.'],
  'steps':[
    {'n':'01 / ЗАДАЧА','h':'Показать живую площадку, а не проект «на бумаге»',
     'p':['Объяснить наглядно, почему «Зубово» — удобная точка входа для бизнеса в Башкортостане: сформировавшаяся площадка с реальными резидентами и понятными условиями.'],
     'ul':['Подчеркнуть инновационную специализацию технопарка.','Показать вклад в политику импортозамещения.','Продемонстрировать, что здесь есть всё для запуска и масштабирования высокотехнологичных проектов.']},
    {'n':'02 / РЕШЕНИЕ','h':'Технопарк глазами потенциального резидента',
     'p':['Выстроили ролик как рассказ о возможностях глазами резидента: масштабы территории, производственные корпуса, транспортная доступность и примеры уже работающих компаний.']},
    {'n':'03 / РЕЗУЛЬТАТ','h':'Готовая площадка, которой доверяют',
     'p':['Ролик используется на встречах с инвесторами, делегациями, властью и потенциальными резидентами — в презентациях и на цифровых площадках.',
          'Наглядная визуализация территории и работающих производств повышает доверие: «Зубово» воспринимается как реальная, живая площадка для бизнеса.']},
  ],
  'cards_label':'Три ключевых блока','cards':[
    ('01','Инфраструктура','Готовые площади, инженерные сети, дороги, парковки.'),
    ('02','Бизнес-возможности','Участки под строительство, гибкие форматы размещения, сервисная поддержка.'),
    ('03','Стратегический контекст','Роль «Зубово» в промышленной политике региона и развитии инноваций.')],
 },
}

for key, cfg in CASES.items():
    f = cfg['file']
    s = open(f, encoding='utf-8', errors='ignore').read()
    start = s.index(f'<div id="{cfg["rec"]}"')
    end = start + 10 + re.search(r'<div id="rec\d+"', s[start + 10:]).start()
    s2 = s[:start] + render(cfg) + s[end:]
    s2 = s2.replace("window.mainTracker='tilda'", "window.mainTracker='custom'")
    open(f, 'w').write(s2)
    print(f'{key}: showcase вставлен, размер {len(s2)}')
