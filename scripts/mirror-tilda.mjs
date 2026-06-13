// Зеркало hand-marketing.ru (Tilda) -> mirror/ : HTML + CSS/JS/шрифты/картинки локально.
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import path from 'node:path'

const ROOT = new URL('..', import.meta.url).pathname
const OUT = path.join(ROOT, 'mirror')
const SITE = 'https://hand-marketing.ru'

const sitemap = await readFile(path.join(ROOT, 'public/sitemap.xml'), 'utf8')
const pages = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1])

const assetMap = new Map() // remote url -> local rel path
const queue = []

function localAssetPath(u) {
  const url = new URL(u)
  let p = url.hostname.replace(/\./g, '_') + url.pathname
  if (url.pathname === '/' || url.pathname === '') p += 'index'
  p = p.replace(/[?#].*$/, '')
  if (!/\.[a-z0-9]{1,5}$/i.test(p)) p += '.bin'
  return 'static/' + p
}

function registerAsset(u) {
  try {
    u = u.replace(/&amp;/g, '&')
    const url = new URL(u, SITE)
    if (!/^https?:$/.test(url.protocol)) return null
    const host = url.hostname
    if (!/tildacdn|tilda(cdn)?\.|static\.tildacdn|hand-marketing\.ru/.test(host)) return null
    if (host.includes('hand-marketing.ru') && !/\.(css|js|png|jpe?g|svg|gif|webp|ico|woff2?|ttf|mp4)$/i.test(url.pathname)) return null
    const key = url.href.split('#')[0]
    if (!assetMap.has(key)) {
      assetMap.set(key, localAssetPath(key))
      queue.push(key)
    }
    return assetMap.get(key)
  } catch {
    return null
  }
}

async function fetchBuf(u, tries = 3) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(u, {
        headers: {
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
          accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'accept-language': 'ru-RU,ru;q=0.9',
        },
      })
      if (r.ok) return Buffer.from(await r.arrayBuffer())
    } catch {}
    await new Promise((s) => setTimeout(s, 500 * (i + 1)))
  }
  return null
}

function pageOutPath(u) {
  const p = new URL(u).pathname.replace(/\/$/, '')
  return path.join(OUT, p === '' ? 'index.html' : p.slice(1) + '/index.html')
}

// глубина страницы -> префикс к static/
function relPrefix(u) {
  const p = new URL(u).pathname.replace(/\/$/, '')
  const depth = p === '' ? 0 : p.slice(1).split('/').length
  return '../'.repeat(depth)
}

const URL_RE = /https?:\/\/(?:[a-z0-9-]+\.)*(?:tildacdn\.[a-z.]+|tilda\.ws|hand-marketing\.ru)\/(?:(?!&quot|&amp)[^\s"'()<>\\;])+/gi

console.log(`Страниц: ${pages.length}`)
const htmls = new Map()
for (const u of pages) {
  if (existsSync(pageOutPath(u))) { process.stdout.write('s'); continue }
  let buf = await fetchBuf(u, 5)
  if (!buf) { await new Promise((s) => setTimeout(s, 10000)); buf = await fetchBuf(u, 5) }
  if (!buf) { console.error('FAIL page', u); continue }
  htmls.set(u, buf.toString('utf8'))
  await new Promise((s) => setTimeout(s, 1500))
  process.stdout.write('.')
}
console.log('\nHTML скачан. Сбор ассетов…')

// зарегистрировать ассеты со всех страниц
for (const h of htmls.values()) for (const m of h.matchAll(URL_RE)) registerAsset(m[0])

// скачать ассеты (CSS может тянуть ещё — обрабатываем очередь)
let done = 0
const failed = []
while (queue.length) {
  const u = queue.shift()
  const rel = assetMap.get(u)
  const fp = path.join(OUT, rel)
  if (!existsSync(fp)) {
    const buf = await fetchBuf(u)
    if (!buf) { failed.push(u); continue }
    await mkdir(path.dirname(fp), { recursive: true })
    if (/\.css$/i.test(rel)) {
      let css = buf.toString('utf8')
      for (const m of css.matchAll(URL_RE)) registerAsset(m[0])
      // url(...) относительные к CDN — оставляем абсолютные ссылки переписанными ниже вторым проходом
      await writeFile(fp, css)
    } else {
      await writeFile(fp, buf)
    }
  }
  if (++done % 50 === 0) console.log(`  ассеты: ${done}, осталось ~${queue.length}`)
}
console.log(`Ассетов: ${done}, ошибок: ${failed.length}`)

// второй проход по CSS: переписать ссылки внутри css на относительные (css лежит в static/<host>/...)
for (const [u, rel] of assetMap) {
  if (!/\.css$/i.test(rel)) continue
  const fp = path.join(OUT, rel)
  if (!existsSync(fp)) continue
  let css = await readFile(fp, 'utf8')
  const up = '../'.repeat(rel.split('/').length - 1) // от файла css к корню mirror
  css = css.replace(URL_RE, (m) => {
    const r = assetMap.get(m.split('#')[0].replace(/&amp;/g, '&'))
    return r ? up + r : m
  })
  await writeFile(fp, css)
}

// записать страницы с переписанными ссылками
for (const [u, h] of htmls) {
  const pre = relPrefix(u)
  let out = h.replace(URL_RE, (m) => {
    const key = m.split('#')[0].replace(/&amp;/g, '&')
    const r = assetMap.get(key)
    if (r) return pre + r
    // внутренние ссылки на страницы -> относительные пути
    try {
      const url = new URL(m)
      if (url.hostname === 'hand-marketing.ru') return url.pathname + url.search
    } catch {}
    return m
  })
  const fp = pageOutPath(u)
  await mkdir(path.dirname(fp), { recursive: true })
  await writeFile(fp, out)
}
console.log('Готово -> mirror/')
if (failed.length) console.log('Не скачалось:', failed.slice(0, 10))
