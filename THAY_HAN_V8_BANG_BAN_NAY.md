# Thay hẳn AutoLearn v8 bằng v15.1 Fixed Final

Bạn không cần backup v8 nếu muốn thay hẳn.

## Cách làm trên GitHub/Streamlit Cloud

1. Giải nén ZIP này.
2. Vào GitHub repo đang chạy bản v8.
3. Xóa toàn bộ file cũ trong repo.
4. Upload toàn bộ nội dung thư mục này lên repo.
5. Đảm bảo repo có:

```
app.py
modules/
scripts/
sql/
.streamlit/config.toml
requirements.txt
packages.txt
.github/workflows/medicine-reminders.yml
```

6. Vào Supabase → SQL Editor → chạy file:

```
sql/supabase_schema.sql
```

7. Vào Streamlit Cloud → Manage app → Settings → Secrets.
8. Copy nội dung file:

```
STREAMLIT_SECRETS_COPY_PASTE.toml
```

9. Điền các dòng CHANGEME bằng thông tin thật.
10. Save Secrets → Reboot app.

## Nếu chỉ muốn chạy local ngay

Có thể chạy SQLite local, không cần Supabase:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Hoặc copy `STREAMLIT_SECRETS_LOCAL_SQLITE.toml` thành `.streamlit/secrets.toml`.

## Lưu ý

- Không đưa key thật lên GitHub.
- Không gửi Service Role Key cho người khác.
- Muốn dữ liệu bền trên Streamlit Cloud thì dùng Supabase, không dùng SQLite.
