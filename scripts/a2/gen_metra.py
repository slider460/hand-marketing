#!/usr/bin/env python3
"""Генерит mirror/creative/metra/index.html — кейс «Брендбук Metra Technology Group».

Дизайн-концепция: брендбук описывает не один бренд, а архитектуру из пяти
(головной Metra Technology Group плюс НПП Метра, МетраPRO, MetraRobotics и
МетраПолис). Все пять построены на одном знаке и одной модульной сетке, поэтому
страница не показывает пять наборов скриншотов, а даёт систему вживую:

  • переключатель брендов перекрашивает секцию целиком: логотип, цвет, стена
    паттерна, слоган, миссия, палитра;
  • паттерны рисуются скриптом на той самой сетке из гайдлайна, её видно по
    тумблеру, масштаб двигается ползунком (гайдлайн прямо говорит: паттерн
    безграничен и масштабируется);
  • палитра отдаёт HEX в буфер по клику, рядом лежат CMYK из брендбука;
  • фотостиль показан правилом, а не картинкой: чёрный слой 70% и маска-сота
    накладываются на живой кадр;
  • «недопустимо» собрано из того же инлайнового знака искажениями через CSS.

Логотипы и знаки — настоящие кривые из PDF (scripts/metra-assets.py), поэтому
коммерческий Gotham Pro на странице не нужен: заголовки набраны Montserrat,
текст Onest (self-host, см. mirror/fonts/).

Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import json
import os
import re
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/metra'
URL = 'https://hand-marketing.ru/creative/metra/'
MAN = json.load(open(os.path.join(ROOT, 'images', 'metra', 'manifest.json'), encoding='utf-8'))

ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
CHEV = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2"/></svg>'


def svg(name):
    """Логотип инлайном: только так CSS красит его в выворотку и по бренду."""
    return open(os.path.join(ROOT, 'images', 'metra', name + '.svg'), encoding='utf-8').read()


def fkey(k):
    """Ключ бренда → префикс файлов кропов (у MetraRobotics он короче)."""
    return 'robo' if k == 'robotics' else k


# ─── бренды экосистемы ──────────────────────────────────────────────────────
# key, имя, дескриптор, цвета (основной, светлый, тёмный), слоган, миссия,
# характер паттерна, ценности
BRANDS = [
    dict(k='mtg', name='Metra Technology Group', short='Metra Technology Group',
         desc='Головной бренд, индустриальная экосистема',
         b='#005F7C', b2='#2188A0', b3='#87C7D7', ink='#00323F',
         slogan='Импульс к технологическому превосходству',
         about='Экосистема выросла из научно-производственного предприятия «Метра», '
               'основанного инженерами в 1991 году. Головной бренд собирает под собой четыре '
               'компании и отвечает за общий голос группы.',
         mission='Создавать импульс к технологическому превосходству российской промышленности, '
                 'открывая новые возможности для роста и развития.',
         pat='Изометрические кубы',
         patnote='Куб собирается из ромба и двух граней. Стена растёт как город: '
                 'это про масштаб группы и про то, что модули складываются друг с другом.',
         values=[('Инновации во благо', 'Технологии для людей, а не только для машин'),
                 ('Надёжность и безопасность', 'Самые строгие стандарты качества'),
                 ('Открытость к изменениям', 'Нет ничего, что нельзя улучшить'),
                 ('Социальная ответственность', 'Часть прибыли идёт в социальные проекты')]),
    dict(k='metra', name='НПП Метра', short='Метра',
         desc='Весоизмерительная техника',
         b='#1C3F7E', b2='#5381BC', b3='#8FB0DC', ink='#12294F',
         slogan='Успех точно можно измерить',
         about='Один из первых заводов страны, наладивших серийный выпуск весовой техники для '
               'промышленности. В штате 150 человек, дилерская сеть работает в России, Беларуси, '
               'Казахстане и Армении.',
         mission='Создание систем точного весового учёта и комплексной автоматизации '
                 'взвешивания для прозрачного управления бизнесом.',
         pat='Шевроны из знака',
         patnote='Буква M вынута из знака и поставлена в ряд, как шкала. Ромбы с шевроном '
                 'внутри повторяют сам знак, повёрнутый на сорок пять градусов.',
         values=[('Честность и надёжность', 'В материалоёмких отраслях каждый грамм имеет значение'),
                 ('Стремление к совершенству', 'Свой отдел исследований и разработок'),
                 ('Нацеленность на результат', 'Внимание к деталям и успех клиента')]),
    dict(k='pro', name='МетраPRO', short='МетраPRO',
         desc='Экспертный центр металлообработки',
         b='#E44F36', b2='#ED977B', b3='#F6C9BC', ink='#5A1E21',
         slogan='Стальные решения в железные сроки',
         about='Центр металлообработки вырос из запроса клиентов: подрядчика с широким парком '
               'оборудования найти было негде. Сейчас это контрактное производство для '
               'строительства, сельского хозяйства, транспорта и логистики.',
         mission='Сформировать гибкую производственную среду для раскрытия промышленного '
                 'потенциала российских предприятий.',
         pat='Ступени',
         patnote='Квадраты идут лестницей вверх и вправо: линия толще, чем у остальных, '
                 'потому что речь про металл и про рост объёмов.',
         values=[('Высокие стандарты качества', 'Система менеджмента качества по ISO 9001'),
                 ('Гибкость и кооперация', 'Нестандартное решение под конкретную задачу'),
                 ('Прозрачность', 'Заказчик погружён в процесс, недосказанностей нет')]),
    dict(k='robotics', name='MetraRobotics', short='MetraRobotics',
         desc='Многопрофильный центр промышленной роботизации',
         b='#6F2381', b2='#9460A4', b3='#C4A6CD', ink='#362B59',
         slogan='Окно в мир индустриальной роботизации',
         about='Инжиниринговый центр с собственной производственной базой: от технологического '
               'аудита до запуска роботизированных комплексов под ключ. С 2017 года ведёт '
               'образовательные курсы по роботизации производств.',
         mission='Повышение производительности, безопасности и конкурентоспособности '
                 'предприятий за счёт осознанной роботизации.',
         pat='Зигзаг',
         patnote='Диагональные линии сходятся и расходятся, как траектория манипулятора. '
                 'Единственный паттерн группы, который построен не на прямых углах.',
         values=[('Лидерство и проактивность', 'Задаём тренды и разрабатываем решения'),
                 ('Эмпатия и осознанность', 'На первом месте люди, роботы усиливают их'),
                 ('Ответственность', 'Продукт становится частью экосистемы заказчика')]),
    dict(k='polis', name='МетраПолис', short='МетраПолис',
         desc='Первый индустриальный хаб в Обнинске',
         b='#57A332', b2='#7FBF5E', b3='#B4DBA0', ink='#3E752F',
         slogan='Пространство синергии людей и технологий',
         about='Площадка для производителей оборудования, автоматизаторов, инжиниринга, '
               'промышленного дизайна, IT и патентования в первом наукограде страны.',
         mission='Создание объединяющей среды компетентного сообщества '
                 'производственно-технических компаний для технологического развития.',
         pat='Столбики города',
         patnote='Вертикальные скобы разной высоты: кварталы хаба. Серые чередуются с '
                 'фирменными, поэтому паттерн работает и на белом бланке, и на пакете.',
         values=[('Кооперация', 'Каждый вносит вклад в развитие промышленности'),
                 ('Мотивация', 'Поддержка тех, кто хочет менять индустрию'),
                 ('Смелость', 'Площадка для экспериментов и новых решений')]),
]
BY = {b['k']: b for b in BRANDS}

# ─── носители: (заголовок, пояснение, [(файл, alt-хвост, бренд)]) ───────────
MEDIA = [
    ('Деловая документация',
     'Бланк договора и папка. Паттерн уходит в подвал листа и не спорит с текстом, '
     'логотип головного бренда всегда стоит рядом с логотипом компании.',
     [('mtg-docs', 'Metra Technology Group', 'mtg'), ('metra-docs', 'НПП Метра', 'metra'),
      ('pro-docs', 'МетраPRO', 'pro'), ('robo-docs', 'MetraRobotics', 'robotics'),
      ('polis-docs', 'МетраПолис', 'polis')]),
    ('Визитки и бейджи',
     'Оборот визитки закрывает фирменный цвет с паттерном, лицевая сторона белая. '
     'Вторая визитка в комплекте всегда групповая: имя экосистемы и QR.',
     [('mtg-cards', 'Metra Technology Group', 'mtg'), ('metra-cards', 'НПП Метра', 'metra'),
      ('pro-cards', 'МетраPRO', 'pro'), ('robo-cards', 'MetraRobotics', 'robotics'),
      ('polis-cards', 'МетраПолис', 'polis')]),
    ('Наружная реклама',
     'Сити-формат собирается из трёх элементов: логотип сверху, слоган крупно, продукт '
     'в фирменной соте. Дальше меняется только цвет и продукт.',
     [('mtg-city', 'Metra Technology Group', 'mtg'), ('metra-city', 'НПП Метра', 'metra'),
      ('pro-city', 'МетраPRO', 'pro'), ('robo-city', 'MetraRobotics', 'robotics'),
      ('polis-city', 'МетраПолис', 'polis')]),
    ('Сайты и экраны',
     'Шаблон один на всю группу: тёмный блок экосистемы слева, цветной блок компании справа. '
     'Переход между сайтами читается как переход между разделами одного продукта.',
     [('mtg-web', 'Metra Technology Group', 'mtg'), ('metra-web', 'НПП Метра', 'metra'),
      ('pro-web', 'МетраPRO', 'pro'), ('robo-web', 'MetraRobotics', 'robotics'),
      ('polis-web', 'МетраПолис', 'polis')]),
    ('Сувенирная продукция',
     'Пакет, флешка, бутылка, кружка. Паттерн садится на нижнюю треть предмета, знак сверху: '
     'подрядчику уходит готовая схема, а не отдельный макет на каждую позицию.',
     [('mtg-gifts', 'Metra Technology Group', 'mtg'), ('metra-gifts', 'НПП Метра', 'metra'),
      ('pro-gifts', 'МетраPRO', 'pro'), ('robo-gifts', 'MetraRobotics', 'robotics'),
      ('polis-gifts', 'МетраПолис', 'polis')]),
    ('Презентации',
     'Три раскладки слайда: текстовая, с тезисами на цветном блоке и с картинкой в соте. '
     'Внутри группы отличается только цвет заливки.',
     [('mtg-present', 'Metra Technology Group', 'mtg'), ('metra-present', 'НПП Метра', 'metra'),
      ('pro-present', 'МетраPRO', 'pro'), ('robo-present', 'MetraRobotics', 'robotics'),
      ('polis-present', 'МетраПолис', 'polis')]),
]

# ─── одиночные носители головного бренда ────────────────────────────────────
SOLO = [
    ('mtg-transport', 'Транспорт',
     'Борт машины держит три слова слогана и паттерн по низу кузова. Логотип не растягивается '
     'по всей длине, поэтому фургон читается и в потоке.'),
    ('mtg-cobrand', 'Co-branding и стенды',
     'Правило соседства: макет остаётся в своей палитре, пропорции логотипов не меняются. '
     'На выставке это позволяет ставить рядом два бренда группы без пересогласований.'),
    ('mtg-social', 'Социальные сети',
     'Сетка постов и сторис на трёх фонах: сплошной цвет, белый с контурным паттерном и '
     'фотография в соте.'),
    ('mtg-cloth', 'Одежда',
     'Лонгслив с паттерном по низу: тот же модуль, что и на бланке, только крупнее.'),
]

# ─── недопустимо: (подпись, класс искажения) ────────────────────────────────
DONT = [
    ('Перекрашивать в цвета, которых нет в брендбуке', 'recolor'),
    ('Менять расстояния между элементами', 'space'),
    ('Масштабировать непропорционально', 'squash'),
    ('Ставить тёмный логотип на пёстрый фон', 'noise'),
    ('Располагать под углом', 'tilt'),
    ('Масштабировать отдельные элементы', 'part'),
]

SPEC = [('5', 'брендов в экосистеме'), ('69', 'полос гайдлайна'),
        ('5', 'паттернов на одной сетке'), ('10', 'групп носителей')]


# ─── CSS ────────────────────────────────────────────────────────────────────
PAGE_CSS = """<style id="mt-css">
.mt{--ink:#14181a;--mut:#5d6a70;--ln:#e3e8ea;--b:#005F7C;--b2:#2188A0;--b3:#87C7D7;--dk:#00323F;
 font-family:'Onest','Montserrat',system-ui,sans-serif;color:var(--ink);background:#fff;
 -webkit-font-smoothing:antialiased;overflow-x:clip}
.mt *{box-sizing:border-box}
.mt-task__grid>*,.mt-mark__grid>*,.mt-br__grid>*,.mt-photo__grid>*,.mt-res__grid>*,.mt-band__h>*,.mt-row>*,.mt-tiles>*,.mt-solo>*{min-width:0}
.mt h1,.mt h2,.mt h3,.mt .mt-num,.mt .mt-kick,.mt .mt-btn{font-family:'Montserrat',sans-serif}
.mt p{margin:0 0 14px}
.mt-w{max-width:1240px;margin:0 auto;padding:0 28px}
.mt-kick{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.18em;
 text-transform:uppercase;color:var(--b);margin:0 0 18px}
.mt h2{font-size:clamp(28px,3.6vw,46px);line-height:1.06;letter-spacing:-.02em;font-weight:800;margin:0 0 18px}
.mt h3{font-size:19px;line-height:1.25;font-weight:700;margin:0 0 10px}
.mt-lead{font-size:clamp(16px,1.5vw,19px);line-height:1.6;color:var(--mut);max-width:64ch}
.mt-r{opacity:0;transform:translateY(18px);transition:opacity .7s ease,transform .7s ease}
.mt-r.is-in{opacity:1;transform:none}
.mt-btn{display:inline-flex;align-items:center;gap:9px;padding:14px 24px;border-radius:2px;
 font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;
 border:1px solid transparent;cursor:pointer;transition:.2s}
.mt-btn svg{width:17px;height:17px}
.mt-btn--p{background:#fff;color:var(--dk)}
.mt-btn--p:hover{background:var(--b3)}
.mt-btn--gh{border-color:rgba(255,255,255,.45);color:#fff}
.mt-btn--gh:hover{border-color:#fff;background:rgba(255,255,255,.1)}
.mt-logo svg{display:block;width:100%;height:auto}
.mt-logo--w path{fill:#fff}

/* ── герой ─────────────────────────────────────────────────────────────── */
.mt-hero{position:relative;background:#005F7C;color:#fff;overflow:hidden;padding:120px 0 0}
.mt-hero__pat{position:absolute;inset:0;opacity:.17;pointer-events:none;-webkit-mask-image:linear-gradient(115deg,transparent 22%,#000 72%);mask-image:linear-gradient(115deg,transparent 22%,#000 72%)}
.mt-hero__pat svg{width:100%;height:100%;display:block}
.mt-hero__in{position:relative;padding-bottom:66px}
.mt-hero__logo{width:min(320px,60vw);margin:0 0 46px}
.mt-hero h1{font-size:clamp(34px,6vw,74px);line-height:1.02;letter-spacing:-.03em;font-weight:800;
 margin:0 0 22px;max-width:16ch}
.mt-hero__sub{font-size:clamp(16px,1.6vw,20px);line-height:1.6;color:rgba(255,255,255,.82);max-width:60ch}
.mt-hero__rule{display:flex;flex-wrap:wrap;gap:8px 26px;padding:0 0 18px;margin:0 0 34px;
 border-bottom:1px solid rgba(255,255,255,.24);font-size:12px;letter-spacing:.12em;
 text-transform:uppercase;color:rgba(255,255,255,.7)}
.mt-hero__cta{display:flex;flex-wrap:wrap;gap:12px;margin:30px 0 0}
.mt-spec{position:relative;border-top:1px solid rgba(255,255,255,.24);background:rgba(0,0,0,.14)}
.mt-spec__in{max-width:1240px;margin:0 auto;padding:0 28px;display:grid;
 grid-template-columns:repeat(4,1fr)}
.mt-spec div{padding:26px 0}
.mt-spec div+div{border-left:1px solid rgba(255,255,255,.16);padding-left:26px}
.mt-num{display:block;font-size:clamp(30px,3.4vw,46px);font-weight:800;line-height:1;letter-spacing:-.02em}
.mt-spec dd,.mt-spec dt{margin:0}
.mt-spec dt{font-size:13px;color:rgba(255,255,255,.72);margin-top:8px}

/* ── задача ────────────────────────────────────────────────────────────── */
.mt-task{padding:96px 0}
.mt-task__grid{display:grid;grid-template-columns:1.25fr .9fr;gap:56px}
.mt-task__side{border-left:2px solid var(--b);padding-left:28px}
.mt-task__side p{font-size:15px;line-height:1.6;color:var(--mut)}
.mt-task__side b{color:var(--ink)}

/* ── архитектура ───────────────────────────────────────────────────────── */
.mt-arch{padding:0 0 96px}
.mt-arch__top{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:34px 0 0}
.mt-arch__head{border:1px solid var(--ln);border-top:4px solid #005F7C;padding:26px;margin:0 0 14px;
 display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}
.mt-arch__head .mt-logo{width:230px}
.mt-arch__head p{margin:0;font-size:14px;color:var(--mut);max-width:52ch}
.mt-card{display:block;width:100%;text-align:left;background:#fff;border:1px solid var(--ln);
 border-top:4px solid var(--c);padding:22px 20px 24px;cursor:pointer;transition:.25s;font:inherit}
.mt-card:hover{transform:translateY(-4px);box-shadow:0 14px 34px rgba(20,24,26,.1)}
.mt-card__m{width:34px;margin:0 0 16px}
.mt-card b{display:block;font-family:'Montserrat',sans-serif;font-size:16px;font-weight:700;margin:0 0 6px}
.mt-card span{display:block;font-size:13px;line-height:1.45;color:var(--mut)}

/* ── знак ──────────────────────────────────────────────────────────────── */
.mt-mark{background:#f5f7f8;padding:96px 0}
.mt-mark__grid{display:grid;grid-template-columns:.95fr 1.05fr;gap:56px;align-items:center}
.mt-mark__stage{position:relative;background:#fff;border:1px solid var(--ln);aspect-ratio:1;
 display:grid;place-items:center}
.mt-mark__stage .mt-logo{width:44.44%}
.mt-mark__stage .mt-logo path{fill:#005F7C}
.mt-mark__grid2{position:absolute;inset:0;opacity:0;transition:opacity .3s}
.mt-mark__stage.is-grid .mt-mark__grid2{opacity:1}
.mt-mark__grid2 svg{width:100%;height:100%;display:block}
.mt-lock{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--ln);
 border:1px solid var(--ln);margin:26px 0 0}
.mt-lock div{background:#fff;padding:22px 20px;display:flex;align-items:center;min-height:96px}
.mt-lock .mt-logo{width:min(190px,80%)}
.mt-lock div:first-child{grid-column:1/-1}
.mt-lock div:first-child .mt-logo{width:min(250px,72%)}
.mt-tog{display:inline-flex;align-items:center;gap:10px;margin:22px 0 0;font-size:13px;
 font-weight:600;color:var(--mut);cursor:pointer;background:none;border:0;font-family:inherit}
.mt-tog i{width:38px;height:21px;border-radius:11px;background:#cfd8db;position:relative;transition:.2s}
.mt-tog i:after{content:"";position:absolute;top:3px;left:3px;width:15px;height:15px;border-radius:50%;
 background:#fff;transition:.2s}
.mt-tog[aria-pressed="true"] i{background:var(--b)}
.mt-tog[aria-pressed="true"] i:after{transform:translateX(17px)}

/* ── переключатель брендов ─────────────────────────────────────────────── */
.mt-br{position:relative;background:var(--b);color:#fff;transition:background .5s ease}
.mt-br__pat{position:absolute;inset:0;opacity:.2;pointer-events:none;-webkit-mask-image:linear-gradient(#0000 4%,#000 42%);mask-image:linear-gradient(#0000 4%,#000 42%)}
.mt-br__pat svg{width:100%;height:100%;display:block}
.mt-br__in{position:relative;padding-top:88px;padding-bottom:96px}
.mt-br__tabs{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0 44px}
.mt-br__tabs button{font:inherit;font-family:'Montserrat',sans-serif;font-size:12px;font-weight:700;
 letter-spacing:.08em;text-transform:uppercase;padding:12px 18px;border:1px solid rgba(255,255,255,.4);
 background:none;color:#fff;cursor:pointer;transition:.2s}
.mt-br__tabs button:hover{background:rgba(255,255,255,.12)}
.mt-br__tabs button[aria-selected="true"]{background:#fff;color:var(--b);border-color:#fff}
.mt-br__grid{display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:start}
.mt-br__logo{width:min(360px,78%);margin:0 0 30px}
.mt-br__slog{font-family:'Montserrat',sans-serif;font-size:clamp(24px,2.9vw,38px);font-weight:800;
 line-height:1.1;letter-spacing:-.02em;margin:0 0 20px}
.mt-br__desc{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.72);
 margin:0 0 22px}
.mt-br__about{font-size:16px;line-height:1.65;color:rgba(255,255,255,.88);max-width:52ch}
.mt-br__mis{border-left:2px solid rgba(255,255,255,.5);padding:2px 0 2px 20px;margin:24px 0 0;
 font-size:15px;line-height:1.6;color:rgba(255,255,255,.92)}
.mt-br__mis b{display:block;font-size:11px;letter-spacing:.16em;text-transform:uppercase;
 color:rgba(255,255,255,.6);margin:0 0 8px;font-family:'Montserrat',sans-serif}
.mt-vals{list-style:none;margin:26px 0 0;padding:0;display:grid;gap:12px}
.mt-vals li{display:grid;grid-template-columns:26px 1fr;gap:12px;font-size:14px;line-height:1.5;
 color:rgba(255,255,255,.86)}
.mt-vals i{font-style:normal;font-family:'Montserrat',sans-serif;font-weight:800;font-size:12px;
 color:rgba(255,255,255,.55);padding-top:2px}
.mt-vals b{color:#fff}
.mt-side{background:rgba(0,0,0,.16);border:1px solid rgba(255,255,255,.2);padding:26px}
.mt-side h3{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.66);
 font-weight:700;margin:0 0 16px}
.mt-side+.mt-side{margin-top:14px}
.mt-sw{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:8px}
.mt-sw button{font:inherit;border:0;padding:0;cursor:pointer;background:none;text-align:left;
 position:relative}
.mt-sw span{display:block;height:56px;border:1px solid rgba(255,255,255,.35)}
.mt-sw em{display:block;font-style:normal;font-family:'Montserrat',sans-serif;font-size:11px;
 font-weight:700;letter-spacing:.04em;margin:8px 0 2px}
.mt-sw small{display:block;font-size:10px;letter-spacing:.06em;color:rgba(255,255,255,.6)}
.mt-sw button:after{content:"скопировано";position:absolute;left:0;top:18px;font-size:10px;
 letter-spacing:.08em;text-transform:uppercase;background:#fff;color:#14181a;padding:3px 7px;
 opacity:0;transition:.2s;pointer-events:none}
.mt-sw button.is-copied:after{opacity:1}
.mt-shot{border:1px solid rgba(255,255,255,.2);background:rgba(0,0,0,.16);margin:14px 0 0}
.mt-shot img{display:block;width:100%;height:auto}
.mt-shot figcaption{padding:12px 16px;font-size:12px;color:rgba(255,255,255,.7)}

/* ── лаборатория паттернов ─────────────────────────────────────────────── */
.mt-lab{padding:96px 0}
.mt-lab__head{display:flex;justify-content:space-between;align-items:flex-end;gap:34px;flex-wrap:wrap}
.mt-lab__ctl{display:flex;align-items:center;gap:30px;flex-wrap:wrap}
/* оба управления живут в одной строке-сетке: одинаковая высота ячейки,
   одинаковая подпись и один порядок «подпись, потом элемент» */
.mt-lab__ctl>*{display:flex;align-items:center;gap:12px;height:34px;margin:0;
 font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.mt-lab__ctl .mt-tog{flex-direction:row-reverse}
.mt-lab__ctl input[type=range]{width:150px;accent-color:var(--b);margin:0}
.mt-tiles{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:34px 0 0}
.mt-tile{border:1px solid var(--ln);background:#fff}
.mt-tile__box{position:relative;aspect-ratio:1;overflow:hidden;color:var(--c)}
.mt-tile__box svg{position:absolute;inset:0;width:100%;height:100%}
.mt-tile__cap{border-top:1px solid var(--ln);padding:14px 16px 18px}
.mt-tile__cap b{display:block;font-family:'Montserrat',sans-serif;font-size:13px;font-weight:700;
 color:var(--c);margin:0 0 6px}
.mt-tile__cap span{display:block;font-size:12px;line-height:1.45;color:var(--mut)}
.mt-lab__note{margin:26px 0 0;font-size:14px;color:var(--mut);max-width:70ch}

/* ── фотостиль ─────────────────────────────────────────────────────────── */
.mt-photo{background:#14181a;color:#fff;padding:96px 0}
.mt-photo .mt-kick{color:var(--b3)}
.mt-photo__grid{display:grid;grid-template-columns:1fr 1.15fr;gap:56px;align-items:center}
.mt-photo p{color:rgba(255,255,255,.74)}
.mt-photo__stage{position:relative;aspect-ratio:4/3;background:#000}
.mt-photo__stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 transition:filter .35s ease}
.mt-photo__stage:before{content:"";position:absolute;inset:0;background:#000;opacity:0;
 transition:opacity .35s ease;z-index:1;pointer-events:none}
.mt-photo__stage.is-dark:before{opacity:.7;mix-blend-mode:darken}
.mt-photo__stage.is-hex img{clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
.mt-photo__hex{position:absolute;inset:0;opacity:0;transition:opacity .35s ease;z-index:2;
 pointer-events:none}
.mt-photo__stage.is-hex .mt-photo__hex{opacity:1}
.mt-photo__hex svg{width:100%;height:100%;display:block}
.mt-photo__ctl{display:flex;gap:22px;flex-wrap:wrap;margin:26px 0 0}
.mt-photo .mt-tog{color:rgba(255,255,255,.7)}
.mt-photo .mt-tog i{background:rgba(255,255,255,.25)}
.mt-photo .mt-tog[aria-pressed="true"] i{background:var(--b3)}

/* ── носители ──────────────────────────────────────────────────────────── */
.mt-media{padding:96px 0}
.mt-band{margin:56px 0 0}
.mt-band__h{display:grid;grid-template-columns:.8fr 1.2fr;gap:34px;align-items:baseline;
 border-top:1px solid var(--ln);padding:22px 0 0}
.mt-band__h p{font-size:14px;line-height:1.6;color:var(--mut);margin:0}
.mt-row{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:24px 0 0;align-items:start}
.mt-fig{margin:0;border:1px solid var(--ln);border-bottom:3px solid var(--c);background:#fff}
.mt-fig img{display:block;width:100%;height:auto}
.mt-fig figcaption{padding:10px 12px;font-size:11px;letter-spacing:.04em;color:var(--mut)}
.mt-solo{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin:56px 0 0}
.mt-solo figure{margin:0;border:1px solid var(--ln)}
.mt-solo img{display:block;width:100%;height:auto}
.mt-solo figcaption{padding:18px 20px 22px}
.mt-solo b{display:block;font-family:'Montserrat',sans-serif;font-size:15px;margin:0 0 6px}
.mt-solo span{display:block;font-size:13px;line-height:1.55;color:var(--mut)}

/* ── недопустимо ───────────────────────────────────────────────────────── */
.mt-dont{background:#f5f7f8;padding:96px 0}
.mt-dont__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:34px 0 0}
.mt-dont figure{margin:0;background:#fff;border:1px solid var(--ln);padding:26px 22px 20px}
.mt-dont__box{position:relative;height:130px;display:flex;align-items:center;justify-content:center;
 gap:14px;overflow:hidden;padding:0 16px}
.mt-dont__box .mt-logo{width:210px}
.mt-dont__box:after{content:"";position:absolute;inset:0;
 background:linear-gradient(to top right,transparent calc(50% - 1px),#e0342a calc(50% - 1px),
 #e0342a calc(50% + 1px),transparent calc(50% + 1px))}
.mt-dont figcaption{margin:18px 0 0;font-size:13px;line-height:1.45;color:var(--mut)}
.mt-dont__m{width:38px!important;flex:none}
.mt-dont__t{width:150px!important;flex:none}
.mt-dont [data-x=recolor] .mt-logo path{fill:#e0342a}
.mt-dont [data-x=recolor] .mt-logo path:nth-child(-n+3){fill:#f39326}
.mt-dont [data-x=space]{gap:56px}
.mt-dont [data-x=squash] .mt-logo svg{transform:scale(1.32,.66)}
.mt-dont [data-x=noise]{background:repeating-conic-gradient(#d63384 0 25%,#0d6efd 0 50%) 0 0/20px 20px}
.mt-dont [data-x=tilt] .mt-logo svg{transform:rotate(-12deg)}
.mt-dont [data-x=part] .mt-dont__m{width:74px!important}

/* ── гайдлайн ──────────────────────────────────────────────────────────── */
.mt-book{padding:96px 0}
.mt-book__grid{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin:34px 0 0}
.mt-book__grid button{padding:0;border:1px solid var(--ln);background:#fff;cursor:pointer;
 transition:.2s;display:block}
.mt-book__grid button:hover{border-color:var(--b);transform:translateY(-3px)}
.mt-book__grid img{display:block;width:100%;height:auto}
.mt-lb{position:fixed;inset:0;background:rgba(10,14,16,.94);z-index:9999;display:none;
 align-items:center;justify-content:center;padding:28px}
.mt-lb.is-open{display:flex}
.mt-lb__box{position:relative;max-width:1200px;width:100%}
.mt-lb img{display:block;width:100%;height:auto;max-height:82vh;object-fit:contain}
.mt-lb__cap{color:rgba(255,255,255,.7);font-size:13px;text-align:center;padding:14px 0 0}
.mt-lb__x,.mt-lb__nav{position:absolute;background:rgba(255,255,255,.12);border:0;color:#fff;
 cursor:pointer;width:46px;height:46px;display:grid;place-items:center;transition:.2s}
.mt-lb__x:hover,.mt-lb__nav:hover{background:rgba(255,255,255,.26)}
.mt-lb__x{top:-58px;right:0;font-size:26px;line-height:1}
.mt-lb__nav{top:50%;transform:translateY(-50%)}
.mt-lb__nav svg{width:22px;height:22px}
.mt-lb__nav--p{left:-58px}
.mt-lb__nav--n{right:-58px}
.mt-lb__nav--n svg{transform:rotate(180deg)}

/* ── результат ─────────────────────────────────────────────────────────── */
.mt-res{background:#00323F;color:#fff;padding:88px 0}
.mt-res__grid{display:grid;grid-template-columns:1fr 1fr;gap:56px}
.mt-res p{color:rgba(255,255,255,.8)}
.mt-res a{color:#87C7D7}
.mt-res__list{list-style:none;margin:0;padding:0;display:grid;gap:1px;background:rgba(255,255,255,.2);
 border:1px solid rgba(255,255,255,.2)}
.mt-res__list li{background:#00323F;padding:18px 20px;font-size:15px;line-height:1.5}
.mt-res__list b{display:block;font-family:'Montserrat',sans-serif;font-size:13px;letter-spacing:.06em;
 text-transform:uppercase;color:#87C7D7;margin:0 0 6px}

@media (max-width:1000px){
 .mt-task__grid,.mt-mark__grid,.mt-br__grid,.mt-photo__grid,.mt-res__grid,.mt-band__h{
  grid-template-columns:1fr;gap:32px}
 .mt-arch__top{grid-template-columns:repeat(2,1fr)}
 .mt-tiles{grid-template-columns:repeat(2,1fr)}
 .mt-row{grid-template-columns:repeat(2,1fr)}
 .mt-solo{grid-template-columns:1fr}
 .mt-dont__grid{grid-template-columns:repeat(2,1fr)}
 .mt-book__grid{grid-template-columns:repeat(4,1fr)}
 .mt-spec__in{grid-template-columns:repeat(2,1fr)}
 .mt-spec div:nth-child(3){border-left:0;padding-left:0}
 .mt-spec div:nth-child(n+3){border-top:1px solid rgba(255,255,255,.16)}
 .mt-lb__nav--p{left:0}.mt-lb__nav--n{right:0}
 .mt-task__side{border-left:0;border-top:2px solid var(--b);padding:24px 0 0}
}
@media (max-width:640px){
 .mt-w{padding:0 18px}
 .mt-hero{padding-top:96px}
 .mt-hero__in{padding-bottom:44px}
 .mt-task,.mt-mark,.mt-lab,.mt-media,.mt-dont,.mt-book,.mt-photo{padding:64px 0}
 .mt-arch{padding-bottom:64px}
 .mt-br__in{padding-top:64px;padding-bottom:64px}
 .mt-lock{grid-template-columns:1fr}
 .mt-lock div:first-child{grid-column:auto}
 .mt-tiles,.mt-row,.mt-dont__grid{grid-template-columns:1fr}
 .mt-book__grid{grid-template-columns:repeat(3,1fr)}
 .mt-spec__in{grid-template-columns:1fr}
 .mt-spec div+div{border-left:0;border-top:1px solid rgba(255,255,255,.16);padding-left:0}
 .mt-arch__head{padding:20px}
 .mt-lb{padding:16px}
 .mt-lb__x{top:-46px}
}
@media (prefers-reduced-motion:reduce){
 .mt-r{opacity:1;transform:none;transition:none}
 .mt-card:hover{transform:none}
}
</style>"""


# ─── разметка ───────────────────────────────────────────────────────────────
def hero():
    spec = ''.join(f'<div><span class="mt-num">{n}</span><dt>{t}</dt></div>' for n, t in SPEC)
    return (
      '<header class="mt-hero">'
      '<div class="mt-hero__pat" id="mt-hero-pat" aria-hidden="true"></div>'
      '<div class="mt-w mt-hero__in">'
      f'<div class="mt-hero__logo mt-logo mt-logo--w">{svg("logo-mtg")}</div>'
      '<div class="mt-hero__rule"><span>Metra Technology Group, Обнинск</span>'
      '<span>Архитектура бренда и гайдлайн на 69 полос</span></div>'
      '<h1>Пять брендов, собранных из одного квадрата</h1>'
      '<p class="mt-hero__sub">Индустриальная экосистема с четырьмя компаниями внутри. '
      'Мы сделали для неё знак, который выдерживает пять названий, пять палитр, которые не '
      'спорят между собой, пять паттернов на общей сетке и брендбук, по которому это собирают '
      'без дизайнера.</p>'
      '<div class="mt-hero__cta">'
      f'<a class="mt-btn mt-btn--p" href="#mt-brands">Посмотреть систему {ARROW}</a>'
      '<a class="mt-btn mt-btn--gh" href="#mt-book">Открыть гайдлайн</a>'
      '</div></div>'
      f'<div class="mt-spec"><dl class="mt-spec__in">{spec}</dl></div>'
      '</header>')


def task():
    return (
      '<section class="mt-task"><div class="mt-w"><div class="mt-task__grid">'
      '<div class="mt-r"><span class="mt-kick">Задача</span>'
      '<h2>Четыре компании, которые должны читаться как одна группа</h2>'
      '<p class="mt-lead">Metra Technology Group выросла из научно-производственного '
      'предприятия «Метра», основанного инженерами в 1991 году. За тридцать лет вокруг завода '
      'весовой техники появились центр металлообработки, центр промышленной роботизации и '
      'индустриальный хаб в Обнинске.</p>'
      '<p class="mt-lead">Названия для головного бренда и компаний экосистемы заказчик '
      'определил сам. Всё остальное предстояло собрать с нуля, причём так, чтобы четыре очень '
      'разных бизнеса, от весов до роботов, выглядели частями одной группы, а не случайными '
      'соседями в реестре.</p></div>'
      '<div class="mt-task__side mt-r"><h3>Что сделали</h3>'
      '<p><b>Знак</b> для головного бренда и пять локапов: логотип каждой компании собирается '
      'из одного и того же модуля.</p>'
      '<p><b>Пять палитр</b> с приоритетами, монохромными версиями и общими дополнительными '
      'цветами, которые связывают группу.</p>'
      '<p><b>Пять паттернов</b> на одной модульной сетке: у каждой компании свой характер, '
      'но общая логика построения.</p>'
      '<p><b>Фотостиль, носители и гайдлайн</b> на 69 полос: документация, наружная реклама, '
      'сайты, транспорт, сувенирка, презентации, co-branding и правила соседства брендов.</p>'
      '</div></div></div></section>')


def arch():
    cards = ''.join(
      f'<button class="mt-card mt-r" type="button" data-go="{b["k"]}" style="--c:{b["b"]}">'
      f'<span class="mt-card__m mt-logo">{svg("mark-" + b["k"])}</span>'
      f'<b>{b["name"]}</b><span>{b["desc"]}</span></button>'
      for b in BRANDS[1:])
    return (
      '<section class="mt-arch"><div class="mt-w">'
      '<span class="mt-kick">Архитектура бренда</span>'
      '<h2 class="mt-r">Головной бренд и четыре компании</h2>'
      '<p class="mt-lead mt-r">Экосистема устроена как зонтик: головной бренд отвечает за общий '
      'голос группы, компании работают каждая на своём рынке. Поэтому знак у всех один, '
      'а цвет, паттерн и слоган разные.</p>'
      '<div class="mt-arch__head mt-r">'
      f'<div class="mt-logo">{svg("logo-mtg")}</div>'
      '<p>Головной бренд: производство весового оборудования, разработка и интеграция '
      'робототехнических комплексов, металлообработка, инжиниринг, беспилотный транспорт '
      'и промышленный консалтинг.</p></div>'
      f'<div class="mt-arch__top">{cards}</div>'
      '</div></section>')


def mark():
    locks = ''.join(
      f'<div><span class="mt-logo">{svg("logo-" + b["k"])}</span></div>' for b in BRANDS)
    return (
      '<section class="mt-mark"><div class="mt-w"><div class="mt-mark__grid">'
      '<div class="mt-r"><span class="mt-kick">Знак</span>'
      '<h2>Квадрат, из которого вырезана буква M</h2>'
      '<p class="mt-lead">Срезанный угол и шеврон внутри читаются и как буква, и как стрелка '
      'вниз, то есть как импульс. Знак построен на модуле x: из него же берутся расстояния '
      'внутри логотипа и область безопасности вокруг него.</p>'
      '<p class="mt-lead">Дальше к знаку приставляется название, и получается локап. '
      'Названия разной длины, поэтому у головного бренда логотип в три строки, у компаний '
      'в одну или две, но модуль и высота знака не меняются никогда.</p>'
      '<button class="mt-tog" id="mt-mark-tog" type="button" aria-pressed="false">'
      '<i aria-hidden="true"></i>Показать сетку построения</button>'
      f'<div class="mt-lock">{locks}</div>'
      '</div>'
      '<div class="mt-mark__stage mt-r" id="mt-mark-stage">'
      f'<span class="mt-logo">{svg("mark-metra")}</span>'
      '<div class="mt-mark__grid2" id="mt-mark-grid" aria-hidden="true"></div>'
      '</div></div></div></section>')


def brands():
    tabs = ''.join(
      f'<button type="button" role="tab" data-b="{b["k"]}" id="mt-tab-{b["k"]}" '
      f'aria-selected="{"true" if i == 0 else "false"}" aria-controls="mt-panel">{b["short"]}</button>'
      for i, b in enumerate(BRANDS))

    panels = ''
    for i, b in enumerate(BRANDS):
        pal = MAN['brands'][b['k']]['palette']
        sw = ''.join(
          f'<button class="mt-sw__i" type="button" data-hex="{p["hex"]}">'
          f'<span style="background:{p["hex"]}"></span><em>{p["hex"]}</em>'
          f'<small>CMYK {" ".join(p["cmyk"])}</small></button>' for p in pal)
        vals = ''.join(
          f'<li><i>{n + 1:02d}</i><span><b>{t}.</b> {d}</span></li>'
          for n, (t, d) in enumerate(b['values']))
        hid = '' if i == 0 else ' hidden'
        panels += (
          f'<div class="mt-br__pane" data-pane="{b["k"]}"{hid}>'
          '<div class="mt-br__grid">'
          '<div>'
          f'<div class="mt-br__logo mt-logo mt-logo--w">{svg("logo-" + b["k"])}</div>'
          f'<div class="mt-br__desc">{b["desc"]}</div>'
          f'<p class="mt-br__slog">{b["slogan"]}</p>'
          f'<p class="mt-br__about">{b["about"]}</p>'
          f'<div class="mt-br__mis"><b>Миссия</b>{b["mission"]}</div>'
          f'<ul class="mt-vals">{vals}</ul>'
          '</div>'
          '<div>'
          f'<div class="mt-side"><h3>Палитра</h3><div class="mt-sw">{sw}</div></div>'
          f'<div class="mt-side"><h3>Паттерн: {b["pat"].lower()}</h3>'
          f'<p style="margin:0;font-size:14px;line-height:1.55;color:rgba(255,255,255,.8)">'
          f'{b["patnote"]}</p></div>'
          f'<figure class="mt-shot"><img src="{IMG}/m-{fkey(b["k"])}-city.jpg" '
          f'loading="lazy" width="900" height="700" alt="Наружная реклама {b["name"]}: '
          f'сити-формат со слоганом «{b["slogan"].lower()}»">'
          f'<figcaption>Сити-формат {b["name"]}</figcaption></figure>'
          '</div></div></div>')

    return (
      '<section class="mt-br" id="mt-brands" style="--b:#005F7C">'
      '<div class="mt-br__pat" id="mt-br-pat" aria-hidden="true"></div>'
      '<div class="mt-w mt-br__in">'
      '<span class="mt-kick" style="color:rgba(255,255,255,.7)">Пять брендов</span>'
      '<h2>Один знак, пять характеров</h2>'
      '<p class="mt-hero__sub">Переключите бренд: вместе с логотипом меняются цвет, паттерн, '
      'слоган и палитра. Это и есть система, которую описывает брендбук.</p>'
      f'<div class="mt-br__tabs" role="tablist" aria-label="Бренды экосистемы">{tabs}</div>'
      f'<div id="mt-panel" role="tabpanel">{panels}</div>'
      '</div></section>')


def lab():
    tiles = ''.join(
      f'<div class="mt-tile mt-r" style="--c:{b["b"]}">'
      f'<div class="mt-tile__box" data-pat="{b["k"]}"></div>'
      f'<div class="mt-tile__cap"><b>{b["short"]}</b><span>{b["pat"]}</span></div></div>'
      for b in BRANDS)
    return (
      '<section class="mt-lab"><div class="mt-w">'
      '<div class="mt-lab__head">'
      '<div><span class="mt-kick">Паттерн</span>'
      '<h2>Одна сетка, пять рисунков</h2></div>'
      '<div class="mt-lab__ctl">'
      '<button class="mt-tog" id="mt-lab-tog" type="button" aria-pressed="false">'
      '<i aria-hidden="true"></i>Сетка построения</button>'
      '<label>Масштаб<input type="range" id="mt-lab-sc" min="32" max="96" value="56" '
      'aria-label="Масштаб паттерна"></label>'
      '</div></div>'
      '<p class="mt-lead mt-r">У паттерна нет границ: он начинается в любой точке, тянется '
      'сколько нужно и масштабируется под носитель, от подвала бланка до стены переговорной. '
      'Все пять рисунков строятся на одной модульной сетке, где клетка равна модулю знака.</p>'
      f'<div class="mt-tiles">{tiles}</div>'
      '<p class="mt-lab__note">Рисунки на странице собираются скриптом по правилам гайдлайна, '
      'поэтому их можно крутить прямо здесь: включить сетку построения и подвигать масштаб.</p>'
      '</div></section>')


def photo():
    hexsvg = ('<svg viewBox="0 0 100 100" preserveAspectRatio="none">'
              '<polygon points="50,0 100,25 100,75 50,100 0,75 0,25" fill="none" '
              'stroke="#fff" stroke-width=".6" opacity=".85" '
              'transform="translate(2.5,-2.5)"/></svg>')
    return (
      '<section class="mt-photo"><div class="mt-w"><div class="mt-photo__grid">'
      '<div class="mt-r"><span class="mt-kick">Фотостиль</span>'
      '<h2>Два правила вместо фотобанка</h2>'
      '<p class="mt-lead" style="color:rgba(255,255,255,.74)">Брендбук не собирает библиотеку '
      'кадров, он задаёт обработку. Фон перекрывается чёрным слоем в режиме «замена тёмным» '
      'с прозрачностью 70 процентов: любая пёстрая съёмка уходит в глубину и перестаёт спорить '
      'с логотипом.</p>'
      '<p class="mt-lead" style="color:rgba(255,255,255,.74)">Когда картинка идёт блоком, '
      'она садится в маску фирменного элемента, то есть в соту, с контурной обводкой со '
      'смещением. Тот же приём работает на сайте, в презентации и в сторис.</p>'
      '<div class="mt-photo__ctl">'
      '<button class="mt-tog" id="mt-ph-dark" type="button" aria-pressed="false">'
      '<i aria-hidden="true"></i>Чёрный слой 70%</button>'
      '<button class="mt-tog" id="mt-ph-hex" type="button" aria-pressed="false">'
      '<i aria-hidden="true"></i>Маска-сота</button>'
      '</div></div>'
      '<div class="mt-photo__stage mt-r" id="mt-ph-stage">'
      f'<img src="{IMG}/photo-cell.jpg" loading="lazy" width="677" height="451" '
      'alt="Роботизированная ячейка на производстве: кадр в фотостиле Metra Technology Group">'
      f'<div class="mt-photo__hex" aria-hidden="true">{hexsvg}</div>'
      '</div></div></div></section>')


def media():
    bands = ''
    for title, note, shots in MEDIA:
        row = ''.join(
          f'<figure class="mt-fig mt-r" style="--c:{BY[k]["b"]}">'
          f'<img src="{IMG}/m-{f}.jpg" loading="lazy" width="900" height="700" '
          f'alt="{title}: {alt}"><figcaption>{alt}</figcaption></figure>'
          for f, alt, k in shots)
        bands += (f'<div class="mt-band"><div class="mt-band__h"><h3>{title}</h3>'
                  f'<p>{note}</p></div><div class="mt-row">{row}</div></div>')
    solo = ''.join(
      f'<figure class="mt-r"><img src="{IMG}/m-{f}.jpg" loading="lazy" width="1100" height="800" '
      f'alt="{t}: носитель фирменного стиля Metra Technology Group">'
      f'<figcaption><b>{t}</b><span>{d}</span></figcaption></figure>' for f, t, d in SOLO)
    solo = f'<div class="mt-solo">{solo}</div>'
    return (
      '<section class="mt-media"><div class="mt-w">'
      '<span class="mt-kick">Носители</span>'
      '<h2 class="mt-r">Один шаблон, пять заливок</h2>'
      '<p class="mt-lead mt-r">Носители сделаны так, чтобы компании не заказывали дизайн '
      'заново. Раскладка визитки, бланка, сити-формата и слайда общая для всей группы, '
      'меняются только цвет, паттерн и логотип.</p>'
      f'{bands}{solo}'
      '</div></section>')


def dont():
    # там, где нарушение про расстояния и масштаб отдельных элементов, знак и
    # начертание кладём отдельными файлами: только так «нельзя» видно с первого взгляда
    def art(cls):
        if cls in ('space', 'part'):
            return (f'<span class="mt-dont__m mt-logo">{svg("mark-mtg")}</span>'
                    f'<span class="mt-dont__t mt-logo">{svg("word-mtg")}</span>')
        return f'<span class="mt-logo">{svg("logo-mtg")}</span>'

    tiles = ''.join(
      f'<figure class="mt-r"><div class="mt-dont__box" data-x="{cls}">{art(cls)}</div>'
      f'<figcaption>{cap}</figcaption></figure>' for cap, cls in DONT)
    return (
      '<section class="mt-dont"><div class="mt-w">'
      '<span class="mt-kick">Недопустимо</span>'
      '<h2 class="mt-r">Что со знаком делать нельзя</h2>'
      '<p class="mt-lead mt-r">Раздел, ради которого брендбук обычно и открывают. '
      'Ниже те же запреты, что и в гайдлайне, показанные на живом знаке.</p>'
      f'<div class="mt-dont__grid">{tiles}</div>'
      '</div></section>')


def book():
    cells = ''.join(
      f'<button type="button" data-i="{i}" data-src="{IMG}/sheet/{f}" '
      f'aria-label="Полоса {i + 1} из {len(MAN["sheet"])}">'
      f'<img src="{IMG}/sheet/th-{f}" loading="lazy" width="420" height="210" '
      f'alt="Брендбук Metra Technology Group, полоса {i + 1}"></button>'
      for i, f in enumerate(MAN['sheet']))
    return (
      '<section class="mt-book" id="mt-book"><div class="mt-w">'
      '<span class="mt-kick">Гайдлайн</span>'
      '<h2 class="mt-r">Все 69 полос</h2>'
      '<p class="mt-lead mt-r">Головной бренд занимает первые двадцать полос, дальше по '
      'разделу на каждую компанию: позиционирование, логотип, цвет, шрифт, паттерн, '
      'документация, коммуникации, web, фотостиль, транспорт и сувенирка.</p>'
      f'<div class="mt-book__grid">{cells}</div>'
      '</div></section>')


def result():
    items = [
      ('Один знак на пять брендов',
       'Новая компания в группе получает логотип за час: модуль, отступы и высота знака уже '
       'описаны, добавляется только название.'),
      ('Пять палитр, которые не спорят',
       'У каждой компании свой цвет, но дополнительные три цвета общие, поэтому совместные '
       'материалы группы собираются без конфликтов.'),
      ('Паттерн вместо иллюстраций',
       'Пустое место на любом носителе закрывается фирменной сеткой, а не стоковой картинкой.'),
      ('Документ, по которому работают подрядчики',
       'Типография, сувенирка и монтажники получают правила и готовые макеты, а не переписку '
       'с дизайнером.'),
    ]
    lis = ''.join(f'<li><b>{t}</b>{d}</li>' for t, d in items)
    return (
      '<section class="mt-res"><div class="mt-w"><div class="mt-res__grid">'
      '<div class="mt-r"><span class="mt-kick" style="color:#87C7D7">Результат</span>'
      '<h2>Система, которая живёт без дизайнера</h2>'
      '<p>Брендбук на 69 полос закрывает всё, что группа выпускает каждый день: от договора '
      'и визитки до стенда на выставке. Компании экосистемы работают внутри одного стиля, '
      'а головной бренд остаётся узнаваемым на любом носителе.</p>'
      '<p>Больше о направлении: <a href="/creativedesign">услуга «Creative&nbsp;&amp;&nbsp;Design»</a></p>'
      '</div>'
      f'<ul class="mt-res__list mt-r">{lis}</ul>'
      '</div></div></section>')


LIGHTBOX = ('<div class="mt-lb" id="mt-lb" aria-hidden="true">'
            '<div class="mt-lb__box">'
            '<button class="mt-lb__x" id="mt-lb-x" type="button" aria-label="Закрыть">&times;</button>'
            f'<button class="mt-lb__nav mt-lb__nav--p" id="mt-lb-p" type="button" '
            f'aria-label="Предыдущая полоса">{CHEV}</button>'
            f'<button class="mt-lb__nav mt-lb__nav--n" id="mt-lb-n" type="button" '
            f'aria-label="Следующая полоса">{CHEV}</button>'
            '<img id="mt-lb-img" src="" alt="">'
            '<div class="mt-lb__cap" id="mt-lb-c"></div>'
            '</div></div>')


BRAND_JSON = json.dumps({b['k']: {'b': b['b'], 'b2': b['b2'], 'b3': b['b3'], 'ink': b['ink']}
                         for b in BRANDS}, ensure_ascii=False)

PAGE_JS = """<script>(function(){
 var BR=%s;
 // ── движок паттернов: те же построения, что в гайдлайне, только вживую ──
 function seeded(s){return function(){s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff;};}
 function esc(a){return a.join('');}
 function tag(d,w,o){return '<path d="'+d+'" fill="none" stroke="currentColor" stroke-width="'+w+
  '" stroke-linecap="square" opacity="'+(o||1)+'"/>';}
 // dense=true — стена на всю площадь (фон секции), иначе композиция как в гайдлайне
 var PAT={
  mtg:function(W,H,u,r,dense){ // изометрические кубы: ромб сверху и две грани
   var a=u*.8,b=a*.55,hf=a*.95,o=[],i=0;
   for(var x=-a;x<W+a*2;x+=a,i++){
    var base=H-hf-(i%%2?b:0),top=dense?-hf:base-hf*Math.floor(r()*3);
    for(var cy=base;cy>=top;cy-=hf){
     o.push(tag('M'+x+' '+(cy-b)+'L'+(x+a)+' '+cy+'L'+x+' '+(cy+b)+'L'+(x-a)+' '+cy+'Z',1.2));
     o.push(tag('M'+(x-a)+' '+cy+'V'+(cy+hf)+'L'+x+' '+(cy+b+hf)+'V'+(cy+b),1.2));
     o.push(tag('M'+(x+a)+' '+cy+'V'+(cy+hf)+'L'+x+' '+(cy+b+hf),1.2));
    }
   }
   return esc(o);},
  metra:function(W,H,u,r,dense){ // шевроны из буквы M и ромбы со знаком внутри
   var o=[],step=dense?u*1.9:H+u;
   for(var base=H-u*.2;base>-u;base-=step){
    for(var x=u*.1;x<W+u;x+=u*1.2){
     var h=u*(.8+r()*.9);
     o.push(tag('M'+x+' '+base+'V'+(base-h)+'L'+(x+u*.45)+' '+(base-h*.42)+'L'+(x+u*.9)+' '+
      (base-h)+'V'+base,1.4));
     if(r()>.78){
      var cy=base-h-u*.7,s=u*.42;
      o.push(tag('M'+(x+u*.45)+' '+(cy-s)+'L'+(x+u*.45+s)+' '+cy+'L'+(x+u*.45)+' '+(cy+s)+'L'+
       (x+u*.45-s)+' '+cy+'Z',1.4));
      o.push(tag('M'+(x+u*.45-s*.6)+' '+(cy-s*.15)+'L'+(x+u*.45)+' '+(cy+s*.42)+'L'+
       (x+u*.45+s*.6)+' '+(cy-s*.15),1.4));
     }
    }
   }
   return esc(o);},
  pro:function(W,H,u,r,dense){ // лестница из квадратов, линия толще остальных
   var o=[],w=Math.max(5,u*.2),n=Math.ceil(W/u)+Math.ceil(H/u)+4,runs=dense?n:1;
   for(var q=0;q<runs;q++){
    var off=dense?(q*3-Math.ceil(H/u)-2):-2;
    for(var s=0;s<n;s++){
     var x=(s+off)*u*.9,y=H-u*.5-s*u*.62;
     if(y<-u||y>H+u||x>W+u)continue;
     o.push(tag('M'+x+' '+y+'H'+(x+u),w));
     o.push(tag('M'+(x+u*.9)+' '+y+'V'+(y-u*.85),w));
     if((s+q)%%2)o.push(tag('M'+(x+u*.45)+' '+(y+u*.3)+'V'+(y-u*.28),w));
    }
   }
   return esc(o);},
  robotics:function(W,H,u,r,dense){ // зигзаг: траектория манипулятора
   var o=[],step=u*.62;
   for(var k=-3;k<H/step+3;k++){
    var y0=k*step,d='M'+(-u)+' '+y0,up=true;
    for(var x=-u;x<W+u*2;x+=u*.8){up=!up;d+='L'+(x+u*.8)+' '+(y0+(up?0:u*.9));}
    o.push(tag(d,1.2,k%%3?.8:1));
   }
   return esc(o);},
  polis:function(W,H,u,r,dense){ // столбики города: серые и фирменные
   var o=[],w=Math.max(3.5,u*.16),step=dense?H*.52:H+u;
   for(var base=H-u*.12;base>-u;base-=step){
    for(var x=u*.1;x<W+u;x+=u*.66){
     var h=u*(.55+r()*2),br=r()>.45,col=br?'currentColor':'#c9cfd1';
     o.push('<path d="M'+x+' '+base+'V'+(base-h)+'H'+(x+u*.32)+'V'+base+
      '" fill="none" stroke="'+col+'" stroke-width="'+w+'"/>');
     if(r()>.85){var sy=base-h-u*.55;
      o.push('<path d="M'+x+' '+sy+'h'+(u*.32)+'v'+(u*.32)+'h'+(-u*.32)+'Z" fill="none" stroke="'+
       col+'" stroke-width="'+w+'"/>');}
    }
   }
   return esc(o);}
 };
 function grid(W,H,u,step){
  var o=[],s=step||u/2;
  for(var x=0;x<=W;x+=s)o.push('<path d="M'+x+' 0V'+H+'" stroke="rgba(20,24,26,.13)" stroke-width=".6"/>');
  for(var y=0;y<=H;y+=s)o.push('<path d="M0 '+y+'H'+W+'" stroke="rgba(20,24,26,.13)" stroke-width=".6"/>');
  return o.join('');
 }
 function draw(node,key,u,W,H,withGrid,seed,dense){
  var body=PAT[key](W,H,u,seeded(seed||7),dense);
  node.innerHTML='<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="xMidYMax slice" '+
   'aria-hidden="true">'+(withGrid?grid(W,H,u):'')+body+'</svg>';
 }
 // фон героя и секции брендов
 var hp=document.getElementById('mt-hero-pat');
 if(hp)draw(hp,'mtg',60,1500,760,false,11,true);
 var bp=document.getElementById('mt-br-pat');
 function paintWall(k){if(bp)draw(bp,k,74,1500,1300,false,23,true);}
 paintWall('mtg');
 // плитки лаборатории
 var tiles=[].slice.call(document.querySelectorAll('[data-pat]')),labGrid=false,labScale=56;
 function paintTiles(){tiles.forEach(function(t,i){
  draw(t,t.getAttribute('data-pat'),labScale,320,320,labGrid,17+i*5);});}
 paintTiles();
 var lt=document.getElementById('mt-lab-tog');
 if(lt)lt.addEventListener('click',function(){labGrid=!labGrid;
  lt.setAttribute('aria-pressed',String(labGrid));paintTiles();});
 var ls=document.getElementById('mt-lab-sc');
 if(ls)ls.addEventListener('input',function(){labScale=+ls.value;paintTiles();});
 // сетка построения знака
 var ms=document.getElementById('mt-mark-stage'),mg=document.getElementById('mt-mark-grid'),
     mt=document.getElementById('mt-mark-tog');
 // поле 9x на 9x: знак ровно 4x в центре, вокруг него модуль x безопасной зоны
 if(mg)mg.innerHTML='<svg viewBox="0 0 360 360" aria-hidden="true">'+grid(360,360,80,40)+
  '<rect x="100" y="100" width="160" height="160" fill="none" stroke="rgba(0,95,124,.45)" '+
  'stroke-width="1"/>'+
  '<rect x="60" y="60" width="240" height="240" fill="none" stroke="rgba(224,52,42,.6)" '+
  'stroke-width="1" stroke-dasharray="5 4"/>'+
  '<text x="66" y="52" font-family="Montserrat,sans-serif" font-size="13" font-weight="700" '+
  'fill="rgba(20,24,26,.45)">x</text>'+
  '<text x="176" y="52" font-family="Montserrat,sans-serif" font-size="13" font-weight="700" '+
  'fill="rgba(20,24,26,.45)">4x</text></svg>';
 if(mt&&ms)mt.addEventListener('click',function(){var on=!ms.classList.contains('is-grid');
  ms.classList.toggle('is-grid',on);mt.setAttribute('aria-pressed',String(on));});
 // ── переключатель брендов ───────────────────────────────────────────────
 var sec=document.getElementById('mt-brands');
 var tabs=[].slice.call(document.querySelectorAll('.mt-br__tabs button')),
     panes=[].slice.call(document.querySelectorAll('.mt-br__pane'));
 function pick(k){
  var c=BR[k];if(!c||!sec)return;
  sec.style.setProperty('--b',c.b);sec.style.setProperty('--b2',c.b2);
  sec.style.setProperty('--b3',c.b3);
  tabs.forEach(function(t){t.setAttribute('aria-selected',String(t.getAttribute('data-b')===k));});
  panes.forEach(function(p){p.hidden=p.getAttribute('data-pane')!==k;});
  paintWall(k);
 }
 tabs.forEach(function(t){t.addEventListener('click',function(){pick(t.getAttribute('data-b'));});
  t.addEventListener('keydown',function(e){
   var i=tabs.indexOf(t),n=e.key==='ArrowRight'?i+1:e.key==='ArrowLeft'?i-1:-1;
   if(n<0&&e.key!=='ArrowLeft')return;
   if(n===-1)return;
   n=(n+tabs.length)%%tabs.length;e.preventDefault();tabs[n].focus();
   pick(tabs[n].getAttribute('data-b'));});});
 [].forEach.call(document.querySelectorAll('[data-go]'),function(c){
  c.addEventListener('click',function(){
   pick(c.getAttribute('data-go'));
   sec.scrollIntoView({behavior:'smooth',block:'start'});});});
 // ── палитра: HEX в буфер ────────────────────────────────────────────────
 [].forEach.call(document.querySelectorAll('.mt-sw__i'),function(sw){
  sw.addEventListener('click',function(){
   var hex=sw.getAttribute('data-hex');
   function done(){sw.classList.add('is-copied');
    setTimeout(function(){sw.classList.remove('is-copied');},1100);}
   if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(hex).then(done,fallback);
   }else{fallback();}
   function fallback(){var t=document.createElement('textarea');t.value=hex;
    document.body.appendChild(t);t.select();
    try{document.execCommand('copy');}catch(e){}document.body.removeChild(t);done();}});});
 // ── фотостиль ───────────────────────────────────────────────────────────
 var st=document.getElementById('mt-ph-stage');
 [['mt-ph-dark','is-dark'],['mt-ph-hex','is-hex']].forEach(function(p){
  var b=document.getElementById(p[0]);if(!b||!st)return;
  b.addEventListener('click',function(){var on=!st.classList.contains(p[1]);
   st.classList.toggle(p[1],on);b.setAttribute('aria-pressed',String(on));});});
 // ── гайдлайн: лайтбокс ──────────────────────────────────────────────────
 var cards=[].slice.call(document.querySelectorAll('.mt-book__grid button')),
     lb=document.getElementById('mt-lb'),img=document.getElementById('mt-lb-img'),
     cap=document.getElementById('mt-lb-c'),x=document.getElementById('mt-lb-x'),
     pv=document.getElementById('mt-lb-p'),nx=document.getElementById('mt-lb-n'),cur=0;
 function show(i){
  if(i<0)i=cards.length-1;if(i>=cards.length)i=0;cur=i;
  img.src=cards[i].getAttribute('data-src');
  img.alt='Брендбук Metra Technology Group, полоса '+(i+1);
  cap.textContent='Полоса '+(i+1)+' из '+cards.length;
 }
 function open(i){show(i);lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';x.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  img.removeAttribute('src');document.body.style.overflow='';}
 cards.forEach(function(c,i){c.addEventListener('click',function(){open(i);});});
 if(x){x.addEventListener('click',close);
  pv.addEventListener('click',function(){show(cur-1);});
  nx.addEventListener('click',function(){show(cur+1);});
  lb.addEventListener('click',function(e){if(e.target===lb)close();});
  document.addEventListener('keydown',function(e){
   if(!lb.classList.contains('is-open'))return;
   if(e.key==='Escape')close();
   if(e.key==='ArrowRight'){e.preventDefault();show(cur+1);}
   if(e.key==='ArrowLeft'){e.preventDefault();show(cur-1);}});}
 // ── появление блоков ────────────────────────────────────────────────────
 var els=[].slice.call(document.querySelectorAll('.mt-r'));
 function inn(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8%% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(n);else io.observe(n);});
})();</script>""" % BRAND_JSON


BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Брендбук Metra Technology Group",'
  f'"item":"{URL}"}}]}}</script>')

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Брендбук Metra Technology Group: архитектура бренда, знак и паттерны | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: брендбук индустриальной экосистемы Metra Technology Group на 69 полос. Знак и пять логотипов группы (НПП Метра, МетраPRO, MetraRobotics, МетраПолис), пять палитр и пять паттернов на одной модульной сетке, фотостиль, деловая документация, наружная реклама, транспорт, сувенирка и презентации.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Брендбук Metra Technology Group | кейс Hand Marketing">
<meta property="og:description" content="Архитектура бренда для индустриальной экосистемы: один знак, пять компаний, пять паттернов на общей сетке и гайдлайн на 69 полос.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/sheet/01.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def build():
    # своего блока «обсудить проект» нет: фиолетовая форма из rc.footer() закрывает страницу
    body = (f'{rc.header()}<main class="mt">{hero()}{task()}{arch()}{mark()}{brands()}'
            f'{lab()}{photo()}{media()}{dont()}{book()}{result()}</main>{LIGHTBOX}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'metra')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
