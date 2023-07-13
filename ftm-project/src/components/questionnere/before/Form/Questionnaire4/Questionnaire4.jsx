import Paragraph from '../../../../../ui/Paragraph/Paragraph'
import { useState } from 'react';
import styles from './questionnaire.module.css'
import {BsFillArrowUpCircleFill, BsFillArrowDownCircleFill} from 'react-icons/bs'

const questions = [
    {
      id: 1,
      question: "Όταν οι δουλειές είναι λίγες, οι άνδρες θα πρέπει να έχουν προτεραιότητα σε μία δουλειά παρά οι γυναίκες.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 2,
      question: "Όταν οι θέσεις σε ένα σχολείο είναι περιορισμένες προτεραιότητα θα έπρεπε να δίνεται σε ντόπιους μαθητές παρά σε μετανάστες.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 3,
      question: "Εάν μια γυναίκα κερδίζει περισσότερα από το σύζυγό της, είναι σχεδόν βέβαιο ότι θα προκαλέσει προβλήματα.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 4,
      question: "Αν κάποιος στο σχολείο είναι διαφορετικός καλύτερα να κρατάμε τις αποστάσεις μας και να μην έχουμε επαφές.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 5,
      question: "Το να κάνεις παιδιά είναι καθήκον απέναντι στην κοινωνία.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 6,
      question: "Τα ενήλικα παιδιά έχουν καθήκον να φροντίζουν τους γονείς τους.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 7,
      question: "Όσοι δεν εργάζονται γίνονται τεμπέληδες.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 8,
      question: "Η εργασία αποτελεί καθήκον απέναντι στην κοινωνία.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
    {
      id: 9,
      question: "Η εργασία πάντοτε πρέπει να προηγείται, ακόμα κι αν σημαίνει λιγότερο ελεύθερο χρόνο.",
      options: [
        { id: 1, label: "Συμφωνώ Πολύ" },
        { id: 2, label: "Συμφωνώ" },
        { id: 3, label: "Διαφωνώ" },
        { id: 4, label: "Διαφωνώ Πολύ" },
      ],
    },
]

const Questionnaire4 = () => {
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
                <h4>Ερωτηματολόγιο 4</h4>
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


export default Questionnaire4