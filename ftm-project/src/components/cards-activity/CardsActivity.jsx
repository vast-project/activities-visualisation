import {createContext, useContext, useState} from 'react'
import styles from './cardsactivity.module.css'
import Before from '../questionnaire/before/Before.jsx'
import Button from '../../ui/Button/Button.jsx'
import {LangContext} from '../../layout/Layout.jsx'
import Title from '../../ui/Title/Title.jsx'
import Paragraph from '../../ui/Paragraph/Paragraph.jsx'
import Characters from './characters/Characters.jsx'
import Functions from './functions/Functions.jsx'
import WritingActivity from '../writing-activity/WritingActivity.jsx'

const text = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis ab sit repudiandae! Facilis libero molestias sint quaerat, vitae amet soluta, accusantium nostrum, placeat ullam eius."

export const CharactersContext = createContext([])
export const FunctionsContext = createContext([])

const CardsActivity = () => {
    const {isEnglish} = useContext(LangContext)
    const [next, setNext] = useState(false)
    const [prev, setPrev] = useState(false)

    const [selectedCharacters, setSelectedCharacters] = useState([])
    const [selectedFunctions, setSelectedFunctions] = useState([])

    let handleCharacters = (characters) => {
        setSelectedCharacters(characters)
    }
    let handleFunctions = (functions) => {
        setSelectedFunctions(functions)
    }

    const prevBtnText = {
        en: "PREVIOUS",
        gr: "ΠΙΣΩ"
    }
    const nextBtnText = {
        en: "NEXT",
        gr: "ΕΠΟΜΕΝΟ"
    }

    if (prev) {
        return <Before/>
    }
    if (next) {
        return (
            <CharactersContext.Provider value={selectedCharacters}>
                <FunctionsContext.Provider value={selectedFunctions}>
                    <WritingActivity/>
                </FunctionsContext.Provider>
            </CharactersContext.Provider>
        )
    }

    return (
        <div>
            <Title title="Morphology of Fairy Tale"/>
            <h5 className={styles.miniTitle}>(inspired by Vladimir Propp)</h5>

            <Paragraph text={text}/>

            <Characters onChange={handleCharacters}/>
            <Functions onChange={handleFunctions}/>

            <div className={styles.btnContainer}>
                <button className={styles.btnBack}
                        onClick={() => setPrev(true)}>{isEnglish ? prevBtnText.en : prevBtnText.gr}</button>
                <Button onClick={() => setNext(true)} text={isEnglish ? nextBtnText.en : nextBtnText.gr}
                        color="rgb(105, 160, 130)"/>
            </div>
        </div>
    )
}

export default CardsActivity