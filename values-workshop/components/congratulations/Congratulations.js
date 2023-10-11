import {useContext, useState} from 'react'
import styles from './congratulations.module.css'
import {IdContext} from '../welcome/Welcome'
import {LangContext} from "../layout/Layout";
import {DotLoader} from "react-spinners";

const backendUrl = "https://activities-backend.vast-project.eu";

const saveData = async function (data) {
    // Send the POST request
    return fetch(backendUrl + '/api/save-values-workshop-data', {
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

function selectedValueToAnnotation(selectedValue) {
    return {
        segment: selectedValue.text,
        value: selectedValue.comment,
    }
}

function Congratulations({annotations, selectedValuesFromFirst, selectedValuesFromSecond, selectedValuesFromThird}) {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const userId = useContext(IdContext);
    const [saving, setSaving] = useState(true);

    const data = {
        userId: userId,
        annotations: annotations,
        valueLevels: [
            {
                level: 1,
                values: selectedValuesFromFirst.map(v => selectedValueToAnnotation(v))
            }, {
                level: 2,
                values: selectedValuesFromSecond.map(v => selectedValueToAnnotation(v))
            }, {
                level: 3,
                values: selectedValuesFromThird.map(v => selectedValueToAnnotation(v))
            },
        ]
    }

    if (saving) {
        console.log("Saving data: ", data);
        saveData(data).then(() => {
            setSaving(false);
        })
    }


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
