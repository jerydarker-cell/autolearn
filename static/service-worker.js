self.addEventListener('install', event => { self.skipWaiting(); });
self.addEventListener('activate', event => { event.waitUntil(self.clients.claim()); });
self.addEventListener('push', function(event) {
  let data = {};
  try { data = event.data ? event.data.json() : {}; } catch(e) { data = {title: 'AutoLearn', body: event.data ? event.data.text() : 'Bạn có nhắc nhở mới.'}; }
  event.waitUntil(self.registration.showNotification(data.title || 'AutoLearn Reminder', {
    body: data.body || 'Đã đến giờ học / uống thuốc / ôn bài.',
    icon: '/app/static/icon-192.svg',
    badge: '/app/static/icon-192.svg',
    data: { url: data.url || '/' }
  }));
});
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  const url = (event.notification.data && event.notification.data.url) || '/';
  event.waitUntil(clients.openWindow ? clients.openWindow(url) : Promise.resolve());
});
