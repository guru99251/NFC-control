# local-app/exit_mode.py
import requests
from utils import load_config
from cache import load_failed_logs, clear_failed_logs

def exit_mode():
    CONFIG = load_config("config.json")
    server = CONFIG["serverUrl"]
    print("Exit mode: 태깅 내역 확인 및 누락 보정")
    uid = input("카드를 태그한 후, UID를 입력하세요: ").strip()
    # 서버에서 기록된 방문 내역 불러오기
    try:
        r = requests.get(f"{server}/api/history/{uid}", timeout=5)
        r.raise_for_status()
        history = r.json().get("history", [])
    except Exception as e:
        print(f"[ERR] 서버 조회 실패: {e}")
        # 로컬 캐시 확인
        history = [e["artwork"] for e in load_failed_logs() if e["uid"] == uid]
    print(f"기록된 작품: {', '.join(history) if history else '없음'}")

    # 누락된 작품 보정
    to_add = input("추가로 태깅할 작품 코드(콤마 구분) 입력 (없으면 엔터): ").strip()
    if to_add:
        codes = [c.strip() for c in to_add.split(",")]
        for artwork in codes:
            payload = {"uid": uid, "artwork": artwork}
            try:
                requests.post(f"{server}/api/log", json=payload, timeout=5)
                print(f"[OK] Added {artwork}")
            except Exception as e:
                print(f"[ERR] Failed to add {artwork}: {e}")
        # 보정 후 캐시 초기화
        clear_failed_logs()

if __name__ == "__main__":
    exit_mode()
