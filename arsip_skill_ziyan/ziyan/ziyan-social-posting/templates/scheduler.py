"""
ZIYAN Intake Scheduler v2 - posting batch per 77 menit + arsip CSV + X.
Orion enqueue() tiap Bos kirim file/link. Tiap 77 menit: post FB (+YT kalau video) + X, lalu tulis arsip CSV.
"""
import os, json, time, subprocess
from datetime import datetime, timezone

BASE = r"C:\Users\arija\ziyan_intake"
QUEUE = os.path.join(BASE, "queue.json")
FB_TOK = open(r"C:\Users\arija\OneDrive\ziyan_pending\fb_page_token.txt").read().strip()
PAGE_ID = "975723622288353"
INTERVAL = 77 * 60

def _sheet_append(row):
    """Arsip lokal CSV (DB penanda upload)."""
    import csv
    arch = os.path.join(BASE, "arsip.csv")
    hdr = ["enqueued_at","file_path","deskripsi","link_aff","caption","fb_id","yt_id","x_id","posted_at"]
    if not os.path.exists(arch):
        with open(arch, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(hdr)
    with open(arch, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)

def enqueue(item: dict):
    q = json.load(open(QUEUE)) if os.path.exists(QUEUE) else []
    item.update({"enqueued_at": datetime.now(timezone.utc).isoformat(), "posted": False})
    q.append(item)
    json.dump(q, open(QUEUE, "w"), indent=2, ensure_ascii=False)
    print(f"QUEUED ({len(q)}): {item.get('deskripsi','')[:40]}")

def _post_fb(caption, file_path=None):
    if file_path and file_path.lower().endswith((".mp4", ".mov", ".webm")):
        cmd = ["curl", "-s", "-m", "60", "-X", "POST", f"https://graph.facebook.com/v19.0/{PAGE_ID}/videos",
               "-F", f"description={caption}", "-F", f"access_token={FB_TOK}", "-F", f"source=@{file_path};type=video/mp4"]
    else:
        cmd = ["curl", "-s", "-m", "20", "-X", "POST", f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed",
               "-F", f"message={caption}", "-F", f"access_token={FB_TOK}"]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=70).stdout.strip()

def _post_yt(caption, file_path):
    if not (file_path and file_path.lower().endswith((".mp4", ".mov", ".webm"))):
        return "SKIP"
    tok = json.load(open(r"C:\Users\arija\AppData\Local\hermes\ziyan_youtube_token.json"))["access_token"]
    meta = {"snippet": {"title": (caption.split(chr(10))[1][:60] if len(caption.split(chr(10)))>1 else "ZIYAN"),
                        "description": caption}, "status": {"privacyStatus": "public"}}
    tmp = os.path.join(BASE, "yt_meta.json"); json.dump(meta, open(tmp,"w"), ensure_ascii=False)
    cmd = ["curl","-s","-m","90","-X","POST","https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status&uploadType=multipart",
           "-H", f"Authorization: Bearer {tok}", "-F", f"metadata=<{tmp};type=application/json", "-F", f"file=@{file_path};type=video/mp4"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=100)
    try:
        r = json.loads(out.stdout); return r.get("id", "ERR:"+str(r.get('error',{}).get('message',''))[:50])
    except: return "ERR:"+out.stdout[:50]

def _post_x(caption, file_path=None):
    try:
        import sys; sys.path.insert(0, BASE)
        from post_tweet_helpers import post_tweet as px
        return px(caption, file_path)
    except Exception as e:
        return f"XERR:{str(e)[:50]}"

def run_once():
    q = json.load(open(QUEUE)) if os.path.exists(QUEUE) else []
    for it in q:
        if not it.get("posted"):
            cap = it.get("caption") or it.get("deskripsi", "")
            fb = _post_fb(cap, it.get("file_path"))
            yt = _post_yt(cap, it.get("file_path"))
            xt = _post_x(cap, it.get("file_path"))
            it.update({"posted": True, "fb_result": fb[:50], "yt_result": yt, "x_result": str(xt)[:50],
                       "posted_at": datetime.now(timezone.utc).isoformat()})
            json.dump(q, open(QUEUE, "w"), indent=2, ensure_ascii=False)
            _sheet_append([it.get("enqueued_at",""), it.get("file_path",""), it.get("deskripsi",""),
                           it.get("link_aff",""), cap, fb[:30], yt, str(xt)[:30], it.get("posted_at","")])
            print(f"POSTED FB={fb[:25]} YT={yt} X={xt}")
            return True
    return False

def loop():
    last = 0
    while True:
        q = json.load(open(QUEUE)) if os.path.exists(QUEUE) else []
        if [i for i in q if not i.get("posted")] and (time.time()-last >= INTERVAL):
            run_once(); last = time.time()
        time.sleep(60)

if __name__ == "__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="loop": loop()
    elif len(sys.argv)>1 and sys.argv[1]=="once": run_once()
