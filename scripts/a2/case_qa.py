#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA одной страницы под все девайсы и ориентации:

    python3 scripts/a2/case_qa.py event/riviera
    python3 scripts/a2/case_qa.py event/riviera --base http://127.0.0.1:8080

Без --base сам поднимает статический сервер на mirror/ (порт 8098).
6 вьюпортов: телефон портрет/ландшафт, планшет портрет/ландшафт, ноутбук, десктоп.
На каждом: автоскролл до низа (будит IntersectionObserver-reveal и lazy-картинки),
затем проверки:
  - горизонтальное переполнение + топ-виновники;
  - ошибки консоли и pageerror;
  - битые <img> (naturalWidth=0 у видимых);
  - сетевые 404 (запросы в /media/ на локальном сервере — предупреждение, не ошибка:
    крупные видео живут на хостинге);
  - маркеры hm-cookie-consent / hm-metrika-goals в DOM;
  - полностраничный скриншот в scripts/a2/qa-shots/<slug>/.
Chromium встроенный на длинных кейсах отдаёт пустые кадры → channel='chrome'.
Код возврата 1, если есть ошибки (404 в /media и prefers-reduced — не считаются).
"""
import os
import re
import socket
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
MIRROR = os.path.join(ROOT, 'mirror')
PORT = 8098

VIEWPORTS = [
    ('mob-port', 390, 844),
    ('mob-land', 844, 390),
    ('tab-port', 768, 1024),
    ('tab-land', 1024, 768),
    ('laptop', 1280, 800),
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
      if (r.width > vw + 2 || r.right > vw + 8) {
        if (r.width * r.height < 16) continue;
        const cls = (el.className && typeof el.className === 'string')
          ? '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.') : '';
        offenders.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + cls
                       + ' w=' + Math.round(r.width));
        if (offenders.length >= 5) break;
      }
    }
  }
  const brokenImgs = [...document.images]
    .filter(i => i.src && !i.src.startsWith('data:') && i.complete && !i.naturalWidth)
    .filter(i => { const r = i.getBoundingClientRect(); return r.width > 4 && r.height > 4; })
    .slice(0, 8).map(i => i.src.replace(location.origin, ''));
  return {
    overflowPx, offenders, brokenImgs,
    cookie: !!document.getElementById('hm-cookie-consent') || !!document.getElementById('hmCookie'),
    goals: !!document.getElementById('hm-metrika-goals')
        || !!document.querySelector('script#hm-metrika-goals')
        || document.documentElement.outerHTML.includes('hm-metrika-goals'),
  };
}"""

AUTOSCROLL_JS = """async () => {
  const step = Math.max(400, window.innerHeight - 100);
  const max = document.body.scrollHeight;
  for (let y = 0; y < max + step; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 120));
  }
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 400));
}"""


def port_free(port):
    with socket.socket() as s:
        return s.connect_ex(('127.0.0.1', port)) != 0


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit('Использование: python3 scripts/a2/case_qa.py <event/riviera> [--base URL]')
    path = args[0].strip('/')
    base = None
    if '--base' in args:
        base = args[args.index('--base') + 1].rstrip('/')

    if not base and not os.path.isfile(os.path.join(MIRROR, path, 'index.html')):
        sys.exit(f'✗ нет mirror/{path}/index.html')

    slug = path.replace('/', '-') or 'home'
    shots = os.path.join(HERE, 'qa-shots', slug)
    os.makedirs(shots, exist_ok=True)

    server = None
    if not base:
        if port_free(PORT):
            server = subprocess.Popen(
                [sys.executable, '-m', 'http.server', str(PORT), '-d', MIRROR],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for _ in range(50):
                if not port_free(PORT):
                    break
                time.sleep(0.1)
        base = f'http://127.0.0.1:{PORT}'
    url = f'{base}/{path}/' if path else base + '/'

    problems, warns = [], []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel='chrome')
            # прогрев: самый первый запрос свежего Chrome к локальному серверу
            # изредка возвращается 404, и первый вьюпорт снимался бы с ошибкой
            warm = browser.new_context()
            try:
                wp = warm.new_page()
                for _ in range(4):
                    r = wp.goto(url, wait_until='domcontentloaded', timeout=20000)
                    if r is not None and r.status == 200:
                        break
                    wp.wait_for_timeout(500)
            except Exception:
                pass
            warm.close()
            for name, w, h in VIEWPORTS:
                ctx = browser.new_context(viewport={'width': w, 'height': h},
                                          device_scale_factor=1)
                page = ctx.new_page()
                console_errs, req404 = [], []

                def on_console(m, acc=console_errs):
                    if m.type != 'error':
                        return
                    src = (m.location or {}).get('url', '')
                    # недоступность ВНЕШНИХ ресурсов (Метрика и т.п.) в песочнице
                    # без сети — не дефект страницы
                    if 'Failed to load resource' in m.text and not src.startswith(base):
                        return
                    acc.append(m.text)
                page.on('console', on_console)
                page.on('pageerror', lambda e, acc=console_errs: acc.append(str(e)))
                page.on('response', lambda r, acc=req404:
                        acc.append(r.url) if r.status == 404 else None)
                try:
                    resp = page.goto(url, wait_until='load', timeout=45000)
                    # локальный http.server изредка отдаёт 404 на первый запрос
                    # свежего контекста: это не дефект страницы, перезапрашиваем
                    tries = 0
                    while resp is not None and resp.status == 404 and tries < 3:
                        tries += 1
                        page.wait_for_timeout(600 * tries)
                        console_errs.clear()
                        req404.clear()
                        resp = page.goto(url, wait_until='load', timeout=45000)
                    page.wait_for_timeout(800)
                    page.evaluate(AUTOSCROLL_JS)
                    res = page.evaluate(CHECK_JS)
                    page.screenshot(path=os.path.join(shots, f'{name}.png'),
                                    full_page=True)
                except Exception as e:
                    problems.append(f'[{name}] страница не прогрузилась: {e}')
                    ctx.close()
                    continue

                tag = f'[{name} {w}x{h}]'
                if res['overflowPx'] > 1:
                    problems.append(f'{tag} гориз. переполнение {res["overflowPx"]}px: '
                                    + '; '.join(res['offenders']))
                if res['brokenImgs']:
                    problems.append(f'{tag} битые img: ' + ', '.join(res['brokenImgs']))
                if not res['cookie']:
                    problems.append(f'{tag} нет плашки cookie (hm-cookie-consent)')
                if not res['goals']:
                    problems.append(f'{tag} нет целей Метрики (hm-metrika-goals)')
                for e in console_errs:
                    if 'mc.yandex' in e or 'ERR_INTERNET_DISCONNECTED' in e:
                        continue
                    problems.append(f'{tag} console: {e[:160]}')
                for u in sorted(set(req404)):
                    short = u.replace(base, '')
                    if short.startswith('/media/'):
                        warns.append(f'{tag} 404 {short} (видео на хостинге — ок, '
                                     'если файл есть на проде)')
                    else:
                        problems.append(f'{tag} 404 {short}')
                print(f'  {name:9} {w}x{h}  ✓ снят')
                ctx.close()
            browser.close()
    finally:
        if server:
            server.terminate()

    print(f'\nСкриншоты: {os.path.relpath(shots, ROOT)}/')
    if warns:
        print('\n— Предупреждения —')
        for x in sorted(set(warns)):
            print(' ', x)
    if problems:
        print('\n== ПРОБЛЕМЫ ==')
        for x in problems:
            print(' ', x)
        sys.exit(1)
    print('\n✓ Все 6 вьюпортов чистые')


if __name__ == '__main__':
    main()
