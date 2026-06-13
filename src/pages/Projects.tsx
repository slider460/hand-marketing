import { useState } from 'react'
import Seo from '../components/Seo'
import CaseCard from '../components/CaseCard'
import { CtaSection } from '../components/PageBlocks'
import casesData from '../data/cases.json'
import { CaseMeta } from '../lib/content'

const cases = casesData as CaseMeta[]
const FILTERS = [
  { key: 'all', label: 'Все' },
  { key: 'event', label: 'Event' },
  { key: 'video', label: 'Video Production' },
  { key: 'creative', label: 'Creative & Design' },
  { key: 'digital', label: 'Digital' },
  { key: '3dmapping', label: '3D Mapping' },
]

export default function Projects() {
  const [filter, setFilter] = useState('all')
  const shown = filter === 'all' ? cases : cases.filter((c) => c.category === filter)
  return (
    <>
      <Seo title="Проекты агентства Hand Marketing" description="Проекты агентства по ключевым услугам: Event, Video, Creative, Digital, 3D Mapping." />
      <section className="mx-auto max-w-7xl px-4 pb-16 pt-28 sm:px-6">
        <h1 className="font-display text-4xl font-extrabold sm:text-5xl">Проекты</h1>
        <div className="mt-8 flex flex-wrap gap-2">
          {FILTERS.map((f) => (
            <button
              key={f.key}
              onClick={() => setFilter(f.key)}
              className={`rounded-full px-4 py-2 font-display text-sm font-bold transition ${
                filter === f.key ? 'bg-hm-ink text-white' : 'bg-white text-hm-graphite hover:bg-hm-mist'
              }`}
            >
              {f.label}
              <span className="ml-2 text-xs opacity-60">
                {f.key === 'all' ? cases.length : cases.filter((c) => c.category === f.key).length}
              </span>
            </button>
          ))}
        </div>
        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {shown.map((c, i) => (
            <CaseCard key={c.slug} c={c} index={i} />
          ))}
        </div>
      </section>
      <CtaSection />
    </>
  )
}
