/* Service Worker — إلهام
   تخزين مؤقت للعمل دون اتصال + تحديث عبر الشبكة أولاً للصفحات */
var CACHE = 'ilham-v1';
var CORE = [
  './',
  './index.html',
  './manifest.json',
  './assets/fonts/Amiri-Regular.ttf',
  './assets/fonts/ArefRuqaa-Regular.ttf',
  './assets/icons/icon-192.png',
  './assets/icons/icon-512.png'
];

self.addEventListener('install', function(e){
  e.waitUntil(
    caches.open(CACHE).then(function(c){ return c.addAll(CORE); })
      .then(function(){ return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function(e){
  e.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(keys.filter(function(k){ return k !== CACHE; })
        .map(function(k){ return caches.delete(k); }));
    }).then(function(){ return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function(e){
  var req = e.request;
  if(req.method !== 'GET') return;
  var url = new URL(req.url);
  if(url.origin !== location.origin) return;

  /* الصفحات: الشبكة أولاً مع رجوع للكاش */
  if(req.mode === 'navigate'){
    e.respondWith(
      fetch(req).then(function(res){
        var cl = res.clone();
        caches.open(CACHE).then(function(c){ c.put('./index.html', cl); });
        return res;
      }).catch(function(){ return caches.match('./index.html'); })
    );
    return;
  }

  /* الأصول: الكاش أولاً مع تحديث خلفي */
  e.respondWith(
    caches.match(req).then(function(hit){
      if(hit){
        fetch(req).then(function(res){
          if(res && res.ok){
            var cl = res.clone();
            caches.open(CACHE).then(function(c){ c.put(req, cl); });
          }
        }).catch(function(){});
        return hit;
      }
      return fetch(req).then(function(res){
        if(res && res.ok){
          var cl = res.clone();
          caches.open(CACHE).then(function(c){ c.put(req, cl); });
        }
        return res;
      }).catch(function(){ return hit; });
    })
  );
});
