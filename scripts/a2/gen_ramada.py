#!/usr/bin/env python3
"""Генерит mirror/creative/becar/ramada/index.html — кейс «Брошюра Ramada Encore»
для Becar Asset Management: печатная брошюра на 20 полос, которой продавали номера
в первом корпусе отельного комплекса Coasis Vertical на Орджоникидзе, 44 в Петербурге.

Дизайн-концепция: «круг вместо рамки». Айдентика Ramada Encore держится на круге,
и в брошюре круг режет фотографию, выводит текст на градиент и держит композицию
полосы без единой линейки. Веб-аналог: Manrope (дисплей) + Onest (текст) из
/fonts/manrope-onest.css, круглые кадры (border-radius:50% на квадратах, вырезанных
из полос), точки-боке и плюсы как декор, градиент красный → магента → фиолетовый.

Живые блоки:
  • переключатель RELAX / REFRESH / CONNECT — три слова бренда, на которых держится
    издание, каждое со своим круглым кадром;
  • калькулятор инвестора — считает по цифрам брошюры (до 16,5% по агентскому
    договору, до 10% по договору аренды, рост стоимости актива от 30%);
  • шторка «ТЗ и дизайн» и листалка из 9 разворотов со скролл-снапом и лайтбоксом.

Ассеты: mirror/images/ramada/ (scripts/ramada-assets.py).

URL кейса прежний (он в sitemap и каталогах). Правки — ТОЛЬКО через этот скрипт;
build_v1 страницу пропускает по маркеру <!--custom-page-->."""
import os
import importlib.util
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/ramada'
URL = 'https://hand-marketing.ru/creative/becar/ramada/'

# ─── 9 разворотов: (полосы, глава, заголовок, описание, alt) ─────────────────
SPREADS = [
 ('2-3', 'Продукт',
  'Всё предложение на первом развороте',
  'Слева обещание: инновационный продукт Becar, отельный комплекс Coasis Vertical '
  'на Орджоникидзе, 44 и доходность до 16,5% годовых. Справа пять фактов, за которыми '
  'инвестор и открывает брошюру: международный бренд, 10 000 м² общественных пространств, '
  'вход от 3,4 млн рублей, открытие в 2022 году, пять корпусов.',
  'Разворот брошюры Ramada Encore: доходность до 16,5% годовых и пять ключевых фактов о проекте'),
 ('4-5', 'Деньги',
  'Почему отель, а не квартира',
  'Разворот отвечает на первый вопрос инвестора. Заполняемость отелей нового формата '
  'выше 80%, это больше показателей классических гостиниц в том же сегменте. Номер '
  'остаётся 100% в собственности и растёт в цене от старта проекта до открытия. Справа '
  'три строки расчёта без таблицы: доходность, порог входа, рост стоимости актива.',
  'Разворот брошюры Ramada Encore: заполняемость отелей нового формата и расчёт доходности номера'),
 ('6-7', 'Продукт',
  'Кто за этим стоит',
  'Слева вес партнёров цифрами: Wyndham Hotels & Resorts с 20 брендами, 9 200 отелями '
  'и 817 000 номеров в 80 странах, Becar Asset Management с 28 годами на рынке, 8 млн м² '
  'в управлении и 5 500 гостиничными номерами. Справа идеология REFRESH: кондо-формат '
  'как старт и для частного, и для институционального инвестора.',
  'Разворот брошюры Ramada Encore: цифры Wyndham и Becar Asset Management, идеология REFRESH'),
 ('8-9', 'Деньги',
  'Зарабатывай, не теряя',
  'Номер приносит доход без личного участия: все заботы берёт управляющая компания. '
  'Четыре аргумента расставлены по кругу фотографии: 100% собственность, прозрачная '
  'отчётность по всему циклу работы УК, выбор программы доходности, ликвидность актива. '
  'Справа сеть Vertical как подтверждённый опыт, а не обещание.',
  'Разворот брошюры Ramada Encore: доход без личного участия инвестора и сеть кондо-отелей Vertical'),
 ('10-11', 'Доказательства',
  'Почему мы уверены в обещаниях',
  'Три причины по номерам: работа с крупнейшими каналами продаж, корпоративные соглашения '
  'и программа лояльности Wyndham, опыт Becar в оптимизации затрат. Справа сравнение '
  'доходности: реализованные проекты приносят собственникам 8-15%, номера в действующем '
  'отеле Vertical на Московском проспекте выросли на 40%, пока квартиры и стрит-ретейл '
  'прибавили 5-10%.',
  'Разворот брошюры Ramada Encore: три аргумента и сравнение доходности с квартирами и стрит-ретейлом'),
 ('12-13', 'Условия',
  '16,5 или 10 процентов',
  'Две программы стоят рядом, чтобы выбор читался за секунду. Агентский договор: '
  'до 16,5% годовых, вознаграждение УК 15%, доход зависит от этапа входа. Договор аренды: '
  'до 10% гарантированно, регистрация в ФРС, номер в аренде на пять лет. Справа условия '
  'покупки: 214-ФЗ, ипотека с первым взносом от 20%, рассрочка, спецусловия при повторной покупке.',
  'Разворот брошюры Ramada Encore: две программы доходности и условия покупки номера'),
 ('14-15', 'Объект',
  'Standard и Comfort',
  'Номерной фонд первого корпуса на двух полосах: 189 номеров Standard по 17 м² '
  'и 280 номеров Comfort по 23 м². Название категории лежит эхом на фоне, фотографии '
  'вырезаны дугами и заходят одна за другую, поэтому две полосы читаются как один кадр. '
  'Метраж и количество стоят цифрами, без описаний интерьера.',
  'Разворот брошюры Ramada Encore: категории номеров Standard и Comfort с метражом и фотографиями'),
 ('16-17', 'Объект',
  'Локация и место встреч',
  'Слева карта в круге: 10 км до Пулково, 20 минут до Экспофорума, 15 минут до метро '
  'пешком, 30 минут до Московского вокзала и делового центра. Справа CONNECT: '
  'многофункциональное общественное пространство объединяет лобби, фронтдеск, рабочие '
  'и ресторанные зоны, и гость перестаёт быть foreigner.',
  'Разворот брошюры Ramada Encore: карта локации в Петербурге и общественные пространства отеля'),
 ('18-19', 'Объект',
  'Что нужно современному путешественнику',
  'Финал издания собирает продукт из деталей: матрасы по стандартам Wyndham, все пять '
  'корпусов соединены переходами, тихий lounge и коворкинг рядом с party zones, '
  'конференц-зал под любое число участников, рестораны от обеда до grab & go и фудмаркета, '
  'дизайн номеров в логике like at home.',
  'Разворот брошюры Ramada Encore: общественные зоны, коворкинг, конференц-зал и рестораны комплекса'),
]

# Каждый кадр — свой разворот, повторов в сетке «В печати» нет
MOCKUPS = [
 ('mock-cover.jpg', 'Обложка рядом с развёрнутым разворотом про общественные пространства'),
 ('mock-earn.jpg', 'Разворот про доход без личного участия и сеть Vertical'),
 ('mock-kondo.jpg', 'Разворот про Wyndham, Becar и идеологию REFRESH'),
 ('mock-terms.jpg', 'Разворот про две программы доходности и условия покупки'),
 ('mock-compare.jpg', 'Разворот про сравнение доходности с квартирой и стрит-ретейлом'),
]

# Три слова бренда: (код, слово, подпись, заголовок, текст, картинка, alt)
CREDO = [
 ('relax', 'Relax', 'Отдых как продукт',
  'Сначала выспаться',
  'Удобная кровать это первый запрос гостя, поэтому в брошюре она стоит раньше сервиса '
  'и технологий. Матрасы по стандартам Wyndham Hotels & Resorts, номера 17 и 23 м², '
  'все пять корпусов соединены переходами. Идеология RELAX в издании отвечает за '
  'полноценный отдых, а не за перечисление опций.',
  'circle-relax.jpg',
  'Круглый кадр из брошюры Ramada Encore: номер Comfort с кроватью у панорамного окна'),
 ('refresh', 'Refresh', 'Кондо-формат',
  'Потом заработать',
  'Вложение в отельный комплекс это старт и для частного, и для институционального '
  'инвестора. Номер остаётся в собственности, доход идёт с первого дня работы отеля, '
  'управляет международный оператор. Так брошюра переводит гостиничный сервис на язык '
  'инвестиционного продукта.',
  'circle-refresh.jpg',
  'Круглый кадр из брошюры Ramada Encore: рендер отельного комплекса на Орджоникидзе, 44'),
 ('connect', 'Connect', 'Общественные пространства',
  'И не быть туристом',
  'Центр притяжения отеля это многофункциональное общественное пространство: лобби, '
  'фронтдеск, рабочие и ресторанные зоны всех корпусов. Место встреч, знакомств '
  'и культурной жизни, где гость перестаёт быть foreigner и становится local. Одним '
  'словом, CONNECT.',
  'circle-connect.jpg',
  'Круглый кадр из брошюры Ramada Encore: гости в общественной зоне отеля с планшетом'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 5l-7 7 7 7"/></svg>')
GRIP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M9 6l-5 6 5 6M15 6l5 6-5 6"/></svg>')

PAGE_CSS = """<style id="rm-css">
:root{
 --rm-red:#e4002b;--rm-mag:#c4108e;--rm-vio:#5b2b90;--rm-lime:#8cc63f;--rm-teal:#00a3ad;
 --rm-ink:#14161c;--rm-ink2:#5c6270;--rm-paper:#f6f3f8;
 --rm-df:'Manrope',system-ui,-apple-system,Arial,sans-serif;
 --rm-tf:'Onest',system-ui,-apple-system,Arial,sans-serif;
 --rm-grad:linear-gradient(126deg,#e4002b 0%,#c4108e 46%,#5b2b90 100%);
}
.rm{font-family:var(--rm-tf);font-size:17px;line-height:1.62;color:var(--rm-ink);
 background:#fff;-webkit-font-smoothing:antialiased}
.rm *{box-sizing:border-box}
.rm h1,.rm h2,.rm h3,.rm h4{font-family:var(--rm-df);font-weight:800;line-height:1.04;
 letter-spacing:-.022em;margin:0;text-wrap:balance}
.rm p{margin:14px 0 0}
.rm a{color:inherit}
.rm-w{width:min(1240px,100% - 40px);margin-inline:auto}
.rm-kick{font-family:var(--rm-df);font-weight:700;font-size:12px;letter-spacing:.18em;
 text-transform:uppercase;display:block}
.rm-r{opacity:0;transform:translateY(22px);transition:opacity .7s cubic-bezier(.2,.7,.3,1),
 transform .7s cubic-bezier(.2,.7,.3,1)}
.rm-r.is-in{opacity:1;transform:none}
.rm-num{font-family:var(--rm-df);font-weight:800;font-variant-numeric:tabular-nums}

/* точки-боке: тот же декор, что на полосах брошюры */
.rm-dots{position:absolute;inset:0;pointer-events:none;
 background-image:radial-gradient(circle,rgba(255,255,255,.5) 2px,transparent 2px),
  radial-gradient(circle,rgba(255,255,255,.28) 5px,transparent 5px),
  radial-gradient(circle,rgba(255,255,255,.16) 9px,transparent 9px);
 background-size:120px 120px,210px 210px,330px 330px;
 background-position:0 0,60px 40px,140px 90px;opacity:.55}

/* ── ГЕРОЙ ── */
.rm-hero{position:relative;background:var(--rm-grad);color:#fff;overflow:hidden;
 padding:clamp(46px,6vw,76px) 0 0}
.rm-hero__in{position:relative;z-index:2}
.rm-hero__top{display:flex;justify-content:space-between;align-items:center;gap:18px;
 flex-wrap:wrap;padding-bottom:clamp(28px,4vw,52px);
 border-bottom:1px solid rgba(255,255,255,.24)}
.rm-logo{font-family:var(--rm-df);font-weight:800;font-size:19px;letter-spacing:-.01em}
.rm-logo span{font-weight:500;opacity:.72;font-size:14px;letter-spacing:.02em}
.rm-hero__by{font-size:13.5px;color:rgba(255,255,255,.72)}
.rm-hero__grid{display:grid;grid-template-columns:1.06fr .94fr;
 gap:clamp(26px,4.4vw,64px);align-items:center;padding:clamp(34px,5vw,66px) 0 0}
.rm-hero .rm-kick{color:rgba(255,255,255,.66)}
.rm-hero h1{font-size:clamp(33px,5.1vw,66px);margin-top:16px}
.rm-hero h1 em{font-style:normal;color:#ffe14d}
.rm-hero__sub{font-size:clamp(16px,1.4vw,19px);color:rgba(255,255,255,.84);max-width:52ch}
.rm-chips{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 0;padding:0;list-style:none}
.rm-chips li{font-size:13px;font-weight:600;padding:8px 14px;border-radius:999px;
 border:1px solid rgba(255,255,255,.34);color:rgba(255,255,255,.92)}
.rm-hero__cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:clamp(24px,3vw,34px)}
.rm-btn{display:inline-flex;align-items:center;gap:10px;font-family:var(--rm-df);
 font-weight:700;font-size:15px;padding:15px 26px;border-radius:999px;text-decoration:none;
 border:1.6px solid transparent;cursor:pointer;transition:transform .2s,background .2s,color .2s}
.rm-btn svg{width:19px;height:19px}
/* .rm a{color:inherit} специфичнее одиночного класса, поэтому цвет кнопок
   задаём через .rm .rm-btn--*, иначе белый текст ложится на белую плашку */
.rm .rm-btn--w{background:#fff;color:var(--rm-vio)}
.rm .rm-btn--gh{border-color:rgba(255,255,255,.5);color:#fff}
.rm-btn:hover{transform:translateY(-2px)}
.rm-btn--gh:hover{background:rgba(255,255,255,.14)}
/* обложка квадратом, за ней большой круг, поверх круглая эмблема */
.rm-hero__art{position:relative;aspect-ratio:1/1}
.rm-hero__ring{position:absolute;inset:-6% -12% -6% 4%;border-radius:50%;
 background:radial-gradient(circle at 34% 30%,rgba(255,255,255,.22),rgba(255,255,255,0) 62%);
 border:1px solid rgba(255,255,255,.22)}
.rm-hero__cover{position:absolute;left:0;top:6%;width:76%;
 box-shadow:0 40px 90px -40px rgba(20,4,30,.75)}
.rm-hero__cover img{display:block;width:100%;height:auto}
.rm-hero__emb{position:absolute;right:-2%;bottom:0;width:44%}
.rm-hero__emb img{display:block;width:100%;height:auto;
 filter:drop-shadow(0 18px 40px rgba(20,4,30,.45))}
.rm-spec{position:relative;z-index:2;margin-top:clamp(34px,5vw,66px);
 border-top:1px solid rgba(255,255,255,.24)}
.rm-spec__in{display:grid;grid-template-columns:repeat(4,1fr);margin:0;
 width:min(1240px,100% - 40px);margin-inline:auto}
.rm-spec__in>div{padding:22px 22px 26px 0}
.rm-spec dt{font-family:var(--rm-df);font-weight:800;font-size:clamp(18px,2vw,25px)}
.rm-spec dd{margin:6px 0 0;font-size:14px;color:rgba(255,255,255,.7);max-width:24ch}

/* ── КЛИЕНТ ── */
.rm-about{padding:clamp(58px,8vw,106px) 0;background:#fff}
.rm-about .rm-kick{color:var(--rm-mag)}
.rm-about h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:22ch}
.rm-about__lede{font-size:clamp(16px,1.35vw,18.5px);color:#333940;max-width:66ch}
.rm-about__two{margin-top:clamp(32px,4.4vw,54px);display:grid;
 grid-template-columns:1fr 1fr;gap:2px;background:#e7e2ee}
.rm-fbox{background:#fff;padding:clamp(22px,2.6vw,34px)}
.rm-fbox h3{font-size:19px}
.rm-fbox>span{display:block;margin-top:6px;font-size:13.5px;color:var(--rm-ink2)}
.rm-fbox__grid{margin-top:22px;display:grid;grid-template-columns:1fr 1fr;gap:18px 14px}
.rm-fbox__grid b{display:block;font-family:var(--rm-df);font-weight:800;
 font-size:clamp(21px,2.3vw,29px);letter-spacing:-.02em}
.rm-fbox__grid span{font-size:13.5px;color:var(--rm-ink2);line-height:1.35}
.rm-fbox--w b{color:var(--rm-red)}
.rm-fbox--b b{color:var(--rm-teal)}

/* ── ЗАДАЧА ── */
.rm-task{padding:clamp(58px,8vw,106px) 0;background:var(--rm-ink);color:#fff}
.rm-task .rm-kick{color:var(--rm-lime)}
.rm-task__grid{display:grid;grid-template-columns:.86fr 1.14fr;gap:clamp(26px,5vw,62px)}
.rm-task h2{font-size:clamp(28px,3.7vw,48px);margin-top:14px}
.rm-task ul{margin:0;padding:0;list-style:none}
.rm-task li{padding:20px 0;border-top:1px solid rgba(255,255,255,.16);display:grid;
 grid-template-columns:44px 1fr;gap:16px;align-items:start}
.rm-task li:last-child{border-bottom:1px solid rgba(255,255,255,.16)}
.rm-task li i{font-style:normal;width:34px;height:34px;border-radius:50%;
 display:grid;place-items:center;background:rgba(255,255,255,.1);
 font-family:var(--rm-df);font-weight:800;font-size:14px;color:var(--rm-lime)}
.rm-task li p{margin:0;font-size:16.5px;color:rgba(255,255,255,.8);max-width:62ch}

/* ── ШТОРКА ТЗ И ДИЗАЙН ── */
.rm-cmp{background:var(--rm-paper);padding:clamp(58px,8vw,106px) 0}
.rm-cmp .rm-kick{color:var(--rm-mag)}
.rm-cmp__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:22px;
 flex-wrap:wrap;padding-bottom:clamp(24px,3.2vw,38px)}
.rm-cmp__hd h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:18ch}
.rm-cmp__hint{font-size:15px;color:var(--rm-ink2);max-width:40ch}
.rm-cmp__box{position:relative;aspect-ratio:2/1;overflow:hidden;background:#fff;
 --p:50%;border-radius:18px;box-shadow:0 30px 70px -44px rgba(20,4,30,.6)}
.rm-cmp__box img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.rm-cmp__box img.b{clip-path:inset(0 0 0 var(--p))}
.rm-cmp__lbl{position:absolute;top:14px;z-index:3;background:rgba(20,22,28,.76);color:#fff;
 font-family:var(--rm-df);font-weight:700;font-size:11.5px;letter-spacing:.12em;
 text-transform:uppercase;padding:7px 13px;border-radius:999px;
 backdrop-filter:blur(6px);pointer-events:none}
.rm-cmp__lbl.l{left:14px}
.rm-cmp__lbl.r{right:14px;background:var(--rm-mag)}
.rm-cmp__bar{position:absolute;top:0;bottom:0;left:var(--p);width:3px;z-index:2;
 background:#fff;pointer-events:none;transform:translateX(-1.5px)}
.rm-cmp__grip{position:absolute;top:50%;left:var(--p);z-index:3;width:48px;height:48px;
 margin:-24px 0 0 -24px;border-radius:50%;background:#fff;color:var(--rm-mag);
 display:grid;place-items:center;pointer-events:none;box-shadow:0 10px 26px rgba(0,0,0,.32)}
.rm-cmp__grip svg{width:22px;height:22px}
.rm-cmp__range{position:absolute;inset:0;z-index:4;width:100%;height:100%;margin:0;
 opacity:0;cursor:ew-resize;-webkit-appearance:none;appearance:none;background:none}
.rm-cmp__range::-webkit-slider-thumb{-webkit-appearance:none;width:48px;height:100%}
.rm-cmp__range::-moz-range-thumb{width:48px;height:400px;border:0;background:none}
.rm-cmp__range:focus-visible{outline:3px solid var(--rm-mag);outline-offset:3px}
.rm-cmp__cap{margin:18px 0 0;font-size:15px;color:var(--rm-ink2);max-width:78ch}

/* ── КРУГ ВМЕСТО РАМКИ ── */
.rm-craft{padding:clamp(58px,8vw,106px) 0;background:#fff}
.rm-craft__grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,62px);
 align-items:center}
.rm-craft .rm-kick{color:var(--rm-red)}
.rm-craft h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px}
.rm-craft p{font-size:clamp(16px,1.35vw,18.5px);color:#333940;max-width:58ch}
.rm-pal{margin-top:28px;display:grid;grid-template-columns:repeat(5,1fr);gap:2px}
.rm-sw{padding:44px 10px 12px;color:#fff}
.rm-sw span{display:block;font-family:var(--rm-df);font-weight:700;font-size:13px}
.rm-sw small{font-size:11.5px;opacity:.78;font-variant-numeric:tabular-nums}
.rm-sw--r{background:var(--rm-red)}
.rm-sw--m{background:var(--rm-mag)}
.rm-sw--v{background:var(--rm-vio)}
.rm-sw--l{background:var(--rm-lime);color:#16240a}
.rm-sw--t{background:var(--rm-teal)}
.rm-craft__ph figure{margin:0}
.rm-craft__ph img{width:100%;height:auto;display:block;border-radius:14px;
 box-shadow:0 30px 70px -44px rgba(20,4,30,.55)}
.rm-craft__ph figcaption{margin-top:14px;font-size:14.5px;color:var(--rm-ink2)}

/* ── ТРИ СЛОВА БРЕНДА ── */
.rm-credo{position:relative;padding:clamp(58px,8vw,106px) 0;
 background:linear-gradient(180deg,#3b1a63 0%,#5b2b90 58%,#7a1d78 100%);color:#fff;
 overflow:hidden}
.rm-credo>*{position:relative;z-index:2}
.rm-credo .rm-kick{color:rgba(255,255,255,.6)}
.rm-credo h2{font-size:clamp(28px,3.7vw,48px);margin-top:14px;max-width:24ch}
.rm-credo__lede{font-size:clamp(16px,1.35vw,18.5px);color:rgba(255,255,255,.78);max-width:64ch}
.rm-credo__tabs{margin-top:clamp(30px,4vw,48px);display:flex;gap:12px;flex-wrap:wrap}
.rm-tab{flex:0 0 auto;width:clamp(104px,11vw,132px);aspect-ratio:1/1;border-radius:50%;
 border:1.6px solid rgba(255,255,255,.34);background:transparent;color:#fff;cursor:pointer;
 display:grid;place-content:center;gap:3px;text-align:center;padding:0 10px;
 font-family:var(--rm-df);transition:background .25s,border-color .25s,transform .25s}
.rm-tab b{font-weight:800;font-size:clamp(15px,1.5vw,18px);letter-spacing:-.01em}
.rm-tab i{font-style:normal;font-family:var(--rm-tf);font-size:11px;
 color:rgba(255,255,255,.62);line-height:1.2}
.rm-tab:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.7)}
.rm-tab.is-on{background:#fff;color:var(--rm-vio);border-color:#fff}
.rm-tab.is-on i{color:rgba(91,43,144,.7)}
.rm-credo__panes{margin-top:clamp(26px,3.4vw,42px)}
.rm-pane{display:none;grid-template-columns:1fr .8fr;gap:clamp(24px,4.4vw,58px);
 align-items:center}
.rm-pane.is-on{display:grid;animation:rm-fade .5s cubic-bezier(.2,.7,.3,1) both}
@keyframes rm-fade{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.rm-pane h3{font-size:clamp(24px,2.9vw,38px)}
.rm-pane p{font-size:clamp(15.5px,1.3vw,18px);color:rgba(255,255,255,.8);max-width:56ch}
.rm-pane__ph{position:relative}
.rm-pane__ph img{display:block;width:100%;height:auto;border-radius:50%;
 border:6px solid rgba(255,255,255,.14);box-shadow:0 34px 80px -40px rgba(0,0,0,.7)}
.rm-pane__word{position:absolute;left:-6%;bottom:4%;font-family:var(--rm-df);
 font-weight:800;font-size:clamp(30px,4vw,54px);color:rgba(255,255,255,.16);
 letter-spacing:-.03em;pointer-events:none;text-transform:uppercase}

/* ── КАЛЬКУЛЯТОР ── */
.rm-calc{padding:clamp(58px,8vw,106px) 0;background:var(--rm-paper)}
.rm-calc .rm-kick{color:var(--rm-vio)}
.rm-calc h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:22ch}
.rm-calc__lede{font-size:clamp(16px,1.35vw,18.5px);color:#333940;max-width:64ch}
.rm-calc__box{margin-top:clamp(30px,4vw,48px);display:grid;grid-template-columns:.92fr 1.08fr;
 gap:2px;background:#e7e2ee;border-radius:20px;overflow:hidden;
 box-shadow:0 30px 70px -46px rgba(20,4,30,.5)}
.rm-calc__in{background:#fff;padding:clamp(24px,3vw,38px)}
.rm-field+.rm-field{margin-top:26px}
.rm-field>label{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
 font-size:13.5px;color:var(--rm-ink2);font-weight:600}
.rm-field>label b{font-family:var(--rm-df);font-weight:800;font-size:20px;color:var(--rm-ink)}
.rm-range{-webkit-appearance:none;appearance:none;width:100%;height:4px;margin:16px 0 0;
 border-radius:999px;background:linear-gradient(90deg,var(--rm-mag) var(--f,50%),
 #e2dce9 var(--f,50%));cursor:pointer}
.rm-range::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;
 border-radius:50%;background:#fff;border:5px solid var(--rm-mag);cursor:grab;
 box-shadow:0 4px 14px rgba(0,0,0,.2)}
.rm-range::-moz-range-thumb{width:24px;height:24px;border-radius:50%;background:#fff;
 border:5px solid var(--rm-mag);cursor:grab}
.rm-range:focus-visible{outline:3px solid var(--rm-vio);outline-offset:4px}
.rm-seg{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px}
.rm-seg button{font-family:var(--rm-tf);font-size:13.5px;line-height:1.3;text-align:left;
 padding:14px 16px;border-radius:14px;border:1.6px solid #e2dce9;background:#fff;
 color:var(--rm-ink2);cursor:pointer;transition:border-color .2s,background .2s,color .2s}
.rm-seg button b{display:block;font-family:var(--rm-df);font-weight:800;font-size:19px;
 color:var(--rm-ink)}
.rm-seg button.is-on{border-color:var(--rm-mag);background:#fdf4fa;color:var(--rm-mag)}
.rm-seg button.is-on b{color:var(--rm-mag)}
.rm-calc__out{background:var(--rm-ink);color:#fff;padding:clamp(24px,3vw,38px);
 display:flex;flex-direction:column;justify-content:center}
.rm-outs{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:rgba(255,255,255,.14)}
.rm-out{background:var(--rm-ink);padding:20px 18px}
.rm-out span{display:block;font-size:12.5px;letter-spacing:.06em;text-transform:uppercase;
 color:rgba(255,255,255,.55);font-weight:600}
.rm-out b{display:block;margin-top:8px;font-family:var(--rm-df);font-weight:800;
 font-size:clamp(23px,2.7vw,34px);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.rm-out--k b{color:var(--rm-lime)}
.rm-calc__note{margin-top:20px;font-size:13px;color:rgba(255,255,255,.55);max-width:56ch}

/* ── ЛИСТАЛКА РАЗВОРОТОВ ── */
.rm-book{background:#fff;padding:clamp(58px,8vw,106px) 0;overflow:hidden}
.rm-book .rm-kick{color:var(--rm-mag)}
.rm-book__hd{display:flex;justify-content:space-between;align-items:flex-end;gap:22px;
 flex-wrap:wrap;padding-bottom:clamp(24px,3.2vw,40px)}
.rm-book__hd h2{font-size:clamp(28px,3.8vw,50px);margin-top:12px}
.rm-book__hint{font-size:14.5px;color:var(--rm-ink2);max-width:34ch}
.rm-track{display:flex;gap:clamp(14px,2vw,26px);overflow-x:auto;scroll-snap-type:x mandatory;
 scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.rm-track::-webkit-scrollbar{display:none}
.rm-slide{flex:0 0 100%;scroll-snap-align:center;margin:0}
.rm-slide__ph{position:relative;background:#f2eef7;cursor:zoom-in;overflow:hidden;
 border-radius:14px}
/* height:auto обязателен: атрибут height у <img> это презентационный хинт, и без
   сброса он перебивает aspect-ratio, а разворот показывается обрезанным по центру */
.rm-slide__ph img{width:100%;height:auto;aspect-ratio:2/1;object-fit:cover;display:block}
.rm-slide__ph::after{content:"";position:absolute;top:0;bottom:0;left:50%;width:2px;
 background:linear-gradient(180deg,rgba(0,0,0,.14),rgba(0,0,0,.04));pointer-events:none}
.rm-slide__pg{position:absolute;left:14px;bottom:14px;z-index:2;background:var(--rm-mag);
 color:#fff;font-family:var(--rm-df);font-weight:700;font-size:11.5px;
 letter-spacing:.1em;text-transform:uppercase;padding:7px 13px;border-radius:999px}
.rm-slide__ch{position:absolute;right:14px;bottom:14px;z-index:2;background:rgba(20,22,28,.7);
 color:#fff;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
 padding:7px 13px;border-radius:999px;backdrop-filter:blur(6px)}
.rm-slide__zoom{position:absolute;right:14px;top:14px;z-index:2;background:rgba(20,22,28,.7);
 color:#fff;font-size:12px;font-weight:600;padding:7px 13px;border-radius:999px;
 backdrop-filter:blur(6px);opacity:0;transition:opacity .25s}
.rm-slide__ph:hover .rm-slide__zoom{opacity:1}
.rm-slide figcaption{padding:24px 2px 0;display:grid;grid-template-columns:.6fr 1.4fr;
 gap:clamp(14px,3vw,40px);align-items:start;min-height:150px}
.rm-slide figcaption h3{font-size:clamp(20px,2.1vw,27px)}
.rm-slide figcaption p{margin:0;font-size:15.5px;color:var(--rm-ink2);max-width:64ch}
.rm-nav{margin-top:clamp(18px,2.4vw,28px);display:flex;align-items:center;
 justify-content:space-between;gap:18px;flex-wrap:wrap}
.rm-nav__btns{display:flex;align-items:center;gap:10px}
.rm-arrow{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;
 background:transparent;border:1.6px solid #ddd5e6;color:var(--rm-ink);cursor:pointer;
 transition:background .2s,border-color .2s,color .2s,opacity .2s}
.rm-arrow svg{width:20px;height:20px}
.rm-arrow--next svg{transform:rotate(180deg)}
.rm-arrow:hover{background:var(--rm-mag);border-color:var(--rm-mag);color:#fff}
.rm-arrow[disabled]{opacity:.3;cursor:default}
.rm-arrow[disabled]:hover{background:transparent;border-color:#ddd5e6;color:var(--rm-ink)}
.rm-count{font-family:var(--rm-df);font-weight:700;font-size:16px;letter-spacing:.06em;
 color:var(--rm-ink2);min-width:5.5em;font-variant-numeric:tabular-nums}
.rm-count b{color:var(--rm-mag);font-weight:800}
.rm-thumbs{display:flex;gap:7px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.rm-thumbs::-webkit-scrollbar{display:none}
.rm-thumb{flex:0 0 auto;width:74px;padding:0;border:0;background:none;cursor:pointer;
 opacity:.4;transition:opacity .22s,outline-color .22s;outline:2px solid transparent;
 outline-offset:2px;border-radius:4px}
.rm-thumb img{width:100%;height:auto;aspect-ratio:2/1;object-fit:cover;display:block;border-radius:4px}
.rm-thumb:hover{opacity:.75}
.rm-thumb.is-on{opacity:1;outline-color:var(--rm-mag)}

/* ── НОМЕРА ── */
.rm-rooms{padding:clamp(58px,8vw,106px) 0;background:var(--rm-ink);color:#fff}
.rm-rooms .rm-kick{color:var(--rm-teal)}
.rm-rooms h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:20ch}
.rm-rooms__lede{font-size:clamp(16px,1.35vw,18.5px);color:rgba(255,255,255,.76);max-width:58ch}
.rm-rooms__row{margin-top:clamp(32px,4.4vw,54px);display:grid;
 grid-template-columns:repeat(3,1fr);gap:clamp(20px,3vw,40px);align-items:start}
.rm-room{text-align:center}
.rm-room__ph{width:100%;aspect-ratio:1/1;border-radius:50%;overflow:hidden;
 border:5px solid rgba(255,255,255,.14)}
.rm-room__ph img{width:100%;height:100%;object-fit:cover;display:block}
.rm-room h3{margin-top:22px;font-size:clamp(21px,2.3vw,29px);letter-spacing:.02em}
.rm-room dl{margin:16px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.rm-room dt{font-size:12px;letter-spacing:.06em;text-transform:uppercase;
 color:rgba(255,255,255,.5);font-weight:600}
.rm-room dd{margin:4px 0 0;font-family:var(--rm-df);font-weight:800;
 font-size:clamp(20px,2.2vw,27px);font-variant-numeric:tabular-nums}
.rm-total{align-self:center;padding:clamp(22px,2.6vw,34px);border-radius:20px;
 background:linear-gradient(140deg,rgba(0,163,173,.22),rgba(140,198,63,.14));
 border:1px solid rgba(255,255,255,.16)}
.rm-total b{display:block;font-family:var(--rm-df);font-weight:800;
 font-size:clamp(34px,4.4vw,58px);letter-spacing:-.03em;color:var(--rm-teal)}
.rm-total span{display:block;margin-top:8px;font-size:14.5px;color:rgba(255,255,255,.74)}

/* ── В ПЕЧАТИ ── */
.rm-print{padding:clamp(58px,8vw,106px) 0;background:#fff}
.rm-print .rm-kick{color:var(--rm-red)}
.rm-print h2{font-size:clamp(28px,3.6vw,46px);margin-top:14px;max-width:20ch}
.rm-print__lede{font-size:clamp(16px,1.35vw,18.5px);color:#333940;max-width:66ch}
.rm-print__grid{margin-top:clamp(30px,4vw,48px);display:grid;
 grid-template-columns:repeat(3,1fr);gap:clamp(14px,2vw,24px)}
.rm-print__grid figure{margin:0}
.rm-print__grid img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block;
 border-radius:14px}
.rm-print__grid figcaption{margin-top:12px;font-size:14px;color:var(--rm-ink2)}
.rm-print__specs{margin-top:clamp(26px,3.4vw,40px);display:flex;flex-wrap:wrap;gap:8px}
.rm-print__specs span{font-size:13px;font-weight:600;padding:9px 16px;border-radius:999px;
 background:var(--rm-paper);color:var(--rm-ink2)}

/* ── РЕЗУЛЬТАТ ── */
.rm-res{padding:clamp(58px,8vw,106px) 0;background:var(--rm-paper)}
.rm-res__grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(26px,5vw,62px)}
.rm-res .rm-kick{color:var(--rm-mag)}
.rm-res h2{font-size:clamp(28px,3.7vw,48px);margin-top:14px}
.rm-res__more{font-size:15px;color:var(--rm-ink2);margin-top:22px}
.rm-res__more a{color:var(--rm-mag);font-weight:600}
.rm-res__list{margin:0;padding:0;list-style:none}
.rm-res__list li{display:grid;grid-template-columns:74px 1fr;gap:18px;align-items:start;
 padding:22px 0;border-top:1px solid #e2dce9}
.rm-res__list li:last-child{border-bottom:1px solid #e2dce9}
.rm-res__list span:first-child{font-family:var(--rm-df);font-weight:800;
 font-size:clamp(32px,3.6vw,46px);line-height:.9;color:var(--rm-mag)}
.rm-res__list span:last-child{font-size:16.5px;color:#333940}

/* ── ЛАЙТБОКС ── */
.rm-lb{position:fixed;inset:0;z-index:9999;background:rgba(12,6,20,.94);display:none;
 padding:clamp(16px,4vw,48px);overflow:auto}
.rm-lb.is-open{display:grid;place-items:center}
.rm-lb__box{position:relative;max-width:1400px;width:100%}
.rm-lb__box img{width:100%;height:auto;display:block;border-radius:10px}
.rm-lb__x{position:absolute;right:0;top:-44px;width:36px;height:36px;border-radius:50%;
 border:1.6px solid rgba(255,255,255,.4);background:none;color:#fff;font-size:22px;
 line-height:1;cursor:pointer}
.rm-lb__cap{margin-top:14px;font-size:14px;color:rgba(255,255,255,.72);text-align:center}

@media(max-width:1000px){
 .rm-hero__grid,.rm-craft__grid,.rm-task__grid,.rm-calc__box,.rm-res__grid,
 .rm-pane.is-on,.rm-about__two{grid-template-columns:1fr}
 .rm-hero__art{max-width:520px}
 .rm-spec__in{grid-template-columns:1fr 1fr}
 .rm-print__grid{grid-template-columns:1fr 1fr}
 .rm-rooms__row{grid-template-columns:1fr 1fr}
 .rm-total{grid-column:1/-1}
 .rm-pane__ph{max-width:420px}
 .rm-slide figcaption{grid-template-columns:1fr;min-height:0}
}
@media(max-width:680px){
 .rm{font-size:16px}
 .rm-pal{grid-template-columns:repeat(3,1fr)}
 .rm-sw{padding:34px 8px 10px}
 .rm-print__grid,.rm-rooms__row,.rm-outs,.rm-seg,.rm-fbox__grid{grid-template-columns:1fr}
 .rm-thumbs{order:3;width:100%}
 .rm-lb__x{top:-38px}
 .rm-slide__ch{display:none}
 .rm-tab{width:96px}
 .rm-pane__word{display:none}
}
@media(prefers-reduced-motion:reduce){
 .rm-r{opacity:1!important;transform:none!important;transition-duration:.01ms!important}
 .rm *{transition-duration:.01ms!important;scroll-behavior:auto;animation-duration:.01ms!important}
 .rm-track{scroll-behavior:auto}
}
</style>"""

HEAD = f'''<!doctype html><html lang="ru" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Брошюра Ramada Encore для Becar: 20 полос про инвестиции в кондо-отель | Hand Marketing</title>
<meta name="description" content="Кейс Hand Marketing: печатная брошюра отельного комплекса Ramada Encore ® by Wyndham в Санкт-Петербурге для Becar Asset Management. 20 полос, 9 разворотов, квадрат 220×220 мм, полноцвет 4+4. Концепция, копирайтинг, вёрстка и препресс: издание объясняет инвестору кондо-формат и доходность номера.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="Брошюра Ramada Encore для Becar Asset Management | кейс Hand Marketing">
<meta property="og:description" content="20 полос и 9 разворотов, которыми Becar продавал номера в кондо-отеле на Орджоникидзе, 44. Концепция, копирайтинг, вёрстка, препресс.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://hand-marketing.ru{IMG}/mock-cover.jpg">
<link rel="shortcut icon" href="/static/cdn/as3561-3033-4731-b230-393638356539/---140.ico" type="image/x-icon">
<!--custom-page-->
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
{rc.FONT}<link href="/fonts/manrope-onest.css" rel="stylesheet">{rc.CSS}{PAGE_CSS}{METRIKA}
</head>
<body>'''


def hero():
    return (
      '<header class="rm-hero">'
      '<div class="rm-dots" aria-hidden="true"></div>'
      '<div class="rm-w rm-hero__in">'
      '<div class="rm-hero__top">'
      '<span class="rm-logo">Ramada Encore <span>® by Wyndham, Saint Petersburg</span></span>'
      '<span class="rm-hero__by">Becar Asset Management, комплекс на Орджоникидзе, 44</span>'
      '</div>'
      '<div class="rm-hero__grid">'
      '<div>'
      '<span class="rm-kick">Полиграфия и копирайтинг</span>'
      '<h1>Брошюра, в которой инвестор <em>считает</em>, а не читает</h1>'
      '<p class="rm-hero__sub">Becar Asset Management строил в Петербурге первый корпус '
      'отельного комплекса под международным брендом и продавал номера частным инвесторам. '
      'Мы собрали издание на 20 полос: менеджер открывает нужный разворот на встрече '
      'и оставляет брошюру на столе после неё.</p>'
      '<ul class="rm-chips"><li>Концепция издания</li><li>Копирайтинг</li>'
      '<li>Вёрстка разворотов</li><li>Препресс и печать</li></ul>'
      '<div class="rm-hero__cta">'
      f'<a class="rm-btn rm-btn--w" href="#rm-book">Листать развороты {ARROW}</a>'
      '<a class="rm-btn rm-btn--gh" href="#rm-calc">Посчитать доход</a>'
      '</div></div>'
      '<div class="rm-hero__art">'
      '<div class="rm-hero__ring" aria-hidden="true"></div>'
      '<div class="rm-hero__cover">'
      f'<img src="{IMG}/cover.jpg" width="1400" height="1400" '
      'alt="Обложка брошюры Ramada Encore: карандашный красно-фиолетовый градиент, круглый '
      'кадр с рендером отеля и заголовок «Создай стабильное финансовое будущее»" '
      'loading="eager" fetchpriority="high"></div>'
      '<div class="rm-hero__emb">'
      f'<img src="{IMG}/emblem.png" width="900" height="749" '
      'alt="Круглая эмблема проекта: логотипы Becar Asset Management и Ramada Encore by Wyndham" '
      'loading="eager"></div>'
      '</div></div></div>'
      '<div class="rm-spec"><dl class="rm-spec__in">'
      '<div><dt>20 полос</dt><dd>девять разворотов плюс обложка и задник</dd></div>'
      '<div><dt>220×220 мм</dt><dd>квадрат, который на стенде видно с трёх метров</dd></div>'
      '<div><dt>4+4</dt><dd>полноцвет с двух сторон, клеевое скрепление</dd></div>'
      '<div><dt>2020 год</dt><dd>к старту продаж номеров в первом корпусе</dd></div>'
      '</dl></div></header>')


def about():
    """Справка о партнёрах проекта. Все цифры взяты с полосы 6 самой брошюры."""
    wyn = [('20', 'брендов в портфеле оператора'), ('9 200', 'отелей по всему миру'),
           ('80', 'стран присутствия'), ('817 000', 'номеров под управлением')]
    bec = [('28 лет', 'на рынке недвижимости'), ('8 млн м²', 'площадей в управлении'),
           ('5 500', 'гостиничных номеров'), ('5 000', 'сотрудников в группе')]

    def cells(rows):
        return ''.join(f'<div><b>{k}</b><span>{H.escape(v)}</span></div>' for k, v in rows)
    return (
      '<section class="rm-about"><div class="rm-w">'
      '<div class="rm-r" style="max-width:76ch"><span class="rm-kick">Клиент и проект</span>'
      '<h2>Кондо-отель, у которого два имени</h2>'
      '<p class="rm-about__lede">Первый корпус комплекса Coasis Vertical на Орджоникидзе, 44 '
      'реализовывался под брендом Ramada Encore ® by Wyndham в кондо-формате: инвестор '
      'покупает номер в собственность, а отелем управляет международный оператор. Сегмент '
      'Upper Midscale по классификации STR, это уровень четырёх звёзд. В брошюре нужно было '
      'удержать оба веса сразу: сеть Wyndham как гарантию сервиса и Becar как управляющего, '
      'который уже сдал сеть Vertical.</p></div>'
      '<div class="rm-about__two rm-r">'
      '<div class="rm-fbox rm-fbox--w"><h3>Wyndham Hotels &amp; Resorts</h3>'
      '<span>Крупнейшая гостиничная компания в мире, оператор бренда</span>'
      f'<div class="rm-fbox__grid">{cells(wyn)}</div></div>'
      '<div class="rm-fbox rm-fbox--b"><h3>Becar Asset Management</h3>'
      '<span>Основана в 1992 году, проектирует и управляет сетью кондо-отелей</span>'
      f'<div class="rm-fbox__grid">{cells(bec)}</div></div>'
      '</div></div></section>')


def task():
    items = [
      'Данные, технические параметры и таблицы доходности нужно было пересобрать в текст, '
      'который читают без подготовки и без менеджера рядом.',
      'Объяснить кондо-формат человеку, который до этого покупал квартиры, а не номера: '
      'что он получает в собственность и кто зарабатывает вместе с ним.',
      'Показать преимущество перед квартирой и стрит-ретейлом цифрами по действующему '
      'объекту, а не обещаниями роста.',
      'Сделать издание, которое на стенде выставки выделяется среди каталогов новостроек '
      'и не выглядит очередным из них.',
    ]
    lis = ''.join(f'<li><i>{i}</i><p>{t}</p></li>' for i, t in enumerate(items, 1))
    return (
      '<section class="rm-task"><div class="rm-w rm-task__grid">'
      '<div class="rm-r"><span class="rm-kick">Задача</span>'
      '<h2>Превратить документацию в брошюру, которую забирают со стенда</h2></div>'
      f'<ul class="rm-r">{lis}</ul>'
      '</div></section>')


def compare():
    """Шторка «ТЗ и дизайн»: слева вводные по проекту, справа разворот 2-3.

    Левую половину собирает scripts/ramada-assets.py из фактов этого проекта
    (в старой версии кейса тут стоял общий текст Becar, не про Ramada). Правая
    половина именно первый разворот, потому что ТЗ и он держатся на одном наборе:
    доходность до 16,5%, вход от 3,4 млн, 10 000 кв. м, пять корпусов, 2022 год."""
    return (
      '<section class="rm-cmp"><div class="rm-w">'
      '<div class="rm-cmp__hd rm-r"><div><span class="rm-kick">С чего начинали</span>'
      '<h2>ТЗ и дизайн</h2></div>'
      '<p class="rm-cmp__hint">Потяните ползунок: слева вводные по проекту, '
      'справа те же факты на полосах 2-3.</p></div>'
      '<div class="rm-cmp__box rm-r" id="rm-cmp">'
      f'<img class="a" src="{IMG}/brief.jpg" width="1680" height="840" '
      'alt="Вводные по проекту без вёрстки: доходность до 16,5%, вход от 3,4 млн, '
      '10 000 кв. м общественных пространств, пять корпусов, открытие в 2022 году" '
      'loading="lazy">'
      f'<img class="b" src="{IMG}/spread-01.jpg" width="2500" height="1250" '
      'alt="Те же факты в готовом развороте брошюры: «Стань частью большего» '
      'и пять показателей проекта на правой полосе" loading="lazy">'
      '<span class="rm-cmp__lbl l">ТЗ</span>'
      '<span class="rm-cmp__lbl r">Дизайн</span>'
      '<span class="rm-cmp__bar"></span>'
      f'<span class="rm-cmp__grip">{GRIP}</span>'
      '<input class="rm-cmp__range" id="rm-cmp-range" type="range" min="0" max="100" '
      'value="50" step="0.5" aria-label="Сравнить ТЗ и готовый разворот">'
      '</div>'
      '<p class="rm-cmp__cap rm-r">Факты те же, набор не менялся: доходность '
      'до 16,5% годовых, вход от 3,4 млн рублей, 10 000 кв. м общественных пространств, '
      'пять корпусов, открытие в 2022 году. Слева это список, который надо прочитать '
      'подряд и удержать в голове. Справа тот же список работает как разворот: '
      'обещание крупным кеглем на левой полосе, пять показателей на правой, и цифра, '
      'ради которой брошюру открывают, стоит первой.</p>'
      '</div></section>')


def craft():
    return (
      '<section class="rm-craft"><div class="rm-w rm-craft__grid">'
      '<div class="rm-r"><span class="rm-kick">Графика</span>'
      '<h2>Круг вместо рамки</h2>'
      '<p style="margin-top:22px">Знак Ramada Encore построен на круге, и мы сделали круг '
      'рабочим инструментом вёрстки. Круг режет фотографию, выводит текст на градиент '
      'и держит композицию полосы <b>без единой линейки</b>. Дуга проходит через сгиб, '
      'поэтому разворот читается как одна плоскость, а не как две страницы рядом.</p>'
      '<p>Там, где фотографии нет, ту же геометрию подхватывают точки-боке и плюсы: они '
      'дают полосе воздух и связывают сухие развороты с цифрами и эмоциональные с людьми.</p>'
      '<p>Цвет ведёт по изданию. Красный и магента отвечают за бренд отеля, фиолетовый '
      'за деньги и условия, зелёно-синий градиент за рост и инвестиционный блок, лайм '
      'за акценты Wyndham.</p>'
      '<div class="rm-pal">'
      '<div class="rm-sw rm-sw--r"><span>Красный</span><small>#E4002B</small></div>'
      '<div class="rm-sw rm-sw--m"><span>Магента</span><small>#C4108E</small></div>'
      '<div class="rm-sw rm-sw--v"><span>Фиолетовый</span><small>#5B2B90</small></div>'
      '<div class="rm-sw rm-sw--l"><span>Лайм</span><small>#8CC63F</small></div>'
      '<div class="rm-sw rm-sw--t"><span>Тил</span><small>#00A3AD</small></div>'
      '</div></div>'
      '<div class="rm-craft__ph rm-r"><figure>'
      f'<img src="{IMG}/spread-08.jpg" width="2500" height="1250" '
      'alt="Разворот брошюры Ramada Encore: карта Петербурга в круге слева и общественные '
      'пространства отеля справа" loading="lazy">'
      '<figcaption>Карта локации сама стала круглым кадром: дуга обрезает её слева, '
      'а точки отмечают Пулково, Экспофорум и Московский вокзал. Справа тот же круг '
      'работает уже с фотографией гостей, поэтому сухая схема и живая сцена держатся '
      'одной геометрией.</figcaption>'
      '</figure></div>'
      '</div></section>')


def credo():
    tabs = ''.join(
      f'<button class="rm-tab{" is-on" if i == 0 else ""}" type="button" data-pane="{code}" '
      f'aria-pressed="{"true" if i == 0 else "false"}"><b>{word}</b><i>{H.escape(sub)}</i></button>'
      for i, (code, word, sub, _t, _p, _im, _alt) in enumerate(CREDO))
    panes = ''.join(
      f'<div class="rm-pane{" is-on" if i == 0 else ""}" id="rm-pane-{code}">'
      f'<div><span class="rm-kick" style="color:var(--rm-lime)">{word.upper()}</span>'
      f'<h3 style="margin-top:12px">{H.escape(title)}</h3><p>{text}</p></div>'
      f'<div class="rm-pane__ph"><img src="{IMG}/{im}" width="616" height="616" '
      f'alt="{alt}" loading="lazy">'
      f'<span class="rm-pane__word" aria-hidden="true">{word}</span></div></div>'
      for i, (code, word, sub, title, text, im, alt) in enumerate(CREDO))
    return (
      '<section class="rm-credo">'
      '<div class="rm-dots" aria-hidden="true"></div>'
      '<div class="rm-w">'
      '<div class="rm-r" style="max-width:74ch"><span class="rm-kick">Каркас издания</span>'
      '<h2>Три слова бренда вместо списка опций</h2>'
      '<p class="rm-credo__lede">У Ramada Encore есть три слова, которые оператор пишет '
      'на всех своих отелях: relax, refresh, connect. Мы не стали перечислять опции '
      'комплекса списком, а разложили брошюру по этим словам. Получилась логика, по которой '
      'инвестор проходит сам: сначала отдых как продукт, потом деньги, в конце люди.</p></div>'
      f'<div class="rm-credo__tabs rm-r" id="rm-tabs" role="group" '
      f'aria-label="Три принципа бренда">{tabs}</div>'
      f'<div class="rm-credo__panes rm-r">{panes}</div>'
      '</div></section>')


def calc():
    return (
      '<section class="rm-calc" id="rm-calc"><div class="rm-w">'
      '<div class="rm-r" style="max-width:70ch"><span class="rm-kick">Живой блок</span>'
      '<h2>Калькулятор, который стоял в брошюре таблицей</h2>'
      '<p class="rm-calc__lede">В печати выбор программы занимал разворот: слева агентский '
      'договор с доходностью до 16,5%, справа договор аренды с гарантированными 10%. '
      'На сайте тот же разворот можно потрогать: подвиньте сумму и горизонт, чтобы увидеть '
      'разницу между программами.</p></div>'
      '<div class="rm-calc__box rm-r">'
      '<div class="rm-calc__in">'
      '<div class="rm-field">'
      '<label for="rm-sum">Стоимость номера<b><span id="rm-sum-v">6,0</span> млн ₽</b></label>'
      '<input class="rm-range" id="rm-sum" type="range" min="3.4" max="20" step="0.1" '
      'value="6" aria-label="Стоимость номера в миллионах рублей">'
      '</div>'
      '<div class="rm-field">'
      '<label for="rm-years">Горизонт<b><span id="rm-years-v">5</span> лет</b></label>'
      '<input class="rm-range" id="rm-years" type="range" min="1" max="10" step="1" '
      'value="5" aria-label="Горизонт в годах">'
      '</div>'
      '<div class="rm-field">'
      '<label>Программа доходности</label>'
      '<div class="rm-seg" id="rm-prog">'
      '<button type="button" class="is-on" data-rate="16.5" aria-pressed="true">'
      '<b>до 16,5%</b>агентский договор, доход зависит от этапа входа</button>'
      '<button type="button" data-rate="10" aria-pressed="false">'
      '<b>до 10%</b>договор аренды, гарантированный доход</button>'
      '</div></div></div>'
      '<div class="rm-calc__out">'
      '<div class="rm-outs">'
      '<div class="rm-out"><span>Доход в год</span><b id="rm-o-year">990 000 ₽</b></div>'
      '<div class="rm-out"><span>Доход в месяц</span><b id="rm-o-month">82 500 ₽</b></div>'
      '<div class="rm-out rm-out--k"><span>Доход за горизонт</span>'
      '<b id="rm-o-total">4,95 млн ₽</b></div>'
      '<div class="rm-out rm-out--k"><span>Номер к открытию</span>'
      '<b id="rm-o-asset">7,8 млн ₽</b></div>'
      '</div>'
      '<p class="rm-calc__note">Считаем по цифрам брошюры 2020 года: доходность до 16,5% '
      'по агентскому договору, до 10% по договору аренды с опцией «Гарант+», рост стоимости '
      'актива от 30% от старта проекта до открытия отеля. Это иллюстрация к кейсу, '
      'не оферта и не инвестиционное предложение.</p>'
      '</div></div></div></section>')


def book():
    slides, thumbs = '', ''
    total = len(SPREADS)
    for i, (pg, chap, title, text, alt) in enumerate(SPREADS, 1):
        src = f'{IMG}/spread-{i:02d}.jpg'
        eager = 'eager' if i == 1 else 'lazy'
        slides += (
          f'<figure class="rm-slide" data-i="{i}">'
          f'<div class="rm-slide__ph rm-zoom" role="button" tabindex="0" data-src="{src}" '
          f'data-cap="Разворот {i} из {total}: {H.escape(title)}. Полосы {pg}" '
          f'aria-label="Открыть разворот {i} на весь экран">'
          f'<span class="rm-slide__pg">Полосы {pg}</span>'
          f'<span class="rm-slide__ch">{chap}</span>'
          f'<img src="{src}" width="2500" height="1250" alt="{alt}" loading="{eager}">'
          f'<span class="rm-slide__zoom">Открыть крупно</span></div>'
          f'<figcaption><h3>{H.escape(title)}</h3><p>{text}</p></figcaption></figure>')
        thumbs += (f'<button class="rm-thumb{" is-on" if i == 1 else ""}" data-go="{i}" '
                   f'type="button" aria-label="Разворот {i}, полосы {pg}">'
                   f'<img src="{IMG}/thumb-{i:02d}.jpg" width="220" height="110" alt="" '
                   f'loading="lazy"></button>')
    return (
      '<section class="rm-book" id="rm-book"><div class="rm-w">'
      '<div class="rm-book__hd rm-r"><div><span class="rm-kick">Развороты</span>'
      f'<h2>{total} разворотов, {total * 2 + 2} полосы</h2></div>'
      '<p class="rm-book__hint">Брошюру читали в руках, поэтому здесь она тоже собрана '
      'разворотами. Нажмите на разворот, чтобы рассмотреть его целиком.</p></div>'
      f'<div class="rm-track" id="rm-track">{slides}</div>'
      '<div class="rm-nav"><div class="rm-nav__btns">'
      f'<button class="rm-arrow rm-arrow--prev" id="rm-prev" type="button" aria-label="Предыдущий разворот">{CHEV}</button>'
      f'<button class="rm-arrow rm-arrow--next" id="rm-next" type="button" aria-label="Следующий разворот">{CHEV}</button>'
      f'<span class="rm-count" id="rm-count"><b>01</b> / {total:02d}</span></div>'
      f'<div class="rm-thumbs" id="rm-thumbs">{thumbs}</div>'
      '</div></div></section>')


def rooms():
    cards = [
      ('circle-standard.jpg', 'Standard', '189', '17 м²',
       'Круглый кадр из брошюры: номер Standard с рабочим столом и окном'),
      ('circle-comfort.jpg', 'Comfort', '280', '23 м²',
       'Круглый кадр из брошюры: номер Comfort с двумя кроватями, вид сверху'),
    ]
    figs = ''.join(
      f'<div class="rm-room"><div class="rm-room__ph">'
      f'<img src="{IMG}/{im}" width="518" height="518" alt="{alt}" loading="lazy"></div>'
      f'<h3>{name}</h3><dl><div><dt>Номеров</dt><dd>{n}</dd></div>'
      f'<div><dt>Средняя площадь</dt><dd>{a}</dd></div></dl></div>'
      for im, name, n, a, alt in cards)
    return (
      '<section class="rm-rooms"><div class="rm-w">'
      '<div class="rm-r" style="max-width:70ch"><span class="rm-kick">Номерной фонд</span>'
      '<h2>Две категории и ни одного описания интерьера</h2>'
      '<p class="rm-rooms__lede">На развороте про номера мы оставили только то, что решает: '
      'название категории, количество и метраж. Всё остальное показывает фотография, '
      'вырезанная дугой. Название лежит эхом на фоне, поэтому полоса читается как кадр, '
      'а не как страница каталога.</p></div>'
      f'<div class="rm-rooms__row rm-r">{figs}'
      '<div class="rm-total"><b>469</b><span>номеров в первом корпусе комплекса, '
      'и каждый продавался частному инвестору отдельно</span></div>'
      '</div></div></section>')


def printing():
    figs = ''.join(
      f'<figure><img src="{IMG}/{f}" alt="Мокап печатной брошюры Ramada Encore: '
      f'{H.escape(c.lower())}" loading="lazy"><figcaption>{H.escape(c)}</figcaption></figure>'
      for f, c in MOCKUPS)
    return (
      '<section class="rm-print" id="rm-print"><div class="rm-w">'
      '<div class="rm-r" style="max-width:66ch"><span class="rm-kick">В печати</span>'
      '<h2>Квадрат, который забирают со стенда</h2>'
      '<p class="rm-print__lede">Формат выбрали под сценарий выставки: квадрат 220×220 мм '
      'удобно держать вдвоём, он не похож на каталог новостройки и его видно в стойке '
      'с трёх метров. Брошюра ушла в печать полноцветом с двух сторон, с вылетами '
      'под обрез и клеевым скреплением.</p></div>'
      f'<div class="rm-print__grid rm-r">{figs}</div>'
      '<div class="rm-print__specs rm-r"><span>20 полос</span><span>220×220 мм</span>'
      '<span>Полноцвет 4+4</span><span>Вылеты под обрез</span>'
      '<span>Клеевое скрепление</span></div>'
      '</div></section>')


def result():
    items = [
      ('20', 'Готовый макет на <b>20 полос</b> с препрессом: вылеты, полноцвет, файл '
       'для типографии. Клиент получил издание, а не набор макетов.'),
      ('9', '<b>Девять разворотов</b>, каждый закрывает один вопрос инвестора '
       'и заканчивается цифрой. На встрече менеджер открывает нужный разворот вместо '
       'пересказа условий.'),
      ('3', '<b>Три слова бренда</b> стали каркасом издания: relax отвечает за продукт, '
       'refresh за деньги, connect за людей. Опции комплекса перестали быть списком.'),
      ('1', '<b>Один визуальный язык</b> на всё издание: круг, градиент и крупная цифра '
       'как точка в конце разворота. Когда у проекта менялись цены и сроки, брошюру '
       'переиздавали по цифрам, не переверстывая развороты заново.'),
    ]
    lis = ''.join(f'<li><span>{k}</span><span>{v}</span></li>' for k, v in items)
    return (
      '<section class="rm-res"><div class="rm-w rm-res__grid">'
      '<div class="rm-r"><span class="rm-kick">Результат</span>'
      '<h2>Что получил клиент</h2>'
      '<p class="rm-res__more">Концепция, тексты, вёрстка и препресс. Больше о направлении: '
      '<a href="/creativedesign">услуга «Creative&nbsp;&amp;&nbsp;Design»</a></p></div>'
      f'<ul class="rm-res__list rm-r">{lis}</ul>'
      '</div></section>')


LIGHTBOX = ('<div class="rm-lb" id="rm-lb" aria-hidden="true">'
            '<div class="rm-lb__box">'
            '<button class="rm-lb__x" id="rm-lb-x" type="button" aria-label="Закрыть">&times;</button>'
            '<img id="rm-lb-img" src="" alt="">'
            '<div class="rm-lb__cap" id="rm-lb-cap"></div></div></div>')

PAGE_JS = """<script>(function(){
 // ── листалка разворотов ──
 var track=document.getElementById('rm-track');
 if(track){
  var slides=[].slice.call(track.querySelectorAll('.rm-slide')),
      thumbs=[].slice.call(document.querySelectorAll('.rm-thumb')),
      prev=document.getElementById('rm-prev'),next=document.getElementById('rm-next'),
      count=document.getElementById('rm-count'),cur=1,total=slides.length;
  function pad(n){return n<10?'0'+n:''+n;}
  function mark(i){cur=i;
   count.innerHTML='<b>'+pad(i)+'</b> / '+pad(total);
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
 // ── шторка «ТЗ и дизайн» ──
 var cmp=document.getElementById('rm-cmp'),cr=document.getElementById('rm-cmp-range');
 if(cmp&&cr){var setp=function(){cmp.style.setProperty('--p',cr.value+'%');};
  cr.addEventListener('input',setp);setp();}
 // ── три слова бренда ──
 var tabs=document.getElementById('rm-tabs');
 if(tabs){
  var btns=[].slice.call(tabs.querySelectorAll('.rm-tab'));
  btns.forEach(function(b){b.addEventListener('click',function(){
   var id=b.getAttribute('data-pane');
   btns.forEach(function(x){var on=(x===b);x.classList.toggle('is-on',on);
    x.setAttribute('aria-pressed',on?'true':'false');});
   [].forEach.call(document.querySelectorAll('.rm-pane'),function(p){
    p.classList.toggle('is-on',p.id==='rm-pane-'+id);});
  });});
 }
 // ── калькулятор инвестора ──
 var sum=document.getElementById('rm-sum'),yrs=document.getElementById('rm-years'),
     prog=document.getElementById('rm-prog');
 if(sum&&yrs&&prog){
  var rate=16.5, GROWTH=0.30;
  function fmt(n){return Math.round(n).toLocaleString('ru-RU');}
  function mln(n){return (Math.round(n*100)/100).toLocaleString('ru-RU',
   {minimumFractionDigits:2,maximumFractionDigits:2});}
  function fill(el){var min=+el.min,max=+el.max;
   el.style.setProperty('--f',((el.value-min)/(max-min)*100)+'%');}
  function calc(){
   var s=+sum.value*1e6, y=+yrs.value, year=s*rate/100;
   document.getElementById('rm-sum-v').textContent=(+sum.value).toLocaleString('ru-RU',
    {minimumFractionDigits:1,maximumFractionDigits:1});
   document.getElementById('rm-years-v').textContent=y;
   document.getElementById('rm-o-year').textContent=fmt(year)+' \\u20bd';
   document.getElementById('rm-o-month').textContent=fmt(year/12)+' \\u20bd';
   document.getElementById('rm-o-total').textContent=mln(year*y/1e6)+' \\u043c\\u043b\\u043d \\u20bd';
   document.getElementById('rm-o-asset').textContent=mln(s*(1+GROWTH)/1e6)+' \\u043c\\u043b\\u043d \\u20bd';
   fill(sum);fill(yrs);
  }
  [sum,yrs].forEach(function(el){el.addEventListener('input',calc);});
  [].forEach.call(prog.querySelectorAll('button'),function(b){
   b.addEventListener('click',function(){
    rate=+b.getAttribute('data-rate');
    [].forEach.call(prog.querySelectorAll('button'),function(x){
     var on=(x===b);x.classList.toggle('is-on',on);
     x.setAttribute('aria-pressed',on?'true':'false');});
    calc();});});
  calc();
 }
 // ── лайтбокс разворотов ──
 var lb=document.getElementById('rm-lb'),lbi=document.getElementById('rm-lb-img'),
     lbc=document.getElementById('rm-lb-cap'),lbx=document.getElementById('rm-lb-x');
 function open(src,cap,alt){lbi.src=src;lbi.alt=alt||'';lbc.textContent=cap||'';
  lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';lbx.focus();}
 function close(){lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');
  lbi.removeAttribute('src');document.body.style.overflow='';}
 [].forEach.call(document.querySelectorAll('.rm-zoom'),function(z){
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
 var els=[].slice.call(document.querySelectorAll('.rm-r'));
 function show(n){n.classList.add('is-in');}
 if(!('IntersectionObserver' in window)){els.forEach(show);return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){show(e.target);io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
 els.forEach(function(n){var r=n.getBoundingClientRect();
  if(r.top<innerHeight&&r.bottom>0)show(n);else io.observe(n);});
})();</script>"""

BREADCRUMB_LD = (
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
  '"itemListElement":[{"@type":"ListItem","position":1,"name":"Проекты","item":"https://hand-marketing.ru/project/"},'
  '{"@type":"ListItem","position":2,"name":"Creative & Design","item":"https://hand-marketing.ru/creativedesign/"},'
  '{"@type":"ListItem","position":3,"name":"Брошюра Ramada Encore",'
  f'"item":"{URL}"}}]}}</script>')


def build():
    # Отдельного CTA-блока нет: фиолетовая форма из rc.footer() уже закрывает страницу,
    # второй «Обсудить проект» был бы дублем (как на We&I, Vertical, CeramicaNova и OBO)
    body = (f'{rc.header()}<main class="rm">{hero()}{about()}{task()}{compare()}{craft()}'
            f'{credo()}{calc()}{book()}{rooms()}{printing()}{result()}</main>{LIGHTBOX}'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{PAGE_JS}{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    out = os.path.join(ROOT, 'creative', 'becar', 'ramada')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build())
    print('written', os.path.join(out, 'index.html'))
    # CI переименовывает index-a2.html в index.html, поэтому старый A2-файл надо убрать,
    # иначе он затрёт кастомную страницу прямо на деплое. Прежняя Tilda-версия остаётся
    # в истории git.
    a2 = os.path.join(out, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('removed', a2)
