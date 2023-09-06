import {useContext, useState} from 'react'
import styles from './writingactivity.module.css'
import {LangContext} from '../../../layout/Layout'
import {CharactersContext} from './../activity-1/characters/Characters'
import Title from "../../../ui/Title/Title.jsx";
import Button from "../../../ui/Button/Button.jsx";
import Activity1 from "../activity-1/Activity1.jsx";
import Congratulations from "../../congratulations/Congratulations.jsx";

const WritingActivity = () => {
    const {isEnglish} = useContext(LangContext)
    const myCharacters = useContext(CharactersContext)
    const [next, setNext] = useState(false)
    const [prev, setPrev] = useState(false)
    console.log(myCharacters);


    const textareaPlaceholder = {
        en: "Write a story...",
        gr: "Γράψε μια ιστορία..."
    }

    if (prev) {
        return <Activity1/>
    }

    if (next) {
        // todo: Save the data to the database
        return <Congratulations/>
    }

    return (
        <div className={styles.storyContainer}>
            <Title title="Write a story"/>

            <textarea className={styles.storyInput}
                      placeholder={isEnglish ? textareaPlaceholder.en : textareaPlaceholder.el}></textarea>

            <div className={styles.btnContainer}>
                <button className={styles.btnBack} onClick={() => setPrev(true)}>ΠΙΣΩ</button>
                <Button onClick={() => setNext(true)} text="ΕΠΟΜΕΝΟ" color="rgb(105, 160, 130)"/>
            </div>
        </div>
    )
}

export default WritingActivity
