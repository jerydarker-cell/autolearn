from typing import Dict, Any
import streamlit as st
import streamlit.components.v1 as components


def render(profile: Dict[str, Any], save_cb) -> None:
    st.title('📱 Mobile Pro Mode')
    st.caption('Tối ưu giao diện học trên điện thoại: card rõ hơn, nút lớn hơn, luồng học ngắn, checklist 1 tay. Public Mobile Safe: ưu tiên 1 màn hình = 1 việc chính.')
    mobile = profile.setdefault('mobile', {'compact': True, 'large_buttons': True, 'daily_flow': True})
    c1, c2, c3 = st.columns(3)
    with c1: mobile['compact'] = st.toggle('Chế độ gọn', value=mobile.get('compact', True))
    with c2: mobile['large_buttons'] = st.toggle('Nút lớn dễ bấm', value=mobile.get('large_buttons', True))
    with c3: mobile['daily_flow'] = st.toggle('Luồng học mỗi ngày', value=mobile.get('daily_flow', True))
    if st.button('💾 Lưu cấu hình mobile'):
        save_cb(profile)
        st.success('Đã lưu cấu hình mobile.')
    st.markdown('### Mobile learning flow')
    steps = [('1','Xem gợi ý hôm nay','Mở Dashboard, nghe AI gợi ý 30 giây.'),('2','Học 1 bài nhỏ','Chọn 1 module lái xe hoặc 1 bài English.'),('3','Làm 5–10 câu quiz','Ưu tiên câu sai hoặc câu điểm liệt.'),('4','Xem giải thích sai','Đọc đáp án đúng/sai trước khi qua câu tiếp.'),('5','Lưu tiến độ','Lưu profile và backup nếu cần.')]
    for n, title, desc in steps:
        st.markdown(f"<div class='panel' style='margin:.5rem 0'><div style='display:flex;gap:14px;align-items:center'><div style='font-size:2.2rem;font-weight:900;color:#93c5fd'>{n}</div><div><h3 style='margin:0'>{title}</h3><p class='muted' style='margin:.15rem 0'>{desc}</p></div></div></div>", unsafe_allow_html=True)
    components.html('''
    <style>@media(max-width:780px){.stButton button{min-height:46px!important;font-size:16px!important;width:100%!important}.stRadio div[role="radiogroup"]{gap:10px!important}}</style>
    <div style="border:1px solid #1f2b42;border-radius:24px;background:#0e1628;color:#e2e8f0;padding:14px;font-family:Arial"><b>📱 Mobile preview</b><br>Giao diện được tối ưu để học từng phần nhỏ, ít cuộn ngang, nút bấm to và nội dung theo checklist.</div>
    ''', height=120)
