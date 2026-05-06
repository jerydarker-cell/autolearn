
from __future__ import annotations
from typing import Dict, Any
import streamlit as st

from . import ui


def render(profile: Dict[str, Any] | None = None, save_cb=None) -> None:
    st.title("🛡️ Terms & Privacy")
    st.caption("Bản Public Safe: điều khoản, quyền riêng tư và cảnh báo an toàn rõ ràng hơn trước khi chia sẻ link cho người khác.")

    tabs = st.tabs(["📜 Điều khoản sử dụng", "🔐 Quyền riêng tư", "⚕️ Lưu ý sức khỏe", "🚗 Lưu ý học lái", "📥 Video/TikTok", "✅ Xác nhận"])

    with tabs[0]:
        st.markdown("""
        <div class='public-safe-card safe-ok'>
        <h3>📜 Điều khoản sử dụng</h3>
        <p>Ứng dụng AutoLearn hỗ trợ học tập, ôn luyện, nhắc lịch và quản lý tiến độ cá nhân. Ứng dụng không thay thế tài liệu pháp luật chính thức, giáo viên đào tạo, bác sĩ, dược sĩ hoặc chuyên gia có thẩm quyền.</p>
        <ul>
          <li>Người dùng chịu trách nhiệm kiểm tra thông tin quan trọng trước khi áp dụng.</li>
          <li>Không dùng app để vi phạm bản quyền, quyền riêng tư hoặc điều khoản nền tảng khác.</li>
          <li>Không nhập dữ liệu nhạy cảm của người khác nếu chưa được cho phép.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("""
        <div class='public-safe-card safe-ok'>
        <h3>🔐 Chính sách quyền riêng tư tóm tắt</h3>
        <ul>
          <li>Dữ liệu học tập, quiz, thuốc và ghi chú được tách theo tài khoản đăng nhập.</li>
          <li>Không đưa API key, Supabase service role key, SMTP password lên GitHub.</li>
          <li>Nếu dùng Supabase/Streamlit Secrets, hãy lưu key trong mục Secrets, không lưu trong code.</li>
          <li>Khi chia sẻ app, nên test tài khoản A không thấy dữ liệu tài khoản B.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.warning("Nếu app dùng cho người thân, dữ liệu thuốc/sức khỏe là dữ liệu nhạy cảm. Hãy giới hạn quyền truy cập link và dùng mật khẩu mạnh.")

    with tabs[2]:
        st.markdown("""
        <div class='public-safe-card safe-warn'>
        <h3>⚕️ Lưu ý sức khỏe & nhắc thuốc</h3>
        <p>Tính năng nhắc thuốc chỉ hỗ trợ ghi nhớ lịch. Không tự ý đổi thuốc, đổi liều hoặc dừng thuốc dựa trên app.</p>
        <ul>
          <li>Khi có triệu chứng bất thường, hãy liên hệ bác sĩ/dược sĩ.</li>
          <li>Luôn kiểm tra tên thuốc, liều, giờ uống với đơn thuốc thật.</li>
          <li>Thông báo email/Telegram/Web Push có thể bị trễ do mạng hoặc nền tảng.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("""
        <div class='public-safe-card safe-warn'>
        <h3>🚗 Lưu ý học lái xe</h3>
        <p>Bộ 600 câu trong app hỗ trợ ôn tập. Khi đi thi hoặc học chính thức, hãy đối chiếu với tài liệu do cơ quan có thẩm quyền công bố và hướng dẫn của trung tâm đào tạo.</p>
        <ul>
          <li>Không lái xe thật chỉ dựa vào mô phỏng trong app.</li>
          <li>Luôn tuân thủ pháp luật, biển báo, hiệu lệnh người điều khiển giao thông.</li>
          <li>Cần đánh dấu đủ 60 câu điểm liệt nếu có danh sách ID chuẩn.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with tabs[4]:
        st.markdown("""
        <div class='public-safe-card safe-warn'>
        <h3>📥 TikTok / Video downloader</h3>
        <p>Chỉ tải video bạn sở hữu hoặc được chủ sở hữu cho phép. Không dùng để sao chép, phát tán hoặc khai thác nội dung vi phạm bản quyền/quyền riêng tư.</p>
        <p>Tính năng này là tính năng phụ, được lazy-load để không làm chậm app chính.</p>
        </div>
        """, unsafe_allow_html=True)

    with tabs[5]:
        accepted = False
        if profile is not None:
            safe = profile.setdefault("public_safe", {})
            accepted = bool(safe.get("terms_accepted"))
            st.info("Bạn có thể lưu xác nhận cho tài khoản hiện tại.")
            new_val = st.checkbox("Tôi đã đọc và hiểu các điều khoản/lưu ý trên.", value=accepted)
            if st.button("💾 Lưu xác nhận Terms & Privacy"):
                safe["terms_accepted"] = bool(new_val)
                if save_cb:
                    save_cb(profile)
                st.success("Đã lưu xác nhận.")
        else:
            st.info("Trang này có thể chạy độc lập. Khi đăng nhập, app sẽ lưu xác nhận vào profile.")
