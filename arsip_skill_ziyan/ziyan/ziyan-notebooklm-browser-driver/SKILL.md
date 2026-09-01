---
name: ziyan-notebooklm-browser-driver
description: "Drive NotebookLM via computer_use when CDP cookie fails."
version: 1.0.0
author: ZIYAN Orchestrator
---

# NotebookLM Browser Driver (ZIYAN) — computer_use Fallback

Gunakan skill ini KALAU `ziyan-notebooklm-autopilot` (CDP cookie) gagal: Brave jalan
tanpa flag `--remote-debugging-port`, atau App-Bound Encryption (Chrome 127+) blokir
baca cookie HttpOnly dari disk (`SID`/`__Secure-1PSIDTS`/`HSID`/`SSID` → value kosong
saat decrypt DPAPI).

**JANGAN** suruh Bos export cookie manual dari DevTools Console — `document.cookie`
CUMA dapat cookie non-HttpOnly. Auth Google semuanya HttpOnly → tidak bisa dipakai
agent. (Konfirm 2026-08-02: Bos jalankan script `copy(document.cookie...)`, hasilnya
cuma log error, bukan JSON auth.)

**Jalan terakhir yang PASTI works:** Bos sudah login di Brave (akun mziyan266) →
agent DRIVE Brave langsung via `computer_use` (background, tidak curi kursor Bos).
Bos sudah setuju pola ini (2026-08-02, "setuju" setelah "biar aku aja.. lama kali pun").

---

## 1. SETUP — Buka Brave di sesi Bos

Bos harus sudah buka `notebook.google.com` dan login. Agent verifikasi via capture:
```python
computer_use(action="capture", app="Brave", mode="som")
```
Cari elemen "Gemini Notebook" / "notebook.google.com" di AX-tree. Kalau tidak ada tab
NotebookLM, minta Bos buka di Brave (bukan Chrome/Edge — computer_use hanya bisa
drive app yang sedang jalan di sesi Bos).

Tutup DevTools (F12 / Ctrl+Shift+I) sebelum mulai — panel DevTools menutupi layout
dan mengacaukan indeks SOM.

---

## 2. URUTAN UPLOAD SUMBER (TERBUKTI works — 2026-08-02)

1. Capture Brave → klik **"+ Create new"** (index biasanya ~39). Notebook kosong kebuat,
   modal "Create Audio and Video Overviews from websites" muncul.
2. Klik **Close/Cancel** modal itu (jangan "Allow"/"Customize").
3. Klik **"Add source"** (panel kiri) → modal "Add source" terbuka dengan tombol
   **Upload files / Websites / Drive / Copied text**.
4. Klik **"Upload files"** → file picker Windows muncul.
5. Di file picker, **ketik path folder lengkap di filename box + Enter**
   (mis. `C:\Users\arija\ziyan_sources_batch`). Hindari klik breadcrumb — tidak
   konsisten antar bukaan.
6. **KLIK 1 FILE** lalu **Open**. Notebook menyerap 1 source.
7. Ulangi step 3–6 untuk tiap file sampai "N sources" lengkap (target 10).

**VERIFIKASI:** panel kiri menampilkan "N sources" + preview ringkasan sebelum lanjut
generate artefak.

---

## 3. PITFALL PICKER (KRITIS — 2026-08-02)

| Gejala | Penyebab | Fix |
|---|---|---|
| Picker crash "Invalid window handle 0x80070578" | **Multi-select** (Ctrl+A / Shift+Click range) | Upload **1 file per Open**. JANGAN select >1. |
| Tab Brave jadi kosong setelah picker | Crash picker menular ke tab | Reload tab (tombol Reload), sumber yang sudah masuk tetap aman. Lanjut sisa file. |
| Error "File not found: Everify-Free-Version-1.0" | Filename box berisi teks sisa dari upload sebelumnya | Klik OK, lalu KLIK 1 file (bukan ketik di filename box), lalu Open. |
| Picker buka di folder salah (Downloads, bukan batch) | Path tidak diketik ulang | Selalu ketik path folder di filename box tiap buka picker. |
| Select all checkbox di panel notebook | Itu select source YANG SUDAH ADA, bukan tambah | Abaikan; pakai "Add source" untuk tambah file baru. |

**Folder batch:** buat dulu folder berisi HANYA `.md` (bersih, tanpa pasangan `.html`
duplikat) untuk percepat:
```bash
mkdir -p /c/Users/arija/ziyan_sources_batch
cp ionq_*.md qi_*.md /c/Users/arija/ziyan_sources_batch/
```
HTML asli bisa diupload tapi raw HTML berat; `.md` hasil konversi lebih ringan & clean.

---

## 4. CATATAN computer_use

- `computer_use` background TIDAK curi kursor Bos — aman dijalankan saat Bos aktif.
- Gunakan `mode="som"` untuk dapat indeks elemen; klik via `element=N`.
- Untuk klik di file picker Windows (Win32 dialog), kadang perlu
  `delivery_mode="foreground"` agar input ter-register.
- `key` dengan `keys="Control+A"` sering gagal di picker Win32 → hindari; klik 1 file.
- Vision analysis kadang return 404 (auxiliary vision routing gagal) — abaikan, ANDALKAN
  AX-tree / SOM indeks, bukan screenshot visual.
- Setelah tiap aksi, `capture` ulang untuk verifikasi state sebelum langkah berikutnya.

---

## 5. LANJUT KE GENERATE (setelah 10 sumber)

Setelah "10 sources" aman, generate 8 artefak via `notebooklm-py` CLI (lihat
`divisi-notebooklm-automation`) — TAPI hanya kalau `storage_state.json` agent valid.
Kalau masih expired, generate artefak JUGA via computer_use (klik "Video Overview" /
"Audio Overview" / "Slide Deck" di panel Studio, tunggu render, download manual).
