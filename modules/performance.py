from __future__ import annotations

from typing import Dict, Any
import streamlit as st


def ensure_performance_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    perf = profile.setdefault("performance", {})
    perf.setdefault("mode", "balanced")  # light / balanced / full
    perf.setdefault("mobile_first", True)
    perf.setdefault("animations", "reduced")
    perf.setdefault("quiz_page_size", 10)
    perf.setdefault("lazy_media_tools", True)
    return perf


def apply_performance_style(profile: Dict[str, Any]) -> None:
    perf = ensure_performance_profile(profile)
    mode = perf.get("mode", "balanced")
    mobile_first = perf.get("mobile_first", True)
    reduce_motion = mode == "light" or perf.get("animations") == "reduced"
    css = """
    <style>
      .perf-badge{display:inline-block;padding:.35rem .7rem;border-radius:999px;background:#0f233f;border:1px solid #25436b;color:#dbeafe;font-weight:800;margin:.12rem;}
      .mobile-quick{position:sticky;top:0;z-index:999;background:rgba(5,10,19,.88);backdrop-filter:blur(8px);border:1px solid #1f2b42;border-radius:18px;padding:.5rem;margin-bottom:.75rem;}
      .friendly-error{border:1px solid #7f1d1d;background:#2a1118;border-radius:22px;padding:1rem;color:#fecaca;}
      .health-ok{border:1px solid #14532d;background:#0d2216;border-radius:18px;padding:.8rem}.health-warn{border:1px solid #854d0e;background:#261a0a;border-radius:18px;padding:.8rem}.health-bad{border:1px solid #7f1d1d;background:#2a1118;border-radius:18px;padding:.8rem}
      .small-card{border:1px solid #1f2b42;background:#0d1628;border-radius:18px;padding:.85rem;margin:.35rem 0;}
    """
    if mobile_first:
        css += """
        @media(max-width:780px){
          .main .block-container{padding-left:.55rem!important;padding-right:.55rem!important;padding-top:.55rem!important;}
          h1{font-size:1.55rem!important} h2{font-size:1.28rem!important} h3{font-size:1.1rem!important}
          .card,.panel,.fin-card,.glass-card{border-radius:18px!important;padding:.78rem!important;}
          .stButton>button,.stDownloadButton>button{min-height:44px!important;width:100%;}
          div[data-testid="stSidebar"]{width:18rem!important;}
          .stTabs [data-baseweb="tab"]{padding:.38rem .55rem!important;font-size:.86rem!important;}
          .element-container:has(iframe){max-height:230px;overflow:hidden;}
        }
        """
    if reduce_motion:
        css += """
        *{scroll-behavior:auto!important;}
        .drive-car,.road-line,.hero:before{animation:none!important;}
        @media (prefers-reduced-motion: reduce){*{animation:none!important;transition:none!important}}
        """
    if mode == "light":
        css += """
        .hero-grid{grid-template-columns:1fr!important}.road{display:none}.phone-panel{display:none}.fin-grid{grid-template-columns:1fr!important}.action-row{gap:6px}.action-chip{padding:.45rem .7rem!important;font-size:.84rem!important}
        """
    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)


def render_mobile_quick_bar() -> None:
    st.markdown("""
    <div class='mobile-quick'>
      <span class='perf-badge'>⚡ Lazy load</span>
      <span class='perf-badge'>📱 Mobile first</span>
      <span class='perf-badge'>🩺 Health check</span>
      <span class='perf-badge'>🧯 Friendly errors</span>
    </div>
    """, unsafe_allow_html=True)


def render(profile: Dict[str, Any], save_cb) -> None:
    st.title("⚡ Performance & Mobile Mode")
    st.caption("Điều chỉnh độ mượt của app: chế độ nhẹ, mobile-first, giảm animation và lazy-load các module nặng.")
    st.info("Public Safe khuyến nghị: khi chia sẻ link cho nhiều người, dùng chế độ Nhẹ hoặc Cân bằng, bật Mobile-first và lazy-load Google Veo/TikTok.")
    perf = ensure_performance_profile(profile)
    c1, c2 = st.columns(2)
    with c1:
        mode = st.radio("Chế độ hiệu năng", ["light", "balanced", "full"], index=["light","balanced","full"].index(perf.get("mode", "balanced")), format_func=lambda x: {"light":"⚡ Nhẹ / mượt nhất","balanced":"🚀 Cân bằng","full":"✨ Đầy đủ hình động"}[x])
        mobile_first = st.toggle("📱 Mobile-first", value=bool(perf.get("mobile_first", True)))
    with c2:
        animations = st.radio("Animation", ["reduced", "full"], index=0 if perf.get("animations", "reduced") == "reduced" else 1, format_func=lambda x: "Giảm animation" if x == "reduced" else "Đầy đủ animation")
        quiz_page_size = st.slider("Số câu quiz khuyến nghị mỗi lượt", 5, 20, int(perf.get("quiz_page_size", 10)))
    lazy_media = st.toggle("Không tải Google Veo/TikTok ở app chính, chỉ tải khi mở trang đó", value=bool(perf.get("lazy_media_tools", True)))
    if st.button("💾 Lưu cấu hình hiệu năng"):
        perf.update({"mode": mode, "mobile_first": mobile_first, "animations": animations, "quiz_page_size": quiz_page_size, "lazy_media_tools": lazy_media})
        profile["performance"] = perf
        save_cb(profile)
        st.success("Đã lưu. Hãy Reboot/Rerun app nếu muốn cảm nhận thay đổi rõ hơn.")
    st.markdown("### Gợi ý dùng")
    st.info("Nếu deploy trên Streamlit Cloud và chia sẻ cho nhiều người: chọn **Nhẹ / mượt nhất** hoặc **Cân bằng**, bật Mobile-first và giảm animation.")
    st.markdown("""
    <div class='small-card'><b>Dashboard nhẹ:</b> chỉ tải số liệu cơ bản, không tải Google Veo/TikTok/Bộ 600 câu cho tới khi bạn mở đúng trang.</div>
    <div class='small-card'><b>Mobile tốt hơn:</b> nút to hơn, tab gọn hơn, giảm chiều cao animation để tránh giật trên điện thoại.</div>
    <div class='small-card'><b>Quiz dễ học:</b> nên làm 5–10 câu/lượt trên điện thoại để app nhẹ và người học không mệt.</div>
    """, unsafe_allow_html=True)
