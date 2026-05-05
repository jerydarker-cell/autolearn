import smtplib
from email.mime.text import MIMEText
from typing import Tuple

import requests

from . import config


def send_email(to_email: str, subject: str, body: str) -> Tuple[bool, str]:
    if not (config.SMTP_HOST and config.SMTP_USER and config.SMTP_PASSWORD and to_email):
        return False, "SMTP chưa cấu hình hoặc thiếu email nhận."
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = config.SMTP_FROM
        msg["To"] = to_email
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=25) as s:
            s.starttls()
            s.login(config.SMTP_USER, config.SMTP_PASSWORD)
            s.sendmail(config.SMTP_FROM, [to_email], msg.as_string())
        return True, "Email sent"
    except Exception as exc:
        return False, str(exc)


def send_telegram(chat_id: str, text: str) -> Tuple[bool, str]:
    if not (config.TELEGRAM_BOT_TOKEN and chat_id):
        return False, "Telegram chưa cấu hình hoặc thiếu chat_id."
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=25)
        r.raise_for_status()
        return True, "Telegram sent"
    except Exception as exc:
        return False, str(exc)
