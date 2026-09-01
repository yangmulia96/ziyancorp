# ZIYAN Social Auth — Resep Riil (8 Agt 2026)

## FB Page Token 60 Hari
1. Bos kasih USER token pendek (atau ambil dari Explorer).
2. Ambil PAGE token:
   `GET https://graph.facebook.com/v19.0/me/accounts?fields=id,name,access_token&access_token=USER_TOK`
   → copy `access_token` dari page "Celine Aurel" (id 975723622288353).
3. Exchange ke 60 hari (butuh FB_APP_ID + FB_APP_SECRET):
   `GET https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APPID&client_secret=APPSEC&fb_exchange_token=PAGE_TOK`
   → token hasil disimpan ke `OneDrive/ziyan_pending/fb_page_token.txt`.
4. Verifikasi + test post lalu DELETE:
   `POST https://graph.facebook.com/v19.0/975723622288353/feed -F message=... -F access_token=...`
   `DELETE https://graph.facebook.com/v19.0/<post_id>?access_token=...`
- Catatan: USER token pendek expired ~1 jam. PAGE token dari exchange = 60 hari (debug_token gak tampil expires_at = normal long-lived).

## X / Twitter OAuth1a (FREE posting)
- BEARER (App-only) → 403 Forbidden untuk v2 write (free tier read-only).
- Pakai OAuth1a User Context:
  ```python
  from requests_oauthlib import OAuth1Session
  o = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_KEY_SECRET,
                    resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESS_TOKEN_SECRET)
  r = o.post("https://api.twitter.com/2/tweets", json={"text": "..."})  # 201 = sukses
  # media: upload dulu ke https://upload.twitter.com/1.1/media/upload.json (files={'media':f})
  ```
- Credential di `~/.x_credentials` (format: BEARER_TOKEN=, CONSUMER_KEY=, CONSUMER_KEY_SECRET=, ACCESS_TOKEN=, ACCESS_TOKEN_SECRET=, CLIENT_SECRET=, TWITTER_USERNAME=). File `.bak` biasanya berisi token asli; `.x_credentials` template kosong.

## YouTube Token Refresh
- File: `AppData/Local/hermes/ziyan_youtube_token.json` (access_token, refresh_token, client_id, client_secret).
- Kalau access_token expired (401):
  ```python
  import urllib.parse, urllib.request, json
  d=json.load(open(path))
  data=urllib.parse.urlencode({"client_id":d['client_id'],"client_secret":d['client_secret'],"refresh_token":d['refresh_token'],"grant_type":"refresh_token"}).encode()
  r=json.loads(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token",data=data,method="POST"),timeout=15).read())
  d['access_token']=r['access_token']; json.dump(d,open(path,'w'))
  ```
- Upload Shorts (private/public): multipart ke `https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status&uploadType=multipart` dengan `-F metadata=<file.json;type=application/json -F file=@video.mp4`. Pakai file temp metadata (jangan inline `-F` dengan JSON panjang — error "Invalid JSON payload").

## Keamanan
- JANGAN print token ke chat. Simpan ke file, baca lewat script.
- FB: `OneDrive/ziyan_pending/fb_page_token.txt`. X: `~/.x_credentials`. YT: `AppData/Local/hermes/ziyan_youtube_token.json`.
