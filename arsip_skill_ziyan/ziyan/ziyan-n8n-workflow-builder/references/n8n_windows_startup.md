# n8n Windows Startup & Debug (PITFALL #10)

## Symptom → Root Cause → Fix

### 1. `Command "api" not found` + token bash leak di log
- **Cause**: `~/.n8n/.env` corrupt — baris pertama cuma hash tanpa key name (`c6b85f...` bukan `N8N_API_KEY=c6b85f...`).
- **Fix**: `write_file` ulang `~/.n8n/.env` isi rapi:
  ```
  N8N_API_KEY=c6b85f458996bb4e6edeb89be62a5012
  ```

### 2. `n8n's port 5678 is already in use`
- **Cause**: session background lama gak ke-kill (punya PID sendiri, gak ikut mati).
- **Fix**:
  ```bash
  ps aux | grep node | grep -v grep   # cari PID
  kill -9 <PID>
  # atau semua:
  for p in $(ps aux | grep node | grep -v grep | awk '{print $1}'); do kill -9 $p; done
  sleep 4
  netstat -tln | grep -E "5678|5679" || echo "port kosong"
  ```
  CATATAN: `taskkill //F //IM node.exe` di MSYS sering gagal → pakai `kill -9` dari bash.

### 3. Proses langsung mati setelah start
- **Cause**: pakai `n8n start &` di terminal foreground → bash background gak jaga proses.
- **Fix**: pakai `terminal(background=true)` (bukan `&`).

### 4. API `Unauthorized` walau key benar
- **Cause**: n8n start sebelum `.env` diperbaiki → env gak ke-load.
- **Fix**: kill semua n8n, perbaiki `.env`, start bersih.

### 5. Port bentrok terus
- **Fix**: pakai port lain:
  ```bash
  export N8N_PORT=5679
  n8n start   # background=true
  ```

## Health Check
```bash
curl -s -m 5 localhost:5679/healthz   # {"status":"ok"}
curl -s -m 8 localhost:5679/rest/workflows -H "X-N8N-API-KEY: $KEY"  # list workflow
```

## Import Workflow (setelah n8n live)
- CLI: `n8n import:workflow --input=file.json` (HAPUS field `id`/`versionId`/`webhookId`/`credentials` dari JSON dulu, else SQLITE_CONSTRAINT).
- Atau POST `/rest/workflows` dengan header `X-N8N-API-KEY`.
- Activate: `POST /rest/workflows/{id}/activate`.

## Catatan Sesi 2026-08-09
- n8n v2.33.4 di Windows 10 (MSYS bash). Start butuh 40-50 detik baru listen.
- DB sqlite lama (`~/.n8n/database.sqlite` 2MB dari 07-08) tetap valid, berisi 11 workflow lama.
- CLI import gagal `NOT NULL constraint failed: workflow_entity.id` walau tanpa id → prefer API POST atau perbaiki JSON.
- User management: kalau DB sudah punya owner, `N8N_USER_MANAGEMENT_DISABLED=true` gak otomatis bypass API auth — tetap perlu setup owner lewat UI (`localhost:5679` → Sign in).
