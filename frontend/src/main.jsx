import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Register service worker for PWA functionality
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // Request notification permission first
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission().then(permission => {
        console.log('Notification permission:', permission)
      })
    }
    
    // Register service worker
    navigator.serviceWorker
      .register('/serviceWorker.js', { scope: '/' })
      .then(registration => {
        console.log('✅ GuardianAI Service Worker registered:', registration.scope)
      })
      .catch(error => {
        console.error('❌ Service Worker registration failed:', error)
      })
  })
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
