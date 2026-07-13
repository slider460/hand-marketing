#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Единый мобильный подвал на всех Tilda-страницах (маркеры hm-foot-unify / hm-foot-canon).

Проблема 1 (СберКорус): при ширине 640–959px (айфон в ландшафте, планшет-портрет)
кастомная мобильная версия .mhome уже скрыта (её media-порог 640px), а виден
десктопный тильдовский футер #t-footer (rec237610606), у которого на брейкпоинте
640 лого СберКорус стоит на top:305px при высоте артборда 330px — низ лого
вылезает за подвал, а при ширине ≤680px и за правый край экрана.

Решение: после #t-footer вставляется копия единого мобильного подвала .mh-foot
с классом-модификатором .mh-foot--u; в диапазоне видимости #t-footer прячется:
  - страницы с .mhome: копия видна 640.5–959.98px (портрет рисует .mhome);
  - /clients и /privacy (без .mhome): копия видна на всём диапазоне ≤959.98px.

Единство подвала: и портретный `.mhome .mh-foot`, и ландшафтная копия .mh-foot--u
приводятся к ОДНОМУ каноничному HTML (CANON_INNER) — значки соцсетей (Telegram,
WhatsApp, YouTube, инлайн-SVG, без внешних CDN — принцип проекта), год 2012–2026.

Проблема 2 (маркер hm-eager-hero): верхняя картинка первого экрана «растрила»
пиксельным превью /static/thb/.../resize/20x/ пока отложенный движок td не
стартовал. Мини-IIFE перед </body> подменяет видимые (offsetParent!=null) верхние
(top<1400px) превью на оригинал (data-original). Скрытые (#allrecords на портрете)
не трогаются — лишние мегабайты на мобиле не качаются.

Идемпотентен. Откат: git checkout mirror/**/index-a2.html
"""
import glob
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror')

# --- соцссылки (взяты из десктопного #t-footer, web-friendly) ---
TG = 'https://t.me/narodetskii'
WA = 'https://wa.me/79859998783'
YT = 'https://youtube.com/channel/UCKBNvpFhrJXQjzZdTnIFYxw'

# --- инлайн-SVG значки (белые, fill:currentColor; 20×20 внутри круга 44px) ---
SVG_TG = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">'
          '<path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12'
          'c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81'
          'c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg>')
SVG_WA = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">'
          '<path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.817 '
          '11.817 0 018.413 3.488 11.824 11.824 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 '
          '11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 '
          '9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884a9.87 9.87 0 001.51 '
          '5.26l-.999 3.648 3.978-1.607zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031'
          '-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149'
          '-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347'
          '.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242'
          '-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 '
          '1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 '
          '1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>')
SVG_YT = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">'
          '<path d="M23 12s0-3.13-.4-4.63a2.4 2.4 0 00-1.7-1.7C19.4 5.27 12 5.27 12 5.27s-7.4 0-8.9.4'
          'a2.4 2.4 0 00-1.7 1.7C1 8.87 1 12 1 12s0 3.13.4 4.63c.22.83.87 1.48 1.7 1.7 1.5.4 8.9.4 8.9.4'
          's7.4 0 8.9-.4a2.4 2.4 0 001.7-1.7C23 15.13 23 12 23 12zM9.75 15.02V8.98L15.5 12l-5.75 3.02z"/></svg>')

# --- каноничное содержимое подвала (без обёртки <footer>) ---
CANON_INNER = (
    '<b>HAND MARKETING</b>'
    '<p>м. Краснопресненская / Баррикадная<br>123022, Москва, Рочдельская, 14А</p>'
    '<div class="mh-foot__c"><a href="tel:+74955807537">+7 495 580 75 37</a>'
    '<a href="mailto:info@hand-marketing.ru">info@hand-marketing.ru</a></div>'
    '<div class="mh-foot__s">'
    f'<a href="{TG}" target="_blank" rel="noopener" aria-label="Telegram">{SVG_TG}</a>'
    f'<a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{SVG_WA}</a>'
    f'<a href="{YT}" target="_blank" rel="noopener" aria-label="YouTube">{SVG_YT}</a>'
    '</div>'
    '<nav class="mh-foot__nav"><a href="/about">О нас</a><a href="/service">Услуги</a>'
    '<a href="/project">Проекты</a><a href="/clients">Клиенты</a><a href="/contacts">Контакты</a></nav>'
    '<small>© 2012–2026 ООО «Хэнд-маркетинг»</small>'
)

FOOT_HTML = f'<footer class="mh-foot mh-foot--u">{CANON_INNER}</footer>'

# {range} — media-диапазон видимости копии подвала.
# ВАЖНО: копия вставляется ВНУТРЬ #allrecords (сразу за #t-footer), поэтому
# глобальные Tilda-правила `#allrecords a{color:#ff8562}` / `.t-records a` бьют
# по id-специфичности любые классовые селекторы копии → ссылки красились в
# оранжевый и подвал НЕ совпадал с портретным (.mhome живёт вне #allrecords,
# потому чистый). Все цвета/фон в копии форсируем !important, чтобы 1:1.
FOOT_CSS = """<style>/*hm-foot-unify*/
.mh-foot--u{{display:none}}
@media {range}{{
  #t-footer,.t-footer{{display:none!important}}
  .mh-foot--u{{display:block;box-sizing:border-box;font-family:'Circe','Montserrat',-apple-system,Arial,sans-serif;background:#14171C!important;color:#cfd3d9!important;padding:40px 24px 36px;font-size:16px;line-height:1.5}}
  .mh-foot--u *{{box-sizing:border-box}}
  .mh-foot--u a{{text-decoration:none!important}}
  .mh-foot--u>b{{font-family:'Montserrat';font-weight:800;font-size:20px;letter-spacing:.04em;color:#fff!important;display:block;margin-bottom:14px}}
  .mh-foot--u>p{{margin:0 0 18px;font-size:15px;line-height:1.5;color:#cfd3d9!important}}
  .mh-foot--u .mh-foot__c{{display:flex;flex-direction:column;gap:6px;margin-bottom:18px}}
  .mh-foot--u .mh-foot__c a{{color:#fff!important;font-family:'Montserrat';font-weight:600;font-size:17px}}
  .mh-foot--u .mh-foot__s{{display:flex;gap:10px;margin-bottom:24px}}
  .mh-foot--u .mh-foot__s a{{width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.1)!important;display:flex;align-items:center;justify-content:center;color:#fff!important}}
  .mh-foot--u .mh-foot__s a svg{{width:20px;height:20px;display:block}}
  .mh-foot--u .mh-foot__nav{{display:flex;flex-wrap:wrap;gap:8px 20px;padding-top:22px;border-top:1px solid rgba(255,255,255,.12);margin-bottom:18px}}
  .mh-foot--u .mh-foot__nav a{{color:#cfd3d9!important;font-size:15px}}
  .mh-foot--u small{{color:#8A909A!important;font-size:13px}}
}}
</style>"""

# Родной десктоп-подвал #t-footer свёрстан под БАЗОВЫЙ (≥1200) дизайн: блок
# max-width:1199 у него пустой, поэтому на 960–1199 он берёт 1200-координаты и
# РЕЖЕТ элементы краем артборда (аудит: clipR ~192px на 55 страницах). Значит
# единый подвал должен покрывать весь диапазон до 1199.98; с 1200 — родной (ОК).
RANGE_LANDSCAPE = '(min-width:640.5px) and (max-width:1199.98px)'  # страницы с .mhome
RANGE_ALL_MOBILE = '(max-width:1199.98px)'                          # /clients, /privacy — без .mhome

# svg-значки в портретном подвале растянутся по инлайн width/height, но зададим
# и CSS на случай отсутствия атрибутов; правило глобальное (портрет .mh-foot).
PORTRAIT_SVG_CSS = '<style>/*hm-foot-canon*/.mh-foot__s a svg{width:20px;height:20px;display:block}</style>'

# заменяем ТОЛЬКО портретный <footer class="mh-foot"> (копия — class="mh-foot mh-foot--u",
# под этот regex не попадает).
PORTRAIT_RE = re.compile(r'<footer class="mh-foot">.*?</footer>', re.S)

EAGER_JS = (
    '<script>/*hm-eager-hero*/(function(){function go(){try{'
    "document.querySelectorAll('#allrecords img.t-img[data-original]').forEach(function(im){"
    'if(!im.offsetParent)return;'
    "if(im.src.indexOf('/thb/')===-1)return;"
    'var t=im.getBoundingClientRect().top+(window.scrollY||0);'
    "if(t<1400)im.src=im.getAttribute('data-original');});}catch(e){}}"
    "if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',go);}else{go();}"
    '})();</script>'
)


def patch(path):
    html = open(path, encoding='utf-8').read()
    changed = []

    # --- 1. портретный .mhome .mh-foot → канон (значки + год) ---
    new = PORTRAIT_RE.sub(f'<footer class="mh-foot">{CANON_INNER}</footer>', html, count=1)
    if new != html:
        html = new
        if 'hm-foot-canon' not in html:
            html = html.replace('</head>', PORTRAIT_SVG_CSS + '\n</head>', 1)
        changed.append('portrait')

    # --- 2. единая копия подвала для 640–959px (за #t-footer) ---
    if 'hm-foot-unify' not in html and 'id="t-footer"' in html:
        i = html.find('id="t-footer"')
        j = html.find('</footer>', i)
        if j < 0:
            print(f'  !! {path}: не найден </footer> у t-footer, пропуск')
        else:
            rng = RANGE_LANDSCAPE if 'id="mhome"' in html else RANGE_ALL_MOBILE
            block = '\n' + FOOT_CSS.format(range=rng) + '\n' + FOOT_HTML + '\n'
            j += len('</footer>')
            html = html[:j] + block + html[j:]
            changed.append('foot(' + ('land' if rng == RANGE_LANDSCAPE else 'mob') + ')')

    # --- 3. мгновенная подмена верхних превьюшек ---
    if 'hm-eager-hero' not in html and 'id="allrecords"' in html and '</body>' in html:
        html = html.replace('</body>', EAGER_JS + '\n</body>', 1)
        changed.append('eager')

    if changed:
        open(path, 'w', encoding='utf-8').write(html)
    return changed


def main():
    files = sorted(glob.glob(os.path.join(ROOT, '**', 'index-a2.html'), recursive=True))
    root_index = os.path.join(ROOT, 'index-a2.html')
    if os.path.exists(root_index) and root_index not in files:
        files.insert(0, root_index)
    n = 0
    for f in files:
        rel = os.path.relpath(f, ROOT)
        if rel.startswith('samara_vdnh'):  # страница-редирект
            continue
        ch = patch(f)
        if ch:
            n += 1
            print(f'  + {rel}: {", ".join(ch)}')
    print(f'Готово: изменено {n} страниц.')


if __name__ == '__main__':
    sys.exit(main())
