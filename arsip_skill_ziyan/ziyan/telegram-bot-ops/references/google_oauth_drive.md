# Google OAuth (user) for Drive/Sheets writes

## Why
Service Accounts (SA) cannot write to a personal Google Drive — they hit their own
(zero) storage quota: `403 storageQuotaExceeded`. Share-the-folder tricks do NOT help
because quota is charged to the SA, not the folder owner. Use an **OAuth user** token.

## Flow
1. Google Cloud Console -> APIs & Services -> Credentials -> Create OAuth client ID
   -> Application type: Desktop app -> download JSON -> `client_secret.json`.
2. Place `client_secret.json` in the bot dir.
3. Run the auth script with `GOOGLE_CREDENTIALS_FILE=client_secret.json`:
   `env -u PYTHONPATH GOOGLE_CREDENTIALS_FILE=client_secret.json ./venv/Scripts/python.exe scripts/google_auth.py`
4. Open the printed URL in a browser **on the same machine** as the bot. Log in with the
   account that owns the target Drive folder. Allow Drive + Sheets scopes.
5. Browser redirects to `http://localhost:<port>/?code=...&state=...` — the script
   auto-captures it and writes `token.json`. (If the page shows "can't be reached",
   that is EXPECTED — the redirect was still caught locally.)

## Manual code exchange (fallback when redirect isn't caught)
If the auto-catch fails (e.g. you opened the URL from a different device), use a script
that reads the full redirect URL from stdin, extracts `code=`, and exchanges it:
```python
import sys, json
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file('client_secret.json',
    ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets'])
flow.fetch_token(authorization_response=sys.stdin.read().strip())
json.dump(json.loads(flow.credentials.to_json()), open('token.json','w'))
print('TOKEN SAVED')
```
> The OAuth `code` is single-use and expires in ~30s. Paste the redirect URL immediately.

## Pitfalls
- **Test users**: if the consent screen is in "Testing" mode, add the owner's email as a
  Test User or token exchange returns `invalid_grant`.
- **Multiple instances**: only ONE bot should run; see SKILL.md section 1.
- `GoogleWorkspace` prefers `token.json` over the SA key when both exist — no code change
  needed once `token.json` is present.
