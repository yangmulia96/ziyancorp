#!/usr/bin/env python3
"""
ZiyanCorp — Unified Autonomous Ecosystem Supervisor
Oversees and coordinates:
1. Telegram Ingest QuickBots (Abangjal & Celine)
2. Auto-Ingest Bridges (quick_archive.db -> Google Drive/Sheets)
3. Social Media Distribution Agents (YouTube, IG, FB, Threads)
4. 4K Scenic Wildlife Queue Engine & Auto-Restock Watchdog
Runs 24/7 in background with zero human intervention required.
"""
import os
import sys
import time
import subprocess
import logging
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
LOG_FILE = ROOT / "ecosystem_supervisor.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger("Supervisor")

CELINE_DIR = ROOT / "arsip_celine_aurel"
ABANGJAL_DIR = ROOT / "abangjal_archive_bot"
SCENIC_DIR = ROOT / "scenic_wildlife_bot"

processes = {}

def start_bot(name: str, script_path: Path, cwd: Path):
    """Start or restart a background bot process."""
    proc = processes.get(name)
    if proc is None or proc.poll() is not None:
        try:
            p = subprocess.Popen(
                [sys.executable, str(script_path)],
                cwd=str(cwd),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            processes[name] = p
            log.info(f"[+] Started daemon process: {name} (PID: {p.pid})")
        except Exception as e:
            log.error(f"[-] Failed to start {name}: {e}")

def run_task(name: str, script_path: Path, cwd: Path, timeout: int = 180):
    """Run a periodic synchronization task."""
    try:
        res = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if res.returncode == 0:
            log.info(f"[OK] Task {name} finished successfully.")
        else:
            log.warning(f"[WARN] Task {name} exited with code {res.returncode}: {res.stderr[:200]}")
    except subprocess.TimeoutExpired:
        log.error(f"[TIMEOUT] Task {name} timed out after {timeout}s.")
    except Exception as e:
        log.error(f"[ERR] Task {name} execution error: {e}")

def main():
    log.info("=" * 60)
    log.info("🚀 ZIYANCORP AUTONOMOUS ECOSYSTEM SUPERVISOR STARTED")
    log.info("=" * 60)

    last_ingest_check = 0
    # Configuration Flags: Set to True to enable
    ENABLE_CELINE_BOT = False
    ENABLE_ABANGJAL_BOT = False

    while True:
        now = time.time()

        # 1. Maintain Telegram Quick Bots (DISABLED by user request)
        if ENABLE_CELINE_BOT:
            start_bot("CelineQuickBot", CELINE_DIR / "quick_bot.py", CELINE_DIR)
        if ENABLE_ABANGJAL_BOT:
            start_bot("AbangjalQuickBot", ABANGJAL_DIR / "quick_bot.py", ABANGJAL_DIR)

        # 2. Check & Run Auto-Ingest Bridge (Every 30 seconds)
        if now - last_ingest_check >= 30:
            if ENABLE_CELINE_BOT:
                run_task("CelineAutoIngest", CELINE_DIR / "auto_ingest_bridge.py", CELINE_DIR)
            if ENABLE_ABANGJAL_BOT:
                run_task("AbangjalAutoIngest", ABANGJAL_DIR / "auto_ingest_bridge.py", ABANGJAL_DIR)
            last_ingest_check = now

        # 3. Check & Run Distribution Agents (Every 5 minutes)
        if now - last_distribute_check >= 300:
            if ENABLE_CELINE_BOT:
                run_task("CelineDistributor", CELINE_DIR / "distribute_agent.py", CELINE_DIR)
            if ENABLE_ABANGJAL_BOT:
                run_task("AbangjalDistributor", ABANGJAL_DIR / "distribute_agent.py", ABANGJAL_DIR)
            last_distribute_check = now

        # 4. Check Scenic Wildlife Auto-Restock (Every 30 minutes)
        if now - last_restock_check >= 1800:
            log.info("🐾 Checking Scenic Wildlife Content Queue...")
            run_task("ScenicRestock", SCENIC_DIR / "auto_restock_topics.py", SCENIC_DIR)
            last_restock_check = now

        time.sleep(10)

if __name__ == "__main__":
    main()
