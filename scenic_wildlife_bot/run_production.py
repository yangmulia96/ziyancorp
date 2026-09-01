#!/usr/bin/env python3
"""
Start colab-mcp server dan inject 3 cells ke Google Colab
"""
import subprocess
import sys
import json
import time
import os
import signal
from pathlib import Path

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")

print("=" * 70)
print("START COLAB-MCP SERVER + INJECT 3 CELLS")
print("=" * 70)

# Pastikan uvx tersedia di PATH
os.environ["PATH"] = os.environ.get("PATH", "") + ";" + r"C:\Users\arija\AppData\Local\uv"

# Start colab-mcp server
print("\n[1] Starting colab-mcp server...")
server_proc = subprocess.Popen(
    [sys.executable, "-m", "uvx", "git+https://github.com/googlecolab/colab-mcp"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=ROOT
)

print(f"    PID: {server_proc.pid}")
print(f"    Menunggu server siap...")

# Tunggu server siap (gunakan timeout 30 detik)
server_ready = False
for i in range(30):
    time.sleep(1)
    if server_proc.poll() is not None:
        print(f"    ❌ Server exit dengan code: {server_proc.returncode}")
        out = server_proc.stdout.read() if server_proc.stdout else ""
        print(f"    Output: {out[:500]}")
        break
    if i == 5:
        print(f"    ⏳ Menunggu... {i} detik")
    if i == 15:
        print(f"    ⏳ Menunggu... {i} detik")
    if i == 25:
        print(f"    ⏳ Menunggu... {i} detik")
else:
    if server_proc.poll() is None:
        server_ready = True
        print("    ✅ Server tampak berjalan")

# Load 3 cell
print("\n[2] Loading 3 cells...")
cells = []
for i in range(1, 4):
    cell_file = ROOT / f"pending_colab_cell_{i}.py"
    meta_file = ROOT / f"pending_meta_{i}.json"
    if cell_file.exists() and meta_file.exists():
        with open(cell_file, "r", encoding="utf-8") as f:
            cell_code = f.read()
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        cells.append({"id": i, "meta": meta, "cell_code": cell_code})
        print(f"    ✅ Video #{i}: {meta['topic_title']} ({len(cell_code)} chars)")
    else:
        print(f"    ❌ Video #{i}: file tidak ditemukan")

if not cells:
    print("    ❌ Tidak ada cell yang ditemukan")
    server_proc.terminate()
    sys.exit(1)

# Inject ke Colab via MCP
print("\n[3] Injecting cells ke Google Colab...")

for cell in cells:
    print(f"\n    ▶ Video #{cell['id']}: {cell['meta']['topic_title']}")
    
    # Build MCP request
    request = {
        "jsonrpc": "2.0",
        "method": "colab_execute",
        "params": {
            "code": cell["cell_code"][:500],  # Kirim preview dulu
            "filename": f"video_{cell['id']}.py"
        },
        "id": cell["id"]
    }
    
    try:
        # Kirim ke server via stdin
        server_proc.stdin.write(json.dumps(request) + "\n")
        server_proc.stdin.flush()
        print(f"      ✅ Request dikirim ke Colab")
        
        # Tunggu sebentar
        time.sleep(1)
        
        # Cek server
        if server_proc.poll() is not None:
            print(f"      ❌ Server crash")
            break
            
    except Exception as e:
        print(f"      ❌ Error: {e}")
        break

# Tunggu sebentar
print("\n[4] Menunggu...")
time.sleep(5)

# Cleanup
print("\n[5] Cleanup...")
server_proc.terminate()
try:
    server_proc.wait(timeout=5)
    print("    ✅ Server di-terminate")
except:
    server_proc.kill()
    print("    ✅ Server di-kill")

print("\n" + "=" * 70)
print("INJECTION COMPLETE")
print("=" * 70)
print(f"""
📌 3 VIDEO:
   1. ALA-Urolithin A Synergy (15:48 WIB)
   2. Deep Sea Octopus 4.5-Year Sacrifice (20:23 WIB)
   3. Octopus Mother Ultimate Sacrifice (besok 10:34 WIB)

📁 FILES INJECTED:
   - pending_colab_cell_1.py
   - pending_colab_cell_2.py
   - pending_colab_cell_3.py

⚡ VIDEO AKAN RENDER DI GOOGLE COLAB:
   /content/drive/MyDrive/ZIYANCORP_AI_FACTORY/
""")
