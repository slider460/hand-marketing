#!/usr/bin/env node
// Генерирует sitemap.xml из СТРУКТУРЫ ЗЕРКАЛА (mirror/**/index.html) —
// список URL не ведётся руками и не может устареть: что задеплоено, то и в sitemap.
// lastmod — из mtime страницы. Пишет mirror/sitemap.xml (боевой) и копию в public/.
import { writeFileSync, statSync, globSync } from 'node:fs'
import { join } from 'node:path'

const ROOT = new URL('..', import.meta.url).pathname
const BASE = 'https://hand-marketing.ru'

const pages = globSync(join(ROOT, 'mirror/**/index.html'))
  .filter((f) => !f.includes('/static/'))
  // /for/** — приватные клиентские страницы (доступ по коду), в sitemap не попадают
  .filter((f) => !f.includes('/mirror/for/'))
  .map((f) => ({
    loc: f.replace(join(ROOT, 'mirror'), '').replace(/index\.html$/, ''),
    lastmod: statSync(f).mtime.toISOString().slice(0, 10),
  }))
  .sort((a, b) => a.loc.localeCompare(b.loc))

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map((p) => `  <url><loc>${BASE}${p.loc}</loc><lastmod>${p.lastmod}</lastmod></url>`).join('\n')}
</urlset>
`
writeFileSync(join(ROOT, 'mirror/sitemap.xml'), xml)
writeFileSync(join(ROOT, 'public/sitemap.xml'), xml)
console.log(`sitemap.xml: ${pages.length} URL (mirror/ + копия в public/)`)
