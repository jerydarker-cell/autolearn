from typing import Dict, Any, List

from . import config


def offline_suggestions(profile: Dict[str, Any], meds_count: int = 0) -> List[str]:
    driving = profile.get("driving", {})
    english = profile.get("english", {})
    suggestions = []
    if len(driving.get("wrong_bank", {})):
        suggestions.append(f"Ôn {len(driving.get('wrong_bank', {}))} câu lái xe đang sai trước khi học bài mới.")
    else:
        suggestions.append("Làm 5 câu Quiz lái xe để tạo dữ liệu điểm yếu cho AI gợi ý.")
    if len(english.get("learned_words", [])) < 10:
        suggestions.append("Học 5 từ tiếng Anh mới, nghe phát âm và đặt 1 câu với mỗi từ.")
    else:
        suggestions.append("Luyện Speaking Coach 7 phút để biến từ vựng thành phản xạ nói.")
    if meds_count:
        suggestions.append("Kiểm tra lịch thuốc hôm nay, xác nhận từng liều ngay sau khi uống và xem cảnh báo thuốc sắp hết.")
    else:
        suggestions.append("Thêm thuốc đầu tiên cho mẹ để bật hệ thống nhắc thuốc ngoài app.")
    suggestions.append("Cuối ngày vào Backup để tải bản sao JSON về máy hoặc lưu trên cloud riêng.")
    return suggestions


def final_score(profile: Dict[str, Any], meds_count: int = 0) -> int:
    driving = profile.get("driving", {})
    english = profile.get("english", {})
    score = 20
    score += min(25, len(driving.get("completed", [])) * 4)
    score += min(20, len(driving.get("quiz_history", [])) * 3)
    score += min(20, len(english.get("learned_words", [])) * 2)
    score += min(10, meds_count * 3)
    score += 5 if profile.get("notification", {}).get("email_enabled") else 0
    return max(0, min(100, score))


def gemini_response(prompt: str) -> str:
    key = config.GOOGLE_API_KEY
    if not key:
        return "Chưa cấu hình GOOGLE_API_KEY. AI đang dùng gợi ý offline."
    try:
        from google import genai
        client = genai.Client(api_key=key)
        res = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        return getattr(res, "text", "") or "Không có phản hồi."
    except Exception as exc:
        return f"Không gọi được Gemini: {exc}"
