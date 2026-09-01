# FB Token — Short-Lived Reality (verified 2026-08-15)

## FAKTA (bukan asumsi)
Meta access token untuk akun Celine Aurel (FB Page `975723622288353`) = **SHORT-LIVED ~6 JAM**, BUKAN 60 hari.

Bukti sesi 15/8:
- Token dari Graph Explorer app "n8n"/"nibs" → expired same day (error 190 subcode 463 "Session has expired")
- Token dari `fb_reauth.py` (setelah `fb_exchange_token` POST form) → expired ~6 jam kemudian
- `debug_token` tidak menampilkan `expires_at` → jangan gunakan sebagai bukti "long-lived"

## FLOW RE-AUTH YANG WORK (verified)
```bash
cd /c/Users/arija/ziyancorp/ziyan_archive_bot
# 1. Print login URL (app 1994676317847313)
env -u PYTHONPATH ./venv/Scripts/python.exe fb_reauth.py
# 2. Bos buka URL di HP -> authorize -> paste redirect URL (https://localhost:8123/?code=...)
env -u PYTHONPATH ./venv/Scripts/python.exe fb_reauth.py "https://localhost:8123/?code=XXXX"
# 3. Script: code -> user token -> me/accounts -> PAGE token
# 4. Simpan vault
bash bin/token_vault.sh set fb_page_token "$PTOK"
bash bin/token_vault.sh set fb_user_token "$UTOK"
# 5. VALIDATE (wajib)
PTOK=$(bash bin/token_vault.sh get fb_page_token 2>/dev/null | tr -d '\n')
curl -s "https://graph.facebook.com/v20.0/975723622288353?fields=id,name&access_token=$PTOK"
# harus return {"id":"975723622288353","name":"Celine Aurel "}
```

## App credentials
- App ID: `199467631784631` (di `OneDrive/ziyan_pending/fb_app_id.txt`)
- App Secret: `OneDrive/ziyan_pending/fb_app_secret.txt`
- Redirect URI di app: `https://localhost:8123/`

## JANGAN
- Jangan asumsi token "60 hari" — selalu validate sebelum pakai
- Jangan pakai USER token untuk posting (403) — harus PAGE token dari `me/accounts`
- Jangan percaya klaim "100% valid" tanpa test API sendiri (agent lain sering salah)
