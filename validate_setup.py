"""Kiểm tra nhanh biến môi trường/Secrets cho AutoLearn v15.
Chạy local: python scripts/validate_setup.py
"""
import os

required = [
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
]
optional = [
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "SMTP_FROM",
    "TELEGRAM_BOT_TOKEN",
    "GOOGLE_API_KEY",
    "REMINDER_LOOKAHEAD_MIN",
]

print("AutoLearn v15 setup validation")
print("=" * 40)

ok = True
for key in required:
    value = os.getenv(key, "").strip()
    if not value:
        print(f"❌ Missing required: {key}")
        ok = False
    elif key == "SUPABASE_URL" and not value.startswith("https://"):
        print(f"⚠️ {key} có vẻ không đúng dạng URL: {value[:20]}...")
        ok = False
    else:
        print(f"✅ {key}: configured")

for key in optional:
    value = os.getenv(key, "").strip()
    print(("✅" if value else "➖") + f" {key}: " + ("configured" if value else "not set"))

if ok:
    print("\n✅ Cấu hình tối thiểu đã đủ để dùng Supabase.")
else:
    print("\n❌ Cần bổ sung các biến còn thiếu trước khi deploy production.")
