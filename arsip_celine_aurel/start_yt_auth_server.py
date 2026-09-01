import os
import sys
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

ROOT = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel")
cs = ROOT / "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

print("=== STARTING CLEAN LOCAL YOUTUBE AUTH SERVER ===", flush=True)
flow = InstalledAppFlow.from_client_secrets_file(str(cs), SCOPES)
creds = flow.run_local_server(
    host="localhost",
    port=8090,
    prompt="consent",
    open_browser=True,
    authorization_prompt_message="Silakan otorisasi di browser yang terbuka:"
)

(ROOT / "token.json").write_text(creds.to_json(), encoding="utf-8")
print("SUCCESS: YouTube Token automatically saved to token.json!", flush=True)
