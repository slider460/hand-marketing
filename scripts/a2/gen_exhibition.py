#!/usr/bin/env python3
"""Генерит mirror/exhibition/index.html — страницу услуги «Exhibition Build»
(застройка выставочных стендов). Светлая страница в стиле остальных услуг сайта:
огромный H1 слева, справа — «чертёж» стенда (арка на изометрической сетке с выносками,
анимация посборочного монтажа), процесс 5 шагов, компактные кейсы в масштабе родного стора,
фиолетовая форма + тёмный футер из react-chrome.py.
build_v1 её пропускает по маркеру <!--custom-page-->. Деплой CI не трогает (нет index-a2.html)."""
import os, importlib.util, html as H

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,'..','..','mirror'))

# подключаем chrome (header/footer/CSS/JS/FONT) из react-chrome.py
spec=importlib.util.spec_from_file_location("rc", os.path.join(HERE,"react-chrome.py"))
rc=importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

CASES=[
 ("/portfolio/samara-stand-vdnh","Стенд Самарской области","Выставка-форум «Россия», ВДНХ","/images/lib/custom-samara-vdnh/cover-main.png"),
 ("/portfolio/stavropol-stand-vdnh","Стенд Ставропольского края","Выставка-форум «Россия», ВДНХ","/images/lib/custom-stavropol-vdnh/cover-main.png"),
 ("/portfolio/samara-exhibition","Выставка «Самара»","Музей им. Алабина","/images/lib/custom-samara-exhibition/cover-main.png"),
 ("/eaton_online","Виртуальный стенд Eaton","Онлайн-трансляция выставки","/images/lib/as6438-6362-4632-b262-313335333833/image_2021-03-06_22-.png"),
]
STEPS=[
 ("Дизайн и 3D-визуализация","Концепция, зонирование и фотореалистичная визуализация будущего стенда"),
 ("Конструктив и инженерия","Проектирование каркаса, расчёт нагрузок, свет и инженерные системы"),
 ("Производство","Собственная и партнёрская база — печать, дерево, металл, пластик, акрил"),
 ("Мультимедиа и интерактив","LED-экраны, проекции, сенсорные панели, AR/VR и 3D-маппинг"),
 ("Логистика и монтаж","Доставка, монтаж и демонтаж на площадке в любом городе России"),
]

METRIKA='<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

PAGE_CSS="""<style id="ex-css">
/* точная Tilda-шапка приходит из общего хрома (react-chrome.py, TILDA_HDR_CSS) */
.ex-main{font-family:'Montserrat',-apple-system,Arial,sans-serif;color:#14171C}
.ex-main a:focus-visible,.ex-main button:focus-visible{outline:3px solid #673A7E;outline-offset:3px;border-radius:4px}
/* ------- герой: чертёж стенда ------- */
.ex-hero{position:relative;background:#fff;overflow:hidden}
.ex-hero__in{position:relative;max-width:1180px;margin:0 auto;padding:64px 40px 72px;display:grid;grid-template-columns:1.05fr .95fr;gap:32px;align-items:center}
.ex-hero__blueprint{position:absolute;inset:0;left:42%;
 background:
  repeating-linear-gradient(60deg,rgba(20,23,28,.05) 0 1px,transparent 1px 34px),
  repeating-linear-gradient(-60deg,rgba(20,23,28,.05) 0 1px,transparent 1px 34px),
  repeating-linear-gradient(0deg,rgba(20,23,28,.035) 0 1px,transparent 1px 34px);
 -webkit-mask-image:radial-gradient(75% 85% at 60% 50%,#000 55%,transparent 100%);
 mask-image:radial-gradient(75% 85% at 60% 50%,#000 55%,transparent 100%)}
.ex-eyebrow{margin:0 0 18px;font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#673A7E}
.ex-hero__t{margin:0;font-size:clamp(44px,6.6vw,88px);line-height:.98;font-weight:800;letter-spacing:-.025em}
.ex-hero__sub{margin:20px 0 0;font-size:clamp(18px,2vw,24px);font-weight:700}
.ex-hero__lead{margin:18px 0 0;max-width:520px;font-size:17px;line-height:1.65;color:#5A616A}
.ex-hero__act{margin-top:34px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.ex-cta{display:inline-block;background:#FCB724;color:#14171C;font-weight:800;font-size:16px;text-decoration:none;padding:16px 42px;border-radius:30px;transition:transform .15s,box-shadow .15s}
.ex-cta:hover{transform:translateY(-2px);box-shadow:0 14px 26px -14px rgba(252,183,36,.9)}
.ex-cta_ghost{background:transparent;box-shadow:inset 0 0 0 2px rgba(20,23,28,.16);font-weight:700}
.ex-cta_ghost:hover{box-shadow:inset 0 0 0 2px #673A7E}
/* чертёж (SVG): сборка арки + выноски */
.ex-draft{position:relative;width:100%;max-width:560px;margin:0 auto;display:block}
.ex-part{opacity:0;transform:translateY(14px);animation:exUp .55s cubic-bezier(.2,.7,.2,1) forwards}
.ex-part_1{animation-delay:.15s}.ex-part_2{animation-delay:.3s}.ex-part_3{animation-delay:.45s}.ex-part_4{animation-delay:.62s}.ex-part_5{animation-delay:.8s}
@keyframes exUp{to{opacity:1;transform:none}}
.ex-note{font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;fill:#673A7E;opacity:0;animation:exIn .5s ease forwards 1s}
@keyframes exIn{to{opacity:1}}
.ex-dim{stroke:#673A7E;stroke-width:1;opacity:0;animation:exIn .5s ease forwards 1s}
@media (prefers-reduced-motion:reduce){
 .ex-part,.ex-note,.ex-dim{animation:none;opacity:1;transform:none}
 .ex-rev{transition:none!important;opacity:1!important;transform:none!important}}
/* ------- секции ------- */
.ex-sec{max-width:1180px;margin:0 auto;padding:76px 40px}
.ex-sec__head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;margin-bottom:40px}
.ex-sec__h{font-size:clamp(26px,3vw,38px);font-weight:800;letter-spacing:-.02em;margin:0}
.ex-all{font-weight:700;font-size:15px;color:#673A7E;text-decoration:none;white-space:nowrap}
.ex-all:hover{text-decoration:underline}
/* появление при скролле — как плитки услуг */
.ex-rev{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1)}
.ex-rev.is-in{opacity:1;transform:none}
/* процесс: монтажная направляющая */
.ex-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:26px;position:relative;counter-reset:exstep}
.ex-steps::before{content:"";position:absolute;left:24px;right:24px;top:23px;height:2px;background:linear-gradient(90deg,#673A7E 0%,rgba(103,58,126,.15) 100%)}
.ex-step{position:relative;counter-increment:exstep}
.ex-step__n{position:relative;z-index:1;display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:50%;background:#673A7E;color:#fff;font-weight:800;font-size:15px;margin-bottom:18px;box-shadow:0 0 0 6px #fff}
.ex-step__n::before{content:"0" counter(exstep)}
.ex-step h3{margin:0 0 8px;font-size:17px;font-weight:700;line-height:1.3}
.ex-step p{margin:0;font-size:14px;line-height:1.55;color:#5A616A}
.ex-steps__note{margin:44px 0 0;text-align:center;font-size:16px;color:#5A616A}
.ex-steps__note b{color:#14171C}
/* кейсы: масштаб родного стора (~295px), фото без апскейла */
.ex-cases-wrap{background:#F5F5F7}
.ex-cases{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.ex-card{display:block;text-decoration:none;color:inherit;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 8px 22px -16px rgba(0,0,0,.25);transition:transform .2s,box-shadow .2s}
.ex-card:hover{transform:translateY(-4px);box-shadow:0 22px 38px -22px rgba(0,0,0,.32)}
.ex-card__img{position:relative;aspect-ratio:477/396;overflow:hidden;background:#e9ebee}
.ex-card__img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .35s}
.ex-card:hover .ex-card__img img{transform:scale(1.05)}
.ex-card__cat{position:absolute;left:12px;top:12px;background:#673A7E;color:#fff;font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:11px;letter-spacing:.06em;padding:5px 10px;border-radius:999px}
.ex-card__b{padding:16px 18px 20px}
.ex-card__t{font-size:16px;font-weight:800;letter-spacing:-.01em;margin:0 0 5px;line-height:1.3}
.ex-card__d{font-size:13.5px;color:#5A616A;margin:0}
/* ------- адаптив ------- */
@media(max-width:1020px){
 .ex-hero__in{grid-template-columns:1fr;padding:48px 24px 56px}
 .ex-hero__blueprint{left:0;top:46%}
 .ex-draft{max-width:440px;margin-top:10px}
 .ex-steps{grid-template-columns:1fr 1fr;gap:30px 26px}
 .ex-steps::before{display:none}
 .ex-cases{grid-template-columns:1fr 1fr}
 .ex-sec{padding:56px 24px}}
@media(max-width:560px){
 .ex-hero__in{padding:36px 16px 44px}
 .ex-hero__lead{font-size:15.5px}
 .ex-cta{padding:14px 32px;font-size:15px}
 .ex-sec{padding:44px 16px}
 .ex-sec__head{margin-bottom:24px}
 .ex-steps{grid-template-columns:1fr;gap:22px}
 .ex-step__n{margin-bottom:10px}
 .ex-steps__note{margin-top:28px;text-align:left}
 /* кейсы — горизонтальный свайп, как родная мобильная карусель */
 .ex-cases{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:8px;margin:0 -16px;padding-left:16px;padding-right:16px;-webkit-overflow-scrolling:touch}
 .ex-card{flex:0 0 78%;scroll-snap-align:start}}
</style>"""

# арка exhibition-build крупно на изометрической сетке + размерная линия снизу.
# Геометрия арки — из mirror/images/services/exhibition-build.svg (viewBox 110 40 204 220).
DRAFT_SVG="""<svg class="ex-draft" viewBox="0 0 560 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Выставочный стенд-арка: от идеи до монтажа — под ключ">
<defs>
 <linearGradient id="exf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E5FB0"/><stop offset="1" stop-color="#5A3473"/></linearGradient>
 <linearGradient id="ext" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#BD96D8"/><stop offset="1" stop-color="#9A6CBE"/></linearGradient>
 <linearGradient id="exs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A3473"/><stop offset="1" stop-color="#3E2553"/></linearGradient>
</defs>
<g transform="translate(126,26) scale(1.55)">
 <g class="ex-part ex-part_1"><polygon points="270,70 270,250 304,230 304,50" fill="url(#exs)" transform="translate(-110,-40)"/></g>
 <g class="ex-part ex-part_2"><polygon points="230,110 230,250 264,230 264,90" fill="#4A2A5E" transform="translate(-110,-40)"/><polygon points="160,110 230,110 264,90 194,90" fill="#7B4E9E" transform="translate(-110,-40)"/></g>
 <g class="ex-part ex-part_3"><path d="M120,250 L120,70 L270,70 L270,250 L230,250 L230,110 L160,110 L160,250 Z" fill="url(#exf)" transform="translate(-110,-40)"/></g>
 <g class="ex-part ex-part_4"><polygon points="120,70 270,70 304,50 154,50" fill="url(#ext)" transform="translate(-110,-40)"/></g>
 <g class="ex-part ex-part_5"><polygon points="176,96 214,96 214,82 176,82" fill="#FFE000" transform="translate(-110,-40)"/><polygon points="214,96 214,82 226,75 226,89" fill="#E6C800" transform="translate(-110,-40)"/></g>
</g>
<!-- размерная линия -->
<g class="ex-dim"><line x1="142" y1="372" x2="374" y2="372"/><line x1="142" y1="364" x2="142" y2="380"/><line x1="374" y1="364" x2="374" y2="380"/></g>
<text class="ex-note" x="120" y="398">От идеи до монтажа — под ключ</text>
</svg>"""

# ============================================================================
# РАЗБОР ПРОЕКТА: стенд Самарской области, форум «Россия — спортивная держава».
# Тёмный иммерсивный full-bleed модуль: рендеры проекта — главный визуал.
# Сигнатура — «конструкторская рама»: маркеры SMR·NN с световой линией (мотив
# металлоферм стенда с рендеров), HUD-строка паспорта, кинолента кадров,
# интерактивы — технологической ведомостью. Две равноправные концепции —
# диптих арт-панелей с видео. Плеер/лайтбокс — vp-modal (ниже).
# Ассеты: mirror/images/exhibition/samara/*.jpg, постеры /images/vp/*, /media/samara-pres-*.
# ============================================================================

CONCEPTS = [
    dict(tag='Концепция А', name='Пять хранителей', video='/media/samara-pres-5spirits.mp4',
         poster='/images/vp/5-stihy_samara.jpg',
         essence='Легенда о пяти духах Самарской земли: Волга, Жигули, промышленность, космос и инновации ведут гостя по стенду.',
         chips=[('#8B5CF6', '«Прогресс» · космос'), ('#3BC9D8', '«Лука» · Волга'), ('#98A2B3', '«Лада» · индустрия'),
                ('#7BC144', '«Леший» · природа'), ('#E44FA0', '«Ягоза» · инновации')]),
    dict(tag='Концепция Б', name='Четыре стихии', video='/media/samara-pres-4elements.mp4',
         poster='/images/vp/4-stihii_samara.jpg',
         essence='Земля, вода, огонь и воздух — четыре силы региона, каждая со своим цветом, звуком и зоной стенда.',
         chips=[('#7BC144', 'Земля · Жигули'), ('#3BC9D8', 'Вода · Волга'), ('#F0603A', 'Огонь · индустрия'),
                ('#C9D4E0', 'Воздух · космос')]),
]

# Две отдельные ленты — по варианту дизайна (одной длинной листать слишком долго)
FRAMES_V1 = [
    ('video', '/media/samara-pres-vizual-1.mp4', '/images/vp/vizual_1_samara.jpg', 'Видеооблёт варианта'),
    ('img', 'render-v1-a', '', '«Неоновая арена»: общий вид'),
    ('img', 'render-v1-b', '', 'Зона «Самарской регаты»'),
    ('img', 'render-v1-c', '', 'Интерьер с медиапотолком'),
    ('img', 'plan-v1', '', 'План застройки'),
]
FRAMES_V2 = [
    ('video', '/media/samara-pres-vizual-2.mp4', '/images/vp/vizual_2_samara.jpg', 'Видеооблёт варианта'),
    ('img', 'render-v2-a', '', '«Хранители»: общий вид'),
    ('img', 'render-v2-b', '', 'Медиаколонны с хранителями'),
    ('img', 'render-v2-c', '', 'Фасад с LED-принтами'),
    ('img', 'plan-v2', '', 'План застройки'),
]

SPEC = [
    ('И-01', 'Кинетическое шоу из хоккейных шайб', 'Шайбы на индивидуальных лебёдках выстраиваются в объёмные фигуры над сценой — визуальный якорь стенда и всех фото с форума.'),
    ('И-02', '«Сдай ГТО с чемпионом»', 'Компьютерное зрение считает повторения и следит за техникой; амбассадор на экране тренирует, диплом печатается на стенде.'),
    ('И-03', 'Полоса препятствий «Путь Героя»', 'Замкнутое пространство 360°: панорамные проекции реагируют на движение участника.'),
    ('И-04', '«Самарская регата»', 'Гость раскрашивает корпус судна, сканер оцифровывает рисунок — и корабль уходит в плавание по медиаакватории стенда.'),
    ('И-05', 'AR-фото с амбассадором', 'Цифровая копия легендарного спортсмена встаёт рядом с гостем; снимок с готовыми хэштегами уходит на почту.'),
    ('И-06', '«Аллея Чемпионов»', 'Девять аттракционов, где физика управляет графикой: виртуальная рыбалка, прыжковый тест, пиксель-арт на велотренажёрах, симулятор старта LADA.'),
    ('И-07', 'Тач-панели «Цифровая Самара»', 'Шесть вертикальных панелей — мультимедийный портал о спорте, инфраструктуре и проектах региона.'),
    ('И-08', 'Бар амбассадоров', 'Авторские безалкогольные коктейли в честь чемпионов: «Апперкот Саитова», «Сальто Немова», «Синхрон Киселёвой».'),
]

def _mark(code, title):
    return f'<div class="sam-mark ex-rev"><span class="sam-mark__c">{code}</span><h3 class="sam-mark__t">{title}</h3><i></i></div>'

def _concepts():
    h = '<div class="sam-duo">'
    for c in CONCEPTS:
        chips = ''.join(f'<span class="sam-chip"><i style="background:{col}"></i>{txt}</span>' for col, txt in c['chips'])
        h += (f'<div class="sam-con ex-rev">'
              f'<button type="button" class="vp-facade sam-con__art" data-video="{c["video"]}" data-title="{c["name"]} — видеопрезентация концепции" '
              f'aria-label="Смотреть видеопрезентацию: {c["name"]}">'
              f'<img src="{c["poster"]}" alt="{c["name"]} — креативная концепция выставочного стенда Самарской области" loading="lazy" width="960" height="540">'
              f'<span class="sam-con__shade" aria-hidden="true"></span>'
              f'<span class="sam-con__kick">{c["tag"]}</span>'
              f'<span class="sam-con__name">{c["name"]}</span>'
              f'<span class="vp-facade__play sam-con__play" aria-hidden="true"></span></button>'
              f'<p class="sam-con__d">{c["essence"]}</p>'
              f'<div class="sam-chips">{chips}</div></div>')
    return h + '</div>'

def _strip(frames, variant):
    h = (f'<div class="sam-strip ex-rev" tabindex="0" '
         f'aria-label="Галерея рендеров: {variant}, прокручивается горизонтально">')
    n = len(frames)
    for i, (kind, src, poster, cap) in enumerate(frames, 1):
        idx = f'{i:02d}/{n:02d}'
        full = f'{variant} · {cap}'
        if kind == 'video':
            h += (f'<figure class="sam-frame"><button type="button" class="vp-facade" data-video="{src}" data-title="{full}" '
                  f'aria-label="Смотреть видео: {full}">'
                  f'<img src="{poster}" alt="{full} — дизайн-проект стенда Самарской области" loading="lazy" width="800" height="450">'
                  f'<span class="vp-facade__play" aria-hidden="true"></span></button>'
                  f'<figcaption class="sam-frame__cap"><span>{cap}</span><span class="sam-frame__idx">{idx}</span></figcaption></figure>')
        else:
            p = f'/images/exhibition/samara/{src}.jpg'
            h += (f'<figure class="sam-frame"><button type="button" class="sam-zoom" data-img="{p}" data-title="{full}" '
                  f'aria-label="Открыть кадр: {full}">'
                  f'<img src="{p}" alt="{full} — дизайн-проект выставочного стенда" loading="lazy" width="800" height="450"></button>'
                  f'<figcaption class="sam-frame__cap"><span>{cap}</span><span class="sam-frame__idx">{idx}</span></figcaption></figure>')
    return h + '</div>'

def _variant_head(kick, name, note):
    return (f'<div class="sam-vhead ex-rev"><span class="sam-vhead__k">{kick}</span>'
            f'<h4 class="sam-vhead__n">{name}</h4><p class="sam-vhead__d">{note}</p></div>')

def _spec():
    rows = ''.join(f'<div class="sam-row ex-rev"><span class="sam-row__i">{i}</span>'
                   f'<span class="sam-row__n">{n}</span><span class="sam-row__d">{d}</span></div>'
                   for i, n, d in SPEC)
    return f'<div class="sam-spec">{rows}</div>'

def case_narr():
    hud = ('<div class="sam-hud ex-rev">'
           '<div><b>204&nbsp;м²</b><span>площадь</span></div>'
           '<div><b>2</b><span>концепции</span></div>'
           '<div><b>2</b><span>варианта дизайна</span></div>'
           '<div><b>12+</b><span>интерактивов</span></div>'
           '<div><b>5</b><span>видеопрезентаций</span></div>'
           '<div><b>79</b><span>листов проекта</span></div></div>')

    brief = ('<p class="sam-brief ex-rev">Сделать стенд региона <em>хедлайнером</em> международного спортивного форума '
             'на «Солидарность Самара Арене» — с WOW-эффектом для VIP-гостей и живыми очередями посетителей.</p>'
             '<div class="sam-goals ex-rev">'
             '<div>Показать спортивный, промышленный и космический потенциал области</div>'
             '<div>Вовлечь гостей интерактивом, а не плакатами</div>'
             '<div>Дать делегациям деловую зону для переговоров и подписаний</div>'
             '<div>Создать поводы для фото, публикаций и СМИ</div></div>')

    zoning = ('<div class="sam-zon"><ul class="sam-zlist ex-rev">'
              '<li><b>Деловая зона</b><span>сцена с LED-экраном для церемоний федерального уровня, VIP-переговорная на 8 персон</span></li>'
              '<li><b>Шоу-зона</b><span>кинетическая инсталляция и центральный арт-экран</span></li>'
              '<li><b>Интерактивная зона</b><span>«Аллея Чемпионов», ГТО, полоса препятствий 360°, медиаакватория регаты</span></li>'
              '<li><b>Гостевая зона</b><span>спорт-бар с продукцией самарских производителей и лаунж</span></li></ul>'
              '<figure class="sam-plan ex-rev"><button type="button" class="sam-zoom" data-img="/images/exhibition/samara/plan-v1.jpg" '
              'data-title="План застройки стенда, 204 м²" aria-label="Открыть план застройки">'
              '<img src="/images/exhibition/samara/plan-v1.jpg" alt="План застройки выставочного стенда 204 м² — зонирование" loading="lazy" width="800" height="450">'
              '</button><figcaption class="sam-frame__cap"><span>План застройки · маршруты четырёх аудиторий</span></figcaption></figure></div>')

    content = ('<div class="sam-cnt"><figure class="sam-cnt__v ex-rev">'
               '<button type="button" class="vp-facade" data-video="/media/samara-pres-content.mp4" data-title="Концепция контента стенда" '
               'aria-label="Смотреть видео: концепция контента стенда">'
               '<img src="/images/vp/content_samara.jpg" alt="Концепция мультимедийного контента выставочного стенда" loading="lazy" width="800" height="450">'
               '<span class="vp-facade__play" aria-hidden="true"></span></button></figure>'
               '<div class="sam-cnt__t ex-rev"><p>Стенд без контента — это мебель. Вместе с проектом заказчик получил сценарии каждого экрана: '
               'ролики с AI-образами великих самарских спортсменов, инфографику «Самара в цифрах», спортивный квиз для тач-панелей '
               'и правила адаптации графики под все поверхности — от медиапотолка до пола.</p>'
               '<p class="sam-dim">Как мы делаем такой контент — на страницах <a href="/content/">Content</a> и <a href="/videoproduction/">Video Production</a>.</p></div></div>')

    outro = ('<div class="sam-outro ex-rev">'
             '<h3>Такой дизайн-проект — первый этап любого нашего стенда</h3>'
             '<p>Концепции на выбор, зонирование, интерактив, рендеры и видеооблёты, планы застройки и контент-пакет — '
             'всё это вы оцениваете <b>до начала производства</b>. Дальше строим: собственное производство, мультимедиа и монтаж в любом городе России.</p>'
             '<a class="ex-cta" href="#ex-quiz">Рассчитать свой стенд</a></div>')

    return (f'<div class="sam-dark" id="ex-case"><div class="sam-in">'
            f'<p class="sam-over ex-rev">Разбор проекта</p>'
            f'<h2 class="sam-h ex-rev">Стенд Самарской области:<br>от легенды до рабочих чертежей</h2>'
            f'<p class="sam-intro ex-rev">Показываем подход Hand Marketing к застройке выставочных стендов на реальном дизайн-проекте — '
            f'стенде региона для международного форума «Россия — спортивная держава».</p>'
            f'{hud}'
            f'{_mark("SMR·01", "Задача")}{brief}'
            f'{_mark("SMR·02", "Две концепции на выбор заказчика")}'
            f'<p class="sam-lead ex-rev">Хороший стенд рассказывает историю. Мы разработали две равноправные креативные концепции — '
            f'каждая с собственной легендой, визуальным кодом и полной видеопрезентацией. Нажмите — видео откроется со звуком:</p>'
            f'{_concepts()}'
            f'{_mark("SMR·03", "Зонирование · 204 м²")}{zoning}'
            f'{_mark("SMR·04", "Ведомость интерактивов")}'
            f'<p class="sam-lead ex-rev">Мультимедиа проектируется вместе со стендом, а не «прикручивается» потом. '
            f'Интерактивные инсталляции этого проекта:</p>{_spec()}'
            f'{_mark("SMR·05", "Дизайн · два варианта")}'
            f'<p class="sam-lead ex-rev">Заказчик получил две полностью проработанные архитектуры стенда — у каждой свой видеооблёт, '
            f'рендеры и план застройки. Ленты листаются, кадры открываются в полный размер:</p>'
            f'{_variant_head("Вариант 1", "«Неоновая арена»", "Белый корпус, циановая светографика, медиапотолок-«Волга»")}'
            f'</div>{_strip(FRAMES_V1, "Вариант 1")}<div class="sam-in sam-in_seq">'
            f'{_variant_head("Вариант 2", "«Хранители»", "Тёмный корпус и гигантские арт-принты легенды на медиаколоннах")}'
            f'</div>{_strip(FRAMES_V2, "Вариант 2")}<div class="sam-in">'
            f'{_mark("SMR·06", "Контент для всех экранов")}{content}'
            f'{outro}'
            f'</div></div>')

FAQ = [
    ('Что входит в дизайн-проект выставочного стенда?',
     'Креативная концепция (обычно две на выбор), зонирование под задачи и потоки посетителей, дизайн с 3D-визуализацией и видеооблётами, планы застройки, проект мультимедийного наполнения и интерактивов, концепция контента для всех экранов.'),
    ('Сколько времени занимает разработка концепции стенда?',
     'Зависит от площади и состава работ: первые эскизы и зонирование — обычно за одну-две недели, полный дизайн-проект с рендерами и видео — от двух недель. Точный график зафиксируем после брифа.'),
    ('Вы делаете только дизайн или строите стенд под ключ?',
     'Полный цикл: концепция, дизайн-проект, производство конструкций, мультимедийное наполнение (экраны, интерактив, контент), монтаж и сопровождение на площадке — в любом городе России.'),
    ('Можно ли заказать только мультимедиа и контент для готового стенда?',
     'Да. Интерактивные инсталляции, видеомаппинг, контент для LED-экранов и тач-панелей мы делаем и как отдельную услугу — в том числе для стендов, которые строит другой подрядчик.'),
    ('Сколько стоит выставочный стенд под ключ?',
     'Бюджет зависит от площади, конструктива и объёма мультимедиа. Ответьте на четыре вопроса в калькуляторе ниже — подготовим расчёт под вашу выставку и перезвоним с вариантами.'),
]

def faq_html():
    import json
    items, ld = '', []
    for q, a in FAQ:
        items += f'<details class="sam-faq__item ex-rev"><summary>{q}</summary><p>{a}</p></details>'
        ld.append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    schema = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': ld}, ensure_ascii=False)
    return (f'<section class="ex-sec" id="ex-faq"><div class="ex-sec__head"><h2 class="ex-sec__h ex-rev">Вопросы о застройке стендов</h2></div>'
            f'<div class="sam-faq">{items}</div>'
            f'<script type="application/ld+json">{schema}</script></section>')

CASE_CSS = """<style id="sam-css">
.sam-dark{--cy:#3BC9D8;--ink:#0D1117;--panel:#141A21;--tx:#E9EDF1;--dim:#98A2B3;--hair:rgba(233,237,241,.1);
 margin:76px calc(50% - 50vw) 0;background:
 radial-gradient(1200px 500px at 80% -5%,rgba(59,201,216,.08),transparent 60%),
 radial-gradient(900px 420px at 8% 30%,rgba(139,92,246,.05),transparent 55%),var(--ink);
 color:var(--tx);overflow:hidden}
.sam-in{max-width:1180px;margin:0 auto;padding:72px 40px 8px}
.sam-in+.sam-in,.sam-in_seq{padding-top:0}
/* шапки лент вариантов */
.sam-vhead{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;margin:18px 0 14px}
.sam-vhead__k{font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:11px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--ink);background:var(--cy);padding:5px 10px;border-radius:4px;white-space:nowrap}
.sam-vhead__n{margin:0;font-size:clamp(18px,2.1vw,23px);font-weight:800;letter-spacing:-.015em;color:#fff}
.sam-vhead__d{margin:0;font-size:13.5px;color:var(--dim);flex-basis:100%;max-width:60ch}
@media(min-width:881px){.sam-vhead__d{flex-basis:auto}}
.sam-over{margin:0 0 14px;font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--cy)}
.sam-h{margin:0 0 16px;font-size:clamp(28px,3.8vw,46px);font-weight:800;line-height:1.04;letter-spacing:-.02em;color:#fff}
.sam-intro{max-width:62ch;margin:0 0 34px;font-size:17px;line-height:1.65;color:var(--dim)}
/* HUD-строка паспорта */
.sam-hud{display:flex;flex-wrap:wrap;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);margin-bottom:26px}
.sam-hud div{flex:1 1 auto;padding:16px 26px 16px 0;display:flex;align-items:baseline;gap:10px;white-space:nowrap}
.sam-hud b{font-size:clamp(20px,2.2vw,28px);font-weight:800;letter-spacing:-.02em;color:var(--cy);font-variant-numeric:tabular-nums}
.sam-hud span{font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
/* маркеры-«фермы» */
.sam-mark{display:flex;align-items:center;gap:16px;margin:54px 0 18px}
.sam-mark__c{font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:11px;letter-spacing:.2em;color:var(--cy);
 border:1px solid rgba(59,201,216,.45);padding:5px 10px;border-radius:4px;white-space:nowrap}
.sam-mark__t{margin:0;font-size:clamp(19px,2.4vw,26px);font-weight:800;letter-spacing:-.015em;color:#fff}
.sam-mark i{flex:1;height:1px;background:linear-gradient(90deg,rgba(59,201,216,.45),transparent)}
.sam-lead{max-width:66ch;margin:0 0 22px;font-size:15.5px;line-height:1.6;color:var(--dim)}
/* задача */
.sam-brief{max-width:30ch;margin:6px 0 26px;font-size:clamp(21px,2.6vw,30px);font-weight:700;line-height:1.3;color:#fff}
.sam-brief em{font-style:normal;color:var(--cy)}
.sam-goals{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-bottom:8px}
.sam-goals div{border-left:2px solid var(--cy);padding-left:14px;font-size:14px;line-height:1.55;color:#C6CDD6}
/* диптих концепций */
.sam-duo{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:8px}
.sam-con__art{position:relative;display:block;width:100%;border:0;padding:0;cursor:pointer;border-radius:16px;overflow:hidden;background:#000}
.sam-con__art>img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;transition:transform .35s ease}
.sam-con__art:hover>img{transform:scale(1.045)}
.sam-con__shade{position:absolute;inset:0;background:linear-gradient(190deg,rgba(13,17,23,.05) 40%,rgba(13,17,23,.88) 92%)}
.sam-con__art::after{content:"";position:absolute;inset:0;border-radius:16px;border:1px solid rgba(59,201,216,0);transition:border-color .25s}
.sam-con__art:hover::after{border-color:rgba(59,201,216,.6)}
.sam-con__kick{position:absolute;left:20px;bottom:58px;font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--cy)}
.sam-con__name{position:absolute;left:20px;bottom:20px;right:96px;font-size:clamp(21px,2.4vw,29px);font-weight:800;letter-spacing:-.02em;color:#fff;text-align:left}
.sam-con__play{left:auto;top:auto;right:22px;bottom:22px;transform:none;width:54px;height:54px}
.sam-con__art:hover .sam-con__play{transform:scale(1.1)}
.sam-con__d{margin:14px 2px 10px;font-size:14.5px;line-height:1.6;color:var(--dim)}
.sam-chips{display:flex;flex-wrap:wrap;gap:8px}
.sam-chip{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--hair);border-radius:999px;padding:5px 12px;
 font-size:12.5px;font-weight:600;color:#C6CDD6;white-space:nowrap}
.sam-chip i{width:8px;height:8px;border-radius:50%;flex:none}
/* зонирование */
.sam-zon{display:grid;grid-template-columns:1fr 1.15fr;gap:28px;align-items:start;margin-bottom:8px}
.sam-zlist{list-style:none;margin:0;padding:0}
.sam-zlist li{padding:14px 0;border-bottom:1px solid var(--hair)}
.sam-zlist li:first-child{border-top:1px solid var(--hair)}
.sam-zlist b{display:block;font-size:15.5px;color:#fff;margin-bottom:3px}
.sam-zlist span{font-size:13.5px;line-height:1.5;color:var(--dim)}
.sam-plan{margin:0}
/* ведомость */
.sam-spec{border-top:1px solid var(--hair);margin-bottom:8px}
.sam-row{display:grid;grid-template-columns:64px minmax(220px,290px) 1fr;gap:18px;padding:15px 6px;border-bottom:1px solid var(--hair);transition:background .15s}
.sam-row:hover{background:rgba(59,201,216,.05)}
.sam-row__i{font-weight:800;font-size:13px;color:var(--cy);font-variant-numeric:tabular-nums;letter-spacing:.06em}
.sam-row__n{font-weight:700;font-size:14.5px;color:#fff;line-height:1.4}
.sam-row__d{font-size:13.5px;line-height:1.55;color:var(--dim)}
/* кинолента */
.sam-strip{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x proximity;padding:6px max(40px,calc(50vw - 590px)) 22px;
 scrollbar-width:thin;scrollbar-color:rgba(59,201,216,.5) transparent;-webkit-overflow-scrolling:touch}
.sam-strip::-webkit-scrollbar{height:6px}
.sam-strip::-webkit-scrollbar-thumb{background:rgba(59,201,216,.45);border-radius:3px}
.sam-strip:focus-visible{outline:2px solid var(--cy);outline-offset:4px}
.sam-frame{flex:0 0 min(720px,84vw);margin:0;scroll-snap-align:center}
.sam-frame .vp-facade,.sam-frame .sam-zoom{border-radius:14px}
.sam-frame__cap{display:flex;justify-content:space-between;gap:14px;margin-top:9px;
 font-family:'Raleway',Arial,sans-serif;font-weight:700;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim)}
.sam-frame__idx{color:var(--cy);font-variant-numeric:tabular-nums}
/* контент */
.sam-cnt{display:grid;grid-template-columns:1.05fr 1fr;gap:28px;align-items:center;margin-bottom:8px}
.sam-cnt__v{margin:0}
.sam-cnt__t p{margin:0 0 14px;font-size:15.5px;line-height:1.65;color:#C6CDD6}
.sam-dim{color:var(--dim)!important;font-size:14px!important}
.sam-dim a{color:var(--cy);font-weight:600}
/* зум и фасады внутри тёмного */
.sam-zoom{display:block;width:100%;border:0;padding:0;cursor:zoom-in;border-radius:14px;overflow:hidden;background:#000}
.sam-zoom img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;transition:transform .3s}
.sam-zoom:hover img{transform:scale(1.04)}
.vp-facade{position:relative;display:block;width:100%;border:0;padding:0;cursor:pointer;border-radius:14px;overflow:hidden;background:#000}
.vp-facade img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;transition:transform .3s,opacity .2s}
.vp-facade:hover img{transform:scale(1.04);opacity:.9}
.vp-facade__play{position:absolute;left:50%;top:50%;width:62px;height:62px;transform:translate(-50%,-50%);border-radius:50%;
 background:#FFE000;box-shadow:0 12px 30px -10px rgba(0,0,0,.65);transition:transform .2s}
.vp-facade__play::before{content:"";position:absolute;left:53%;top:50%;transform:translate(-50%,-50%);
 border-left:17px solid #14171C;border-top:10px solid transparent;border-bottom:10px solid transparent}
.vp-facade:hover .vp-facade__play{transform:translate(-50%,-50%) scale(1.1)}
/* аутро */
.sam-outro{margin:56px 0 72px;padding:clamp(26px,4vw,44px);border:1px solid rgba(59,201,216,.35);border-radius:18px;
 background:linear-gradient(135deg,rgba(59,201,216,.09),transparent 55%)}
.sam-outro h3{margin:0 0 12px;font-size:clamp(20px,2.6vw,28px);font-weight:800;letter-spacing:-.02em;color:#fff}
.sam-outro p{margin:0 0 22px;max-width:72ch;font-size:15.5px;line-height:1.65;color:#C6CDD6}
/* FAQ (светлая зона страницы) */
.sam-faq{display:grid;gap:10px;max-width:820px}
.sam-faq__item{border:1px solid rgba(20,23,28,.1);border-radius:14px;background:#fff;padding:0 20px}
.sam-faq__item summary{cursor:pointer;list-style:none;position:relative;padding:16px 36px 16px 0;font-size:16px;font-weight:700}
.sam-faq__item summary::-webkit-details-marker{display:none}
.sam-faq__item summary::after{content:"";position:absolute;right:2px;top:50%;width:12px;height:12px;transform:translateY(-70%) rotate(45deg);
 border-right:2.5px solid #673A7E;border-bottom:2.5px solid #673A7E;transition:transform .2s}
.sam-faq__item[open] summary::after{transform:translateY(-30%) rotate(225deg)}
.sam-faq__item p{margin:0 0 18px;font-size:15px;line-height:1.65;color:#5A616A}
@media(max-width:1080px){.sam-goals{grid-template-columns:1fr 1fr;gap:16px}
 .sam-zon{grid-template-columns:1fr}.sam-cnt{grid-template-columns:1fr}}
@media(max-width:880px){.sam-duo{grid-template-columns:1fr}
 .sam-row{grid-template-columns:52px 1fr;grid-template-rows:auto auto}.sam-row__d{grid-column:2}}
@media(max-width:640px){.sam-in{padding:52px 18px 8px}
 .sam-hud div{padding:12px 16px 12px 0}.sam-goals{grid-template-columns:1fr}
 .sam-strip{padding-left:18px;padding-right:18px}.sam-frame{flex-basis:88vw}}
@media (prefers-reduced-motion: reduce){.sam-zoom img,.vp-facade img,.vp-facade__play,.sam-con__art>img{transition:none}}
</style>"""

# Модальный плеер (тот же, что на /videoproduction) + просмотр рендеров (data-img)
VP_MODAL = """<style id="vpm-css">
.vp-modal{position:fixed;inset:0;z-index:2000;display:flex;align-items:center;justify-content:center;padding:24px;background:rgba(10,12,16,.9);animation:vpFade .2s ease}
@keyframes vpFade{from{opacity:0}to{opacity:1}}
.vp-modal__box{position:relative;width:min(1100px,96vw)}
.vp-modal video,.vp-modal__img{display:block;width:100%;max-height:82vh;aspect-ratio:16/9;object-fit:contain;background:#000;border-radius:14px;box-shadow:0 40px 90px -30px rgba(0,0,0,.8)}
.vp-modal__cap{margin-top:12px;color:#fff;font-weight:700;font-size:15px;font-family:'Montserrat',Arial,sans-serif}
.vp-modal__close{position:absolute;top:-14px;right:-14px;z-index:1;width:44px;height:44px;border:0;border-radius:50%;background:#FFE000;cursor:pointer;box-shadow:0 10px 24px -8px rgba(0,0,0,.6);transition:transform .15s}
.vp-modal__close:hover{transform:scale(1.08)}
.vp-modal__close::before,.vp-modal__close::after{content:"";position:absolute;left:50%;top:50%;width:20px;height:2.5px;background:#14171C;border-radius:2px}
.vp-modal__close::before{transform:translate(-50%,-50%) rotate(45deg)}
.vp-modal__close::after{transform:translate(-50%,-50%) rotate(-45deg)}
@media (max-width:640px){.vp-modal{padding:12px}.vp-modal__close{top:-10px;right:-4px;width:40px;height:40px}}
</style><script>(function(){
var opener=null;
function closeModal(){
 var m=document.querySelector('.vp-modal');if(!m)return;
 var v=m.querySelector('video');if(v){v.pause();v.removeAttribute('src');v.load();}
 m.remove();document.body.style.overflow='';
 if(opener&&opener.focus)opener.focus();opener=null;
}
function openModal(node,title){
 closeModal();
 var m=document.createElement('div');m.className='vp-modal';
 m.setAttribute('role','dialog');m.setAttribute('aria-modal','true');
 m.setAttribute('aria-label',title||'Просмотр');
 var box=document.createElement('div');box.className='vp-modal__box';
 var x=document.createElement('button');x.type='button';x.className='vp-modal__close';x.setAttribute('aria-label','Закрыть');
 box.appendChild(x);box.appendChild(node);
 if(title){var c=document.createElement('div');c.className='vp-modal__cap';c.textContent=title;box.appendChild(c);}
 m.appendChild(box);document.body.appendChild(m);
 document.body.style.overflow='hidden';x.focus();
}
document.addEventListener('click',function(e){
 var b=e.target.closest&&e.target.closest('.vp-facade');
 if(b){opener=b;var v=document.createElement('video');
  v.controls=true;v.playsInline=true;v.preload='metadata';v.autoplay=true;
  v.setAttribute('playsinline','');v.src=b.getAttribute('data-video');
  openModal(v,b.getAttribute('data-title')||'');v.play().catch(function(){});return;}
 var z=e.target.closest&&e.target.closest('.sam-zoom');
 if(z){opener=z;var im=document.createElement('img');im.className='vp-modal__img';
  im.src=z.getAttribute('data-img');im.alt=z.getAttribute('data-title')||'';
  openModal(im,z.getAttribute('data-title')||'');return;}
 if(e.target.closest&&e.target.closest('.vp-modal__close')){closeModal();return;}
 if(e.target.classList&&e.target.classList.contains('vp-modal'))closeModal();
});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal();});
})();</script>"""

# Квиз-калькулятор стенда: 4 вопроса -> заявка в /api/lead.php (form=exhibition-quiz).
# Цены не показывает (фактуры нет) — обещает расчёт; цели Метрики: quiz_start / quiz_submit.
QUIZ = """<section class="ex-sec" id="ex-quiz"><style>
.ex-quiz{background:#fff;border:2px solid rgba(103,58,126,.18);border-radius:24px;padding:clamp(26px,4vw,48px);max-width:760px;margin:0 auto}
.ex-quiz__t{margin:0;font-size:clamp(24px,3vw,36px);font-weight:800;letter-spacing:-.02em}
.ex-quiz__s{margin:10px 0 26px;color:#5A616A;font-size:16px;line-height:1.55}
.ex-quiz__dots{display:flex;gap:8px;margin-bottom:22px}
.ex-quiz__dot{width:34px;height:6px;border-radius:3px;background:rgba(103,58,126,.15);transition:background .2s}
.ex-quiz__dot.on{background:#673A7E}
.ex-quiz__q{margin:0 0 16px;font-size:19px;font-weight:700}
.ex-quiz__opts{display:grid;gap:10px}
.ex-quiz__opt{display:flex;align-items:center;gap:12px;border:2px solid rgba(20,23,28,.12);border-radius:14px;padding:14px 18px;cursor:pointer;font-size:16px;font-weight:600;transition:border-color .15s,background .15s}
.ex-quiz__opt:hover{border-color:#673A7E}
.ex-quiz__opt input{accent-color:#673A7E;width:18px;height:18px;flex:none}
.ex-quiz__opt.sel{border-color:#673A7E;background:rgba(103,58,126,.06)}
.ex-quiz__nav{display:flex;gap:12px;margin-top:24px;align-items:center}
.ex-quiz__btn{border:0;cursor:pointer;background:#FCB724;color:#14171C;font:800 16px Montserrat,Arial,sans-serif;padding:14px 36px;border-radius:30px;transition:transform .15s}
.ex-quiz__btn:hover{transform:translateY(-2px)}
.ex-quiz__btn[disabled]{opacity:.45;cursor:default;transform:none}
.ex-quiz__back{border:0;background:none;cursor:pointer;color:#673A7E;font:700 15px Montserrat,Arial,sans-serif}
.ex-quiz__fin{display:grid;gap:12px;max-width:420px}
.ex-quiz__fin input{border:2px solid rgba(20,23,28,.15);border-radius:14px;padding:14px 18px;font:500 16px Montserrat,Arial,sans-serif}
.ex-quiz__fin input:focus{outline:none;border-color:#673A7E}
.ex-quiz__ok{font-size:18px;font-weight:700;color:#14171C}
.ex-quiz__err{color:#C0392B;font-size:14px;margin:0}
.ex-quiz__hp{position:absolute!important;left:-9999px;width:1px;height:1px;opacity:0}
.ex-quiz__consent{font-size:12px;color:#8a8f96}.ex-quiz__consent a{color:#673A7E}
</style>
<div class="ex-sec__head"><h2 class="ex-sec__h ex-rev">Рассчитайте стоимость стенда</h2></div>
<div class="ex-quiz ex-rev" data-quiz>
 <p class="ex-quiz__s">Четыре вопроса и минута времени — подготовим расчёт под вашу выставку и перезвоним с вариантами.</p>
 <div class="ex-quiz__dots" aria-hidden="true"></div>
 <form novalidate></form>
</div>
<script>(function(){
var STEPS=[
 {q:'Какая площадь стенда?',name:'Площадь',opts:['до 20 м²','20–50 м²','50–100 м²','больше 100 м²'],type:'radio'},
 {q:'Какой тип стенда нужен?',name:'Тип стенда',opts:['Индивидуальная застройка','Аренда готовых конструкций','Пока не знаю — нужна консультация'],type:'radio'},
 {q:'Нужны мультимедиа и интерактив? Можно несколько.',name:'Мультимедиа',opts:['LED-экраны','Интерактивные столы и панели','Видеомаппинг / проекции','Контент под ключ','Без мультимедиа'],type:'check'},
 {q:'Когда выставка?',name:'Сроки',opts:['В ближайшие 2 месяца','В этом году','Пока планируем бюджет'],type:'radio'}
];
var box=document.querySelector('[data-quiz]');if(!box)return;
var form=box.querySelector('form'),dots=box.querySelector('.ex-quiz__dots');
var step=0,answers={},started=false;
function ym_goal(g){try{if(window.ym)ym(71125393,'reachGoal',g);}catch(e){}}
function drawDots(){dots.innerHTML='';for(var i=0;i<STEPS.length+1;i++){var d=document.createElement('i');d.className='ex-quiz__dot'+(i<=step?' on':'');dots.appendChild(d);}}
function draw(){
 drawDots();
 if(step<STEPS.length){var s=STEPS[step];
  var h='<p class="ex-quiz__q">'+s.q+'</p><div class="ex-quiz__opts">';
  s.opts.forEach(function(o,i){
   var sel=(answers[s.name]||[]).indexOf(o)>-1;
   h+='<label class="ex-quiz__opt'+(sel?' sel':'')+'"><input type="'+(s.type==='check'?'checkbox':'radio')+'" name="q'+step+'" value="'+o+'"'+(sel?' checked':'')+'>'+o+'</label>';});
  h+='</div><div class="ex-quiz__nav">'+(step>0?'<button type="button" class="ex-quiz__back">← Назад</button>':'')+
   '<button type="button" class="ex-quiz__btn" '+((answers[STEPS[step].name]||[]).length?'':'disabled')+'>Дальше</button></div>';
  form.innerHTML=h;
 }else{
  form.innerHTML='<p class="ex-quiz__q">Куда прислать расчёт?</p><div class="ex-quiz__fin">'+
   '<input class="ex-quiz__hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">'+
   '<input type="text" name="name" placeholder="Имя" autocomplete="name">'+
   '<input type="tel" name="phone" placeholder="+7 ___ ___ __ __" autocomplete="tel" required>'+
   '<div class="ex-quiz__nav"><button type="button" class="ex-quiz__back">← Назад</button>'+
   '<button type="submit" class="ex-quiz__btn">Получить расчёт</button></div>'+
   '<p class="ex-quiz__consent">Нажимая кнопку, вы даёте согласие на обработку <a href="/privacy">персональных данных</a></p></div>';
 }
}
box.addEventListener('change',function(e){
 if(!e.target.name||e.target.name.indexOf('q')!==0)return;
 if(!started){started=true;ym_goal('quiz_start');}
 var s=STEPS[step];
 if(s.type==='check'){
  var arr=[].slice.call(form.querySelectorAll('input:checked')).map(function(i){return i.value;});
  answers[s.name]=arr;
 }else{answers[s.name]=[e.target.value];}
 [].slice.call(form.querySelectorAll('.ex-quiz__opt')).forEach(function(l){l.classList.toggle('sel',l.querySelector('input').checked);});
 var btn=form.querySelector('.ex-quiz__btn');if(btn)btn.disabled=!(answers[s.name]||[]).length;
 if(s.type==='radio'){setTimeout(function(){step++;draw();},220);}
});
box.addEventListener('click',function(e){
 if(e.target.classList.contains('ex-quiz__back')){step--;draw();return;}
 if(e.target.classList.contains('ex-quiz__btn')&&e.target.type==='button'&&!e.target.disabled){step++;draw();}
});
form.addEventListener('submit',function(e){
 e.preventDefault();
 var tel=form.querySelector('input[name=phone]');
 if(!tel||tel.value.replace(/\\D/g,'').length<6){if(tel)tel.focus();return;}
 var data={form:'exhibition-quiz',name:(form.querySelector('input[name=name]')||{}).value||'',phone:tel.value,
  website:(form.querySelector('input[name=website]')||{}).value||''};
 Object.keys(answers).forEach(function(k){data[k]=answers[k].join(', ');});
 var btn=form.querySelector('.ex-quiz__btn');btn.disabled=true;btn.textContent='Отправляем…';
 fetch('/api/lead.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
 .then(function(r){return r.json();}).then(function(j){
  if(!j||!j.success)throw 0;
  ym_goal('quiz_submit');
  form.innerHTML='<p class="ex-quiz__ok">Спасибо! Расчёт подготовим и перезвоним в ближайшее время.</p>';
  step=STEPS.length;drawDots();
 }).catch(function(){
  btn.disabled=false;btn.textContent='Получить расчёт';
  var m=form.querySelector('.ex-quiz__err');
  if(!m){m=document.createElement('p');m.className='ex-quiz__err';form.appendChild(m);}
  m.textContent='Не удалось отправить. Позвоните нам: +7 495 580 75 37';
 });
});
draw();
})();</script></section>"""

REVEAL_JS="""<noscript><style>.ex-rev{opacity:1!important;transform:none!important}</style></noscript>
<script>(function(){
var els=[].slice.call(document.querySelectorAll('.ex-rev'));
function showAll(){els.forEach(function(n){n.classList.add('is-in');});}
if(!('IntersectionObserver' in window)){showAll();return;}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
els.forEach(function(n,i){n.style.transitionDelay=Math.min(i%4*90,270)+'ms';io.observe(n);});
/* страховка: через 12 с показать всё, что ещё не раскрылось (раньше тут был unobserve —
   элементы навсегда оставались невидимыми у посетителей, задержавшихся на первом экране) */
setTimeout(function(){els.forEach(function(n){if(!n.classList.contains('is-in')){n.classList.add('is-in');io.unobserve(n);}});},12000);
})();</script>"""

HEAD=f'''<!doctype html><html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Застройка выставочных стендов под ключ в Москве и по всей России | Hand Marketing</title>
<meta name="description" content="Застройка выставочных стендов под ключ: дизайн и 3D-визуализация, изготовление, мультимедийные и интерактивные стенды, монтаж в любом городе России. Кейсы: ВДНХ, Самара, Ставрополь.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hand-marketing.ru/exhibition/">
<meta property="og:type" content="website"><meta property="og:title" content="Застройка выставочных стендов под ключ в Москве и по всей России | Hand Marketing">
<meta property="og:description" content="Выставочные стенды под ключ: дизайн, изготовление, интерактив и мультимедиа, монтаж по всей России.">
<meta property="og:url" content="https://hand-marketing.ru/exhibition">
<meta property="og:image" content="https://hand-marketing.ru/images/lib/custom-samara-vdnh/cover-main.png">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
{rc.FONT}{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''

def steps():
    return ''.join(f'<div class="ex-step ex-rev"><span class="ex-step__n" aria-hidden="true"></span><h3>{H.escape(t)}</h3><p>{H.escape(d)}</p></div>' for t,d in STEPS)

def cases():
    out=''
    for url,t,d,img in CASES:
        out+=(f'<a class="ex-card ex-rev" href="{url}"><div class="ex-card__img">'
              f'<img src="{img}" alt="{H.escape(t)}" loading="lazy">'
              f'<span class="ex-card__cat">Exhibition Build</span></div>'
              f'<div class="ex-card__b"><div class="ex-card__t">{H.escape(t)}</div>'
              f'<div class="ex-card__d">{H.escape(d)}</div></div></a>')
    return out

def build():
    hero=(f'<section class="ex-hero"><div class="ex-hero__blueprint" aria-hidden="true"></div><div class="ex-hero__in">'
          f'<div><p class="ex-eyebrow">Услуга</p>'
          # SEO: русский запрос — в <h1>, английское слово — крупный видимый акцент (вид не меняется)
          f'<div class="ex-hero__t">Exhibition<br>Build</div>'
          f'<h1 class="ex-hero__sub">Застройка выставочных стендов под&nbsp;ключ</h1>'
          f'<p class="ex-hero__lead">Проектируем и строим выставочные стенды любого масштаба — от дизайна выставочного стенда и 3D-визуализации до производства, мультимедийного наполнения и монтажа на площадке в любом городе России.</p>'
          f'<div class="ex-hero__act"><a class="ex-cta" href="#lead">Обсудить проект</a>'
          f'<a class="ex-cta ex-cta_ghost" href="#ex-cases">Смотреть кейсы</a></div></div>'
          f'<div>{DRAFT_SVG}</div>'
          f'</div></section>')
    steps_sec=(f'<section class="ex-sec"><div class="ex-sec__head"><h2 class="ex-sec__h ex-rev">Как мы строим стенд</h2></div>'
          f'<div class="ex-steps">{steps()}</div>'
          f'<p class="ex-steps__note ex-rev">Один подрядчик на весь цикл: <b>сдаём готовый стенд точно в срок</b> — включая экспозиции в виртуальном формате.</p></section>')
    case_sec=(f'<div class="ex-cases-wrap" id="ex-cases"><section class="ex-sec">'
          f'<div class="ex-sec__head"><h2 class="ex-sec__h ex-rev">Кейсы</h2><a class="ex-all ex-rev" href="/project">Все проекты →</a></div>'
          f'<div class="ex-cases">{cases()}</div></section></div>')
    body=(f'{rc.header()}<main class="ex-main">{hero}{steps_sec}{CASE_CSS}{case_narr()}{case_sec}{QUIZ}{faq_html()}</main>'
          f'<a id="lead"></a>{rc.footer()}{rc.JS}{VP_MODAL}{REVEAL_JS}</body></html>')
    return HEAD+body

if __name__=='__main__':
    out=os.path.join(ROOT,'exhibition'); os.makedirs(out,exist_ok=True)
    open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(build())
    print("создано: mirror/exhibition/index.html")
