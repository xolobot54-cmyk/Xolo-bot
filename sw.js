const NOMBRE_CACHE = 'xolo-anti-ia-v1';
const ARCHIVOS_CACHE = [
  './',
  './index.html',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(NOMBRE_CACHE)
      .then(cache => cache.addAll(ARCHIVOS_CACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(nombres =>
      Promise.all(
        nombres.filter(n => n !== NOMBRE_CACHE).map(n => caches.delete(n))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request)
      .then(respuesta => respuesta || fetch(e.request))
  );
});
