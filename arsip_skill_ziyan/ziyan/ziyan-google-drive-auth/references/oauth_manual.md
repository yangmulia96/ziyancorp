# Manual OAuth code exchange (Windows, no localhost catch)

When `scripts/google_auth.py` (which uses `InstalledAppFlow.run_local_server`) cannot catch the
browser redirect — e.g. Bos opens the auth URL from a phone, or the listener port is unreachable —
exchange the `code` yourself:

1. Start the flow to get a FRESH auth URL (state changes every run):
   ```
   env -u PYTHONPATH GOOGLE_CREDENTIALS_FILE=client_secret.json ./venv/Scripts/python.exe scripts/google_auth.py
   ```
   Copy the printed `https://accounts.google.com/o/oauth2/auth?...` URL.

2. Open it in a browser, log in with the Bos Google account (must be a Test User on the
   OAuth consent screen), click Allow. Browser redirects to `http://localhost:PORT/...`
   and shows a connection error — that is expected. Copy the FULL redirect URL from the address bar.

3. Exchange the code with this helper (pipe the redirect URL via stdin so it is not single-quoted):
   ```python
   # oauth_manual.py
   import sys
   from pathlib import Path
   from dotenv import load_dotenv
   from google_auth_oauthlib.flow import InstalledAppFlow
   ROOT = Path(r"C:\Users\arija\ziyancorp\ziyan_archive_bot")
   load_dotenv(ROOT / ".env")
   flow = InstalledAppFlow.from_client_secrets_file(
       str(ROOT / "client_secret.json"),
       ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"])
   flow.redirect_uri = "http://localhost"
   auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")
   print("AUTH_URL:", auth_url)
   resp = input("Paste full redirect URL: ").strip()
   code = resp.split("code=")[1].split("&")[0] if "code=" in resp else resp
   flow.fetch_token(code=code)
   (ROOT / "token.json").write_text(flow.credentials.to_json(), encoding="utf-8")
   print("TOKEN SAVED ->", ROOT / "token.json")
   ```
   Run:
   ```
   echo "<full redirect URL>" | env -u PYTHONPATH ./venv/Scripts/python.exe oauth_manual.py
   ```

## Gotchas
- The `code` is single-use and expires in ~30s. If you see `invalid_grant`/`invalid_grant`,
  the code was already used or expired — re-run step 1 for a new URL and repeat quickly.
- `invalid_grant` with a fresh code almost always means the Bos account is NOT added as a
  Test User on the OAuth consent screen (External app, "restricted to test users").
- After `token.json` exists, `google_workspace.py` uses OAuth automatically; the `.env`
  `GOOGLE_CREDENTIALS_FILE` can stay pointing at `client_secret.json`.
