import json
from datetime import datetime
from typing import Dict, Any

import streamlit as st

from . import ui
from .db import AppDatabase

TERMS = [
    ("Thông tin học lái xe", "Nội dung trong app dùng để học và ôn tập. Khi tham gia giao thông thực tế, hãy tuân thủ luật hiện hành, biển báo ngoài đường và hướng dẫn của giáo viên/đơn vị đào tạo."),
    ("Nhắc thuốc", "App hỗ trợ nhắc lịch và ghi nhận, không thay thế bác sĩ/dược sĩ. Không tự ý đổi liều, ngừng thuốc hoặc uống bù nếu chưa có hướng dẫn chuyên môn."),
    ("Sức khỏe", "Các chỉ số sức khỏe chỉ dùng để ghi chú cá nhân/gia đình. Khi có triệu chứng bất thường, hãy liên hệ bác sĩ hoặc cơ sở y tế."),
    ("Google Veo", "Tạo video từ ảnh cần tuân thủ điều khoản của Google và quyền sử dụng hình ảnh. Không dùng ảnh của người khác khi chưa được phép."),
    ("TikTok Downloader", "Chỉ tải video bạn sở hữu hoặc được chủ sở hữu cho phép. Không dùng để vi phạm bản quyền, quyền riêng tư hoặc điều khoản nền tảng."),
    ("Dữ liệu riêng", "Mỗi tài khoản có dữ liệu riêng trong database. Không chia sẻ mật khẩu, service key, SMTP password hoặc token nhắc thuốc."),
]

TEST_CHECKLIST = [
    ("Tạo tài khoản mới", "Đăng ký bằng email test, mật khẩu ít nhất 8 ký tự, đăng nhập được."),
    ("Đăng nhập lại", "Đăng xuất rồi đăng nhập lại, profile vẫn còn đúng."),
    ("Thêm thuốc", "Thêm 1 thuốc có giờ uống gần hiện tại, kiểm tra thuốc xuất hiện ở lịch hôm nay."),
    ("Ghi nhận liều", "Bấm Đã uống/Uống trễ/Bỏ qua và kiểm tra dữ liệu vẫn lưu sau refresh."),
    ("Ghi sức khỏe", "Thêm một bản ghi huyết áp/mạch/ghi chú và kiểm tra trong bảng lịch sử."),
    ("Quiz lái xe", "Làm 5 câu, cố tình sai 1 câu để kiểm tra wrong bank."),
    ("English Quiz", "Làm quiz tiếng Anh và kiểm tra lịch sử điểm."),
    ("Backup JSON", "Tải backup JSON về máy, mở file kiểm tra có profile/medications/health_logs."),
    ("Supabase", "Mở Supabase Table Editor, kiểm tra users/profiles/medications có dữ liệu."),
    ("GitHub Actions", "Vào tab Actions, chạy workflow reminder thủ công và xem log."),
]

DEPLOY_STEPS = [
    "Tạo Supabase project, sau đó chạy file sql/supabase_schema.sql trong SQL Editor.",
    "Upload toàn bộ thư mục app lên GitHub, giữ nguyên cấu trúc modules/, scripts/, sql/, .streamlit/.",
    "Vào Streamlit Cloud → New app → chọn repo → Main file path là app.py.",
    "Trong Streamlit Secrets, dán DB_BACKEND=supabase, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY và các SMTP/Telegram secrets nếu dùng nhắc thuốc ngoài app.",
    "Bấm Deploy/Reboot, đăng ký tài khoản test đầu tiên trong app.",
    "Vào GitHub repo → Settings → Secrets and variables → Actions để thêm cùng các secrets cho reminder worker.",
    "Vào GitHub Actions, chạy medicine-reminders workflow thủ công một lần để kiểm tra log.",
]

ERROR_GUIDE = [
    ("App báo lỗi database", "Kiểm tra DB_BACKEND, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY trong Streamlit Secrets. Nếu chưa cấu hình Supabase, app sẽ chạy SQLite local."),
    ("Không đăng ký được", "Kiểm tra email đúng định dạng, mật khẩu ít nhất 8 ký tự. Nếu email đã tồn tại, dùng email khác hoặc đăng nhập."),
    ("Không gửi email nhắc thuốc", "Kiểm tra SMTP_USER, SMTP_PASSWORD là app password, SMTP_HOST/PORT đúng và workflow GitHub Actions có secrets."),
    ("Telegram không gửi", "Kiểm tra TELEGRAM_BOT_TOKEN và telegram_chat_id trong profile. Người nhận cần start bot trước."),
    ("Veo không chạy", "Kiểm tra GOOGLE_API_KEY, gói google-genai và quota/tài khoản Google."),
    ("TikTok không tải", "Một số video bị riêng tư/giới hạn khu vực/thay đổi cơ chế. Chỉ thử với video bạn có quyền tải."),
    ("Streamlit deploy lỗi packages", "Kiểm tra requirements.txt và packages.txt. Nếu log báo thiếu ffmpeg, giữ file packages.txt trong repo."),
]


def render_terms() -> None:
    st.title("🛡️ Điều khoản & lưu ý an toàn")
    st.caption("Trang này giúp app rõ ràng hơn trước khi dùng thật hoặc public link cho người khác.")
    st.warning("Quan trọng: app hỗ trợ học tập, ghi chú và nhắc lịch; không thay thế chuyên gia pháp lý, bác sĩ, dược sĩ hoặc điều khoản của nền tảng bên thứ ba.")
    for title, body in TERMS:
        st.markdown(f"<div class='panel'><h3>{title}</h3><p class='muted'>{body}</p></div>", unsafe_allow_html=True)
    st.markdown("### Xác nhận khuyến nghị")
    st.checkbox("Tôi hiểu phần nhắc thuốc không thay thế bác sĩ/dược sĩ.")
    st.checkbox("Tôi hiểu TikTok Downloader chỉ dùng cho nội dung có quyền tải.")
    st.checkbox("Tôi sẽ không đưa API key/service role key lên GitHub công khai.")
    ui.speak_button("Lưu ý quan trọng: ứng dụng hỗ trợ học tập, nhắc lịch và ghi chú. Không tự ý đổi liều thuốc, không dùng công cụ tải video để vi phạm bản quyền hoặc quyền riêng tư.", "🔊 Nghe lưu ý", key="terms_voice")


def render_test_checklist(db: AppDatabase, user: Dict[str, Any], profile: Dict[str, Any]) -> None:
    st.title("🧪 Checklist test trước khi public")
    st.caption("Dùng trang này để kiểm tra ổn định trước khi gửi link cho người khác.")
    completed = 0
    for i, (title, desc) in enumerate(TEST_CHECKLIST, 1):
        checked = st.checkbox(f"{i}. {title}", help=desc, key=f"stability_check_{i}")
        if checked:
            completed += 1
        st.caption(desc)
    percent = round(completed / len(TEST_CHECKLIST) * 100)
    st.progress(percent / 100)
    st.metric("Mức sẵn sàng", f"{percent}%", f"{completed}/{len(TEST_CHECKLIST)} bước")
    if percent >= 80:
        st.success("App đã khá sẵn sàng để public. Hãy test thêm 2 tài khoản nếu có dữ liệu nhạy cảm.")
    else:
        st.info("Nên hoàn thành ít nhất 80% checklist trước khi public link.")
    snapshot = {
        "checked": completed,
        "total": len(TEST_CHECKLIST),
        "percent": percent,
        "user": user.get("email"),
        "db_mode": getattr(db, "mode", "unknown"),
        "profile_keys": sorted(list(profile.keys())),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
    st.download_button("⬇️ Tải kết quả checklist JSON", json.dumps(snapshot, ensure_ascii=False, indent=2), "autolearn_stability_check.json", "application/json")


def render_two_account_test(db: AppDatabase, user: Dict[str, Any]) -> None:
    st.title("👥 Test 2 tài khoản")
    st.caption("Trang hướng dẫn test quyền riêng tư: tài khoản A không được thấy dữ liệu của tài khoản B.")
    st.markdown("""
    ### Cách test nhanh
    1. Tài khoản A: thêm một thuốc tên `TEST_A_PRIVATE` và lưu profile.
    2. Đăng xuất.
    3. Tạo tài khoản B bằng email khác.
    4. Kiểm tra tài khoản B **không thấy** thuốc `TEST_A_PRIVATE`.
    5. Tài khoản B thêm thuốc `TEST_B_PRIVATE`.
    6. Đăng nhập lại A, kiểm tra A **không thấy** `TEST_B_PRIVATE`.
    """)
    meds = db.list_medications(user["id"], active_only=False)
    st.markdown("### Dữ liệu tài khoản hiện tại")
    st.write({"email": user.get("email"), "user_id": user.get("id"), "medications_count": len(meds), "db_mode": getattr(db, "mode", "unknown")})
    if meds:
        st.dataframe([{"name": m.get("name"), "dose": m.get("dose"), "active": m.get("active")} for m in meds], use_container_width=True, hide_index=True)
    st.info("Không cần gửi user_id hoặc dữ liệu thật cho ai. Chỉ cần bạn xác nhận dữ liệu không bị lẫn giữa hai tài khoản.")


def render_deploy_guide() -> None:
    st.title("🚀 Hướng dẫn deploy trong app")
    st.caption("Các bước ngắn gọn để deploy bản Production lên Streamlit Cloud.")
    for i, step in enumerate(DEPLOY_STEPS, 1):
        st.markdown(f"<div class='panel'><h3>Bước {i}</h3><p class='muted'>{step}</p></div>", unsafe_allow_html=True)
    st.markdown("### Mẫu Streamlit Secrets")
    st.code('''DB_BACKEND = "supabase"
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "your_service_role_key"
GOOGLE_API_KEY = "optional"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USER = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
SMTP_FROM = "your_email@gmail.com"

TELEGRAM_BOT_TOKEN = "optional"
REMINDER_LOOKAHEAD_MIN = "15"''', language="toml")
    st.warning("Không commit Secrets vào GitHub. Chỉ dán vào Streamlit Secrets và GitHub Actions Secrets.")


def render_performance() -> None:
    st.title("⚡ Tối ưu tốc độ & ổn định")
    st.caption("Các gợi ý nhỏ giúp app mượt hơn khi deploy Streamlit Cloud.")
    st.markdown("""
    ### Đã tối ưu trong v15.1
    - Code được tách module, dễ sửa và giảm rủi ro lỗi dây chuyền.
    - Database adapter được dùng lại trong phiên app.
    - Dữ liệu lớn không nhồi hết vào dashboard.
    - Các hình động chỉ render ở những trang cần thiết.

    ### Khi app bắt đầu chậm, nên làm
    - Giảm số SVG/animation trên Dashboard.
    - Không hiển thị toàn bộ lịch sử log quá dài, chỉ lấy 100–1000 dòng mới nhất.
    - Dùng Supabase thay vì SQLite khi có nhiều người dùng.
    - Tránh upload video/ảnh quá lớn lên session.
    - Tách thêm static assets nếu muốn làm UI rất nặng.
    """)
    st.markdown("### Checklist mượt")
    st.checkbox("Không mở quá nhiều animation trên trang đầu.")
    st.checkbox("Supabase đã bật khi deploy nhiều người dùng.")
    st.checkbox("Video TikTok/Veo chỉ xử lý khi người dùng bấm nút, không tự chạy.")
    st.checkbox("Dữ liệu backup tải theo yêu cầu, không export tự động mỗi lần rerun.")


def render_error_center() -> None:
    st.title("🧯 Trung tâm lỗi & khắc phục")
    st.caption("Thông báo lỗi thân thiện hơn để bạn tự xử lý nhanh khi deploy.")
    for title, fix in ERROR_GUIDE:
        st.markdown(f"<div class='panel'><h3>{title}</h3><p class='muted'>{fix}</p></div>", unsafe_allow_html=True)
    st.markdown("### Cách gửi lỗi để kiểm tra")
    st.info("Chụp màn hình log lỗi nhưng che API key, service role key, mật khẩu SMTP, token Telegram trước khi gửi.")


def render_stability_hub(db: AppDatabase, user: Dict[str, Any], profile: Dict[str, Any]) -> None:
    st.title("🛡️ Stability Hub v15.1")
    st.caption("Trung tâm ổn định: điều khoản, checklist test, test 2 tài khoản, deploy guide, tối ưu tốc độ và khắc phục lỗi.")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ui.metric_card("Backend", getattr(db, "mode", "unknown"), "database mode")
    with c2:
        ui.metric_card("User", user.get("email", ""), "đang đăng nhập")
    with c3:
        ui.metric_card("Profile keys", len(profile.keys()), "mục dữ liệu")
    with c4:
        ui.metric_card("Ready", "15.1", "Stability Pack")
    tabs = st.tabs(["🛡️ Điều khoản", "🧪 Checklist", "👥 2 tài khoản", "🚀 Deploy", "⚡ Tốc độ", "🧯 Lỗi"])
    with tabs[0]:
        render_terms()
    with tabs[1]:
        render_test_checklist(db, user, profile)
    with tabs[2]:
        render_two_account_test(db, user)
    with tabs[3]:
        render_deploy_guide()
    with tabs[4]:
        render_performance()
    with tabs[5]:
        render_error_center()
