#!/usr/bin/env python3
"""
Hand Marketing — логотип как 3D-сцена + анимация сборки.

Оригинал (HM_logo.pdf) — не буквы на гранях куба, а КУБ С ВЫРЕЗАМИ:
  • зелёное тело   — куб; в левой грани два кармана (счётчики H),
                     в правой — нижний вырез и верхний V-паз (M);
  • фиолетовый     — вертикальный полуцилиндр в верхнем кармане H;
  • оранжевый      — брусок в нижнем кармане, выступает ниже низа куба;
  • красный        — согнутая V-пластина («галка») в нижнем вырезе M;
  • жёлтый         — сложенная лента-клин поперёк верха; её правый конец
                     отогнут вниз и садится в V-паз M (одно тело, не два).

Камера подогнана по углам куба из оригинала: yaw 45°, pitch 23°, слабая
перспектива, тело чуть приплюснуто по высоте (0.94).

Скрытые поверхности снимаются z-буфером: сортировка граней здесь не работает —
вставки сидят внутри карманов и взаимно пересекаются с телом.

Тайминги анимации взяты со схемы заказчика (освещение omni, без теней):
  жёлтый      — вход 1 сек, затем пауза 1 сек;
  фиолетовый  — 2 сек, оборот 360°;
  оранжевый   — 2 сек подъём с поворотом на 45°;
  красный     — три такта по 1 сек, второй с поворотом на 180°.

Запуск:
  python3 scripts/gen-logo-3d.py           — статичные PNG + сверка с оригиналом
  python3 scripts/gen-logo-3d.py --anim    — плюс анимация сборки (GIF + MP4)
"""

import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image

# ── Камера (подогнана под оригинал, rms 8px из 1000) ─────────────────────────
YAW, PITCH, DIST = math.radians(45), math.radians(23), 20.0
BODY_H = 0.94                      # сжатие тела по вертикали

# ── Геометрия (снята из HM_logo.pdf; ny — высота в долях полувысоты тела) ────
PKT_X = (-0.39, 0.33)              # карманы H по ширине левой грани
PKT_Z = 0.66                       # дно карманов
PKT_TOP_Y = (0.00, 0.97)           # верхний карман H
PKT_BOT_Y = (-1.00, -0.44)         # нижний карман H (открыт вниз)

# нижний вырез M в правой грани, контур (z, ny)
M_NOTCH = [(0.33, -1.02), (0.33, -0.573), (0.226, -0.579),
           (0.229, -0.429), (-0.387, -0.510), (-0.400, -1.02)]
M_NOTCH_X = 0.78                   # глубина выреза

# верхний V-паз M, контур (z, ny), и остриё ленты, которое в него садится.
# Остриё чуть шире паза и выступает на 0.004 — иначе грани z-конфликтуют
# и по краю проступает зелёная стенка.
M_VEE = [(0.41, 1.00), (0.00, 0.44), (-0.41, 1.00)]
M_VEE_X = 0.62
TIP = [(0.43, 1.006), (0.00, 0.44), (-0.43, 1.006)]

# Полуцилиндр: плоский срез — вертикальная плоскость x = CYL_X (нормаль +x),
# хорда идёт вдоль z, выпуклость уходит влево (-x). Так замеряется и оригинал:
# след сечения 0.30 × 0.57 = R × 2R.
CYL_X, CYL_Z, CYL_R = -0.05, 0.86, 0.34
CYL_Y = (0.27, 0.97)

BOX_X, BOX_Y, BOX_Z = (-0.35, 0.29), (-1.26, -0.53), (0.62, 1.04)

# красная «галка», сечение (z, ny), выдавлено по x
CHEVRON = [(-0.175, -0.476), (0.241, -0.003), (0.229, -0.718),
           (-0.193, -1.185), (-0.589, -0.686), (-0.567, 0.004)]
CHEVRON_X = (0.78, 1.04)

# Жёлтая лента: клин с ребром вдоль x, лежит на верхней грани и доходит до
# правой грани (x = 1), где переходит в отогнутое остриё в V-пазу.
# Сечение в (ny, z): задний скат пологий и яркий, передний — крутой.
# Низ ленты чуть выше плоскости верхней грани, иначе грани z-конфликтуют.
BAR_X = (-1.25, 1.00)
BAR_SECTION = [(1.005, -0.43), (1.09, 0.26), (1.005, 0.43)]

# ── Палитра: точные цвета из оригинала, по три тона на материал ──────────────
# (верх, лицо +z, бок +x)
MAT_GREEN  = ((0xC6, 0xD2, 0x00), (0x92, 0xC0, 0x1F), (0x5F, 0x93, 0x2F))
MAT_YELLOW = ((0xFF, 0xEB, 0x00), (0xFC, 0xC4, 0x00), (0xE2, 0x96, 0x00))
MAT_PURPLE = ((0x93, 0x1B, 0x80), (0x79, 0x20, 0x81), (0x52, 0x1F, 0x75))
MAT_ORANGE = ((0xDE, 0x63, 0x11), (0xF6, 0xA4, 0x00), (0xC7, 0x4D, 0x1B))
MAT_RED    = ((0xE9, 0x50, 0x45), (0xE2, 0x05, 0x20), (0xB9, 0x1E, 0x1E))
# внутренности вырезов — тон затенённой грани, как в оригинале
MAT_POCKET = ((0x6E, 0xA6, 0x33), (0x5F, 0x93, 0x2F), (0x4B, 0x75, 0x25))

DARK = 0.55        # грани, отвёрнутые от света (-x, -y, -z)

TRIS = []          # (v0, v1, v2, материал, множитель)


# ── Примитивы ────────────────────────────────────────────────────────────────
def tri(a, b, c, mat, k=1.0):
    TRIS.append((a, b, c, mat, k))


def quad(a, b, c, d, mat, k=1.0):
    tri(a, b, c, mat, k)
    tri(a, c, d, mat, k)


def face(poly, mat, k=1.0):
    """Многоугольник, в т.ч. невыпуклый: триангуляция отсечением ушей."""
    poly = list(poly)
    if len(poly) < 3:
        return
    if len(poly) == 3:
        tri(*poly, mat, k)
        return
    n = np.cross(np.subtract(poly[1], poly[0]), np.subtract(poly[2], poly[0]))
    drop = int(np.argmax(np.abs(n)))
    ax = [i for i in range(3) if i != drop]
    flat = [(p[ax[0]], p[ax[1]]) for p in poly]
    area = sum(flat[i][0] * flat[(i + 1) % len(flat)][1] -
               flat[(i + 1) % len(flat)][0] * flat[i][1] for i in range(len(flat)))
    if area < 0:
        poly.reverse(); flat.reverse()

    def cross2(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    idx = list(range(len(poly)))
    guard = 0
    while len(idx) > 3 and guard < 4 * len(poly):
        guard += 1
        for i in range(len(idx)):
            a, b, c = idx[i - 1], idx[i], idx[(i + 1) % len(idx)]
            if cross2(flat[a], flat[b], flat[c]) <= 0:
                continue
            if any(j not in (a, b, c) and
                   cross2(flat[a], flat[b], flat[j]) >= 0 and
                   cross2(flat[b], flat[c], flat[j]) >= 0 and
                   cross2(flat[c], flat[a], flat[j]) >= 0 for j in idx):
                continue
            tri(poly[a], poly[b], poly[c], mat, k)
            idx.pop(i)
            break
        else:
            break
    if len(idx) == 3:
        tri(poly[idx[0]], poly[idx[1]], poly[idx[2]], mat, k)


def prism(poly, lo, hi, mat, k=1.0):
    """Призма: контур poly задан парами (y, z) и выдавлен по x от lo до hi."""
    lo_f = [(lo, p[0], p[1]) for p in poly]
    hi_f = [(hi, p[0], p[1]) for p in poly]
    face(lo_f[::-1], mat, k)
    face(hi_f, mat, k)
    for i in range(len(poly)):
        j = (i + 1) % len(poly)
        quad(lo_f[i], lo_f[j], hi_f[j], hi_f[i], mat, k)


def box(xr, yr, zr, mat, k=1.0):
    x0, x1 = xr; y0, y1 = yr; z0, z1 = zr
    for poly in ([(x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)],
                 [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
                 [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
                 [(x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0)],
                 [(x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1)],
                 [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)]):
        face(poly, mat, k)


# ── Элементы ─────────────────────────────────────────────────────────────────
def green_body():
    m, k = MAT_GREEN, 1.0
    px0, px1 = PKT_X

    # Левая грань (+z): «H» — стойки, перемычка и рамки над/под карманами
    for xr, yr in [((-1, px0), (-1, 1)), ((px1, 1), (-1, 1)),
                   ((px0, px1), (PKT_BOT_Y[1], PKT_TOP_Y[0])),
                   ((px0, px1), (PKT_TOP_Y[1], 1)), ((px0, px1), (-1, PKT_BOT_Y[0]))]:
        if yr[1] - yr[0] > 1e-4:
            quad((xr[0], yr[0], 1), (xr[1], yr[0], 1), (xr[1], yr[1], 1), (xr[0], yr[1], 1), m, k)

    # Карманы H: дно и четыре стенки
    for (ya, yb) in (PKT_TOP_Y, PKT_BOT_Y):
        quad((px0, ya, PKT_Z), (px1, ya, PKT_Z), (px1, yb, PKT_Z), (px0, yb, PKT_Z), MAT_POCKET)
        quad((px0, ya, PKT_Z), (px0, yb, PKT_Z), (px0, yb, 1), (px0, ya, 1), MAT_POCKET)
        quad((px1, ya, 1), (px1, yb, 1), (px1, yb, PKT_Z), (px1, ya, PKT_Z), MAT_POCKET)
        for yc in (ya, yb):
            quad((px0, yc, PKT_Z), (px1, yc, PKT_Z), (px1, yc, 1), (px0, yc, 1), MAT_POCKET)

    # Правая грань (+x): прямоугольник минус нижний вырез и верхний V-паз
    for zr, yr in [((-1, M_NOTCH[-1][0]), (-1, 1)),
                   ((M_NOTCH[0][0], 1), (-1, 1)),
                   ((M_NOTCH[-1][0], M_NOTCH[0][0]), (M_NOTCH[3][1], 1))]:
        quad((1, yr[0], zr[0]), (1, yr[0], zr[1]), (1, yr[1], zr[1]), (1, yr[1], zr[0]), m, k)
    quad((1, M_NOTCH[1][1], M_NOTCH[0][0]), (1, M_NOTCH[1][1], M_NOTCH[2][0]),
         (1, M_NOTCH[3][1], M_NOTCH[2][0]), (1, M_NOTCH[3][1], M_NOTCH[0][0]), m, k)

    for i in range(len(M_NOTCH) - 1):                       # стенки нижнего выреза
        (z0, y0v), (z1v, y1v) = M_NOTCH[i], M_NOTCH[i + 1]
        quad((1, y0v, z0), (1, y1v, z1v), (M_NOTCH_X, y1v, z1v), (M_NOTCH_X, y0v, z0), MAT_POCKET)
    quad((M_NOTCH_X, -1, M_NOTCH[-1][0]), (M_NOTCH_X, -1, M_NOTCH[0][0]),
         (M_NOTCH_X, M_NOTCH[3][1], M_NOTCH[0][0]), (M_NOTCH_X, M_NOTCH[3][1], M_NOTCH[-1][0]),
         MAT_POCKET)

    for i in range(len(M_VEE) - 1):                         # стенки V-паза
        (z0, y0v), (z1v, y1v) = M_VEE[i], M_VEE[i + 1]
        quad((1, y0v, z0), (1, y1v, z1v), (M_VEE_X, y1v, z1v), (M_VEE_X, y0v, z0), MAT_POCKET)

    quad((-1, 1, 1), (1, 1, 1), (1, 1, -1), (-1, 1, -1), m, k)          # верх
    quad((-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1), m, DARK)   # низ
    quad((-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1), m, DARK)   # задние
    quad((1, -1, -1), (-1, -1, -1), (-1, 1, -1), (1, 1, -1), m, DARK)


def purple_cylinder():
    """Полуцилиндр с вертикальной осью: плоский срез вправо, выпуклость влево."""
    y0, y1 = CYL_Y
    N = 48
    arc = [(CYL_X - CYL_R * math.sin(math.pi * i / N),
            CYL_Z - CYL_R * math.cos(math.pi * i / N)) for i in range(N + 1)]
    for i in range(N):
        (xa, za), (xb, zb) = arc[i], arc[i + 1]
        quad((xa, y0, za), (xb, y0, zb), (xb, y1, zb), (xa, y1, za), MAT_PURPLE)
    quad((CYL_X, y0, arc[0][1]), (CYL_X, y0, arc[-1][1]),
         (CYL_X, y1, arc[-1][1]), (CYL_X, y1, arc[0][1]), MAT_PURPLE)
    face([(x, y1, z) for x, z in arc], MAT_PURPLE)
    face([(x, y0, z) for x, z in arc], MAT_PURPLE, DARK)


def orange_box():
    box(BOX_X, BOX_Y, BOX_Z, MAT_ORANGE)


def red_chevron():
    prism([(ny, z) for z, ny in CHEVRON], CHEVRON_X[0], CHEVRON_X[1], MAT_RED)


def yellow_ribbon():
    """Единая лента: клин по верхней грани + отогнутое вниз остриё в V-пазу."""
    prism(BAR_SECTION, BAR_X[0], BAR_X[1], MAT_YELLOW)
    prism([(ny, z) for z, ny in TIP], M_VEE_X, BAR_X[1] + 0.004, MAT_YELLOW)


# ── Трансформации элементов (для анимации) ───────────────────────────────────
def emit(builder, move=(0.0, 0.0, 0.0), spin=0.0, pivot=(0.0, 0.0)):
    """Строит элемент, затем поворачивает его вокруг вертикали и сдвигает."""
    start = len(TRIS)
    builder()
    if move == (0.0, 0.0, 0.0) and abs(spin) < 1e-9:
        return
    s, c = math.sin(spin), math.cos(spin)
    px, pz = pivot

    def xf(p):
        dx, dz = p[0] - px, p[2] - pz
        return (px + dx * c + dz * s + move[0],
                p[1] + move[1],
                pz - dx * s + dz * c + move[2])

    for i in range(start, len(TRIS)):
        a, b, c3, mat, k = TRIS[i]
        TRIS[i] = (xf(a), xf(b), xf(c3), mat, k)


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def seg(t, t0, t1):
    """Доля прохождения такта [t0, t1] со сглаживанием."""
    return ease((t - t0) / (t1 - t0)) if t1 > t0 else 1.0


# ── Раскадровка по схеме ─────────────────────────────────────────────────────
T_IN, T_HOLD, T_END = 0.35, 1.00, 7.0


def build_scene(t=None):
    """t=None — собранный логотип; иначе состояние сцены на момент t (сек)."""
    TRIS.clear()
    green_body()

    if t is None:
        emit(purple_cylinder); emit(orange_box); emit(red_chevron); emit(yellow_ribbon)
        return

    # фиолетовый: 2 сек, оборот 360°, вход из передне-левого угла
    p = seg(t, T_IN, T_IN + 2.0)
    emit(purple_cylinder,
         move=(-0.42 * (1 - p), 0.05 * (1 - p), 0.80 * (1 - p)),
         spin=2 * math.pi * (1 - p), pivot=(CYL_X, CYL_Z))

    # оранжевый: 2 сек, подъём снизу с поворотом на 45°
    p = seg(t, T_IN, T_IN + 2.0)
    emit(orange_box,
         move=(0.0, -1.55 * (1 - p), 0.0),
         spin=math.radians(45) * (1 - p),
         pivot=(sum(BOX_X) / 2, sum(BOX_Z) / 2))

    # красный: три такта по 1 сек — подлёт, разворот на 180°, посадка снизу
    t0 = T_IN + 1.85
    piv = (sum(CHEVRON_X) / 2, sum(z for z, _ in CHEVRON) / len(CHEVRON))
    if t < t0:
        mv, sp = (1.65, -1.00, 0.0), math.pi
    elif t < t0 + 1.0:                                   # 1) подлёт
        mv, sp = (1.65 - 0.95 * seg(t, t0, t0 + 1.0), -1.00, 0.0), math.pi
    elif t < t0 + 2.0:                                   # 2) разворот 180°
        mv, sp = (0.70, -1.00, 0.0), math.pi * (1 - seg(t, t0 + 1.0, t0 + 2.0))
    else:                                                # 3) посадка
        p = seg(t, t0 + 2.0, t0 + 3.0)
        mv, sp = (0.70 * (1 - p), -1.00 * (1 - p), 0.0), 0.0
    emit(red_chevron, move=mv, spin=sp, pivot=piv)

    # жёлтый: вход 1 сек сверху, затем пауза 1 сек до конца ролика.
    # Стартовая высота такая, чтобы до своего такта лента была целиком за
    # кадром — иначе сверху всё время торчит её остриё.
    t0 = T_END - T_HOLD - 1.0
    emit(yellow_ribbon, move=(0.0, 2.85 * (1 - seg(t, t0, t0 + 1.0)), 0.0))


# ── Камера и затенение ───────────────────────────────────────────────────────
CAM = np.array([DIST * math.sin(YAW) * math.cos(PITCH),
                DIST * math.sin(PITCH),
                DIST * math.cos(YAW) * math.cos(PITCH)])
FWD = -CAM / np.linalg.norm(CAM)
RIGHT = np.array([-FWD[2], 0.0, FWD[0]]); RIGHT /= np.linalg.norm(RIGHT)
UP = np.cross(RIGHT, FWD)


def project(v):
    p = np.array([v[0], v[1] * BODY_H, v[2]]) - CAM
    vz = p @ FWD
    return np.array([(p @ RIGHT) / vz, -(p @ UP) / vz, vz])


def shade(mat, n, k):
    top, front, side = (np.array(c, float) for c in mat)
    wt, wf, ws = max(0.0, n[1]), max(0.0, n[2]), max(0.0, n[0])
    wb = max(0.0, -n[1]) + max(0.0, -n[2]) + max(0.0, -n[0])
    num = wt * top + wf * front + ws * side + wb * (front * DARK)
    return np.clip(num / max(1e-6, wt + wf + ws + wb) * k, 0, 255)


def prepare():
    out = []
    for a, b, c, mat, k in TRIS:
        A, B, C = np.array(a, float), np.array(b, float), np.array(c, float)
        n = np.cross(B - A, C - A)
        ln = np.linalg.norm(n)
        if ln < 1e-12:
            continue
        n = n / ln
        n = np.array([n[0], n[1] / BODY_H, n[2]]); n /= np.linalg.norm(n)
        cen = (A + B + C) / 3
        # Нелицевые НЕ отсекаем — их отбросит z-буфер. Нормаль для затенения
        # разворачиваем к камере: у замкнутого тела это внешняя нормаль,
        # и результат перестаёт зависеть от порядка обхода вершин.
        if n @ (CAM - np.array([cen[0], cen[1] * BODY_H, cen[2]])) < 0:
            n = -n
        out.append(([project(v) for v in (a, b, c)], shade(mat, n, k)))
    return out


def fit_for(prepared, size, pad):
    pts = np.array([p[:2] for tr, _ in prepared for p in tr])
    minx, maxx = pts[:, 0].min(), pts[:, 0].max()
    miny, maxy = pts[:, 1].min(), pts[:, 1].max()
    scale = (size - 2 * pad) / max(maxx - minx, maxy - miny)
    return (scale,
            (size - (maxx - minx) * scale) / 2 - minx * scale,
            (size - (maxy - miny) * scale) / 2 - miny * scale)


def raster(prepared, size, ss, fit):
    """Растеризация z-буфером. fit = (масштаб, смещение x, смещение y)."""
    W = size * ss
    scale, offx, offy = fit
    zbuf = np.full((W, W), np.inf)
    rgb = np.zeros((W, W, 3), np.float32)
    alpha = np.zeros((W, W), np.float32)
    for trp, color in prepared:
        sx = np.array([p[0] * scale * ss + offx * ss for p in trp])
        sy = np.array([p[1] * scale * ss + offy * ss for p in trp])
        sz = np.array([p[2] for p in trp])
        x0, x1 = max(0, int(sx.min())), min(W - 1, int(sx.max()) + 1)
        y0, y1 = max(0, int(sy.min())), min(W - 1, int(sy.max()) + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1 + 1, x0:x1 + 1]
        px, py = xx + 0.5, yy + 0.5
        d = ((sy[1] - sy[2]) * (sx[0] - sx[2]) + (sx[2] - sx[1]) * (sy[0] - sy[2]))
        if abs(d) < 1e-9:
            continue
        w0 = ((sy[1] - sy[2]) * (px - sx[2]) + (sx[2] - sx[1]) * (py - sy[2])) / d
        w1 = ((sy[2] - sy[0]) * (px - sx[2]) + (sx[0] - sx[2]) * (py - sy[2])) / d
        w2 = 1.0 - w0 - w1
        inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not inside.any():
            continue
        z = w0 * sz[0] + w1 * sz[1] + w2 * sz[2]
        sub = zbuf[y0:y1 + 1, x0:x1 + 1]
        win = inside & (z < sub)
        sub[win] = z[win]
        rgb[y0:y1 + 1, x0:x1 + 1][win] = color
        alpha[y0:y1 + 1, x0:x1 + 1][win] = 255.0
    img = Image.fromarray(np.dstack([rgb, alpha[..., None]]).astype(np.uint8))
    return img.resize((size, size), Image.LANCZOS)


OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logo-3d")
os.makedirs(OUT, exist_ok=True)

# ── Статичный логотип ────────────────────────────────────────────────────────
SIZE, SS, PAD = 1024, 3, 24
build_scene(None)
final = prepare()
png = raster(final, SIZE, SS, fit_for(final, SIZE, PAD))
png.save(os.path.join(OUT, "logo-3d.png"))
for sz in (512, 256, 128):
    png.resize((sz, sz), Image.LANCZOS).save(os.path.join(OUT, f"logo-3d-{sz}.png"))

PW, PH, HALF = 1400, 520, 700
sheet = Image.new("RGB", (PW, PH), (0xF6, 0xF6, 0xF4))
sheet.paste((0x14, 0x16, 0x16), (HALF, 0, PW, PH))
for x, sz in [(40, 380), (460, 140), (630, 64)]:
    th = png.resize((sz, sz), Image.LANCZOS)
    y = (PH - sz) // 2
    sheet.paste(th, (x, y), th)
    sheet.paste(th, (x + HALF, y), th)
sheet.save(os.path.join(OUT, "preview.png"))
print(f"треугольников: {len(TRIS)}")

ref_path = os.path.join(OUT, "reference.png")
if os.path.exists(ref_path):
    ref = Image.open(ref_path).convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS)
    cmp_sheet = Image.new("RGB", (SIZE * 3, SIZE), (255, 255, 255))
    cmp_sheet.paste(ref, (0, 0), ref)
    cmp_sheet.paste(png, (SIZE, 0), png)
    cmp_sheet.paste(Image.blend(ref.convert("RGB"), png.convert("RGB"), 0.5), (SIZE * 2, 0))
    cmp_sheet.resize((SIZE * 3 // 2, SIZE // 2), Image.LANCZOS).save(
        os.path.join(OUT, "compare.png"))

# ── Анимация сборки ──────────────────────────────────────────────────────────
if "--anim" in sys.argv:
    A_SIZE, A_SS, FPS = 512, 2, 25
    # кадр фиксируем по собранному состоянию с запасом — иначе логотип «прыгает»
    a_fit = fit_for(final, A_SIZE, 96)
    n = int(T_END * FPS)
    frames = []
    for i in range(n):
        build_scene(i / FPS)
        f = raster(prepare(), A_SIZE, A_SS, a_fit)
        bg = Image.new("RGB", f.size, (255, 255, 255))
        bg.paste(f, (0, 0), f)
        frames.append(bg)
        if (i + 1) % 25 == 0:
            print(f"  кадр {i + 1}/{n}")

    gif = os.path.join(OUT, "assembly.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:],
                   duration=int(1000 / FPS), loop=0, optimize=True)

    raw = os.path.join(OUT, "_frames.raw")
    with open(raw, "wb") as fh:
        for f in frames:
            fh.write(f.tobytes())
    mp4 = os.path.join(OUT, "assembly.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{A_SIZE}x{A_SIZE}", "-r", str(FPS), "-i", raw,
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", mp4],
        check=True)
    os.remove(raw)
    print(f"анимация: {gif}\n           {mp4}  ({n} кадров, {T_END} сек)")

print("готово:", os.path.join(OUT, "logo-3d.png"))
