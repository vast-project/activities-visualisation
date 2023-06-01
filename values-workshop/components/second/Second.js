import styles from './second.module.css'
import {FaArrowDown} from 'react-icons/fa'
import { BsArrowLeftCircleFill } from 'react-icons/bs'
import { useState,useEffect,useContext } from 'react';
import Button from '@component/ui/button/Button';
import Third from '../third/Third'
import First from '../first/First';
import TextAnnotations from '../textAnnotation/TextAnnotation';
import { LangContext } from "../layout/Layout";


function Second({selectedWordsArray,selectedValuesFromFirst}) {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const [next, setNext] = useState(false);
    const [previous, setPrevious] = useState(false);

    const [newArr, setNewArr] = useState([]);
    const [selectedValues, setSelectedValues] = useState([]);
    const [count, setCount] = useState(0);

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
        if(count < 3){
            const updatedValue = {...value, selected:true};
            const updatedFirstArray = newArr.filter((obj) => obj.id !== value.id);
            const updatedSecondArray = [...selectedValues, updatedValue];
    
            setNewArr(updatedFirstArray);
            setSelectedValues(updatedSecondArray);
            setCount( prev => setCount(prev + 1));
        }
    }

    const handleRemove = (value) => {
        setNewArr([value,...newArr ]);
        const updatedArray = selectedValues.filter((obj) => obj.id !== value.id);
        setSelectedValues(updatedArray);
        setCount( prev => setCount(prev - 1));
    }

    if(next){
        return <Third selectedWordsArray={selectedWordsArray} selectedValuesFromFirst={selectedValuesFromFirst} selectedValuesFromSecond={selectedValues} />
    }
    if(previous){
        return <TextAnnotations />
    }

    return (
        <div className={styles.container}>
            <BsArrowLeftCircleFill onClick={() => setPrevious(true)} className={styles.leftArrow} />
            <h1 className={styles.primaryHeadline}>{isEnglish ? 'Secondary Level' : 'Μεσαίο επίπεδο'}</h1>
            <h3 className={styles.tertiaryHeadline}>{isEnglish ? 'Pick 3 Values' : 'Επίλεξε 3 Αξίες'}</h3>
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
                <h2 className={styles.secondaryHeadline}>{isEnglish ? 'Secondary Value Level' : 'Μεσαίο επίπεδο Αξιών'}</h2>
                <div className={styles.valuePlaceholder}>
                    {selectedValues.map((value, index) => {
                        return (
                            <div onClick={() => handleRemove(value)} key={index} className={styles.placeHolder}>{value.comment}</div>
                        )
                    })}
                </div>
            </div>

            <Button onClick={() => setNext(!next)} color="#FFC857" title={isEnglish ? 'Next' : "Επομενο"} />
        
        </div>
        
    )
}

export default Second