#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alt-тексты на главной: плитки кейсов (десктоп, планшет) и 30 логотипов клиентов.

    python3 scripts/a2/add_home_alts.py

Подпись плитки берётся из карточки того же кейса в scripts/a2/carousels/all.html
(подписи там выверены по кейсам в текстовом аудите 13.09.2026). Имена логотипов сверены
по самим картинкам. Правит mirror/index-a2.html (прод), шаблоны gen_mhome.py и
fix_home_tablet.py, чтобы пересборка не вернула пустые alt. Идемпотентен.

Десктопный каталог (t-store, rec249749070) рисует lib-catalog из JSON без alt, поэтому
подписи ставит инлайн-скрипт после отрисовки: alt первой картинке, alt="" hover-дублю,
aria-label ссылке. Вид не меняется.
"""
import html as H
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PAGE = os.path.join(ROOT, 'mirror', 'index-a2.html')

LOGOS = {  # имя файла -> клиент (порядок как на сайте)
    '-1___1.png': 'Samsung', 'samregion.png': 'Правительство Самарской области',
    '-1___1_.png': 'Mriya Resort & Spa', 'tb-drone-logo-footer.svg': 'Транспорт будущего',
    '-1___1__23.png': 'МФК «Саларис»', 'logo_1.svg': 'Технопарк «Бекабад»',
    '-1___1__22.png': 'ВСК', '-1___1__21.png': 'ТРЦ «Ривьера»', '-1___1__20.png': 'Changan',
    '-1___1__19.png': 'Московская школа управления СКОЛКОВО', '-1___1__18.png': 'Teoxane',
    '-1___1__17.png': 'Академия Научной Красоты', '-1___1__16.png': 'Hearst Shkulev Media',
    '-1___1__15.png': 'Silk Way Rally', '-1___1__14.png': 'ЛОР клиника №1',
    'logo.svg': 'Технопарк «Зубово»', '1603629-01.png': 'РЖД', '-1___1__12.png': 'МедикСити',
    '-1___1__11.png': 'VIVAX', '-1___1__10.png': 'Saint-Gobain', '-1___1__9.png': 'Marie Claire',
    '-1___1__8.png': 'Lingerie', '-1___1__7.png': 'Альфа-Центр Здоровья',
    '-1___1__6.png': 'Messe Düsseldorf', '-1___1__5.png': 'IXcellerate',
    '-1___1__4.png': 'ТРЦ «Мозаика»', '-1___1__3.png': 'Eaton',
    '__-71.png': 'Becar Asset Management', 'bella-systech.png': 'Bella-Systech',
    'ceramicanova.png': 'CeramicaNova',
}


def case_alts():
    car = open(os.path.join(HERE, 'carousels', 'all.html'), encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'<a class="mcase" href="([^"]+)".*?<div class="mcase__t">([^<]*)</div>'
                         r'<div class="mcase__d">([^<]*)</div>', car, re.S):
        t, d = H.unescape(m.group(2)).strip(), H.unescape(m.group(3)).strip()
        out[m.group(1).rstrip('/')] = f'{t}. {d}' if d else t
    return out


def main():
    alts = case_alts()
    s = open(PAGE, encoding='utf-8').read()
    log = {}

    # планшетная сетка кейсов
    def tab(m):
        a = alts.get(m.group(1).rstrip('/'))
        return m.group(0) if not a else m.group(0).replace('alt="Проект Hand Marketing"', f'alt="{H.escape(a)}"')
    s, log['планшет'] = re.subn(r'<a class="hm-cases-t__c" href="([^"]+)"><img [^>]*alt="Проект Hand Marketing"[^>]*>', tab, s)

    # логотипы: любые <img>, чей файл в словаре и alt пустой (мобильная, планшетная, десктопная сетки)
    def logo(m):
        tag = m.group(0)
        src = re.search(r'(?:data-original|src)=[\'"]([^\'"]+)', tag)
        name = LOGOS.get(os.path.basename(src.group(1))) if src else None
        if not name:
            return tag
        return re.sub(r'alt=([\'"])\1', lambda q: f'alt={q.group(1)}{H.escape(name)}{q.group(1)}', tag, count=1)
    before = s.count('alt=""') + s.count("alt=''")
    s = re.sub(r'<img\b[^>]*>', logo, s)
    log['логотипы'] = before - (s.count('alt=""') + s.count("alt=''"))

    # десктопный каталог: инлайн-скрипт
    s = re.sub(r'<script id="hm-home-card-alts">.*?</script>\n?', '', s, flags=re.S)
    js = ('<script id="hm-home-card-alts">(function(){var M=' + json.dumps(alts, ensure_ascii=False) + ';'
          'function f(){var n=0;document.querySelectorAll("#rec249749070 a[href],#rec249926772 a[href]").forEach(function(a){'
          'var h=(a.getAttribute("href")||"").replace(/^https?:\\/\\/[^\\/]+/,"").replace(/\\/$/,"");var k=M[h];if(!k)return;'
          'if(!a.getAttribute("aria-label"))a.setAttribute("aria-label",k);'
          'var im=a.querySelectorAll("img");im.forEach(function(i,j){if(!i.getAttribute("alt"))i.setAttribute("alt",j?"":k)});n++});return n}'
          'var t=0,iv=setInterval(function(){t++;if(f()>=56||t>40)clearInterval(iv)},500);})();</script>\n')
    i = s.rfind('</body>')
    s = s[:i] + js + s[i:]
    open(PAGE, 'w', encoding='utf-8').write(s)

    # шаблоны
    g = os.path.join(HERE, 'gen_mhome.py')
    t = open(g, encoding='utf-8').read()
    if 'LOGO_ALT' not in t:
        t = t.replace("logos=''.join(f'<div class=\"mh-logo\"><img src=\"{l}\" alt=\"\" loading=\"lazy\"></div>' for l in LOGOS)",
                      "from add_home_alts import LOGOS as LOGO_ALT  # alt логотипов, сверены по картинкам\n"
                      "logos=''.join(f'<div class=\"mh-logo\"><img src=\"{l}\" alt=\"{LOGO_ALT.get(l.split(\"/\")[-1], \"\")}\" loading=\"lazy\"></div>' for l in LOGOS)")
        open(g, 'w', encoding='utf-8').write(t)
    ft = os.path.join(HERE, 'fix_home_tablet.py')
    t = open(ft, encoding='utf-8').read()
    if 'case_alts' not in t:
        t = t.replace("f'<a class=\"hm-cases-t__c\" href=\"{href}\"><img src=\"{cov}\" alt=\"Проект Hand Marketing\" loading=\"lazy\"></a>'",
                      "f'<a class=\"hm-cases-t__c\" href=\"{href}\"><img src=\"{cov}\" alt=\"{_alt(href)}\" loading=\"lazy\"></a>'")
        t = t.replace("def build_block(cases):",
                      "def _alt(href):\n    import html as _h\n    from add_home_alts import case_alts\n"
                      "    return _h.escape(case_alts().get(href.rstrip('/'), 'Проект Hand Marketing'))\n\n\ndef build_block(cases):")
        open(ft, 'w', encoding='utf-8').write(t)
    print('✓ главная:', log, '| скрипт каталога: подписей', len(alts))


if __name__ == '__main__':
    main()
