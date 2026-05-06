import json
from datetime import datetime

import streamlit as st

from modules import ai, backup, driving, english, medicine, settings, stability, ui, official_exam, push_notifications, mobile_pro, performance, health_check, terms_privacy, public_safe, admin_mini, deploy_hotfix
from modules.auth import current_user, logout, render_auth_gate
from modules.db import get_db
from modules.config import APP_NAME, APP_VERSION

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
profile.setdefault("performance", {"mode": "balanced", "mobile_first": True, "animations": "reduced", "quiz_page_size": 10, "lazy_media_tools": True})
performance.apply_performance_style(profile)


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
          <p>Bản v15.8.2 Public Safe Release: thêm Terms & Privacy, Admin mini dashboard, kiểm tra sâu bộ 600 câu, công cụ 60 câu điểm liệt và mobile public an toàn.</p>
          <span class='pill green'>v{APP_VERSION}</span><span class='pill blue'>{user['email']}</span><span class='pill purple'>Final Score {score}/100</span>
        </div>
        <div class='phone-panel'><div class='road'><div class='drive-car'>🚗</div><div class='road-lane'></div><div class='road-line'></div></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class='fin-grid'>
      <div class='fin-card'>
        <div class='fin-label'>Public Safe Portfolio</div>
        <div class='fin-big'>{score}/100</div>
        <div class='muted'>Điểm tổng hợp từ tiến độ học lái, tiếng Anh, nhắc thuốc và cấu hình riêng tư.</div>
        <div class='action-row'><div class='action-chip'>🛡️ Terms</div><div class='action-chip'>👑 Admin Mini</div><div class='action-chip'>🚨 60 câu điểm liệt</div><div class='action-chip'>📱 Public mobile</div><div class='action-chip'>🧯 Hotfix</div></div>
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
    with c1: ui.metric_card("Module lái xe", len(driving_data.get("completed", [])), "đã hoàn thành")
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
    st.markdown("## 🖼️ Minh họa nhanh nổi bật")
    ui.lane_svg()
    st.markdown("<div class='deploy-note'><b>☁️ Streamlit Cloud tối ưu:</b> bản này đã tinh gọn khởi động, giảm phụ thuộc không cần thiết ở giao diện chính, bổ sung cấu hình .streamlit phù hợp và tài liệu deploy nhanh ngay trong gói.</div>", unsafe_allow_html=True)


def ai_center():
    st.title("🤖 AI Suggestion Center")
    st.caption("Trung tâm gợi ý cho tất cả ứng dụng. Có chế độ offline và Gemini nếu cấu hình GOOGLE_API_KEY.")
    module = st.selectbox("Bạn muốn AI gợi ý cho mục nào?", ["Tổng quan hôm nay", "Học lái xe", "Học tiếng Anh", "Nhắc thuốc cho mẹ", "TikTok hợp lệ", "Sao lưu & riêng tư"])
    extra = st.text_area("Thông tin thêm", placeholder="Ví dụ: Tôi yếu phần chuyển làn, mẹ hay quên thuốc buổi tối...", height=100)
    if st.button("✨ Tạo gợi ý"):
        base = ai.offline_suggestions(profile, len(db.list_medications(user["id"])))
        prompt = f"Bạn là trợ lý học tập và chăm sóc gia đình. Module: {module}. Profile JSON: {json.dumps(profile, ensure_ascii=False)[:3000]}. Thông tin thêm: {extra}. Hãy gợi ý ngắn gọn, dễ làm, tiếng Việt."
        result = ai.gemini_response(prompt)
        if result.startswith("Chưa cấu hình") or result.startswith("Không gọi"):
            result = "Gợi ý offline:\n" + "\n".join([f"- {x}" for x in base]) + f"\n\nRiêng cho {module}: hãy chọn một việc nhỏ có thể làm trong 10 phút và lưu lại kết quả."
        st.markdown(f"<div class='panel'><pre style='white-space:pre-wrap;font-family:inherit'>{result}</pre></div>", unsafe_allow_html=True)
        profile.setdefault("ai_notes", []).append({"time": datetime.now().isoformat(timespec="seconds"), "module": module, "result": result, "extra": extra})
        save_profile(profile)


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
    st.markdown("## 🚀 AutoLearn v15.8.1")
    st.caption("Performance · Stability · Lazy Load · Mobile")
    st.markdown(f"**{user.get('display_name','Bạn')}**  \\n{user['email']}")
    page = st.radio("Đi tới", [
        "🏠 Production Dashboard",
        "🤖 AI Suggestion Center",
        "🚗 Driving Academy Master",
        "🧪 Driving Quiz Master",
        "🪪 Bộ 600 câu chính thức",
        "🇬🇧 English Master A1–B2",
        "🧪 English Quiz Master",
        "💊 Nhắc thuốc Production",
        "🔔 Push Notification",
        "📱 Mobile Pro Mode",
        "⚡ Performance Mode",
        "🛡️ Terms & Privacy",
        "👑 Admin Mini Dashboard",
        "🛡️ Public Safe Center",
        "🧯 Deploy Hotfix Guide",
        "🩺 App Health Check",
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
elif page == "🚗 Driving Academy Master":
    driving.render_dashboard(profile, save_profile)
elif page == "🧪 Driving Quiz Master":
    driving.render_quiz(profile, save_profile)
elif page == "🪪 Bộ 600 câu chính thức":
    official_exam.render(profile, save_profile)
elif page == "🇬🇧 English Master A1–B2":
    english.render(profile, save_profile)
elif page == "🧪 English Quiz Master":
    english.render_quiz(profile, save_profile)
elif page == "💊 Nhắc thuốc Production":
    medicine.render_medicine(db, user, profile, save_profile)
elif page == "🔔 Push Notification":
    push_notifications.render(profile, save_profile)
elif page == "📱 Mobile Pro Mode":
    mobile_pro.render(profile, save_profile)
elif page == "⚡ Performance Mode":
    performance.render(profile, save_profile)
elif page == "🛡️ Terms & Privacy":
    terms_privacy.render(profile, save_profile)
elif page == "👑 Admin Mini Dashboard":
    admin_mini.render(db, user, profile)
elif page == "🛡️ Public Safe Center":
    public_safe.render(profile, save_profile)
elif page == "🧯 Deploy Hotfix Guide":
    deploy_hotfix.render()
elif page == "🩺 App Health Check":
    health_check.render(db, user, profile)
elif page == "🩺 Sức khỏe & báo cáo":
    medicine.render_health(db, user)
elif page == "🎬 Google Veo":
    try:
        from modules import media_tools as _media_tools
        _media_tools.render_veo()
    except Exception as exc:
        st.error("Không mở được Google Veo. Chức năng này chỉ tải khi bạn vào trang này để không làm chậm app chính.")
        st.caption(str(exc))
elif page == "📥 TikTok Downloader":
    try:
        from modules import media_tools as _media_tools
        _media_tools.render_tiktok()
    except Exception as exc:
        st.error("Không mở được TikTok Downloader. Chức năng này chỉ tải khi bạn vào trang này để không làm chậm app chính.")
        st.caption(str(exc))
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
st.caption("AutoLearn v15.8.2 · Public Safe Release · Terms & Privacy · Admin Mini · 60 Critical Manager · Mobile Safe · Hotfix Guide.")
