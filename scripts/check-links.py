#!/usr/bin/env python3
"""Проверка битых локальных ссылок по всему mirror/. Код возврата 1 — если есть битые."""
import glob, os, re, json, sys

M = 'mirror'
broken, checked = [], 0


def resolve(base, ref):
    ref = ref.split('#')[0].split('?')[0]
    if not ref or ref.startswith(('//', 'http', 'mailto:', 'tel:', 'data:', 'javascript:')):
        return None
    # /media/ — видео живут на хостинге (заливаются отдельно), не в репозитории
    if ref.startswith('/media/'):
        return None
    return os.path.normpath(M + ref) if ref.startswith('/') else os.path.normpath(os.path.join(base, ref))


for f in glob.glob(M + '/**/*.html', recursive=True):
    base = os.path.dirname(f)
    s = open(f, encoding='utf-8', errors='ignore').read()
    refs = set(re.findall(r'(?:src|href)="([^"]+)"', s))
    refs |= set(re.findall(r'data-original="([^"]+)"', s))
    refs |= set(re.findall(r"url\((?:'|\")?([^'\")]+)", s))
    for r in refs:
        p = resolve(base, r)
        if p and (r.startswith('/') or 'static/' in r or '/portfolio/' in r or '/api/' in r or r.startswith('..')):
            checked += 1
            if not os.path.exists(p):
                broken.append((f.replace(M + '/', ''), r))

for jf in glob.glob(M + '/api/getproductslist*.json'):
    for prod in json.load(open(jf)).get('products', []):
        for img in json.loads(prod.get('gallery', '[]')):
            u = img['img']
            if u.startswith('/'):
                checked += 1
                if not os.path.exists(os.path.normpath(M + u)):
                    broken.append((jf, u))

print(f'Проверено ссылок: {checked} | битых: {len(broken)}')
for b in broken[:40]:
    print('  BROKEN', b[0], '->', b[1][:80])
sys.exit(1 if broken else 0)
