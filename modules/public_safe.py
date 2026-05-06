
from __future__ import annotations
import csv
import io
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import streamlit as st

from . import ui
from . import official_exam

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CRITICAL_TEMPLATE = DATA_DIR / "official_critical_ids_template.csv"


def _bank(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    return official_exam.active_bank(profile)


def _parse_ids_from_text(raw: str) -> Set[int]:
    ids: Set[int] = set()
    for part in raw.replace(";", ",").replace("\n", ",").split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            try:
                a, b = [int(x.strip()) for x in part.split("-", 1)]
                for i in range(min(a, b), max(a, b) + 1):
                    ids.add(i)
            except Exception:
                pass
        else:
            try:
                ids.add(int(part))
            except Exception:
                pass
    return {i for i in ids if 1 <= i <= 600}


def _csv_bytes(bank: List[Dict[str, Any]]) -> bytes:
    fields = ["id", "chapter", "question", "answer_index", "answer", "is_critical", "has_original_image", "license_groups"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields)
    writer.writeheader()
    for q in bank:
        writer.writerow({
            "id": q.get("id"),
            "chapter": q.get("chapter"),
            "question": q.get("question"),
            "answer_index": q.get("answer_index"),
            "answer": q.get("answer"),
            "is_critical": str(bool(q.get("is_critical"))).lower(),
            "has_original_image": str(bool(q.get("has_original_image"))).lower(),
            "license_groups": "|".join(q.get("license_groups") or []),
        })
    return buf.getvalue().encode("utf-8-sig")


def deep_validate(bank: List[Dict[str, Any]]) -> Tuple[List[Dict[str, str]], Dict[str, Any]]:
    checks: List[Dict[str, str]] = []
    def add(status: str, name: str, detail: str):
        checks.append({"status": status, "name": name, "detail": detail})

    ids = [q.get("id") for q in bank]
    id_set = set(ids)
    missing = [i for i in range(1, 601) if i not in id_set]
    dupes = sorted({x for x in ids if ids.count(x) > 1 and x is not None})

    add("ok" if len(bank) == 600 else "bad", "Tổng số câu", f"{len(bank)}/600")
    add("ok" if not missing and not dupes else "bad", "ID 1–600", f"Thiếu {len(missing)}; trùng {len(dupes)}")

    empty_questions = [q.get("id") for q in bank if not str(q.get("question", "")).strip()]
    add("ok" if not empty_questions else "bad", "Nội dung câu hỏi", f"Câu rỗng: {empty_questions[:10]}")

    bad_options = [q.get("id") for q in bank if not isinstance(q.get("options"), list) or len(q.get("options")) < 2]
    add("ok" if not bad_options else "bad", "Phương án trả lời", f"Lỗi phương án: {bad_options[:10]}")

    bad_answers = []
    for q in bank:
        idx = q.get("answer_index")
        opt_indexes = {o.get("index") for o in q.get("options", []) if isinstance(o, dict)}
        if idx not in opt_indexes or not q.get("answer"):
            bad_answers.append(q.get("id"))
    add("ok" if not bad_answers else "bad", "Đáp án khớp phương án", f"Lỗi: {bad_answers[:10]}")

    expected = {1: 180, 2: 25, 3: 58, 4: 37, 5: 185, 6: 115}
    chapter_counts: Dict[int, int] = {}
    chapter_range_bad = []
    ranges = {1: (1, 180), 2: (181, 205), 3: (206, 263), 4: (264, 300), 5: (301, 485), 6: (486, 600)}
    for q in bank:
        try:
            ch = int(q.get("chapter") or 0)
            qid = int(q.get("id") or 0)
        except Exception:
            ch, qid = 0, 0
        chapter_counts[ch] = chapter_counts.get(ch, 0) + 1
        lo, hi = ranges.get(ch, (None, None))
        if lo is None or not (lo <= qid <= hi):
            chapter_range_bad.append(qid)
    chapter_ok = all(chapter_counts.get(ch, 0) == expected[ch] for ch in expected)
    add("ok" if chapter_ok else "bad", "Số lượng 6 chương", " ; ".join([f"Ch.{ch}: {chapter_counts.get(ch,0)}/{expected[ch]}" for ch in expected]))
    add("ok" if not chapter_range_bad else "bad", "ID đúng khoảng chương", f"Lỗi khoảng chương: {chapter_range_bad[:10]}")

    critical = [q.get("id") for q in bank if q.get("is_critical")]
    add("ok" if len(critical) == 60 else "warn", "60 câu điểm liệt", f"Đã đánh dấu {len(critical)}/60")

    missing_license = [q.get("id") for q in bank if not q.get("license_groups")]
    add("ok" if not missing_license else "warn", "Phân loại hạng bằng", f"Thiếu license_groups: {missing_license[:10]}")

    summary = {
        "total": len(bank),
        "missing": missing[:50],
        "duplicates": dupes[:50],
        "bad_options": bad_options[:50],
        "bad_answers": bad_answers[:50],
        "chapter_counts": chapter_counts,
        "chapter_range_bad": chapter_range_bad[:50],
        "critical_count": len(critical),
        "critical_ids": critical[:80],
        "missing_license": missing_license[:50],
    }
    return checks, summary


def render(profile: Dict[str, Any], save_cb) -> None:
    st.title("🛡️ Public Safe Center")
    st.caption("Trung tâm phát hành an toàn: kiểm tra sâu bộ 600 câu, đánh dấu 60 câu điểm liệt, tối ưu public và ghi chú lỗi sau deploy.")

    bank = _bank(profile)
    tabs = st.tabs(["✅ Kiểm tra 600 câu", "🚨 60 câu điểm liệt", "📱 Public mobile", "🧯 Lỗi sau deploy", "📦 Release checklist"])

    with tabs[0]:
        checks, summary = deep_validate(bank)
        cols = st.columns(4)
        with cols[0]: ui.metric_card("Tổng câu", summary["total"], "/600")
        with cols[1]: ui.metric_card("Điểm liệt", summary["critical_count"], "/60")
        with cols[2]: ui.metric_card("Lỗi đáp án", len(summary["bad_answers"]), "câu")
        with cols[3]: ui.metric_card("Thiếu ID", len(summary["missing"]), "câu")
        for c in checks:
            css = {"ok": "safe-ok", "warn": "safe-warn", "bad": "safe-bad"}.get(c["status"], "safe-warn")
            icon = {"ok": "✅", "warn": "⚠️", "bad": "❌"}.get(c["status"], "ℹ️")
            st.markdown(f"<div class='public-safe-card {css}'><b>{icon} {c['name']}</b><br><span class='muted'>{c['detail']}</span></div>", unsafe_allow_html=True)
        with st.expander("JSON kiểm tra chi tiết"):
            st.json(summary)

    with tabs[1]:
        st.markdown("### 🚨 Đánh dấu 60 câu điểm liệt")
        st.warning("Chỉ đánh dấu khi bạn có danh sách ID chuẩn. Nếu chưa có, giữ nguyên để tránh học sai.")
        raw = st.text_area("Dán danh sách ID câu điểm liệt, ví dụ: 1, 4, 12 hoặc 1-10", height=120)
        uploaded = st.file_uploader("Hoặc upload CSV có cột id hoặc question_id", type=["csv"], key="critical_upload")
        ids = set()
        if raw.strip():
            ids |= _parse_ids_from_text(raw)
        if uploaded is not None:
            try:
                text = uploaded.getvalue().decode("utf-8-sig")
                reader = csv.DictReader(io.StringIO(text))
                for row in reader:
                    val = row.get("id") or row.get("question_id") or row.get("qid")
                    if val:
                        ids |= _parse_ids_from_text(str(val))
            except Exception as exc:
                st.error("Không đọc được CSV điểm liệt.")
                st.caption(str(exc))
        st.caption(f"Đang nhận diện {len(ids)} ID hợp lệ.")
        if st.button("✅ Áp dụng danh sách điểm liệt vào profile"):
            if len(ids) != 60:
                st.error(f"Danh sách cần đúng 60 ID. Hiện có {len(ids)} ID.")
            else:
                new_bank = []
                for q in bank:
                    qq = dict(q)
                    qq["is_critical"] = int(qq.get("id", 0)) in ids
                    new_bank.append(qq)
                profile["official_exam_bank"] = new_bank
                save_cb(profile)
                st.success("Đã đánh dấu 60 câu điểm liệt vào profile hiện tại.")
        st.download_button("⬇️ Tải CSV bộ 600 câu hiện tại", data=_csv_bytes(bank), file_name="official_600_questions_with_critical_flags.csv", mime="text/csv")
        if CRITICAL_TEMPLATE.exists():
            st.download_button("⬇️ Tải template nhập 60 câu điểm liệt", data=CRITICAL_TEMPLATE.read_bytes(), file_name="official_critical_ids_template.csv", mime="text/csv")

    with tabs[2]:
        st.markdown("### 📱 Public mobile checklist")
        checklist = [
            "Mở app trên điện thoại thật",
            "Đăng nhập / đăng xuất được",
            "Bấm radio sidebar dễ không",
            "Làm 5 câu bộ 600 câu không bị tràn màn hình",
            "Nút chấm điểm đủ lớn",
            "English conversation đọc dễ",
            "Nhắc thuốc thêm/sửa dễ",
            "Google Veo/TikTok không làm dashboard chậm",
        ]
        for item in checklist:
            st.checkbox(item, key=f"public_mobile_{item}")
        st.info("Gợi ý: giữ Performance Mode ở 'Nhẹ' hoặc 'Cân bằng' khi public cho nhiều người dùng.")

    with tabs[3]:
        st.markdown("### 🧯 Nhật ký lỗi sau deploy")
        notes = profile.setdefault("deploy_error_notes", [])
        new_note = st.text_area("Ghi lỗi thực tế sau deploy để sửa theo từng lỗi", placeholder="Ví dụ: Streamlit báo thiếu modules/, hoặc official JSON không load được...")
        if st.button("➕ Lưu ghi chú lỗi"):
            if new_note.strip():
                notes.append({"note": new_note.strip()})
                save_cb(profile)
                st.success("Đã lưu ghi chú lỗi.")
        for i, n in enumerate(notes[-10:], 1):
            st.markdown(f"<div class='deploy-fix'><b>Lỗi #{i}</b><br>{n.get('note','')}</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='deploy-fix'>
        <b>3 lỗi hay gặp nhất</b><br>
        1) ModuleNotFoundError → upload thiếu thư mục modules/.<br>
        2) Không đọc được 600 câu → thiếu thư mục data/ hoặc file JSON.<br>
        3) App chậm → bật Performance Mode = Nhẹ, không mở Veo/TikTok ở dashboard.
        </div>
        """, unsafe_allow_html=True)

    with tabs[4]:
        st.markdown("### 📦 Release checklist trước khi public")
        items = [
            "App mở được sau Reboot Streamlit",
            "App Health Check không có lỗi đỏ quan trọng",
            "Bộ 600 câu đủ 600/600",
            "Đáp án khớp phương án",
            "Đã biết trạng thái 60 câu điểm liệt",
            "Terms & Privacy đã hiển thị",
            "Tài khoản A không thấy dữ liệu B",
            "Backup JSON tải được",
            "Veo/TikTok chỉ load khi mở trang riêng",
            "Mobile test đạt",
        ]
        state = profile.setdefault("public_release_checklist", {})
        for item in items:
            state[item] = st.checkbox(item, value=bool(state.get(item)), key=f"release_{item}")
        done = sum(1 for x in state.values() if x)
        st.progress(done / len(items))
        st.caption(f"Hoàn thành {done}/{len(items)} mục.")
        if st.button("💾 Lưu release checklist"):
            save_cb(profile)
            st.success("Đã lưu checklist.")
