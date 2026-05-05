# AutoLearn v15.1 Fixed Final - Replace v8 Package

Gói này là bản hoàn chỉnh để thay hẳn AutoLearn v8.

## Có sẵn trong gói

- App Production v15.1 Fixed
- Đăng nhập thật
- Database SQLite local / Supabase production
- Nhắc thuốc ngoài app bằng GitHub Actions
- Học lái xe
- Học tiếng Anh
- Nhắc mẹ uống thuốc
- Google Veo
- TikTok Downloader
- Stability Hub
- Checklist test
- Setup Wizard
- Streamlit Secrets template
- GitHub Actions Secrets template

## Bạn chỉ cần điền thông tin

Mở file:

```
STREAMLIT_SECRETS_COPY_PASTE.toml
```

Điền:

- SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY
- SMTP_USER
- SMTP_PASSWORD
- SMTP_FROM
- GOOGLE_API_KEY nếu dùng Veo/Gemini
- TELEGRAM_BOT_TOKEN nếu dùng Telegram

Sau đó copy vào Streamlit Cloud Secrets.

## Setup Wizard

Windows:

```
run_setup_wizard.bat
```

Mac:

```
Run_Setup_Wizard_Mac.command
```

Wizard sẽ giúp bạn tạo nội dung Secrets để copy/paste.


## V15.2 Offline AI

Đã thêm AI nội bộ không tốn API mặc định. Vào trang `🧠 API nội bộ tiết kiệm` để kiểm tra. Xem thêm `AI_NO_COST_GUIDE.md`.
