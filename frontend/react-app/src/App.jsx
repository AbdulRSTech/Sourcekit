import {HashRouter as Router, Routes, Route} from 'react-router-dom'

import Layout from './Layout'
import Download from './pages/Download'
import Search from './pages/Search'

import './App.css'

//render appropriate page
const App = () => {
  return (
    <Router>
      <Routes>
        {/* Layout route */}
        <Route element={<Layout/>}>
          <Route path="/" element={<Download/>}/>
          <Route path="search" element={<Search/>}/>
        </Route>
      </Routes>
    </Router>
  )
}

export default App;