import React from 'react'
import styles from './error.module.css'
import { ErrorMessage } from '@hookform/error-message';

function Error({errors,id}) {

  return (
    <ErrorMessage 
        errors={errors} 
        name={id} 
        render={() => <p className={styles.errorMessage}>Required Fields</p>}
    />
  )
}

export default Error
