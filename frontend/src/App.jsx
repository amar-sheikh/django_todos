import { useEffect, useState } from "react"

function App() {
  const [message, setMessage] = useState('Connecting to a backend...!')

  useEffect(()=>{
    const connectToBackend = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/health', {
          method: 'GET'
        })
  
        if (response.status === 200) {
          setMessage('Backend connected successfully...!')
        }
      }
      catch {
        setMessage('Error connecting to backend...!')
      }
    }

    connectToBackend()
  }, [])

  return (
    <div>{message}</div>
  )
}

export default App
