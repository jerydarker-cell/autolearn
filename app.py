import base64
import html
import json
import math
import os
import random
import tempfile
import time
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

try:
    from google import genai
    from google.genai import types
except Exception:
    genai = None
    types = None

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="AutoLearn Ultra UI v6",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_VERSION = "6.0 Ultra UI"
BASE_DIR = Path(__file__).resolve().parent
PROGRESS_FILE = BASE_DIR / "autolearn_progress.json"
TODAY = date.today().isoformat()

# =========================================================
# CSS: ULTRA MOBILE UI
# =========================================================
st.markdown(
    """
    <style>
        :root{
            --bg:#f7fbff;--card:#ffffff;--ink:#0f172a;--muted:#64748b;
            --blue:#2563eb;--cyan:#06b6d4;--purple:#7c3aed;--green:#16a34a;--amber:#d97706;--red:#dc2626;
        }
        html,body,[class*="css"]{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
        .stApp{background:
            radial-gradient(circle at 5% 8%, rgba(34,211,238,.18), transparent 24%),
            radial-gradient(circle at 92% 15%, rgba(124,58,237,.16), transparent 22%),
            linear-gradient(180deg,#f8fbff 0%,#eef6ff 100%);}
        .main .block-container{padding-top:1rem;padding-bottom:5rem;max-width:1320px;}
        div[data-testid="stSidebar"]{background:linear-gradient(180deg,#f8fafc 0%,#e0f2fe 100%);border-right:1px solid #dbeafe;}
        .hero{position:relative;overflow:hidden;color:white;border-radius:36px;padding:2rem;margin-bottom:1rem;
            background:radial-gradient(circle at 10% 12%,rgba(34,211,238,.55),transparent 24%),
            radial-gradient(circle at 88% 22%,rgba(167,139,250,.45),transparent 24%),
            linear-gradient(135deg,#0f172a 0%,#1d4ed8 48%,#06b6d4 100%);
            box-shadow:0 26px 70px rgba(15,23,42,.24);}
        .hero h1{font-size:clamp(2rem,4vw,3.4rem);line-height:1.04;margin:0 0 .45rem 0;position:relative;z-index:2;letter-spacing:-.03em;}
        .hero p{max-width:980px;font-size:1.06rem;opacity:.95;position:relative;z-index:2;}
        .hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:1rem;align-items:center;position:relative;z-index:2;}
        .road{position:relative;height:112px;border-radius:24px;overflow:hidden;background:linear-gradient(180deg,rgba(255,255,255,.17),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.18);}
        .road-lane{position:absolute;left:0;right:0;bottom:12px;height:40px;background:#111827;}
        .road-line{position:absolute;left:-20%;bottom:30px;width:150%;height:4px;opacity:.9;background-image:linear-gradient(90deg,transparent 0 5%,white 5% 10%,transparent 10% 20%);background-size:120px 100%;animation:dash 2.2s linear infinite;}
        .drive-car{position:absolute;left:4%;bottom:35px;font-size:2.5rem;filter:drop-shadow(0 10px 14px rgba(0,0,0,.26));animation:drive 6.2s ease-in-out infinite alternate;}
        .float-badge{position:absolute;right:1rem;top:1rem;padding:.42rem .75rem;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.26);border-radius:999px;font-weight:900;animation:pulse 2s ease-in-out infinite;}
        .phone-panel{border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.12);backdrop-filter:blur(12px);border-radius:28px;padding:1rem;}
        .quick-row{display:flex;gap:.55rem;overflow-x:auto;padding:.2rem 0 .8rem 0;}
        .quick-chip{white-space:nowrap;border:1px solid #dbeafe;background:#eff6ff;color:#1d4ed8;padding:.52rem .85rem;border-radius:999px;font-weight:900;box-shadow:0 8px 18px rgba(37,99,235,.08);}
        .card,.soft-card,.metric-card,.sim-card,.glass-card{background:var(--card);border:1px solid #e2e8f0;border-radius:28px;box-shadow:0 16px 38px rgba(15,23,42,.06);}
        .card{padding:1.15rem;height:100%;transition:transform .18s ease,box-shadow .18s ease;}
        .card:hover{transform:translateY(-4px);box-shadow:0 22px 48px rgba(15,23,42,.11);}
        .soft-card{background:#f8fafc;padding:1rem;}
        .glass-card{padding:1rem;background:rgba(255,255,255,.72);backdrop-filter:blur(12px);}
        .metric-card{padding:1rem;background:linear-gradient(180deg,#fff,#f8fafc);}
        .sim-card{padding:1rem;overflow:hidden;}
        .metric-title{color:var(--muted);font-size:.9rem;}
        .metric-value{font-size:1.85rem;font-weight:950;margin:.1rem 0;color:var(--ink);letter-spacing:-.03em;}
        .muted{color:var(--muted);}.big-icon{font-size:2.45rem;line-height:1;margin-bottom:.35rem;}
        .pill{display:inline-block;padding:.36rem .74rem;border-radius:999px;background:#e0f2fe;color:#0369a1;font-weight:900;font-size:.78rem;margin-right:.35rem;margin-bottom:.35rem;}
        .green{background:#dcfce7;color:#166534}.yellow{background:#fef9c3;color:#854d0e}.red{background:#fee2e2;color:#991b1b}.purple{background:#ede9fe;color:#6d28d9}.gray{background:#f1f5f9;color:#334155}.blue{background:#dbeafe;color:#1d4ed8}
        .timer-box{text-align:center;padding:1.3rem;border-radius:30px;background:linear-gradient(135deg,#0f172a,#2563eb);color:white;box-shadow:0 18px 45px rgba(15,23,42,.2);}
        .timer-value{font-size:clamp(2.4rem,6vw,4.2rem);font-weight:950;letter-spacing:.03em;}
        .risk-low{color:#166534;font-weight:950}.risk-mid{color:#a16207;font-weight:950}.risk-high{color:#b91c1c;font-weight:950}
        .achievement{padding:.85rem;border-radius:22px;background:linear-gradient(135deg,#fff7ed,#eff6ff);border:1px solid #e2e8f0;}
        .ai-bubble{padding:1rem;border-radius:24px;background:linear-gradient(135deg,#eef2ff,#f0f9ff);border:1px solid #c7d2fe;}
        .mini-map{border-radius:26px;overflow:hidden;border:1px solid #e2e8f0;background:#fff;}
        .stButton > button,.stDownloadButton > button,.stLinkButton > a{border-radius:999px!important;font-weight:900!important;border:1px solid #cbd5e1!important;}
        @keyframes dash{from{transform:translateX(0)}to{transform:translateX(-120px)}}
        @keyframes drive{from{transform:translateX(0)}to{transform:translateX(min(720px,58vw))}}
        @keyframes pulse{0%,100%{transform:scale(1);opacity:.9}50%{transform:scale(1.07);opacity:1}}
        @keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
        @keyframes rain{from{transform:translateY(-40px);opacity:.15}to{transform:translateY(120px);opacity:.85}}
        @media(max-width:820px){.main .block-container{padding-left:.7rem;padding-right:.7rem}.hero{padding:1.25rem;border-radius:28px}.hero-grid{grid-template-columns:1fr}.card,.soft-card,.metric-card,.sim-card,.glass-card{border-radius:24px}}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# DATA
# =========================================================
LESSONS = [
    {"id":"mindset","icon":"🧠","title":"Tư duy lái phòng vệ","level":"Nền tảng","minutes":25,"summary":"Học cách dự đoán rủi ro trước khi rủi ro xảy ra.","topics":["Quan sát xa","Giữ khoảng cách","Dự đoán nguy hiểm"],"content":"Lái phòng vệ là chủ động nhìn xa, quét rộng, giữ khoảng cách và luôn có phương án thoát. Khi chưa chắc chắn, phản ứng tốt nhất thường là giảm tốc trước."},
    {"id":"signs","icon":"🚦","title":"Biển báo giao thông","level":"Cơ bản","minutes":40,"summary":"Nhận diện biển cấm, nguy hiểm, hiệu lệnh, chỉ dẫn bằng hình vẽ và âm thanh.","topics":["Biển cấm","Biển nguy hiểm","Biển hiệu lệnh","Biển chỉ dẫn"],"content":"Học biển báo theo mẫu: hình dạng → màu sắc → hành động cần làm → lỗi nếu làm sai. Đừng chỉ học tên biển, hãy nhớ hành động cần làm ngoài đường."},
    {"id":"law","icon":"📘","title":"Luật & quyền ưu tiên","level":"Quan trọng","minutes":45,"summary":"Nhường đường, chuyển làn, vượt xe, dừng đỗ, giao lộ.","topics":["Giao lộ","Nhường đường","Vượt xe","Dừng đỗ"],"content":"Khi làm câu hỏi luật, ưu tiên phương án an toàn, đúng quyền ưu tiên, không gây bất ngờ cho phương tiện khác."},
    {"id":"control","icon":"🕹️","title":"Kỹ thuật điều khiển xe","level":"Thực hành","minutes":45,"summary":"Vô lăng, ga, phanh, gương, điểm mù, căn làn.","topics":["Điểm mù","Căn làn","Phanh","Vào cua"],"content":"Công thức chuyển làn: Gương → Xi nhan → Điểm mù → Chuyển làn từ từ → Tắt xi nhan. Không đánh lái gấp khi tốc độ cao."},
    {"id":"weather","icon":"🌧️","title":"Lái xe trời mưa/ban đêm","level":"Nâng cao","minutes":35,"summary":"Xử lý tầm nhìn kém, đường trơn, phản xạ chậm.","topics":["Mưa","Sương mù","Ban đêm","Đèn xe"],"content":"Khi tầm nhìn hoặc độ bám giảm, hãy giảm tốc, tăng khoảng cách, dùng đèn phù hợp và tránh thao tác đột ngột."},
    {"id":"parking","icon":"🅿️","title":"Sa hình & đỗ xe","level":"Ôn thi","minutes":60,"summary":"Đề-pa dốc, ghép xe, vệt bánh xe, đường vuông góc.","topics":["Đề-pa dốc","Ghép xe","Vệt bánh","Vuông góc"],"content":"Học sa hình theo 3 phần: mục tiêu bài → điểm căn → lỗi bị trừ điểm. Tập chậm, chính xác và giữ bình tĩnh."},
    {"id":"maintenance","icon":"🔧","title":"Bảo dưỡng cơ bản","level":"Bổ trợ","minutes":20,"summary":"Lốp, đèn, dầu, nước làm mát, phanh, gạt mưa.","topics":["Lốp","Đèn","Dầu máy","Phanh"],"content":"Trước khi đi xa, kiểm tra lốp, đèn, nhiên liệu, nước làm mát, gạt mưa và quanh xe. Xe tốt giúp lái an toàn hơn."},
]

SIGNS = [
    {"id":"s1","name":"Cấm đi ngược chiều","type":"Biển cấm","symbol":"⛔","meaning":"Không được đi vào theo chiều đặt biển.","action":"Tuyệt đối không đi vào.","tip":"Đỏ + vạch trắng = dừng lại, không vào."},
    {"id":"s2","name":"Cấm rẽ trái","type":"Biển cấm","symbol":"↩️","meaning":"Không được rẽ trái.","action":"Đi theo hướng khác được phép.","tip":"Mũi tên bị cấm nghĩa là hướng đó không được đi."},
    {"id":"s3","name":"Cấm quay đầu","type":"Biển cấm","symbol":"🔄","meaning":"Không được quay đầu xe.","action":"Không quay đầu tại vị trí đặt biển.","tip":"Quay đầu là đổi hướng 180 độ."},
    {"id":"s4","name":"Tốc độ tối đa","type":"Biển cấm","symbol":"50","meaning":"Không vượt quá tốc độ ghi trên biển.","action":"Giữ tốc độ bằng hoặc thấp hơn giới hạn.","tip":"Nhìn số, kiểm tra đồng hồ tốc độ."},
    {"id":"s5","name":"Cấm vượt","type":"Biển cấm","symbol":"🚫","meaning":"Không được vượt xe khác.","action":"Giữ làn, không vượt cho đến khi hết cấm.","tip":"Không đủ an toàn thì không vượt."},
    {"id":"s6","name":"Đường trơn","type":"Biển nguy hiểm","symbol":"〰️","meaning":"Mặt đường dễ trơn trượt.","action":"Giảm tốc, tránh phanh gấp và đánh lái gấp.","tip":"Trơn = thao tác phải mềm."},
    {"id":"s7","name":"Trẻ em","type":"Biển nguy hiểm","symbol":"👧","meaning":"Khu vực có trẻ em qua lại.","action":"Giảm tốc, quan sát hai bên đường.","tip":"Trẻ em có thể băng qua bất ngờ."},
    {"id":"s8","name":"Giao nhau có đèn","type":"Biển nguy hiểm","symbol":"🚥","meaning":"Sắp tới giao lộ có tín hiệu đèn.","action":"Giảm tốc, quan sát tín hiệu.","tip":"Gặp giao lộ là giảm tốc trước."},
    {"id":"s9","name":"Đường hẹp","type":"Biển nguy hiểm","symbol":"↕️","meaning":"Đường phía trước hẹp.","action":"Giảm tốc, giữ làn chính xác.","tip":"Hẹp thì chậm, không lấn."},
    {"id":"s10","name":"Người đi bộ","type":"Biển nguy hiểm","symbol":"🚶","meaning":"Có người đi bộ qua đường.","action":"Giảm tốc, sẵn sàng nhường đường.","tip":"Gần vạch qua đường phải đề phòng."},
    {"id":"s11","name":"Đi thẳng","type":"Biển hiệu lệnh","symbol":"⬆️","meaning":"Chỉ được đi thẳng.","action":"Không rẽ trái hoặc phải.","tip":"Biển xanh tròn là bắt buộc thực hiện."},
    {"id":"s12","name":"Rẽ phải","type":"Biển hiệu lệnh","symbol":"↪️","meaning":"Phải đi theo hướng rẽ phải.","action":"Rẽ phải theo quy định.","tip":"Hiệu lệnh là phải làm."},
    {"id":"s13","name":"Vòng xuyến","type":"Biển hiệu lệnh","symbol":"🔄","meaning":"Đi theo chiều vòng xuyến.","action":"Nhập vòng xuyến đúng chiều, quan sát xe trong vòng.","tip":"Vòng xuyến: chậm, nhìn, nhường."},
    {"id":"s14","name":"Nơi đỗ xe","type":"Biển chỉ dẫn","symbol":"🅿️","meaning":"Khu vực được phép đỗ xe.","action":"Đỗ xe đúng khu vực và đúng quy định.","tip":"Chỉ dẫn giúp tìm thông tin đường đi."},
    {"id":"s15","name":"Đường một chiều","type":"Biển chỉ dẫn","symbol":"➡️","meaning":"Đường chỉ đi một chiều.","action":"Đi đúng theo chiều mũi tên.","tip":"Mũi tên xanh chỉ hướng được đi."},
    {"id":"s16","name":"Bến xe buýt","type":"Biển chỉ dẫn","symbol":"🚌","meaning":"Khu vực xe buýt dừng đón trả khách.","action":"Quan sát xe buýt và người đi bộ.","tip":"Xe buýt có thể dừng/ra vào bất ngờ."},
    {"id":"s17","name":"Bệnh viện","type":"Biển chỉ dẫn","symbol":"🏥","meaning":"Có cơ sở y tế gần đó.","action":"Chú ý người đi bộ và xe cấp cứu.","tip":"Khu bệnh viện thường đông và cần đi chậm."},
    {"id":"s18","name":"Trạm xăng","type":"Biển chỉ dẫn","symbol":"⛽","meaning":"Phía trước có trạm nhiên liệu.","action":"Chuẩn bị chuyển hướng nếu cần đổ nhiên liệu.","tip":"Quan sát xe ra vào trạm xăng."},
]

QUESTION_BASE = [
    ("Biển báo nguy hiểm thường có hình dạng nào?", ["Tam giác viền đỏ", "Tròn nền xanh", "Vuông nền xanh", "Tròn viền xanh"], "Tam giác viền đỏ", "Biển nguy hiểm dùng hình dạng dễ nhận ra để cảnh báo giảm tốc.", "Biển báo"),
    ("Biển hiệu lệnh thường có đặc điểm nào?", ["Tròn nền xanh", "Tam giác nền vàng", "Vuông nền trắng", "Chữ nhật đỏ"], "Tròn nền xanh", "Biển hiệu lệnh yêu cầu người lái phải thực hiện theo hướng dẫn.", "Biển báo"),
    ("Gặp biển cấm đi ngược chiều, bạn nên làm gì?", ["Đi chậm vào", "Không đi vào", "Bấm còi rồi vào", "Chỉ xe máy bị cấm"], "Không đi vào", "Biển này cấm đi vào theo chiều đặt biển.", "Biển báo"),
    ("Biển chỉ dẫn thường dùng để làm gì?", ["Cung cấp thông tin đường đi", "Cảnh báo nguy hiểm", "Cấm hành vi", "Yêu cầu phanh gấp"], "Cung cấp thông tin đường đi", "Biển chỉ dẫn giúp người lái biết hướng, địa điểm hoặc dịch vụ.", "Biển báo"),
    ("Khi đến giao lộ, phản ứng an toàn đầu tiên là gì?", ["Tăng tốc", "Giảm tốc và quan sát", "Bấm còi liên tục", "Dừng giữa đường"], "Giảm tốc và quan sát", "Giao lộ có nhiều hướng xung đột nên cần giảm tốc trước.", "Luật"),
    ("Khi chuyển làn, thứ tự đúng là gì?", ["Gương → Xi nhan → Điểm mù → Chuyển làn", "Xi nhan rồi chuyển ngay", "Bóp còi rồi lách", "Tăng tốc trước"], "Gương → Xi nhan → Điểm mù → Chuyển làn", "Quy trình này giúp xe khác biết ý định và bạn tránh vùng điểm mù.", "Kỹ thuật"),
    ("Không nên vượt xe ở đâu?", ["Nơi tầm nhìn bị che khuất", "Đường thẳng thoáng", "Nơi cho phép vượt", "Đường vắng"], "Nơi tầm nhìn bị che khuất", "Vượt khi không thấy rõ phía trước rất nguy hiểm.", "Luật"),
    ("Khi trời mưa to, nên làm gì?", ["Giảm tốc và tăng khoảng cách", "Phanh gấp liên tục", "Tắt đèn", "Chạy sát xe trước"], "Giảm tốc và tăng khoảng cách", "Mưa làm giảm tầm nhìn và độ bám đường.", "An toàn"),
    ("Điểm mù là gì?", ["Vùng không nhìn thấy rõ qua gương", "Vùng trước kính lái", "Vị trí đặt biển báo", "Khoảng cách phanh"], "Vùng không nhìn thấy rõ qua gương", "Cần quay đầu kiểm tra nhanh hoặc dùng cảnh báo điểm mù nếu có.", "Kỹ thuật"),
    ("Khoảng cách an toàn giúp gì?", ["Tăng thời gian phản ứng", "Tăng tốc độ xe", "Đỡ cần nhìn gương", "Dễ bấm còi"], "Tăng thời gian phản ứng", "Khoảng cách là vùng đệm khi xe trước phanh gấp.", "An toàn"),
    ("Khi xe trước phanh gấp trên cao tốc, nên làm gì?", ["Phanh có kiểm soát và giữ thẳng lái", "Đánh lái gấp", "Tăng tốc vượt", "Nhắm mắt phanh"], "Phanh có kiểm soát và giữ thẳng lái", "Đổi làn gấp ở tốc độ cao có thể gây mất lái.", "An toàn"),
    ("Đi ban đêm cần chú ý gì?", ["Dùng đèn phù hợp và giảm tốc", "Tắt đèn để tiết kiệm", "Chạy nhanh hơn", "Chỉ nhìn vạch đường"], "Dùng đèn phù hợp và giảm tốc", "Ban đêm tầm nhìn giảm nên cần tốc độ phù hợp.", "An toàn"),
    ("Mục tiêu của điểm căn xe trong sa hình là gì?", ["Tránh cán vạch", "Đi nhanh hơn", "Không cần nhìn gương", "Bỏ qua xi nhan"], "Tránh cán vạch", "Điểm căn giúp giữ xe đúng quỹ đạo.", "Sa hình"),
    ("Lỗi hay gặp ở đề-pa dốc là gì?", ["Tụt dốc hoặc chết máy", "Đi quá thẳng", "Không bật radio", "Rửa kính"], "Tụt dốc hoặc chết máy", "Bài dốc cần phối hợp phanh/côn/ga chính xác.", "Sa hình"),
    ("Trước khi đi xa nên kiểm tra gì?", ["Lốp, đèn, nhiên liệu", "Chỉ ghế ngồi", "Chỉ radio", "Màu xe"], "Lốp, đèn, nhiên liệu", "Kiểm tra cơ bản giúp giảm rủi ro hỏng xe giữa đường.", "Bảo dưỡng"),
    ("Áp suất lốp thấp có thể gây gì?", ["Mòn lốp và kém an toàn", "Xe bay nhanh hơn", "Không ảnh hưởng", "Đèn sáng hơn"], "Mòn lốp và kém an toàn", "Lốp tiếp xúc trực tiếp với mặt đường nên rất quan trọng.", "Bảo dưỡng"),
    ("Nếu nghi ngờ phía trước có nguy hiểm, nên làm gì?", ["Giảm tốc trước", "Tăng tốc", "Đánh lái thử", "Bỏ tay khỏi vô lăng"], "Giảm tốc trước", "Giảm tốc cho bạn thêm thời gian xử lý.", "An toàn"),
    ("Ở vòng xuyến, nên làm gì trước khi nhập vào?", ["Giảm tốc và quan sát xe trong vòng", "Lao vào thật nhanh", "Dừng giữa vòng", "Không cần nhìn gương"], "Giảm tốc và quan sát xe trong vòng", "Vòng xuyến có nhiều hướng di chuyển, cần quan sát kỹ.", "Luật"),
    ("Khi gần trường học, phản ứng nào an toàn?", ["Giảm tốc và đề phòng trẻ em", "Tăng tốc qua nhanh", "Bấm còi liên tục", "Đi sát lề"], "Giảm tốc và đề phòng trẻ em", "Trẻ em có thể băng qua bất ngờ.", "An toàn"),
    ("Khi vào cua, điều gì nên tránh?", ["Đánh lái gấp ở tốc độ cao", "Giảm tốc trước cua", "Nhìn theo hướng cua", "Giữ làn"], "Đánh lái gấp ở tốc độ cao", "Đánh lái gấp dễ gây mất ổn định xe.", "Kỹ thuật"),
]
QUESTIONS = [
    {"id": f"q{i+1}", "question": q, "options": opts, "answer": ans, "explain": exp, "topic": topic}
    for i, (q, opts, ans, exp, topic) in enumerate(QUESTION_BASE)
]

FLASHCARDS = [
    {"id":"f1","topic":"Biển báo","front":"Biển tam giác viền đỏ thường là gì?","back":"Biển nguy hiểm/cảnh báo. Gặp biển này nên giảm tốc và quan sát."},
    {"id":"f2","topic":"Kỹ thuật","front":"Công thức chuyển làn an toàn?","back":"Gương → Xi nhan → Điểm mù → Chuyển làn từ từ → Tắt xi nhan."},
    {"id":"f3","topic":"An toàn","front":"Khi trời mưa cần nhớ gì?","back":"Giảm tốc, tăng khoảng cách, bật đèn phù hợp, tránh phanh gấp."},
    {"id":"f4","topic":"Luật","front":"Đến giao lộ cần làm gì đầu tiên?","back":"Giảm tốc, quan sát và xác định quyền ưu tiên."},
    {"id":"f5","topic":"Sa hình","front":"Điểm căn xe dùng để làm gì?","back":"Giúp xe đi đúng quỹ đạo và tránh cán vạch."},
    {"id":"f6","topic":"Bảo dưỡng","front":"Trước khi đi xa nên kiểm tra gì?","back":"Lốp, đèn, nhiên liệu, dầu, nước làm mát, gạt mưa và quanh xe."},
]

SCENARIOS = [
    {"id":"sc1","title":"Xe máy tạt đầu","mode":"city","context":"Bạn đi trong phố đông. Một xe máy phía trước lạng sang trái, có dấu hiệu đổi hướng bất ngờ.","choices":["Tăng tốc vượt nhanh","Giảm tốc, giữ khoảng cách, chuẩn bị phanh","Bấm còi liên tục và bám sát"],"best":"Giảm tốc, giữ khoảng cách, chuẩn bị phanh","why":"Trong phố đông, hành vi khó đoán rất phổ biến. Giảm tốc sớm cho bạn thêm thời gian phản ứng."},
    {"id":"sc2","title":"Người đi bộ gần vạch qua đường","mode":"crosswalk","context":"Có người đứng sát mép đường ở vạch qua đường, chưa rõ họ có băng qua hay không.","choices":["Giữ nguyên tốc độ","Giảm tốc và quan sát hai bên","Lách sang làn khác thật nhanh"],"best":"Giảm tốc và quan sát hai bên","why":"Người đi bộ có thể bước xuống bất ngờ. Vạch qua đường là vùng cần phòng vệ cao."},
    {"id":"sc3","title":"Vòng xuyến đông xe","mode":"roundabout","context":"Bạn sắp nhập vào vòng xuyến, nhiều xe đang di chuyển trong vòng.","choices":["Lao vào trước để giành đường","Giảm tốc, quan sát và nhập khi có khoảng trống","Dừng giữa vòng xuyến"],"best":"Giảm tốc, quan sát và nhập khi có khoảng trống","why":"Vòng xuyến cần quan sát luồng xe và nhập vào từ từ khi an toàn."},
    {"id":"sc4","title":"Mưa lớn trên cao tốc","mode":"rain","context":"Mưa lớn, kính lái nhiều nước, xe trước cách bạn không xa.","choices":["Giữ tốc độ cũ","Giảm tốc, tăng khoảng cách, bật đèn phù hợp","Tăng tốc để thoát mưa"],"best":"Giảm tốc, tăng khoảng cách, bật đèn phù hợp","why":"Mưa làm giảm tầm nhìn và tăng quãng đường phanh."},
    {"id":"sc5","title":"Điểm mù khi chuyển làn","mode":"blind","context":"Bạn muốn chuyển làn phải. Gương không thấy xe nào, nhưng làn phải có thể có xe máy ở điểm mù.","choices":["Chuyển làn ngay","Xi nhan, kiểm tra gương và điểm mù rồi chuyển từ từ","Bấm còi rồi lách"],"best":"Xi nhan, kiểm tra gương và điểm mù rồi chuyển từ từ","why":"Gương không bao phủ toàn bộ vùng bên hông xe. Điểm mù là nguyên nhân phổ biến gây va chạm."},
    {"id":"sc6","title":"Ban đêm đường vắng","mode":"night","context":"Bạn đi ban đêm trên đường vắng, tầm nhìn xa bị hạn chế.","choices":["Chạy nhanh vì đường vắng","Giữ tốc độ hợp lý, dùng đèn phù hợp, quan sát xa","Chỉ nhìn sát đầu xe"],"best":"Giữ tốc độ hợp lý, dùng đèn phù hợp, quan sát xa","why":"Đường vắng không đồng nghĩa với an toàn; ban đêm cần dự phòng tầm nhìn hạn chế."},
]

BRANCH_STORIES = {
    "Giao lộ không đèn": [
        {"text":"Bạn đến giao lộ không có đèn tín hiệu. Có xe máy bên phải đang tiến tới.","choices":{"Giảm tốc và quan sát":"safe","Tăng tốc qua trước":"danger","Bấm còi rồi đi":"mid"}},
        {"safe":"Bạn giảm tốc, thấy xe máy đang đi nhanh và chủ động nhường. Điểm an toàn +20.","mid":"Bấm còi không thay thế quan sát. Bạn vẫn cần giảm tốc. Điểm an toàn +5.","danger":"Tăng tốc ở giao lộ làm rủi ro va chạm tăng cao. Điểm an toàn -20."},
    ],
    "Trời mưa, xe trước phanh": [
        {"text":"Trời mưa, xe trước bật đèn phanh mạnh. Bạn đang cách 15m ở tốc độ 55 km/h.","choices":{"Phanh nhẹ có kiểm soát và giữ thẳng lái":"safe","Đánh lái gấp sang trái":"danger","Bấm còi rồi giữ ga":"danger"}},
        {"safe":"Bạn giữ được ổn định và có thời gian quan sát phía sau. Điểm an toàn +25.","danger":"Thao tác gấp trên đường trơn dễ làm mất lái hoặc va chạm dây chuyền. Điểm an toàn -25."},
    ],
}

MICRO_LESSONS = [
    "Luôn nhìn xa hơn xe ngay trước mặt.",
    "Gặp giao lộ, hãy giảm tốc trước rồi mới quyết định.",
    "Điểm mù không nằm trong gương, hãy kiểm tra nhanh bằng mắt.",
    "Mưa, sương mù, ban đêm: giảm tốc và tăng khoảng cách.",
    "Biển báo nên nhớ theo hành động, không chỉ nhớ tên.",
]

# =========================================================
# PROGRESS / STATE
# =========================================================
def default_progress():
    return {
        "profile": {"name":"Bạn", "goal_minutes":20},
        "xp": 0,
        "level": 1,
        "streak": 0,
        "last_study_date": "",
        "total_seconds": 0,
        "completed_lessons": [],
        "quiz_history": [],
        "exam_history": [],
        "sim_history": [],
        "wrong_bank": {},
        "srs": {},
        "bookmarked_signs": [],
        "ai_notes": [],
        "achievements": [],
    }


def load_progress():
    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            base = default_progress()
            for k, v in base.items():
                data.setdefault(k, v)
            data.setdefault("profile", {}).setdefault("name", "Bạn")
            data.setdefault("profile", {}).setdefault("goal_minutes", 20)
            return data
        except Exception:
            return default_progress()
    return default_progress()


def save_progress():
    p = st.session_state.progress
    p["level"] = max(1, int(p.get("xp", 0) // 100) + 1)
    try:
        PROGRESS_FILE.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as exc:
        st.warning(f"Không lưu được tiến độ: {exc}")


def award_xp(amount, reason=""):
    p = st.session_state.progress
    p["xp"] = int(p.get("xp", 0)) + int(amount)
    if reason:
        st.toast(f"+{amount} XP · {reason}", icon="⭐")
    unlock_achievements()
    save_progress()


def mark_studied(seconds=60):
    p = st.session_state.progress
    p["total_seconds"] = int(p.get("total_seconds", 0)) + int(seconds)
    if p.get("last_study_date") != TODAY:
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        p["streak"] = int(p.get("streak", 0)) + 1 if p.get("last_study_date") == yesterday else 1
        p["last_study_date"] = TODAY
    save_progress()


def unlock_achievements():
    p = st.session_state.progress
    achievements = set(p.get("achievements", []))
    rules = [
        ("starter", p.get("xp", 0) >= 20, "Người mới bắt đầu"),
        ("quiz_hero", len(p.get("quiz_history", [])) >= 3, "Chiến binh Quiz"),
        ("sim_driver", len(p.get("sim_history", [])) >= 3, "Tài xế mô phỏng"),
        ("streak_3", p.get("streak", 0) >= 3, "Học 3 ngày liên tục"),
        ("sign_collector", len(p.get("bookmarked_signs", [])) >= 5, "Sưu tập biển báo"),
    ]
    for key, ok, label in rules:
        if ok and key not in achievements:
            achievements.add(key)
            st.toast(f"Mở khóa thành tích: {label}", icon="🏆")
    p["achievements"] = sorted(list(achievements))


if "progress" not in st.session_state:
    st.session_state.progress = load_progress()
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_started_at" not in st.session_state:
    st.session_state.timer_started_at = 0.0
if "timer_elapsed" not in st.session_state:
    st.session_state.timer_elapsed = 0
if "current_quiz_ids" not in st.session_state:
    st.session_state.current_quiz_ids = [q["id"] for q in random.sample(QUESTIONS, min(5, len(QUESTIONS)))]
if "branch_score" not in st.session_state:
    st.session_state.branch_score = 50

# =========================================================
# UI HELPERS
# =========================================================
def metric_card(title, value, note):
    st.markdown(f"""<div class='metric-card'><div class='metric-title'>{title}</div><div class='metric-value'>{value}</div><div class='muted'>{note}</div></div>""", unsafe_allow_html=True)


def pills(items, cls="blue"):
    st.markdown("".join([f"<span class='pill {cls}'>{html.escape(str(x))}</span>" for x in items]), unsafe_allow_html=True)


def sign_svg(sign_type, symbol, size=164):
    sym = html.escape(str(symbol))
    if sign_type == "Biển cấm":
        body = f"""<circle cx='82' cy='82' r='56' fill='white' stroke='#dc2626' stroke-width='16'/><line x1='44' y1='120' x2='120' y2='44' stroke='#dc2626' stroke-width='11' stroke-linecap='round'/><text x='82' y='94' font-size='27' text-anchor='middle' font-family='Arial'>{sym}</text>"""
    elif sign_type == "Biển nguy hiểm":
        body = f"""<polygon points='82,18 148,140 16,140' fill='#fef08a' stroke='#dc2626' stroke-width='10' join='round'/><text x='82' y='105' font-size='30' text-anchor='middle' font-family='Arial'>{sym}</text>"""
    elif sign_type == "Biển hiệu lệnh":
        body = f"""<circle cx='82' cy='82' r='60' fill='#2563eb' stroke='#1d4ed8' stroke-width='8'/><text x='82' y='96' fill='white' font-size='32' text-anchor='middle' font-family='Arial'>{sym}</text>"""
    else:
        body = f"""<rect x='22' y='22' width='120' height='120' rx='20' fill='#2563eb' stroke='#1d4ed8' stroke-width='8'/><text x='82' y='96' fill='white' font-size='32' text-anchor='middle' font-family='Arial'>{sym}</text>"""
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='{size}' height='{size}' viewBox='0 0 164 164'>{body}</svg>"
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def speak_button(text, label="🔊 Nghe đọc", key="speak"):
    safe = json.dumps(text, ensure_ascii=False)
    components.html(
        f"""
        <button onclick='speakText()' style="border:1px solid #cbd5e1;border-radius:999px;padding:9px 14px;font-weight:800;background:white;cursor:pointer;">{label}</button>
        <script>
        function speakText(){{
            const text = {safe};
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(text);
            u.lang = 'vi-VN'; u.rate = 0.92; u.pitch = 1.0;
            window.speechSynthesis.speak(u);
        }}
        </script>
        """,
        height=48,
    )


def risk_score(speed, distance, weather, visibility, reaction, tire):
    score = 0
    score += max(0, (speed - 30) * 0.75)
    score += max(0, 35 - distance) * 1.15
    score += {"Khô ráo": 0, "Mưa nhẹ": 12, "Mưa lớn": 24, "Sương mù": 28, "Ban đêm": 18}.get(weather, 0)
    score += {"Tốt": 0, "Trung bình": 12, "Kém": 25}.get(visibility, 0)
    score += max(0, (reaction - 0.8) * 20)
    score += {"Tốt": 0, "Hơi mòn": 12, "Mòn nhiều": 26}.get(tire, 0)
    return int(max(0, min(100, score)))


def risk_label(score):
    if score < 35:
        return "Thấp", "risk-low", "Bạn đang ở vùng tương đối an toàn, vẫn cần quan sát liên tục."
    if score < 70:
        return "Trung bình", "risk-mid", "Nên giảm tốc, tăng khoảng cách và chuẩn bị phương án xử lý."
    return "Cao", "risk-high", "Rủi ro cao. Hãy giảm tốc rõ rệt, giữ khoảng cách và tránh thao tác gấp."


def simulator_svg(mode="city", weather="Khô ráo", risk=30, speed=40, distance=25):
    rain = ""
    if weather in ["Mưa nhẹ", "Mưa lớn"]:
        drops = []
        for x in range(20, 620, 50):
            dur = 0.8 if weather == "Mưa lớn" else 1.3
            drops.append(f"<line x1='{x}' y1='-20' x2='{x-12}' y2='35' stroke='#bfdbfe' stroke-width='3' opacity='.8' style='animation:rain {dur}s linear infinite;'/>")
        rain = "".join(drops)
    fog = "<rect x='0' y='0' width='640' height='260' fill='rgba(226,232,240,.45)'/>" if weather == "Sương mù" else ""
    night = "<rect x='0' y='0' width='640' height='260' fill='rgba(15,23,42,.38)'/>" if weather == "Ban đêm" else ""
    extra = ""
    if mode == "roundabout":
        extra = "<circle cx='320' cy='138' r='62' fill='#22c55e' stroke='#166534' stroke-width='6'/><text x='320' y='150' text-anchor='middle' font-size='34'>🔄</text>"
    elif mode == "crosswalk":
        extra = "".join([f"<rect x='{245+i*24}' y='96' width='14' height='92' fill='white' opacity='.9'/>" for i in range(7)]) + "<text x='378' y='78' font-size='30'>🚶</text>"
    elif mode == "blind":
        extra = "<path d='M412 102 Q500 70 596 90' fill='none' stroke='#ef4444' stroke-width='4' stroke-dasharray='8 8'/><text x='510' y='72' font-size='18' fill='#b91c1c'>Điểm mù</text><text x='538' y='112' font-size='28'>🏍️</text>"
    elif mode == "night":
        extra = "<polygon points='255,125 600,52 600,204' fill='#fde68a' opacity='.28'/><text x='70' y='64' font-size='28'>🌙</text>"
    elif mode == "rain":
        extra = "<text x='48' y='64' font-size='28'>🌧️</text>"
    else:
        extra = "<text x='500' y='82' font-size='34'>🏙️</text><text x='90' y='88' font-size='30'>🚦</text>"
    risk_color = "#16a34a" if risk < 35 else "#d97706" if risk < 70 else "#dc2626"
    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 260' width='100%' height='260'>
      <style>@keyframes carmove{{0%{{transform:translateX(0)}}100%{{transform:translateX(24px)}}}} @keyframes rain{{from{{transform:translateY(-50px)}}to{{transform:translateY(300px)}}}}</style>
      <rect width='640' height='260' rx='26' fill='#dbeafe'/>
      <rect x='0' y='0' width='640' height='82' fill='#bfdbfe'/>
      <circle cx='560' cy='44' r='25' fill='#fde68a'/>
      <rect x='0' y='84' width='640' height='176' fill='#334155'/>
      <line x1='0' y1='172' x2='640' y2='172' stroke='white' stroke-width='5' stroke-dasharray='38 28'/>
      <rect x='0' y='82' width='640' height='16' fill='#22c55e'/>
      {extra}
      <g style='animation:carmove 1.5s ease-in-out infinite alternate;'>
        <rect x='168' y='142' width='92' height='45' rx='13' fill='#2563eb'/>
        <rect x='186' y='124' width='50' height='30' rx='10' fill='#60a5fa'/>
        <circle cx='188' cy='190' r='11' fill='#111827'/><circle cx='240' cy='190' r='11' fill='#111827'/>
        <text x='198' y='172' font-size='20'>🚗</text>
      </g>
      <rect x='22' y='214' width='{max(20, min(596, risk*5.96))}' height='14' rx='7' fill='{risk_color}'/>
      <rect x='22' y='214' width='596' height='14' rx='7' fill='none' stroke='white' opacity='.7'/>
      <text x='26' y='246' font-size='16' fill='white'>Tốc độ {speed} km/h · Khoảng cách {distance} m · Rủi ro {risk}/100</text>
      {fog}{night}{rain}
    </svg>
    """
    return svg


def brake_distance(speed, reaction, weather, tire):
    # simple educational approximation
    v = speed / 3.6
    friction = 0.75
    if weather == "Mưa nhẹ": friction = 0.55
    if weather == "Mưa lớn": friction = 0.42
    if weather == "Sương mù": friction = 0.55
    if tire == "Hơi mòn": friction *= 0.85
    if tire == "Mòn nhiều": friction *= 0.68
    reaction_distance = v * reaction
    braking = (v * v) / (2 * 9.81 * friction)
    return reaction_distance, braking, reaction_distance + braking


def offline_tutor(prompt="", mode="plan"):
    p = st.session_state.progress
    weak = weak_topics()
    wrong_count = len(p.get("wrong_bank", {}))
    if mode == "plan":
        topics = ", ".join(weak[:3]) if weak else "Biển báo, kỹ thuật lái, tình huống an toàn"
        return f"""### Lộ trình cá nhân 7 ngày
**Mục tiêu chính:** {topics}. Hiện bạn có {wrong_count} câu trong ôn sai.

**Ngày 1:** Ôn 10 phút biển báo + 5 câu quiz.  
**Ngày 2:** Học chuyển làn, điểm mù + mô phỏng điểm mù.  
**Ngày 3:** Luyện giao lộ/vòng xuyến + 10 câu luật.  
**Ngày 4:** Mưa/ban đêm + buồng lái rủi ro.  
**Ngày 5:** Sa hình từng bước + flashcard.  
**Ngày 6:** Thi thử 20 câu, ghi lỗi sai.  
**Ngày 7:** Ôn sai thông minh, làm lại chủ đề yếu.

**Cách học:** mỗi phiên 20–30 phút, làm sai câu nào lưu ngay vào ôn sai."""
    if mode == "explain":
        return f"""### Giải thích dễ hiểu
Câu hỏi/tình huống bạn đưa là: **{prompt or 'chưa nhập nội dung'}**

Khi học lái, hãy ưu tiên 3 nguyên tắc: **giảm tốc khi chưa chắc, quan sát đủ, không gây bất ngờ cho xe khác**. Nếu đáp án nào làm xe khác khó đoán hoặc làm bạn mất thời gian phản ứng, thường đó là đáp án rủi ro.

**Mẹo nhớ:** Gặp giao lộ, mưa, điểm mù, trẻ em, người đi bộ → hãy giảm tốc trước."""
    return f"""### Bài luyện gợi ý
1. Làm 5 câu quiz ở chủ đề yếu: {', '.join(weak[:2]) if weak else 'An toàn và Biển báo'}.  
2. Vào Mô phỏng, đặt tốc độ 60 km/h, khoảng cách 15m, trời mưa để xem rủi ro.  
3. Ghi lại 2 lỗi sai trong Sổ tay.  
4. Ôn flashcard đến khi trả lời đúng 2 lần."""


def ask_gemini(api_key, model, prompt):
    if genai is None:
        return "Chưa cài google-genai. App sẽ dùng AI nội bộ."
    try:
        client = genai.Client(api_key=api_key)
        resp = client.models.generate_content(model=model, contents=prompt)
        return getattr(resp, "text", str(resp))
    except Exception as exc:
        return f"Không gọi được Gemini, dùng AI nội bộ thay thế. Lỗi: {exc}"


def get_question(qid):
    return next(q for q in QUESTIONS if q["id"] == qid)


def weak_topics():
    hist = st.session_state.progress.get("quiz_history", [])
    if not hist:
        return []
    scores = {}
    for h in hist:
        topic = h.get("topic", "Khác")
        scores.setdefault(topic, []).append(h.get("score", 0))
    avg = {k: sum(v)/len(v) for k, v in scores.items()}
    return [k for k, v in sorted(avg.items(), key=lambda x: x[1]) if v < 75]


def record_wrong(q, correct=False):
    bank = st.session_state.progress.setdefault("wrong_bank", {})
    qid = q["id"]
    if correct:
        if qid in bank:
            bank[qid]["correct_streak"] = bank[qid].get("correct_streak", 0) + 1
            bank[qid]["last_review"] = TODAY
            if bank[qid]["correct_streak"] >= 2:
                del bank[qid]
    else:
        bank[qid] = {"misses": bank.get(qid, {}).get("misses", 0) + 1, "correct_streak": 0, "last_review": TODAY, "topic": q["topic"]}
    save_progress()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🚗 AutoLearn v6")
    st.caption("Ultra UI · Mobile · AI Tutor · Simulator")
    p = st.session_state.progress
    name = st.text_input("Tên người học", value=p.get("profile", {}).get("name", "Bạn"))
    p["profile"]["name"] = name or "Bạn"
    page = st.radio(
        "Đi tới",
        [
            "🏠 Dashboard",
            "📱 Lộ trình mobile",
            "🚦 Biển báo 3D",
            "🃏 Flashcard SRS",
            "✅ Quiz Arena",
            "🧠 Ôn sai thông minh",
            "🕹️ Mô phỏng Ultra",
            "🎭 Tình huống phân nhánh",
            "🅿️ Sa hình 2D",
            "🤖 AI Tutor",
            "⏱️ Pomodoro",
            "🎬 Google Veo",
            "📈 Phân tích tiến độ",
            "⚙️ Dữ liệu & cài đặt",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown(f"**Level {p.get('level',1)}** · {p.get('xp',0)} XP")
    st.progress((p.get("xp",0) % 100) / 100)
    st.caption(f"Streak: {p.get('streak',0)} ngày 🔥")
    st.caption(f"Ôn sai: {len(p.get('wrong_bank',{}))} câu")
    if st.button("💾 Lưu tiến độ"):
        save_progress(); st.success("Đã lưu tiến độ.")

# quick nav / mobile feel
st.markdown(
    """
    <div class='quick-row'>
      <span class='quick-chip'>🏠 Home</span><span class='quick-chip'>🕹️ Simulator</span><span class='quick-chip'>🤖 AI Tutor</span><span class='quick-chip'>🧠 Ôn sai</span><span class='quick-chip'>🚦 Biển báo</span><span class='quick-chip'>📈 Progress</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# PAGES
# =========================================================
if page == "🏠 Dashboard":
    p = st.session_state.progress
    st.markdown(
        f"""
        <div class='hero'>
          <div class='float-badge'>v{APP_VERSION}</div>
          <div class='hero-grid'>
            <div>
              <h1>Xin chào, {html.escape(p.get('profile',{}).get('name','Bạn'))} 👋<br/>Hôm nay lái xe an toàn hơn 1%.</h1>
              <p>Dashboard học lái ô tô kiểu mobile app: học bài, luyện biển báo, quiz, ôn sai, mô phỏng tình huống và AI Tutor cá nhân hóa.</p>
              <span class='pill green'>Level {p.get('level',1)}</span><span class='pill yellow'>{p.get('xp',0)} XP</span><span class='pill red'>{p.get('streak',0)} ngày streak</span>
            </div>
            <div class='phone-panel'><div class='road'><div class='drive-car'>🚗</div><div class='road-lane'></div><div class='road-line'></div></div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("Tổng thời gian", f"{p.get('total_seconds',0)//60} phút", "Đã ghi nhận")
    with c2: metric_card("Bài hoàn thành", f"{len(p.get('completed_lessons',[]))}/{len(LESSONS)}", "Lộ trình")
    with c3: metric_card("Quiz đã làm", len(p.get("quiz_history",[])), "Lượt luyện")
    with c4: metric_card("Câu cần ôn", len(p.get("wrong_bank",{})), "Ôn sai thông minh")

    st.markdown("## 🎯 Gợi ý thông minh hôm nay")
    weak = weak_topics()
    cols = st.columns(3)
    suggestions = [
        ("🧠", "Ôn sai 5 phút", f"Bạn đang có {len(p.get('wrong_bank',{}))} câu cần ôn."),
        ("🕹️", "Chạy mô phỏng rủi ro", "Thử mưa lớn + tốc độ 60 km/h để hiểu quãng đường phanh."),
        ("🤖", "Hỏi AI Tutor", "Nhờ AI tạo lộ trình 7 ngày theo chủ đề yếu."),
    ]
    if weak:
        suggestions[0] = ("⚠️", "Chủ đề yếu", "Nên ôn: " + ", ".join(weak[:2]))
    for col, (ic, title, desc) in zip(cols, suggestions):
        with col:
            st.markdown(f"<div class='card'><div class='big-icon'>{ic}</div><h3>{title}</h3><p class='muted'>{desc}</p></div>", unsafe_allow_html=True)

    st.markdown("## ⚡ Micro-learning 60 giây")
    tip = random.choice(MICRO_LESSONS)
    st.markdown(f"<div class='ai-bubble'><h3>{tip}</h3><p class='muted'>Bấm nghe đọc để học nhanh bằng âm thanh.</p></div>", unsafe_allow_html=True)
    speak_button(tip, "🔊 Nghe mẹo học")
    if st.button("✅ Tôi đã học mẹo này"):
        mark_studied(60); award_xp(3, "Micro-learning")

elif page == "📱 Lộ trình mobile":
    st.title("📱 Lộ trình học kiểu mobile")
    st.caption("Mỗi bài là một card ngắn, rõ mục tiêu, có checklist và XP.")
    cols = st.columns(3)
    p = st.session_state.progress
    for i, lesson in enumerate(LESSONS):
        done = lesson["id"] in p.get("completed_lessons", [])
        with cols[i % 3]:
            st.markdown(f"""
            <div class='card'>
              <div class='big-icon'>{lesson['icon']}</div><h3>{lesson['title']}</h3>
              <p class='muted'>{lesson['summary']}</p>
              <span class='pill {'green' if done else 'yellow'}'>{'Đã xong' if done else lesson['level']}</span><span class='pill blue'>{lesson['minutes']} phút</span>
            </div>
            """, unsafe_allow_html=True)
    lesson_map = {f"{x['icon']} {x['title']}": x for x in LESSONS}
    selected = st.selectbox("Mở bài học", list(lesson_map.keys()))
    lesson = lesson_map[selected]
    tab1, tab2, tab3 = st.tabs(["📖 Học", "🎧 Nghe", "✅ Checklist"])
    with tab1:
        st.subheader(lesson["title"]); pills(lesson["topics"]); st.write(lesson["content"])
    with tab2:
        speak_button(lesson["title"] + ". " + lesson["content"], "🔊 Nghe toàn bài")
        st.info("Tính năng âm thanh dùng giọng đọc của trình duyệt. Trên Mac, Safari/Chrome thường hỗ trợ tốt tiếng Việt.")
    with tab3:
        st.checkbox("Tôi hiểu mục tiêu bài học", key=f"ck1_{lesson['id']}")
        st.checkbox("Tôi ghi được 1 mẹo nhớ", key=f"ck2_{lesson['id']}")
        st.checkbox("Tôi đã làm quiz hoặc mô phỏng liên quan", key=f"ck3_{lesson['id']}")
        if st.button("✅ Hoàn thành bài này"):
            if lesson["id"] not in p["completed_lessons"]:
                p["completed_lessons"].append(lesson["id"])
            mark_studied(lesson["minutes"]*60); award_xp(15, "Hoàn thành bài")
            st.rerun()

elif page == "🚦 Biển báo 3D":
    st.title("🚦 Biển báo 3D/SVG + âm thanh")
    sign_df = pd.DataFrame(SIGNS)
    col1,col2 = st.columns(2)
    with col1:
        sign_type = st.selectbox("Nhóm biển", ["Tất cả"] + sorted(sign_df["type"].unique().tolist()))
    with col2:
        kw = st.text_input("Tìm biển", placeholder="Ví dụ: cấm, trơn, vòng xuyến...")
    filtered = sign_df.copy()
    if sign_type != "Tất cả": filtered = filtered[filtered["type"] == sign_type]
    if kw.strip():
        k = kw.lower().strip()
        filtered = filtered[filtered.apply(lambda r: k in (r["name"]+r["meaning"]+r["action"]+r["tip"]).lower(), axis=1)]
    cols = st.columns(3)
    p = st.session_state.progress
    for i, row in filtered.reset_index(drop=True).iterrows():
        tag = "red" if row["type"] == "Biển cấm" else "yellow" if row["type"] == "Biển nguy hiểm" else "green" if row["type"] == "Biển hiệu lệnh" else "purple"
        with cols[i % 3]:
            st.markdown(f"""
            <div class='card' style='text-align:center'>
              <img src='{sign_svg(row['type'], row['symbol'])}' width='138'/>
              <h3>{row['name']}</h3><span class='pill {tag}'>{row['type']}</span>
              <p>{row['meaning']}</p><p><b>Xử lý:</b> {row['action']}</p><p class='muted'>💡 {row['tip']}</p>
            </div>
            """, unsafe_allow_html=True)
            speak_button(f"{row['name']}. {row['meaning']}. Cách xử lý: {row['action']}", "🔊 Nghe", f"sp_{row['id']}")
            if st.button("🔖 Lưu ôn", key=f"bm_{row['id']}"):
                if row["id"] not in p["bookmarked_signs"]:
                    p["bookmarked_signs"].append(row["id"]); award_xp(2, "Lưu biển báo")
                save_progress()

elif page == "🃏 Flashcard SRS":
    st.title("🃏 Flashcard SRS thông minh")
    st.caption("Chọn mức nhớ để app tự lên lịch ôn lại.")
    p = st.session_state.progress
    srs = p.setdefault("srs", {})
    due_cards = []
    for card in FLASHCARDS:
        item = srs.get(card["id"], {"due": TODAY, "level": 0})
        if item.get("due", TODAY) <= TODAY:
            due_cards.append(card)
    if not due_cards:
        st.success("Hôm nay chưa có thẻ đến hạn. Bạn có thể học lại toàn bộ hoặc nghỉ.")
        due_cards = FLASHCARDS
    card = st.selectbox("Chọn thẻ", due_cards, format_func=lambda x: f"{x['topic']} · {x['front']}")
    show = st.toggle("Hiện đáp án")
    st.markdown(f"<div class='card' style='text-align:center;min-height:230px;display:flex;flex-direction:column;justify-content:center'><span class='pill purple'>{card['topic']}</span><h2>{card['back'] if show else card['front']}</h2><p class='muted'>{'Đáp án' if show else 'Câu hỏi'}</p></div>", unsafe_allow_html=True)
    speak_button(card["front"] + ". " + card["back"], "🔊 Nghe thẻ")
    c1,c2,c3 = st.columns(3)
    def update_srs(level_delta, days, label):
        item = srs.get(card["id"], {"level":0})
        item["level"] = max(0, item.get("level",0)+level_delta)
        item["due"] = (date.today()+timedelta(days=days)).isoformat()
        srs[card["id"]] = item
        mark_studied(45); award_xp(4 if level_delta>0 else 1, label)
    with c1:
        if st.button("🔁 Chưa nhớ"):
            update_srs(-1, 0, "Ôn lại flashcard")
    with c2:
        if st.button("👌 Tạm nhớ"):
            update_srs(1, 1, "Flashcard")
    with c3:
        if st.button("🚀 Nhớ rất tốt"):
            update_srs(2, 3, "Flashcard tốt")

elif page == "✅ Quiz Arena":
    st.title("✅ Quiz Arena")
    st.caption("Quiz đẹp hơn, có XP, lưu câu sai và chế độ chủ đề yếu.")
    topics = ["Tất cả"] + sorted(set(q["topic"] for q in QUESTIONS)) + ["Chủ đề yếu"]
    topic = st.selectbox("Chọn chủ đề", topics)
    n = st.slider("Số câu", 5, min(20, len(QUESTIONS)), 5)
    if st.button("🎲 Tạo đề mới"):
        pool = QUESTIONS
        if topic == "Chủ đề yếu":
            weak = weak_topics()
            pool = [q for q in QUESTIONS if q["topic"] in weak] or QUESTIONS
        elif topic != "Tất cả":
            pool = [q for q in QUESTIONS if q["topic"] == topic]
        st.session_state.current_quiz_ids = [q["id"] for q in random.sample(pool, min(n, len(pool)))]
    quiz = [get_question(qid) for qid in st.session_state.current_quiz_ids]
    with st.form("quiz_form_v6"):
        answers = {}
        st.progress(0)
        for idx, q in enumerate(quiz, 1):
            st.markdown(f"### Câu {idx}/{len(quiz)} · {q['topic']}")
            st.write(q["question"])
            answers[q["id"]] = st.radio("Chọn đáp án", q["options"], key=f"ans_{q['id']}_{idx}", label_visibility="collapsed")
        submit = st.form_submit_button("Chấm điểm")
    if submit:
        correct = 0
        wrong_topics = []
        for q in quiz:
            ok = answers[q["id"]] == q["answer"]
            correct += int(ok)
            record_wrong(q, correct=ok)
            if ok:
                st.success(f"✅ {q['question']} — Đúng")
            else:
                wrong_topics.append(q["topic"])
                st.error(f"❌ {q['question']} — Bạn chọn: {answers[q['id']]}. Đúng: {q['answer']}")
            st.info(q["explain"])
        score = round(correct / len(quiz) * 100)
        st.session_state.progress["quiz_history"].append({"time": datetime.now().strftime("%d/%m/%Y %H:%M"), "topic": topic, "score": score, "correct": correct, "total": len(quiz)})
        mark_studied(len(quiz)*45); award_xp(correct*3, "Quiz")
        st.metric("Điểm", f"{score}%", f"{correct}/{len(quiz)} câu đúng")
        if score >= 85: st.balloons()

elif page == "🧠 Ôn sai thông minh":
    st.title("🧠 Ôn sai thông minh")
    bank = st.session_state.progress.get("wrong_bank", {})
    if not bank:
        st.success("Không có câu sai cần ôn. Làm thêm quiz để hệ thống cá nhân hóa cho bạn.")
    else:
        st.caption("Trả lời đúng 2 lần liên tiếp, câu sẽ tự rời khỏi danh sách ôn sai.")
        qids = list(bank.keys())
        qid = st.selectbox("Câu cần ôn", qids, format_func=lambda x: f"{get_question(x)['topic']} · {get_question(x)['question']}")
        q = get_question(qid)
        st.markdown(f"<div class='card'><span class='pill red'>Sai {bank[qid].get('misses',1)} lần</span><h3>{q['question']}</h3></div>", unsafe_allow_html=True)
        ans = st.radio("Chọn lại đáp án", q["options"])
        if st.button("Kiểm tra ôn sai"):
            if ans == q["answer"]:
                record_wrong(q, correct=True); st.success("Đúng rồi. Nếu đúng 2 lần liên tiếp câu này sẽ được gỡ."); award_xp(5, "Ôn sai")
            else:
                record_wrong(q, correct=False); st.error(f"Chưa đúng. Đáp án: {q['answer']}")
            st.info(q["explain"])
        st.markdown("### AI giải thích nhanh")
        st.markdown(offline_tutor(q["question"], "explain"))

elif page == "🕹️ Mô phỏng Ultra":
    st.title("🕹️ Mô phỏng Ultra: Buồng lái rủi ro")
    left, right = st.columns([1, 1])
    with left:
        mode = st.selectbox("Bối cảnh", ["city", "crosswalk", "roundabout", "rain", "blind", "night"], format_func=lambda x: {"city":"Phố đông","crosswalk":"Vạch qua đường","roundabout":"Vòng xuyến","rain":"Mưa lớn","blind":"Điểm mù","night":"Ban đêm"}[x])
        speed = st.slider("Tốc độ (km/h)", 10, 120, 45)
        distance = st.slider("Khoảng cách với xe/vật phía trước (m)", 5, 100, 25)
        weather = st.selectbox("Thời tiết / ánh sáng", ["Khô ráo", "Mưa nhẹ", "Mưa lớn", "Sương mù", "Ban đêm"])
        visibility = st.selectbox("Tầm nhìn", ["Tốt", "Trung bình", "Kém"])
        reaction = st.slider("Thời gian phản xạ (giây)", 0.5, 2.5, 1.0, 0.1)
        tire = st.selectbox("Tình trạng lốp", ["Tốt", "Hơi mòn", "Mòn nhiều"])
    risk = risk_score(speed, distance, weather, visibility, reaction, tire)
    label, cls, advice = risk_label(risk)
    with right:
        components.html(simulator_svg(mode, weather, risk, speed, distance), height=280)
        st.markdown(f"### Rủi ro: <span class='{cls}'>{risk}/100 · {label}</span>", unsafe_allow_html=True)
        st.progress(risk/100)
        st.info(advice)
        rd, bd, total = brake_distance(speed, reaction, weather, tire)
        st.metric("Quãng đường dừng ước tính", f"{total:.1f} m", f"Phản xạ {rd:.1f}m + phanh {bd:.1f}m")
        if distance < total:
            st.error("Khoảng cách hiện tại có thể không đủ để dừng an toàn.")
        else:
            st.success("Khoảng cách hiện tại tương đối đủ, nhưng vẫn cần quan sát.")
        if st.button("💾 Lưu lượt mô phỏng"):
            st.session_state.progress["sim_history"].append({"time": datetime.now().strftime("%d/%m/%Y %H:%M"), "mode": mode, "risk": risk, "speed": speed, "distance": distance, "weather": weather})
            mark_studied(120); award_xp(8, "Mô phỏng")

elif page == "🎭 Tình huống phân nhánh":
    st.title("🎭 Tình huống phân nhánh")
    scenario = st.selectbox("Chọn tình huống", SCENARIOS, format_func=lambda x: x["title"])
    components.html(simulator_svg(scenario["mode"], "Khô ráo", 45, 40, 25), height=280)
    st.markdown(f"<div class='card'><span class='pill purple'>Mô phỏng quyết định</span><h3>{scenario['title']}</h3><p>{scenario['context']}</p></div>", unsafe_allow_html=True)
    choice = st.radio("Bạn chọn cách xử lý nào?", scenario["choices"])
    if st.button("Phân tích quyết định"):
        ok = choice == scenario["best"]
        if ok:
            st.success("Lựa chọn an toàn nhất. +10 XP")
            award_xp(10, "Tình huống đúng")
        else:
            st.error(f"Chưa tối ưu. Nên chọn: {scenario['best']}")
        st.info(scenario["why"])
        st.session_state.progress["sim_history"].append({"time": datetime.now().strftime("%d/%m/%Y %H:%M"), "mode": scenario["mode"], "risk": 20 if ok else 78, "choice": choice})
        save_progress()
    st.markdown("## Story mode")
    story_name = st.selectbox("Chọn câu chuyện", list(BRANCH_STORIES.keys()))
    step, outcome = BRANCH_STORIES[story_name]
    st.write(step["text"])
    story_choice = st.radio("Quyết định của bạn", list(step["choices"].keys()), key="branch_choice")
    if st.button("Tiếp tục câu chuyện"):
        result_key = step["choices"][story_choice]
        msg = outcome.get(result_key, "Kết quả chưa xác định.")
        delta = 20 if result_key == "safe" else 5 if result_key == "mid" else -20
        st.session_state.branch_score = max(0, min(100, st.session_state.branch_score + delta))
        st.write(msg)
        st.progress(st.session_state.branch_score/100)

elif page == "🅿️ Sa hình 2D":
    st.title("🅿️ Sa hình 2D từng bước")
    bài = st.selectbox("Bài sa hình", ["Đề-pa dốc", "Ghép xe dọc", "Vệt bánh xe", "Đường vuông góc"])
    step = st.slider("Bước", 1, 4, 1)
    text = {
        "Đề-pa dốc": ["Dừng đúng vị trí trước vạch.", "Giữ phanh, tìm điểm bám côn.", "Tăng ga nhẹ, nhả phanh từ từ.", "Xe lên dốc ổn định, không tụt."],
        "Ghép xe dọc": ["Căn xe song song vị trí ghép.", "Lùi chậm, quan sát gương.", "Đánh lái theo điểm căn.", "Chỉnh xe thẳng, không cán vạch."],
        "Vệt bánh xe": ["Vào bài thật chậm.", "Căn bánh theo vệt.", "Giữ vô lăng ổn định.", "Ra khỏi bài, trả lái mượt."],
        "Đường vuông góc": ["Giảm tốc trước góc.", "Xác định điểm đánh lái.", "Đánh lái vừa đủ.", "Trả lái đúng lúc."],
    }[bài]
    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 280' width='100%' height='280'>
      <rect width='640' height='280' rx='26' fill='#ecfeff'/><rect x='90' y='60' width='460' height='170' rx='20' fill='#334155'/>
      <line x1='120' y1='145' x2='520' y2='145' stroke='white' stroke-dasharray='25 18' stroke-width='5'/>
      <rect x='{105+step*85}' y='{126 if bài!='Đề-pa dốc' else 156-step*18}' width='82' height='42' rx='12' fill='#2563eb'/><circle cx='{125+step*85}' cy='{172 if bài!='Đề-pa dốc' else 202-step*18}' r='10' fill='#111827'/><circle cx='{168+step*85}' cy='{172 if bài!='Đề-pa dốc' else 202-step*18}' r='10' fill='#111827'/>
      <text x='320' y='36' text-anchor='middle' font-size='22' font-weight='700'>{html.escape(bài)} · Bước {step}</text>
      <text x='320' y='260' text-anchor='middle' font-size='18'>{html.escape(text[step-1])}</text>
    </svg>"""
    components.html(svg, height=300)
    st.info(text[step-1])
    speak_button(f"{bài}. Bước {step}. {text[step-1]}", "🔊 Nghe bước này")

elif page == "🤖 AI Tutor":
    st.title("🤖 AI Tutor thật sự hữu ích")
    st.caption("Có chế độ nội bộ không cần API; nếu nhập Google API Key, app có thể gọi Gemini để trả lời linh hoạt hơn.")
    mode = st.selectbox("Bạn muốn AI giúp gì?", ["Tạo lộ trình cá nhân", "Giải thích câu sai/tình huống", "Tạo bài luyện theo điểm yếu", "Viết lời nhắc học hôm nay"])
    prompt = st.text_area("Nội dung cần hỏi / câu sai / tình huống", height=120, placeholder="Ví dụ: Vì sao đi trời mưa phải tăng khoảng cách?")
    use_online = st.toggle("Dùng Gemini nếu có API Key", value=False)
    api_key = ""
    model = "gemini-2.0-flash"
    if use_online:
        api_key = st.text_input("Google API Key", type="password")
        model = st.text_input("Model", value="gemini-2.0-flash")
    if st.button("✨ Tạo câu trả lời"):
        mode_map = {"Tạo lộ trình cá nhân":"plan", "Giải thích câu sai/tình huống":"explain", "Tạo bài luyện theo điểm yếu":"practice", "Viết lời nhắc học hôm nay":"practice"}
        offline = offline_tutor(prompt, mode_map.get(mode, "plan"))
        if use_online and api_key:
            system_prompt = f"Bạn là gia sư dạy lái xe bằng tiếng Việt, giải thích rất dễ hiểu, ngắn gọn, an toàn, có ví dụ thực tế. Chế độ: {mode}. Dữ liệu tiến độ: {json.dumps(st.session_state.progress, ensure_ascii=False)[:3000]}. Câu hỏi người học: {prompt}"
            result = ask_gemini(api_key, model, system_prompt)
            if result.startswith("Không gọi được") or result.startswith("Chưa cài"):
                st.warning(result); result = offline
        else:
            result = offline
        st.markdown(f"<div class='ai-bubble'>{result}</div>", unsafe_allow_html=True)
        st.session_state.progress["ai_notes"].append({"time": datetime.now().strftime("%d/%m/%Y %H:%M"), "mode": mode, "prompt": prompt, "result": result[:1000]})
        award_xp(4, "AI Tutor")

elif page == "⏱️ Pomodoro":
    st.title("⏱️ Pomodoro học lái")
    if st.session_state.timer_running:
        elapsed = st.session_state.timer_elapsed + int(time.time() - st.session_state.timer_started_at)
    else:
        elapsed = st.session_state.timer_elapsed
    mm, ss = divmod(elapsed, 60)
    st.markdown(f"<div class='timer-box'><div class='timer-value'>{mm:02d}:{ss:02d}</div><p>Học tập tập trung, mỗi phiên 20–30 phút.</p></div>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        if st.button("▶️ Bắt đầu") and not st.session_state.timer_running:
            st.session_state.timer_running=True; st.session_state.timer_started_at=time.time(); st.rerun()
    with c2:
        if st.button("⏸️ Dừng") and st.session_state.timer_running:
            st.session_state.timer_elapsed += int(time.time() - st.session_state.timer_started_at); st.session_state.timer_running=False; st.rerun()
    with c3:
        if st.button("✅ Lưu phiên"):
            if st.session_state.timer_running:
                st.session_state.timer_elapsed += int(time.time() - st.session_state.timer_started_at); st.session_state.timer_running=False
            mark_studied(st.session_state.timer_elapsed); award_xp(max(1, st.session_state.timer_elapsed//60), "Pomodoro")
            st.session_state.timer_elapsed=0; st.success("Đã lưu thời gian học.")
    with c4:
        if st.button("🔄 Reset"):
            st.session_state.timer_running=False; st.session_state.timer_elapsed=0; st.rerun()
    st.info("Mẹo: học 20 phút, nghỉ 5 phút, sau đó làm quiz 5 câu để khóa kiến thức.")

elif page == "🎬 Google Veo":
    st.title("🎬 Google Veo: tạo video từ ảnh")
    if genai is None or types is None:
        st.error("Chưa cài google-genai. Hãy chạy install_once hoặc pip install google-genai.")
    else:
        api_key = st.text_input("Google API Key", type="password")
        uploaded_file = st.file_uploader("Chọn ảnh JPG/PNG", type=["jpg","jpeg","png"])
        prompt = st.text_area("Mô tả chuyển động", value="Animate this image naturally, cinematic camera motion, high quality.", height=100)
        aspect_ratio = st.selectbox("Tỷ lệ", ["16:9","9:16","1:1"])
        if uploaded_file: st.image(uploaded_file, use_container_width=True)
        if st.button("🚀 Tạo video"):
            if not api_key or not uploaded_file:
                st.warning("Cần API key và ảnh.")
            else:
                client = genai.Client(api_key=api_key)
                tmp = None
                try:
                    with st.spinner("Đang tạo video bằng Veo..."):
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
                            f.write(uploaded_file.getvalue()); tmp=f.name
                        img = client.files.upload(file=tmp)
                        op = client.models.generate_videos(model="veo-2.0-generate-001", prompt=prompt, image=img, config=types.GenerateVideosConfig(aspect_ratio=aspect_ratio))
                        while not op.done:
                            time.sleep(5); op = client.operations.get(operation=op.name)
                    result = getattr(op, "result", None) or getattr(op, "response", None)
                    videos = getattr(result, "videos", None) or getattr(result, "generated_videos", None) or []
                    if videos:
                        v = videos[0]; nested = getattr(v, "video", v)
                        b = getattr(nested, "video_bytes", None) or getattr(nested, "bytes", None)
                        uri = getattr(nested, "uri", None) or getattr(nested, "url", None)
                        st.success("Tạo video thành công!")
                        if b:
                            st.video(b); st.download_button("⬇️ Tải video", b, "video_veo.mp4", "video/mp4")
                        elif uri:
                            st.video(uri); st.link_button("Mở video", uri)
                        else: st.json(str(v))
                    else: st.error("Không tìm thấy video trong response.")
                except Exception as exc:
                    st.error(f"Lỗi: {exc}")
                finally:
                    if tmp and os.path.exists(tmp): os.remove(tmp)

elif page == "📈 Phân tích tiến độ":
    st.title("📈 Phân tích tiến độ")
    p = st.session_state.progress
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("XP", p.get("xp",0), f"Level {p.get('level',1)}")
    with c2: metric_card("Streak", p.get("streak",0), "ngày liên tục")
    with c3: metric_card("Thời gian", f"{p.get('total_seconds',0)//60} phút", "tổng học")
    with c4: metric_card("Ôn sai", len(p.get("wrong_bank",{})), "câu")
    if p.get("quiz_history"):
        df = pd.DataFrame(p["quiz_history"])
        st.subheader("Điểm quiz")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.line_chart(df.set_index("time")["score"])
        topic_df = df.groupby("topic", as_index=False)["score"].mean()
        st.subheader("Điểm trung bình theo chủ đề")
        st.bar_chart(topic_df.set_index("topic"))
    else:
        st.info("Chưa có quiz history.")
    if p.get("sim_history"):
        sdf = pd.DataFrame(p["sim_history"])
        st.subheader("Lịch sử mô phỏng")
        st.dataframe(sdf, use_container_width=True, hide_index=True)
    st.subheader("Thành tích")
    labels = {"starter":"Người mới bắt đầu","quiz_hero":"Chiến binh Quiz","sim_driver":"Tài xế mô phỏng","streak_3":"Học 3 ngày liên tục","sign_collector":"Sưu tập biển báo"}
    if p.get("achievements"):
        for key in p["achievements"]:
            st.markdown(f"<div class='achievement'>🏆 <b>{labels.get(key,key)}</b></div>", unsafe_allow_html=True)
    else: st.caption("Chưa có thành tích. Hãy học bài, làm quiz hoặc chạy mô phỏng.")

elif page == "⚙️ Dữ liệu & cài đặt":
    st.title("⚙️ Dữ liệu & cài đặt")
    p = st.session_state.progress
    p["profile"]["goal_minutes"] = st.number_input("Mục tiêu học mỗi ngày (phút)", 5, 180, int(p.get("profile",{}).get("goal_minutes",20)), 5)
    st.subheader("Xuất / nhập dữ liệu")
    data = json.dumps(p, ensure_ascii=False, indent=2)
    st.download_button("⬇️ Tải tiến độ JSON", data, "autolearn_progress_backup.json", "application/json")
    uploaded = st.file_uploader("Nhập lại file tiến độ JSON", type=["json"])
    if uploaded and st.button("Nhập dữ liệu"):
        try:
            st.session_state.progress = json.loads(uploaded.getvalue().decode("utf-8")); save_progress(); st.success("Đã nhập dữ liệu. Tải lại trang nếu cần.")
        except Exception as exc: st.error(f"Không nhập được: {exc}")
    st.subheader("Sổ tay học lái")
    notes_text = "\n\n".join([n.get("result", "") for n in p.get("ai_notes", [])[-3:]])
    notes = st.text_area("Ghi chú cá nhân", value=p.get("notes", notes_text), height=220)
    p["notes"] = notes
    c1,c2 = st.columns(2)
    with c1:
        if st.button("💾 Lưu tất cả"):
            save_progress(); st.success("Đã lưu vào autolearn_progress.json")
    with c2:
        if st.button("🧹 Reset toàn bộ tiến độ"):
            st.session_state.progress = default_progress(); save_progress(); st.rerun()

save_progress()
st.divider()
st.caption("AutoLearn Ultra UI v6 · Mobile-first · AI Tutor · Mô phỏng trực quan · Lưu tiến độ thật · Chạy local hoặc deploy Streamlit Cloud.")
