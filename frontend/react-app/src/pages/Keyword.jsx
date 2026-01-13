import React, {useState, useEffect} from 'react'
import {useCSRFToken} from '../utils/csrfToken'

const Keyword = () => {
    const {getCSRFToken} = useCSRFToken()
    const token = getCSRFToken()

    return (
        <h1>Keyword crud operations</h1>
    )
}

export default Keyword