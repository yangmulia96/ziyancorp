#!/usr/bin/env python3
"""
Celine Aurel — Auto-Ingest Bridge
Connects Telegram quick_archive.db (inbox) -> Google Drive & Google Sheets (PRODUCT_MASTER)
Transforms incoming files into READY items for distribute_agent.py
"""
import os
import sys
import json
import sqlite3
import requests
import datetime
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel")
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT))

from ziyan_bot.config import Settings
from ziyan_bot.google_workspace import GoogleWorkspace

DB_PATH = ROOT / "quick_archive.db"
MAIN_DB_PATH = ROOT / "archive.db"
TMP_DIR = ROOT / "tmp_assets"
TMP_DIR.mkdir(parents=True, exist_ok=True)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def download_telegram_file(file_id: str, dest_path: Path) -> bool:
    """Download binary file from Telegram API via file_id."""
    if not BOT_TOKEN:
        print("[-] Error: TELEGRAM_BOT_TOKEN missing")
        return False
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        r = requests.get(url, timeout=30)
        res = r.json()
        if not res.get("ok"):
            print(f"[-] Telegram getFile error: {res}")
            return False
        file_path = res["result"]["file_path"]
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        
        r_file = requests.get(download_url, timeout=120, stream=True)
        if r_file.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in r_file.iter_content(chunk_size=1024*1024):
                    f.write(chunk)
            print(f"[+] Downloaded: {dest_path.name} ({dest_path.stat().st_size / (1024*1024):.2f} MB)")
            return True
        else:
            print(f"[-] Failed to download binary: HTTP {r_file.status_code}")
            return False
    except Exception as e:
        print(f"[-] Exception downloading file: {e}")
        return False

def parse_caption_links(caption: str):
    """Extract product title and Shopee/TikTok links from text."""
    import re
    shopee_match = re.search(r"https?://(?:s\.shopee\.co\.id|shopee\.co\.id)/\S+", caption)
    tiktok_match = re.search(r"https?://(?:vt\.tiktok\.com|tiktok\.com)/\S+", caption)
    
    shopee_url = shopee_match.group(0) if shopee_match else ""
    tiktok_url = tiktok_match.group(0) if tiktok_match else ""
    
    clean_text = caption
    if shopee_url:
        clean_text = clean_text.replace(shopee_url, "").strip()
    if tiktok_url:
        clean_text = clean_text.replace(tiktok_url, "").strip()
        
    title = clean_text.split("\n")[0].strip() if clean_text else "Produk Celine Aurel"
    desc = clean_text if clean_text else "Fashion & Lifestyle Produk Rekomendasi Celine Aurel"
    return title[:120], desc, shopee_url, tiktok_url

def process_inbox_items():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inbox WHERE status='NEW' ORDER BY id ASC")
    items = cursor.fetchall()
    
    if not items:
        conn.close()
        return 0

    print(f"[+] Found {len(items)} NEW items in Celine Inbox. Initializing Google Workspace...")
    settings = Settings.from_env()
    gw = GoogleWorkspace(settings.google_credentials_file, settings.google_token_file,
                         settings.google_root_folder_id, settings.google_spreadsheet_id)

    processed_count = 0

    for item in items:
        item_id = item["id"]
        file_id = item["file_id"]
        file_type = item["file_type"]
        file_name = item["file_name"] or f"media_{item_id}.mp4"
        caption = item["caption"] or item["raw_text"] or ""
        
        print(f"\n--- Processing Inbox Item #{item_id}: {file_name} ---")
        title, desc, shopee_url, tiktok_url = parse_caption_links(caption)
        
        # 1. Generate Product ID
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        product_id = f"CELINE_{now_str}_{item_id}"
        
        # 2. Download File if exists
        local_file = TMP_DIR / f"{product_id}_{file_name}"
        drive_file_id = ""
        drive_file_url = ""
        drive_folder_url = ""
        
        if file_id:
            download_ok = download_telegram_file(file_id, local_file)
            if download_ok and local_file.exists():
                # 3. Create Product Folder on Google Drive
                try:
                    folder_name = f"{product_id} - {title[:30]}"
                    folder = gw.find_or_create_folder(folder_name, settings.google_root_folder_id)
                    drive_folder_id = folder["id"]
                    drive_folder_url = folder["webViewLink"]
                    
                    # 4. Upload File to Google Drive
                    up_res = gw.upload_file(local_file, drive_folder_id)
                    drive_file_id = up_res["id"]
                    drive_file_url = up_res["webViewLink"]
                    print(f"[+] Uploaded to Drive: {drive_file_url}")
                except Exception as e:
                    print(f"[-] Drive upload error: {e}")
                finally:
                    if local_file.exists():
                        try:
                            local_file.unlink()
                        except:
                            pass
        
        # 5. Insert Row to Google Sheets PRODUCT_MASTER
        try:
            now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row_data = [
                product_id,
                title,
                desc,
                shopee_url,
                tiktok_url,
                "",  # other_links
                drive_folder_url or drive_file_url,
                1 if file_id else 0,  # asset_count
                now_iso,  # created_at
                now_iso,  # updated_at
                "READY"   # status
            ]
            gw.append_product(row_data)
            print(f"[+] Appended to Google Sheets PRODUCT_MASTER as READY (row for {product_id})")
        except Exception as e:
            print(f"[-] Sheets append error: {e}")
            
        # 6. Mark Inbox item as PROCESSED
        cursor.execute("UPDATE inbox SET status='PROCESSED' WHERE id=?", (item_id,))
        conn.commit()
        processed_count += 1
        print(f"[+] Marked Inbox #{item_id} as PROCESSED")
        
    conn.close()
    return processed_count

if __name__ == "__main__":
    count = process_inbox_items()
    print(f"\n[+] Ingest completed. Total processed: {count}")
