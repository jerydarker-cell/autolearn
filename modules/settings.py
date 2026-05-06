import streamlit as st

from . import config


def render() -> None:
    st.title("⚙️ Production Settings")
    st.markdown("""
    ### Trạng thái backend
    - `DB_BACKEND`: **{}**
    - SQLite path: `{}`
    - Supabase URL configured: **{}**

    ### Secrets nên cấu hình khi deploy
    ```toml
    DB_BACKEND = "supabase"
    SUPABASE_URL = "https://xxxxx.supabase.co"
    SUPABASE_SERVICE_ROLE_KEY = "..."
    GOOGLE_API_KEY = "..."

    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = "587"
    SMTP_USER = "your_email@gmail.com"
    SMTP_PASSWORD = "app_password"
    SMTP_FROM = "your_email@gmail.com"

    TELEGRAM_BOT_TOKEN = "..."
    REMINDER_LOOKAHEAD_MIN = "15"
    ```
    """.format(config.DB_BACKEND, config.SQLITE_PATH, bool(config.SUPABASE_URL)))
