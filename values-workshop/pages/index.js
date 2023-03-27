import Head from 'next/head'
import styles from '@component/styles/Home.module.css'
import Welcome from '@component/components/welcome/Welcome'


export default function Home() {

  return (
    <>
      <Head>
        <title>Annotation Project</title>
        <meta name="description" content="Annotation Project" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <main className={styles.main}>
        <Welcome />
      </main>
    </>
  )
}
