# Tùy chọn: chỉ dùng nếu đã cài GitHub CLI và chạy gh auth login
# Thay CHANGEME trước khi chạy.

gh secret set SUPABASE_URL --body "CHANGEME_PROJECT_URL"
gh secret set SUPABASE_SERVICE_ROLE_KEY --body "CHANGEME_SERVICE_ROLE_KEY"
gh secret set SMTP_HOST --body "smtp.gmail.com"
gh secret set SMTP_PORT --body "587"
gh secret set SMTP_USER --body "CHANGEME_EMAIL@gmail.com"
gh secret set SMTP_PASSWORD --body "CHANGEME_EMAIL_APP_PASSWORD"
gh secret set SMTP_FROM --body "CHANGEME_EMAIL@gmail.com"
gh secret set TELEGRAM_BOT_TOKEN --body ""
gh secret set REMINDER_LOOKAHEAD_MIN --body "15"
gh secret set GOOGLE_API_KEY --body ""
