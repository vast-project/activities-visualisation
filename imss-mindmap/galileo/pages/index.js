import Head from 'next/head'
import Image from 'next/image'
import styles from '@/styles/Home.module.css'
import Form from '@/components/Form/Form'


export default function Home() {
  return (
    <>
      <Head>
        <title>Mindmap - Vast</title>
        <meta name="description" content="Vast Project" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/vast-logo.png" />
      </Head>
      <main className={styles.main}>
        <Form></Form>
      </main>
    </>
  )
}
