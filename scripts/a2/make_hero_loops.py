#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Немые лупы для баннеров новых страниц услуг (дизайн-система hm_ds).

    python3 scripts/a2/make_hero_loops.py            # все
    python3 scripts/a2/make_hero_loops.py ny conf    # выборочно

Кладёт в mirror/videos/<имя>-hero-loop.mp4: 1280×576 (20:9, как баннер), 25 к/с, без звука,
x264 crf 28 + faststart, ~2 МБ. Лежат внутри mirror/**, поэтому уезжают обычным деплоем,
ручная заливка в /media не нужна. Каждый кусок обрезается под кадр баннера:
crop=(ширина, высота, x, y) в долях исходника; без crop берётся центр 20:9.
Плашки «10 лет», логотипы в углах и чёрные поля срезаются увеличенным кропом.
Исходники: локальные media/ (симлинк mirror/media) и mirror/videos/.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'mirror', 'videos')
W, H, SEG = 1280, 576, 2.5

M, V = 'media', 'mirror/videos'
LETTERBOX = (0.74,)          # чёрные поля сверху и снизу
LOGO = (0.72,)               # логотип в углу кадра
LOGO_BIG = (0.66,)           # плашка «10 лет» в правом верхнем углу
LOGO_LOW = (1.0, 0.66, 0.0, 0.1)  # логотипы Eaton и HM по нижнему краю

LOOPS = {
    # Новый год Samsung: сцена, ёлка, «50 лет», маски, сброс сетки, зал по дуге
    'ny': [(f'{M}/samsung-2020.mp4', t, LETTERBOX) for t in (31, 49, 73.5, 79.5, 84.5, 120.5)],
    # партнёрская конференция Eaton в Алматы: зал, доклад, вопросы из зала
    'conf': [(f'{M}/eaton-almaty.mp4', t, LOGO_LOW) for t in (32, 46, 50.5, 64.5, 78, 86.5)],
    # мультимедиа на стендах: Ставрополье (анаморфный куб) и Самара (парус, кинетика)
    'mm': [(f'{M}/stavropol-vdnh-nakedeye.mp4', t, None) for t in (31, 96, 132)]
          + [(f'{M}/samara-vdnh-hero-loop.mp4', t, None) for t in (0.3, 3, 5.6)],
    # дизайн стенда: 3D-визуализация двух вариантов проекта Самарской области
    'design': [(f'{M}/samara-pres-vizual-1.mp4', t, None) for t in (1, 12, 20)]
              + [(f'{M}/samara-pres-vizual-2.mp4', t, None) for t in (5, 22, 42)],
    # цены: все направления, нарезка из шоурила
    'price': [(f'{M}/hm-showreel.mp4', t, LOGO) for t in (8, 13, 35, 40, 83, 94)],
    # команда за работой: площадки «Газели-трансформера» и VIVAX, монтаж сцены Samsung
    'team': [(f'{V}/gaz-backstage.mp4', 4, None), (f'{V}/gaz-backstage.mp4', 26, None),
             (f'{V}/vivax-bts-pads.mp4', 3, (1.0, 0.5, 0.0, 0.24)),
             (f'{M}/samsung-2020.mp4', 7, LETTERBOX), (f'{M}/samsung-2020.mp4', 13, LETTERBOX),
             (f'{M}/samsung-2020.mp4', 19, LETTERBOX)],
    # отзывы: проекты тех, кто писал письма (Saint-Gobain, Eaton, «Саларис», ЦМ РЖД)
    'reviews': [(f'{M}/sg-cx-part1.mp4', 61, LOGO), (f'{M}/sg-cx-part1.mp4', 252, LOGO),
                (f'{M}/eaton-almaty.mp4', 78, LOGO_LOW), (f'{M}/salaris-event-fin180416.mp4', 77, LOGO),
                (f'{M}/transrzhd.mp4', 200, LOGO_BIG), (f'{M}/salaris-event-fin180416.mp4', 126, LOGO)],
}


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                          'stream=width,height', '-of', 'csv=p=0', path],
                         capture_output=True, text=True, check=True).stdout.strip()
    w, h = out.split(',')[:2]
    return int(w), int(h)


def crop_expr(path, crop):
    sw, sh = probe(path)
    if crop and len(crop) == 4:                       # явная рамка в долях: w, h, x, y
        cw, ch, x, y = crop
        cw, ch = sw * cw, sh * ch
        # подгоняем к 20:9 по меньшей стороне
        if cw / ch > W / H:
            cw = ch * W / H
        else:
            ch = cw * H / W
        x, y = min(sw - cw, sw * x + (sw * crop[0] - cw) / 2), min(sh - ch, sh * y)
    else:
        k = crop[0] if crop else 1.0                  # доля высоты, центр
        ch = sh * k
        cw = ch * W / H
        if cw > sw:
            cw = sw
            ch = cw * H / W
        x, y = (sw - cw) / 2, (sh - ch) / 2
    return f'crop={int(cw)}:{int(ch)}:{int(x)}:{int(y)},scale={W}:{H}:flags=lanczos,setsar=1,fps=25'


# брендбук: готового ролика нет, листаем полосы брендбука Metra с медленным наездом,
# по одной на каждый бренд экосистемы (обложка, Metra TG, Metra, Pro, Robotics, Polis)
SHEETS = [f'mirror/images/metra/sheet/{n}.jpg' for n in ('01', '15', '29', '39', '54', '68')]


def build_sheets(name='brandbook'):
    frames = int(SEG * 25)
    args, chains = ['ffmpeg', '-v', 'error', '-y'], []
    for i, src in enumerate(SHEETS):
        args += ['-loop', '1', '-t', str(SEG), '-i', os.path.join(ROOT, src)]
        # кадр 20:9 из полосы 2:1, наезд 1.0 → 1.07 к центру за 2,5 с
        chains.append(f'[{i}:v]scale=2560:-2,crop=2560:1152,zoompan=z=\'1+0.07*on/{frames}\':'
                      f'x=\'iw/2-iw/zoom/2\':y=\'ih/2-ih/zoom/2\':d=1:s={W}x{H}:fps=25,setsar=1,'
                      f'format=yuv420p[v{i}]')
    fc = ';'.join(chains) + ';' + ''.join(f'[v{i}]' for i in range(len(SHEETS))) + \
        f'concat=n={len(SHEETS)}:v=1:a=0[out]'
    out = os.path.join(OUT, f'{name}-hero-loop.mp4')
    args += ['-filter_complex', fc, '-map', '[out]', '-an', '-c:v', 'libx264', '-preset', 'slow',
             '-crf', '28', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
    subprocess.run(args, check=True)
    print(f'{out}  {os.path.getsize(out) / 1e6:.1f} МБ')


def build(name):
    if name == 'brandbook':
        return build_sheets()
    segs = LOOPS[name]
    args, chains = ['ffmpeg', '-v', 'error', '-y'], []
    for i, (src, t, crop) in enumerate(segs):
        path = os.path.join(ROOT, src)
        args += ['-ss', str(t), '-t', str(SEG), '-i', path]
        chains.append(f'[{i}:v]{crop_expr(path, crop)},format=yuv420p[v{i}]')
    fc = ';'.join(chains) + ';' + ''.join(f'[v{i}]' for i in range(len(segs))) + \
        f'concat=n={len(segs)}:v=1:a=0[out]'
    out = os.path.join(OUT, f'{name}-hero-loop.mp4')
    args += ['-filter_complex', fc, '-map', '[out]', '-an', '-c:v', 'libx264', '-preset', 'slow',
             '-crf', '28', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
    subprocess.run(args, check=True)
    print(f'{out}  {os.path.getsize(out) / 1e6:.1f} МБ')


if __name__ == '__main__':
    for n in (sys.argv[1:] or [*LOOPS, 'brandbook']):
        build(n)
