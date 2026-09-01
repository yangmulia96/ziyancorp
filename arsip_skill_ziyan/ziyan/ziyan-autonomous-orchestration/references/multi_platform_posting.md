# Multi-Platform Posting Implementation (2026-08-10)

## Overview
Added Instagram support to the autonomous affiliate agent (FB + IG). TikTok skipped (no public API). Threads skipped (no publish API). X/Twitter skipped (needs X Developer Pro $100/mo).

## Architecture

### Sheets Queue (Google Sheets)
- **New column**: `platform` (position 5, after `affiliate_link`)
- Columns: `job_id`, `media_path`, `caption`, `affiliate_link`, **`platform`**, `status`, `schedule_time`, `created_at`, `posted_at`, `error_message`, `retry_count`
- Values: `facebook` (default), `instagram`, `both`
- Caption tags: `#ig` → instagram, `#fb` → facebook, `#both`/`#all` → both

### Instagram Uploader (`modules/ig_upload.py`)
- Uses **same FB Page token** via FB Graph API
- Requires: Instagram Business Account linked to FB Page "Celine Aurel"
- Endpoints:
  - `GET /me?fields=instagram_business_account` → get `ig_user_id`
  - `POST /{ig_user_id}/media` (create container: `source` file + `caption`)
  - `POST /{ig_user_id}/media_publish` (publish: `creation_id`)
- Video/Reels: `media_type=REELS` + polling `status_code` until `FINISHED`
- Returns `ig_user_id` or `""` if not linked

### Scheduler (`modules/scheduler.py`)
- `post_callbacks` dict: `{'facebook': fb_uploader.post_job, 'instagram': ig_uploader.post_job}`
- Logic for `platform`:
  - `facebook` → call FB callback
  - `instagram` → call IG callback
  - `both` → call BOTH, success only if both succeed

### Agent Entry (`agent.py`)
- Try to get `ig_user_id` at startup
- If fails (no IG Business linked) → `ig_available=False` → graceful fallback to FB only
- Log warning, continue running

## Graceful Fallback
```python
# In agent.py
ig_user_id = loop.run_until_complete(ig_uploader.get_ig_user_id())
if ig_user_id:
    ig_available = True
else:
    ig_available = False
    logger.warning("Instagram not available (no IG Business Account linked to FB Page)")
```

## Pitfalls Fixed
1. **Multi-instance Conflict**: `telegram.error.Conflict: terminated by other getUpdates request` → kill all old processes before starting new
2. **Event Loop**: `BackgroundScheduler` + synchronous `telegram_bot.run()` works on Windows
3. **Venv**: Pin `cryptography==42.0.5` `cffi==1.17.1` with `--force-reinstall --no-deps`

## Test Commands
```bash
# Check IG Business linked
curl -s "https://graph.facebook.com/v19.0/me?fields=instagram_business_account&access_token=$FB_TOKEN"

# Check queue in Sheets
# Open Google Sheet → tab "Queue" → check platform column
```

## Status (2026-08-10)
- ✅ Facebook Page: Celine Aurel (working)
- ❌ Instagram: @celineaurel99 (personal, not Business linked) → agent runs FB only
- ✅ YouTube: @celineaurel-q4h (token ready)
- ❌ Threads: @celineaurel99 (no publish API)
- ❌ X/Twitter: @celineaurel99 (needs Pro tier)