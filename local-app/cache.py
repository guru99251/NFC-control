# local-app/cache.py
import json
import os
from datetime import datetime

CACHE_FILE = "failed_logs.json"

def save_failed_log(entry):
    """
    전송 실패 시, entry(dict)를 로컬 JSON 파일에 append.
    """
    logs = []
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    logs.append(entry)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def load_failed_logs():
    """
    이전에 실패했던 로그 리스트 반환.
    """
    if not os.path.exists(CACHE_FILE):
        return []
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def clear_failed_logs():
    """
    캐시 파일 초기화.
    """
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)

def retry_failed_logs(server_url):
    """
    저장된 로그를 재전송하고, 성공하면 캐시 삭제.
    """
    import requests
    logs = load_failed_logs()
    success = []
    for entry in logs:
        try:
            r = requests.post(f"{server_url}/api/log", json=entry, timeout=5)
            if r.status_code == 200:
                success.append(entry)
        except Exception:
            continue
    if success:
        clear_failed_logs()
    return success
