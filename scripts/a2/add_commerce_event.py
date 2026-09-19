#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Блок «Стоимость и отзывы» на /event (тильдовская страница, генератора нет).

    python3 scripts/a2/add_commerce_event.py

Правит mirror/event/index-a2.html (на прод уезжает он, см. память index-a2-deploy-trap).
SEO-секция ev-seo лежит в файле дважды (мобильная и десктопная копии): блок встаёт перед
FAQ в обе, стили и JSON-LD только в первую. Идемпотентен: старый блок между маркерами
<!--hmc:event--> вырезается и вставляется заново. Цена «от» дописывается в ответ FAQ
в теле и в JSON-LD FAQPage, и в шаблон add_event_seo.py, чтобы пересборка её не потеряла.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import commerce_block as cb  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PAGE = os.path.join(ROOT, 'mirror', 'event', 'index-a2.html')
SEO_SCRIPT = os.path.join(HERE, 'add_event_seo.py')
ANCHOR = '<h3 class="ev-h3">Вопросы об организации мероприятий</h3>'
FAQ_OLD = 'Бюджет зависит от формата, площадки, числа гостей и техники.'
FAQ_NEW = ('Мероприятие под ключ стоит от 500 000 ₽, мультимедийная зона от 150 000 ₽. '
           'Итог зависит от формата, площадки, числа гостей и техники.')


def main():
    s = open(PAGE, encoding='utf-8').read()
    s, removed = re.subn(r'<!--hmc:event-->.*?<!--/hmc:event-->', '', s, flags=re.S)
    parts = s.split(ANCHOR)
    if len(parts) < 2:
        sys.exit('✗ не нашёл заголовок FAQ на /event')
    out = parts[0]
    for i, tail in enumerate(parts[1:]):
        first = i == 0
        # стили кладём в обе копии страницы: мобильную копию секции пересоздаёт
        # add_seo_mobile, и если <style> оказался только в ней, он уезжает вместе
        # с копией и блок цены остаётся без оформления. Дубль <style> безвреден,
        # дубль JSON-LD нет, поэтому разметку ставим только в первый блок
        block = ('<!--hmc:event--><h3 class="ev-h3">Стоимость и отзывы</h3>'
                 + cb.render('event', with_css=True, with_ld=first) + '<!--/hmc:event-->')
        out += block + ANCHOR + tail
    n_faq = out.count(FAQ_OLD)
    out = out.replace(FAQ_OLD, FAQ_NEW)
    open(PAGE, 'w', encoding='utf-8').write(out)

    t = open(SEO_SCRIPT, encoding='utf-8').read()
    n_tpl = t.count(FAQ_OLD)
    if n_tpl:
        open(SEO_SCRIPT, 'w', encoding='utf-8').write(t.replace(FAQ_OLD, FAQ_NEW))
    print(f'✓ /event: блоков {len(parts) - 1} (старых вырезано {removed}), '
          f'цена в FAQ {n_faq} мест, в шаблоне {n_tpl}')


if __name__ == '__main__':
    main()
