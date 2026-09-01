# ZIYAN Affiliate Agent Daemon (Python) — Spec & Implementation Notes

## Overview
Replaces n8n workflow. Autonomous daemon running 24/7 at `C:\Users\arija\ziyan_agent\`.

**Flow:** Input file+link → @Ziyanclipperbot → download/split → 9Router caption → Google Sheets queue → cron 8min → FB/IG post → mark POSTED. Zero human in loop.

## Architecture
```
agent.py                  # Main entry (BackgroundScheduler + sync telegram.run())
├── modules/
│   ├── telegram_bot.py   # Polling @Ziyanclipperbot, download media, queue to Sheets
│   ├── sheets.py         # gspread + service account, queue in Google Sheets
│   ├── caption.py        # 9Router channel-researcher (SSE parser)
│   ├── scheduler.py      # APScheduler BackgroundScheduler: cron 8min, stagger 77min
│   ├── fb_upload.py      # FB Graph API v19.0 /me/photos + /me/videos
│   └── ig_upload.py      # IG via FB Graph API (same token), /ig_user_id/media
├── config.yaml           # All tokens, sheet ID, FB token path
├── credentials/
│   └── service_account.json  # Google SA (Sheets + Drive API)
└── run_agent.bat         # Launcher (venv + deps + run)
```

## Key Technical Fixes (Windows + Python 3.13 MS Store)

### 1. Venv + cryptography/cffi
Fresh venv broken `_cffi_backend`. MS Store Python venv lacks system binaries.
```bash
.venv/Scripts/pip.exe install "cryptography==42.0.5" "cffi==1.17.1" --force-reinstall --no-deps
# Then install requirements.txt
```

### 2. Event Loop Conflict (python-telegram-bot v21+)
`AsyncIOScheduler` + `Application.run_polling()` → "event loop already running".
**Fix:** Use `BackgroundScheduler` (thread-based) + synchronous `telegram_bot.run()` calling `application.run_polling()` internally.

```python
# agent.py
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(fb_uploader.get_page_id())
loop.run_until_complete(ig_uploader.get_ig_user_id())

# Telegram bot manages its own event loop via run_polling()
telegram_bot.run()  # blocking
```

### 3. Multi-Instance Conflict
`telegram.error.Conflict: terminated by other getUpdates request` = old instance still running.
**Fix:** Kill all old processes before starting new:
```bash
# List and kill
process(action='list')  # find proc_* for ziyan_agent
process(action='kill', session_id='proc_xxx')
```

### 4. 9Router SSE Parser
Returns SSE chunks `data: {json}\n\n`, not single JSON. Handled in `caption.py`.

## Multi-Platform Posting (FB + IG)

### Instagram Requirements
- **Must have** Instagram Business Account linked to FB Page "Celine Aurel"
- Uses **same FB Page token** via FB Graph API
- Endpoint: `POST /ig_user_id/media` (create container) → `POST /ig_user_id/media_publish` (publish)
- Video/Reels: poll `status_code` until `FINISHED` before publish

### Caption Routing (Telegram)
- `#ig` = Instagram only
- `#fb` = Facebook only  
- `#both` / `#all` = both platforms

### Sheets Queue Schema
Added `platform` column (col 5):
```
job_id | media_path | caption | affiliate_link | **platform** | status | schedule_time | created_at | posted_at | error_message | retry_count
```

### Scheduler Callbacks
```python
post_callbacks = {
    'facebook': fb_uploader.post_job,
    'instagram': ig_uploader.post_job  # only if ig_available
}
scheduler = PostScheduler(config, sheets_queue, post_callbacks=post_callbacks)
```

### Graceful Fallback
```python
ig_user_id = await ig_uploader.get_ig_user_id()
if ig_user_id:
    ig_available = True
else:
    ig_available = False  # log warning, run FB only
```

## Configuration
All tokens in `config.yaml` (no hardcoded secrets):
- Telegram bot token
- Google Sheets ID + SA path
- FB Page token (or file path to OneDrive)
- 9Router base_url + model (channel-researcher)
- Scheduler: check_interval_minutes=8, stagger_minutes_per_job=77

## Deployment
- Background process: `nohup .venv/Scripts/python.exe agent.py > logs/agent.log 2>&1 &`
- Logs: `logs/agent.log`
- Media downloads: `media/`
- 9Router auto-start required (separate process)

## Test Checklist
- [ ] Send photo/video + caption with affiliate link to @Ziyanclipperbot
- [ ] Verify job appears in Google Sheets (PENDING)
- [ ] Wait for scheduler (8 min) → check FB Page post
- [ ] Verify status → POSTED in Sheets
- [ ] Check stagger: 2nd job posts ~77 min after 1st