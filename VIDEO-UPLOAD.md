# Видео для загрузки в /media/ (на хостинг)

> **18.07.2026 — пережатые версии.** В `media-optimized/` лежат облегчённые копии всех роликов >40МБ
> (720p, x264 crf24, звук сохранён, те же имена файлов). Заливать ПОВЕРХ старых в `/media/` на сервере —
> ссылки в коде менять не нужно. Плюс новый `media/event-hero-loop.mp4` (1.2МБ) — hero-луп страницы /event.

> **30.07.2026 — клипы кейса Samsung НЕ нужно грузить вручную.** `mirror/videos/samsung-mesh-drop.mp4`
> (сброс сетки, 1.4 МБ) и `mirror/videos/samsung-mailbox.mp4` (зона ящика, 2.6 МБ) лежат в `mirror/**`
> и уезжают на хостинг вместе с обычным деплоем, адреса `/videos/samsung-*.mp4`. Режет их
> `scripts/samsung-assets.py` из ~/Downloads/Самсунг.

Всего файлов: 31 (некоторые ролики общие для нескольких кейсов).

| Кейс | Файл на хостинге | Исходник |
|---|---|---|
| /3d/stavropol | `/media/stavropol-3dmapping.mp4` | Stavropol 3DMapping.mp4 |
| /bekobod1 | `/media/bekabad-hd.mp4` | bekabad-hd.mp4 |
| /bekobod1 | `/media/silkway-3d.mp4` | 3D Silk Way.mp4 |
| /event (hero-луп) | `/media/event-hero-loop.mp4` | смонтирован локально: media/event-hero-loop.mp4 (1.2 МБ) ✅ залито 18.07 |
| /portfolio/samara-exhibition (hero-луп) | `/media/samara-exh-hero-loop.mp4` | смонтирован локально (0.8 МБ) |
| /portfolio/samara-stand-vdnh (hero-луп) | `/media/samara-vdnh-hero-loop.mp4` | смонтирован локально (0.9 МБ) |
| /event/changan | `/media/changan-hm-180220.mp4` | Changan HM 180220.mp4 |
| /event/eaton | `/media/eaton-almaty.mp4` | Eaton Almaty.mp4 |
| /event/marieclaire | `/media/marie-claire-event.mp4` | Marie Claire Event.mp4 |
| /event/riviera | `/media/event-riviera.mp4` | Event Riviera.mp4 |
| /event/salaris | `/media/salaris-event-fin180416.mp4` | Salaris Event FIN180416.mp4 |
| /event/samsung | `/media/samsung-new-year-2020.mp4` | Samsung 2020.mp4 |
| index | `/media/hm-showreel.mp4` | HM_Showreel.mp4 |
| /isotec | `/media/izotek-brand-video.mp4` | izotek-brand-video.mp4 |
| /isotec | `/media/silkway-3d.mp4` | 3D Silk Way.mp4 |
| /mmg | `/media/mmg-paveleckayaplaza.mp4` | MMG_PaveleckayaPlaza.mp4 |
| /samara_vdnh | `/media/samara_vdnh-1.mp4` | 4_.mp4 |
| /samara_vdnh | `/media/samara_vdnh-2.mp4` | 1_.mp4 |
| /samara_vdnh | `/media/samara_vdnh-3.mp4` | 5_.mp4 |
| /samara_vdnh | `/media/samara_vdnh-4.mp4` | 7_-_.mp4 |
| /samara_vdnh | `/media/samara_vdnh-5.mp4` | 2_.mp4 |
| /samara_vdnh | `/media/samara_vdnh-6.mp4` | 3_.mp4 |
| /samara_vdnh | `/media/samsung-new-year-2020.mp4` | Samsung 2020.mp4 |
| /video/eaton | `/media/presentation-eaton-russia.mp4` | Presentation_Eaton_Russia.mp4 |
| /video/gaz | `/media/gazelle-transformer.mp4` | GAZelle Transformer.mp4 |
| /video/interplastika | `/media/interplastica-messe-duesseldorf.mp4` | Interplastica Messe Duesseldorf.mp4 |
| /video/lingerie | `/media/video-lingerie-hand-marketing.mp4` | Video Lingerie Hand Marketing.mp4 |
| /video/mozaika | `/media/as-mozaika.mp4` | AS Mozaika.mp4 |
| /video/patriot | `/media/eaton-yaz.mp4` | Eaton Yaz.mp4 |
| /video/powertechnologies | `/media/pt-film-long.mp4` | PT Film LONG.mp4 |
| /video/powertechnologies | `/media/pt-film-short.mp4` | PT Film SHORT.mp4 |
| /video/rgd/history | `/media/transrzhd.mp4` | TransRZHD.mp4 |
| /video/salaris | `/media/as-salaris-1.mp4` | AS_Salaris_1.mp4 |
| /video/salaris | `/media/as-salaris-2.mp4` | AS_Salaris_2.mp4 |
| /video/silkway | `/media/silkway-3d.mp4` | 3D Silk Way.mp4 |
| /video/vivax | `/media/vivax-samburskaya.mp4` | Vivax&Samburskaya.mp4 |
| /zubovo | `/media/technopark-zubovo.mp4` | technopark-zubovo.mp4 |
| /zubovo | `/media/silkway-3d.mp4` | 3D Silk Way.mp4 |

## Новая страница /videoproduction (контент weshow, 07.07.2026)

Файлы лежат в `media/` в корне репо, заливаются вручную в `/media/` на хостинг.
Остальные примеры страницы (vivax, eaton-yaz, transrzhd, pt-film-long,
gazelle-transformer, event-riviera, salaris-event-fin180416) уже на сервере.

| Блок | Файл на хостинге | Исходник |
|---|---|---|
| hero (зацикленный луп) | `/media/vp-hero-loop.mp4` | нарезка из шоурила weshow, 14 с, 1.9 МБ |
| Репортажные: форум «Россия» | `/media/samara-vdnh-report.mp4` | Dropbox weshow |
| Обучающие: Saint-Gobain | `/media/saint-gobain-training.mp4` | Dropbox weshow (пережат 720p) |
| Видеопрезентации | `/media/samara-pres-4elements.mp4` | Dropbox weshow (пережат) |
| Видеопрезентации | `/media/samara-pres-5spirits.mp4` | Dropbox weshow (пережат) |
| Видеопрезентации | `/media/samara-pres-vizual-1.mp4` | Dropbox weshow |
| Видеопрезентации | `/media/samara-pres-vizual-2.mp4` | Dropbox weshow |
| Видеопрезентации | `/media/samara-pres-content.mp4` | Dropbox weshow (пережат) |

## Новая страница /content (мультимедийный контент, 07.07.2026)

Файлы в `media/` в корне репо, заливать в `/media/` на хостинг.
Naked Eye 3D переиспользует уже залитый `/media/stavropol-vdnh-nakedeye.mp4` — заливать не надо.

| Блок | Файл на хостинге | Исходник |
|---|---|---|
| Графическое оформление | `/media/content-graphics.mp4` | Dropbox weshow (пережат 720p, 46 МБ) |
| Мэппинг на архитектуре | `/media/content-mapping-arch.mp4` | Dropbox weshow (пережат, 7.6 МБ) |
| Изогнутые экраны | `/media/content-mapping-curved.mp4` | Dropbox weshow (пережат, 25 МБ) |
| Инфо-панели | `/media/content-infopanels.mp4` | Dropbox weshow (пережат, 21 МБ) |
| Адаптация (автолуп) | `/media/content-adaptation-loop.mp4` | нарезка 10 с из ролика изогнутых экранов (0.8 МБ; у weshow этого видео нет — их файл битый) |
| hero (зацикленная нарезка) | `/media/content-hero-loop.mp4` | 19 с / 2 МБ, только 3D-контент: трансформация робота + нога робота в лужу (Газель), маппинг Ставрополя, огненная заставка, 3D Шёлковый путь, Волга с ладьями и мостом, закат с лодками, ракета |