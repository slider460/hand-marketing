#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Видео-hero для React-кейсов /portfolio/samara-exhibition и /portfolio/samara-stand-vdnh
(маркер hm-pf-hero) — как на /videoproduction, /content и /event.

Исходников кейс-чанков нет (бандл перенесён с weshow) — секция вставляется в ШЕЛЛ
перед <div id="root"> (тот же приём, что react-chrome.py). Родная первая секция
приложения (тёмная карточка с заголовком) прячется CSS-ом, её бейдж/заголовок/чипы
перенесены в hero. CTA ведёт на инжект-форму hm-cta (скрипт даёт ей id).

Механика видео = vp-hero: постер-<img> под видео, .is-on по 'playing', autoplay +
немедленный play() + повтор при возврате вкладки (фоновые вкладки Chrome морозят
observer'ы), IO — пауза/возврат при скролле, prefers-reduced-motion не стартует.

Идемпотентен (повторный запуск обновляет блоки). Откат: git checkout mirror/portfolio/.
"""
import io, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MARK = "hm-pf-hero"

PAGES = {
    "samara-exhibition": {
        "video": "/media/samara-exh-hero-loop.mp4",
        "poster": "/portfolio/samara-exh-hero-poster.jpg",
        "badge": "🏛️ Проект 2024–2025",
        "title": "Выставка «Самара»",
        "accent": "в Музее им. П.В. Алабина",
        "chips": ["Музей им. П.В. Алабина, Самара", "VR и интерактивы", "Виртуальный маскот «Ладушка»"],
    },
    "samara-stand-vdnh": {
        "video": "/media/samara-vdnh-hero-loop.mp4",
        "poster": "/portfolio/samara-vdnh-hero-poster.jpg",
        "badge": "👥 Проект 2024",
        "title": "Стенд Самарской области",
        "accent": "на выставке‑форуме «Россия»",
        "chips": ["4 ноября 2023 — 8 июля 2024", "Москва, ВДНХ", "18+ млн посетителей"],
    },
}

CSS = """<style data-%(m)s="css">
.pfh{position:relative;overflow:hidden;background:#0f172a;color:#fff;font-family:'Montserrat',-apple-system,Arial,sans-serif}
.pfh__poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;margin:0}
.pfh__v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s ease;pointer-events:none}
.pfh__v.is-on{opacity:1}
.pfh__shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(2,6,23,.66) 0%,rgba(2,6,23,.38) 46%,rgba(2,6,23,.78) 100%)}
.pfh__in{position:relative;max-width:1180px;margin:0 auto;padding:104px 40px 96px;min-height:min(62vh,540px);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.pfh__badge{display:inline-flex;align-items:center;gap:8px;padding:7px 16px;border-radius:999px;background:rgba(255,255,255,.12);backdrop-filter:blur(4px);font-size:14px;font-weight:600;margin-bottom:22px}
.pfh__t{margin:0;font-size:clamp(34px,5vw,64px);line-height:1.05;font-weight:800;letter-spacing:-.02em;color:#fff}
.pfh__t span{display:block;color:#60a5fa}
.pfh__chips{margin-top:24px;display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.pfh__chip{padding:7px 14px;border-radius:999px;font-size:13.5px;font-weight:600;background:rgba(255,255,255,.1);box-shadow:inset 0 0 0 1px rgba(255,255,255,.22)}
.pfh__act{margin-top:30px}
.pfh-cta{display:inline-block;background:#FCB724;color:#14171C!important;font-weight:800;font-size:16px;text-decoration:none!important;padding:15px 40px;border-radius:30px;transition:transform .15s,box-shadow .15s}
.pfh-cta:hover{transform:translateY(-2px);box-shadow:0 14px 26px -14px rgba(252,183,36,.9)}
/* прячем родную первую секцию приложения (тёмная карточка-хедер с тем же заголовком) */
#root .min-h-screen>section:first-of-type{display:none!important}
@media(max-width:1020px){.pfh__in{padding:80px 24px 80px}}
@media(max-width:560px){.pfh__in{padding:60px 16px 64px;min-height:56vh}.pfh-cta{padding:13px 30px;font-size:15px}}
</style>""".replace("%(m)s", MARK)

JS = """<script data-%(m)s="js">(function(){
function kick(hv){hv.play&&hv.play().catch(function(){});}
function init(){
 var hv=document.querySelector('.pfh__v');
 if(!hv||hv.getAttribute('data-on'))return;
 hv.setAttribute('data-on','1');
 hv.muted=true;
 hv.addEventListener('playing',function(){hv.classList.add('is-on');});
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){
  hv.preload='metadata';hv.src=hv.getAttribute('data-src');return;
 }
 hv.autoplay=true;
 hv.src=hv.getAttribute('data-src');
 kick(hv);
 document.addEventListener('visibilitychange',function(){
  if(document.visibilityState==='visible')kick(hv);
 });
 if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(en){
   if(en.isIntersecting){if(document.visibilityState==='visible')kick(hv);}
   else{hv.pause&&hv.pause();}
  });});
  io.observe(hv);window.__pfHeroIO=io;
 }
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();</script>""".replace("%(m)s", MARK)


def section(cfg):
    chips = "".join('<span class="pfh__chip">%s</span>' % c for c in cfg["chips"])
    return ('<section class="pfh" data-%(m)s="sec">'
            '<img class="pfh__poster" src="%(poster)s" alt="" aria-hidden="true">'
            '<video class="pfh__v" muted loop playsinline preload="none" data-src="%(video)s" aria-hidden="true"></video>'
            '<div class="pfh__shade" aria-hidden="true"></div>'
            '<div class="pfh__in">'
            '<div class="pfh__badge">%(badge)s</div>'
            '<div class="pfh__t">%(title)s<span>%(accent)s</span></div>'
            '<div class="pfh__chips">%(chips)s</div>'
            '<div class="pfh__act"><a class="pfh-cta" href="#hm-cta">Обсудить проект</a></div>'
            '</div></section>') % dict(cfg, m=MARK, chips=chips)


def patch(path, cfg):
    html = io.open(path, encoding="utf-8").read()
    orig = html
    # снять прежние блоки (обновление)
    html = re.sub(r'<style data-%s="css">.*?</style>' % MARK, '', html, flags=re.S)
    html = re.sub(r'<section class="pfh" data-%s="sec">.*?</section>' % MARK, '', html, flags=re.S)
    html = re.sub(r'<script data-%s="js">.*?</script>' % MARK, '', html, flags=re.S)

    i = html.find('<div id="root">')
    if i < 0:
        print("SKIP (нет #root):", path); return False
    html = html[:i] + CSS + section(cfg) + html[i:]

    # якорь формы: секции hm-cta даём id (класс не трогаем)
    html = html.replace('<section class="hm-cta">', '<section class="hm-cta" id="hm-cta">')

    j = html.rfind("</body>")
    if j < 0:
        print("SKIP (нет </body>):", path); return False
    html = html[:j] + JS + html[j:]

    if html != orig:
        io.open(path, "w", encoding="utf-8").write(html)
        print("OK:", os.path.relpath(path, ROOT))
        return True
    print("Без изменений:", path)
    return False


if __name__ == "__main__":
    n = 0
    for slug, cfg in PAGES.items():
        for base in ("index.html", "index-a2.html"):
            p = os.path.join(ROOT, "mirror", "portfolio", slug, base)
            if os.path.exists(p):
                n += bool(patch(p, cfg))
            else:
                print("НЕТ ФАЙЛА:", p)
    sys.exit(0 if n else 1)
