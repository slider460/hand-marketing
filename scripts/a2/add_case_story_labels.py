#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ярлыки «Компания / Задача / Решение / Результат» в мобильных версиях кейсов
(маркер hm-story-lbl). Жалоба: в .mh-story абзацы идут сплошняком, хотя на
десктопе каждый текст стоит под своим ярлыком уникальной вёрстки.

Скрипт для 30 кейс-страниц (все категории, кроме creative/* — там середина уже
реконструирована gen_creative_mobile.py — и portfolio/* — React):
1) парсит десктопный Zero-артборд (та же логика, что gen_creative_mobile);
2) строит соответствие «текст -> ярлык» (ярлык = ближайший заголовок-слово
   Компания/Задача(и)/Решение/Результат над/рядом с текстом в потоке чтения);
3) каждому <p> из .mh-story ищет пару среди десктопных текстов (нормализованный
   префикс, затем difflib) и вставляет ярлык перед первым абзацем каждой группы.
Абзацы без уверенного соответствия не трогаются. Идемпотентен (повторный прогон
снимает старые ярлыки и ставит заново).
"""
import difflib, glob, io, importlib.util, json, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MARK = "hm-story-lbl"

spec = importlib.util.spec_from_file_location("gcm", os.path.join(ROOT, "scripts", "a2", "gen_creative_mobile.py"))
gcm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gcm)

LBL = re.compile(r"^(Компания|Клиент|Задач(?:а|и)?|Решение|Результат(?:ы)?|Техническое решение)\b", re.I)

CSS = ('<style data-%s="css">@media (max-width:640px){'
       '.mh-slbl{font-family:\'Montserrat\',Arial,sans-serif;font-weight:800;font-size:21px;'
       'letter-spacing:-.02em;color:var(--ink,#14171C);padding:0;margin:18px 0 2px}'
       '.mh-story p:first-child{margin-top:0}}</style>' % MARK)


def norm(s):
    s = re.sub(r"[«»\"'’()\[\]]", "", s or "")
    return re.sub(r"\W+", " ", s.lower()).strip()


def desk_pairs(html):
    """[(ярлык, норм-текст)] из десктопных Zero-артбордов."""
    j = html.find('id="allrecords"')
    desk = html[j:]
    recs = [(m.group(1), m.group(2), m.start())
            for m in re.finditer(r'<div id="rec(\d+)"[^>]*data-record-type="(\d+)"', desk)]
    pairs = []
    for k, (rid, rt, pos) in enumerate(recs):
        if rt != "396" or k == 0 or k == len(recs) - 1:
            continue
        end = recs[k+1][2] if k+1 < len(recs) else len(desk)
        els = gcm.parse_zero(desk[pos:end], rid, [])
        txts = [e for e in els if e["kind"] == "txt"]
        labels = [(LBL.match(e["plain"].strip()).group(1).capitalize(), e)
                  for e in txts if e.get("fs", 0) >= 24 and LBL.match(e["plain"].strip())]
        # каждому обычному тексту — ближайший ярлык сверху в его колонке
        for t in txts:
            if t.get("fs", 0) >= 18 or len(t["plain"]) < 25:
                continue   # заголовки и лиды-подзаголовки (fs 18-23) — не абзацы повествования
            # ярлык «привязан» к началу текста: его левый ИЛИ правый край у левого
            # края текста (обычный над текстом / повёрнутый вплотную слева)
            best, best_key = None, None
            for name, L in labels:
                if L["top"] > t["top"] + 150:
                    continue
                dx = min(abs(L["left"] - t["left"]), abs(L["left"] + L["w"] - t["left"]))
                dy = abs(t["top"] - L["top"])
                key = (dx + dy, -L["top"])
                if best is None or key < best_key:
                    best, best_key = (name, L), key
            if best:
                pairs.append((best[0], norm(t["plain"])))
    return pairs


def label_for(p_text, pairs):
    t = norm(re.sub(r"<[^>]+>", " ", p_text))
    if len(t) < 25:
        return None
    for lbl, dt in pairs:
        if dt[:30] and (t[:30] == dt[:30] or t[:30] in dt or dt[:30] in t):
            return lbl
    best, bl = 0, None
    for lbl, dt in pairs:
        r = difflib.SequenceMatcher(None, t[:160], dt[:160]).ratio()
        if r > best:
            best, bl = r, lbl
    return bl if best >= 0.75 else None


def patch(path):
    html = io.open(path, encoding="utf-8").read()
    orig = html
    # снять прежние ярлыки/стили
    html = re.sub(r'<div class="mh-slbl" data-%s>.*?</div>' % MARK, "", html)
    html = re.sub(r'<style data-%s="css">.*?</style>' % MARK, "", html, flags=re.S)

    st = re.search(r'(<section class="mh-sec mh-story">)(.*?)(</section>)', html, re.S)
    if not st:
        return False, "нет mh-story"
    pairs = desk_pairs(html)
    if not pairs:
        return False, "нет пар на десктопе"

    body = st.group(2)
    out, used = [], set()
    labeled = 0
    for pm in re.finditer(r"<p>(.*?)</p>", body, re.S):
        lbl = label_for(pm.group(1), pairs)
        if lbl and lbl not in used:
            used.add(lbl)
            out.append('<div class="mh-slbl" data-%s>%s</div>' % (MARK, lbl))
            labeled += 1
        out.append("<p>%s</p>" % pm.group(1))
    if labeled < 2:      # один ярлык погоды не делает, а риск ошибки есть
        return False, "мало уверенных пар (%d)" % labeled
    html = html[:st.start()] + st.group(1) + CSS + "".join(out) + st.group(3) + html[st.end():]

    if html != orig:
        io.open(path, "w", encoding="utf-8").write(html)
        return True, "ярлыков: %d (%s)" % (labeled, ", ".join(sorted(used)))
    return False, "без изменений"


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    cases = json.load(open(os.path.join(ROOT, "src", "data", "cases.json"), encoding="utf-8"))
    routes = [c["route"].strip("/") for c in cases
              if not c["route"].strip("/").startswith(("creative/", "portfolio"))]
    n = 0
    for r in sorted(set(routes)):
        if r == "samara_vdnh":
            continue
        p = os.path.join(ROOT, "mirror", r, "index-a2.html")
        if not os.path.exists(p):
            continue
        if dry:
            html = io.open(p, encoding="utf-8").read()
            pairs = desk_pairs(html)
            st = re.search(r'<section class="mh-sec mh-story">(.*?)</section>', html, re.S)
            res = []
            if st:
                for pm in re.finditer(r"<p>(.*?)</p>", st.group(1), re.S):
                    res.append(label_for(pm.group(1), pairs) or "—")
            print("%-28s %s" % (r, " | ".join(res)))
        else:
            ok, msg = patch(p)
            n += ok
            print("%-28s %s" % (r, msg))
    if not dry:
        print("изменено:", n)
