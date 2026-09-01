"""Verifikasi video YouTube lewat Data API — bukan lewat stdout script upload.

Dipakai SESUDAH `upload_youtube_scheduled.py`. stdout script upload hanya menggemakan
respons pertama; ini menanyakan ulang ke YouTube apa yang benar-benar tersimpan.

Cara pakai (cron-safe: write_file lalu terminal, JANGAN execute_code):
    python3 ziyan_pending/_verify_upload.py <VIDEO_ID> [token_file]

Kriteria LULUS:
    channelId    = UCzWib2-2CPkWo315fzucaUw (Compound Daily)
    privacyStatus= private
    publishAt    = jadwal UTC yang diminta (14:00 WIB -> T07:00:00Z)
    uploadStatus = uploaded
NORMAL beberapa menit pertama: processingStatus=processing, duration=P0D.
Jangan laporkan itu sebagai kegagalan.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

CRED = r"C:\Users\arija\ziyan_credentials"
CLIENT = json.load(open(os.path.join(CRED, "youtube_desktop_client.json")))["installed"]

VID = sys.argv[1] if len(sys.argv) > 1 else None
TOK = os.path.join(CRED, sys.argv[2] if len(sys.argv) > 2 else "youtube_token_compound.json")

if not VID:
    print(__doc__)
    sys.exit(1)

t = json.load(open(TOK))
data = urllib.parse.urlencode({
    "client_id": CLIENT["client_id"], "client_secret": CLIENT["client_secret"],
    "refresh_token": t["refresh_token"], "grant_type": "refresh_token"}).encode()
acc = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://oauth2.googleapis.com/token", data=data, method="POST")).read())["access_token"]

url = ("https://www.googleapis.com/youtube/v3/videos"
       "?part=snippet,status,processingDetails,contentDetails&id=" + VID)
items = json.loads(urllib.request.urlopen(urllib.request.Request(
    url, headers={"Authorization": "Bearer " + acc})).read()).get("items", [])

if not items:
    print("VERIFY FAIL: video tidak ditemukan di channel token ini")
    sys.exit(1)

it = items[0]
print("ID        :", it["id"])
print("TITLE     :", it["snippet"]["title"])
print("CHANNEL   :", it["snippet"]["channelId"], "|", it["snippet"].get("channelTitle"))
print("PRIVACY   :", it["status"]["privacyStatus"])
print("PUBLISH_AT:", it["status"].get("publishAt"))
print("UPLOADSTAT:", it["status"].get("uploadStatus"))
print("PROCESSING:", it.get("processingDetails", {}).get("processingStatus"))
print("DURATION  :", it.get("contentDetails", {}).get("duration"))
print("TAGS      :", len(it["snippet"].get("tags", [])), "tags")
print("DESC_LEN  :", len(it["snippet"].get("description", "")))
