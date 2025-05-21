import { useEffect, useState } from "react"
import { Routes, Route, useNavigate } from 'react-router-dom'
import TodoList from './components/TodoList'
import TodoEdit from './components/TodoEdit'
import TodoAdd from './components/TodoAdd'
import TodoDelete from './components/TodoDelete'

const App = () => {
  const [message, setMessage] = useState('Connecting to a backend...!')
  const navigate = useNavigate()

  useEffect(()=>{
    const connectToBackend = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/health', {
          method: 'GET'
        })

        if (response.status === 200) {
          setMessage('Backend connected successfully...!')

          const timeoutID = setTimeout(()=>navigate('/todos'), 300)
          return ()=>clearTimeout(timeoutID)
        }
      }
      catch {
        setMessage('Error connecting to backend...!')
      }
    }

    connectToBackend()
  }, [])

  return (
    <Routes>
      <Route path='' element={<div>{message}</div>} />
      <Route path='/todos' element={<TodoList />} />
      <Route path='/todos/add' element={<TodoAdd />} />
      <Route path='/todos/edit/:id' element={<TodoEdit />} />
      <Route path='/todos/delete/:id' element={<TodoDelete />} />
    </Routes>
  )
}

export default App
