import Paragraph from '../../../../ui/Paragraph/Paragraph'
import { useState, useContext } from 'react'
import { LangContext } from './../../../../layout/Layout'
import SubTitle from '../../../../ui/SubTitle/SubTitle';
import styles from './form.module.css'
import Title from "./../../../../ui/Title/Title"
import Questionnaire1 from './Questionnaire1/Questionnaire1';
import Questionnaire2 from './Questionnaire2/Questionnaire2';
import Questionnaire3 from './Questionnaire3/Questionnaire3';
import Questionnaire4 from './Questionnaire4/Questionnaire4';
import Button from './../../../../ui/Button/Button'
import Activity1 from '../../../activities/activity-1/Activity1';

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

const Form = () => {
    const {isEnglish} = useContext(LangContext)
    const [next, setNext] = useState(false)

    if(next){
      return <Activity1 />
    }

    return (
        <>
            <Title title="Ερωτηματολόγιο Αξιών" />
            <Paragraph text={text} />
            <SubTitle title="Αντίληψη και Σημαντικότητα Αξιών" />
            <div className={styles.formContainer} >
                {/* Questionnaire 1 */}
                <Questionnaire1 />
                {/* Questionnaire 2 */}
                <Questionnaire2 />
                {/* Questionnaire 3 */}
                <Questionnaire3 />
                {/* Questionnaire 4 */}
                <Questionnaire4 />
            </div>

            <Button onClick={() => setNext(true)} text="ΕΠΟΜΕΝΟ" color="rgb(105, 160, 130)" />

        </>
    )
}

export default Form


// const FormTest = () => {
//     const [answers, setAnswers] = useState({});
//     const [showQuestionnaire, setShowQuestionnaire] = useState(false)


//     const handleAnswerChange = (event) => {
//         const { name, value } = event.target;
//         setAnswers((prevState) => ({ ...prevState, [name]: value }));
//     };

//     const handleSubmit = (event) => {
//         event.preventDefault();
//         console.log(answers);
//     };

//     const questionnaire = questions.map((question) => (
//         <div key={question.id}>
//         <h3>{question.question}</h3>
//         {question.options.map((option) => (
//             <label key={option.id}>
//             <input
//                 type="radio"
//                 name={`question_${question.id}`}
//                 value={option.label}
//                 checked={answers[`question_${question.id}`] === option.label}
//                 onChange={handleAnswerChange}
//             />
//             {option.label}
//             </label>
//         ))}
//         </div>
//     ))

//     return (
//         <>
//             <Paragraph text={text} />
//             <SubTitle title="Αντίληψη και Σημαντικότητα Αξιών" />
//             <form className={styles.formContainer} onSubmit={handleSubmit}>
//                 <div className={styles.titleContainer}>
//                     <h4>Ερωτηματολόγιο 1</h4>
                    
//                     {!showQuestionnaire
//                     ?
//                         <BsFillArrowUpCircleFill onClick={() => setShowQuestionnaire(true)} className={styles.icon} />
//                     :
//                         <BsFillArrowDownCircleFill onClick={() => setShowQuestionnaire(false)} className={styles.icon} />
//                     }                    
//                 </div>
//                 {
//                     !showQuestionnaire
//                     &&
//                     <>
                    
//                     <Paragraph text={text} />
//                     {questionnaire}
//                     </>
//                 }


//                 <button className={styles.submitBtn} type="submit">Submit</button>
//             </form>
//         </>
//     )
// }