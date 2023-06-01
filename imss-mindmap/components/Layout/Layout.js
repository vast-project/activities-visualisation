import React, { useEffect, useRef, useState } from 'react'

import styles from './layout.module.css'
import Image from 'next/image'
import logo from '../../public/logo.png'
import italy from '../../public/ita-flag.png'
import uk from '../../public/uk-flag.png'
import { createContext } from 'react'

export const LanguageContext = createContext();

const Layout = ({children}) => {
    const [isItalian, setIsItalian] = useState(true);

    const handleSetItalian = () => {
        setIsItalian(true);
      }
      const handleSetEnglish = () => {
        setIsItalian(false);
      }
  return (
    <LanguageContext.Provider value={isItalian}>
        <div className={styles.flagContainer}>
          <button className={styles.flagBtn} onClick={handleSetItalian}>
            <Image src={italy} alt="italian" width={37} height={31} />
          </button>
          <button className={styles.flagBtn} onClick={handleSetEnglish}>
            <Image src={uk} alt="English" width={37} height={31} />
          </button>
        </div>
        {children}
    </LanguageContext.Provider>
  )
}

export default Layout