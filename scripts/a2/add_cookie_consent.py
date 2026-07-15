#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Плашка согласия на cookie — как на weshow.su, но self-contained (без Tailwind/CDN).

Фиксированная снизу белая карточка: заголовок «Мы используем файлы cookie»,
текст согласия со ссылкой на /privacy, тёмная кнопка «ПРИНИМАЮ», крестик.
Показывается, пока не нажали «Принимаю»/крестик (флаг в localStorage).
Метрику НЕ гейтит (информационная модель «продолжая использовать — согласны»),
как на weshow.su.

Идемпотентен (маркер hm-cookie-consent). Патчит index.html И index-a2.html
всех страниц mirror/. Правки — только через этот скрипт.

Запуск: python3 scripts/a2/add_cookie_consent.py [--dry]
"""
import os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR = os.path.join(HERE, '..', '..', 'mirror')
MARK = 'hm-cookie-consent'
DRY = '--dry' in sys.argv

BLOCK = """<style id="hm-cookie-consent">
.hmc{position:fixed;left:0;right:0;bottom:0;z-index:9000;padding:16px;box-sizing:border-box;transform:translateY(120%);transition:transform .35s cubic-bezier(.4,0,.2,1);font-family:'Inter','Montserrat',-apple-system,Segoe UI,Roboto,Arial,sans-serif}
.hmc.is-on{transform:translateY(0)}
.hmc *,.hmc *::before,.hmc *::after{box-sizing:border-box}
.hmc__card{position:relative;max-width:1200px;margin:0 auto;background:#fff;border:1px solid #f3f4f6;border-radius:16px;box-shadow:0 25px 50px -12px rgba(0,0,0,.25);padding:24px 28px;display:flex;flex-direction:row;align-items:center;justify-content:space-between;gap:24px}
.hmc__title{font-family:'Montserrat','Inter',sans-serif;font-weight:700;font-size:16px;line-height:1.3;color:#0f172a;margin:0 0 6px}
.hmc__text{font-size:14px;line-height:1.55;color:#334155;margin:0;max-width:820px}
.hmc__text a{color:#2563eb;text-decoration:none}
.hmc__text a:hover{text-decoration:underline;text-underline-offset:3px}
.hmc__accept{flex:none;appearance:none;border:0;cursor:pointer;background:#111827;color:#fff;font-family:'Montserrat','Inter',sans-serif;font-weight:600;font-size:14px;letter-spacing:.02em;padding:14px 32px;border-radius:12px;box-shadow:0 10px 20px -8px rgba(0,0,0,.4);transition:background .15s,transform .15s,box-shadow .15s}
.hmc__accept:hover{background:#1f2937;transform:translateY(-2px);box-shadow:0 16px 26px -10px rgba(0,0,0,.45)}
.hmc__close{position:absolute;top:10px;right:12px;width:28px;height:28px;border:0;background:transparent;color:#94a3b8;font-size:22px;line-height:1;cursor:pointer;display:none}
.hmc__close:hover{color:#475569}
@media (max-width:760px){
 .hmc{padding:12px}
 .hmc__card{flex-direction:column;align-items:flex-start;gap:16px;padding:22px 20px}
 .hmc__accept{width:100%}
 .hmc__close{display:block}
}
</style>
<div class="hmc" id="hmCookie" role="dialog" aria-label="Согласие на использование файлов cookie" aria-live="polite">
 <div class="hmc__card">
  <div>
   <div class="hmc__title">Мы используем файлы cookie</div>
   <p class="hmc__text">Продолжая использовать этот сайт и нажимая кнопку «Принимаю», вы даёте согласие на обработку файлов cookie. Подробнее в <a href="/privacy">Политике обработки персональных данных</a>.</p>
  </div>
  <button type="button" class="hmc__accept" id="hmCookieOk">ПРИНИМАЮ</button>
  <button type="button" class="hmc__close" id="hmCookieX" aria-label="Закрыть">&times;</button>
 </div>
</div>
<script>(function(){
 var KEY='hm-cookie-consent';
 try{if(localStorage.getItem(KEY)==='1')return;}catch(e){}
 var box=document.getElementById('hmCookie');if(!box)return;
 function accept(){try{localStorage.setItem(KEY,'1');}catch(e){}box.classList.remove('is-on');setTimeout(function(){if(box&&box.parentNode)box.parentNode.removeChild(box);},400);}
 document.getElementById('hmCookieOk').addEventListener('click',accept);
 document.getElementById('hmCookieX').addEventListener('click',accept);
 setTimeout(function(){box.classList.add('is-on');},600);
})();</script>"""


def patch(path):
    html = open(path, encoding='utf-8').read()
    if MARK in html:
        return 'skip'
    if '</body>' not in html:
        return 'no-body'
    html = html.replace('</body>', BLOCK + '</body>', 1)
    if not DRY:
        open(path, 'w', encoding='utf-8').write(html)
    return 'patched'


def main():
    files = sorted(set(
        glob.glob(os.path.join(MIRROR, '**', 'index.html'), recursive=True) +
        glob.glob(os.path.join(MIRROR, '**', 'index-a2.html'), recursive=True)
    ))
    n = skip = 0
    for f in files:
        st = patch(f)
        if st == 'patched':
            n += 1
        elif st == 'skip':
            skip += 1
    print(f'{"[DRY] " if DRY else ""}пропатчено: {n} | уже было: {skip} | всего файлов: {len(files)}')


if __name__ == '__main__':
    main()
