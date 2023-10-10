import {useContext} from 'react'
import styles from './congratulations.module.css'
import {IdContext} from '../welcome/Welcome'
import {LangContext} from "../layout/Layout";


function Congratulations({annotations, selectedValuesFromFirst, selectedValuesFromSecond, selectedValuesFromThird}) {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const userId = useContext(IdContext);

    console.log("User ID", userId)
    console.log("Annotations", annotations)
    console.log("1st values", selectedValuesFromFirst)
    console.log("2nd values", selectedValuesFromSecond)
    console.log("3rd values", selectedValuesFromThird)

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
        </div>
    )
}

export default Congratulations
