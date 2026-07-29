/** Единый источник правды о сайте (DRY). Сменить бренд — одна константа. */
export interface NavItem { label: string; href: string }
export interface SiteConfig {
  brand: string;
  legalName: string;
  domain: string;        // без слэша в конце
  tagline: string;
  description: string;
  founded: string;
  email: string;
  phone: string;         //人-читаемый
  phoneHref: string;     // tel:
  address: { country: string; locality: string; postalCode: string; street: string };
  social: string[];
  nav: NavItem[];
  metrikaId?: number;    // Яндекс.Метрика
}

export const site: SiteConfig = {
  brand: 'Hand Marketing',
  legalName: 'ООО «Хэнд-маркетинг»',
  domain: 'https://hand-marketing.ru',
  tagline: 'Рекламное агентство полного цикла',
  description:
    'Event, Creative & Design, Video Production, Print, Digital, 3D Mapping, BTL. Более 10 лет эффективных маркетинговых коммуникаций.',
  founded: '2012',
  email: 'info@hand-marketing.ru',
  phone: '+7 495 580 75 37',
  phoneHref: 'tel:+74955807537',
  address: { country: 'RU', locality: 'Москва', postalCode: '123022', street: 'Рочдельская, 14А' },
  social: [],
  nav: [
    { label: 'Проекты', href: '/project' },
    { label: 'Услуги', href: '/service' },
    { label: 'О нас', href: '/about' },
    { label: 'Клиенты', href: '/clients' },
    { label: 'Контакты', href: '/contacts' },
  ],
  metrikaId: 71125393,
};

export const services = [
  { slug: 'event', title: 'Event', color: '#673A7E' },
  { slug: 'creativedesign', title: 'Creative & Design', color: '#C12164' },
  { slug: 'videoproduction', title: 'Video Production', color: '#CF6F19' },
  { slug: 'digital', title: 'Digital', color: '#5E9A2E' },
  { slug: '3dmapping', title: '3D Mapping', color: '#7E3FA0' },
  { slug: 'printandproduction', title: 'Print & Production', color: '#E08A2B' },
  { slug: 'btl', title: 'BTL', color: '#D6357E' },
] as const;
