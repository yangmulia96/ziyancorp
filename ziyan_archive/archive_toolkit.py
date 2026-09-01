#!/usr/bin/env python3
"""
ZIYAN Archive Toolkit — Google Drive + Sheets (Service Account).
Hermes-callable: python3 archive_toolkit.py <command> [args]

Commands:
  archive  <file_path> <title> <platform> [affiliate_json_path]
            -> buat folder Drive ZIYAN_ARCHIVE/YYYY-MM/<content_id>/, upload file + AFFILIATE.json, append row ke Sheet
  list     [query]
            -> list arsip (baca Sheet)
  addlink  <content_id> <platform> <label> <url> [price_text]
            -> tambah link affiliate ke Sheet + AFFILIATE.json di Drive
  get      <content_id>
            -> ambil detail 1 konten (drive_url + semua link)
  export   [month]
            -> export semua link affiliate ke CSV

Semua operasi pakai Service Account (no-expiry). Butuh: sa_key.json + config terisi.
"""
import json, os, sys, re, datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CFG_PATH = os.path.join(os.path.dirname(__file__), "config", "archive_config.json")

def load_cfg():
    with open(CFG_PATH) as f:
        return json.load(f)

def get_services(cfg):
    creds = service_account.Credentials.from_service_account_file(
        cfg["sa_key_path"], scopes=cfg["scopes"])
    drive = build("drive", "v3", credentials=creds)
    sheets = build("sheets", "v4", credentials=creds)
    return drive, sheets

def new_content_id():
    d = datetime.date.today()
    seq = int(datetime.datetime.now().strftime("%H%M%S"))
    return f"ZA-{d.strftime('%Y%m%d')}-{seq:03d}"

def find_or_create_month_folder(drive, parent_id, month):
    q = f"mimeType='application/vnd.google-apps.folder' and name='{month}' and '{parent_id}' in parents and trashed=false"
    res = drive.files().list(q=q, fields="files(id,name)").execute()
    if res.get("files"):
        return res["files"][0]["id"]
    meta = {"name": month, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
    return drive.files().create(body=meta, fields="id").execute()["id"]

def create_content_folder(drive, parent_id, content_id):
    meta = {"name": content_id, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
    return drive.files().create(body=meta, fields="id").execute()["id"]

def upload_file(drive, folder_id, path):
    name = os.path.basename(path)
    meta = {"name": name, "parents": [folder_id]}
    media = MediaFileUpload(path, resumable=True)
    return drive.files().create(body=meta, media_body=media, fields="id,webViewLink").execute()

def append_sheet_row(sheets, sheet_id, row):
    sheets.spreadsheets().values().append(
        spreadsheetId=sheet_id, range="ARSIP_MASTER!A:K",
        valueInputOption="USER_ENTERED", body={"values": [row]}).execute()

def archive(file_path, title, platform, affiliate_json=None):
    cfg = load_cfg()
    drive, sheets = get_services(cfg)
    month = datetime.date.today().strftime("%Y-%m")
    parent = find_or_create_month_folder(drive, cfg["drive_folder_id"], month)
    cid = new_content_id()
    cfid = create_content_folder(drive, parent, cid)
    up = upload_file(drive, cfid, file_path)
    aff = {}
    if affiliate_json and os.path.exists(affiliate_json):
        aff = json.load(open(affiliate_json))
        # upload affiliate json ke folder yang sama
        tmp = os.path.join(os.path.dirname(affiliate_json), "AFFILIATE.json")
        with open(tmp, "w") as f:
            json.dump(aff, f, indent=2)
        upload_file(drive, cfid, tmp)
    plats = aff.get("platforms", {})
    row = [
        cid, title, platform, up.get("webViewLink", ""),
        ", ".join(x.get("url", "") for x in plats.get("shopee", [])),
        ", ".join(x.get("url", "") for x in plats.get("tiktok", [])),
        ", ".join(x.get("url", "") for x in plats.get("tokopedia", [])),
        ", ".join(x.get("url", "") for x in plats.get("amazon", [])),
        ", ".join(x.get("url", "") for x in plats.get("other", [])),
        datetime.datetime.now().isoformat(), "ARCHIVED"
    ]
    append_sheet_row(sheets, cfg["sheet_id"], row)
    print(json.dumps({"content_id": cid, "drive_url": up.get("webViewLink"), "row": row}, indent=2))

def list_archive(query=None):
    cfg = load_cfg()
    _, sheets = get_services(cfg)
    rng = "ARSIP_MASTER!A:K"
    res = sheets.spreadsheets().values().get(spreadsheetId=cfg["sheet_id"], range=rng).execute()
    rows = res.get("values", [])
    if not rows:
        print("Kosong"); return
    header = rows[0]
    for r in rows[1:]:
        if query and query.lower() not in " ".join(r).lower():
            continue
        print(dict(zip(header, r)))

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    cmd = sys.argv[1]
    if cmd == "archive":
        archive(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
    elif cmd == "list":
        list_archive(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        print("Unknown command"); print(__doc__)

if __name__ == "__main__":
    main()
