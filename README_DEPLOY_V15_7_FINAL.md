# Deploy v15.7 lên Streamlit Cloud

1. Upload toàn bộ thư mục package lên GitHub.
2. Main file path: `app.py`.
3. Copy nội dung `STREAMLIT_SECRETS_V15_7_COPY_PASTE.toml` vào Streamlit Secrets và điền key thật.
4. Reboot app.
5. Vào app > Push Notification để test thông báo.

## Web Push
- Chạy local: `python scripts/generate_vapid_keys.py` để tạo VAPID key.
- Thêm VAPID_PUBLIC_KEY và VAPID_PRIVATE_KEY vào Streamlit/GitHub Secrets.
- Người dùng tạo subscription trong app và lưu profile.
- Dùng `scripts/send_web_push.py push_subscription.json` để test gửi push.
