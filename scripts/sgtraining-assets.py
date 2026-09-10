#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Обучение руководителей» Saint-Gobain (/video/saintgobain/training/).

Материал (папка «Материалы для обновления сайта/Saint-Gobain/Обучение»):
  • «1 часть_правки_ГОЛОС.mp4» — 467,3 с, 1280×720, 25 к/с: виды вопросов;
  • «2 часть_правка ГОЛОС.mp4» — 703,4 с: модель STAR и разбор неполных ответов;
  • «Презентация_ВИДЕО_26.12.2023_ver5.pptx» — 28 экранов курса;
  • «Структура_ Видео_26.12.2023_ver5.xlsx» — дикторский текст и реплики диалогов.

Тайм-коды взяты из scripts/a2/agent-out/sg-training/ (facts.json, scenes.json),
собранных фактологом по плотному скану обоих файлов.

Полных роликов на странице нет: это внутреннее обучение заказчика. На сайт
уезжают только немой хайлайт первого экрана и пять коротких фрагментов по темам,
все внутри mirror/** — на хостинг они попадают обычным деплоем, вручную грузить
нечего.

Запуск: python3 scripts/sgtraining-assets.py [--fonts] [--frames] [--clips] [--map]
Без флагов делает всё.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MIRROR = os.path.join(ROOT, 'mirror')
IMG = os.path.join(MIRROR, 'images', 'sgtraining')
VIDEOS = os.path.join(MIRROR, 'videos')
OUT = os.path.join(ROOT, 'scripts', 'a2', 'agent-out', 'sg-training')

SRC = os.environ.get('SGT_SRC', os.path.expanduser(
    '~/Documents/Материалы для обновления сайта/Saint-Gobain/Обучение'))
P1 = os.path.join(SRC, '1 часть_правки_ГОЛОС.mp4')
P2 = os.path.join(SRC, '2 часть_правка ГОЛОС.mp4')

FONTS = os.path.join(MIRROR, 'fonts')
FILES = os.path.join(FONTS, 'files')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
# Rubik: у знаков скруглённые углы, и это не «просто красиво» — тем же радиусом
# скруглены в роликах рамка окна живого кадра, плашка-комментарий и облако под
# флэт-иллюстрацией. Alegreya Sans держит длинные реплики диалогов, и у неё есть
# настоящая кириллическая италика — ей на странице говорит кандидат.
GF = ('https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,400..900;1,400..600'
      '&family=Alegreya+Sans:ital,wght@0,400;0,500;0,700;0,800;1,400;1,500&display=swap')
KEEP_SUBSETS = ('cyrillic-ext', 'cyrillic', 'latin-ext', 'latin')

# ─── кадры графики: тайм-код → имя, подпись ────────────────────────────────
# Границы графических сегментов сняты фактологом (scenes.json), внутри сегмента
# берётся момент, когда все плашки уже выехали и экран собран целиком.
GRAPHICS = [
    (P1,   5.8, 'g-title',     'Титр курса: подготовка к интервью и виды вопросов'),
    (P1,  30.0, 'g-prep',      'Подготовка к интервью и определение компетенции'),
    (P1,  60.0, 'g-open',      'Открытые вопросы: основной инструмент'),
    (P1,  78.0, 'g-closed',    'Закрытые вопросы: да или нет'),
    (P1, 100.0, 'g-clarify',   'Уточняющие вопросы'),
    (P1, 118.0, 'g-funnel',    'Воронка вопросов: открытый, уточняющие, закрытые'),
    (P1, 142.0, 'g-leading',   'Наводящие вопросы, содержащие ответ или оценку'),
    (P1, 163.0, 'g-social',    'Вопросы с социально ожидаемым ответом'),
    (P1, 182.0, 'g-complex',   'Сложные вопросы из нескольких вопросов'),
    (P1, 213.0, 'g-personal',  'Личная сфера: сначала спрашиваем разрешение'),
    (P1, 458.0, 'g-recap',     'Повторение материала первой части'),
    (P2,  80.0, 'g-star',      'Модель STAR: ситуация, задача, действия, результат'),
    (P2, 100.0, 'g-star-more', 'Уточняющие вопросы к модели STAR'),
    (P2, 412.0, 'g-star-sum',  'Разбор ответа по буквам S, T, A, R'),
    (P2, 440.0, 'g-partial',   'Что делать, если ответ неполный'),
    (P2, 692.0, 'g-final',     'Финальный экран: успешного интервью'),
]

# ─── кадры съёмки: девять диалогов, три плана на сцену ─────────────────────
LIVE = [
    (P1, 241.9, 'd1-wide',  1, 'Сцена 1, закрытые вопросы: общий план переговорной'),
    (P1, 250.4, 'd1-a',     1, 'Сцена 1: крупный план'),
    (P1, 240.4, 'd1-b',     1, 'Сцена 1: второй крупный план'),
    (P1, 336.4, 'd2-wide',  2, 'Сцена 2, открытый вопрос про стресс: общий план'),
    (P1, 312.5, 'd2-a',     2, 'Сцена 2: крупный план'),
    (P1, 317.1, 'd2-b',     2, 'Сцена 2: второй крупный план'),
    (P1, 378.6, 'd3-wide',  3, 'Сцена 3, самая короткая в курсе: общий план'),
    (P1, 379.6, 'd3-a',     3, 'Сцена 3: крупный план'),
    (P1, 414.6, 'd4-wide',  4, 'Сцена 4, вопрос о плане развития: общий план'),
    (P1, 418.1, 'd4-a',     4, 'Сцена 4: крупный план'),
    (P1, 427.1, 'd4-b',     4, 'Сцена 4: второй крупный план'),
    (P2, 135.0, 'd5-wide',  5, 'Сцена 5, пример не тех лет: общий план'),
    (P2, 125.0, 'd5-a',     5, 'Сцена 5: крупный план'),
    (P2, 113.1, 'd5-b',     5, 'Сцена 5: второй крупный план'),
    (P2, 214.1, 'd6-wide',  6, 'Сцена 6, переговоры по грунтовке: общий план'),
    (P2, 215.7, 'd6-a',     6, 'Сцена 6: крупный план'),
    (P2, 187.1, 'd6-b',     6, 'Сцена 6: второй крупный план'),
    (P2, 381.5, 'd7-wide',  7, 'Сцена 7, задача без опыта: общий план'),
    (P2, 392.0, 'd7-a',     7, 'Сцена 7: крупный план'),
    (P2, 330.0, 'd7-b',     7, 'Сцена 7: второй крупный план'),
    (P2, 458.5, 'd8-wide',  8, 'Сцена 8, нелояльный клиент: общий план'),
    (P2, 500.4, 'd8-a',     8, 'Сцена 8: крупный план'),
    (P2, 468.0, 'd8-b',     8, 'Сцена 8: второй крупный план'),
    (P2, 537.9, 'd9-wide',  9, 'Сцена 9, самая длинная в курсе: общий план'),
    (P2, 555.6, 'd9-a',     9, 'Сцена 9: крупный план'),
    (P2, 553.7, 'd9-b',     9, 'Сцена 9: второй крупный план'),
]

# приём фильма: живой кадр уезжает и уменьшается, слева выходит светлая панель,
# сверху встаёт плашка с разбором. Девять раз на два ролика, по одному на диалог
COMMENTS = [
    (P1, 265.0, 'c-d1', 'Разбор первого диалога поверх кадра сцены'),
    (P2, 285.0, 'c-d6', 'Разбор шестого диалога: пример релевантный'),
    (P2, 525.0, 'c-d8', 'Разбор восьмого диалога: связи с результатом нет'),
]

# шторка из трёх полос: живёт 0,1–0,2 с, тайм-код взят из facts.json (f44/f45)
WIPE = (P1, 230.52, 'wipe', 'Фирменный переход: шторка из трёх полос')

# ─── фрагменты, которые уезжают на сайт ────────────────────────────────────
# Со звуком, короткие, по одному на тему. Полных роликов на странице нет.
CLIPS = [
    ('clip-closed',    P1, 238.3, 19.2, 'Диалог 1 целиком: закрытые вопросы и социально ожидаемые ответы'),
    ('clip-open',      P1, 412.5, 19.0, 'Диалог 4: открытый вопрос и конкретный ответ'),
    ('clip-star',      P2,   9.1, 31.0, 'Моушн-графика: как собирается модель STAR'),
    ('clip-weak',      P2, 103.2, 30.0, 'Диалог 5: пример десятилетней давности и просьба заменить его'),
    ('clip-interrupt', P2, 537.3, 38.0, 'Диалог 9: интервьюер дважды вежливо возвращает кандидата к делу'),
]

# немой хайлайт первого экрана: пять кусков по 2,5 с
HERO = [
    (P2, 537.9, 2.5),   # общий план девятой сцены
    (P1, 414.0, 2.5),   # общий план четвёртой сцены
    (P2,  79.0, 2.5),   # экран модели STAR
    (P1, 116.5, 2.5),   # экран воронки вопросов
    (P1, 316.0, 2.5),   # крупный план в разговоре
]


def fetch(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA})).read()


def fonts():
    os.makedirs(FILES, exist_ok=True)
    css = fetch(GF).decode('utf-8')
    blocks = re.findall(r'/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    out, n = [], 0
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        wght = re.search(r'font-weight:\s*([\d .]+)', block).group(1).strip().replace(' ', '-')
        ital = 'i' if 'font-style: italic' in block else ''
        name = f'{fam.lower().replace(" ", "-")}-{wght}{ital}-{subset}.woff2'
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        path = os.path.join(FILES, name)
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(url))
            n += 1
        out.append(block.replace(url, f'files/{name}'))
    head = ('/* Rubik + Alegreya Sans, self-host для /video/saintgobain/training/.\n'
            '   Сгенерировано scripts/sgtraining-assets.py, руками не править. */\n')
    open(os.path.join(FONTS, 'rubik-alegreya.css'), 'w', encoding='utf-8').write(
        head + '\n'.join(out) + '\n')
    print(f'✓ шрифты: {len(out)} @font-face, скачано файлов {n}')


def grab(src, t, name, widths=(1120, 560)):
    """Кадр 16:9 в двух ширинах. Кадр берётся точно, без поиска резкости:
    графика статична, а в диалогах планы длинные и мыла нет."""
    os.makedirs(IMG, exist_ok=True)
    for i, w in enumerate(widths):
        out = os.path.join(IMG, f'{name}.jpg' if i == 0 else f'{name}@{w}.jpg')
        pre = max(0.0, t - 4.0)
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{pre:.2f}', '-i', src,
                        '-ss', f'{t - pre:.2f}', '-frames:v', '1',
                        '-vf', f'scale={w}:-2',
                        '-q:v', '3', '-y', out], check=True)


def frames():
    rows = []
    for src, t, name, cap in GRAPHICS:
        grab(src, t, name)
        rows.append({'id': name, 'kind': 'graphics', 'part': 1 if src == P1 else 2,
                     't': t, 'caption': cap})
        print(f'  · {name:<12} {t:6.1f}s  {cap}')
    for src, t, name, dlg, cap in LIVE:
        grab(src, t, name)
        rows.append({'id': name, 'kind': 'live', 'part': 1 if src == P1 else 2,
                     't': t, 'dialog': dlg, 'caption': cap})
        print(f'  · {name:<12} {t:6.1f}s  {cap}')
    for src, t, name, cap in COMMENTS:
        grab(src, t, name)
        rows.append({'id': name, 'kind': 'comment', 'part': 1 if src == P1 else 2,
                     't': t, 'caption': cap})
        print(f'  · {name:<12} {t:6.1f}s  {cap}')
    src, t, name, cap = WIPE
    grab(src, t, name, widths=(1120, 560))
    rows.append({'id': name, 'kind': 'wipe', 'part': 1, 't': t, 'caption': cap})
    print(f'  · {name:<12} {t:6.1f}s  {cap}')
    json.dump(rows, open(os.path.join(OUT, 'frames.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'✓ кадров: {len(rows)}')


def clips():
    os.makedirs(VIDEOS, exist_ok=True)
    rows = []
    for name, src, t0, dur, cap in CLIPS:
        out = os.path.join(VIDEOS, f'sgt-{name}.mp4')
        pre = max(0.0, t0 - 4.0)
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{pre:.2f}', '-i', src,
                        '-ss', f'{t0 - pre:.2f}', '-t', f'{dur:.2f}',
                        '-vf', 'scale=960:-2',
                        '-c:v', 'libx264', '-crf', '26', '-preset', 'slow',
                        '-pix_fmt', 'yuv420p', '-profile:v', 'high',
                        '-c:a', 'aac', '-b:a', '96k', '-ac', '2',
                        '-movflags', '+faststart', '-y', out], check=True)
        mb = os.path.getsize(out) / 1e6
        rows.append({'id': name, 'src': f'/videos/sgt-{name}.mp4', 'dur': dur,
                     'part': 1 if src == P1 else 2, 't': t0, 'caption': cap,
                     'mb': round(mb, 2)})
        print(f'  · sgt-{name:<15} {dur:5.1f}s  {mb:5.2f} МБ  {cap}')
    hero()
    json.dump(rows, open(os.path.join(OUT, 'clips.json'), 'w'),
              ensure_ascii=False, indent=1)


def hero():
    """Немой хайлайт первого экрана: пять кусков по 2,5 с, без звука."""
    parts = []
    for i, (src, t0, dur) in enumerate(HERO):
        p = os.path.join('/tmp', f'sgt-hero-{i}.mp4')
        pre = max(0.0, t0 - 4.0)
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{pre:.2f}', '-i', src,
                        '-ss', f'{t0 - pre:.2f}', '-t', f'{dur:.2f}', '-an',
                        '-vf', 'scale=960:-2,fps=25',
                        '-c:v', 'libx264', '-crf', '27', '-preset', 'slow',
                        '-pix_fmt', 'yuv420p', '-y', p], check=True)
        parts.append(p)
    lst = '/tmp/sgt-hero-list.txt'
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    out = os.path.join(VIDEOS, 'sgt-hero-loop.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                    '-c', 'copy', '-movflags', '+faststart', '-y', out], check=True)
    print(f'  · sgt-hero-loop      {sum(d for _, _, d in HERO):5.1f}s  '
          f'{os.path.getsize(out) / 1e6:5.2f} МБ  немой хайлайт первого экрана')


def main():
    args = sys.argv[1:]
    todo = set(a.lstrip('-') for a in args) or {'fonts', 'frames', 'clips'}
    if 'fonts' in todo:
        fonts()
    if 'frames' in todo:
        frames()
    if 'clips' in todo:
        clips()


if __name__ == '__main__':
    main()
