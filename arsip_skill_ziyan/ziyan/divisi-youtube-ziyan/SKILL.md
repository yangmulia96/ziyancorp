---
name: divisi-youtube-ziyan
description: "ZIYAN video, buat di NotebookLM, upload ke Compound Daily."
category: ziyan
---

# Divisi YouTube ZIYAN — Channel "Compound Daily"

Ruang kerja: `#youtube-ziyan` (private). Target: **Compound Daily** (`UCzWib2-2CPkWo315fzucaUw`, `@compounddaily-v7c`).

## Mandat
1. Produksi video via **NotebookLM** (JALUR UTAMA, wajib).
2. Upload ke Compound Daily via YouTube Data API (token compound).
3. Jadwal: Shorts 3x/hari (18:00/00:00/06:00 WIB), Long-form 3x/minggu (Selasa/Kamis/Sabtu).
4. Lapor tiap siklus ke `#hq`.

## Pipeline (4 tahap)
1. **Script** — divisi content/riset tulis naskah English (Tech/AI/Business/Finance, rotasi harian). Simpan ke `C:\Users\arija\ziyan_scripts\`.
2. **Produksi NotebookLM** (Bos eksekusi via Brave login, agent siapkan topik & arahan):
   - Agent TENTUKAN topik harian (Tech/AI/Biz/Finance, English).
   - Bos buka NotebookLM di Brave (login Google aktif, akun PRO/Ultra).
   - KETIK topik di prompt box → NotebookLM CARI SUMBER otomatis.
   - SUMBER diimpor ke notebook.
   - Pakai CHAT NotebookLM → perintahkan generate Long/Short video sesuai keinginan.
   - Generate background >30 mnt. Bos klik Download → simpan ke `C:\Users\arija\`.
   - **Agent BISA generate NotebookLM via `computer_use`** (Bos login sekali di Brave, lalu agent klik Studio → Generate → Download otomatis). Tanpa API publik memang tidak bisa lewat script murni, tapi computer_use menutupi itu. Bos sepakat 2026-08-02: "agent yang selesaikan semua" (bukan Bos manual). Jika computer_use gagal, fallback: Bos generate manual lalu taruh file di `OneDrive/ziyan_pending/`.
3. **Upload** — ambil file video dari disk, upload via YouTube Data API:
   - Token: `C:\Users\arija\ziyan_credentials\youtube_token_compound.json` (BOUND Compound Daily, jangan pakai `youtube_token.json` yg ke Ziyan Malik).
   - Metadata: title, description (disclosure AI-generated), tags, categoryId=28, privacyStatus=`private` dulu (Bos review sebelum publik).
   - Resumable: `POST /upload/youtube/v3/videos?uploadType=resumable&part=snippet,status` → PUT bytes ke Location.
4. **Verify** — list playlist → pastikan video masuk Compound Daily. Lapor URL ke `#hq`.

## Pitfalls (jangan diulang)
- **JANGAN render video lokal** (ffmpeg + TTS). edge-tts SSL error, 9router TTS 502. Jalur utama = NotebookLM. Lokal cuma cadangan kalau Bos minta.
- **Token salah channel** → upload ke Ziyan Malik. SELALU `youtube_token_compound.json`.
- **Video jangan dikirim ke chat** (besar). Simpan di `C:\Users\arija\`, lapor URL.
- refresh_token Production TIDAK expire 7 hari — kalau 401, tukar ulang pakai code baru.

## Keamanan
- Credential hanya di `ziyan_credentials/`, tidak ke chat.
- Bahasa video: English.
- Wajib disclosure AI-generated. JANGAN AI-spam/reused-content.
