# AutoLearn v15.8 Official 600 Integrated

Bản này đã tích hợp PDF `600 câu hỏi dùng cho sát hạch lái xe cơ giới đường bộ - Cục CSGT - 2025` do bạn upload.

## Có gì mới
- Có sẵn `data/official_600_questions_2025.pdf`.
- Có sẵn `data/official_600_questions_2025_extracted.json` gồm 600 câu.
- Có sẵn `data/official_600_questions_2025_extracted.csv` để kiểm tra/chỉnh sửa.
- Tab `🪪 Bộ 600 câu chính thức` tự dùng bộ câu hỏi này, không cần import CSV nữa.
- Quiz chính thức có lọc theo hạng bằng, chương, tìm kiếm theo ID/từ khóa.

## Lưu ý
PDF gốc nói có 60 câu tình huống mất an toàn nghiêm trọng. Nếu file PDF không có ký hiệu riêng trong text cho từng câu điểm liệt, app chưa tự đánh dấu chính xác được 60 câu đó. Bạn có thể cập nhật cột `is_critical` trong CSV rồi import lại.

## Deploy
Upload nguyên toàn bộ thư mục lên GitHub, không upload riêng `app.py`.
