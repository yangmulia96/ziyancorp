# FB / IG / Threads Token Re-Auth & Diagnosis (15-Agt-2026)

## Vault mekanisme (WAJIB pakai, jangan hardcode)
Passphrase di `~/.hermes/.env` (`VAULT_PASS`). Tool: `C:\Users\arija\bin\token_vault.sh`
```bash
bash bin/token_vault.sh get fb_page_token      # decrypt -> stdout (token)
bash bin/token_vault.sh set fb_page_token "$TOK"  # encrypt AES256
bash bin/token_vault.sh list
```
File terenkripsi: `.hermes/vault/*.gpg` (fb_page_token, fb_user_token, threads_token, instagram_token).

## FB Page re-auth (terbukti jalan)
1. Bos kasih **Page/User access token** (format `EAA...`) -> verifikasi:
   `curl "https://graph.facebook.com/v20.0/me?access_token=$TOK"` -> harus return `{"name":"Celine Aurel","id":"122119007576915460"}`.
2. Ambil **Page token** dari `me/accounts`:
   `curl ".../me/accounts?access_token=$TOK&fields=id,name,access_token"` -> data[].access_token = PAGE_TOKEN.
3. Simpan: `bash bin/token_vault.sh set fb_page_token "$PAGE_TOKEN"`.
4. Page Celine Aurel id = `975723622288353` (jangan typo: bukan `97573262288353` / `97572362283593`).

## IG diagnosis: "Sudah link di HP tapi API bilang belum"
Fakta absolut dari sesi ini:
- Bos link IG<->FB di HP, tapi `me/accounts?fields=instagram_business_account` return **kosong** (field gak ada, error 100).
- Penyebab umum:
  1. IG belum **Professional/Business account** (Settings -> Account -> Switch to Professional).
  2. Di IG: Settings -> Account -> Linked Accounts -> Facebook -> memilih **FB personal profile**, bukan **FB Page "Celine Aurel"**. Harus Page.
  3. Threads butuh IG Business dulu, baru bisa link.
- Verifikasi dari sisi FB (pakai PAGE_TOKEN atau USER_TOKEN):
  `curl ".../975723622288353?fields=instagram_business_account{id,username}&access_token=$PAGE_TOK"`
  - Sukses -> return `instagram_business_account: {id, username}` -> simpan IG_CELINE_ID.
  - Error 100 `nonexisting field` -> IG BELUM ter-link ke Page ini.

## IG token langsung (Graph Explorer app "n8n"/"nibs")
- Bos bisa generate IG token di developers.facebook.com -> Graph API Explorer -> "Generate Access Token" -> **Copy Token**.
- Token `EAA...` dari Bos kadang **invalid/cannot parse** (kepotong saat copy). Minta Bos klik "Copy Token" (jangan ketik manual).
- Verifikasi: `curl "https://graph.instagram.com/v25.0/me?fields=id,username&access_token=$IG_TOK"`.

## Threads
- `threads_token.gpg` lama = **expired** (error 190).
- Threads token didapat dari Graph API setelah IG Business ter-link ke Page:
  `curl ".../975723622288353/threads_business_account?access_token=$PAGE_TOK"` (endpoint terpisah, bukan field di Page node).
- Atau via Graph Explorer dengan permission `threads_business_account`.

## App credentials
- FB App ID: `OneDrive/ziyan_pending/fb_app_id.txt` (app `1994676317847313`)
- FB App Secret: `OneDrive/ziyan_pending/fb_app_secret.txt`
- Valid OAuth Redirect: `https://localhost:8123/`
- Script re-auth siap pakai: `ziyancorp/ziyan_archive_bot/fb_reauth.py` (tanpa arg = print login URL; dengan arg URL redirect = exchange token).

## Status token (14-Agt-2026)
| Platform | State |
|---------|-------|
| FB Page (`975723622288353`) | VALID, vault |
| FB User | VALID, vault |
| YouTube Celine (`UC8Lzhi5_SvJZcecD79xIiog`) | `youtube_token_celineaurel.json` |
| IG Celine | belum ter-link ke Page |
| Threads | expired / belum link |
