#!/usr/bin/env python3
# compound_pipeline_harvest.py — idempoten: parse _gen.log -> download mp4 -> upload YouTube Compound Daily.
# Jalankan DI DALAM proses background yang sama setelah `notebooklm generate video` selesai
# (bukan di run cron terpisah), supaya download+upload berurutan dalam satu proses yang bertahan.
# Idempoten: aman dijalankan berulang; tidak akan upload ganda (flag uploaded).
import json, os, re, sys, subprocess, urllib.request
from datetime import datetime, timezone

VP    = os.environ.get("VIDEO_DIR", r"C:\Users\arija\workdir\videos\2026-08-07")
STATE = os.path.join(VP, "pipeline_state.json")
GENLOG= os.path.join(VP, "_gen.log")
LOG   = r"C:\Users\arija\logs\pipeline.log"
PY    = r"C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
ZUP   = r"C:\Users\arija\ziyan_upload.py"
CWD   = r"C:\Users\arija"

def log(m):
    with open(LOG, "a") as f:
        f.write(f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} {m}\n")

st = json.load(open(STATE))
status = st.get("status", "idle")

# 1) Cari URL download di log generasi
if status in ("generating", "ready"):
    url = None
    if os.path.exists(GENLOG):
        txt = open(GENLOG, encoding="utf-8", errors="ignore").read()
        m = re.search(r'https?://[^\s"\'\u2019]+\.mp4[^\s"\'\u2019]*', txt)
        if m:
            url = m.group(0)
    if url:
        st["video_url"] = url
        st["status"] = "ready"
        json.dump(st, open(STATE, "w"), indent=2)
        log(f"HARVEST url ditemukan: {url[:90]}")
    else:
        log("HARVEST belum ada url (masih generate / gagal)")
        sys.exit(0)

# 2) Download mp4
if st.get("status") == "ready" and st.get("video_url") and not st.get("local_mp4"):
    local = os.path.join(VP, "video.mp4")
    try:
        urllib.request.urlretrieve(st["video_url"], local)
        st["local_mp4"] = local
        st["status"] = "downloaded"
        json.dump(st, open(STATE, "w"), indent=2)
        log(f"HARVEST download OK {local} ({os.path.getsize(local)} bytes)")
    except Exception as e:
        log(f"HARVEST download GAGAL: {e}")
        sys.exit(1)

# 3) Upload ke YouTube Compound Daily
if st.get("status") == "downloaded" and st.get("local_mp4") and not st.get("uploaded"):
    title = "AI Is Splitting the Chip Market in Two - Nvidia, SOXX & Tower Semi Explained"
    desc  = ("AI infrastructure spend is reshaping semiconductors. Nvidia's AI stock bets (one up 170% YTD), "
             "the SOXX ETF down 21% in July, Tower Semi surging on earnings, rotation from TSM to equipment makers. "
             "Sources: The Motley Fool, Yahoo Finance, AOL. #AIstocks #semiconductors #investing")
    tags  = "AI stocks,semiconductor,Nvidia,SOXX,Tower Semiconductor,investing,Compound Daily"
    r = subprocess.run([PY, ZUP, "--file", st["local_mp4"], "--title", title,
                        "--description", desc, "--tags", tags, "--category", "28", "--privacy", "public"],
                       capture_output=True, text=True, cwd=CWD)
    out = (r.stdout or "") + (r.stderr or "")
    log(f"HARVEST upload rc={r.returncode} out={out[:240]}")
    m = re.search(r'UPLOAD_OK\|([\w-]+)\|(https?://\S+)', out)
    if m:
        st["youtube_id"] = m.group(1)
        st["youtube_url"] = m.group(2)
        st["uploaded"] = True
        st["status"] = "uploaded"
        json.dump(st, open(STATE, "w"), indent=2)
        log(f"HARVEST upload SUKSES {m.group(2)}")
    else:
        log("HARVEST upload parse gagal (lihat out di atas)")

if st.get("status") == "uploaded":
    log("HARVEST sudah uploaded; tidak ada aksi")
