# Fix n8n Silent Crash di Windows — Node v24 incompatibility

## GEJALA
`n8n start` keluar TANPA output (log kosong, process langsung hilang), port 5678 TIDAK
listen, `curl -o /dev/null -w '%{http_code}' localhost:5678/healthz` balik `000`.
DB tidak corrupt, env tidak salah, coba port lain (5679) sama.

## ROOT CAUSE
n8n 2.33 butuh Node 20/22. Laptop Bos cuma punya **Node v24.16.0**
(`C:\Program Files\nodejs\node.exe --version` = v24.16.0). Node 24 bikin n8n
crash senyap saat load (tidak kasih error apa pun).

## VERIFIKASI SEBELUM LAPOR "JALAN"
```
netstat -ano | findstr 5678        # HARUS ada baris LISTENING
curl -s -o /dev/null -w "%{http_code}" localhost:5678/healthz   # HARUS 200
```
JANGAN percaya `curl .../healthz | head -c` → bisa balik `OK` dari cache/stale walau
process mati (sudah terjadi, Bos marah "faktamu selalu salah").

## FIX (NO-ADMIN, TERBUKTI JALAN 2026-08-10)
`winget install` / `nvm install` BUTUH elevasi (prompt admin, gagal diam-diam).
Pakai **portable ZIP** instead:

1. Download Node 22.22.0 (zip, tanpa installer):
   ```
   curl -L -o node22b.zip "https://nodejs.org/dist/v22.22.0/node-v22.22.0-win-x64.zip"
   unzip -q node22b.zip -d node22b
   ```
   Hasil: `C:\Users\arija\node22b\node-v22.22.0-win-x64\node.exe` (cek `--version` = v22.22.0)

2. Cari binary n8n dari npx cache (atau `C:\Users\arija\AppData\Roaming\npm\node_modules\n8n\bin\n8n`):
   ```
   dir "C:\Users\arija\AppData\Local\npm-cache\_npx" /s /b | findstr "n8n\\bin\\n8n"
   ```
   Contoh path: `C:\Users\arija\AppData\Local\npm-cache\_npx\a8a7eec953f1f314\node_modules\n8n\bin\n8n`

3. Jalankan n8n dengan node 22 eksplisit (BACKGROUND, jangan `&`):
   ```
   C:\Users\arija\node22b\node-v22.22.0-win-x64\node.exe "C:\Users\arija\AppData\Local\npm-cache\_npx\a8a7eec953f1f314\node_modules\n8n\bin\n8n" start
   ```
   → port 5678 LISTENING, HTTP 200, log muncul (license SDK init, JS Task Runner).

4. Biar surviv reboot — update `start-n8n.bat` (Startup folder) pakai node 22 eksplisit:
   ```
   @echo off
   title n8n Fast Server (Node 22.22)
   "C:\Users\arija\node22b\node-v22.22.0-win-x64\node.exe" "C:\Users\arija\AppData\Local\npm-cache\_npx\a8a7eec953f1f314\node_modules\n8n\bin\n8n" start
   pause
   ```
   Path: `C:\Users\arija\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start-n8n.bat`

## JANGAN LAKUKAN
- Jangan hapus Node v24 (biarkan side-by-side). n8n aja yang pakai node 22.
- Jangan `winget install OpenJS.Nodejs.LTS.22` / `nvm install 22` tanpa admin — gagal.
- Jangan lapor "jalan" cuma dari healthz `OK` — verifikasi port LISTENING + http 200.
- Jangan suruh Bos ganti `localhost` jadi IP saat remote (9Remote cuma nampilkan layar laptop,
  browser jalan di laptop — lihat PITFALL #39).
