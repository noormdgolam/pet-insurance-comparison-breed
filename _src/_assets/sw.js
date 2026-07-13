const CACHE_NAME = 'pet-insurance-guide-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/css/style.css',
    '/js/main.js',
    '/manifest.json'
];

// Install event
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

// Activate event
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch event: Stale-while-revalidate strategy
self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;
    // Don't cache analytics or adsense
    if (event.request.url.includes('google-analytics') || event.request.url.includes('googlesyndication') || event.request.url.includes('googletagmanager')) {
        return;
    }
    
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            const fetchPromise = fetch(event.request).then((networkResponse) => {
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, networkResponse.clone());
                });
                return networkResponse;
            });
            return cachedResponse || fetchPromise;
        })
    );
});
