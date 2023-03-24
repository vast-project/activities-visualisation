import {useState} from 'react'
import styles from './instructions.module.css'
import { BsCheck2Circle } from 'react-icons/bs'
import Button from '@component/ui/button/Button';
import TextAnnotations from '../textAnnotation/TextAnnotation';


function Instructions({userid}) {
    const [next, setNext] = useState(false);

    if(next){
      return <TextAnnotations userid={userid} />
    }

  return (
    <div className={styles.container}>
      <h1 className={styles.primaryHeadline}>Οδηγίες Εντοπισμού Αξιών</h1>
      <h3 className={styles.secondaryHeadline}>Επισημείωση/Σύνδεση αξιών με λέξεις/φράσεις του κειμένου </h3>
      <ul className={styles.instructionsList}>
        <li className={styles.instructionsItem}><BsCheck2Circle className={styles.icon} />Διαβάστε μία φορά το κείμενο (χωρίς επισημείωση).</li>
        <li className={styles.instructionsItem}><BsCheck2Circle className={styles.icon} />Διαβάστε δεύτερη φορά το κείμενο εντοπίζοντας λέξεις/φράσεις που ξεκάθαρα μιλούν για μια αξία. Για παράδειγμα  η φράση:  “...κάποιος πρέπει να μιλά ελεθευρια” συνδέεται με την αξία “ελευθερία λόγου”.
        </li>
        <li className={styles.instructionsItem}><BsCheck2Circle className={styles.icon} />Διαβάστε τρίτη φορά το κείμενο εντοπίζοντας λέξεις/φράσεις που έμμεσα μιλούν για μια αξία. Για παράδειγμα  η φράση:  “... είναι πάντα πλήρως ενημερωμένη για τις τρέχουσες εξελίξεις ” συνδέεται με την αξία “γνώση”.</li>
        <li className={styles.instructionsItem}><BsCheck2Circle className={styles.icon} /> Αποτυπώστε την πρώτη σας εντύπωση - δεν υπάρχει σωστή ή λάθος ερμηνεία</li>
      </ul>

      <Button onClick={() => setNext(!next)} color="#5C47C2" title="Εντοπισμος αξιων" />
    </div>
  )
}

export default Instructions
