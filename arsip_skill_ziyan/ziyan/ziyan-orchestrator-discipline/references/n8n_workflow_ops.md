# n8n Workflow Ops — Pola Terverifikasi (v2.33, Windows, tanpa Docker)

## 1. Install & Start (tanpa Docker)
- `npm install -g n8n` → jalan langsung di Node.js (tidak butuh Docker).
- Start: background terminal `n8n start` (port 5678). Cek `curl localhost:5678/healthz` → `{"status":"ok"}`.
- Log: `/tmp/n8n.log`. Warning "outside container deprecated" = masih jalan.
- **INSTALL LAMA**: `npm install -g n8n@2.33.4` bisa timeout 60s di foreground. Jalankan background (`notify_on_complete`) + polling `n8n --version`. Jika gagal dengan TAR_ENTRY_ERROR (extract rusak) → ulang dengan `npm install -g n8n@2.33.4 --no-audit --no-fund`.

## 2. API Key lokasi (ZIYAN)
- Key di `ziyan_keys.env` tapi **line berpindah** antar edit (pernah 49, jadi 44 setelah hapus Twitter).
- JANGAN hardcode line. Ambil dynamic:
  `KEY=$(grep -E '^eyJ' ziyan_keys.env | head -1)`
- Header: `X-N8N-API-KEY: $KEY`

## 3. Import Workflow JSON
- POST `http://localhost:5678/api/v1/workflows` body JSON.
- WAJIB: `name`, `nodes`, `connections`, `settings` (minimal `{"executionOrder":"v1"}`).
- HAPUS `versionId`, `pinData` (400 error).

## 4. Activate Workflow
- `PATCH` → 405. `PUT` → 400 "additional properties" (harus strip updatedAt/createdAt/id).
- **CARA JALAN**: `POST /api/v1/workflows/{id}/activate` → langsung active:true.
- **ATAU CLI**: `n8n publish:workflow --id=ID` (tapi butuh restart n8n biar effect, dan node credential tetap harus valid di memory).
- **ATAU DB**: `UPDATE workflow_entity SET active=1 WHERE id='ID'` lalu restart — tapi n8n cache di memory, sering tidak load tanpa restart benar.

## 5. executeCommand TIDAK didukung v2.33
- Error: `Unrecognized node type: n8n-nodes-base.executeCommand`
- FIX: ganti `n8n-nodes-base.code` + child_process:
  ```js
  const {execSync}=require('child_process');
  const out=execSync(`python x.py "arg"`).toString();
  return [{json:{output:out}}];
  ```

## 6. Env Var tidak kebaca dari Background Shell
- `export` di bg shell sering tidak masuk proses n8n.
- FIX: inject key langsung ke URL/body node HTTP (`?key=AKTU_KEY`), bukan `{{$env.X}}`.

## 7. Gemini Veo3 / NanoBanana Quirks
- Key valid tapi bisa 429 (quota) atau 404 (`veo-3.0-generate-preview` tidak ada di v1beta).
- Test: `curl ".../v1beta/models/gemini-2.0-flash:generateContent?key=K"` → 429 = quota, bukan format.

## 8. Reverse-Engineer Kompetitor
- TikTok transcript BLOCK (CAPTCHA). Pakai **oembed**: `curl "https://www.tiktok.com/oembed?url=<url>"` → caption.
- YouTube oembed untuk title; `r.jina.ai/<url>` untuk blog article.
- Dari caption/hashtag → rebuild workflow tanpa lihat node asli.

## 9. PITFALL WINDOWS v2.33 — SETUP OWNER & CREDENTIAL (DITEMUKAN 2026-08-09)
- **"Instance owner shell user not found"**: n8n 2.33 di Windows butuh user OS dengan role owner, bukan cuma DB. Setup owner via UI sering gagal kalau DB user rusak (id=NULL / roleSlug='global:member').
  - FIX DB: `UPDATE user SET id='owner-ziyan', roleSlug='global:owner' WHERE email='...'` lalu restart n8n.
  - KALAU tetap gagal → hapus user (`DELETE FROM user`) + set `isInstanceOwnerSetUp=false` → restart → setup owner BARU lewat UI (Bos isi password sendiri).
  - Bypass: `N8N_USER_MANAGEMENT_DISABLED=true` di `.n8n/.env` → n8n tanpa auth (langsung dashboard). TAPI kalau DB sudah ada user management enabled, env tidak cukup — harus hapus user + settings dulu.
- **"Found credential with no ID"** (Telegram Trigger / node lain): n8n 2.33 tidak terima credential yang di-inject lewat DB/CLI/API tanpa login session. Node `credentials: {'telegramApi':'ziyan_clipperbot_cred'}` di DB TIDAK cukup — n8n cek di memory/encrypt saat activate.
  - SATU-SATUNYA cara pasti: **Bos buka UI → klik node → pilih credential dari dropdown → Save → Activate**. Browser tool sandbox TIDAK bisa akses localhost (connection refused) → pakai `computer_use` (background desktop) atau Bos yang klik.
  - Credential bisa dibuat lewat CLI (`n8n import:credentials --input=cred.json` dengan format `[{id,name,type,data:{accessToken}}]`) → masuk DB tapi tetap butuh link di UI.
- **JANGAN hapus user/settings sembarangan** (SQL DELETE without WHERE = butuh approval, dan bisa rusak instance). Lebih aman: backup DB dulu (`cp .n8n/database.sqlite backup.sqlite`).
- **Reinstall bersih** (kalau instance korup): `npm uninstall -g n8n` → `rm -rf .n8n` → `npm install -g n8n@2.33.4 --no-audit --no-fund` → setup owner baru via UI. Export workflow dulu (`n8n export:workflow --id=ID --output=backup.json`) sebelum hapus.

## 10. 9REMOTE (remote desktop dari jauh)
- CLI: `9remote start` (background) → Bos buka `https://9remote.cc/login` di HP, scan QR / masukkan One-Time Key.
- Fitur "Unlock PC remotely" ada di **app 9Remote** (bukan web) → nyalakan saat laptop LOGIN (Start → 9Remote → Settings). Kalau laptop ke-lock & fitur belum nyala, agent TIDAK bisa bypass dari jauh (butuh admin/shell).
- `9remote key` / `9remote otk` untuk dapat connect URL (butuh server jalan).
- Zombie: kalau port 2208 / pipe `9remote-pty` sudah dipakai → kill process node lama + `rm -f //./pipe/9remote-pty` lalu start ulang.
