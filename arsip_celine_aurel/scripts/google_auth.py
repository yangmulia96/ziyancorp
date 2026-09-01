from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
credentials_file = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", ROOT / "credentials.json"))
if not credentials_file.is_absolute():
    credentials_file = ROOT / credentials_file
token_file = Path(os.getenv("GOOGLE_TOKEN_FILE", ROOT / "token.json"))
if not token_file.is_absolute():
    token_file = ROOT / token_file

if not credentials_file.exists():
    raise SystemExit(f"File OAuth tidak ditemukan: {credentials_file}")
flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), SCOPES)
creds = flow.run_local_server(port=0)
token_file.write_text(creds.to_json(), encoding="utf-8")
print(f"Token tersimpan di {token_file}")
