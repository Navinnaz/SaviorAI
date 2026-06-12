import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import StudentProfile from './pages/StudentProfile'
import ActionLog from './pages/ActionLog'

function Navigation() {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path
  
  return (
    <nav className="bg-dark-card border-b border-dark-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <h1 className="text-xl font-bold text-accent-primary">GuardianAI</h1>
            <div className="flex space-x-4">
              <Link
                to="/"
                className={`px-3 py-2 rounded-md text-sm font-medium transition ${
                  isActive('/') 
                    ? 'bg-dark-bg text-accent-primary' 
                    : 'text-gray-300 hover:bg-dark-bg hover:text-white'
                }`}
              >
                Dashboard
              </Link>
              <Link
                to="/action-log"
                className={`px-3 py-2 rounded-md text-sm font-medium transition ${
                  isActive('/action-log')
                    ? 'bg-dark-bg text-accent-primary'
                    : 'text-gray-300 hover:bg-dark-bg hover:text-white'
                }`}
              >
                Action Log
              </Link>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="h-2 w-2 bg-accent-success rounded-full"></div>
            <span className="text-sm text-gray-400">Live</span>
          </div>
        </div>
      </div>
    </nav>
  )
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-dark-bg">
        <Navigation />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/student/:studentId" element={<StudentProfile />} />
            <Route path="/action-log" element={<ActionLog />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
