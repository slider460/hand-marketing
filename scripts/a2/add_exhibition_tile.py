# Exhibition Build — восьмая плитка ПЕРВОЙ в родной Tilda Zero-сетке услуг (/service, rec228726270).
# Сетка 4+3 -> 4+4: двигает 7 существующих иконок/подписей (data-field-атрибуты движка lib-zero
# И запечённый CSS, все 5 брейкпоинтов), клонирует плитку Event под новую услугу, сдвигает
# stagger-анимацию (+500мс каждой), добавляет карточку в кастомный мобильный список.
# Идемпотентен. Правит mirror/service/index.html (исходник) и index-a2.html (деплой).
import os, re, sys

HERE=os.path.dirname(os.path.abspath(__file__))
MIRROR=os.path.abspath(os.path.join(HERE,'..','..','mirror'))
REC='228726270'
NEW_ICON='1751500000010'; NEW_LABEL='1751500000011'

# --- целевые слоты: (top,left) иконок по брейкпоинтам [base,960,640,480,320] ---
ICON={  # elem-id -> {bp:(top,left)}; сохраняем «фирменные» вертикальные сдвиги каждой иконки
 '1599785693270': {'base':(370,371),'960':(405,280),'640':(391,161),'480':(449,102),'320':(-1,80)},   # Event -> слот 2
 '1599785734369': {'base':(370,670),'960':(405,538),'640':(391,326),'480':(445,207),'320':(2,165)},   # Creative -> 3
 '1599785737665': {'base':(370,970),'960':(405,781),'640':(391,473),'480':(446,330),'320':(-1,245)},  # Video -> 4
 '1599785746128': {'base':(616,74), '960':(651,21), '640':(591,11), '480':(637,-5), '320':(145,1)},   # Print -> 5 (ряд 2)
 '1599785749359': {'base':(616,371),'960':(651,280),'640':(591,161),'480':(636,102),'320':(147,80)},  # BTL -> 6
 '1599785752800': {'base':(616,670),'960':(651,538),'640':(591,326),'480':(637,207),'320':(154,165)}, # Digital -> 7
 '1599785755041': {'base':(614,970),'960':(649,781),'640':(589,473),'480':(634,330),'320':(145,245)}, # 3D -> 8
}
LABEL={ # elem-id -> {bp:(top,offset)}; top/offset — как у Тильды: якорь center, единицы "%"
 '1599786054561': {'base':(6,-13), '960':(7,-13), '640':(5,-13), '480':(12,-12),'320':(-31,-11)},  # Event
 '1599786054569': {'base':(8,12),  '960':(9,14),  '640':(7,13),  '480':(14,9),  '320':(-30,13)},   # Creative
 '1599786054575': {'base':(8,37),  '960':(9,40),  '640':(7,36),  '480':(14,34), '320':(-30,38)},   # Video
 '1599786054582': {'base':(33,-38),'960':(34,-40),'640':(28,-36),'480':(32,-34),'320':(-5,-36)},   # Print
 '1599786054587': {'base':(33,-13),'960':(34,-13),'640':(28,-13),'480':(32,-12),'320':(-6,-11)},   # BTL
 '1599786054592': {'base':(33,12), '960':(34,14), '640':(28,13), '480':(32,9),  '320':(-6,13)},    # Digital
 '1599786054597': {'base':(33,37), '960':(34,40), '640':(28,36), '480':(33,34), '320':(-6,38)},    # 3D
}
# порядок появления (stagger, шаг 500мс): новая плитка dt=0, остальные +500 к прежнему ритму
DT={'1599785693270':500,'1599786054561':500, '1599785734369':1000,'1599786054569':1000,
    '1599785737665':1500,'1599786054575':1500, '1599785746128':2000,'1599786054582':2000,
    '1599785749359':2500,'1599786054587':2500, '1599785752800':3000,'1599786054592':3000,
    '1599785755041':3500,'1599786054597':3500}
BP_ORDER=['base','960','640','480','320']       # порядок CSS-правил: base, @1199, @959, @639, @479
HALF={'base':600,'960':480,'640':320,'480':240,'320':160}  # половина грида в left:calc(50% - Xpx + ...)

EXH_ICON={'base':(370,74),'960':(405,21),'640':(391,11),'480':(449,-5),'320':(-1,1)}
EXH_LABEL={'base':(6,-38),'960':(7,-40),'640':(5,-36),'480':(12,-34),'320':(-31,-36)}

SBS_OPTS=lambda dt:("[{'ti':'0','mx':'0','my':'0','sx':'1','sy':'1','op':'1','ro':'0','bl':'0','ea':'','dt':'0'},"
 "{'ti':0,'mx':'0','my':'0','sx':'1','sy':'1','op':0,'ro':'0','bl':'0','ea':'','dt':'0'},"
 f"{{'ti':1000,'mx':'0','my':'0','sx':'1','sy':'1','op':1,'ro':'0','bl':'0','ea':'','dt':{dt}}}]")

def icon_html():
    g=EXH_ICON
    return (f"<div class='t396__elem tn-elem tn-elem__{REC}{NEW_ICON} t396__elem--anim-hidden' "
     f"data-elem-id='{NEW_ICON}' data-elem-type='shape' "
     f'data-field-top-value="{g["base"][0]}" data-field-left-value="{g["base"][1]}" '
     'data-field-height-value="145" data-field-width-value="157" '
     'data-field-axisy-value="top" data-field-axisx-value="left" data-field-container-value="grid" '
     'data-field-topunits-value="px" data-field-leftunits-value="px" data-field-heightunits-value="px" data-field-widthunits-value="px" '
     'data-animate-sbs-event="blockintoview" data-animate-sbs-trg="1" data-animate-sbs-trgofst="0" '
     f'data-animate-sbs-opts="{SBS_OPTS(0)}" '
     f'data-field-top-res-320-value="{g["320"][0]}" data-field-left-res-320-value="{g["320"][1]}" '
     'data-field-height-res-320-value="83" data-field-width-res-320-value="77" '
     f'data-field-top-res-480-value="{g["480"][0]}" data-field-left-res-480-value="{g["480"][1]}" '
     f'data-field-top-res-640-value="{g["640"][0]}" data-field-left-res-640-value="{g["640"][1]}" '
     f'data-field-top-res-960-value="{g["960"][0]}" data-field-left-res-960-value="{g["960"][1]}"> '
     '<a class=\'tn-atom t-bgimg\' href="/exhibition" data-original="../images/services/exhibition-build.svg" '
     'aria-label=\'Exhibition Build\' role="img"> </a> </div>')

def label_html():
    g=EXH_LABEL
    return (f"<div class='t396__elem tn-elem tn-elem__{REC}{NEW_LABEL} t396__elem--anim-hidden' "
     f"data-elem-id='{NEW_LABEL}' data-elem-type='text' "
     f'data-field-top-value="{g["base"][0]}" data-field-left-value="{g["base"][1]}" data-field-width-value="200" '
     'data-field-axisy-value="center" data-field-axisx-value="center" data-field-container-value="grid" '
     'data-field-topunits-value="%" data-field-leftunits-value="%" data-field-heightunits-value="" data-field-widthunits-value="px" '
     'data-animate-sbs-event="intoview" data-animate-sbs-trg="1" data-animate-sbs-trgofst="0" '
     f'data-animate-sbs-opts="{SBS_OPTS(0)}" data-field-fontsize-value="20" '
     f'data-field-top-res-320-value="{g["320"][0]}" data-field-left-res-320-value="{g["320"][1]}" '
     'data-field-fontsize-res-320-value="12" data-field-width-res-320-value="110" '
     f'data-field-top-res-480-value="{g["480"][0]}" data-field-left-res-480-value="{g["480"][1]}" '
     f'data-field-top-res-640-value="{g["640"][0]}" data-field-left-res-640-value="{g["640"][1]}" '
     f'data-field-top-res-960-value="{g["960"][0]}" data-field-left-res-960-value="{g["960"][1]}"> '
     '<div class=\'tn-atom\'><a href="/exhibition" style="color: inherit">Exhibition Build</a></div> </div>')

MEDIA={'960':'@media screen and (max-width:1199px)','640':'@media screen and (max-width:959px)',
       '480':'@media screen and (max-width:639px)','320':'@media screen and (max-width:479px)'}
ATOM_SHAPE=('background-position:center center;background-size:auto 69%;background-repeat:no-repeat;'
 'border-width:var(--t396-borderwidth,0);border-style:var(--t396-borderstyle,solid);border-color:var(--t396-bordercolor,transparent);'
 'transition:background-color var(--t396-speedhover,0s) ease-in-out,color var(--t396-speedhover,0s) ease-in-out,'
 'border-color var(--t396-speedhover,0s) ease-in-out,box-shadow var(--t396-shadowshoverspeed,0.2s) ease-in-out;')
ATOM_TEXT=("color:#000000;font-size:20px;font-family:'Raleway',Arial,sans-serif;line-height:0.95;font-weight:700;"
 'background-position:center center;border-width:var(--t396-borderwidth,0);border-style:var(--t396-borderstyle,solid);'
 'border-color:var(--t396-bordercolor,transparent);transition:background-color var(--t396-speedhover,0s) ease-in-out,'
 'color var(--t396-speedhover,0s) ease-in-out,border-color var(--t396-speedhover,0s) ease-in-out,'
 'box-shadow var(--t396-shadowshoverspeed,0.2s) ease-in-out;')

def new_css():
    p=f'#rec{REC} .tn-elem[data-elem-id="{NEW_ICON}"]'
    q=f'#rec{REC} .tn-elem[data-elem-id="{NEW_LABEL}"]'
    c=[]
    t,l=EXH_ICON['base']
    c.append(f'{p}{{z-index:16;top:{t}px;;left:calc(50% - 600px + {l}px);;width:157px;height:145px;}}')
    c.append(f'{p} .tn-atom{{{ATOM_SHAPE}}}')
    c.append(f'@media (min-width:1200px){{#rec{REC} .tn-elem.t396__elem--anim-hidden[data-elem-id="{NEW_ICON}"]{{opacity:0;}}}}')
    for bp in ['960','640','480','320']:
        t,l=EXH_ICON[bp]; extra='width:77px;height:83px;' if bp=='320' else ''
        c.append(f'{MEDIA[bp]}{{{p}{{top:{t}px;;left:calc(50% - {HALF[bp]}px + {l}px);;{extra}}}}}')
    t,o=EXH_LABEL['base']
    c.append(f'{q}{{color:#000000;text-align:center;z-index:17;top:calc(470px - 0px + {t}px);;left:calc(50% - 100px + {o}px);;width:200px;height:auto;}}')
    c.append(f'{q} .tn-atom{{{ATOM_TEXT}}}')
    c.append(f'@media (min-width:1200px){{#rec{REC} .tn-elem.t396__elem--anim-hidden[data-elem-id="{NEW_LABEL}"]{{opacity:0;}}}}')
    for bp in ['960','640','480','320']:
        t,o=EXH_LABEL[bp]; w2='55' if bp=='320' else '100'; extra='width:110px;' if bp=='320' else ''
        c.append(f'{MEDIA[bp]}{{{q}{{top:calc(470px - 0px + {t}px);;left:calc(50% - {w2}px + {o}px);;height:auto;{extra}}}}}')
    c.append(f'@media screen and (max-width:479px){{{q} .tn-atom{{font-size:12px;}}}}')
    return ''.join(c)

def patch_attrs(tag,geo):
    for bp,(t,l) in geo.items():
        suf='' if bp=='base' else f'-res-{bp}'
        tag=re.sub(rf'data-field-top{suf}-value="[-\d.]+"',f'data-field-top{suf}-value="{t}"',tag)
        tag=re.sub(rf'data-field-left{suf}-value="[-\d.]+"',f'data-field-left{suf}-value="{l}"',tag)
    return tag

def patch_dt(tag,dt):
    m=list(re.finditer(r"'dt':'?\d+'?",tag))
    if not m: return tag
    last=m[-1]
    return tag[:last.start()]+f"'dt':{dt}"+tag[last.end():]

def patch_css(html,eid,geo,is_label):
    pat=re.compile(rf'(#rec{REC} \.tn-elem\[data-elem-id="{eid}"\]{{)([^}}]*)}}')
    hits=[m for m in pat.finditer(html) if 'top:' in m.group(2)]
    assert len(hits)==5, f'{eid}: {len(hits)} positional rules'
    out=[]; pos=0
    for m,bp in zip(hits,BP_ORDER):
        t,l=geo[bp]; body=m.group(2)
        if is_label:
            body=re.sub(r'top:calc\(470px - 0px \+ -?[\d.]+px\)',f'top:calc(470px - 0px + {t}px)',body)
            body=re.sub(r'left:calc\(50% - ([\d.]+)px \+ -?[\d.]+px\)',rf'left:calc(50% - \g<1>px + {l}px)',body)
        else:
            body=re.sub(r'top:-?[\d.]+px',f'top:{t}px',body)
            body=re.sub(r'left:calc\(50% - ([\d.]+)px \+ -?[\d.]+px\)',rf'left:calc(50% - \g<1>px + {l}px)',body)
        out.append(html[pos:m.start()]); out.append(m.group(1)+body+'}'); pos=m.end()
    out.append(html[pos:])
    return ''.join(out)

MOBILE_CARD=('<a class="mh-scard" href="/exhibition" style="--c:#8E5FB0">'
 '<span class="mh-scard__ghost" aria-hidden="true">E</span><span class="mh-scard__tag">Услуга</span>'
 '<h3 class="mh-scard__t">Exhibition Build</h3><p class="mh-scard__d">Застройка выставочных стендов под ключ</p>'
 '<span class="mh-scard__go" aria-hidden="true"></span></a>')

def process(path,mobile):
    html=open(path).read()
    if NEW_ICON in html:
        print(f'{path}: уже пропатчен, пропуск'); return
    # 1) атрибуты и анимация существующих элементов
    for eid,geo in {**ICON,**LABEL}.items():
        m=re.search(rf"<div class='t396__elem[^']*' data-elem-id='{eid}'[^>]*>",html)
        assert m, f'{eid} не найден в {path}'
        tag=patch_dt(patch_attrs(m.group(0),geo),DT[eid])
        html=html[:m.start()]+tag+html[m.end():]
    # 2) запечённый CSS существующих
    for eid,geo in ICON.items(): html=patch_css(html,eid,geo,False)
    for eid,geo in LABEL.items(): html=patch_css(html,eid,geo,True)
    # 3) новые элементы: CSS в конец style-блока рекорда, DOM — перед иконкой Event
    style_end=html.index('</style>',html.index(f'<div id="rec{REC}"'))
    html=html[:style_end]+new_css()+html[style_end:]
    anchor=html.index(f"<div class='t396__elem tn-elem tn-elem__{REC}1599785693270")
    html=html[:anchor]+icon_html()+' '+label_html()+' '+html[anchor:]
    # 4) мобильная карточка (только в index-a2, где инжектится кастомный мобайл)
    if mobile:
        a=html.find('<a class="mh-scard" href="/event"')
        if a>0: html=html[:a]+MOBILE_CARD+html[a:]
    open(path,'w').write(html)
    print(f'{path}: OK')

if __name__=='__main__':
    process(os.path.join(MIRROR,'service','index.html'),mobile=False)
    process(os.path.join(MIRROR,'service','index-a2.html'),mobile=True)
