# n8n v2.33 Function Node & Webhook Gotchas (Sesi 2026-08-08)

## 1. `Date.now()` DIBLOKIR di Function Node
- **Symptom**: Workflow error silent — `status: error`, `resultData: []`, `lastNodeExecuted: None`, tanpa error message.
- **Root cause**: n8n v2.33 sandbox (VM2/isolated-vm) memblokir `Date.now()` / `new Date()`.
- **Test bukti**: 2-node webhook→function TANPA Date.now = SUCCESS (Exec 27). 3+ node dengan `Date.now()` = selalu ERROR.
- **Fix**: 
  - Timestamp dari webhook body: `body.timestamp` atau `body.order_id`
  - Hardcode placeholder: `"ORD-1"`
  - Atau generate ID di luar n8n (HTTP request ke service lain)
- **JANGAN** pakai `Date.now()` di function node untuk unique ID.

## 2. Webhook Path Conflict
- **Symptom**: Workflow error silent di path `wa-order-webhook` / `wa-order-v2` / `wa-order-v3` (dibuat banyak versi), tapi minimal test di path lain JALAN.
- **Root cause**: n8n cache webhook path di memory. Delete + re-import dengan path SAMA bisa conflict (terutama kalau path sudah pernah dipakai workflow yang di-delete).
- **Test bukti**: `ziyan-wa-2026-xyz` (path unik, sekali pakai) = SUCCESS (Exec 35). `wa-order-*` (reuse path) = selalu ERROR.
- **Fix**:
  - Pakai path UNIK & jarang dipakai untuk tiap production workflow: `ziyan-wa-2026-xyz`, `ziyan-shopee-sync-2026`, dll.
  - Hindari reuse path yang pernah dipakai workflow deleted.
  - Restart n8n TIDAK selalu bersihkan cache path.
  - Untuk test, pakai path acak (mis. `min-test`) — itu aman karena belum pernah conflict.

## 3. Node Name dengan `&` / Spasi
- Tidak error langsung, tapi confuse saat debug connection.
- Rekomendasi: `ParseOrder`, `SendWA` (camelCase, tanpa simbol).

## 4. HTTP Request Node Error Handling
- Tanpa `continueOnFail`, kalau API gagal (401/403) → seluruh workflow error.
- Fix: set `continueOnFail: true` + `onError: 'continueRegularOutput'` di parameter HTTP node.

## Debug Checklist (workflow error silent)
1. Cek `resultData` kosong? → webhook node gagal di core (bukan function).
2. Cek function pakai `Date.now()`? → hapus.
3. Cek path pernah dipakai sebelumnya? → ganti path unik.
4. Test minimal 2-node (webhook→echo) di path baru → isolate masalah.
5. Cek execution detail: `GET /api/v1/executions/{id}` → cari `lastNodeExecuted` & `runData`.
