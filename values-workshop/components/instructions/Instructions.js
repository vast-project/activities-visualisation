import {useState,useContext} from 'react'
import styles from './instructions.module.css'
import { BsCheck2Circle,BsArrowLeftCircleFill } from 'react-icons/bs'
import Button from '@component/ui/button/Button';
import TextAnnotations from '../textAnnotation/TextAnnotation';
import Welcome from '../welcome/Welcome';
import { LangContext } from "../layout/Layout";



function Instructions() {
  const {isEnglish, setIsEnglish} = useContext(LangContext)
  const [next, setNext] = useState(false);
  const [previous, setPrevious] = useState(false);

  if(next){
    return <TextAnnotations />
  }
  if(previous){
    return <Welcome />
  }

  return (
    <div className={styles.container}>
      <BsArrowLeftCircleFill onClick={() => setPrevious(true)} className={styles.leftArrow} />
      <h1 className={styles.primaryHeadline}>{isEnglish ? 'Guidelines for Locating Values' : 'Οδηγίες Εντοπισμού Αξιών'}</h1>
      <h3 className={styles.secondaryHeadline}>{isEnglish ? 'Marking/Associating values ​​with words/phrases in the text' : 'Επισημείωση/Σύνδεση αξιών με λέξεις/φράσεις του κειμένου'} </h3>
      <ul className={styles.instructionsList}>
        <li className={styles.instructionsItem}><BsCheck2Circle className={styles.icon} />{isEnglish ? 'Read the text once (without marking).' : 'Διαβάστε μία φορά το κείμενο (χωρίς επισημείωση).'}</li>
        <li className={styles.instructionsItem}><BsCheck2Circle className={styles.icon} />{isEnglish ? 'Read the text a second time looking for words/phrases that clearly speak of a value.' : 'Διαβάστε δεύτερη φορά το κείμενο εντοπίζοντας λέξεις/φράσεις που ξεκάθαρα μιλούν για μια αξία.'}
        </li>
        <li className={styles.instructionsItem}><BsCheck2Circle className={styles.icon} />{isEnglish ? 'Read the text a third time finding words/phrases that indirectly talk about a value. For example the phrase: "... is always fully informed about current developments" is associated with the value "knowledge".' : 'Διαβάστε τρίτη φορά το κείμενο εντοπίζοντας λέξεις/φράσεις που έμμεσα μιλούν για μια αξία. Για παράδειγμα  η φράση:  “... είναι πάντα πλήρως ενημερωμένη για τις τρέχουσες εξελίξεις ” συνδέεται με την αξία “γνώση”.'}</li>
        <li className={styles.instructionsItem}><BsCheck2Circle className={styles.icon} />{isEnglish ? 'Capture your first impression - there is no right or wrong interpretation' : 'Αποτυπώστε την πρώτη σας εντύπωση - δεν υπάρχει σωστή ή λάθος ερμηνεία.'}</li>
      </ul>

      <Button onClick={() => setNext(!next)} color="#5C47C2" title={isEnglish ? 'ΝΕΧΤ' : "ΕΠΟΜΕΝΟ"} />
    </div>
  )
}

export default Instructions
