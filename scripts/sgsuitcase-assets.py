#!/usr/bin/env python3
"""Ассеты кейса «Проектный чемодан Saint-Gobain» (/creative/saintgobain/suitcase).

Источники:
  • ~/Downloads/Case.pdf — наше предложение клиенту от 31.07.2019, 9 полос.
    Растры внутри лежат крупнее, чем то, что когда-то залили на Tilda: полоса
    с тремя видами чемодана это картинка 3840×1684, то есть каждая грань
    больше тысячи пикселей по ширине. Поэтому берём поток (extract_image),
    а не рендер страницы;
  • ~/Downloads/Креативный бриф.pptx — оттуда нужны только три логотипа
    (Saint-Gobain, Gyproc, ISOVER). Фотографии чемодана-референса чужого
    бренда с рабочего стола НЕ трогаем, они на страницу не идут.

Что делает:
  1. режет полосу с чемоданом на три грани и отдельно вырезает «тело» каждой
     грани, без ручки, петель и ножек. Тела нужны для 3D-объекта в шапке:
     ширина лицевой и ширина торца дают реальную пропорцию коробки, и она
     собирается CSS-трансформами как настоящий параллелепипед;
  2. вынимает фотографии сюжета (перфоратор, спящий ребёнок), макет второй
     концепции и фото стартовой площадки к нему;
  3. переводит три логотипа из белой подложки в PNG с альфой.

Итог: mirror/images/sgsuitcase/. После прогона — scripts/gen-webp.sh mirror/images/sgsuitcase
Идемпотентно, просто перезаписывает.
"""
import io
import os
import zipfile

import fitz
import numpy as np
from PIL import Image

SRC = os.path.expanduser('~/Downloads/Case.pdf')
BRIEF = os.path.expanduser('~/Downloads/Креативный бриф.pptx')
DST = 'mirror/images/sgsuitcase'

os.makedirs(DST, exist_ok=True)


def save(im, name, q=90):
    p = os.path.join(DST, name)
    if name.endswith('.png'):
        im.save(p)
    else:
        im.convert('RGB').save(p, quality=q, subsampling=0, optimize=True)
    print(f'  {name:<18} {im.size[0]}×{im.size[1]}')
    return p


def content_box(im, thr=246):
    """Рамка непустого содержимого: всё, что темнее thr по любому каналу."""
    a = np.asarray(im.convert('RGB')).astype(int)
    mask = a.min(2) < thr
    ys, xs = np.where(mask)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def columns(im, thr=246, gap=30):
    """Разбивает картинку на вертикальные сегменты (три вида чемодана в ряд)."""
    a = np.asarray(im.convert('RGB')).astype(int)
    mask = a.min(2) < thr
    cols = mask.any(0)
    segs, start = [], None
    for i, v in enumerate(cols):
        if v and start is None:
            start = i
        if not v and start is not None:
            if i - start > gap:
                segs.append((start, i))
            start = None
    if start is not None:
        segs.append((start, len(cols)))
    return segs


def panel_body(im, thr=246):
    """Прямоугольник запечатанной панели: без ручки сверху и ножек снизу.

    Ручка занимает узкую полосу по центру, панель идёт почти во всю ширину
    кадра, поэтому строку считаем «телом», когда закрашено больше половины
    её ширины. Так же по колонкам внутри найденных строк."""
    a = np.asarray(im.convert('RGB')).astype(int)
    mask = a.min(2) < thr
    rows = np.where(mask.mean(1) > 0.5)[0]
    top, bot = rows.min(), rows.max() + 1
    sub = mask[top:bot]
    cols = np.where(sub.mean(0) > 0.5)[0]
    return cols.min(), top, cols.max() + 1, bot


def pdf_images(path):
    """Все растры документа по страницам: {номер страницы: [PIL.Image, ...]}.

    Серую подложку полосы InDesign кладёт одним и тем же объектом на каждую
    страницу, поэтому картинки, встречающиеся больше одного раза, пропускаем."""
    doc = fitz.open(path)
    used = {}
    for i in range(doc.page_count):
        for xref, *_ in doc[i].get_images(full=True):
            used[xref] = used.get(xref, 0) + 1
    out = {}
    for i in range(doc.page_count):
        imgs = []
        for xref, *_ in doc[i].get_images(full=True):
            if used[xref] > 1:
                continue
            d = doc.extract_image(xref)
            im = Image.open(io.BytesIO(d['image']))
            if im.width < 300:            # мелочь вроде иконок
                continue
            imgs.append(im.convert('RGB'))
        out[i + 1] = imgs
    return out


def alpha_logo(im, thr=238):
    """Белую подложку логотипа переводим в прозрачность, поля обрезаем."""
    im = im.convert('RGBA')
    a = np.array(im)
    white = (a[:, :, :3].min(2) >= thr)
    a[:, :, 3] = np.where(white, 0, 255)
    im = Image.fromarray(a)
    return im.crop(im.getbbox())


print('Case.pdf →', DST)
pages = pdf_images(SRC)

# ── полоса 4: три вида чемодана в ряд ────────────────────────────────────────
strip = max(pages[4], key=lambda i: i.width)
segs = columns(strip)
assert len(segs) == 3, f'ожидали три вида чемодана, нашли {len(segs)}'
names = ('front', 'edge', 'back')
for (x0, x1), name in zip(segs, names):
    view = strip.crop((x0, 0, x1, strip.height))
    # view-* это кадр целиком, с ручкой и тенью (идёт в разбор сторон),
    # face-* только запечатанная панель (из них собирается объёмный чемодан).
    # У торца кадр целиком не нужен: на странице он стоит только панелью
    if name != 'edge':
        save(view.crop(content_box(view)), f'view-{name}.jpg')
    save(view.crop(panel_body(view)), f'face-{name}.jpg')

# ── полоса 3: сюжет «две комнаты» ────────────────────────────────────────────
drill, baby = sorted(pages[3], key=lambda i: -i.width)[:2]
save(drill, 'room-work.jpg')
save(baby, 'room-sleep.jpg')

# ── полоса 6: макет второй концепции «Стартовая площадка» ────────────────────
# фотография космодрома с полосы 5 на страницу не идёт: вторая концепция стоит
# в переключателе одним кадром, и это именно макет чемодана
space = max(pages[6], key=lambda i: i.width).crop(
    content_box(max(pages[6], key=lambda i: i.width)))
# на странице кадр стоит максимум в 720 css-пикселей, 1400 хватает с запасом
space.thumbnail((1400, 1400), Image.LANCZOS)
save(space, 'alt-space.jpg')

# ── логотипы трёх брендов из брифа ───────────────────────────────────────────
print('Креативный бриф.pptx →', DST)
with zipfile.ZipFile(BRIEF) as z:
    media = {n: z.read(n) for n in z.namelist() if n.startswith('ppt/media/')}
# из брифа берём только логотипы: чемодан-референс чужого бренда и цеховые
# фотографии со страницы не идут, поэтому подписываем файлы вручную
for src, out in (('image7.png', 'logo-sg.png'),
                 ('image6.png', 'logo-gyproc.png'),
                 ('image5.png', 'logo-isover.png')):
    im = Image.open(io.BytesIO(media['ppt/media/' + src]))
    save(alpha_logo(im), out)

print('готово')
