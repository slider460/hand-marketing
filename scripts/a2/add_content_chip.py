# Content — ВТОРОЙ чип услуг на ГЛАВНОЙ (Tilda Zero rec226204768), после Exhibition Build.
# Ряд 1 (база/960) становится 5 капсул: Exhibition, Content, Event, Creative, Video —
# пересчитан с сохранением центра сетки; ряд 2 не трогаем. Планшет (640): Content в третий
# ряд к Print и 3D (ряд пересчитан по центру). 480/320 скрыты кастомной мобильной главной.
# Чип = пара текст+капсула (клон Event-пары, hover через data-animate-sbs-trgels).
# Идемпотентен. Правит mirror/index.html и mirror/index-a2.html (+ mh-chip в a2).
import os, re

HERE=os.path.dirname(os.path.abspath(__file__))
MIRROR=os.path.abspath(os.path.join(HERE,'..','..','mirror'))
REC='226204768'
EV_TXT='1599143810215'; EV_PILL='1602343067387'      # чип Event — донор разметки/CSS
NEW_TXT='1751500000040'; NEW_PILL='1751500000041'

# --- новые позиции существующих (только изменяемые брейкпоинты) ---
TEXTS={  # elem-id -> {bp:(top,left%)}
 '1751500000020': {'base':(20,-30),'960':(26,-37)},              # Exhibition
 EV_TXT:          {'base':(20,-4), '960':(26,-5)},               # Event
 '1599144251550': {'base':(20,11), '960':(26,14)},               # Creative & Design
 '1599144319846': {'base':(20,30), '960':(26,37)},               # Video production
 '1599144393830': {'640':(32,-25)},                              # Print (третий ряд планшета)
 '1599144552758': {'640':(32,7)},                                # 3D Mapping
}
PILLS={  # elem-id -> {bp:(top,left px)}
 '1751500000021': {'base':(411,137),'960':(436,31)},             # Exhibition
 EV_PILL:         {'base':(411,505),'960':(436,385)},            # Event
 '1602343207645': {'base':(411,638),'960':(436,511)},            # Creative
 '1602343322196': {'base':(411,866),'960':(436,732)},            # Video
 '1602343349908': {'640':(306,56)},                              # Print
 '1602343417196': {'640':(306,299)},                             # 3D
}
NEW_TXT_G={'base':(20,-15),'960':(26,-18),'640':(32,33),'480':(0,0),'320':(-30,0)}
NEW_PILL_G={'base':(411,363),'960':(436,250),'640':(306,472),'480':(0,-300),'320':(0,-300)}
BP_ORDER=['base','960','640','480','320']

def patch_attrs(tag,geo):
    for bp,tl in geo.items():
        if tl is None: continue
        t,l=tl; suf='' if bp=='base' else f'-res-{bp}'
        tag=re.sub(rf'data-field-top{suf}-value="[-\d.]+"',f'data-field-top{suf}-value="{t}"',tag)
        tag=re.sub(rf'data-field-left{suf}-value="[-\d.]+"',f'data-field-left{suf}-value="{l}"',tag)
    return tag

def set_rule_pos(body,t,l,is_text):
    if is_text:
        body=re.sub(r'top:calc\(([\d.]+px - [\d.]+px) \+ -?[\d.]+px\)',rf'top:calc(\g<1> + {t}px)',body)
    else:
        body=re.sub(r'top:-?[\d.]+px',f'top:{t}px',body)
    body=re.sub(r'left:calc\(50% - ([\d.]+)px \+ -?[\d.]+px\)',rf'left:calc(50% - \g<1>px + {l}px)',body)
    return body

def patch_css(html,eid,geo,is_text):
    pat=re.compile(rf'(#rec{REC} \.tn-elem\[data-elem-id="{eid}"\]{{)([^}}]*)}}')
    hits=[m for m in pat.finditer(html) if 'top:' in m.group(2)]
    assert len(hits)==5, f'{eid}: {len(hits)} positional rules'
    out=[];pos=0
    for m,bp in zip(hits,BP_ORDER):
        body=m.group(2)
        if geo.get(bp): body=set_rule_pos(body,*geo[bp],is_text)
        out.append(html[pos:m.start()]);out.append(m.group(1)+body+'}');pos=m.end()
    out.append(html[pos:])
    return ''.join(out)

def clone_css(html,src_id,new_id,geo,is_text,zindex,new_w=None,new_half=None):
    seg_start=html.index(f'<div id="rec{REC}"')
    css=html[seg_start:html.index('</style>',seg_start)]
    rules=re.findall(rf'(?:@media[^{{]*{{\s*)?#rec{REC} [^{{]*\[data-elem-id="{src_id}"\][^{{]*{{[^}}]*}}(?:\s*}})?',css)
    pos_i=0; out=[]
    for r in rules:
        r=r.replace(src_id,new_id)
        if '.tn-atom' not in r and 'anim-hidden' not in r and 'top:' in r:
            bp=BP_ORDER[pos_i]; pos_i+=1
            t,l=geo[bp]
            r=set_rule_pos(r,t,l,is_text)
            if new_w:   r=re.sub(r'width:[\d.]+px',f'width:{new_w}px',r)
            if new_half:r=re.sub(r'left:calc\(50% - [\d.]+px \+',f'left:calc(50% - {new_half}px +',r)
            r=re.sub(r'z-index:\d+',f'z-index:{zindex}',r)
        out.append(r)
    assert pos_i==5, f'{src_id}: клонировано позиционных правил {pos_i}'
    return ''.join(out)

def process(path,mobile):
    html=open(path,encoding='utf-8').read()
    if NEW_TXT in html:
        print(f'{path}: уже пропатчен, пропуск'); return
    # 1) сдвиги существующих
    for eid,geo in {**TEXTS,**PILLS}.items():
        m=re.search(rf"<div class='t396__elem[^']*' data-elem-id='{eid}'[^>]*>",html)
        assert m, f'{eid} не найден в {path}'
        html=html[:m.start()]+patch_attrs(m.group(0),geo)+html[m.end():]
    for eid,geo in TEXTS.items(): html=patch_css(html,eid,geo,True)
    for eid,geo in PILLS.items(): html=patch_css(html,eid,geo,False)
    # 2) CSS новых элементов (клоны Event-пары)
    new_css=(clone_css(html,EV_PILL,NEW_PILL,NEW_PILL_G,False,32,new_w=112)
            +clone_css(html,EV_TXT,NEW_TXT,NEW_TXT_G,True,33,new_w=90,new_half=45))
    style_end=html.index('</style>',html.index(f'<div id="rec{REC}"'))
    html=html[:style_end]+new_css+html[style_end:]
    # 3) DOM: пара Content перед парой Event (получится второй после Exhibition)
    mp=re.search(rf"<div class='t396__elem[^']*' data-elem-id='{EV_PILL}'[^>]*>",html)
    pill_tag=mp.group(0).replace(EV_PILL,NEW_PILL).replace(f'tn-elem__{REC}{EV_PILL}',f'tn-elem__{REC}{NEW_PILL}')
    pill_tag=re.sub(r'data-field-width-value="[\d.]+"','data-field-width-value="112"',pill_tag)
    pill_tag=re.sub(r'data-field-width-res-640-value="[\d.]+"','data-field-width-res-640-value="112"',pill_tag)
    pill_tag=re.sub(r"data-animate-sbs-trgels=\"\d+\"",f'data-animate-sbs-trgels="{NEW_TXT}"',pill_tag)
    pill=patch_attrs(pill_tag,NEW_PILL_G)+" <div class='tn-atom'> </div> </div>"
    html=html[:mp.start()]+pill+' '+html[mp.start():]
    mt=re.search(rf"<div class='t396__elem[^']*' data-elem-id='{EV_TXT}'[^>]*>",html)
    txt_tag=mt.group(0).replace(EV_TXT,NEW_TXT).replace(f'tn-elem__{REC}{EV_TXT}',f'tn-elem__{REC}{NEW_TXT}')
    txt_tag=re.sub(r'data-field-width-value="[\d.]+"','data-field-width-value="90"',txt_tag)
    txt_tag=re.sub(r'\s*data-field-width-res-640-value="[\d.]+"','',txt_tag)
    txt=patch_attrs(txt_tag,NEW_TXT_G)+' <h2 class=\'tn-atom\'><a href="/content" style="color: inherit">Content</a></h2> </div>'
    html=html[:mt.start()]+txt+' '+html[mt.start():]
    # 4) мобильный чип — вторым (перед Event, т.е. сразу после Exhibition Build)
    if mobile:
        a=html.find('<a class="mh-chip" href="/event"')
        if a>0: html=html[:a]+'<a class="mh-chip" href="/content" style="--c:#E0427E">Content</a>'+html[a:]
    open(path,'w',encoding='utf-8').write(html)
    print(f'{path}: OK')

if __name__=='__main__':
    process(os.path.join(MIRROR,'index.html'),mobile=False)
    process(os.path.join(MIRROR,'index-a2.html'),mobile=True)
