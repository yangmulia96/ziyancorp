import subprocess, sys, os, time, json
from pathlib import Path

# Start colab-mcp server menggunakan uvx (seperti di mcp_config.json)
# uvx sudah terinstall dan colab-mcp tersedia di cache

print("=" * 70)
print("STARTING COLAB-MCP SERVER VIA UVX")
print("=" * 70)

# Jalankan uvx colab-mcp di background
# Perlu port yang visible untuk MCP client

try:
    # Coba start colab-mcp dengan port yang bisa diakses
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvx", "git+https://github.com/googlecolab/colab-mcp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=r"C:\Users\arija\ziyancorp\scenic_wildlife_bot"
    )
    
    print(f"✅ Process started: PID {proc.pid}")
    print(f"   Menunggu server siap...")
    
    # Tunggu sebentar dan cek apakah berjalan
    time.sleep(10)
    
    if proc.poll() is None:
        print("✅ Server masih berjalan (belum exit)")
        
        # Cek port yang dipakai
        ps_out = subprocess.run(["tasklist", "/FI", f"PID eq {proc.pid}"], 
                               capture_output=True, text=True, timeout=5)
        print(f"   Process info: {ps_out.stdout[:200] if ps_out.stdout else 'no info'}")
        
        # Tunggu lagi dan coba cek port
        time.sleep(5)
        
        if proc.poll() is None:
            print(f"✅ Server masih running setelah 15 detik")
            print(f"   Mengambil output/error (jika ada)...")
            if proc.stdout:
                out = proc.stdout.read(100)
                if out:
                    print(f"   stdout: {out}")
            if proc.stderr:
                err = proc.stderr.read(100)
                if err:
                    print(f"   stderr: {err}")
        else:
            print(f"❌ Server exited dengan code: {proc.returncode}")
            if proc.stdout:
                print(f"   stdout: {proc.stdout.read()[:500]}")
            if proc.stderr:
                print(f"   stderr: {proc.stderr.read()[:500]}")
    else:
        print(f"❌ Server exited segera dengan code: {proc.returncode}")
        if proc.stdout:
            print(f"   stdout: {proc.stdout.read()[:500]}")
        if proc.stderr:
            print(f"   stderr: {proc.stderr.read()[:500]}")
            
except Exception as e:
    print(f"❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()
