import React, {useState, useEffect} from 'react'

const Search = () => {
        // Fetch CSRF token on component mount
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
    
        function getCookie(name) {
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
    
        function getCSRFToken() {
            // First try the state (from API)
            if (csrfToken) {
                return csrfToken;
            }
            
            // Fallback to cookie
            return getCookie('csrftoken');
        }

    return (
        <h1 className="text-white">Search/history</h1>
    )
}

export default Search;