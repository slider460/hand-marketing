#!/usr/bin/env python3
"""Вставляет фирменный (HM) контент-блок вместо исходного rec в кейсах mmg/bekobod1/zubovo.
Шапка, бургер-меню, CTA-форма и подвал страницы остаются родными."""
import re, html, os

CSS = r'''<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Raleway:wght@400;500;600;700&display=swap');
.hmc{--ink:#161616;--body:#4a4a4a;--mut:#8a8a8a;--bg:#ffffff;--soft:#f5f5f3;--line:#e7e7e3;
 --green:#5e9a2e;--orange:#cf6f19;--purple:#673a7e;--pink:#c12164;--acc:var(--orange);
 background:var(--bg);color:var(--body);font-family:'Raleway',Arial,sans-serif;font-size:17px;line-height:1.62;padding:18px 0 8px}
.hmc *{box-sizing:border-box}
.hmc__wrap{max-width:1100px;margin:0 auto;padding:0 22px}
.hmc h2,.hmc h3,.hmc .h1{font-family:'Montserrat',Arial,sans-serif;color:var(--ink);letter-spacing:-.01em}
.hmc__eyebrow{font-family:'Montserrat';font-weight:700;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--mut);margin:0 0 16px;display:flex;align-items:center;gap:10px}
.hmc__eyebrow::before{content:"";width:30px;height:4px;border-radius:3px;background:linear-gradient(90deg,var(--green),var(--orange) 40%,var(--purple) 70%,var(--pink))}
.hmc .h1{font-weight:800;font-size:clamp(34px,8.5vw,62px);line-height:1.02;color:var(--ink);margin:0 0 20px}
.hmc .h1 em{font-style:normal;color:var(--acc)}
.hmc__lead{max-width:640px;font-size:clamp(17px,4.2vw,20px);color:var(--body);margin:0 0 30px}
.hmc__meta{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:14px;overflow:hidden;max-width:640px;margin:0 0 40px}
.hmc__meta div{padding:15px 18px;border-bottom:1px solid var(--line)}
.hmc__meta div:nth-child(odd){border-right:1px solid var(--line)}
.hmc__meta div:nth-last-child(-n+2){border-bottom:0}
.hmc__meta dt{font-family:'Montserrat';font-weight:700;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin:0 0 4px}
.hmc__meta dd{margin:0;font-weight:600;color:var(--ink);font-size:15.5px}
.hmc__video{position:relative;border-radius:18px;overflow:hidden;background:#0c0c0c;box-shadow:0 24px 60px -34px rgba(0,0,0,.5);margin:0 0 48px}
.hmc__video video,.hmc__video img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#000}
.hmc__pb{position:absolute;inset:0;border:0;width:100%;padding:0;cursor:pointer;background-size:cover;background-position:center;display:flex;align-items:center;justify-content:center}
.hmc__play{width:78px;height:78px;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 10px 30px rgba(0,0,0,.35);transition:transform .22s}
.hmc__pb:hover .hmc__play{transform:scale(1.08)}
.hmc__play::after{content:"";margin-left:5px;border-style:solid;border-width:12px 0 12px 20px;border-color:transparent transparent transparent var(--ink)}
.hmc__about{display:grid;gap:24px;margin:0 0 50px}
@media(min-width:840px){.hmc__about{grid-template-columns:.8fr 1.2fr;gap:46px;align-items:start}}
.hmc__about h2{font-size:clamp(24px,6vw,34px);font-weight:800;line-height:1.1;margin:0 0 16px}
.hmc__about p{margin:0 0 15px}
.hmc__tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.hmc__tag{font-size:13px;font-weight:600;color:var(--ink);background:var(--soft);border:1px solid var(--line);padding:7px 13px;border-radius:999px}
.hmc__seclabel{font-family:'Montserrat';font-weight:700;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--mut);margin:0 0 22px;display:flex;align-items:center;gap:11px}
.hmc__seclabel::before{content:"";width:26px;height:3px;border-radius:3px;background:var(--ink)}
.hmc__steps{display:grid;gap:14px;margin:0 0 50px}
.hmc__step{position:relative;border:1px solid var(--line);border-radius:16px;background:#fff;padding:24px 22px 24px 26px;overflow:hidden}
.hmc__step::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px}
.hmc__step.g::before{background:var(--green)} .hmc__step.o::before{background:var(--orange)} .hmc__step.p::before{background:var(--purple)}
.hmc__n{font-family:'Montserrat';font-weight:800;font-size:13px;letter-spacing:.1em;text-transform:uppercase}
.hmc__step.g .hmc__n{color:var(--green)} .hmc__step.o .hmc__n{color:var(--orange)} .hmc__step.p .hmc__n{color:var(--purple)}
.hmc__step h3{font-size:clamp(20px,5vw,26px);font-weight:700;margin:7px 0 12px;line-height:1.12}
.hmc__step p{margin:0 0 12px}
.hmc__step ul{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:9px}
.hmc__step li{position:relative;padding-left:22px;font-size:15.5px}
.hmc__step li::before{content:"";position:absolute;left:0;top:9px;width:8px;height:8px;border-radius:50%;background:currentColor}
.hmc__step.g li::before{color:var(--green)} .hmc__step.o li::before{color:var(--orange)} .hmc__step.p li::before{color:var(--purple)}
.hmc__step b{color:var(--ink)}
</style>'''

def esc(t): return html.escape(t, quote=False)

def step_html(cls, n, title, paras, bullets):
    out = f'<div class="hmc__step {cls}"><div class="hmc__n">{esc(n)}</div><h3>{esc(title)}</h3>'
    for p in paras: out += f'<p>{p}</p>'
    if bullets:
        out += '<ul>' + ''.join(f'<li>{b}</li>' for b in bullets) + '</ul>'
    return out + '</div>'

def build_section(cfg):
    meta = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in cfg['meta'])
    if cfg.get('video'):
        media = (f'<div class="hmc__video"><video id="hmcfilm" playsinline preload="none" controls poster="{cfg["poster"]}">'
                 f'<source src="{cfg["video"]}" type="video/mp4"></video>'
                 f'<button class="hmc__pb" id="hmcpb" style="background-image:url(\'{cfg["poster"]}\')" aria-label="Смотреть ролик"><span class="hmc__play"></span></button></div>'
                 '<script>(function(){var v=document.getElementById("hmcfilm"),p=document.getElementById("hmcpb");if(v&&p){p.addEventListener("click",function(){p.style.display="none";v.play();});v.addEventListener("pause",function(){if(v.currentTime===0)p.style.display="";});}})();</script>')
    else:
        media = f'<div class="hmc__video"><img src="{cfg["poster"]}" alt="{esc(cfg["title_plain"])}"></div>'
    tags = ''.join(f'<span class="hmc__tag">{esc(t)}</span>' for t in cfg['tags'])
    steps = ''.join(step_html(*s) for s in cfg['steps'])
    return (f'<div id="{cfg["rec"]}" class="r t-rec" style="background-color:#ffffff;" data-record-type="custom">'
            f'<section class="hmc" style="--acc:{cfg["acc"]}">{CSS}<div class="hmc__wrap">'
            f'<p class="hmc__eyebrow">{esc(cfg["eyebrow"])}</p>'
            f'<div class="h1">{cfg["title_html"]}</div>'
            f'<p class="hmc__lead">{esc(cfg["lead"])}</p>'
            f'<dl class="hmc__meta">{meta}</dl>'
            f'{media}'
            f'<div class="hmc__about"><div><h2>{esc(cfg["about_h"])}</h2><div class="hmc__tags">{tags}</div></div>'
            f'<div>{"".join(f"<p>{esc(p)}</p>" for p in cfg["about_p"])}</div></div>'
            f'<p class="hmc__seclabel">Как мы это сделали</p><div class="hmc__steps">{steps}</div>'
            f'</div></section></div>')

CASES = {
 'mmg': {
  'rec':'rec2198174601','acc':'var(--pink)',
  'eyebrow':'Mall Management Group · Видеопродакшн',
  'title_html':'Рекламный ролик <em>«Павелецкая Плаза»</em>','title_plain':'Рекламный ролик «Павелецкая Плаза»',
  'lead':'Ролик, показывающий высокую стадию готовности ТРЦ и демонстрирующий ключевые преимущества для арендаторов.',
  'meta':[('Клиент','Mall Management Group'),('Объект','ТРЦ «Павелецкая Плаза»'),('Формат','Рекламный ролик'),('Группа','Plaza B.V.')],
  'poster':'/portfolio/mmg/poster.jpg',
  'about_h':'Mall Management Group — девелопмент коммерческой недвижимости',
  'about_p':['Компания Mall Management Group (MMG) занимается девелопментом и созданием качественных объектов коммерческой недвижимости, а также сопровождением полного цикла жизни проектов.',
             'MMG входит в группу «Plaza B.V.», контролируемую Сергеем Гордеевым, и управляет портфелем коммерческой недвижимости.'],
  'tags':['Коммерческая недвижимость','Девелопмент','ТРЦ'],
  'steps':[
    ('g','01 — Задача','Сценарий и продакшн под арендаторов',[],
     ['Разработать сценарий ролика, показывающий высокую стадию готовности ТРЦ и преимущества для арендаторов.','Осуществить съёмки и постпродакшн ролика.']),
    ('o','02 — Решение','Съёмка на финальной стадии строительства',
     ['Так как сам ТРЦ находился на финальной стадии строительства, мы собрали ролик из нескольких слоёв материала:'],
     ['<b>Аэросъёмка</b> — для обозначения локации и масштабности проекта.','<b>Коммерческие кадры</b> — в качестве фона для инфографики.','<b>Интервью с основателями</b> компаний, уже ставших арендаторами, — как залог успешности проекта.','<b>Уличные интервью</b> с будущими покупателями — для подтверждения правильного выбора места и концепции.']),
  ],
 },
 'bekobod1': {
  'rec':'rec2206284071','acc':'var(--green)',
  'eyebrow':'Технопарк · Презентационный ролик',
  'title_html':'Технопарк <em>«Бекабад»</em>','title_plain':'Технопарк «Бекабад»',
  'lead':'Презентационный ролик о промышленной площадке в Ташкентской области, создаваемой при участии Республики Башкортостан.',
  'meta':[('Клиент','Технопарк «Бекабад»'),('Регион','Ташкентская область'),('Партнёрство','Узбекистан · Башкортостан'),('Формат','Презентационный ролик')],
  'video':'/portfolio/bekobod/brand-video.mp4','poster':'/portfolio/bekobod/poster.jpg',
  'about_h':'«Бекабад» — точка входа на рынки Центральной Азии',
  'about_p':['Промышленная площадка, создаваемая при участии Республики Башкортостан на территории Ташкентской области. Проект ориентирован на размещение производственных предприятий, логистических и сервисных компаний, а также развитие научно-технологической и образовательной инфраструктуры вокруг резидентов.',
             'Задача технопарка — стать точкой входа для российского и международного бизнеса на рынки Центральной Азии через отстроенную инфраструктуру и механизмы межгосударственной кооперации.'],
  'tags':['Промышленная площадка','Инвестиции и резиденты','Центральная Азия'],
  'steps':[
    ('g','01 — Задача','Показать готовый инфраструктурный проект',
     ['Создать видео, которое понятно и наглядно объяснит, что «Бекабад» — не абстрактная идея, а реальный проект с продуманной архитектурой, логистикой и управлением. Важно было:'],
     ['Показать масштаб территории и будущую инфраструктуру.','Объяснить условия для инвесторов и резидентов.','Подчеркнуть стратегическое значение площадки как точки выхода на рынки Центральной Азии.','Передать управляемость проекта и готовность инфраструктуры к приёму резидентов.']),
    ('o','02 — Решение','Визуальная экскурсия по будущему технопарку',
     ['Выстроили ролик как экскурсию: от общей концепции и мастер-плана до ключевых зон и возможностей для бизнеса. Сделали акцент на трёх направлениях:'],
     ['<b>Инфраструктура</b> — инженерные сети, транспортная доступность, производственные площади.','<b>Этапность реализации</b> — что готово сейчас, что появится в следующих очередях, как масштабируется площадка.','<b>Управление и готовность</b> — кто стоит за проектом и как устроена поддержка резидентов.']),
    ('p','03 — Результат','Инструмент презентации для инвесторов',
     ['Видеоролик стал удобным инструментом презентации проекта для инвесторов, делегаций и партнёров — позволяет быстро донести суть и потенциал технопарка без погружения в проектную документацию.',
      'Формат видео усилил доверие: визуализация территории помогла показать «Бекабад» как готовое решение для размещения бизнеса, а не как план на бумаге. Это особенно важно в работе с международными инвесторами.'],[]),
  ],
 },
 'zubovo': {
  'rec':'rec2206287151','acc':'var(--purple)',
  'eyebrow':'Технопарк · Презентационный ролик',
  'title_html':'Технопарк <em>«Зубово»</em>','title_plain':'Технопарк «Зубово»',
  'lead':'Презентационный ролик об индустриальной площадке около 78 гектаров рядом с Уфой — с действующими резидентами и готовой инфраструктурой.',
  'meta':[('Клиент','Технопарк «Зубово»'),('Регион','Башкортостан, Уфа'),('Площадь','≈ 78 гектаров'),('Формат','Презентационный ролик')],
  'video':'/portfolio/zubovo/brand-video.mp4','poster':'/portfolio/zubovo/poster.jpg',
  'about_h':'«Зубово» — живая промышленная площадка под Уфой',
  'about_p':['Индустриальная площадка площадью около 78 гектаров в непосредственной близости от Уфы, с удобным доступом к основным транспортным магистралям. Резидентам предоставляются готовые производственные корпуса, административные помещения и земельные участки с подведёнными инженерными сетями.',
             'На территории уже работают крупные резиденты, в том числе компании, инвестировавшие сотни миллионов и миллиарды рублей в собственные производства, создавая рабочие места и формируя ядро промышленного кластера региона.'],
  'tags':['Индустриальная площадка','78 гектаров','Импортозамещение'],
  'steps':[
    ('g','01 — Задача','Показать живую площадку, а не проект «на бумаге»',
     ['Создать ролик, который наглядно объясняет, почему «Зубово» — удобная точка входа для бизнеса в Башкортостане: уже сформировавшаяся площадка с реальными резидентами, действующими производствами и понятными условиями.'],
     ['Подчеркнуть инновационную специализацию технопарка.','Показать вклад в политику импортозамещения.','Продемонстрировать, что здесь есть всё для запуска и масштабирования высокотехнологичных проектов.']),
    ('o','02 — Решение','Технопарк глазами потенциального резидента',
     ['Выстроили ролик как рассказ о возможностях технопарка глазами резидента: масштабы территории, производственные корпуса, транспортная доступность и примеры уже работающих компаний. Акцент на трёх блоках:'],
     ['<b>Инфраструктура</b> — готовые площади, инженерные сети, дороги, парковки.','<b>Бизнес-возможности</b> — участки под строительство, гибкие форматы размещения, сервисная поддержка.','<b>Стратегический контекст</b> — роль «Зубово» в промышленной политике региона.']),
    ('p','03 — Результат','Готовая площадка, которой доверяют',
     ['Ролик стал удобным инструментом презентации технопарка для инвесторов, делегаций, представителей власти и потенциальных резидентов — используется на встречах, в презентациях и на цифровых площадках.',
      'Благодаря наглядной визуализации территории и уже работающих производств «Зубово» воспринимается как реальная, живая площадка для размещения бизнеса — это повышает доверие к проекту.'],[]),
  ],
 },
}

PAGES = {'mmg':'mirror/mmg/index.html','bekobod1':'mirror/bekobod1/index.html','zubovo':'mirror/zubovo/index.html'}

for key, cfg in CASES.items():
    f = PAGES[key]
    s = open(f, encoding='utf-8', errors='ignore').read()
    rec = cfg['rec']
    start = s.index(f'<div id="{rec}"')
    nxt = re.search(r'<div id="rec\d+"', s[start+10:])
    end = start + 10 + nxt.start()
    s2 = s[:start] + build_section(cfg) + s[end:]
    # дочистка mainTracker
    s2 = s2.replace("window.mainTracker='tilda'", "window.mainTracker='custom'")
    open(f, 'w').write(s2)
    print(f'{key}: заменён {rec}, новый размер {len(s2)}')
