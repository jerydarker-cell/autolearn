# AutoLearn Public v15.8.2 Hotfix - English IndexError

Bản này sửa lỗi Streamlit Cloud:

```text
IndexError
modules/english.py line 161
with cols[i]
```

Nguyên nhân: English Master A1–B2 có 4 cấp độ A1/A2/B1/B2 nhưng layout chỉ tạo 3 cột bằng `st.columns(3)`, nên khi đến item thứ 4 bị vượt index.

Đã sửa:
- `with cols[i]` -> `with cols[i % len(cols)]`
- thêm hiển thị B2 trong Learning Focus
- thêm B2 vào bộ lọc Vocabulary / Conversation / Listening / Grammar
- giữ tên app: AutoLearn Public

Upload toàn bộ thư mục package lên GitHub, không upload riêng app.py.
