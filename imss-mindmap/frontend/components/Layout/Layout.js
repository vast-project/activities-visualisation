import React, { useEffect, useRef, useState } from 'react'
import styles from './layout.module.css'
import italy from '../../public/italy-flag.png'
import uk from '../../public/eng-flag.png'
import Image from 'next/image'

function Layout({children}) {
  const [isItalian, setIsItalian] = useState(true);

  const handleSetItalian = () => {
    setIsItalian(true);
  }
  const handleSetEnglish = () => {
    setIsItalian(false);
  }
  return (
    <section className={styles.layoutContainer} >
      
      <div className={styles.flagContainer}>
          <button className={styles.flagBtn} onClick={handleSetItalian}>
            <Image src={italy} alt="italian" width={50} height={45} />
          </button>
          <button className={styles.flagBtn} onClick={handleSetEnglish}>
            <Image src={uk} alt="English" width={50} height={45} />
          </button>
        </div>

        {children}
    </section>
  )
}

export default Layout