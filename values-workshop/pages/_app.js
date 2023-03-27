import '@component/styles/globals.css'
import Layout from '@component/components/layout/Layout'
import {DndProvider} from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'

export default function App({ Component, pageProps }) {
  return (
    <DndProvider backend={HTML5Backend}>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </DndProvider>
  )
}
