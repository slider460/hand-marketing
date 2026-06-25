# Делает белый фон квадратных обложек кейсов прозрачным (заливка от краёв).
# Внутренние белые детали (надписи внутри круга) сохраняются.
import os
from collections import deque
from PIL import Image

ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILES=[
 'mirror/static/cdn/stor3435-6339-4163-a433-646336343434/88889dcf73b126c47c1dec4a187d308a.png',  # mmg
 'mirror/static/cdn/stor3864-3666-4061-a664-313234373466/3c39f9f2139e90b9e968795284629146.png',  # bekobod1
 'mirror/static/cdn/stor6538-6135-4162-a565-653035323933/f16af483ac499f1871910e5ee28eb3e7.png',  # zubovo
 'mirror/static/cdn/stor3039-3238-4836-b039-616562373464/11635b224858f8c0034b3ee15dc4687f.png',  # isotec
]
THR=238  # порог «белого»

def process(path):
    im=Image.open(path).convert('RGBA')
    w,h=im.size
    px=im.load()
    def passable(x,y):  # прозрачный фон ИЛИ белый — по таким распространяем заливку
        r,g,b,a=px[x,y]
        return a==0 or (r>=THR and g>=THR and b>=THR)
    seen=bytearray(w*h)
    dq=deque()
    for x in range(w):
        for y in (0,h-1):
            if passable(x,y) and not seen[y*w+x]:
                seen[y*w+x]=1; dq.append((x,y))
    for y in range(h):
        for x in (0,w-1):
            if passable(x,y) and not seen[y*w+x]:
                seen[y*w+x]=1; dq.append((x,y))
    n=0
    while dq:
        x,y=dq.popleft()
        r,g,b,a=px[x,y]
        if a!=0:  # белый -> прозрачный (прозрачные оставляем как есть)
            px[x,y]=(r,g,b,0); n+=1
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if 0<=nx<w and 0<=ny<h and not seen[ny*w+nx] and passable(nx,ny):
                seen[ny*w+nx]=1; dq.append((nx,ny))
    im.save(path)
    return w,h,n

for f in FILES:
    p=os.path.join(ROOT,f)
    if not os.path.exists(p): print('MISSING',f); continue
    w,h,n=process(p)
    print(f'{os.path.basename(f)}: {w}x{h}, cleared {n} px ({n*100//(w*h)}%)')
