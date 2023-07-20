import React, {useEffect, useState} from 'react'
import {useRouter} from 'next/router'
import styles from './form.module.css'
import Image from 'next/image'
import logo from '../../public/logo.png'
import italy from '../../public/italy-flag.png'
import uk from '../../public/eng-flag.png'
import Mindmap from '../Mindmap/Mindmap'
import Loading from '../Loading/Loading'
import {motion} from 'framer-motion'
import Mappa from '../Mindmap/Mappa'

/**
 * Get current date and time in ISO format
 * @returns {string} Current date in "YYYY-MM-DDTHH:MM" format
 */
function getCurrentIsoDate() {
    // Get current date
    let currentDate = new Date();

    // Get month and day with leading zeros
    let currMonth = currentDate.getMonth() + 1;
    if (currMonth < 10) {
        currMonth = '0' + currMonth;
    }
    let currDay = currentDate.getDate();
    if (currDay < 10) {
        currDay = '0' + currDay;
    }

    // Combine into "YYYY-MM-DDTHH:MM" format
    return currentDate.getFullYear() + '-' + currMonth + '-' + currDay + 'T' + currentDate.getHours() + ':' + currentDate.getMinutes();
}

/**
 * Given the visitorData object and the router object, set the visitorData object values from the query parameters.
 * @param visitorData The visitorData object
 * @param router The router object
 */
function setVisitorDataFromQueryParams(visitorData, router) {
    // Get query parameters
    let query = router.query;

    // Set the mapping between the visitorData object and the query parameter names
    let params = [
        {dataName: 'school', queryName: 'school'},
        {dataName: 'education_level', queryName: 'edulevel'},
        {dataName: 'age', queryName: 'age'},
        {dataName: 'nationality', queryName: 'nationality'},
        {dataName: 'mother_language', queryName: 'language'},
        {dataName: 'event_id', queryName: 'eventid'},
        {dataName: 'activity', queryName: 'activityid'},
        {dataName: 'activity_step', queryName: 'activitystepid'},
        {dataName: 'visitor_group', queryName: 'vgroupid'},
        {dataName: 'creator_username', queryName: 'username'},
    ]

    // Set the visitorData object values from the query parameters
    params.forEach(param => {
        let value = query[param.queryName];
        if (value !== undefined && visitorData[param.dataName] === '') {
            visitorData[param.dataName] = value;
        }
    });
}

function Form() {
    const [isValid, setIsValid] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [isItalian, setIsItalian] = useState(true);

    const [visitorData, setVisitorData] = useState({
        name: '',
        age: '',
        gender: '',
        date_of_visit: getCurrentIsoDate(),
        nationality: '',
        mother_language: '',
        activity: '',
        activity_step: '',
        education_level: '',
        event_id: '',
        visitor_group: '',
        school: '',
        creator_username: '',
    });

    // Set visitorData from query parameters
    const router = useRouter();
    setVisitorDataFromQueryParams(visitorData, router);

    const handleSubmit = (event) => {
        event.preventDefault();

        // Define the endpoint URL
        const apiUrl = 'https://activities-backend.vast-project.eu/rest/visitors/';

        // Send the POST request
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(visitorData),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Visitor created:', data);
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => setIsValid(true));
    };

    // Handle Change Function for every input
    const handleChange = (event) => {
        const {name, value} = event.target;
        setVisitorData(prevData => ({
            ...prevData,
            [name]: value,
        }));
        console.log('Updated visitor data:', visitorData);
    };

    // Dynamic Media Query for screen width
    const [width, setWidth] = useState(0);
    const breakpoint = 700;

    const handleWindowResize = () => {
        setWidth(window.innerWidth);
    }

    // Handle Language Functions
    const handleSetItalian = () => {
        setIsItalian(true);
    }
    const handleSetEnglish = () => {
        setIsItalian(false);
    }

    useEffect(() => {
        handleWindowResize();
        window.addEventListener("resize", () => setWidth(window.innerWidth));

        return window.removeEventListener("resize", () => setWidth(window.innerWidth))
    }, [width]);

    useEffect(() => {
        setTimeout(() => {
            setIsLoading(false);
        }, 2000);
    }, []);

    if (isLoading) {
        return (
            <Loading isLoading={isLoading}/>
        )
    }

    if (!isValid) {
        return (
            <motion.div transition={{duration: 1}} initial={{opacity: 0}} animate={{opacity: 1}}
                        className={styles.container}>

                <h1 className={styles.primary}>{isItalian ? 'Benvenuti al' : 'Welcome to'} <span
                    className={styles.bold}>Museo Galileo</span></h1>
                <h2 className={styles.secondary}>{isItalian ? 'Goditi la tua visita al nostro museo' : 'Enjoy your visit to our museum'}</h2>
                <div className={styles.boldline}></div>

                {/* Form */}
                <form className={styles.form} onSubmit={handleSubmit}>

                    {/* Name */}
                    <div className={styles.inputContainer}>
                        <label>{isItalian ? "Il nome del visitatore" : "Visitor's Name"}</label>
                        <input required id="inputname" type="text"
                               label={isItalian ? "Il nome del visitatore" : "Visitor's Name"} name="name"
                               value={visitorData.name} onChange={handleChange}/>
                    </div>

                    {/* Age */}
                    <div className={styles.ageContainer}>
                        <label>{isItalian ? "Età" : "Age"}</label>
                        <select name="age" value={visitorData.age}
                                onChange={handleChange} required>
                            <option>{isItalian ? "Selezionare  Età..." : "Select Age..."} </option>
                            <option value="14-15">14-15</option>
                            <option value="15-16">15-16</option>
                            <option value="16-17">16-17</option>
                            <option value="17-18">17-18</option>
                            <option value="18-19">18-19</option>
                        </select>
                    </div>

                    {/* Gender */}
                    <div className={styles.ageContainer}>
                        <label>{isItalian ? "Il genere del visitatore" : "Visitor's Gender"}</label>
                        <select value={visitorData.gender} name="gender" onChange={handleChange} required>
                            <option value="">{isItalian ? "Selezionare  Genere..." : "Select Gender..."}</option>
                            <option value="Male">{isItalian ? "Maschio" : "Male"}</option>
                            <option value="Female">{isItalian ? "Maschia" : "Female"}</option>
                        </select>
                    </div>

                    {/* Date */}
                    <div className={styles.inputContainer}>
                        <label>{isItalian ? "Data/Tempo del visitatore" : "Date/Time of Visit"}</label>
                        <input required id="inputtime" type="datetime-local"
                               label={isItalian ? "Data/Tempo del visitatore" : "Date/Time of Visit"}
                               name="date_of_visit" value={visitorData.date_of_visit} onChange={handleChange}/>
                    </div>

                    {/* Nationality */}
                    <div className={styles.inputContainer}>
                        <label>{isItalian ? "Nazionalità" : "Nationality"}</label>
                        <input required name="nationality" value={visitorData.nationality} onChange={handleChange}/>
                    </div>

                    {/* Language */}
                    <div className={styles.inputContainer}>
                        <label>{isItalian ? "Lingua" : "Language"}</label>
                        <input required type="text" name="mother_language" value={visitorData.mother_language}
                               onChange={handleChange}/>
                    </div>

                    {/* Activity */}
                    <div className={styles.inputContainer}>
                        <label>{isItalian ? "Attività" : "Activity"}</label>
                        <input required type="text" name="activity" value={visitorData.activity}
                               onChange={handleChange}/>
                    </div>
                    {/* Visitor Group */}
                    <div className={styles.inputContainer}>
                        <label>{isItalian ? "Gruppo di visitatori" : "Visitor Group"}</label>
                        <input required type="text" name="visitor_group" value={visitorData.visitor_group}
                               onChange={handleChange}/>
                    </div>

                    {/* School */}
                    <div className={styles.inputContainer}>
                        <label>{isItalian ? "Scuola" : "School"}</label>
                        <input required type="text" name="school" value={visitorData.school} onChange={handleChange}/>
                    </div>

                    <button className={styles.submitBtn} type="submit">{isItalian ? "Benvenuto" : "Welcome"}</button>
                </form>

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
        )
    }

    return (
        width > breakpoint ? <Mappa isItalian={isItalian} setIsItalian={setIsItalian}/> :
            <Mindmap isItalian={isItalian} setIsItalian={setIsItalian}/>
    )
}

export default Form
