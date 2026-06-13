import Seo from '../components/Seo'
import { CtaSection } from '../components/PageBlocks'
import { CLIENT_LOGOS } from '../data/clients'
import { imgSrc } from '../lib/content'

export default function Clients() {
  return (
    <>
      <Seo title="Клиенты агентства Hand Marketing" description="С нами работают федеральные бренды и крупные компании России." />
      <section className="mx-auto max-w-7xl px-4 pb-16 pt-28 sm:px-6">
        <h1 className="font-display text-4xl font-extrabold sm:text-5xl">С нами работают</h1>
        <div className="mt-12 grid grid-cols-2 items-center gap-x-10 gap-y-12 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
          {CLIENT_LOGOS.map((l, i) => (
            <img key={i} src={imgSrc({ src: l.remote, local: l.local })} alt="" loading="lazy" className="mx-auto h-12 w-auto max-w-[150px] object-contain opacity-75 transition hover:opacity-100" />
          ))}
        </div>
      </section>
      <CtaSection />
    </>
  )
}
