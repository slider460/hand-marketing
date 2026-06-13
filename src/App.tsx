import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import Home from './pages/Home'
import About from './pages/About'
import Services from './pages/Services'
import ServicePage from './pages/ServicePage'
import Projects from './pages/Projects'
import CasePage from './pages/CasePage'
import Clients from './pages/Clients'
import Contacts from './pages/Contacts'
import Privacy from './pages/Privacy'
import Thanks from './pages/Thanks'
import NotFound from './pages/NotFound'
import { SERVICES } from './data/site'

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/service" element={<Services />} />
          {SERVICES.map((s) => (
            <Route key={s.slug} path={`/${s.slug}`} element={<ServicePage />} />
          ))}
          <Route path="/project" element={<Projects />} />
          <Route path="/clients" element={<Clients />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/sk" element={<Thanks />} />
          {/* Кейсы: /event/:slug, /video/:slug, /creative/..., /digital/..., /3d/... и одиночные */}
          <Route path="*" element={<CasePage />} />
        </Routes>
      </main>
      <Footer />
    </BrowserRouter>
  )
}
