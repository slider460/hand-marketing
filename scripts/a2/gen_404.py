#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/404.html: страница «не найдено» в обвязке сайта.

Зачем: до 10.10.2026 на любой несуществующий адрес хостинг отдавал свою
заглушку Reg.ru (770 КБ, без меню сайта, со ссылкой на панель управления).
Человек, пришедший по старой ссылке (/page14437437.html и т.п.),
упирался в тупик. Здесь шапка, подвал и ссылки на основные разделы.

Подключается в mirror/.htaccess строкой ErrorDocument 404 /404.html,
статус ответа остаётся 404. Страница закрыта от индексации (noindex),
в sitemap не попадает (генератор карты берёт только index.html).

Метрики и cookie-баннера здесь нет намеренно: без счётчика страница не ставит
cookie, а пост-скрипты finalize_page.py работают только с index*.html.
Все адреса абсолютные: страница отдаётся на любом пути, хоть /a/b/c/.

Прогон: python3 scripts/a2/gen_404.py
"""
import html as H
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location('rc', os.path.join(HERE, 'react-chrome.py'))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

# куда чаще всего шли за старыми адресами: портфолио и страницы услуг
LINKS = [
    ('/project/', 'Проекты', 'Все кейсы агентства с 2012 года'),
    ('/videoproduction/', 'Видеопродакшн', 'Рекламные, имиджевые и корпоративные ролики'),
    ('/event/', 'Мероприятия', 'Корпоративы, презентации, конференции'),
    ('/exhibition/', 'Выставочные стенды', 'Дизайн и застройка под ключ'),
    ('/content/', 'Мультимедийный контент', 'Экраны, проекции, интерактив'),
    ('/creativedesign/', 'Креатив и дизайн', 'Фирменный стиль, брендбуки, полиграфия'),
    ('/price/', 'Цены', 'Сколько стоят ролики, мероприятия и стенды'),
    ('/contacts/', 'Контакты', '+7 495 580 75 37, info@hand-marketing.ru'),
]

CSS = """<style id="nf-css">
.nf{--ink:#14171C;--mut:#5A616A;--a:#673A7E;--line:rgba(20,23,28,.12);
 font-family:'Montserrat',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff}
.nf *{box-sizing:border-box}
.nf__wrap{max-width:1180px;margin:0 auto;padding:72px 40px 80px}
.nf__code{display:block;margin-bottom:10px;font-size:15px;font-weight:800;letter-spacing:.12em;color:var(--a)}
.nf h1{margin:0 0 16px;font-size:clamp(30px,4.4vw,52px);font-weight:800;letter-spacing:-.025em;line-height:1.06}
.nf__lead{margin:0 0 36px;max-width:62ch;font-size:16.5px;line-height:1.65;color:var(--mut)}
.nf__lead a{color:var(--a);font-weight:700}
.nf__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:0;padding:0;list-style:none}
.nf__grid a{display:block;height:100%;padding:20px 20px 22px;border:1px solid var(--line);border-radius:18px;
 color:var(--ink);text-decoration:none;transition:border-color .15s,transform .15s}
.nf__grid a:hover{border-color:var(--a);transform:translateY(-2px)}
.nf__grid b{display:block;margin-bottom:6px;font-size:17px;font-weight:800;letter-spacing:-.01em}
.nf__grid span{display:block;font-size:13.5px;line-height:1.5;color:var(--mut)}
@media(max-width:1000px){.nf__grid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.nf__wrap{padding:44px 18px 56px}.nf__grid{grid-template-columns:1fr}}
</style>"""


def page():
    cards = ''.join(f'<li><a href="{href}"><b>{H.escape(t)}</b><span>{H.escape(d)}</span></a></li>'
                    for href, t, d in LINKS)
    head = (
        '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Страница не найдена | Hand Marketing</title>'
        '<meta name="robots" content="noindex, follow">'
        '<link rel="icon" href="/favicon.ico">'
        + rc.FONT + rc.CSS + CSS + '</head><body>')
    body = (
        f'{rc.header()}<main class="nf"><div class="nf__wrap">'
        '<span class="nf__code">ОШИБКА 404</span>'
        '<h1>Такой страницы нет</h1>'
        '<p class="nf__lead">Адрес мог поменяться, когда сайт обновлялся, или в ссылке '
        'опечатка. Все проекты и услуги на месте: начните с раздела ниже или '
        '<a href="/">с главной</a>.</p>'
        f'<ul class="nf__grid">{cards}</ul>'
        '</div></main>'
        f'{rc.footer()}{rc.JS}</body></html>')
    out = head + body
    # меню общей обвязки ссылается на /about, /service…: на каталог сразу со слэшем, без 301
    out = re.sub(r'href="/(about|service|project|clients|contacts|privacy)"', r'href="/\1/"', out)
    return out


if __name__ == '__main__':
    p = os.path.join(ROOT, '404.html')
    open(p, 'w', encoding='utf-8').write(page())
    print('создано:', p, os.path.getsize(p) // 1024, 'КБ')
