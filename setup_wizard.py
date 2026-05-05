import json
import textwrap
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="AutoLearn v15 Setup Wizard", page_icon="🛠️", layout="wide")

st.markdown("""
<style>
.stApp{background:linear-gradient(180deg,#f8fbff,#edf6ff)}
.card{background:white;border:1px solid #e2e8f0;border-radius:24px;padding:18px;box-shadow:0 14px 34px rgba(15,23,42,.07)}
.big{font-size:2.1rem;font-weight:900;margin:0}.muted{color:#64748b}
</style>
""", unsafe_allow_html=True)

st.title("🛠️ AutoLearn v15 Production Setup Wizard")
st.caption("Bạn chỉ cần điền thông tin, app sẽ tạo sẵn nội dung để dán vào Streamlit Secrets và GitHub Actions Secrets. Không upload file chứa key lên GitHub.")

st.warning("Không chia sẻ các key/mật khẩu trong chat hoặc commit lên GitHub. File tạo ra chỉ dùng trên máy bạn.")

with st.expander("1️⃣ Supabase", expanded=True):
    supabase_url = st.text_input("SUPABASE_URL", placeholder="https://xxxxx.supabase.co")
    supabase_key = st.text_input("SUPABASE_SERVICE_ROLE_KEY", type="password", placeholder="service_role key")

with st.expander("2️⃣ Email SMTP để nhắc thuốc ngoài app", expanded=True):
    smtp_host = st.text_input("SMTP_HOST", value="smtp.gmail.com")
    smtp_port = st.text_input("SMTP_PORT", value="587")
    smtp_user = st.text_input("SMTP_USER", placeholder="your_email@gmail.com")
    smtp_password = st.text_input("SMTP_PASSWORD / App Password", type="password", placeholder="mật khẩu ứng dụng email")
    smtp_from = st.text_input("SMTP_FROM", placeholder="your_email@gmail.com")

with st.expander("3️⃣ Telegram Bot, Google API, nhắc thuốc", expanded=False):
    telegram_token = st.text_input("TELEGRAM_BOT_TOKEN", type="password", placeholder="có thể để trống nếu chưa dùng")
    google_api_key = st.text_input("GOOGLE_API_KEY", type="password", placeholder="có thể để trống nếu chưa dùng Gemini/Veo")
    reminder_lookahead = st.text_input("REMINDER_LOOKAHEAD_MIN", value="15")

secrets_toml = f'''DB_BACKEND = "supabase"
SUPABASE_URL = "{supabase_url.strip()}"
SUPABASE_SERVICE_ROLE_KEY = "{supabase_key.strip()}"

GOOGLE_API_KEY = "{google_api_key.strip()}"

SMTP_HOST = "{smtp_host.strip()}"
SMTP_PORT = "{smtp_port.strip()}"
SMTP_USER = "{smtp_user.strip()}"
SMTP_PASSWORD = "{smtp_password.strip()}"
SMTP_FROM = "{smtp_from.strip()}"

TELEGRAM_BOT_TOKEN = "{telegram_token.strip()}"
REMINDER_LOOKAHEAD_MIN = "{reminder_lookahead.strip()}"
'''

github_env = f'''SUPABASE_URL={supabase_url.strip()}
SUPABASE_SERVICE_ROLE_KEY={supabase_key.strip()}
SMTP_HOST={smtp_host.strip()}
SMTP_PORT={smtp_port.strip()}
SMTP_USER={smtp_user.strip()}
SMTP_PASSWORD={smtp_password.strip()}
SMTP_FROM={smtp_from.strip()}
TELEGRAM_BOT_TOKEN={telegram_token.strip()}
REMINDER_LOOKAHEAD_MIN={reminder_lookahead.strip()}
GOOGLE_API_KEY={google_api_key.strip()}
'''

gh_commands = f'''gh secret set SUPABASE_URL --body "{supabase_url.strip()}"
gh secret set SUPABASE_SERVICE_ROLE_KEY --body "{supabase_key.strip()}"
gh secret set SMTP_HOST --body "{smtp_host.strip()}"
gh secret set SMTP_PORT --body "{smtp_port.strip()}"
gh secret set SMTP_USER --body "{smtp_user.strip()}"
gh secret set SMTP_PASSWORD --body "{smtp_password.strip()}"
gh secret set SMTP_FROM --body "{smtp_from.strip()}"
gh secret set TELEGRAM_BOT_TOKEN --body "{telegram_token.strip()}"
gh secret set REMINDER_LOOKAHEAD_MIN --body "{reminder_lookahead.strip()}"
gh secret set GOOGLE_API_KEY --body "{google_api_key.strip()}"
'''

st.markdown("## ✅ Kết quả cấu hình")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Streamlit Secrets")
    st.code(secrets_toml, language="toml")
    st.download_button("⬇️ Tải streamlit_secrets.toml", secrets_toml, "streamlit_secrets.toml", "text/plain")
with col2:
    st.markdown("### GitHub Actions Secrets")
    st.code(github_env, language="bash")
    st.download_button("⬇️ Tải github_actions_secrets.env", github_env, "github_actions_secrets.env", "text/plain")

st.markdown("### Lệnh GitHub CLI tùy chọn")
st.caption("Chỉ dùng nếu bạn đã cài GitHub CLI và chạy `gh auth login`. Nếu không, nhập thủ công trong GitHub Settings → Secrets and variables → Actions.")
st.code(gh_commands, language="bash")
st.download_button("⬇️ Tải github_cli_secret_commands.sh", gh_commands, "github_cli_secret_commands.sh", "text/x-shellscript")

st.markdown("## 📌 Dán ở đâu?")
st.markdown("""
- **Streamlit Cloud:** Manage app → Settings → Secrets → dán nội dung `streamlit_secrets.toml`.
- **GitHub Actions:** Repo → Settings → Secrets and variables → Actions → New repository secret → nhập từng dòng trong `github_actions_secrets.env`.
- **Supabase:** SQL Editor → dán nội dung file `sql/supabase_schema.sql` → Run.
""")

if st.button("🧪 Kiểm tra nhanh thông tin đã điền"):
    problems = []
    if not supabase_url.startswith("https://") or ".supabase.co" not in supabase_url:
        problems.append("SUPABASE_URL có vẻ chưa đúng dạng https://xxxxx.supabase.co")
    if len(supabase_key.strip()) < 20:
        problems.append("SUPABASE_SERVICE_ROLE_KEY có vẻ đang trống hoặc quá ngắn")
    if smtp_user and not smtp_from:
        problems.append("Bạn đã nhập SMTP_USER nhưng chưa nhập SMTP_FROM")
    if problems:
        st.error("\n".join([f"- {p}" for p in problems]))
    else:
        st.success("Thông tin nhìn ổn. Hãy dán vào Streamlit Secrets và GitHub Actions Secrets.")
