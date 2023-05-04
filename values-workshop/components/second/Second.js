import styles from './second.module.css'
import {FaArrowDown} from 'react-icons/fa'
import { useState,useEffect } from 'react';
import Button from '@component/ui/button/Button';
import Third from '../third/Third';

function Second({userid, selectedValuesfirst, selectedWordsArray}) {
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
        //return <Third selectedWordsArray={selectedWordsArray} />
        return <Third userid={userid} selectedValuesfirst={selectedValuesfirst} selectedValuessecond={selectedValues} selectedWordsArray={selectedWordsArray} />
    }

    return (
        <div className={styles.container}>
            <h1 className={styles.primaryHeadline}>Μεσαίο επίπεδο</h1>

            <h3 className={styles.tertiaryHeadline}>Επίλεξε 3 Αξίες</h3>

            <div className={styles.valuesContainer}>
                {newArr.map((value, index) => {
                    return (
                        <div onClick={() => handleSelect(value)} key={index} className={styles.valueContainer}>{value.comment}</div>
                        // <DraggableDiv key={index} id={index} draggable="true" value={value.comment} />
                    )
                })}
            </div>
            <div className={styles.iconContainer}>
                <FaArrowDown className={styles.icon} />
            </div>

            <div className={styles.valuesPlaceholder}>
                <h2 className={styles.secondaryHeadline}>Μεσαίο Επίπεδο Αξιών</h2>
                <div className={styles.valuePlaceholder}>
                    {selectedValues.map((value, index) => {
                        return (
                            <div key={index} className={styles.placeHolder}>{value.comment}</div>
                            // <DraggableDiv key={index} id={index} draggable="true" value={value.comment} />
                        )
                    })}
                </div>
            </div>

            <Button onClick={() => setNext(!next)} color="#FFC857" title="Επομενο" />
        
        </div>
        
    )
}

export default Second