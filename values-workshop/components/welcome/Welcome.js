import {useState} from 'react'
import styles from './welcome.module.css'
import { BsArrowRight } from 'react-icons/bs'
import Instructions from '../instructions/Instructions';
import Button from '@component/ui/button/Button';

function Welcome() {
  const [start, setStart] = useState(false);
  const [userid, setUserid] = useState('');
  
    const handleChange = (event) => {
      setUserid(event.target.value)
    };

    if(start){
      return <Instructions userid={userid} />
    }

  return (
    <div className={styles.container}>
      <h1 className={styles.primaryHeadline}>VAST Values Workshop</h1>
      <h3 className={styles.secondaryHeadline}>Εργαστήριο Αξιών VAST</h3>
      <p className={styles.text}>Το εργαστήριο αξιών VAST περιλαμβάνει δύο δράσεις. Στην πρώτη δράση καλείστε να υποδείξετε τις αξίες που μεταφέρει σύμφωνα με τη γνώμη σας ένα απόσπασμα από το θεατρικό έργο του συγγραφέα Karel Capek (1890-1938) “Rossum’s Universal Robots” (1920). Οι οδηγίες για τον τρόπο εντοπισμού των αξιών δίνονται στην επόμενη σελίδα. Στη συνέχεια, κατά τη διάρκεια της δεύτερης δράσης καλείστε να ιεραρχήσετε τις αξίες που εντοπίσατε στο κείμενο με γνώμονα τη σημαντικότητά τους στη ζωή σας. Καλή διασκέδαση! 
</p>
      <form>
        <div className={styles.inputContainer}>
            <label htmlFor="password">Εισαγωγή Κωδικού</label>
            <input name="password" className={styles.input} type="text" onChange ={handleChange} />
        </div>
        
      </form>
      {/* <button onClick={() => setStart(!start)} className={styles.btn}>Start <BsArrowRight/></button> */}
      <Button onClick={() => setStart(!start)} color="#5C47C2" title="ΕΝΑΡΞΗ" />
    </div>
  )
}

export default Welcome
