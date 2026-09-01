# Remote Execution — Bos Tidak Pegang Laptop

TERBUKTI 2026-08-09. Bos marah berulang karena agent suruh dia klik UI / buka remote padahal dia jauh.

## HARD RULE
- Saat Bos remote/jauh (tidak pegang laptop): **EKSEKUSI sendiri lewat terminal / DB sqlite / n8n CLI**. JANGAN suruh Bos klik UI, buka remote desktop, atau "tunggu Bos buka laptop".
- Respons HARUS cepat & pendek. Jangan bertele-tele jelaskan masalah — langsung solusi + hasil.

## 9Remote (fitur 9Router)
- START CUKUP: `9remote start` → keluar QR + Connect URL + One-Time Key. JANGAN ribet kill zombie / cek port dulu (Bos: "tinggal ketik 9remote lalu enter").
- Kalau `9remote start` silent exit / port 2208 conflict → `tasklist | grep 9remote` lalu `taskkill /F /PID <pid>`, lalu `9remote start` lagi.
- Agent TETAP kerjakan task lewat terminal, jangan lempar ke Bos walau 9Remote jalan.

## Annoy signals (jangan tunggu)
- "Aku gak pegang laptop bodoh, dari tadi aku suruh sama kamu"
- "Kenapa ribet kali, tinggal ketik 9remote lalu enter"
- "Gak kamu turn on, aku tunggu kamu dari tadi"
- "Jangan lambat responnya"
