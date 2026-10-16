// Скриншоты интерактивных блоков страницы для PDF (окно погружения, пол, LED-фасад).
// Нужен сервер mirror с PHP (launch mirror-php-nomail на :8093 или mirror-php на :8091).
import { chromium } from '/Users/aleksandrnarodetskii/.npm/_npx/6f4879659183bc49/node_modules/playwright/index.mjs';
import path from 'path';
import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, 'captures');
const url = (process.argv[2] || 'http://localhost:8093') + '/for/oceanarium/_preview-page.html';
const b = await chromium.launch({ channel: 'chrome' });
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await p.goto(url, { waitUntil: 'networkidle' });
await p.evaluate(() => document.querySelectorAll('.rv').forEach(n => n.classList.add('in')));
const dive = await p.$('#dive'); await dive.scrollIntoViewIfNeeded(); await p.waitForTimeout(800);
const waits = [2500, 3500, 5000, 3000, 6000];
for (let i = 0; i < 5; i++) { await p.click(`#chap li[data-i="${i}"]`); await p.waitForTimeout(waits[i]); await dive.screenshot({ path: `${out}/dive-${i}.png` }); }
const floor = await p.$('#floor');
for (const m of ['plankton', 'school', 'rays', 'clean']) {
  await p.click(`#ftabs button[data-m="${m}"]`);
  const box = await floor.boundingBox();
  for (let i = 0; i < 90; i++) { await p.mouse.move(box.x + box.width * (.08 + .84 * i / 90), box.y + box.height * (.5 + .32 * Math.sin(i / 7))); await p.waitForTimeout(16); }
  await p.mouse.move(box.x + box.width * .93, box.y + box.height * .5);
  await floor.screenshot({ path: `${out}/floor-${m}.png` });
}
const led = await p.$('#led-svg'); await led.scrollIntoViewIfNeeded(); await p.waitForTimeout(3500);
await led.screenshot({ path: `${out}/led.png` });
await b.close();
console.log('ok');
