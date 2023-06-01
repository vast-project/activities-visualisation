import { BsArrowRight } from 'react-icons/bs'
import styles from './button.module.css'

function Button({title, color, onClick}) {

  return (
    <button onClick={onClick} style={{backgroundColor: color}} className={styles.btn}>{title} <BsArrowRight/></button>
  )
}

export default Button