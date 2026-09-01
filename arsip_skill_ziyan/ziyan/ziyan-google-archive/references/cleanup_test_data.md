# Cleanup Ghost / Test Data from ZIYAN Archive

## When
- Bos flags "file hantu" / junk in his Drive or Sheets.
- After any E2E test run that wrote real data (test_full_chain.py, test_bos_spec.py, etc.).

## Identify real vs test
Drive path: `ZIYAN_ARCHIVE (root) / 2026-08 / PROD-YYYYMMDD-XXXXXX_...`
```python
import os, sys; sys.path.append('.')
from dotenv import load_dotenv; load_dotenv('.env')
from distributor import Settings, GoogleWorkspace
s = Settings.from_env()
gw = GoogleWorkspace(s.google_credentials_file, s.google_token_file, s.google_root_folder_id, s.google_spreadsheet_id)
month = '1TPfsj_C1zUpIzHPjjRUNHgpORlZPG8jG'  # folder "2026-08" — get via list, jangan hardcode
r = gw.drive.files().list(q=f"'{month}' in parents and trashed=false", fields='files(id,name)').execute()
for f in r.get('files', []):
    print(f['id'], '||', f['name'])  # PROD-20260816-* = test; PROD-20260815-* = real
```
Real folder contents (keep): actual `telegram_XX.jpg/.mp4` + `PRODUCT_INFO.txt` + `AFFILIATE.json`.
Test folder contents (delete): dummy PNGs, captions `KAOS TEST` / `FULL CHAIN TEST`.

## Purge (reversible — goes to Drive Trash, 30d)
```python
ghost = {name: fid for name, fid in all_items if name.startswith('PROD-20260816')}
for name, fid in ghost.items():
    gw.drive.files().delete(fileId=fid).execute()   # trash, not permanent
```

## Strip Sheet rows
```python
import re
pat = re.compile(r'^PROD-20260816-')
pm = gw.sheets.spreadsheets().values().get(spreadsheetId=s.google_spreadsheet_id, range='PRODUCT_MASTER!A:Z').execute()
keep = [r for r in pm.get('values', []) if not (r and pat.match(str(r[0])))]
ca = gw.sheets.spreadsheets().values().get(spreadsheetId=s.google_spreadsheet_id, range='CONTENT_ASSETS!A:Z').execute()
keep_ca = [r for r in ca.get('values', []) if not (r and pat.match(str(r[0])))]
gw.sheets.spreadsheets().values().clear(spreadsheetId=s.google_spreadsheet_id, range='PRODUCT_MASTER!A:Z').execute()
gw.sheets.spreadsheets().values().update(spreadsheetId=s.google_spreadsheet_id, range='PRODUCT_MASTER!A1', valueInputOption='RAW', body={'values': keep}).execute()
# same for CONTENT_ASSETS
```

## Prevention (do this BEFORE next test)
Option A — isolate: inside the test script set a dedicated test folder + spreadsheet:
```python
s.google_root_folder_id = '<test_folder_id>'          # separate from Bos's real archive
s.google_spreadsheet_id = '<test_sheet_id>'
```
Option B — self-cleanup: at end of the test script, run the purge + Sheet-strip above for the test-date prefix it created.

Bos monitors his Drive personally. Leftover test artifacts = lost trust. Always clean.
