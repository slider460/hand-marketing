// Зеркало кейса weshow.su/portfolio/samara-stand-vdnh в mirror/:
// SPA index.html -> mirror/portfolio/samara-stand-vdnh/index.html,
// все JS/CSS-чанки -> mirror/assets/, картинки -> mirror/portfolio/samara-vdnh/...
import { mkdir, writeFile, readFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import path from 'node:path'

const ROOT = new URL('..', import.meta.url).pathname
const M = path.join(ROOT, 'mirror')
const SITE = 'https://weshow.su'
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

async function get(u) {
  for (let i = 0; i < 3; i++) {
    try {
      const r = await fetch(u, { headers: { 'user-agent': UA } })
      if (r.ok) return Buffer.from(await r.arrayBuffer())
    } catch {}
    await new Promise((s) => setTimeout(s, 700))
  }
  return null
}

async function save(rel, buf) {
  const fp = path.join(M, rel)
  await mkdir(path.dirname(fp), { recursive: true })
  await writeFile(fp, buf)
}

// 1. index.html
const idx = (await get(SITE + '/portfolio/samara-stand-vdnh')).toString('utf8')

// 2. собрать ассеты рекурсивно
const queue = [...new Set([...idx.matchAll(/\/assets\/[A-Za-z0-9._-]+\.(?:js|css)/g)].map((m) => m[0]))]
const seen = new Set(queue)
const media = new Set()
let n = 0
while (queue.length) {
  const rel = queue.shift()
  const buf = await get(SITE + rel)
  if (!buf) { console.log('FAIL', rel); continue }
  await save(rel, buf)
  n++
  if (/\.(js|css)$/.test(rel)) {
    const s = buf.toString('utf8')
    // транзитивные чанки
    for (const m of s.matchAll(/(?:\.\/|\/assets\/)([A-Za-z0-9._-]+\.(?:js|css))/g)) {
      const r = '/assets/' + m[1]
      if (!seen.has(r)) { seen.add(r); queue.push(r) }
    }
    // медиа по абсолютным путям
    for (const m of s.matchAll(/"(\/(?:images|portfolio|videos|media|fonts)\/[A-Za-z0-9/._ -]+\.(?:jpg|jpeg|png|webp|svg|mp4|woff2?|ico))"/g)) {
      media.add(m[1])
    }
  }
}
console.log('чанков:', n)

// favicon и manifest
for (const r of ['/favicon.svg', '/favicon.ico', '/site.webmanifest']) media.add(r)

let mok = 0, mfail = 0
for (const rel of media) {
  if (existsSync(path.join(M, rel))) { mok++; continue }
  const buf = await get(SITE + encodeURI(rel))
  if (!buf) { console.log('MEDIA FAIL', rel); mfail++; continue }
  await save(rel, buf)
  mok++
}
console.log('медиа:', mok, 'ошибок:', mfail)

// 3. страница
await save('portfolio/samara-stand-vdnh/index.html', Buffer.from(idx))
console.log('Готово: /portfolio/samara-stand-vdnh')
