# Streamlit Cloud Test Checklist - AutoLearn v15.8.1

## Upload / Repo
- [ ] app.py ở root repo
- [ ] modules/ ở root repo
- [ ] data/ ở root repo
- [ ] requirements.txt ở root repo
- [ ] .streamlit/config.toml ở root repo
- [ ] Không bị lồng thư mục kiểu autolearn_pkg/app.py

## Build
- [ ] Streamlit build thành công
- [ ] Không còn ModuleNotFoundError
- [ ] Dashboard mở được trong 10–20 giây đầu

## Auth / Data
- [ ] Đăng ký tài khoản A
- [ ] Đăng nhập lại tài khoản A
- [ ] Tạo tài khoản B
- [ ] B không thấy dữ liệu của A

## Bộ 600 câu
- [ ] App Health Check báo 600/600 câu
- [ ] 6 chương đúng số lượng
- [ ] Làm quiz 5 câu thành công
- [ ] Tìm kiếm theo ID câu thành công
- [ ] Nếu có danh sách điểm liệt: đánh dấu đủ 60 câu

## Mobile
- [ ] Mở trên điện thoại
- [ ] Bật Performance Mode > Light
- [ ] Quiz 5–10 câu/lượt không bị giật

## Optional heavy features
- [ ] Google Veo chỉ test khi có API key
- [ ] TikTok chỉ test khi cần và link hợp lệ
- [ ] Dashboard vẫn chạy nếu chưa dùng 2 mục này

## Backup
- [ ] Tải backup JSON được
- [ ] Reboot app xong vẫn đăng nhập và dùng được
