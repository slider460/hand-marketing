import os, re
HERE=os.path.dirname(__file__)
ROOT='/Users/aleksandrnarodetskii/Downloads/hand-marketing-react/mirror'
ANIM='<style>'+open(os.path.join(HERE,'mobile.css')).read()+'</style>\n<script>'+open(os.path.join(HERE,'anim.js')).read()+'\n</script>'
CAROUSEL='<!--MCASES-->'+open(os.path.join(HERE,'cases_carousel.html')).read()+'<!--/MCASES-->'
n=0
for dp,_,fns in os.walk(ROOT):
    if 'index-a2.html' not in fns: continue
    p=os.path.join(dp,'index-a2.html'); h=open(p,encoding='utf-8').read()
    # карусель кейсов — на странице проектов (мобайл): вставляем перед списком стора, убрав прежнюю
    if os.path.basename(dp)=='project':
        h=re.sub(r'<!--MCASES-->.*?<!--/MCASES-->','',h,flags=re.S)  # снять старую (на случай повторного патча)
        m=re.search(r'<div class="[^"]*t-store__card-list', h)
        if m: h=h[:m.start()]+CAROUSEL+h[m.start():]
    i=h.find('<style id="a2-geo">')
    if i<0:  # React-страницы без a2-geo: вставим anim перед </body>, если есть слайдер/стор
        if '</body>' in h and ('t-slds' in h or 't-store__card' in h):
            h=h.replace('</body>', ANIM+'</body>',1); open(p,'w',encoding='utf-8').write(h); n+=1
        continue
    styEnd=h.find('</style>', i)+len('</style>')
    body=h.find('</body>', styEnd)
    new=h[:styEnd]+ANIM+h[body:]
    open(p,'w',encoding='utf-8').write(new); n+=1
print('patched', n, 'pages')
