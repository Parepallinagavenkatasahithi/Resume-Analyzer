/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        charcoal: {
          800: '#2d3748',
          900: '#1a202c',
        }
      }
    },
  },
  plugins: [],
}
