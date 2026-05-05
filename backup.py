import json

import streamlit as st

from .db import AppDatabase


def render(db: AppDatabase, user, profile, save_cb) -> None:
    st.title("📤 Sao lưu, khôi phục & dữ liệu riêng")
    st.info("Dữ liệu hiện được lưu trong database. Bạn vẫn nên tải backup JSON định kỳ, đặc biệt khi dùng bản miễn phí/cloud.")
    data = db.export_user_data(user["id"])
    st.download_button("⬇️ Tải backup JSON", json.dumps(data, ensure_ascii=False, indent=2), f"autolearn_backup_{user['email']}.json", "application/json")
    uploaded = st.file_uploader("Khôi phục phần profile từ backup JSON", type=["json"])
    if uploaded and st.button("Khôi phục profile"):
        obj = json.loads(uploaded.getvalue().decode("utf-8"))
        if "profile" in obj:
            save_cb(obj["profile"])
            st.success("Đã khôi phục profile. Thuốc/log trong backup không tự ghi đè để tránh mất dữ liệu database.")
        else:
            st.error("File không có khóa profile.")
    if st.button("💾 Lưu nhanh profile hiện tại"):
        save_cb(profile); st.success("Đã lưu.")
