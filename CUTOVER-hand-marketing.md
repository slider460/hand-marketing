# Перенос сайта на боевой домен hand-marketing.ru

Рунбук перевода `hand-marketing.ru` с Тильды на наш статический билд.

## Вводные (проверено 29.06.2026)

| Что | Значение |
|---|---|
| Хостинг (целевой) | **Reg.ru**, IP `31.31.197.38` — тот же сервер, где сейчас стейджинг `weshowstudia.ru` |
| Стек сервера | nginx (фронт) + **Apache-бэкенд читает `.htaccess`** + PHP-FPM (формы работают) |
| Домен hand-marketing.ru | NS на **nic.ru** (`ns3-l2.nic.ru` …), сейчас A-запись → `185.215.4.10` (ddos-guard → Тильда) |
| Билд | `mirror/` — автономная статика, CI льёт её на сервер при пуше в `main` |

**Идея переезда:** добавить `hand-marketing.ru` вторым доменом на тот же аккаунт/docroot Reg.ru, выпустить TLS, затем переключить A-записи на nic.ru с `185.215.4.10` на `31.31.197.38`. CI и код менять не нужно — docroot общий со стейджингом.

## Готовность билда — ПОДТВЕРЖДЕНО ✅

- Канонические ссылки, `og:url`, `sitemap.xml` (59 URL), `robots.txt` → уже `hand-marketing.ru`.
- Внешних обращений к Tilda/tildacdn нет — вся статика локальная.
- Формы постят в `/api/lead.php`; PHP на сервере работает (проверено GET → `405 JSON`). Получатель писем: `info@hand-marketing.ru` (`mirror/api/lead.php`, `$TO`).
- ЧПУ-редиректы (trailing slash) и host-своп `robots.txt` для стейджинга работают (Apache `.htaccess`).
- Все 20 видео в `/media/` (включая Ставрополь) и картинки кейсов `/case-assets/` — на сервере.
- `.htaccess` закрывает стейджинг `weshowstudia.ru` от индексации (`X-Robots-Tag: noindex`); боевой домен не затрагивается.

## Шаги переноса

### 1. Reg.ru — добавить домен (ДО смены DNS)
1. Панель Reg.ru → хостинг-аккаунт со стейджингом → **добавить домен/алиас** `hand-marketing.ru` (и `www.hand-marketing.ru`) **на тот же сайт/docroot**, что и `weshowstudia.ru`.
2. Включить **бесплатный Let's Encrypt SSL** для `hand-marketing.ru` + `www`.
   - Если панель выпускает сертификат HTTP-проверкой — выпуск пройдёт только ПОСЛЕ шага 2 (когда A-запись уже укажет на Reg.ru). Тогда последовательность: сменить DNS → дождаться → выпустить сертификат → включить редирект на HTTPS.
   - Если доступна DNS-проверка (DNS-01) — можно выпустить сертификат заранее, до смены A-записи, и тогда HTTPS заработает сразу в момент переключения.

### 2. nic.ru — переключить DNS
1. **Заранее** (за сутки) снизить TTL A-записей `hand-marketing.ru` и `www` до 300 сек — ускорит откат/распространение.
2. В DNS-панели nic.ru заменить:
   - `hand-marketing.ru` A `185.215.4.10` → **`31.31.197.38`**
   - `www.hand-marketing.ru` → **`31.31.197.38`** (A) или CNAME на `hand-marketing.ru`
   - убрать прочие записи, ведущие на ddos-guard/Тильду.
3. Дождаться распространения (`dig +short hand-marketing.ru` → `31.31.197.38`).

### 3. Канонические редиректы (после выпуска TLS)
Включить в **панели Reg.ru** (надёжнее, чем `.htaccess` за их nginx-прокси):
- **www → без www**
- **http → https**

> ⚠️ НЕ добавлять `http→https` в `.htaccess` вслепую: TLS терминирует nginx-фронт, Apache-бэкенд может видеть `HTTPS=off` → бесконечный цикл редиректа. Если делать в `.htaccess`, проверять по `%{HTTP:X-Forwarded-Proto}`, а не `%{HTTPS}`, и сначала убедиться, что цикла нет. По умолчанию — тумблер в панели.

### 4. Проверка после переключения
```bash
curl -sI https://hand-marketing.ru/ | grep -iE 'server|x-tilda|location|content-type'   # x-tilda НЕ должен присутствовать
curl -sI http://hand-marketing.ru/  | grep -i location                                    # http -> https 301
curl -sI https://www.hand-marketing.ru/ | grep -i location                                # www -> без www 301
curl -s  https://hand-marketing.ru/robots.txt        # Allow: / (боевой, НЕ staging-Disallow)
curl -s -o /dev/null -w '%{http_code}\n' https://hand-marketing.ru/api/lead.php           # 405 (PHP жив)
```
Глазами: главная (десктоп = Тильда 1:1, мобайл = кастомный), кейсы, видео-плееры, отправка формы (письмо на `info@hand-marketing.ru` + строка в `api/leads.csv`).

### 5. Откат
Вернуть на nic.ru A-записи `hand-marketing.ru`/`www` → `185.215.4.10`. С низким TTL откат — минуты.

## После успешного переезда
- Сообщить пользователю про кэш ddos-guard/браузера (жёсткий refresh, см. `deploy-hand-marketing` в памяти).
- Тильда-подписку можно не продлевать (домен больше не на ней).
- Стейджинг `weshowstudia.ru` остаётся как тест-зеркало (закрыт от индексации).
