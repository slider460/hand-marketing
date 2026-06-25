import os, json, time, threading, http.server, functools
from playwright.sync_api import sync_playwright
ROOT='/Users/aleksandrnarodetskii/Downloads/hand-marketing-react/mirror'; PORT=8096
cases=json.load(open(os.path.join(os.path.dirname(ROOT),'src/data/cases.json')))
routes=[c['route'].strip('/') for c in cases]
JS=r"""()=>{
  // картинки галереи: bg-image у .t-slds__bgimg / .tn-atom__slds-img, плюс img внутри галереи
  var urls=[];
  document.querySelectorAll('.tn-atom__gallery .t-bgimg, .tn-atom__gallery img, .t-slds__bgimg').forEach(function(e){
    var s=e.getAttribute('data-original')||'';
    if(!s){ var bg=getComputedStyle(e).backgroundImage; var m=bg && bg.match(/url\(["']?([^"')]+)/); if(m)s=m[1]; }
    if(!s && e.tagName==='IMG') s=e.getAttribute('data-original')||e.src||'';
    if(s){ s=s.replace(/^.*?(\/static\/)/,'$1').replace(/^https?:\/\/[^/]+/,''); if(/\.(jpg|jpeg|png|webp)/i.test(s) && urls.indexOf(s)<0) urls.push(s); }
  });
  return urls;
}"""
def main():
    os.chdir(ROOT)
    httpd=http.server.ThreadingHTTPServer(('127.0.0.1',PORT),functools.partial(http.server.SimpleHTTPRequestHandler))
    threading.Thread(target=httpd.serve_forever,daemon=True).start()
    out={}
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(); pg.set_viewport_size({'width':1280,'height':1000})
        for r in routes:
            url=f'http://127.0.0.1:{PORT}/{r}/'
            try: pg.goto(url,wait_until='networkidle',timeout=40000)
            except Exception:
                try: pg.goto(url,wait_until='load',timeout=40000)
                except Exception as e: print('  fail',r); continue
            try: pg.wait_for_selector('.tn-atom__gallery .t-slds, .t-slds__item', timeout=6000)
            except Exception: pass
            time.sleep(0.8)
            try: imgs=pg.evaluate(JS)
            except Exception: imgs=[]
            if imgs: out[r]=imgs
            print(f'  {r}: {len(imgs)} gallery imgs')
        b.close()
    httpd.shutdown()
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'gallery_map.json'),'w'), ensure_ascii=False)
    print('cases with gallery:',len(out))
main()
