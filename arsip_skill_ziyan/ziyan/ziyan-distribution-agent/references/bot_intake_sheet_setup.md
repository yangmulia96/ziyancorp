# ZIYAN Bot Intake — Google Sheet Tab Initialization

When cloning the archive bot to a NEW brand (e.g. ZIYAN → AbangJal, 17/8), the bot crashes at startup with `HttpError 400: Unable to parse range: <TAB>!1:1` for EACH missing tab. `GoogleWorkspace.__init__ → ensure_headers()` checks 3 tabs on boot.

## Required tabs + headers (PRODUCT_MASTER, CONTENT_ASSETS, PROCESS_LOG)
`ARSIP_MASTER` is also used by the distribution agent — create it too.

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
creds = Credentials.from_authorized_user_file('token.json',
    ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive'])
srv = build('sheets','v4',credentials=creds)
SID = '<SHEET_ID>'  # the new brand's spreadsheet

need = {
  'PRODUCT_MASTER': ['product_id','title','description','shopee_url','tiktok_url',
                     'other_links','folder_url','timestamp','published_at','status'],
  'CONTENT_ASSETS': ['asset_id','product_id','file_name','drive_url','mime_type','size','status'],
  'PROCESS_LOG':    ['timestamp','event','product_id','details'],
  'ARSIP_MASTER':   ['product_id','title','description','shopee_url','tiktok_url',
                     'other_links','folder_url','timestamp','status'],
}
cur = [s['properties']['title'] for s in srv.spreadsheets().get(spreadsheetId=SID).execute()['sheets']]
for name, hdr in need.items():
    if name not in cur:
        srv.spreadsheets().batchUpdate(spreadsheetId=SID,
            body={'requests':[{'addSheet':{'properties':{'title':name}}}]}).execute()
        print('ADD', name)
    srv.spreadsheets().values().update(spreadsheetId=SID, range=f'{name}!A1',
        valueInputOption='RAW', body={'values':[hdr]}).execute()
    print('HEADER', name, 'OK')
```

## Drive folder + sheet creation recipe (one pass)
```python
drive = build('drive','v3',credentials=creds)
root = '<ROOT_FOLDER_ID>'  # e.g. ZIYAN root 11m4fW0...
# 1. Brand archive folder
f = drive.files().create(body={'name':'Abangjal Arsip',
    'mimeType':'application/vnd.google-apps.folder','parents':[root]}, fields='id').execute()
folder_id = f['id']
# 2. 2026-08 subfolder
f2 = drive.files().create(body={'name':'2026-08',
    'mimeType':'application/vnd.google-apps.folder','parents':[folder_id]}, fields='id').execute()
# 3. Spreadsheet
sh = drive.files().create(body={'name':'ARSIP_ABANGJAL',
    'mimeType':'application/vnd.google-spreadsheets','parents':[folder_id]}, fields='id').execute()
sheet_id = sh['id']
# 4. Then run the tab-init block above with SID=sheet_id
print('FOLDER', folder_id, 'SHEET', sheet_id)
```

## Pitfalls
- `gw.sheets.get_values(...)` / `gw.drive.list_files(...)` → AttributeError (GoogleWorkspace is a thin wrapper, not the raw Resource). Use the raw `build()` client for setup, or the agent's `get_products_latest()` etc. for runtime.
- A sheet created via `drive.files().create` may briefly return 400 on `values.update` (race). Retry once or use the second `build()` block above which creates cleanly then inits headers.
- Bot still needs `TELEGRAM_BOT_TOKEN` + `TELEGRAM_ALLOWED_USER_IDS` + `GOOGLE_ROOT_FOLDER_ID` + `GOOGLE_SPREADSHEET_ID` in `.env` before `config.from_env()` passes. Missing → RuntimeError (expected for fresh blueprint).
- Never copy `.env`, `token*.json`, `client_secret.json`, `credentials.json` between brands — per-brand secrets.
