import {createContext, useState} from 'react'
import styles from './characters.module.css'
import {BsFillArrowDownCircleFill} from 'react-icons/bs'
import img1 from '../../../../public/characters/img1.png'
import img2 from '../../../../public/characters/img2.png'
import img3 from '../../../../public/characters/img3.png'
import img4 from '../../../../public/characters/img4.png'
import img5 from '../../../../public/characters/img5.png'
import img6 from '../../../../public/characters/img6.png'
import img7 from '../../../../public/characters/img7.png'

const characters = [
    {id: 1, src: img1, selected: false, name: "hero"},
    {id: 2, src: img2, selected: false, name: "helper"},
    {id: 3, src: img3, selected: false, name: "sender"},
    {id: 4, src: img4, selected: false, name: "princess-reward"},
    {id: 5, src: img5, selected: false, name: "adversary"},
    {id: 6, src: img6, selected: false, name: "donor"},
    {id: 7, src: img7, selected: false, name: "fake-hero"},
]

const CharactersContext = createContext()

const Characters = ({onChange}) => {
    const [allCharacters, setAllCharacters] = useState(characters)
    const [myCharacters, setMyCharacters] = useState([])

    // Pick a character
    const handleSelect = (character) => {
        const selectedCharacter = {...character, selected: true};
        // Remove character from all characters
        const updatedAllCharacters = allCharacters.filter(char => char.id !== character.id)
        setAllCharacters(updatedAllCharacters)
        // Add character to my characters
        const updatedMyCharacters = [...myCharacters, selectedCharacter]
        setMyCharacters(updatedMyCharacters)

        // Send the data to the parent
        onChange(updatedMyCharacters)
    }

    // Remove a character
    const handleRemove = (character) => {
        setAllCharacters([...allCharacters, character])
        let updatedMyCharacters = myCharacters.filter((char) => char.id !== character.id)
        setMyCharacters(updatedMyCharacters)

        // Send the data to the parent
        onChange(updatedMyCharacters)
    }

    return (
        <CharactersContext.Provider value={myCharacters}>
            <h2 className={styles.charactersMainTitle}>Choose Your Character</h2>

            <h3 className={styles.charactersTitle}>Characters</h3>
            <div className={styles.charactersContainer}>
                {
                    allCharacters.map((character, index) => {
                        return (
                            <figure onClick={() => handleSelect(character)} key={character.id}
                                    className={styles.character}>
                                <img className={styles.img} src={character.src} alt="Character"/>
                            </figure>
                        )
                    })
                }
            </div>

            <BsFillArrowDownCircleFill className={styles.icon}/>

            <h3 className={styles.charactersTitle}>Your Characters</h3>
            <div className={styles.charactersContainer}>
                {
                    myCharacters.map((character) => {
                        return (
                            <figure onClick={() => handleRemove(character)} key={character.id}
                                    className={styles.character}>
                                <img className={styles.img} src={character.src} alt="Character"/>
                            </figure>
                        )
                    })
                }
            </div>
        </CharactersContext.Provider>
    )
}

export default Characters