import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://hand-marketing.ru',
  integrations: [sitemap()],
  build: { inlineStylesheets: 'auto' },
  prefetch: { prefetchAll: true },
});
