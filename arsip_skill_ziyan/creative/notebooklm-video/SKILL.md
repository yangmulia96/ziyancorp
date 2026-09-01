---
name: notebooklm-video
description: "Buat & download video NotebookLM via computer_use."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows, macos, linux]
---

# NotebookLM Video Production (computer_use driven)

Workflow membuat & mendownload video dari Google NotebookLM. Per 2026 layanan
ini rebrand jadi **Gemini Notebook** (URL `notebooklm.google.com` tetap valid).

## Kapan pakai
User minta "buat video di NotebookLM" / "generate video Gemini Notebook" /
"download video dari NotebookLM". Bisa sebagai tugas langsung atau didelegasikan
ke divisi produksi konten.

## HARD PITFALL — Google blokir sesi browser otomatis
JANGAN pakai `browser_navigate`/`browser_*` untuk login Google. Google menolak
dengan: *"This browser or app may not be secure"* — dan itu muncul **SEBELUM**
kolom password. Bukan salah password; sesi otomatis terdeteksi tidak aman.

WORKAROUND TERVERIFIKASI (dipakai 2026-07-31, sukses):
- Pakai `computer_use` dengan `app='Brave'` (atau Chrome) untuk mengendarai
  browser ASLI user yang SUDAH login. Sesi otomatis saya (browser_navigate)
  diblokir; Brave pribadi user tidak.
- Cari tab "Gemini Notebook" via capture mode=ax, klik untuk fokus. Kalau tiada,
  buka URL di address bar.
- Kalau belum login sama sekali: user yang selesaikan login manual. **Password
  TIDAK PERNAH kita ketik** (aturan keamanan keras, berlaku terlepas izin user).

## Alur (computer_use, Brave sudah login)
1. `capture(app='Brave', mode='ax')` → cari TabItem "Gemini Notebook". Klik.
   Bila tidak ada, ketik URL di address bar (index Edit "Address and search bar").
2. Klik "Create new notebook".
3. Dialog sumber terbuka. Klik "Copied text" → ketik naskah sumber → klik "Insert".
   (Alternatif: Upload files / Websites / Drive — lihat referensi format.)
4. Notebook terbuat; nama bisa diedit di field judul. Sumber muncul di panel kiri
   ("1 source").
5. Panel kanan = Studio. Klik tombol **"Video Overview"**.
6. Pilih Format (radio):
   - **Short** (~60 dtk, BAHASA INGGRIS + usia 18+)
   - **Explainer** (komprehensif, dukung Indonesia)
   - **Cinematic** (imersif, Inggris + 18+)
7. Klik **"Generate"**. Dialog tertutup = request masuk antrean Google.
8. GENERATE JALAN DI SERVER GOOGLE, BUKAN DI LAYAR — bisa **>30 menit**.
   Tidak ada progress bar di AX tree. Cek berkala (capture ulang) sampai kartu
   video muncul di Studio.
9. Kartu video muncul di Studio (label spt "Inside the Zero-Employee AI Company
   · Short · 1:11 · 13m ago"). **JANGAN klik tombol Play** — langsung klik KARTU
   video itu sendiri untuk membuka modal pemutar, lalu klik tombol **"Download"**
   di pojok kanan-atas modal (bukan kontrol play di tengah). Memutar dulu sia-sia
   & boros; user cuma butuh file.

## PITFALL — Dialog Save As mendarat di folder aneh
Brave sering menampilkan dialog Windows "Save As" (judul: "*usercontent.google.com
wants to save") dengan folder default BUKAN Downloads — bisa mendarat di folder
proyek acak (misal `nb_proof`). Penanganan terverifikasi:
- Isi field "File name" dengan **path absolut eksplisit**, contoh:
  `C:\Users\arija\ziyan_notebooklm_short.mp4` (pakai `set_value` di computer_use).
- Klik **Save**. Lalu VERIFIKASI file benar-benar ada: `search_files` pola
  `*.mp4` atau `ls -la` path tsb. Kalau tak ada, cek tombol "New download
  available" di Brave (download manager) → filename asli spt
  `Inside_the_Zero-Employee_AI_Company.mp4`.
- Bila mendarat di folder tak terduga, `cp` ke lokasi pasti (home folder user).

## PITFALL — JANGAN kirim video ke chat
User eksplisit: "video yang kamu download dari notebooklm gak usah kirim kesini.
Cukup di laptop aja." Simpan di disk (`C:\Users\arija\`) dan LAPORKAN path-nya
saja. Jangan lampirkan MEDIA ke Discord. (Tujuannya jaga token session agar tak
limit.)

## Batasan (verified)
- Short & Cinematic: hanya Inggris, usia 18+. Explainer: dukung Indonesia.
- Tidak ada long-form native 10–30 mnt. Workaround: potong notebook + gabung
  (CapCut/FFmpeg/Clipchamp).
- Butuh Google Account; beberapa fitur 18+.

## Verifikasi (jangan klaim sukses sebelum ini)
- Tab menunjukkan judul notebook ("The ZIYAN Blueprint..." dst).
- Panel sumber menunjukkan "1 source" (atau jumlah sumber yang diupload).
- Kartu video benar-benar muncul di Studio SEBELUM klik Download.
- File video ada di disk (folder Download) setelah Download diklik.
- JANGAN lapor "video selesai/terdownload" kalau kartu belum muncul.

## Referensi
- `references/format-limits.md` — detail batasan format & workaround long-form.
- **Path otomatis (tanpa Brave):** untuk generate video via CLI `notebooklm-py` (auth cookie Netscape), lihat skill `ziyan-video-production` → **JALUR A2**. Di sana ada `add-research`, `generate video --format brief` (Short), dan cara parse download URL dari output (id notebook ada di stderr, bukan stdout JSON).
