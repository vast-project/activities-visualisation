import React, { useEffect, useRef, useState } from 'react'
import mindmap from '../../public/mindmap.png'
import mappa from '../../public/mappa-mentale.png'
import logo from '../../public/logo.png'
import Image from 'next/image'
import styles from './mindmap.module.css'
import {motion} from 'framer-motion'
import Congratulations from '../Congratulations/Congratulations'

import {AiFillPlusCircle} from 'react-icons/ai';
import {FaTrash} from 'react-icons/fa';
import {BsPlus} from 'react-icons/bs';

function Mindmap({isItalian}) {
  const [submitForm, setSubmitForm] = useState(false);

  const [nodes, setNodes] = useState([
    { id: 1, category:"opposto", text: "Opposites", input: "OPPOSTO"},
    { id: 2, category:"conseguenza", text: "sequences", input: "CONSEGUENZA"},
    { id: 3, category:"equivalenza", text: "equivalents", input: "EQUIVALENZA"},
  ]);

  const handleSubmit = (e) =>{
    e.preventDefault();
    setSubmitForm(true);
    console.log(nodes);
  }

  const newValue = isItalian ? "Nuovo Valore" : "New Value";

  const addNode = (value) => {
    const newId = nodes.length + 1;
    const newNode = { id: newId, category:value, text: "New Value", input: newValue };
    setNodes([...nodes, newNode]);
  };

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
          <button className={styles.btnSubmit} type="submit">{isItalian ? "creare una mappa mentale" : "create mindmap"}</button>
            {nodes.map((node) => (
              <form className={styles.mindmapInput} key={node.id} >
                <input
                  className={node.category === "opposto" ? styles.mindmapInputOpposite : node.category === "conseguenza" ? styles.mindmapInputSequence : styles.mindmapInputEquivalent}
                  type="text"
                  placeholder={node.input}
                  onChange={(e) => handleInputChange(e, node.id)}
                />
                <button className={styles.removeBtn} onClick={() => handleDeleteNode(node.id)}>
                  <FaTrash />
                </button>
              </form>
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
          </div>
        <Image alt="Logo Vast" className={styles.logo} src={logo} width={188} height={64}></Image>
      </motion.div>
    );
}

export default Mindmap