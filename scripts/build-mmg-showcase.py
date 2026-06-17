#!/usr/bin/env python3
"""Кинематографичный showcase-дизайн кейса MMG / «Павелецкая Плаза».
Заменяет только контент-rec (rec2198174601). Шапка/CTA/подвал — родные."""
import re, math, random

# --- генерим золотую параметрическую решётку (триангулированный меш) как у купола ---
def lattice_svg(w=1200, h=220, cols=24, rows=5, seed=7):
    random.seed(seed)
    pts = []
    for r in range(rows + 1):
        row = []
        for c in range(cols + 1):
            x = c * (w / cols) + (0 if r % 2 == 0 else (w / cols) / 2)
            y = r * (h / rows) + random.uniform(-6, 6)
            row.append((round(x, 1), round(y, 1)))
        pts.append(row)
    lines = []
    for r in range(rows):
        for c in range(cols):
            a = pts[r][c]; b = pts[r][c + 1]; d = pts[r + 1][c]
            lines.append((a, b)); lines.append((a, d))
            if c == cols - 1:
                lines.append((pts[r][c + 1], pts[r + 1][c + 1]))
        lines.append((pts[r][cols], pts[r + 1][cols]))
    for c in range(cols):
        lines.append((pts[rows][c], pts[rows][c + 1]))
    # диагонали для триангуляции
    for r in range(rows):
        for c in range(cols):
            lines.append((pts[r][c + 1], pts[r + 1][c]))
    body = ''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for a, b in lines)
    return (f'<svg class="pp__mesh" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">'
            f'<g stroke="url(#ppg)" stroke-width="1" fill="none">{body}</g>'
            f'<defs><linearGradient id="ppg" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="#7a5e22"/><stop offset=".5" stop-color="#E7C66B"/>'
            f'<stop offset="1" stop-color="#7a5e22"/></linearGradient></defs></svg>')

MESH = lattice_svg()

SECTION = '''<div id="rec2198174601" class="r t-rec" style="background:#0B0B0D;" data-record-type="custom"><section class="pp"><style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Onest:wght@400;500;600;700&display=swap');
.pp{--ink:#0B0B0D;--ink2:#101117;--cream:#F3ECDD;--mut:#9A9385;--dim:#6A6456;--gold:#C9A24B;--gold2:#E7C66B;--line:rgba(231,198,107,.18);--ease:cubic-bezier(.16,1,.3,1);
 background:var(--ink);color:var(--cream);font-family:'Onest',system-ui,sans-serif;font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow:hidden;position:relative}
.pp *{box-sizing:border-box}\n.pp::before{content:"";position:absolute;top:0;left:0;right:0;height:150px;z-index:1;pointer-events:none;background:linear-gradient(180deg,#F4EFE4 0%,#cdbc9d 14%,#6f6550 34%,#22201b 64%,#0B0B0D 100%)}
.pp ::selection{background:var(--gold);color:#000}
.pp__wrap{max-width:1140px;margin:0 auto;padding:0 24px;position:relative;z-index:2}
.pp__kick{font-size:12px;letter-spacing:.34em;text-transform:uppercase;color:var(--gold);font-weight:600;margin:0 0 26px;display:flex;gap:14px;align-items:center}
.pp__kick::before{content:"";width:34px;height:1px;background:var(--gold)}
.pp__hero{padding:104px 0 30px;position:relative}
.pp__title{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;color:var(--cream);
 font-size:clamp(52px,15vw,124px);line-height:.92;letter-spacing:-.01em;margin:0 0 8px}
.pp__title em{font-style:italic;color:var(--gold2)}
.pp__sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:clamp(20px,5vw,30px);color:var(--mut);margin:0 0 36px}
.pp__lead{max-width:600px;color:#D9D2C4;font-size:clamp(16px,4vw,18px);margin:0 0 40px}
/* video cinematic frame */
.pp__stage{position:relative;border:1px solid var(--line);border-radius:2px;overflow:hidden;background:#000;
 box-shadow:0 50px 120px -50px rgba(0,0,0,.9),0 0 0 1px rgba(231,198,107,.06)}
.pp__stage video,.pp__stage img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#000}
.pp__pb{position:absolute;inset:0;border:0;width:100%;padding:0;cursor:pointer;background-size:cover;background-position:center;
 display:flex;align-items:center;justify-content:center;transition:.5s var(--ease)}
.pp__pb::after{content:"";position:absolute;inset:0;background:radial-gradient(60% 80% at 50% 50%,transparent,rgba(0,0,0,.5))}
.pp__play{position:relative;width:92px;height:92px;border-radius:50%;border:1px solid var(--gold);
 display:grid;place-items:center;background:rgba(11,11,13,.35);backdrop-filter:blur(3px);transition:.4s var(--ease)}
.pp__play::before{content:"";width:92px;height:92px;border-radius:50%;position:absolute;border:1px solid var(--gold);animation:ppr 3s ease-out infinite}
.pp__play::after{content:"";margin-left:6px;border-style:solid;border-width:11px 0 11px 19px;border-color:transparent transparent transparent var(--gold2)}
.pp__pb:hover .pp__play{transform:scale(1.08);background:rgba(231,198,107,.12)}
@keyframes ppr{0%{transform:scale(1);opacity:.6}100%{transform:scale(1.5);opacity:0}}
.pp__tick{position:absolute;width:14px;height:14px;border-color:var(--gold);opacity:.7}
.pp__tick.tl{top:10px;left:10px;border-top:1px solid;border-left:1px solid}
.pp__tick.tr{top:10px;right:10px;border-top:1px solid;border-right:1px solid}
.pp__tick.bl{bottom:10px;left:10px;border-bottom:1px solid;border-left:1px solid}
.pp__tick.br{bottom:10px;right:10px;border-bottom:1px solid;border-right:1px solid}
/* credits strip */
.pp__credits{display:flex;flex-wrap:wrap;gap:10px 26px;margin:22px 0 0;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}
.pp__credits b{color:var(--mut);font-weight:600}
.pp__credits span{display:flex;gap:26px}
.pp__credits span::after{content:"·";color:var(--gold)}
.pp__credits span:last-child::after{display:none}
/* mesh signature */
.pp__mesh{position:absolute;left:0;right:0;width:100%;height:220px;opacity:.5}
.pp__meshwrap{position:relative;height:220px;margin:8px 0;display:flex;align-items:center}
.pp__meshwrap::after{content:"";position:absolute;inset:0;background:radial-gradient(60% 120% at 50% 50%,transparent,var(--ink))}
.pp__bgmesh{position:absolute;top:-40px;right:-10%;width:80%;height:520px;opacity:.14;z-index:0;pointer-events:none}
/* sections */
.pp__sec{padding:60px 0;border-top:1px solid rgba(255,255,255,.05)}
.pp__label{font-family:'Onest';font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);margin:0 0 28px;font-weight:600}
.pp__about{display:grid;gap:30px}
@media(min-width:860px){.pp__about{grid-template-columns:.9fr 1.1fr;gap:60px}}
.pp__about h2{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:clamp(30px,6vw,44px);line-height:1.04;margin:0;color:var(--cream)}
.pp__about p{margin:0 0 16px;color:#CFC8BA}
.pp__about p.drop::first-letter{font-family:'Cormorant Garamond',serif;font-size:3.4em;float:left;line-height:.8;padding:6px 12px 0 0;color:var(--gold2)}
.pp__facts{display:flex;flex-wrap:wrap;gap:0 30px;margin-top:26px;border-top:1px solid var(--line)}
.pp__fact{flex:1 1 80px;min-width:80px;padding:16px 0;border-bottom:1px solid rgba(255,255,255,.05)}
.pp__fact .n{font-family:'Cormorant Garamond',serif;font-size:34px;color:var(--gold2);font-variant-numeric:tabular-nums;line-height:1}
.pp__fact .t{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);margin-top:6px}
/* process editorial */
.pp__steps{display:grid;gap:0}
.pp__step{display:grid;grid-template-columns:auto 1fr;gap:24px;padding:34px 0;border-top:1px solid rgba(255,255,255,.07)}
.pp__step:last-child{border-bottom:1px solid rgba(255,255,255,.07)}
@media(max-width:640px){.pp__step{grid-template-columns:1fr;gap:14px}}
.pp__num{font-family:'Cormorant Garamond',serif;font-size:clamp(44px,9vw,72px);color:var(--gold);line-height:.8;font-variant-numeric:tabular-nums;opacity:.9}
.pp__step h3{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:clamp(24px,5.5vw,34px);margin:0 0 14px;color:var(--cream);line-height:1.06}
.pp__step p{margin:0 0 14px;color:#CFC8BA}
.pp__method{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:0}
.pp__method li{display:grid;grid-template-columns:auto 1fr;gap:16px;padding:14px 0;border-top:1px solid rgba(255,255,255,.06);align-items:baseline}
.pp__method .mk{font-family:'Cormorant Garamond',serif;font-style:italic;color:var(--gold2);font-size:18px;white-space:nowrap}
.pp__method .mv{color:var(--mut);font-size:15px}
/* pull quote */
.pp__quote{padding:70px 0;text-align:center}
.pp__quote blockquote{margin:0 auto;max-width:760px;font-family:'Cormorant Garamond',serif;font-weight:500;
 font-size:clamp(26px,6.2vw,46px);line-height:1.18;color:var(--cream)}
.pp__quote blockquote em{font-style:italic;color:var(--gold2)}
.pp__quote .by{margin-top:24px;font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--dim)}
/* reveal */
.pp .rv{opacity:0;transform:translateY(26px);transition:opacity 1s var(--ease),transform 1s var(--ease)}
.pp .rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.pp .rv{opacity:1;transform:none;transition:none}.pp__play::before{animation:none}}
</style>

''' + f'''<svg class="pp__bgmesh" viewBox="0 0 1200 520" preserveAspectRatio="none" aria-hidden="true"><g stroke="#E7C66B" stroke-width="1" fill="none" opacity=".7">{MESH[MESH.index('>')+1:MESH.index('<defs')]}</g></svg>

<div class="pp__wrap">
  <header class="pp__hero">
    <p class="pp__kick">Mall Management Group · Москва</p>
    <h1 class="pp__title rv">Павелецкая <em>Плаза</em></h1>
    <p class="pp__sub rv">Рекламный ролик торгово-развлекательного центра</p>
    <p class="pp__lead rv">Высокая стадия готовности ТРЦ, снятая так, чтобы её увидел и почувствовал будущий арендатор: масштаб, локация, концепция и спрос — в одном фильме.</p>
    <div class="pp__stage rv">
      <video id="ppfilm" playsinline preload="none" controls poster="/portfolio/mmg/poster.jpg"><source src="/portfolio/mmg/brand-video.mp4" type="video/mp4"></video>
      <button class="pp__pb" id="pppb" style="background-image:url('/portfolio/mmg/poster.jpg')" aria-label="Смотреть рекламный ролик «Павелецкая Плаза»"><span class="pp__play"></span></button>
      <i class="pp__tick tl"></i><i class="pp__tick tr"></i><i class="pp__tick bl"></i><i class="pp__tick br"></i>
    </div>
    <div class="pp__credits rv"><span><b>Сценарий</b></span><span><b>Аэросъёмка</b></span><span><b>Постпродакшн</b></span><span><b>Хронометраж</b> 5:37</span></div>
  </header>
</div>

<div class="pp__meshwrap rv">{MESH}</div>

<div class="pp__wrap">
  <section class="pp__sec pp__about rv">
    <div>
      <p class="pp__label">О девелопере</p>
      <h2>Mall Management Group — коммерческая недвижимость полного цикла</h2>
      <div class="pp__facts">
        <div class="pp__fact"><div class="n">Plaza B.V.</div><div class="t">Группа</div></div>
        <div class="pp__fact"><div class="n">ТРЦ</div><div class="t">Формат</div></div>
        <div class="pp__fact"><div class="n">5:37</div><div class="t">Хронометраж</div></div>
      </div>
    </div>
    <div>
      <p class="drop">Компания Mall Management Group занимается девелопментом и созданием качественных объектов коммерческой недвижимости, а также сопровождением полного цикла жизни проектов.</p>
      <p>MMG входит в группу «Plaza B.V.», контролируемую Сергеем Гордеевым, и управляет портфелем коммерческой недвижимости. «Павелецкая Плаза» — один из её флагманских объектов в Москве.</p>
    </div>
  </section>

  <section class="pp__sec rv">
    <p class="pp__label">Как снимали</p>
    <div class="pp__steps">
      <div class="pp__step">
        <div class="pp__num">01</div>
        <div>
          <h3>Сценарий и продакшн под арендаторов</h3>
          <p>Разработать сценарий ролика, который показывает высокую стадию готовности ТРЦ и его ключевые преимущества для арендаторов. Дальше — съёмки и постпродакшн под этот нарратив.</p>
        </div>
      </div>
      <div class="pp__step">
        <div class="pp__num">02</div>
        <div>
          <h3>Съёмка на финальной стадии строительства</h3>
          <p>ТРЦ был на финальной стадии — поэтому фильм собран из нескольких слоёв материала, каждый со своей задачей:</p>
          <ul class="pp__method">
            <li><span class="mk">Аэросъёмка</span><span class="mv">обозначает локацию и масштаб проекта.</span></li>
            <li><span class="mk">Коммерческие кадры</span><span class="mv">служат фоном для инфографики.</span></li>
            <li><span class="mk">Интервью с основателями</span><span class="mv">компаний-арендаторов — как залог успешности проекта.</span></li>
            <li><span class="mk">Уличные интервью</span><span class="mv">с будущими покупателями — подтверждение выбора места и концепции.</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</div>

<div class="pp__wrap">
  <section class="pp__quote rv">
    <blockquote>Стройку показали так, чтобы арендатор увидел <em>готовый поток</em> — людей, локацию и спрос, а не бетон.</blockquote>
    <div class="by">Hand Marketing · видеопродакшн</div>
  </section>
</div>

<script>(function(){{
  var v=document.getElementById('ppfilm'),p=document.getElementById('pppb');
  if(v&&p){{p.addEventListener('click',function(){{p.style.opacity='0';p.style.pointerEvents='none';v.play();}});
    v.addEventListener('pause',function(){{if(v.currentTime===0){{p.style.opacity='1';p.style.pointerEvents='';}}}});}}
  if(matchMedia('(prefers-reduced-motion:reduce)').matches){{document.querySelectorAll('.pp .rv').forEach(function(e){{e.classList.add('in')}});return;}}
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}});}},{{threshold:.14}});
  document.querySelectorAll('.pp .rv').forEach(function(e){{io.observe(e)}});
}})();</script>
</section></div>
'''

f = 'mirror/mmg/index.html'
s = open(f, encoding='utf-8', errors='ignore').read()
start = s.index('<div id="rec2198174601"')
end = start + 10 + re.search(r'<div id="rec\d+"', s[start + 10:]).start()
s2 = s[:start] + SECTION + s[end:]
s2 = s2.replace("window.mainTracker='tilda'", "window.mainTracker='custom'")
open(f, 'w').write(s2)
print('MMG showcase вставлен, размер', len(s2))
