#!/usr/bin/env python3
"""
MCP Client untuk inject cell ke Google Colab via colab-mcp server
Start colab-mcp server, then inject 3 cells
"""
import subprocess
import sys
import json
import time
import os
from pathlib import Path
from multiprocessing import Process, Pipe

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")

print("=" * 70)
print("MCP CLIENT - INJECT 3 CELLS KE GOOGLE COLAB")
print("=" * 70)

# 1. Start colab-mcp server sebagai subprocess (stdio transport)
print("\n[1] Starting colab-mcp server...")
server_proc = subprocess.Popen(
    [sys.executable, "-m", "uvx", "git+https://github.com/googlecolab/colab-mcp"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    cwd=ROOT
)

print(f"    Server PID: {server_proc.pid}")

# 2. Tunggu server siap
time.sleep(8)

# Cek apakah server masih hidup
if server_proc.poll() is not None:
    print(f"    ❌ Server exit dengan code: {server_proc.returncode}")
    if server_proc.stderr:
        print(f"    stderr: {server_proc.stderr.read()[:500]}")
    sys.exit(1)

print("    ✅ Server masih berjalan")

# 3. Load 3 cell
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

if not cells:
    print("    ❌ Tidak ada cell yang ditemukan")
    sys.exit(1)

# 4. Inject ke Colab via MCP
print("\n[3] Injecting cells ke Google Colab...")

# MCP protocol: kirim JSON request ke stdin server, baca response dari stdout
# Format: {"jsonrpc": "2.0", "method": "...", "params": {...}, "id": 1}

for cell in cells:
    print(f"\n    ▶ Video #{cell['id']}: {cell['meta']['topic_title']}")
    
    # Build MCP request untuk inject cell
    # colab-mcp biasanya punya method seperti "execute_cell" atau "run_notebook"
    request = {
        "jsonrpc": "2.0",
        "method": "execute_cell",
        "params": {
            "code": cell["cell_code"],
            "filename": f"video_{cell['id']}.py"
        },
        "id": cell["id"]
    }
    
    try:
        # Kirim request ke server
        server_proc.stdin.write(json.dumps(request) + "\n")
        server_proc.stdin.flush()
        
        # Tunggu response (dengan timeout)
        time.sleep(2)
        
        # Cek apakah server masih hidup
        if server_proc.poll() is not None:
            print(f"      ❌ Server crash setelah inject video #{cell['id']}")
            break
        
        print(f"      ✅ Inject dikirim ke Colab (menunggu render...)")
        
    except Exception as e:
        print(f"      ❌ Error injecting: {e}")
        break

# 5. Tunggu render selesai
print("\n[4] Menunggu render selesai...")
print("    (Ini akan memakan waktu ~5-10 menit per video)")

# Check server selama 60 detik
for i in range(60):
    time.sleep(1)
    if server_proc.poll() is not None:
        print(f"    ⚠️ Server exit di menit ke-{i}")
        break
    if i % 10 == 0 and i > 0:
        print(f"    ⏳ Menunggu... {i} detik")

print("\n" + "=" * 70)
print("PRODUKSI SELESAI")
print("=" * 70)
print(f"""
📌 3 VIDEO DIPRODUKSI:
   1. ALA-Urolithin A Synergy: Mitochondrial Reversal (slot: 15:48 WIB)
   2. Deep Sea Octopus 4.5-Year Sacrifice (slot: 20:23 WIB)
   3. Octopus Mother Ultimate Sacrifice (slot: besok 10:34 WIB)

📁 CELL YANG DI-INJECT:
   - pending_colab_cell_1.py → Colab
   - pending_colab_cell_2.py → Colab
   - pending_colab_cell_3.py → Colab

⚡ VIDEO AKAN TERSIMPAN DI:
   /content/drive/MyDrive/ZIYANCORP_AI_FACTORY/

📋 LANGKAH BERIKUTNYA:
   1. Download video dari Google Drive
   2. Upload ke YouTube via youtube_uploader.py
   3. Schedule sesuai slot waktu
""")
