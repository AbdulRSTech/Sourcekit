import React, {useState, useEffect} from 'react'
import { useCSRFToken } from '../utils/csrfToken'

const Resource = () => {
    const {getCSRFToken} = useCSRFToken()
    const token = getCSRFToken()

    return (
        <h1>Resource</h1>
    )
}

export default Resource