"""
Master Scheduler - ScenicWildlifeProducer Agent
Runs 3x/day with organic time jitter for @4kscenicwildlife
Schedule (WIB): ~21:23, ~02:47, ~07:19
"""
import os
import sys
import json
import time
import random
import shutil
import logging
import datetime
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
LOG_FILE = ROOT / "production_log.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ROOT / "agent.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger("ScenicWildlifeAgent")


# Organic time slots (WIB = UTC+7)
# Represented as (hour, minute_base, jitter_minutes)
UPLOAD_SLOTS_WIB = [
    (10, 34, 10),   # Slot 1: ~10:24 - 10:44 WIB (Siang)
    (15, 48, 10),   # Slot 2: ~15:38 - 15:58 WIB (Sore)
    (20, 23, 10),   # Slot 3: ~20:13 - 20:33 WIB (Malam, sebelum 22:00)
]


def load_log():
    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"total_videos": 0, "total_views_estimate": 0, "uploads": []}


def save_log(data):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_wib_now():
    utc_now = datetime.datetime.utcnow()
    wib = utc_now + datetime.timedelta(hours=7)
    return wib


def seconds_until_next_slot():
    """Calculate seconds until the next upload slot."""
    now = get_wib_now()
    
    candidates = []
    for (h, m_base, jitter) in UPLOAD_SLOTS_WIB:
        jitter_val = random.randint(-jitter, jitter)
        target_min = m_base + jitter_val
        target_hour = h
        if target_min < 0:
            target_min += 60
            target_hour -= 1
        elif target_min >= 60:
            target_min -= 60
            target_hour += 1
        
        # Build target datetime for today and tomorrow
        for day_offset in [0, 1]:
            target = now.replace(hour=target_hour % 24, minute=target_min, second=0, microsecond=0)
            target += datetime.timedelta(days=day_offset)
            if target > now:
                diff_seconds = (target - now).total_seconds()
                candidates.append((diff_seconds, target))
    
    candidates.sort(key=lambda x: x[0])
    if candidates:
        return candidates[0]
    return (3600, now + datetime.timedelta(hours=1))


def run_production_cycle():
    """Full cycle: Research -> Render on Colab -> Upload to YouTube."""
    log.info("=" * 60)
    log.info("STARTING PRODUCTION CYCLE")
    log.info("=" * 60)
    
    # Step 1: Generate topic and script
    log.info("STEP 1: Generating viral topic and script via Gemini AI...")
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / "topic_engine.py")],
            capture_output=True, text=True, timeout=120, encoding="utf-8"
        )
        if result.returncode != 0:
            log.error(f"Topic engine failed: {result.stderr}")
            return False
        
        data = json.loads(result.stdout.strip())
        log.info(f"Topic selected: {data['topic_title']}")
    except Exception as e:
        log.error(f"Topic generation error: {e}")
        return False

    # Save data to temp file for Colab to read
    data_file = ROOT / "current_production.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Step 2: Execute Colab production
    log.info("STEP 2: Launching Colab production (render + subtitle + audio mix)...")
    try:
        from colab_renderer import build_colab_cell
        colab_cell_code = build_colab_cell(data)
        
        # Use colab-mcp to inject and run the cell
        # This is called via Antigravity's colab MCP tool
        log.info("Colab cell built. Flagging for MCP execution...")
        
        # Write cell to temp file
        cell_file = ROOT / "pending_colab_cell.py"
        with open(cell_file, "w", encoding="utf-8") as f:
            f.write(colab_cell_code)
        log.info(f"Colab cell written to {cell_file}")
        log.info("Colab rendering in progress (estimated 3-5 min)...")
        
        # Wait for completion signal
        time.sleep(300)  # 5 min buffer for Colab rendering
        
    except Exception as e:
        log.error(f"Colab render error: {e}")
        return False

    # Step 3: Log success
    import re
    safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", data["topic_title"])[:40]
    
    production_log = load_log()
    production_log["total_videos"] += 1
    production_log["uploads"].append({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "topic": data["topic_title"],
        "youtube_title": data["youtube_title"],
        "safe_name": safe_name,
        "status": "queued_for_upload"
    })
    save_log(production_log)
    
    # Save used topic to archive
    used_path = ROOT / "used_topics.json"
    used = []
    if used_path.exists():
        with open(used_path, "r", encoding="utf-8") as f:
            used = json.load(f)
    used.append(data["topic_title"])
    with open(used_path, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)
    
    log.info(f"CYCLE COMPLETE. Video #{production_log['total_videos']} queued.")
    return True


def main():
    log.info("ScenicWildlifeProducer Agent STARTED")
    log.info(f"Channel: @4kscenicwildlife")
    log.info(f"Schedule: 3 videos/day with organic jitter")
    log.info(f"Start time (WIB): {get_wib_now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    cycle_count = 0
    
    while True:
        wait_seconds, next_slot_time = seconds_until_next_slot()
        
        log.info(f"Next upload slot: {next_slot_time.strftime('%Y-%m-%d %H:%M:%S')} WIB")
        log.info(f"Sleeping for {wait_seconds/3600:.2f} hours ({int(wait_seconds)} seconds)...")
        
        # Sleep in chunks to avoid OS sleep issues
        sleep_chunk = 60  # check every minute
        elapsed = 0
        while elapsed < wait_seconds:
            chunk = min(sleep_chunk, wait_seconds - elapsed)
            time.sleep(chunk)
            elapsed += chunk
        
        log.info("WAKE UP - Slot time reached! Starting production...")
        cycle_count += 1
        
        try:
            success = run_production_cycle()
            if success:
                log.info(f"Cycle #{cycle_count} completed successfully.")
            else:
                log.warning(f"Cycle #{cycle_count} failed. Will retry next slot.")
        except Exception as e:
            log.error(f"Unexpected error in cycle #{cycle_count}: {e}")
        
        # Safety cooldown to avoid double-firing
        time.sleep(120)


if __name__ == "__main__":
    main()
