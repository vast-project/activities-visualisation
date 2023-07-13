import styles from './subtitle.module.css'

const SubTitle = ({title}) => {
  return (
    <h3 className={styles.title}>
      {title}
    </h3>
  )
}

export default SubTitle