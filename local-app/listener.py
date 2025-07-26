# local-app/listener.py
import time
import nfc
import requests
from utils import load_config
from cache import save_failed_log, retry_failed_logs

def on_connect(tag):
    uid = tag.identifier.hex().upper()
    payload = {
        "uid": uid,
        "artwork": CONFIG["artworkCode"],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    try:
        r = requests.post(f"{CONFIG['serverUrl']}/api/log", json=payload, timeout=5)
        r.raise_for_status()
        # 재전송 캐시가 있다면 시도
        retry_failed_logs(CONFIG["serverUrl"])
        print(f"[OK] Sent tag: {payload}")
    except Exception as e:
        print(f"[ERR] Failed to send, caching: {e}")
        save_failed_log(payload)
    return True  # 다시 대기

if __name__ == "__main__":
    CONFIG = load_config("config.json")
    clf = nfc.ContactlessFrontend()
    print("Listening for NFC tags. Press Ctrl+C to exit.")
    try:
        while True:
            clf.connect(rdwr={'on-connect': on_connect})
    except KeyboardInterrupt:
        print("Exiting listener.")
