from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

import streamlit as st

from . import ui

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OFFICIAL_JSON = DATA_DIR / "official_600_questions_2025_extracted.json"
OFFICIAL_CSV = DATA_DIR / "official_600_questions_2025_extracted.csv"
OFFICIAL_PDF = DATA_DIR / "official_600_questions_2025.pdf"

EXPECTED_CHAPTER_COUNTS = {1: 180, 2: 25, 3: 58, 4: 37, 5: 185, 6: 115}
REQUIRED_FILES = [
    "app.py", "requirements.txt", "packages.txt", "modules", "data", ".streamlit/config.toml",
    "modules/official_exam.py", "modules/driving.py", "modules/english.py", "modules/performance.py",
    "modules/health_check.py", "data/official_600_questions_2025_extracted.json",
]


def _status_box(status: str, title: str, body: str) -> None:
    cls = {"ok": "health-ok", "warn": "health-warn", "bad": "health-bad"}.get(status, "health-warn")
    icon = {"ok": "✅", "warn": "⚠️", "bad": "❌"}.get(status, "ℹ️")
    st.markdown(f"<div class='{cls}'><b>{icon} {title}</b><br><span class='muted'>{body}</span></div>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_official_questions() -> List[Dict[str, Any]]:
    try:
        data = json.loads(OFFICIAL_JSON.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def validate_official_bank(bank: List[Dict[str, Any]]) -> Tuple[List[Dict[str, str]], Dict[str, Any]]:
    checks: List[Dict[str, str]] = []
    def add(status, name, detail): checks.append({"status": status, "name": name, "detail": detail})
    total = len(bank)
    add("ok" if total == 600 else "bad", "Tổng số câu", f"Hiện có {total}/600 câu.")
    ids = [q.get("id") for q in bank]
    id_set = set(ids)
    missing_ids = [i for i in range(1, 601) if i not in id_set]
    duplicate_ids = sorted({x for x in ids if ids.count(x) > 1})[:20]
    add("ok" if not missing_ids and not duplicate_ids else "bad", "ID câu 1–600", f"Thiếu {len(missing_ids)} ID; trùng {len(duplicate_ids)} ID." + (f" Thiếu ví dụ: {missing_ids[:10]}" if missing_ids else ""))
    answered = sum(1 for q in bank if q.get("answer_index") and q.get("answer"))
    add("ok" if answered == total and total else "bad", "Đáp án", f"Có đáp án: {answered}/{total} câu.")
    opt_ok = sum(1 for q in bank if isinstance(q.get("options"), list) and len(q.get("options")) >= 2)
    add("ok" if opt_ok == total and total else "bad", "Phương án trả lời", f"Có ít nhất 2 phương án: {opt_ok}/{total} câu.")
    chapter_counts = {}
    for q in bank:
        try: ch = int(q.get("chapter") or 0)
        except Exception: ch = 0
        chapter_counts[ch] = chapter_counts.get(ch, 0) + 1
    chapter_bad = {ch: (chapter_counts.get(ch, 0), expected) for ch, expected in EXPECTED_CHAPTER_COUNTS.items() if chapter_counts.get(ch, 0) != expected}
    add("ok" if not chapter_bad and total else "bad", "Cấu trúc 6 chương", " ; ".join([f"Ch.{ch}: {chapter_counts.get(ch,0)}/{ex}" for ch, ex in EXPECTED_CHAPTER_COUNTS.items()]))
    critical = sum(1 for q in bank if q.get("is_critical"))
    add("ok" if critical == 60 else "warn", "60 câu điểm liệt", f"Đang đánh dấu {critical}/60 câu. Nếu chưa có danh sách ID chính thức, hãy bổ sung qua CSV.")
    images = sum(1 for q in bank if q.get("has_original_image"))
    add("ok" if images > 0 else "warn", "Câu có hình/sa hình", f"Đang đánh dấu {images} câu có hình/sa hình.")
    summary = {"total": total, "answered": answered, "critical": critical, "images": images, "chapter_counts": chapter_counts, "missing_ids": missing_ids[:50], "duplicate_ids": duplicate_ids}
    return checks, summary


def validate_required_files() -> List[Dict[str, str]]:
    out = []
    for rel in REQUIRED_FILES:
        p = ROOT / rel
        ok = p.exists()
        out.append({"status": "ok" if ok else "bad", "name": rel, "detail": "Có" if ok else "Thiếu file/thư mục này trên repo."})
    return out


def validate_imports() -> List[Dict[str, str]]:
    modules = ["streamlit", "modules.auth", "modules.db", "modules.official_exam", "modules.performance", "modules.health_check"]
    out = []
    for name in modules:
        try:
            importlib.import_module(name)
            out.append({"status": "ok", "name": name, "detail": "Import OK"})
        except Exception as exc:
            out.append({"status": "bad", "name": name, "detail": str(exc)[:220]})
    # optional heavy imports
    for name in ["yt_dlp", "google.genai", "pywebpush"]:
        try:
            importlib.import_module(name)
            out.append({"status": "ok", "name": name, "detail": "Optional package có sẵn"})
        except Exception:
            out.append({"status": "warn", "name": name, "detail": "Optional package chưa có hoặc chỉ cần khi mở đúng chức năng."})
    return out


def render(db=None, user: Dict[str, Any] | None = None, profile: Dict[str, Any] | None = None) -> None:
    st.title("🩺 App Health Check")
    st.caption("Kiểm tra sức khỏe app trước/sau khi deploy Streamlit Cloud: file, module, bộ 600 câu, database, optional tools và mobile mode.")
    bank = load_official_questions()
    official_checks, summary = validate_official_bank(bank)
    file_checks = validate_required_files()
    import_checks = validate_imports()

    st.markdown("## 1) Kiểm tra nhanh")
    total_bad = sum(1 for x in official_checks + file_checks + import_checks if x["status"] == "bad")
    total_warn = sum(1 for x in official_checks + file_checks + import_checks if x["status"] == "warn")
    c1, c2, c3, c4 = st.columns(4)
    with c1: ui.metric_card("Official questions", summary.get("total", 0), "câu")
    with c2: ui.metric_card("Bad", total_bad, "lỗi nặng")
    with c3: ui.metric_card("Warnings", total_warn, "cảnh báo")
    with c4: ui.metric_card("Critical marked", summary.get("critical", 0), "/60")
    if total_bad == 0:
        st.success("Không thấy lỗi nặng trong Health Check cơ bản. Nếu deploy vẫn lỗi, mở log Streamlit Cloud để xem chi tiết.")
    else:
        st.error("Có lỗi nặng cần sửa trước khi public link.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🪪 Bộ 600 câu", "📦 File repo", "🐍 Imports", "🗄️ Database", "☁️ Cloud checklist"])
    with tab1:
        for x in official_checks: _status_box(x["status"], x["name"], x["detail"])
        with st.expander("Xem summary JSON"):
            st.json(summary)
        if OFFICIAL_CSV.exists(): st.download_button("⬇️ Tải CSV 600 câu để chỉnh", OFFICIAL_CSV.read_bytes(), "official_600_questions_2025_extracted.csv", "text/csv")
    with tab2:
        for x in file_checks: _status_box(x["status"], x["name"], x["detail"])
        st.info("Nếu lỗi thiếu modules/: trên GitHub cần thấy app.py, modules/, data/, requirements.txt nằm ngay ngoài cùng repo, không bị lồng trong thư mục con.")
    with tab3:
        for x in import_checks: _status_box(x["status"], x["name"], x["detail"])
        st.info("Google Veo, TikTok và Web Push là optional: không nên làm dashboard lỗi chỉ vì chưa dùng các tính năng đó.")
    with tab4:
        if db and user:
            try:
                prof = db.load_profile(user["id"])
                _status_box("ok", "Database profile", f"Đọc profile OK cho user {user.get('email','')}")
                try:
                    meds = db.list_medications(user["id"])
                    _status_box("ok", "Medication table", f"Đọc thuốc OK: {len(meds)} dòng")
                except Exception as exc:
                    _status_box("warn", "Medication table", f"Không đọc được danh sách thuốc: {exc}")
            except Exception as exc:
                _status_box("bad", "Database", f"Không đọc được profile: {exc}")
        else:
            _status_box("warn", "Database", "Không có db/user được truyền vào Health Check.")
    with tab5:
        st.markdown("""
        ### Checklist test cố định trên Streamlit Cloud
        1. Reboot app sau khi upload source.
        2. Mở app trên desktop và mobile.
        3. Đăng ký tài khoản A, làm 1 quiz, lưu profile.
        4. Đăng xuất, đăng ký tài khoản B, kiểm tra không thấy dữ liệu A.
        5. Vào **Bộ 600 câu chính thức**, kiểm tra tổng 600 câu và làm 5 câu.
        6. Vào **English**, mở Conversation và Quiz.
        7. Vào **Performance Mode**, bật chế độ nhẹ/mobile.
        8. Vào **Google Veo/TikTok** chỉ khi cần; nếu thiếu key/lib app chính vẫn phải chạy.
        9. Vào **Sao lưu & dữ liệu**, tải backup JSON.
        10. Mở **Manage app → Logs** nếu còn lỗi đỏ.
        """)
        st.download_button("⬇️ Tải checklist markdown", CLOUD_TEST_CHECKLIST.encode("utf-8"), "STREAMLIT_CLOUD_TEST_CHECKLIST.md", "text/markdown")


CLOUD_TEST_CHECKLIST = """# Streamlit Cloud Test Checklist - AutoLearn v15.8.1

- [ ] Repo có app.py, modules/, data/, requirements.txt ở root
- [ ] App build thành công sau Reboot
- [ ] Đăng ký tài khoản A thành công
- [ ] Đăng xuất, đăng nhập lại tài khoản A thành công
- [ ] Tài khoản A làm 1 quiz và lưu profile
- [ ] Đăng ký tài khoản B, không thấy dữ liệu của A
- [ ] Bộ 600 câu hiện đủ 600 câu
- [ ] Làm quiz 5 câu trong Bộ 600 câu
- [ ] English Conversation mở được
- [ ] English Quiz mở được
- [ ] Performance Mode lưu được chế độ nhẹ/mobile
- [ ] Google Veo/TikTok không làm dashboard lỗi khi chưa mở trang
- [ ] Backup JSON tải được
- [ ] App mở được trên điện thoại
- [ ] Logs không còn ModuleNotFoundError
"""
