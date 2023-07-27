import React, {useState} from "react"
import styles from "./mappa.module.css"
import Image from "next/image";
import centerBubbleIta from "../../public/center-bubble-ita.svg";
import centerBubbleEng from "../../public/center-bubble-eng.svg";
import logo from "../../public/logo.png"
import {motion} from "framer-motion"
import Congratulations from "../Congratulations/Congratulations"
import italy from "../../public/italy-flag.png"
import uk from "../../public/eng-flag.png"
import {saveVisitor, saveMindmap} from "./BackendCommunication"
import {getCenterSubject} from "./Subject";

/**
 * The Mindmap component, showing a subject in the center and three predicates that describe it with 3 objects each.
 */
function Mappa({isItalian, setIsItalian, routerQuery, visitorData}) {
    const [submitForm, setSubmitForm] = useState(false);
    const [formData, setFormData] = useState({
        consequence1: "",
        consequence2: "",
        consequence3: "",
        equivalent1: "",
        equivalent2: "",
        equivalent3: "",
        opposite1: "",
        opposite2: "",
        opposite3: "",
    });

    let messageText = isItalian ? "Si prega di compilare questo campo" : "Please fill out this field";

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Save visitor data
        saveVisitor(visitorData).then(() => {
            // Create mindmap data: an object with the subject, and the objects for each predicate
            const data = {
                product: "Mindmap",
                subject: getCenterSubject(isItalian),
                predicates: {
                    consequence: [formData.consequence1, formData.consequence2, formData.consequence3],
                    equivalent: [formData.equivalent1, formData.equivalent2, formData.equivalent3],
                    opposite: [formData.opposite1, formData.opposite2, formData.opposite3],
                },
                language: isItalian ? "it" : "en",
                activity_step: routerQuery["activitystepid"],
                creator_username: routerQuery["username"],
                visitor_name: visitorData.name,
            };

            // Save mindmap
            saveMindmap(data).then(() => {
                setSubmitForm(true);
            });
        });
    };

    // Set Language
    const handleSetItalian = () => {
        setIsItalian(true);
    }
    const handleSetEnglish = () => {
        setIsItalian(false);
    }

    if (submitForm) {
        return (
            <Congratulations isItalian={isItalian}/>
        )
    }

    return (
        <motion.section className={styles.mindmapContainer} transition={{duration: 1}}
                        initial={{opacity: 0, scale: 0.5}} animate={{opacity: 1, scale: 1}}>
            <div className={styles.headlineContainer}>
                <h1>{isItalian ? "Mappa Mentale" : "Mindmap"}</h1>
                <h2>{isItalian ? "LA MENTE CHE RIESCE AD ALLAGARSI NON ORNA MAIN ALLA DIMENSIONE PRECEDENTE" : "The mind that succeeds in expanding never returns to its previous dimension"}</h2>
                <h4 className={styles.tertiaryHeadline}>ALBERT EINSTEIN</h4>
            </div>
            <form className={styles.formContainer} onSubmit={handleSubmit}>
                <Image className={styles.centerBubble} src={isItalian ? centerBubbleIta : centerBubbleEng} alt="mindmap"
                       width={350} height={212}/>
                <SectionContainer sectionName={isItalian ? "consequenza" : "consequences"} setFormData={setFormData}>
                    <FieldInput formData={formData} setFormData={setFormData} name="consequence1"
                                styleClass="consequenza" label={isItalian ? "consequenza" : "Consequence"}
                                messageText={messageText}/>
                    <FieldInput formData={formData} setFormData={setFormData} name="consequence2"
                                styleClass="consequenza" label={isItalian ? "consequenza" : "Consequence"}
                                messageText={messageText}/>
                    <FieldInput formData={formData} setFormData={setFormData} name="consequence3"
                                styleClass="consequenza" label={isItalian ? "consequenza" : "Consequence"}
                                messageText={messageText}/>
                </SectionContainer>
                <SectionContainer sectionName={isItalian ? "equivalenza" : "equivalents"} setFormData={setFormData}>
                    <FieldInput formData={formData} setFormData={setFormData} name="equivalent1"
                                styleClass="equivalenza" label={isItalian ? "equivalenza" : "equivalent"}
                                messageText={messageText}/>
                    <FieldInput formData={formData} setFormData={setFormData} name="equivalent2"
                                styleClass="equivalenza" label={isItalian ? "equivalenza" : "equivalent"}
                                messageText={messageText}/>
                    <FieldInput formData={formData} setFormData={setFormData} name="equivalent3"
                                styleClass="equivalenza" label={isItalian ? "equivalenza" : "equivalent"}
                                messageText={messageText}/>
                </SectionContainer>

                <SectionContainer sectionName={isItalian ? "opposto" : "opposites"} setFormData={setFormData}>
                    <FieldInput formData={formData} setFormData={setFormData} name="opposite1" styleClass="opposto"
                                label={isItalian ? "opposto" : "opposite"} messageText={messageText}/>
                    <FieldInput formData={formData} setFormData={setFormData} name="opposite2" styleClass="opposto"
                                label={isItalian ? "opposto" : "opposite"} messageText={messageText}/>
                    <FieldInput formData={formData} setFormData={setFormData} name="opposite3" styleClass="opposto"
                                label={isItalian ? "opposto" : "opposite"} messageText={messageText}/>
                </SectionContainer>

                <button className={styles.btnSubmit}
                        type="submit">{isItalian ? "creare una mappa mentale" : "create mindmap"}</button>

            </form>

            <div className={styles.flagContainer}>
                <button className={styles.flagBtn} onClick={handleSetItalian}>
                    <Image src={italy} alt="italian" width={37} height={32}/>
                </button>
                <button className={styles.flagBtn} onClick={handleSetEnglish}>
                    <Image src={uk} alt="English" width={37} height={32}/>
                </button>
            </div>
            <div className={styles.logoContainer}>
                <Image alt="Logo Vast" className={styles.logo} src={logo} width={188} height={64}></Image>
            </div>
        </motion.section>
    );
}

const SectionContainer = ({sectionName, children, setFormData}) => {
    return (
        <fieldset className={styles.sectionContainer}>
            <legend className={styles.sectionContainerHeadline}>{sectionName}</legend>
            {children}
        </fieldset>
    );
};

const FieldInput = ({name, label, styleClass, type = "text", formData, setFormData, messageText, ...rest}) => {
    const [value, setValue] = useState("");

    const handleChange = (e) => {
        setValue(e.target.value);
        setFormData((prevFormData) => ({
            ...prevFormData,
            [name]: e.target.value,
        }));
        console.log(formData);
    };

    return (
        <div className={styles.inputContainer}>
            <input className={styles[styleClass]} autoComplete="off" id={name} placeholder={label} name={name}
                   type={type} value={value} onChange={handleChange}  {...rest}
                   onInvalid={e => e.target.setCustomValidity(messageText)}
                   onInput={e => e.target.setCustomValidity('')} required/>
        </div>
    );
};

export default Mappa
