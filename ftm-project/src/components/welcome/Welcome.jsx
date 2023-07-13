import Title from './../../ui/Title/Title'
import SubTitle from './../../ui/SubTitle/SubTitle'
import Paragraph from './../../ui/Paragraph/Paragraph'
import Button from './../../ui/Button/Button'
import Before from './../questionnere/before/Before'

import { useState, useContext } from 'react'
import { LangContext } from '../../layout/Layout'

const text = "Η δραστηριότητα «Οι Αξίες στα Παραμύθια» μέσα από ένα ταξίδι στον μαγικό κόσμο των παραμυθιών και στο πως αυτά δημιουργούνται αλλά και μέσα από την ανασκαφή των αξιών που απορρέουν από αυτά παρασύρει τους εφήβους σε μια ενδοσκόπηση για το πως οι αξίες αυτές διέπουν την καθημερινότητα τους αλλά και την κοινωνία στην οποία ζούν."

const Welcome = () => {
  const {isEnglish} = useContext(LangContext)
  const [next,setNext] = useState(false)

  if(next) {
    return (
      <>
      <Before />
      </>
    )
  }

  return (
    <>
      <Title title="Οι Αξιες στα Παραμύθια" />
      <SubTitle title="Καλώς ήλθατε" />
      <Paragraph text={text} />
      <Button onClick={() => setNext(true)} text="ΕΠΟΜΕΝΟ" color="rgb(105, 160, 130)" />
    </>
  )
}

export default Welcome