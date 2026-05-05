# AutoLearn Ultra Production v15

Bản v15 là bản Production: đăng nhập thật, database thật, nhắc thuốc ngoài app, tách code module, deploy-ready cho Streamlit Cloud.

## 1. Cấu trúc

```text
app.py
modules/
  auth.py
  db.py
  ui.py
  ai.py
  driving.py
  english.py
  medicine.py
  notifications.py
  media_tools.py
  backup.py
  settings.py
scripts/
  reminder_worker.py
sql/
  supabase_schema.sql
.github/workflows/
  medicine-reminders.yml
.streamlit/config.toml
requirements.txt
packages.txt
```

## 2. Chạy local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Mặc định app dùng SQLite trong thư mục `app_data/`.

## 3. Deploy Streamlit Cloud

Upload toàn bộ repo lên GitHub rồi chọn:

```text
Main file path: app.py
```

## 4. Database thật bằng Supabase

1. Tạo project Supabase.
2. Mở SQL Editor.
3. Chạy file:

```text
sql/supabase_schema.sql
```

4. Trong Streamlit Cloud → App settings → Secrets, thêm:

```toml
DB_BACKEND = "supabase"
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "service_role_key"
GOOGLE_API_KEY = "optional"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USER = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
SMTP_FROM = "your_email@gmail.com"
TELEGRAM_BOT_TOKEN = "optional"
REMINDER_LOOKAHEAD_MIN = "15"
```

## 5. Nhắc thuốc ngoài app

Có 2 cách:

### Cách A: GitHub Actions

Repo đã có workflow:

```text
.github/workflows/medicine-reminders.yml
```

Nó chạy mỗi 15 phút và gọi:

```bash
python scripts/reminder_worker.py
```

Bạn cần thêm secrets trong GitHub repo Settings → Secrets and variables → Actions:

```text
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
SMTP_HOST
SMTP_PORT
SMTP_USER
SMTP_PASSWORD
SMTP_FROM
TELEGRAM_BOT_TOKEN
```

### Cách B: Server/VPS/Cron

```bash
*/15 * * * * cd /path/to/app && python scripts/reminder_worker.py
```

## 6. Lưu ý

- TikTok Downloader chỉ dùng cho video bạn sở hữu hoặc được phép tải.
- App nhắc thuốc hỗ trợ lịch và ghi nhận, không thay thế tư vấn bác sĩ/dược sĩ.
- Mật khẩu được băm bằng PBKDF2, không lưu mật khẩu dạng rõ.
- Supabase service role key chỉ để trong Secrets, không commit lên GitHub.


## v15.1 Stability Pack

Bản này đã được đóng gói lại đầy đủ module từ v15 Production và thêm `modules/stability.py`, `STABILITY_CHECKLIST.md`, các trang Stability Hub, Checklist test, Test 2 tài khoản, Hướng dẫn deploy, Trung tâm lỗi.

Trước khi public, chạy thử: đăng ký 2 tài khoản, thêm thuốc, làm quiz, backup, kiểm tra Supabase và GitHub Actions.

---

## Thay hẳn v8 bằng bản này

Nếu repo của bạn đang chạy AutoLearn v8, hãy xóa toàn bộ file cũ rồi upload toàn bộ gói này. Không chỉ upload app.py, vì bản v15.1 dùng modules/, scripts/, sql/ và workflow.

## Secrets đã chuẩn bị sẵn

Dùng file `STREAMLIT_SECRETS_COPY_PASTE.toml` để copy vào Streamlit Cloud Secrets.
Dùng file `GITHUB_ACTIONS_SECRETS_COPY_PASTE.env` để nhập GitHub Actions Secrets.

Không commit file đã điền key thật lên GitHub.
