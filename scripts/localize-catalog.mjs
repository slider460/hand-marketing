// Локализация каталогов Tilda: выкачивает productslist для каждого storepart
// и вшивает в страницы XHR-патч, который перенаправляет запросы на локальные JSON.
import { readFile, writeFile, mkdir } from 'node:fs/promises'
import path from 'node:path'

const ROOT = new URL('..', import.meta.url).pathname
const MIRROR = path.join(ROOT, 'mirror')
const API = path.join(MIRROR, 'api')
await mkdir(API, { recursive: true })

const pages = [
  'index.html', 'project/index.html', 'event/index.html', 'creativedesign/index.html',
  'videoproduction/index.html', 'digital/index.html', '3dmapping/index.html', 'printandproduction/index.html',
]

const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

const PATCH = `<script>(function(){var o=XMLHttpRequest.prototype.open;XMLHttpRequest.prototype.open=function(m,u){if(typeof u==='string'&&u.indexOf('tildaapi.com')>-1){var sp=(u.match(/storepartuid=(\\d+)/)||[])[1];if(u.indexOf('getproductslist')>-1&&sp)u='/api/getproductslist_'+sp+'.json';else if(u.indexOf('getfilters')>-1)u='/api/getfilters.json';}return o.apply(this,[m,u].concat([].slice.call(arguments,2)))};})();</script>`

for (const rel of pages) {
  const fp = path.join(MIRROR, rel)
  let html = await readFile(fp, 'utf8')
  const parts = [...html.matchAll(/storepart:'(\d+)'/g)].map((m) => m[1])
  const recs = [...html.matchAll(/id="rec(\d+)"/g)].map((m) => m[1])
  for (const sp of new Set(parts)) {
    const out = path.join(API, `getproductslist_${sp}.json`)
    const url = `https://store.tildaapi.com/api/getproductslist/?storepartuid=${sp}&recid=${recs[0]}&c=${Date.now()}&getparts=true&getoptions=true&slice=1&size=200`
    const r = await fetch(url, { headers: { 'user-agent': UA, referer: 'https://hand-marketing.ru/' + rel.replace('/index.html', '').replace('index.html', '') } })
    const j = await r.text()
    await writeFile(out, j)
    let total = 'n/a'
    try { total = JSON.parse(j).total } catch {}
    console.log(rel, 'storepart', sp, '-> total:', total)
    await new Promise((s) => setTimeout(s, 500))
  }
  if (parts.length && !html.includes('tildaapi.com')) { /* nothing */ }
  if (parts.length && !html.includes("getproductslist_'")) {
    if (!html.includes('XMLHttpRequest.prototype.open=function(m,u)')) {
      html = html.replace('</head>', PATCH + '</head>')
      await writeFile(fp, html)
    }
  }
}
console.log('Готово')
