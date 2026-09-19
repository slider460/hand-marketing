#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Режет hero-лупы и кадры для галерей трёх страниц видеопродакшна.

Луп: 6 фрагментов по 2,6 с из своих же роликов, 1280×720, без звука, ~2 МБ,
как у /videoproduction (/media/vp-hero-loop.mp4). Кадры для галереи снимаются
из тех же роликов в 1600 px.

Тайм-коды выбраны глазами по контактным листам (кадры без титров с именами,
без чёрных и переходных планов).

    python3 scripts/a2/make_video_loops.py            # всё
    python3 scripts/a2/make_video_loops.py ad         # одна страница

Лупы кладутся в media/ и на сервер заливаются ВРУЧНУЮ (см. VIDEO-UPLOAD.md),
кадры кладутся в mirror/images/vpg/ и уезжают обычным деплоем.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
MEDIA = os.path.join(ROOT, 'media')
SHOTS = os.path.join(ROOT, 'mirror', 'images', 'vpg')

CLIP = 2.6  # длина фрагмента в лупе

# (источник, секунда) для лупа
LOOPS = {
    'ad': [('eaton-yaz', 17.6), ('gazelle-transformer', 40.7), ('vivax-samburskaya', 29.7),
           ('eaton-yaz', 23.8), ('vivax-samburskaya', 39.8), ('gazelle-transformer', 72.2)],
    'film': [('transrzhd', 21.1), ('sg-cx-part1', 80.2), ('pt-film-long', 134.6),
             ('transrzhd', 117.1), ('sg-cx-part1', 208.3), ('pt-film-long', 349.7)],
    'obj': [('mozaika', 52.1), ('salaris-1', 16.1), ('mmg-paveleckaya', 99.5),
            ('mozaika', 79.8), ('salaris-1', 107.6), ('technopark-zubovo', 54.4)],
}

# (имя файла, источник, секунда) для галереи кадров
SHOTLIST = {
    'ad': [('patriot-mud', 'eaton-yaz', 17.6), ('patriot-ford', 'eaton-yaz', 23.8),
           ('patriot-diff', 'eaton-yaz', 36.0), ('vivax-gym', 'vivax-samburskaya', 29.7),
           ('vivax-apply', 'vivax-samburskaya', 39.8), ('gaz-robot', 'gazelle-transformer', 40.7),
           ('gaz-street', 'gazelle-transformer', 72.2)],
    'film': [('rzd-yard', 'transrzhd', 21.1), ('rzd-crane', 'transrzhd', 117.1),
             ('rzd-air', 'transrzhd', 189.1), ('sg-wall', 'sg-cx-part1', 80.2),
             ('sg-line', 'sg-cx-part1', 208.3), ('pt-gallery', 'pt-film-long', 134.6),
             ('pt-numbers', 'pt-film-long', 349.7), ('isotec-plant', 'izotek-brand-video', 137.0)],
    'obj': [('mozaika-air', 'mozaika', 52.1), ('mozaika-gallery', 'mozaika', 79.8),
            ('mozaika-link', 'mozaika', 107.5), ('salaris-scheme', 'salaris-1', 16.1),
            ('salaris-site', 'salaris-1', 107.6), ('mmg-air', 'mmg-paveleckaya', 99.5),
            ('mmg-reach', 'mmg-paveleckaya', 168.7), ('zubovo-map', 'technopark-zubovo', 35.5),
            ('zubovo-plan', 'technopark-zubovo', 54.4)],
}


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def loop(key):
    parts, tmp = [], os.path.join(MEDIA, '.tmp')
    os.makedirs(tmp, exist_ok=True)
    for i, (src, at) in enumerate(LOOPS[key]):
        out = os.path.join(tmp, f'{key}-{i}.mp4')
        run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(MEDIA, src + '.mp4'),
             '-ss', str(at), '-t', str(CLIP),
             '-vf', 'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=25',
             '-an', '-c:v', 'libx264', '-crf', '28', '-preset', 'slow',
             '-pix_fmt', 'yuv420p', out])
        parts.append(out)
    lst = os.path.join(tmp, f'{key}.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    dst = os.path.join(MEDIA, f'{key}-hero-loop.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst,
         '-c:v', 'libx264', '-crf', '28', '-preset', 'slow', '-pix_fmt', 'yuv420p',
         '-movflags', '+faststart', '-an', dst])
    # постер: первый кадр лупа, им же закрывается hero до старта видео
    run(['ffmpeg', '-v', 'error', '-y', '-i', dst, '-frames:v', '1', '-q:v', '3',
         os.path.join(SHOTS, f'{key}-hero.jpg')])
    for p in parts + [lst]:
        os.remove(p)
    print(f'{key}-hero-loop.mp4  {os.path.getsize(dst)//1024} КБ')


def shots(key):
    d = os.path.join(SHOTS, key)
    os.makedirs(d, exist_ok=True)
    for name, src, at in SHOTLIST[key]:
        out = os.path.join(d, name + '.jpg')
        run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(MEDIA, src + '.mp4'),
             '-ss', str(at), '-frames:v', '1', '-vf', 'scale=1600:-2', '-q:v', '3', out])
    print(f'{key}: кадров {len(SHOTLIST[key])}')


if __name__ == '__main__':
    os.makedirs(SHOTS, exist_ok=True)
    keys = sys.argv[1:] or list(LOOPS)
    for k in keys:
        loop(k)
        shots(k)
