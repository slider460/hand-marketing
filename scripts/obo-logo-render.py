#!/usr/bin/env python3
"""Из ОФИЦИАЛЬНОГО вектора логотипа OBO Bettermann (scripts/assets/obo-logo.svg —
оригинал прислан клиентом; OBO оранжевый #F39B00, BETTERMANN контуры #1A171B)
пишет цветовые SVG-варианты в mirror/images/obo/ для использования на странице
через <img src=".svg"> (идеально чётко, без растеризации):
  logo-color.svg — оригинал (оранж OBO + чёрный BETTERMANN) — для светлого фона
  logo-white.svg — весь белый — для оранжевого/тёмного фона
  logo-ink.svg   — весь графит #282a31

PNG-растр нужен только обложкам каталога (PIL): logo-white.png растеризуется
из logo-white.svg движком браузера (canvas.toDataURL) — на этой машине нет
libcairo/renderPM. Готовый PNG лежит в репозитории; пере-растеризация — вручную
через локальный превью-сервер (см. memory obo-academy-case)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
SRC = os.path.join(HERE, 'assets', 'obo-logo.svg')
OUT = os.path.join(ROOT, 'mirror', 'images', 'obo')
os.makedirs(OUT, exist_ok=True)

src = open(SRC, encoding='utf-8').read()
VARIANTS = {
    'color': src,
    'white': src.replace('#F39B00', '#FFFFFF').replace('#1A171B', '#FFFFFF'),
    'ink':   src.replace('#F39B00', '#282A31').replace('#1A171B', '#282A31'),
}

if __name__ == '__main__':
    for name, svg in VARIANTS.items():
        p = os.path.join(OUT, f'logo-{name}.svg')
        open(p, 'w', encoding='utf-8').write(svg)
        print('written', p)
