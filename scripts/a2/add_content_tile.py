# Content — девятая плитка ВТОРОЙ в родной Tilda Zero-сетке услуг (/service, rec228726270).
# Сетка 4+4 -> 4+4+1 (третий ряд): Content в слот 2, Event..Digital сдвигаются на слот вправо,
# 3D Mapping уходит в третий ряд. Высота артборда растёт (940->1186 и т.д. по брейкпоинтам),
# поэтому %-координаты ВСЕХ подписей пересчитываются под новые высоты по формуле движка
# lib-zero (проверена замером): center_px = H/2 + v/100*H; подписи визуально не двигаются.
# Иконки — px-координаты, на высоту не завязаны. Идемпотентен.
# Правит mirror/service/index.html и index-a2.html (+ mh-scard в кастомном мобильном списке a2).
import os, re

HERE=os.path.dirname(os.path.abspath(__file__))
MIRROR=os.path.abspath(os.path.join(HERE,'..','..','mirror'))
REC='228726270'
NEW_ICON='1751500000030'; NEW_LABEL='1751500000031'
EXH_ICON_ID='1751500000010'; EXH_LABEL_ID='1751500000011'

BPS=['base','960','640','480','320']
H_OLD={'base':940,'960':940,'640':940,'480':940,'320':520}
H_NEW={'base':1186,'960':1186,'640':1140,'480':1128,'320':666}
HALF={'base':600,'960':480,'640':320,'480':240,'320':160}
ROW_D={'base':246,'960':246,'640':200,'480':188,'320':146}   # шаг ряда по иконкам

# --- слоты иконок: (top,left) px по брейкпоинтам ---
SLOT_ICON={
 2:{'base':(370,371),'960':(405,280),'640':(391,161),'480':(449,102),'320':(-1,80)},
 3:{'base':(370,670),'960':(405,538),'640':(391,326),'480':(445,207),'320':(2,165)},
 4:{'base':(370,970),'960':(405,781),'640':(391,473),'480':(446,330),'320':(-1,245)},
 5:{'base':(616,74), '960':(651,21), '640':(591,11), '480':(637,-5), '320':(145,1)},
 6:{'base':(616,371),'960':(651,280),'640':(591,161),'480':(636,102),'320':(147,80)},
 7:{'base':(616,670),'960':(651,538),'640':(591,326),'480':(637,207),'320':(154,165)},
 8:{'base':(614,970),'960':(649,781),'640':(589,473),'480':(634,330),'320':(145,245)},
 9:{'base':(862,74), '960':(897,21), '640':(791,11), '480':(825,-5), '320':(291,1)},
}
# --- слоты подписей: (v-старой-высоты, left%) ---
SLOT_LABEL={
 1:{'base':(6,-38),'960':(7,-40),'640':(5,-36),'480':(12,-34),'320':(-31,-36)},
 2:{'base':(6,-13),'960':(7,-13),'640':(5,-13),'480':(12,-12),'320':(-31,-11)},
 3:{'base':(8,12), '960':(9,14), '640':(7,13), '480':(14,9),  '320':(-30,13)},
 4:{'base':(8,37), '960':(9,40), '640':(7,36), '480':(14,34), '320':(-30,38)},
 5:{'base':(33,-38),'960':(34,-40),'640':(28,-36),'480':(32,-34),'320':(-5,-36)},
 6:{'base':(33,-13),'960':(34,-13),'640':(28,-13),'480':(32,-12),'320':(-6,-11)},
 7:{'base':(33,12), '960':(34,14), '640':(28,13), '480':(32,9), '320':(-6,13)},
 8:{'base':(33,37), '960':(34,40), '640':(28,36), '480':(33,34),'320':(-6,38)},
}

def center_px(v,bp): return H_OLD[bp]/2 + v/100.0*H_OLD[bp]
# ВАЖНО: движок lib-zero парсит %-значения через parseInt — пишем только целые.
# Округляем вверх (ceil): подпись может сдвинуться только ВНИЗ от иконки (до ~12px),
# но никогда не наедет на неё.
import math
def v_new_from_center(c,bp): return math.ceil((c-H_NEW[bp]/2)/H_NEW[bp]*100)
def v_new(v,bp): return v_new_from_center(center_px(v,bp),bp)
# слот 9 (третий ряд): центр = центр слота 5 + шаг ряда
SLOT_LABEL[9]={bp:(v_new_from_center(center_px(SLOT_LABEL[5][bp][0],bp)+ROW_D[bp],bp),
               SLOT_LABEL[5][bp][1]) for bp in BPS}
# у слота 9 значение уже в НОВЫХ единицах; для остальных пересчитаем на месте
def label_geo_new(slot):
    g={}
    for bp in BPS:
        v,l=SLOT_LABEL[slot][bp]
        g[bp]=((v if slot==9 else v_new(v,bp)),l)
    return g

# --- распределение: элемент -> слот ---
ICON_SLOT={EXH_ICON_ID:None,  # остаётся в слоте 1, top/left не меняются
 '1599785693270':3,  # Event
 '1599785734369':4,  # Creative
 '1599785737665':5,  # Video
 '1599785746128':6,  # Print
 '1599785749359':7,  # BTL
 '1599785752800':8,  # Digital
 '1599785755041':9,  # 3D
}
LABEL_SLOT={EXH_LABEL_ID:1,
 '1599786054561':3,'1599786054569':4,'1599786054575':5,'1599786054582':6,
 '1599786054587':7,'1599786054592':8,'1599786054597':9}
# stagger: пары иконка+подпись, порядок слотов
DT={EXH_ICON_ID:0,EXH_LABEL_ID:0,
 '1599785693270':1000,'1599786054561':1000,
 '1599785734369':1500,'1599786054569':1500,
 '1599785737665':2000,'1599786054575':2000,
 '1599785746128':2500,'1599786054582':2500,
 '1599785749359':3000,'1599786054587':3000,
 '1599785752800':3500,'1599786054592':3500,
 '1599785755041':4000,'1599786054597':4000}

MEDIA={'960':'@media screen and (max-width:1199px)','640':'@media screen and (max-width:959px)',
       '480':'@media screen and (max-width:639px)','320':'@media screen and (max-width:479px)'}
SBS_OPTS=lambda dt:("[{'ti':'0','mx':'0','my':'0','sx':'1','sy':'1','op':'1','ro':'0','bl':'0','ea':'','dt':'0'},"
 "{'ti':0,'mx':'0','my':'0','sx':'1','sy':'1','op':0,'ro':'0','bl':'0','ea':'','dt':'0'},"
 f"{{'ti':1000,'mx':'0','my':'0','sx':'1','sy':'1','op':1,'ro':'0','bl':'0','ea':'','dt':{dt}}}]")
ATOM_SHAPE=('background-position:center center;background-size:auto 69%;background-repeat:no-repeat;'
 'border-width:var(--t396-borderwidth,0);border-style:var(--t396-borderstyle,solid);border-color:var(--t396-bordercolor,transparent);'
 'transition:background-color var(--t396-speedhover,0s) ease-in-out,color var(--t396-speedhover,0s) ease-in-out,'
 'border-color var(--t396-speedhover,0s) ease-in-out,box-shadow var(--t396-shadowshoverspeed,0.2s) ease-in-out;')
ATOM_TEXT=("color:#000000;font-size:20px;font-family:'Raleway',Arial,sans-serif;line-height:0.95;font-weight:700;"
 'background-position:center center;border-width:var(--t396-borderwidth,0);border-style:var(--t396-borderstyle,solid);'
 'border-color:var(--t396-bordercolor,transparent);transition:background-color var(--t396-speedhover,0s) ease-in-out,'
 'color var(--t396-speedhover,0s) ease-in-out,border-color var(--t396-speedhover,0s) ease-in-out,'
 'box-shadow var(--t396-shadowshoverspeed,0.2s) ease-in-out;')

CT_ICON=SLOT_ICON[2]; CT_LABEL=label_geo_new(2)

def icon_html():
    g=CT_ICON
    return (f"<div class='t396__elem tn-elem tn-elem__{REC}{NEW_ICON} t396__elem--anim-hidden' "
     f"data-elem-id='{NEW_ICON}' data-elem-type='shape' "
     f'data-field-top-value="{g["base"][0]}" data-field-left-value="{g["base"][1]}" '
     'data-field-height-value="145" data-field-width-value="157" '
     'data-field-axisy-value="top" data-field-axisx-value="left" data-field-container-value="grid" '
     'data-field-topunits-value="px" data-field-leftunits-value="px" data-field-heightunits-value="px" data-field-widthunits-value="px" '
     'data-animate-sbs-event="blockintoview" data-animate-sbs-trg="1" data-animate-sbs-trgofst="0" '
     f'data-animate-sbs-opts="{SBS_OPTS(500)}" '
     f'data-field-top-res-320-value="{g["320"][0]}" data-field-left-res-320-value="{g["320"][1]}" '
     'data-field-height-res-320-value="83" data-field-width-res-320-value="77" '
     f'data-field-top-res-480-value="{g["480"][0]}" data-field-left-res-480-value="{g["480"][1]}" '
     f'data-field-top-res-640-value="{g["640"][0]}" data-field-left-res-640-value="{g["640"][1]}" '
     f'data-field-top-res-960-value="{g["960"][0]}" data-field-left-res-960-value="{g["960"][1]}"> '
     '<a class=\'tn-atom t-bgimg\' href="/content" data-original="../images/services/content.svg" '
     'aria-label=\'Content\' role="img"> </a> </div>')

def label_html():
    g=CT_LABEL
    return (f"<div class='t396__elem tn-elem tn-elem__{REC}{NEW_LABEL} t396__elem--anim-hidden' "
     f"data-elem-id='{NEW_LABEL}' data-elem-type='text' "
     f'data-field-top-value="{g["base"][0]}" data-field-left-value="{g["base"][1]}" data-field-width-value="200" '
     'data-field-axisy-value="center" data-field-axisx-value="center" data-field-container-value="grid" '
     'data-field-topunits-value="%" data-field-leftunits-value="%" data-field-heightunits-value="" data-field-widthunits-value="px" '
     'data-animate-sbs-event="intoview" data-animate-sbs-trg="1" data-animate-sbs-trgofst="0" '
     f'data-animate-sbs-opts="{SBS_OPTS(500)}" data-field-fontsize-value="20" '
     f'data-field-top-res-320-value="{g["320"][0]}" data-field-left-res-320-value="{g["320"][1]}" '
     'data-field-fontsize-res-320-value="12" data-field-width-res-320-value="110" '
     f'data-field-top-res-480-value="{g["480"][0]}" data-field-left-res-480-value="{g["480"][1]}" '
     f'data-field-top-res-640-value="{g["640"][0]}" data-field-left-res-640-value="{g["640"][1]}" '
     f'data-field-top-res-960-value="{g["960"][0]}" data-field-left-res-960-value="{g["960"][1]}"> '
     '<div class=\'tn-atom\'><a href="/content" style="color: inherit">Content</a></div> </div>')

def new_css():
    p=f'#rec{REC} .tn-elem[data-elem-id="{NEW_ICON}"]'
    q=f'#rec{REC} .tn-elem[data-elem-id="{NEW_LABEL}"]'
    c=[]
    t,l=CT_ICON['base']
    c.append(f'{p}{{z-index:18;top:{t}px;;left:calc(50% - 600px + {l}px);;width:157px;height:145px;}}')
    c.append(f'{p} .tn-atom{{{ATOM_SHAPE}}}')
    c.append(f'@media (min-width:1200px){{#rec{REC} .tn-elem.t396__elem--anim-hidden[data-elem-id="{NEW_ICON}"]{{opacity:0;}}}}')
    for bp in ['960','640','480','320']:
        t,l=CT_ICON[bp]; extra='width:77px;height:83px;' if bp=='320' else ''
        c.append(f'{MEDIA[bp]}{{{p}{{top:{t}px;;left:calc(50% - {HALF[bp]}px + {l}px);;{extra}}}}}')
    t,o=CT_LABEL['base']
    c.append(f'{q}{{color:#000000;text-align:center;z-index:19;top:calc(470px - 0px + {t}px);;left:calc(50% - 100px + {o}px);;width:200px;height:auto;}}')
    c.append(f'{q} .tn-atom{{{ATOM_TEXT}}}')
    c.append(f'@media (min-width:1200px){{#rec{REC} .tn-elem.t396__elem--anim-hidden[data-elem-id="{NEW_LABEL}"]{{opacity:0;}}}}')
    for bp in ['960','640','480','320']:
        t,o=CT_LABEL[bp]; w2='55' if bp=='320' else '100'; extra='width:110px;' if bp=='320' else ''
        c.append(f'{MEDIA[bp]}{{{q}{{top:calc(470px - 0px + {t}px);;left:calc(50% - {w2}px + {o}px);;height:auto;{extra}}}}}')
    c.append(f'@media screen and (max-width:479px){{{q} .tn-atom{{font-size:12px;}}}}')
    return ''.join(c)

def patch_attrs(tag,geo):
    for bp,(t,l) in geo.items():
        suf='' if bp=='base' else f'-res-{bp}'
        tag=re.sub(rf'data-field-top{suf}-value="[-\d.]+"',f'data-field-top{suf}-value="{t}"',tag)
        tag=re.sub(rf'data-field-left{suf}-value="[-\d.]+"',f'data-field-left{suf}-value="{l}"',tag)
    return tag

def patch_attrs_top_only(tag,geo):
    for bp,(t,_l) in geo.items():
        suf='' if bp=='base' else f'-res-{bp}'
        tag=re.sub(rf'data-field-top{suf}-value="[-\d.]+"',f'data-field-top{suf}-value="{t}"',tag)
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
    for m,bp in zip(hits,BPS):
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

def patch_artboard(html):
    # data-атрибуты артборда
    m=re.search(rf'<div class="t396__artboard[^>]*data-artboard-recid="{REC}"[^>]*>',html)
    assert m, 'артборд не найден'
    tag=m.group(0)
    tag=re.sub(r'data-artboard-height="\d+"',f'data-artboard-height="{H_NEW["base"]}"',tag)
    tag=re.sub(r'data-artboard-height-res-960="\d+"',f'data-artboard-height-res-960="{H_NEW["960"]}"',tag)
    tag=re.sub(r'data-artboard-height-res-320="\d+"',f'data-artboard-height-res-320="{H_NEW["320"]}"',tag)
    if 'data-artboard-height-res-640' not in tag:
        tag=tag.replace('data-artboard-height-res-960',f'data-artboard-height-res-640="{H_NEW["640"]}" data-artboard-height-res-960',1)
    if 'data-artboard-height-res-480' not in tag:
        tag=tag.replace('data-artboard-height-res-640',f'data-artboard-height-res-480="{H_NEW["480"]}" data-artboard-height-res-640',1)
    html=html[:m.start()]+tag+html[m.end():]
    # запечённый CSS высот
    html=html.replace(f'#rec{REC} .t396__artboard {{height:940px;',
                      f'#rec{REC} .t396__artboard {{height:{H_NEW["base"]}px;',1)
    html=re.sub(rf'(@media screen and \(max-width:1199px\) {{#rec{REC} \.t396__artboard,#rec{REC} \.t396__filter,#rec{REC} \.t396__carrier {{)height:940px;',
                rf'\g<1>height:{H_NEW["960"]}px;',html,count=1)
    html=re.sub(rf'(@media screen and \(max-width:959px\) {{#rec{REC} \.t396__artboard,#rec{REC} \.t396__filter,#rec{REC} \.t396__carrier {{)',
                rf'\g<1>height:{H_NEW["640"]}px;',html,count=1)
    html=re.sub(rf'(@media screen and \(max-width:639px\) {{#rec{REC} \.t396__artboard,#rec{REC} \.t396__filter,#rec{REC} \.t396__carrier {{)',
                rf'\g<1>height:{H_NEW["480"]}px;',html,count=1)
    html=re.sub(rf'(@media screen and \(max-width:479px\) {{#rec{REC} \.t396__artboard,#rec{REC} \.t396__filter,#rec{REC} \.t396__carrier {{)height:520px;',
                rf'\g<1>height:{H_NEW["320"]}px;',html,count=1)
    return html

MOBILE_CARD=('<a class="mh-scard" href="/content" style="--c:#E0427E">'
 '<span class="mh-scard__ghost" aria-hidden="true">C</span><span class="mh-scard__tag">Услуга</span>'
 '<h3 class="mh-scard__t">Content</h3><p class="mh-scard__d">Мультимедийный контент: графика, мэппинг, VR</p>'
 '<span class="mh-scard__go" aria-hidden="true"></span></a>')

def process(path,mobile):
    html=open(path,encoding='utf-8').read()
    if NEW_ICON in html:
        print(f'{path}: уже пропатчен, пропуск'); return
    html=patch_artboard(html)
    # 1) иконки: атрибуты + dt
    for eid,slot in ICON_SLOT.items():
        m=re.search(rf"<div class='t396__elem[^']*' data-elem-id='{eid}'[^>]*>",html)
        assert m, f'{eid} не найден в {path}'
        tag=m.group(0)
        if slot: tag=patch_attrs(tag,SLOT_ICON[slot])
        tag=patch_dt(tag,DT[eid])
        html=html[:m.start()]+tag+html[m.end():]
    # 2) подписи: атрибуты (v пересчитан под новые высоты) + dt
    for eid,slot in LABEL_SLOT.items():
        m=re.search(rf"<div class='t396__elem[^']*' data-elem-id='{eid}'[^>]*>",html)
        assert m, f'{eid} не найден в {path}'
        tag=patch_attrs(m.group(0),label_geo_new(slot))
        tag=patch_dt(tag,DT[eid])
        html=html[:m.start()]+tag+html[m.end():]
    # 3) запечённый CSS
    for eid,slot in ICON_SLOT.items():
        if slot: html=patch_css(html,eid,SLOT_ICON[slot],False)
    for eid,slot in LABEL_SLOT.items():
        html=patch_css(html,eid,label_geo_new(slot),True)
    # 4) новые элементы Content: CSS в конец style-блока рекорда, DOM — перед иконкой Event
    style_end=html.index('</style>',html.index(f'<div id="rec{REC}"'))
    html=html[:style_end]+new_css()+html[style_end:]
    anchor=html.index(f"<div class='t396__elem tn-elem tn-elem__{REC}1599785693270")
    html=html[:anchor]+icon_html()+' '+label_html()+' '+html[anchor:]
    # 5) мобильная карточка — второй, после Exhibition Build
    if mobile:
        a=html.find('<a class="mh-scard" href="/event"')
        if a>0: html=html[:a]+MOBILE_CARD+html[a:]
    open(path,'w',encoding='utf-8').write(html)
    print(f'{path}: OK')

if __name__=='__main__':
    process(os.path.join(MIRROR,'service','index.html'),mobile=False)
    process(os.path.join(MIRROR,'service','index-a2.html'),mobile=True)
