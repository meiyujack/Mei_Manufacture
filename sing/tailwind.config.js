/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["sing/templates/*.html","sing/forms.py","sing/static/base.css"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

