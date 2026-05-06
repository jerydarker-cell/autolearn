
from __future__ import annotations
from typing import Dict, Any, List
import streamlit as st

from . import ui
from . import official_exam
from . import public_safe


def _safe_list_users(db) -> List[Dict[str, Any]]:
    for name in ("list_users", "users", "all_users"):
        if hasattr(db, name):
            try:
                val = getattr(db, name)
                return val() if callable(val) else list(val)
            except Exception:
                return []
    return []


def render(db, user: Dict[str, Any], profile: Dict[str, Any]) -> None:
    st.title("👑 Admin Mini Dashboard")
    st.caption("Dashboard quản trị nhỏ để kiểm tra app trước khi public. Không thay thế hệ thống admin chuyên nghiệp.")

    bank = official_exam.active_bank(profile)
    checks, summary = public_safe.deep_validate(bank)
    users = _safe_list_users(db)
    meds_count = 0
    try:
        meds_count = len(db.list_medications(user["id"]))
    except Exception:
        pass

    c1, c2, c3, c4 = st.columns(4)
    with c1: ui.metric_card("Người dùng", len(users) if users else "N/A", "local/Supabase")
    with c2: ui.metric_card("600 câu", summary["total"], "câu")
    with c3: ui.metric_card("Điểm liệt", summary["critical_count"], "/60")
    with c4: ui.metric_card("Thuốc user hiện tại", meds_count, "mục")

    tabs = st.tabs(["🩺 App status", "🪪 Bộ 600 câu", "👥 User privacy", "☁️ Deploy", "🔐 Secrets"])

    with tabs[0]:
        bad = [c for c in checks if c["status"] == "bad"]
        warn = [c for c in checks if c["status"] == "warn"]
        if not bad:
            st.success("Không phát hiện lỗi dữ liệu nghiêm trọng trong kiểm tra nhanh.")
        else:
            st.error(f"Có {len(bad)} lỗi cần xử lý trước khi public.")
        if warn:
            st.warning(f"Có {len(warn)} cảnh báo nên xem lại.")
        for c in checks:
            status_icon = {"ok": "✅", "warn": "⚠️", "bad": "❌"}.get(c["status"], "ℹ️")
            st.markdown(f"<div class='admin-tile'><b>{status_icon} {c['name']}</b><br><span class='muted'>{c['detail']}</span></div>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("### Tóm tắt bộ 600 câu")
        st.json({k: v for k, v in summary.items() if k not in ("missing", "duplicates", "bad_options", "bad_answers")})
        st.info("Nếu chưa có đủ 60 câu điểm liệt, vào Public Safe Center để nhập danh sách ID chuẩn.")

    with tabs[2]:
        st.markdown("### Kiểm tra riêng tư tài khoản")
        st.write("Quy tắc cần đạt: tài khoản A không được thấy dữ liệu thuốc, quiz, backup của tài khoản B.")
        st.markdown("""
        <div class='admin-tile'>
        <b>Checklist nhanh</b><br>
        1. Tạo tài khoản A và thêm một thuốc test.<br>
        2. Đăng xuất, tạo tài khoản B.<br>
        3. Tài khoản B không được thấy thuốc của A.<br>
        4. Làm quiz ở B rồi đăng nhập lại A để kiểm tra dữ liệu không trộn.
        </div>
        """, unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("### Deploy readiness")
        st.code("app.py\nmodules/\ndata/\nstatic/\nscripts/\nsql/\n.streamlit/\nrequirements.txt\npackages.txt", language="text")
        st.warning("Không upload riêng app.py. Phải upload toàn bộ thư mục package lên GitHub.")

    with tabs[4]:
        st.markdown("### Secrets không được đưa lên GitHub")
        st.code("""DB_BACKEND = "supabase"
SUPABASE_URL = "..."
SUPABASE_SERVICE_ROLE_KEY = "..."
SMTP_PASSWORD = "..."
GOOGLE_API_KEY = ""
VAPID_PRIVATE_KEY = "..."
""", language="toml")
        st.info("Các key thật phải nằm trong Streamlit Cloud → Manage app → Settings → Secrets.")
