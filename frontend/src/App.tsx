import { useState } from 'react'
import LoginPage from './pages/login'
import Projects from './pages/projects'

const TOKEN_KEY = 'auth_token'

function App() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY))

  const handleLogin = (newToken: string) => {
    localStorage.setItem(TOKEN_KEY, newToken)
    setToken(newToken)
  }

  const handleLogout = () => {
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
  }

  if (!token) {
    return <LoginPage onLogin={handleLogin} />
  }

  return <Projects token={token} onUnauthorized={handleLogout} />
}

export default App
