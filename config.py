import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
APP_DATA_DIR = BASE_DIR / "app_data"
APP_DATA_DIR.mkdir(exist_ok=True)

APP_NAME = "AutoLearn Ultra Production v15.2"
APP_VERSION = "15.2 Smart Offline AI"


def get_setting(name: str, default: str = "") -> str:
    """Read setting from environment first, then Streamlit secrets if available."""
    value = os.getenv(name)
    if value not in (None, ""):
        return value
    try:
        import streamlit as st
        if name in st.secrets:
            return str(st.secrets[name])
        # Support nested sections like [supabase]
        for section in ("supabase", "email", "telegram", "google", "app"):
            if section in st.secrets and name in st.secrets[section]:
                return str(st.secrets[section][name])
    except Exception:
        pass
    return default


DB_BACKEND = get_setting("DB_BACKEND", "sqlite").lower().strip()
SQLITE_PATH = get_setting("SQLITE_PATH", str(APP_DATA_DIR / "autolearn_v15.sqlite3"))
SUPABASE_URL = get_setting("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = get_setting("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_ANON_KEY = get_setting("SUPABASE_ANON_KEY", "")

GOOGLE_API_KEY = get_setting("GOOGLE_API_KEY", "")

# AI cost control: offline-first by default. External AI is disabled unless explicitly enabled.
AI_MODE = get_setting("AI_MODE", "offline").lower().strip()  # offline | hybrid | external
USE_EXTERNAL_AI = get_setting("USE_EXTERNAL_AI", "false").lower().strip() in ("1", "true", "yes", "on")
AI_CACHE_ENABLED = get_setting("AI_CACHE_ENABLED", "true").lower().strip() in ("1", "true", "yes", "on")
AI_CACHE_PATH = get_setting("AI_CACHE_PATH", str(APP_DATA_DIR / "internal_ai_cache.json"))
MAX_EXTERNAL_AI_CALLS_PER_SESSION = int(get_setting("MAX_EXTERNAL_AI_CALLS_PER_SESSION", "0") or "0")

SMTP_HOST = get_setting("SMTP_HOST", "")
SMTP_PORT = int(get_setting("SMTP_PORT", "587") or "587")
SMTP_USER = get_setting("SMTP_USER", "")
SMTP_PASSWORD = get_setting("SMTP_PASSWORD", "")
SMTP_FROM = get_setting("SMTP_FROM", SMTP_USER)

TELEGRAM_BOT_TOKEN = get_setting("TELEGRAM_BOT_TOKEN", "")

REMINDER_LOOKAHEAD_MIN = int(get_setting("REMINDER_LOOKAHEAD_MIN", "15") or "15")
