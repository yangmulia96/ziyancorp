# 9Remote & Remote n8n Execution

TERBUKTI 2026-08-09.

## 9Remote start (simpel)
- `9remote start` → QR + Connect URL + One-Time Key. JANGAN ribet.
- Conflict port 2208 / pipe `9remote-pty`: kill node nyangkut lalu start lagi.

## Eksekusi saat Bos remote (tidak pegang laptop)
- JANGAN suruh Bos klik UI n8n / buka remote desktop.
- Agent kerjakan lewat DB sqlite (PITFALL #19/#32) atau n8n CLI:
  - `n8n publish:workflow --id=<ID>` (publish = activate tanpa UI)
  - `n8n import:credentials --input=file.json` (PITFALL #27)
- Setelah edit DB: suruh Bos restart n8n (atau sudah jalan → reload).

## Tool yang GAGAL akses localhost
- `browser_navigate` localhost:5678 → ERR_CONNECTION_REFUSED (sandbox beda network). JANGAN loop.
- `computer_use` TIDAK bisa kontrol keyboard browser di Windows (foreground-lock, butuh UIAccess). Jangan andalkan klik UI n8n dari jauh.
- Solusi remote: DB edit + restart, atau Bos 1 klik kalau sudah pegang laptop.
