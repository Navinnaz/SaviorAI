import React from 'react'
import { BrowserRouter, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Home from './pages/Home'
import StudentProfile from './pages/StudentProfile'
import ActionLog from './pages/ActionLog'

function Navigation() {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path
  
  const handleLogout = () => {
    localStorage.removeItem('institutionId')
    window.location.href = '/'
  }
  
  return (
    <nav className="bg-dark-card border-b border-dark-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <h1 className="text-xl font-bold text-accent-primary">SaviorAI</h1>
            <div className="flex space-x-4">
              <Link
                to="/dashboard"
                className={`px-3 py-2 rounded-md text-sm font-medium transition ${
                  isActive('/dashboard') 
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
            <button
              onClick={handleLogout}
              className="text-sm text-gray-400 hover:text-white transition"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

// Protected Route wrapper
function ProtectedRoute({ children }) {
  const institutionId = localStorage.getItem('institutionId')
  
  if (!institutionId) {
    return <Navigate to="/" replace />
  }
  
  return children
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Route - Login */}
        <Route path="/" element={<Login />} />
        
        {/* Protected Routes - Require institutionId */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-dark-bg">
                <Navigation />
                <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                  <Home />
                </main>
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/student/:studentId"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-dark-bg">
                <Navigation />
                <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                  <StudentProfile />
                </main>
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/action-log"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-dark-bg">
                <Navigation />
                <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                  <ActionLog />
                </main>
              </div>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App

