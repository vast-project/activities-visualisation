import {useContext, useState} from 'react'
import styles from './writingactivity.module.css'
import {LangContext} from '../../layout/Layout.jsx'
import Title from "../../ui/Title/Title.jsx";
import Button from "../../ui/Button/Button.jsx";
import CardsActivity, {CharactersContext, FunctionsContext} from "../cards-activity/CardsActivity.jsx";
import Congratulations from "../congratulations/Congratulations.jsx";

const WritingActivity = () => {
    const {isEnglish} = useContext(LangContext)
    const selectedCharacters = useContext(CharactersContext)
    const selectedFunctions = useContext(FunctionsContext)
    const [next, setNext] = useState(false)
    const [prev, setPrev] = useState(false)

    const title = {
        en: "Write a story",
        gr: "Γράψε μια ιστορία"
    }

    const textareaPlaceholder = {
        en: "Write a story...",
        gr: "Γράψε μια ιστορία..."
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
        return <CardsActivity/>
    }

    if (next) {
        // todo: Save the data to the database
        return <Congratulations/>
    }

    return (
        <div className={styles.storyContainer}>
            <Title title={isEnglish ? title.en : title.gr}/>

            <div className={styles.cardsRow}>
                <div className={styles.storyCards}>
                    <span className={styles.cardsTitle}>{isEnglish ? "Characters" : "Χαρακτήρες"}</span>
                    <div className={styles.cardsContainer}>
                        {
                            selectedCharacters.map((character) => {
                                return (
                                    <div className={styles.imageContainer}>
                                        <img src={character.src} alt="A character" width={50}/>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
                <div className={styles.storyCards}>
                    <span className={styles.cardsTitle}>{isEnglish ? "Functions" : "Συναρτήσεις"}</span>
                    <div className={styles.cardsContainer}>
                        {
                            selectedFunctions.map((func) => {
                                return (
                                    <div className={styles.imageContainer}>
                                        <img src={func.src} alt="A character"/>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            </div>

            <textarea className={styles.storyInput}
                      placeholder={isEnglish ? textareaPlaceholder.en : textareaPlaceholder.gr}></textarea>

            <div className={styles.btnContainer}>
                <button className={styles.btnBack}
                        onClick={() => setPrev(true)}>{isEnglish ? prevBtnText.en : prevBtnText.gr}</button>
                <Button onClick={() => setNext(true)} text={isEnglish ? nextBtnText.en : nextBtnText.gr}
                        color="rgb(105, 160, 130)"/>
            </div>
        </div>
    )
}

export default WritingActivity
