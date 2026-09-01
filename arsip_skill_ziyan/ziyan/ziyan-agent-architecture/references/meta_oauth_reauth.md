# Meta OAuth Re-Auth Pitfalls (ZIYAN, 2026-08-16)

Bos re-auth IG/Threads via `fb_reauth.py` (atau manual di Meta Console). Fakta teruji saat sesi 16/8 — jangan ulang kesalahan ini.

## Alur Re-Auth (yg bener)
1. Jalankan `fb_reauth.py` tanpa argumen -> print **login URL** (pakai APP_ID dari file/secret yg VALID).
2. Bos buka URL di HP -> authorize -> browser redirect ke `https://localhost:8123/?code=XXX` (biasanya blank/error, gak apa-apa).
3. Bos **copy URL redirect lengkap** -> paste ke agent.
4. Agent jalankan `fb_reauth.py "<URL>"` -> extract `code` -> tukar token -> print PAGE_TOKEN + IG_BIZ_ID.
5. Simpan token ke `.env` + vault (`bin/token_vault.sh set ...`).

## PITFALLS (semua kejadian 16/8)
- **App ID digit mismatch:** URL login pakai `1994676317847313` tapi app bener di console = `19946763178947313` (selisih 1 angka). Secret gak akan pernah match. SELALU cross-check App ID dari console screenshot, bukan dari ingatan/file lama.
- **Secret desync (OneDrive vs Vault):** `~/OneDrive/ziyan_pending/fb_app_secret.txt` (`19f1b7...`) BEDA dengan vault `fb_app_secret` (`99068c...`). Dua-duanya salah untuk app yg dipakai. Pakai secret ASLI dari Meta Console -> Show App Secret.
- **App "Unpublished" + gak punya product:** App `n8n` status Unpublished, gak ada Instagram Graph API product -> `Error validating application` saat tukar code. BUTUH: Meta Console -> Add Product -> Instagram Graph API + Threads, lalu link IG Business `@celineaurel99`.
- **Code expires ~10 menit:** Meta `code` dari redirect HANYA valid ~10 menit. Jangan muter-muter cek secret sambil code masih pending -> generate URL BARU setelah secret benar.
- **FB App vs Threads App terpisah:** Threads punya App ID/Secret SENDIRI (`1546767553487099` di Threads Integration section). Untuk Threads token murni, pakai Threads App, bukan FB App.
- **Threads delete gak bisa via API:** `DELETE graph.threads.net/v1.0/<id>` -> `code:10 Application does not have permission`. Bos HARUS hapus manual di HP (3-dot -> Delete).
- **Token scope:** FB_PAGE_TOKEN (vault) masih valid lama; META_USER_TOKEN / THREADS_USER_TOKEN expired -> IG & Threads mati, FB jalan. Test validitas tiap token via `GET /me?access_token=` sebelum klaim.

## Verifikasi Token (script cepat)
```python
import os, requests
from dotenv import load_dotenv; load_dotenv('.env')
for k in ['FB_PAGE_TOKEN','META_USER_TOKEN','THREADS_USER_TOKEN']:
    t=os.environ.get(k,'')
    r=requests.get('https://graph.facebook.com/v20.0/me',params={'access_token':t},timeout=15)
    print(k, 'OK' if r.status_code==200 else f'ERR {r.status_code}')
```

## Endpoint beda per platform
- FB/IG: `graph.facebook.com/v20.0/`
- Threads: `graph.threads.net/v1.0/` (user token, App ID/Secret Threads)
