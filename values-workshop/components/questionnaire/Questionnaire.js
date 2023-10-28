import styles from './questionnaire.module.css'
import {BsArrowLeftCircleFill} from 'react-icons/bs'
import React, {useContext, useState} from 'react';
import Button from '@component/ui/button/Button';
import {LangContext} from "../layout/Layout";
import Instructions from "@component/components/instructions/Instructions";
import Welcome from "@component/components/welcome/Welcome";


function Questionnaire() {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const [next, setNext] = useState(false);
    const [previous, setPrevious] = useState(false);

    if (next) {
        return <Instructions/>
    }
    if (previous) {
        return <Welcome/>
    }

    return (
        <div className={styles.container}>
            <BsArrowLeftCircleFill onClick={() => setPrevious(true)} className={styles.leftArrow}/>
            <h1 className={styles.primaryHeadline}>{isEnglish ? 'Questionnaire' : 'Ερωτηματολόγιο'}</h1>
            <h3 className={styles.secondaryHeadline}>{isEnglish ? 'Please answer the following questions' : 'Παρακαλώ απαντήστε στις παρακάτω ερωτήσεις'}</h3>

            <Button onClick={() => setNext(!next)} color="#FFC857" title={isEnglish ? 'Next' : "Επομενο"}/>
        </div>
    )
}

export default Questionnaire