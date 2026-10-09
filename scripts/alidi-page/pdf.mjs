// PDF-презентация для АЛИДИ: слайды 1280×720 из _preview-slides.html (собирает slides.py).
// Запуск: python3 scripts/alidi-page/slides.py && node scripts/alidi-page/pdf.mjs [http://localhost:8091]
// Нужен локальный сервер mirror-php (.claude/launch.json). Выход: mirror/for/alidi/alidi-materials.pdf
import { chromium } from '/Users/aleksandrnarodetskii/.npm/_npx/6f4879659183bc49/node_modules/playwright/index.mjs';
import { fileURLToPath } from 'url';
import path from 'path';

const base = process.argv[2] || 'http://localhost:8091';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const out = path.join(root, 'mirror/for/alidi/alidi-materials.pdf');

const b = await chromium.launch({ channel: 'chrome' });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(base + '/for/alidi/_preview-slides.html', { waitUntil: 'networkidle' });
await p.evaluate(async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
});
await p.pdf({ path: out, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true });
await b.close();
console.log('PDF:', out);
