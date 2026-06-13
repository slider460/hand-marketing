import { Link } from 'react-router-dom'
import Seo from '../components/Seo'

export default function NotFound() {
  return (
    <>
      <Seo title="Страница не найдена — Hand Marketing" />
      <section className="mx-auto flex min-h-[60vh] max-w-3xl flex-col items-center justify-center px-4 pt-16 text-center">
        <p className="font-display text-7xl font-extrabold text-hm-green">404</p>
        <h1 className="mt-4 font-display text-2xl font-bold">Такой страницы нет</h1>
        <Link to="/" className="mt-8 rounded-xl border-2 border-hm-ink px-6 py-3 font-display font-bold transition hover:bg-hm-ink hover:text-white">На главную</Link>
      </section>
    </>
  )
}
