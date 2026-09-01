# n8n v2.33 Operational Notes (Windows / Hermes)

## Install (tanpa Docker)
```
npm install -g n8n
n8n start   # http://localhost:5678
```
Health check: `curl http://localhost:5678/healthz` -> `{"status":"ok"}`

## API Key n8n
- Bos generate di n8n UI: Settings -> n8n API -> Create Key
- Tersimpan di `C:\Users\arija\ziyan_keys.env` (cari baris yang diawali `eyJ` — JANGAN hardcode nomor line, line berpindah setelah file diedit)
- Ambil: `KEY=$(grep -E '^eyJ' ziyan_keys.env | head -1)`
- Header: `X-N8N-API-KEY: $KEY`

## Import Workflow (JSON -> n8n)
- `POST /api/v1/workflows` dengan body JSON (harus ada `settings`, `name`, `nodes`, `connections`)
- Hapus `versionId`, `pinData` sebelum kirim (error: "versionId must be string")
- Error "request/body must have required property 'settings'" -> tambah `"settings":{"executionOrder":"v1"}`
- Response sukses berisi `"id"` (workflow ID, 16 char)

## Activate Workflow (v2.33 QUIRKS — PENTING)
- `PATCH` -> "method not allowed"
- `PUT /workflows/{id}` -> butuh full body + "additional properties" error (strip `updatedAt`,`createdAt`,`id`,`versionId`,`activeVersionId`,`versionCounter`,`triggerCount`,`sourceWorkflowId`,`shared`,`tags`,`activeVersion`)
- **Cara benar:** `POST /api/v1/workflows/{id}/activate` (setelah workflow ada)
- Jika error "Unrecognized node type: n8n-nodes-base.executeCommand" -> node itu DEPRECATED di v2.33
  - Fix: ganti ke `n8n-nodes-base.code` dengan JS:
    ```js
    const {execSync} = require('child_process');
    const out = execSync(`PERINTAH_DISINI`).toString();
    return [{json:{output: out}}];
    ```

## Node Restrictions v2.33
- `executeCommand` = TIDAK didukung (ganti Code node)
- `httpRequest` typeVersion 4 OK
- `webhook` typeVersion 2 OK
- `code` node = jalankan shell via `child_process.execSync` (bisa TTS/FFmpeg)

## Contoh activate penuh
```bash
KEY=$(grep -E '^eyJ' ziyan_keys.env | head -1)
WID=$(curl -s -X POST localhost:5678/api/v1/workflows -H "X-N8N-API-KEY: $KEY" \
  -H "Content-Type: application/json" -d @workflow.json | python -c "import sys,json;print(json.load(sys.stdin)['id'])")
curl -s -X POST localhost:5678/api/v1/workflows/$WID/activate -H "X-N8N-API-KEY: $KEY"
```

## Templates ZIYAN (sudah ada)
- `C:\Users\arija\ziyan_n8n_templates\ig_auto_post.json` — IG auto-post (Meta Graph API)
- `C:\Users\arija\ziyan_n8n_templates\affiliate_video_generator.json` — Veo3 + NanoBanana + TTS (ACTIVE: hFKcsF60ERImmp3z)
- `tts_edge.py` — Edge-TTS helper (gratis, Indo: ArdiNeural/GadisNeural)

## Pitfall Distribusi (CORRECTION BOS 2026-08-07)
- **Twitter/X auto-post DIMATIKAN** — Bos: "ngabisin saldo aja gak jelas postingan nya"
- `~/.x_credentials` dikosongkan, token dihapus dari `ziyan_keys.env`
- Jangan auto-post ke X tanpa approval Bos. Channel lain (YouTube/Telegram/Blog) aman.
