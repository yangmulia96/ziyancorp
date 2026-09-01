import os, sys, json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(r"C:\Users\arija\ziyancorp\abangjal_archive_bot")
CLIENT_SECRET = ROOT / "client_secret.json"
TOKEN_ARIJAL = ROOT / "token_arijal.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

def main():
    if not CLIENT_SECRET.exists():
        src = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel\client_secret.json")
        if src.exists():
            CLIENT_SECRET.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            print("Copied client_secret.json to abangjal_archive_bot")

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    print("\n" + "="*60)
    print("OTENTIKASI YOUTUBE CHANNEL: ARIJAL MEUTUWAH")
    print("="*60)
    
    creds = flow.run_local_server(port=8088, prompt='consent', access_type='offline')
    
    TOKEN_ARIJAL.write_text(creds.to_json(), encoding="utf-8")
    print(f"\n[OK] Token YouTube Arijal tersimpan di: {TOKEN_ARIJAL}")
    
    # Inspect channel details
    yt = build("youtube", "v3", credentials=creds)
    ch = yt.channels().list(mine=True, part="snippet,contentDetails,statistics").execute()
    for item in ch.get("items", []):
        title = item["snippet"]["title"]
        cid = item["id"]
        print(f"-> Terhubung ke Channel YouTube: {title} (Channel ID: {cid})")

if __name__ == "__main__":
    main()
