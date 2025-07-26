# local-app/utils.py
import json
import os

def load_config(path="config.json"):
    """
    config.json을 읽어 dict로 반환.
    예시 파일(config.example.json)과 동일한 구조여야 합니다.
    {
      "artworkCode": "001",
      "serverUrl": "https://your-server.onrender.com"
    }
    """
    here = os.path.dirname(__file__)
    full_path = os.path.join(here, path)
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)
