# Multi-Platform Posting — FB + IG + YT (VERIFIED 2026-08-11)

## Architecture
- **Agent Python Daemon**: `ziyan_affiliate_agent` at `C:\Users\arija\ziyan_agent\`
- **Telegram Bot**: @Ziyanclipperbot (polling, splits media per file)
- **Caption Generator**: 9Router `channel-researcher` (free) via HTTP POST
- **Queue**: Google Sheets (service account `ziyan-sheets-bot@ziyancorp.iam.gserviceaccount.com`)
- **Scheduler**: APScheduler BackgroundScheduler (cron 8 min check, stagger 77 min)
- **Platforms**: Facebook, Instagram, YouTube (multi-platform via tags)

## Instagram Business Integration
- **IG Business ID**: `17841479944713462` (@celineaurel99)
- **Linked to FB Page**: Celine Aurel (`975723622288353`)
- **Token**: Same FB Page token (long-lived 60 days)
- **Config**: `config.yaml` → `instagram.ig_user_id: "17841479944713462"`
- **Module**: `ig_upload.py` reads from config, skips auto-fetch

## Platform Tags (Telegram Caption)
| Tag | Platforms |
|-----|-----------|
| `#fb` | Facebook only |
| `#ig` | Instagram only |
| `#yt` | YouTube only |
| `#both` | Facebook + Instagram |
| `#ytfb` | YouTube + Facebook |

## Scheduler Logic
- Check PENDING jobs every 8 minutes
- Stagger: 77 minutes per job (queue_position * 77min)
- Platform callbacks:
```python
post_callbacks = {
    'facebook': fb_uploader.post_job,
    'instagram': ig_uploader.post_job,
    'youtube': yt_uploader.upload_video
}
```

## Graceful Fallback
- If IG Business not linked → `ig_uploader.get_ig_user_id()` returns `""`
- `ig_available = False` → agent runs FB only, logs warning
- No crash, no blocking

## Verification Commands
```bash
# Verify IG Business ID via Graph API
curl "https://graph.facebook.com/v19.0/17841479944713462?fields=id,username&access_token=TOKEN"

# Verify IG linked to Page
curl "https://graph.facebook.com/v19.0/me?fields=instagram_business_account&access_token=TOKEN"
```

## Pitfalls Fixed
1. **Multi-instance ConflictError**: `telegram.error.Conflict: terminated by other getUpdates request`
   - Fix: `taskkill /F /PID <all_python_pids>` before restart
2. **FB Page Token 400 Error**: Token 1 returns 400 on `/me`
   - Fix: Use token 2 from OneDrive for IG fetch
3. **Event Loop Conflict**: `AsyncIOScheduler` + `run_polling()` → use `BackgroundScheduler`
4. **Python 3.13 cryptography/cffi**: Pin `cryptography==42.0.5` + `cffi==1.17.1`