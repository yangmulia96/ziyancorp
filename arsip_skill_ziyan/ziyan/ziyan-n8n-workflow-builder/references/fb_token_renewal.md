# FB Page Token Renewal (ZIYAN)

## Fakta (terbukti 2026-08-07)
- FB token di `AppData/Local/hermes/ziyan_fb_credentials.env` (`FB_PAGE_TOKEN`) dan
  `ziyan_fb_usertoken.env` (`FB_USER_TOKEN`) **sudah ada tapi EXPIRED**.
- FB Graph balas: `Error validating access token: Session has expired` (code 190).
- File Bos tidak punya `FB_APP_ID` / `FB_APP_SECRET` → tidak bisa auto-tukar ke long-lived.

## Cek validitas (sebelum test posting FB)
```bash
curl -s -m 8 "https://graph.facebook.com/v19.0/<PAGE_ID>?fields=name&access_token=$FB_PAGE_TOKEN"
# {"error":{"code":190}} = EXPIRED  |  {"name":"...","id":"..."} = VALID
```
Page ID ZIYAN intake: `975723622288353`

## Jalur A (Bos generate)
1. https://developers.facebook.com/tools/explorer → Pilih App → Generate Access Token
2. Scope: `pages_show_list, pages_read_engagement, pages_manage_posts, publish_video`
3. Open in Access Token Tool → tekan "Extend" (60 hari)
4. Ambil Page Token dari `me/accounts?fields=access_token` → simpan `OneDrive/ziyan_pending/fb_page_token.txt`

## Jalur B (agent tukar, butuh secret)
Bos kasih ke `OneDrive/ziyan_pending/` (atau kirim langsung ke chat DM — Bos nyaman kirim token ke DM privat, agent simpan TANPA print ulang):
- `fb_app_id.txt`, `fb_app_secret.txt`, `fb_short_token.txt`
```bash
curl -s "https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=<APP_ID>&client_secret=<SECRET>&fb_exchange_token=<SHORT_TOKEN>"
# -> {"access_token":"<LONG>","expires_in":5184000}
```
Colok ke `C:\Users\arija\.env` (`FB_PAGE_TOKEN=...`) + restart n8n.
