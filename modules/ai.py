from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

from . import config


def _profile_counts(profile: Dict[str, Any], meds_count: int = 0) -> Dict[str, int]:
    driving = profile.get("driving", {})
    english = profile.get("english", {})
    return {
        "driving_completed": len(driving.get("completed", [])),
        "driving_quiz": len(driving.get("quiz_history", [])),
        "driving_wrong": len(driving.get("wrong_bank", {})),
        "english_words": len(english.get("learned_words", [])),
        "english_quiz": len(english.get("quiz_history", [])),
        "english_wrong": len(english.get("wrong_bank", {})),
        "meds": meds_count,
    }


def offline_suggestions(profile: Dict[str, Any], meds_count: int = 0) -> List[str]:
    counts = _profile_counts(profile, meds_count)
    suggestions: List[str] = []
    if counts["driving_wrong"]:
        suggestions.append(f"Ôn {counts['driving_wrong']} câu lái xe đang sai trước khi học bài mới.")
    elif counts["driving_quiz"] < 3:
        suggestions.append("Làm 5 câu Quiz lái xe để tạo dữ liệu điểm yếu cho hệ gợi ý nội bộ.")
    else:
        suggestions.append("Chạy mô phỏng chuyển làn hoặc trời mưa 7 phút để biến lý thuyết thành phản xạ.")

    if counts["english_words"] < 10:
        suggestions.append("Học 5 từ tiếng Anh mới, nghe phát âm và đặt 1 câu ngắn với mỗi từ.")
    elif counts["english_wrong"]:
        suggestions.append(f"Ôn {counts['english_wrong']} câu English sai rồi luyện nói lại 3 câu mẫu.")
    else:
        suggestions.append("Luyện Speaking Coach 7 phút để biến từ vựng thành phản xạ nói.")

    if counts["meds"]:
        suggestions.append("Kiểm tra lịch thuốc hôm nay, xác nhận từng liều ngay sau khi uống và xem cảnh báo thuốc sắp hết.")
    else:
        suggestions.append("Thêm thuốc đầu tiên cho mẹ để bật hệ thống nhắc thuốc ngoài app.")

    suggestions.append("Cuối ngày vào Backup để tải bản sao JSON về máy hoặc lưu trên cloud riêng.")
    return suggestions


def final_score(profile: Dict[str, Any], meds_count: int = 0) -> int:
    counts = _profile_counts(profile, meds_count)
    score = 20
    score += min(25, counts["driving_completed"] * 4)
    score += min(20, counts["driving_quiz"] * 3)
    score += min(20, counts["english_words"] * 2)
    score += min(10, counts["meds"] * 3)
    score += 5 if profile.get("notification", {}).get("email_enabled") else 0
    return max(0, min(100, score))


def _load_cache() -> Dict[str, str]:
    if not config.AI_CACHE_ENABLED:
        return {}
    path = Path(config.AI_CACHE_PATH)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_cache(cache: Dict[str, str]) -> None:
    if not config.AI_CACHE_ENABLED:
        return
    try:
        path = Path(config.AI_CACHE_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def _cache_key(module: str, user_text: str, profile: Dict[str, Any], meds_count: int) -> str:
    counts = _profile_counts(profile, meds_count)
    raw = json.dumps({"module": module, "text": user_text.lower().strip(), "counts": counts}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _extract_focus(text: str) -> str:
    text_l = text.lower()
    keywords = [
        ("rẽ làn", "rẽ làn/nhập làn"), ("chuyển làn", "rẽ làn/nhập làn"), ("điểm mù", "điểm mù"),
        ("mưa", "đi trời mưa"), ("biển báo", "biển báo"), ("sa hình", "sa hình"), ("vòng xuyến", "vòng xuyến"),
        ("thuốc", "lịch thuốc của mẹ"), ("huyết áp", "theo dõi sức khỏe"),
        ("speaking", "luyện nói tiếng Anh"), ("listening", "luyện nghe tiếng Anh"), ("grammar", "ngữ pháp"),
        ("tiktok", "TikTok hợp lệ"), ("backup", "sao lưu dữ liệu"), ("supabase", "database/Supabase"),
    ]
    for key, label in keywords:
        if key in text_l:
            return label
    return "mục tiêu hiện tại"


def _plan_for_module(module: str, focus: str, counts: Dict[str, int]) -> List[str]:
    module_l = module.lower()
    if "lái" in module_l or "driving" in module_l:
        return [
            f"Ôn nhanh phần {focus}: đọc 1 mẹo, xem hình minh họa, rồi làm 5 câu quiz liên quan.",
            "Chạy 1 mô phỏng trong 5–7 phút: chỉnh tốc độ/khoảng cách/thời tiết để hiểu rủi ro.",
            "Ghi lại 1 lỗi mình hay nhầm vào ôn sai; hôm sau chỉ ôn lỗi đó trước khi học bài mới.",
        ]
    if "english" in module_l or "tiếng anh" in module_l:
        return [
            f"Học 3–5 từ/câu về {focus}, nghe 2 lần, đọc theo 2 lần, rồi tự đặt 1 câu ngắn.",
            "Làm 5 câu English Quiz; câu sai đưa vào wrong-bank để ôn lại cuối ngày.",
            "Luyện Speaking Coach 5 phút, ưu tiên nói chậm – rõ – đúng hơn là nói nhanh.",
        ]
    if "thuốc" in module_l or "care" in module_l or "mẹ" in module_l:
        return [
            "Kiểm tra lịch thuốc hôm nay theo 3 mốc: sáng – trưa – tối.",
            "Sau mỗi lần mẹ uống, bấm Đã uống/Uống trễ ngay để báo cáo không bị sai.",
            "Nếu có triệu chứng lạ hoặc quên liều, ghi chú lại và hỏi bác sĩ/dược sĩ; không tự ý uống bù.",
        ]
    if "tiktok" in module_l:
        return [
            "Chỉ tải video bạn sở hữu hoặc được chủ sở hữu cho phép.",
            "Trước khi tải, kiểm tra quyền riêng tư, bản quyền âm thanh/hình ảnh và mục đích sử dụng.",
            "Không dùng công cụ để lấy lại nội dung riêng tư, nội dung bị hạn chế hoặc vi phạm điều khoản nền tảng.",
        ]
    if "riêng" in module_l or "backup" in module_l or "sao lưu" in module_l:
        return [
            "Cuối ngày tải backup JSON về máy hoặc lưu vào kho cloud riêng của bạn.",
            "Không đưa service role key, SMTP password hoặc API key lên GitHub.",
            "Tạo 2 tài khoản test để chắc chắn dữ liệu tài khoản A không hiện ở tài khoản B.",
        ]
    return [
        "Chọn một việc nhỏ có thể làm trong 10 phút thay vì học quá nhiều cùng lúc.",
        "Làm xong thì lưu tiến độ/backup để dữ liệu không bị mất.",
        "Nếu có câu sai hoặc lỗi thao tác, đưa ngay vào danh sách ôn lại.",
    ]


def internal_ai_response(module: str, user_text: str, profile: Dict[str, Any], meds_count: int = 0) -> str:
    """Offline, no-cost response engine: templates + profile stats + light retrieval."""
    cache = _load_cache()
    key = _cache_key(module, user_text, profile, meds_count)
    if key in cache:
        return cache[key] + "\n\n_Đã dùng lại phản hồi từ cache nội bộ, không tốn API._"

    focus = _extract_focus(user_text + " " + module)
    counts = _profile_counts(profile, meds_count)
    plan = _plan_for_module(module, focus, counts)
    score = final_score(profile, meds_count)
    suggestions = offline_suggestions(profile, meds_count)

    response = f"""### Gợi ý thông minh nội bộ cho: {module}

**Trọng tâm:** {focus}  
**Final Score hiện tại:** {score}/100  
**Chế độ:** Offline-first, không gọi API ngoài.

#### Việc nên làm ngay
"""
    response += "\n".join([f"{i+1}. {item}" for i, item in enumerate(plan)])
    response += "\n\n#### Vì sao nên làm vậy\n"
    if counts["driving_wrong"] or counts["english_wrong"]:
        response += "Bạn đang có dữ liệu câu sai, nên ôn lỗi sai trước để tăng điểm nhanh hơn học dàn trải.\n"
    elif counts["driving_quiz"] + counts["english_quiz"] < 3:
        response += "App chưa có nhiều dữ liệu quiz, nên cần làm vài bài ngắn để hệ gợi ý nhận biết điểm yếu.\n"
    else:
        response += "Bạn đã có dữ liệu học cơ bản; bước tiếp theo là luyện bằng mô phỏng, nói/nghe hoặc checklist thực tế.\n"

    response += "\n#### Gợi ý tổng hợp hôm nay\n" + "\n".join([f"- {x}" for x in suggestions])
    response += "\n\n#### Lưu ý tiết kiệm API\nPhản hồi này được tạo bằng bộ gợi ý nội bộ + cache, không tốn Google/OpenAI/Gemini API. Nếu sau này cần câu trả lời sáng tạo hơn, bạn có thể bật chế độ Hybrid trong Secrets."

    cache[key] = response
    _save_cache(cache)
    return response


def api_usage_status() -> Dict[str, Any]:
    cache = _load_cache()
    return {
        "ai_mode": config.AI_MODE,
        "use_external_ai": config.USE_EXTERNAL_AI,
        "cache_enabled": config.AI_CACHE_ENABLED,
        "cache_items": len(cache),
        "max_external_calls_per_session": config.MAX_EXTERNAL_AI_CALLS_PER_SESSION,
        "google_key_configured": bool(config.GOOGLE_API_KEY),
    }


def clear_ai_cache() -> int:
    cache = _load_cache()
    count = len(cache)
    try:
        Path(config.AI_CACHE_PATH).unlink(missing_ok=True)
    except Exception:
        pass
    return count


def gemini_response(prompt: str) -> str:
    """External Gemini is disabled by default to avoid API cost."""
    if config.AI_MODE == "offline" or not config.USE_EXTERNAL_AI:
        return "Không gọi API ngoài: AI_MODE=offline hoặc USE_EXTERNAL_AI=false. Đang dùng AI nội bộ miễn phí."
    if not config.GOOGLE_API_KEY:
        return "Chưa cấu hình GOOGLE_API_KEY. Đang dùng AI nội bộ miễn phí."
    if config.MAX_EXTERNAL_AI_CALLS_PER_SESSION <= 0:
        return "Đã chặn gọi API ngoài vì MAX_EXTERNAL_AI_CALLS_PER_SESSION=0."
    try:
        from google import genai
        client = genai.Client(api_key=config.GOOGLE_API_KEY)
        res = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        return getattr(res, "text", "") or "Không có phản hồi."
    except Exception as exc:
        return f"Không gọi được Gemini: {exc}. Bạn vẫn có thể dùng AI nội bộ miễn phí."
