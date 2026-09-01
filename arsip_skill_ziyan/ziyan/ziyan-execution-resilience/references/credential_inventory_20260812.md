# Credential Inventory — 2026-08-12

## Full scan result (16 credential entries across 8 files)

| # | Credential | File | Status |
|---|------------|------|--------|
| 1 | `GEMINI_API_KEY` | AppData/Local/hermes/.env | ✅ Ada (Antigravity, optional) |
| 2 | `OPENAI_API_KEY` | AppData/Local/hermes/.env | ⚠️ Legacy, tidak dipakai |
| 3 | `OPENROUTER_API_KEY` | AppData/Local/hermes/.env | ✅ Aktif (parent model CEO) |
| 4 | `DISCORD_BOT_TOKEN` | AppData/Local/hermes/.env | ❌ Gateway failed (expired/invalid) |
| 5 | `DISCORD_ALLOWED_USERS` | AppData/Local/hermes/.env | ✅ Whitelist |
| 6 | `DISCORD_HOME_CHANNEL` | AppData/Local/hermes/.env | ✅ Channel ID |
| 7 | `TELEGRAM_BOT_TOKEN` | AppData/Local/hermes/.env | ✅ Aktif (Hermes TG gateway) |
| 8 | `TELEGRAM_ALLOWED_USERS` | AppData/Local/hermes/.env | ✅ Whitelist |
| 9 | `HERMES_CUSTOM_9ROUTER_API_KEY` | AppData/Local/hermes/config.yaml | ✅ Aktif (9Router 200 OK) |
| 10 | `9Router Key sk-0867...` | .9remote/keys.json | ✅ Aktif |
| 11 | `Google Service Account` | ziyan_agent/credentials/service_account.json | ✅ Aktif (SA OK, project ziyancorp) |
| 12 | `YouTube Token (Celine Aurel)` | ziyan_agent/ziyan_credentials/youtube_token_celineaurel.json | ❌ EXPIRED (2026-08-11, access_token kosong, refresh ada) |
| 13 | `YouTube Desktop Client` | ziyan_agent/ziyan_credentials/youtube_desktop_client.json | ✅ OAuth client |
| 14 | `Telegram Bot Token (ziyan)` | ziyan_agent/config.yaml | ✅ Aktif (bot polling OK, getMe 200) |
| 15 | `ROOT .env` | .env (root) | ⚠️ Kosong, tidak terpakai |
| 16 | `n8n Encryption Key` | .n8n/config | ⚠️ Legacy (n8n dibuang) |

## Verification commands (SAFE — no bare tokens in argv)

```bash
# 1. .env key names only
grep -oE "^[A-Z_]+=" .env AppData/Local/hermes/.env

# 2. 9Router health (env var already exported)
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:20128/v1/models

# 3. Google SA validity
cd ziyan_agent && .venv/Scripts/python.exe -c "
from google.oauth2.service_account import Credentials
c=Credentials.from_service_account_file('credentials/service_account.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
print('SA OK', c.project_id)"

# 4. Telegram bot (read token from config, not literal)
python3 << 'EOF'
import re, json, requests
cfg = open('ziyan_agent/config.yaml').read()
tok = re.search(r'bot_token: "([^"]+)"', cfg).group(1)
r = requests.get(f"https://api.telegram.org/bot{tok}/getMe", timeout=10)
print(r.json().get('result',{}).get('username'), r.status_code)
EOF

# 5. YouTube token expiry
python3 << 'EOF'
import json, time
d = json.load(open('ziyan_agent/ziyan_credentials/youtube_token_celineaurel.json'))
exp = d.get('expiry','').replace('.772816','').replace('Z','')
exp_ts = time.mktime(time.strptime(exp, '%Y-%m-%dT%H:%M:%S'))
print('YT:', 'EXPIRED' if exp_ts < time.time() else 'VALID', exp)
EOF

# 6. Discord — DO NOT curl with literal token (hardline block).
#    Use python heredoc reading .env:
python3 << 'EOF'
import re, requests
env = open('AppData/Local/hermes/.env').read()
tok = re.search(r'DISCORD_BOT_TOKEN="([^"]+)"', env).group(1)
r = requests.get("https://discord.com/api/v10/gateway/bot", headers={"Authorization": f"Bot {tok}"}, timeout=10)
print(r.status_code, r.text[:120])
EOF
```

## Consolidated inventory file
`C:\Users\arija\ZIYAN_SECRETS.md` — lokasi + status semua credential TANPA nilai mentah.
Bisa dihapus legacy (#2 OpenAI, #15 root .env, #16 n8n) setelah Bos konfirmasi.
