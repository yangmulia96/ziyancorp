---
name: ziyan-notebooklm-autopilot
description: Generate NotebookLM via Bos Brave cookies (CDP), no manual login.
version: 2.0.0
author: ZIYAN Orchestrator
---

# NotebookLM Autopilot (ZIYAN)

Generate NotebookLM audio/video TANPA Bos login manual tiap kali. Cookie sesi Brave
diambil agent lewat CDP (Chrome DevTools Protocol) — **JANGAN** minta Bos download/export
cookie manual dari DevTools, itu ribet dan gampang salah format.

Workdir: `C:\Users\arija\ziyan_drive_learn\`
Cookie store: `C:\Users\arija\OneDrive\ziyan_pending\storage_state.json` (JANGAN pernah di-print ke chat)

---

## 1. CARA AMBIL COOKIES (Bos 30 detik, sisanya agent)

### Yang Bos lakukan
1. Tutup semua jendela Brave dulu (biar profil tidak terkunci).
2. Buka Brave dengan remote debugging AKTIF — Bos cukup klik shortcut, atau agent jalankan:
   ```bash
   "/c/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe" \
     --remote-debugging-port=9222 \
     --user-data-dir="C:\Users\arija\AppData\Local\BraveSoftware\Brave-Browser\User Data" &
   ```
3. Di Brave itu, buka `https://notebooklm.google.com` dan pastikan **sudah login** (akun mziyan266).
   Kalau diminta login, Bos login sekali. Selesai — Bos tidak perlu apa-apa lagi.

### Yang agent lakukan (otomatis)
```bash
cd /c/Users/arija/ziyan_drive_learn
python cdp_cookies.py
```
Script ini:
- Connect ke `http://127.0.0.1:9222/json/list`
- `Network.getAllCookies` (browser-wide, termasuk httpOnly — ini kenapa CDP > manual export)
- Filter domain `notebooklm` + `google.com`
- Tulis Playwright `storage_state.json` ke OneDrive.

Output aman untuk dilaporkan: **jumlah cookie + daftar domain saja**. Nilai cookie NEVER printed.

### Verifikasi cookie hidup
```bash
python cdp_nb_check5.py     # via CDP tab baru
python test_nb_access.py    # via Playwright headless
```
Sehat = body page berisi UI NotebookLM ("New notebook" / daftar notebook) dan
FINAL URL tetap `notebooklm.google.com`.

---

## 2. JALANKAN AUTOPILOT

```bash
cd /c/Users/arija/ziyan_drive_learn

# Step 0 — cek CDP + sesi login saja (aman, tidak bikin notebook)
python nb_autopilot.py --dry-run

# Step 1 — generate Video Overview di NotebookLM lalu auto-download ke C:\Users\arija\ziyan_videos
python nb_autopilot.py --url "<URL sumber/YouTube>" --wait 20

# Step 1b — WAJIB verifikasi file benar-benar turun (deteksi selesai masih bisa false-positive)
ls -la /c/Users/arija/ziyan_videos

# Step 2 — upload ke YouTube Compound Daily (default DRY-RUN, tambah --run untuk eksekusi)
python upload_pipeline.py --max 1            # dry-run
python upload_pipeline.py --max 1 --run      # upload beneran (jadwal random)
python upload_pipeline.py --max 1 --run --now  # publish langsung
```

Flag penting:
- `nb_autopilot.py`: `--url` sumber, `--wait` menit maks render, `--keep-tab`, `--dry-run`
- `upload_pipeline.py`: `--run`, `--now`, `--max N`, `--no-router` (skip 9router, pakai template judul/desc murni)

Catatan operasional:
- `nb_autopilot.py` baca `storage_state.json`; kalau tidak ada / expired → berhenti dan lapor.
- Audio >25MB dikompres dulu: `ffmpeg -i in.m4a -b:a 48k -ac 1 out.m4a` (30MB → ~8MB).
- `upload_pipeline.py` pakai `youtube_token.json` (OAuth) — lihat skill `ziyan-youtube`.
- Rate: maksimal beberapa generate per hari. Jangan spam — Google anti-bot agresif.

---

## 3. TROUBLESHOOTING

| Gejala | Penyebab | Fix |
|---|---|---|
| `test_nb_access.py` redirect ke `accounts.google.com` | **Cookies expired** | Bos buka Brave (langkah 1), refresh NotebookLM sampai kelihatan login, agent jalankan ulang `cdp_cookies.py` |
| `Connection refused 127.0.0.1:9222` | Brave jalan tanpa flag debugging | Tutup SEMUA Brave, buka ulang pakai `--remote-debugging-port=9222` |
| `SAVED 0 cookies` / domain kosong | Profil `--user-data-dir` salah (Brave buka profil kosong) | Pakai path User Data asli Bos, bukan temp dir |
| Page load tapi body kosong/spinner terus | Cookie sah tapi butuh waktu render | Naikkan `time.sleep`/`wait_for_timeout` ke 12–15 detik |
| Muncul "unusual traffic" / captcha | Terdeteksi anti-bot | **STOP**, jangan retry. Lapor Bos, jeda minimal 24 jam |
| Upload YouTube 401/403 | `youtube_token.json` expired | Refresh OAuth, lihat skill `ziyan-youtube-blogger-oauth` |
| `nb_autopilot.py` print "SELESAI (auto-download)" tapi MP4 tidak ada di `C:\Users\arija\ziyan_videos` | **BUG KNOWN (2026-08-02)**: deteksi selesai false-positive, nama file (`_ctest.mp4`) hasil tebakan DOM, download event tak pernah selesai | Selalu verifikasi `ls -la /c/Users/arija/ziyan_videos`. Fix: tunggu `Browser.downloadProgress` state=completed sebelum klaim sukses (deliverable Agent A) |


Umur cookie Google ~beberapa hari sampai beberapa minggu. Kalau autopilot mulai gagal,
**cek cookie dulu** sebelum debug hal lain.

---

## CRITICAL RULES
- Cookies = "cap VIP" (sesi sah), BUKAN password. Tapi tetap: JANGAN print isi cookies ke chat/log/laporan.
- Kalau akun kena blokir → STOP total, lapor Bos.
- Video WAJIB dari NotebookLM (peraturan Bos).
- Kalau cookies invalid → minta Bos buka Brave, jangan coba akal-akalan login otomatis.

## REFERENSI
- `C:\Users\arija\ziyan_drive_learn\laporan_pabrik_youtube.md` — breakdown lengkap
- `C:\Users\arija\ziyan_drive_learn\transkrip_audio.txt` — transkrip
- `C:\Users\arija\ziyan_drive_learn\AUTOPILOT_README.md` — README operasional
- 4 pilar: niche down, organize sources, transform to content, expand
