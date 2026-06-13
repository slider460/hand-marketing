/** Палитра Hand Marketing v2.2 — извлечена из векторного логотипа (куб) и фирменного паттерна */
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        hm: {
          // Green — primary (грани куба)
          'green-light': '#c7d306',
          green: '#96c223',
          'green-dark': '#629535',
          // Yellow (лента)
          'yellow-light': '#ffdf2e',
          yellow: '#e1b905',
          'yellow-dark': '#c2981a',
          // Orange
          'orange-light': '#f39306',
          orange: '#cf6f19',
          'orange-dark': '#a75c21',
          // Red / Carmine (буква M)
          'red-light': '#e8413b',
          red: '#bb3b42',
          'red-dark': '#9c2c40',
          // Purple (буква H)
          'purple-light': '#95388d',
          purple: '#673a7e',
          'purple-dark': '#4a2d6f',
          // Cyan / Teal (фигуры паттерна)
          'cyan-light': '#a2d3c3',
          cyan: '#5bbcb0',
          'cyan-dark': '#2e7d75',
          // Pink / Magenta (фигуры паттерна)
          'pink-light': '#ec609e',
          pink: '#e71a83',
          'pink-dark': '#c12164',
          // Нейтрали
          ink: '#1a1a1a',
          graphite: '#3d3d3d',
          stone: '#8a8a8a',
          mist: '#e9e9e4',
          paper: '#fafaf7',
        },
      },
      fontFamily: {
        display: ['Montserrat', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        brand: '0.18em',
      },
    },
  },
  plugins: [],
}
