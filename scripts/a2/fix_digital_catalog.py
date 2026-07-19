#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Фикс каталога кейсов на /digital (19.07.2026, жалоба пользователя: «кейсы в двух
стилистиках + к диджиталу относятся только сайты, а не вёрстки брошюр»).

Корень: десктопный t786-каталог rec250597283 (виден ≥980px) был подключён к
сторпарту 573067849371 — это набор категории КРЕАТИВ (14 позиций с брошюрами),
а планшетный rec248666862 — к правильному Digital-набору 750728959451 (сайты).
Отсюда на десктопе брошюры и «другая стилистика».

Правки (идемпотентно):
1) mirror/digital/index.html + index-a2.html: в опциях rec250597283
   storepart 573067849371 -> 750728959451.
2) mirror/api/getproductslist_750728959451.json: добавлен кейс
   /digital/becar/vertical (посадочная «Бутик-отель Vertical» — сайт, был в
   мобильной карусели и общем каталоге, но отсутствовал в Digital-наборе);
   запись копируется из getproductslist.json, total пересчитывается.
"""
import io, json, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
WRONG, RIGHT = "573067849371", "750728959451"
REC = "250597283"

# --- 1. HTML: сторпарт десктопного каталога ---
for base in ("index.html", "index-a2.html"):
    p = os.path.join(ROOT, "mirror", "digital", base)
    if not os.path.exists(p):
        continue
    h = io.open(p, encoding="utf-8").read()
    # правим ТОЛЬКО в пределах скрипта инициализации rec250597283
    i = h.find("'%s'" % REC)
    n = 0
    if i > 0 and WRONG in h:
        # все вхождения неправильного uid на странице относятся к этому стору
        n = h.count(WRONG)
        h = h.replace(WRONG, RIGHT)
        io.open(p, "w", encoding="utf-8").write(h)
    print("%s: заменено вхождений %d" % (base, n))

# --- 2. JSON: добавить /digital/becar/vertical в Digital-набор ---
jp = os.path.join(ROOT, "mirror", "api", "getproductslist_%s.json" % RIGHT)
d = json.load(io.open(jp, encoding="utf-8"))
urls = [x.get("url") for x in d["products"]]
if "/digital/becar/vertical" in urls:
    print("vertical уже в наборе")
else:
    full = json.load(io.open(os.path.join(ROOT, "mirror", "api", "getproductslist.json"), encoding="utf-8"))
    src = next(x for x in full["products"] if x.get("url") == "/digital/becar/vertical")
    src = dict(src)
    # заголовок/описание/обложка в стиле остальных карточек Digital-набора
    # (в общем каталоге title пуст, а обложка — красный круг, выбивается из мокапов)
    cover = "/images/lib/as3462-6263-4765-b137-646564356534/__-66.png"   # как в моб. карусели
    src["title"] = "Becar"
    src["text"] = "Digital"
    src["descr"] = "Посадочная страница «Бутик-отель Vertical»"
    src["gallery"] = json.dumps([{"img": cover}]).replace("/", "\\/")
    if src.get("editions"):
        src["editions"] = [dict(src["editions"][0], img=cover)]
    # partuids: пометить принадлежность к набору
    try:
        pu = json.loads(src.get("partuids") or "[]")
        if int(RIGHT) not in pu:
            pu.append(int(RIGHT))
        src["partuids"] = json.dumps(pu)
    except Exception:
        pass
    # вставить после smile (сохранить логичный порядок Becar-кейсов)
    idx = next((k for k, x in enumerate(d["products"]) if x.get("url") == "/digital/becar/smile"), len(d["products"]) - 1)
    d["products"].insert(idx + 1, src)
    d["total"] = len(d["products"])
    io.open(jp, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
    print("vertical добавлен, total =", d["total"])
