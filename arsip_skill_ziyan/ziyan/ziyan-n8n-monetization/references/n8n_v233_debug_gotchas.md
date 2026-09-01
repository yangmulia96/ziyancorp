# n8n v2.33.4 — Debug Gotchas (dari build workflow `wa_order_notif`, 2026-08-08)

Workflow gagal 15x sebelum jalan. Ini root-cause yang ditemukan, urut dari yang paling sering bikin silent error.

## GEJALA KUNCI: "Error in workflow" / execution `status:error` tapi `resultData:[]`, `lastNodeExecuted:null`, `data:[]`
Artinya execution gagal SEBELUM node manapun jalan. BUKAN logic function. Cek urutan di bawah.

## 1. Webhook PATH CONFLICT (paling sering)
- Build ulang workflow berkali-kali dengan path mirip (`wa-order-webhook`, `wa-order-v2`, `wa-order-v3`) → n8n simpan registrasi webhook lama di memory → POST balik "Workflow was started" tapi execution error kosong.
- **FIX**: pakai **path unik segar** tiap build besar (mis. `ziyan-wa-2026-xyz`). Atau restart n8n (`taskkill /F /PID <pid>` lalu `n8n start` bg) untuk bersihkan registration.
- Minimal 2-node (Webhook→Function echo) SELALU jalan → kalau gagal, ini pasti path conflict atau webhook node rusak, bukan function.

## 2. `Date.now()` di Function node → SILENT FAIL
- `orderId: body.order_id || ("ORD-" + Date.now())` → execution error kosong (n8n v2.33 sandbox restriction pada `Date.now()`? terbukti gagal; hapus → jalan).
- **FIX**: jangan pakai `Date.now()` di Function node. Ambil timestamp dari webhook body (`body.timestamp`) atau hardcode / pakai node lain.

## 3. Import REST API v1 — field read-only
- `POST /api/v1/workflows` dengan `active:true` → `request/body/active is read-only`.
- Dengan `tags:[...]` → `request/body/tags is read-only`.
- Tanpa `settings` → `request/body must have required property 'settings'`.
- **FIX**: strip `active` + `tags`, WAJIB sertakan `"settings":{"executionOrder":"v1"}`.
- Setelah import dapat ID BARU → re-activate (`POST /api/v1/workflows/{id}/activate`).

## 4. Webhook `responseMode: onReceived` → "Error in workflow"
- Default (tanpa responseMode) atau `"lastNode"` jalan. `onReceived` bikin silent error di v2.33.
- **FIX**: hapus field `responseMode` dari webhook node.

## 5. HTTP Request node ke eksternal tanpa creds → workflow error
- Node `Kirim WA (Fonnte)` → FONNTE_KEY kosong → 401 → execution error.
- **FIX**: di parameters node tambah `"continueOnFail": true` + `"onError": "continueRegularOutput"` agar node gagal tapi workflow lanjut ke Log.

## 6. Node name dengan `&` / spasi — hindari
- `Parse & Validate Order`, `Kirim WA (Fonnte)` → rename ke `ParseOrder`, `SendWA` (camelCase). Hygiene + hindari reference node lintas dengan string nama.

## 7. Regex di Function node — prefer loop sederhana
- `phoneRaw.replace(/[^0-9]/g,'')` jalan di Node lokal, tapi untuk hindari risk sandbox n8n: pakai `for...of` + banding karakter (`ch >= '0' && ch <= '9'`). Terbukti jalan di execution.

## METODE ISOLASI (terbukti cepat nemu root cause)
1. Buat minimal: Webhook → Function(echo `$json`). Test. Kalau jalan → webhook OK.
2. Tambah 1 node tiap iterasi, test tiap kali.
3. Kalau tambah node X → gagal → X adalah penyebab.
4. Cek execution via `GET /api/v1/executions/{id}` → `resultData.runData` untuk lihat node error spesifik (tapi kalau empty = path conflict / pre-node, lihat #1).

## RESTART n8n (Windows, tanpa nohup)
- Hermes BLOKIR `nohup`/`setsid` di terminal foreground → pakai `terminal(background=true)` dengan command `n8n start`.
- Kill old: `taskkill //F //PID <pid>` (dapat dari `netstat -ano | grep :5678`).
- After restart: health `curl localhost:5678/healthz` → 200, lalu re-activate workflow (state reset).
