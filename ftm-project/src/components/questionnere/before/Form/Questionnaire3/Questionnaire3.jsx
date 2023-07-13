import Paragraph from '../../../../../ui/Paragraph/Paragraph'
import { useState } from 'react';
import styles from './questionnaire.module.css'
import {BsFillArrowUpCircleFill, BsFillArrowDownCircleFill} from 'react-icons/bs'

const questions = [
    {
      id: 1,
      question: "Μία από τις κύριες επιδιώξεις μου στη ζωή είναι να κάνω τους γονείς μου υπερήφανους.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 2,
      question: "Όταν μια μητέρα εργάζεται, τα παιδιά υποφέρουν.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 3,
      question: "Η πανεπιστημιακή εκπαίδευση είναι πιο σημαντική για ένα αγόρι απ’ ότι για ένα κορίτσι.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 4,
      question: "Εάν είμαι μάρτυρας σε ένα περιστατικό παρενόχλησης ενός συμμαθητή δεν πρέπει να επέμβω με κάποιο τρόπο.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
]

const Questionnaire3 = () => {
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
                <h4>Ερωτηματολόγιο 3</h4>
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
                    {/* <Paragraph text={text} /> */}
                    {questionnaire}
                    <button className={styles.submitBtn} type="submit">Submit</button>
                </form>
            }
        </>
    )
}


export default Questionnaire3