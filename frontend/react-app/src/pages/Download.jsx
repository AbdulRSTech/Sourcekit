import React, {useState, useEffect} from 'react'
import {useCSRFToken} from '../utils/csrfToken'

const Download = () => {
    const {getCSRFToken} = useCSRFToken()
    const toekn = getCSRFToken()

    return (
        <h1>Download</h1>
    )
}

export default Download;