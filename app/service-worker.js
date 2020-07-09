'use strict';

// CODELAB: Update cache names any time any of the cached files change.
const CACHE_NAME = 'mail-app-test-v1.1.4';

// CODELAB: Add list of files to cache here.
const FILES_TO_CACHE = [
    'index.html', 'app20.css', 'main_v2007091333.js', 'images/hm_sq.png', 'images/ikukuru_sq.png',
    'images/max_sq.gif', 'images/mint_sq.gif', 'images/pencil.png', 'images/select-icon.png',
    'images/to-bottom.png', 'images/wkwk_sq.gif', 'images/arr.png',
    'images/app_int/u1_1.png', 'images/app_int/u1_2.png', 'images/app_int/u1_3.png', 'images/app_int/u2_1.png',
    'images/app_int/u2_2.png', 'images/app_int/u2_3.png', 'images/app_int/u3_1.png', 'images/app_int/u3_2.png',
    'images/app_int/u3_3.png', 'images/app_int/u3_4.png', 'images/app_int/u4_1.png', 'images/app_int/u4_2.png'
];

self.addEventListener('install', (evt) => {
    console.log('[ServiceWorker] Install');
    // CODELAB: Precache static resources here.
    evt.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[ServiceWorker] Pre-caching offline page');
            return cache.addAll(FILES_TO_CACHE);
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
    console.log('[ServiceWorker] Activate');
    // CODELAB: Remove previous cached data from disk.
    evt.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (key !== CACHE_NAME) {
                    console.log('[ServiceWorker] Removing old cache', key);
                    return caches.delete(key);
                }
            }));
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (evt) => {
    console.log('[ServiceWorker] Fetch', evt.request.url);
    // CODELAB: Add fetch event handler here.
    if (evt.request.mode !== 'navigate') {
        // Not a page navigation, bail.
        return;
    }
    evt.respondWith(
        fetch(evt.request)
            .catch(() => {
                return caches.open(CACHE_NAME)
                    .then((cache) => {
                        return cache.match('index.html');
                    });
            })
    );


});
