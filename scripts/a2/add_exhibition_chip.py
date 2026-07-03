# Exhibition Build — первый чип услуг на ГЛАВНОЙ (Tilda Zero rec226204768).
# Чип = ПАРА элементов: текст-ссылка (якорь center, %-отступы) + капсула-shape (px, hover
# завязан на id текста через data-animate-sbs-trgels). Ряды: база/960 — 4+4 (было 4+3),
# 640 (планшет 640-959) — 3 ряда. 480/320 не трогаем (Тильда там скрыта кастомной мобильной
# главной mhome). Идемпотентен. Правит mirror/index.html и mirror/index-a2.html (+ mh-chip в a2).
import os, re

HERE=os.path.dirname(os.path.abspath(__file__))
MIRROR=os.path.abspath(os.path.join(HERE,'..','..','mirror'))
REC='226204768'
EV_TXT='1599143810215'; EV_PILL='1602343067387'      # чип Event — донор разметки/CSS
NEW_TXT='1751500000020'; NEW_PILL='1751500000021'

TEXTS={  # elem-id -> {bp:(top,left)} в % сетки (только видимые брейкпоинты)
 EV_TXT:          {'base':(20,-10),'960':(26,-12),'640':(7,7)},    # Event
 '1599144251550': {'base':(20,6),  '960':(26,7),  '640':(20,-27)}, # Creative & Design
 '1599144319846': {'base':(20,25), '960':(26,30), '640':(20,8)},   # Video production
 '1599144393830': {'base':(31,-19),'960':(38,-21),'640':(32,-14)}, # Print & Production
 '1599144494280': {'base':(31,-3), '960':(38,-3), '640':(7,25)},   # BTL
 '1599144524102': {'base':(31,9),  '960':(38,9),  '640':(20,34)},  # Digital
 '1599144552758': {'base':(31,22), '960':(38,24), '640':(32,19)},  # 3D Mapping
}
PILLS={  # elem-id -> {bp:(top,left)} в px сетки
 EV_PILL:         {'base':(411,428),'960':(436,313),'640':(204,329)}, # Event
 '1602343207645': {'base':(411,573),'960':(436,448),'640':(256,49)},  # Creative
 '1602343322196': {'base':(411,801),'960':(436,669),'640':(256,272)}, # Video
 '1602343349908': {'base':(478,271),'960':(507,177),'640':(306,129)}, # Print (ряд 1 -> 2)
 '1602343381397': {'base':(478,511),'960':(507,409),'640':(204,427)}, # BTL
 '1602343401676': {'base':(478,658),'960':(507,520),'640':(256,491)}, # Digital
 '1602343417196': {'base':(478,798),'960':(507,640),'640':(306,372)}, # 3D
}
NEW_TXT_G={'base':(20,-25),'960':(26,-30),'640':(7,-18),'480':(0,0),'320':(-30,0)}
NEW_PILL_G={'base':(411,202),'960':(436,94),'640':(204,107),'480':(0,-300),'320':(0,-300)}
BP_ORDER=['base','960','640','480','320']

def patch_attrs(tag,geo):
    for bp,tl in geo.items():
        if tl is None: continue
        t,l=tl; suf='' if bp=='base' else f'-res-{bp}'
        tag=re.sub(rf'data-field-top{suf}-value="[-\d.]+"',f'data-field-top{suf}-value="{t}"',tag)
        tag=re.sub(rf'data-field-left{suf}-value="[-\d.]+"',f'data-field-left{suf}-value="{l}"',tag)
    return tag

def set_rule_pos(body,t,l,is_text):
    if is_text:  # top:calc(310px - 8.5px + T px)
        body=re.sub(r'top:calc\(([\d.]+px - [\d.]+px) \+ -?[\d.]+px\)',rf'top:calc(\g<1> + {t}px)',body)
    else:        # top:T px
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
    """все CSS-правила элемента-донора -> правила нового элемента."""
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
    # 1) сдвигаем существующие тексты и капсулы (атрибуты движка + запечённый CSS)
    for eid,geo in {**TEXTS,**PILLS}.items():
        m=re.search(rf"<div class='t396__elem[^']*' data-elem-id='{eid}'[^>]*>",html)
        assert m, f'{eid} не найден в {path}'
        html=html[:m.start()]+patch_attrs(m.group(0),geo)+html[m.end():]
    for eid,geo in TEXTS.items(): html=patch_css(html,eid,geo,True)
    for eid,geo in PILLS.items(): html=patch_css(html,eid,geo,False)
    # 2) CSS новых элементов (клоны Event-пары)
    new_css=(clone_css(html,EV_PILL,NEW_PILL,NEW_PILL_G,False,30,new_w=196)
            +clone_css(html,EV_TXT,NEW_TXT,NEW_TXT_G,True,31,new_w=160,new_half=80))
    style_end=html.index('</style>',html.index(f'<div id="rec{REC}"'))
    html=html[:style_end]+new_css+html[style_end:]
    # 3) DOM: новая капсула перед капсулой Event, новый текст перед текстом Event
    mp=re.search(rf"<div class='t396__elem[^']*' data-elem-id='{EV_PILL}'[^>]*>",html)
    pill_tag=mp.group(0).replace(EV_PILL,NEW_PILL).replace(f'tn-elem__{REC}{EV_PILL}',f'tn-elem__{REC}{NEW_PILL}')
    pill_tag=re.sub(r'data-field-width-value="[\d.]+"','data-field-width-value="196"',pill_tag)
    pill_tag=re.sub(r'data-field-width-res-640-value="[\d.]+"','data-field-width-res-640-value="196"',pill_tag)
    pill_tag=re.sub(r"data-animate-sbs-trgels=\"\d+\"",f'data-animate-sbs-trgels="{NEW_TXT}"',pill_tag)
    pill=patch_attrs(pill_tag,NEW_PILL_G)+" <div class='tn-atom'> </div> </div>"
    html=html[:mp.start()]+pill+' '+html[mp.start():]
    mt=re.search(rf"<div class='t396__elem[^']*' data-elem-id='{EV_TXT}'[^>]*>",html)
    txt_tag=mt.group(0).replace(EV_TXT,NEW_TXT).replace(f'tn-elem__{REC}{EV_TXT}',f'tn-elem__{REC}{NEW_TXT}')
    txt_tag=re.sub(r'data-field-width-value="[\d.]+"','data-field-width-value="160"',txt_tag)
    txt_tag=re.sub(r'\s*data-field-width-res-640-value="[\d.]+"','',txt_tag)
    txt=patch_attrs(txt_tag,NEW_TXT_G)+' <h2 class=\'tn-atom\'><a href="/exhibition" style="color: inherit">Exhibition Build</a></h2> </div>'
    html=html[:mt.start()]+txt+' '+html[mt.start():]
    # 4) мобильный чип (кастомная мобильная главная, только в index-a2)
    if mobile:
        a=html.find('<a class="mh-chip" href="/event"')
        if a>0: html=html[:a]+'<a class="mh-chip" href="/exhibition" style="--c:#8E5FB0">Exhibition Build</a>'+html[a:]
    open(path,'w',encoding='utf-8').write(html)
    print(f'{path}: OK')

if __name__=='__main__':
    process(os.path.join(MIRROR,'index.html'),mobile=False)
    process(os.path.join(MIRROR,'index-a2.html'),mobile=True)
