# Multi-Platform Posting Status & Setup (FB, IG, Threads, Twitter/X, YouTube)

## Platform Readiness Matrix (as of 2026-08-10)

| Platform | Auto-Post Ready? | Credentials | Blocker / Next Step |
|----------|------------------|-------------|---------------------|
| **Facebook Page** | ✅ **YES** | Page token (`EAAcWJcVdZCxEBSBoRo6dQzPng...`) in config.yaml + OneDrive | Working in agent |
| **Instagram** | ⚠️ **Partial** | Same FB token (if IG Business linked) | **Need: Convert @celineaurel99 to Business + link to FB Page "Celine Aurel" in Meta Business Suite** |
| **Threads** | ❌ **NO** | App ID: `1346767533487099`, Secret: `70a9d2be92c369` | Meta belum rilis publish API (hanya read) |
| **Twitter/X** | 💰 **Paid only** | Client ID, Secret, Access Token, Secret (OAuth 2.0) | Free tier = read-only. Write needs **X Developer Pro ($100/bln)** |
| **YouTube** | ✅ **Ready** | `youtube_token_celineaurel.json` (OAuth) | Need implementation in agent |

## Instagram Business Setup (Free, One-time)

1. Go to **Meta Business Suite** → Settings → Instagram Accounts
2. Click "Add Instagram Account" → log in as `@celineaurel99`
3. Convert to **Business Account** (choose category, connect to FB Page "Celine Aurel")
4. Verify: `GET https://graph.facebook.com/v19.0/me?fields=instagram_business_account&access_token=<FB_PAGE_TOKEN>`
5. Should return `{"instagram_business_account": {"id": "IG_USER_ID"}}`
6. Agent will auto-detect on startup (`ig_uploader.get_ig_user_id()`)

## Twitter/X Reality Check

| Tier | Cost | Write Access | Notes |
|------|------|--------------|-------|
| Free | $0 | ❌ | Read-only (GET tweets, users) |
| Basic | $100/bln | ✅ Limited | Post tweets, but rate limited |
| Pro | $5,000/bln | ✅ Full | Enterprise |

**No free write API** since Musk acquisition. Unofficial (`twikit`, `tweetipy`) = browser automation, rawan ban.

## YouTube Upload Implementation

Token ready: `youtube_token_celineaurel.json` (channel: Celine Aurel @celineaurel-q4h)

Endpoint: `POST https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status&uploadType=resumable`

Scopes needed (already in token):
- `youtube.upload`
- `youtube.readonly`
- `youtube.force-ssl`

## Threads API Status

- App credentials exist in Meta Developer Portal
- **No publish API** available (only read: get profile, posts)
- Meta roadmap: "coming soon" since 2023

## Agent Caption Routing

In Telegram caption to @Ziyanclipperbot:
- `#fb` → Facebook only (default)
- `#ig` → Instagram only
- `#both` / `#all` → Both FB + IG

Sheets queue `platform` column handles routing. Scheduler calls appropriate callback.