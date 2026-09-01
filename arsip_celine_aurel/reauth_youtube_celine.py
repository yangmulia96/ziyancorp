#!/usr/bin/env python3
"""
SKRIP AUTENTIKASI ULANG YOUTUBE CELINE AUREL
Jalankan SEKALI dari laptop dengan browser terbuka.
Setelah berhasil, token akan tersimpan di token_celine.json dan tidak perlu diulang.
"""
import sys
from pathlib import Path
import json

ROOT = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel")
sys.path.insert(0, str(ROOT))

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

TOKEN_FILE = ROOT / "token_celine.json"

CLIENT_ID = "3131524149-5nk7lrhpmkk62letakgpg3bjlld0qnau.apps.googleusercontent.com"
CLIENT_SECRET = "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"

client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost:8080/"]
    }
}

print("=" * 60)
print("AUTENTIKASI YOUTUBE CELINE AUREL")
print("=" * 60)
print()
print("Browser akan terbuka secara otomatis.")
print("Login dengan akun Google CELINE AUREL!")
print()

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_local_server(port=8080, open_browser=True)

# Save token
token_data = {
    "token": creds.token,
    "refresh_token": creds.refresh_token,
    "token_uri": creds.token_uri,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scopes": list(creds.scopes),
    "universe_domain": "googleapis.com",
    "account": "",
    "expiry": creds.expiry.strftime("%Y-%m-%dT%H:%M:%SZ") if creds.expiry else ""
}
TOKEN_FILE.write_text(json.dumps(token_data, indent=2), encoding="utf-8")

print()
print("=" * 60)
print(f"SUKSES! Token Celine Aurel tersimpan di:")
print(f"  {TOKEN_FILE}")
print("Mesin distribusi otomatis sudah siap upload ke YouTube Celine!")
print("=" * 60)
