#!/usr/bin/env python3
"""
Агентная проверка вёрстки: все страницы sitemap × 5 вьюпортов.
Для каждой: горизонтальное переполнение, элементы шире вьюпорта (топ-виновники),
ошибки консоли/страницы. Отдельно — тест «поворота» (загрузка 375 → resize 844:
ожидается автоперезагрузка rotate-fix и целая вёрстка).
Скриншоты — только для проблемных комбинаций.
"""
import json, re, sys, os
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8099'
S = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(S, 'sweep-shots'); os.makedirs(SHOTS, exist_ok=True)

# URL из sitemap деплой-копии
sm = open(os.path.join(S, 'deploytree', 'sitemap.xml'), encoding='utf-8').read()
paths = sorted(set(re.findall(r'<loc>https://hand-marketing\.ru(/[^<]*)</loc>', sm)))

VIEWPORTS = [
    ('mob-port', 375, 812),
    ('mob-land', 844, 390),
    ('tab-port', 768, 1024),
    ('tab-land', 1024, 768),
    ('desktop', 1440, 900),
]

CHECK_JS = """() => {
  const doc = document.documentElement;
  const vw = doc.clientWidth;
  const overflowPx = Math.max(0, doc.scrollWidth - vw);
  const offenders = [];
  if (overflowPx > 1) {
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width > vw + 2 || r.right > vw + 8 + Math.max(0, overflowPx)) {
        if (r.width * r.height < 16) continue;
        const cls = (el.className && typeof el.className === 'string') ? '.' + el.className.trim().split(/\\s+/).slice(0,2).join('.') : '';
        offenders.push({ sel: el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + cls, w: Math.round(r.width), right: Math.round(r.right) });
        if (offenders.length >= 5) break;
      }
    }
  }
  return { vw, scrollW: doc.scrollWidth, overflowPx, offenders };
}"""

results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for label, w, h in VIEWPORTS:
        ctx = browser.new_context(viewport={'width': w, 'height': h},
                                  user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15' if 'mob' in label else None)
        page = ctx.new_page()
        errors = []
        page.on('console', lambda m: errors.append(m.text[:160]) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errors.append(str(e)[:160]))
        for path in paths:
            errors.clear()
            try:
                page.goto(BASE + path, wait_until='networkidle', timeout=25000)
            except Exception:
                try: page.wait_for_timeout(1500)
                except Exception: pass
            page.wait_for_timeout(900)
            try:
                data = page.evaluate(CHECK_JS)
            except Exception as e:
                data = {'error': str(e)[:120], 'overflowPx': -1, 'offenders': []}
            bad_console = [e for e in errors if 'favicon' not in e and '404' not in e]
            row = {'path': path, 'vp': label, **data, 'consoleErrors': bad_console[:4]}
            results.append(row)
            if data.get('overflowPx', 0) > 4:
                shot = os.path.join(SHOTS, f"{label}{path.rstrip('/').replace('/', '_') or '_home'}.png")
                try: page.screenshot(path=shot, full_page=False)
                except Exception: pass
                row['shot'] = shot
        ctx.close()
        print(f'[{label}] {w}x{h}: {len(paths)} страниц', flush=True)

    # тест поворота: загрузка 375 -> resize 844 (5 ключевых страниц)
    rotate_pages = ['/', '/event/', '/btl/', '/creativedesign/', '/clients/']
    ctx = browser.new_context(viewport={'width': 375, 'height': 812})
    page = ctx.new_page()
    for path in rotate_pages:
        page.goto(BASE + path, wait_until='networkidle', timeout=25000)
        page.wait_for_timeout(800)
        page.evaluate("window.__flag = true")
        page.set_viewport_size({'width': 844, 'height': 390})
        page.wait_for_timeout(1600)  # rotate-fix: debounce 250мс + reload
        try:
            reloaded = page.evaluate("!window.__flag")
            data = page.evaluate(CHECK_JS)
            tilda = page.evaluate("!!document.querySelector('#allrecords .t396__artboard') || !document.querySelector('#allrecords')")
        except Exception as e:
            reloaded, data, tilda = None, {'overflowPx': -1}, None
        results.append({'path': path, 'vp': 'ROTATE 375->844', 'reloaded': reloaded,
                        'tildaInited': tilda, **data})
        print(f'[rotate] {path}: reload={reloaded} tilda={tilda} overflow={data.get("overflowPx")}', flush=True)
    ctx.close()
    browser.close()

json.dump(results, open(os.path.join(S, 'sweep-results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

bad = [r for r in results if r.get('overflowPx', 0) > 4]
print(f'\nИТОГО: {len(results)} проверок, переполнений >4px: {len(bad)}')
for r in bad:
    offs = ', '.join(o['sel'] for o in r.get('offenders', [])[:3])
    print(f"  {r['vp']:9} {r['path']:34} +{r['overflowPx']}px  [{offs}]")
conerr = [r for r in results if r.get('consoleErrors')]
print(f'страниц с JS-ошибками: {len(set(r["path"] for r in conerr))}')
for r in conerr[:10]:
    print(f"  {r['vp']:9} {r['path']:34} {r['consoleErrors'][0][:100]}")
