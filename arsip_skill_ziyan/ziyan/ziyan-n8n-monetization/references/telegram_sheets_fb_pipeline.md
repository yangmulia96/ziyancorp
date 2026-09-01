# Telegram → Sheets → FB Page Pipeline (ZIYAN Shopee Affiliate)

## Arsitektur (2026-08-07, rencana aktif)
```
Telegram (@CelineaureBot)
  ├─ Bos kirim: link Shopee + foto/video produk
  ├─ Hermes tanya: harga, diskon, kategori (kalau kurang)
  ├─ Simpan 1 row ke Google Sheet
  └─ n8n Schedule tiap 87 menit:
       ambil row posted=false
       ├─ FOTO → composite PIL (foto asli + BG flux-1-schnell) → FB /photos multipart
       └─ VIDEO → upload FB /videos multipart (feed video)
       mark posted=true
```

## File & ID (jangan hardcode ulang, pakai ini)
- Bot token: `ziyan_telegram.env` (TELEGRAM_BOT_TOKEN)
- Google token: `ziyan_google_token.json`
- Sheet ID: `1wLqdaYcjdaxXD1nEXPIv9PHObFhQPCi80cSiUHqEG8w` (ZIYAN Shopee Affiliate)
  - Kolom: A=link_affiliate B=url_foto_asli C=kategori D=harga E=diskon F=caption G=posted
- Form ID: `1G1TDq7VzFqMN50tAOJw5dY5J36wRha3yCRzlp4aeto0` (BELUM tersambung ke Sheet via API)
- FB Page: `975723622288353` (Celine Aurel), token di `ziyan_fb_credentials.env` (FB_PAGE_TOKEN)
- n8n workflow DB id: `8a30e6f0-bb49-404f-98db-ff6b309fcd65` (file `ziyan_workflow_v2.json`)

## Setup Telegram Gateway (tested)
1. Token di `.env` Hermes: baris `TELEGRAM_BOT_TOKEN=<literal>` (uncomment `#` + isi).
   JANGAN biarkan `#` → gateway baca kosong.
2. `hermes gateway restart` → log harus "✓ telegram connected".
3. Bos kirim 1 pesan ke @CelineaureBot supaya gateway tahu chat_id.

## FB Video Upload (belum di workflow, rencana)
- `POST graph.facebook.com/v19.0/{PAGE_ID}/videos`
- multipart: `source=@file.mp4`, `description=<caption>`, `access_token=<PAGE_TOKEN>`
- Beda dari foto (`/photos`). Video = feed video, bukan carousel.

## X / Threads status
- X: butuh API key berbayar ($100/bulan Basic). Bos belum punya → node placeholder mati.
- Threads: subcode 33, butuh Meta app review → skip auto-post.

## Pitfall
- Form `responseDestination` TIDAK didukung di Forms API batchUpdate versi ini → Bos sambung manual UI (Responses → ikon spreadsheet → pilih existing Sheet).
- Jangan janjikan X/Threads sebelum key/review ada.
- Interval 87 menit: n8n Schedule "every X minutes" = 87 (valid, bukan cron).
