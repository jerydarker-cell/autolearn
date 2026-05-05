import base64
import hashlib
import hmac
import os
from typing import Optional, Dict, Any

import streamlit as st

from .db import AppDatabase


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 240_000)
    return "pbkdf2_sha256$240000$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(dk).decode()


def verify_password(password: str, stored: str) -> bool:
    try:
        alg, rounds, salt_b64, hash_b64 = stored.split("$", 3)
        if alg != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(hash_b64)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(rounds))
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


def current_user() -> Optional[Dict[str, Any]]:
    return st.session_state.get("user")


def logout() -> None:
    st.session_state.pop("user", None)
    st.session_state.pop("profile", None)
    st.rerun()


def render_auth_gate(db: AppDatabase) -> Optional[Dict[str, Any]]:
    if st.session_state.get("user"):
        return st.session_state["user"]

    st.markdown("""
    <div class='hero'>
      <div class='hero-grid'>
        <div>
          <h1>🔐 AutoLearn Production</h1>
          <p>Đăng nhập thật, dữ liệu riêng, database thật, sẵn sàng deploy. Mỗi tài khoản có lịch thuốc, tiến độ học và dữ liệu sao lưu riêng.</p>
          <span class='pill green'>Production v15</span><span class='pill blue'>Private by account</span><span class='pill purple'>Database-backed</span>
        </div>
        <div class='phone-panel'><div class='road'><div class='drive-car'>🚗</div><div class='road-lane'></div><div class='road-line'></div></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["Đăng nhập", "Tạo tài khoản"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Mật khẩu", type="password")
            submitted = st.form_submit_button("Đăng nhập")
            if submitted:
                user = db.get_user_by_email(email)
                if user and verify_password(password, user.get("password_hash", "")):
                    st.session_state.user = {"id": user["id"], "email": user["email"], "display_name": user.get("display_name", "Bạn")}
                    st.session_state.profile = db.load_profile(user["id"])
                    st.success("Đăng nhập thành công.")
                    st.rerun()
                else:
                    st.error("Email hoặc mật khẩu chưa đúng.")

    with tab_register:
        with st.form("register_form"):
            display_name = st.text_input("Tên hiển thị", placeholder="Ví dụ: Minh")
            email = st.text_input("Email đăng ký", placeholder="you@example.com")
            password = st.text_input("Mật khẩu", type="password")
            password2 = st.text_input("Nhập lại mật khẩu", type="password")
            submitted = st.form_submit_button("Tạo tài khoản")
            if submitted:
                if not email or "@" not in email:
                    st.error("Email chưa hợp lệ.")
                elif len(password) < 8:
                    st.error("Mật khẩu nên có ít nhất 8 ký tự.")
                elif password != password2:
                    st.error("Hai mật khẩu chưa khớp.")
                elif db.get_user_by_email(email):
                    st.error("Email này đã tồn tại.")
                else:
                    user = db.create_user(email, display_name or email.split("@")[0], hash_password(password))
                    default_profile = {
                        "name": display_name or email.split("@")[0],
                        "xp": 0,
                        "level": 1,
                        "streak": 0,
                        "driving": {"completed": [], "quiz_history": [], "wrong_bank": {}},
                        "english": {"learned_words": [], "quiz_history": [], "wrong_bank": {}, "level": "A1"},
                        "ai_notes": [],
                        "notification": {"email_enabled": True, "telegram_chat_id": "", "daily_summary": True},
                    }
                    db.save_profile(user["id"], default_profile)
                    st.session_state.user = {"id": user["id"], "email": user["email"], "display_name": user.get("display_name", display_name)}
                    st.session_state.profile = default_profile
                    st.success("Tạo tài khoản thành công.")
                    st.rerun()

    st.info("Bản Production hỗ trợ SQLite khi chạy local và Supabase khi deploy. Nếu dùng Supabase, hãy tạo bảng theo `sql/supabase_schema.sql` và thêm Secrets.")
    return None
