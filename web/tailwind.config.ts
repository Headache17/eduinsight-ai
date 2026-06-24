import type { Config } from 'tailwindcss'
const config: Config = {
  content: ['./pages/**/*.{js,ts,jsx,tsx}','./components/**/*.{js,ts,jsx,tsx}','./app/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: { colors: { brand: { 50: '#EEEDFE',600:'#534AB7', 800:'#3C3489' } } } },
  plugins: []
}
export default config
