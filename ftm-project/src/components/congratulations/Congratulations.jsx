import styles from './congratulations.module.css'
import {useContext} from "react";
import {LangContext} from "../../layout/Layout.jsx";

const Congratulations = () => {
    const {isEnglish} = useContext(LangContext)

    const headline = {
        en: "Congratulations",
        gr: "Συγχαρητήρια"
    }

    const secondaryHeadline = {
        en: "Thank you for completing the activity “Values in Fairy Tales”.",
        gr: "Ευχαριστούμε που ολοκληρώσατε την δραστηριότητα «Οι Αξίες στα Παραμύθια»."
    }

    return (
        <section>
            <h1 className={styles.primaryHeadline}>{isEnglish ? headline.en : headline.gr}</h1>
            <h3 className={styles.secondaryHeadline}>{isEnglish ? secondaryHeadline.en : secondaryHeadline.gr}</h3>
        </section>
    )
}

export default Congratulations