/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./**/*.{html,js}"],
    darkMode: 'class', // Enable dark mode via class
    theme: {
      extend: {
        colors: {
          // Your custom color palette
          primary: {
            50: '#e6f1fe',
            100: '#cce3fd',
            200: '#99c8fb',
            300: '#66acf9',
            400: '#3391f7',
            500: '#0066f5',
            600: '#0052c4',
            700: '#003d93',
            800: '#002962',
            900: '#001431',
          },
          dark: {
            100: '#333342',
            200: '#2c2c3b',
            300: '#252534',
            400: '#1e1e2d',
            500: '#181826',
            600: '#12121c',
            700: '#0c0c13',
            800: '#060609',
            900: '#000000',
          },
        },
        fontFamily: {
          sans: ['Inter', 'sans-serif'],
          mono: ['Fira Code', 'monospace'],
        },
        animation: {
          'fade-in': 'fadeIn 0.5s ease-in-out',
          'slide-in': 'slideIn 0.5s ease-in-out',
        },
        keyframes: {
          fadeIn: {
            '0%': { opacity: '0' },
            '100%': { opacity: '1' },
          },
          slideIn: {
            '0%': { transform: 'translateY(10px)', opacity: '0' },
            '100%': { transform: 'translateY(0)', opacity: '1' },
          },
        },
        boxShadow: {
          'message': '0 1px 2px rgba(0, 0, 0, 0.1)',
          'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        },
      },
    },
    plugins: [],
  }