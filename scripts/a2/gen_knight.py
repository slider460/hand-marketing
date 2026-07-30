#!/usr/bin/env python3
"""Генерит mirror/creative/becar/knight-house/index.html — кейс «Брошюра „Дом
с рыцарем“» для Becar Asset Management: издание на 18 полос про шесть апартаментов
в доходном доме начала XX века на Садовой-Самотечной, 2/12.

Дизайн-концепция: «линия вместо декора». В брошюре готика показана не орнаментом,
а тонкой медной линией: она строит шевроны, аркады и пересечения на чёрном листе,
а фотография врезана в шеврон. Веб-аналог: Cormorant Garamond (дисплей) + Onest
(текст) из /fonts/cormorant-onest.css, линейная графика на SVG, чёрный лист и медь.

Живые блоки:
  • семь рыцарей Москвы — схема на SVG: линии от радиально стоящих домов сходятся
    на Манежной площади, как написано на второй полосе брошюры;
  • выбор апартамента — шесть лотов с метражом из брошюры, состав помещений
    показан пропорциональной полосой, план этажа переключается вместе с лотом;
  • листалка из 18 полос со скролл-снапом и лайтбоксом.

Ассеты: mirror/images/knight/ (scripts/knight-assets.py).
Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import os
import importlib.util
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/knight'
URL = 'https://hand-marketing.ru/creative/becar/knight-house/'

# ─── 18 полос: (номер, глава, заголовок, описание, alt) ──────────────────────
PAGES = [
 (1, 'Обложка', 'Дом с рыцарем, дом с историей',
  'Чёрный лист, четыре медные линии и разреженный капс. Ни фотографии, ни плана: '
  'на обложке только имя дома и адрес сайта, потому что дальше вся брошюра '
  'построена на этой же линии.',
  'Обложка брошюры «Дом с рыцарем»: чёрный лист с медными линиями и разреженным капсом'),
 (2, 'История', 'Семь рыцарей Москвы',
  'Полоса-легенда: семь рыцарей появились на фасадах московских домов в одно время '
  'и получили направления по сторонам света. Линии от этих домов пересекаются '
  'на Манежной площади, там же нашли образ Георгия Победоносца. Герб на фоне выбит '
  'в чёрном почти без контраста, поэтому текст читается первым.',
  'Полоса брошюры: легенда о семи рыцарях Москвы, герб выбит в чёрном фоне'),
 (3, 'Дом', 'Северный модерн с элементами готики',
  'Первая фотография в издании: фасад доходного дома начала XX века по проекту '
  'архитектора Василия Волокитина. Текст слева перечисляет то, что видно справа: '
  'массивные формы, лепные барельефы с дамами и воинами, крылатые львы у парадных '
  'и рыцарь в латах на уровне седьмого этажа.',
  'Полоса брошюры: фасад дома в стиле северный модерн с готическим декором'),
 (4, 'Дом', 'Барельефы, маскароны, метлахская плитка',
  'Разбор декора: горельефы с профилями рыцарей, розетки, мечи и щиты, стрельчатые '
  'окна, балюстрады и аркады. Фотография парадного врезана в шеврон, а медная линия '
  'подхватывает форму арки. Так готика попадает на полосу без единого орнамента.',
  'Полоса брошюры: фотография парадного входа врезана в шеврон из медных линий'),
 (5, 'Район', 'Расположение',
  'Карта Тверского района с домом в центре: театры, посольства и министерства, парки, '
  'транспорт. Карта нарисована в цветах издания, поэтому она читается как часть '
  'брошюры, а не как скриншот. Дом отмечен ромбом, Садовое кольцо ведёт взгляд.',
  'Полоса брошюры: карта Тверского района с домом на Садовой-Самотечной'),
 (6, 'Район', 'Новое жильё здесь редкость',
  'Короткая полоса-аргумент про Тверской район: старейший район Москвы, где каждый '
  'новый жилой комплекс привлекает и инвесторов, и покупателей, потому что подобных '
  'предложений почти нет.',
  'Полоса брошюры: аргумент про редкость нового жилья в Тверском районе'),
 (7, 'Район', 'Пять причин выбрать район',
  'Развитая инфраструктура, выгодное расположение, статусность соседства '
  'с министерствами и посольствами, историческая застройка, близость к культурной '
  'жизни. Каждый пункт стоит отдельным блоком на линии, без списка с маркерами.',
  'Полоса брошюры: пять причин выбрать Тверской район, блоки на медных линиях'),
 (8, 'Апартаменты', 'Толстые стены и тишина',
  'Полоса-переход к апартаментам. Один аргумент, который важнее планировок: '
  'в доме очень толстые стены, они дают шумоизоляцию и защищают от суеты Садового '
  'кольца.',
  'Полоса брошюры: раздел «Апартаменты», аргумент про толстые стены и тишину'),
 (9, 'Апартаменты', 'Что получает покупатель',
  'Слева фотография спальни с высокими потолками, справа пять пунктов на чёрном: '
  'высокие потолки и большие окна, свет и пространство, парадные, огороженный двор '
  'и всего три квартиры на этаже. Последний пункт выделен медью, потому что он '
  'и есть главный.',
  'Полоса брошюры: интерьер спальни и пять преимуществ апартаментов'),
 (10, 'Апартаменты', 'Планировки',
  'Вводная полоса к планам: мастер-спальни, просторные кухни-гостиные и обещание, '
  'что среди шести лотов найдётся своё.',
  'Полоса брошюры: вступление к планировкам апартаментов'),
 (11, 'Планировки', 'Два этажа целиком',
  'Планы второго и третьего этажей на одной полосе. Апартаменты подкрашены разными '
  'тонами, метраж подписан внутри помещений, номер лота стоит крупно. По этой полосе '
  'менеджер показывает, что на этаже действительно три квартиры.',
  'Полоса брошюры: планы второго и третьего этажей с апартаментами А1, А2, А3, В1, В2, В3'),
 (12, 'Планировки', 'Апартаменты А1 и В1',
  'Текст про кухню-гостиную 32,4 кв.м: готовить и присматривать за ребёнком '
  'одновременно, ужинать всем вместе, устраивать посиделки за большим столом. '
  'Сравнение с обычной планировкой той же площади сделано в пользу евроформата.',
  'Полоса брошюры: описание апартаментов А1 и В1 с кухней-гостиной 32,4 кв.м'),
 (13, 'Планировки', 'План А1 и В1',
  'Два плана рядом: 56 кв.м на втором этаже и 56,7 кв.м на третьем, где к тем же '
  'помещениям добавляется балкон 4,6 кв.м. Разница между лотами видна за секунду, '
  'потому что планы стоят в одном масштабе.',
  'Полоса брошюры: планы апартаментов А1 на 56 кв.м и В1 на 56,7 кв.м'),
 (14, 'Планировки', 'Апартаменты А2 и В2',
  'Полоса про спальню с двумя окнами и балкон, на котором помещается зона отдыха. '
  'Аргумент строится не на метраже, а на том, что происходит в комнате.',
  'Полоса брошюры: описание апартаментов А2 и В2 со спальней и балконом'),
 (15, 'Планировки', 'План А2 и В2',
  'Самые компактные лоты издания: 35,9 и 37,2 кв.м. Кухня-гостиная, спальная зона, '
  'холл и санузел, ничего лишнего в подписях.',
  'Полоса брошюры: планы апартаментов А2 на 35,9 кв.м и В2 на 37,2 кв.м'),
 (16, 'Планировки', 'Апартаменты А3 и В3',
  'Лоты с отдельным входом: четыре окна, потолок 3,2 метра, мастер-спальня, в которой '
  'помещается гардеробная, и санузел, куда встаёт ванна. Тут же довод про вид из окна '
  'и настроение, единственная эмоциональная строка на всю полосу.',
  'Полоса брошюры: описание апартаментов А3 и В3 с отдельным входом и мастер-спальней'),
 (17, 'Планировки', 'План А3 и В3',
  'Финальная пара планов: 40,5 и 41,6 кв.м. Дальше в брошюре только адрес, поэтому '
  'разговор о метрах заканчивается на самом просторном лоте после первого.',
  'Полоса брошюры: планы апартаментов А3 на 40,5 кв.м и В3 на 41,6 кв.м'),
 (18, 'Контакты', 'Адрес и телефон',
  'Задник собран как обложка: чёрный лист, медная линия, три строки контактов. '
  'Сайт, телефон и адрес, ничего больше.',
  'Задник брошюры: сайт knight-house.ru, телефон и адрес на Садовой-Самотечной'),
]

# ─── Шесть лотов: (код, этаж, площадь, помещения, текст) ─────────────────────
FLATS = [
 ('a1', 'А1', 2, '56', [('Кухня-гостиная', 32.4), ('Спальная зона', 11.8),
                        ('Холл', 7.6), ('С/У', 4.2)],
  'Самый большой лот на этаже. Кухня-гостиная 32,4 кв.м работает как вторая комната: '
  'в брошюре это объясняется не метражом, а сценариями, от уроков за большим столом '
  'до перекуса не отрываясь от работы.'),
 ('a2', 'А2', 2, '35,9', [('Кухня-гостиная', 18.1), ('Спальная зона', 9.1),
                          ('Холл', 4.5), ('С/У', 4.2)],
  'Компактный лот с той же логикой: кухня-гостиная как общая комната и отдельная '
  'спальная зона с двумя окнами.'),
 ('a3', 'А3', 2, '40,5', [('Кухня-гостиная', 18.8), ('Спальная зона', 15.3),
                          ('Холл', 3.3), ('С/У', 4.2)],
  'Лот с индивидуальным входом, четырьмя окнами и потолком 3,2 метра. Мастер-спальня '
  'позволяет выделить гардеробную, а в санузел встаёт ванна.'),
 ('b1', 'В1', 3, '56,7', [('Кухня-гостиная', 32.4), ('Спальная зона', 12.5),
                          ('Холл', 7.6), ('С/У', 4.2), ('Балкон', 4.6)],
  'Тот же план, что у А1, но этажом выше и с балконом 4,6 кв.м, на котором '
  'помещается зона отдыха с видом во двор.'),
 ('b2', 'В2', 3, '37,2', [('Кухня-гостиная', 19.0), ('Спальная зона', 9.5),
                          ('Холл', 4.5), ('С/У', 4.2)],
  'Компактный лот третьего этажа. От А2 отличается на 1,3 квадратных метра, '
  'которые ушли в кухню-гостиную и спальню.'),
 ('b3', 'В3', 3, '41,6', [('Кухня-гостиная', 18.8), ('Спальная зона', 15.3),
                          ('Холл', 3.3), ('С/У', 4.2)],
  'Самый просторный лот с отдельным входом. Мастер-спальня 15,3 кв.м с двумя окнами '
  'выходит в тихий двор.'),
]

# ─── Семь рыцарей: (код, угол в градусах от севера, подпись, пояснение) ──────
KNIGHTS = [
 ('n', 0, 'Север', 'Самый молодой рыцарь, у него даже нет щита'),
 ('e', 90, 'Восток', 'Старый бородатый рыцарь: направление требует мудрых решений'),
 ('s', 180, 'Юг', 'Второй бородатый рыцарь, тоже старый и взвешенный'),
 ('w1', 245, 'Запад', 'Западную сторону охраняют четыре рыцаря'),
 ('w2', 265, 'Запад', 'Западную сторону охраняют четыре рыцаря'),
 ('w3', 285, 'Запад', 'Западную сторону охраняют четыре рыцаря'),
 ('w4', 305, 'Запад', 'Западную сторону охраняют четыре рыцаря'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 5l-7 7 7 7"/></svg>')
GRIP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M9 6l-5 6 5 6M15 6l5 6-5 6"/></svg>')

PAGE_CSS = """<style id="kn-css">
:root{
 --kn-ink:#141310;--kn-ink2:#1e1c18;--kn-cop:#b3763c;--kn-gold:#c9a25e;
 --kn-paper:#f4f1ea;--kn-gray:#7a746a;
 --kn-df:'Cormorant Garamond',Georgia,'Times New Roman',serif;
 --kn-tf:'Onest',system-ui,-apple-system,Arial,sans-serif;
}
.kn{font-family:var(--kn-tf);font-size:17px;line-height:1.65;color:var(--kn-ink);
 background:var(--kn-paper);-webkit-font-smoothing:antialiased}
.kn *{box-sizing:border-box}
.kn h1,.kn h2,.kn h3{font-family:var(--kn-df);font-weight:600;line-height:1.06;
 letter-spacing:-.005em;margin:0;text-wrap:balance}
.kn p{margin:14px 0 0}
.kn a{color:inherit}
.kn-w{width:min(1240px,100% - 40px);margin-inline:auto}
.kn-kick{font-family:var(--kn-tf);font-weight:600;font-size:11.5px;letter-spacing:.26em;
 text-transform:uppercase;display:block;color:var(--kn-cop)}
.kn-r{opacity:0;transform:translateY(20px);transition:opacity .8s cubic-bezier(.2,.7,.3,1),
 transform .8s cubic-bezier(.2,.7,.3,1)}
.kn-r.is-in{opacity:1;transform:none}
.kn-dark{background:var(--kn-ink);color:var(--kn-paper)}
.kn-dark .kn-kick{color:var(--kn-gold)}

/* ── ГЕРОЙ ── */
.kn-hero{position:relative;background:var(--kn-ink);color:var(--kn-paper);overflow:hidden;
 padding:clamp(44px,6vw,74px) 0 0}
.kn-hero__lines{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;
 opacity:.62}
.kn-hero__in{position:relative;z-index:2}
.kn-hero__top{display:flex;justify-content:space-between;align-items:baseline;gap:18px;
 flex-wrap:wrap;padding-bottom:clamp(26px,4vw,48px);
 border-bottom:1px solid rgba(179,118,60,.42)}
.kn-mark{font-family:var(--kn-df);font-weight:600;font-size:19px;letter-spacing:.22em;
 text-transform:uppercase}
.kn-hero__by{font-size:13px;color:rgba(244,241,234,.6);letter-spacing:.04em}
.kn-hero__grid{display:grid;grid-template-columns:1.04fr .96fr;
 gap:clamp(26px,4.4vw,62px);align-items:center;padding:clamp(32px,5vw,64px) 0 0}
.kn-hero h1{font-size:clamp(36px,5.6vw,74px);margin-top:18px;font-weight:500}
.kn-hero h1 em{font-style:italic;color:var(--kn-gold)}
.kn-hero__sub{font-size:clamp(15.5px,1.35vw,18px);color:rgba(244,241,234,.76);max-width:50ch}
.kn-chips{display:flex;flex-wrap:wrap;gap:0;margin:26px 0 0;padding:0;list-style:none}
.kn-chips li{font-size:12px;letter-spacing:.1em;text-transform:uppercase;
 padding:8px 16px 8px 0;margin-right:16px;color:rgba(244,241,234,.72);
 border-right:1px solid rgba(179,118,60,.4)}
.kn-chips li:last-child{border-right:0}
.kn-hero__cta{display:flex;flex-wrap:wrap;gap:14px;margin-top:clamp(24px,3vw,36px)}
.kn-btn{display:inline-flex;align-items:center;gap:10px;font-family:var(--kn-tf);
 font-weight:600;font-size:13px;letter-spacing:.1em;text-transform:uppercase;
 padding:15px 26px;text-decoration:none;border:1px solid var(--kn-cop);cursor:pointer;
 transition:background .25s,color .25s}
.kn-btn svg{width:17px;height:17px}
.kn .kn-btn--f{background:var(--kn-cop);color:#14130f}
.kn .kn-btn--g{background:transparent;color:var(--kn-gold)}
.kn .kn-btn--f:hover{background:var(--kn-gold)}
.kn .kn-btn--g:hover{background:rgba(179,118,60,.16)}
.kn-hero__art{position:relative}
.kn-hero__art img{display:block;width:100%;height:auto;
 box-shadow:0 40px 90px -50px rgba(0,0,0,.9);border:1px solid rgba(179,118,60,.3)}
.kn-spec{position:relative;z-index:2;margin-top:clamp(32px,5vw,62px);
 border-top:1px solid rgba(179,118,60,.42)}
.kn-spec__in{display:grid;grid-template-columns:repeat(4,1fr);margin:0;
 width:min(1240px,100% - 40px);margin-inline:auto}
.kn-spec__in>div{padding:22px 22px 26px 0}
.kn-spec dt{font-family:var(--kn-df);font-weight:600;font-size:clamp(20px,2.2vw,28px);
 color:var(--kn-gold);font-variant-numeric:lining-nums}
.kn-spec dd{margin:6px 0 0;font-size:13.5px;color:rgba(244,241,234,.62);max-width:24ch}

/* ── ДОМ ── */
.kn-about{padding:clamp(56px,8vw,104px) 0}
.kn-about h2{font-size:clamp(30px,4vw,52px);margin-top:16px;max-width:20ch;font-weight:500}
.kn-about__grid{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(28px,5vw,64px);
 align-items:center}
.kn-about p{font-size:clamp(16px,1.3vw,18px);color:#3a362f;max-width:56ch}
.kn-about__ph img{display:block;width:100%;height:auto;
 clip-path:polygon(0 0,100% 0,100% 88%,50% 100%,0 88%)}
.kn-facts{margin-top:clamp(32px,4.4vw,52px);display:grid;grid-template-columns:repeat(4,1fr);
 border-top:1px solid rgba(20,19,16,.16)}
.kn-facts>div{padding:22px 20px 0 0;border-right:1px solid rgba(20,19,16,.12)}
.kn-facts>div:last-child{border-right:0}
.kn-facts b{display:block;font-family:var(--kn-df);font-weight:600;
 font-size:clamp(26px,3vw,40px);color:var(--kn-cop);line-height:1;
 font-variant-numeric:lining-nums}
.kn-facts span{display:block;margin-top:8px;font-size:13.5px;color:var(--kn-gray);
 line-height:1.4}

/* ── ЗАДАЧА ── */
.kn-task{padding:clamp(56px,8vw,104px) 0}
.kn-task__grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(26px,5vw,62px)}
.kn-task h2{font-size:clamp(28px,3.8vw,48px);margin-top:16px;font-weight:500}
.kn-task ul{margin:0;padding:0;list-style:none}
.kn-task li{padding:20px 0;border-top:1px solid rgba(244,241,234,.14);display:grid;
 grid-template-columns:44px 1fr;gap:14px;align-items:start}
.kn-task li:last-child{border-bottom:1px solid rgba(244,241,234,.14)}
.kn-task li i{font-style:normal;font-family:var(--kn-df);font-size:22px;
 color:var(--kn-gold);line-height:1}
.kn-task li p{margin:0;font-size:16.5px;color:rgba(244,241,234,.78);max-width:60ch}

/* ── СЕМЬ РЫЦАРЕЙ ── */
.kn-kn{padding:clamp(56px,8vw,104px) 0}
.kn-kn h2{font-size:clamp(28px,3.8vw,48px);margin-top:16px;font-weight:500;max-width:22ch}
.kn-kn__lede{font-size:clamp(16px,1.3vw,18px);color:rgba(244,241,234,.74);max-width:62ch}
.kn-kn__grid{margin-top:clamp(30px,4vw,50px);display:grid;grid-template-columns:1.05fr .95fr;
 gap:clamp(26px,4.4vw,58px);align-items:center}
.kn-map{width:100%;height:auto;overflow:visible}
.kn-map .ring{fill:none;stroke:rgba(179,118,60,.34);stroke-width:1}
.kn-map .ray{fill:none;stroke:var(--kn-cop);stroke-width:1;opacity:.5;
 stroke-dasharray:var(--len);stroke-dashoffset:var(--len);
 transition:opacity .3s,stroke-width .3s}
.kn-map.is-in .ray{animation:kn-draw 1.5s cubic-bezier(.3,.7,.2,1) forwards}
@keyframes kn-draw{to{stroke-dashoffset:0}}
.kn-map .kt{cursor:pointer}
.kn-map .kt circle{fill:var(--kn-ink);stroke:var(--kn-cop);stroke-width:1;
 transition:fill .25s,r .25s}
.kn-map .kt path{fill:var(--kn-gold);transition:fill .25s}
.kn-map .kt:hover circle,.kn-map .kt.is-on circle{fill:var(--kn-cop)}
.kn-map .kt:hover path,.kn-map .kt.is-on path{fill:#14130f}
.kn-map .ray.is-on{opacity:1;stroke-width:1.8}
.kn-map .hub circle{fill:none;stroke:var(--kn-gold);stroke-width:1}
.kn-map .lbl{font-family:var(--kn-tf);font-size:11px;letter-spacing:.14em;
 text-transform:uppercase;fill:rgba(244,241,234,.56)}
.kn-kn__say{min-height:6.5em;padding:24px 0 0;border-top:1px solid rgba(179,118,60,.36)}
.kn-kn__say b{display:block;font-family:var(--kn-df);font-size:clamp(22px,2.4vw,30px);
 color:var(--kn-gold);font-weight:600}
.kn-kn__say span{display:block;margin-top:10px;font-size:16px;
 color:rgba(244,241,234,.76);max-width:46ch}
.kn-kn__note{margin-top:22px;font-size:13.5px;color:rgba(244,241,234,.5);max-width:52ch}

/* ── ЛОТЫ ── */
.kn-flats{padding:clamp(56px,8vw,104px) 0;background:#fff}
.kn-flats h2{font-size:clamp(28px,3.8vw,48px);margin-top:16px;font-weight:500;max-width:22ch}
.kn-flats__lede{font-size:clamp(16px,1.3vw,18px);color:#3a362f;max-width:64ch}
.kn-tabs{margin-top:clamp(28px,3.6vw,44px);display:flex;gap:0;flex-wrap:wrap;
 border-top:1px solid rgba(20,19,16,.14);border-bottom:1px solid rgba(20,19,16,.14)}
.kn-tab{flex:1 1 0;min-width:96px;padding:18px 12px;background:none;border:0;
 border-right:1px solid rgba(20,19,16,.1);cursor:pointer;text-align:left;
 font-family:var(--kn-tf);transition:background .25s}
.kn-tab:last-child{border-right:0}
.kn-tab b{display:block;font-family:var(--kn-df);font-size:26px;font-weight:600;
 color:var(--kn-ink);font-variant-numeric:lining-nums}
.kn-tab i{font-style:normal;display:block;margin-top:4px;font-size:12px;
 letter-spacing:.08em;text-transform:uppercase;color:var(--kn-gray)}
.kn-tab:hover{background:rgba(179,118,60,.08)}
.kn-tab.is-on{background:var(--kn-ink)}
.kn-tab.is-on b{color:var(--kn-gold)}
.kn-tab.is-on i{color:rgba(244,241,234,.6)}
.kn-flat{display:none;margin-top:clamp(26px,3.4vw,42px);
 grid-template-columns:1fr 1.15fr;gap:clamp(24px,4.4vw,56px);align-items:start}
.kn-flat.is-on{display:grid;animation:kn-fade .5s cubic-bezier(.2,.7,.3,1) both}
@keyframes kn-fade{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.kn-flat__area{font-family:var(--kn-df);font-weight:600;font-size:clamp(48px,7vw,96px);
 line-height:.9;color:var(--kn-ink);font-variant-numeric:lining-nums tabular-nums}
.kn-flat__area sup{font-family:var(--kn-tf);font-size:15px;font-weight:600;
 letter-spacing:.06em;color:var(--kn-cop);vertical-align:super;margin-left:8px}
.kn-flat__floor{margin-top:10px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;
 color:var(--kn-gray)}
.kn-flat p{font-size:16.5px;color:#3a362f;max-width:48ch}
.kn-bar{margin-top:26px;display:flex;height:14px;overflow:hidden}
.kn-bar i{display:block;height:100%}
.kn-bar i:nth-child(1){background:var(--kn-cop)}
.kn-bar i:nth-child(2){background:#8d6a4e}
.kn-bar i:nth-child(3){background:#5d564c}
.kn-bar i:nth-child(4){background:#3a362f}
.kn-bar i:nth-child(5){background:var(--kn-gold)}
.kn-rooms{margin:16px 0 0;padding:0;list-style:none;display:grid;
 grid-template-columns:1fr 1fr;gap:8px 22px}
.kn-rooms li{display:flex;justify-content:space-between;gap:12px;font-size:14.5px;
 padding:7px 0;border-bottom:1px solid rgba(20,19,16,.1);color:var(--kn-gray)}
.kn-rooms li b{font-family:var(--kn-df);font-size:18px;color:var(--kn-ink);font-weight:600;
 font-variant-numeric:lining-nums tabular-nums}
.kn-flat__ph{border:1px solid rgba(20,19,16,.14);background:var(--kn-ink)}
.kn-flat__ph img{display:block;width:100%;height:auto}
.kn-flat__ph figcaption{padding:12px 14px;font-size:13px;color:rgba(244,241,234,.6)}
.kn-flats__note{margin-top:26px;font-size:13.5px;color:var(--kn-gray);max-width:62ch}

/* ── РАЙОН ── */
.kn-dist{padding:clamp(56px,8vw,104px) 0}
.kn-dist__grid{display:grid;grid-template-columns:.92fr 1.08fr;gap:clamp(26px,4.4vw,58px);
 align-items:center}
.kn-dist h2{font-size:clamp(28px,3.8vw,48px);margin-top:16px;font-weight:500}
.kn-dist dl{margin:clamp(24px,3vw,36px) 0 0}
.kn-dist dt{font-family:var(--kn-df);font-size:21px;color:var(--kn-gold);
 padding-top:18px;border-top:1px solid rgba(179,118,60,.3)}
.kn-dist dd{margin:8px 0 18px;font-size:15.5px;color:rgba(244,241,234,.74);max-width:52ch}
.kn-dist__ph img{display:block;width:100%;height:auto;border:1px solid rgba(179,118,60,.3)}

/* ── ЛИСТАЛКА ── */
.kn-book{padding:clamp(56px,8vw,104px) 0;background:#fff;overflow:hidden}
.kn-book__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:22px;
 flex-wrap:wrap;padding-bottom:clamp(24px,3.2vw,40px)}
.kn-book__hd h2{font-size:clamp(28px,3.8vw,50px);margin-top:14px;font-weight:500}
.kn-book__hint{font-size:14.5px;color:var(--kn-gray);max-width:34ch}
.kn-track{display:flex;gap:clamp(14px,2vw,26px);overflow-x:auto;scroll-snap-type:x mandatory;
 scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.kn-track::-webkit-scrollbar{display:none}
.kn-slide{flex:0 0 100%;scroll-snap-align:center;margin:0}
.kn-slide__ph{position:relative;background:var(--kn-ink);cursor:zoom-in;overflow:hidden;
 border:1px solid rgba(20,19,16,.14)}
/* height:auto обязателен: атрибут height у <img> перебивает aspect-ratio,
   и полоса показывалась бы обрезанной по центру */
.kn-slide__ph img{width:100%;height:auto;aspect-ratio:1700/1030;object-fit:cover;display:block}
.kn-slide__pg{position:absolute;left:0;bottom:0;z-index:2;background:var(--kn-cop);
 color:#14130f;font-family:var(--kn-tf);font-weight:700;font-size:11px;
 letter-spacing:.14em;text-transform:uppercase;padding:8px 14px}
.kn-slide__ch{position:absolute;right:0;bottom:0;z-index:2;background:rgba(20,19,16,.82);
 color:var(--kn-gold);font-size:11px;font-weight:600;letter-spacing:.12em;
 text-transform:uppercase;padding:8px 14px}
.kn-slide__zoom{position:absolute;right:0;top:0;z-index:2;background:rgba(20,19,16,.82);
 color:var(--kn-paper);font-size:11.5px;font-weight:600;padding:8px 14px;
 opacity:0;transition:opacity .25s}
.kn-slide__ph:hover .kn-slide__zoom{opacity:1}
.kn-slide figcaption{padding:24px 2px 0;display:grid;grid-template-columns:.56fr 1.44fr;
 gap:clamp(14px,3vw,40px);align-items:start;min-height:140px}
.kn-slide figcaption h3{font-size:clamp(21px,2.2vw,28px);font-weight:500}
.kn-slide figcaption p{margin:0;font-size:15.5px;color:var(--kn-gray);max-width:64ch}
.kn-nav{margin-top:clamp(18px,2.4vw,28px);display:flex;align-items:center;
 justify-content:space-between;gap:18px;flex-wrap:wrap}
.kn-nav__btns{display:flex;align-items:center;gap:10px}
.kn-arrow{width:44px;height:44px;display:grid;place-items:center;background:transparent;
 border:1px solid rgba(20,19,16,.22);color:var(--kn-ink);cursor:pointer;
 transition:background .2s,border-color .2s,color .2s,opacity .2s}
.kn-arrow svg{width:19px;height:19px}
.kn-arrow--next svg{transform:rotate(180deg)}
.kn-arrow:hover{background:var(--kn-cop);border-color:var(--kn-cop);color:#14130f}
.kn-arrow[disabled]{opacity:.3;cursor:default}
.kn-arrow[disabled]:hover{background:transparent;border-color:rgba(20,19,16,.22);
 color:var(--kn-ink)}
.kn-count{font-family:var(--kn-df);font-size:19px;color:var(--kn-gray);min-width:5em;
 font-variant-numeric:lining-nums tabular-nums}
.kn-count b{color:var(--kn-cop);font-weight:600}
.kn-thumbs{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.kn-thumbs::-webkit-scrollbar{display:none}
.kn-thumb{flex:0 0 auto;width:72px;padding:0;border:0;background:none;cursor:pointer;
 opacity:.38;transition:opacity .22s,outline-color .22s;outline:1px solid transparent;
 outline-offset:2px}
.kn-thumb img{width:100%;height:auto;aspect-ratio:1700/1030;object-fit:cover;display:block}
.kn-thumb:hover{opacity:.7}
.kn-thumb.is-on{opacity:1;outline-color:var(--kn-cop)}

/* ── ЛИНИЯ ВМЕСТО ДЕКОРА ── */
.kn-craft{padding:clamp(56px,8vw,104px) 0}
.kn-craft__grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,62px);
 align-items:center}
.kn-craft h2{font-size:clamp(28px,3.8vw,48px);margin-top:16px;font-weight:500}
.kn-craft p{font-size:clamp(16px,1.3vw,18px);color:rgba(244,241,234,.76);max-width:56ch}
.kn-pal{margin-top:28px;display:grid;grid-template-columns:repeat(4,1fr);gap:1px}
.kn-sw{padding:40px 10px 12px;border:1px solid rgba(244,241,234,.14)}
.kn-sw span{display:block;font-size:12.5px;letter-spacing:.08em}
.kn-sw small{font-size:11px;opacity:.7;font-variant-numeric:tabular-nums}
.kn-sw--i{background:#141310;color:var(--kn-paper)}
.kn-sw--c{background:#b3763c;color:#14130f}
.kn-sw--g{background:#c9a25e;color:#14130f}
.kn-sw--p{background:#f4f1ea;color:#14130f}
.kn-craft__ph img{display:block;width:100%;height:auto;
 border:1px solid rgba(179,118,60,.3)}
.kn-craft__ph figcaption{margin-top:14px;font-size:14px;color:rgba(244,241,234,.6)}

/* ── РЕЗУЛЬТАТ ── */
.kn-res{padding:clamp(56px,8vw,104px) 0;background:#fff}
.kn-res__grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(26px,5vw,62px)}
.kn-res h2{font-size:clamp(28px,3.8vw,48px);margin-top:16px;font-weight:500}
.kn-res__more{font-size:15px;color:var(--kn-gray);margin-top:22px}
.kn-res__more a{color:var(--kn-cop);font-weight:600}
.kn-res__list{margin:0;padding:0;list-style:none}
.kn-res__list li{display:grid;grid-template-columns:78px 1fr;gap:18px;align-items:start;
 padding:22px 0;border-top:1px solid rgba(20,19,16,.14)}
.kn-res__list li:last-child{border-bottom:1px solid rgba(20,19,16,.14)}
.kn-res__list span:first-child{font-family:var(--kn-df);font-weight:600;
 font-size:clamp(34px,3.8vw,48px);line-height:.9;color:var(--kn-cop);
 font-variant-numeric:lining-nums}
.kn-res__list span:last-child{font-size:16.5px;color:#3a362f}

/* ── ЛАЙТБОКС ── */
.kn-lb{position:fixed;inset:0;z-index:9999;background:rgba(10,9,7,.96);display:none;
 padding:clamp(16px,4vw,48px);overflow:auto}
.kn-lb.is-open{display:grid;place-items:center}
.kn-lb__box{position:relative;max-width:1500px;width:100%}
.kn-lb__box img{width:100%;height:auto;display:block}
.kn-lb__x{position:absolute;right:0;top:-42px;width:34px;height:34px;
 border:1px solid rgba(244,241,234,.4);background:none;color:var(--kn-paper);
 font-size:20px;line-height:1;cursor:pointer}
.kn-lb__cap{margin-top:14px;font-size:13.5px;color:rgba(244,241,234,.66);text-align:center}

@media(max-width:1000px){
 .kn-hero__grid,.kn-about__grid,.kn-task__grid,.kn-kn__grid,.kn-dist__grid,
 .kn-craft__grid,.kn-res__grid,.kn-flat.is-on{grid-template-columns:1fr}
 .kn-spec__in,.kn-facts{grid-template-columns:1fr 1fr}
 .kn-facts>div:nth-child(2){border-right:0}
 .kn-slide figcaption{grid-template-columns:1fr;min-height:0}
 .kn-hero__art{max-width:560px}
}
@media(max-width:680px){
 .kn{font-size:16px}
 .kn-pal{grid-template-columns:repeat(2,1fr)}
 .kn-rooms{grid-template-columns:1fr}
 .kn-tab{flex:1 1 33%;min-width:0}
 .kn-thumbs{order:3;width:100%}
 .kn-lb__x{top:-36px}
 .kn-slide__ch{display:none}
 .kn-hero__lines{opacity:.3}
}
@media(prefers-reduced-motion:reduce){
 .kn-r{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .kn *{transition-duration:.01ms!important;animation-duration:.01ms!important;
  scroll-behavior:auto}
 .kn-map .ray{stroke-dashoffset:0!important}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Брошюра «Дом с рыцарем» для Becar: 18 полос про апартаменты в доходном доме | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: печатная брошюра «Дом с рыцарем» для Becar Asset Management. 18 полос, альбом 297×180 мм, чёрный лист и медная линия. Концепция, копирайтинг, вёрстка и препресс: издание продаёт шесть апартаментов в доходном доме начала XX века на Садовой-Самотечной, 2/12.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Брошюра «Дом с рыцарем» для Becar Asset Management | кейс Hand Marketing">
<meta property="og:description" content="18 полос про шесть апартаментов в доходном доме начала XX века: чёрный лист, медная линия, семь рыцарей Москвы и планировки.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/page-01.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/cormorant-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''

# Линии обложки: четыре параллельные диагонали и аркада по низу, как на полосе 1
HERO_LINES = (
  '<svg class="kn-hero__lines" viewBox="0 0 1200 700" preserveAspectRatio="xMidYMid slice" '
  'aria-hidden="true" fill="none" stroke="#b3763c" stroke-width="1">'
  + ''.join(f'<path d="M{330 + i * 22} -40 L{980 + i * 22} 610"/>' for i in range(4))
  + ''.join(f'<path d="M{980 + i * 22} -40 L{330 + i * 22} 610"/>' for i in range(4))
  + '<path d="M0 556 H1200"/>'
  + ''.join(f'<path d="M{x} 556 L{x + 62} 700 M{x + 124} 556 L{x + 62} 700 '
            f'M{x} 556 V700 M{x + 124} 556 V700"/>' for x in range(60, 1200, 186))
  + '</svg>')


def hero():
    return (
      '<header class="kn-hero">' + HERO_LINES +
      '<div class="kn-w kn-hero__in">'
      '<div class="kn-hero__top">'
      '<span class="kn-mark">Дом с рыцарем</span>'
      '<span class="kn-hero__by">Becar Asset Management, Садовая-Самотечная, 2/12</span>'
      '</div>'
      '<div class="kn-hero__grid">'
      '<div>'
      '<span class="kn-kick">Полиграфия и копирайтинг</span>'
      '<h1>Брошюра, которая продаёт <em>дом</em>, а потом метры</h1>'
      '<p class="kn-hero__sub">В Тверском районе шесть апартаментов в доходном доме '
      'начала XX века с рыцарем в латах на фасаде. Мы собрали издание на 18 полос: '
      'сначала оно рассказывает про дом и легенду семи рыцарей Москвы, и только потом '
      'переходит к планировкам.</p>'
      '<ul class="kn-chips"><li>Концепция издания</li><li>Копирайтинг</li>'
      '<li>Вёрстка</li><li>Препресс</li></ul>'
      '<div class="kn-hero__cta">'
      f'<a class="kn-btn kn-btn--f" href="#kn-book">Листать полосы {ARROW}</a>'
      '<a class="kn-btn kn-btn--g" href="#kn-flats">Выбрать апартамент</a>'
      '</div></div>'
      '<div class="kn-hero__art">'
      f'<img src="{IMG}/page-01.jpg" width="1700" height="1030" '
      'alt="Обложка брошюры «Дом с рыцарем»: чёрный лист, медные линии и разреженный капс" '
      'loading="eager" fetchpriority="high"></div>'
      '</div></div>'
      '<div class="kn-spec"><dl class="kn-spec__in">'
      '<div><dt>18 полос</dt><dd>от легенды о рыцарях до планировок и адреса</dd></div>'
      '<div><dt>297×180 мм</dt><dd>альбом, который открывают на столе переговорной</dd></div>'
      '<div><dt>6 лотов</dt><dd>по три апартамента на двух этажах</dd></div>'
      '<div><dt>2 цвета</dt><dd>чёрный лист и медь, фотография как третий</dd></div>'
      '</dl></div></header>')


def about():
    facts = [('7', 'рыцарей на фасадах московских домов'),
             ('3', 'квартиры на этаже, и это главный аргумент'),
             ('3,2 м', 'высота потолка в лотах с отдельным входом'),
             ('8 минут', 'пешком до метро «Цветной бульвар»')]
    cells = ''.join(f'<div><b>{k}</b><span>{H.escape(v)}</span></div>' for k, v in facts)
    return (
      '<section class="kn-about"><div class="kn-w">'
      '<div class="kn-about__grid">'
      '<div class="kn-r"><span class="kn-kick">Объект</span>'
      '<h2>Доходный дом, у которого есть имя</h2>'
      '<p>Дом на Садовой-Самотечной построен в начале XX века по проекту архитектора '
      'Василия Волокитина в стиле северный модерн с элементами готики: массивные формы, '
      'природные цвета и фактуры, никаких мелких деталей. Фасады украшают лепные '
      'барельефы с фигурами средневековых дам и воинов в доспехах, у парадных стоят '
      'парные скульптуры крылатых львов.</p>'
      '<p>Главная деталь дала дому имя: <b>статуя рыцаря в латах на уровне седьмого '
      'этажа</b>, который опирается на меч. В парадном вестибюле сохранились росписи '
      'с геральдикой, лепные медальоны и пол из метлахской плитки.</p></div>'
      '<div class="kn-about__ph kn-r">'
      f'<img src="{IMG}/facade.jpg" width="748" height="887" '
      'alt="Фасад дома на Садовой-Самотечной: северный модерн, стрельчатые окна '
      'и лепные барельефы" loading="lazy"></div>'
      '</div>'
      f'<div class="kn-facts kn-r">{cells}</div>'
      '</div></section>')


def task():
    items = [
      'Продать шесть апартаментов, а не квадратные метры: у дома есть история, '
      'и она стоит дороже описания планировок.',
      'Уложить в одно издание две разные вещи, легенду про рыцарей и сухие метражи '
      'шести лотов, так чтобы они не спорили друг с другом.',
      'Показать готику, не превращая брошюру в стилизацию под средневековье '
      'и не сползая в орнамент.',
      'Дать менеджеру инструмент для показа: планы двух этажей рядом, чтобы разница '
      'между лотами читалась за секунду.',
    ]
    lis = ''.join(f'<li><i>{i}</i><p>{t}</p></li>' for i, t in enumerate(items, 1))
    return (
      '<section class="kn-task kn-dark"><div class="kn-w kn-task__grid">'
      '<div class="kn-r"><span class="kn-kick">Задача</span>'
      '<h2>Рассказать про дом раньше, чем про метры</h2></div>'
      f'<ul class="kn-r">{lis}</ul>'
      '</div></section>')


def knights():
    """Живая схема: линии от семи домов с рыцарями сходятся на Манежной площади."""
    import math
    cx, cy, R = 300, 300, 232
    marks, rays = '', ''
    for code, ang, lbl, note in KNIGHTS:
        a = math.radians(ang - 90)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        ln = round(math.hypot(x - cx, y - cy))
        rays += (f'<path class="ray" id="kn-ray-{code}" style="--len:{ln}" '
                 f'd="M{x:.1f} {y:.1f} L{cx} {cy}"/>')
        # ромб-маркер, как на карте в брошюре
        marks += (f'<g class="kt" id="kn-kt-{code}" data-k="{code}" role="button" '
                  f'tabindex="0" aria-label="Рыцарь: {H.escape(lbl)}">'
                  f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13"/>'
                  f'<path d="M{x:.1f} {y - 6:.1f} L{x + 6:.1f} {y:.1f} '
                  f'L{x:.1f} {y + 6:.1f} L{x - 6:.1f} {y:.1f} Z"/></g>')
    return (
      '<section class="kn-kn kn-dark"><div class="kn-w">'
      '<div class="kn-r" style="max-width:74ch"><span class="kn-kick">Полоса 2</span>'
      '<h2>Семь рыцарей и точка на Манежной</h2>'
      '<p class="kn-kn__lede">Вторая полоса брошюры это легенда. Семь рыцарей появились '
      'на фасадах московских домов в одно время и получили направления по сторонам света. '
      'Если провести линии от радиально стоящих домов, они пересекутся на Манежной '
      'площади, где при раскопках нашли образ Георгия Победоносца. Мы вынесли эту схему '
      'из текста в графику: наведите на рыцаря.</p></div>'
      '<div class="kn-kn__grid kn-r">'
      f'<svg class="kn-map" id="kn-map" viewBox="0 0 600 600" '
      f'aria-label="Схема: линии от семи домов с рыцарями сходятся на Манежной площади">'
      f'<circle class="ring" cx="{cx}" cy="{cy}" r="{R}"/>'
      f'<circle class="ring" cx="{cx}" cy="{cy}" r="{R - 74}"/>'
      f'{rays}'
      f'<g class="hub"><circle cx="{cx}" cy="{cy}" r="7"/>'
      f'<circle cx="{cx}" cy="{cy}" r="18"/></g>'
      f'<text class="lbl" x="{cx + 28}" y="{cy + 5}">Манежная</text>'
      f'{marks}</svg>'
      '<div>'
      '<div class="kn-kn__say" id="kn-say"><b>Наведите на рыцаря</b>'
      '<span>Юг и восток охраняют самые старые бородатые рыцари: эти направления '
      'требуют взвешенных решений. Северу достался самый молодой, а запад закрыли '
      'четверо.</span></div>'
      '<p class="kn-kn__note">Схема условная: в брошюре названы направления, а не адреса. '
      'Наш дом стоит на внутренней стороне Садового кольца.</p>'
      '</div></div></div></section>')


def flats():
    tabs = ''.join(
      f'<button class="kn-tab{" is-on" if i == 0 else ""}" type="button" data-f="{code}" '
      f'aria-pressed="{"true" if i == 0 else "false"}"><b>{name}</b>'
      f'<i>{area} м², {fl} этаж</i></button>'
      for i, (code, name, fl, area, rooms, text) in enumerate(FLATS))
    panes = ''
    for i, (code, name, fl, area, rooms, text) in enumerate(FLATS):
        total = sum(a for _n, a in rooms)
        bars = ''.join(f'<i style="width:{a / total * 100:.2f}%" '
                       f'title="{H.escape(n)}, {str(a).replace(".", ",")} м²"></i>'
                       for n, a in rooms)
        lis = ''.join(f'<li><span>{H.escape(n)}</span>'
                      f'<b>{str(a).replace(".0", "").replace(".", ",")}</b></li>'
                      for n, a in rooms)
        panes += (
          f'<div class="kn-flat{" is-on" if i == 0 else ""}" id="kn-flat-{code}">'
          f'<div><div class="kn-flat__area">{area}<sup>м²</sup></div>'
          f'<div class="kn-flat__floor">Апартамент {name}, {fl} этаж</div>'
          f'<p>{text}</p>'
          f'<div class="kn-bar" aria-hidden="true">{bars}</div>'
          f'<ul class="kn-rooms">{lis}</ul></div>'
          f'<figure class="kn-flat__ph"><img src="{IMG}/plan-{fl}.jpg" width="1000" '
          f'height="460" alt="План {fl} этажа дома с апартаментами '
          f'{"А1, А2, А3" if fl == 2 else "В1, В2, В3"}" loading="lazy">'
          f'<figcaption>План {fl} этажа из брошюры. Апартамент {name} подкрашен '
          f'своим тоном, метраж подписан внутри помещений.</figcaption></figure></div>')
    return (
      '<section class="kn-flats" id="kn-flats"><div class="kn-w">'
      '<div class="kn-r" style="max-width:70ch"><span class="kn-kick">Живой блок</span>'
      '<h2>Шесть лотов, которые в печати занимают шесть полос</h2>'
      '<p class="kn-flats__lede">В брошюре каждый апартамент разложен на две полосы: '
      'текст и план. На сайте те же данные собраны в один блок: выберите лот, и состав '
      'помещений покажет полоса, где ширина куска равна метражу.</p></div>'
      f'<div class="kn-tabs kn-r" id="kn-tabs" role="group" aria-label="Выбор апартамента">{tabs}</div>'
      f'<div class="kn-r">{panes}</div>'
      '<p class="kn-flats__note">Метраж помещений и итог по лоту даны как в брошюре. '
      'У А3 и В3 планировка одна, разница в площади идёт по внешней стене дома.</p>'
      '</div></section>')


def district():
    rows = [
      ('Театры', 'Красная площадь, Успенский собор, Храм Василия Блаженного, Цирк '
       'на Цветном, Большой театр и МХТ имени Чехова.'),
      ('Посольства и министерства', 'Напротив дома Управление ГИБДД ГУ МВД России, '
       'рядом Минстрой, Минпросвещения и Департамент здравоохранения. Большая часть '
       'посольств Москвы стоит в Тверском районе.'),
      ('Парки', 'Зарядье, Патриаршие пруды, Сад Эрмитаж, Александровский сад, '
       'Делегатский парк и парк Осипа Бове.'),
      ('Транспорт', '8 минут пешком до станции «Цветной бульвар», быстрый выезд '
       'на Садовое кольцо, 10 минут до Кремля и до Белорусского вокзала.'),
    ]
    dl = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows)
    return (
      '<section class="kn-dist kn-dark"><div class="kn-w kn-dist__grid">'
      '<div class="kn-r"><span class="kn-kick">Полоса 5</span>'
      '<h2>Район как часть предложения</h2>'
      f'<dl>{dl}</dl></div>'
      '<div class="kn-dist__ph kn-r">'
      f'<img src="{IMG}/map.jpg" width="851" height="1031" '
      'alt="Карта Тверского района из брошюры: дом отмечен ромбом на Садовом кольце" '
      'loading="lazy"></div>'
      '</div></section>')


def book():
    slides, thumbs = '', ''
    total = len(PAGES)
    for i, (num, chap, title, text, alt) in enumerate(PAGES, 1):
        src = f'{IMG}/page-{num:02d}.jpg'
        eager = 'eager' if i == 1 else 'lazy'
        slides += (
          f'<figure class="kn-slide" data-i="{i}">'
          f'<div class="kn-slide__ph kn-zoom" role="button" tabindex="0" data-src="{src}" '
          f'data-cap="Полоса {num} из {total}: {H.escape(title)}" '
          f'aria-label="Открыть полосу {num} на весь экран">'
          f'<span class="kn-slide__pg">Полоса {num}</span>'
          f'<span class="kn-slide__ch">{chap}</span>'
          f'<img src="{src}" width="1700" height="1030" alt="{alt}" loading="{eager}">'
          f'<span class="kn-slide__zoom">Открыть крупно</span></div>'
          f'<figcaption><h3>{H.escape(title)}</h3><p>{text}</p></figcaption></figure>')
        thumbs += (f'<button class="kn-thumb{" is-on" if i == 1 else ""}" data-go="{i}" '
                   f'type="button" aria-label="Полоса {num}">'
                   f'<img src="{IMG}/thumb-{num:02d}.jpg" width="220" height="133" alt="" '
                   f'loading="lazy"></button>')
    return (
      '<section class="kn-book" id="kn-book"><div class="kn-w">'
      '<div class="kn-book__hd kn-r"><div><span class="kn-kick">Полосы</span>'
      f'<h2>{total} полос подряд</h2></div>'
      '<p class="kn-book__hint">Издание альбомное, поэтому полосы идут по одной. '
      'Нажмите на полосу, чтобы рассмотреть её целиком.</p></div>'
      f'<div class="kn-track" id="kn-track">{slides}</div>'
      '<div class="kn-nav"><div class="kn-nav__btns">'
      f'<button class="kn-arrow kn-arrow--prev" id="kn-prev" type="button" aria-label="Предыдущая полоса">{CHEV}</button>'
      f'<button class="kn-arrow kn-arrow--next" id="kn-next" type="button" aria-label="Следующая полоса">{CHEV}</button>'
      f'<span class="kn-count" id="kn-count"><b>01</b> / {total}</span></div>'
      f'<div class="kn-thumbs" id="kn-thumbs">{thumbs}</div>'
      '</div></div></section>')


def craft():
    return (
      '<section class="kn-craft kn-dark"><div class="kn-w kn-craft__grid">'
      '<div class="kn-r"><span class="kn-kick">Графика</span>'
      '<h2>Линия вместо декора</h2>'
      '<p style="margin-top:22px">Готику легко испортить орнаментом, поэтому в издании '
      'её нет вовсе. Вместо лепнины работает <b>одна медная линия толщиной в волос</b>: '
      'она собирается в шевроны, повторяет ритм аркады по низу полосы и уходит '
      'в пересечения, из которых на обложке складывается герб.</p>'
      '<p>Фотография врезана в шеврон, а не в прямоугольник, поэтому фасад и парадное '
      'попадают в ту же геометрию, что и линии. Чёрный лист держит всё издание, '
      'светлые полосы включаются только там, где нужно читать длинный текст.</p>'
      '<div class="kn-pal">'
      '<div class="kn-sw kn-sw--i"><span>Чёрный лист</span><small>#141310</small></div>'
      '<div class="kn-sw kn-sw--c"><span>Медь</span><small>#B3763C</small></div>'
      '<div class="kn-sw kn-sw--g"><span>Золото</span><small>#C9A25E</small></div>'
      '<div class="kn-sw kn-sw--p"><span>Бумага</span><small>#F4F1EA</small></div>'
      '</div></div>'
      '<div class="kn-craft__ph kn-r"><figure>'
      f'<img src="{IMG}/gate.jpg" width="510" height="1031" '
      'alt="Полоса брошюры: фотография парадного входа врезана в шеврон, рядом медный '
      'треугольник и сетка линий" loading="lazy">'
      '<figcaption>Тот же шеврон работает и как кадр, и как указатель: он выводит '
      'взгляд к следующей полосе, а медный треугольник рядом закрывает композицию '
      'без единой рамки.</figcaption>'
      '</figure></div>'
      '</div></section>')


def result():
    items = [
      ('18', 'Готовый макет на <b>18 полос</b> с препрессом: вылеты, полноцвет, файл '
       'для типографии. Издание, а не набор макетов.'),
      ('6', '<b>Шесть лотов</b> с планами, метражами и текстом под каждый. Менеджер '
       'открывает нужную полосу вместо пересказа планировки.'),
      ('2', '<b>Две части в одном издании</b>: сначала дом и легенда, потом метры. '
       'Порядок держит внимание: покупатель успевает захотеть дом до того, как '
       'начинает считать площадь.'),
      ('1', '<b>Одна линия</b> вместо готического орнамента. Такую графику можно '
       'переиздавать и переносить в баннеры и на сайт, не переверстывая полосы.'),
    ]
    lis = ''.join(f'<li><span>{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="kn-res"><div class="kn-w kn-res__grid">'
      '<div class="kn-r"><span class="kn-kick">Результат</span>'
      '<h2>Что получил клиент</h2>'
      '<p class="kn-res__more">Концепция, тексты, вёрстка и препресс. Больше '
      'о направлении: <a href="/creativedesign">услуга «Creative&nbsp;&amp;&nbsp;Design»</a></p></div>'
      f'<ul class="kn-res__list kn-r">{lis}</ul>'
      '</div></section>')


LIGHTBOX = ('<div class="kn-lb" id="kn-lb" aria-hidden="true">'
            '<div class="kn-lb__box">'
            '<button class="kn-lb__x" id="kn-lb-x" type="button" aria-label="Закрыть">&times;</button>'
            '<img id="kn-lb-img" src="" alt="">'
            '<div class="kn-lb__cap" id="kn-lb-cap"></div></div></div>')

KNIGHT_JS_DATA = ',\n  '.join(
  f'{code}:{{t:{H.escape(lbl)!r},n:{H.escape(note)!r}}}'.replace("'", '"')
  for code, ang, lbl, note in KNIGHTS)

PAGE_JS = """<script>(function(){
 // ── листалка полос ──
 var track=document.getElementById('kn-track');
 if(track){
  var slides=[].slice.call(track.querySelectorAll('.kn-slide')),
      thumbs=[].slice.call(document.querySelectorAll('.kn-thumb')),
      prev=document.getElementById('kn-prev'),next=document.getElementById('kn-next'),
      count=document.getElementById('kn-count'),cur=1,total=slides.length;
  function pad(n){return n<10?'0'+n:''+n;}
  function mark(i){cur=i;
   count.innerHTML='<b>'+pad(i)+'</b> / '+total;
   thumbs.forEach(function(t,k){t.classList.toggle('is-on',k===i-1);});
   prev.disabled=(i===1);next.disabled=(i===total);
   var t=thumbs[i-1];
   if(t&&t.parentNode.scrollWidth>t.parentNode.clientWidth){
    var box=t.parentNode,l=t.offsetLeft-(box.clientWidth-t.offsetWidth)/2;
    box.scrollTo({left:l,behavior:'smooth'});}
  }
  function go(i){i=Math.min(total,Math.max(1,i));
   track.scrollTo({left:slides[i-1].offsetLeft-track.offsetLeft,behavior:'smooth'});mark(i);}
  prev.addEventListener('click',function(){go(cur-1);});
  next.addEventListener('click',function(){go(cur+1);});
  thumbs.forEach(function(t){t.addEventListener('click',function(){go(+t.getAttribute('data-go'));});});
  var tmr;
  track.addEventListener('scroll',function(){clearTimeout(tmr);tmr=setTimeout(function(){
   var mid=track.scrollLeft+track.clientWidth/2,best=1,d=1e9;
   slides.forEach(function(s,k){var c=s.offsetLeft-track.offsetLeft+s.offsetWidth/2,
    dd=Math.abs(c-mid);if(dd<d){d=dd;best=k+1;}});
   if(best!==cur)mark(best);},90);});
  track.addEventListener('keydown',function(e){
   if(e.key==='ArrowRight'){e.preventDefault();go(cur+1);}
   if(e.key==='ArrowLeft'){e.preventDefault();go(cur-1);}});
  mark(1);
 }
 // ── выбор апартамента ──
 var ftabs=document.getElementById('kn-tabs');
 if(ftabs){
  var fb=[].slice.call(ftabs.querySelectorAll('.kn-tab'));
  fb.forEach(function(b){b.addEventListener('click',function(){
   var id=b.getAttribute('data-f');
   fb.forEach(function(x){var on=(x===b);x.classList.toggle('is-on',on);
    x.setAttribute('aria-pressed',on?'true':'false');});
   [].forEach.call(document.querySelectorAll('.kn-flat'),function(p){
    p.classList.toggle('is-on',p.id==='kn-flat-'+id);});
  });});
 }
 // ── семь рыцарей ──
 var KN={__DATA__};
 var say=document.getElementById('kn-say');
 if(say){
  [].forEach.call(document.querySelectorAll('.kn-map .kt'),function(g){
   function on(){var k=g.getAttribute('data-k'),d=KN[k];
    [].forEach.call(document.querySelectorAll('.kn-map .kt'),function(x){
     x.classList.toggle('is-on',x===g);});
    [].forEach.call(document.querySelectorAll('.kn-map .ray'),function(r){
     r.classList.toggle('is-on',r.id==='kn-ray-'+k);});
    say.innerHTML='<b>'+d.t+'</b><span>'+d.n+'</span>';}
   g.addEventListener('mouseenter',on);
   g.addEventListener('focus',on);
   g.addEventListener('click',on);
   g.addEventListener('keydown',function(e){
    if(e.key==='Enter'||e.key===' '){e.preventDefault();on();}});
  });
 }
 // ── лайтбокс ──
 var lb=document.getElementById('kn-lb'),lbi=document.getElementById('kn-lb-img'),
     lbc=document.getElementById('kn-lb-cap'),lbx=document.getElementById('kn-lb-x');
 function open(src,cap,alt){lbi.src=src;lbi.alt=alt||'';lbc.textContent=cap||'';
  lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';lbx.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  lbi.removeAttribute('src');document.body.style.overflow='';}
 [].forEach.call(document.querySelectorAll('.kn-zoom'),function(z){
  function fire(){var im=z.querySelector('img');
   open(z.getAttribute('data-src'),z.getAttribute('data-cap'),im?im.alt:'');}
  z.addEventListener('click',fire);
  z.addEventListener('keydown',function(e){
   if(e.key==='Enter'||e.key===' '){e.preventDefault();fire();}});});
 lbx.addEventListener('click',close);
 lb.addEventListener('click',function(e){if(e.target===lb||e.target===lb.firstChild)close();});
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape'&&lb.classList.contains('is-open'))close();});
 // ── reveal ──
 var els=[].slice.call(document.querySelectorAll('.kn-r'));
 function show(n){n.classList.add('is-in');
  var m=n.querySelector('.kn-map');if(m)m.classList.add('is-in');
  if(n.classList.contains('kn-map'))n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(show);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){show(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)show(n);else io.observe(n);});
})();</script>""".replace('__DATA__', KNIGHT_JS_DATA)

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Брошюра «Дом с рыцарем»",'
  f'"item":"{URL}"}}]}}</script>')


def build():
    # Отдельного CTA-блока нет: фиолетовая форма из rc.footer() уже закрывает страницу
    body = (f'{rc.header()}<main class="kn">{hero()}{about()}{task()}{knights()}'
            f'{flats()}{district()}{book()}{craft()}{result()}</main>{LIGHTBOX}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'becar', 'knight-house')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
