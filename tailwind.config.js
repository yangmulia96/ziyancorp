/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Google Sans Text', 'Google Sans', 'system-ui', 'sans-serif'],
        display: ['Google Sans Display', 'Google Sans', 'system-ui', 'sans-serif'],
      },
      colors: {
        surface: {
          dark: '#131314',
          'dark-card': '#1E1F20',
          'dark-elevated': '#28292A',
          light: '#F0F4F9',
          'light-card': '#FFFFFF',
          'light-elevated': '#E8ECF1',
        },
        crimson: {
          50: '#FEF2F2',
          100: '#FEE2E2',
          200: '#FECACA',
          300: '#FCA5A5',
          400: '#F87171',
          500: '#EF4444',
          600: '#DC2626',
          700: '#B91C1C',
          800: '#991B1B',
          900: '#7F1D1D',
        },
        ink: {
          primary: '#1F1F1F',
          secondary: '#444746',
          tertiary: '#747775',
          light: '#F8F9FA',
          'light-secondary': '#C4C7C5',
        },
      },
      borderRadius: {
        'pill': '9999px',
        '2xl': '1rem',
        '3xl': '1.5rem',
        '4xl': '1.75rem',
      },
      keyframes: {
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'glow-pulse': {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '0.8' },
        },
        blob: { '0%': { transform: 'translate(0px, 0px) scale(1)' }, '33%': { transform: 'translate(30px, -50px) scale(1.1)' }, '66%': { transform: 'translate(-20px, 20px) scale(0.9)' }, '100%': { transform: 'translate(0px, 0px) scale(1)' } }, 'badge-pulse': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        },
      },
      animation: {
        'fade-in-up': 'fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'fade-in-up-delay-1': 'fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.1s forwards',
        'fade-in-up-delay-2': 'fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards',
        'fade-in-up-delay-3': 'fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.3s forwards',
        'glow-pulse': 'glow-pulse 4s ease-in-out infinite',
        'blob': 'blob 7s infinite', 'badge-pulse': 'badge-pulse 2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};

