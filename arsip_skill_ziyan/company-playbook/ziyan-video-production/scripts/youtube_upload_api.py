#!/usr/bin/env python3
"""
youtube_upload_api.py - Upload video ke channel Compound Daily via YouTube Data API v3.

TERVERIFIKASI: video ID HvN-fR1FcLQ (2026-08-01, HTTP 200, privacy public).

Cara pakai:
    python3 youtube_upload_api.py --video short_03.mp4 --meta meta.json [--privacy public]

Token : ziyan_credentials/youtube_token_compound.json (refresh_token + scope youtube.upload)
Client: ziyan_credentials/youtube_desktop_client.json (installed app)

meta.json:
{
  "title": "...",
  "description": "...",
  "tags": ["..."],
  "categoryId": "28",
  "defaultLanguage": "en",
  "defaultAudioLanguage": "en"
}
"""
import argparse, json, os, requests

BASE = r"C:\Users\arija\ziyan_credentials"
TOKEN_FILE = os.path.join(BASE, "youtube_token_compound.json")
CLIENT_FILE = os.path.join(BASE, "youtube_desktop_client.json")


def refresh():
    tok = json.load(open(TOKEN_FILE))
    client = json.load(open(CLIENT_FILE))["installed"]
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "refresh_token": tok["refresh_token"],
        "grant_type": "refresh_token",
    })
    if r.status_code != 200:
        raise SystemExit(f"REFRESH FAIL {r.status_code}: {r.text[:200]}")
    j = r.json()
    tok["access_token"] = j["access_token"]
    tok["expires_in"] = j.get("expires_in", 3599)
    json.dump(tok, open(TOKEN_FILE, "w"), indent=2)
    return tok["access_token"]


def verify(access):
    vr = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
        headers={"Authorization": f"Bearer {access}"})
    if vr.status_code != 200:
        raise SystemExit(f"VERIFY FAIL {vr.status_code}: {vr.text[:200]}")
    items = vr.json().get("items", [])
    if not items:
        raise SystemExit("TOKEN tidak terikat ke channel manapun!")
    for c in items:
        print("  bound channel:", c["snippet"]["title"], c["snippet"].get("customUrl", "-"))


def upload(video, meta, access, privacy):
    meta = dict(meta)
    meta["status"] = {"privacyStatus": privacy, "selfDeclaredMadeForKids": False}
    boundary = "----ytdboundary7f3a9c"
    meta_part = (
        f"--{boundary}\r\n"
        f"Content-Type: application/json; charset=UTF-8\r\n"
        f"Content-Disposition: form-data; name=\"metadata\"\r\n\r\n"
        f"{json.dumps(meta)}\r\n"
    ).encode("utf-8")
    with open(video, "rb") as f:
        vid = f.read()
    media_part = (
        f"--{boundary}\r\n"
        f"Content-Type: video/mp4\r\n"
        f"Content-Disposition: form-data; name=\"media\"; filename=\"{os.path.basename(video)}\"\r\n\r\n"
    ).encode("utf-8") + vid + f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = meta_part + media_part
    headers = {
        "Authorization": f"Bearer {access}",
        "Content-Type": f"multipart/related; boundary={boundary}",
        "Content-Length": str(len(body)),
    }
    url = ("https://www.googleapis.com/upload/youtube/v3/videos"
           "?uploadType=multipart&part=snippet,status,contentDetails")
    r = requests.post(url, headers=headers, data=body)
    print("UPLOAD STATUS:", r.status_code)
    if r.status_code == 200:
        j = r.json()
        print("VIDEO_ID:", j["id"])
        print("WATCH:", "https://youtu.be/" + j["id"])
        print("PRIVACY:", j.get("status", {}).get("privacyStatus"))
        print("CHANNEL_ID:", j.get("snippet", {}).get("channelId"))
        return j["id"]
    print("UPLOAD BODY:", r.text[:1000])
    raise SystemExit("UPLOAD GAGAL")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--privacy", default="public")
    a = ap.parse_args()
    meta = json.load(open(a.meta, encoding="utf-8"))
    access = refresh()
    verify(access)
    upload(a.video, meta, access, a.privacy)


if __name__ == "__main__":
    main()
