#!/usr/bin/env python3
# Заставка по ТЗ: сборка куба HM из деталей, покадровый рендер 25fps
# Собственный растеризатор SVG (плоские полигоны + безье), суперсэмплинг 3x
import math, os, re, sys
from PIL import Image, ImageDraw, ImageFont

SC = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(SC, "intro_frames")
os.makedirs(FRAMES, exist_ok=True)
FPS = 25
DUR = 8.2115  # 9 битов
N = round(DUR * FPS)  # 205

# ── парсинг SVG ──
svg_src = open("/Users/aleksandrnarodetskii/Downloads/hand-marketing-react/public/brand/logo_header.svg").read()
pat = re.compile(r'<(path|polygon|polyline|rect)\b([^>]*?)/?>', re.S)
elems = [(m.group(1), m.group(2)) for m in pat.finditer(svg_src)]
assert len(elems) == 22

COLORS = {"cls-2":"#9c2c40","cls-3":"#629535","cls-4":"#a75c21","cls-5":"#c7d306",
          "cls-6":"#96c223","cls-8":"#629435","cls-9":"#c2981a","cls-10":"#ffdf2e",
          "cls-11":"#e1b905","cls-12":"#e8413b","cls-13":"#bb3b42","cls-14":"#cf6f19",
          "cls-15":"#f39306","cls-16":"#95388d","cls-18":"#4a2d6f","cls-19":"#673a7e"}

NUM = re.compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?')

def parse_path(d):
    """M/L/H/V/C/A/Z -> список точек (кубики флэттеним, дуги — хордами)"""
    tok = re.findall(r'[MmLlHhVvCcAaZz]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', d)
    pts, i, cx, cy = [], 0, 0.0, 0.0
    cmd = None
    while i < len(tok):
        t = tok[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd in "Zz": pts.append(pts[0]); continue
        rel = cmd.islower()
        c = cmd.upper()
        if c == "M":
            x, y = float(tok[i]), float(tok[i+1]); i += 2
            if rel: x += cx; y += cy
            cx, cy = x, y; pts.append((x, y)); cmd = "l" if rel else "L"
        elif c == "L":
            x, y = float(tok[i]), float(tok[i+1]); i += 2
            if rel: x += cx; y += cy
            cx, cy = x, y; pts.append((x, y))
        elif c == "H":
            x = float(tok[i]); i += 1
            if rel: x += cx
            cx = x; pts.append((cx, cy))
        elif c == "V":
            y = float(tok[i]); i += 1
            if rel: y += cy
            cy = y; pts.append((cx, cy))
        elif c == "C":
            x1,y1,x2,y2,x,y = (float(tok[i+k]) for k in range(6)); i += 6
            if rel: x1+=cx;y1+=cy;x2+=cx;y2+=cy;x+=cx;y+=cy
            for k in range(1, 13):
                u = k/12
                mt = 1-u
                bx = mt**3*cx + 3*mt*mt*u*x1 + 3*mt*u*u*x2 + u**3*x
                by = mt**3*cy + 3*mt*mt*u*y1 + 3*mt*u*u*y2 + u**3*y
                pts.append((bx, by))
            cx, cy = x, y
        elif c == "A":  # большие радиусы -> хорда
            x, y = float(tok[i+5]), float(tok[i+6]); i += 7
            if rel: x += cx; y += cy
            cx, cy = x, y; pts.append((x, y))
        else:
            i += 1
    return pts

def elem_points(tag, attrs):
    if tag in ("polygon", "polyline"):
        nums = [float(v) for v in NUM.findall(re.search(r'points="([^"]+)"', attrs).group(1))]
        return list(zip(nums[::2], nums[1::2]))
    if tag == "path":
        return parse_path(re.search(r'\bd="([^"]+)"', attrs).group(1))
    if tag == "rect":  # градиентный rect -> форма клипа (path 0)
        return parse_path(re.search(r'\bd="([^"]+)"', elems[0][1]).group(1))
    return []

GEOM = []  # (points, color) в исходных координатах
for tag, attrs in elems:
    cls = re.search(r'class="(cls-\d+)"', attrs).group(1)
    if cls == "cls-1": GEOM.append(None); continue
    GEOM.append((elem_points(tag, attrs), COLORS[cls]))

# порядок отрисовки (z-order фикс: 1 за 11, 3 перед 17)
ORDER = [2,4,5,6,7, 8,9,10,11, 1,12,13,14, 15,16, 3,17, 18, 19,20,21]
GROUP_OF = {}
for g, idxs in {"body":[2,4,5,6,7,16,18], "lid":[8,9,10,11],
                "red":[1,12,13,14], "orange":[3,15,17],
                "purple":[19,20,21]}.items():
    for i in idxs: GROUP_OF[i] = g

CENTERS = {"lid":(176,60), "red":(285,255), "orange":(105,300), "purple":(55,115)}

def ease(u):
    u = max(0.0, min(1.0, u))
    return u*u*(3-2*u)

def lerp(a, b, u): return a+(b-a)*u

def transforms(t):
    tr = {"body": (0,0,1)}
    # ФИОЛЕТОВАЯ: 0.3-2.3, слева + 360°
    u = (t-0.3)/2.0
    if u < 1:
        tr["purple"] = (lerp(-175,0,ease(u)), 0, math.cos(2*math.pi*max(u,0)))
    else:
        tr["purple"] = (0,0,1)
    # ОРАНЖЕВАЯ: 0.3-2.3, снизу + 45°
    u = (t-0.3)/2.0
    if u < 1:
        tr["orange"] = (0, lerp(160,0,ease(u)), lerp(math.cos(math.pi/4),1.0,ease(u)))
    else:
        tr["orange"] = (0,0,1)
    # КРАСНАЯ: 1.3 подлёт | 2.3 разворот 180° | 3.3 стыковка | 4.3 готово
    if t < 1.3:   tr["red"] = (150, 85, -1)
    elif t < 2.3:
        ue = ease(t-1.3); tr["red"] = (lerp(150,58,ue), lerp(85,33,ue), -1)
    elif t < 3.3: tr["red"] = (58, 33, -math.cos(math.pi*(t-2.3)))
    elif t < 4.3:
        ue = ease(t-3.3); tr["red"] = (lerp(58,0,ue), lerp(33,0,ue), 1)
    else:         tr["red"] = (0,0,1)
    # КРЫШКА: пауза | 3.3 проход вправо | 4.3 спуск | 5.3 пауза
    if t < 3.3:   tr["lid"] = (-95, -155, 1)
    elif t < 4.3: tr["lid"] = (lerp(-95,0,ease(t-3.3)), -155, 1)
    elif t < 5.3: tr["lid"] = (0, lerp(-155,0,ease(t-4.3)), 1)
    else:         tr["lid"] = (0,0,1)
    return tr

# ── геометрия кадра ──
W, H = 1280, 720
SS = 3                     # суперсэмплинг
LOGO_H, LOGO_Y = 280, 115
SCALE = LOGO_H / 357.43
OX = W/2 - 352.68/2*SCALE  # svg x=0 в px
OY = LOGO_Y

F_XB = ImageFont.truetype(os.path.join(SC, "fonts/montserrat-latin-800.ttf"), 60)
F_SB = ImageFont.truetype(os.path.join(SC, "fonts/montserrat-600.ttf"), 26)

def spaced(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking

def spaced_w(draw, text, font, tracking):
    return sum(draw.textlength(c, font=font) for c in text) + tracking*(len(text)-1)

def alpha_mix(c, a):
    return tuple(round(255+(v-255)*a) for v in c)

def render_frame(i, out_path):
    t = i / FPS
    tr = transforms(t)
    big = Image.new("RGB", (W*SS, H*SS), (255,255,255))
    d = ImageDraw.Draw(big)
    for idx in ORDER:
        pts, color = GEOM[idx]
        g = GROUP_OF[idx]
        tx, ty, sx = tr[g]
        cx, cy = CENTERS.get(g, (0,0))
        out = []
        for x, y in pts:
            if g != "body":
                x = (x-cx)*sx + cx + tx
                y = y + ty
            out.append(((OX + x*SCALE)*SS, (OY + y*SCALE)*SS))
        if len(out) >= 3 and abs(sx) > 0.02:
            d.polygon(out, fill=color)
    img = big.resize((W, H), Image.LANCZOS)
    dd = ImageDraw.Draw(img)
    a1 = ease((t-5.5)/0.7)
    a2 = ease((t-5.9)/0.7)
    if a1 > 0:
        t1 = "HAND MARKETING"
        w1 = spaced_w(dd, t1, F_XB, 21)
        spaced(dd, ((W-w1)/2, H*0.60+(1-a1)*18), t1, F_XB, alpha_mix((26,26,26), a1), 21)
    if a2 > 0:
        t2 = "рекламное агентство полного цикла"
        w2 = spaced_w(dd, t2, F_SB, 5)
        spaced(dd, ((W-w2)/2, H*0.72+(1-a2)*14), t2, F_SB, alpha_mix((140,140,140), a2), 5)
    z = 1.0 + 0.045*(t/DUR)
    cw, ch = round(W/z), round(H/z)
    img = img.crop(((W-cw)//2, (H-ch)//2, (W+cw)//2, (H+ch)//2)).resize((W,H), Image.LANCZOS)
    img.save(out_path, quality=95)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "poses":
        for t in (0.0, 0.9, 1.6, 2.1, 2.8, 3.8, 4.8, 5.1, 6.6):
            render_frame(round(t*FPS), os.path.join(SC, f"pose_{t:.1f}.jpg"))
            print("pose", t)
    else:
        for i in range(N):
            render_frame(i, os.path.join(FRAMES, f"f{i:04d}.jpg"))
            if i % 50 == 0: print("frame", i, "/", N)
        print("DONE", N)
