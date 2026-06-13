export const CONTACTS = {
  phone: '+7 495 580 75 37',
  phoneHref: 'tel:+74955807537',
  email: 'info@hand-marketing.ru',
  address: '123022, Москва, Рочдельская, 14А',
  metro: 'м. Краснопресненская / м. Баррикадная',
  whatsapp:
    'https://wa.me/+79859998783?text=Здравствуйте.%20Меня%20интересуют%20ваши%20услуги',
  telegram: 'https://t.me/narodetskii',
  youtube: 'https://youtube.com/channel/UCKBNvpFhrJXQjzZdTnIFYxw',
  requisites: 'ООО «Хэнд-маркетинг» · ИНН 7709931482 · КПП 770901001 · ОГРН 1137746525608',
  showreel: 'https://dl.dropboxusercontent.com/s/9cqeabb1b6pla6k/HM_Showreel.mp4?dl=0',
}

export const NAV = [
  { to: '/service', label: 'Услуги' },
  { to: '/about', label: 'О нас' },
  { to: '/project', label: 'Проекты' },
  { to: '/clients', label: 'Клиенты' },
  { to: '/contacts', label: 'Контакты' },
]

export interface ServiceDef {
  slug: string
  label: string
  category: string // категория кейсов
  color: string // цветовая семья v2.2
  blurb: string
}

export const SERVICES: ServiceDef[] = [
  { slug: 'event', label: 'Event', category: 'event', color: '#96c223', blurb: 'Организация мероприятий, wow show, road show, MICE' },
  { slug: 'creativedesign', label: 'Creative & Design', category: 'creative', color: '#e71a83', blurb: 'Креативные концепции, айдентика, брендбук, POS-материалы' },
  { slug: 'videoproduction', label: 'Video Production', category: 'video', color: '#e8413b', blurb: 'Рекламные, вирусные, имиджевые и обучающие ролики' },
  { slug: 'printandproduction', label: 'Print & Production', category: 'creative', color: '#f39306', blurb: 'Рекламные конструкции, POSm, печатная продукция' },
  { slug: 'btl', label: 'BTL', category: 'event', color: '#5bbcb0', blurb: 'Дегустации, семплинг, промо, Mystery Shopper, HoReCa' },
  { slug: 'digital', label: 'Digital', category: 'digital', color: '#673a7e', blurb: 'Сайты, контекст, SEO, таргет, сквозная аналитика' },
  { slug: '3dmapping', label: '3D Mapping', category: '3dmapping', color: '#ffdf2e', blurb: '3D Mapping show под ключ: контент, оборудование, реализация' },
]

/** Цвет квадрата кейс-карточки по категории (v2.2) */
export const CATEGORY_COLOR: Record<string, string> = {
  event: '#96c223',
  video: '#e8413b',
  creative: '#e71a83',
  digital: '#673a7e',
  '3dmapping': '#f39306',
}

export const FACTS = [
  { title: 'Более 10 лет', text: 'Мы делаем эффективные маркетинговые коммуникации' },
  { title: 'Full service', text: 'Любые услуги в области маркетинговых коммуникаций' },
  { title: 'Сотрудничество', text: 'Целеустремлённость и внимание к партнёрам — долгосрочное партнёрство' },
  { title: 'Локация', text: 'Офис в центре Москвы, региональная партнёрская сеть с охватом более 100 городов России' },
]

export const ABOUT_TEXT = [
  'Основную бизнес-философию агентства можно охарактеризовать словом «прозрачность»: клиент имеет возможность наблюдать за исполнением заказа на каждом этапе проекта с экспертной оценкой исполняемых процедур. Главной движущей силой нашей компании являются её сотрудники. На сегодняшний день в агентстве работают специалисты, имеющие богатый опыт работы в рекламном бизнесе.',
  'Основной принцип нашей работы — комплексное обеспечение клиентского сервиса на основе ситуационного анализа его потребностей, с последующей выработкой наиболее оптимальных методик и инструментов продвижения продуктов и услуг. Головной офис находится в Москве, партнёрская сеть охватывает все крупные города России.',
]

export interface TeamMember {
  name: string
  role: string
  photo: string // ВНИМАНИЕ: сверить соответствие фото и имён визуально (см. ANTIGRAVITY.md)
  photoRemote: string
}

const tild = (p: string) => `https://static.tildacdn.com/${p}`

export const TEAM: TeamMember[] = [
  { name: 'Народецкий Александр', role: 'Client Service Director / CEO', photo: '/assets/beff2559_mriyaresort_-01-01.png', photoRemote: tild('tild3735-6531-4234-b830-363630623332/mriyaresort_-01-01.png') },
  { name: 'Семенов Эдвард', role: 'Commercial Director', photo: '/assets/926f2b86_mriyaresort_-01-02.png', photoRemote: tild('tild6238-6262-4661-a665-306166343031/mriyaresort_-01-02.png') },
  { name: 'Дементьев Святослав', role: 'Chief Creative Officer', photo: '/assets/832093b2_mriyaresort_-01-03.png', photoRemote: tild('tild3636-6463-4437-b436-383331356332/mriyaresort_-01-03.png') },
  { name: 'Кличановский Сергей', role: 'Business Development Director', photo: '/assets/daf7e1c6_mriyaresort_-01-04.png', photoRemote: tild('tild3731-3535-4665-a633-663639313564/mriyaresort_-01-04.png') },
  { name: 'Осотов Алексей', role: 'Chief Information Officer', photo: '/assets/7eed117e_mriyaresort_-01-05.png', photoRemote: tild('tild6133-3736-4165-a366-353530633430/mriyaresort_-01-05.png') },
  { name: 'Муратов Денис', role: 'Technical Director', photo: '/assets/1a4c5098_mriyaresort_-01-06.png', photoRemote: tild('tild3366-6336-4430-b166-646662633061/mriyaresort_-01-06.png') },
  { name: 'Агафонова Илона', role: 'Senior Account Manager', photo: '/assets/c1b18cc9_mriyaresort_-01-07.png', photoRemote: tild('tild6463-3334-4266-b835-313433396166/mriyaresort_-01-07.png') },
]
