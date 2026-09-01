import json, urllib.request, urllib.parse, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\arija\ziyancorp\arsip_celine_aurel\.env")
TOK = os.environ.get("TELEGRAM_BOT_TOKEN")
def api(method, data=None):
    url = f"https://api.telegram.org/bot{TOK}/{method}"
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode() if data else None, method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

upd = api("getUpdates", {"limit": 5, "offset": -5})
for u in upd.get("result", []):
    msg = u.get("message", {})
    fwd = msg.get("forward_from_chat")
    ch = msg.get("chat", {})
    print("UPDATE_ID", u.get("update_id"))
    print("  chat:", ch.get("id"), ch.get("type"))
    if fwd:
        print("  FORWARD_FROM_CHAT ID:", fwd.get("id"), "title:", fwd.get("title"), "type:", fwd.get("type"))
    print("  text:", (msg.get("text") or "")[:50])
