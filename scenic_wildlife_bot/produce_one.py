import sys, json, subprocess
from pathlib import Path

# Gunakan Python dari Hermes venv yang udah punya google-genai
VENV_PYTHON = r"C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")
sys.path.insert(0, str(ROOT))

def main():
    # 1. Generate topic via topic_engine (pakai VENV_PYTHON)
    print("🔥 Generating topic...")
    result = subprocess.run(
        [VENV_PYTHON, str(ROOT / "topic_engine.py")],
        capture_output=True, text=True, timeout=120, cwd=ROOT
    )
    if result.returncode != 0:
        print("❌ Topic engine error:", result.stderr[-500:])
        sys.exit(1)
    
    data = json.loads(result.stdout.strip())
    print(f"✅ Topic: {data['topic_title']}")
    
    # 2. Build Colab cell via colab_renderer
    print("📝 Building Colab cell...")
    from colab_renderer import build_colab_cell
    cell_code = build_colab_cell(data)
    (ROOT / "pending_colab_cell.py").write_text(cell_code, encoding="utf-8")
    (ROOT / "pending_meta.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Cell written ({len(cell_code)} chars) → pending_colab_cell.py")
    print(f"✅ Meta written → pending_meta.json")
    
    # 3. Update production_log.json
    print("📋 Updating production_log.json...")
    log_file = ROOT / "production_log.json"
    log = json.loads(log_file.read_text(encoding="utf-8")) if log_file.exists() else {"total_videos": 0, "uploads": []}
    log["total_videos"] += 1
    log["uploads"].append({
        "timestamp": subprocess.run(
            ["powershell", "-NoProfile", "-Command", "(Get-Date -Format 'o')"],
            capture_output=True, text=True
        ).stdout.strip(),
        "topic": data["topic_title"],
        "status": "cell_ready"
    })
    log_file.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Log updated")
    
    # 4. Show cell preview (30 baris pertama)
    print("\n📋 Cell preview (30 baris pertama):")
    for i, line in enumerate(cell_code.splitlines()[:30], 1):
        print(f"{i:3}| {line}")

if __name__ == "__main__":
    main()
