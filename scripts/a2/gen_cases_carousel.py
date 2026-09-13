import json, re, os, glob, html as H
API='mirror/api'
def strip(s): return re.sub('<[^>]+>','',s or '').strip()
data={}
for f in glob.glob(API+'/getproductslist_*.json'):
    try: d=json.load(open(f))
    except: continue
    for p in d.get('products',[]):
        url=p.get('url') or ''
        if not url: continue
        title=(p.get('title') or '').strip()
        if title=='⠀': title=''
        cur=data.get(url,{})
        if title and not cur.get('title'):
            g=json.loads(p['gallery']) if p.get('gallery') else []
            # descr в данных Tilda бывает с HTML (<br />) — чистим до текста
            cur.update(title=strip(title), descr=strip(p.get('descr')), cat=strip(p.get('text')), img=(g[0]['img'] if g else cur.get('img','')))
        if not cur.get('img'):
            g=json.loads(p['gallery']) if p.get('gallery') else []
            if g: cur['img']=g[0]['img']
        data[url]=cur
order=json.load(open(API+'/getproductslist_689558768071.json'))['products']
FB={
    '/video/eaton':('Eaton','Ролик для международной выставки','Video production'),
    '/creative/becar/vertical':('Becar','Брошюра Vertical BW Signature Collection','Creative & Design'),
    '/bekobod1':('Технопарк «Бекабад»','Презентационный ролик технопарка','Video production'),
    '/zubovo':('Технопарк «Зубово»','Презентационный фильм технопарка под Уфой','Video production'),
    '/isotec':('Изотек','Бренд-ролик ISOTEC для Saint-Gobain','Video production'),
    '/video/saintgobain/training':('Обучающие видео Saint-Gobain','Курс для руководителей: вопросы и модель STAR','Video production'),
    '/video/saintgobain/cx':('Фильм «Клиентский опыт» Saint-Gobain','48 сотрудников названы в кадре по имени','Video production'),
    '/photo/saint-gobain':('Съёмка продукции Gyproc','63 позиции за один съёмочный день','Photo Production'),
    '/creative/samara':('Фирменный стиль выставки «Самара»','Брендбук Самарской области, 28 полос','Creative & Design'),
    '/creative/metra':('Брендбук Metra Technology Group','Пять брендов индустриальной экосистемы','Creative & Design'),
    '/creative/becar/smile':('Брошюра ТЦ «Смайл»','22 полосы про доход с торговых метров','Creative & Design'),
    '/creative/becar/knight-house':('Брошюра «Дом с рыцарем»','18 полос про апартаменты в доходном доме','Creative & Design'),
    '/creative/saintgobain/calendar':('Новогодний календарь Saint-Gobain','Концепция: иллюстрации из инструментов','Creative & Design'),
    '/portfolio/ceramicanova':('Имиджевые ролики для CeramicaNova','17 роликов по коллекциям санфарфора','Video production'),
    '/portfolio/obo-academy':('Серия роликов для OBO Bettermann','Съёмка продукции в Академии OBO','Video production'),
    '/portfolio/becar-private-money':('Стенд You&Co для Becar','Private Money Expo Forum 2021','Exhibition Build'),
    '/portfolio/samara-stand-vdnh':('Стенд Самарской области','Выставка-форум «Россия», ВДНХ','Exhibition Build'),
    '/portfolio/samara-exhibition':('Выставка «Самара»','Музей им. Алабина','Exhibition Build'),
    '/portfolio/stavropol-stand-vdnh':('Стенд Ставропольского края','Выставка-форум «Россия», ВДНХ','Exhibition Build'),
    '/event/changan':('Презентация Changan CS35','Атриум ТЦ и финал с 3D mapping шоу','Event')}
# Жёсткие подписи там, где данных каталога не хватает. У трёх digital-кейсов
# в поле text вместо категории лежит подзаголовок («Бизнес центр "Станция"»
# и т.п.), поэтому cat_key их не распознавал и они выпадали из карусели digital,
# хотя в десктопном каталоге стоят. Заодно фиксируем формулировки: подписи
# в самих каталогах погашены под карточку v2.2 (круг + ховер-квадрат).
OVERRIDE={
 '/digital/becar/invest':('Becar','Сайт Becar Invest','Digital'),
 '/digital/becar/smile':('Becar','Посадочная страница продукта «ТРЦ Смайл»','Digital'),
 '/becar_stancia':('Becar','Посадочная страница «БЦ Станция»','Digital'),
 '/bacar_vertical_all':('Becar','Посадочная страница «Сеть отелей Vertical»','Digital'),
 '/mmg':('MMG Павелецкая Плаза','Рекламный фильм торгового центра','Video production'),
 '/video/rgd/history':('ЦМ РЖД','Фильм к десятилетию дирекции, 3:54','Video production'),
 '/eaton_online':('Eaton','Семь часов эфира на IT-ОСЬ 2020 из офиса','Event'),
 '/video/patriot':('УАЗ и Eaton','Рекламный ролик УАЗ Патриот, 60 секунд','Video production'),
 '/video/gaz':('ГАЗ и Eaton','Вирусный ролик «Газель-трансформер», 1:42','Video production'),
 '/event/salaris':('МФК «Саларис»','Презентация для арендаторов, 200 гостей','Event'),
 '/video/salaris':('МФК «Саларис»','Два ролика: объект и аудитория','Video production'),
 '/event/riviera':('ТРЦ «Ривьера»','«Внутри стихии»: вечер для арендаторов на стройке','Event'),
 '/event/mozaika':('ТЦ «Мозаика»','«Пора выходить на свет»: 134 гостя зажгли знак','Event'),
 '/event/samsung':('Samsung','Новогодний вечер 2020, зимний лес из проекций','Event'),
 '/video/powertechnologies':('Power Technologies','ЧМ-2018: 11 городов, 12 стадионов','Video production'),
 '/video/mozaika':('ТРЦ «Мозаика»','4:31 и тринадцать синхронов','Video production'),
 '/event/messeduessleldorf':('Messe Düsseldorf','Новый год в собственном офисе','Event'),
 '/video/interplastika':('Messe Düsseldorf','«интерпластика» за 2:12, 17 компаний в кадре','Video production'),
 '/video/silkway':('Silk Way Rally','Маршрут 5 947,93 км рельефом по легенде','Video production'),
 '/video/vivax':('VIVAX SPORT','Настасья Самбурская и три средства за 49 секунд','Video production'),
 '/creative/becar/weampi':('Becar','We&I: 24 полосы про кондо-отель','Creative'),
 '/creative/tunel':('AnVIT','Тоннель дезинфекции с циклом до 20 секунд','Creative'),
 '/creative/skolkovo':('СКОЛКОВО','Доклад «Цифровое производство» на 86 полос','Creative'),
 '/digital/becar/vertical':('Becar','Посадочная страница бутик-отеля Vertical','Digital'),
 '/3d/stavropol':('Администрация Ставрополя','27 проекторов, более 25 000 зрителей','3D mapping')}
COL={'event':'#C12164','exhibition':'#673A7E','creative':'#C12164','video':'#CF6F19','digital':'#5E9A2E','3d':'#7E3FA0','btl':'#D6357E','print':'#E08A2B'}
def cat_key(cat):
    c=cat.lower()
    for k in COL:
        if k in c: return k
    return ''
# описания, у которых заголовок остаётся из каталога (текстовый аудит 13.09.2026)
DESCR_OVERRIDE={'/event/marieclaire': 'Кросс-мероприятия в ТЦ Москвы, 2011–2013', '/creative/samara': '28 полос и маскот в 16 образах'}
def card(url,title,descr,cat,img):
    k=cat_key(cat); color=COL.get(k,'#14171C')
    return f'''<a class="mcase" href="{H.escape(url)}"><div class="mcase__img"><img src="{H.escape(img)}" alt="" loading="lazy"><span class="mcase__cat" style="--c:{color}">{H.escape(cat)}</span></div><div class="mcase__b"><div class="mcase__t">{H.escape(H.unescape(title))}</div><div class="mcase__d">{H.escape(H.unescape(descr))}</div></div></a>'''
allcards=[]; bycat={}; CARD={}
for p in order:
    url=p.get('url') or ''
    g=json.loads(p['gallery']) if p.get('gallery') else []
    img=(g[0]['img'] if g else '')
    info=data.get(url,{}); title=info.get('title') or ''; descr=info.get('descr') or ''; cat=info.get('cat') or ''
    if url in FB and not title: title,descr,cat=FB[url]
    if url in OVERRIDE: title,descr,cat=OVERRIDE[url]
    if url in DESCR_OVERRIDE: descr=DESCR_OVERRIDE[url]
    if not img: img=info.get('img','')
    if not title and not img: continue
    c=card(url,title,descr,cat,img); allcards.append(c)
    k=cat_key(cat); bycat.setdefault(k,[]).append((url,c))
    CARD[url]=c
# Состав и порядок категорийной карусели берём из каталога самой страницы услуги.
# По ярлыку категории раскладывать нельзя: у карточки он один, а в каталогах
# кейс живёт сразу в нескольких сторпартах (Ставрополь стоит и в event, и в 3d,
# Changan — в event и 3d). Из-за ярлыка мобильная карусель теряла такие кейсы
# и расходилась с десктопной сеткой. Категория -> сторпарт страницы.
PART_ORDER={'event':'252167513721','creative':'573067849371','digital':'750728959451',
            '3d':'305877663751','print':'351156592581'}
for k,sp in PART_ORDER.items():
    f=f'{API}/getproductslist_{sp}.json'
    if not os.path.exists(f): continue
    urls=[p.get('url') for p in json.load(open(f))['products']]
    bycat[k]=[(u,CARD[u]) for u in urls if u in CARD]
def wrap(cards): return '<div class="mcases" data-mcases><div class="mcases__track">'+''.join(cards)+'</div></div>'
os.makedirs('scripts/a2/carousels',exist_ok=True)
open('scripts/a2/carousels/all.html','w').write(wrap(allcards))
for k,cs in bycat.items():
    if k: open(f'scripts/a2/carousels/{k}.html','w').write(wrap(c for _,c in cs))
print('all:',len(allcards),'| by cat:',{k:len(v) for k,v in bycat.items()})
