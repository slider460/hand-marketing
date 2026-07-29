#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Фикс каталога кейсов на /digital (29.07.2026, жалоба пользователя: «идут две
пары кейсов»).

Корень: на странице два t786-каталога, как и на остальных категориях, но device
visibility проставлена только у одного. Десктопный rec250597283 помечен
t-screenmin-980px, а планшетный rec248666862 остался без ограничения и потому
показывается на всех ширинах. Пока каталоги были подключены к разным сторпартам,
это выглядело как «кейсы в двух стилистиках» (см. fix_digital_catalog.py), после
того фикса оба тянут один набор и список кейсов честно дублируется.

Правильная пара стоит на /3dmapping: t-screenmax-980px + t-screenmin-980px.
Приводим /digital к ней.

Заодно меняем обложку карточки «ТРЦ Смайл»: на старой стояла плашка «Creative»,
хотя кейс живёт в Digital. Новая (scripts/smile-assets.py) собрана в стилистике
соседних Digital-карточек: ноутбук с первым экраном на бирюзовом круге.

Идемпотентно.
"""
import io
import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
REC = "rec248666862"                      # планшетный каталог без ограничения
COVER = "/images/lib/custom-smile/cover.png"
CATALOGS = ("getproductslist_750728959451.json",   # набор Digital
            "getproductslist_950070406371.json",   # общий каталог /project
            "getproductslist.json")                # полный дамп

# ── 1. device visibility планшетного каталога ────────────────────────────────
for base in ("index.html", "index-a2.html"):
    p = os.path.join(ROOT, "mirror", "digital", base)
    if not os.path.exists(p):
        continue
    h = io.open(p, encoding="utf-8").read()
    m = re.search(r'<div id="%s" class="([^"]*)"([^>]*)>' % REC, h)
    if not m:
        print("%s: блок %s не найден" % (base, REC))
        continue
    if "t-screenmax-980px" in m.group(1):
        print("%s: уже поправлено" % base)
        continue
    old = m.group(0)
    new = old.replace('class="%s"' % m.group(1),
                      'class="%s t-screenmax-980px"' % m.group(1))
    if 'data-screen-max' not in new:
        new = new.replace('data-record-type="786"',
                          'data-record-type="786" data-screen-max="980px"')
    h = h.replace(old, new, 1)
    io.open(p, "w", encoding="utf-8").write(h)
    print("%s: %s спрятан на десктопе" % (base, REC))

# ── 2. обложка карточки «ТРЦ Смайл» ──────────────────────────────────────────
for name in CATALOGS:
    p = os.path.join(ROOT, "mirror", "api", name)
    if not os.path.exists(p):
        continue
    d = json.load(io.open(p, encoding="utf-8"))
    hit = False
    for prod in d.get("products", []):
        if prod.get("url") != "/digital/becar/smile":
            continue
        prod["gallery"] = json.dumps([{"img": COVER}]).replace("/", "\\/")
        if prod.get("editions"):
            prod["editions"] = [dict(prod["editions"][0], img=COVER)]
        # кавычки-лапки в подписи карточки на ёлочки
        if prod.get("descr"):
            prod["descr"] = prod["descr"].replace('"ТРЦ Смайл"', "«ТРЦ Смайл»")
        hit = True
    if hit:
        io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
        print("%s: обложка и подпись обновлены" % name)
