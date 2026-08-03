#!/usr/bin/env python3
"""Ассеты кейса «Внутри стихии» / ТРЦ Ривьера (/event/riviera).

Источники (все лежат в ~/Downloads):
  • Riviera_report_FIN.pdf — финальный отчёт по проведению, 38 полос.
    Внутри две ценные вещи: репортажная съёмка вечера (1200×610, чистые кадры,
    подписи в PDF наложены текстом сверху и в растр не попадают) и слайды
    «МАТЕРИАЛЫ», где каждый вариант макета лежит ОТДЕЛЬНОЙ картинкой. Именно
    поэтому варианты приглашений, ключей, бейджей и касок берём потоком
    (extract_image), а не рендером полосы: иначе пришлось бы резать коллаж;
  • Proposal_Riviera_150622.pdf — предложение от 22.06.2015. Оттуда берём
    только то, что сделано нами или клиентом (рендер фасада ТРЦ), стоковые
    референсы предложения (ведущий, барабанщики, силуэты, еда) на страницу
    не идут.

Что делает:
  1. складывает репортаж вечера и слайды материалов как есть;
  2. режет полосу с четырьмя кирпичами на отдельные знаки стихий;
  3. режет чёрную полосу «четыре стихии» на четыре квадрата;
  4. вырезает зонт и аромат-набор из общей полосы подарков.

Итог: mirror/images/riviera/. После прогона — scripts/gen-webp.sh mirror/images/riviera
Идемпотентно, просто перезаписывает.
"""
import io
import os

import fitz
import numpy as np
from PIL import Image

REPORT = os.path.expanduser('~/Downloads/Riviera_report_FIN.pdf')
PROP = os.path.expanduser('~/Downloads/Proposal_Riviera_150622.pdf')
DST = 'mirror/images/riviera'

os.makedirs(DST, exist_ok=True)


def save(im, name, q=88):
    p = os.path.join(DST, name)
    if name.endswith('.png'):
        im.save(p)
    else:
        im.convert('RGB').save(p, quality=q, subsampling=0, optimize=True)
    print(f'  {name:<24} {im.size[0]}×{im.size[1]}')
    return p


def grab(doc, xref):
    """Растр из потока PDF без пережатия страницей."""
    x = doc.extract_image(xref)
    return Image.open(io.BytesIO(x['image']))


def trim(im, thr=250):
    """Обрезает белые поля вокруг объекта на белой подложке."""
    a = np.asarray(im.convert('RGB')).astype(int)
    mask = a.min(2) < thr
    ys, xs = np.where(mask)
    if not len(xs):
        return im
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def trim_alpha(im):
    """Обрезает прозрачные поля."""
    ys, xs = np.where(np.asarray(im.split()[-1]) > 0)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


# ─── репортаж вечера: xref → имя ────────────────────────────────────────────
SHOTS = {
    34: 'welcome-hostess',    # хостес в платьях фирменного цвета, стол с бейджами
    38: 'welcome-drink',      # официант с напитками на бетоне
    42: 'host',               # ведущий открывает вечер
    46: 'official-hall',      # зал во время официальной части
    50: 'official-gift',      # вручение памятных сувениров
    54: 'tour-amulet',        # гостья с табличкой «Воздух»
    58: 'tour-arch',          # экскурсия под арками галереи
    62: 'drummers',           # Vasiliev Groove
    66: 'catering',           # фуршетные острова
    70: 'umbrella-gift',      # зонты на выходе
    154: 'badges-photo',      # готовые бейджи на стойке регистрации
    158: 'stage',             # сцена с тремя экранами
    162: 'cocktails',         # приветственный коктейль
    166: 'audience',          # гости в зале
    170: 'stage-award',       # передача помещений на сцене
    174: 'tour-helmets',      # группа в касках на экскурсии
    178: 'team-photo',        # общее фото у пресс-волла
}

# ─── макеты и производство ──────────────────────────────────────────────────
MATS = {
    75: 'inv-deep',           # приглашение: тёмная вода
    76: 'inv-sunset',         # приглашение: закат
    77: 'inv-wave-ru',        # приглашение: волна, русская версия (в работе)
    78: 'inv-wave-en',        # приглашение: волна, английская версия (в работе)
    81: 'banner-street',      # уличный баннер 4×1,5 м
    83: 'presswall',          # пресс-волл 2×3 м
    87: 'navigation',         # напольная навигация
    100: 'key-box-open',      # ключ: куб с якорем внутри
    101: 'key-box-pair',      # ключ: куб закрытый и с запонками
    102: 'key-frame',         # ключ: ключ-визитка Auchan × Ривьера в раме
    95: 'key-capsule',        # ключ: капсула с грамотой
    98: 'key-usb',            # ключ: флешка в форме ключа
    119: 'badge-flat',        # бейджи: знак стихии и цветная плашка (в работе)
    116: 'badge-aqua',        # бейджи: акварельные стихии
    107: 'badge-pocket',      # бейджи: карман с цветной вкладкой
    110: 'badge-tassel',      # бейджи: кисти по цвету стихии
    113: 'badge-cord',        # бейджи: шнуры-браслеты
    125: 'helmet-a',          # каски с лого
    129: 'helmet-b',
    133: 'helmet-c',
    142: 'route-map',         # схема проезда
    143: 'route-shuttle',     # схема подъезда и шаттла
}


def main():
    rep = fitz.open(REPORT)
    print('репортаж вечера:')
    for xr, name in SHOTS.items():
        save(grab(rep, xr), f'{name}.jpg')

    print('материалы:')
    for xr, name in MATS.items():
        save(grab(rep, xr), f'{name}.jpg')

    # схема площадки лежит PNG с прозрачностью, кладём на белое
    plan = grab(rep, 146).convert('RGBA')
    bg = Image.new('RGBA', plan.size, (255, 255, 255, 255))
    save(Image.alpha_composite(bg, plan), 'plan.jpg')

    # подарки: слева аромат-набор, справа четыре флакона, отдельно зонт
    save(trim(grab(rep, 138)), 'gift-aroma.jpg')
    save(trim(grab(rep, 139)), 'gift-umbrella.jpg')

    # ── четыре кирпича со знаками стихий: кирпичи в полосе перекрываются,
    # поэтому режем не их, а снимаем белый фон, чтобы полоса легла на тёмную
    # страницу без светлой подложки
    br = grab(rep, 12).convert('RGB')
    a = np.asarray(br).astype(int)
    alpha = np.where(a.min(2) > 244, 0, 255).astype(np.uint8)
    br = br.convert('RGBA')
    br.putalpha(Image.fromarray(alpha))
    save(trim_alpha(br), 'bricks.png')

    # ── логотип ТРЦ: на титуле он векторный, поэтому рендерим область
    # бирюзовых кривых в PNG с прозрачностью, а не вынимаем растр
    pix = rep[0].get_pixmap(clip=fitz.Rect(213, 163, 630, 262),
                            matrix=fitz.Matrix(4, 4), alpha=True)
    logo = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    a = np.asarray(logo).astype(int)
    # серый градиент титула попадает в клип вместе с логотипом, гасим его
    alpha = np.where(a.min(2) > 228, 0, 255).astype(np.uint8)
    logo = logo.convert('RGBA')
    logo.putalpha(Image.fromarray(alpha))
    save(trim_alpha(logo), 'logo-riviera.png')

    # ── рендер фасада будущего ТРЦ (материал клиента, есть в обоих файлах)
    save(grab(rep, 19), 'facade.jpg')

    # макет теста на планшете из предложения: вырезаем сам планшет,
    # стоковые модели по краям полосы на страницу не идут
    pr = fitz.open(PROP)
    tab = grab(pr, 37)
    w, h = tab.size
    save(tab.crop((round(w * .202), round(h * .368), round(w * .810), h)), 'ipad-test.jpg')

    print('\nдальше: scripts/gen-webp.sh mirror/images/riviera')


if __name__ == '__main__':
    main()
