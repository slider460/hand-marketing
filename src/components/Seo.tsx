import { useEffect } from 'react'

export default function Seo({ title, description }: { title: string; description?: string }) {
  useEffect(() => {
    document.title = title
    let meta = document.querySelector('meta[name="description"]')
    if (!meta) {
      meta = document.createElement('meta')
      meta.setAttribute('name', 'description')
      document.head.appendChild(meta)
    }
    if (description) meta.setAttribute('content', description)
    window.scrollTo(0, 0)
  }, [title, description])
  return null
}
