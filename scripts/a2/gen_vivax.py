#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/vivax/index.html: кейс «Вирусный ролик VIVAX SPORT
с Настасьей Самбурской» для компании «Академия Научной Красоты».

Материал: ролик 49,28 с и папка со смены (5 фото + 2 клипа, iPhone,
29 мая, зал X-Fit). Всё, что есть на странице, вынуто из этих файлов
скриптом scripts/vivax-assets.py: кадры, склейки, громкость, палитра
и сам знак-шеврон (контуром с титра, а не срисован).

Идея страницы. Ролик устроен как одна тренировка, разложенная по трём
средствам линейки: разогрев до нагрузки, восстановление после,
реабилитация после ушиба. Значит и страница должна быть устроена как
тренировка, а не как хронометраж.

  • Палитру страницы ведёт сам плеер: пока идёт разогрев, страница
    красная, после 23-й секунды синеет, после 38-й зеленеет. Ролик
    красит собственный кейс.
  • «Три средства» — обещания прочитаны прямо с упаковки в кадре,
    слово в слово, включая мелкий шрифт буллетов.
  • «Что происходит с мышцей» — механика, которой на сайте ещё не было:
    продольный разрез мышцы на canvas проходит те же 49 секунд.
    Капилляры раскрываются на разогреве, копится лактат под нагрузкой,
    вымывается после геля, микроразрыв затягивается на реабилитации.
    Каждый эффект подписан строкой с тюбика: схема нарисована
    по обещаниям производителя, ничего сверх них.
  • «Тело в кадре» — 64 плана приколоты к зонам, которые в них видны:
    ролик про средство для мышц и потому говорит фрагментами тела.
    Зоны покрашены тем средством, которое к ним применяют в ролике.
  • «Тренировка за 49 секунд» — что она реально делает в кадре.
  • «По ту сторону камеры» — фото и клипы со смены; клипы сняты ровно
    на той сцене с лапами, что стоит в ролике на 19,04–20,96.

Шрифты: Jost (титры ролика и логотип VIVAX набраны геометрической
антиквой футуровского строя) + Inter Tight.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->. index-a2.html в каталоге кейса быть не должно: деплой
переименовал бы его в index.html и затёр кастомную страницу."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/vivax'
URL = 'https://hand-marketing.ru/video/vivax/'
TITLE = 'Рекламный ролик VIVAX SPORT с Настасьей Самбурской | Hand Marketing'
DESCR = ('Вирусный ролик спортивных средств VIVAX SPORT с актрисой Настасьей '
         'Самбурской для компании «Академия Научной Красоты». Разбор кейса: '
         'три средства линейки в одной тренировке, схема работы мышцы, '
         'карта тела по 64 планам, съёмка в зале X-Fit.')

MAP = json.load(open(os.path.join(HERE, 'vivax_map.json'), encoding='utf-8'))
STILL = MAP['stills']
WHAT = {k: v['what'] for k, v in STILL.items()}
SEC = {k: v['sec'] for k, v in STILL.items()}
PHOTOS = MAP['photos']
CLIPS = MAP['clips']
PAL = MAP['palette']
CHEVRON = MAP['chevron']
SHOTS = MAP['shots']
STATS = MAP['stats']
DURATION = MAP['duration']
VIDEO = MAP['video']
QUIET = MAP['quiet'][0]

# самый длинный СНЯТЫЙ план: пустой зал, и ровно на нём музыка уходит в ноль
# (планы заставки длиннее, но это графика, а не съёмка)
LONGEST = STATS['film_longest_at']

# ─── три средства: текст прочитан с упаковки в кадре, слово в слово ────────
# у каждого свой титр в ролике, свой цвет шеврона и своя секунда
TUBES = [
    dict(
        id='warm', word='Разогрев', sec=5.04, title=6.24, still='tube-warm',
        kind='Крем разогревающий для тела с активными пептидными комплексами',
        claim='Эффективные тренировки',
        note='Наносит до нагрузки: плечи, трапеция, поясница, предплечья.',
        bullets=[
            'Глубоко разогревает мышцы и связки, подготавливая к нагрузкам',
            'Улучшает микроциркуляцию крови',
            'Повышает эластичность мышц, увеличивает подвижность суставов',
            'Способствует активизации АТФ',
            'Значительно снижает вероятность получения травм',
        ]),
    dict(
        id='cool', word='Восстановление', sec=23.48, title=24.44, still='tube-cool',
        kind='Гель релаксантный с активными пептидными комплексами',
        claim='Интенсивное восстановление',
        note='Наносит после нагрузки: голень, затем бедро и квадрицепс.',
        bullets=[
            'Способствует выведению молочной кислоты',
            'Снимает болевые ощущения и мышечный спазм',
            'Эффективная профилактика варикозного расширения вен',
            'Восстанавливает здоровье кожи после солнечного стресса',
            'Оказывает противоотёчное действие',
        ]),
    dict(
        id='heal', word='Реабилитация', sec=38.36, title=39.12, still='tube-heal',
        kind='Крем регенерирующий с активными пептидными комплексами',
        claim='Быстрая реабилитация',
        note='Наносит на ушиб: локоть, которым она приложилась на тренировке.',
        bullets=[
            'Значительно сокращает период реабилитации при растяжениях, '
            'переломах и др. травмах',
            'Быстро рассасывает гематомы и отёки при ушибах',
            'Снимает судороги и мышечный спазм',
        ]),
]

# ─── фазы ролика: их же читает JS, чтобы красить страницу по плееру ────────
PHASES = [
    ('none', 0.00, 5.04, 'Зал', 'Приходит в зал: общий план, проход, портрет'),
    ('warm', 5.04, 9.68, 'Разогрев', 'Красный тюбик и нанесение до нагрузки'),
    ('work', 9.68, 23.48, 'Тренировка', 'Мяч, бодибар, приседания, работа по лапам'),
    ('cool', 23.48, 28.08, 'Восстановление', 'Синий тюбик после нагрузки'),
    ('fall', 28.08, 35.32, 'Падение', 'Оступается на блине от штанги и уходит из кадра'),
    ('heal', 35.32, 42.04, 'Ушиб и реабилитация', 'Гематома на локте, зелёный тюбик'),
    ('end', 42.04, 49.28, 'Заставка', 'VIVAX SPORT, «Ты сможешь больше!»'),
]

# ─── роль: что Самбурская играет за 49 секунд, по кадрам ──────────────────
STAR = [
    (4.24, 'walk-face', 'Заходит в зал'),
    (16.72, 'face-pad', 'Лапа над головой'),
    (21.24, 'rest-face', 'Работает в полную силу'),
    (22.76, 'rest-smile', 'Кураж'),
    (33.36, 'fall-back', 'После падения'),
    (34.30, 'face-shock', 'Что это было'),
    (37.20, 'grimace', 'Больно'),
    (41.30, 'heal-smile', 'Отпустило'),
]

# ─── падение: комическая кульминация, разложенная по кадрам ───────────────
FALL = [
    (28.28, 'fall-step', 'Наступает на блин от штанги'),
    (29.28, 'fall-flail', 'Взмах руками'),
    (30.00, 'fall-out', 'Уходит вниз из кадра'),
    (32.00, 'empty-gym', 'Пустой зал'),
    (33.36, 'fall-back', 'Выныривает обратно'),
]

# ─── тренировка: что она делает в кадре, по порядку ───────────────────────
PROGRAMME = [
    (9.96, 'Отведение ноги в упоре', 'ex-kick'),
    (10.48, 'Набивной мяч у груди', 'ex-medball'),
    (11.44, 'Прыжки через мяч', 'ex-ballstep'),
    (12.04, 'Серия ударов руками', 'ex-abs'),
    (13.32, 'Бросок мяча над головой', 'ex-throw'),
    (13.92, 'Выпады с бодибаром', 'ex-bodybar'),
    (14.56, 'Приседания', 'ex-squat'),
    (16.96, 'Выпад назад', 'ex-glutes'),
    (17.48, 'Удар локтем', 'ex-elbow'),
    (18.76, 'Упор лёжа, отведение ноги', 'ex-plank'),
    (19.04, 'Работа по лапам', 'ex-pads'),
    (22.00, 'Растяжка трицепса', 'ex-stretch'),
]

# ─── зоны тела: (id, подпись, средство, секунда, кадр, что показывает) ─────
ZONES = [
    ('traps', 'Шея и трапеция', 'warm', 6.92, 'warm-shoulder',
     'Первое, что она мажет, открыв тюбик'),
    ('delts', 'Плечи и дельты', 'warm', 7.36, 'warm-delta',
     'Крем растирают по дельте перед нагрузкой на плечевой пояс'),
    ('elbow', 'Локоть', 'heal', 35.32, 'bruise',
     'Гематома после падения: единственная травма в сюжете'),
    ('arms', 'Предплечья', 'warm', 8.48, 'warm-arm',
     'Последняя зона разогрева, перед работой по лапам'),
    ('hands', 'Кисти', 'work', 19.04, 'ex-pads',
     'Перчатки и лапы: полторы секунды ролика на одну связку'),
    ('abs', 'Пресс', 'work', 12.04, 'ex-abs',
     'Серия ударов снята одним кадром по прессу и косым'),
    ('core', 'Поясница и косые', 'warm', 7.72, 'warm-back',
     'Поясница, на которую придётся вся работа с мячом и грифом'),
    ('glutes', 'Ягодицы', 'work', 16.96, 'ex-glutes',
     'Выпад назад, снятый со спины'),
    ('quads', 'Бедро и квадрицепс', 'cool', 25.68, 'cool-quad',
     'Гель поднимают с голени выше, на квадрицепс'),
    ('calves', 'Голень и икра', 'cool', 24.96, 'cool-shin',
     'Первое, куда идёт синий гель после нагрузки'),
]

ZONE_TUBE = {'warm': 'Разогрев', 'cool': 'Восстановление', 'heal': 'Реабилитация',
             'work': 'Без средства'}

# ─── фото со смены: порядок показа ────────────────────────────────────────
SET_ORDER = ['set-wide', 'set-monitor', 'set-red', 'set-selfie']


def mmss(sec):
    return '%d:%02d' % (int(sec) // 60, int(round(sec)) % 60)


def num(x):
    return str(x).replace('.', ',')


def plural(n, one, few, many):
    n = abs(n) % 100
    if 11 <= n <= 14:
        return many
    n %= 10
    return one if n == 1 else few if 2 <= n <= 4 else many


def pic(slug, sizes, cls='', extra=''):
    """<img> кадра в трёх размерах: браузер берёт нужный по ширине места."""
    a = WHAT.get(slug, '')
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="{IMG}/{slug}-s.jpg" '
            f'srcset="{IMG}/{slug}-s.jpg 420w, {IMG}/{slug}-m.jpg 720w, '
            f'{IMG}/{slug}.jpg 1080w" sizes="{sizes}" alt="{a}" '
            f'loading="lazy" decoding="async"{extra}>')


def photo(slug, sizes, cls=''):
    a = PHOTOS[slug]['what']
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="{IMG}/{slug}-s.jpg" '
            f'srcset="{IMG}/{slug}-s.jpg 480w, {IMG}/{slug}-m.jpg 900w, '
            f'{IMG}/{slug}.jpg 1400w" sizes="{sizes}" alt="{a}" '
            f'loading="lazy" decoding="async">')


def chev(cls='', extra=''):
    """Знак-шеврон VIVAX: контур снят с титра ролика (9 точек)."""
    return (f'<svg class="vx-chev {cls}" viewBox="0 0 100 100" '
            f'aria-hidden="true" {extra}><path d="{CHEVRON}" fill="currentColor"/></svg>')


def seek(sec, label=None):
    lbl = label or mmss(sec)
    return (f'<button class="vx-seek" type="button" data-seek="{sec}">'
            f'<span class="vx-seek__i" aria-hidden="true"></span>{lbl}</button>')


# ══════════════════════════════════════════════════════════════════════════
CSS = """<style>
/* Кейс /video/vivax/. Палитра снята пипеткой с титров ролика и с плашки
   заставки (scripts/vivax-assets.py): шевроны в ролике залиты градиентом
   от светлого к насыщенному, поэтому у каждого средства две меры цвета.
   Тон --*-d затемнён от измеренного, чтобы текст читался на белом. */
.vx{
  --ink:#14171C; --mut:#69707A; --line:rgba(20,23,28,.13);
  --bg:#fff; --bg2:#F1F3F5; --bg3:#E7EAED;
  --brand:%BRAND%;
  --warm-1:%WARM1%; --warm-2:%WARM2%; --warm-d:#BC0D38;
  --cool-1:%COOL1%; --cool-2:%COOL2%; --cool-d:#1B6F9E;
  --heal-1:%HEAL1%; --heal-2:%HEAL2%; --heal-d:#3F7F26;
  /* активный акцент: его переставляет плеер */
  --a1:#C9CFD4; --a2:#8E979F; --ad:#14171C;
  font-family:'Inter Tight','Inter',-apple-system,Arial,sans-serif;
  color:var(--ink); background:var(--bg);
  -webkit-font-smoothing:antialiased;
}
.vx[data-act="warm"],.vx[data-act="work"]{--a1:var(--warm-1);--a2:var(--warm-2);--ad:var(--warm-d)}
.vx[data-act="cool"]{--a1:var(--cool-1);--a2:var(--cool-2);--ad:var(--cool-d)}
.vx[data-act="fall"]{--a1:#C9CFD4;--a2:#7C868F;--ad:#3A4249}
.vx[data-act="heal"]{--a1:var(--heal-1);--a2:var(--heal-2);--ad:var(--heal-d)}
.vx[data-act="end"]{--a1:#F8899C;--a2:var(--brand);--ad:var(--brand)}
.vx *{box-sizing:border-box}
.vx h1,.vx h2,.vx h3,.vx .jost{font-family:'Jost','Jost Fallback',Arial,sans-serif}
.vx p{margin:0}
.vx__in{max-width:1160px;margin:0 auto;padding:0 40px}
.vx section{padding:96px 0}
.vx .lbl{font-family:'Jost',Arial,sans-serif;font-weight:500;font-size:12px;
  letter-spacing:.22em;text-transform:uppercase;color:var(--ad);
  transition:color .5s}
.vx h2{font-size:clamp(28px,4.2vw,52px);font-weight:500;line-height:1.04;
  letter-spacing:-.01em;margin:12px 0 0}
.vx .lead{font-size:clamp(16px,1.5vw,19px);line-height:1.62;color:var(--mut);
  max-width:64ch;margin-top:18px}
.vx .vx-chev{width:1em;height:1em;display:inline-block;vertical-align:-.12em}
.vx-seek{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);
  background:#fff;border-radius:100px;padding:5px 13px 5px 9px;cursor:pointer;
  font:600 12px/1 'Inter Tight',Arial,sans-serif;color:var(--ink);
  letter-spacing:.02em;transition:border-color .18s,color .18s,background .18s}
.vx-seek:hover{border-color:var(--ad);color:var(--ad)}
.vx-seek__i{width:0;height:0;border:5px solid transparent;border-left:8px solid currentColor;
  margin-left:2px}

/* ── шапка ─────────────────────────────────────────────────────────────── */
.vx-hero{padding:0 0 0;background:var(--bg)}
.vx-hero__top{padding:44px 0 34px}
.vx-back{display:inline-block;font-size:13px;color:var(--mut);text-decoration:none;
  margin-bottom:34px}
.vx-back:hover{color:var(--ink)}
.vx-hero h1{font-size:clamp(42px,8.4vw,116px);font-weight:400;line-height:.94;
  letter-spacing:-.025em;margin:14px 0 0}
.vx-hero h1 em{font-style:normal;font-weight:600;color:var(--ad);transition:color .5s}
.vx-hero__star{margin-top:18px;font-family:'Jost',Arial,sans-serif;font-weight:400;
  font-size:clamp(19px,2.4vw,30px);letter-spacing:.02em;color:var(--ink)}
.vx-hero__sub{margin-top:26px;display:grid;grid-template-columns:1.25fr 1fr;
  gap:40px;align-items:end}
.vx-hero__sub p{font-size:17px;line-height:1.6;color:var(--mut);max-width:52ch}
.vx-hero__cred{font-size:13px;line-height:1.75;color:var(--mut);text-align:right}
.vx-hero__cred b{display:block;color:var(--ink);font-weight:600;font-size:14px}
.vx-hero__lock{display:flex;align-items:center;gap:11px;color:var(--ad);
  font-family:'Jost',Arial,sans-serif;font-weight:500;font-size:14px;
  letter-spacing:.2em;text-transform:uppercase;transition:color .5s}
.vx .vx-hero__lock .vx-chev{width:17px;height:17px;flex:none}

/* плеер */
.vx-player{position:relative;background:#0C0E11;border-radius:4px;overflow:hidden}
.vx-player video{display:block;width:100%;height:auto;background:#0C0E11}
.vx-phases{display:grid;gap:2px;margin-top:2px}
.vx-ph{position:relative;border:0;padding:11px 12px 12px;cursor:pointer;text-align:left;
  background:var(--bg2);color:var(--mut);font:500 11px/1.25 'Inter Tight',Arial,sans-serif;
  transition:background .25s,color .25s;overflow:hidden}
.vx-ph b{display:block;font-family:'Jost',Arial,sans-serif;font-weight:500;font-size:14px;
  letter-spacing:.01em;color:var(--ink);margin-bottom:4px;transition:color .25s}
.vx-ph:hover{background:var(--bg3)}
.vx-ph[aria-current="true"]{background:var(--ink);color:rgba(255,255,255,.62)}
.vx-ph[aria-current="true"] b{color:#fff}
.vx-ph__bar{position:absolute;left:0;bottom:0;height:3px;width:0;
  background:linear-gradient(90deg,var(--a1),var(--a2))}
.vx-ph__t{display:block;font-size:10px;letter-spacing:.08em;opacity:.6;margin-bottom:5px;
  font-family:'Jost',Arial,sans-serif}
.vx-facts{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--line);
  border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:56px}
.vx-facts div{background:var(--bg);padding:24px 20px 26px}
.vx-facts b{display:block;font-family:'Jost',Arial,sans-serif;font-weight:400;
  font-size:clamp(28px,3.4vw,44px);line-height:1;letter-spacing:-.02em}
.vx-facts span{display:block;margin-top:9px;font-size:12px;line-height:1.45;color:var(--mut)}

/* ── три средства ──────────────────────────────────────────────────────── */
.vx-tubes{background:var(--bg2)}
.vx-tubes__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:52px}
.vx-tube{background:#fff;display:flex;flex-direction:column;overflow:hidden}
.vx-tube__ph{position:relative;aspect-ratio:16/9;overflow:hidden;background:#0C0E11}
.vx-tube__ph img{width:100%;height:100%;object-fit:cover;display:block}
.vx-tube__hd{padding:26px 26px 0;display:flex;align-items:center;gap:12px}
.vx-tube__hd .vx-chev{width:30px;height:30px}
.vx-tube--warm .vx-chev{color:var(--warm-2)}
.vx-tube--cool .vx-chev{color:var(--cool-2)}
.vx-tube--heal .vx-chev{color:var(--heal-2)}
.vx-tube__w{font-family:'Jost',Arial,sans-serif;font-weight:400;font-size:23px;
  letter-spacing:.13em;text-transform:uppercase;line-height:1}
.vx-tube__b{padding:20px 26px 26px;display:flex;flex-direction:column;gap:14px;flex:1}
.vx-tube__kind{font-size:12px;line-height:1.5;color:var(--mut);text-transform:uppercase;
  letter-spacing:.06em}
.vx-tube__claim{font-family:'Jost',Arial,sans-serif;font-size:20px;font-weight:500;
  line-height:1.2}
.vx-tube--warm .vx-tube__claim{color:var(--warm-d)}
.vx-tube--cool .vx-tube__claim{color:var(--cool-d)}
.vx-tube--heal .vx-tube__claim{color:var(--heal-d)}
.vx-tube ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:9px}
.vx-tube li{position:relative;padding-left:18px;font-size:13.5px;line-height:1.5;
  color:var(--ink)}
.vx-tube li:before{content:"";position:absolute;left:0;top:8px;width:7px;height:7px;
  border-radius:50%}
.vx-tube--warm li:before{background:var(--warm-2)}
.vx-tube--cool li:before{background:var(--cool-2)}
.vx-tube--heal li:before{background:var(--heal-2)}
.vx-tube__note{margin-top:auto;padding-top:16px;border-top:1px solid var(--line);
  font-size:13px;line-height:1.5;color:var(--mut);display:flex;flex-direction:column;
  gap:12px;align-items:flex-start}
.vx-src{margin-top:26px;font-size:12.5px;color:var(--mut);line-height:1.6}

/* ── мышца ─────────────────────────────────────────────────────────────── */
.vx-muscle{background:#0C0E11;color:#fff;--line:rgba(255,255,255,.14);--mut:#8F979F}
.vx-muscle h2{color:#fff}
.vx-muscle .lbl{color:var(--a2)}
.vx-muscle__wrap{margin-top:48px;border:1px solid var(--line);background:#0F1216}
.vx-muscle__cv{position:relative;width:100%;aspect-ratio:2/1;background:#0F1216}
.vx-muscle__cv canvas{position:absolute;inset:0;width:100%;height:100%;display:block}
.vx-muscle__ctl{display:grid;grid-template-columns:auto 1fr auto;gap:18px;align-items:center;
  padding:16px 22px;border-top:1px solid var(--line)}
.vx-play{width:42px;height:42px;border-radius:50%;border:1px solid var(--line);
  background:transparent;color:#fff;cursor:pointer;display:grid;place-items:center;
  transition:background .18s,border-color .18s}
.vx-play:hover{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.4)}
.vx-play span{width:0;height:0;border:7px solid transparent;border-left:11px solid #fff;
  margin-left:4px}
.vx-play[aria-pressed="true"] span{width:11px;height:13px;border:0;margin:0;
  border-left:4px solid #fff;border-right:4px solid #fff}
.vx-muscle input[type=range]{width:100%;accent-color:#fff;height:22px;cursor:pointer}
.vx-muscle__t{font:500 13px/1 'Jost',Arial,sans-serif;letter-spacing:.08em;
  color:#fff;min-width:86px;text-align:right}
.vx-gauges{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);
  border-top:1px solid var(--line)}
.vx-gauge{background:#0F1216;padding:18px 22px 20px}
.vx-gauge__n{display:flex;justify-content:space-between;align-items:baseline;
  font-size:12px;color:var(--mut);letter-spacing:.04em}
.vx-gauge__n b{font-family:'Jost',Arial,sans-serif;font-weight:400;font-size:26px;
  color:#fff;letter-spacing:-.01em}
.vx-gauge__t{height:3px;background:rgba(255,255,255,.13);margin-top:12px;overflow:hidden}
.vx-gauge__t i{display:block;height:100%;width:0;background:currentColor;
  transition:width .12s linear}
.vx-gauge--flow{color:#F0637A}.vx-gauge--lac{color:#E2B33C}.vx-gauge--swell{color:#7FD455}
.vx-muscle__note{margin-top:22px;font-size:13px;line-height:1.65;color:var(--mut);
  max-width:78ch}
.vx-muscle__cap{position:absolute;left:22px;bottom:18px;right:22px;font-size:13px;
  line-height:1.5;color:rgba(255,255,255,.9);pointer-events:none;max-width:44ch}
.vx-muscle__cap i{font-style:normal;color:var(--mut);display:block;font-size:11.5px;
  letter-spacing:.06em;text-transform:uppercase;margin-bottom:5px}

/* ── роль ──────────────────────────────────────────────────────────────── */
.vx-star__row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:46px}
.vx-face{border:0;background:transparent;padding:0;cursor:pointer;text-align:left;
  font:inherit;color:inherit;display:block;transition:transform .2s}
.vx-face:hover{transform:translateY(-3px)}
.vx-face__ph{display:block;aspect-ratio:16/9;overflow:hidden;background:var(--bg2)}
.vx-face__ph img{width:100%;height:100%;object-fit:cover;display:block}
.vx-face__n{display:block;margin-top:12px;font-size:15px;font-weight:500;line-height:1.3}
.vx-face__t{display:block;margin-top:3px;font:500 11px/1 'Jost',Arial,sans-serif;
  letter-spacing:.1em;color:var(--mut)}

/* ── тело в кадре ──────────────────────────────────────────────────────── */
.vx-frames{margin-top:46px;border-top:1px solid var(--line)}
.vx-fr{width:100%;display:grid;grid-template-columns:250px 1fr auto;gap:26px;
  align-items:center;border:0;border-bottom:1px solid var(--line);background:transparent;
  padding:16px 0;cursor:pointer;text-align:left;font:inherit;color:inherit;
  transition:background .18s,padding .18s}
.vx-fr:hover{background:var(--bg2);padding-left:14px;padding-right:14px}
.vx-fr__ph{display:block;aspect-ratio:16/9;overflow:hidden;background:var(--bg2);
  position:relative}
.vx-fr__ph img{width:100%;height:100%;object-fit:cover;display:block}
.vx-fr__ph:after{content:"";position:absolute;left:0;top:0;bottom:0;width:5px}
.vx-fr--warm .vx-fr__ph:after{background:var(--warm-2)}
.vx-fr--cool .vx-fr__ph:after{background:var(--cool-2)}
.vx-fr--heal .vx-fr__ph:after{background:var(--heal-2)}
.vx-fr--work .vx-fr__ph:after{background:var(--ink)}
.vx-fr__b{display:block;font-size:14.5px;line-height:1.5;color:var(--mut)}
.vx-fr__b b{display:block;font-family:'Jost',Arial,sans-serif;font-weight:500;
  font-size:clamp(19px,2vw,25px);line-height:1.15;color:var(--ink);margin-bottom:6px}
.vx-fr__r{display:flex;align-items:center;gap:18px;white-space:nowrap}
.vx-fr__chip{display:inline-flex;align-items:center;gap:7px;font-size:11px;
  letter-spacing:.1em;text-transform:uppercase;font-weight:600}
.vx-fr__chip .vx-chev{width:14px;height:14px}
.vx-fr--warm .vx-fr__chip{color:var(--warm-d)}
.vx-fr--cool .vx-fr__chip{color:var(--cool-d)}
.vx-fr--heal .vx-fr__chip{color:var(--heal-d)}
.vx-fr__t{font:500 13px/1 'Jost',Arial,sans-serif;letter-spacing:.08em;color:var(--mut)}
.vx-body__legend{margin-top:30px;display:flex;flex-wrap:wrap;gap:26px;
  font-size:13px;color:var(--mut)}
.vx-body__legend span{display:inline-flex;align-items:center;gap:9px}
.vx-body__legend i{width:12px;height:12px;border-radius:3px;display:block}

/* ── тренировка ────────────────────────────────────────────────────────── */
.vx-prog{background:var(--bg2)}
.vx-prog__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:48px}
.vx-card{background:#fff;border:0;padding:0;text-align:left;cursor:pointer;
  display:flex;flex-direction:column;font:inherit;color:inherit;
  transition:transform .2s}
.vx-card:hover{transform:translateY(-3px)}
.vx-card__ph{aspect-ratio:16/9;overflow:hidden;background:var(--bg3);position:relative}
.vx-card__ph img{width:100%;height:100%;object-fit:cover;display:block}
.vx-card__t{position:absolute;left:0;bottom:0;background:var(--ink);color:#fff;
  font:600 11px/1 'Inter Tight',Arial,sans-serif;letter-spacing:.06em;padding:6px 9px}
.vx-card__n{padding:15px 16px 18px;font-size:14px;line-height:1.4;font-weight:500}

/* ── падение ───────────────────────────────────────────────────────────── */
.vx-fall{background:var(--bg)}
.vx-fall__strip{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:46px}
.vx-step{border:0;background:transparent;padding:0;cursor:pointer;text-align:left;
  font:inherit;color:inherit;display:block;transition:transform .2s}
.vx-step:hover{transform:translateY(-3px)}
.vx-step__ph{display:block;aspect-ratio:16/9;overflow:hidden;background:var(--bg2)}
.vx-step__ph img{width:100%;height:100%;object-fit:cover;display:block}
.vx-step__n{display:block;margin-top:12px;font-size:14px;font-weight:500;line-height:1.35}
.vx-step__t{display:block;margin-top:3px;font:500 11px/1 'Jost',Arial,sans-serif;
  letter-spacing:.09em;color:var(--mut)}
.vx-fall__snd{margin-top:44px;display:grid;grid-template-columns:1.6fr 1fr;gap:32px;
  align-items:center;padding-top:30px;border-top:1px solid var(--line)}
.vx-fall__note{font-size:14px;line-height:1.6;color:var(--mut)}
.vx-fall__note .vx-seek{margin-top:14px}
.vx-wave{height:74px;width:100%;display:block}

/* ── смена ─────────────────────────────────────────────────────────────── */
.vx-bts__pair{display:grid;grid-template-columns:minmax(190px,270px) 1fr;
  gap:24px 26px;margin-top:48px;align-items:start}
.vx-bts__cell{background:var(--bg2)}
.vx-bts__cell video,.vx-bts__cell img{display:block;width:100%;height:auto}
.vx-bts__cell--clip video{aspect-ratio:9/16;object-fit:cover;background:#0C0E11}
.vx-bts__cell--shot img{aspect-ratio:16/9;object-fit:cover}
.vx-bts__cap{padding:16px 20px 20px;font-size:13px;line-height:1.55;color:var(--mut)}
.vx-bts__cap b{display:block;font-family:'Jost',Arial,sans-serif;font-weight:500;
  font-size:15px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);
  margin-bottom:7px}
.vx-bts__grid{display:grid;grid-template-columns:repeat(6,1fr);gap:18px;margin-top:22px}
.vx-bts__grid figure{margin:0;grid-column:span 3}
.vx-bts__grid img{width:100%;height:auto;object-fit:cover;display:block;
  aspect-ratio:4/3;background:var(--bg2)}
.vx-bts__grid figcaption{margin-top:11px;font-size:12.5px;line-height:1.5;color:var(--mut)}

/* ── итог ──────────────────────────────────────────────────────────────── */
.vx-out{background:var(--ink);color:#fff}
.vx-out h2{color:#fff}
.vx-out__grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;margin-top:44px}
.vx-out p{font-size:15.5px;line-height:1.7;color:rgba(255,255,255,.72)}
.vx-out p+p{margin-top:16px}
.vx-out b{color:#fff;font-weight:600}
.vx-out__end{margin-top:0}
.vx-out__end img{width:100%;height:auto;display:block}

@media(max-width:1000px){
  .vx__in{padding:0 24px}
  .vx section{padding:72px 0}
  .vx-tubes__grid{grid-template-columns:1fr;gap:18px}
  .vx-facts{grid-template-columns:repeat(2,1fr)}
  .vx-star__row{grid-template-columns:repeat(3,1fr)}
  .vx-fr{grid-template-columns:200px 1fr;gap:18px}
  .vx-fr__r{grid-column:2;gap:14px}
  .vx-fall__strip{grid-template-columns:repeat(3,1fr)}
  .vx-fall__snd{grid-template-columns:1fr;gap:18px}
  .vx-prog__grid{grid-template-columns:repeat(2,1fr)}
  .vx-bts__pair{grid-template-columns:minmax(0,180px) 1fr;gap:16px 18px}
  .vx-bts__grid{grid-template-columns:repeat(2,1fr)}
  .vx-bts__grid{grid-template-columns:repeat(2,1fr)}
  .vx-bts__grid figure{grid-column:span 1}
  .vx-out__grid{grid-template-columns:1fr;gap:28px}
  .vx-hero__sub{grid-template-columns:1fr;gap:22px}
  .vx-hero__cred{text-align:left}
  .vx-muscle__cv{aspect-ratio:16/10}
}
@media(max-width:720px){
  .vx__in{padding:0 18px}
  .vx section{padding:56px 0}
  .vx-hero__top{padding:26px 0 24px}
  .vx-facts{grid-template-columns:1fr}
  .vx-facts div{padding:18px 18px 20px}
  .vx-phases{grid-template-columns:1fr!important}
  .vx-ph__t{display:inline-block;margin:0 8px 0 0}
  .vx-prog__grid{grid-template-columns:1fr}
  .vx-star__row{grid-template-columns:repeat(2,1fr)}
  .vx-fr{grid-template-columns:126px 1fr;gap:14px;padding:14px 0}
  .vx-fr__b b{font-size:18px}
  .vx-fr__r{grid-column:1/-1;gap:12px}
  .vx-fall__strip{grid-template-columns:repeat(2,1fr)}
  .vx-muscle__ctl{grid-template-columns:auto 1fr;row-gap:10px}
  .vx-muscle__t{grid-column:2;text-align:left}
  .vx-gauges{grid-template-columns:1fr}
  .vx-tube__hd,.vx-tube__b{padding-left:20px;padding-right:20px}
  .vx-muscle__cv{aspect-ratio:4/3}
  .vx-muscle__cap{position:static;padding:0 18px 16px;max-width:none}
}
@media(prefers-reduced-motion:reduce){
  .vx *{transition-duration:.01ms!important;animation-duration:.01ms!important}
}
</style>"""

CSS = (CSS.replace('%BRAND%', PAL['brand']['dark'])
          .replace('%WARM1%', PAL['warm']['light']).replace('%WARM2%', PAL['warm']['dark'])
          .replace('%COOL1%', PAL['cool']['light']).replace('%COOL2%', PAL['cool']['dark'])
          .replace('%HEAL1%', PAL['heal']['light']).replace('%HEAL2%', PAL['heal']['dark']))


# ══ шапка ═════════════════════════════════════════════════════════════════
def hero():
    ph = ''
    for pid, a, b, name, note in PHASES:
        ph += (f'<button class="vx-ph" type="button" data-ph="{pid}" data-a="{a}" '
               f'data-b="{b}" data-seek="{a}">'
               f'<span class="vx-ph__t">{mmss(a)}</span><b>{name}</b>{note}'
               f'<span class="vx-ph__bar"></span></button>')
    cols = ' '.join(f'minmax(min-content,{(b - a) / DURATION * 100:.2f}fr)'
                    for _, a, b, _, _ in PHASES)
    facts = [
        (num(DURATION) + ' с', 'Хронометраж ролика'),
        (str(STATS['shots']), 'Планов в монтаже'),
        (num(STATS['film_mean']) + ' с', 'Средняя длина плана до заставки'),
        ('3', 'Средства линейки в одном сюжете'),
        ('1', 'Смена в зале X-Fit'),
    ]
    f = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in facts)
    return (
      '<section class="vx-hero"><div class="vx__in">'
      '<div class="vx-hero__top">'
      '<a class="vx-back" href="/project">← Все проекты</a>'
      '<div class="vx-hero__lock">' + chev() +
      'VIVAX Sport · Video Production</div>'
      '<h1>Ты сможешь<br><em>больше</em></h1>'
      '<div class="vx-hero__star">Настасья Самбурская</div>'
      '<div class="vx-hero__sub">'
      '<p>Вирусный ролик спортивных средств VIVAX. Тренировка с комичными '
      'ситуациями, в которые попадает героиня, и вся линейка внутри одного '
      'сюжета: разогрев до нагрузки, восстановление после и реабилитация '
      'после падения.</p>'
      '<div class="vx-hero__cred"><b>Академия Научной Красоты</b>'
      'Продакшн, сценарий, кастинг, съёмка и монтаж<br>'
      'Зал X-Fit, съёмка на RED, одна смена</div>'
      '</div></div>'
      f'<div class="vx-player"><video id="vx-video" controls preload="metadata" '
      f'playsinline poster="{IMG}/rest-smile.jpg" '
      f'aria-label="Рекламный ролик VIVAX SPORT с Настасьей Самбурской">'
      f'<source src="{VIDEO}" type="video/mp4"></video></div>'
      f'<div class="vx-phases" style="grid-template-columns:{cols}">{ph}</div>'
      f'<div class="vx-facts">{f}</div>'
      '</div></section>')


# ══ три средства ══════════════════════════════════════════════════════════
def tubes():
    cards = ''
    for t in TUBES:
        li = ''.join(f'<li>{b}</li>' for b in t['bullets'])
        cards += (
          f'<article class="vx-tube vx-tube--{t["id"]}">'
          f'<div class="vx-tube__ph">{pic(t["still"], "(max-width:1000px) 100vw, 33vw")}</div>'
          f'<div class="vx-tube__hd">{chev()}'
          f'<span class="vx-tube__w">{t["word"]}</span></div>'
          f'<div class="vx-tube__b">'
          f'<div class="vx-tube__kind">{t["kind"]}</div>'
          f'<div class="vx-tube__claim">{t["claim"]}</div>'
          f'<ul>{li}</ul>'
          f'<div class="vx-tube__note">{t["note"]}'
          f'{seek(t["sec"], "Титр в ролике · " + mmss(t["sec"]))}</div>'
          f'</div></article>')
    return (
      '<section class="vx-tubes"><div class="vx__in">'
      '<div class="lbl">Линейка</div>'
      '<h2>Три средства, три состояния мышцы</h2>'
      '<p class="lead">Сюжет ролика это и есть продуктовая линейка: до нагрузки, '
      'после нагрузки и после травмы. Каждое средство появляется своим титром '
      'и своим цветом, шеврон в титре это знак VIVAX. Ниже обещания взяты '
      'не из брифа, а прочитаны прямо с упаковки в кадре.</p>'
      f'<div class="vx-tubes__grid">{cards}</div>'
      '<p class="vx-src">Текст на тюбиках снят с кадров 5,85 с, 23,95 с '
      'и 39,40 с и приведён слово в слово, включая мелкий шрифт.</p>'
      '</div></section>')


# ══ главная роль ══════════════════════════════════════════════════════════
def star():
    cards = ''
    for sec, slug, name in STAR:
        cards += (f'<button class="vx-face" type="button" data-seek="{sec}">'
                  f'<span class="vx-face__ph">'
                  f'{pic(slug, "(max-width:720px) 44vw, (max-width:1000px) 30vw, 16vw")}'
                  f'</span><span class="vx-face__n">{name}</span>'
                  f'<span class="vx-face__t">{mmss(sec)}</span></button>')
    return (
      '<section class="vx-star"><div class="vx__in">'
      '<div class="lbl">Главная роль</div>'
      '<h2>Настасья Самбурская</h2>'
      '<p class="lead">Вирусным ролик делает не тюбик, а актриса и то, что '
      'с ней происходит. За 49 секунд Самбурская успевает отыграть '
      'собранность, раздражение, кураж, растерянность после падения, боль '
      'и облегчение. Нажмите на кадр, ролик перемотается на него.</p>'
      f'<div class="vx-star__row">{cards}</div>'
      '</div></section>')


# ══ мышца ═════════════════════════════════════════════════════════════════
def muscle():
    g = ''
    for cls, name, unit in (('flow', 'Кровоток', 'vx-g-flow'),
                            ('lac', 'Лактат', 'vx-g-lac'),
                            ('swell', 'Отёк и гематома', 'vx-g-swell')):
        g += (f'<div class="vx-gauge vx-gauge--{cls}">'
              f'<div class="vx-gauge__n">{name}<b id="{unit}">0 %</b></div>'
              f'<div class="vx-gauge__t"><i id="{unit}-t"></i></div></div>')
    return (
      '<section class="vx-muscle"><div class="vx__in">'
      '<div class="lbl">Что продаёт ролик</div>'
      '<h2>Мышца за те же 49 секунд</h2>'
      '<p class="lead">Разрез мышцы проходит ролик синхронно с ним. Тяните '
      'ползунок или нажмите воспроизведение: капилляры раскрываются на '
      'разогреве, под нагрузкой копится лактат, после синего геля он уходит, '
      'а после падения появляется тот самый ушиб, который затягивается '
      'зелёным кремом.</p>'
      '<div class="vx-muscle__wrap">'
      '<div class="vx-muscle__cv"><canvas id="vx-cv" role="img" '
      'aria-label="Схема продольного разреза мышцы: кровоток, лактат и ушиб '
      'меняются по ходу ролика"></canvas>'
      '<div class="vx-muscle__cap" id="vx-cap"></div></div>'
      '<div class="vx-muscle__ctl">'
      '<button class="vx-play" id="vx-mplay" type="button" aria-pressed="false" '
      'aria-label="Проиграть схему"><span></span></button>'
      f'<input id="vx-range" type="range" min="0" max="{DURATION}" step="0.04" '
      'value="0" aria-label="Секунда ролика">'
      '<div class="vx-muscle__t" id="vx-mt">0:00</div>'
      '</div>'
      f'<div class="vx-gauges">{g}</div>'
      '</div>'
      '<p class="vx-muscle__note">Схема нарисована по обещаниям с упаковки '
      'и по хронологии ролика: разогрев улучшает микроциркуляцию, гель '
      'способствует выведению молочной кислоты и оказывает противоотёчное '
      'действие, регенерирующий крем рассасывает гематомы при ушибах. '
      'Это иллюстрация заявленного производителем действия, а не измерение.</p>'
      '</div></section>')


# ══ тело в кадре ══════════════════════════════════════════════════════════
def frames():
    rows = ''
    for zid, name, tube, sec, slug, note in ZONES:
        chip = ('' if tube == 'work' else
                f'<span class="vx-fr__chip">{chev()}{ZONE_TUBE[tube]}</span>')
        rows += (
          f'<button class="vx-fr vx-fr--{tube}" type="button" data-seek="{sec}">'
          f'<span class="vx-fr__ph">'
          f'{pic(slug, "(max-width:720px) 40vw, (max-width:1000px) 34vw, 250px")}'
          f'</span>'
          f'<span class="vx-fr__b"><b>{name}</b>{note}</span>'
          f'<span class="vx-fr__r">{chip}'
          f'<span class="vx-fr__t">{mmss(sec)}</span></span></button>')
    leg = ''
    for k, nm in (('warm', 'Разогрев'), ('cool', 'Восстановление'),
                  ('heal', 'Реабилитация'), ('work', 'В работе, без средства')):
        c = {'warm': 'var(--warm-2)', 'cool': 'var(--cool-2)',
             'heal': 'var(--heal-2)', 'work': 'var(--ink)'}[k]
        leg += f'<span><i style="background:{c}"></i>{nm}</span>'
    return (
      '<section class="vx-body"><div class="vx__in">'
      '<div class="lbl">Оптика ролика</div>'
      '<h2>Тело в кадре</h2>'
      f'<p class="lead">Из {STATS["shots"]} планов в ролике почти нет общих: '
      'средство наносят на мышцу, и камера говорит фрагментами тела. Ниже '
      'ролик пересобран сверху вниз, от шеи до стопы: каждая строка это '
      'кадр, в котором эта зона действительно попадает в объектив, '
      'и средство, которое к ней применяют по сюжету.</p>'
      f'<div class="vx-frames">{rows}</div>'
      f'<div class="vx-body__legend">{leg}</div>'
      '</div></section>')


# ══ тренировка и падение ══════════════════════════════════════════════════
def programme():
    cards = ''
    for sec, name, slug in PROGRAMME:
        cards += (f'<button class="vx-card" type="button" data-seek="{sec}">'
                  f'<div class="vx-card__ph">'
                  f'{pic(slug, "(max-width:720px) 100vw, (max-width:1000px) 50vw, 25vw")}'
                  f'<span class="vx-card__t">{mmss(sec)}</span></div>'
                  f'<div class="vx-card__n">{name}</div></button>')
    # огибающая громкости: показываем, где музыка уходит в тишину
    db = MAP['loudness']
    n = len(db)
    pts = []
    for i, v in enumerate(db):
        x = i / (n - 1) * 1000
        y = 74 - max(0.0, min(1.0, (v + 45) / 45)) * 68
        pts.append(f'{x:.1f} {y:.1f}')
    poly = 'M0 74 L' + ' L'.join(pts) + ' L1000 74 Z'
    qa = QUIET[0] / DURATION * 1000
    qb = QUIET[1] / DURATION * 1000
    wave = (f'<svg class="vx-wave" viewBox="0 0 1000 74" preserveAspectRatio="none" '
            f'aria-hidden="true">'
            f'<rect x="{qa:.1f}" y="0" width="{qb - qa:.1f}" height="74" '
            f'fill="rgba(20,23,28,.08)"/>'
            f'<path d="{poly}" fill="var(--ink)" opacity=".82"/></svg>')
    strip = ''
    for sec, slug, name in FALL:
        strip += (f'<button class="vx-step" type="button" data-seek="{sec}">'
                  f'<span class="vx-step__ph">'
                  f'{pic(slug, "(max-width:720px) 44vw, (max-width:1000px) 30vw, 20vw")}'
                  f'</span><span class="vx-step__n">{name}</span>'
                  f'<span class="vx-step__t">{num(sec)} с</span></button>')
    return (
      '<section class="vx-prog"><div class="vx__in">'
      '<div class="lbl">Что она делает в кадре</div>'
      '<h2>Тренировка за 49 секунд</h2>'
      '<p class="lead">Полноценная тренировка, разложенная по планам: '
      'набивной мяч, бодибар, приседания, работа по лапам с тренером '
      'и растяжка. Нажмите на карточку, ролик перемотается на это '
      'упражнение.</p>'
      f'<div class="vx-prog__grid">{cards}</div>'
      '</div></section>'

      '<section class="vx-fall"><div class="vx__in">'
      '<div class="lbl">Кульминация</div>'
      '<h2>Падение, которого не показали</h2>'
      '<p class="lead">Клиент просил серию комичных ситуаций, и главная из них '
      'построена на том, чего в кадре нет. Героиня наступает на край блина '
      'от штанги, лежащего на полу, '
      'взмахивает руками и уходит вниз за нижнюю границу кадра. Дальше идёт '
      f'самый длинный снятый план ролика, {num(STATS["film_max"])} с пустого '
      f'зала, и на {num(round(QUIET[1] - QUIET[0], 2))} секунды музыка уходит '
      'почти в ноль. Только потом Самбурская выныривает обратно, ошарашенная. '
      'Само падение зритель достраивает сам.</p>'
      f'<div class="vx-fall__strip">{strip}</div>'
      '<div class="vx-fall__snd">'
      f'{wave}'
      '<div class="vx-fall__note">Громкость дорожки по всему ролику. Провал '
      f'на {num(QUIET[0])}–{num(QUIET[1])} с это и есть тишина на месте '
      'падения, единственная во всём ролике.'
      f'<br>{seek(28.28, "Смотреть сцену · " + mmss(28.28))}</div>'
      '</div></div></section>')


# ══ смена ═════════════════════════════════════════════════════════════════
def bts():
    c = CLIPS['bts-pads']
    # сколько эта сцена реально идёт в ролике: длина плана, в который попал кадр
    pads_len = next(round(b - a, 2) for a, b in SHOTS
                    if a <= SEC['ex-pads'] < b)
    pair = (
      '<div class="vx-bts__cell vx-bts__cell--clip">'
      f'<video class="vx-clip" muted loop playsinline preload="none" '
      f'poster="{IMG}/bts-pads-s.jpg" aria-label="{c["what"]}">'
      f'<source src="{c["url"]}" type="video/mp4"></video>'
      f'<div class="vx-bts__cap"><b>Как снимали</b>{c["what"]}</div></div>'
      '<div class="vx-bts__cell vx-bts__cell--shot">'
      f'{pic("ex-pads", "(max-width:1000px) 100vw, 60vw")}'
      f'<div class="vx-bts__cap"><b>Что в ролике</b>{num(pads_len)} секунды '
      f'экранного времени.<br>{seek(SEC["ex-pads"])}</div></div>')
    ph = ''
    for slug in SET_ORDER:
        ph += (f'<figure>{photo(slug, "(max-width:1000px) 50vw, 25vw")}'
               f'<figcaption>{PHOTOS[slug]["what"]}</figcaption></figure>')
    return (
      '<section class="vx-bts"><div class="vx__in">'
      '<div class="lbl">Съёмка</div>'
      '<h2>По ту сторону камеры</h2>'
      '<p class="lead">Клип со смены снят ровно на той сцене с лапами, что '
      'стоит в ролике на 19-й секунде: тренер отходит спиной вперёд, камера '
      'едет рядом с рук. Слева площадка, справа то, что из неё получилось.</p>'
      f'<div class="vx-bts__pair">{pair}</div>'
      f'<div class="vx-bts__grid">{ph}</div>'
      '</div></section>')


# ══ итог ══════════════════════════════════════════════════════════════════
def outro():
    return (
      '<section class="vx-out"><div class="vx__in">'
      '<div class="lbl">Задача и решение</div>'
      '<h2>Что от нас требовалось</h2>'
      '<div class="vx-out__grid">'
      '<div><p>Снять вирусный ролик о спортивных средствах VIVAX для компании '
      '«Академия Научной Красоты». VIVAX производит лечебно-профилактические '
      'и гигиенические средства на активных пептидных комплексах. «Академия '
      'Научной Красоты» это эксклюзивный дистрибьютор профессиональной '
      'косметики, инъекционных препаратов и оборудования для индустрии '
      'красоты, медицинских клиник и спортивных центров в России, СНГ '
      'и странах Балтии.</p>'
      '<p>На главную роль пригласили актрису <b>Настасью Самбурскую</b>. '
      'Сценарий собран из комичных ситуаций, в которые она попадает '
      'на тренировке в фитнес-центре <b>X-FIT</b>: дразнящая лапа над головой, '
      'неудачный шаг на блин от штанги, падение за кадром и ушиб, из-за '
      'которого в сюжете появляется третье средство линейки.</p></div>'
      '<div><p>Такая конструкция позволила показать всю линейку в одном сюжете, '
      'не разбивая его на три отдельных ролика: каждый тюбик выходит там, где '
      'он и нужен по ходу тренировки, и получает свой титр фирменным '
      'шевроном.</p>'
      f'<p>Итог: {num(DURATION)} секунды, {STATS["shots"]} '
      f'{plural(STATS["shots"], "план", "плана", "планов")}, из них '
      f'{STATS["film_shots"]} снятых, средняя длина {num(STATS["film_mean"])} с. '
      'Ролик закрывается заставкой с обещанием бренда.</p>'
      f'<div class="vx-out__end">{pic("endcard", "(max-width:1000px) 100vw, 50vw")}</div>'
      '</div></div>'
      '</div></section>')


# ══ JS ════════════════════════════════════════════════════════════════════
PAGE_JS = """<script>(function(){
var PHASES=%PHASES%,DUR=%DUR%;
var root=document.querySelector('.vx');
if(!root)return;
var video=document.getElementById('vx-video');
var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;

function mmss(s){s=Math.max(0,s);return Math.floor(s/60)+':'+('0'+Math.round(s%60)).slice(-2);}

/* ── перемотка: любая кнопка data-seek ведёт плеер ───────────────────── */
function seekTo(sec,scroll){
  if(!video)return;
  try{video.currentTime=sec;}catch(e){}
  setAct(sec);
  if(scroll!==false){
    var r=video.getBoundingClientRect();
    if(r.top<0||r.bottom>innerHeight)
      video.scrollIntoView({block:'center',behavior:RM?'auto':'smooth'});
  }
  var p=video.play();if(p&&p.catch)p.catch(function(){});
}
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-seek]');
  if(!b||!root.contains(b))return;
  e.preventDefault();seekTo(parseFloat(b.getAttribute('data-seek')),true);
});

/* ── палитра страницы идёт за головкой воспроизведения ───────────────── */
var phBtns=[].slice.call(document.querySelectorAll('.vx-ph'));
function setAct(t){
  var cur=PHASES[0];
  for(var i=0;i<PHASES.length;i++)if(t>=PHASES[i][1])cur=PHASES[i];
  if(root.getAttribute('data-act')!==cur[0])root.setAttribute('data-act',cur[0]);
  phBtns.forEach(function(b){
    var a=parseFloat(b.getAttribute('data-a')),z=parseFloat(b.getAttribute('data-b'));
    var on=t>=a&&t<z;
    b.setAttribute('aria-current',on?'true':'false');
    var bar=b.querySelector('.vx-ph__bar');
    if(bar)bar.style.width=(t<=a?0:t>=z?100:(t-a)/(z-a)*100)+'%';
  });
}
if(video){
  video.addEventListener('timeupdate',function(){
    setAct(video.currentTime);
    if(!dragging&&!mplaying)setT(video.currentTime,false);
  });
  video.addEventListener('seeked',function(){setAct(video.currentTime);});
  video.addEventListener('ended',function(){setAct(0);});
}
setAct(0);

/* ── клипы со смены: тихо крутятся, когда видны ──────────────────────── */
var clips=[].slice.call(document.querySelectorAll('.vx-clip'));
if(clips.length&&'IntersectionObserver' in window){
  var co=new IntersectionObserver(function(es){
    es.forEach(function(en){
      var v=en.target;
      if(en.isIntersecting){if(!RM){var p=v.play();if(p&&p.catch)p.catch(function(){});}}
      else v.pause();
    });
  },{threshold:.35});
  clips.forEach(function(v){co.observe(v);});
}

/* ── разрез мышцы ────────────────────────────────────────────────────── */
var cv=document.getElementById('vx-cv');
if(cv&&cv.getContext){
  var ctx=cv.getContext('2d'),W=0,H=0,DPR=1;
  var range=document.getElementById('vx-range'),mplay=document.getElementById('vx-mplay'),
      mt=document.getElementById('vx-mt'),cap=document.getElementById('vx-cap');
  var t=0,mplaying=false,dragging=false,raf=0,last=0;

  /* ключевые кадры сигналов: по хронологии ролика и по обещаниям с тюбиков */
  var K={
    flow:[[0,.20],[5.04,.20],[6.9,.55],[9.68,.88],[23.48,.92],[26,.80],[30,.55],
          [35.3,.50],[36.6,.72],[38.4,.68],[41,.48],[49.28,.40]],
    heat:[[0,.04],[5.04,.04],[7.4,.55],[9.68,.92],[23.48,.86],[27,.5],[33,.28],
          [49.28,.18]],
    load:[[0,0],[9.5,0],[10.2,1],[23.0,1],[23.9,0],[49.28,0]],
    lac :[[0,0],[9.68,.02],[16,.55],[23.48,1],[24.8,.96],[28,.55],[31,.28],
          [34,.14],[49.28,.10]],
    sw  :[[0,0],[35.0,0],[35.6,.85],[36.6,1],[38.4,.98],[39.9,.9],[41,.5],
          [42.1,.28],[49.28,.20]]
  };
  function val(k,x){
    var a=K[k];
    if(x<=a[0][0])return a[0][1];
    for(var i=1;i<a.length;i++){
      if(x<=a[i][0]){
        var u=(x-a[i-1][0])/(a[i][0]-a[i-1][0]);
        u=u*u*(3-2*u);
        return a[i-1][1]+(a[i][1]-a[i-1][1])*u;
      }
    }
    return a[a.length-1][1];
  }
  /* подписи: что именно сейчас показывает схема, словами с упаковки */
  var CAPS=[
    [0,'Покой','Мышца до тренировки: кровоток базовый, волокна расслаблены.'],
    [5.04,'Разогрев','«Глубоко разогревает мышцы и связки, подготавливая '+
      'к нагрузкам», «улучшает микроциркуляцию крови»: капилляры раскрываются.'],
    [9.68,'Нагрузка','Волокна работают, в мышце копится молочная кислота.'],
    [23.48,'Восстановление','«Способствует выведению молочной кислоты», '+
      '«снимает болевые ощущения и мышечный спазм»: лактат уходит с кровотоком.'],
    [28.08,'Падение','Она оступается на блине от штанги и уходит из кадра.'],
    [35.32,'Ушиб','Гематома и отёк на локте: цена того падения.'],
    [38.36,'Реабилитация','«Быстро рассасывает гематомы и отёки при ушибах»: '+
      'разрыв затягивается, отёк спадает.'],
    [42.04,'Итог','Мышца вернулась в работу. Ролик уходит на заставку.']
  ];

  /* детерминированная геометрия: одна и та же картинка при каждой отрисовке */
  function rnd(s){return function(){s=(s*16807)%2147483647;return s/2147483647;};}
  var R=rnd(20170529),NB=11,FIB=[],BND=[],CAP=[];
  for(var i=0;i<NB;i++){FIB.push({tone:R()*2-1});}
  for(var i2=0;i2<=NB;i2++){
    var o=-1+2*i2/NB;
    BND.push({o:o,ph:R()*6.283,amp:(.45+R()*.85)*(1-Math.abs(o))});
  }
  for(var j=0;j<11;j++){CAP.push({y:R()*2-1,ph:R()*6.283,amp:.4+R()*.9,w:.5+R()*.8});}
  var LAC=[];
  for(var k=0;k<120;k++){LAC.push({x:R(),y:R()*2-1,r:.55+R()*.85,ph:R()*6.283});}

  function fit(){
    var r=cv.getBoundingClientRect();
    DPR=Math.min(2,window.devicePixelRatio||1);
    W=Math.max(300,Math.round(r.width));H=Math.max(160,Math.round(r.height));
    cv.width=Math.round(W*DPR);cv.height=Math.round(H*DPR);
    ctx.setTransform(DPR,0,0,DPR,0,0);
    draw();
  }
  /* контур брюшка: веретено, к сухожилиям сходит в нить */
  function belly(u){
    u=Math.min(1,Math.max(0,u));
    return .06+.94*Math.pow(Math.sin(Math.PI*u),.62);
  }
  function draw(){
    if(!W)return;
    var flow=val('flow',t),heat=val('heat',t),load=val('load',t),
        lac=val('lac',t),sw=val('sw',t);
    var pulse=load?(.5+.5*Math.sin(t*7.2)):0;
    /* сокращение: мышца короче и толще */
    var padX=W*.055,padY=H*.10;
    var bw=(W-padX*2)*(1-.055*load*pulse);
    var bh=(H-padY*2)*(1+.10*load*pulse);
    var cy=H/2,x0=(W-bw)/2,N=44;
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='#0F1216';ctx.fillRect(0,0,W,H);
    /* сухожилия по краям */
    ctx.strokeStyle='rgba(226,226,226,.30)';ctx.lineWidth=Math.max(2,H*.012);
    ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(padX*.35,cy);ctx.lineTo(x0+2,cy);
    ctx.moveTo(W-padX*.35,cy);ctx.lineTo(x0+bw-2,cy);ctx.stroke();
    /* пучки волокон заливкой */
    /* границы пучков считаются один раз и переиспользуются соседями */
    var EDGE=[];
    for(var e0=0;e0<=NB;e0++){
      var b0=BND[e0],row=[];
      for(var s0=0;s0<=N;s0++){
        var uu=s0/N,thh=belly(uu)*bh/2;
        row.push(cy+b0.o*thh+
          Math.sin(uu*6.1+b0.ph+t*(load?2.6:.45))*bh*.045*b0.amp*belly(uu));
      }
      EDGE.push(row);
    }
    for(var i=0;i<NB;i++){
      var f=FIB[i],ea=EDGE[i],eb=EDGE[i+1];
      ctx.beginPath();
      for(var s1=0;s1<=N;s1++){
        if(s1===0)ctx.moveTo(x0,ea[0]);else ctx.lineTo(x0+s1/N*bw,ea[s1]);
      }
      for(var s2=N;s2>=0;s2--)ctx.lineTo(x0+s2/N*bw,eb[s2]);
      ctx.closePath();
      /* тон ткани: от приглушённого к разогретому */
      var r0=78+heat*128+f.tone*11,g0=56-heat*12+f.tone*5,b0c=64-heat*10+f.tone*5;
      var mid=(BND[i].o+BND[i+1].o)/2;
      var depth=1-Math.abs(mid)*.26;            /* края темнее: объём */
      ctx.fillStyle='rgb('+Math.round(r0*depth)+','+Math.round(g0*depth)+','+
        Math.round(b0c*depth)+')';
      ctx.fill();
      ctx.strokeStyle='rgba(10,12,15,.62)';ctx.lineWidth=1.1;ctx.stroke();
    }
    /* поперечная исчерченность: заметнее под нагрузкой */
    ctx.save();
    ctx.globalAlpha=.07+load*.12;
    ctx.strokeStyle='#F2D9DC';ctx.lineWidth=1;
    var step=Math.max(11,bw/40);
    for(var xs=x0+step;xs<x0+bw-step;xs+=step){
      var u3=(xs-x0)/bw,th4=belly(u3)*bh/2*.94;
      var sh=Math.sin(u3*3.2+t*(load?3.4:0))*th4*.06;
      ctx.beginPath();ctx.moveTo(xs,cy-th4+sh);ctx.lineTo(xs,cy+th4+sh);ctx.stroke();
    }
    ctx.restore();
    /* оболочка */
    ctx.beginPath();
    for(var s3=0;s3<=N;s3++){
      if(s3===0)ctx.moveTo(x0,EDGE[0][0]);else ctx.lineTo(x0+s3/N*bw,EDGE[0][s3]);}
    for(var s4=N;s4>=0;s4--)ctx.lineTo(x0+s4/N*bw,EDGE[NB][s4]);
    ctx.closePath();
    ctx.strokeStyle='rgba(255,255,255,.26)';ctx.lineWidth=1.4;ctx.stroke();
    /* капилляры: толщина и яркость = кровоток */
    ctx.save();
    if(flow>.45){ctx.shadowColor='rgba(240,99,122,.55)';ctx.shadowBlur=6+flow*10;}
    for(var j2=0;j2<CAP.length;j2++){
      var c=CAP[j2];
      ctx.beginPath();
      for(var s5=0;s5<=N;s5++){
        var u6=s5/N,th5=belly(u6)*bh/2;
        var y4=cy+c.y*th5*.88+Math.sin(u6*9+c.ph)*th5*.16*c.amp;
        if(s5===0)ctx.moveTo(x0+u6*bw,y4);else ctx.lineTo(x0+u6*bw,y4);
      }
      ctx.strokeStyle='rgba(244,110,132,'+(.10+flow*.72).toFixed(3)+')';
      ctx.lineWidth=(.5+flow*2.6)*c.w;
      ctx.stroke();
    }
    ctx.restore();
    /* лактат */
    var n2=Math.round(lac*LAC.length);
    for(var k2=0;k2<n2;k2++){
      var p=LAC[k2];
      var u7=.05+p.x*.9,th6=belly(u7)*bh/2;
      var px=x0+(u7+(1-lac)*.05)*bw;
      var py=cy+p.y*th6*.86+Math.sin(t*1.6+p.ph)*bh*.012;
      ctx.beginPath();ctx.arc(px,py,p.r*Math.max(1.6,bh*.012),0,6.283);
      ctx.fillStyle='rgba(232,187,66,'+(.4+lac*.5).toFixed(3)+')';ctx.fill();
    }
    /* разрыв и отёк */
    if(sw>.01){
      var tx=x0+bw*.68,ty=cy-belly(.68)*bh/2*.42;
      var rad=bh*(.16+.20*sw);
      var healed=t>=38.36?Math.min(1,(t-38.36)/3.6):0;
      var cr=Math.round(216-104*healed),cg=Math.round(44+152*healed),
          cb=Math.round(62+22*healed);
      var g=ctx.createRadialGradient(tx,ty,2,tx,ty,rad);
      g.addColorStop(0,'rgba('+cr+','+cg+','+cb+','+(.62*sw).toFixed(3)+')');
      g.addColorStop(1,'rgba('+cr+','+cg+','+cb+',0)');
      ctx.fillStyle=g;ctx.beginPath();ctx.arc(tx,ty,rad,0,6.283);ctx.fill();
      var gap=bh*.07*sw;
      ctx.beginPath();
      ctx.moveTo(tx-bw*.042,ty-gap*.6);ctx.lineTo(tx+bw*.046,ty-gap*1.1);
      ctx.lineTo(tx+bw*.02,ty+gap*.95);ctx.lineTo(tx-bw*.046,ty+gap*.55);
      ctx.closePath();
      ctx.fillStyle='rgba(13,15,19,'+(.88*sw).toFixed(3)+')';ctx.fill();
      ctx.strokeStyle='rgba('+cr+','+cg+','+cb+','+(.92*sw).toFixed(3)+')';
      ctx.lineWidth=1.5;ctx.stroke();
    }
    /* подписи */
    if(range)range.value=t;
    if(mt)mt.textContent=mmss(t)+' / '+mmss(DUR);
    gauge('vx-g-flow',flow);gauge('vx-g-lac',lac);gauge('vx-g-swell',sw);
    var c2=CAPS[0];
    for(var q=0;q<CAPS.length;q++)if(t>=CAPS[q][0])c2=CAPS[q];
    if(cap&&cap.getAttribute('data-k')!==c2[1]){
      cap.setAttribute('data-k',c2[1]);
      cap.innerHTML='<i>'+c2[1]+'</i>'+c2[2];
    }
  }
  function gauge(id,v){
    var b=document.getElementById(id),tr=document.getElementById(id+'-t');
    if(b)b.textContent=Math.round(v*100)+' %';
    if(tr)tr.style.width=(v*100).toFixed(1)+'%';
  }
  window.setT=function(v,stopVideo){
    t=Math.max(0,Math.min(DUR,v));
    if(stopVideo&&video&&!video.paused)video.pause();
    draw();
  };
  if(range){
    range.addEventListener('input',function(){
      dragging=true;stopM();setT(parseFloat(range.value),true);
    });
    range.addEventListener('change',function(){dragging=false;});
  }
  function stopM(){
    mplaying=false;if(raf)cancelAnimationFrame(raf);raf=0;
    if(mplay)mplay.setAttribute('aria-pressed','false');
  }
  function startM(){
    if(RM){setT(DUR,true);return;}
    if(video&&!video.paused)video.pause();
    mplaying=true;mplay.setAttribute('aria-pressed','true');
    if(t>=DUR-.05)t=0;
    last=performance.now();
    raf=requestAnimationFrame(function step(now){
      var dt=(now-last)/1000;last=now;
      t+=dt;
      if(t>=DUR){t=DUR;draw();stopM();return;}
      draw();raf=requestAnimationFrame(step);
    });
  }
  if(mplay)mplay.addEventListener('click',function(){mplaying?stopM():startM();});
  /* один раз проигрываем схему сама, когда до неё доскроллили: блок должен
     объяснять себя без нажатия */
  if(!RM&&'IntersectionObserver' in window){
    var once=new IntersectionObserver(function(es){
      es.forEach(function(en){
        if(en.isIntersecting){once.disconnect();
          if(!mplaying&&t<.05&&(!video||video.paused))startM();}
      });
    },{threshold:.5});
    once.observe(cv);
  }
  window.addEventListener('resize',fit);
  if('ResizeObserver' in window)new ResizeObserver(fit).observe(cv);
  fit();
  document.addEventListener('visibilitychange',function(){if(document.hidden)stopM();});
}else{window.setT=function(){};}
})();</script>"""


BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Video","item":"https://hand-marketing.ru/videoproduction/"},'
  '{"@type":"ListItem","position":3,"name":"Рекламный ролик VIVAX SPORT с Настасьей Самбурской",'
  f'"item":"{URL}"}}]}}</script>')

VIDEO_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"VideoObject","name":"Рекламный ролик VIVAX SPORT с Настасьей Самбурской",'
  '"description":"Вирусный ролик спортивных средств VIVAX SPORT с актрисой '
  'Настасьей Самбурской для компании «Академия Научной Красоты».",'
  f'"thumbnailUrl":"https://hand-marketing.ru{IMG}/rest-smile.jpg",'
  f'"contentUrl":"https://hand-marketing.ru{VIDEO}",'
  '"uploadDate":"2026-08-31","duration":"PT49S"}</script>')

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
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/rest-smile.jpg">'
        '<link rel="stylesheet" href="/fonts/jost-intertight.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    phases = [[p[0], p[1], p[2]] for p in PHASES]
    js = (PAGE_JS.replace('%PHASES%', json.dumps(phases))
                 .replace('%DUR%', str(DURATION)))
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="vx" data-act="none">{hero()}{tubes()}{star()}'
            f'{muscle()}{frames()}{programme()}{bts()}{outro()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{js}'
            f'{BREADCRUMB_LD}{VIDEO_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'vivax')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('· удалён index-a2.html (деплой затёр бы им кастомную страницу)')
    print(f'✓ {os.path.relpath(p, os.path.dirname(ROOT))} '
          f'({os.path.getsize(p) / 1024:.0f} КБ)')
