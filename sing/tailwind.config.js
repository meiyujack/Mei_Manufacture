/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["sing/templates/*.html","sing/forms.py"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

