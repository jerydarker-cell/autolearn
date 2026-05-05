# AI nội bộ không tốn API

Bản v15.2 thêm chế độ **Offline-first AI**:

- Không gọi Google/OpenAI/Gemini mặc định.
- Trả lời bằng dữ liệu hồ sơ + bộ luật nội bộ + template + cache.
- Có trang `🧠 API nội bộ tiết kiệm` để test phản hồi.
- Có thể bật API ngoài sau này bằng Secrets nếu thật sự cần.

## Secrets khuyến nghị

```toml
AI_MODE = "offline"
USE_EXTERNAL_AI = "false"
AI_CACHE_ENABLED = "true"
MAX_EXTERNAL_AI_CALLS_PER_SESSION = "0"
GOOGLE_API_KEY = ""
```

## Khi nào tốn API?

Chỉ tốn nếu bạn tự bật:

```toml
AI_MODE = "hybrid"
USE_EXTERNAL_AI = "true"
MAX_EXTERNAL_AI_CALLS_PER_SESSION = "5"
GOOGLE_API_KEY = "..."
```

Google Veo vẫn cần API/key nếu bạn dùng chức năng tạo video. Còn AI gợi ý học tập/chăm sóc có thể chạy miễn phí nội bộ.
