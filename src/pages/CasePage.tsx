import { Link, useLocation } from 'react-router-dom'
import Seo from '../components/Seo'
import CaseCard from '../components/CaseCard'
import { BlockView, CtaSection } from '../components/PageBlocks'
import casesData from '../data/cases.json'
import { CaseMeta, getPage } from '../lib/content'
import NotFound from './NotFound'

const cases = casesData as CaseMeta[]

export default function CasePage() {
  const { pathname } = useLocation()
  const route = pathname.replace(/\/$/, '') || '/'
  const meta = cases.find((c) => c.route === route)
  const slug = meta?.slug ?? route.slice(1).replace(/\//g, '__')
  const page = getPage(slug)
  if (!page || !meta) return <NotFound />

  const related = cases.filter((c) => c.category === meta.category && c.slug !== meta.slug).slice(0, 3)

  return (
    <>
      <Seo title={`${meta.title} — кейс Hand Marketing`} description={page.description || meta.metaTitle} />
      <article className="pt-24">
        <header className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
          <p className="font-display text-sm font-bold uppercase tracking-brand text-hm-green-dark">
            {meta.categoryLabel} · {meta.client}
          </p>
          <h1 className="mt-3 font-display text-3xl font-extrabold leading-tight sm:text-5xl">{meta.title}</h1>
        </header>
        {page.blocks.map((b) => (
          <BlockView key={b.id} block={b} />
        ))}
      </article>

      {related.length > 0 && (
        <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6">
          <div className="flex items-end justify-between">
            <h2 className="font-display text-2xl font-bold sm:text-3xl">Ещё проекты</h2>
            <Link to="/project" className="font-display text-sm font-bold text-hm-green-dark hover:underline">
              Все проекты →
            </Link>
          </div>
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
