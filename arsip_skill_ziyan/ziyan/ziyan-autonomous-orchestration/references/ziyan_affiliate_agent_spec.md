# ZIYAN Affiliate Agent Specification (Python Daemon)

**Built**: 2026-08-10 | **Location**: `C:\Users\arija\ziyan_agent\` | **Replaces**: n8n workflow "ZIYAN Affiliate Auto-Post"

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Telegram Bot    │────▶│ Agent Orchestrator│────▶│ Google Sheets   │
│ (polling)       │     │ (queue + logic)   │     │ (queue + log)   │
└─────────────────┘     └────────┬─────────┘     └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
             ┌──────────┐ ┌──────────┐ ┌──────────┐
             │ 9Router  │ │ Scheduler│ │ FB API   │
             │ Caption  │ │ 77 min   │ │ Upload   │
             └──────────┘ └──────────┘ └──────────┘
```

## Modules

| File | Purpose |
|------|---------|
| `agent.py` | Main entry point, initializes all components |
| `config.yaml` | All tokens, sheet ID, FB token path, 9Router URL |
| `modules/telegram_bot.py` | Polling @Ziyanclipperbot, handle photo/video + caption |
| `modules/caption.py` | POST to 9Router `channel-researcher` for caption |
| `modules/sheets.py` | gspread + service account, append/get/update jobs |
| `modules/scheduler.py` | APScheduler BackgroundScheduler: cron 8 min, stagger 77 min |
| `modules/fb_upload.py` | Graph API v19.0 upload photo/video to Page |

## Flow

### Input (Telegram → Sheets)
1. Bos kirim **photo/video + caption dengan link affiliate** ke @Ziyanclipperbot
2. Bot download media → `media/{job_id}_{timestamp}.{ext}`
3. Caption Generator (9Router) → generate caption Indonesia max 1024 char + hashtag
4. Append ke Google Sheets: `job_id, media_path, caption, affiliate_link, status=PENDING, schedule_time, created_at`
5. Stagger: `schedule_time = now + 77min * (pending_count + 1)`

### Publish (Cron → FB)
6. Scheduler tiap **8 menit** cek Sheet: `status=PENDING` AND `schedule_time <= now`
7. Untuk tiap job: upload ke FB Page via Graph API (`/me/photos` atau `/me/videos`)
8. Update Sheet: `status=POSTED`, `posted_at=now` (atau `FAILED` + error)

## Config (config.yaml)

```yaml
telegram:
  bot_token: "8984029406:AAHDxG9NZbag9xIVuDKKrG16SQZtLpZaR8c"
  bot_username: "@Ziyanclipperbot"

google_sheets:
  spreadsheet_id: "1lsyqnE51_eT2JFf0nuLNuT4AjOo4-VvXLMvEdr8hSSs"
  credentials_path: "credentials/service_account.json"
  worksheet_name: "Queue"

facebook:
  page_access_token: ""  # loaded from token_file_path
  token_file_path: "C:/Users/arija/OneDrive/ziyan_pending/fb_page_token.txt"

ninerouter:
  base_url: "http://127.0.0.1:20128/v1"
  model: "channel-researcher"
  caption_max_chars: 1024
  caption_language: "indonesian"
  caption_include_hashtags: true

scheduler:
  check_interval_minutes: 8
  stagger_minutes_per_job: 77
  timezone: "Asia/Jakarta"

agent:
  media_dir: "media"
  log_file: "logs/agent.log"
  log_level: "INFO"
```

## Requirements

```
python-telegram-bot>=21.0,<22.0
gspread>=6.0.0
google-auth>=2.25.0
google-auth-oauthlib>=1.1.0
requests>=2.31.0
httpx>=0.25.0
apscheduler>=3.10.0
pyyaml>=6.0
python-dotenv>=1.0.0
tqdm>=4.66.0
aiofiles>=23.0.0
aiohttp>=3.9.0
```

## Launcher

`run_agent.bat`:
- Creates venv if missing
- Installs deps from requirements.txt
- Creates `media/`, `logs/`, `credentials/` dirs
- Warns if service_account.json missing
- Runs `python agent.py`

## Setup Required (Bos)

1. **Google Service Account**:
   - Console Cloud → IAM → Service Accounts → Create
   - Enable: Google Sheets API + Google Drive API
   - Create Key → JSON → save as `credentials/service_account.json`
   - Share Sheet (ID: `1lsyqnE51_eT2JFf0nuLNuT4AjOo4-VvXLMvEdr8hSSs`) with service account email (Editor)

2. **FB Page Token**: Already at `OneDrive/ziyan_pending/fb_page_token.txt`

3. **9Router**: Must be running (`start-9router.bat` in Startup)

## TikTok Auto-Post

**TIDAK ADA** di agent ini. TikTok tidak punya public API untuk auto-post:
- Official Content Posting API → butuh verified business + review
- Unofficial `tiktok-uploader` → browser automation, rawan ban
- Third-party (Zapier/Make) → manual buffer

Fokus: FB Page (ready), IG/X/YT (butuh token setup terpisah).

## Critical Fixes (Windows + Python 3.13 MS Store)

### Venv + cryptography/cffi Issue
MS Store Python 3.13 (`python3.13.exe`) has broken `_cffi_backend` in fresh venvs.

**Fix:** Pin cryptography and cffi with binary wheels:
```bash
.venv/Scripts/python.exe -m pip install "cryptography==42.0.5" "cffi==1.17.1" --force-reinstall --no-deps
```

### Event Loop Conflict (python-telegram-bot v21+)
`AsyncIOScheduler` + `Application.run_polling()` conflict on Windows.

**Fix:** Use `BackgroundScheduler` (thread-based) + synchronous `telegram_bot.run()` which calls `application.run_polling()` internally managing its own event loop.

### 9Router SSE Parser (Already in caption.py)
9router returns SSE, not single JSON. Parser handles `data: {json}\n\n` chunks with `delta.content`.

## Credentials Available (Audit 2026-08-10)

| Platform | Account | Token Status |
|----------|---------|--------------|
| Facebook | Celine Aurel (Page ID: 975723622288353) | ✅ Valid (OneDrive/ziyan_pending/fb_page_token.txt) |
| YouTube | Compound Daily (@@compounddaily-v7c) | ✅ Valid (refresh via desktop client) |
| YouTube | Ziyan Malik (@@ziyanmalik28) | ✅ Valid (refresh via desktop client) |
| Blogger | Blog ID: 598320500315317650 | ✅ Token exists (_blogger_auth_url.txt) |
| Instagram | - | ❌ Not configured (use FB Graph API /me/media) |
| Threads | - | ❌ No public API |
| Twitter/X | - | ❌ Token discarded (Bos request) |
| LinkedIn | - | ❌ Not configured |
| TikTok | - | ❌ No public API for auto-post |

## Verification

```bash
# Check agent running
tail -f logs/agent.log

# Check queue
# Buka Google Sheet → tab "Queue"

# Test 9Router
curl http://127.0.0.1:20128/v1/models
```