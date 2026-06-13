# hand-marketing.ru — React/Vite

Миграция сайта hand-marketing.ru с Tilda на собственный стек.
Контент: 58 страниц, 43 кейса, 358 изображений — извлечён с живого сайта автоматически.

## Быстрый старт

```bash
npm install
npm run assets   # скачать всю графику с tildacdn -> public/assets (один раз)
npm run dev      # http://localhost:5173
```

## Сборка и деплой

```bash
npm run sitemap && npm run build
# содержимое dist/ -> public_html на хостинге (Apache, PHP >= 7.4)
```

Подробное ТЗ и чек-лист запуска: **ANTIGRAVITY.md**

## Зеркало 1:1 (точная копия Tilda)

Папка `mirror/` — пиксельная копия живого сайта: HTML всех 57 страниц + все CSS/JS/картинки Тильды локально.

```bash
node scripts/mirror-tilda.mjs   # обновить зеркало с живого сайта
npx serve mirror -l 8080        # смотреть: http://localhost:8080
```

Снаружи подгружаются только Яндекс.Метрика, Яндекс.Карты (на /contacts) и showreel-видео с Dropbox.
