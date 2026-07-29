// Миграция кейсов Tilda-экспорта → Astro Content Collection.
// Источник: src/data/cases.json + src/data/pages/<slug>.json, картинки из public/assets.
// Назначение: site/src/content/projects/<slug>.md + site/src/assets/projects/<slug>/*.
// Идемпотентно: уже существующие .md (4 ручных) не трогаем. Запуск: node scripts/migrate-cases.mjs [--dry]
import { readFileSync, existsSync, mkdirSync, copyFileSync, writeFileSync, readdirSync } from 'node:fs';
import { basename, extname, join } from 'node:path';

const ROOT = process.cwd();
const DRY = process.argv.includes('--dry');
const ONLY = process.argv.find((a) => a.startsWith('--only='))?.split('=')[1];

const SRC_ASSETS = join(ROOT, 'public/assets');
const PAGES_DIR = join(ROOT, 'src/data/pages');
const OUT_CONTENT = join(ROOT, 'site/src/content/projects');
const OUT_ASSETS = join(ROOT, 'site/src/assets/projects');

const CAT = {
  event:     { label: 'Event',             accent: '#673A7E' },
  creative:  { label: 'Creative & Design', accent: '#C12164' },
  video:     { label: 'Video Production',  accent: '#CF6F19' },
  digital:   { label: 'Digital',           accent: '#5E9A2E' },
  '3dmapping': { label: '3D Mapping',       accent: '#7E3FA0' },
};

const cases = JSON.parse(readFileSync(join(ROOT, 'src/data/cases.json'), 'utf8'));
const existing = new Set(
  existsSync(OUT_CONTENT) ? readdirSync(OUT_CONTENT).filter((f) => f.endsWith('.md')).map((f) => f.replace(/\.md$/, '')) : [],
);

/** /assets/xxx.ext -> абсолютный путь к локальному файлу в public/assets, либо null */
const localPath = (p) => {
  if (!p) return null;
  const f = join(SRC_ASSETS, basename(p));
  return existsSync(f) ? f : null;
};
const yamlStr = (s) => `'${String(s).replace(/'/g, "''").replace(/\s+/g, ' ').trim()}'`;

let created = 0, skipped = 0, missingCover = 0;
const report = [];

for (const c of cases) {
  if (ONLY && c.slug !== ONLY) continue;
  if (existing.has(c.slug)) { skipped++; continue; }

  const meta = CAT[c.category] || { label: c.categoryLabel || 'Проект', accent: '#673A7E' };
  const coverSrc = localPath(c.cover);
  if (!coverSrc) { missingCover++; report.push(`нет обложки: ${c.slug} (${c.cover})`); continue; }

  // Детальная страница
  const pageFile = join(PAGES_DIR, `${c.slug}.json`);
  const page = existsSync(pageFile) ? JSON.parse(readFileSync(pageFile, 'utf8')) : {};
  const texts = (page.blocks || []).flatMap((b) => (b.texts || []).map((t) => (t.text || '').trim())).filter(Boolean);
  const images = (page.blocks || []).flatMap((b) => b.images || []);
  // Видео берём только если это уже локальный /media/<имя> (ушли от Dropbox/weshow).
  const rawVideo = (page.blocks || []).flatMap((b) => b.videos || []).find((v) => v?.src)?.src || '';
  const video = rawVideo.startsWith('/media/') ? rawVideo : '';

  const summary = (page.description || c.title || '').replace(/\s+/g, ' ').trim().slice(0, 315);
  // Тело: длинные содержательные абзацы (отсекаем заголовки/метки)
  const body = texts.filter((t) => t.length > 120 && t !== summary);

  // Папка ассетов кейса
  const dir = join(OUT_ASSETS, c.slug);
  const coverExt = extname(coverSrc) || '.jpg';
  const coverOut = join(dir, `cover${coverExt}`);

  // Галерея: локальные картинки кроме самой обложки
  const seen = new Set([basename(coverSrc)]);
  const gallery = [];
  for (const img of images) {
    const lp = localPath(img.local || img.src);
    if (!lp || seen.has(basename(lp))) continue;
    seen.add(basename(lp));
    const name = `g${gallery.length + 1}${extname(lp) || '.jpg'}`;
    gallery.push({ src: lp, name, alt: (img.alt || c.title).replace(/\s+/g, ' ').trim() });
  }

  const fm = [
    '---',
    `title: ${yamlStr(c.title)}`,
    `client: ${yamlStr(c.client || c.title)}`,
    `services: ['${meta.label}']`,
    `summary: ${yamlStr(summary)}`,
    `cover: '../../assets/projects/${c.slug}/cover${coverExt}'`,
    `coverAlt: ${yamlStr(c.title)}`,
    `accent: '${meta.accent}'`,
    `category: ${yamlStr(c.category)}`,
    'featured: false',
    'order: 100',
    ...(video ? [`video: ${yamlStr(video)}`] : []),
    ...(gallery.length
      ? ['gallery:', ...gallery.map((g) => `  - { src: '../../assets/projects/${c.slug}/${g.name}', alt: ${yamlStr(g.alt)} }`)]
      : []),
    ...(c.metaTitle ? ['seo:', `  description: ${yamlStr(c.metaTitle)}`] : []),
    '---',
    '',
    ...(body.length ? body.map((p) => p + '\n') : [summary + '\n']),
  ].join('\n');

  report.push(`✓ ${c.slug}  (галерея: ${gallery.length}, видео: ${video ? 'да' : '—'}, абзацев: ${body.length})`);
  created++;
  if (DRY) continue;

  mkdirSync(dir, { recursive: true });
  copyFileSync(coverSrc, coverOut);
  for (const g of gallery) copyFileSync(g.src, join(dir, g.name));
  writeFileSync(join(OUT_CONTENT, `${c.slug}.md`), fm, 'utf8');
}

console.log(report.join('\n'));
console.log(`\nИтого: создано ${created}, пропущено (уже есть) ${skipped}, без обложки ${missingCover}${DRY ? '  [DRY-RUN]' : ''}`);
