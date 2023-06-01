import React from 'react'
import Image from 'next/image'
import styles from './loading.module.css'
import logo from '../../public/vast-loading.png'
import {motion} from 'framer-motion'


function Loading({isLoading}) {
  return (
    <motion.div transition={{ duration: 2 }} animate={{ opacity: 0 }} initial={{ opacity: 1 }}  className={styles.container}>
        <motion.div initial={{ scale: 0.5 }} animate={{ scale: 1 }} transition={{ duration: 1 }} >
        <Image src={logo} alt="vast logo" width={442} height={151} />
        </motion.div>        
    </motion.div>
  )
}

export default Loading