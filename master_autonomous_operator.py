"""
ZIYAN CORP - MASTER AUTONOMOUS OPERATOR
Operator Tunggal & Sentral Seluruh Pipeline Otomasi:
1. Pagi Hari: Produksi 3 Shorts 4K Wildlife & Penjadwalan Prime Time (10:34, 15:48, 20:23 WIB).
2. Siang/Malam: Monitoring & Eksekusi Distribusi Konten Affiliate (YouTube Shorts Celine & Abangjal).
3. Auto-Audit & Logging Database.
"""

import sys
import os
import time
import datetime
import subprocess
import sqlite3
import json
import logging
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"C:\Users\arija\ziyancorp")
LOG_FILE = ROOT_DIR / "master_operator.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("MasterOperator")

def get_wib_now():
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)

def run_wildlife_morning_production():
    """Memproduksi 3 Shorts Satwa 4K dan menjadwalkannya di slot prime time."""
    logger.info("=== [ROUTINE 1] MEMULAI PRODUKSI 3 VIDEO SHORTS SATWA 4K ===")
    wildlife_dir = ROOT_DIR / "scenic_wildlife_bot"
    if not wildlife_dir.exists():
        logger.error(f"Direktori {wildlife_dir} tidak ditemukan.")
        return False

    script = wildlife_dir / "run_agent.py"
    try:
        # Jalankan cycle produksi satwa
        res = subprocess.run([sys.executable, str(script)], cwd=str(wildlife_dir), capture_output=True, text=True, timeout=300)
        logger.info(f"Status Produksi Satwa 4K: ExitCode={res.returncode}")
        if res.stdout:
            logger.info(f"Output: {res.stdout[-400:]}")
        return True
    except Exception as e:
        logger.error(f"Gagal memproduksi video satwa: {e}")
        return False

def run_affiliate_distribution():
    """Memindai antrean produk affiliate yang belum diposting dan mengeksekusinya."""
    logger.info("=== [ROUTINE 2] MEMERIKSA & MENGEKSEKUSI DISTRIBUSI KONTEN AFFILIATE ===")
    celine_dir = ROOT_DIR / "arsip_celine_aurel"
    abangjal_dir = ROOT_DIR / "abangjal_archive_bot"

    # 1. Jalankan Distributor Celine Aurel
    if celine_dir.exists():
        try:
            logger.info("Mengeksekusi distributor Celine Aurel...")
            res = subprocess.run([sys.executable, "distribute_agent.py"], cwd=str(celine_dir), capture_output=True, text=True, timeout=180)
            logger.info(f"Celine Distributor: {res.stdout[-300:] if res.stdout else 'Selesai tanpa antrean baru.'}")
        except Exception as e:
            logger.error(f"Error Celine distributor: {e}")

    # 2. Jalankan Distributor Abangjal
    if abangjal_dir.exists():
        try:
            logger.info("Mengeksekusi distributor Abangjal Meutuwah...")
            res = subprocess.run([sys.executable, "distribute_agent.py"], cwd=str(abangjal_dir), capture_output=True, text=True, timeout=180)
            logger.info(f"Abangjal Distributor: {res.stdout[-300:] if res.stdout else 'Selesai tanpa antrean baru.'}")
        except Exception as e:
            logger.error(f"Error Abangjal distributor: {e}")

def master_audit_and_execute():
    wib = get_wib_now()
    logger.info(f"=== MASTER OPERATOR AUDIT DIMULAI: {wib.strftime('%Y-%m-%d %H:%M:%S WIB')} ===")
    
    # 1. Eksekusi Distribusi Konten Menunggu
    run_affiliate_distribution()
    
    # 2. Jika pagi hari (antara 05:00 - 09:00 WIB), jalankan produksi 3 video satwa
    if 5 <= wib.hour <= 9:
        logger.info("Waktu Pagi Terdeteksi: Menjalankan produksi 3 video Shorts Satwa 4K...")
        run_wildlife_morning_production()
        
    logger.info("=== MASTER OPERATOR AUDIT SELESAI DENGAN SUKSES ===")

if __name__ == "__main__":
    master_audit_and_execute()
