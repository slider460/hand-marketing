// PDF текущей версии страницы /for/alidi/ (без архива). Ролики заменяются обложками.
// Запуск: node scripts/alidi-page/pdf.mjs [http://localhost:8091]  → mirror/for/alidi/alidi-materials.pdf
// Нужен локальный сервер mirror-php (.claude/launch.json) и свежий _preview-page.html (python3 scripts/alidi-page/build.py).
import { chromium } from '/Users/aleksandrnarodetskii/.npm/_npx/6f4879659183bc49/node_modules/playwright/index.mjs';
import { fileURLToPath } from 'url';
import path from 'path';

const base = process.argv[2] || 'http://localhost:8091';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const out = path.join(root, 'mirror/for/alidi/alidi-materials.pdf');

const b = await chromium.launch({ channel: 'chrome' });
const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
await p.goto(base + '/for/alidi/_preview-page.html', { waitUntil: 'networkidle' });
const version = await p.evaluate(() => {
  // ролики → обложки
  document.querySelectorAll('.ex-v video, .vid0 video, .mp video').forEach(v => {
    const w = document.createElement('div'); w.className = 'pv-wrap';
    const i = document.createElement('img'); i.className = 'pv'; i.src = v.getAttribute('poster');
    w.appendChild(i); v.replaceWith(w);
  });
  // ленивые картинки грузим сразу
  document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager');
  const m = document.querySelector('.memo-side .pdf-dl .mono');
  return m ? m.textContent.replace('версия от ', '') : '';
});
await p.evaluate(async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
});
await p.pdf({
  path: out, format: 'A4', scale: 0.62, printBackground: true,
  margin: { top: '12mm', bottom: '14mm', left: '0', right: '0' },
  displayHeaderFooter: true,
  headerTemplate: '<div></div>',
  footerTemplate: `<div style="width:100%;font:8px Arial;color:#8a8a93;padding:0 14mm;display:flex;justify-content:space-between">
    <span>Hand Marketing для ГК АЛИДИ · материалы, версия от ${version} · hand-marketing.ru/for/alidi</span>
    <span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
});
await b.close();
console.log('PDF:', out, 'версия', version);
