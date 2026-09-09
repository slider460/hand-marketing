#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/saintgobain/cx/index.html: кейс «Клиентский опыт»
для Saint-Gobain (ООО «Сен-Гобен Строительная Продукция Рус»).

Материал: два ролика (416,6 с «путь клиента» и 190,9 с «тезисы»), расписание
съёмок на три дня и сценарий в двух книгах Excel. Всё, что стоит на странице,
вынуто из этих файлов скриптом scripts/sgcx-assets.py: 48 портретов финала,
17 портретов руководителей, кадры сцен, палитра, тайм-коды.

Страница показывает работу, а не разбор монтажа. Первый вариант был построен
вокруг цифр (доля хронометража, сценарий против кадра, кого не сняли) и читался
как аналитический отчёт: посетителю сайта это ничего не говорит о том, что
агентство умеет. Поэтому здесь:

  • кадры крупно и много: путь заказа, цеха, склады, отгрузка, монтаж;
  • стена лиц из финала фильма, каждое открывает свою секунду;
  • прямая речь руководителей карточками, портрет в арочной маске, снятой
    с монтажа второй части (цветное окно поверх обесцвеченного дубля);
  • съёмка описана по-человечески: три смены, офис и два завода;
  • доказательство в финале — благодарственное письмо клиента.

Никаких процентов, счётчиков «сколько кого подписано» и сравнений плана
с фактом на странице быть не должно.

Шрифты: Wix Madefor Display + Wix Madefor Text. Фильм набран не парой шрифтов,
а одним нейтральным гротеском в двух оптиках: имя в плашке капсом крупной,
подпись отдела мелкой.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->. index-a2.html в каталоге кейса быть не должно: деплой
переименовал бы его в index.html и затёр кастомную страницу."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))
OUT = os.path.join(HERE, 'agent-out', 'sg-cx')

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

FACTS = json.load(open(os.path.join(OUT, 'facts.json'), encoding='utf-8'))
PARADE = FACTS['parade']
THESES = FACTS['theses']

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/sgcx'
V1 = '/media/sg-cx-part1.mp4'
V2 = '/media/sg-cx-part2.mp4'
# короткая немая нарезка для первого экрана, лежит внутри mirror/**
HERO = '/videos/sgcx-hero-loop.mp4'
URL = 'https://hand-marketing.ru/video/saintgobain/cx/'
TITLE = 'Корпоративный фильм «Клиентский опыт» для Saint-Gobain | Hand Marketing'
DESCR = ('Корпоративный фильм программы «Клиентский опыт» для Saint-Gobain: '
         'путь клиента и 18 тезисов директоров, 48 сотрудников названы по имени, '
         'три съёмочных дня в офисе и на заводах в Егорьевске.')

# ─── подразделения в порядке первого появления в параде ────────────────────
# высота башни знака = число людей, поэтому порядок менять нельзя: силуэт
# складывается из фактических данных, а не подгоняется под красоту
UNITS = [
    ('Клиентский сервис', ['Отдел Клиентского Сервиса']),
    ('Информационные технологии', ['Отдел Информационных Технологий']),
    ('Закупки', ['Отдел Закупок']),
    ('Персонал', ['Отдел Персонала']),
    ('Планирование', ['Отдел Планирования']),
    ('Сертификация', ['Отдел Сертификации']),
    ('Безопасность', ['Отдел Безопасности']),
    ('Маркетинг', ['Отдел Маркетинга']),
    ('Логистика', ['Отдел Логистики', 'Отдел Логистика']),
    ('Стажёр', ['Стажер']),
    ('Продажи', ['Отдел Продаж']),
    ('Аналитика', ['Отдел Аналитики']),
    ('Производство', ['Оператор Производства', 'Начальник смены', 'Инженер Технолог',
                      'Колорист', 'Ведущий специалист по охране труда',
                      'Старший оператор холодной части',
                      'Оператор конвейерной линии оборудования', 'Оператор Мультипак',
                      'Водитель погрузчика', 'Водитель Погрузчика', 'Сменный мастер']),
    ('Офис-менеджер', ['Офис Менеджер']),
    ('Клиентский опыт', ['Клиентский опыт']),
]
SHORT = {'Информационные технологии': 'ИТ'}


def unit_rows():
    """Башни знака: имя, число людей, тайм-код первой плашки, номера портретов."""
    rows = []
    for name, keys in UNITS:
        ppl = [(i, p) for i, p in enumerate(PARADE) if p['unit'] in keys]
        rows.append({'name': name, 'n': len(ppl), 't': ppl[0][1]['t'],
                     'ids': [f'p{i + 1:02d}' for i, _ in ppl],
                     'names': [p['name'] for _, p in ppl]})
    return rows


UROWS = unit_rows()
assert sum(u['n'] for u in UROWS) == 48, sum(u['n'] for u in UROWS)

# ─── тезис → подразделение из парада (если такое есть) ─────────────────────
# семь функций сходятся, у одиннадцати реплик нижнего этажа в фильме нет
TH_UNIT = {
    'Артём Гаврилюк': 'Продажи', 'Андрей Васильев': 'Продажи',
    'Елена Сильвестрова': 'Персонал', 'Андрей Зарипов': 'Производство',
    'Людмила Кирмусова': 'Производство', 'Ирина Кочкина': 'Закупки',
    'Марина Ченцова': 'Логистика', 'Тимур Сагиров': 'Информационные технологии',
    'Юлия Ночёвина': 'Маркетинг',
}

# кадры сцен первой части: тайм-код, файл, подпись. Порядок хронологический
SCENES = [
    (16.0,  'reception',     'Менеджер программы идёт по офису с папкой'),
    (23.2,  'folder',        'На обложке папки портрет клиента'),
    (33.0,  'measure',       'Клиенты выбирают материалы на своём ремонте'),
    (37.2,  'road',          'Дорога мимо рекламы Saint-Gobain'),
    (57.0,  'sales-talk',    'Разговор с сотрудником отдела продаж'),
    (78.0,  'mosaic',        'Знак компании собран из портретов сотрудников'),
    (135.0, 'meeting',       'Совещание с презентацией'),
    (142.4, 'gyproc-yard',   'Площадка завода Gyproc'),
    (148.4, 'isover-stock',  'Линия ISOVER в цеху'),
    (168.0, 'vetonit-line',  'Маркировка ведра weber.vetonit'),
    (183.0, 'mnemo',         'Оператор Vetonit за пультом линии'),
    (191.6, 'control-room',  'Операторская завода'),
    (211.0, 'shipping-doc',  'Отметка в накладной на пункте отгрузки'),
    (221.4, 'pallets',       'Паллеты уходят в фуру'),
    (226.4, 'truck',         'Фура с продукцией на трассе'),
    (232.0, 'mounting',      'Монтаж на объекте'),
    (409.5, 'clients-final', 'Финал: клиенты в готовой квартире'),
]

# три съёмочных дня: лист расписания, дата, место, что стояло в сетке
DAYS = [
    ('11 июля', 'Офис ПРЕО, Преображенская площадь', 33, 15, 7,
     ['ИТ за работой', 'совещание закупок', 'аналитики', 'собеседование в HR',
      'клиентский сервис принимает заказы', 'планирование Isover'],
     ['Оливье Дерош', 'Маргарита Молодых', 'Рафаэль Зохрабян', 'Юлия Ночёвина',
      'Тимур Сагиров', 'Марина Ченцова', 'Алексей Бабак']),
    ('12 июля', 'Егорьевск, два завода', 33, 9, 2,
     ['инструктаж по безопасности и спецодежда', 'производство, две по четыре локации',
      'склады', 'переход на второй завод'],
     ['Людмила Кирмусова', 'Андрей Зарипов']),
    ('17 июля', 'Офис ПРЕО, Преображенская площадь', 35, 13, 6,
     ['совещание маркетинга', 'планирование Vetonit', 'логисты', 'потолки', 'Isoroc'],
     ['Тамара Афонина', 'Григорий Ушаков', 'Ирина Кочкина', 'Николай Морщинин',
      'Елена Радченко', 'Елена Сильвестрова']),
]

LETTER = '/images/lib/as6739-3465-4238-b064-323735316130/sg-video-letter.jpg'

CSS = """<style id="sgcx-css">
.sg{--ink:#101828;--dim:#5A6478;--line:#DDE4EC;--paper:#fff;--cold:#F3F7FA;
 --blue:#181F71;--teal:#3DA2AD;--red:#CE1A3D;--orange:#D65D32;--cx:#2996C5;--night:#0E1330;
 font-family:'Wix Madefor Text','Wix Madefor Display',-apple-system,Arial,sans-serif;
 color:var(--ink);background:var(--paper);overflow-x:hidden}
.sg *{box-sizing:border-box}
.sg h1,.sg h2,.sg h3,.sg .disp{font-family:'Wix Madefor Display','Wix Madefor Text',Arial,sans-serif}
.sg a:focus-visible,.sg button:focus-visible{outline:3px solid var(--cx);outline-offset:3px;border-radius:6px}
.sg__in{max-width:1180px;margin:0 auto;padding:0 32px}
.sg section{padding:96px 0}
.sg .lead{font-size:19px;line-height:1.66;color:var(--dim);max-width:62ch}
.sg .kicker{font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--cx);margin:0 0 18px}
.sg h2{font-size:clamp(28px,3.6vw,46px);line-height:1.08;font-weight:800;letter-spacing:-.02em;margin:0 0 20px}
.sg h3{font-size:20px;font-weight:700;margin:0 0 10px}
.sg .rev{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.sg .rev.on{opacity:1;transform:none}

/* ── герой ───────────────────────────────────────────────────────────── */
.sg-hero{position:relative;background:var(--night);color:#fff;padding:0;overflow:hidden;
 min-height:clamp(480px,72vh,700px);display:flex;align-items:flex-end}
.sg-hero__bg,.sg-hero__v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 transform:scale(1.2) translate(-2.5%,2%);transform-origin:50% 55%}
.sg-hero__bg{opacity:1}
.sg-hero__v{opacity:0;transition:opacity 1.2s ease;pointer-events:none}
.sg-hero__v.is-on{opacity:1}
/* Затемнение не сплошное: кадр должен читаться. Слева плотная подложка под
   текст, справа кадр почти чистый, снизу мягкий уход в цвет секции. */
.sg-hero::after{content:'';position:absolute;inset:0;pointer-events:none;
 background:linear-gradient(100deg,rgba(9,13,36,.94) 0%,rgba(9,13,36,.88) 34%,
  rgba(9,13,36,.62) 58%,rgba(9,13,36,.3) 78%,rgba(9,13,36,.18) 100%),
 linear-gradient(180deg,rgba(9,13,36,.55) 0%,rgba(9,13,36,0) 26%,
  rgba(9,13,36,.12) 62%,rgba(9,13,36,.72) 100%)}
.sg-hero__in{position:relative;z-index:1;width:100%;max-width:1180px;margin:0 auto;
 padding:92px 32px 64px}
.sg-hero__cx{display:flex;align-items:center;gap:14px;margin:0 0 26px}
.sg-hero__cx svg{width:44px;height:44px;flex:none;filter:drop-shadow(0 2px 10px rgba(0,0,0,.5))}
.sg-hero__cx span{font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:#C6D6E4;
 font-weight:700;text-shadow:0 1px 12px rgba(9,13,36,.8)}
.sg-hero h1{font-size:clamp(34px,4.6vw,60px);line-height:1.04;font-weight:800;letter-spacing:-.03em;
 margin:0;max-width:19ch;text-shadow:0 2px 26px rgba(9,13,36,.5)}
.sg-hero h1 em{font-style:normal;color:var(--cx)}
.sg-hero__sub{margin:20px 0 0;font-size:clamp(16px,1.7vw,20px);color:#CBD9E6;max-width:50ch;
 line-height:1.6;text-shadow:0 1px 16px rgba(9,13,36,.7)}
.sg-hero__meta{display:flex;flex-wrap:wrap;gap:10px;margin:28px 0 0}
.sg-hero__meta span{font-size:13px;font-weight:600;color:#DCE7F0;border:1px solid rgba(255,255,255,.28);
 background:rgba(9,13,36,.4);backdrop-filter:blur(3px);border-radius:99px;padding:8px 16px}

/* ── плеер: карточка заходит на герой, чтобы стык не был пустым ───────── */
.sg-player{background:var(--cold);padding:0 0 96px}
.sg-player__in{max-width:1180px;margin:0 auto;padding:0 32px}
.sg-frame{position:relative;margin-top:-88px;background:#000;border-radius:16px;overflow:hidden;
 aspect-ratio:16/9;box-shadow:0 30px 70px rgba(9,13,36,.42)}
.sg-frame video{width:100%;height:100%;display:block;object-fit:contain;background:#000}
.sg-player__tabs{display:flex;gap:10px;margin:26px 0 0;flex-wrap:wrap}
.sg-tab{appearance:none;border:1px solid var(--line);background:#fff;color:var(--dim);
 font:inherit;font-size:14px;font-weight:700;padding:11px 20px;border-radius:99px;cursor:pointer;
 transition:background .2s,color .2s,border-color .2s}
.sg-tab:hover{border-color:var(--cx);color:var(--ink)}
.sg-tab[aria-pressed="true"]{background:var(--cx);border-color:var(--cx);color:#fff}

/* ── задача и съёмка: две колонки текста ─────────────────────────────── */
.sg-brief{background:#fff}
.sg-brief__grid{display:grid;grid-template-columns:1fr 1fr;gap:36px;margin-top:30px}

/* ── путь клиента ────────────────────────────────────────────────────── */
.sg-path{background:#fff}
.sg-path__lead{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:40px 0 22px}
.sg-path__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.sg-shot{display:block;background:#fff;border:0;border-radius:14px;overflow:hidden;text-align:left;
 padding:0;cursor:pointer;font:inherit;transition:transform .25s ease,box-shadow .25s ease}
.sg-shot:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(16,24,40,.16)}
.sg-shot img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block;background:#E7EDF2;
 border-radius:14px}
.sg-shot--big img{aspect-ratio:4/3}
.sg-shot__b{display:block;padding:12px 2px 0}
.sg-shot__d{display:block;font-size:14.5px;line-height:1.5;color:var(--ink);font-weight:500}
.sg-shot--big .sg-shot__d{font-size:17px;font-weight:600}
.sg-path__hint{margin:26px 0 0;font-size:13.5px;color:var(--dim)}

/* ── стена лиц ───────────────────────────────────────────────────────── */
.sg-names{background:var(--cold)}
.sg-names__wall{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin:42px 0 0}
.sg-face{position:relative;display:block;padding:0;border:0;background:#0E1330;border-radius:12px;
 overflow:hidden;cursor:pointer;font:inherit;transition:transform .22s ease}
.sg-face img{display:block;width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;
 transition:transform .5s ease,filter .3s ease}
.sg-face:hover img{transform:scale(1.05)}
.sg-face__b{position:absolute;left:0;right:0;bottom:0;padding:26px 12px 11px;text-align:left;
 background:linear-gradient(180deg,rgba(14,19,48,0) 0%,rgba(14,19,48,.9) 62%)}
.sg-face__n{display:block;font-family:'Wix Madefor Display',Arial,sans-serif;font-weight:800;
 font-size:12.5px;line-height:1.2;color:#fff;text-transform:uppercase;letter-spacing:.01em}
.sg-face__u{display:block;margin-top:3px;font-size:11px;line-height:1.25;color:#B7C6D4}

/* ── тезисы ──────────────────────────────────────────────────────────── */
.sg-th{background:var(--night);color:#fff}
.sg-th h2{color:#fff}
.sg-th .lead{color:#A9BCCC}
.sg-th__list{margin-top:46px;display:grid;grid-template-columns:1fr 1fr;gap:22px}
.sg-t{display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:center;
 background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.09);border-radius:16px;padding:18px 20px}
.sg-t__ph{position:relative;width:150px;height:186px;flex:none}
.sg-t__ph img{position:absolute;object-fit:cover}
.sg-t__ph .bw{left:0;top:12px;width:118px;height:162px;filter:grayscale(1) contrast(.92) brightness(.78);
 opacity:.5;border-radius:8px}
.sg-t__ph .cl{right:0;top:0;width:118px;height:186px;clip-path:inset(0 0 0 0 round 58px 10px 10px 10px)}
.sg-t__body{min-width:0}
.sg-t__q{font-family:'Wix Madefor Display',Arial,sans-serif;font-weight:800;font-size:16px;
 line-height:1.32;letter-spacing:.004em;text-transform:uppercase;margin:0}
.sg-t__q .dim{color:#8FA6B8}
.sg-t__q .hi{color:#fff}
.sg-t__w{margin:13px 0 0;font-size:13.5px;color:#9FB6C9;line-height:1.45}
.sg-t__w b{color:#fff;font-weight:700;font-size:14.5px}
.sg-t__seek{appearance:none;border:1px solid rgba(255,255,255,.24);background:transparent;color:#C9D7E2;
 font:inherit;font-size:12.5px;font-weight:700;padding:7px 15px;border-radius:99px;cursor:pointer;margin-top:13px}
.sg-t__seek:hover{background:var(--cx);border-color:var(--cx);color:#fff}

/* ── производство ────────────────────────────────────────────────────── */
.sg-shoot{background:#fff}
.sg-prod{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:42px 0 0}
.sg-prod__i{margin:0}
.sg-prod__i img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:12px;display:block;
 background:#E7EDF2}
.sg-prod__i figcaption{margin:10px 0 0;font-size:13.5px;color:var(--dim)}

/* ── письмо ──────────────────────────────────────────────────────────── */
.sg-let{background:var(--cold)}
.sg-let__grid{display:grid;grid-template-columns:340px 1fr;gap:44px;align-items:center}
.sg-let__grid img{width:100%;height:auto;border-radius:10px;border:1px solid var(--line);background:#fff}
.sg-let blockquote{margin:0;font-family:'Wix Madefor Display',Arial,sans-serif;font-size:clamp(20px,2.4vw,30px);
 line-height:1.3;font-weight:800;letter-spacing:-.01em}
.sg-let cite{display:block;margin:22px 0 0;font-style:normal;font-size:15px;color:var(--dim);line-height:1.6}
.sg-let cite b{color:var(--ink);font-weight:700}

@media (max-width:1100px){
 .sg-names__wall{grid-template-columns:repeat(4,1fr)}
 .sg-th__list{grid-template-columns:1fr}
 .sg-t{grid-template-columns:150px 1fr}
}
@media (max-width:860px){
 .sg section{padding:64px 0}
 .sg__in,.sg-hero__in,.sg-player__in{padding-left:20px;padding-right:20px}
 .sg-hero{min-height:clamp(440px,76vh,620px)}
 .sg-hero__in{padding-top:80px;padding-bottom:48px}
 .sg-hero::after{background:linear-gradient(180deg,rgba(9,13,36,.6) 0%,rgba(9,13,36,.35) 34%,
  rgba(9,13,36,.82) 78%,rgba(9,13,36,.95) 100%)}
 .sg-frame{margin-top:-52px;border-radius:12px}
 .sg-brief__grid{grid-template-columns:1fr;gap:18px}
 .sg-path__lead{grid-template-columns:1fr}
 .sg-path__grid,.sg-prod{grid-template-columns:1fr 1fr;gap:14px}
 .sg-names__wall{grid-template-columns:repeat(3,1fr);gap:10px}
 .sg-face__b{padding:20px 9px 9px}
 .sg-face__n{font-size:11px}
 .sg-face__u{font-size:10px}
 .sg-let__grid{grid-template-columns:1fr;gap:26px}
 .sg-let__grid img{max-width:300px}
}
@media (max-width:560px){
 .sg-path__grid,.sg-prod{grid-template-columns:1fr}
 .sg-names__wall{grid-template-columns:repeat(2,1fr)}
 .sg-t{grid-template-columns:1fr}
 .sg-t__ph{width:100%;max-width:200px;height:230px}
 .sg-t__ph .bw{width:158px;height:206px}
 .sg-t__ph .cl{width:158px;height:230px}
}
@media (max-height:520px) and (orientation:landscape){
 .sg-hero__in{padding-top:44px;padding-bottom:40px}
 .sg section{padding:48px 0}
}
@media (prefers-reduced-motion:reduce){
 .sg .rev{opacity:1;transform:none;transition:none}
 .sg-shot:hover,.sg-face:hover img{transform:none}
}
</style>"""

CX_SVG = ('<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M22 116V44a30 30 0 0 1 60 0v18" '
          'fill="none" stroke="#2996C5" stroke-width="7" stroke-linecap="round"/>'
          '<path d="M92 54 82 66 72 54" fill="none" stroke="#2996C5" stroke-width="7" '
          'stroke-linecap="round" stroke-linejoin="round"/>'
          '<path d="M82 66V44" fill="none" stroke="#2996C5" stroke-width="7" stroke-linecap="round"/></svg>')


def hero():
    """Первый экран: кадр из фильма и одна мысль, без витрины цифр."""
    # постер лежит под видео и виден, пока луп грузится: это первый кадр
    # самого лупа, поэтому подмены не заметно. Видео проявляется по событию
    # playing, а не по загрузке: на мобильных с запретом автозапуска
    # остаётся аккуратный кадр без системной кнопки
    return ('<section class="sg-hero">'
            f'<img class="sg-hero__bg" src="{IMG}/hero-poster.jpg" alt="" aria-hidden="true">'
            f'<video class="sg-hero__v" src="{HERO}" poster="{IMG}/hero-poster.jpg" '
            'autoplay muted loop playsinline preload="metadata" aria-hidden="true"></video>'
            '<div class="sg-hero__in">'
            f'<div class="sg-hero__cx">{CX_SVG}<span>Saint-Gobain · программа «Клиентский опыт»</span></div>'
            '<h1>Корпоративный фильм<br>о людях, которые<br><em>делают клиентский опыт</em></h1>'
            '<p class="sg-hero__sub">Две части, десять минут: путь клиента от рекламы у дороги '
            'до готовой квартиры и прямая речь руководителей компании. Снимали в московском офисе '
            'и на двух заводах в Егорьевске.</p>'
            '<div class="sg-hero__meta">'
            '<span>Saint-Gobain</span><span>корпоративный фильм</span>'
            '<span>две части, 10 минут</span><span>съёмка, интервью, монтаж, графика</span>'
            '</div>'
            '</div></section>')


def player():
    return ('<section class="sg-player"><div class="sg-player__in">'
            f'<div class="sg-frame"><video id="sgpl" controls preload="metadata" playsinline '
            f'poster="{IMG}/sc-clients-final.jpg" src="{V1}"></video></div>'
            '<div class="sg-player__tabs" role="group" aria-label="Части фильма">'
            '<button class="sg-tab" type="button" data-part="1" aria-pressed="true">'
            'Часть первая. Путь клиента</button>'
            '<button class="sg-tab" type="button" data-part="2" aria-pressed="false">'
            'Часть вторая. Голоса руководителей</button></div>'
            '</div></section>')


def brief():
    return ('<section class="sg-brief"><div class="sg__in">'
            '<p class="kicker">Задача</p>'
            '<h2>Показать сотрудникам программу,<br>которую видит только клиент</h2>'
            '<div class="sg-brief__grid">'
            '<p class="lead">Saint-Gobain запускал внутри компании программу «Клиентский опыт» '
            'и хотел объяснить каждому сотруднику простую вещь: путь клиента складывается '
            'из работы всех подразделений, даже тех, кто клиента ни разу не видит.</p>'
            '<p class="lead">Мы предложили снять это буквально. Первая часть проходит весь путь '
            'заказа: реклама, выбор, оформление, закупка сырья, планирование, смена на линии, '
            'склад, отгрузка, доставка, монтаж и готовый дом. Вторая собирает прямую речь '
            'руководителей всех направлений, от продаж и логистики до заводов и региональных '
            'компаний.</p>'
            '</div></div></section>')


def path():
    """Путь клиента: крупные кадры, каждый перематывает фильм."""
    big = SCENES[:2]
    rest = SCENES[2:]
    def card(t, sl, d, cls=''):
        return (f'<button class="sg-shot {cls}" type="button" data-part="1" data-t="{t}">'
                f'<img src="{IMG}/sc-{sl}.jpg" alt="{d}" loading="lazy" width="1120" height="630">'
                f'<span class="sg-shot__b"><span class="sg-shot__d">{d}</span></span></button>')
    lead = ''.join(card(t, sl, d, 'sg-shot--big') for t, sl, d in big)
    grid = ''.join(card(t, sl, d) for t, sl, d in rest)
    return ('<section class="sg-path"><div class="sg__in">'
            '<p class="kicker">Первая часть</p>'
            '<h2>Один заказ проходит<br>через всю компанию</h2>'
            '<p class="lead">Клиент видит рекламу, сайт и готовый ремонт. За этим стоят закупки '
            'сырья, планирование производства, смена у линии, склад, погрузчик, фура и монтажники '
            'на объекте. Фильм проходит эту цепочку целиком, без пропусков.</p>'
            f'<div class="sg-path__lead">{lead}</div>'
            f'<div class="sg-path__grid">{grid}</div>'
            '<p class="sg-path__hint">Любой кадр перематывает фильм на свою сцену.</p>'
            '</div></section>')


def names():
    """Финал фильма: 48 сотрудников на своих рабочих местах."""
    cards = ''
    for i, p in enumerate(PARADE):
        pid = f'p{i + 1:02d}'
        cards += (f'<button class="sg-face" type="button" data-part="1" data-t="{p["t"]}" '
                  f'aria-label="{p["name"]}, {p["unit"]}">'
                  f'<img src="{IMG}/{pid}@280.jpg" alt="{p["name"]}" loading="lazy" '
                  'width="280" height="373">'
                  f'<span class="sg-face__b"><span class="sg-face__n">{p["name"]}</span>'
                  f'<span class="sg-face__u">{p["unit"]}</span></span></button>')
    return ('<section class="sg-names"><div class="sg__in">'
            '<p class="kicker">Финал первой части</p>'
            '<h2>Компанию сняли<br>по именам</h2>'
            '<p class="lead">Вместо титров с логотипом фильм заканчивается лицами: сотрудники '
            'офиса и заводов на своих рабочих местах, каждый с именем и подразделением. '
            'Съёмка шла в рабочие смены, без постановочных студий и переодеваний.</p>'
            f'<div class="sg-names__wall">{cards}</div>'
            '<p class="sg-path__hint">Клик по человеку открывает его секунду в фильме.</p>'
            '</div></section>')


def theses():
    ids = {}
    n = 0
    for t in THESES:
        if t['speaker'] not in ids:
            n += 1
            ids[t['speaker']] = f'sp-{n:02d}'
    cards = ''
    seen = set()
    for th in THESES:
        if th['speaker'] in seen:
            continue
        seen.add(th['speaker'])
        pid = ids[th['speaker']]
        l1 = f'<span class="dim">{th["l1"]}</span> ' if th.get('l1') else ''
        cards += ('<article class="sg-t rev">'
                  f'<span class="sg-t__ph"><img class="bw" src="{IMG}/{pid}.jpg" alt="" '
                  'loading="lazy" width="560" height="746">'
                  f'<img class="cl" src="{IMG}/{pid}.jpg" alt="{th["speaker"]}" loading="lazy" '
                  'width="560" height="746"></span>'
                  f'<span class="sg-t__body"><p class="sg-t__q">{l1}'
                  f'<span class="hi">{th.get("l2", th["text"])}</span></p>'
                  f'<p class="sg-t__w"><b>{th["speaker"]}</b><br>{th["title"]}</p>'
                  f'<button class="sg-t__seek" type="button" data-part="2" data-t="{th["t"]}">'
                  'смотреть фрагмент</button></span></article>')
    return ('<section class="sg-th"><div class="sg__in">'
            '<p class="kicker">Вторая часть</p>'
            '<h2>Прямая речь<br>руководителей</h2>'
            '<p class="lead">Семнадцать интервью: операционный и генеральный директора, продажи, '
            'персонал, закупки, логистика, финансы, ИТ, маркетинг, индустриальные директора '
            'заводов и главы компаний в Казахстане и Беларуси. Каждому дали одну мысль '
            'и один кадр.</p>'
            f'<div class="sg-th__list">{cards}</div>'
            '</div></section>')


def shoot():
    """Производство: чем именно занималась съёмочная группа."""
    shots = [('gyproc-yard', 'Площадка завода'), ('isover-stock', 'Линия ISOVER'),
             ('vetonit-line', 'Маркировка партии weber.vetonit'), ('control-room', 'Операторская'),
             ('pallets', 'Отгрузка'), ('mounting', 'Монтаж на объекте')]
    gal = ''.join(f'<figure class="sg-prod__i"><img src="{IMG}/sc-{sl}.jpg" alt="{cap}" '
                  f'loading="lazy" width="1120" height="630">'
                  f'<figcaption>{cap}</figcaption></figure>' for sl, cap in shots)
    return ('<section class="sg-shoot"><div class="sg__in">'
            '<p class="kicker">Как снимали</p>'
            '<h2>Три смены: офис,<br>цеха и склады</h2>'
            '<div class="sg-brief__grid">'
            '<p class="lead">Две смены в московском офисе на Преображенской: интервью '
            'руководителей между их встречами, рабочие сцены отделов, финальные портреты '
            'сотрудников на местах.</p>'
            '<p class="lead">Одна смена в Егорьевске на двух заводах: инструктаж и спецодежда '
            'с утра, дальше цеха, линии, лаборатория, склады и отгрузка. Двух руководителей, '
            'работающих в Казахстане и Беларуси, сняли отдельно и собрали в общий монтаж.</p>'
            '</div>'
            f'<div class="sg-prod">{gal}</div>'
            '</div></section>')


def letter():
    q = FACTS['letter']
    return ('<section class="sg-let"><div class="sg__in"><div class="sg-let__grid">'
            f'<img class="rev" src="{LETTER}" alt="Благодарственное письмо '
            '«Сен-Гобен Строительная Продукция Рус»" loading="lazy" width="1680" height="2375">'
            '<div><blockquote>«Результат оправдал и превзошёл ожидания»</blockquote>'
            '<cite>Из благодарственного письма ООО «Сен-Гобен Строительная Продукция Рус» '
            'за создание корпоративного видеоролика высокого качества, выполненного '
            'в сжатые сроки.<br><br><b>Татьяна Дулуба</b>, руководитель программы '
            '«Клиентский опыт» в Saint-Gobain.</cite>'
            '</div></div></div></section>')


PAGE_JS = """<script>(function(){
var V1='%V1%',V2='%V2%',pl=document.getElementById('sgpl');
var tabs=[].slice.call(document.querySelectorAll('.sg-tab'));
function setPart(p,cb){
 var want=(p==='2')?V2:V1;
 tabs.forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.part===p));});
 if(pl.getAttribute('src')===want){if(cb)cb();return;}
 pl.setAttribute('src',want);
 pl.addEventListener('loadedmetadata',function h(){pl.removeEventListener('loadedmetadata',h);if(cb)cb();});
 pl.load();
}
function seek(part,t){
 setPart(part,function(){
  try{pl.currentTime=t;}catch(e){}
  var p=pl.play();if(p&&p.catch)p.catch(function(){});
 });
 var box=pl.closest('.sg-frame');
 if(box){var r=box.getBoundingClientRect();
  if(r.top<0||r.bottom>window.innerHeight)box.scrollIntoView({behavior:'smooth',block:'center'});}
}
tabs.forEach(function(b){b.addEventListener('click',function(){setPart(b.dataset.part);});});
document.addEventListener('click',function(e){
 var el=e.target.closest('[data-t][data-part]');
 if(!el)return;
 seek(el.dataset.part,parseFloat(el.dataset.t));
 var tw=e.target.closest('.tower');
 if(tw)pick(tw);
});
// башни знака
var pickBox=document.getElementById('sgPick');
function pick(tw){
 [].forEach.call(document.querySelectorAll('.tower'),function(o){o.classList.remove('on');});
 tw.classList.add('on');
 if(!pickBox)return;
 var t=parseFloat(tw.dataset.t),m=Math.floor(t/60),s=(t%60).toFixed(1);
 pickBox.innerHTML='<b>'+tw.dataset.unit+'</b>: '+tw.dataset.n+
  (tw.dataset.n==='1'?' человек':(+tw.dataset.n<5?' человека':' человек'))+
  ' в перекличке, первая плашка на '+m+':'+(s.length<4?'0'+s:s)+'.';
}
[].forEach.call(document.querySelectorAll('.tower'),function(tw){
 tw.addEventListener('keydown',function(e){
  if(e.key==='Enter'||e.key===' '){e.preventDefault();seek('1',parseFloat(tw.dataset.t));pick(tw);}
 });
});
// луп героя: показываем, только когда воспроизведение реально началось,
// иначе на мобильных с запретом автозапуска мигал бы чёрный прямоугольник
var hv=document.querySelector('.sg-hero__v');
if(hv){
 hv.addEventListener('playing',function(){hv.classList.add('is-on');});
 var hp=hv.play();if(hp&&hp.catch)hp.catch(function(){});
 if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){
  hv.pause();hv.classList.remove('is-on');
 }
}
// проявление блоков
var io=window.IntersectionObserver?new IntersectionObserver(function(es){
 es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('on');io.unobserve(en.target);}});
},{rootMargin:'0px 0px -8% 0px'}):null;
[].forEach.call(document.querySelectorAll('.sg .rev'),function(n){
 if(io)io.observe(n);else n.classList.add('on');
});
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Video","item":"https://hand-marketing.ru/videoproduction/"},'
  '{"@type":"ListItem","position":3,"name":"Корпоративный фильм «Клиентский опыт» для Saint-Gobain",'
  f'"item":"{URL}"}}]}}</script>')

VIDEO_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"VideoObject","name":"Корпоративный фильм «Клиентский опыт» для Saint-Gobain",'
  '"description":"Первая часть корпоративного фильма программы «Клиентский опыт»: '
  'путь клиента и перекличка 48 сотрудников компании.",'
  f'"thumbnailUrl":"https://hand-marketing.ru{IMG}/sc-mosaic.jpg",'
  f'"contentUrl":"https://hand-marketing.ru{V1}",'
  '"uploadDate":"2026-09-08","duration":"PT6M57S"}</script>')

HEAD = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<!--custom-page-->'
        f'<title>{TITLE}</title>'
        f'<meta name="description" content="{DESCR}">'
        '<meta name="robots" content="index, follow">'
        f'<link rel="canonical" href="{URL}">'
        '<meta property="og:type" content="article">'
        f'<meta property="og:title" content="{TITLE}">'
        f'<meta property="og:description" content="{DESCR}">'
        f'<meta property="og:url" content="{URL}">'
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/sc-mosaic.jpg">'
        '<link rel="stylesheet" href="/fonts/madefor.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    js = PAGE_JS.replace('%V1%', V1).replace('%V2%', V2)
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="sg">{hero()}{player()}{brief()}{path()}'
            f'{names()}{theses()}{shoot()}{letter()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}'
            f'{BREADCRUMB_LD}{VIDEO_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'saintgobain', 'cx')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('· удалён index-a2.html (деплой затёр бы им кастомную страницу)')
    print(f'✓ {os.path.relpath(p, os.path.dirname(ROOT))} '
          f'({os.path.getsize(p) / 1024:.0f} КБ)')
