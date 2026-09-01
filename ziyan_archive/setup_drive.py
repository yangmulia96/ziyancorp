#!/usr/bin/env python3
"""Setup ZIYAN_ARCHIVE: buat folder + sheet via API, grant SA akses penuh, test archive."""
import os, json, datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

KEY = r'C:/Users/arija/ziyancorp/credentials/sa_key.json'
SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/spreadsheets']

cred = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
drive = build('drive', 'v3', credentials=cred)
sheets = build('sheets', 'v4', credentials=cred)
SA_EMAIL = cred.service_account_email

def grant(writer, file_id):
    drive.permissions().create(
        fileId=file_id,
        body={'type': 'user', 'role': 'writer', 'emailAddress': SA_EMAIL},
        fields='id').execute()

# 1. Folder ZIYAN_ARCHIVE
meta = {'name': 'ZIYAN_ARCHIVE', 'mimeType': 'application/vnd.google-apps.folder'}
folder = drive.files().create(body=meta, fields='id,name,webViewLink').execute()
grant(drive, folder['id'])
print('FOLDER:', folder['name'], folder['id'], folder.get('webViewLink'))

# 2. Sheet ARSIP_MASTER di dalam folder
sheet_meta = {'name': 'ARSIP_MASTER', 'parents': [folder['id']],
              'mimeType': 'application/vnd.google-apps.spreadsheet'}
sheet = drive.files().create(body=sheet_meta, fields='id,name,webViewLink').execute()
grant(drive, sheet['id'])
print('SHEET:', sheet['name'], sheet['id'], sheet.get('webViewLink'))

# 3. Buat header + 1 contoh row di sheet
header = ['content_id','title','platform','drive_url','shopee','tiktok','tokopedia','amazon','other','created','status']
example = ['ZA-20260814-001','CONTOH: Review Keyboard RGB','shopee',
           'https://drive.google.com/drive/folders/'+folder['id'],
           'https://s.shopee.co.id/contoh','https://vt.tiktok.com/contoh','','','',
           datetime.datetime.now().isoformat(),'ARCHIVED']
sheets.spreadsheets().values().update(
    spreadsheetId=sheet['id'], range='A1',
    valueInputOption='USER_ENTERED',
    body={'values': [header, example]}).execute()
print('SHEET seeded: header + 1 example row')

# 4. Simpan config
cfg = {
    'drive_folder_id': folder['id'],
    'sheet_id': sheet['id'],
    'sa_key_path': KEY,
    'scopes': SCOPES
}
os.makedirs(r'C:/Users/arija/ziyancorp/ziyan_archive/config', exist_ok=True)
with open(r'C:/Users/arija/ziyancorp/ziyan_archive/config/archive_config.json','w') as f:
    json.dump(cfg, f, indent=2)
print('CONFIG saved ->', r'C:/Users/arija/ziyancorp/ziyan_archive/config/archive_config.json')
print(json.dumps(cfg, indent=2))
