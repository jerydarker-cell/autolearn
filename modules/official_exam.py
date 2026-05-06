import csv
import io
import json
import random
from pathlib import Path
from typing import Dict, Any, List

import streamlit as st
import streamlit.components.v1 as components

from . import ui

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MANIFEST_PATH = DATA_DIR / "official_exam_manifest_2025.json"
DEFAULT_BANK_PATH = DATA_DIR / "official_600_questions_2025_extracted.json"
DEFAULT_CSV_PATH = DATA_DIR / "official_600_questions_2025_extracted.csv"
DEFAULT_PDF_PATH = DATA_DIR / "official_600_questions_2025.pdf"

CHAPTERS = {
    1: {"name": "Quy định chung và quy tắc giao thông đường bộ", "range": "1-180", "count": 180},
    2: {"name": "Văn hóa giao thông, đạo đức người lái xe, kỹ năng PCCC và cứu hộ cứu nạn", "range": "181-205", "count": 25},
    3: {"name": "Kỹ thuật lái xe", "range": "206-263", "count": 58},
    4: {"name": "Cấu tạo và sửa chữa", "range": "264-300", "count": 37},
    5: {"name": "Báo hiệu đường bộ", "range": "301-485", "count": 185},
    6: {"name": "Giải thế sa hình và kỹ năng xử lý tình huống giao thông", "range": "486-600", "count": 115},
}


@st.cache_data(show_spinner=False)
def load_default_bank() -> List[Dict[str, Any]]:
    try:
        data = json.loads(DEFAULT_BANK_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def active_bank(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    return profile.get("official_exam_bank") or load_default_bank()



def validate_bank(bank: List[Dict[str, Any]]) -> Dict[str, Any]:
    expected = {1: 180, 2: 25, 3: 58, 4: 37, 5: 185, 6: 115}
    ids = [q.get('id') for q in bank]
    missing_ids = [i for i in range(1, 601) if i not in set(ids)]
    duplicate_ids = sorted({x for x in ids if ids.count(x) > 1})
    chapter_counts = {}
    for q in bank:
        try: ch = int(q.get('chapter') or 0)
        except Exception: ch = 0
        chapter_counts[ch] = chapter_counts.get(ch, 0) + 1
    return {
        'total': len(bank),
        'answered': sum(1 for q in bank if q.get('answer_index') and q.get('answer')),
        'options_ok': sum(1 for q in bank if isinstance(q.get('options'), list) and len(q.get('options')) >= 2),
        'critical_marked': sum(1 for q in bank if q.get('is_critical')),
        'image_marked': sum(1 for q in bank if q.get('has_original_image')),
        'missing_ids': missing_ids,
        'duplicate_ids': duplicate_ids,
        'chapter_counts': chapter_counts,
        'chapter_ok': all(chapter_counts.get(k, 0) == v for k, v in expected.items()),
    }


def render_validation_tab(bank: List[Dict[str, Any]]) -> None:
    st.markdown('### ✅ Kiểm tra chuẩn bộ 600 câu')
    v = validate_bank(bank)
    c1, c2, c3, c4 = st.columns(4)
    with c1: ui.metric_card('Tổng câu', v['total'], '/600')
    with c2: ui.metric_card('Có đáp án', v['answered'], 'câu')
    with c3: ui.metric_card('Đúng chương', 'OK' if v['chapter_ok'] else 'Review', '6 chương')
    with c4: ui.metric_card('Điểm liệt', v['critical_marked'], '/60')
    if v['total'] == 600 and v['answered'] == 600 and not v['missing_ids'] and not v['duplicate_ids'] and v['chapter_ok']:
        st.success('Bộ 600 câu đạt kiểm tra kỹ thuật cơ bản: đủ ID 1–600, đủ đáp án, đúng số lượng 6 chương.')
    else:
        st.error('Bộ câu hỏi cần kiểm tra lại trước khi dùng ôn thi chính thức.')
    if v['critical_marked'] != 60:
        st.warning('Chưa đánh dấu đủ 60 câu điểm liệt. Hãy dùng CSV để cập nhật cột is_critical khi có danh sách ID chính thức.')
    st.markdown('#### Số câu theo chương')
    expected = {1: 180, 2: 25, 3: 58, 4: 37, 5: 185, 6: 115}
    for ch in range(1, 7):
        got = v['chapter_counts'].get(ch, 0)
        if got == expected[ch]: st.success(f'Chương {ch}: {got}/{expected[ch]} câu')
        else: st.error(f'Chương {ch}: {got}/{expected[ch]} câu')
    with st.expander('Xem chi tiết kiểm tra JSON'):
        st.json(v)


def sample_visual(chapter: int, question_id: int | None = None):
    colors = {1:'#3b82f6',2:'#22c55e',3:'#f59e0b',4:'#8b5cf6',5:'#ef4444',6:'#06b6d4'}
    labels = {1:'QUY TẮC',2:'VĂN HÓA',3:'KỸ THUẬT',4:'CẤU TẠO',5:'BIỂN BÁO',6:'SA HÌNH'}
    c = colors.get(int(chapter or 1), '#3b82f6')
    label = labels.get(int(chapter or 1), 'ÔN THI')
    qtxt = f"CÂU {question_id}" if question_id else "OFFICIAL"
    components.html(f"""
    <div style='border:1px solid #1f2b42;border-radius:18px;background:#0e1628;padding:8px'>
    <svg viewBox='0 0 520 190' width='100%' height='180'>
      <defs><linearGradient id='g' x1='0' x2='1'><stop offset='0' stop-color='{c}'/><stop offset='1' stop-color='#111b2f'/></linearGradient></defs>
      <rect width='520' height='190' rx='18' fill='#0e1628'/>
      <rect x='22' y='24' width='476' height='142' rx='24' fill='url(#g)' opacity='.62' stroke='#334155'/>
      <circle cx='96' cy='95' r='50' fill='{c}' opacity='.9'/>
      <text x='96' y='87' text-anchor='middle' font-size='22' fill='white'>{chapter}</text>
      <text x='96' y='112' text-anchor='middle' font-size='14' fill='white'>{qtxt}</text>
      <text x='286' y='78' text-anchor='middle' font-size='26' font-weight='700' fill='#e2e8f0'>{label}</text>
      <text x='286' y='110' text-anchor='middle' font-size='15' fill='#dbeafe'>Bộ 600 câu chính thức 2025</text>
      <text x='286' y='136' text-anchor='middle' font-size='13' fill='#93a4be'>đáp án trích theo phần gạch chân trong PDF</text>
    </svg>
    </div>
    """, height=195)


def parse_csv(uploaded_file) -> List[Dict[str, Any]]:
    text = uploaded_file.getvalue().decode('utf-8-sig')
    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        if row.get('question'):
            rows.append({k: (v or '').strip() for k, v in row.items()})
    return rows


def normalize_import(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for i, row in enumerate(rows, 1):
        options = [row.get('option1',''), row.get('option2',''), row.get('option3',''), row.get('option4','')]
        options = [{'index': j+1, 'text': x} for j, x in enumerate(options) if x]
        answer_index = row.get('answer_index','')
        try:
            answer_index = int(answer_index) if answer_index else None
        except Exception:
            answer_index = None
        answer = row.get('answer','') or next((o['text'] for o in options if o['index'] == answer_index), '')
        groups = row.get('license_groups') or row.get('license_group') or 'B/C/D/E/FC'
        out.append({
            'id': int(row.get('id') or i),
            'license_groups': [x.strip() for x in groups.replace(',', ';').split(';') if x.strip()],
            'chapter': int(row.get('chapter') or 1),
            'chapter_name': row.get('chapter_name',''),
            'question': row.get('question',''),
            'options': options,
            'answer_index': answer_index,
            'answer': answer,
            'is_critical': str(row.get('is_critical','')).lower() in ('1','true','yes','co','có'),
            'source_page': row.get('source_page',''),
            'has_original_image': str(row.get('has_original_image','')).lower() in ('1','true','yes','co','có'),
        })
    return out


def filter_bank(bank: List[Dict[str, Any]], license_group: str, chapter: str, only_critical: bool, search: str = ""):
    pool = bank
    if license_group != 'Tất cả':
        pool = [q for q in pool if license_group in q.get('license_groups', [])]
    if chapter != 'Tất cả':
        pool = [q for q in pool if str(q.get('chapter')) == str(chapter)]
    if only_critical:
        pool = [q for q in pool if q.get('is_critical')]
    if search.strip():
        s = search.lower().strip()
        pool = [q for q in pool if s == str(q.get('id')) or s in q.get('question','').lower() or any(s in o.get('text','').lower() for o in q.get('options', []))]
    return pool


def show_question(q: Dict[str, Any], idx: int, reveal: bool = False):
    st.markdown(f"### Câu {idx} · ID {q.get('id')}" + (' · ⚠️ Điểm liệt' if q.get('is_critical') else ''))
    sample_visual(int(q.get('chapter') or 1), int(q.get('id') or idx))
    st.write(q.get('question'))
    for opt in q.get('options') or []:
        prefix = '✅ ' if reveal and opt.get('index') == q.get('answer_index') else ''
        st.markdown(f"{prefix}**{opt.get('index')}.** {opt.get('text')}")
    if reveal:
        st.success(f"Đáp án đúng: {q.get('answer_index')}. {q.get('answer')}")
    if q.get('has_original_image'):
        st.caption(f"Câu này có khả năng liên quan hình/sa hình trong PDF gốc · Trang PDF khoảng: {q.get('source_page')}")


def official_quiz(profile: Dict[str, Any], save_cb):
    bank = active_bank(profile)
    if not bank:
        st.error('Không tải được bộ 600 câu. Hãy kiểm tra file data/official_600_questions_2025_extracted.json có nằm đúng trong thư mục data/ trên GitHub không.')
        return
    license_groups = ['Tất cả'] + sorted({g for q in bank for g in q.get('license_groups', [])})
    chapters = ['Tất cả'] + [str(i) for i in range(1, 7)]
    c1, c2, c3 = st.columns(3)
    with c1:
        lg = st.selectbox('Hạng bằng / nhóm câu', license_groups, key='official_lg')
    with c2:
        ch = st.selectbox('Chương', chapters, key='official_ch')
    with c3:
        max_count = max(5, min(35, len(bank)))
        count = st.slider('Số câu', 5, max_count, min(10, max_count), key='official_count')
    critical = st.checkbox('Chỉ câu điểm liệt / tình huống mất an toàn nghiêm trọng', key='official_critical')
    if critical and not any(q.get('is_critical') for q in bank):
        st.warning('Bộ PDF đã trích xuất chưa có danh sách 60 câu điểm liệt được đánh dấu riêng. Nếu bạn có danh sách ID điểm liệt, hãy cập nhật cột is_critical trong CSV rồi import lại.')
    pool = filter_bank(bank, lg, ch, critical)
    if not pool:
        st.warning('Không có câu phù hợp bộ lọc.')
        return
    random.shuffle(pool)
    quiz = pool[:min(count, len(pool))]
    with st.form('official_quiz_form'):
        answers=[]
        for idx,q in enumerate(quiz,1):
            st.markdown(f"### Câu {idx} · ID {q.get('id')}" + (' · ⚠️ Điểm liệt' if q.get('is_critical') else ''))
            sample_visual(int(q.get('chapter') or 1), int(q.get('id') or idx))
            st.write(q.get('question'))
            opt_texts = [f"{o.get('index')}. {o.get('text')}" for o in q.get('options', [])]
            answers.append(st.radio('Chọn đáp án', opt_texts, key=f"official_{q.get('id')}_{idx}", label_visibility='collapsed'))
        submitted=st.form_submit_button('📌 Chấm điểm & xem giải thích')
    if submitted:
        correct=0; critical_wrong=False
        st.markdown('## 📋 Kết quả chi tiết')
        for q,a in zip(quiz,answers):
            chosen_index = int(a.split('.',1)[0]) if a else None
            ok = chosen_index == q.get('answer_index')
            if ok: correct += 1
            elif q.get('is_critical'): critical_wrong = True
            with st.container(border=True):
                st.markdown(f"**ID {q.get('id')}. {q.get('question')}**")
                if ok:
                    st.success(f"✅ Đúng · Đáp án: {q.get('answer_index')}. {q.get('answer')}")
                else:
                    st.error(f"❌ Sai · Bạn chọn: {a}")
                    st.info(f"Đáp án đúng: {q.get('answer_index')}. {q.get('answer')}")
                st.caption(f"Chương {q.get('chapter')} · Trang PDF khoảng {q.get('source_page')}")
        score = round(correct/len(quiz)*100)
        st.metric('Điểm', f'{score}%', f'{correct}/{len(quiz)}')
        profile.setdefault('official_exam_history', []).append({'score': score, 'correct': correct, 'total': len(quiz), 'license_group': lg, 'chapter': ch})
        save_cb(profile)
        if critical_wrong:
            st.error('Có câu điểm liệt bị sai: bài lý thuyết có thể không đạt nếu sai câu điểm liệt.')
        elif score >= 80:
            st.success('Kết quả tốt. Hãy tiếp tục ôn câu sai và chương yếu.')
        else:
            st.warning('Nên ôn lại chương yếu và làm lại bộ đề.')


def render(profile: Dict[str, Any], save_cb) -> None:
    st.title('🪪 Bộ 600 câu chính thức 2025')
    st.caption('Đã tích hợp PDF 600 câu bạn vừa gửi: app có sẵn 600 câu + đáp án trích theo phần gạch chân trong PDF.')
    bank = active_bank(profile)
    tabs = st.tabs(['📌 Tổng quan','✅ Kiểm tra chuẩn','🧪 Ôn thi chính thức','🔎 Tìm kiếm / xem đáp án','⬆️ Import / Export','📱 Mobile'])
    with tabs[0]:
        st.markdown('### Dữ liệu đã tích hợp')
        c1, c2, c3, c4 = st.columns(4)
        with c1: ui.metric_card('Tổng câu', len(bank), 'câu')
        with c2: ui.metric_card('Có đáp án', sum(1 for q in bank if q.get('answer_index')), 'câu')
        with c3: ui.metric_card('Có hình/sa hình', sum(1 for q in bank if q.get('has_original_image')), 'câu')
        with c4: ui.metric_card('Chương', 6, 'phần')
        st.markdown('### Cấu trúc 6 chương')
        cols = st.columns(3)
        for i, (ch, meta) in enumerate(CHAPTERS.items()):
            with cols[i % 3]:
                ui.card(str(ch), meta['name'], f"Câu {meta['range']} · {meta['count']} câu", 'Chương')
                sample_visual(ch)
        if DEFAULT_PDF_PATH.exists():
            st.download_button('⬇️ Tải PDF gốc đã tích hợp', DEFAULT_PDF_PATH.read_bytes(), 'official_600_questions_2025.pdf', 'application/pdf')
        if DEFAULT_CSV_PATH.exists():
            st.download_button('⬇️ Tải CSV trích xuất 600 câu', DEFAULT_CSV_PATH.read_bytes(), 'official_600_questions_2025_extracted.csv', 'text/csv')
        st.info('Ghi chú: PDF gốc nêu có 60 câu tình huống mất an toàn nghiêm trọng, nhưng bản trích xuất tự động không tự đánh dấu được chính xác 60 câu này nếu PDF không có ký hiệu riêng trong text. Bạn có thể bổ sung danh sách ID điểm liệt bằng CSV sau.')
    with tabs[1]:
        render_validation_tab(bank)
    with tabs[2]:
        official_quiz(profile, save_cb)
    with tabs[3]:
        st.markdown('### Tìm kiếm nhanh trong bộ 600 câu')
        c1, c2, c3 = st.columns(3)
        with c1: lg = st.selectbox('Hạng bằng', ['Tất cả'] + sorted({g for q in bank for g in q.get('license_groups', [])}), key='search_lg')
        with c2: ch = st.selectbox('Chương', ['Tất cả'] + [str(i) for i in range(1,7)], key='search_ch')
        with c3: critical = st.checkbox('Chỉ điểm liệt', key='search_critical')
        query = st.text_input('Nhập từ khóa hoặc ID câu')
        results = filter_bank(bank, lg, ch, critical, query)[:50]
        st.caption(f'Hiển thị {len(results)} kết quả đầu tiên.')
        for q in results:
            with st.expander(f"Câu {q.get('id')} · Chương {q.get('chapter')} · {q.get('question')[:90]}"):
                show_question(q, int(q.get('id') or 0), reveal=True)
    with tabs[4]:
        st.markdown('### Import CSV khác nếu cần chỉnh dữ liệu')
        st.code('id,license_groups,chapter,chapter_name,question,option1,option2,option3,option4,answer_index,answer,is_critical,source_page,has_original_image', language='text')
        if DEFAULT_CSV_PATH.exists():
            st.download_button('⬇️ Tải CSV mẫu/trích xuất hiện tại', DEFAULT_CSV_PATH.read_bytes(), 'official_600_questions_2025_extracted.csv', 'text/csv')
        up = st.file_uploader('Upload CSV bộ đề chính thức đã chỉnh', type=['csv'])
        if up:
            rows = normalize_import(parse_csv(up))
            st.success(f'Đã đọc {len(rows)} câu.')
            if st.button('💾 Lưu CSV này vào hồ sơ hiện tại'):
                profile['official_exam_bank'] = rows
                save_cb(profile)
                st.success('Đã lưu bộ đề chính thức vào hồ sơ.')
        if profile.get('official_exam_bank'):
            if st.button('↩️ Quay về bộ 600 câu mặc định trong app'):
                profile.pop('official_exam_bank', None)
                save_cb(profile)
                st.success('Đã quay về bộ mặc định.')
    with tabs[5]:
        st.markdown('''
        **Cách ôn nhanh trên điện thoại:**
        1. Vào tab **Ôn thi chính thức**.
        2. Chọn hạng bằng và chương yếu.
        3. Làm 10 câu/lượt để không bị mệt.
        4. Sai câu nào, đọc lại đáp án đúng và tìm lại bằng ID câu.
        5. Trước ngày thi, ưu tiên các chương: quy tắc, biển báo, sa hình.
        ''')
