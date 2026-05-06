
from __future__ import annotations
import streamlit as st


def render() -> None:
    st.title("🧯 Deploy Hotfix Guide")
    st.caption("Sửa nhanh các lỗi thực tế hay gặp sau khi deploy Streamlit Cloud.")
    issues = [
        ("ModuleNotFoundError: modules", "Upload thiếu thư mục modules/ hoặc repo bị lồng thư mục.", "Vào GitHub, đảm bảo app.py và modules/ nằm cùng cấp ở ngoài cùng repo."),
        ("Không đọc được bộ 600 câu", "Thiếu data/official_600_questions_2025_extracted.json.", "Upload lại toàn bộ data/ và kiểm tra chữ hoa/thường trong tên file."),
        ("App chậm khi mở", "Dashboard hoặc module nặng load sớm.", "Bật Performance Mode = Nhẹ; chỉ mở Veo/TikTok khi cần."),
        ("Secrets không nhận", "Dán sai TOML hoặc thiếu dấu ngoặc kép.", "Vào Manage app → Settings → Secrets, kiểm tra TOML rồi Reboot."),
        ("Push/Web Push không hoạt động", "Thiếu HTTPS/VAPID/subscription hoặc browser chặn notification.", "Dùng Email/Telegram làm kênh nhắc ổn định chính; Web Push là nâng cao."),
    ]
    for title, cause, fix in issues:
        with st.expander(title):
            st.write("**Nguyên nhân thường gặp:** " + cause)
            st.write("**Cách sửa:** " + fix)
