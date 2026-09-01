#!/usr/bin/env python3
"""
AbangJal / Arijal Meutuwah Distribution Agent (Self-Managing & Anti-Repeat Engine)

ATURAN DISTRIBUSI BAKU (PERMANEN):
  Arijal Meutuwah -> YouTube Shorts ONLY
  (TIDAK ke Instagram, TIDAK ke Facebook, TIDAK ke Threads, TIDAK ke Twitter/X)

Fungsi:
1. Memeriksa antrean konten PENDING di Google Sheets.
2. Jika ada PENDING -> Download dari Drive, upload ke YouTube Shorts, tandai POSTED.
3. JIKA STOK HABIS -> DILARANG mengulang konten lama. Kirim notifikasi ke Bos.
"""
import os, sys, json, re, io, tempfile
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from dotenv import load_dotenv

ROOT = Path(r"C:\Users\arija\ziyancorp\abangjal_archive_bot")
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT))

from distributor import distribute_to_platforms_arijal, gen_caption
from abangjal_bot.config import Settings as Cfg
from abangjal_bot.google_workspace import GoogleWorkspace
from scheduler_queue import split_product_into_queue_items

TMP = ROOT / "tmp_assets"
TMP.mkdir(exist_ok=True)


def notify_boss_telegram(message: str) -> None:
    """Kirim notifikasi langsung ke chat Telegram Bos."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    allowed_ids = os.environ.get("TELEGRAM_ALLOWED_USER_IDS", "").split(",")
    if not bot_token or not allowed_ids:
        return
    
    for uid in allowed_ids:
        uid = uid.strip()
        if uid:
            try:
                requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                    "chat_id": uid,
                    "text": message,
                    "parse_mode": "HTML"
                }, timeout=15)
            except Exception:
                pass


def get_pending_queue_items(limit=1):
    """Ambil aset konten yang benar-benar berstatus PENDING (belum pernah di-post)."""
    s = Cfg.from_env()
    gw = GoogleWorkspace(s.google_credentials_file, s.google_token_file,
                         s.google_root_folder_id, s.google_spreadsheet_id)
    res = gw.sheets.spreadsheets().values().get(
        spreadsheetId=s.google_spreadsheet_id, range="PRODUCT_MASTER!A2:J").execute()
    rows = res.get("values", [])
    pending = []
    
    for idx, r in enumerate(rows):
        if len(r) > 0 and r[0]:
            status = r[7] if len(r) > 7 else (r[8] if len(r) > 8 else "")
            # Hanya ambil yang berstatus PENDING / READY (bukan POSTED / PUBLISHED)
            if status.upper() not in ("POSTED", "PUBLISHED", "SKIP", "COMPLETED"):
                pending.append({
                    "row_index": idx + 2,
                    "product_id": r[0],
                    "title": r[1] if len(r) > 1 else "",
                    "description": r[2] if len(r) > 2 else "",
                    "shopee_url": r[3] if len(r) > 3 else "",
                    "drive_url": r[4] if len(r) > 4 else "",
                    "media_type": r[5] if len(r) > 5 else "video",
                    "status": status
                })
                if len(pending) >= limit:
                    break
    return pending


def mark_asset_posted(row_index: int, product_id: str, platform_urls: dict = None) -> None:
    """Tandai status POSTED secara permanen di Google Sheets."""
    ts = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S WIB")
    s = Cfg.from_env()
    gw = GoogleWorkspace(s.google_credentials_file, s.google_token_file,
                         s.google_root_folder_id, s.google_spreadsheet_id)
    
    gw.sheets.spreadsheets().values().update(
        spreadsheetId=s.google_spreadsheet_id,
        range=f"PRODUCT_MASTER!H{row_index}:I{row_index}",
        valueInputOption="RAW",
        body={"values": [["POSTED", ts]]}
    ).execute()
    print(f"[OK] Baris {row_index} ({product_id}) status ditandai POSTED permanen pada {ts}")


def run_distribution_cycle() -> dict:
    """Eksekusi 1 siklus distribusi slot waktu."""
    print("=== MEMERIKSA ANTREAN KONTEN ARIJAL MEUTUWAH ===")
    try:
        pending_items = get_pending_queue_items(limit=1)
    except Exception as e:
        print(f"[ERROR] Gagal menghubungi Google Sheets: {e}")
        return {"status": "error", "error": str(e)}
    
    # KONDISI 1: STOK KONTEN HABIS
    if not pending_items:
        print("[STOK HABIS] Tidak ada konten baru berstatus PENDING di antrean.")
        print("[ANTI-REPEAT] Sistem menolak memposting ulang konten lama.")
        alert_msg = (
            "⚠️ <b>[PEMBERITAHUAN STOK KONTEN HABIS]</b>\n\n"
            "Halo Bos! Stok konten untuk <b>Arijal Meutuwah</b> di antrean saat ini sudah <b>KOSONG / HABIS</b>.\n\n"
            "🛡️ <i>Sistem otomatis menahan diri dan TIDAK AKAN mengunggah konten lama.</i>\n\n"
            "📲 Silakan kirimkan foto/video & link Shopee baru ke bot <b>@Abangjal_arspbot</b> agar jadwal slot berikutnya tetap terisi! 🚀"
        )
        notify_boss_telegram(alert_msg)
        return {"status": "empty_queue", "message": "Stok konten habis, alert Telegram telah dikirim ke Bos."}

    # KONDISI 2: ADA KONTEN PENDING
    item = pending_items[0]
    print(f"[EKSEKUSI] Menemukan konten pending: [{item['product_id']}] {item['title'][:40]}")
    
    # 1. Download file dari Drive jika diperlukan
    video_path = None
    if item.get("drive_url") and "http" in item.get("drive_url"):
        # Ambil file_id
        m = re.search(r"/d/([a-zA-Z0-9_-]+)", item["drive_url"]) or re.search(r"id=([a-zA-Z0-9_-]+)", item["drive_url"])
        if m:
            fid = m.group(1)
            s = Cfg.from_env()
            gw = GoogleWorkspace(s.google_credentials_file, s.google_token_file,
                                 s.google_root_folder_id, s.google_spreadsheet_id)
            local_file = TMP / f"dist_{item['product_id']}_{fid}.mp4"
            if not local_file.exists():
                print(f"Downloading aset dari Google Drive (ID: {fid})...")
                data = gw.drive.files().get_media(fileId=fid).execute()
                local_file.write_bytes(data)
            video_path = str(local_file)
            
    # 2. Generate Caption
    caption = gen_caption(item, persona="Arijal Meutuwah")

    # 3. DISTRIBUSI: Arijal Meutuwah -> YouTube Shorts ONLY
    results = distribute_to_platforms_arijal(item, caption, targets=["youtube"], video_path=video_path)
    print(f"Hasil Distribusi: {json.dumps(results, indent=2)}")
    
    # 4. Tandai POSTED permanen
    mark_asset_posted(item["row_index"], item["product_id"], results)
    
    # 5. Kirim konfirmasi sukses ke Telegram Bos
    yt_url = results.get("youtube", {}).get("url", "-")
    yt_status = results.get("youtube", {}).get("status", "-")
    success_msg = (
        "✅ <b>[KONTEN ARIJAL BERHASIL TAYANG]</b>\n\n"
        f"👑 <b>Persona:</b> Arijal Meutuwah\n"
        f"📦 <b>Produk:</b> {item['title'][:50]}\n"
        f"📺 <b>YouTube Shorts:</b> {yt_url if yt_url != '-' else yt_status}\n\n"
        "✨ Status antrean di Google Sheets telah diubah menjadi <b>POSTED</b>."
    )
    notify_boss_telegram(success_msg)
    return {"status": "success", "results": results}


if __name__ == "__main__":
    res = run_distribution_cycle()
    print(f"\nStatus Siklus: {res}")
