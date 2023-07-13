import styles from './paragraph.module.css'

const Paragraph = ({text}) => {
  return (
    <p className={styles.paragraph}>
      {text}
    </p>
  )
}

export default Paragraph