import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { DEMO_INSTITUTION_ID } from '../config'

function Login() {
  const [institutionId, setInstitutionId] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (institutionId.trim()) {
      localStorage.setItem('institutionId', institutionId.trim())
      navigate('/dashboard')
    }
  }

  const handleDemoLogin = () => {
    localStorage.setItem('institutionId', DEMO_INSTITUTION_ID)
    navigate('/dashboard')
  }

  return (
    <div className="min-h-screen bg-dark-bg flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-accent-primary mb-2">SaviorAI</h1>
          <p className="text-gray-400">Student Mental Health Monitoring System</p>
        </div>

        {/* Login Card */}
        <div className="bg-dark-card border border-dark-border rounded-lg p-8 shadow-lg">
          <h2 className="text-2xl font-semibold text-white mb-6">Institution Login</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Institution ID Input */}
            <div>
              <label htmlFor="institutionId" className="block text-sm font-medium text-gray-300 mb-2">
                Institution ID
              </label>
              <input
                type="text"
                id="institutionId"
                value={institutionId}
                onChange={(e) => setInstitutionId(e.target.value)}
                placeholder="Enter your institution UUID"
                className="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-transparent transition"
              />
            </div>

            {/* Login Button */}
            <button
              type="submit"
              className="w-full bg-accent-primary hover:bg-accent-primary/90 text-white font-semibold py-3 px-4 rounded-lg transition focus:outline-none focus:ring-2 focus:ring-accent-primary focus:ring-offset-2 focus:ring-offset-dark-bg"
            >
              Login to Dashboard
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-dark-border"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-dark-card text-gray-400">or</span>
            </div>
          </div>

          {/* Demo Login Button */}
          <button
            onClick={handleDemoLogin}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-dark-bg shadow-lg"
          >
            🎭 Demo Login (IIT Delhi)
          </button>
          
          <p className="text-xs text-gray-500 text-center mt-4">
            Demo login pre-fills the IIT Delhi demo institution with 50 sample students
          </p>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-sm text-gray-500">
          <p>Built with ❤️ for student wellbeing</p>
        </div>
      </div>
    </div>
  )
}

export default Login
