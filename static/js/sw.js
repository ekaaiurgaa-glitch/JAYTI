/* ============================================
   SERVICE WORKER - TRUE OFFLINE MODE (PWA)
   Cache-First Strategy | Offline Write Support
   ============================================ */

const CACHE_NAME = 'jaytipargal-v1';
const APP_SHELL_URLS = [
    '/',
    '/dashboard/',
    '/diary/',
    '/diary/write/',
    '/goals/',
    '/notes/',
    '/astro/',
    '/static/css/custom.css',
    '/static/js/offline-sync.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&family=Dancing+Script:wght@400;600&display=swap'
];

// Install Event - Cache App Shell
self.addEventListener('install', (event) => {
    console.log('[SW] Installing...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] Caching app shell');
                return cache.addAll(APP_SHELL_URLS);
            })
            .then(() => {
                console.log('[SW] App shell cached successfully');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('[SW] Cache failed:', error);
            })
    );
});

// Activate Event - Clean old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames
                        .filter((name) => name !== CACHE_NAME)
                        .map((name) => caches.delete(name))
                );
            })
            .then(() => {
                console.log('[SW] Activated successfully');
                return self.clients.claim();
            })
    );
});

// Fetch Event - Cache-First Strategy
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET requests (POST, PUT, DELETE go to network)
    if (request.method !== 'GET') {
        return;
    }
    
    // Strategy: Cache-First for App Shell, Network-First for API
    if (isAppShell(url.pathname)) {
        event.respondWith(cacheFirst(request));
    } else if (isAPIRequest(url.pathname)) {
        event.respondWith(networkFirst(request));
    } else {
        // Default: Cache with network fallback
        event.respondWith(cacheWithNetworkFallback(request));
    }
});

// Helper: Check if request is for app shell
function isAppShell(pathname) {
    const appPaths = ['/', '/dashboard/', '/diary/', '/goals/', '/notes/', '/astro/', '/static/'];
    return appPaths.some(path => pathname.startsWith(path));
}

// Helper: Check if request is for API
function isAPIRequest(pathname) {
    return pathname.startsWith('/api/') || pathname.includes('/send_message/');
}

// Cache-First Strategy
async function cacheFirst(request) {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    
    if (cached) {
        console.log('[SW] Serving from cache:', request.url);
        return cached;
    }
    
    try {
        const networkResponse = await fetch(request);
        cache.put(request, networkResponse.clone());
        return networkResponse;
    } catch (error) {
        console.error('[SW] Network failed, no cache:', request.url);
        throw error;
    }
}

// Network-First Strategy (for API calls)
async function networkFirst(request) {
    const cache = await caches.open(CACHE_NAME);
    
    try {
        const networkResponse = await fetch(request);
        cache.put(request, networkResponse.clone());
        return networkResponse;
    } catch (error) {
        console.log('[SW] Network failed, trying cache:', request.url);
        const cached = await cache.match(request);
        
        if (cached) {
            return cached;
        }
        
        // Return offline response for API
        return new Response(
            JSON.stringify({ 
                offline: true, 
                message: 'You are offline. Your data will sync when connection returns.' 
            }),
            { 
                headers: { 'Content-Type': 'application/json' },
                status: 503 
            }
        );
    }
}

// Cache with Network Fallback
async function cacheWithNetworkFallback(request) {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    
    const networkFetch = fetch(request)
        .then((response) => {
            cache.put(request, response.clone());
            return response;
        })
        .catch(() => cached);
    
    return cached || networkFetch;
}

// Background Sync for Offline Writes
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-diary-entries') {
        console.log('[SW] Background sync triggered');
        event.waitUntil(syncDiaryEntries());
    }
});

// Sync diary entries from IndexedDB to server
async function syncDiaryEntries() {
    const clients = await self.clients.matchAll();
    
    clients.forEach((client) => {
        client.postMessage({
            type: 'SYNC_DIARY_ENTRIES'
        });
    });
}

// Listen for messages from main thread
self.addEventListener('message', (event) => {
    if (event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
