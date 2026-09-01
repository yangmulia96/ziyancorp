# Instagram Business Setup for ZIYAN Auto-Post

## Prerequisites
- Facebook Page: "Celine Aurel" (Page ID: 122119007576915460)
- Instagram account: @celineaurel99 (currently personal)

## Steps to Enable Auto-Post via FB Graph API

### 1. Convert Instagram to Professional/Business Account
1. Open Instagram app → Profile → Menu (☰) → Settings and privacy
2. Account type and tools → Switch to professional account
3. Choose "Business" (not Creator) → Select category (e.g., Digital Creator)
4. Complete setup (contact info optional)

### 2. Link Instagram to Facebook Page
1. Open Meta Business Suite (business.facebook.com)
2. Settings → Instagram accounts → Add Instagram account
3. Log in with @celineaurel99 credentials
4. Select Facebook Page: "Celine Aurel"
5. Confirm linking

### 3. Verify Connection via API
```bash
# Test with FB Page token
curl -G "https://graph.facebook.com/v19.0/me" \
  -d "access_token=<FB_PAGE_TOKEN>" \
  -d "fields=instagram_business_account"

# Expected response:
# {"instagram_business_account":{"id":"178414..."}}
```

### 4. Test IG Container Creation
```bash
# Create container (photo)
curl -X POST "https://graph.facebook.com/v19.0/<IG_USER_ID>/media" \
  -F "access_token=<FB_PAGE_TOKEN>" \
  -F "image_url=<PUBLIC_IMAGE_URL>" \
  -F "caption=Test post #test"

# Returns: {"id": "container_id"}
# Then publish:
curl -X POST "https://graph.facebook.com/v19.0/<IG_USER_ID>/media_publish" \
  -F "access_token=<FB_PAGE_TOKEN>" \
  -F "creation_id=<container_id>"
```

### 5. Video/Reels (requires polling)
```bash
# Create video container
curl -X POST "https://graph.facebook.com/v19.0/<IG_USER_ID>/media" \
  -F "access_token=<FB_PAGE_TOKEN>" \
  -F "media_type=REELS" \
  -F "video_url=<PUBLIC_VIDEO_URL>" \
  -F "caption=Test Reel #test"

# Poll status until FINISHED
curl -G "https://graph.facebook.com/v19.0/<container_id>" \
  -d "access_token=<FB_PAGE_TOKEN>" \
  -d "fields=status_code"

# Then publish when status_code=FINISHED
```

## Current Blockers (2026-08-10)
- @celineaurel99 is personal account, not Business
- Not linked to FB Page "Celine Aurel"
- `ig_uploader.get_ig_user_id()` returns `""` → agent runs FB only with warning

## Once Fixed
- Agent automatically detects `ig_available=True`
- Platform tag `#ig` or `#both` routes to Instagram
- Same FB Page token works for both FB and IG