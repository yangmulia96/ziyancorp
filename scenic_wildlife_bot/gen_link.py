import sys, json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")
CLIENT_SECRET = ROOT / "client_secret.json"
TOKEN_SCENIC = ROOT / "token_scenic_wildlife.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

flow = InstalledAppFlow.from_client_secrets_file(
    str(CLIENT_SECRET),
    SCOPES,
    redirect_uri="urn:ietf:wg:oauth:2.0:oob"  # Standard copy-paste code mode
)

auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
print("="*70)
print("LINK LOGIN RESMI GOOGLE (MODE KODE):")
print("="*70)
print(auth_url)
print("="*70)
