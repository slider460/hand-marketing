#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Мобильные копии SEO-секций. Проблема: секции (ev-seo/sv-seo) вставлены внутрь
#allrecords, который на мобильном (max-width:640px) скрыт целиком — мобильные
посетители и mobile-first краулеры не видели новые тексты.
Решение: копия секции (без <style> и без ld+json — они остаются в одном экземпляре)
вставляется в мобильную версию перед формой (<section class="mh-form"),
в обёртке .hm-seo-mob, видимой только ≤640px. Стили секций уже адаптивны.
Идемпотентен (маркер hm-seo-mob). После повторного прогона add_event_seo/add_service_seo
перезапускать и этот скрипт.
"""
import os, re

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'mirror')
PAGES = ['event', 'creativedesign', 'btl', '3dmapping', 'printandproduction']
MOB_ANCHOR = '<section class="mh-form'

WRAP_CSS = ('<style id="hm-seo-mob-css">.hm-seo-mob{display:none}'
            '@media (max-width:640px){.hm-seo-mob{display:block}}</style>')

def extract_section(h):
    m = re.search(r'<section class="(?:ev|sv)-seo".*?</section>', h, flags=re.S)
    if not m:
        return None
    sec = m.group(0)
    # убрать ld+json из копии (schema остаётся один раз в десктоп-экземпляре)
    sec = re.sub(r'<script type="application/ld\+json">.*?</script>', '', sec, flags=re.S)
    return sec

total = 0
for slug in PAGES:
    for name in ('index-a2.html', 'index.html'):
        path = os.path.join(ROOT, slug, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8') as f:
            h = f.read()
        if 'hm-seo-mob' in h:
            print(f'/{slug}/{name}: уже пропатчен')
            continue
        if MOB_ANCHOR not in h:
            print(f'/{slug}/{name}: мобильной формы нет — пропуск')
            continue
        sec = extract_section(h)
        if not sec:
            print(f'/{slug}/{name}: SEO-секция не найдена — пропуск')
            continue
        mob = f'{WRAP_CSS}<div class="hm-seo-mob">{sec}</div>'
        h = h.replace(MOB_ANCHOR, mob + MOB_ANCHOR, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(h)
        total += 1
        print(f'/{slug}/{name}: мобильная копия вставлена перед mh-form')
print('Готово, файлов:', total)
