import {useContext, useState} from 'react'
import styles from './writingactivity.module.css'
import {LangContext} from '../../layout/Layout.jsx'
import Title from "../../ui/Title/Title.jsx";
import Button from "../../ui/Button/Button.jsx";
import CardsActivity, {CharactersContext, FunctionsContext} from "../cards-activity/CardsActivity.jsx";
import Congratulations from "../congratulations/Congratulations.jsx";
import {AnnotationsContext} from "../annotation-activity/AnnotationActivity.jsx";

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
        valuesSrc.push(`../../../../public/values/${selectedValues[i]}.png`);
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

        // Make call to API
        saveData(dataForBackend).then(() => {
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
