import styles from './button.module.css'

const Button = ({text,color, onClick}) => {
  return (
    <button onClick={onClick} className={styles.button} style={{backgroundColor:color}}>
      {text}
    </button>
  )
}

export default Button