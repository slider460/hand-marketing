#!/usr/bin/env python3
"""Немой луп первого экрана /for/alidi/: нарезка складов, отгрузки, терминалов и производства
из наших фильмов. Рецепт как у sgt-hero-loop: куски до 2,2 с, 854×480, 25 к/с, без звука, CRF 31.
Куски подобраны вручную по раскадровке, каждый внутри одного плана; кадр
обрезан от левого нижнего угла (82 %), чтобы ушли логотипы заказчиков справа сверху.

Источники читаются с прода по Range (целиком не качаются). Таймкоды взяты из
scripts/sgcx-assets.py, rgd-history-assets.py, isotec-assets.py, powertech-assets.py.
Выход: mirror/for/alidi/img/hero-loop.mp4 + постер hero-loop.jpg (первый кадр).
Запуск: python3 scripts/alidi-page/hero_loop.py
"""
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'mirror' / 'for' / 'alidi' / 'img'
M = 'https://hand-marketing.ru/media/'
SG, RZD, ISO, PT = M + 'sg-cx-part1.mp4', M + 'transrzhd.mp4', M + 'izotek-brand-video.mp4', M + 'pt-film-short.mp4'

CUTS = [  # источник, начало, длительность (подобраны по раскадровке 4 к/с, каждый кусок внутри одного плана)
    (SG, 221.05, 1.35, 'погрузчик с паллетами'),
    (SG, 222.80, 1.00, 'погрузка в фуру'),
    (SG, 224.05, 1.20, 'фура на мосту'),
    (SG, 225.55, 1.30, 'трасса с воздуха'),
    (RZD, 113.90, 1.60, 'козловой кран на терминале'),
    (RZD, 158.10, 1.50, 'кран над контейнером, сверху'),
    (RZD, 94.30, 1.60, 'контейнерный двор с воздуха'),
    (ISO, 187.55, 1.20, 'цех'),
    (ISO, 189.05, 1.50, 'оператор на линии'),
    (SG, 195.30, 0.90, 'плита на конвейере'),
    (ISO, 178.35, 1.40, 'замер изоляции'),
    (PT, 224.00, 1.60, 'генератор и кран на объекте'),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix='alidi-loop-'))
    parts, total = [], 0.0
    for i, (src, t0, dur, what) in enumerate(CUTS):
        p = tmp / f'{i:02d}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.2f}', '-i', src, '-t', f'{dur:.2f}', '-an',
                        '-vf', 'crop=iw*0.82:ih*0.82:0:ih*0.18,scale=854:480:force_original_aspect_ratio=increase,crop=854:480,fps=25,setsar=1',
                        '-c:v', 'libx264', '-crf', '31', '-preset', 'slow', '-tune', 'film', '-pix_fmt', 'yuv420p',
                        '-y', str(p)], check=True)
        parts.append(p)
        total += dur
        print(f'  · {i:02d} {what}: {t0:.2f}+{dur:.2f}')
    lst = tmp / 'list.txt'
    lst.write_text(''.join(f"file '{p}'\n" for p in parts))
    out = OUT / 'hero-loop.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst),
                    '-c', 'copy', '-movflags', '+faststart', '-y', str(out)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(out), '-frames:v', '1', '-q:v', '4', '-y', str(OUT / 'hero-loop.jpg')], check=True)
    print(f'hero-loop.mp4 {total:.1f} с, {os.path.getsize(out) / 1e6:.2f} МБ')


if __name__ == '__main__':
    main()
