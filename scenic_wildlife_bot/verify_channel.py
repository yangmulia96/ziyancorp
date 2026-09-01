from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

token_path = r"C:\Users\arija\ziyancorp\scenic_wildlife_bot\token_scenic_wildlife.json"
creds = Credentials.from_authorized_user_file(token_path)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds)

ch = yt.channels().list(mine=True, part="snippet,statistics").execute()
if ch.get("items"):
    item = ch["items"][0]
    print("="*60)
    print("STATUS RESMI CHANNEL TERHUBUNG:")
    print("="*60)
    print("Nama Channel :", item["snippet"]["title"])
    print("Handle       :", item["snippet"].get("customUrl", "@4kscenicwildlife"))
    print("Subscribers  :", item["statistics"].get("subscriberCount", "0"))
    print("Total Video  :", item["statistics"].get("videoCount", "0"))
    print("="*60)
