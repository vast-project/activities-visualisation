import React, { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/router'
import styles from './mappa.module.css'
import Image from 'next/image';
import centerBubbleIta from '../../public/center-bubble-ita.svg';
import centerBubbleEng from '../../public/center-bubble-eng.svg';
import logo from '../../public/logo.png'
import {motion} from 'framer-motion'
import Congratulations from '../Congratulations/Congratulations'

import italy from '../../public/ita-flag.png'
import uk from '../../public/uk-flag.png'

async function saveproduct(data) { 
  try {
    const response = await fetch('https://activities_backend.vast-project.eu/api/saveproduct', {
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

function Mappa({isItalian, setIsItalian}) {
    const [submitForm, setSubmitForm] = useState(false);
    const [formData, setFormData] = useState([]);
    let messageText = isItalian ? 'Si prega di compilare questo campo' : 'Please Fill Out This Field';
    var router = useRouter();
    var vstepid = router.query["activitystepid"];
    var jsondata = {
      name: null,
      name_local: null,
      created_by: 2,
      description: null,
      description_local: null,
      activity_step:vstepid,
      visitor: null,
      data: null
    };

    const handleSubmit = (e) => {
      jsondata={
        name: "IMSS Web App Product",
        name_local: null,
        created_by: 2,
        description: null,
        description_local: null,
        activity_step:vstepid,
        visitor: 2,
        data: JSON.stringify(formData)
      }
      console.log("JSON DATA")
      console.log(JSON.stringify(jsondata))
      saveproduct(jsondata)
      
      e.preventDefault();   
      setSubmitForm(true)
      console.log(formData);
      e.target.reset()

    }

      // Set Language
  const handleSetItalian = () => {
    setIsItalian(true);
  }
  const handleSetEnglish = () => {
    setIsItalian(false);
  }

    if(submitForm){
      return (
        <Congratulations isItalian={isItalian} />
      )
    }
    
    return (
      <motion.section className={styles.mindmapContainer} transition={{ duration: 1 }} initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }} >
        <div className={styles.headlineContainer}>
            <h1>{isItalian ? "Mappa Mentale" : "Mindmap"}</h1>
            <h2>{isItalian ? "LA MENTE CHE RIESCE AD ALLAGARSI NON ORNA MAIN ALLA DIMENSIONE PRECEDENTE" : "The mind that succeeds in expanding never returns to its previous dimension"}</h2>
            <h4 className={styles.tertiaryHeadline}>ALBERT EINSTEIN</h4>
        </div>
        <form className={styles.formContainer} onSubmit={handleSubmit}>
          <Image className={styles.centerBubble} src={isItalian ? centerBubbleIta : centerBubbleEng} alt="mindmap" width={350} height={212} />
          <SectionContainer sectionName={isItalian ? "consequenza" : "consequences"} setFormData={setFormData}>
            <FieldInput setFormData={setFormData} name="consequence1" styleClass="consequenza" label={isItalian ? "consequenza" : "Consequence"} messageText={messageText} />
            <FieldInput setFormData={setFormData} name="consequence2" styleClass="consequenza" label={isItalian ? "consequenza" : "Consequence"} messageText={messageText} />
            <FieldInput setFormData={setFormData} name="consequence3" styleClass="consequenza" label={isItalian ? "consequenza" : "Consequence"} messageText={messageText} />
        </SectionContainer>
        <SectionContainer sectionName={isItalian ? "equivalenza" : "equivalents"} setFormData={setFormData}>
            <FieldInput setFormData={setFormData} name="equivalent1" styleClass="equivalenza" label={isItalian ? "equivalenza" : "equivalent"} messageText={messageText} />
            <FieldInput setFormData={setFormData} name="equivalent2" styleClass="equivalenza" label={isItalian ? "equivalenza" : "equivalent"} messageText={messageText} />
            <FieldInput setFormData={setFormData} name="equivalent3" styleClass="equivalenza" label={isItalian ? "equivalenza" : "equivalent"} messageText={messageText} />
        </SectionContainer>
        
        <SectionContainer sectionName={isItalian ? "opposto" : "opposites"} setFormData={setFormData}>
            <FieldInput setFormData={setFormData} name="opposite1" styleClass="opposto" label={isItalian ? "opposto" : "opposite"} messageText={messageText} />
            <FieldInput setFormData={setFormData} name="opposite2" styleClass="opposto" label={isItalian ? "opposto" : "opposite"} messageText={messageText} />
            <FieldInput setFormData={setFormData} name="opposite3" styleClass="opposto" label={isItalian ? "opposto" : "opposite"} messageText={messageText} />
        </SectionContainer>
        
        <button className={styles.btnSubmit} type="submit">{isItalian ? "creare una mappa mentale" : "create mindmap"}</button>
        
        </form>

        <div className={styles.flagContainer}>
          <button className={styles.flagBtn} onClick={handleSetItalian}>
            <Image src={italy} alt="italian" width={37} height={32} />
          </button>
          <button className={styles.flagBtn} onClick={handleSetEnglish}>
            <Image src={uk} alt="English" width={37} height={32} />
          </button>
        </div>
        <div className={styles.logoContainer}>
          <Image alt="Logo Vast" className={styles.logo} src={logo} width={188} height={64}></Image>
        </div>

        
      </motion.section>
    );
}

const SectionContainer = ({ sectionName, children, setFormData }) => {
    return (
      <fieldset className={styles.sectionContainer}>
        <legend className={styles.sectionContainerHeadline}>{sectionName}</legend>
        {children}
      </fieldset>
    );
  };
  
  const FieldInput = ({ name, label, styleClass, type = "text", setFormData, messageText, ...rest }) => {
    const [value, setValue] = useState("");
  
    const handleChange = (e) => {
      setValue(e.target.value);
      setFormData((prevFormData) => ({
        ...prevFormData,
        [name]: e.target.value,
      }));
    };
  
    return (
      <div className={styles.inputContainer}>
        <input className={styles[styleClass]} autoComplete='off' id={name} placeholder={label} name={name} type={type} value={value} onChange={handleChange}  {...rest} onInvalid={e => e.target.setCustomValidity(messageText)} onInput={e => e.target.setCustomValidity('')} required />
      </div>
    );
  };

export default Mappa