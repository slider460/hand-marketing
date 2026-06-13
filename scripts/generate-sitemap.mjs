#!/usr/bin/env node
// Генерирует public/sitemap.xml по реестру страниц и кейсов
import { writeFileSync } from 'node:fs'
import cases from '../src/data/cases.json' with { type: 'json' }

const BASE = 'https://hand-marketing.ru'
const staticRoutes = ['/', '/about', '/service', '/project', '/clients', '/contacts', '/privacy',
  '/event', '/creativedesign', '/videoproduction', '/printandproduction', '/btl', '/digital', '/3dmapping']
const urls = [...staticRoutes, ...cases.map((c) => c.route)]
const today = new Date().toISOString().slice(0, 10)
const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((u) => `  <url><loc>${BASE}${u}</loc><lastmod>${today}</lastmod></url>`).join('\n')}
</urlset>
`
writeFileSync(new URL('../public/sitemap.xml', import.meta.url), xml)
console.log(`sitemap.xml: ${urls.length} URL`)
