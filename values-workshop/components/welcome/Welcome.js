import React, {createContext, useContext, useRef, useState} from 'react'
import styles from './welcome.module.css'
import Instructions from '../instructions/Instructions';
import Button from '@component/ui/button/Button';
import Congratulations from '../congratulations/Congratulations';
import {LangContext} from "../layout/Layout";

// Create Context
export const IdContext = createContext();

console.log(IdContext);

async function savevisitor(data) {
    try {
        const response = await fetch('https://activities_backend.vast-project.eu/api/savevisitor', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {'Content-Type': 'application/json'}
        });

        if (!response.ok) {
            console.log(response)
            throw new Error(`Error! status: ${response.status}`);
        }

        const result = await response.json();
        return result;
    } catch (err) {
        console.log(err);
    }
}

function Welcome() {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const [start, setStart] = useState(false);
    const [cong, setCong] = useState(false);
    const [id, setId] = useState('');
    var jsondata = {
        name: "Values Workshop Visitor",
        userid: null,
        created_by: 3,
        age: null,
        gender: null,
        education: null,
        nationality: null,
        motherLanguage: null,
        activity: null,
        group: null
    };

    const useridRef = useRef(null);

    const handleSubmit = event => {
        jsondata = {
            name: "Values Workshop Visitor",
            userid: useridRef.current.value,
            created_by: 3,
            age: null,
            gender: null,
            education: null,
            motherLanguage: 3,
            activity: vstepid,
            group: vgroupname,
            nationality: 3
        }
        console.log("JSON DATA")
        console.log(jsondata)
        savevisitor(jsondata)
        event.target.reset()
    }

    if (start) {
        jsondata = {
            name: "Values Workshop Visitor",
            userid: useridRef.current.value,
            created_by: 3,
            age: null,
            gender: null,
            education: null,
            motherLanguage: 3,
            activity: 2,
            group: 2,
            nationality: 3
        };
        console.log("JSON DATA");
        console.log(jsondata);
        savevisitor(jsondata);
        return <Instructions/>
    }

    const englishText = "The VAST values workshop includes two actions. In the first activity you are asked to indicate the values that you think are conveyed by a passage from the play by the writer Karel Capek (1890-1938) “Rossum's Universal Robots” (1920). Instructions on how to locate the values are given on the next page. Then, during the second activity you are asked to rank the values you identified in the text according to their importance in your life. Have fun!";
    const greekText = "Το εργαστήριο αξιών VAST περιλαμβάνει δύο δράσεις. Στην πρώτη δράση καλείστε να υποδείξετε τις αξίες που μεταφέρει σύμφωνα με τη γνώμη σας ένα απόσπασμα από το θεατρικό έργο του συγγραφέα Karel Capek (1890-1938) “Rossum’s Universal Robots” (1920). Οι οδηγίες για τον τρόπο εντοπισμού των αξιών δίνονται στην επόμενη σελίδα. Στη συνέχεια, κατά τη διάρκεια της δεύτερης δράσης καλείστε να ιεραρχήσετε τις αξίες που εντοπίσατε στο κείμενο με γνώμονα τη σημαντικότητά τους στη ζωή σας. Καλή διασκέδαση!";

    return (
        <IdContext.Provider value="vjassa">
            <div className={styles.container}>
                <h1 className={styles.primaryHeadline}>VAST Values Workshop</h1>
                <p className={styles.text}>
                    {isEnglish ? englishText : greekText}
                </p>
                <form>
                    <div className={styles.inputContainer}>
                        <label htmlFor="userid">{isEnglish ? 'Enter User ID' : 'Εισαγωγή Κωδικού Χρήστη'}</label>
                        <input ref={useridRef} name="userid" value={id} onChange={(e) => setId(e.target.value)}
                               className={styles.input} type="text"/>
                    </div>
                    <Button type="submit" onClick={() => setStart(!start)} color="#5C47C2"
                            title={isEnglish ? 'START' : "ΕΝΑΡΞΗ"}/>
                </form>
            </div>
            {cong ? <Congratulations/> : ''}
        </IdContext.Provider>
    )
}

export default Welcome
