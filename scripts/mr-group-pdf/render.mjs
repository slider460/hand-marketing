// Печать out/print.html в mirror/for/mr-group/mr-proposal.pdf (A4 альбом, векторный текст и QR).
// Playwright берётся из npx-кэша, браузер системный Chrome (см. память preview-screenshots-playwright).
import { chromium } from '/Users/aleksandrnarodetskii/.npm/_npx/6f4879659183bc49/node_modules/playwright/index.mjs';
import path from 'path';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = 'file://' + path.join(here, 'out', 'print.html');
const out = process.argv[2] || path.join(here, '..', '..', 'mirror', 'for', 'mr-group', 'mr-proposal.pdf');

const b = await chromium.launch({ channel: 'chrome' });
const p = await b.newPage();
await p.goto(src, { waitUntil: 'load' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: out, width: '297mm', height: '210mm', printBackground: true, preferCSSPageSize: true });
await b.close();
console.log(out);
