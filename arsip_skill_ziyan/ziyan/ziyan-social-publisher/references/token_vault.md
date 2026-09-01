# Meta Token Vault — Recipe (2026-08-15)

## Lokasi
- Vault: `C:\Users\arija\.hermes\vault\*.gpg` (AES256)
- Passphrase: `~/.hermes/.env` → `VAULT_PASS`
- Script: `C:\Users\arija\bin\token_vault.sh`

## Dekripsi (SELALU lewat script)
```bash
cd /c/Users/arija
PAGE_TOK=$(bash bin/token_vault.sh get fb_page_token 2>/dev/null | tr -d '\n')
USER_TOK=$(bash bin/token_vault.sh get fb_user_token 2>/dev/null | tr -d '\n')
```
**JANGAN** `gpg --decrypt file.gpg` langsung → hang 25s (interactive prompt gak muncul di non-tty).

## Simpan token baru
```bash
bash bin/token_vault.sh set fb_page_token "$PAGE_TOK"
bash bin/token_vault.sh set fb_user_token "$USER_TOK"
```

## Bos kasih User Token (EAA...) → exchange ke Page Token 60 hari
```bash
APPID=$(cat OneDrive/ziyan_pending/fb_app_id.txt)
APPSEC=$(cat OneDrive/ziyan_pending/fb_app_secret.txt)
SHORT="<EAA... dari Bos>"   # user token pendek (~1 jam expired)
LONG=$(curl -s "https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=$APPID&client_secret=$APPSEC&fb_exchange_token=$SHORT" | python3 -c "import sys,json;print(json.load(sys.stdin).get('access_token',''))")
curl -s "https://graph.facebook.com/v19.0/me/accounts?fields=id,name,access_token&access_token=$LONG" | python3 -c "
import sys,json
for p in json.load(sys.stdin).get('data',[]):
    if p.get('id')=='975723622288353':
        print(p['access_token'])
"
```

## Verifikasi token valid
```bash
curl -s "https://graph.facebook.com/v19.0/me?access_token=$PAGE_TOK"
# user Celine Aurel + id 122119007576915460 = VALID
```

## Status token (2026-08-15)
| Token | State |
|-------|-------|
| fb_page_token (vault) | VALID (re-auth 14-Agu) |
| fb_user_token (vault) | VALID |
| threads_token (vault) | EXPIRED (decrypt OK, API error 190) |
| IG/Threads via Page | BELUM LINK (field gak ada di API) |

## App Credentials
- App ID: 1994676317847313 (di OneDrive/ziyan_pending/fb_app_id.txt)
- App Secret: OneDrive/ziyan_pending/fb_app_secret.txt
- Page ID: 975723622288353
- User ID: 122119007576915460
- Valid OAuth Redirect: https://localhost:8123/
- Re-auth script: C:\Users\arija\ziyancorp\ziyan_archive_bot\fb_reauth.py
