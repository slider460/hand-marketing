import { Link } from 'react-router-dom'
import Seo from '../components/Seo'

export default function Thanks() {
  return (
    <>
      <Seo title="Спасибо! — Hand Marketing" />
      <section className="mx-auto flex min-h-[60vh] max-w-3xl flex-col items-center justify-center px-4 pt-16 text-center">
        <img src="/brand/logo_header.svg" alt="" className="h-16 w-16" />
        <h1 className="mt-6 font-display text-4xl font-extrabold">Спасибо!</h1>
        <p className="mt-3 text-lg text-hm-graphite">Мы получили вашу заявку и перезвоним в ближайшее время.</p>
        <Link to="/" className="mt-8 rounded-xl bg-hm-green px-7 py-3.5 font-display font-bold text-white transition hover:bg-hm-green-dark">На главную</Link>
      </section>
    </>
  )
}
