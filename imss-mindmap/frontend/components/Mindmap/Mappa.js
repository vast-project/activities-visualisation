import React, { useEffect, useRef, useState } from 'react'
import styles from './mappa.module.css'
import Image from 'next/image';
import centerBubbleIta from '../../public/center-bubble-ita.svg';
import centerBubbleEng from '../../public/center-bubble-eng.svg';
import logo from '../../public/logo.png'
import {motion} from 'framer-motion'
import Congratulations from '../Congratulations/Congratulations'

function Mappa({isItalian}) {
    const [submitForm, setSubmitForm] = useState(false);
    const [formData, setFormData] = useState([]);
  
    const handleSubmit = (e) => {
      e.preventDefault();   
      setSubmitForm(true)
      console.log(formData);
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
            <FieldInput setFormData={setFormData} name="consequence1" styleClass="consequenza" label={isItalian ? "consequenza" : "Consequence"} />
            <FieldInput setFormData={setFormData} name="consequence2" styleClass="consequenza" label={isItalian ? "consequenza" : "Consequence"} />
            <FieldInput setFormData={setFormData} name="consequence3" styleClass="consequenza" label={isItalian ? "consequenza" : "Consequence"} />
        </SectionContainer>
        <SectionContainer sectionName={isItalian ? "equivalenza" : "equivalents"} setFormData={setFormData}>
            <FieldInput setFormData={setFormData} name="equivalent1" styleClass="equivalenza" label={isItalian ? "equivalenza" : "equivalent"} />
            <FieldInput setFormData={setFormData} name="equivalent2" styleClass="equivalenza" label={isItalian ? "equivalenza" : "equivalent"} />
            <FieldInput setFormData={setFormData} name="equivalent3" styleClass="equivalenza" label={isItalian ? "equivalenza" : "equivalent"} />
        </SectionContainer>
        
        <SectionContainer sectionName={isItalian ? "opposto" : "opposites"} setFormData={setFormData}>
            <FieldInput setFormData={setFormData} name="opposite1" styleClass="opposto" label={isItalian ? "opposto" : "opposite"} />
            <FieldInput setFormData={setFormData} name="opposite2" styleClass="opposto" label={isItalian ? "opposto" : "opposite"} />
            <FieldInput setFormData={setFormData} name="opposite3" styleClass="opposto" label={isItalian ? "opposto" : "opposite"} />
        </SectionContainer>
        
        <button className={styles.btnSubmit} type="submit">{isItalian ? "creare una mappa mentale" : "create mindmap"}</button>
        </form>
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
  
  const FieldInput = ({ name, label, styleClass, type = "text", setFormData, ...rest }) => {
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
        <input className={styles[styleClass]} autoComplete='off' id={name} placeholder={label} name={name} type={type} value={value} onChange={handleChange} {...rest} />
      </div>
    );
  };

export default Mappa