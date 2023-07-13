import './App.css'
import Layout from './layout/Layout'

import Welcome from './components/welcome/Welcome'



function App() {

  return (
    <>
      <Layout>
        {/* <Title title="Welcome to the Activity" />
        <SubTitle title="Secondary Title" />
        <Paragraph text={text} />
        <Button text="Next" color="#b4c5a5" /> */}
        <Welcome />

      </Layout>
    </>
  )
}

export default App
