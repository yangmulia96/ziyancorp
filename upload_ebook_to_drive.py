# -*- coding: utf-8 -*-
import os, sys, json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(r"C:\Users\arija\ziyancorp\abangjal_archive_bot")
CLIENT_SECRET = ROOT / "client_secret.json"
TOKEN_PATH = ROOT / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive"
]

def get_drive_service():
    creds = None
    if TOKEN_PATH.exists():
        try:
            with open(TOKEN_PATH, 'r') as f:
                info = json.load(f)
            creds = Credentials.from_authorized_user_info(info, SCOPES)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(TOKEN_PATH, 'w') as f:
                    f.write(creds.to_json())
        except Exception as e:
            print("Token expired/invalid, starting re-auth flow...")
            creds = None

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CLIENT_SECRET),
            SCOPES
        )
        print("\n[!] BROWSER AKAN TERBUKA UNTUK LOGIN GOOGLE DRIVE...")
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as f:
            f.write(creds.to_json())
        # sync to celine as well
        celine_token = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel\token.json")
        with open(celine_token, 'w') as f:
            f.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def main():
    service = get_drive_service()
    print("\n[1/3] Memeriksa / Membuat Folder Khusus di Google Drive...")
    
    folder_name = "📂 Produk Digital & E-Book Ziyan"
    q = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    res = service.files().list(q=q, spaces='drive', fields='files(id, name)').execute()
    files = res.get('files', [])

    if files:
        folder_id = files[0]['id']
        print(f"-> Folder sudah ada! ID: {folder_id}")
    else:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')
        print(f"-> Folder baru berhasil dibuat! ID: {folder_id}")

    # Files to upload
    pdf_path = r"C:\Users\arija\Downloads\Panduan_Ngonten_Tanpa_Wajah.pdf"
    html_path = r"C:\Users\arija\ziyancorp\ebook_ai_creator\index.html"

    items = [
        (pdf_path, "Panduan_Ngonten_Tanpa_Wajah.pdf", "application/pdf"),
        (html_path, "index_ebook_interaktif.html", "text/html")
    ]

    print("\n[2/3] Mengunggah file ke Google Drive...")
    for path, name, mime in items:
        if os.path.exists(path):
            file_metadata = {
                'name': name,
                'parents': [folder_id]
            }
            media = MediaFileUpload(path, mimetype=mime, resumable=True)
            f = service.files().create(body=file_metadata, media_body=media, fields='id, name, webViewLink').execute()
            print(f"✅ Berhasil Upload: {name} (ID: {f.get('id')})")
            print(f"   Link Drive: {f.get('webViewLink')}")
        else:
            print(f"⚠️ File tidak ditemukan: {path}")

    print("\n[3/3] SELESAI! Folder dan E-Book sudah tersimpan rapi di Google Drive!")

if __name__ == '__main__':
    main()