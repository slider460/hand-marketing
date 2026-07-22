#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Баннер первого экрана главной во всех ориентациях (маркер hm-hero-tablet).

Что было сломано:
  1) Полоса 641–959px (айфон в альбоме, планшет в портрете): артборд героя
     #rec226204768 берёт координаты res-640, но высоту артборда 400px. Подписи
     услуг уходят ниже, а артборд с overflow:visible — они рисуются поверх
     следующей записи, фото стенда #rec2200454521 («наезжает имидж»).
  2) Портрет телефона (.mhome ≤640): имиджа не было вовсе — герой обрывался
     на пилюлях услуг.

Фикс: в полосе 641–959px прячем обе битые записи и показываем самодостаточный
.hm-hero-t с раскладкой по ориентации (альбом — две колонки, портрет планшета —
одна). В .mhome добавляем тот же имидж в конец героя.

Имидж — чистое фото стенда samara-booth.jpg, подписи положены живым текстом
(.hm-heropic__ov). Готовая обложка Samara-2.png не годится: её запечённый текст
на колонке шириной ~350–380px даёт плашки по 6px.

Идемпотентен. Откат: git checkout mirror/index-a2.html
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mirror')
PAGE = os.path.join(ROOT, 'index-a2.html')

CHIPS = [
    ('/exhibition', 'Exhibition Build', '#8E5FB0'),
    ('/content', 'Content', '#E0427E'),
    ('/event', 'Event', '#673A7E'),
    ('/creativedesign', 'Creative &amp; Design', '#C12164'),
    ('/videoproduction', 'Video Production', '#CF6F19'),
    ('/digital', 'Digital', '#5E9A2E'),
    ('/3dmapping', '3D Mapping', '#7E3FA0'),
    ('/printandproduction', 'Print &amp; Production', '#E08A2B'),
    ('/btl', 'BTL', '#D6357E'),
]

HERO_IMG = '/portfolio/samara-booth.jpg'
HERO_HREF = '/portfolio/samara-stand-vdnh'

CSS = """<style>/*hm-hero-tablet*/
.hm-hero-t{display:none}
/* имидж кейса: фото + живые подписи (общий для всех ориентаций) */
.hm-heropic{position:relative;display:block;overflow:hidden;line-height:0;border-radius:18px;
  box-shadow:0 20px 44px -24px rgba(20,23,28,.6)}
.hm-heropic img{width:100%;height:auto;display:block}
.hm-heropic__ov{position:absolute;left:0;right:0;bottom:0;display:block;padding:44px 18px 16px;
  font-family:'Montserrat',Arial,sans-serif;line-height:1.2;
  background:linear-gradient(to top,rgba(10,12,16,.86) 12%,rgba(10,12,16,.5) 55%,rgba(10,12,16,0))}
.hm-heropic__eye{display:block;margin-bottom:7px;font-weight:700;font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;color:rgba(255,255,255,.78)!important}
.hm-heropic__t{display:block;font-weight:800;font-size:21px;letter-spacing:-.01em;color:#fff!important}
.hm-heropic__m{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px}
.hm-heropic__m i{font-style:normal;padding:4px 10px;border:1px solid rgba(255,255,255,.5);border-radius:999px;
  font-weight:600;font-size:11px;color:#fff!important;white-space:nowrap}
@media (min-width:641px) and (max-width:959.98px){
  #rec226204768{display:none!important}   /* герой: тексты res-640 вылезают за артборд 400px */
  #rec2200454521{display:none!important}  /* фото стенда, на которое они наезжали */
  .hm-hero-t{display:block;background:#fff;box-sizing:border-box;color:#14171C;
    font-family:'Circe','Montserrat',-apple-system,Arial,sans-serif;
    padding:26px max(28px,env(safe-area-inset-right)) 30px max(28px,env(safe-area-inset-left))}
  .hm-hero-t *{box-sizing:border-box}
  .hm-hero-t__in{max-width:900px;margin:0 auto;display:grid;gap:24px;align-items:center}
  .hm-hero-t__eye{margin:0 0 12px;font:700 12px/1.3 'Montserrat',Arial,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#673A7E}
  .hm-hero-t__h1{margin:0;font:800 48px/.96 'Montserrat',Arial,sans-serif;letter-spacing:-.02em;color:#14171C}
  .hm-hero-t__lead{margin:14px 0 18px;font-size:17px;line-height:1.45;color:#454C54;max-width:30ch}
  .hm-hero-t__lead b{color:#14171C}
  .hm-hero-t__chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px}
  .hm-hero-t__chip{display:inline-flex;align-items:center;min-height:34px;padding:6px 14px;border-radius:999px;
    border:1.5px solid var(--c,rgba(20,23,28,.12));color:#14171C!important;text-decoration:none!important;
    font:600 13px/1 'Montserrat',Arial,sans-serif;transition:background .2s,color .2s}
  .hm-hero-t__chip:hover{background:var(--c);color:#fff!important}
  .hm-hero-t__reel{display:inline-flex;align-items:center;gap:10px;min-height:50px;padding:0 26px;border-radius:999px;
    background:#FFE000;color:#14171C!important;text-decoration:none!important;
    font:800 16px/1 'Montserrat',Arial,sans-serif;box-shadow:0 14px 30px -14px rgba(255,224,0,.9);transition:transform .2s}
  .hm-hero-t__reel:hover{transform:translateY(-2px)}
  .hm-hero-t__reel::before{content:'';width:0;height:0;border:8px solid transparent;border-left:13px solid #14171C}
}
@media (min-width:641px) and (max-width:959.98px) and (orientation:landscape){
  .hm-hero-t{padding-top:20px;padding-bottom:24px}
  .hm-hero-t__in{grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:28px}
  .hm-hero-t__h1{font-size:clamp(32px,4.8vw,42px)}
  .hm-hero-t__lead{margin:12px 0 16px;font-size:clamp(14px,1.9vw,15px)}
  .hm-hero-t__chips{gap:7px;margin-bottom:18px}
  .hm-hero-t__chip{min-height:30px;padding:5px 12px;font-size:12px}
  .hm-hero-t__reel{min-height:44px;padding:0 22px;font-size:15px}
}
@media (min-width:641px) and (max-width:959.98px) and (orientation:portrait){
  .hm-hero-t__in{grid-template-columns:1fr}
  .hm-hero-t__h1{font-size:56px}
  .hm-heropic__ov{padding:56px 24px 22px}
  .hm-heropic__eye{font-size:12px}
  .hm-heropic__t{font-size:30px}
  .hm-heropic__m i{font-size:13px;padding:5px 13px}
}
/* портрет телефона: имиджа в .mhome не было вовсе — добавляем в конец героя */
@media (max-width:640px){
  .mh-hero__pic{margin-top:4px}
}
</style>"""


def build_pic(extra_class=''):
    cls = ('hm-heropic ' + extra_class).strip()
    return (
        f'<a class="{cls}" href="{HERO_HREF}">'
        f'<img src="{HERO_IMG}" alt="Стенд Самарской области на выставке-форуме «Россия», ВДНХ" '
        'width="1592" height="894">'
        '<span class="hm-heropic__ov">'
        '<span class="hm-heropic__eye">Выставка-форум «Россия» · ВДНХ</span>'
        '<span class="hm-heropic__t">Стенд Самарской области</span>'
        '<span class="hm-heropic__m"><i>ноябрь 2023 — июль 2024</i><i>18+ млн посетителей</i></span>'
        '</span></a>'
    )


def build_block():
    chips = ''.join(
        f'<a class="hm-hero-t__chip" href="{href}" style="--c:{color}">{label}</a>'
        for href, label, color in CHIPS
    )
    return (
        f'\n{CSS}\n'
        '<section class="hm-hero-t"><div class="hm-hero-t__in">'
        '<div class="hm-hero-t__txt">'
        '<p class="hm-hero-t__eye">Рекламное агентство полного цикла · с 2012</p>'
        '<h1 class="hm-hero-t__h1">Hand<br>Marketing</h1>'
        '<p class="hm-hero-t__lead">Делаем маркетинг, <b>который видно</b> — от идеи до реализации.</p>'
        f'<div class="hm-hero-t__chips">{chips}</div>'
        '<a class="hm-hero-t__reel" href="#" data-vpfacade data-video="/media/hm-showreel.mp4"'
        ' data-title="Шоурил Hand Marketing">Смотреть шоурил</a>'
        '</div>'
        + build_pic('hm-hero-t__pic') +
        '</div></section>\n'
    )


def main():
    html = open(PAGE, encoding='utf-8').read()
    if 'hm-hero-tablet' in html:
        print('Уже применено (hm-hero-tablet), пропуск.')
        return
    a = html.find('id="rec226204768"')
    if a < 0:
        print('!! якорь rec226204768 не найден')
        return 1
    ins = html.rfind('<div ', 0, a)
    if ins < 0:
        print('!! не найдено начало <div> якоря')
        return 1
    html = html[:ins] + build_block() + html[ins:]

    # портрет телефона: имидж в конец <section class="mh-hero"> мобильной версии
    h = html.find('<section class="mh-hero">')
    end = html.find('</section>', h) if h >= 0 else -1
    if end < 0:
        print('!! секция .mh-hero в .mhome не найдена')
        return 1
    html = html[:end] + '\n  ' + build_pic('mh-hero__pic') + '\n' + html[end:]

    open(PAGE, 'w', encoding='utf-8').write(html)
    print('Готово: баннер первого экрана — 641–959px по ориентации + имидж в портрете ≤640px.')


if __name__ == '__main__':
    sys.exit(main())
