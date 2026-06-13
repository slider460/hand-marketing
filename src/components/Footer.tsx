import { Link } from 'react-router-dom'
import { CONTACTS, NAV } from '../data/site'

export default function Footer() {
  return (
    <footer className="bg-hm-ink text-white">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-14 sm:px-6 md:grid-cols-3">
        <div>
          <div className="flex items-center gap-3">
            <img src="/brand/logo_header.svg" alt="" className="h-10 w-10" />
            <span className="font-display text-xs font-bold tracking-brand">HAND MARKETING</span>
          </div>
          <p className="mt-4 text-sm text-white/60">
            {CONTACTS.metro}
            <br />
            {CONTACTS.address}
          </p>
          <a href={CONTACTS.phoneHref} className="mt-4 block font-display font-bold hover:text-hm-green-light">
            {CONTACTS.phone}
          </a>
          <a href={`mailto:${CONTACTS.email}`} className="text-sm text-white/60 hover:text-hm-green-light">
            {CONTACTS.email}
          </a>
        </div>

        <nav className="grid grid-cols-2 content-start gap-x-6 gap-y-3">
          {NAV.map((n) => (
            <Link key={n.to} to={n.to} className="text-sm text-white/80 hover:text-hm-green-light">
              {n.label}
            </Link>
          ))}
          <Link to="/privacy" className="text-sm text-white/80 hover:text-hm-green-light">
            Политика конфиденциальности
          </Link>
        </nav>

        <div className="content-start">
          <div className="flex gap-4">
            <a href={CONTACTS.telegram} aria-label="Telegram" className="text-sm font-semibold text-white/80 hover:text-hm-green-light">Telegram</a>
            <a href={CONTACTS.whatsapp} aria-label="WhatsApp" className="text-sm font-semibold text-white/80 hover:text-hm-green-light">WhatsApp</a>
            <a href={CONTACTS.youtube} aria-label="YouTube" className="text-sm font-semibold text-white/80 hover:text-hm-green-light">YouTube</a>
          </div>
          <p className="mt-6 text-xs leading-relaxed text-white/40">
            {CONTACTS.requisites}
            <br />
            Использование материалов Hand Marketing разрешено только с согласия правообладателя.
            <br />© 2012–{new Date().getFullYear()} Hand Marketing
          </p>
        </div>
      </div>
    </footer>
  )
}
