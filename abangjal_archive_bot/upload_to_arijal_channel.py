import sys, os, json
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r"C:\Users\arija\ziyancorp\abangjal_archive_bot")
load_dotenv(ROOT / ".env")

TOKEN_ARIJAL = ROOT / "token_arijal.json"
local_video_path = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel\tmp_assets\test_upload_henley.mp4")

shopee_link = "https://s.shopee.co.id/8plAFEeqEI"
title = "Classic Henley Fitted T-Shirt Heavyweight Cotton Combed 200 GSM++"
desc = "Rekomendasi kaos Henley pria premium dengan bahan heavyweight cotton combed 200 GSM++. Potongan fitted pas di badan, adem, dan bikin tampilan kasual makin maskulin!"
hashtags = "#ArijalMeutuwah #ShopeeAffiliate #HenleyShirt #OutfitPria #StylePria"

caption_final = f"{shopee_link}\n\n{desc}\n\n{hashtags}"

print("=== UPLOAD KE OFFICIAL CHANNEL: ARIJAL MEUTUWAH ===")
print("Caption Target:")
print(caption_final)
print("---------------------------------------------------\n")

# 2. Upload to Channel Arijal Meutuwah
yt_creds = Credentials.from_authorized_user_file(str(TOKEN_ARIJAL))
if yt_creds.expired and yt_creds.refresh_token:
    yt_creds.refresh(Request())
yt_service = build('youtube', 'v3', credentials=yt_creds)

# Verify channel title before upload
ch = yt_service.channels().list(mine=True, part="snippet").execute()
target_channel_name = ch["items"][0]["snippet"]["title"]
target_channel_id = ch["items"][0]["id"]
print(f"Target Channel: {target_channel_name} (ID: {target_channel_id})")

if "Arijal" not in target_channel_name and "Meutuwah" not in target_channel_name:
    raise ValueError(f"GUARD REJECT: Target channel '{target_channel_name}' does not match Arijal Meutuwah!")

body = {
    'snippet': {
        'title': f'{title[:70]} #Shorts',
        'description': caption_final,
        'tags': ['Henley', 'OutfitPria', 'ShopeeAffiliate', 'Shorts', 'ArijalMeutuwah'],
        'categoryId': '26'
    },
    'status': {
        'privacyStatus': 'public',
        'selfDeclaredMadeForKids': False
    }
}
media = MediaFileUpload(str(local_video_path), mimetype='video/mp4', resumable=True)
req = yt_service.videos().insert(part='snippet,status', body=body, media_body=media)
yt_res = req.execute()
yt_id = yt_res.get('id')
yt_url = f"https://youtube.com/shorts/{yt_id}"

print(f"\n[SUKSES 100%] Video berhasil TAYANG LIVE di Channel Arijal Meutuwah!")
print(f"URL: {yt_url}")
print(f"Video ID: {yt_id}")
