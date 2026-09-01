# Fashion Asset Ingestion — Mass Content dari Zip

## Skenario (2026-08-07)
Bos kirim `download.zip` (149MB) → berisi 176 file jpeg fashion (street style, OOTD, mirror selfie, hijab, pria/wanita). Tujuannya: jadi konten schedule FB Page + X via workflow n8n.

## Langkah
1. **Extract**: `python3 -c "import zipfile; zipfile.ZipFile('download.zip').extractall('fashion_assets')"` → 150 jpeg di `C:/Users/arija/Downloads/fashion_assets/`
2. **Filter watermark**: cek `if 'bellzxshop' not in f.lower()` (1 foto punya watermark brand, sisanya bersih berdasar vision sampling).
3. **Isi Sheet** (Google Sheets API, token di `ziyan_google_token.json`):
   - Kolom: `link_affiliate, url_foto_asli, kategori, harga, diskon, caption, posted`
   - `url_foto_asli` = `C:/Users/arija/Downloads/fashion_assets/<file>.jpeg` (path lokal absolut Windows)
   - `kategori` = `fashion`, `posted` = `FALSE`, `link_affiliate` = `` (outfit utuh → caption inspirasi OOTD)
   - Batch 50 row per request (`values/Sheet1!A2:G51` dst)
4. **Refresh token kalau 401**: `curl -s -X POST https://oauth2.googleapis.com/token -d "client_id=$CID&client_secret=$CS&refresh_token=$RT&grant_type=refresh_token"` → simpan `access_token` baru ke `ziyan_google_token.json` (pertahankan `refresh_token`).

## Pitfalls
- **Path Windows vs posix**: script Python jalankan dari `C:/Users/arija/Downloads/fashion_assets` tapi baca file pakai path absolut `C:/Users/arija/...` (bash MSYS kadang ubah `/c/` → gagal).
- **base64 di bash GAGAL** untuk file >~100KB: `curl: Argument list too long`. Kirim image ke vision/API lewat `requests` di Python, bukan `curl` CLI dengan `-d @b64`.
- **Tesseract tidak ada** di laptop → pakai `vision_analyze` sampling (5 foto cukup) untuk deteksi watermark, jangan brute-force 150x.
- **Google token expired 1 jam** → selalu refresh sebelum operasi Sheets/Form besar.

## Workflow n8n
- Schedule 87 menit → Sheets Read (`posted!=TRUE`) → Parse → AI Caption → 9router BG (flux-1-schnell) → PIL composite → FB Post Photo + FB Upload Video (paralel) → X Post Tweet → mark `posted=true`.
- Fashion foto (outfit utuh) → composite dengan AI bg → jadi konten Feed (bukan affiliate langsung).
