#!/usr/bin/env node
// Генерирует sitemap.xml из СТРУКТУРЫ ЗЕРКАЛА (mirror/**/index.html) —
// список URL не ведётся руками и не может устареть: что задеплоено, то и в sitemap.
// lastmod — из mtime страницы. Пишет mirror/sitemap.xml (боевой) и копию в public/.
import { writeFileSync, statSync, readFileSync, existsSync, globSync } from 'node:fs'
import { join } from 'node:path'

const ROOT = new URL('..', import.meta.url).pathname
const BASE = 'https://hand-marketing.ru'

const pages = globSync(join(ROOT, 'mirror/**/index.html'))
  .filter((f) => !f.includes('/static/'))
  // /for/** — приватные клиентские страницы (доступ по коду), в sitemap не попадают
  .filter((f) => !f.includes('/mirror/for/'))
  // страницы, чей canonical ведёт на другой адрес: дубль в карте противоречит canonical
  // (случай /samara_vdnh/ -> /portfolio/samara-stand-vdnh/)
  .filter((f) => {
    const loc = f.replace(join(ROOT, 'mirror'), '').replace(/index\.html$/, '')
    // на прод уезжает index-a2.html, если он есть: проверяем именно его
    const a2 = f.replace(/index\.html$/, 'index-a2.html')
    const src = existsSync(a2) ? a2 : f
    const m = readFileSync(src, 'utf8').match(/<link rel="canonical" href="([^"]+)"/)
    if (!m) return true
    return m[1].replace(BASE, '').replace(/\/$/, '') === loc.replace(/\/$/, '')
  })
  .map((f) => ({
    loc: f.replace(join(ROOT, 'mirror'), '').replace(/index\.html$/, ''),
    // на прод уезжает index-a2.html, если он есть: дата правки берётся с него,
    // иначе главная и тильдовские страницы годами висят с датой мёртвого index.html
    lastmod: (() => {
      const a2 = f.replace(/index\.html$/, 'index-a2.html')
      const t = Math.max(statSync(f).mtimeMs, existsSync(a2) ? statSync(a2).mtimeMs : 0)
      return new Date(t).toISOString().slice(0, 10)
    })(),
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
