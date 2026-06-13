// Типы данных, извлечённых с Tilda-версии сайта
export type TextRole = 'title' | 'subtitle' | 'text' | 'button'

export interface TextItem {
  role: TextRole
  text: string
  href?: string
}

export interface ImageItem {
  src: string // оригинальный URL на tildacdn (до запуска scripts/download-assets.mjs)
  local: string // локальный путь /assets/... (после скачивания)
  alt: string
}

export interface VideoItem {
  type: 'embed' | 'mp4'
  src: string
}

export interface Block {
  id: string
  type: string
  texts: TextItem[]
  images: ImageItem[]
  videos: VideoItem[]
  links: { href: string; text: string }[]
}

export interface PageData {
  title: string
  description: string
  og_image?: string
  og_local?: string
  blocks: Block[]
}

export interface CaseMeta {
  slug: string
  route: string
  category: 'event' | 'video' | 'creative' | 'digital' | '3dmapping'
  categoryLabel: string
  client: string
  title: string
  metaTitle: string
  cover: string
  coverRemote: string
}

/** До скачивания ассетов используем remote-URL, после — локальный путь.
 *  Переключатель: VITE_LOCAL_ASSETS=1 (выставляется автоматически скриптом download-assets). */
const useLocal = import.meta.env.VITE_LOCAL_ASSETS === '1'

export function imgSrc(img: { src: string; local?: string } | string): string {
  if (typeof img === 'string') return img
  return useLocal && img.local ? img.local : img.src
}

export function coverSrc(c: CaseMeta): string {
  return useLocal && c.cover ? c.cover : c.coverRemote || c.cover
}

export function youtubeEmbed(src: string): string | null {
  const m =
    src.match(/(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([\w-]{6,})/) ||
    src.match(/^([\w-]{11})$/)
  return m ? `https://www.youtube.com/embed/${m[1]}` : null
}

const modules = import.meta.glob('../data/pages/*.json', { eager: true }) as Record<
  string,
  { default: PageData }
>

export function getPage(slug: string): PageData | null {
  const key = `../data/pages/${slug}.json`
  return modules[key]?.default ?? null
}
