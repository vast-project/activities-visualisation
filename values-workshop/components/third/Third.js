import styles from './third.module.css'
import {FaArrowDown} from 'react-icons/fa'
import { BsArrowLeftCircleFill } from 'react-icons/bs'
import { useState,useEffect,useContext } from 'react';
import Button from '@component/ui/button/Button';
import Congratulations from '../congratulations/Congratulations';
import TextAnnotations from '../textAnnotation/TextAnnotation';
import { LangContext } from "../layout/Layout";

function Second({selectedWordsArray,selectedValuesFromFirst,selectedValuesFromSecond}) {
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
        if(count < 5){
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
        return <Congratulations selectedValuesFromThird={selectedValues} selectedValuesFromFirst={selectedValuesFromFirst} selectedValuesFromSecond={selectedValuesFromSecond} />
    }
    if(previous){
        return <TextAnnotations />
    }

    return (
        <div className={styles.container}>
            <BsArrowLeftCircleFill onClick={() => setPrevious(true)} className={styles.leftArrow} />
            <h1 className={styles.primaryHeadline}>{isEnglish ? 'Low Level' : 'Χαμηλό επίπεδο'}</h1>
            <h3 className={styles.tertiaryHeadline}>{isEnglish ? 'Pick 5 Values' : 'Επίλεξε 5 Αξίες'}</h3>
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
                <h2 className={styles.secondaryHeadline}>{isEnglish ? 'Low Value Level' : 'Χαμηλό Επίπεδο Αξιών'}</h2>
                <div className={styles.valuePlaceholder}>
                    {selectedValues.map((value, index) => {
                        return (
                            <div onClick={() => handleRemove(value)} key={index} className={styles.placeHolder}>{value.comment}</div>
                        )
                    })}
                </div>
            </div>

            <Button onClick={() => setNext(!next)} color="#E5446D" title={isEnglish ? 'Next' : "Επομενο"} />
        
        </div>
        
    )
}

export default Second