#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Единое поведение фоновых видео: заглушка, потом луп, без кнопок.

Проблема (19.09.2026): Safari в режиме энергосбережения, при выключенном
автозапуске и при «уменьшить движение» не стартует видео и рисует поверх него
свою кнопку Play. Посетитель видит мёртвый плеер там, где должен идти луп.
В Chrome этого не видно, поэтому дефект жил незамеченным.

Что делает скрипт на странице:
  1. пока ролик не поехал, видео прозрачно и виден постер;
  2. как только браузер готов, запускаем и показываем; если отказал, повторяем
     попытку до двенадцати раз и на любое действие посетителя;
  3. при «уменьшить движение» видео не играет и остаётся постер;
  4. вне экрана ставим на паузу, чтобы не грузить процессор.

Трогаем только фоновые видео: autoplay, muted, без controls. Плееры кейсов,
где посетитель сам жмёт play, не затрагиваются.

    python3 scripts/a2/add_hero_video_fix.py

Идемпотентен: блок вырезается по маркеру и вставляется заново. Страницы
с собственной логикой (три страницы видеопродакшна) пропускаем: там она
уже такая и лежит в генераторе.
"""
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', 'mirror'))
MARK = 'hm-hero-video'
SKIP = ('videoproduction/reklamnyy-rolik', 'videoproduction/korporativnyy-film',
        'videoproduction/prezentacionnyy-rolik')

BLOCK = """<style id="hm-hero-video-css">video.hm-video-idle{opacity:0!important;visibility:hidden!important}</style>
<script id="hm-hero-video">(function(){
var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var list=[].slice.call(document.querySelectorAll('video[autoplay]')).filter(function(v){
 return !v.controls&&(v.muted||v.hasAttribute('muted'))});
list.forEach(function(v){
 var tries=0;
 function show(){v.classList.remove('hm-video-idle')}
 function hide(){v.classList.add('hm-video-idle')}
 if(reduce){hide();v.removeAttribute('autoplay');try{v.pause()}catch(e){}return}
 v.muted=true;
 hide();
 function attempt(){
  if(v.readyState<3)return;
  var p=v.play();
  if(!p||!p.then){v.paused?hide():show();return}
  p.then(show).catch(function(){hide();if(++tries<12)setTimeout(attempt,700)});
 }
 ['loadeddata','canplay','canplaythrough','progress'].forEach(function(e){v.addEventListener(e,attempt)});
 attempt();
 document.addEventListener('visibilitychange',function(){if(!document.hidden)attempt()});
 ['pointerdown','touchstart','scroll','keydown'].forEach(function(e){
  window.addEventListener(e,attempt,{passive:true})});
 if('IntersectionObserver' in window){
  new IntersectionObserver(function(en){en[0].isIntersecting?attempt():v.pause()},
   {threshold:.05}).observe(v)}
});
})();</script>
"""


def main():
    patched = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '**', 'index*.html'), recursive=True)):
        rel = f.replace(ROOT + '/', '').replace('/index-a2.html', '').replace('/index.html', '')
        if rel in SKIP:
            continue
        s = open(f, encoding='utf-8').read()
        vids = [v for v in re.findall(r'<video[^>]*autoplay[^>]*>', s) if 'controls' not in v]
        s2 = re.sub(r'<style id="hm-hero-video-css">.*?</style>\s*<script id="' + MARK +
                    r'">.*?</script>\n?', '', s, flags=re.S)
        if not vids:
            if s2 != s:
                open(f, 'w', encoding='utf-8').write(s2)
                print(f'/{rel}: блок убран, автозапускаемых видео нет')
            continue
        i = s2.rfind('</body>')
        if i < 0:
            print(f'/{rel}: нет </body>, пропуск')
            continue
        open(f, 'w', encoding='utf-8').write(s2[:i] + BLOCK + s2[i:])
        patched += 1
        print(f'/{rel}: видео под контролем ({len(vids)} шт.)')
    print('страниц пропатчено:', patched)


if __name__ == '__main__':
    main()
