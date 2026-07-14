#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Единый автоплей-плеер (vp-modal) для ВСЕХ видео на Tilda-кейс-страницах.

Приводит воспроизведение к эталону главной (add_showreel_modal.py):
клик по постеру-триггеру -> модалка <video controls autoplay> (звук — жест
пользователя), закрытие крестиком/фоном/Esc, скролл-лок.

ВАЖНО: источник берём из scripts/a2/video_map.json (маршрут -> файлы /media),
т.к. src внутри старых Tilda-попапов боевого HTML ПРОТУХЛИ после миграции
Dropbox->/media (отдают 404 на проде). Имена из video_map проверены на проде (206).
Побочный эффект — чиним ранее битые видео на кейсах.

Механика: триггер попапа  href="#popup:embedcodeNN"  (обёртка постера) ->
  href="#" data-vpfacade data-video=<верный /media> data-title=<заголовок>.
Несколько триггеров на странице мапятся ПОЗИЦИОННО на список video_map[route]
(порядок совпадает — оба из одного порядка Tilda-блоков). Старые t-popup
остаются в DOM мёртвыми (как t868 у шоурила) — вёрстка цела.

Идемпотентен (маркер hm-vpmodal-all). Патчит index.html И index-a2.html.

Запуск: python3 scripts/a2/apply_vpmodal_players.py [--dry]
"""
import os, re, glob, sys, json, html as htmllib

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR = os.path.join(HERE, '..', '..', 'mirror')
MARK = 'hm-vpmodal-all'
DRY = '--dry' in sys.argv

VMAP = json.load(open(os.path.join(HERE, 'video_map.json'), encoding='utf-8'))['videos']
# человекочитаемые названия кейсов по маршруту (подпись в модалке)
_cases = json.load(open(os.path.join(HERE, '..', '..', 'src', 'data', 'cases.json'), encoding='utf-8'))
TITLE_BY_ROUTE = {c['route'].strip('/'): c['title'] for c in _cases}

# эталонный CSS+JS vp-modal — читаем из add_showreel_modal.py, меняем только id/marker
_src = open(os.path.join(HERE, 'add_showreel_modal.py'), encoding='utf-8').read()
CSS_JS = re.search(r'CSS_JS = """(.*?)"""', _src, re.S).group(1)
CSS_JS = CSS_JS.replace('id="hm-reel-vpmodal"', 'id="%s"' % MARK)

# доп-стили для инлайн-«stage»-видео, превращённых в постер-фасад (кнопка Play поверх постера)
STAGE_CSS = """<style id="hm-vpmodal-stage">
a.vp-stage{position:relative;display:block;cursor:pointer;text-decoration:none}
a.vp-stage>video{pointer-events:none;display:block;width:100%}
a.vp-stage .vp-stage__play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:84px;height:84px;border-radius:50%;background:rgba(20,23,28,.62);display:flex;align-items:center;justify-content:center;transition:transform .15s,background .15s}
a.vp-stage:hover .vp-stage__play{transform:translate(-50%,-50%) scale(1.07);background:rgba(20,23,28,.8)}
a.vp-stage .vp-stage__play::before{content:"";margin-left:6px;border-style:solid;border-width:15px 0 15px 26px;border-color:transparent transparent transparent #FFE000}
</style>"""


def route_of(path):
    r = path.replace(MIRROR, '').replace('/index-a2.html', '').replace('/index.html', '')
    return r.strip('/')


def page_title(html):
    t = re.search(r'<title>(.*?)</title>', html, re.S)
    if not t:
        return 'Видео'
    title = re.sub(r'\s*[—-]\s*Hand Marketing\s*$', '', htmllib.unescape(t.group(1)).strip())
    return title or 'Видео'


STAGE_RE = re.compile(
    r'<video\b([^>]*\bposter="(/portfolio/[^"]+)"[^>]*)>(.*?)</video>', re.S)


def convert_stage(html, title, report, route):
    """Инлайн-«stage»-видео (кастомная секция, poster=/portfolio/..) -> постер-фасад <a>."""
    n = 0

    def repl(m):
        nonlocal n
        attrs, poster, inner = m.group(1), m.group(2), m.group(3)
        s = re.search(r'src="([^"]+\.mp4)"', inner) or re.search(r'\bsrc="([^"]+\.mp4)"', attrs)
        if not s:
            return m.group(0)
        src = s.group(1)
        new_attrs = re.sub(r'\s*\bcontrols\b', '', attrs)      # снять controls -> постер
        n += 1
        report.append((route, 'stage', src, title))
        return ('<a href="#" class="vp-stage" data-vpfacade data-video="%s" data-title="%s">'
                '<video%s>%s</video><span class="vp-stage__play"></span></a>'
                % (src, htmllib.escape(title, quote=True), new_attrs, inner))

    return STAGE_RE.sub(repl, html), n


def patch(path, report):
    html = open(path, encoding='utf-8').read()
    if MARK in html:
        return 'skip-done', 0
    route = route_of(path)
    title = TITLE_BY_ROUTE.get(route) or page_title(html)
    changed = 0
    has_stage = False

    # 1) Tilda-попап-триггеры -> фасад (источник из video_map)
    srcs = VMAP.get(route)
    trig = list(re.finditer(r'href="#popup:(embedcode\d*)"\s*', html))
    if srcs and trig:
        multi = len(srcs) > 1
        plan = []
        for k, m in enumerate(trig):
            src = srcs[k] if k < len(srcs) else srcs[-1]
            cap = title if not multi else f'{title} — ролик {k+1}'
            plan.append((m.span(), src, cap))
            report.append((route, m.group(1), src, cap))
        for (a, b), src, cap in reversed(plan):
            rep = 'href="#" data-vpfacade data-video="%s" data-title="%s" ' % (src, htmllib.escape(cap, quote=True))
            html = html[:a] + rep + html[b:]
        changed += len(plan)

    # 2) инлайн-«stage»-видео -> постер-фасад
    html, ns = convert_stage(html, title, report, route)
    if ns:
        has_stage = True
        changed += ns

    if changed == 0:
        return 'no-video', 0

    inject = CSS_JS + (STAGE_CSS if has_stage else '') + '</body>'
    html = html.replace('</body>', inject, 1)
    if not DRY:
        open(path, 'w', encoding='utf-8').write(html)
    return 'patched', changed


def main():
    files = sorted(set(
        glob.glob(os.path.join(MIRROR, '**', 'index.html'), recursive=True) +
        glob.glob(os.path.join(MIRROR, '**', 'index-a2.html'), recursive=True)
    ))
    report = []
    pages = trig = 0
    for f in files:
        st, n = patch(f, report)
        if st == 'patched':
            pages += 1
            trig += n
    # печать предложенного маппинга (уникально по маршруту, из index.html)
    seen = set()
    print('Предложенный маппинг триггер -> источник:')
    for route, key, src, cap in report:
        rk = (route, key)
        if rk in seen:
            continue
        seen.add(rk)
        print(f'  {route:24} {key:12} -> {src:44} [{cap}]')
    print(f'\nИтого: файлов пропатчено {pages} | триггеров {trig}'
          + (' (DRY — файлы не изменены)' if DRY else ''))


if __name__ == '__main__':
    main()
