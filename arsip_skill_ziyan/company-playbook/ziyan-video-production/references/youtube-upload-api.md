# Upload YouTube Compound Daily — Resep API (terverifikasi)

## Fakta kunci (2026-08-01)
- Token valid ADA: `ziyan_credentials/youtube_token_compound.json`
  - isi: `access_token`, `refresh_token`, `scope` = `youtube.upload ...`, `token_type`.
  - channel terikat: **Compound Daily** (`UCzWib2-2CPkWo315fzucaUw`, @compounddaily-v7c).
- Client untuk refresh: `ziyan_credentials/youtube_desktop_client.json` (installed app).
- Path `./credentials/youtube_oauth.json` di instruksi cron **TIDAK ADA** — jangan cari.

## Alur (skrip: scripts/youtube_upload_api.py)
1. `refresh()` — POST `oauth2.googleapis.com/token` grant_type=refresh_token pakai client installed → simpan access_token baru ke token file.
2. `verify()` — GET `youtube/v3/channels?mine=true` → harus 200 & balikin Compound Daily. (Gagal = token revoked / API mati.)
3. `upload()` — POST `youtube/v3/videos?uploadType=multipart&part=snippet,status,contentDetails`
   - Header: `Authorization: Bearer <access_token>`, `Content-Type: multipart/related; boundary=...`.
   - Body: metadata JSON (snippet: title, description, tags, categoryId, defaultLanguage) + file video binary.
   - `status.privacyStatus`: "public" (channel Compound Daily memang publikasi).

## Metadata standar
- `categoryId`: "28" (Science & Technology) untuk topik Tech/AI/Finance.
- `defaultLanguage` / `defaultAudioLanguage`: "en" (audiens internasional).
- `tags`: 6–8 kata kunci (semiconductor, chip stocks, AI, finance, dst).
- Judul <= 100 char; deskripsi sertakan sumber (Yahoo Finance via Google News) + disclaimer.

## Verifikasi sukses (jangan klaim sebelum ini)
- HTTP 200 + field `id` ada.
- `channelId` di response == `UCzWib2-2CPkWo315fzucaUw`.
- `status.privacyStatus` sesuai.
- Cek ulang via `channels?mine=true` atau buka `https://youtu.be/<id>`.

## Pitfall
- edge-tts host (`speech.platform.bing.com`) sering terblokir di host → `render_short.py` fallback `pyttsx3` (lokal). Video tetap punya narasi.
- Jangan fabrikasi upload. Bila refresh 400/403 → token revoked → minta Bos login ulang (lihat `credentials/README_SETUP_OAUTH.md`).
- Dedup: catat `content_id` ke `logs/uploaded.jsonl` sebelum/saat upload.
- Upload publik bersifat irreversibel → pastikan QC (judul, metadata, tidak ada klaim palsu) lewat dulu.
