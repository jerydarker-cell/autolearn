import json
from datetime import date, datetime, timedelta
from typing import Dict, Any, List

import pandas as pd
import streamlit as st

from .db import AppDatabase
from . import ui
from .notifications import send_email, send_telegram

WEEKDAYS = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]


def today_name() -> str:
    return WEEKDAYS[date.today().weekday()]


def due_items(db: AppDatabase, user_id: str) -> List[Dict[str, Any]]:
    meds = db.list_medications(user_id)
    items=[]
    logs = db.list_dose_logs(user_id, 500)
    logged = {(l.get("medication_id"), l.get("scheduled_at")[:16]): l for l in logs}
    for med in meds:
        days = med.get("days") or ["Tất cả"]
        if "Tất cả" not in days and today_name() not in days: continue
        for t in med.get("times", []):
            scheduled = f"{date.today().isoformat()} {t}"
            dt = datetime.strptime(scheduled, "%Y-%m-%d %H:%M")
            key=(med["id"], scheduled[:16])
            status = logged.get(key, {}).get("status", "pending")
            items.append({"med":med,"time":t,"scheduled_at":scheduled,"dt":dt,"status":status,"late": datetime.now()>dt+timedelta(minutes=30) and status=="pending"})
    return sorted(items, key=lambda x:x["dt"])


def render_medicine(db: AppDatabase, user: Dict[str, Any], profile: Dict[str, Any], save_cb) -> None:
    st.title("💊 Nhắc thuốc Production")
    st.caption("Lưu database thật, gửi nhắc ngoài app qua Email/Telegram bằng reminder worker.")
    meds = db.list_medications(user["id"], active_only=False)
    today = due_items(db, user["id"])
    c1,c2,c3,c4=st.columns(4)
    with c1: ui.metric_card("Thuốc", len(meds), "tổng danh sách")
    with c2: ui.metric_card("Hôm nay", len(today), "liều")
    with c3: ui.metric_card("Đã uống", len([x for x in today if x["status"]=="taken"]), "liều")
    with c4: ui.metric_card("Trễ", len([x for x in today if x["late"]]), "liều")

    st.subheader("🔔 Kênh nhắc ngoài app")
    note = profile.setdefault("notification", {})
    col1,col2,col3=st.columns(3)
    with col1: note["email_enabled"] = st.checkbox("Gửi email nhắc thuốc", value=note.get("email_enabled", True))
    with col2: note["telegram_chat_id"] = st.text_input("Telegram chat_id", value=note.get("telegram_chat_id", ""), placeholder="Ví dụ: 123456789")
    with col3:
        if st.button("💾 Lưu kênh nhắc"):
            save_cb(profile); st.success("Đã lưu cấu hình nhắc.")
    st.info("Để nhắc ngoài app hoạt động, bật GitHub Actions workflow `medicine-reminders.yml` hoặc chạy `python scripts/reminder_worker.py` bằng cron/server.")

    tab_today, tab_add, tab_manage = st.tabs(["Hôm nay", "Thêm thuốc", "Quản lý thuốc"])
    with tab_today:
        if not today: st.info("Hôm nay chưa có liều nào.")
        for item in today:
            med=item["med"]
            st.markdown(f"<div class='panel'><h3>{item['time']} · {med['name']}</h3><p><b>Liều:</b> {med['dose']} · <b>Cách dùng:</b> {med.get('instructions','')}</p><p class='muted'>Trạng thái: {item['status']}</p></div>", unsafe_allow_html=True)
            b1,b2,b3=st.columns(3)
            with b1:
                if st.button("✅ Đã uống", key="take"+item["scheduled_at"]+med["id"]):
                    db.log_dose(user["id"], med["id"], item["scheduled_at"], "taken");
                    inv = float(med.get("inventory",0) or 0) - float(med.get("units_per_dose",1) or 1)
                    db.update_medication(med["id"], {"inventory": max(0, inv)}); st.rerun()
            with b2:
                if st.button("⏰ Uống trễ", key="late"+item["scheduled_at"]+med["id"]): db.log_dose(user["id"], med["id"], item["scheduled_at"], "delayed"); st.rerun()
            with b3:
                if st.button("⏭️ Bỏ qua", key="skip"+item["scheduled_at"]+med["id"]): db.log_dose(user["id"], med["id"], item["scheduled_at"], "skipped"); st.rerun()
        low=[m for m in meds if float(m.get("inventory",0) or 0)<=float(m.get("refill_threshold",5) or 5) and m.get("active", True)]
        if low: st.warning("Thuốc sắp hết: " + ", ".join([m["name"] for m in low]))

    with tab_add:
        with st.form("add_med"):
            c1,c2,c3=st.columns(3)
            with c1: name=st.text_input("Tên thuốc *"); dose=st.text_input("Liều *", placeholder="1 viên")
            with c2: times=st.text_input("Giờ uống", value="07:00, 12:00, 20:00"); instructions=st.selectbox("Cách dùng", ["Sau ăn", "Trước ăn", "Trong bữa ăn", "Trước khi ngủ", "Theo chỉ định bác sĩ"])
            with c3: days=st.multiselect("Ngày uống", ["Tất cả"]+WEEKDAYS, default=["Tất cả"]); inventory=st.number_input("Số lượng còn",0.0,9999.0,0.0,1.0); threshold=st.number_input("Nhắc mua khi còn ≤",0.0,999.0,5.0,1.0)
            if st.form_submit_button("Thêm thuốc"):
                if not name or not dose: st.error("Nhập tên thuốc và liều.")
                else:
                    db.add_medication(user["id"], {"name":name,"dose":dose,"times":[x.strip() for x in times.split(',') if x.strip()],"days":days or ["Tất cả"],"instructions":instructions,"inventory":inventory,"refill_threshold":threshold})
                    st.success("Đã thêm thuốc."); st.rerun()

    with tab_manage:
        for med in meds:
            with st.expander(f"{med['name']} · {', '.join(med.get('times',[]))}"):
                st.write(med)
                if st.button("Tắt thuốc này", key="off"+med["id"]): db.update_medication(med["id"], {"active": False}); st.rerun()


def render_health(db: AppDatabase, user: Dict[str, Any]) -> None:
    st.title("🩺 Sức khỏe & báo cáo")
    with st.form("health"):
        c1,c2,c3,c4=st.columns(4)
        with c1: bp=st.text_input("Huyết áp", placeholder="120/80")
        with c2: pulse=st.text_input("Mạch", placeholder="72")
        with c3: temp=st.text_input("Nhiệt độ", placeholder="36.8")
        with c4: sugar=st.text_input("Đường huyết")
        pain=st.slider("Mức khó chịu/đau",0,10,0)
        note=st.text_area("Triệu chứng / ghi chú")
        if st.form_submit_button("Lưu ghi chú"):
            db.add_health_log(user["id"], {"bp":bp,"pulse":pulse,"temp":temp,"sugar":sugar,"pain":pain,"note":note})
            st.success("Đã lưu.")
    logs=db.list_health_logs(user["id"])
    if logs:
        df=pd.DataFrame([{**l["data"],"created_at":l["created_at"]} for l in logs])
        st.dataframe(df, use_container_width=True, hide_index=True)
