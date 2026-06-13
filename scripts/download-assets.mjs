#!/usr/bin/env node
/**
 * Скачивает все изображения с tildacdn в public/assets по манифесту.
 * Запуск: npm run assets
 * После успешного скачивания создаёт .env.local с VITE_LOCAL_ASSETS=1 —
 * сайт переключается на локальные файлы и перестаёт зависеть от Тильды.
 */
import { createWriteStream, existsSync, mkdirSync, statSync, writeFileSync } from 'node:fs'
import { get } from 'node:https'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import manifest from '../src/data/assets-manifest.json' with { type: 'json' }

const root = dirname(dirname(fileURLToPath(import.meta.url)))
const outDir = join(root, 'public')
mkdirSync(join(outDir, 'assets'), { recursive: true })

const entries = Object.entries(manifest)
let done = 0
let failed = 0

function download(url, dest, attempt = 1) {
  return new Promise((resolve) => {
    const file = createWriteStream(dest)
    get(url, (res) => {
      if (res.statusCode >= 300 && res.headers.location) {
        file.close()
        return resolve(download(res.headers.location, dest, attempt))
      }
      if (res.statusCode !== 200) {
        file.close()
        if (attempt < 3) return resolve(download(url, dest, attempt + 1))
        failed++
        console.error(`  FAIL ${res.statusCode} ${url}`)
        return resolve(false)
      }
      res.pipe(file)
      file.on('finish', () => {
        file.close()
        done++
        if (done % 25 === 0) console.log(`  ${done}/${entries.length}…`)
        resolve(true)
      })
    }).on('error', () => {
      file.close()
      if (attempt < 3) return resolve(download(url, dest, attempt + 1))
      failed++
      console.error(`  FAIL net ${url}`)
      resolve(false)
    })
  })
}

console.log(`Скачиваю ${entries.length} файлов с tildacdn…`)
const CONCURRENCY = 8
let i = 0
async function worker() {
  while (i < entries.length) {
    const [url, local] = entries[i++]
    const dest = join(outDir, local)
    if (existsSync(dest) && statSync(dest).size > 0) {
      done++
      continue
    }
    await download(url, dest)
  }
}
await Promise.all(Array.from({ length: CONCURRENCY }, worker))

console.log(`Готово: ${done} ок, ${failed} ошибок.`)
if (failed === 0) {
  writeFileSync(join(root, '.env.local'), 'VITE_LOCAL_ASSETS=1\n')
  console.log('Создан .env.local (VITE_LOCAL_ASSETS=1) — сайт использует локальные ассеты.')
} else {
  console.log('Есть ошибки — .env.local не создан, сайт продолжит использовать tildacdn. Перезапустите скрипт.')
}
