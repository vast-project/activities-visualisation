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
import Input from '../Input/Input'
import Mappa from '../Mindmap/Mappa'
export const randomid = Math.round(Math.random()*1000000000)
export var eventid

function Form() {
  const [isValid, setIsValid] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isItalian, setIsItalian] = useState(true);
  const [width, setWidth] = useState(0);
  const breakpoint = 700;

  const handleWindowResize = () => {
    setWidth(window.innerWidth);
  }
  const handleSetItalian = () => {
    setIsItalian(true);
  }
  const handleSetEnglish = () => {
    setIsItalian(false);
  }
  
  const ref = useRef(null);
  var router = useRouter();
  var variables = router.query["variables"];
  if (typeof variables !== 'undefined') {
    var params = variables.split(",");
    var eventid = params[0].split(":")[1];
    eventid = eventid.substring(1,eventid.length-1);
    console.log(eventid);
    var datetime = params[1].split(" ");
    var date = datetime[0].split(":")[1].substring(1,datetime[0].length);
    var time = datetime[1].substring(0,datetime[1].length-4);
    var visitor = params[2].split(":")[1];
    visitor = visitor.substring(1,visitor.length-1);
    var educationlevel = params[4].split(":")[1];
    educationlevel = educationlevel.substring(1,educationlevel.length-2);
  }
  
  useEffect(() => {
    handleWindowResize();
    window.addEventListener("resize", () => setWidth(window.innerWidth));

    return window.removeEventListener("resize", () => setWidth(window.innerWidth))
  }, [width]);
  
  const {register, formState: {errors}, handleSubmit} = useForm();
  const onSubmit = (data) =>{
    console.log(data);
    setIsValid(true);
    if (eventid !== undefined) {
      var item = {
        'eventid': eventid,
        'randomid': randomid,
        'eventdatafromdb': variables,
        'userformdata': JSON.stringify(data)
      };
    }
    else
    {
      var item = {
        'randomid': randomid,
        'userformdata': JSON.stringify(data)
      };
    }
    
    fetch('/api/server/', {
      method: 'POST',
      body: JSON.stringify(item)
    })
    .then((response) => response.json())
    .catch((err) => console.log(err));
    
    console.log(item);
  }

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
  
        <form className={styles.form} onSubmit={handleSubmit(onSubmit)} >  
          <Input ref={ref} id="name" register={register} type="text" label={isItalian ? "Il nome del visitatore" : "Visitor's Name"} errors={errors} iname="name" />
          <Input id="date" register={register} type="date" label={isItalian ? "Data del visitatore" : "Date of Visit"} errors={errors} defvalue={date} iname="date" />
          <Input id="time" register={register} type="time" label={isItalian ? "Tempo del visitatore" : "Time of Visit"} errors={errors} defvalue={time} iname="time" />
          <Input id="school" register={register} type="text" label={isItalian ? "Il nome della scuola" : "School Name"} errors={errors} defvalue={visitor} iname="school" />
          <Input id="educlevel" register={register} type="text" label={isItalian ? "Livello educativo" : "Educational Level"} errors={errors} defvalue={educationlevel} iname="educlevel" /> 
          <button className={styles.submitBtn} type="submit">{isItalian ? "Benvenuto" : "Welcome"}</button>
        </form>
  
        <Image alt="Logo Vast" className={styles.logo} src={logo} width={188} height={64}></Image>

        <div className={styles.flagContainer}>
          <button className={styles.flagBtn} onClick={handleSetItalian}>
            <Image src={italy} alt="italian" width={50} height={45} />
          </button>
          <button className={styles.flagBtn} onClick={handleSetEnglish}>
            <Image src={uk} alt="English" width={50} height={45} />
          </button>
        </div>
      </motion.div>
    )

  }

  return (
    width > breakpoint ? <Mappa isItalian={isItalian} /> : <Mindmap isItalian={isItalian} />
  )
  
}

export default Form
