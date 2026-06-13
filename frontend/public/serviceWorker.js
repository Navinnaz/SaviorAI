/**
 * GuardianAI Service Worker
 * 
 * Features:
 * - Cache app shell for offline access
 * - Show installation notification
 * - Register push notifications
 */

const CACHE_NAME = 'guardianai-v1'
const APP_SHELL = [
  '/',
  '/index.html',
  '/src/main.jsx',
  '/src/App.jsx',
  '/src/index.css'
]

// Install event - cache app shell
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Installing...')
  
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Caching app shell')
      return cache.addAll(APP_SHELL)
    })
  )
  
  self.skipWaiting()
})

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activating...')
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      )
    })
  )
  
  self.clients.claim()
  
  // Show installation notification (only if permission granted)
  if (Notification.permission === 'granted') {
    self.registration.showNotification('GuardianAI', {
      body: 'GuardianAI is watching 👁️\nStudent mental health monitoring active.',
      icon: '/icons/icon-192x192.png',
      badge: '/icons/icon-72x72.png',
      tag: 'guardianai-installed',
      requireInteraction: false
    }).catch(err => console.log('Notification error:', err))
  } else {
    console.log('Notification permission not granted, skipping notification')
  }
})

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return
  }
  
  // Skip API requests (always fetch fresh)
  if (event.request.url.includes('/api/')) {
    return event.respondWith(fetch(event.request))
  }
  
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request).then((fetchResponse) => {
        return caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, fetchResponse.clone())
          return fetchResponse
        })
      })
    }).catch(() => {
      // Offline fallback
      return caches.match('/')
    })
  )
})

// Push notification event
self.addEventListener('push', (event) => {
  console.log('[ServiceWorker] Push notification received')
  
  const data = event.data ? event.data.json() : {}
  const title = data.title || 'GuardianAI Alert'
  const options = {
    body: data.body || 'New update available',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    tag: data.tag || 'guardianai-alert',
    data: data.url || '/',
    requireInteraction: data.urgent || false
  }
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  )
})

// Notification click event
self.addEventListener('notificationclick', (event) => {
  console.log('[ServiceWorker] Notification clicked')
  
  event.notification.close()
  
  const urlToOpen = event.notification.data || '/'
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((windowClients) => {
        // Check if there's already a window open
        for (let client of windowClients) {
          if (client.url === urlToOpen && 'focus' in client) {
            return client.focus()
          }
        }
        // Open new window
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen)
        }
      })
  )
})

console.log('[ServiceWorker] Loaded')
