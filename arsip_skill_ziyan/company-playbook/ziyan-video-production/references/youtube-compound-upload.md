# Upload YouTube Headless — Channel Compound Daily (token Compound)

Token: `ziyan_credentials/youtube_token_compound.json` (field: `access_token`, `refresh_token`, `scope` = `youtube.upload youtube.readonly`, `token_type`).
Client: `ziyan_credentials/youtube_desktop_client.json` — OAuth app TIPE `installed`, field bersarang di `installed.{client_id, client_secret, token_uri, auth_uri}`.

## Kenapa BUKAN nb_proof/youtube_uploader.py
Script itu di `build_credentials()` pakai `InstalledAppFlow.run_local_server(port=0)` → **BUKA BROWSER consent**. TIDAK HEADLESS → gagal di cron/otonom. Jangan pakai untuk pipeline otomatis.

## Resep headless (ziyan_upload.py) — TERBUKTI 2026-08-05
```python
import json, argparse
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN = "ziyan_credentials/youtube_token_compound.json"
CLIENT = "ziyan_credentials/youtube_desktop_client.json"

def load_creds():
    t = json.load(open(TOKEN)); c = json.load(open(CLIENT))["installed"]
    creds = Credentials(
        token=t.get("access_token"), refresh_token=t.get("refresh_token"),
        token_uri=c["token_uri"], client_id=c["client_id"], client_secret=c["client_secret"],
        scopes=t.get("scope", "").split(),
    )
    creds.refresh(Request())   # ambil access_token segar dari refresh_token
    return creds

def upload(file_path, title, description, tags, category, privacy):
    yt = build("youtube", "v3", credentials=load_creds())
    body = {"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category},
            "status": {"privacyStatus": privacy}}
    media = MediaFileUpload(file_path, mimetype="video/mp4", chunksize=5*1024*1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    return f"https://youtu.be/{resp['id']}"

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True); p.add_argument("--title", required=True)
    p.add_argument("--description", default=""); p.add_argument("--tags", default="")
    p.add_argument("--category", default="22"); p.add_argument("--privacy", default="public")
    a = p.parse_args()
    tags = [x.strip() for x in a.tags.split(",") if x.strip()]
    print(upload(a.file, a.title, a.description, tags, a.category, a.privacy))
```

## Jalankan (venv Hermes)
```
AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe ziyan_upload.py ^
  --file "C:/Users/arija/workdir/videos/2026-08-05/compound_daily_2026-08-05.mp4" ^
  --title "US Stocks Hit Record Highs as Palantir Profits Explode" ^
  --description "..." --tags "stocks,finance,palantir,compound daily" --category 22 --privacy public
```
- `categoryId`: 22 = People & Blogs, 27 = Education, 28 = Science & Technology. Compound Daily Shorts → 22 atau 28.
- Dependency sudah ada di venv (per 2026-08-05): `google-api-python-client`, `google-auth-oauthlib`.
- Validasi tiap run: setelah `refresh()`, panggil `channels().list(part="snippet", mine=True)` → harus 200 & balikin "Compound Daily".
- HAPUS butuh scope `youtube.force-ssl` (token ini tidak punya) → DELETE balik 403.
