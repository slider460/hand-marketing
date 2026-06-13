// Полное отвязывание зеркала от Tilda:
// 1) убрать dns-prefetch на tildacdn; 2) убрать tilda-stat и tilda-fallback;
// 3) нейтрализовать runtime-эндпоинты Tilda в JS; 4) формы -> /api/lead.php;
// 5) переименовать каталоги/файлы tilda-* в нейтральные и переписать ссылки.
import { readFile, writeFile, rename, mkdir } from 'node:fs/promises'
import { globSync } from 'node:fs'
import path from 'node:path'
import { execSync } from 'node:child_process'

const ROOT = new URL('..', import.meta.url).pathname
const M = path.join(ROOT, 'mirror')

const htmlFiles = execSync(`find ${M} -name '*.html'`).toString().trim().split('\n')
const cssFiles = execSync(`find ${M} -name '*.css'`).toString().trim().split('\n').filter(Boolean)
const jsFiles = execSync(`find ${M} -name '*.js'`).toString().trim().split('\n').filter(Boolean)

// --- 1-2: правки HTML
for (const f of htmlFiles) {
  let s = await readFile(f, 'utf8')
  s = s.replace(/<link rel="dns-prefetch" href="https:\/\/[a-z.]*tildacdn\.com">\s*/g, '')
  // tilda-stat: скрипт + инлайн-инициализации Tilda.sendEventToStatistics и пр.
  s = s.replace(/<script[^>]*src="[^"]*tilda-stat-[^"]*"[^>]*><\/script>\s*/g, '')
  s = s.replace(/<script[^>]*src="[^"]*tilda-fallback-[^"]*"[^>]*( data-[a-z-]+="[^"]*")*><\/script>\s*/g, '')
  s = s.replace(/<script[^>]*src="[^"]*tilda-upwidget-[^"]*"[^>]*><\/script>\s*/g, '')
  await writeFile(f, s)
}
console.log('HTML: prefetch/stat/fallback/upwidget убраны')

// --- 3-4: нейтрализация эндпоинтов в JS
const jsRepl = [
  ['https://stat.tildaapi.', 'https://blackhole.invalid.'],
  ['https://forms.tildacdn.com/procces/', '/api/lead.php?'],
  ['https://upwidget.tildacdn.com/upload/', '/api/none/'],
  ['"store.tildaapi.com"', '"blackhole.invalid"'],
  ['"store2.tildaapi."', '"blackhole.invalid."'],
]
for (const f of jsFiles) {
  let s = await readFile(f, 'utf8')
  let s0 = s
  for (const [a, b] of jsRepl) s = s.split(a).join(b)
  if (s !== s0) await writeFile(f, s)
}
console.log('JS: эндпоинты Tilda нейтрализованы')

// --- 5: переименования
const dirMap = {
  static_tildacdn_com: 'cdn',
  neo_tildacdn_com: 'neo',
  thb_tildacdn_com: 'thb',
}
for (const [a, b] of Object.entries(dirMap)) {
  try { await rename(path.join(M, 'static', a), path.join(M, 'static', b)) } catch {}
}
// файлы tilda-*.js / tilda-*.css -> lib-*
const renames = []
for (const f of execSync(`find ${M}/static -name 'tilda-*'`).toString().trim().split('\n').filter(Boolean)) {
  const nf = path.join(path.dirname(f), path.basename(f).replace(/^tilda-/, 'lib-'))
  await rename(f, nf)
  renames.push([path.basename(f), path.basename(nf)])
}
// переписать ссылки во всех текстовых файлах
const textFiles = execSync(`find ${M} -name '*.html' -o -name '*.css' -o -name '*.js' -o -name '*.json'`).toString().trim().split('\n').filter(Boolean)
for (const f of textFiles) {
  let s = await readFile(f, 'utf8')
  let s0 = s
  for (const [a, b] of Object.entries(dirMap)) s = s.split('static/' + a).join('static/' + b)
  for (const [a, b] of renames) s = s.split(a).join(b)
  if (s !== s0) await writeFile(f, s)
}
console.log('Переименовано: каталоги', Object.keys(dirMap).length, ', файлов tilda-*:', renames.length)
