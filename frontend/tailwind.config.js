/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      colors: {
        primary: {
          DEFAULT: '#0070F3',
          dark: '#0060D9',
          light: '#00C2FF',
        },
        dark: {
          DEFAULT: '#0A0A0B',
          card: '#1A1A1B',
        },
      },
      boxShadow: {
        'glow-blue': '0 0 20px rgba(0, 112, 243, 0.2)',
        'glow-blue-lg': '0 0 30px rgba(0, 112, 243, 0.3)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
};
