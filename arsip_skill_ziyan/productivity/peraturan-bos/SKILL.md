---
name: peraturan-bos
description: "Peraturan kritikal workflow otomatisasi ZIYAN."
version: 1.0.0
author: ZIYAN Orchestrator
---

# Peraturan Kritikal ZIYAN

## 1. Cookies = VIP Stamp (Sesi Sah)
- Cookies bukti keabsesan, bukan kredensial. **Jangan tampilkan isi cookies ke chat publik.**
- Export cookies NotebookLM (`mziyan266`) → format Netscape → konversi ke `storage_state.json`.
- Simpan di `OneDrive/ziyan_pending/`, **jangan di chat**.
- Cookie expired → minta Bos export ulang.

## 2. Anti‑Bot Google
- Google agresif. Jika akun blokir → **STOP + beri tahu Bos.**
- Hindari spam request berulang.

## 3. Verifikasi Hasil
- Output video/audio di `C:\Users\arija\ziyan_videos\`
- Script harus pakai event `Browser.downloadProgress` (state `completed`).
- Jangan andalkan `print 'SELESAI'` tanpa verifikasi file.

## 4. NotebookLM Wajib untuk Video
- Video hanya via NotebookLM.

## 5. Referensi
- `ziyan_drive_learn/laporan_pabrik_youtube.md`
- `ziyan_drive_learn/transkrip_audio.txt`