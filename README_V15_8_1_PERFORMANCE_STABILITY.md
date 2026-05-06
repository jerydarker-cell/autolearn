# AutoLearn v15.8.1 Performance & Stability Pack

Bản này không nhồi thêm app mới, mà làm cho bản v15.8 chạy mượt và ổn định hơn.

## Nâng cấp chính

1. Kiểm tra chuẩn bộ 600 câu
   - Kiểm tra tổng 600 câu.
   - Kiểm tra ID 1–600.
   - Kiểm tra đáp án.
   - Kiểm tra số lượng 6 chương: 180, 25, 58, 37, 185, 115.
   - Cảnh báo nếu chưa đánh dấu đủ 60 câu điểm liệt.

2. Tối ưu load dữ liệu
   - Dữ liệu 600 câu dùng cache.
   - Google Veo/TikTok chỉ import khi mở đúng trang.
   - Thêm Performance Mode để chọn light/balanced/full.

3. Chế độ nhẹ/mobile
   - Giảm animation.
   - Nút dễ bấm hơn trên điện thoại.
   - Tab/card gọn hơn.
   - Khuyến nghị quiz 5–10 câu/lượt.

4. Health Check
   - Kiểm tra file repo.
   - Kiểm tra imports.
   - Kiểm tra bộ 600 câu.
   - Kiểm tra database/profile.
   - Checklist test Cloud.

5. Error message thân thiện
   - Lỗi thiếu data/modules được giải thích rõ hơn.
   - Google Veo/TikTok không làm hỏng dashboard nếu thiếu thư viện/API.

## Cách deploy
Upload toàn bộ thư mục lên GitHub, không upload riêng app.py.

Repo cần có:
- app.py
- modules/
- data/
- scripts/
- sql/
- .streamlit/
- requirements.txt
- packages.txt

Sau khi deploy, vào app > App Health Check để kiểm tra.
