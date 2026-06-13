import Seo from '../components/Seo'
import { CtaSection } from '../components/PageBlocks'
import { ABOUT_TEXT, FACTS, TEAM } from '../data/site'
import { imgSrc } from '../lib/content'

export default function About() {
  return (
    <>
      <Seo title="Об агентстве Hand Marketing" description="Рекламное агентство полного цикла: более 10 лет, full service, офис в Москве, партнёрская сеть в 100+ городах России." />
      <section className="relative overflow-hidden pt-24">
        <img src="/brand/pattern_about.svg" alt="" aria-hidden className="pointer-events-none absolute -right-24 top-10 w-[460px] opacity-15" />
        <div className="relative mx-auto max-w-5xl px-4 py-12 sm:px-6">
          <h1 className="font-display text-4xl font-extrabold sm:text-5xl">О нас</h1>
          {ABOUT_TEXT.map((p, i) => (
            <p key={i} className="mt-6 max-w-3xl text-lg leading-relaxed text-hm-graphite">{p}</p>
          ))}
        </div>
      </section>
      <section className="mx-auto grid max-w-7xl gap-6 px-4 py-12 sm:grid-cols-2 sm:px-6 lg:grid-cols-4">
        {FACTS.map((f, i) => (
          <div key={i} className="rounded-2xl bg-white p-7">
            <p className="font-display text-2xl font-bold" style={{ color: ['#629535', '#cf6f19', '#673a7e', '#c12164'][i] }}>{f.title}</p>
            <p className="mt-3 text-sm leading-relaxed text-hm-graphite">{f.text}</p>
          </div>
        ))}
      </section>
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6">
        <h2 className="font-display text-3xl font-bold sm:text-4xl">Наша команда</h2>
        <div className="mt-10 grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-4">
          {TEAM.map((m) => (
            <figure key={m.name} className="text-center">
              <img src={imgSrc({ src: m.photoRemote, local: m.photo })} alt={m.name} loading="lazy" className="mx-auto aspect-square w-full max-w-[180px] rounded-full object-cover" />
              <figcaption className="mt-3">
                <p className="font-display font-bold leading-tight">{m.name}</p>
                <p className="mt-1 text-xs uppercase tracking-wide text-hm-stone">{m.role}</p>
              </figcaption>
            </figure>
          ))}
        </div>
      </section>
      <CtaSection />
    </>
  )
}
