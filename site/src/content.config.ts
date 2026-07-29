import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/** Кейсы/проекты — строго типизированы (Zod). Картинка проходит через astro:assets. */
const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      client: z.string(),
      year: z.coerce.number().int().min(2010).max(2030).optional(),
      services: z.array(z.string()).min(1),
      summary: z.string().max(320),
      cover: image(),
      coverAlt: z.string(),
      accent: z.string().regex(/^#([0-9a-f]{6})$/i),
      category: z.enum(['event', 'creative', 'video', 'digital', '3dmapping']).optional(),
      featured: z.boolean().default(false),
      order: z.number().default(100),
      video: z.string().optional(),       // /media/<имя>.mp4
      videoPoster: z.string().optional(),
      gallery: z.array(z.object({ src: image(), alt: z.string() })).default([]),
      seo: z.object({ title: z.string().optional(), description: z.string().optional() }).default({}),
    }),
});

export const collections = { projects };
