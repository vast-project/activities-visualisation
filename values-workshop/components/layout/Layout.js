import styles from './layout.module.css'
import Image from 'next/image'
import logo from '../../public/logo.png'
import greek from '../../public/gr-flag.png'
import english from '../../public/gb-flag.png'
import { useState,createContext } from 'react'

export const LangContext = createContext();

function Layout({children}) {
  const [isEnglish, setIsEnglish] = useState(false)

  return (
    <div className={styles.container}>
        <div className={styles.flagContainer}>
        <Image onClick={() => setIsEnglish(false)} src={greek} alt="Vast Logo" className={styles.flag} width={32} height={32} />
        <Image onClick={() => setIsEnglish(true)} src={english} alt="Vast Logo" className={styles.flag} width={32} height={32} />
        </div>

        <LangContext.Provider value={{isEnglish, setIsEnglish}}>
          {children}
        </LangContext.Provider>
        
        <Image src={logo} alt="Vast Logo" className={styles.biglogo} width={400} height={140} />
        <Image src={logo} alt="Vast Logo" className={styles.logo} width={200} height={70} />
    </div>
  )
}

export default Layout
