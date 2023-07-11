import React, { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/router'
import mindmap from '../../public/mindmap.png'
import mappa from '../../public/mappa-mentale.png'
import logo from '../../public/logo.png'
import Image from 'next/image'
import styles from './mindmap.module.css'
import {motion} from 'framer-motion'
import Congratulations from '../Congratulations/Congratulations'
import {v4} from 'uuid';
import {FaTrash} from 'react-icons/fa';
import {BsPlus} from 'react-icons/bs';

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

function Mindmap({isItalian,setIsItalian}) {
  const [submitForm, setSubmitForm] = useState(false);
  const [textInputValue, setTextInputValue] = useState("");
  const [createdButtons, setCreatedButtons] = useState([]);
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

  const inputData = [
    { id: 1, category:"opposto", text: "Opposites", input: isItalian ? "OPPOSTO" : "OPPOSITE"},
    { id: 2, category:"conseguenza", text: "sequences", input: isItalian ? "CONSEGUENZA" : "CONSEQUENCE"},
    { id: 3, category:"equivalenza", text: "equivalents", input: isItalian ? "EQUIVALENZA" : "equivalent"},
  ];
  const [nodes, setNodes] = useState(inputData);

  // Set Language
  const handleSetItalian = () => {
    setIsItalian(true);
  }
  const handleSetEnglish = () => {
    setIsItalian(false);
  }

  const newValue = isItalian ? "Nuovo Valore" : "New Value";

  // Functions

  const addNode = (value) => {
    const newId = v4();
    const newNode = { id: newId, category:value, text: "New Value", input: newValue };
    setNodes([...nodes, newNode]);
  };
  const addNewNode = (value) => {
    const newId = v4();
    const newNode = { id: newId, category:value, text: "New Value", input: newValue };
    setNodes([...nodes, newNode]);
  };

  const handleSubmit = (e) =>{

    e.preventDefault();
    //------------------------
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
    //---------------------------------
    
    // setSubmitForm(true);
    console.log(nodes);
    e.target.reset()

  }

  const handleDeleteNode = (nodeId) => {
    setNodes(nodes.filter((node) => node.id !== nodeId));
  };

  const handleInputChange = (e, nodeId) => {
    const newNodes = nodes.map((node) => {
      if (node.id === nodeId) {
        return { ...node, input: e.target.value };
      }
      return node;
    });
    setNodes(newNodes);
  };

  if(submitForm){
    return (
      <Congratulations isItalian={isItalian} />
    )
  }

  // Functions for Creating new Relations
  const handleTextInputChange = (event) => {
    setTextInputValue(event.target.value);
  };

  const handleButtonClick = () => {
    const button = <button className={styles.addBtn}>{textInputValue}<BsPlus className={styles.plusIcon} /></button>;
    setCreatedButtons([...createdButtons, button]);
    setTextInputValue("");
  };

  return (
      <motion.div className={styles.container} transition={{ duration: 1 }} initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }}>
        <p className={styles.curvyTextHeadline}>
        {isItalian ? "Mappa Mentale" : "Mindmap"}
        </p>
        <p className={styles.curvyText}>
        {isItalian ? "LA MENTE CHE RIESCE AD ALLAGARSI NON ORNA MAIN ALLA DIMENSIONE PRECEDENTE" : "The mind that succeeds in expanding never returns to its previous dimension"}
        </p>
        <p className={styles.curvyTextSmall}>ALBERT EINSTEIN</p>

        <form className={styles.formContainer} onSubmit={handleSubmit}>
          
            {nodes.map((node) => (
              <div className={styles.mindmapInput} key={node.id} >
                <input
                  className={
                    node.category === "opposto" ? styles.mindmapInputOpposite 
                    : node.category === "conseguenza" ? styles.mindmapInputSequence 
                    : node.category === "equivalenza" ? styles.mindmapInputEquivalent 
                    : styles.mindmapInputNewValue}
                  type="text"
                  placeholder={newValue}
                  onChange={(e) => handleInputChange(e, node.id)}
                  onInvalid={e => e.target.setCustomValidity(messageText)}
                  onInput={e => e.target.setCustomValidity('')}
                  required
                />
                <button className={styles.removeBtn} onClick={() => handleDeleteNode(node.id)}>
                  <FaTrash />
                </button>
              </div>
            ))}
        </form>

        <div className={styles.btnContainer}>
          <button className={styles.addBtnOpposite} onClick={() => addNode("opposto")} >
          {isItalian ? "OPPOSTO" : "OPPOSITE"}
            <BsPlus className={styles.plusIcon} />
          </button>
          <button className={styles.addBtnSequence} onClick={() => addNode("conseguenza")}>
          {isItalian ? "CONSEGUENZA" : "CONSEQUENCE"}
            <BsPlus className={styles.plusIcon} />
          </button>
          <button className={styles.addBtnEquivalent} onClick={() => addNode("equivalenza")}>
          {isItalian ? "EQUIVALENZA" : "EQUIVALENT"}
            <BsPlus className={styles.plusIcon} />
          </button>
          {createdButtons.map((btn,index) => {
              return <button className={styles.btnCustom} onClick={() => addNewNode("")} key={index}>{btn}</button>
            })}
          
        </div>

        <div className={styles.textAndBtnContainer}>
          <p className={styles.textInsertedValues}>{isItalian ? 'Inserisci le tue Relazioni' : 'Insert your own relations'}</p>
          <input className={styles.textInput} type="text" value={textInputValue} onChange={handleTextInputChange} />
          <button className={styles.createBtn} onClick={handleButtonClick}>{isItalian ? 'Crea un pulsante' : 'Create Button'}</button>
          {/* <div className={styles.createdBtnsContainer}>
            {createdButtons.map((btn,index) => {
              return <div onClick={() => addNewNode("")} key={index}>{btn}</div>
            })}
          </div> */}
        </div>

        <button className={styles.btnSubmit} onClick={() => setSubmitForm(true)}>
            {isItalian ? "creare una mappa mentale" : "create mindmap"}
          </button>

        <Image alt="Logo Vast" className={styles.logo} src={logo} width={188} height={64}></Image>

        <div className={styles.flagContainer}>
          <button className={styles.flagBtn} onClick={handleSetItalian}>
            <Image src={italy} alt="italian" width={37} height={32} />
          </button>
          <button className={styles.flagBtn} onClick={handleSetEnglish}>
            <Image src={uk} alt="English" width={37} height={32} />
          </button>
        </div>
      </motion.div>
    );
}

export default Mindmap
