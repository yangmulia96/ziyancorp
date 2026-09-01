import requests
import json
import sys
from datetime import datetime

# UTF-8 encoding support
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TOPIC = "ziyancorp_narasikilat_feedback_vault_2026"
URL = f"https://ntfy.sh/{TOPIC}/json?poll=1"

def fetch_feedbacks():
    try:
        res = requests.get(URL, timeout=8)
        if res.status_code != 200:
            print(f"[-] Gagal mengambil feedback (Status {res.status_code})")
            return []
        
        feedbacks = []
        lines = res.text.strip().split('\n')
        for line in lines:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if 'message' in data:
                    try:
                        parsed = json.loads(data['message'])
                        feedbacks.append(parsed)
                    except:
                        feedbacks.append({
                            'name': 'Anonim',
                            'rating': 5,
                            'category': '💬 Masukan',
                            'message': data['message'],
                            'timestamp': datetime.fromtimestamp(data.get('time', 0)).strftime('%Y-%m-%d %H:%M:%S')
                        })
            except Exception:
                continue
        return feedbacks
    except Exception as e:
        print(f"[-] Error fetching: {e}")
        return []

if __name__ == "__main__":
    items = fetch_feedbacks()
    print(f"\n=======================================================")
    print(f"📋 TOTAL MASUKAN KOMUNITAS DI CLOUD VAULT: {len(items)}")
    print(f"=======================================================\n")
    if not items:
        print("Belum ada masukan baru yang masuk.")
    for idx, f in enumerate(items, 1):
        try:
            r = int(f.get('rating', 5))
        except:
            r = 5
        stars = '⭐' * r
        print(f"[{idx}] {f.get('timestamp', '-')} | {f.get('name', 'Anonim')} | {f.get('category', '-')}")
        print(f"    Rating : {stars} ({r}/5)")
        print(f"    Pesan  : \"{f.get('message', '')}\"")
        print(f"    ---------------------------------------------------")
