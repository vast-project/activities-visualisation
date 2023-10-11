import {useContext, useState} from 'react'
import styles from './congratulations.module.css'
import {IdContext} from '../welcome/Welcome'
import {LangContext} from "../layout/Layout";
import {DotLoader} from "react-spinners";


function Congratulations({annotations, selectedValuesFromFirst, selectedValuesFromSecond, selectedValuesFromThird}) {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const userId = useContext(IdContext);
    const [saving, setSaving] = useState(true);

    console.log("User ID", userId)
    console.log("Annotations", annotations)
    console.log("1st values", selectedValuesFromFirst)
    console.log("2nd values", selectedValuesFromSecond)
    console.log("3rd values", selectedValuesFromThird)

    // todo: Save the data to the api, and then set saving to false!

    return (
        <div className={styles.container}>
            <h1 className={styles.primaryHeadline}>{isEnglish ? 'Congratulations' : 'Συγχαρητήρια'}</h1>
            <h4>{isEnglish ? 'Chosen Values' : 'Οι αξίες που επιλέξατε.'}</h4>
            <div className={styles.valuesContainer}>
                <h3 className={styles.valueContainerHeadline}>{isEnglish ? 'HIGH LEVEL' : 'ΠΡΩΤΟ ΕΠΙΠΕΔΟ'}</h3>
                <div className={styles.valueContainer}>

                    {selectedValuesFromFirst.map((value, index) => {
                        return (
                            <div key={index} className={styles.value}>{value.comment}</div>
                        )
                    })}
                </div>
                <h3 className={styles.valueContainerHeadline}>{isEnglish ? 'SECONDARY LEVEL' : 'ΔΕΥΤΕΡΟ ΕΠΙΠΕΔΟ'}</h3>
                <div className={styles.valueContainer}>
                    {selectedValuesFromSecond.map((value, index) => {
                        return (
                            <div key={index} className={styles.value}>{value.comment}</div>
                        )
                    })}
                </div>
                <h3 className={styles.valueContainerHeadline}>{isEnglish ? 'LOW LEVEL' : 'ΤΡΙΤΟ ΕΠΙΠΕΔΟ'}</h3>
                <div className={styles.valueContainer}>
                    {selectedValuesFromThird.map((value, index) => {
                        return (
                            <div key={index} className={styles.value}>{value.comment}</div>
                        )
                    })}
                </div>
            </div>
            {saving ?
                <div>
                    <div className={styles.dotLoader}>
                        <DotLoader color="#36d7b7"/>
                    </div>
                    <div className={styles.savingText}>
                        <span>{isEnglish ? "Saving data..." : "Αποθήκευση δεδομένων..."}</span>
                    </div>
                </div>
                :
                <div className={styles.savingText}>
                    <span>{isEnglish ? "Thank you for participating!" : "Ευχαριστούμε για τη συμμετοχή!"}</span>
                </div>
            }
        </div>
    )
}

export default Congratulations
