import '@/styles/globals.css'
import localFont from '@next/font/local'
const myFont = localFont({src: '../fonts/Curvy-Thins.ttf'})

export default function App({ Component, pageProps }) {
  return (
      <Component {...pageProps} />
  )
}
