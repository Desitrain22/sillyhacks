/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'purple': '#662D91',
        'pink': '#ED4B79',
        'magenta': '#FF00FF',
        'green': '#D9E021',
        'cyan': '#D3FFFF',
        'light-green': '#F0F3A6',
      },
      fontFamily: {
        stretch: ["Stretch Pro", "sans-serif"],
        comic: ["Comic Sans", "sans-serif"],
      },
    },
  },
  plugins: [],
}

