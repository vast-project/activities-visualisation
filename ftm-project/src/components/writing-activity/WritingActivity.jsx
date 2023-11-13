import {useContext, useState} from 'react'
import styles from './writingactivity.module.css'
import {LangContext} from '../../layout/Layout.jsx'
import Title from "../../ui/Title/Title.jsx";
import Button from "../../ui/Button/Button.jsx";
import CardsActivity, {CharactersContext, FunctionsContext} from "../cards-activity/CardsActivity.jsx";
import Congratulations from "../congratulations/Congratulations.jsx";
import {AnnotationsContext} from "../annotation-activity/AnnotationActivity.jsx";
import {DotLoader} from "react-spinners";

import img1 from '../../../public/values/1.png'
import img2 from '../../../public/values/2.png'
import img3 from '../../../public/values/3.png'
import img4 from '../../../public/values/4.png'
import img5 from '../../../public/values/5.png'
import img6 from '../../../public/values/6.png'
import img7 from '../../../public/values/7.png'
import img8 from '../../../public/values/8.png'
import img9 from '../../../public/values/9.png'
import img10 from '../../../public/values/10.png'
import img11 from '../../../public/values/11.png'
import img12 from '../../../public/values/12.png'
import img13 from '../../../public/values/13.png'
import img14 from '../../../public/values/14.png'
import img15 from '../../../public/values/15.png'
import img16 from '../../../public/values/16.png'
import img17 from '../../../public/values/17.png'
import img18 from '../../../public/values/18.png'
import img19 from '../../../public/values/19.png'
import img20 from '../../../public/values/20.png'
import img21 from '../../../public/values/21.png'
import img22 from '../../../public/values/22.png'
import img23 from '../../../public/values/23.png'
import img24 from '../../../public/values/24.png'
import img25 from '../../../public/values/25.png'

const valueSrcs = [img1, img2, img3, img4, img5, img6, img7, img8, img9, img10, img11, img12, img13, img14,
    img15, img16, img17, img18, img19, img20, img21, img22, img23, img24, img25];

const backendUrl = "https://activities-backend.vast-project.eu";
// const backendUrl = "http://localhost:8000";

const saveData = async function (data) {
    // Send the POST request
    return fetch(backendUrl + '/api/ftm/save-statements', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    }).then(response => {
        if (!response.ok) {
            throw new Error(`Error! Status: ${response.status}`);
        }
        console.log("Data saved successfully");
    }).catch(error => {
        console.error("Error:", error);
    });
}


const WritingActivity = () => {
    const {isEnglish} = useContext(LangContext)
    const annotations = useContext(AnnotationsContext)
    const selectedCharacters = useContext(CharactersContext)
    const selectedFunctions = useContext(FunctionsContext)
    const [next, setNext] = useState(false)
    const [prev, setPrev] = useState(false)
    const [storyText, setStoryText] = useState("")
    const [selectedValues, setSelectedValues] = useState([])
    const [saving, setSaving] = useState(false)

    const numValues = 25; // number of total values that exist
    const valuesToChoose = 3;

    const valueNames = {
        1: "democracy",
        2: "dialogue",
        3: "equality",
        4: "freedom",
        5: "dignity",
        6: "human rights",
        7: "justice",
        8: "peace",
        9: "progress",
        10: "logic",
        11: "cooperation",
        12: "curiosity",
        13: "empathy",
        14: "generosity",
        15: "sincerity",
        16: "integrity",
        17: "kindness",
        18: "love",
        19: "loyalty",
        20: "piety",
        21: "purity",
        22: "respect",
        23: "reward",
        24: "solidarity",
        25: "tolerance",
    }

    // Choose random values
    if (selectedValues.length === 0) {
        console.log("Choosing " + valuesToChoose + " random values...");
        const values = [];
        for (let i = 0; i < valuesToChoose; i++) {
            let value = Math.floor(Math.random() * numValues) + 1;
            // Avoid duplicate values
            while (values.includes(value)) {
                value = Math.floor(Math.random() * numValues) + 1;
            }
            values.push(value);
        }

        setSelectedValues(values);
    }

    // Get the image source paths for the value cards to display in the page
    const valuesSrc = [];
    for (let i = 0; i < selectedValues.length; i++) {
        valuesSrc.push(valueSrcs[selectedValues[i]]);
    }

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

    /**
     * Event handler for the story text area
     * @param event
     */
    const handleStoryChange = event => {
        setStoryText(event.target.value);
    };

    const handleNextBtn = event => {
        // Create statements for saving
        const statements = [];

        // Add annotations to the statements
        annotations.forEach((annotation) => {
            const statement = {
                segment: annotation["text"],
                value: annotation["tag"],
                start: annotation["start"],
                end: annotation["end"],
            };

            statements.push(statement);
        })

        // Create story statements array
        const storyStatements = [];

        // Add story statements for values
        selectedValues.forEach((value) => {
            storyStatements.push({
                // subject will be the story
                predicate: "includes_value",
                object: valueNames[value]
            })
        })

        // Add story statements for characters
        selectedCharacters.forEach((character) => {
            storyStatements.push({
                // subject will be the story
                predicate: "includes_character",
                object: character.name
            })
        })

        // Add story statements for functions
        selectedFunctions.forEach((storyFunction) => {
            storyStatements.push({
                // subject will be the story
                predicate: "includes_function",
                object: storyFunction.name
            })
        })

        // Create object with all the data for the backend
        const dataForBackend = {
            annotations: statements,
            story: storyText,
            storyStatements: storyStatements,
            language: isEnglish ? "en" : "el",
        };
        console.log("Data for backend:", dataForBackend);

        // Show loading animation
        setSaving(true);

        // Make call to API
        saveData(dataForBackend).then(() => {
            setSaving(false);
            setNext(true);
        });
    }

    if (prev) {
        return <CardsActivity/>
    }

    if (next) {
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

            <div className={styles.cardsRow}>
                <div className={styles.storyCards} style={{width: "75%"}}>
                    <span className={styles.cardsTitle}>{isEnglish ? "Values" : "Αξίες"}</span>
                    <div className={styles.cardsContainer}>
                        {
                            valuesSrc.map((src) => {
                                return (
                                    <div className={styles.imageContainer}>
                                        <img src={src} alt="A value"/>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            </div>

            <textarea className={styles.storyInput}
                      placeholder={isEnglish ? textareaPlaceholder.en : textareaPlaceholder.gr}
                      value={storyText}
                      onChange={handleStoryChange}></textarea>

            {saving ?
                <div>
                    <div className={styles.dotLoader}>
                        <DotLoader color="#69A082"/>
                    </div>
                    <div className={styles.savingText}>
                        <span>{isEnglish ? "Saving data..." : "Αποθήκευση δεδομένων..."}</span>
                    </div>
                </div>
                :
                <div/>
            }

            <div className={styles.btnContainer}>
                <button className={styles.btnBack}
                        onClick={() => setPrev(true)}>{isEnglish ? prevBtnText.en : prevBtnText.gr}</button>
                <Button onClick={handleNextBtn} text={isEnglish ? nextBtnText.en : nextBtnText.gr}
                        color="rgb(105, 160, 130)"/>
            </div>
        </div>
    )
}

export default WritingActivity
