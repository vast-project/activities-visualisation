import { useState, useContext } from 'react'
import styles from './activity2.module.css'
// import Form from '../../questionnere/before/Form/Form'
// import Button from './../../../ui/Button/Button'
import { LangContext } from '../../../layout/Layout'
// import Title from '../../../ui/Title/Title'
// import Paragraph from '../../../ui/Paragraph/Paragraph'
import { CharactersContext } from './../activity-1/characters/Characters'
// import Functions from './functions/Functions'

const Activity2 = () => {
    const {isEnglish} = useContext(LangContext)
    const myCharacters = useContext(CharactersContext)
    const [next, setNext] = useState(false)
    const [prev, setPrev] = useState(false)
    console.log(myCharacters);

  return (
    <div>
        Activity
    </div>
  )
}

export default Activity2