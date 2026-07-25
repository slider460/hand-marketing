#!/usr/bin/env python3
"""Генерит mirror/portfolio/obo-academy/index.html — кейс «Серия продуктовых
роликов для OBO Bettermann» (съёмка в Академии OBO, ведущий — Сергей Шаталов,
ведущий специалист по техническому обучению ОБО Беттерманн).

Дизайн-концепция: «инженерный каталог, оживший видео». Айдентика OBO из брендбука:
оранжевый-дренч #f39b00 (как обложка брендбука), графит #282a31, холодные серо-
голубые из вторичной палитры (НЕ тёплый крем). Типографика self-host: Geologica
(дисплей, инженерный гротеск), Onest (текст), JetBrains Mono (тех-метаданные: №,
тайм-коды, категории). Ролики — как пронумерованный каталог из 3 глав (I/II/III),
каждая — фичер + ряд, БЕЗ единой карточной сетки. Мотив «Building Connections» —
прочерченная линия-трасса (SVG, анимация). Реальный логотип OBO (obo_logo.py).

Видео — самохостинг /media/obo-*.mp4 (заливка ВРУЧНУЮ, вне CI, см. VIDEO-UPLOAD.md),
постеры /images/obo/poster-*.jpg. Правки — ТОЛЬКО через этот скрипт; build_v1
пропускает по маркеру <!--custom-page-->."""
import os, importlib.util, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/obo'
MEDIA = '/media'

# ─── данные роликов ──────────────────────────────────────────────────────────
FLAGSHIP = dict(slug='obo-point', title='ОБО Поинт', dur='5:06',
    cap='Обзорный фильм серии: Сергей Шаталов проводит по продуктовому миру OBO '
        'Bettermann прямо в шоу-руме Академии — три направления и логика '
        'ассортимента в одном ролике.')

# главы каталога: (римская, ключ-иконка, латиница, название, вводка, [ролики])
# ролик: (slug, title, dur, caption)
CHAPTERS = [
 ('I', 'factory', 'Industrieinstallation', 'Индустриальные инсталляции',
  'Несущие кабельные трассы и крепёж для промышленных объектов.', [
    ('obo-cable-ladder', 'Лестничные кабельные лотки', '2:04',
     'Несущая способность, сборка секций и трассировка тяжёлых кабельных потоков.'),
    ('obo-beam-clamps', 'Балочные зажимы', '2:17',
     'Крепление трасс к балкам и профильным рейкам без сверления.'),
    ('obo-mounting-rails', 'Монтажные рейки', '1:54',
     'Профильные рейки как основа сборных креплений: типоразмеры и узлы.'),
    ('obo-wire-tray', 'Проволочные лотки', '0:53',
     'Гибкая трассировка, вентилируемая прокладка и скоростной монтаж.'),
 ]),
 ('II', 'building', 'Gebäudeinstallation', 'Инсталляции зданий',
  'Коммутация и вывод линий в интерьере и полу.', [
    ('obo-junction-b', 'Распределительные коробки серии B', '2:02',
     'Степень защиты, ввод кабеля и аккуратная коммутация в зданиях.'),
    ('obo-junction-mx', 'Распределительные коробки MX', '1:48',
     'Коробки MX для ответственных линий и повышенных требований.'),
    ('obo-floor-box', 'Напольные лючки', '3:42',
     'Установка в стяжку и фальшпол, вывод силовых и слаботочных линий в пол.'),
 ]),
 ('III', 'shield', 'Schutzinstallation', 'Защита и безопасность',
  'Молниезащита и заземление по действующим нормам.', [
    ('obo-lightning', 'Внешняя молниезащита', '3:01',
     'Молниеприёмники, токоотводы и сборка системы по нормам.'),
    ('obo-earthing', 'Комплект заземления', '2:16',
     'Электроды, зажимы и последовательная сборка надёжного контура.'),
 ]),
]

ICONS = {
 'factory': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><path d="M3 21V10l6 4V10l6 4V6l3-2"/><path d="M18 21V8"/><path d="M3 21h18"/></svg>',
 'building': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><rect x="4" y="3" width="10" height="18"/><path d="M14 8h6v13h-6"/><path d="M7 7h1.5M10.5 7H12M7 10.5h1.5M10.5 10.5H12M7 14h1.5M10.5 14H12M17 12h.5M17 15.5h.5"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><path d="M12 3l7 3v5c0 4.4-3 8.4-7 10-4-1.6-7-5.6-7-10V6z"/><path d="M12 8v4M12 15v.4"/></svg>',
}
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'

PAGE_CSS = """<style id="obo-css">
:root{--o-orange:#f39b00;--o-orange-d:#d98a00;--o-ink:#282a31;--o-ink2:#1e2026;
 --o-blue:#41525d;--o-blue2:#6c8493;--o-mist:#d3dde1;--o-paper:#eceff1;--o-line:#c3ccd1;
 --f-disp:'Geologica','Onest',system-ui,Arial,sans-serif;
 --f-body:'Onest',system-ui,Arial,sans-serif;
 --f-mono:'JetBrains Mono',ui-monospace,monospace;
 --z-modal:1000}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.obo{font-family:var(--f-body);color:var(--o-ink);background:var(--o-paper);
 line-height:1.55;font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.obo *{box-sizing:border-box}
.obo img{max-width:100%;height:auto;display:block}
.obo-w{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,48px)}
.obo h1,.obo h2,.obo h3{font-family:var(--f-disp);font-weight:800;line-height:1.02;
 letter-spacing:-.02em;margin:0;text-wrap:balance}
.obo p{text-wrap:pretty}
.obo-mono{font-family:var(--f-mono);font-weight:500;letter-spacing:.02em;
 text-transform:uppercase;font-size:12.5px}
.obo a{color:inherit}

/* ── HERO (оранжевый дренч) ── */
.obo-hero{position:relative;background:var(--o-orange);color:var(--o-ink);overflow:hidden}
.obo-hero::before{content:"";position:absolute;inset:0;pointer-events:none;
 background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.08) 0 1.5px,transparent 1.5px 22px)}
.obo-hero__route{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1}
.obo-hero__route path{fill:none;stroke:rgba(40,42,49,.22);stroke-width:2;
 stroke-dasharray:2400;stroke-dashoffset:2400;animation:obo-draw 2.4s .2s cubic-bezier(.2,.7,.2,1) forwards}
.obo-hero__route circle{fill:var(--o-ink);opacity:0;animation:obo-dot .5s 2.2s forwards}
.obo-hero__in{position:relative;z-index:2;padding-top:clamp(22px,3vw,34px);padding-bottom:clamp(56px,7vw,96px)}
.obo-hero__top{display:flex;align-items:center;justify-content:space-between;gap:20px;
 padding-bottom:clamp(40px,8vw,110px);flex-wrap:wrap}
.obo .obo-hero__logo{height:clamp(46px,5.2vw,72px);width:auto;max-width:340px}
.obo-hero__slogan{font-family:var(--f-mono);font-weight:600;letter-spacing:.22em;
 font-size:12px;text-transform:uppercase;color:var(--o-ink);opacity:.75}
.obo-hero h1{font-size:clamp(40px,8.4vw,104px);max-width:14ch;font-weight:800;letter-spacing:-.035em}
.obo-hero__sub{font-size:clamp(17px,1.7vw,21px);max-width:56ch;margin:clamp(20px,3vw,30px) 0 0;
 color:#5a3d05;line-height:1.5;font-weight:450}
.obo-hero__spec{margin-top:clamp(26px,3.5vw,38px);display:flex;flex-wrap:wrap;gap:10px 26px;
 border-top:1.5px solid rgba(40,42,49,.28);padding-top:16px;color:var(--o-ink)}
.obo-hero__spec span{opacity:.85}
.obo-anim{opacity:0;transform:translateY(26px);animation:obo-rise .9s cubic-bezier(.2,.7,.2,1) forwards}

/* ── FEATURE-плеер (кинематографичный) ── */
.obo-feature{margin-top:clamp(-40px,-4vw,-64px);position:relative;z-index:3}
.obo-fplayer{position:relative;aspect-ratio:16/9;overflow:hidden;cursor:pointer;
 background:var(--o-ink);box-shadow:0 40px 90px -40px rgba(30,32,38,.7);
 outline:1px solid rgba(40,42,49,.12)}
.obo-fplayer img{width:100%;height:100%;object-fit:cover;transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.obo-fplayer:hover img{transform:scale(1.05)}
.obo-fplayer__scrim{position:absolute;inset:0;
 background:linear-gradient(180deg,rgba(30,32,38,.05) 0,rgba(30,32,38,.06) 50%,rgba(30,32,38,.82) 100%)}
.obo-fplayer__meta{position:absolute;top:0;left:0;right:0;display:flex;justify-content:space-between;
 align-items:flex-start;padding:clamp(16px,2.4vw,28px);color:#fff}
.obo-fplayer__tag{background:var(--o-orange);color:var(--o-ink);padding:7px 13px;font-weight:600}
.obo-fplayer__body{position:absolute;left:0;bottom:0;padding:clamp(18px,3vw,40px);color:#fff;
 max-width:640px}
.obo-fplayer__body h2{font-size:clamp(26px,3.6vw,46px);color:#fff}
.obo-fplayer__body p{margin:12px 0 0;color:rgba(255,255,255,.8);font-size:clamp(14px,1.4vw,17px)}
.obo-play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none}
.obo-play i{width:clamp(64px,7vw,92px);height:clamp(64px,7vw,92px);border-radius:50%;
 background:var(--o-orange);color:var(--o-ink);display:flex;align-items:center;justify-content:center;
 box-shadow:0 12px 34px rgba(0,0,0,.4);transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.obo-play i svg{width:42%;height:42%;margin-left:6%}
.obo-fplayer:hover .obo-play i,.obo-vid:hover .obo-play i{transform:scale(1.12)}

/* ── INTRO (графит) ── */
.obo-intro{background:var(--o-ink);color:#fff;padding:clamp(72px,10vw,140px) 0}
.obo-intro__grid{display:grid;grid-template-columns:1.15fr 1fr;gap:clamp(36px,6vw,90px);align-items:end}
.obo-intro h2{font-size:clamp(28px,4.4vw,58px);color:#fff;letter-spacing:-.03em}
.obo-intro h2 em{font-style:normal;color:var(--o-orange)}
.obo-intro__lede{font-size:clamp(16px,1.5vw,19px);color:#c7d0d6;line-height:1.65}
.obo-intro__lede p{margin:0 0 16px}
.obo-intro__lede b{color:#fff;font-weight:600}
.obo-credit{margin-top:34px;display:flex;align-items:center;gap:16px;
 border-top:1px solid rgba(255,255,255,.15);padding-top:22px}
.obo-credit__ava{width:52px;height:52px;flex:none;border-radius:50%;background:var(--o-orange);
 color:var(--o-ink);display:flex;align-items:center;justify-content:center;font-family:var(--f-disp);
 font-weight:800;font-size:20px}
.obo-credit b{display:block;font-weight:600;font-size:16px}
.obo-credit span{color:var(--o-blue2);font-size:13.5px}

/* ── CATALOG (главы) ── */
.obo-cat{padding:clamp(60px,8vw,110px) 0 clamp(30px,5vw,60px)}
.obo-chap{padding:clamp(46px,6vw,80px) 0;border-top:1.5px solid var(--o-line)}
.obo-chap:first-child{border-top:0;padding-top:clamp(20px,3vw,40px)}
.obo-chaphd{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:clamp(18px,3vw,34px);
 margin-bottom:clamp(30px,4vw,48px)}
.obo-chaphd__num{font-family:var(--f-disp);font-weight:800;font-size:clamp(56px,10vw,130px);
 line-height:.8;color:var(--o-orange);letter-spacing:-.04em}
.obo-chaphd__t h2{font-size:clamp(24px,3.2vw,40px)}
.obo-chaphd__t .obo-mono{color:var(--o-blue2);margin-bottom:8px;display:block}
.obo-chaphd__t p{margin:8px 0 0;color:var(--o-blue);max-width:46ch;font-size:15.5px}
.obo-chaphd__ico{width:clamp(48px,6vw,74px);height:clamp(48px,6vw,74px);color:var(--o-ink);
 opacity:.9;justify-self:end}
.obo-chaphd__ico svg{width:100%;height:100%}

.obo-lead{position:relative;overflow:hidden;cursor:pointer;aspect-ratio:16/9;background:var(--o-ink);
 outline:1px solid var(--o-line);margin-bottom:22px}
.obo-lead img{width:100%;height:100%;object-fit:cover;transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.obo-lead:hover img{transform:scale(1.04)}
.obo-lead__scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,32,38,0) 45%,rgba(30,32,38,.8))}
.obo-lead__b{position:absolute;left:0;bottom:0;right:0;padding:clamp(16px,2.4vw,30px);color:#fff;
 display:flex;justify-content:space-between;align-items:flex-end;gap:16px}
.obo-lead__b h3{color:#fff;font-size:clamp(20px,2.4vw,30px)}
.obo-lead__b p{margin:8px 0 0;color:rgba(255,255,255,.78);font-size:14.5px;max-width:52ch}

.obo-row{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2vw,26px)}
.obo-row.n2{grid-template-columns:repeat(2,1fr)}
.obo-vid{cursor:pointer}
.obo-vthumb{position:relative;aspect-ratio:16/9;overflow:hidden;background:var(--o-ink);
 outline:1px solid var(--o-line);outline-offset:0;transition:outline-color .25s,outline-width .25s}
.obo-vthumb img{width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.obo-vid:hover .obo-vthumb{outline:2px solid var(--o-orange)}
.obo-vid:hover .obo-vthumb img{transform:scale(1.05)}
.obo-dur{position:absolute;right:10px;bottom:10px;background:rgba(30,32,38,.9);color:#fff;
 font-family:var(--f-mono);font-size:12px;font-weight:500;padding:4px 9px}
.obo-vmeta{display:flex;align-items:baseline;gap:10px;margin:14px 0 0}
.obo-vmeta .num{font-family:var(--f-mono);font-size:13px;color:var(--o-orange-d);font-weight:600}
.obo-vid h4{font-family:var(--f-disp);font-weight:700;font-size:18px;letter-spacing:-.01em;margin:0}
.obo-vid p{font-size:14px;color:var(--o-blue);margin:7px 0 0;line-height:1.45}

/* ── PROCESS (линия-трасса) ── */
.obo-proc{background:var(--o-ink);color:#fff;padding:clamp(72px,10vw,130px) 0;position:relative;overflow:hidden}
.obo-proc__hd{max-width:640px;margin-bottom:clamp(44px,6vw,72px)}
.obo-proc__hd .obo-mono{color:var(--o-orange);display:block;margin-bottom:14px}
.obo-proc__hd h2{font-size:clamp(28px,4.4vw,56px);color:#fff}
.obo-proc__hd p{color:#c7d0d6;margin:16px 0 0;font-size:clamp(16px,1.5vw,19px)}
.obo-line{position:relative}
.obo-line__rail{position:absolute;left:0;right:0;top:19px;height:2px;background:rgba(255,255,255,.16)}
.obo-line__fill{position:absolute;left:0;top:19px;height:2px;background:var(--o-orange);width:0}
.obo-line.is-in .obo-line__fill{width:100%;transition:width 1.6s .1s cubic-bezier(.3,.6,.2,1)}
.obo-steps{display:grid;grid-template-columns:repeat(6,1fr);gap:24px}
.obo-step{position:relative;padding-top:44px}
.obo-step__dot{position:absolute;top:11px;left:0;width:18px;height:18px;border-radius:50%;
 background:var(--o-ink);border:2px solid rgba(255,255,255,.4);transition:border-color .3s,background .3s}
.obo-line.is-in .obo-step__dot{border-color:var(--o-orange);background:var(--o-orange)}
.obo-step em{font-family:var(--f-mono);font-style:normal;font-size:12px;color:var(--o-blue2);font-weight:600}
.obo-step b{display:block;font-family:var(--f-disp);font-weight:700;font-size:17px;margin:8px 0 6px}
.obo-step span{color:var(--o-blue2);font-size:13.5px;line-height:1.45}

/* ── OUTRO (оранжевый дренч, буквенный бэкенд) ── */
.obo-outro{background:var(--o-orange);color:var(--o-ink);position:relative;overflow:hidden;
 padding:clamp(70px,9vw,120px) 0}
.obo-outro::before{content:"";position:absolute;inset:0;pointer-events:none;
 background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.09) 0 1.5px,transparent 1.5px 22px)}
.obo-outro__in{position:relative;z-index:2;display:grid;grid-template-columns:1.3fr auto;
 gap:36px;align-items:center}
.obo-outro h2{font-size:clamp(30px,4.6vw,60px);max-width:16ch;letter-spacing:-.03em}
.obo-outro p{margin:16px 0 0;font-size:clamp(16px,1.6vw,19px);color:#5a3d05;max-width:46ch}
.obo-outro__more{margin-top:20px;font-family:var(--f-mono);font-size:12.5px;text-transform:uppercase}
.obo-outro__more a{font-weight:600;text-decoration:underline;text-underline-offset:3px}
.obo .obo-btn{display:inline-flex;align-items:center;gap:12px;background:var(--o-ink);color:#fff;
 font-family:var(--f-disp);font-weight:700;font-size:clamp(16px,1.6vw,19px);
 padding:20px 36px;text-decoration:none;transition:transform .25s cubic-bezier(.2,.7,.2,1),background .2s;
 white-space:nowrap}
.obo-btn:hover{transform:translateY(-3px);background:#000}
.obo-btn svg{width:20px;height:20px}

/* ── О КОМПАНИИ (спецификация) ── */
.obo-about{padding:clamp(56px,7vw,96px) 0}
.obo-about__card{border:1.5px solid var(--o-line);background:#fff;display:grid;
 grid-template-columns:.82fr 1.18fr;box-shadow:0 30px 60px -50px rgba(30,32,38,.5)}
.obo-about__brand{padding:clamp(26px,3.4vw,44px);border-right:1.5px solid var(--o-line);
 display:flex;flex-direction:column;gap:22px}
.obo-about .obo-about__logo{width:min(230px,72%);height:auto}
.obo-about__slogan{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.18em;
 text-transform:uppercase;color:var(--o-blue2)}
.obo-about__cats{margin-top:auto;display:flex;gap:16px;padding-top:12px}
.obo-about__cats i{width:34px;height:34px;color:var(--o-orange);flex:none}
.obo-about__cats i svg{width:100%;height:100%}
.obo-about__body{padding:clamp(26px,3.4vw,44px)}
.obo-about__body>.obo-mono{color:var(--o-blue2)}
.obo-about__body h2{font-size:clamp(28px,3.4vw,44px);margin:10px 0 0}
.obo-about__body>p{color:var(--o-blue);margin:18px 0 0;max-width:62ch;font-size:15.5px;line-height:1.6}
.obo-spec{margin:26px 0 0;border-top:1px solid var(--o-line)}
.obo-spec>div{display:grid;grid-template-columns:190px 1fr;gap:20px;padding:12px 0;
 border-bottom:1px solid var(--o-line)}
.obo-spec dt{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;
 color:var(--o-blue2);margin:0;padding-top:2px}
.obo-spec dd{margin:0;font-weight:500;font-size:15.5px}

/* ── modal ── */
.obo-modal{position:fixed;inset:0;z-index:var(--z-modal);background:rgba(20,21,25,.94);
 display:none;align-items:center;justify-content:center;padding:clamp(12px,3vw,28px)}
.obo-modal.is-open{display:flex}
.obo-modal__box{width:min(1180px,100%);aspect-ratio:16/9;background:#000;overflow:hidden;
 box-shadow:0 40px 100px rgba(0,0,0,.6)}
.obo-modal__box video{width:100%;height:100%;display:block;background:#000}
.obo-modal__x{position:absolute;top:18px;right:22px;width:48px;height:48px;background:var(--o-orange);
 border:0;color:var(--o-ink);font-size:26px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.obo-modal__cap{position:absolute;left:0;right:0;bottom:18px;text-align:center;color:#c7d0d6;
 font-family:var(--f-mono);font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;padding:0 20px}

/* ── reveal (усиление уже видимого) ── */
.obo-r{opacity:0;transform:translateY(24px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.obo-r.is-in{opacity:1;transform:none}
html.no-js .obo-r{opacity:1;transform:none}

@keyframes obo-rise{to{opacity:1;transform:none}}
@keyframes obo-draw{to{stroke-dashoffset:0}}
@keyframes obo-dot{to{opacity:1}}

@media(max-width:920px){
 .obo-intro__grid{grid-template-columns:1fr;gap:34px;align-items:start}
 .obo-row{grid-template-columns:repeat(2,1fr)}
 .obo-steps{grid-template-columns:repeat(3,1fr);gap:30px 20px}
 .obo-line__rail,.obo-line__fill{display:none}
 .obo-step{padding-top:0;padding-left:30px}
 .obo-step__dot{top:4px;left:0}
 .obo-outro__in{grid-template-columns:1fr;align-items:start}
 .obo-about__card{grid-template-columns:1fr}
 .obo-about__brand{border-right:0;border-bottom:1.5px solid var(--o-line);flex-direction:row;
  align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}
 .obo-about__cats{margin:0;padding:0}
}
@media(max-width:600px){
 .obo{font-size:16px}
 .obo-feature{margin-top:-28px}
 .obo-chaphd{grid-template-columns:auto 1fr;gap:16px}
 .obo-chaphd__ico{display:none}
 .obo-row,.obo-row.n2{grid-template-columns:1fr}
 .obo-steps{grid-template-columns:1fr;gap:22px}
 .obo-fplayer__body p,.obo-lead__b p{display:none}
 .obo-lead__b{flex-direction:column;align-items:flex-start}
 .obo-spec>div{grid-template-columns:1fr;gap:3px}
 .obo-spec dt{padding-top:0}
}
@media(prefers-reduced-motion:reduce){
 .obo-anim,.obo-hero__route path,.obo-hero__route circle{animation:none!important;opacity:1!important;
  stroke-dashoffset:0!important;transform:none!important}
 .obo-r{opacity:1!important;transform:none!important}
 .obo *{transition-duration:.01ms!important}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Серия продуктовых роликов для OBO Bettermann — съёмка в Академии | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: серия из 10 продуктовых видеороликов для OBO Bettermann. Съёмка в Академии OBO, ведущий — Сергей Шаталов. Три направления: индустриальные инсталляции, инсталляции зданий, защита. Сценарий, студийная съёмка, макросъёмка, 3D-инфографика, монтаж.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hand-marketing.ru/portfolio/obo-academy/">
<meta property="og:type" content="article"><meta property="og:title" content="Серия продуктовых роликов для OBO Bettermann — кейс Hand Marketing">
<meta property="og:description" content="10 видеороликов о продукции OBO Bettermann, снятых в Академии OBO с ведущим специалистом Сергеем Шаталовым.">
<meta property="og:url" content="https://hand-marketing.ru/portfolio/obo-academy/">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/poster-obo-point.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/geologica-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def feature_player(slug, title, dur, tag, cap):
    return (f'<div class="obo-fplayer obo-play-trigger" role="button" tabindex="0" '
            f'data-src="{MEDIA}/{slug}.mp4" data-title="{H.escape(title)}" '
            f'aria-label="Смотреть: {H.escape(title)}">'
            f'<img src="{IMG}/poster-{slug}.jpg" alt="{H.escape(title)}" loading="lazy">'
            f'<div class="obo-fplayer__scrim"></div>'
            f'<div class="obo-fplayer__meta"><span class="obo-fplayer__tag obo-mono">{tag}</span>'
            f'<span class="obo-mono">{dur}</span></div>'
            f'<div class="obo-play"><i>{PLAY}</i></div>'
            f'<div class="obo-fplayer__body"><h2>{H.escape(title)}</h2><p>{H.escape(cap)}</p></div>'
            f'</div>')


def hero():
    return (
      '<header class="obo-hero"><svg class="obo-hero__route" viewBox="0 0 1440 760" '
      'preserveAspectRatio="xMaxYMid slice" aria-hidden="true">'
      '<path d="M-40 150 H720 a40 40 0 0 1 40 40 V470 a40 40 0 0 0 40 40 H1480"/>'
      '<path d="M1480 300 H1120 a40 40 0 0 0-40 40 V600 a40 40 0 0 1-40 40 H-40"/>'
      '<circle cx="760" cy="510" r="7"/><circle cx="1080" cy="340" r="7"/></svg>'
      '<div class="obo-w obo-hero__in">'
      '<div class="obo-hero__top">'
      f'<img class="obo-hero__logo" src="{IMG}/logo-white.png" alt="OBO Bettermann">'
      '<span class="obo-hero__slogan">Building Connections</span></div>'
      '<p class="obo-mono obo-anim" style="animation-delay:.05s;color:#5a3d05">'
      'Видеопродакшн · Академия OBO Bettermann</p>'
      '<h1 class="obo-anim" style="animation-delay:.12s">Продуктовая линейка&nbsp;OBO — по деталям</h1>'
      '<p class="obo-hero__sub obo-anim" style="animation-delay:.22s">Серия из десяти роликов, '
      'снятых в шоу-руме Академии OBO. Ведущий специалист по техническому обучению '
      'Сергей Шаталов разбирает каждый продукт — назначение, устройство и монтаж по шагам. '
      'Это короткие мастер-классы, а не рекламные споты.</p>'
      '<div class="obo-hero__spec obo-mono obo-anim" style="animation-delay:.32s">'
      '<span>10 роликов</span><span>3 направления</span><span>Съёмка в Академии OBO</span>'
      '<span>Ведущий: С. Шаталов</span></div>'
      '</div></header>')


def feature():
    f = FLAGSHIP
    return ('<div class="obo-w"><div class="obo-feature obo-anim" style="animation-delay:.4s">'
            + feature_player(f['slug'], f['title'], f['dur'], 'Обзорный ролик', f['cap'])
            + '</div></div>')


def company():
    specs = [('Основана', '1911'), ('Штаб-квартира', 'Менден, Германия'),
             ('Форма', 'семейное предприятие'),
             ('Направления', 'Индустрия · Здания · Защита'),
             ('Слоган', 'Building Connections')]
    rows = ''.join(f'<div><dt class="obo-mono">{H.escape(k)}</dt><dd>{H.escape(v)}</dd></div>'
                   for k, v in specs)
    cats = ''.join(f'<i>{ICONS[k]}</i>' for k in ('factory', 'building', 'shield'))
    return (
      '<section class="obo-about"><div class="obo-w">'
      '<div class="obo-about__card obo-r">'
      f'<div class="obo-about__brand"><img class="obo-about__logo" src="{IMG}/logo-ink.png" '
      'alt="OBO Bettermann"><span class="obo-about__slogan">Building Connections</span>'
      f'<div class="obo-about__cats">{cats}</div></div>'
      '<div class="obo-about__body"><span class="obo-mono">Клиент проекта</span>'
      '<h2>OBO Bettermann</h2>'
      '<p>Немецкий производитель систем для монтажа электротехники. Компания основана '
      'в 1911 году в Мендене и уже более века остаётся семейным предприятием. В портфеле — '
      'кабеленесущие системы, крепёж и соединение, распределительные коробки, напольные '
      'и настенные системы, заземление и молниезащита. Весь ассортимент разложен по трём '
      'направлениям — они же задают структуру этой серии роликов.</p>'
      f'<dl class="obo-spec">{rows}</dl></div>'
      '</div></div></section>')


def intro():
    return (
      '<section class="obo-intro"><div class="obo-w obo-intro__grid">'
      '<div class="obo-r"><h2>Продукцию сняли там, где ей учат — '
      'в&nbsp;<em>Академии&nbsp;OBO</em></h2></div>'
      '<div class="obo-intro__lede obo-r">'
      '<p>У OBO Bettermann есть собственная <b>Академия</b> — учебный центр '
      'с шоу-румом реальных решений и смонтированных систем. Мы сняли серию '
      'прямо в этом пространстве.</p>'
      '<p>Для каждой позиции — свой сценарий, '
      'предметная макросъёмка деталей и 3D-инфографика с выносками. Всё в фирменном '
      'стиле OBO: <b>оранжевый и графит</b>, единые заставки и титры.</p>'
      '<div class="obo-credit"><span class="obo-credit__ava">СШ</span>'
      '<span><b>Сергей Шаталов</b><span>ведущий специалист по техническому обучению '
      'ОБО Беттерманн</span></span></div>'
      '</div></div></section>')


def catalog():
    chaps = ''
    n = 0
    for roman, icon, latin, name, blurb, vids in CHAPTERS:
        lead = vids[0]
        rest = vids[1:]
        n += 1
        lead_num = f'{n:02d}.1'
        lead_html = (
          f'<div class="obo-lead obo-play-trigger obo-r" role="button" tabindex="0" '
          f'data-src="{MEDIA}/{lead[0]}.mp4" data-title="{H.escape(lead[1])}" '
          f'aria-label="Смотреть: {H.escape(lead[1])}">'
          f'<img src="{IMG}/poster-{lead[0]}.jpg" alt="{H.escape(lead[1])}" loading="lazy">'
          f'<div class="obo-lead__scrim"></div>'
          f'<div class="obo-play"><i>{PLAY}</i></div>'
          f'<span class="obo-dur">{lead[2]}</span>'
          f'<div class="obo-lead__b"><div><h3>{H.escape(lead[1])}</h3>'
          f'<p>{H.escape(lead[3])}</p></div></div></div>')
        cards = ''
        for i, (slug, title, dur, cap) in enumerate(rest, start=2):
            cards += (
              f'<div class="obo-vid obo-play-trigger obo-r" role="button" tabindex="0" '
              f'data-src="{MEDIA}/{slug}.mp4" data-title="{H.escape(title)}" '
              f'aria-label="Смотреть: {H.escape(title)}">'
              f'<div class="obo-vthumb"><img src="{IMG}/poster-{slug}.jpg" alt="{H.escape(title)}" loading="lazy">'
              f'<div class="obo-play"><i>{PLAY}</i></div><span class="obo-dur">{dur}</span></div>'
              f'<div class="obo-vmeta"><span class="num">{n:02d}.{i}</span>'
              f'<h4>{H.escape(title)}</h4></div><p>{H.escape(cap)}</p></div>')
        rowcls = 'obo-row n2' if len(rest) == 2 else 'obo-row'
        chaps += (
          f'<div class="obo-chap"><div class="obo-chaphd obo-r">'
          f'<span class="obo-chaphd__num">{roman}</span>'
          f'<div class="obo-chaphd__t"><span class="obo-mono">{H.escape(latin)} · {len(vids)} ролика</span>'
          f'<h2>{H.escape(name)}</h2><p>{H.escape(blurb)}</p></div>'
          f'<span class="obo-chaphd__ico">{ICONS[icon]}</span></div>'
          f'{lead_html}<div class="{rowcls}">{cards}</div></div>')
    return f'<section class="obo-cat"><div class="obo-w">{chaps}</div></section>'


def process():
    steps = [
        ('01', 'Сценарий', 'Назначение, ключевые узлы и порядок монтажа для каждого продукта.'),
        ('02', 'Съёмка в Академии', 'Студийный свет и несколько камер в шоу-руме OBO.'),
        ('03', 'Макросъёмка', 'Крупные планы резьбы, защёлок и соединений.'),
        ('04', '3D-инфографика', 'Выноски, обозначения и 3D-аннотации поверх кадра.'),
        ('05', 'Монтаж', 'Сборка, титры и фирменная графика на всю серию.'),
        ('06', '10 роликов', 'Готовый пакет для сайта, соцсетей, обучения и выставок.'),
    ]
    cells = ''.join(f'<div class="obo-step"><span class="obo-step__dot"></span>'
                    f'<em>{n}</em><b>{H.escape(t)}</b><span>{H.escape(d)}</span></div>'
                    for n, t, d in steps)
    return ('<section class="obo-proc"><div class="obo-w">'
            '<div class="obo-proc__hd obo-r"><span class="obo-mono">Производство</span>'
            '<h2>Полный цикл — от сценария до пэкшота</h2>'
            '<p>Мы отвечали за всё, кроме экспертизы: её принёс сам OBO.</p></div>'
            f'<div class="obo-line" data-line><div class="obo-line__rail"></div>'
            f'<div class="obo-line__fill"></div><div class="obo-steps">{cells}</div></div>'
            '</div></section>')


def outro():
    arrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
    return ('<section class="obo-outro"><div class="obo-w obo-outro__in">'
            '<div class="obo-r"><h2>Снимем серию роликов о вашей продукции</h2>'
            '<p>Экспертный обзор, предметная съёмка и инфографика в вашем фирменном стиле — под ключ.</p>'
            '<div class="obo-outro__more">Ещё о видеопродакшне — '
            '<a href="/videoproduction">услуга Video Production</a></div></div>'
            f'<a class="obo-btn obo-r" href="#lead">Обсудить проект {arrow}</a>'
            '</div></section>')


MODAL = ('<div class="obo-modal" id="obo-modal" aria-hidden="true">'
         '<button class="obo-modal__x" id="obo-modal-x" aria-label="Закрыть">×</button>'
         '<div class="obo-modal__box"><video id="obo-modal-video" controls playsinline preload="none"></video></div>'
         '<div class="obo-modal__cap" id="obo-modal-cap"></div></div>')

PAGE_JS = """<script>(function(){
 var modal=document.getElementById('obo-modal'),vid=document.getElementById('obo-modal-video'),
     cap=document.getElementById('obo-modal-cap'),x=document.getElementById('obo-modal-x');
 function open(src,title){vid.src=src;cap.textContent=title||'';modal.classList.add('is-open');
  modal.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';
  var p=vid.play();if(p&&p.catch)p.catch(function(){});}
 function close(){modal.classList.remove('is-open');modal.setAttribute('aria-hidden','true');
  vid.pause();vid.removeAttribute('src');vid.load();cap.textContent='';document.body.style.overflow='';}
 [].forEach.call(document.querySelectorAll('.obo-play-trigger'),function(t){
  function go(){open(t.getAttribute('data-src'),t.getAttribute('data-title'));}
  t.addEventListener('click',go);
  t.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});
 });
 x.addEventListener('click',close);
 modal.addEventListener('click',function(e){if(e.target===modal)close();});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&modal.classList.contains('is-open'))close();});
 // reveal + линия-трасса
 var els=[].slice.call(document.querySelectorAll('.obo-r,[data-line]'));
 function show(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(show);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
  show(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)show(n);else io.observe(n);});
})();</script>"""

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
 '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
 '{"@type":"ListItem","position":2,"name":"Серия продуктовых роликов для OBO Bettermann",'
 '"item":"https://hand-marketing.ru/portfolio/obo-academy/"}]}</script>')


def build():
    body = (f'{rc.header()}<main class="obo">{hero()}{feature()}{company()}{intro()}{catalog()}'
            f'{process()}</main>{MODAL}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'portfolio', 'obo-academy')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
