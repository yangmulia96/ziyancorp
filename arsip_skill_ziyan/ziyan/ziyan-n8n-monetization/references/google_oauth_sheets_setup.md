# Google OAuth Setup untuk n8n Sheets/Form (ZIYAN) — TERBUKTI 2026-08-07

## Client secret type
- PAKAI `installed` (Desktop app) type, BUKAN `web`.
- Web type punya `redirect_uris: []` -> `redirect_uri_mismatch` (Error 400).
- File yang jalan: `C:\Users\arija\client_secret_3131524149-2ek5m9fg8o60p78bl8b1a546m7aj5o19.apps.googleusercontent.com.json`
  (type `installed`, `redirect_uris:["http://localhost"]`).

## Alur yang JALAN (terbukti)
1. OAuth client ID = **Desktop app** di https://console.cloud.google.com/apis/credentials
2. Consent screen -> User type **External** -> tambah **Test user** `mziyan266@gmail.com`
   (kalau mode Testing, else 403 `access_denied: has not completed verification`)
3. Enable API: **Google Sheets API** + **Google Forms API** (`forms.googleapis.com`)
   (kalau Forms tidak di-enable -> 403 `SERVICE_DISABLED`)
4. Auth URL **PLAIN, tanpa PKCE**:
   `https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=<CID>&redirect_uri=http://localhost&scope=https://www.googleapis.com/auth/spreadsheets+https://www.googleapis.com/auth/forms+https://www.googleapis.com/auth/drive&access_type=offline&prompt=consent`
5. Bos login -> browser redirect `http://localhost/?code=XXXX` (error biasa, itu wajar) -> **copy URL penuh**
6. Tukar token **MANUAL curl, tanpa PKCE** (setup.py pakai PKCE tapi tukar gagal `invalid_grant`):
   ```bash
   curl -s -X POST "https://oauth2.googleapis.com/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "code=<CODE>&client_id=<CID>&client_secret=<CSEC>&redirect_uri=http://localhost&grant_type=authorization_code"
   ```
   -> simpan `access_token` + `refresh_token` ke `ziyan_google_token.json`.

## PITFALL (jangan diulang)
- `google-workspace` skill `setup.py --auth-url` generate URL **dengan PKCE** (`code_challenge`) + redirect `localhost:1`.
  Tukar pakai `--auth-code` GAGAL (`code_verifier or verifier is not needed` / `invalid_grant`).
  -> Gunakan plain URL + manual curl di atas.
- Kode OAuth **cepat expired (~1 menit)**. Generate URL -> Bos login -> tukar dalam hitungan detik.
- `localhost:1` tidak dikenali kalau client secret `redirect_uris=["http://localhost"]` -> pakai `http://localhost` PERSIS.
- Jangan pakai client secret `web` type (redirect kosong) -> selalu `redirect_uri_mismatch`.

## Bikin Sheet + Form (terbukti)
- Sheet: `POST https://sheets.googleapis.com/v4/spreadsheets?access_token=<TOK>` body `{"properties":{"title":"ZIYAN Shopee Affiliate"}}`
- Header: `PUT .../values/Sheet1!A1:G2?valueInputOption=RAW` body `{"values":[[kolom...],[contoh...]]}`
  kolom: `link_affiliate, url_foto_asli, kategori, harga, diskon, caption, posted`
- Form: `POST https://forms.googleapis.com/v1/forms` (butuh Forms API enable dulu)
- Token file: `C:\Users\arija\AppData\Local\hermes\ziyan_google_token.json`
- Sheet ID hasil: `1wLqdaYcjdaxXD1nEXPIv9PHObFhQPCi80cSiUHqEG8w` (ZIYAN Shopee Affiliate)
