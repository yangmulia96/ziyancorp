# Upload YouTube Terjadwal + Verifikasi Berbasis API (Compound Daily)

Terverifikasi 4 Agu 2026 (cron job artefak "OpenAI Math" → video `ZENnmjAtp54`).
Catatan ini ditaruh di sini karena skill `divisi-youtube-ziyan` dan
`divisi-notebooklm-automation` milik Bos (user-owned, tidak boleh ditulis agent).
Kalau Bos menjalankan `hermes curator adopt <skill>`, pindahkan isi ini ke sana.

## 1. Pilih file video yang BENAR
NotebookLM mengeluarkan DUA artefak bertipe `Video`; nama file tergantung urutan download:
| Peran | Ciri | Contoh sesi ini |
|---|---|---|
| Explainer (Long, 16:9) | ~39 MB, ~490 dtk | `Video_Explainer.mp4` == `Video_2.mp4` |
| Brief (Short, 9:16) | ~9,7 MB, ~73 dtk | `Video_Brief.mp4` == `Video.mp4` |

Jangan tebak dari nama. Buktikan:
```bash
cd /c/Users/arija/ziyan_artifacts/<notebook>
md5sum Video_Explainer.mp4 Video_2.mp4          # hash sama = file sama
ffprobe -v error -show_entries format=duration -of csv=p=0 Video_Explainer.mp4
```
**Quirk ffprobe di git-bash/MSYS:** path gaya `/c/Users/...` ditolak
(`No such file or directory`) walau file ada. Solusi: `cd` ke foldernya dulu lalu pakai nama
file relatif, atau pakai path Windows `C:\...`.

## 2. Konversi jadwal
`publishAt` RFC3339 UTC. WIB = UTC+7.
- 14:00 WIB → `T07:00:00Z`
- "besok" dihitung dari `date` host, bukan asumsi. Cek `date` dan `date -u` sekaligus —
  host bisa sudah lewat tengah malam UTC (contoh: 4 Agu 23:22 WIB = 4 Agu 16:22 UTC).
`privacyStatus` WAJIB `private` bila `publishAt` diisi (aturan YouTube).

## 3. Perintah upload
```bash
cd /c/Users/arija && python3 ziyan_credentials/upload_youtube_scheduled.py \
  "C:\Users\arija\ziyan_artifacts\<nb>\Video_Explainer.mp4" \
  "Judul Maksimal 100 Karakter" \
  "C:\Users\arija\ziyan_artifacts\<nb>\yt_description.txt" \
  "tag1,tag2,tag3" \
  "2026-08-05T07:00:00Z"
```
- Judul boleh mengandung apostrof selama dibungkus kutip ganda bash.
- Judul default yang bagus = heading H1 dari `Report.md`; deskripsi = `yt_description.txt`.
- File 40 MB dibaca sekaligus ke memori lalu PUT → butuh >60 dtk. Jalankan `background=true`
  dan poll; `process(action='wait')` di-clamp 60 dtk per panggilan.

## 4. Verifikasi WAJIB (dua sisi)
Sebelum upload — buktikan token → channel:
```
GET https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true
youtube_token_compound.json         -> UCzWib2-2CPkWo315fzucaUw | Compound Daily
youtube_token_compounddaily_v1.json -> UCzWib2-2CPkWo315fzucaUw | Compound Daily
youtube_token.json                  -> UCzWib2-2CPkWo315fzucaUw | Compound Daily
youtube_token_ziyanmalik.json       -> UCend05oI081uEVPTNa934Bg | Ziyan Malik (JANGAN untuk Compound Daily)
```
Probe siap pakai: `scripts/probe_youtube_tokens.py` (tulis ke `ziyan_pending/`, jalankan via
`terminal`). Tiga token berbeda menunjuk channel yang sama — pakai `youtube_token_compound.json`
sebagai default supaya konsisten dengan `upload_youtube_scheduled.py`.
Sesudah upload — jangan percaya stdout script, tanya API:
```
GET videos?part=snippet,status,processingDetails,contentDetails&id=<VIDEO_ID>
```
Yang harus benar: `channelId`, `privacyStatus=private`, `publishAt` sesuai jadwal,
`uploadStatus=uploaded`. `processingStatus=processing` dan `duration=P0D` beberapa menit
pertama itu NORMAL — jangan dilaporkan sebagai kegagalan.

## 5. Bentuk laporan ke Bos
Tabel ringkas: Video ID, URL, judul, channel, privasi, jadwal publish (WIB + UTC),
uploadStatus, jumlah tag, panjang deskripsi — plus daftar artefak yang tersisa untuk
kanal lain (Short, Telegram voice, thread X, carousel LinkedIn, paket Gumroad).

## 6. Menjalankan ULANG poll script (idempotency) — konfirmasi 5 Agu 2026
Cron kedua atas notebook yang sama (`poll_openai_math.py`, video Long → `JX87PqCwL3Q`,
jadwal `2026-08-06T07:00:00Z`) membuktikan resep di atas sekali lagi, plus tiga jebakan:

- **Script TIDAK idempotent.** Penghitung `seen` di dalamnya reset tiap run dan download pakai
  `--force`, jadi run kedua menulis nama generik (`Video.mp4`, `Video_2.mp4`, `Audio.mp3`, …)
  berdampingan dengan hasil run pertama (`Video_Explainer.mp4`, `Video_Brief.mp4`, `* (2).*`).
  Folder membengkak ~113 MB duplikat identik. Cek `ls -la` folder artefak SEBELUM menjalankan
  ulang; kalau 8 tipe sudah ada dan >0 byte, poll hanya untuk memastikan status `completed`.
- **`Downloaded 9/8` BUKAN error.** NotebookLM punya dua artefak bertipe `Video` (Explainer +
  Brief), jadi 9 file untuk 8 tipe artefak itu hasil yang benar. Jangan laporkan sebagai anomali.
- **Jangan hapus duplikat tanpa izin Bos.** Laporkan saja ukurannya ("~113 MB bisa dibuang")
  dan tunggu perintah — penghapusan file di folder aset Bos bukan keputusan agent.

Cara aman menentukan Long setelah run berulang (jangan andalkan nama):
```bash
cd /c/Users/arija/ziyan_artifacts/<nb>
md5sum Video*.mp4                     # kelompokkan file identik
ffprobe -v error -show_entries format=duration -show_entries stream=width,height \
  -of default=nw=1 Video_Explainer.mp4   # Long = 1280x720, ~490 dtk
```

