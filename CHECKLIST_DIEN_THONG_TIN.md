# Checklist điền thông tin AutoLearn v15 Production

## Bạn chỉ cần chuẩn bị 5 thông tin chính

1. `SUPABASE_URL`
2. `SUPABASE_SERVICE_ROLE_KEY`
3. `SMTP_USER`
4. `SMTP_PASSWORD` / email app password
5. `SMTP_FROM`

Tuỳ chọn:

6. `TELEGRAM_BOT_TOKEN`
7. `GOOGLE_API_KEY`

## Thứ tự làm

1. Tạo Supabase project.
2. Vào Supabase SQL Editor, chạy file `sql/supabase_schema.sql`.
3. Mở `setup_wizard.py` bằng `run_setup_wizard.bat` hoặc `Run_Setup_Wizard_Mac.command`.
4. Điền các thông tin vào form.
5. Copy nội dung Streamlit Secrets dán vào Streamlit Cloud.
6. Copy GitHub Actions Secrets nhập vào GitHub repo.
7. Reboot app trên Streamlit Cloud.
8. Test đăng ký tài khoản, đăng nhập, thêm thuốc thử.

## Không làm

- Không đưa `service_role_key` lên GitHub.
- Không gửi key/mật khẩu trong chat.
- Không commit file `streamlit_secrets.toml` nếu đã điền key thật.
