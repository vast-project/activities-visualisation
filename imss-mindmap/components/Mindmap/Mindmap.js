import React, {useState} from "react"
import logo from "../../public/logo.png"
import Image from "next/image"
import styles from "./mindmap.module.css"
import {motion} from "framer-motion"
import Congratulations from "../Congratulations/Congratulations"
import {v4} from "uuid";
import {FaTrash} from "react-icons/fa";
import {BsPlus} from "react-icons/bs";

import italy from "../../public/italy-flag.png"
import uk from "../../public/eng-flag.png"
import {saveMindmap, saveVisitor} from "./BackendCommunication";
import {getCenterSubject} from "./Subject";

/**
 * Mobile version of the Mindmap component. Supports adding more than 3 concepts per predicate, as well as adding new
 * predicates.
 */
function Mindmap({isItalian, setIsItalian, routerQuery, visitorData}) {
    const [submitForm, setSubmitForm] = useState(false);
    const [newRelationInputValue, setNewRelationInputValue] = useState("");
    const [createdRelations, setCreatedRelations] = useState([]);
    let messageText = isItalian ? "Si prega di compilare questo campo" : "Please fill out this field";

    const initialData = [
        {id: v4(), category: "opposite", input: ""},
        {id: v4(), category: "consequence", input: ""},
        {id: v4(), category: "equivalent", input: ""},
    ];
    const [nodes, setNodes] = useState(initialData);
    const newValue = isItalian ? "Nuovo Valore" : "New Value";

    // Set Language
    const handleSetItalian = () => {
        setIsItalian(true);
    }
    const handleSetEnglish = () => {
        setIsItalian(false);
    }

    const addNode = (value) => {
        const newNode = {id: v4(), category: value, input: newValue};
        setNodes([...nodes, newNode]);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Save visitor data
        console.log("Saving visitor");
        saveVisitor(visitorData).then(() => {
            console.log("Visitor saved, saving mindmap");

            // Gather predicates from the nodes
            let predicates = {};
            nodes.forEach((node) => {
                if (predicates[node.category] === undefined) {
                    predicates[node.category] = [];
                }
                predicates[node.category].push(node.input);
            });

            // Create mindmap data: an object with the subject, and the objects for each predicate
            const data = {
                product: "Mindmap",
                subject: getCenterSubject(isItalian),
                predicates: predicates,
                language: isItalian ? "it" : "en",
                activity_step: routerQuery["activitystepid"],
                creator_username: routerQuery["username"],
                visitor_name: visitorData.name,
            };

            // Save mindmap
            saveMindmap(data).then(() => {
                // Show congratulations
                setSubmitForm(true);
            });
        });
    }

    const handleDeleteNode = (nodeId) => {
        setNodes(nodes.filter((node) => node.id !== nodeId));
    };

    const handleInputChange = (e, nodeId) => {
        const newNodes = nodes.map((node) => {
            if (node.id === nodeId) {
                node.input = e.target.value;
            }
            return node;
        });
        setNodes(newNodes);
    };

    if (submitForm) {
        return (
            <Congratulations isItalian={isItalian}/>
        )
    }

    // Functions for Creating new Relations
    const handleNewRelationInputChange = (event) => {
        setNewRelationInputValue(event.target.value);
    };

    const handleNewRelationBtnClick = () => {
        // Add the current newRelationInputValue to the list of created relation types
        setCreatedRelations([...createdRelations, newRelationInputValue]);
        setNewRelationInputValue("");
    };

    return (
        <motion.div className={styles.container} transition={{duration: 1}} initial={{opacity: 0, scale: 0.5}}
                    animate={{opacity: 1, scale: 1}}>
            <p className={styles.curvyTextHeadline}>
                {isItalian ? "Mappa Mentale" : "Mindmap"}
            </p>
            <p className={styles.curvyText}>
                {isItalian ? "LA MENTE CHE RIESCE AD ALLAGARSI NON ORNA MAIN ALLA DIMENSIONE PRECEDENTE" : "The mind that succeeds in expanding never returns to its previous dimension"}
            </p>
            <p className={styles.curvyTextSmall}>ALBERT EINSTEIN</p>

            <form className={styles.formContainer} onSubmit={handleSubmit}>
                {nodes.map((node) => (
                    <div className={styles.mindmapInput} key={node.id}>
                        <input
                            className={
                                node.category === "opposite" ? styles.mindmapInputOpposite
                                    : node.category === "consequence" ? styles.mindmapInputSequence
                                        : node.category === "equivalent" ? styles.mindmapInputEquivalent
                                            : styles.mindmapInputNewValue}
                            type="text"
                            placeholder={newValue}
                            onChange={(e) => handleInputChange(e, node.id)}
                            onInvalid={e => e.target.setCustomValidity(messageText)}
                            onInput={e => e.target.setCustomValidity("")}
                            required
                        />
                        <button className={styles.removeBtn} onClick={() => handleDeleteNode(node.id)}>
                            <FaTrash/>
                        </button>
                    </div>
                ))}
            </form>

            <div className={styles.btnContainer}>
                <button className={styles.addBtnOpposite} onClick={() => addNode("opposite")}>
                    {isItalian ? "OPPOSTO" : "OPPOSITE"}
                    <BsPlus className={styles.plusIcon}/>
                </button>
                <button className={styles.addBtnSequence} onClick={() => addNode("consequence")}>
                    {isItalian ? "CONSEGUENZA" : "CONSEQUENCE"}
                    <BsPlus className={styles.plusIcon}/>
                </button>
                <button className={styles.addBtnEquivalent} onClick={() => addNode("equivalent")}>
                    {isItalian ? "EQUIVALENZA" : "EQUIVALENT"}
                    <BsPlus className={styles.plusIcon}/>
                </button>
                {createdRelations.map((relation, index) => {
                    return <button className={styles.addBtnCustom} onClick={() => addNode(relation)}
                                   key={index}>{relation}<BsPlus className={styles.plusIcon}/></button>
                })}

            </div>

            {/* New Relation text input & button */}
            <div className={styles.textAndBtnContainer}>
                <p className={styles.textInsertedValues}>{isItalian ? "Inserisci le tue Relazioni" : "Insert your own relations"}</p>
                <input className={styles.textInput} type="text" value={newRelationInputValue}
                       onChange={handleNewRelationInputChange}/>
                <button className={styles.createBtn} onClick={handleNewRelationBtnClick}>
                    {isItalian ? "Crea un pulsante" : "Create Button"}
                </button>
            </div>

            <button className={styles.btnSubmit} onClick={handleSubmit}>
                {isItalian ? "creare una mappa mentale" : "create mindmap"}
            </button>

            <Image alt="Logo Vast" className={styles.logo} src={logo} width={188} height={64}></Image>

            <div className={styles.flagContainer}>
                <button className={styles.flagBtn} onClick={handleSetItalian}>
                    <Image src={italy} alt="italian" width={37} height={32}/>
                </button>
                <button className={styles.flagBtn} onClick={handleSetEnglish}>
                    <Image src={uk} alt="English" width={37} height={32}/>
                </button>
            </div>
        </motion.div>
    );
}

export default Mindmap
