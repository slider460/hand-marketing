#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сравнивает две версии фильма Power Technologies и складывает результат в JSON.

Кейс /video/powertechnologies строится вокруг того, что на выходе две версии
одного фильма. Чтобы показать это честно, а не на словах, обе версии
сопоставляются покадрово:

  1. из каждого файла раз в секунду берётся кадр 16x16 в градациях серого;
  2. яркость и контраст каждого кадра нормализуются, чтобы цветокоррекция и
     затемнения не мешали сравнению;
  3. для каждой секунды короткой версии ищется самый похожий кадр полной
     (косинусная близость);
  4. подряд идущие совпадения, где источник тоже идёт подряд, склеиваются в
     сегменты. Получается монтажный лист: какой кусок полной версии куда
     переехал в короткой.

Результат ложится в scripts/a2/powertech_edl.json, страницу из него собирает
scripts/a2/gen_powertech.py. Перегенерировать нужно только если поменяются
сами файлы роликов.

Запуск: python3 scripts/powertech-edl.py   (нужны ffmpeg и numpy)
"""
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
MEDIA = os.path.join(ROOT, 'media')
OUT = os.path.join(HERE, 'a2', 'powertech_edl.json')

LONG = 'pt-film-long.mp4'
SHORT = 'pt-film-short.mp4'
W = H = 16          # размер миниатюры кадра
Q = 0.80            # ниже этой близости считаем, что кадр не опознан
JUMP = 3            # разрыв в источнике больше этого = новая склейка


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                          'format=duration', '-of', 'csv=p=0', path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def frames(path):
    """Посекундные кадры как нормализованные векторы (N, W*H)."""
    cmd = ['ffmpeg', '-v', 'error', '-i', path,
           '-vf', f'fps=1,scale={W}:{H},format=gray',
           '-f', 'rawvideo', '-pix_fmt', 'gray', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, W * H).astype(np.float64)
    a -= a.mean(axis=1, keepdims=True)
    n = np.linalg.norm(a, axis=1, keepdims=True)
    n[n == 0] = 1
    return a / n


def build():
    lp, sp = os.path.join(MEDIA, LONG), os.path.join(MEDIA, SHORT)
    lng, shr = frames(lp), frames(sp)
    sim = shr @ lng.T
    best, score = sim.argmax(axis=1), sim.max(axis=1)

    segs, cur = [], None
    for i in range(len(shr)):
        if score[i] < Q:
            cur = None
            continue
        l = int(best[i])
        if cur and i == cur['s1'] + 1 and 0 <= l - cur['l1'] <= JUMP:
            cur['s1'], cur['l1'] = i, max(cur['l1'], l)
            continue
        cur = {'s0': i, 's1': i, 'l0': l, 'l1': l}
        segs.append(cur)
    segs = [g for g in segs if g['s1'] - g['s0'] >= 1]   # одиночные кадры это шум

    kept = sum(g['l1'] - g['l0'] + 1 for g in segs)
    data = {
        'long': {'file': '/media/' + LONG, 'dur': round(duration(lp), 2)},
        'short': {'file': '/media/' + SHORT, 'dur': round(duration(sp), 2)},
        'segments': [[g['l0'], g['l1'], g['s0'], g['s1']] for g in segs],
        'kept': kept,
        'matched': sum(g['s1'] - g['s0'] + 1 for g in segs),
    }
    return data


if __name__ == '__main__':
    d = build()
    json.dump(d, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"полная {d['long']['dur']:.0f} c, короткая {d['short']['dur']:.0f} c")
    print(f"сегментов {len(d['segments'])}, в короткую вошло {d['kept']} c "
          f"({d['kept'] / d['long']['dur'] * 100:.0f}% полной версии)")
    print('записано', OUT)
