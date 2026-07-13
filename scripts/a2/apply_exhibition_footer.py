#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Единый подвал в стиле /exhibition (hm-foot) на ВСЕХ Tilda-страницах, все размеры
(маркер hm-foot-ex). Заменяет старые подвалы A2-страниц: тёмный .mh-foot (mhome, ≤640),
мою планшетную копию .mh-foot--u и десктопный тильдовский #t-footer — все прячутся.

Подвал ставится на body-уровень (перед </body>) → виден на любой ширине. Соцсети:
Telegram + WhatsApp + YouTube. Дизайн 1:1 с /exhibition (меню с жёлтой линией, 3 колонки
→ 1 на мобиле, реквизиты, СберКорус, копирайт).

Идемпотентно. Откат: git checkout mirror/**/index-a2.html
"""
import glob
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror')

TG = 'https://t.me/narodetskii'
WA = 'https://wa.me/79859998783'
YT = 'https://youtube.com/channel/UCKBNvpFhrJXQjzZdTnIFYxw'
SBER = '/images/lib/as6562-3737-4062-a266-336439646532/sberkorus.png'
PHONE_T = '+74955807537'
PHONE = '+7 495 580 75 37'
MAIL = 'info@hand-marketing.ru'

TG_SVG = ('<svg viewBox="0 0 24 24"><path d="M9.8 16.6l-.4 4c.5 0 .8-.2 1-.5l2.5-2.3 5 3.7'
          'c.9.5 1.6.2 1.8-.8l3.3-15.3c.3-1.2-.5-1.7-1.3-1.4L1.6 10c-1.2.5-1.2 1.1-.2 1.4l5 1.6'
          'L18 5.7c.5-.3 1-.2.6.2"/></svg>')
WA_SVG = ('<svg viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.817 11.817 0 018.413 3.488 11.824 11.824 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884a9.87 9.87 0 001.51 5.26l-.999 3.648 3.978-1.607zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>')
YT_SVG = ('<svg viewBox="0 0 24 24"><path d="M23 7.5a3 3 0 00-2.1-2.1C19 5 12 5 12 5s-7 0-8.9.4'
          'A3 3 0 001 7.5 31 31 0 001 12a31 31 0 00.1 4.5 3 3 0 002.1 2.1C5 19 12 19 12 19s7 0 8.9-.4'
          'a3 3 0 002.1-2.1A31 31 0 0023 12a31 31 0 00-.1-4.5zM10 15V9l5 3z"/></svg>')

# CSS 1:1 с /exhibition (namespace .hm-foot--x, чтобы ничего не задеть)
CSS = """<style>/*hm-foot-ex*/
.mh-foot,.mh-foot--u,#t-footer,.t-footer{display:none!important}
.hm-foot--x{background:#242424;color:#cfd2d6;padding:42px 40px 30px;font-family:'Circe','Montserrat',-apple-system,Arial,sans-serif;box-sizing:border-box}
.hm-foot--x *{box-sizing:border-box}
.hm-foot--x .hm-foot__in{max-width:1080px;margin:0 auto}
.hm-foot--x .hm-foot__nav{display:flex;flex-wrap:wrap;gap:30px;padding-bottom:22px;border-bottom:2px solid #FFE000}
.hm-foot--x .hm-foot__nav a{color:#fff;text-decoration:none;font-weight:700;font-size:16px}
.hm-foot--x .hm-foot__nav a:hover{color:#FFE000}
.hm-foot--x .hm-foot__cols{display:grid;grid-template-columns:1fr 1fr 1fr;gap:30px;padding-top:26px;font-size:13px;line-height:1.6}
.hm-foot--x a{color:#cfd2d6;text-decoration:none}
.hm-foot--x .hm-foot__c .ph{display:block;font-weight:800;font-size:17px;color:#fff;margin-bottom:4px}
.hm-foot--x .hm-foot__soc{display:flex;gap:12px;margin-top:14px}
.hm-foot--x .hm-foot__soc a{display:inline-flex;width:36px;height:36px;border-radius:50%;background:#3a3a3a;align-items:center;justify-content:center}
.hm-foot--x .hm-foot__soc svg{width:18px;height:18px;fill:#fff}
.hm-foot--x .hm-foot__sber{display:flex;align-items:center;gap:8px;margin-top:10px}
.hm-foot--x .hm-foot__sber img{height:20px;width:auto;filter:brightness(0) invert(1);opacity:.85}
.hm-foot--x .hm-foot__cp{margin-top:22px;font-size:12px;color:#8a8f96}
@media(max-width:860px){.hm-foot--x{padding:30px 18px}.hm-foot--x .hm-foot__cols{grid-template-columns:1fr;gap:20px}}
</style>"""

FOOT = (
    '<footer class="hm-foot--x" role="contentinfo"><div class="hm-foot__in">'
    '<nav class="hm-foot__nav"><a href="/about">О нас</a><a href="/service">Услуги</a>'
    '<a href="/project">Проекты</a><a href="/clients">Клиенты</a><a href="/contacts">Контакты</a></nav>'
    '<div class="hm-foot__cols">'
    f'<div class="hm-foot__c"><a class="ph" href="tel:{PHONE_T}">{PHONE}</a>'
    f'<a href="mailto:{MAIL}">{MAIL}</a>'
    '<div class="hm-foot__soc">'
    f'<a href="{TG}" target="_blank" rel="noopener" aria-label="Telegram">{TG_SVG}</a>'
    f'<a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a>'
    f'<a href="{YT}" target="_blank" rel="noopener" aria-label="YouTube">{YT_SVG}</a>'
    '</div></div>'
    '<div>© 2026 ООО «Хэнд-маркетинг»<br>ИНН 7709931482 КПП 770901001<br>ОГРН 1137746525608<br>'
    '<a href="/privacy">Политика конфиденциальности</a></div>'
    '<div>Использование материалов Hand Marketing разрешено только с согласия правообладателя'
    f'<div class="hm-foot__sber"><img src="{SBER}" alt="СберКорус"></div></div>'
    '</div><div class="hm-foot__cp">2012 — 2026 Hand Marketing</div></div></footer>'
)


def main():
    files = sorted(glob.glob(os.path.join(ROOT, '**', 'index-a2.html'), recursive=True))
    root_index = os.path.join(ROOT, 'index-a2.html')
    if os.path.exists(root_index) and root_index not in files:
        files.insert(0, root_index)
    n = 0
    for f in files:
        rel = os.path.relpath(f, ROOT)
        html = open(f, encoding='utf-8').read()
        if 'hm-foot-ex' in html:
            continue
        # кастомные React-страницы (portfolio/*) уже имеют подвал hm-foot — не дублируем
        if 'hm-foot__soc' in html or 'class="hm-foot"' in html:
            print('  = ' + rel + ': уже hm-foot (кастом), пропуск')
            continue
        if rel.startswith('samara_vdnh'):   # страница-редирект
            continue
        if '</body>' not in html:
            print(f'  !! {rel}: нет </body>, пропуск')
            continue
        html = html.replace('</body>', CSS + '\n' + FOOT + '\n</body>', 1)
        open(f, 'w', encoding='utf-8').write(html)
        n += 1
        print('  + ' + rel)
    print(f'Готово: единый подвал /exhibition на {n} A2-страницах.')


if __name__ == '__main__':
    main()
