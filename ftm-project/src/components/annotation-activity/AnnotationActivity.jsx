import {createContext, useContext, useState} from 'react'
import Button from '../../ui/Button/Button.jsx'
import {LangContext} from '../../layout/Layout.jsx'
import Title from '../../ui/Title/Title.jsx'
import Paragraph from '../../ui/Paragraph/Paragraph.jsx'
import styles from './annotationactivity.module.css'
import Welcome from "../welcome/Welcome.jsx";
import Before from "../questionnaire/before/Before.jsx";
import {TextAnnotator} from "react-text-annotate";
import {CirclePicker} from "react-color";

export const AnnotationsContext = createContext([])

const AnnotationActivity = () => {
    const {isEnglish} = useContext(LangContext)
    const [next, setNext] = useState(false)
    const [prev, setPrev] = useState(false)
    const [annotations, setAnnotations] = useState([])
    const [annotationColor, setAnnotationColor] = useState("#cddc39")
    const [annotationTag, setAnnotationTag] = useState("")

    const titleText = {
        en: "Recognition of Values",
        gr: "Αναγνώριση Αξιών"
    }

    const explanationText = {
        en: "Read the following passage and try to write down in the blank boxes that follow the values contained in it, marking the sentence or sentences in which each value appears in the corresponding colour.",
        gr: "Διαβάστε το ακόλουθο απόσπασμα και προσπαθήστε να καταγράψετε στα κενά που ακολουθούν αξίες που περιλαμβάνονται σε αυτό επισημειώνοντας με το αντίστοιχο χρώμα την πρόταση ή τις προτάσεις στις οποίες παρουσιάζεται η κάθε αξία."
    }

    const annotationText = {
        en: "Near the king's palace there was a large forest where there was a well. Whenever it was very hot, the little princess used to sit by the well to cool off. She used to play with a golden ball which she would throw in the air and catch. Out of all her toys, she loved this ball the most. One day her ball left her hands and after bouncing on the ground fell into the well. The princess saw the ball falling into the water, but the well was so deep that its bottom could not be seen. Then the girl began to cry inconsolably, and as time passed, she cried louder and louder. As she was crying, someone called out to her: \"What's the matter, princess, you're crying so much that even a stone would feel sorry for you!\" The princess looked around to see who spoke. Then she saw a frog that had stuck its slimy head out of the water.\n" +
            "\n\"Ah, it’s you, frog?\" the princess tells him \"I cry for my golden ball that fell into the well.\"\n" +
            "\n\"Calm down and don't cry and I can find the solution for you\" replied the frog \"but tell me what will you give me if I bring you your toy?\"\n" +
            "\n\"Whatever you like and love, my frog,\" replied the girl, \"my clothes, my jewellery and diamonds, even the golden crown that I wear.\"\n" +
            "\n\"I don't care about your clothes, your jewellery and your crown, but if you want to love me and be your playmate, let me sit next to you at your table, eat from your plate, drink from your little glass and to sleep beside you in your little bed: if you promise me these things I will go down to the well and bring you back your golden ball.'\n" +
            "\n\"Oh well,\" replied the girl, \"I promise you anything you want as long as you bring me my golden ball.\" Yet she inwardly thought that the frog's place was with his fellows in the water, and he could be no person's friend.\n" +
            "\nAs soon as the frog heard that the princess agreed, he dived into the water. After disappearing for a while, he reappeared on the surface of the water with the ball in his mouth. Then he threw the ball on the grass. The princess was very happy when she saw her toy, she took it in her hands and ran away. \"Wait, wait take me with you, I can't run as fast as you,” cried the frog. However, no matter how much the frog shouted, the princess paid no attention and ran back to the palace and she soon forgot about the frog.\n",
        gr: "Κοντά στο παλάτι του βασιλιά ήταν ένα μεγάλο δάσος όπου υπήρχε ένα πηγάδι. Όποτε είχε πολύ ζέστη η μικρή βασιλοπούλα συνήθιζε να κάθεται δίπλα στο πηγάδι για να δροσιστεί. Συνήθιζε να παίζει με μία χρυσή σφαίρα την οποία πετούσε στον αέρα και την έπιανε. Από όλα της τα παιχνίδια αυτή τη σφαίρα την αγαπούσε πιο πολύ. Κάποια μέρα η σφαίρα της, της έφυγε από τα χέρια και αφού αναπήδησε στο έδαφος έπεσε μέσα στο πηγάδι. Η βασιλοπούλα έβλεπε την σφαίρα να πέφτει στο νερό, αλλά το πηγάδι ήταν τόσο βαθύ που δεν φαινόταν ο πάτος του. Τότε το κορίτσι άρχισε να κλαίει απαρηγόρητα, και όσο περνούσε η ώρα έκλαιγε ολοένα και πιο δυνατά. Καθώς έκλαιγε, της φώναξε κάποιος: «Τι έχεις βασιλοπούλα, κλαις τόσο πολύ που θα σε λυπόταν ακόμη και μία πέτρα!» Η βασιλοπούλα κοίταξε γύρω της για να δει ποιος μίλησε. Τότε είδε έναν βάτραχο ο οποίος είχε βγάλει το γλοιώδη κεφάλι του από το νερό.\n" +
            "\n«Ά, εσύ είσαι νεροανακατωσάρη;» του λέει η βασιλοπούλα «κλαίω για την χρυσή μου σφαίρα που έπεσε στο πηγάδι.»\n" +
            "\n«Ησύχασε και μη κλαις και εγώ μπορώ να σου βρω τη λύση» απάντησε ο βάτραχος «αλλά πες μου τι θα μου δώσεις αν σου φέρω το παιχνίδι σου;»\n" +
            "\n«Ότι σου αρέσει και αγαπάς βατραχάκο μου» απάντησε η κοπέλα «τα ρούχα μου, τα χρυσαφικά και τα διαμαντικά μου, ακόμη και την χρυσή κορώνα που φοράω.»\n" +
            "\n«Τα ρούχα σου, τα χρυσαφικά και η κορώνα σου δεν με ενδιαφέρουν, αλλά αν θέλεις να με αγαπάς και να είμαι ο φίλος στα παιχνίδια σου, να με αφήνεις να κάθομαι δίπλα σου στο τραπεζάκι σου, να τρώω από το πιατάκι σου, να πίνω από το ποτηράκι σου και να κοιμάμαι δίπλα σου στο κρεβατάκι σου: αν μου τα υποσχεθείς αυτά θα κατεβώ στο πηγάδι και θα σου ξαναφέρω την χρυσή σου σφαίρα».\n" +
            "\n«Α καλά», απάντησε η κοπέλα «σου υπόσχομαι ό,τι θέλεις αρκεί να μου φέρεις τη χρυσή μου σφαίρα.» Ωστόσο από μέσα της σκεφτόταν ότι η θέση του  βάτραχου είναι με τους όμοιούς του μέσα στο νερό και δεν θα μπορούσε να είναι φίλος κανενός ανθρώπου.\n" +
            "\nΜόλις ο βάτραχος άκουσε ότι η βασιλοπούλα συμφωνεί βούτηξε στο νερό. Αφού εξαφανίστηκε για λίγο εμφανίστηκε πάλι στην επιφάνεια του νερού έχοντας την σφαίρα στο στόμα. Μετά πέταξε την σφαίρα στο γρασίδι. Η βασιλοπούλα χάρηκε πολύ μόλις είδε το παιχνίδι της, το πήρε στα χέρια και έφυγε τρέχοντας. «Περίμενε, περίμενε να με πάρεις μαζί σου δεν μπορώ να τρέχω τόσο γρήγορα σαν εσένα» φώναξε ο βάτραχος. Ωστόσο όσο και να φώναζε ο βάτραχος, η βασιλοπούλα δεν έδινε σημασία και επέστρεψε τρέχοντας στο παλάτι και σύντομα είχε ξεχάσει τον βάτραχο.\n",
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
        return (
            <AnnotationsContext.Provider value={annotations}>
                <Before/>
            </AnnotationsContext.Provider>
        )
    }

    return (
        <div>
            <Title title={isEnglish ? titleText.en : titleText.gr}/>
            <Paragraph text={isEnglish ? explanationText.en : explanationText.gr}/>

            <div className={styles.annotatorRow}>
                <div className={styles.annotationCreator}>
                    <div className={styles.valueContainer}>
                        <p>{isEnglish ? "Value" : "Αξία"}: </p>
                        <input type="text"
                               placeholder={isEnglish ? "Enter value" : "Εισάγετε αξία"}
                               className={styles.tagInput}
                               value={annotationTag}
                               onChange={(newTag) => {
                                   setAnnotationTag(newTag.target.value);
                               }}/>
                    </div>
                    <div className={styles.colorPickerContainer}>
                        <CirclePicker
                            color={annotationColor}
                            onChangeComplete={(color) => {
                                setAnnotationColor(color.hex);
                            }}/>
                    </div>
                </div>
            </div>

            <div className={styles.annotatorRow}>
                <div className={styles.annotatorContainer}>
                    <TextAnnotator
                        style={{
                            maxWidth: 610,
                            lineHeight: 1.3,
                        }}
                        content={(isEnglish ? annotationText.en : annotationText.gr)}
                        value={annotations}
                        onChange={value => setAnnotations(value)}
                        getSpan={span => ({
                            ...span,
                            tag: annotationTag,
                            color: annotationColor,
                        })}
                    />

                    <p>({isEnglish ? "The Frog Prince" : "Ο Βασιλιάς Βάτραχος"} - <a target="_blank"
                                                                                     href="https://www.paidika-paramythia.gr/story/16/o-basilias-batrahos">https://www.paidika-paramythia.gr/story/16/o-basilias-batrahos</a>)
                    </p>
                </div>
            </div>


            <pre className={styles.annotatorContainer}
                 style={{textAlign: "left"}}>{JSON.stringify(annotations, null, 2)}</pre>

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