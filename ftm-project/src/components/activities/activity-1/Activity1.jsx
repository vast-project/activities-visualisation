import {useContext, useState} from 'react'
import styles from './activity1.module.css'
import Form from '../../questionnere/before/Form/Form'
import Button from './../../../ui/Button/Button'
import {LangContext} from '../../../layout/Layout'
import Title from '../../../ui/Title/Title'
import Paragraph from '../../../ui/Paragraph/Paragraph'
import Characters, {CharactersContext} from './characters/Characters'
import Functions from './functions/Functions'
import WritingActivity from '../activity-2/WritingActivity.jsx'

const text = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis ab sit repudiandae! Facilis libero molestias sint quaerat, vitae amet soluta, accusantium nostrum, placeat ullam eius."

const Activity1 = () => {
    const {isEnglish} = useContext(LangContext)
    const myCharacters = useContext(CharactersContext)
    const [next, setNext] = useState(false)
    const [prev, setPrev] = useState(false)

    if(prev){
        return <Form />
    }
    if(next){
        return <WritingActivity />
    }

  return (
    <div>
        <Title title="Morphology of Fairy Tale" />
        <h5 className={styles.miniTitle}>(inspired by Vladimir Propp)</h5>

        <Paragraph text={text} />

        <Characters />
        <Functions />

        <div className={styles.btnContainer}>
            <button className={styles.btnBack} onClick={() => setPrev(true)}>ΠΙΣΩ</button>
            <Button onClick={() => setNext(true)} text="ΕΠΟΜΕΝΟ" color="rgb(105, 160, 130)" />
        </div>
    </div>
  )
}

export default Activity1