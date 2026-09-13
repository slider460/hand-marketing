#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Живая выдача Яндекса и Google через XMLRiver: что показывают по нашим запросам,
где стоит сайт, не конкурируют ли между собой две наши страницы.

    python3 scripts/audit/serp.py top "видеопродакшн" --lr 213
    python3 scripts/audit/serp.py pos "видеопродакшн москва" --lr 213
    python3 scripts/audit/serp.py pos --file scripts/audit/queries.txt --lr 213 --csv out.csv
    python3 scripts/audit/serp.py ask "видеопродакшн"        # похожие запросы и вопросы
    python3 scripts/audit/serp.py balance

Доступы (получить на https://xmlriver.com/queries/) кладутся в файлы,
в git не попадают:
    mkdir -p ~/.config/xmlriver
    printf '%s' 'ВАШ_USER_ID' > ~/.config/xmlriver/user
    printf '%s' 'ВАШ_KEY'     > ~/.config/xmlriver/key
    chmod 600 ~/.config/xmlriver/*
Либо переменные окружения XMLRIVER_USER и XMLRIVER_KEY.

Расход: один запрос это одна поисковая выдача. По прайсу 25 ₽ за 1000,
то есть весь аудит сайта укладывается в несколько рублей. Тем не менее
результаты кэшируются в scripts/audit/serp-cache/, повторный тот же запрос
денег не стоит.
"""
import csv
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
CACHE = os.path.join(HERE, 'serp-cache')
CONF = os.path.expanduser('~/.config/xmlriver')
OUR = 'hand-marketing.ru'

ENDPOINT = {
    'yandex': 'https://xmlriver.com/search_yandex/xml',
    'google': 'https://xmlriver.com/search/xml',
}


def creds():
    user = os.environ.get('XMLRIVER_USER')
    key = os.environ.get('XMLRIVER_KEY')
    if not user and os.path.isfile(os.path.join(CONF, 'user')):
        user = open(os.path.join(CONF, 'user'), encoding='utf-8').read().strip()
    if not key and os.path.isfile(os.path.join(CONF, 'key')):
        key = open(os.path.join(CONF, 'key'), encoding='utf-8').read().strip()
    if not user or not key:
        sys.exit('Нет доступов XMLRiver. Положи user и key в ~/.config/xmlriver/ '
                 '(см. шапку файла) или задай XMLRIVER_USER и XMLRIVER_KEY.')
    return user, key


def fetch(query, engine='yandex', lr=213, groupby=10, extra=None, fresh=False):
    user, key = creds()
    params = {'user': user, 'key': key, 'query': query, 'groupby': groupby}
    if engine == 'yandex':
        params.update({'lr': lr, 'lang': 'ru', 'domain': 'ru'})
    else:
        params.update({'lr': 'RU', 'country': 2008, 'domain': 10, 'device': 'desktop'})
    if extra:
        params.update(extra)

    ck = hashlib.md5(f'{engine}|{query}|{lr}|{groupby}|{extra}'.encode()).hexdigest()
    os.makedirs(CACHE, exist_ok=True)
    cf = os.path.join(CACHE, ck + '.xml')
    if os.path.isfile(cf) and not fresh:
        return open(cf, encoding='utf-8').read()

    url = ENDPOINT[engine] + '?' + urllib.parse.urlencode(params)
    # 500 «выполните перезапрос» у них штатная ситуация: поисковик не ответил,
    # деньги не списываются, надо просто повторить
    RETRY_CODES = {'500', '15', '111', '100'}
    body = ''
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                body = r.read().decode('utf-8', 'replace')
        except Exception as e:
            if attempt == 4:
                sys.exit(f'XMLRiver не ответил: {e}')
            time.sleep(3 + attempt * 3)
            continue
        code = None
        if '<error' in body:
            try:
                el = ET.fromstring(body).find('.//error')
                code = el.get('code') if el is not None else None
            except ET.ParseError:
                code = None
        if code in RETRY_CODES and attempt < 4:
            time.sleep(3 + attempt * 4)
            continue
        break
    if '<error' in body:
        try:
            code = ET.fromstring(body).find('.//error')
            print(f'  ! ошибка API: {code.get("code")} {code.text}', file=sys.stderr)
        except ET.ParseError:
            print(f'  ! ошибка API: {body[:200]}', file=sys.stderr)
        return body
    open(cf, 'w', encoding='utf-8').write(body)
    return body


def parse(body):
    """Разбирает ответ в список позиций: (позиция, домен, url, заголовок)."""
    out = []
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return out
    n = 0
    for doc in root.iter('doc'):
        url = (doc.findtext('url') or '').strip()
        if not url:
            continue
        n += 1
        title = ''.join(doc.find('title').itertext()).strip() if doc.find('title') is not None else ''
        host = urllib.parse.urlparse(url).netloc.replace('www.', '')
        out.append((n, host, url, title))
    return out


def fetch_deep(query, engine='yandex', lr=213, depth=100, stop_on=None):
    """XMLRiver отдаёт ~10 результатов на запрос, глубину набираем страницами (page с нуля).
    Нумерация сквозная. stop_on — домен: как только он найден, дальше не листаем (экономия)."""
    out = []
    for pg in range((depth + 9) // 10):
        rows = parse(fetch(query, engine, lr, groupby=10, extra={'page': pg}))
        if not rows:
            break
        for _n, host, url, title in rows:
            out.append((len(out) + 1, host, url, title))
        if stop_on and any(stop_on in h for _n, h, _u, _t in rows):
            break
    return out


def extras(body):
    """Похожие запросы и «люди спрашивают», если пришли в ответе."""
    rel, ask = [], []
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return rel, ask
    for tag, bucket in (('related', rel), ('relatedsearch', rel),
                        ('question', ask), ('relatedquestion', ask)):
        for el in root.iter(tag):
            t = ' '.join(el.itertext()).strip()
            if t and t not in bucket:
                bucket.append(t)
    return rel, ask


def cmd_top(args):
    q = next(a for i, a in enumerate(args) if not a.startswith('--') and not (i and args[i-1].startswith('--')))
    lr = int(opt(args, '--lr', 213))
    eng = opt(args, '--engine', 'yandex')
    rows = parse(fetch(q, eng, lr, groupby=int(opt(args, '--num', 10))))
    print(f'\n{eng} lr={lr}  «{q}»  найдено {len(rows)}\n')
    for n, host, url, title in rows:
        mark = ' ◀ МЫ' if OUR in host else ''
        print(f'{n:3d}. {host:34s} {title[:70]}{mark}')
        if OUR in host:
            print(f'     {url}')


def cmd_pos(args):
    lr = int(opt(args, '--lr', 213))
    eng = opt(args, '--engine', 'yandex')
    f = opt(args, '--file', None)
    # значения опций (--lr 213, --engine yandex) запросами не считаем
    taken = {i + 1 for i, a in enumerate(args) if a.startswith('--')}
    free = [a for i, a in enumerate(args) if not a.startswith('--') and i not in taken]
    queries = free if not f else [
        l.strip() for l in open(f, encoding='utf-8') if l.strip() and not l.startswith('#')]
    out = []
    for q in queries:
        rows = fetch_deep(q, eng, lr, depth=int(opt(args, '--num', 50)), stop_on=OUR)
        ours = [(n, url) for n, host, url, _t in rows if OUR in host]
        top3 = ', '.join(h for _n, h, _u, _t in rows[:3])
        if ours:
            pos = ours[0][0]
            second = f'  (ещё наших URL: {len(ours)-1})' if len(ours) > 1 else ''
            print(f'{pos:4d}  {q:45s} {ours[0][1]}{second}')
        else:
            pos = ''
            print(f'  —   {q:45s} нет в топ-{opt(args, "--num", 50)}   топ: {top3}')
        out.append({'запрос': q, 'позиция': pos,
                    'url': ours[0][1] if ours else '',
                    'наших_в_топе': len(ours), 'топ3': top3})
    csvp = opt(args, '--csv', None)
    if csvp:
        with open(csvp, 'w', encoding='utf-8-sig', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
            w.writeheader()
            w.writerows(out)
        print(f'\n→ {csvp}')
    dup = [r for r in out if r['наших_в_топе'] > 1]
    if dup:
        print(f'\nКаннибализация ({len(dup)}): по этим запросам в выдаче больше одной нашей страницы')
        for r in dup:
            print(f"  {r['запрос']}")


def cmd_ask(args):
    q = args[0]
    lr = int(opt(args, '--lr', 213))
    eng = opt(args, '--engine', 'yandex')
    body = fetch(q, eng, lr, extra={'additional': 'related_questions,related_searches'})
    rel, ask = extras(body)
    print(f'\nПохожие запросы ({len(rel)}):')
    for t in rel:
        print('  ·', t)
    print(f'\nЛюди спрашивают ({len(ask)}):')
    for t in ask:
        print('  ·', t)
    if not rel and not ask:
        print('  (в ответе не пришли; возможно, нужен параметр additional на тарифе)')


def cmd_balance(_args):
    user, key = creds()
    url = f'https://xmlriver.com/api/get_balance/?user={user}&key={key}'
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            print('Баланс:', r.read().decode('utf-8', 'replace').strip())
    except Exception as e:
        print('Не удалось получить баланс:', e)


def opt(args, name, default=None):
    return args[args.index(name) + 1] if name in args else default


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    {'top': cmd_top, 'pos': cmd_pos, 'ask': cmd_ask, 'balance': cmd_balance}.get(
        cmd, lambda a: sys.exit(f'Неизвестная команда: {cmd}'))(args)


if __name__ == '__main__':
    main()
