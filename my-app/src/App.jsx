import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Login1 from './components/Login1'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Login1/>
    </>
  )
}

export default App
