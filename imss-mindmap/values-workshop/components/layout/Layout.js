import styles from './layout.module.css'
import Image from 'next/image'
import logo from '../../public/logo.png'

function Layout({children}) {
  return (
    <div className={styles.container}>
        {children}
        <Image src={logo} alt="Vast Logo" className={styles.biglogo} width={400} height={140} />
        <Image src={logo} alt="Vast Logo" className={styles.logo} width={200} height={70} />
    </div>
  )
}

export default Layout
