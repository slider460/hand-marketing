#!/usr/bin/env python3
"""Полноценный мобильный кейс /creative/eaton/visual (3D визуализация Eaton).
Страница уже имеет mcase-шаблон (gen_mcases.py), но его галерея пуста: рендер
___2131231845654.png и плакаты noroot.png отсеяны JUNK-фильтром по именам файлов,
остался только текст + обложка (photo.jpg). Этот скрипт обогащает story-секцию
ИМЕННО ЭТОЙ страницы: метки Компания/Задача/Решение/Результат + все три
визуализации с подписями (обложка = рендер «типовое размещение», в Решении —
3D-модель, в Результате — плакаты). Пути картинок — родные /images/lib (webp есть).
Идемпотентен (маркеры). Правит index.html и index-a2.html."""
import os, re

HERE=os.path.dirname(os.path.abspath(__file__))
PAGE_DIR=os.path.abspath(os.path.join(HERE,'..','..','mirror','creative','eaton','visual'))
MARK_A='<!--mk-eaton-visual-->'; MARK_B='<!--/mk-eaton-visual-->'
PINK='#C12164'  # акцент категории Creative & Design (как в mcase-шаблоне)

MODEL='/images/lib/as6636-3261-4534-a339-306632633334/___2131231845654.png'
POSTERS='/images/lib/as3536-6531-4037-b531-323736343233/noroot.png'

STORY=f"""{MARK_A}<style id="mk-css">
.mh-story .mk-l{{margin:26px 0 10px;font-family:'Montserrat',Arial,sans-serif;font-weight:800;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:{PINK}}}
.mh-story .mk-l:first-child{{margin-top:0}}
.mh-story figure{{margin:16px 20px 22px}}
.mh-story figure img{{display:block;width:100%;height:auto;border-radius:16px;box-shadow:0 18px 36px -20px rgba(20,23,28,.4)}}
.mh-story figcaption{{margin-top:8px;font-size:13px;line-height:1.4;color:#7A828C}}
</style><section class="mh-sec mh-story">
<p class="mk-l">Компания</p>
<p>EATON — американская машиностроительная корпорация, производитель электротехнического и&nbsp;гидравлического оборудования и&nbsp;автокомплектующих компонентов для авиационной промышленности. Основана в&nbsp;1911&nbsp;году.</p>
<p class="mk-l">Задача</p>
<p>Создать визуальные образы, демонстрирующие типовое размещение оборудования компании EATON при использовании его на&nbsp;промышленных объектах.</p>
<p class="mk-l">Решение</p>
<p>Для визуализации объектов было принято решение — создать 3D-модель промышленных объектов и&nbsp;оборудования. Были созданы гипермаркет, завод и&nbsp;центр обработки данных.</p>
<figure><img src="{MODEL}" alt="3D-модель промышленного объекта с оборудованием Eaton" loading="lazy">
<figcaption>3D-модель промышленного объекта с&nbsp;расстановкой оборудования</figcaption></figure>
<p>Инженеры компании расставили типовой набор оборудования в&nbsp;соответствии с&nbsp;типом объекта. Сделав рендеры, мы адаптировали подачу для печатных плакатов, добавив описание каждого вида оборудования.</p>
<p class="mk-l">Результат</p>
<p>Серия печатных плакатов с&nbsp;3D-визуализациями — промышленный объект и&nbsp;центр обработки данных — с&nbsp;пояснениями по&nbsp;каждому виду оборудования.</p>
<figure><img src="{POSTERS}" alt="Печатные плакаты с 3D-визуализациями и описанием оборудования Eaton" loading="lazy">
<figcaption>Печатные плакаты с&nbsp;описанием оборудования</figcaption></figure>
</section>{MARK_B}"""

def patch(path,require_story=True):
    h=open(path,encoding='utf-8').read()
    if MARK_A in h and '<section class="mh-sec mh-story">' in re.search(
            re.escape(MARK_A)+r'.*?'+re.escape(MARK_B),h,re.S).group(0):
        # повторный прогон: обновить маркированный фрагмент на месте
        h=re.sub(re.escape(MARK_A)+r'.*?'+re.escape(MARK_B),lambda _:STORY,h,flags=re.S)
    else:
        # снести старую параллельную .mk-вставку (первая версия скрипта), если была
        h=re.sub(re.escape(MARK_A)+r'.*?'+re.escape(MARK_B),'',h,flags=re.S)
        m=re.search(r'<section class="mh-sec mh-story">.*?</section>',h,re.S)
        if not m:
            if require_story: raise AssertionError(f'mh-story не найдена в {path}')
            open(path,'w',encoding='utf-8').write(h)  # только чистка .mk
            print('чистка:',path); return
        h=h[:m.start()]+STORY+h[m.end():]
    open(path,'w',encoding='utf-8').write(h)
    print('OK:',path)

if __name__=='__main__':
    # исходник Тильды: mcase туда не вшит — только чистим старую .mk-вставку
    patch(os.path.join(PAGE_DIR,'index.html'),require_story=False)
    # деплойный файл со вшитым mcase-шаблоном
    patch(os.path.join(PAGE_DIR,'index-a2.html'))
    # шаблон mcases — чтобы пересборка страниц не потеряла обогащение
    patch(os.path.join(HERE,'mcases','creative__eaton__visual.html'))
