import json, os, sys
from pathlib import Path
from pywebpush import webpush, WebPushException

VAPID_PRIVATE_KEY = os.getenv('VAPID_PRIVATE_KEY', '')
VAPID_SUBJECT = os.getenv('VAPID_SUBJECT', 'mailto:admin@example.com')
if not VAPID_PRIVATE_KEY:
    raise SystemExit('Thiếu VAPID_PRIVATE_KEY trong environment/secrets.')
sub_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('push_subscription.json')
subscription = json.loads(sub_file.read_text(encoding='utf-8'))
payload = json.dumps({'title':'AutoLearn', 'body':'Đến giờ học / uống thuốc / ôn bài.', 'url':'/'}, ensure_ascii=False)
try:
    webpush(subscription_info=subscription, data=payload, vapid_private_key=VAPID_PRIVATE_KEY, vapid_claims={'sub': VAPID_SUBJECT})
    print('Đã gửi push.')
except WebPushException as exc:
    print('Gửi push lỗi:', repr(exc))
    if exc.response is not None:
        print(exc.response.text)
