#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерит mirror/video/saintgobain/training/index.html: кейс «Обучение
руководителей» для Saint-Gobain (ООО «Сен-Гобен Строительная Продукция Рус»).

Материал: два готовых ролика (467,3 с и 703,4 с), презентация на 28 экранов
и таблица структуры с дикторским текстом и репликами девяти диалогов.
Фактура вынута фактологом в scripts/a2/agent-out/sg-training/ (facts.json,
scenes.json, structure.md, slides.md), кадры и фрагменты режет
scripts/sgtraining-assets.py.

Полных роликов на странице нет и не должно быть: это внутреннее обучение
заказчика. На сайте лежат немой хайлайт первого экрана и пять коротких
фрагментов по темам, все внутри mirror/videos/.

Две механики страницы:
  • тренажёр «какой это вопрос»: настоящие формулировки из курса, посетитель
    относит вопрос к типу и получает разбор дикторским текстом плюс кадр
    того экрана, где это правило объясняют;
  • разметка стенограммы по STAR: реплики диалогов лежат текстом, кнопки
    S-T-A-R подсвечивают фразы внутри реплик; рядом слабый ответ с флагами,
    где счёт «мы» против «я» и возраст примера считаются по репликам.

Чего на странице нет сознательно: расхождений сценария с фактом, коридора
хронометража, склейки роликов и прочего разбора нашей кухни (урок /video/
saintgobain/cx). Цифры из диалогов подписаны как реплики игровых сцен,
а не как результаты Saint-Gobain.

Шрифты: Rubik (заголовки, интерфейс) + Alegreya Sans (реплики, италика для
второго голоса). У Rubik скруглены углы знаков, тем же радиусом скруглены
в роликах рамка окна живого кадра, плашка-комментарий и облако под флэт-
иллюстрацией.

Правки: ТОЛЬКО через этот скрипт, build_v1 страницу пропускает по маркеру
<!--custom-page-->. index-a2.html в каталоге кейса быть не должно."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', 'mirror'))
OUT = os.path.join(HERE, 'agent-out', 'sg-training')

spec = importlib.util.spec_from_file_location("rc", os.path.join(HERE, "react-chrome.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

FRAMES = {f['id']: f for f in json.load(open(os.path.join(OUT, 'frames.json'), encoding='utf-8'))}

METRIKA = '<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(71125393,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/71125393" style="position:absolute;left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'

IMG = '/images/sgtraining'
VID = '/videos'
URL = 'https://hand-marketing.ru/video/saintgobain/training/'
TITLE = 'Обучающие видео для руководителей Saint-Gobain | Hand Marketing'
DESCR = ('Курс обучающих видео для руководителей Saint-Gobain: интервью по '
         'компетенциям и модель STAR. 19,5 минут видео, 28 экранов моушн-графики '
         'и девять игровых сцен с актёрами.')

# ─── тренажёр: формулировки взяты со слайдов курса ─────────────────────────
# type → (название, роль: рабочий инструмент или то, что не задают)
TYPES = [
    ('open',    'Открытый',   'work', 'Основной инструмент. Заставляет кандидата рассказывать.'),
    ('closed',  'Закрытый',   'work', 'Вспомогательный. Проверяет факт, ответ да или нет.'),
    ('clarify', 'Уточняющий', 'work', 'Дополняет неполный ответ, бывает открытым и закрытым.'),
    ('leading', 'Наводящий',  'stop', 'Содержит ответ или оценку, кандидат просто соглашается.'),
    ('social',  'Социально ожидаемый', 'stop', 'Ответ известен заранее и ничего не проверяет.'),
    ('multi',   'Сложный',    'stop', 'Несколько вопросов сразу, кандидат ответит на один.'),
]

# вопрос, верный тип, разбор (дикторский текст, xlsx столбец E), кадр экрана,
# где это правило объясняют, и тайм-код этого экрана в ролике
QUIZ = [
    ('Какая задача перед вами стояла?', 'open',
     'Открытые вопросы это основной инструмент для получения информации. '
     'Начинаются со слов: какой, когда, как, сколько, что, чем, опишите ситуацию когда вы.',
     'g-open', 1, 60.0),
    ('У вас есть опыт работы с проектными институтами?', 'closed',
     'Закрытые вопросы нужны, чтобы быстро проверить информацию или подтвердить факты '
     'из резюме. Они предполагают односложный ответ. Это вспомогательный инструмент.',
     'g-closed', 1, 78.0),
    ('Правильно ли я поняла, что вы проводили обучения и шеф-монтажи?', 'clarify',
     'Уточняющие вопросы мы задаём, когда нам дали неполный ответ. '
     'Они могут быть открытого и закрытого вида.',
     'g-clarify', 1, 100.0),
    ('Вы проработали десять лет торговым представителем, неужели у вас не было амбиций '
     'стать руководителем?', 'leading',
     'Вопрос звучит так, как будто мы ставим под сомнение карьерный путь и достижения '
     'кандидата.',
     'g-leading', 1, 142.0),
    ('Вы неконфликтный человек?', 'social',
     'В этом случае кандидат даст правильный ответ, но это не означает, что он так поступит.',
     'g-social', 1, 163.0),
    ('Почему вы сейчас находитесь в поиске и по каким критериям выбираете работодателя?', 'multi',
     'Кандидат скорее всего ответит на один из вопросов. И вы получите неполную информацию.',
     'g-complex', 1, 182.0),
    ('В чём заключался ваш вклад в проекте?', 'clarify',
     'Уточняющие вопросы мы задаём для получения дополнительной информации, '
     'когда нам дали неполный ответ.',
     'g-clarify', 1, 100.0),
    ('Вы готовы к работе в режиме многозадачности?', 'social',
     'На интервью не следует задавать вопросы, предполагающие социально ожидаемые ответы.',
     'g-social', 1, 163.0),
]

# ─── цепочка сужения: диалог 6, реплики из xlsx E35 ────────────────────────
CHAIN = [
    ('q', 'open', 'Приведите пример сложных переговоров за последние два года. '
     'Что это была за ситуация? Какая у вас была цель?',
     'Широкий вопрос открывает тему и отдаёт слово кандидату.'),
    ('a', None, 'Месяц назад я вёл переговоры с главным инженером компании. '
     'Я поставил себе цель договориться о первой поставке на объект.', None),
    ('q', 'clarify', 'В чём была сложность переговоров?',
     'Уточняющий вопрос достаёт то, чего в ответе не было.'),
    ('a', None, 'Они привыкли использовать более дешёвый продукт конкурента, '
     'качество которого их устраивало. Преимущества нашего были неочевидны.', None),
    ('q', 'clarify', 'Как вы действовали, чтобы преодолеть эту сложность?',
     'Второе уточнение переводит разговор с обстоятельств на действия.'),
    ('a', None, 'Я проанализировал технические характеристики нашего продукта и продукта '
     'конкурента, доказал более низкий расход, предложил обучение для бригады. '
     'Главный инженер выбрал наш продукт.', None),
]

# ─── стенограмма: сильный ответ (диалог 6) размечен по STAR ────────────────
# роль: q вопрос интервьюера, a ответ кандидата. Метка = буква модели STAR.
STRONG = [
    ('q', None, 'Приведите, пожалуйста, пример сложных переговоров за последние два года. '
     'Что это была за ситуация? Какая у вас была цель? В чём заключалась сложность? '
     'Какие действия вы предпринимали? Какой был результат?'),
    ('a', 'S', 'Месяц назад я вёл переговоры с главным инженером компании «Строительная».'),
    ('a', 'T', 'Я поставил себе цель договориться о первой поставке на объект.'),
    ('a', 'S', 'Я знал их потребность в грунтовке, на десять тысяч квадратных метров.'),
    ('a', 'A', 'Я доказал, что наша грунтовка выгоднее, несмотря на то что она дороже.'),
    ('a', 'R', 'Мы сделали поставку на большую сумму.'),
    ('q', None, 'В чём была сложность переговоров?'),
    ('a', 'S', 'Они привыкли использовать более дешёвый продукт, использовали грунтовку '
     'конкурента, качество которой их устраивало. Преимущества нашего продукта '
     'для них были совсем неочевидны.'),
    ('q', None, 'Как вы действовали, чтобы преодолеть эту сложность в переговорах?'),
    ('a', 'A', 'Я детально проанализировал технические характеристики нашего продукта '
     'и продукта конкурента.'),
    ('a', 'A', 'Я доказал, что нашу грунтовку выгоднее использовать за счёт технологии '
     'нанесения и более низкого расхода, аргументировал преимущества, '
     'предложил обучение для бригады.'),
    ('a', 'R', 'После обучения и презентации продукта на объекте главный инженер выбрал '
     'наш продукт, и мы отгрузили фуру грунтовки.'),
    ('a', 'R', 'Нас порекомендовали, и мы запланировали переговоры с другой компанией.'),
]

# слабый ответ (диалог 5) с флагами разбора, формулировки флагов из слайда 22
FLAGS = [
    ('old',  'Пример не тех лет', 'Курс задаёт сквозной критерий: пример не старше двух лет.'),
    ('we',   'Говорит «мы»', 'Из ответа не видно, что делал сам кандидат.'),
    ('easy', 'Сложности нет', 'Преодолевать было нечего, оценивать нечего.'),
    ('role', 'Роль вспомогательная', 'Результат получен не действиями кандидата.'),
]
WEAK = [
    ('q', [], 'Приведите, пожалуйста, пример сложных переговоров за последние два года.'),
    ('a', ['old'], 'Я участвовала в сложных переговорах в начале моей карьеры, десять лет назад.'),
    ('q', [], 'Я прошу прощения, не могли бы привести пример за последние два года?'),
    ('a', ['we'], 'Такой пример тоже есть. Мы должны были зайти на крупный объект. '
     'Клиент хотел получить выгодную цену. В результате переговоров удалось договориться.'),
    ('q', [], 'За счёт чего вам удалось договориться?'),
    ('a', ['we'], 'Мы дали скидку, которую попросил клиент.'),
    ('q', [], 'А в чём была сложность переговоров?'),
    ('a', ['easy'], 'В целом сложностей не было.'),
    ('q', [], 'Кто вёл переговоры?'),
    ('a', ['role'], 'Я и мой руководитель.'),
    ('q', [], 'А в чём заключалась ваша роль?'),
    ('a', ['role'], 'Я организовала встречу.'),
]

# ─── галерея экранов курса ─────────────────────────────────────────────────
SCREENS = ['g-prep', 'g-open', 'g-closed', 'g-clarify', 'g-funnel', 'g-leading',
           'g-social', 'g-complex', 'g-personal', 'g-star', 'g-star-more',
           'g-partial', 'g-recap', 'g-final']

# ─── фрагменты по темам ────────────────────────────────────────────────────
CLIPS = {
    'closed': ('sgt-clip-closed', 'd1-wide', 'Закрытые вопросы в деле',
               'Первая сцена курса: три закрытых вопроса подряд и три ответа, '
               'после которых о кандидате по-прежнему ничего не известно.'),
    'open': ('sgt-clip-open', 'd4-wide', 'Открытый вопрос в деле',
             'Тот же формат сцены, другой инструмент: один открытый вопрос '
             'и конкретный ответ про навыки и планы.'),
    'star': ('sgt-clip-star', 'g-star', 'Как собирается модель STAR',
             'Полминуты моушн-графики: буквы встают столбцом, к каждой выезжает '
             'расшифровка и пример вопроса.'),
    'weak': ('sgt-clip-weak', 'd5-wide', 'Пример не тех лет',
             'Кандидат уходит на десять лет назад, интервьюер возвращает разговор '
             'в нужные два года.'),
    'interrupt': ('sgt-clip-interrupt', 'd9-wide', 'Как вежливо перебить',
                  'Самая длинная сцена курса: интервьюер дважды останавливает '
                  'кандидата и оба раза оставляет разговор в рабочем тоне.'),
}


CSS = """<style id="sgt-css">
.sgt{--ink:#1B2430;--dim:#59636F;--line:#D2D6D8;--paper:#F4F4F2;--screen:#DCDCDC;
 --white:#fff;--orange:#E06428;--red:#D81C40;--blue:#204880;--teal:#48A4A0;
 --mint:#E4FCF8;--wa:#00A282;--wb:#347892;--wc:#F46C54;--r:10px;
 font-family:'Alegreya Sans','Rubik',-apple-system,Arial,sans-serif;
 color:var(--ink);background:var(--paper);overflow-x:hidden;font-size:17px}
.sgt *{box-sizing:border-box}
.sgt h1,.sgt h2,.sgt h3,.sgt .ui,.sgt button{font-family:'Rubik','Alegreya Sans',Arial,sans-serif}
.sgt a:focus-visible,.sgt button:focus-visible{outline:3px solid var(--blue);outline-offset:3px;border-radius:6px}
.sgt__in{max-width:1180px;margin:0 auto;padding:0 32px}
.sgt section{padding:88px 0}
.sgt .kicker{font-family:'Rubik',Arial,sans-serif;font-size:12px;letter-spacing:.14em;
 text-transform:uppercase;font-weight:700;color:var(--teal);margin:0 0 14px}
/* заголовок экранов курса: оранжевый капс сверху, бирюзовый подзаголовок под ним */
.sgt h2{font-size:clamp(26px,3.3vw,42px);line-height:1.06;font-weight:800;letter-spacing:-.01em;
 text-transform:uppercase;color:var(--orange);margin:0 0 18px}
.sgt h3{font-size:19px;font-weight:600;margin:0 0 10px;line-height:1.25}
.sgt p{line-height:1.62;margin:0 0 16px}
.sgt .lead{font-size:19px;line-height:1.66;color:var(--dim);max-width:64ch}
.sgt .rev{opacity:0;transform:translateY(20px);transition:opacity .7s ease,transform .7s ease}
.sgt .rev.on{opacity:1;transform:none}
.sgt figure{margin:0}
.sgt img{display:block;max-width:100%;height:auto;border-radius:var(--r)}
.sgt figcaption{font-size:14px;color:var(--dim);margin-top:10px;line-height:1.45}

/* ── шторка из трёх полос: фирменный переход ролика, 14 срабатываний ──── */
.sgt-wipe{height:10px;display:flex;gap:0;margin:0}
.sgt-wipe i{flex:1 1 33.33%}
.sgt-wipe i:nth-child(1){background:var(--wa)}
.sgt-wipe i:nth-child(2){background:var(--wb)}
.sgt-wipe i:nth-child(3){background:var(--wc)}

/* ── первый экран ─────────────────────────────────────────────────────── */
.sgt-hero{background:var(--screen);padding:64px 0 72px}
.sgt-hero__in{max-width:1180px;margin:0 auto;padding:0 32px;display:grid;
 grid-template-columns:minmax(0,1fr) minmax(0,1.02fr);gap:48px;align-items:center}
.sgt-hero__brand{display:flex;align-items:center;gap:12px;margin:0 0 22px}
.sgt-hero__brand b{font-family:'Rubik',Arial,sans-serif;font-size:12px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--blue);font-weight:700}
.sgt-hero__brand span{height:1px;flex:1;background:var(--blue);opacity:.3;max-width:120px}
.sgt-hero h1{font-family:'Rubik',Arial,sans-serif;font-size:clamp(30px,4.1vw,52px);line-height:1.03;
 font-weight:800;letter-spacing:-.02em;margin:0;text-transform:uppercase;color:var(--orange)}
.sgt-hero h1 em{font-style:normal;display:block;color:var(--teal);font-size:.52em;
 letter-spacing:.02em;margin-top:14px;line-height:1.18}
.sgt-hero__sub{margin:24px 0 0;font-size:18px;line-height:1.6;color:#3A4450;max-width:46ch}
.sgt-hero__meta{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0 0;padding:0;list-style:none}
.sgt-hero__meta li{font-family:'Rubik',Arial,sans-serif;font-size:13px;font-weight:500;
 background:var(--white);border-radius:99px;padding:8px 15px;color:var(--blue)}
/* окно живого кадра: рамка со скруглением, как в самом ролике */
.sgt-hero__win{position:relative;border-radius:var(--r);overflow:hidden;
 box-shadow:0 18px 44px rgba(27,36,48,.18)}
.sgt-hero__win video,.sgt-hero__win img{width:100%;display:block;border-radius:0}
.sgt-hero__tag{position:absolute;left:0;bottom:0;right:0;padding:14px 18px;
 background:linear-gradient(90deg,rgba(32,72,128,.94),rgba(72,164,160,.92));
 color:#fff;font-family:'Rubik',Arial,sans-serif;font-size:13px;line-height:1.35}

/* ── цифры работы ─────────────────────────────────────────────────────── */
.sgt-nums{background:var(--white)}
.sgt-nums__grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;margin-top:34px}
.sgt-nums__c{background:var(--paper);border-radius:var(--r);padding:22px 20px}
.sgt-nums__c b{display:block;font-family:'Rubik',Arial,sans-serif;font-size:34px;font-weight:800;
 color:var(--blue);line-height:1;letter-spacing:-.02em}
.sgt-nums__c span{display:block;margin-top:10px;font-size:15px;color:var(--dim);line-height:1.4}

/* ── три слоя курса ───────────────────────────────────────────────────── */
.sgt-layers{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:38px}
.sgt-layer{background:var(--white);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column}
.sgt-layer img{border-radius:0}
.sgt-layer__t{padding:20px 22px 24px}
.sgt-layer__t b{display:block;font-family:'Rubik',Arial,sans-serif;font-size:12px;
 letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px}
.sgt-layer:nth-child(1) .sgt-layer__t b{color:var(--teal)}
.sgt-layer:nth-child(2) .sgt-layer__t b{color:var(--orange)}
.sgt-layer:nth-child(3) .sgt-layer__t b{color:var(--blue)}
.sgt-layer__t p{font-size:16px;margin:0;color:#39424E}

/* ── фрагмент ролика ──────────────────────────────────────────────────── */
.sgt-clip{background:var(--white);border-radius:var(--r);overflow:hidden}
.sgt-clip__v{position:relative;background:#0E1620;aspect-ratio:16/9}
.sgt-clip__v video{width:100%;height:100%;display:block;object-fit:cover;border-radius:0}
.sgt-clip__poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 border-radius:0;transition:opacity .35s ease}
.sgt-clip.is-on .sgt-clip__poster{opacity:0;pointer-events:none}
.sgt-clip__play{position:absolute;inset:0;width:100%;height:100%;border:0;cursor:pointer;
 background:rgba(14,22,32,.18);display:flex;align-items:center;justify-content:center;
 transition:background .3s ease}
.sgt-clip__play:hover{background:rgba(14,22,32,.32)}
.sgt-clip.is-on .sgt-clip__play{display:none}
.sgt-clip__play i{width:66px;height:66px;border-radius:50%;background:var(--orange);
 display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px rgba(14,22,32,.35)}
.sgt-clip__play i::after{content:'';border-left:19px solid #fff;border-top:12px solid transparent;
 border-bottom:12px solid transparent;margin-left:5px}
.sgt-clip__t{padding:18px 22px 22px}
.sgt-clip__t b{display:block;font-family:'Rubik',Arial,sans-serif;font-size:17px;font-weight:600;
 margin-bottom:8px}
.sgt-clip__t p{font-size:15.5px;color:var(--dim);margin:0}
.sgt-clip__t span{display:inline-block;margin-top:10px;font-family:'Rubik',Arial,sans-serif;
 font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--teal)}

/* ── тренажёр вопросов ────────────────────────────────────────────────── */
.sgt-quiz{background:var(--white)}
.sgt-quiz__box{margin-top:36px;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);
 gap:32px;align-items:start}
.sgt-quiz__q{background:var(--screen);border-radius:var(--r);padding:30px 32px}
.sgt-quiz__count{font-family:'Rubik',Arial,sans-serif;font-size:12px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--dim);margin:0 0 10px}
.sgt-quiz__bar{height:4px;border-radius:99px;background:#C9CDCE;overflow:hidden;margin:0 0 20px}
.sgt-quiz__bar i{display:block;height:100%;background:var(--blue);border-radius:99px;
 transition:width .35s ease}
.sgt-quiz__text{font-size:clamp(20px,2.2vw,27px);line-height:1.32;font-weight:500;margin:0;
 min-height:2.6em}
.sgt-quiz__btns{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;
 margin-top:24px}
.sgt-quiz__btns button{font-family:'Rubik',Arial,sans-serif;font-size:14px;font-weight:500;
 border:1.5px solid var(--blue);background:#fff;color:var(--blue);border-radius:99px;
 padding:11px 16px;cursor:pointer;display:flex;align-items:center;gap:8px;
 text-align:left;line-height:1.2;min-height:46px;
 transition:background .18s ease,color .18s ease,border-color .18s ease,opacity .18s ease}
.sgt-quiz__btns button::before{content:'';width:16px;height:16px;border-radius:50%;
 border:1.5px solid currentColor;opacity:.45;flex:none;
 display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;
 line-height:1}
.sgt-quiz__btns button:hover:not(:disabled){background:var(--blue);color:#fff}
/* после ответа: верный всегда зелёный с галочкой, выбранный неверный красный
   с крестиком, остальные гаснут — чтобы взгляд не разбирал четыре состояния */
.sgt-quiz__btns button.is-right{background:var(--wa);border-color:var(--wa);color:#fff;
 opacity:1}
.sgt-quiz__btns button.is-right::before{content:'✓';border-color:#fff;opacity:1;
 background:rgba(255,255,255,.18)}
.sgt-quiz__btns button.is-picked{background:var(--red);border-color:var(--red);color:#fff;
 opacity:1}
.sgt-quiz__btns button.is-picked::before{content:'✕';border-color:#fff;opacity:1;
 background:rgba(255,255,255,.18)}
.sgt-quiz__btns button.is-dim{border-color:#CBD1D4;color:#8E979F;background:#fff;opacity:.55}
.sgt-quiz__btns button.is-dim::before{opacity:.25}
.sgt-quiz__btns button:disabled{cursor:default}
/* вердикт: одна строка, которую видно раньше, чем разбор */
.sgt-quiz__verdict{display:flex;gap:12px;align-items:flex-start;margin:22px 0 0;
 border-radius:10px;padding:14px 18px;font-size:16px;line-height:1.45;
 font-family:'Rubik',Arial,sans-serif}
.sgt-quiz__verdict[hidden]{display:none}
.sgt-quiz__verdict i{flex:none;width:24px;height:24px;border-radius:50%;color:#fff;
 display:flex;align-items:center;justify-content:center;font-size:14px;font-style:normal;
 font-weight:700}
.sgt-quiz__verdict b{font-weight:600}
.sgt-quiz__verdict.is-ok{background:#E3F6F0;color:#0B5F4E;box-shadow:inset 3px 0 0 var(--wa)}
.sgt-quiz__verdict.is-ok i{background:var(--wa)}
.sgt-quiz__verdict.is-no{background:#FCE7EC;color:#8E1230;box-shadow:inset 3px 0 0 var(--red)}
.sgt-quiz__verdict.is-no i{background:var(--red)}
.sgt-quiz__ans{background:var(--blue);color:#fff;border-radius:var(--r);padding:26px 28px}
.sgt-quiz__ans b{display:block;font-family:'Rubik',Arial,sans-serif;font-size:12px;
 letter-spacing:.12em;text-transform:uppercase;color:#9FD4CF;margin-bottom:12px}
.sgt-quiz__ans p{font-size:16.5px;line-height:1.58;margin:0 0 16px;color:#E9F1F7}
.sgt-quiz__ans img{border-radius:8px;margin-top:6px}
.sgt-quiz__ans figcaption{color:#9FB4CC;font-size:13px}
.sgt-quiz__hint{color:#96A0AA;font-size:15px}
.sgt-quiz__next{margin-top:20px;font-family:'Rubik',Arial,sans-serif;font-size:15px;font-weight:500;
 background:var(--orange);color:#fff;border:0;border-radius:99px;padding:12px 24px;cursor:pointer;
 display:inline-flex;align-items:center;gap:10px}
.sgt-quiz__next::after{content:'→'}
.sgt-quiz__next:hover{background:#C8551F}
.sgt-quiz__next[hidden]{display:none}
.sgt-quiz__legend{display:flex;flex-wrap:wrap;gap:18px;margin-top:26px;padding:0;list-style:none}
.sgt-quiz__legend li{font-size:15px;color:var(--dim);max-width:30ch}
.sgt-quiz__legend b{font-family:'Rubik',Arial,sans-serif;font-size:14px;color:var(--ink);
 display:block;margin-bottom:3px}

/* ── цепочка сужения ──────────────────────────────────────────────────── */
.sgt-chain{display:grid;gap:14px;margin-top:36px}
.sgt-chain__row{display:grid;grid-template-columns:132px minmax(0,1fr);gap:20px;align-items:start}
.sgt-chain__tag{font-family:'Rubik',Arial,sans-serif;font-size:12px;letter-spacing:.1em;
 text-transform:uppercase;font-weight:500;padding:7px 12px;border-radius:99px;text-align:center;
 color:#fff;background:var(--teal)}
.sgt-chain__row[data-kind="a"] .sgt-chain__tag{background:transparent;color:var(--dim);
 border:1px solid var(--line)}
.sgt-chain__body{background:var(--white);border-radius:var(--r);padding:18px 22px}
.sgt-chain__row[data-kind="a"] .sgt-chain__body{background:transparent;
 border:1px dashed var(--line);font-style:italic;color:#3E4854}
.sgt-chain__body p{margin:0;font-size:17px}
.sgt-chain__body small{display:block;margin-top:9px;font-size:14px;color:var(--dim);font-style:normal}
.sgt-chain__row+.sgt-chain__row{position:relative}

/* ── стенограмма по STAR ──────────────────────────────────────────────── */
.sgt-star{background:var(--white)}
.sgt-star__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:34px;margin-top:36px;
 align-items:start}
.sgt-doc{background:var(--paper);border-radius:var(--r);padding:28px 28px 32px}
.sgt-doc__h{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:6px}
.sgt-doc__h b{font-family:'Rubik',Arial,sans-serif;font-size:19px;font-weight:600}
.sgt-doc__h span{font-size:14px;color:var(--dim)}
.sgt-doc__note{font-size:15.5px;color:var(--dim);margin:0 0 20px}
.sgt-keys{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px;padding:0;list-style:none}
.sgt-keys button{font-family:'Rubik',Arial,sans-serif;font-size:14px;font-weight:500;cursor:pointer;
 border-radius:8px;border:1.5px solid var(--line);background:var(--white);color:var(--ink);
 padding:9px 14px;transition:all .2s ease;display:flex;gap:9px;align-items:baseline}
.sgt-keys button i{font-style:normal;font-weight:700;font-size:15px}
.sgt-keys button small{font-size:12.5px;color:var(--dim);letter-spacing:.04em}
.sgt-keys button:hover{border-color:var(--blue)}
.sgt-keys button.is-on{background:var(--blue);border-color:var(--blue);color:#fff}
.sgt-keys button.is-on small{color:#B9CCE2}
.sgt-doc[data-doc="weak"] .sgt-keys button.is-on{background:var(--red);border-color:var(--red)}
.sgt-line{margin:0 0 14px;display:grid;grid-template-columns:104px minmax(0,1fr);gap:16px;
 align-items:start}
.sgt-line__who{font-family:'Rubik',Arial,sans-serif;font-size:12px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--dim);padding-top:4px}
.sgt-line__txt{font-size:16.5px;line-height:1.56;border-radius:8px;padding:6px 10px;
 margin-left:-10px;transition:background .25s ease,color .25s ease,box-shadow .25s ease}
.sgt-line[data-who="a"] .sgt-line__txt{font-style:italic}
.sgt-line[data-who="a"] .sgt-line__who{color:var(--teal)}
.sgt-doc.is-marking .sgt-line__txt{color:#98A1AA}
.sgt-doc.is-marking .sgt-line.is-hit .sgt-line__txt{color:var(--ink);background:var(--mint);
 box-shadow:inset 3px 0 0 var(--teal)}
.sgt-doc[data-doc="weak"].is-marking .sgt-line.is-hit .sgt-line__txt{background:#FCE8EC;
 box-shadow:inset 3px 0 0 var(--red)}
.sgt-line__mark{display:inline-block;font-family:'Rubik',Arial,sans-serif;font-size:11px;
 font-weight:700;letter-spacing:.06em;color:#fff;background:var(--blue);border-radius:5px;
 padding:2px 7px;margin-left:8px;vertical-align:1px;opacity:0;transition:opacity .25s ease}
.sgt-doc.is-marking .sgt-line.is-hit .sgt-line__mark{opacity:1}
.sgt-doc[data-doc="weak"] .sgt-line__mark{background:var(--red)}
.sgt-doc__sum{margin:22px 0 0;padding:16px 18px;background:var(--white);border-radius:8px;
 font-size:15.5px;color:var(--dim);line-height:1.5}
.sgt-doc__sum b{color:var(--ink)}
.sgt-star__foot{margin-top:30px;font-size:16px;color:var(--dim);max-width:74ch}

/* ── съёмка ───────────────────────────────────────────────────────────── */
.sgt-shoot__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:36px}
.sgt-shoot__grid figure:first-child{grid-column:span 2}
.sgt-set{margin-top:44px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);
 gap:36px;align-items:center;background:var(--white);border-radius:var(--r);padding:32px}
.sgt-set__list{margin:16px 0 0;padding:0;list-style:none}
.sgt-set__list li{display:grid;grid-template-columns:26px minmax(0,1fr);gap:12px;
 padding:11px 0;border-top:1px solid var(--line);font-size:16px;line-height:1.45}
.sgt-set__list li b{font-family:'Rubik',Arial,sans-serif;color:var(--orange);font-weight:700}
.sgt-dlg{display:flex;flex-wrap:wrap;gap:6px;margin-top:22px;padding:0;list-style:none}
.sgt-dlg li{font-family:'Rubik',Arial,sans-serif;font-size:12.5px;color:var(--blue);
 background:var(--mint);border-radius:6px;padding:6px 10px}

/* ── экраны курса ─────────────────────────────────────────────────────── */
.sgt-screens{background:var(--screen)}
.sgt-screens__grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:36px}
.sgt-screens__grid figure{background:var(--white);border-radius:var(--r);overflow:hidden}
.sgt-screens__grid img{border-radius:0}
.sgt-screens__grid figcaption{padding:12px 14px 15px;font-size:13.5px;margin:0}
.sgt-craft{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin-top:34px}
.sgt-craft__c{background:var(--white);border-radius:var(--r);padding:24px}
.sgt-craft__c b{display:block;font-family:'Rubik',Arial,sans-serif;font-size:16px;margin-bottom:8px}
.sgt-craft__c p{font-size:15.5px;color:var(--dim);margin:0}
.sgt-craft__c img{margin-bottom:16px}
.sgt-craft__bars{display:flex;height:56px;border-radius:8px;overflow:hidden;margin-bottom:16px}
.sgt-craft__bars i{flex:1}
.sgt-craft__bars i:nth-child(1){background:var(--wa)}
.sgt-craft__bars i:nth-child(2){background:var(--wb)}
.sgt-craft__bars i:nth-child(3){background:var(--wc)}

/* ── итог ─────────────────────────────────────────────────────────────── */
.sgt-done{background:var(--blue);color:#fff}
.sgt-done h2{color:#fff}
.sgt-done .kicker{color:#8FD0CA}
.sgt-done p{color:#D5E2EE;font-size:18px;line-height:1.65;max-width:66ch}
.sgt-done__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin-top:36px}
.sgt-done__c{background:rgba(255,255,255,.08);border-radius:var(--r);padding:24px}
.sgt-done__c b{display:block;font-family:'Rubik',Arial,sans-serif;font-size:15px;margin-bottom:8px;
 color:#fff}
.sgt-done__c span{font-size:15.5px;color:#C5D6E6;line-height:1.5}

/* ── адаптив ──────────────────────────────────────────────────────────── */
@media (max-width:1080px){
 .sgt-screens__grid{grid-template-columns:repeat(3,minmax(0,1fr))}
}
@media (max-width:900px){
 .sgt section{padding:64px 0}
 .sgt__in,.sgt-hero__in{padding:0 22px}
 .sgt-hero{padding:44px 0 52px}
 .sgt-hero__in{grid-template-columns:minmax(0,1fr);gap:32px}
 .sgt-nums__grid{grid-template-columns:repeat(2,minmax(0,1fr))}
 .sgt-layers,.sgt-craft,.sgt-done__grid{grid-template-columns:minmax(0,1fr)}
 .sgt-quiz__box,.sgt-star__grid,.sgt-set{grid-template-columns:minmax(0,1fr);gap:24px}
 .sgt-quiz__btns{grid-template-columns:repeat(2,minmax(0,1fr))}
 .sgt-shoot__grid{grid-template-columns:repeat(2,minmax(0,1fr))}
 .sgt-shoot__grid figure:first-child{grid-column:span 2}
}
@media (max-width:620px){
 .sgt{font-size:16px}
 .sgt section{padding:52px 0}
 .sgt-screens__grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
 .sgt-chain__row{grid-template-columns:minmax(0,1fr);gap:8px}
 .sgt-chain__tag{justify-self:start}
 .sgt-line{grid-template-columns:minmax(0,1fr);gap:4px}
 .sgt-line__who{padding-top:0}
 .sgt-doc{padding:22px 18px 26px}
 .sgt-quiz__q{padding:22px 20px}
 .sgt-quiz__btns{grid-template-columns:minmax(0,1fr)}
 .sgt-set{padding:22px 18px}
 .sgt-shoot__grid{grid-template-columns:minmax(0,1fr)}
 .sgt-shoot__grid figure:first-child{grid-column:auto}
 .sgt-hero__meta li{font-size:12px;padding:7px 12px}
}
/* телефон в ландшафте: высота маленькая, поэтому первый экран не тянем */
@media (max-height:520px) and (orientation:landscape){
 .sgt-hero{padding:32px 0 36px}
 .sgt section{padding:44px 0}
}
</style>"""


def img(fid, cls='', width=1120):
    """Кадр из ролика: 2 ширины, подпись берётся из frames.json."""
    f = FRAMES[fid]
    small = f'{IMG}/{fid}@560.jpg'
    return (f'<img src="{IMG}/{fid}.jpg" srcset="{small} 560w, {IMG}/{fid}.jpg 1120w" '
            f'sizes="(max-width:620px) 92vw, {width}px" loading="lazy" decoding="async" '
            f'width="1120" height="630" alt="{f["caption"]}"{f" class={cls}" if cls else ""}>')


def figure(fid):
    return f'<figure class="rev">{img(fid)}<figcaption>{FRAMES[fid]["caption"]}</figcaption></figure>'


def wipe():
    return '<div class="sgt-wipe" aria-hidden="true"><i></i><i></i><i></i></div>'


def hero():
    return f'''<header class="sgt-hero"><div class="sgt-hero__in">
<div><div class="sgt-hero__brand"><b>Saint-Gobain</b><span></span></div>
<h1>Курс для руководителей<em>Интервью по компетенциям и модель STAR</em></h1>
<p class="sgt-hero__sub">Компания хотела, чтобы руководитель приходил на интервью
подготовленным и умел разбирать ответы сам, а не оставлял оценку рекрутеру.
Мы сняли курс: правила на экране, живые сцены с актёрами и разбор каждой сцены.</p>
<ul class="sgt-hero__meta"><li>19 минут 30 секунд</li><li>28 экранов графики</li>
<li>9 игровых сцен</li><li>4 актёра</li></ul></div>
<div class="sgt-hero__win"><video src="{VID}/sgt-hero-loop.mp4" poster="{IMG}/d6-wide.jpg"
 autoplay muted loop playsinline preload="metadata" width="960" height="540"
 aria-label="Кадры курса: переговорная, экраны графики и модель STAR"></video>
<div class="sgt-hero__tag">Кадры курса. Полностью ролики остаются внутри компании:
это обучение сотрудников</div></div></div></header>'''


def nums():
    rows = [('19:30', 'готового видео в двух частях: виды вопросов и модель STAR'),
            ('28', 'экранов моушн-графики, нарисованных под курс с нуля'),
            ('9', 'игровых сцен с разбором, 8 минут 46 секунд чистой съёмки'),
            ('4', 'актёра, одна переговорная, три плана на каждую сцену')]
    cards = ''.join(f'<div class="sgt-nums__c rev"><b>{a}</b><span>{b}</span></div>'
                    for a, b in rows)
    return f'''<section class="sgt-nums"><div class="sgt__in">
<p class="kicker">Что сделали</p>
<h2>Учебный фильм, а не запись лекции</h2>
<p class="lead">Материал заказчика это методика найма: виды вопросов, воронка,
модель STAR и работа с неполным ответом. Мы разложили её на три слоя, которые
чередуются весь курс, чтобы правило сразу проверялось на живом примере.</p>
<div class="sgt-nums__grid">{cards}</div></div></section>'''


def layers():
    return f'''<section><div class="sgt__in">
<p class="kicker">Устройство курса</p>
<h2>Правило, сцена, разбор</h2>
<p class="lead">Каждая тема проходит один и тот же путь. Сначала правило на экране,
затем сцена в переговорной, где интервьюер это правило соблюдает или нарушает,
и сразу за ней разбор поверх кадра той же сцены.</p>
<div class="sgt-layers">
<div class="sgt-layer rev">{img('g-clarify', width=380)}<div class="sgt-layer__t">
<b>Слой 1. Правило</b><p>Экран с формулировкой и примерами вопросов. Из таких экранов
собраны 7 минут курса, это 36 процентов хронометража.</p></div></div>
<div class="sgt-layer rev">{img('d2-wide', width=380)}<div class="sgt-layer__t">
<b>Слой 2. Сцена</b><p>Интервьюер и кандидат в переговорной. Девять сцен, в каждой
общий план и два крупных, реплики написаны под конкретную ошибку или приём.</p></div></div>
<div class="sgt-layer rev">{img('c-d6', width=380)}<div class="sgt-layer__t">
<b>Слой 3. Разбор</b><p>Кадр сцены уезжает в окно, поверх выходит плашка с выводом.
Девять разборов, по одному на сцену.</p></div></div>
</div></div></section>'''


def clip(key, extra=''):
    name, poster, title, text = CLIPS[key]
    return f'''<div class="sgt-clip rev" data-clip>
<div class="sgt-clip__v"><video src="{VID}/{name}.mp4" preload="none"
 poster="{IMG}/{poster}.jpg" playsinline controls width="960" height="540"
 aria-label="{title}"></video>
<img class="sgt-clip__poster" src="{IMG}/{poster}.jpg" alt="" loading="lazy" decoding="async"
 width="1120" height="630">
<button class="sgt-clip__play" type="button" aria-label="Смотреть фрагмент: {title}">
<i aria-hidden="true"></i></button></div>
<div class="sgt-clip__t"><b>{title}</b><p>{text}</p>{extra}</div></div>'''


def quiz():
    btns = ''.join(
        f'<button type="button" data-t="{code}" data-role="{role}">{name}</button>'
        for code, name, role, _ in TYPES)
    legend = ''.join(f'<li><b>{name}</b>{note}</li>' for _, name, _, note in TYPES)
    return f'''<section class="sgt-quiz" id="trainer"><div class="sgt__in">
<p class="kicker">Первая часть курса</p>
<h2>Вопрос решает всё</h2>
<p class="lead">Курс учит различать шесть видов вопросов: три работают на оценку,
три только кажутся вопросами. Формулировки ниже взяты с экранов курса, а разбор это
дикторский текст, который звучит в ролике. Попробуйте определить вид сами.</p>
<div class="sgt-quiz__box">
<div class="sgt-quiz__q">
<p class="sgt-quiz__count ui" data-count></p>
<div class="sgt-quiz__bar" aria-hidden="true"><i data-bar style="width:0"></i></div>
<p class="sgt-quiz__text" data-question></p>
<div class="sgt-quiz__btns" data-btns role="group"
 aria-label="Выберите вид вопроса">{btns}</div>
<p class="sgt-quiz__verdict" data-verdict hidden role="status" aria-live="polite"></p>
<button class="sgt-quiz__next" type="button" data-next hidden>Следующий вопрос</button>
</div>
<figure class="sgt-quiz__ans" data-answer>
<b>Разбор из курса</b>
<p class="sgt-quiz__hint" data-hint>Выберите вид вопроса, и здесь появится объяснение
из ролика и кадр экрана, на котором это правило разбирают.</p>
<div data-answer-body hidden></div>
</figure>
</div>
<ul class="sgt-quiz__legend">{legend}</ul>
</div></section>'''


def chain():
    rows = ''
    for kind, tag, text, note in CHAIN:
        label = {'open': 'Открытый', 'clarify': 'Уточняющий'}.get(tag, 'Ответ')
        body = f'<p>{text}</p>' + (f'<small>{note}</small>' if note else '')
        rows += (f'<div class="sgt-chain__row rev" data-kind="{kind}">'
                 f'<div class="sgt-chain__tag ui">{label}</div>'
                 f'<div class="sgt-chain__body">{body}</div></div>')
    return f'''<section><div class="sgt__in">
<p class="kicker">Воронка вопросов</p>
<h2>Как разговор сужается до факта</h2>
<p class="lead">В курсе это называют воронкой: начинаем с открытого вопроса, дальше
достаём недостающее уточняющими. Ниже реальная цепочка из шестой сцены, реплики
сокращены по репликам сценария.</p>
<div class="sgt-chain">{rows}</div>
</div></section>'''


SCENE_LEN = [(1, '19 с'), (2, '55 с'), (3, '5,5 с'), (4, '19 с'), (5, '62 с'),
             (6, '95 с'), (7, '94 с'), (8, '57 с'), (9, '118 с')]

STAR_KEYS = [('S', 'Ситуация', 'что и как происходило'),
             ('T', 'Задача', 'что нужно было сделать'),
             ('A', 'Действия', 'что делал кандидат'),
             ('R', 'Результат', 'к чему всё привело')]


def count_first_person(lines, who='a'):
    """Сколько раз кандидат говорит «я» в своих репликах. Считается по тексту,
    который стоит на странице, поэтому цифру можно проверить глазами."""
    import re as _re
    n = 0
    for row in lines:
        if row[0] != who:
            continue
        n += len(_re.findall(r'(?<![а-яё])я(?![а-яё])', row[2].lower()))
    return n


def doc(kind, lines, keys, head, sub, note, summary):
    """Документ стенограммы: реплики текстом, кнопки сверху подсвечивают фразы.

    keys — список (код, название). Для сильного ответа код это буква модели
    и она печатается на кнопке; для слабого коды служебные, на кнопке только
    название флага."""
    labels = dict(keys)
    ks = ''
    for code, name in keys:
        letter = f'<i>{code}</i>' if len(code) == 1 else ''
        ks += (f'<button type="button" data-key="{code}">{letter}'
               f'<small>{name}</small></button>')
    body = ''
    for who, mark, text in lines:
        marks = mark if isinstance(mark, list) else ([mark] if mark else [])
        label = 'Интервьюер' if who == 'q' else 'Кандидат'
        badge = (f'<span class="sgt-line__mark">{labels.get(marks[0], marks[0])}</span>'
                 if marks else '')
        body += (f'<p class="sgt-line" data-who="{who}" data-marks="{" ".join(marks)}">'
                 f'<span class="sgt-line__who">{label}</span>'
                 f'<span class="sgt-line__txt">{text}{badge}</span></p>')
    return f'''<div class="sgt-doc rev" data-doc="{kind}">
<div class="sgt-doc__h"><b>{head}</b><span>{sub}</span></div>
<p class="sgt-doc__note">{note}</p>
<div class="sgt-keys">{ks}</div>
<div data-lines>{body}</div>
<p class="sgt-doc__sum">{summary}</p></div>'''


def star():
    strong_i = count_first_person(STRONG)
    weak_i = count_first_person(WEAK)
    strong = doc(
        'strong', STRONG, [(k, name) for k, name, _ in STAR_KEYS],
        'Шестая сцена', 'сильный ответ, 95 секунд',
        'Нажмите букву модели, и подсветятся фразы, которые её закрывают.',
        f'Кандидат говорит «я» {strong_i} раз и каждый раз про своё действие. '
        'Все четыре буквы закрыты, ответ можно оценивать.')
    weak = doc(
        'weak', WEAK, [(code, name) for code, name, _ in FLAGS],
        'Пятая сцена', 'слабый ответ, 62 секунды',
        'Те же кнопки, но здесь они показывают, что мешает поставить оценку.',
        f'Кандидат говорит «я» {weak_i} раза, и ни разу это не про сами переговоры: '
        'участвовала, была на встрече с руководителем, организовала встречу. '
        'Оценивать нечего, нужен другой пример.')
    legend = ''.join(f'<li><b>{name}</b>{note}</li>' for _, name, note in FLAGS)
    return f'''<section class="sgt-star" id="star"><div class="sgt__in">
<p class="kicker">Вторая часть курса</p>
<h2>Модель STAR на живых ответах</h2>
<p class="lead">Вторая часть учит разбирать ответ по четырём буквам: ситуация, задача,
действия, результат. Мы сняли две сцены на один и тот же вопрос про сложные переговоры.
Ниже их реплики, как они написаны в сценарии и звучат в кадре.</p>
<div class="sgt-star__grid">{strong}{weak}</div>
<ul class="sgt-quiz__legend">{legend}</ul>
<p class="sgt-star__foot">Цифры в репликах, десять тысяч квадратных метров грунтовки
и рост продаж на тридцать процентов, это текст учебных сцен, а не показатели компании.</p>
</div></section>'''


def clips_row():
    return f'''<section><div class="sgt__in">
<p class="kicker">Фрагменты</p>
<h2>Как это выглядит в кадре</h2>
<p class="lead">Полностью ролики остаются внутри компании. Здесь пять коротких
фрагментов, по одному на приём: две сцены с вопросами, разбор неудачного примера,
работа интервьюера с длинным ответом и кусок моушн-графики.</p>
<div class="sgt-layers">{clip('closed')}{clip('open')}{clip('star')}</div>
<div class="sgt-layers" style="margin-top:24px">{clip('weak')}{clip('interrupt')}</div>
</div></section>'''


def shoot():
    grid = ''.join(figure(f) for f in ['d9-wide', 'd6-b', 'd1-b', 'd4-a', 'd8-b',
                                       'd7-b', 'd2-b'])
    dlg = ''.join(f'<li>Сцена {i} · {d}</li>' for i, d in SCENE_LEN)
    return f'''<section><div class="sgt__in">
<p class="kicker">Съёмка</p>
<h2>Одна переговорная, девять сцен</h2>
<p class="lead">Всё снято в одном интерьере: белая стена со знаком компании,
красное и жёлтое кресла напротив друг друга. Смена планов держит внимание там,
где по сути идёт разговор двух людей на одном месте.</p>
<div class="sgt-shoot__grid">{grid}</div>
<div class="sgt-set">
<figure>{img('d3-wide', width=520)}</figure>
<div><h3>Как устроена каждая сцена</h3>
<ul class="sgt-set__list">
<li><b>1</b><span>Общий план: видно обоих, кресла и знак на стене</span></li>
<li><b>2</b><span>Крупный интервьюера, когда звучит вопрос</span></li>
<li><b>3</b><span>Крупный кандидата на весь ответ</span></li>
<li><b>4</b><span>Кадр уезжает в окно, сверху выходит разбор</span></li>
</ul>
<p style="margin-top:18px;color:#59636F;font-size:16px">Девять сцен, от пяти секунд
до почти двух минут. Самая короткая построена на одном вопросе и одном ответе,
самая длинная держит две вежливые остановки кандидата.</p>
<ul class="sgt-dlg">{dlg}</ul></div></div>
</div></section>'''


def screens():
    cells = ''.join(
        f'<figure class="rev">{img(f, width=280)}'
        f'<figcaption>{FRAMES[f]["caption"]}</figcaption></figure>' for f in SCREENS)
    return f'''<section class="sgt-screens"><div class="sgt__in">
<p class="kicker">Графика</p>
<h2>Двадцать восемь экранов</h2>
<p class="lead">Экраны курса нарисованы под материал заказчика: заголовок, правило,
примеры вопросов и иллюстрация переговорной. Цвет плашки работает как знак:
бирюзовая это инструмент, оранжевая пример вопроса, тёмно-синяя определение или вывод.</p>
<div class="sgt-screens__grid">{cells}</div>
<div class="sgt-craft">
<div class="sgt-craft__c rev"><div class="sgt-craft__bars" aria-hidden="true">
<i></i><i></i><i></i></div>
<b>Переход из трёх полос</b><p>Зелёная, синяя и коралловая полосы проходят кадр
за две десятых секунды. Четырнадцать раз за курс, всегда на смене темы.</p></div>
<div class="sgt-craft__c rev">{img('wipe', width=340)}
<b>Он же в кадре</b><p>Полосы закрывают уходящий экран и открывают следующий,
поэтому склейка читается как часть оформления, а не как монтажный стык.</p></div>
<div class="sgt-craft__c rev">{img('c-d1', width=340)}
<b>Разбор поверх кадра</b><p>Второй фирменный приём: сцена сжимается в окно,
плашка с выводом выходит сверху. Девять раз, по одному на сцену.</p></div>
</div></div></section>'''


def done():
    return f'''<section class="sgt-done"><div class="sgt__in">
<p class="kicker">Результат</p>
<h2>Курс, который можно выдать сотруднику</h2>
<p>Заказчик получил готовый материал для внутреннего обучения: две части,
которые смотрят подряд или по одной, разложенные по темам правила и живые примеры,
на которые можно ссылаться в разговоре с руководителем перед интервью.</p>
<div class="sgt-done__grid">
<div class="sgt-done__c"><b>Сценарий и текст</b><span>Дикторский текст и реплики девяти
сцен собраны по методике заказчика, каждая сцена написана под конкретное правило.</span></div>
<div class="sgt-done__c"><b>Съёмка</b><span>Актёры, интерьер, три плана на сцену
и работа со звуком: разговор слышно так же ровно, как дикторский голос.</span></div>
<div class="sgt-done__c"><b>Графика и сборка</b><span>28 экранов, два фирменных перехода
и монтаж, в котором правило, сцена и разбор идут единым ритмом.</span></div>
</div></div></section>'''


PAGE_JS = """<script>
(function(){
 // ── появление блоков ────────────────────────────────────────────────────
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);}});},
  {rootMargin:'0px 0px -8% 0px',threshold:.06});
 document.querySelectorAll('.sgt .rev').forEach(function(n){io.observe(n);});

 // ── фрагменты: постер уходит по клику, играет один за раз ───────────────
 var clips=[].slice.call(document.querySelectorAll('[data-clip]'));
 clips.forEach(function(c){
  var v=c.querySelector('video'),b=c.querySelector('.sgt-clip__play');
  if(!v||!b)return;
  b.addEventListener('click',function(){
   clips.forEach(function(o){if(o!==c){var ov=o.querySelector('video');if(ov)ov.pause();}});
   c.classList.add('is-on');v.play();
  });
  v.addEventListener('play',function(){c.classList.add('is-on');});
 });

 // ── тренажёр «какой это вопрос» ─────────────────────────────────────────
 var QUIZ=%QUIZ%,TYPES=%TYPES%;
 var box=document.querySelector('.sgt-quiz');
 if(box&&QUIZ.length){
  var qEl=box.querySelector('[data-question]'),cEl=box.querySelector('[data-count]'),
      btns=box.querySelector('[data-btns]'),hint=box.querySelector('[data-hint]'),
      ansBody=box.querySelector('[data-answer-body]'),next=box.querySelector('[data-next]'),
      verdict=box.querySelector('[data-verdict]'),bar=box.querySelector('[data-bar]'),
      done=false,i=0;
  function show(){
   var q=QUIZ[i];
   done=false;
   qEl.textContent=q.q;
   cEl.textContent='Вопрос '+(i+1)+' из '+QUIZ.length;
   bar.style.width=Math.round((i)/QUIZ.length*100)+'%';
   [].forEach.call(btns.children,function(b){
    b.classList.remove('is-right','is-picked','is-dim');b.disabled=false;
    b.removeAttribute('aria-pressed');});
   verdict.hidden=true;verdict.className='sgt-quiz__verdict';verdict.innerHTML='';
   ansBody.hidden=true;ansBody.innerHTML='';hint.hidden=false;next.hidden=true;
  }
  function answer(code){
   var q=QUIZ[i],ok=(code===q.t),name=TYPES[q.t]||'',picked=TYPES[code]||'';
   done=true;
   bar.style.width=Math.round((i+1)/QUIZ.length*100)+'%';
   // одно состояние на кнопку: верный зелёный, свой неверный красный,
   // все прочие гаснут — иначе на экране четыре разных подсветки сразу
   [].forEach.call(btns.children,function(b){
    b.disabled=true;
    if(b.dataset.t===q.t){b.classList.add('is-right');}
    else if(b.dataset.t===code){b.classList.add('is-picked');}
    else{b.classList.add('is-dim');}
    if(b.dataset.t===code)b.setAttribute('aria-pressed','true');});
   verdict.hidden=false;
   verdict.className='sgt-quiz__verdict '+(ok?'is-ok':'is-no');
   verdict.innerHTML=ok
    ? '<i aria-hidden="true">✓</i><span><b>Верно.</b> Это '+name.toLowerCase()+' вопрос.</span>'
    : '<i aria-hidden="true">✕</i><span><b>Не он.</b> Вы выбрали «'+picked+'», '+
      'а это '+name.toLowerCase()+' вопрос.</span>';
   hint.hidden=true;
   ansBody.hidden=false;
   ansBody.innerHTML='<p><b style="color:#fff;font-size:16px;letter-spacing:0;'+
    'text-transform:none;display:inline">'+name+'.</b> '+q.note+'</p>'+
    '<img src="%IMG%/'+q.shot+'@560.jpg" width="560" height="315" alt="Экран курса: '+
    name.toLowerCase()+' вопросы" loading="lazy" decoding="async">'+
    '<figcaption>Экран курса, часть '+q.part+', '+q.tc+'</figcaption>';
   next.hidden=false;
   next.textContent=(i>=QUIZ.length-1)?'Пройти ещё раз':'Следующий вопрос';
   if(document.activeElement&&document.activeElement.disabled)next.focus();
  }
  btns.addEventListener('click',function(e){
   var b=e.target.closest('button');if(!b||done)return;
   answer(b.dataset.t);
  });
  next.addEventListener('click',function(){
   i=(i+1)%QUIZ.length;show();
   if(btns.firstElementChild)btns.firstElementChild.focus();
  });
  show();
 }

 // ── разметка стенограммы: буквы модели и флаги разбора ──────────────────
 document.querySelectorAll('.sgt-doc').forEach(function(d){
  var keys=d.querySelectorAll('.sgt-keys button'),
      lines=[].slice.call(d.querySelectorAll('.sgt-line'));
  keys.forEach(function(b){
   b.addEventListener('click',function(){
    var on=b.classList.contains('is-on');
    keys.forEach(function(o){o.classList.remove('is-on');});
    lines.forEach(function(l){l.classList.remove('is-hit');});
    if(on){d.classList.remove('is-marking');return;}
    b.classList.add('is-on');d.classList.add('is-marking');
    var k=b.dataset.key;
    lines.forEach(function(l){
     if((l.dataset.marks||'').split(' ').indexOf(k)>-1)l.classList.add('is-hit');
    });
   });
  });
 });
})();
</script>"""


def page_js():
    quiz_rows = [{'q': q, 't': t, 'note': note, 'shot': shot, 'part': part,
                  'tc': f'{int(tc) // 60:02d}:{int(tc) % 60:02d}'}
                 for q, t, note, shot, part, tc in QUIZ]
    types = {code: name for code, name, _, _ in TYPES}
    return (PAGE_JS.replace('%QUIZ%', json.dumps(quiz_rows, ensure_ascii=False))
            .replace('%TYPES%', json.dumps(types, ensure_ascii=False))
            .replace('%IMG%', IMG))


BREADCRUMB_LD = (
    '<script type="application/ld+json">{"@context":"https://schema.org",'
    '"@type":"BreadcrumbList","itemListElement":['
    '{"@type":"ListItem","position":1,"name":"Главная","item":"https://hand-marketing.ru/"},'
    '{"@type":"ListItem","position":2,"name":"Кейсы","item":"https://hand-marketing.ru/project/"},'
    '{"@type":"ListItem","position":3,"name":"Видеопродакшн",'
    '"item":"https://hand-marketing.ru/videoproduction/"},'
    '{"@type":"ListItem","position":4,"name":"Обучающие видео для руководителей Saint-Gobain",'
    f'"item":"{URL}"}}]}}</script>')

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
        f'<meta property="og:image" content="https://hand-marketing.ru{IMG}/d6-wide.jpg">'
        '<link rel="stylesheet" href="/fonts/rubik-alegreya.css">'
        + rc.FONT + rc.CSS + CSS + METRIKA + '</head><body>')


def page():
    # своего блока «обсудить проект» на странице нет: её закрывает фиолетовая
    # форма из rc.footer(), второй CTA был бы дублем
    body = (f'{rc.header()}<main class="sgt">{hero()}{wipe()}{nums()}{layers()}'
            f'{quiz()}{chain()}{wipe()}{star()}{clips_row()}{shoot()}'
            f'{screens()}{done()}</main>'
            f'<a id="lead"></a>{rc.footer()}{rc.JS}{page_js()}'
            f'{BREADCRUMB_LD}</body></html>')
    return HEAD + body


if __name__ == '__main__':
    outdir = os.path.join(ROOT, 'video', 'saintgobain', 'training')
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'index.html')
    open(p, 'w', encoding='utf-8').write(page())
    a2 = os.path.join(outdir, 'index-a2.html')
    if os.path.exists(a2):
        os.remove(a2)
        print('· удалён index-a2.html (деплой затёр бы им кастомную страницу)')
    print(f'✓ {os.path.relpath(p, os.path.dirname(ROOT))} '
          f'({os.path.getsize(p) / 1024:.0f} КБ)')
