import React, { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/router'
import styles from './form.module.css'
import Image from 'next/image'
import logo from '../../public/logo.png'
import italy from '../../public/italy-flag.png'
import uk from '../../public/eng-flag.png'
import {useForm} from 'react-hook-form'
import Mindmap from '../Mindmap/Mindmap'
import Loading from '../Loading/Loading'
import {motion} from 'framer-motion'
import Mappa from '../Mindmap/Mappa'
import { BsHourglass } from 'react-icons/bs'

async function savevisitor(data) { 
    try {
      const response = await fetch('https://activities-backend.vast-project.eu/rest/visitors/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' }
      });
  
      if (!response.ok) {
         console.log(response)
        throw new Error(`Error! status: ${response.status}`);
      }
  
      const result = await response.json();
      var id = result['id']
      return id;
    }
    catch (err) {
      console.log(err);
    }
  }

function Form() {
  const [isValid, setIsValid] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isItalian, setIsItalian] = useState(true);

  const [visitorData, setVisitorData] = useState({
    name: '',
    age: '',
    gender: '',
    date_of_visit: '',
    nationality: '',
    mother_language: '',
    activity: '',
    visitor_group: '',
    school: '',
  });

  // const handleSubmit = (event) => {
  //   event.preventDefault();
  
  //   const apiUrl = 'https://activities-backend.vast-project.eu/rest/visitors/';
  
  //   const requestData = {
  //     name: visitorData.name,
  //     age: visitorData.age,
  //     gender: visitorData.gender,
  //     date_of_visit: visitorData.date_of_visit,
  //     nationality: visitorData.nationality,
  //     mother_language: visitorData.mother_language,
  //     activity: visitorData.activity,
  //     visitor_group: visitorData.visitor_group,
  //     school: visitorData.school
  //   };
  
  const handleSubmit = (event) => {
    event.preventDefault();

    // Define the endpoint URL
    const apiUrl = 'https://activities_backend.vast-project.eu/rest/visitors/';

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
    const { name, value } = event.target;
    setVisitorData(prevData => ({
      ...prevData,
      [name]: value,
    }));
    // console.log('Updated visitor data:', visitorData);
  };

  //const [jsondata,setJsonData] = useState({

  // Temporarily commented
  // -----------------
  // var jsondata = {
  //   name: "Maria Papa",
  //   userid: null,
  //   created_by: 2,
  //   date_of_visit: null,
  //   age: null,
  //   gender: null,
  //   education: null,
  //   nationality: null,
  //   motherLanguage: null,
  //   activity: null,
  //   group: null,
  //   school: null
  // };
  // -----------------------

  // Dynamic Media Query for sceen width
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

  // ---------------------------------
  var router = useRouter();
  var vschool = router.query["school"];
  var vmuseum = router.query["museum"];
  var vage = router.query["age"];
  var veduclevel = router.query["edulevel"];
  var veventid = router.query["eventid"];
  var vstepid = router.query["activitystepid"];
  var vactivityid = router.query["activityid"];
  var vgroupid = router.query["vgroupid"];
  const nameRef = useRef(null);
  const dateRef = useRef(null);
  const schoolRef = useRef(vschool);
  const museumRef = useRef(vmuseum);
  const educlevelRef = useRef(veduclevel);
  const ageRef = useRef(vage);
  const genderRef = useRef(null);
  // --------------------------------------------
  
  useEffect(() => {
    handleWindowResize();
    window.addEventListener("resize", () => setWidth(window.innerWidth));

    return window.removeEventListener("resize", () => setWidth(window.innerWidth))
  }, [width]);


  // ----------------------------------------
  // const handleSubmit = event => {
  //   if (vgroupid==undefined || vgroupid==null)
  //     {vgroupid=0;}
  //   else
  //     {vgroupid = Number(vgroupid.substring(0,vgroupid.length-1));}
  //   if (vactivityid==undefined || vactivityid==null)
  //     {vactivityid=0;}
  //   else
  //     {vactivityid = Number(vactivityid);}
  //   jsondata={
  //     name: nameRef.current.value,
  //     created_by: 2,
  //     age: ageRef.current.value,
  //     date_of_visit: dateRef.current.value,
  //     gender: genderRef.current.value,
  //     education: educlevelRef.current.value,
  //     motherLanguage: 2,
  //     activity: vactivityid,
  //     group: vgroupid,
  //     school: schoolRef.current.value,
  //     nationality: 2
  //   }
  //   console.log("JSON DATA")
  //   console.log(JSON.stringify(jsondata))
  //   var res = savevisitor(jsondata)
  //   console.log(res)
  //   setIsValid(true)
  //   event.target.reset()
  // }
  // ------------------------------------------

  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 2000);
  }, []);

  if(isLoading){
    return(
      <Loading isLoading={isLoading} />
    )
  }

  if(!isValid){
    return (
      
      <motion.div transition={{ duration: 1 }} initial={{ opacity: 0 }} animate={{ opacity: 1}} className={styles.container}>

        <h1 className={styles.primary}>{isItalian ? 'Benvenuti al' : 'Welcome to' } <span className={styles.bold}>Museo Galileo</span></h1>
        <h2 className={styles.secondary}>{isItalian ? 'Goditi la tua visita al nostro museo' : 'Enjoy your visit to our museum'}</h2>
        <div className={styles.boldline}></div>

        {/* Form */}
        <form className={styles.form} onSubmit={handleSubmit} >  

          {/* Name */}
          <div className={styles.inputContainer}>
            <label>{isItalian ? "Il nome del visitatore" : "Visitor's Name"}</label>
            <input ref={nameRef} required id="inputname" type="text" label={isItalian ? "Il nome del visitatore" : "Visitor's Name"} name="name" value={visitorData.name} onChange={handleChange} />
          </div>

          {/* Age */}
          <div className={styles.ageContainer}>
            <label>{isItalian ? "Età" : "Age"}</label>
            <select  name="age" ref={ageRef} defaultValue={vage} value={visitorData.age} onChange={handleChange} required>
              <option >{isItalian ? "Selezionare  Età..." : "Select Age..."} </option>
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
            <select value={visitorData.gender} name="gender" onChange={handleChange} required >
              <option value="">{isItalian ? "Selezionare  Genere..." : "Select Gender..."}</option>
              <option value="Male">{isItalian ? "Maschio" : "Male"}</option>
              <option value="Female">{isItalian ? "Maschia" : "Female"}</option>
            </select>
          </div>

          {/* Date */}
          <div className={styles.inputContainer}>
            <label>{isItalian ? "Data/Tempo del visitatore" : "Date/Time of Visit"}</label>
            <input ref={dateRef} required id="inputtime" type="datetime-local" label={isItalian ? "Data/Tempo del visitatore" : "Date/Time of Visit"} name="date_of_visit" value={visitorData.date_of_visit} onChange={handleChange} />
          </div>

          {/* Nationality */}
          <div className={styles.inputContainer}>
            <label>{isItalian ? "Nazionalità" : "Nationality"}</label>
            <input required name="nationality" value={visitorData.nationality} onChange={handleChange} />
          </div>

          {/* Language */}
          <div className={styles.inputContainer}>
            <label>{isItalian ? "Lingua" : "Language"}</label>
            <input required type="text" name="mother_language" value={visitorData.mother_language} onChange={handleChange} />
          </div>

          {/* Activity */}
          <div className={styles.inputContainer}>
            <label>{isItalian ? "Attività" : "Activity"}</label>
            <input required type="text" name="activity" value={visitorData.activity} onChange={handleChange} /> 
          </div>
          {/* Visitor Group */}
          <div className={styles.inputContainer}>
            <label>{isItalian ? "Gruppo di visitatori" : "Visitor Group"}</label>
            <input required type="text" name="visitor_group" value={visitorData.visitor_group} onChange={handleChange} /> 
          </div>

          {/* School */}
          <div className={styles.inputContainer}>
            <label>{isItalian ? "Scuola" : "School"}</label>
            <input required type="text" name="school" value={visitorData.school} onChange={handleChange} /> 
          </div>

          <button className={styles.submitBtn} type="submit">{isItalian ? "Benvenuto" : "Welcome"}</button>
        </form>
  
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
    )
  }

  return (
    width > breakpoint ? <Mappa isItalian={isItalian} setIsItalian={setIsItalian} /> : <Mindmap isItalian={isItalian} setIsItalian={setIsItalian} />
  )
}

export default Form
