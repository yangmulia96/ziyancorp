#!/usr/bin/env python3
"""
Celine Aurel Distribution Agent - Anti-Duplikasi & 4-Slot Scheduler
Persona: AI Influencer "Celine Aurel" (Fashion / Lifestyle / Shopee Affiliate)

ATURAN DISTRIBUSI BAKU (PERMANEN):
  Celine Aurel -> YouTube Shorts + Instagram + Facebook + Threads
  (TIDAK ke Twitter/X dan TIDAK ke Telegram Channel publik)
"""
import os, sys, json, re, io, tempfile
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from dotenv import load_dotenv

ROOT = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel")
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT))

from distributor import (
    post_facebook, post_instagram, post_threads,
    post_youtube_celine, gen_caption
)
from ziyan_bot.config import Settings as Cfg
from ziyan_bot.google_workspace import GoogleWorkspace

TMP = ROOT / "tmp_assets"
TMP.mkdir(exist_ok=True)


def notify_boss_telegram(message: str) -> None:
    """Kirim notifikasi ke Telegram pribadi Bos."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    allowed_ids = os.environ.get("TELEGRAM_ALLOWED_USER_IDS", "").split(",")
    if not bot_token:
        return
    for uid in allowed_ids:
        uid = uid.strip()
        if uid:
            try:
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": uid, "text": message, "parse_mode": "HTML"},
                    timeout=15
                )
            except Exception:
                pass


def get_pending_queue_items(limit=1):
    """Ambil konten PENDING dari Google Sheets Celine."""
    s = Cfg.from_env()
    gw = GoogleWorkspace(s.google_credentials_file, s.google_token_file,
                         s.google_root_folder_id, s.google_spreadsheet_id)
    res = gw.sheets.spreadsheets().values().get(
        spreadsheetId=s.google_spreadsheet_id,
        range="PRODUCT_MASTER!A2:K"
    ).execute()
    rows = res.get("values", [])
    pending = []

    for idx, r in enumerate(rows):
        if len(r) > 0 and r[0]:
            # Columns: 0:product_id, 1:title, 2:description, 3:shopee, 4:tiktok, 5:other, 6:drive, 7:assets, 8:created, 9:updated, 10:status
            status = r[10] if len(r) > 10 else (r[7] if len(r) > 7 and r[7] in ("POSTED", "PUBLISHED", "READY", "SKIP") else "")
            if status.upper() in ("READY", "PENDING", "NEW") or (status.upper() not in ("POSTED", "PUBLISHED", "SKIP", "COMPLETED") and not str(status).isdigit()):
                pending.append({
                    "row_index": idx + 2,
                    "product_id": r[0],
                    "title": r[1] if len(r) > 1 else "",
                    "description": r[2] if len(r) > 2 else "",
                    "shopee_url": r[3] if len(r) > 3 else "",
                    "tiktok_url": r[4] if len(r) > 4 else "",
                    "drive_url": r[6] if len(r) > 6 else "",
                    "status": status
                })
                if len(pending) >= limit:
                    break
    return pending


def mark_asset_posted(row_index: int, product_id: str) -> None:
    """Tandai POSTED secara permanen di Google Sheets."""
    ts = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S WIB")
    s = Cfg.from_env()
    gw = GoogleWorkspace(s.google_credentials_file, s.google_token_file,
                         s.google_root_folder_id, s.google_spreadsheet_id)
    gw.sheets.spreadsheets().values().update(
        spreadsheetId=s.google_spreadsheet_id,
        range=f"PRODUCT_MASTER!J{row_index}:K{row_index}",
        valueInputOption="RAW",
        body={"values": [[ts, "POSTED"]]}
    ).execute()
    print(f"[OK] Baris {row_index} ({product_id}) ditandai POSTED pada {ts}")


def get_drive_public_url(gw, file_id: str) -> str:
    """Buat link publik untuk file di Google Drive (diperlukan IG)."""
    try:
        gw.drive.permissions().create(
            fileId=file_id,
            body={"role": "reader", "type": "anyone"}
        ).execute()
        meta = gw.drive.files().get(
            fileId=file_id,
            fields="webContentLink"
        ).execute()
        return meta.get("webContentLink", "")
    except Exception as e:
        print(f"[WARN] Gagal buat link publik Drive: {e}")
        return ""


def extract_file_id_from_url(url: str) -> str:
    """Extract Drive file ID or folder ID from URL."""
    if not url:
        return ""
    # Check /file/d/{id} or /folders/{id} or id={id}
    m = re.search(r"(?:/file/d/|/folders/|id=)([a-zA-Z0-9_-]{20,})", url)
    if m:
        return m.group(1)
    return ""


def distribute_to_platforms_celine(item: dict, caption: str, video_path: str = None, public_url: str = None) -> dict:
    """
    DISTRIBUSI RESMI CELINE AUREL:
    1. YouTube Shorts  (via API token_celine.json)
    2. Instagram       (via Meta Graph API)
    3. Facebook Page   (via Meta Graph API)
    4. Threads         (via Threads API)
    """
    results = {}
    fb_token = os.environ.get("FB_PAGE_TOKEN", "")
    fb_page_id = os.environ.get("FB_PAGE_ID", "")
    ig_user_id = os.environ.get("IG_BUSINESS_ID", "")
    threads_token = os.environ.get("THREADS_USER_TOKEN", "")

    yt_title = item["title"]
    yt_title = re.sub(r"dengan harga Rp[0-9.]+", "", yt_title, flags=re.I)
    yt_title = re.sub(r"\. Dapatkan di Shopee sekarang!.*", "", yt_title, flags=re.I)
    yt_title = re.sub(r"http\S+", "", yt_title).strip()
    if not yt_title or len(yt_title) < 3:
        yt_title = "Rekomendasi Outfit & Fashion Wanita Kekinian ✨"

    # 1. YouTube Shorts Celine
    if video_path and os.path.exists(video_path):
        try:
            print("[POSTING] YouTube Celine...")
            results["youtube"] = post_youtube_celine(yt_title, caption, video_path)
        except Exception as e:
            results["youtube"] = {"status": "error", "error": str(e)}
    else:
        results["youtube"] = {"status": "skipped", "reason": "no_video_file"}

    # 2. Instagram
    if public_url and ig_user_id and fb_token:
        try:
            print("[POSTING] Instagram Celine...")
            results["instagram"] = post_instagram(
                caption=caption,
                media_url=public_url,
                ig_user_id=ig_user_id,
                token=fb_token
            )
        except Exception as e:
            results["instagram"] = {"status": "error", "error": str(e)}
    else:
        results["instagram"] = {"status": "skipped", "reason": "missing_meta_auth"}

    # 3. Facebook Page
    if fb_token and fb_page_id:
        try:
            print("[POSTING] Facebook Page Celine...")
            results["facebook"] = post_facebook(
                caption=caption,
                page_id=fb_page_id,
                page_token=fb_token,
                media_url=public_url
            )
        except Exception as e:
            results["facebook"] = {"status": "error", "error": str(e)}
    else:
        results["facebook"] = {"status": "skipped", "reason": "missing_fb_auth"}

    # 4. Threads
    if threads_token and public_url:
        try:
            print("[POSTING] Threads Celine...")
            results["threads"] = post_threads(
                text=caption,
                media_url=public_url,
                token=threads_token
            )
        except Exception as e:
            results["threads"] = {"status": "error", "error": str(e)}
    else:
        results["threads"] = {"status": "skipped", "reason": "missing_threads_auth"}

    return results


def run_distribution_cycle() -> dict:
    """Eksekusi 1 siklus distribusi penuh untuk Celine Aurel."""
    print("=== MEMERIKSA ANTREAN KONTEN CELINE AUREL ===")
    try:
        pending_items = get_pending_queue_items(limit=1)
    except Exception as e:
        print(f"[ERROR] Gagal menghubungi Google Sheets: {e}")
        return {"status": "error", "error": str(e)}

    if not pending_items:
        print("[STOK HABIS] Tidak ada konten PENDING di Google Sheets.")
        return {"status": "empty_queue"}

    item = pending_items[0]
    print(f"[EKSEKUSI] [{item['product_id']}] {item['title'][:40]}")

    s = Cfg.from_env()
    gw = GoogleWorkspace(s.google_credentials_file, s.google_token_file,
                         s.google_root_folder_id, s.google_spreadsheet_id)

    # Cari file ID dari drive_url
    fid = extract_file_id_from_url(item.get("drive_url", ""))
    video_path = None
    public_url = None

    if fid:
        local_file = TMP / f"dist_celine_{item['product_id']}_{fid}.mp4"
        if not local_file.exists():
            print(f"[DOWNLOAD] File dari Drive ID: {fid}...")
            try:
                # Check if fid is folder or file
                meta = gw.drive.files().get(fileId=fid, fields="id,mimeType,name").execute()
                actual_fid = fid
                if meta.get("mimeType") == "application/vnd.google-apps.folder":
                    # Get first file inside folder
                    q = f"'{fid}' in parents and trashed = false"
                    children = gw.drive.files().list(q=q, fields="files(id,name,mimeType)").execute().get("files", [])
                    if children:
                        actual_fid = children[0]["id"]
                
                data = gw.drive.files().get_media(fileId=actual_fid).execute()
                local_file.write_bytes(data)
                print(f"[+] Downloaded: {local_file.name} ({len(data)/(1024*1024):.2f} MB)")
                public_url = get_drive_public_url(gw, actual_fid)
                video_path = str(local_file)
            except Exception as e:
                print(f"[-] Drive file download error: {e}")
        else:
            video_path = str(local_file)
            public_url = get_drive_public_url(gw, fid)

    caption = gen_caption(item, persona="Celine Aurel")
    results = distribute_to_platforms_celine(item, caption, video_path, public_url)

    print(f"\nHasil Distribusi: {json.dumps(results, indent=2, ensure_ascii=False)}")

    # Tandai POSTED di Google Sheets
    mark_asset_posted(item["row_index"], item["product_id"])

    # Laporan ke Bos via Telegram
    yt_url = results.get("youtube", {}).get("url", "-")
    ig_status = results.get("instagram", {}).get("status", "-")
    fb_status = results.get("facebook", {}).get("status", "-")
    th_status = results.get("threads", {}).get("status", "-")

    success_msg = (
        "✅ <b>[KONTEN CELINE BERHASIL TAYANG]</b>\n\n"
        f"👧 <b>Persona:</b> Celine Aurel\n"
        f"📦 <b>Produk:</b> {item['title'][:50]}\n\n"
        f"📺 <b>YouTube:</b> {yt_url}\n"
        f"📸 <b>Instagram:</b> {ig_status}\n"
        f"👍 <b>Facebook:</b> {fb_status}\n"
        f"🧵 <b>Threads:</b> {th_status}\n\n"
        "✨ Status di Google Sheets → <b>POSTED</b>"
    )
    notify_boss_telegram(success_msg)
    return {"status": "success", "results": results}


if __name__ == "__main__":
    run_distribution_cycle()
