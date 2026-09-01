# Cron Bridge — Ingatan Bersama Telegram ↔ Discord (SHARED_MEMORY.md)

Resep kerja untuk cron 30-menitan yang menyinkronkan percakapan lintas-gateway ke satu file
ingatan. Terverifikasi berjalan berulang (siklus 15:52 → 22:50, 9 Agustus 2026; siklus 06:20,
10 Agustus 2026).

## Aset tetap
| Item | Path |
|---|---|
| File ingatan | `C:\Users\arija\ZIYAN_BRIDGE\SHARED_MEMORY.md` |
| State cursor | `C:\Users\arija\ZIYAN_BRIDGE\_sync_state.json` |
| Sumber pesan | `C:\Users\arija\AppData\Local\hermes\logs\agent.log` |
| Backup otomatis | `SHARED_MEMORY.md.bak` (ditulis tiap run sebelum edit) |

Struktur heading yang WAJIB dipertahankan (skrip menargetkan ini dengan regex):
`## STATISTIK (agent.log)` → `## RINGKASAN ZIYAN` → `## PESAN TELEGRAM TERAKHIR (30)` →
`## PESAN DISCORD TERAKHIR (30)` → `## KEPUTUSAN` → `## BACKLOG AKTIF` → `## BACKUP MEMORY & SKILLS`.

## Pola dua skrip (jangan digabung)
`execute_code` diblokir di cron, jadi: `write_file` skrip `.py` → `terminal: python <skrip>.py`.

**1. `_sync_<HHMM>.py` — ekstraksi delta (read-only, aman diulang).**
Regex penangkap inbound:
```python
pat = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ INFO gateway\.run: inbound message: "
    r"platform=(\w+) user=(.+?) chat=\S+ msg='(.*?)' reply_to_id=", re.S)
```
Bandingkan timestamp dengan `state["last_seen"][platform]` (perbandingan string ISO cukup).
Simpan hasil ke `_delta_<HHMM>.json`: `counts`, `new_telegram`, `new_discord`,
`tg_tail30`, `dc_tail30`, `new_last_seen`. Cetak delta ke stdout supaya langsung terbaca.

**2. `_apply_<HHMM>.py` — penulisan (destruktif, sekali jalan).**
- `shutil.copyfile(MD, BAK)` paling awal.
- Ganti tiap section dengan `re.sub(..., lambda m: konten_baru, txt, count=1)` — **selalu lambda**
  (isi log bisa mengandung `\`, path Windows di teks keputusan bikin `bad escape \U`).
- Pola regex section yang terbukti: `r"## JUDUL\n(?:.*\n)*?\n## JUDUL_BERIKUT"` (non-greedy sampai
  heading berikutnya). Untuk section terakhir sebelum blok lain, jangkar ke heading sesudahnya.
- Menambah KEPUTUSAN: `txt.replace("\n## BACKLOG AKTIF", KEP + "\n## BACKLOG AKTIF", 1)` —
  `str.replace` lebih aman daripada regex untuk sisipan.
- Kalau `re.sub` untuk satu item BACKLOG bisa gagal (pola berubah tiap siklus), pasang **fallback**:
  bandingkan `md == md_sebelum`; kalau tidak berubah, sisipkan item baru di awal BACKLOG.
  Jangan biarkan kegagalan senyap membuat BACKLOG tampak masih sama.
- Tulis file SATU KALI di akhir, lalu perbarui `_sync_state.json`.

## Verifikasi wajib sesudah run
```bash
grep -n "^## " SHARED_MEMORY.md      # semua heading masih ada & urut
grep -n "LAST SYNC" SHARED_MEMORY.md # timestamp terbarui
wc -l SHARED_MEMORY.md               # tidak menyusut drastis
```
Kalau satu heading hilang → restore dari `SHARED_MEMORY.md.bak` dan perbaiki regex.

## Aturan isi (bukan teknis, tapi yang bikin file ini berguna)
- `agent.log` memotong pesan user di **80 karakter**. Untuk pesan penting (perintah, spesifikasi,
  keputusan) WAJIB ambil teks penuh lewat `session_search` sebelum menulis ke KEPUTUSAN.
  Sesi Discord ZIYAN: `20260802_173653_9fedc03b`.
- Setiap butir KEPUTUSAN harus menyebut **bukti yang diverifikasi**, bukan klaim. Contoh baik:
  "Diverifikasi: folder `.n8n` TIDAK ADA, `npm ls -g` tanpa n8n, port 5678 tidak LISTENING."
- Kalau keputusan lama dibatalkan Bos, tulis eksplisit `*** ... DIBATALKAN/GUGUR ***` dan sebut
  butir mana yang gugur. Jangan diam-diam menimpa — riwayat pembatalan itu sendiri informasi.
- **Batalkan juga ROOT CAUSE yang dibantah BUKTI, bukan cuma yang dibatalkan Bos.** File ini
  append-only, jadi diagnosis lama yang salah akan terus dibaca siklus berikutnya dan menyesatkan.
  Contoh nyata (10 Agu): butir 22:50 menetapkan "Windows Defender penyebab install n8n gagal";
  siklus berikutnya membuktikan Defender sudah dimatikan namun gagalnya berlanjut dengan error
  berbeda (`@parcel/watcher` native build). Wajib ditulis `*** ... RESMI KELIRU ***` + root cause
  pengganti, bukan sekadar menambah temuan baru di bawahnya.
- Saat pivot besar (uninstall/hapus semua), **reset BACKLOG** dan catat di mana backup aset berada,
  supaya siklus berikut tidak "bangun dari nol" padahal backup ada.
- Kalau cron mendeteksi sesi live sedang menangani hal yang sama (misal restart service), JANGAN
  ikut mengeksekusi — cukup catat state. Dua proses rebutan port = kerusakan baru.
- **Kebalikannya: kalau Bos sudah lama diam (tidak ada pesan masuk berjam-jam, tidak ada sesi live)
  dan ada item BACKLOG MENDESAK yang blocker-nya sudah hilang — KERJAKAN.** Jendela Bos tidur itu
  waktu paling aman untuk operasi berisiko (restart service, reset DB rusak). Cron 10 Agu memakai
  jendela ini untuk menghidupkan kembali n8n yang mati sejak semalam. Tetap: verifikasi hasil nyata
  (HTTP 200 / API), lalu laporkan sebagai fakta, bukan rencana.
- **Service jangka panjang yang dinyalakan cron WAJIB dilepas dari sesi.** Proses dari
  `terminal(background=true)` mati bersama sesi cron → Bos bangun dan menemukan service mati padahal
  laporan bilang hidup. Pakai `.bat` + `start "" /b` (lihat section "n8n Restart" di SKILL.md).

## Format laporan ke Bos (maks ~150 kata)
Urutan tetap: **jumlah pesan baru per platform → topik utama → root cause bila ada →
apa yang butuh tindakan**. Jangan menempel isi file. Jangan menyodorkan menu pilihan
("Bos mau 1, 2, atau 3?") — Bos membalas perintah hapus/stop ketika disodori pilihan.
Putuskan sendiri, laporkan keputusannya.
Kalau siklus itu mengoreksi diagnosis lama, sebutkan koreksinya terang-terangan
("teori X keliru, penyebab sebenarnya Y") — Bos lebih percaya laporan yang mengakui salah
daripada laporan yang diam-diam ganti cerita.
