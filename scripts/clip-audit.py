#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Детектор «съехавшей вёрстки»: клиппинг и наложения ВНУТРИ Tilda-артбордов.

Обычный layout-sweep ловит только переполнение страницы (document.scrollWidth).
Но артборды Tilda имеют overflow:hidden — если элемент по координатам вылезает
за край, он ОБРЕЗАЕТСЯ (страница не скроллится, но контент режется). Плюс
элементы с фикс-координатами под десктоп на планшете НАЕЗЖАЮТ друг на друга.

Скрипт для каждой страницы × вьюпорт находит:
  A) CLIP  — видимый элемент, правый край которого выходит за правую границу
             своего артборда больше чем на THRESH, или левый край < −THRESH
             (т.е. частично срезан краем артборда);
  B) OVER  — два ТЕКСТОВЫХ элемента, чьи прямоугольники существенно пересекаются
             (наложение подписей — как у команды).

Вьюпорты — планшетный «данжер-зон» 641–1279 (где ломаются десктоп-координаты).
"""
import json
import os
import sys
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8099'
S = os.path.dirname(os.path.abspath(__file__))
sm = open(os.path.join(S, 'deploytree', 'sitemap.xml'), encoding='utf-8').read()
import re
PATHS = sorted(set(re.findall(r'<loc>https://hand-marketing\.ru(/[^<]*)</loc>', sm)))

VIEWPORTS = [('tab-port', 768, 1024), ('tab-land', 1024, 768), ('small-lap', 1180, 820)]

JS = r"""
(THRESH) => {
  const res = {clips: [], overs: []};
  const seen = new Set();
  const boards = document.querySelectorAll('.t396__artboard');
  for (const ab of boards) {
    if (ab.offsetParent === null) continue;
    const abr = ab.getBoundingClientRect();
    if (abr.height < 20) continue;
    const clipsHidden = getComputedStyle(ab.parentElement).overflow !== 'visible'
                     || getComputedStyle(ab).overflow !== 'visible';
    const elems = ab.querySelectorAll('.tn-elem');
    const texts = [];
    for (const el of elems) {
      const r = el.getBoundingClientRect();
      if (r.width < 4 || r.height < 4) continue;
      if (el.offsetParent === null) continue;
      // A) клиппинг краем артборда
      const overR = r.right - abr.right;
      const overL = abr.left - r.left;
      if (clipsHidden && (overR > THRESH || overL > THRESH)) {
        const rec = ab.closest('[id^=rec]');
        const label = (el.textContent || '').trim().slice(0, 30) || el.querySelector('img') ? (el.querySelector('img') ? 'img' : 'el') : 'el';
        res.clips.push({rec: rec ? rec.id : '?', side: overR > overL ? 'R' : 'L', px: Math.round(Math.max(overR, overL)), label});
      }
      // собрать текстовые для B
      const atom = el.querySelector('.tn-atom');
      if (atom && (atom.getAttribute('field') || '').startsWith('tn_text') && (el.textContent || '').trim().length > 1) {
        texts.push({el, r, t: (el.textContent || '').trim().slice(0, 24)});
      }
    }
    // B) наложение текстов (значимая площадь пересечения)
    for (let i = 0; i < texts.length; i++) {
      for (let j = i + 1; j < texts.length; j++) {
        const a = texts[i].r, b = texts[j].r;
        const ix = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
        const iy = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
        const inter = ix * iy;
        const minA = Math.min(a.width * a.height, b.width * b.height);
        if (inter > 0 && minA > 0 && inter / minA > 0.35) {
          const rec = texts[i].el.closest('[id^=rec]');
          const key = (rec ? rec.id : '') + texts[i].t + texts[j].t;
          if (seen.has(key)) continue; seen.add(key);
          res.overs.push({rec: rec ? rec.id : '?', a: texts[i].t, b: texts[j].t, pct: Math.round(inter / minA * 100)});
        }
      }
    }
  }
  return res;
}
"""

def main():
    THRESH = 12
    findings = {}   # path -> {vp -> {clips, overs}}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, w, h in VIEWPORTS:
            ctx = browser.new_context(viewport={'width': w, 'height': h},
                                      user_agent='Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15')
            page = ctx.new_page()
            for path in PATHS:
                try:
                    page.goto(BASE + path, wait_until='networkidle', timeout=25000)
                except Exception:
                    page.wait_for_timeout(1000)
                # прогон скроллом — инициализировать движок и reveal по всей странице
                try:
                    page.evaluate("async()=>{const H=document.body.scrollHeight;for(let y=0;y<H;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,20));}window.scrollTo(0,0);}")
                except Exception:
                    pass
                page.wait_for_timeout(500)
                try:
                    data = page.evaluate(JS, THRESH)
                except Exception as e:
                    data = {'clips': [], 'overs': [], 'err': str(e)[:80]}
                if data.get('clips') or data.get('overs'):
                    findings.setdefault(path, {})[label] = data
            ctx.close()
            print(f'[{label}] {w}x{h}: просканировано {len(PATHS)}', flush=True)
        browser.close()

    json.dump(findings, open(os.path.join(S, 'clip-audit.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # сводка: сгруппировать по rec (какие блоки чаще всего бьются)
    from collections import Counter
    rec_clip = Counter(); rec_over = Counter(); pages_bad = set()
    for path, vps in findings.items():
        for vp, d in vps.items():
            for c in d.get('clips', []):
                rec_clip[c['rec']] += 1; pages_bad.add(path)
            for o in d.get('overs', []):
                rec_over[o['rec']] += 1; pages_bad.add(path)
    print(f"\n=== ИТОГ: страниц с проблемами: {len(pages_bad)} из {len(PATHS)} ===")
    print("\nТОП блоков с КЛИППИНГОМ (rec: число срабатываний по стр×вьюпорт):")
    for rec, n in rec_clip.most_common(20):
        print(f"  {rec}: {n}")
    print("\nТОП блоков с НАЛОЖЕНИЕМ текстов:")
    for rec, n in rec_over.most_common(20):
        print(f"  {rec}: {n}")
    print("\nСтраницы с проблемами:")
    for pth in sorted(pages_bad):
        vps = findings[pth]
        tot = sum(len(d.get('clips', [])) + len(d.get('overs', [])) for d in vps.values())
        print(f"  {pth:40} [{','.join(vps.keys())}] всего {tot}")


if __name__ == '__main__':
    sys.exit(main())
