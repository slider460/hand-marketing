#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сравнение наших страниц услуг с тем, что стоит в топе Яндекса.

Меряет у каждой страницы то, по чему поисковик судит, похожа ли она на место,
где услугу можно заказать: объём текста, структура заголовков, цены, отзывы,
вопросы, разметка, формы, перелинковка, вес и скорость.

    python3 scripts/audit/compare.py scripts/audit/compare-set.json out.json

Файл набора: {"группа": {"наш": "url", "топ": ["url", ...]}}
Наши страницы берём с локального mirror:8080, чтобы мерить то, что собрано сейчас.
"""
import json
import re
import sys
import urllib.parse

from playwright.sync_api import sync_playwright

JS = r"""() => {
  const T = document.body ? document.body.innerText : '';
  const words = (T.match(/[\wа-яёА-ЯЁ-]+/g) || []).length;
  const host = location.hostname.replace('www.','');
  const A = [...document.querySelectorAll('a[href]')];
  const inner = A.filter(a => { try { return new URL(a.href).hostname.replace('www.','') === host } catch(e){ return false } });
  const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => {
     try { return JSON.parse(s.textContent) } catch(e) { return null } }).filter(Boolean);
  const types = [];
  const walk = o => { if (!o) return;
     if (Array.isArray(o)) return o.forEach(walk);
     if (typeof o === 'object') { if (o['@type']) types.push([].concat(o['@type']).join('/'));
        Object.values(o).forEach(walk) } };
  walk(ld);
  const price = /(от\s*)?\d[\d\s  ]{2,}(₽|руб)/i.test(T);
  const rub = (T.match(/\d[\d\s  ]{2,}\s*(₽|руб)/gi) || []).length;
  return {
    title: document.title || '',
    descr: (document.querySelector('meta[name="description"]')||{}).content || '',
    h1: [...document.querySelectorAll('h1')].map(h => h.innerText.trim()).filter(Boolean),
    h2: document.querySelectorAll('h2').length,
    h3: document.querySelectorAll('h3').length,
    words,
    imgs: document.querySelectorAll('img').length,
    imgs_noalt: [...document.querySelectorAll('img')].filter(i => !i.getAttribute('alt')).length,
    video: document.querySelectorAll('video, iframe[src*="youtube"], iframe[src*="rutube"], iframe[src*="vk.com/video"]').length,
    links_in: inner.length,
    links_out: A.length - inner.length,
    forms: document.querySelectorAll('form').length,
    inputs: document.querySelectorAll('input, textarea').length,
    tel: /(\+7|8)[\s(-]*\d{3}/.test(T),
    price, rub,
    reviews: /отзыв|благодарствен|рекомендательн/i.test(T),
    faq: /вопрос|faq/i.test(T) && (document.querySelectorAll('details').length > 0 || /FAQPage/.test(JSON.stringify(types))),
    schema: [...new Set(types)],
    dl: document.querySelectorAll('a[href$=".pdf"]').length,
  };
}"""


def measure(page, url):
    weight = {'bytes': 0, 'req': 0}

    def on_resp(r):
        weight['req'] += 1
        try:
            cl = r.headers.get('content-length')
            if cl:
                weight['bytes'] += int(cl)
        except Exception:
            pass
    page.on('response', on_resp)
    t0 = page.evaluate('() => 0') if False else None
    try:
        r = page.goto(url, wait_until='domcontentloaded', timeout=45000)
        status = r.status if r else 0
        page.wait_for_timeout(2500)
        try:
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(900)
        except Exception:
            pass
        d = page.evaluate(JS)
        nav = page.evaluate("() => { const n = performance.getEntriesByType('navigation')[0];"
                            " return n ? Math.round(n.domContentLoadedEventEnd) : null }")
    except Exception as e:
        page.remove_listener('response', on_resp)
        return {'url': url, 'error': str(e)[:120]}
    page.remove_listener('response', on_resp)
    d.update(url=url, status=status, dcl_ms=nav, req=weight['req'],
             kb=round(weight['bytes'] / 1024))
    return d


def main(setfile, out):
    data = json.load(open(setfile, encoding='utf-8'))
    res = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel='chrome', headless=True)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900},
                             user_agent=('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/126.0 Safari/537.36'))
        page = ctx.new_page()
        for group, g in data.items():
            res[group] = {'ours': [], 'top': []}
            for kind in ('ours', 'top'):
                for url in g.get(kind, []):
                    d = measure(page, url)
                    res[group][kind].append(d)
                    host = urllib.parse.urlparse(url).netloc
                    print(f'{group:22s} {kind:4s} {host:28s} '
                          f'{d.get("words", "-"):>6} слов  {d.get("kb","-")} КБ  {d.get("error","")}')
        br.close()
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\nсохранено:', out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'compare.json')
