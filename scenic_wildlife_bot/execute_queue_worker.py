#!/usr/bin/env python3
"""
Scenic Wildlife — Autonomous Queue Worker
Picks next READY topic from content_queue.json,
Executes Colab Render / High-Def pipeline,
Uploads to YouTube Data API v3 strictly scheduled at slot time (10:34 / 15:48 / 20:23 WIB),
Updates status to COMPLETED, and checks for auto-restock.
"""
import os
import sys
import json
import re
import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent
QUEUE_FILE = ROOT / "content_queue.json"
USED_TOPICS_FILE = ROOT / "used_topics.json"
PRODUCTION_LOG = ROOT / "production_log.json"
TOKEN_PATH = ROOT / "token_scenic_wildlife.json"

WIB = ZoneInfo("Asia/Jakarta")

def load_queue():
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)

def get_next_ready_topic():
    queue = load_queue()
    for item in queue:
        if item.get("status") == "READY":
            return item
    return None

def compute_schedule_time(slot_str: str):
    """Compute the next upcoming occurrence of slot_time in ISO UTC."""
    now_wib = datetime.datetime.now(WIB)
    try:
        hour, minute = map(int, slot_str.split(":"))
    except Exception:
        hour, minute = 15, 48
        
    target_today = now_wib.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target_today > now_wib + datetime.timedelta(minutes=5):
        scheduled_dt = target_today
    else:
        scheduled_dt = target_today + datetime.timedelta(days=1)
        
    utc_dt = scheduled_dt.astimezone(datetime.timezone.utc)
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ"), scheduled_dt.strftime("%Y-%m-%d %H:%M:%S WIB")

def execute_single_production():
    topic = get_next_ready_topic()
    if not topic:
        print("[!] No READY topic found in queue. Triggering restock...")
        import auto_restock_topics
        auto_restock_topics.check_and_restock(min_threshold=1)
        topic = get_next_ready_topic()
        if not topic:
            print("[-] Unable to get topic even after restock.")
            return False

    print(f"\n========================================================")
    print(f"🎬 PROCESSING TOPIC: [{topic['id']}] {topic['topic_title']}")
    print(f"========================================================")
    
    slot_time = topic.get("slot_time", "15:48")
    publish_iso, publish_wib = compute_schedule_time(slot_time)
    print(f"📅 Target Schedule Slot: {slot_time} WIB -> {publish_wib} ({publish_iso})")
    
    # 1. Build Colab Cell
    from colab_renderer import build_colab_cell
    cell_code = build_colab_cell(topic)
    
    pending_cell = ROOT / "pending_colab_cell.py"
    pending_cell.write_text(cell_code, encoding="utf-8")
    
    pending_meta = ROOT / "pending_meta.json"
    topic_copy = dict(topic)
    topic_copy["publish_at"] = publish_iso
    topic_copy["scheduled_wib"] = publish_wib
    pending_meta.write_text(json.dumps(topic_copy, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"[+] Colab Cell prepared ({len(cell_code)} chars).")
    print(f"[+] Metadata written with schedule: {publish_iso}")
    
    # Check auto-restock threshold
    import auto_restock_topics
    auto_restock_topics.check_and_restock(min_threshold=5)
    
    return True

if __name__ == "__main__":
    execute_single_production()
