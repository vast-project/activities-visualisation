import React, { useEffect, useRef, useState } from 'react'
import styles from './congratulations.module.css'
import Image from 'next/image'
import logo from '../../public/logo.png'
import eu from '../../public/eu_flag.svg'
import {motion} from 'framer-motion'
import mindmap from '../../public/congratulations-mindmap.svg'


function Congratulations({isItalian}) {
  return (
    <motion.div className={styles.container} transition={{ duration: 1 }} initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }}>
        <h1 className={styles.primaryHeadline}>{isItalian ? 'Congratulazioni' : 'Congratulations'}</h1>
        <h3 className={styles.secondaryHeadline}>{isItalian ? 'Grazie per aver completato la mappa mentale' : 'Thank you for completing the mindmap'}</h3>

        <Image alt="Mindmap"  src={mindmap} width={364} height={247}></Image>
        <Image alt="Logo Vast" className={styles.logo} src={logo} width={125} height={42}></Image>
        <div className={styles.euContainer}>
          <Image alt="Logo EU" className={styles.logo} src={eu} width={80} height={50}></Image>
          <p>{isItalian ? "Questo progetto è stato finanziato dal programma di ricerca e innovazione Horizon 2020 dell'Unione Europea con l'accordo di sovvenzione n. 101004949. Questo sito web riflette solo il punto di vista degli autori e la Commissione europea non è responsabile dell'uso che può essere fatto delle informazioni in esso contenute." : "This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 101004949. This website reflects only the view of the authors and the European Commission is not responsible for any use that may be made of the information it contains."}</p>
        </div>

    </motion.div>
  )
}

export default Congratulations