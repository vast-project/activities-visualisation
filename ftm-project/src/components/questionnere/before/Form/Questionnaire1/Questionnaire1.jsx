import Paragraph from '../../../../../ui/Paragraph/Paragraph'
import { useState } from 'react';
import styles from './questionnaire.module.css'
import {BsFillArrowUpCircleFill, BsFillArrowDownCircleFill} from 'react-icons/bs'

const text = "Αν θεωρήσουμε ότι οι αξίες αναφέρονται σε κάποιες βασικές αρχές ή πρότυπα συμπεριφοράς, κατηγοριοποιήστε βάζοντας  με βάση το ποιες θεωρείτε πιο σημαντικές στη σημερινή εποχή, τις ακόλουθες αξίες."

const questions = [
    {
      id: 1,
      question: "Ισότητα",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
    {
      id: 2,
      question: "Ελευθερία",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
    {
      id: 3,
      question: "Δημοκρατία",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
    {
      id: 4,
      question: "Δικαιοσύνη",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
    {
      id: 5,
      question: "Ειρήνη",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
    {
      id: 6,
      question: "Αγάπη",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
    {
      id: 7,
      question: "Αφοσίωση",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
    {
      id: 8,
      question: "Σεβασμός",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
    {
      id: 9,
      question: "Αλληλεγγύη",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
    {
      id: 10,
      question: "Ανοχή",
      options: [
        { id: 1, label: "1" },
        { id: 2, label: "2" },
        { id: 3, label: "3" },
        { id: 4, label: "4" },
        { id: 5, label: "5" },
        { id: 6, label: "6" },
        { id: 7, label: "7" },
        { id: 8, label: "8" },
        { id: 9, label: "9" },
        { id: 10, label: "10" },
      ],
    },
  ];

const Questionnaire = () => {
    const [answers, setAnswers] = useState({});
    const [showQuestionnaire, setShowQuestionnaire] = useState(false)


    const handleAnswerChange = (event) => {
        const { name, value } = event.target;
        setAnswers((prevState) => ({ ...prevState, [name]: value }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(answers);
    };

    const questionnaire = questions.map((question) => (
        <div key={question.id}>
        <h3>{question.question}</h3>
        {question.options.map((option) => (
            <label key={option.id}>
              <input
                  type="radio"
                  name={`question_${question.id}`}
                  value={option.label}
                  checked={answers[`question_${question.id}`] === option.label}
                  onChange={handleAnswerChange}
              />
              {option.label}
            </label>
        ))}
        </div>
    ))


    return (
        <>
            <div className={styles.titleContainer}>
                <h4>Ερωτηματολόγιο 1</h4>
                {showQuestionnaire
                ?
                    <BsFillArrowUpCircleFill onClick={() => setShowQuestionnaire(false)} className={styles.icon} />
                :
                    <BsFillArrowDownCircleFill onClick={() => setShowQuestionnaire(true)} className={styles.icon} />
                }                    
            </div>
            {/* Questionnaire 1 */}
            {
                showQuestionnaire
                &&
                <form onSubmit={handleSubmit}> 
                    <Paragraph text={text} />
                    {questionnaire}
                    <button className={styles.submitBtn} type="submit">Submit</button>
                </form>
            }
        </>
    )
}

export default Questionnaire