import Paragraph from '../../../../../ui/Paragraph/Paragraph'
import { useState } from 'react';
import styles from './questionnaire.module.css'
import {BsFillArrowUpCircleFill, BsFillArrowDownCircleFill} from 'react-icons/bs'

import data from './data';

const Questionnaire2 = () => {
  const [answers, setAnswers] = useState({});
  const [showQuestionnaire, setShowQuestionnaire] = useState(false)
  const handleChange = (e) => {
    const { name, value } = e.target;
    setAnswers((prevAnswers) => ({
      ...prevAnswers,
      [name]: value,
    }));
};

const handleSubmit = (event) => {
    event.preventDefault();
    console.log(answers);
};


  return (
    <form onSubmit={handleSubmit}>
        <div className={styles.titleContainer}>
                <h4>Ερωτηματολόγιο 2</h4>
                {showQuestionnaire
                ?
                    <BsFillArrowUpCircleFill onClick={() => setShowQuestionnaire(false)} className={styles.icon} />
                :
                    <BsFillArrowDownCircleFill onClick={() => setShowQuestionnaire(true)} className={styles.icon} />
                }                    
        </div>
        {
            showQuestionnaire
            &&
            <> 
                {/* <Paragraph text={text} /> */}
                {data.map((question, index) => {
                    return (
                        <div key={question.id} className={styles.questionContainer}>
                            <label className={styles.questionLabel} htmlFor="question1">{question.question}</label>
                            <select className={styles.questionSelect} id={question.id} name={`question-${index}`} onChange={handleChange}>
                                {
                                    question.options.map(option => {
                                        return (
                                            <option key={option.id} value={option.id}>
                                                {option.label}
                                            </option>
                                    )})
                                }
                            </select>  
                        </div>
                        )
                })}
                <button className={styles.submitBtn} type="submit">Submit</button>
            </>
        }       
    </form>
  );
};

export default Questionnaire2;