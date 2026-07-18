#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Видео-hero на /event — как на /videoproduction и /content (маркер hm-event-hero).

Вставляет тёмную секцию с зацикленным лёгким роликом (/media/event-hero-loop.mp4,
~1.7 МБ, нарезка лучших моментов эвент-кейсов: Samsung, Ривьера, Changan,
Marie Claire, Саларис) и постером-кадром до старта воспроизведения:
  - в #allrecords перед старым hero (rec226728692) — десктоп/планшет (>640px);
  - в .mhome перед мобильным hero (.mh-hero) — мобильные (≤640px), только index-a2;
старые hero прячутся CSS-ом (разметка остаётся — откат = git checkout mirror/event/).

Механика как у vp-hero (gen_videoproduction.py): постер-<img> всегда под видео,
видео opacity:0 до события 'playing' (.is-on) — при заблокированном autoplay виден
только постер; пауза вне вьюпорта; prefers-reduced-motion не запускает видео.
src подставляется JS только ВИДИМОЙ копии (offsetParent) — скрытый слой ничего
не качает (preload=none, без src в разметке).

Идемпотентен: повторный запуск обновляет ранее вставленные блоки.
"""
import io, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
FILES = [os.path.join(ROOT, "mirror", "event", "index.html"),
         os.path.join(ROOT, "mirror", "event", "index-a2.html")]

MARK = "hm-event-hero"
OLD_REC = "rec226728692"   # старый белый Zero-hero «Event» (скрываем)
POSTER = "/images/event/hero-poster.jpg"
VIDEO = "/media/event-hero-loop.mp4"

CSS = f"""<style data-{MARK}="css">
/* --- видео-hero /event (по образцу vp-hero) --- */
.evh{{position:relative;overflow:hidden;background:#14171C;color:#fff;font-family:'Montserrat',-apple-system,Arial,sans-serif}}
.evh__poster{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;margin:0}}
.evh__v{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s ease;pointer-events:none}}
.evh__v.is-on{{opacity:1}}
.evh__shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,23,28,.62) 0%,rgba(20,23,28,.34) 46%,rgba(20,23,28,.74) 100%)}}
.evh__in{{position:relative;max-width:1180px;margin:0 auto;padding:110px 40px 120px;min-height:min(66vh,560px);display:flex;flex-direction:column;justify-content:center}}
.evh__t{{margin:0;font-size:clamp(44px,6.6vw,88px);line-height:.98;font-weight:800;letter-spacing:-.025em;color:#fff}}
.evh__sub{{margin:20px 0 0;font-size:clamp(18px,2vw,24px);font-weight:700;color:#fff}}
.evh__lead{{margin:18px 0 0;max-width:560px;font-size:17px;line-height:1.65;color:rgba(255,255,255,.85)}}
.evh__act{{margin-top:34px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}}
/* цвета с !important — глобальные Tilda-правила #allrecords a бьют по специфичности */
.evh-cta{{display:inline-block;background:#FCB724;color:#14171C!important;font-weight:800;font-size:16px;text-decoration:none!important;padding:16px 42px;border-radius:30px;transition:transform .15s,box-shadow .15s}}
.evh-cta:hover{{transform:translateY(-2px);box-shadow:0 14px 26px -14px rgba(252,183,36,.9)}}
#{OLD_REC}{{display:none!important}}
.mhome .mh-hero{{display:none!important}}
@media(max-width:1020px){{.evh__in{{padding:84px 24px 92px}}}}
@media(max-width:560px){{.evh__in{{padding:64px 16px 72px;min-height:60vh}}.evh__lead{{font-size:15.5px}}.evh-cta{{padding:14px 32px;font-size:15px}}}}
</style>"""

def section(anchor):
    return (f'<section class="evh" data-{MARK}="sec">'
            f'<img class="evh__poster" src="{POSTER}" alt="" aria-hidden="true">'
            f'<video class="evh__v" muted loop playsinline preload="none" data-src="{VIDEO}" aria-hidden="true"></video>'
            f'<div class="evh__shade" aria-hidden="true"></div>'
            f'<div class="evh__in">'
            f'<div class="evh__t">Event</div>'
            f'<div class="evh__sub">Ивент-агентство полного цикла</div>'
            f'<p class="evh__lead">Конференции, выставки, презентации, корпоративные мероприятия и road show — концепция, площадка, продакшн и режиссура под ключ.</p>'
            f'<div class="evh__act"><a class="evh-cta" href="{anchor}">Обсудить проект</a></div>'
            f'</div></section>')

JS = f"""<script data-{MARK}="js">(function(){{
/* старт НЕ зависит от IntersectionObserver: в фоновой вкладке Chrome морозит
   observer'ы и паузит видео — поэтому autoplay+play() сразу, ещё раз при
   возврате вкладки на передний план; IO — только пауза/возврат при скролле */
var ios=[];
function kick(hv){{hv.play&&hv.play().catch(function(){{}});}}
function init(){{
 var vs=document.querySelectorAll('.evh__v');
 [].forEach.call(vs,function(hv){{
  if(!hv.offsetParent)return;               /* скрытый слой (другой брейкпоинт) не качаем */
  if(hv.getAttribute('data-on'))return;
  hv.setAttribute('data-on','1');
  hv.muted=true;
  hv.addEventListener('playing',function(){{hv.classList.add('is-on');}});
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){{
   hv.preload='metadata';hv.src=hv.getAttribute('data-src');return;
  }}
  hv.autoplay=true;
  hv.src=hv.getAttribute('data-src');
  kick(hv);
  document.addEventListener('visibilitychange',function(){{
   if(document.visibilityState==='visible'&&hv.offsetParent)kick(hv);
  }});
  if('IntersectionObserver' in window){{
   var io=new IntersectionObserver(function(es){{es.forEach(function(en){{
    if(en.isIntersecting){{if(document.visibilityState==='visible')kick(hv);}}
    else{{hv.pause&&hv.pause();}}
   }});}});
   io.observe(hv);ios.push(io);
  }}
 }});
}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
}})();</script>"""


def strip_old(html):
    """Убрать ранее вставленные блоки (для идемпотентного обновления)."""
    html = re.sub(r'<style data-%s="css">.*?</style>' % MARK, '', html, flags=re.S)
    html = re.sub(r'<section class="evh" data-%s="sec">.*?</section>' % MARK, '', html, flags=re.S)
    html = re.sub(r'<script data-%s="js">.*?</script>' % MARK, '', html, flags=re.S)
    return html


def patch(path):
    html = io.open(path, encoding="utf-8").read()
    orig = html
    html = strip_old(html)

    # 1) десктоп/планшет: секция + стили перед старым hero-рекордом
    m = re.search(r'<div id="%s"' % OLD_REC, html)
    if not m:
        print("SKIP (нет %s): %s" % (OLD_REC, path)); return False
    html = html[:m.start()] + CSS + section("#rec237885363") + html[m.start():]

    # 2) мобильный слой (.mhome): секция перед родным .mh-hero (только index-a2)
    mh = re.search(r'<section class="mh-hero', html)
    if mh:
        html = html[:mh.start()] + section("#mh-form") + html[mh.start():]

    # 3) JS один раз перед </body>
    i = html.rfind("</body>")
    if i < 0:
        print("SKIP (нет </body>): %s" % path); return False
    html = html[:i] + JS + html[i:]

    if html != orig:
        io.open(path, "w", encoding="utf-8").write(html)
        print("OK: %s (моб. слой: %s)" % (os.path.relpath(path, ROOT), "да" if mh else "нет"))
        return True
    print("Без изменений: %s" % path)
    return False


if __name__ == "__main__":
    changed = 0
    for f in FILES:
        if os.path.exists(f):
            changed += bool(patch(f))
        else:
            print("НЕТ ФАЙЛА:", f)
    sys.exit(0 if changed or "--check" in sys.argv else 1)
