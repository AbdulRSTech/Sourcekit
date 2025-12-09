import React, {useState, useEffect} from 'react'

const Download = () => {
    const initialFormData = {
        title: '',
        url: '',
        filename: '',
        notes: '',
        keywords: [],
        format: 'mp3'
    }

    const [isCreating, setIsCreating] = useState(false)
    const [formData, setFormData] = useState(initialFormData)
    const [csrfToken, setCsrfToken] = useState('')

    const [isSearching, setIsSearching] = useState(false)
    const [searchWord, setSearchWord] = useState('')
    const [keywordMessage, setKeywordMessage] = useState('')
    const [resourceMessage, setResourceMessage] = useState('')

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

    const addKeyword = (e) => {
        e.preventDefault()
        
        if (!searchWord.trim()) {
            setKeywordMessage('Please enter a keyword')
            return
        }

        setIsSearching(true)
        const token = getCSRFToken()
        let keyword = searchWord.trim()

        fetch(`/api/saveKeyword/${encodeURIComponent(keyword)}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            credentials: 'include'
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }
            return response.json()
        }).then(data => {
            if (data.error) {
                setKeywordMessage(data.error)
            } else {
                setKeywordMessage(data.success)
                setFormData({
                    ...formData,
                    keywords: [...formData.keywords, keyword]
                })
            }
        }).catch(error => {
            console.error('Error:', error)
            setKeywordMessage('Error occurred: ' + error.message)
        }).finally(() => {
            setIsSearching(false)
            setSearchWord('')
        })
    }

    const save = (e) => {
        e.preventDefault()
        const token = getCSRFToken()

        if (!token) {
            setResourceMessage('CSRF token not available. Please refresh the page.')
            return
        }

        setIsCreating(true)

        fetch('/api/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            credentials: 'include',
            body: JSON.stringify(formData)
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }
            return response.json()
        }).then(data => {
            if (data.error) {
                setResourceMessage(data.error)
            } else {
                setResourceMessage(data.success)
                setFormData(initialFormData)
            }
        }).catch(error => {
            console.error('Error:', error)
            setResourceMessage('Error occurred while creating resource: ' + error.message)
        }).finally(() => {
            setIsCreating(false)
        })
    }

    const saveAndDownload = (e) => {
        e.preventDefault()
        const token = getCSRFToken()

        if (!token) {
            setResourceMessage('CSRF token not available. Please refresh the page.')
            return
        }

        setIsCreating(true)

        fetch('/api/saveAndDownload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            credentials: 'include',
            body: JSON.stringify(formData)
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }
            return response.json()
        }).then(data => {
            if (data.error) {
                setResourceMessage(data.error)
            } else {
                setResourceMessage(data.success)
                setFormData(initialFormData)
            }
        }).catch(error => {
            console.error('Error:', error)
            setResourceMessage('Error occurred while creating resource: ' + error.message)
        }).finally(() => {
            setIsCreating(false)
        })
    }

    return (
        {resourceMessage && <p className="text-white font-bold">{resourceMessage}</p>}

        <form className="flex flex-col text-white gap-5">
            <input 
                type="text" 
                name="title" 
                placeholder="Title" 
                value={formData.title} 
                onChange={(event) => setFormData({...formData, title: event.target.value})}
                className="p-2 bg-gray-800 rounded"
            />

            <input 
                type="text" 
                name="url" 
                placeholder="URL" 
                value={formData.url}
                onChange={(event) => setFormData({...formData, url: event.target.value})}
                className="p-2 bg-gray-800 rounded"
            />

            <input 
                type="text" 
                name="filename" 
                placeholder="Filename" 
                value={formData.filename}
                onChange={(event) => setFormData({...formData, filename: event.target.value})}
                className="p-2 bg-gray-800 rounded"
            />

            <input 
                type="text" 
                name="notes" 
                placeholder="Notes" 
                value={formData.notes}
                onChange={(event) => setFormData({...formData, notes: event.target.value})}
                className="p-2 bg-gray-800 rounded"
            />

            <label className="flex flex-col gap-2">
                Select format (Only required if downloading now)
                <select 
                    className="bg-black text-white p-2 rounded" 
                    value={formData.format} 
                    onChange={(event) => setFormData({...formData, format: event.target.value})}
                >
                    <option value="mp3">mp3</option>
                    <option value="mp4">mp4</option>
                </select>
            </label> 

            <div className="flex flex-col gap-2">
                <p className="text-sm">Keywords added: {formData.keywords.join(', ') || 'None'}</p>
            </div>

            <input 
                type="text" 
                name="keyword" 
                placeholder="Type 1 keyword at a time" 
                value={searchWord}
                onChange={(event) => setSearchWord(event.target.value)}
                className="p-2 bg-gray-800 rounded"
            />

            {keywordMessage && <p className="text-white font-bold">{keywordMessage}</p>}
            
            <button 
                type="button"
                onClick={addKeyword} 
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
                disabled={isSearching}
            >
                Add keyword
            </button>
            {isSearching && <p className="text-white font-bold">Searching...</p>}

            <button 
                type="button"
                onClick={save} 
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
                disabled={isCreating}
            >
                Save
            </button>

            <button 
                type="button"
                onClick={saveAndDownload} 
                className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
                disabled={isCreating}
            >
                Save and Download
            </button>

            {isCreating && <p className="text-white font-bold">Creating...</p>}
        </form>
    )
}

export default Download;