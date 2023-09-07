import gr from './../../public/gr-flag.png'
import gb from './../../public/gb-flag.png'
import logo from './../../public/logo.png'

import styles from './layout.module.css'
import {useState, createContext} from 'react'

export const LangContext = createContext();

const Layout = ({children}) => {
    const [isEnglish, setIsEnglish] = useState(false)

    return (
        <section className={styles.layoutContainer}>
            <div className={styles.flagContainer}>
                <img onClick={() => setIsEnglish(false)} src={gr} alt="gr flag"/>
                <img onClick={() => setIsEnglish(true)} src={gb} alt="gb flag"/>
            </div>

            <LangContext.Provider value={{isEnglish, setIsEnglish}} className={styles.container}>
                {children}
            </LangContext.Provider>

            <div className={styles.logoContainer}>
                <img src={logo} alt="logo"/>
            </div>
        </section>
    )
}

export default Layout