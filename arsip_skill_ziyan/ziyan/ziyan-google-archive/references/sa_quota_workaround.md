# SA Quota = 0 Workaround (proven 2026-08-15)

## Symptom
Creating a file/folder via Service Account:
```
googleapiclient.errors.HttpError: 403 ... "The user's Drive storage quota has been exceeded."
storageQuota: {"limit": "0", "usage": "0", ...}
```

## Root cause
The GCP project behind the SA has **0 bytes of Drive storage**. A Service Account's own Drive
inherits the project's storage quota, which is zero on the free tier. SA cannot host files.

## Fix: host in Bos's personal Drive, share to SA
1. In **Bos's** Google Drive, create folder `ZIYAN_ARCHIVE` (and/or the `ARSIP_MASTER` Sheet).
2. Share both with the SA email (e.g. `hggh-568@ziyancorp.iam.gserviceaccount.com`) as **Editor**.
3. SA now writes INTO Bos's Drive — quota belongs to Bos, not the project.
4. Point config at the shared IDs:
   - `GOOGLE_ROOT_FOLDER_ID` = folder id from `drive.google.com/drive/folders/<ID>`
   - `GOOGLE_SPREADSHEET_ID` = id from `docs.google.com/spreadsheets/d/<ID>`

## Verify before building
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
cred = service_account.Credentials.from_service_account_file('credentials.json',
        scopes=['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets'])
d = build('drive','v3', credentials=cred)
for f in [FOLDER_ID, SHEET_ID]:
    r = d.files().get(fileId=f, fields='id,name,capabilities(canEdit)').execute()
    print(r['name'], 'canEdit=', r['capabilities']['canEdit'])  # must be True
```
If `canEdit=False` → sharing not set to Editor yet.

## On-prem auto-create pitfall
`google_workspace.create_folder` works for the SA's OWN drive (folder gets created), but any
subsequent WRITE into it fails with 403 quota. So: do NOT auto-create via SA. Have Bos create
in personal Drive + share. The SA can still create subfolders/files *inside* the shared parent.
