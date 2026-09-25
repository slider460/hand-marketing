#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финализация кастомной страницы одной командой (вместо ручной цепочки
«генератор → add_cookie_consent → add_metrika_goals → откат чужих файлов → sitemap»):

    python3 scripts/a2/finalize_page.py gen_riviera.py

Шаги:
1. Снимок изменённых файлов (git) до запуска.
2. Прогон генератора.
3. Пост-скрипты add_cookie_consent.py + add_metrika_goals.py
   (их блоки живут в готовом HTML и затираются регенерацией).
4. Откат файлов, которые тронули ТОЛЬКО пост-скрипты (чужие страницы) —
   в коммит уходит одна своя страница.
5. Sitemap хирургически: lastmod=сегодня своей странице; если URL новой
   страницы нет — добавляется (полный npm run sitemap НЕ гоняется, чтобы
   не уплыли lastmod остальных страниц из-за смены mtime).
6. Контроль: маркеры hm-cookie-consent, hm-metrika-goals и счётчик Метрики
   на каждой сгенерированной странице. Код возврата 1, если чего-то нет.
"""
import datetime
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
MIRROR = os.path.join(ROOT, 'mirror')
SITEMAP = os.path.join(MIRROR, 'sitemap.xml')
POSTSCRIPTS = ['add_cookie_consent.py', 'add_metrika_goals.py',
               # блок «Похожие проекты»: без него свежесобранный кейс снова
               # становится тупиком без внутренних ссылок
               'add_related_links.py',
               # ссылки шапки и подвала сразу на адрес со слэшем, без 301;
               # идёт последним, чтобы поймать и ссылки блока «Похожие проекты»
               'fix_internal_slashes.py']
MARKERS = ['hm-cookie-consent', 'hm-metrika-goals', 'mc.yandex']


def git_status():
    out = subprocess.run(['git', 'status', '--porcelain', '--', 'mirror'],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    files = {}
    for line in out.splitlines():
        path = line[3:].strip().strip('"')
        if ' -> ' in path:
            path = path.split(' -> ')[1]
        files[path] = line[:2]
    return files


def git_dirty():
    return set(git_status())


def git_deleted():
    return {p for p, st in git_status().items() if 'D' in st}


def page_mtimes():
    out = {}
    for dirpath, _, files in os.walk(MIRROR):
        for f in files:
            if f in ('index.html', 'index-a2.html'):
                p = os.path.join(dirpath, f)
                out[p] = os.stat(p).st_mtime_ns
    return out


def run(script_path):
    print(f'\n▶ {os.path.relpath(script_path, ROOT)}', flush=True)
    r = subprocess.run([sys.executable, script_path], cwd=ROOT)
    if r.returncode != 0:
        sys.exit(f'✗ {os.path.basename(script_path)} упал с кодом {r.returncode}')


def resolve_generator(arg):
    name = os.path.basename(arg)
    if not name.endswith('.py'):
        name += '.py'
    for cand in (os.path.join(ROOT, arg), os.path.join(HERE, name)):
        if os.path.isfile(cand):
            return cand
    sys.exit(f'✗ генератор не найден: {arg} (искал в scripts/a2/{name})')


def page_url(rel_path):
    """mirror/event/riviera/index.html -> /event/riviera/ ; mirror/index.html -> /"""
    d = os.path.dirname(rel_path)[len('mirror'):].strip('/')
    return '/' + (d + '/' if d else '')


def touch_sitemap(url):
    today = datetime.date.today().isoformat()
    s = open(SITEMAP, encoding='utf-8').read()
    loc = f'<loc>https://hand-marketing.ru{url}</loc>'
    entry_re = re.compile(re.escape(loc) + r'<lastmod>[^<]*</lastmod>')
    if entry_re.search(s):
        s = entry_re.sub(f'{loc}<lastmod>{today}</lastmod>', s)
        note = 'lastmod обновлён'
    else:
        s = s.replace('</urlset>',
                      f'  <url>{loc}<lastmod>{today}</lastmod></url>\n</urlset>')
        note = 'URL ДОБАВЛЕН (новая страница)'
    open(SITEMAP, 'w', encoding='utf-8').write(s)
    print(f'  sitemap: {url} — {note}')


def canonical_of(url):
    d = os.path.join(MIRROR, url.strip('/'))
    for name in ('index-a2.html', 'index.html'):
        p = os.path.join(d, name)
        if os.path.isfile(p):
            m = re.search(r'<link rel="canonical" href="([^"]+)"', open(p, encoding='utf-8').read())
            return m.group(1) if m else None
    return None


def drop_from_sitemap(url):
    s = open(SITEMAP, encoding='utf-8').read()
    loc = re.escape(f'<loc>https://hand-marketing.ru{url}</loc>')
    new = re.sub(r'[ \t]*<url>' + loc + r'<lastmod>[^<]*</lastmod></url>\n?', '', s)
    if new != s:
        open(SITEMAP, 'w', encoding='utf-8').write(new)
        print(f'  sitemap: {url} — убран (canonical ведёт на другой адрес)')


def main():
    if len(sys.argv) < 2:
        sys.exit('Использование: python3 scripts/a2/finalize_page.py gen_<slug>.py')
    gen = resolve_generator(sys.argv[1])

    dirty_before = git_dirty()
    deleted_before = git_deleted()
    mtimes_before = page_mtimes()
    run(gen)
    # генератор кастомной страницы может СНОСИТЬ файл (типичный случай:
    # index-a2.html, который на деплое переименовывается в index.html и затёр бы
    # кастомную страницу). Такие удаления нельзя откатывать вместе с чужими.
    deleted_by_gen = git_deleted() - deleted_before
    if deleted_by_gen:
        print('  удалено генератором:', ', '.join(sorted(deleted_by_gen)))

    # целевые страницы: index*.html, переписанные генератором. Сравниваем mtime
    # со снимком до запуска (ловит и «перезаписал тем же содержимым»). Раньше брали
    # «mtime >= старт − 1 с», и прогон сразу после другого прогона забирал себе
    # 56 кейсов, которые пост-скрипты прошлого прогона переписали в ту же секунду
    targets = sorted(os.path.relpath(p, ROOT) for p, t in page_mtimes().items()
                     if mtimes_before.get(p) != t)
    if not targets:
        sys.exit('✗ генератор не переписал ни одного mirror/**/index*.html — проверь его вывод')
    print('  страницы генератора:', ', '.join(targets))

    for ps in POSTSCRIPTS:
        run(os.path.join(HERE, ps))

    # откат чужих файлов, изменённых только пост-скриптами
    extra = sorted(git_dirty() - dirty_before - set(targets) - deleted_by_gen)
    extra = [f for f in extra if re.search(r'index(-a2)?\.html$', f)]
    if extra:
        subprocess.run(['git', 'checkout', '--'] + extra, cwd=ROOT, check=True)
        print(f'  откатено чужих файлов: {len(extra)}')
    else:
        print('  чужих изменений нет (пост-скрипты идемпотентны)')

    for url in sorted({page_url(t) for t in targets}):
        # страница с canonical на другой адрес в карту не идёт (как в generate-sitemap.mjs),
        # иначе /samara_vdnh/ возвращалась в sitemap при каждой сборке кейсов
        canon = canonical_of(url)
        if canon and canon.rstrip('/') != f'https://hand-marketing.ru{url}'.rstrip('/'):
            drop_from_sitemap(url)
            continue
        touch_sitemap(url)

    print('\n== Контроль маркеров ==')
    fail = False
    for t in targets:
        s = open(os.path.join(ROOT, t), encoding='utf-8').read()
        missing = [m for m in MARKERS if m not in s]
        print(f'  {"✗" if missing else "✓"} {t}' + (f' — НЕТ: {", ".join(missing)}' if missing else ''))
        fail |= bool(missing)
    if fail:
        sys.exit(1)
    print('\n✓ Готово. Дальше: python3 scripts/a2/case_qa.py <путь-страницы>')


if __name__ == '__main__':
    main()
