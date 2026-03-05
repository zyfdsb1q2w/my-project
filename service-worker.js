// 美霖个人助手 - Service Worker
// 版本: 1.0.0
// 缓存名称
const CACHE_NAME = '美霖助手-v1.0.0';
const STATIC_CACHE_NAME = '美霖助手-static-v1.0.0';

// 需要缓存的静态资源
const STATIC_ASSETS = [
  '/',
  '/manifest.json',
  '/icons/icon-72x72.png',
  '/icons/icon-96x96.png',
  '/icons/icon-128x128.png',
  '/icons/icon-144x144.png',
  '/icons/icon-152x152.png',
  '/icons/icon-192x192.png',
  '/icons/icon-384x384.png',
  '/icons/icon-512x512.png'
];

// 安装事件 - 缓存静态资源
self.addEventListener('install', event => {
  console.log('Service Worker 安装中...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then(cache => {
        console.log('缓存静态资源...');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('Service Worker 安装完成');
        return self.skipWaiting();
      })
  );
});

// 激活事件 - 清理旧缓存
self.addEventListener('activate', event => {
  console.log('Service Worker 激活中...');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          // 删除旧版本的缓存
          if (cacheName !== CACHE_NAME && cacheName !== STATIC_CACHE_NAME) {
            console.log('删除旧缓存:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('Service Worker 激活完成');
      return self.clients.claim();
    })
  );
});

// 获取事件 - 网络优先，回退到缓存
self.addEventListener('fetch', event => {
  // 跳过非GET请求
  if (event.request.method !== 'GET') return;
  
  // 跳过Streamlit的WebSocket连接
  if (event.request.url.includes('/_stcore/stream')) return;
  
  event.respondWith(
    // 尝试网络请求
    fetch(event.request)
      .then(response => {
        // 如果请求成功，克隆并缓存响应
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseClone);
            });
        }
        return response;
      })
      .catch(() => {
        // 网络失败，尝试从缓存获取
        return caches.match(event.request)
          .then(cachedResponse => {
            if (cachedResponse) {
              console.log('从缓存返回:', event.request.url);
              return cachedResponse;
            }
            
            // 如果缓存也没有，返回离线页面
            if (event.request.mode === 'navigate') {
              return caches.match('/')
                .then(cachedPage => {
                  if (cachedPage) {
                    return cachedPage;
                  }
                  // 返回简单的离线提示
                  return new Response(
                    '<h1>美霖助手离线中</h1><p>请检查网络连接后重试</p>',
                    { headers: { 'Content-Type': 'text/html' } }
                  );
                });
            }
            
            // 对于其他资源，返回错误
            return new Response('网络连接失败', { status: 408 });
          });
      })
  );
});

// 后台同步事件（如果需要）
self.addEventListener('sync', event => {
  console.log('后台同步:', event.tag);
  
  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

// 推送事件（如果需要）
self.addEventListener('push', event => {
  console.log('推送通知:', event);
  
  const options = {
    body: '美霖助手有新消息',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '1'
    },
    actions: [
      {
        action: 'explore',
        title: '查看',
        icon: '/icons/icon-72x72.png'
      },
      {
        action: 'close',
        title: '关闭',
        icon: '/icons/icon-72x72.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('美霖助手', options)
  );
});

// 通知点击事件
self.addEventListener('notificationclick', event => {
  console.log('通知被点击:', event.notification.tag);
  event.notification.close();
  
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(clientList => {
      for (const client of clientList) {
        if (client.url === '/' && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow('/');
      }
    })
  );
});

// 同步数据函数
function syncData() {
  // 这里可以添加数据同步逻辑
  console.log('同步数据...');
  return Promise.resolve();
}