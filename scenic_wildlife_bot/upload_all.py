#!/usr/bin/env python3
"""
Upload 3 video ke YouTube dan schedule sesuai slot waktu
Slot hari ini: 15:48 WIB, 20:23 WIB
Slot besok: 10:34 WIB
"""
import subprocess
import sys
import json
import os
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")
OUTPUT = ROOT / "output_videos"
TOKEN = ROOT / "token_scenic_wildlife.json"

print("=" * 70)
print("UPLOAD 3 VIDEO KE YOUTUBE + SCHEDULE")
print("=" * 70)

# Load metadata
def load_meta(i):
    with open(ROOT / f"pending_meta_{i}.json") as f:
        return json.load(f)

metas = {
    1: load_meta(1),  # 15:48 WIB hari ini
    2: load_meta(2),  # 20:23 WIB hari ini  
    3: load_meta(3),  # 10:34 WIB besok
}

# Convert WIB ke UTC untuk schedule
WIB = timezone(timedelta(hours=7))

for i, data in metas.items():
    video_path = OUTPUT / f"short_{i}.mp4"
    if not video_path.exists():
        print(f"❌ Video {i} tidak ditemukan: {video_path}")
        continue
    
    # Hitung waktu publish
    wib_time_str = "15:48" if i == 1 else ("20:23" if i == 2 else "10:34")
    wib_time = datetime.strptime(wib_time_str, "%H:%M").time()
    
    now = datetime.now(WIB)
    today = now.date()
    publish_dt = datetime.combine(today, wib_time, tzinfo=WIB)
    
    # Jika waktu sudah lewat, gunakan besok
    if publish_dt < now:
        publish_dt += timedelta(days=1)
    
    utc_dt = publish_dt.astimezone(timezone.utc)
    publish_iso = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    print(f"\n▶ Video {i}: {data['topic_title']}")
    print(f"   File: {video_path}")
    print(f"   YT Title: {data['youtube_title']}")
    print(f"   Slot: {wib_time_str} WIB")
    print(f"   Publish UTC: {publish_iso}")
    
    # Upload via youtube_uploader.py with strict scheduling
    print(f"   Uploading & Scheduling to YouTube...")
    result = subprocess.run([
        sys.executable, "youtube_uploader.py",
        str(video_path),
        str(ROOT / f"pending_meta_{i}.json"),
        publish_iso
    ], capture_output=True, text=True, cwd=str(ROOT))
    
    print(f"   stdout: {result.stdout[:500]}")
    if result.returncode == 0:
        print(f"   ✅ Upload success!")
        try:
            upload_result = json.loads(result.stdout.strip())
            print(f"   Video ID: {upload_result.get('video_id', 'N/A')}")
            print(f"   URL: {upload_result.get('url', 'N/A')}")
        except:
            print(f"   (gagal parse hasil)")
    else:
        print(f"   ❌ Upload gagal: {result.stderr[:300]}")

print("\n" + "=" * 70)
print("UPLOAD Selesai")
print("=" * 70)