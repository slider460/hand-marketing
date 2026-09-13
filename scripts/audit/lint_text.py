#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Детерминированный линтер текстов сайта + сборка брифов для агентов-ревьюеров.

    python3 scripts/audit/lint_text.py                 # линт всего, что снято
    python3 scripts/audit/lint_text.py event/changan   # одна страница

Читает scripts/audit/pages/*.json (снимает extract_text.py) и делает две вещи:

1. Линт без модели: мета, типографика, словарь ИИ-штампов, подписи-тавтологии,
   alt, объём текста, дубли между страницами, битые внутренние ссылки.
   → scripts/audit/lint.json + scripts/audit/lint.md

2. Бриф на каждую страницу: текст в порядке чтения, с номерами фрагментов
   и вырезанной шапкой-подвалом. Агенты ссылаются на F-номера, по ним правка
   находится в JSON и в источнике.
   → scripts/audit/briefs/<slug>.md

Общие для всего сайта фрагменты (шапка, подвал, фиолетовая форма, cookie)
определяются по частоте и в брифы страниц не попадают: они выносятся
в briefs/_common.md и правятся один раз.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
MIRROR = os.path.join(ROOT, 'mirror')
PAGES = os.path.join(HERE, 'pages')
BRIEFS = os.path.join(HERE, 'briefs')

TITLE_MIN, TITLE_MAX = 30, 70
DESC_MIN, DESC_MAX = 70, 180
COMMON_SHARE = 0.35          # фрагмент на 35%+ страниц = общий блок сайта

# Штампы. Не «запрещённые слова», а места, куда смотрит редактор.
CLICHE = [
    'в современном мире', 'в мире, где', 'играет важную роль', 'играет ключевую роль',
    'комплексный подход', 'комплексные решения', 'широкий спектр', 'полный спектр',
    'инновацион', 'уникальн', 'динамично развива', 'команда профессионалов',
    'индивидуальный подход', 'высококвалифицированн', 'на высшем уровне',
    'ключевую роль', 'важно отметить', 'стоит отметить', 'следует отметить',
    'таким образом', 'в конечном итоге', 'позволяет добиться', 'позволяет достичь',
    'широкие возможности', 'богатый опыт', 'многолетний опыт', 'лидер рынка',
    'не просто ', 'выходит за рамки', 'новый уровень', 'в кратчайшие сроки',
    'максимальн', 'оптимальн', 'эффективн', 'качественн', 'профессиональн',
    'мы предлагаем', 'мы гарантируем', 'наша компания', 'нашей компании',
    'современные технологии', 'широкий ассортимент', 'гибкая система',
    'воплотить в жизнь', 'под ключ', 'от идеи до реализации', 'полного цикла',
]
# Подпись, которая пересказывает кадр
CAPTION_TAUTOLOGY = [
    'на фото', 'на снимке', 'на изображении', 'на картинке', 'на кадре',
    'изображение ', 'фотография ', 'здесь видно', 'как видно', 'на этом фото',
    'фото:', 'кадр:', 'слева направо', 'общий вид', 'вид на ',
]
AI_PUNCT = {
    'длинное тире': re.compile(r'\s—\s|^—\s', re.M),
    'лапки вместо ёлочек': re.compile(r'"[^"]{2,60}"'),
    'двойной пробел': re.compile(r'[А-Яа-яЁёA-Za-z]  +[А-Яа-яЁёA-Za-z]'),
    'пробел перед знаком': re.compile(r'\s+[,.;:!?]'),
    # начало предложения не считаем: «Вы делаете дизайн?» это норма.
    # ловим вежливое обращение внутри фразы
    'заглавное Вы': re.compile(r'(?<=[а-яё,] )(?:Вы|Ваш[аиеуего]*)\b'),
    'три точки вместо многоточия': re.compile(r'\.\.\.'),
}
STOP = set('и в во не что он на я с со как а то все она так его но да ты к у же вы за бы по '
           'ее мне было вот от меня еще нет о из ему теперь когда даже ну вдруг ли если уже или '
           'ни быть был него до вас нибудь опять уж вам ведь там потом себя ничего ей может они '
           'тут где есть надо ней для мы тебя их чем была сам чтоб без будто чего раз тоже себе '
           'под будет ж тогда кто этот того потому этого какой совсем ним здесь этом один почти '
           'мой тем чтобы нее сейчас были куда зачем всех никогда можно при наконец два об другой '
           'хоть после над больше тот через эти нас про всего них какая много разве три эту моя '
           'впрочем хорошо свою этой перед иногда лучше чуть том нельзя такой им более всегда '
           'конечно всю между это как для все или'.split())


def load_pages(filter_path=None):
    out = []
    if not os.path.isdir(PAGES):
        sys.exit('Нет scripts/audit/pages/ — сначала extract_text.py --all')
    for fn in sorted(os.listdir(PAGES)):
        if not fn.endswith('.json'):
            continue
        d = json.load(open(os.path.join(PAGES, fn), encoding='utf-8'))
        if filter_path and d['path'] != filter_path:
            continue
        out.append(d)
    return out


def body_flow(d, common=frozenset()):
    """Поток страницы без шапки-подвала и без общесайтовых блоков."""
    out = []
    for it in d['flow']:
        if it.get('chrome'):
            continue
        t = it.get('text')
        if t and t in common:
            continue
        out.append(it)
    return out


def build_common(pages):
    cnt = Counter()
    for d in pages:
        seen = set()
        for it in d['flow']:
            t = it.get('text')
            if t and len(t) > 3 and t not in seen:
                seen.add(t)
                cnt[t] += 1
    need = max(3, int(len(pages) * COMMON_SHARE))
    return {t for t, c in cnt.items() if c >= need}, cnt


def norm_words(text):
    ws = re.findall(r'[А-Яа-яЁёA-Za-z]{3,}', text.lower())
    return [w for w in ws if w not in STOP]


def lint_page(d, common, all_pages, internal_paths):
    F = []
    flow = body_flow(d, common)
    text_items = [i for i in flow if i.get('text')]
    full = ' '.join(i['text'] for i in text_items)
    m = d['meta']

    def add(sev, cat, msg, frag=None):
        F.append({'sev': sev, 'cat': cat, 'msg': msg, 'frag': frag})

    # --- мета ---
    t = m.get('title') or ''
    if not t:
        add('красный', 'мета', 'нет title')
    else:
        if len(t) < TITLE_MIN:
            add('жёлтый', 'мета', f'title короткий ({len(t)} симв.): {t}')
        if len(t) > TITLE_MAX:
            add('жёлтый', 'мета', f'title длинный ({len(t)} симв.), в сниппете обрежется: {t}')
    ds = m.get('description') or ''
    if not ds:
        add('красный', 'мета', 'нет description')
    else:
        if len(ds) < DESC_MIN:
            add('жёлтый', 'мета', f'description короткий ({len(ds)} симв.)')
        if len(ds) > DESC_MAX:
            add('жёлтый', 'мета', f'description длинный ({len(ds)} симв.), обрежется')
    # og-теги: короткий og:description это норма (карточка в соцсетях),
    # а вот og:title, отставший от title, это почти всегда недосмотр
    ogt = (m.get('og_title') or '').strip()
    if ogt and t and ogt != t.strip():
        add('жёлтый', 'мета', f'og:title разошёлся с title: {ogt[:70]!r}')
    for label, val in (('title', t), ('description', ds), ('og:title', ogt),
                       ('og:description', (m.get('og_description') or ''))):
        if ' — ' in val or val.startswith('— '):
            add('красный', 'типографика', f'длинное тире в {label}')
    if m.get('keywords'):
        add('жёлтый', 'мета', 'есть meta keywords — поисковики их игнорируют, а переспам в них виден')
    can = m.get('canonical') or ''
    if can and d['path'] and not can.rstrip('/').endswith(d['path']):
        add('жёлтый', 'мета', f'canonical на другой адрес (страница-дубль отдаёт вес оригиналу, '
                              f'проверь, что так и задумано): {can}')

    # --- заголовки ---
    h1s = d.get('h1s') or []
    vis = [h for h in h1s if h.get('visible')]
    if not h1s:
        add('красный', 'структура', 'нет H1 вовсе')
    elif not vis:
        # sr-only H1 с релевантным текстом это обычная практика, а не нарушение.
        # Красным считаем только мусор: технические имена, одно латинское слово
        ht = h1s[0]['text']
        junk = ('_' in ht or re.fullmatch(r'[A-Za-z&;\s]{1,20}', ht or '')
                or len(ht) < 8)
        if junk:
            add('красный', 'структура', f'скрытый H1 с техническим текстом: {ht[:70]!r}')
        else:
            add('жёлтый', 'структура', f'H1 скрыт (sr-only), визуальный заголовок другой: {ht[:70]!r}')
    elif len(vis) > 1:
        add('жёлтый', 'структура', f'несколько видимых H1: {len(vis)} шт.')
    if vis and m.get('title') and vis[0]['text'].strip().lower() == (m['title'] or '').strip().lower():
        add('жёлтый', 'структура', 'H1 дословно повторяет title: один из них стоит написать для человека')

    # --- объём и графика ---
    wb = d['stats']['words_body']
    if wb < 120:
        add('красный', 'объём', f'мало текста: {wb} слов в теле страницы')
    elif wb < 250:
        add('жёлтый', 'объём', f'текста немного: {wb} слов')
    if d['stats'].get('canvas') and wb < 400:
        add('жёлтый', 'объём', f"смысл может жить в canvas ({d['stats']['canvas']} шт.) "
                               f"при {wb} словах текста — для поисковика страница почти пустая")

    # --- alt ---
    st = d['stats']
    if st['imgs_total'] and st['imgs_no_alt'] / st['imgs_total'] > 0.3:
        add('жёлтый', 'alt', f"без alt {st['imgs_no_alt']} из {st['imgs_total']} картинок")
    alts = [i['alt'] for i in d['imgs'] if i['alt'] and not i.get('deco')]
    dup_alt = [a for a, c in Counter(alts).items() if c > 2]
    if dup_alt:
        add('жёлтый', 'alt', f'alt повторяется дословно: {dup_alt[:2]}')

    # --- типографика ---
    for name, rx in AI_PUNCT.items():
        hay = re.sub(r'«[^»]{0,160}»', '', full) if name == 'заглавное Вы' else full
        hits = rx.findall(hay)
        if hits:
            sev = 'красный' if name in ('длинное тире', 'заглавное Вы') else 'жёлтый'
            add(sev, 'типографика', f'{name}: {len(hits)} шт., напр. {str(hits[0])[:60]!r}')

    # --- двоеточие на месте пропущенного глагола («Фильм: обычно 3–6 недель»),
    #     чаще всего остаётся после механической замены тире. Бессоюзное
    #     предложение с глаголом в одной из частей это законное двоеточие,
    #     перечисление после обобщающего слова тоже; заголовки и ярлыки не смотрим ---
    VERB = re.compile(r'[а-яё]{2,}(?:ет|ют|ут|ит|ят|ал|ала|ало|али|ил|ила|или|ел|ела|ели'
                      r'|ть|ться|ешь|ишь|ете|ите|ется|ются|ится|ятся|лся|лась|лись|ан|ян|ен|ён|ано|ены|аны|ты|та)\b', re.I)
    PREP = re.compile(r'(в|во|на|за|от|до|по|с|со|у|около|обычно|примерно|когда|если)\b', re.I)
    colon_bad = []
    for it in text_items:
        if it['role'] in ('heading', 'cta', 'link', 'metric', 'form'):
            continue
        for sent in re.split(r'(?<=[.!?])\s+', it['text']):
            if ': ' not in sent or sent.rstrip().endswith(':'):
                continue
            left, right = sent.split(': ', 1)
            if len(left.split()) < 3 or re.search(r'\d$', left):
                continue            # «Телефон: …», «Срок: …», тайм-коды
            if VERB.search(left) or VERB.search(right.split('. ')[0]):
                continue            # бессоюзное предложение
            # ловим главный случай: справа обстоятельство без глагола
            # («: обычно 3–6 недель», «: в студии и на объекте»)
            if PREP.match(right):
                colon_bad.append(sent[:80])
    if colon_bad:
        add('жёлтый', 'типографика',
            f'двоеточие на месте глагола: {len(colon_bad)} шт., напр. {colon_bad[0]!r}')

    # --- штампы ---
    low = full.lower()
    found = [c for c in CLICHE if c in low]
    if found:
        sev = 'красный' if len(found) >= 4 else 'жёлтый'
        add(sev, 'штампы', f'{len(found)} шт.: {", ".join(found[:6])}')

    # --- подписи ---
    # Подписью считаем только текст, идущий сразу за кадром и в том же контейнере.
    # Иначе на сетках карточек в пару попадает текст следующего раздела.
    caps = []
    for idx, it in enumerate(flow):
        if it['role'] != 'media' or idx + 1 >= len(flow):
            continue
        nxt = flow[idx + 1]
        if not nxt.get('text') or nxt['role'] not in ('caption', 'text', 'metric'):
            continue
        if len(nxt['text']) > 220:
            continue
        same_box = (it.get('sel', '').split('>')[:-1] == nxt.get('sel', '').split('>')[:-1]
                    or it.get('inFigure') and nxt.get('inFigure'))
        if same_box or nxt['role'] == 'caption':
            caps.append((idx, it, idx + 1, nxt))
    taut = [c for _, _m, _i, c in caps if any(k in c['text'].lower() for k in CAPTION_TAUTOLOGY)]
    if taut:
        add('красный', 'подписи', f'подпись пересказывает кадр: {len(taut)} шт., '
                                  f'напр. {taut[0]["text"][:70]!r}')
    # серии кадров вообще без слов
    run = 0
    silent = 0
    for it in flow:
        # сетка карточек-ссылок это навигация, а не немой фотоотчёт
        if it['role'] == 'media' and not it.get('href'):
            run += 1
        elif it['role'] == 'media':
            run = 0
        else:
            if run >= 4:
                silent += 1
            run = 0
    if run >= 4:
        silent += 1
    if silent:
        add('жёлтый', 'подписи', f'{silent} серии из 4+ кадров подряд без единого слова')

    # --- переспам ---
    ws = norm_words(full)
    if len(ws) > 120:
        top, n = Counter(ws).most_common(1)[0]
        share = n / len(ws)
        if share > 0.035:
            add('жёлтый', 'seo', f'слово «{top}» занимает {share*100:.1f}% текста ({n} раз) — похоже на переспам')

    # --- битые внутренние ссылки ---
    bad = []
    for l in d['links']:
        h = (l['href'] or '').split('#')[0].split('?')[0]
        if not h or ':' in h.split('/')[0] or h.startswith(('http', 'mailto:', 'tel:', 'javascript:', 'data:')):
            continue
        p = h.strip('/')
        if p and p not in internal_paths and not re.search(r'\.(html|pdf|jpg|png|webp|mp4|svg|ico|xml|txt)$', p):
            bad.append(h)
    for h in sorted(set(bad))[:5]:
        add('красный', 'ссылки', f'внутренняя ссылка в никуда: {h}')

    return F, flow, caps



def page_facts(d, limit=5):
    """Короткая выжимка страницы: чем она может подписать ведущий на неё кадр."""
    facts = []
    flow = [i for i in d['flow'] if not i.get('chrome')]
    h1 = next((i['text'] for i in flow if i['role'] == 'heading' and i.get('level') == 1), None)
    if h1:
        facts.append(('заголовок', h1))
    for idx, it in enumerate(flow):
        if len(facts) >= limit + 1:
            break
        t = it.get('text') or ''
        if not t or len(t) > 90:
            continue
        # цифра с расшифровкой в соседнем блоке — самая ходовая фактура кейса
        if re.search(r'\d', t) and it['role'] in ('metric', 'heading') and len(t) < 30:
            nxt = flow[idx + 1]['text'] if idx + 1 < len(flow) and flow[idx + 1].get('text') else ''
            facts.append(('цифра', f"{t} — {nxt[:70]}" if nxt and len(nxt) < 90 else t))
    return facts


def write_brief(d, flow, caps, by_path=None):
    os.makedirs(BRIEFS, exist_ok=True)
    m = d['meta']
    src = d['source']
    L = []
    L.append(f"# {d['path'] or '(главная)'}")
    L.append('')
    L.append(f"- URL: {d['url']}")
    L.append(f"- Править здесь: **{src['file']}** ({src['kind']})")
    if src['kind'] == 'generator':
        L.append("  после правки: `python3 scripts/a2/finalize_page.py " +
                 os.path.basename(src['file']) + "`")
    L.append(f"- Слов в теле: {d['stats']['words_body']}, кадров: {d['stats']['media']}, "
             f"canvas: {d['stats'].get('canvas', 0)}")
    L.append('')
    L.append('## Мета')
    L.append(f"- title ({len(m.get('title') or '')} из {TITLE_MAX} допустимых): {m.get('title')}")
    L.append(f"- description ({len(m.get('description') or '')}, норма {DESC_MIN}-{DESC_MAX}): "
             f"{m.get('description')}")
    L.append(f"- canonical: {m.get('canonical')}")
    L.append('')
    L.append('Мета, H1 и первый абзац несут поиск: в них сохраняем название услуги '
             'тем же словом и держим длину в норме.')
    L.append('')
    L.append('## Текст в порядке чтения')
    L.append('')
    L.append('Формат: `F<номер> [роль]` — ссылайся в отчёте на этот номер. '
             'Без пометки фрагмент виден везде; `(desktop)` или `(mobile)` значит, '
             'что он есть только в этой версии. У кадров `→` показывает, куда ведёт клик.')
    L.append('')
    n = 0
    first_para_done = False
    for it in flow:
        n += 1
        vp = it.get('vp', 'both')
        vps = '' if vp == 'both' else f' ({vp})'
        if it['role'] == 'media':
            alt = it.get('alt') or ''
            alt = f' alt="{alt}"' if alt else ' alt=ПУСТОЙ'
            href = (f" →{it['href']}" if it.get('href')
                    else (f" →[{it['action']}, перехода нет]" if it.get('action') else ''))
            L.append(f"F{n:03d} [кадр {it['tag']} {it.get('w')}×{it.get('h')}]{alt} "
                     f"{os.path.basename(it.get('src') or '')}{href}{vps}")
        else:
            seo = ''
            if it.get('level') == 1:
                seo = ' [несёт поиск]'
            elif it['role'] == 'text' and n <= 8 and len(it['text']) > 60 and not first_para_done:
                seo = ' [несёт поиск]'
                first_para_done = True
            role = {'heading': 'ЗАГОЛОВОК', 'caption': 'подпись', 'cta': 'КНОПКА',
                    'metric': 'цифра', 'form': 'форма', 'link': 'ссылка',
                    'text': 'текст'}.get(it['role'], it['role'])
            lvl = f"H{it['level']}" if it.get('level') else ''
            L.append(f"F{n:03d} [{role}{(' ' + lvl) if lvl else ''}]{seo}{vps} {it['text']}")
    L.append('')
    if caps:
        L.append('## Пары «кадр → подпись» (сюда смотрит caption-critic)')
        L.append('')
        for mi, mm, ci, cc in caps:
            href = f" → ведёт на {mm['href']}" if mm.get('href') else ''
            L.append(f"- F{mi+1:03d} `{os.path.basename(mm.get('src') or 'canvas')}`{href}"
                     f"  |  F{ci+1:03d} подпись: {cc['text'][:160]}")
        L.append('')
    # чем подписать кадры-двери: выжимка со страниц, куда они ведут
    targets = []
    for it in flow:
        h = (it.get('href') or '').strip('/')
        if not h or not by_path or h not in by_path or h == d['path']:
            continue
        if h not in [t[0] for t in targets]:
            targets.append((h, by_path[h]))
    if targets:
        L.append('## Что лежит за ссылками с этой страницы')
        L.append('')
        L.append('Факты взяты с целевых страниц. Ими можно подписывать кадры-двери, '
                 'не выдумывая ничего нового.')
        L.append('')
        for h, td in targets[:24]:
            fs = page_facts(td)
            if not fs:
                continue
            L.append(f"- **/{h}/**")
            for kind, txt in fs:
                L.append(f"  - {kind}: {txt}")
        L.append('')

    path = os.path.join(BRIEFS, d['slug'] + '.md')
    open(path, 'w', encoding='utf-8').write('\n'.join(L))
    return path


def main():
    arg = sys.argv[1].strip('/') if len(sys.argv) > 1 else None
    pages = load_pages()
    if not pages:
        sys.exit('pages/ пуст')
    common, cnt = build_common(pages)
    # существующие пути берём из зеркала, а не из снятых страниц:
    # иначе при частичном прогоне живые ссылки выглядят битыми
    internal = set()
    for dirpath, _dirs, files in os.walk(MIRROR):
        rel = os.path.relpath(dirpath, MIRROR)
        rel = '' if rel == '.' else rel.replace(os.sep, '/')
        if 'index.html' in files:
            internal.add(rel)
        for fn in files:
            if fn.endswith('.html'):
                internal.add((rel + '/' + fn[:-5]).lstrip('/'))
                internal.add((rel + '/' + fn).lstrip('/'))

    # общие блоки — отдельным брифом, правятся один раз на весь сайт
    os.makedirs(BRIEFS, exist_ok=True)
    with open(os.path.join(BRIEFS, '_common.md'), 'w', encoding='utf-8') as f:
        f.write('# Общие блоки сайта (шапка, подвал, форма, cookie)\n\n')
        f.write(f'Фрагменты, встречающиеся минимум на {int(len(pages)*COMMON_SHARE)} '
                f'из {len(pages)} страниц. Правятся один раз.\n\n')
        for t in sorted(common, key=lambda x: -cnt[x]):
            f.write(f'- ({cnt[t]}×) {t}\n')

    target = [d for d in pages if arg is None or d['path'] == arg]
    report = {}
    # дубли мета по всему сайту
    tt, dd = defaultdict(list), defaultdict(list)
    for d in pages:
        if d['meta'].get('title'):
            tt[d['meta']['title']].append(d['path'])
        if d['meta'].get('description'):
            dd[d['meta']['description']].append(d['path'])

    by_path = {x['path']: x for x in pages}
    for d in target:
        F, flow, caps = lint_page(d, common, pages, internal)
        # дубль-заглушка с canonical на оригинал оформлена правильно: не штрафуем
        # ни её, ни оригинал, на который она указывает
        def canon_of(x):
            return (x['meta'].get('canonical') or '').split('hand-marketing.ru')[-1].strip('/')
        def dup_ok(others):
            for o in others:
                od = by_path.get(o)
                if od is None:
                    return False
                if not (canon_of(od) == d['path'] or canon_of(d) == o):
                    return False
            return True
        t = d['meta'].get('title')
        if t and len(tt[t]) > 1 and not dup_ok([x for x in tt[t] if x != d['path']]):
            F.append({'sev': 'красный', 'cat': 'мета',
                      'msg': f'title дублируется на: {", ".join(p or "(главная)" for p in tt[t] if p != d["path"])}',
                      'frag': None})
        ds = d['meta'].get('description')
        if ds and len(dd[ds]) > 1 and not dup_ok([x for x in dd[ds] if x != d['path']]):
            F.append({'sev': 'красный', 'cat': 'мета',
                      'msg': f'description дублируется на: {", ".join(p or "(главная)" for p in dd[ds] if p != d["path"])}',
                      'frag': None})
        report[d['path']] = F
        write_brief(d, flow, caps, by_path={p['path']: p for p in pages})

    json.dump(report, open(os.path.join(HERE, 'lint.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    # сводка
    L = ['# Линт текстов сайта', '',
         f'Страниц: {len(target)}. Общих блоков сайта: {len(common)} (см. briefs/_common.md)', '']
    tot = Counter()
    for p, F in sorted(report.items(), key=lambda kv: -len([f for f in kv[1] if f['sev'] == 'красный'])):
        if not F:
            continue
        red = len([f for f in F if f['sev'] == 'красный'])
        L.append(f"## {p or '(главная)'} — красных {red}, жёлтых {len(F)-red}")
        for f in F:
            tot[f['cat']] += 1
            mark = '🔴' if f['sev'] == 'красный' else '🟡'
            L.append(f"- {mark} **{f['cat']}** {f['msg']}")
        L.append('')
    L.insert(3, 'По категориям: ' + ', '.join(f'{k} {v}' for k, v in tot.most_common()) + '\n')
    open(os.path.join(HERE, 'lint.md'), 'w', encoding='utf-8').write('\n'.join(L))

    red = sum(len([f for f in F if f['sev'] == 'красный']) for F in report.values())
    yel = sum(len([f for f in F if f['sev'] != 'красный']) for F in report.values())
    print(f'Страниц: {len(target)}. Находок: 🔴 {red}, 🟡 {yel}')
    print(f'  {os.path.relpath(os.path.join(HERE, "lint.md"), ROOT)}')
    print(f'  брифы: {os.path.relpath(BRIEFS, ROOT)}/')
    for k, v in tot.most_common():
        print(f'    {k:14s} {v}')


if __name__ == '__main__':
    main()
