#!/usr/bin/env python3
"""Генерит mirror/btl/salaris-xmas/index.html — кейс «Ком подарков»:
BTL-кампания для ТРЦ «Саларис» на ритейл-сезон Christmas (21.12 — 12.01).

Дизайн-концепция: презентация построена на цветовом дренче — каждая полоса своего
цвета, а сквозной герой один, ком из подарков. Страница живёт по тем же правилам:
секции идут цветными экранами ровно тех оттенков, что в исходнике, ком встречает
на первом экране PNG с прозрачностью, дальше визуалы полос идут оригиналами.

Два интерактива, которых не бывает в PDF:
  • калькулятор кома — механика акции (1000 ₽ = 1 salar, команда до 4 человек,
    в розыгрыш не более 50 билетов с участника) считается ползунками, а не
    пересказывается абзацем;
  • носители кампании открываются в лайтбоксе со стрелками.

Ассеты: mirror/images/salaris-xmas/ (scripts/salaris-xmas-assets.py).
Правки — ТОЛЬКО через этот скрипт; build_v1 страницу пропускает по маркеру
<!--custom-page-->."""
import os
import importlib.util

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/salaris-xmas'
URL = 'https://hand-marketing.ru/btl/salaris-xmas/'

def dim(f):
    """width/height прямо из файла: браузер резервирует место, вёрстка не прыгает."""
    im = Image.open(os.path.join(ROOT, 'images', 'salaris-xmas', f))
    return f'width="{im.width}" height="{im.height}"'


ARROW = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">'
         '<path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" '
         'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true">'
        '<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ─── шаги механики: (номер, цвет фона, заголовок, текст, сноска, файл, alt) ───
STEPS = [
    ('1', '#FFC04C', 'Купи',
     'При покупке от 1000 ₽ кассир предлагает стать участником бонусной программы. '
     'Согласился — вместе с чеком получил карту участника.',
     'от 1000 ₽ на чек', 'step-card',
     'Карта участника акции «Ком подарков» ТРЦ «Саларис»'),
    ('2', '#FF8ADE', 'Активируй',
     'Карта включается регистрацией: сайт акции, мобильное приложение или помощь '
     'промоутера у стойки — три входа, чтобы не терять тех, кто не любит формы.',
     'сайт, приложение, промо-стойка', 'step-site',
     'Главная страница сайта акции «Ком подарков»'),
    ('3', '#C4D600', 'Копи баллы',
     'QR-код с чека или цифровой код с него же — и баллы падают на личный счёт. '
     'Валюта акции своя, salar.',
     '1000 ₽ = 1 salar', 'step-coins',
     'Призовые баллы акции — монеты salar'),
    ('4', '#EEC4D7', 'Прибавляй',
     'Здесь акция перестаёт быть личной: участник создаёт команду или вступает '
     'в чужую, и баллы складываются в один общий ком.',
     'команда от 2 до 4 человек', 'step-team',
     'Ёлочные шары в коробке — визуал шага «Прибавляй»'),
    ('5', '#AEE2BE', 'Забирай подарки',
     'Баллы тратятся внутри ТРЦ, в специальных зонах с активностями. Список — '
     'на сайте, в приложении и в подарочном буклете.',
     'зоны активностей в ТРЦ', 'step-gifts',
     'Подарочные коробки — визуал шага «Подарки»'),
    ('6', '#ECC2B1', 'Играй в розыгрыш',
     'Потраченные баллы не сгорают: каждый salar остаётся билетом финального '
     'розыгрыша. Чем больше людей в команде, тем больше билетов в барабане.',
     '1 salar = 1 билет, до 50 билетов с участника', 'step-draw',
     'Игрушечный автомобиль — визуал шага «Розыгрыш призов»'),
]

# ─── подарочный фонд: (заголовок, цвет метки, позиции) ───────────────────────
GIFTS = [
    ('Активности и подарки от ТЦ', '#FF5A73',
     ['Профессиональная фотосессия в студии',
      '4 билета в Kidzania или PandaPark',
      'Активности в специальных зонах центра']),
    ('Партнёрские подарки', '#6716F2',
     ['4 билета в кинотеатр на семейный сеанс',
      'Ужин в ресторане на четверых',
      'Чашка кофе в кофейне',
      'Персональный стилист на час',
      'Сертификаты магазинов центра']),
    ('Розыгрыш главных призов', '#C4D600',
     ['20 домашних кинотеатров',
      'Поездка в Сочи на четверых',
      'Либо семейный кроссовер']),
]

# ─── носители кампании: (файл, заголовок, подпись) ───────────────────────────
MEDIA = [
    ('pos', 'POS-материалы',
     'Лайтбоксы и ролл-апы в центре: знак, ком и одно слово — «Ком подарков». '
     'Больше на носителе ничего не нужно, механику расскажет промоутер.'),
    ('corner', 'Промо-корнер',
     'Стойка под подвесным комом: промоутеры регистрируют участников, объясняют '
     'правила и подхватывают тех, кто прошёл мимо кассы.'),
    ('billboard', 'Наружная реклама',
     'Билборд собран из фирменного градиента и кома: узнаётся на скорости, '
     'работает афишей акции для района.'),
    ('decor', 'Оформление центра',
     'Комы подарков в трёх цветах висят в атриуме — тот же объект, что на карте, '
     'сайте и билборде, только физический.'),
    ('wifi', 'Экран WiFi',
     'Точка контакта, которую обычно тратят впустую: страница авторизации '
     'в бесплатной сети анонсирует акцию и зовёт участвовать.'),
    ('sponsor', 'Информационный спонсор',
     'Beauty-журнал даёт анонсы в разделе событий Москвы и ставит свой корнер: '
     'укладка, make-up и журнал обмениваются на баллы (пример — Marie Claire).'),
]

# ─── что вошло в работу ──────────────────────────────────────────────────────
SCOPE = [
    ('Механика', 'Идея кампании, командная механика накопления, правила розыгрыша '
                 'и подарочный фонд с партнёрами.'),
    ('Digital', 'Сайт акции, мобильное приложение, личный счёт с баллами, '
                'сканирование чека, запись на активности.'),
    ('Оформление', 'Подвесные конструкции в атриуме, промо-корнеры, POS-материалы, '
                   'фотозоны и навигация по зонам активностей.'),
    ('Персонал', 'Промоутеры у стоек и студий, график 10:00–23:00 ежедневно, '
                 'сценарии общения и контроль очереди.'),
    ('Ивент', 'Финальное шоу 12 января: сцена в центральном холле, концерт, '
              'розыгрыш главных призов и автограф-сессия.'),
    ('Смета', 'Стоимостная оценка реализации всей кампании — от печати POS '
              'до гонораров артистов.'),
]

PAGE_CSS = """<style id="sx-css">
.sx{--v:#4C3594;--vd:#33215F;--ink:#2A1A57;--pink:#FFB2DB;--lilac:#D9C4E6;--red:#FF5560;
 --mint:#92FFAA;--ice:#BDF9FF;--tang:#FFC57A;--coral:#FF5A73;--grass:#A8D605;--blush:#FCD7E3;
 font-family:'Onest','Manrope',-apple-system,Arial,sans-serif;color:var(--ink);background:#fff;
 -webkit-font-smoothing:antialiased}
.sx *{box-sizing:border-box}
/* атрибуты width/height у <img> Chrome кладёт в CSS: без height:auto картинка тянется */
.sx img{max-width:100%;height:auto}
.sx h1,.sx h2,.sx h3{font-family:'Manrope','Onest',Arial,sans-serif;font-weight:800;
 letter-spacing:-.02em;margin:0}
.sx p{margin:0}
.sx section{position:relative;overflow:hidden}
.sx-w{max-width:1180px;margin:0 auto;padding:0 40px}
.sx-kick{display:inline-block;font-weight:700;font-size:13px;letter-spacing:.16em;
 text-transform:uppercase;opacity:.62;margin-bottom:18px}
.sx-r{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.3,1)}
.sx-r.is-in{opacity:1;transform:none}

/* ── первый экран ─────────────────────────────────────────────────────────── */
.sx-hero{background:var(--v);color:#fff;padding:96px 0 0}
.sx-hero__in{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,430px);
 gap:32px;align-items:center;padding-bottom:70px}
.sx-hero__logo{height:76px;margin-bottom:38px}
.sx-hero__logo img{height:100%;width:auto;display:block}
.sx-hero h1{font-size:clamp(36px,4.4vw,62px);line-height:1.04;margin-bottom:22px;max-width:15ch}
.sx-hero h1 em{font-style:normal;color:#FF9AD5}
.sx-hero__sub{font-size:19px;line-height:1.55;color:rgba(255,255,255,.84);max-width:620px}
.sx-hero__rule{display:flex;flex-wrap:wrap;gap:10px 26px;font-size:14px;font-weight:600;
 color:rgba(255,255,255,.62);margin-bottom:26px}
.sx-chips{list-style:none;display:flex;flex-wrap:wrap;gap:9px;padding:0;margin:30px 0 0}
.sx-chips li{border:1px solid rgba(255,255,255,.34);border-radius:999px;padding:8px 16px;
 font-size:13.5px;font-weight:600;color:rgba(255,255,255,.9)}
.sx-hero__cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:34px}
.sx-btn{display:inline-flex;align-items:center;gap:9px;height:54px;padding:0 30px;border-radius:999px;
 font:700 15.5px 'Manrope',Arial,sans-serif;text-decoration:none;transition:transform .16s ease,background .16s}
.sx-btn--p{background:#FF4D8D;color:#fff}
.sx-btn--p:hover{background:#ff3480;transform:translateY(-2px)}
.sx-btn--gh{border:1.5px solid rgba(255,255,255,.42);color:#fff}
.sx-btn--gh:hover{background:rgba(255,255,255,.12);transform:translateY(-2px)}
.sx-hero__kom{position:relative;margin:0 -40px -1px 0;min-height:400px}
.sx-hero__kom img{position:absolute;right:-8%;top:50%;transform:translateY(-50%);width:104%;max-width:none;
 filter:drop-shadow(0 40px 70px rgba(0,0,0,.34));animation:sx-float 9s ease-in-out infinite}
@keyframes sx-float{0%,100%{transform:translateY(-50%) rotate(0)}50%{transform:translateY(calc(-50% - 16px)) rotate(-1.3deg)}}
.sx-spec{position:relative;z-index:3;background:rgba(0,0,0,.19);border-top:1px solid rgba(255,255,255,.14)}
.sx-spec__in{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;padding:26px 40px;
 max-width:1180px;margin:0 auto}
.sx-spec dt{font:800 30px 'Manrope',Arial,sans-serif;color:#fff;letter-spacing:-.02em}
.sx-spec dd{margin:4px 0 0;font-size:13.5px;color:rgba(255,255,255,.66);line-height:1.35}

/* ── бриф ─────────────────────────────────────────────────────────────────── */
.sx-task{background:var(--pink);padding:100px 0}
.sx-task__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,440px);gap:56px;align-items:start}
.sx-task h2{font-size:clamp(30px,3.6vw,46px);line-height:1.06;margin-bottom:20px}
.sx-task p{font-size:17px;line-height:1.62;margin-bottom:16px;max-width:640px}
.sx-brief{list-style:none;padding:26px 28px;margin:0;background:rgba(255,255,255,.62);border-radius:22px}
.sx-brief li{display:flex;gap:12px;font-size:15.5px;line-height:1.5;padding:11px 0;
 border-bottom:1px solid rgba(42,26,87,.12)}
.sx-brief li:last-child{border-bottom:0;padding-bottom:0}
.sx-brief li:first-child{padding-top:0}
.sx-brief b{font-weight:800}
.sx-brief span.n{font:800 13px 'Manrope',Arial,sans-serif;opacity:.45;padding-top:2px}
.sx-task__pic{margin-top:34px;border-radius:22px;overflow:hidden;aspect-ratio:16/9}
.sx-task__pic img{display:block;width:100%;height:100%;object-fit:cover}

/* ── инсайт ───────────────────────────────────────────────────────────────── */
.sx-ins{color:#fff;padding:120px 0;background:var(--red)}
.sx-ins__bg{position:absolute;inset:0;background:center/cover no-repeat;opacity:.9}
.sx-ins__in{position:relative;z-index:2;max-width:760px;margin-left:auto;text-align:right}
.sx-ins p{font-size:18px;line-height:1.6;color:rgba(255,255,255,.88);margin-bottom:26px}
.sx-ins h2{font-size:clamp(32px,5vw,62px);line-height:1.05;font-weight:300;
 font-family:'Onest',Arial,sans-serif}
.sx-ins h2 b{font-weight:800}

/* ── идея ─────────────────────────────────────────────────────────────────── */
.sx-idea{background:var(--mint);padding:100px 0}
.sx-idea__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,470px);gap:50px;align-items:center}
.sx-idea h2{font-size:clamp(40px,6vw,86px);line-height:.96;margin:6px 0 24px;color:var(--v)}
.sx-idea__lede{font-size:19px;line-height:1.6;max-width:600px}
.sx-idea__lede b{font-weight:800}
.sx-idea__pic{border-radius:26px;overflow:hidden;aspect-ratio:1/1}
.sx-idea__pic img{display:block;width:100%;height:100%;object-fit:cover;object-position:100% 50%}
.sx-idea__facts{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:38px}
.sx-idea__facts div{background:rgba(255,255,255,.55);border-radius:18px;padding:20px}
.sx-idea__facts b{display:block;font:800 26px 'Manrope',Arial,sans-serif;color:var(--v);margin-bottom:4px}
.sx-idea__facts span{font-size:14px;line-height:1.4}

/* ── механика ─────────────────────────────────────────────────────────────── */
.sx-steps{background:#fff;padding:100px 0 70px}
.sx-steps__head{max-width:720px;margin-bottom:46px}
.sx-steps h2{font-size:clamp(30px,3.6vw,46px);line-height:1.06;margin-bottom:16px}
.sx-steps__head p{font-size:17px;line-height:1.6;opacity:.78}
.sx-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.sx-step{border-radius:26px;overflow:hidden;display:flex;flex-direction:column;color:var(--ink);
 transition:transform .25s cubic-bezier(.2,.7,.3,1)}
.sx-step:hover{transform:translateY(-6px)}
.sx-step__pic{aspect-ratio:16/10;overflow:hidden}
.sx-step__pic img{display:block;width:100%;height:100%;object-fit:cover}
.sx-step__body{padding:24px 26px 28px;flex:1;display:flex;flex-direction:column}
.sx-step__no{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;
 border-radius:50%;background:#fff;font:800 17px 'Manrope',Arial,sans-serif;color:var(--v);margin-bottom:14px}
.sx-step h3{font-size:25px;margin-bottom:10px}
.sx-step p{font-size:15px;line-height:1.55}
.sx-step__note{margin-top:auto;padding-top:16px;font-weight:700;font-size:13.5px;
 letter-spacing:.02em;color:var(--v)}

/* ── калькулятор ──────────────────────────────────────────────────────────── */
.sx-calc{background:var(--vd);color:#fff;padding:96px 0}
.sx-calc__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,440px);gap:56px;align-items:center}
.sx-calc h2{font-size:clamp(28px,3.4vw,42px);line-height:1.08;margin-bottom:16px}
.sx-calc__lede{font-size:17px;line-height:1.6;color:rgba(255,255,255,.78);max-width:560px}
.sx-ctl{margin-top:32px;max-width:560px}
.sx-ctl label{display:flex;justify-content:space-between;align-items:baseline;gap:16px;
 font-size:14.5px;font-weight:600;color:rgba(255,255,255,.72);margin:22px 0 10px}
.sx-ctl label b{font:800 19px 'Manrope',Arial,sans-serif;color:#fff}
.sx-ctl input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:6px;border-radius:3px;
 background:rgba(255,255,255,.22);outline:none}
.sx-ctl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;
 border-radius:50%;background:#FF4D8D;border:3px solid #fff;cursor:pointer}
.sx-ctl input[type=range]::-moz-range-thumb{width:20px;height:20px;border-radius:50%;
 background:#FF4D8D;border:3px solid #fff;cursor:pointer}
.sx-out{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:26px;padding:34px}
.sx-out__row{display:flex;align-items:baseline;justify-content:space-between;gap:16px;padding:14px 0;
 border-bottom:1px solid rgba(255,255,255,.12)}
.sx-out__row:last-of-type{border-bottom:0}
.sx-out__row span{font-size:14.5px;color:rgba(255,255,255,.7)}
.sx-out__row b{font:800 34px 'Manrope',Arial,sans-serif;letter-spacing:-.02em}
.sx-out__row b i{font-style:normal;font-size:15px;font-weight:700;color:rgba(255,255,255,.6);margin-left:6px}
.sx-out__note{margin-top:16px;font-size:13px;line-height:1.5;color:rgba(255,255,255,.55)}
.sx-out__bar{height:10px;border-radius:5px;background:rgba(255,255,255,.14);overflow:hidden;margin-top:20px}
.sx-out__bar i{display:block;height:100%;background:linear-gradient(90deg,#FF4D8D,#FFC04C);
 transition:width .3s ease}

/* ── подарки ──────────────────────────────────────────────────────────────── */
.sx-gifts{background:var(--ice);padding:100px 0}
.sx-gifts h2{font-size:clamp(30px,3.6vw,46px);line-height:1.06;margin-bottom:16px}
.sx-gifts__lede{font-size:17px;line-height:1.6;max-width:660px;margin-bottom:44px}
.sx-gcols{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.sx-gcol{background:#fff;border-radius:26px;padding:30px 28px}
.sx-gcol h3{font-size:21px;line-height:1.2;margin-bottom:18px}
.sx-gcol i{display:block;width:44px;height:6px;border-radius:3px;margin-bottom:18px}
.sx-gcol ul{list-style:none;padding:0;margin:0}
.sx-gcol li{font-size:15.5px;line-height:1.5;padding:10px 0 10px 22px;position:relative}
.sx-gcol li:before{content:'';position:absolute;left:0;top:18px;width:8px;height:8px;border-radius:50%;
 background:currentColor;opacity:.35}
.sx-gifts__belt{margin-top:44px;border-radius:26px;overflow:hidden;aspect-ratio:24/9}
.sx-gifts__belt img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 62%}

/* ── две активности крупным планом ────────────────────────────────────────── */
.sx-act{display:grid;grid-template-columns:1fr 1fr}
.sx-act__c{display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:0}
.sx-act__c--a{background:var(--tang)}
.sx-act__c--b{background:var(--coral);color:#fff}
.sx-act__t{padding:56px 44px}
.sx-act__t h3{font-size:clamp(24px,2.4vw,32px);line-height:1.1;margin-bottom:14px}
.sx-act__t p{font-size:15.5px;line-height:1.6}
.sx-act__c--b p{color:rgba(255,255,255,.9)}
.sx-act__t ul{list-style:none;padding:0;margin:14px 0 0}
.sx-act__t li{font-size:14.5px;line-height:1.5;padding:6px 0 6px 20px;position:relative}
.sx-act__t li:before{content:'';position:absolute;left:0;top:14px;width:7px;height:7px;
 border-radius:50%;background:currentColor;opacity:.4}
.sx-act__p{align-self:stretch}
.sx-act__p img{display:block;width:100%;height:100%;object-fit:cover}

/* ── финал: розыгрыш и ивент ──────────────────────────────────────────────── */
.sx-draw{background:var(--grass);padding:96px 0 0}
.sx-draw__in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,520px);gap:48px;align-items:center}
.sx-draw h2{font-size:clamp(30px,3.8vw,50px);line-height:1.05;margin-bottom:18px;color:var(--v)}
.sx-draw p{font-size:17px;line-height:1.62;margin-bottom:14px;max-width:600px}
.sx-draw__car{margin:0 -40px 0 0}
.sx-draw__car img{display:block;width:100%;height:auto;
 filter:drop-shadow(0 24px 34px rgba(0,0,0,.22))}
.sx-event{background:var(--blush);padding:0}
.sx-event__in{display:grid;grid-template-columns:minmax(0,480px) minmax(0,1fr);gap:48px;align-items:center}
.sx-event__pic{border-radius:0 26px 26px 0;overflow:hidden;aspect-ratio:4/3}
.sx-event__pic img{display:block;width:100%;height:100%;object-fit:cover;object-position:36% 50%}
.sx-event__t{padding:80px 0}
.sx-event h2{font-size:clamp(28px,3.4vw,44px);line-height:1.06;margin-bottom:18px;color:var(--v)}
.sx-event p{font-size:17px;line-height:1.62;margin-bottom:14px}
.sx-event__day{display:inline-flex;align-items:baseline;gap:10px;background:var(--v);color:#fff;
 border-radius:999px;padding:10px 22px;font-weight:700;font-size:15px;margin-bottom:22px}

/* ── носители ─────────────────────────────────────────────────────────────── */
.sx-media{background:var(--v);color:#fff;padding:100px 0}
.sx-media h2{font-size:clamp(30px,3.6vw,46px);line-height:1.06;margin-bottom:16px}
.sx-media__lede{font-size:17px;line-height:1.6;color:rgba(255,255,255,.78);max-width:640px;margin-bottom:44px}
.sx-media__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.sx-media__grid button{display:block;width:100%;text-align:left;padding:0;border:0;cursor:pointer;
 background:rgba(255,255,255,.08);border-radius:22px;overflow:hidden;color:#fff;font:inherit;
 transition:background .2s ease,transform .25s cubic-bezier(.2,.7,.3,1)}
.sx-media__grid button:hover{background:rgba(255,255,255,.16);transform:translateY(-5px)}
.sx-media__grid img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover}
.sx-media__cap{padding:20px 22px 24px}
.sx-media__cap h3{font-size:18px;margin-bottom:8px}
.sx-media__cap p{font-size:14px;line-height:1.5;color:rgba(255,255,255,.7)}

/* ── сроки ────────────────────────────────────────────────────────────────── */
.sx-when{background:var(--lilac);padding:96px 0}
.sx-when__in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,460px);gap:50px;align-items:center}
.sx-when h2{font-size:clamp(28px,3.4vw,44px);line-height:1.06;margin-bottom:26px;color:var(--v)}
.sx-when dl{margin:0;display:grid;gap:20px}
.sx-when dt{font-size:14px;font-weight:600;opacity:.66}
.sx-when dd{margin:4px 0 0;font:800 26px 'Manrope',Arial,sans-serif;color:var(--v);letter-spacing:-.02em}
.sx-when__pic{border-radius:26px;overflow:hidden;aspect-ratio:5/4}
.sx-when__pic img{display:block;width:100%;height:100%;object-fit:cover;object-position:62% 50%}

/* ── что сделали ──────────────────────────────────────────────────────────── */
.sx-scope{background:#fff;padding:96px 0}
.sx-scope__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:56px;align-items:start}
.sx-scope h2{font-size:clamp(28px,3.4vw,44px);line-height:1.06;margin-bottom:16px}
.sx-scope__lede{font-size:17px;line-height:1.62;opacity:.8}
.sx-scope__lede a{color:var(--v);font-weight:700}
.sx-scope ul{list-style:none;padding:0;margin:0;display:grid;gap:2px}
.sx-scope li{display:grid;grid-template-columns:150px 1fr;gap:20px;padding:18px 0;
 border-top:1px solid rgba(42,26,87,.14)}
.sx-scope li:last-child{border-bottom:1px solid rgba(42,26,87,.14)}
.sx-scope li b{font:800 15px 'Manrope',Arial,sans-serif;color:var(--v)}
.sx-scope li span{font-size:15.5px;line-height:1.55}

/* ── лайтбокс ─────────────────────────────────────────────────────────────── */
.sx-lb{position:fixed;inset:0;z-index:9999;background:rgba(24,14,52,.94);display:none;
 align-items:center;justify-content:center;padding:40px}
.sx-lb.is-open{display:flex}
.sx-lb__box{position:relative;max-width:1180px;width:100%}
.sx-lb img{display:block;width:100%;height:auto;max-height:76vh;object-fit:contain;border-radius:14px}
.sx-lb__cap{color:#fff;text-align:center;margin-top:18px;font-size:14.5px;line-height:1.5}
.sx-lb__cap b{display:block;font:800 18px 'Manrope',Arial,sans-serif;margin-bottom:6px}
.sx-lb__cap span{color:rgba(255,255,255,.66)}
.sx-lb__x,.sx-lb__nav{position:absolute;border:0;background:rgba(255,255,255,.14);color:#fff;
 border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;
 transition:background .18s}
.sx-lb__x:hover,.sx-lb__nav:hover{background:rgba(255,255,255,.28)}
.sx-lb__x{top:-46px;right:0;width:38px;height:38px;font-size:24px;line-height:1}
.sx-lb__nav{top:50%;transform:translateY(-50%);width:52px;height:52px}
.sx-lb__nav--p{left:-66px}.sx-lb__nav--p svg{transform:rotate(180deg)}
.sx-lb__nav--n{right:-66px}

@media(max-width:1080px){
 .sx-lb__nav--p{left:6px}.sx-lb__nav--n{right:6px}
 .sx-grid,.sx-gcols,.sx-media__grid{grid-template-columns:1fr 1fr}
 .sx-hero__in,.sx-task__grid,.sx-idea__grid,.sx-calc__grid,.sx-draw__in,.sx-event__in,
 .sx-when__in,.sx-scope__grid{grid-template-columns:1fr}
 .sx-hero__kom{margin:0 -40px -1px;min-height:300px}
 .sx-hero__kom img{position:relative;right:auto;top:0;transform:none;animation:none;width:72%;margin:0 auto;display:block}
 .sx-act{grid-template-columns:1fr}
 .sx-draw__car{margin:24px 0 0}
 .sx-event__t{padding:56px 0}
 .sx-spec__in{grid-template-columns:1fr 1fr}
 .sx-ins__in{text-align:left;margin-left:0}
}
@media(max-width:720px){
 .sx-w{padding:0 18px}
 .sx-hero{padding-top:60px}
 .sx-hero__logo{height:56px;margin-bottom:26px}
 .sx-hero__in{padding-bottom:40px}
 .sx-hero__kom{margin:0 -18px -1px}
 .sx-task,.sx-idea,.sx-steps,.sx-calc,.sx-gifts,.sx-media,.sx-when,.sx-scope{padding:64px 0}
 .sx-ins{padding:80px 0}
 .sx-draw{padding-top:64px}
 .sx-grid,.sx-gcols,.sx-media__grid,.sx-idea__facts,.sx-act__c{grid-template-columns:1fr}
 .sx-act__t{padding:36px 18px}
 .sx-act__p img{max-height:320px}
 .sx-scope li{grid-template-columns:1fr;gap:6px}
 .sx-out{padding:26px 22px}
 .sx-spec__in{padding:22px 18px}
 .sx-lb{padding:18px}
 .sx-lb__x{top:-42px}
}
@media(prefers-reduced-motion:reduce){
 .sx-r{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .sx *{transition-duration:.01ms!important;animation:none!important}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>BTL-кампания для ТРЦ «Саларис»: акция «Ком подарков» на Christmas | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: новогодняя BTL-кампания «Ком подарков» для ТРЦ «Саларис». Командная механика накопления баллов (1000 ₽ = 1 salar), карта участника, сайт и приложение акции, подарочный фонд с партнёрами, оформление центра, промо-корнеры, POS и финальное шоу с розыгрышем автомобиля.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="«Ком подарков» — BTL-кампания для ТРЦ «Саларис» | кейс Hand Marketing">
<meta property="og:description" content="Командная механика вместо личных баллов: семья копит подарки вместе. Механика, digital, оформление центра, промо-персонал и финальное шоу с розыгрышем кроссовера.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/step-site.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def hero():
    chips = ''.join(f'<li>{c}</li>' for c in (
        'Механика акции', 'Digital', 'Оформление ТРЦ', 'POS', 'Промо-персонал',
        'Партнёры', 'Ивент'))
    spec = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in (
        ('23 дня', 'акция с 21 декабря по 12 января'),
        ('6 шагов', 'от чека до розыгрыша призов'),
        ('до 4 человек', 'копят баллы одной командой'),
        ('1 salar', 'за каждую 1000 ₽ в чеке'),
    ))
    return (
      '<header class="sx-hero">'
      '<div class="sx-w sx-hero__in">'
      '<div>'
      f'<div class="sx-hero__logo"><img src="{IMG}/logo-salaris.png" '
      f'alt="Логотип ТРЦ «Саларис»" {dim("logo-salaris.png")}></div>'
      '<div class="sx-hero__rule"><span>ТРЦ «Саларис», Москва</span>'
      '<span>BTL-кампания, ритейл-сезон Christmas</span></div>'
      '<h1>Ком подарков: акция, в которую играют <em>всей семьёй</em></h1>'
      '<p class="sx-hero__sub">Обычная новогодняя механика торгового центра работает с одним '
      'покупателем и одним чеком. Мы предложили «Саларису» механику, где баллы складываются '
      'командой: семья и друзья копят подарки вместе и вместе идут за главным призом.</p>'
      f'<ul class="sx-chips">{chips}</ul>'
      '<div class="sx-hero__cta">'
      f'<a class="sx-btn sx-btn--p" href="#sx-steps">Как работает механика {ARROW}</a>'
      '<a class="sx-btn sx-btn--gh" href="#lead">Обсудить кампанию</a>'
      '</div></div>'
      f'<div class="sx-hero__kom"><img src="{IMG}/kom-red.png" '
      'alt="Ком подарков — ключевой образ кампании: шар, собранный из подарочных коробок" '
      f'{dim("kom-red.png")} fetchpriority="high"></div>'
      '</div>'
      f'<div class="sx-spec"><dl class="sx-spec__in">{spec}</dl></div>'
      '</header>')


def task():
    brief = [
        ('01', 'Механика для посетителей', 'привлечение партнёров и digital-компонент'),
        ('02', 'Оформление площадки', 'атриум, входные группы, зоны активностей'),
        ('03', 'Персонал', 'внешний вид и порядок работы на площадке'),
        ('04', 'POS-материалы', 'и варианты их распространения'),
        ('05', 'Нестандартная коммуникация', 'инсталляции, подвесные конструкции, стикеры, фотозоны'),
        ('06', 'Ивенты', 'события внутри центра на весь период акции'),
    ]
    lis = ''.join(f'<li><span class="n">{n}</span><span><b>{t}</b> — {d}</span></li>'
                  for n, t, d in brief)
    return (
      '<section class="sx-task" id="sx-task"><div class="sx-w sx-task__grid">'
      '<div class="sx-r"><span class="sx-kick">Задача</span>'
      '<h2>Придумать и посчитать BTL-кампанию на сезон Christmas</h2>'
      '<p>«Саларис» — большой семейный центр на юго-западе Москвы, и декабрьский трафик '
      'ему приносить не нужно: люди и так придут за подарками. Ценность в другом — '
      'чтобы человек вернулся не один раз, а несколько, и чтобы средний чек рос вместе '
      'с числом визитов.</p>'
      '<p>Клиент попросил не «идею на слайде», а собранную кампанию: механику, партнёров, '
      'оформление, персонал и смету реализации.</p>'
      f'<div class="sx-task__pic"><img src="{IMG}/balls-pink.jpg" loading="lazy" '
      f'alt="Ёлочные шары на розовом фоне — визуальный ряд кампании" {dim("balls-pink.jpg")}></div>'
      '</div>'
      f'<ul class="sx-brief sx-r">{lis}</ul>'
      '</div></section>')


def insight():
    return (
      '<section class="sx-ins" id="sx-ins">'
      f'<div class="sx-ins__bg" style="background-image:url({IMG}/trees.jpg)" aria-hidden="true"></div>'
      '<div class="sx-w"><div class="sx-ins__in sx-r">'
      '<p>Новый год и Рождество начинаются задолго до самих дат. Каждую зиму все заняты '
      'одними и теми же вопросами: как сделать праздники запоминающимися и кому какой '
      'подарок выбрать.</p>'
      '<h2>А можно ли получать подарки <b>всем вместе</b>?</h2>'
      '</div></div></section>')


def idea():
    facts = ''.join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in (
        ('2–4', 'человека в команде: семья или друзья'),
        ('×4', 'быстрее копится общий счёт'),
        ('0', 'сгоревших баллов: они же билеты розыгрыша'),
    ))
    return (
      '<section class="sx-idea" id="sx-idea"><div class="sx-w sx-idea__grid">'
      '<div class="sx-r"><span class="sx-kick">Идея</span>'
      '<h2>Ком подарков</h2>'
      '<p class="sx-idea__lede">Мы предложили посетителям <b>совместное участие</b>: баллы '
      'копятся быстрее, а превратить их в подарок можно тут же — или продолжить катить дальше, '
      'как снежный ком. Участвовать можно всей семьёй или с друзьями, командами от двух '
      'до четырёх человек.</p>'
      f'<div class="sx-idea__facts">{facts}</div>'
      '</div>'
      f'<div class="sx-idea__pic sx-r"><img src="{IMG}/kom-green.jpg" loading="lazy" '
      f'alt="Ком подарков — образ акции: шар из подарочных коробок" {dim("kom-green.jpg")}></div>'
      '</div></section>')


def steps():
    cards = ''.join(
      f'<article class="sx-step sx-r" style="background:{bg}">'
      f'<div class="sx-step__pic"><img src="{IMG}/{f}.jpg" loading="lazy" alt="{alt}" '
      f'{dim(f + ".jpg")}></div>'
      f'<div class="sx-step__body"><span class="sx-step__no">{no}</span>'
      f'<h3>{t}</h3><p>{d}</p><div class="sx-step__note">{note}</div></div></article>'
      for no, bg, t, d, note, f, alt in STEPS)
    return (
      '<section class="sx-steps" id="sx-steps"><div class="sx-w">'
      '<div class="sx-steps__head sx-r"><span class="sx-kick">Механика</span>'
      '<h2>Шесть шагов: от чека до финального шоу</h2>'
      '<p>Каждый шаг должен объясняться одной фразой на кассе и одним экраном в телефоне — '
      'иначе покупатель в декабре просто не станет разбираться.</p></div>'
      f'<div class="sx-grid">{cards}</div>'
      '</div></section>')


def calc():
    return (
      '<section class="sx-calc" id="sx-calc"><div class="sx-w sx-calc__grid">'
      '<div class="sx-r"><span class="sx-kick">Арифметика акции</span>'
      '<h2>Почему командой выгоднее</h2>'
      '<p class="sx-calc__lede">Один и тот же семейный бюджет даёт разное количество баллов '
      'в зависимости от того, играет человек в одиночку или собрал команду. Подвигайте '
      'ползунки — так механику объясняли и промоутеры на площадке.</p>'
      '<div class="sx-ctl">'
      '<label for="sx-sum">Покупки в центре за акцию, на всю команду'
      '<b id="sx-sum-v">40 000 ₽</b></label>'
      '<input type="range" id="sx-sum" min="5000" max="150000" step="1000" value="40000">'
      '<label for="sx-team">Участников в команде<b id="sx-team-v">4</b></label>'
      '<input type="range" id="sx-team" min="1" max="4" step="1" value="4">'
      '</div></div>'
      '<div class="sx-out sx-r">'
      '<div class="sx-out__row"><span>Накоплено баллов</span>'
      '<b id="sx-salars">40<i>salar</i></b></div>'
      '<div class="sx-out__row"><span>Билетов в финальном розыгрыше</span>'
      '<b id="sx-tickets">40<i>шт.</i></b></div>'
      '<div class="sx-out__row"><span>Потолок команды</span>'
      '<b id="sx-cap">200<i>билетов</i></b></div>'
      '<div class="sx-out__bar"><i id="sx-bar" style="width:20%"></i></div>'
      '<p class="sx-out__note">1000 ₽ = 1 salar. Потраченные на подарки баллы остаются '
      'билетами розыгрыша, но в барабан идёт не больше 50 билетов от одного владельца — '
      'поэтому команда из четырёх человек поднимает потолок вчетверо.</p>'
      '</div></div></section>')


def gifts():
    cols = ''.join(
      f'<div class="sx-gcol sx-r"><i style="background:{c}"></i><h3>{t}</h3>'
      f'<ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div>'
      for t, c, items in GIFTS)
    return (
      '<section class="sx-gifts" id="sx-gifts"><div class="sx-w">'
      '<div class="sx-r"><span class="sx-kick">Подарочный фонд</span>'
      '<h2>Три уровня подарков</h2>'
      '<p class="sx-gifts__lede">Фонд собран так, чтобы у любого количества баллов был '
      'свой сценарий: мелочь тратится сразу и удерживает интерес, крупные позиции держат '
      'человека в акции до финала. Партнёры центра дают свои подарки и получают за это '
      'трафик в собственные точки.</p></div>'
      f'<div class="sx-gcols">{cols}</div>'
      f'<div class="sx-gifts__belt sx-r"><img src="{IMG}/gifts-belt.jpg" loading="lazy" '
      'alt="Подарочные коробки на конвейере — визуал подарочного фонда акции" '
      f'{dim("gifts-belt.jpg")}></div>'
      '</div></section>')


def activities():
    return (
      '<section class="sx-act" id="sx-act">'
      '<div class="sx-act__c sx-act__c--a">'
      '<div class="sx-act__t sx-r"><span class="sx-kick">Активность от центра</span>'
      '<h3>Фотосессия в студии</h3>'
      '<p>Самая ходовая позиция фонда: семейная съёмка в новогодних декорациях прямо '
      'в центре. Запись — на сайте акции или в приложении, слот 15 минут.</p>'
      '<ul><li>Не хватает мест — открывается дополнительная студия</li>'
      '<li>Студии стоят на виду, рядом дежурят промоутеры</li>'
      '<li>Печатный кадр забирают через 15 минут, остальные приходят на почту</li></ul>'
      '</div>'
      f'<div class="sx-act__p"><img src="{IMG}/photo-studio.jpg" loading="lazy" '
      f'alt="Новогодняя семейная фотосессия в студии" {dim("photo-studio.jpg")}></div>'
      '</div>'
      '<div class="sx-act__c sx-act__c--b">'
      '<div class="sx-act__t sx-r"><span class="sx-kick">Партнёрский подарок</span>'
      '<h3>Ужин в ресторане центра</h3>'
      '<p>Команда, накопившая достаточно баллов, ужинает в одном из ресторанов ТРЦ. '
      'Подарок закрывает вечер целиком и возвращает людей в центр ещё раз — '
      'уже в ресторанную зону.</p></div>'
      f'<div class="sx-act__p"><img src="{IMG}/dinner.jpg" loading="lazy" '
      f'alt="Семейный ужин в ресторане — партнёрский подарок акции" {dim("dinner.jpg")}></div>'
      '</div></section>')


def finale():
    return (
      '<section class="sx-draw" id="sx-draw"><div class="sx-w sx-draw__in">'
      '<div class="sx-r"><span class="sx-kick">Розыгрыш</span>'
      '<h2>Главный приз стоит в холле все 23 дня</h2>'
      '<p>Автомобиль в брендировании акции занимает центральный вход на весь период: '
      'это самый честный носитель кампании — его видно каждому входящему и он '
      'объясняет, ради чего копить.</p>'
      '<p>Призы предоставляют спонсоры акции, разыгрываются они в финальном шоу.</p>'
      '</div>'
      f'<div class="sx-draw__car sx-r"><img src="{IMG}/volvo.png" loading="lazy" '
      'alt="Кроссовер в брендировании акции «Ком подарков» — главный приз" '
      f'{dim("volvo.png")}></div>'
      '</div></section>'
      '<section class="sx-event" id="sx-event"><div class="sx-w sx-event__in">'
      f'<div class="sx-event__pic sx-r"><img src="{IMG}/disco.jpg" loading="lazy" '
      f'alt="Ёлочный шар-диско — визуал финального ивента" {dim("disco.jpg")}></div>'
      '<div class="sx-event__t sx-r"><span class="sx-kick">Ивент</span>'
      '<div class="sx-event__day">12 января<span>финал акции</span></div>'
      '<h2>Финальное шоу в центральном холле</h2>'
      '<p>В день окончания в холле собирается сцена: музыкальный концерт, затем ведущий '
      'объявляет розыгрыш главных призов и вручает их победителям.</p>'
      '<p>После розыгрыша — выступление звёзд и автограф-сессия: люди остаются в центре '
      'ещё на пару часов, а не расходятся сразу после барабана.</p>'
      '</div></div></section>')


def media():
    cards = ''.join(
      f'<button type="button" data-src="{IMG}/{f}.jpg" data-title="{t}" data-cap="{c}">'
      f'<img src="{IMG}/thumb-{f}.jpg" loading="lazy" alt="{t} кампании «Ком подарков»" '
      'width="420" height="252">'
      f'<div class="sx-media__cap"><h3>{t}</h3><p>{c}</p></div></button>'
      for f, t, c in MEDIA)
    return (
      '<section class="sx-media" id="sx-media"><div class="sx-w">'
      '<div class="sx-r"><span class="sx-kick">Коммуникация</span>'
      '<h2>Один образ на всех носителях</h2>'
      '<p class="sx-media__lede">Ком подарков работает и как логотип акции, и как физический '
      'объект в атриуме, и как картинка на экране авторизации в WiFi. За счёт этого кампания '
      'узнаётся мгновенно, в какой бы точке центра человек её ни встретил.</p></div>'
      f'<div class="sx-media__grid">{cards}</div>'
      '</div></section>')


def when():
    rows = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in (
        ('Период акции', 'с 21 декабря по 12 января'),
        ('Финальный розыгрыш и ивент', '12 января'),
        ('График работы персонала', 'с 10:00 до 23:00, ежедневно'),
    ))
    return (
      '<section class="sx-when" id="sx-when"><div class="sx-w sx-when__in">'
      '<div class="sx-r"><span class="sx-kick">Сроки</span>'
      '<h2>Кампания встаёт на пик сезона</h2>'
      f'<dl>{rows}</dl></div>'
      f'<div class="sx-when__pic sx-r"><img src="{IMG}/clock.jpg" loading="lazy" '
      f'alt="Циферблат из ёлочных шаров — сроки проведения акции" {dim("clock.jpg")}></div>'
      '</div></section>')


def scope():
    lis = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in SCOPE)
    return (
      '<section class="sx-scope" id="sx-scope"><div class="sx-w sx-scope__grid">'
      '<div class="sx-r"><span class="sx-kick">Состав работ</span>'
      '<h2>Что вошло в кампанию</h2>'
      '<p class="sx-scope__lede">Разработка и стоимостная оценка BTL-кампании под ключ: '
      'от механики и партнёрских договорённостей до финального шоу. Другие проекты '
      'направления — <a href="/btl">услуга «BTL»</a>.</p></div>'
      f'<ul class="sx-r">{lis}</ul>'
      '</div></section>')


LIGHTBOX = ('<div class="sx-lb" id="sx-lb" aria-hidden="true">'
            '<div class="sx-lb__box">'
            '<button class="sx-lb__x" id="sx-lb-x" type="button" aria-label="Закрыть">&times;</button>'
            f'<button class="sx-lb__nav sx-lb__nav--p" id="sx-lb-p" type="button" aria-label="Предыдущий носитель">{CHEV}</button>'
            f'<button class="sx-lb__nav sx-lb__nav--n" id="sx-lb-n" type="button" aria-label="Следующий носитель">{CHEV}</button>'
            '<img id="sx-lb-img" src="" alt="">'
            '<div class="sx-lb__cap"><b id="sx-lb-t"></b><span id="sx-lb-c"></span></div>'
            '</div></div>')

PAGE_JS = """<script>(function(){
 // ── калькулятор кома: 1000 ₽ = 1 salar, в розыгрыш не более 50 билетов с участника
 var sum=document.getElementById('sx-sum'),team=document.getElementById('sx-team');
 if(sum&&team){
  var sv=document.getElementById('sx-sum-v'),tv=document.getElementById('sx-team-v'),
      os=document.getElementById('sx-salars'),ot=document.getElementById('sx-tickets'),
      oc=document.getElementById('sx-cap'),bar=document.getElementById('sx-bar');
  function nf(n){return String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g,'\\u00A0');}
  function calc(){
   var s=+sum.value,t=+team.value,salars=Math.floor(s/1000),cap=t*50,
       tickets=Math.min(salars,cap);
   sv.textContent=nf(s)+'\\u00A0₽';
   tv.textContent=t;
   os.innerHTML=nf(salars)+'<i>salar</i>';
   ot.innerHTML=nf(tickets)+'<i>шт.</i>';
   oc.innerHTML=nf(cap)+'<i>билетов</i>';
   bar.style.width=Math.min(100,Math.round(tickets/cap*100))+'%';
  }
  sum.addEventListener('input',calc); team.addEventListener('input',calc); calc();
 }
 // ── носители: лайтбокс
 var cards=[].slice.call(document.querySelectorAll('.sx-media__grid button')),
     lb=document.getElementById('sx-lb'),img=document.getElementById('sx-lb-img'),
     ttl=document.getElementById('sx-lb-t'),cap=document.getElementById('sx-lb-c'),
     x=document.getElementById('sx-lb-x'),p=document.getElementById('sx-lb-p'),
     n=document.getElementById('sx-lb-n'),cur=0;
 function show(i){
  if(i<0)i=cards.length-1; if(i>=cards.length)i=0; cur=i;
  var c=cards[i];
  img.src=c.getAttribute('data-src');
  img.alt=c.getAttribute('data-title')+' кампании «Ком подарков»';
  ttl.textContent=c.getAttribute('data-title');
  cap.textContent=c.getAttribute('data-cap');
 }
 function open(i){show(i);lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';x.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  img.removeAttribute('src');document.body.style.overflow='';}
 cards.forEach(function(c,i){c.addEventListener('click',function(){open(i);});});
 if(x){x.addEventListener('click',close);
  p.addEventListener('click',function(){show(cur-1);});
  n.addEventListener('click',function(){show(cur+1);});
  lb.addEventListener('click',function(e){if(e.target===lb)close();});
  document.addEventListener('keydown',function(e){
   if(!lb.classList.contains('is-open'))return;
   if(e.key==='Escape')close();
   if(e.key==='ArrowRight'){e.preventDefault();show(cur+1);}
   if(e.key==='ArrowLeft'){e.preventDefault();show(cur-1);}});}
 // ── появление блоков
 var els=[].slice.call(document.querySelectorAll('.sx-r'));
 function inn(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(inn);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){inn(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)inn(n);else io.observe(n);});
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"BTL","item":"https://hand-marketing.ru/btl/"},'
  '{"@type":"ListItem","position":3,"name":"Ком подарков — BTL-кампания для ТРЦ «Саларис»",'
  f'"item":"{URL}"}}]}}</script>')


def build():
    # своего блока «обсудить проект» нет: фиолетовая форма из rc.footer() закрывает
    # страницу, второй CTA был бы дублем (как на CeramicaNova, OBO и SALESDEP)
    body = (f'{rc.header()}<main class="sx">{hero()}{task()}{insight()}{idea()}{steps()}'
            f'{calc()}{gifts()}{activities()}{finale()}{media()}{when()}{scope()}</main>'
            f'{LIGHTBOX}<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'btl', 'salaris-xmas')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'index.html')
    open(p, 'w', encoding='utf-8').write(build())
    print('written', p, f'{os.path.getsize(p) // 1024} КБ')
