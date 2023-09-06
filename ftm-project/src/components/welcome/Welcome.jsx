import Title from './../../ui/Title/Title'
import SubTitle from './../../ui/SubTitle/SubTitle'
import Paragraph from './../../ui/Paragraph/Paragraph'
import Button from './../../ui/Button/Button'
import Before from './../questionnere/before/Before'

import {useContext, useState} from 'react'
import {LangContext} from '../../layout/Layout'

const Welcome = () => {
    const {isEnglish} = useContext(LangContext);
    const [next, setNext] = useState(false);

    const titleText = {
        en: "Values in Fairy Tales",
        gr: "Οι Αξιες στα Παραμύθια"
    }

    const welcomeText = {
        en: "Welcome",
        gr: "Καλώς ήλθατε"
    }

    const nextBtnText = {
        en: "NEXT",
        gr: "ΕΠΟΜΕΝΟ"
    }

    const text = {
        en: "The activity “Values in Fairy Tales” through a journey to the magical world of fairy tales and how they are created but also through the excavation of the values that derive from them, it leads teenagers to an introspection of how these values govern their daily lives and the society in which they live.",
        gr: "Η δραστηριότητα «Οι Αξίες στα Παραμύθια» μέσα από ένα ταξίδι στον μαγικό κόσμο των παραμυθιών και στο πως αυτά δημιουργούνται αλλά και μέσα από την ανασκαφή των αξιών που απορρέουν από αυτά παρασύρει τους εφήβους σε μια ενδοσκόπηση για το πως οι αξίες αυτές διέπουν την καθημερινότητα τους αλλά και την κοινωνία στην οποία ζούν."
    }

    if (next) {
        return (
            <>
                <Before/>
            </>
        )
    }

    return (
        <>
            <Title title={isEnglish ? titleText.en : titleText.gr}/>
            <SubTitle title={isEnglish ? welcomeText.en : welcomeText.gr}/>
            <Paragraph text={isEnglish ? text.en : text.gr}/>
            <Button onClick={() => setNext(true)} text={isEnglish ? nextBtnText.en : nextBtnText.gr}
                    color="rgb(105, 160, 130)"/>
        </>
    )
}

export default Welcome