#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Кадры для кейса /video/powertechnologies — режутся из обеих версий фильма.

Своей фотосъёмки по проекту нет, кейс про видеопродакшн, поэтому вся графика
страницы это кадры самих роликов. Где сцена есть в короткой версии, кадр берём
из неё: короткая версия лежит в 1280x720, полная в 640x360. Из полной режем
только то, чего в короткой нет.

Два кадра со съёмочной площадки (аппаратная и оператор на стадионе) уже лежат
в mirror/case-assets в высоком разрешении со времён Tilda, их просто
переносим и пережимаем.

Тайминги совпадают с OBJECTS/VOICES в scripts/a2/gen_powertech.py: клик по
карточке перематывает плеер ровно на тот эпизод, кадр из которого в карточке.

Запуск: python3 scripts/powertech-assets.py   (нужен ffmpeg)
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
MEDIA = os.path.join(ROOT, 'media')
CASE = os.path.join(ROOT, 'mirror', 'case-assets')
OUT = os.path.join(ROOT, 'mirror', 'images', 'powertech')

SHORT = os.path.join(MEDIA, 'pt-film-short.mp4')
LONG = os.path.join(MEDIA, 'pt-film-long.mp4')

# имя, источник, секунда, ширина, качество
SHOTS = [
    # ── короткая версия, 720p ──────────────────────────────────────────────
    ('poster-short',  SHORT,  37.0, 1280, 3),   # Лужники, оборудование на трибуне
    ('obj-match',     SHORT,  66.0, 1200, 3),   # матч на арене, общий план
    ('nums-a',        SHORT,  78.0, 1200, 3),   # инфографика: ДГУ, топливо, щиты
    ('nums-b',        SHORT,  92.0, 1200, 3),   # инфографика: кабель, мощность, люди
    ('sp-best',       SHORT, 105.5,  900, 4),   # Малкольм Бест
    ('shoot-fence',   SHORT, 112.0, 1100, 4),   # обход площадки
    ('sp-sherbakov',  SHORT, 141.0,  900, 4),   # Олег Щербаков
    ('shoot-cables',  SHORT, 165.0, 1100, 4),   # кабельные трассы
    ('sp-yablonski',  SHORT, 181.0,  900, 4),   # Чарльз Яблонски, NBC
    ('sp-grinter',    SHORT, 218.0,  900, 4),   # Питер Гринтер, NBC и Telemundo
    ('sp-warram',     SHORT, 196.0,  900, 4),   # Уаррам Питер Леонард, HBS
    ('shoot-gen',     SHORT, 225.0, 1100, 4),   # доставка ДГУ краном
    # ── полная версия, 360p: только то, чего в короткой нет ────────────────
    ('sp-antonyan',   LONG,  151.5,  860, 4),   # Эдуард Антонян
    ('sp-krylov',     LONG,  195.0,  860, 4),   # Александр Крылов
    ('sp-sapozhnikov', LONG, 266.5,  860, 4),   # Леонид Сапожников
    ('cut-ibc',       LONG,  222.0,  860, 4),   # монтаж вещательного центра, не вошло
    ('cut-fans',      LONG,  616.0,  860, 4),   # трибуны, не вошло
]

# готовые кадры со съёмки, лежат с Tilda-времён
COPIES = [
    ('poster-full',  'cf073ba9_image_2020-10-10_23-.png', 1400, 3),   # аппаратная
    ('shoot-camera', 'dd50cd1c_image_2020-10-11_00-.png', 1400, 3),   # оператор на поле
]


def grab(name, src, sec, width, q):
    """Кадр из видео. Быстрая перемотка до sec-6 и точная досылка декодером:
    иначе ffmpeg встаёт на ближайший ключевой кадр и промахивается на секунды,
    а тайминги тут должны совпадать с кнопками перемотки на странице."""
    pre = max(0.0, sec - 6)
    dst = os.path.join(OUT, name + '.jpg')
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(pre), '-i', src,
                    '-ss', str(round(sec - pre, 2)), '-frames:v', '1',
                    '-vf', f'scale={width}:-2:flags=lanczos',
                    '-q:v', str(q), dst, '-y'], check=True)
    return dst


def copy(name, src, width, q):
    dst = os.path.join(OUT, name + '.jpg')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(CASE, src),
                    '-vf', f'scale={width}:-2:flags=lanczos', '-q:v', str(q),
                    dst, '-y'], check=True)
    return dst


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, src, sec, width, q in SHOTS:
        p = grab(name, src, sec, width, q)
        total += os.path.getsize(p)
        tag = 'short' if src == SHORT else 'long '
        print(f'{name:16s} {tag} {sec:6.1f}s  {os.path.getsize(p) // 1024:4d} KB')
    for name, src, width, q in COPIES:
        p = copy(name, src, width, q)
        total += os.path.getsize(p)
        print(f'{name:16s} case-assets     {os.path.getsize(p) // 1024:4d} KB')
    print(f'— всего {total // 1024} KB в {OUT.replace(ROOT, "")}')
