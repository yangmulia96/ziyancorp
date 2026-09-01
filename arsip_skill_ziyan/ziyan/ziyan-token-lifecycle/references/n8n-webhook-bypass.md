# n8n webhook broken → Python scheduler fallback

Symptom: n8n v2.33, workflow inserted manually into `.n8n/database.sqlite` → webhook returns "Cannot POST /webhook" (not registered).

Fix: don't fight n8n webhook; run a Python scheduler that does the same job.

Structure (`C:\Users\arija\ziyan_intake\scheduler.py`):
- `queue.json` — array of pending items `{file_path, deskripsi, link_aff, platform, caption, posted:false}`
- `enqueue(item)` — append to queue.json
- `run_once()` — pop first unposted: post FB (curl graph video/feed) + YT (curl multipart if video) + X (OAuth1a) → write arsip row → mark posted
- `loop()` — sleep 60s; if pending AND (now-last >= INTERVAL) → run_once; INTERVAL=77*60 (batch rule)

Post helpers:
- FB: `curl -X POST graph.facebook.com/v19.0/{PAGE_ID}/feed -F message= -F access_token=`  (text) OR `/videos -F source=@file` (video)
- YT: multipart upload (see youtube skill / token-lifecycle body §3)
- X: OAuth1a (see x-oauth1a.md)
- Arsip: Sheets curl append (see google-sheets-curl.md) OR local CSV fallback

Run: `uv run python3 ziyan_intake/scheduler.py loop` (background).

Rule embedded: Bos wants batch posting spaced 77 minutes, X/Twitter included, YT Shorts public.
