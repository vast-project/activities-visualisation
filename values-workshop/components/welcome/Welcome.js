import {useState, createContext, useContext} from 'react'
import styles from './welcome.module.css'
import { BsArrowRight } from 'react-icons/bs'
import Instructions from '../instructions/Instructions';
import Button from '@component/ui/button/Button';
import Congratulations from '../congratulations/Congratulations';
import { LangContext } from "../layout/Layout";

// Create Context
export const IdContext = createContext();

console.log(IdContext);

function Welcome() {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const [start, setStart] = useState(false);
    const [cong, setCong] = useState(false);
    const [id, setId] = useState('');

    if(start){
      return <Instructions />
    }

  return (
    <IdContext.Provider value="vjassa" >
        <div className={styles.container}>
        <h1 className={styles.primaryHeadline}>VAST Values Workshop</h1>
        {/* <h3 className={styles.secondaryHeadline}>Εργαστήριο Αξιών VAST</h3> */}
        <p className={styles.text}>{
        isEnglish 
        ?
        "The VAST values ​​workshop includes two actions. In the first activity you are asked to indicate the values ​​that you think are conveyed by a passage from the play by the writer Karel Capek (1890-1938) “Rossum's Universal Robots” (1920). Instructions on how to locate the values ​​are given on the next page. Then, during the second activity you are asked to rank the values ​​you identified in the text according to their importance in your life. Have fun!"
        :
        'Το εργαστήριο αξιών VAST περιλαμβάνει δύο δράσεις. Στην πρώτη δράση καλείστε να υποδείξετε τις αξίες που μεταφέρει σύμφωνα με τη γνώμη σας ένα απόσπασμα από το θεατρικό έργο του συγγραφέα Karel Capek (1890-1938) “Rossum’s Universal Robots” (1920). Οι οδηγίες για τον τρόπο εντοπισμού των αξιών δίνονται στην επόμενη σελίδα. Στη συνέχεια, κατά τη διάρκεια της δεύτερης δράσης καλείστε να ιεραρχήσετε τις αξίες που εντοπίσατε στο κείμενο με γνώμονα τη σημαντικότητά τους στη ζωή σας. Καλή διασκέδαση! '}
        </p>
        <form>
          <div className={styles.inputContainer}>
              <label htmlFor="password">{isEnglish ? 'Insert Password' : 'Εισαγωγή Κωδικού'}</label>
              <input name="password" value={id} onChange={(e) => setId(e.target.value)} className={styles.input} type="text" />
          </div>
          <Button type="submit" onClick={() => setStart(!start)} color="#5C47C2" title={isEnglish ? 'START' : "ΕΝΑΡΞΗ"} />
        </form>
      </div>
      {cong ? <Congratulations /> : ''}
    </IdContext.Provider>
  )
}

export default Welcome
