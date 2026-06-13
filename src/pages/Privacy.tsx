import Seo from '../components/Seo'
import { BlockView } from '../components/PageBlocks'
import { getPage } from '../lib/content'

export default function Privacy() {
  const page = getPage('privacy')
  return (
    <>
      <Seo title="Политика конфиденциальности — Hand Marketing" />
      <section className="mx-auto max-w-4xl px-4 pb-16 pt-28 sm:px-6">
        <h1 className="font-display text-3xl font-extrabold sm:text-4xl">Политика конфиденциальности</h1>
      </section>
      {page?.blocks.map((b) => <BlockView key={b.id} block={b} />)}
    </>
  )
}
