"""External medicine reminder worker.
Run by GitHub Actions, cron, Render worker, VPS, or local scheduler.
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules import config
from modules.db import get_db
from modules.notifications import send_email, send_telegram

WEEKDAYS = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]


def today_name():
    return WEEKDAYS[datetime.now().date().weekday()]


def main() -> int:
    db = get_db()
    now = datetime.now()
    lookahead = timedelta(minutes=config.REMINDER_LOOKAHEAD_MIN)
    sent_count = 0
    meds = db.list_all_active_medications()
    for med in meds:
        days = med.get("days") or ["Tất cả"]
        if "Tất cả" not in days and today_name() not in days:
            continue
        user = db.get_user_by_id(med["user_id"])
        if not user:
            continue
        profile = db.load_profile(user["id"])
        notif = profile.get("notification", {})
        for t in med.get("times", []):
            try:
                due = datetime.strptime(now.date().isoformat() + " " + t, "%Y-%m-%d %H:%M")
            except Exception:
                continue
            if not (now <= due <= now + lookahead):
                continue
            key = due.strftime("%Y-%m-%d %H:%M")
            subject = f"Đến giờ uống thuốc: {med['name']}"
            body = f"Nhắc thuốc cho mẹ:\n\n{key}\nThuốc: {med['name']}\nLiều: {med['dose']}\nCách dùng: {med.get('instructions','')}\n\nVui lòng xác nhận trong app sau khi uống."
            if notif.get("email_enabled", True) and not db.reminder_was_sent(user["id"], med["id"], key, "email"):
                ok, msg = send_email(user["email"], subject, body)
                print("email", user["email"], med["name"], ok, msg)
                if ok:
                    db.mark_reminder_sent(user["id"], med["id"], key, "email"); sent_count += 1
            chat_id = notif.get("telegram_chat_id")
            if chat_id and not db.reminder_was_sent(user["id"], med["id"], key, "telegram"):
                ok, msg = send_telegram(chat_id, body)
                print("telegram", chat_id, med["name"], ok, msg)
                if ok:
                    db.mark_reminder_sent(user["id"], med["id"], key, "telegram"); sent_count += 1
    print(f"Done. Sent {sent_count} reminders.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
