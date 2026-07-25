#!/usr/bin/env python3
"""Генерит mirror/portfolio/ceramicanova/index.html — кейс «Имиджевые ролики для
CeramicaNova»: серия из 17 роликов по коллекциям санфарфора (по одному на SKU).

Дизайн-концепция: «витрина имиджевых фильмов премиального фарфора». Айдентика
CeramicaNova — минималистичная люксовая: чистый галерейный белый (сам фарфор),
графитовый «кинозал» для героя и галереи, фирменное сердце (малиново-красный),
подкрашенная бирюзовая вода как холодный мотив, слоган «Extraordinary every day».
Типографика self-host: Manrope (дисплей) + Onest (текст) из /fonts/manrope-onest.css.

Съёмка: в шоуруме бренда построили инсталляцию, художник оформил сцену, сделали
систему замкнутого слива и подкрасили воду — чтобы безободковый смыв читался в кадре.
Бекстейдж — реальные фото/кадры со съёмки (НЕ видео).

Ролики — самохостинг /media/ceramicanova-cnNN.mp4 (заливка ВРУЧНУЮ, вне CI),
постеры /images/ceramicanova/poster-cnNN.jpg, бекстейдж backstage-*.jpg.
Правки — ТОЛЬКО через этот скрипт; build_v1 пропускает по маркеру <!--custom-page-->."""
import os, importlib.util, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/ceramicanova'
MEDIA = '/media'

# ─── данные роликов: (NN, slug, коллекция, вариант, длительность в сек) ───────
FILMS = [
    ('01', 'cn01', 'Play',       '',      58),
    ('02', 'cn02', 'Moments',    '',      55),
    ('03', 'cn03', 'Metric',     '',      49),
    ('04', 'cn04', 'Forma',      '',      52),
    ('05', 'cn05', 'Metropol',   '',      54),
    ('06', 'cn06', 'New Day',    '',      54),
    ('07', 'cn07', 'Forma',      '',      49),
    ('08', 'cn08', 'Noel',       '',      58),
    ('09', 'cn09', 'Long',       '',      51),
    ('10', 'cn10', 'Highlight',  '',      46),
    ('11', 'cn11', 'Mia',        '',      50),
    ('12', 'cn12', 'Cubic',      '',      54),
    ('13', 'cn13', 'Mono',       '',      56),
    ('14', 'cn14', 'Balearica',  '',      60),
    ('15', 'cn15', 'Play',       'Black', 53),
    ('16', 'cn16', 'Metric',     'Black', 59),
    ('17', 'cn17', 'Metropol',   'Black', 50),
]
FLAGSHIP = 'cn02'   # маркиз-ролик в герое (бирюзовый каскад воды, «Moments»)

def mmss(s): return f'{s//60}:{s%60:02d}'

HEART = ('<svg class="cn-heart" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.7'
         'C6.7 16.9 3 13.6 3 9.6 3 7 5 5.1 7.4 5.1c1.6 0 2.9.8 3.6 2 .3.5 1.7.5 2 0 .7-1.2 '
         '2-2 3.6-2C21 5.1 21 7 21 9.6c0 4-3.7 7.3-9 11.1z"/></svg>')
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>'
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

def MARK(cls=''):
    return (f'<span class="cn-mark {cls}">ceramica<b>nova</b>{HEART}</span>')

PAGE_CSS = """<style id="cn-css">
:root{
 --cn-white:#ffffff;--cn-paper:#f3f5f6;--cn-ink:#0d0e11;--cn-ink2:#5b626b;
 --cn-cin:#101216;--cn-cin2:#171a1f;--cn-red:#e1103f;--cn-red-d:#b60d33;
 --cn-aqua:#37b6d3;--cn-line:#e6e8ea;--cn-line-d:#2a2e35;
 --cn-df:'Manrope',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --cn-bf:'Onest',system-ui,-apple-system,Segoe UI,Arial,sans-serif;
 --z-modal:1000}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.cn{font-family:var(--cn-bf);color:var(--cn-ink);background:var(--cn-white);
 line-height:1.6;font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.cn *{box-sizing:border-box}
.cn img{max-width:100%;height:auto;display:block}
.cn-w{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,52px)}
.cn h1,.cn h2,.cn h3,.cn h4{font-family:var(--cn-df);font-weight:800;line-height:1.04;
 letter-spacing:-.03em;margin:0;text-wrap:balance}
.cn p{text-wrap:pretty}
.cn a{color:inherit;text-decoration:none}
.cn-kick{font-family:var(--cn-df);font-weight:600;font-size:12.5px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--cn-red)}
.cn-mark{font-family:var(--cn-df);font-weight:500;letter-spacing:-.01em;
 display:inline-flex;align-items:center;gap:.14em;font-size:20px;line-height:1}
.cn-mark b{font-weight:800}
.cn-heart{width:.62em;height:.62em;fill:var(--cn-red);margin-left:.12em;transform:translateY(-.24em)}
.cn-num{font-family:var(--cn-df);font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:.02em}

/* ── HERO (графитовый кинозал) ── */
.cn-hero{position:relative;background:var(--cn-cin);color:#fff;overflow:hidden}
.cn-hero::before{content:"";position:absolute;top:-30%;right:-10%;width:60vw;height:60vw;
 max-width:760px;max-height:760px;border-radius:50%;pointer-events:none;filter:blur(60px);
 background:radial-gradient(circle,rgba(55,182,211,.22),transparent 62%)}
.cn-hero::after{content:"";position:absolute;bottom:-24%;left:-8%;width:46vw;height:46vw;
 max-width:560px;max-height:560px;border-radius:50%;pointer-events:none;filter:blur(60px);
 background:radial-gradient(circle,rgba(225,16,63,.18),transparent 64%)}
.cn-hero__in{position:relative;z-index:2;padding:clamp(22px,3vw,32px) 0 clamp(52px,7vw,88px)}
.cn-topbar{display:flex;align-items:center;justify-content:space-between;gap:20px;
 flex-wrap:wrap;padding-bottom:clamp(40px,7vw,86px)}
.cn-topbar .cn-mark{font-size:clamp(20px,2.4vw,26px)}
.cn-slogan{font-family:var(--cn-df);font-weight:500;letter-spacing:.02em;font-size:14px;
 color:rgba(255,255,255,.62);font-style:italic}
.cn-hero__grid{display:grid;grid-template-columns:1.02fr .98fr;gap:clamp(28px,4vw,56px);align-items:center}
.cn-hero__l .cn-kick{color:#ff5f7f}
.cn-hero h1{font-size:clamp(38px,6vw,74px);margin:16px 0 0;max-width:15ch}
.cn-hero h1 em{font-style:normal;color:var(--cn-aqua)}
.cn-hero__sub{margin:clamp(18px,2.4vw,26px) 0 0;font-size:clamp(16px,1.5vw,19px);
 color:rgba(255,255,255,.74);max-width:52ch;line-height:1.62}
.cn-hero__cta{margin-top:clamp(24px,3vw,34px);display:flex;gap:14px;flex-wrap:wrap}
.cn-btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--cn-df);font-weight:700;
 font-size:15px;letter-spacing:-.01em;padding:.92em 1.4em;border-radius:999px;cursor:pointer;
 border:0;transition:background .25s,transform .25s,color .25s,border-color .25s}
.cn-btn svg{width:1.1em;height:1.1em}
.cn-btn--red{background:var(--cn-red);color:#fff}
.cn-btn--red:hover{background:var(--cn-red-d);transform:translateY(-2px)}
.cn-btn--ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.28)}
.cn-btn--ghost:hover{border-color:#fff;transform:translateY(-2px)}
.cn-btn--dark{background:var(--cn-ink);color:#fff}
.cn-btn--dark:hover{background:#000;transform:translateY(-2px)}

/* фичер-плеер в герое */
.cn-feat{position:relative;aspect-ratio:4/3;border-radius:16px;overflow:hidden;cursor:pointer;
 background:#000;box-shadow:0 44px 90px -46px rgba(0,0,0,.9);isolation:isolate}
.cn-feat img{width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.cn-feat:hover img{transform:scale(1.045)}
.cn-feat__scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05),transparent 34%,rgba(0,0,0,.6))}
.cn-feat__meta{position:absolute;left:16px;top:15px;display:flex;gap:10px;align-items:center;
 font-family:var(--cn-df);font-weight:600;font-size:12px;letter-spacing:.04em;color:#fff}
.cn-feat__tag{background:rgba(255,255,255,.16);backdrop-filter:blur(6px);
 padding:.42em .8em;border-radius:999px;text-transform:uppercase}
.cn-feat__b{position:absolute;left:18px;right:18px;bottom:16px;color:#fff}
.cn-feat__b b{font-family:var(--cn-df);font-weight:800;font-size:20px;letter-spacing:-.02em;display:block}
.cn-feat__b span{font-size:13.5px;color:rgba(255,255,255,.8)}
.cn-playbtn{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
 width:74px;height:74px;border-radius:50%;background:rgba(255,255,255,.16);backdrop-filter:blur(8px);
 border:1.5px solid rgba(255,255,255,.5);display:grid;place-items:center;
 transition:background .25s,transform .25s,border-color .25s}
.cn-playbtn svg{width:26px;height:26px;color:#fff;margin-left:3px}
.cn-feat:hover .cn-playbtn{background:var(--cn-red);border-color:var(--cn-red);transform:translate(-50%,-50%) scale(1.08)}

/* спец-строка под героем */
.cn-spec{border-top:1px solid var(--cn-line-d);margin-top:clamp(34px,4.5vw,54px);
 padding-top:22px;display:flex;flex-wrap:wrap;gap:14px 34px}
.cn-spec div{display:flex;flex-direction:column;gap:3px}
.cn-spec dt{font-family:var(--cn-df);font-weight:800;font-size:24px;letter-spacing:-.02em;color:#fff}
.cn-spec dd{margin:0;font-size:13px;color:rgba(255,255,255,.6)}

/* ── BRIEF (галерейный белый) ── */
.cn-brief{padding:clamp(64px,9vw,120px) 0}
.cn-brief__grid{display:grid;grid-template-columns:.86fr 1.14fr;gap:clamp(24px,5vw,72px);align-items:start}
.cn-brief h2{font-size:clamp(28px,3.6vw,46px)}
.cn-brief h2 .cn-mark{font-size:inherit;font-weight:500}
.cn-brief h2 .cn-mark b{font-weight:800}
.cn-brief__lede p{margin:0 0 1.1em;font-size:clamp(16px,1.35vw,18.5px);color:#31353b;max-width:62ch}
.cn-brief__lede p:last-child{margin-bottom:0}
.cn-brief__lede b{font-weight:700;color:var(--cn-ink)}
.cn-facts{margin-top:clamp(40px,5vw,64px);display:grid;grid-template-columns:repeat(4,1fr);
 gap:1px;background:var(--cn-line);border:1px solid var(--cn-line);border-radius:14px;overflow:hidden}
.cn-fact{background:var(--cn-white);padding:22px 22px 24px}
.cn-fact b{font-family:var(--cn-df);font-weight:800;font-size:clamp(26px,3vw,38px);letter-spacing:-.03em;
 display:block;line-height:1}
.cn-fact span{display:block;margin-top:9px;font-size:13.5px;color:var(--cn-ink2);line-height:1.4}

/* ── BACKSTAGE / КАК СНЯТО ── */
.cn-make{background:var(--cn-paper);padding:clamp(64px,9vw,116px) 0;border-top:1px solid var(--cn-line)}
.cn-make__hd{max-width:60ch}
.cn-make__hd h2{font-size:clamp(28px,3.8vw,50px);margin-top:14px}
.cn-make__hd p{margin:18px 0 0;font-size:clamp(16px,1.4vw,19px);color:#31353b}
.cn-make__lead{margin-top:clamp(34px,4vw,52px);position:relative;border-radius:18px;overflow:hidden;
 aspect-ratio:16/9;background:#ddd}
.cn-make__lead img{width:100%;height:100%;object-fit:cover}
.cn-make__lead figcaption{position:absolute;left:0;right:0;bottom:0;padding:26px 24px 20px;color:#fff;
 font-size:14px;background:linear-gradient(transparent,rgba(0,0,0,.72))}
.cn-make__row{margin-top:22px;display:grid;grid-template-columns:1fr 1fr;gap:22px}
.cn-make__ph{border-radius:16px;overflow:hidden;aspect-ratio:16/10;position:relative;background:#ddd}
.cn-make__ph img{width:100%;height:100%;object-fit:cover}
.cn-make__ph figcaption{position:absolute;left:0;right:0;bottom:0;padding:20px 18px 15px;color:#fff;
 font-size:13.5px;background:linear-gradient(transparent,rgba(0,0,0,.7))}
.cn-steps{margin-top:clamp(40px,5vw,64px);display:grid;grid-template-columns:repeat(4,1fr);gap:26px 30px}
.cn-step{position:relative;padding-top:22px;border-top:2px solid var(--cn-ink)}
.cn-step .cn-num{font-size:14px;color:var(--cn-red)}
.cn-step h3{font-size:19px;margin:8px 0 7px;letter-spacing:-.02em}
.cn-step p{margin:0;font-size:14.5px;color:#31353b;line-height:1.5}

/* ── ГАЛЕРЕЯ 17 ФИЛЬМОВ (кинозал) ── */
.cn-gal{background:var(--cn-cin);color:#fff;padding:clamp(60px,8vw,110px) 0}
.cn-gal__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;
 padding-bottom:clamp(30px,4vw,48px)}
.cn-gal__hd h2{font-size:clamp(28px,3.8vw,50px)}
.cn-gal__hd .cn-kick{color:#ff5f7f}
.cn-gal__hint{font-size:14px;color:rgba(255,255,255,.55);max-width:34ch}
.cn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(212px,1fr));gap:clamp(14px,1.6vw,22px)}
.cn-tile{position:relative;aspect-ratio:1/1;border-radius:14px;overflow:hidden;cursor:pointer;
 background:#000;isolation:isolate;-webkit-tap-highlight-color:transparent}
.cn-tile img{width:100%;height:100%;object-fit:cover;transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.cn-tile:hover img,.cn-tile:focus-visible img{transform:scale(1.06)}
.cn-tile__scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.34),transparent 30%,transparent 52%,rgba(0,0,0,.72));
 transition:background .3s}
.cn-tile:hover .cn-tile__scrim{background:linear-gradient(180deg,rgba(0,0,0,.4),rgba(0,0,0,.12) 40%,rgba(0,0,0,.8))}
.cn-tile__top{position:absolute;top:12px;left:13px;right:13px;display:flex;justify-content:space-between;
 align-items:center;font-family:var(--cn-df);font-weight:700;font-size:12.5px}
.cn-tile__idx{color:rgba(255,255,255,.92)}
.cn-tile__dur{color:rgba(255,255,255,.8);background:rgba(0,0,0,.35);backdrop-filter:blur(4px);
 padding:.24em .55em;border-radius:999px;font-weight:600;font-size:11.5px}
.cn-tile__b{position:absolute;left:14px;right:14px;bottom:13px}
.cn-tile__b b{font-family:var(--cn-df);font-weight:800;font-size:19px;letter-spacing:-.02em;display:block}
.cn-tile__b span{font-size:12.5px;color:rgba(255,255,255,.7)}
.cn-tag{display:inline-block;margin-left:7px;font-size:10.5px;font-weight:700;letter-spacing:.06em;
 text-transform:uppercase;padding:.16em .5em;border-radius:999px;vertical-align:middle;
 background:rgba(255,255,255,.16);color:#fff}
.cn-tile__play{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) scale(.85);
 width:52px;height:52px;border-radius:50%;background:rgba(255,255,255,.14);backdrop-filter:blur(6px);
 border:1.4px solid rgba(255,255,255,.55);display:grid;place-items:center;opacity:0;
 transition:opacity .28s,transform .28s,background .28s,border-color .28s}
.cn-tile__play svg{width:20px;height:20px;color:#fff;margin-left:2px}
.cn-tile:hover .cn-tile__play,.cn-tile:focus-visible .cn-tile__play{opacity:1;transform:translate(-50%,-50%) scale(1)}
.cn-tile:hover .cn-tile__play{background:var(--cn-red);border-color:var(--cn-red)}

/* ── РЕЗУЛЬТАТ ── */
.cn-res{padding:clamp(62px,8vw,110px) 0;background:var(--cn-white)}
.cn-res__grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(24px,5vw,64px);align-items:start}
.cn-res h2{font-size:clamp(28px,3.6vw,46px)}
.cn-res__list{list-style:none;margin:0;padding:0;display:grid;gap:18px}
.cn-res__list li{display:flex;gap:16px;font-size:clamp(16px,1.3vw,18px);color:#31353b;
 padding-bottom:18px;border-bottom:1px solid var(--cn-line)}
.cn-res__list li:last-child{border-bottom:0;padding-bottom:0}
.cn-res__list b{font-weight:700;color:var(--cn-ink)}
.cn-res__list .cn-num{color:var(--cn-red);flex:none;font-size:16px;min-width:2.2em;padding-top:.05em}

/* ── OUTRO CTA (малиновый дренч) ── */
.cn-outro{background:var(--cn-red);color:#fff;padding:clamp(60px,8vw,104px) 0}
.cn-outro__in{display:grid;grid-template-columns:1.3fr .7fr;gap:clamp(24px,4vw,48px);align-items:center}
.cn-outro h2{font-size:clamp(28px,4vw,54px);color:#fff}
.cn-outro p{margin:16px 0 0;font-size:clamp(16px,1.5vw,19px);color:rgba(255,255,255,.9);max-width:46ch}
.cn-outro__more{margin-top:20px;font-size:14.5px;color:rgba(255,255,255,.85)}
.cn-outro__more a{color:#fff;text-decoration:underline;text-underline-offset:3px}
.cn-outro__cta{display:flex;justify-content:flex-end}
.cn-outro .cn-btn--dark{font-size:16px;padding:1.05em 1.6em}

/* ── МОДАЛКА ── */
.cn-modal{position:fixed;inset:0;z-index:var(--z-modal);display:none;align-items:center;justify-content:center;
 padding:clamp(12px,3vw,40px);background:rgba(8,9,11,.9);backdrop-filter:blur(4px)}
.cn-modal.is-open{display:flex}
.cn-modal__box{position:relative;width:min(1100px,100%);aspect-ratio:16/9;background:#000;
 border-radius:12px;overflow:hidden;box-shadow:0 40px 100px -30px rgba(0,0,0,.8)}
.cn-modal__box video{width:100%;height:100%;display:block;background:#000}
.cn-modal__x{position:absolute;top:-46px;right:0;width:38px;height:38px;border-radius:50%;
 border:1.4px solid rgba(255,255,255,.4);background:transparent;color:#fff;font-size:22px;line-height:1;
 cursor:pointer;transition:background .2s,border-color .2s}
.cn-modal__x:hover{background:rgba(255,255,255,.14);border-color:#fff}
.cn-modal__cap{position:absolute;left:2px;top:-42px;color:rgba(255,255,255,.85);font-family:var(--cn-df);
 font-weight:700;font-size:15px;letter-spacing:-.01em}
@media(max-width:640px){.cn-modal__x{top:-40px}.cn-modal__cap{top:-36px;font-size:13.5px}}

/* ── REVEAL (по умолчанию видно; анимация — только при JS) ── */
html.no-js .cn-r,html.no-js .cn-stag>*{opacity:1!important;transform:none!important}
.cn-r{opacity:0;transform:translateY(24px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.cn-r.is-in{opacity:1;transform:none}
.cn-stag>*{opacity:0;transform:translateY(20px);transition:opacity .6s cubic-bezier(.2,.7,.2,1),transform .6s cubic-bezier(.2,.7,.2,1)}
.cn-stag.is-in>*{opacity:1;transform:none}
.cn-stag.is-in>*:nth-child(2){transition-delay:.05s}
.cn-stag.is-in>*:nth-child(3){transition-delay:.1s}
.cn-stag.is-in>*:nth-child(4){transition-delay:.15s}
.cn-stag.is-in>*:nth-child(n+5){transition-delay:.2s}

/* ── АДАПТИВ ── */
@media(max-width:1020px){
 .cn-hero__grid{grid-template-columns:1fr;gap:28px}
 .cn-feat{aspect-ratio:16/9;order:-1}
 .cn-brief__grid,.cn-res__grid{grid-template-columns:1fr;gap:20px}
 .cn-outro__in{grid-template-columns:1fr;gap:26px}
 .cn-outro__cta{justify-content:flex-start}
 .cn-facts{grid-template-columns:repeat(2,1fr)}
 .cn-steps{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:680px){
 .cn{font-size:16px}
 .cn-make__row{grid-template-columns:1fr}
 .cn-spec{gap:14px 24px}
 .cn-spec dt{font-size:21px}
 .cn-grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
 .cn-tile__b b{font-size:16px}
 .cn-tile__play{width:44px;height:44px}
}
@media(max-width:420px){
 .cn-facts{grid-template-columns:1fr}
 .cn-steps{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){
 .cn-r,.cn-stag>*{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .cn *{transition-duration:.01ms!important;scroll-behavior:auto}
 .cn-feat:hover img,.cn-tile:hover img{transform:none}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Имиджевые ролики для CeramicaNova — серия из 17 фильмов по коллекциям | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: серия из 17 имиджевых видеороликов для CeramicaNova — по одному на коллекцию санфарфора. В шоуруме бренда построили съёмочную инсталляцию, художник оформил сцену, сделали замкнутый слив и подкрасили воду, чтобы показать безободковый смыв. Предметная съёмка, макро, монтаж под ключ.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hand-marketing.ru/portfolio/ceramicanova/">
<meta property="og:type" content="article"><meta property="og:title" content="Имиджевые ролики для CeramicaNova — кейс Hand Marketing">
<meta property="og:description" content="17 имиджевых фильмов о коллекциях санфарфора CeramicaNova. Съёмочная инсталляция в шоуруме, замкнутый слив, подкрашенная вода — безободковый смыв в кадре.">
<meta property="og:url" content="https://hand-marketing.ru/portfolio/ceramicanova/">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/poster-{FLAGSHIP}.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def feat_player():
    n, slug, name, var, dur = next(f for f in FILMS if f[1] == FLAGSHIP)
    return (f'<div class="cn-feat cn-play-trigger" role="button" tabindex="0" '
            f'data-src="{MEDIA}/ceramicanova-{slug}.mp4" data-title="{H.escape(name)} — имиджевый ролик" '
            f'aria-label="Смотреть ролик: {H.escape(name)}">'
            f'<img src="{IMG}/poster-{slug}.jpg" alt="Кадр из имиджевого ролика коллекции {H.escape(name)}: '
            f'подкрашенная вода в безободковой чаше" loading="eager">'
            f'<div class="cn-feat__scrim"></div>'
            f'<div class="cn-feat__meta"><span class="cn-feat__tag">Имиджевый ролик</span>'
            f'<span>Безободковый смыв · {mmss(dur)}</span></div>'
            f'<div class="cn-playbtn">{PLAY}</div>'
            f'<div class="cn-feat__b"><b>{H.escape(name)}</b>'
            f'<span>Тонированная вода обходит всю чашу — смыв читается в кадре</span></div></div>')


def hero():
    return (
      '<header class="cn-hero"><div class="cn-w cn-hero__in">'
      f'<div class="cn-topbar">{MARK()}<span class="cn-slogan">Extraordinary every day</span></div>'
      '<div class="cn-hero__grid">'
      '<div class="cn-hero__l">'
      '<span class="cn-kick">Видеопродакшн для CeramicaNova</span>'
      '<h1>Каждая коллекция — <em>отдельный фильм</em></h1>'
      '<p class="cn-hero__sub">Сняли серию из семнадцати имиджевых роликов для '
      'CeramicaNova — по одному на коллекцию санфарфора. Чистая предметная съёмка, '
      'макро глазури и линий и безободковый смыв, показанный подкрашенной водой.</p>'
      '<div class="cn-hero__cta">'
      '<a class="cn-btn cn-btn--red" href="#cn-gallery">Смотреть ролики ' + PLAY + '</a>'
      '<a class="cn-btn cn-btn--ghost" href="#cn-make">Как это снято</a>'
      '</div></div>'
      f'{feat_player()}'
      '</div>'
      '<dl class="cn-spec">'
      '<div><dt>17</dt><dd>роликов по коллекциям</dd></div>'
      '<div><dt>1&#8202;шоурум</dt><dd>съёмочная инсталляция</dd></div>'
      '<div><dt>Санфарфор</dt><dd>предметная макросъёмка</dd></div>'
      '<div><dt>Смыв</dt><dd>замкнутый слив, вода в кадре</dd></div>'
      '</dl>'
      '</div></header>')


def brief():
    return (
      '<section class="cn-brief"><div class="cn-w cn-brief__grid">'
      '<div class="cn-r"><span class="cn-kick" style="color:var(--cn-red)">О проекте</span>'
      f'<h2 style="margin-top:14px">{MARK()} — фарфор,<br>снятый как продукт-герой</h2></div>'
      '<div class="cn-brief__lede cn-r">'
      '<p><b>CeramicaNova</b> — бренд премиального санфарфора с философией '
      '«extraordinary every day»: безободковые унитазы, чистая геометрия и качество глазури. '
      'Каждую коллекцию нужно было показать не как строчку в каталоге, а как самостоятельный '
      'объект — со своим характером формы и светом.</p>'
      '<p>Мы сделали серию имиджевых роликов: по одному фильму на коллекцию. '
      'Единый визуальный язык на всю линейку, крупные планы фактуры и линий и — главный приём — '
      '<b>безободковый смыв, снятый подкрашенной водой</b>, чтобы поток был виден в кадре.</p>'
      '</div></div>'
      '<div class="cn-w"><div class="cn-facts cn-stag cn-r">'
      '<div class="cn-fact"><b>17</b><span>имиджевых роликов — по одному на коллекцию</span></div>'
      '<div class="cn-fact"><b>≈1 мин</b><span>хронометраж каждого фильма</span></div>'
      '<div class="cn-fact"><b>16:9 + 1:1</b><span>горизонталь для сайта и квадрат-обложка для соцсетей</span></div>'
      '<div class="cn-fact"><b>1 язык</b><span>единая графика и подача на всю линейку</span></div>'
      '</div></div>'
      '</section>')


def make():
    steps = [
        ('01', 'Инсталляция в шоуруме',
         'Съёмочную сцену собрали прямо в пространстве бренда — с плинтом под коллекцию '
         'и полноценным светом.'),
        ('02', 'Художник оформил сцену',
         'Декоративная штукатурка стен, реквизит и фактуры: каждый кадр читается как '
         'интерьер, а не как каталог.'),
        ('03', 'Система замкнутого слива',
         'Организовали оборотную подачу воды — смыв можно было гонять дубль за дублем '
         'без подключения к канализации.'),
        ('04', 'Подкрашенная вода',
         'Воду тонировали, чтобы безободковый смыв был виден: поток обходит всю чашу '
         'ровным кольцом прямо в кадре.'),
    ]
    cells = ''.join(
        f'<div class="cn-step"><span class="cn-num">{n}</span><h3>{H.escape(t)}</h3>'
        f'<p>{H.escape(d)}</p></div>' for n, t, d in steps)
    return (
      '<section class="cn-make" id="cn-make"><div class="cn-w">'
      '<div class="cn-make__hd cn-r"><span class="cn-kick" style="color:var(--cn-red)">Как это снято</span>'
      '<h2>Съёмочную сцену построили под смыв — а не наоборот</h2>'
      '<p>Главная сложность имиджевого ролика про сантехнику — показать смыв красиво и '
      'повторяемо. Мы решили её на площадке: инсталляция, замкнутая вода и её тонировка.</p></div>'
      f'<figure class="cn-make__lead cn-r"><img src="{IMG}/backstage-set.jpg" '
      'alt="Съёмочная инсталляция CeramicaNova в шоуруме: коллекция на плинте у декоративной '
      'стены, свет и слайдер" loading="lazy">'
      '<figcaption>Съёмочная инсталляция в шоуруме бренда: художник оформил сцену, коллекция — на плинте под светом</figcaption></figure>'
      '<div class="cn-make__row cn-r">'
      f'<figure class="cn-make__ph"><img src="{IMG}/backstage-water.jpg" '
      'alt="Подкрашенная вода поднимается в безободковой чаше во время съёмки смыва" loading="lazy">'
      '<figcaption>Подкрашенная вода — безободковый смыв читается в кадре</figcaption></figure>'
      f'<figure class="cn-make__ph"><img src="{IMG}/backstage-rig.jpg" '
      'alt="Оператор Hand Marketing на слайдере снимает коллекцию CeramicaNova в шоуруме" loading="lazy">'
      '<figcaption>Слайдер и макро: предметная съёмка каждой коллекции</figcaption></figure>'
      '</div>'
      f'<div class="cn-steps cn-stag cn-r">{cells}</div>'
      '</div></section>')


def gallery():
    tiles = ''
    for n, slug, name, var, dur in FILMS:
        tag = f'<span class="cn-tag">{var}</span>' if var else ''
        sub = 'Матовый чёрный санфарфор' if var == 'Black' else 'Имиджевый ролик коллекции'
        tiles += (
          f'<div class="cn-tile cn-play-trigger" role="button" tabindex="0" '
          f'data-src="{MEDIA}/ceramicanova-{slug}.mp4" data-title="{H.escape(name)}{" · "+var if var else ""}" '
          f'aria-label="Смотреть ролик: {H.escape(name)}{" "+var if var else ""}">'
          f'<img src="{IMG}/poster-{slug}.jpg" alt="Кадр из имиджевого ролика коллекции '
          f'{H.escape(name)}{" "+var if var else ""} CeramicaNova" loading="lazy">'
          f'<div class="cn-tile__scrim"></div>'
          f'<div class="cn-tile__top"><span class="cn-tile__idx cn-num">{n}</span>'
          f'<span class="cn-tile__dur">{mmss(dur)}</span></div>'
          f'<div class="cn-tile__play">{PLAY}</div>'
          f'<div class="cn-tile__b"><b>{H.escape(name)}{tag}</b><span>{sub}</span></div>'
          f'</div>')
    return (
      '<section class="cn-gal" id="cn-gallery"><div class="cn-w">'
      '<div class="cn-gal__hd cn-r"><div><span class="cn-kick">Галерея серии</span>'
      '<h2 style="margin-top:12px">17 фильмов — вся линейка</h2></div>'
      '<p class="cn-gal__hint">Кликните по коллекции, чтобы посмотреть её имиджевый ролик целиком.</p></div>'
      f'<div class="cn-grid cn-stag cn-r">{tiles}</div>'
      '</div></section>')


def result():
    items = [
        ('17', '<b>17 готовых имиджевых роликов</b> — по одному на каждую коллекцию '
         'санфарфора, в едином визуальном языке.'),
        ('16:9', 'Горизонтальные версии <b>для сайта и карточек товара</b> плюс квадратные '
         'обложки 1:1 <b>для соцсетей</b> и маркетплейсов.'),
        ('∞', 'Отработанная <b>съёмочная схема со смывом</b>: инсталляция, замкнутая вода и '
         'её тонировка — задел под любые новые коллекции бренда.'),
    ]
    lis = ''.join(f'<li><span class="cn-num">{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="cn-res"><div class="cn-w cn-res__grid">'
      '<div class="cn-r"><span class="cn-kick" style="color:var(--cn-red)">Результат</span>'
      '<h2 style="margin-top:14px">Что получил клиент</h2></div>'
      f'<ul class="cn-res__list cn-r">{lis}</ul>'
      '</div></section>')


def outro():
    return (
      '<section class="cn-outro"><div class="cn-w cn-outro__in">'
      '<div class="cn-r"><h2>Снимем имиджевые ролики о вашем продукте</h2>'
      '<p>Предметная съёмка, макро и продуманная площадка под сложные кадры — под ключ, '
      'в вашем фирменном стиле.</p>'
      '<div class="cn-outro__more">Больше о направлении — '
      '<a href="/videoproduction">услуга «Видеопродакшн»</a></div></div>'
      f'<div class="cn-outro__cta cn-r"><a class="cn-btn cn-btn--dark" href="#lead">'
      f'Обсудить проект {ARROW}</a></div>'
      '</div></section>')


MODAL = ('<div class="cn-modal" id="cn-modal" aria-hidden="true">'
         '<div class="cn-modal__box"><div class="cn-modal__cap" id="cn-modal-cap"></div>'
         '<button class="cn-modal__x" id="cn-modal-x" aria-label="Закрыть">&times;</button>'
         '<video id="cn-modal-video" controls playsinline preload="none"></video></div></div>')

PAGE_JS = """<script>(function(){
 var modal=document.getElementById('cn-modal'),vid=document.getElementById('cn-modal-video'),
     cap=document.getElementById('cn-modal-cap'),x=document.getElementById('cn-modal-x');
 function open(src,title){vid.src=src;cap.textContent=title||'';modal.classList.add('is-open');
  modal.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';
  var p=vid.play();if(p&&p.catch)p.catch(function(){});}
 function close(){modal.classList.remove('is-open');modal.setAttribute('aria-hidden','true');
  vid.pause();vid.removeAttribute('src');vid.load();cap.textContent='';document.body.style.overflow='';}
 [].forEach.call(document.querySelectorAll('.cn-play-trigger'),function(t){
  function go(){open(t.getAttribute('data-src'),t.getAttribute('data-title'));}
  t.addEventListener('click',go);
  t.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});
 });
 x.addEventListener('click',close);
 modal.addEventListener('click',function(e){if(e.target===modal)close();});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&modal.classList.contains('is-open'))close();});
 var els=[].slice.call(document.querySelectorAll('.cn-r'));
 function show(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(show);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
  show(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)show(n);else io.observe(n);});
})();</script>"""

BREADCRUMB_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
 '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
 '{"@type":"ListItem","position":2,"name":"Имиджевые ролики для CeramicaNova",'
 '"item":"https://hand-marketing.ru/portfolio/ceramicanova/"}]}</script>')


def build():
    body = (f'{rc.header()}<main class="cn">{hero()}{brief()}{make()}{gallery()}'
            f'{result()}</main>{MODAL}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'portfolio', 'ceramicanova')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
