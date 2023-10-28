import styles from './questionnaire.module.css'
import {BsArrowLeftCircleFill} from 'react-icons/bs'
import React, {useContext, useState} from 'react';
import Button from '@component/ui/button/Button';
import {LangContext} from "../layout/Layout";
import Instructions from "@component/components/instructions/Instructions";
import Welcome, {IdContext} from "@component/components/welcome/Welcome";


function Questionnaire() {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const [next, setNext] = useState(false);
    const [previous, setPrevious] = useState(false);

    const questionnaireBaseUrl = 'https://platform.vast-project.eu/portrait-values-questionnaire-mscds/?participant_id='

    if (next) {
        return <Instructions/>
    }
    if (previous) {
        return <Welcome/>
    }

    // Get user id and use it to create the questionnaire URL
    const userId = useContext(IdContext);
    const questionnaireUrl = questionnaireBaseUrl + encodeURIComponent(userId);

    return (
        <div className={styles.container}>
            <BsArrowLeftCircleFill onClick={() => setPrevious(true)} className={styles.leftArrow}/>
            <h1 className={styles.primaryHeadline}>{isEnglish ? 'Questionnaire' : 'Ερωτηματολόγιο'}</h1>
            <h3 className={styles.secondaryHeadline}>{isEnglish ? 'Please answer the following questions' : 'Παρακαλώ απαντήστε στις παρακάτω ερωτήσεις'}</h3>

            <iframe className={styles.iframe} src={questionnaireUrl} title="Questionnaire"></iframe>

            <Button onClick={() => setNext(!next)} color="#FFC857" title={isEnglish ? 'Next' : "Επομενο"}/>
        </div>
    )
}

export default Questionnaire