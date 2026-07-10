#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Шоурил на главной: вместо Tilda-попапа (#popup:embedcode120, видео без автозапуска)
открываем тот же модальный плеер vp-modal, что на /videoproduction и /content:
клик -> модалка с <video controls autoplay> (звук разрешён — это жест пользователя),
закрытие крестиком/фоном/Esc, скролл-лок. Старый t868-попап остаётся в DOM мёртвым.
Идемпотентен (маркер hm-reel-vpmodal). Патчит mirror/index-a2.html и mirror/index.html.
"""
import os

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'mirror')
MARK = 'hm-reel-vpmodal'
SRC = '/media/hm-showreel.mp4'

CSS_JS = """<style id="hm-reel-vpmodal">
.vp-modal{position:fixed;inset:0;z-index:2000;display:flex;align-items:center;justify-content:center;padding:24px;background:rgba(10,12,16,.9);animation:vpFade .2s ease}
@keyframes vpFade{from{opacity:0}to{opacity:1}}
.vp-modal__box{position:relative;width:min(1100px,96vw)}
.vp-modal video{display:block;width:100%;max-height:82vh;aspect-ratio:16/9;object-fit:contain;background:#000;border-radius:14px;box-shadow:0 40px 90px -30px rgba(0,0,0,.8)}
.vp-modal__cap{margin-top:12px;color:#fff;font-weight:700;font-size:15px;font-family:'Montserrat',Arial,sans-serif}
.vp-modal__close{position:absolute;top:-14px;right:-14px;z-index:1;width:44px;height:44px;border:0;border-radius:50%;background:#FFE000;cursor:pointer;box-shadow:0 10px 24px -8px rgba(0,0,0,.6);transition:transform .15s}
.vp-modal__close:hover{transform:scale(1.08)}
.vp-modal__close::before,.vp-modal__close::after{content:"";position:absolute;left:50%;top:50%;width:20px;height:2.5px;background:#14171C;border-radius:2px}
.vp-modal__close::before{transform:translate(-50%,-50%) rotate(45deg)}
.vp-modal__close::after{transform:translate(-50%,-50%) rotate(-45deg)}
@media (max-width:640px){.vp-modal{padding:12px}.vp-modal__close{top:-10px;right:-4px;width:40px;height:40px}}
</style><script>(function(){
var opener=null;
function closeModal(){
 var m=document.querySelector('.vp-modal');if(!m)return;
 var v=m.querySelector('video');if(v){v.pause();v.removeAttribute('src');v.load();}
 m.remove();document.body.style.overflow='';
 if(opener&&opener.focus)opener.focus();opener=null;
}
function openModal(src,title){
 closeModal();
 var m=document.createElement('div');m.className='vp-modal';
 m.setAttribute('role','dialog');m.setAttribute('aria-modal','true');
 m.setAttribute('aria-label',title||'Видео');
 var box=document.createElement('div');box.className='vp-modal__box';
 var x=document.createElement('button');x.type='button';x.className='vp-modal__close';x.setAttribute('aria-label','Закрыть видео');
 var v=document.createElement('video');
 v.controls=true;v.playsInline=true;v.preload='metadata';v.autoplay=true;
 v.setAttribute('playsinline','');v.src=src;
 if(title)v.setAttribute('aria-label',title);
 box.appendChild(x);box.appendChild(v);
 if(title){var c=document.createElement('div');c.className='vp-modal__cap';c.textContent=title;box.appendChild(c);}
 m.appendChild(box);document.body.appendChild(m);
 document.body.style.overflow='hidden';
 v.play().catch(function(){});x.focus();
}
document.addEventListener('click',function(e){
 var b=e.target.closest&&e.target.closest('[data-vpfacade]');
 if(b){e.preventDefault();opener=b;openModal(b.getAttribute('data-video'),b.getAttribute('data-title')||'');return;}
 if(e.target.closest&&e.target.closest('.vp-modal__close')){closeModal();return;}
 if(e.target.classList&&e.target.classList.contains('vp-modal'))closeModal();
},true);
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal();});
})();</script>"""

def patch(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    if MARK in html:
        print(f'{path}: уже пропатчен, пропускаю')
        return
    if 'href="#popup:embedcode120"' not in html:
        print(f'{path}: ссылки на попап нет, пропускаю')
        return
    html = html.replace(
        'href="#popup:embedcode120"',
        f'href="#" data-vpfacade data-video="{SRC}" data-title="Шоурил Hand Marketing" ',
        1,
    )
    html = html.replace('</body>', CSS_JS + '</body>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{path}: готово (ссылка -> vp-modal, попап t868 больше не используется)')

for name in ('index-a2.html', 'index.html'):
    p = os.path.join(ROOT, name)
    if os.path.exists(p):
        patch(p)
