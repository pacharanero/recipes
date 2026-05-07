// Service worker for the Recipes PWA.
// Minimal network-first strategy: just enough to satisfy the install
// criteria and provide a small offline fallback for already-visited pages.

const CACHE_NAME = 'recipes-cache-v1';
const OFFLINE_URLS = [
  '/recipes/',
  '/recipes/manifest.webmanifest',
  '/recipes/assets/icons/icon-192.png',
  '/recipes/assets/icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(OFFLINE_URLS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(request)
      .then((response) => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        return response;
      })
      .catch(() =>
        caches.match(request).then(
          (cached) => cached || caches.match('/recipes/')
        )
      )
  );
});
