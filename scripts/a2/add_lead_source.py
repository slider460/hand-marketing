#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Источник заявки в письме с формы.

Зачем: 01.10.2026 разбирали три заказа недели и не смогли сказать, откуда пришёл ни один.
В письме с формы было только «Страница:» (Referer самого POST), то есть страница, где
нажали кнопку, а не то, как человек попал на сайт.

Что делает: на каждой странице небольшой скрипт запоминает
  - первый визит (localStorage, 180 дней): дата, страница входа, источник, utm-метки;
  - текущий визит (sessionStorage): страница входа, источник, метки;
и при любой отправке в /api/lead.php дописывает к FormData или JSON поля
«Source first visit», «Source this visit», «Pages this visit» (имена латиницей:
фильтр имён в lead.php — [\w\- ] и кириллицу может не пропустить). lead.php принимает любые поля
(до 20) и кладёт их в письмо и leads.csv, поэтому сам обработчик НЕ трогаем
(на сервере живой config.php с токенами, CLAUDE.md запрещает его перезаписывать).

Источник: домен реферера с понятным именем для поисковиков и соцсетей, utm_* и
признак yclid (клик из Директа). Без внешних запросов, без кук.

    python3 scripts/a2/add_lead_source.py          # все mirror/**/index*.html
Идемпотентен (маркер hm-lead-src, старый блок заменяется). Стоит в POSTSCRIPTS
finalize_page.py, иначе регенерация страницы блок потеряет.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
MIRROR = os.path.join(ROOT, 'mirror')
MARK = 'hm-lead-src'

JS = r"""<script id="hm-lead-src">(function(){
var LS='hm_src1',SS='hm_src',now=new Date();
function host(u){try{return new URL(u).hostname.replace(/^www\./,'')}catch(e){return''}}
function name(h){if(!h)return'прямой заход';
 if(/(^|\.)yandex\.|(^|\.)ya\.ru$/.test(h))return'Яндекс ('+h+')';
 if(/google\./.test(h))return'Google';if(/dzen\.ru$/.test(h))return'Дзен';
 if(/(^|\.)vk\.(com|ru)$/.test(h))return'ВКонтакте';if(/t\.me$|telegram/.test(h))return'Telegram';
 if(/mail\.ru$/.test(h))return'Mail.ru ('+h+')';return h}
function tags(){var q=new URLSearchParams(location.search),o=[];
 ['utm_source','utm_medium','utm_campaign','utm_term','utm_content'].forEach(function(k){var v=q.get(k);if(v)o.push(k.slice(4)+'='+v)});
 if(q.get('yclid'))o.push('Директ (yclid)');if(q.get('gclid'))o.push('Google Ads (gclid)');return o.join(', ')}
function rd(st,k){try{return JSON.parse(st.getItem(k)||'null')}catch(e){return null}}
function wr(st,k,v){try{st.setItem(k,JSON.stringify(v))}catch(e){}}
var ref=host(document.referrer),own=/hand-marketing\.ru$|weshowstudia\.ru$/.test(ref);
var cur={p:location.pathname,s:own?'внутренний переход':name(ref),t:tags(),d:now.toISOString().slice(0,10)};
var ses=rd(sessionStorage,SS);
if(!ses){ses={p:cur.p,s:cur.s,t:cur.t,n:0}}ses.n=(ses.n||0)+1;wr(sessionStorage,SS,ses);
var first=rd(localStorage,LS);
if(!first||(Date.now()-new Date(first.d).getTime())>180*864e5){first={p:cur.p,s:cur.s,t:cur.t,d:cur.d};wr(localStorage,LS,first)}
function fmt(o,date){return (date?o.d+', ':'')+o.s+', вход: '+o.p+(o.t?', '+o.t:'')}
function fields(){return{'Source first visit':fmt(first,1),'Source this visit':fmt(ses,0),'Pages this visit':String(ses.n)}}
var of=window.fetch;if(!of||of.hmSrc)return;
var nf=function(u,o){try{if(String(u).indexOf('/api/lead.php')>-1&&o&&o.body){var f=fields(),k;
 if(typeof FormData!=='undefined'&&o.body instanceof FormData){for(k in f)if(!o.body.has(k))o.body.append(k,f[k])}
 else if(typeof o.body==='string'&&o.body.charAt(0)==='{'){var j=JSON.parse(o.body);for(k in f)if(!(k in j))j[k]=f[k];o.body=JSON.stringify(j)}
}}catch(e){}return of.apply(this,arguments)};nf.hmSrc=1;window.fetch=nf;
// тильдовские формы шлют XHR (FormData или urlencoded), мобильные иногда обычным submit
var XO=XMLHttpRequest.prototype.open,XS=XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.open=function(m,u){this._hmLead=String(u).indexOf('lead.php')>-1;return XO.apply(this,arguments)};
XMLHttpRequest.prototype.send=function(body){try{if(this._hmLead){var f=fields(),k;
 if(typeof FormData!=='undefined'&&body instanceof FormData){for(k in f)if(!body.has(k))body.append(k,f[k])}
 else if(typeof body==='string'){if(body.charAt(0)==='{'){var j=JSON.parse(body);for(k in f)if(!(k in j))j[k]=f[k];body=JSON.stringify(j)}
  else{for(k in f)if(body.indexOf(encodeURIComponent(k)+'=')<0)body+=(body?'&':'')+encodeURIComponent(k)+'='+encodeURIComponent(f[k])}}
}}catch(e){}return XS.call(this,body)};
document.addEventListener('submit',function(ev){try{var fm=ev.target;if(!fm||!/lead\.php/.test(fm.getAttribute('action')||''))return;
 var f=fields(),k;for(k in f){var i=fm.querySelector('input[type=hidden][name="'+k+'"]');if(!i){i=document.createElement('input');i.type='hidden';i.name=k;fm.appendChild(i)}i.value=f[k]}}catch(e){}},true);
})();</script>"""

BLOCK = f'<!-- {MARK} -->{JS}<!-- /{MARK} -->'
OLD = re.compile(r'<!-- ' + MARK + r' -->.*?<!-- /' + MARK + r' -->', re.S)


def patch(s):
    s2 = OLD.sub('', s)
    # как можно раньше: до любых скриптов форм, сразу после <head ...>
    m = re.search(r'<head[^>]*>', s2, re.I)
    if not m:
        return s, False
    s2 = s2[:m.end()] + BLOCK + s2[m.end():]
    return s2, s2 != s


def main():
    n = 0
    for dirpath, _dirs, files in os.walk(MIRROR):
        for f in files:
            if f not in ('index.html', 'index-a2.html'):
                continue
            p = os.path.join(dirpath, f)
            s = open(p, encoding='utf-8').read()
            if '/api/lead.php' not in s and 'lead.php' not in s and 'hm-cta' not in s and 'mh-f' not in s:
                # страницы без форм (приватные отчёты и т.п.) не трогаем
                if MARK not in s:
                    continue
            new, changed = patch(s)
            if changed:
                open(p, 'w', encoding='utf-8').write(new)
                n += 1
    print(f'add_lead_source: обновлено файлов {n}')


if __name__ == '__main__':
    main()
