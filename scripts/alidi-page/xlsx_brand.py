#!/usr/bin/env python3
"""Фирменный вид Excel для АЛИДИ: полихромия Hand Marketing, шапки листов картинками, 3D-фигуры разделов.

Шапки рисуются HTML → PNG через playwright (Montserrat и JetBrains Mono с локального mirror:8080),
потому что в ячейках Excel фирменных шрифтов у клиента может не быть. В ячейках Arial.
Используют budget.py и facts_xlsx.py.
"""
import base64
import json
import subprocess
from html import escape as e
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / 'xlsx-assets'
CACHE = ASSETS / 'png'          # отрендеренные PNG (пересобираются при каждом запуске)
NODE_PLAYWRIGHT = '/Users/aleksandrnarodetskii/.npm/_npx/6f4879659183bc49/node_modules/playwright/index.mjs'
FONT_ORIGIN = 'http://localhost:8080'   # сервер mirror: отдаёт /fonts/*.css

INK, PAPER = '080000', 'FAFAF8'
STONE = {50: 'F4F4F2', 100: 'E7E7E4', 200: 'C8C8C4', 400: '8C8C88', 600: '4A4A47', 800: '1F1F1D'}
# семь цветовых семей логотипа: (основной, светлая подложка, цвет текста на основном, фигура)
FAMILY = {
    'green':  ('93C01F', 'EEF5D9', INK, 'fig_02'),
    'orange': ('F6A500', 'FDF0D2', INK, 'fig_05'),
    'cyan':   ('60C0D8', 'E2F3F8', INK, 'fig_03'),
    'purple': ('941B80', 'F3E3F0', 'FFFFFF', 'fig_15'),
    'yellow': ('FDC400', 'FFF6CC', INK, 'fig_08'),
    'pink':   ('EE2BEE', 'FCE3FC', INK, 'fig_14'),
    'red':    ('E30521', 'FCE0E3', 'FFFFFF', 'fig_09'),
    'blue':   ('48A8D8', 'E3F1F9', INK, 'fig_10'),
}
ORDER = ['green', 'orange', 'cyan', 'purple', 'yellow', 'pink', 'red']
INPUT_FILL = 'FFF6B0'   # ячейки, которые можно менять


def svg_uri(path):
    return 'data:image/svg+xml;base64,' + base64.b64encode(Path(path).read_bytes()).decode()


def col_px(width_chars):
    """Ширина колонки Excel (в символах) → пиксели, как считает Excel для Calibri 11."""
    return int(width_chars * 7.8)  # подобрано по Excel для Mac: картинка встаёт ровно по ширине колонок


def render(jobs):
    """jobs: [{'out': путь, 'html': тело, 'w': px, 'h': px, 'transparent': bool}] → PNG @2x."""
    CACHE.mkdir(parents=True, exist_ok=True)
    spec = CACHE / '_jobs.json'
    spec.write_text(json.dumps(jobs, ensure_ascii=False), encoding='utf8')
    js = f'''
import {{ chromium }} from '{NODE_PLAYWRIGHT}';
import fs from 'fs';
const jobs = JSON.parse(fs.readFileSync({json.dumps(str(spec))}, 'utf8'));
const b = await chromium.launch({{ channel: 'chrome' }});
const p = await b.newPage({{ deviceScaleFactor: 2 }});
await p.goto('{FONT_ORIGIN}/');
for (const j of jobs) {{
  await p.setViewportSize({{ width: j.w, height: j.h }});
  await p.setContent(j.html, {{ waitUntil: 'networkidle' }});
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({{ path: j.out, omitBackground: !!j.transparent, clip: {{ x: 0, y: 0, width: j.w, height: j.h }} }});
}}
await b.close();
'''
    runner = CACHE / '_render.mjs'
    runner.write_text(js, encoding='utf8')
    subprocess.run(['node', str(runner)], check=True)


HEAD_CSS = '''<link rel="stylesheet" href="/fonts/montserrat.css"><link rel="stylesheet" href="/fonts/manrope-onest.css">
<style>*{margin:0;padding:0;box-sizing:border-box}html,body{width:100%;height:100%}
body{font-family:Montserrat,Arial,sans-serif;color:#080000;-webkit-font-smoothing:antialiased}
.mono{font-family:'JetBrains Mono',monospace}</style>'''


def banner_html(w, h, kicker, title, sub, figs, stripe=None, dark=False):
    """Шапка листа: логотипы HM и АЛИДИ, заголовок Montserrat 800, фигуры справа, полихромная полоса снизу.
    stripe: [(цвет, доля)] — полоса из долей разделов; по умолчанию семь равных цветов логотипа."""
    stripe = stripe or [(FAMILY[k][0], 1) for k in ORDER]
    tot = sum(s for _, s in stripe)
    bar = ''.join(f'<i style="flex:{s / tot:.4f};background:#{c}"></i>' for c, s in stripe)
    bg, fg, dim = ('#080000', '#fafaf8', 'rgba(250,250,248,.55)') if dark else ('#fafaf8', '#080000', '#8c8c88')
    hm = svg_uri(ASSETS / ('hm_logo_cube.svg' if dark else 'hm_logo_with_text.svg'))
    al = (HERE / 'alidi-logo.svg').read_text(encoding='utf8')
    if dark:
        al = al.replace('#141417', '#fafaf8')
    al_uri = 'data:image/svg+xml;base64,' + base64.b64encode(al.encode()).decode()
    pos = [(w - 250, 26, 74, -8), (w - 150, 70, 92, 6), (w - 330, 104, 58, 12), (w - 92, 18, 54, -14)]
    fg_imgs = ''.join(
        f'<img src="{svg_uri(ASSETS / (f + ".svg"))}" style="position:absolute;left:{x}px;top:{y}px;height:{s}px;transform:rotate({r}deg)">'
        for f, (x, y, s, r) in zip(figs, pos))
    return (f'<html><head>{HEAD_CSS}</head><body style="background:{bg};position:relative;overflow:hidden">'
            f'<div style="position:absolute;left:36px;top:26px;display:flex;align-items:center;gap:18px">'
            f'<img src="{hm}" style="height:{40 if dark else 46}px"><i style="width:1px;height:30px;background:{dim}"></i>'
            f'<img src="{al_uri}" style="height:17px"></div>'
            f'<p class="mono" style="position:absolute;left:36px;top:{max(h - 150, 100)}px;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:{dim}">{e(kicker)}</p>'
            f'<h1 style="position:absolute;left:34px;top:{max(h - 126, 124)}px;font-weight:800;font-size:46px;line-height:1;letter-spacing:-.03em;color:{fg}">{e(title)}</h1>'
            f'<p style="position:absolute;left:36px;top:{max(h - 64, 186)}px;font-size:14px;font-weight:500;color:{dim}">{e(sub)}</p>'
            f'{fg_imgs}<div style="position:absolute;left:0;right:0;bottom:0;height:10px;display:flex">{bar}</div></body></html>')


def fig_html(name, size):
    return (f'<html><head>{HEAD_CSS}</head><body style="background:transparent;display:flex;align-items:center;justify-content:center">'
            f'<img src="{svg_uri(ASSETS / (name + ".svg"))}" style="max-width:{size}px;max-height:{size}px"></body></html>')


def fig_png(name):
    return CACHE / f'{name}.png'


def render_figs(names, size=40):
    render([{'out': str(fig_png(n)), 'html': fig_html(n, size - 6), 'w': size, 'h': size, 'transparent': True} for n in names])


# ---------- openpyxl-помощники ----------
def styles():
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    F = 'Arial'

    def font(size=10, bold=False, color=INK, italic=False):
        return Font(name=F, size=size, bold=bold, color=color, italic=italic)

    def fill(c):
        return PatternFill('solid', fgColor=c)
    thin = Side(style='thin', color=STONE[100])
    return {
        'font': font, 'fill': fill,
        'line': Border(bottom=thin), 'line_ink': Border(top=Side(style='medium', color=INK)),
        'wrap': Alignment(wrap_text=True, vertical='top'), 'mid': Alignment(vertical='center'),
        'mid_r': Alignment(vertical='center', horizontal='right'), 'mid_c': Alignment(vertical='center', horizontal='center'),
        'top_r': Alignment(vertical='top', horizontal='right'),
    }


def paper(ws, rows, cols):
    """Фон «бумага» на всю рабочую область, а не белый Excel."""
    from openpyxl.styles import PatternFill
    f = PatternFill('solid', fgColor=PAPER)
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            ws.cell(r, c).fill = f


def put_image(ws, path, anchor, w, h):
    from openpyxl.drawing.image import Image
    img = Image(str(path))
    img.width, img.height = w, h
    ws.add_image(img, anchor)


def caps(ws, cell, text, color=STONE[400], size=8):
    from openpyxl.styles import Font
    ws[cell] = ' '.join(text.upper())   # разрядка, как у капс-плашек HM
    ws[cell].font = Font(name='Arial', size=size, bold=True, color=color)


def footer(ws, row, ncols, s):
    ws.cell(row, 2, 'Hand Marketing · hand-marketing.ru · +7 985 999 87 83 · anarodetsky@hand-marketing.ru').font = s['font'](8, color=STONE[400])
