import React, {createContext, useContext, useRef, useState} from 'react'
import styles from './welcome.module.css'
import Instructions from '../instructions/Instructions';
import Button from '@component/ui/button/Button';
import {LangContext} from "../layout/Layout";

// Create Context for the user ID
export const IdContext = createContext();
export const TeamContext = createContext();

function Welcome() {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const [start, setStart] = useState(false);
    const [userId, setUserId] = useState('');
    const [teamNumber, setTeamNumber] = useState('');
    const [showUserIdWarning, setShowUserIdWarning] = useState(false);
    const [showTeamNumberWarning, setShowTeamNumberWarning] = useState(false);

    const useridRef = useRef(null);
    const teamNumberRef = useRef(null);
    if (start) {
        return (
            <IdContext.Provider value={userId}>
                <TeamContext.Provider value={teamNumber}>
                    <Instructions/>
                </TeamContext.Provider>
            </IdContext.Provider>
        )
    }

    /**
     * Go to the next page if the user ID is set, or show warning otherwise.
     * @param e The click event
     */
    const handleSubmit = (e) => {
        // Prevent default to avoid page reload on form submission
        e.preventDefault();
        if (userId !== '' && teamNumber !== '') {
            setStart(true);
        } else {
            if (userId === '') {
                setShowUserIdWarning(true);
            }
            if (teamNumber === '') {
                setShowTeamNumberWarning(true);
            }
        }
    }

    const englishText = "The VAST values workshop includes two actions. In the first activity you are asked to indicate the values that you think are conveyed by a passage from the play by the writer Karel Capek (1890-1938) “Rossum's Universal Robots” (1920). Instructions on how to locate the values are given on the next page. Then, during the second activity you are asked to rank the values you identified in the text according to their importance in your life. Have fun!";
    const greekText = "Το εργαστήριο αξιών VAST περιλαμβάνει δύο δράσεις. Στην πρώτη δράση καλείστε να υποδείξετε τις αξίες που μεταφέρει σύμφωνα με τη γνώμη σας ένα απόσπασμα από το θεατρικό έργο του συγγραφέα Karel Capek (1890-1938) “Rossum’s Universal Robots” (1920). Οι οδηγίες για τον τρόπο εντοπισμού των αξιών δίνονται στην επόμενη σελίδα. Στη συνέχεια, κατά τη διάρκεια της δεύτερης δράσης καλείστε να ιεραρχήσετε τις αξίες που εντοπίσατε στο κείμενο με γνώμονα τη σημαντικότητά τους στη ζωή σας. Καλή διασκέδαση!";

    return (
        <div className={styles.container}>
            <h1 className={styles.primaryHeadline}>VAST Values Workshop</h1>
            <p className={styles.text}>
                {isEnglish ? englishText : greekText}
            </p>
            <form>
                <div className={styles.inputContainer}>
                    <label htmlFor="userid">{isEnglish ? 'Enter User ID' : 'Εισαγωγή Κωδικού Χρήστη'}</label>
                    <input ref={useridRef} name="userid" value={userId} onChange={(e) => setUserId(e.target.value)}
                           className={styles.input} type="text"/>
                </div>
                {showUserIdWarning &&
                    <p className={styles.warning}>{isEnglish ? 'Please enter a user ID' : 'Παρακαλώ εισάγετε έναν κωδικό χρήστη'}</p>}

                <div className={styles.inputContainer}>
                    <label htmlFor="userid">{isEnglish ? 'Team number' : 'Αριθμός ομάδας'}</label>
                    <input ref={teamNumberRef} name="teamNumber" value={teamNumber} onChange={(e) => setTeamNumber(e.target.value)}
                           className={styles.input} type="text"/>
                </div>
                {showTeamNumberWarning &&
                    <p className={styles.warning}>{isEnglish ? 'Please enter a team number' : 'Παρακαλώ εισάγετε έναν αριθμό ομάδας'}</p>}


                <Button type="submit" onClick={handleSubmit} color="#5C47C2" title={isEnglish ? 'START' : "ΕΝΑΡΞΗ"}/>
            </form>
        </div>
    )
}

export default Welcome
