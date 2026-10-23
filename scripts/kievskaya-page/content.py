# -*- coding: utf-8 -*-
# Хелперы и тексты из kievskaya_build_md.py (папка тендера), без генерации md.
import re
from data import RATES, POS, AGENCY_FEE, discounted, PAYKEY
DISC = 0.10
def clean(t):
    t = t.replace("ё", "е").replace("Ё", "Е").replace("—", "-").replace("–", "-")
    return re.sub(r"[ \t]+", " ", t).strip()

def provide_items(t):
    parts = re.split(r"\s*(?:^|\n)\s*\d+\.\s*", "\n" + t)
    return [clean(p) for p in parts if clean(p)]

SPECIFIC = [
 (r"собственными силами.*субподряде", "Проект, дизайн, сопровождение и приемку ведем сами. Изготовление на постоянном партнерском производстве."),
 (r"численность монтажной бригады|максимальную численность бригады", "До 12 монтажников на смену. Допуски к договору."),
 (r"собственного инструмента", "Ручной инструмент и электроинструмент входят в ставку смены, вышки-туры по прайсу. Перечень к договору."),
 (r"собственного транспорта", "Грузовой автомобиль до 3 т, рейс по Москве в прайсе."),
 (r"форматы и разрешения сдачи|форматы сдачи", "16:9 и 9:16, 4K. Нестандартные экраны ТЦ под ваш техпаспорт экрана."),
 (r"ai-сервисов", "Работаем только на тарифах с коммерческой лицензией. Перечень сервисов в договоре."),
 (r"брендинговых проектов", "Проекты со ссылками в блоке «Похожие проекты» ниже."),
 (r"состав команды: арт-директор", "Chief Creative Officer Святослав Дементьев, арт-директор, дизайнеры, копирайтер."),
 (r"чужому брендбуку", "Доклад СКОЛКОВО сверстан по брендбуку заказчика, ссылка ниже."),
 (r"tone of voice", "Тестовый пост по вашему брифу покажет это лучше примеров. Сделаем бесплатно."),
 (r"пул постоянных подрядчиков|список постоянных партнеров", "Постоянная команда фотографов, операторов, стилистов, декораторов, кейтеринга и техники. Назовем на встрече."),
 (r"обработанных фото за час", "От 35 обработанных кадров за час репортажа."),
 (r"собственного оборудования, включая свет|перечень оборудования: камеры", "Камеры, стабилизатор, звук и свет в ставке. Дрон: FPV для съемки внутри атриума."),
 (r"каталог продукции", "Цены по тиражам 100 и 500 в расчете выше. Каталог под ваш запрос пришлем за 2 р.д."),
 (r"минимальный тираж по текстилю", "От 30 шт."),
 (r"методы нанесения", "Вышивка, шелкография, тампопечать, лазерная гравировка, УФ-печать. Ограничения покажем на макете."),
 (r"варианты подарочной упаковки", "Предложим 2-3 варианта конструкции вместе с расчетом коробки."),
 (r"собственное производство или закупка", "Ведем под ключ: макет, образец, тираж, контроль качества, доставка."),
 (r"минимальный тираж боксов", "От 20 боксов."),
 (r"база блогеров", "Работаем по списку заказчика или подбираем блогеров под задачу."),
 (r"фио менеджера", "Закрепленный менеджер: Народецкий Александр, Client Service Director."),
 (r"службой безопасности тц|администрацией", "Работали в атриумах Ривьеры, Мозаики, ГУМа, «Европейского», «Атриума», «Метрополиса». Кейсы ниже."),
 (r"ухода за живой флористикой", "Ежедневный уход на период экспозиции, замена увядших элементов."),
 (r"оборудования в собственности", "Комплект под мероприятие из нашего постоянного парка. Перечень к договору."),
 (r"резервного оборудования", "Резервный радиомикрофон в комплекте, резервный пульт по прайсу."),
 (r"оборудовании площадки или со своим", "Оба варианта."),
 (r"контакта заказчиков для рекомендаций", "Дадим контакты после согласования с заказчиками."),
 (r"жанры и форматы", "Lounge, deep house, nu disco, джаз-фанк, фоновые сеты для галерей."),
 (r"технический райдер", "Пришлем с подтверждением даты."),
 (r"наличие собственного оборудования", "Есть. Расчет с оборудованием и без в таблице выше."),
 (r"плейлиста", "Плейлист согласуем заранее, письменно."),
 (r"форму оформления персонала", "ГПХ и самозанятые."),
 (r"обучения и инструктажа", "Инструктаж по объекту и продукту перед каждым выходом."),
 (r"замены сотрудника", "Замена в течение 3 часов, часы неявки к оплате не выставляем."),
 (r"срочном запросе", "Выезд в течение 24 часов, доплата 25% к стоимости смен."),
 (r"форма оплаты", "Аванс 70%, остаток 30% после акта."),
]
def status(item, no):
    s = item.lower()
    for rx, ans in SPECIFIC:
        if re.search(rx, s): return ans
    if re.search(r"тестов", s): return "Выполним бесплатно до договора."
    if re.search(r"портфолио|кейс|шоурил|реализованн|выполненн|примеры текстов|ссылки на записи|список 5 последних|отчетных ролик|примеры изготовленных|образцы карт", s):
        return "Проекты со ссылками в блоке «Похожие проекты» ниже. Дополнительные примеры пришлем по запросу."
    if re.search(r"стоимост|ставк|прайс|цен[аы] |размер агентской|почасов", s):
        return "В расчете и в прайсе на этой странице."
    if re.search(r"срок|время", s): return "В расчете на этой странице, в рабочих днях."
    if re.search(r"правок|концепций на первом", s): return "Указано в блоке «Что входит»."
    if re.search(r"передач|исключительн|релиз|права", s): return "Передаем по договору, в стоимость включено. Музыка, шрифты, стоки и AI-материалы в объеме их лицензий."
    if re.search(r"пример сметы|пример итоговой сметы|технического райдера", s): return "Пришлем пример сметы по запросу, структура видна в расчете выше."
    if re.search(r"фото-отчет|фотоотчет", s): return "Фотоотчет после каждого выезда, пример пришлем по запросу."
    if re.search(r"копии|допуск|полис|страхован|сертификат|декларац|медкниж|санитар|удостоверени|адрес производства|фото цехов|снаряжени", s):
        return "К договору."  # служебная проверка ниже
    if re.search(r"ночн", s): return "Работаем ночью по регламенту ТЦ, доплата в прайсе."
    if re.search(r"замер", s): return "Выезд на замер в течение 1 рабочего дня, бесплатно."
    return "Ответим в расчете или к договору."

COVERS = {
 "riviera": "https://hand-marketing.ru/images/lib/as3062-3363-4134-b333-623232303134/__-22.png",
 "mozaika": "https://hand-marketing.ru/images/lib/as6263-3532-4466-b765-323663363739/__-28.png",
 "salaris": "https://hand-marketing.ru/images/lib/as3234-6262-4231-b031-663033663939/__-16.png",
 "mmg": "https://hand-marketing.ru/images/lib/stor3435-6339-4163-a433-646336343434/88889dcf73b126c47c1dec4a187d308a.png",
 "changan": "https://hand-marketing.ru/images/lib/as3635-3436-4663-b265-633363383261/__-98.png",
 "marieclaire": "https://hand-marketing.ru/images/lib/as3731-3666-4163-a661-383336646133/__-13.png",
 "samara": "https://hand-marketing.ru/images/lib/custom-samara-vdnh/cover-main.png",
 "sgphoto": "https://hand-marketing.ru/images/lib/custom-sgphoto/cover-main.png",
 "metra": "https://hand-marketing.ru/images/lib/custom-metra/cover-main.png",
 "samsung": "https://hand-marketing.ru/images/lib/as3466-3261-4738-b938-303637303133/__-18.png",
 "rgd": "https://hand-marketing.ru/images/lib/as3634-3861-4239-b237-356636663535/__-60.png",
 "mozvideo": "https://hand-marketing.ru/images/lib/as6537-6538-4133-b832-383637333832/__-45.png",
 "teoxane": "https://hand-marketing.ru/images/lib/as3538-6538-4236-b937-343132366134/__-76.png",
 "samara_brand": "https://hand-marketing.ru/images/lib/custom-samara-brand/cover-main.png",
 "becar_sdep": "https://hand-marketing.ru/images/lib/as6366-6163-4338-b039-373730386163/__-74.png",
 "becar_wei": "https://hand-marketing.ru/images/lib/as3532-6637-4235-a237-396563653836/__-78.png",
 "becar_smile": "https://hand-marketing.ru/images/lib/custom-smile-broch/cover-main.png",
 "sg_calendar": "https://hand-marketing.ru/images/lib/custom-sgcalendar/cover-main.png",
 "skolkovo": "https://hand-marketing.ru/images/lib/as3266-3963-4363-a239-646364383365/__-72.png",
 "sgcx": "https://hand-marketing.ru/images/lib/custom-sgcx/cover-main.png",
 "silkway": "https://hand-marketing.ru/images/lib/as6164-6432-4132-a361-613136626438/__-51.png",
 "salaris_v": "https://hand-marketing.ru/images/lib/as3933-3462-4563-b861-383364333966/__-15.png",
 "lingerie": "https://hand-marketing.ru/images/lib/as3439-3739-4562-a533-616631333163/__-37.png",
 "interpl": "https://hand-marketing.ru/images/lib/as3331-3035-4965-a439-613266363431/__-54.png",
 "eaton_kz": "https://hand-marketing.ru/images/lib/as6165-3534-4833-b866-366532623865/__-26.png",
 "eaton_on": "https://hand-marketing.ru/images/lib/as6135-3563-4735-a365-643234376439/icons-112.png",
 "stavropol": "https://hand-marketing.ru/images/lib/as6466-3635-4534-b432-353364376364/__-01.png",
 "messe": "https://hand-marketing.ru/images/lib/as6536-6131-4737-a636-313561623430/__-47.png",
 "becar_pm": "https://hand-marketing.ru/images/lib/custom-becar-pm/cover-main.png",
}
CASES = {
 "riviera": ("ТРЦ «Ривьера»: вечер «Внутри стихии»", "Почти двести руководителей на стройке ТРЦ, передача помещения «Ашан Сити», три экрана в одной композиции", "https://hand-marketing.ru/event/riviera"),
 "mozaika": ("ТРЦ «Мозаика»: «Пора выходить на свет»", "Вечер для арендаторов: 134 гостя собрали новый знак ТЦ из лампочек", "https://hand-marketing.ru/event/mozaika"),
 "salaris": ("МФК «Саларис»: презентация для арендаторов", "200 ритейлеров, площадка, концепция, ролик об объекте", "https://hand-marketing.ru/event/salaris"),
 "mmg": ("ТРЦ «Павелецкая Плаза»: фильм для арендаторов", "Локация, трафик, аудитория, готовность объекта, 5:37", "https://hand-marketing.ru/mmg"),
 "changan": ("Changan CS35 в атриуме ТЦ", "Три недели презентации, запись на тест-драйв, финал с 3D mapping на кузове", "https://hand-marketing.ru/event/changan"),
 "marieclaire": ("Marie Claire в ТЦ Москвы", "ГУМ, «Европейский», «Атриум», «Метрополис»: стенды, семплинг, POS, финальный вечер", "https://hand-marketing.ru/event/marieclaire"),
 "samara": ("Стенд Самарской области на ВДНХ", "Ладья с экраном-парусом, 204 м², выставка-форум «Россия», более 18 млн посетителей", "https://hand-marketing.ru/portfolio/samara-stand-vdnh"),
 "sgphoto": ("Saint-Gobain, предметная съемка", "63 позиции за смену, 62 кадра в сдаче под каталог, сайт и POS", "https://hand-marketing.ru/photo/saint-gobain"),
 "metra": ("Брендбук Metra Technology Group", "Один знак на пять брендов, пять палитр на общей сетке", "https://hand-marketing.ru/creative/metra"),
 "samsung": ("Новый год Samsung", "Зимний лес из проекций и интерактивный почтовый ящик Деда Мороза", "https://hand-marketing.ru/event/samsung"),
 "rgd": ("Новогодний набор РЖД", "Шесть позиций сувенирки в одной концепции", "https://hand-marketing.ru/creative/rgd/suvenir"),
 "mozvideo": ("Ролик ТРЦ «Мозаика»", "4:31, аэросъемка, галереи и 13 синхронов арендаторов", "https://hand-marketing.ru/video/mozaika"),
 "teoxane": ("Key visual Teoxane", "Ключевой визуал научной конференции на образе иконописи", "https://hand-marketing.ru/creative/teoxane"),
 "samara_brand": ("Фирменный стиль выставки «Самара»", "28 полос, маскот в 16 образах, правила для залов, экранов и навигации", "https://hand-marketing.ru/creative/samara"),
 "becar_sdep": ("Айдентика отдела продаж Becar", "Знак, паттерн и палитра, по которым макеты собирают сами менеджеры", "https://hand-marketing.ru/creative/becar/sdep"),
 "becar_wei": ("Буклет We&I", "24 полосы, которые объясняют формат кондо-отеля", "https://hand-marketing.ru/creative/becar/weampi"),
 "becar_smile": ("Брошюра ТЦ «Смайл»", "22 полосы для инвесторов в торговые метры", "https://hand-marketing.ru/creative/becar/smile"),
 "sg_calendar": ("Календарь Saint-Gobain", "Материалы глазами мастера: профиль становится небоскребом", "https://hand-marketing.ru/creative/saintgobain/calendar"),
 "skolkovo": ("Доклад СКОЛКОВО", "86 полос по брендбуку, переработанная инфографика", "https://hand-marketing.ru/creative/skolkovo"),
 "sgcx": ("Фильм Saint-Gobain «Клиентский опыт»", "10 минут, 17 интервью, офис и два завода", "https://hand-marketing.ru/video/saintgobain/cx"),
 "silkway": ("3D-маршрут Silk Way Rally", "5 947,93 км рельефом по координатам легенды", "https://hand-marketing.ru/video/silkway"),
 "salaris_v": ("Ролики МФК «Саларис»", "Объект на стадии стройки в 3D-графике и аэросъемке", "https://hand-marketing.ru/video/salaris"),
 "lingerie": ("Подиумная съемка Lingerie", "Полуторачасовой показ в двухкамерной съемке, ролик на 7 минут", "https://hand-marketing.ru/video/lingerie"),
 "interpl": ("Ролик выставки «Интерпластика»", "2:12 вместо прогулки по четырем павильонам, 17 компаний в кадре", "https://hand-marketing.ru/video/interplastika"),
 "eaton_kz": ("Конференция Eaton в Алматы", "Под ключ: сцена, LED, застройка, сопровождение трое суток", "https://hand-marketing.ru/event/eaton"),
 "eaton_on": ("Эфир Eaton на IT-ОСЬ 2020", "Семь часов эфира, две камеры, vMix, свет, резервный канал", "https://hand-marketing.ru/eaton_online"),
 "stavropol": ("3D mapping в Ставрополе", "27 проекторов, лазеры, более 25 000 зрителей", "https://hand-marketing.ru/3d/stavropol"),
 "messe": ("Новый год Messe Düsseldorf", "Офис на вечер: четыре зоны, фуршет, сцена, бар", "https://hand-marketing.ru/event/messeduessleldorf"),
 "becar_pm": ("Стенд Becar на Private Money Expo", "Проект, застройка, презентация для сцены, дежурство, демонтаж", "https://hand-marketing.ru/portfolio/becar-private-money"),
}
POS_CASES = {
 1: ["marieclaire", "samara", "becar_pm"], 3: ["samara", "changan", "becar_pm"],
 9: ["silkway", "salaris_v", "samsung", "samara"], 10: ["metra", "samara_brand", "becar_sdep"],
 11: ["teoxane", "sg_calendar", "skolkovo", "becar_smile"], 12: ["becar_wei", "becar_smile"],
 13: ["sgcx", "sgphoto", "mmg"], 14: ["sgphoto", "riviera"], 15: ["mozvideo", "lingerie", "interpl"],
 16: ["rgd"], 17: ["rgd"], 22: ["riviera", "mozaika", "salaris", "changan", "messe"],
 23: ["samsung", "samara", "mozaika"], 25: ["eaton_kz", "eaton_on", "stavropol"],
 26: ["messe", "mozaika"], 27: ["messe", "salaris"], 30: ["marieclaire", "changan"], 31: ["samara", "mozaika"],
}
TAG = {1: "PROD", 3: "PROD", 9: "3D", 10: "CREATIVE", 11: "CREATIVE", 12: "CREATIVE", 13: "PROD", 14: "PROD",
       15: "PROD", 16: "PROD", 17: "BTL", 22: "EVENTS", 23: "EVENTS", 25: "EVENTS", 26: "EVENTS", 27: "EVENTS", 30: "BTL", 31: "PROD"}
TAGCOLOR = {"PROD": "orange", "3D": "pink", "CREATIVE": "yellow", "EVENTS": "purple", "BTL": "red"}
PAY = {"svc": "100% по факту, оплата в течение 10 рабочих дней после акта, без аванса",
       "adv": "Аванс 50% на расходы подрядчиков (модели, аренда, персонал), остаток в течение 10 рабочих дней после акта",
       "prod": "Аванс 70%, остаток 30% после акта"}
FIX = {"svc": "Цена фиксирована на 6 месяцев с даты КП", "adv": "Цена фиксирована на 6 месяцев с даты КП",
       "prod": "Цена производства и закупок действует 3 месяца с даты КП, дальше пересчет по ценам поставщиков на дату заказа"}

def money(x): return f"{x:,.0f}".replace(",", " ") + " руб."
def num(q): return (f"{q:.2f}".rstrip("0").rstrip(".")).replace(".", ",")

def line_calc(key, q):
    price = RATES[key][2]
    if price is None: return None
    h = round(q * price)
    d = DISC if discounted(key) else 0
    return h, d, round(h * (1 - d))

def task_total(lines, no):
    th = tj = 0
    for key, q, _ in lines:
        c = line_calc(key, q)
        if c is None: return None
        th += c[0]; tj += c[2]
    if no == 22:
        fh = round(AGENCY_FEE * th); tj += round(fh * (1 - DISC))
    return tj
