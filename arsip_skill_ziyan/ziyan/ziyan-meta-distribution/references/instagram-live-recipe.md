# Instagram LIVE Recipe (verified 16/8/2026)

## Token source (NOT Facebook Graph)
- Generated at Meta Console -> App "n8n" -> Instagram product -> "User Token Generator" -> pick @celineaurel99.
- Format: `IGAAcb...` (long, ~190 chars).
- Validate: `GET https://graph.instagram.com/v20.0/me?fields=id,username&access_token=TOK` -> `{"id":"...","username":"celineaurel99"}`.
- Store: vault `instagram_user_token`; `.env` `INSTAGRAM_USER_TOKEN`.

## Endpoint (CRITICAL)
- Use `graph.instagram.com` for ALL IG calls.
- Using `graph.facebook.com` with IG token -> `code 190 "Cannot parse access token"`.

## Image hosting (CRITICAL)
IG cannot fetch Google Drive URLs (they return HTML -> code 36001 "image format not supported").
WORKING FIX: upload the real photo to the FB Page, read its CDN URL, use that for IG.

```python
import requests
fb_tok = vault("fb_page_token")          # or os.environ FB_PAGE_TOKEN
ig_tok = vault("instagram_user_token")   # or os.environ INSTAGRAM_USER_TOKEN
ig_id  = "17841444876830769"
page_id = "975723622288353"

# 1. upload asli (sudah didownload dari Drive) ke FB Page
r = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/photos",
                  files={"source": open(photo_local, "rb")},
                  data={"published": "false", "access_token": fb_tok}, timeout=30)
cdn = requests.get(f"https://graph.facebook.com/v20.0/{r.json()['id']}",
                   params={"fields": "source", "access_token": fb_tok}, timeout=15).json()["source"]

# 2. IG container + publish
c = requests.post(f"https://graph.instagram.com/v20.0/{ig_id}/media",
                  data={"image_url": cdn, "caption": caption, "access_token": ig_tok}, timeout=30).json()["id"]
p = requests.post(f"https://graph.instagram.com/v20.0/{ig_id}/media_publish",
                  data={"creation_id": c, "access_token": ig_tok}, timeout=30).json()
# p["id"] = published media id  ->  SUCCESS
```

## Error map
| Error | Cause | Fix |
|-------|-------|-----|
| 190 "Cannot parse access token" | IG token used on graph.facebook.com | Switch to graph.instagram.com |
| 36001 "image format not supported" | image_url is Drive HTML page | Use FB-Page-CDN URL |
| 9004 "Only photo or video can be accepted" | image_url missing/invalid | Provide real image URL |
| "Insufficient Developer Role" | IG account not admin/tester of app | Add @celineaurel99 as Admin in App roles, accept invite in IG app |
