import sys, json, subprocess
from pathlib import Path

VENV = r"C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")

print("="*60)
print("PRODUCTION PIPELINE - AUTO EXEC")
print("="*60)

# STEP 1: Generate topic
print("\n🔥 STEP 1: Generate topik via Gemini...")
result = subprocess.run(
    [VENV, str(ROOT / "topic_engine.py")],
    capture_output=True, text=True, timeout=120, cwd=ROOT
)
# Split output: garis pemisah antara log dan JSON
output = result.stdout.strip()
if "{" in output:
    json_start = output.index("{")
    json_str = output[json_start:]
    data = json.loads(json_str)
else:
    print("ERROR: Tidak ada JSON di output")
    sys.exit(1)

print(f"✅ TOPIK: {data['topic_title']}")
print(f"   YT: {data['youtube_title']}")

# STEP 2: Build Colab cell
print("\n📝 STEP 2: Build Colab cell...")
sys.path.insert(0, str(ROOT))
from colab_renderer import build_colab_cell
cell_code = build_colab_cell(data)
(ROOT / "pending_colab_cell.py").write_text(cell_code, encoding="utf-8")
(ROOT / "pending_meta.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ Cell: {len(cell_code)} chars")
print(f"   → pending_colab_cell.py")
print(f"   → pending_meta.json")

# STEP 3: Update production log
print("\n📋 STEP 3: Update production_log.json...")
log_file = ROOT / "production_log.json"
log = json.loads(log_file.read_text(encoding="utf-8")) if log_file.exists() else {"total_videos": 0, "uploads": []}
log["total_videos"] += 1
log["uploads"].append({
    "video_number": log["total_videos"],
    "topic_title": data["topic_title"],
    "youtube_title": data["youtube_title"],
    "status": "cell_ready",
    "created_at": subprocess.run(
        ["powershell", "-NoProfile", "-Command", "(Get-Date -Format 'o')"],
        capture_output=True, text=True
    ).stdout.strip(),
})
log_file.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"✅ Total videos: {log['total_videos']}")

# STEP 4: Update used_topics
print("\n📌 STEP 4: Archive topik...")
used_file = ROOT / "used_topics.json"
used = json.loads(used_file.read_text(encoding="utf-8")) if used_file.exists() else []
if data["topic_title"] not in used:
    used.append(data["topic_title"])
    used_file.write_text(json.dumps(used, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"✅ Used topics: {len(used)}")

print("\n" + "="*60)
print("✅ PIPELINE SELESAI - SIAP INJECT KE COLAB")
print("="*60)
print(f"\n📌 TOPIK: {data['topic_title']}")
print(f"📌 YOUTUBE: {data['youtube_title']}")
print(f"📌 HOOK: {data['hook_sentence']}")
print(f"\n📁 pending_colab_cell.py: {len(cell_code)} chars")
print(f"📁 pending_meta.json: ready")
print(f"📁 production_log.json: {log['total_videos']} videos")
print("\n⚡ LANGKAH SELANJUTNYA:")
print("   → Inject cell ke Google Colab via MCP")
print("   → Colab: TTS + Pexels + FFmpeg + Subtitle → Render")
print("   → YouTube: Upload + Schedule")
