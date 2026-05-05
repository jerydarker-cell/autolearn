import json
from datetime import datetime

import pandas as pd
import streamlit as st

from modules import ai, backup, driving, english, media_tools, medicine, settings, stability, ui
from modules.auth import current_user, logout, render_auth_gate
from modules.db import get_db
from modules.config import APP_NAME, APP_VERSION, AI_MODE, USE_EXTERNAL_AI

st.set_page_config(page_title=APP_NAME, page_icon="🚗", layout="wide", initial_sidebar_state="expanded")
ui.apply_style()

db = get_db()
user = render_auth_gate(db)
if not user:
    st.stop()

if "profile" not in st.session_state:
    st.session_state.profile = db.load_profile(user["id"])
profile = st.session_state.profile
profile.setdefault("name", user.get("display_name", "Bạn"))
profile.setdefault("driving", {"completed": [], "quiz_history": [], "wrong_bank": {}})
profile.setdefault("english", {"learned_words": [], "quiz_history": [], "wrong_bank": {}, "level": "A1"})
profile.setdefault("ai_notes", [])
profile.setdefault("notification", {"email_enabled": True, "telegram_chat_id": "", "daily_summary": True})


def save_profile(new_profile=None):
    if new_profile is not None:
        st.session_state.profile = new_profile
    db.save_profile(user["id"], st.session_state.profile)


def dashboard():
    meds = db.list_medications(user["id"])
    driving_data = profile.get("driving", {})
    english_data = profile.get("english", {})
    score = ai.final_score(profile, len(meds))
    st.markdown(f"""
    <div class='hero'>
      <div class='hero-grid'>
        <div>
          <h1>🚀 {APP_NAME}</h1>
          <p>Bản Production: đăng nhập thật, database thật, nhắc thuốc ngoài app, module gọn, AI gợi ý toàn hệ thống, sẵn sàng deploy Streamlit Cloud.</p>
          <span class='pill green'>v{APP_VERSION}</span><span class='pill blue'>{user['email']}</span><span class='pill purple'>Final Score {score}/100</span>
        </div>
        <div class='phone-panel'><div class='road'><div class='drive-car'>🚗</div><div class='road-lane'></div><div class='road-line'></div></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class='fin-grid'>
      <div class='fin-card'>
        <div class='fin-label'>Production Portfolio</div>
        <div class='fin-big'>{score}/100</div>
        <div class='muted'>Điểm tổng hợp từ tiến độ học lái, tiếng Anh, nhắc thuốc và cấu hình riêng tư.</div>
        <div class='action-row'><div class='action-chip'>🚗 Driving</div><div class='action-chip'>🇬🇧 English</div><div class='action-chip'>💊 Care</div><div class='action-chip'>🔐 Database</div><div class='action-chip'>🤖 AI Suggest</div></div>
      </div>
      <div class='fin-card'>
        <div class='fin-label'>Account</div>
        <h3>{user.get('display_name','Bạn')}</h3>
        <p class='muted'>{user['email']}</p>
        <p class='muted'>Dữ liệu được tách theo tài khoản đăng nhập.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: ui.metric_card("Bài lái xe", len(driving_data.get("completed", [])), "đã hoàn thành")
    with c2: ui.metric_card("Quiz lái", len(driving_data.get("quiz_history", [])), "lượt")
    with c3: ui.metric_card("English words", len(english_data.get("learned_words", [])), "đã học")
    with c4: ui.metric_card("Thuốc", len(meds), "đang theo dõi")
    st.markdown("## 🤖 AI gợi ý hôm nay")
    suggestions = ai.offline_suggestions(profile, len(meds))
    cols = st.columns(len(suggestions[:4]))
    icons = ["🧠", "🇬🇧", "💊", "🔐"]
    for col, icon, text in zip(cols, icons, suggestions[:4]):
        with col: ui.card(icon, "Gợi ý", text)
    ui.speak_button(". ".join(suggestions), "🔊 Nghe gợi ý hôm nay", key="daily_suggest")
    st.markdown("## 🛡️ Stability Pack")
    cols_stab = st.columns(3)
    with cols_stab[0]: ui.card("🛡️", "Điều khoản rõ ràng", "Có trang lưu ý an toàn cho thuốc, video, dữ liệu riêng và học lái xe.")
    with cols_stab[1]: ui.card("🧪", "Checklist test", "Test đăng nhập, Supabase, nhắc thuốc, quiz, backup và GitHub Actions trước khi public.")
    with cols_stab[2]: ui.card("🚀", "Deploy guide", "Hướng dẫn deploy nằm ngay trong app để bạn không cần mở file README liên tục.")
    st.markdown("## 🖼️ Hình động hướng dẫn nhanh")
    ui.lane_svg()


def ai_center():
    st.title("🤖 AI Suggestion Center")
    st.caption("Mặc định dùng AI nội bộ/offline-first: trả lời thông minh bằng dữ liệu trong app + template + cache, không tốn API.")
    module = st.selectbox("Bạn muốn AI gợi ý cho mục nào?", ["Tổng quan hôm nay", "Học lái xe", "Học tiếng Anh", "Nhắc thuốc cho mẹ", "TikTok hợp lệ", "Sao lưu & riêng tư"])
    extra = st.text_area("Thông tin thêm", placeholder="Ví dụ: Tôi yếu phần chuyển làn, mẹ hay quên thuốc buổi tối...", height=100)
    st.info(f"Chế độ hiện tại: AI_MODE={AI_MODE} · USE_EXTERNAL_AI={USE_EXTERNAL_AI}. Nếu để offline/false thì không tốn API.")
    if st.button("✨ Tạo gợi ý miễn phí"):
        result = ai.internal_ai_response(module, extra, profile, len(db.list_medications(user["id"])))
        st.markdown(f"<div class='panel'><pre style='white-space:pre-wrap;font-family:inherit'>{result}</pre></div>", unsafe_allow_html=True)
        profile.setdefault("ai_notes", []).append({"time": datetime.now().isoformat(timespec="seconds"), "module": module, "result": result, "extra": extra, "engine": "internal_offline"})
        save_profile(profile)

    with st.expander("⚙️ Dùng API ngoài khi thật sự cần"):
        st.warning("API ngoài mặc định bị tắt để không phát sinh chi phí. Chỉ bật nếu bạn chủ động cấu hình USE_EXTERNAL_AI=true và đặt giới hạn số lần gọi.")
        if st.button("Thử gọi API ngoài có kiểm soát"):
            prompt = f"Module: {module}. Thông tin: {extra}. Hãy gợi ý ngắn gọn."
            result = ai.gemini_response(prompt)
            st.write(result)


def internal_api_page():
    st.title("🧠 API nội bộ tiết kiệm")
    st.caption("Nâng cấp để app trả lời thông minh hơn mà không tốn Google/OpenAI/Gemini API mặc định.")
    status = ai.api_usage_status()
    c1, c2, c3, c4 = st.columns(4)
    with c1: ui.metric_card("AI mode", status["ai_mode"], "offline là miễn phí")
    with c2: ui.metric_card("External API", "ON" if status["use_external_ai"] else "OFF", "mặc định nên OFF")
    with c3: ui.metric_card("Cache", status["cache_items"], "phản hồi đã lưu")
    with c4: ui.metric_card("Google key", "Có" if status["google_key_configured"] else "Không", "không bắt buộc")

    st.markdown("""
    ### Cách app trả lời thông minh mà không tốn API
    1. Đọc dữ liệu hồ sơ: quiz sai, từ đã học, thuốc đang theo dõi, lịch sử học.  
    2. Nhận diện chủ đề: lái xe, tiếng Anh, thuốc, TikTok, backup, Supabase.  
    3. Sinh gợi ý bằng bộ luật nội bộ + template hướng dẫn chi tiết.  
    4. Lưu cache phản hồi để lần sau dùng lại, nhanh hơn và không gọi API.

    ### Khi nào mới cần API ngoài?
    - Khi muốn AI viết nội dung dài/sáng tạo hơn.
    - Khi muốn trả lời câu hỏi mở hoàn toàn ngoài dữ liệu app.
    - Khi bạn đã đặt ngân sách và bật `USE_EXTERNAL_AI=true`.
    """)

    module = st.selectbox("Test AI nội bộ cho module", ["Học lái xe", "Học tiếng Anh", "Nhắc thuốc cho mẹ", "TikTok hợp lệ", "Sao lưu & riêng tư", "Tổng quan hôm nay"], key="internal_module")
    question = st.text_area("Nhập câu hỏi hoặc tình huống", value="Tôi muốn học nhanh phần chuyển làn và không muốn tốn API.", height=90)
    if st.button("🚀 Tạo câu trả lời nội bộ"):
        st.markdown(ai.internal_ai_response(module, question, profile, len(db.list_medications(user["id"]))), unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 Xóa cache AI nội bộ"):
            n = ai.clear_ai_cache()
            st.success(f"Đã xóa {n} phản hồi cache.")
    with col_b:
        st.download_button("⬇️ Tải trạng thái AI JSON", json.dumps(status, ensure_ascii=False, indent=2), "internal_ai_status.json", "application/json")

    st.markdown("### Secrets khuyến nghị để không tốn API")
    st.code("""AI_MODE = "offline"
USE_EXTERNAL_AI = "false"
AI_CACHE_ENABLED = "true"
MAX_EXTERNAL_AI_CALLS_PER_SESSION = "0"
# GOOGLE_API_KEY có thể để trống nếu không dùng Veo/Gemini
GOOGLE_API_KEY = """"", language="toml")


def final_report():
    st.title("📊 Production Report")
    data = db.export_user_data(user["id"])
    score = ai.final_score(profile, len(db.list_medications(user["id"])))
    st.metric("Final Score", f"{score}/100")
    report = {
        "user": {"email": user["email"], "display_name": user.get("display_name")},
        "score": score,
        "suggestions": ai.offline_suggestions(profile, len(db.list_medications(user["id"]))),
        "data_snapshot": data,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
    st.download_button("⬇️ Tải báo cáo JSON", json.dumps(report, ensure_ascii=False, indent=2), "autolearn_production_report.json", "application/json")
    st.json({"score": score, "suggestions": report["suggestions"]})


with st.sidebar:
    st.markdown("## 🚀 AutoLearn v15.2")
    st.caption("Production · Offline AI nội bộ · Không tốn API mặc định")
    st.markdown(f"**{user.get('display_name','Bạn')}**  \\n{user['email']}")
    page = st.radio("Đi tới", [
        "🏠 Production Dashboard",
        "🤖 AI Suggestion Center",
        "🧠 API nội bộ tiết kiệm",
        "🚗 Học lái xe",
        "🧪 Quiz lái xe",
        "🇬🇧 English Pro",
        "🧪 English Quiz",
        "💊 Nhắc thuốc Production",
        "🩺 Sức khỏe & báo cáo",
        "🎬 Google Veo",
        "📥 TikTok Downloader",
        "📊 Production Report",
        "🛡️ Stability Hub",
        "🧪 Checklist test",
        "👥 Test 2 tài khoản",
        "🚀 Hướng dẫn deploy",
        "🧯 Trung tâm lỗi",
        "📤 Sao lưu & dữ liệu",
        "⚙️ Production Settings",
    ])
    st.divider()
    if st.button("💾 Lưu profile"):
        save_profile(profile); st.success("Đã lưu.")
    if st.button("🚪 Đăng xuất"):
        logout()

if page == "🏠 Production Dashboard":
    dashboard()
elif page == "🤖 AI Suggestion Center":
    ai_center()
elif page == "🧠 API nội bộ tiết kiệm":
    internal_api_page()
elif page == "🚗 Học lái xe":
    driving.render_dashboard(profile, save_profile)
elif page == "🧪 Quiz lái xe":
    driving.render_quiz(profile, save_profile)
elif page == "🇬🇧 English Pro":
    english.render(profile, save_profile)
elif page == "🧪 English Quiz":
    english.render_quiz(profile, save_profile)
elif page == "💊 Nhắc thuốc Production":
    medicine.render_medicine(db, user, profile, save_profile)
elif page == "🩺 Sức khỏe & báo cáo":
    medicine.render_health(db, user)
elif page == "🎬 Google Veo":
    media_tools.render_veo()
elif page == "📥 TikTok Downloader":
    media_tools.render_tiktok()
elif page == "📊 Production Report":
    final_report()
elif page == "🛡️ Stability Hub":
    stability.render_stability_hub(db, user, profile)
elif page == "🧪 Checklist test":
    stability.render_test_checklist(db, user, profile)
elif page == "👥 Test 2 tài khoản":
    stability.render_two_account_test(db, user)
elif page == "🚀 Hướng dẫn deploy":
    stability.render_deploy_guide()
elif page == "🧯 Trung tâm lỗi":
    stability.render_error_center()
elif page == "📤 Sao lưu & dữ liệu":
    backup.render(db, user, profile, save_profile)
elif page == "⚙️ Production Settings":
    settings.render()

st.divider()
st.caption("AutoLearn Ultra Production v15.2 Smart Offline AI · Tách module · Đăng nhập thật · Database thật · Reminder worker ngoài app · Deploy-ready.")
