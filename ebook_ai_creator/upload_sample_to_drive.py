import os
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

token_path = r'C:\Users\arija\ziyancorp\abangjal_archive_bot\token.json'
creds = Credentials.from_authorized_user_file(token_path)
service = build('drive', 'v3', credentials=creds)

# Find ZIYANCORP_AI_FACTORY folder ID
res = service.files().list(q="name='ZIYANCORP_AI_FACTORY' and mimeType='application/vnd.google-apps.folder' and trashed=false", fields='files(id, name)').execute()
folders = res.get('files', [])

if not folders:
    print("Folder ZIYANCORP_AI_FACTORY not found.")
    sys.exit(1)

folder_id = folders[0]['id']
print(f"Target Folder: ZIYANCORP_AI_FACTORY ({folder_id})")

file_path = r'C:\Users\arija\ziyancorp\ebook_ai_creator\Sample_Illustrated_Ebook.pdf'
file_name = '00_SAMPLE_EBOOK_BERILUSTRASI_3D.pdf'

media = MediaFileUpload(file_path, mimetype='application/pdf')
file_metadata = {
    'name': file_name,
    'parents': [folder_id]
}

uploaded = service.files().create(body=file_metadata, media_body=media, fields='id, name, webViewLink').execute()
print(f"🎉 SUKSES UPLOAD KE GOOGLE DRIVE!")
print(f"File Name : {uploaded.get('name')}")
print(f"File ID   : {uploaded.get('id')}")
print(f"Link View : {uploaded.get('webViewLink')}")
