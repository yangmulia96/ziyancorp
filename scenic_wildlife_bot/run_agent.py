"""
Master Runner - dipanggil oleh Windows Task Scheduler atau startup
Menjalankan full production cycle: Topic -> Colab Render -> YouTube Upload
"""
import sys
import os
import json
import time
import re
import datetime
import subprocess
import shutil
import logging
import random
from pathlib import Path

ROOT = Path(__file__).parent
LOG_FILE = ROOT / "production_log.json"

# Windows safe logging - UTF8
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ROOT / "agent.log", encoding="utf-8"),
        logging.StreamHandler(open(os.devnull, 'w'))  # Suppress console emoji errors
    ]
)
log = logging.getLogger("ScenicAgent")

UPLOAD_SLOTS_WIB = [
    (10, 34, 10),   # Slot 1: ~10:24 - 10:44 WIB (Siang)
    (15, 48, 10),   # Slot 2: ~15:38 - 15:58 WIB (Sore)
    (20, 23, 10),   # Slot 3: ~20:13 - 20:33 WIB (Malam, sebelum 22:00)
]


def load_log():
    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"total_videos": 0, "uploads": []}


def save_log(data):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_wib_now():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=7)


def seconds_until_next_slot():
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
        for day_offset in [0, 1]:
            try:
                target = now.replace(hour=target_hour % 24, minute=target_min % 60, second=0, microsecond=0)
                target += datetime.timedelta(days=day_offset)
                if target > now + datetime.timedelta(minutes=2):
                    diff_seconds = (target - now).total_seconds()
                    candidates.append((diff_seconds, target))
            except Exception:
                pass
    candidates.sort(key=lambda x: x[0])
    if candidates:
        return candidates[0]
    return (3600, now + datetime.timedelta(hours=1))


def generate_topic():
    """Call topic engine and return parsed data."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "topic_engine.py")],
        capture_output=True, timeout=180, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        log.error(f"Topic engine stderr: {result.stderr[-500:]}")
        return None
    raw = result.stdout.strip()
    return json.loads(raw)


def run_colab_production(data: dict) -> bool:
    """Build Colab cell and inject via MCP."""
    try:
        from colab_renderer import build_colab_cell
        cell_code = build_colab_cell(data)
        cell_file = ROOT / "pending_colab_cell.py"
        cell_file.write_text(cell_code, encoding="utf-8")
        log.info(f"Colab cell written ({len(cell_code)} chars). Waiting for Antigravity MCP to process...")
        
        # Mark as pending for Antigravity to pick up and inject
        pending_meta = ROOT / "pending_meta.json"
        pending_meta.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception as e:
        log.error(f"Colab build error: {e}")
        return False


def record_upload(data: dict, safe_name: str):
    production_log = load_log()
    production_log["total_videos"] += 1
    production_log["uploads"].append({
        "timestamp": get_wib_now().isoformat(),
        "topic": data["topic_title"],
        "youtube_title": data["youtube_title"],
        "safe_name": safe_name,
        "status": "production_queued"
    })
    save_log(production_log)

    # Archive used topic
    used_path = ROOT / "used_topics.json"
    used = json.loads(used_path.read_text(encoding="utf-8")) if used_path.exists() else []
    used.append(data["topic_title"])
    used_path.write_text(json.dumps(used, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    log.info("ScenicWildlifeProducer AGENT STARTED")
    log.info(f"Channel: @4kscenicwildlife | Start: {get_wib_now().strftime('%Y-%m-%d %H:%M:%S')} WIB")

    while True:
        wait_secs, next_time = seconds_until_next_slot()
        log.info(f"Next slot: {next_time.strftime('%Y-%m-%d %H:%M:%S')} WIB | Sleeping {wait_secs/3600:.2f}h")

        # Sleep in 60-second chunks
        elapsed = 0
        while elapsed < wait_secs:
            chunk = min(60, wait_secs - elapsed)
            time.sleep(chunk)
            elapsed += chunk

        log.info("SLOT TIME - Starting production cycle...")

        try:
            data = generate_topic()
            if not data:
                log.error("Topic generation failed. Skipping slot.")
                time.sleep(120)
                continue

            log.info(f"Topic: {data['topic_title']}")
            safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", data["topic_title"])[:40]

            ok = run_colab_production(data)
            if ok:
                record_upload(data, safe_name)
                total = load_log()["total_videos"]
                log.info(f"Cycle complete! Total queued: {total} videos")
            else:
                log.warning("Colab production queuing failed.")

        except Exception as ex:
            log.error(f"Cycle error: {ex}")

        time.sleep(120)  # Cooldown before next check


if __name__ == "__main__":
    main()
