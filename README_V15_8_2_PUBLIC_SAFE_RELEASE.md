# AutoLearn Public

Bản nhỏ tập trung làm app an toàn hơn khi chia sẻ public:

- Terms & Privacy rõ hơn.
- Admin Mini Dashboard.
- Public Safe Center.
- Công cụ đánh dấu 60 câu điểm liệt nếu có danh sách ID chuẩn.
- Kiểm tra sâu bộ 600 câu.
- Tối ưu mobile thêm.
- Deploy Hotfix Guide để sửa lỗi thực tế sau deploy.
- Tiếp tục giữ lazy-load Google Veo/TikTok để không làm chậm app chính.

## Cách deploy
Upload toàn bộ package lên GitHub, không upload riêng app.py.

Cần có:
app.py
modules/
data/
static/
scripts/
sql/
.streamlit/
requirements.txt
packages.txt

Sau deploy, vào:
1. App Health Check
2. Public Safe Center
3. Terms & Privacy
4. Admin Mini Dashboard
