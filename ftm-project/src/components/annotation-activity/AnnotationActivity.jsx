import {useContext, useState} from 'react'
import Button from '../../ui/Button/Button.jsx'
import {LangContext} from '../../layout/Layout.jsx'
import Title from '../../ui/Title/Title.jsx'
import Paragraph from '../../ui/Paragraph/Paragraph.jsx'
import styles from './annotationactivity.module.css'
import Welcome from "../welcome/Welcome.jsx";
import Before from "../questionnaire/before/Before.jsx";


const AnnotationActivity = () => {
    const {isEnglish} = useContext(LangContext)
    const [next, setNext] = useState(false)
    const [prev, setPrev] = useState(false)

    const titleText = {
        en: "Recognition of Values",
        gr: "Αναγνώριση Αξιών"
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
        return <Welcome/>
    }
    if (next) {
        return <Before/>
    }

    return (
        <div>
            <Title title={isEnglish ? titleText.en : titleText.gr}/>

            <Paragraph text="text to annotate goes here"/>

            <div className={styles.btnContainer}>
                <button className={styles.btnBack}
                        onClick={() => setPrev(true)}>{isEnglish ? prevBtnText.en : prevBtnText.gr}</button>
                <Button onClick={() => setNext(true)} text={isEnglish ? nextBtnText.en : nextBtnText.gr}
                        color="rgb(105, 160, 130)"/>
            </div>
        </div>
    )
}

export default AnnotationActivity