# AUDIT.md — комплексный аудит кодовой базы hand-marketing.ru

**Дата:** 09.07.2026
**Метод:** 5 параллельных read-only проверок (качество кода, баги, безопасность, SEO, остатки Tilda). В проект изменения не вносились.
**Контекст:** в репозитории две кодовые базы — React SPA в корне (`src/`) и Astro-слой в `site/`; прод (зеркало `mirror/`) — 62 пре-рендеренных статических HTML + React-чанки `/portfolio/*` + PHP-хендлер форм.

---

## Сводка

Миграция с Tilda в своей основе выполнена чисто: в проде **ни одной ссылки на tildacdn**, битых картинок нет (0 отсутствующих, регистр путей везде совпадает), токены и креды в git не утекали (проверены все 93 коммита), прод индексируется — 62 статических HTML с уникальными title и canonical.

Три системные проблемы:

1. **Формы теряют заявки** — форма на `/videoproduction` несовместима с `lead.php` (заявки падают с 422), а боевая версия хендлера имеет CRLF-инъекцию и публичный диагностический endpoint.
2. **Внешние зависимости вопреки правилам проекта** — Google Fonts на 123 прод-страницах (локальных woff2 фирменных шрифтов в проекте нет вообще) и ~30 видео с Dropbox в проде, при том что большинство роликов уже залито в `/media`, но код на них не переключён.
3. **«Двоевластие» React ↔ Astro** — две базы расходятся в адресе офиса, палитре, шрифтах и контракте форм; деплой Astro-сборки в общий docroot перекроет React-роуты и может дать белый экран всего сайта.

---

## 🔴 КРИТИЧНО

### К1. Форма на /videoproduction гарантированно теряет заявки
`site/src/pages/videoproduction.astro:188` — нативный `<form method="post">` с полями `name`/`contact`/`comment`, а `public/api/lead.php:16-21` ждёт `name`+`phone` и валидирует телефон → **любая отправка = 422**, пользователь видит голый JSON вместо «спасибо». Ни одна заявка с этой страницы не доходит. Плюс в `site/public/` вообще нет `api/lead.php` — standalone-сборка Astro без хендлера.

### К2. Dropbox в проде (нарушение правила CLAUDE.md)
- `mirror/mmg/index.html:199` и `mirror/video/salaris/index.html:50,57` — видео грузятся с `dl.dropboxusercontent.com`, **локальных копий нет вообще** (единственная точка отказа).
- 11 React-чанков в `mirror/assets/*.js` (CaseDetail, ShowreelModal, VideoProduction, SalarisCase, CaseStavropol3DMapping и др.) — ~30 Dropbox-URL, при этом локальные файлы **уже лежат** в `/media` (eaton-yaz.mp4, event-riviera.mp4, samara-vdnh-*.mp4, stavropol-vdnh-*.mp4…) — миграция сделана наполовину: файлы залиты, код не переключён.
- `site/src/pages/videoproduction.astro:16-31` — 14 Dropbox-URL в исходнике; прод-страница уже переведена на `/media`, но **пересборка Astro вернёт регресс**.
- Showreel главной: `src/data/site.ts:12` → Dropbox, используется в модалке `src/pages/Home.tsx:179`.

### К3. Битые видео в Astro-контенте
- `site/src/content/projects/isotec.md:12` → `/media/silkway-3d.mp4` — файла нет нигде (ни в `site/public/media`, ни в `media/`, ни в `mirror/media`).
- `site/src/content/projects/mmg.md:12` → `/media/mmg-paveleckaya.mp4` — аналогично.

### К4. Конфликт URL двух кодовых баз при деплое
Astro генерирует физические `/index.html`, `/project/index.html`, `/videoproduction/index.html` — по правилам `.htaccess` они перекроют React-роуты; выгрузка Astro-сборки в текущий docroot затрёт корневой `index.html` SPA → **белый экран всего сайта**. При этом навигация Astro (`Header.astro:17,24`, `Footer.astro:22`, `config/site.ts:33-37`) ссылается на `/contacts`, `/privacy`, `/about`, `/clients`, `/service` — страницы, существующие только в React SPA. Деплоить Astro без плана сшивки нельзя.

### К5. Google Fonts CDN на 123 прод-страницах
Прямое нарушение принципа «всё локально» (CLAUDE.md) + риск при блокировках Google-доменов в РФ:
- прод: 123 HTML в `mirror/` — Montserrat **весь вариативный диапазон 100..900**, Raleway ×6; на `/portfolio/*` дополнительно Inter, JetBrains Mono, Manrope, Space Grotesk, Material Symbols;
- исходники: `index.html:9-11` (корень), `site/src/layouts/Base.astro:32-36`, `site/src/pages/home-b.astro:15-16`.
Локальных woff2 фирменных шрифтов нет ни в `public/`, ни в `site/public/` (только `mirror/static/fonts/circe/`).

### К6. Tilda-заголовки и битые description на прод-страницах
- **28 кейсов** несут сырые Tilda-названия в `<title>`, `h1` и `og:title`: `Event_Changan`, `Creative_ brochure_Ramada`, `Site_Becar`, `MICE_Eaton` и т.п.
- **32 из 62 страниц** — сломанный description: `content=" — Hand Marketing, рекламное агентство полного цикла."` (шаблон подставил пустой заголовок).
Для SEO это самая дешёвая по трудозатратам и самая результативная правка.

---

## 🟡 ВАЖНО

### Безопасность
- **В1. CRLF-инъекция в боевом `mirror/api/lead.php:80-83`** — `$data['email']` вставляется в `Reply-To:` без `FILTER_VALIDATE_EMAIL`; через `\r\n` можно дописать заголовки (Bcc) → потенциальная рассылка спама через сервер. Тело письма собирается из произвольных POST-полей без лимитов (`:61-66`).
- **В2. Диагностический endpoint `?selftest=hm2026`** (`mirror/api/lead.php:19-39`) — раскрывает PHP_VERSION, `disable_functions`, `sendmail_path`, размер leads.csv, триггерит отправку письма в цикле. Ключ захардкожен и лежит в публичном git. Убрать с прода.
- **В3. Три расходящиеся копии lead.php** (`public/`, `mirror/`, `dist-deploy/*`) с разными контрактами (JSON+Telegram vs Tilda-POST+почта). Случайный деплой `public/`-версии поверх боевой отключит уведомления (токены в git-версии пустые — это правильно, но контракт другой).
- **В4. `Access-Control-Allow-Origin: *`** (`mirror/api/lead.php:11`) — постить может любой сайт; для same-origin формы CORS не нужен.

### Баги и данные
- **В5. 23 кейс-страницы React (31 URL) тянут видео с Dropbox, ещё 4 — с weshow.su** (`src/data/pages/`: gaz, eaton, salaris, samsung, riviera, samara_vdnh, zubovo, bekobod1, isotec и др.) — локальные замены в `/media` частично готовы.
- **В6. Расхождение брендовых данных между базами:** адрес офиса — «Рочдельская, 14А» (`src/data/site.ts:5`) vs «наб. Академика Туполева, 15» (`site/src/config/site.ts:33`, `Base.astro:15`); палитры услуг не совпадают ни по одному пункту (event `#96c223` vs `#673A7E`); шрифты — Montserrat+Inter vs Montserrat+**Onest** (`Base.astro:36`). Один из адресов на живом сайте неверен.
- **В7. Fallback на tildacdn зависит от негитуемого `.env.local`** (`src/lib/content.ts:52-60`): сборка на чистом клоне без `VITE_LOCAL_ASSETS=1` молча вернёт сайт на CDN Тильды.
- **В8. Дубль кейса:** `site/src/content/projects/bekobod.md` (заглушка без category) рядом с полноценным `bekobod1.md` — два живых URL `/project/bekobod` и `/project/bekobod1`; похоже на забытый черновик.
- **В9. Astro-слой не закоммичен в git** — несколько недель работы (`site/src/components/`, `content/`, `pages/project/` и т.д.) untracked; риск потери.

### SEO
- **В10. Alt у картинок: 631 из 686 `<img>` в проде — с пустым alt (92%).** Худшие: `mirror/index.html` (65), `/about` (35), `/event/riviera` (20). Для портфолио-сайта — потерянный картиночный трафик. В исходниках: 7 пустых alt в React (`Home.tsx`, `About.tsx`, `Footer.tsx`…).
- **В11. 390 из 1019 jpg/png в проде без .webp-пары** — новые разделы (`case-assets/` — 88, `images/vp/` — 15, `images/services/` — 15, `/portfolio/stavropol-vdnh/` — 5) не прогнаны через `scripts/gen-webp.sh`.
- **В12. `scripts/generate-sitemap.mjs` и `public/sitemap.xml` отстали от прода** (57 vs 62 URL — не знают про /content, /exhibition, /portfolio/*) — следующий прогон скрипта **затрёт свежий sitemap урезанным**.
- **В13. og:image:** `site/public/og.jpg` не существует, а `Base.astro:8` ставит его на все Astro-страницы; на старых прод-страницах og:image — относительные URL (соцсети не подхватят); на Tilda-кейсах отсутствует.
- **В14. Метрика 71125393 не вставлена в Astro-слой** (`site/src/config/site.ts:49` объявлен, но не используется) и отсутствует на `mirror/samara_vdnh/`; визиты на /project/*, /videoproduction не считаются.
- **В15. Экспериментальные страницы `/v2`, `/home-b`, `/compare` попадут в sitemap** — `@astrojs/sitemap` без фильтра включит их в индекс; `compare.astro:31` вдобавок содержит iframe на `http://localhost:8080/`.

### Качество кода / производительность
- **В16. ~400 КБ JSON в основном бандле SPA:** `src/lib/content.ts:70` — eager-glob 58 JSON (376 КБ) + `cases.json` (18 КБ) статически в главный чанк; каждый посетитель главной качает данные всех 43 кейсов. Ленивый glob разрежет бандл на порядок (менять аккуратно — см. правило «не каскадить пере-хеш чанков»).
- **В17. Мёртвые SEO-компоненты:** `site/src/components/SEO.astro` (76 строк) и `Picture.astro` нигде не импортируются; их функциональность вручную задублирована в `Base.astro` и 5 местах с повторяющимися `widths/sizes/formats`. Из-за этого кейсы `/project/[slug]` не получают per-page JSON-LD и og:image.
- **В18. Дубли внутри Astro:** шапка сверстана инлайном заново в `index.astro:15-27` и `v2.astro:16-22` вместо `Header.astro` (3 визуально разных шапки); карточка кейса скопирована 1-в-1 между `project/index.astro` и `videoproduction.astro`; список услуг с цветами живёт в 4 местах.
- **В19. Мыльные дубли логотипов:** `src/data/clients.ts:60-65` — последние 6 записей это `/-/resizeb/20x/` 20-пиксельные копии предыдущих шести; на /clients рендерятся размытыми.
- **В20. 6 fallback-логотипов с `lh3.googleusercontent.com`** в прод-чанке `mirror/assets/SoftwareAndGames-*.js` (Unity, Unreal, WebGL…).
- **В21. 7 сиротских JSON** в `src/data/pages/` (index, about, clients, contacts, project, service, sk) — никем не запрашиваются, но из-за eager-glob попадают в бандл.

---

## 🟢 ЖЕЛАТЕЛЬНО

### Зависимости (dev-only, плановые major-апгрейды)
- **vite ≤6.4.2 — high** (fs.deny bypass, path traversal — только dev-сервер, преимущественно Windows) → vite 8.1.4; заодно закроется esbuild moderate.
- **astro — high** (reflected XSS через slot name, SSRF в prerendered error page) → astro 7.0.7. Прод статический, но XSS-баги рендера теоретически могут попасть в сгенерированный HTML.

### Безопасность
- Анти-спам для форм: rate-limiting, honeypot-поле, CSRF — нет ни в одной версии lead.php.
- CSV-formula-injection в `mirror/api/lead.php:72-77` — экранировать ведущие `=`,`+`,`-`,`@` при записи в leads.csv.
- `.htaccess`: добавить `Options -Indexes` явно, страховочное правило запрета `/.git`, `ErrorDocument 404` (сейчас несуществующие URL отдают честный 404, но голым Apache-дефолтом); CSP-заголовок.
- Следить, чтобы легаси `public/.htaccess` (правило «всё → index.html», даст 200 на любой мусорный URL) не попал в прод.

### Вес ассетов
- Видео 50–93 МБ (`samara-vdnh-30.mp4` 93 МБ, `samara-vdnh-report.mp4` 87 МБ, `transrzhd.mp4` 59 МБ, `pt-film-long.mp4` 58 МБ) — пережать (H.264 CRF 26–28 или AV1).
- 163 картинки >500 КБ; худшее — фотографии в PNG по 2–2.7 МБ (`site/src/assets/projects/creative__patriki/g1.png` 2.68 МБ и др.) — конвертация в JPG/WebP даст −80–90%.
- `loading="lazy"` только у 55 из 686 картинок в проде.

### Гигиена репозитория
- Каталог-опечатка `{public` в корне (след неудавшегося brace-expansion).
- `dist-deploy/` (~290 МБ старых архивов) и устаревший `dist/` (там ещё внешняя иконка `i.ibb.co` в пине карты — в проде уже локальная) — удалить/пересобрать.
- `src/data/assets-manifest.json` (42 КБ) нужен только скрипту миграции — перенести из `src/`.
- Вычистить мёртвые remote-поля tildacdn (`coverRemote`/`photoRemote` в `cases.json`, `clients.ts`, `site.ts`, `pages/*.json` — ~900 вхождений) и remote-ветку в `imgSrc()/coverSrc()` — ассеты давно локальные.
- CLAUDE.md устарел: `npm run deploy` в package.json отсутствует, деплой идёт через GitHub Actions (FTP-креды в Secrets — корректно).

### Код
- Небезопасный cast `casesData as CaseMeta[]` повторён в 5 файлах — вынести один типизированный экспорт в `src/lib/content.ts`; явных `any`/`@ts-ignore` в обеих базах ноль (хороший результат).
- Захардкоженные массивы цветов продублированы в `Home.tsx:110` и `About.tsx:22`.
- ~90 строк контента захардкожено в `videoproduction.astro` (workTypes, presentations) — вынести в `site/src/content/`.
- `src/data/pages/samara_vdnh.json` — 6 URL с `&amp;amp;` вместо `&`; `VideoEmbed.tsx:20` — `.replace('?dl=0','')` не срабатывает для новых `scl/fi`-ссылок Dropbox.
- Модалка showreel (`Home.tsx:159-182`) не закрывается по Escape и не блокирует прокрутку body.
- Мёртвый якорь `#showreel` в `home-b.astro:48`; JSON-LD отсутствует на 3 новых страницах (/content, /exhibition, /videoproduction); для кейсов напрашивается schema.org CreativeWork/VideoObject.

---

## Что в порядке (проверено, проблем нет)

- **tildacdn в проде — 0 вхождений**; все ~900 упоминаний в `src/data` — неактивные remote-фолбэки при живых локальных копиях (358 файлов в `public/assets`).
- **Битых картинок нет:** все `/images/`, `/assets/` пути в обеих базах указывают на существующие файлы, расхождений регистра нет.
- **Роутинг React SPA цел:** все 42 кейс-роута ↔ page-JSON сходятся, дублей роутов нет, catch-all 404 есть, `target="_blank"` без `rel` не найдено.
- **Секреты:** токенов в рабочем дереве и во всей git-истории нет; `leads.csv` в .gitignore и в exclude FTP-синка; `.git` на сервер не заливается.
- **Индексация:** прод отдаёт полноценный статический HTML (не пустой шелл), `mirror/robots.txt` и `mirror/sitemap.xml` (62 URL) корректны, staging закрыт X-Robots-Tag, Яндекс-верификация на месте.
- **`.htaccess` прода:** leads.csv/bak закрыты `Require all denied`, security-заголовки (nosniff, X-Frame-Options, Referrer-Policy) есть.

---

## Рекомендуемый порядок работ

1. **Формы** (К1, В1–В4): починить контракт формы /videoproduction ↔ lead.php, убрать `?selftest`, валидировать email через `FILTER_VALIDATE_EMAIL`, унифицировать копии хендлера. Совпадает с открытой задачей «аудит форм».
2. **Dropbox → /media** (К2, К3, В5): переключить чанки и `videoproduction.astro` на уже залитые локальные файлы; долить отсутствующие mmg/salaris/silkway ролики.
3. **Шрифты локально** (К5): скачать woff2 Montserrat (3–4 начертания, не 100..900) + Inter, прописать `@font-face`, убрать fonts.googleapis.com из всех трёх точек.
4. **Tilda-титулы и description** (К6) — максимальный SEO-эффект при минимальном риске.
5. **План сшивки React ↔ Astro** (К4, В6): решить, кто главный, зафиксировать единый источник бренд-данных (адрес!), закоммитить Astro-слой (В9).
6. Далее по списку «важно»: alt, webp, sitemap-генератор, og.jpg, Метрика в Astro.
