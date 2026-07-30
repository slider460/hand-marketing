#!/usr/bin/env python3
"""Генерит mirror/event/samsung/index.html — кейс «Новый год Samsung 2020»:
корпоративный вечер, где новогоднюю атмосферу собрали из проекций.

Дизайн-концепция: «сказка снаружи, схема внутри». Гость видел зимний лес по дуге
зала, логотип в воздухе и светящийся почтовый ящик; за этим стояли панорамные
полотна, сетка с автосбросом и УКФ-проектор в задекорированном коробе. Страница
показывает оба слоя: тёмный ночной лист с проекционными кадрами плюс «инженерный
лист» на светлом фоне, где те же кадры подписаны по оборудованию.

Шрифты: Geologica (дисплей) + Onest (текст) + JetBrains Mono (данные, консоль)
из /fonts/geologica-onest.css.

Живые блоки:
  • переключатель «взгляд гостя / взгляд техника»: на трёх кадрах появляются
    подписи по оборудованию (панорама зала, сетка над сценой, зона ящика);
  • расчёт дистанции проекции L = W × k: почему в короб перед ящиком встал только
    объектив с ультракоротким фокусом, плюс демонстрация потери контраста
    при засветке зоны;
  • схема сигнала: контент, медиасервер, три канала вывода и датчик обратно;
  • почтовый ящик Деда Мороза: открытка уходит в ящик, датчик даёт сигнал,
    на стене включается одна из пяти заставок;
  • сетка над сценой: схематичное полотно поверх кадра уходит вниз по кнопке;
  • вечер по шагам: от монтажа с фермами до конфетти, листалка со снапом;
  • галерея на 38 кадров с лайтбоксом и стрелками.

Ассеты: mirror/images/samsung/ (scripts/samsung-assets.py).
Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->. index-a2.html в каталоге кейса быть не должно: деплой
переименовывает его в index.html и затёр бы кастомную страницу."""
import os
import importlib.util
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/samsung'
URL = 'https://hand-marketing.ru/event/samsung/'
VIDEO = '/media/samsung-new-year-2020.mp4'

# ─── Галерея: alt к g-01..g-38 в порядке хода вечера ──────────────────────────
GALLERY = [
 'Гости и персонажи в белых пушистых костюмах у входа в зал',
 'Гости Samsung фотографируются с персонажами в белых костюмах на серебряном фоне',
 'Руководитель Samsung с персонажами-снежками в фотозоне',
 'Дед Мороз и гостья в фотозоне новогоднего вечера Samsung',
 'Дед Мороз и Снегурочка у мраморной лестницы',
 'Снегурочка у стеклянного почтового ящика, в открытом коробе виден проектор',
 'Гостья опускает открытку в стеклянный ящик, на стене проекция приветствия',
 'Гостья выбирает новогоднюю открытку на стойке рядом с ящиком',
 'Сервировка стола с приглашением и новогодним декором',
 'Панорамная проекция зимнего леса по дуге зала, гости за столами',
 'Зал во время ужина: проекция леса и цветная заливка потолка',
 'Гости снимают на телефоны проекцию с белыми зверями на стенах зала',
 'Зал с наклонным полотном над столами и панорамными экранами',
 'Золотые фигуры оленей на фоне проекции с блёстками и логотипом Samsung',
 'Главный экран: ёлка из частиц и надпись 50 years of experience',
 'Духовой оркестр в белых костюмах с заячьими ушами',
 'Оркестр в белых костюмах играет у проекции зимнего леса',
 'Артистки в костюмах снежинок на сцене',
 'Логотип Samsung на проекционной сетке, артисты работают за полотном',
 'Спикер на сцене, на экране надпись 50 years of experience is our greatest power in 2020',
 'Экран с представлением президента штаб-квартиры Samsung в России и странах СНГ',
 'Ведущий и артист на сцене, на экране имя David Yang',
 'Ведущие вечера на сцене на фоне проекции с блёстками',
 'Ведущий в синем костюме с пером на сцене',
 'Певица в белом платье с длинным полотном, над сценой воздушная гимнастка',
 'Танцоры на сцене на фоне синей графики',
 'Артист на сцене на фоне яркой геометрической графики',
 'Артисты на сцене на фоне бирюзовой светодиодной графики',
 'Табло музыкального конкурса на главном экране, участники на сцене',
 'Общий план сцены с группой и золотой графикой на экранах',
 'Торт с логотипом Samsung, гости разрезают его на сцене',
 'Гости и артисты на сцене под падающими блёстками',
 'Танцпол у сцены во время финального выступления',
 'Гости машут белыми салфетками у сцены',
 'Финал вечера: конфетти над сценой и гостями',
 'Чёрно-белый кадр: гость поднял руки на танцполе',
 'Ведущая на сцене на фоне синего экрана',
 'Три гостьи в вечерних платьях на фоне проекции с цифрами 2020',
]

# ─── Кадры «взгляда техника»: подписи по оборудованию ─────────────────────────
# (файл, ширина, высота, подпись гостя, [(x, y, номер-подписи), ...])
SHOTS = [
 ('annot-hall.jpg', 1400, 933, 'Зал под зимним лесом: гости ужинали внутри картинки',
  'Панорама зала',
  [(0.17, 0.25, 'Панорамное полотно: зимний лес по дуге балкона'),
   (0.56, 0.05, 'Заливка потолка светом идёт за сценарием вечера'),
   (0.33, 0.16, 'Наклонное полотно над залом'),
   (0.66, 0.72, 'Зона ужина: картинку видно с любого стола'),
   (0.88, 0.20, 'Гирлянды на колоннах: тёплый акцент рядом с холодной проекцией')]),
 ('annot-stage.jpg', 1400, 933, 'Логотип висел в воздухе, артисты выходили прямо из него',
  'Сцена и сетка',
  [(0.51, 0.44, 'Логотип на проекционной сетке перед артистами'),
   (0.09, 0.34, 'Боковое панорамное полотно с лесом'),
   (0.50, 0.26, 'Контровой свет в дыму рисует объём'),
   (0.34, 0.59, 'Артисты работают за полотном'),
   (0.74, 0.80, 'Столы стоят почти у сцены')]),
 ('annot-mail.jpg', 980, 1441, 'Открытку опускали в светящийся ящик и получали ответ на стене',
  'Зона почтового ящика',
  [(0.74, 0.83, 'Проектор с ультракоротким фокусом в задекорированном коробе'),
   (0.66, 0.40, 'Стеклянный ящик с датчиком'),
   (0.60, 0.14, 'Проекция на стене: заставка меняется в момент отправки'),
   (0.27, 0.28, 'Снегурочка помогает гостям заполнить открытку')]),
]

# ─── Схема сигнала: (код, подпись, пояснение для панели) ─────────────────────
NODES = [
 ('content', 'Контент', 'Заставки, панорамные сюжеты и ролики. Зимний лес, олени, '
  'белки и Дед Мороз на санях сделаны отдельными сценами, чтобы их можно было '
  'запускать в любом порядке по ходу вечера.'),
 ('server', 'Медиасервер', 'Держит все сцены и раздаёт их по каналам. Один и тот же '
  'сервер отвечает и за панорамные полотна, и за сетку над сценой, и за зону '
  'почтового ящика, поэтому картинки не расходятся между собой.'),
 ('pano', 'Панорамные полотна', 'Дуга зала и балкон: сюда идёт зимний лес и сказочные '
  'персонажи. Полотна работают весь вечер, включая ужин и паузы между номерами.'),
 ('mesh', 'Сетка над сценой', 'Полупрозрачное полотно на всю ширину портала. Пока на '
  'него идёт картинка, графика висит в воздухе; система автоматического сброса '
  'снимает сетку, и номер продолжается на открытой сцене.'),
 ('proj', 'УКФ-проектор у ящика', 'Отдельный канал на стену за почтовым ящиком. '
  'Проектор спрятан в задекорированный короб прямо перед ящиком, поэтому луч '
  'не перекрывают гости.'),
 ('sensor', 'Датчик в ящике', 'Стеклянный ящик с датчиком: как только открытка падает '
  'внутрь, сигнал уходит на сервер, и тот переключает сцену на стене. Это '
  'единственный вход в системе, всё остальное идёт от сервера наружу.'),
]

# ─── Проекторы для расчёта дистанции: (код, имя, throw ratio, примечание) ─────
LENSES = [
 ('ukf', 'Ультракороткий фокус', 0.25, 'самый близкий вынос от стены'),
 ('short', 'Короткофокусный', 0.80, 'нужен вынос в зону гостей'),
 ('std', 'Стандартный', 1.50, 'проектор оказался бы в центре зоны'),
]

# ─── Вечер по шагам: (файл, глава, заголовок, текст, alt) ─────────────────────
BEATS = [
 ('build-1.jpg', 'Монтаж', 'Зал до гостей',
  'Строительные леса в центре зала, приборы заводят на подвес, столы уже стоят. '
  'Проекция начинается не с контента, а с геометрии: где висят полотна, откуда '
  'бьёт луч, что перекрывает картинку.',
  'Монтаж в зале: строительные леса и подвес световых приборов над накрытыми столами'),
 ('build-2.jpg', 'Монтаж', 'Работа на ферме',
  'Приборы и проекторы разводят по фермам. От точки подвеса зависит, попадёт ли '
  'картинка на полотно целиком и не будет ли она ломаться на архитектуре зала.',
  'Техник работает на ферме под потолком зала, подсветка синим'),
 ('build-3.jpg', 'Монтаж', 'Полотно над сценой',
  'Сетку поднимают на портал сцены. Полотно должно уйти вниз по сигналу за секунды, '
  'поэтому систему сброса проверяют до прогонов, а не в момент номера.',
  'Проекционное полотно на подвесе над сценой во время монтажа'),
 ('build-4.jpg', 'Монтаж', 'Короб для проектора',
  'Тот самый короб, в который спрятали проектор у почтового ящика. Он собирается '
  'на месте: снаружи это декорация, внутри техника и кабель до сервера.',
  'Монтажники собирают декорированный короб для проектора в холле'),
 ('build-5.jpg', 'Настройка', 'Юстировка проекции',
  'Картинку выставляют по месту и проверяют на засветку. В холле с мрамором и '
  'светильниками контраст падает, поэтому яркость и глубину чёрного в контенте '
  'подбирают под конкретную зону.',
  'Настройка проекции на стену холла: на поверхности видна надпись 50 years of experience'),
 ('welcome.jpg', 'Встреча', 'Гостей встречали снежки',
  'Первый кадр вечера, который видит гость: белые персонажи у входа. Дальше '
  'фотозона, оркестр в таких же костюмах и лестница в зал.',
  'Два персонажа в белых пушистых костюмах встречают гостей у входа'),
 ('mail-drop.jpg', 'Почта', 'Открытка в ящик',
  'Гость выбирал открытку, подписывал её и опускал в стеклянный ящик. В этот момент '
  'срабатывал датчик, и на стене включалась новогодняя заставка.',
  'Гостья опускает открытку в стеклянный почтовый ящик, на стене проекция приветствия'),
 ('hero.jpg', 'Ужин', 'Зал под зимним лесом',
  'Панорамные полотна идут по дуге балкона, поэтому лес читается с любого стола. '
  'Контент меняется медленно и не мешает разговору за столом.',
  'Панорамная проекция зимнего леса по дуге зала, гости за столами'),
 ('mesh.jpg', 'Сцена', 'Логотип в воздухе',
  'Номер начинается с графики на сетке: логотип и снежная графика висят перед '
  'артистами. После сброса полотна сцена открывается целиком.',
  'Логотип Samsung на проекционной сетке, артисты работают за полотном'),
 ('quiz.jpg', 'Конкурс', 'Счёт на главном экране',
  'Музыкальный конкурс со счётом на большом экране. Экран, боковые полотна и свет '
  'идут из одной системы, поэтому переход от номера к конкурсу занимает секунды.',
  'Табло музыкального конкурса на главном экране, участники на сцене'),
 ('cake.jpg', 'Торт', 'Логотип на торте',
  'Кульминация официальной части: торт с логотипом на сцене и общий кадр '
  'с руководством.',
  'Торт с логотипом Samsung на сцене, гости разрезают его'),
 ('finale.jpg', 'Финал', 'Конфетти',
  'Финальный номер, конфетти над сценой и танцпол. Техника к этому моменту работает '
  'уже пятый час, без пауз на перезапуск.',
  'Финал вечера: конфетти над сценой и гостями'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
PLAY = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M8 5.5v13l11-6.5z"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 5l-7 7 7 7"/></svg>')

PAGE_CSS = """<style id="sm-css">
:root{
 --sm-ink:#05080F;--sm-night:#0A1024;--sm-navy:#111B3C;--sm-line:rgba(143,211,255,.18);
 --sm-blue:#1428A0;--sm-live:#4C8DFF;--sm-ice:#8FD3FF;--sm-gold:#E9B44C;
 --sm-paper:#EDF2FA;--sm-snow:#F6F9FF;--sm-mute:#9BADD0;
 --sm-df:'Geologica',system-ui,-apple-system,Arial,sans-serif;
 --sm-tf:'Onest',system-ui,-apple-system,Arial,sans-serif;
 --sm-mf:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
}
.sm{font-family:var(--sm-tf);font-size:17px;line-height:1.65;color:var(--sm-snow);
 background:var(--sm-ink);-webkit-font-smoothing:antialiased;overflow-x:clip}
.sm *{box-sizing:border-box}
.sm h1,.sm h2,.sm h3{font-family:var(--sm-df);font-weight:600;line-height:1.08;
 letter-spacing:-.015em;margin:0;text-wrap:balance}
.sm p{margin:14px 0 0}
.sm a{color:inherit}
.sm-w{width:min(1240px,100% - 40px);margin-inline:auto}
.sm-kick{font-family:var(--sm-mf);font-weight:500;font-size:11.5px;letter-spacing:.2em;
 text-transform:uppercase;display:block;color:var(--sm-ice)}
.sm-r{opacity:0;transform:translateY(22px);transition:opacity .8s cubic-bezier(.2,.7,.3,1),
 transform .8s cubic-bezier(.2,.7,.3,1)}
.sm-r.is-in{opacity:1;transform:none}
.sm-mono{font-family:var(--sm-mf);font-variant-numeric:tabular-nums}
.sm-note{margin-top:18px;font-family:var(--sm-mf);font-size:12px;line-height:1.6;
 color:var(--sm-mute);max-width:74ch}
.sm-btn{display:inline-flex;align-items:center;gap:10px;font-family:var(--sm-tf);
 font-weight:600;font-size:14px;padding:14px 26px;border-radius:999px;cursor:pointer;
 text-decoration:none;border:1px solid transparent;transition:transform .2s,background .2s,
 border-color .2s,color .2s}
.sm-btn svg{width:17px;height:17px}
.sm-btn:hover{transform:translateY(-2px)}
.sm .sm-btn--f{background:var(--sm-live);color:#04102B;font-weight:700}
.sm .sm-btn--f:hover{background:#6ea3ff}
.sm .sm-btn--g{border-color:rgba(143,211,255,.34);color:var(--sm-snow)}
.sm .sm-btn--g:hover{background:rgba(76,141,255,.14);border-color:var(--sm-live)}

/* ── ГЕРОЙ ── */
.sm-hero{position:relative;overflow:hidden;padding:clamp(38px,5vw,64px) 0 0;
 background:radial-gradient(120% 80% at 78% 4%,rgba(20,40,160,.55) 0%,rgba(5,8,15,0) 62%),
 radial-gradient(90% 60% at 8% 96%,rgba(76,141,255,.2) 0%,rgba(5,8,15,0) 60%),var(--sm-ink)}
.sm-snow{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:.62}
.sm-hero__in{position:relative;z-index:2}
.sm-hero__top{display:flex;justify-content:space-between;align-items:baseline;gap:18px;
 flex-wrap:wrap;padding-bottom:clamp(22px,3vw,38px);border-bottom:1px solid var(--sm-line)}
.sm-mark{font-family:var(--sm-mf);font-weight:500;font-size:12px;letter-spacing:.24em;
 text-transform:uppercase;color:var(--sm-ice)}
.sm-back{font-family:var(--sm-mf);font-size:12px;letter-spacing:.1em;color:var(--sm-mute);
 text-decoration:none}
.sm-back:hover{color:var(--sm-snow)}
.sm-hero__grid{display:grid;grid-template-columns:1.02fr .98fr;gap:clamp(26px,4vw,58px);
 align-items:center;padding:clamp(30px,4.6vw,58px) 0 0}
.sm-hero h1{font-size:clamp(38px,6vw,82px);font-weight:500;margin-top:16px}
.sm-hero h1 b{font-weight:700;color:var(--sm-ice);display:block;
 text-shadow:0 0 42px rgba(143,211,255,.35)}
.sm-hero__sub{font-size:clamp(15.5px,1.32vw,18.5px);color:#C4D2EC;max-width:56ch}
.sm-chips{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0 0;padding:0;list-style:none}
.sm-chips li{font-family:var(--sm-mf);font-size:11.5px;letter-spacing:.06em;
 text-transform:uppercase;padding:7px 14px;border-radius:999px;color:#CFE0FF;
 border:1px solid var(--sm-line);background:rgba(17,27,60,.5)}
.sm-hero__cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:clamp(24px,3vw,34px)}
.sm-hero__art{position:relative}
.sm-hero__art img{display:block;width:100%;height:auto;border-radius:20px;
 border:1px solid var(--sm-line);box-shadow:0 50px 110px -60px rgba(0,0,0,.95)}
.sm-hero__cap{margin-top:12px;font-family:var(--sm-mf);font-size:11.5px;line-height:1.55;
 color:var(--sm-mute)}
.sm-spec{position:relative;z-index:2;margin-top:clamp(30px,4vw,54px);
 border-top:1px solid var(--sm-line)}
.sm-spec__in{display:grid;grid-template-columns:repeat(4,1fr);margin:0;
 width:min(1240px,100% - 40px);margin-inline:auto}
.sm-spec__in>div{padding:24px 24px 30px 0;border-right:1px solid var(--sm-line)}
.sm-spec__in>div:last-child{border-right:0}
.sm-spec dt{font-family:var(--sm-df);font-weight:600;font-size:clamp(26px,3vw,40px);
 line-height:1;color:var(--sm-ice);font-variant-numeric:lining-nums}
.sm-spec dd{margin:10px 0 0;font-size:13.5px;line-height:1.5;color:var(--sm-mute);
 max-width:26ch}

/* ── БРИФ ── */
.sm-brief{padding:clamp(56px,7vw,100px) 0;background:var(--sm-night)}
.sm-brief__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(18px,2.4vw,30px);
 margin-top:clamp(26px,3.4vw,44px)}
.sm-brief h2{font-size:clamp(28px,3.6vw,46px);max-width:26ch}
.sm-card{padding:26px 26px 30px;border-radius:18px;background:rgba(17,27,60,.58);
 border:1px solid var(--sm-line)}
.sm-card h3{font-size:15px;font-weight:600;font-family:var(--sm-mf);letter-spacing:.14em;
 text-transform:uppercase;color:var(--sm-ice)}
.sm-card p{color:#C4D2EC;font-size:16px}

/* ── ЧТО ВИДЕЛИ ГОСТИ ── */
.sm-scene{padding:clamp(56px,7vw,100px) 0;background:var(--sm-ink)}
.sm-scene h2{font-size:clamp(28px,3.8vw,50px);max-width:24ch;margin-top:16px}
.sm-scene__lede{font-size:clamp(16px,1.25vw,18px);color:#C4D2EC;max-width:68ch}
.sm-mosaic{display:grid;grid-template-columns:repeat(6,1fr);
 grid-template-rows:clamp(240px,26vw,392px) clamp(180px,19vw,272px);gap:14px;
 margin-top:clamp(28px,3.4vw,46px)}
.sm-tile{position:relative;overflow:hidden;border-radius:16px;border:1px solid var(--sm-line);
 background:var(--sm-navy)}
.sm-tile img{display:block;width:100%;height:100%;object-fit:cover}
.sm-tile figcaption{position:absolute;inset:auto 0 0 0;padding:44px 18px 16px;font-size:13.5px;
 line-height:1.5;color:#EAF2FF;
 background:linear-gradient(to top,rgba(4,8,18,.94),rgba(4,8,18,.55) 52%,rgba(4,8,18,0))}
.sm-tile figcaption b{display:block;font-family:var(--sm-mf);font-size:11px;
 letter-spacing:.14em;text-transform:uppercase;color:var(--sm-ice);margin-bottom:5px}
.sm-tile--a{grid-column:span 4}
.sm-tile--b{grid-column:span 2}
.sm-tile--c{grid-column:span 3}
.sm-tile--d{grid-column:span 3}

/* ── ИНЖЕНЕРНЫЙ ЛИСТ (светлый) ── */
.sm-sheet{background:var(--sm-paper);color:#0C1330;
 background-image:linear-gradient(rgba(20,40,160,.055) 1px,transparent 1px),
 linear-gradient(90deg,rgba(20,40,160,.055) 1px,transparent 1px);
 background-size:34px 34px}
.sm-sheet .sm-kick{color:var(--sm-blue)}
.sm-sheet h2{font-size:clamp(28px,3.8vw,50px);max-width:26ch;margin-top:16px}
.sm-sheet p{color:#33406B}
.sm-sheet .sm-note{color:#5A6690}
.sm-two{padding:clamp(56px,7vw,100px) 0 clamp(40px,5vw,64px)}
.sm-two__hd{display:grid;grid-template-columns:1.2fr .8fr;gap:clamp(20px,3vw,44px);
 align-items:end}
.sm-two__lede{font-size:clamp(16px,1.25vw,18px);max-width:60ch}
.sm-switch{display:inline-flex;padding:5px;border-radius:999px;background:#fff;
 border:1px solid rgba(20,40,160,.16);box-shadow:0 12px 30px -22px rgba(12,19,48,.6)}
.sm-switch button{font-family:var(--sm-tf);font-weight:600;font-size:13.5px;padding:11px 22px;
 border:0;border-radius:999px;background:transparent;color:#3A4770;cursor:pointer;
 transition:background .22s,color .22s}
.sm-switch button.is-on{background:var(--sm-blue);color:#fff}
.sm-shots{display:grid;grid-template-columns:1.32fr 1.32fr .84fr;gap:clamp(14px,1.8vw,22px);
 margin-top:clamp(26px,3.2vw,44px);align-items:start}
.sm-shot{position:relative}
.sm-shot__ph{position:relative;overflow:hidden;border-radius:14px;background:#0A1024;
 border:1px solid rgba(20,40,160,.2)}
.sm-shot__ph img{display:block;width:100%;height:auto}
.sm-shot__no{position:absolute;left:12px;top:12px;z-index:4;font-family:var(--sm-mf);
 font-size:11px;letter-spacing:.12em;padding:5px 10px;border-radius:6px;
 background:rgba(4,8,18,.72);color:#CFE0FF;text-transform:uppercase}
.sm-shot__guest{margin-top:12px;font-size:15px;line-height:1.55;color:#33406B;
 transition:opacity .3s}
.sm-shot__list{margin:12px 0 0;padding:0;list-style:none;display:none}
.sm-shot__list li{position:relative;padding-left:30px;font-family:var(--sm-mf);font-size:12px;
 line-height:1.55;color:#33406B;margin-top:9px}
.sm-shot__list li b{position:absolute;left:0;top:0;width:20px;height:20px;border-radius:50%;
 background:var(--sm-blue);color:#fff;font-size:11px;display:flex;align-items:center;
 justify-content:center}
.sm-pin{position:absolute;z-index:3;transform:translate(-50%,-50%);opacity:0;
 transition:opacity .35s;pointer-events:none}
.sm-pin__dot{position:relative;width:22px;height:22px;border-radius:50%;
 background:var(--sm-live);color:#04102B;font-family:var(--sm-mf);font-size:11px;
 font-weight:700;display:flex;align-items:center;justify-content:center;cursor:help;
 box-shadow:0 0 0 4px rgba(76,141,255,.28),0 0 22px rgba(76,141,255,.7)}
/* подпись всплывает по наведению на точку: иначе они наезжают друг на друга,
   а полный список всё равно стоит под кадром */
.sm-pin__lbl{position:absolute;left:30px;top:-6px;width:max-content;max-width:210px;
 font-family:var(--sm-mf);font-size:10.5px;line-height:1.45;padding:7px 10px;border-radius:8px;
 background:rgba(4,8,18,.94);color:#DCE9FF;border:1px solid rgba(143,211,255,.34);
 opacity:0;transition:opacity .2s;pointer-events:none}
.sm-pin--l .sm-pin__lbl{left:auto;right:30px;text-align:right}
.sm-pin:hover .sm-pin__lbl{opacity:1}
.sm-shots.is-tech .sm-pin{opacity:1;pointer-events:auto}
.sm-shots.is-tech .sm-shot__list li:hover b{background:var(--sm-live);color:#04102B}
.sm-shots.is-tech .sm-shot__guest{opacity:0;height:0;margin:0;overflow:hidden}
.sm-shots.is-tech .sm-shot__list{display:block}
.sm-shots.is-tech .sm-shot__ph img{filter:saturate(.7) brightness(.82)}
.sm-shot__ph img{transition:filter .35s}

/* ── РАСЧЁТ ДИСТАНЦИИ ── */
.sm-throw{padding:clamp(40px,5vw,66px) 0 clamp(56px,7vw,100px)}
.sm-throw__grid{display:grid;grid-template-columns:.92fr 1.08fr;gap:clamp(24px,3.4vw,52px);
 margin-top:clamp(24px,3vw,40px);align-items:start}
.sm-form{padding:24px 24px 28px;border-radius:18px;background:#fff;
 border:1px solid rgba(20,40,160,.14);box-shadow:0 26px 60px -46px rgba(12,19,48,.7)}
.sm-form__eq{font-family:var(--sm-mf);font-size:13px;color:var(--sm-blue);
 padding-bottom:16px;border-bottom:1px dashed rgba(20,40,160,.22)}
.sm-ctrl{margin-top:20px}
.sm-ctrl label{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
 font-family:var(--sm-mf);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;
 color:#5A6690}
.sm-ctrl label output{font-size:15px;letter-spacing:0;color:var(--sm-blue);font-weight:700;
 text-transform:none}
.sm-ctrl input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:26px;
 margin:4px 0 0;background:transparent;cursor:pointer}
.sm-ctrl input[type=range]::-webkit-slider-runnable-track{height:4px;border-radius:4px;
 background:linear-gradient(90deg,var(--sm-blue),var(--sm-live))}
.sm-ctrl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;
 width:20px;height:20px;margin-top:-8px;border-radius:50%;background:#fff;
 border:2px solid var(--sm-blue);box-shadow:0 4px 12px rgba(12,19,48,.28)}
.sm-ctrl input[type=range]::-moz-range-track{height:4px;border-radius:4px;background:#C6D3F2}
.sm-ctrl input[type=range]::-moz-range-thumb{width:18px;height:18px;border-radius:50%;
 background:#fff;border:2px solid var(--sm-blue)}
.sm-rows{margin:22px 0 0;padding:0;list-style:none}
.sm-rows li{padding:13px 0;border-top:1px solid rgba(20,40,160,.12)}
.sm-rows .rw{display:flex;justify-content:space-between;align-items:baseline;gap:14px}
.sm-rows b{font-family:var(--sm-tf);font-weight:600;font-size:15px;color:#0C1330}
.sm-rows i{font-style:normal;font-family:var(--sm-mf);font-size:11px;color:#5A6690;
 display:block;margin-top:2px}
.sm-rows .val{font-family:var(--sm-mf);font-size:17px;font-weight:700;color:var(--sm-blue);
 white-space:nowrap}
.sm-rows .bar{height:6px;border-radius:6px;background:#DFE7F8;margin-top:9px;overflow:hidden}
.sm-rows .bar i{display:block;height:100%;margin:0;border-radius:6px;
 background:linear-gradient(90deg,var(--sm-live),var(--sm-blue));transition:width .35s}
.sm-rows li.is-fit .val{color:#0E7A3C}
.sm-rows li.is-fit .bar i{background:linear-gradient(90deg,#2FBF6B,#0E7A3C)}
.sm-verdict{margin-top:20px;padding:16px 18px;border-radius:14px;
 background:rgba(20,40,160,.07);border-left:3px solid var(--sm-blue);font-size:15px;
 line-height:1.55;color:#22305C}
.sm-plan{border-radius:18px;overflow:hidden;background:#0A1024;
 border:1px solid rgba(20,40,160,.2)}
.sm-plan svg{display:block;width:100%;height:auto}
.sm-plan__hd{display:flex;justify-content:space-between;gap:12px;padding:12px 16px;
 font-family:var(--sm-mf);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
 color:#8FA6D8;border-bottom:1px solid rgba(143,211,255,.16)}
.sm-lux{margin-top:clamp(20px,2.6vw,30px);display:grid;grid-template-columns:1fr 1fr;
 gap:clamp(16px,2vw,26px);align-items:center}
.sm-lux__ph{position:relative;border-radius:14px;overflow:hidden;background:#000;
 border:1px solid rgba(20,40,160,.2)}
.sm-lux__ph img{display:block;width:100%;height:auto}
.sm-lux__haze{position:absolute;inset:0;background:#EAF1FF;opacity:0;transition:opacity .25s}
.sm-lux__tag{position:absolute;left:12px;bottom:12px;font-family:var(--sm-mf);font-size:11px;
 padding:5px 9px;border-radius:6px;background:rgba(4,8,18,.7);color:#CFE0FF}

/* ── СХЕМА СИГНАЛА ── */
.sm-flow{padding:clamp(56px,7vw,100px) 0;background:var(--sm-night)}
.sm-flow h2{font-size:clamp(28px,3.8vw,50px);max-width:24ch;margin-top:16px}
.sm-flow__grid{display:grid;grid-template-columns:1.42fr .58fr;gap:clamp(22px,3vw,44px);
 margin-top:clamp(26px,3.2vw,44px);align-items:center}
.sm-map{display:block;width:100%;height:auto}
.sm-map .wire{fill:none;stroke:rgba(143,211,255,.3);stroke-width:1.6}
.sm-map .flow{fill:none;stroke:var(--sm-live);stroke-width:2.2;stroke-dasharray:9 15;
 opacity:.9;animation:sm-dash 1.5s linear infinite}
.sm-map .flow--back{stroke:var(--sm-gold);animation-direction:reverse}
@keyframes sm-dash{to{stroke-dashoffset:-48}}
.sm-map .nd rect{fill:rgba(17,27,60,.92);stroke:rgba(143,211,255,.34);stroke-width:1.4;
 transition:fill .25s,stroke .25s}
.sm-map .nd text{fill:#DCE9FF;font-family:var(--sm-mf);font-size:14px}
.sm-map .nd{cursor:pointer}
.sm-map .nd:hover rect,.sm-map .nd.is-on rect{fill:rgba(20,40,160,.92);stroke:var(--sm-live)}
.sm-map .nd.is-on text{fill:#fff}
.sm-map .nd--in rect{stroke:rgba(233,180,76,.5)}
.sm-map .nd--in.is-on rect{stroke:var(--sm-gold);fill:rgba(70,52,16,.8)}
.sm-map .cap{fill:#7E93C4;font-family:var(--sm-mf);font-size:11px;letter-spacing:.1em}
.sm-say{padding:24px 26px 28px;border-radius:18px;background:rgba(5,8,15,.6);
 border:1px solid var(--sm-line);min-height:230px}
.sm-say b{display:block;font-family:var(--sm-df);font-size:21px;font-weight:600;
 color:var(--sm-ice);margin-bottom:10px}
.sm-say span{display:block;font-size:15.5px;line-height:1.6;color:#C4D2EC}
.sm-chain{display:none;margin:26px 0 0;padding:0;list-style:none}
.sm-chain li{padding:14px 16px;border-radius:14px;background:rgba(17,27,60,.6);
 border:1px solid var(--sm-line);margin-top:10px}
.sm-chain li b{display:block;font-family:var(--sm-mf);font-size:12px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--sm-ice)}
.sm-chain li span{display:block;margin-top:6px;font-size:14.5px;line-height:1.55;color:#C4D2EC}
.sm-chain li.in{border-color:rgba(233,180,76,.4)}
.sm-chain li.in b{color:var(--sm-gold)}

/* ── ПОЧТОВЫЙ ЯЩИК ── */
.sm-mail{padding:clamp(56px,7vw,100px) 0;
 background:radial-gradient(90% 70% at 82% 12%,rgba(20,40,160,.5),rgba(5,8,15,0) 60%),
 var(--sm-ink)}
.sm-mail h2{font-size:clamp(28px,3.8vw,50px);max-width:22ch;margin-top:16px}
.sm-mail__grid{display:grid;grid-template-columns:.86fr 1.14fr;gap:clamp(24px,3.4vw,52px);
 margin-top:clamp(28px,3.4vw,46px);align-items:start}
.sm-mail__ph{margin:22px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.sm-mail__ph figure{margin:0}
.sm-mail__ph img{display:block;width:100%;height:auto;border-radius:12px;
 border:1px solid var(--sm-line)}
.sm-mail__ph figcaption{margin-top:8px;font-family:var(--sm-mf);font-size:10.5px;
 line-height:1.5;color:var(--sm-mute)}
.sm-rig{border-radius:20px;overflow:hidden;background:rgba(10,16,36,.86);
 border:1px solid var(--sm-line)}
.sm-wall{position:relative;aspect-ratio:16/9;overflow:hidden;background:#0B1330;
 border-bottom:1px solid var(--sm-line)}
/* затемнение под текстом, иначе мотив спорит с пожеланием */
.sm-wall::after{content:"";position:absolute;inset:0;z-index:3;pointer-events:none;
 background:radial-gradient(58% 40% at 50% 66%,rgba(3,8,22,.82),rgba(3,8,22,0) 74%);
 opacity:0;transition:opacity .6s}
.sm-rig.is-live .sm-wall::after{opacity:1}
.sm-wall__bg{position:absolute;inset:0;z-index:1;opacity:0;transition:opacity .7s}
.sm-wall__bg.is-on{opacity:1}
.sm-wall__bg svg{position:absolute;left:50%;top:40%;transform:translate(-50%,-50%);
 width:44%;height:auto;opacity:.8}
.sm-wall__test{position:absolute;inset:0;z-index:4;transition:opacity .5s}
.sm-wall__test svg{position:absolute;inset:0;width:100%;height:100%}
.sm-rig.is-live .sm-wall__test{opacity:0}
.sm-wall__idle{position:absolute;inset:0;z-index:5;display:flex;align-items:center;
 justify-content:center;flex-direction:column;gap:8px;text-align:center;padding:20px;
 font-family:var(--sm-mf);font-size:12px;letter-spacing:.12em;text-transform:uppercase;
 color:#7C93C8;transition:opacity .4s}
.sm-rig.is-live .sm-wall__idle{opacity:0}
.sm-wall__txt{position:absolute;left:0;right:0;top:70%;z-index:6;transform:translateY(-50%);
 padding:0 clamp(18px,4vw,44px);text-align:center;opacity:0;transition:opacity .6s .2s}
.sm-rig.is-live .sm-wall__txt{opacity:1}
.sm-wall__txt em{display:block;font-family:var(--sm-df);font-style:normal;font-weight:400;
 font-size:clamp(15px,2vw,25px);letter-spacing:.01em;line-height:1.35;color:#fff;
 text-shadow:0 0 30px rgba(143,211,255,.6)}
.sm-wall__txt small{display:block;margin-top:10px;font-family:var(--sm-mf);font-size:11px;
 letter-spacing:.18em;text-transform:uppercase;color:var(--sm-ice)}
.sm-wall__flake{position:absolute;top:-8%;z-index:2;width:4px;height:4px;border-radius:50%;
 background:rgba(255,255,255,.85);animation:sm-fall linear infinite;opacity:0}
.sm-rig.is-live .sm-wall__flake{opacity:1}
@keyframes sm-fall{0%{transform:translateY(0)}100%{transform:translateY(340px)}}
.sm-rig__body{display:grid;grid-template-columns:1.06fr .94fr;gap:0}
.sm-fields{padding:22px 22px 24px;border-right:1px solid var(--sm-line)}
.sm-fields label{display:block;font-family:var(--sm-mf);font-size:11px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--sm-ice);margin:0 0 7px}
.sm-fields .f{margin-top:16px}
.sm-fields .f:first-child{margin-top:0}
.sm-fields input,.sm-fields select,.sm-fields textarea{width:100%;font:500 15px var(--sm-tf);
 color:#EAF2FF;background:rgba(5,8,15,.72);border:1px solid var(--sm-line);border-radius:10px;
 padding:11px 13px;outline:none;transition:border-color .2s}
.sm-fields textarea{resize:vertical;min-height:74px;line-height:1.5}
.sm-fields input:focus,.sm-fields select:focus,.sm-fields textarea:focus{
 border-color:var(--sm-live)}
.sm-fields select{appearance:none;background-image:linear-gradient(45deg,transparent 50%,
 #8FD3FF 50%),linear-gradient(135deg,#8FD3FF 50%,transparent 50%);
 background-position:calc(100% - 18px) 19px,calc(100% - 12px) 19px;
 background-size:6px 6px,6px 6px;background-repeat:no-repeat}
.sm-cnt{display:flex;justify-content:space-between;margin-top:6px;font-family:var(--sm-mf);
 font-size:10.5px;color:var(--sm-mute)}
.sm-send{width:100%;margin-top:18px;justify-content:center}
.sm-log{padding:22px;background:rgba(5,8,15,.55)}
.sm-log__hd{font-family:var(--sm-mf);font-size:10.5px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--sm-mute);padding-bottom:12px;
 border-bottom:1px dashed var(--sm-line)}
.sm-log__lines{margin:0;padding:0;list-style:none;font-family:var(--sm-mf);font-size:11.5px;
 line-height:1.75;min-height:108px}
.sm-log__lines li{opacity:0;transform:translateX(-6px);color:#BFD3F5;
 transition:opacity .3s,transform .3s}
.sm-log__lines li.is-in{opacity:1;transform:none}
.sm-log__lines li u{text-decoration:none;color:var(--sm-live)}
.sm-log__lines li.ok u{color:#54D28A}
.sm-log__lines li.in u{color:var(--sm-gold)}
.sm-box{margin-top:16px;display:flex;align-items:flex-end;gap:14px}
.sm-box__glass{position:relative;width:64px;height:88px;border-radius:8px;
 border:1px solid rgba(143,211,255,.5);
 background:linear-gradient(180deg,rgba(143,211,255,.28),rgba(76,141,255,.1));
 box-shadow:inset 0 0 26px rgba(143,211,255,.4);overflow:hidden;flex:none}
.sm-box__slot{position:absolute;left:12px;right:12px;top:9px;height:3px;border-radius:3px;
 background:rgba(5,8,15,.7)}
.sm-card2{position:absolute;left:14px;top:-30px;width:36px;height:24px;border-radius:3px;
 background:#F6F9FF;box-shadow:0 3px 10px rgba(0,0,0,.4);opacity:0}
.sm-rig.is-drop .sm-card2{animation:sm-drop 1s cubic-bezier(.5,.05,.7,.6) forwards}
@keyframes sm-drop{0%{opacity:1;top:-30px;transform:rotate(-8deg)}
 55%{opacity:1;top:16px;transform:rotate(2deg)}
 100%{opacity:.9;top:62px;transform:rotate(6deg)}}
.sm-box__note{font-family:var(--sm-mf);font-size:10.5px;line-height:1.6;color:var(--sm-mute)}
.sm-box__note b{display:block;color:var(--sm-ice);font-weight:500}

/* ── СЕТКА НАД СЦЕНОЙ ── */
.sm-mesh{padding:clamp(56px,7vw,100px) 0;background:var(--sm-night)}
.sm-mesh h2{font-size:clamp(28px,3.8vw,50px);max-width:22ch;margin-top:16px}
.sm-mesh__grid{display:grid;grid-template-columns:1.24fr .76fr;gap:clamp(24px,3.4vw,48px);
 margin-top:clamp(26px,3.2vw,44px);align-items:center}
.sm-stage{position:relative;border-radius:18px;overflow:hidden;border:1px solid var(--sm-line);
 background:#05080F}
.sm-stage img{display:block;width:100%;height:auto}
/* полотно нарисовано поверх кадра: сетка плюс лёгкая дымка, как у настоящей гардины,
   поэтому при сбросе картинка под ней становится чище */
.sm-veil{position:absolute;left:7%;right:7%;top:13%;bottom:32%;
 background-image:linear-gradient(rgba(143,211,255,.26) 1px,transparent 1px),
 linear-gradient(90deg,rgba(143,211,255,.26) 1px,transparent 1px);
 background-size:15px 15px;border:1px solid rgba(143,211,255,.45);
 background-color:rgba(120,170,255,.07);
 -webkit-backdrop-filter:blur(1.4px) saturate(.9);backdrop-filter:blur(1.4px) saturate(.9);
 box-shadow:inset 0 0 60px rgba(76,141,255,.22);
 transition:transform 1.15s cubic-bezier(.5,.02,.6,.55),opacity 1.15s}
.sm-veil__tag{position:absolute;left:0;top:-1px;transform:translateY(-100%);
 font-family:var(--sm-mf);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
 padding:5px 9px;border-radius:6px 6px 0 0;background:rgba(76,141,255,.85);color:#04102B}
.sm-stage.is-down .sm-veil{transform:translateY(102%);opacity:0}
.sm-stage__state{position:absolute;right:14px;top:14px;font-family:var(--sm-mf);font-size:11px;
 letter-spacing:.1em;padding:6px 11px;border-radius:6px;background:rgba(4,8,18,.78);
 color:#CFE0FF;border:1px solid var(--sm-line)}
.sm-mesh__ctrl{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:22px}
.sm-mesh__log{font-family:var(--sm-mf);font-size:11.5px;color:var(--sm-mute)}

/* ── ВЕЧЕР ПО ШАГАМ ── */
.sm-run{padding:clamp(56px,7vw,100px) 0;background:var(--sm-ink);overflow:hidden}
.sm-run__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;
 flex-wrap:wrap}
.sm-run h2{font-size:clamp(28px,3.8vw,50px);margin-top:16px}
.sm-run__hint{font-family:var(--sm-mf);font-size:11.5px;line-height:1.6;color:var(--sm-mute);
 max-width:34ch}
.sm-track{display:flex;gap:clamp(16px,2vw,26px);overflow-x:auto;scroll-snap-type:x mandatory;
 scrollbar-width:none;padding:clamp(24px,3vw,38px) 0 8px;margin:0 calc(50% - 50vw);
 padding-inline:max(20px,calc(50vw - 620px))}
.sm-track::-webkit-scrollbar{display:none}
.sm-beat{flex:0 0 min(760px,84vw);scroll-snap-align:center}
.sm-beat__ph{position:relative;border-radius:18px;overflow:hidden;border:1px solid var(--sm-line);
 background:var(--sm-navy);cursor:zoom-in}
.sm-beat__ph img{display:block;width:100%;height:auto;aspect-ratio:16/10;object-fit:cover}
.sm-beat__ch{position:absolute;left:14px;top:14px;font-family:var(--sm-mf);font-size:10.5px;
 letter-spacing:.14em;text-transform:uppercase;padding:6px 11px;border-radius:6px;
 background:rgba(4,8,18,.78);color:var(--sm-ice)}
.sm-beat__no{position:absolute;right:14px;top:14px;font-family:var(--sm-mf);font-size:10.5px;
 padding:6px 10px;border-radius:6px;background:rgba(4,8,18,.78);color:var(--sm-mute)}
.sm-beat h3{margin-top:18px;font-size:clamp(19px,2vw,26px)}
.sm-beat p{font-size:15.5px;color:#C4D2EC;max-width:62ch}
.sm-nav{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:clamp(18px,2.4vw,30px)}
.sm-arrow{width:46px;height:46px;border-radius:50%;border:1px solid var(--sm-line);
 background:rgba(17,27,60,.6);color:var(--sm-snow);cursor:pointer;display:inline-flex;
 align-items:center;justify-content:center;transition:background .2s,opacity .2s}
.sm-arrow svg{width:18px;height:18px}
.sm-arrow--next svg{transform:rotate(180deg)}
.sm-arrow:hover{background:rgba(76,141,255,.28)}
.sm-arrow:disabled{opacity:.32;cursor:default}
.sm-count{font-family:var(--sm-mf);font-size:12.5px;color:var(--sm-mute)}
.sm-count b{color:var(--sm-ice)}
.sm-thumbs{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;flex:1 1 320px}
.sm-thumbs::-webkit-scrollbar{display:none}
.sm-thumb{flex:none;width:76px;height:48px;padding:0;border-radius:8px;overflow:hidden;
 border:1px solid var(--sm-line);background:none;cursor:pointer;opacity:.44;
 transition:opacity .2s,border-color .2s}
.sm-thumb img{width:100%;height:100%;object-fit:cover;display:block}
.sm-thumb.is-on{opacity:1;border-color:var(--sm-live)}

/* ── ВИДЕО ── */
.sm-video{padding:clamp(56px,7vw,100px) 0;background:var(--sm-night)}
.sm-video h2{font-size:clamp(28px,3.8vw,50px);max-width:22ch;margin-top:16px}
.sm-video__box{margin-top:clamp(24px,3vw,40px);border-radius:20px;overflow:hidden;
 border:1px solid var(--sm-line);background:#000;position:relative;aspect-ratio:16/9}
.sm-video__box video{display:block;width:100%;height:100%;object-fit:cover}
.sm-video__cap{margin-top:14px;font-family:var(--sm-mf);font-size:11.5px;color:var(--sm-mute)}

/* ── ГАЛЕРЕЯ ── */
.sm-gal{padding:clamp(56px,7vw,100px) 0;background:var(--sm-ink)}
.sm-gal h2{font-size:clamp(28px,3.8vw,50px);margin-top:16px}
 /* кладка в колонках: кадры разной ориентации ложатся без дыр и без обрезки */
.sm-grid{margin-top:clamp(24px,3vw,40px);columns:4;column-gap:12px}
.sm-cell{display:block;width:100%;margin:0 0 12px;position:relative;overflow:hidden;
 border-radius:12px;border:1px solid var(--sm-line);background:var(--sm-navy);
 cursor:zoom-in;padding:0;break-inside:avoid}
.sm-cell img{width:100%;height:auto;display:block;transition:transform .5s,opacity .3s}
.sm-cell:hover img{transform:scale(1.04)}
.sm-cell:focus-visible{outline:2px solid var(--sm-live);outline-offset:2px}

/* ── РЕЗУЛЬТАТ ── */
.sm-res{padding:clamp(56px,7vw,100px) 0;background:var(--sm-night)}
.sm-res__grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(24px,3.4vw,52px)}
.sm-res h2{font-size:clamp(28px,3.8vw,50px);margin-top:16px}
.sm-res__more{font-family:var(--sm-mf);font-size:12px;line-height:1.7;color:var(--sm-mute);
 margin-top:20px}
.sm-res__more a{color:var(--sm-ice)}
.sm-res__list{margin:0;padding:0;list-style:none}
.sm-res__list li{display:grid;grid-template-columns:56px 1fr;gap:18px;padding:20px 0;
 border-top:1px solid var(--sm-line)}
.sm-res__list li:first-child{border-top:0}
.sm-res__list li>span:first-child{font-family:var(--sm-mf);font-size:12px;color:var(--sm-live);
 padding-top:5px}
.sm-res__list li>span:last-child{font-size:16px;line-height:1.6;color:#C4D2EC}
.sm-res__list b{color:#fff;font-weight:600}

/* ── ЛАЙТБОКС ── */
.sm-lb{position:fixed;inset:0;z-index:9000;display:none;align-items:center;
 justify-content:center;background:rgba(3,6,12,.95);padding:clamp(14px,3vw,44px)}
.sm-lb.is-open{display:flex}
.sm-lb__box{position:relative;max-width:min(1400px,100%);max-height:100%;display:flex;
 flex-direction:column;align-items:center;gap:12px}
.sm-lb img{max-width:100%;max-height:calc(100vh - 150px);object-fit:contain;border-radius:8px}
.sm-lb__cap{font-family:var(--sm-mf);font-size:11.5px;line-height:1.6;color:#BFD3F5;
 text-align:center;max-width:80ch}
.sm-lb__x{position:absolute;right:-6px;top:-46px;width:38px;height:38px;border-radius:50%;
 border:1px solid var(--sm-line);background:rgba(17,27,60,.7);color:#fff;font-size:22px;
 line-height:1;cursor:pointer}
.sm-lb__nav{position:absolute;top:50%;transform:translateY(-50%);width:48px;height:48px;
 border-radius:50%;border:1px solid var(--sm-line);background:rgba(17,27,60,.72);color:#fff;
 cursor:pointer;display:inline-flex;align-items:center;justify-content:center}
.sm-lb__nav svg{width:20px;height:20px}
.sm-lb__nav--p{left:-4px}
.sm-lb__nav--n{right:-4px}
.sm-lb__nav--n svg{transform:rotate(180deg)}
.sm-lb__no{font-family:var(--sm-mf);font-size:11px;color:var(--sm-mute)}

/* ── ПЛАНШЕТ И ТЕЛЕФОН ── */
@media(max-width:1080px){
 .sm-hero__grid,.sm-flow__grid,.sm-mail__grid,.sm-mesh__grid,.sm-res__grid,
 .sm-throw__grid,.sm-two__hd{grid-template-columns:1fr}
 .sm-shots{grid-template-columns:1fr 1fr}
 .sm-shots>div:last-child{grid-column:span 2;max-width:520px}
 .sm-spec__in{grid-template-columns:repeat(2,1fr)}
 .sm-spec__in>div:nth-child(2n){border-right:0}
 .sm-spec__in>div:nth-child(n+3){border-top:1px solid var(--sm-line)}
 .sm-brief__grid{grid-template-columns:1fr}
 .sm-mosaic{grid-template-columns:repeat(4,1fr);
  grid-template-rows:clamp(230px,30vw,320px) clamp(180px,24vw,240px)}
 .sm-tile--a{grid-column:span 2}
 .sm-tile--b,.sm-tile--c,.sm-tile--d{grid-column:span 2}
 .sm-grid{columns:3}
 .sm-two__hd{gap:22px}
}
@media(max-width:820px){
 .sm-map{display:none}
 .sm-chain{display:block}
 .sm-say{display:none}
 .sm-rig__body{grid-template-columns:1fr}
 .sm-fields{border-right:0;border-bottom:1px solid var(--sm-line)}
 .sm-plan .dim{display:none}
 .sm-lux{grid-template-columns:1fr}
}
@media(max-width:640px){
 .sm{font-size:16px}
 .sm-w,.sm-spec__in{width:min(1240px,100% - 32px)}
 .sm-hero h1{font-size:clamp(32px,10vw,44px)}
 .sm-spec__in{grid-template-columns:1fr}
 .sm-spec__in>div{padding:18px 0 20px;border-right:0;border-top:1px solid var(--sm-line)}
 .sm-spec__in>div:first-child{border-top:0}
 .sm-mosaic{grid-template-columns:1fr;grid-template-rows:none;gap:10px}
 .sm-tile--a,.sm-tile--b,.sm-tile--c,.sm-tile--d{grid-column:span 1;aspect-ratio:4/3}
 .sm-shots{grid-template-columns:1fr}
 .sm-shots>div:last-child{grid-column:span 1}
 .sm-pin__lbl{display:none}
 .sm-mail__ph{grid-template-columns:1fr}
 .sm-grid{columns:2;column-gap:8px}
 .sm-cell{margin-bottom:8px}
 .sm-beat{flex:0 0 88vw}
 .sm-res__list li{grid-template-columns:1fr;gap:6px}
 .sm-lb__nav--p{left:-2px}.sm-lb__nav--n{right:-2px}
}
@media(prefers-reduced-motion:reduce){
 .sm-r{opacity:1;transform:none;transition:none}
 .sm-map .flow{animation:none}
 .sm-wall__flake{animation:none;opacity:.5}
 .sm-veil{transition:none}
 .sm-cell:hover img{transform:none}
}
</style>"""


# ─── СЕКЦИИ ──────────────────────────────────────────────────────────────────
def hero():
    spec = [
      ('3', 'проекционные системы в одном зале: панорама, сетка, почтовая зона'),
      ('УКФ', 'объектив с ультракоротким фокусом спрятан в короб перед ящиком'),
      ('1', 'датчик: он переключал картинку в момент отправки открытки'),
      ('∞', 'адресов: открытки уходили в любую точку мира'),
    ]
    dl = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in spec)
    return (
      '<section class="sm-hero">'
      '<canvas class="sm-snow" id="sm-snow" aria-hidden="true"></canvas>'
      '<div class="sm-hero__in"><div class="sm-w">'
      '<div class="sm-hero__top"><span class="sm-mark">Event · Samsung</span>'
      '<a class="sm-back" href="/project">← все проекты</a></div>'
      '<div class="sm-hero__grid">'
      '<div class="sm-r"><span class="sm-kick">Новый год 2020</span>'
      '<h1>Новый год Samsung <b>2020</b></h1>'
      '<p class="sm-hero__sub">Корпоративный вечер, где новогоднюю атмосферу собрали '
      'из проекций: зимний лес по дуге зала, логотип в воздухе над сценой и стеклянный '
      'почтовый ящик Деда Мороза, который отвечал заставкой на каждую опущенную открытку. '
      'Наша часть работы: контент, оборудование, монтаж и техническое сопровождение.</p>'
      '<ul class="sm-chips"><li>Контент</li><li>Мультимедиа</li><li>Монтаж</li>'
      '<li>Техсопровождение</li></ul>'
      '<div class="sm-hero__cta">'
      f'<a class="sm-btn sm-btn--f" href="#sm-video">{PLAY}Смотреть вечер</a>'
      f'<a class="sm-btn sm-btn--g" href="#lead">Обсудить проект{ARROW}</a>'
      '</div></div>'
      '<figure class="sm-hero__art sm-r">'
      f'<img src="{IMG}/hero.jpg" width="1680" height="1120" '
      'alt="Панорамная проекция зимнего леса по дуге зала на новогоднем вечере Samsung" '
      'fetchpriority="high" decoding="async">'
      '<figcaption class="sm-hero__cap">Зимний лес идёт по дуге балкона: панорамное '
      'полотно закрывает зал целиком, поэтому картинка читается с любого стола.</figcaption>'
      '</figure>'
      '</div></div>'
      f'<div class="sm-spec"><dl class="sm-spec__in">{dl}</dl></div>'
      '</div></section>')


def brief():
    cards = [
      ('Задача', 'Разработать контент под мероприятие и собрать новогоднюю атмосферу '
       'в зале. Подобрать и инсталлировать мультимедийное оборудование. Взять на себя '
       'полное техническое сопровождение вечера.'),
      ('Компания', 'Samsung: транснациональная компания, которая делает электронику, '
       'полупроводники, телеком-оборудование, чипы памяти и дисплеи. Тема вечера шла '
       'по всем экранам: 50 years of experience is our greatest power in 2020.'),
      ('Решение', 'Мультимедиа вместо декораций. Зимний лес, олени, белки и Дед Мороз '
       'на санях идут по панорамным полотнам весь вечер, а сцена и почтовая зона '
       'получают свои отдельные проекционные системы.'),
    ]
    cs = ''.join(f'<div class="sm-card"><h3>{k}</h3><p>{v}</p></div>' for k, v in cards)
    return (
      '<section class="sm-brief"><div class="sm-w">'
      '<div class="sm-r" style="max-width:74ch"><span class="sm-kick">Вводные</span>'
      '<h2>Новогоднюю сказку нужно было не построить, а показать</h2></div>'
      f'<div class="sm-brief__grid sm-r">{cs}</div>'
      '</div></section>')


def scenes():
    tiles = [
      ('a', 'hall2.jpg', 1400, 933, 'Зимний лес',
       'Панорамные полотна по дуге зала и балкона держат сюжет весь вечер: лес, '
       'белки и зайцы, Дед Мороз на санях.',
       'Зал вечера: наклонное полотно над столами и панорамные экраны с проекцией'),
      ('b', 'deer.jpg', 980, 1469, 'Олени',
       'Золотые фигуры стоят прямо в проекции, поэтому свет и графика работают вместе.',
       'Золотые фигуры оленей на фоне проекции с блёстками и логотипом Samsung'),
      ('c', 'tree.jpg', 1200, 799, 'Главный экран',
       'Ёлка из частиц и тема вечера: 50 years of experience.',
       'Главный экран вечера: ёлка из частиц и надпись 50 years of experience'),
      ('d', 'content-2.jpg', 1280, 720, 'Кадр контента',
       'Лента и снежинки: заставка, которая закрывала вечер.',
       'Кадр графики вечера: лента, снежинки и логотип Samsung'),
    ]
    ts = ''.join(
      f'<figure class="sm-tile sm-tile--{c}">'
      f'<img src="{IMG}/{f}" width="{w}" height="{h}" alt="{H.escape(alt)}" loading="lazy" '
      f'decoding="async">'
      f'<figcaption><b>{t}</b>{d}</figcaption></figure>'
      for c, f, w, h, t, d, alt in tiles)
    return (
      '<section class="sm-scene"><div class="sm-w">'
      '<div class="sm-r" style="max-width:76ch"><span class="sm-kick">Взгляд гостя</span>'
      '<h2>Зимний лес, олени, белки и Дед Мороз на санях</h2>'
      '<p class="sm-scene__lede">Контент под вечер рисовали сценами, а не одним '
      'бесконечным роликом: у каждой части вечера свой сюжет на полотнах. Пока идёт ужин, '
      'лес живёт медленно и не спорит с разговором за столом; к номеру графика '
      'переходит на сцену и становится частью шоу.</p></div>'
      f'<div class="sm-mosaic sm-r">{ts}</div>'
      '</div></section>')


def two():
    shots = ''
    for i, (f, w, h, guest, name, pins) in enumerate(SHOTS, 1):
        pin_html, list_html = '', ''
        for n, (x, y, lbl) in enumerate(pins, 1):
            side = ' sm-pin--l' if x > 0.62 else ''
            pin_html += (f'<span class="sm-pin{side}" style="left:{x * 100:.1f}%;'
                         f'top:{y * 100:.1f}%"><span class="sm-pin__dot">{n}</span>'
                         f'<span class="sm-pin__lbl">{H.escape(lbl)}</span></span>')
            list_html += f'<li><b>{n}</b>{H.escape(lbl)}</li>'
        shots += (
          f'<div class="sm-shot">'
          f'<div class="sm-shot__ph"><span class="sm-shot__no">{name}</span>'
          f'<img src="{IMG}/{f}" width="{w}" height="{h}" alt="{H.escape(guest)}" '
          f'loading="lazy" decoding="async">{pin_html}</div>'
          f'<p class="sm-shot__guest">{H.escape(guest)}</p>'
          f'<ul class="sm-shot__list">{list_html}</ul></div>')
    return (
      '<section class="sm-two"><div class="sm-w">'
      '<div class="sm-two__hd">'
      '<div class="sm-r"><span class="sm-kick">Живой блок</span>'
      '<h2>Две стороны одной проекции</h2>'
      '<p class="sm-two__lede">Гость видит сказку, техник видит плоскости, лучи и точки '
      'подвеса. Это одни и те же кадры вечера: переключите режим, и на фотографиях '
      'появятся подписи по оборудованию.</p></div>'
      '<div class="sm-switch sm-r" id="sm-switch" role="group" aria-label="Режим просмотра">'
      '<button type="button" class="is-on" data-mode="guest" aria-pressed="true">'
      'Взгляд гостя</button>'
      '<button type="button" data-mode="tech" aria-pressed="false">Взгляд техника</button>'
      '</div></div>'
      f'<div class="sm-shots sm-r" id="sm-shots">{shots}</div>'
      '<p class="sm-note">Подписи расставлены по кадрам вечера. Точные модели приборов '
      'и схему подвеса согласовывали с площадкой, здесь показан принцип.</p>'
      '</div></section>')


# ─── План зоны: вид сверху, стена, короб, три проектора ───────────────────────
SC = 56.0        # пикселей схемы на метр
WALL = 56.0      # линия стены
CX = 360.0       # центр картинки
BOXD = 0.9       # глубина короба перед ящиком, м (по кадру зоны)
FLOOR = 318.0    # нижняя граница схемы
MONO = 'JetBrains Mono, monospace'


def ru(v, d=2):
    """Число по-русски: 0,65 вместо 0.65."""
    return f'{v:.{d}f}'.replace('.', ',')


def geom(w):
    """Геометрия схемы для ширины картинки w (м): точки объектива и подписи."""
    half = w * SC / 2
    out = {}
    for code, name, k, _note in LENSES:
        y = WALL + w * k * SC
        out[code] = {'y': min(y, FLOOR - 34), 'off': y > FLOOR - 34,
                     'dist': w * k, 'half': half, 'name': name}
    return half, out


def plan_svg(w=2.6):
    """Схема с готовым стартовым состоянием: без JS страница остаётся осмысленной."""
    half, g = geom(w)
    u = g['ukf']
    dots = ''
    for x, y in [(96, 128), (150, 186), (110, 250), (196, 292), (268, 214),
                 (556, 132), (612, 196), (520, 262), (648, 250), (588, 300),
                 (300, 296), (430, 288), (664, 146), (72, 196)]:
        dots += f'<circle cx="{x}" cy="{y}" r="9" fill="#31406E" opacity=".55"/>'
    ghosts = ''
    for code, col in (('short', '#E9B44C'), ('std', '#FF8A8A')):
        d = g[code]
        y, lbl = d['y'], f'{d["name"].lower()} {ru(d["dist"])} м'
        ghosts += (
          f'<g opacity=".9">'
          f'<line id="sm-ray-{code}-a" x1="{CX:.0f}" y1="{y:.0f}" x2="{CX - half:.0f}" '
          f'y2="{WALL:.0f}" stroke="{col}" stroke-width="1" stroke-dasharray="4 5" '
          'opacity=".5"/>'
          f'<line id="sm-ray-{code}-b" x1="{CX:.0f}" y1="{y:.0f}" x2="{CX + half:.0f}" '
          f'y2="{WALL:.0f}" stroke="{col}" stroke-width="1" stroke-dasharray="4 5" '
          'opacity=".5"/>'
          f'<rect id="sm-box-{code}" x="{CX - 30:.0f}" y="{y:.0f}" width="60" height="24" '
          f'rx="4" fill="rgba(10,16,36,.9)" stroke="{col}" stroke-width="1.4" '
          'stroke-dasharray="5 4"/>'
          f'<text id="sm-lbl-{code}" x="{CX + 42:.0f}" y="{y + 16:.0f}" fill="{col}" '
          f'font-family="{MONO}" font-size="13">{lbl}</text></g>')
    return (
      '<svg id="sm-plan" viewBox="0 0 720 340" '
      'aria-label="Схема зоны сверху: стена с картинкой, короб с проектором, '
      'зона гостей и дистанции для трёх типов объективов">'
      '<defs><linearGradient id="sm-beam" x1="0" y1="1" x2="0" y2="0">'
      '<stop offset="0" stop-color="#8FD3FF" stop-opacity=".42"/>'
      '<stop offset="1" stop-color="#4C8DFF" stop-opacity=".08"/></linearGradient>'
      '<pattern id="sm-hatch" width="8" height="8" patternUnits="userSpaceOnUse" '
      'patternTransform="rotate(45)">'
      '<line x1="0" y1="0" x2="0" y2="8" stroke="rgba(143,211,255,.22)" stroke-width="1.4"/>'
      '</pattern></defs>'
      '<rect width="720" height="340" fill="#0A1024"/>'
      f'<rect x="40" y="{WALL + BOXD * SC:.0f}" width="640" '
      f'height="{FLOOR - WALL - BOXD * SC:.0f}" fill="rgba(49,64,110,.16)"/>'
      f'{dots}'
      f'<text x="52" y="{FLOOR - 8:.0f}" fill="#5E7099" font-family="{MONO}" '
      'font-size="12">зона гостей</text>'
      # стена и штриховка за ней
      f'<rect x="40" y="{WALL - 14:.0f}" width="640" height="14" fill="url(#sm-hatch)" '
      'opacity=".5"/>'
      f'<line x1="40" y1="{WALL:.0f}" x2="680" y2="{WALL:.0f}" '
      'stroke="rgba(143,211,255,.55)" stroke-width="3"/>'
      # короб
      f'<rect id="sm-band" x="{CX - 104:.0f}" y="{WALL:.0f}" width="208" '
      f'height="{BOXD * SC:.0f}" fill="rgba(76,141,255,.09)" '
      'stroke="rgba(143,211,255,.4)" stroke-width="1" stroke-dasharray="6 5"/>'
      f'<text x="52" y="{WALL + BOXD * SC - 10:.0f}" fill="#8FA6D8" font-family="{MONO}" '
      f'font-size="12">короб ≈ {ru(BOXD, 1)} м</text>'
      # луч УКФ и сам проектор
      f'<polygon id="sm-beam-p" points="{CX:.0f},{u["y"]:.0f} {CX - half:.0f},{WALL:.0f} '
      f'{CX + half:.0f},{WALL:.0f}" fill="url(#sm-beam)"/>'
      f'<line id="sm-img" x1="{CX - half:.0f}" y1="{WALL:.0f}" x2="{CX + half:.0f}" '
      f'y2="{WALL:.0f}" stroke="#8FD3FF" stroke-width="6"/>'
      f'<text id="sm-img-lbl" x="{CX:.0f}" y="{WALL - 22:.0f}" text-anchor="middle" '
      f'fill="#DCE9FF" font-family="{MONO}" font-size="13" class="dim">'
      f'картинка W = {ru(w)} м</text>'
      f'<rect id="sm-box-ukf" x="{CX - 32:.0f}" y="{u["y"]:.0f}" width="64" height="26" '
      'rx="4" fill="#111B3C" stroke="#4C8DFF" stroke-width="1.8"/>'
      f'<circle id="sm-lens-ukf" cx="{CX:.0f}" cy="{u["y"]:.0f}" r="4.5" fill="#8FD3FF"/>'
      f'<text id="sm-lbl-ukf" x="{CX + 44:.0f}" y="{u["y"] + 18:.0f}" fill="#8FD3FF" '
      f'font-family="{MONO}" font-size="13">укф {ru(u["dist"])} м</text>'
      f'{ghosts}'
      f'<text x="668" y="{FLOOR - 8:.0f}" text-anchor="end" fill="#42527D" '
      f'font-family="{MONO}" font-size="11">вид сверху, схема</text>'
      '</svg>')


def throwcalc():
    rows = ''
    for code, name, k, note in LENSES:
        rows += (f'<li id="sm-row-{code}" data-k="{k}"><div class="rw"><div><b>{name}</b>'
                 f'<i>throw ratio ≈ {str(k).replace(".", ",")}:1, {note}</i></div>'
                 f'<span class="val" id="sm-val-{code}">0,00 м</span></div>'
                 f'<div class="bar"><i id="sm-bar-{code}" style="width:0%"></i></div></li>')
    plan = plan_svg()
    return (
      '<section class="sm-throw"><div class="sm-w">'
      '<div class="sm-r" style="max-width:76ch">'
      '<span class="sm-kick">Расчёт</span>'
      '<h2>Почему у ящика стоял объектив с ультракоротким фокусом</h2>'
      '<p>Проектор нельзя было увести в глубину зоны: вокруг ящика стояли гости, и любой '
      'человек в луче ставил тень на всю картинку. Поэтому проектор спрятали '
      'в задекорированный короб прямо перед ящиком, а объектив взяли с ультракоротким '
      'фокусом. Дистанция до поверхности считается просто: ширину картинки умножаем '
      'на throw ratio объектива.</p></div>'
      '<div class="sm-throw__grid">'
      '<div class="sm-form sm-r">'
      '<div class="sm-form__eq">L = W × k · где L дистанция до стены, W ширина картинки, '
      'k throw ratio</div>'
      '<div class="sm-ctrl"><label for="sm-w">Ширина картинки на стене'
      '<output id="sm-w-out">2,6 м</output></label>'
      '<input type="range" id="sm-w" min="1.2" max="4" step="0.1" value="2.6" '
      'aria-label="Ширина картинки на стене, метры"></div>'
      f'<ul class="sm-rows">{rows}</ul>'
      '<p class="sm-verdict" id="sm-verdict"></p></div>'
      '<div class="sm-r">'
      '<div class="sm-plan"><div class="sm-plan__hd"><span>Зона почтового ящика</span>'
      '<span class="sm-mono" id="sm-plan-tag">L = 0,65 м</span></div>'
      f'{plan}</div>'
      '<div class="sm-lux">'
      '<div class="sm-ctrl"><label for="sm-lux">Засветка зоны'
      '<output id="sm-lux-out">30%</output></label>'
      '<input type="range" id="sm-lux" min="0" max="100" step="1" value="30" '
      'aria-label="Засветка зоны, проценты">'
      '<p class="sm-note" id="sm-lux-say" style="margin-top:10px"></p></div>'
      '<div class="sm-lux__ph">'
      f'<img src="{IMG}/content-1.jpg" width="1280" height="720" '
      'alt="Кадр новогодней графики: как он выглядит на проекции при разной засветке зоны" '
      'loading="lazy" decoding="async">'
      '<span class="sm-lux__haze" id="sm-haze"></span>'
      '<span class="sm-lux__tag sm-mono" id="sm-lux-tag">контраст в норме</span>'
      '</div></div></div></div>'
      '<p class="sm-note">Throw ratio округлён до типовых значений: у УКФ-объективов около '
      '0,25:1, у короткофокусных около 0,8:1, у стандартных около 1,5:1. Глубину короба '
      'берём около 0,9 м, как на кадре зоны. Расчёт показывает логику подбора, конкретную '
      'модель и яркость подбирали по площадке.</p>'
      '</div></section>')


def flow():
    # координаты узлов схемы: (код, x, y, ширина)
    pos = {'content': (30, 118, 168), 'server': (262, 118, 158),
           'pano': (512, 22, 178), 'mesh': (512, 118, 178), 'proj': (512, 214, 178),
           'sensor': (262, 300, 158)}
    NH = 62
    names = {c: n for c, n, _ in NODES}
    nds, wires, flows = '', '', ''
    for code, (x, y, w) in pos.items():
        cls = ' nd--in' if code == 'sensor' else ''
        label = names[code]
        # длинные подписи в две строки
        parts = label.split(' ')
        if len(label) > 16 and len(parts) > 1:
            mid = len(parts) // 2
            l1, l2 = ' '.join(parts[:mid]), ' '.join(parts[mid:])
            txt = (f'<text x="{x + w / 2}" y="{y + NH / 2 - 4}" text-anchor="middle">{l1}</text>'
                   f'<text x="{x + w / 2}" y="{y + NH / 2 + 15}" text-anchor="middle">{l2}</text>')
        else:
            txt = f'<text x="{x + w / 2}" y="{y + NH / 2 + 5}" text-anchor="middle">{label}</text>'
        nds += (f'<g class="nd{cls}" id="sm-nd-{code}" data-n="{code}" role="button" '
                f'tabindex="0" aria-label="{H.escape(label)}">'
                f'<rect x="{x}" y="{y}" width="{w}" height="{NH}" rx="12"/>{txt}</g>')
    # линии: контент → сервер → три канала, датчик → сервер
    cx1 = pos['content'][0] + pos['content'][2]
    sx0, sy = pos['server'][0], pos['server'][1] + NH / 2
    sx1 = sx0 + pos['server'][2]
    wires += f'<path class="wire" d="M{cx1} {sy} H{sx0}"/>'
    flows += f'<path class="flow" d="M{cx1} {sy} H{sx0}"/>'
    for code in ('pano', 'mesh', 'proj'):
        x, y, w = pos[code]
        ty = y + NH / 2
        mid = sx1 + 34
        d = f'M{sx1} {sy} H{mid} V{ty} H{x}'
        wires += f'<path class="wire" d="{d}"/>'
        flows += f'<path class="flow" d="{d}"/>'
    px, py, pw = pos['sensor']
    d = f'M{px + pw / 2} {py} V{pos["server"][1] + NH}'
    wires += f'<path class="wire" d="{d}" stroke-dasharray="5 5"/>'
    flows += f'<path class="flow flow--back" d="{d}"/>'
    chain = ''.join(
      f'<li class="{"in" if c == "sensor" else ""}"><b>{H.escape(n)}</b>'
      f'<span>{H.escape(t)}</span></li>' for c, n, t in NODES)
    return (
      '<section class="sm-flow"><div class="sm-w">'
      '<div class="sm-r" style="max-width:74ch"><span class="sm-kick">Схема</span>'
      '<h2>Один сервер, три канала вывода и один вход</h2>'
      '<p class="sm-scene__lede">Панорама зала, сетка над сценой и зона почтового ящика '
      'это три разные поверхности с разной геометрией, но контент для них живёт '
      'в одном месте. Наведите на блок схемы, чтобы прочитать, что он делает.</p></div>'
      '<div class="sm-flow__grid sm-r">'
      f'<svg class="sm-map" id="sm-map" viewBox="0 0 720 380" '
      'aria-label="Схема сигнала: контент, медиасервер, панорамные полотна, сетка '
      'над сценой, проектор у ящика и датчик обратно на сервер">'
      f'{wires}{flows}{nds}'
      '<text class="cap" x="262" y="376">датчик единственный вход в системе</text>'
      '</svg>'
      '<div class="sm-say" id="sm-say"><b>Медиасервер</b><span>Держит все сцены и раздаёт '
      'их по каналам. Один и тот же сервер отвечает и за панорамные полотна, и за сетку '
      'над сценой, и за зону почтового ящика, поэтому картинки не расходятся между '
      'собой.</span></div>'
      f'<ul class="sm-chain">{chain}</ul>'
      '</div></div></section>')


# заставки почтового ящика: (код, фон, мотив)
def motif(i):
    if i == 1:  # снежинка
        arms = ''
        for a in range(6):
            arms += (f'<g transform="rotate({a * 60} 200 110)">'
                     '<path d="M200 110 V40" stroke="#fff" stroke-width="2.4"/>'
                     '<path d="M200 58 l-13 -13 M200 58 l13 -13 M200 78 l-10 -10 '
                     'M200 78 l10 -10" stroke="#fff" stroke-width="1.8" fill="none"/></g>')
        return f'<svg viewBox="0 0 400 225" aria-hidden="true">{arms}</svg>'
    if i == 2:  # ёлка из точек
        dots = ''
        for r in range(9):
            for c in range(r + 1):
                x = 200 + (c - r / 2) * 15
                y = 40 + r * 16
                dots += f'<circle cx="{x:.0f}" cy="{y}" r="{2.4 if r % 2 else 3.2}" fill="#fff"/>'
        dots += '<rect x="196" y="186" width="8" height="16" fill="#E9B44C"/>'
        return f'<svg viewBox="0 0 400 225" aria-hidden="true">{dots}</svg>'
    if i == 3:  # олень
        return ('<svg viewBox="0 0 400 225" aria-hidden="true">'
                '<path fill="#E9B44C" d="M243 74c4-9 6-18 5-27l7 1c1 8 0 16-2 24l9-11 6 4'
                '-12 15 15-3 2 7-19 5c3 5 4 11 3 17l-7 42c-1 6-5 11-11 13l-6 2 3 40h-8l-3-38'
                'h-33l-3 38h-8l3-40-8-3c-6-2-10-8-11-14l-5-32-14 8-4-6 18-11 4-19c2-10 10-17'
                ' 20-18l40-5c8-1 16 2 21 8zm-49 21c-3 0-5 2-5 5s2 5 5 5 5-2 5-5-2-5-5-5z"/>'
                '<path d="M258 47c-2-9-2-18 1-26l7 2c-2 7-2 14 0 21z" fill="#E9B44C"/>'
                '</svg>')
    if i == 4:  # лента
        return ('<svg viewBox="0 0 400 225" aria-hidden="true">'
                '<path d="M40 150 C120 80 180 200 250 120 S340 60 380 96" fill="none" '
                'stroke="#E9B44C" stroke-width="9" stroke-linecap="round" opacity=".9"/>'
                '<path d="M40 168 C120 98 180 218 250 138 S340 78 380 114" fill="none" '
                'stroke="#8FD3FF" stroke-width="3" stroke-linecap="round" opacity=".8"/>'
                '</svg>')
    stars = ''  # звёздное небо
    seed = [(40, 60), (95, 34), (150, 74), (205, 44), (262, 80), (318, 40), (360, 96),
            (70, 130), (128, 158), (186, 122), (240, 168), (300, 132), (352, 170)]
    for i2, (x, y) in enumerate(seed):
        r = 3.4 if i2 % 3 == 0 else 2.1
        stars += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>'
        if i2 % 4 == 0:
            stars += (f'<path d="M{x - 10} {y} H{x + 10} M{x} {y - 10} V{y + 10}" '
                      'stroke="#fff" stroke-width="1" opacity=".6"/>')
    return f'<svg viewBox="0 0 400 225" aria-hidden="true">{stars}</svg>'


SCREENS = [
 ('s1', 'linear-gradient(160deg,#0B1F63 0%,#123AA8 52%,#0A1024 100%)', 'снежинка'),
 ('s2', 'linear-gradient(180deg,#061436 0%,#0F2E86 60%,#0A1024 100%)', 'ёлка'),
 ('s3', 'linear-gradient(150deg,#12204F 0%,#1E3E9E 55%,#050810 100%)', 'олень'),
 ('s4', 'linear-gradient(200deg,#0A1636 0%,#152F7E 48%,#070C1C 100%)', 'лента'),
 ('s5', 'linear-gradient(170deg,#050B1E 0%,#0E2160 55%,#050810 100%)', 'звёзды'),
]


# тестовая сетка проектора: то, что висит на стене до первой открытки
TESTCARD = (
  '<span class="sm-wall__test" aria-hidden="true">'
  '<svg viewBox="0 0 400 225" preserveAspectRatio="none">'
  '<defs><pattern id="sm-tc" width="25" height="25" patternUnits="userSpaceOnUse">'
  '<path d="M25 0 V25 M0 25 H25" stroke="rgba(143,211,255,.14)" stroke-width="1"/>'
  '</pattern></defs>'
  '<rect width="400" height="225" fill="url(#sm-tc)"/>'
  '<rect x="14" y="14" width="372" height="197" fill="none" '
  'stroke="rgba(143,211,255,.28)" stroke-width="1" stroke-dasharray="6 6"/>'
  '<path d="M200 96 v14 M200 115 v14 M191 105 h14 M210 105 h14" '
  'stroke="rgba(143,211,255,.5)" stroke-width="1.2"/>'
  '<circle cx="200" cy="112" r="26" fill="none" stroke="rgba(143,211,255,.22)" '
  'stroke-width="1"/>'
  '<path d="M14 14 h22 M14 14 v18 M386 14 h-22 M386 14 v18 M14 211 h22 M14 211 v-18 '
  'M386 211 h-22 M386 211 v-18" stroke="rgba(143,211,255,.55)" stroke-width="1.6"/>'
  '</svg></span>')


def mail():
    bgs = ''.join(
      f'<span class="sm-wall__bg" id="sm-bg-{i}" style="background:{grad}">{motif(i)}</span>'
      for i, (code, grad, name) in enumerate(SCREENS, 1))
    flakes = ''.join(
      f'<span class="sm-wall__flake" style="left:{(i * 7 + 4) % 97}%;'
      f'animation-duration:{4 + (i % 5) * 1.3:.1f}s;animation-delay:{(i % 7) * .45:.2f}s;'
      f'width:{2 + i % 3}px;height:{2 + i % 3}px"></span>' for i in range(1, 26))
    cities = ['Сеул', 'Москва', 'Санкт-Петербург', 'Лондон', 'Нью-Йорк', 'Токио',
              'Дубай', 'Алматы', 'Владивосток']
    opts = ''.join(f'<option value="{c}">{c}</option>' for c in cities)
    return (
      '<section class="sm-mail" id="sm-mail"><div class="sm-w">'
      '<div class="sm-r" style="max-width:74ch"><span class="sm-kick">Живой блок</span>'
      '<h2>Почтовый ящик Деда Мороза</h2></div>'
      '<div class="sm-mail__grid">'
      '<div class="sm-r"><p>Отдельная проекционная зона вечера. Гость выбирал открытку, '
      'подписывал её и опускал в стеклянный ящик, чтобы отправить поздравление в любую '
      'точку мира. Ящик стоял на задекорированном коробе, внутри которого работал '
      'проектор с ультракоротким фокусом.</p>'
      '<p>Стекло было не только красивым решением: внутри ящика стоял датчик. Как только '
      'открытка падала внутрь, сигнал уходил на сервер, и тот менял аудиовизуальный '
      'контент на стене. Гость видел ответ на своё письмо сразу, а не через минуту.</p>'
      '<div class="sm-mail__ph">'
      f'<figure><img src="{IMG}/mail-drop.jpg" width="980" height="1469" '
      'alt="Гостья опускает открытку в стеклянный почтовый ящик, на стене проекция" '
      'loading="lazy" decoding="async">'
      '<figcaption>Момент отправки: на стене приветствие почты Деда Мороза.</figcaption>'
      '</figure>'
      f'<figure><img src="{IMG}/mail-cards.jpg" width="1200" height="799" '
      'alt="Гостья выбирает новогоднюю открытку на стойке рядом с ящиком" loading="lazy" '
      'decoding="async">'
      '<figcaption>Стойка с открытками рядом с зоной: выбрать, подписать, отправить.'
      '</figcaption></figure>'
      '</div></div>'
      '<div class="sm-r"><div class="sm-rig" id="sm-rig">'
      f'<div class="sm-wall">{bgs}{flakes}{TESTCARD}'
      '<div class="sm-wall__idle"><span>проекция на стене</span>'
      '<span style="letter-spacing:.04em;text-transform:none;font-size:11px">'
      'ждёт сигнала от датчика</span></div>'
      '<div class="sm-wall__txt"><em id="sm-wall-txt"></em>'
      '<small id="sm-wall-sub"></small></div></div>'
      '<div class="sm-rig__body">'
      '<form class="sm-fields" id="sm-form" autocomplete="off">'
      '<div class="f"><label for="sm-to">Кому</label>'
      '<input type="text" id="sm-to" maxlength="22" value="Родителям" '
      'placeholder="кому пишем"></div>'
      '<div class="f"><label for="sm-city">Куда уходит открытка</label>'
      f'<select id="sm-city">{opts}</select></div>'
      '<div class="f"><label for="sm-wish">Пожелание</label>'
      '<textarea id="sm-wish" maxlength="90" '
      'placeholder="пара строк, как на настоящей открытке">С Новым годом, пусть 2020 '
      'будет вашим годом</textarea>'
      '<div class="sm-cnt"><span>как на открытке, коротко</span>'
      '<span id="sm-cnt">0 / 90</span></div></div>'
      f'<button class="sm-btn sm-btn--f sm-send" type="submit" id="sm-send">'
      f'Опустить в ящик{ARROW}</button>'
      '</form>'
      '<div class="sm-log">'
      '<div class="sm-log__hd">Лог зоны · демонстрация принципа</div>'
      '<ul class="sm-log__lines" id="sm-log">'
      '<li class="is-in"><u>[t+0,00]</u> проектор: тестовая сетка на стене</li>'
      '<li class="is-in"><u>[t+0,00]</u> сервер: сцены загружены, 5 из 5</li>'
      '<li class="is-in"><u>[t+0,00]</u> датчик: ожидание открытки</li></ul>'
      '<div class="sm-box"><div class="sm-box__glass"><span class="sm-box__slot"></span>'
      '<span class="sm-card2"></span></div>'
      '<div class="sm-box__note"><b>Стеклянный ящик</b>датчик внутри, короб с проектором '
      'снизу, кабель до сервера в декорации</div></div>'
      '</div></div></div>'
      '<p class="sm-note">Тайминги в логе и пять заставок в этом блоке наши, для '
      'демонстрации порядка событий. В зоне работала та же логика: открытка в ящике, '
      'сигнал датчика, новая картинка на стене.</p>'
      '</div></div></div></section>')


def mesh():
    return (
      '<section class="sm-mesh"><div class="sm-w">'
      '<div class="sm-r" style="max-width:74ch"><span class="sm-kick">Живой блок</span>'
      '<h2>Сетка над сценой и автоматический сброс</h2></div>'
      '<div class="sm-mesh__grid">'
      '<div class="sm-r"><div class="sm-stage" id="sm-stage">'
      f'<img src="{IMG}/mesh.jpg" width="1600" height="1067" '
      'alt="Логотип Samsung на проекционной сетке над сценой, артисты работают за полотном" '
      'loading="lazy" decoding="async">'
      '<span class="sm-veil"><span class="sm-veil__tag">проекционная сетка</span></span>'
      '<span class="sm-stage__state" id="sm-stage-state">полотно в рабочем положении</span>'
      '</div>'
      '<div class="sm-mesh__ctrl">'
      '<button class="sm-btn sm-btn--f" type="button" id="sm-drop">Сбросить сетку</button>'
      '<span class="sm-mesh__log" id="sm-drop-log">картинка идёт по полотну перед '
      'артистами</span>'
      '</div></div>'
      '<div class="sm-r"><p>Проекционная сетка это полупрозрачное полотно на всю ширину '
      'портала. Пока на неё идёт картинка, графика висит в воздухе перед артистами, '
      'а самих артистов почти не видно. На фотографии так появился логотип: он не на '
      'экране позади сцены, а прямо перед номером.</p>'
      '<p>Система автоматического сброса снимает полотно по сигналу за секунды. Номер '
      'не приходится останавливать: графика заканчивается, сетка уходит вниз, сцена '
      'открывается целиком. Обратный подъём готовят между номерами.</p>'
      '<p class="sm-note">Сетка на кадре нарисована поверх фотографии: так видно, какую '
      'плоскость она закрывает и куда уходит при сбросе.</p></div>'
      '</div></div></section>')


def run():
    beats, thumbs = '', ''
    total = len(BEATS)
    for i, (f, chap, title, text, alt) in enumerate(BEATS, 1):
        eager = 'eager' if i == 1 else 'lazy'
        beats += (
          f'<figure class="sm-beat" data-i="{i}">'
          f'<div class="sm-beat__ph sm-zoom" role="button" tabindex="0" '
          f'data-src="{IMG}/{f}" data-cap="{H.escape(chap)}: {H.escape(title)}" '
          f'aria-label="Открыть кадр «{H.escape(title)}» на весь экран">'
          f'<span class="sm-beat__ch">{chap}</span>'
          f'<span class="sm-beat__no">{i:02d} / {total}</span>'
          f'<img src="{IMG}/{f}" width="1280" height="800" alt="{H.escape(alt)}" '
          f'loading="{eager}" decoding="async"></div>'
          f'<figcaption><h3>{H.escape(title)}</h3><p>{text}</p></figcaption></figure>')
        thumbs += (f'<button class="sm-thumb{" is-on" if i == 1 else ""}" data-go="{i}" '
                   f'type="button" aria-label="Шаг {i}: {H.escape(title)}">'
                   f'<img src="{IMG}/{f}" width="76" height="48" alt="" loading="lazy">'
                   f'</button>')
    return (
      '<section class="sm-run"><div class="sm-w">'
      '<div class="sm-run__hd"><div class="sm-r"><span class="sm-kick">Хронология</span>'
      '<h2>Вечер по шагам: от ферм до конфетти</h2></div>'
      '<p class="sm-run__hint sm-r">Первые четыре кадра сняты до гостей. Их видно '
      'в начале ролика вечера: зал, фермы, полотно и короб для проектора.</p></div></div>'
      f'<div class="sm-track" id="sm-track">{beats}</div>'
      '<div class="sm-w"><div class="sm-nav"><div style="display:flex;gap:10px">'
      f'<button class="sm-arrow sm-arrow--prev" id="sm-prev" type="button" '
      f'aria-label="Предыдущий шаг">{CHEV}</button>'
      f'<button class="sm-arrow sm-arrow--next" id="sm-next" type="button" '
      f'aria-label="Следующий шаг">{CHEV}</button></div>'
      f'<span class="sm-count" id="sm-count"><b>01</b> / {total}</span>'
      f'<div class="sm-thumbs" id="sm-thumbs">{thumbs}</div>'
      '</div></div></section>')


def video():
    return (
      '<section class="sm-video" id="sm-video"><div class="sm-w">'
      '<div class="sm-r" style="max-width:70ch"><span class="sm-kick">Видео</span>'
      '<h2>Вечер за две минуты</h2>'
      '<p class="sm-scene__lede">Ролик начинается с монтажа: фермы, подвес приборов, '
      'полотно над сценой. Дальше вечер целиком, от встречи гостей до финала '
      'с конфетти.</p></div>'
      '<div class="sm-video__box sm-r">'
      f'<video controls preload="none" poster="{IMG}/poster.jpg" '
      'playsinline aria-label="Ролик новогоднего вечера Samsung 2020">'
      f'<source src="{VIDEO}" type="video/mp4">'
      'Ваш браузер не воспроизводит видео.</video></div>'
      '<p class="sm-video__cap">Съёмка и монтаж ролика: Hand Marketing. '
      'Видео идёт с нашего сервера, без внешних плееров.</p>'
      '</div></section>')


def gallery():
    """Сетка на 38 кадров. Вертикальные кадры занимают две строки."""
    from PIL import Image
    cells = ''
    for i, alt in enumerate(GALLERY, 1):
        p = os.path.join(ROOT, 'images', 'samsung', f'g-{i:02d}.jpg')
        w, h = Image.open(p).size if os.path.exists(p) else (1600, 1067)
        cells += (
          f'<button class="sm-cell" type="button" data-i="{i}" '
          f'aria-label="Открыть фото {i} из {len(GALLERY)}">'
          f'<img src="{IMG}/t-{i:02d}.jpg" width="480" '
          f'height="{round(480 * h / w)}" alt="{H.escape(alt)}" loading="lazy" '
          f'decoding="async"></button>')
    return (
      '<section class="sm-gal"><div class="sm-w">'
      '<div class="sm-r" style="max-width:70ch"><span class="sm-kick">Галерея</span>'
      f'<h2>{len(GALLERY)} кадров вечера</h2>'
      '<p class="sm-scene__lede">Съёмка двух фотографов: встреча гостей, почта Деда '
      'Мороза, ужин под зимним лесом, сцена, конкурс и финал с конфетти.</p></div>'
      f'<div class="sm-grid sm-r" id="sm-grid">{cells}</div>'
      '</div></section>')


def result():
    items = [
      ('панорама', '<b>Панорамные проекционные декорации</b> зимнего леса, сказочных '
       'персонажей и главного новогоднего символа по всей дуге зала.'),
      ('сцена', '<b>Проекционные сетки с системой автоматического сброса</b> над сценой: '
       'графика перед артистами и мгновенный переход к открытой сцене.'),
      ('почта', '<b>Digital-почтовый ящик</b> для отправки поздравительных открыток '
       'в любую точку мира: датчик в стекле, УКФ-проектор в коробе, заставка в ответ '
       'на каждое письмо.'),
      ('вечер', '<b>Полное техническое сопровождение</b>: монтаж, юстировка, работа '
       'на площадке весь вечер и демонтаж после финала.'),
    ]
    lis = ''.join(f'<li><span class="sm-mono">{k}</span><span>{v}</span></li>'
                  for k, v in items)
    return (
      '<section class="sm-res"><div class="sm-w sm-res__grid">'
      '<div class="sm-r"><span class="sm-kick">Результат</span>'
      '<h2>Что получил клиент</h2>'
      '<p class="sm-res__more">Больше о направлениях: '
      '<a href="/event">организация мероприятий</a>, '
      '<a href="/3dmapping">3D mapping и проекционное шоу</a>.</p></div>'
      f'<ul class="sm-res__list sm-r">{lis}</ul>'
      '</div></section>')


LIGHTBOX = ('<div class="sm-lb" id="sm-lb" aria-hidden="true">'
            '<div class="sm-lb__box">'
            '<button class="sm-lb__x" id="sm-lb-x" type="button" aria-label="Закрыть">'
            '&times;</button>'
            f'<button class="sm-lb__nav sm-lb__nav--p" id="sm-lb-p" type="button" '
            f'aria-label="Предыдущее фото">{CHEV}</button>'
            f'<button class="sm-lb__nav sm-lb__nav--n" id="sm-lb-n" type="button" '
            f'aria-label="Следующее фото">{CHEV}</button>'
            '<img id="sm-lb-img" src="" alt="">'
            '<div class="sm-lb__cap" id="sm-lb-cap"></div>'
            '<div class="sm-lb__no sm-mono" id="sm-lb-no"></div></div></div>')

GAL_JS_DATA = ',\n  '.join(
  '{s:"%s/g-%02d.jpg",a:%s}' % (IMG, i, ('"' + a.replace('"', '') + '"'))
  for i, a in enumerate(GALLERY, 1))

PAGE_JS = """<script>(function(){
 var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;
 // ── снег в герое ──
 var cv=document.getElementById('sm-snow');
 if(cv&&!RM){
  // DPR режем до 1.5 и останавливаем цикл, когда герой ушёл из вида:
  // канвас на всю ширину экрана иначе греет процессор всю страницу
  var dpr=Math.min(devicePixelRatio||1,1.5),ctx=cv.getContext('2d'),fl=[],W=0,Hh=0,
      live=true,raf=0;
  function size(){var r=cv.parentNode.getBoundingClientRect();
   W=cv.width=r.width*dpr;Hh=cv.height=r.height*dpr;
   fl=[];var n=Math.min(130,Math.round(r.width/10));
   for(var i=0;i<n;i++)fl.push({x:Math.random()*W,y:Math.random()*Hh,
    r:(Math.random()*1.6+.5)*dpr,s:(Math.random()*.5+.18)*dpr,d:Math.random()*6.28});}
  function draw(){ctx.clearRect(0,0,W,Hh);
   for(var i=0;i<fl.length;i++){var f=fl[i];
    ctx.globalAlpha=.25+f.r/(3*dpr);ctx.beginPath();
    ctx.arc(f.x,f.y,f.r,0,6.29);ctx.fillStyle='#dceaff';ctx.fill();
    f.y+=f.s;f.x+=Math.sin(f.d+=0.008)*.25*dpr;
    if(f.y>Hh+4){f.y=-4;f.x=Math.random()*W;}}
   if(live)raf=requestAnimationFrame(draw);}
  size();draw();addEventListener('resize',size);
  if('IntersectionObserver' in window){
   new IntersectionObserver(function(es){
    var vis=es[0].isIntersecting;
    if(vis&&!live){live=true;draw();}
    else if(!vis&&live){live=false;cancelAnimationFrame(raf);}
   },{threshold:0}).observe(cv.parentNode);
  }
 }
 // ── взгляд гостя / техника ──
 var sw=document.getElementById('sm-switch'),shots=document.getElementById('sm-shots');
 if(sw&&shots){
  [].forEach.call(sw.querySelectorAll('button'),function(b){
   b.addEventListener('click',function(){
    [].forEach.call(sw.querySelectorAll('button'),function(x){
     var on=(x===b);x.classList.toggle('is-on',on);
     x.setAttribute('aria-pressed',on?'true':'false');});
    shots.classList.toggle('is-tech',b.getAttribute('data-mode')==='tech');});});
 }
 // ── расчёт дистанции проекции ──
 var wi=document.getElementById('sm-w');
 if(wi){
  var K={ukf:0.25,short:0.8,std:1.5},NM={ukf:'укф',short:'короткофокусный',std:'стандартный'},
      SC=56,WALL=56,CX=360,BOXD=0.9,FLOOR=318;
  function m(v){return v.toFixed(2).replace('.',',')+' м';}
  function set(id,a,v){var e=document.getElementById(id);if(e)e.setAttribute(a,v);}
  function upd(){
   var w=parseFloat(wi.value),L={},half=w*SC/2,maxL=w*K.std;
   document.getElementById('sm-w-out').textContent=m(w);
   for(var k in K)L[k]=w*K[k];
   // стена: ширина картинки и рамка короба
   set('sm-img','x1',CX-half);set('sm-img','x2',CX+half);
   document.getElementById('sm-img-lbl').textContent='картинка W = '+m(w);
   // три проектора: УКФ рисуем лучом, остальные пунктиром
   ['ukf','short','std'].forEach(function(k){
    var y=WALL+L[k]*SC,off=y>FLOOR-34;if(off)y=FLOOR-34;
    set('sm-box-'+k,'y',y);
    if(k==='ukf'){
     set('sm-lens-ukf','cy',y);
     set('sm-beam-p','points',CX+','+y+' '+(CX-half)+','+WALL+' '+(CX+half)+','+WALL);
    }else{
     set('sm-ray-'+k+'-a','y1',y);set('sm-ray-'+k+'-a','x2',CX-half);
     set('sm-ray-'+k+'-b','y1',y);set('sm-ray-'+k+'-b','x2',CX+half);
    }
    var t=document.getElementById('sm-lbl-'+k);
    if(t){t.setAttribute('y',y+(k==='ukf'?18:16));
     t.textContent=NM[k]+' '+m(L[k])+(off?', за кадром':'');}
    var row=document.getElementById('sm-row-'+k);
    document.getElementById('sm-val-'+k).textContent=m(L[k]);
    document.getElementById('sm-bar-'+k).style.width=(L[k]/maxL*100).toFixed(1)+'%';
    row.classList.toggle('is-fit',L[k]<=BOXD);
   });
   document.getElementById('sm-plan-tag').textContent='L = '+m(L.ukf);
   var fits=L.ukf<=BOXD;
   document.getElementById('sm-verdict').innerHTML=
    'Картинка шириной '+m(w)+' на стене. '+(fits
     ? 'Ультракороткий фокус ставит проектор в '+m(L.ukf)+' от поверхности, и он '+
       'прячется в короб глубиной около 0,9 м.'
     : 'Даже ультракороткому фокусу нужно '+m(L.ukf)+', а короб перед ящиком глубиной '+
       'около 0,9 м: картинку такой ширины в этой зоне уже не собрать.')+
    ' Короткофокусному нужно '+m(L.short)+', стандартному '+m(L.std)+
    ': такой проектор стоял бы среди гостей, и любой человек в луче закрывал бы картинку.';
  }
  wi.addEventListener('input',upd);upd();
 }
 // ── засветка зоны ──
 var lx=document.getElementById('sm-lux');
 if(lx){
  function lupd(){var v=+lx.value;
   document.getElementById('sm-lux-out').textContent=v+'%';
   document.getElementById('sm-haze').style.opacity=(v*0.0062).toFixed(3);
   var t,s;
   if(v<25){t='контраст в норме';s='Приглушённый свет: картинке хватает умеренной яркости, '+
    'чёрный на проекции остаётся чёрным.';}
   else if(v<62){t='нужен запас яркости';s='Рабочая ситуация вечера: свет в зоне есть, '+
    'поэтому берём проектор с запасом по яркости и держим в контенте плотный фон.';}
   else{t='картинка растворяется';s='Холл с окнами и включённым светом: без сильного '+
    'проектора проекция уходит в серое, и заставку не читает никто.';}
   document.getElementById('sm-lux-tag').textContent=t;
   document.getElementById('sm-lux-say').textContent=s;}
  lx.addEventListener('input',lupd);lupd();
 }
 // ── схема сигнала ──
 var ND={__NODES__};
 var say=document.getElementById('sm-say');
 if(say){
  [].forEach.call(document.querySelectorAll('.sm-map .nd'),function(g){
   function on(){var k=g.getAttribute('data-n'),d=ND[k];if(!d)return;
    [].forEach.call(document.querySelectorAll('.sm-map .nd'),function(x){
     x.classList.toggle('is-on',x===g);});
    say.innerHTML='<b>'+d.t+'</b><span>'+d.n+'</span>';}
   g.addEventListener('mouseenter',on);g.addEventListener('focus',on);
   g.addEventListener('click',on);
   g.addEventListener('keydown',function(e){
    if(e.key==='Enter'||e.key===' '){e.preventDefault();on();}});});
  var srv=document.getElementById('sm-nd-server');if(srv)srv.classList.add('is-on');
 }
 // ── почтовый ящик ──
 var form=document.getElementById('sm-form');
 if(form){
  var rig=document.getElementById('sm-rig'),log=document.getElementById('sm-log'),
      wish=document.getElementById('sm-wish'),cnt=document.getElementById('sm-cnt'),
      txt=document.getElementById('sm-wall-txt'),sub=document.getElementById('sm-wall-sub'),
      btn=document.getElementById('sm-send'),shot=0,tmrs=[];
  function count(){cnt.textContent=wish.value.length+' / 90';}
  wish.addEventListener('input',count);count();
  function line(t,cls,delay){
   var li=document.createElement('li');li.className=cls||'';li.innerHTML=t;
   log.appendChild(li);
   tmrs.push(setTimeout(function(){li.classList.add('is-in');},RM?0:delay));
  }
  form.addEventListener('submit',function(e){
   e.preventDefault();
   tmrs.forEach(clearTimeout);tmrs=[];
   var to=(document.getElementById('sm-to').value||'').trim()||'всем';
   var city=document.getElementById('sm-city').value;
   var w=(wish.value||'').trim()||'С Новым годом';
   shot=shot%5+1;
   log.innerHTML='';rig.classList.remove('is-drop','is-live');
   void rig.offsetWidth;rig.classList.add('is-drop');
   btn.disabled=true;
   line('<u>[t+0,00]</u> датчик: конверт в ящике',null,RM?0:340);
   line('<u>[t+0,12]</u> сервер: сигнал принят',null,RM?0:640);
   line('<u>[t+0,30]</u> сервер: заставка '+shot+' из 5',null,RM?0:940);
   line('<u>[t+0,45]</u> проектор: кадр на стене','ok',RM?0:1240);
   line('<u>[t+0,60]</u> '+city+': открытка в пути','in',RM?0:1540);
   tmrs.push(setTimeout(function(){
    for(var i=1;i<=5;i++)
     document.getElementById('sm-bg-'+i).classList.toggle('is-on',i===shot);
    txt.textContent=w;
    sub.textContent=to+' · '+city+' · заставка '+shot+' из 5';
    rig.classList.add('is-live');btn.disabled=false;
   },RM?0:1000));
  });
 }
 // ── сброс сетки ──
 var drop=document.getElementById('sm-drop');
 if(drop){
  var stage=document.getElementById('sm-stage'),st=document.getElementById('sm-stage-state'),
      dlog=document.getElementById('sm-drop-log'),down=false;
  drop.addEventListener('click',function(){
   down=!down;stage.classList.toggle('is-down',down);
   drop.textContent=down?'Поднять сетку':'Сбросить сетку';
   st.textContent=down?'полотно сброшено':'полотно в рабочем положении';
   dlog.textContent=down?'сброс по сигналу: дальше номер идёт на открытой сцене'
    :'картинка идёт по полотну перед артистами';});
 }
 // ── листалка шагов ──
 var track=document.getElementById('sm-track');
 if(track){
  var beats=[].slice.call(track.querySelectorAll('.sm-beat')),
      thumbs=[].slice.call(document.querySelectorAll('.sm-thumb')),
      prev=document.getElementById('sm-prev'),next=document.getElementById('sm-next'),
      count2=document.getElementById('sm-count'),cur=1,total=beats.length;
  function pad(n){return n<10?'0'+n:''+n;}
  function mark(i){cur=i;count2.innerHTML='<b>'+pad(i)+'</b> / '+total;
   thumbs.forEach(function(t,k){t.classList.toggle('is-on',k===i-1);});
   prev.disabled=(i===1);next.disabled=(i===total);
   var t=thumbs[i-1];
   if(t&&t.parentNode.scrollWidth>t.parentNode.clientWidth){
    var box=t.parentNode;box.scrollTo({left:t.offsetLeft-(box.clientWidth-t.offsetWidth)/2,
     behavior:RM?'auto':'smooth'});}}
  function go(i){i=Math.min(total,Math.max(1,i));
   var b=beats[i-1];
   track.scrollTo({left:b.offsetLeft-(track.clientWidth-b.offsetWidth)/2,
    behavior:RM?'auto':'smooth'});mark(i);}
  prev.addEventListener('click',function(){go(cur-1);});
  next.addEventListener('click',function(){go(cur+1);});
  thumbs.forEach(function(t){t.addEventListener('click',function(){
   go(+t.getAttribute('data-go'));});});
  var tmr;
  track.addEventListener('scroll',function(){clearTimeout(tmr);tmr=setTimeout(function(){
   var mid=track.scrollLeft+track.clientWidth/2,best=1,d=1e9;
   beats.forEach(function(s,k){var c=s.offsetLeft-track.offsetLeft+s.offsetWidth/2,
    dd=Math.abs(c-mid);if(dd<d){d=dd;best=k+1;}});
   if(best!==cur)mark(best);},90);});
  mark(1);
 }
 // ── лайтбокс ──
 var G=[
  __GAL__
 ];
 var lb=document.getElementById('sm-lb'),lbi=document.getElementById('sm-lb-img'),
     lbc=document.getElementById('sm-lb-cap'),lbn=document.getElementById('sm-lb-no'),
     lbx=document.getElementById('sm-lb-x'),lbp=document.getElementById('sm-lb-p'),
     lbnx=document.getElementById('sm-lb-n'),idx=0,inGal=false;
 function show(i){idx=(i+G.length)%G.length;var g=G[idx];
  lbi.src=g.s;lbi.alt=g.a;lbc.textContent=g.a;
  lbn.textContent=(idx+1)+' / '+G.length;}
 function open(src,cap,alt,gal){inGal=!!gal;
  lbp.style.display=lbnx.style.display=gal?'inline-flex':'none';
  if(!gal){lbi.src=src;lbi.alt=alt||'';lbc.textContent=cap||'';lbn.textContent='';}
  lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';lbx.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  lbi.removeAttribute('src');document.body.style.overflow='';}
 [].forEach.call(document.querySelectorAll('.sm-cell'),function(c){
  c.addEventListener('click',function(){show(+c.getAttribute('data-i')-1);
   open(null,null,null,true);});});
 [].forEach.call(document.querySelectorAll('.sm-zoom'),function(z){
  function fire(){var im=z.querySelector('img');
   open(z.getAttribute('data-src'),z.getAttribute('data-cap'),im?im.alt:'',false);}
  z.addEventListener('click',fire);
  z.addEventListener('keydown',function(e){
   if(e.key==='Enter'||e.key===' '){e.preventDefault();fire();}});});
 lbp.addEventListener('click',function(){show(idx-1);});
 lbnx.addEventListener('click',function(){show(idx+1);});
 lbx.addEventListener('click',close);
 lb.addEventListener('click',function(e){if(e.target===lb)close();});
 document.addEventListener('keydown',function(e){
  if(!lb.classList.contains('is-open'))return;
  if(e.key==='Escape')close();
  if(inGal&&e.key==='ArrowRight')show(idx+1);
  if(inGal&&e.key==='ArrowLeft')show(idx-1);});
 // ── reveal ──
 var els=[].slice.call(document.querySelectorAll('.sm-r'));
 function inview(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inview);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inview(e.target);io.unobserve(e.target);}});},
  {rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inview(n);else io.observe(n);});
})();</script>"""

NODES_JS = ',\n  '.join(
  '%s:{t:"%s",n:"%s"}' % (c, n.replace('"', ''), t.replace('"', ''))
  for c, n, t in NODES)
PAGE_JS = PAGE_JS.replace('__NODES__', NODES_JS).replace('__GAL__', GAL_JS_DATA)

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org",'
  '"@type":"BreadcrumbList","itemListElement":['
  '{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Event","item":"https://hand-marketing.ru/event/"},'
  '{"@type":"ListItem","position":3,"name":"Новый год Samsung 2020",'
  f'"item":"{URL}"}}]}}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Новый год Samsung 2020: панорамные проекции, сетка с автосбросом и digital-ящик Деда Мороза | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: новогодний корпоратив Samsung. Панорамные проекционные декорации зимнего леса, проекционные сетки с автоматическим сбросом над сценой и digital-почтовый ящик Деда Мороза с датчиком и УКФ-проектором. Контент, оборудование, монтаж и полное техническое сопровождение вечера.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Новый год Samsung 2020 | кейс Hand Marketing">
<meta property="og:description" content="Зимний лес по дуге зала, логотип на проекционной сетке и почтовый ящик Деда Мороза, который отвечал заставкой на каждую открытку.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/hero.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/geologica-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def build():
    # Отдельного CTA-блока нет: фиолетовая форма из rc.footer() закрывает страницу
    body = (f'{rc.header()}<main class="sm">{hero()}{brief()}{scenes()}'
            f'<div class="sm-sheet">{two()}{throwcalc()}</div>'
            f'{flow()}{mail()}{mesh()}{run()}{video()}{gallery()}{result()}</main>'
            f'{LIGHTBOX}<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}'
            '</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'event', 'samsung')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('удалён', a2, '(деплой переименовал бы его в index.html)')
    print('written', os.path.join(out, 'index.html'))
