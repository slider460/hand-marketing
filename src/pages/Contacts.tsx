import Seo from '../components/Seo'
import ContactForm from '../components/ContactForm'
import { CONTACTS } from '../data/site'

export default function Contacts() {
  return (
    <>
      <Seo title="Контакты агентства Hand Marketing" description="Москва, Рочдельская 14А. +7 495 580 75 37, info@hand-marketing.ru" />
      <section className="mx-auto max-w-7xl px-4 pb-20 pt-28 sm:px-6">
        <h1 className="font-display text-4xl font-extrabold sm:text-5xl">Контакты</h1>
        <div className="mt-12 grid gap-12 lg:grid-cols-2">
          <div className="space-y-7">
            <div>
              <p className="font-display text-xs font-bold uppercase tracking-wider text-hm-stone">Адрес</p>
              <p className="mt-1 text-lg">{CONTACTS.metro}<br />{CONTACTS.address}</p>
            </div>
            <div>
              <p className="font-display text-xs font-bold uppercase tracking-wider text-hm-stone">Телефон</p>
              <a href={CONTACTS.phoneHref} className="mt-1 block font-display text-2xl font-bold hover:text-hm-green-dark">{CONTACTS.phone}</a>
            </div>
            <div>
              <p className="font-display text-xs font-bold uppercase tracking-wider text-hm-stone">Email</p>
              <a href={`mailto:${CONTACTS.email}`} className="mt-1 block text-lg hover:text-hm-green-dark">{CONTACTS.email}</a>
            </div>
            <div className="flex gap-5 pt-2">
              <a href={CONTACTS.telegram} className="font-display font-bold text-hm-green-dark hover:underline">Telegram</a>
              <a href={CONTACTS.whatsapp} className="font-display font-bold text-hm-green-dark hover:underline">WhatsApp</a>
              <a href={CONTACTS.youtube} className="font-display font-bold text-hm-green-dark hover:underline">YouTube</a>
            </div>
          </div>
          <div className="rounded-3xl bg-white p-8">
            <h2 className="font-display text-2xl font-bold">Давайте сделаем проект вместе?</h2>
            <p className="mt-2 text-sm text-hm-stone">Отправьте свои данные, и мы вам перезвоним</p>
            <div className="mt-6"><ContactForm /></div>
          </div>
        </div>
      </section>
    </>
  )
}
