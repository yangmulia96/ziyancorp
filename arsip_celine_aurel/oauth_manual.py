import os, sys
from pathlib import Path
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

ROOT = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel")
load_dotenv(ROOT / ".env")
cs = ROOT / "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
flow = InstalledAppFlow.from_client_secrets_file(str(cs), SCOPES)
flow.redirect_uri = "http://localhost"
auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")
print("AUTH_URL:", auth_url)
print("PASTE full redirect URL (atau cukup bagian 'code=') setelah authorize:")
resp = input("> ").strip()
if "code=" in resp:
    code = resp.split("code=")[1].split("&")[0]
else:
    code = resp
flow.fetch_token(code=code)
(ROOT / "token.json").write_text(flow.credentials.to_json(), encoding="utf-8")
print("TOKEN SAVED ->", ROOT / "token.json")
