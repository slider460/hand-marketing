#!/usr/bin/env python3
"""Новые круги-постеры (477×396) для четырёх карточек, которые выбивались из ряда:
стенд Самарской области, стенд Ставрополья, выставка «Самара», обучение Saint-Gobain.

Механика одна на всех, в ключе соседних SG-карточек (v2.2): настоящее фото
под тинтом цвета кейса, имя клиента разрядкой, тёмная таблетка с одной
метрикой, кубики HM по углам. Огромных плашек больше нет.

Картинки, сделанные через NordRouter (tools/nordrouter), лежат в scripts/covers-src/:
- sgt-empty-room-sq.png: общий план переговорной курса (d1-wide), из кадра убраны
  оба актёра (лиц снятых людей на карточке быть не должно) и кадр достроен до
  квадрата (gpt-image-2-edit, два прохода). Кресла остаются в родном цвете;
- stav-cube-cut.png: графика куба, вырезанная из фона (recraft-remove-bg); из неё
  stav-wheat.png, пшеничное «сердце» без остатков рамки. Лежит поверх круга
  и выходит за его верх, как объёмная графика выходила за грани куба.

python3 scripts/gen-covers-stands-sgt.py [--out DIR]   (без --out пишет в mirror)
webp потом через scripts/gen-webp.sh."""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
SRC = os.path.join(HERE, 'covers-src')
LIB = os.path.join(ROOT, 'mirror', 'images', 'lib')
_FONT = os.path.join(HERE, 'fonts', 'Montserrat.ttf')

W, H = 477, 396
CX, CY, R = 238, 196, 176
SS = 4
WHITE = (255, 255, 255)
INK = (16, 20, 30)

# кубики HM с карточки Eaton: вырезаем по связной области цвета, без
# хвостов белого круга и линий, которые попадают в прямоугольный кроп
_E = Image.open(os.path.join(LIB, 'as6135-3563-4735-a365-643234376439', 'icons-112.png')).convert('RGBA')
_BOX = {'green': (19, 14, 81, 77), 'orange': (379, 26, 443, 92),
        'red': (14, 296, 75, 372), 'magenta': (382, 341, 449, 382)}


def _sprite(box, pad=6):
    x0, y0, x1, y1 = box
    crop = _E.crop((x0 - pad, y0 - pad, x1 + pad, y1 + pad))
    px = crop.load()
    keep = Image.new('L', crop.size, 0)
    kp = keep.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b, a = px[x, y]
            if a > 20 and max(r, g, b) - min(r, g, b) > 45:
                kp[x, y] = 255
    keep = keep.filter(ImageFilter.MaxFilter(5))
    crop.putalpha(Image.composite(crop.getchannel('A'), Image.new('L', crop.size, 0), keep))
    return crop


CUBE = {k: _sprite(v) for k, v in _BOX.items()}

METRICS = {
    'samara-vdnh': 'ВЫСТАВКА-ФОРУМ «РОССИЯ»',
    'stavropol-vdnh': '248 ДНЕЙ НА ВДНХ',
    'samara-exhibition': '4 МЕСЯЦА ПОД КЛЮЧ',
}
POP_LADYA = (236, 0, 236)  # x, y, ширина вырезанной ладьи на холсте 477×396


def font(sz, v='ExtraBold'):
    f = ImageFont.truetype(_FONT, sz)
    try:
        f.set_variation_by_name(v)
    except Exception:
        pass
    return f


def square(path, fx=0.5, fy=0.5, zoom=1.0):
    """Квадратный кроп с фокусом (fx, fy) и приближением zoom."""
    im = Image.open(path).convert('RGB')
    side = int(min(im.size) / zoom)
    left = int((im.width - side) * fx)
    top = int((im.height - side) * fy)
    return im.crop((left, top, left + side, top + side))


def tint(im, dark, mid, hi=0.3):
    """Дуотон: тени в dark, средние в mid, свет к белому (как у SG-карточек)."""
    g = ImageOps.autocontrast(im.convert('L'), cutoff=2)
    bands = []
    for c in range(3):
        lut = [max(0, min(255, round(dark[c] + (mid[c] - dark[c]) * (v / 255)
                                     + (255 - mid[c]) * (v / 255) ** 2 * hi))) for v in range(256)]
        bands.append(g.point(lut))
    return Image.merge('RGB', bands)


def spaced(d, cx, y, text, f, color, track):
    ws = [d.textbbox((0, 0), ch, font=f)[2] for ch in text]
    total = sum(ws) + track * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, ws):
        d.text((x, y), ch, font=f, fill=color)
        x += w + track


def pill(d, cx, y, text, fg, S, size=16, maxw=290):
    pf = font(int(size * S))
    while d.textlength(text, font=pf) > maxw * S and size > 12:
        size -= 1
        pf = font(int(size * S))
    tb = d.textbbox((0, 0), text, font=pf)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = int(20 * S), int(13 * S)
    pw, ph = tw + px * 2, th + py * 2
    x = cx - pw // 2
    d.rounded_rectangle([x, y, x + pw, y + ph], radius=ph // 2, fill=INK + (255,))
    d.text((x + px - tb[0], y + py - tb[1]), text, font=pf, fill=fg + (255,))


def cubes(img, spec, S):
    for name, (x, y), scale, flip in spec:
        spr = CUBE[name]
        spr = spr.resize((int(spr.width * scale * S), int(spr.height * scale * S)), Image.LANCZOS)
        if flip:
            spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
        img.alpha_composite(spr, (int(x * S), int(y * S)))


def title_block(img, cx, y, lines, S, size=31, maxw=300):
    """Крупное название в 1-2 строки с мягкой тенью, чтобы читалось на любом фото."""
    f = font(int(size * S), 'Black')
    probe = ImageDraw.Draw(img)
    while max(probe.textlength(ln, font=f) for ln in lines) > maxw * S and size > 20:
        size -= 1
        f = font(int(size * S), 'Black')
    lh = int(size * 1.08 * S)
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    for i, ln in enumerate(lines):
        tw = ds.textlength(ln, font=f)
        ds.text((cx - tw / 2, y + i * lh + 2 * S), ln, font=f, fill=(0, 0, 0, 150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5 * S)))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        d.text((cx - tw / 2, y + i * lh), ln, font=f, fill=WHITE + (255,))


def poster(photo, dark, mid, name, metric, metric_fg, cube_spec, pop=None, hi=0.18, keep=None,
           title=None, mix=1.0, title_y=24, pop_under=False):
    S = SS
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    cx, cy, r = CX * S, CY * S, R * S
    src = photo.resize((2 * r, 2 * r), Image.LANCZOS)
    disc = tint(src, dark, mid, hi).convert('RGBA')
    if mix < 1.0:
        # тон кейса только слоем поверх фото, чтобы картинка читалась
        disc = Image.blend(src.convert('RGBA'), disc, mix)
    if keep is not None:
        # цвет возвращается только там, где keep(r, g, b, y) вернул True
        m = Image.new('L', src.size, 0)
        sp, mp = src.load(), m.load()
        for y in range(src.height):
            for x in range(src.width):
                if keep(*sp[x, y], y / src.height):
                    mp[x, y] = 255
        m = m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(2 * S))
        disc = Image.composite(src.convert('RGBA'), disc, m)
    # затемнение низа круга под имя и таблетку
    col = Image.new('L', (1, 256))
    for y in range(256):
        t = max(0.0, (y / 255 - 0.40) / 0.60)
        col.putpixel((0, y), int((200 if title else 160) * t ** 1.2))
    shade = Image.new('RGBA', (2 * r, 2 * r), dark + (0,))
    shade.putalpha(col.resize((2 * r, 2 * r)))
    disc.alpha_composite(shade)
    mask = Image.new('L', (2 * r, 2 * r), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    img.paste(disc, (cx - r, cy - r), mask)
    cubes(img, cube_spec, S)
    if pop is not None:
        spr, (px, py, pw) = pop
        k = pw * S / spr.width
        spr = spr.resize((int(spr.width * k), int(spr.height * k)), Image.LANCZOS)
        # низ объекта обрезает круг, за край выходит только верх (нос ладьи)
        ox, oy = int(px * S), int(py * S)
        clip = Image.new('L', img.size, 0)
        cd = ImageDraw.Draw(clip)
        cd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
        cd.rectangle([0, 0, img.size[0], cy - int(40 * S)], fill=255)
        clip = clip.filter(ImageFilter.GaussianBlur(1 * S)).crop((ox, oy, ox + spr.width, oy + spr.height))
        spr.putalpha(Image.composite(spr.getchannel('A'), Image.new('L', spr.size, 0), clip))
        a = spr.getchannel('A')
        rgb = spr.copy()  # в родном цвете
        sh = Image.new('RGBA', rgb.size, (0, 0, 0, 0))
        sh.putalpha(a.point(lambda v: int(v * 0.35)))
        sh = sh.filter(ImageFilter.GaussianBlur(6 * S))
        img.alpha_composite(sh, (int(px * S), int(py * S) + 6 * S))
        img.alpha_composite(rgb, (int(px * S), int(py * S)))
    if title:
        title_block(img, cx, cy + int(title_y * S), title, S)
    d = ImageDraw.Draw(img)
    if name:
        spaced(d, cx, cy + int(62 * S), name, font(int(18 * S)), WHITE + (255,), int(3 * S))
    if metric:
        if title:
            pill(d, cx, cy + r - int(74 * S), metric, metric_fg, S, size=18)
        else:
            pill(d, cx, cy + r - int(70 * S), metric, metric_fg, S)
    return img.resize((W, H), Image.LANCZOS)


# раскладки кубиков: у каждой карточки своя
CUBES_A = [('orange', (6, 10), 1.0, True), ('green', (8, 300), 1.0, False),
           ('magenta', (392, 334), 1.0, False)]
CUBES_B = [('green', (4, 40), 1.0, True), ('red', (8, 300), 0.95, False),
           ('orange', (402, 290), 1.0, False)]
CUBES_C = [('magenta', (8, 336), 1.0, True), ('orange', (404, 10), 1.0, False),
           ('red', (406, 290), 0.95, True)]


def build():
    out = {}
    # кадр с паруса на стенде: белый парус с гербом, небо, ладья (присланный кадр лежит
    # в covers-src/ladya-photo.jpg). Через gpt-image-2-edit из него сделаны два слоя:
    # sail-clean.jpg (лодка убрана, парус и небо достроены) и ladya-boat.png
    # (сама ладья). Круг берёт парус, ладья поверх выходит носом за край круга
    boat = os.path.join(SRC, 'ladya-boat.png')
    pop = (Image.open(boat).convert('RGBA'), POP_LADYA) if os.path.exists(boat) else None
    out['custom-samara-vdnh'] = poster(
        Image.open(os.path.join(SRC, 'sail-clean.jpg')).convert('RGB').crop((176, 105, 1143, 1072)),
        dark=(20, 30, 90), mid=(40, 90, 200), name='', title=['СТЕНД САМАРСКОЙ', 'ОБЛАСТИ'],
        metric=METRICS['samara-vdnh'], metric_fg=(120, 190, 255), cube_spec=CUBES_A,
        pop=pop, mix=0.0, title_y=46)
    out['custom-stavropol-vdnh'] = poster(
        square(os.path.join(ROOT, 'mirror', 'images', 'stavropol', 'poster-main.jpg'), 0.5, 0.2),
        dark=(24, 10, 40), mid=(104, 56, 132), name='', title=['СТЕНД', 'СТАВРОПОЛЬЯ'],
        metric=METRICS['stavropol-vdnh'], metric_fg=(206, 160, 255), cube_spec=CUBES_B,
        mix=0.3, title_y=34)
    out['custom-samara-exhibition'] = poster(
        square(os.path.join(ROOT, 'mirror', 'portfolio', 'samara-exhibition', 'photos', 'Ekran_parus.jpg'), 0.28),
        dark=(10, 36, 10), mid=(70, 140, 36), name='', title=['ВЫСТАВКА', '«САМАРА»'],
        metric=METRICS['samara-exhibition'], metric_fg=(150, 230, 90), cube_spec=CUBES_C,
        mix=0.35, title_y=34)
    room = os.path.join(SRC, 'sgt-empty-room-sq.jpg')
    if os.path.exists(room):
        im = Image.open(room).convert('RGB')
        side = im.width
        im = im.crop((0, 0, side, side))

        def chairs(r_, g_, b_, yy):
            # красное и жёлтое кресло: насыщенные тёплые пиксели в нижней половине
            return yy > 0.45 and max(r_, g_, b_) - min(r_, g_, b_) > 90 and r_ > 110 and b_ < 90
        # имя клиента не пишем: знак Saint-Gobain уже висит на стене в кадре
        out['custom-sgtraining'] = poster(
            im, dark=(12, 54, 52), mid=(31, 110, 106), name='',
            metric='9 СЦЕН, 28 ЭКРАНОВ', metric_fg=(244, 108, 84), cube_spec=[], hi=0.45, keep=chairs)
    return out


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--out', help='папка для черновиков; без неё пишет в mirror/images/lib/<slug>/')
    x = a.parse_args()
    for slug, im in build().items():
        if x.out:
            os.makedirs(x.out, exist_ok=True)
            p = os.path.join(x.out, slug + '.png')
        else:
            p = os.path.join(LIB, slug, 'cover-main.png')
        im.save(p)
        print('written', p)
