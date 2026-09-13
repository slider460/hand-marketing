#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Снимает с живой страницы весь видимый текст в порядке DOM и складывает
структурированный дамп в scripts/audit/pages/<slug>.json.

    python3 scripts/audit/extract_text.py event/changan        # одна страница
    python3 scripts/audit/extract_text.py --all                # всё зеркало
    python3 scripts/audit/extract_text.py --all --only video/  # префикс

Зачем: агентам-ревьюерам нельзя давать HTML — тильдовская разметка и наши
кейсы с canvas дают кашу. Здесь на выходе поток вида
    heading → paragraph → image → caption → metric → cta
где у каждого фрагмента есть якорь (селектор + первые слова) и адрес источника,
в котором его надо править: генератор scripts/a2/gen_*.py или сырое зеркало.

Два прохода — десктоп 1440 и телефон 390: у тильдовских страниц mhome-версия
несёт свой текст, и на телефоне он может отличаться. Фрагменты помечаются
vp = both | desktop | mobile.

Скрытое (t868-попапы, display:none) не собирается: это мёртвый код зеркала.
"""
import json
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
OUT = os.path.join(HERE, 'pages')
PORT = 8099

AUTOSCROLL_JS = """async () => {
  const step = Math.max(400, window.innerHeight - 100);
  const max = document.body.scrollHeight;
  for (let y = 0; y < max + step; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 110));
  }
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 350));
}"""

COLLECT_JS = r"""() => {
  const norm = s => (s || '').replace(/\s+/g, ' ').trim();
  const visible = el => {
    const st = getComputedStyle(el);
    if (st.display === 'none' || st.visibility === 'hidden') return false;
    if (parseFloat(st.opacity || '1') < 0.05) return false;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return false;
    // элемент, уведённый за экран (тильдовские офф-скрин заглушки)
    if (r.bottom < -20000 || r.right < -20000) return false;
    return true;
  };
  const selOf = el => {
    const parts = [];
    let n = el, depth = 0;
    while (n && n.nodeType === 1 && n !== document.body && depth < 5) {
      let p = n.tagName.toLowerCase();
      if (n.id) { parts.unshift(p + '#' + n.id); break; }
      const cls = (typeof n.className === 'string' && n.className.trim())
        ? '.' + n.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
      parts.unshift(p + cls);
      n = n.parentElement; depth++;
    }
    return parts.join('>');
  };
  const CHROME_SEL = ['header', 'footer', 'nav', '.hm-chrome', '.hm-hdr', '.hm-ftr',
                      '.t-menu', '.t-menusub', '.t-footer', '.t228', '.t280',
                      '#hm-cookie-consent', '#hmCookie', '.hm-header', '.hm-footer'];
  const inChrome = el => CHROME_SEL.some(s => el.closest(s));

  // ссылки и выделения внутри абзаца собираются вместе с ним, иначе в тексте
  // остаются дыры на месте <a> и фраза читается как сломанная
  const INLINE = new Set(['a', 'b', 'i', 'em', 'strong', 'span', 'u', 's', 'mark',
                          'small', 'sup', 'sub', 'br', 'code', 'nobr']);
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  const seen = new Set();
  const skip = new Set();
  let node;
  while ((node = walker.nextNode())) {
    if (skip.has(node)) continue;
    const tag = node.tagName.toLowerCase();

    if (tag === 'img' || tag === 'svg' || tag === 'canvas' || tag === 'video') {
      if (!visible(node)) continue;
      const r = node.getBoundingClientRect();
      if (r.width * r.height < 2500) continue;   // иконки и декор не считаем кадром
      out.push({
        role: 'media', tag,
        src: (node.currentSrc || node.src || '').replace(location.origin, '') || null,
        alt: node.getAttribute ? norm(node.getAttribute('alt')) : '',
        w: Math.round(r.width), h: Math.round(r.height),
        sel: selOf(node), chrome: !!inChrome(node),
        // кадр внутри ссылки это карточка-дверь, а не фотоотчёт:
        // к нему другие требования по подписи
        href: node.closest('a') ? node.closest('a').getAttribute('href') : null,
        // кадр бывает не ссылкой, а кнопкой: клик открывает поп-ап и никуда
        // не ведёт. Для подписи это принципиально разные обещания
        action: (() => {
          const b = node.closest('button, [data-video], [data-popup], [onclick]');
          if (!b) return null;
          if (b.hasAttribute('data-video')) return 'попап с видео';
          if (b.hasAttribute('data-popup')) return 'попап';
          return 'кнопка';
        })(),
      });
      continue;
    }
    if (tag === 'script' || tag === 'style' || tag === 'noscript') continue;

    // берём только элементы с собственным текстом, иначе получим текст N раз
    let own = '';
    for (const ch of node.childNodes) {
      if (ch.nodeType === 3) own += ch.nodeValue;
    }
    own = norm(own);
    if (!own || own.length < 2) continue;
    if (!visible(node)) continue;

    const kids = [...node.children];
    const inlineKids = kids.filter(k => INLINE.has(k.tagName.toLowerCase()));
    if (kids.length && kids.length === inlineKids.length) {
      own = norm(node.textContent);
      for (const k of inlineKids) {
        skip.add(k);
        for (const d of k.querySelectorAll('*')) skip.add(d);
      }
    }

    const key = own + '|' + selOf(node);
    if (seen.has(key)) continue;
    seen.add(key);

    const st = getComputedStyle(node);
    const fs = parseFloat(st.fontSize) || 16;
    let role = 'text';
    let level = null;
    const hAnc = node.closest('h1, h2, h3, h4, h5, h6');
    if (/^h[1-6]$/.test(tag)) { role = 'heading'; level = +tag[1]; }
    else if (hAnc && norm(hAnc.textContent) === own) {
      // текст заголовка завёрнут во вложенный div (тильдовская вёрстка)
      role = 'heading'; level = +hAnc.tagName[1];
    }
    else if (tag === 'figcaption') role = 'caption';
    else if (tag === 'button' || tag === 'a' && own.length < 40 && node.closest('.t-btn, .hm-btn, button')) role = 'cta';
    else if (tag === 'a') role = 'link';
    else if (tag === 'label' || node.closest('form')) role = 'form';
    else if (/caption|подпис|figc|cap$/i.test(node.className || '')) role = 'caption';
    else if (fs >= 34 && own.length < 120) { role = 'heading'; level = 0; }
    else if (own.length <= 24 && /\d/.test(own)) role = 'metric';

    out.push({
      role, tag, level, text: own, fs: Math.round(fs),
      sel: selOf(node), chrome: !!inChrome(node),
      inFigure: !!node.closest('figure'),
      href: node.closest('a') ? node.closest('a').getAttribute('href') : null,
    });
  }

  const metaOf = n => {
    const el = document.querySelector(`meta[name="${n}"], meta[property="${n}"]`);
    return el ? norm(el.getAttribute('content')) : null;
  };
  const canon = document.querySelector('link[rel="canonical"]');
  return {
    meta: {
      title: norm(document.title),
      description: metaOf('description'),
      keywords: metaOf('keywords'),
      og_title: metaOf('og:title'),
      og_description: metaOf('og:description'),
      canonical: canon ? canon.getAttribute('href') : null,
      lang: document.documentElement.getAttribute('lang'),
      robots: metaOf('robots'),
    },
    flow: out,
    imgs: [...document.images].map(i => ({
      src: (i.currentSrc || i.src || '').replace(location.origin, ''),
      alt: norm(i.getAttribute('alt')),
      w: i.naturalWidth, h: i.naturalHeight,
      // декоративные дубли (hover-слои) прячутся от скринридера:
      // пустой alt у них корректен и ошибкой не считается
      deco: i.getAttribute('aria-hidden') === 'true' || i.closest('[aria-hidden="true"]') !== null,
    })),
    links: [...document.querySelectorAll('a[href]')].map(a => ({
      href: a.getAttribute('href'), text: norm(a.textContent).slice(0, 80),
    })),
    canvasCount: document.querySelectorAll('canvas').length,
    // H1 переписываем отдельно: часть страниц несёт его скрытым (clip:rect, 1×1),
    // это не «нет H1», а спрятанный от людей текст, и лечится иначе
    h1s: [...document.querySelectorAll('h1')].map(h => {
      const st = getComputedStyle(h);
      const r = h.getBoundingClientRect();
      return {
        text: norm(h.textContent),
        visible: !(st.display === 'none' || st.visibility === 'hidden'
                   || parseFloat(st.opacity || '1') < 0.05
                   || r.width < 4 || r.height < 4
                   || (st.clip && st.clip !== 'auto')
                   || (st.clipPath && st.clipPath !== 'none' && r.width < 8)),
      };
    }),
  };
}"""


def port_free(port):
    with socket.socket() as s:
        return s.connect_ex(('127.0.0.1', port)) != 0


def all_pages():
    out = []
    for dirpath, _dirs, files in os.walk(MIRROR):
        if 'index.html' not in files:
            continue
        rel = os.path.relpath(dirpath, MIRROR)
        rel = '' if rel == '.' else rel.replace(os.sep, '/')
        out.append(rel)
    return sorted(out)


def prod_file(path):
    """Файл, который реально уезжает на прод. Если рядом лежит index-a2.html,
    деплой (deploy.yml) переименовывает его в index.html и затирает исходный."""
    base = os.path.join(MIRROR, path) if path else MIRROR
    return 'index-a2.html' if os.path.isfile(os.path.join(base, 'index-a2.html')) else 'index.html'


def find_source(path):
    """Где править текст этой страницы: генератор или сырое зеркало."""
    pf = prod_file(path)
    target = f"mirror/{path}/{pf}" if path else f"mirror/{pf}"
    gens = []
    a2 = os.path.join(ROOT, 'scripts', 'a2')
    for fn in sorted(os.listdir(a2)):
        if not fn.endswith('.py'):
            continue
        p = os.path.join(a2, fn)
        try:
            s = open(p, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        needle = f"{path}/index.html" if path else "index.html"
        if needle in s and (path or 'home' in fn):
            gens.append(f"scripts/a2/{fn}")
    prefer = [g for g in gens if os.path.basename(g).startswith('gen_')]
    if prefer:
        return {'kind': 'generator', 'file': prefer[0], 'also': prefer[1:] + [g for g in gens if g not in prefer]}
    if gens:
        return {'kind': 'script', 'file': gens[0], 'also': gens[1:]}
    return {'kind': 'mirror', 'file': target, 'also': []}


def collect(page, url):
    page.goto(url, wait_until='domcontentloaded', timeout=45000)
    page.wait_for_timeout(700)
    try:
        page.evaluate(AUTOSCROLL_JS)
    except Exception:
        pass
    page.wait_for_timeout(300)
    return page.evaluate(COLLECT_JS)


def merge(desk, mob):
    """Склеивает поток десктопа и телефона, помечая, где фрагмент виден."""
    def key(it):
        return (it.get('role'), it.get('text') or it.get('src') or '')

    mob_keys = {key(i) for i in mob['flow']}
    desk_keys = {key(i) for i in desk['flow']}
    flow = []
    for it in desk['flow']:
        it = dict(it)
        it['vp'] = 'both' if key(it) in mob_keys else 'desktop'
        flow.append(it)
    for it in mob['flow']:
        if key(it) not in desk_keys:
            it = dict(it)
            it['vp'] = 'mobile'
            flow.append(it)
    return flow


def words(flow):
    n = 0
    for it in flow:
        if it.get('text'):
            n += len([w for w in it['text'].split() if re.search(r'[А-Яа-яЁёA-Za-z]', w)])
    return n


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        sys.exit('Использование: extract_text.py <path> | --all [--only prefix]')

    only = None
    if '--only' in args:
        only = args[args.index('--only') + 1]
    if '--all' in args:
        paths = all_pages()
        if only:
            paths = [p for p in paths if p.startswith(only)]
    else:
        paths = [args[0].strip('/')]

    os.makedirs(OUT, exist_ok=True)
    server = None
    if port_free(PORT):
        server = subprocess.Popen(
            [sys.executable, '-m', 'http.server', str(PORT), '-d', MIRROR],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            if not port_free(PORT):
                break
            time.sleep(0.1)
    base = f'http://127.0.0.1:{PORT}'

    done = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel='chrome')
            # прогрев: первый запрос свежего Chrome к http.server изредка 404
            warm = browser.new_context()
            try:
                wp = warm.new_page()
                for _ in range(4):
                    r = wp.goto(base + '/', wait_until='domcontentloaded', timeout=20000)
                    if r is not None and r.status == 200:
                        break
                    wp.wait_for_timeout(400)
            except Exception:
                pass
            warm.close()

            for path in paths:
                pf = prod_file(path)
                if pf == 'index-a2.html':
                    url = f'{base}/{path}/index-a2.html' if path else base + '/index-a2.html'
                else:
                    url = f'{base}/{path}/' if path else base + '/'
                slug = path.replace('/', '-') or 'home'
                try:
                    cd = browser.new_context(viewport={'width': 1440, 'height': 900})
                    pd = cd.new_page()
                    desk = collect(pd, url)
                    cd.close()
                    cm = browser.new_context(viewport={'width': 390, 'height': 844},
                                             is_mobile=True, has_touch=True,
                                             device_scale_factor=2)
                    pm = cm.new_page()
                    mob = collect(pm, url)
                    cm.close()
                except Exception as e:
                    print(f'  ✗ {path or "(главная)"}: {e}', file=sys.stderr)
                    continue

                flow = merge(desk, mob)
                body = [i for i in flow if not i.get('chrome')]
                data = {
                    'path': path,
                    'slug': slug,
                    'url': f"https://hand-marketing.ru/{path}/" if path else "https://hand-marketing.ru/",
                    'source': find_source(path),
                    'prod_file': prod_file(path),
                    'meta': desk['meta'],
                    'h1s': desk.get('h1s', []),
                    'meta_mobile_title': mob['meta'].get('title'),
                    'stats': {
                        'words_total': words(flow),
                        'words_body': words(body),
                        'blocks': len(body),
                        'media': len([i for i in body if i['role'] == 'media']),
                        'canvas': desk.get('canvasCount', 0),
                        'imgs_no_alt': len([i for i in desk['imgs'] if not i['alt'] and not i.get('deco')]),
                        'imgs_total': len([i for i in desk['imgs'] if not i.get('deco')]),
                        'imgs_deco': len([i for i in desk['imgs'] if i.get('deco')]),
                    },
                    'flow': flow,
                    'imgs': desk['imgs'],
                    'links': desk['links'],
                }
                with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=1)
                done.append((slug, data['stats']['words_body'], data['source']['kind']))
                print(f"  ✓ {path or '(главная)':40s} {data['stats']['words_body']:5d} слов  "
                      f"{data['source']['kind']}:{os.path.basename(data['source']['file'])}")
            browser.close()
    finally:
        if server:
            server.terminate()

    print(f"\nГотово: {len(done)} страниц → scripts/audit/pages/")


if __name__ == '__main__':
    main()
