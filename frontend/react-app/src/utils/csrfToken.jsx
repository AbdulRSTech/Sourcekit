import { useState, useEffect } from 'react'

// Utility function to get a cookie by name
export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Custom hook to manage CSRF token
export function useCSRFToken() {
    const [csrfToken, setCsrfToken] = useState('')

    useEffect(() => {
        fetch('/api/csrf/', {
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            setCsrfToken(data.csrfToken)
        })
        .catch(error => {
            console.error('Error fetching CSRF token:', error)
        })
    }, [])

    // Function to get the CSRF token (from state or cookie)
    const getCSRFToken = () => {
        // First try the state (from API)
        if (csrfToken) {
            return csrfToken;
        }
        
        // Fallback to cookie
        return getCookie('csrftoken');
    }

    return { csrfToken, getCSRFToken }
}
