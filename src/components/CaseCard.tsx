import { Link } from 'react-router-dom'
import { CaseMeta, coverSrc } from '../lib/content'
import { CATEGORY_COLOR } from '../data/site'

/** Декоративные мини-фигуры v2.2, выступающие за границу круга.
 *  Позиции фиксированы, цвет варьируется по индексу карточки. */
const FIGS = [
  { cls: 'left-[6%] top-[2%] h-4 w-4 rotate-12', shape: 'rounded-sm' },
  { cls: 'right-[4%] top-[14%] h-5 w-5 -rotate-6', shape: 'rounded-full' },
  { cls: 'right-[10%] bottom-[6%] h-4 w-6 rotate-45', shape: 'rounded-sm' },
  { cls: 'left-[2%] bottom-[18%] h-6 w-3 -rotate-12', shape: 'rounded' },
  { cls: 'left-[40%] -top-[2%] h-3 w-3', shape: 'rounded-full' },
  { cls: 'right-[36%] -bottom-[1%] h-3 w-5 rotate-12', shape: 'rounded-sm' },
]
const FIG_COLORS = ['#ffdf2e', '#e71a83', '#5bbcb0', '#f39306', '#95388d', '#c7d306', '#e8413b']

export default function CaseCard({ c, index = 0 }: { c: CaseMeta; index?: number }) {
  const color = CATEGORY_COLOR[c.category] ?? '#96c223'
  const cover = coverSrc(c)
  return (
    <Link to={c.route} className="case-card group relative block aspect-square outline-none">
      {/* Декоративные фигуры — за пределами круга */}
      {FIGS.map((f, i) => (
        <span
          key={i}
          aria-hidden
          className={`absolute z-10 ${f.cls} ${f.shape} shadow-sm`}
          style={{ background: FIG_COLORS[(index + i) % FIG_COLORS.length] }}
        />
      ))}

      {/* Front: круг-постер (фото + тонировка фирменным цветом) */}
      <span className="face face-front absolute inset-2 overflow-hidden rounded-full">
        {cover ? (
          <img src={cover} alt={c.title} loading="lazy" className="h-full w-full object-cover" />
        ) : (
          <span className="block h-full w-full" style={{ background: color }} />
        )}
        <span className="absolute inset-0 mix-blend-multiply" style={{ background: color, opacity: 0.28 }} />
      </span>

      {/* Back: цветной квадрат с минимальным контентом */}
      <span
        className="face face-back absolute inset-2 flex flex-col rounded-3xl p-6 text-white"
        style={{ background: color }}
      >
        <span
          aria-hidden
          className="pointer-events-none absolute inset-0 flex items-center overflow-hidden rounded-3xl p-4 font-display text-5xl font-extrabold uppercase leading-none text-white/5"
        >
          {c.client}
        </span>
        <span className="relative w-fit rounded-full bg-hm-green-light px-3 py-1 font-display text-[11px] font-bold uppercase tracking-wider text-hm-ink">
          {c.categoryLabel}
        </span>
        <span className="relative mt-auto font-display text-lg font-bold leading-snug">
          {c.title}
        </span>
        <span className="relative mt-2 text-sm text-white/85">{c.client}</span>
      </span>
    </Link>
  )
}
