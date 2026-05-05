# AutoLearn v15 Setup Ready

Gói này đã chuẩn bị sẵn để bạn chỉ cần điền thông tin.

## Cách dễ nhất

### Windows
Bấm:

```text
run_setup_wizard.bat
```

### MacBook
Bấm:

```text
Run_Setup_Wizard_Mac.command
```

Nếu macOS chặn file `.command`, mở Terminal trong thư mục này và chạy:

```bash
chmod +x *.command
xattr -dr com.apple.quarantine .
./Run_Setup_Wizard_Mac.command
```

## Setup Wizard làm gì?

Nó tạo sẵn:

- Streamlit Secrets TOML
- GitHub Actions secrets ENV
- GitHub CLI commands

Bạn chỉ copy/paste vào đúng nơi.

## File quan trọng

- `sql/supabase_schema.sql`: chạy trong Supabase SQL Editor.
- `setup_wizard.py`: form điền thông tin.
- `setup_templates/STREAMLIT_SECRETS_TEMPLATE.toml`: mẫu Streamlit Secrets.
- `setup_templates/GITHUB_ACTIONS_SECRETS_TEMPLATE.env`: mẫu GitHub Actions Secrets.
- `README_DEPLOY_STREAMLIT.md`: hướng dẫn deploy.

## Bảo mật

Không commit file chứa key thật. Không gửi key trong chat.
