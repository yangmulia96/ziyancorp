# X/Twitter OAuth Setup untuk Posting (ZIYAN)

## Fakta kritis (tested 2026-08-07)
- App-only Bearer token **TIDAK BISA** POST tweet → 403 `Unsupported Authentication`.
- X Free Tier **bisa post** asal pakai **OAuth 1.0a User Context**.
- App Bos: `shopeeaffiliateee`, akun `@AgenticsID` (id `2079132337502359552`).
- **Consumer Key BENAR = `vVXNsMZEZ2k2EhyiHRA3a8YQt`** (di `ziyan_x_consumer.env`).
  - ⚠️ `GXkFwJzQvMj1Iem2g8d3wguH` = SALAH (app beda, 401 Unauthorized).
- Access Token `2079132337502359552-5RyHsdhfTOtCwZMqKj1pKVfHs9TgnO` + Secret `IxFS7LXBHjluCmFmKWy1m5xXE04QYMST32UBM8Z1hTRwG` (OAuth 1.0a, dari X Dev Console → "Access Token and Secret").
- **BEARER di `ziyan_x.env` TIDAK DIPAKAI** (app-only, 403).

## Cara post yang JALAN (Python, SUDAH TESTED — tweet id `2085701683632644177`)
```python
from requests_oauthlib import OAuth1Session
CK="vVXNsMZEZ2k2EhyiHRA3a8YQt"
CS="eSnEj7NYndhzL3F0piBxY26Yktoz76vbCShEYiRYAyZGn1VTb3"
AT="2079132337502359552-5RyHsdhfTOtCwZMqKj1pKVfHs9TgnO"
ATS="IxFS7LXBHjluCmFmKWy1m5xXE04QYMST32UBM8Z1hTRwG"
o=OAuth1Session(CK, client_secret=CS, resource_owner_key=AT, resource_owner_secret=ATS)
r=o.post('https://api.twitter.com/2/tweets', json={'text':'caption link'})
# 201 = sukses, 401 = consumer key salah
```

## n8n node (SUDAH AKTIF di workflow)
- Node `X: Post Tweet` (type `executeCommand`) panggil `python3 -c "..."` dengan env `X_CK/X_CS/X_AT/X_ATS`.
- Env diset di n8n `settings` key=`env` (JSON), restart n8n agar load.
- **PITFALL**: `executeCommand` di n8n v2.33 BELUM terverifikasi jalan di dalam n8n (hanya pola Python di atas yang tested langsung). Kalau gagal di n8n, ganti Code node (Python) atau HTTP Request + signing manual HMAC-SHA1.
- Free tier = 17 tweet/24 jam (akun baru).

## Etika
Jangan auto-post X tanpa izin Bos. Aktifkan hanya kalau Bos suruh.
