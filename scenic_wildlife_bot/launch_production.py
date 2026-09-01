#!/usr/bin/env python3
"""
Production launcher - inject 3 cells ke Google Colab dan monitoring
"""
import subprocess, sys, json, time, os
from pathlib import Path

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")
VENV = r"C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"

print("=" * 70)
print("PRODUCTION LAUNCHER - 3 VIDEO SHORT")
print("=" * 70)

# Load meta untuk semua 3 video
videos = []
for i in range(1, 4):
    meta_file = ROOT / f"pending_meta_{i}.json"
    cell_file = ROOT / f"pending_colab_cell_{i}.json"
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        videos.append({
            "id": i,
            "topic": data["topic_title"],
            "yt_title": data["youtube_title"],
            "hook": data["hook_sentence"],
            "script": data["script_lines"],
            "search_kw": data["search_keyword"],
            "description": data["youtube_description"],
            "tags": data["youtube_tags"],
        })
        print(f"\n📌 Video #{i}: {data['topic_title']}")
        print(f"   YT: {data['youtube_title'][:80]}...")
        print(f"   Hook: {data['hook_sentence']}")
    else:
        print(f"❌ Video #{i}: meta file tidak ditemukan")

# Generate colab cell untuk masing-masing
print("\n" + "=" * 70)
print("BUILDING COLAB CELLS")
print("=" * 70)

from colab_renderer import build_colab_cell

for video in videos:
    cell_code = build_colab_cell(video)
    cell_file = ROOT / f"pending_colab_cell_{video['id']}.py"
    with open(cell_file, "w", encoding="utf-8") as f:
        f.write(cell_code)
    print(f"✅ Cell #{video['id']}: {len(cell_code)} chars → {cell_file.name}")

print("\n" + "=" * 70)
print("INSTRUCTIONS UPLOAD KE GOOGLE COLAB")
print("=" * 70)
print("""
LANGKAH UPLOAD MANUAL:

1. Buka https://colab.research.google.com
2. Buat notebook baru (File → New notebook)
3. Upload 3 file pairs (cell + meta) untuk tiap video:
   
   Video #1 (target: 15:48 WIB):
   - pending_colab_cell_1.py
   - pending_meta_1.json
   
   Video #2 (target: 20:23 WIB):
   - pending_colab_cell_2.py
   - pending_meta_2.json
   
   Video #3 (target: besok 10:34 WIB):
   - pending_colab_cell_3.py
   - pending_meta_3.json

4. Upload juga colab_runner_X.py sebagai runner

5. Di notebook, run sel urutan ini:
   # Cell 1: Install deps
   !pip install -q pydub edge-tts Pillow requests google-generativeai
   
   # Cell 2: Load metadata
   import json
   with open('pending_meta_1.json', 'r') as f:
       data = json.load(f)
   print(f"TOPIK: {data['topic_title']}")
   
   # Cell 3: Run production cell
   exec(open('pending_colab_cell_1.py').read())

6. Tunggu render selesai (~5-10 menit per video)
7. Download video dari /content/drive/MyDrive/ZIYANCORP_AI_FACTORY/
8. Upload ke YouTube via youtube_uploader.py
9. Schedule di slot waktu:
   - Video #1: 15:48 WIB
   - Video #2: 20:23 WIB
   - Video #3: besok 10:34 WIB
""")

print("\n" + "=" * 70)
print("STATUS PRODUKSI")
print("=" * 70)
print(f"""
📌 TOPIK 3 VIDEO:
   1. {videos[0]['topic_title']}
      → {videos[0]['youtube_title']}
   2. {videos[1]['topic_title']}
      → {videos[1]['youtube_title']}
   3. {videos[2]['topic_title']}
      → {videos[2]['youtube_title']}

📁 FILES:
   - pending_colab_cell_1.py + pending_meta_1.json ✅
   - pending_colab_cell_2.py + pending_meta_2.json ✅
   - pending_colab_cell_3.py + pending_meta_3.json ✅

⏰ TIME SLOTS:
   - Video #1: 15:48 WIB (DATANG) - segera produksi
   - Video #2: 20:23 WIB (DATANG) - setelah video #1
   - Video #3: 10:34 WIB BESOK - terakhir

⚡ REKOMENDASI:
   Upload sekarang ke Google Colab dan mulai render.
   Semakin awal render, semakin cepat video ready untuk upload.
""")
