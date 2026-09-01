# Affiliate FB / Threads Pipeline — Exact Commands (ZIYAN 2026-08)

## 1. FB User Token → Long-lived → Page Token
Generate User Token di https://developers.facebook.com/tools/explorer
(app "n8n", scope: pages_manage_posts, pages_read_engagement, pages_show_list). Lalu:

```bash
# extend ke 60 hari
curl -X GET "https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=1994676317847313&client_secret=APP_SECRET&fb_exchange_token=USER_TOKEN"

# list Page + dapatkan Page token
curl -X GET "https://graph.facebook.com/v19.0/me/accounts?access_token=USER_TOKEN"
```

## 2. Post carousel ke Page
```bash
# upload tiap gambar dulu
curl -X POST "https://graph.facebook.com/v19.0/{PAGE_ID}/photos" -F "url=URL_GAMBAR" -F "access_token=PAGE_TOKEN"
# atau feed dengan attached media
curl -X POST "https://graph.facebook.com/v19.0/{PAGE_ID}/feed" -F "message=CAPTION" -F "access_token=PAGE_TOKEN"
```

## 3. Threads limitation
Threads Graph API publish butuh app Live + review `business_use_case`. Tanpa itu: hanya read.
Jangan burn waktu review sekarang — FB Page dulu, Threads manual/semiotomatis.

## 4. 9router-image (lifestyle background)
```bash
curl -X POST "http://127.0.0.1:20128/v1/images/generations" \
  -H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"lifestyle background for electronics product, clean desk setup","n":1,"size":"1024x1024"}'
```

## 5. Firebase Admin (v2, ganti Sheets)
Butuh `firebase-admin` (pip) + Service Account JSON di `ziyan_credentials/firebase_admin.json`.
Firestore enable di console.cloud.google.com → project `ZiyanCorp`.
