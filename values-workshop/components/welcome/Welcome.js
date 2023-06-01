import {useState, createContext, useContext} from 'react'
import React, { useRef } from 'react'
import styles from './welcome.module.css'
import { BsArrowRight } from 'react-icons/bs'
import Instructions from '../instructions/Instructions';
import Button from '@component/ui/button/Button';
import Congratulations from '../congratulations/Congratulations';
import { LangContext } from "../layout/Layout";

// Create Context
export const IdContext = createContext();

console.log(IdContext);

async function savevisitor(data) { 
  try {
    const response = await fetch('https://activities_backend.vast-project.eu/api/savevisitor', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
       console.log(response)
      throw new Error(`Error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  }
  catch (err) {
    console.log(err);
  }
}

function Welcome() {
    const {isEnglish, setIsEnglish} = useContext(LangContext)
    const [start, setStart] = useState(false);
    const [cong, setCong] = useState(false);
    const [id, setId] = useState('');
    var jsondata = {
      name: "Values Workshop Visitor",
      userid: null,
      created_by: 3,
      age: null,
      gender: null,
      education: null,
      nationality: null,
      motherLanguage: null,
      activity: null,
      group: null
    };

    const useridRef = useRef(null);

    const handleSubmit = event => {
      jsondata={
        name: "Values Workshop Visitor",
        userid: useridRef.current.value,
        created_by: 3,
        age: null,
        gender: null,
        education: null,
        motherLanguage: 3,
        activity: vstepid,
        group: vgroupname,
        nationality: 3
      }
      console.log("JSON DATA")
      console.log(jsondata)
      savevisitor(jsondata)
      event.target.reset()
    }

    if(start){
      jsondata={
        name: "Values Workshop Visitor",
        userid: useridRef.current.value,
        created_by: 3,
        age: null,
        gender: null,
        education: null,
        motherLanguage: 3,
        activity: 2,
        group: 2,
        nationality: 3
      };
      console.log("JSON DATA");
      console.log(jsondata);
      savevisitor(jsondata);
      return <Instructions />
    }

  return (
    <IdContext.Provider value="vjassa" >
        <div className={styles.container}>
        <h1 className={styles.primaryHeadline}>VAST Values Workshop</h1>
        {/* <h3 className={styles.secondaryHeadline}>???ast???? ????? VAST</h3> */}
        <p className={styles.text}>{
        isEnglish 
        ?
        "The VAST values ??workshop includes two actions. In the first activity you are asked to indicate the values ??that you think are conveyed by a passage from the play by the writer Karel Capek (1890-1938) Rossum's Universal Robots (1920). Instructions on how to locate the values ??are given on the next page. Then, during the second activity you are asked to rank the values ??you identified in the text according to their importance in your life. Have fun!"
        :
        '?? e??ast???? a???? VAST pe???aµß??e? d?? d??se??. St?? p??t? d??s? ?a?e?ste ?a ?p?de??ete t?? a??e? p?? µetaf??e? s?µf??a µe t? ???µ? sa? ??a ap?spasµa ap? t? ?eat???? ???? t?? s????af?a Karel Capek (1890-1938) Rossums Universal Robots (1920). ?? ?d???e? ??a t?? t??p? e?t?p?sµ?? t?? a???? d????ta? st?? ep?µe?? se??da. St? s????e?a, ?at? t? d????e?a t?? de?te??? d??s?? ?a?e?ste ?a ?e?a???sete t?? a??e? p?? e?t?p?sate st? ?e?µe?? µe ???µ??a t? s?µa?t???t?t? t??? st? ??? sa?. ?a?? d?as??das?! '}
        </p>
        <form>  
          <div className={styles.inputContainer}>
              <label htmlFor="userid">{isEnglish ? 'Enter User ID' : '??sa???? ??d????'}</label>
              <input ref={useridRef} name="userid" value={id} onChange={(e) => setId(e.target.value)} className={styles.input} type="text" />
          </div>
          <Button type="submit" onClick={() => setStart(!start)} color="#5C47C2" title={isEnglish ? 'START' : "??????"} />
        </form>
      </div>
      {cong ? <Congratulations /> : ''}
    </IdContext.Provider>
  )
}

export default Welcome
