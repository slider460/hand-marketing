import { FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

type Status = 'idle' | 'sending' | 'error'

export default function ContactForm({ dark = false }: { dark?: boolean }) {
  const [status, setStatus] = useState<Status>('idle')
  const navigate = useNavigate()

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const form = e.currentTarget
    const data = Object.fromEntries(new FormData(form).entries())
    setStatus('sending')
    try {
      const res = await fetch('/api/lead.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...data, page: window.location.pathname }),
      })
      if (!res.ok) throw new Error(String(res.status))
      navigate('/sk')
    } catch {
      setStatus('error')
    }
  }

  const inputCls = `w-full rounded-xl border px-4 py-3 text-base outline-none transition focus:border-hm-green ${
    dark
      ? 'border-white/20 bg-white/10 text-white placeholder:text-white/40'
      : 'border-hm-mist bg-white text-hm-ink placeholder:text-hm-stone'
  }`

  return (
    <form onSubmit={onSubmit} className="mx-auto w-full max-w-xl">
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="sr-only">Ваше имя</span>
          <input name="name" required placeholder="Александр" autoComplete="name" className={inputCls} />
        </label>
        <label className="block">
          <span className="sr-only">Телефон</span>
          <input
            name="phone"
            required
            type="tel"
            inputMode="tel"
            placeholder="+7 ___ ___ __ __"
            autoComplete="tel"
            className={inputCls}
          />
        </label>
      </div>

      <button
        type="submit"
        disabled={status === 'sending'}
        className="mt-4 w-full rounded-xl bg-hm-green px-6 py-3.5 font-display font-bold text-white transition hover:bg-hm-green-dark disabled:opacity-60"
      >
        {status === 'sending' ? 'Отправляем…' : 'Перезвоните мне'}
      </button>

      {status === 'error' && (
        <p className={`mt-3 text-sm ${dark ? 'text-hm-yellow-light' : 'text-hm-red-light'}`}>
          Не получилось отправить. Позвоните нам: +7 495 580 75 37 — или попробуйте ещё раз.
        </p>
      )}

      <p className={`mt-3 text-xs ${dark ? 'text-white/50' : 'text-hm-stone'}`}>
        Нажимая на кнопку, вы даёте{' '}
        <Link to="/privacy" className="underline hover:text-hm-green">
          согласие на обработку персональных данных
        </Link>
      </p>
    </form>
  )
}
