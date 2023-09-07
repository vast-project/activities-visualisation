import {useContext, useState} from 'react'
import {LangContext} from '../../../layout/Layout.jsx'
import styles from './before.module.css'
import Title from "../../../ui/Title/Title.jsx"
import Button from '../../../ui/Button/Button.jsx'
import Activity1 from '../../activities/activity-1/Activity1.jsx';
import AnnotationActivity from "../../annotation-activity/AnnotationActivity.jsx";

const Before = () => {
    const {isEnglish} = useContext(LangContext)
    const [prev, setPrev] = useState(false)
    const [next, setNext] = useState(false)

    // Set the text for the component based on the language
    const englishTitle = "Values Questionnaire"
    const greekTitle = "Ερωτηματολόγιο Αξιών"

    const prevBtnText = {
        en: "PREVIOUS",
        gr: "ΠΙΣΩ"
    }
    const nextBtnText = {
        en: "NEXT",
        gr: "ΕΠΟΜΕΝΟ"
    }

    if (prev) {
        return <AnnotationActivity/>
    }
    if (next) {
        return <Activity1/>
    }

    return (
        <>
            <Title title={isEnglish ? englishTitle : greekTitle}/>
            <div className={styles.formContainer}>
                <iframe className={styles.questionnaireFrame} src="https://platform.vast-project.eu/ftm-pre-assessment/"
                        title="Pre-assessment questionnaire"></iframe>
            </div>

            <div className={styles.btnContainer}>
                <button className={styles.btnBack}
                        onClick={() => setPrev(true)}>{isEnglish ? prevBtnText.en : prevBtnText.gr}</button>
                <Button onClick={() => setNext(true)} text={isEnglish ? nextBtnText.en : nextBtnText.gr}
                        color="rgb(105, 160, 130)"/>
            </div>
        </>
    )
}

export default Before
