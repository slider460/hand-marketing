import { useLocation } from 'react-router-dom'
import Seo from '../components/Seo'
import CaseCard from '../components/CaseCard'
import { BlockView, CtaSection } from '../components/PageBlocks'
import { SERVICES } from '../data/site'
import casesData from '../data/cases.json'
import { CaseMeta, getPage } from '../lib/content'
import NotFound from './NotFound'

const cases = casesData as CaseMeta[]

export default function ServicePage() {
  const slug = useLocation().pathname.replace(/\//g, '')
  const svc = SERVICES.find((s) => s.slug === slug)
  const page = getPage(slug)
  if (!svc || !page) return <NotFound />

  const related = cases.filter((c) => c.category === svc.category).slice(0, 6)

  return (
    <>
      <Seo title={page.title} description={page.description} />
      <section className="relative overflow-hidden pt-24">
        <div aria-hidden className="absolute inset-x-0 top-0 h-72" style={{ background: `linear-gradient(180deg, ${svc.color}22, transparent)` }} />
        <header className="relative mx-auto max-w-5xl px-4 py-12 sm:px-6">
          <p className="font-display text-sm font-bold uppercase tracking-brand" style={{ color: svc.color }}>
            Услуга
          </p>
          <h1 className="mt-3 font-display text-4xl font-extrabold sm:text-5xl">{svc.label}</h1>
          <p className="mt-4 max-w-2xl text-lg text-hm-graphite">{svc.blurb}</p>
        </header>
      </section>
      {page.blocks.map((b) => (
        <BlockView key={b.id} block={b} />
      ))}
      {related.length > 0 && (
        <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6">
          <h2 className="font-display text-2xl font-bold sm:text-3xl">Проекты по направлению</h2>
          <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {related.map((c, i) => (
              <CaseCard key={c.slug} c={c} index={i} />
            ))}
          </div>
        </section>
      )}
      <CtaSection />
    </>
  )
}
