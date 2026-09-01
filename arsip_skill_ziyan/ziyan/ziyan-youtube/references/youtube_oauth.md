# YouTube OAuth — Pitfall & Flow ZIYAN

## ERROR YANG TERJADI (1 Aug 2026)
```
Access blocked: This app's request is invalid
Error 400: redirect_uri_mismatch
```
Penyebab: `google_client_secret.json` lama bertipe **WEB** → `urn:ietf:wg:oauth:2.0:oob` DITOLAK ("Invalid Redirect: must contain a domain").

## SOLUSI (terbukti jalan)
1. GCP Console → Credentials → **Create OAuth client ID** → Application type = **Desktop app**
2. Download JSON → `ziyan_credentials/youtube_desktop_client.json` (project `lofty-layout-504106-n4`)
3. Desktop client auto punya `redirect_uris: ['http://localhost']` → VALID
4. Generate auth URL dengan redirect `http://localhost`
5. Bos buka URL → login `mziyan266@gmail.com` → Allow → Google redirect ke `http://localhost?code=XXXX` (error browser normal) → copy `code=` dari address bar
6. Agent tukar code → refresh_token via `https://oauth2.googleapis.com/token` (POST: client_id, client_secret, code, redirect_uri=http://localhost, grant_type=authorization_code)
7. Simpan refresh_token ke `ziyan_credentials/youtube_refresh_token.txt` (lokal, TIDAK chat)

## CATATAN
- `access_type=offline` di auth URL → dapat refresh_token (berlaku lama)
- Jangan pernah print token/code ke chat. Bos hanya tempel `code=` (bukan token)
- File client lama (web) tetap di `ziyan_credentials/google_client_secret.json` — TIDAK dipakai untuk upload
