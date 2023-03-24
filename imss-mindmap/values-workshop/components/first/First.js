import styles from './first.module.css'
import {FaArrowDown} from 'react-icons/fa'
import { useState,useEffect } from 'react';
import Button from '@component/ui/button/Button';
import Second from '../second/Second';

function First({selectedWordsArray, userid}) {
    const [next, setNext] = useState(false);
    const [newArr, setNewArr] = useState([]);
    const [selectedValues, setSelectedValues] = useState([]);

    useEffect(() => {
        const updatedArray = selectedWordsArray.map((obj, index) => {
          return {
            ...obj,
            id: index
          };
        });
        setNewArr(updatedArray);
      }, []);


    const handleSelect = (value) =>{
        const updatedValue = {...value, selected:true};
        const updatedFirstArray = newArr.filter((obj) => obj.id !== value.id);
        const updatedSecondArray = [...selectedValues, updatedValue];

        setNewArr(updatedFirstArray);
        setSelectedValues(updatedSecondArray);
    }

    if(next){
        //return <Second selectedWordsArray={selectedWordsArray} />
        return <Second userid={userid} selectedValuesfirst={selectedValues} selectedWordsArray={selectedWordsArray} />
    }


    return (
        <div className={styles.container}>
            <h1 className={styles.primaryHeadline}>Υψηλότερο επίπεδο</h1>

            <h3 className={styles.tertiaryHeadline}>Επίλεξε Μια Αξία</h3>

            <div className={styles.valuesContainer}>
                {newArr.map((value, index) => {
                    return (
                        <div onClick={() => handleSelect(value)} key={index} className={styles.valueContainer}>{value.comment}</div>
                    )
                })}
            </div>
            <div className={styles.iconContainer}>
                <FaArrowDown className={styles.icon} />
            </div>

            <div className={styles.valuesPlaceholder}>
                <h2 className={styles.secondaryHeadline}>Υψηλότερο επίπεδο Αξιών</h2>
                <div className={styles.valuePlaceholder}>
                    {selectedValues.map((value, index) => {
                        return (
                            <div key={index} className={styles.placeHolder}>{value.comment}</div>
                        )
                    })}
                </div>
            </div>

            <Button onClick={() => setNext(!next)} color="#5C47C2" title="Επομενο" />
        
        </div>
        
    )
}

export default First