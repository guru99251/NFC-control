import nfc, requests, json
from utils import load_config

config = load_config('config.json')

def on_connect(tag):
    uid = tag.identifier.hex().upper()
    payload = {"uid": uid, "artwork": config["artworkCode"]}
    requests.post(config["serverUrl"] + '/api/log', json=payload)
    return True

if __name__ == '__main__':
    clf = nfc.ContactlessFrontend('usb')
    while True:
        clf.connect(rdwr={'on-connect': on_connect})
