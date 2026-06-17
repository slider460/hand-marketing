#!/usr/bin/env python3
"""Креативный светлый showcase ISOTEC: инженерный/термографический.
Сигнатура — тепловая шкала тепловизора. Заменяет только контент-rec."""
import re, html

def esc(t): return html.escape(t, quote=False)

SECTION = '''<div id="rec137505836_iso" class="r t-rec" style="background:#FFFFFF;" data-record-type="custom"><section class="iz"><style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Onest:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');
.iz{--bg:#FFFFFF;--bg2:#F5F6F8;--text:#474C54;--head:#13161B;--dim:#8A909A;--faint:#B4BAC2;
 --blue:#1E4FD0;--line:rgba(20,23,28,.11);--ease:cubic-bezier(.16,1,.3,1);
 --therm:linear-gradient(90deg,#1E51C8 0%,#7A33C0 30%,#E0531C 64%,#F6B73C 100%);
 background:var(--bg);color:var(--text);font-family:'Onest',system-ui,sans-serif;font-size:17px;line-height:1.62;
 -webkit-font-smoothing:antialiased;position:relative;overflow:hidden}
.iz *{box-sizing:border-box}
.iz ::selection{background:var(--blue);color:#fff}
.iz__wrap{max-width:1120px;margin:0 auto;padding:0 24px;position:relative;z-index:2}
/* thermal scale signature */
.iz__scale{position:relative;height:10px;border-radius:6px;background:var(--therm);max-width:560px;margin:0 0 8px;
 box-shadow:0 6px 22px -8px rgba(224,83,28,.4)}
.iz__scale::after{content:"";position:absolute;inset:0;border-radius:6px;
 background:repeating-linear-gradient(90deg,transparent 0 27px,rgba(255,255,255,.55) 27px 28px)}
.iz__scalab{display:flex;justify-content:space-between;max-width:560px;font-family:'JetBrains Mono',monospace;
 font-size:10.5px;letter-spacing:.05em;color:var(--dim);margin:0 0 34px}
/* hero */
.iz__hero{padding:34px 0 26px}
.iz__kick{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);
 margin:0 0 22px;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-weight:500}
.iz__kick .sq{width:9px;height:9px;background:var(--therm);display:inline-block}
.iz__title{font-family:'Manrope',sans-serif;font-weight:800;color:var(--head);
 font-size:clamp(38px,10.5vw,84px);line-height:1.0;letter-spacing:-.03em;margin:0 0 22px}
.iz__title em{font-style:normal;background:var(--therm);-webkit-background-clip:text;background-clip:text;color:transparent}
.iz__lead{max-width:600px;font-size:clamp(16px,4.2vw,20px);color:#3D434B;margin:0 0 30px}
/* spec */
.iz__spec{display:grid;grid-template-columns:repeat(2,1fr);border:1px solid var(--line);max-width:640px;margin:0 0 40px;background:var(--bg2)}
@media(min-width:720px){.iz__spec{grid-template-columns:repeat(4,1fr)}}
.iz__spec div{padding:15px 16px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.iz__spec dt{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--dim);margin:0 0 6px}
.iz__spec dd{margin:0;font-weight:600;color:var(--head);font-size:14.5px}
/* video */
.iz__stage{position:relative;border:1px solid var(--line);overflow:hidden;background:#0c0d10;box-shadow:0 30px 70px -42px rgba(20,23,28,.4)}
.iz__stage video,.iz__stage img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#000}
.iz__pb{position:absolute;inset:0;border:0;width:100%;padding:0;cursor:pointer;background-size:cover;background-position:center;
 display:flex;align-items:center;justify-content:center;transition:.5s var(--ease)}
.iz__pb::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,12,15,.05),rgba(10,12,15,.4))}
.iz__play{position:relative;width:86px;height:86px;border-radius:50%;background:var(--therm);padding:2px;transition:.35s var(--ease);z-index:1}
.iz__play i{width:100%;height:100%;border-radius:50%;background:#fff;display:grid;place-items:center}
.iz__play i::after{content:"";margin-left:5px;border-style:solid;border-width:11px 0 11px 18px;border-color:transparent transparent transparent #E0531C}
.iz__pb:hover .iz__play{transform:scale(1.08)}
.iz__cap{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:16px;font-family:'JetBrains Mono',monospace;font-size:11.5px;letter-spacing:.06em;color:var(--faint);text-transform:uppercase}
.iz__cap b{color:var(--dim);font-weight:500}
/* sections */
.iz__sec{padding:56px 0;border-top:1px solid var(--line)}
.iz__label{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--blue);margin:0 0 24px;display:flex;align-items:center;gap:12px;font-weight:500}
.iz__label::before{content:"";width:24px;height:3px;border-radius:2px;background:var(--therm)}
.iz__about{display:grid;gap:28px}
@media(min-width:860px){.iz__about{grid-template-columns:1fr 1.15fr;gap:54px;align-items:start}}
.iz__about h2{font-family:'Manrope',sans-serif;font-weight:800;font-size:clamp(25px,6vw,38px);line-height:1.08;margin:0 0 16px;color:var(--head);letter-spacing:-.02em}
.iz__about p{margin:0 0 15px;color:#4A4F57}
.iz__tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.iz__tag{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--head);background:var(--bg2);border:1px solid var(--line);padding:7px 12px}
/* steps */
.iz__steps{display:grid;gap:0}
.iz__step{display:grid;grid-template-columns:auto 1fr;gap:24px;padding:30px 0;border-top:1px solid var(--line)}
@media(max-width:620px){.iz__step{grid-template-columns:1fr;gap:10px}}
.iz__num{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:13px;color:var(--blue);letter-spacing:.05em;padding-top:7px;white-space:nowrap}
.iz__step h3{font-family:'Manrope',sans-serif;font-weight:700;font-size:clamp(20px,5vw,27px);margin:0 0 12px;color:var(--head);line-height:1.12;letter-spacing:-.01em}
.iz__step p{margin:0 0 12px;color:#4A4F57}
.iz__step ul{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:0}
.iz__step li{position:relative;padding:12px 0 12px 22px;border-top:1px solid var(--line);font-size:15.5px}
.iz__step li::before{content:"";position:absolute;left:0;top:19px;width:9px;height:3px;border-radius:2px;background:var(--therm)}
.iz__step b{color:var(--head)}
/* values with thermal index */
.iz__vals{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);margin-top:8px}
@media(min-width:760px){.iz__vals{grid-template-columns:repeat(3,1fr)}}
.iz__val{background:var(--bg);padding:26px 22px}
.iz__val .b{height:4px;width:46px;border-radius:2px;background:var(--therm);margin-bottom:14px}
.iz__val h4{font-family:'Manrope',sans-serif;font-weight:700;font-size:18px;color:var(--head);margin:0 0 8px}
.iz__val p{margin:0;font-size:14.5px;color:var(--dim)}
.iz .rv{opacity:0;transform:translateY(24px);transition:opacity .9s var(--ease),transform .9s var(--ease)}
.iz .rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.iz .rv{opacity:1;transform:none;transition:none}}
</style>
<div class="iz__wrap">
  <header class="iz__hero">
    <p class="iz__kick"><span class="sq"></span>Saint-Gobain · Видеопродакшн · 2024</p>
    <h1 class="iz__title rv">Бренд-ролик <em>«Изотек»</em></h1>
    <div class="iz__scale rv"></div>
    <div class="iz__scalab rv"><span>ХОЛОДНО</span><span>ТЕПЛОВАЯ ШКАЛА · ISOTEC</span><span>ГОРЯЧО</span></div>
    <p class="iz__lead rv">Имиджевый фильм для одного из продуктовых брендов Saint-Gobain в России — компании «Изотек», производителя технической изоляции под маркой ISOTEC.</p>
    <dl class="iz__spec rv">
      <div><dt>Клиент</dt><dd>ISOTEC / Изотек</dd></div>
      <div><dt>Группа</dt><dd>Saint-Gobain</dd></div>
      <div><dt>Формат</dt><dd>Имиджевый ролик</dd></div>
      <div><dt>Контур</dt><dd>Имидж + корпоратив</dd></div>
    </dl>
    <div class="iz__stage rv">
      <video id="izfilm" playsinline preload="none" controls poster="/portfolio/isotec/poster.jpg"><source src="/portfolio/isotec/brand-video.mp4" type="video/mp4"></video>
      <button class="iz__pb" id="izpb" style="background-image:url('/portfolio/isotec/poster.jpg')" aria-label="Смотреть ролик"><span class="iz__play"><i></i></span></button>
    </div>
    <div class="iz__cap rv"><span><b>Архив + съёмка</b></span><span><b>Производство</b></span><span><b>Команда</b></span><span><b>Постпродакшн</b></span></div>
  </header>
</div>

<div class="iz__wrap">
  <section class="iz__sec iz__about rv">
    <div>
      <p class="iz__label">О компании</p>
      <h2>«Изотек» — экспертный бренд изоляции в экосистеме Saint-Gobain</h2>
      <div class="iz__tags"><span class="iz__tag">МИНВАТА</span><span class="iz__tag">ТЕПЛО- И ОГНЕЗАЩИТА</span><span class="iz__tag">ЭНЕРГЕТИКА · ЖКХ</span></div>
    </div>
    <div>
      <p>Российский производитель технической изоляции на основе минеральной ваты под торговой маркой ISOTEC. Продукция применяется для тепло- и огнезащиты промышленного оборудования, трубопроводов, систем отопления и вентиляции, инженерных коммуникаций на объектах строительства, энергетики и ЖКХ.</p>
      <p>«Изотек» — часть международной группы Saint-Gobain, одного из мировых лидеров в производстве строительных материалов (более 200 заводов в 62 странах). Внутри экосистемы группы ISOTEC занимает позицию экспертного бренда в сегменте технической изоляции.</p>
    </div>
  </section>

  <section class="iz__sec rv">
    <p class="iz__label">Как мы это сделали</p>
    <div class="iz__steps">
      <div class="iz__step"><div class="iz__num">01 / ЗАДАЧА</div><div>
        <h3>Показать живой бренд, а не поставщика материалов</h3>
        <p>Зафиксировать путь становления компании: рост компетенций, расширение линейки, укрепление позиций, формирование команды экспертов. Ролик должен работать в двух контурах:</p>
        <ul><li><b>Имиджевый</b> — для клиентов, партнёров, отраслевых мероприятий, сайта и презентаций.</li><li><b>Корпоративный</b> — для внутренних коммуникаций, адаптации сотрудников и идентичности бренда внутри команды.</li></ul>
      </div></div>
      <div class="iz__step"><div class="iz__num">02 / РЕШЕНИЕ</div><div>
        <h3>Короткая визуальная история развития</h3>
        <p>Соединили архивные и актуальные материалы, производственные съёмки, командные моменты и ключевые достижения — так, чтобы за несколько минут зритель увидел, как менялись масштаб, технологии и подход к клиенту.</p>
        <p>Сценарная конструкция — путь: от первого запуска производства к зрелому бренду с узнаваемым именем. Съёмки шли на действующих площадках с соблюдением регламентов СИЗ и техники безопасности — стандартов всех заводов Saint-Gobain в России.</p>
      </div></div>
      <div class="iz__step"><div class="iz__num">03 / РЕЗУЛЬТАТ</div><div>
        <h3>Универсальный имиджевый инструмент</h3>
        <p>Ролик используют на сайте, в отраслевых презентациях, на партнёрских встречах и во внутренних коммуникациях. Для «Изотек» видео зафиксировало рубеж развития и стало эмоциональной точкой опоры для команды.</p>
      </div></div>
    </div>
  </section>

  <section class="iz__sec rv">
    <p class="iz__label">Три опоры визуального стиля</p>
    <div class="iz__vals">
      <div class="iz__val"><div class="b"></div><h4>Надёжность</h4><p>Промышленная фактура, реальные площадки, инженерная точность кадра.</p></div>
      <div class="iz__val"><div class="b"></div><h4>Технологичность</h4><p>Динамика производства, масштаб и современность процессов компании.</p></div>
      <div class="iz__val"><div class="b"></div><h4>Человеческое лицо</h4><p>Команда и экспертиза — бренд, за которым стоят люди, а не только материал.</p></div>
    </div>
  </section>
</div>
<script>(function(){var v=document.getElementById('izfilm'),p=document.getElementById('izpb');
if(v&&p){p.addEventListener('click',function(){p.style.opacity='0';p.style.pointerEvents='none';v.play();});
v.addEventListener('pause',function(){if(v.currentTime===0){p.style.opacity='1';p.style.pointerEvents='';}});}
if(matchMedia('(prefers-reduced-motion:reduce)').matches){document.querySelectorAll('.iz .rv').forEach(function(e){e.classList.add('in')});return;}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.14});
document.querySelectorAll('.iz .rv').forEach(function(e){io.observe(e)});})();</script>
</section></div>
'''

f = 'mirror/isotec/index.html'
s = open(f, encoding='utf-8', errors='ignore').read()
# текущий контент-блок — мой прошлый rec2206289241 (light brand). Заменяем его.
start = s.index('<div id="rec2206289241"')
end = start + 10 + re.search(r'<div id="rec\d+"', s[start + 10:]).start()
# поправим id новой секции на исходный, чтобы порядок/якоря не ломались
section = SECTION.replace('rec137505836_iso', 'rec2206289241')
s2 = s[:start] + section + s[end:]
s2 = s2.replace("window.mainTracker='tilda'", "window.mainTracker='custom'")
open(f, 'w').write(s2)
print('ISOTEC showcase вставлен, размер', len(s2))
