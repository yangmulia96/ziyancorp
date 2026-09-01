---
name: ziyan-delivery
description: Output ke Bos yang mobile (voice over, email, OneDrive).
category: ziyan
---

# ZIYAN Delivery — Output ke Bos yang Mobile

Bos (Komisaris) sering di jalan (nyetir) atau cuma buka HP. Output agent harus bisa dikonsumsi tanpa laptop. Tiga kebutuhan berulang: **voice over** (Bos mau dengar, bukan baca), **cek email**, dan **akses file di HP**.

## 1. VOICE OVER (TTS lokal)

Bos mau laporan dibacakan saat nyetir.

**Aturan wajib:**
- **JANGAN** generate via inline bash (`python3 -c "..."`) → quote/bash EOF error (`unexpected EOF while looking for matching backtick`). SELALU tulis script ke file lalu jalankan.
- **edge-tts GAGAL** di jaringan ini (koneksi ke speech.platform.bing.com terblokir / SSL error). Pakai **pyttsx3** (lokal, gratis, tanpa internet).
- pyttsx3 di venv Hermes (`python3`) jalan. Voice SAPI5 default (robotik tapi jelas).
- Bersihkan marker markdown (`#`, `*`, `>`) sebelum TTS biar bacanya natural.

**Template:** lihat `scripts/gen_voiceover.py` — baca `.md`, strip markdown, save ke `.mp3`.

**Pengiriman ke Bos:** `MEDIA:<path>` TIDAK auto-attach ke Discord di setup ini (terbukti: Bos bilang "gak ada aku terima apa apa"). JANGAN andalkan MEDIA. Sebaliknya **copy ke `OneDrive/ziyan_pending/`** → Bos buka app OneDrive di HP → putar. Ini jalan pasti.

```
cp hasil.mp3 "OneDrive/ziyan_pending/nama.mp3"
```

## 2. CEK EMAIL (Gmail via imaplib)

Bos: "tolong cek email yang barusan masuk".

**Masalah:** `himalaya` CLI tidak ter-install di laptop ini, dan `curl` ke install script GitHub raw gagal (jaringan blokir). `pip install himalaya` salah package (ML library).

**Jalan yang jalan:** Python `imaplib` baca langsung config himalaya yang sudah ada (`C:\Users\arija\.config\himalaya\config.toml` — password sudah tersimpan di situ, jangan print).

**Script:** lihat `scripts/check_mail.py` — list 10 terbaru + baca isi by ID, TANPA print password.

**Catatan keamanan:** password di config.toml adalah app-password Gmail (bukan saya yang tulis). Script login pakai nilai itu, TIDAK pernah print ke output.

### Tambah akun Gmail kedua (terverifikasi 2026-08-02: mziyan266)
- Bos buat App Password di Google Account → taruh di OneDrive `ziyan_pending/Ziyan key.docx` (bukan chat).
- Baca .docx tanpa library (`python-docx` tidak ter-install) → **unzip lalu regex**:
  ```python
  import re, zipfile
  z = zipfile.ZipFile('OneDrive/ziyan_pending/Ziyan key.docx')
  xml = z.read('word/document.xml').decode('utf-8')
  text = ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml))
  ```
  App password = 16 char (4 grup x 4 huruf, spasi dipisah). Simpan ke `ziyan_keys.env` + tambah section `[accounts.nama]` ke config.toml.
- **PITFALL TOML**: jangan pakai `imap.tls.reject_unknown_certs = false` bersama `imap.tls = true` (bentrok → TOMLDecodeError "Cannot overwrite a value"). Cukup `imap.tls = true`. Sama untuk `smtp.tls.encryption` vs `smtp.tls`.
- Test: `imaplib.IMAP4_SSL('imap.gmail.com',993).login(user,pw)` → "LOGIN SUKSES".
- Setelah test, **hapus file .docx dari OneDrive** (transit sementara).
- imaplib fetch email besar bisa timeout di foreground → jalankan background, tulis hasil ke `_out.txt`, baca file.

## 3. AKSES FILE DI HP

Semua hasil yang Bos butuh di mobile → taruh di `OneDrive/ziyan_pending/`. OneDrive auto-sync ke HP Bos. Jangan kirim lewat Discord attachment untuk file besar.

## 4. OCR GAMBAR (saat Bos kirim screenshot)
Bos sering kirim gambar (OneDrive panel, dll) di Discord. Vision API (`vision_analyze`) GAGAL di setup ini (API key invalid, bukan 9router).

**Jalan yang jalan:** Tesseract CLI ada di `C:\Program Files\Tesseract-OCR\tesseract.exe` tapi TIDAK di PATH.
```bash
export PATH="/c/Program Files/Tesseract-OCR:$PATH"
tesseract "path/ke/gambar.jpeg" stdout 2>/dev/null
```
- `pytesseract` Python wrapper GAGAL (TesseractNotFoundError) kalau PATH tidak diset → panggil binary langsung via `export PATH` di atas.
- Untuk .docx (bukan gambar): pakai unzip+regex (lihat section Email).

## PITFALLS
- `MEDIA:<path>` di Discord TIDAK terlampir otomatis → selalu fallback OneDrive copy.
- pyttsx3 inline bash = error quote → selalu file script.
- edge-tts = network blocked → pyttsx3.
- vision_analyze GAGAL (API key invalid) → fallback OCR tesseract (PATH manual) atau unzip docx.
- Jangan print credential/appPassword ke chat (insiden leak Gemini key di masa lalu).
- **Password/credential TIDAK BOLEH dikirim di chat** (Bos tegas: "Aku kirim kesini aja password" → saya TOLAK, arahkan ke OneDrive/ziyan_pending/). Ini mutlak, berlaku semua layanan (Gmail, GitHub, YouTube, dsb).
- **STYLE: jangan over-explain credential exchange di chat** (Bos protes: "Lama kali kayak gini.. buang buang waktu"). Kalau Bos sudah taruh file di OneDrive, LANGSUNG baca → pasang → konfirmasi singkat. Jangan ulang panjang lebar cara kerja tiap kali.

## SCRIPT PERMANEN (re-create kalau hilang)
- `scripts/check_mail.py` — baca INBOX via imaplib, TANPA print password. Argumen: account (default arizalkempo).
- `scripts/gen_voiceover.py` — baca `.md`, strip markdown, pyttsx3 → `.mp3`. Argumen: input.md, output.mp3.
- `scripts/start_9router.bat` — shortcut auto-start 9router (lihat skill ziyan-ai-infra).

## REFERENSI
- `references/delivery.md` — catatan observasi sesi (MEDIA gagal, alur OneDrive).
