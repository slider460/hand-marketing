#!/usr/bin/env python3
"""Врезает блок кейса «Ком подарков» на страницу услуги /btl.

До этого на /btl не было ни одного кейса: услуга рассказывала о себе словами,
а доказательства жили только в общем каталоге проектов. Блок ставим между
SEO-секцией и формой — сразу после «Частые вопросы», где посетитель уже понял,
что мы делаем, и хочет увидеть пример.

Правим оба файла: index.html (то, что лежит на проде сейчас) и index-a2.html
(источник деплоя, CI переименовывает его в index.html). Идемпотентно по маркеру
btl-case-salaris. Zero-блоки Tilda не трогаем — вставка идёт целой секцией
перед блоком формы."""
import os

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'mirror')
ANCHOR = '<div id="rec237885363"'   # блок формы «Давайте сделаем проект вместе»
MARK = 'btl-case-salaris'

URL = '/btl/salaris-xmas/'
IMG = '/images/salaris-xmas'

FACTS = [
    ('23 дня', 'акция с 21 декабря по 12 января'),
    ('до 4 человек', 'копят баллы одной командой'),
    ('6 шагов', 'от чека до розыгрыша призов'),
]

SECTION = f'''<!-- {MARK}: кейс на странице услуги (вставка перед формой) -->
<style id="{MARK}-css">
.bc-sec{{font-family:'Montserrat',-apple-system,Arial,sans-serif;background:#fff;padding:0 0 72px}}
.bc-in{{max-width:1180px;margin:0 auto;padding:0 40px}}
.bc-h3{{margin:0 0 18px;font-size:clamp(20px,2.3vw,26px);font-weight:800;letter-spacing:-.015em;color:#14171C}}
.bc-card{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,400px);gap:30px;align-items:center;
 background:#4C3594;border-radius:26px;padding:38px 40px;color:#fff;overflow:hidden;position:relative}}
.bc-card__t{{position:relative;z-index:2}}
.bc-kick{{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
 color:rgba(255,255,255,.62);margin-bottom:12px}}
.bc-card h4{{margin:0 0 12px;font-size:clamp(22px,2.6vw,32px);font-weight:800;line-height:1.1;letter-spacing:-.02em}}
.bc-card p{{margin:0;max-width:56ch;font-size:15.5px;line-height:1.6;color:rgba(255,255,255,.84)}}
.bc-facts{{display:flex;flex-wrap:wrap;gap:12px 32px;margin:22px 0 0;padding:0;list-style:none}}
.bc-facts b{{display:block;font-size:20px;font-weight:800;letter-spacing:-.02em}}
.bc-facts span{{font-size:12.5px;color:rgba(255,255,255,.62);line-height:1.35}}
.bc-go{{display:inline-flex;align-items:center;gap:9px;margin-top:26px;height:50px;padding:0 28px;border-radius:30px;
 background:#FF4D8D;color:#fff;font-weight:800;font-size:15px;text-decoration:none;transition:transform .15s,background .15s}}
.bc-go:hover{{background:#ff3480;transform:translateY(-2px)}}
.bc-card__p{{position:relative;z-index:2;margin:-38px -40px -38px 0}}
.bc-card__p img{{display:block;width:100%;height:auto}}
@media(max-width:960px){{.bc-card{{grid-template-columns:1fr;padding:30px 26px}}
 .bc-card__p{{margin:6px -26px -30px;max-width:340px}}}}
@media(max-width:640px){{.bc-in{{padding:0 20px}}.bc-sec{{padding-bottom:48px}}}}
</style>
<section class="bc-sec" aria-label="Кейс направления BTL">
<div class="bc-in">
<h3 class="bc-h3">Кейс направления</h3>
<div class="bc-card">
<div class="bc-card__t">
<span class="bc-kick">ТРЦ «Саларис» · сезон Christmas</span>
<h4>«Ком подарков»: акция, в которую играют всей семьёй</h4>
<p>BTL-кампания для торгового центра под ключ: командная механика накопления
баллов, карта участника, сайт и приложение акции, подарочный фонд с партнёрами,
оформление центра, промо-персонал и финальное шоу с розыгрышем автомобиля.</p>
<ul class="bc-facts">{''.join(f'<li><b>{b}</b><span>{s}</span></li>' for b, s in FACTS)}</ul>
<a class="bc-go" href="{URL}">Смотреть кейс
<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"
fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
</div>
<div class="bc-card__p"><img src="{IMG}/kom-red.png" loading="lazy" width="1000" height="838"
alt="Ком подарков — ключевой образ BTL-кампании для ТРЦ «Саларис»"></div>
</div>
</div>
</section>
'''

total = 0
for name in ('index-a2.html', 'index.html'):
    path = os.path.join(ROOT, 'btl', name)
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8') as f:
        h = f.read()
    if MARK in h:
        print(f'/btl/{name}: уже пропатчен')
        continue
    if ANCHOR not in h:
        print(f'/btl/{name}: якорь формы не найден — пропуск')
        continue
    with open(path, 'w', encoding='utf-8') as f:
        f.write(h.replace(ANCHOR, SECTION + ANCHOR, 1))
    total += 1
    print(f'/btl/{name}: блок кейса вставлен')
print('изменено файлов:', total)
