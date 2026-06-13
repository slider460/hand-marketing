import { useState } from 'react'
import { Link } from 'react-router-dom'
import Seo from '../components/Seo'
import CaseCard from '../components/CaseCard'
import { CtaSection } from '../components/PageBlocks'
import { SERVICES, FACTS, ABOUT_TEXT, TEAM, CONTACTS } from '../data/site'
import { CLIENT_LOGOS } from '../data/clients'
import casesData from '../data/cases.json'
import { CaseMeta, imgSrc } from '../lib/content'

const cases = casesData as CaseMeta[]
// Флагманские кейсы на главной — Самара ВДНХ первым
const FEATURED = ['samara_vdnh', 'event__samsung', 'video__patriot', '3d__stavropol', 'event__marieclaire', 'creative__skolkovo']
const featured = FEATURED.map((s) => cases.find((c) => c.slug === s)!).filter(Boolean)

export default function Home() {
  const [showreel, setShowreel] = useState(false)
  return (
    <>
      <Seo
        title="Hand Marketing — рекламное агентство полного цикла"
        description="Event, Creative & Design, Video Production, Print, Digital, 3D Mapping, BTL. Более 10 лет эффективных маркетинговых коммуникаций."
      />

      {/* HERO */}
      <section className="relative overflow-hidden pt-16">
        <img
          src="/brand/pattern_hero.svg"
          alt=""
          aria-hidden
          className="pointer-events-none absolute inset-x-0 top-10 mx-auto w-full max-w-6xl opacity-[0.10]"
        />
        <div className="relative mx-auto grid max-w-7xl gap-12 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:py-24">
          <div>
            <p className="font-display text-sm font-bold uppercase tracking-brand text-hm-green-dark">
              Hand Marketing
            </p>
            <h1 className="mt-3 font-display text-4xl font-extrabold leading-tight sm:text-5xl">
              Рекламное агентство полного цикла
            </h1>
            <ul className="mt-8 space-y-1">
              {SERVICES.map((s) => (
                <li key={s.slug}>
                  <Link
                    to={`/${s.slug}`}
                    className="group flex items-baseline gap-3 py-1.5 font-display text-2xl font-bold text-hm-graphite transition-colors hover:text-hm-ink sm:text-3xl"
                  >
                    <span
                      className="h-3 w-3 shrink-0 rounded-sm transition-transform group-hover:scale-125"
                      style={{ background: s.color }}
                    />
                    {s.label}
                  </Link>
                </li>
              ))}
            </ul>
            <button
              onClick={() => setShowreel(true)}
              className="mt-10 rounded-xl bg-hm-ink px-7 py-3.5 font-display font-bold text-white transition hover:bg-hm-graphite"
            >
              Смотреть showreel
            </button>
          </div>
          <div className="hidden items-center justify-center lg:flex">
            <img src="/brand/logo_hero.svg" alt="Hand Marketing — фирменный куб" className="w-full max-w-md" />
          </div>
        </div>
      </section>

      {/* КЕЙСЫ */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6">
        <div className="flex items-end justify-between">
          <h2 className="font-display text-3xl font-bold sm:text-4xl">Кейсы</h2>
          <Link to="/project" className="font-display text-sm font-bold text-hm-green-dark hover:underline">
            Все проекты →
          </Link>
        </div>
        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {featured.map((c, i) => (
            <CaseCard key={c.slug} c={c} index={i} />
          ))}
        </div>
      </section>

      {/* О НАС */}
      <section className="bg-white py-16">
        <div className="mx-auto grid max-w-7xl gap-12 px-4 sm:px-6 lg:grid-cols-2">
          <div>
            <h2 className="font-display text-3xl font-bold sm:text-4xl">О нас</h2>
            {ABOUT_TEXT.map((p, i) => (
              <p key={i} className="mt-5 leading-relaxed text-hm-graphite">
                {p}
              </p>
            ))}
            <Link
              to="/about"
              className="mt-8 inline-block rounded-xl border-2 border-hm-ink px-6 py-3 font-display font-bold transition hover:bg-hm-ink hover:text-white"
            >
              Подробнее
            </Link>
          </div>
          <div className="grid content-start gap-6 sm:grid-cols-2">
            {FACTS.map((f, i) => (
              <div key={i} className="rounded-2xl bg-hm-paper p-6">
                <p className="font-display text-xl font-bold" style={{ color: ['#629535', '#cf6f19', '#673a7e', '#c12164'][i] }}>
                  {f.title}
                </p>
                <p className="mt-2 text-sm leading-relaxed text-hm-graphite">{f.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* КОМАНДА */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6">
        <h2 className="font-display text-3xl font-bold sm:text-4xl">Наша команда</h2>
        <div className="mt-10 grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-4">
          {TEAM.map((m) => (
            <figure key={m.name} className="text-center">
              <img
                src={imgSrc({ src: m.photoRemote, local: m.photo })}
                alt={m.name}
                loading="lazy"
                className="mx-auto aspect-square w-full max-w-[180px] rounded-full object-cover"
              />
              <figcaption className="mt-3">
                <p className="font-display font-bold leading-tight">{m.name}</p>
                <p className="mt-1 text-xs uppercase tracking-wide text-hm-stone">{m.role}</p>
              </figcaption>
            </figure>
          ))}
        </div>
      </section>

      {/* КЛИЕНТЫ — бегущая строка */}
      <section className="overflow-hidden bg-white py-14">
        <h2 className="mx-auto max-w-7xl px-4 font-display text-3xl font-bold sm:px-6 sm:text-4xl">
          С нами работают
        </h2>
        <div className="marquee mt-10">
          <div className="marquee-track flex w-max items-center gap-14 px-4">
            {[...CLIENT_LOGOS, ...CLIENT_LOGOS].map((l, i) => (
              <img
                key={i}
                src={imgSrc({ src: l.remote, local: l.local })}
                alt=""
                loading="lazy"
                className="h-10 w-auto max-w-[140px] object-contain opacity-70 grayscale transition hover:opacity-100 hover:grayscale-0"
              />
            ))}
          </div>
        </div>
      </section>

      <CtaSection />

      {/* SHOWREEL POPUP */}
      {showreel && (
        <div
          className="fixed inset-0 z-[60] flex items-center justify-center bg-black/85 p-4"
          onClick={() => setShowreel(false)}
          role="dialog"
          aria-label="Showreel"
        >
          <button
            className="absolute right-5 top-4 font-display text-3xl text-white"
            aria-label="Закрыть"
            onClick={() => setShowreel(false)}
          >
            ×
          </button>
          <video
            controls
            autoPlay
            className="max-h-[80vh] w-full max-w-4xl rounded-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <source src={CONTACTS.showreel} type="video/mp4" />
          </video>
        </div>
      )}
    </>
  )
}
