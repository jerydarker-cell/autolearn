import json
from typing import Dict, Any

import streamlit as st
import streamlit.components.v1 as components

from . import config


def render(profile: Dict[str, Any], save_cb) -> None:
    st.title('🔔 Push Notification thật')
    st.caption('Hỗ trợ thông báo trình duyệt, PWA/Web Push bằng Service Worker + VAPID, và worker gửi push ngoài app.')
    push = profile.setdefault('push', {})
    tabs = st.tabs(['⚡ Test ngay','📲 Web Push / PWA','💾 Lưu subscription','🧰 Worker gửi push'])
    with tabs[0]:
        st.markdown('### Browser notification test')
        components.html("""
        <div style="border:1px solid #1f2b42;border-radius:18px;background:#0f1728;color:#eef4ff;padding:14px;font-family:Arial">
          <button onclick="notifyNow()" style="padding:10px 14px;border-radius:999px;background:#111b2f;color:white;border:1px solid #334155;font-weight:800">Bật và test thông báo</button>
          <p id="status" style="color:#93a4be"></p>
        </div>
        <script>
        async function notifyNow(){
          if(!('Notification' in window)){document.getElementById('status').innerText='Trình duyệt không hỗ trợ Notification API.';return;}
          let p = await Notification.requestPermission();
          document.getElementById('status').innerText='Permission: '+p;
          if(p==='granted') new Notification('AutoLearn', {body:'Thông báo test hoạt động. Bạn có thể dùng để nhắc học / nhắc thuốc khi app đang mở.', icon:'/app/static/icon-192.svg'});
        }
        </script>
        """, height=120)
        st.info('Test này hoạt động ngay khi trình duyệt cho phép thông báo. Để push khi app đóng, cần Web Push + Service Worker + VAPID ở tab kế tiếp.')
    with tabs[1]:
        st.markdown('### Đăng ký Service Worker và tạo subscription')
        public_key = st.text_input('VAPID_PUBLIC_KEY', value=config.VAPID_PUBLIC_KEY, type='password')
        st.caption('Bạn có thể tạo VAPID key bằng lệnh: python scripts/generate_vapid_keys.py')
        components.html(f"""
        <div style="border:1px solid #1f2b42;border-radius:18px;background:#0f1728;color:#eef4ff;padding:14px;font-family:Arial">
          <button onclick="setupPush()" style="padding:10px 14px;border-radius:999px;background:#111b2f;color:white;border:1px solid #334155;font-weight:800">Tạo Push Subscription</button>
          <textarea id="sub" style="width:100%;height:150px;margin-top:10px;background:#0b1220;color:#dbeafe;border:1px solid #334155;border-radius:12px;padding:8px" placeholder="Subscription JSON sẽ hiện ở đây để copy"></textarea>
          <p id="msg" style="color:#93a4be"></p>
        </div>
        <script>
        const vapidPublicKey = {json.dumps(public_key)};
        function urlBase64ToUint8Array(base64String) {{
          const padding = '='.repeat((4 - base64String.length % 4) % 4);
          const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
          const rawData = window.atob(base64);
          const outputArray = new Uint8Array(rawData.length);
          for (let i = 0; i < rawData.length; ++i) outputArray[i] = rawData.charCodeAt(i);
          return outputArray;
        }}
        async function setupPush() {{
          const msg = document.getElementById('msg');
          try {{
            if(!('serviceWorker' in navigator)) throw new Error('Browser không hỗ trợ service worker');
            if(!('PushManager' in window)) throw new Error('Browser không hỗ trợ Push API');
            if(!vapidPublicKey) throw new Error('Bạn cần nhập VAPID_PUBLIC_KEY');
            const permission = await Notification.requestPermission();
            if(permission !== 'granted') throw new Error('Bạn chưa cho phép thông báo');
            let reg;
            try {{ reg = await navigator.serviceWorker.register('/service-worker.js'); }}
            catch(e) {{ reg = await navigator.serviceWorker.register('/app/static/service-worker.js'); }}
            const sub = await reg.pushManager.subscribe({{userVisibleOnly:true, applicationServerKey:urlBase64ToUint8Array(vapidPublicKey)}});
            document.getElementById('sub').value = JSON.stringify(sub, null, 2);
            msg.innerText = 'Đã tạo subscription. Copy JSON này dán vào tab Lưu subscription.';
          }} catch(e) {{ msg.innerText = 'Lỗi: ' + e.message; }}
        }}
        </script>
        """, height=260)
        st.warning('Web Push thật cần HTTPS, Service Worker, VAPID key và một worker/server gửi push định kỳ. Streamlit Cloud là HTTPS nên phù hợp, nhưng iOS/Android có thể yêu cầu cài PWA hoặc mở quyền thông báo.')
    with tabs[2]:
        sub_text = st.text_area('Dán Push Subscription JSON ở đây', value=json.dumps(push.get('subscription', {}), ensure_ascii=False, indent=2) if push.get('subscription') else '', height=220)
        c1, c2 = st.columns(2)
        with c1:
            if st.button('💾 Lưu subscription vào profile'):
                try:
                    push['subscription'] = json.loads(sub_text) if sub_text.strip() else {}
                    save_cb(profile)
                    st.success('Đã lưu Push subscription.')
                except Exception as e:
                    st.error(f'JSON chưa hợp lệ: {e}')
        with c2:
            if st.button('🧹 Xóa subscription'):
                push.pop('subscription', None)
                save_cb(profile)
                st.success('Đã xóa.')
        if push.get('subscription'):
            st.download_button('⬇️ Tải subscription JSON', json.dumps(push['subscription'], ensure_ascii=False, indent=2), 'push_subscription.json', 'application/json')
    with tabs[3]:
        st.markdown('''
        ### Gửi push thật ngoài app
        Bản này có sẵn:
        - `static/service-worker.js`
        - `static/manifest.webmanifest`
        - `scripts/generate_vapid_keys.py`
        - `scripts/send_web_push.py`

        Secrets cần thêm:
        ```toml
        VAPID_PUBLIC_KEY = "..."
        VAPID_PRIVATE_KEY = "..."
        VAPID_SUBJECT = "mailto:email_cua_ban@example.com"
        ```
        ''')
