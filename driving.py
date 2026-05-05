import random
from datetime import datetime
from typing import Dict, Any

import streamlit as st

from . import ui

LESSONS = [
    ("🧠", "Tư duy lái phòng vệ", "Nhìn xa, quét rộng, giữ khoảng cách và luôn có phương án thoát."),
    ("🚦", "Biển báo giao thông", "Nhận diện biển cấm, nguy hiểm, hiệu lệnh và chỉ dẫn bằng hình dạng + hành động."),
    ("↔️", "Rẽ làn & nhập làn", "Gương → xi nhan → điểm mù → chuyển làn mượt."),
    ("🌧️", "Đi mưa/ban đêm", "Giảm tốc, tăng khoảng cách, dùng đèn phù hợp, tránh thao tác gấp."),
    ("🅿️", "Sa hình", "Điểm căn, tốc độ chậm, quan sát gương và tránh cán vạch."),
]

QUESTIONS = [
    ("Khi chuyển làn, thứ tự đúng là gì?", ["Gương → Xi nhan → Điểm mù → Chuyển làn", "Xi nhan rồi chuyển ngay", "Bấm còi rồi lách", "Tăng tốc trước"], "Gương → Xi nhan → Điểm mù → Chuyển làn", "Quy trình này giúp xe khác nhận biết ý định và bạn tránh vùng điểm mù."),
    ("Khi trời mưa to, nên làm gì?", ["Giảm tốc và tăng khoảng cách", "Phanh gấp", "Tắt đèn", "Chạy sát xe trước"], "Giảm tốc và tăng khoảng cách", "Mưa làm giảm tầm nhìn và độ bám đường."),
    ("Gặp giao lộ không đèn, phản ứng đầu tiên là gì?", ["Giảm tốc và quan sát", "Tăng tốc", "Bấm còi liên tục", "Dừng giữa đường"], "Giảm tốc và quan sát", "Giao lộ có nhiều hướng xung đột nên cần phòng vệ."),
    ("Điểm mù là gì?", ["Vùng không nhìn thấy rõ qua gương", "Vùng trước kính lái", "Vị trí biển báo", "Khoảng cách phanh"], "Vùng không nhìn thấy rõ qua gương", "Cần liếc vai nhanh trước khi đổi hướng."),
    ("Khi nhập làn trên đường lớn, cách làm an toàn là gì?", ["Quan sát, tăng tốc phù hợp và nhập từ từ", "Dừng giữa làn nhập", "Lao thẳng vào làn", "Chỉ bấm còi"], "Quan sát, tăng tốc phù hợp và nhập từ từ", "Nhập làn an toàn cần hòa nhịp với dòng xe."),
    ("Khi xuống dốc dài, thói quen tốt là?", ["Giữ số phù hợp và kiểm soát tốc độ", "Về N cho trôi", "Tắt máy", "Chỉ dùng còi"], "Giữ số phù hợp và kiểm soát tốc độ", "Xuống dốc cần kiểm soát tốc độ và tận dụng phanh động cơ."),
    ("Gặp xe ưu tiên phát tín hiệu, bạn nên?", ["Giảm tốc, nhường đường an toàn", "Tăng tốc trước", "Đi giữa đường", "Không quan tâm"], "Giảm tốc, nhường đường an toàn", "Xe ưu tiên cần được nhường đường theo luật."),
    ("Lỗi phổ biến khi lùi chuồng là gì?", ["Đi quá nhanh và căn gương sai", "Đi chậm", "Nhìn gương", "Bật xi nhan"], "Đi quá nhanh và căn gương sai", "Lùi chuồng cần chậm và chính xác."),
]


def render_dashboard(profile: Dict[str, Any], save_cb) -> None:
    st.title("🚗 Học lái xe Production")
    st.caption("Bài học ngắn, hình động, quiz và AI gợi ý theo câu sai.")
    ui.lane_svg()
    cols = st.columns(3)
    for i, (ic, title, desc) in enumerate(LESSONS):
        with cols[i % 3]: ui.card(ic, title, desc, "Học nhanh")
    ui.speak_button("Hôm nay bạn nên học một bài ngắn, sau đó làm quiz và ôn lại câu sai ngay.", "🔊 Nghe gợi ý học lái", key="drive_hint")
    completed = set(profile.setdefault("driving", {}).setdefault("completed", []))
    selected = st.selectbox("Đánh dấu bài đã học", [x[1] for x in LESSONS])
    if st.button("✅ Lưu hoàn thành bài học"):
        completed.add(selected); profile["driving"]["completed"] = sorted(completed); save_cb(profile); st.success("Đã lưu tiến độ.")


def render_quiz(profile: Dict[str, Any], save_cb) -> None:
    st.title("🧪 Quiz lái xe thông minh")
    driving = profile.setdefault("driving", {})
    wrong_bank = driving.setdefault("wrong_bank", {})
    mode = st.radio("Chế độ", ["Quiz ngẫu nhiên", "Chỉ ôn câu sai"], horizontal=True)
    if mode == "Chỉ ôn câu sai" and wrong_bank:
        pool = [q for q in QUESTIONS if q[0] in wrong_bank]
    else:
        pool = QUESTIONS
    quiz = random.sample(pool, min(5, len(pool)))
    with st.form("driving_quiz"):
        answers = []
        for idx, q in enumerate(quiz, 1):
            st.markdown(f"**Câu {idx}: {q[0]}**")
            answers.append(st.radio("Chọn đáp án", q[1], key=f"dq_{idx}_{q[0]}", label_visibility="collapsed"))
        submitted = st.form_submit_button("Chấm điểm")
    if submitted:
        correct = 0
        for q, a in zip(quiz, answers):
            if a == q[2]:
                correct += 1
                if q[0] in wrong_bank:
                    wrong_bank[q[0]]["fixed"] = wrong_bank[q[0]].get("fixed", 0) + 1
                    if wrong_bank[q[0]]["fixed"] >= 2: wrong_bank.pop(q[0], None)
                st.success(f"Đúng: {q[0]}")
            else:
                wrong_bank[q[0]] = {"answer": q[2], "explain": q[3], "fixed": 0}
                st.error(f"Sai. Đáp án đúng: {q[2]}")
            st.info(q[3])
        score = round(correct / len(quiz) * 100)
        driving.setdefault("quiz_history", []).append({"time": datetime.now().isoformat(timespec="seconds"), "score": score, "correct": correct, "total": len(quiz)})
        save_cb(profile)
        st.metric("Điểm", f"{score}%", f"{correct}/{len(quiz)}")
