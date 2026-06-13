import { Link } from 'react-router-dom'
import Seo from '../components/Seo'
import { CtaSection } from '../components/PageBlocks'
import { SERVICES } from '../data/site'
import casesData from '../data/cases.json'
import { CaseMeta } from '../lib/content'

const cases = casesData as CaseMeta[]

export default function Services() {
  return (
    <>
      <Seo title="Услуги агентства Hand Marketing" description="Основные услуги агентства: Event, Creative & Design, Video Production, Print, Digital, 3D Mapping, BTL" />
      <section className="mx-auto max-w-7xl px-4 pb-16 pt-28 sm:px-6">
        <h1 className="font-display text-4xl font-extrabold sm:text-5xl">Услуги</h1>
        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {SERVICES.map((s) => {
            const n = cases.filter((c) => c.category === s.category).length
            return (
              <Link
                key={s.slug}
                to={`/${s.slug}`}
                className="group relative overflow-hidden rounded-3xl bg-white p-7 transition-shadow hover:shadow-xl"
              >
                <span aria-hidden className="absolute -right-6 -top-6 h-24 w-24 rounded-full opacity-15 transition-transform group-hover:scale-150" style={{ background: s.color }} />
                <span className="block h-3 w-10 rounded-sm" style={{ background: s.color }} />
                <h2 className="mt-5 font-display text-2xl font-bold">{s.label}</h2>
                <p className="mt-2 text-sm leading-relaxed text-hm-graphite">{s.blurb}</p>
                <p className="mt-5 font-display text-xs font-bold uppercase tracking-wider text-hm-stone">
                  {n > 0 ? `${n} проектов` : 'Под ключ'}
                </p>
              </Link>
            )
          })}
        </div>
      </section>
      <CtaSection />
    </>
  )
}
