import {useContext, useState} from 'react'
import {LangContext} from '../../../layout/Layout.jsx'
import styles from './before.module.css'
import Title from "../../../ui/Title/Title.jsx"
import Button from '../../../ui/Button/Button.jsx'
import Activity1 from '../../activities/activity-1/Activity1.jsx';

const Before = () => {
    const {isEnglish} = useContext(LangContext)
    const [next, setNext] = useState(false)

    // Set the text for the component based on the language
    const englishTitle = "Values Questionnaire"
    const englishButton = "NEXT"
    const greekTitle = "Ερωτηματολόγιο Αξιών"
    const greekButton = "ΕΠΟΜΕΝΟ"

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

            <Button onClick={() => setNext(true)} text={isEnglish ? englishButton : greekButton}
                    color="rgb(105, 160, 130)"/>
        </>
    )
}

export default Before
