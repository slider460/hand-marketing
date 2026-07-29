#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ассеты кейса «Посадочная страница ТРЦ Смайл» (Becar Asset Management).

Источник: исходники самой посадочной страницы — ~/Downloads/Site_Smile_HM_v12_200814
(вёрстка 2020 года: HTML + CSS + Gotham Pro + картинки). Сайт клиента давно снят
с продажи, поэтому кейс собираем из живого исходника, а не из архивных мокапов.

Что делает:
  1. поднимает копию исходника на localhost (vite отдаёт public/_smilesrc/) и
     снимает страницу целиком headless-хромом: десктоп 1440 и телефон 375@2x;
     версия shot.html отличается от боевой только двумя вещами — гугл-карта
     заменена локальным снимком (в headless iframe пустой) и scroll-анимации
     домотаны до финального состояния;
  2. режет полноразмерные снимки на экраны для разбора («первый экран»,
     «арендаторы», «Макдональдс», «гарантии», «цифры», «карта», «Becar»);
  3. перекладывает фирменные элементы страницы: подмигивающий смайл (gif),
     контурный логотип СМАЙЛ, логотипы 14 арендаторов;
  4. пересобирает обложку каталога: у карточки в /digital/ стояла плашка
     «Creative», хотя кейс живёт в Digital.

Запуск (нужен поднятый `npm run dev` и папка public/_smilesrc):
    python3 scripts/smile-assets.py            # всё
    python3 scripts/smile-assets.py --no-shots # без съёмки, только резка/копии

Итог: mirror/images/smile/. После прогона — scripts/gen-webp.sh mirror/images/smile
"""
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
SRC = os.path.expanduser('~/Downloads/Site_Smile_HM_v12_200814')
PUB = os.path.join(ROOT, 'public', '_smilesrc')      # копия исходника под vite
DST = os.path.join(ROOT, 'mirror', 'images', 'smile')
TMP = os.path.join(ROOT, '.smile-shots')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
URL = 'http://localhost:5173/_smilesrc/shot.html'

# Размеры съёмки. Десктоп — 1440. Телефон снимаем в окне 500: headless-хром не
# опускает вьюпорт ниже ~500 CSS px, и при 375 мобильная раскладка обрезается
# справа. При 500 кадр совпадает с тем, что показывает настоящий телефон.
DESK_W, DESK_H = 1440, 6945
MOB_W, MOB_H = 500, 7923

# границы блоков посадочной на десктопе (сняты в браузере)
BLOCKS = {
    'hero':      (0, 1040),        # block1 — логотип, форма, смайл
    'tenants':   (1040, 2074),     # block2 — 80% + слайдер арендаторов
    'mac':       (2087, 2857),     # block3 — готовый арендный бизнес
    'guarantee': (2857, 3738),     # block4 — гарантии дохода
    'numbers':   (3737, 4807),     # block5 — секрет успеха, цифры
    'map':       (4737, 5487),     # block6 — Smile Family на карте района
    'becar':     (5487, 6438),     # block8 — цифры группы Becar
}
# то же на телефоне
MOB_BLOCKS = {
    'mob-hero':    (0, 885),
    'mob-numbers': (4444, 5879),   # по волне: где начинается и кончается бирюза
    'mob-becar':   (5879, 7113),
}

TENANTS = [
    ('perekrestok', 'Перекрёсток'), ('familiya', 'Фамилия'), ('modis', 'Modis'),
    ('sberbank', 'Сбербанк'), ('mts', 'МТС'), ('beeline', 'Билайн'),
    ('bukvoed', 'Буквоед'), ('kari', 'Kari'), ('obuv.com', 'Obuv.com'),
    ('trial_sport', 'Триал-Спорт'), ('redmond', 'Redmond'), ('detki', 'Детки'),
    ('equipment', 'ВсеИнструменты'), ('kotofei', 'Котофей'),
]


def save(im, name, maxw, q=82):
    if im.mode != 'RGB':
        im = im.convert('RGB')
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(DST, name)
    im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)
    print('   %-22s %sx%s  %s КБ' % (name, im.width, im.height, os.path.getsize(p) // 1024))


def shoot(w, h, out, scale=1):
    cmd = [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
           '--virtual-time-budget=20000', '--window-size=%d,%d' % (w, h),
           '--screenshot=%s' % out, URL]
    if scale != 1:
        cmd.insert(-1, '--force-device-scale-factor=%d' % scale)
    subprocess.run(cmd, capture_output=True)
    if not os.path.exists(out):
        sys.exit('не сняли %s — поднят ли `npm run dev` и лежит ли public/_smilesrc/shot.html?' % out)
    print('   снято', os.path.basename(out), Image.open(out).size)


def make_shot_html():
    """Копия боевого index.html под съёмку: карта картинкой, анимации домотаны."""
    s = open(os.path.join(PUB, 'index.html'), encoding='utf-8').read()
    s = s.replace('<iframe src="https://www.google.com/maps/embed',
                  '<iframe data-src="https://www.google.com/maps/embed')
    s = s.replace('<div class="map">',
                  '<div class="map" style="background:url(./img/map.jpg) center/cover no-repeat">')
    s = s.replace('</body>', """
<script>
function hmShotDone(){['block2','block3','block4','block5','block8','block9']
  .forEach(function(id){var e=document.getElementById(id);if(e)e.classList.add('animation');});}
document.addEventListener('DOMContentLoaded',hmShotDone);
window.addEventListener('load',function(){setTimeout(hmShotDone,1200);});
</script></body>""")
    open(os.path.join(PUB, 'shot.html'), 'w', encoding='utf-8').write(s)


def cut(shot, blocks, prefix_ok, maxw=1200):
    im = Image.open(shot).convert('RGB')
    for name, (a, b) in blocks.items():
        b = min(b, im.height)
        save(im.crop((0, a, im.width, b)), '%s.jpg' % name, maxw)
    return im


def tenants():
    """Логотипы арендаторов: обрезаем белые поля, приводим к одной высоте."""
    out = os.path.join(DST, 'tenants')
    os.makedirs(out, exist_ok=True)
    for slug, _title in TENANTS:
        p = os.path.join(SRC, 'img', 'logo', '%s.jpg' % slug)
        im = Image.open(p).convert('RGB')
        # bbox по не-белому
        g = im.convert('L').point(lambda v: 0 if v > 244 else 255)
        box = g.getbbox()
        if box:
            im = im.crop((max(0, box[0] - 6), max(0, box[1] - 6),
                          min(im.width, box[2] + 6), min(im.height, box[3] + 6)))
        h = 96
        im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
        f = os.path.join(out, '%s.png' % slug.replace('.', '-'))
        im.save(f, 'PNG', optimize=True)
    print('   логотипы арендаторов:', len(TENANTS))


def brand():
    """Фирменные элементы самой посадочной."""
    shutil.copy(os.path.join(SRC, 'img', 'ball_smile.gif'), os.path.join(DST, 'smile-wink.gif'))
    Image.open(os.path.join(SRC, 'img', 'logo_big.png')).save(
        os.path.join(DST, 'logo-smile.png'), 'PNG', optimize=True)
    print('   smile-wink.gif, logo-smile.png')


def cover(hero_shot):
    """Обложка карточки каталога 477x396: ноутбук с первым экраном на бирюзовом круге.

    Старая обложка была подписана «Creative», хотя кейс лежит в Digital, — плашку
    убираем совсем: у соседних Digital-карточек (Invest, Vertical) её тоже нет.
    """
    W, H, CX, CY, R = 477, 396, 238, 190, 176
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.ellipse([CX - R, CY - R, CX + R, CY + R], fill=(42, 200, 187, 255))
    lap = Image.open(os.path.join(ROOT, 'mirror', 'case-assets',
                                  '56b95887_1814_-02.png')).convert('RGBA')
    w = 430
    lap = lap.resize((w, round(lap.height * w / lap.width)), Image.LANCZOS)
    base.alpha_composite(lap, (CX - w // 2, CY - lap.height // 2 + 6))
    out = os.path.join(ROOT, 'mirror', 'images', 'lib', 'custom-smile')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'cover.png')
    base.save(p, 'PNG', optimize=True)
    print('   обложка каталога:', p.replace(ROOT + '/', ''), os.path.getsize(p) // 1024, 'КБ')


def main():
    os.makedirs(DST, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    desk = os.path.join(TMP, 'desktop.png')
    mob = os.path.join(TMP, 'mobile.png')

    if '--no-shots' not in sys.argv:
        print('1. съёмка исходника')
        make_shot_html()
        shoot(DESK_W, DESK_H + 15, desk)
        shoot(MOB_W, MOB_H, mob)

    print('2. страница целиком (прокрутка внутри мокапа)')
    save(Image.open(desk).convert('RGB').crop((0, 0, DESK_W, DESK_H)), 'page-desktop.jpg', 1120, q=80)
    save(Image.open(mob).convert('RGB'), 'page-mobile.jpg', 500, q=78)

    print('3. экраны для разбора')
    cut(desk, BLOCKS, True)
    cut(mob, MOB_BLOCKS, True, maxw=500)

    print('4. фирменные элементы')
    brand()
    tenants()

    print('5. обложка каталога')
    cover(desk)

    print('\nготово →', DST.replace(ROOT + '/', ''))
    print('дальше: scripts/gen-webp.sh mirror/images/smile')


if __name__ == '__main__':
    main()
