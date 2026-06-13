import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { CONTACTS, NAV } from '../data/site'

export default function Header() {
  const [open, setOpen] = useState(false)
  return (
    <header className="fixed inset-x-0 top-0 z-50 bg-hm-paper/90 backdrop-blur border-b border-hm-mist">
      <div className="mx-auto flex h-16 max-w-7xl items-center gap-6 px-4 sm:px-6">
        <Link to="/" className="flex items-center gap-3 shrink-0" onClick={() => setOpen(false)}>
          <img src="/brand/logo_header.svg" alt="Hand Marketing" className="h-10 w-10" />
          <span className="hidden font-display text-xs font-bold tracking-brand sm:block">
            HAND&nbsp;MARKETING
          </span>
        </Link>

        <nav className="ml-auto hidden items-center gap-7 lg:flex">
          {NAV.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              className={({ isActive }) =>
                `text-sm font-medium transition-colors hover:text-hm-green-dark ${
                  isActive ? 'text-hm-green-dark' : 'text-hm-ink'
                }`
              }
            >
              {n.label}
            </NavLink>
          ))}
        </nav>

        <div className="ml-auto hidden flex-col items-end leading-tight lg:ml-8 lg:flex">
          <a href={CONTACTS.phoneHref} className="font-display text-sm font-bold hover:text-hm-green-dark">
            {CONTACTS.phone}
          </a>
          <a href={`mailto:${CONTACTS.email}`} className="text-xs text-hm-stone hover:text-hm-green-dark">
            {CONTACTS.email}
          </a>
        </div>

        <button
          aria-label="Меню"
          aria-expanded={open}
          onClick={() => setOpen(!open)}
          className="ml-auto flex h-10 w-10 flex-col items-center justify-center gap-1.5 lg:hidden"
        >
          <span className={`h-0.5 w-6 bg-hm-ink transition ${open ? 'translate-y-2 rotate-45' : ''}`} />
          <span className={`h-0.5 w-6 bg-hm-ink transition ${open ? 'opacity-0' : ''}`} />
          <span className={`h-0.5 w-6 bg-hm-ink transition ${open ? '-translate-y-2 -rotate-45' : ''}`} />
        </button>
      </div>

      {open && (
        <nav className="border-t border-hm-mist bg-hm-paper px-6 py-4 lg:hidden">
          {NAV.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              onClick={() => setOpen(false)}
              className="block py-3 font-display text-lg font-semibold"
            >
              {n.label}
            </NavLink>
          ))}
          <a href={CONTACTS.phoneHref} className="mt-2 block py-2 font-display font-bold">
            {CONTACTS.phone}
          </a>
        </nav>
      )}
    </header>
  )
}
