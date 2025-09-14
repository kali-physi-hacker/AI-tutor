/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      borderRadius: { xl: '1rem', '2xl': '1.25rem' },
      boxShadow: {
        card: '0 8px 30px rgba(0,0,0,0.06)',
        lift: '0 12px 40px rgba(0,0,0,0.10)'
      },
      colors: {
        ink: { DEFAULT: '#12131A', soft: '#2A2C36', inverted: '#E8EAF2' },
        paper: { DEFAULT: '#FAFAFC', raised: '#FFFFFF', sunken: '#F3F5F9' },
        primary: { DEFAULT: '#3A5BF5', soft: '#6C89FF' },
        accent: { DEFAULT: '#16A394', soft: '#4CCFBF' }
      }
    }
  },
  plugins: []
}

