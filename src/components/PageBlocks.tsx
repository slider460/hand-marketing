import { Block, imgSrc } from '../lib/content'
import VideoEmbed from './VideoEmbed'
import ContactForm from './ContactForm'

/** Рендерит блок, извлечённый с Tilda: тексты по ролям, галерея, видео.
 *  Это «честный» перенос контента; финальную типографику каждой страницы
 *  можно дорабатывать в Антигравити поверх этого рендера. */
export function BlockView({ block }: { block: Block }) {
  const photos = block.images.filter((i) => !i.src.endsWith('.svg'))
  return (
    <section className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
      <div className="space-y-4">
        {block.texts.map((t, i) => {
          if (t.role === 'title')
            return (
              <h2 key={i} className="font-display text-3xl font-bold leading-tight sm:text-4xl">
                {t.text}
              </h2>
            )
          if (t.role === 'subtitle')
            return (
              <h3 key={i} className="font-display text-xl font-semibold text-hm-graphite">
                {t.text}
              </h3>
            )
          if (t.role === 'button') return null
          return (
            <p key={i} className="max-w-3xl leading-relaxed text-hm-graphite">
              {t.text}
            </p>
          )
        })}
      </div>

      {block.videos.length > 0 && (
        <div className="mt-8 space-y-6">
          {block.videos.map((v, i) => (
            <VideoEmbed key={i} video={v} />
          ))}
        </div>
      )}

      {photos.length > 0 && (
        <div
          className={`mt-8 grid gap-4 ${
            photos.length === 1 ? '' : photos.length === 2 ? 'sm:grid-cols-2' : 'sm:grid-cols-2 lg:grid-cols-3'
          }`}
        >
          {photos.map((img, i) => (
            <img
              key={i}
              src={imgSrc(img)}
              alt={img.alt}
              loading="lazy"
              className="w-full rounded-2xl object-cover"
            />
          ))}
        </div>
      )}
    </section>
  )
}

export function CtaSection() {
  return (
    <section className="relative overflow-hidden bg-hm-ink py-20 text-white">
      <img
        src="/brand/pattern_about.svg"
        alt=""
        aria-hidden
        className="pointer-events-none absolute -right-20 -top-10 w-[520px] opacity-20"
      />
      <div className="relative mx-auto max-w-7xl px-4 text-center sm:px-6">
        <h2 className="font-display text-3xl font-bold sm:text-4xl">Давайте сделаем проект вместе?</h2>
        <p className="mt-3 text-white/60">Отправьте свои данные, и мы вам перезвоним</p>
        <div className="mt-8">
          <ContactForm dark />
        </div>
      </div>
    </section>
  )
}
