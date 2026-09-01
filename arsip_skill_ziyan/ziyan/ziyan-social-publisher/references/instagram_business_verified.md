# Instagram Business Account — VERIFIED CONNECTED (2026-08-11)

## Status: ✅ CONNECTED & WORKING
- **Instagram Business Account ID**: `17841479944713462`
- **Username**: `@celineaurel99`
- **Linked to FB Page**: `Celine Aurel` (`975723622288353`)
- **Verified via Graph API**: `GET /me?fields=instagram_business_account` → returns IG ID ✅

## How It Was Connected
1. Instagram @celineaurel99 already Professional Account (Business)
2. Added to Business Portfolio "Agent AI" via Meta Business Suite
3. Connection request sent to Facebook Page "Celine Aurel" (portfolio "Celine Aurel")
4. **Approved via Page Settings**: `facebook.com/CelineAurel` → Settings → Instagram → Confirm
5. After approve: IG Business Account linked to Page

## Integration in ziyan_affiliate_agent
- Config `config.yaml` → `instagram.ig_user_id: "17841479944713462"`
- Module `ig_upload.py` → reads `ig_user_id` from config, skips auto-fetch
- Uses **same FB Page token** (long-lived 60 days) for IG API calls
- Graceful fallback: if `ig_user_id` empty → log warning, run FB only

## Tested Endpoints
- `GET /17841479944713462?fields=id,username` → 200 OK
- `POST /17841479944713462/media` (photo/video) → container created
- `POST /17841479944713462/media_publish` → published

## Multi-Platform Tags (Telegram Bot)
- `#fb` → Facebook only
- `#ig` → Instagram only
- `#yt` → YouTube only
- `#both` → Facebook + Instagram
- `#ytfb` → YouTube + Facebook

## Scheduler (ziyan_affiliate_agent)
- Check PENDING every 8 minutes
- Stagger 77 minutes per job
- Platform callbacks: `{'facebook': fb, 'instagram': ig, 'youtube': yt}`

## Pitfall
- FB Page token 1 (config) returns 400 on `/me` — use token 2 (OneDrive) for IG fetch
- Multi-instance ConflictError: kill old python processes before restart