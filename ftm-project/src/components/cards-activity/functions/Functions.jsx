import {useState} from 'react'
import styles from './functions.module.css'
import {BsFillArrowDownCircleFill} from 'react-icons/bs'
import img1 from '../../../../public/functions/img1.png'
import img2 from '../../../../public/functions/img2.png'
import img3 from '../../../../public/functions/img3.png'
import img4 from '../../../../public/functions/img4.png'
import img5 from '../../../../public/functions/img5.png'
import img6 from '../../../../public/functions/img6.png'
import img7 from '../../../../public/functions/img7.png'
import img8 from '../../../../public/functions/img8.png'
import img9 from '../../../../public/functions/img9.png'
import img10 from '../../../../public/functions/img10.png'
import img11 from '../../../../public/functions/img11.png'
import img12 from '../../../../public/functions/img12.png'
import img13 from '../../../../public/functions/img13.png'
import img14 from '../../../../public/functions/img14.png'
import img15 from '../../../../public/functions/img15.png'
import img16 from '../../../../public/functions/img16.png'
import img17 from '../../../../public/functions/img17.png'
import img18 from '../../../../public/functions/img18.png'
import img19 from '../../../../public/functions/img19.png'
import img20 from '../../../../public/functions/img20.png'
import img21 from '../../../../public/functions/img21.png'
import img22 from '../../../../public/functions/img22.png'
import img23 from '../../../../public/functions/img23.png'
import img24 from '../../../../public/functions/img24.png'
import img25 from '../../../../public/functions/img25.png'
import img26 from '../../../../public/functions/img26.png'
import img27 from '../../../../public/functions/img27.png'
import img28 from '../../../../public/functions/img28.png'
import img29 from '../../../../public/functions/img29.png'
import img30 from '../../../../public/functions/img30.png'
import img31 from '../../../../public/functions/img31.png'

const functions = [
    {id: 1, src: img1, selected: false, name: "absence"},
    {id: 2, src: img2, selected: false, name: "ban"},
    {id: 3, src: img3, selected: false, name: "violation"},
    {id: 4, src: img4, selected: false, name: "investigation"},
    {id: 5, src: img5, selected: false, name: "assignment"},
    {id: 6, src: img6, selected: false, name: "deception"},
    {id: 7, src: img7, selected: false, name: "complicity"},
    {id: 8, src: img8, selected: false, name: "sabotage"},
    {id: 9, src: img9, selected: false, name: "mediation"},
    {id: 10, src: img10, selected: false, name: "initiation of spontaneous action"},
    {id: 11, src: img11, selected: false, name: "departure hero"},
    {id: 12, src: img12, selected: false, name: "donor's first function"},
    {id: 13, src: img13, selected: false, name: "hero's reaction"},
    {id: 14, src: img14, selected: false, name: "magical gifts"},
    {id: 15, src: img15, selected: false, name: "transport"},
    {id: 16, src: img16, selected: false, name: "fight"},
    {id: 17, src: img17, selected: false, name: "stigmatization - mark"},
    {id: 18, src: img18, selected: false, name: "victory hero"},
    {id: 19, src: img19, selected: false, name: "elimination of unhappiness"},
    {id: 20, src: img20, selected: false, name: "return"},
    {id: 21, src: img21, selected: false, name: "persecution"},
    {id: 22, src: img22, selected: false, name: "rescue"},
    {id: 23, src: img23, selected: false, name: "unrecognizable poster"},
    {id: 24, src: img24, selected: false, name: "unsubstantiated claims"},
    {id: 25, src: img25, selected: false, name: "test"},
    {id: 26, src: img26, selected: false, name: "solution"},
    {id: 27, src: img27, selected: false, name: "recognition"},
    {id: 28, src: img28, selected: false, name: "revelation"},
    {id: 29, src: img29, selected: false, name: "transformation"},
    {id: 30, src: img30, selected: false, name: "punishment"},
    {id: 31, src: img31, selected: false, name: "marriage"},
]

const Functions = ({onChange}) => {
    const [allFunctions, setAllFunctions] = useState(functions);
    const [myFunctions, setMyFunctions] = useState([]);

    // Pick a character
    const handleSelect = (func) => {
        const selectedFunction = {...func, selected: true};
        // Remove character from all characters
        const updatedAllFunctions = allFunctions.filter(f => f.id !== func.id);
        setAllFunctions(updatedAllFunctions);
        // Add character to my characters
        const updatedMyFunctions = [...myFunctions, selectedFunction];
        setMyFunctions(updatedMyFunctions);

        // Send the data to the parent
        onChange(updatedMyFunctions)
    }


    //Remove a character
    const handleRemove = (func) => {
        setAllFunctions([...allFunctions, func])
        let updatedMyFunctions = myFunctions.filter((f) => f.id !== func.id)
        setMyFunctions(updatedMyFunctions)

        // Send the data to the parent
        onChange(updatedMyFunctions)
    }


    return (
        <>
            <h2 className={styles.functionsMainTitle}>Choose Your Functions</h2>

            <h3 className={styles.functionsTitle}>Functions</h3>
            <div className={styles.functionsContainer}>
                {
                    allFunctions.map((func) => {
                        return (
                            // <div onClick={() => handleSelect(func)} key={func.id} className={styles.func}></div>
                            <figure onClick={() => handleSelect(func)} key={func.id} className={styles.func}>
                                <img className={styles.img} src={func.src} alt="Function"/>
                            </figure>
                        )
                    })
                }
            </div>

            <BsFillArrowDownCircleFill className={styles.icon}/>

            <h3 className={styles.functionsTitle}>Your Functions</h3>
            <div className={styles.functionsContainer}>
                {
                    myFunctions.map((func) => {
                        return (
                            // <div onClick={() => handleRemove(func)} key={func.id} className={styles.func}></div>
                            <figure onClick={() => handleRemove(character)} key={func.id} className={styles.func}>
                                <img className={styles.img} src={func.src} alt="Function"/>
                            </figure>

                        )
                    })
                }
            </div>
        </>
    )
}

export default Functions