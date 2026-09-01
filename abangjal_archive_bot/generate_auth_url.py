import os, sys, json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

ROOT = Path(r"C:\Users\arija\ziyancorp\abangjal_archive_bot")
CLIENT_SECRET = ROOT / "client_secret.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

flow = InstalledAppFlow.from_client_secrets_file(
    str(CLIENT_SECRET),
    SCOPES,
    redirect_uri="http://localhost:8088/"
)

auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
print("=== GOOGLE OAUTH URL UNTUK YOUTUBE ARIJAL MEUTUWAH ===")
print(auth_url)
print("=======================================================")
