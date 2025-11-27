/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "../app.py",
    "./**/*.js",
  ],
  // safelist: [{ pattern: /.*/ }], //убрать строку перед отправкой в прод и перебилдить стили для tailwind 
  theme: {
    extend: {
      fontFamily: {
        sans: ["Manrope", "ui-sans-serif", "system-ui"],
      },
      colors: {
        sun1: "#FFD271", // primary
        sun2: "#BFA66F",
        sun3: "#A67D25",
        sun4: "#FFDD95",
        sun5: "#FFE6B1",
      },
    },
  },
  plugins: [],
};
